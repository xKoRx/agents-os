---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures — Runtime Pools]]"
  - "[[EF-PROD-PRD5-DEV-PREFLIGHT-AND-COVERAGE-20261026]]"
  - "[[EF-PROD-GOD-05-MANAGER-ADJUDICATION]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-26"
updated: "2026-10-26"
---

# EF-PROD PRD.5 — Manager Review, 2026-10-26

## Propósito

Adjudicar PRD.5 y distinguir **inventario apto** de **migración segura**. Primary Manager GPT-6, source review GitHub sobre `xKoRx/echo@c2d713579da559e9d7e02ea7f2ebf21b8818283e` (código producto igual a `0e17c4d3f1179cde709f923c8dd28e8cd853afc9`, delta de 11 test files+tooling); Agents-OS evidencia `EF-PROD-PRD5-DEV-PREFLIGHT-AND-COVERAGE-20261026`. No se ejecutaron pruebas ni accedió físicamente a host .75 durante este dictamen.

## Contenido

### Decisión vinculante

- **PRD.5 INVENTORY / G-ENV-DEV-PREFLIGHT = ACCEPTED_AS_RO_EVIDENCE.** DEV existente: Flink/StateFun compartido en host .75, Compose project `flink`; FX+Futures 17 ingresses, checkpoint vigente host-local; sin savepoint; M1 vigente at-least-once. PROD intacto. **No crear tercer Flink, ni Docker stack, VM, LXC, Kafka/ETCD extra, ni mover topología.**
- **PRD.5 OWNER WINDOW = NOT_AUTHORIZED_YET.** La tarjeta de despliegue está preparada por agente, pero NO prueba todavía migración/snapshot reproducible: lo detectado en SOURCE abajo puede provocar discontinuidad o dejar la restauración bloqueada. Un restart compartido FX/Futures sin un snapshot completo y compatible es un riesgo económico, aunque Futures esté desarmado.
- **G-IMPL = BLOCKED_RECOVERY_MIGRATION_AND_COVERAGE.** El trabajo anterior de GI-2 conserva progreso y laboratorio L3 positivo en su alcance; no contradice estos problemas de *migración desde el estado LEGACY efectivo*. Se requiere un **solo cierre mínimo**, no otro GOD, B1/B2/B3 ni rediseño.
- **G-ENV/G-REC/G-FEED/SIM/PROD = NOT_CERTIFIED.** No desplegar ni reiniciar servicios compartidos por este documento.

### P0-G5A — RecoveryManifest sellado con datos parciales/sintéticos

**Código verificado:** `v3/core/cmd/echo-runtime-control/seal.go`, función `runSeal`:
1. CLI exige un solo `--ingress-id --topic --consumer-group` y crea `Ingresses: []recovery.TopicOffset{{...}}`; el job DEV tiene **17 ingresses FX/Futures**. No representa ni contrasta todos los offsets/particiones/identidades del checkpoint y la fuente de offsets es Kafka **high watermark ACTUAL**, no el conjunto de offsets del checkpoint. HWM posterior ≠ frontera causal restaurada.
2. `DomainScope: recovery.DomainScopeFutures` aunque DEV comparte job de FX+Futures. La selección de scope debe coincidir con el job real; no es una etiqueta cosmética.
3. `JobGraphDigest` es hash sintético de un ingress/topic/grupo, `MaxParallelism:1` constante, `ConfigSnapshotRevision:1` constante, `Artifacts[].ArtifactDigest` derivado de una cadena en vez del binario y `CompletedAt:time.Now()` en lugar del tiempo de Flink. No acreditar esos campos como identidades reales. C-REC-1/M01 exige source authority o BLOCKED.
4. El shell `master-restore-args` y el path oficial del entrypoint están bien encaminados, pero no subsanan un manifest que describa otra frontera.

**Mandato mínimo:** obtener/validar TODOS los ingress offsets reales incluidos en el checkpoint y sus topic IDs+particiones, obtener JobGraph/UIDs/maxParallelism/roles y hashes/revisiones reales, acotar scope al deployment compartido. Si Flink 1.14/StateFun 3.2 no expone directamente offsets/roster, no fabricarlos desde HWM: implementar lector/verificación offline real del checkpoint o negar seal y registrar la brecha. Mantener IDs de fuentes sin resets oportunistas. Reutilizar `seal`, SDK y restore existentes.

### P0-G5B — Backup NO independiente: sólo copia _metadata

**Código verificado:** `seal.go` lee `_metadata` de checkpoint y escribe SOLO esa copia en `<storage-root>/objects/<lineage>/chk-.../_metadata`; el manifest y el restore apuntan a la copia. Para checkpoint incremental RocksDB, `_metadata` puede contener referencias a archivos/SST externos; copiar solamente el metadata no vuelve relocatable/independiente el estado. DEV ahora usa checkpoint host-local (checkpoint 1286, savepoints vacíos). Además un segundo path sobre el MISMO host no es copia independiente. Documento oficial Flink 1.14 `docs/ops/state/savepoints` diferencia savepoints relocatables de checkpoints generalmente NO movibles; `docs/ops/state/checkpoints` permite restore desde _metadata SÓLO si sus dependencias siguen accesibles.
**Mandato mínimo:** plan de corte DEV respaldado con savepoint consistente completo (o checkpoint integral con dependencias verificadas y misma URI/mount accesible), identidad/offsets sellados y copia independiente de host con ensayo de restore. No borrar el checkpoint original ni asumir que un `cp _metadata` basta. Rollback de FX+Futures se valida en la misma frontera antes de reiniciar, nunca restart fresh para salir del bloqueo.

### P0-G5C — Migración de markers sobre keys LEGACY existentes

**Código verificado:** `v3/core/internal/functions/owner_continuity.go`: `checkContinuity` (RECOVER) rechaza `RosterActive` sin marcador `continuity` (`StateMissingInRecoveryError`). El release nuevo añade `OwnerContinuitySpec`; el checkpoint activo fue creado por el release viejo SIN este ValueSpec. La afirmación “ValueSpecs sólo aditivos ⇒ restore compatible” no demuestra que el guard permita procesar keys históricas. Marcar keys legacy como `BIRTH` para saltar el bloqueo falsearía el contrato.
**Mandato mínimo:** validar en una copia real/sanitizada del checkpoint DEV que EXISTING owners FX/Futures mantienen estado y son capaces de migrar su marker mediante un procedimiento explícito, transicional, idempotente y con identidad/fingerprint/roster del estado previo, seguida de checkpoint completo y modo estricto. Si no puede preservarse el state económico, BLOCKED; no cold-start para “arreglar” el error. No relajar el guard RECOVER indefinidamente.

### QA y trayectoria operativa

Coberturas actuales reportadas: archivos Go nuevos **2532/2734=92.61%** y diff-aware **409/518=78.96%**, pisos GOD-03 ≥95% aún incumplidos. El delta `0e17c4d3..c2d71357` sólo cambia tests/tooling; no es motivo por sí solo para otro rediseño. Terminar tests útiles de paths nuevos y diff-aware con evidencia sin gaming, pudiendo utilizar infraestructura de pruebas preexistente/aislada. No usar DEV Kafka para crear topics de prueba. Si el 95% real no es factible sin falsear semántica, remitir excepción explícita a Manager (exclusivamente DEV feed-only), sin marcar G-IMPL accepted.

**Orden mínimo:** (1) normalizar `seal` al job REAL/17 ingresses y sellar checkpoint completo; (2) proteger datos con savepoint/copia independiente con dependencias; (3) probar migración de marcador legacy→estricto y restore FX/Futures; (4) QA + release card/rollback con hashes; (5) re-review Manager; (6) sólo entonces ventana Owner para actualizar **MISMO** Flink DEV existente, observation-only/FX seguro. No tocar PROD, no cuentas, no órdenes. Owner autorizará fecha/ventana de interrupción de FX después del resultado, no por haber terminado PRD.5 RO.

**No es un tercer Flink, no es rediseño GOD.**

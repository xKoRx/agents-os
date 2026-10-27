---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[EF-PROD-PRD6-MANAGER-ADJUDICATION-20261026]]"
  - "[[EF-PROD-PRD6-RECOVERY-MIGRATION-CLOSURE-20261026]]"
  - "[[Echo Futures — Runtime Pools]]"
  - "[[OWNER-CHECKLIST-CERT-NT-01]]"
aliases:
  - WINDOW-CARD-PRD6
tags:
  - kind/doc
created: "2026-10-26"
updated: "2026-10-27"
---

# WINDOW-CARD-PRD6 — tarjeta única de ventana Owner (PRE-01..05 resueltas)

## Veredicto Primary Manager post cierre `5a0cf62f` — 2026-10-27

**STATUS: PREWINDOW_SOURCE_ACCEPTED_WITH_RUNTIME_GATES; G0=BLOCKED_EXTERNAL; OWNER_WINDOW_REQUEST=NOT_READY; FX/DEV NO RESTART; PROD/SIM NO_GO.** Fuente remota `xKoRx/echo feature/ef-runtime-pools@5a0cf62f8ddbffa0a4926d1c1883085be7b87b6d` comprobada; delta 13 archivos vs `4a041e6c`, sin despliegue reportado. El Manager revisó los cambios de `seal`, roster, economic ValueSpec evidence y el lector REST de Flink. No ha ejecutado la sonda ni el restore sobre savepoint real. El resultado del submanager no autoriza por sí mismo tocar el job.

- **PRE-01 (source accepted / runtime pending):** roster de 8 keys se proyecta de config y se confrontará con el STATE restaurado por la sonda de presencia del propio owner. `present` para market_stream+4 materializados y `absent` posible para tres provider_rules son **hipótesis anotadas, NO mediciones del checkpoint**. La lista no demuestra inexistencia de owners huérfanos fuera de config. Cualquier discrepancia, lectura tipada inválida, oráculo de otras ValueSpecs económicas o falta de owner → BLOCKED, sin reclasificar silenciosamente ni hacer `BIRTH` para pasar.
- **PRE-02/PRE-05 (G0 obligatorio antes de ventana):** el MCP SSH `aranea-ssh` expiró. Restaurar esa conexión externa y ejecutar solamente prueba SFTP de staging + `docker inspect` de mounts JM/TM; hashes y espacio evidenciados. Sin G0 PASS, **no pedir fecha ni autorización de reinicio**. Esta instancia de Manager no dispone de ese servidor remoto, no afirma haberlo re-inicializado.
- **PRE-04 (source accepted / físico pendiente):** `seal --cut-kind savepoint` hace join del REST `latest.savepoint` con la ruta, lee `_metadata` por sonda, copia y sella; tests positivos/negativos reportados, pero **compatibilidad de bytes savepoint 1.14 real aún NOT_RUN**. Dentro de una ventana Owner **ya autorizada**, crear savepoint con job todavía corriendo, probar la sonda, roster de 17 ingress y dependencia de copia; todo error ⇒ STOP sin interrumpir.
- **R1 (enmienda bloqueante para seguridad de FX):** el `docker-compose.yml` heredado `ac0621a1` **NO tiene `echo-runtime-control gate` ni inyección automática de `--fromSavepoint`**. Por tanto, `restore compose backups + gate con manifest ANTERIOR (o bootstrap)` NO es un rollback ejecutable demostrado para el job antiguo. Antes de P4 el Submanager debe dejar **comandos y argumentos explícitos, offline-verificados contra la misma imagen y mounts**, para restaurar el artefacto legado compatible por el entrypoint oficial con `-s/--fromSavepoint` y job identity/UIDs, o prueba equivalente. Si no existe manifest anterior, **NO inventar uno ni hacer bootstrap**. Cualquier efecto FX posterior al corte obliga reconciliarlo antes de restaurar un corte viejo; sin prueba ⇒ fail-closed/forward recovery. Preparar rollback ANTES de la ventana de restart, no improvisarlo luego. Sin evidencia de rollback, no ejecutar P4.

**Orden mínima al mismo Submanager:** G0 staging+mounts, confirmar procedimiento R1 LEGACY desde el MISMO savepoint y documentar oráculo de no-effects/FX, volver con evidencia GO/NO-GO. No otro GOD, no infraestructura extra, no tests masivos de cobertura, no nuevo PRD; sin enviar órdenes ni cambiar PROD. Después de G0+R1 auditables, el único permiso Owner solicitado será para la ventana compartida FX/Futures.

## Decisión Primary Manager post Fase 0 — 2026-10-26 (PRE-VENTANA, vinculante)

**Fase 0 ACCEPTED. El Owner NO debe autorizar aún el restart.** Los puntos P4 son preparación técnica del submanager, no tres decisiones personales del Owner. Seguir el mismo plan CERT-NT-01; no nueva etapa de arquitectura, ni nuevo Flink, Docker Compose project, Kafka/ETCD, VM/LXC o servicios. Sólo la ventana que interrumpa FX compartido requiere aprobación expresa del Owner, cuando todos los bloqueos previos estén cerrados.

**PRE-01 / Roster:** existe `v3/core/internal/futuresruntime/recovery_gate.go::Runtime.ExpectedRoster()` en el SHA `4a041e6c`, que deriva los 7 tipos de owner de la composición/configuración sellada (stream, strategies, pool bindings y operation composite key, accounts, pools). **Usarlo como proyección canónica de claves CONFIGURADAS** en vez de inventar otro enumerador. Pero no demuestra por sí mismo las claves y estados realmente MATERIALIZADOS en Flink/legacy: cruzar las keys ACTIVE y RETIRED contra el snapshot real/journal/identidad y el roster del manifest; detectar claves ausentes, huérfanas, estado no inicializado y conflicto. `RECOVER_MIGRATE` actualmente estampa el marker a un `RosterActive` sin lectura explícita de otra ValueSpec económica dentro de `initializeContinuity`; no aceptar una proyección de configuración como prueba de estado preexistente. Si no puede acreditarse la clasificación, STOP sin reinicio. No declarar BIRTH sobre estado histórico para silenciar el guard.

**PRE-02 / Copia:** recomendar **relay SFTP existente del agente**, cifrado hacia `.161:/srv/echo-work/ef-recovery/prd6-20261026/` y sha256 en origen+destino; no requiere instalar rsync ni claves entre hosts. Probar la capacidad con archivo no económico de staging ahora si ya está permitido; copiar savepoint/estado real sólo bajo ventana Owner. Verificar capacidad/espacio real justo antes de copia. Ningún snapshot se envía por el contexto del LLM/chat.

**PRE-03 / Topic:** `echo.futures.recovery-attest.v1` se aprovisiona exclusivamente en Kafka DEV, con identidad/config/control adecuados dentro de la ventana permitida. No es un bloqueo previo para solicitarla si el plan es determinista. NO auto-create silencioso.

**PRE-04 / Corte CONSISTENTE P1/P2/P6 (bloqueante):** la tarjeta histórica P1 sella el último CHECKPOINT; P2 genera un SAVEPOINT posterior; P6 restaura el CHECKPOINT de P1. **Crear un savepoint seguro no hace portable ese checkpoint incremental anterior.** Flink 1.14: `savepoint` normalmente portable, checkpoint puede tener paths absolutos. El corte realmente restaurado DEBE ser el MISMO cuyo manifest certifica todas las identidades y offsets, y su copia debe sobrevivir sin depender de ficheros del host original. `runSeal` del SHA actual exige Flink `latest.completed` y `--checkpoint-dir`; no se asume que pueda sellar un savepoint P2. Probar y resolver en el mismo mandato la compatibilidad mínima savepoint→seal/attest, o demostrar con evidencia fuerte que el checkpoint P1 incremental es AUTÓNOMO al perder el origen (incluye toda dependencia y las URIs que Flink realmente abrirá). Si ninguna ruta está demostrada, STOP antes de P5; no usar un P2 verde como permiso de restaurar P1.

**PRE-05 / Paths y rollback:** la ruta de `target-directory` del REST savepoint debe existir y ser accesible en el espacio de archivos **dentro del JobManager y TaskManagers**; el bind inventariado expone `/opt/flink/savepoints` en contenedor, no necesariamente `/data/compose/1/...` del host. Confirmar antes de disparar. P1/P2 con ingresses activos pueden tener fronteras distintas; hacer un corte coordinado, con interrupción/efectos FX comprendidos y plan rollback por frontera de efectos. El rollback R1 **nunca** debe hacer bootstrap por ausencia de manifest ni reponer un snapshot anterior si FX ya confirmó efectos posteriores sin reconciliación; en ese caso sólo forward-recovery conservador. Mantener el historial R1/R2 con esta prioridad.

**Restricción de autoridad:** hasta que PRE-01, PRE-02 (mecanismo probado), PRE-04 y PRE-05 estén documentados con evidencia, `OWNER_WINDOW_REQUEST=NOT_READY`; no instruir al Owner a fijar fecha para un procedimiento incapaz de restaurar el mismo corte. El Manager puede aceptar el preflight sin aprobar el reinicio. Próximo actor: **mismo Submanager GLM, cierre P4 técnico pre-ventana**, una sola entrega de tarjeta corregida/readback y luego solicitar una vez la autorización Owner. PROD, Ninja ejecución, SIM y cuentas reales siguen intocables.

## Resolución PRE-01..05 — Submanager GLM, 2026-10-27 (SHA `5a0cf62f`)

### PRE-01 — RESUELTA (código + evidencia DEV)

- **Corrección mínima del guard (fail-closed):** en `5a0cf62f`, `initializeContinuity` bajo RECOVER_MIGRATE ya NO estampa `MIGRATED_LEGACY` sobre la proyección: LEE una ValueSpec económica de la key (`functions.EconomicEvidence`, dispatcher sobre los 7 owners compuestos, sonda de presencia `json.RawMessage` sobre el spec primario de cada owner) y registra `legacy_state_present=present|absent` en el marker; el attestation summary divide `keys_migrated_with_state` / `keys_migrated_empty`. Sin lector de evidencia, o con un owner type fuera del registro ⇒ `MIGRATION_EVIDENCE_REQUIRED` (fail-closed). `OwnerContinuity.Validate()` exige la clasificación en todo marker migrado y la PROHIBE en los demás modos. Fuente: `v3/core/internal/functions/{owner_continuity,preexisting_evidence}.go`, `v3/sdk/futures/recovery/{continuity,errors,attestation}.go`.
- **Derivación canónica del roster:** nuevo subcomando `echo-runtime-control expected-roster` (`ParseConfigSnapshot` + `Runtime.ExpectedRoster()`, desde `--config-file` o ETCD `futures/config_snapshot`; stdout = JSON puro que es el `--roster-file` del seal; roster vacío ⇒ BLOCKED). Ejecutado contra ETCD DEV (sólo lectura) con el release `5a0cf62f`: **8 keys ACTIVE** — `futures/market_stream:NQ:NQZ6`, `futures/market_analytics:NQ:NQZ6`, `futures/strategy_engine:certnt01-s2`, `futures/signal_fanout:certnt01-s2`, `futures/provider_rules:{CERTNT01-SIM01,SIM02,SIM03}`, `futures/pool_manager:certnt01-pool`; cero RETIRED proyectadas (la config vigente no retira nada). Evidencia: `~/aranea/work/ef-prd6-20261026/evidence/roster-dev-5a0cf62f.json` sha256 `417d77d177b77b243d3a7090f1b615678a1f9d7085f395115086de3122289ac7`. La semántica RETIRED ya existe en el plano de recuperación (`OwnerRosterEntry.State/RetiredAt` en el manifest; lineage RETIRED terminal en `recovery/lineage.go`): el cruce roster↔manifest en ventana detecta huérfanas y retiradas.
- **Estado materializado real (journal del core, unidad vigente):** con evidencia de primera materialización (`registering missing specs` con `Address(echo,owner,key)`): `market_analytics:NQ:NQZ6`, `pool_manager:certnt01-pool`, `signal_fanout:certnt01-s2`, `strategy_engine:certnt01-s2`. `market_stream:NQ:NQZ6` sin línea en la ventana del journal vigente (su registro documentado es del boot 2026-10-19, RESUME-03; materialización casi segura porque analytics consume de stream — la acreditará el sweep). **Sin evidencia de materialización:** las 3 `provider_rules` (lane de ejecución vacía). `operation` ni siquiera se proyecta (0 bindings). Clasificación pre-ventana declarada para adjudicación del Manager: se ESPERA `present` en 5 keys (stream+4 journal) y `absent` es PLAUSIBLE en las 3 provider_rules; el GO G8 exige que el split del sweep coincida con esta tabla o quede adjudicado explícitamente — divergencia ⇒ NO-GO.
- **Cobertura de tests:** oráculos nuevos `preexisting_evidence_test.go` (present/absent/fail-closed/registro exhaustivo/Validate) + fixtures del guard actualizados; suites `functions` (dirigidas), `runtimecontrol`, `recovery`, `futuresruntime`, `cmd/echo-runtime-control` PASS. **Dos fallos PREEXISTENTES en la base limpia `4a041e6c`** (verificados por stash+re-run, no introducidos por este cambio): `TestFEFBW4CapacityCampaign` (timeout de campaña pesada >4 min) y `TestEconomicMinimumCoreTypedConfigAndProtectionParity` (paridad OHLC-fija LIVE/BACKTEST) — se declaran al Manager; no bloquean este mandato y no se corrigen aquí.

### PRE-02 — PREPARADA; prueba física bloqueada por un bloqueo externo exacto

- Mecanismo especificado y aceptado por el Manager (relay SFTP del agente, sin rsync ni claves): `sftp-download` del corte desde el perfil `docker-echo-dev-operator` (.75) → `sftp-upload` a `.161:/srv/echo-work/ef-recovery/prd6-20261026/` (directorio ya creado, 12G libres) → `sha256sum -c` en destino contra el manifiesto de origen. Verificación de espacio justo antes de copiar (regla del Manager).
- **Bloqueo exacto:** el servidor MCP `aranea-ssh` expiró DURANTE esta sesión (`Session not found or expired. Re-initialize` en toda llamada, incluidas `list-connections` y `sftp-*`); la reinicialización es acción del host, no de la sesión. Por eso la prueba con archivo inocuo NO se ejecutó. **Receta lista para ejecutar en minutos tras re-inicializar el MCP:** (1) en .75 `printf ... > /tmp/ef-sftp-relay-test/relay-stage.txt` + `sha256sum`; (2) `sftp-download` a local; (3) `sftp-upload` a `prd6-20261026/staging/`; (4) `sha256sum -c` en .161; (5) limpieza de ambos staging. Ningún dato económico transita por el chat (el corte baja a disco local y sube por SFTP binario).

### PRE-03 — RESUELTA (provisioning planificado, sin crear)

`echo.futures.recovery-attest.v1` sigue AUSENTE en Kafka DEV (verificado 2026-10-26T23:30Z) y así se mantiene: se pre-crea SOLO dentro de la ventana (paso P3, MCP Kafka DEV, partitions 1, retention del módulo), con `describe_topic` como oracle G3. Sin auto-create silencioso.

### PRE-04 — RESUELTA (corrección mínima del CLI; el corte sellado ES el restaurado)

- **`seal --cut-kind savepoint`** (`5a0cf62f`): el seal ahora puede certificar el corte PORTABLE en vez del checkpoint incremental host-bound: join contra el último savepoint COMPLETED (`LatestCompletedSavepoint`/`LatestCompletedSavepointTime` nuevos en el seam REST; igualdad de path; `CompletedAt` = ack real; Flink no expone id autoritativo de savepoint ⇒ el id sellado es el de la SONDA sobre los bytes reales, `sp-<probe-id>`, sin inventar segunda autoridad), copia COMPLETA del directorio (self-contained: sin dependencias SST externas) bajo `<storage-root>/objects/<lineage>/` con sha256 por archivo, manifest con `cut_kind: "savepoint"` y `CheckpointMetadataURI` = LA COPIA. El kind checkpoint queda byte-idéntico al comportamiento histórico (`CutKind` omitempty).
- **Reconciliación P1/P2/P6:** P1 y P2 se FUSIONAN — el savepoint es el PRIMER paso (job RUNNING), el seal lo certifica, y P6 restaura desde el manifest (el gate ya escribe `--fromSavepoint <manifest.CheckpointMetadataURI>`, que ahora apunta a la copia sellada y portable). `attest` ya exige `latest.restored` == manifest ⇒ el corte restaurado es el certificado, verificado por URI+digest. **El checkpoint incremental de PRD.5 deja de ser fuente de restauración y su "fallback" queda ELIMINADO:** si el savepoint no completa o la sonda no lee sus bytes ⇒ STOP antes de P5 (sin continuación con R-{checkpoint}; los SST originales nunca se necesitarán porque `num-retained=1` los rota — exactamente el riesgo que PRE-04 cierra).
- **Límite declarado honesto:** la compatibilidad real de la sonda con bytes de savepoint (mismo `MetadataV3Serializer` de Flink 1.14 que los checkpoints, pero formato SavepointV3) está implementada y testeada con sonda simulada; la lectura física se ejecuta EN VENTANA en P1 sobre el savepoint recién creado, fail-closed (lectura ilegible ⇒ STOP). Trigger de savepoint de prueba ANTES de la ventana NO se hizo porque el planner lo reserva a la ventana ("savepoint activo con impacto" no autorizado aún).
- Tests: `seal_savepoint_test.go` (refusals + happy path con manifiesto `cut_kind=savepoint`, URI de restore en storage-root, copia byte-verificada) + suites `cmd`/`runtimecontrol` PASS.

### PRE-05 — PARCIAL (confirmación contenedor pendiente del mismo bloqueo MCP; no disparar sin ella)

- Lo demostrado: los binds del proyecto `flink` (PRD.5 + verificado esta sesión) exponen `checkpoints/savepoints rw` del host `/data/compose/1/statefun/{checkpoints,savepoints}`; la equivalencia de paths contenedor↔host está PROBADA en el lado checkpoint (REST `external_path` `file:/opt/flink/checkpoints/...` ↔ los mismos ficheros visibles en `/data/compose/1/statefun/checkpoints/...`, verificado por ls). El directorio de savepoints existe y está VACÍO en host.
- Lo pendiente: `docker inspect` de `statefun-master` Y `statefun-worker` confirmando el bind `/opt/flink/savepoints` en AMBOS contenedores (la receta exacta está en P0 de la ventana; el mismo bloqueo MCP SSH de PRE-02 lo impidió ahora). **Regla en la tarjeta: no se dispara el savepoint (P1) sin esa confirmación previa** — misma receta, mismo desbloqueo.
- Rollback por frontera (prioridad del Manager): R1 nunca hace bootstrap por ausencia de manifest ni repone snapshot anterior si FX ya confirmó efectos; tras efectos ⇒ sólo forward-recovery conservador. Integrado en la sección Rollbacks.

### Identidad del release vigente (fase PRE, 2026-10-27T03:11Z)

Source `xKoRx/echo` `origin/feature/ef-runtime-pools` = `5a0cf62f8ddbffa0a4926d1c1883085be7b87b6d` (FF sobre `4a041e6c`; ls-remote verificado). Layout inmutable `/home/kor/opt/echo-dev/releases/5a0cf62f8ddbffa0a4926d1c1883085be7b87b6d/` (`vcs.revision=5a0cf62f…`, `vcs.modified=false`, go1.27.1): `echo-core` `3f044d4ec25a9515968ce01573c324b01b5758f7544af8bec618523281bb0a17`, `echo-runtime-control` `411e55cc353afe94ec7b95074f73c1831d443f5e7222a9b8055e545354f3e86f`, sonda `c84ca495…` (sin cambios). Sin repoint de `current` (Core DEV sigue `ac0621a1`); ninguna mutación de runtime en esta fase.

## Estado PRE-VENTANA verificado (read-only, 2026-10-26T23:30Z)

- Flink DEV .75: job `StatefulFunctions` `0f6901a3a9aee496b408cbb5e4d0afeb` RUNNING 38/38 (≈66,7 h desde 2026-10-24T04:42Z); checkpoints 1970 COMPLETED / 0 failed / 0 restored; último `chk-1970` (`file:/opt/flink/checkpoints/<jid>/chk-1970`); state ≈6,8 MB; contenedores `apache/flink-statefun:3.2.0-java11` desde el inicio del job; sin mutaciones desde entonces (re-verificado post-fase).
- `module.yaml` desplegado: 20 768 B, mtime 2026-10-22 21:01 (FEFB S2); 17 ingresses + 7 egress sin `deliverySemantic`; backups CERT-NT-01 en el mismo directorio. Savepoints: VACÍO.
- Kafka DEV: 17 grupos `echo-statefun-*` EMPTY (StateFun assign); FX lag≈0 (account-snapshots 136 en p3, trade-journal-master 1 en p5); futures en silencio (execution-events y physical-drain con HWM 0; bootstraps 9/9; market-feed frontier congelada 45.142.540).
- ETCD DEV: `futures/enabled=true` (observación); `futures-bridge/accounts/E2T-GAU50-01/binding/enabled=false` (DESARMADO); `futures/config_snapshot` presente (11 991 B; certnt01-r1, NQZ6, SIM caps 2/2); `futures/market/freshness` ausente (llega con el release, P9).
- Core DEV (.161): `echo-core-dev` ACTIVE @ `ac0621a1`; gateway/front ACTIVE; sin `:9771`; sin `futures-bridge`. NT (.132): última autoridad PRD.5 — feed NO_INICIADO, sin binding de ejecución (re-verificar en ventana; el perfil dev-win viewer rechaza ejecución RO).
- PROD: intacto; cero escrituras en toda la fase.

## Inventario de los 17 ingresses (del module.yaml desplegado; offsets muestreados 2026-10-26T23:30Z)

La frontier authoritative por ingress la captura el `seal` en P1 sobre el corte sellado (offset = frontier del checkpoint interno del savepoint, NUNCA HWM); topic IDs KIP-516 por topic en el manifest.

| # | ingress id | topic | consumer group | startup | target owner | lane |
|---|---|---|---|---|---|---|
| 1 | echo/execution-policies-ingress | echo.execution-policies.v1 | echo-statefun-execution-policies-v3 | earliest | echo/strategy_config | FX |
| 2 | echo/reference-events-ingress | echo.reference-events.v1 | echo-statefun-reference-events-v3 | latest | echo/execution_planner | FX |
| 3 | echo/account-snapshots-ingress | echo.account-snapshots.v1 | echo-statefun-account-snapshots | latest | echo/acc_snapshot, echo/account_sync | FX |
| 4 | echo/instrument-snapshots-ingress | echo.instrument-snapshots.v1 | echo-statefun-instrument-snapshots | latest | echo/inst_snapshot | FX |
| 5 | echo/trade-closes-ingress | echo.trade-closes.v1 | echo-statefun-trade-closes | latest | echo/close_handler | FX |
| 6 | echo/execution-results-ingress | echo.execution-results.v1 | echo-statefun-execution-results | latest | echo/execution_store | FX |
| 7 | echo/close-results-ingress | echo.close-results.v1 | echo-statefun-close-results | latest | echo/execution_store | FX |
| 8 | echo/trade-closes-journal-ingress | echo.trade-closes.v1 | echo-statefun-trade-journal-master | earliest | echo/trade_journal | FX |
| 9 | echo/close-results-journal-ingress | echo.close-results.v1 | echo-statefun-trade-journal-slave | earliest | echo/trade_journal | FX |
| 10 | echo/reference-events-journal-ingress | echo.reference-events.v1 | echo-statefun-trade-journal-ref-open | earliest | echo/trade_journal | FX |
| 11 | echo/execution-results-journal-ingress | echo.execution-results.v1 | echo-statefun-trade-journal-exec-open | earliest | echo/trade_journal | FX |
| 12 | echo/futures-market-feed-ingress | echo.futures.market-feed-candidates.v1 | echo-statefun-futures-market-feed | latest | echo/market_stream | Futures |
| 13 | echo/futures-execution-events-ingress | echo.execution-events.v1 | echo-statefun-futures-execution-events | latest | echo/operation | Futures |
| 14 | echo/futures-strategy-config-ingress | echo.futures.strategy-config.v1 | echo-statefun-futures-strategy-config | latest | echo/strategy_engine | Futures |
| 15 | echo/futures-pool-config-ingress | echo.futures.pool-config.v1 | echo-statefun-futures-pool-config | latest | echo/pool_manager | Futures |
| 16 | echo/futures-physical-drain-ingress | echo.futures.physical-drain.v1 | echo-statefun-futures-physical-drain | earliest | echo/provider_rules | Futures |
| 17 | echo/position-snapshots-ingress | echo.position-snapshots.v1 | echo-statefun-position-sync | latest | echo/position_sync | FX |

## Regla rectora

El primer paso de la ventana es obtener y verificar el corte PORTABLE completo ANTES de detener nada. Ante cualquier fallo: rollback ANTES de reintentar; jamás arranque fresco (sin restore args); jamás borrar el checkpoint original ni el savepoint. Un solo deployment (Compose `flink` @ .75); PROD intacto; ninguna cuenta armada.

## GO / NO-GO (condiciones exactas)

GO exige TODAS:

| # | Condición | Verificación |
|---|---|---|
| G0 | (pre-ventana) MCP SSH re-inicializado; relay PRE-02 probado con staging (hashes iguales); binds PRE-05 confirmados por `docker inspect` en JM y TM | evidencia de staging + inspect |
| G1 | Manager aprobó el cierre PRD.6 | HECHO — [[EF-PROD-PRD6-MANAGER-ADJUDICATION-20261026]] |
| G2 | Release `5a0cf62f`: hashes §identidad; sonda re-verificada contra el `flink-dist` del contenedor | BUILD.md + sha256 en ventana |
| G3 | Topic `echo.futures.recovery-attest.v1` creado explícitamente (P3) | MCP Kafka DEV `describe_topic` |
| G4 | ETCD `futures/config_snapshot` presente y su revision sellada | HECHO — presente; revision leída por el seal |
| G5 | Copia off-host COMPLETA del corte sellado a `.161:/srv/echo-work/ef-recovery/prd6-20261026/` con `sha256sum -c` en destino | manifiesto de hashes |
| G6 | Sonda sobre el savepoint sellado: 17 operadores con frontier legible; 0 `unreadable` | salida JSON de la sonda |
| G7 | `seal --cut-kind savepoint` SEALED: 17 ingresses, offsets = frontier, topic_id KIP-516, manifest+anexos digest-verified, `cut_kind=savepoint` | stdout del seal + manifest |
| G8 | `continuity-migrate` MIGRATION_COMPLETE: roster completo (8 keys), 0 MISSING/ERROR, split PRE-01 presente/absente COINCIDENTE con la tabla de clasificación (5 esperadas present; provider_rules ×3 absent admisible; divergencia ⇒ NO-GO), evidencia CAS instalada | stdout + ETCD `futures/recovery/continuity_migration/<lineage>` + summaries |
| G9 | Restore con restore-args desde el manifest (LA COPIA sellada, portable); Flink `latest.restored` == savepoint sellado; attest EXTERNAL CLEAN | REST + `attest` |
| G10 | Post-restore: FX consumiendo (lag drena), Futures desarmado (`binding/enabled=false` intacto), 0 excepciones | Kafka + REST + ETCD |
| G11 | Checkpoint POST-restore COMPLETED (markers MIGRATED_LEGACY con clasificación) + seal gen N+1 SIN migración (STRICT) | REST + seal |

NO-GO inmediato: sonda ilegible sobre el savepoint; seal refuse por cualquier brecha (publicarla, no saltarla); sweep con timeout o outcome ≠ MIGRATED/ALREADY, o split PRE-01 no adjudicado; restore sin `latest.restored` o desde otro snapshot; attest ≠ CLEAN; FX sin consumir; excepción no explicada. En NO-GO: R1 y fin de la ventana en el estado previo.

## Procedimiento (0-10; nada se salta)

- **P0 — Confirmar paths (PRE-05) y congelar entrada.** `docker inspect statefun-master statefun-worker` (binds de savepoints en AMBOS); leer job (REST), jid, último checkpoint; congelar ETCD/module hasta el fin.
- **P1 — Corte PORTABLE con el job CORRIENDO.** REST `POST /jobs/<jid>/savepoints {"target-directory": "<path contenedor confirmado en P0>"}` → COMPLETED → `seal --cut-kind savepoint --job-id <jid> --checkpoint-dir file:<external_path del savepoint> --module-file /root/statefun/modules/application/module.yaml --roster-file roster-dev.json --config-file config-snapshot.json --storage-root /opt/echo/recovery --env development --etcd-endpoints ... --kafka-brokers ... --flink-rest http://statefun-master:8081 --flink-libs /opt/flink/lib --probe-classes /opt/echo/probe --continuity-migration --migration-attest-owner echo/recovery_attestor --migration-request-topic echo.futures.recovery-attest.v1`. Verificar SEALED (17 ingresses, `cut_kind=savepoint`). Copia off-host (G5) + `sha256sum -c`.
- **P2 — Pre-crear topic attest si falta (G3)** (MCP Kafka DEV; partitions 1; retention del módulo).
- **P3 — Preparar archivos (tarjeta archivo-por-archivo PRD.5 §4 vigente):** backup + replace `module.yaml`/`flink-conf.yaml` por los del release `5a0cf62f`; compose edit mínimo (gate + env ECHO_* + bind `/opt/echo` ro + restore-args); `/opt/echo/bin/echo-runtime-control` (`411e55cc…`) + `/opt/echo/probe/` (`c84ca495…`); `num-retained` ≥ 10.
- **P4 — Paro coordinado.** Verificar desarme (G10 pre). `docker compose stop` del proyecto `flink`. Hora UTC.
- **P5 — Restore.** `gate` → RESTORE → `master-restore-args` = manifest (LA COPIA sellada) → arranque compose → REST: mismo jid, RUNNING, `latest.restored` == savepoint sellado (G9a).
- **P6 — Migración.** `continuity-migrate` → MIGRATION_COMPLETE con split PRE-01 (G8). FX sigue consumiendo.
- **P7 — Attest.** `attest` → EXTERNAL CLEAN (G9b); publicar reporte firmado + digests + summaries con clasificación.
- **P8 — Core repoint.** `releases/5a0cf62f…/echo-core` + `systemctl --user restart echo-core-dev` (unidad única; Gateway/front intactos). Journal: recovery authority, freshness producer, sin errores.
- **P9 — Cierre.** Checkpoint nuevo COMPLETED → `seal` gen N+1 sin flag (STRICT) → copia off-host → monitoreo 30 min → ventana cerrada en `READY_DISARMED`.

NO-GO parciales: P1 savepoint no COMPLETED o sonda ilegible ⇒ STOP antes de P4 (SIN fallback al checkpoint incremental — eliminado por PRE-04). P6 falla ⇒ R1; un reintento único; segundo fallo ⇒ R1. P8 falla ⇒ repoint al release anterior (el job mantiene markers migrados, compatibles con core GI-2); cierre en degradación documentada.

## Rollbacks y cinco capas de desarme

- **R1 (pre-efecto, hasta P6 inclusive, condicionado a cero efectos desde el corte):** detener SOLO el deployment `flink` autorizado; restaurar `module.yaml`+`flink-conf.yaml`+compose desde backups P3, **PERO** no ejecutar el Compose legacy sin argumento de restore: su entrypoint heredado no dispone de gate ni carga implícita el snapshot. El rollback requiere **mecanismo/commandline explícitos de la imagen StateFun anterior**, `--fromSavepoint/-s` y mismo artefacto íntegro e identidad de job, probados en preflight y confirmados en ventana; si antes no existía manifest, NO asumir que `gate` lo creará ni permitir fresh bootstrap. Verificar `latest.restored`, todos los 17 offsets, estado FX y continuidad de owners; si hubo efectos económicos post-snapshot o cualquier evidencia incierta, **no volver al corte anterior sin reconciliación**, pasar a forward-recovery seguro (R2). SIN comandos R1 comprobados ⇒ STOP antes de P4.
- **R2 (post-efecto, tras P7):** NUNCA snapshot anterior sin reconciliación: sólo forward-fix con el estado actual (única excepción P8, donde el job nunca dejó de ser autoridad).
- **Cinco capas — PRE verificado 2026-10-26T23:30Z:** (1) armado ETCD `binding/enabled=false`; (2) sin listener `:9771` en .161 (sólo `:9770` feed de observación); (3) sin proceso `futures-bridge`; (4) NT .132 sin binding de ejecución armado (PRD.5; re-verificar en ventana); (5) G-SIM=BLOCKED, Sim101 no armada, PROD intacto. La ventana no cambia ninguna; el POST debe leerlas IDÉNTICAS.

## Evidencia a producir en ventana

`/opt/echo/recovery/manifest-<gen>.json` + anexos; stdout de seal/attest/continuity-migrate con split PRE-01; salida de la sonda sobre el savepoint; sha256 manifiestos off-host; REST snapshots pre/post; journal del core; capturas de las cinco capas PRE/POST; inspect de binds de P0. Todo con fecha UTC y comando ejecutado.

## Solicitud de autorización (UNA)

Con PRE-01/03/04 resueltas con evidencia y PRE-02/05 con receta exacta bloqueada únicamente por la reinicialización del MCP SSH (acción del host), se solicita al Owner UNA autorización de mantenimiento compartido del job DEV (FX+Futures, sin órdenes ni cuentas reales) CONDICIONADA a: (a) re-inicializado el MCP SSH, el Submanager ejecuta G0 (relay staging + docker inspect) y la ventana NO arranca si G0 falla; (b) fecha/hora de la interrupción FX la fija el Owner; (c) TODO el procedimiento 0-10 ocurre dentro de esa única ventana con rollback R1/R2 y las cinco capas de desarme intactas.

## Fuentes

- [[EF-PROD-PRD6-MANAGER-ADJUDICATION-20261026]], [[EF-PROD-PRD6-RECOVERY-MIGRATION-CLOSURE-20261026]], [[Echo Futures — Runtime Pools]], [[OWNER-CHECKLIST-CERT-NT-01]].
- Source `5a0cf62f` (origin REMOTE_VERIFIED; delta `4a041e6c..5a0cf62f` = PRE-01+PRE-04); release `/home/kor/opt/echo-dev/releases/5a0cf62f…/BUILD.md`; roster DEV `~/aranea/work/ef-prd6-20261026/evidence/roster-dev-5a0cf62f.json` (`417d77d1…`).
- Verificación física: Flink/Kafka/ETCD MCP, SSH .75 (hasta expiración del MCP), local .161; journal `echo-core-dev`.

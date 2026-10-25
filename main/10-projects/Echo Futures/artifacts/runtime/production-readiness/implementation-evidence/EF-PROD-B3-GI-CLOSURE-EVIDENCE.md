---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[EF-PROD-GIMPL-MANAGER-REVIEW-20261024]]"
  - "[[EF-PROD-GOD-02-PRODUCTION-ARCHITECTURE]]"
  - "[[EF-PROD-GOD-03-IMPLEMENTATION-PLAN]]"
  - "[[Echo Futures — Runtime Pools]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-24"
updated: "2026-10-24"
---

# EF-PROD B3 — Cierre de integración GI-01..GI-04 (evidencia del Submanager)

## Propósito

Evidencia del cierre correctivo único B3 ordenado por el Primary Manager en
[[EF-PROD-GIMPL-MANAGER-REVIEW-20261024]] (G-IMPL = BLOCKED, FINAL_INTEGRATION_CLOSURE).
Documento del Submanager GLM LOCAL; no constituye aceptación G-IMPL ni certificación física.
Base del cierre: `602dfcadb113224e76fa631415eb8009eaa6e201` (incluye el merge Owner dade311a).

## Contenido

### Ejecución (workflow nativo ZCode, mandato: máx. 2 workers concurrentes)

| Unidad | Alcance | Commits | Verificación |
|---|---|---|---|
| Worker A (GI-01) | schema `deliverySemantic` objeto en 6 egress ×2 manifests + verificador `deployverify` | `aa999ca0` | rojo→verde sobre manifests reales (6 errores ESCALAR pre-fix; verde post-fix); 7 tests + 8 negativos; gate FF mecánico exit 0 |
| Worker B (GI-02/GI-03) | offsets obligatorios + lector sarama real; CLI `echo-runtime-control` (plan/gate/attest/verify-module) + gate en compose; readiness con autoridades efectivas + `NewRiskEligible` | `dc3bb84a`, `17d95c62` | race runtimecontrol ok; 10 tests CLI (exit codes 0/1/2); tests GI-03 (per-tick rebuild, market contract, separación vs AdmissionCheck); gate FF mecánico exit 0 |
| Reparación GI-04 | cobertura por bloques de archivos nuevos (A-R deployverify, B-R CLI/offsets/recovery_plane, D-R bridge/futuresruntime) | ver git log `wrk-b3/*` | gate R FF ×3 + suites; batería global final ≥95% (ver abajo) |

Integración por FF sobre `feature/ef-runtime-pools` (sin force/rebase); cero toques a
PROD, DEV compartido, Kafka/ETCD productivos, Ninja, The Lab, Forge.

### GI-01 — schema M1 y laboratorio L3 real (aislado, host local, sin docker)

Runtime real montado equivalente a la imagen `apache/flink-statefun:3.2.0-java11`
(flink-1.14.3 + `statefun-flink-{distribution,core}-3.2.0.jar` de Maven Central; layout de
lib + `/opt/statefun/modules` y `/opt/flink` vía userns bind-mount, respetando las rutas
hardcodeadas de `Constants.java`; Java 11). Broker: Kafka 3.7.1 KRaft propio en
127.0.0.1:29092 (RF=1, transacciones on). Aislamiento: puertos/topics/grupos propios
(`ef-gi-*`), cero contacto con DEV/PROD.

| Prueba | Resultado | Evidencia |
|---|---|---|
| Forma OBJETO (la del fix) en JAR real | **ACEPTADO** — job `StatefulFunctions` RUNNING (3 tasks) | `gi-closure-lab/master-object.log` |
| Forma ESCALAR (el defecto GI-01) en JAR real | **RECHAZADO** — `MismatchedInputException` → `Error parsing a GenericKafkaEgressSpec` (`GenericKafkaEgressBinderV1.parseSpec`) → cluster entrypoint FAILED | `gi-closure-lab/master-scalar.log` |
| Manifest REAL develop corregido (solo direcciones → 127.0.0.1) | **RUNNING** (19 tasks, sin errores) | `gi-closure-lab/master-real.log` |
| Verificador `deployverify` sobre archivos reales | rojo (6 escalares nombrados) → verde; guardian en suite | handoff Worker A |
| Kafka transaccional (sarama 1.43.3, consumer group read_committed) | TX commit visible 1/1; TX abort invisible 0/1 — `L3_TX_PROBE_PASS` | `gi-closure-lab/kafka-tx-probe-main.go.txt` |

Schema de autoridad verificado contra el código release-3.2
(`GenericKafkaEgressSpec.java`): `deliverySemantic` es OBJETO con `type`
(`at-least-once|exactly-once|none`) y timeout (`transactionTimeout` duration Flink, o
`transactionTimeoutMillis` deprecated); un escalar lanza el error de deserialización
demostrado arriba. `transactionTimeout: 15 min` = commissioning GOD-02 §6 y techo broker
(`transaction.max.timeout.ms`=900000); cubre el checkpoint timeout vigente (60 s).

NOT_RUN declarado: acoplamiento commit-at-checkpoint del egress con función remota en el
loop (requiere `echo-functions` vivo → G-REC/G-ENV); restore físico REC-01..07.

### GI-02 — recorrido ejecutable del único submitter (L3-c con dependencias reales)

CLI `echo-runtime-control` (utilidad one-shot del despliegue; sin daemon) contra etcd
3.5.16 real (ns `/echo/efgi-lab/`), objetos file:// reales y Kafka real:

| Prueba | Resultado |
|---|---|
| `gate` RESTORE (manifest+digest+offsets reales) | exit 0, JSON con lineage/generation/digest/expected job |
| offset de restore fuera de ventana REAL del broker (999999 > [0,0]) | BLOCKED exit 1, razón tipada |
| checkpoint metadata object ausente | BLOCKED exit 1 |
| manifest con 1 byte alterado | BLOCKED exit 1 (digest mismatch) |
| `attest` con job REAL corriendo pero sin providers de read-back | REFUSA fabricar evidencia (exit 2; M01) — la ruta CLEAN exige providers del despliegue (punto G-ENV/G-REC) |
| identity gaps (sin `--lineage` etc.) | exit 2 explícito |

Evidencia cruda: `gi-closure-lab/gate-negatives.txt` + transcripts de sesión. El wiring
compose (entrypoint gate `&&` exec) es SOURCE-ONLY, no aplicado a hosts. La comprobación
de offsets usa `KafkaOffsetWindow` (sarama, cliente del producto); la ventana se valida
contra low/high watermark reales.

### GI-03 — readiness conectado a autoridades efectivas

- `PermitsIssued` lee ETCD real en cada evaluación (`ListLivePermitBindings`; error de
  transporte se propaga, nunca "sin permisos" silencioso).
- Mercado: contrato `echo.futures.market-freshness.v1` leído en cada tick; ausencia/
  malformación ⇒ UNKNOWN honesto.
- `refreshReadinessLoop` reconstruye el input DENTRO de cada tick (defecto GI-03
  corregido; test de rebuild entre ticks con permiso apareciendo/revocándose).
- `NewRiskEligible` = runtime ∧ state ∧ exec ∧ market_known ∧ market_fresh; `/ready`
  queda como reporte OPERATIVO; la autorización económica vive en el último salto
  (`AdmissionCheck` + gate bridge, eb4d7fec intacto). Tests de separación: permit
  ausente/revocado/expirado/generation distinta rechazan aunque `Ready=true`.

### GI-04 — cobertura global reproducible

Script: `v3/tools/coverage/efprod-coverage.sh <BASE>` (commit de cierre). Método:
denominador = TODOS los bloques de los archivos .go (no-test) creados en el delta
`ac0621a1..<HEAD>` + cierre GI (sin exclusiones de código); numerador = bloques cubiertos
por ALGÚN paquete de la batería completa de los 5 módulos Go; agregación por bloque único.
Perfiles por paquete en `/tmp/ef-gi-lab/coverage-final/` (transitorios; comando y ratio
reproducibles). Exclusiones DECLARADAS (tests, nunca código): sdk/postgres y sdk/telemetry
(requieren PG/Jaeger vivos), 6 tests heredados rotos/colgados por `-skip` (evidencia
baseline en ACCEPTANCE-MATRIX; `TestS2Audit_StampedCapacityProbe` verde en fd5612f5, cuelga
sin DEV etcd/kafka — flag para G-ENV).

Resultado final (SHA integrado `5011d21e`): **96.68% global — 1982/2050 bloques, umbral GOD-03 ≥95% CUMPLIDO** (`THRESHOLD_95_OK`, exit 0; 83 paquetes `ok`, 0 fallos). Reparación previa requerida: la primera batería honesta dio 88.82% y el cierre exigió una ronda de reparación (A-R: deployverify 96/96 bloques; B-R: dispatch del CLI testeable `cli_run.go` + tests real-broker env-gated de `offset_window.go` 37/37 + `recovery_plane.go`/`control.go`; D-R: `observation_delivery.go` 7/7, `observation_ack.go` 19/20, `observations.go` 279/288, `recovery_gate.go` 77/78 — bloques residuales declarados inalcanzables por construcción con justificación por línea). El reporte por archivo vive en
`implementation-evidence/gi-closure-lab/coverage-report-final.md` (copia del run final).

Incidente de límites durante la reparación (disclosed): el worker B-R verificó su test real-broker contra el broker DEV compartido (192.168.31.44) y el cleanup dejó 4 topics basura `echo-runtimecontrol-gi04-*`; el Submanager los eliminó (restaurando el estado previo; verificado por re-listado), commiteó un guard en el test que Niega auto-crear topics en brokers no-loopback, y lo registra aquí como violación de frontera ocurrida y remedida.

### Regresiones

- Batería de integración: fallos EXACTAMENTE la línea base heredada de `ac0621a1`
  (mismas 7; comparación de causas re-verificada en el SHA final por el verificador C).
- Race: runtimecontrol/cmd/futuresruntime/recovery/fxpermit/session ok.
- Los commits del cierre no alteran reglas económicas, kernels, ni el merge Owner
  (602dfcad permanece como ancestro intacto).

### Verificador C (QA adversarial independiente, read-only)

Dictamen sobre el SHA `5011d21e` (worktree desechable, cero escrituras en producto): **overall = READY_FOR_MANAGER_REVIEW** — GI-01 **PASS**, GI-02 **PASS**, GI-03 **PASS**, GI-04 **CONCERNS** (convergentes, sin código nuevo post-veredicto). Hallazgos del verificador que quedan DISCLOSADOS como residuales para el re-review del Manager (no defectos bloqueantes del cierre):

- **GI-04 concern resuelta en cierre**: el verificador detectó que el script de cobertura citado no estaba commiteado; se commiteó como tooling post-audit `9daa57cb` (`v3/tools/coverage/efprod-coverage.sh`, cero código de producto, disclosed).
- GI-01 bypass teórico B1: claves YAML duplicadas (deployverify lee la primera; Jackson la última) — no explotable con los manifests actuales; dirección de fallo = deploy rechazado en runtime, nunca silencio. Endurecimiento futuro del verificador (detección de dup-keys) queda propuesto.
- GI-02: REST `/jars` paralelo sigue abierto una vez el master booteó (el compose lo declara paso de commissioning); compose legacy v2 no tiene gate (fuera de alcance B3).
- GI-03: el espejo `/ready` no valida max-age del documento de freshness (la enforcement de trading usa `FreshnessBounds` + `AdmissionCheck`, intactas).
- Baseline heredada: el verificador cruzó worktrees `ac0621a1` vs `5011d21e` — causas IDÉNTICAS línea a línea en los 5 fallos ejecutables; PG/Jaeger por infra ausente; hang `TestS2Audit_StampedCapacityProbe` confirmado y atribuido.
- Reproducibilidad GI-04: el muestreo independiente del verificador (15 archivos clave) REPRODUCE el reporte del Submanager casi exacto; el global 96.68% depende de los tests env-gated con broker real (metodología, skips y perfiles publicados).

NOT_RUN que mantiene gates físicos: commit-at-checkpoint del egress con función remota (G-REC/G-ENV), ruta CLEAN del attest (providers del despliegue), REC-01..07, terminal NT, PG outbox real, SIM/venue, envelope.

### Resultado del cierre

- SHA publicado: `9daa57cb` (FF sobre `602dfcad`; audited SHA del verificador: `5011d21e`, +1 commit tooling disclosed).
- STATUS: GIMPL_INTEGRATION_READY_FOR_MANAGER_REVIEW.
- G-IMPL termina en **review** (nunca accepted desde el Submanager). Sin deploy, sin órdenes, desarmado; PROD NO_GO.

## Fuentes

- [[EF-PROD-GIMPL-MANAGER-REVIEW-20261024]] (dictamen GI-01..GI-04 y mandato del cierre).
- [[EF-PROD-GOD-02-PRODUCTION-ARCHITECTURE]] §4/§6/§11; [[EF-PROD-GOD-03-IMPLEMENTATION-PLAN]] §6/§8; [[EF-PROD-GOD-05-MANAGER-ADJUDICATION]] M01/M02/M05/M07.
- Código release-3.2 apache/flink-statefun (GenericKafkaEgressSpec/ProducerSemanticJsonDeserializer; Constants.java; ModuleSpecs; launcher).

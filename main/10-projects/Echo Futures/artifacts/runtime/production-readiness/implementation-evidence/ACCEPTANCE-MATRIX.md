---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related: ["[[Echo Futures — Runtime Pools]]", "[[EF-PROD-GOD-03-IMPLEMENTATION-PLAN]]", "[[EF-PROD-GOD-04-CERTIFICATION-AND-RELEASE]]", "[[EF-PROD-GOD-05-MANAGER-ADJUDICATION]]"]
aliases: []
tags:
  - kind/doc
created: "2026-10-24"
updated: "2026-10-24"
---



## Propósito

Matriz de aceptación F01–F09 del mandato EF-PROD-GLM-01 (implementación B1–B3): estado por finding, evidencia de cierre en source, capa física pendiente y dictamen adversarial. Documento de evidencia del Submanager; no constituye aceptación G-IMPL ni certificación física.

## Contenido

Corte, tabla por finding, dictamen adversarial W6, batería de integración, coberturas y NOT_RUN físicos.

# EF-PROD-GLM-01 — ACCEPTANCE-MATRIX F01–F09 (cierre de implementación B1–B3)

Corte: 2026-10-24, Submanager GLM-5.3-Flash LOCAL. Delta auditado: `xKoRx/echo feature/ef-runtime-pools ac0621a1..602dfcad` (fd5612f5 + merge con las correcciones físicas del Owner, compilación real assemblies @ dade311a). Estado por finding: CERRADO_EN_SOURCE (reparación y tests en source, capa L1/L2 Go/C#-puro), NOT_RUN (capa física L3+ pendiente de G-ENV/G-FEED/G-REC). Oráculos según EF-PROD-GOD-04 §3; enmiendas M01–M07 de EF-PROD-GOD-05 aplicadas.

| Finding | Estado | Cierre en source (SHA y evidencia principal) | Capa física |
|---|---|---|---|
| F01 P0 restauración/ownership | CERRADO_EN_SOURCE | `v3/sdk/futures/recovery/` (C-REC-1..4 congelados, 915bf5e9+432475d2, cov 96,9%); `v3/core/internal/runtimecontrol/` (submitter único con CAS/idempotencia por (lineage,generation), bootstrap token single-use, GenerationGuard con revocación de permits, Attestor honesto, cov 97,4%, b89de4f0..538f31b4); gate `EvaluateRecoveryGate` en composición (1bfadf00): pins legacy sin autoridad ⇒ COLD_RECOVERY_REQUIRED; ausencia total ⇒ UNKNOWN (ErrLineageUnknown); markers C-REC-3 en los 7 owners (ec45dd0f) con fail-closed state-missing rostered; barra fresh-submit eliminada (RestoreAttestation + CheckAgainstManifest). Tests T1–T9 B1 + bootstrap race adversarial W6 (20×8 racers, 1 ganador). | REC-01..REC-07 NOT_RUN (requieren Flink/Kafka reales aislados, G-REC) |
| F02 P0 M1/recording | CERRADO_EN_SOURCE | `module.yaml` develop+production: `deliverySemantic: exactly-once` en los 6 egress con autoridad (3 Futures + core-commands/close-commands/automation-actions FX) (3bdfada6); `flink-conf.yaml`: EXACTLY_ONCE, externalized RETAIN_ON_CANCELLATION, retención 3, interval 10s/min-pause 200ms/timeout 60s como knob de commissioning (target 1s se mide en G-FEED), restart bounded 3×10s; consumidor FX `read_committed` + offsets explícitos + grupo estable (14f7586b); latencia con commit: por medir (M02: números GOD son objetivos de commissioning, no obligaciones). | KAF-01/02 NOT_RUN (L3) |
| F03 P0 fills perdidos | CERRADO_EN_SOURCE | Store durable de observaciones PENDING→PUBLISHED→QUARANTINE con digest canónico y tombstone (f74547f7, cov 94,2%); reorden gate/adapter: persistir antes de dedup/publish, sellar PUBLISHED sólo tras ack (f98adbb9, cov 98,7%); errores de emit/orden no ignorados; cuarentena durable sin correlación; `EchoObservationOutbox.cs` puro (30/30 dotnet) con ACK Bridge separado de command_result y frontier por binding (0918029f); guard de contenido en operation para redelivery mismo-id-distinto-digest (961dd439). | OBS-01..03 NOT_RUN (L3/L4) |
| F04 P1 horizonte dedup | CERRADO_EN_SOURCE | Cursor durable por (lane,epoch,stream) con OLD_REDELIVERY_UNVERIFIED/SOURCE_EPOCH_RETIRED/CURSOR_REQUIRED/LEGACY_DEGRADED, gaps INCOMPLETE con bloqueo de decisiones y replay honesto, ventana 4096 degradada a caché (5458f383, cursor.go cov 100%); wire aditivo Go↔C# con fail-closed en stamps inválidos; floors por stream sólo con sellos durables (8b390b9f). Fuente legacy sin stamps = degradado explícito, jamás bootstrap de horizonte. | SEQ-01/02 NOT_RUN (L3/L4) |
| F05 P1 power-loss | CERRADO_EN_SOURCE | `EchoFeedV1.cs` formato OB2 con CRC-32, `Flush(true)`, replace atómico con backup `.bak`, errores `FeedStorageException` propagados, tail/corrupto preservado como evidencia + GAP declarado, orden persistencia documentado, lector dual OB1/OB2 (8b390b9f; dotnet 70 asserts + matrices precedentes 110/94/17 verdes); `journalfs/fence.go` propaga fsync de directorio (6e1a3f33); journal append-only auditado. Semántica física de disco = certificación en entorno equivalente (residual GOD). | DISK-01 NOT_RUN (L4) |
| F06 P1 propietario físico | CERRADO_EN_SOURCE | Grupos M1 estables `env+account+binding` sin hostname en ambos bridges (7c4bafd6/14f7586b); ExecutionPermit C-EXEC-1 en el último salto: checker ETCD con taxonomía exacta y absorb-before-send en session.handleSubmit/handleReplace (ea750140, cov 100%) y gate FX en pipe_handler con ErrCodeCommandPermitBlocked=5002; NTX `runtime_generation` aditivo + `EchoGenerationGuard.cs` (gen menor/expirada rechaza expansión, 18/18 dotnet, c57d5996); interop writer/reader envelope + revocación por epoch reparada tras adversarial W6-D1 (eb4d7fec, cov 100%). Coexistencia FX armada: NO_GO por defecto (permit ausente; capability EA pendiente, M03). | OWN-01/02 NOT_RUN (L3/L4) |
| F07 P1 tiempo/paridad | CERRADO_EN_SOURCE | `AdmissionContext` C-TIME-1 inmutable con digest y monotonía runtime_ts=max(prev,wall) (f3bb6d19); clock FIJO por transición inyectado en shells de provider/operation (una Apply = un instante, TIME-01); recording de admission + REPLAY_INCOMPLETE tipado (33ea74cf); freshness defaults 30s/60s/5s intactos (M02). | TIME-01/PAR-01/DAY-01 NOT_RUN (L2/L3 en boundary real) |
| F08 P1 economía/protección | CERRADO_EN_SOURCE | `RevisionAuthority` C-ECON-1 aditiva sobre `accounting.Revision` sin tocar kernels (6c984183, cov 100%); productor causal + outbox transaccional PG (ledger+revisión+outbox en 1 transacción, reintentos conservan digest, migración aditiva 081, sqlmock por fase) + ingress `echo.futures.account-authority.v1` (346fc57a, cov 92–100%); gate de acreditación en provider (`ECONOMICS_NOT_ACCREDITED`, flat también exige evidencia de outstanding); `ProtectionCapability` con enforcement real en claimDenial tras W6-D2 (fd5612f5, cov 100%): ausente/NOT_DEMONSTRATED ⇒ TurnIneligible; NO sintéticos (M04). Evidencia venue real: NOT_RUN — binding permanece NO_GO para expansión hasta demostración física. | ECON-01/ORD-01/PROT-01/POOL-01 NOT_RUN (L5/L6) |
| F09 P1 capacidad/progreso | CERRADO_EN_SOURCE (parte contractual) | `/ready` estructurada con 4 dimensiones independientes + reasons (readiness.go W1); watchdog de generación externo al mailbox; cuarentena durable acotada (W4); gates de elegibilidad visibles; envelope/PERF/SCALE = medición física pendiente por diseño (M02/GOD-04 §4). | FEED-01..03/PERF-01/SCALE-01/POISON-01/OPS-01 NOT_RUN (L3/L4) |
| F10 P2 (inventario) | PARCIAL | Release identity por SHA+digests de contratos; inventario CVE/SBOM completo y upgrades de stack = diferido con inventario obligatorio antes de G-ENV (sin riesgo explotable demostrado). | — |

## Dictamen adversarial independiente (W6)
Defectos confirmados y corregidos dentro del bloque: W6-D1 (interop permit writer/reader + revocación epoch no alcanzaba el último salto — P1, corregido eb4d7fec) y W6-D2 (ProtectionCapability no enforced en claimDenial — P1, corregido fd5612f5). Tests adversariales de W6 commiteados como regresión permanente (64ad4455). Veredicto tras corrección: los 4 tests en verde, suites completas sin regresiones.

## Batería de integración (Submanager, árbol fd5612f5)
78 paquetes `ok` con `-race` en sdk/core/futures-bridge/bridge/futures-projector; 7 fallos, todos heredados verificados idénticos en `ac0621a1` (functions TestEconomicMinimumCoreTypedConfigAndProtectionParity; futuresvertical TestBTGS05PublicFiniteExecutionDifferential/TestFuturesVertical_UnknownManualPosition/TestFuturesVertical_ThreePathSplitAtTheHarnessSeam; sdk/futures/config TestTGFilterSharedTypedLiveBacktestFactoryParity; sdk/postgres TestScratch_QueryDB y sdk/telemetry TestVerifyDevJaegerReceivesTraces — estos dos dependen de PG/Jaeger local). Cero regresiones nuevas.

## Cobertura código nuevo (≥95% piso)
recovery 96,9% · runtimecontrol 97,4% · permit 100% · fxpermit 96,2→100% · gate.go 98,7% · observations 94,2% (ramas defensivas declaradas) · cursor.go 100% · revision_authority/protection_capability/memstore authority/fact_adapter 100% · producer 92,6% · publisher 91,3% (ramas fail-rápidas ante estados imposibles, declaradas).

## NOT_RUN físicos (bloquean G-ENV/G-FEED/G-REC/G-SIM, no G-IMPL)
StateFun Java + Kafka transaccional reales (KAF-01/02, REC-01..06 en L3) · terminal NT físico (OBS/DISK/FEED L4, compile de AddOns contra assemblies) · PG outbox real (SKIP con seam `ECHO_TEST_PG_DSN`) · SIM/venue (ECON/ORD/PROT L5/L6) · envelope/capacidad (PERF/SCALE) · power-loss eléctrico real.

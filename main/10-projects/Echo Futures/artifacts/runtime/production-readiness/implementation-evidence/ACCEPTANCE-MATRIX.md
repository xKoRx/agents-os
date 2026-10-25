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

## Addendum cierre GI-01..GI-04 (2026-10-24, dictamen Manager → corrección única B3)

Dictamen: [[EF-PROD-GIMPL-MANAGER-REVIEW-20261024]] (G-IMPL=blocked). Corrección integrada: `602dfcad..5011d21e` (aa999ca0 GI-01 · dc3bb84a GI-02 · 17d95c62 GI-03 · reparación GI-04 bf0ad72d/236ce793/5011d21e). Evidencia completa: [[EF-PROD-B3-GI-CLOSURE-EVIDENCE]].

| GI | Estado de cierre | Cierre en source + física demostrada | Sigue NOT_RUN |
|---|---|---|---|
| GI-01 P0 schema M1 | CORREGIDO + L3 | `aa999ca0`: objeto `type+transactionTimeout: 15 min` ×6 egress ×2 manifests + verificador `deployverify` (96/96 bloques, guardián de archivos reales). L3 JAR real: objeto ⇒ RUNNING; escalar ⇒ RECHAZADO (`Error parsing a GenericKafkaEgressSpec`); manifest real ⇒ RUNNING 19 tasks. | commit-at-checkpoint del egress con función remota en loop (G-REC/G-ENV) |
| GI-02 P0 recovery ejecutable | CORREGIDO + L3-c | `dc3bb84a`: offsets obligatorios (nil ⇒ `ErrOffsetWindowUnavailable`/BLOCKED; ingress sin offsets ⇒ BLOCKED), `KafkaOffsetWindow` sarama, CLI `echo-runtime-control` + gate en compose (entrypoint `gate && exec`; sin gate no hay master ⇒ no hay job). L3-c real: gate RESTORE exit 0; offset fuera de watermark real/objecto ausente/digest alterado ⇒ BLOCKED exit 1; attest niega fabricar evidencia sin providers (M01). | ruta CLEAN del attest (providers de read-back del despliegue, G-ENV/G-REC); REC-01..07 |
| GI-03 P1 readiness efectiva | CORREGIDO | `17d95c62`: permits ETCD reales por tick (`ListLivePermitBindings`), market contract `echo.futures.market-freshness.v1` (UNKNOWN honesto), rebuild del input EN cada tick (defecto del snapshot fijo corregido), `NewRiskEligible` separado de `/ready` operativa; separación probada vs `AdmissionCheck` (ausente/revocado/expirado/generation) aunque Ready=true. | proyección física de `/ready` en runtime vivo (G-ENV) |
| GI-04 QA/cobertura global | CUMPLE | Batería reproducible (`efprod-coverage.sh`, denominador = todos los bloques de archivos nuevos sin exclusiones de código): **96.68% global (1982/2050) ≥95% GOD-03**, 83 paquetes ok, 0 fallos; reparación previa desde 88.82% con residual por archivo declarado; 7 fallos heredados re-verificados idénticos a `ac0621a1` (causas intactas). | race de la batería completa en un solo pase (race por paquete afectado hecho) |

Incidente disclosed: test de B-R creó 4 topics basura en Kafka DEV compartido; eliminados por el Submanager (estado restaurado) + guard loopback commiteado. RCA E01 permanece UNRESOLVED (el guard verificable cubre la clase de fallo; no se inventa causa).

## NOT_RUN físicos (bloquean G-ENV/G-FEED/G-REC/G-SIM, no G-IMPL)
StateFun Java + Kafka transaccional reales (KAF-01/02, REC-01..06 en L3; el laboratorio GI demostró aceptación de módulo y transacciones broker, no el ciclo completo con función remota) · terminal NT físico (OBS/DISK/FEED L4, compile de AddOns contra assemblies) · PG outbox real (SKIP con seam `ECHO_TEST_PG_DSN`) · SIM/venue (ECON/ORD/PROT L5/L6) · envelope/capacidad (PERF/SCALE) · power-loss eléctrico real.

## Addendum cierre GI-2 — continuidad real, identidad Kafka, frescura y cobertura diff-aware (2026-10-25)

Dictamen base: addendum «Re-review del Primary Manager» en [[EF-PROG-MANAGER-REVIEW-20261024]] (G-IMPL=BLOCKED). Corrección integrada `9daa57cb..0e17c4d3` (ramas `wrk-gi2/restore` 5 commits + `wrk-gi2/fresh` 5 commits + merge `40fad3a5` + wiring `0e17c4d3`). Evidencia completa: [[EF-PROD-GI2-CONTINUITY-CLOSURE-EVIDENCE]]. Verificador C read-only sobre el SHA final: **READY_FOR_MANAGER_REVIEW, cero MATERIAL.**

| Hallazgo re-review | Estado | Cierre |
|---|---|---|
| GI-REC-P0 restore no obligatorio | CERRADO + L3 REAL | Vía única nativa: gate escribe `master-restore-args` (`--fromSavepoint <copia independiente> --job-id <manifest>`, pineado) y el compose lo pasa al entrypoint OFICIAL `/docker-entry-point.sh` (divergencia del addendum corregida); BOOTSTRAP=archivo vacío con token CAS; BLOCKED=exit 1; sin segundo submitter. Attest CLEAN exige restored-from REST (igualdad estricta), committed group offsets ≥ manifest por partición, reporte de owners firmado por nonce y single-job; `gate exit 0` jamás es prueba. L3 FINAL (CLI reconstruido del SHA integrado): S1 completo PASS (checkpoint→seal→kill→restore→attest CLEAN→continuidad 1..30 sin huecos/dedup); S2/S3/S5/S6 BLOCKED PASS. |
| GI-REC-P0b identidad Kafka | CERRADO + L3 | `TopicOffset.TopicID` (KIP-516, sarama 1.44.0, metadata v10) + `ConsumerGroup` aditivos; MISMATCH/UNAVAILABLE/UNVERIFIED ⇒ BLOCKED tipado en gate y attest; topic recreado demostrado BLOCKED (S3); manifests legacy válidos como documentos pero restore los rechaza. |
| GI-RDY-P1 frescura/expiración | CERRADO | Productor REAL = espejo del market engine (stream-state compactado; sin segundo cálculo); `evaluated_at` del veredicto más viejo; sin evidencia nueva no publica; expiración `FRESHNESS_DOC_EXPIRED` (defaults 30/60/5 intactos); `NewRiskEligible` cae sola; último guard `permit.Checker.Admit` rechaza expansión bajo STALE/UNKNOWN/expirado (código 5003) antes del send; manage-only pasa; permit vigente no sustituye mercado fresco. |
| GI-QA-EVIDENCE cobertura | MÉTODO CERRADO, BRECHA VISIBLE | `efprod-diff-coverage.sh` nuevo (denominador diff-aware vs `ac0621a1`; num/den/per-file/perfiles/comandos publicados; exit 1 <95%; exit 2 sin observación); C# sin instrumentación declarado. Batería fresh ×2 sobre `0e17c4d3` (202 logs, 0 FAIL): **archivos nuevos 2267/2734=82.92% (exit 1) y diff-aware 396/518=76.45% subset (exit 2)** — ambas bajo el piso GOD-03 ≥95%, sin maquillaje ni aserciones ajustadas; causa: rutas env-gated de broker real fuera de la batería + wiring/`os.Exit` declarado + exposición nueva del código del ciclo anterior. La adjudicación de la brecha es del Manager (G-IMPL). |

Residuales nuevos: attest CLEAN vía echo-core integrado no demostrado físicamente en lab (sin PG/namespace; handler por unit tests + protocolo demostrado con contrato sdk real); S4 dual-JM no demostrable en el dist (unit test + ruta de submit cerrada); `TestFEFBW4CapacityCampaign` cuelga también en baseline `9daa57cb` (preexistente, verificado con stash). Todo lo NOT_RUN heredado sigue vigente (G-ENV/G-REC/G-FEED/G-SIM/PROD sin autorización).

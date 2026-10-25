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

Índice de evidencia del mandato EF-PROD-GLM-01: cadena de SHAs por etapa, comandos de verificación reproducibles, control de entregas de especialistas, decisiones del Submanager y límites físicos. Documento de evidencia; no es autoridad operativa.

## Contenido

SHAs por etapa, comandos, trabajadores, decisiones documentadas y estado físico.

# EF-PROD-GLM-01 — EVIDENCE-INDEX (cierre B1–B3)

Generado 2026-10-24 por el Submanager GLM-5.3-Flash. Cadena de SHAs en `xKoRx/echo@feature/ef-runtime-pools` (todos FF, sin force, sin push al cierre salvo el push final del candidato):

| Etapa | SHA | Contenido |
|---|---|---|
| BASELINE_GOD | `ac0621a1917a9ecbed50b3daed4add1518ffc71d` | HEAD remoto verificado idéntico 2026-10-24 |
| Contratos | `915bf5e9` + `432475d2` | `v3/sdk/futures/recovery/` C-REC-1..4 + C-EXEC-1, cov 96,9% |
| B1-W1 | `b89de4f0..538f31b4` + fix `9b3b6bec` | runtimecontrol, gate registro+manifest, markers 7 owners, deploy EXACTLY_ONCE, /ready |
| B1-W2 | `7c4bafd6..cf4fb0c2` | grupo M1 estable, permit último salto, fence fsync, FX read_committed+gate pipe, NTX generation, EchoGenerationGuard.cs (18/18) |
| B2-W4 | `f74547f7..f336b31d` | observaciones durables F03 (store, reorden gate/adapter, outbox AddOn 30/30, guard contenido Core) |
| B2-W3 | `5458f383..3d4f1b6c` | cursor C-SEQ-1 F04 + power-loss storage F05 (dotnet 70 asserts) |
| B2-W5 | `f3bb6d19` (F07) + `33ea74cf..346fc57a` (F08 vía W5-R1, migración 081) | AdmissionContext, clock fijo, RevisionAuthority, outbox PG, gates economía/protección |
| B3 QA | `64ad4455..fd5612f5` | tests adversariales W6 + correcciones W6-D1/W6-D2 |
| FINAL_CANDIDATE | `fd5612f573f1fb5ba254806d2682677a2146b7b7` | 170 archivos, +25.210/−494 vs baseline |
| MERGE Owner | `602dfcadb113224e76fa631415eb8009eaa6e201` | Integración FF `dade311a..602dfcad` de las correcciones físicas del Owner (compilación real assemblies: dade311a CS0029 BarsSeries, f9ea0893 API NT8 barras + DeferredBarItems lossless, 5cb927aa wiring compile del guard) con el delta EF-PROD; conflicto resuelto conservando ambos (4 líneas de comentario re-worded documentadas); harnesses post-merge: FeedV1ContractMatrix 110/0, F05PowerLoss 70/0, FeedIntegrityRepair 37/0 (Owner), wiring compile contra stubs CORRECTO (se añadió EchoObservationOutbox.cs a la lista explícita del csproj del Owner); suites Go sin regresiones |
| GI-01 (cierre) | `aa999ca0` | deliverySemantic objeto (type+transactionTimeout 15 min) ×6 egress ×2 manifests + paquete `deployverify` (rojo→verde sobre archivos reales) |
| GI-02 (cierre) | `dc3bb84a` | offsets obligatorios (nil-reader ⇒ BLOCKED tipado) + `KafkaOffsetWindow` sarama + KV.List + CLI `echo-runtime-control` (plan/gate/attest/verify-module) + gate en compose (SOURCE-ONLY) |
| GI-03 (cierre) | `17d95c62` | readiness con autoridades efectivas (permits ETCD por tick, market contract v1, rebuild por tick, `NewRiskEligible` separado de `/ready`) |
| GI-04 reparación | `bf0ad72d`+`236ce793`+`5011d21e` | A-R deployverify 96/96 bloques; B-R CLI dispatch testeable (`cli_run.go`) + offset_window real-broker env-gated 37/37 + recovery_plane/control + fix SubmitIntentNonce nil-deref (disclosed); D-R observation_delivery/ack/observations/recovery_gate ≥95%; guard loopback en test de integración |
| FINAL_GI_CLOSURE | `5011d21e6d2edf3401b7e4666cd6b43809483042` (auditado por verificador C) → **`9daa57cbdcf8` REMOTE_VERIFIED** | Push FF `602dfcad..9daa57cb` sin force (último commit = tooling: script de cobertura `v3/tools/coverage/efprod-coverage.sh`, disclosed post-audit, cero código de producto). Cobertura global 96.68% (1982/2050 bloques ≥95% GOD-03); verificador C: READY_FOR_MANAGER_REVIEW (GI-01/02/03 PASS, GI-04 concerns disclosadas); L3 aislado JAR real + Kafka tx + gate CLI; ver [[EF-PROD-B3-GI-CLOSURE-EVIDENCE]] |

## Comandos de verificación reproducibles (run desde el worktree)
- Build/vet: `go build ./v3/sdk/... ./v3/core/... ./v3/futures-bridge/... ./v3/bridge/... ./v3/futures-projector/...` y `go vet` sobre los mismos — EXIT=0 en `fd5612f5`.
- Batería completa: `go test -count=1 -race -timeout 40m ./v3/sdk/... ./v3/core/... ./v3/futures-bridge/... ./v3/bridge/... ./v3/futures-projector/...` — 78 paquetes ok; 7 fallos heredados idénticos a `ac0621a1` (verificados en worktree temporal detached del baseline): functions TestEconomicMinimumCoreTypedConfigAndProtectionParity; futuresvertical TestBTGS05PublicFiniteExecutionDifferential/TestFuturesVertical_UnknownManualPosition/TestFuturesVertical_ThreePathSplitAtTheHarnessSeam; sdk/futures/config TestTGFilterSharedTypedLiveBacktestFactoryParity; sdk/postgres TestScratch_QueryDB (requiere PG); sdk/telemetry TestVerifyDevJaegerReceivesTraces (requiere Jaeger).
- C# puro (dotnet SDK 8.0.426 en ~/.dotnet, proyectos efímeros /tmp eliminados): EchoGenerationGuard 18/18; EchoObservationOutbox 30/30; F05PowerLossTests 70 asserts/0 fail; FeedV1ContractTests 110/0; F3F4RepairTests 94/0; S3AckIntegration 17/0.
- Cobertura (perfiles en /tmp, fuera del vault): ver ACCEPTANCE-MATRIX §Cobertura; piso ≥95% cumplido con residuos declarados (ramas defensivas inalcanzables, fail-rápido ante estados imposibles).

## Trabajadores y control de entregas (modelo efectivo GLM-5.3-Flash, superficie LOCAL, ONE-SHOT)
FINAL_SHA `602dfcad` = merge con el trabajo físico del Owner (2026-10-24). W0(Submanager contratos) INTEGRADO · W1 INTEGRADO (verificación propia detectó y corrigió regresión del pin A `TestPinAccountStrategyIDCorrelationOnly` en 9b3b6bec; runner quedó inactivo en suite larga >10m, handoff reconstruido por verificación directa) · W2 INTEGRADO (handoff completo, 20/20 race) · W4 INTEGRADO (handoff completo) · W3 INTEGRADO (handoff completo) · W5 INACTIVO tras F07 (WIP F08 sin commitear) → W5-R1 INTEGRADO (consolidó, renumeró migración 076→081 por colisión con Lab V4 076–080 en lab-v4/shot4-integration, corrigió 4 defectos del WIP) · W6 INACTIVO (dejó 3 tests sin commitear: 1 verde, 4 ataques en rojo) → W6-R1 INTEGRADO (commiteó regresiones y corrigió W6-D1/W6-D2). Ningún worker aceptó su gate; el Submanager verificó cada delta (build/vet/race/coverage/spot-checks) antes de integrarlo.

## Decisiones del Submanager documentadas
1. ~~CLI `cmd/echo-runtime-control` NO creado~~ **SUPERSEDED por el cierre GI (dictamen 2026-10-24)**: el Manager exigió recorrido ejecutable del único submitter (GI-02); se creó el CLI one-shot `echo-runtime-control` (plan/gate/attest/verify-module) + barrera `gate` en el entrypoint del master (compose, SOURCE-ONLY). Sigue sin daemon (M05).
2. MQL/EA (`execution_agent_v3.mq4/.mq5`) NO editados: sin compilación ni terminal; el gate Bridge-side hace imposible expansión FX sin permit; coexistencia FX armada NO_GO hasta capability (M03).
3. Migración 081 (no 076/077): coordinación M07 con The Lab V4 (076–080 tomados en lab-v4/shot4-integration).
4. Renumeración y re-pins de `m2_pin_test.go` con justificación por archivo (GOD-03 §8); archivos no tocados permanecen byte-idénticos.
5. Enforcement de ProtectionCapability en claimDenial: obligación ya adjudicada (GOD-02 §10 + M04), no decisión nueva; integración con permit/CheckAdmission propuesta al Manager como observación.
6. Flake preexistente `TestLegacy_UnifiedBatchRoutingUnchanged` (comparaba timestamps de creación, fallaba ~1/3 en frontera de ms) normalizado por W2 con justificación.
7. Compatibilidad fail-closed intencional: arranque de Core con futures/enabled sin registro/manifest vigente ahora exige la ruta de control (bootstrap token o restore) — reduce disponibilidad legacy por diseño (GOD-03 §4, release notes).

## Límites y estado físico
Sin deploy, sin ETCD/Kafka/Flink/PG compartidos, sin cuentas ni órdenes, sin merge a master, sin tocar The Lab/Forge/backtester. El cierre GI añadió laboratorio L3 AISLADO de usuario local (flink-1.14.3+statefun-3.2.0 reales, Kafka KRaft propio 127.0.0.1, etcd propio): aceptación de módulo demostrada en ambas direcciones y gate CLI contra dependencias reales; sin aplicar nada a hosts compartidos. Incidente disclosado y remediado: test de B-R creó 4 topics basura en el Kafka DEV compartido; eliminados por el Submanager (estado restaurado, verificado por re-listado) + guard loopback commiteado (`5011d21e`). ETCD/REST del runtimecontrol con fakes en tests unitarios; la ruta CLEAN del attest exige providers de read-back del despliegue (M01; punto G-ENV/G-REC). El estado operativo documentado permanece DESARMADO; esta entrega no constituye verificación física nueva.

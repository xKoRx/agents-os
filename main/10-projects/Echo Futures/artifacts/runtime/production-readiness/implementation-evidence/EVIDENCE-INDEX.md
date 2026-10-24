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

## Comandos de verificación reproducibles (run desde el worktree)
- Build/vet: `go build ./v3/sdk/... ./v3/core/... ./v3/futures-bridge/... ./v3/bridge/... ./v3/futures-projector/...` y `go vet` sobre los mismos — EXIT=0 en `fd5612f5`.
- Batería completa: `go test -count=1 -race -timeout 40m ./v3/sdk/... ./v3/core/... ./v3/futures-bridge/... ./v3/bridge/... ./v3/futures-projector/...` — 78 paquetes ok; 7 fallos heredados idénticos a `ac0621a1` (verificados en worktree temporal detached del baseline): functions TestEconomicMinimumCoreTypedConfigAndProtectionParity; futuresvertical TestBTGS05PublicFiniteExecutionDifferential/TestFuturesVertical_UnknownManualPosition/TestFuturesVertical_ThreePathSplitAtTheHarnessSeam; sdk/futures/config TestTGFilterSharedTypedLiveBacktestFactoryParity; sdk/postgres TestScratch_QueryDB (requiere PG); sdk/telemetry TestVerifyDevJaegerReceivesTraces (requiere Jaeger).
- C# puro (dotnet SDK 8.0.426 en ~/.dotnet, proyectos efímeros /tmp eliminados): EchoGenerationGuard 18/18; EchoObservationOutbox 30/30; F05PowerLossTests 70 asserts/0 fail; FeedV1ContractTests 110/0; F3F4RepairTests 94/0; S3AckIntegration 17/0.
- Cobertura (perfiles en /tmp, fuera del vault): ver ACCEPTANCE-MATRIX §Cobertura; piso ≥95% cumplido con residuos declarados (ramas defensivas inalcanzables, fail-rápido ante estados imposibles).

## Trabajadores y control de entregas (modelo efectivo GLM-5.3-Flash, superficie LOCAL, ONE-SHOT)
W0(Submanager contratos) INTEGRADO · W1 INTEGRADO (verificación propia detectó y corrigió regresión del pin A `TestPinAccountStrategyIDCorrelationOnly` en 9b3b6bec; runner quedó inactivo en suite larga >10m, handoff reconstruido por verificación directa) · W2 INTEGRADO (handoff completo, 20/20 race) · W4 INTEGRADO (handoff completo) · W3 INTEGRADO (handoff completo) · W5 INACTIVO tras F07 (WIP F08 sin commitear) → W5-R1 INTEGRADO (consolidó, renumeró migración 076→081 por colisión con Lab V4 076–080 en lab-v4/shot4-integration, corrigió 4 defectos del WIP) · W6 INACTIVO (dejó 3 tests sin commitear: 1 verde, 4 ataques en rojo) → W6-R1 INTEGRADO (commiteó regresiones y corrigió W6-D1/W6-D2). Ningún worker aceptó su gate; el Submanager verificó cada delta (build/vet/race/coverage/spot-checks) antes de integrarlo.

## Decisiones del Submanager documentadas
1. CLI `cmd/echo-runtime-control` NO creado: M05 (utility del despliegue existente; control plane in-process en echo-core + paquete runtimecontrol como única ruta de submit). Operacionalización del binario queda para G-ENV.
2. MQL/EA (`execution_agent_v3.mq4/.mq5`) NO editados: sin compilación ni terminal; el gate Bridge-side hace imposible expansión FX sin permit; coexistencia FX armada NO_GO hasta capability (M03).
3. Migración 081 (no 076/077): coordinación M07 con The Lab V4 (076–080 tomados en lab-v4/shot4-integration).
4. Renumeración y re-pins de `m2_pin_test.go` con justificación por archivo (GOD-03 §8); archivos no tocados permanecen byte-idénticos.
5. Enforcement de ProtectionCapability en claimDenial: obligación ya adjudicada (GOD-02 §10 + M04), no decisión nueva; integración con permit/CheckAdmission propuesta al Manager como observación.
6. Flake preexistente `TestLegacy_UnifiedBatchRoutingUnchanged` (comparaba timestamps de creación, fallaba ~1/3 en frontera de ms) normalizado por W2 con justificación.
7. Compatibilidad fail-closed intencional: arranque de Core con futures/enabled sin registro/manifest vigente ahora exige la ruta de control (bootstrap token o restore) — reduce disponibilidad legacy por diseño (GOD-03 §4, release notes).

## Límites y estado físico
Sin deploy, sin ETCD/Kafka/Flink/PG compartidos, sin cuentas ni órdenes, sin merge a master, sin tocar The Lab/Forge/backtester. ETCD/REST del runtimecontrol con fakes en tests; `read_committed` contra transacciones reales = capa L3 (G-ENV). El estado operativo documentado permanece DESARMADO; esta entrega no constituye verificación física nueva.

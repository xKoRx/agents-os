---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo Forge — Factory V2 Completion]]"
sprint:
start: 2026-09-10
due:
progress: 70
repo: xKoRx/symphony
jira:
prs:
aliases:
  - F-04 Magic allocation version seal handoff
  - Echo Forge F-04 implementation
  - StrategyVersion seal handoff
tags:
  - kind/project
  - area/echo
  - agent/owner
created: "2026-09-10"
updated: "2026-09-12"
---

# Echo Forge — F-04 Magic allocation, version seal and handoff

%% Naming: Echo Forge — F-04 Magic allocation, version seal and handoff es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo Forge — F-04 Magic allocation, version seal and handoff
> **Área:** [[Echo]] · **Estado:** review · **Prioridad:** P1 · **Parent:** [[Echo Forge — Factory V2 Completion]] · **Repo:** `xKoRx/symphony`
> Subproyecto de implementación de la fase F-04. Contrato: [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]].

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre [[Echo Forge — Factory V2 Completion]] enlaza esta fase. El humano sigue el track desde [[Echo — Producto Integrado]].

## 🎯 Objetivo

Materializar el pipeline contractual Forge: allocation durable de magic → stamp/readback → compile/verify bytes → StrategyVersion seal → HandoffManifestV1 write-once → thin adapter. S0 pin `91671f6f`. CC = `CC_MISSING_OWNER_GATE` (no allocation física de producción). No escribir DB Echo. No tercer dominio Integration.

## 📊 Estado actual

- **TOP READY (2026-09-12).** El STOP de NORMAL queda resuelto: la autoridad de `compile_evaluation_ref` es un `domain.EvaluationRef` real sellado por StageExecution `mt5_compiler@mt5-compile.v1` en el plano Durable Foundation existente. **MIGRATION 017 = NO.** PHYSICAL sigue operacionalmente pending (host compile/SQX); eso no bloquea el plan. E-04 consumer READY `@ a99f9a6`; T21/AC-37 espera golden auténtico tras T2.
- **READY FOR MANAGER REVIEW (2026-09-11).** Owner gate resuelto: Magic Number V1 (`YYMMIIIDSSS`, 11 dígitos) implementado sobre `1999da1` en commit `ea8be76` (pushed). `CC_MISSING_OWNER_GATE`/`GateMagicCandidateSource` eliminados de producción; allocation V1 con catálogo/contador durables (migration 016), wiring productivo desde el control plane. SOURCE+CONTRACT+CONCURRENCY+MIGRATION PASS (`-race`; sweep paquete registry-postgres = mismos 4 fallos pre-existentes baseline). `PHYSICAL: BLOCKED — entorno`: mt5-kronos (Windows) tiene MetaEditor64 pero no SQX/sqcli para el stamp .sqx→.mq5 y los hosts Linux del stack son viewer/read-only esta sesión; no se finge PHYSICAL. INTEGRATION espera E-04. Worktree CLEAN.
- HEAD Symphony `9fad768ccd1f9d25ebb535a2d26edb3d74556c10` (merge autorizado `origin/master` y pushed a la feature); `origin/master` real `0b9742b09019526a8119f086199d15d1f0d42cb1`; merge-base actual `0b9742b09019526a8119f086199d15d1f0d42cb1`; `ea8be76` y `origin/master` son ancestros. Worktree: dirty foráneo preservado en `specs/FEAT-SQX-STRATEGY-EVALUATION/fixtures/phase4_performance.json`, reescrito por suite ajena; no restaurado ni borrado.
- S0 pin ya certificado por F-04; no se reabre ni se copian tipos desde Echo.
- CC: **resuelto — Magic Number V1 frozen** (owner decision 2026-09-11; `YYMMIIIDSSS`, XAUUSD=001). E-04 authority real: `xKoRx/echo@a99f9a63354bbe72219d1e590bb93757ed08e45e`; boundary integrado, T21/AC-37 espera el golden auténtico de Forge.
- `DATABASE MIGRATION: 015_strategy_magic_version_seal_handoff` + `016_magic_number_v1_allocator` (catálogo inmutable + contador mensual).
- Agents OS vault sin `.git` (degraded); última SHA durable de journal `f1070bec27db3ca415fe24f3c3576139674b7e09`.
- `GOD REQUIRED: NONE`.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/symphony | `feature/f04-magic-version-handoff` | `0b9742b09019526a8119f086199d15d1f0d42cb1` reconciliado | [[Echo Forge — Factory V2 Completion]] F-04 | [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]] | **TOP READY — compile Evaluation authority frozen; NORMAL T2 pending manager** |

## Parent / SPEC / baselines

- Parent: [[Echo Forge — Factory V2 Completion]]
- SPEC: [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]] — `VAULT_ROOT/30-resources/applications/Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract.md`
- Frozen: S0 pin; Live Authority §3; F-01/F-02/F-03 CLOSED no se reabren; B1/B2 no-touch.

## Source map

Magic TaskSpec: `sqx/core/runtime/config.go` `ApplySelectedRunTaskConfig.MagicNumber`; validate `mt5_task_config.go`. Apply: `sqx/adapters/apply-selected-run/binding/contract.go` `ApplicationConfig` + `HashIdentity`; physical `durable_apply_selected_run_physical.go` `writeApplySelectedRunProperties`; Java `EchoForgeRobustRunExporter`. Compiler físico `sqx/adapters/mt5/artifact_compiler.go` `ArtifactCompiler.Compile` via `MT5ArtifactActivities.CompileArtifact` (`mt5_compile_artifact` en `sqx-mt5-queue`). Caller compile: `generic_workflow.go` `executeMT5CompilerTask` → `executeMT5ArtifactTask` → child `MT5CompileArtifactWorkflow`. Identity `persistence_identity.go` `NewEvaluationRef` / `NewStageExecutionIdentity`. Finalist V2: `runFinalistPromotion` / `decision.go` policy `2.0.0`. F-04 actual: `sqx/core/forge/handoff_producer.go`, `sqx/core/capabilities/handoff.go`, StrategyVersion stores y migration 015/016. **Gap cerrado en planning:** compile no llama `ResolveStageExecution`/`PutEvaluation`/`CompleteStageExecution`; el patrón vivo a reusar es `persistMT5ReconcileV1` + `durable_apply_selected_run.go` recover/complete. `UseDurableMagicAllocation` existe pero el caller `runDurableApplySelectedRun` nunca lo setea. No existe HTTP E-04 en Symphony (`FakeConsumerIngress` only).

## Requirement-to-evidence

| Req | State | Evidence |
|---|---|---|
| Durable unique magic CAS | missing | no table; 888111 shared |
| Same identity replay | missing | no allocator |
| Stamp readback == allocated | missing | assumed requested==applied |
| Seal S0 StrategyVersionRef | missing | no type |
| HandoffManifestV1 write-once | missing | no producer |
| Thin adapter + fakeconsumer | missing | no port |
| G22 zero POST | missing | no producer |
| CC gate | documented | `CC_MISSING_OWNER_GATE` |
| No Echo DB writes | keep | no echo-api |
| HashIdentity ≠ H() | missing as F-04 test | recipes coexist; no inequality gate in Forge |

## Decision register

| ID | status | resolution | source | phase |
|---|---|---|---|---|
| D1 sequence | TECHNICAL_RESOLUTION | Allocation **before Apply** for Apply cohort; Finalist V2 admits seal/handoff only | Live Authority §3; padre F-04 hypothesis | 1 |
| D2 mapping | TECHNICAL_RESOLUTION | 1:1 StrategyRef↔magic; 1:N StrategyVersion same magic | S0 G04/G05; Live Authority | 1 |
| D3 namespace | TECHNICAL_RESOLUTION | `forge-live` | S0 fixtures | 1 |
| D4 allocation_ref | TECHNICAL_RESOLUTION | `H("forge-magic-allocation.v1",[ns,canonical,magic_decimal])` | Live Authority | 1 |
| D5 CAS | TECHNICAL_RESOLUTION | UNIQUE(ns,strategy_ref)+UNIQUE(ns,magic)+SELECT-then-INSERT; conflict magic → next candidate N=32; never random/MAX+1/hostname | this SPEC | 1 |
| D6 reserved | TECHNICAL_RESOLUTION | `11111` y `888111` no allocatable | source defaults | 1 |
| D7 CC | TECHNICAL_RESOLUTION | `CC_MISSING_OWNER_GATE`; production physical Allocate fail-closed; tests inject MagicCandidateSource | O2 owner | 1 |
| D8 readback | TECHNICAL_RESOLUTION | XML `.sqx` + MQ5; mismatch FAIL CLOSED; no EX5 parse | source gap | 1 |
| D9 requested | TECHNICAL_RESOLUTION | TaskSpec magic si presente debe == allocated; else use allocated | D12 Apply TaskSpec | 1 |
| D10 seal recipe | TECHNICAL_RESOLUTION | S0 `StrategyVersionRef`; effective_inputs via `C()`/`H()` not HashIdentity | S0 evidence.go | 1 |
| D11 handoff | TECHNICAL_RESOLUTION | S0 `HandoffManifestV1` + IdempotencyKey + PayloadDigest; G22 0 POST | S0 promotion.go | 1 |
| D12 adapter | TECHNICAL_RESOLUTION | Port `HandoffIngress`; CONTRACT fakeconsumer; no provisional E-04 URL | E-04 To Do | 1 |
| D13 post-commit | TECHNICAL_RESOLUTION | timeout post-commit → `UNKNOWN_RECEIPT`; no re-POST | S0 G35; this SPEC | 1 |
| D14 migration | TECHNICAL_RESOLUTION | `015_strategy_magic_version_seal_handoff` | last 014 | 1 |
| D15 hashes | TECHNICAL_RESOLUTION | keep HashIdentity on Apply Evaluation internals; S0 recipes only on seal/handoff/allocation_ref | FR-4 | 1 |
| D16 compile_evaluation_ref | TECHNICAL_RESOLUTION | Autoridad = `domain.EvaluationRef` de un compile StageExecution `mt5_compiler@mt5-compile.v1` persistido en Mongo EvaluationEvidence + `sqx.stage_execution_results`. Produce sólo tras compile físico success verificado. Cardinalidad 1. Recovery por ref exacta / `LoadEvaluation`, nunca latest. MIGRATION 017 NO. | Durable Foundation; `persistMT5ReconcileV1` analog; this TOP 2026-09-12 | 2 |

## Technical resolution — compile Evaluation (frozen 2026-09-12)

Hipótesis preferida **aceptada con prueba de source**. `EvaluationEvidence` existente representa compile; `ResolveStageExecution` / `PutEvaluation` / `CompleteStageExecution` / `LoadStageExecutionResults` / `LoadEvaluation` ya sellan refs inmutables. No hay stage contract compile hoy (`mt5_compiler@` ausente); se congela uno nuevo con la fórmula canónica `CanonicalStageKey(taskType, producerContractVersion)`, no un identity system nuevo.

### Source trace (authority → símbolo → identidad durable → replay)

1. **Caller ArtifactTaskRequest:** `generic_workflow.go` `executeMT5CompilerTask` → `executeMT5ArtifactTask` → `startMT5ArtifactChildren`. Identidad de routing: `RequestID` + `SourceKey`; durable: `FlowIntentToken`+`FlowRunRef`+`TaskPath`+`StrategyRef`+`SourceArtifact`. Replay Temporal: child workflow ID `MT5ArtifactChildWorkflowID`; no es EvaluationRef.
2. **StageExecution compile (hoy ausente):** debe crearse como Apply/MT5 reconcile, no existe en compile. Identidad futura: `NewStageExecutionIdentity` `TaskType=mt5_compiler` `ProducerContractVersion=mt5-compile.v1` subject STRATEGY `Generation=1`. Replay: `ResolveStageExecution` converge por `execution_intent_key`; retry Temporal no crea otro slot.
3. **Child workflow:** `MT5CompileArtifactWorkflow` → `ExecuteMT5CompileArtifactActivity`. Identidad Temporal only. Replay: MaximumAttempts ilimitado; contract/source_not_found non-retryable.
4. **Compile activity:** `MT5ArtifactActivities.CompileArtifact` (`mt5_compile_artifact`) en `sqx-mt5-queue`. Resultado `ArtifactTaskResult` (EX5/log/source). Retry infra; functional fail retorna `Status=failed` error nil — **no Evaluation**.
5. **Compiler físico:** `mt5.ArtifactCompiler.Compile` / `evaluateCompileArtifacts`. Bytes EX5+log en MinIO. SHA/size son integridad de artifact, no EvaluationRef.
6. **Evidence writer comparable:** `apply-selected-run/binding.BuildEvidence` + `DurableApplySelectedRunActivity.persistApplyEvidenceAndComplete`; MT5 analog `adapters/mt5/binding.PersistEvidence` llamado desde `persistMT5ReconcileV1` en **parent queue** (`sqx-worker`), no en Windows.
7. **Helpers Evaluation:** `domain.NewEvaluationRef(stageExecutionRef, subject.Digest, scopeDigest, producerContractVersion)`; Apply `BuildEvidence`; MT5 `binding.BuildSubject`/`BuildScope`.
8. **PutEvaluation:** `capabilities.ImmutableEvidenceStore.PutEvaluation` → `adapters/metadata-mongo/evidence_store.go`. Same digest ACK; distinct digest CONTRACT_CONFLICT.
9. **CompleteStageExecution:** `ControlPlane.CompleteStageExecution` inserta `sqx.stage_execution_results` y sella COMPLETED. Replay same ref set ACK; distinct set CONTRACT_CONFLICT. Empty set sólo si no hay producer-output.
10. **Exact readback:** `LoadStageExecutionResults(exact StageExecutionRef)` + `LoadEvaluation(exact EvaluationRef)`. Apply `recoverCompleted` exige `len(EvaluationRefs)==1`.
11. **Finalist V2:** `generic_workflow.go` `runFinalistPromotion` → `FinalistPromotionActivityName`. Decision write-once. Membership estructural; rank no entra.
12. **StrategyVersion seal:** `ControlPlane.SealStrategyVersion` / `domain.StrategyVersionIdentity.Ref` receta S0. Capacidades `VerifyMagicReadback` + `VerifyCompiledArtifactForSeal` existen **sin caller productivo**.
13. **Handoff producer:** `forge.BuildHandoffManifest` copia `HandoffArtifacts.CompileEvaluationRef` a S0 `BuildLineage`. Callers productivos: **ninguno** (sólo tests). Delivery: `capabilities.DeliverHandoff` + `echo-handoff.FakeConsumerIngress`.

### Compile Evaluation contract

| Campo | Valor frozen |
|---|---|
| `stage.key` | `mt5_compiler` (TaskSpec.Type vivo) |
| `stage.contract_version` | `mt5-compile.v1` |
| StageKey | `mt5_compiler@mt5-compile.v1` |
| Subject | `STRATEGY` / StrategyRef UUID / digest `HashIdentity("mt5-compile-strategy-subject.v1", JSON {schema,strategy_ref})` — artefact SHA no entra al subject |
| InputEvaluationRefs | exactamente uno: role `source_evaluation` = `StrategyArtifact.EvaluationRef` del carrier (la Evaluation SQX que `mt5_exporter` ya `LoadEvaluation`). Compile persist **no** busca Apply por latest. Assembler F-04 exige que esa Evaluation tenga `Stage.Key=apply_selected_run` y `ContractVersion=sqx-apply-selected-run.v1`; si no, no seal/handoff |
| Scope JSON | `{"schema":"mt5-compile-scope.v1","platform":"MetaTrader5","compiler":"MetaEditor64 /portable"}`. Prohibido: host, worker, Temporal IDs, timestamps, request ID, artifact SHA |
| ScopeDigest | `HashIdentity("mt5-compile-scope.v1", canonical JSON)` |
| Producer.component | `sqx-mt5-compile` |
| Producer.contract_version | `mt5-compile.v1` (identidad semántica; participa en EvaluationRef) |
| Producer.build_ref | `mt5-compile.v1` (provenance de contrato, no git SHA; igual convención Apply) |
| Artifacts | INPUT `STRATEGY_MQ5` = source MQ5 durable; OUTPUT `EX5` = PrimaryDurable; EVIDENCE `LOG` = compile log durable. SQX es dependencia upstream vía `source_evaluation`, no INPUT directo del compile |
| Payload | `{"schema":"mt5-compile-payload.v1","result":"success","error_count":0}` — no duplicar bytes ya en ArtifactRef |
| ConfigurationSnapshot | `{"schema":"mt5-compile-config.v1","compiler":"MetaEditor64 /portable","platform":"MetaTrader5"}` — no `{}` |
| Variant | `{"schema":"mt5-compile-variant.v1","operation":"compile"}` |
| EvaluationRef | `domain.NewEvaluationRef(stageRef, subject.Digest, scopeDigest, "mt5-compile.v1")` |
| CreatedAt | metadata only; no identidad (igual MT5 evidence) |

### Success / failure

- **Success:** EX5 non-empty + SHA/size match + compile log `Result: 0 errors` + source MQ5 SHA == expected `SourceArtifact` (`VerifyCompiledArtifactForSeal` **antes** de `ResolveStageExecution`). Entonces Persist: Resolve → PutEvaluation → CompleteStageExecution(`[exactly 1 ref]`).
- **Functional failure:** no Evaluation de éxito; no Complete con ref usable. No crear fila StageExecution (parser-before-write como `mt5_reconcile_v1`). No es candidato de seal/handoff.
- **Infra / cancel:** error retryable; sin fake success; StageExecution no se abre. Cancel Temporal nativa del compile activity.

### Replay / UNKNOWN_COMMIT / cardinality

- Mismo StageExecution + mismos bytes/evidence → mismo EvaluationRef (PutEvaluation ACK; Complete ACK).
- Mismo slot + contenido inmutable distinto → PutEvaluation / Complete `CONTRACT_CONFLICT` (payload digest o result set).
- Evidence ACK perdido: retry recomputa el mismo ref y `LoadEvaluation(exact)`; no latest.
- UNKNOWN_COMMIT: retryable; `ResolveStageExecution` reconcilia UUID existente; un solo EvaluationRef.
- Retry Temporal / Run ID distinto: no cambia `ExecutionIntentKey` ni EvaluationRef.
- **Cardinalidad:** 1 StageExecution success → exactamente 1 EvaluationRef. 0 → no seal/handoff. >1 → `CONTRACT_CONFLICT`. Nunca first/latest.

### Caller seam (no topología global)

No se declara “compile always followed by seal”. Dos seams existentes y opt-in:

1. **Produce (MUST):** `executeMT5ArtifactTask` tras compile `PersistenceModelV1` + `ArtifactStatusSuccess` → nueva activity `mt5_compile_persist_v1` en queue padre (`sqx-worker`), espejo de `persistMT5ReconcileV1`. El persist **no** corre en `sqx-mt5-queue`. Devuelve StageExecutionRef+EvaluationRef; el parent escribe `StrategyArtifact.CompileEvaluationRef` **sin** pisar `EvaluationRef` (Apply/source).
2. **Consume (MUST):** `runFinalistPromotion` tras Decision V2 completed → activity `forge_seal_handoff_v1`. Por cada member: exact Finalist Decision + StrategyRef + MagicAllocation + Apply EvaluationRef (carrier `EvaluationRef` validado como Apply) + Compile EvaluationRef (carrier o `LoadStageExecutionResults` de la StageExecution re-resoluble por intent) + bytes verificados → `SealStrategyVersion` → `BuildHandoffManifest` → persist write-once → `DeliverHandoff`. G22: membership vacío → 0 manifests.

`UseDurableMagicAllocation` debe setearse en `runDurableApplySelectedRun` para el path F-04; hoy el flag existe y el caller productivo lo deja false.

### Migration

**MIGRATION 017 REQUIRED: NO.** Mongo EvaluationEvidence + PG `stage_executions` + `stage_execution_results` expresan el hecho. 015/016 no-touch. Un reader `LoadStageExecutionIdentityByIntent` sería MAY sobre índice UNIQUE existente, no migración.

### E-04 join (plan, no HTTP client en este TOP)

Tras T2 compile+seal+handoff: Finalist real → manifest canónico → `POST /api/v1/forge/promotions` → receipt `INGESTED` → GET by-key → golden T21/AC-37. Consumer Echo `@ a99f9a63354bbe72219d1e590bb93757ed08e45e`. Puerto `HandoffIngress.Deliver(ctx, ns, *HandoffManifestV1, payloadDigest)`.

### PHYSICAL (operacional, no planning blocker)

Host mínimo para NORMAL cert: (1) SQX/sqcli con licencia válida para exporter MQ5 — si SQX reporta expired: STOP owner, sin trial-key; (2) MetaEditor64 `/portable` en worker `sqx-mt5-queue`; (3) PG control plane + Mongo evidence + object store; (4) reachability HTTP Echo promotions. No convertir viewers read-only en workers. `mt5-kronos` inaccesible es blocker de ejecución, no de este plan.

### Dirty worktree

`specs/FEAT-SQX-STRATEGY-EVALUATION/fixtures/phase4_performance.json` es dirty foráneo. NORMAL trabaja en worktree aislado o lo preserva. No restaurar/borrar/commitear en F-04.

## Planned diff

Fase 1 (T1.x) **done** en `ea8be76`. Fase 2 (T2.x) implementa compile Evaluation + caller F-04 + HTTP E-04.

### MUST

- create `sqx/adapters/mt5-compile/binding/` (`contract.go`, `evidence.go`, `subject.go`) — no reusar `adapters/mt5/binding` (ese paquete es `mt5_backtesting@mt5-backtest.v1`)
- create `sqx/activities/worker/mt5_compile_persist_activity.go` activity name `mt5_compile_persist_v1`
- modify `sqx/cmd/sqx-worker/main.go` register persist (parent worker, **not** mt5-worker)
- modify `sqx/workflows/generic_workflow.go` `executeMT5ArtifactTask`: tras compile V1 success llamar persist (espejo `persistMT5ReconcileV1`); `runFinalistPromotion` tras V2 → seal/handoff
- modify `sqx/core/runtime/config.go` `StrategyArtifact.CompileEvaluationRef` omitempty; no pisar `EvaluationRef`
- modify `sqx/workflows/durable_apply_selected_run_workflow.go` set `UseDurableMagicAllocation: true` en el path F-04
- create `sqx/activities/worker/forge_seal_handoff.go` (`forge_seal_handoff_v1`) using existing `VerifyMagicReadback` / `VerifyCompiledArtifactForSeal` / `SealStrategyVersion` / `BuildHandoffManifest` / `DeliverHandoff`
- create `sqx/adapters/echo-handoff/http_ingress.go` implementing `HandoffIngress` over Echo POST `/api/v1/forge/promotions` + GET by-key
- tests: persist identity/replay/conflict/UNKNOWN_COMMIT/cardinality; assembler fail-closed sin compile eval; SOURCE greps no latest

### MAY

- `StageExecutionReader.LoadStageExecutionIdentityByIntent` sobre UNIQUE `execution_intent_key` (no migración)
- `StageProducerOutput` para EX5 compile (Apply lo usa; compile locator no depende de StageExecution UUID)
- campo `EvaluationRef` en `ArtifactTaskResult` (el persist result basta)

### NO-TOUCH

Migrations `015_strategy_magic_version_seal_handoff` y `016_magic_number_v1_allocator`. Magic V1 `YYMMIIIDSSS` / XAUUSD=001. F-01 CanonicalStrategyID. F-02 membership. F-03 SQX lifetime. B1/B2 ownership/takeover/Slot Pool. StrategyVersion S0 recipe. S0 `BuildLineage` fields. Echo source/DB. ranking-as-membership. delivery terminal semantics / `UNKNOWN_RECEIPT`. F-05. `adaptive_workflow.go`. `adapters/mt5/binding` backtest contracts. Foreign dirty `phase4_performance.json`. Invented EvaluationRef from SHA/key/workflow ID.

## No-touch

F-01 CanonicalStrategyID/publication. F-02 policy `finalist_promotion@2.0.0`. F-03 timeouts. F-05. B1A/B1B/B2 Slot Pool/fencing/takeover. Echo source. S0 types (consume, don't fork). `adaptive_workflow.go`. Foreign dirty symphony. Invented CC ranges. Provisional Echo HTTP distinto de E-04. Magic V1 codec/catálogo. HashIdentity newline como `H()`.

## Execution sequence

T1.1–T1.18 **done**. T2.1 binding → T2.2 persist activity → T2.3 wire `executeMT5ArtifactTask` → T2.4 carrier `CompileEvaluationRef` → T2.5 recovery/UNKNOWN_COMMIT/cardinality tests. T2.6 `UseDurableMagicAllocation` caller. T2.7 seal assembler. T2.8 handoff assembler after Finalist V2. T2.9 HTTP ingress. T2.10 auth/config. T2.11 golden capture. T2.12 PHYSICAL. T2.13 cross-lane T21/AC-37.

T2.3 after T2.2. T2.4 with T2.3. T2.5 after T2.2. T2.6 ∥ T2.1–T2.5. T2.7 needs T2.3+T2.6. T2.8 needs T2.7. T2.9 after T2.8 CONTRACT. T2.11 after T2.8. T2.12/T2.13 PHYSICAL/INTEGRATION.

## Dependencies

F-01 CLOSED (stable IDs). F-02 CLOSED (V2 membership). F-03 CLOSED (no-touch). E-01 S0 pin. E-04 optional for INTEGRATION (development E-04 may run now; integrate/CROSS_LANE gated by E-03 CONTRACT_PASS). CC owner for PHYSICAL allocation.

## ✅ Tareas

> [!note]+ Ownership
> Board `#owner/agent`. Cada ítem es una TASK atómica para NORMAL tras autorización del manager.

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. %%
> - [x] T1.1 go.mod pin S0 contracts + test HashIdentity ≠ H() #owner/agent #type/dev #area/echo
> - [x] T1.2 migration 015 strategy_magic + versions + manifests + deliveries #owner/agent #type/dev #area/echo
> - [x] T1.3 allocator CAS/replay/reserved 11111+888111 #owner/agent #type/dev #area/echo
> - [x] T1.4 CC_MISSING_OWNER_GATE + fixture MagicCandidateSource #owner/agent #type/dev #area/echo
> - [x] T1.5 Apply stamp usa allocated; requested must match #owner/agent #type/dev #area/echo
> - [x] T1.6 readback XML MagicNumber del .sqx #owner/agent #type/dev #area/echo
> - [x] T1.7 readback MQ5 MagicNumber #owner/agent #type/dev #area/echo
> - [x] T1.8 mismatch FAIL CLOSED no seal/handoff #owner/agent #type/dev #area/echo
> - [x] T1.9 compile verify size/sha/0-errors/source sha #owner/agent #type/dev #area/echo
> - [x] T1.10 StrategyVersion seal S0 write-once #owner/agent #type/dev #area/echo
> - [x] T1.11 HandoffManifestV1 producer S0 + MemberProof V2 #owner/agent #type/dev #area/echo
> - [x] T1.12 handoff_manifests write-once DetectSealedConflict #owner/agent #type/dev #area/echo
> - [x] T1.13 HandoffIngress + fakeconsumer CONTRACT #owner/agent #type/dev #area/echo
> - [x] T1.14 delivery states; no re-POST post-commit #owner/agent #type/dev #area/echo
> - [x] T1.15 corpus G04–G10 G19–G25 G22 #owner/agent #type/dev #area/echo
> - [x] T1.16 concurrent allocation same/different identity #owner/agent #type/dev #area/echo
> - [x] T1.17 BWC no backfill 888111; brownfield sin fila magic #owner/agent #type/dev #area/echo
> - [x] T1.18 SOURCE greps ownership/latest/ranking/HashIdentity-on-S0 #owner/agent #type/dev #area/echo
> - [ ] T2.1 compile Evaluation binding contract `mt5-compile.v1` #owner/agent #type/dev #area/echo
> - [ ] T2.2 `mt5_compile_persist_v1` activity + PutEvaluation/CompleteStageExecution #owner/agent #type/dev #area/echo
> - [ ] T2.3 wire persist after durable compile success in `executeMT5ArtifactTask` #owner/agent #type/dev #area/echo
> - [ ] T2.4 carrier `CompileEvaluationRef` exact pointer #owner/agent #type/dev #area/echo
> - [ ] T2.5 exact recovery UNKNOWN_COMMIT cardinality CONTRACT_CONFLICT #owner/agent #type/dev #area/echo
> - [ ] T2.6 `UseDurableMagicAllocation` productive caller #owner/agent #type/dev #area/echo
> - [ ] T2.7 seal assembler exact Apply+Compile+readback+verify #owner/agent #type/dev #area/echo
> - [ ] T2.8 handoff assembler after Finalist V2 #owner/agent #type/dev #area/echo
> - [ ] T2.9 Echo HTTP `HandoffIngress` POST+GET by-key #owner/agent #type/dev #area/echo
> - [ ] T2.10 Echo ingest auth/config #owner/agent #type/dev #area/echo
> - [ ] T2.11 authentic Forge golden capture #owner/agent #type/dev #area/echo
> - [ ] T2.12 PHYSICAL certification host capabilities #owner/agent #type/dev #area/echo
> - [ ] T2.13 cross-lane smoke Echo T21/AC-37 #owner/agent #type/dev #area/echo

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label]of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any)dv.paragraph("_Sin tareas._");}
const owner=((dv.current().owner)==="agent")?"agent":"me";
const all=dv.current().file.tasks.array();
const primary=all.filter(t=>has(t,`owner/${owner}`));
const loose=all.filter(t=>!has(t,"owner/me")&&!has(t,"owner/agent"));
dv.header(3, owner==="agent"?"🤖 Tareas del agente":"🧍 Mis tareas");
board(primary);
if(loose.length){dv.header(3,"🧺 Sin owner (clasificar)");render(loose);}
```

## Atomic tasks

Contrato de cada TASK: `archivo/símbolo → cambio exacto → authority → failure/retry → tests → DONE`. Sin decisiones arquitectónicas en NORMAL.

### T1.1 pin S0 contracts + HashIdentity ≠ H()

- **Modelo:** NORMAL
- **Archivos/símbolos:** `sqx/go.mod` (o módulo que compile el worker) require `github.com/xKoRx/echo/v3/sdk/contracts` @ `91671f6f46ffa889a79aed0979cb3b4e5821ed33`; test nuevo junto a `persistence_identity.go`.
- **Cambio:** importar el módulo nested S0. Test: mismo tag+parts → `domain.HashIdentity` ≠ `wire.HashTagged`. No modificar `hashIdentity`.
- **Authority:** FR-4; S0 `wire/hash.go` + `hash_legacy_inequality_test.go` patrón.
- **Failure/retry:** n/a (compile).
- **Tests:** `TestHashIdentity_DoesNotEqualS0H`.
- **DONE:** `go test` del paquete identity + módulo contracts se importa. Pin exacto en go.mod.
- **Stop:** fork de tipos S0 dentro de Symphony → PLAN_CONFLICT.

### T1.2 migration 015

- **Modelo:** NORMAL
- **Archivos:** `sqx/adapters/registry-postgres/migrations/015_strategy_magic_version_seal_handoff.up.sql` + `.down.sql`; runner de migrations existente.
- **Cambio:** tablas/UNIQUE/CHECK/FK exactos de la SPEC. Down solo DROP de esas tablas.
- **Authority:** SPEC migration section; last `014`.
- **Failure/retry:** restart-safe; no rewrite history.
- **Tests:** brownfield: DB con 014 applied → 015 up; strategies sin fila magic; down/up.
- **DONE:** migration aplica sobre dump 014; down no toca 001–014.
- **Stop:** ALTER destructivo de `sqx.strategies` history → PLAN_CONFLICT.

### T1.3 allocator CAS

- **Modelo:** NORMAL
- **Archivos:** `sqx/core/capabilities` `MagicAllocator`; `sqx/core/domain` allocation types; `sqx/adapters/registry-postgres` insert/SELECT.
- **Cambio:** algoritmo Allocate de la SPEC. `allocation_ref` vía `contracts`/`wire.HashTagged("forge-magic-allocation.v1", ...)`. Reserved skip.
- **Authority:** D3–D6.
- **Failure/retry:** matrix Allocate rows.
- **Tests:** replay same StrategyRef; two StrategyRefs unique; unique-violation retry next candidate; reserved 888111 rejected.
- **DONE:** tests verdes; PRODUCTION source no MAX+1.
- **Stop:** hostname/worker in key → PLAN_CONFLICT.

### T1.4 CC gate + fixture source

- **Modelo:** NORMAL
- **Archivos:** `MagicCandidateSource` interface; production impl returns `CC_MISSING_OWNER_GATE`; test fixture yields injected int64s.
- **Cambio:** production Allocate físico no INSERT sin CC. CONTRACT tests usan fixture source.
- **Authority:** D7.
- **Failure/retry:** CC missing = no INSERT, non-terminal for CONTRACT.
- **Tests:** production path error code; fixture path allocates.
- **DONE:** grep no hardcoded CC ranges.
- **Stop:** inventar rangos Forex → viola CC gate.

### T1.5 Apply stamp allocated

- **Modelo:** NORMAL
- **Archivos/símbolos:** `EffectiveConfig` / `durable_apply_selected_run_physical.go` `writeApplySelectedRunProperties`; validate requested vs allocated.
- **Cambio:** properties `strategy.magic_number=<allocated>`. Si TaskSpec magic presente y ≠ allocated → `CONTRACT_CONFLICT` pre-stamp.
- **Authority:** D8/D9. No cambiar D13 four-properties set salvo el valor de magic.
- **Failure/retry:** pre-stamp conflict terminal; Apply recovery existing KEEP.
- **Tests:** allocated written; mismatch requested fails before SQX.
- **DONE:** properties usan allocated; 888111 no se escribe en path F-04 salvo que estuviera uniquely allocated (prohibido).
- **Stop:** seguir leyendo ETCD hot-path F-04.

### T1.6 XML readback

- **Modelo:** NORMAL
- **Archivos:** parser de `<Variable name="MagicNumber">` (o nodo equivalente del exporter) sobre bytes `.sqx` de output.
- **Cambio:** extraer int64; comparar con allocated.
- **Authority:** Java `EchoForgeRobustRunExporter` node.
- **Failure/retry:** parse fail = mismatch path.
- **Tests:** fixture XML 11111 vs 888111 vs allocated; missing node fails closed.
- **DONE:** parser no asume requested.
- **Deps:** T1.5.

### T1.7 MQ5 readback

- **Modelo:** NORMAL
- **Archivos:** parser de `input … MagicNumber` en `.mq5` exportado.
- **Cambio:** igual T1.6 sobre mq5.
- **Authority:** SQX `SourceCode.generate`.
- **Tests:** mq5 con MagicNumber distinto falla.
- **DONE:** ambos readbacks en el pipeline.
- **Deps:** T1.5. Paralelo T1.6.

### T1.8 mismatch FAIL CLOSED

- **Modelo:** NORMAL
- **Archivos:** orquestación seal/handoff gate.
- **Cambio:** si XML≠allocated OR mq5≠allocated: no compile-as-seal-input, no StrategyVersion, no manifest.
- **Authority:** SPEC stamp contract.
- **Failure/retry:** terminal `CONTRACT_CONFLICT`.
- **Tests:** requested==allocated pero XML 11111 → no seal.
- **DONE:** test de no-seal en mismatch.
- **Deps:** T1.6+T1.7.

### T1.9 compile byte verify

- **Modelo:** NORMAL
- **Archivos:** `artifact_compiler.go` evaluateCompileArtifacts (reuse, no Slot Pool).
- **Cambio:** gate seal exige size/sha EX5, log 0 errors, source mq5 sha == exported mq5.
- **Authority:** existing compiler success gate.
- **Failure/retry:** compile fail retry técnico; digest mismatch terminal.
- **Tests:** missing ex5 / sha mismatch / nonzero errors → no seal.
- **DONE:** no seal without verified bytes.
- **Stop:** parsear EX5 magic.

### T1.10 StrategyVersion seal

- **Modelo:** NORMAL
- **Archivos:** store `sqx.strategy_versions`; `contracts.StrategyVersionRef(...)`.
- **Cambio:** persist write-once; effective_inputs via S0 `C()`/`H()`; no HashIdentity.
- **Authority:** S0 `evidence.go` StrategyVersionRef.
- **Failure/retry:** replay same digest OK; distinct → CONTRACT_CONFLICT.
- **Tests:** same inputs same ref; different exec sha different ref; HashIdentity of config ≠ effective_inputs_sha256.
- **DONE:** roundtrip Validate-equivalent identity.
- **Deps:** T1.2+T1.8+T1.9.

### T1.11 HandoffManifestV1 producer

- **Modelo:** NORMAL
- **Archivos:** producer construye `contracts.HandoffManifestV1`; `Validate(supported=[forge-echo-ingestion.v1])`.
- **Cambio:** MemberProof desde Finalist V2 (requested/observed == strategy instrument/TF; tested hashes == version). Rank/score no entran. Empty membership → 0 manifests.
- **Authority:** S0 promotion.go; F-02 membership.
- **Failure/retry:** Validate fail = no persist.
- **Tests:** G08 identity mismatch; G09 version digest; G11/G12 structural; G22 zero.
- **DONE:** `Validate` PASS on golden assembled from S0-compatible fields.
- **Deps:** T1.10. Stop: ranking-as-membership.

### T1.12 handoff write-once store

- **Modelo:** NORMAL
- **Archivos:** `sqx.handoff_manifests` adapter.
- **Cambio:** persist canonical body + payload_digest; DetectSealedConflict.
- **Authority:** S0 conflict.go.
- **Tests:** G06 converge; G07 409; G23/G24 as applicable at store layer.
- **DONE:** second persist same key different digest fails; same digest no-op.
- **Deps:** T1.11.

### T1.13 HandoffIngress + fakeconsumer

- **Modelo:** NORMAL
- **Archivos:** port + adapter wrapping `fakeconsumer.Consumer.Ingest`.
- **Cambio:** un manifest por llamada; ns `forge-live`. Cero HTTP inventado.
- **Authority:** S0 fakeconsumer.go.
- **Failure/retry:** CONTRACT statuses 201/200/409.
- **Tests:** Ingest G01-like body 201; replay 200; non-effects AssertNone.
- **DONE:** `fakeconsumer` tests del producer Forge verdes contra pin.
- **Stop:** URL Echo inventada.

### T1.14 delivery states

- **Modelo:** NORMAL
- **Archivos:** `sqx.handoff_deliveries`.
- **Cambio:** estados SPEC; timeout post-commit → `UNKNOWN_RECEIPT` sin re-POST.
- **Authority:** D13; G35.
- **Tests:** pre-commit retry increments attempts; post-commit unknown does not call Ingest twice with distinct side-effect simulation.
- **DONE:** matrix rows Echo unavailable / timeout pre / timeout post cubiertas.
- **Deps:** T1.13.

### T1.15 corpus G04–G10 G19–G25 G22

- **Modelo:** NORMAL
- **Archivos:** tests que cargan testdata del módulo contracts pin (o copies via `go:embed` del módulo, no fork).
- **Cambio:** producer/consumer gates listados en SPEC CERTIFICATION CONTRACT.
- **Authority:** `testdata/v1/manifest.json` @ 91671f6f.
- **Tests:** G04 reuse version/magic; G05 new version; G06/G07; G08–G10; G19 id limits; G20 magic>int32; G21 wire number; G22 zero POST; G23/G24/G25 where producer emits wire.
- **DONE:** corpus subset PASS; G22 assert 0 Deliver calls.
- **Deps:** T1.11–T1.13.

### T1.16 concurrency allocation

- **Modelo:** NORMAL
- **Archivos:** tests allocator (pgtestdb o control_plane_integration pattern).
- **Cambio:** none production beyond T1.3.
- **Authority:** D5.
- **Tests:** parallel Allocate distinct refs unique magics; same ref converges; crash/unknown via unique constraint.
- **DONE:** race detector on allocator tests.
- **Deps:** T1.3.

### T1.17 BWC brownfield

- **Modelo:** NORMAL
- **Archivos:** tests migration + allocator.
- **Cambio:** none backfill.
- **Authority:** BWC SPEC.
- **Tests:** existing strategy without magic row; Allocate does not write 888111; Apply legacy path still compiles (no-touch unless F-04 path selected).
- **DONE:** no UPDATE of historical config_snapshot magics.
- **Deps:** T1.2+T1.3.

### T1.18 SOURCE greps

- **Modelo:** NORMAL
- **Archivos:** tests/scripts de certificación.
- **Cambio:** none functional.
- **Authority:** SOURCE gates.
- **Tests:** grep F-04 path: no ListObjects-as-authority; no Echo SQL; no TopProjection as membership; no HashIdentity in allocation_ref/version_ref/payload_digest helpers.
- **DONE:** SOURCE scoped PASS.
- **Deps:** T1.3+T1.8+T1.10+T1.13.

## 📆 Bitácora

- **2026-09-12 (E-04 DEPENDENCY — FORGE GOLDEN FIXTURE).** Fetch completo y revisión de `master`/`origin/master` @ `0b9742b09019526a8119f086199d15d1f0d42cb1` y `feature/f04-magic-version-handoff`/`origin/feature/f04-magic-version-handoff` @ `ea8be76c4587b2d00e4cad8cf2a67c4fd8e6680f`; worktree limpio y `git diff --check` PASS. La feature no es descendiente del master actual (`merge-base --is-ancestor` devuelve 1), por lo que ambos pins quedan explícitos y no se mezclan.
- **2026-09-12 (producer audit).** `rg` sobre `sqx/core`, `sqx/adapters`, `sqx/activities` y `sqx/workflows` encontró `BuildHandoffManifest` únicamente en la definición productiva y cuatro llamadas de `handoff_producer_test.go`; no existe caller no-test que lo alimente desde Decision V2, StrategyVersion sellada, MagicAllocation persistida y artefactos verificados. `go test -count=1 -race ./sqx/core/forge ./sqx/adapters/echo-handoff` PASS sólo certifica el contrato sintético.
- **2026-09-12 (physical evidence audit).** El módulo S0 resuelto es `github.com/xKoRx/echo/v3/sdk/contracts@91671f6f46ff`; su corpus G04/G05/G12 contiene payloads de contrato, no preimages físicos de F-04. La feature no trackea `.mq5`, `.ex5` ni `compile.log`; su `testdata/v1` sólo contiene G06/G07/G20/G21/G22. En Zeus, Hera y Kronos, las búsquedas read-only no encontraron `handoff`, `StrategyVersion` o magic allocation; sólo aparecieron `.sqx` históricos y `.mq5` antiguos, sin `.ex5`/compile evidence del flujo F-04 actual.
- **2026-09-12 (decision).** No se copió S0, no se reutilizó corpus como golden, no se construyó payload a mano, no se calculó digest esperado y no se tocaron semántica F-04/Echo ni repos externos. Estado final: `BLOCKED / FORGE_GOLDEN_FIXTURE_PENDING`; Manager debe proporcionar o habilitar una ejecución F-04 real que produzca Decision V2 + StrategyVersion + allocation + readback/compile bytes y permita exportar todos los preimages referenciados.
- **2026-09-12 (F-04 correction audit).** Se verificó el seam único de `GenericSQXWorkflow`: la asignación durable no está activada en el request productivo y `ArtifactTaskResult` no persiste un `compile_evaluation_ref`; el resultado compile sólo transporta EX5, compile log y `SourceKey`. La corrección no se implementó porque no existe una autoridad durable simultánea para alimentar `BuildHandoffManifest` sin fabricar un ref o abrir una decisión arquitectónica. El sondeo read-only de `mt5-kronos` falló por resolución DNS; no se ejecutó SQX ni se declaró licencia. STOP — MANAGER REVIEW.
- **2026-09-11** — Join E-04: planning [[Echo — E-04 Forge Ingestion E1]] congela `POST /api/v1/forge/promotions` + GET by-key + envelope S0. F-04 CONTRACT `fakeconsumer` no se reabre. INTEGRATION real sigue esperando implementación E-04 **y** E-03 CONTRACT_PASS. No se inventa URL provisional distinta.
- **2026-09-10 (cierre NORMAL)** — Sello/readback/seal/handoff implementados: `sqx/adapters/magic-readback` (XML+MQ5 parsers fail-closed), `capabilities.VerifyMagicReadback`+`VerifyCompiledArtifactForSeal` (bytes reales, 0-errors), `domain` recetas S0 (EffectiveInputs/RuntimeContext/ExecutionManifest/DependenciesDigest vía `ExactInputRefsDigest`, StrategyVersionRef por recompute), store `SealStrategyVersion` write-once (replay/conflict), `core/forge` producer `BuildHandoffManifest` (Validate S0 PASS, membership estructural, G22 `HandoffMembersForDecision`), migration 015 con UNIQUE(decision_ref,version_ref) G24, stores handoff_manifests/handoff_deliveries, `capabilities.DeliverHandoff` (estados + UNKNOWN_RECEIPT sin re-POST + attempts), `adapters/echo-handoff` fakeconsumer CONTRACT (201/200/409/G24/non-effects/corpus G06-G07-G20-G21). Race verde en todos los paquetes F-04. Fixture de benchmark `specs/.../phase4_performance.json` lo reescriben tests ajenos — restaurado, worktree CLEAN.
- **2026-09-10 (sesión NORMAL)** — Branch `feature/f04-magic-version-handoff` (nombre del briefing; difiere del registrado arriba). T1.1–T1.4 committeados: pin S0 resuelto por SSH directo (`v0.0.0-20260910031519-91671f6f46ff`), migración 015 + runner + tests fresh/brownfield/down/restart, allocator CAS SELECT-then-INSERT con replay/colisión/reservados/exhaustión N=32, `GateMagicCandidateSource` = producción (`CC_MISSING_OWNER_GATE`), concurrencia same/distinct con `-race` verde. Nota: 4 tests pre-existentes fallan en baseline (`TestUpsertStrategyV2_V0V1V2Coexistence`, `TestControlPlane_AdoptStrategyV1ConcurrentFilenameVariantsConverge`, `TestRegisterStrategy_LegacyRollbackTargetsOnlyV0`, `TestControlPlane_AdoptStrategyV1UnexpectedUniqueFailsWithoutPoisonedRead`) — set idéntico en baseline y branch, sin regresión F-04. Delegación MiniMax bloqueada por plan limit; NORMAL ejecutó directo.
- **2026-09-11 (owner gate Magic V1, NORMAL)** — Sobre `1999da1`, commit `ea8be76`: codec `domain/magic_v1.go` (Encode/Decode/Validate, round-trip obligatorio, dirección L/S parseada estricta del canonical id, BOTH reservado D=3 sin inventar flow), migration `016_magic_number_v1_allocator` (`sqx.magic_instruments` con UNIQUE instrument/code + CHECK 001..999 + trigger inmutable; `sqx.magic_monthly_counters (period YYMM, instrument_code) → last_sequence` CHECK 0..999; seed XAUUSD=001 y AUDUSD/EURUSD/GBPUSD/NZDUSD/USDCAD/USDCHF/USDJPY=002..008 lexicográfico una vez), `ControlPlane.AllocateMagicV1` (upsert atómico initialize-or-increment RETURNING, guard <999 → `MAGIC_MONTHLY_CAPACITY_EXHAUSTED` sin wrap/reset, `INSTRUMENT_CODE_MISSING`, clock UTC determinista `cp.now`, replay-first reusa motor CAS/UNKNOWN_COMMIT), wiring productivo: `NewDurableApplySelectedRunActivity` deriva `MagicAllocatorV1` del control plane (gate fake sólo en tests). Correctivo: `assigned_at`/`sealed_at` truncados a µs → replay byte-equal (3 tests que fallaban por precisión en esta máquina quedan verdes; baseline queda en los 4 documentados). Tests: codec completo, concurrencia XAUUSD L/S/BOTH → {001,002,003} compartiendo contador, replay sin consumir ordinal y conservando magic septiembre en octubre, capacity #999 PASS/#1000 exhaust, catálogo exacto+inmutable+SILVER=009, PG fresh/brownfield 015→016/constraints/down/restart, todos `-race`. Físico: sondeo mt5-kronos vía SSH (MetaEditor64 en `C:\MT5\*`, worker desplegado; sin SQX/sqcli ni PG registry alcanzable; hosts Linux viewer) → PHYSICAL BLOCKED entorno, no se finge. Módulos privados Go resueltos por SSH (git insteadOf + GOPRIVATE). Fixture `phase4_performance.json` re-escrito por tests ajenos — restaurado, worktree CLEAN.
- **2026-09-10 (corrección G1, NORMAL)** — Correctivos sobre `24b807f`: `928d3db` (C1: UNKNOWN_COMMIT reconcilia solo vía SELECT durable — read failure preserva `ErrUnknownCommit` sin segundo Next/INSERT; identity race `pk_strategy_magic` converge solo leyendo al ganador, winner invisible falla cerrado `ErrContractConflict`; solo colisión `(ns,magic)` avanza candidate) y `1999da1` (C2: `canonicalBody` debe ser byte-equal a `manifest.Encode()` antes de todo efecto, sin JSONEq; C3: replay conflictivo preserva state/receipt/attempts, G24 sin delivery huérfana, guard atómico en `SaveHandoffDelivery` — INGESTED terminal, UNKNOWN_RECEIPT solo acepta re-park, sin state-machine nueva). Tests: 7 sqlmock fail-closed allocator, 2 contract (body gate + preservation con fakeconsumer), 5 PostgreSQL aislados migration 015 (INGESTED/UNKNOWN_RECEIPT/G24/replay idéntico/guard). Gates re-ejecutados: SOURCE 111 pass, CONTRACT+S0 corpus race verde, CONCURRENCY 26/26 `-race`, MIGRATION 5/5; sweep paquete completo = mismo set de 4 fallos pre-existentes baseline (verificado con/sin cambios, sin regresión). Migration 015 sin tocar. `PHYSICAL`/`INTEGRATION` unchanged. MiniMax delegación bloqueada (plan limit); ejecución directa.

## 🧭 Decisiones

Ver Decision register. Manager debe autorizar NORMAL.

## 🔗 Docs / Links

- [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]]
- [[Echo Forge — Factory V2 Completion]]
- [[Echo — E-01 Canonical SDK Foundation S0]]
- [[Echo — Live Platform V1]]
- [[Echo Forge — F-02 Finalist Model V2 Contract]]
- [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]
- [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]]

## 💡 Ideas

### Backlog de ideas

- Join INTEGRATION cuando E-04 certifique endpoint del mismo pin.

### Motivos / principios

- Fail closed. Write-once. S0 pin único. CC no se inventa.

### Memoria pública / interna

- **Memoria pública:** esta nota + SPEC.
- **Memoria interna:** no duplicar el contrato.
- **Motivo:** Agents OS planner único.

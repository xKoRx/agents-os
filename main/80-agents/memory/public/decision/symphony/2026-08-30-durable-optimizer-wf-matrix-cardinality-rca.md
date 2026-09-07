---
type: decision
schema_version: 1
scope: project
created: "2026-08-30"
updated: "2026-08-30"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[AGENTS OS]]"
related:
  - "[[2026-08-30-durable-project-stages-recovery-fault-certification]]"
  - "[[optimizer-wf-matrix-second-sqx-output]]"
  - "[[2026-08-30-durable-retester-optimizer-recovery-rca]]"
aliases:
  - DURABLE-OPTIMIZER-WF-MATRIX-CARDINALITY-RCA-TOP
  - optimizer two sqx cardinality
confidence: verified
source_session: DURABLE-OPTIMIZER-WF-MATRIX-CARDINALITY-RCA-TOP
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
---

# 2026-08-30-durable-optimizer-wf-matrix-cardinality-rca

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- RCA read-only sobre `xKoRx/symphony` @ `abe19d09a0bafc7ec21abbf54ca136684e202177` (`HEAD == origin/master == RCA_SOURCE == CERTIFIED_SOURCE` de release `0.2.81`; DRIFT: NONE). CODE CHANGES: NONE. Foreign dirty preexistente no mezclado.
- Golden fallido: RequestID `final-stages-recovery-cert-e2e-normal-20260830T200907Z-9511775d`, FlowRun `abcd39d4-03e8-4621-9095-50cae6eaafd6`, WorkflowID `sqx-main-v1-c719890e-004c-478c-9186-c0420deb1f76`, RunID `01a0544e-3baf-726e-aeca-39fcaf15b1bd`, Optimizer StageExecution `c95a655d-1dae-41a6-a0b4-782febe59608` (`Strategy_4.1.15.h0` / StrategyRef `28a432c4…`). Gate F8: `len(ResultFiles) > 1` → `CONTRACT_CONFLICT` antes de record/put. Fail-closed correcto. La pregunta era si la cardinalidad 0|1 vive en raw local `.sqx`.
- Premisas rechazadas: «Optimizer produce dos outputs lógicos»; «el segundo `.sqx` debe eliminarse». H1/H2/H3 se evaluaron con evidencia, no por preferencia.

## Decisión

- **H2 (con precisión):** el producer output contractual de `sqx-optimizer.v1` es **un** `.sqx` publishable: el databank SQX de Walk-Forward Matrix (filename histórico `WF Matrix - <name>.sqx` / `WF_Matrix_-_…`). El segundo archivo local (estrategia original/sidecar, ~42 KiB) **no** es un segundo output lógico ni una segunda Strategy. SAME_LOGICAL_STRATEGY=YES. Walk-forward **cells** (NDJSON de `evaluate_wfm`) siguen **no** siendo este producer.
- **H1 rechazada:** el `.sqx` pequeño no es el logical Optimizer output. El filtro histórico **conserva** `WF_Matrix` y **descarta** el sidecar. El stack de identidad documenta etapa 03* como `WF_Matrix_-_<StrategyID>.sqx` (`canonical_strategy_id.go`). Tests WFM/robust/optimizer usan esa key como Optimizer artifact.
- **H3 rechazada:** no hay dos artifact roles durables. NEW_SCHEMA_REQUIRED=NO. Evaluation sigue 0|1 `OUTPUT/STRATEGY_SQX`. StageProducerOutput sigue singleton.
- **Opción A (primaria):** RAW_LOCAL puede ser N. Clasificar/filtrar publishable **antes** del gate F8. Exigir 0|1 PUBLISHABLE. Solo el publishable entra a producer authority / Evaluation / MinIO. Auxiliares locales transitorios. `upload_prefix_filter=WF_Matrix` es routing brownfield **legítimo** del contrato de publicación (congelado 2026-07-12, `1e79137`), no identidad de negocio.
- **Opción C opcional/separada:** `DontSaveOriginalStr=true` en `optimizer_test.cfx` para que SQX no emita el sidecar. No es el fix mínimo; no sustituye el gate en la capa publishable.
- **F8_GATE:** `CARDINALITY_CHECK_AT_WRONG_LAYER`. Slice 2 midió raw `ResultFiles` (glob `*.sqx` post-SQX) en vez del output publishable que el filtro y `db_register` ya trataban como 0|1. Pre-`8caa97a` el mismo par físico era filtrado a 1 PUT.
- **OPTIMIZER_BINDING:** `INCOMPLETE` (comentario mezcla «WF_Matrix prefix / cells WFM» con el databank `.sqx`; ArtifactType `STRATEGY_SQX` y cardinalidad 0|1 **sí** describen el artifact publicado). No bump de `sqx-optimizer.v1`: la interpretación durable observable de Evaluation/producer no cambia; se restaura la semántica ya declarada.
- **WFM:** REQUIRES_WF_MATRIX_SQX=YES (el Optimizer artifact exacto, que históricamente **es** ese databank). REQUIRES_OPTIMIZED_SIDECAR=NO. REQUIRES_BOTH=NO. Authority = Optimizer EvaluationRef + DurableArtifactRef. `EchoForgeWFMExporter` lee `WalkForwardMatrixResult` del ResultsGroup cargado desde ese artifact (`TYPE_PROCESS_DATABANK`).
- **Apply:** APPLY_INPUT_ARTIFACT = el mismo Optimizer `OUTPUT/STRATEGY_SQX`. `EchoForgeRobustRunExporter` exige `WalkForwardMatrixResult` en `mainResult` y aplica parámetros al XML del mismo ResultsGroup. No usa el sidecar.
- **WF Matrix ownership:** OPTIMIZER_ARTIFACT; DURABLE_REQUIRED=YES (es el unique producer output; WFM y Apply lo consumen). El sidecar es TRANSIENT. No DurableArtifactRef propio, no StageProducerOutput propio, no Evidence extra, no recovery propio; recreable por SQX y no necesario tras WFM Evidence.
- **FinalReretester / Retester:** MULTI_LOCAL_OUTPUT=PROVEN_NO a nivel CFX (`WalkForwardMatrix use="false"` / `WalkForwardOptimization use="false"`). IN_FIX_SCOPE=NO. No ampliar.
- **Cohort 25 vs 26:** NO es causalidad. El mismo `optimizer_test.cfx` (`Optimization type=3` Walk-Forward + `DontSaveOriginalStr=false`) aplica a todos los Optimizer del golden. 0.2.80 no tenía F8; el filtro ocultaba el sidecar. Cleanup post-upload borra raw local; «flow 25 no emitió el segundo archivo» queda **no demostrado**.
- **LAN residual:** unzip byte-level de los `.sqx` de Zeus no se ejecutó (errno 65 a `192.168.31.0/24` desde esta sesión). Clasificación cerrada por CFX + filtro + Java consumers + tests de identidad + SHAs de la certificación previa (par 4.1.24). Si un unzip futuro mostrara que el archivo pequeño contiene el `WalkForwardMatrixResult` y el grande no, reabrir; la evidencia actual apunta al inverso.

## Rationale

- `collect_results` hace `Glob(output, "*.sqx")` sin filtro. F8 (`steps.go` upload_results) falla si `len(ResultFiles)>1` para cualquier singleton (Retester/Optimizer/FinalReretester) **antes** de `UploadPrefixFilter`. El upload (`minio_storage.go`) con `ExactOutputName==""` y `UploadPrefixFilter=WF_Matrix` hace `continue` si el filename no tiene prefijo `WF Matrix` / `WF_Matrix`. Optimizer **no** setea `ExactOutputName` (solo FinalReretester). Por tanto el contrato histórico publishable era 0|1 **después** del filtro.
- CFX Optimizer (`input/example/optimizer_test.cfx` SHA256 `121ec05ebb1b4ca0be1d3e427de6ca2c0f6ec272c7ec336447ecae6315c1ffed`, task único activo Optimize): `WalkForward type=0` + Rankings `<DontSaveOriginalStr>false</DontSaveOriginalStr>`. SQX está configurado para persistir original **y** WF Matrix en databank `output`.
- Downstream durable ya asume el artifact Optimizer = databank WF: WFM physical descarga exactamente 1 `DurableArtifactRef`; RobustRunExporter falla sin `WalkForwardMatrixResult`; Apply SPEC dice no leer una WFM matrix **ndjson** (eso es evaluate_wfm), no niega el databank `.sqx`.
- Identity v2 no se reabre: un StrategyRef, dos archivos físicos con roles distinctos (publishable vs sidecar). El prefix `WF_Matrix` se strippea del CanonicalStrategyID; no es identidad.

## Consecuencias

- NEXT EXACT: `DURABLE-OPTIMIZER-OUTPUT-CARDINALITY-CORRECTION-NORMAL`. Fix mínimo: clasificar publishable (filtro canónico ya existente) **antes** de F8; F8/db_register/producer cuentan 0|1 publishable; >1 publishable sigue `CONTRACT_CONFLICT`; 0 publishable = CompleteEmpty. No schema. No migration. No producer contract bump. Budget esperado 6–8 archivos (`steps.go` + tests Optimizer/F8, helper de filtro en storage o capabilities, tests de upload filter+cardinality). Hard concern >14 no aplica.
- Tests obligatorios: raw `{optimized.sqx, WF Matrix - x.sqx}` → 1 publishable, 1 producer row, 1 Evaluation artifact; WFM/Apply consumen esa authority; retry after producer record; completed recovery; different-host ObjectKey; zero output; truly multiple publishable → CONTRACT_CONFLICT. FinalReretester/Retester fuera de scope.
- Recertificación: NEW RELEASE + NEW RequestID/FlowRun/Workflow/RunID/Wave. Part A F0–F7 y F9–F16 citables si `origin/master` no cambia recovery mechanics. F8 **no** se cita as-is (mide raw). Targeted rerun: F8 reescrito + golden físico completo. NEW_FULL_GOLDEN=YES.
- Recovery: SINGLETON_STILL_VALID=YES. Precedencia Results > Evaluation > ProducerOutput > Physical intacta. Record-before-put sigue sobre el unique publishable.

## Alternativas descartadas

- **B (two-artifact Evaluation):** ambos archivos no son business outputs durables. El sidecar no tiene consumidor WFM/Apply. Schema innecesario.
- **C como primaria:** cambiar CFX puede dejar raw=1, pero no corrige el gate si SQX u leftovers vuelven a emitir N; el filtro publishable sigue siendo la capa contractual. Permitida como higiene posterior.
- **D (WF Matrix owned by WFM):** el databank es output del Optimizer y input de WFM, no un producer WFM. Mover ownership rompería Optimizer Evaluation y Apply source `OUTPUT/STRATEGY_SQX`.
- **Eliminar el `.sqx` WF Matrix:** invertiría el contrato histórico y rompería WFM/Apply (`WalkForwardMatrixResult` missing).
- **Seleccionar el sidecar como logical output:** contradice filtro, tests de identidad, keys WFM y Java.

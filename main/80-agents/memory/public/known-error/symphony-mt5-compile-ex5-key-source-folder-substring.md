---
type: known_error
schema_version: 1
scope: application
created: "2026-08-23"
updated: "2026-08-23"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[Symphony]]"
entities:
  - "[[Symphony]]"
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[symphony-mt5-compile-ex5-absent]]"
aliases:
  - derive ex5 key source_folder
  - 07_mt5_mq5 substring
  - durable mq5 ex5 key
confidence: verified
source_session: "FINAL-DURABLE-E2E-DEPLOY-RERUN-NORMAL-ATTEMPT-15"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
  - area/echo
  - tech/mt5
  - project/echo-forge
---

# symphony-mt5-compile-ex5-key-source-folder-substring

## Síntoma

- `mt5_compile_artifact` falla cerrado con `derive ex5 key: source_folder "07_mt5_mq5" no aparece en "<durable-mq5-object-key>"`.
- Los child workflows de compile reciben carriers exactos `durable/mt5-export/v1/<flow_run_ref>/<strategy_ref>/…/final-<StrategyRef>.mq5` y `list_mt5_artifacts` = 0.

## Causa

- La derivación del ObjectKey EX5 reescribe o valida el key MQ5 exigiendo que el token brownfield `source_folder` (`07_mt5_mq5`) sea substring del ObjectKey fuente.
- Las keys durable de MT5 Export no contienen ese token; membership exacta y key EX5 son contratos distintos.

## Impacto

- Compile children FAILED 6/6 en Attempt 15 (release `0.2.65`, FlowRunRef `b4776ba2-…`). Cero EX5, cero backtest, cero scores, cero GLOBAL ranking. El parent Temporal puede quedar `COMPLETED`.

## Detección

- Temporal: `list_mt5_artifacts` SCHEDULED = 0 y todos los `MT5CompileArtifactWorkflow` FAILED con el mismo mensaje `source_folder "07_mt5_mq5" no aparece`.
- El ObjectKey fuente empieza por `durable/mt5-export/v1/`.

## Mitigación

- No reabrir el cutover de membership (`current.Keys` + `current.StrategyArtifacts`).
- Próxima sesión: derivar EX5 ArtifactRef desde la MQ5 current key durable / StrategyArtifact y el folder destino configurado, sin exigir el substring `07_mt5_mq5`.
- No tratar leftovers del prefijo compartido `07_mt5_mq5` como autoridad.

## Evidencia

- Attempt 15: `specs/FEAT-SQX-DURABLE-PIPELINE-CLOSURE/FINAL-E2E.md`
- WorkflowID `sqx-main-v1-0ca61c57-0d2f-45bd-848c-6beb803590a9`
- Error canónico: `…/final-b144deb9-e94f-4edd-b9df-f24dff3da674.mq5`

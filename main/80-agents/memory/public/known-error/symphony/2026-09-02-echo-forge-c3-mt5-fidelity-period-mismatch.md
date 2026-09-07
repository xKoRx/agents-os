---
type: known_error
schema_version: 1
scope: project
created: "2026-09-02"
updated: "2026-09-02"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities: []
related:
  - "[[2026-09-02-echo-forge-c3-adaptive-workflow-registration]]"
  - "[[2026-09-02-echo-forge-c3-cert-a-supply-via-aligned-mt5-window]]"
  - "[[2026-08-31-forge-campaign-stop-policy-v1-contract]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-C3-PHYSICAL-BLOCKERS-RCA-TOP
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
  - project/echo-forge
---

# Echo Forge C3 mt5-final-fidelity SCORE_NOT_COMPARABLE by period mismatch

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- `FINALIST_PROMOTION` COMPLETED con `finalists=[]` y reason `TOP_PROJECTION_EMPTY` sobre ranking `mt5-final-fidelity-ranking`.
- RankingSnapshot GLOBAL con `effective_top_n=0`; todos los candidatos `eligible=false` y `exclusion_reason=SCORE_NOT_COMPARABLE`.

## Causa

- `mt5_fidelity_shadow.v1` exige igualdad de `period_start_utc` y `period_end_utc` entre baseline SQX CFX y candidate MT5.
- El JSON de tester usa `mt5.from=2026.07.01` / `mt5.to=2026.07.31`; el TradeSet SQX usa `configured_from=2016-01-04` / `configured_to=2026-06-05` (`sqx_cfx_setup.v1`).
- Ventanas disjuntas: SQX termina `2026-06-05`; MT5 empieza `2026-07-01`.
- Ranking y Promotion proyectan vacío de forma correcta. No es un fallo de Promotion.

## Impacto

- CERT-A no puede demostrar `finalists >= 1` con la config de qualification ni con el `input/example/config.json` actual.
- Census físico: 2/2 FINALIST_PROMOTION vacías; 11/11 snapshots `mt5-final-fidelity-ranking` con `effective_top_n=0`.

## Detección

- RCA READ ONLY sobre FlowRun `9bc03705-7f96-4f7f-a676-5facae5fb437` y golden `c7eb6b3b-95ec-4088-aba5-2d5db6906e4c`.
- Scores con reasons `period_start_utc_mismatch` y `period_end_utc_mismatch`; resto de predicates de fidelity PASS.

## Mitigación

- No bajar comparability, no rebind promotion a `builder-early-per-type`, no insertar Decision.
- Alinear `tasks[mt5_backtesting named mt5-final].mt5.from/to` a `2016.01.04` / `2026.06.05` y reintentar CERT-A tras el fix de registro Adaptive.
- Residual: Darwinex-Demo debe tener historia XAUUSD H1 desde `2016-01-04`.
- Resolución source aplicada en `48997d773e91dec9b8fe57fbd1650e8d8beb8b57`: `input/example/config.json` alinea exactamente la ventana y agrega `promotion` con `finalist_promotion@1.0.0` enlazado a `mt5-final-fidelity-ranking`.
- Este cambio sólo hace la configuración compatible; finalists nonempty sigue sin estar probado físicamente y no se reabre el RCA.

## Evidencia

- DecisionRef `sha256:12a48f18f4ab9545b7f385f504a5f54a747b68c7fb2b09c20335ae9eb06c7b78`.
- RankingSnapshotRef `sha256:a5921bb156449fea5c73b9c938ddd55eec42c08418fe8306b124400f43c151f4`.
- RCA: `specs/FEAT-SQX-DURABLE-RANKING-SNAPSHOT/rca/RCA-C3-B2-nonempty-promotion-supply.md`.
- Runtime/config regression: JSON válido, `ValidateWorkflowSpec` PASS y ranking fuente resuelve exactamente una vez.

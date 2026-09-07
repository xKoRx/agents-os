---
type: decision
schema_version: 1
scope: application
created: "2026-08-23"
updated: "2026-08-23"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-08-23-cursor-grok-4-6-durable-strategy-identity-v2-storage-support-normal]]"
aliases:
  - durable strategy identity v2 storage
  - identity_model_version 2
confidence: verified
source_session: DURABLE-STRATEGY-IDENTITY-V2-STORAGE-SUPPORT-NORMAL
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/application
  - app/echo-forge
  - tech/symphony
---

# Decision — Durable Strategy identity v2 storage support

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- v1 identifica Strategy por `(config_id, canonical_strategy_id)`. Eso es incorrecto: `config_id` es el Config bajo el cual se trabaja una Strategy, no su identidad de negocio.
- Una Strategy nace una vez en Builder y se reutiliza en otros FlowRuns/configs sin dejar de ser la misma.
- Esta sesión prepara el contrato de storage. El cutover de `AdoptStrategy()` queda para la sesión siguiente.

## Decisión

1. `identity_model_version = 2` existe en schema y writer. `AdoptStrategy()` llamaba a `upsertStrategyV1()` hasta el cutover; SUPERSEDED por [[2026-08-23-durable-strategy-identity-v2-cutover]].
2. Identidad de negocio v2: `canonical_strategy_id`. Unique conceptual: `UNIQUE(canonical_strategy_id) WHERE identity_model_version = 2`.
3. `config_id` se conserva como provenance/origin del Config de la primera adopción. No participa en la business identity v2. No se reemplaza si la misma Strategy se reutiliza desde otro config.
4. Atributos inmutables de conflicto: `instrument`, `direction`, `timeframe`, `strategy`, `version`. Divergencia → `ErrContractConflict`. Cero UPDATE silencioso.
5. Cero backfill. Cero modificación de filas v0/v1. Cero StrategyRef histórica modificada.
6. Hipótesis G2B basadas en `HOST_KEY=zeus/hera/kronos` quedan SUPERSEDED.
7. No existe autorización para semantic identity, equivalence model, stripping de `z0/h0/k0`, ni rediseño de `CanonicalStrategyID()`.

## Rationale

- El invariant real de Echo Forge es que Strategies nacen una vez y `StrategyRef`/`CanonicalStrategyID` sobreviven Builder → Retester → Optimizer → WFM → Robust → Apply → Final Reretester → TradeList → MT5 → Score → Ranking.
- `config_id` sigue siendo válido y reutilizable en `sqx.configs`; sólo deja de ser parte de la llave de negocio v2.
- La relación posterior sigue siendo FlowRun → FlowRunStrategy → Strategy.

## Consecuencias

- Migración 006 amplía CHECK a `(0,1,2)` y crea partial unique v2. DOWN elimina el índice v2 y restaura CHECK 0,1 sólo si no hay filas v2; si hay filas v2, falla cerrado.
- `runner.go` registra 006 para que `Apply()` local/test la ejecute. Esta sesión no aplica la migración en producción.
- Cutover ejecutado en DURABLE-STRATEGY-IDENTITY-V2-CUTOVER-NORMAL: ver [[2026-08-23-durable-strategy-identity-v2-cutover]].

## Alternativas descartadas

- Eliminar `config_id` de `sqx.strategies` o modificar `SaveConfig()` / fórmula de cfgID.
- Activar el writer v2 en el mismo cambio que el schema.
- Semantic digest / StrategyDefinition / StrategyVariant / generation identity nueva.

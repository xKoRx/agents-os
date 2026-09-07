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
  - "[[2026-08-23-durable-strategy-identity-v2-storage-support]]"
  - "[[embedded-postgres-maven-dns-timeout]]"
aliases:
  - durable strategy identity v2 cutover
  - AdoptStrategy upsertStrategyV2
confidence: verified
source_session: DURABLE-STRATEGY-IDENTITY-V2-CUTOVER-NORMAL
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/application
  - app/echo-forge
  - tech/symphony
---

# Decision — Durable Strategy identity v2 cutover

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Echo Forge todavía no está en producción. No existe obligación de compatibilidad productiva con Strategy identity v1, ni migration v1→v2, ni backfill, ni rollback histórico.
- Storage v2 ya existía (`upsertStrategyV2`, unique parcial `canonical_strategy_id WHERE identity_model_version = 2`, migration 006). `AdoptStrategy()` seguía escribiendo v1.
- Strategy nace una sola vez en Builder. Downstream (Retester → Optimizer → WFM → Robust → Apply → Final Reretester → TradeList → MT5 → Score → Ranking) trabaja siempre la misma Strategy.

## Decisión

1. `AdoptStrategy()` llama a `upsertStrategyV2()`. No hay dual v1/v2, feature flag, ni fallback a v1.
2. Identidad de negocio v2: `canonical_strategy_id`. Unique: `UNIQUE(canonical_strategy_id) WHERE identity_model_version = 2`.
3. `config_id` se conserva como provenance/origen de la primera adopción. No participa en identity v2. Reuse con otro config no recrea la fila ni cambia el `config_id` original.
4. `REPROCESSED` representa reuse de la misma Strategy en otro FlowRun, no una Strategy nueva. El primer FlowRun es `PRODUCED`/origin.
5. Conflicto de atributos inmutables (`instrument`, `direction`, `timeframe`, `strategy`, `version`) → `ErrContractConflict` sin mutación silenciosa.
6. No se toca `CanonicalStrategyID()`, `HOST_KEY`, Builder naming, ni tokens `.z0/.h0/.k0`.
7. Esta decisión SUPERSEDE el punto 1 de [[2026-08-23-durable-strategy-identity-v2-storage-support]] (`AdoptStrategy()` ya no llama a `upsertStrategyV1()`).

## Rationale

- Antes del lanzamiento inicial, v2 es el contrato vigente. Diseñar coexistencia operacional v1/v2 o migration histórica sería sobreingeniería: no hay StrategyRef productivas v1 que preservar.
- Misma Strategy + otro config o FlowRun debe devolver el mismo `StrategyRef`. Eso es el caso central del invariante de dominio.

## Consecuencias

- Escrituras nuevas de `AdoptStrategy()` quedan con `identity_model_version = 2`. Cero filas v1 nuevas por este camino.
- Tests de control plane que observaban model=1 vía `AdoptStrategy()` se actualizaron a model=2. `upsertStrategyV1()` permanece para coexistencia de storage y tests directos.
- Cutover en `7c0b2892a507975dfbdced085c37a4bafbb9e858` (`HEAD == origin/master`). No hay deploy ni aplicación de migration 006 en producción en esta sesión.
- Certificación Postgres del cutover quedó DEGRADED: embedded-postgres no resuelve Maven Central. Ver [[embedded-postgres-maven-dns-timeout]].

## Alternativas descartadas

- Mecanismo dual v1/v2, feature flag, o lookup previo de fila v1.
- Migration 007 / backfill / rollback histórico.
- Instalar Postgres/Docker local como proyecto paralelo de infraestructura para desbloquear Maven.

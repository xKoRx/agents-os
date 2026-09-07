---
type: decision
schema_version: 1
scope: application
created: "2026-08-19"
updated: "2026-08-19"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-08-15-echo-forge-g0l-owner-amendments]]"
  - "[[2026-08-16-echo-forge-g0p-mvp-physical-design]]"
  - "[[2026-08-19-echo-forge-a6-strategy-flowrunstrategy]]"
aliases:
  - Echo Forge A6 Big Bang
  - A5 SUPERSEDED
confidence: verified
source_session: owner-amendment-2026-08-19
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/application
  - app/echo-forge
  - application/echoforge
  - area/echo
  - project/echo-forge
  - tech/symphony
---

# Decision — Echo Forge A6 Big Bang supersede A5 incremental

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- A5 era un plan de migración incremental con dual-write/backfill implícito.
- No hay PROD relevante que preservar; el leftover de test puede borrarse salvo fixtures/golden.
- El modelo lógico G0-L y el diseño físico G0-P siguen vigentes; cambia el *cómo* se corta el legacy.

## Decisión

1. A5 incremental queda **SUPERSEDED**. No reutilizar el id A5 con otro significado.
2. Fase activa: **A6 — Durable Pipeline Big-Bang Migration**.
3. Binding: BIG BANG, NO BACKFILL, NO DUAL WRITE, NO compatibilidad legacy innecesaria, NO framework de migración histórica.
4. No reabrir M6 (parser/normalization/canonical symbol/timeframe/comparability/Score algorithm). No avanzar M7.
5. RankingSnapshot físico de entries sigue abierto hasta evidencia de access/cardinalidad.

## Rationale

- Dual-write y backfill protegen un PROD que no existe y alargan dos modelos en paralelo.
- El contrato durable ya está diseñado; el trabajo es adoptar writers y cortar readers legacy.

## Consecuencias

- Planner canónico: [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]].
- Identidad Strategy v1 exige origin + participation en la misma transacción.
- Folders son routing físico, no identidad.
- G0-L/G0-P no se reabren salvo contradicción real en código.

## Alternativas descartadas

- Seguir A5 incremental o dual-write “por seguridad”.
- Inventar otro persistence framework o entidades (`pipeline_run`, `stage_run`, `StructuralSignature`).
- Reabrir M6 o desbloquear M7 como parte de A6.

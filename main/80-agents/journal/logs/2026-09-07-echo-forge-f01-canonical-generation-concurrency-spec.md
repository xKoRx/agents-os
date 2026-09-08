---
type: change_log
schema_version: 1
scope: session
created: "2026-09-07"
updated: "2026-09-07"
area: "[[Echo]]"
project: "[[Echo Forge — Factory V2 Completion]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge — F-01 Canonical generation concurrency]]"
related:
  - "[[Echo Forge — F-01 Canonical Generation Concurrency Contract]]"
  - "[[2026-09-04-echo-forge-campaign-builder-supply-identity]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-F01-CANONICAL-GENERATION-CONCURRENCY-TOP
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/echo
  - project/echo-forge
---

# 2026-09-07-echo-forge-f01-canonical-generation-concurrency-spec

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `30-resources/applications/Echo Forge — F-01 Canonical Generation Concurrency Contract.md` (created) — SPEC técnica F-01.
  - `10-projects/Echo/agentes/Echo Forge — F-01 Canonical generation concurrency.md` (created) — subproyecto de implementación hijo de Factory V2, con TASKS T1.1–T1.4.
  - `10-projects/Echo/agentes/Echo Forge — Factory V2 Completion.md` (updated) — enlace mínimo al hijo y a la SPEC.
  - `30-resources/applications/00-index.md` (updated) — fila de catálogo de arquitectura.
  - `30-resources/applications/log.md` (updated) — ingest de la SPEC.

## Motivo

- TOP F-01 debía persistir contrato, plan de ejecución y TASKS atómicas en Agents OS antes de cualquier NORMAL.

## Fuentes usadas

- `xKoRx/symphony@db8a022703082fd7ee9d1e15243c5d1b2feaf578`
- Agents OS `83506a14f0b850402fbb61d50e90790662fe19f0`
- [[2026-09-04-echo-forge-campaign-builder-supply-identity]]
- [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]
- `80-agents/skills/agents-os-implementation-planning/SKILL.md`

## Resolución aplicada

- Discriminador durable intra-wave: `OutputNamespaceOwnership` (FlowRun). Identity GENERATED: `CanonicalStrategyID(published basename)` con `BuilderSupplyBatchRef` en Campaign. HOST_KEY fuera de identity/publication GENERATED. Migration none.

## Validación

- `python3 80-agents/skills/agents-os-implementation-planning/scripts/validate_plan.py` sobre el subproyecto.
- `python3 scripts/lint.py --strict` sobre notas nuevas/modificadas.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos, sin paths de máquina, sin memoria interna

## Rollback

- Borrar las dos notas nuevas y revertir los tres updates de enlace si el manager rechaza el diseño.

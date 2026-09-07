---
type: change_log
schema_version: 1
scope: session
created: "2026-08-27"
updated: "2026-08-27"
area:
project: "[[Echo Forge]]"
application:
entities: []
related: []
aliases: []
confidence: verified
source_session: SQX-CROSS-FLOWRUN-BUILDER-TEMPLATES-CORRECTION-NORMAL
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# SQX Cross-FlowRun Builder templates correction

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `xKoRx/symphony`: 13 feature files, commit `7d2199a55a844a1bf83c04c27a9fe9ebc0754587`
  - `specs/FEAT-SQX-CROSS-FLOWRUN-REUSE/SPEC.md`
  - `specs/FEAT-SQX-CROSS-FLOWRUN-REUSE/TOP-DECISIONS.md`

## Motivo

- Se implementó FD-9 para historical Builder templates y se consolidaron los amendments A1–A3: cohort como provenance, inputs `template:<StrategyRef>`, validación CFX fail-closed, y rechazo de colisión canonical template/output.

## Fuentes usadas

  - [[sqx-historical-builder-templates-fd9]]
  - [[Echo Forge]]

## Resolución aplicada

- Se extrajo un resolver histórico read-only compartido; downstream conserva same-flow noop y cross-flow `REPROCESSED`. Builder registra `REUSED`, evita `ListStrategies`, usa bindings exactos y mantiene subject `FLOW`.

## Validación

- Feature tests y bloques worker/overview/core/metadata-mongo pasan; `git diff --check` pasa; push verificado con `HEAD == origin/master`. Workflow broad mantiene fallos conocidos de fixtures `flow_run_start`; registry mantiene únicamente `TestUpsertStrategyV2_V0V1V2Coexistence` aceptado.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Rollback lógico: revertir el commit feature en `master`; no se ejecutaron migraciones ni cambios destructivos. El workspace foreign dirty quedó preservado.

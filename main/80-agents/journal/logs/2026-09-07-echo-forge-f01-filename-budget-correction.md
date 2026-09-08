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
source_session: ECHO-FORGE-F01-TOP-CORRECTION-02
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

# 2026-09-07-echo-forge-f01-filename-budget-correction

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `30-resources/applications/Echo Forge — F-01 Canonical Generation Concurrency Contract.md` (updated in-place) — fórmula filename compacta.
  - `10-projects/Echo/agentes/Echo Forge — F-01 Canonical generation concurrency.md` (updated in-place) — T1.1/T1.2/T1.4.
  - `10-projects/Echo/agentes/Echo Forge — Factory V2 Completion.md` (updated) — bitácora.
  - `30-resources/applications/log.md` (updated) — ingest.

## Motivo

- `p`+64 hex (65) + Campaign `FilenameToken` (~45) no cabe en el máximo 128 de `sanitizeFileName`. Truncar el digest está prohibido.

## Fuentes usadas

- `xKoRx/symphony@db8a022703082fd7ee9d1e15243c5d1b2feaf578` `sanitizeFileName` máximo 128
- `BuilderSupplyBatchRef.FilenameToken()` ≈ 45 chars
- SPEC F-01 corregida (ExecutionIntentKey aceptado)

## Resolución aplicada

- Published GENERATED nuevo = `Base64URLNoPad(EIK.digest) + "_" + Base64URLNoPad(SHA256(canonical local stem)) + ".sqx"` (91 chars). Campaign `FilenameToken` no se proyecta en nombres nuevos; fórmula `BuilderSupplyBatchRef` intacta. `DATABASE MIGRATION: NONE`.

## Validación

- `python3 80-agents/skills/agents-os-implementation-planning/scripts/validate_plan.py` sobre el subproyecto.
- `python3 80-agents/skills/agents-os-entity-lifecycle/scripts/lint.py --strict` sobre notas canónicas tocadas.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos, sin paths de máquina, sin memoria interna

## Rollback

- Revertir este commit si el manager exige Campaign token en el filename nuevo.

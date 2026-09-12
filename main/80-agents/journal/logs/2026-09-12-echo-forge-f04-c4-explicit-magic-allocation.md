---
type: change_log
schema_version: 1
scope: session
created: "2026-09-12"
updated: "2026-09-12"
area: "[[Echo]]"
project: "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
  - "[[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]]"
related:
  - "[[Echo Forge — Factory V2 Completion]]"
  - "[[Echo Forge — F-01 Canonical Generation Concurrency Contract]]"
  - "[[Echo — E-04 Forge Ingestion E1]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-09-12-f04-c4-contract-session-feedback]]"
share_scope: team
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-12-echo-forge-f04-c4-explicit-magic-allocation

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo Forge — F-04 Magic allocation, version seal and handoff.md`
  - `30-resources/applications/Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract.md`
  - `10-projects/Echo/agentes/Echo Forge — Factory V2 Completion.md`
  - `30-resources/applications/00-index.md`
  - `30-resources/applications/log.md`

## Motivo

- PHYSICAL `0.2.97` falló en `ParseMagicV1AllocationIdentity` porque Magic V1 extraía instrument/direction desde `CanonicalStrategyID`. F-01 deja ese ID opaco. C4 congela autoridades explícitas ya persistidas en `sqx.strategies` y corrige D9 (TaskSpec `magic_number` no es requested).

## Fuentes usadas

- Symphony `d645ed6c2f438995d636a8213b1e4a3f5f26cbea`; F-01 `0509342439cfbaa048839088787458dde1ed1b05`; Magic V1 `ea8be76c4587b2d00e4cad8cf2a67c4fd8e6680f`.
- `sqx/core/domain/magic_v1.go`, `sqx/adapters/registry-postgres/magic_v1.go`, `magic_allocation.go`, migrations 015/016, `adopt_strategy.go`, `durable_apply_selected_run.go`, `apply-selected-run/binding/contract.go`, `canonical_strategy_id.go`.

## Resolución aplicada

- D17 frozen: instrument=`sqx.strategies.instrument`; direction=`sqx.strategies.direction`; mapper `MagicV1DirectionFromStrategy`; replay conflict via `DecodeMagicV1`; `DATABASE MIGRATION: NONE`. D9 corrected. Multi-strategy soportado. T2.13 E-04 es one-shot separado. Tareas C4.1–C4.6 para NORMAL.

## Validación

- Source dirigido verificado; 015 no tiene columnas instrument/direction y no las necesita; 016 catálogo+counter suficientes. Sin implementación Symphony/Echo. Sin deploy/physical/merge.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales de máquina, memoria interna ni secretos

## Rollback

- Revertir las actualizaciones documentales de Agents OS; no hay cambios de código Symphony/Echo que revertir.

---
type: change_log
schema_version: 1
scope: session
created: "2026-09-10"
updated: "2026-09-10"
area: "[[Echo]]"
project: "[[Echo Forge — Factory V2 Completion]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
related:
  - "[[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]]"
  - "[[Echo — E-01 Canonical SDK Foundation S0]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-F04-MAGIC-SEAL-HANDOFF-TOP
source_feedbacks:
  - "[[2026-09-10-echo-forge-f04-magic-seal-handoff-session-feedback]]"
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

# 2026-09-10-echo-forge-f04-magic-seal-handoff-spec

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/slugs son solo automatización. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `30-resources/applications/Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract.md` (created)
  - `10-projects/Echo/agentes/Echo Forge — F-04 Magic allocation, version seal and handoff.md` (created)
  - `10-projects/Echo/agentes/Echo Forge — Factory V2 Completion.md` (updated)
  - `30-resources/applications/00-index.md` (updated)
  - `30-resources/applications/log.md` (updated)

## Motivo

- TOP F-04 debía persistir contrato, plan y TASKS atómicas en Agents OS antes de cualquier NORMAL. No modificar symphony/echo/SDK.

## Fuentes usadas

- `xKoRx/symphony@382f4ba5d417371f778e21619ed9eb72624a23f4` CLEAN
- S0 `xKoRx/echo@91671f6f46ffa889a79aed0979cb3b4e5821ed33` (impl `08a0eb9a`)
- Agents OS vault sin `.git`; última SHA durable `f1070bec27db3ca415fe24f3c3576139674b7e09`
- Live Authority §3; SDK §§9–13; F-01/F-02/F-03 contracts

## Resolución aplicada

- Allocation before Apply; Finalist admite seal/handoff. 1:1 StrategyRef↔magic. CC_MISSING_OWNER_GATE. Migration 015. Readback XML+MQ5 fail-closed. S0 recipes only on seal/handoff. Adapter+fakeconsumer; no endpoint E-04 inventado. NORMAL no autorizado.

## Validación

- Symphony HEAD=`origin/master`=`382f4ba`; worktree CLEAN.
- S0 pin `git cat-file` + `git show` de identity/promotion/evidence/hash/fakeconsumer/corpus.
- Lint dirigido pendiente en el mismo cambio.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos ni paths de máquina en el contrato (VAULT_ROOT relativo)

## Rollback

- Archivar/eliminar las dos notas F-04 y revertir deltas del padre/índice/log.

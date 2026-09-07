---
type: change_log
schema_version: 1
scope: session
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Personal]]"
project: "[[Echo Forge]]"
application:
entities:
  - "[[Echo Forge]]"
related:
  - "[[AGENTS OS]]"
aliases: []
confidence: verified
source_session: "ECHO-FORGE-RELEASE-0.2.94-AND-FINALIST-FACTORY-V1-PHYSICAL-RECERT-NORMAL"
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Echo Forge release 0.2.94 physical recertification cost safety

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated / conflict-resolution
- **Archivo(s):**
  - Release 0.2.94 and deployed fleet
  - One physical Campaign and its Wave 1/Wave 2 evidence

## Motivo

- Release 0.2.94 was published from exact source. Physical recertification stopped when Wave 2 materialized 5 MT5 backtest children under one Generic despite the hard budget of 4.

## Fuentes usadas

- Source `9ef5549da3308b286ecff52f2d825af8024c27fe`, SDK `c85594440f6755443ceb97ec4e333cd0ddb5b0ed`, PostgreSQL/Temporal read-only evidence, fleet checks and canonical release logs.

## Resolución aplicada

- Proved V2 intake → request v2 + StopPolicy v1 + ReplenishmentPolicy v1; Wave 1 `CONTINUE`; Wave 2 fresh `g000002` supply with zero produced StrategyRef intersection. Issued one authorized CancelWorkflow for the exact Generic and waited for `running=0`.

## Validación

- No source patch, stage, commit, push, migration write, manual DB/MinIO write or TerminateWorkflow. Final Campaign is `FAILED / WAVE_FLOW_RUN_CANCELLED`; this is not a certification PASS.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- No rollback; cancellation was the required safety containment. Future recertification requires cap enforcement/certification before another Campaign.

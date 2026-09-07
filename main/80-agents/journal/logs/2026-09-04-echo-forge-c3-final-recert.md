---
type: change_log
schema_version: 1
scope: session
created: "2026-09-04"
updated: "2026-09-04"
area:
project:
application:
entities: []
related: []
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-04-echo-forge-c3-final-recert

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated / conflict-resolution
- **Archivo(s):** release remoto `0.2.92`; evidencia operativa de una Campaign física; checkpoint canónico de Echo Forge.

## Motivo

- Cerrar la recertificación física final de C3 sobre source exacto `93c66651251edefcc65ef183ac9f7b832b4de5de` y SDK `c85594440f6755443ceb97ec4e333cd0ddb5b0ed`.

## Fuentes usadas

- Gate 0/1/2/3/4/5, watcher logs, PostgreSQL durable state, Temporal histories, `LoadForgeCampaignResult`, result-surface equivalente, hashes de artefactos y replay detached exacto.

## Resolución aplicada

- Publicada `0.2.92` con manifest SHA `8e03857f8d87bbfc4465b10f811b8431eaccf7e8143e60d6adfd0da8442ba800`, Symphony `e21e73f95a933348baddeaa4391dba122ea4ea3c7109810bb1731e29cb22f236`, Windows worker `8d58323f591e50828c967143ce1345a0f2992fbf7cd36527238d57265fd4ebdb`; fleet convergió 4/4.
- Ejecutada exactamente una Campaign nueva, Branch A, `TARGET_REACHED`, un wave, un FlowRun `COMPLETED`, Promotion durable y exact redelivery sin materialización adicional.

## Validación

- Final Reretester produjo 3 outputs; TradeList/MQ5/Compile/MT5/Reconcile/Score ejecutaron sólo para ese cohort; 3 compile y 3 backtest físicos, build `6140`, reconcile PASS; ranking disponible con top 1 y Promotion disponible con finalist 1.
- Replay: Campaign histórica contaminada, Campaign nueva, Generic child y un MT5Backtest child: `nondeterminism=NONE`; topología padre→Generic directa única y Generic→3 compile+3 backtest.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- No se ejecutó rollback ni mutation destructiva; dirty foráneo se preservó, históricos quedaron inmutables y no hubo stage/commit/push/config committed.

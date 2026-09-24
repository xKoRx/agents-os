---
type: change_log
schema_version: 1
scope: session
created: "2026-09-24"
updated: "2026-09-24"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application:
entities:
  - "[[Echo Futures]]"
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

# 2026-09-24 — Echo Futures withdrawal KPI correction

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Futures/Echo Futures.md`

## Motivo

- Corregir una sobrelectura del fixture matemático q=10% y fijar como KPI primario la conversión desde evaluation comprada hasta primer retiro real.

## Fuentes usadas

- Aclaración explícita del owner.
- D4 simulator fixtures T5/T6.

## Resolución aplicada

- `q_withdraw = P(evaluation comprada → primer retiro real)` pasa a ser la métrica primaria. Pass/funded quedan como estados intermedios. Los escenarios q≈0.10 de D4 quedan etiquetados como fixtures de validación, no evidencia de una prop real.

## Validación

- Proyecto principal actualizado; D5 reformulado alrededor de retiro real.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- No aplica salvo cambio explícito del KPI económico por parte del owner.

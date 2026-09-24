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

# 2026-09-24 — Echo Futures martingale recovery invariant

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Futures/Echo Futures.md`

## Motivo

- Resolver matemáticamente si un add con size mayor crea una nueva probabilidad 50/50 bajo un mercado aleatorio y convertir el resultado en invariant/test del simulador.

## Fuentes usadas

- Ejemplo explícito planteado por el owner.
- First-passage probability de random walk/Brownian sin drift y propiedad de martingala.

## Resolución aplicada

- Confirmado que después del add existe una nueva probabilidad condicional, pero no una nueva moneda 50/50. Si el terminal PnL sigue fijo en +G/-L, sizing dinámico predictivo no cambia la probabilidad total: P(win)=L/(G+L). Se documenta el caso +100/-100 con add en -30 y se convierte en acceptance test.

## Validación

- Cálculo exacto del ejemplo: P(win antes de add)=30/130; P(reach add)=100/130; tras add 1+1 con average -15, TP +35 y SL -65, P(win|add)=35/100; total=0.5.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir sólo si el modelo operativo deja de conservar outcomes monetarios terminales fijos o se redefine el null model.

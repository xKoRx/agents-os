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

# 2026-09-24 — Echo Futures simulation-first pivot

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Futures/Echo Futures.md`

## Motivo

- Reordenar D3 para validar primero la tesis mediante simulación estocástica completa sin datos históricos, manteniendo backtest como etapa posterior de calibración/falsificación.

## Fuentes usadas

- Decisión explícita del owner.
- Reglas oficiales vigentes de Topstep, Lucid Trading y Apex consultadas el 2026-09-24.

## Resolución aplicada

- Definidos L0 Bernoulli ladder, L1 random-walk null model y L2 synthetic strategy edge; hardscalping, prop lifecycle y cohort correlation pasan al núcleo del simulador. Se declara que adds y cuentas copiadas no son independientes por defecto.

## Validación

- Proyecto persistido en master; no se autoriza todavía compra de cohorte real. Backtest histórico queda deferred, no cancelado.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir el commit si evidencia posterior muestra que el simulador sintético no puede representar suficientemente la tesis económica.

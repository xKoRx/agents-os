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

# 2026-09-24 — Echo Futures D3 abstract model

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Futures/Echo Futures.md`

## Motivo

- Congelar los principios abstractos de Echo Futures y separar economía de prop, señal, gestión intra-trade, riesgo inter-trade y validación de ejecución.

## Fuentes usadas

- D2 synthesis de los tres DR.
- Decisión del owner de mantener los principios abstractos y reemplazables.
- Documentación oficial vigente de Databento y NinjaTrader consultada el 2026-09-24.

## Resolución aplicada

- Modelo conceptual modular; Prop Economics Simulator separado del Market Strategy Backtester; política 1m para screening, 1s/tick para finalists y NinjaTrader para verificación. Databento histórico CME seleccionado como candidato preferido para el sprint.

## Validación

- Proyecto persistido en master; D3 sigue WIP hasta congelar reglas exactas de C0/S1/S2 y negative recovery.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir el commit D3 si el owner cambia el enfoque de validación o la fuente de datos.

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

# 2026-09-24 — Echo Futures Gerard D1 extraction

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Futures/Echo Futures.md`

## Motivo

- Persistir el primer brain dump del curso de Gerard como evidencia D1 y separar los motores de gestión antes de continuar la entrevista.

## Fuentes usadas

- Brain dump del owner sobre el curso privado de Gerard García.
- Captura suministrada de la tabla `Riesgo por Trade=300`, `Multiplicador=1.20`, payoff `1:1.5`.

## Resolución aplicada

- Separados negative hardscalping intra-trade, positive hardscalping/pyramiding y variable-risk inter-trade. Se documentó modelo matemático provisional de bandas sobre precio medio y contradicciones/UNKNOWNs para entrevista.

## Validación

- Los valores visibles 300→360→432→518→622→746→896→1075 son compatibles con multiplicador 1.20 salvo redondeos; la recuperación acumulada deja de ser positiva después de dos pérdidas. Proyecto re-leído tras persistencia.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir el commit D1 si el owner corrige sustancialmente el recuerdo del curso; mantener la fuente original como evidencia del cambio.

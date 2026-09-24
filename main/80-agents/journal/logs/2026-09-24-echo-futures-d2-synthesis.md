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

# 2026-09-24 — Echo Futures D2 synthesis

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Futures/Echo Futures.md`

## Motivo

- Revisar adversarialmente los tres Deep Research persistidos en `30-resources/futures`, cerrar D2 y evitar otra ronda abierta de investigación.

## Fuentes usadas

- `30-resources/futures/gerard-garcia-dr.md`
- `30-resources/futures/tradesfera-dr.md`
- `30-resources/futures/psicologo-del-trading-dr.md`
- Extracto/entrevista Gerard ya persistidos en el proyecto.

## Resolución aplicada

- Gerard DR clasificado evidencia pública débil; Tradesfera válido sólo para principios explícitos; Psicólogo NO_GO por corpus insuficiente. Research amplio cerrado. Pasan a D3 C0 random control, S1 ORB30 y S2 H4+Bollinger; experimentación secuencial entry→negative recovery→positive hardscalping→variable risk/prop.

## Validación

- Los tres informes fueron leídos desde `master`; se compararon fuentes, evidence ledgers y candidatos. Se rechazaron reglas inventadas sin soporte, especialmente atribuciones VWAP/RSI/ATR y secuencias ficticias.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir el commit D2 si aparece evidencia primaria concreta que cambie materialmente la selección de candidatos.

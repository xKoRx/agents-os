---
type: change_log
schema_version: 1
scope: session
created: "2026-09-21"
updated: "2026-09-21"
area: "[[Meli]]"
project: "[[Estandarización de Scopes RIO]]"
application: "[[rio-playmaker]]"
entities:
  - "[[Estandarización de Scopes RIO]]"
  - "[[POC KISS — Routing de scopes en Playmaker]]"
  - "[[rio-playmaker]]"
related:
  - "[[scope-naming-standard]]"
  - "[[SPEC técnica — Routing KISS por scope en rio-playmaker]]"
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

# Actualización — Routing desde la lane del runtime Fury

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Meli/Estandarización de Scopes RIO/agentes/POC KISS — Routing de scopes en Playmaker.md`
  - `10-projects/Meli/Estandarización de Scopes RIO/SPEC técnica — Routing KISS por scope en rio-playmaker.md`

## Motivo

- El owner cerró que `X-Rio-Scope` sólo pertenece a Fury Routes y que Playmaker debe derivar la lane desde el `SCOPE` de su propio runtime. También identificó un riesgo previo al routing: la resolución actual de Spring profiles puede impedir el arranque de alpha/prod o cargar recursos productivos en beta nonprod.

## Fuentes usadas

- Corrección explícita del owner del 2026-09-21.
- `rio-playmaker origin/master@f350fb26091d`: `ScopeUtils`, `application.yml`, `application-stage.yml`, `application-beta.yml`, ambos producers y `DeploymentTimeoutJob`.
- mqclient `3.4.9`: `Producer.send(Object, Filters)` y `Filters(List<String>)`.

## Resolución aplicada

- El plan quedó en tres fases: profiles/defaults seguros, filtros derivados del runtime en ambos producers y E2E alpha multibatch/retry.
- La SPEC define `prod → production`, `stage | alpha | beta | gamma → stage`, lane como primer token validado, default base `playmkrstg`/`nonprod` y fallback legacy sin filtro.
- Se eliminaron del estado objetivo el contrato HTTP de Playmaker, carrier por request, parsing de filtros en consumers, límite de retry/restart, spike de Fury y fallback a topics separados.
- La única limitación declarada es el posible retry cross-lane por la consulta global de `DeploymentTimeoutJob`; no se resuelve con estado durable en la POC.

## Validación

- `validate_plan.py`: 3 fases, 3 gates, 3 dispatches, 0 errores y 0 warnings.
- Lint estricto sobre planner y SPEC: `ERROR=0 WARN=0`.
- Búsqueda focalizada confirmó la ausencia de R2, R3, R6, R8, R9, DD-2, DD-3, DD-7, `invalid_header` y `malformed_filter`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sólo rutas relativas, SHA y contratos técnicos; sin secretos, tokens ni payloads productivos

## Rollback

- Revertir ambas notas mediante historial del vault si el owner revoca la fuente runtime. No existe código, schema ni infraestructura modificada por esta actualización.

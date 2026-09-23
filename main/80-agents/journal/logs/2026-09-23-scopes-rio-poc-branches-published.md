---
type: change_log
schema_version: 1
scope: session
created: "2026-09-23"
updated: "2026-09-23"
area: "[[Meli]]"
project: "[[Estandarización de Scopes RIO]]"
application:
entities:
  - "[[Estandarización de Scopes RIO]]"
  - "[[ads-signals-frontend]]"
  - "[[rio-playmaker]]"
  - "[[rio-controlplane-flink]]"
related:
  - "[[SPEC técnica — Routing dinámico de backend en ads-signals-frontend]]"
  - "[[SPEC técnica — Routing KISS por scope en rio-playmaker]]"
  - "[[SPEC técnica — Continuidad de scope en control planes RIO]]"
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

# Scopes RIO — ramas POC publicadas

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Meli/Estandarización de Scopes RIO/Estandarización de Scopes RIO.md`
  - `10-projects/Meli/Estandarización de Scopes RIO/SPEC técnica — Routing dinámico de backend en ads-signals-frontend.md`

## Motivo

- El scope frontend alpha fue materializado por Fury como `alpha-nonprod`; la SPEC anterior enviaba `env.SCOPE` sin separar la lane lógica del segmento físico. La implementación y el estado del proyecto debían reflejar el nombre real antes de levantar el resto de la infraestructura.

## Fuentes usadas

- Declaración del usuario sobre el alta `alpha-nonprod`.
- `ads-signals-frontend` `feature/poc-scope-routing@3a9eb3a0`.
- `rio-playmaker` `feature/poc-scope-routing@11de1d5fe` y commit funcional `f6ee097f9`.
- `rio-controlplane-flink` `feature/poc-scope-routing@e06a3bd8`.

## Resolución aplicada

- El default del BFF elimina exclusivamente el sufijo final `-nonprod`; `alpha-nonprod` se convierte en `alpha`. Los overrides explícitos permanecen literales y `*-nonsite` falla cerrado si el routing test estuviera habilitado. Se publicó la versión Fury común `0.0.1-poc-scopes-standard` para los tres artefactos. En Flink se reemplazó el accessor que confundía `APPLICATION` con el scope Fury por lectura directa de `SCOPE`, con fallback local y regresión dedicada. No se declararon cerrados los gates de deploy, infraestructura ni E2E.

## Validación

- Front: 21 tests focales, 7.034 tests completos, lint focal y build Nordic verdes; el typecheck aislado de tests conserva deuda previa fuera del delta.
- Playmaker: tests focales y suite completa verdes antes y después del merge de `develop`.
- Flink: tests focales y suite completa verdes, incluida la regresión con `APPLICATION` presente.
- Push verificado en `origin/feature/poc-scope-routing` para los tres repos.
- Fury: `0.0.1-poc-scopes-standard` quedó `FINISHED` en Front, Playmaker y Flink; Front requirió un reintento por timeouts Jest no reproducibles localmente y Flink otro después del fix de lectura de scope.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir los commits publicados o deshabilitar `playmaker_scope_routing_enabled`; no retirar routes/scopes legacy antes de probar drenaje y rollback.

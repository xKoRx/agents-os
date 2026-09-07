---
type: change_log
schema_version: 1
scope: session
created: "2026-08-24"
updated: "2026-08-24"
area: "[[Meli]]"
project: "[[Crear Context]]"
application: "[[rio-sdk-events]]"
entities:
  - "[[Crear Context]]"
  - "[[rio-sdk-events]]"
  - "[[rio-playmaker]]"
  - "[[AGENTS OS]]"
related:
  - "[[rjara-agent-profile]]"
  - "[[rjara-meli-work-preferences]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-08-24-rio-component-context-session-feedback]]"
  - "[[2026-08-24-rio-component-context-graphify-feedback]]"
share_scope: team
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Guardrail de versiones productivas desde master

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** conflict-resolution
- **Archivo(s):** constitución de Agents OS, perfiles global y Meli, skill `fury-lib-consumer-deploy`, proyecto [[Crear Context]], SPEC técnica y tasks canónicas de Context, y `build.gradle` de `rio-sdk-events`.

## Motivo

- La implementación había dejado `1.4.0` en `feature/new-component-context`, contradiciendo la regla del usuario: una versión productiva `X.Y.Z` sólo nace desde `master` después del merge.

## Fuentes usadas

- Corrección explícita del usuario, preferencia Meli preexistente y contrato operativo de `fury-lib-consumer-deploy` para versiones de prueba con sufijo.

## Resolución aplicada

- La feature del SDK queda en `0.0.2-component-context`; SIG-590 y T-06/T-07 separan la validación de feature del release `1.4.0` desde `master`; la prohibición queda duplicada intencionalmente en constitución, perfil global, perfil Meli y skill Fury.

## Validación

- Búsqueda cruzada de referencias `1.4.0`; Gradle reportó `version: 0.0.2-component-context`; suite y cobertura SDK verdes con 696 tests, 0 fallas y 0 errores; schema contract y lint estricto del delta sin errores; Graphify update bloqueado por 10 errores y una advertencia preexistentes fuera del cambio.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir este change log junto con las ediciones listadas y restaurar una versión de prueba con sufijo; nunca restaurar `X.Y.Z` en una feature.

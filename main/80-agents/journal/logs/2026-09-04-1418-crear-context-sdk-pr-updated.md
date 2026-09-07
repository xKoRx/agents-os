---
type: change_log
schema_version: 1
scope: session
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Meli]]"
project: "[[Crear Context]]"
application: "[[rio-sdk-events]]"
entities:
  - "[[Crear Context]]"
  - "[[rio-sdk-events]]"
related:
  - "[[Descripción PR — rio-sdk-events]]"
  - "[[2026-09-04-1418-codex-gpt-5-rio-sdk-context-pr]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-09-04-crear-context-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Crear Context — contrato SDK 1.5 y PR #46 actualizados

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):** [[Crear Context]]; [[Descripción PR — rio-sdk-events]].

## Motivo

- El owner cerró el shape 1.5: no existe `CurrentVersion`; `LatestVersion` lleva `inputs + outputs`; los relacionados llevan `outputs` directo; Context cubre deploy y undeploy; actions queda como extensión futura; la release objetivo es `1.5.0`.

## Fuentes usadas

- Definiciones entregadas por el owner; diff y tests de `rio-sdk-events`; [PR #46](https://github.com/melisource/fury_rio-sdk-events/pull/46); template `.github/PULL_REQUEST_TEMPLATE.md`.

## Resolución aplicada

- Se actualizó la fuente canónica del proyecto y su recurso de PR al commit `31b674d`, se retiró la política de logging sin autoridad, y se mantuvo la versión productiva `1.5.0` como objetivo para publicación desde `master`; la branch usa `0.0.2-component-version-identity`.

## Validación

- 703 tests PASS, JaCoCo PASS, `./gradlew check` PASS, `git diff --check` limpio, SHA local/remoto idéntico, todos los checks remotos del nuevo head verdes y lint estricto de las cuatro notas tocadas en `0 ERROR / 0 WARN`. El reindex Graphify se intentó y quedó bloqueado por deuda preexistente de 27 errores y 6 warnings; se conservó el último índice válido.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir `31b674d` en la branch y restaurar las dos notas desde su versión previa si el equipo rechaza el contrato.

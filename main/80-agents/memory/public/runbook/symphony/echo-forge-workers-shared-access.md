---
type: runbook
schema_version: 1
scope: application
created: "2026-08-11"
updated: "2026-10-27"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[StrategyQuant X]]"
  - "[[Symphony]]"
related:
  - "[[sqx-instrument-sync-history-only-verification-gap]]"
  - "[[2026-07-29-sqx-watcher-missing-on-hera-kronos]]"
aliases:
  - Echo Forge worker access
  - acceso Mac a workers Symphony
  - echo-forge-worker
  - echo-forge-workers-macos-keychain-access
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/runbook
  - scope/application
  - area/echo
  - project/echo-forge
  - app/echo-forge
  - tech/macos
  - tech/ssh
---

# Acceso compartido desde macOS a los workers de Echo Forge

## Propósito

Conservar la compatibilidad de enlaces de esta ruta histórica. La única autoridad operativa es [[30-resources/runbooks/symphony/echo-forge-workers-shared-access.md]]. Esta nota es una redirección y no posee procedimiento propio.

## Procedimiento

1. Abrir [[30-resources/runbooks/symphony/echo-forge-workers-shared-access.md]].
2. Resolver allí la vigencia, precondiciones y autorización del trabajo solicitado. La redirección no concede permisos ni acredita ejecución.

## Validación

- Consolidación documental del 2026-10-27: las rutas core y federada compartían el mismo blob Git `8bd4389ef7d56391be4d5cba3b70e761d7dd36ce` en `xKoRx/agents-os@81d4d6b00205855d223914f2c6d7ac70aebc5fa1`.
- Se conserva esta ruta y su título para referencias existentes; el procedimiento completo y su historia permanecen en la autoridad federada y en Git.
- Recuperación normal deshabilitada aquí: `indexable: false`, `index_priority: never`, `load_policy: manual`. No es una segunda autoridad activa.
- Validación de enlaces y schema no equivale a certificación física del runbook destino.

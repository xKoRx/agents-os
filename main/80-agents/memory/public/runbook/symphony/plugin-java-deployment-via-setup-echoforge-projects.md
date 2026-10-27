---
type: runbook
schema_version: 1
scope: application
created: "2026-08-03"
updated: "2026-10-27"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[StrategyQuant X]]"
  - "[[Symphony]]"
related:
  - "[[sqcli-echoforge-class-not-found-fresh-worker]]"
  - "[[echo-forge-workers-shared-access]]"
aliases:
  - Cómo desplegar EchoForgeAutomator.jar en workers
  - Setup plugin Java SQX
  - sqx/scripts/setup_echoforge_projects.sh
confidence: high
source_session: "2026-08-03-echo-forge-robust-run-audit-deploy-0-2-31"
load_policy: manual
indexable: false
index_priority: never
tags:
  - app/echo-forge
  - app/echoforge
  - area/echo
  - kind/runbook
  - project/echo-forge
  - project/echoforge
  - scope/application
  - tool/strategyquant
---

# Despliegue del plugin Java EchoForge en workers Symphony

## Propósito

Conservar la compatibilidad de enlaces de esta ruta histórica. La única autoridad operativa es [[30-resources/runbooks/symphony/plugin-java-deployment-via-setup-echoforge-projects.md]]. Esta nota es una redirección y no posee procedimiento propio.

## Procedimiento

1. Abrir [[30-resources/runbooks/symphony/plugin-java-deployment-via-setup-echoforge-projects.md]].
2. Resolver allí la vigencia, precondiciones y autorización del trabajo solicitado. La redirección no concede permisos ni acredita ejecución.

## Validación

- Consolidación documental del 2026-10-27: las rutas core y federada compartían el mismo blob Git `3f7180bb1a7973f955ffebf92abf37186e7f043c` en `xKoRx/agents-os@81d4d6b00205855d223914f2c6d7ac70aebc5fa1`.
- Se conserva esta ruta y su título para referencias existentes; el procedimiento completo y su historia permanecen en la autoridad federada y en Git.
- Recuperación normal deshabilitada aquí: `indexable: false`, `index_priority: never`, `load_policy: manual`. No es una segunda autoridad activa.
- Validación de enlaces y schema no equivale a certificación física del runbook destino.

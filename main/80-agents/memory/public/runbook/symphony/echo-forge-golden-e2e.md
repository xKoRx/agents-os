---
type: runbook
schema_version: 1
scope: application
created: "2026-08-29"
updated: "2026-10-27"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Symphony]]"
related:
  - "[[e2e-gated-validation]]"
  - "[[symphony-release-certification]]"
  - "[[symphony-worker-runtime-proof]]"
  - "[[symphony-prod-probe]]"
  - "[[echo-forge-cross-system-triage]]"
aliases:
  - golden run Echo Forge
  - E2E físico Symphony
  - certificación final durable
confidence: verified
source_session: DURABLE-ARTIFACT-VERIFIED-READS-FINAL-E2E-NORMAL
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/runbook
  - scope/application
  - project/echo-forge
---

# echo-forge-golden-e2e

## Propósito

Conservar la compatibilidad de enlaces de esta ruta histórica. La única autoridad operativa es [[30-resources/runbooks/symphony/echo-forge-golden-e2e.md]]. Esta nota es una redirección y no posee procedimiento propio.

## Procedimiento

1. Abrir [[30-resources/runbooks/symphony/echo-forge-golden-e2e.md]].
2. Resolver allí la vigencia, precondiciones y autorización del trabajo solicitado. La redirección no concede permisos ni acredita ejecución.

## Validación

- Consolidación documental del 2026-10-27: las rutas core y federada compartían el mismo blob Git `86f24f8839b3ec85c81c7903f03c83bf358f8f60` en `xKoRx/agents-os@81d4d6b00205855d223914f2c6d7ac70aebc5fa1`.
- Se conserva esta ruta y su título para referencias existentes; el procedimiento completo y su historia permanecen en la autoridad federada y en Git.
- Recuperación normal deshabilitada aquí: `indexable: false`, `index_priority: never`, `load_policy: manual`. No es una segunda autoridad activa.
- Validación de enlaces y schema no equivale a certificación física del runbook destino.

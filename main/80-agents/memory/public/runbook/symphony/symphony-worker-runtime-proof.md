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
  - "[[deployment-proof]]"
  - "[[evidence-channel-discovery]]"
  - "[[symphony-release-certification]]"
aliases:
  - prueba de workers Symphony
  - matriz de canales de evidencia Echo Forge
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

# symphony-worker-runtime-proof

## Propósito

Conservar la compatibilidad de enlaces de esta ruta histórica. La única autoridad operativa es [[30-resources/runbooks/symphony/symphony-worker-runtime-proof.md]]. Esta nota es una redirección y no posee procedimiento propio.

## Procedimiento

1. Abrir [[30-resources/runbooks/symphony/symphony-worker-runtime-proof.md]].
2. Resolver allí la vigencia, precondiciones y autorización del trabajo solicitado. La redirección no concede permisos ni acredita ejecución.

## Validación

- Consolidación documental del 2026-10-27: las rutas core y federada compartían el mismo blob Git `114a5be5a12511bc52a3b0bc3674be761ee3b84b` en `xKoRx/agents-os@81d4d6b00205855d223914f2c6d7ac70aebc5fa1`.
- Se conserva esta ruta y su título para referencias existentes; el procedimiento completo y su historia permanecen en la autoridad federada y en Git.
- Recuperación normal deshabilitada aquí: `indexable: false`, `index_priority: never`, `load_policy: manual`. No es una segunda autoridad activa.
- Validación de enlaces y schema no equivale a certificación física del runbook destino.

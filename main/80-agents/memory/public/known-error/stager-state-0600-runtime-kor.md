---
type: known_error
schema_version: 1
scope: application
created: "2026-08-15"
updated: "2026-08-15"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[stager-app]]"
entities:
  - "[[stager-app]]"
related:
  - "[[stager-staged-without-runtime-request]]"
  - "[[Stager - Cross-Platform Deployment Lifecycle]]"
aliases:
  - stager CURRENT permission denied
  - state CURRENT 0600
confidence: verified
source_session: 7bfc3412-5936-4c7c-85b8-8dd1cf059569
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
---

# Stager state 0600 vs runtime kor

## Síntoma

- `stager-runtime failed: read CURRENT: open .../state/CURRENT: permission denied`
- El overlay canary corre el runtime como `kor`; el one-shot escribe como `stager`.

## Causa

- `activation.Store.writeAtomic` hacía `Chmod(0600)` en `state/CURRENT`, `ACTIVATION.json` y `RUNNING`. Un `chmod` manual a 644 se pierde en el siguiente reconcile.

## Impacto

- Tras cada `deploy_release` el runtime no adopta la release; el worker queda en la versión anterior o cae.

## Detección

- `stat` de `state/CURRENT` = 600 y owner `stager`, mientras `stager-runtime.service` `User=kor`.
- Journal: `permission denied` al leer `state/CURRENT`.

## Mitigación

- El one-shot debe escribir esos archivos en 0644 (mismo criterio que el `CURRENT` de raíz).
- No parchear permisos a mano en el host: el próximo tick los vuelve a 0600 si el binario viejo sigue.

## Evidencia

- 2026-08-15: chmod host sobrevivió horas hasta el reconcile; con binario 0644, `0.2.43` y `0.2.44` dejaron 644 en Zeus/Hera/Kronos y runtime `active`.

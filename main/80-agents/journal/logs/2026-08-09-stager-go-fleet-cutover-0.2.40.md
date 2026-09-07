---
type: change_log
scope: session
created: 2026-08-09
updated: 2026-08-09
area: "[[Echo]]"
project: "[[Stager - Symphony Publisher Integration]]"
application: "[[stager-app]]"
entities:
  - "[[Stager - Symphony Publisher Integration]]"
  - "[[Echo Forge]]"
  - "[[stager-app]]"
related:
  - "[[stager-go-requires-current-pending-bridge]]"
aliases:
  - stager go fleet cutover 0.2.40
confidence: verified
source_session:
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Cutover Stager Go + release 0.2.40

## Cambio

- **Tipo:** updated / operational cutover
- **Archivo(s) / hosts:**
  - Zeus/Hera/Kronos: `/usr/local/bin/stager`, `/usr/local/sbin/symphony-stager-go`, `symphony-stager.service`
  - MinIO `deploy/worker/sqx` release + manifest `0.2.40`
  - `docs/deployment/stager-publisher-integration.md`
  - `10-projects/Echo Forge/agentes/Stager - Symphony Publisher Integration.md`
  - `10-projects/Echo Forge/Echo Forge.md`
  - `80-agents/memory/public/known-error/stager-go-requires-current-pending-bridge.md`

## Motivo

Owner pidió preparar Hera/Kronos (y de facto Zeus) para el Stager nuevo, publicar Echo Forge y validar actualización en toda la flota.

## Resultado

- Flota en `CURRENT=0.2.40` con workers `active` desde `releases/0.2.40`.
- Bash respaldado como `.bash.bak`.
- Known error del puente layout/permisos documentado.

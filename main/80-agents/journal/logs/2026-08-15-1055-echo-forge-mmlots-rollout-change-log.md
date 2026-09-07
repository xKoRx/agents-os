---
type: change_log
schema_version: 1
scope: session
created: "2026-08-15"
updated: "2026-08-15"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[stager-app]]"
entities:
  - "[[stager-app]]"
  - "[[Symphony]]"
related:
  - "[[stager-state-0600-runtime-kor]]"
  - "[[2026-08-15-1055-echo-forge-mmlots-rollout-session-feedback]]"
aliases: []
confidence: verified
source_session: 7bfc3412-5936-4c7c-85b8-8dd1cf059569
source_feedbacks:
  - "[[2026-08-15-1055-echo-forge-mmlots-rollout-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-15-1055-echo-forge-mmlots-rollout-change-log

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `80-agents/memory/public/known-error/stager-state-0600-runtime-kor.md`
  - `10-projects/Echo Forge/Echo Forge.md`
  - `stager/internal/activation/store.go` (repo externo)

## Motivo

- El one-shot escribía state v2 en 0600 y el runtime `kor` no podía leer `CURRENT` tras cada reconcile.

## Fuentes usadas

- Canary de permisos en Zeus/Hera/Kronos tras `0.2.43` y `0.2.44`
- `activation/store.go` `writeAtomic`

## Resolución aplicada

- State files 0644 en código + binario one-shot en flota; known error indexable; tarea puente a Review.

## Validación

- Tras `0.2.44`, `stat` de `CURRENT`/`ACTIVATION.json`/`RUNNING` = 644 y `stager-runtime` `active` en los tres Linux.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales de máquina de desarrollo, memoria interna ni secretos

## Rollback

- Revertir `stateFilePerm` a 0600 y redesplegar el one-shot; no revierte los archivos ya escritos.

---
type: change_log
scope: project
created: 2026-08-08
updated: 2026-08-08
area: "[[Echo]]"
project: "[[Echo Forge - Etapa 6]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge - Etapa 6]]"
  - "[[Echo Forge]]"
related:
  - "[[echo-forge]]"
aliases: []
confidence: verified
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/project
  - project/echo-forge
  - area/echo
---

# Change log — Echo Forge Etapa 6 F7–F8 completed

## Qué cambió

- Sistema 2: [[Echo Forge - Etapa 6]] registra F7 y F8 completadas, progreso 75% y F9 como siguiente fase.
- Sistema 2: [[Echo Forge]] actualiza el resumen y la tarea puente a F0–F8 PASS.
- Código `symphony`: commits `6fc3999` (runner portable, preflight SQ y deltas de journals) y `b4cc7b4` (activity de backtesting y publicación de evidencia).

## Motivo

El owner solicitó desarrollar F7 y F8 de Etapa 6 y cerrar la sesión al concluir.

## Validación

- Tests focalizados y regresión de `adapters/mt5` y `activities/worker` en PASS.
- Ejecución con detector de carreras y cross-build Windows amd64 en PASS.
- `git diff --check` limpio para los cambios entregados.

## Rollback

Revertir los commits `b4cc7b4` y `6fc3999` en orden inverso; restaurar las dos notas de proyecto si se deshace la entrega.

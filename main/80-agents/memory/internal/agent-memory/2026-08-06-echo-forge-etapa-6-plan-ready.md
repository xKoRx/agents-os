---
type: agent_memory
scope: project
created: 2026-08-06
updated: 2026-08-06
project: "[[Echo Forge - Etapa 6]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge - Etapa 6]]"
aliases:
  - etapa 6 mt5 plan ready
tags:
  - kind/doc
  - kind/agent-memory
  - project/echo-forge
  - status/active
---

# Continuidad — Etapa 6 F2 lista; siguiente = F3 keys/listing/affinity

F0 y F1 quedaron aprobados, y F2 fue implementada y verificada en el commit
`3f5d9a7`. La tarea puente de [[Echo Forge]] está en Review; no avanzar F3 sin
revisión/continuación del owner.

## Próximo paso

**F3 — Derivación de keys, listado y afinidad**: implementar full keys opacas,
listado determinista y routing puro `task type → WorkerClassMT5 →
sqx-mt5-queue`, respetando los archivos Allowed/New del PLAN.

## Anclas

- Tareas atómicas: `mt5_compiler` + `mt5_backtesting`; child workflow por estrategia; sin parseo/Mongo/deviation.
- Affinity: `WorkerClass` → `sqx-mt5-queue` para esas dos.
- SDD: extender `CHANGE-001` aprobado de `FEAT-SQX-MT5-BACKTEST-COMPILE`, no inventar delta nuevo.
- Etapa 6 se adelanta a Etapa 5 a propósito (R9); [[Echo Forge - Etapas 5 y 7]] queda para backtracking/reporte.

---
type: change_log
scope: session
created: 2026-08-06
updated: 2026-08-06
area: "[[Echo]]"
project: "[[Echo Forge]]"
entities:
  - "[[Echo Forge]]"
  - "[[echo-forge]]"
related:
  - "[[Echo Forge - Etapa 6]]"
  - "[[Echo Forge - Etapas 5 y 7]]"
  - "[[80-agents/skills/agents-os-requirement-interview/SKILL.md|agents-os-requirement-interview]]"
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
share_scope: local
tags:
  - kind/change-log
  - scope/session
  - area/echo
  - project/echo-forge
  - change/created
  - change/updated
---

# Change Log — Separación de Etapa 6 y plan de backtesting MT5

## Cambios

- **Creado** `10-projects/Echo Forge/agentes/Echo Forge - Etapa 6.md`: proyecto de
  agente con el plan de implementación de la Etapa 6. Contiene alcance decidido,
  contexto verificado del repo (8 hechos con archivo:línea), siete hallazgos de
  desalineamiento (H1–H7), diseño de las dos tareas atómicas, contrato de
  `config.json`, registro de afinidad de workers, mapa de impacto de archivos,
  checklist inicial de siete fases, luego auditado y reemplazado por doce fases
  secuenciales F0-F11 con gates explícitos.
- **Renombrado** `Echo Forge - Etapas 5-7.md` → `Echo Forge - Etapas 5 y 7.md`.
  Ajustados título, alias, objetivo, estado, fuente de tareas y las cuatro
  queries `path includes`. Progreso recalculado 40% → 20% porque el avance que lo
  sostenía (worker MT5 y filtro de desviación) migró al proyecto nuevo.
- **Actualizado** `Echo Forge.md`: nueva tarea puente para Etapa 6, tarea puente
  existente reapuntada al nombre nuevo, estado de Etapa 6 corregido (estaba
  declarada "parcial" por código existente, cuando en realidad no está integrada
  al pipeline) y entrada de bitácora.
- **Actualizadas** referencias al nombre viejo en `Echo Forge - Etapa 4.md`,
  `Echo Forge - Cierre de Etapa 4.md` y
  `journal/logs/2026-08-06-echo-forge-stage-4-closeout.md`.

## Decisiones del owner que cambian el diseño previo

La guía externa `GUIA_WORKER_TEMPORAL_MT5` proponía una sola tarea MT5 con
parseo, normalización, Mongo, deviation y lock distribuido. El owner la redujo a
**dos tareas atómicas** que solo depositan artefactos crudos en MinIO
(`mt5_compiler` y `mt5_backtesting`), dejando el procesamiento para tareas
posteriores. También descartó extender `adaptive_workflow.go`: la única puerta es
`generic_workflow.go` con `config.json`.

## Efecto colateral positivo

El diseño elimina la sección `[Common]` del `tester.ini`, con lo que cierra el
GAP `EF-G27` del backlog del programa (password demo MT5 expuesta en archivo
temporal).

## Replanificación validada

- El plan se contrastó contra los contracts/adapters/workflows reales, las reglas
  SDD del repo, tests focalizados y la documentación primaria de MetaTrader 5.
- Se corrigieron desalineamientos materiales: los child workflows no pueden
  ejecutarse en la queue MT5 actual porque allí sólo se registran activities;
  `Model=4` representa ticks reales; `Leverage` debe escribirse `1:N`; la
  validación del config debe entrar por el watcher; los contratos adaptativos
  existentes requieren BWC aditiva; y las full keys de MinIO deben propagarse
  sin reconstruir identidad.
- SDD se movió al inicio y se decidió crear
  `FEAT-SQX-MT5-PIPELINE-ARTIFACTS` en vez de sobrescribir el PLAN/TASKS/PASS
  histórico de `FEAT-SQX-MT5-BACKTEST-COMPILE`.
- Se mantienen `sqx-main-queue` y `sqx-mt5-queue`; unificar las claves ETCD
  duplicadas queda fuera de esta etapa.
- La tarea puente del padre pasó de Todo a WIP.

## Pendiente

Ejecutar F0: contrato físico Windows, fixtures sanitizados y aprobación del SPEC
antes de cualquier implementación.

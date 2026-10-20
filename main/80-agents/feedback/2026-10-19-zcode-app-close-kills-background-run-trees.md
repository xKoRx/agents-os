---
type: feedback
schema_version: 1
scope: session
created: "2026-10-19"
updated: "2026-10-19"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
  - "[[Echo Futures]]"
related: ["[[ZCode]]"]
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run: "[[2026-10-19-zcode-glm53-flash-challenge-history]]"
session_goal: ejecutar y auditar la historia completa challenge (26 configuraciones) reanudando el WIP de GOD
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/agents-os
  - agent/system1
---

# Session Feedback - 2026-10-19 - zcode app close kills background run trees

## Context

- Agent surface: [[ZCode]]
- Agent model: GLM-5.3-Flash (host-reported)
- Agent run: [[2026-10-19-zcode-glm53-flash-challenge-history]]
- Session goal: completar ejecución histórica 26 configuraciones Echo Futures
- Main entity: [[Echo Futures]]
- Skills used: agents-os-bootstrap, agents-os-session-close, agents-os-session-feedback
- Retrieval mode: handoff local (PAUSA-HANDOFF) + evidencia del checkout; sin Graphify
- Artifacts changed: repo echo (5 commits pusheados), run roots r4/r5, release GitHub, notas de continuidad

## Scores

- Startup clarity: 5
- Retrieval usefulness: 4
- Skill fit: 4
- Template fit: 4
- Closeout friction: 3
- Overall confidence: 4

## What Complicated The Session Most

- Observation: el cierre de la app anfitriona (owner cerró ZCode "bugeada") mató el lanzador de campañas y 4 motores que corrían como tareas en segundo plano del harness; los estados quedaron RUNNING sin procesos.
- Why it was hard: las tareas background del harness son hijas del árbol de la app; la continuación por notificación no existe si la app muere, y la recuperación en la misma raíz está prohibida por diseño (intentos interrumpidos inmutables) → raíz nueva + re-ejecución completa de 4 trayectorias (~20 h perdidas).
- Proposed improvement: para cualquier proceso largo lanzado desde el agente, usar `setsid nohup` + estados duraderos en disco desde el primer lanzamiento, no como remedio posterior; documentarlo como patrón operativo.

## Most Useful Part Of Sistema 1

- What helped: el handoff PAUSA-HANDOFF.md con checkout/HEAD/recibos exactos permitió retomar sin re-derivar nada.
- Why it helped: identidad y evidencia ya separadas del historial de chat.
- Keep/change: keep.

## Least Useful Or Noisy Part

- What did not help: los directorios `.tmp.*` huérfanos acumulados en `10-projects/Echo Futures/` ensucian el descubrimiento de la nota de control.
- Why it was weak/noisy: restos de escrituras atómicas interrumpidas nunca recolectados.
- Proposed cleanup: barrido de `*.tmp.*` con regla de higiene.

## Missing Support

- Problem not solved by Sistema 1: no había patrón registrado para ejecuciones de horas que deben sobrevivir al ciclo de vida de la app anfitriona.
- How Sistema 1 could help next time: un runbook operativo corto (setsid + estado atómico en disco + reconciliación al volver) referenciado desde el perfil de operaciones.
- Suggested artifact type: runbook (Sistema 1) — ya se dejó el patrón probado en el RUNBOOK-CONTINUIDAD del repo echo.

## Retrieval Feedback

- Useful query or source: handoff local del chat anterior; recibos de verificación dentro del repo.
- Missing context: ninguna relevante para el arranque.
- Duplicate/noisy result: n/a.
- Better future query: n/a.

## Skill Feedback

- Skill that worked well: agents-os-bootstrap (cold start mínimo), agents-os-session-close (delta classifier claro).
- Skill that was confusing: el nombre de tipos contratados (`agent_run`/`feedback` con guion bajo) no es obvio desde los nombres de template (`agent-run.md`/`session-feedback.md`).
- Trigger/routing gap: menor.
- Suggested contract change: ninguna.

## Template Feedback

- Template used: agent-run, session-feedback.
- Field that helped: agent_surface/agent_model/model_source separados.
- Field that felt redundant: ninguna.
- Missing field: n/a.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? sí (nota global always-load del bootstrap).
- ¿Qué valor operativo aportó para esta sesión? reglas transferibles (leer estado durable antes de repetir efectos; terminalidad lógica ≠ drenaje físico) aplicadas a la reconciliación de estados RUNNING muertos.
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna? la continuidad quedó en el repo (RUNBOOK), release GitHub y nota de proyecto; la automatización programada publica r5.
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad? 4.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: medium
- Candidate owner: operación de agentes con ejecuciones largas (cualquier proyecto).
- Promote to L3 memory? defer (el patrón setsid ya quedó documentado en el RUNBOOK del repo; promover si se repite en otro proyecto).

## One Next Improvement

- Registrar el patrón "procesos largos setsid-desacoplados + estado atómico + reconciliación" como runbook de Sistema 1 la próxima vez que una ejecución de horas vuelva a ser necesaria.

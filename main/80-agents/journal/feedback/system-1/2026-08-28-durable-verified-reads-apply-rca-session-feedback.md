---
type: feedback
schema_version: 1
scope: session
created: 2026-08-28
updated: 2026-08-28
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[2026-08-28-durable-verified-reads-apply-reconciliation-rca]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3
agent_run: "[[2026-08-28-zcode-glm-5-3-durable-verified-reads-apply-rca-top]]"
session_goal: DURABLE-ARTIFACT-VERIFIED-READS-APPLY-RCA-TOP
source_session: DURABLE-ARTIFACT-VERIFIED-READS-APPLY-RCA-TOP
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

# Session Feedback - 2026-08-28 - durable verified reads apply rca

## Context

- Agent surface: [[ZCode]]
- Agent model: GLM-5.3 (builtin:zai-coding-plan/GLM-5.3)
- Agent run: [[2026-08-28-zcode-glm-5-3-durable-verified-reads-apply-rca-top]]
- Session goal: RCA/DESIGN read-only del blocker Apply reconcile (fabricación de digest desde storage) sobre symphony @`5e93c7c`.
- Main entity: [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]
- Skills used: agents-os-bootstrap, agents-os-context-retrieval (implícito), agents-os-session-close, agents-os-agent-run-register
- Retrieval mode: búsqueda enfocada por nombres exactos (known-error, checkpoints, decisiones) + Graphify no necesario (nombres canónicos conocidos de antemano)
- Artifacts changed: decisión symphony (created), known-error (updated), checkpoint proyecto (append), agent-run, change-log, feedback, continuidad interna.

## Scores

Use 1-5, where 1 is poor and 5 is excellent.

- Startup clarity: 5
- Retrieval usefulness: 5
- Skill fit: 5
- Template fit: 4
- Closeout friction: 4
- Overall confidence: 5

## What Complicated The Session Most

- Observation: el veredicto de byte-determinismo del productor Apply NO es comprobable desde una máquina de dev (`/home/kor/sqx` inexistente; `sqcli` + `project.cfx` reales viven sólo en workers).
- Why it was hard: la clasificación BYTE_DETERMINISTIC_PROVEN vs NONDETERMINISTIC decide entre opciones de recovery authority; hubo que diseñar un contrato cuya corrección NO dependa del veredicto y derivar el experimento físico a la fase E2E.
- Proposed improvement: incluir en la guía de certificación E2E un "determinism probe" estandarizado (2 corridas ≥90s aparte + `zipinfo -v` diff) para productores SQX, ejecutable en worker host, de modo que futuros RCAs de recovery citen evidencia física en vez de dejarla como NOT_PROVEN.

## Most Useful Part Of Sistema 1

- What helped: los checkpoints densos por sesión en la nota del proyecto (formato KEY:VALUE) permitieron cargar 6 sesiones de historia en 2 lecturas quirúrgicas; el known-error ya registrado hizo el bootstrap del blocker trivial.
- Why it helped: la pregunta central del RCA ya estaba semiformalizada por sesiones previas (write-once, verified reads, builder recovery) y cada hecho citado tenía file:line verificable.
- Keep/change: keep; el patrón checkpoint-denso + decisión-compacta + handoff-al-owner es el ciclo correcto.

## Least Useful Or Noisy Part

- What did not help: nada material esta sesión.
- Why it was weak/noisy: —
- Proposed cleanup: —

## Missing Support

- Problem not solved by Sistema 1: la imposibilidad de ejecutar experimentos físicos contra workers/infra real desde la superficie de agente (limitación de entorno, no de Sistema 1).
- How Sistema 1 could help next time: runbook canónico de "experimento físico en worker host" con template de evidencia (comandos + captura + dónde depositar el resultado para citarlo desde notas).
- Suggested artifact type: runbook.

## Retrieval Feedback

- Useful query or source: `find` por nombre exacto de known-error y decisión; lectura del último bloque de checkpoints del proyecto (offset sobre `grep -n "^## Session checkpoint"`).
- Missing context: ninguno material.
- Duplicate/noisy result: —
- Better future query: —

## Skill Feedback

- Skill that worked well: agents-os-bootstrap (cold start quirúrgico, 3 archivos base + entity pack en ~4 lecturas); agents-os-session-close (delta classifier evitó L0/L1 innecesarios).
- Skill that was confusing: ninguna.
- Trigger/routing gap: ninguna.
- Suggested contract change: ninguna.

## Template Feedback

- Template used: decision, agent_run, feedback, change_log.
- Field that helped: `source_session` + `related` en known-error (trazabilidad RCA→corrección sin buscar).
- Field that felt redundant: —
- Missing field: —

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? sí (nota global always según bootstrap).
- ¿Qué valor operativo aportó para esta sesión (continuidad, detalles crudos, advertencias)? continuidad completa del track durable: 6 sesiones previas condensadas con baselines/veredictos/next-exact, evitando re-derivar historia.
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna? sí: línea de continuidad de esta sesión con el veredicto y el NEXT EXACT.
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad? 5; mantener la disciplina de una línea por sesión.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: medium
- Candidate owner: certificación E2E / track durable
- Promote to L3 memory? defer (probar el probe en el próximo E2E primero)

## One Next Improvement

- Agregar un "determinism probe" estandarizado (worker host) a la guía de certificación E2E para productores SQX, y citar su evidencia desde los RCAs de recovery en lugar de cerrar BYTE_DETERMINISTIC_NOT_PROVEN por imposibilidad de entorno.

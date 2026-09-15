---
type: feedback
schema_version: 1
scope: session
created: 2026-09-14
updated: 2026-09-14
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[AGENTS OS - Context Hygiene and Canonical Integrity]]"
  - "[[pass-declarado-no-es-pass-verificado]]"
  - "[[doctor-verde-falso-por-duplicados-core-federado]]"
aliases: []
agent_surface: "[[Claude Code]]"
agent_model: claude-opus-5
agent_run: "[[2026-09-14-claude-code-opus-5-p4-adversarial-verification]]"
session_goal: Validar adversarialmente PHASE 3.5 y PHASE 4 entregadas por otro agente, y cerrar consenso
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

# Session Feedback - 2026-09-14 - verificación adversarial P4

## Context

- Agent surface: Claude Code (desktop)
- Agent model: claude-opus-5
- Agent run: [[2026-09-14-claude-code-opus-5-p4-adversarial-verification]]
- Session goal: actuar como verifier independiente de dos entregas consecutivas de otro agente
- Main entity: [[AGENTS OS]]
- Skills used: `agents-os-bootstrap`, `agents-os-project-impact-brief`, `agents-os-session-close`
- Retrieval mode: ejecución directa de gates reales; sondas en scratch; lectura dirigida de fuentes canónicas
- Artifacts changed: un learning reforzado, un agent run, este feedback, un change log

## Scores

- Startup clarity: 5
- Retrieval usefulness: 4
- Skill fit: 4
- Template fit: 4
- Closeout friction: 4
- Overall confidence: 5

## What Complicated The Session Most

- Observation: los dos defectos de PHASE 4 eran inalcanzables por los caminos vigentes. `LOW=0` hoy, y el fidelity gate estaba en `PASS`, así que ninguna corrida real los mostraba.
- Why it was hard: sólo aparecieron al invocar `structural_component` y `exit_code` directamente con entradas sintéticas. Ni el diff, ni los selftests del implementador, ni el reporte los habrían revelado, porque todos ejercitan el estado actual y no el estado posible.
- Proposed improvement: cuando un componente mapee severidades o estados a un vocabulario distinto del propio, exigir un caso de prueba por valor del vocabulario de origen, incluidos los que hoy valen cero. Una tabla de mapeo sin cobertura por valor es una rama sin test.

## Most Useful Part Of Sistema 1

- What helped: `agents-os-project-impact-brief` otra vez, y el protocolo de no aceptar reportes por autoridad.
- Why it helped: el implementador entregó evidencia verde, abundante y verdadera en las cuatro rondas. Lo que cambió cada veredicto fue ejecutar el gate, no leerlo — incluido el caso donde yo mismo descarté una hipótesis propia antes de reportarla.
- Keep/change: keep. El handoff adversarial que el implementador dejó, con resultados esperados y doce ataques concretos, es el formato que hizo barata la verificación; vale la pena volverlo norma para cualquier entrega que pida challenge.

## Least Useful Or Noisy Part

- What did not help: el lint corpus-wide en `NO-GO` con 76 fingerprints nuevos sobre un baseline del 2026-09-09.
- Why it was weak/noisy: apareció en cada `graphify` de la sesión sin poder distinguir deuda mía de deuda ajena, así que su única contribución fue ruido que hubo que declarar y descartar cuatro veces.
- Proposed cleanup: repoblar el baseline del lint o declararlo caducado. Un gate que siempre dice `NO-GO` deja de ser señal.

## Missing Support

- Problem not solved by Sistema 1: nada del sistema obliga a que un verifier sea distinto del implementador. Esta sesión funcionó porque el owner lo pidió explícitamente, no porque el contrato lo exija.
- How Sistema 1 could help next time: que un gate de entrega estructural declare quién verificó y con qué superficie×modelo, y que coincidir implementador y verifier sea un estado declarado, no invisible.
- Suggested artifact type: campo en el contrato de gate del project workflow, no una skill nueva.

## Retrieval Feedback

- Useful query or source: los entrypoints reales de los providers y `build-core.py`. Leer el código del check fue lo que refutó dos diagnósticos escritos.
- Missing context: ninguno bloqueante.
- Duplicate/noisy result: ya resuelto — la duplicación core↔federado que ensuciaba toda búsqueda por nombre de skill desapareció con PHASE 3.5.
- Better future query: ante un `MEDIUM` cuyo texto nombre el síntoma, leer la función del check antes de aceptar su redacción como diagnóstico.

## Skill Feedback

- Skill that worked well: `agents-os-project-impact-brief`.
- Skill that was confusing: ninguna.
- Trigger/routing gap: el mismo de la sesión anterior y sigue abierto: `agents-os-implementation-planning` puede emitir un plan de cinco fases sin contrastar nada contra la implementación vigente. Esta sesión volvió a demostrarlo: el plan original no tocaba ninguno de los cuatro defectos reales.
- Suggested contract change: exigir el contraste con la realidad antes de emitir fases, o declarar explícitamente que no se hizo.

## Template Feedback

- Template used: `feedback`, `agent_run`, `change_log`.
- Field that helped: `verification` y `user_rework` del `agent_run`; separan lo que se ejecutó de lo que el owner tuvo que rehacer.
- Field that felt redundant: ninguno.
- Missing field: en `agent_run`, algo que distinga el rol —implementador o verifier—. Son trabajos con perfiles de evidencia distintos y hoy se miden con la misma plantilla.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna al iniciar? Sí, la nota global de continuidad.
- ¿Qué valor operativo aportó? El mismo párrafo que ya sirvió la sesión pasada: un comando verde no prueba el resultado real, y la verificación pertenece a la capa dueña de la semántica. Esta vez fue literalmente el criterio que encontró los dos defectos.
- ¿Dejaste algún mensaje para el próximo agente? No hizo falta: el delta durable quedó en el learning público y en el planner.
- ¿Utilidad del espacio privado (1-5)? 4. Su valor sostenido es que contiene comportamientos y no estado.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: medium
- Candidate owner: [[AGENTS OS - Context Hygiene and Canonical Integrity]]
- Promote to L3 memory? no — se reforzó [[pass-declarado-no-es-pass-verificado]] en vez de crear una nota nueva

## One Next Improvement

- Cobertura por valor en toda tabla de mapeo entre vocabularios. Los dos defectos de PHASE 4 vivían en ramas que ninguna entrada real alcanzaba todavía, y el sistema las reportaba como verdes porque nunca las ejecutó.

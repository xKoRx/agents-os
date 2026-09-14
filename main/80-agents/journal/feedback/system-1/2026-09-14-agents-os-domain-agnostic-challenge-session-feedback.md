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
  - "[[AGENTS OS - Desarrollo Agnóstico por Dominio]]"
  - "[[AGENTS OS - Context Hygiene and Canonical Integrity]]"
  - "[[doctor-verde-falso-por-duplicados-core-federado]]"
aliases: []
agent_surface: "[[Claude Code]]"
agent_model: claude-opus-5
agent_run:
session_goal: Validar si un plan de desarrollo agnóstico por dominio aportaba valor real, y converger con el agente autor
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

# Session Feedback - 2026-09-14 - challenge desarrollo agnóstico

## Context

- Agent surface: Claude Code (desktop)
- Agent model: claude-opus-5
- Agent run: no aplica; no hubo generación ni evaluación de código
- Session goal: auditar una propuesta arquitectónica y negociar consenso con el agente que la escribió
- Main entity: [[AGENTS OS]]
- Skills used: `agents-os-bootstrap`, `agents-os-project-impact-brief`, `agents-os-session-close`
- Retrieval mode: lectura dirigida de fuentes canónicas + ejecución read-only de `doctor.py` y comparaciones byte a byte
- Artifacts changed: un known error, un change log, tres notas de proyecto

## Scores

- Startup clarity: 5
- Retrieval usefulness: 4
- Skill fit: 5
- Template fit: 4
- Closeout friction: 3
- Overall confidence: 5

## What Complicated The Session Most

- Observation: el plan bajo auditoría llegó con validación propia declarada verde (`validate_plan.py` PASS, lint `ERROR=0/WARN=0`, schemas verdes) y con la deuda de Doctor clasificada como "previa y ajena". Todo eso era literalmente cierto y aun así el diagnóstico estaba equivocado.
- Why it was hard: los verdes del sistema miden forma, no verdad. Para refutar el diagnóstico hubo que ejecutar Doctor, leer su código de check y comparar archivos a mano. Un agente que confíe en el reporte anterior hereda el error completo.
- Proposed improvement: cuando una bitácora clasifique deuda como "ajena" o "previa", exigir la evidencia del baseline que lo respalda. Acá el cockpit declaraba `Doctor 0/0/0` al 2026-09-09 y la deuda apareció después: el contraste estaba a una línea de distancia.

## Most Useful Part Of Sistema 1

- What helped: `agents-os-project-impact-brief`. Su procedimiento —ledger `CONFIRMADO/INFERIDO/DESCONOCIDO`, separar propuesta de realidad, citar evidencia por contradicción material— es exactamente lo que evitó aceptar un plan bien escrito.
- Why it helped: obliga a ir al artefacto vigente antes de opinar. Las tres contradicciones que cambiaron la decisión salieron de ahí.
- Keep/change: keep sin cambios.

## Least Useful Or Noisy Part

- What did not help: el mensaje del check de Doctor, `skill missing from index`.
- Why it was weak/noisy: nombra el síntoma como si fuera la causa. El agente anterior lo leyó literal y concluyó "faltan filas en `INDEX.md`", cuando las filas estaban y lo que sobraba eran archivos. El mensaje dirigió mal la investigación.
- Proposed cleanup: cuando la skill exista en ambos árboles, el finding debería decir que hay duplicado core↔federado y nombrar las dos rutas.

## Missing Support

- Problem not solved by Sistema 1: ninguna herramienta cubre runbooks. `canonical-linter` y `doctor` miran skills contra `INDEX.md`, así que 9 runbooks duplicados —tres con divergencia real de contenido y uno `superseded` vivo en el core— no producen un solo finding.
- How Sistema 1 could help next time: la cobertura del linter debería declararse por clase de artefacto, y una clase sin cobertura debería ser visible en el reporte en vez de silenciosa. Un verde que no dice qué no miró es un verde que miente por omisión.
- Suggested artifact type: check del provider `Canonical` (ya acordado como P35-E) + declaración explícita de cobertura en el envelope de PHASE 4.

## Retrieval Feedback

- Useful query or source: `sources.list` y `build-core.py` del core export. Fueron los que convirtieron "el core menciona Meli" en un impacto concreto sobre otra persona.
- Missing context: nada bloqueante.
- Duplicate/noisy result: los duplicados core↔federado ensuciaron toda búsqueda por nombre de skill durante la sesión. El defecto también es ruido de retrieval, no sólo de canonicalidad.
- Better future query: comparar los dos árboles por nombre antes de abrir cualquier skill federada.

## Skill Feedback

- Skill that worked well: `agents-os-project-impact-brief`.
- Skill that was confusing: ninguna.
- Trigger/routing gap: `agents-os-implementation-planning` puede emitir un proyecto de cinco fases con gates sin haber contrastado nada contra la implementación vigente. Acá produjo 5 fases, 5 gates y 14 tareas para un problema que se resuelve en un slice. El impact brief llegó después del plan, que es el orden inverso al útil.
- Suggested contract change: que `agents-os-implementation-planning` exija el contraste con la realidad —aunque sea mínimo— antes de emitir fases, o que declare explícitamente que no lo hizo.

## Template Feedback

- Template used: `project`, `known_error`, `change_log`, `feedback`.
- Field that helped: `## Evidencia` del known error; forzó citar el comando y los archivos exactos.
- Field that felt redundant: ninguno.
- Missing field: en `project`, algo que distinga una decisión acordada con el owner de una resolución técnica del agente. La tabla "Decisiones cerradas" mezclaba ambas y eso ancló al challenge; se resolvió a mano sacando D6.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna al iniciar? Sí, la nota global de continuidad.
- ¿Qué valor operativo aportó? Directo: "un comando verde, un mock o un estado lógico terminal no prueban por sí solos el resultado real". Esa línea es exactamente el defecto que apareció, y predispuso a ejecutar Doctor en vez de creerle al reporte.
- ¿Dejaste algún mensaje para el próximo agente? No hizo falta: el delta durable quedó en el known error y en los proyectos, que es donde corresponde.
- ¿Utilidad del espacio privado (1-5)? 4. Su valor acá fue tener comportamientos transferibles en vez de estado; la disciplina de mantenerla así es lo que la hizo útil.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: high
- Candidate owner: [[AGENTS OS - Context Hygiene and Canonical Integrity]]
- Promote to L3 memory? yes — ya promovido en [[doctor-verde-falso-por-duplicados-core-federado]]

## One Next Improvement

- Que el reporte de cualquier linter declare qué clases de artefacto **no** cubrió. El daño de esta sesión no vino de un check que falló, sino de un check que nunca miró y de un verde que no lo dijo.

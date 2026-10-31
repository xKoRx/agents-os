---
type: feedback
schema_version: 1
scope: session
created: 2026-10-31
updated: 2026-10-31
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
entities:
  - "[[AGENTS OS]]"
  - "[[Polymarket Engine — MVP]]"
related:
  - "[[Preregistration — Prospective Economic Candidate W1-r 2026-10-31]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: minimax/MiniMax-M3.1-Flash
agent_run: "[[2026-10-31-zcode-minimax-m3.1-flash-polymarket-w1r-prospective-prereg]]"
session_goal: Consolidar UN preregistro candidato (DRAFT_NOT_APPROVED) para la próxima prueba exploratoria económica de PE-005-R1, reutilizando el draft W1-q y los planes vigentes, sin ejecutar nada de lo propuesto.
source_session: w1r-prospective-prereg-20261031
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

# Session Feedback - 2026-10-31 - polymarket-w1r-prospective-prereg

## Context

- Agent surface: ZCode
- Agent model: minimax/MiniMax-M3.1-Flash (reportado por el host)
- Agent run: [[2026-10-31-zcode-minimax-m3.1-flash-polymarket-w1r-prospective-prereg]]
- Session goal: consolidar un único candidato de preregistro prospectivo (documental) para la próxima prueba exploratoria económica de Polymarket Engine.
- Main entity: [[Polymarket Engine — MVP]]
- Skills used: agents-os-bootstrap, agents-os-context-retrieval, agents-os-context-scout (inline-fallback), scout-contract, agents-os-session-close, agents-os-session-feedback, agents-os-agent-run-register, agents-os-entity-update.
- Retrieval mode: sin Graphify y sin Glob/Grep en la superficie ⇒ lectura dirigida de archivos y rangos conocidos; scout inline con `dispatch_id=w1r-prereg`.
- Artifacts changed: 1 doc de Sistema 2 creado (candidato W1-r), 2 notas de Sistema 2 editadas (MVP, continuidad), 4 artefactos de evidencia del shot, 5 notas de journal (resumen, feedback de sesión, feedback de scout, agent run, bitácora de entidad).

## Scores

Use 1-5, where 1 is poor and 5 is excellent.

- Startup clarity: 5
- Retrieval usefulness: 4
- Skill fit: 5
- Template fit: 4
- Closeout friction: 3
- Overall confidence: 4

## What Complicated The Session Most

- Observation: el hook denegó varias lecturas y comandos que eran útiles y were autoritativos para el encargo (fuentes W1-o/W1-j del vault, `internal/regimes/feeresolver.go`, `70-templates/doc.md`, `crew/ZCode.md`, `ls`, `grep`, `awk`, y un Bash compuesto de Git+fecha).
- Why it was hard: el contrato del scout exige separar `declarado`, `observado` e `inferido`; con lecturas denegadas, el pack tenía que citar las notas canónicas alternativas en vez de la fuente primaria, y eso se tuvo que declarar explícitamente en vez de resolverlo.
- Proposed improvement: permitir en el perfil del hook las lecturas de `internal/regimes/*.go` y `70-templates/*.md` (ya son superficie de lectura autorizada para el autor documental) y una forma separada para `git status`/`rev-parse`/`date` que no se pueda encadenar.

## Most Useful Part Of Sistema 1

- What helped: el contrato de scout (`scout-contract.md`) y el runbook del context-scout, que obligan a devolver request/result/facts/gaps con referencia por hecho y a no tratar el pack como memoria canónica.
- Why it helped: evitó dos trampas reales de esta sesión: elegir la regla de L por resultados y presentar el bound lineal histórico como si fuera el modelo documentado.
- Keep/change: mantener; agregar una línea que diga explícitamente qué hacer cuando la fuente primaria de un hecho está denegada (citar la nota canónica equivalente y marcarlo como cita, no como lectura directa).

## Least Useful Or Noisy Part

- What did not help: el materializador y el contrato de esquema exigieron una pasada extra de edición de frontmatter sobre notas recién materializadas (`project`, `related`, `tags`, `entities`) que el template deja vacíos.
- Why it was weak/noisy: el template `doc.md`/`session-summary.md` no expone los campos de routing que estas notas necesitan (`project`, `entities`, `related`), así que la edición posterior es esperable pero no está documentada en la skill.
- Proposed cleanup: documentar en `agents-os-entity-update` que el relleno de routing post-materialización es normal, o añadir esos campos ya poblados al template `doc`.

## Missing Support

- Problem not solved by Sistema 1: no hay ninguna forma canónica de **consolidar** varios documentos canónicos en un único documento derivado sin duplicar su autoridad; esta sesión lo resolvió con un mapa de fuentes explícito (`source-map.json`) y una regla de "una sola autoridad", pero ese patrón no está en ninguna skill.
- How Sistema 1 could help next time: una nota de patrón en `80-agents/memory/public/pattern/` para "consolidación documental con una sola autoridad y mapa de fuentes", reutilizable en cualquier dominio.
- Suggested artifact type: pattern (S1).

## Retrieval Feedback

- Useful query or source: las secciones canónicas del MVP (tareas W1-nR…W1-p y bitácora) y el bloque «Cierre» de la continuidad concentraban casi todo lo que había que reutilizar, sin necesidad de re-derivarlo.
- Missing context: las notas `Research — Target Fee Inventory W1-o` y `Research — Single Episode Public Pilot W1-j` estaban fuera de la allowlist del hook; el contenido equivalente sí estaba disponible en MVP y continuidad, pero sólo de forma resumida.
- Duplicate/noisy result: el plan W1-j contiene bloques de actualización sucesivos (lotes 2 y 3) que se solapan con su §1–§5; leerlo completo obliga a reconciliar historia con estado vigente.
- Better future query: leer primero la bitácora del MVP y el último bloque «Cierre» de la continuidad para fijar el estado vigente, y recién después abrir el documento de plan por las secciones que falten.

## Skill Feedback

- Skill that worked well: `agents-os-context-scout` con su runbook: el patrón «fuente + sección/rango + revisión» evitó convertir una lectura parcial en una afirmación completa.
- Skill that was confusing: `agents-os-session-close` no contemplate explícitamente el caso «el usuario pide un entregable documental Y notas de cierre»: su disparador es por pedido explícito de cierre, y aquí el cierre vino incluido en el encargo.
- Trigger/routing gap: la ruta de cierre y la ruta de entrega documental compiten por el mismo turno; conviene que el encargo del autor documental indique explícitamente qué notas de journal produce.
- Suggested contract change: en `agents-os-session-close`, aclarar que cuando el encargo del turno ya nombra los artefactos de cierre exigidos, la skill se ejecuta sin pedir confirmación adicional.

## Template Feedback

- Template used: `70-templates/doc.md` (vía `materialize_schema_note.py doc`).
- Field that helped: `type: doc` + `status` obligatorios más `## Propósito` / `## Contenido` / `## Fuentes` obligatorios, que dieron una estructura estable a un documento largo.
- Field that felt redundant: `aliases` vacío por defecto y `related` vacío: ambos hubo que poblarlos manualmente después de materializar.
- Missing field: un campo que marque explícitamente el estado `DRAFT_NOT_APPROVED`; hoy sólo existe en el cuerpo, y `status` está limitado por el contrato a `active|archived`, así que un candidato no aprobado y vigente queda indistinguible de un documento aprobado por frontmatter.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? [sí]
- ¿Qué valor operativo aportó para esta sesión (continuidad, detalles crudos, advertencias)? Aportó la advertencia de no recortar contexto útil por un techo fijo y la de separar terminalidad lógica de drenaje físico; ninguna otra nota interna era pertinente a un encargo documental de este tipo.
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna? No: el delta de esta sesión es estado y decisión de proyecto, que pertenecen a las notas canónicas de Sistema 2, no a la memoria interna.
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad? 4; para un trabajo como éste sirve sobre todo por la advertencia de "no persistir historia", y sería más útil si admitiera una nota de checkpoint por proyecto con el estado de la decisión pendiente.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: medium
- Candidate owner: principal / responsable del hook de superficie
- Promote to L3 memory? defer

## One Next Improvement

- Registrar en el runbook del context-scout una regla de degradación explícita para el caso «fuente primaria denegada por el hook»: citar la nota canónica equivalente, marcarla como cita en el pack y no inferir el valor faltante.

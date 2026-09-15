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
  - "[[doctor-verde-falso-por-duplicados-core-federado]]"
aliases: []
agent_surface: "[[Codex]]"
agent_model: unknown
agent_run: "[[2026-09-14-codex-unknown-agents-os-domain-decoupling]]"
session_goal: Implementar la autoridad federada única y desacoplar dominios del core de AGENTS OS
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

# Session Feedback - 2026-09-14 - desacoplamiento de dominio

## Context

- Agent surface/model/run: Codex / unknown / [[2026-09-14-codex-unknown-agents-os-domain-decoupling]].
- Session goal/main entity: implementar PHASE 3.5 en [[AGENTS OS]].
- Skills used: bootstrap, project workflow, entity lifecycle, agent-run register, session feedback y session close.
- Retrieval mode/artifacts: lectura dirigida del planner y contratos; cambios en autoridad federada, hot path, export y providers.
- Review outcome: validación adversarial independiente reproducida; se retiró una excepción muerta del allowlist y se hizo explícito el trade-off de `[[Personal]]` como fallback portable.

## Scores

- Startup clarity: 5; Retrieval usefulness: 5; Skill fit: 5.
- Template fit: 3; Closeout friction: 3; Overall confidence: 4.

## What Complicated The Session Most

- Observation: la primera implementación convirtió “artefacto construido” en “hot path construido”. Eso dejó fuera seis memorias scoped y templates capaces de reproducir tags, áreas y paths de dominios ausentes.
- Why it was hard: fuente y export podían dar Doctor verde porque los links resolvían en el vault fuente y Doctor no materializa templates; el defecto sólo aparece en el contexto receptor.
- Proposed improvement: todo export debe validar metadata de routing y materializar cada tipo canónico en un vault DEFAULT temporal. Un gate textual es complementario, no evidencia suficiente.

## Most Useful Part Of Sistema 1

- What helped: el planner de Context Hygiene ya contenía alcance, ownership, gates y el consenso adversarial exacto.
- Why it helped / keep: permitió reabrir sólo el acceptance gate defectuoso sin reabrir la propuesta descartada; mantener el patrón planner único + provider owns semantics.

## Least Useful Or Noisy Part

- What did not help: tratar un grep sobre startup como sustituto del contexto de instalación DEFAULT.
- Why / cleanup: el builder ahora prueba ambos niveles: referencias estructuradas pre-render y entidades materializadas post-render.

## Missing Support

- Problem: el provider de Canonical corre sobre la fuente y no puede observar por sí solo un artefacto derivado en un contexto receptor.
- How to help / artifact: conservar el gate como responsabilidad del builder y hacer que PHASE 4 reporte su evidencia sin duplicar su lógica.

## Retrieval Feedback

- Useful source: proyecto Context Hygiene, known error y `sources.list`.
- Missing/duplicate: ninguna carencia bloqueante; los duplicados fueron eliminados.
- Better future query: CL-21 dirigido antes de abrir dos candidatos del mismo artefacto federado.

## Skill Feedback

- Worked well: project workflow y session close.
- Confusing/gap: session close ocurrió antes de que la revisión adversarial verificara el alcance completo; hubo que reabrir y corregir la evidencia durable.
- Suggested change: al documentar un default portable, registrar también cómo falla en el vault del owner; “resuelve” no implica “rutea al dominio correcto”.

## Template Feedback

- Template: change_log, agent_run y feedback.
- Helped/redundant/missing: provenance y validación ayudaron; no se detectó un campo material faltante.

## Memoria Interna (Internal Memory)

- Sí, se consultó en cold start; aportó la regla transferible de no confundir un verde lógico con prueba física.
- No se escribió continuidad privada: proyecto, known error y change log contienen el delta durable.
- Utilidad: 5/5; mantenerla libre de estado de proyecto hizo que fuera directamente aplicable.

## Pain Pattern Candidate

- Is this likely to repeat? yes; suggested severity: high; candidate owner: core-export.
- Promote to L3 memory? no: el known error y el builder ya contienen detección y mitigación ejecutable.

## One Next Improvement

- Exponer en PHASE 4 el resultado del build/materialization gate sin trasladar ni reimplementar su semántica.

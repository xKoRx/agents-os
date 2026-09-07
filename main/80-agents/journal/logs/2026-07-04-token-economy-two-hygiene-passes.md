---
type: change_log
scope: global
created: 2026-07-04
updated: 2026-07-04
area: "[[Personal]]"
project: "[[Economía de Tokens]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agent-constitution]]"
  - "[[2026-07-04-system1-broad-consistency-audit]]"
tags:
  - kind/changelog
  - area/personal
  - project/agents-os
---

# 2026-07-04 — Economía de Tokens: 2 pasadas de higiene (Evidencia + hermes-skill)

Cierre de los dos pendientes menores de [[Economía de Tokens]] flageados en
[[2026-07-04-system1-broad-consistency-audit]].

## 1. Compactar `## Evidencia` inflada en learnings de AGENTS OS

Causa raíz ya estaba corregida en el template `learning.md` (Evidencia = cita, no prosa).
Pasada per-file con juicio sobre `memory/public/learning/agents-os/` (NO en masa): cada
`## Evidencia` quedó como cita (fuente + prueba concreta irreemplazable), cortando la
re-narración del aprendizaje ya destilado arriba.

- Compactadas (7): `diff-audit-diagnostic-leftovers`, `human-views-must-explicitly-exclude-agent-tasks`,
  `manual-validation-vs-automated-healthcheck-policy`, `ownership-retrofit-scope-by-open-status`,
  `pr-branch-clean-reconstruction`, `preserve-legacy-semantics-when-extending-feature`,
  `verify-parent-child-project-ownership-before-splitting-content`.
- **Evidencia real preservada** en cada una: SHA `5996a3af99f4`, SDK `polycardVersion 8.179.0`,
  nombres de clase/método, citas literales del owner, rutas de log.
- Fuera de scope (sin sección `## Evidencia`): `official-docs-memory-boundary`,
  `surface-external-repo-policy-conflicts-before-writing`.

## 2. Reclasificar `hermes-dashboard-recovery` (runbook vestido de skill)

Era `type: skill` en `80-agents/skills/` pero: (a) no se invoca —la skill viva está fuera del
vault—, (b) duplicaba el runbook canónico `[[dashboard-hermes-agent]]` (Sistema 2), (c)
contaminaba el namespace de skills. Nunca estuvo en `skills/INDEX.md`.

Decisión del owner: **puente delgado**. Acciones:

- **Deprecada/eliminada** la skill `80-agents/skills/hermes-dashboard-recovery/SKILL.md`.
- **Creado** puente `type: index` en `80-agents/memory/public/reference/hermes-dashboard-recovery.md`:
  nodo buscable sin procedimiento duplicado, que enruta al skill vivo externo + al runbook
  canónico. Honra "una fuente canónica por hecho".
- `skills/INDEX.md`: sin cambios (nunca la listó).
- Referencias al path externo `~/.hermes/.../` en `[[dashboard-hermes-agent]]` y el learning
  systemd apuntan a la skill viva: se dejan intactas (son correctas).

## Validación

- 7 learnings: `## Evidencia` = cita con link; aprendizaje intacto en `## Aprendizaje`.
- `hermes-dashboard-recovery` ya no aparece bajo `80-agents/skills/`; puente presente en
  `memory/public/reference/`. Un agente fresco ya no lo carga como skill invocable.
- Pendiente: reindex de Graphify (cierre de sesión).

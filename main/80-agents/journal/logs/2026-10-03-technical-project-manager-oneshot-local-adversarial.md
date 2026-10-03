---
type: change_log
schema_version: 1
scope: session
created: "2026-10-03"
updated: "2026-10-03"
area:
project:
application:
entities: []
related:
  - "[[technical-project-manager]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Technical Project Manager — one-shot + local adversarial correction

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `30-resources/agents/skills/technical-project-manager/SKILL.md`

## Motivo

- Corregir la política de superficies: el review adversarial de implementación debe ser LOCAL porque debe crear y ejecutar E2E/falsification tests contra la implementación real.
- Formalizar RESEARCHER como función con dos modos CLOUD: SEARCH y DEEPRESEARCH.
- Hacer ONE-SHOT obligatorio para todo worker despachado por master prompt o subagente directo.
- Hacer feedback + session-close de Agents-OS obligatorio al final de cada worker ONE-SHOT.
- Mantener PRIMARY MANAGER y SUBMANAGER como coordinadores multi-turn; son la única excepción al auto-close por ejecución.
- Corregir TOP a GPT-6 Sol en CLOUD y LOCAL.

## Fuentes usadas

- Decisión explícita del Owner, 2026-10-03.
- OpenAI Help — ChatGPT Search: búsqueda rápida de información reciente con fuentes.
- OpenAI Help — Deep Research: investigación multi-step, multi-source, más profunda y documentada.
- `80-agents/skills/agents-os-skill-authoring/SKILL.md`
- `80-agents/memory/public/runbook/agents-os-skill-authoring.md`
- `80-agents/skills/_shared/skill-contract.md`

## Resolución aplicada

- GOD = GPT-6 Astra — CLOUD / LOCAL.
- TOP = GPT-6 Sol — CLOUD / LOCAL.
- NORMAL = GLM-5.3-Flash — LOCAL.
- Shot 2 adversarial = LOCAL ONLY; debe intentar botar la implementación mediante pruebas independientes E2E/adversariales/falsification.
- CLOUD review puede complementar Shot 2, nunca reemplazarlo.
- RESEARCHER/SEARCH = lookup actual/narrow/rápido.
- RESEARCHER/DEEPRESEARCH = investigación amplia/multi-source/documentada.
- Todo worker = fresh-context ONE-SHOT + persistencia requerida + agent-run cuando aplica + feedback + session-close + handoff.
- PRIMARY MANAGER / SUBMANAGER = coordinadores; permanecen abiertos hasta cierre explícito del Owner.

## Validación

- No quedan referencias a GPT-5.6 Sol en la skill.
- Existe mapping TOP=GPT-6 Sol.
- Shot 2 declara LOCAL ONLY.
- Excepción ONE-SHOT limitada a PRIMARY MANAGER y SUBMANAGER coordinadores.
- SEARCH y DEEPRESEARCH aparecen como modos distintos de RESEARCHER.
- CLOUD ya no declara adversarial implementation review como capacidad equivalente.
- Commit de skill: `93e6f749416f06b693225248393a3b48ca915027`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos ni paths locales.

## Rollback

- Revertir `93e6f749416f06b693225248393a3b48ca915027` si una decisión canónica posterior reemplaza esta política.

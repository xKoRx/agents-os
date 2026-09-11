---
type: change_log
schema_version: 1
scope: session
created: "2026-09-11"
updated: "2026-09-11"
area: "[[Aranea]]"
project: "[[AGENT-PLATFORM - MCP Access Plane]]"
application:
entities:
  - "[[Aranea]]"
related: []
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
  - area/aranea
  - tech/mcp
---

# Aranea MCP skill refactor — 2026-09-11

## Cambio

- **Tipo:** created / updated / deleted
- **Archivo(s):**
  - `xKoRx/symphony/.agents/skills/aranea-mcps-expert/SKILL.md` — creado como fuente canónica agent-facing del capability plane Aranea.
  - `xKoRx/symphony/.agents/skills/aranea-mcps-expert/RUNBOOK.md` y `runbooks/{SSH,POSTGRES,MONGODB}.md` — creados para procedimientos operativos por familia.
  - `xKoRx/symphony/.agents/skills/echo-forge-wfm-troubleshooting/{SKILL.md,RUNBOOK.md}` — refactorizados para conservar sólo routing/conocimiento de dominio y delegar MCP.
  - runbooks MCP duplicados bajo `echo-forge-wfm-troubleshooting/runbooks/` — eliminados.
  - `xKoRx/symphony/docs/prd/echo-forge/POSTGRES-MCP-ACCESS.md` — actualizado para apuntar al experto MCP.
  - `main/80-agents/skills/INDEX.md` — registry federado actualizado.
  - `main/10-projects/Aranea/AGENT-PLATFORM/agentes/AGENT-PLATFORM - MCP Access Plane.md` — T4 MongoDB cerrado y decisiones/estado sincronizados.

## Motivo

- El conocimiento de uso de capabilities MCP estaba repartido dentro de una skill de dominio Echo Forge, creando duplicación y riesgo de drift.
- Se necesitaba una única autoridad reutilizable para SSH/PostgreSQL/MongoDB del homelab, con boundary explícito Aranea-only y prohibición de uso en MELI/corporativo.

## Fuentes usadas

- `main/80-agents/skills/agents-os-skill-authoring/SKILL.md`
- `main/80-agents/memory/public/runbook/agents-os-skill-authoring.md`
- `main/80-agents/skills/_shared/skill-contract.md`
- `main/80-agents/skills/_shared/schema-contract.md`
- proyecto canónico `[[AGENT-PLATFORM - MCP Access Plane]]`
- implementación/runtime MCP validada durante T2/T3/T4.

## Resolución aplicada

- `aranea-mcps-expert` posee selección de capability, least privilege, boundaries y handoff a runbooks específicos.
- `echo-forge-wfm-troubleshooting` posee exclusivamente routing de dominio/evidence ownership.
- El registry federado enlaza la fuente app-owned sin copiarla.
- T4 queda cerrado y el siguiente carril funcional es T5 Temporal MCP.

## Validación

- Skills releídas desde `master` tras escritura.
- Se verificó ausencia de referencias remanentes a los runbooks MCP eliminados mediante búsqueda en `xKoRx/symphony`.
- El proyecto canónico fue releído después de la actualización y conserva T0/T2/T3/T4 cerrados con T1 WIP y T5 siguiente.
- Limitación de superficie: esta sesión operó vía GitHub connector; no hubo ejecución local de `materialize_schema_note.py`, lint AGENTS OS ni reindex de Graphify. Por lo tanto, no se declara un gate mecánico local que no fue ejecutado.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin bearer tokens, passwords, private keys ni secretos finales.

## Rollback

- Revertir commits de `xKoRx/symphony` que crean/refactorizan `aranea-mcps-expert` y restaurar los tres runbooks MCP previos dentro de `echo-forge-wfm-troubleshooting`; revertir registry/proyecto en `xKoRx/agents-os` si el ownership centralizado se rechaza.
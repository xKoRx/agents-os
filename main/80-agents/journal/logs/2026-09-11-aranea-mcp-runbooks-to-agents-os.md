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
related:
  - "[[aranea-mcps-expert]]"
  - "[[aranea-ssh-mcp]]"
  - "[[aranea-postgres-mcp]]"
  - "[[aranea-mongodb-mcp]]"
  - "[[aranea-mcp-capability-plane]]"
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

# Aranea MCP runbooks → AGENTS OS — 2026-09-11

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated / deleted
- **Archivo(s):**
  - `30-resources/agents/skills/aranea-mcps-expert/SKILL.md` — skill canónica promovida al vault (no al core `80-agents/skills/`).
  - `80-agents/memory/public/runbook/aranea-ssh-mcp.md` — creado; procedimiento SSH MCP extraído de Symphony.
  - `80-agents/memory/public/runbook/aranea-postgres-mcp.md` — creado; procedimiento PostgreSQL MCP extraído de Symphony.
  - `80-agents/memory/public/runbook/aranea-mongodb-mcp.md` — creado; procedimiento MongoDB MCP extraído de Symphony.
  - `80-agents/memory/public/runbook/aranea-mcp-capability-plane.md` — creado; troubleshooting del plano MCP extraído de Symphony.
  - `80-agents/skills/INDEX.md` — skill registrada en transversales; quitada de app-owned Symphony.
  - `10-projects/Aranea/AGENT-PLATFORM/agentes/AGENT-PLATFORM - MCP Access Plane.md` — D20, estado, links y bitácora sincronizados.
  - `xKoRx/symphony/.agents/skills/aranea-mcps-expert/SKILL.md` — reducido a pointer de discovery hacia el vault.
  - `xKoRx/symphony/.agents/skills/aranea-mcps-expert/RUNBOOK.md` y `runbooks/{SSH,POSTGRES,MONGODB}.md` — eliminados tras la promoción.
  - `xKoRx/symphony/.agents/skills/echo-forge-wfm-troubleshooting/{SKILL.md,RUNBOOK.md}` y `docs/prd/echo-forge/POSTGRES-MCP-ACCESS.md` — handoff actualizado al vault.

## Motivo

- `aranea-mcps-expert` es transversal de Aranea, no core AGENTS OS ni skill de una sola app. Debía vivir en el vault bajo `30-resources/agents/skills/`, con runbooks en Sistema 1.

## Fuentes usadas

- `xKoRx/symphony` `origin/master`: `.agents/skills/aranea-mcps-expert/{SKILL.md,RUNBOOK.md,runbooks/SSH.md,runbooks/POSTGRES.md,runbooks/MONGODB.md}`
- `80-agents/skills/agents-os-skill-authoring/SKILL.md`
- `80-agents/memory/public/runbook/agents-os-skill-authoring.md`
- `80-agents/skills/_shared/note-types.md`
- `80-agents/skills/_shared/schema-contract.md`
- proyecto canónico `[[AGENT-PLATFORM - MCP Access Plane]]`

## Resolución aplicada

- La skill permanece en `xKoRx/symphony` y sigue decidiendo capability, least privilege y boundary Aranea-only.
- Cada familia MCP tiene un runbook canónico en `80-agents/memory/public/runbook/`.
- El troubleshooting del plano MCP (cliente/proxy/auth) quedó separado de los runbooks de backend.
- D20 fija que no se vuelven a copiar esos procedimientos en el repo owner.

## Validación

- `materialize_schema_note.py` creó las cinco notas canónicas (4 runbooks + change_log) sin overwrite.
- `validate_schema_contract.py --type runbook|change_log` y `lint.py --strict` sobre el delta de AGENTS OS se ejecutan en el mismo cambio.
- En el worktree Symphony `chore/aranea-mcp-runbooks-to-agents-os` (base `origin/master`, sin mezclar F-04) no quedan referencias a `aranea-mcps-expert/runbooks/` ni a `aranea-mcps-expert/RUNBOOK.md`.
- Activación: skill app-owned en Symphony; runbooks Sistema 1 en AGENTS OS.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin bearer tokens, passwords, private keys ni secretos finales.

## Rollback

- Restaurar los cuatro archivos de runbook en `xKoRx/symphony/.agents/skills/aranea-mcps-expert/` y revertir el handoff de la skill, el PRD PostgreSQL, el INDEX y D20 del proyecto MCP Access Plane. Borrar las cuatro notas nuevas de `80-agents/memory/public/runbook/` si se revierte la promoción.

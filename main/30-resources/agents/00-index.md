---
type: index
schema_version: 1
status: active
icon: 🗂️
slug: "00-index-index"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: "2026-08-10"
updated: "2026-09-12"
reviewed: "2026-09-12"
aliases:
  - "00-index index"
cssclasses:
  - wide
tags:
  - kind/index
---

# 🗂️ Agents — Índice

> [!info] Wiki compilada de recursos
> Este índice es el catálogo curado del dominio `30-resources/agents/`. Ver [[30-resources/00-RESOURCE-WIKI|Reglas de la Resource Wiki]] y `log.md`.

## 📊 De un vistazo

- **Páginas curadas:** 21
- **Última ingesta:** 2026-09-12
- **Estado:** active

## 📂 Catálogo

| Página | Una línea | Meta |
|---|---|---|
| [[agent-executor]] | Prompt reusable para encargar una fase acotada sin sustituir el planificador canónico. | target: agent · v1 |
| [[f3-skill-migration]] | Inventario, checksums y rollback del movimiento de skills de Fase 3. | migration record |
| [[30-resources/agents/skills/meli-agent-dev/SKILL|meli-agent-dev]] | Router del dominio Meli: boundary, preferencias scoped y skill especializada por tarea. | skill · Meli-only |
| [[30-resources/agents/skills/aranea-agent-dev/SKILL|aranea-agent-dev]] | Router del dominio Aranea (homelab); puerta única del acceso MCP vía aranea-mcps-expert. | skill · Aranea-only |
| [[30-resources/agents/skills/aranea-mcps-expert/SKILL|aranea-mcps-expert]] | Router agent-facing para elegir ambiente/capability MCP de Aranea y cargar el runbook canónico correcto. | skill · Aranea-only |
| [[30-resources/agents/skills/signals-code-review/SKILL|signals-code-review]] | Code review Meli con Zord; en Signals/RIO agrega el revisor independiente `rjara-rio-impact`. | skill · Meli-only |
| [[30-resources/agents/skills/signals-func-spec-authoring/SKILL|signals-func-spec-authoring]] | Specs funcionales de Signals/Ads en Spellbook con convenciones del equipo. | skill · Meli-only |
| [[30-resources/agents/skills/signals-tech-spec-authoring/SKILL|signals-tech-spec-authoring]] | Specs técnicas de Signals/Ads y design docs backend RIO (DD-N, marcadores de cambio). | skill · Meli-only |
| [[30-resources/agents/skills/pr-description/SKILL|pr-description]] | Descripciones de PR con evidencia real, materializadas como recurso del proyecto. | skill · transversal |
| [[30-resources/agents/skills/human-first-technical-writing/SKILL|human-first-technical-writing]] | Narrativa técnica causal que reduce la carga cognitiva del lector. | skill · transversal |
| [[30-resources/agents/skills/fury-lib-consumer-deploy/SKILL|fury-lib-consumer-deploy]] | Publica versiones test de librerías Java con Fury e importa las versiones en consumidores. | skill · Meli-only |
| [[30-resources/agents/skills/sync-local-branch/SKILL|sync-local-branch]] | Sincroniza ramas Git exclusivamente locales con merge conservador. | skill · transversal |
| [[30-resources/agents/skills/sdd-workflow/SKILL|sdd-workflow]] | Clasifica y ejecuta fases SDD sin mezclarlas. | skill · transversal |
| [[30-resources/agents/skills/e2e-gated-validation/SKILL|e2e-gated-validation]] | Validación E2E como secuencia de gates con evidencia y PASS/FAIL por gate. | skill · transversal |
| [[30-resources/agents/skills/release-certification/SKILL|release-certification]] | Certifica que release/binario corresponde al source autorizado. | skill · transversal |
| [[30-resources/agents/skills/deployment-proof/SKILL|deployment-proof]] | Demuestra que el runtime ejecuta la release nueva; exit 0 no es prueba. | skill · transversal |
| [[30-resources/agents/skills/readonly-production-probe/SKILL|readonly-production-probe]] | Probes read-only temporales contra sistemas reales con cleanup obligatorio. | skill · transversal |
| [[30-resources/agents/skills/distributed-incident-triage/SKILL|distributed-incident-triage]] | Triage forense multi-subsistema con timeline común y primer punto de divergencia. | skill · transversal |
| [[30-resources/agents/skills/evidence-channel-discovery/SKILL|evidence-channel-discovery]] | Descubre y persiste los canales de evidencia reales por pregunta. | skill · transversal |
| [[30-resources/agents/skills/write-once-conflict-triage/SKILL|write-once-conflict-triage]] | Triage de conflictos write-once: duplicate/race/stale/contract-defect. | skill · transversal |
| [[30-resources/agents/skills/operational-healthcheck-policy/SKILL|operational-healthcheck-policy]] | Cuándo validar manualmente componentes vigilables y cuándo confiar en la automatización. | skill · transversal |

## 🔗 MCP Aranea y dominios de agente

El acceso MCP de Aranea es exclusivo del dominio [[30-resources/agents/skills/aranea-agent-dev/SKILL|aranea-agent-dev]], cuya única puerta MCP es `aranea-mcps-expert` (`30-resources/agents/skills/aranea-mcps-expert/SKILL.md`). Sus runbooks mecánicos viven en `30-resources/runbooks/` (dominio Runbooks): `aranea-ssh-mcp.md`, `aranea-postgres-mcp.md`, `aranea-mongodb-mcp.md`, `aranea-hasura-mcp.md` y `aranea-mcp-capability-plane.md`. El dominio corporativo equivalente es [[30-resources/agents/skills/meli-agent-dev/SKILL|meli-agent-dev]]; los dos routers se excluyen mutuamente.

Desde 2026-09-12 las skills de dominio y transversales viven aquí (migradas desde `80-agents/skills/`, que quedó reservado a comportamientos de AGENTS OS); el catálogo operativo completo vive en `80-agents/skills/INDEX.md`.

## 🔗 Links

- [[30-resources/00-RESOURCE-WIKI|Reglas de la Resource Wiki]]
- `log.md` — bitácora cronológica de este dominio

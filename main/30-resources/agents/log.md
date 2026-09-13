# Agents resource log

## [2026-08-10] ingest | AGENTS OS Fase 3 → dominio agents

- Se activó `30-resources/agents/` con su índice, contrato de prompt reusable y registro de migración F3.

## [2026-08-10] ingest | AGENTS OS Fase 3 → ownership y discovery

- Se migraron las dos skills app-owned pendientes a `xKoRx/symphony`, se actualizó el registry federado y el pack, y el forward-test terminó sin fallas.

## [2026-08-11] lint | Auditoría base de AGENTS OS Fase 4

- Cobertura del índice completa; contrato superficie×modelo revisado; Graphify limpio y actualizado.

## [2026-09-11] ingest | Aranea MCP capability plane

- Se actualizó `aranea-mcps-expert` para seleccionar primero ambiente y luego capability: data PROD=RO y DEV=RW; se documentó explícitamente que los runbooks viven en `80-agents/memory/public/runbook/` y se alinearon los runbooks PostgreSQL, MongoDB, SSH y capability-plane con el estado verificado.

## [2026-09-12] ingest | Restructura de skills: core agents-os vs federadas

- Se movieron 13 skills no-agents-os desde `80-agents/skills/` a `30-resources/agents/skills/` (signals-*, pr-description, human-first-technical-writing, y las 8 de evidencia/validación); el core quedó reservado a comportamientos de AGENTS OS.
- Se crearon los routers de dominio `meli-agent-dev` y `aranea-agent-dev` (excluyentes entre sí); `aranea-mcps-expert` quedó subordinada a `aranea-agent-dev` como única puerta MCP de Aranea.
- `80-agents/skills/INDEX.md` se reescribió en formato índice wiki (core + registro federado enlazado); este `00-index.md` incorporó las 18 skills como filas del catálogo.

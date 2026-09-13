# Runbooks resource log

## [2026-09-12] ingest | Activación del dominio y mudanza desde AGENTS OS

- Dominio activado explícitamente con `00-index.md` + `log.md`.
- Se movieron desde `80-agents/memory/public/runbook/` los runbooks de dominios/aplicaciones: 5 de Aranea (`aranea-ssh-mcp`, `aranea-postgres-mcp`, `aranea-mongodb-mcp`, `aranea-hasura-mcp`, `aranea-mcp-capability-plane`), 2 de Meli (`signals-code-review-runbook`, `resolver-versiones-java-sin-construir-via-fury-nexus`), `stager-windows-mt5-cutover-and-occupieddrain`, `2026-07-25-fix-pack-for-gate-handoff-review` y la subcarpeta `symphony/` (8 runbooks de Echo Forge).
- Quedaron en `80-agents/memory/public/runbook/` sólo los de AGENTS OS: `agents-os-skill-authoring`, `graphify-obsidian-install`, `reindex-bloqueado-por-deuda-global`, `resource-wiki-lint-reindex`, `delegacion-a-subagentes`.
- `signals-code-review.md` se marcó `status: superseded` con `superseded_by: [[signals-code-review-runbook]]`: variante anterior del mismo día con los mismos aliases; la canónica es la versión con gate Meli y `rjara-rio-impact`.
- Referencias de path actualizadas en `aranea-mcps-expert`, `signals-code-review` (skill), `30-resources/aranea/02-servicios/ml-ia.md` y `30-resources/agents/00-index.md`.

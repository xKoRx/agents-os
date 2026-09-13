---
type: index
schema_version: 1
status: active
icon: 📋
slug: "runbooks-index"
area: "[[Personal]]"
created: "2026-09-12"
updated: "2026-09-12"
reviewed: "2026-09-12"
aliases:
  - "runbooks index"
  - "índice de runbooks"
cssclasses:
  - wide
tags:
  - kind/index
---

# 📋 Runbooks — Índice

> [!info] Wiki compilada de recursos
> Runbooks operativos de dominios y aplicaciones; activado explícitamente como dominio de la [[30-resources/00-RESOURCE-WIKI|Resource Wiki]] el 2026-09-12. Los runbooks de AGENTS OS (comportamiento del sistema) viven en `80-agents/memory/public/runbook/`; los de cada app viven junto a su dominio cuando ese dominio los posee. Un runbook es la parte mecánica validada (pasos, verificación, rollback); el criterio vive en su skill.

## 📊 De un vistazo

- **Runbooks curados:** 15 (+1 superseded, 8 en `symphony/`)
- **Última ingesta:** 2026-09-12
- **Estado:** active

## 📂 Catálogo

| Runbook | Una línea | Dominio |
|---|---|---|
| [[30-resources/runbooks/aranea-ssh-mcp|aranea-ssh-mcp]] | Ejecución mecánica de la capability MCP SSH de Aranea (viewer/operator). | Aranea |
| [[30-resources/runbooks/aranea-postgres-mcp|aranea-postgres-mcp]] | Uso de las capabilities PostgreSQL RO/RW de Aranea (Echo). | Aranea |
| [[30-resources/runbooks/aranea-mongodb-mcp|aranea-mongodb-mcp]] | Uso de las capabilities MongoDB RO/RW de Aranea (Echo Forge). | Aranea |
| [[30-resources/runbooks/aranea-hasura-mcp|aranea-hasura-mcp]] | Superficie certificada Hasura PROD RO y administración DEV. | Aranea |
| [[30-resources/runbooks/aranea-mcp-capability-plane|aranea-mcp-capability-plane]] | Plano de capabilities MCP: discovery, auth, transporte y policy. | Aranea |
| [[30-resources/runbooks/signals-code-review-runbook|signals-code-review-runbook]] | Ejecución mecánica del code review Meli con Zord y `rjara-rio-impact`; gate humano único. | Meli |
| [[30-resources/runbooks/resolver-versiones-java-sin-construir-via-fury-nexus|resolver-versiones-java-sin-construir-via-fury-nexus]] | Resolver versiones Java publicadas vía Fury/Nexus sin construir. | Meli |
| [[30-resources/runbooks/stager-windows-mt5-cutover-and-occupieddrain|stager-windows-mt5-cutover-and-occupieddrain]] | Cutover Windows de stager MT5 con occupied/drain. | stager |
| [[30-resources/runbooks/Descripciones de PR — recurso del proyecto en el vault|Descripciones de PR]] | Materializar la descripción de PR como recurso del proyecto en el vault. | transversal |
| [[30-resources/runbooks/Signals - Escribir specs funcionales (SIG)|Signals — Escribir specs funcionales (SIG)]] | Mecánica de escritura de specs funcionales SIG en Spellbook. | Meli/Signals |
| [[30-resources/runbooks/agents_os_github_sync|agents_os_github_sync]] | Sync del vault al repo GitHub agents-os. | vault ops |
| [[30-resources/runbooks/hermes_obsidian_livesync_troubleshooting|hermes_obsidian_livesync_troubleshooting]] | Setup y troubleshooting de Hermes + Obsidian LiveSync. | vault ops |
| [[30-resources/runbooks/symphony-zeus-troubleshooting|symphony-zeus-troubleshooting]] | Troubleshooting del remote worker Symphony/Zeus. | Symphony |
| [[30-resources/runbooks/2026-07-25-fix-pack-for-gate-handoff-review|2026-07-25-fix-pack-for-gate-handoff-review]] | Pase de fix para handoffs de gate rechazados en review (Echo Forge). | Echo Forge |

### `symphony/` — Echo Forge (SQX)

| Runbook | Una línea |
|---|---|
| [[30-resources/runbooks/symphony/echo-forge-cross-system-triage|echo-forge-cross-system-triage]] | Triage cruzado de sistemas Echo Forge. |
| [[30-resources/runbooks/symphony/echo-forge-golden-e2e|echo-forge-golden-e2e]] | Ejecución del golden E2E de Echo Forge. |
| [[30-resources/runbooks/symphony/echo-forge-workers-shared-access|echo-forge-workers-shared-access]] | Acceso compartido a workers de Echo Forge. |
| [[30-resources/runbooks/symphony/plugin-java-deployment-via-setup-echoforge-projects|plugin-java-deployment-via-setup-echoforge-projects]] | Deploy de plugins Java vía setup de proyectos EchoForge. |
| [[30-resources/runbooks/symphony/remote-worker-file-manipulation|remote-worker-file-manipulation]] | Manipulación de archivos en el remote worker. |
| [[30-resources/runbooks/symphony/symphony-prod-probe|symphony-prod-probe]] | Probe read-only de producción Symphony. |
| [[30-resources/runbooks/symphony/symphony-release-certification|symphony-release-certification]] | Certificación de release Symphony. |
| [[30-resources/runbooks/symphony/symphony-worker-runtime-proof|symphony-worker-runtime-proof]] | Prueba de que el worker corre la release nueva. |

## 🔗 Reglas del dominio

- **AGENTS OS vs dominios:** los runbooks que cambian el comportamiento del propio AGENTS OS (`agents-os-skill-authoring`, `graphify-obsidian-install`, `reindex-bloqueado-por-deuda-global`, `resource-wiki-lint-reindex`, `delegacion-a-subagentes`) viven en `80-agents/memory/public/runbook/`; este dominio aloja los de dominios y aplicaciones.
- La parte de criterio de cada runbook vive en su skill federada (`30-resources/agents/skills/`); aquí va sólo la mecánica.
- Naming canónico según `90-system/convenciones.md`; los wikilinks de esta página apuntan al nombre canónico.

## 🔗 Links

- [[30-resources/00-RESOURCE-WIKI|Resource Wiki — reglas del formato]]
- `log.md` — bitácora cronológica de este dominio

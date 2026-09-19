---
type: index
schema_version: 1
status: active
icon: 📋
slug: "runbooks-index"
area: "[[Personal]]"
created: "2026-09-12"
updated: "2026-09-18"
reviewed: "2026-09-17"
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
> Runbooks operativos de dominios y aplicaciones; activado explícitamente como dominio de la [[30-resources/00-RESOURCE-WIKI|Resource Wiki]] el 2026-09-12. Los runbooks de AGENTS OS (comportamiento del sistema) viven en `80-agents/memory/public/runbook/`; los de cada app viven junto a su dominio cuando ese dominio los posee. Un runbook contiene mecánica validada (pasos, verificación, rollback); el criterio vive en su skill.

## 📊 De un vistazo

- **Runbooks curados:** 25 (+1 superseded, 8 en `symphony/`); se incorporan `proxmox-lifecycle-operator-contract`, `linux-container-operator-contract`, `windows-operator-contract` y `service-lifecycle-operator-contract` (2026-09-18).
- **Última ingesta:** 2026-09-18.
- **Estado:** active.

## 📂 Catálogo

| Runbook | Una línea | Dominio |
|---|---|---|
| [[30-resources/runbooks/hermes-linux-update-recovery|hermes-linux-update-recovery]] | Update/recovery de Hermes en Linux: systemd user, perfiles, mixed sys.modules, fleet marker, gateways y validación funcional. | Aranea/Hermes |
| [[30-resources/runbooks/proxmox-lifecycle-operator-contract|proxmox-lifecycle-operator-contract]] | Contrato del futuro operador Proxmox H2: canales API/SSH, recursos protegidos, precondiciones, rollback y abort (enablement-only, no autoriza operaciones). | Aranea |
| [[30-resources/runbooks/linux-container-operator-contract|linux-container-operator-contract]] | Contrato del futuro operador Linux/containers H3: canales por target (SSH nativo, qm guest cmd host-mediated, MCP consumidor), Docker/systemd, recursos protegidos, rollback y abort (enablement-only). | Aranea |
| [[30-resources/runbooks/windows-operator-contract\|windows-operator-contract]] | Contrato del operador Windows H3+W1: admin nativa CERTIFICADA por SSH (ariadna-win, from=.122, host key pinneada) sobre worker-kronos VM 135 — alcance limitado a esa VM; canales, validación, revoke/rollback; flota Windows restante sin canal. | Aranea |
| [[30-resources/runbooks/service-lifecycle-operator-contract|service-lifecycle-operator-contract]] | Contrato del futuro operador de servicios H3: systemd system/user, Docker/Compose, Task Scheduler, ownership del servicio, validación semántica y rollback (enablement-only). | Aranea |
| [[30-resources/runbooks/aranea-ssh-mcp|aranea-ssh-mcp]] | SSH Aranea: viewer/operator, `docker-echo-dev-operator` y evidence publisher Windows ACTIVE/CERTIFIED. | Aranea |
| [[30-resources/runbooks/aranea-postgres-mcp|aranea-postgres-mcp]] | PostgreSQL RO/RW Aranea (Echo). | Aranea |
| [[30-resources/runbooks/aranea-mongodb-mcp|aranea-mongodb-mcp]] | MongoDB RO/RW Aranea (Echo Forge). | Aranea |
| [[30-resources/runbooks/aranea-hasura-mcp|aranea-hasura-mcp]] | Hasura PROD strict-RO (3 tools) y DEV admin. | Aranea |
| [[30-resources/runbooks/aranea-kafka-mcp|aranea-kafka-mcp]] | Kafka DEV admin; PROD diferido. | Aranea |
| [[30-resources/runbooks/aranea-flink-mcp|aranea-flink-mcp]] | Flink/StateFun DEV REST + host operator; PROD diferido. | Aranea |
| [[30-resources/runbooks/aranea-mcp-capability-plane|aranea-mcp-capability-plane]] | Discovery, onboarding, auth, transporte/policy; 13 capabilities registradas, certificación diferenciada por cliente. | Aranea |
| [[30-resources/runbooks/aranea-observability-mcp|aranea-observability-mcp]] | ARGUS Grafana/Prometheus/Loki RO, sin Jaeger toolset. | Aranea |
| [[30-resources/runbooks/aranea-temporal-mcp|aranea-temporal-mcp]] | Temporal SQX RO, 28 tools, namespaces allowlisted, sin mutadores. | Aranea |
| [[30-resources/runbooks/aranea-minio-mcp|aranea-minio-mcp]] | MinIO RO: IAM scoped deploy/worker/sqx y examples; backups y escritura denegados. ACTIVE 2026-09-17. | Aranea |
| [[30-resources/runbooks/aranea-etcd-mcp|aranea-etcd-mcp]] | etcd RO: prefixes allowlisted y secret-names excluidos, sin writes. ACTIVE 2026-09-17; hardening cluster separado. | Aranea |
| [[30-resources/runbooks/signals-code-review-runbook|signals-code-review-runbook]] | Code review Meli con Zord y `rjara-rio-impact`; gate humano único. | Meli |
| [[30-resources/runbooks/resolver-versiones-java-sin-construir-via-fury-nexus|resolver-versiones-java-sin-construir-via-fury-nexus]] | Resolver versiones Java Fury/Nexus sin construir. | Meli |
| [[30-resources/runbooks/stager-windows-mt5-cutover-and-occupieddrain|stager-windows-mt5-cutover-and-occupieddrain]] | Cutover Windows de stager MT5 con occupied/drain. | stager |
| [[30-resources/runbooks/Descripciones de PR — recurso del proyecto en el vault|Descripciones de PR]] | Descripción de PR como recurso del proyecto. | transversal |
| [[30-resources/runbooks/Signals - Escribir specs funcionales (SIG)|Signals — Escribir specs funcionales (SIG)]] | Escritura de specs funcionales SIG en Spellbook. | Meli/Signals |
| [[30-resources/runbooks/agents_os_github_sync|agents_os_github_sync]] | Sync vault → GitHub agents-os. | vault ops |
| [[30-resources/runbooks/hermes_obsidian_livesync_troubleshooting|hermes_obsidian_livesync_troubleshooting]] | Troubleshooting Hermes + Obsidian LiveSync. | vault ops |
| [[30-resources/runbooks/symphony-zeus-troubleshooting|symphony-zeus-troubleshooting]] | Troubleshooting worker Symphony/Zeus. | Symphony |
| [[30-resources/runbooks/2026-07-25-fix-pack-for-gate-handoff-review|2026-07-25-fix-pack-for-gate-handoff-review]] | Fix para handoffs de gate rechazados en review Echo Forge. | Echo Forge |

### `symphony/` — Echo Forge (SQX)

| Runbook | Una línea |
|---|---|
| [[30-resources/runbooks/symphony/echo-forge-cross-system-triage|echo-forge-cross-system-triage]] | Triage cruzado Echo Forge. |
| [[30-resources/runbooks/symphony/echo-forge-golden-e2e|echo-forge-golden-e2e]] | Golden E2E Echo Forge. |
| [[30-resources/runbooks/symphony/echo-forge-workers-shared-access|echo-forge-workers-shared-access]] | Acceso compartido histórico a workers; preferir MCP cuando cubra operación. |
| [[30-resources/runbooks/symphony/plugin-java-deployment-via-setup-echoforge-projects|plugin-java-deployment-via-setup-echoforge-projects]] | Deploy plugin Java EchoForge. |
| [[30-resources/runbooks/symphony/remote-worker-file-manipulation|remote-worker-file-manipulation]] | Archivos en remote worker. |
| [[30-resources/runbooks/symphony/symphony-prod-probe|symphony-prod-probe]] | Probe RO producción Symphony. |
| [[30-resources/runbooks/symphony/symphony-release-certification|symphony-release-certification]] | Certificación de release Symphony. |
| [[30-resources/runbooks/symphony/symphony-worker-runtime-proof|symphony-worker-runtime-proof]] | Prueba del worker corriendo release. |

## 🔗 Reglas del dominio

- Runbooks del propio AGENTS OS (`agents-os-skill-authoring`, `graphify-obsidian-install`, `reindex-bloqueado-por-deuda-global`, `resource-wiki-lint-reindex`, `delegacion-a-subagentes`) permanecen en `80-agents/memory/public/runbook/`; aquí viven procedimientos de dominios/aplicaciones.
- Criterios de routing en skills federadas `30-resources/agents/skills/`; sólo mecánica en runbooks. Naming y links según `90-system/convenciones.md`.
- Para accesos específicos de coding agents Echo/Forge en Daedalus, consultar [[Daedalus — Development Agents MCP Access & Gaps]] antes de proponer una capability nueva. No confundir gateway Telegram Hermes con MCP certificado para coding agents.

## 🔗 Links

- [[30-resources/00-RESOURCE-WIKI|Resource Wiki — reglas del formato]]
- [[Daedalus — Development Agents MCP Access & Gaps]] — inventario y gaps de acceso por operación
- `log.md` — bitácora cronológica del dominio
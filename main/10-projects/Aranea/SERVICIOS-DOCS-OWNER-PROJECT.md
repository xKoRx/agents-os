---
title: "Servicios — Documentación Operativa por Servicio (Pausado)"
type: project
schema_version: 1
status: paused
icon: 📚
slug: servicios-docs-owner-project
area: "[[Aranea]]"
project:
created: 2026-07-02
updated: 2026-08-10
activated: 2026-07-02
paused: 2026-07-02
owner: me
root: true
priority: P1
progress: 10
aliases:
  - Servicios docs
  - Per-service docs
  - Documentación servicios Aranea
tags:
  - kind/project
  - area/aranea
  - domain/documentation
related:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
  - "[[30-resources/aranea/02-servicios/README]]"
  - "[[30-resources/aranea/00-index]]"
  - "[[2026-07-02-022-deferred-service-docs]]"
---

# 📚 Servicios — Documentación Operativa por Servicio (Deferred)

> [!warning] Status: **DEFERRED** — sin plazo de ejecución
> Este proyecto documenta la **iniciativa** de generar docs operativas por servicio individual (no por categoría). NO se ejecuta hasta que el owner lo apruebe y defina plazo.
>
> **Trigger**: owner dijo "anótalas por ahí como servicios disponibles. quizás estaría bueno documentar cada uno en el second brain, para tener el acceso a todo ahí bien enlazado. qué dices? (déjalo como tarea para más adelante)"

## 🎯 Objetivo

Crear **una nota de Second Brain por servicio crítico** de Aranea, con:
- Propósito real (qué hace, no solo nombre)
- Acceso concreto (URL Traefik, ssh tunnel, API endpoint, dashboard)
- Storage asociado (datasets, volúmenes, secrets)
- Procedimientos (restart, logs, health check, owner-only ops)
- Cross-refs al ticket Backup/DR (tier classification, secrets_refs)

> [!warning] Corrección crítica 2026-07-02 (owner)
> **Aranea NO es un homelab hobby. Es un datacenter para el sistema de trading algorítmico "echo".** Sin esto no hay homelab. Esta verdad define el scope del proyecto: documentar los servicios fundamentales que sostienen el sistema echo, NO hacer gap analysis exhaustivo de toda la infra.

Servicios target — **scope definido por owner el 2026-07-02**, clasificados por capa:

### Tier 0a — Infraestructura base (sin estos NADA funciona)

| # | VMID | Nombre | Nodo | Razón |
|---|---|---|---|---|
| 1 | 130 | opnsense | athena | gateway/firewall — control plane absoluto |
| 2 | 149 | pi-hole | athena | DNS |
| 3 | 115 | traefik | athena | reverse proxy |

### Tier 0b — Storage (sobre la capa base)

| # | VMID | Nombre | Nodo | Razón |
|---|---|---|---|---|
| 4 | 145 | truenas | hades | storage para TODOS los servicios |

### Tier 0c — Cluster quorum crítico (warning feo si baja de 3)

| # | VMID | Nombre | Nodo | Razón |
|---|---|---|---|---|
| 5 | 101 | etcd-athena | athena | etcd member — quorum |
| 6 | 147 | etcd-hades | hades | etcd member — quorum |
| 7 | 154 | etcd-kronos | kronos | etcd member — quorum |
| 8 | 155 | etcd-hera | hera | etcd member — quorum |
| 9 | 156 | etcd-zeus | zeus | etcd member — quorum |
| 10 | 148 | etcd-keeper | hades | UI keeper — NO cuenta para quorum |
| 11 | 136 | kafka-hera | hera | kafka broker |
| 12 | 138 | kafka-kronos | kronos | kafka broker |
| 13 | 139 | kafka-zeus | zeus | kafka broker |

> **etcd**: el cluster debe mantenerse **siempre con 5 nodos**, **NUNCA menos de 3** (bajar de 3 = "warning feo" según owner). Cada LXC de etcd en cada nodo forma parte del cluster.

### Tier 0d — Sistema echo (trading algorítmico)

| # | VMID | Nombre | Nodo | Razón |
|---|---|---|---|---|
| 14 | 124 | mt4-real | hades | cuenta real — producción crítica |
| 15 | 133 | mt4-ftmo | hades | FTMO prop firm |
| 16 | 134 | mt4-ttp | hades | TTP trend following |
| 17 | 144 | mt4-demo | hades | demo (parte del sistema echo) |
| 18 | 140 | echo | hades | orquestador del sistema |
| 19 | 152 | postgresql | hades | DB relacional — alimenta echo |
| 20 | 153 | mongodb | hades | DB documental — alimenta echo |
| 21 | 160 | argus | hades | observabilidad general (paneles, monitores de todo) |
| 22 | 126 | docker-flink | hades | stream processing (consumer del cluster kafka que alimenta echo) |
| 23 | 129 | docker-hasura | hades | capa GraphQL sobre postgres para echo |

### Tier 1+ — Resto (NO es la idea documentarlos ahora)

Servicios que **NO entran al scope inicial** de este proyecto:
- mcps, obsidian-sync, docker-observability, emqx, frigate, homeassistant, ubuntu-dev, temporal, sqx-ulab-*, win-*, docker-kafka, etc.

Estos quedan **fuera del scope** del proyecto deferred. Si el owner en el futuro pide incluirlos, se reabre el ticket 022.

**Total scope inicial**: **23 servicios tier 0** (3 infra + 1 storage + 9 quorum + 10 echo). Sin análisis mío adicional — esta lista es lo que vos nombraste.

## 📊 Estado actual

- Pausado por decisión del owner; el proyecto hijo completó tres notas Tier 0a de veintinueve acciones y no continúa sin autorización explícita.

## 📂 Entregables (cuando se active)

### Estructura de cada nota de servicio

Template único (`70-templates/service-operational.md` a crear cuando se active):

```markdown
---
title: "<nombre-servicio>"
type: service-doc
status: active | partial | draft
vmid: <id>
node: <host>
tier: 0 | 1 | 2 | 3
owner: rodrigo
aliases:
  - <alias1>
  - <alias2>
tags:
  - service-doc
  - aranea
  - kind/service-doc
  - area/aranea
---

# <Servicio>

## 🎯 Propósito
[Qué hace realmente, no solo el nombre]

## 🌐 Acceso
- URL pública (vía Traefik):
- URL interna (LAN IP:port):
- SSH:
- API endpoint:
- Dashboard:

## 💾 Storage
- Datasets / volúmenes:
- Mount paths:
- Backups:

## 🔐 Secrets
- Refs a `[[20-areas/Aranea#Secret-Zero]]`:
- API keys / tokens:

## 🔧 Operación
- Restart:
- Health check:
- Logs:
- Update:

## 📊 Observabilidad
- Métricas Prometheus:
- Alertas Grafana:

## 🚨 Incidentes
- Runbooks:
- Known errors:

## 🔗 Cross-refs
- [[BACKUP-DR-DESIGN]] — tier, backup policy
- [[<servicios-relacionados>]]
```

### Ubicación de las notas

**Decisión pendiente**: cuándo se active, decidir entre:
- `30-resources/aranea/02-servicios/<servicio>.md` (junto al catálogo por categoría, mismo folder)
- `30-resources/services/<servicio>.md` (folder nuevo a crear)

**Recomendación del agente**: opción A — mismo folder, junto al catálogo. Mantiene locality.

## 📂 Estructura del proyecto

```
10-projects/Aranea/
└── SERVICIOS-DOCS-OWNER-PROJECT.md           (este archivo)

agentes/
└── agent-project-09-service-docs-rollout.md   (subproyecto agente)

05-tickets/
└── 2026-07-02-022-deferred-service-docs.md    (ticket formal)
```

## ✅ Tareas

- [ ] [[agent-project-09-service-docs-rollout]] reactivar + seguimiento #owner/me #type/supervision #area/aranea

1. **Aprobar inicio** del proyecto y dar plazo estimado.
2. **Priorizar los 22 servicios** identificados en el gap analysis (tier 0 primero → tier 3 último).
3. **Definir template canónico** (`70-templates/service-operational.md`) — base ya propuesta en sección "Estructura de cada nota de servicio".
4. **Resolver secretos**: para servicios con secrets_refs (ej. step-ca, postgres, mongo), el owner debe confirmar acceso vía Secret Zero antes de que el agente documente.

## ⚠️ Restricciones aplicadas

1. **NO consumir tiempo del owner ahora** — el proyecto está deferred. No tocar docs existentes ni pedir input.
2. **NO contaminar 02-servicios/** — hasta que se active, no se agregan archivos de servicio individual.
3. **Capex $0, opex $0** — sigue la regla Aranea.
4. **Secret Zero discipline** — cuando se ejecute, el agente NUNCA escribe secrets en docs; solo referencias.

## 🛣️ Roadmap (no activado)

```
Fase 0 (al activarse)            → crear 70-templates/service-operational.md
Fase 1 (cuando owner apruebe)   → Tier 0a (3 servicios: opnsense, pi-hole, traefik)
Fase 2                           → Tier 0b (1 servicio: truenas)
Fase 3                           → Tier 0c (9 servicios: etcd cluster + kafka cluster)
Fase 4                           → Tier 0d (8 servicios: mt4-demo/real/ftmo/ttp + echo + postgres + mongo + argus)
Fase 5                           → cross-refs con BACKUP-DR-DESIGN y backup policy
```

> [!danger] Regla de scope estricta
> El agente **NO documenta servicios fuera de los 21 tier 0** sin autorización explícita del owner. Si durante la ejecución surge la tentación de documentar mcps, flink, emqx, frigate, etc., se reporta al owner y se espera luz verde.

## 🔗 Links

- [[BACKUP-DR-OWNER-PROJECT]] — proyecto hermano (activo, awaiting 018-021)
- [[30-resources/aranea/02-servicios/README]] — catálogo por categoría (referencia, no se modifica)
- [[2026-07-02-022-deferred-service-docs]] — ticket formal
- [[agent-project-09-service-docs-rollout]] — subproyecto agente

## 📝 Convention

- **Proyecto deferred** → `10-projects/Aranea/` con `status: deferred`, `priority: P3`
- **Subproyecto agente** → `agentes/` con `parent: "[[SERVICIOS-DOCS-OWNER-PROJECT]]"`
- **Ticket formal** → `05-tickets/YYYY-MM-DD-NNN-slug.md`
- **Logs de cambio** → `80-agents/journal/logs/`

## 📆 Bitácora

- **2026-08-10** — Parent migrado a `project` v1 para soportar contractualmente el hijo `owner: agent`; se preservó la pausa y se creó su tarea puente humana en To Do.

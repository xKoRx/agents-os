---
title: "agent-project-09 — Rollout de docs operativas por servicio"
type: project
schema_version: 1
owner: agent
root: false
status: paused
status_detail: "PAUSADO 2026-07-02 por owner: 'No avances más con SERVICIOS-DOCS. Prioridad única = Backup/DR'. Tier 0a (3 notas partial) queda en disco; no se continúa hasta nueva orden."
slug: agent-project-09-service-docs-rollout
area: "[[Aranea]]"
project: "[[AGENTS OS]]"
parent: "[[SERVICIOS-DOCS-OWNER-PROJECT]]"
created: 2026-07-02
updated: 2026-08-10
priority: P3
progress: 10
aliases:
  - agent-project-09
  - ap-09
tags:
  - kind/project
  - area/aranea
  - project/agents-os
  - agent/owner
  - domain/documentation
related:
  - "[[2026-07-02-022-deferred-service-docs]]"
  - "[[30-resources/aranea/02-servicios/README]]"
---

# agent-project-09 — Rollout de docs operativas por servicio

> [!warning] Status: **PAUSED** (no activado)
> Este subproyecto NO se ejecuta hasta que el owner apruebe el proyecto padre `[[SERVICIOS-DOCS-OWNER-PROJECT]]`.

## 🎯 Objetivo

Generar una **nota canónica por servicio** en el Second Brain, con template uniforme y cross-refs al sistema Backup/DR.

## 📊 Estado actual

- Pausado por instrucción del owner; tres notas Tier 0a están creadas y el resto no se reactiva sin autorización explícita.

## ✅ Tareas

> [!danger] Regla de scope estricta
> El agente **NO documenta servicios fuera de los 21 tier 0** sin autorización explícita del owner. Esta lista la define el owner, no el agente.

### Fase 0 — Setup

- [ ] Crear `70-templates/service-operational.md` (template canónico).
- [ ] Validar template con un servicio piloto (sugerencia: opnsense vm 130, base de la infra).
- [ ] Confirmar con owner el folder destino (recomendado: `30-resources/aranea/02-servicios/`).

### Fase 1 — Tier 0a: Infraestructura base (3 servicios)

Sin estos NADA funciona:

- [x] **opnsense** (vm 130, athena) — gateway/firewall, control plane absoluto — **NOTA CREADA 2026-07-02** `[[30-resources/aranea/02-servicios/opnsense]]`
- [x] **pi-hole** (vm 149, athena) — DNS — **NOTA CREADA 2026-07-02** `[[30-resources/aranea/02-servicios/pi-hole]]`
- [x] **traefik** (vm 115, athena) — reverse proxy — **NOTA CREADA 2026-07-02** `[[30-resources/aranea/02-servicios/traefik]]`

### Fase 2 — Tier 0b: Storage (1 servicio)

Sobre la capa base:

- [ ] **truenas** (vm 145, hades) — storage para TODOS los servicios

### Fase 3 — Tier 0c: Cluster quorum crítico (9 servicios)

**etcd**: siempre con 5 nodos, NUNCA menos de 3 (bajar de 3 = "warning feo").

- [ ] **etcd-athena** (vm 101, athena) — quorum member
- [ ] **etcd-hades** (vm 147, hades) — quorum member
- [ ] **etcd-kronos** (vm 154, kronos) — quorum member
- [ ] **etcd-hera** (vm 155, hera) — quorum member
- [ ] **etcd-zeus** (vm 156, zeus) — quorum member
- [ ] **etcd-keeper** (vm 148, hades) — UI keeper (NO cuenta para quorum)
- [ ] **kafka-hera** (vm 136, hera) — broker
- [ ] **kafka-kronos** (vm 138, kronos) — broker
- [ ] **kafka-zeus** (vm 139, zeus) — broker

### Fase 4 — Tier 0d: Sistema echo (8 servicios)

El core del trading algorítmico. Aranea = datacenter para esto.

- [ ] **mt4-real** (vm 124, hades) — cuenta real
- [ ] **mt4-ftmo** (vm 133, hades) — FTMO prop firm
- [ ] **mt4-ttp** (vm 134, hades) — TTP trend following
- [ ] **mt4-demo** (vm 144, hades) — demo
- [ ] **echo** (vm 140, hades) — orquestador
- [ ] **postgresql** (vm 152, hades) — DB relacional
- [ ] **mongodb** (vm 153, hades) — DB documental
- [ ] **argus** (vm 160, hades) — observabilidad general (paneles, monitores de todo)
- [ ] **docker-flink** (vm 126, hades) — stream processing (consumer kafka)
- [ ] **docker-hasura** (vm 129, hades) — capa GraphQL sobre postgres

### Fase 5 — Cross-refs

- [ ] Actualizar `02-servicios/README.md` con links a cada nota individual.
- [ ] Cross-ref con `BACKUP-DR-DESIGN.md` (tier classification, backup policy).
- [ ] Cross-ref con `agent-project-00` (policy cleanup) si aplica.

## 🛠️ Workflow por servicio

Para cada servicio, el agente debe:

1. **Verificar existencia** vía `agent-read pvesh get /cluster/resources --vmid <id>` (no modificar nada).
2. **Inspeccionar config** vía `qm config <vmid>` o `pct config <vmid>` (read-only).
3. **Identificar servicios internos** vía `agent-read running_services --node <host>` (si aplica).
4. **Preguntar al owner** lo que NO se pueda inferir:
   - Propósito real (ej: argus — qué hace exactamente?)
   - URLs de acceso (ej: dashboard URL, ruta Traefik)
   - Credenciales/secrets (NUNCA pedir el secret, pedir solo el **path de referencia**)
5. **Escribir la nota** desde el template `70-templates/service-operational.md`.
6. **Commit log** en `80-agents/journal/logs/`.

## 🔐 Política de secretos

- El agente **NUNCA** escribe API keys, tokens, passwords en las notas.
- Solo referencias: `[[secret-zero → pcloud-service-account]]`, `[[secret-zero → pbs-api-token]]`, etc.
- Las URLs internas con secretos embebidos (ej. `postgres://user:pass@host`) se redactan como `postgres://USER:PASS@host → ver Secret Zero → postgresql-prod-password`.

## ⚠️ Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Servicios desconocidos (argus, echo) requieren discovery | Preguntar al owner ANTES de escribir la nota; no inventar |
| Secrets filtrados a docs | Redacción sistemática + revisión owner antes de commit |
| Inventario desactualizado entre refresh | Re-ejecutar `agent-read` antes de cada nota; usar timestamp |
| Conflictos con docs existentes en `02-servicios/` | Las nuevas notas NO reemplazan las viejas; coexisten (catálogo + individuales) |
| Owner ausente por tiempo prolongado | Ticket formal con plazo; agente reporta estado cada N notas |

## 📊 Métricas de éxito

- 23 servicios tier 0 documentados al cierre del proyecto (3 + 1 + 9 + 10).
- 0 secrets en plaintext en las notas.
- Cross-refs bidireccionales con Backup/DR.
- Inventario base actualizado al día del último refresh.

## 🔗 Links

- [[SERVICIOS-DOCS-OWNER-PROJECT]] — proyecto padre
- [[2026-07-02-022-deferred-service-docs]] — ticket formal
- [[30-resources/aranea/02-servicios/README]] — catálogo por categoría (referencia)
- [[30-resources/aranea/00-index]] — índice general Aranea

## 📝 Convention

- Subproyectos agente → `10-projects/Aranea/agentes/` con `parent: "[[Proyecto padre]]"`
- `status: pending` significa "no activado"; cambiar a `in-progress` cuando el owner apruebe inicio

## 📆 Bitácora

- **2026-08-10** — Migrado de `agent-project` legacy a `project` v1 conservando la pausa del owner; progress queda en `10` por tres acciones completadas de veintinueve.

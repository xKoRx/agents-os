---
title: "agent-project-06 — Observability and alerting"
type: project
schema_version: 1
owner: agent
root: false
status: paused
status_detail: "Legacy ready, pero no autorizado para ejecución por el owner."
priority: P2
progress: 0
icon: 📊
slug: agent-project-06-observability-and-alerting
area: "[[Aranea]]"
project: "[[AGENTS OS]]"
created: 2026-07-01
updated: 2026-08-10
tags:
  - kind/project
  - area/aranea
  - project/agents-os
  - agent/owner
  - domain/backup
related:
  - "[[BACKUP-DR-DESIGN]]"
parent: "[[BACKUP-DR-OWNER-PROJECT]]"
cssclasses: wide
---

# 📊 Agent Project 06: Observability and alerting

## 🎯 Objetivo

Integrar el sistema de backup con el stack de observabilidad existente (`docker-observability` en hades). Implementar las 16 alertas mínimas definidas en BACKUP-DR-DESIGN §8.2 con thresholds y canales.

## 📊 Estado actual

- Pausado y listo para ejecución sólo cuando el owner habilite el proyecto padre; ninguna tarea del agente está completada.

## Scope

- 16 alertas con thresholds.
- Integración con `docker-observability` (Prometheus + Grafana si existen, o lo que haya).
- Canales: Telegram owner + email + dashboard banner.
- Runbook links en cada alerta.

## Out of scope

- Crear nuevo stack Prometheus/Grafana desde cero (gap #6 del roadmap, fuera de alcance backup).
- Alertas no-listadas en BACKUP-DR-DESIGN §8.2.

## Required inputs

- ap-02 (PBS operativo, fuente de métricas).
- ap-03, ap-04, ap-05 (cada script expone exit code y log).

## Required owner permissions

- Acceso a canal Telegram del owner (configuración bot).
- Acceso email relay (SMTP) si se usa canal email.
- Acceso a `docker-observability` para agregar scrape targets.

## Required credentials / secrets

- Telegram bot token (en Secret Zero).
- SMTP credentials (si aplica).

## Required maintenance window

No estricto.

## Dependencies

- ap-02, ap-04, ap-05 (todos los jobs emiten señales).

## Protected resources

Ninguno.

## Risks

| Riesgo | Mitigación |
|---|---|
| Alert storm (muchas alertas simultáneas) | Rate limiting por alerta. |
| Telegram bot caído | Fallback a email. |
| False positives frecuentes | Thresholds calibrados después de 30d de datos. |

## Safety gates

- Solo lectura sobre Prometheus/Grafana.
- Cambios a alerting rules pasan por review.

## Implementation plan

1. Identificar stack actual en `docker-observability`.
2. Crear alert rules en formato Prometheus (16 alertas).
3. Configurar Alertmanager con rutas Telegram + email.
4. Crear dashboard Grafana con estado de backups.
5. Wire cada script de backup (ap-01/03/04/05) a Pushgateway o textfile collector para emitir métricas.
6. Validar con `promtool test rules`.

## Validation plan

- Cada alerta se puede forzar (trigger manual).
- Telegram recibe mensaje.
- Dashboard Grafana muestra métricas.

## Rollback plan

- `git revert` de alert rules.
- Alertmanager config revert.

## Evidence to collect

- Screenshots dashboard.
- Trigger manual de cada alerta.
- Ticket cerrado.

## Expected artifacts

- 16 alert rules.
- Alertmanager config.
- Dashboard Grafana.
- Ticket ap-06 cerrado.

## Definition of Done

- [ ] 16 alertas activas.
- [ ] Trigger manual PASS.
- [ ] Telegram recibe mensajes.
- [ ] Dashboard poblado.

## Linked owner tasks

Ninguno urgente (config Telegram puede esperar).

## ✅ Tareas

- [ ] **AGENT-TASK-06-1**: identificar stack observability actual.
  - tags: [agent, discovery]

- [ ] **AGENT-TASK-06-2**: crear 16 alert rules Prometheus.
  - tags: [agent, config]

- [ ] **AGENT-TASK-06-3**: configurar Alertmanager routes.
  - tags: [agent, config]

- [ ] **AGENT-TASK-06-4**: crear dashboard Grafana.
  - tags: [agent, dashboard]

- [ ] **AGENT-TASK-06-5**: wire scripts backup → métricas.
  - tags: [agent, integration]

- [ ] **AGENT-TASK-06-6**: validar con trigger manual.
  - tags: [agent, validation]

---

## Requirements

### Functional requirements
- FR-001: 16 alertas activas con thresholds.
- FR-002: Canales Telegram + email.
- FR-003: Dashboard Grafana con estado.

### Non-functional requirements
- NFR-001: Rate limiting en alertas.
- NFR-002: Thresholds calibrados después de 30d.

### Safety requirements
- SAFE-001: Solo lectura sobre stack existente.

### Observability requirements
- OBS-001: Cada alerta tiene runbook link.
- OBS-002: Severidades correctas (critical/warning).

### Documentation requirements
- DOC-001: Cada alerta documentada en BACKUP-DR-DESIGN §8.2.

### Acceptance criteria
- AC-001: 16 alertas forzadas PASS.
- AC-002: Telegram recibe al menos 1 mensaje por canal.

---

**Status**: ready. NO ejecutado.
**Sesión cerrada por instrucción del owner**: 2026-07-01.

## 📆 Bitácora

- **2026-08-10** — Migrado de `agent-project` legacy a `project` v1 sin activar la ejecución; owner, parent, lifecycle, progress, tags y secciones quedaron contractuales.

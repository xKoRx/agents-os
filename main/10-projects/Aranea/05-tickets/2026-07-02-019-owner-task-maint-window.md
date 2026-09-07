---
id: 2026-07-02-019
title: "OWNER-TASK — Declarar ventana de mantenimiento preferida"
type: action
schema_version: 1
status: todo
status_detail: "Bloqueante para ap-02 (crear VM PBS interrumpe brevemente kronos). F-06, F-07."
severity: medium
icon: 🎫
slug: 2026-07-02-019-owner-task-maint-window
area: "[[Aranea]]"
project: "[[AGENTS OS]]"
created: 2026-07-02
updated: 2026-08-10
owner: me
aliases:
  - ticket 019
  - OWNER-TASK-MAINT-WINDOW
tags:
  - kind/action
  - area/aranea
  - project/agents-os
  - action/owner
related:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
  - "[[agent-project-02-pbs-on-backup-node]]"
---

# 2026-07-02-019 — OWNER-TASK-MAINT-WINDOW

## Descripción

Declarar la ventana de mantenimiento preferida para habilitar la creación y programación del PBS.

## Checklist

- [ ] Completar la tarea del owner y verificar los criterios de aceptación documentados.

## Contexto

`agent-project-02` necesita crear VM PBS (vmid 180) en kronos, descargar ISO, instalar PBS interactivo, registrar storage en 5 PVE nodes. Esto es **DANGEROUS** (clasificado en `dangerous_commands.qm_create`) e interrumpe brevemente el nodo kronos (ZFS pool-kronos y Ceph quorum compartidos en kronos). El agente solo ejecuta dentro de una ventana confirmada por owner.

## Tarea del owner

Declarar:

1. **Día + hora local preferida** (sábado madrugada, domingo noche, otro).
2. **Duración máxima aceptable** (cuánto downtime toleras para kronos).
3. **Owner presente o no presente** durante la ventana (afecta qué pasos son interactivos vs automáticos).
4. **Contacto de emergencia** durante ventana (para abort si algo sale mal).

## Inputs requeridos

- Conocimiento del calendario personal/profesional.
- Conocimiento de carga esperada en kronos (cluster prod, Ceph quorum, etc).

## Outputs esperados

```yaml
maint_window:
  preferred_day: "sabado"      # sábado / domingo / miercoles-am / etc
  preferred_time: "02:00"      # local time
  duration_max_minutes: 120
  owner_present: false         # true/false
  emergency_contact: "telegram @rodrigo"
  notify_telegram_channel: "Home"
```

## Acceptance criteria

- Texto firmado por owner en ticket o chat.
- Agente confirma que la ventana cae en hora de bajo uso (puede usar histórico de `inventory` si lo hubiera).

## Bloquea

- `agent-project-02` PBS setup (Phase 2.1-2.6 en el runbook §1).
- Cualquier cambio DANGEROUS subsiguiente que requiera downtime.

## Riesgo si no se resuelve

- Ap-02 queda en status `ready` para siempre, sin ventana confirmada.
- Owner podría ser interrumpido fuera de horario por emergencia improvisada.

## Consideraciones técnicas

- **Kronos**: 80 threads, 251 GB RAM, Ceph MON/MGR + 2 OSDs + storage PVE. Crear VM 180 (4 vCPU, 8 GB, 32 GB disco) tiene impacto nominal.
- **Ceph quorum**: crear VM no toca Ceph. Pero si el agent necesita `qm create` y por error usa `local-kronos` VG (8.5 TB libres, NO sagrado), OK. `local-sqx-kronos` (931 GB) está en `protected_resources` y NO TOCAR.
- **ZFS pool-kronos** no se ve afectado por crear VM en LVM-VG.
- **Datacenter windows**: si el owner prefiere ventana laboral (09-18h), agendar para cuando no tenga reuniones y Telegraf/grafana esté fuera de horario de equipos pesados.

## Referencias

- BACKUP-DR-OWNER-PROJECT.md §"Tareas del owner"
- agent-project-02 Required inputs
- BACKUP-DR-RUNBOOK.md §1

## Source files

- agent-project-02-pbs-on-backup-node.md
- BACKUP-DR-OWNER-PROJECT.md

## Captured

Ticket creado 2026-07-02 como materialización formal de OWNER-TASK-MAINT-WINDOW listada en BACKUP-DR-OWNER-PROJECT.md.

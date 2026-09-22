---
id: 2026-07-02-018
title: "OWNER-TASK — Confirmar lista tier 0 (VMs críticas)"
type: action
schema_version: 1
status: todo
status_detail: "Bloqueante para ap-02 (PBS schedule vzdump). F-08 segregación cloud. Owner-driven."
severity: medium
icon: 🎫
slug: 2026-07-02-018-owner-task-critical-vms
area: "[[Aranea]]"
project: "[[AGENTS OS]]"
created: 2026-07-02
updated: 2026-08-10
owner: me
aliases:
  - ticket 018
  - OWNER-TASK-CRITICAL-VMS
tags:
  - kind/action
  - area/aranea
  - project/agents-os
  - action/owner
related:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
  - "[[BACKUP-DR-DESIGN]]"
  - "[[agent-project-02-pbs-on-backup-node]]"
  - "[[../../../30-resources/aranea/02-servicios/red]]"
---

# 2026-07-02-018 — OWNER-TASK-CRITICAL-VMS

> [!warning] CONGELACIÓN noche-6 (2026-09-21) — el ticket NO se cierra solo: falta firma owner. La base y los deltas ya están congelados en `~/aranea/work/cierre-preparatorio-20260921/018-MATRIZ-COBERTURA.md` (matriz VM + datos con huecos reales). Deltas aplicados: 162 y 170 ELIMINADAS del universo (qmdestroy owner 20sep 23:58, verificado); 149 condicionado a P5; datos argus (40,5G usados) y kafka ×3 = ÚNICAS decisiones técnicas que faltan (retención vs reconstruible). Respuesta en una línea: `018 = lista OK + argus=<reconstruible|retener> + kafka=<reconstruible|retener>`. Con esa línea este ticket pasa a done y B1 obtiene su exclusión ledger definitiva. La lista de candidatos de abajo queda HISTORICAL (inventario jul-2026).

## Descripción

Confirmar la lista de VMs críticas Tier 0 requerida por el diseño Backup/DR.

## Checklist

- [ ] Completar la tarea del owner y verificar los criterios de aceptación documentados.

## Contexto

El sistema de backup necesita saber qué VMs son **tier 0** (críticas, daily PBS, retención agresiva, drills mensuales) para configurar `vzdump` con la cadencia correcta. Sin esta lista, ap-02 no puede finalizar `jobs.vzdump_tier_0` y `restore_drills.drill_1_vm_pbs`.

## Tarea del owner

Producir lista firmada con **VMID y nombre** de cada VM que entra en tier 0. Criterio sugerido: cualquier VM cuya pérdida cause outage material (servicio productivo, control plane, identity).

## Candidatos sugeridos desde el inventory 2026-07-02

Del inventario materializado en `/home/hermes/aranea/topology/inventory_2026-07-02.json` (57 VMs+LXCs, filtro por `status="running"` y por rol crítico, **owner decide**):

| vmid | name | node | role candidato |
|---|---|---|---|
| 130 | opnsense | athena | gateway/firewall (control plane absoluto) |
| 149 | pi-hole | athena | DNS |
| 115 | traefik | athena | reverse proxy |
| 200 | ca | athena | step-ca (identity / certs) |
| 145 | truenas | hades | storage (single point of data) |
| 152 | postgresql | hades | DB prod |
| 153 | mongodb | hades | DB prod |
| 116 | obsidian-sync | hades | knowledge base |
| 157 | minio | hades | object storage |
| 124 | mt4-real | hades | trading real (no producción crítica cluster-wide, pero owner decide) |
| 134 | mt4-ttp | hades | trading real |
| 133 | mt4-ftmo | hades | trading real |

> El agente NO decide. Solo presenta candidatos basados en `status` + tags. Owner confirma o quita.

## Inputs requeridos

- `inventory_2026-07-02.json` sección `vms` (filtrar por `status="running"` y por tag/role).
- Conocimiento del owner sobre qué VMs son productivas vs lab.

## Outputs esperados

Decisión owner, una de:

1. **Lista confirmada**: `tier_0 = ["vm 130", "vm 149", "vm 152", ...]`, firmada por owner.
2. **Lista alternativa** con criterio: ej. "tier 0 = sólo control plane (opnsense + step-ca + truenas)".
3. **Diferida**: pedir al agente categorizar por tag `tier0` primero, después owner confirma.

## Acceptance criteria

- Lista firmada (chat o ticket decision).
- VMs marcadas con tag `tier0` en Proxmox (de ejecución, en sesión dedicada).
- Backup policy actualiza `tiers.tier_0.candidates_pending_owner` con la lista confirmada.

## Bloquea

- `agent-project-02` PBS `vzdump_tier_0` schedule.
- `agent-project-02` retention policy tier 0.
- `agent-project-07` drill 1 (restore VM tier 0 mensual).

## Riesgo si no se resuelve

- Sin tier 0 definido, ap-02 puede arrancar pero `vzdump` corre contra TODAS las VMs → fail-backup de tier 3 (lab/dev) saturando datastore PBS sin razón.

## Referencias

- BACKUP-DR-OWNER-PROJECT.md §"Tareas del owner"
- BACKUP-DR-DESIGN.md §3 (F-08)
- agent-project-02 Required inputs
- `inventory_2026-07-02.json` (raw capture 2026-07-02)

## Source files

- `/home/hermes/aranea/topology/inventory_2026-07-02.json`
- `/home/hermes/aranea/topology/discovery/*_20260702_033204.txt`

## Captured

Ticket creado 2026-07-02 como materialización formal de OWNER-TASK-CRITICAL-VMS listada en BACKUP-DR-OWNER-PROJECT.md.

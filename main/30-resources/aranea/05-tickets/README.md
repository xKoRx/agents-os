---
type: action
schema_version: 1
project:
status: done
created: 2026-08-10
updated: 2026-08-10
tags:
  - kind/action
  - area/aranea
---

## Descripción

Registro histórico de ejecución para [[Aranea]].

## Checklist

- [x] Resultado histórico preservado

---
title: "05 — Tickets del sistema Aranea (histórico)"
type: index
schema_version: 1
status: archived
icon: 🎫
slug: aranea-tickets-legacy
area: "[[Aranea]]"
project: "[[AGENTS OS]]"
created: 2026-06-29
updated: 2026-07-02
aliases:
  - Aranea tickets
  - Tickets Aranea
tags:
  - kind/index
  - area/aranea
  - project/agents-os
  - topic/tickets
---

# 🎫 05 — Tickets del sistema Aranea (histórico)

## 📊 De un vistazo

> **Capturado**: 2026-06-29..02
> **Convención**: `~/aranea/tickets/YYYY-MM-DD-NNN-topic.md`
>
> **2026-07-02**: los tickets **del proyecto** Backup/DR (018-021) se migraron a `10-projects/Aranea/05-tickets/`. Este folder conserva el **histórico** de tickets operativos del cluster (001-017), que siguen vigentes como referencia de qué se hizo y qué se rompió.
> Los links `[[2026-07-02-018-...]]` siguen resolviendo porque Obsidian matchea por nombre canónico, no por path.

## 📂 Catálogo

### Tickets cerrados (2026-06-29)

| # | ID | Título | Status | Risk | Category |
|---|---|---|---|---|---|
| 1 | [[2026-06-29-001-create-lxc-ca]] | Crear LXC ca-aranea en athena para step-ca | failed | low | create-resource |
| 2 | [[2026-06-29-002-create-lxc-ca-retry]] | Retry crear LXC ca-aranea | failed | low | create-resource |
| 3 | [[2026-06-29-003-create-lxc-ca-retry2]] | Retry2 crear LXC ca-aranea | failed | low | create-resource |
| 4 | [[2026-06-29-004-create-lxc-ca-retry3]] | Retry3 crear LXC ca-aranea | failed | low | create-resource |
| 5 | [[2026-06-29-005-install-step-ca]] | Instalar step-ca en LXC ca-aranea (CTID 200) | **applied** | low | deploy-service |
| 6 | [[2026-06-29-006-configure-traefik-stepca]] | Configurar Traefik con certResolver stepca | **applied** | low | modify-config |
| 7 | [[2026-06-29-007-expose-dashboard-via-traefik]] | Exponer dashboard.lab.aranea via Traefik con TLS step-ca | **applied** | low | deploy-service |
| 8 | [[2026-06-29-008-dashboard-no-password-via-reverse-tunnel]] | Eliminar doble auth dashboard — túnel SSH reverso | **applied** | medium | modify-config |
| 9 | [[2026-06-29-009-setup-obsidian-headless]] | Setup Obsidian headless client + LiveSync | **applied** | medium | deploy-service |

### Tickets cerrados (2026-06-30)

| # | ID | Título | Status | Risk | Category |
|---|---|---|---|---|---|
| 10 | [[2026-06-30-010-aranea-full-docs]] | Documentación canónica completa del cluster Aranea | **applied** | low | documentation |
| 12 | [[2026-06-30-012-unlock-agent-ro-nopasswd]] | Unlock agent_ro NOPASSWD on all 6 nodes + refresh inventory | **applied** | medium | infra+inventory |

### Tickets cerrados (2026-07-01)

| # | ID | Título | Status | Risk | Category |
|---|---|---|---|---|---|
| 14 | [[2026-07-01-014-hermes-dashboard-bind-loopback-after-update]] | Dashboard muerto tras update v0.17.0 — recovery completo (5 fixes) | **closed** | medium | modify-config |

### Tickets abiertos (owner-task de Backup/DR, 2026-07-02)

| # | ID | Título | Status | Risk | Category |
|---|---|---|---|---|---|
| 18 | [[2026-07-02-018-owner-task-critical-vms]] | OWNER-TASK — Confirmar lista tier 0 (VMs críticas) | **open** | medium | owner-task blocking |
| 19 | [[2026-07-02-019-owner-task-maint-window]] | OWNER-TASK — Declarar ventana de mantenimiento preferida | **open** | medium | owner-task blocking |
| 20 | [[2026-07-02-020-owner-task-secret-zero]] | OWNER-TASK — Confirmar ubicación de Secret Zero (caja fuerte + USB cifrado) | **open** | high | owner-task blocking |
| 21 | [[2026-07-02-021-owner-task-oauth-scope]] | OWNER-TASK — Decidir quién ejecuta OAuth flows (pcloud + GDrive) | **open** | high | owner-task blocking |

### Tickets abiertos (dashboard follow-ups, 2026-07-01)

| # | ID | Título | Status | Risk | Category |
|---|---|---|---|---|---|
| 15 | [[2026-07-01-015-dashboard-dns-ariadne-to-traefik]] | DNS dashboard.lab.aranea apunta a Hermes (122) en vez de Traefik (11) | **open** | low | dns |
| 16 | [[2026-07-01-016-hermes-config-version-31-to-32]] | Migrar Hermes config v31 → v32 (gateway_running=false reportado) | **open** | low | upgrade |
| 17 | [[2026-07-01-017-dashboard-healthcheck-script]] | Healthcheck programado para dashboard Hermes | **open** | low | observability |

### Tickets en curso (2026-06-30)

| # | ID | Título | Status | Risk | Category |
|---|---|---|---|---|---|
| 11 | 2026-06-30-011-aranea-storage-audit-backup | Auditoría de storages Aranea + diseño de sistema de backup | approved → pending T2 | low | documentation |
| 13 | 2026-06-30-013-storage-redesign-backup-design | Storage redesign + backup design proposal | **superseded** → ver backup-dr/ | high | design |

## 📊 Resumen

| Métrica | Valor |
|---|---|
| Tickets totales | **17** |
| Applied | 8 (47%) |
| Closed (2026-07-01+) | 1 (6%) — ticket 014 |
| Failed | 4 (24%) — todos del LXC ca-aranea retries |
| Approved (en curso) | 1 (ticket 011) |
| Proposal-pending-approval | 1 (ticket 013) |
| Open (follow-ups) | 3 (tickets 015-017) |
| Rejected | 0 |

## 🎯 Temas cubiertos

- **step-ca**: tickets 001..005 (4 failed + 1 applied)
- **Traefik + TLS interno**: tickets 006, 007, 008
- **Obsidian sync (CouchDB)**: ticket 009
- **Documentación del homelab**: tickets 010, 011
- **Infra + inventario**: ticket 012 (NOPASSWD + refresh)
- **Storage + backup design**: ticket 013 (propuesta iter 3, capex $0)

## 🔄 Patrones de fallo

- **Tickets 001..004 (create LXC)**: bug del wrapper `aranea-pve-create` (parámetro `ostemplate` excede 255 chars). Solucionado en ticket 005 con nuevo CTID 200.

## 📚 Convención

Ver `~/aranea/tickets/README.md` y `~/aranea/tickets/schema.md`.

## 🔗 Links a propuesta activa

- **[[../../03-storage/DESIGN-PROPOSAL|Design proposal storage + backup (iter 3)]]** ← ticket 013
- **[[../../03-storage/TOPOLOGY-AUDIT|Auditoría topológica]]** ← anomalías detectadas

---

## Source files

- `/home/hermes/aranea/tickets/README.md`
- `/home/hermes/aranea/tickets/schema.md`
- `/home/hermes/aranea/tickets/2026-06-29-*.md`
- `/home/hermes/aranea/tickets/2026-06-30-*.md`

## Captured

Tickets: 2026-06-29..30. Doc generado el 2026-06-30, actualizado 2026-06-30 (cierre sesión).

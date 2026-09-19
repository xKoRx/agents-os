---
type: index
schema_version: 1
status: active
icon: 💥
slug: aranea-high-impact
area: "[[Aranea]]"
project: "[[HERMES — Infrastructure Operations]]"
created: 2026-09-19
updated: 2026-09-19
reviewed: 2026-09-19
aliases:
  - Aranea high-impact index
  - H5 high-impact index
  - high-impact infrastructure
cssclasses:
  - wide
tags:
  - kind/index
  - area/aranea
  - domain/aranea
  - domain/homelab
  - action/high-impact
  - project/hermes-aranea-autonomous-operations
---

# 💥 Aranea — High-Impact Infrastructure (H5)

> [!info] Índice de habilitación H5 — alto impacto (enablement-only)
> **Mandato:** H5 ONE-SHOT 2026-09-19 · **Veredicto:** `H5 ENABLEMENT PASS — VERIFIED SCOPE` · **Mutaciones de infraestructura: 0**
> Auditoría read-only en vivo 2026-09-19 15:42–15:50 UTC. Evidencia cruda: `~/aranea/work/h5-high-impact-20260919/probes/` (fuera del vault).
> La **ejecución** de cualquier operación high-impact pertenece al proyecto ejecutor con sus propios gates; los contratos NO autorizan operaciones.

## 📊 De un vistazo

| Familia | Componentes clave | Estado habilitación | Clase máx. ops | Recovery doc. | Recovery demostrado | Contrato |
|---|---|---|---|---|---|---|
| A — Networking/Firewall | OPNsense 130 (SPOF LAN, running), PVE firewall disabled, Tailscale 119 (running) | PARTIAL | CLASS 3 | NO | NO | [[high-impact-networking-dns-contract]] |
| B — DNS/DHCP/resolución | Pi-hole .31/.149 (FTL vivo), wildcard `*.lab.aranea` + `lab.aranea.cl`, DHCP upstream (router ISP) | PARTIAL | CLASS 3 | NO | Resolución demostrada (consulta viva) | [[high-impact-networking-dns-contract]] |
| C — Cluster Proxmox/quorum | 5 nodos 8.4.20, quorum 5/5, HA sin recursos, corosync sin red dedicada | VERIFIED_READ | CLASS 3 | Parcial (SSH+sudo EJERCIDO; consola owner = break-glass) | SSH EJERCIDO; node-loss NO | [[cluster-node-maintenance-contract]] |
| D — Ceph/storage distribuido | 4 OSD NVMe, 3 MON, HEALTH_WARN persistente (osd.0/2 nearfull ~85.6%, pool1 87.26%) | VERIFIED_READ | CLASS 3 | NO | NO | [[ceph-storage-operations-contract]] |
| E — TrueNAS/storage compartido | VM 145 @hades, pool0/pool2 ONLINE, NFS/SMB/iSCSI activos, scrub pool0 6-sep 0 errores | VERIFIED_READ (admin FULL revalidado) | CLASS 2/3 | SSH+sudo EJERCIDO | SSH EJERCIDO | Reutiliza matriz H1 |
| F — PBS/protección | VM 180 @kronos, datastore main 731M (snapshot única ct/155), fail-closed EN VIVO confirmado | VERIFIED_READ | CLASS 2 | R2 validado 2026-09-19 | SSH+reboot/fail-closed EJERCIDO (mandato R2) | R2 vigente (Backup/DR) |
| G — PKI/certificados | step-ca LXC 200 @athena STOPPED (CA .12), Traefik 115 + wildcard vigentes | PARTIAL | CLASS 3 | NO | NO | — (gap documental) |
| H — Energía/UPS | UPS NO CONFIGURADO (histórico); servicio `ups` STOPPED en TrueNAS; sin NUT en el cluster | NOT_PROVEN | CLASS 3 | NO | NO | — (sin superficie) |
| I — Control plane Ariadna/Hermes | hermes-vm 118 @kronos (.122), self-management, keys `ariadna_*` | VERIFIED_READ | CLASS 2 | SÍ ([[hermes-linux-update-recovery]]) | SÍ (recovery 2026-09-16) | Existente |
| J — Host transversal | 5 nodos PVE + TrueNAS como VM (turtles), kernel drift athena -29 vs -18 | VERIFIED_READ | CLASS 3 | SSH+sudo EJERCIDO 5/5 | SSH EJERCIDO | [[cluster-node-maintenance-contract]] |

**Síntesis de brecha:** el trío sin recovery documentado ni demostrado es **A (OPNsense = SPOF), D (Ceph) y G (step-ca stopped + CA sin backup)**; H (energía) ni siquiera tiene superficie de protección (UPS sin configurar). Riesgo agregado: un corte eléctrico prolongado o la caída de athena degradan a la vez gateway, DNS interno, CA y acceso remoto.

## ⛓️ Dependencias críticas (mapa G5)

```text
Ariadna (hermes-vm .122 @kronos)
  └─ management: SSH llaves ariadna_pve(×5 nodos)/truenas/pbs/win — LAN 192.168.31.0/24 — sin dependencia MCP
  └─ DNS: 192.168.31.31 (Pi-hole .149) → upstream 192.168.31.1 (router ISP)
  └─ gateway: OPNsense 130 (SPOF): TODO el tráfico LAN/WAN incl. corosync y Ceph-over-LAN
OPNsense 130 ─ depende de: athena (host físico) ─ alimenta: LAN completa, WAN, DHCP
Pi-hole .149 ─ depende de: athena + upstream router .1 ─ alimenta: resolución de todo el homelab
step-ca 200 ─ STOPPED; alimenta: emisión/renovación TLS interno (Traefik); wildcard vigente
Ceph ─ 3 MONs en LAN (NO en 10.10.10.0/24): saturación LAN puede degradar quorum Ceph
TrueNAS 145 ─ VM sobre hades (turtles); alimenta NFS/SMB/iSCSI a todo el cluster
```

Puntos donde un cambio deja fuera a Ariadna o al owner: gateway OPNsense, DNS Pi-hole, la LAN física del nodo athena, y el `from="192.168.31.122"` de las llaves SSH (si hermes-vm cambia de IP o muere, el acceso nativo exige reinstalación por consola del owner).

## 📁 Contenido

| Recurso | Contenido |
|---|---|
| [[high-impact-networking-dns-contract]] | Contrato operador networking/DNS/host transversal (familias A, B, J) |
| [[cluster-node-maintenance-contract]] | Contrato operador mantenimiento de nodos/quorum (familias C, J) |
| [[ceph-storage-operations-contract]] | Contrato operador Ceph/storage distribuido (familia D) |
| [[HERMES — Infrastructure Operations]] | Programa padre + matrices H0–H5 |
| [[30-resources/aranea/01-topologia/fechas-captura|fechas-captura]] | Honestidad documental: fecha de cada captura |

## 🔍 Negativos clasificados (sin provocar fallas)

| ID | Situación | Clasificación |
|---|---|---|
| N1 (de H2, vigente) | Operación que compromete quorum (p.ej. cambiar corosync sin ventana) | NO_GO — CLASS 3 |
| N2 (de H4, vigente) | Provisioning sobre pool1 nearfull | NO_GO — capacidad |
| N3 (H5, observado) | Recovery de OPNsense/step-ca/UPS: no existe runbook ni procedimiento | NOT_CERTIFIED |
| N4 (de H0, vigente) | `ca.lab.aranea` resuelve por DNS pero el servicio está stopped | AMBIGUOUS si se opera por nombre — target proof exige estado vivo |
| N5 (de H4, vigente) | Operación CLASS 3 sin owner gate | GATED |
| N6 (de H0/H2, vigente) | MCP Access Plane no disponible → Ariadna opera por SSH nativo (independencia demostrada) | CANAL NATIVO (no provoca la falla) |

## 📆 Bitácora

- **2026-09-19 — H5 ENABLEMENT PASS — VERIFIED SCOPE (mandato owner one-shot; ZERO INFRASTRUCTURE MUTATIONS):** inventario G1 (familias A–J), matriz de autoridad (G2), blast radius (G3), revalidación Ceph 3/3 MONs (G4), mapa networking/DNS (G5), cluster/quorum (G6), TrueNAS/PBS/PKI/UPS (G7), 3 contratos nuevos + reutilización H1/R2 (G8). Golden G9 sesión fresca PASS (hijo aislado, 3 sesiones SSH read-only): Escenario A = **NO_GO condicionado** para mantenimiento de zeus (osd.2 nearfull en el nodo + SQX 108 sin plan de protección), Escenario B = **HANDOFF operativo** a [[ceph-storage-operations-contract]]; 6 negativos; `operaciones_mutantes=0`, `mcp_calls=0`. Detalle: change log `80-agents/journal/logs/2026-09-19-h5-high-impact-enablement.md`.

## 🔗 Links

- [[HERMES — Infrastructure Operations]] — programa padre con matrices de autoridad por nivel.
- [[HERMES — ARANEA AUTONOMOUS OPERATIONS]] — programa raíz.
- [[BACKUP-DR-OWNER-PROJECT]] — R2/protección PBS (autoridad de ejecución).
- [[30-resources/aranea/00-index|Aranea index]] — catálogo del dominio.

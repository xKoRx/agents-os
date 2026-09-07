---
type: area
status: active
icon: 🕸️
slug: aranea
banner: "[[banner-aranea.png]]"
desc: Infra, red, servicios y automatización
tags:
  - area/aranea
  - kind/area
review: weekly
status_detail: "Sesión 2026-06-30 cerrada limpiamente. Gaps #1-4 cerrados (diseño). Propuesta activa en `03-storage/DESIGN-PROPOSAL.md` (capex $0, iter 3). Auditoría topológica en `03-storage/TOPOLOGY-AUDIT.md` (10 anomalías). Pendiente: 5 decisiones owner (tickets 014-017 cuando se apruebe)."
created: 2026-06-23
updated: 2026-06-30
aliases:
  - aranea
  - Homelab
  - Infra
cssclasses:
  - wide
---

![[banner-aranea.png]]

> [!abstract]+ 🕸️ Aranea
> Mi homelab: la infraestructura viva. Servidores, red, storage, servicios y observabilidad — lo que corre, se rompe, se monitorea y se respalda.

## 🎯 Objetivo

- 

## 📊 Estado actual

- **Inventario**: ✅ Refrescado 2026-06-30 19:44 UTC. Drift = 0d.
- **Gap #1 (NOPASSWD agent_ro)**: ✅ Cerrado 2026-06-30 (ticket `2026-06-30-012`).
- **Gap #2 (drift inventario)**: ✅ Cerrado 2026-06-30.
- **Gap #3 (auditoría storage)**: ✅ Diseño cerrado 2026-06-30 (ticket `2026-06-30-013`).
- **Gap #4 (diseño backup)**: ✅ Diseño cerrado 2026-06-30 (iter 3). **Capex $0**. Plan B definitivo. Pendiente 5 decisiones owner + ejecución Fases 1-4.
- **Cierre sesión 2026-06-30**: ver `30-resources/aranea/00-index` § "Cierre de sesión — handover" para resumen completo + 5 decisiones pendientes.
- **Cluster**: 5 Proxmox + TrueNAS VM + hermes-vm = **7 máquinas** · 302t / 767 GB RAM / ~12 TB útil.
- **Doc principal**: [[30-resources/aranea/00-index]] · por nodo en [[30-resources/aranea/01-topologia/]].
- **Proyecto activo**: [[10-projects/Aranea/BACKUP-DR-OWNER-PROJECT]] — Backup/DR integral (design-frozen, awaiting owner 018-021).
- **Skill operativa**: `aranea_agent_ro_inventory_refresh` — refresh periódico del inventario. 

## 🧩 Stack / Servicios

- Proxmox · Traefik · MinIO · CouchDB (Obsidian LiveSync) · Frigate · Home Assistant (servicio) · OPNsense · DNS · Ceph · Temporal · backups · monitoreo

## 🟢 Proyectos de esta área

```base
filters:
  and:
    - 'type == "project"'
    - 'file.hasLink(this.file)'
views:
  - type: cards
    name: Proyectos
    order:
      - file.name
      - note.status
```

## 📚 Recursos de esta área

```base
filters:
  and:
    - 'type == "resource"'
    - 'file.hasLink(this.file)'
views:
  - type: table
    name: Recursos
    order:
      - file.name
      - note.status
```

## ✅ Tareas abiertas

```tasks
sort by priority
not done
tags include #area/aranea
short mode
hide task count
```

## 🧭 Decisiones relevantes

- 

## 🔗 Links

- 

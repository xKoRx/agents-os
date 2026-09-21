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
status_detail: "Backup/DR ACTIVE: R0/R1/R1.5/D0 DONE (16-18sep); G1A+G1B (20sep) = primera protección recuperable CERTIFICADA de PG/Mongo/MinIO; MP-01 (20-21sep) = A1 dumps diarios DONE (2º ciclo verificado 21sep) + A0/A5 PASS; R2 piloto 3/7 (expira 26sep; run 21sep perdido por apagado de hermes). Master Plan+matriz 59/59+placement+ventana P0 cerrados (20sep). Owner decidió 21sep: semana 21-25sep de preparación, intervención tras cierre operativo real de Echo del vie 25, ventana sáb 26sep 02:00-07:00 pendiente de autorización. Estado datado: [[ARANEA-CONTINUIDAD-Y-VENTANA-25-26-SEP]]. Preflight G0 2026-09-17: inventario 6/6 (59 VMs). Docs storage previos deprecated/superseded → [[BACKUP-DR-DESIGN]]."
created: 2026-06-23
updated: 2026-09-21
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

- **Inventario**: ✅ Refrescado 2026-09-17 18:58 UTC (captura 6/6 + JSON materializado). Drift = 0d.
- **Gap #1 (NOPASSWD agent_ro)**: ✅ Cerrado 2026-06-30 (ticket `2026-06-30-012`).
- **Gap #2 (drift inventario)**: ✅ Cerrado 2026-06-30.
- **Gap #3 (auditoría storage)**: ✅ Diseño cerrado 2026-06-30 (ticket `2026-06-30-013`).
- **Gap #4 (diseño backup)**: ✅ Diseño cerrado 2026-06-30 (iter 3). **Capex $0**. Plan B definitivo. Pendiente 5 decisiones owner + ejecución Fases 1-4.
- **Cierre sesión 2026-06-30**: ver `30-resources/aranea/00-index` § "Cierre de sesión — handover" para resumen completo + 5 decisiones pendientes.
- **Cluster**: 5 Proxmox + TrueNAS VM + hermes-vm = **7 máquinas** · 302t / 767 GB RAM / ~12 TB útil.
- **Doc principal**: [[30-resources/aranea/00-index]] · por nodo en [[30-resources/aranea/01-topologia/]].
- **Proyecto activo**: [[10-projects/Aranea/BACKUP-DR-OWNER-PROJECT]] — Backup/DR integral **ACTIVE**: R0 ✅, R1 ✅ (con deuda owner), D0 ✅, G1A/G1B ✅ (20sep, primera protección recuperable certificada), MP-01 ✅ (A1 DONE al 21sep); R2 piloto 3/7 (expira 26sep). Semana 21-25sep = preparación; ventana P0 sáb 26sep 02:00-07:00 pendiente de autorización (gates owner). Continuidad: [[ARANEA-CONTINUIDAD-Y-VENTANA-25-26-SEP]] — mutaciones en gate owner (tickets 018/019).
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

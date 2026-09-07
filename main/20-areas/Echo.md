---
type: area
status: active
icon: ⚙️
slug: echo
banner: "[[banner-echo.png]]"
desc: Trading algorítmico, Forge, Core y pipelines
tags:
  - area/echo
  - kind/area
review: weekly
created: 2026-06-23
updated: 2026-06-27
aliases:
  - echo
  - Echo Systems
  - Sistemas propios
---

![[banner-echo.png]]

> [!abstract]+ ⚙️ Echo
> Mi ecosistema de software de trading/dev a largo plazo: sistemas propios, pipelines y arquitectura. No es la infra (eso es Aranea) — es el producto.

## 🎯 Objetivo

- 

## 📊 Estado actual

- **2026-08-20** — Estado del ecosistema recapitulado en [[Echo - Discovery y Estado]]: v3 activo (roadmap "Olympus"), reportería = Daily Ops (Watchtower) + The Lab (WIP); hotfix Daily Ops nativas verificado en prod, mergeado y pusheado a master (`c8aa59a4`). Nativas siguen sin verse por dos causas nuevas: opens nativos con `lot_size=0` rechazados por el core, y matview Daily Ops que filtra cuentas INACTIVE (0 filas para todo). Ver detalle y pendientes en el proyecto.

## 🧩 Componentes

- Echo Core · Echo Forge · SQX · plugins · SPECs / RFCs · pipelines · MT5 · StrategyQuant · modelos de datos · arquitectura Go

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
tags include #area/echo
short mode
hide task count
```

## 🧭 Decisiones relevantes

- [[Echo - Discovery y Estado]] (proyecto de comprensión del ecosistema, 2026-08-20)

## 🔗 Links

- 

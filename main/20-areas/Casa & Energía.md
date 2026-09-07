---
type: area
status: active
icon: 🏠
slug: casa
banner: "[[banner-casa.png]]"
desc: Domótica, solar, baterías y consumo
tags:
  - area/casa
  - kind/area
review: weekly
created: 2026-06-23
updated: 2026-06-27
aliases:
  - casa
  - casa energia
  - Casa y Energía
  - Casa y Energia
  - Casa
  - Energía
  - Energia
  - Hogar
---

![[banner-casa.png]]

> [!abstract]+ 🏠 Casa & Energía
> El hogar como sistema: domótica y automatizaciones (Home Assistant), más energía solar, baterías y consumo (Victron, paneles).

## 🎯 Objetivo

- 

## 📊 Estado actual

- 

## 🧩 Incluye

- Domótica: automatizaciones, sensores, cámaras/presencia, luces, escenas, dashboard hogar
- Energía: Victron, paneles, baterías, cuenta de luz, optimización de carga, consumo homelab vs casa

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
tags include #area/casa
short mode
hide task count
```

> [!example]- Fuente de tareas — editar / mover de estado aquí
> - [ ] Instalar cámara interior y exterior #owner/me #type/admin #area/casa
> - [ ] Instalar cortina de cocina #owner/me #type/admin #area/casa

## 🧭 Decisiones relevantes

- 

## 🔗 Links

- 

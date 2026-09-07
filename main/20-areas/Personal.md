---
type: area
status: active
icon: 🌱
slug: personal
banner: "[[banner-personal.png]]"
desc: Vida personal, administración y decisiones
tags:
  - area/personal
  - kind/area
review: weekly
created: 2026-06-23
updated: 2026-06-27
aliases:
  - personal
  - Otros
  - Misceláneo
---

![[banner-personal.png]]

> [!abstract]+ 🌱 Personal
> Mi vida personal: administración, hábitos, decisiones e ideas que no caen en otra área.

## 🎯 Objetivo

- 

## 📊 Estado actual

- 

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
tags include #area/personal
short mode
hide task count
```

> [!example]- Fuente de tareas — editar / mover de estado aquí
> - [ ] Identificar pendientes con tabla de Eisenhower #owner/me #type/admin #area/personal

## 🧭 Decisiones relevantes

- 

## 🔗 Links

- 

---
type: area
status: active
icon: 👨‍👩‍👧
slug: familia
banner: "[[banner-familia.png]]"
desc: Momentos, colegio, planes y recuerdos
tags:
  - area/familia
  - kind/area
review: weekly
created: 2026-06-23
updated: 2026-06-27
aliases:
  - familia
---

![[banner-familia.png]]

> [!abstract]+ 👨‍👩‍👧 Familia
> Mi familia: planes, recordatorios, momentos y compromisos importantes.

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
tags include #area/familia
short mode
hide task count
```

## 🧭 Decisiones relevantes

- 

## 🔗 Links

- 

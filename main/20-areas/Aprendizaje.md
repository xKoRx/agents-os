---
type: area
status: active
icon: 🎓
slug: aprendizaje
banner: "[[banner-aprendizaje.png]]"
desc: Cursos, libros, skills y research
tags:
  - area/aprendizaje
  - kind/area
review: weekly
created: 2026-06-23
updated: 2026-06-27
aliases:
  - aprendizaje
  - Learning
  - Estudio
---

![[banner-aprendizaje.png]]

> [!abstract]+ 🎓 Aprendizaje
> Lo que estoy estudiando: cursos, libros, skills técnicas y notas de lo aprendido.

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
tags include #area/aprendizaje
short mode
hide task count
```

> [!example]- Fuente de tareas — editar / mover de estado aquí
> - [ ] Leer sobre la dicotomía del control #owner/me #type/research #area/aprendizaje
> - [ ] Leer Tráguese ese sapo #owner/me #type/research #area/aprendizaje

## 🧭 Decisiones relevantes

- 

## 🔗 Links

- 

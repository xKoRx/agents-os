---
type: area
status: active
icon: 💼
slug: meli
banner: "[[banner-meli.png]]"
desc: Trabajo, VIS, arquitectura y equipo
tags:
  - area/meli
  - kind/area
review: weekly
created: 2026-06-23
updated: 2026-06-27
aliases:
  - meli
  - MELI
  - Trabajo
  - Mercado Libre
  - MercadoLibre
---

![[banner-meli.png]]

> [!abstract]+ 💼 Meli
> Mi trabajo en MercadoLibre: desarrollo, releases, proyectos técnicos y seguimiento del día a día.

## 🗓️ Daily / Standup

**✅ Ayer**
```tasks
sort by priority
done on yesterday
tags include #area/meli
short mode
hide task count
```

**✅ Hoy**
```tasks
sort by priority
done on today
tags include #area/meli
short mode
hide task count
```

**🔵 En curso — Sprint [[A26Q2S7]]**
```tasks
sort by priority
not done
tags include #sprint/A26Q2S7
group by status
short mode
hide task count
```

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
    - '!note.parent'
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

## 💡 Ideas / validaciones

```base
filters:
  and:
    - 'type == "idea"'
    - 'file.hasLink(this.file)'
views:
  - type: table
    name: Ideas
    order:
      - file.name
      - note.status
      - note.priority
```

## ✅ Tareas abiertas

```tasks
sort by priority
not done
tags include #area/meli
short mode
hide task count
```

> [!example]- Fuente de tareas — editar / mover de estado aquí
> - [ ] [[Destaques de Precio]] crear tareas Jira faltantes #owner/me #type/admin #area/meli
> - [ ] Cerrar releases de Credits #owner/me #type/admin #area/meli
> - [ ] Solicitar revisión de PRs pendientes #owner/me #type/pr-review #area/meli
> - [ ] Pedir permisos de [[feed-cheshire|Cheshire]] #owner/me #type/admin #area/meli
> - [ ] [[vis-motors-mcp]] planificar migración #owner/me #type/dev #area/meli
> - [ ] Reagendar 1:1 #owner/me #type/admin #area/meli
> - [ ] Hablar con yofrank para agendar sesión y luego escribirle #owner/me #type/admin #area/meli
> - [ ] [[search-middleware]] revisar coverage pendiente #owner/me #type/dev #area/meli
> - [ ] Completar notas de aplicaciones Meli (github, path local, contexto): [[vis-items-loader-tagging]], [[java-polycard-sdk]], [[search-middleware]], [[vis-octopus-lib]], [[vpp-backend]] #owner/me #type/admin #area/meli

## 🧭 Decisiones relevantes

- 

## 🔗 Links

- 

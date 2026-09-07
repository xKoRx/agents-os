---
type: home
icon: 🏠
tags:
  - home
  - kind/home
created: 2026-06-23
updated: 2026-06-27
cssclasses:
  - wide
---

# 🏠 Home

> [!tip] Tu portada diaria. Captura rápido en [[tareas]], enfoca por área y revisa el pulso del día. Homes de foco: [[Meli]] · [[Personal]] · Seguimiento humano/agente en [[Panel de Proyectos]]

## 📥 Inbox — sin clasificar

```tasks
sort by priority
not done
path includes 00-inbox
short mode
hide task count
```

## 🗓️ Standup — hoy

%% Vista humana: muestra tus tareas y las tareas puente (#type/supervision). Las tareas de agente NO aparecen; el trabajo delegado se ve en los puentes y en [[Panel de Proyectos]]. %%

**✅ Completado hoy — mías + puentes**
```tasks
sort by priority
done on today
tags include #owner/me
short mode
hide task count
```

**🔵 En curso — mías + puentes**
```tasks
sort by priority
not done
tags include #area/
tags include #owner/me
group by filename
short mode
hide task count
```

**🌉 Delegado — proyectos de agente que sigo**
```tasks
sort by priority
not done
tags include #type/supervision
short mode
hide task count
```

**🧺 Sin owner — clasificar**
```tasks
sort by priority
not done
tags include #area/
not tags include #owner/me
not tags include #owner/agent
group by filename
short mode
hide task count
```

## 🟢 Proyectos activos (todas las áreas)

```base
filters:
  and:
    - 'type == "project"'
    - '!note.parent'
    - 'status != "done"'
views:
  - type: cards
    name: Proyectos
    order:
      - note.area
      - file.name
      - note.status
      - note.priority
  - type: table
    name: Por área
    order:
      - file.name
      - note.area
      - note.status
      - note.priority
      - note.sprint
    groupBy:
      property: note.area
      direction: ASC
```

## 🗂️ Áreas

Galería completa en [[Áreas]]. Cada área es su propio home de foco.

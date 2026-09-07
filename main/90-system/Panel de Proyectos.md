---
type: dashboard
icon: 🗂️
tags:
  - kind/dashboard
  - kind/system
created: 2026-07-01
updated: 2026-07-01
aliases:
  - Panel de proyectos
  - dashboard de proyectos
---

# 🗂️ Panel de Proyectos

> [!tip] Control de seguimiento humano vs agente. Fuente de verdad: cada nota de proyecto (`owner: me|agent`, `root`, `parent`). Convenciones en [[convenciones]]. Cockpit diario en [[Home]].

## 🌉 Mi cockpit de supervisión — proyectos de agente que sigo

%% Una línea por curro delegado. El estado refleja tu relación: To Do (no arranco) → WIP (lo sigo) → Review (reviso entrega) → Done. %%

```tasks
not done
(tags include #type/supervision)
sort by priority
group by filename
short mode
hide task count
```

## 🤖 Proyectos de agente (activos)

```base
filters:
  and:
    - 'type == "project"'
    - 'note.owner == "agent"'
    - 'status != "done"'
views:
  - type: cards
    name: De agente
    order:
      - note.parent
      - file.name
      - note.status
      - note.priority
```

## 🧍 Proyectos humanos (activos)

```base
filters:
  and:
    - 'type == "project"'
    - 'note.owner == "me"'
    - 'status != "done"'
views:
  - type: cards
    name: Humanos
    order:
      - note.area
      - file.name
      - note.status
      - note.priority
```

## 🚨 Huérfanos — subproyectos sin padre (adoptar)

%% type project, sin parent y sin root. Setéales parent o root: true. %%

```base
filters:
  and:
    - 'type == "project"'
    - '!note.parent'
    - 'note.root != true'
views:
  - type: cards
    name: Huérfanos
    order:
      - file.name
      - note.area
      - note.owner
```

## 🧺 Sin owner — proyectos sin clasificar (humano/agente)

%% type project sin owner. Ponles owner: me u owner: agent. %%

```base
filters:
  and:
    - 'type == "project"'
    - '!note.owner'
views:
  - type: cards
    name: Sin owner
    order:
      - file.name
      - note.parent
      - note.area
```

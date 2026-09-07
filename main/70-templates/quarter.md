---
type: quarter
schema_version: 1
status: active
area: "[[Meli]]"
start:
end:
tags:
  - quarter
  - kind/quarter
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# {{title}}

> [!info]+ Quarter {{title}}
> **Estado:** active · **Inicio:** — · **Fin:** —

## 🎯 Objetivo del quarter

- 

## 📅 Sprints

```base
filters:
  and:
    - 'type == "sprint"'
    - 'file.hasLink(this.file)'
views:
  - type: table
    name: Sprints
    order:
      - file.name
      - note.status
      - note.start
      - note.end
    sort:
      - property: note.start
        direction: ASC
```

## 🔵 Pendientes del quarter

%% Vista humana: excluye tareas de agente; el trabajo delegado aparece como tarea puente (#type/supervision). %%
```tasks
sort by priority
not done
tags include #quarter/{{title}}
tags do not include #owner/agent
group by filename
hide task count
```

---
type: sprint
schema_version: 1
status: active
area: "[[Meli]]"
quarter:
start:
end:
tags:
  - sprint
  - kind/sprint
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
---

# {{title}}

> [!info]+ Sprint {{title}}
> **Estado:** active · **Inicio:** — · **Fin:** — · 2 semanas
> Tag para asociar tareas: `#sprint/{{title}}`

## 🎯 Objetivo del sprint

- 

## 📝 Descripción

- 

## 🔵 Pendientes del sprint

%% Vista humana: excluye tareas de agente; el trabajo delegado aparece como tarea puente (#type/supervision). %%
```tasks
sort by priority
not done
tags include #sprint/{{title}}
tags do not include #owner/agent
group by status
hide task count
```

## ✅ Completadas en el sprint

```tasks
sort by priority
done
tags include #sprint/{{title}}
tags do not include #owner/agent
hide task count
```

## 🔗 Proyectos del sprint

- 

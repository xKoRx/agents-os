---
type: area
schema_version: 1
status: active
icon: 🗂️
slug: cambiar-slug
banner: ""
desc: ""
tags:
  - area
  - kind/area
  - area/cambiar-slug
review: weekly
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
aliases: []
---

%% Naming: el título de la nota es el link canónico; slug es solo identificador técnico para tags/paths; aliases contiene variantes humanas. %%
%% Pega aquí la cabecera cuando tengas el banner: ![[banner-<slug>.png]] — y completá banner: "[[banner-<slug>.png]]" en el frontmatter %%

> [!abstract]+ {{title}}
> _Una frase que describa de qué se trata esta área de tu vida y qué estándar querés mantener._

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

%% Cambiá #area/cambiar-slug por el tag de esta área. Las tareas deben escribirse como "- [ ] ... #area/<slug>". Otras notas deben referenciar esta área con area: "[[{{title}]]". Vista humana: excluye tareas de agente; el trabajo delegado aparece como tarea puente (#type/supervision). %%
```tasks
sort by priority
not done
tags include #area/cambiar-slug
tags do not include #owner/agent
short mode
hide task count
```

## 🧭 Decisiones relevantes

- 

## 🔗 Links

- 

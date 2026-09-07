---
type: project
owner: me
root: true
status: active
priority: P1
area: "[[Personal]]"
parent:
sprint:
start: "2026-06-30"
due:
progress: 0
repo:
jira:
prs:
aliases:
  - corrección masiva de tags
  - massive tagging cleanup
tags:
  - area/personal
  - kind/project
created: "2026-06-30"
updated: "2026-06-30"
---


# Corrección masiva de tags

%% Naming: Corrección masiva de tags es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Corrección masiva de tags
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** —

## 🎯 Objetivo

- Realizar una corrección masiva y automatizada de los tags en el Second Brain (corrigiendo 436 inconsistencias de taggeo).
- Robustecer la constitución del agente para incluir la filosofía de aprendizaje evolutivo, uso, y mejora de habilidades (skills) y reglas de interacción.

## 📊 Estado actual

- Linter arrojó 436 inconsistencias de tags.
- La constitución aún no tiene la sección sobre mejora y aprendizaje evolutivo de skills.

## 🧩 Subproyectos

```base
filters:
  and:
    - 'type == "project"'
    - 'file.hasLink(this.file)'
views:
  - type: cards
    name: Subproyectos
    order:
      - file.name
      - note.status
      - note.priority
```

## ✅ Tareas

> [!note]+ Convención de ownership
> Usa `#owner/me` para tareas humanas y `#owner/agent` para tareas de agentes.
> Si una tarea no tiene owner, queda visible abajo para corregirla.

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
const ord={" ":0,"/":1,"r":2,"x":3,"X":3,"-":4};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function render(tasks){
  const el=dv.el('div','');
  el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");
}
function owned(tasks, owner){return tasks.filter(t=>new RegExp(`(^|\\s)#owner/${owner}(\\s|$)`).test(String(t.text)));}
const tasks=dv.current().file.tasks.array().sort((a,b)=>(ord[a.status]??9)-(ord[b.status]??9));
const mine=owned(tasks,"me");
const agent=owned(tasks,"agent");
const loose=tasks.filter(t=>!new RegExp(`(^|\\s)#owner/(me|agent)(\\s|$)`).test(String(t.text)));

dv.header(3,"🧍 Tareas mías");
mine.length ? render(mine) : dv.paragraph("_Sin tareas mías._");

dv.header(3,"🤖 Tareas de agentes");
agent.length ? render(agent) : dv.paragraph("_Sin tareas de agentes._");

dv.header(3,"🧺 Sin owner");
loose.length ? render(loose) : dv.paragraph("_Sin tareas sin owner._");
```

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. Tipos: #type/dev #type/admin #type/research #type/pr-review. Flags: #blocked #waiting #urgent. Ver [[convenciones]]. %%
> - [x] Crear script de corrección automática `fix_tags.py` #owner/agent #type/dev #area/personal
> - [x] Ejecutar script de corrección masiva de tags en todo el vault #owner/agent #type/dev #area/personal
> - [x] Validar corrección con el linter de tags #owner/agent #type/dev #area/personal
> - [x] Reindexar Graphify #owner/agent #type/dev #area/personal
> - [ ] Generar logs de cierre de sesión (esperando orden de cierre) #owner/agent #type/dev #area/personal

## 📋 Tablero

#### 🟦 To Do
```tasks
sort by priority
path includes Corrección masiva de tags
status.name includes Todo
short mode
hide task count
```

#### 🟡 WIP
```tasks
sort by priority
path includes Corrección masiva de tags
status.name includes WIP
short mode
hide task count
```

#### 🔵 Review
```tasks
sort by priority
path includes Corrección masiva de tags
status.name includes Review
short mode
hide task count
```

#### ✅ Done
```tasks
path includes Corrección masiva de tags
done
short mode
hide task count
```

## 📆 Bitácora

- **2026-06-30** — Inicialización del proyecto de limpieza de tags, creación del script automatizado y actualización constitucional.

## 🧭 Decisiones

- 

## 🔗 Docs / Links

- [[agents-os-tagging-system]]

## 💡 Ideas

### Backlog de ideas

- 

### Motivos / principios

- 

### Memoria pública / interna

- **Memoria pública:** [[metadata-schema.md]]
- **Memoria interna:** 
- **Motivo:** 

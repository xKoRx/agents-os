---
type: project
owner: me
root: true
status: active
priority: P0
area: "[[Meli]]"
parent:
sprint:
start: 2026-07-27
due: 2026-08-10
progress: 0
repo:
jira:
prs:
aliases:
  - cierre vis
tags:
  - area/meli
  - kind/project
created: 2026-07-27
updated: 2026-08-04
cssclasses:
  - wide
---


# Cierre VIS

%% Naming: Cierre de temas de VIS por cambio de equipo a ADS. %%

> [!info]+ Cierre VIS
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P0 · **Sprint:** —

## 🎯 Objetivo

- Terminar todos los pendientes hasta 10/08/26

## 📊 Estado actual

- Destaque de precio
- Fase 1 de loader tagging: modelo de señales para price discount, con seguimiento delegado en [[Fase 1 — Modelo de Señales Price Discount — Loader Tagging]].
- Implementación de Destaque de Precio en Search planificada por repositorio en [[Destaque de Precio Search — Search API Go]], [[Destaque de Precio Search — Java Polycard SDK]] y [[Destaque de Precio Search — Search Middleware]].

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
> - [x] HABLAR CON DUGLAS #owner/me #type/dev #area/meli ✅ 2026-07-27
> - [x] DESPLEGAR VERSIÓN LOADER TAGGING CON PROCESO NUEVO #owner/me #type/dev #area/meli ✅ 2026-07-27
> - [x] CREAR TP PRODUCTIVO NUEVO #owner/me #type/dev #area/meli ✅ 2026-07-27
> - [x] CREAR TÓPICOS Y DESPLEGAR VERSIÓN PARA BACKFILL #owner/me #type/dev #area/meli ✅ 2026-07-27
> - [x] SACAR VERSIÓN DE PRUEBA #owner/me #type/dev #area/meli ✅ 2026-07-27
> - [r] [[Fase 1 — Modelo de Señales Price Discount — Loader Tagging]] arrancar + seguimiento #owner/me #type/supervision #area/meli #app/vis-items-loader-tagging #feature/destaques-de-precio
> - [r] [[Fase 2 — Proceso Masivo por Site vía items_batch_search — Loader Tagging]] implementación lista para revisión (masivo sin BigQuery, scroll resumible) #owner/me #type/supervision #area/meli #app/vis-items-loader-tagging #feature/destaques-de-precio
> - [r] [[Bajó de precio all platforms]] implementación lista para revisión humana; suite completa bloqueada por 13 fallas preexistentes de `SearchShopsAdsServiceTest` #owner/me #type/supervision #area/meli #app/search-middleware #feature/destaques-de-precio
> - [x] Desplegar nueva config en scopes productivos #owner/me #type/dev #area/meli 📅 2026-07-28 ✅ 2026-07-28
> - [r] Desplegar versión de prueba y probar en scope backfill #owner/me #type/dev #area/meli 🔺 📅 2026-07-29
> - [r] Hablar con douglas y ari para validar proceso masivo y tópicos/consumers por lag de mensajes #owner/me #type/dev #area/meli 🔺 📅 2026-07-31
> - [r] Lanzar mensaje de review de fase 2 #owner/me #type/dev #area/meli
> - [ ] Revisar tópico de cambio de atributos de ítems motors (tópico classi) #owner/me #type/dev #area/meli 
> - [r] Realizar una última prueba #owner/me #type/dev #area/meli 🔺 📅 2026-07-31
> - [-] Desarrollo destaque de precio Search/Polycard — reemplazada por tres tareas puente por repositorio #owner/me #type/dev #area/meli 📅 2026-07-31
> - [r] [[Destaque de Precio Search — Search API Go]] implementación lista para revisión; `go test ./...` pasa; lint local no disponible #owner/me #type/supervision #area/meli #app/search-api-go #feature/destaques-de-precio
> - [/] [[Destaque de Precio Search — Java Polycard SDK]] arrancar + seguimiento #owner/me #type/supervision #area/meli #app/java-polycard-sdk #feature/destaques-de-precio
> - [/] [[Destaque de Precio Search — Search Middleware]] arrancar + seguimiento #owner/me #type/supervision #area/meli #app/search-middleware #feature/destaques-de-precio
> - [r] Agregar a Jira tarea de desarrollo de all platform y destaque de precio search y polycard #owner/me #type/dev #area/meli 🔺 📅 2026-07-31
> - [r] dar aviso sobre las limitaciones de los bordes en la pill #owner/me #type/dev #area/meli 🔺 📅 2026-08-05
> - [/] tirar prs de search #owner/me #type/dev #area/meli 🔺 📅 2026-08-05
> - [/] hablar con yor sobre la spec de título con short version #owner/me #type/dev #area/meli 🔺 📅 2026-08-05

## 📋 Tablero

#### 🟦 To Do
```tasks
sort by priority
path includes cierre vis
tag includes #owner/me
status.name includes Todo
short mode
hide task count
```

#### 🟡 WIP
```tasks
sort by priority
path includes cierre vis
tag includes #owner/me
status.name includes WIP
short mode
hide task count
```

#### 🔵 Review
```tasks
sort by priority
path includes cierre vis
tag includes #owner/me
status.name includes Review
short mode
hide task count
```

#### ✅ Done
```tasks
path includes cierre vis
tag includes #owner/me
done
short mode
hide task count
```

## 📆 Bitácora

- **2026-08-04** — Se reemplaza la tarea genérica de desarrollo Search/Polycard por tres proyectos de agente bajo este cierre: Search API Go, Java Polycard SDK y Search Middleware. Cada nota contiene baseline, diseño, tareas, gates, tests, rollout y dependencias.
- **2026-06-30** — Inicialización del proyecto de limpieza de tags, creación del script automatizado y actualización constitucional.
- **2026-07-27** — Corregida la clasificación copiada de otro proyecto: `area` pasó de `Personal` a [[Meli]], se eliminó el callout de "Corrección masiva de tags" y se creó la tarea puente para [[Fase 1 — Modelo de Señales Price Discount — Loader Tagging]].
- **2026-07-28** — Fase 2 de Destaque de Precio quedó en Review: trigger asíncrono y scroll resumible implementados sobre `items-batch-search`, con fan-out directo al flujo unitario. Falta validación operativa del spike y carga real.

## 🧭 Decisiones

- [[Cierre VIS]] es el proyecto humano raíz para el seguimiento de pendientes de VIS; los trabajos delegados deben aparecer como una sola tarea puente `#type/supervision`.

## 🔗 Docs / Links

- [[Destaques de Precio]]
- [[Fase 1 — Modelo de Señales Price Discount — Loader Tagging]]
- [[Fase 2 — Proceso Masivo por Site vía items_batch_search — Loader Tagging]]
- [[Bajó de precio all platforms]]
- [[Destaque de Precio Search — Search API Go]]
- [[Destaque de Precio Search — Java Polycard SDK]]
- [[Destaque de Precio Search — Search Middleware]]
- [[vis-items-loader-tagging]]
- [[vis-sdk-go]]
- [[Meli]]

## 💡 Ideas

### Backlog de ideas

- cuándo se pueden activar los experimentos?
- 

### Motivos / principios

- 

### Memoria pública / interna

- **Memoria pública:** no aplica; el estado vive en este proyecto y en sus tareas.
- **Memoria interna:**
- **Motivo:**

---
type: project
owner: me
root: true
status: active
cssclasses:
  - wide
priority: P1
area: "[[Meli]]"
parent:
sprint: "[[A26Q2S7]]"
start: 2026-06-24
due: 2026-06-26
progress: 0
repo: java-polycard-sdk, search-middleware, recommendations-decoration-sdk, recommendations-middleend, feed-cheshire
jira:
prs:
tags:
  - area/meli
  - kind/project
created: 2026-06-24
updated: 2026-07-15
---

# Refactor Polycard

> [!info]+ Refactor Polycard
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** [[A26Q2S7]]
> Fixes de Polycard en los 5 componentes de la cadena de decoración.

## 🎯 Objetivo

- Aplicar el fix de Polycard en las 5 aplicaciones de la cadena (SDK → middlewares/middleends → feed).

## ✅ Tareas

```dataviewjs
const meta = {
  " ": ["To Do","var(--text-muted)","var(--background-modifier-border)"],
  "/": ["WIP","#ba7517","rgba(234,124,12,.18)"],
  "r": ["Review","#185fa5","rgba(55,138,221,.18)"],
  "x": ["Done","#3b6d11","rgba(99,153,34,.18)"],
  "X": ["Done","#3b6d11","rgba(99,153,34,.18)"],
  "-": ["Canceled","var(--text-faint)","var(--background-modifier-border)"]
};
const ord = {" ":0,"/":1,"r":2,"x":3,"X":3,"-":4};
function linkify(s){
  return String(s)
    .replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`)
    .replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`)
    .replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`)
    .replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");
}
const tasks = dv.current().file.tasks.array().sort((a,b)=>(ord[a.status]??9)-(ord[b.status]??9));
const el = dv.el('div','');
el.innerHTML = tasks.map(t=>{
  const [label,fg,bg] = meta[t.status] || ["?","var(--text-muted)","var(--background-modifier-border)"];
  return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;">
    <span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span>
    <span>${linkify(t.text)}</span></div>`;
}).join("");
```

> [!example]- Fuente de tareas — editar / mover de estado aquí
> - [x] Fix [[java-polycard-sdk]] #owner/me #type/dev #area/meli #sprint/A26Q2S7 📅 2026-06-24 ✅ 2026-06-25
> - [x] Fix [[search-middleware]] #owner/me #type/dev #area/meli #sprint/A26Q2S7 📅 2026-06-24 ✅ 2026-06-25
> - [x] Fix [[recommendations-decoration-sdk]] #owner/me #type/dev #area/meli #sprint/A26Q2S7 📅 2026-06-24 ✅ 2026-06-26
> - [x] Fix [[recommendations-middleend]] #owner/me #type/dev #area/meli #sprint/A26Q2S7 📅 2026-06-24 ✅ 2026-07-03
> - [x] Fix [[feed-cheshire]] #owner/me #type/dev #area/meli #sprint/A26Q2S7 📅 2026-06-24 ✅ 2026-07-01
> - [x] [[Single View Layout — Migración al Polycard SDK]] arrancar + seguimiento #owner/me #type/supervision #area/meli #sprint/A26Q2S7 ✅ 2026-07-07
> - [r] [[Título Compuesto Motors — Short Version y Dedup]] arrancar + seguimiento #owner/me #type/supervision #area/meli #sprint/A26Q2S7 📅 2026-07-09
> - [r] [[Tests de Contrato Polycard Search Motors]] arrancar + seguimiento #owner/me #type/supervision #area/meli #sprint/A26Q2S7 📅 2026-07-10

## 📋 Tablero

#### 🟦 To Do
```tasks
sort by priority
path includes Refactor Polycard
status.name includes Todo
short mode
hide task count
```

#### 🟡 WIP
```tasks
sort by priority
path includes Refactor Polycard
status.name includes WIP
short mode
hide task count
```

#### 🔵 Review
```tasks
sort by priority
path includes Refactor Polycard
status.name includes Review
short mode
hide task count
```

#### ✅ Done
```tasks
path includes Refactor Polycard
done
short mode
hide task count
```

## 📆 Bitácora

- **2026-06-24** — Proyecto creado con los 5 fixes de Polycard.
- **2026-07-03** — Nace subproyecto de agente [[Single View Layout — Migración al Polycard SDK]]: mover la personalización de orden del Single view (Motors/VIS) de search-middleware al Polycard SDK (pedido del TL de Search). Ramas `feature/single-view-layout-sdk-migration` creadas en ambos repos; ejecución delegada a IA.
- **2026-07-09** — La tarea suelta "Crear versión solo title {BRAND} {MODEL} {SHORT_VERSION} {VEHICLE_YEAR}" se extendió (título compuesto Motors + problema de repetición de palabras) y pasa a subproyecto de agente [[Título Compuesto Motors — Short Version y Dedup]]. Ejecución del dedup delegada a IA; pendientes de investigación de caché/coverage quedan como `#owner/me`.
- **2026-07-15** — [[Título Compuesto Motors — Short Version y Dedup]] queda en **code review**: el PR del SDK contiene el título corto de Motors con fallback `SHORT_VERSION/TRIM`, deduplicación de tokens y guardrail de 45 caracteres; la integración del consumidor omite el subtítulo para evitar duplicar la versión. La tarea puente pasa a Review.

## 🧭 Decisiones

- 

## 🔗 Docs / Links

- Apps: [[java-polycard-sdk]] · [[search-middleware]] · [[recommendations-decoration-sdk]] · [[recommendations-middleend]] · [[feed-cheshire]]

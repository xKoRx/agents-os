---
type: project
owner: me
root: true
cssclasses:
  - wide
status: active
priority: P1
area: "[[Meli]]"
parent:
sprint: "[[A26Q2]]"
start: 2026-05-28
due:
progress: 0
repo: vis-items-loader-tagging, search-middleware, java-polycard-sdk, vis-octopus-lib, vpp-backend
jira: VMDUPPER-5, VISMDMID-4
prs:
tags:
  - area/meli
  - kind/project
created: 2026-06-23
updated: 2026-07-01
aliases:
  - previous-price-motors
  - Pricing Motors
---
# Destaques de Precio

> [!info]+ Destaques de Precio
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** [[A26Q2S7]]
> Iniciativa **Pricing Motors** (VIS Motors Demand): dos señales de pricing para Motors.

## 🎯 Objetivo

- Mostrar señales de precio en Motors: **Hito 1 — Bajó de Precio** (`PREVIOUS_PRICE`, ya desarrollado) e **Hito 2 — [[Bajo y Muy Bajo Precio]]** (en MLB, destaque único vía FIPE; en el resto de sites, tiers `BAJO` / `MUY BAJO` vía Sugeridor 2.0; en continuación).
- Regla de jerarquía: si el destaque de Hito 2 está activo, Bajó de Precio (Hito 1) queda suprimido.

## 📊 Estado actual

- **Hito 1 — Bajó de Precio**: desarrollo terminado en los 5 componentes, en **code review**.
- **Hito 2 — [[Bajo y Muy Bajo Precio]]**: propuesta de continuación, en fase de diseño. Desde 2026-06-30 el diseño de este mismo proyecto se ramifica por site: MLB (destaque único FIPE, bloqueado por lista de exclusión marca/modelo/año y rango de elegibilidad a confirmar) y resto de sites (2 tiers vía Sugeridor 2.0, falta cliente bypass-cache y proceso masivo). Detalle en el RFC.

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

## ✅ Tareas de la iniciativa (mías + puentes, por subproyecto)

%% Vista humana: solo #owner/me (incluye tareas puente #type/supervision), agrupada por subproyecto. Las tareas de agente NO se muestran acá; viven en su proyecto de agente. %%

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
const ord={" ":0,"/":1,"r":2,"x":3,"X":3,"-":4};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
let any=false;
for(const p of dv.pages('"10-projects/Destaques de Precio"').sort(x=>x.file.name)){
  const t=p.file.tasks.array().filter(x=>has(x,"owner/me")&&x.status!=="x"&&x.status!=="X").sort((a,b)=>(ord[a.status]??9)-(ord[b.status]??9));
  if(t.length){any=true;dv.el('h4',p.file.link);render(t);}
}
if(!any)dv.paragraph("_Sin tareas mías abiertas en la iniciativa._");
```

> [!example]- Fuente de tareas (iniciativa) — editar aquí
> - [/] Confirmar pendientes de definición del RFC (bordes de tier, scope #MLM / #MLB, storage de `origin`) #owner/me #type/research #area/meli #sprint/A26Q2S7 📅 2026-07-03
> - [ ] Coordinar rollout: dry-run #MLA → #MLM → #MLB #owner/me #type/admin #area/meli
> - [x] [[search-middleware]] revisar experiencia rota #owner/me #type/dev #area/meli 📅 2026-06-25
> - [x] [[vpp-backend]] revisar experiencia rota y responder code review #owner/me #type/dev #area/meli 📅 2026-06-25

## 📋 Tablero

#### 🟦 To Do
```tasks
sort by priority
path includes 10-projects/Destaques de Precio
tags do not include #owner/agent
status.name includes Todo
short mode
hide task count
```

#### 🟡 WIP
```tasks
sort by priority
path includes 10-projects/Destaques de Precio
tags do not include #owner/agent
status.name includes WIP
short mode
hide task count
```

#### 🔵 Review
```tasks
sort by priority
path includes 10-projects/Destaques de Precio
tags do not include #owner/agent
status.name includes Review
short mode
hide task count
```

#### ✅ Done
```tasks
sort by priority
path includes 10-projects/Destaques de Precio
tags do not include #owner/agent
done
short mode
hide task count
```

## 📆 Bitácora

- **2026-06-23** — Migrada la iniciativa a Obsidian desde el RFC. Refinamiento: nuevo Sugeridor aún no desplegado en MLB.
- **2026-06-30** — Reunión de equipo: FIPE en MLB está mal catalogado en algunos ítems (Cris: vehículos verificados podrían tener el FIPE correcto porque los proveedores lo devuelven en validaciones históricas). Decisión: MLB pivota a **un solo destaque basado en precio FIPE** (ya no Sugeridor); el resto de los sites mantiene full compatibilidad Sugeridor 2.0 con los **2 destaques** (`BAJO`/`MUY_BAJO`) sin FIPE. Se menciona un rango ilustrativo (no confirmado) de -10%/-1% vs FIPE para el destaque de MLB. El equipo va a revisar góndola vs FIPE por marca/modelo/año para armar una lista que excluya ítems mal catalogados — en curso, sin ETA. RFC actualizado con el detalle y los puntos abiertos.

## 🧭 Decisiones

- Elegibilidad server-side; Search/VIP no calculan tier.
- Sugeridor 2.0 como fuente de verdad; no se valida FIPE — **excepto MLB desde 2026-06-30**, donde FIPE es la fuente del destaque único.
- Reproceso masivo cubre **todo Motors** (sin allowlist de dominio); desde 2026-06-30 la fuente de cálculo se ramifica por site (FIPE en MLB, Sugeridor en el resto).

## 🔗 Docs / Links

- [RFC Pricing Motors](file:///Users/rjara/fuentes/second-brain/sb-main/01_Projects/previous-price-motors/rfc.md)
- Carpeta del repo: `~/fuentes/second-brain/sb-main/01_Projects/previous-price-motors/`

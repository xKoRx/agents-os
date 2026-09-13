---
type: project
owner: agent
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo Forge]]"
sprint:
start: 2026-06-28
due:
progress: 100
repo: "github.com/xKoRx/symphony"
jira:
prs:
aliases:
  - Echo Forge WFM Troubleshooting
  - echo-forge-wfm-troubleshooting
tags:
  - application/echoforge
  - area/symphony
  - kind/project
created: "2026-06-28"
updated: "2026-06-29"
---

# Echo Forge WFM Troubleshooting

> [!info]+ Echo Forge WFM Troubleshooting
> **Área:** [[Symphony]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** —

## 🎯 Objetivo

Resolver los atascos en el pipeline de optimización de Walk-Forward (WFM) en Temporal causados por el descarte de estrategias robustas y discrepancia de claves de base de datos vs. claves hasheadas de Temporal.

## 📊 Estado actual

- Desarrollada una solución robusta y dinámica en las actividades `verify_wfm_extracted` y `evaluate_wfm` del worker.
- Compilado y desplegado el worker en la versión `0.1.34` en el host Zeus, solucionando el bucle de reinicio infinito en el stager de actualización.
- Verificada la ejecución exitosa de todo el pipeline y la finalización completa de los 13 subflujos y el flujo principal en Temporal.

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
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. %%
> - [x] Modificar verify_wfm.go para admitir descarte legítimo de matrices en base de datos. #owner/agent #type/dev
> - [x] Resolver discrepancia entre claves legibles e hasheadas dinámicamente usando MongoDB metadata. #owner/agent #type/dev
> - [x] Modificar evaluate_wfm.go para retornar veredicto FAIL de forma grácil sin fallar la actividad. #owner/agent #type/dev
> - [x] Compilar y desplegar versión 0.1.33 en Zeus. #owner/agent #type/dev
> - [x] Monitorear ejecución en Zeus y verificar destrabe de tareas en Temporal. #owner/agent #type/dev
> - [x] Documentar skills de troubleshooting en Obsidian. #owner/agent #type/doc

## 📆 Bitácora

- **2026-06-28** — Modificadas las actividades de WFM (`verify_wfm.go`, `evaluate_wfm.go`) e inyectadas interfaces faltantes en `main.go`. Generada la versión `0.1.33` y subida a Zeus.
- **2026-06-29** — Detectado bucle infinito de reinicio en el stager de actualización por formato de PENDING en texto plano. Desarrollada y testeada la versión `0.1.34` con soporte robusto de fallback para PENDING crudo y JSON. Desplegada en Zeus, solucionando el reinicio constante del worker. Verificada la finalización exitosa de los 13 subflujos y del flujo principal en Temporal sin atascos ni errores. Documentada la solución en la skill de troubleshooting en Obsidian. Proyecto completado al 100%.

## 🧭 Decisiones

- **Decisión 1:** Cargar parámetros reales de WFM de la base de datos MongoDB al vuelo usando matrices existentes para evitar errores de claves generadas por discrepancia de parámetros.

## 🔗 Docs / Links

- [[Symphony]]
- [[Echo Forge]]

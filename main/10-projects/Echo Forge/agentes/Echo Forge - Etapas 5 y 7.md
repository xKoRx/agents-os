---
type: project
owner: agent
root: false
cssclasses:
  - wide
status: active
priority: P2
area: "[[Echo]]"
parent: "[[Echo Forge]]"
sprint:
start:
due:
progress: 20
repo: symphony
jira:
prs:
tags:
  - area/echo
  - kind/project
created: 2026-06-27
updated: 2026-08-06
aliases:
  - Echo Forge - Etapas 5 y 7
  - Echo Forge - Etapas 5-7
---
# Echo Forge - Etapas 5 y 7: Backtracking y Reporte de Wave

> [!info]+ Echo Forge - Etapas 5 y 7: Backtracking y Reporte de Wave
> **Padre:** [[Echo Forge]] · **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P2 · **Progreso:** 20%
> Bucle adaptativo con backtracking por tipo lógico y consolidación de reportes de Wave. La validación real en MT5 (Etapa 6) vive en [[Echo Forge - Etapa 6]].

## 🎯 Objetivo

- Cerrar el ciclo adaptativo del pipeline inyectando estrategias rechazadas de vuelta al builder, y generar el reporte final que audite toda la Wave.

## 📊 Estado actual

- **WIP (20%)**: la Etapa 6 se separó a su propio proyecto de agente el 2026-08-06 ([[Echo Forge - Etapa 6]]), donde vive el diseño de las tareas `mt5_compiler` y `mt5_backtesting`. Este proyecto conserva únicamente Etapa 5 (backtracking adaptativo por tipo lógico y tick retest) y Etapa 7 (reporte consolidado de Wave). Resta formalizar el backtracking dinámico de reintento en el workflow oficial, definir el linaje físico y sidecars en MinIO, y diseñar la activity de `WaveReporting`.

## ✅ Tareas

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
const ord={" ":0,"/":1,"r":2,"x":3,"X":3,"-":4};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
const tasks=dv.current().file.tasks.array().sort((a,b)=>(ord[a.status]??9)-(ord[b.status]??9));
const el=dv.el('div','');
el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");
```

> [!example]- Fuente de tareas — editar / mover de estado aquí
> - [x] **Completadas en el Repositorio**
>   - [x] [[echo-forge]] Agregar la etapa `tick_retest` a la activity `Project` de SQX #owner/agent #type/dev #area/echo
> - [ ] **Etapa 5: Backtracking adaptativo**
>   - [ ] [[echo-forge]] Implementar backtracking adaptativo por tipo lógico (reinyección y pools) en el workflow Temporal de producción #owner/agent #type/dev #area/echo
>   - [ ] [[echo-forge]] Configurar persistencia de finalistas y lineage de 7 eslabones en MinIO y MongoDB #owner/agent #type/dev #area/echo
> - [ ] **Etapa 7: Reporte de Wave**
>   - [ ] [[echo-forge]] Diseñar y desarrollar la activity de reporte consolidado `WaveReporting` en Go/MongoDB #owner/agent #type/dev #area/echo
> - [-] **Movido a [[Echo Forge - Etapa 6]]**
>   - [-] [[echo-forge]] Compilación y backtesting MT5 en worker Windows + filtro de desviación #owner/agent #type/dev #area/echo

## 📋 Tablero

#### 🟦 To Do
```tasks
sort by priority
path includes Echo Forge - Etapas 5 y 7
status.name includes Todo
short mode
hide task count
```

#### 🟡 WIP
```tasks
sort by priority
path includes Echo Forge - Etapas 5 y 7
status.name includes WIP
short mode
hide task count
```

#### 🔵 Review
```tasks
sort by priority
path includes Echo Forge - Etapas 5 y 7
status.name includes Review
short mode
hide task count
```

#### ✅ Done
```tasks
sort by priority
path includes Echo Forge - Etapas 5 y 7
done
short mode
hide task count
```

## 📆 Bitácora

- **2026-08-06** — Reencuadre de alcance: Etapa 6 (compilación y backtesting MT5) se separó a su propio proyecto de agente, [[Echo Forge - Etapa 6]]. Este proyecto se renombró de "Etapas 5-7" a "Etapas 5 y 7" y quedó con backtracking adaptativo y reporte de Wave. Progreso recalculado de 40% a 20% porque el avance que lo sostenía (worker MT5 y filtro de desviación) migró al proyecto nuevo.

## 🔗 Docs / Links

- [[Echo Forge]] (programa padre)
- [[Echo Forge - Etapa 6]] (validación MT5, separada de este proyecto)
- [[echo-forge]] (Aplicación)
- `specs/FEAT-SQX-ADAPTIVE-WORKFLOW/SPEC.md` — backtracking adaptativo
- `specs/FEAT-SQX-FINALIST-ARTIFACTS-LINEAGE/SPEC.md` — lineage de finalistas
- `specs/FEAT-SQX-WAVE-REPORTING/SPEC.md` — reporte consolidado de Wave
- `reports/echo-forge/ECHO_FORGE_STAGE_4_IMPLEMENTATION_REPORT.md`

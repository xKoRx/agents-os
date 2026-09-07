---
type: project
owner: agent
root: false
cssclasses:
  - wide
status: completed
priority: P3
area: "[[Echo]]"
parent: "[[Echo Forge]]"
sprint: "[[A26Q2S7]]"
start: 2026-06-12
due: 2026-06-27
progress: 100
repo: symphony
jira:
prs:
tags:
  - area/echo
  - kind/project
created: 2026-06-27
updated: 2026-06-27
aliases:
  - Echo Forge - Etapas 1-3
---
# Echo Forge - Etapas 1-3: Cimientos y WFM

> [!info]+ Echo Forge - Etapas 1-3: Cimientos y WFM
> **Padre:** [[Echo Forge]] · **Área:** [[Echo]] · **Estado:** completed · **Prioridad:** P3 · **Progreso:** 100%
> Fase de cimentación, extracción física de metadatos, clasificación adaptativa y evaluador Go de Walk-Forward Matrix (WFM).

## 🎯 Objetivo

- Establecer el canal físico de datos desde StrategyQuant, clasificar estrategias según su comportamiento, y validar la estabilidad paramétrica mediante WFM evaluado de manera determinista en Go.

## 📊 Estado actual

- **Completado**: El pipeline realiza el intake de candidatos, descarga las estrategias, extrae las grillas WFM e infiere estabilidad con warnings de variabilidad, outliers, picos aislados e inconsistencias OOS. Todos los componentes y actividades de Temporal fueron verificados con unit tests robustos.

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
> - [x] **Etapa 1: Cimientos y Extracción Física**
>   - [x] Resolver API de plugins de SQ (NI-JP-1) mediante spike #owner/me #type/research #area/echo
>   - [x] Crear plugin Java unificado `echo-forge-sqx-exporter-plugin` con MetadataExporter #owner/me #type/dev #area/echo
>   - [x] Crear esquema y configurar colecciones de MongoDB (`wfm_runs`, `wfm_matrices`, etc.) con índices contractuales #owner/me #type/dev #area/echo
> - [x] **Etapa 2: Clasificación e Ingesta Adaptativa**
>   - [x] Desarrollar motor de clasificación por firma lógica en Go #owner/me #type/dev #area/echo
>   - [x] Implementar ranking multi-criterio y re-ranking #owner/me #type/dev #area/echo
>   - [x] Diseñar e integrar flujo de intake en el workflow de Temporal #owner/me #type/dev #area/echo
> - [x] **Etapa 3: WFM y Evaluador Go**
>   - [x] Agregar `WFMMatrixExporter` al plugin Java y gate `verify_wfm_extracted` #owner/me #type/dev #area/echo
>   - [x] Implementar el Evaluador Go de estabilidad con vecindario de 3x3 y warnings globales/locales #owner/me #type/dev #area/echo
>   - [x] Desarrollar chequeos de consistencia y warnings de OOS (outliers, variabilidad, picos aislados) #owner/me #type/dev #area/echo
>   - [x] Crear actividades de validación Temporal (`verify_wfm_extracted` y `verify_wfm_evaluated`) #owner/me #type/dev #area/echo
>   - [x] Correr suite de pruebas con race detector y validación de cobertura al 100% de la lógica nueva #owner/me #type/dev #area/echo

## 📋 Tablero

#### 🟦 To Do
```tasks
sort by priority
path includes Echo Forge - Etapas 1-3
status.name includes Todo
short mode
hide task count
```

#### 🟡 WIP
```tasks
sort by priority
path includes Echo Forge - Etapas 1-3
status.name includes WIP
short mode
hide task count
```

#### 🔵 Review
```tasks
sort by priority
path includes Echo Forge - Etapas 1-3
status.name includes Review
short mode
hide task count
```

#### ✅ Done
```tasks
path includes Echo Forge - Etapas 1-3
done
short mode
hide task count
```

## 📆 Bitácora

- **2026-06-15** — Ajuste conceptual de arquitectura (plugin Java como exportador tonto, Go motor de decisión).
- **2026-06-27** — Culminación exitosa de la Etapa 3 y validación del 100% de los tests de WFM.

## 🧭 Decisiones

- Renombrar `RobustRunExporter` y `robust_runs` a `WFMRunsExporter` y `wfm_runs` para evitar acoplamiento de lógica en Java.
- Mapear warnings de WFM de manera transparente en la base de datos documental (`WaveReportStore` / `wfm_evaluations`).

## 🔗 Docs / Links

- [[echo-forge]] (Aplicación)
- [Stage 3 Implementation Report](file:///Users/rjara/go/src/github.com/xKoRx/symphony/reports/echo-forge/ECHO_FORGE_STAGE_3_IMPLEMENTATION_REPORT.md)

---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P0
area: "[[Echo]]"
parent:
sprint:
start: 2026-09-23
due:
progress: 5
repo: xKoRx/symphony
jira:
prs:
aliases:
  - Echo Forge Operacion Real V2
  - Forge V2
tags:
  - kind/project
  - area/echo
created: "2026-09-23"
updated: "2026-09-23"
---

# Echo Forge — Operación Real V2

%% Naming: Echo Forge — Operación Real V2 es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo Forge — Operación Real V2
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P0 · **Repo:** `xKoRx/symphony`
> Sucesor operativo de [[Echo Forge]] (V1 CLOSED / FOUNDATION COMPLETE 2026-09-23): operar Forge con estrategias reales, con el desarrollo futuro dirigido por campañas.

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> `owner: me` → **proyecto humano**: la iniciativa/esfuerzo que conduces tú.
> `owner: agent` → **proyecto de agente**: un curro delegado, con detalle pesado que escribe y sigue un agente. Casi siempre es subproyecto de uno humano y vive en la subcarpeta `agentes/` de su iniciativa.
> `root: true` solo en **iniciativas raíz** (sin `parent`). Todo subproyecto debe setear `parent`; si no, aparece como huérfano en [[Panel de Proyectos]].
>
> **Tarea puente:** cuando este proyecto es `owner: agent`, en su proyecto **padre** debe existir UNA sola tarea humana que lo representa (arrancar + seguimiento). Así tu cockpit ve una línea por curro delegado, no las tareas internas del agente. Ejemplo, en el padre:
> `- [ ] [[Echo Forge — Operación Real V2]] arrancar + seguimiento #owner/me #type/supervision #area/personal`

## 🎯 Objetivo

- Operar Forge con estrategias auténticas, evolucionar ranking/selection con evidencia de campañas reales, estabilizar el funnel completo (Import → Classification → Ranking → Selection → Campaña B → SQX Tick → MT5) y construir la nueva integración Forge→Echo compatible con The Lab V3. El desarrollo futuro es dirigido por campañas reales, no por el roadmap histórico de construcción (cerrado con [[Echo Forge]] V1).

## 📊 Estado actual

- **CREADO (2026-09-23, mandato manager).** Consolidación completada en la misma ventana: `origin/master @ d07cc69` (master único local y remoto; 14 ramas cerradas eliminadas, 19 worktrees eliminados, cero pérdida — tips verificados en master o tags `archive/*`; material no trackeado único preservado en `~/aranea/work/forge-consolidation-20260923/preserved/`). Campaña B CB-G2 (resolver `selection_cohort`) integrada a master con gate 4/4 (build PASS, tests del delta PASS, fail-set 37/37 idéntico al baseline `9a69243`, review scoped PASS). Release candidate **0.2.106** publicada desde master consolidado (`deploy_release.sh --release-only`). La integración Forge→Echo histórica (contrato Echo SDK V1) queda `SUPERSEDED_BY_INTEGRATION_V2` — no se termina bajo el contrato viejo (ver Track C).
- **NEXT EXACT: procesar el primer cohort real mediante Watcher Import** (= arrancar [[Echo Forge — Campaign 001]]).

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/symphony | `master` @ `d07cc69` (origin, único) | RC 0.2.106 publicada | Mandato manager 2026-09-23 (cierre V1 → operación real V2) + mandatos por campaña | `specs/FEAT-SQX-IMPORT-TASK-V1/SPEC.md` · `specs/FEAT-SQX-IMPORT-CAMPAIGN-B/SPEC.md` · specs F-0x vigentes | **Fundación completa; operación dirigida por campañas** |

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

> [!note]+ Ownership y tarea puente
> `#owner/me` = tuya · `#owner/agent` = de un agente · sin owner = clasifícala.
> El board es **adaptativo según `owner` del frontmatter**:
> - **Proyecto humano** (`owner: me`): muestra tus tareas y las **tareas puente** (`#type/supervision`) que representan proyectos de agente. Las tareas de agente **no** aparecen acá; viven en su propio proyecto.
> - **Proyecto de agente** (`owner: agent`): muestra las tareas del agente.

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. Tipos: #type/dev #type/admin #type/research #type/pr-review #type/supervision. Flags: #blocked #waiting #urgent. Ver [[convenciones]]. %%
> - [ ] [[Echo Forge — Campaign 001]] arrancar + seguimiento #owner/me #type/supervision #area/echo
> - [ ] **Track A — REAL CAMPAIGNS**: ejecutar campañas reales end-to-end (Import → Classification → Ranking → Selection → Campaign B → SQX Tick → MT5); cada campaña = subproyecto con evidencia durable #owner/agent #type/dev #area/echo
> - [ ] **Track B — FUNNEL QUALITY**: versionar y comparar classification, ranking algorithms, weights, thresholds y selection policies; toda iteración conserva input/output y versión (comparación por refs, sin reescritura) #owner/agent #type/dev #area/echo
> - [ ] **Track C — INTEGRATION V2**: definir e implementar el nuevo boundary Forge → Echo (históricos SQX + MT5 + operaciones + evidence → ingestion/normalization Echo → canonical operations → The Lab curves/analytics/portfolios). Forge NO es autoridad de curvas finales. Reemplaza la integración histórica (SUPERSEDED_BY_INTEGRATION_V2); requiere SPEC funcional nueva aprobada por owner antes de implementar #owner/me #type/dev #area/echo
> - [ ] Pendientes owner heredados de Campaña B: CB-G1 review manager + freeze §3 (período OOS, tick model, parámetros MT5, criterios A-vs-B) — gate de ejecución física de Campaña B en [[Echo Forge — Campaign 001]] #owner/me #blocked #area/echo

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label]of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any)dv.paragraph("_Sin tareas._");}
const owner=((dv.current().owner)==="agent")?"agent":"me";
const all=dv.current().file.tasks.array();
const primary=all.filter(t=>has(t,`owner/${owner}`));
const loose=all.filter(t=>!has(t,"owner/me")&&!has(t,"owner/agent"));
dv.header(3, owner==="agent"?"🤖 Tareas del agente":"🧍 Mis tareas");
board(primary);
if(loose.length){dv.header(3,"🧺 Sin owner (clasificar)");render(loose);}
```

%% Rollup de iniciativa — descomentar solo en proyectos padre para ver las tareas #owner/me (incluye puentes) de todos los subproyectos, agrupadas por nota. Cambiar la ruta por la carpeta de esta iniciativa. Nunca muestra tareas de agente.
```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
const ord={" ":0,"/":1,"r":2,"x":3,"X":3,"-":4};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
const pages=dv.pages('"10-projects/CARPETA-DE-LA-INICIATIVA"');
for(const p of pages.sort(x=>x.file.name)){const t=p.file.tasks.array().filter(x=>has(x,"owner/me")&&x.status!=="x"&&x.status!=="X").sort((a,b)=>(ord[a.status]??9)-(ord[b.status]??9));if(t.length){dv.el('h4',p.file.link);render(t);}}
```
%%

## 📆 Bitácora

%% Log diario para las dailies. Una línea por día con lo avanzado / blockers. %%
- **2026-09-23** — Proyecto creado por mandato manager (cierre Echo Forge V1 → operación real V2). Misma ventana: master consolidado @ `d07cc69` (Campaña B integrada con gate 4/4, ramas/worktrees cerrados eliminados, manifiesto 0.2.105 preservado), RC 0.2.106 publicada, V1 cerrado como FOUNDATION COMPLETE, integración histórica marcada SUPERSEDED_BY_INTEGRATION_V2, [[Echo Forge — Campaign 001]] creado. Siguiente exacto: primer cohort real vía Watcher Import.

## 🧭 Decisiones

- **D-V2-1 (2026-09-23): no reabrir features históricas sin defecto material.** El roadmap de construcción queda cerrado con V1; todo trabajo nuevo nace de una campaña real o de un defecto material observado en operación.
- **D-V2-2 (2026-09-23): integración Forge→Echo histórica = SUPERSEDED_BY_INTEGRATION_V2.** No se termina bajo el contrato Echo SDK V1; Track C diseña el boundary nuevo compatible con The Lab V3, donde Forge no es autoridad de curvas finales.
- **D-V2-3 (2026-09-23): Campaña B arranca de un SelectionSnapshot durable.** No reimporta ni reselecciona: SelectionSnapshot → SQX Tick Retest OOS → MT5 Export → Compile → Real-Tick Backtest → Reconcile/Fidelity → Final Decision/Report. El resolver `selection_cohort` (CB-G2 @ `dc151e4`) ya está en master.

## 🔗 Docs / Links

- Predecesor: [[Echo Forge]] (V1 CLOSED / FOUNDATION COMPLETE) · Subproyecto: [[Echo Forge — Campaign 001]] · Campaña B: [[Echo Forge — Campaña B]] · Import: [[Echo Forge — Import Task V1]]
- Entidad: [[echo-forge]] · Integración histórica: [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]] (SUPERSEDED para integración) · Boundary nuevo por diseñar en Track C

## 💡 Ideas

%% Captura ideas sueltas del proyecto al final. Si maduran, promover a tarea o a nota de idea (70-templates/idea.md). %%

### Backlog de ideas

- 

### Motivos / principios

- 

### Memoria pública / interna

%% Opcional para proyectos de agentes o conocimiento: definir qué memoria gobierna el sistema y cuál gobierna el agente, y por qué existe cada una. %%
- **Memoria pública:** 
- **Memoria interna:** 
- **Motivo:** 

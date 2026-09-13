---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Personal]]"
parent: "[[AGENTS OS]]"
sprint:
start:
due:
progress: 0
repo:
jira:
prs:
aliases:
  - Agents OS Context Hygiene
  - Context Hygiene and Canonical Integrity
tags:
  - kind/project
  - area/personal
  - project/agents-os
created: "2026-09-13"
updated: "2026-09-13"
---

# AGENTS OS - Context Hygiene and Canonical Integrity

%% Naming: AGENTS OS - Context Hygiene and Canonical Integrity es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ AGENTS OS - Context Hygiene and Canonical Integrity
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** —
> _parent / sprint / repo / jira / prs son opcionales._

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> `owner: me` → **proyecto humano**: la iniciativa/esfuerzo que conduces tú.
> `owner: agent` → **proyecto de agente**: un curro delegado, con detalle pesado que escribe y sigue un agente. Casi siempre es subproyecto de uno humano y vive en la subcarpeta `agentes/` de su iniciativa.
> `root: true` solo en **iniciativas raíz** (sin `parent`). Todo subproyecto debe setear `parent`; si no, aparece como huérfano en [[Panel de Proyectos]].
>
> **Tarea puente:** cuando este proyecto es `owner: agent`, en su proyecto **padre** debe existir UNA sola tarea humana que lo representa (arrancar + seguimiento). Así tu cockpit ve una línea por curro delegado, no las tareas internas del agente. Ejemplo, en el padre:
> `- [ ] [[AGENTS OS - Context Hygiene and Canonical Integrity]] arrancar + seguimiento #owner/me #type/supervision #area/meli`

## 🎯 Objetivo

- Dotar a Agents-OS de dos mecanismos reproducibles que complementen (sin duplicar) al Conformance Harness: **PHASE 2 — Context Budget + Domain Leak Auditor** (medir el contexto que carga el sistema por scope DEFAULT/MELI/ARANEA, detectar contexto innecesario, contaminación entre dominios y cambios de contexto al cambiar de dominio) y **PHASE 3 — Canonical / Deprecation Linter** (linter determinista de higiene documental: canonicalidad, deprecación, archive, links, routing, metadata, hot-path). Ambos con diseño → spec parent → implementación → verificación adversarial, máximo 2 ciclos de corrección, sin auto-corregir el sistema bajo prueba, y exponiendo records compatibles con una futura integración `agents-os doctor` (fuera de alcance).

## 📊 Estado actual

- **2026-09-13 — Ejecución en curso.** Baseline: Conformance Harness entregado (PASS 4 · FAIL 1 [F1] · WARN 4 · SKIP 17), Agents-OS revision `a6a503f` como ancestro del HEAD vivo. Proyecto creado como único planificador de PHASE 2 + PHASE 3. Paso actual: P2-A (Context Budget Auditor/Designer).

## 🧱 Entrega de desarrollo

_No aplica — el tooling vive como scripts/tests dentro del vault bajo `80-agents/tools/`; no toca repos de aplicaciones._

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
> - [ ] P2-A — Context Budget Auditor/Designer: analizar bootstrap, packs MELI/ARANEA, DEFAULT, harness y filesystem; clasificar EXACT/ESTIMATED/INFERRED/UNOBSERVABLE; diseñar métricas y escenarios → `80-agents/tools/context-budget/artifacts/p2-context-budget-design.md` #owner/agent #type/research #area/personal
> - [ ] PARENT GATE P2 — reconciliar design contra harness, definir spec (métricas, métodos, escenarios, semántica PASS/WARN/FAIL/SKIP, schema) → `80-agents/tools/context-budget/artifacts/p2-context-budget-spec.md` #owner/agent #type/admin #area/personal
> - [ ] P2-B — Context Budget Implementer: tool en `80-agents/tools/context-budget/`, reutilizando contratos del harness, ejecución DEFAULT/MELI/ARANEA cold/warm/switch #owner/agent #type/dev #area/personal
> - [ ] P2-C — Context Budget Adversarial Verifier → `80-agents/tools/context-budget/artifacts/p2-adversarial-verification.md` #owner/agent #type/research #area/personal
> - [ ] P2-D — Context Budget Fixer (sólo si hay defectos materiales del auditor; máx 2 ciclos) #owner/agent #type/dev #area/personal
> - [ ] PHASE 2 acceptance gate + cierre de fase en esta nota #owner/agent #type/admin #area/personal
> - [ ] P3-A — Canonical Integrity Designer: extraer modelo canonical/deprecation de autoridades vigentes, clasificar MACHINE-DETERMINISTIC/HEURISTIC/HUMAN-REVIEW → `80-agents/tools/canonical-linter/artifacts/p3-canonical-model.md` #owner/agent #type/research #area/personal
> - [ ] PARENT GATE P3 — spec del linter (check IDs, severidad, determinismo, evidencia, exclusiones, formato) → `80-agents/tools/canonical-linter/artifacts/p3-canonical-linter-spec.md` #owner/agent #type/admin #area/personal
> - [ ] P3-B — Canonical Linter Implementer: linter determinista en `80-agents/tools/canonical-linter/` reutilizando tooling de schema existente #owner/agent #type/dev #area/personal
> - [ ] P3-C — Canonical Linter Adversarial Verifier → `80-agents/tools/canonical-linter/artifacts/p3-adversarial-verification.md` #owner/agent #type/research #area/personal
> - [ ] P3-D — Canonical Linter Fixer (sólo si hay defectos materiales; máx 2 ciclos) #owner/agent #type/dev #area/personal
> - [ ] PHASE 3 acceptance gate + estado final del proyecto (IMPLEMENTATION COMPLETE / OWNER REVIEW) #owner/agent #type/admin #area/personal

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
- **2026-09-13** — 

## 🧭 Decisiones

- 

## 🔗 Docs / Links

- 

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

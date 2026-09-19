---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Personal]]"
parent: "[[Loom]]"
sprint:
start: 2026-09-19
due:
progress: 0
repo: xKoRx/loom
jira:
prs:
aliases:
  - Loom v0.5
  - FEAT-LOOM-V05
  - Daily Operations Center
tags:
  - kind/project
  - area/personal
  - agent/owner
created: "2026-09-19"
updated: "2026-09-19"
cssclasses:
  - wide
---

# Loom — Product v0.5

%% Naming: Loom — Product v0.5 es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Loom — Product v0.5
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Loom]] · **Repo:** `xKoRx/loom` (**VERIFIED** 2026-09-19; base `feature/loom-v04 @ cead63c` INTEGRITY_PASS certificada; master `848fb28` intacto)
> Subproyecto de agente: **Daily Operations Center** — mandato maestro 2026-09-19. Convierte Loom en el centro de operaciones diario: (1) Human Action Center — aprobaciones humanas derivadas EXCLUSIVAMENTE de tareas puente canónicas (`#owner/me #type/supervision` en review con relación verificable al subproyecto de agente), con casos incompletos diagnosticados y revisiones genéricas separadas; (2) Project Command Center — ProjectView extendido con la jerarquía estado → próxima acción → hito → tareas humanas → entregas a review → bloqueos → subproyectos → docs; (3) Resume Context — acción contextual read-only que reúne continuidad verificable del snapshot; (4) Smart Collections MVP documentado (implementación sólo si P0 integrado y presupuesto resta). Read-only siempre: sin writer, sin merge a master, sin editar el schema canónico.

## 🎯 Objetivo

- Convertir Loom en el centro de operaciones diario que responde: qué requiere intervención humana, en qué punto está cada proyecto, y cómo retomar exactamente el trabajo interrumpido.
- El conjunto primario de aprobaciones humanas deriva de tareas puente canónicas: Owner `me` · Tipo `supervision` · Estado `review` · relación verificable con subproyecto de agente (validado contra [[agents-os-agent-project-workflow|la skill canónica]] y OPERATIONAL-CONTRACT §5). Nunca todas las `[r]`; las revisiones genéricas quedan separadas.
- Cada intervención muestra, cuando existe: proyecto padre, subproyecto de agente, tarea puente, estado documentado, motivo/descripción, último hito verificable y enlaces a fuentes. Si una relación no se resuelve, el caso se presenta como INCOMPLETO, nunca como aprobación inequívoca. Sin botones de aprobación/rechazo que aparenten persistir.
- ProjectView se extiende (no segunda pantalla) con la jerarquía del mandato; la próxima acción NO se infiere desde la primera tarea abierta sin regla contractual (los compromisos del plan diario de hoy SÍ son contractuales, ver DAILY-PLAN-FORMAT); el estado del padre nunca se deriva del de sus hijos; timestamps no se transforman en afirmaciones de avance.
- Resume Context reúne exclusivamente información verificable del snapshot (estado documentado, última entrada de bitácora identificable, próxima acción si existe, bloqueos, reviews, docs clave), cada dato enlazado a su fuente; campos no extraíbles de forma fiable se declaran NO DISPONIBLES vía API read-only aditiva. Sin LLM ni resúmenes especulativos; sin segundo planificador.
- Entregable: UNA versión integrada y verificable en `feature/loom-v05`, sin merge a master. RESULT objetivo: RC_READY.

## 📊 Estado actual

- **EN EJECUCIÓN (2026-09-19):** mandato maestro v0.5 arrancado sobre `cead63c` (== origin/feature/loom-v04; master intacto). Preflight PASS: rama `feature/loom-v05` creada, worktree limpio, 3 worktrees v03/v04 verificados sin modificar. Contratos v0.5 por congelar en `specs/FEAT-LOOM-V05/`.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| `xKoRx/loom` (**VERIFIED** 2026-09-19) | `feature/loom-v05` | `cead63c` (v0.4 INTEGRITY_PASS, sin merge a master) | Mandato maestro "LOOM v0.5 — Daily Operations Center" 2026-09-19 | `specs/FEAT-LOOM-V05/` (SPEC + HUMAN-ACTIONS + SMART-COLLECTIONS-MVP) | **IN EXECUTION** |

- Política heredada: rama de integración de iteración; sin force push/reset --hard/clean destructivo; sin merge a master; APIs nuevas aditivas y read-only; dist productivo consolidada sólo en esta rama; fixtures sintéticos viven fuera del vault real (workspace `loom-v05-evidence/`).

## 🧩 Subproyectos

_No aplica — subproyecto de ejecución; no crea hijos._

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

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. %%
> - [x] Preflight + baseline: `cead63c` verificado (== origin), rama `feature/loom-v05` creada, subproyecto materializado + tarea puente en [[Loom]] #owner/agent #type/dev #area/personal ✅ 2026-09-19
> - [ ] C0 — Contratos congelados: SPEC + HUMAN-ACTIONS (clasificación aprobación/incompleto) + SMART-COLLECTIONS-MVP (documento) en `specs/FEAT-LOOM-V05/` #owner/agent #type/research #area/personal
> - [ ] H1 — Backend human-actions: proyección en internal/index (aprobaciones/incompletos deterministas) + `GET /api/v1/human-actions` + tests Go de cada caso del mandato #owner/agent #type/dev #area/personal
> - [ ] H2 — Backend resume: extracción mecánica bitácora/estado-actual + `GET /api/v1/projects/{path}/resume` + tests #owner/agent #type/dev #area/personal
> - [ ] H3 — Human Action Center UI: vista `/actions` + resumen "Necesita mi intervención" en Home + composable + tests #owner/agent #type/dev #area/personal
> - [ ] H4 — Project Command Center: ProjectView con jerarquía del mandato (próxima acción contractual vía plan de hoy; vacío explícito cuando no hay regla) + tests #owner/agent #type/dev #area/personal
> - [ ] H5 — Resume Context UI: acción contextual + panel read-only con fuente enlazada por dato + tests #owner/agent #type/dev #area/personal
> - [ ] F1 — Fixtures v0.5: puente en review SIN relación verificable, subproyecto de agente sin puente, proyectos sin bitácora/estado (estados vacíos) + lint strict #owner/agent #type/dev #area/personal
> - [ ] S1 — Storybook: componentes nuevos con stories + tests de regresión #owner/agent #type/dev #area/personal
> - [ ] E1 — Evidencia: capturas dark/light × 3 anchos, contact sheets, verify del mandato en Chromium, judge visual #owner/agent #type/dev #area/personal
> - [ ] G1 — Gates integrales + regresiones del mandato (review genérica ≠ aprobación; puente Review aparece; puente Done no; sin puente se diagnostica; datos ausentes no inventados; continuidad vacía explícita; Home sin saturación) #owner/agent #type/dev #area/personal
> - [r] Entrega al owner (RESULT RC_READY + evidencias + guías de review) #owner/agent #type/dev #area/personal

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

## 📆 Bitácora

- **2026-09-19 (BOOTSTRAP + PREFLIGHT):** Agents-OS cargado (constitución, perfil, continuidad, dominio DEFAULT — Loom es área Personal). Preflight PASS: local `feature/loom-v04 @ cead63c` == origin (SHA obligatorio del mandato), master `848fb28` intacto, worktree limpio, worktrees loom-a/loom-b verificados sin tocar. Rama `feature/loom-v05` creada desde `cead63c`; subproyecto materializado con `materialize_schema_note.py`; tarea puente registrada en [[Loom]] como `[/]`.

## 🧭 Decisiones

- **(mandato maestro, 2026-09-19):** aprobaciones humanas SÓLO desde puentes canónicas (me+supervision+review+relación verificable); casos sin relación verificable = incompletos, no aprobaciones; revisiones genéricas separadas; sin botones de aprobación; próxima acción sólo con regla contractual (plan diario) o vacío explícito; estado del padre nunca derivado de hijos; timestamps jamás presentados como avance; resume sin LLM con cada dato enlazado; API read-only aditiva; sin segundo planificador; Smart Collections sólo documento + implementación condicionada a presupuesto restante tras P0.

## Risks

- **R-1 Ambigüedad del ciclo puente:** mitigado clasificando contra la skill canónica ([[agents-os-agent-project-workflow]]) y OPERATIONAL-CONTRACT §5; tests por cada caso del mandato.
- **R-2 Home satura de nuevo:** el resumen de intervención es un bloque acotado (top-N + enlace); colas globales mantienen cap y posición subordinada.
- **R-3 Parsing bitácora frágil:** extracción mecánica documentada (bullet con fecha bajo `## 📆 Bitácora`); sin match → "no disponible", jamás inferencia.
- **R-4 Presupuesto:** P1 Smart Collections queda como documento; implementación sólo si P0 integrado, certificado y resta presupuesto.

## Blockers

- Ninguno activo.

## 🔗 Docs / Links

- [[Loom]] — proyecto padre (decisiones del owner, tarea puente).
- [[Loom — Product v0.4]] — iteración anterior (INTEGRITY_PASS; base de esta).
- [[agents-os-agent-project-workflow]] — skill canónica del ciclo puente que gobierna la clasificación de aprobaciones.
- Repo: `specs/FEAT-LOOM-V05/` (contratos de esta iteración).

## 💡 Ideas

### Backlog de ideas

- Smart Collections implementadas (arquitectura/runbooks/decisions/project knowledge) si el MVP documentado se aprueba.
- Acción "abrir bitácora en línea N" con anclas de editor si algún día hay writer.

### Motivos / principios

- Los Markdown siguen siendo la base de datos; read-only siempre; Loom nunca sustituye la decisión humana.
- Aprobación inequívoca ≠ diagnóstico: si la evidencia no alcanza, se muestra incompleto.

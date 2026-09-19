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
progress: 100
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

- **RC_READY (2026-09-19):** mandato maestro v0.5 completo y publicado en `origin/feature/loom-v05 @ 144482e` (== local; base `cead63c`; master `848fb28` intacto; sin merge; sin writer; read-only). **P0-A Human Action Center:** proyección `internal/index/humanactions.go` con la clasificación congelada (puente `#owner/me #type/supervision` en review + relación verificable → aprobación; sin relación/no resoluble/ambigua/fuera de proyecto → incompleto con razón; subproyecto de agente sin puente → diagnóstico `missing_bridge` con estados terminales excluidos; reviews genéricas fuera por construcción) + `GET /api/v1/human-actions` + vista `/actions` (tarjetas con padre/subproyecto/puente/estado/motivo/hito/enlaces, cero botones de aprobación) + resumen acotado en Home. **P0-B Project Command Center:** ProjectView con la jerarquía del mandato (estado documentado; próxima acción SÓLO contractual — compromisos de hoy del plan diario vía `committedRefsInScope` — o "No documentada" explícito; último hito por fecha máxima de bitácora; tareas humanas; entregas de agentes a review; bloqueos; tablero completo debajo). **P0-C Resume Context:** `GET /api/v1/projects/{path}/resume` (extracto verbatim de Estado actual, hito por fecha máxima, clasificación de subárbol, links; vacíos declarados `{"available":false}` con razón) + acción "Retomar" con deep-link `?resume=1`. **P1 Smart Collections:** MVP documentado (`SMART-COLLECTIONS-MVP.md`), sin implementar (por mandato, sujeto a presupuesto). **Gates @ `144482e`:** gofmt/vet · go 6/6 paquetes · race index+serve limpio · vue-tsc · vitest **367**/4 skipped (+21) · storybook build · dist reproducible byte-a-byte · smoke · e2e 10/10 · live-refresh 6/6 · G9 0×"storybook" · hex/rgba 0 fuera de tokens · secret scan limpio · fixtures lint strict **18/18** · `verify-v05.mjs` **40/40** en Chromium · judge visual **PASS dark + PASS light** (3 pasadas: 3 P1 → 1 P1 → 0; hallazgos corregidos: URL hostil envuelve en columna con `overflow-wrap` — defecto pre-existente de v0.4 —, píldoras con nombre corto, filas de tarea como grid items con `min-width:0`). Pendiente: revisión del owner (experiencia + clasificación) antes de merge a master; reviews humanas v0.1–v0.4 siguen abiertas.

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
> - [x] C0 — Contratos congelados: SPEC + HUMAN-ACTIONS + SMART-COLLECTIONS-MVP en `specs/FEAT-LOOM-V05/` #owner/agent #type/research #area/personal ✅ 2026-09-19 (`9378607`)
> - [x] H1 — Backend human-actions: proyección en internal/index + `GET /api/v1/human-actions` + tests Go de cada caso del mandato #owner/agent #type/dev #area/personal ✅ 2026-09-19 (`498619c`, race limpio)
> - [x] H2 — Backend resume: extracción mecánica bitácora/estado-actual + `GET /api/v1/projects/{path}/resume` + tests #owner/agent #type/dev #area/personal ✅ 2026-09-19 (`498619c` + `f2ac81d`: parser acepta ambos spellings canónicos de bitácora)
> - [x] H3 — Human Action Center UI: vista `/actions` + resumen "Necesita mi intervención" en Home + composable + tests #owner/agent #type/dev #area/personal ✅ 2026-09-19 (`5f20a68`)
> - [x] H4 — Project Command Center: ProjectView con jerarquía del mandato + tests #owner/agent #type/dev #area/personal ✅ 2026-09-19 (`5f20a68`)
> - [x] H5 — Resume Context UI: acción contextual + panel read-only con fuente enlazada por dato + tests #owner/agent #type/dev #area/personal ✅ 2026-09-19 (`5f20a68`)
> - [x] F1 — Fixtures v0.5: puente sin relación verificable, subproyecto sin puente, proyecto sin continuidad + lint strict 18/18 #owner/agent #type/dev #area/personal ✅ 2026-09-19
> - [x] S1 — Storybook: LoomApprovalCard/LoomIncompleteRow/ResumePanel/CommandCenter con stories; suite 367 vitest #owner/agent #type/dev #area/personal ✅ 2026-09-19
> - [x] E1 — Evidencia: 60 capturas dark/light × 3 anchos, sheets, `verify-v05.mjs` 40/40 en Chromium, judge visual 3 pasadas → PASS dark + PASS light #owner/agent #type/dev #area/personal ✅ 2026-09-19 (fixes `318d41e` + `e25b4f2`)
> - [x] G1 — Gates integrales + regresiones del mandato (go 6/6+race, vue-tsc, vitest 367, storybook, dist reproducible, smoke, e2e 10/10, live-refresh 6/6, G9, hex/rgba, secret scan, review genérica ≠ aprobación, puente Done fuera, sin puente diagnosticado, datos ausentes declarados, Home sin saturación) #owner/agent #type/dev #area/personal ✅ 2026-09-19 (todos PASS @ `144482e`)
> - [r] Entrega al owner (RESULT RC_READY + evidencias + guías de review) #owner/agent #type/dev #area/personal — publicada `origin/feature/loom-v05 @ 144482e`, a review del owner

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

- **2026-09-19 (RC_READY — entrega del mandato):** mandato maestro "Daily Operations Center" completo sobre `cead63c`, publicado en `origin/feature/loom-v05 @ 144482e` (push normal; master y reviews humanas previas intactos; sin merge; sin writer; producto 100% read-only). Backend: proyección human-actions determinista publicada con el snapshot (misma generación, incluida en la firma de invariancia), endpoints aditivos `/api/v1/human-actions` y `/api/v1/projects/{path}/resume` (dispatch por sufijo `/resume` — inequívoco porque todo DocumentID termina en `.md`), conjunto terminal de estados unificado en `index.IsTerminalStatus` (serve delega). Clasificación congelada: aprobación = puente me+supervision+review con EXACTAMENTE un subproyecto de agente hijo del padre referenciado por wikilink del texto; 0 referencias/no resoluble/ambigua/fuera de proyecto → incompleto con razón; subproyecto de agente no terminal sin NINGUNA puente que lo referencie → `missing_bridge`; reviews genéricas fuera por construcción. Frontend: `/actions` con tarjetas (padre/subproyecto/puente/estado/motivo/hito vía /resume del subproyecto/enlaces) y casos incompletos como diagnóstico; Home con bloque "Necesita mi intervención" acotado (top-3 + enlace, colas globales cap 5 intactas); ProjectView con Command Center (próxima acción SÓLO desde compromisos del plan de hoy con `committedRefsInScope` — sin inferencia de primera tarea abierta; hito por FECHA MÁXIMA independiente del orden del documento) y panel "Retomar" deep-linkable `?resume=1` con cada dato enlazado a su fuente; vacíos declarados `{"available":false}` + razón (sin sección / sección vacía / sin entradas con fecha). Hallazgos corregidos en camino: parser de bitácora con segundo spelling canónico (`**FECHA** — texto`), URL hostil que escapaba la columna de lectura (defecto PRE-EXISTENTE de v0.4, ahora `overflow-wrap: anywhere`), píldoras con nombre corto y filas de tarea como grid items con `min-width:0` (colisión `L44`, confirmada con medición de cajas). Gates completos PASS @ `144482e` (detalle en Estado actual) + `verify-v05.mjs` **40/40** + judge visual **PASS/PASS** tras 3 pasadas. RESULT: **RC_READY** — el writer (F3) y Smart Collections implementadas siguen esperando decisión del owner. Run register: `80-agents/journal/agent-runs/2026-09-19-zcode-glm-loom-v05-daily-operations.md`.

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

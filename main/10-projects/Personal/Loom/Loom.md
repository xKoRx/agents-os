---
type: project
schema_version: 1
owner: me
root: true
cssclasses:
  - wide
status: active
priority: P2
area: "[[Personal]]"
parent:
sprint:
start: 2026-08-23
due:
progress: 20
repo: xKoRx/loom
jira:
prs:
aliases:
  - Project Lens
  - Vault Viewer
  - Obsidian viewer
  - project-lens
tags:
  - kind/project
  - area/personal
created: "2026-08-23"
updated: "2026-09-13"
---

# Loom

%% Naming: Loom es el link canónico del proyecto (renombrado desde Project Lens el 2026-09-13); aliases guarda variantes humanas e históricas; tags/slugs son solo automatización. %%

> [!info]+ Loom
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P2 · **Sprint:** — · **Repo:** `xKoRx/loom` (**VERIFIED** 2026-09-13; baseline `5afd63e`)
> Viewer local read-only del vault para usar en la pega, dado que MELI vetó Obsidian y con eso perdí la visibilidad de mis proyectos durante el día. La fundación/arquitectura v0.1 quedó congelada y la ejecución vive en [[Loom — Foundation v0.1]] (subproyecto de agente).

## 🎯 Objetivo

- Recuperar en la pega la parte del flujo que cubría Obsidian: navegar, leer, buscar y relacionar los `.md` del vault (proyectos, áreas, recursos, tareas, backlinks) — con live refresh del vault sin reiniciar el proceso.
- No es un clon de Obsidian: es un viewer deliberadamente sin plugins, sin JavaScript dinámico y sin editor en v1. La edición sigue fuera del horario/herramienta vetada (VSCode + vault sincronizado).
- Los Markdown siguen siendo la base de datos; el índice es derivado, desechable y reconstruible.

## 📊 Estado actual

- **EJECUCIÓN INICIADA (2026-09-13):** repo `xKoRx/loom` VERIFICADO (workspace local, branch `master`, worktree clean, baseline `5afd63e468e7a2104a175a727a961e4f678c09ea`); B1 resuelto; contratos congelados migrados al repo (`specs/FEAT-LOOM-V01/`); implementación T01–T17 en curso bajo el límite MAX_CONCURRENT_LOOM_SUBAGENTS=1. Detalle de estado en [[Loom — Foundation v0.1]].
- **FOUNDATION FINALIZATION (2026-09-13):** decisiones owner aplicadas — proyecto renombrado **Project Lens → Loom** (canonical; aliases históricos preservados: Project Lens, Vault Viewer, Obsidian viewer, project-lens); repo `xKoRx/loom` + workspace `~/go/src/github.com/xKoRx/loom` + módulo `github.com/xKoRx/loom` + binario `loom` + branch `master` declarados; live refresh promovido a core de F1; concurrencia de subagents limitada a 1; security invariant DocumentID registrada.
- **F0 Foundation + review congelados (2026-09-13):** el plan completo (dominio con identidad path-based, matriz canonical/derived, boundaries, storage sin SQLite, decisión Graphify, API v0.1, roadmap F1–F5, tasks T01–T17, subagents y gates) vive en [[Loom — Foundation v0.1]] — esta nota queda como capa del owner: decisiones, riesgos y supervisión.
- **Pendiente del owner:** (1) validar política corporativa MELI, (2) crear el repo `xKoRx/loom` (branch `master`) y dejarlo en el workspace local — acción exacta registrada en los Blockers del subproyecto. Ningún código arranca hasta (2).

### Decisiones pendientes del owner

- ¿Qué prohíbe exactamente MELI: instalar software no aprobado en general, ejecutar extensiones/plugins, o algo más acotado? ¿Existe canal aprobado equivalente (web interna, navegador, contenedor)? Gate antes de uso diario en la máquina corporativa (no bloquea el desarrollo en máquina personal).

## 🧩 Subproyectos

- [[Loom — Foundation v0.1]] — subproyecto de agente: fundación + ejecución v0.1 (planificador único de implementación).
- [[Loom — Design System & Storybook]] — subproyecto de agente: design system compartido + integración Storybook (mandato del owner 2026-09-17; entrega a review sin reabrir v0.1).
- [[Loom — Product v0.2]] — subproyecto de agente: producto + identidad Notion-inspired con 2 subagentes (mandato del owner 2026-09-18).
- [[Loom — Product v0.3]] — subproyecto de agente: Daily Workspace + theming dark/light/System + graph local con 2 subagentes (mandato del owner 2026-09-18).

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
> `#owner/me` = tuya · `#owner/agent` = de un agente · sin owner = clasifícala. Las tareas de desarrollo delegadas viven en [[Loom — Foundation v0.1]] (WP-A…WP-F); aquí solo quedan tus decisiones y el puente de supervisión.

- [ ] Validar política corporativa MELI: qué está vetado exactamente y qué canales alternos existen #owner/me #type/research #area/personal
- [x] Crear repo GitHub `xKoRx/loom` (branch `master`) + workspace local `~/go/src/github.com/xKoRx/loom` #owner/me #type/admin #area/personal ✅ 2026-09-13
- [r] [[Loom — Foundation v0.1]] arrancar + seguimiento #owner/me #type/supervision #area/personal ✅ implementación T01–T17 completa 2026-09-13 — a Review del owner
- [r] [[Loom — Design System & Storybook]] arrancar + seguimiento #owner/me #type/supervision #area/personal ✅ fundación completa 2026-09-17 (`feature/loom-design-system` `5f7270d`+`b0e24a2`, gates G1–G10 PASS) — a Review del owner
- [ ] [[Loom — Product v0.2]] arrancar + seguimiento #owner/me #type/supervision #area/personal ✅ entregada 2026-09-18 (`feature/loom-v02` @ `0a71272`, gates PASS) — a Review del owner
- [/] [[Loom — Product v0.3]] arrancar + seguimiento #owner/me #type/supervision #area/personal — [r] RC_READY hotfix RC2 2026-09-18 (`origin/feature/loom-v03 @ 5636e4f`: FIX 1 filtros kinds + FIX 2 truncado preserva centro + FIX 3 truncado verificado en navegador 21/21; gates PASS) — a Review del owner

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

- **2026-09-18 — LOOM v0.3 HOTFIX RC2 (a Review):** mandato de Dirección Técnica ejecutado sobre la RC `3f13ea1` sin reabrir discovery ni v0.4. Dos defectos del grafo corregidos: FIX 1 filtros kinds de GraphView (los chips salían de la respuesta ya filtrada y colapsaban sobre la selección; ahora cubren el vocabulario congelado, test reproductor RED→GREEN a nivel vista) y FIX 2 truncado preserva el centro (contrato + SPEC §3: centro siempre en `nodes`, `max-1` restantes alfabéticos, `max=1` → centro exacto; regresión de masa con 150 vecinos). FIX 3: fixture sintético `fixture-truncated` (151 notas) ejercita el indicador en Chromium — `verify-truncation.mjs` 21/21 (centro, indicador, límite 100, chips tras filtrar con dos kinds, Back/Forward, refresh, dark/light). Gates completos PASS sobre `origin/feature/loom-v03 @ 5636e4f` (== local; master y v0.2 intactos). Evidencia: sheets regeneradas inspeccionables (judge PASS), capturas 44, MANIFEST RC2; sheets RC1 preservadas. Detalle en [[Loom — Product v0.3]].

- **2026-09-18 — LOOM v0.3 RC_READY (a Review):** ejecución completa del mandato "Daily Workspace, Themes, Agent Supervision & Knowledge Graph" sobre `feature/loom-v03` @ `3f13ea1` (== origin; sin merge a master). P0: Daily Workspace accionable (continuidad local + 6 colas con conteos reales de la API), presets de tasks URL-backed con D1/D1b/D2 aditivas, supervisión de proyectos. Theming dark/light/System con anti-flash, persistencia (defecto real hallado y corregido RED→GREEN), LoomThemeToggle accesible, Storybook con temas. P1: Knowledge Graph local (`/api/v1/graph` read-only con caps + GraphView radial determinista + acción desde nota). Gates integrales PASS (go 6/6 + race, vitest 269, storybook, e2e 10/10, live-refresh 6/6, G9, tokens, secret scan) + recorrido del mandato 22/22 en Chromium real (3 resoluciones, teclado, deep links, Back/Forward). Evidencia sintética: contact sheets dark/light + 36 capturas + MANIFEST (`~/go/src/github.com/xKoRx/loom-v03-evidence/`; subconjunto en `specs/FEAT-LOOM-V03/evidence/`). Tarea puente a Review. Detalle en [[Loom — Product v0.3]].

- **2026-09-18 — LOOM v0.3 EN EJECUCIÓN:** mandato del owner "Daily Workspace, Themes, Agent Supervision & Knowledge Graph" sobre el baseline certificado `feature/loom-v02 @ 0cba972`. Rama de integración `feature/loom-v03` (sin merge a master); contratos congelados `specs/FEAT-LOOM-V03/` @ `f58c3ac`; D1–D5 autorizadas por el mandato; 2 subagentes (A=UI theming, B=Product P0 + graph P1) con manager integrador único. Detalle en [[Loom — Product v0.3]].

- **2026-09-18 — LOOM v0.2.1 TÉCNICAMENTE CERTIFICADA (a decisión de dirección técnica):** estabilización sobre la RC `0a71272` → `origin/feature/loom-v02` @ `ff53337` (sin merge a master). Corregidos: breadcrumbs con directorio padre real (bug de auditoría externa), frontmatter etiquetado como reconstrucción, encoding de rutas en sidebar, filtros de texto dark. Auditoría integral en navegador real (7 rutas + estados + hostiles inertes + live refresh), accesibilidad con sub-gates NO VERIFICADO documentados, gates integrales PASS sobre el SHA final (race determinista vía snapshot congelado — el vault real recibe escrituras concurrentes de otras sesiones), secret scan limpio, 10 capturas sanitizadas. Detalle en [[Loom — Product v0.2]] § Bitácora.

- **2026-09-18 — LOOM v0.2 ENTREGADA (a Review):** iteración completa en `origin/feature/loom-v02` @ `0a71272` (sin merge a master). 2 subagentes en paralelo (A=UI: 9 componentes Loom con stories/tests; B=Producto: fix búsqueda, `/api/v1/tree`+`/vault`, Note Viewer content-first con inspector, `/tasks`, cockpit) + manager integrador (shell Notion-inspired con tree en sidebar, shortcut `/`, skip-link, edad del índice). Gates integrales PASS (go 6/6+race, vitest 203, storybook, smoke, e2e 10/10, live-refresh 6/6, G9) + visual en navegador real 1440/1920 con evidencia. Durante la integración se detectó y preservó trabajo concurrente de la sesión de auditoría externa (fix closed-world de carpetas vacías). Detalle en [[Loom — Product v0.2]] § Bitácora.

- **2026-09-18 — LOOM v0.2 EN EJECUCIÓN:** mandato del owner "Product Experience, Notion-Inspired Design System & Autonomous Delivery". Preflight PASS (master `848fb28` == origin, design system `b0e24a2` verificado con gates, auditoría UX `UX-IA-REVIEW-V0.1.md` preservada untracked). Decisión registrada: **MAX_CONCURRENT_LOOM_SUBAGENTS = 2** para v0.2 (A=UI, B=Product, worktrees independientes, manager integrador único). Contratos congelados en repo `specs/FEAT-LOOM-V02/` @ `738de70` (rama `feature/loom-v02`, sin merge a master). Detalle en [[Loom — Product v0.2]].

- **2026-09-17 — DESIGN SYSTEM & STORYBOOK FOUNDATION ENTREGADA (a Review):** ejecutada por el agente bajo mandato del owner del mismo día, sin reabrir v0.1. Rama `feature/loom-design-system` (sin push/merge) con tokens compartidos app↔Storybook, 9 componentes compartidos con consumidor real (`internal/web/src/ui/`), 43 stories + autodocs (Storybook 10.6 + addon-docs dentro de `internal/web/`), migración incremental de las 5 vistas y aislamiento total del binario (G9: cero Storybook en dist). Gates G1–G10 PASS (vitest 126/126, e2e 6/6, visual en navegador real). Incluye fix pre-existente del smoke del Makefile. Durante la ejecución apareció en el repo el review UX/IA (`specs/FEAT-LOOM-V01/UX-IA-REVIEW-V0.1.md`, untracked) — preservado; sus pendientes (R1–R4, bug P1 de búsqueda) quedan para la próxima iteración con el owner. Detalle en [[Loom — Design System & Storybook]] § Bitácora.

- **2026-09-13** — **LOOM v0.1 COMPLETA (T01–T17, 100%):** backend (scan/watcher/proyecciones/links/API segura) + frontend (shell dark, viewer, cockpit, board 5 estados, search, diagnostics) + gates (e2e 10/10, live-refresh 6/6 sin reinicio, coverage vault 100%/index 95.7%, race limpio, binario único 12.6MB offline) + validación visual real en browser (3 defectos encontrados y corregidos). Final `xKoRx/loom` master @ `848fb28` == origin/master. Tarea puente a Review. Detalle completo en [[Loom — Foundation v0.1]] § Bitácora.

- **2026-09-13** — SESIÓN DE IMPLEMENTACIÓN PAUSADA POR OWNER (10/17 tasks = 59%): T01–T10 DONE y aceptados en `xKoRx/loom` master @ `4a9d0a4` (== origin/master, push externo confirmado) — backend completo (scaffold, fixtures, parser frontmatter/body, scanner+snapshot+watcher+generation con invariancia de rebuild probada, proyecciones Agents-OS, resolución de links/backlinks, API meta/projects/areas con security boundary DocumentID). T11 (notes/render/search) interrumpido por quota del surface a mitad de dispatch; parcial preservado como referencia (`render.go.partial-t11`, sin compilar). Cobertura acumulada: vault 100%, parse 95.3%, index 95.7%, serve 98.7%. v0.1 NO está completo: restan T11–T17 (API notes/render/search/tasks/diagnostics + frontend completo + e2e/hardening). Detalle de retomada en [[Loom — Foundation v0.1]] § Bitácora (SESSION CLOSE).
- **2026-09-13** — EXECUTION START: repo `xKoRx/loom` verificado (owner lo creó físicamente: workspace + GitHub, branch `master`, worktree clean, baseline `5afd63e468e7a2104a175a727a961e4f678c09ea`); B1 cerrado; tarea de creación de repo marcada Done. Contratos congelados migrados del planner al repo `specs/FEAT-LOOM-V01/` (SPEC/TASKS/PLAN @ `b031006`) según patrón Echo E-01 — el repo es autoridad del contrato, el subproyecto conserva estado/routing. Sesión de implementación iniciada (T01–T17, 1 subagente a la vez).
- **2026-09-13** — FOUNDATION FINALIZATION: proyecto renombrado **Loom** (git mv con historial; alias Project Lens preservado); decisiones de repo/workspace/módulo/binario/branch registradas (repo aún sin crear — verificado con gh/ls-remote/local, sin SHA inventado); live refresh promovido a core de F1 (backend dueño exclusivo del fs, generation en `/meta`, polling en la SPA, F5 queda como hardening); límite duro `MAX_CONCURRENT_LOOM_SUBAGENTS = 1` (secuencia estricta, sin delegación recursiva); security invariant DocumentID registrada con tests en T10/T11. ADRs L11–L13 añadidos en el subproyecto. Tareas actualizadas: decisión de nombre cerrada, queda la acción física del repo.
- **2026-09-13** — Rebase del proyecto sobre el Agents-OS vigente (sesión de fundación): creado subproyecto de agente (entonces llamado Project Lens — Foundation v0.1, hoy [[Loom — Foundation v0.1]]) con la arquitectura congelada (ADRs L1–L10), dominio con identidad path-based, matriz canonical/derived, boundaries, API v0.1, roadmap vertical F1–F5 y tasks atómicas T01–T17. Las tareas de desarrollo de esta nota (diseño v0, MVP v0.1, dashboard, search) migraron a los WP del subproyecto — una fuente por hecho. Idea de agosto ([[2026-08-25-project-lens-knowledge-runtime]]) promovida: su SQLite-day-1 y MCP quedan como future drivers F7/F8, no como v0.1. Bloqueos owner registrados: política MELI + nombre/repo/workspace.
- **2026-08-23** — Creación del proyecto. Evaluada propuesta inicial de arquitectura (IA externa): Go + HTTP localhost + SPA embebida, sin plugins/editor en v1, markdown como base de datos. Aporte propio principal: el valor real está en replicar server-side el subset de Dataview/Bases que ya uso (tableros, rollups, backlinks), no en el render de markdown. Gate previo a desarrollar en serio: validar qué prohíbe la política de MELI.

## 🧭 Decisiones

- **2026-09-13 (finalización)** — Nombre canónico del producto y proyecto: **Loom** (antes Project Lens; alias histórico preservado). Repo canónico `xKoRx/loom`, workspace local `~/go/src/github.com/xKoRx/loom`, módulo Go `github.com/xKoRx/loom`, binario `loom`, branch `master`. Live refresh sin reinicio de proceso = comportamiento core de v0.1 (backend dueño exclusivo del filesystem; frontend sólo observa generation vía HTTP). Límite duro de ejecución: máximo 1 subagente Loom concurrente, sin delegación recursiva. Security invariant: los DocumentIDs HTTP se resuelven sólo contra el snapshot publicado, nunca como paths de filesystem. Detalle y rationale en [[Loom — Foundation v0.1]] § Decisiones (ADRs L11–L13).
- **2026-09-13** — Congeladas las decisiones de fundación (ADRs L1–L10) en [[Loom — Foundation v0.1]] § Decisiones: autoridad Markdown, identidad path-based, Go+Vue 3 embed, índice in-memory sin SQLite, Project/Area como proyecciones tipadas de Note, render server-side, sin dependencia de Graphify, bloques dinámicos raw, ciclo de task 5 estados, seguridad local loopback read-only.
- **2026-08-23** — Alcance v1 read-only: navegar/leer/buscar/relacionar. Sin plugin system, sin `eval()`, sin módulos remotos, sin URLs externas por defecto; superficie de privilegios mínima a propósito (es la razón por la que vetaron Obsidian).
- **2026-08-23** — Arquitectura: binario Go escuchando en `127.0.0.1` + SPA embebida con `go:embed`; sin Electron ni instaladores. Wails v3 queda como envoltorio opcional posterior.

## 🔗 Docs / Links

- [[Loom — Foundation v0.1]] — planner ejecutable y ADRs congelados.
- [[2026-08-25-project-lens-knowledge-runtime]] — idea de origen (promovida; nombre histórico: Project Lens).
- Propuesta original evaluada (ChatGPT, 2026-08-23): resumen destilado en Estado actual y Decisiones; texto completo quedó en la conversación.

## 💡 Ideas

### Backlog de ideas

- Exponer el Core Vault como servidor MCP: agentes consultando proyectos, tareas y backlinks del vault directamente (deferred F8 en el subproyecto; reopen trigger: necesidad demostrada de query/retrieval programático sobre Loom — Graphify es un índice derivado independiente, no sustituto de esa API).
- Graph view ligero (solo entidades proyecto/app/área) más adelante (F6).
- Snapshot HTML estático exportable como plan B si la política corporativa no permite binarios propios (F9).

### Motivos / principios

- Los Markdown son la base de datos; el índice es desechable y reconstruible.
- Read-only primero; Loom nunca compite con el editor.
- Sin plugins: eliminar la superficie exacta que motivó el veto.

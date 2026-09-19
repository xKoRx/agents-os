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
start: 2026-09-18
due:
progress: 100
repo: xKoRx/loom
jira:
prs:
aliases:
  - Loom v0.4
  - FEAT-LOOM-V04
  - Workspace Model & UX Refinement
tags:
  - kind/project
  - area/personal
  - agent/owner
created: "2026-09-18"
updated: "2026-09-19"
cssclasses:
  - wide
---

# Loom — Product v0.4

%% Naming: Loom — Product v0.4 es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Loom — Product v0.4
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Loom]] · **Repo:** `xKoRx/loom` (**VERIFIED** 2026-09-18; base `feature/loom-v03 @ 5636e4f` RC2 certificada; master `848fb28` intacto)
> Subproyecto de agente: **Workspace Model & UX Refinement** — mandato de Dirección Técnica 2026-09-18. Convierte la experiencia saturada por el volumen global del vault en un workspace personal de foco: hotfix visual P0 (ancho de lectura Comfortable/Wide, scrollbars, overflow), contrato operativo Agents-OS documentado (sin editar el schema canónico), fixtures realistas materializados con el materializador canónico, Home orientada a foco, vista Today read-only sobre fixtures y contrato de writer como entrega separada. Sin migración del vault, sin escritura, sin merge a master.

## 🎯 Objetivo

- Partir de la RC2 v0.3 certificada (`5636e4f`) y transformar la experiencia en un workspace personal: foco, planificación diaria y separación explícita del trabajo humano y delegado.
- P0 visual: auditar en navegador real y corregir ancho excesivamente limitado del Markdown, espacio desperdiciado a la derecha, layout responsive, scroll horizontal global, scrollbar blanca de la sidebar en dark y scrollbars de paneles; ancho de lectura Comfortable/Wide por tokens. Sin modificar documentos.
- Contrato operativo Agents-OS documentado por separado (lifecycle de proyecto/tarea, responsabilidad, review humana, foco personal, plan diario, evidencia de ejecución de agente) reutilizando campos y estados existentes; sin nuevos estados de Project para favoritos/foco; modificaciones sólo como propuesta de contrato.
- Fixtures realistas sintéticos y privados (7 proyectos, subproyectos de agente, tareas del owner, delegadas, reviews, blocked/waiting, backlog amplio, pausados/completados, dos planes diarios consecutivos, notas y relaciones) materializados con el materializador canónico y lint cuando corresponda; sin copiar notas privadas del owner.
- Home orientada a foco (plan de hoy, proyectos seleccionados explícitamente, reviews y bloqueos relevantes, delegado resumido, continuar trabajando); catálogo completo en Projects/Tasks; la selección de foco no modifica `status`; localStorage etiquetado como no sincronizado.
- Vista Today read-only funcional sobre fixtures + contrato del writer como entrega separada (sin botones que aparenten persistir cambios).
- Entregable: UNA versión integrada y verificable en `feature/loom-v04`, sin merge a master. RESULT objetivo: READY_FOR_OWNER_UX_REVIEW.

## 📊 Estado actual

- **INTEGRITY_PASS (2026-09-19):** los 5 defectos de integridad del plan diario detectados por Dirección Técnica quedan resueltos y publicados en `origin/feature/loom-v04 @ cead63c` (== local; base `57aeb13`; master `848fb28` intacto; sin merge; sin writer). **A** resolución exacta de block IDs (`^task-a` ya no matchea `^task-ab`; duplicados → `ambigua`/sin resolver, jamás la primera). **B** cargas de orígenes deduplicadas por DocumentID en `usePlan` (una ref repetida o un fallo ya no pisan una nota bien cargada) + guard de generación igual al de useTasks. **C** `canceled` nunca más bajo "completadas": done/canceled/open/unresolved separados, porcentaje = done/total documentado, badges de canceladas en Home/Today. **D** `useToday()` reactivo (timeout al próximo midnight, cleanup por scope): una instancia abierta >24h recarga su plan; Today sigue a hoy sólo si el usuario estaba en hoy. **E** contrato `#plan/ref`/`#plan/moved` = compromisos, no tareas ejecutables: fuera de las colas de /tasks (My Tasks, Unassigned) con toggle explícito `?plan=1` y conteo visible; `#plan/own` sigue ejecutable; `/api/v1/tasks` intacta; cero migración. Gates: go 6/6+race, vue-tsc, vitest **346** (+23), storybook, dist reproducible, smoke, e2e 10/10, live-refresh 6/6, G9, secret scan · verify **32/32** en Chromium (fixtures con 2 regresiones en vivo nuevas: `api-v2` antes que `api` y tarea cancelada comprometida hoy) · judge visual PASS (15 capturas cambiadas). Contrato actualizado: `DAILY-PLAN-FORMAT.md` (§Identidad exacta, §Presencia en el índice global, §Progreso) + `OPERATIONAL-CONTRACT.md` §7. Pendiente: re-review de Dirección Técnica antes de autorizar el writer (F3).

- **READY_FOR_OWNER_UX_REVIEW (2026-09-19):** mandato "Workspace Model & UX Refinement" completo y publicado en `origin/feature/loom-v04 @ 3b69eed` (== local; base RC2 v0.3 `5636e4f`; master `848fb28` intacto; sin merge). **S1 hotfix visual P0:** auditoría Chromium → causa real del scroll horizontal global era la nav del topbar (<1080px, ~450px naturales desbordando TODAS las rutas); corregido con wrap + ancho de lectura Comfortable/Wide por tokens (`--measure-*`, `html[data-measure]`, toggle accesible etiquetado "this browser") + scrollbars token-driven dark/light; comfortable queda bit-a-bit igual al estado anterior. **S2 contrato operativo:** `specs/FEAT-LOOM-V04/{OPERATIONAL-CONTRACT,DAILY-PLAN-FORMAT,CONTRACT-PROPOSALS,SPEC}.md` — lifecycles, responsabilidad, review humana (review ≠ aprobación; la puente es el único punto de aceptación), foco personal no-estado, plan diario referencial, evidencia documental; propuestas F1–F4 SIN editar el schema canónico. **S3 fixtures:** `fixture-workspace/` 16 notas/10 proyectos/48 tareas con 2 planes diarios, materializado vía `materialize_schema_note.py` y lint strict 16/16 ERROR=0; identidad por block ID único + (path,line). **S4 Home de foco:** Plan de hoy + Proyectos en foco (localStorage etiquetado, nunca toca `status`) + Reviews/Bloqueos relevantes foco-primero con owner visible + Delegado resumido + Continue working; catálogo completo en `/projects` con estrella. **S5 Today read-only:** `/today?date=` con progreso computado (live del origen), arrastre del día anterior, reprogramadas, historial, deep-link; sin controles de escritura; writer = propuesta F3 separada. **Gates @ `1c8c508` (producto) / `3b69eed` (rama):** gofmt/vet · go test 6/6 · race limpio · vue-tsc · vitest 323 (32 archivos; +32 nuevos) · storybook · dist reproducible byte-a-byte · smoke · e2e 10/10 · live-refresh 6/6 · G9 · hex/rgba 0 · secret scan limpio · overflow 0 en 6 rutas × 3 anchos · `verify-v04.mjs` 22/22 en Chromium real · judge visual PASS (38 capturas, sheets dark/light). Pendiente: revisión de experiencia y contrato por Dirección Técnica antes de autorizar el writer (F3).

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| `xKoRx/loom` (**VERIFIED** 2026-09-18) | `feature/loom-v04` | `5636e4f` (RC2 v0.3 certificada, sin merge a master) | Mandato de Dirección Técnica "LOOM — Workspace Model & UX Refinement" 2026-09-18 | `specs/FEAT-LOOM-V04/` (OPERATIONAL-CONTRACT + CONTRACT-PROPOSALS + SPEC) | **IN EXECUTION** |

- Política heredada: rama de integración de iteración; sin force push/reset --hard/clean destructivo; sin merge a master; APIs nuevas aditivas y read-only; dist productivo consolidada sólo en esta rama; fixtures sintéticos viven fuera del vault real (workspace `loom-v04-evidence/`).

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
> - [x] Preflight + baseline: `5636e4f` verificado, rama `feature/loom-v04` creada, subproyecto materializado + tarea puente en [[Loom]] #owner/agent #type/dev #area/personal ✅ 2026-09-18
> - [x] S1 — Hotfix visual P0: auditoría Chromium (causa real: nav topbar <1080px) + Comfortable/Wide por tokens + scrollbars themed + wrap; verificado con notas reales y nota stress de fixtures #owner/agent #type/dev #area/personal ✅ 2026-09-18 (`95ad680`)
> - [x] S2 — Contrato operativo Agents-OS: OPERATIONAL-CONTRACT + DAILY-PLAN-FORMAT + CONTRACT-PROPOSALS (F1–F4, sin editar schema canónico) + SPEC #owner/agent #type/research #area/personal ✅ 2026-09-18 (`6315e3c`)
> - [x] S3 — Fixtures realistas: fixture-workspace 16 notas/10 proyectos/48 tareas, materializador canónico + lint strict 0, block IDs únicos, 2 planes diarios, nota stress visual #owner/agent #type/dev #area/personal ✅ 2026-09-18 (`6315e3c`)
> - [x] S4 — Home orientada a foco + catálogo en /projects (estrella de foco, `loom.focus` etiquetado, nunca toca status) #owner/agent #type/dev #area/personal ✅ 2026-09-19 (`55c3009`)
> - [x] S5 — Vista Today read-only sobre fixtures (progreso/arrastre/reprogramadas/historial + deep-link) + writer como propuesta F3 separada #owner/agent #type/dev #area/personal ✅ 2026-09-19 (`55c3009`)
> - [x] S6 — Evidencia visual: 38 capturas dark/light × 3 ventanas, contact sheets, judge visual PASS, subconjunto en repo #owner/agent #type/dev #area/personal ✅ 2026-09-19 (`3b69eed`)
> - [x] Gates integrales + recorrido del mandato `verify-v04.mjs` 22/22 en Chromium real #owner/agent #type/dev #area/personal ✅ 2026-09-19 (todos PASS @ `1c8c508`)
> - [x] Integrity Gate: A block IDs exactos + ambigüedad · B dedup de cargas por DocumentID · C canceled fuera de completadas + denominador documentado · D rollover de día (useToday) · E compromisos fuera de las colas de /tasks con toggle `?plan=1`; contrato + fixtures + verify 32/32 + judge #owner/agent #type/dev #area/personal ✅ 2026-09-19 (todos PASS @ `cead63c`)
> - [r] Entrega al owner (RESULT READY_FOR_OWNER_UX_REVIEW + integridad resuelta INTEGRITY_PASS + evidencias + guías de review) #owner/agent #type/dev #area/personal — publicada `origin/feature/loom-v04 @ cead63c`, a re-Review de Dirección Técnica antes de autorizar el writer

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

- **2026-09-19 (INTEGRITY_PASS — corrección del gate de integridad):** mandato de Dirección Técnica "resuelve los defectos de integridad antes de autorizar el writer" ejecutado sobre `57aeb13`, publicado en `origin/feature/loom-v04 @ cead63c` (push normal; master/v0.2/v0.3/vault real intactos; sin nuevas funcionalidades, sin writer). **A** `findOriginTask` ahora exige el identificador completo como token — la reproducción `^task-a`/`^task-ab` del informe quedó como test RED→GREEN y como regresión EN VIVO en los fixtures (Altair define `api-v2` antes que `api`; el check "estados vivos done" del verify falla con el matching viejo); definiciones duplicadas marcan la referencia `ambigua` (badge "bloque duplicado"), nunca primera arbitraria. **B** la deduplicación por referencia envenenaba el Map de `usePlan` con `[noteName, null]` (ref repetida o fallo posterior pisaban una nota bien cargada): ahora las cargas se deduplican por DocumentID de origen — una petición por documento, verificada en vivo (6 reqs = 1 plan + 5 orígenes) — y `usePlan` adopta el guard de generación de `useTasks` (colapsa la publicación 0→N del shell). **C** `planProgress` contaba `canceled` como completado y las vistas mostraban "X/Y completadas" con cancelaciones dentro: ahora done/canceled/open/unresolved van separados, el badge "N cancelada(s)" es visible en Home y Today, el porcentaje es `done/total` con el denominador documentado en el contrato (todo compromiso permanece en él — lo cancelado arrastra la barra, no la infla) y `planOpen` de Home excluye own canceladas; regresión en vivo: rotación de Vega cancelada comprometida hoy → "1 cancelada · 0/5". **D** Home congelaba la fecha en setup: `useToday()` con timeout al próximo midnight local (re-armado, cleanup por scope, probado con reloj controlado) recarga el plan de una instancia abierta >24h; Today hace reactivos `isToday`/`goTo`/historial y sólo sigue a hoy si el usuario estaba en hoy (deep-links intactos). **E** las líneas `#plan/ref`/`#plan/moved` entraban a las colas de /tasks como `unassigned` (y la misma tarea en 2 planes consecutivos aparecía N veces): contrato nuevo en DAILY-PLAN-FORMAT § "Presencia en el índice global" — son compromisos, no tareas ejecutables; /tasks las muestra aparte tras toggle URL-backed `?plan=1` con conteo visible (+8 líneas…), `#plan/own` sigue ejecutable, la API intacta y cero migración; regresión con los 2 planes consecutivos (Helios PR en ambos días = 2 filas sólo dentro del toggle). **Hallazgos intermedios corregidos:** guard de generación faltante en usePlan, own cancelada listada en planOpen, `page.clock.setFixedTime` en arnés de capturas/verify para que la evidencia no envejezca al cambiar el día real, y el judge visual detectó que MI brief exigía un badge condicional que correctamente no se renderiza (re-disparo con spec corregida → PASS). **Gates @ `cead63c`:** gofmt/vet · go 6/6 · race · vue-tsc · vitest 346/4 skipped (+23) · storybook · dist reproducible · smoke · e2e 10/10 · live-refresh 6/6 · G9 · hex/rgba 0 · secret scan limpio · `verify-v04.mjs` **32/32** · judge visual PASS (15 capturas). RESULT: **INTEGRITY_PASS** — Today confiable para evaluar UX; writer (F3) sigue esperando autorización. Run register: `80-agents/journal/agent-runs/2026-09-19-zcode-glm-loom-v04-integrity-gate.md`.

- **2026-09-19 (READY_FOR_OWNER_UX_REVIEW — entrega del mandato):** verificado el estado real primero (worktree `feature/loom-v03` limpio @ `5636e4f` == origin; master `848fb28` intacto). **S1:** auditoría Chromium real — el scroll horizontal global reportado NO era del Markdown (pre/tablas ya contenían su scroll) sino de la nav del topbar <1080px desbordando `documentElement` en todas las rutas (sw 948 vs cw 885 a 900px); fixes: `.sidebar-top`/`.nav` wrap, tokens `--measure-comfortable/--measure-wide` con `html[data-measure]` + composable `readingWidth` (localStorage `loom.readingWidth`, etiquetado "this browser"), `LoomMeasureToggle` radiogroup accesible con story/tests, scrollbars token-driven dark/light (`--scrollbar-thumb/-hover`); comfortable queda bit-a-bit igual. **S2:** contratos en repo — OPERATIONAL-CONTRACT (§1–§9: lifecycles, responsabilidad, review owner-neutral con la puente como único punto de aprobación humana, foco no-estado, plan referencial, evidencia documental, identidad block ID + (path,line)), DAILY-PLAN-FORMAT (clases #plan/ref|own|moved — moved como TASK porque la API no sirve bullets —, referencias por block ID con resolución por anchor del índice, fallback documentado, read-only), CONTRACT-PROPOSALS F1–F4 (foco sincronizable diferido, tipo daily_plan, writer del plan restringido + requisitos FUTURE-WRITING heredados, vocabulario #type), SPEC. **S3:** `fixture-workspace/` con generador idempotente `generate_fixture_workspace.py` que materializa cada nota vía `materialize_schema_note.py --stdout` (proyectos 7 raíz + 3 subproyectos de agente con pausado/completados, área, hub con relations, nota stress, 2 planes diarios, inbox) — lint strict 16/16 ERROR=0; identidad de tareas documentada en FIXTURES.md; sin contenido real del owner. **S4/S5:** `focus.ts` (cap 12, presentation-only) + `plan.ts` + HomeView (Plan de hoy con estados vivos, foco cards, Reviews/Bloqueos foco-primero owner-visible, Delegado por proyecto, Continue working intacto) + ProjectsView (catálogo íntegro reubicado + estrella aria-pressed) + TodayView (deep-link `?date=`, progreso con unresolved visible, arrastre computado vs día previo, reprogramadas, historial por PLAN_DIR, microcopy read-only, sin controles) + router/nav (Today, Projects, ícono calendar). **Gates @ `1c8c508`:** gofmt/vet limpios · go test 6/6 · race serve+index limpio · vue-tsc limpio · vitest 323 passed/4 skipped (32 archivos; +32 tests nuevos) · storybook build OK · dist reproducible byte-a-byte (commiteada `1c8c508`) · smoke PASS · e2e 10/10 · live-refresh 6/6 · G9 0×"storybook" · hex/rgba 0 fuera de tokens.css · secret scan limpio · lint fixtures 16/16. **Evidencia:** 38 capturas (11 vistas × dark/light 1440 + core × 1280/900 angosta), contact sheets 2×N 2048px con judge visual independiente PASS (sin P0; solape estrella/"1 sub" corregido y recapturado), `verify-v04.mjs` **22/22 PASS** en Chromium real (incluye foco end-to-end, arrastre 2026-09-17, Comfortable→Wide medido, overflow 0 en 6 rutas × 3 anchos); subconjunto en `specs/FEAT-LOOM-V04/evidence/` + MANIFEST. **Hallazgos de integración corregidos:** App.vue no llamaba `initFocus()` (foco persistido no se restauraba al recargar — hallado en verificación end-to-end) y el progreso con unresolved excluía del denominador (mostraba "1/2 · 100%" contradictorio). **Publicación:** push normal `5636e4f..3b69eed` → `origin/feature/loom-v04` (== local); master y reviews humanas previas intactos; sin implementación de escritura; servers de auditoría detenidos. Run register: `80-agents/journal/agent-runs/2026-09-18-zcode-glm-loom-v04-workspace-ux.md`. RESULT: **READY_FOR_OWNER_UX_REVIEW**.

- **2026-09-18 (BOOTSTRAP + PREFLIGHT):** Agents-OS cargado (constitución, perfil, continuidad, dominio DEFAULT — Loom es área Personal). Preflight PASS: `feature/loom-v03 @ 5636e4f` == origin (RC2 certificada), master `848fb28` intacto, worktree limpio. Rama `feature/loom-v04` creada desde `5636e4f`; subproyecto materializado con `materialize_schema_note.py`; tarea puente registrada en [[Loom]].

## 🧭 Decisiones

- **(mandato Dirección Técnica, 2026-09-18):** partir desde la RC2 v0.3 certificada; sin migración masiva del vault; sin implementar escritura; sin merge a master; el foco de proyectos NO modifica `status`; sin nuevos estados de Project para favoritos/foco; sin inferir actividad runtime desde status documental; sin asumir que toda tarea Review requiere aprobación humana; propuestas de contrato sin editar el schema canónico público; writer como entrega separada; sin grafo global.

## Risks

- **R-1 Home pierde el catálogo:** mitigado moviendo el cockpit completo a `/projects` (nav nueva) — nada se elimina, se reubica.
- **R-2 fixtures vs schema real:** materialización vía `materialize_schema_note.py --stdout` + lint contractual; identidad de tareas por `note_path + line` documentada.
- **R-3 ancho Wide rompe vistas existentes:** tokens nuevos aditivos (`--measure-*`), default Comfortable bit-a-bit igual al estado actual; gates visuales antes de integrar.
- **R-4 Today aparenta escritura:** vista 100% read-only; contrato del writer en doc separado; microcopy explícita.

## Blockers

- Ninguno activo.

## 🔗 Docs / Links

- [[Loom]] — proyecto padre (decisiones del owner, tarea puente).
- [[Loom — Foundation v0.1]] · [[Loom — Design System & Storybook]] · [[Loom — Product v0.2]] · [[Loom — Product v0.3]] — iteraciones anteriores (en Review; NO reabiertas).
- Repo: `specs/FEAT-LOOM-V04/` (contratos de esta iteración).

## 💡 Ideas

### Backlog de ideas

- Sincronización futura del foco y del plan diario si algún día hay backend multi-dispositivo (fuera de v0.4 por diseño; hoy son browser-local etiquetado).

### Motivos / principios

- Los Markdown siguen siendo la base de datos; el índice es derivado y reconstruible; read-only siempre.
- El foco es presentación personal, nunca estado documental.
- Estado documentado ≠ actividad en runtime.

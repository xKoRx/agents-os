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
start: 2026-09-13
due:
progress: 0
repo: xKoRx/loom
jira:
prs:
aliases:
  - Loom v0.1
  - Loom Foundation
  - Project Lens — Foundation v0.1
  - Project Lens v0.1
  - Lens Foundation
  - PL-F01
tags:
  - kind/project
  - area/personal
  - agent/owner
created: "2026-09-13"
updated: "2026-09-13"
cssclasses:
  - wide
---

# Loom — Foundation v0.1

%% Naming: Loom — Foundation v0.1 es el link canónico del proyecto; aliases guarda variantes humanas e históricas (Project Lens); tags/slugs son solo automatización. %%

> [!info]+ Loom — Foundation v0.1
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Loom]] · **Repo:** `xKoRx/loom` (**VERIFIED** 2026-09-13; baseline `5afd63e468e7a2104a175a727a961e4f678c09ea`, branch `master`, worktree clean, HEAD == origin/master)
> Subproyecto de **fundación y ejecución v0.1** de Loom. Esta nota es el planificador único de ESTADO de la implementación (order/state/evidence/bitácora); los **contratos congelados viven en el repo** (`specs/FEAT-LOOM-V01/SPEC.md`, `TASKS.md`, `PLAN.md` — migrados 2026-09-13 cuando B1 se resolvió; una fuente por hecho). El padre [[Loom]] conserva las decisiones del owner y la tarea puente.

## 🎯 Objetivo

- Entregar **Loom v0.1**: viewer local read-only del vault real — binario Go único (127.0.0.1) con SPA Vue 3 embebida que recupera el valor diario perdido con el veto de Obsidian: leer notas con links resueltos, cockpit de proyectos con rollup, tableros de tareas con ciclo de 5 estados, backlinks y búsqueda — **reflejando cambios del vault sin reiniciar el proceso**.
- Todo el estado derivado (índice, proyecciones, HTML renderizado) es reconstruible desde el vault: delete-all-derived → rescan → producto idéntico. Markdown es la única autoridad.
- v0.1 es un **walking skeleton productivo**: cada slice recorre el sistema real end-to-end (vault real → scan/parse/index → API → UI) y todo el código está destinado a sobrevivir. No hay prototype/, temp/ ni throwaway/.

## 📊 Estado actual

- **EJECUCIÓN DESBLOQUEADA (2026-09-13):** repo `xKoRx/loom` VERIFICADO (workspace `~/go/src/github.com/xKoRx/loom`, branch `master`, worktree clean, HEAD == origin/master); baseline real `5afd63e468e7a2104a175a727a961e4f678c09ea` registrado; **B1 RESUELTO**; contratos congelados migrados al repo (`specs/FEAT-LOOM-V01/` @ `b031006b400e37a3a4647abc6049161bd2c2a7d6`); WP-A ejecutable; T01 = siguiente task READY. Sesión de implementación iniciada.
- **FOUNDATION FINALIZATION (2026-09-13):** decisiones owner aplicadas — rename canónico **Project Lens → Loom** (aliases históricos preservados), repo `xKoRx/loom` + workspace `~/go/src/github.com/xKoRx/loom` + módulo `github.com/xKoRx/loom` + binario `loom` + branch `master` declarados; live refresh promovido a comportamiento CORE de F1 (backend dueño exclusivo del fs: watch fsnotify → debounce → rebuild → snapshot inmutable → swap atómico → generation++; Vue observa generation por polling y refetch); **MAX_CONCURRENT_LOOM_SUBAGENTS = 1** (secuencia estricta, sin R2∥R3, sin delegación recursiva); invariante de seguridad HTTP DocumentID registrada.
- **F0 FOUNDATION COMPLETA (2026-09-13):** sesión de rebase/arquitectura produjo el planner original — dominio, identidad, matriz canonical/derived, boundaries, storage (sin SQLite), decisión Graphify (sin dependencia), API v0.1, roadmap vertical F1–F5, work packages atómicos T01–T17, modelo de subagents y gates. Cero product code en fundación.
- **FOUNDATION REVIEW (2026-09-13):** arquitectura y roadmap **ACCEPTED** por el owner con 4 correcciones load-bearing aplicadas: (1) identity/API por path, (2) separación conceptual genérico↔Agents-OS dentro de `internal/index`, (3) scan best-effort + snapshot inmutable + swap atómico, (4) rationale MCP corregido.
- **Muestreo del vault real (2026-09-13, evidencia del diseño):** 2741 notas .md; 80-agents 2234 (mayoritariamente journal); 349 tasks con `#owner/*` en 10-projects; sin sistema de `id:`/`uid:` global → identidad path-based; frontmatter con valores legacy/malformados → tolerancia obligatoria; bloques dinámicos: 36 dataviewjs, 32 base, 39 tasks plugin.
- **Graphify (2026-09-13):** binario `graphify-obsidian` NO instalado en esta máquina. Contrato inspeccionado ([[graphify-contract]]). Refuerza la decisión de NO depender de Graphify (SPEC § Graphify).

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| `xKoRx/loom` (**VERIFIED** 2026-09-13) | `master` (fase v0.1) | `5afd63e468e7a2104a175a727a961e4f678c09ea` (Initial commit) | repo `specs/FEAT-LOOM-V01/SPEC.md` @ `b031006b400e37a3a4647abc6049161bd2c2a7d6` (§ Product definition + § API contract) | repo `specs/FEAT-LOOM-V01/SPEC.md` @ `b031006b400e37a3a4647abc6049161bd2c2a7d6` (§ Domain model + § Architecture + § Test strategy) | **EXECUTION READY — T01 READY** |

- Política: la ejecución corre con repo + branch/base registrados en esta tabla (regla dura de `agents-os-entity-lifecycle`). El repo es autoridad del contrato técnico; esta nota conserva estado/progreso/routing.
- Checklist atómico T01–T17: repo `specs/FEAT-LOOM-V01/TASKS.md`; orden/gates/gobernanza: repo `specs/FEAT-LOOM-V01/PLAN.md`.

## 🔒 Contratos congelados — routing (repo = autoridad)

- **SPEC (`specs/FEAT-LOOM-V01/SPEC.md` @ `b031006`):** product definition · committed scope F1–F5 · non-goals · domain model (identidad path-based NFC, projections) · matriz canonical/derived + invariante de reconstrucción · architecture boundaries y forbidden deps · filesystem ownership (backend único dueño del fs) · storage (NO SQLite) · Graphify (sin dependencia) · API contract v0.1 (identity por path, security invariant DocumentID) · frontend (Vue 3, polling de generation, sin Pinia) · error/consistency model (best-effort scan + snapshot inmutable + swap atómico) · test strategy (fixtures reales, piso ≥95% vault+index).
- **TASKS (`specs/FEAT-LOOM-V01/TASKS.md`):** checklist atómico T01–T17 con deps/allowed files/AC/tests/non-goals + dependency graph (secuencia estricta por MAX_CONCURRENT_LOOM_SUBAGENTS=1).
- **PLAN (`specs/FEAT-LOOM-V01/PLAN.md`):** roadmap F1–F5 con gates · subagent model (R1–R4, límite 1) · TOP/NORMAL/GOD boundaries · orchestration contract · closure conditions.
- Los ADRs L1–L13 (decisiones + rationale) permanecen en esta nota (§ 🧭 Decisiones). Cambio de contrato = GOD del owner, actualizando el repo, nunca mutación silenciosa.

## 🧩 Subproyectos

_No aplica — este es el subproyecto de fundación/implementación de Loom; no crea más hijos._

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. Estado atómico T01–T17: repo `specs/FEAT-LOOM-V01/TASKS.md`. %%
> - [ ] WP-A Scaffold: T01 Go scaffold (module github.com/xKoRx/loom, binario loom) + T02 Web scaffold #owner/agent #type/dev #area/personal
> - [ ] WP-B Parse core: T05 fixtures → T03 frontmatter → T04 body #owner/agent #type/dev #area/personal
> - [ ] WP-C Index + live refresh: T06 scanner/snapshot/watcher/generation → T07 projections → T08 links/backlinks → T09 rebuild invariance #owner/agent #type/dev #area/personal
> - [ ] WP-D API: T10 meta/projects/areas + security boundary → T11 notes/render/search/tasks → T12 diagnostics #owner/agent #type/dev #area/personal
> - [ ] WP-E Frontend (secuencial): T13 shell + generation polling → T14 viewer → T15 cockpit → T16 search/diagnostics #owner/agent #type/dev #area/personal
> - [ ] WP-F Gates: T17 e2e + hardening live refresh + build binario único #owner/agent #type/dev #area/personal

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

- **2026-09-13 (EXECUTION START):** pre-flight git PASS sobre `~/go/src/github.com/xKoRx/loom` (remote `git@github.com:xKoRx/loom.git`, branch `master`, worktree clean, HEAD `5afd63e468e7a2104a175a727a961e4f678c09ea` == origin/master; commit "Initial commit" 2026-09-13T01:06:31-03:00, árbol = README.md) → **B1 RESUELTO** (repo creado físicamente por el owner; baseline real registrado sin SHA inventado). Contratos congelados migrados del planner al repo `specs/FEAT-LOOM-V01/` (SPEC/TASKS/PLAN @ `b031006b400e37a3a4647abc6049161bd2c2a7d6`) según patrón Echo E-01: repo = autoridad del contrato; esta nota conserva estado/routing; una fuente por hecho. WP-A desbloqueado; T01 = READY. Nota de gobernanza: T01/T02 son scaffold TOP-level (los allowed-scope de R1–R4 no los cubren) → los ejecuta el orchestrator; R1–R4 subagents para T03–T17, uno a la vez.

- **2026-09-13 (FOUNDATION FINALIZATION):** decisiones owner + execution constraints aplicadas al planner aceptado, sin reabrir arquitectura. **(1) Rename:** Project Lens → **Loom** (git mv con historial; aliases históricos preservados en frontmatter; links activos actualizados). **(2) Repo/workspace:** `xKoRx/loom` · `~/go/src/github.com/xKoRx/loom` · módulo `github.com/xKoRx/loom` · binario `loom` · branch `master` declarados; verificación física del repo: NO existía entonces → acción exacta registrada en Blockers, sin SHA inventado. **(3) Live refresh core en F1:** backend dueño exclusivo del fs (watch fsnotify → debounce → rebuild → snapshot inmutable → swap atómico → generation++), `generation` expuesto en `/api/v1/meta`, Vue observa generation por polling HTTP y refetch de la vista actual; sin WebSockets/SSE/event bus/push; F5 reclasificado como hardening del mismo mecanismo. T06/T10/T13/T17 extendidos; hard boundary frontend (cero fs) registrada. **(4) Concurrencia:** `MAX_CONCURRENT_LOOM_SUBAGENTS = 1` — sin R2∥R3; especialista no lanza subagents. **(5) Security invariant:** DocumentIDs HTTP se resuelven EXCLUSIVAMENTE contra el snapshot publicado; jamás `vaultRoot + requestPath → os.Open`; security tests en T10/T11. ADRs L11–L13. Cero product code en fundación.

- **2026-09-13 (FOUNDATION REVIEW — CORRECTION):** review del owner: arquitectura y roadmap ACCEPTED; 4 correcciones load-bearing aplicadas — (1) **Identity/API:** Project identity == source Note path; API re-addressada (`/projects/{path...}`, `resolve?name=&alias=` convenience fail-closed, `tasks?project=<path>`, rutas Vue `/project/*path`); (2) **Boundary:** EntityEnvelope/Task projection separadas conceptualmente de la extracción raw — Frontmatter VO es map crudo genérico en vault/parse y el envelope vive en la capa Agents-OS de index (T03/T07); (3) **Scan:** congelado best-effort scan + immutable snapshot + atomic publication/swap, sin locking; (4) **MCP rationale:** deferred por falta de consumidor agent-facing en v0.1; reopen trigger = necesidad demostrada de query/retrieval programático sobre el producto.

- **2026-09-13 (F0 — sesión de fundación/rebase):** rebase completo del proyecto sobre el Agents-OS vigente: convención parent/agentes (referencia Echo E-01), schema contract, muestreo real del vault (2741 notas; sin id system → identidad path-based; 218 alias links / 20 heading / 13 embeds / 0 block refs; 349 tasks con owner; estados legacy malformados presentes) y Graphify (contrato + binario ausente). Decisión de dominio validada con evidencia: Project/Area = typed projections de Note; identidad = path + TitleName/aliases; 5 estados de task + owner tags. Storage: sin SQLite (in-memory snapshot). Graphify: sin dependencia, semántica alineada. Planner original escrito con adversarial pass de 5 correcciones: (1) eliminada la capa VaultID/EntityID (duplicaba autoridad de identidad sin evidencia); (2) interfaces SearchProvider/GraphProvider retiradas por YAGNI; (3) goldmark render movido a `internal/serve`; (4) proyecciones Project/Area sacadas de `internal/vault` hacia `internal/index`; (5) resuelta contradicción del "único touchpoint" de parsing (goldmark permitido en `parse` y `serve`, nunca en el dominio). Bloqueo registrado: B1. Cero product code en fundación.

## 🧭 Decisiones (frozen ADRs con matriz CURRENT NEED? / EXPENSIVE TO CHANGE?)

- **ADR-L1 Markdown = única autoridad; todo derivado reconstruible (Y+Y).** Invariante verificada por test (T09). No hay estado irreconstruible en v0.1.
- **ADR-L2 Note identity = path vault-relativo NFC; routing = TitleName + aliases; sin id system (Y+Y).** Evidencia: no existe `id:`/`uid:` global en el vault (solo incidental en tickets/ADRs); Obsidian y Graphify resuelven por nombre/alias.
- **ADR-L3 Go binario único + SPA Vue 3 embebida `go:embed` + bind 127.0.0.1 (Y+Y).** Sin Electron/Wails en v0.1 (Wails v3 alpha; wrapper = future driver).
- **ADR-L4 Índice in-memory; NO SQLite v0.1 (Y+N → opción más simple).** 2741 notas; queries = rollups/lookups. Re-apertura solo por disparadores del SPEC § Storage.
- **ADR-L5 Project/Area = typed projections de Note; una sola fuente de verdad (Y+Y).** Validado con evidencia: todo el estado de proyecto vive en frontmatter+body.
- **ADR-L6 Render Markdown server-side (goldmark); SPA consume HTML sanitizado (Y+N → más simple).** Evita duplicar parser en cliente; bloques dinámicos = raw.
- **ADR-L7 Sin dependencia de Graphify; semántica de relaciones alineada a su allowlist (N+Y → seam mínimo).** Convergencia futura (MCP) sin acoplamiento ni SPOF; binario ausente en esta máquina lo confirma como decisión, no como accidente.
- **ADR-L8 Bloques dinámicos (dataviewjs/base/tasks) = código crudo + panels propios equivalentes donde existan (Y+N).** Loom replica las proyecciones concretamente usadas, no un engine de queries.
- **ADR-L9 Ciclo de task de 5 estados (todo/wip/review/done/canceled) + owner/type/flags como parte del modelo (Y+Y).** Evidencia: convenciones + 349 tasks con `#owner/*`.
- **ADR-L10 Modelo de seguridad local: read-only, loopback-only, path traversal prohibido, sin contenido remoto, CSP (Y+Y).** Es la razón de ser del producto tras el veto.
- **ADR-L11 Live refresh es comportamiento core de v0.1 (owner, 2026-09-13): backend dueño exclusivo del fs — fsnotify + debounce → rebuild → snapshot inmutable → swap atómico → generation monotónico expuesto en `/api/v1/meta`; Vue observa generation por polling HTTP y refetch (Y+Y).** Sin WebSockets/SSE/event bus/push infra en v0.1 (reabrible por evidencia); F5 = hardening del mismo mecanismo, nunca su introducción.
- **ADR-L12 Ejecución estrictamente secuencial (owner, 2026-09-13): `MAX_CONCURRENT_LOOM_SUBAGENTS = 1`; sin delegación recursiva; capacidad global compartida con otros tracks (N+Y → constraint operacional, no arquitectura).** Overridea la independencia file-level; el ownership R1–R4 por package se preserva.
- **ADR-L13 Security invariant HTTP/DocumentID (owner, 2026-09-13): los path parameters NUNCA se unen al vault root para abrir archivos; resolución exclusiva contra el snapshot publicado; rechazo de absolutos/`..`/traversal/encoding inválido/no normalizados/identidades ausentes en el boundary (Y+Y).** Sin subsistema de seguridad separado; probado en T10/T11.

## Risks

- **R1 Política corporativa MELI (owner):** que el veto a Obsidian extienda el veto a binarios propios. Mitigación: desarrollo y uso en máquina personal; F9 (export estático) es el plan B documentado; decisión owner ANTES de invertir horas de uso diario.
- **R2 Unicode/encoding en paths:** áreas con acentos y `&` ("Economía de Tokens", "Casa & Energía"). Mitigación: NFC + case-preserved + tests desde T03.
- **R3 Frontmatter legacy/malformado:** evidenciado (valores `PENDING|RUNNING|…`, tipos no contractuales). Mitigación: tolerancia fail-open por nota + diagnostics desde T03.
- **R4 Dialecto Obsidian del Markdown:** callouts (`> [!info]`), embeds, comentarios `%% %%`, wikilinks a headings. Mitigación: corpus real como fixture desde T05; render subset declarado (lo no soportado queda raw legible).
- **R5 Scope creep hacia "knowledge runtime":** la idea de agosto propone SQLite day-1, MCP y Context Bundles. Mitigación: non-goals congelados con por qué; future drivers con disparadores de re-apertura explícitos.
- **R6 ~~Repo sin crear~~ RESUELTO (2026-09-13):** repo verificado, baseline registrado, B1 cerrado, WP-A desbloqueado.
- **R7 Concurrency limit:** MAX_CONCURRENT_LOOM_SUBAGENTS=1 alarga el wall-clock de ejecución. Mitigación: secuencia definida por dependencias reales; trabajo paralelo identificado se encola como READY para review del owner.

## Blockers

- ~~**B1 (acción física del owner, bloqueaba WP-A):**~~ **RESUELTO 2026-09-13:** repo `xKoRx/loom` verificado en GitHub y workspace (baseline `5afd63e468e7a2104a175a727a961e4f678c09ea`, branch `master`, worktree clean); contratos migrados al repo; WP-A ejecutable. Sin blockers activos.
- No bloquear por: Graphify stale/ausente, frontmatter legacy del vault, o notas malformadas — todo eso es input válido del dominio con manejo definido.

## Acceptance gates (F0→ejecución)

- [x] Proyecto cargado, Agents-OS inspeccionado, vault real muestreado, Graphify inspeccionado, Vue 3 congelado, dominio/identidad/matriz/boundaries/dependencias definidos (F0, 2026-09-13).
- [x] v0.1 scope cerrado · future drivers separados · CouchDB/MCP/plugins/semantic/SQLite/WebSockets NO implementados · seams mínimas · roadmap vertical · tasks atomizadas · gates por fase · test strategy · subagent strategy · orchestration · adversarial pass ×3 (fundación, review, finalización).
- [x] **OWNER:** nombre canónico (Loom) + repo (xKoRx/loom) + workspace + módulo + binario + branch decididos.
- [x] **OWNER:** crear repo `xKoRx/loom` (branch `master`) + workspace local — **DONE, verificado 2026-09-13** (baseline `5afd63e`); desbloquea WP-A.
- [ ] **OWNER:** política MELI validada (gate de riesgo, no técnico; no bloquea el desarrollo en máquina personal).

## 🔗 Docs / Links

- [[Loom]] — proyecto padre (owner decisions, tarea puente; nombre histórico: Project Lens).
- Repo `xKoRx/loom` (`~/go/src/github.com/xKoRx/loom`): `specs/FEAT-LOOM-V01/SPEC.md` (contrato congelado) · `specs/FEAT-LOOM-V01/TASKS.md` (checklist atómico T01–T17) · `specs/FEAT-LOOM-V01/PLAN.md` (roadmap/gobernanza).
- [[2026-08-25-project-lens-knowledge-runtime]] — idea de origen (promovida; nombre histórico: Project Lens).
- Convenciones vigentes: [[convenciones]] · contrato de schema: `80-agents/skills/_shared/schema-contract.md` · Graphify: [[graphify-contract]].
- Referencia de patrón de ejecución: [[Echo — E-01 Canonical SDK Foundation S0]] (parent/agentes/SPEC/TASKS/gates).
- Refs técnicas: goldmark (parse/render), fsnotify (watcher F1, hardening F5), Vue 3 + Vite + vue-router. Sin más deps.

## 💡 Ideas

### Backlog de ideas

- MCP adapter read-only (`loom.search/get_document/list_projects/query_tasks/backlinks/build_context`) — F8, sólo con evidencia de necesidad de agentes (reopen: query/retrieval programático sobre Loom).
- Graph view de entidades — F6; datos de links ya existen desde F1.
- Export snapshot estático (HTML navegable) — F9, plan B si la política MELI prohíbe binarios propios.
- CLI `loom serve|query` — se decide con el repo; `cmd/loom` ya es la semilla.

### Motivos / principios

- Una fuente por hecho: el vault es la autoridad; esta nota es el plan de estado; el repo es el código y el contrato.
- Small core, clear boundaries, few abstractions: boundaries de package reales, cero interface-per-class.
- Read-only primero: Loom nunca compite con el editor ni repite la superficie vetada.
- El backend es el único que toca el vault; la UI sólo ve snapshots publicados.

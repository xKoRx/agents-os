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
start: 2026-09-17
due:
progress: 0
repo: xKoRx/loom
jira:
prs:
aliases:
  - Loom Design System
  - Loom Storybook
  - DS-F01
tags:
  - kind/project
  - area/personal
  - agent/owner
created: "2026-09-17"
updated: "2026-09-17"
cssclasses:
  - wide
---

# Loom — Design System & Storybook

%% Naming: Loom — Design System & Storybook es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Loom — Design System & Storybook
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Loom]] · **Repo:** `xKoRx/loom` (**VERIFIED** 2026-09-17; baseline `848fb28f12e92f8220792e4ba55fc9b78571fd26`, branch `master`; feature `feature/loom-design-system`)
> Subproyecto de agente: **fundación del design system + integración Storybook** para Loom, ordenada por el owner el 2026-09-17. No reabre [[Loom — Foundation v0.1]] (cierre 100% @ `848fb28`, en Review del owner). Los componentes existen una sola vez: la app y Storybook importan el mismo código. Entrega fundación, NO el rediseño completo de pantallas.

## 🎯 Objetivo

- Design system real compartido por la app Loom y Storybook: tokens CSS como contrato, componentes compartidos con un solo consumidor real mínimo, stories con estados pertinentes, y Storybook (framework `@storybook/vue3-vite`) integrado dentro de `internal/web/` sin tocar el binario productivo (`go:embed` sigue embebiendo sólo `dist/`).
- Preparar el terreno de R1–R5 del owner (navegación por carpetas, notes content-first, atributos ocultos, acceso opcional a proyectos/relaciones/frontmatter, componentes/estilos compartidos) sin implementar el rediseño ni decidir la arquitectura final de información (pendiente del review UX).

## 📊 Estado actual

- **ITERACIÓN INICIADA (2026-09-17):** baseline verificado `848fb28` == origin/master, worktree clean; rama `feature/loom-design-system` creada. Inventario frontend completo (ver Bitácora). Implementación en curso.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| `xKoRx/loom` (**VERIFIED** 2026-09-17) | `feature/loom-design-system` | `848fb28f12e92f8220792e4ba55fc9b78571fd26` (master, cierre Foundation v0.1) | Mandato del owner 2026-09-17 "Loom Design System & Storybook Foundation" (§2, §4–§9, §11–§13, §15) — registrado en esta nota y en [[Loom]] | Esta nota § Tareas + contratos del repo `specs/FEAT-LOOM-V01/` vigentes (sin mutar) | **EXECUTING** |

- Política: ejecución en rama feature aislada; sin force push; sin merge a master sin autorización del owner; `make web` / `make build` / smoke / e2e no cambian de semántica. Los SPEC congelados de FEAT-LOOM-V01 no se reabren; esta iteración es aditiva (design system) con migración incremental.

## 🔒 Contratos — routing

- **Mandato del owner (2026-09-17):** alcance, gates G1–G10 y criterios de aceptación §15 — viven en el mandato (registrado en el chat del owner); esta nota conserva estado, evidencia y decisiones de implementación.
- **Repo:** `specs/FEAT-LOOM-V01/` sigue siendo autoridad del contrato v0.1 (API, dominio, boundaries). Esta iteración NO muta esos SPECs.
- **Requisitos de producto vigentes del owner (R1–R5):** navegación por carpetas, notes content-first, atributos ocultos inicialmente, acceso opcional a proyectos/relaciones/frontmatter, componentes y estilos compartidos — el design system se prepara para ellos sin implementarlos.

## 🧩 Subproyectos

_No aplica — subproyecto de ejecución; no crea hijos._

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. %%
> - [x] Preflight + baseline: repo verificado @ `848fb28`, rama `feature/loom-design-system` #owner/agent #type/dev #area/personal ✅ 2026-09-17
> - [x] Inventario frontend: tokens, estilos globales, componentes reutilizables, duplicados, riesgos #owner/agent #type/dev #area/personal ✅ 2026-09-17
> - [/] Storybook: instalar `@storybook/vue3-vite` compatible con Vite 8/Vue 3.5, main.ts preview, scripts `storybook`/`build-storybook`, aislamiento de builds, gitignore #owner/agent #type/dev #area/personal
> - [ ] Tokens: extraer `:root` → `src/styles/tokens.css` + `base.css` compartidos (app y Storybook cargan los mismos) #owner/agent #type/dev #area/personal
> - [ ] Componentes compartidos con consumidor real: Button, Badge, Panel+SectionHeader, MetadataPanel, CopyButton, Breadcrumbs; StateBlock reubicado en ui/ #owner/agent #type/dev #area/personal
> - [ ] Stories por componente (variantes reales) + autodocs + controls #owner/agent #type/dev #area/personal
> - [ ] Migración incremental de las vistas a los componentes compartidos (comportamiento conservado) #owner/agent #type/dev #area/personal
> - [ ] Tests focalizados nuevos donde aporten valor #owner/agent #type/dev #area/personal
> - [ ] Gates G1–G9 (visual G10 si hay navegador) + commits con evidencia #owner/agent #type/dev #area/personal
> - [ ] Documentación mínima para agregar nuevos componentes (docs del design system en el repo) #owner/agent #type/dev #area/personal
> - [ ] Entrega: bitácora + RESULT en el vault; tarea puente a Review #owner/agent #type/dev #area/personal

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

- **2026-09-17 (BOOTSTRAP + PREFLIGHT + INVENTARIO):** Agents-OS cargado (constitución, perfil, continuidad, dominio DEFAULT sin router). Preflight PASS: `xKoRx/loom` master @ `848fb28f12e92f8220792e4ba55fc9b78571fd26` == origin/master, worktree clean; rama `feature/loom-design-system` creada. Inventario frontend (`internal/web/`): Vue 3.5 + vue-router 5.3 + Vite 8.3 + vitest 5 + TS 5.9 strict; 5 vistas (Home/Project/Note/Search/Diagnostics), 1 componente (`StateBlock.vue`), 5 composables con tests. Tokens ya normalizados en `:root` de `style.css` (dark-first: superficies bg/bg-subtle/bg-raised/bg-hover/bg-active, bordes, texto 3 niveles, accent único azul, task-states 5, semánticos success/warning/danger/info/stale, radios 4/6/10, spacing 4→64, font sans/mono, layout sidebar-w/content-pad/measure). Duplicados reales detectados: (1) `copyPath` clipboard logic idéntica en NoteView y ProjectView (~15 líneas ×2); (2) `envelopeRows` key-values casi idénticos en NoteView y ProjectView; (3) `.aside-section`/`.aside-title` panel en 5 usos en 3 vistas; (4) `h1.page-title`+`p.page-sub` en las 5 vistas; (5) `.btn` global con disabled y variante small; (6) `.badge` con vocabulario state-/owner-/flag-/orphan/plain. Candidatos sin consumidor real hoy (sólo documentar): DisclosurePanel (el fold de callouts es `<details>` server-rendered), NavigationItem (nav estática), FolderExplorer/FolderNode/NoteInspector/ProjectRelationPanel/SearchResult (R1–R4, requieren review UX). Riesgos: `dist/` está commiteado y embebido por `go:embed all:dist` → storybook output debe vivir fuera de `dist/` y en `.gitignore`; `npm ci` en `make web` debe seguir passando; sin cambios de API Go.

## 🧭 Decisiones

- **(agente, 2026-09-17) Alcance de componentes compartidos v0 = sólo patrones con consumidores reales:** Button (`.btn`, ≥5 consumidores), Badge (`.badge`, 3 vistas), Panel/SectionHeader (`.aside-section`/`.aside-title`, 3 vistas), MetadataPanel (`.note-envelope`, 2 vistas con lógica duplicada), CopyButton (clipboard duplicado en 2 vistas), Breadcrumbs (`.crumbs`, ProjectView; R1 la necesitará), StateBlock ya existe (se reubica a `ui/`). DisclosurePanel y NavigationItem quedan como candidatos documentados sin implementación (sin consumidor Vue real hoy). — Fundado en §7/§10 del mandato (no abstraer para un único consumidor; no fabricar estados).
- **(agente, 2026-09-17) Tokens: split físico, cero cambio visual:** `style.css` se divide en `src/styles/tokens.css` (`:root`) + `src/styles/base.css` (reset/focus/selection/links/code) + resto del stylesheet; la app importa los mismos archivos que el preview de Storybook. Sin theming engine, sin dark/light switch, sin tocar valores.

## Risks

- **R-A Compatibilidad Storybook ↔ Vite 8:** Vite 8 es muy nuevo; verificar la versión de `@storybook/vue3-vite` que lo soporta antes de instalar (fijar versión, actualizar lockfile). Fallback documentado si no hay soporte: seguir el pegado oficial vigente y declarar el delta.
- **R-B `dist/` commiteado + `go:embed all:dist`:** cualquier output de Storybook dentro de `dist/` se embebería en el binario. Mitigación: `storybook-static/` fuera de dist + `.gitignore` + G9 verificado.
- **R-C Regresión visual por extracción:** mitigación: migración incremental por componente, comportamiento conservado, vitest + build + smoke/e2e Go después de cada bloque.

## Blockers

- Ninguno activo. La decisión pendiente del review UX (arquitectura final de información) NO bloquea la fundación (mandato §0).

## 🔗 Docs / Links

- [[Loom]] — proyecto padre (decisiones del owner, tarea puente de esta iteración).
- [[Loom — Foundation v0.1]] — iteración anterior (cerrada 100%, en Review; NO reabierta).
- Repo `xKoRx/loom`: `internal/web/` (SPA + Storybook), `specs/FEAT-LOOM-V01/` (contratos congelados v0.1), `Makefile` (web/build/test/smoke/e2e).
- Convenciones vigentes: [[convenciones]].

## 💡 Ideas

### Backlog de ideas

- FolderExplorer/FolderNode cuando R1 tenga review UX (usan NavigationItem + Breadcrumbs).
- NoteInspector y ProjectRelationPanel para R3/R4 (DisclosurePanel como primitivo de atributos ocultos).
- Tests de interacción de stories (addon-vitest / play functions) cuando el catálogo estabilice.

### Motivos / principios

- Una sola implementación por componente: app y Storybook importan el mismo código; prohibido el twin de Storybook.
- Restraint heredado del stylesheet v0.1: sin gradientes, sin glow, sin glassmorphism; contraste accesible y tranquilo.
- Componentes visuales puros: props/slots/events tipados, sin fetch, sin estado global, sin dominio; la lógica sigue en composables.

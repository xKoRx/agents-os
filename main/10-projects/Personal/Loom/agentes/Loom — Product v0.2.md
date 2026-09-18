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
progress: 0
repo: xKoRx/loom
jira:
prs:
aliases:
  - Loom v0.2
  - FEAT-LOOM-V02
tags:
  - kind/project
  - area/personal
  - agent/owner
created: "2026-09-18"
updated: "2026-09-18"
cssclasses:
  - wide
---

# Loom — Product v0.2

%% Naming: Loom — Product v0.2 es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Loom — Product v0.2
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Loom]] · **Repo:** `xKoRx/loom` (**VERIFIED** 2026-09-18; master `848fb28` == origin/master; integración `feature/loom-v02`)
> Subproyecto de agente: **experiencia de producto + identidad Notion-inspired** para Loom, mandato del owner 2026-09-18 (LOOM v0.2). Ejecución con DOS subagentes concurrentes (Agente A = Loom UI, Agente B = Loom Product) bajo manager integrador único. Contratos congelados en el repo: `specs/FEAT-LOOM-V02/SPEC.md` + `COMPONENT-REGISTRY.md`.

## 🎯 Objetivo

- Evolucionar Loom v0.1 a un producto visualmente coherente (referencia Notion, sin ser clon), content-first y navegable por la estructura real del vault: fix de búsqueda, Note Viewer con inspector bajo demanda, Folder Explorer (`/api/v1/tree` + `/vault`), índice global de tareas (`/tasks`), cockpit depurado y design system Loom UI consolidado en Storybook. Entregable: UNA versión integrada y verificable en `feature/loom-v02`, sin merge a master.

## 📊 Estado actual

- **CONTRATOS CONGELADOS (2026-09-18):** rama `feature/loom-v02` @ `738de70` (base `b0e24a2` design system + lucide `09e6d1f`); SPEC v0.2 + Component Registry commiteados; decisiones D1 (API tree) y D2 (`/tasks`) autorizadas por el mandato, D4 (etiquetar system zones + filtro) y D5 (umbral Outline ≥5, supresión H1 duplicado) resueltas; D6 fuera de alcance. Gates del design system reejecutados PASS (vitest 126/126, vue-tsc, go build/vet/test, binario).
- **PREFLIGHT PASS:** worktree limpio (única excepción: `specs/FEAT-LOOM-V01/UX-IA-REVIEW-V0.1.md` untracked del owner — preservado intacto, sin promocionar a contrato); proceso `loom` sirviendo el vault en loopback (read-only, no interfiere); sin merge automático a master.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| `xKoRx/loom` (**VERIFIED** 2026-09-18) | `feature/loom-v02` (+ branches `feature/loom-v02-ui` A, `feature/loom-v02-product` B) | `09e6d1f` (= design system `b0e24a2` + lucide) sobre master `848fb28` | Mandato del owner "LOOM v0.2" 2026-09-18 + `specs/FEAT-LOOM-V01/UX-IA-REVIEW-V0.1.md` (SLICE-0…5, AC) | `specs/FEAT-LOOM-V02/SPEC.md` + `COMPONENT-REGISTRY.md` (congelados @ `738de70`) | **IN EXECUTION** |

- Política: rama de integración v0.2 + worktrees independientes por subagente; sin force push/reset --hard/clean destructivo; sin merge a master; contratos FEAT-LOOM-V01 no se reabren (la API tree es aditiva); dist productivo se consolida sólo en integración.

## 🧩 Subproyectos

_No aplica — subproyecto de ejecución; no crea hijos._

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. %%
> - [x] Preflight + reconciliación de baseline (master/origin/DS gates/auditoría UX preservada) #owner/agent #type/dev #area/personal ✅ 2026-09-18
> - [x] Component Contract Freeze: inventario + COMPONENT-REGISTRY congelado #owner/agent #type/dev #area/personal ✅ 2026-09-18 (`738de70`)
> - [x] SPEC v0.2 congelada + decisión MAX_CONCURRENT_LOOM_SUBAGENTS=2 registrada #owner/agent #type/dev #area/personal ✅ 2026-09-18
> - [x] Agente A — Loom UI: 9/9 componentes required (P0+P1) con stories+tests+commits #owner/agent #type/dev #area/personal ✅ 2026-09-18 (10 commits `922e854`→`0fa3e38`; gates: typecheck OK, vitest 164/164, storybook build OK; 2 desviaciones de contrato justificadas: Disclosure prop+emit equivalente a defineModel, TaskItem `noteHref`+emit `open`)
> - [/] Integración A verificada y publicada: merge --no-ff a `feature/loom-v02` @ `83f363e` (vitest 164/164 + storybook build en integración) #owner/agent #type/dev #area/personal ✅ 2026-09-18
> - [/] Agente B — Loom Product: SLICE-0 search fix en curso (test-first) → SLICE-2 explorer (API+UI) → SLICE-1 note viewer → SLICE-3 tasks → SLICE-5 cockpit; sync con `83f363e` enviado para migrar vistas a componentes A #owner/agent #type/dev #area/personal
> - [ ] Integración manager (App.vue sidebar, style.css, dist) + gates integrales + revisión visual navegador real #owner/agent #type/dev #area/personal
> - [ ] Entrega al owner (RESULT + evidencias + guías de review) #owner/agent #type/dev #area/personal

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

- **2026-09-18 (CHECKPOINT OWNER — PUBLICACIÓN):** preflight de los 3 worktrees consistente; commit identificado `a1f3fe4` incorpora la auditoría UX del owner byte-a-byte (sha256 `da429ccd` verificado pre/post commit); escaneo de secretos del diff limpio; `feature/loom-v02` publicada en origin por push normal (local == remoto `a1f3fe4`), sin tocar master ni los worktrees A/B (A sin commits aún, B WIP en test de regresión de búsqueda). Auditoría externa habilitada con: SPEC + Registry + auditoría en GitHub (`specs/FEAT-LOOM-V02/`, `specs/FEAT-LOOM-V01/UX-IA-REVIEW-V0.1.md`), planner en el vault.

- **2026-09-18 (BOOTSTRAP + PREFLIGHT + CONTRATOS):** Agents-OS cargado (constitución, perfil, continuidad, dominio DEFAULT). Preflight PASS: master `848fb28` == origin/master; DS branch `b0e24a2` verificada con gates reejecutados (vitest 126/126, vue-tsc clean, go build/vet/test ok); auditoría UX del owner preservada untracked. Decisión del owner registrada: **MAX_CONCURRENT_LOOM_SUBAGENTS = 2** para v0.2 (sustituye el límite 1 de v0.1 sólo en esta iteración; contrato histórico intacto). Creada `feature/loom-v02` desde DS + lucide pre-instalado por el manager (`09e6d1f`); SPEC + Registry congelados (`738de70`). Worktrees `loom-a` / `loom-b` creados; dispatch paralelo inmediato.

## 🧭 Decisiones

- **(owner, 2026-09-18) Concurrencia 2 subagentes para v0.2:** Agente A (Loom UI: `src/ui/**`, `src/styles/**`, `.storybook/**`) + Agente B (Loom Product: `views/composables/router/api`, `internal/index`, `internal/serve`); worktrees y branches exclusivos; manager único integrador de archivos compartidos (App.vue, style.css, package.json, dist, Makefile). No altera el contrato histórico v0.1.
- **(owner vía mandato, 2026-09-18) D1/D2/D4/D5:** API tree aditiva autorizada; `/tasks` autorizada; system zones se etiquetan + filtro (cero exclusión de datos); Outline ≥5 headings y supresión H1 duplicado; `%%comments%%` y snippets quedan como están (D6 fuera de alcance).

## Risks

- **R-1 doble writer en archivos compartidos:** mitigado por ownership congelado + consolidación exclusiva del manager; subagentes prohibidos de tocar App.vue/style.css/package.json/dist.
- **R-2 `dist/` trackeado + `go:embed`:** branches de subagentes no commitean dist; el manager reconstruye en integración (G9: Storybook fuera del binario).
- **R-3 dependencia B→A:** B arranca independiente (search fix, API, composables) y consume componentes de A sólo tras integración verificada en `feature/loom-v02`; prohibido twins provisionales.
- **R-4 repro intermitente del bug de búsqueda:** test de regresión con fake timers ANTES del fix (AC-0.4).

## Blockers

- Ninguno activo.

## 🔗 Docs / Links

- [[Loom]] — proyecto padre (decisiones del owner, tarea puente).
- [[Loom — Foundation v0.1]] · [[Loom — Design System & Storybook]] — iteraciones anteriores (en Review; NO reabiertas).
- Repo: `specs/FEAT-LOOM-V02/SPEC.md`, `specs/FEAT-LOOM-V02/COMPONENT-REGISTRY.md`, `specs/FEAT-LOOM-V01/UX-IA-REVIEW-V0.1.md` (insumo funcional del owner).

## 💡 Ideas

### Backlog de ideas

- P11 snippets legibles y P12 `%%comments%%` si el owner los prioriza en review.
- Tests de interacción de stories (play functions) cuando el catálogo v0.2 estabilice.

### Motivos / principios

- Una sola implementación por componente; vistas componen, no reimplementan.
- Identidad propia Notion-inspired, dark-first, sin theming engine; tokens existentes sin cambios de valor.
- Los Markdown siguen siendo la base de datos; el índice es derivado y reconstruible; read-only siempre.

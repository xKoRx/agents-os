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
progress: 5
repo: xKoRx/loom
jira:
prs:
aliases:
  - Loom v0.3
  - FEAT-LOOM-V03
tags:
  - kind/project
  - area/personal
  - agent/owner
created: "2026-09-18"
updated: "2026-09-18"
cssclasses:
  - wide
---

# Loom — Product v0.3

%% Naming: Loom — Product v0.3 es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Loom — Product v0.3
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Loom]] · **Repo:** `xKoRx/loom` (**VERIFIED** 2026-09-18; base `feature/loom-v02 @ 0cba972` certificada; master referencia `848fb28` intacto)
> Subproyecto de agente: **Daily Workspace + theming dark/light/System + Knowledge Graph local** para Loom, mandato del owner 2026-09-18 (LOOM v0.3). Ejecución con DOS subagentes concurrentes (Agente A = Loom UI, Agente B = Loom Product) bajo manager integrador único. Contratos congelados en el repo: `specs/FEAT-LOOM-V03/SPEC.md` + `COMPONENT-REGISTRY.md` + `FUTURE-WRITING.md` @ `f58c3ac` (rama `feature/loom-v03`, sin merge a master).

## 🎯 Objetivo

- Convertir Loom en second brain de uso diario: Home accionable que responde qué requiere atención, qué tareas son mías/delegadas, qué espera Review y qué proyectos están activos; identidad visual con temas dark/light/System de calidad Notion-like (sin copiar assets); Knowledge Graph local derivado 100% del snapshot para navegar relaciones; continuidad local (recientes/favoritos) y contrato documentado (no implementado) de escritura futura. Entregable: UNA versión integrada y verificable en `feature/loom-v03`, sin merge a master.

## 📊 Estado actual

- **SPEC CONGELADA + DISPATCH (2026-09-18):** discovery acotado ejecutado contra el repo y el vault vivo (matriz dato→fuente→API→gap en la SPEC; muestras reales: 2403 tareas, review 52, blocked 39, waiting 24, unassigned 814); contratos `specs/FEAT-LOOM-V03/` congelados @ `f58c3ac` en rama `feature/loom-v03` (base `0cba972`); D1 (filtro flag en /api/v1/tasks), D2 (relations en note detail), D3 (endpoint /api/v1/graph read-only acotado), D4 (theming), D5 (continuidad local) autorizadas por el mandato; MAX_CONCURRENT_LOOM_SUBAGENTS = 2; worktrees `loom-a`/`loom-b` sobre branches `feature/loom-v03-ui`/`feature/loom-v03-product`; dispatch A+B en paralelo.
- **Baseline verificado:** `feature/loom-v02 @ 0cba972447cd9a5752a1460f1fff9667dcefebea` == origin, worktree limpio; master `848fb28` == origin/master (sin merge); disciplina de tokens vigente (0 hex fuera de tokens.css; 7 rgba a tokenizar en v0.3).

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| `xKoRx/loom` (**VERIFIED** 2026-09-18) | `feature/loom-v03` (+ branches `feature/loom-v03-ui` A, `feature/loom-v03-product` B) | `0cba972` (v0.2.1 certificada + release prep) sobre master `848fb28` | Mandato del owner "LOOM v0.3" 2026-09-18 | `specs/FEAT-LOOM-V03/SPEC.md` + `COMPONENT-REGISTRY.md` + `FUTURE-WRITING.md` (congelados @ `f58c3ac`) | **IN EXECUTION** |

- Política: rama de integración v0.3 + worktrees independientes por subagente; sin force push/reset --hard/clean destructivo; sin merge a master; contratos v0.1/v0.2 no se reabren (todas las APIs nuevas son aditivas y read-only); dist productivo se consolida sólo en integración.

## 🧩 Subproyectos

_No aplica — subproyecto de ejecución; no crea hijos._

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. %%
> - [x] Preflight + baseline: `0cba972` verificado, rama `feature/loom-v03` creada desde el baseline certificado #owner/agent #type/dev #area/personal ✅ 2026-09-18
> - [x] Discovery acotado (≤90min): matriz dato→fuente→API→gap + muestras reales del vault #owner/agent #type/research #area/personal ✅ 2026-09-18
> - [x] SPEC v0.3 + COMPONENT-REGISTRY addendum + FUTURE-WRITING congelados en repo @ `f58c3ac` #owner/agent #type/dev #area/personal ✅ 2026-09-18
> - [/] Agente A — Loom UI: theming dark/light/System (tokens, composable theme, LoomThemeToggle, Storybook con temas, audit tokenización) con stories+tests #owner/agent #type/dev #area/personal
> - [/] Agente B — Loom Product: S1 Daily Workspace · S2 presets de tasks + filtro flag · S3 supervisión de proyectos · S4 continuidad local #owner/agent #type/dev #area/personal
> - [ ] Integración P0 (manager): merges a `feature/loom-v03`, App.vue/index.html/style.css, dist, gates #owner/agent #type/dev #area/personal
> - [ ] Agente B — Knowledge Graph local (P1): API `/api/v1/graph` + GraphView + filtros + límites + estados #owner/agent #type/dev #area/personal
> - [ ] Gates integrales + recorrido completo del mandato (3 resoluciones × dark/light/system, teclado, deep links, live-refresh) #owner/agent #type/dev #area/personal
> - [ ] Evidencia visual sintética (contact sheets dark/light, manifiesto SHAs) + paquete local fuera del repo #owner/agent #type/dev #area/personal
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

- **2026-09-18 (BOOTSTRAP + DISCOVERY + SPEC FREEZE + DISPATCH):** Agents-OS cargado (constitución, perfil, continuidad, dominio DEFAULT — Loom es área Personal). Preflight PASS: `feature/loom-v02 @ 0cba972` == origin (baseline certificado del mandato), master `848fb28` intacto, disciplina de tokens verificada (0 hex fuera de tokens.css). Discovery acotado contra el vault vivo en loopback (meta 3263 notas / 138 proyectos / 2403 tareas; owner=me/todo 239, review 52, blocked 39, waiting 24, unassigned 814) y contratos del repo (SPEC/REGISTRY v0.2, TaskIndex, relations allowlist, guard de seguridad). Gap API: filtro por flags (D1), relations por nota (D2), grafo (D3). Rama `feature/loom-v03` creada desde `0cba972`; SPEC + Registry addendum + FUTURE-WRITING congelados @ `f58c3ac`; worktrees A/B repuntados a `feature/loom-v03-ui`/`feature/loom-v03-product` (conservando node_modules de v0.2); dispatch paralelo A (theming) + B (P0 product, luego graph).

## 🧭 Decisiones

- **(owner vía mandato, 2026-09-18) D1–D6:** ver SPEC §Decisiones del owner — filtro flag aditivo en /api/v1/tasks; relations aditivo en note detail; /api/v1/graph read-only derivado del snapshot con caps (depth≤2, max≤200, truncation determinista); theming dark/light/system con anti-flash y persistencia local; continuidad local (recientes/favoritos ≤20, ids only, nunca autoridad de Agents-OS); escritura futura SÓLO como contrato documentado (FUTURE-WRITING.md), sin implementación.
- **(manager, 2026-09-18) Concurrencia 2 subagentes para v0.3:** prolonga la decisión v0.2 con el mismo ownership (A=ui/styles/storybook + `composables/theme.ts` nuevo exclusivo; B=vistas/composables/router/api/index/serve/e2e); manager único integrador de App.vue, index.html, style.css, package.json, dist y Makefile. No altera contratos históricos.

## Risks

- **R-1 doble writer en archivos compartidos:** mitigado por ownership congelado + consolidación exclusiva del manager; subagentes prohibidos de tocar App.vue/index.html/style.css/package.json/dist.
- **R-2 theming rompe vistas existentes:** el dark queda bit-a-bit (`:root` intacto); light es override nuevo; gates visuales en ambos temas antes de integrar.
- **R-3 graph sobre-notas con 3263 documentos:** caps duros (depth≤2, max≤200) + truncation determinista; nunca carga el vault completo; sin motor externo.
- **R-4 dependencia B→A:** B consume componentes de A sólo tras integración verificada en `feature/loom-v03`; prohibido twins provisionales.

## Blockers

- Ninguno activo.

## 🔗 Docs / Links

- [[Loom]] — proyecto padre (decisiones del owner, tarea puente).
- [[Loom — Foundation v0.1]] · [[Loom — Design System & Storybook]] · [[Loom — Product v0.2]] — iteraciones anteriores (en Review; NO reabiertas).
- Repo: `specs/FEAT-LOOM-V03/SPEC.md`, `specs/FEAT-LOOM-V03/COMPONENT-REGISTRY.md`, `specs/FEAT-LOOM-V03/FUTURE-WRITING.md`.

## 💡 Ideas

### Backlog de ideas

- Virtualización del tree y del índice de tareas si la escala lo pide (3263 notas hoy).
- Favoritos/recientes compartidos por(sync) si algún día hay backend multi-dispositivo (fuera de v0.3 por diseño).

### Motivos / principios

- Los Markdown siguen siendo la base de datos; el índice es derivado y reconstruible; read-only siempre.
- El grafo es una navegación derivada del snapshot, no una nueva autoridad de conocimiento.
- Estado documentado ≠ actividad en runtime: la UI nunca inventa presencia de agentes.

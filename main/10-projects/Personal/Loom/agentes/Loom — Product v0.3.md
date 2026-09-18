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

- **HOTFIX RC2 READY FOR OWNER ACCEPTANCE (2026-09-18):** mandato de Dirección Técnica ejecutado — dos defectos del grafo corregidos sobre la RC `3f13ea1` y publicados en `origin/feature/loom-v03 @ 5636e4f` (== local, push normal; master `848fb28` y v0.2 intactos). **FIX 1** (`f38a5f7`): los chips de kinds de GraphView se derivaban de la respuesta ya filtrada → al activar un tipo los demás desaparecían (irreversible en deep link/refresh); ahora los chips cubren SIEMPRE el vocabulario congelado (opciones separadas del resultado filtrado; respuesta sólo atenúa is-off/is-absent), sin segundo fetch ni API nueva; reproductor a nivel vista (SSR+router) RED→GREEN + unitarios `graphKindChips`. **FIX 2** (`5fb93ad`): el truncado (primeros N alfabético) podía excluir el centro; contrato corregido — centro SIEMPRE presente, `max-1` restantes alfabéticos, sin colgantes, `max=1` → centro exacto; SPEC §3 actualizada sólo en truncado; regresión de masa (centro tras 150 vecinos, max 100/2/150/500) + byte-stability. **FIX 3:** fixture sintético `fixture-truncated` (151 notas) ejercita el indicador en Chromium: `verify-truncation.mjs` 21/21 (centro, indicador, límite 100, chips tras filtrar con dos kinds reales, Back/Forward, refresh, navegación, dark/light). Gates re-ejecutados sobre el SHA final: gofmt/vet · go test 6/6 · race limpio · vue-tsc · vitest 274 · storybook build · dist reproducible · smoke · e2e 10/10 · live-refresh 6/6 · G9 · hex/rgba 0 · seguridad graph 25 checks · secret scan limpio. Evidencia: sheets regeneradas (grilla 2×N inspeccionable, judge PASS), capturas 44, MANIFEST RC2 con SHAs; RC1 preservada en `archive/`. Pendiente: aceptación humana del owner.
- **READY FOR OWNER ACCEPTANCE (2026-09-18):** `origin/feature/loom-v03 @ 3f13ea1` == local (push normal, sin merge a master; master `848fb28` intacto). P0 + P1 completos e integrados: theming dark/light/system con anti-flash + persistencia (defecto real de persistencia hallado en walkthrough y corregido RED→GREEN `4d465db`), Daily Workspace accionable (continuidad + 6 colas + cockpit), presets de tasks con D1/D1b (flag + CSV) y D2 (relations), supervisión de proyectos, Knowledge Graph local (D3: `/api/v1/graph` con caps + GraphView radial determinista + acción Graph en NoteView). Gates integrales sobre el SHA final: gofmt/vet/test 6/6 · race serve+index limpio · vue-tsc · vitest 269 · storybook build · dist reproducible · smoke · e2e 10/10 · live-refresh 6/6 · G9 · hex/rgba 0 fuera de tokens.css · secret scan limpio · recorrido del mandato 22/22 PASS en Chromium real (3 resoluciones, dark/light/system, teclado, deep links, Back/Forward) · grafo verificado en navegador (navegación por click y teclado, filtros kinds, depth 2, hostile 400/404, empty state útil). Evidencia sintética: paquete completo `~/go/src/github.com/xKoRx/loom-v03-evidence/` (36 capturas, contact sheets dark/light, MANIFEST) + subconjunto en repo `specs/FEAT-LOOM-V03/evidence/`. Reviews de v0.1/DS/v0.2 intactas.
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
> - [x] Agente A — Loom UI: theming dark/light/System (tokens, composable theme, LoomThemeToggle, Storybook con temas, audit tokenización) con stories+tests #owner/agent #type/dev #area/personal ✅ 2026-09-18 (6 commits `fe5c67f`→`cea6fa7`; vitest 231, storybook build, contraste AA light; merge `0e59998`)
> - [x] Agente B — Loom Product: S1 Daily Workspace · S2 presets de tasks + filtro flag · S3 supervisión de proyectos · S4 continuidad local #owner/agent #type/dev #area/personal ✅ 2026-09-18 (6 commits `1f8dda5`→`1077251`; smoke vivo D1/D1b/D2; merge `704ab92`)
> - [x] Integración P0 (manager): merges a `feature/loom-v03`, App.vue/index.html/style.css, dist, gates #owner/agent #type/dev #area/personal ✅ 2026-09-18 (`664db33`; fix persistencia tema RED→GREEN `4d465db`; walkthrough 22/22)
> - [x] Agente B — Knowledge Graph local (P1): API `/api/v1/graph` + GraphView + filtros + límites + estados #owner/agent #type/dev #area/personal ✅ 2026-09-18 (4 commits `39b2b19`→`f5db2fa`; race serve limpio; merge `21e6155`)
> - [x] Gates integrales + recorrido completo del mandato (3 resoluciones × dark/light/system, teclado, deep links, live-refresh) #owner/agent #type/dev #area/personal ✅ 2026-09-18 (todos PASS @ `a7a7f91`/`3f13ea1`; grafo 10/12 navegador + 2 limitaciones documentadas en MANIFEST)
> - [x] Evidencia visual sintética (contact sheets dark/light, manifiesto SHAs) + paquete local fuera del repo #owner/agent #type/dev #area/personal ✅ 2026-09-18 (`~/go/src/github.com/xKoRx/loom-v03-evidence/`; subconjunto en repo `specs/FEAT-LOOM-V03/evidence/`)
> - [x] Hotfix RC2 (mandato Dirección Técnica): FIX 1 filtros kinds de GraphView (test reproductor RED→GREEN) + FIX 2 truncado preserva el centro (SPEC §3) + FIX 3 fixture truncado verificado en Chromium 21/21 + gates completos #owner/agent #type/dev #area/personal ✅ 2026-09-18 (`f38a5f7` + `5fb93ad` + evidencia `5636e4f`; publicado `origin/feature/loom-v03 @ 5636e4f`)
> - [r] Entrega al owner (RESULT + evidencias + guías de review) #owner/agent #type/dev #area/personal — publicada `origin/feature/loom-v03 @ 5636e4f` (hotfix RC2), a Review del owner

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

- **2026-09-18 (HOTFIX RC2 — mandato de Dirección Técnica, sin reabrir discovery ni v0.4):** verificado el estado real primero (worktree `feature/loom-v03` limpio @ `3f13ea1` == origin; worktrees A/B intactos; master `848fb28` sin tocar). **FIX 1 — filtros del grafo:** defecto confirmado con test reproductor a nivel vista (SSR + router en memoria + useGraph stub; 3/3 FAIL antes del fix) — la leyenda salía de `presentKinds(respuesta)` y la respuesta ya viene filtrada por `kinds`, colapsando los controles sobre la selección activa. Solución conforme al mandato (sin API nueva, sin segundo fetch): chips desde el vocabulario congelado (`graphKindChips`, opciones separadas del resultado filtrado), la respuesta sólo atenúa (`is-off` lo filtrado, `is-absent` lo ausente); leyenda visible también cuando un filtro deja 0 edges (escape) y oculta en neighborhood sin aristas. **FIX 2 — centro del grafo:** regla vieja "primeros N alfabético" podía excluir el DocumentID central (documentado así deliberadamente en la RC); contrato corregido en `graph.go` + SPEC §3 (sólo apartado de truncado): centro SIEMPRE en `nodes`, restantes `max-1` alfabéticos entre no-centro, orden alfabético intacto, edges filtrados a ambos extremos, `truncated=true` cuando corresponde, `max=1` → centro exacto; regresiones: reescritura de max=1/2/3 (el caso max=1 viejo fijaba la exclusión del centro) + masa con centro alfabéticamente posterior a 150 vecinos (max 100/2/150/500) + byte-stability. **FIX 3 — prueba visual:** fixture sintético `fixture-truncated` (151 notas: 150 vecinos `40-archive/…` que ordenan ANTES que el centro `50-resources/Truncation Hub.md`; link + related_to reales) en `loom-v03-evidence/`; `verify-truncation.mjs` en Chromium: **21/21 PASS** (centro visible, indicador "truncated at max 100", límite 100, chips=10 tras filtrar, deep link kinds=, añadir/quitar/volver-a-todos con dos kinds, Back/Forward con disciplina replace — Back sale a /vault y Forward restaura el estado filtrado, refresh con filtro, click-nodo→nota, dark/light). **Gates sobre el SHA final `5fb93ad`:** gofmt/vet limpios · go test 6/6 · race serve+index · vue-tsc · vitest 274 · storybook build · dist reproducible (== commiteada, commiteada con FIX 1) · smoke · e2e 10/10 · live-refresh 6/6 · G9 0×"storybook" · hex/rgba 0 · seguridad `/api/v1/graph` 25 checks (hostiles 400/404/503, nunca 500) · secret scan limpio. **Evidencia:** capturas 44 (incluye 82-graph-truncated y 83-graph-truncated-filtered en dark/light); contact sheets regeneradas como grilla 2×N a 2048px (~69% tamaño nativo, texto legible — requisito del mandato), judge visual PASS en ambas; sheets RC1 preservadas en `archive/`; MANIFEST RC2 en repo + paquete local con SHA final de producto. Push normal `3f13ea1..5636e4f`; sin merge a master; sin cerrar reviews humanas. RESULT: **RC_READY**. Run register: `80-agents/journal/agent-runs/2026-09-18-zcode-glm-loom-v03-hotfix-rc2.md`.

- **2026-09-18 (AUDITORÍA DEL MANAGER EN PARALELO — semántica de colas + theming + verificación independiente del grafo):** sesión de auditoría concurrente a la ejecución de B, sobre el checkpoint publicado `4d465db`. **Colas (§3 del mandato):** conteos verificados contra el vault real (my 261 · review 52 = me 33/agent 15/sin owner 4 · blocked 39 · waiting 24 con 2 done · delegadas 246 · sin responsable 559); Review es owner-neutral con responsable visible (badge por fila); delegadas sin inferir ejecución; filtros AND entre dimensiones y OR sólo dentro del CSV de estados; las colas Blocked/Waiting son tag-views "any state" (congelado en SPEC) — se hizo explícito en microcopy ("#blocked tag · any state", "state review · owner shown") `2753f8c`; regresión nueva de intersecciones en `serve/tasks_test.go` (flags coexisten en una tarea, flag×state, review×owner, owner×state×flag). **Theming (§4) en Chromium real:** 2 defectos corregidos — badges con paths largos desbordaban horizontalmente la grilla de colas (fix en LoomTaskItem: ellipsis en badges del meta) y `--text-faint` dark 3.15→4.66:1 (AA en microcopy 11px) `dff1af3`; verificados dark/light/system/persistencia/anti-flash (script inline en index.html)/contraste (dots 4.5–8.5:1; canceled 2.6:1 dark = des-énfasis deliberado). **Grafo (§2) verificado independientemente:** contrato D3 al pie de la letra (snapshot-only, sin fs en handlers, self-loops/attachments excluidos, vocabulario kinds único); probes hostiles (traversal/NFC/depth/max/kinds → 400/404, clamp max=99999→200 verificado, payloads byte-idénticos); E2E real: click en nodo → nota correcta (`/note/20-areas/Personal`), depth 2 con truncamiento explícito en UI, estado vacío de nota aislada, kinds filtran en UI, acción Graph en NoteView, light/dark con tokens. **Gates re-ejecutados independientemente sobre `a7a7f91`/`3f13ea1`:** go test 6/6 + race limpio + vet + gofmt, vitest 269, vue-tsc, storybook build, smoke, e2e 10/10, live-refresh 6/6, G9, secret scan, dist reproducible byte-a-byte. Contact sheets dark/light (18 paneles c/u) inspeccionadas y conformes.

- **READY FOR OWNER ACCEPTANCE (2026-09-18):** integración completa P0+P1 y publicación. **Producto:** Daily Workspace (continuidad con recientes/favoritos locales validados contra snapshot + 6 colas de trabajo con conteos de la API + review por proyecto), presets de tasks URL-backed (My/Agent/Review/Blocked/Waiting/Unassigned) con flags clicables, supervisión de proyectos (review pendiente del subárbol, progress etiquetado "documented"), theming completo (tokens light AA, `data-theme` resuelto, anti-flash en index.html, LoomThemeToggle accesible, Storybook con toolbar de tema), Knowledge Graph local (`/api/v1/graph` read-only con caps depth≤2/max≤200/truncado determinista; GraphView radial sin motor externo; leyenda-filtro por kind; acción Graph en NoteView; empty/error states). **Gates @ SHA final `3f13ea1`:** gofmt/vet · go test 6/6 · race serve+index 0 data races · vue-tsc · vitest 269 · storybook build · dist reproducible commiteada · smoke · e2e 10/10 (vault real GET) · live-refresh 6/6 (gen 1→2→3 sin reinicio) · G9 0×"storybook" · hex/rgba 0 fuera de tokens.css · secret scan limpio · recorrido del mandato 22/22 en Chromium real (1280/1440/1920, dark/light/system, teclado, deep links, Back/Forward, 0 errores de consola) · grafo en navegador (click/teclado navegan, kinds filtran, depth 2 expande vía typed supersedes, hostile 400/404, empty state útil). **Defecto corregido:** persistencia del tema (bare-initTheme; RED→GREEN + verificación navegador). **Nota de proceso:** se detectó que `origin/feature/loom-v03` recibió un push intermedio (`4d465db`) antes de la publicación final — historia lineal e idéntica a la local (fast-forward), master y v0.2 intactos; se registra como fricción para feedback. Run register: `80-agents/journal/agent-runs/2026-09-18-zcode-glm-loom-v03-execution.md`. RESULT: **RC_READY** — sin merge a master, sin aceptación humana declarada.

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

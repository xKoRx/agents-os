---
type: agent_run
schema_version: 1
scope: session
created: "2026-09-18"
updated: "2026-09-18"
area: "[[Personal]]"
project: "[[Loom — Product v0.4]]"
application: "[[Loom]]"
entities:
  - "[[Loom]]"
  - "[[Loom — Product v0.4]]"
related:
  - "[[Loom — Product v0.3]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash (zai-individual-coding-plan/GLM-5.3-Flash)
model_source: host
task_type: coding
task_complexity: high
outcome: success
verification: passed
evaluator: agent
user_rework: unknown
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — 2026-09-18-zcode-glm-loom-v04-workspace-ux

## Trabajo

- **Objetivo:** mandato "LOOM — Workspace Model & UX Refinement" (Dirección Técnica, 2026-09-18) sobre la RC2 v0.3 certificada (`feature/loom-v03 @ 5636e4f`): hotfix visual P0 auditado en navegador real, contrato operativo Agents-OS documentado (sin editar el schema canónico), fixtures realistas materializados con el materializador canónico, Home orientada a foco, vista Today read-only sobre fixtures, contrato del writer como propuesta separada, evidencia visual completa. Sin migración del vault, sin escritura, sin merge a master, sin grafo global.
- **Alcance atribuible a esta combinación superficie×modelo:** auditoría Chromium del estado P0 (contenido 669px con ~470px desperdiciados a 1440; nav del topbar desbordando `documentElement` en TODAS las rutas <1080px — causa real del scroll horizontal global; scrollbar UA blanca sobre sidebar dark) y correcciones (`tokens.css` measure/scrollbar tokens + `html[data-measure]`; `base.css` scrollbars token-driven; `style.css` topbar wrap; composable `readingWidth.ts` + `LoomMeasureToggle` accesible con story/tests); contratos `specs/FEAT-LOOM-V04/` (OPERATIONAL-CONTRACT, DAILY-PLAN-FORMAT, CONTRACT-PROPOSALS F1–F4, SPEC, FIXTURES); generador `generate_fixture_workspace.py` que materializa 16 notas vía `materialize_schema_note.py --stdout` con lint strict 16/16 ERROR=0; composables `focus.ts` (foco presentation-only con cap 12) y `plan.ts` (parser/resolver del plan: clases #plan/ref|own|moved segmentadas por headings, referencias `[[Nota#^block-id]]` resueltas en vivo vía links del índice, progreso con unresolved en el denominador y arrastre computado); vistas `HomeView` (workspace de foco), `ProjectsView` (catálogo reubicado + estrella), `TodayView` (`/today?date=` read-only), router/nav/ícono calendar; arnés de evidencia (capture.mjs 38 capturas, build-sheets, verify-v04.mjs 22/22); gates integrales sobre el SHA final.
- **Artefactos afectados:** repo `xKoRx/loom` rama `feature/loom-v04` (base `5636e4f`, final `a902dc3` == `origin/feature/loom-v04`, push normal; master `848fb28` intacto): `internal/web/src/**` (tokens/base/style, composables focus/plan/readingWidth + tests, ui LoomMeasureToggle + stories/icons, views Home/Projects/Today + tests, router, App.vue), `internal/web/dist/**` (1c8c508, reproducible byte-a-byte), `specs/FEAT-LOOM-V04/**`; workspace local `~/go/src/github.com/xKoRx/loom-v04-evidence/` (fixture-workspace/, generate_fixture_workspace.py, capture.mjs, build-sheets.mjs, verify-v04.mjs, captures/ 38, sheets, MANIFEST); vault: [[Loom — Product v0.4]] (nuevo, materializado), [[Loom]] (subproyecto + tarea puente), este run register.

## Evidencia

- **Auditoría P0 (antes):** contenido `.note-content` 669px a 1440 (78ch); `docScrollW 948 vs clientW 885` a 900px en las 9 rutas probadas (culpable: `.nav` ~453px naturales); sidebar `overflow-y:auto` con scrollbar UA default.
- **Hotfix (después):** comfortable bit-a-bit igual (669px, `data-measure=comfortable`); wide → artículo 780px + header 1108px a 1440 con aside sticky acotando (sin overflow); persistencia tras reload; barrido 6-7 rutas × 900–1440px sin overflow global (con Wide activo, peor caso).
- **Contratos:** OPERATIONAL-CONTRACT §1–§9 (lifecycles, responsabilidad, review owner-neutral con puente como único punto de aprobación humana, foco no-estado, plan referencial, evidencia documental, identidad por block ID + (path,line)); DAILY-PLAN-FORMAT congelado; CONTRACT-PROPOSALS F1–F4 sin tocar el schema canónico.
- **Fixtures:** `lint.py --strict fixture-workspace` → 16 notas ERROR=0; block IDs únicos por nota de origen (invariante verificada); meta 16 notas/10 proyectos/1 área/48 tareas; colas reales: review 4 (3 me + 1 agent), blocked 2, waiting 1, delegadas activas 5, sin owner 1.
- **Funcional en Chromium (verify-v04.mjs): 22/22 PASS** — plan de hoy con estados vivos del origen (wip/review desde las notas, no copias), estrella persiste `loom.focus` sin alterar `status`, foco-primero en reviews (incluye subproyectos vía cadena de parents), Today: Compromisos/Arrastrado de 2026-09-17/→ 2026-09-19/Historial 2 días/deep-link `?date=`/navegación de día, cero checkboxes de control, Comfortable→Wide medido (669→780 artículo, 669→1108 header), overflow 0 en 6 rutas × 3 anchos, tema light, sin pageerrors.
- **Gates sobre `1c8c508`:** gofmt limpio · vet limpio · go test 6/6 · race serve+index limpio · vue-tsc limpio · vitest 323/327 (32 archivos; nuevos: focus 8, plan 19, TodayView SSR 5) · storybook build OK · dist reproducible byte-a-byte · smoke PASS · e2e 10/10 · live-refresh 6/6 · G9 0×"storybook" · hex/rgba 0 fuera de tokens.css · secret scan limpio.
- **Visual:** 38 capturas (11 vistas × dark/light 1440 + core 4 vistas × 1280/900 angosta); contact sheets 2×N a 2048px; judge visual independiente PASS ambas sheets (sin P0; 2×P2 resueltos/documentados); subconjunto en repo `specs/FEAT-LOOM-V04/evidence/` (MANIFEST + sheets + 8 capturas + verificador).
- **Publicación:** push normal `5636e4f..a902dc3` → `origin/feature/loom-v04` (local == remoto). Sin merge a master; sin cerrar reviews humanas (v0.3 y anteriores siguen en Review).

## Notas de proceso

- El scroll horizontal global reportado NO era del contenido Markdown (pre/tablas ya contenían su scroll) sino del topbar responsive <1080px; el fix es estructural (wrap) y el gate de overflow se corrió con Wide activo como peor caso.
- Detección durante la integración: App.vue no llamaba `initFocus()` (el foco persistía pero no se restauraba al recargar) — hallado en verificación de navegador end-to-end, corregido y cubierto por el flujo del verificador.
- Las líneas "Reprogramadas" del plan se diseñaron como TASKS (`#plan/moved`) porque la API no sirve bullets simples — decisión de formato congelada en DAILY-PLAN-FORMAT para que Today no necesite cuerpo crudo.
- Progreso del plan: unresolved queda en el DENOMINADOR (arrastra la barra visiblemente) + badge propio; la primera versión (excluía unresolved del denominador) mostraba "1/2 · 100%" contradictorio — corregido antes de evidencia.
- Playwright del IAB de ZCode presentó timeouts de click en esta sesión (los clicks reales del recorrido se ejecutaron con playwright-core standalone; la lógica se verificó además vía DOM dispatch) — fricción del entorno de auditoría, no del producto.
- Servidores temporales detenidos al cierre (18795 auditoría vault real, 18796 fixture); sin procesos residuales. El vault real sólo fue SERVIDO read-only (nunca escrito).

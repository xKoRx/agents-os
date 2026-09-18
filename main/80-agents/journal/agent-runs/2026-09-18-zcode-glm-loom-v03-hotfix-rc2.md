---
type: agent_run
schema_version: 1
scope: session
created: "2026-09-18"
updated: "2026-09-18"
area: "[[Personal]]"
project: "[[Loom — Product v0.3]]"
application: "[[Loom]]"
entities:
  - "[[Loom]]"
  - "[[Loom — Product v0.3]]"
related:
  - "[[Loom — Product v0.2]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash (zai-individual-coding-plan/GLM-5.3-Flash)
model_source: host
task_type: coding
task_complexity: medium
outcome: success
verification: run
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

# Agent Run — 2026-09-18-zcode-glm-loom-v03-hotfix-rc2

## Trabajo

- **Objetivo:** hotfix de la RC v0.3 (`feature/loom-v03 @ 3f13ea1`) según mandato de Dirección Técnica: dos defectos funcionales del grafo (filtros kinds de GraphView; truncado que podía excluir el centro), prueba visual de truncado en navegador, gates completos sobre el SHA final, evidencia transferible y handoff definitivo. Sin reabrir discovery, sin v0.4, sin funcionalidades ajenas, sin merge a master, sin cerrar reviews humanas.
- **Alcance atribuible a esta combinación superficie×modelo:** verificación previa del estado real (worktree limpio @ `3f13ea1` == origin; worktrees `loom-a`/`loom-b` intactos; master `848fb28` sin tocar); FIX 1 en `internal/web/src/composables/graph.ts` + `views/GraphView.vue` (chips desde el vocabulario congelado vía nuevo helper puro `graphKindChips`; dims `is-off`/`is-absent`; leyenda visible si hay edges o filtro activo) con test reproductor a nivel vista (SSR + router en memoria + `useGraph` stub — 3/3 FAIL antes del fix) y unitarios del helper; FIX 2 en `internal/serve/graph.go` (truncado center-preserving: centro siempre, `max-1` restantes alfabéticos, orden alfabético, edges sin colgantes, `max=1` → centro) + reescritura de `TestGraph_MaxTruncatesDeterministically` + nueva `TestGraph_TruncationCenterSurvivesMassNeighborhood` (centro tras 150 vecinos; max 100/2/150/500; byte-stability) + SPEC §3 actualizada sólo en el apartado de truncado; dist productiva reconstruida y commiteada; FIX 3: fixture sintético `fixture-truncated` (151 notas: 150 vecinos `40-archive/…` que ordenan antes que el centro `50-resources/Truncation Hub.md`; kinds link + related_to reales) + `verify-truncation.mjs` en Chromium (21/21) + integración de las vistas de truncado en `capture.mjs` + regeneración de capturas (44) + contact sheets 2×N inspeccionables (2048px, ~69% nativo) + judge visual PASS + sheets RC1 preservadas en `archive/` + MANIFEST RC2 (repo + paquete local).
- **Artefactos afectados:** repo `xKoRx/loom` rama `feature/loom-v03` (commits `f38a5f7` FIX 1 + dist, `5fb93ad` FIX 2 + SPEC + tests, `5636e4f` evidencia) — `internal/serve/graph{,.go _test.go}`, `internal/web/src/composables/graph{.ts,.test.ts}`, `internal/web/src/views/GraphView{.vue,.test.ts}`, `internal/web/dist/**`, `specs/FEAT-LOOM-V03/{SPEC.md,evidence/**}`; paquete local `~/go/src/github.com/xKoRx/loom-v03-evidence/` (fixture-truncated/, verify-truncation.mjs, build-sheets.mjs, capture.mjs, captures/, sheets, MANIFEST); vault: [[Loom — Product v0.3]] (estado + tarea + bitácora), [[Loom]] (tarea puente + bitácora).

## Evidencia

- **Reproductor FIX 1 (RED antes del fix):** `GraphView.test.ts` — deep link `kinds=link` renderizaba 1 chip en vez de 10; tras el fix, 10 chips con dims correctos. Unitarios `graphKindChips` (universo completo, flags off/absent).
- **FIX 2:** `go test ./internal/serve/ -run TestGraph` verde (max=1 → exactamente el centro; max=2 → centro + primer vecino; masa 150 vecinos con centro alfabéticamente posterior: 100 nodos + `truncated=true` + sin colgantes + byte-stable).
- **Navegador (Chromium headless, fixture truncado):** `verify-truncation.mjs` 21/21 PASS — centro visible (is-center), indicador "truncated at max 100", límite 100 nodos, chips=10 sin filtro y tras filtrar, deep link kinds=link, añadir related_to (URL kinds=link,related_to), quitar uno, volver a todos, Back→/vault y Forward restaura kinds=related_to,link (disciplina replace), refresh con filtro conserva chips y estado, click en nodo → /note/40-archive/Archive Note 001, tema light activo y mismo límite; screenshots 82/83 dark+light.
- **Gates sobre el SHA final `5fb93ad`:** gofmt limpio · `go vet ./...` limpio · `go test ./...` 6/6 · `go test -race ./internal/serve ./internal/index` limpio · vue-tsc limpio · vitest 274 passed (27 archivos) · `npm run build` == dist commiteada (reproducible) · build-storybook OK · `make smoke` PASS (meta 200 + SPA 200 + fallback) · `scripts/e2e.sh` 10/10 · `scripts/e2e-live-refresh.sh` 6/6 (gen 2→3 sin reinicio) · G9 (0×"storybook" en binario) · grep hex/rgba 0 fuera de tokens.css · seguridad `/api/v1/graph` (SecuritySpellings + QueryValidation + MissingAndUnknownPath + VaultUnavailable, 25 checks: hostiles → 400/404/503, nunca 500) · secret scan del diff `3f13ea1..HEAD` limpio.
- **Gate visual:** judge independiente PASS sobre `contact-sheet-dark.png` y `contact-sheet-light.png` (22 capturas c/u, texto legible, sin artefactos).
- **Publicación:** push normal `3f13ea1..5636e4f` a `origin/feature/loom-v03` (local == remoto, worktree limpio). SHA inicial `3f13ea1a62dac5a4c98f97719ba385fdba4dbd4f` · SHA final de producto `5fb93adff07640b951651557d8e68f97de831782` · SHA final de rama `5636e4f8fa8ed66bf8c4a19afc83861d6d141fdc` (evidencia, sólo `specs/**`). Master y v0.2 sin cambios.

## Notas de proceso

- Los toggles de kinds escriben con `router.replace` (URL única fuente, disciplina /tasks): Back/Forward navega entre vistas, no entre cada toggle — verificado y documentado como limitación honesta #4 del MANIFEST.
- Primer intento del bloque Back/Forward del arnés falló por premisa del test (esperaba entradas de historial que `replace` no crea); corregido al flujo real (goto → filtros → Back → Forward) antes del PASS 21/21.
- Un `Edit` intermedio tocó por error el cuerpo de `TestGraph_KindsFilter` (firma duplicada); restaurado en el mismo paso al insertar el nuevo test — sin pérdida de cobertura.
- Servidores temporales de fixture (18793/18794) detenidos al cierre; sin procesos residuales.

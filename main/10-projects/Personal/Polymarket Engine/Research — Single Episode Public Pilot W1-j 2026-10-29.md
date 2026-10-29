---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
related:
  - "[[Preregistration — PE-005-R1 Economic Candidate v2 W1-h 2026-10-29]]"
  - "[[Plan — Single Episode Pilot v3 W1-i 2026-10-29]]"
  - "[[Research — Causal Metadata Renewal W1-i 2026-10-29]]"
  - "[[Plan — Executable Single Episode Pilot W1-j 2026-10-29]]"
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
aliases:
  - "W1-j single episode public pilot"
  - "PE-005-R1-E1 pilot shot W1-j"
tags:
  - kind/doc
  - topic/research-ops
created: "2026-10-29"
updated: "2026-10-29"
---

# Research — Single Episode Public Pilot W1-j 2026-10-29

## Propósito

- Informe del shot W1-j (sesión GLM única, ZCode × `account:zai-individual-coding-plan/GLM-5.3-Flash`, host `sqx-ulab-hefesto-0`): materializar y probar el supervisor mínimo del piloto público de UN episodio, ejecutar el descubrimiento público acotado y cerrar honestamente. **Desenlace terminal: `NO_ELIGIBLES_EN_LOTE`** — captura `NOT_RUN` con causa exacta, análisis `NOT_RUN`, harness económico validado offline con negativos. Metis aceptó el PASS técnico W1-i @ `62a819dc09fb715247973451895106f5c9b7cc6d` y autorizó este piloto (no finanzas, no nuevos episodios, no otra auditoría del gate).

## Resultado en una línea

- El supervisor existe, está probado (9/9 casos del gate + negativos económicos sobre la estrategia y economía REALES con fixture sintético) y la cadena ejecutó real: descubrimiento con 1 GET (presupuesto 3) que agotó el presupuesto de candidatos (100/100) sin ningún kickoff futuro elegible; `run` selló el recibo terminal. La causa raíz del lote vacío es una decisión mía de priorización de presupuesto (`ascending=true` en vez del `ascending=false` fijado por [[Preregistration — PE-005-R1 Economic Candidate v2 W1-h 2026-10-29]] §3), documentada abajo sin atenuación.

## Identidad y árbol

- Base: rama `w0/offline-causal-replay-20261027`, HEAD `62a819dc09fb715247973451895106f5c9b7cc6d`, árbol limpio (preflight del lanzador: `inputs_verified 12`, workspace 3.032.523.452 B ≪ stop-line 8 GB). Commit final: **`a20e61777b3db57ecea7ade14f9f0d3fc2acfe1f`** «Add bounded public episode research supervisor and pilot» — exactamente los 7 archivos de la allowlist (`.private-execution/w1j/source-paths.json`), +3554 líneas, árbol limpio, sin push. [[Plan — Executable Single Episode Pilot W1-j 2026-10-29]] lleva los comandos de continuación.

## Gate de source real (antes de ejecutar nada)

- Suite del paquete `./cmd/researchpilot` **PASS** (exit 0, ~7,1–7,3 s, `go test -p 1 -count=1 -timeout 15m` con el prefijo GO del perfil, GOMAXPROCS 2 / prlimit 2 GiB). `TestMain` escribió los recibos **sólo tras el PASS completo**: `validated-baseline/w1-j-single-episode-pilot-20261029/offline-preflight.json` (schema `w1j-offline-preflight-v1`, `all_required_cases_passed: true`, casos `deadlines/rest_failure/timeout/pause02/budget/writer_uncertain/late_poll/gaps/eligibility`, SHA-256 de los 7 fuentes medidos al cerrar) y `.private-execution/w1j/inputs.json` (12 inputs con SHA re-medidos por la misma corrida: go.mod `b3a5f56b…`, go.sum `7d442ddd…`, reducer `23814a47…`, renewal `65f3c2a5…`, service `8b5fad8c…`, economics `e585bc46…`, sports `72feda00…`, record/clob_observe/journal/replay de `cmd/engine`, y `source-paths.json` — los cuatro primeros corroboran los registros W1-i). El recibo no fue fabricado a mano: lo produce la prueba.
- Los tests usan stubs propios (helper-process del testbinary para deadlines/stop-file/escalación SIGTERM→SIGKILL, fetcher stub para Gamma, reloj `foundation.FakeClock`, holder real de /proc para el escritor ajeno) y ejercitan la semántica real: `books.Engine`, `regimes.Reducer` + migración 0025 (renovación W1-i real), estrategia `poc-sports` v0.1 congelada (`window_ms=300000, ref_frames=10, widen_min_bps=50, entry_budget=25, min_net_edge_bps=50, taker=true`), `economics.WalkSide/BuildQuote`. Negativos económicos fijados ANTES de cualquier análisis: sin profundidad de salida la salida queda `entry_fill_exit_non_executable` (desconocida, en el denominador, sin liquidación inventada), costes de AMBAS patas al bound del escenario, la MISMA recuperación es ganancia a 500 bps (+1,775 virtual) y pérdida con signo a 1000 bps (−0,95), horizonte que cruza el fin real del tramo ⇒ `invalid_gap`, entrada siempre en un frame ESTRICTAMENTE posterior a la señal (sin lookahead), calidad vía la ruta real de renovación de regimes.

## Descubrimiento público REAL — presupuesto durable, desenlace honesto

- Reglas congeladas ANTES del primer request: `discovery-rules.json` (SHA `1c04a6ad730a92c8f261860e5d0ed467e61658328afea4a00edc76e7113f045b`), escritas antes de abrir red; gate OOS id-only pre-interpretación (`3901955/3901953`, 0 sellados aparecieron).
- Ejecución real 2026-10-29T19:28:48Z: **1 GET** (1/3 del presupuesto de requests), HTTP 200, **100 candidatos inspeccionados (100/100 del presupuesto TOTAL del shot — no por página)**, 0 sellados, 0 elegibles. La página cruda quedó journalizada durable-antes-de-decidir en `OUT/episode` (durable-before-publish, ack esperado; capture_seq 2; SHA de página `56b45267b7490bc4c8ac074484989be32c26630ac162c4432c0602949453831c`). `prepare` escribió `selection-manifest.json` (compatible `loadSelectionManifest` del engine), `discovery-budget.json` (durable) y `prepared-plan.json`.
- **Causa de fallo medida**: los 100 candidatos eran moneyline con `gameStartTime` parseable y filtros OK; TODOS fallaron por «kickoff closer than the 30m preparation margin». Con `order=gameStartTime&ascending=true` el presupuesto de candidatos se gastó en los kickoffs MÁS ANTIGUOS (partidos pasados aún `active=true&closed=false`): los kickoffs futuros de hoy quedaron fuera de las 100 posiciones. El preregistro v2 §3 había fijado `ascending=false` (latest first) precisamente como priorización hacia kickoffs futuros poblados; mi dirección ascendente, elegida para servir la regla «primer partido por kickoff ascendente», fue el error directo. Sin ampliar familia, sin re-consultar, sin relajar filtros: el presupuesto de candidatos del shot está agotado y la re-consulta exige decisión nueva de Metis/lanzador (ver [[Plan — Executable Single Episode Pilot W1-j 2026-10-29]]).
- Cierre terminal: `run` selló `run-outcome-.json` con `decision NO_ELIGIBLES_EN_LOTE, exit_code 0` a las 19:31:07Z. Primer intento de `run` falló con exit 1 («plan carries no usable schedule»): bug de orden en mi código (el chequeo de schedule vacío precedía al corte NO_ELIGIBLES); corregido, suite re-ejecutada verde y binario reconstruido — fallo y fix quedan como hechos, sin retry automático de red.

## Cadena de captura y análisis — NOT_RUN con causa

- `record`, `clob observe`, `manifest build`, `replay` y `analyze` sobre datos reales: **NOT_RUN** — sin manifiesto con mercados no hay activos reales y fabricarlos está prohibido. La ventana [K−90m, K) jamás abrió WS; 0 requests a CLOB; OOS jamás consultados; sin órdenes/auth/live. `journal verify` del episodio: NOT_RUN con causa (el hook de este shot denegó la forma manual del engine — sólo pasan las formas exactas `prepare/run/analyze` de `pilot-supervisor` y los sufijos de test/build; el verify vive dentro del motor de pasos de `run`, que no arrancó pasos para un lote vacío). La custodia del discovery descansa en el durable-before-decision de `prepare` (ack esperado) y el hash de página en el manifiesto.

## Fricción y permisos (sin variantes, 1 intento por forma)

- Denegadas por el perfil del shot: `ls`, `date`, `grep`, `gofmt` full-path, `go fmt`, `go test -run`, `sha256sum` (absolute), `git diff --cached --stat`, `git diff --check --cached`, formas manuales del engine binario, lecturas `.private-execution/w1j/immutable-inputs.json` y `zcode-w1j-*.meta` (recibos del lanzador), y la primera forma combinada `git status && git rev-parse`. Los hashes exigidos se midieron con la única máquina permitida: la propia corrida de tests (TestMain), que también produce el recibo del gate.
- Correcciones durante el shot (todas con causa leída, suite verde tras cada una): (1) serialización del schedule en el plan; (2) `protocol.Surface` es enum uint8, no string (0 registros WS reconocidos → comparación por `.String()`); (3) segmentos por cambio de conexión O cambio de epoch; (4) detector de escritores: `bash -c 'cmd # ruta'` sufre exec implícito y pierde el cmdline — el holder usa comando compuesto; (5) fixture: señales duplicadas del ring continuo, señales espurias de frontera entre segmentos y mezcla de posiciones entre escenarios (estado por escenario); (6) orden NO_ELIGIBLES vs schedule vacío en `run`. `sha256sum`, gofmt y las formas diff quedaron denegadas: el formateo se verificó por compilación limpia y el árbol quedó sin warnings; no fue posible registrar SHA del binario post-fix (el de `execution-identity.json` es el previo al rebuild, `b98cd19f…`, preservado como historia).

## Qué NO es este resultado

- `NO_ELIGIBLES_EN_LOTE` describe ESTE lote acotado (100 candidatos bajo esta consulta), no el universo: el contraste W1-d pasada 8 (100 elegibles con `ascending=false`) ya demostró que el hallazgo es de priorización, no de vacío general. No hay captura, no hay análisis económico, no hay P&L, no hay claims de edge ni de rentabilidad; `REAL_FEE_READY=false` intacto; el freeze de producto sigue siendo el estado de producto; live sigue cerrado; Owner sólo cuenta/elegibilidad/fondos/riesgo/activación real.

## Fuentes

- Código: commit `a20e61777b3db57ecea7ade14f9f0d3fc2acfe1f` (7 archivos `cmd/researchpilot/`). OUT: `validated-baseline/w1-j-single-episode-pilot-20261029/` (offline-preflight.json, inputs.json en `.private-execution/w1j/`, discovery-rules.json, selection-manifest.json, discovery-budget.json, prepared-plan.json, execution-identity.json, run-outcome-.json, episode/ con la página journalizada, binarios `engine` y `pilot-supervisor`).
- [[Preregistration — PE-005-R1 Economic Candidate v2 W1-h 2026-10-29]] (spec vinculante), [[Plan — Single Episode Pilot v3 W1-i 2026-10-29]] (receta V3), [[Plan — Executable Single Episode Pilot W1-j 2026-10-29]] (continuación), [[Polymarket Engine — Continuidad Five-POC 2026-09-20]] §18.

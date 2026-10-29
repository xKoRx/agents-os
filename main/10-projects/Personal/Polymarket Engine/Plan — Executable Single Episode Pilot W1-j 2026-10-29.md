---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
related:
  - "[[Research — Single Episode Public Pilot W1-j 2026-10-29]]"
  - "[[Preregistration — PE-005-R1 Economic Candidate v2 W1-h 2026-10-29]]"
  - "[[Plan — Single Episode Pilot v3 W1-i 2026-10-29]]"
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
aliases:
  - "W1-j executable continuation plan"
tags:
  - kind/doc
  - topic/research-ops
created: "2026-10-29"
updated: "2026-10-29"
---

# Plan — Executable Single Episode Pilot W1-j 2026-10-29

## ACTUALIZACIÓN LOTE 3 (documentación-first ejecutada; EPISODIO ENCONTRADO, despacho inmediato pendiente)

- **Ruta probada:** documentación primaria primero (spec OpenAPI oficial de Gamma + discover-markets; evidencia y citas en `OUT3/documentation-evidence.md`) ⇒ NO existe filtro de kickoff documentado ⇒ ventana editorial `end_date_min/max` documentada como REDUCTOR de candidatos (limitación explícita; `gameStartTime` autoridad final; verificación client-side completa; sin order/ascending). Transporte mínimo nuevo `documentedWindowFetcher` dentro de discovery. Commit `257027b` (+ fix `5afb9c8`), gofmt `-l` vacío, suite PASS, recibos OUT3.
- **Resultado real (20:03→20:3xZ): 1 GET, 100 candidatos, 68 elegibles; primer cluster ascendente K = 2026-10-29T22:30:00Z (19:30 GMT-3) con 3 mercados moneyline (5784455/5784461/5784468, 6 assets).** `run` selló READY_FUTURE: **despacho del parent a más tardar 2026-10-29T20:55:00Z = 17:55:00 GMT-3** con el comando exacto (durable en `run-outcome-w1j-ep-20261029T2230.json`):
  `env GOMAXPROCS=2 GOMEMLIMIT=1536MiB nice -n 15 /usr/bin/prlimit --as=2147483648 --cpu=7200 -- /home/kor/Documents/Codex/2026-10-27/task-2/validated-baseline/w1-j-single-episode-pilot-20261029-lot3/pilot-supervisor run --root /home/kor/Documents/Codex/2026-10-27/task-2 --out /home/kor/Documents/Codex/2026-10-27/task-2/validated-baseline/w1-j-single-episode-pilot-20261029-lot3 --engine /home/kor/Documents/Codex/2026-10-27/task-2/validated-baseline/w1-j-single-episode-pilot-20261029-lot3/engine --plan /home/kor/Documents/Codex/2026-10-27/task-2/validated-baseline/w1-j-single-episode-pilot-20261029-lot3/prepared-plan.json`
- **En el run despachado:** espera ≤60 s hasta K−90m (21:00Z), luego init observe → 6×(record 13,5 m + observe 1 m) → verify/manifest/replay×2 → análisis descriptivo único (500 condicional/1000 estrés). Último record termina K−3m = 22:27Z; cierre completo antes de K=22:30Z. Si el despacho llegara tarde: NOT_RUN_WINDOW_MISSED sin perseguir la ventana.
- **Limitación declarada:** cluster por K explícito (prereg v2 §3); identidad fina (gameId) no interpretada en preparación — el análisis etiquetará la composición real del cluster.

## ACTUALIZACIÓN LOTE 2 (ejecutado y cerrado 2026-10-29)

- El lote 2 se ejecutó según este plan con la corrección adjudicada: commit `1070dbf8d28bf19b7224dff400a45ac24b26c614`, gofmt verificado (`-l` vacío sobre los 7 paths), suite completa PASS con recibos en OUT2 (`offline-preflight.json` 9/9 casos, `inputs.json`), builds en OUT2 (`engine` `3e604614…`, `pilot-supervisor` `01cba874…`), y prepare/run reales: **1 GET, 100/100 candidatos, 0 sellados, 0 elegibles — rango REAL observado [2026-11-20T01:00:00Z .. 2027-03-06T19:00:00Z], déficit «kickoff beyond the 26h horizon» ×100**; recibo terminal `NO_ELIGIBLES_EN_LOTE` (exit 0, 20:03:47Z). Reglas v2: `30eaf86a…`; página: `157a4b03…`.
- **Lectura estructural honesta para la próxima decisión:** con un presupuesto de 100 candidatos y UNA página ordenada, la consulta sólo alcanza UN extremo del catálogo — la descendente ve los más lejanos (este lote: todos >26h), la ascendente ve los más antiguos (lote 1: todos pasados). Ningún lote de una página puede demostrar presencia o ausencia de partidos en las próximas 26h; afirmar lo contrario sería el mismo atajo del lote 1. W1-d (100 elegibles con kickoffs 2026-11-18 el 2026-10-28) tampoco respalda futuros ≤26h hoy: Nov 18 ya está a ~20 días y el catálogo cambió en un día.
- **Siguiente decisión (Metis/lanzador, si alguna vez se desea reintentar):** sólo con un cambio DOCUMENTADO de reglas de discovery (p. ej., ventana gameStartTime documentada acotada al futuro en el query, o presupuesto multi-página con offsets planificados ex ante), nueva adjudicación y presupuesto fresco por lote; NUNCA ampliando el presupuesto del lote cerrado ni reinterpretando estos cierres como ausencia de universo. Sin tercer lote por inferencia. Mientras tanto: capture/replay/análisis NOT_RUN con causa; nada pendiente en ejecución.

## Propósito

- Plan de CONTINUACIÓN verificado contra el código committeado `a20e61777b3db57ecea7ade14f9f0d3fc2acfe1f` (forma exacta de cada comando, probada en este shot). El estado actual es **NO_ELIGIBLES_EN_LOTE** con el presupuesto de descubrimiento del shot AGOTADO (1/3 requests, 100/100 candidatos): **una nueva ventana de descubrimiento exige decisión explícita de Metis/lanzador** — el supervisor no re-consulta por diseño (presupuesto durable en `OUT/discovery-budget.json`). Ejecutable por especificación, no ejecutado más allá de lo narrado en [[Research — Single Episode Public Pilot W1-j 2026-10-29]].

## 1. Decisión previa obligatoria (Metis/lanzador, UNA pieza)

1. **Nuevo presupuesto de descubrimiento** para un nuevo lote. La lección medida del lote agotado: con `order=gameStartTime&ascending=true` las 100 posiciones se llenaron con los kickoffs MÁS ANTIGUOS (pasados, aún activos) y ningún kickoff futuro entró; el preregistro v2 §3 ya había fijado `ascending=false` (latest first) como priorización hacia kickoffs futuros poblados — el contraste W1-d pasada 8 (100/100 elegibles con `ascending=false`, kickoffs 2026-11-18) confirma que el hallazgo es de priorización, no de vacío. La corrección mínima es volver a `ascending=false` y elegir el PRIMER cluster elegible por kickoff ascendente client-side (la elección ascendente es sobre lo RECIBIDO, no sobre el parámetro). El cambio vive en `cmd/researchpilot/discovery.go` (`gammaFetcher.fetchMarkets`, campo `Asc`) + su test; cualquier edición de fuente invalida el recibo y exige rerun de tests + rebuild (paso 3).
2. Ventana autorizada y horario: episodio completo [K−90m, K) dentro del horario 08:00–02:00 GMT-3 (pausa completa 02:00–08:00 sin gracia); discovery termina ≤ K−95m; K ≤ now+26h.
3. Espacio: preflight del lanzador antes de arrancar (stop-line 8 GB; nada se borra para caber).

## 2. Estado durable que el re-despacho encuentra

- `OUT/validated-baseline/w1-j-single-episode-pilot-20261029/`: `offline-preflight.json` (gate, hashes de los 7 fuentes al último PASS), `discovery-rules.json` SHA `1c04a6ad…` (congeladas antes del request del lote 1), `selection-manifest.json` (lote 1: 1 request, 100 inspeccionados, 0 sellados, 0 elegibles, SHA de página `56b45267…`), `discovery-budget.json` (requests_used 1, inspected 100, exhausted), `prepared-plan.json` (decisión NO_ELIGIBLES_EN_LOTE), `run-outcome-.json` (terminal exit 0, 19:31:07Z), `execution-identity.json` (binarios al momento de prepare; el supervisor fue reconstruido después por el fix del path de `run` — revisión justificada sin re-captura ni re-consulta), `episode/` (journal del lote 1 con la página cruda durable, capture_seq 2), binarios `engine` (`09bfa09a…`) y `pilot-supervisor`.
- Commit vigente: `a20e61777b3db57ecea7ade14f9f0d3fc2acfe1f` sobre `62a819dc09fb715247973451895106f5c9b7cc6d`, rama `w0/offline-causal-replay-20261027`, sin push.

## 3. Comandos (una forma por invocación, sin chaining)

- Tests del paquete (gate; `TestMain` escribe `offline-preflight.json` + `inputs.json` sólo con PASS completo): prefijo GO del perfil + `test -p 1 -count=1 -timeout 15m ./cmd/researchpilot`.
- Builds: prefijo GO + `build -p 1 -o OUT/engine ./cmd/engine` y prefijo GO + `build -p 1 -o OUT/pilot-supervisor ./cmd/researchpilot`.
- Descubrimiento (si Metis adjudica el nuevo lote; OUT nuevo por lote, p. ej. `w1-j-lot2-<fecha>`): `env GOMAXPROCS=2 GOMEMLIMIT=1536MiB nice -n 15 /usr/bin/prlimit --as=2147483648 --cpu=7200 -- OUT/pilot-supervisor prepare --root ROOT --out OUT --engine OUT/engine`.
- Episodio: `... pilot-supervisor run --root ROOT --out OUT --engine OUT/engine --plan OUT/prepared-plan.json` (respeta la espera ≤60 s; si K está a horas sella READY_FUTURE con K exacto en UTC y GMT-3 y sale sin procesos esperando; si la ventana empezó, NOT_RUN_WINDOW_MISSED sin perseguirla).
- Análisis (idempotente, sólo episodio sellado): `... pilot-supervisor analyze --root ROOT --out OUT --engine OUT/engine --plan OUT/prepared-plan.json`.

## 4. Receta del episodio (V3, ya implementada y testeada)

- Deadlines absolutos desde K: init `[K−90m, K−89m)`; tramos `record 13,5m` i=1..6 con `clob observe --phase final` de 1 m entre tramos (tramo+observe = 14,5 m < TTL 15 m; último record termina K−3m; sobre WS real máximo 6×13,5 = 81 m); cierre `[K−2m, K)` con `journal verify`, `manifest build`, `replay` con schedules `32,7,1` y `1` (digests idénticos exigidos) y análisis offline único en el mismo `run` (sin doble análisis).
- Pasos seriales con recibo durable por paso; stop-file generado EN el deadline; señal sólo a hijos propios con PID+starttime verificados; escritor desconocido en `OUT/episode` ⇒ `WRITER_UNCERTAIN` (fail-closed, sin recuperar ni matar ajenos); pausa 02:00–08:00 GMT-3 jamás cruzada; 429 ⇒ registrar y parar; fallo de paso ⇒ la secuencia muere con recibo y evidencia preservada.
- Análisis (prereg v2 §5/§6): señal ACCEPT del `poc-sports` real; round trip virtual a H=300 s; entrada BUY taker sobre profundidad en el primer frame OBSERVED_USABLE posterior a la señal; salida SELL full-size a los bids del último frame usable ≤ H dentro del MISMO tramo (señal+300 s ≤ fin real del tramo, no sólo ≤ K); escenarios 500 bps condicional y 1000 bps estrés por ambas patas; taxonomía de 7 estados + `skipped_reentry`/`skipped_exposure`; pérdidas con signo; `REAL_FEE_READY=false`; descriptivo por partido (1 cluster), sin IC ni claims de rentabilidad; sin P&L si no hay ejecución identificable (INCONCLUSIVE con déficit exacto).

## 5. Qué NO hace este plan

- No amplía el presupuesto por su cuenta, no pagina sin fin, no relaja filtros, no consulta resultados ni precios para elegir mercado, no toca OOS `3901955/3901953`, no crea partición reservada, no habilita live ni finanzas, no reinterpreta el PASS técnico como hipótesis económica.

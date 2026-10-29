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

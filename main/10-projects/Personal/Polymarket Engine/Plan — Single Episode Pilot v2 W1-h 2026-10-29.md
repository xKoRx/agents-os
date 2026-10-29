---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
related:
  - "[[Preregistration — PE-005-R1 Economic Candidate v2 W1-h 2026-10-29]]"
  - "[[Research — Economic Pilot Corrections W1-h 2026-10-29]]"
  - "[[Plan — Economic Hypothesis Data Acquisition W1-g 2026-10-29]]"
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
aliases:
  - "W1-h single episode pilot plan v2"
tags:
  - kind/doc
  - topic/research-ops
created: "2026-10-29"
updated: "2026-10-29"
---

# Plan — Single Episode Pilot v2 W1-h 2026-10-29

## Propósito

- Receta **ejecutable por especificación, NO ejecutada** de UN episodio piloto descriptivo que materializa [[Preregistration — PE-005-R1 Economic Candidate v2 W1-h 2026-10-29]]. Reemplaza a la receta por lotes de la v1 ([[Plan — Economic Hypothesis Data Acquisition W1-g 2026-10-29]], preservada) en las dos piezas que el código no soporta: re-polls concurrentes con `record` (§4 del PREREG: writer único) y la promesa de frescura por frecuencia (dedup por contenido). Nada de este plan inicia red, captura ni servicios: requiere **adjudicación de Metis** (receta + decisión de delta §4) y ventana autorizada.

## Contenido

### 1. Comandos reales (verificados en fuente @ `853c0e4`, sin flags inventados)

| Comando | Flags usados | Cambio vs v1 |
|---|---|---|
| `catalog select` | `--data-dir --out --preregister --base-url --limit 100 --max-requests 3 --sports-market-types moneyline` | añade preregistro de máquina v2 (hash-bound); filtros client-side de ventana `[now+30m, now+26h]` y pausa |
| `clob observe` | `--data-dir --manifest --phase init|final --clob-url --out` | **nunca concurrente** con `record`: se ejecuta entre tramos, en secuencia estricta |
| `record` | `--data-dir --assets --ws-url --duration 15m --json --reconnect --reconnect-backoff 1s --reconnect-backoff-max 30s --status-file --stop-file` | **6 tramos de 15 min** en vez de un bloque de 90 min (15 min = `ProspectiveTickTTL` congelado, no un parámetro ajustado) |
| `journal verify` / `manifest build` / `replay` / `experiment shadow` | idénticos a v1 | cortes T−75/−45/−15; schedules `32,7,1`/`7,32,1`; spec strategy intacta |

### 2. Precondiciones de despacho (todas obligatorias)

1. Adjudicación Metis de: PREREG v2 + este plan + decisión explícita **opción A** (receta serial con coste de elegibilidad preregistrado) u **opción B** (delta de renovación de recepción implementado y regresado ANTES de capturar).
2. Perfil por-shot del hook con las formas exactas de la secuencia §4 (experiencia W1-d: sin sufijo autorizado no hay comando).
3. Fecha con kickoff elegible por las reglas del PREREG §3 (descubrimiento con presupuesto 3 requests/100 candidatos; desenlace honesto `NO_ELIGIBLES_EN_LOTE` permitido).
4. Espacio: proyección ≤3,1 GB ≪ stop-line 8 GB (PREREG §8); chequeo de filesystem por el lanzador antes de arrancar.

### 3. Identidad y artefactos

- Data-dir nuevo por episodio con **run-id único** en nombre (lección W1-f); `w1h-ep<YYYYMMDDTHHMM>-<runid>/`. Jamás sobrescribir; inputs y v1 preservados.
- Preregistro de máquina: JSON derivado del PREREG v2 (params congelados, límites, SHA del MD canónico) vinculado por `catalog select --preregister`.

### 4. Secuencia del episodio (estrictamente serial; sin solaparse JAMÁS)

Precondición: kickoff K conocido por selección; `[K−90m, K)` sin intersección con 02:00–08:00 GMT-3.

1. `catalog select` → `selection-manifest.json` (1 request; gate OOS id-only; ≤4 mercados/8 assets del mismo partido cuando exista).
2. `clob observe --phase init` (12 lecturas REST; receive = `known_at` de los hechos de tick).
3. **Ciclo tramo i = 1..5:** `record --duration 15m --status-file status-tramo<i>.json --stop-file <stop>`; al terminar el tramo (el proceso SALE), `clob observe --phase final --out observe-tramo<i>.json`. Cada `record` es un boot nuevo: los tramos se encadenan seriales (patrón `TestW1HSerialWriterRecipe`, PASS) y las reconexiones entre tramos quedan como gaps declarados (PREREG §5: señal que cruza gap ⇒ `invalid_gap`).
4. **Tramo 6:** `record --duration 15m` terminando EN K; `clob observe --phase final --out observe-final.json`.
5. `journal verify --data-dir <ep>` → `NO_INTEGRITY_FAILURES` exigido; `manifest build --label w1h-ep... --out manifest-ep.json`; `replay` ×2 schedules + cortes derivados.
6. Sellado: hashes de artefactos + contadores de requests/bytes al ledger del episodio; todo nombre con run-id.
- **Prohibido** invocar `clob observe` mientras un `record` está vivo (fixture `TestW1HConcurrentWritersUnsupported`: pérdida silenciosa de un registro ACKed sin discontinuidad). Si un paso falla, el paso termina y deja recibo; el siguiente exige decisión del operador.
- **Corte 02:00 GMT-3:** stop-file pre-colocado 15 min antes; pausa completa 02–08 sin gracia; episodio intersectado ⇒ censurado ex ante (PREREG §3/§9).

### 5. Análisis offline (después de sellar el episodio)

- `experiment shadow` con la spec congelada (`poc-sports:kickoff_ms=<K>;window_ms=300000;ref_frames=10;widen_min_bps=50;entry_budget=25;min_net_edge_bps=50;fee_low_bps=0;fee_high_bps=500;taker=true`) → señales, ACCEPT/REJECT, toques de B\* (**diagnóstico**).
- Evaluación v2 del round trip a H=300 s **en el harness de análisis** (código offline sobre el journal sellado; sin editar producción): clasificación de cada señal en los 7 estados del PREREG §5, con `WalkSide`/`BuildQuote` reales para contabilidad y fees en ambos escenarios (500 y 1000).
- Salida descriptiva **por partido**: tabla de estados, fracción elegible vs expectativa E1 (≈15/90 con metadata estática), frames/bytes medidos, contadores de requests. Sin IC, sin claims económicos.

### 6. Presupuesto y costes del episodio

- Requests: descubrimiento ≤3 (separado) + `clob observe` 7×12 = **84 lecturas REST** + WS por 90 min en 6 boots. Sin reintentos; `retry_after_seconds`/429/1310 ⇒ registro y fin del paso (PREREG §9).
- Bytes: peor caso hipotético 20× ≈ 0,16 GB; ancla medida 0,0894 MB/min; medición real al sellar; stop-line 8 GB dura.
- Recursos: un comando a la vez; CPU 2 / RAM 2 GiB (prlimit); journal en disco local del workspace.

### 7. Decisiones externas

1. **Metis:** adjudicar receta (opción A) o delta (opción B con su alcance exacto: `internal/regimes/reducer.go` + evaluación TTL en `internal/regimes`, contratos y aceptación en PREREG §4) **antes** de cualquier captura.
2. **Lanzador:** ventana autorizada, perfil por-shot, ejecución de la secuencia con recibos; checkpoint 02:00.
3. **Owner:** sólo decisiones materiales/financieras (cuenta, fondos, riesgo, activación futura) — jamás resolución de ingeniería.

### 8. Qué NO es este plan

No ejecuta nada hoy; no programa campaña de 25 ventanas (aritmética v1 corregida: 40 GB > techo); no promete elegibilidad del 90 % de la ventana (expectativa E1 preregistrada); no convierte el piloto en validación de rentabilidad.

## Fuentes

- [[Preregistration — PE-005-R1 Economic Candidate v2 W1-h 2026-10-29]] (spec vinculante, §4 frescura/writer, §5 estados, §8 aritmética).
- Fuente @ `853c0e4`: `cmd/engine/{catalog_select,clob_observe,record,replay,experiment}.go`; `internal/capture/{capture,recover}.go`; `internal/regimes/{reducer,prospect}.go`; fixture `internal/experiment/w1h_acquisition_recipe_test.go` (PASS).
- Manifests W1-b/c/d/f (anclas de bytes/contadores ya autorizados); [[Polymarket Engine — Continuidad Five-POC 2026-09-20]].

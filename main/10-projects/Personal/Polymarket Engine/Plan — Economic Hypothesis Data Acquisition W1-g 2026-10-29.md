---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
related:
  - "[[Preregistration — PE-005-R1 Economic Candidate W1-g 2026-10-29]]"
  - "[[Research — Economic Strategy Specification W1-g 2026-10-29]]"
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
aliases:
  - "W1-g acquisition plan"
tags:
  - kind/doc
  - topic/research-ops
created: "2026-10-29"
updated: "2026-10-29"
---

# Plan — Economic Hypothesis Data Acquisition W1-g 2026-10-29

## Propósito

- Paquete de adquisición mínima **ejecutable en plan, NO ejecutado** para falsar `PE-005-R1-E1` ([[Preregistration — PE-005-R1 Economic Candidate W1-g 2026-10-29]]). DISEÑO SOLAMENTE pendiente adjudicación Metis: nada de este plan inicia red, captura, descarga ni servicios.
- Reutiliza exclusivamente capacidades reales del Engine verificadas por lectura de fuente @ `853c0e4` (sin `--help`, sin flags inventados). El binario se construye del checkout sin cambios de código.

## Contenido

### 1. Comandos reales existentes (fuente: cmd/engine @ 853c0e4)

| Comando | Flags admitidos (verificados en fuente) | Uso en este plan |
|---|---|---|
| `catalog select` | `--data-dir --out --preregister --base-url --limit(1..100) --max-requests(1..3) --sports-market-types [--now tests]` | selección ex ante ≤4 mercados/lote |
| `clob observe` | `--data-dir --manifest --phase init|final --clob-url --out` | metadata tick/fee (`/clob-markets/{cid}`, `/tick-size?token_id=`); `/fee-rate` NO se usa |
| `record` | `--data-dir --assets --ws-url --duration --json --reconnect --reconnect-backoff --reconnect-backoff-max --status-file --stop-file` | ventana WS por lote |
| `journal verify` | `--data-dir` | integridad CRC/contigüidad/frontier |
| `manifest build` | `--data-dir --out --label --cutoff --seed` | pin de segmentos (payload SHA-256) |
| `replay` | `--data-dir --manifest --schedule` | reproducibilidad y cortes negativos |
| `experiment shadow` | `--data-dir --run-id --hypothesis --strategy --mode --spread-threshold --bankroll --seed [--param k=v]` | corrida virtual del strategy |
| `experiment compare` | `--data-dir <a> <b>` | comparación durables base/variante |

- WS por defecto (`marketws.DefaultURL`): `wss://ws-subscriptions-clob.polymarket.com/ws/market`; Gamma default `https://gamma-api.polymarket.com`; CLOB default `https://clob.polymarket.com`.
- Especificación del strategy en shadow (forma demostrada en `five_poc_cases_test.go`): `--strategy "poc-sports:kickoff_ms=<K>;window_ms=300000;ref_frames=10;widen_min_bps=50;entry_budget=25;min_net_edge_bps=50;fee_low_bps=0;fee_high_bps=500;taker=true"`.
- **Propuesto NO existente (gate distinto, no comando real):** un flag `--execution DECLARED_L2` en `experiment shadow` NO existe hoy (el campo `RunManifest.Execution` es code-level sin flag CLI). Su uso exigiría delta de código y decisión Metis; el endpoint primario de E1 (toque de B\*) NO lo necesita: se lee de `strategy_metrics` del scorecard (`reverted/not_reverted/rejected_by_costs/blocked`).
- **Orquestación de campaña:** el Engine NO trae runner de campaña. Delta mínimo = ejecución lote-a-lote de la receta pre-escrita (§3) por el operador, sin plataforma nueva. Sin jobs nocturnos.

### 2. Regla de selección ex ante y límites por lote

- Selección: idéntica a la regla v6 probada (`sportsMarketType=moneyline`, `gameStartTime` futuro parseable, fail-closed, ranking por kickoff ascendente, jamás por precios/volumen), con presupuesto de descubrimiento 100 candidatos / 3 requests por lote, reintentos HTTP desactivados (cada GET cuenta 1).
- Máximo **4 mercados (8 assets)** capturados simultáneamente por lote (techo del hook + manifiesto, ya test-enforced). Eventos ligados al partido: sólo los assets de los mercados seleccionados; ninguna otra suscripción.
- Gate OOS: id-only pre-interpretación con sellados `3901955`/`3901953` y **extensión preregistrada**: todo mercado ya asignado a un bloque (exploratorio/OOS-nuevo) no puede re-seleccionarse en el otro bloque.
- Preregistro de máquina por campaña: JSON con params §4 del PREREG, límites y hash; lo vincula `catalog select --preregister` (SHA del archivo dentro del selection manifest).

### 3. Receta por lote (una ventana de episodio)

Precondición: kickoff K conocido por selección; ventana `[K−90min, K)`; sin intersección con 02:00–08:00 GMT-3.

1. `catalog select …` (nuevo data-dir de episodio) → `selection-manifest.json`.
2. `clob observe --phase init …` → 12 lecturas REST journalizadas (receive = `known_at`).
3. `record --assets <8 ids> --duration 90m --reconnect --reconnect-backoff 1s --reconnect-backoff-max 30s --status-file <status.json> --stop-file <stop>`.
4. **Re-polls de metadata a T−60 y T−30:** nueva invocación de `clob observe --phase final` (reutilización del comando existente; la etiqueta de fase es rotulado, el reducer deduplica por contenido y cada body journaliza con su recepción). Sin código nuevo.
5. A K: `clob observe --phase final` → `observe-final.json`.
6. `journal verify --data-dir <episodio>` → `NO_INTEGRITY_FAILURES` exigido.
7. `manifest build --label w1g-ep<N> --out manifest-ep<N>.json`.
8. `replay --schedule 32,7,1` y `--schedule 7,32,1` (invariancia) + cortes derivados a T−75/T−45/T−15 (verificación causal, PREREG §10).
9. Sellado del episodio: artefactos con run-id único en nombre (lección W1-f: jamás nombres sin run-id), manifiesto + hashes en el ledger de campaña.

- **Análisis (offline, fuera de captura):** `experiment shadow --data-dir <episodio> --run-id w1g-e1-ep<N> --hypothesis PE-005-R1 --strategy "poc-sports:…" --bankroll 500 --seed 20260917`; `experiment compare` sólo entre runs declarados base/variante preregistrados. `kickoff_ms` sale de la selección ex ante.
- **Stop/deadline:** stop-file cierra el journal con exit 0; deadline duro = K (y 02:00 GMT-3); tope 90 min/lote; sin reintentos automáticos ante 429 — se registra `retry_after_seconds` (campo documentado del error CLOB) y el lote termina.

### 4. Piloto mínimo y campaña de suficiencia (diferenciados)

- **Piloto (3 episodios):** valida la receta de extremo a extremo (selección→venta→shadow) y mide la tasa real de frames/bytes cerca de kickoff. Criterio de continuación: receta verde sin desviaciones y journal íntegro en 3/3; si no, corrección documental y re-despacho Metis (sin tuning de hipótesis).
- **Campaña:** episodios hasta alcanzar la suficiencia del PREREG §13 (≥90 señales primarias en ≥30 episodios) o hasta límites de §6. Bloques: exploratorio = episodios 1–60; OOS-nuevo = 61+ (sellado, PREREG §12).

### 5. Endpoints públicos usados y parámetros documentados

- `GET https://gamma-api.polymarket.com/markets` — query params documentados usados: `limit`, `offset`, `closed`, `active`, `sports_market_types`, `order`, `ascending` (priorización de presupuesto; la elegibilidad es client-side fail-closed). `start_date_min` RETIRADO (semántica no documentada).
- `GET https://clob.polymarket.com/clob-markets/{condition_id}` — campos usados con semántica documentada: `mbf`, `tbf` (bps base legacy), `fd{r,e,to}`, `mts` (tick), `mos`, `gst`, error `retry_after_seconds`. `rebateRate` sólo existe en el `feeSchedule` de Gamma (market-details), no en `fd`.
- `GET https://clob.polymarket.com/tick-size?token_id={asset_id}`.
- `WSS wss://ws-subscriptions-clob.polymarket.com/ws/market` — suscripción por asset; `book` inicial completo por asset (initial_dump); PING/PONG 10 s; sin resume: reconexión = epoch nuevo.
- **NO usados:** `/fee-rate` (decisión W1-d mantenida), trades/pricehistory/outcomes, Gamma `start_date_min`, cualquier endpoint autenticado.

### 6. Volumen, presupuesto y recursos

- **Fórmula:** `bytes ≈ frames_s·bytes_frame·horas·assets + REST_overhead`. Anclas medidas (capture-v6, 5 min, 8 assets, lejos de kickoff): 75 registros WS = 447.016 B payload (≈5,96 KB/registro); REST observe ≈785 B/body ×12 por invocación; página Gamma de selección ≈550–592 KB una vez por lote.
- **Rango hipótesis vs medido:** calmo ≈0,9 MB/min/lote de 4 mercados → ~81 MB por ventana de 90 min; rango de estrés cerca de kickoff **3–20×** (no medido; supuesto conservador explícito) → 0,24–1,6 GB/ventana. Piloto 3 ventanas ≈ 0,7–5 GB peor caso; campaña de hasta ~25 ventanas adicionales se mantiene bajo el techo **10.000.000.000 bytes** con ledger acumulado del `journal verify`/manifests; stop de presupuesto en 8 GB (reserva 20%).
- **Recursos:** CPU 2 / RAM 2 GiB por proceso (prlimit), un lote a la vez, sin background; journal en disco local del workspace OUT.
- **Cuotas/backoff:** sin reintentos HTTP en descubrimiento (DisableRetry); `record --reconnect` con backoff 1 s→30 s; 429/1310 → parada y registro, honor de `Retry-After`/`retry_after_seconds`, sin bucles.

### 7. Pausa diaria, integridad y sellado

- **Pausa 02:00–08:00 GMT-3 completa, sin gracia:** ningún lote se programa intersectándola; si el venue mueve un kickoff a esa franja, el lote aborta a las 02:00 por stop-file y el episodio queda **truncado/censurado** (PREREG §10) — nunca se "rellena" la ventana.
- **Relojes y secuencia:** cada registro journal trae `ReceivedWall`, `CaptureSeq`, `Epoch`, `ConnectionID` (verificado en fuente); el PIT es receive-time; los venue-ms son datos, no base causal.
- **Integridad/dedup:** `journal verify` por episodio (CRC+contigüidad+frontier), `manifest build` pina payload SHA-256 por segmento, `account_fact DEGRADED` es estado honesto esperado; dedup por contenido en metadata (sólo cambios crean revisiones).
- **Sellado OOS-nuevo:** manifiestos de selección con fecha/kickoff; a partir del episodio 61 los artefactos se marcan `OOS_SEALED` y no se leen métricas hasta la apertura del PREREG §12.
- **Conservación de versiones:** SHA-256 del binario construido de `853c0e4` (sin cambios de código), `go.mod`/`go.sum` hasheados, preregistro y sus revisiones (v1, v2…) inmutables con historial; cada corrección = revisión nueva, jamás edición in-place.

### 8. Decisiones externas requeridas (antes de adquirir)

1. **Metis:** adjudicación del paquete (este plan + PREREG) y del perfil por-shot de comandos (lote §3 con re-invocaciones de `clob observe`).
2. **Metis/Owner:** si la campaña a suficiencia excediera max-4/10 GB/90-min por episodio (no lo hace bajo el rango conservador de §6), se requiere decisión EXACTA previa — no se simplifica la hipótesis para forzar cobertura con ventanas de 5 min.
3. **Owner (sólo materiales/financieros):** cuenta, elegibilidad, fondos, riesgo, activación — jamás resolución de ingeniería ni certificación de fees por defecto.

## Fuentes

- [[Preregistration — PE-005-R1 Economic Candidate W1-g 2026-10-29]] (spec de la hipótesis).
- Fuente Go @ `853c0e4`: `cmd/engine/{catalog_select,clob_observe,record,replay,experiment}.go`, `internal/transport/marketws/marketws.go`, `internal/experiment/{experiment.go,w1f_hypothesis_integration_test.go}` (lección run-id).
- Manifests reales: `selection-manifest-v6.json`, `capture-manifest-v6.json`, `preregister-v6.json`, `observe-init-v6.json`, `capture-status-v6.json`, `journal/manifest.json` (anclas de bytes); `W1-C-MANIFEST.json` (formas shadow/compare ejecutadas).
- [[Research — Economic Strategy Specification W1-g 2026-10-29]] (fees, matriz de aptitud, límites).

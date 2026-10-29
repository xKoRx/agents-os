---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
related:
  - "[[Preregistration — PE-005-R1 Economic Candidate v2 W1-h 2026-10-29]]"
  - "[[Plan — Single Episode Pilot v2 W1-h 2026-10-29]]"
  - "[[Research — Economic Strategy Specification W1-g 2026-10-29]]"
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
aliases:
  - "W1-h corrective research report"
tags:
  - kind/doc
  - topic/research-ops
created: "2026-10-29"
updated: "2026-10-29"
---

# Research — Economic Pilot Corrections W1-h 2026-10-29

## Propósito

- Informe del shot correctivo W1-h (one-shot GLM-5.3-Flash Max vía ZCode, `sqx-ulab-hefesto-0`, 2026-10-29): resolver UNA vez las siete correcciones del lanzador sobre el paquete W1-g, con evidencia de fuente Go y fixture offline propia; entregar el paquete v2 (PREREG + PLAN) para adjudicación de Metis. Sin ejecutar adquisición, sin capturas, sin APIs de mercados, sin raw adicional, sin código productor.

## Estado actual (arriba)

- Checkout `w0/offline-causal-replay-20261027` @ `853c0e46c9be2de4e84201e240e9cf8366b1036e`, árbol limpio salvo UN archivo nuevo untracked: `internal/experiment/w1h_acquisition_recipe_test.go` (SHA `f7c03a4829cae2d31e77bd68be80f1f2c389a18143182dce44d24152f3c0fa17`). Sin commit (perfil del shot sin mutaciones git); HEAD/W1f intactos; OOS/raw/12 inputs intactos; cero requests de mercado.
- Suite autorizada ejecutada 2 veces (intento 1: build FAIL por 3 bugs ordinarios del propio fixture; intento final): **PASS exit 0** — `ok github.com/xKoRx/polymarket-engine/internal/experiment 0.018s` con el comando exacto del mandato (`-run '^TestW1H' ./internal/experiment`, 5 tests).
- Paquete v2 entregado para **adjudicación** (no aprobado): [[Preregistration — PE-005-R1 Economic Candidate v2 W1-h 2026-10-29]] + [[Plan — Single Episode Pilot v2 W1-h 2026-10-29]]. El piloto NO está autorizado ni ejecutado.

## Las siete correcciones → evidencia / estado / decisión

1. **Frescura y writer — RESUELTA con bloqueo parcial del diseño v1.** Evidencia: `internal/regimes/reducer.go` `upsertRegimeRevision` (duplicado por `content_hash` ⇒ sólo `last_observed_at`; sin revisión nueva); `internal/regimes/prospect.go` `ProspectiveTickTTL=15m` con borde inclusive/stale y adquisición acotada por `capture_seq`; `internal/capture/capture.go` `Open` (sin exclusión entre procesos) + `recover.go` (adopta boots activos ajenos). Fixture `TestW1HMetadataFreshnessRecipe`: re-poll idéntico a T0+10m ⇒ 0 revisiones nuevas, `known_at` del ganador sigue en T0, book a T0+15m+1ns ⇒ `observation_stale`; cambio de lexema a T0+20m ⇒ revisión 2 que re-ancla. Fixture `TestW1HConcurrentWritersUnsupported`: segundo `Open` vivo sin exclusión, colisión de seqs, y al reabrir el journal se lee **limpio** (frontier 3, 0 discontinuidades) mientras el registro ACKed-duradero del primer writer es **inacrible por la vista** — pérdida silenciosa. Estado: la v1 era doblemente infundada (frecuencia no arregla frescura; concurrencia no soportada). Decisión en v2: receta serial de 6 tramos×15 min con `observe` entre tramos (opción A, ejecutable hoy, con expectativa E1 de elegibilidad ≈15/90 con metadata estática) **o** delta de renovación de recepción (`observed_at`/`capture_seq` separado de first_seen, sin inferir estabilidad; archivos `internal/regimes/reducer.go` + evaluación TTL en `internal/regimes`; aceptación en PREREG §4) sujeta a decisión de Metis **antes** de capturar.
2. **Economía — RESUELTA.** Endpoint v1 (toque de B\*) reclasificado como diagnóstico; v2 define round trip virtual a H=300 s con entrada sobre profundidad (latencia 1 frame), liquidación **full-size** a bids (profundidad insuficiente ⇒ `exit_non_executable`, permanece en el denominador), costes de ambas patas al escenario y pérdidas con signo. Fixture `TestW1HEconomicsVirtualExitAtHorizon` sobre `economics.WalkSide/BuildQuote` reales: entrada 40 @ worst 0,55 = 21,1; FeeHigh 1,055/2,11 exactos; recuperación cubierta ⇒ +0,645 con 500 bps y **−1,61 con estrés 1000 bps** (mismo camino); salida a 0,45 ⇒ −5,055 conservado; bids 10/40 ⇒ no ejecutable. Taxonomía de 7 estados fijada; gap ⇒ `invalid_gap`; sin datos futuros; exposición virtual ≤ USD 500.
3. **Fees — RESUELTA.** 500 bps degradado de "dominante" a **sensibilidad condicional del escenario A** (fórmula documentada deportes 0,05, vigencia desconocida); 1000 bps = **estrés separado** (cap legacy, U-02); sin POINT ni fee-0 inventados; `REAL_FEE_READY=false` intacto; el fixture demostró que el mismo camino rentable con 500 es pérdida con 1000 — la elección de cifra no reduce la incertidumbre. Sin requests nuevos; correspondencia oficial por mercado sólo con evidencia existente.
4. **Estadística — RESUELTA.** Piloto = UN episodio **descriptivo por partido** (1 cluster por partido; ambos outcomes/mercados del mismo kickoff en UN cluster). Prohibidos en el piloto: Wilson sobre señales correlacionadas, factor 1,3 como IC por cluster, mezclar parada-90-señales con horizonte-60-episodios, potencia sin base. Fase inferencial diferida a apertura prospectiva con unidad/estimando/dependencia/enrollment/split (60 exploratorio + OOS-nuevo sellado)/rechazo predefinidos; tamaño por precisión/presupuesto con supuestos declarados. Sin ATL3901955/SEA3901953; sin IDs de OOS inventados.
5. **Presupuesto/aritmética — RESUELTA.** 447.016/5 = **89.403,2 B/min = 0,0894 MB/min** (fixture `TestW1HPilotWindowAndCountingRules` fija el decimal y rechaza 0,9); 25 ventanas×1,6 GB = 40 GB ⇒ campaña **no programable** bajo techo 10 GB; piloto 1 episodio 20× ≈ 0,16 GB; proyección total ≈3,1 GB (preflight lanzador 2.931.394.683 B) < stop-line 8 GB; parada antes del techo, sin borrado de datos; 81−74 ⇒ ≥1 registro multi-evento por palomar y **no** ≥7 (contraejemplo 73×1+1×8=81 fijado por fixture).
6. **Selección — RESUELTA en diseño.** Reglas para kickoffs "hoy": página documentada `order=gameStartTime&ascending=false` como priorización (aceptación server-side observada una vez, sin prometerla), re-verificación de orden client-side, filtros ex ante `[now+30m, now+26h]` + pausa + OOS id-only pre-contenido, ≤4 mercados/8 assets del mismo partido cuando exista, presupuesto 3 requests/100 candidatos, desenlace `NO_ELIGIBLES_EN_LOTE` honesto sin ampliar familia. No se consultó ningún mercado en este shot; v6 (Nov 18) NO se asume servible.
7. **Supervisión — RESUELTA.** Receta serial de pasos foreground con recibos durables (status-file por tramo, recibos observe, verify), sin daemon/cron ni procesos residentes; checkpoint duro 02:00 GMT-3 con stop-file pre-colocado 15 min antes y pausa completa 02–08 sin gracia; episodio intersectado ⇒ censura ex ante; tras fallo de transporte: preservar logs/exit/heartbeat, `journal verify` antes de relanzar, estado incierto declarado, sin retry automático. El launcher existente sirve de referencia de capacidades; no se implementó supervisor nuevo.

## Viabilidad de la receta y delta

- **Ejecutable HOY sin código productivo (opción A):** sí, con el coste de elegibilidad preregistrado E1 (≈15/90 de frames elegibles con tick estático; los tramos seriales permiten al menos entregar re-polls al journal y capturar cambios reales de contenido si ocurren). El piloto mide ese perfil como desenlace, no como fallo.
- **Delta productor (opción B) propuesto, NO implementado, NO aprobado:** renovación de recepción en el branch de duplicado (`internal/regimes/reducer.go`) + anclaje del TTL a la última renovación admitida (`internal/regimes/prospect.go`/service), first_seen intacto, sin inferencia de estabilidad; aceptación completa en PREREG §4. Requiere decisión explícita de Metis antes de implementar/capturar.
- La prueba NOT_RUN está justificada donde la lectura de fuente bastó (p. ej. no hay fixture de `catalog select`/`record` reales: exigiría red o binario, fuera de alcance); el fixture propio cubre exactamente las semánticas disputadas (frescura, writer, economía, aritmética, ventanas).

## Siguiente acción para UN episodio

Metis adjudica en una pieza: (a) PREREG v2 + PLAN v2, y (b) opción A u opción B de §4. Tras adjudicación (y, si B, implementación+regresión del delta): lanzador descubre kickoffs con las reglas §3 (desenlace `NO_ELIGIBLES_EN_LOTE` permitido), fija ventana sin intersección de pausa, ejecuta la secuencia serial §4 del PLAN con recibos, sella el episodio y el análisis descriptivo §5 se corre offline. Owner: sólo decisiones materiales/financieras.

## Límites

- Fixture demostrativa de semántica, no suite general: no re-certifica W1-f ni la estrategia (código ya certificado, citado por lectura); no prueba nada sobre red/venue. Sin datos nuevos: ninguna cifra económica aquí es evidencia de edge. La expectativa E1 es una predicción registrada, no un resultado.
- Denegaciones registradas sin variantes ni reintentos: TodoWrite (2 intentos, perfil del shot); `gofmt -w` corto (denegado; forma autorizada: ruta completa `/home/kor/opt/go/bin/gofmt`). Un intento de materializador con ruta absoluta falló por contrato (exige ruta relativa al vault); corregido.

## Fuentes

- Fixture: `internal/experiment/w1h_acquisition_recipe_test.go` (única fuente editada; SHA arriba; gofmt aplicado; recibo de corrida en OUT `w1-h-economic-pilot-v2-20261029`).
- Fuente Go @ `853c0e4`: `internal/regimes/{reducer,prospect}.go`, `internal/capture/{capture,recover,envelope}.go`, `internal/economics/economics.go`, `internal/persist/persist.go`, `cmd/engine/record.go`, `internal/strategy/pocs/sports/sports.go`, `internal/experiment/w1f_hypothesis_integration_test.go` (APIs read-only).
- W1-g originales y continuidad §§18–19; `.private-execution/w1h/{inputs.json,workspace-preflight.json}`.

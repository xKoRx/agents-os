---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
related:
  - "[[Plan — Minimal Economic Instrumentation W1-l 2026-10-30]]"
  - "[[Research — W1-j Causal Gate Diagnosis 2026-10-30]]"
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
aliases:
  - "W1-m instrumentación económica"
  - "Research W1-m"
tags:
  - kind/doc
  - topic/research-ops
created: "2026-10-30"
updated: "2026-10-30"
---

# Research — Economic Instrumentation W1-m 2026-10-30

## Propósito

- Ejecutar el incremento técnico aprobado (P0-2, P0-3, P1-4, P1-5, P2-6 del plan W1-l): instrumentación económica fiel sobre la ruta de revisión existente del piloto PE-005-R1, sin cambiar estrategia, parámetros ni decisiones; re-exportar el episodio sellado W1-j con identidad por fila y provenance de fees; objetivo de evidencia económica reproducible y honesta, no claims de beneficio.

## Contenido

- Precondición crítica ejecutada ANTES de tests/revisión: `revisionDirName` (economics.go) y `revisionOutDir` (supervisor_test.go) movidos a `analysis-revision-w1m-20261030`; el hook abrió tests/revisión sólo con ambos destinos declarados; los receipts ejecutados W1-j quedaron intactos (hashes re-medidos después de la corrida: original `8fc7ec9d…` y revisión W1-j `93e7fe79…` sin drift).
- P0-2: la ventana de referencia ahora viaja por fila con identidad — `reference_window` con hasta 10 observaciones pre-append `{seq, wall_utc, bid, ask, mid, spread_bps}` + el frame de señal marcado `is_signal_frame`; `ref_bps` (excluye señal, orden Detect congelado) y `reference_level_L` (incluye señal, orden Evaluate congelado) re-derivables desde la ventana; flags de inclusividad explícitos; exporta para rechazos y para ACCEPTs (`accept_rows`, inerte en el episodio sellado, ejercitado en sintético).
- Regla descriptiva preregistrada ANTES de la revisión (`w1m-prereg-side-leadership.md/.json` en la ruta nueva): partición total y mutuamente excluyente sobre observaciones fuente definidas — derivas exactas `d_bid`/`d_ask` contra medianas lower-middle por lado de la ventana; etiquetas `bid_led`/`ask_led`/`mixto`/`NO_IDENTIFICADO`; sin causalidad, sin inferir desde una mediana sola, sin tuning. En el episodio real los dos assets widening abren por lados OPUESTOS (50306… `bid_led` con bid −0.01/ask 0; 61296… `ask_led` con bid 0/ask +0.01) — observación mecánica por fila, no claim.
- P0-3: `signalRow` ampliado con descomposición completa del round trip ACCEPT — datos del frame de señal (spread/ref/widening/L/leadership), pata de entrada y salida con `{seq, best, size, notional, worst_price, levels_touched, takes_por_nivel}` vía `WalkSideDetailed`/`LevelTake` (mismo Sweep de `WalkSide`), fees por pata al bound, gross, net, B*, H=señal+300s, reason codes estructurados; campos nuevos siempre presentes con valor o null explícito (null = el estado nunca llegó a esa pata); inerte hoy (0 ACCEPTs reales), nace listo para re-score o dato futuro.
- P2-6: timestamps efectivos y gaps por fila — H, `segment_index`/`segment_end_utc` reales en toda fila; toda fila `invalid_gap` declara el fin de segmento OBSERVADO que la causa (no deadline planeado); latencias señal→entrada y salida→H en segundos y en registros WS.
- P1-4 (test-only): oráculos de la FÓRMULA de fee por nivel — `LevelCost == truncate6(rate·p^e·(1−p)^e·take)` con fixture `SYNTHETIC_FIXTURE` (incluye exponente 2 y truncamiento 6dp pineado), Σ costes por nivel sobre `Takes` de `WalkSideDetailed` == `FeeTotal`, INTERVAL [0,500]/UNRESOLVED nunca colapsan a POINT inventado, `REAL_UNVERIFIED` etiquetado in-band como no-certificación; `internal/regimes/w1m_schedule_test.go` + `internal/economics/w1m_scheduled_test.go`, cero código de producto.
- P1-5: provenance de fees exportada en AMBOS artefactos — `fee_formula_applied` (bound lineal por pata vía BuildQuote), `fee_schedule_applied` = null con razón «never applied in this pilot», y `fee_captured_evidence_note` con la evidencia capturada citada EXPLÍCITAMENTE como W1-e sobre capture-v6 (OTROS mercados, no evidencia W1-j): tick 0.01, mbf/tbf 1000 legacy (INTERVAL [0,1000] condición / UNRESOLVED asset), fd verbatim, fee_observed 0; REAL_FEE_READY=false.
- UNKNOWN del plan W1-l cerrado con código leído: `pocdata.EncodeLevels` trunca a `TopLevels = 6` niveles por lado — la profundidad exportable es top-6, exactamente la que la estrategia congelada consumió; no existe profundidad mayor en el artefacto y así se declara en assumptions.
- Revisión nativa UNA ejecución sobre el episodio sellado (sólo journal + engine.db READONLY por flujo nativo): veredicto INCONCLUSIVE preservado, frames 18393/18400, rechazos A=36 S=36 = 72 EXACTOS, cobertura pineada idéntica; comparación por asset/seq/escenario contra el artefacto W1-j congelado: valores compartidos idénticos fila a fila en los solapes verificados (2059/61296 net −1385 depth 74900.39; 2060/50306 net −1073 depth 86615.26 exit 24.8067; 2062/50306 net −1146 exit 24.6144 fee 1.23072); recibos con comandos/exit/hashes en `w1m-run-receipt.json` y `w1m-comparison-w1j.json`.
- Tests: suite EXACTA verde (`ok` cmd/researchpilot 9.499s, internal/economics, internal/regimes) — decisiones y agregados EXACTOS pineados por los tests preexistentes siguen verdes; build EXACTO produce `pilot-supervisor` en la ruta nueva; gofmt `-l` vacío; commit local `9f6caaa` (5 archivos propios, sin push).
- Límites: un episodio, sin IC ni poder, fee UNRESOLVED, `sufficiency_deficit` (falta de profundidad de ENTRADA) sigue sin caso sintético directo — la falta de profundidad de salida sí está cubierta (exit non-executable); clasificación de liderazgo descriptiva de niveles, no de mecanismo; la regla de L (incluir/excluir frame) sigue siendo decisión Owner pendiente de preregistro v3 — este shot NO la adjudicó y la sensibilidad incluir/excluir no se calculó.

## Fuentes

- Repo `polymarket-engine` (rama `w0/offline-causal-replay-20261027`, commit `9f6caaa`): `cmd/researchpilot/economics.go`, `cmd/researchpilot/supervisor_test.go`, `cmd/researchpilot/w1m_instrumentation_test.go`, `internal/economics/w1m_scheduled_test.go`, `internal/regimes/w1m_schedule_test.go`; lectura: `supervisor.go`, `economics_test.go`, `main.go`, `discovery.go`, `internal/strategy/pocs/pocdata/{pocdata,l2}.go`, `internal/strategy/pocs/sports/sports.go` (congelado), `internal/economics/{economics,scheduled}.go`, `internal/regimes/schedule.go`.
- [[Plan — Minimal Economic Instrumentation W1-l 2026-10-30]] (deltas P0-2/P0-3/P1-4/P1-5/P2-6), [[Research — W1-j Causal Gate Diagnosis 2026-10-30]], [[Research — Prospective Metadata Quality W1-e 2026-10-28]] (procedencia de la evidencia de fees citada).
- Artefactos: `validated-baseline/w1-j-single-episode-pilot-20261029-lot3/analysis-revision-w1m-20261030/` — `analysis-revision-w1j-ep-20261029T2230-identity.json` (`w1m-revision-20261030T031117.575690517Z`, sha256 `d646e56e…`), prereg, recibos, preflight/inputs de TestMain, binario `pilot-supervisor` (`91fd24c1…`).

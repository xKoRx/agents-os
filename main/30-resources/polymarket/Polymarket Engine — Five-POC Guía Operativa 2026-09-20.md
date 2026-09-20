---
type: resource
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
created: 2026-09-20
updated: 2026-09-20
aliases:
  - Five-POC operational guide
  - Guía operativa Five-POC
tags:
  - kind/resource
  - tech/polymarket
  - topic/research-ops
---

# Polymarket Engine — Five-POC Guía Operativa (2026-09-20)

Guía operativa mínima para tomar cualquiera de las cinco POCs y experimentar sin
re-derivar la integración. Baseline integrada: `feature/five-poc-integration`
(sobre shared `9d0512a`). WORKTREE de integración:
`~/go/src/github.com/xKoRx/polymarket-engine-integration`. Live siempre
`LIVE_DISABLED`; SHADOW es virtual (`INCONCLUSIVE` honesto, nunca permiso).

## Invocación homogénea (los comandos)

```bash
cd ~/go/src/github.com/xKoRx/polymarket-engine-integration && go build -o /tmp/engine ./cmd/engine
# 0) FIXTURE — materializar el journal de entrada (SINTÉTICO, determinista, nunca sobrescribe)
/tmp/engine fixture fivepoc --kind vertical --out /tmp/j-s01s02   # S01/S02 (AAA/BBB/S1)
/tmp/engine fixture fivepoc --kind s03      --out /tmp/j-s03      # par B0 de S03
/tmp/engine fixture fivepoc --kind combined --out /tmp/j-all      # los cinco consumidores (forecast weather admitido primero)
# 1) SCREEN — detector sobre frames causales de un journal fixture (read-only)
/tmp/engine screen-consolidated --data-dir <journal> --cuts <N> --run "<strategy_id>:<k=v>;..."
# 2) SHADOW — economía virtual sobre el mismo journal (scorecard JSON, durable)
/tmp/engine experiment shadow --data-dir <journal> --run-id <run> --hypothesis <PE-xxx> \
  --strategy <strategy_id> --param k=v [--param ...] [--seed N]
# 3) COMPARE — "¿qué cambió entre dos runs?" desde artifacts, sin logs
/tmp/engine experiment compare --data-dir <journal> <run-a> <run-b>
# 4) REPLAY — pin del journal y replay determinista de observaciones
/tmp/engine manifest build --data-dir <journal> --out /tmp/m.json
/tmp/engine replay --data-dir <journal> --manifest /tmp/m.json --schedule 2,1   # → RESOLVED
```

- INPUT de todos: un **journal fixture** materializado con `engine fixture fivepoc`
  (capture dir cerrado, reloj de fixture + stamps de receive timeline: es
  históricamente determinista y nunca se vuelve `STALE_BOOK` por el reloj de pared).
  Sintéticos (`SYNTHETIC_FIXTURE`) para cierre offline; nunca mezclar con
  `REAL_CAPTURE`; el guard SFG-07 rechaza directorios protegidos y el comando nunca
  sobrescribe un output existente.
- OUTPUT inspectable: reporte JSON de screen (deliveries→evaluations con
  `decision`, `reason_codes`, `metrics`; ahora con `engine_sha` y `dataset_digest`),
  `{outcome, detail, scorecard}` del shadow (`scorecard.content_hash`,
  `observation_digests`, `engine_sha`, `mode`, `dataset_digest`; el run y su scorecard
  quedan durables en `experiment_runs` / `experiment_scorecards` del `engine.db` del
  data-dir), el delta estructurado del compare (parámetros cambiados, contadores,
  métricas, hashes), el `RESOLVED` del replay, y descriptores/observaciones durables
  en la lane RUNTIME del journal.
- Determinismo: misma invocación (mismo run-id + seed) → mismo `content_hash`; los
  stamps de los frames viajan en la receive timeline del journal, así que dos runs
  sobre el mismo journal producen stamps idénticos aunque se ejecuten a distinta hora.
- Comparar BASE vs VARIANT: correr los dos shadows sobre el MISMO journal y
  `experiment compare` — los `parameters_changed` nombran la mutación, los
  `counters_differ` el efecto; `dataset_digest` igual en ambos prueba mismo input.
- Drill completo worked-example por POC (BASE/VARIANT + compare):
  `testdata/research-v05/experiment-drills/DRILLS.md` en el repo.

## POC-S01 — NegRisk / PE-002 (`poc-negrisk`)

- **HOW TO RUN**: `--run "poc-negrisk:event_id=0xe1;assets=AAA,BBB;membership=VERIFIED;exhaustiveness=VERIFIED;other_present=NO;protocol=CTF;fee_bps=0;min_edge_bps=50;max_size_per_leg=25"` (shadow: mismos valores como `--param`).
- **MODE**: SCREEN + SHADOW (2-leg basket, fills sólo de profundidad observada).
- **Caso de uso**: NEG-CASE-01 (`go test ./cmd/engine/ -run TestF5NegCase01Vertical`).
- **KNOWN LIMITATIONS**: acepta condicional `CONDITIONAL_UNEXECUTABLE` en SCREEN (read-only); fee `fee_bps` declarada por fixture.
- **REAL DATA STATUS**: datos de mercado reales requieren capture real (guard SFG-07 protege datasets activos).
- **NEXT EXPERIMENT**: variar `min_edge_bps` / `max_size_per_leg` / dataset.

## POC-S02 — Sports Reversion / PE-005-R1 (`poc-sports`)

- **HOW TO RUN**: `--run "poc-sports:kickoff_ms=1893456000000;window_ms=5000;ref_frames=3;widen_min_bps=150;entry_budget=25;min_net_edge_bps=50;fee_bps=0;taker=true"`.
- **MODE**: SCREEN + SHADOW (1-leg taker).
- **Caso de uso**: SPORT-REV-CASE-01 (`-run TestF5SportRevCase01Vertical`): 3 cuts quietos + bid shock → ACCEPT.
- **KNOWN LIMITATIONS**: kickoff desconocido bloquea TODA señal (por diseño); `taker=true` obligatorio (maker UNCALIBRATED).
- **NEXT EXPERIMENT**: `widen_min_bps`, `window_ms`, `ref_frames`, serie de spreads del fixture.

## POC-S03 — Sports Combinatorial / PE-001 (`poc-sports-combinatorial`)

- **HOW TO RUN**: spec completa en `fivePocS03Spec()` (`cmd/engine/five_poc_gates_test.go`): núcleo `q=20;max_pairs=1024;max_book_age_ms=2000;max_skew_ms=250;min_worst_net=0;max_residual_loss=5;candidate_validity_ms=1000;fee_mode=SCHEDULE;fee_rate=0.05;fee_exponent=1;fee_provenance=SYNTHETIC_FIXTURE;risk_*;risk_snapshot_revision=snap-1;pairs=P001` + por par `pair.P001.*` (identidad ml/sp, `relation_verified=true`, `proof_status=VERIFIED`, reglas `pair.P001.rules_ml_*` / `rules_sp_*` con scope/overtime/cancel/exceptions/source_ref/hash/known_at).
- **MODE**: SCREEN + SHADOW DECLARED (basket 2×BUY, residual secuencial; fee schedule sintética explícita; `Cover(A,-h)⇒Win(A)` verificado en proof).
- **Casos**: PE001-CASE-POSITIVE / NO-EDGE / INSUFFICIENT-DEPTH / SEMANTIC-REJECT (`go test ./internal/strategy/pocs/sportscombinatorial/ -run 'TestPE001Case'`) + vertical engine `TestF5G09S03EngineVertical`.
- **KNOWN LIMITATIONS**: claves de reglas SIN punto extra (`pair.P001.rules_ml_scope`, no `rules_ml_.scope`); `known_at` se valida no-vacío y se hashea (no causalidad vs frame).
- **RESEARCH SURFACE**: relación/template (`pair.*`, reglas), `min_worst_net`, `q`, `max_residual_loss`, fixture de libros. Fee REAL = `UNVERIFIED` (U-02) ⇒ sólo `SYNTHETIC_FEE_EXPLICIT`.
- **NEXT EXPERIMENT**: pares con handicaps distintos, `min_worst_net` de sensibilidad, matrices terminales alternativas (vía SPEC).

## POC-S04 — Weather / PE-030 (`poc-weather`)

- **HOW TO RUN**: dataset con observación externa admitida PRIMERO (`external.AdmitSync` con `weather.BaseRun(nil)` + `weather.BuildRequest`; fuente `weather-fixture`), luego libros YES del fixture (`weather.FixtureBooks(weather.BaseBooks())`, assets `weather.YesAssetIDs()`). Instancia: `--run "poc-weather:contract_id=SYN-WX-20260920-HIGH-UTC"` (contrato sintético registrado `BaseEventID`; o `contract_json` completo). SHADOW con `Execution:"DECLARED_L2"` en el manifest.
- **MODE**: SCREEN + SHADOW `DECLARED_L2` (fills sólo desde `Candidate.Legs`; sin I/O desde Strategy — seam SFG-04 `external.Request → AdmitSync → Project → Frame.Externals`).
- **Casos**: WX-CASE-EDGE / NO-EDGE / FUTURE-VINTAGE-REJECT / STALE-BOOK / NO-BASE (`internal/strategy/pocs/weather/cases_test.go`) + pipeline offline C1 (`integration_test.go`: shadow/replay/determinismo).
- **KNOWN LIMITATIONS**: modelo frozen **UNCALIBRATED** (no fabricar calibración); vintage futura rechazada fail-closed; sin proveedor real.
- **RESEARCH SURFACE**: estación/buckets/ensemble (contrato), `size`, `fee_rate`, `validity_ms`, dataset.
- **NEXT EXPERIMENT**: contratos con buckets distintos (vía `contract_json`), ensembles/pesos alternativos, dataset con vintages encadenadas.

## POC-S05 — New Market Maturation / PE-004 O/B (`poc-maturation`)

- **HOW TO RUN**: `--run "poc-maturation:cohort=B;market_id=0xc;asset_id=AAA"` (cohort `O` exige `known_at_ms`; `B` lo PROHÍBE — ancla = primer book usable). Defaults: `windows_s=60,300,3600;max_book_age_s=30;min_two_sided_samples=2;size_grid_shares=1,5,10;params_revision=1`.
- **MODE**: **OBSERVATION_ONLY** (descriptivo): `Opportunity=none`, `Orders=0`; `FrameObserver` → observaciones durables `pe004.*` (spread, mid, profundidad observable, Q1/Q5/Q10 si hay capacidad, impacto, actividad, censoring, controles PE-019/020).
- **OUTPUT**: digests de observación por frame en el reporte screen (`delivery.observation`) y `scorecard.observation_digests` en shadow.
- **Casos**: PE004-CASE-MATURATION / CENSORED / ZERO-OPPORTUNITIES / TRUNCATED-DEPTH / INSTANCE-ISOLATION (`internal/strategy/pocs/maturation/maturation_test.go`, `core_test.go`) + replay digest MATCH (commit `fa69adc`).
- **KNOWN LIMITATIONS**: cohorte W = `DEFERRED_BLOCKED_BY_SFG06` (residual `new_market → Catalog reducer → UniverseChanged`); censoring por diseño, sin backfill.
- **RESEARCH SURFACE**: cohort, `windows_s`, `size_grid_shares`, filtros/metrics.
- **NEXT EXPERIMENT**: ventanas alternativas, grids Q, cohorte B sobre capturas reales futuras.

## Gates transversales y calidad

- Gates F5 (registro, guard, identidad/live-disabled, vertical S03, coexistencia 5): `go test ./cmd/engine/ -run 'TestF5' -count=1`.
- Suite completa: `go build ./... && go vet ./... && go test ./... -count=1` (33 paquetes, verde en la baseline de esta guía salvo gates en vuelo).
- Certificación: `engine experiment certify --profile no-live --baseline <sha>` → `M4_CERTIFIED_NON_LIVE` esperado al cierre del programa.

## Estado del programa (2026-09-20)

`HYPOTHESIS_VALIDATED = NO` en las cinco (esperado). S01/S02 `RESEARCH_READY`;
S03/S04/S05-O/B `RESEARCH_READY_OFFLINE`. Prohibido fabricar alpha/liquidez
(nada de BBO×10); fees sintéticas siempre con provenance `SYNTHETIC_FIXTURE`;
`REAL_FEE = UNVERIFIED`; datos meteorológicos reales `PENDING`.

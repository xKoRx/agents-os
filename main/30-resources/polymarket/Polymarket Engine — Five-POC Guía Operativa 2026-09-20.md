---
type: resource
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
created: 2026-09-20
updated: 2026-09-21
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
  La identidad determinista es `dataset_digest` (records + receive timeline); el
  contenedor del journal lleva `capture_id`/`boot_id` aleatorios por materialización
  (no afecta ningún artefacto de experimento).
- **Interpretación de contadores (auditoría de aceptación 2026-09-20):** en el
  scorecard, `accepted`/`simulated_fills`/`baskets_*` son TOTALES del run y viven en
  unidades distintas: `accepted` = evaluaciones aceptadas (≤1 candidato por frame en
  S01), `baskets_planned` = canastas 1:1 con candidatos, `simulated_fills` = fills a
  NIVEL DE PATA (S01: 919 canastas × 2 patas = 16 fills + 1822 rechazos FOK por
  profundidad; 16 fills == `baskets_completed`). En S04, el bloque
  `strategy_metrics` (`fee_bps`, `net`, `fee_total`, `notional`, `fair_value`,
  `accepted`/`rejected` chicos) NO son agregados del run: son los hechos del ÚLTIMO
  bucket evaluado del ÚLTIMO frame (merge last-wins), por eso una variante con
  `accepted: 0` puede mostrar `fee_bps/net` no cero. Detalle y evidencia:
  `testdata/research-v05/experiment-drills/DRILLS.md` §"Semántica de los contadores".
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

- **HOW TO RUN**: spec completa en `fivePocS03Spec()` (`cmd/engine/five_poc_gates_test.go`): núcleo `q=20;max_pairs=1024;max_book_age_ms=60000;max_skew_ms=250;min_worst_net=0;max_residual_loss=5;candidate_validity_ms=1000;fee_mode=SCHEDULE;fee_rate=0.05;fee_exponent=1;fee_provenance=SYNTHETIC_FIXTURE;risk_*;risk_snapshot_revision=snap-1;pairs=P001` + por par `pair.P001.*` (identidad ml/sp, `relation_verified=true`, `proof_status=VERIFIED`, reglas `pair.P001.rules_ml_*` / `rules_sp_*` con scope/overtime/cancel/exceptions/source_ref/hash/known_at). (Corregido en aceptación final 2026-09-20: `max_book_age_ms` es `60000` en el spec canónico, no `2000`.)
- **MODE**: SCREEN + SHADOW DECLARED (basket 2×BUY, residual secuencial; fee schedule sintética explícita; `Cover(A,-h)⇒Win(A)` verificado en proof).
- **Casos**: PE001-CASE-POSITIVE / NO-EDGE / INSUFFICIENT-DEPTH / SEMANTIC-REJECT (`go test ./internal/strategy/pocs/sportscombinatorial/ -run 'TestPE001Case'`) + vertical engine `TestF5G09S03EngineVertical`.
- **KNOWN LIMITATIONS**: claves de reglas SIN punto extra (`pair.P001.rules_ml_scope`, no `rules_ml_.scope`); `known_at` se valida no-vacío y se hashea (no causalidad vs frame).
- **RESEARCH SURFACE**: relación/template (`pair.*`, reglas), `min_worst_net`, `q`, `max_residual_loss`, fixture de libros. Fee REAL = `UNVERIFIED` (U-02) ⇒ sólo `SYNTHETIC_FEE_EXPLICIT`.
- **NEXT EXPERIMENT**: pares con handicaps distintos, `min_worst_net` de sensibilidad, matrices terminales alternativas (vía SPEC).
- **REALITY CHECK 2026-09-21** (no sustituye el fixture B0): par WNBA event `986912` ML `4358151` / SP `4778073` (ATL −1.5). Spec honesta usa `proof_status=HYPOTHESIS`, `rules_sp_overtime=UNKNOWN`, `rules_sp_tie=true`. Resultado: 0 ACCEPT / `RULES_CONTRADICT`. Bundle `~/go/src/github.com/xKoRx/polymarket-engine-datasets/pe001-reality-check-20260921/`. CLI: `engine experiment shadow` (no subcomando `shadow`); `engine replay` **no** tiene flag `--json`. Congelar el journal de captura **antes** de SHADOW (el shadow escribe RUNTIME). `LIVE_DISABLED`. Decisión `GO_RESEARCH`, no live.

## POC-S04 — Weather / PE-030 (`poc-weather`)

- **HOW TO RUN**: dataset con observación externa admitida PRIMERO (`external.AdmitSync` con `weather.BaseRun(nil)` + `weather.BuildRequest`; fuente `weather-fixture`), luego libros YES del fixture (`weather.FixtureBooks(weather.BaseBooks())`, assets `weather.YesAssetIDs()`). Instancia: `--run "poc-weather:contract_id=SYN-WX-20260920-HIGH-UTC"` (contrato sintético registrado `BaseEventID`; o `contract_json` completo). SHADOW con `Execution:"DECLARED_L2"` en el manifest.
- **MODE**: SCREEN + SHADOW `DECLARED_L2` (fills sólo desde `Candidate.Legs`; sin I/O desde Strategy — seam SFG-04 `external.Request → AdmitSync → Project → Frame.Externals`).
- **Casos**: WX-CASE-EDGE / NO-EDGE / FUTURE-VINTAGE-REJECT / STALE-BOOK / NO-BASE (`internal/strategy/pocs/weather/cases_test.go`) + pipeline offline C1 (`integration_test.go`: shadow/replay/determinismo).
- **KNOWN LIMITATIONS**: modelo frozen **UNCALIBRATED** (no fabricar calibración); vintage futura rechazada fail-closed; sin proveedor real.
- **RESEARCH SURFACE**: estación/buckets/ensemble (contrato), `size`, `fee_rate`, `validity_ms`, dataset.
- **NEXT EXPERIMENT**: contratos con buckets distintos (vía `contract_json`), ensembles/pesos alternativos, dataset con vintages encadenadas.

## POC-S05 — New Market Maturation / PE-004 O/B (`poc-maturation`)

- **HOW TO RUN**: `--run "poc-maturation:cohort=B;market_id=0xc;asset_id=AAA"` (cohort `O` exige `known_at_ms`; `B` lo PROHÍBE — ancla = primer book usable). Defaults: `windows_s=60,300,3600;max_book_age_s=30;min_two_sided_samples=2;size_grid_shares=1,5,10;params_revision=1`. Cohorte `O` tiene DOS modos explícitos (cierre definitivo 2026-09-20): **fixture** — `--param cohort=O --param known_at_ms=<ms>` declara el ancla sintética (paridad con receipts históricos; ausencia de `anchor_source` = fixture); **catalog** — `engine experiment shadow --param cohort=O --param anchor_source=catalog --param market_id=<gamma-id> --param asset_id=AAA` resuelve el ancla ANTES de congelar el manifest vía `CatalogFirstKnownAnchor` (`internal/strategy/pocs/maturation/catalog_anchor.go`) sobre `catalog.Service.InspectEntity` real del dataset (requisito: el market ingerido en el dataset vía `engine catalog sync --id`; jamás antedata con `createdAt`, jamás pasar `known_at_ms` junto a `anchor_source=catalog`, cohorte `B` + catalog se rechaza); el manifest persistido registra `anchor_source` y la ancla resuelta. `CATALOG_WIRING_VERIFIED=YES`, `REAL_CATALOG_DATA_READY=NO` (pendiente sync Gamma en un dataset de captura real).
- **MODE**: **OBSERVATION_ONLY** (descriptivo): `Opportunity=none`, `Orders=0`; `FrameObserver` → observaciones durables `pe004.*` (spread, mid, profundidad observable, Q1/Q5/Q10 si hay capacidad, impacto, actividad, censoring, controles PE-019/020).
- **OUTPUT**: digests de observación por frame en el reporte screen (`delivery.observation`) y `scorecard.observation_digests` en shadow. Campos económicos del scorecard corregidos en v07 (SHA `56e8fac`): `notional_by_scenario` suma el notional real de patas (antes quedaba vacío en runs con patas) y `reserve_held` = reservas vivas del namespace (suma `HeldReserves`, `"0"` sin reservas; antes siempre `""`) — reporting-only, no alimenta Risk; se liberan 1:1 con la observación `FinalFill` (un run-id re-ejecutado sobre el mismo dataset deja reservas vivas por dedup de fill keys). Tabla BEFORE/AFTER completa: `testdata/research-v07/experiment-drills/DRILLS.md`.
- **Casos**: PE004-CASE-MATURATION / CENSORED / ZERO-OPPORTUNITIES / TRUNCATED-DEPTH / INSTANCE-ISOLATION (`internal/strategy/pocs/maturation/maturation_test.go`, `core_test.go`) + replay digest MATCH (commit `fa69adc`).
- **KNOWN LIMITATIONS**: cohorte W = `DEFERRED_BLOCKED_BY_SFG06` (residual `new_market → Catalog reducer → UniverseChanged`); censoring por diseño, sin backfill.
- **RESEARCH SURFACE**: cohort, `windows_s`, `size_grid_shares`, filtros/metrics.
- **NEXT EXPERIMENT**: ventanas alternativas, grids Q, cohorte B sobre capturas reales futuras.

## Superficie de configuración por POC (auditoría 2026-09-20)

La meta: que el próximo agente no trate infraestructura como parámetro de estrategia.
Un parámetro es de experimento sólo si la factory lo acepta por `--param`/`--run`.

**S01 NegRisk** — fixture: `vertical`.
- SAFE_TO_CHANGE_FOR_EXPERIMENT: `min_edge_bps`, `max_size_per_leg`.
- USUALLY_CHANGE: `fee_bps` (siempre declarada por fixture), dataset (nuevo fixture).
- DO_NOT_CHANGE: `membership`/`exhaustiveness`/`other_present`/`protocol` son evidencia de identidad del set — cambiarlos cambia la hipótesis, no el parámetro; core del engine; registries (`strategyCapabilities` es la única fuente).
- REQUIRES_RESEARCH: fee real (U-02), datasets de capture reales.

**S02 Sports Reversion** — fixture: `vertical`.
- SAFE_TO_CHANGE_FOR_EXPERIMENT: `widen_min_bps`, `min_net_edge_bps`, `window_ms`, `ref_frames`, `entry_budget`.
- USUALLY_CHANGE: `fee_bps`, `kickoff_ms` (siempre futuro respecto de los cuts), serie de spreads del fixture.
- DO_NOT_CHANGE: `taker` (maker UNCALIBRATED); core del engine.
- REQUIRES_RESEARCH: fee real; calibración de fills taker.

**S03 Sports Combinatorial** — fixture: `s03`.
- SAFE_TO_CHANGE_FOR_EXPERIMENT: `min_worst_net`, `q`, `max_residual_loss`, `candidate_validity_ms`, `fee_rate`/`fee_exponent` (schedule sintética), risk_*.
- USUALLY_CHANGE: `pair.P001.*` de identidad/reglas (template de par alternativo — cambia el template declarado, sigue siendo input), fixture de libros.
- DO_NOT_CHANGE: Economics y marketview compartidos; path de replay; `fee_provenance` (REAL es `UNVERIFIED`, la factory lo rechaza); claves de reglas con punto extra.
- REQUIRES_RESEARCH: matrices terminales alternativas (vía SPEC), fee real de venue.

**S04 Weather** — fixture: `combined` (forecast admitido primero).
- SAFE_TO_CHANGE_FOR_EXPERIMENT: `fee_rate`/`fee_mode` (input experimental sintético), `size`, `validity_ms`, buckets/estación/contrato vía `contract_json`.
- USUALLY_CHANGE: dataset (vintages encadenadas), ensemble/pesos (contrato).
- DO_NOT_CHANGE: `internal/external` (seam SFG-04); core Strategy API; modelo frozen sin calibración fabricada; `contract_id` registrado (`SYN-WX-20260920-HIGH-UTC` es el BaseEventID real del fixture — el comentario histórico "WX-BASE-V1" es FALSO).
- REQUIRES_RESEARCH: proveedor real; calibración probabilística (hoy UNCALIBRATED).

**S05 Maturation** — fixture: `combined`.
- SAFE_TO_CHANGE_FOR_EXPERIMENT: `size_grid_shares` (Q grid), `min_two_sided_samples`, `max_book_age_s`, `cohort` O/B, `market_id`/`asset_id`.
- USUALLY_CHANGE: `params_revision`, `manifest_ref`.
- DO_NOT_CHANGE: FrameObserver (observación-only, cero órdenes por diseño); `decision_mode`/`no_orders` (forzados DESCRIPTIVE por la factory).
- REQUIRES_RESEARCH: `windows_s` — hoy restringido a {60, 300, 3600} por validación de la factory; ampliar el dominio es un cambio legítimo de research surface dentro del paquete maturation, no alcanzable por parámetro; cohorte W (`DEFERRED_BLOCKED_BY_SFG06`); capturas reales futuras.

## Gates transversales y calidad

- Gates F5 (registro, guard, identidad/live-disabled, vertical S03, coexistencia 5): `go test ./cmd/engine/ -run 'TestF5' -count=1`.
- Gates de research-readiness: `go test ./cmd/engine/ -run 'TestF5G13|TestF5G14|TestF5G15' -count=1` — G13 RESEARCH MUTABILITY (las cinco POCs aceptan una variante significativa por su research surface sin tocar core), G14 OPERATIONAL DISCOVERABILITY (fixture + screen + shadow + compare desde cero con los comandos documentados), G15 ARTIFACT COMPARABILITY (BASE/VARIANT comparables por artifacts con `experiment compare`).
- Suite completa: `go build ./... && go vet ./... && go test ./... -count=1` (34 paquetes).
- Certificación: `engine experiment certify --profile no-live --baseline <sha>` → `M4_CERTIFIED_NON_LIVE` esperado al cierre del programa.

## Estado del programa (2026-09-20, aceptación final)

`FIVE_POC_FINAL_ACCEPTANCE_READY` — baseline final `1bcae43` (HEAD `c915c11` con
receipt `certificate-v06.json` pineado a `1bcae43`); esta guía alineada a ese SHA.
`HYPOTHESIS_VALIDATED = NO` en las cinco (esperado). S01/S02 `RESEARCH_READY`;
S03/S04/S05-O/B `RESEARCH_READY_OFFLINE` (O/B demostradas con anclas causales;
A2 queda como serialización opcional; A3 cubierto por `CatalogFirstKnownAnchor`).
Cinco smokes operacionales de punta a punta verificados en la aceptación; contadores
NegRisk/Weather auditados sin bug (ver sección de interpretación arriba);
`CORE_CHANGES_REQUIRED_FOR_NEXT_EXPERIMENT = NONE`. **M4 RECERTIFICADO @ `1bcae43`:
27 PASS / 0 FAIL / 0 in-scope NOT_RUN / 5 live diferidos** (`testdata/research-v06/`).
Prohibido fabricar alpha/liquidez (nada de BBO×10); fees sintéticas siempre con
provenance `SYNTHETIC_FIXTURE`; `REAL_FEE = UNVERIFIED`; datos meteorológicos y de
Catalog reales `PENDING`; `LIVE_DISABLED`. Revisión humana del rango
`cb549c7..c915c11` y decisión de merge/push pendientes del owner.

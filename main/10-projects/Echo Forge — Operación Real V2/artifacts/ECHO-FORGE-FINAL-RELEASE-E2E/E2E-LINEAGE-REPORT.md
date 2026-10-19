# E2E-LINEAGE-REPORT — w11 (FlowRun 561267ed-224b-48b5-a803-9f7665927998)

## Veredicto

LINEAGE_PASS — la cadena Builder → Retester → Optimizer → WFM → Apply → Final Reretester → MQ5 → EX5 → MT5 → Promotion quedó ligada por autoridad durable exacta (refs/SHAs), sin reconstrucción por nombres.

## Cadena con autoridad durable

- Builder → cohort: 846 estrategias subidas a `wave_11/ndx/l_h1/flow_example_2/v1/01_builder/` (namespace NUEVO, 18:51:57–18:53:13Z); stage `project@sqx-overview.v2` del FlowRun 561267ed; identity bridge del builder (producer token + token local, mismo cómputo que la publicación).
- Cohort → classification/ranking/selection: `classification_snapshots` + 8 `ranking_snapshots` builder-per-type (18:53:57Z) + `SelectionSnapshot` `sha256:d86dd499…` (18:53:58Z) — grano cohort, sellados sobre el batch merged del FlowRun.
- Selection → group: 35 children `GroupSQXWorkflow` con `source=ranking_snapshot`; bindings de retester "Durable retester input bound from exact upstream refs" (evidencia en logs de worker) — matching por identidad canónica normalizada, fail-closed sin upstream exacto.
- Retester → Optimizer: cada child encadena el output retestado (banco de salida físico) al optimizer del mismo child; semántica `steps.go` @ 0.3.2 (la demostrada por el harness corregido del 2026-10-19 en la certificación de lineage 10/10).
- WFM/Robust: 35 `wfm` + 35 `select_robust_run` + 35 decisiones `OPTIMIZER_SELECTION` en `sqx.decisions` (policy robust_run_selection_v2).
- Apply → MagicNumber durable: 35 filas en `sqx.strategy_magic` (26100091104–26100091138, int64, asignadas 19:4xZ) ligadas a `canonical_strategy_id` del cohort; apply persistido en `durable/apply-selected-run/v1/` (489 objetos del flow).
- Final Reretester → MQ5 → EX5: cada `final-<uuid>.mq5` (línea `input long MagicNumber = <durable>`) y `final-<uuid>.ex5` viven bajo `durable/mt5-export/v1/561267ed…/<uuid>/sha256:<digest>/` — la clave misma codifica flow_run + estrategia + digest del artefacto (línea 386 objetos).
- EX5 → MT5: artefactos por estrategia `13_mt5_backtest/final-<uuid>.{htm,tester.log,agent.log,terminal.log,tester.ini,htm.tradeset.ndjson.gz}` bajo el MISMO prefijo por estrategia; el scope del metric set MT5 registra expert=`final-<uuid>`, mágica efectiva leída del HTM (p.ej. 26100091129) == durable.
- MT5 → Ranking → Promotion: 35 scores `mt5_fidelity_shadow.v1` (baseline=trade list del reretester, candidate=mt5-final), ranking final `mt5-final-fidelity-ranking` `sha256:0356f6b7…` (20:51:35Z), decisión `FINALIST_PROMOTION` COMPLETED `sha256:b325fd29…` (policy finalist_promotion@2.0.0) ligada a flow_run_ref.
- Handoff: 35 `handoff_deliveries` HANDOFF_CREATED con seals `durable/forge-seal/v1/561267ed…/<uuid>/effective-inputs-<digest>.json` (35/35).

## Regla de identidad

Ningún salto reconstruyó identidad desde nombres: cohort por FlowRun+namespace MinIO, batch por normalizeBatchIdentityKey con upstream exacto fail-closed, mágica por allocator durable, MT5 por uuid+digest, promoción por decisión con policy digest.

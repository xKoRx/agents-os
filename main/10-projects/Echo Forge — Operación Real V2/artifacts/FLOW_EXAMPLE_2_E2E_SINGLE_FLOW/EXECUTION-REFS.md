# EXECUTION-REFS — FLOW_EXAMPLE_2 E2E SINGLE FLOW (2026-10-16/17)

## Identidades

| Objeto | Ref |
|---|---|
| FlowRun CERTIFICADO (w9) | `8248f7fa-e3bd-45e4-b0de-66dcfcd564db` |
| WorkflowID root (w9) | `sqx-main-v1-b7f29b77-3e82-4ed7-baaa-fd3a35cd07d2` (run `01a14758-…`, Temporal `sqx-prop`) |
| cfgID (w9) | `NDX_flow_example_2_v1_w9` · request_id `flow-example-2-20261017T023000Z-e2e-w9` |
| FlowRun intento (w8, defecto corregido) | `c6a18689-59ab-4340-bd2d-b520c1dbfe8f` · wf `sqx-main-v1-44005b78-4926-4174-b815-b4b7eb87eb90` · FAILED en fidelity (post-MT5 30/30) |
| Reset de diagnóstico (w8) | run `63d29c7e-6181-4ab4-8ee2-81eadf437544` (probó el fix; sello bloqueado por transición terminal) |
| Repo | `xKoRx/symphony` master `69a6cd7` (fix `b77af11` + manifest 0.2.147) · baseline mandato `f30ed1d0` |
| Release | 0.2.147 linux SHA256 `0e4c9908fe428b65a60261a6a059ae43b6be984679d18e3e5cd140a8a18eb684` rollout 3/3 |

## Snapshots durables (w9)

| Snapshot | Ref |
|---|---|
| ClassificationSnapshot (`indicator_signature.v1`) | `sha256:161bfd25e20f04177b67fb2907588fc88e44b611ca22c105286354a89f6e50de` |
| RankingSnapshots early (weighted_combination_minmax.v1, PER_LOGICAL_TYPE) | 6 refs bajo `flow_run_ref=8248f7fa` (p.ej. `sha256:7f6fbccd…` RANGE_CLOSE,HIGH,LOW,OPEN_RANGE) |
| **SelectionSnapshot** | `sha256:d15af7f9b4572c1a3e947c2eb0ee460664513f82157d2627ff5f099d3d9964b4` (30 entradas, 729 exclusiones, policy_digest `sha256:2df2fe0c…`) |
| **RankingSnapshot FINAL** (`score_descending.v1`, top 100) | `sha256:de770a6d7a1618…` (ordered_entries 30: rank+score_ref+strategy_ref) |
| Scores fidelidad (`mt5_fidelity_shadow.v1`, mt5-score.v1) | 30 docs Mongo `forge.scores` created ≥ 2026-10-17T04:00Z, status COMPUTED |
| TradeSets SQX (tick_retest/optimized FULL) | Mongo `forge.trade_sets` flow `8248f7fa` + MinIO `durable/trade-list/v1/8248f7fa/` |
| MT5 exports | MinIO `durable/mt5-export/v1/8248f7fa/<uuid>` (30 keys) |
| Decisiones robust (30) | PG `sqx.decisions` OPTIMIZER_SELECTION SELECTED policy `wfm_robust_selection` (DecisionRefs sha256 en CSV) |
| Decisión promoción | PG `sqx.decisions` FLOW `finalist_promotion` 2.0.0 **STRUCTURAL_PROMOTED** 2026-10-17T04:17:09.095Z |
| Mágicas | PG `sqx.strategy_magic` 26100091054..26100091083 (30, asignadas 03:09-03:10Z) |
| Stage executions | PG `sqx.stage_executions` flow `8248f7fa`: overview 1/1, retester 30/30, optimizer 30/30, wfm 30/30, robust 30/30, apply 30/30, reretester 30/30, compile 30/30, mt5_backtest 30/30, baseline_materialize 30/30, promote_finalists 1/1 — **todas COMPLETED** |
| Estado terminal | PG `sqx.flow_runs` id `8248f7fa` **status=COMPLETED** (updated 04:17:11.877Z) |

## CFX del Owner (byte-exactos, sin modificación)

```
81497ababb8e632e58241e64f43c8d83ff3a31c5eafb43f908fcfde087cadf6a  builder_test.cfx
094f409e5395cb140fc67d4612477af93c4f37009204453b7fc15f6f9f0003d3  retester_test.cfx
a15124cbfc9cd9b86ca5f7d036aa94316320a921ecafd9a0d3936fbf9387761d  optimizer_test.cfx
420a4f88cd52628129f83027552e818aece5b8480e5fd57f49d378108d7b35af  retesterfull_test.cfx
```

Origen: `worker-kronos` → `C:\Users\KoR\Desktop\SQX144\user\configs\basetest` (copia verificada en `cfx/`).

## Infraestructura operacional usada

- Watcher candidate-local ÚNICO en Daedalus (screen `forge-watcher-w8`, binario recompilado `f30ed1d0` SHA `1c7ce032…`), `ENV=production`; ETCD `/sqx-watcher/production/`: namespace `sqx-prop`, cola `sqx-main-queue`, PG `trading_systems_test`.
- Flota: Zeus (28 cores, builder+group), Hera (64), Kronos (76) con sqcli 144 via `/home/echo-dev/bin/sqcli_worker.sh` (JVM 4g); Windows worker-kronos (`sqx-mt5-worker`, terminal64 serial) para MQ5/EX5/MT5.
- MinIO bucket `sqx-strategies` prefijos `wave_9/ndx/l_h1/flow_example_2/v1/` y `durable/…`; Mongo `forge`; PG `trading_systems_test` esquema `sqx`.

## Helpers efímeros de la sesión (fuera del repo)

`~/aranea/work/flow-example-2-e2e-20261016/tools/`: `sshrpc.sh` (SSH MCP por HTTP con auto-reinit de sesión), `mongorpc.sh` (ídem Mongo), `fe2q/` + `fe2q.bin` (lector PG raw con DSN desde ETCD, `--minio`, `--mongo`, `--reset` Temporal), `ssh_new_session.sh`. Ninguno pertenece al repo ni al vault.

## Cleanup pendiente al cierre

- Watcher `forge-watcher-w8` (screen en Daedalus): se detiene en la sesión de cierre.
- `input/` del watcher: vacío (paquetes w8/w9 en `processed/`).
- Sin sqcli/java residuales en la flota (verificado por última vez post-COMPLETED).

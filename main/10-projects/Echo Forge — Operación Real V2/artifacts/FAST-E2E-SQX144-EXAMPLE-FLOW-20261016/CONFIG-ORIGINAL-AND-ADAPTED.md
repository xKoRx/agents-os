# CONFIG-ORIGINAL-AND-ADAPTED — FAST E2E SQX144 EXAMPLE FLOW (2026-10-16)

## Fuente primaria (owner)

MinIO bucket `sqx-strategies`, prefix `wave_1/ndx/l_h1/example_flow/v1/` (ejecución histórica 2026-07-05/06).

SHA256 de los objetos descargados de `00_configs/`:

```
211aaee69374dad30055ccc59d01365faa1a31ddacaf2d33cd3dc4e69092a405  builder_test.cfx
5356269b0b8d7fbbdb02f825677d703ea25eaf44745c3452d7bef5a19e2ad771  job_config.json
8172ac875aa75d3bc6c5f5c9afd234dd8162919a01908948c62309d58223a460  optimizer_test.cfx
e8861998f5ddf5e583a99c2640dc713cca76371420214300c861d0e8cff5c3ab  retester_test.cfx
```

## Flujos reconstruidos

### Flujo original (job_config.json histórico)

`builder (01_builder, builder_test.cfx) → project SQXOverviewJsonExporter → classify_and_rank → group 02_retester batch 1 [retester_test.cfx, optimizer_test.cfx]`

Proyectos SQX de la época: `otro` (v142.2399), motor `MetaTrader4`, `XAUUSD_darwinex`, fechas 2016.01.04→2026.06.05.

### Evidencia física de la ejecución histórica

La estrategia `01_builder/NDX_L_H1_example_flow_v1_Strategy_2.1.14.z0.sqx` (SHA `d2bd3a393d7001e308e91e56eea75fa3264e7cbdc63175ca4c6090ea9420018f`) contiene `Results/Main: XAUUSD_darwinex_LOM_H1/`, `lastSettings.xml` con `<Chart symbol="XAUUSD_darwinex" timeframe="H1">` y fechas 2016.01.04→2026.06.05. **La ejecución histórica fue XAUUSD H1; el prefijo de nombre `NDX_L_H1` provenía sólo del metadata del job, no de los CFX.** No existen CFX NDX de esa ejecución.

### Datasets NDX reales presentes en la flota 144 (verificados en Zeus data.db ID/144)

- `NDXm_darwinex_tick_UTC02` (TICK, source 4, 2023-06→2026-10) — el par usado por `reretesterfull` y MT5 `NDX_SQX` (pareja de fidelidad certificada 2026-10-16, PRODUCTION_PASS).
- `USATECHIDXUSD_dukascopy_UTC02` (M1, source 2, 2015-01→2026-10) — proxy NDX dukascopy; adaptación dirigida por el owner el 2026-10-16 para los CFX de campaña (probes 3/3 PASS).
- `USATECHIDXUSD{,_darwinex,_dukascopy}` portados a los 3 hosts (filas DATA 213/214, backup `data.db.bak-20261016-precfix`).

## Config nueva (FAST E2E)

Spec: `spec/flow-fast-e2e-144.json` (SPEC_VALID, tasks=12). Identidad nueva aislada: `NDX_example_flow_fast_v1_w1` → prefix MinIO `wave_1/ndx/l_h1/example_flow_fast/v1/`. Magic apply `888333`.

Cadena (superset moderno del flujo original; mandates FASE 3): builder → overview_exporter → group precision (RetestPrecision_144) → classification indicator_signature.v1 → early ranking weighted_combination_minmax.v1 (40/30/30, PER_LOGICAL_TYPE top5) → selection per_logical_type top2 → group full (RetestFull_144) → group optimizer (Optimizer_144 + evaluate_wfm + select_robust robust_run_selection_v2 0.35/0.01/0.01) → apply (magic 888333) → final reretester (reretesterfull_144 NDXm tick) → trade_list → MQ5 → EX5 → MT5 backtest (NDX_SQX H1 2025.07.01→2026.10.09 model 4) → fidelity mt5_fidelity_shadow.v1 → ranking score_descending.v1 → promotion finalist_promotion @1.0.0.

## CFX utilizados y deltas

| CFX | SHA256 | Origen | Delta |
|---|---|---|---|
| `Build_BR_G1_H1_144_fast.cfx` | `2052c5487041cb17d8e61e6efbf9076d458f0b99c28916c5d7dc210da3b8f0b0` | `Build_BR_G1_H1_144.cfx` (`507507c5…`, adaptación certificada 2026-10-16, probes builder Zeus PASS) | Único delta: `<StopCondition type="databank-full" passedStrategies="750"→"24" restartCount="5"→"0">`. Causa: presupuesto 20–30 estrategias. |
| `RetestPrecision_144.cfx` | `2cd587f0bb15dd7f5d854f69e39ae30dcf1ee7539d561efc2a9f87ea379a7f9e` | idéntico al adaptado certificado 3/3 probes | ninguno |
| `RetestFull_144.cfx` | `14d55e9879fcfec718d4c97b3f6b83d1e6eda59d83d49d27ffffc0ee16a83389` | idéntico | ninguno |
| `Optimizer_144.cfx` | `d4d9c0aa5123fd8792b0d1654bf7d63e9a96d00a29c0fc45c0b561f6b678b988` | idéntico | ninguno |
| `reretesterfull_144.cfx` | `a51c1cc32d576281d965f307cb1ad84038a31604b838c9549365a987536bafb3` | idéntico (NDXm_darwinex_tick_UTC02 nativo) | ninguno |

### Causa demostrada de la adaptación (no automática)

1. Los CFX del example flow histórico son plantillas XAUUSD MT4 (v142): probado físicamente en el `.sqx` y en los XML extraídos (`extracted/`).
2. Esos bloques `<Resources><Symbols>` (darwinex source 2 XAUUSD) no resuelven en SQX 144 (causa raíz diagnosticada 2026-10-16: "Project has unresolved resources"); el `<Chart symbol>` es lo que resuelve datos.
3. El owner fijó NDX Long H1 para esta prueba; los únicos datasets NDX físicos de la flota 144 son `NDXm_darwinex_tick_UTC02` (tick: inviable para builder/optimizer en 20–30 min) y la familia `USATECHIDXUSD` M1 (dukascopy UTC02, dirigida por el owner para las adaptaciones del día).
4. Delta mínimo aplicado: un CFX nuevo (builder) con un atributo cambiado; los otros 4 CFX reutilizados byte-exactos de las adaptaciones certificadas del mismo día.

## Parámetros Fast

- Builder: `databank-full passedStrategies=24` (objetivo ≈20–30 estrategias).
- Selección: `per_logical_type top_n=2` (límite absoluto 5; presupuesto 1–3 por tipo).
- Ranking final: `score_descending.v1` top_n=20 GLOBAL (semántica global preservada; la selección final por tipo se entrega como proyección exacta por pertenencia + score, sin recalcular Fidelity).
- Umbral WFM/Robust congelado: `robust_run_selection_v2` cliff 0.35 / epsilon_ret 0.01 / epsilon_aux 0.01 (sin cambios).

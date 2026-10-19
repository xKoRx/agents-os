# MT5-FIDELITY-AND-MAGIC — w11 (2026-10-19)

## MagicNumber 64-bit (cadena completa)

- Allocator sin tocar: 35 mágicas int64 asignadas en `sqx.strategy_magic` (assigned_at hoy), rango **26100091104–26100091138** — continuación exacta de la secuencia w10 (…082–103). Valores > 2^31: ejercitan el camino 64-bit end-to-end.
- MQ5 durable: `input long MagicNumber` por estrategia (fix `d67244b` incluido en 0.3.2 por lineage).
- Readback HTM: el scope del metric set MT5 registra los inputs efectivos del HTM con `MagicNumber = 26100091129` (muestra, estrategia 055b1e71) — **mágica efectiva MT5 == durable**.
- Gate `mt5_reconcile_v1` (fail-closed, corre ANTES de cada backtest): 35/35 backtests ejecutados ⇒ 35/35 reconciles sin CONTRACT_CONFLICT.
- Sin colisiones: 35 mágicas únicas; sin reuso de w10.

## Backtests MT5

- 35/35 ejecutados (100% de los finalistas que alcanzaron la etapa), real ticks ("100% real ticks", 72,2M ticks, 4593 barras por corrida típica), NDX_SQX H1 2026.01.01→2026.10.12, deposit 100000 USD, leverage 1:100, Darwinex-Demo, terminal build 6230, modelo 4.
- Artefactos físicos por estrategia en `durable/mt5-export/v1/561267ed…/<uuid>/13_mt5_backtest/`: HTM (40 KB), tester.log (~4,2 MB), agent.log (~5,5 MB), terminal.log, tester.ini, tradeset ndjson.gz.

## Condiciones de negocio (w11)

| Grupo | N | Detalle |
|---|---|---|
| Con trades MT5 > 0 | **14/35 (40%)** | trades 3–1732; detalle abajo |
| Sin trades MT5 (0 ejecutadas) | **21/35 (60%)** | mismo mecanismo físico documentado (forense 2026-10-17): SL fijo → lote resultante > margen del depósito 100k; el EA rechaza el 100% de señales. NO se modificó Money Management (mandato §4) — no es fallo del runtime |
| Rentables MT5 (net > 0) | **1/14** | 3 trades, +459,22 USD, PF 4,55 |
| No rentables con trades | 13/14 | net −1.993 a −62.517 |

- Fidelidad: 35/35 scores `mt5_fidelity_shadow.v1` COMPUTED (fórmula intacta), valores 18,99–87,12. La comparación SQX↔MT5 es informativa; la evaluación de calidad/rentabilidad es trabajo del owner, no de esta certificación.
- Contraste con w10: 6/22 con trades (27%) → 14/35 (40%); cohort distinto (846 vs 649 generadas; 7-8 tipos). Sin ajustes de Strategy/MM para explicar o mejorar el resultado.

## PRE_ECHO (egreso fail-closed)

- 35/35 `handoff_deliveries` en `HANDOFF_CREATED`; `last_error="echo ingest base url / bearer not configured: ingress_not_configured"` — fail-closed ANTES de HTTP: 0 POSTs, 0 ingestiones, 0 deployments, 0 órdenes. Sin configuración de ingreso Echo en esta prueba (verificado en preflight).

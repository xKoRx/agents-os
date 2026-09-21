# Handoff S02 E3 — STOP fee_source_discrepancy

Para el responsable de consolidación Five-POC. No reabrir U-02. No editar esta nota como plan del padre ni de la guía operativa. Incorporar a Agents-OS cuando el consolidator toque continuidad/wiki; esta sesión no editó esas notas.

**Exit:** `IMPLEMENTATION_BLOCKED` · **no** NO_GO global · E3 **no abierto**

| Campo | Valor |
|---|---|
| Diagnóstico | `fee_source_discrepancy` compara Gamma/CLOB `maker/taker base_fee=1000` bps (tope CLOB) con Market WS `last_trade.fee_rate_bps=0` (feeRate de la orden/trade). No son la misma magnitud. |
| Evidencia E2 | 17/17 `last_trade_price` con fee `"0"` (BUY y SELL). Case 3 sin trade ya da INTERVAL `[0,1000]`; Case 2 con trade `0` pasa a SUSPECT. |
| Gamma vivo | MLB E2 + 2284198: `sports_fees_v3`/`v2`, `takerOnly:true`, curva 0.05/0.03; `feeType`/`feeSchedule` son `unknown_fields` del parser. |
| U-02 | `V2_CASH_CONFIRMED`, `REAL_FEE_READY=false`. No se usó como baseline. No mergear `d5ce263`. |
| Código | no implementado. Integración `85e27ff` leída, no escrita. Master del integrador no tocado (`a770da6` al diagnosticar). |
| E3 | sin journal, sin SCREEN/REPLAY/SHADOW. T−90 de 4584879 = `2026-09-21T21:05:00Z` queda pendiente de autorización de modelo. |
| Bundle | `polymarket-engine-datasets/pe005-r1-e3-20260921/` (`REPORT.md`, `STOP.json`, `MANIFEST.json`) |

Cambio propuesto (no ejecutado): Case 2 → INTERVAL si observado ∈ `[0, max(declared)]`; Detect de spread no exige POINT de fee; ingestión de `feeType`/`feeSchedule` aparte.

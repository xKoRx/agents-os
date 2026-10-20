# POSITIVE-CONTROLS — MT5 Zero Trades Forensics (2026-10-17)

## Selección

Cuatro controles positivos elegidos donde coexisten con cero-traders del mismo árbol lógico: C13 (`2f9c89cd`, rank 13, `RANGE_CLOSE,HIGH,LOW,OPEN_RANGE` — el único tipo 0/5 en fallar), C14 (`4c030499`, rank 14, `RANGE_CLOSE_RANGE` — el único operante de su tipo), C7 (`60248582`, rank 7, `RANGE_CLOSE,HIGH,LOW_RANGE` — mismo tipo que Z23), C1 (`b98f0c1a`, rank 1, `RANGE_CLOSE,LOW,OPEN_RANGE` — mismo tipo que Z19). Mismo FlowRun, mismo símbolo, mismas fechas, mismo terminal (worker-kronos, `C:\MT5\slots\slot-1`), mismos CFX.

## Comparación determinante

| Variable | 16 sin trades | C7 | C13 | C14 | C1 |
|---|---|---|---|---|---|
| SL fijo del robust run (MQ5 `sqGetSLLevel`) | **21.0 pips (los 16)** | 28.0 | 25.5 | 25.5 | ATR-based (no fijo) |
| `Max 1 lot trade drawdown` (tester.log) | 21.00 USD | 28.00 | 25.00–26.00 | 25.00–26.00 | 4542–6133 USD |
| Lote pedido (`Unfiltered Computed Lot Size`) | **9.5 constante** | 7.1 | 7.6–8.0 | 7.6 | 0.0→min 0.1 |
| Señales (`Computing MM for order`) | 312–4471 | 1690 | 4073 | 4593 | 115 |
| `Not enough money` (rechazos) | **= señales (100%)** | 1385 | 3843 | 4377 | 0 |
| Deals ejecutados | **0** | 464 | 256 | 174 | 220 |
| Rango de precios de sus deals | — | 22 954–25 865 | 22 881–25 813 | 22 883–25 562 | 23 163–31 291 |
| Balance final | 100000.00 | 83 513.80 | 90 236.40 | 87 764.00 | 99 053.94 |
| Retcodes ≠ 0 del send | 0 (no llega a enviar) | 10016 ×14 | 10016 ×3 | 10016 ×7 | 0 |

## Lectura

1. **Mismo entorno, mismo comportamiento de inicialización, mismas dependencias, misma lógica de export** — los controles descartan cualquier problema general de entorno, datos, compilación o dependencias. El único discriminador físico entre operar y no operar es el par (SL del robust run → lote pedido) contra el margen disponible.
2. **Aritmética del umbral:** con contract 10 y margen ≈4.2–5.6%, el lote máximo asequible a precio P es ≈ 200 000 / P (con 100k libres y rate 5%). A precio mínimo 2026 (~22 880): máx ≈ 8.74 lotes. El lote 9.5 de las 16 excede el máximo **en todo el período** (el NDX nunca cotizó bajo 21 052); el lote 7.1–8.0 de C7/C13/C14 cupo sólo mientras el precio y el margen libre lo permitieron (por eso acumulan miles de rechazos y su rango de deals termina en ~25.9k, y C13 no pudo operar 8.0 lotes más que con margen libre inflado por PnL flotante).
3. **C1 es el contracontrol de la aritmética:** su SL ATR-based (miles de pips) produce lote 0.1 → margen trivial → 100% de sus 115 señales ejecutadas (220 deals) durante todo el año hasta 31k de precio. Confirma que el bloqueo escala exactamente con lote × precio × contract × rate.
4. **Los controles también están degradados:** ejecutan 6–27% de sus señales y su PnL MT5 (todos negativos) se produce con SLs de 2.5–4.5 unidades contra spread real — la semántica temporal del trade (duración, MFE/MAE, excitación por spread) no es comparable a SQX. El patrón "14 con trades pero todos negativos" es la forma parcial del mismo defecto que en las 16 es total.
5. Los rechazos secundarios `RetCode 10016 (invalid stops)` de los controles (3–14 casos) son congruentes con SL/TP a 2.5–2.8 unidades contra `SYMBOL_TRADES_STOP_LEVEL` del símbolo en momentos puntuales; no afectan la conclusión.

# CLF-Q03 — CENSUS RECONCILIATION (FASE 3)

Fecha: 2026-10-25 · Ejecutor: manager ZCode (GLM-5.3-Flash) · Rama `experiment/clutifx-s01` @ `c127b894`
Fuentes: recibos físicos `~/echo-work/clutifx-backtest/{qualification/out-g2,out-g3,out-g4}` (ciclo previo) y `~/echo-work/clutifx-backtest/q02/{G2,G3,G4,receipts}` (Q02). Censo máquina: `q03/census/physical-attempts.json`.

## 1. Método

Dos contabilidades independientes producidas desde los recibos físicos (result.json + economic.ndjson.gz + cash_events por intento), sin heredar cifras de reportes previos:

- **Censo físico**: todo intento con `result.json` COMPLETE+reconciled; compras = `len(accounts)` por intento; señales/rechazos correlacionados por `SignalID` desde los records `SIGNAL` y `OPERATION_APPLY/CAMPAIGN_SIGNAL` de la traza.
- **Censo de investigación**: identidades únicas del catálogo 34-ID (matriz CLUTIFX), deduplicando equivalencias de señal demostradas (jamás por P&L igual).

## 2. Censo físico — 24 campañas G4 ejecutadas

| ciclo | identidad | compras | pases | pérdidas | pendientes | señales OPEN | ops | fills | rech. sesión (por SignalID) | estado |
|---|---|---|---|---|---|---|---|---|---|---|
| previo | C02 | 1 | 0 | 0 | 1 | 9 | 3 | 6 | 4 | COMPLETE+rec |
| previo | C06 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | COMPLETE+rec (0 señales genuinas) |
| previo | S01 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 4 | COMPLETE+rec |
| previo | S02 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 4 | COMPLETE+rec |
| previo | S09 | 1 | 0 | 0 | 1 | 9 | 3 | 6 | 4 | COMPLETE+rec |
| previo | S10 | 1 | 0 | 0 | 1 | 17 | 4 | 6 | 11 | COMPLETE+rec |
| previo | S16 | 1 | 0 | 0 | 1 | 5 | 2 | 4 | 3 | COMPLETE+rec |
| previo | S17 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 4 | COMPLETE+rec |
| previo | S20 | 1 | 0 | 0 | 1 | 16 | 3 | 6 | 10 | COMPLETE+rec |
| Q02 | C07 | 1 | 0 | 0 | 1 | 9 | 3 | 3 | 4 | COMPLETE+rec |
| Q02 | S03 | 1 | 0 | 0 | 1 | 9 | 3 | 3 | 4 | COMPLETE+rec |
| Q02 | S04 | 1 | 0 | 0 | 1 | 9 | 3 | 3 | 4 | COMPLETE+rec |
| Q02 | S05A | 1 | 0 | 0 | 1 | 9 | 3 | 3 | 4 | COMPLETE+rec |
| Q02 | S05B | 1 | 0 | 0 | 1 | 9 | 3 | 3 | 4 | COMPLETE+rec |
| Q02 | S06 | 1 | 0 | 0 | 1 | 12 | 7 | 6 | 5 | COMPLETE+rec |
| Q02 | S07 | 1 | 0 | 0 | 1 | 10 | 3 | 3 | 6 | COMPLETE+rec |
| Q02 | S11 | 1 | 0 | 0 | 1 | 8 | 2 | 2 | 4 | COMPLETE+rec |
| Q02 | S12 (=C05) | 1 | 0 | 0 | 1 | 9 | 3 | 2 | 6 | COMPLETE+rec |
| Q02 | S13 | 1 | 0 | 0 | 1 | 9 | 4 | 1 | 5 | COMPLETE+rec |
| Q02 | S15 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | COMPLETE+rec (0 señales) |
| Q02 | S19 | 1 | 0 | 0 | 1 | 9 | 3 | 3 | 4 | COMPLETE+rec |
| Q02 | S21 | 1 | 0 | 0 | 1 | 9 | 3 | 3 | 4 | COMPLETE+rec |
| Q02 | **T01** | **1** | 0 | 0 | 1 | 10 | 3 | 3 | 6 | COMPLETE+rec (neto −1.089,94; compra 120 + renovación 120) |
| Q02 | T04 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | COMPLETE+rec (0 señales) |

**Totales físicos: 24 campañas (15 Q02 + 9 previas), 18 compras (13 Q02 + 5 previas), 0 pases, 0 pérdidas duras, 13 cuentas pendientes, 6 campañas con 0 compras (S15/T04/C06/S01/S02/S17).**

## 3. Reconciliación de las cuatro cifras en conflicto

| Cifra nominal | Valor | Veredicto del censo |
|---|---|---|
| 9 campañas previas + 15 Q02 = 24 ejecuciones nominales | 24 | **CUADRA**: 24 intentos G4 con `result.json` COMPLETE+reconciled (9 en `qualification/out-g4`, 15 en `q02/G4`). Ninguna ejecución fantasma, ninguna oculta. |
| 23 identidades con campañas propias | 24 ejecuciones | **CUADRA con alias**: las 24 ejecuciones corresponden a 23 identidades de catálogo con campaña propia porque `S12` ejecuta el slot `C05` (`CLF-VAR-S12 (=C05)`, refinado 15m declarado en la matriz como misma identidad experimental; equivalencia por identidad declarada, no por P&L). |
| 5 compras previas + 13 Q02 = 18 compras nominales | 18 | **CUADRA**: 13 compras Q02 (12 con fila en el CSV Q02 **+ T01**) + 5 previas. Cada compra está respaldada por `accounts`+`cash_events` (`PURCHASE` 120 USD; T01 además `RENEWAL` 120 USD) y cuenta `pending` en su recibo. |
| 17 compras acumuladas reportadas | 18 | **El reporte Q02 quedó corto por 1**: `CLF-Q02-G4-QUARTER-ECONOMICS.csv` omite la fila **T01** pese a existir su ejecución física completa (`q02/G4/out-Q02-T01-G4`, COMPLETE+reconciled, neto −1.089,94, terminal pendiente). Es un defecto de reporting puro del artefacto CSV; el recibo físico siempre estuvo íntegro. Q03 corrige el CSV (la fila T01 ya está en §2). |

**Hipótesis C02≡S09 (deduplicación de compras): DESCARTADA como deduplicación física.** C02 y S09 fueron **dos ejecuciones físicas separadas** (`out-CLF-C02-G4` y `out-CLF-S09-G4`, intentos y recibos propios, cada una compró su propia cuenta simulada). La equivalencia es de **señal**: 9/9 señales OPEN idénticas (mismos instantes, dirección y stops) y 6/6 fills idénticos al nanosegundo (RCA Q02 §2, verificado de nuevo en este censo: ambas 9 señales/6 fills/4 rechazos de sesión con los mismos SignalID). Consecuencia aplicando las reglas: **ninguna compra se elimina del censo físico** (18 se mantiene); **el censo de investigación cuenta un solo voto de familia** para el par y S09 queda como alias de ejecución NQU6 (en otro trimestre pueden divergir). S20 vs C02 sí es identidad distinta (16 señales = las 9 de C02 + 7 que C02 absorbió por red flags), con su propia compra.

## 4. Correlación de rechazos por SignalID (no por razón predominante del día)

Producido por el gate `STRATEGY_SESSION_COMPATIBILITY` (Q03 FASE 2) sobre las trazas G4; detalle por señal en `q03/session-compatibility/STRATEGY_SESSION_COMPATIBILITY-<ident>-G4.json`:

| identidad | señales | en ventana | fuera de ventana | rechazadas por sesión | clasificación |
|---|---|---|---|---|---|
| C02 | 9 | 3 | 6 | 4 | SESSION_COMPATIBLE |
| C06 | 0 | 0 | 0 | 0 | INCONCLUSIVE_NO_SIGNALS |
| S01 | 4 | 0 | 4 | 4 | **SESSION_INCOMPATIBLE** |
| S02 | 4 | 0 | 4 | 4 | **SESSION_INCOMPATIBLE** |
| S09 | 9 | 3 | 6 | 4 | SESSION_COMPATIBLE |
| S10 | 17 | 4 | 13 | 11 | SESSION_COMPATIBLE |
| S16 | 5 | 2 | 3 | 3 | SESSION_COMPATIBLE |
| S17 | 4 | 0 | 4 | 4 | **SESSION_INCOMPATIBLE** |
| S20 | 16 | 3 | 13 | 10 | SESSION_COMPATIBLE |
| Q02 (15 identidades) | ver JSON por identidad | — | — | 4–6 c/u con señales | `q03/session-compatibility/*.json` |

Lectura: el rechazo dominante es `CAMPAIGN_SESSION_ENTRY_WINDOW`/`SAFETY_CUTOFF` (legítimo, E2T 09:30–15:55 ET), pero **no es el único**: S13 registra `SIZE_BELOW_MIN_CONTRACT`, S07 `CAMPAIGN_SESSION_NON_BUSINESS_DAY`, y los conteos por señal difieren de los conteos por día (p. ej. C02: 6 señales fuera de ventana, 4 rechazadas por sesión — las otras 2 fueron absorbidas por otras guardas). El conteo por "razón predominante del día" habría seguido ocultando esa diferencia.

## 5. Censo de investigación — matriz 34-ID (estado al inicio de Q03)

| categoría | IDs | conteo |
|---|---|---|
| Implementadas con campaña propia | C02, S01, S02, S09, S10, S16, S17, S20, C06, S03, S04, S05A, S05B, S06, S07, S11, S12(=C05), S13, C07, S19, S21, S15, T04, T01 | 24 ejecuciones → **23 identidades de catálogo** |
| Alias sin corrida propia (equivalencia demostrada/declarada) | S14≡C06 (config-idéntica), S18≡C02 (max_reemissions 0 = base), C05≡S12 | 3 |
| No implementadas | **C01 (STR-001), C03 (STR-003), C04 (STR-004)**, S08 (depende C03), T03 (depende C04) | 5 |
| BLOCKED_SPEC | T02 (sin ancho de stop declarado en la fuente) | 1 |
| BLOCKED_DATA | STR-007/C08 (SMT sin segundo instrumento), STR-008/C08 (noticias sin calendario), T05 (noticias×TS) | 3 |

Reglas verificadas: ninguna compra eliminada por deduplicar (18 físicas se mantienen); ninguna ejecución contada dos veces (24 intentos, 24 filas); MM constante (SG-R500) no infló familias (familias por `signal_family_id`: FAM-002 y FAM-006); equivalencias declaradas por señal/config demostrada, jamás por P&L igual (C02 y S20 tienen +335,08 pero son identidades distintas; C02≡S09 se probó por señales y fills).

## 6. Consecuencia para Q03

1. El CSV de economía Q03 incluye T01 y cualquier identidad nueva (sin omisiones de reporting).
2. S01/S02/S17 quedan clasificadas `SESSION_INCOMPATIBLE` con la evidencia ya existente en sus trazas — sin G4 adicional.
3. Q03 implementa las tres bases restantes (STR-001/003/004); S08 y T03 quedan declaradas como variantes cuyo bloqueo de dependencia queda resuelto por C03/C04 pero que exigen su propio G0–G4 en un ciclo posterior (presupuesto de este mandato agotado en las bases).

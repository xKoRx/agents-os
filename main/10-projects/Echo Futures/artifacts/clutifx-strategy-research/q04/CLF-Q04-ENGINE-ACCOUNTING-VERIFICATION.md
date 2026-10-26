# CLF-Q04 — ENGINE & ACCOUNTING VERIFICATION (FASE 6)

Alcance: 27 campañas físicas NQU6 (19 con compra + 8 sin compra). Método: reconstrucción independiente desde `economic.ndjson.gz` + `result.json` sellados (script `q04/census_q04.py`, `q04/verify_q04.py`); sin re-ejecuciones.

## Resultado del sweep (script, reproducible)

| Check | Resultado |
|---|---|
| Eventos `CHALLENGE_PASS` en streams/cash_events | **0 en las 27** (cero pases perdidos por reporting) |
| `first_pass_at` / `ruin_at` | valor cero en las 27 |
| `reconciled` | `True` en las 27 |
| Cuentas por campaña | 1 (sin duplicaciones de cuenta) |
| Fills duplicados | 0 (cada round-trip reconstruido posición-a-posición desde fills; 54 en NQU6) |
| Flat checks de sesión | completos: 56/56 (compra temprana) y 26/26 (S07/S11/T01 compra tardía); `RESEARCH_DAILY_CLOSE_V1` |
| `stage_net` (engine) vs P&L fill-a-fill (auditor) | igualdad exacta 19/19 (ej. C02 +335,08; S10 +1.325,06; S06 −594,82; T01 −1.089,94) |
| Fees | $2,49/contrato/lado aplicados uniformemente (verificado en cada round-trip) |
| Slippage | 1 tick en entradas market (verificado contra `slippage_ticks=1` del plan sellado) |
| Compras/renovaciones | uniformes: PURCHASE $120 + RENEWAL $120 cada 30d calendario; 19+35 = 54 eventos = $6.480 |
| Target/DD/días | target $3.000 (`terms.evaluation_target`, todos los planes); DD $2.000 EOD (`rule_set_catalog[0]`); `minimum_traded_days=0` |
| Piso EOD vs equity | ninguna cuenta por debajo del piso en ningún día |
| MM interna | pausa −$1.000/día y meta $870 sin bloqueos observados; rechazos de tamaño `SIZE_BELOW_MIN_CONTRACT` correctos por diseño (ATR×$20 > $500 ⇒ q=0): S13×2, S10×1, S12×1 (NQU6) |

## Timelines testigo (detalle completo en ACCOUNT-TIMELINES)

- **S10**: compra 06-23 17:00Z → W +420,02 (06-23) → W +440,02 (06-26 15:00 ET) → admisión 08-26 14:00 ET muerta en MM (`SIZE_BELOW_MIN_CONTRACT`) → W +465,02 (08-28). Final +1.325,06 (44,2% del target). Sin pérdida: DD jamás amenazado. Causa única de no-pase: deficit $1.674,94 vs target.
- **C03**: compra 06-23 → W +420,02 (06-23) → W +375,02 (08-06). Pico +795,04 (26,5%), cuenta pendiente al horizonte. Consistente con Q03.
- **C02** (control): W +420,02 → W +375,02 → L −459,96 (08-26, qty=2, stop +1 tick de slippage). Final +335,08. Equity: 50.000 → 50.795,04 → 50.335,08. Floor 48.795,04 nunca cercano.
- **S06**: 7 admisiones → 6 rt (2W/4L, −594,82); peor drawdown de la cohorte sin tocar el piso; 1 compra + 2 renovaciones.
- **T01**: 3L seguidas (−374,98 / −424,98 / −289,98) = −1.089,94; sin ruina (límite $2.000); compra tardía 08-06.
- **Variante con rechazo de sesión (C01)**: 1 emisión @01:00 ET 06-23, rechazada `CAMPAIGN_UNAVAILABLE|SESSION_ENTRY_WINDOW` antes de comprar — el guard funcionó; wallet sin compra.

## Defectos económicos

**Ninguno demostrado.** La aparente discrepancia "compra $120 vs `profile.provider_fee $50`" es configuración declarada del Owner (`campaign.go`: `PurchaseCost // 120 USD ON_DEMAND`, knobs = FUNCTIONAL_ASSUMPTIONS): decisión de costeo, no bug; no afecta pases. Cero campañas invalidadas; cero cambios de código en este shot (no hubo rojo→verde porque no hubo defecto reproducido — el gate 14 del mandato queda vacío por la razón correcta).

## Control de defecto común con R03 (FASE 8, resumido)

El mismo motor+reglas con horizonte que incluye NQU6 registra 233 pases en 1.839 compras SG (12,7%); 24 configuraciones con pases solapando la ventana NQU6 (hasta 2026-10-02). El simulador y la cuenta no bloquean pases; la diferencia es frecuencia de entrada (R03 0,1–2,4/día vs ClutiFX 0,02–0,10/día). **No se ejecutaron controles trimestrales nuevos** (la evidencia existente resuelve la pregunta; presupuesto de motores nuevos usado: 0).

# CLF-Q04 — ECONOMIC ROOT CAUSE: WHY ZERO CHALLENGES PASSED

Fecha: 2026-10-26 · Mandato: GOD FORENSIC AUDIT · ONE-SHOT · `OWNER_ACCEPTANCE: REVIEW`
Ejecutor: ZCode (GLM-5.3-Flash) · Fuente: `xKoRx/echo` rama `experiment/clutifx-s01` @ `e8c2e47e` (worktree `~/go/src/github.com/xKoRx/echo-clf`, árbol limpio, WIP preservado intacto)
Método: reconstrucción forense desde recibos sellados (`~/echo-work/clutifx-backtest/{qualification,q02,q03,q03r1}/`), cero re-ejecuciones de motor, cero campañas nuevas, cero históricos.

---

## 1. RESPUESTA DIRECTA

**Ninguna campaña ClutiFX aprobó porque el desafío era matemáticamente inalcanzable con la actividad que las estrategias observaron, no porque las operaciones perdieran ni porque el simulador fallara.**

La cadena causal, cada eslabón medido sobre recibos sellados:

1. **El objetivo del challenge es US$3.000** (`evaluation_target` en TODOS los planes sellados; programa E2T/GAU50 fase EVALUATION; verificado, no asumido). Sin regla de consistencia y sin días mínimos (`minimum_traded_days: 0`).
2. **La geometría ejecutada produce ganadores netos de $275–465**, no $500: el presupuesto bruto de $500 con ratio 1:1 y ATR14-Wilder M1 ×1 dimensiona `q = floor(500 / (ATR_puntos × $20))`; con ATR típico 16–24 puntos esto da `q=1–3` contratos con riesgo real $325–465 y `budget_unused` $35–175 (evidencia literal `MM_EVALUATION.sizing`: `distance_ticks=65, planned_gross_risk=325, budget_unused=175`). El mejor ganador neto del corpus completo es **+$465,02** (S10, 2026-08-28, ya descontando fees $2,49/lado y slippage de 1 tick).
3. **Para alcanzar $3.000 se necesitan ≥7 ganadores netos seguidos sin una sola pérdida** (`ceil(3000/465.02) = 7`); a la tasa de acierto observada de la familia (67%), ≈10–12 ejecuciones.
4. **La frecuencia observada fue de 2–6 operaciones por cuenta en el trimestre completo (60 sesiones elegibles)**: la fuente del curso ancla las señales en las velas de las 21/17/1/5/9 ET (estructura fiel del curso), la ventana operable de la cuenta E2T es `[09:30, 15:55)` ET, y **sólo la vela de las 13:00 ET sobrevive** para la familia STR-002 de ancla 4h. De 9 emisiones del trimestre, 6 se rechazan por sesión (`SESSION_ENTRY_WINDOW`/`SESSION_SAFETY_CUTOFF`) y entran 3.
5. **Resultado: 19/19 campañas `MATHEMATICALLY_UNREACHABLE_WITH_OBSERVED_TRADES`** — incluso si TODAS las operaciones ejecutadas hubieran sido el mejor ganador del corpus, el máximo alcanzable habría sido $2.790,12 (S06, 6 operaciones) < $3.000. El progreso máximo real fue +$1.325,06 = 44,2% del objetivo (S10, 3/3 ganadoras) y la mediana del resto fue 26,5%.

**No es `NEGATIVE_STRATEGY_EXPECTANCY`:** 13 de 19 campañas cerraron neto positivo; la familia maestra con 66,7% de acierto y expectancia +$112/operación. La expectancia no alcanzó a manifestarse porque la muestra por cuenta fue de 2–6 tiradas contra un objetivo que exige 7 aciertos consecutivos.

## 2. Atribución no exclusiva (proporciones sobre las 19)

| Causa | Campañas afectadas | Rol |
|---|---|---|
| A. Frecuencia insuficiente | 19/19 | Co-dominante: 2–6 ejecuciones contra ≥7 ganadores requeridos; sequías de 44–64 días |
| B. Geometría/riesgo vs objetivo | 19/19 | Co-dominante: ganador techo $465 < target/7; q=0 (`SIZE_BELOW_MIN_CONTRACT`) cuando ATR×$20 > $500 (8 señales admitidas muertas: S13×2, S10×1, S12×1, más 5 en NQZ6) |
| C. Operaciones perdedoras | 5/19 (S06, T01, S13, S11, S16 neto negativo) | Secundario: incluso todas-ganadoras no alcanzaba |
| D. Sesión/cuenta | 5/19 estructural (C01, C04, S01, S02, S17: nunca compradas, 100% emisiones fuera de ventana) + atrición de funnel en las 19 operadas | Co-dominante en las no-compradas; causal de la baja frecuencia en las compradas |
| E. Adaptación curso→NQ | 0 defectos demostrados en código; el mismatch curso-vs-ventana-E2T es una decisión de política (KRR-001/002/004) | Pendiente Owner |
| F. Defectos de implementación | 0 en el camino económico; 1 conjunción FS más estricta que la lectura simple del fuente (KRR-003, requiere video) | Sin fix sin evidencia fuente |
| G. Defectos del simulador | 0 | FASE 6: 0 anomalías en 27 campañas; control R03: 233 pases en el mismo motor, 24 configuraciones con pases DENTRO de la ventana NQU6 |
| H. Evidencia insuficiente | KRR-003 (rareza FS), KRR-004 (instante de emisión TS), KRR-005 (ancho stop T02) | Video review Owner |

Las categorías se solapan por diseño (frecuencia × geometría son conjuntas); no suman 100%.

## 3. Censo económico exacto (FASE 1)

Reconstruido independientemente desde los streams `economic.ndjson.gz` sellados (no desde los CSV previos):

- **19 campañas trimestrales con compra** (NQU6, 60 sesiones, 2026-06-14→2026-09-13): 1 cuenta por campaña, compras perezosas al primer entry (`CONTINUOUS_V1`, ventana de compra `NY_RTH_0930`).
- **54 round-trips NQU6 = 32W / 22L**, reconciliados fill-a-fill contra el equity del engine (diferencia 0,00 en las 19).
- **54 eventos de cash = 19 PURCHASE + 35 RENEWAL, todos a $120** → **$6.480 de costo modelado** de investigación. NO son 54 cuentas compradas: son 19 cuentas + 35 renovaciones cada 30 días calendario.
- **Corrección de atribución 54/69 (gate 10 del mandato): RESUELTA.** Los 54 round-trips pertenecen a NQU6 (las campañas del trimestre). Los **69** son los round-trips del smoke G2 sobre **NQZ6** (último contrato, 9 sesiones operadas: 40 de la familia maestra ×4 + S06 ×6 + S07/S11/S16/T01 ×3 + S12 ×5 + S13 ×4 + C03/S10 ×1 = 69). El reporte Q03R1 nunca atribuyó 54 a NQZ6: su CSV de last-contract suma 69 y su CSV G4 suma 54; la revisión externa mezcló los dos archivos. Verificado byte-a-byte.
- Equity: inicio $50.000/cuenta; pico máximo de progreso +$1.325,06 (S10); medianas +$795,04 (familia maestra, 26,5%).
- Wallet de investigación: $5.000 por campaña; `cash_final` $4.640–4.760 según renovaciones.

## 4. S10 — el testigo (mandato 2.4, explicación exacta)

S10 (setup 1h, SG-R500) compró 1 cuenta, ejecutó **3 operaciones y las 3 fueron ganadoras**: +$420,02 (SHORT 06-23), +$440,02 (LONG 06-26), +$465,02 (SHORT 08-28). Neto +$1.325,06; pico = final (nunca devolvió).

**No aprobó por una sola razón: le faltaron $1.674,94 para el target de $3.000.** Sus 3 ganadoras suman 44,2% del objetivo. Con 17 señales emitidas, 13 murieron fuera de ventana (11 ENTRY_WINDOW + 2 SAFETY_CUTOFF), 4 se admitieron y 1 de ellas murió en MM por `SIZE_BELOW_MIN_CONTRACT` (ATR×$20 > $500 en ese instante). Requisitos de días: `minimum_traded_days=0` (cumplido de sobra con 3 días). Consistencia: la regla no existe en el rule set. Trailing DD $2.000: jamás amenazado (pico=final). **`MATHEMATICALLY_UNREACHABLE_WITH_OBSERVED_TRADES`, confianza PROVEN.** Ganar el 100% de lo observado no basta: el curso emite poco, la cuenta exige mucho.

## 5. Frecuencia y cobertura (FASE 3)

Funnel NQU6 por campaña (CSV adjunto): emisiones OPEN 3–17 por trimestre; **en ventana 2–7**; admitidas 2–7; ejecutadas 2–6. Horas de emisión dentro de ventana por familia: maestra 4h = sólo 13:00 ET; S06 = 09:30+13:30 (ancla NY-cash); S07 = 10:00+14:00; S10 = 12:00–15:00 (1h); T01 = 10:30/11:15/14:15; S12 = 13:15–13:45 (refine 15m); S13 = 11:30–15:30 (refine 30m). Ratio ejecutadas/emisiones: 0,18–0,33. Sequía máxima: 44–64 días entre entradas. El cuello NO es el detector ni el MM ni el Provider: es la intersección (anclas del curso) ∩ (ventana E2T), que deja un solo horario operativo por día para la familia maestra.

Comparación NQZ6 (9 sesiones, 69 rt) vs NQU6 (60 sesiones, 54 rt): las tasas normalizadas son consistentes — NQZ6 es una ventana corta intensiva (más round-trips por sesión porque el humo opera todos los días con señales acumuladas), no un cambio de régimen ni un problema de preparación: mismas horas, mismas geometrías, mismo funnel. No se declara ningún cambio de régimen.

## 6. Equivalencia de señales (FASE 4)

Fingerprints conductuales (timestamp ET, dirección, precio, qty, distancia de stop — independientes de hashes y citas):

- **`SIGNAL_EQUIVALENT` (ejecución idéntica demostrada): 10/19 campañas — C02, C07, S03, S04, S05A, S05B, S09, S19, S20, S21 ejecutaron exactamente los mismos 3 trades** (06-23 13:00 SHORT@29863,25; 08-06 13:00 SHORT@29556,50; 08-26 13:00 SHORT@29215,25×2). Los `signal_id` difieren porque el hash incluye las citas de cada variante; la emisión (ts, dirección, stop) es idéntica en 9 de ellas y S20 es un superconjunto (13 emisiones extra fuera de ventana por red-flags off).
- Subconjuntos parciales de la misma fuente: C03 (2/3), S16 (2/3), S11 (2/3).
- Fuentes de ejecución realmente distintas: **10** (las 10 anteriores + S06, S07, S10, S12, S13, T01 = 6 patrones propios). De 19 campañas pagadas, hay 10 evidencias económicas independientes; **no se pueden contar 10 resultados idénticos como 10 evidencias independientes de nada** (mandato FASE 4).
- Ejes experimentales sin efecto observado en NQU6: sesgo EMA (S03), estructura (S04), DMI/ADX (S05A/B), rearme STR-009 (C07, S19) — clasificados `MATERIAL_AXIS_INACTIVE`/`INSUFFICIENT_EVENTS_TO_DIFFERENTIATE` (con 9 emisiones/trimestre los ejes no llegan a divergir). El coste de esa duplicación fue 10 compras y ~$3.480 de presupuesto de investigación por una sola fuente de señal.

## 7. Fuente vs código (FASE 5)

- **Anclas horarias: fieles.** `session_ctx.go` codifica la rejilla 4h del curso (21/17/1/5/9 ET, DST vía IANA); `session_decision.go` materializa London ideal (01:00), NY continuación (09:00-open/13:00-close), NY reversal (05:00) con citas claim-a-claim. La incompatibilidad con la ventana E2T es estructura del fuente contra estructura de la cuenta, no error de implementación (C01: 1×01:00 ET en NQU6; C04: 4×05:00 + 2×09:00; S01/S02/S17: 4/4 fuera).
- **Failure Swing (KRR-003): la conjunción implementada excede la lectura simple del fuente.** El curso R11·c-0029 identifica con "reacción + **uno de los motivos**"; R12·c-0047 trata el order block como opcional ("puedes esperar al order block **si quieres**"); R6 permite entrar sin activación clásica. El detector exige **reacción Y order block Y motivo confirmados dentro de la ventana de tolerancia (strict = la única vela siguiente)**. La lectura estricta es defendible (la cita literal de R11/c-0046 menciona rango/OB en la misma frase) pero es la interpretación más restrictiva de una fuente genuinamente ambigua, y con motivos 1 (SMT) y 3 (brokers) estructuralmente no disponibles en single-feed NQ, queda la conjunción triple de mayor fricción. **No se relaja el detector (prohibido sin evidencia); la ficha exige video de ch06.** Los parámetros no-fuente están declarados honestamente (`ApproachTicks` NOT_IN_SOURCE, etc.).
- **`STRATEGIES-CATALOG.md` (catálogo canónico) NO existe físicamente en el vault** (`knowledge-library/clutifx/strategies/`): el master lo declara "re-domiciliado el 2026-10-24" y el QA verificó su contenido "cuando vivía en este directorio", pero la migración nunca dejó el archivo. La cadena de trazabilidad fina sobrevive en `chNN/rules.md` + `CLAIMS.md` + `CLUTIFX-OBJECTIVE-DETECTORS.md`, pero el documento canológico único que el propio master cita como autoridad está ausente. **Hallazgo material de gobernanza de conocimiento para el Owner** (no bloquea esta auditoría: se auditó contra la capa por-capítulo).
- Cero reglas inventadas encontradas en la superficie auditada; las operacionalizaciones están etiquetadas OP/HIP y los tests del propio implementador no se usaron como evidencia (se reconstructó el comportamiento desde recibos económicos).

## 8. Verificación del simulador y las cuentas (FASE 6)

Sweep completo sobre las 27 campañas físicas (19 con compra + 8 sin compra), verificación independiente desde los eventos:

- **0 eventos `CHALLENGE_PASS` en ningún stream; `first_pass_at` y `ruin_at` en valor cero en las 27** ⇒ no hay pases perdidos por reporting.
- **Reconciliación exacta**: `stage_net` del engine == P&L reconstruido fill-a-fill (precios, qty, fees $2,49/lado/contrato) en las 19 con diferencia 0,00 (ej. C02: +420,02 = 21,25 pts × $20 − $4,98).
- Flat checks de sesión completos (56/56 trimestre; 26/26 compras tardías); 1 cuenta por campaña; compras+renovaciones uniformemente $120; equity jamás bajo el piso EOD ($2.000 trailing desde pico, nunca amenazado: peor drawdown de la cohorte fue T01 −$1.089,94 desde cero).
- MM con pausa interna −$1.000/día y meta diaria $870 (`RGMM_ACCOUNT_POLICY_V1`): sin bloqueos observados por esos límites.
- **Testigos verificados**: S10 (+1.325,06 3W/0L — explicado en §4); C03 (+795,04 2W/0L pendiente al horizonte — consistente con Q03); C02 (control 2W/1L +335,08, timeline exacto en ACCOUNT-TIMELINES); S06 (6 rt, peor balance −594,82, sin ruina, piso nunca tocado); T01 (3L, −1.089,94); variantes con rechazo de sesión (C01/C04: 100% emisiones rechazadas, nunca compradas — comportamiento correcto del guard).
- **Cero defectos económicos demostrados ⇒ cero cambios de código, cero campañas invalidadas.** La compra a $120 es configuración declarada (`campaign.go: PurchaseCost // 120 USD ON_DEMAND`, "FUNCTIONAL_ASSUMPTIONS iterables por el Owner"), no bug; observación menor: el campo `profile.provider_fee $50 (FACT)` del plan no es consumido por el modelo de cash (que usa $120 para compra y renovación) — decisión de costeo para el Owner, sin efecto en pases.

## 9. Control contra baseline R03 (FASE 8)

**Resuelto con recibos existentes: cero motores nuevos.** La comparación 89/89 (3.037 compras → 328 pases, 10,8%) NO se usa como tasa comparable (horizonte distinto); se usó como **control de hipótesis de defecto común**:

- El mismo motor, mismas reglas E2T y mismo horizonte histórico **que incluye NQU6** registran **233 pases en las 63 configuraciones SG `COMPLETE_RECONCILED`** (1.839 compras, 12,7%) y 24 configuraciones con vidas de pase solapando la ventana NQU6 (pases hasta 2026-10-02; ej. SG-TG-CH300-F0-R500: 18 pases, último 2026-09-28 — **un pase dentro del mismo trimestre**).
- La variable que separa R03 de ClutiFX es la frecuencia de entrada: 0,1–2,4 entradas/día (65–500 por configuración en 672 días) contra 0,02–0,10 de ClutiFX (2–6 por trimestre). Con ganador ~$420 y objetivo $3.000, R03 completa una vida de cuenta (~9–16 días, ~19 entradas por vida) con margen; ClutiFX no llega ni en 90 días con todo ganador.
- No se autorizaron ni necesitaron los 2 controles trimestrales adicionales; no se ejecutó ningún candidato R03 ni histórico alguno.

## 10. Conclusión por estrategia (resumen; detalle en STRATEGY-DECISIONS)

| Fuente real | IDs | Estado técnico | Decisión sugerida al Owner |
|---|---|---|---|
| Familia maestra 4h (13:00 ET) | C02=C07=S03=S04=S05A=S05B=S09=S19=S20=S21 (+subconjuntos C03/S11/S16) | Fiel, rentable en muestra (+$112/trade), 3 ejecuciones/trimestre | Si se busca pasar challenge: subir frecuencia operable (adaptación de ancla/eje de sesiones pre-declarada) o bajar target operativo; NINGUNA re-ejecución del trimestre aporta información |
| Anclas 01:00/05:00 ET | C01, C04 (y S01/S02/S17 en su modo) | Fieles, estructuralmente inoperables en ventana E2T | KRR-001/002/004: autorizar adaptación de ancla como identidad NUEVA o declarar no-operables en E2T |
| Failure Swing | C06, S15, T04 | Ready, 0 setups en 69+9 sesiones con conjunción triple + ventana estricta | KRR-003: video ch06 (minutos de R11/R12) antes de cualquier cambio |
| Modos TS alternativos | S01, S02, S17 | Emisiones fuera de ventana (mismo ancla) | Ídem KRR-004 |
| Refinados | S12, S13 | Distintos pero igual de escasos (2–3 ejecuciones) | Sin acción hasta decidir frecuencia |
| Reentradas/cruces | C07/S19, T01 | T01 perdedor puro (−1.089,94); C07≡maestra | T01: evidencia negativa conservada; no re-ejecutar |
| Bloqueadas | T02 (spec), C08/T05 (datos), S08/T03 (pendientes materializar) | Sin corrida propia | Decisiones KRR-005/006/007 |

## 11. Veredicto

`CLUTIFX_TECHNICAL_STATUS`: cadenas funcionales G0–G3+G2C válidas; detectores fieles o con dudas acotadas a video (KRR-003/004/005); cero defectos de implementación demostrados en el camino económico.
`CLUTIFX_ECONOMIC_STATUS`: `QUARTER_NO_PASS` por `MATHEMATICALLY_UNREACHABLE_WITH_OBSERVED_TRADES` 19/19 — baja frecuencia estructural (anclas del curso vs ventana E2T) × ganador techo $465 vs objetivo $3.000. La expectancia observada es positiva; la muestra por cuenta es órdenes de magnitud menor que la que el objetivo exige.
`NEXT_OWNER_DECISIONS`: (1) KRR-001/002/004 adaptación de ancla (identidad nueva) vs no-operables en E2T; (2) KRR-003 video ch06; (3) KRR-005 ancho de stop T02; (4) KRR-006 adquisición de datos; (5) KRR-007 materializar S08/T03; (6) decisión de costo $120/purchase+$120/renewal vs `provider_fee $50`; (7) restaurar o degradar formalmente el catálogo canónico ausente; (8) política de duplicación de campañas equivalentes (10× gasto por una fuente).
`OWNER_ACCEPTANCE: REVIEW`

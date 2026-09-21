# POLYMARKET_FINAL_READINESS

Etapa: **`ENGINEERING_STAGE_CLOSED_RESEARCH_REPRODUCIBLE`**. El engine queda listo para investigación reproducible. No hay alpha, no hay readiness de dinero real y las cinco hipótesis siguen sin validación económica.

## ENGINE

Worktree `~/go/src/github.com/xKoRx/polymarket-engine-integration`, branch `feature/five-poc-integration`, HEAD **`85e27ff`** (limpio). Código **`56e8fac`**. Remoto `origin/feature/research-strategies-v01` @ `25f578a` (local unpushed). **Cero cambios de código.** `LIVE_DISABLED` intacto (`LIVE_ENABLED` fail-closed).

## M4

**`M4_CERTIFIED_NON_LIVE` @ `c38f6c4`** (27 PASS / 0 FAIL / 0 NOT_RUN in-scope / 5 live diferidos). Válido sólo para ese árbol de código. No recertificado: no hubo código nuevo.

## DATA

| Fuente | Estado |
|---|---|
| Fixtures v07 | Sintéticos, intactos |
| RS v0.3 | 41/41 SHA OK |
| PE-001 E3 | 78/78 SHA OK |
| Hardening 2026-09-21 | Bundle nuevo `hardening-20260921/` (read-only; no se copió WAL activo) |
| Weather PIT vintages | **Ausentes** (contratos inventariados) |
| Cohorte O/B de mercado *nuevo* | **Ausente** (sí hubo sync de un mercado ya existente) |

Falta de dato ≠ ausencia de oportunidad: en discovery la API respondió; lo que faltó fue un par semántico∩temporal.

## ECONOMICS

Gate **`U02_PARTIAL`**. `REAL_FEE_READY=NO`. Factory sigue `SYNTHETIC_FIXTURE`.

- **Pareado:** Sports/weather CLOB `fd {r:0.05, e:1, to:true}` = docs + SDK USDC `p(1-p)^e`. Vectores independientes: PE-001 q20 @0.56/0.48 → fee engine 0.2464 / 0.2496 USDC.
- **No pareado (defecto real, sin parche):** BUY en venue reduce **shares**; el engine suma fee en USDC y asume q shares recibidas. Worst payout de la canasta PE-001: 20 vs ≈19.48. Equivalencia USDC no preserva el payoff combinatorio.
- Redondeo: docs 5 dp vs engine `TRUNCATE_6DP`. Tie-break oficial no documentado. Delta típico < 1e-5 / nivel.
- On-chain `CalculatorHelper` usa `min(p,1-p)`; familia distinta. `/fee-rate` `{base_fee:1000}` es legado, no `fd.r`.
- Rebates **no únicos:** sports 15% (docs+Gamma); weather 25%. Maker fee 0 / taker-only en la captura.
- Delay deportivo: `seconds_delay=1` / `sd=1`. Escenario adverso 1 tick × 2 patas q20 = **0.40 USDC** (modelo, no fill). `itode` no afirmado.

Cambio de Economics exigiría ownership explícito, vectores `u02/vectors.json` como regresión y recertificación del SHA final. No se hizo.

## POCS

| POC | Técnico | Datos reales | Contrato | Fees | Experimento | Bloqueo exacto | Próximo mínimo |
|---|---|---|---|---|---|---|---|
| S01 NegRisk | OFFLINE @ 85e27ff | RS v0.3 159954 intacto | Membership VERIFIED; exhaustiveness **UNKNOWN** | Sintético | 663 INCONCLUSIVE; **no promover** | Exhaustiveness futura + Other mutable | Releer `getQuestionCount` al cierre |
| S02 Reversion | OFFLINE | MLB 2284198, 6 h, 0 señales | Kickoff verificado en esa captura | Taker only sintético | `NO_SIGNAL_OBSERVED_IN_WINDOW` **local** | Muestra de frecuencia insuficiente | Otra ventana, mismo harness, otro juego |
| S03 Combinatorial | OFFLINE + E3 `GO_RESEARCH` | 7 pares / 0 ∩ | WNBA 6/6 `RULES_CONTRADICT`; FIBA OT OK pero PAST | `fd` 0.05/1/to observado | H1 no falsificada; 0 ACCEPT | OT/tie WNBA o dictamen owner; BUY-shares | Esperar par OT-emparejado; congelar journal **antes** de SHADOW |
| S04 Weather | OFFLINE UNCALIBRATED | Contratos sí, vintages no | NYC **KLGA**, Tokyo **RJTT** | `weather_fees` 0.05/1/to, rebate 0.25 | Fixtures only | Sin forecast issued-at ≤ frame | Adquisición `weather/ACQUISITION.md`; no calibrar |
| S05 Maturation | OFFLINE descriptivo 0/0/0 | Sync de mercado **ya existente** | `first_known_at` ≠ `createdAt` demostrado | n/a | 0 mercado nuevo en la ventana | Cohorte O/B real ausente | Observar nacimiento; W sigue SFG-06 |

## RESEARCH

Hipótesis contrastadas, no validadas:

1. **H1 PE-001 (reglas verbatim ⇒ no ACCEPT):** no falsificada. Familia WNBA rechazada por OT SP UNKNOWN + cláusula de empate. Un template FIBA con OT escrito en ambas patas **existe**, pero el único miembro semántico está post-kickoff.
2. **Universo ML+SP usable ahora:** denominadores 41 series / 73 eventos / 7 pares / 1 semántico / 3 temporales live / **0 semántico∩temporal** / **0** lock q=20 / 0 datos faltantes. Profundidad live WNBA cubría q=20 (VWAP 1.04 / 1.19 / 1.08); el rechazo es semántico+económico, no de book.
3. **S02:** 0 señales en una ventana ≠ NO_GO de la familia.
4. **S04:** contrato real inventariado; calibración **imposible** sin vintages PIT.
5. **S05:** wiring Catalog honesto; no hay cohorte de nacimiento.

No hubo WS/SHADOW nuevos (no había miembro admisible). No se atribuyeron fills.

## BLOCKERS

Sólo materiales:

1. **Par PE-001 semántico∩temporal.** Falta: OT escrito igual en ML y SP, sin tie, kickoff futuro. Impacto: no se puede SCREEN→SHADOW económico. Resolución: aparece ese par **o** dictamen owner de que la cláusula WNBA es boilerplate inerte.
2. **BUY-shares vs USDC.** Falta: paridad del engine con semántica real de BUY. Impacto: overstatement de payout en 2×BUY. Resolución: ownership + parche mínimo + recertificar SHA.
3. **Weather vintages PIT.** Falta: NWS MOS/NBM issued-at ≤ frame. Impacto: S04 permanece UNCALIBRATED. Resolución: ejecutar `ACQUISITION.md`.
4. **Cohorte O/B de mercado nuevo.** Falta: nacimiento observado (`first_known_at` auténtico). Impacto: S05 no mide maduración real. Resolución: captura durante un alta real; no usar `createdAt`.
5. **NegRisk exhaustiveness.** Falta: payout al cierre / Other inmutable. Impacto: 663 resultados siguen INCONCLUSIVE. Resolución: re-lectura on-chain al settle; no ACCEPT mientras UNKNOWN.

## DEBT

No bloqueante: `capitalLock "5.1"` legacy BBO (`experiment.go:493`); gofmt drift en `five_poc_cases_test.go`, `research_gates_test.go`, `screen.go`; SFG-06 W; A2 serializar corpus PE-004; `/fee-rate` legado vs `fd`; rounding 5 vs 6 dp (delta acotado).

## OWNER_DECISIONS

Pendientes, no autoaceptadas:

- Review humana `c915c11..85e27ff`.
- Publicar o no `feature/five-poc-integration`.
- Dictamen OT/tie WNBA.
- Autorizar o no el parche Economics BUY-shares.
- Habilitar trading: **no**. `LIVE_DISABLED`.

## NEXT_ACTION

Trabajo mínimo restante, **sin código**:

1. Esperar un par ML+SP con OT emparejado y sin tie; entonces WS + congelar journal **antes** de SHADOW.
2. En paralelo, sólo si interesa S04: ingestar vintages NWS as-of (no latest).
3. S02: una segunda ventana pre-match, mismo harness, otro juego.

Evidencia: `~/go/src/github.com/xKoRx/polymarket-engine-datasets/hardening-20260921/REPORT.md`. Continuidad §10. Change log [[2026-09-21-polymarket-final-readiness]]. Sesión abierta.s
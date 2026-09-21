**U-02 queda modelado, no certificado como fee real.** `q` sigue siendo **shares brutas enviadas** al walk; el fee en shares sólo deriva `SharesNet`. `REAL_FEE_READY` permanece **false**.

Worktree aislado: `/home/kor/go/src/github.com/xKoRx/polymarket-engine-u02` (`fix/u02-buy-shares-accounting`). El worktree de integración sigue en `feature/five-poc-integration@85e27ff`, sin tocar.

---

## Causa raíz

El schedule y PE-001 trataban el fee como **USDC aditivo** y el payout como **q shares**. En el venue, el taker fee de BUY se cobra en **outcome tokens** en el match (`CalculatorHelper`: Token Proceeds); SELL recorta **collateral**. Sobreestimación en el basket PE-001 de los vectores: cash `21.296` y worst payout `20` frente a notional `20.80` y payout neto `19.48`.

## Contrato económico

| Campo | `USDC_CASH` (sintético / SDK) | `TAKER_PROCEEDS` (on-chain taker) |
|---|---|---|
| `q` | GROSS sent | GROSS sent (nunca net target) |
| BUY cash | notional + fee USDC | notional |
| BUY shares | = filled | filled − fee_shares |
| SELL | proceeds = notional − fee USDC; shares sold = filled | igual (fee en collateral) |
| Capital BUY | notional (+ fee en cash mode) | notional (caja realmente lockeada) |

Fórmula v1 (sin `min()` on-chain):

- USDC-eq: `rate · p^e · (1−p)^e · take`, `TRUNCATE_6DP`
- BUY shares (`e=1`): `rate · (1−p) · take`, `TRUNCATE_6DP`
- Consistencia: `Truncate6(fee_shares · p) == LevelCost` o rechazo

Resolución de unidad:

- vacío + `SYNTHETIC_FIXTURE` → `USDC_CASH` (preserva 1.505 de B0)
- vacío + `REAL_UNVERIFIED` → unidad no resuelta, `FeeResolved=false`, no ACCEPT
- desacuerdo 5dp vs `TRUNCATE_6DP` → `RoundingUnresolved`, no ACCEPT

PE-001: `fee_settlement` opcional. Métricas nuevas (`ml_shares_net`, `q_meaning`) **sólo** con `TAKER_PROCEEDS`. `quote_inputs_hash` no cambia en sintético vacío.

---

## SHA

| Punto | SHA |
|---|---|
| Inicial (integración, no modificada) | `85e27ff85d466c6522455f1426f6e0c8e23fe157` |
| Código U-02 | `d5ce263cd669e8114b2b0545a343befd5acb92c5` |
| Final (pin M4) | `d62768a7a4f5a9fef7ff76b3f3358e7167a3bb8a` |

Baseline del certificado: **`d5ce263`**. El pin `d62768a` no reescribe v07.

## Archivos (diff código `d5ce263`)

14 files, +1487 / −25:

- `internal/regimes/schedule.go` (+ tests)
- `internal/economics/settlement.go` (nuevo), `scheduled.go`, `u02_settlement_test.go`
- `internal/simulator/simulator.go`, `u02_settlement_test.go`
- `internal/integration/s10_s11_test.go` (Account acredita **net**)
- PE-001: `evaluate.go`, `strategy.go`, `model.go`, tests
- `testdata/economics/u02/vectors.json` (SHA-256 `177d187e…`, idéntico al oracle independiente)

Pin: `testdata/research-v08/certificate-v08.json`, `CERT.md`.

---

## Tests físicos

| Gate | Resultado |
|---|---|
| `gofmt` / `go vet` paquetes tocados | limpio |
| `go test` economics / regimes / simulator / PE-001 / account | PASS |
| Cover atomic | economics **91.2%**, regimes **94.8%**, simulator **97.2%**, PE-001 **95.0%**, account **95.3%** |
| Cinco POCs + `cmd/engine` | PASS (`cmd/engine` 54.8s) |
| M4 `experiment certify --profile no-live --baseline d5ce263` | **`M4_CERTIFIED_NON_LIVE`** 27/0/0 + 5 live deferred |
| LIVE_DISABLED (`TestDefaultsFailClosed`, `TestLiveEnabledFailsClosed`) | PASS |
| Evidence SHA-256 v07 vs v08 | **idénticos** (drills v07 no regenerados) |

Cover por debajo del piso 95% en economics/regimes: mismo tipo de hueco que SFG-02 (reducer / helpers de rounding). No se rellenó con tests cosméticos.

---

## Vectores (esperado = observado)

**USDC_CASH** (vacío + sintético), q=20:

| Pata | fee USDC | cash | shares |
|---|---|---|---|
| ML p=0.56 | 0.246400 | 11.446400 | 20 |
| SP p=0.48 | 0.249600 | 9.849600 | 20 |
| Basket | 0.496000 | **21.296000** | worst si q=20 → **20** |

**TAKER_PROCEEDS**, mismo q bruto:

| Pata | cash | fee_shares | net | payout si gana |
|---|---|---|---|---|
| ML | 11.20 | 0.4400 | 19.5600 | 19.5600 |
| SP | 9.60 | 0.5200 | 19.4800 | 19.4800 |
| Basket | **20.80** | — | — | worst **19.48**; 50/50 **19.52** |

PE-001 B0 (p=0.45/0.45, q=20, r=0.05):

- sintético: cost **18.495**, worst_payoff **20**, worst_net **1.505**, candidate Size **20**
- `TAKER_PROCEEDS`: cost **18**, net **19.45/19.45**, worst_payoff **19.45**, worst_net **1.45**, Size sigue **20**

Otros: FOK/FAK parciales sobre filled no sobre requested; fee 0 → net=gross; settlement desconocido **rechazo**; `REAL_UNVERIFIED` vacío **no resuelve**; fee > filled / proceeds **rechazo**; `0.000693` (5dp vs 6dp) → **INCONCLUSIVE**, no ACCEPT. Ningún `UNKNOWN` pasó a `ACCEPT`.

---

## Certificado y v07

- Nuevo: `testdata/research-v08/certificate-v08.json` @ `d5ce263`
- v07 intacto: hashes de evidencia del matrix **iguales**; no hay scorecard/digest nuevo que reescribir
- SCREEN/REPLAY/SHADOW: suites de las cinco POCs + `cmd/engine` verdes; PE-001 sintético no añade métricas → identidad de drills v07

## Impacto POCs

| POC | Efecto |
|---|---|
| PE-001 sports combinatorial | Default sintético idéntico. Opt-in `TAKER_PROCEEDS` corrige cash/payout. Tie-break → INCONCLUSIVE |
| PE-002 / PE-005 / PE-030 / PE-004 | Sin consumo de settlement; tests PASS |

## Bloqueos U-02 restantes

1. `live_fill_proof_of_unit=false`
2. Tie-break 5dp **no documentado** (sigue bloqueado)
3. Docs USDC vs on-chain `min(p,1−p)` en shares
4. `/fee-rate` 1000 bps ≠ `fd.r=0.05`
5. Fórmula engine sin `min()` on-chain
6. Factory sintético vacío → `USDC_CASH` (intencional, no venue)

**No hay merge, push, live, wallet, signing ni órdenes.** Entrega no autoaceptada; sesión Agents-OS abierta.s
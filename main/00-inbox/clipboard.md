**Dictamen: `V2_CASH_CONFIRMED`.** En los mercados reales de PE-001 y en weather (familia NegRisk), el BUY cobra fee extra en collateral pUSD y entrega las shares completas. `TAKER_PROCEEDS` de `d5ce263` modela el Exchange V1 archivado, no el venue vigente. `REAL_FEE_READY` sigue **false**. No se integró código, no hubo merge/push/live/órdenes.

Integración intacta en `feature/five-poc-integration@85e27ff`. El parche U-02 sigue aislado en `fix/u02-buy-shares-accounting@d62768a` (código `d5ce263`). v07 y v08 no se reescribieron.

---

## 1. Venue aplicable

| Familia | Mercado | Exchange | Collateral |
|---|---|---|---|
| PE-001 sports binary | Gamma `4358151` ATL vs NYL, `createdAt=2026-09-08`, `negRisk=false`, `feesEnabled=true`, `sports_fees_v3`, `fd {r:0.05,e:1,to:true}` | CTF Exchange V2 `0xE111180000d2663C0091e4f400237545B87B996B` | pUSD `0xC011a7E12a19f7B1f670d46F03B03f3342E82DFB` |
| PE-001 SP | Gamma `4778073` ATL −1.5, mismo event 986912 | el mismo V2 (dos CLOB, no Combos) | pUSD |
| Weather / NegRisk | event `1046925` NYC, `negRisk=true`, `weather_fees` | Neg Risk CTF Exchange V2 `0xe2222d279d744050d28e00520010520000310F59` | pUSD |

Fuentes: [docs.polymarket.com/resources/contracts](https://docs.polymarket.com/resources/contracts), Gamma/CLOB read-only, y las txs de abajo (`to=` = esas direcciones). V1 no aparece.

## 2. Rutas V2

En `Trading.sol` V2 el BUY transfiere tokens completos y cobra fee en asset id 0 (collateral). `_matchBuyOrders` hace `takerFillAmount + takerFeeAmount`. `_settleTakerOrder` en BUY llama `_chargeFee` en collateral; en la ruta mint pasa `feeAmount=0` al settle de tokens porque la fee ya salió del pull. `Fees.sol` valida `fee` contra `cashValue`, ambos en collateral. El operador aporta `takerFeeAmount`; el contrato no recalcula `fd`.

V1 archivado (`CalculatorHelper.calculateFee`) sí cobra BUY sobre token proceeds. Eso es exactamente `TAKER_PROCEEDS`.

## 3. Liquidación pública

**PE-001 BUY** [`0x35f204735b3d0854dc3da5a77a0ff4251cf41ad19a88f4dc569a9b83b7c2de61`](https://polygonscan.com/tx/0x35f204735b3d0854dc3da5a77a0ff4251cf41ad19a88f4dc569a9b83b7c2de61) — `matchOrders` en V2, Liberty 180.34 @ 0.46:

- Taker envía **85.196220 pUSD** = notional 82.956400 + fee 2.239820.
- ERC1155 al taker: **180.340000** shares (completas).
- `FeeCharged` **2.239820 pUSD**. `OrderFilled` BUY con fee en collateral.
- Si fuera V1, net ≈ 175.47 shares. No ocurrió.

**Weather BUY** `0x5a2269f1f9a9325b7874630b3346040ddd7fef18899cca5c22ee3f38685c5fc8` — NegRisk V2: takerAmt **483.900000** shares + fee **0.047040 pUSD**. Misma unidad.

On-chain 2.239820 = 5 dp USDC; `TRUNCATE_6DP` del engine daría 2.239822. `fd` no basta para la fee efectiva.

## 4. Help Center

No es otra capa ni mercados mixtos V1/V2 en esta familia. El FAQ de upgrade (2026-07-17) dice que las fees ahora se cobran en USDC, no en shares; eso coincide con el contrato y las txs. Maker Rebates (2026-07-21) todavía dice “collected in shares on buy orders”: lenguaje V1 que quedó en un artículo actualizado después del cutover. Docs `trading/fees` y `place-orders` (`amount` pre-fee, fees **on top**, `maxSpend`) describen el modelo cash-additive.

## 5. `USDC_CASH` vs `TAKER_PROCEEDS`

| | `USDC_CASH` | `TAKER_PROCEEDS` | Venue V2 |
|---|---|---|---|
| Representa | default sintético: cash += fee, shares = filled | V1: BUY recorta shares; el comentario lo llama “on-chain” | BUY: cash += fee pUSD, shares = filled |
| `q` | GROSS sent | GROSS sent | GROSS filled (`takerAmt`) |
| cash BUY | notional+fee | notional | notional+fee |
| shares BUY | filled | filled − fee_shares | filled |
| fee BUY | USDC | SHARES | pUSD |

`USDC_CASH` acierta la **unidad** viva. `TAKER_PROCEEDS` acierta V1 y se etiqueta mal. Impacto del código actual: el default sintético vacío no rompe v07; usar `TAKER_PROCEEDS` como venue de PE-001 **sí** falsearía cash y payout. Cambio mínimo: relabel + no auto-resolver `REAL_UNVERIFIED` a `TAKER_PROCEEDS`. No hace falta otro modelo de cobro.

## 6. Diff `85e27ff..d5ce263`

14 archivos, +1487/−25: settlement dual, PE-001 opt-in, vectores. El default sintético preserva números v07. No hay regresión de drills **mientras** no se tome `TAKER_PROCEEDS` como autoridad de venue. Integrarlo como “fix de shares” sería una regresión de protocolo.

## 7. Gates faltantes (sin tests cosméticos)

De la sesión que produjo `d5ce263`, no re-ejecutados aquí: economics **91.2%**, regimes **94.8%** (piso 95%); `-race` del parche no consta; certificado v08 pineado a `d5ce263` mientras HEAD U-02 es `d62768a` (mismo patrón v07). Correspondencia exacta SHA de código HEAD ↔ certificado: **no**.

## Plan de corrección (no ejecutado)

1. Relabel: `USDC_CASH` = V2 vigente; `TAKER_PROCEEDS` = V1 archivado.
2. No mergear `d5ce263` a integración como corrección de venue.
3. Mantener fail-closed 5 dp vs 6 dp; `fd` ≠ fee match-time.
4. `REAL_FEE_READY=false` hasta reconstruir `takerFeeAmount` (5 dp + tope `maxFeeRateBps`).
5. Recertificar M4/cover/race **solo** si hay cambio de código.

Informe: `polymarket-engine-datasets/u02-protocol-authority-20260921/REPORT.md`. Continuidad §11. Change log [[2026-09-21-u02-protocol-authority]]. Sesión Agents-OS abierta; Review humana y publicación siguen abiertas.s
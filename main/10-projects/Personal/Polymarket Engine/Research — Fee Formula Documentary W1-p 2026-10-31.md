---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
related: []
aliases: []
tags:
  - kind/doc
created: "2026-10-31"
updated: "2026-10-31"
---

# Research — Fee Formula Documentary W1-p 2026-10-31

## Propósito

- Cerrar el paso documental que [[Research — Target Fee Inventory W1-o 2026-10-31]] dejó abierto: establecer, con **fuentes oficiales públicas y fechadas**, qué es la fee de Polymarket (fórmula, unidades, escala, redondeo, base de coste, cobro) y qué significa el campo WS `fee_rate_bps` frente a los límites maker/taker `1000` y al `fd` crudo `{e:1, r:0.05, to:true}` observados en el mercado `5784455`, con as-of `2026-10-29`. Es investigación **documental**: sin código, sin checkout, sin capturas nuevas, sin re-score, sin tocar L ni los escenarios congelados. `REAL_FEE_READY` sigue en `false` y el gap U-02 (`base_fee` ↔ `feeRate` ↔ settlement) **sigue abierto**: W1-p lo acota, no lo cierra.

## Contenido

### Resultado

- **Sí** se puede modelar costo de forma defendible para investigación **futura**: la documentación oficial entrega la fórmula `fee = C × feeRate × p × (1 - p)` (C = shares, p = precio), unidades USDC, redondeo a 5 decimales con mínimo `0.00001`, cobro sólo al taker y en matching time; y el código oficial entrega el techo contractual en basis points sobre el valor de collateral, más el hecho de que **la curva se calcula fuera del contrato**. **No** se puede cerrar la fee histórica del episodio: el sujeto del campo WS `fee_rate_bps` no está documentado en ninguna fuente consultada, y ningún commit o página consultada prueba el despliegue ni el `MAX_FEE_RATE` vigente el 29-10-2026.

### Fórmula, unidades y redondeo (evidencia directa)

- Fórmula documentada: `fee = C × feeRate × p × (1 - p)`; `C` = número de shares, `p` = precio de la share; `feeRate` viene de la categoría o del `feeSchedule` del mercado. "Makers are never charged fees. Only takers pay fees."
- Unidad y redondeo: fee en USDC (collateral pUSD en el régimen V2), calculada a 5 decimales, mínimo no nulo `0.00001 USDC`; por debajo redondea a cero. La fee en dólares es simétrica respecto de 50% de probabilidad.
- Base de cobro: en BUY la fee se **suma** al collateral gastado (el monto de una market BUY es notional pre-fee); en SELL se **descuenta** del proceeds. El contrato acota además `fee ≤ proceeds` del pagador.
- Rates por categoría (taker / maker / maker rebate): Sports `0.05` / 0 / 15%; Crypto `0.07` / 0 / 20%; Finance, Politics, Mentions, Tech `0.04` / 0 / 25%; Economics, Culture, Weather, Other-General `0.05` / 0 / 25%; Geopolitics `0` (fee-free); Combos `0.05`. Ejemplo de magnitud: 100 shares a `$0.50` → `$1.25` en Sports, `$1.75` en Crypto, `$1.00` en los grupos 0.04.
- Parámetros por mercado: `feeSchedule.rate` = "Base rate used in the fee calculation"; `feeSchedule.exponent` = "Exponent applied to the price component of the fee curve"; `takerOnly` = "fees are charged to the taker side only, and makers pay no fee"; `rebateRate` = fracción de la fee de taker devuelta al maker en reposo (`0.25` = 25%).
- Límites declarados: CLOB expone `mbf` y `tbf` ("in basis points"); `GET /fee-rate?token_id=` devuelve `base_fee` en bps (ejemplo `30`). `fd` = "Fee curve parameters for a market" con `e` = "Fee curve exponent", `r` = "Fee rate", `to` = "Whether fees apply to takers only" (Gamma usa los nombres largos `exponent`, `rate`, `takerOnly`, `rebateRate`).
- Campo WS: `last_trade_price` incluye `fee_rate_bps` opcional, descrito sólo como "Fee rate in basis points"; `side` es desde la perspectiva del taker.

### Lo que NO está documentado (y por eso no se afirma)

- **No hay fórmula oficial** que combine `rate`, `exponent`, `mbf`/`tbf` y el collateral. La forma `fee = C × rate × p^e × (1 - p)` es **inferencia**: con `e = 1` (el valor observado) coincide exactamente con la fórmula documentada y ninguna fuente la contradice; con `e ≠ 1` queda como hipótesis explícita.
- `fd.r` no tiene unidad declarada; `mbf`/`tbf` no tienen función documentada (ni techo, ni multiplicador, ni componente aditivo).
- El sujeto de `fee_rate_bps` (maker, taker o mercado) y si su valor `0` implica ausencia de cobro **no están documentados**: el WS ref y el AsyncAPI sólo dan la unidad, y el changelog sólo indica que desde V2 la fee se fija en matching time y la orden ya no lleva `feeRateBps`.
- La equivalencia `fd{e,r,to}` ≡ `feeSchedule{exponent,rate,takerOnly,rebateRate}` es **inferencia** por correspondencia de nombres y semántica: no hay tabla de mapeo oficial publicada.

### Mapa de implementaciones y versiones (código oficial)

- **V2 / Poly v2** (`Polymarket/polymarket-v2-external`, BUSL-1.1): la orden firmada **no lleva ningún campo de fee** (`salt`, `makerAmount`, `takerAmount`…); el operador entrega los importes ya calculados (`makerFeeAmounts`, `takerFeeAmount`); el contrato valida `fee ≤ cashValue × MAX_FEE_RATE / 10000` con `MAX_FEE_RATE` inmutable on-chain y `BPS_DENOMINATOR = 10_000`, techo `MAX_FEE_RATE_BPS_CAP = 10_000` (100%). El invariante formal (spec Certora `Exchange-FeeCap01b`) cubre maker fees, selling-taker y buying-taker, y exige además `fee ≤ proceeds` del pagador.
- **CTF Exchange V2** (`Polymarket/ctf-exchange-v2`): `BPS_DENOMINATOR = 10_000`, techo 100%, `maxFeeRateBps` por defecto `500` (5%); en el matching la fee entra como importe ya calculado y se valida contra el valor de collateral del fill.
- **CTF Exchange legacy V1** (`Polymarket/ctf-exchange`): `MAX_FEE_RATE_BIPS = 1000; // 1000 bips or 10%`, archivo sin cambios desde 2022. Coincide numéricamente con el `mbf`/`tbf` = 1000 observado, pero **es analogía, no prueba**: ninguna fuente oficial liga `mbf`/`tbf` al `MAX_FEE_RATE`.
- **SDK legacy** (`Polymarket/clob-client`): la orden llevaba `feeRateBps` (las market orders ponían `"0"`), sin cálculo de fee ni cap de fee; `ROUNDING_CONFIG` sólo cubre price/size/amount; último commit del path 2026-03-04. Los SDK V1 dejaron de soportarse para trading el 2026-04-28.
- **SDK unificado** (`Polymarket/ts-sdk`, creado 2026-04-02, push 2026-10-29): commit "feat(client): add fee-aware market buy orders" (2026-05-02); sus bindings exponen **builder** fee rates en bps (`BUILDER_FEES_BPS = 10_000`), que **no** son la fee de trading del mercado. Los SDK Python y Rust oficiales no contienen ningún archivo de fee.
- Consecuencia metodológica: como la fee se fija en el matching, **ningún backtest puede usar "la fee de la orden"**: hay que simularla con el `feeSchedule` capturado antes del timestamp de decisión.

### Matriz actual vs. histórico

| Hecho | Vigente 2026-10-31 | Vigencia histórica (≤ 2026-10-29) | Falta |
|---|---|---|---|
| Fórmula `C × feeRate × p × (1 - p)` | `trading/fees.md` (sin fecha) | Probada por régimen: "Fee Structure V2" (30-03-2026) y fee dependiente del precio desde 05-01-2026 | Fecha de vigencia de la página; forma con exponente sin documentar |
| Rate sports 0.05 | tabla de categorías | Probada: changelog 10-07-2026, coef. taker sports `0.03`→`0.05` efectivo a medianoche UTC | Categoría real del mercado `5784455` (su `fd.r` = 0.05 es compatible con varias categorías) |
| Maker paga 0 / rebate 15% sports | fees + maker-rebates | Probada: changelog 10-07-2026 (rebate sports 25%→15%) y 11-02-2026 (rebates por mercado) | `rebateRate` efectivo del target (no capturado) |
| Fee en matching time, orden sin fee | `Exchange.sol` + changelog 17-04-2026 | Probada: anuncio 17-04-2026 y CLOB V2 en producción 28-04-2026 | — |
| Techo contractual en bps | `Exchange.sol`, `IFees.sol`, spec | **No probada para el 29-10-2026**: commit de `Exchange.sol` (autor 2026-09-17, committer 2026-09-24) es fecha de commit, no de despliegue | Deployment proof (fuera de superficie) |
| `mbf`/`tbf` = 1000 bps | `get-clob-market-info.md` | Sólo analogía numérica con el techo legacy V1 | Definición oficial de la función de `mbf`/`tbf` |
| `fee_rate_bps = "0"` | sólo "Fee rate in basis points" | No aplicable: definición no versionada ni fechada | Sujeto del campo |

### Conclusión acotada para el episodio del 29-10-2026

- Lo que **sí** sostiene la evidencia fechada: régimen Fee Structure V2 con `feeSchedule` por mercado; fees determinados en matching time con CLOB V2 en producción; si el mercado estaba en la familia de rate `0.05`, taker `0.05` vigente desde 10-07-2026 y maker sin pago (rebate 15% **si** la categoría era Sports); y bajo la fórmula documentada la fee de taker de un trade a precio `p` sería `C × 0.05 × p × (1 - p)`, es decir **dependiente del precio**, no una constante en bps.
- Lo que **no** se puede afirmar: que se cobrara —o no— fee en los 78 trades ni cuánto (settlement sigue NOT_CERTIFIED); que la categoría fuera Sports; que el contrato desplegado fuera una implementación concreta con un `MAX_FEE_RATE` determinado; que `mbf`/`tbf = 1000` sea el techo aplicado; y por tanto **no se puede declarar `REAL_FEE_READY` en ningún alcance**.
- Por qué el `0` no es interpretable: una tasa de taker *constante* en bps no es representable bajo la fórmula documentada (la fee depende de `p`), y un `0` por redondeo (mínimo `0.00001`) es indistinguible de un `0` real. Leer `fee_rate_bps = "0"` como "no se cobró fee" sería un error de categoría.

### Claims no resueltos

- Sujeto de `fee_rate_bps` y significado de `0` — no documentado en `llms.txt`, api-reference, AsyncAPI ni changelog.
- Fórmula que combina `rate`/`exponent`/base-fee/collateral — inferida, no documentada.
- Categoría y `rebateRate` del mercado `5784455` — requieren endpoint de mercado (fuera de la superficie permitida).
- Implementación y `MAX_FEE_RATE` vigentes el 29-10-2026 — requieren prueba de despliegue (fuera de superficie).
- Fee efectivamente cobrada en los 78 trades — sin settlement observado.

### Límites de esta investigación

- Toda página consultada es la documentación **vigente el 2026-10-31**: consultarla hoy **no** prueba que rigiera el 29-10-2026. Sólo el changelog fechado (05-01, 11-02, 18-02, 30-03, 31-03, 17-04, 28-04, 10-07-2026) aporta histórico, y una fecha de commit no es fecha de despliegue.
- WebFetch devuelve el cuerpo convertido y resumido por un modelo: **no hay hash de origen** de ninguna fuente.
- Denegaciones literales del hook: `raw.githubusercontent.com/Polymarket/ts-sdk/main/packages/client/src/actions/orders/estimate.ts` y `.../market.ts` → `Outside immutable W1-p scope` (código de cálculo de fee del SDK oficial); no se reintentó ni se buscaron variantes. La visualización oficial de la curva (`datawrapper.dwcdn.net/dJ74e/`) está fuera de la allowlist de dominio. `api.github.com/repos/Polymarket/{docs,polymarket-docs,exchange,exchange-core}` → HTTP 404 (ausencia de ese repo, no del tema).
- No se usaron endpoints de mercado, libro, órdenes, RPC, cuentas ni transacciones; no se requiere cuenta propia ni cobro propio real para la etapa offline.

## Fuentes

- Vault: [[Research — Target Fee Inventory W1-o 2026-10-31]] (inventario offline previo y gap U-02), [[Research — Default Suite Isolation W1-nR 2026-10-30]], [[Polymarket Engine — MVP]].
- Documentación oficial (consultada 2026-10-31): `docs.polymarket.com/llms.txt`, `/trading/fees.md`, `/market-data/market-details.md`, `/market-data/realtime-data.md`, `/market-data/prices-order-books.md`, `/api-reference/markets/get-clob-market-info.md`, `/api-reference/markets/get-market-by-id.md`, `/api-reference/wss/market.md`, `/asyncapi.json`, `/api-reference/market-data/get-fee-rate.md`, `/api-reference/market-data/get-fee-rate-by-path-parameter.md`, `/api-reference/trade/post-a-new-order.md`, `/changelog/predictions.md`, `/programs/maker-rebates.md`, `/programs/taker-rebates.md`, `/trading/place-orders.md`, `/concepts/order-lifecycle.md`, `/concepts/markets-events.md`, `/migrate/polymarket-v2/api-integrations.md`, `/migrate/polymarket-v2/overview.md`, `/migrate/data-api-v1-to-v2.md`, `/resources/contracts.md`, `/getting-started/typescript.md`.
- Código oficial: `Polymarket/polymarket-v2-external` (`src/exchange/Exchange.sol`, `OrderStructs.sol`, `MATCH_ORDERS_LIFECYCLE.md`, `certora/specs/Exchange-FeeCap01b.spec`; BUSL-1.1), `Polymarket/ctf-exchange-v2` (`src/exchange/mixins/Fees.sol`, `interfaces/IFees.sol`, `mixins/Trading.sol`), `Polymarket/ctf-exchange` (`src/exchange/mixins/Fees.sol`, `interfaces/IFees.sol`), `Polymarket/clob-client` (`src/order-builder/helpers.ts`), `Polymarket/ts-sdk` (`packages/bindings/src/clob/builder.ts`).
- API pública de GitHub (sin token) para metadatos, árboles e historial de commits por path.
- Artefactos del shot: `validated-baseline/w1-p-fee-documentary-20261031/source-ledger.json` (S01–S34 + denegaciones + claims no resueltos), `research.md`, `prereg-draft.md` (DRAFT_NOT_APPROVED), `run-receipt.json`, `capability.json`, `scout-pack.json`.

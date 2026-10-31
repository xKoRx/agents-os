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

- Cerrar el paso documental que [[Research — Target Fee Inventory W1-o 2026-10-31]] dejó abierto: establecer, con **fuentes oficiales públicas y fechadas**, qué es la fee de Polymarket (fórmula, unidades, precisión, base de coste, cobro) y qué significa el campo WS `fee_rate_bps` frente a los límites maker/taker `1000` y al `fd` crudo `{e:1, r:0.05, to:true}` observados en el mercado `5784455`, con as-of `2026-10-29`. Es investigación **documental**: sin código, sin checkout, sin capturas nuevas, sin re-score, sin tocar L ni los escenarios congelados. `REAL_FEE_READY` sigue en `false` y el gap U-02 (`base_fee` ↔ `feeRate` ↔ settlement) **sigue abierto**: W1-p lo acota, no lo cierra.

## Contenido

### Resultado

- **Sí** se puede modelar costo de forma defendible para investigación **futura**, con la **fórmula documentada** `fee = C × feeRate × p × (1 - p)` y **elegibilidad `e = 1`** (el valor observado): unidades declaradas, redondeo a 5 decimales con mínimo `0.00001` y **modo de redondeo no adjudicado**, cobro sólo al taker y en matching time, base = valor de collateral; y el código oficial entrega el techo contractual en basis points por familia/versión, más el hecho de que **la curva se calcula fuera del contrato**. **No** se puede cerrar la fee histórica del episodio: el sujeto del campo WS `fee_rate_bps` no está documentado en ninguna fuente consultada, y ninguna fuente fechada demuestra la implementación desplegada ni el `MAX_FEE_RATE` vigente el 29-10-2026.

### Fórmula, unidades y precisión (evidencia directa)

- Fórmula documentada (única): `fee = C × feeRate × p × (1 - p)`; `C` = número de shares, `p` = precio de la share; `feeRate` viene de la categoría o del `feeSchedule` del mercado. "Makers are never charged fees. Only takers pay fees."
- Precisión declarada: se calcula a 5 decimales y el mínimo no nulo es `0.00001 USDC`. **El modo de redondeo (floor / ceil / nearest) no está establecido por las fuentes**, y por eso no se afirma un modo exacto para la fee cobrada.
- Unidades: la página de fees usa **USDC**; la documentación de collateral y migración del régimen V2 habla **pUSD**. Las fuentes **no prueban identidad de activo entre ambas ni conversión automática** para el periodo del episodio: el modelo debe **declarar la unidad de cash/collateral** que usa y su incertidumbre.
- Base de cobro y lados: en **BUY** la fee se **suma** al collateral gastado (el monto de una market BUY es notional pre-fee: el taker paga collateral adicional); en **SELL** la fee se **descuenta** del proceeds y el vendedor recibe el **neto**.
- Rates por categoría (tabla vigente consultada hoy, taker / maker / maker rebate): Sports `0.05` / 0 / 15%; Crypto `0.07` / 0 / 20%; Finance, Politics, Mentions, Tech `0.04` / 0 / 25%; Economics, Culture, Weather, Other-General `0.05` / 0 / 25%; Geopolitics `0` (fee-free); Combos `0.05`. Ejemplo de magnitud: 100 shares a `$0.50` → `$1.25` en Sports, `$1.75` en Crypto, `$1.00` en los grupos 0.04.
- Parámetros por mercado: `feeSchedule.rate` = "Base rate used in the fee calculation"; `feeSchedule.exponent` = "Exponent applied to the price component of the fee curve"; `takerOnly` = "fees are charged to the taker side only, and makers pay no fee"; `rebateRate` = fracción de la fee de taker devuelta al maker en reposo (`0.25` = 25%).
- Límites declarados: CLOB expone `mbf` y `tbf` ("in basis points"); `GET /fee-rate?token_id=` devuelve `base_fee` en bps (ejemplo `30`). `fd` = "Fee curve parameters for a market" con `e` = "Fee curve exponent", `r` = "Fee rate", `to` = "Whether fees apply to takers only" (Gamma usa los nombres largos `exponent`, `rate`, `takerOnly`, `rebateRate`).
- Campo WS: `last_trade_price` incluye `fee_rate_bps` opcional, descrito sólo como "Fee rate in basis points"; `side` es desde la perspectiva del taker.

### Lo que NO está documentado (y por eso no se afirma)

- **No hay fórmula publicada que incorpore el exponente.** La única fórmula documentada es `C × feeRate × p × (1 − p)`, ya simétrica respecto de `p ↔ 1 − p`; la documentación sólo **nombra** el exponente. En consecuencia, **el modelo defendible se restringe a la fórmula documentada y es elegible sólo con `e = 1`** (valor observado). **Para `e ≠ 1` no hay modelo**: no se propone ninguna forma alternativa ni generalización, y no puede afirmarse cómo cambia la curva al variar el exponente.
- **La unidad de `rate` no está declarada**: que el `0.05` observado coincida con la familia decimal de la tabla de categorías es una **hipótesis marcada**, no un hecho.
- **La correspondencia `fd{e,r,to}` ≡ `feeSchedule{exponent,rate,takerOnly}` es inferencia** (nombres y semántica compartida), no tabla de mapeo oficial publicada.
- **El papel de `mbf`/`tbf` = 1000 bps no está documentado**: los caps reales viven en familias/versiones distintas (`legacy V1 MAX_FEE_RATE_BIPS = 1000`; `ctf-exchange-v2` con valor por defecto `maxFeeRateBps = 500` y techo 100%; V2 con `MAX_FEE_RATE` inmutable y techo 100%), y **no puede asumirse cuál estaba activo ni con qué valor** el 29-10-2026.
- **El sujeto de `fee_rate_bps` no está documentado**: ni maker, ni taker, ni mercado; ni se dice si equivale al importe cobrado. El redondeo de un **importe monetario** no informa el significado de un **campo de tasa**: son objetos distintos.
- **El check `fee ≤ proceeds`** está probado en el camino de proceeds (taker SELL y maker SELL) y **no está demostrado como límite universal del lado BUY**, donde la fee se paga por encima del collateral. La división entera visible en el código es del cálculo del **techo contractual**, no una regla de redondeo de la fee cobrada.

### Mapa de implementaciones y versiones (código oficial)

- **V2 / Poly v2** (`Polymarket/polymarket-v2-external`, BUSL-1.1): la orden firmada **no lleva ningún campo de fee** (`salt`, `makerAmount`, `takerAmount`…); el operador entrega los importes ya calculados (`makerFeeAmounts`, `takerFeeAmount`); el contrato valida `fee ≤ cashValue × MAX_FEE_RATE / 10000` con `MAX_FEE_RATE` inmutable on-chain y `BPS_DENOMINATOR = 10_000`, techo `MAX_FEE_RATE_BPS_CAP = 10_000` (100%). El invariante formal (spec Certora `Exchange-FeeCap01b`) cubre maker fees, selling-taker y buying-taker y exige además `fee ≤ proceeds` del pagador.
- **CTF Exchange V2** (`Polymarket/ctf-exchange-v2`): `BPS_DENOMINATOR = 10_000`, techo 100%, `maxFeeRateBps` por defecto `500` (5%); en el matching la fee entra como importe ya calculado y se valida contra el valor de collateral del fill.
- **CTF Exchange legacy V1** (`Polymarket/ctf-exchange`): `MAX_FEE_RATE_BIPS = 1000; // 1000 bips or 10%`, archivo sin cambios desde 2022. Coincide numéricamente con el `mbf`/`tbf` = 1000 observado, pero es **analogía, no prueba**: ninguna fuente oficial liga `mbf`/`tbf` al `MAX_FEE_RATE`, y no se afirma que esa familia estuviera activa el 29-10-2026.
- **SDK legacy** (`Polymarket/clob-client`): la orden llevaba `feeRateBps` (las market orders ponían `"0"`), sin cálculo de fee ni cap de fee; `ROUNDING_CONFIG` sólo cubre price/size/amount; último commit del path 2026-03-04. Los SDK V1 dejaron de soportarse para trading el 2026-04-28.
- **SDK recomendado por la documentación consultada hoy** (`Polymarket/ts-sdk` / `@polymarket/client`): con código "fee-aware market buy orders" desde 2026-05-02 (previo al corte) y bindings de **builder** fee rates en bps (`BUILDER_FEES_BPS = 10_000`), que **no** son la fee de trading del mercado. Esto **no** certifica soporte, despliegue ni uso histórico de ese SDK el 29-10-2026. Los SDK Python y Rust oficiales no contienen archivos de fee.
- Consecuencia metodológica: como la fee se fija en el matching, **ningún backtest puede usar "la fee de la orden"**: hay que simularla con la curva y el `feeSchedule` capturado antes del timestamp de decisión.

### Matriz actual vs. histórico

Criterio: el changelog prueba **anuncios documentales con fecha** (existencia de un régimen, coeficientes anunciados, cambios de campos); **no** prueba que la fórmula exacta vigente, la política por mercado, la implementación desplegada ni el `MAX_FEE_RATE` fueran los del episodio. Lo observado en el target sólo se declara **compatible** con esos anuncios.

| Hecho | Evidencia actual (vigente 31-10-2026) | Anuncio documental previo (≤ 29-10-2026) y compatibilidad con lo observado | Qué falta |
|---|---|---|---|
| Fórmula `C × feeRate × p × (1 − p)` | `trading/fees.md` (sin fecha) | Anuncio de fees dependientes del precio (05-01-2026) y de fees por categoría (30-03-2026); **compatibilidad**: `fd.e = 1` hace aplicable la fórmula documentada sin generalización | El texto de fórmula **vigente el 29-10-2026**: no está demostrado que fuera idéntico al consultado hoy |
| Rate de la categoría Sports `0.05` | tabla de categorías | Anuncio **específico de Sports** (coeficiente taker `0.03`→`0.05`, rebate maker 25%→15%, efecto a medianoche UTC del 10-07-2026); **compatibilidad** con `fd.r = 0.05` | El anuncio **no cubre** las demás categorías que hoy muestran `0.05`; la etiqueta de fee-category del target no está capturada |
| Maker paga 0 / rebate de maker | `fees.md`, `maker-rebates.md` | Anuncios del 10-07-2026 y del 11-02-2026 (rebates por mercado); **compatibilidad** con `fd.to = true` | `rebateRate` y la política/override aplicables al target no están capturados |
| Fee en matching time, orden sin fee | `Exchange.sol` + changelog 17-04-2026 | Anuncio 17-04-2026 y go-live 28-04-2026 | Nada relevante |
| Techo contractual en bps | `Exchange.sol`, `IFees.sol`, spec Certora | **No demostrado para el 29-10-2026**: el commit de `Exchange.sol` (autor 2026-09-17, committer 2026-09-24) es fecha de commit, no de despliegue; `resources/contracts.md` no da fechas de deploy | Prueba de despliegue e implementación activa con su `MAX_FEE_RATE` (fuera de la superficie) |
| `mbf`/`tbf` = 1000 bps | `get-clob-market-info.md` (bps) | Coincidencia numérica con el cap constante del legacy V1 | Función oficial de `mbf`/`tbf`; familia/versión de cap aplicable en la fecha |
| `fee_rate_bps = "0"` | sólo "Fee rate in basis points" | No aplicable: la definición no es versionada ni fechada | Sujeto del campo |

### Conclusión acotada para el episodio del 29-10-2026

Se sostiene en tres planos, y sólo en esos:

1. **Anuncio documental previo (con fecha).** El changelog registra fees dependientes del precio en cripto 15m (05-01-2026); taker fees en NCAAB y Serie A desde 18-02-2026 con rebates por mercado (11-02-2026); "Fee Structure V2" con rates por categoría (30-03-2026); uso del `feeSchedule` por mercado (31-03-2026); fees en matching time y sin `feeRateBps` en la orden (17-04-2026); go-live de CLOB V2 (28-04-2026); y, **para la categoría Sports**, coeficiente taker `0.03`→`0.05` y rebate de maker 25%→15%, con efecto a medianoche UTC del 10-07-2026. Esto prueba **anuncios**, no la fórmula exacta vigente el 29-10-2026, ni la política por mercado, ni la implementación desplegada, ni el `MAX_FEE_RATE`.
2. **Compatibilidad de los parámetros observados del target.** `fd.r = 0.05`, `fd.e = 1`, `fd.to = true`, `fees_enabled = true`, `mbf`/`tbf` = 1000 bps son compatibles con ese régimen y con la fórmula documentada en su elegibilidad `e = 1`. El **destino deportivo** del episodio está dado por el encargo y la metadata W1-j; lo que no está capturado es la **etiqueta de fee-category / `rebateRate` / override**, lo que limita la prueba de la **política exacta** aplicable, no la identificación del evento.
3. **Modelo retrospectivo condicional.** *Si* el régimen anunciado era el vigente *y* el mercado aplicaba la curva observada, la fee de taker de un trade a precio `p` sería `C × 0.05 × p × (1 − p)`, es decir **dependiente del precio**, no una constante en bps.

Lo que **no** se puede afirmar:

- que esa fórmula, ese coeficiente, ese mercado, esa implementación o ese `MAX_FEE_RATE` fueran los del episodio;
- **que se cobrara comisión alguna** en los 78 trades ni cuánto (settlement sigue NOT_CERTIFIED, gap U-02 abierto);
- que `fee_rate_bps = "0"` signifique ausencia de cobro, fee cero del mercado o fee aplicada: el sujeto del campo no está documentado y, bajo la fórmula documentada, una tasa de taker *constante* en bps no es representable (la fee depende de `p`);
- por tanto **no se puede declarar `REAL_FEE_READY`** en ningún alcance.

### Claims no resueltos

- Sujeto de `fee_rate_bps` y significado de `0` — no documentado en `llms.txt`, api-reference, AsyncAPI ni changelog.
- Fórmula aplicable con `e ≠ 1` — no resuelta **y fuera de alcance de modelado**: las docs nombran el exponente pero no publican la expresión; no se propone forma alternativa.
- Modo de redondeo de la fee cobrada — no adjudicado; a lo sumo banda conservadora declarada como hipótesis de modelado, no regla del venue.
- Unidad de cash/collateral del episodio — `USDC` (fees) frente a `pUSD` (collateral V2), sin identidad demostrada ni conversión.
- Cap vigente (familia/versión y valor) el 29-10-2026 — sin prueba de despliegue (cadena fuera de superficie).
- Política/rebate/override por fee-category del target — no capturados; el destino deportivo sí está dado.
- Fee efectivamente cobrada en los 78 trades — sin settlement observado ni vínculo campo↔importe.

### Límites de esta investigación

- **Consultas web:** 78 llamadas WebFetch en la ventana medida `2026-10-31T11:35:38.606Z`–`2026-10-31T11:44:35.301Z` (medición del supervisor vía SQLite): 34 entradas de evidencia sobre 31 URLs distintas con éxito, 3 rutas denegadas, 4 HTTP 404 y 1 URL oficial fuera de allowlist no intentada.
- **Rutas denegadas (3):** `raw.githubusercontent.com/Polymarket/ts-sdk/main/packages/client/src/actions/orders/{estimate.ts,market.ts,settlement.ts}`, todas con el error literal `Outside immutable W1-p scope`. El supervisor verificó en el código del hook que el filtro rechaza el substring `/actions` en rutas GitHub/raw y por eso también coincide con rutas de código del SDK; el control no se alteró y la información no se leyó por otra vía. **La existencia y el contenido de esos archivos NO quedan establecidos por esos intentos**: no se afirma que existan ni qué contienen. No se reintentó ni se eludió. Este bloqueo no impide el modelo documentado con `e = 1`; limita la verificación detallada de los helpers del SDK.
- **Otras ausencias:** la visualización oficial de la curva (`datawrapper.dwcdn.net/dJ74e/`) está fuera de la allowlist de dominio y no se intentó; `api.github.com/repos/Polymarket/{docs,polymarket-docs,exchange,exchange-core}` → HTTP 404 (ausencia de ese repo, no del tema); el árbol recursivo de `ts-sdk` vino truncado, por lo que la ausencia de "fee" en ese listado no prueba ausencia en el repo.
- **WebFetch devuelve resúmenes de IA, no cuerpos:** no hay hash de origen ni de cuerpo de ninguna fuente.
- **Vigencia:** toda página consultada es la documentación vigente el 2026-10-31; consultarla **no** prueba que rigiera el 29-10-2026. Sólo el changelog fechado aporta histórico, y una fecha de commit no es fecha de despliegue.
- **Atribución de modelo:** el runtime registra el modelo del turno principal (MiniMax) y no desglosa las llamadas auxiliares de WebFetch; el supervisor verificó en el código de la CLI que el modelo del turno se propaga al contexto de WebFetch sin selección de fallback.
- No se usaron endpoints de mercado, libro, órdenes, RPC, cuentas ni transacciones; **no se requiere cuenta propia ni cobro propio real** para avanzar la etapa offline.
- No se modificó la regla de L (sigue pendiente del Owner), ni los escenarios congelados A/S, ni `REAL_FEE_READY`.

## Fuentes

- Vault: [[Research — Target Fee Inventory W1-o 2026-10-31]] (inventario offline previo y gap U-02), [[Research — Default Suite Isolation W1-nR 2026-10-30]], [[Polymarket Engine — MVP]].
- Documentación oficial (consultada 2026-10-31): `docs.polymarket.com/llms.txt`, `/trading/fees.md`, `/market-data/market-details.md`, `/market-data/realtime-data.md`, `/market-data/prices-order-books.md`, `/api-reference/markets/get-clob-market-info.md`, `/api-reference/markets/get-market-by-id.md`, `/api-reference/wss/market.md`, `/asyncapi.json`, `/api-reference/market-data/get-fee-rate.md`, `/api-reference/market-data/get-fee-rate-by-path-parameter.md`, `/api-reference/trade/post-a-new-order.md`, `/changelog/predictions.md`, `/programs/maker-rebates.md`, `/programs/taker-rebates.md`, `/trading/place-orders.md`, `/concepts/order-lifecycle.md`, `/concepts/markets-events.md`, `/migrate/polymarket-v2/api-integrations.md`, `/migrate/polymarket-v2/overview.md`, `/migrate/data-api-v1-to-v2.md`, `/resources/contracts.md`, `/getting-started/typescript.md`.
- Código oficial: `Polymarket/polymarket-v2-external` (`src/exchange/Exchange.sol`, `OrderStructs.sol`, `MATCH_ORDERS_LIFECYCLE.md`, `certora/specs/Exchange-FeeCap01b.spec`; BUSL-1.1), `Polymarket/ctf-exchange-v2` (`src/exchange/mixins/Fees.sol`, `interfaces/IFees.sol`, `mixins/Trading.sol`), `Polymarket/ctf-exchange` (`src/exchange/mixins/Fees.sol`, `interfaces/IFees.sol`), `Polymarket/clob-client` (`src/order-builder/helpers.ts`), `Polymarket/ts-sdk` (`packages/bindings/src/clob/builder.ts`).
- API pública de GitHub (sin token) para metadatos, árboles e historial de commits por path.
- Artefactos del shot: `validated-baseline/w1-p-fee-documentary-20261031/source-ledger.json` (S01–S34 + denegaciones + claims no resueltos + `corrections_applied`), `research.md`, `prereg-draft.md` (DRAFT_NOT_APPROVED, incremento offline de conformidad del modelo con `e = 1`), `run-receipt.json`, `capability.json`, `scout-pack.json`.

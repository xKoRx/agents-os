#Polymarket — Technical Platform Map — synced 2026-09-17

```text
SYNC_DATE: 2026-09-17 UTC
SYNC_TIME_UTC: 2026-09-17 02:34:53 UTC (cierre de compilación del documento; fuentes verificadas durante esta revisión)
POLYMARKET_DOCS_LAST_OBSERVED_CHANGE: NO PUBLICADO como fecha global del corpus;
  páginas vivas verificadas el 2026-09-17 UTC. SDK Changelog observado en TypeScript v0.10.0.
RESEARCHER: GPT-5.6 Sol — Senior Protocol / API Contract Auditor
SCOPE: Prediction Markets; Perps excluido salvo infraestructura explícitamente compartida.
NETWORK: Polygon mainnet, chainId 137.
STATUS: DOCUMENTO CORREGIDO; CERTIFICACIÓN CONTRACTUAL INTEGRAL PENDIENTE
  mientras subsistan los RESEARCH GAPS expresos de §24. No habilita conversión
  NegRisk Protocol-v2 en vivo sin ruta/ABI verificados.
```

**Convenciones.** `[Sxx]` remite exclusivamente a la fuente oficial con URL completo en §26. `CURRENT` = documentado en la documentación consultada; `LEGACY` y `DEPRECATED` conservan su alcance; `NOT DOCUMENTED` significa que las autoridades consultadas no establecen esa garantía; `RESEARCH GAP` significa que hay material oficial cuya extracción/verificación contractual NO se completó. Un dato dinámico es un snapshot de 2026-09-17, nunca una constante. Los ejemplos con marcadores `<...>` son esquemas didácticos **no transmisibles**. El contenido de SDK y sus normalizaciones NO sustituye la representación HTTP. Se preservan contradicciones observadas. [S01][S32][S33]

## 1. Superficies, hosts y autoridad

| Superficie | Base de producción | Protocolo; auth; dirección | Entidades/uso | Autoridad y estado |
|---|---|---|---|---|
| Gamma | `https://gamma-api.polymarket.com` | REST público R | Event, Market, Tag, Series, deportes, rules | [S02][S39] CURRENT |
| CLOB | `https://clob.polymarket.com` | REST R público; L1/L2/Builder según ruta; W | book, order, trade, fees, rewards | [S03][S40] CURRENT |
| Market WS | `wss://ws-subscriptions-clob.polymarket.com/ws/market` | WS R público | snapshots, deltas y lifecycle | [S08][S45] CURRENT |
| User WS | `wss://ws-subscriptions-clob.polymarket.com/ws/user` | WS R L2 | orden y fill propios | [S09][S46] CURRENT |
| Data v2 | `https://data-api.polymarket.com/v2` | REST público R | actividad, posiciones, historia, resolución | [S30][S41] CURRENT |
| Data v1 | mismo host, rutas previas `/v1` y sin versión | REST R | compatibilidad parcial | [S30] MIGRATING |
| RTDS | `wss://ws-live-data.polymarket.com` | WS R público para topics públicos | precios externos, Chainlink, otros topics | [S11][S49] CURRENT |
| Sports | `wss://sports-api.polymarket.com/ws` | WS R público | marcador/estado de juegos | [S10][S47] CURRENT |
| Combo/RFQ | `https://combos-rfq-api.polymarket.com` | REST R/W, maker auth en writes | legs, quotes, confirmations | [S29][S43] CURRENT |
| RFQ requester | `https://combos-rfq-gateway-requester-api.polymarket.com` | REST L2 W/R | RFQ create/status/accept | [S28] CURRENT; fuera del OpenAPI maker [S43] |
| RFQ quoter | `wss://combos-rfq-gateway-quoter.polymarket.com/ws/rfq` | WS quoter auth bidireccional | RFQ, quote, trade | [S48] CURRENT |
| Combo builder | `https://combos-rfq-gateway-builder.polymarket.com` | REST Builder | RFQ delegado | [S28a][S34] CURRENT |
| Collateral return | `https://combos-rfq-collateral-return.polymarket.com` | REST/workflow | devolución de garantía Combo | [S28b] CURRENT |
| Relayer | `https://relayer-v2.polymarket.com` | REST R/W Builder/Relayer en submit | transacciones gasless/deploy/status | [S42][S13] CURRENT |
| Bridge | `https://bridge.polymarket.com` | REST R/W según ruta | funding/withdrawal únicamente | [S44] CURRENT |
| Contratos | Polygon 137 | EVM, firma/transacción | collateral, positions, settlement | [S25][S34] CURRENT según contrato |

Restricción importante: Gamma describe, CLOB ejecuta, Data agrega historia, el Relayer transmite transacciones y la cadena finaliza movimientos. Ninguna de esas superficies es sustituto universal de las demás. Los rate limits generales son por IP y el trading agrega buckets por signer (§18). [S02][S19][S20]

```text
Predictions
├─ Gamma / Event / Market / token IDs
├─ CLOB REST ─┬─ Market WS (asset IDs)
│             └─ User WS (credentials; condition IDs)
├─ Data API v2 / posiciones, actividad, trades y resolución
├─ Sports WS / RTDS ─ Chainlink y referencia de precios
├─ Auth L1(EIP-712) / L2(HMAC) / wallet EOA, Proxy, Safe, Deposit
├─ CTF-era: Conditional Tokens + adapters + Exchange v2
├─ Protocol-v2: Router + PositionManager + módulos
├─ NegRisk: legado CTF ≠ módulo Protocol-v2
├─ Combos: combinatorial positions + Exchange v3 + RFQ
├─ UMA / oracle / payout ─ redemption
├─ Programs: maker rebates / taker rebates / liquidity rewards / builder fees
├─ Relayer (gasless)
└─ Bridge (depósito/retiro; no matching)
```

## 2. Modelo de entidades e invariantes

| Entidad canónica | Identidad; procedencia | Relaciones; mutabilidad/lifecycle |
|---|---|---|
| `Event` | `id` numérico Gamma, `slug` | agrupa N `Market`; tags/series/sports, fechas, flags y metadata pueden evolucionar; no es asset negociable [S04]. |
| `Market` | `id` numérico Gamma, `conditionId` donde aplique | pregunta binaria, outcomes, token IDs, rules/description/resolution source, active/closed, negRisk, enableOrderBook, precision/rewards; `market.id` NO es `conditionId` [S04][S06]. |
| `Outcome` | etiqueta Yes/No + posición/token | cada market binario tiene dos outcomes; YES/NO no es `BUY/SELL` [S05]. |
| `CTF Condition` | `bytes32 condition_id` | une mercado CTF ↔ oracle ↔ CLOB ↔ Data; distinto del question ID [S05][S27]. |
| `Token` / `assetId` | ERC-1155 `uint256` decimal como string para CTF; protocolo-neutral en SDK v2 | identificador efectivo de `/book`, orden y trades, distinto de Gamma market ID [S06][S33]. |
| `PositionId` v2 | ID protocol-neutral/estructurado | Router/PositionManager; NO inferir que es necesariamente ERC1155 de CTF [S33][S34b]. |
| `Series`, `Tag` | IDs Gamma | agrupación y clasificación; `Category` de programas no es necesariamente entidad universal de ID estable [S39]. |
| `Order` | hash hex CLOB | intención firmada off-chain, estado vivo/cancelado/matched y fills vinculados [S15][S16]. |
| `Trade` / fill | `id` servicio | maker/taker order IDs, `asset_id`, condición, tamaño/precio, estado de settlement y tx hash [S09][S16]. |
| `Wallet` / `signer` / `maker` | direcciones EVM 20 bytes | signer controla clave; maker/funder mantiene collateral; Deposit Wallet = contrato, no necesariamente EOA [S13]. |
| `API credential` | `apiKey` servicio | L2 triple apiKey/secret/passphrase; asociada a signer/scope, NO es order signature [S03]. |
| `NegRisk Event` | Evento Gamma + flag/contexto | outcomes mutuamente excluyentes en construcción aplicable; versión CTF/v2 importa [S26][S34b]. |
| `Placeholder`, `Other` | slots/outcomes augmented NegRisk | placeholder se puede nombrar; `Other` representa lo que aún no está asignado; cambia su conjunto semántico [S26]. |
| `Combo`, `RFQ`, `Quote` | posición/condition y RFQ/quote IDs | legs → Combo → cotización → firma Exchange-v3 → fill, no es `convertPositions` [S28][S29]. |
| `Resolution`, UMA Proposal/Dispute | pregunta/condition + tx/oracle IDs | end, proposal, liveness, dispute, result, redeemable y redeemed son etapas distintas [S27][S41]. |
| `Reward` / `Rebate` | mercado/wallet/programa/fecha | configuración vigente y earnings no garantizan archivo histórico inmutable [S22][S23][S24]. |

```text
Gamma Event.id / slug
  └─ Market.id / slug
       ├─ conditionId (CTF bytes32 o identidad normalizada según versión)
       ├─ outcomes[] / clobTokenIds[]  → YES assetId, NO assetId
       ├─ negRisk, enableOrderBook, tick, min-size, rules, dates
       └─ market.version (discriminador expuesto por SDK vigente)
YES/NO assetId → CLOB book → signed Order(tokenId, maker, signer)
Order hash → Trade.id [taker_order_id | maker_orders[].order_id]
Trade.transaction_hash → Polygon → Position(wallet, asset/positionId)
Market.conditionId / questionId → UMA Resolution → payout → redeem
Combo: leg positionIds → derived condition/position → RFQ id → quote id
       → Exchange-v3 order → trade/settlement → Combo position
```

### Namespace de IDs

| ID | Tipo wire; scope | Relación / ¿input directo de trading? |
|---|---|---|
| `event.id`, `market.id`, `series.id`, `tag.id` | numérico Gamma, con strings numéricos posibles | discovery; NO token para `/order` |
| `slug` | string URL-safe | busca Event o Market; no es ID de matching |
| `condition_id` | CTF bytes32 `0x` + 64 hex, normalizable en v2 | join market CLOB/Data/oracle, NO reemplaza asset para order |
| `question_id` | bytes32 pregunta oracle | resolución/derivación de condición; no token negociable |
| `clobTokenIds`, CTF token ID | decimal `uint256` (NO float) | YES/NO de Gamma, válido para CLOB CTF |
| `asset_id` / `token_id` | string, token CTF o posición protocol-neutral según versión | SÍ input book/order, validar contexto de versión |
| v2 `positionId` | identificador v2 específico, string | Exchange-v3/PositionManager; no equiparar con CTF `tokenId` |
| `orderID` | hash hex | GET `/data/order/{id}`, cancel, join WS/trade |
| `trade.id` | ID opaco servicio | join trade/match, no es orden |
| tx hash | `0x` + 64 hex | settlement Polygon |
| wallet/maker/signer/funder | `0x` + 40 hex | owner/signer/collateral; roles NO necesariamente idénticos |
| Deposit Wallet | dirección de contrato EVM | maker/funder y auth EIP-1271/ERC-7739 |
| `apiKey` | UUID/string servicio | propietario de credenciales L2, wrapper `owner`, no wallet address |
| `rfq_id`, `quote_id` | opacos RFQ | correlación de request/quote/accept |
| `transactionID` Relayer | opaco/UUID | GET `/transaction?id=` → state/transactionHash |

La regla principal del contrato de identidad: `Event.id ≠ Market.id ≠ conditionId ≠ tokenId ≠ orderID`; las APIs usan cada uno en filtros distintos. El campo `markets` del User WS acepta **condition IDs**; `assets_ids` del Market WS acepta **asset IDs**. [S06][S08][S09]


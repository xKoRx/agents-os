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

## 3. Endpoint Catalog — hosts, rutas y contratos base

Para compactar las tablas, `G=https://gamma-api.polymarket.com`, `C=https://clob.polymarket.com`, `D=https://data-api.polymarket.com`, `R=https://relayer-v2.polymarket.com`, `Q=https://combos-rfq-api.polymarket.com`, `QR=https://combos-rfq-gateway-requester-api.polymarket.com`, `B=https://bridge.polymarket.com`. Método + ruta son **HTTP**, no nombres de métodos SDK. `L1` usa firma ClobAuth; `L2` usa API triple + HMAC. Si una ruta está documentada por el error reference pero falta su esquema completo, se declara gap de schema, NO un contrato inventado. [S01][S03][S39][S40][S41][S42][S43][S44]

### 3.1 Gamma (G, lectura pública)

| Método y path | Request / paginación | Output/IDs críticos | Fuente |
|---|---|---|---|
| `GET /status` | — | health | [S39] |
| `GET /events` | `limit`, `offset`, `active`, `closed`, `id`, `slug`, tags/series, orden, fechas según filtro del contrato | Event[] con `id`, `slug`, `markets[]`, condition/token y rules anidadas | [S06][S39] |
| `GET /events/keyset` | cursor/keyset y límite, estado | eventos + cursor; no crear cursor propio | [S06][S39] |
| `GET /events/{id}`; `GET /events/slug/{slug}` | ID Gamma o slug | Event individual + Market[] | [S39] |
| `GET /markets` | `limit`, `offset`, `id`, `slug`, `closed`, `active`, fechas y filtros documentados | Market[]/ids, `conditionId`, `clobTokenIds`, `negRisk`, rules, enableOrderBook | [S06][S39] |
| `GET /markets/keyset` | cursor/keyset | Markets + cursor | [S06][S39] |
| `GET /markets/{id}`; `GET /markets/slug/{slug}` | Gamma market ID o slug | Market | [S39] |
| `GET /events/{id}/tags`; `GET /markets/{id}/tags` | Gamma ID | Tag[] | [S39] |
| `GET /markets/{id}/description` | Gamma market ID | descripción/rules relacionadas | [S39] |
| `POST /markets/information`; `POST /markets/abridged` | batch body según OpenAPI | Markets batch, `id`/condition/tokens | [S39]; **RESEARCH GAP**: cuerpo/restricciones exactas no reextraídos |
| `GET /tags`; `GET /tags/{id}`; `GET /tags/slug/{slug}` | filtros + offset según ruta | Tag.id/slug | [S39] |
| `GET /tags/{id}/related-tags`; `GET /tags/slug/{slug}/related-tags`; `GET /tags/{id}/related-tags/tags`; `GET /tags/slug/{slug}/related-tags/tags` | estado/filtros | ids/objetos relacionados | [S39] |
| `GET /series`; `GET /series/{id}`; `GET /series-summary/{id}`; `GET /series-summary/slug/{slug}` | offset o id/slug | Series ID y agrupación | [S39] |
| `GET /sports`; `GET /sports/market-types`; `GET /teams`; `GET /teams/{id}` | filtros liga/equipo cuando aplica | sport/team metadata | [S39] |
| `GET /public-search` | query y filtros entity/status | resultados Event/Market | [S39] |
| `GET /public-profile`; `GET /profiles/user_address/{addr}` | wallet | perfil público | [S39] |
| `GET /comments`; `GET /comments/{id}`; `GET /comments/user_address/{addr}` | filtro/offset/id | comentarios | [S39] NO crítico para MVP |
| `GET /events/results`; `GET /events/{id}/tweet-count`; `GET /events/{id}/comments/count`; `GET /events/creators`; `GET /events/creators/{id}`; `GET /series/{id}/comments/count`; `GET /events/pagination` | filtros propios | metadata/legacy | [S39] operaciones `x-excluded` o no esenciales; NO usarlas como contratos MVP sin confirmar vigencia |

**Discovery mini-contract.** `GET G/events?closed=false&limit=...&offset=...` lista eventos; `GET G/events/slug/{slug}` resuelve un evento; recorrer `markets[]`. Alternativamente `GET G/markets/slug/{slug}`. En Market leer `id`, `conditionId`, `clobTokenIds` (**Gamma puede devolverlos como JSON-array codificado dentro de string**), `outcomes` (alineados posicionalmente), `enableOrderBook`, `negRisk`, `active/closed`, `startDate/endDate`, `description/rules`, `resolutionSource`, fee/reward flags. No se documenta una garantía de snapshot consistente entre páginas de offset ante altas concurrentes. [S04][S06]

### 3.2 CLOB market data (C; público, sin auth)

| Método y path | Request indispensable; paginación | Response/IDs/error principal | Fuente |
|---|---|---|---|
| `GET /time` | — | tiempo servidor Unix | [S40] |
| `GET /book?token_id={assetId}` | `token_id` obligatorio | `market` condition, `asset_id`, `timestamp`, `hash`, `bids[]`,`asks[]`, `min_order_size`,`tick_size`,`neg_risk`; 400 token inválido, 404 sin book | [S07][S40][S18] |
| `POST /books` | JSON array `{token_id:string}[]`, hasta **500** | array de books por asset; 400 malformed/batch excesivo | [S07][S40][S18] |
| `GET /price` | `token_id`, `side=BUY|SELL` | `{price: string}`; 400 side/token, 404 book | [S40][S18] |
| `GET /prices` | `token_ids` y `sides` CSV alineados | map asset→side→price | [S40] |
| `POST /prices` | array `{token_id,side}` | map asset→side→price; 400 payload/side/batch | [S40][S18] |
| `GET /midpoint`; `GET /midpoints`; `POST /midpoints` | single token; CSV/list o array de `{token_id}` según variante | precio medio por asset | [S07][S40] |
| `GET /spread`; `POST /spreads` | token individual o array `{token_id}` | spread decimal string, map en batch | [S07][S40] |
| `GET /last-trade-price`; `GET /last-trades-prices`; `POST /last-trades-prices` | token single, CSV batch o body array, máximo documentado POST 500 | último trade precio, side/time según variante | [S40] |
| `GET /fee-rate?token_id={assetId}`; `GET /fee-rate/{token_id}` | token/asset ID | `{base_fee:int64}` **basis points**; no confundir con coeficiente decimal categoría de [S21] | [S21][S40][S40a] |
| `GET /tick-size?token_id={assetId}`; `GET /tick-size/{token_id}` | token | tick efectivo; 400 id/404 mercado | [S40][S18] |
| `GET /neg-risk?token_id={assetId}` | token | flag NegRisk del contexto CLOB; no discrimina por sí solo generación de position protocol | [S40] |
| `GET /prices-history` | `market={assetId}` obligatorio; `startTs`,`endTs`, `interval` (`max`,`all`,`1m`,`1w`,`1d`,`6h`,`1h`), `fidelity` minutos | `{history:[{t,p}]}`; precio histórico, NO L2; 400 filtros | [S40][S31] |
| `POST /batch-prices-history` | batch de asset/rango/fidelity según schema | series múltiples; **RESEARCH GAP**: body límite exacto no revalidado | [S40] |
| `GET /clob-markets/{condition_id}` | condition ID | trading market, `fd`/fees, tokens, delay, precision/status | [S40][S40b] |
| `GET /markets-by-token/{token_id}` | asset ID | market/condition reverse mapping | [S40] |
| `GET /simplified-markets`; `GET /sampling-markets`; `GET /sampling-simplified-markets` | `next_cursor` opaco, filtros endpoint | `{data:[...],next_cursor,count,limit}`, condición y tokens | [S40] |
| `GET /markets/live-activity`; `GET /markets/live-activity/{id}` | market/criterios según ruta | actividad corriente | [S40] |
| `GET /ohlc`; `GET /orderbook-history` | `startTs` requerido; `/ohlc` necesita `asset_id`, fidelity enum `1m,5m,15m,30m,1h,4h,1d,1w`; `/orderbook-history` necesita `market` condition o `asset_id`; `limit<=1000` | mencionados explícitamente por referencia vigente de errores; esquema/retención completo **RESEARCH GAP** [S18] |

`GET /fee-rate` es fuente de tarifa base en **bps**; no convertir automáticamente `base_fee=30` en el `feeRate=0.07` de fórmula category sin confirmar relación de campos: son superficies y escalas diferentes. La migración CLOB v2 añade parámetros efectivos `fd.r`, `fd.e` y `fd.to` en CLOB market info. El contrato de cálculo de fee por trading no debe deducirse de un solo campo cuyo significado esté ambiguo. [S21][S40a][S32a]

**Book mini-contract:** `bids:[{price:"0.50",size:"40"}]`, `asks:[...]`, `asset_id` token, `market` condition, `timestamp` epoch **ms string**, `hash` opaco, `tick_size`, `min_order_size`, `neg_risk`. REST publica bids ascendentes y asks descendentes; **último elemento** es mejor bid/ask. `POST /books` devuelve snapshots por token pero NO garantiza snapshot atómico entre assets ni correspondencia con secuencia WS. `hash` es campo de snapshot; no está documentado un checksum reproducible/chain para detectar pérdidas. [S07][S08]

El `midpoint=(bestBid+bestAsk)/2` no es fill price; `last_trade_price` es histórico reciente. UI suele mostrar midpoint y, si spread excede **$0.10**, último trade. BUY cruza asks y SELL bids; precios mostrados ≠ ejecución garantizada en tamaño real. [S07][S07a]

### 3.3 CLOB auth, órdenes, ledger y programas (C)

| Método y path | Auth | Request / response indispensable | Página/cap/errores; fuente |
|---|---|---|---|
| `POST /auth/api-key` | L1 | headers `POLY_ADDRESS,SIGNATURE,TIMESTAMP,NONCE`; `{apiKey,secret,passphrase}` | 400/401 [S03][S34c] |
| `GET /auth/derive-api-key` | L1 | mismos headers; mismas credenciales | 400/401 [S03][S34c] |
| `GET /auth/api-keys` | L2 | sin body; `{apiKeys:[...]}` | 500 [S34c][S18] |
| `DELETE /auth/api-key` | L2 | **sin body**, borra *credencial autenticada*; wire respuesta texto JSON `"OK"` en SDK vigente | 500 [S34c][S18] |
| `POST /auth/builder-api-key` | L2 | crea builder triple de credenciales | 500 [S34c][S18] |
| `GET /auth/builder-api-key` | L2 | lista claves Builder | 500 [S34c][S18] |
| `DELETE /auth/builder-api-key` | headers Builder/credenciales según ruta y current SDK | revoca clave Builder; respuesta `"OK"`; request headers precisos **RESEARCH GAP** [S34c][S18] |
| `POST /order` | L2 + orden firmada | wrapper/DTO de §7; `{success,errorMsg,orderID,status,makingAmount,takingAmount,transactionsHashes,tradeIDs}` | no idempotency key [S15][S40] |
| `POST /orders` | L2 + firma individual | array wrappers, **1–15 órdenes**; array respuesta por orden, posibles resultados mixtos | [S15][S40][S18] |
| `GET /data/order/{orderID}` | L2 | hash exacto → orden incluso terminal si todavía retenida | 400 ID/500 [S16] |
| `GET /data/orders` | L2 | opcionales `id`,`market={conditionId}`,`asset_id`; `next_cursor` | estado actual + filtro por ID para terminal [S16] |
| `GET /data/trades` | L2 | `id`, `market` condition, `asset_id`, `maker_address`,`after`,`before`, `next_cursor`; `{limit,next_cursor,count,data:[trade...]}` | 400 filtro/500, NO incluye órdenes nunca llenadas [S16] |
| `GET /builder/trades` | Builder auth según operación | trades atribuidos a builder, cursor/filtros | [S16][S40] |
| `DELETE /order` | L2 | JSON `{"orderID":"<hash>"}` → `{canceled:[],not_canceled:{...}}` | cuerpo HMAC exacto; 400 id [S16] |
| `DELETE /orders` | L2 | JSON array de order hashes; máximo **1.000** IDs por request desde 2026-06-15; output cancelación parcial | **CONTRADICCIÓN DOCUMENTAL:** la prosa de Manage Orders [S16] aún indica 3.000, pero changelog oficial con fecha efectiva posterior lo redujo explícitamente a 1.000 [S32]. Prevalece la actualización específica fechada; OpenAPI raw no contrastado [S40] |
| `DELETE /cancel-all` | L2 | sin body → `{canceled,not_canceled}`; scoped credenciales | [S16] |
| `DELETE /cancel-market-orders` | L2 | body `{market:"conditionId"}` o `{asset_id:"tokenId"}`; al menos un filtro | output cancelación parcial [S16] |
| `GET /order-scoring`; `GET /orders-scoring`; `POST /orders-scoring` | L2 | `order_id` o IDs en query/body → bool/map id→bool | elegibilidad instantánea [S16][S24][S40] |
| `GET /balance-allowance` | L2 | `asset_type`,`token_id` cuando conditional, `signature_type`; balance y allowances | CLOB cache ≠ ERC20 allowance on-chain; [S18][S40] |
| `GET /balance-allowance/update` | L2 | mismos selectores, solicita refresco de cache de servicio; respuesta exacta/reacción interna **RESEARCH GAP** | ruta soportada por SDK oficial Rust v2 y documentación de límites [S20c][S19] |
| `POST /heartbeats` | L2 | heartbeat account API | no confundir con PING WS [S40] |
| `GET /auth/ban-status`; `GET /auth/ban-status/closed-only` | L2 | account restriction; segundo retorna `{closed_only:boolean}` | closed-only admite reducciones únicamente [S16][S40] |
| `GET /notifications`; `DELETE /notifications` | L2; auth/body de borrado sin revalidar | superficie de notificaciones cuenta, **NO requerida para reconciliar fills** | path+methods observados en SDK clásico; exact schema CURRENT **RESEARCH GAP** [S40][S36a] |
| `GET /rewards/markets/current` | público | config activa por mercado | [S24][S40] |
| `GET /rewards/markets/{id}`; `GET /rewards/markets/multi` | público | config raw individual/múltiple | [S24][S40] |
| `GET /rewards/user`; `GET /rewards/user/total`; `GET /rewards/user/percentages`; `GET /rewards/user/markets` | L2 o público según endpoint; consultar auth propia | earnings, totals, percentage, mercado/config; params user,date,signature_type según ruta | [S24][S40] **RESEARCH GAP** campos/auth por ruta no extraídos |
| `GET /rebates/current` | credencial maker según spec | rebate actual | [S23][S40] **RESEARCH GAP** query/auth/schema exactos |

**Notas sobre actualidad y errores.** `/auth/builder-api-key` se mantiene como gestión de credenciales Builder; builder HMAC sigue pertinente al Relayer, pero atribución de órdenes CLOB v2 se codifica en signed `builder:bytes32`, no antiguos headers Builder por orden. Las rutas RFQ antiguas `/rfq/*` en el OpenAPI CLOB NO equivalen a Exchange-v3 Combos RFQ, y se aíslan como COMPATIBILITY/LEGACY hasta establecer su vigencia específica. En `POST /orders`, la referencia oficial muestra una anomalía: un elemento de rechazo post-only puede llevar `success:true` con `errorMsg` no vacío y `orderID:""`; por tanto `success` aislado NO siempre constituye prueba suficiente de aceptación por elemento. [S18][S32a]

**Order read mini-contract wire:** `{id,market,asset_id,owner,maker_address,side,price,original_size,size_matched,outcome,order_type,status,associate_trades,created_at,expiration}`. `market` es condition ID, `created_at` epoch segundos; `expiration` segundos o `0`. El SDK transforma a camelCase, decimales tipados e ISO strings, que NO son campos wire. [S16]

**Trade read mini-contract wire:** `{id,market,asset_id,owner,maker_address,taker_order_id,side,trader_side,price,size,outcome,status,fee_rate_bps,bucket_index,transaction_hash,maker_orders:[{order_id,asset_id,maker_address,owner,side,price,matched_amount,outcome,fee_rate_bps}],match_time,last_update}`. `match_time`/`last_update` epoch **segundos string** en ejemplo HTTP. **CORRECCIÓN CONTRACTUAL:** la referencia HTTP CURRENT `GET /data/trades` publica un objeto paginado `{limit,next_cursor,count,data:[trade...]}` y cursor terminal `"LTE="` [S16a]. El SDK normaliza adicionalmente en algunas rutas; NO imponer su envelope `{data,has_more,next_cursor,total_count}` al wire ni tratar un ejemplo legacy de array desnudo como respuesta actual. Para unir orden ↔ fills usar `taker_order_id` y cada `maker_orders[].order_id`; `trade.id` y `transaction_hash` conectan ledger con settlement. [S16][S09]

**Cancel mini-contract:** JSON response API `{"canceled":["orderID"],"not_canceled":{"orderID":"order already matched"}}`. La cancelación ya no puede deshacer fills previos. Pérdida de respuesta de DELETE implica volver a consultar por order ID y `size_matched`/trades antes de repetir; no se publica idempotency-key de cancel. [S16]


### 3.4 Data API v2 (D2), Data API v1 y migración

Host D2: `https://data-api.polymarket.com`; todas las rutas siguientes llevan prefijo literal `/v2`; GET públicos de consulta, sin credenciales CLOB. Respuesta v2: objeto `data` más `pagination` cuando aplica; cursores acuñados por servidor, sin paginación offset en estas familias. El identificador canónico de filtro de mercado pasa a `condition`/`condition_id`; **no** sustituirlo por el `market.id` de Gamma. Los límites, parámetros exactos opcionales y nombres de cada envelope deben observar el OpenAPI correspondiente: la tabla es inventario de operaciones, no una promesa de parámetros universales. [S30][S41]

| Método/path exacto | Objeto de consulta y campos críticos | Paginación/IDs |
|---|---|---|
| `GET /v2/approvals` | permisos de wallet; filtro `user` | wallet/spender |
| `GET /v2/positions` | posiciones por `user`, `condition`, `status` cuando habilitado; estados `OPEN`, `REDEEMABLE`, `CLOSED` | cursor; wallet, condition, asset/position ID |
| `GET /v2/positions/combos` | posiciones Combo por wallet/estado | cursor; posición/legs |
| `GET /v2/user-pnl` | serie de PnL de wallet | tiempo, wallet |
| `GET /v2/user-stats` | estadísticas agregadas | wallet |
| `GET /v2/user-volume` | volumen por wallet/tiempo | período, wallet |
| `GET /v2/value` | valor por wallet/conditions | wallet, condition |
| `GET /v2/activity` | actividad de wallet; tipos/intervalos | cursor, actividad/tx |
| `GET /v2/activity/combos` | actividad de Combos | cursor, RFQ/combo/tx si provistos |
| `GET /v2/trades` | operaciones públicas/históricas por condition, asset, wallet y rango | cursor, trade, tx; NO órdenes sin fill |
| `GET /v2/holders` | tenedores de mercado | condition, wallet |
| `GET /v2/live-volume` | volumen evento | event ID |
| `GET /v2/oi` | open interest | condition |
| `GET /v2/prices-history` | serie temporal de precio | asset, tiempo/bucket; no es L2 |
| `GET /v2/resolutions` | estado/historia de resolución | question/condition/event según filtro; resolver IDs entre objetos |
| `GET /v2/biggest-winners` | ranking histórico | cursor, wallet |
| `GET /v2/builders/leaderboard` | ranking builders | cursor, builder |
| `GET /v2/builders/volume` | volumen builders | período, builder |
| `GET /v2/leaderboard` | ranking operadores | cursor, wallet |
| `GET /v2/status` | frescura / estado servicio | sin cursor |

**Mini-contract crítico de posiciones:** entrada GET `/v2/positions?user=<0x...>&status=OPEN` o `REDEEMABLE` o `CLOSED` (verificar aceptación exacta de filtro en schema antes de usar en vivo); campos de respuesta de interés: posición/asset ID, condition, wallet, size/balance, price/value, PnL y resolución cuando presentes. `data:null` y `data:[]` son resultados de lectura legítimos de v2. Un cursor sólo es reutilizable con la combinación de endpoint/filtros original: ciertas familias dan HTTP 400 si cambia el filtro, trades/activity pueden reanclarse; el cursor no codifica un snapshot global inmutable. El detalle de todos los nombres wire de posición y de la paginación de cada familia en los OpenAPI no fue reextraído íntegramente en esta pasada: **RESEARCH GAP**, no inventar struct de Go a partir de este resumen. [S30][S41]

**V1 residual (compatibilidad, NO confundir con D2):** `GET /positions`, `/closed-positions`, `/value`, `/traded`, `/activity`, `/trades`, `/holders`, `/oi`, `/live-volume`, `/v1/market-positions`, `/v1/positions/combos`, `/v1/activity/combos`, `/v1/leaderboard`, `/v1/builders/leaderboard`, `/v1/builders/volume`, `/v1/accounting/snapshot`. La migración explícita orienta posiciones v1 abierta/cerrada al `/v2/positions` con filtro `status`; la función accounting snapshot permanece v1. No trasladar offsets ni alias `market` de v1 a D2. [S30][S32a]

### 3.5 Relayer (R), Deposit Wallet, Combos y Bridge

| Host/surface | Método/path exacto | Auth | Request → respuesta / ID | Autoridad |
|---|---|---|---|---|
| R `relayer-v2.polymarket.com` | `POST /submit` | Builder/Relayer + firma de wallet sobre payload | gasless signed tx, `{type,from,to,nonce,signature,metadata,depositWalletParams?}` → ID y estado de transacción; escribir puede ser ambiguo al perder respuesta | [S42][S13] |
| R | `GET /transaction?id=<relayer-id>` | lectura según contrato publicado | ID → estado, tx hash si minada; estados propios de Relayer | [S42] |
| R | `GET /transactions` | credencial correspondiente | transacciones recientes del usuario | [S42] |
| R | `GET /nonce` | lectura según wallet/selector | nonce de wallet/transacción | [S42] |
| R | `GET /relay-payload` | lectura | dirección/nonce de relayer/payload | [S42] |
| R | `GET /deployed` | lectura, selector wallet | despliegue wallet | [S42] |
| R | `/relayer/api/keys` | gestión de claves Relayer | **RESEARCH GAP:** método y cuerpo no revalidados en raw; no es una operación utilizable sólo con este encabezado | [S42] |
| R | `POST /v1/session-signers/authorizations` | Builder HMAC + owner EIP-712, `Idempotency-Key` | wallet, session signer, alcance y expiración → ID del workflow | [S14] |
| R | `POST /v1/session-signers/revocations` | Builder HMAC + owner EIP-712, `Idempotency-Key` | revocación → ID; efecto off-chain precede confirmación on-chain | [S14] |
| R | `GET /v1/account/transactions/{id}` | identidad del workflow | estado de tx especializada | [S14] |
| R | `GET /v1/account/transactions/params` | wallet owner selector | nonce/parámetros gasless | [S14] |
| CLOB | `GET /v1/user/session-signers` | L2 propietario | session signers activos/utilizables | [S14] |
| Combo `combos-rfq-api.polymarket.com` | `GET /v1/rfq/combo-markets` | público | catálogo legs elegibles, cursor | [S28][S43] |
| Combo maker | `POST /v1/maker/quotes` | quoter autorizado | RFQ y precios/cantidades E6 → quote ID / acuse | [S43][S48] |
| Combo maker | `POST /v1/maker/quotes/cancel` | quoter autorizado | quote ID → resultado cancelación | [S43][S48] |
| Combo maker | `POST /v1/maker/confirmations` | quoter autorizado | RFQ/quote, decisión last-look → confirmación | [S43][S48] |
| Combo requester `combos-rfq-gateway-requester-api.polymarket.com` | `POST /v1/requester/rfq/requests` | L2 identidad compatible | `signer_address,maker_address,signature_type,leg_position_ids,direction,side,requested_size` → `rfq_id` | [S28] |
| Combo requester | `POST /v1/requester/rfq/requests/{rfq_id}/accept` | L2 + signed Exchange-v3 order | `{quote_id,signed_order:{salt,maker,signer,tokenId,makerAmount,takerAmount,side,signatureType,timestamp,metadata,builder,signature}}` → `{rfq_id,status,taker_order_hash?}`; timestamp signed v3 segundos | [S28] |
| Bridge `bridge.polymarket.com` | `GET /supported-assets` | público | chains, assets, addresses soportadas | [S44] |
| Bridge | `POST /deposit` | API especificación por ruta | origen/activo → dirección de depósito | [S44] |
| Bridge | `POST /withdraw` | API especificación por ruta | asset/destino → dirección de retiro | [S44] |
| Bridge | `POST /quote` | API especificación por ruta | asset/cantidad/ruta → quote | [S44] |
| Bridge | `GET /status/{address}` | lectura | address → estado de transferencia | [S44] |

**Relayer core mini-contract gasless:** `POST /submit` usa un sobre `{type:"WALLET",from:"<EOA>",to:"<wallet/factory>",nonce:"<integer>",signature:"<hex>",metadata:"<text>",depositWalletParams:{depositWallet:"<address>",deadline:"<seconds>",calls:[{target:"<contract>",value:"0",data:"<ABI calldata>"}]}}` cuando se utiliza el flujo Deposit Wallet publicado. `GET /transaction?id=<id>` recupera estado `STATE_NEW`, `STATE_EXECUTED`, `STATE_MINED`, `STATE_CONFIRMED`, `STATE_INVALID` o `STATE_FAILED`; una confirmación gasless se identifica por ID de servicio y después `transactionHash` de Polygon. No considerar igual la firma de batch wallet, la firma L2 HTTP y la firma EIP-712 de orden. Los campos obligatorios exactos de las variantes Proxy/Safe/EOA de `POST /submit` deben cotejarse por ruta: **RESEARCH GAP** para un serializador general. [S13][S14][S42]

**Combo requester mini-contract:** `requested_size` usa `{unit:"notional"|"shares",value_e6:"<integer>"}`; BUY solicita notional y SELL shares según documentación. `leg_position_ids` contiene entre 2 y 50 legs elegibles. RFQ se identifica por `rfq_id`, cotización por quote ID, la aceptación requiere firma de orden **Exchange-v3**; la ventana descrita después de quote lista es 5 s. `GET /v1/requester/rfq/requests/{rfq_id}` requiere L2, devuelve `{rfq_id,status,tx_hash?}` y permite conciliación, pero devuelve HTTP 409 antes de aceptación. Repetir la misma aceptación autenticada NO ejecuta la orden dos veces según guía; `EXECUTING` no es fill confirmado. El POST create tiene límite propio de 15 peticiones por minuto rodante por `maker_address` y puede devolver 200 con resultado de negocio sin quote. Si se pierde respuesta del POST create, Polymarket advierte que no existe idempotency key ni búsqueda por request desconocido y repetir puede crear otra RFQ: no declarar retransmisión segura. Las rutas del servicio de collateral return y builder gateway están identificadas por hostname oficial, pero sin extracción de métodos/paths en el documento anterior: **RESEARCH GAP**, fuera del catálogo de endpoints certificados para el MVP CLOB tradicional. [S28][S28a][S28b][S34]

**Bridge** aquí sólo describe financiación/retiros: sus `POST` no son órdenes, no liquidan matches ni resuelven mercados. No se encontró prueba revalidada del schema completo de cada body en esta pasada; **RESEARCH GAP** de implementación de Bridge, no `NOT DOCUMENTED` del protocolo. [S44]

## 4. Autenticación, wallets y autorización

### 4.1 Identidades

| Wallet | `signatureType` CLOB | `maker`/funder | `signer` del Order | Firma de Order |
|---|---:|---|---|---|
| EOA | 0 | EOA | misma EOA | Exchange-v2 Order EIP-712 directo |
| Poly Proxy legacy | 1 | proxy wallet | EOA del propietario | Exchange-v2 Order directo |
| Gnosis Safe compatible/legacy | 2 | Safe | EOA autorizada | Exchange-v2 Order directo |
| Deposit Wallet (default para cuentas nuevas desde 2026-05-04 según docs) | 3 | Deposit contract | **Deposit contract** en la orden | EIP-712 `TypedDataSign` firmado por EOA autorizada, luego ERC-7739 wrapper |

Funder es quien mantiene balances y permisos; signer es quien produce autenticación y firma. No inferir funder de `POLY_ADDRESS`. `chainId=137` corresponde a Polygon producción; las direcciones y la fecha son snapshot [S13][S15][S25][S34].

### 4.2 L1 — crear/derivar API key

Dominio EIP-712 `{name:"ClobAuthDomain",version:"1",chainId:137}`; tipo `ClobAuth(address address,string timestamp,uint256 nonce,string message)`, mensaje `"This message attests that I control the given wallet"`; `timestamp` **string Unix seconds**, nonce `uint256` (flujo estándar 0). La EOA autorizada firma este mensaje, distinto de una orden. Headers HTTP `POLY_ADDRESS` (EOA), `POLY_SIGNATURE` (hex EIP712), `POLY_TIMESTAMP` (seconds), `POLY_NONCE` (decimal). `POST https://clob.polymarket.com/auth/api-key` crea; `GET .../auth/derive-api-key` deriva ya existente; respuesta `{apiKey,secret,passphrase}`. SDK `createOrDerive` es **conveniencia**: captura HTTP 400 del create y luego deriva; no es un endpoint único ni garantía universal de toda causa 400. `GET /auth/api-keys` enumera y `DELETE /auth/api-key` revoca **la credencial que firma esa solicitud**. No se publica en estas fuentes una semántica general universal de rotación/expiración de todas las claves. [S03][S34c]

### 4.3 L2 — firmar requests REST

Clave HMAC = `base64Decode(secret)`; preimage concatenada SIN delimitadores adicionales: `POLY_TIMESTAMP + UPPERCASE_HTTP_METHOD + exact URL path (sin host ni query) + exact serialized body if present`; MAC HMAC-SHA256; firma Base64 URL-safe **con padding**. Headers `POLY_ADDRESS`, `POLY_SIGNATURE` (MAC), `POLY_TIMESTAMP` (Unix segundos), `POLY_API_KEY`, `POLY_PASSPHRASE`. El JSON idéntico semánticamente pero serializado con bytes distintos produce MAC distinta; el body enviado debe corresponder exactamente a los bytes firmados. L2 permite endpoint protegido pero **no reemplaza** la firma de EIP-712 de una orden ni una transacción blockchain. [S03][S15]

### 4.4 Builder, Relayer y Session Keys

Credenciales Builder se crean/listan/revocan en CLOB auth endpoints propios y autentican servicios Builder/Relayer según contrato, no sustituyen automáticamente L2 de trader. Session Keys están en **BETA**, por documentación sólo Deposit Wallet; scopes `CLOB`, `COMBOSRFQ`, `ALL`. La wallet propietaria firma EIP-712 Batch para `authorizeSessionSigner(address,uint256 validUntil)`; API `POST /v1/session-signers/authorizations` exige Builder HMAC, owner authorization y `Idempotency-Key`; revocación usa `POST /v1/session-signers/revocations`, función on-chain `revokeSessionSigner(address)`, mismo control de idempotencia. Vigencia documentada 180 días en SDK actual (ejemplo antiguo usaba 4.315 horas y no coincide exactamente). No permite withdraw. La revocación bloquea primero la identidad delegada en servicio, después cancela órdenes abiertas y completa on-chain con posible retardo. Session Key sólo tiene visibilidad REST de sus propias órdenes; owner no adquiere visibilidad retrospectiva de las generadas por la Session Key. [S14][S33][S34]

**Secretos diferenciados:** private key EOA/session se usa en firmas wallet/EIP-712/on-chain; `secret` CLOB es clave HMAC decodificada; `apiKey/passphrase` identifican credencial L2; Builder/Relayer son juegos independientes; ERC-20 allowance, ERC-1155 aprobación, signature EIP-712 y delegación Session Key son cuatro autorizaciones distintas. [S03][S13][S14][S34a]

## 5. Contrato numérico, unidades y precisión

| Campo/concepto | Wire → unidad | Restricción exacta / autoridad |
|---|---|---|
| EVM network | JSON number / EIP712 uint256 | chainId `137`, Polygon mainnet [S25] |
| `condition_id` | `0x`+64 hex | bytes32; nunca como número decimal [S04] |
| token CTF / `asset_id` | string decimal | `uint256` para CTF; IDs protocol-v2 deben interpretarse con su esquema, nunca float [S04][S34] |
| Gamma event/market IDs | decimal string o JSON numeric | identidad editorial, no trading token [S04][S39] |
| book `price`, `size`, `tick_size`, `min_order_size` | decimal strings | precio $/share en (0,1); shares decimal; tick y min-size dinámicos [S07][S15] |
| pUSD | ERC20 uint256 | `6` decimals, atomic unit E6; denominación del fee page USDC no implica cambiar el token efectivo pUSD [S05][S21][S25] |
| CTF share | ERC1155 unit | órdenes CLOB amounts son strings enteros E6 de shares [S15] |
| Order `salt` | EIP712 uint256; JSON `number` en ejemplo | valor fresco; SDK JS acota a `Number.MAX_SAFE_INTEGER` para evitar corrupción por JSON number, EVM uint256 no equivale a float [S15][S34] |
| `makerAmount`,`takerAmount` | strings de entero | ambos E6, rol BUY/SELL en §7 [S15] |
| `timestamp` EIP712 Order | uint256 / JSON string | epoch **milliseconds** [S15] |
| Order DTO `expiration` | JSON string | epoch **seconds** GTD, GTC `"0"`; NO está firmado [S15] |
| L1/L2 `POLY_TIMESTAMP` | header string | epoch seconds [S03] |
| Price history / Gamma metrics | JSON número/string según esquema | NO deducir precisión de orden desde métricas Gamma [S39][S41] |
| `feeRate` categoría | coeficiente decimal dinámico | NO es lo mismo que `base_fee` entero bps en respuesta CLOB `/fee-rate` [S21][S40a] |
| fee calculada | importe denominación collateral/USDC según página Fees | fórmula §13, **redondeo a 5 decimales**, mínimo positivo `0.00001 USDC`, submínimo **0**; tie-breaking exacto no explicitado [S21] |
| RFQ `*_e6` | entero decimal string | 6 decimales [S28][S48] |
| RPC EVM amount | uint256 | unidades atomic on-chain, no compartir encoding con strings de book sin conversión explícita [S05a] |

### Tabla obligatoria de precisión de órdenes por tick — documentación CURRENT [S15]

| `tick_size` | Máx. decimales precio | Máx. decimales size | Máx. decimales USD amount |
|---|---:|---:|---:|
| `0.1` | 1 | 2 | 3 |
| `0.01` | 2 | 2 | 4 |
| `0.005` | 3 | 2 | 5 |
| `0.0025` | 4 | 2 | 6 |
| `0.001` | 3 | 2 | 5 |
| `0.0001` | 4 | 2 | 6 |

**Algoritmo oficial, en secuencia y sin sustituciones:** (1) expresar precio con **a lo más** decimales de la tabla y verificar que es múltiplo del tick actual; (2) redondear tamaño en shares **hacia abajo** a `Size decimals`; (3) calcular USD `price × size redondeado`; sólo si supera decimales de `Amount`, redondear USD primero **hacia arriba** a `AmountDecimals+4`, luego **hacia abajo** a `AmountDecimals`; (4) confirmar **después del redondeo** que size ≥ `min_order_size` efectivo de `/book`; (5) convertir USD y shares en **enteros E6**; (6) asignar maker/taker según BUY/SELL. Precio inválido por tick, min-size incumplido o escala incorrecta son rechazos de validación, no reintentos infra. El documento publica este orden de operaciones, no un algoritmo de redondeo genérico distinto. [S15]

| Side sobre token YES o NO | `makerAmount` E6 | `takerAmount` E6 |
|---|---|---|
| `BUY` | USD = precio×shares | shares compradas |
| `SELL` | shares vendidas | USD = precio×shares |

Ejemplo BUY YES, 10 shares, `0.52`, book min 5, tick `0.01`: USD=5.20 → `makerAmount:"5200000"`, `takerAmount:"10000000"`; SELL del **mismo asset** invierte los campos. `BUY` de NO sigue siendo BUY, no un SELL de YES por equivalencia económica. [S15]

**Regla fee exacta publicada:** `raw = shares × feeRate × price × (1-price)` cuando fee enabled; redondeo output a 5 decimales, importe positivo mínimo `0.00001 USDC`; si valor calculado por debajo de ese mínimo, cobra cero. No extrapolar orden de redondeos intermedios ni desempate de mitad sin especificación. `base_fee` del endpoint es entero bps; no sustituir automáticamente `feeRate` de fórmula por `base_fee/10000` sin contrato que conecte ambos. [S21][S40a]

## 6. Semántica global de tiempo

| Origen/campo | Unidad wire | Fuente/meaning | Garantía de orden |
|---|---|---|---|
| Gamma `createdAt,startDate,endDate,closedTime` según modelo | ISO8601/RFC3339 | metadatos editoriales, start/end/closed distintos | no global |
| CLOB `/book.timestamp` | epoch **ms string** | hora servicio snapshot | sin secuencia |
| Market WS `book,price_change,last_trade_price.timestamp` | epoch **ms string** | hora evento mercado | sin secuencia especificada |
| CLOB order `created_at` | Unix **seconds** | creación de orden | no total multiorden |
| User WS order `created_at`,`timestamp` | Unix seconds strings en ejemplos | creación/emisión | sin replay/sequence |
| CLOB trade `match_time`,`last_update` | Unix seconds strings | match y última transición; distintos | settlement asíncrono |
| User WS trade `timestamp` | seconds según ejemplo | emisión trade event | no cross-channel order |
| HTTP `POLY_TIMESTAMP` | Unix seconds | frescura autenticación | no event-time |
| EIP-712 CLOB v2 Order `timestamp` | Unix **milliseconds** | campo firmado | no expira por sí solo |
| DTO Order `expiration` | Unix **seconds** | límite GTD declarado; vence 60 s antes | no confundir con timestamp firmado |
| Exchange-v3 Combo Order `timestamp` | Unix seconds | dominio/orden v3 | no reutilizar v2 timestamp |
| RFQ `*_at`,`expires_at`,`confirm_by` | epoch **ms** | deadlines gateway | orden sólo RFQ local |
| Data v2 normalized SDK dates | epoch ms / objeto temporal según SDK; wire según schema | actividad y agregados | cursors ≠ snapshot global |
| RTDS envelope/payload timestamps | epoch ms | hora servicio vs upstream | sin orden cruzado garantizado |
| Chainlink report `validFromTimestamp` etc. | Unix seconds | source/validity window | no sincronía global con CLOB |
| Sports WS | según mensaje/schema | fuente deportiva | no replay garantizado |
| Polygon block timestamp | Unix seconds | tiempo del bloque que incluyó tx | NO equivale a match CLOB |
| UMA proposal/dispute/final | on-chain seconds y Data v2 según entidad | oracle lifecycle | diferente a market end/redeem |

No existe contrato publicado de reloj global común entre Gamma, CLOB, RTDS, deportes, oráculo y chain. [S03][S08][S09][S11][S12][S27][S41][S48]

## 7. Orden CLOB v2: CINCO contratos separados — P0

**Versión:** esta sección describe la orden CLOB v2 documentada por Place Orders en 2026-09-17, NO el antiguo struct CLOB-v1 (`taker`,`nonce`,`feeRateBps` firmados) ni la orden Exchange-v3 Combo. `expiration` **NO pertenece al mensaje firmado**: pertenece al Order DTO HTTP y controla GTD junto con `orderType` del wrapper. La documentación del migration guide todavía contiene ejemplos v1 con campos anteriores: eso es una divergencia de versión visible, no razón para unir schemas. [S15][S32a][S34]

### A. EIP-712 `Order` realmente firmado

Dominio de aplicación: `name="Polymarket CTF Exchange"`, `version="2"`, `chainId=137`, `verifyingContract=CTF Exchange` estándar **o** `NegRisk CTF Exchange` según `GET /book.neg_risk` del asset y su protocolo. `primaryType="Order"` para EOA/Proxy/Safe; para Deposit ver apartado E. **Lista exacta y orden de miembros del struct firmado** [S15]:

| Índice | Nombre | Solidity EIP-712 | Unidad/meaning |
|---:|---|---|---|
| 1 | `salt` | `uint256` | aleatorio nuevo / identidad |
| 2 | `maker` | `address` | wallet que aporta fondos |
| 3 | `signer` | `address` | EOA (tipos 0–2) o Deposit Wallet (tipo 3) |
| 4 | `tokenId` | `uint256` | asset/outcome CTF, NO Gamma market ID |
| 5 | `makerAmount` | `uint256` | E6 USD para BUY, E6 shares para SELL |
| 6 | `takerAmount` | `uint256` | E6 shares para BUY, E6 USD para SELL |
| 7 | `side` | `uint8` | `0` BUY, `1` SELL |
| 8 | `signatureType` | `uint8` | 0 EOA, 1 Proxy, 2 Safe, 3 Deposit |
| 9 | `timestamp` | `uint256` | epoch milliseconds, firmado |
| 10 | `metadata` | `bytes32` | valor bytes32, cero cuando no aplica |
| 11 | `builder` | `bytes32` | atribución builder o cero |

**NO se firma en Order:** `expiration`, `signature` (resultado), `orderType`, `postOnly`, `deferExec`, `owner` (API key), headers HMAC, parámetros de matching. `signatureType` sí se firma como `uint8`; `signature` es artefacto posterior. La firma EIP-712 no convierte `postOnly`/`GTD` en propiedades criptográficamente comprometidas si no aparecen en struct; su enforcement lo hace el servicio. [S15]

### B. DTO `order` transportado a CLOB

Objeto JSON `order` contiene `builder:hex32`, `expiration:string` (GTC `"0"`, GTD Unix segundos), `maker:address`, `makerAmount:string entero E6`, `metadata:hex32`, `salt:JSON number` (no string en ejemplo HTTP), `side:"BUY"|"SELL"` (diferente del `uint8` firmado), `signature:hex bytes`, `signatureType:integer`, `signer:address`, `takerAmount:string entero E6`, `timestamp:string Unix ms`, `tokenId:string decimal uint256`. Los valores equivalentes al firmado deben mantenerse idénticos después de codificar/normalizar; `expiration` es **adicional sólo del transporte**. JSON number del salt obliga cautela en entornos JavaScript, donde el SDK exige entero exactamente representable ≤2^53−1; `uint256` EVM admite otro rango, pero no se puede inferir que el serializador del servidor admita arbitrary-precision JSON number. [S15][S34]

### C. HTTP submission wrapper y ejemplo ilustrativo NO EJECUTABLE

`POST https://clob.polymarket.com/order` con L2 headers de §4.3; body JSON exacto:

```json
{
  "deferExec": false,
  "order": {
    "builder": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "expiration": "0",
    "maker": "0x1111111111111111111111111111111111111111",
    "makerAmount": "5200000",
    "metadata": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "salt": 479249096354,
    "side": "BUY",
    "signature": "<FIRMA_EIP712_FICTICIA_NO_VÁLIDA>",
    "signatureType": 0,
    "signer": "0x1111111111111111111111111111111111111111",
    "takerAmount": "10000000",
    "timestamp": "<UNIX_MILLISECONDS>",
    "tokenId": "<CTF_TOKEN_ID_UINT256_DECIMAL>"
  },
  "orderType": "GTC",
  "owner": "<CLOB_API_KEY>"
}
```

Los placeholders hacen que sea **ejemplo estructural**, NO un request criptográficamente válido ni una orden enviable. `deferExec=false` aparece en solicitud oficial; el detalle temporal exhaustivo de `deferExec=true` no está definido en la página Place Orders: no asignarle una semántica inventada. `owner` es **API key**, no maker address. `postOnly:true` puede añadirse **al wrapper** con `orderType=GTC|GTD`, nunca dentro del signed Order; su omisión equivale a no solicitar ese modo. [S15]

**Respuesta HTTP sin normalización SDK** [S15]:

```json
{
  "success": true,
  "errorMsg": "",
  "orderID": "<HASH>",
  "status": "live",
  "makingAmount": "<INTEGER_AMOUNT>",
  "takingAmount": "<INTEGER_AMOUNT>",
  "transactionsHashes": ["<TX_HASH_IF_AVAILABLE>"],
  "tradeIDs": ["<TRADE_ID_IF_AVAILABLE>"]
}
```

Rechazo puede ser `{success:false,errorMsg:"not enough balance / allowance",orderID:"",status:"",makingAmount:"",takingAmount:""}`. Estados de *placement response*: `live`,`matched`,`delayed`,`unmatched`. `unmatched` significa colocación aceptada según texto actual, NO un enum persistente de orden. `transactionsHashes` y `tradeIDs` pueden no existir/no estar listos al colocar. SDK devuelve `ok,orderId,tradeIds` como **normalización**, no exigir estos nombres en HTTP raw. [S15][S18]

### D. Política de ejecución — no confundir con firma

| Valor | Semántica publicada | Validación, parcialidad y expiry |
|---|---|---|
| `orderType:GTC` | buena hasta cancelación/fill | DTO `expiration:"0"`; puede descansar y llenarse parcialmente; `postOnly` opcional |
| `orderType:GTD` | buena hasta fecha declarada | DTO `expiration:"<Unix seconds>"`; plazo declarado ≥ `server now + 180s`; se expira **60 segundos antes** del declarado; mínimo efectivo ~120 s; `postOnly` opcional |
| `orderType:FOK` | fill inmediato **total** o kill | no resto abierto; `postOnly` incompatible; la validez del snapshot de profundidad no garantiza fill |
| `orderType:FAK` | ejecuta disponible inmediato, mata resto | partial fill válido; `postOnly` incompatible |
| `postOnly:true` | agrega liquidez o rechaza si cruza | sólo `GTC/GTD`, rechazo crossing, no orden maker creada si rechazada |
| `deferExec` | parámetro wrapper booleano presente en contrato | `false` documentado para flujo inmediato; significado exacto de `true`/interacción con tipos: **RESEARCH GAP** de schema y/o NOT DOCUMENTED si schema carece de semántica |
| Batch `POST /orders` | hasta 15 órdenes firmadas separadas | resultado individual por orden; algunos aceptados y otros rechazados, no batch atomic de business outcome |

Una **market order** no es nueva estructura EIP-712: es orden límite agresivamente valorada y política `FAK`/`FOK`. Los helpers SDK `estimateMarketPrice` (BUY budget USD, SELL shares) no garantizan precio de ejecución final y no son endpoint matching distinto. `postOnly` en FAK/FOK no es una combinación válida. [S15][S18]

### E. Ruta de firma por wallet; CLOB v2 vs Exchange v3

| Wallet y `signatureType` | Dominio y primaryType | Campos maker/signer | Artefacto de firma |
|---|---|---|---|
| EOA 0 | Exchange v2, `Order` | EOA/EOA | `signTypedData(Order)` |
| Proxy 1 | Exchange v2, `Order` | proxy/EOA | `signTypedData(Order)` EOA |
| Safe 2 | Exchange v2, `Order` | Safe/EOA | `signTypedData(Order)` EOA autorizada |
| Deposit 3 | Exchange v2 `Order` contenido dentro `TypedDataSign`; `DepositWallet` name/version1/chain137/verifyingContract=wallet en message | Deposit/Deposit | firma `TypedDataSign` por signer externo autorizado y wrap ERC-7739 |
| Combo RFQ | Exchange **v3**, name `Polymarket CTF Exchange`, version `3`, chain137, verifyingContract `0xe333...00Aa`; `timestamp` **segundos** | según account compatible | firma específica v3; NO reutilizar digest de v2 |

Para Deposit Wallet, outer `TypedDataSign` tiene campos `{contents:Order,name:string,version:string,chainId:uint256,verifyingContract:address,salt:bytes32}`, `message.name="DepositWallet"`, `message.version="1"`, verifyingContract es Deposit address y `salt=bytes32(0)`. La firma interna se envuelve concatenando: `innerSignature || appDomainSeparator || contentsHash || hex(ORDER_TYPE literal) || uint16_big_endian(length ORDER_TYPE)` según ejemplo exacto [S15]. El literal `ORDER_TYPE` es `Order(uint256 salt,address maker,address signer,uint256 tokenId,uint256 makerAmount,uint256 takerAmount,uint8 side,uint8 signatureType,uint256 timestamp,bytes32 metadata,bytes32 builder)`; el `appDomainSeparator` es EIP712Domain Exchange v2 y `contentsHash` es hash tipado Order; no usar ingenuamente `eth_sign`/personal_sign. El commit oficial `983a10a7579c95043d4099f60873ff7ea817e5a0` agregó `EIP712Domain` explícito a typed-data payloads por compatibilidad de signers, **sin añadir otro campo firmado Order**. [S15][S34][S34d]

**V1/v2 boundary:** antiguas órdenes CLOB-v1 incluían `taker`, `nonce`,`feeRateBps`; CLOB-v2 documentado actualmente NO los firma ni requiere fee rate firmado, la fee se aplica en matching. La guía de migración todavía puede mostrar fragmentos legacy; priorizar el schema completo de la página vigente y registrar contradicción, nunca construir híbrido. Exchange-v3 Combo cambia contrato/dominio y timestamp, aunque reuse nombres `Order` familiares. [S15][S32a][S28]

## 8. Order management, matching, estados e idempotencia

### 8.1 Vocabularios separados, no «state machine universal»

| Capa | Valores documentados | IDs/observación |
|---|---|---|
| Placement HTTP (lowercase) | `live`, `matched`, `delayed`, `unmatched` y rechazo `success:false` | `orderID` si aceptada; `tradeIDs` opcional [S15] |
| Orden REST persistente | `LIVE`, `INVALID`, `CANCELED`, `MATCHED`, `CANCELED_MARKET_RESOLVED` | order hash; `original_size`, `size_matched`; enum exacto según schema [S16][S40] |
| User WS `order.type` (evento) | ejemplos `PLACEMENT`, `CANCELLATION`; actualizaciones adicionales deben obtenerse del AsyncAPI | `order.id`, `associate_trades` [S09][S46] |
| Trade WS/REST `status` | `MATCHED`, `MINED`, `CONFIRMED`, `RETRYING`, `FAILED` | `trade.id`, `transaction_hash`, `last_update` [S09][S16] |
| Relayer `state` | `STATE_NEW`,`STATE_EXECUTED`,`STATE_MINED`,`STATE_CONFIRMED`,`STATE_INVALID`,`STATE_FAILED` | relayer transaction ID y hash [S42] |
| RFQ requester `status` | `AWAITING_REQUESTER_ACCEPTANCE`,`AWAITING_MAKER_CONFIRMATION`,`EXECUTING`,`MINED`,`RETRYING`,`CONFIRMED`,`FILLED`,`FAILED`,`EXPIRED`,`CANCELED` | RFQ ID; no son status de trade CLOB [S28] |

**DERIVED MODEL (interpretación, NO enum Polymarket):** una solicitud produce respuesta de placement; la orden persistente puede tener remanente `LIVE` mientras fills crean trades `MATCHED`; cada trade pasa independientemente por `MINED/CONFIRMED` o estados de falla/retry; cancelar afecta remanente, no deshace matches confirmados; al resolverse, remanente puede quedar `CANCELED_MARKET_RESOLVED`. No inferir que `matched` placement significa `CONFIRMED` on-chain. [S15][S16]

### 8.2 Matching / mantenimiento

CLOB realiza matching fuera de cadena, settlement on-chain en Polygon. Maker es orden resting; taker consume y puede recibir mejora si resting price es favorable. Fills parciales son posibles y `size_matched` cambia. **Price-time priority exacta NO DOCUMENTED** como garantía contractual, no inferir FIFO universal del book. En `Matching Engine Restarts` se describe HTTP **425 Too Early** durante reinicio y potencial modo post-only posterior; error reference publica HTTP 503 para `post_only_mode` con `retry_after_seconds`/`Retry-After`, también cancel-only y trading-disabled. No identificar `425` como negocio terminal ni retratar `503` como autorización para insistir ciegamente con órdenes. [S17][S18]

### 8.3 Writes ambiguas / reconciliación

| Operación | Idempotencia nativa | Reenvío a ciegas | Qué permite reconciliar |
|---|---|---|---|
| `POST /order` | orden firmada tiene identidad/hash determinista; **sin Idempotency-Key HTTP documentado** | **NO se garantiza** para error/timeout genérico; error oficial específico `order timed out` declara rechazo antes de book y permite resubmisión | hash conocido → `/data/order/{orderID}`; REST órdenes/trades y User WS, revisar fills |
| `POST /orders` | cada orden con hash, sin clave batch | NO hay atomicidad ni safe retry universal; posibles parciales business | por cada order hash/ID; respuesta elemento a elemento |
| `DELETE /order` | target order hash | intención de cancel converge pero repetición HTTP no está formalmente garantizada | `GET /data/order/{id}`, trade ledger |
| `DELETE /orders` | array de hashes; IDs duplicados en mismo batch se ignoran documentadamente | depende de estados actuales; examinar `canceled/not_canceled` | lookups por ID |
| `DELETE /cancel-all` | sin clave request | no recrea órdenes, pero falta garantía formal de replay HTTP | `GET /data/orders` abiertos según signer/credencial |
| `POST R /submit` | nonce/firma/tx ID si recibido | no documentado blind retry general | relayer ID o chain hash/nonce, si ID se obtuvo |
| Session authorize/revoke | `Idempotency-Key` documentado | mismo contenido/clave conforme contrato | tx ID y `/v1/user/session-signers` |
| Combo requester create | **sin idempotency key ni lookup de respuesta perdida** | **NO**, crea potencial duplicado | sólo si se conoce `rfq_id`; ausencia de respuesta es ambigua |
| Combo requester accept | `rfq_id` estable; docs garantizan no doble ejecución al repetir misma aceptación autenticada | retry misma aceptación documentado | GET `/v1/requester/rfq/requests/{rfq_id}` |
| chain tx | hash+nonce EVM | el comportamiento app/relayer de un reenvío no es garantía general | RPC transaction/receipt, nonce y logs |

**Reconciliación cuando User WS cae:** NO hay replay/cursor de User WS; obtener órdenes actuales/por ID en CLOB REST, trades por filtros/tiempo, cruzar `order.id` con `trade.taker_order_id`/`maker_orders[].order_id`, seguir `trade.id`, `transaction_hash` y estado `CONFIRMED/FAILED`. La wallet owner **no ve automáticamente** por REST las órdenes de Session Key: reconciliar con identidad correcta. [S09][S14][S16]

### 8.4 Matriz resumida de errores, terminalidad y retry

| Error/clase | Ejemplo wire / efecto | Estado conocido y retry |
|---|---|---|
| validation HTTP 400 | invalid token/tick, precision/min-size, JSON, malformed order | cambiar input; retry idéntico no soluciona |
| authentication HTTP 401 | POLY headers/HMAC/credencial inválida | rehacer auth sólo después de corregir |
| authorization 403/market disabled | wallet no autorizada, restriction/geoblocking | no evadir; terminal hasta cambio legítimo |
| duplicate order | `Duplicated` / identidad ya conocida | consultar orden/fills; no generar salt nuevo automáticamente |
| balance/allowance | `not enough balance / allowance` | verificar balances y aprobación; no infraestructura transient por defecto |
| invalid signature | digest/domain/maker/signer erróneo | reconstrucción y firma correctas |
| FOK no depth/full fill | resultado de política, no error de red | no reintentar suponiendo falla técnica |
| HTTP 425 | matching engine restart | operación puede reintentarse según naturaleza; para write ambiguo consultar estado |
| HTTP 429 | rate limit IP o signer; `Retry-After` si provisto | bucket/cooldown; NO asumir único limitador |
| HTTP 503 `post_only_mode` | `retry_after_seconds`/header; trading mode | orden incompatible se rechaza; reevalúa modo |
| HTTP 500 `order timed out` **exacto** | ref error declara no entró al book | resubmisión explícitamente segura según fuente |
| HTTP 500 genérico/network timeout | outcome desconocido | reconciliar antes de decidir nueva firma/orden |
| cancel partial | `not_canceled` map | mirar por ID/trades; no asumir cancel all-or-nothing |
| RFQ create respuesta perdida | servidor puede haber creado RFQ | no idempotencia; bloqueo operacional de retransmisión |

[S18][S20][S28]

## 9. Books, Market/User WS, externos y recuperación

### 9.1 Order book REST: representaciones y precios

`GET C/book?token_id=<asset_id>` y `POST C/books` proporcionan snapshots agregados de niveles con `{market:<condition_id>,asset_id,timestamp,hash,bids:[{price,size}],asks:[{price,size}],min_order_size,tick_size,neg_risk,last_trade_price?}`. El batch admite hasta 500 token IDs según especificación observada; la consistencia *atómica entre libros del batch* **NOT DOCUMENTED**. Precios/tamaños son decimal strings; timestamp epoch ms string, `hash` identifica cambio de estado pero no proporciona algoritmo de checksum/continuidad documentado. Orden REST **bids ascendente, asks descendente; best bid y best ask al final de cada array** (no índice cero). [S07][S40]

`best bid` es precio más alto que compra; `best ask`, más bajo que vende; `midpoint=(best bid+best ask)/2` sólo referencia; `last trade` ejecución última; `price?side=BUY|SELL` dato de precio lateral API; UI habitualmente muestra midpoint y pasa a last trade si spread **> $0.10**; para ejecución de BUY consultar asks y SELL bids con profundidad/size. La cotización de UI, midpoint y precio marginal ejecutable no son equivalentes. `tick_size` puede cambiar mediante evento WS; min-size puede variar y debe leerse de snapshot/market. Estado inactive/closed/archived/resolved de Gamma no equivale a book operable; respetar `enableOrderBook` y estado de CLOB. [S07][S07a][S08]

### 9.2 Market WS — contrato de mensajes

Conectar `wss://ws-subscriptions-clob.polymarket.com/ws/market`. Mensaje inicial:

```json
{"type":"market","assets_ids":["<YES_ASSET>","<NO_ASSET>"],"custom_feature_enabled":true,"initial_dump":true}
```

`type`,`assets_ids` esenciales; `custom_feature_enabled` habilita eventos extendidos; cambiar set con `{"operation":"subscribe","assets_ids":["..."]}` o `unsubscribe`. Heartbeat: texto aplicación `PING` cada **10s**, respuesta servidor `PONG`. `assets_ids` NO son Gamma IDs, mientras que `market` en eventos identifica condition ID. AsyncAPI vigente documenta `book` full snapshot **inicial por asset al suscribirse**; no exige snapshot REST inicial si éste se recibe. [S08][S45]

| Server event | Disparador/representación | Key fields fundamentales | Tiempo | Estado local | Secuencia |
|---|---|---|---|---|---|
| `book` | subscription inicial o nuevo snapshot por cambios documentados; FULL | `asset_id`,`market`,`bids`,`asks`,`hash`,`timestamp` | ms | reemplazo completo del libro | NO publicada |
| `price_change` | level cambia por colocación/cancelación | `price_changes[]:{asset_id,price,size,side,hash,best_bid,best_ask}`, market/time | ms | delta de nivel: size actual, cero quita nivel según documentación de evento | NO publicada |
| `last_trade_price` | match | `asset_id`,`market`,`price`,`size`,`side`,`fee_rate_bps`,`transaction_hash`,`timestamp` | ms | trade/BBO indirecto; NO es delta book suficiente | NO publicada |
| `tick_size_change` | cambio tick efectivo | asset, old_tick_size,new_tick_size,time | ms | reemplaza constraint, no reescala nivel por inferencia | NO publicada |
| `best_bid_ask` | cambio BBO, feature activada | asset,best_bid,best_ask,spread,time | ms | proyección, no profundidad | NO publicada |
| `new_market` | alta mercado, feature | Gamma ID, condition, token IDs, outcome/metadata | ms | discovery/evento de alta; no necesariamente book inicial | NO publicada |
| `market_resolved` | resolución mercado, feature | condition, winning asset, outcome, resolve fields | ms | lifecycle, no sustituye redención onchain | NO publicada |

Para eventos de control subscription/heartbeat no existe un `sequence` ni ACK de replay contract. Los nombres/campos auxiliares de cada variante de `new_market/market_resolved` figuran en la AsyncAPI; extracción exhaustiva de TODOS los schemas de esas variantes en esta pasada **RESEARCH GAP**, no usar tabla como sustituto de AsyncAPI para struct completo. [S08][S45]

**Preguntas contractuales:** (1) WS **sí** permite bootstrap de libro actual con full initial `book`, aplicar `price_change` y sustituir por `book` posteriores; (2) GET REST snapshot NO obligatorio en happy path de WS documentado; (3) tras reconnect abrir nueva conexión, resuscribir y esperar nuevos initial books; (4) no hay `resumeToken`, replay, `sequence` ni garantía publicada de orden estricto multiasset; (5) `hash` existe, pero algoritmo/encadenamiento para gap detection no especificado; (6) por ello, un libro actual aproximado se mantiene con WS, mas no puede **probarse replay determinista lossless** entre snapshots. [S08][S45]

### 9.3 User WS — contrato de mensajes

`wss://ws-subscriptions-clob.polymarket.com/ws/user`; suscripción inicial:

```json
{"type":"user","auth":{"apiKey":"<API_KEY>","secret":"<BASE64_SECRET>","passphrase":"<PASSPHRASE>"},"markets":["<CONDITION_ID>"]}
```

`markets` opcional y son **condition IDs** (NO assets/Gamma IDs). Cambios de suscripción con operación subscribe/unsubscribe; PING/PONG texto cada 10 s. [S09][S46]

| Evento | Campos wire esenciales | Relación/semántica |
|---|---|---|
| `order` | `id,market,asset_id,side,original_size,size_matched,price,associate_trades,outcome,type,created_at,expiration,order_type,status,maker_address,timestamp` | `id` order hash, market condition, `type` event vs status persistente; segundos en ejemplos WS |
| `trade` | `id,taker_order_id,market,asset_id,side,size,price,fee_rate_bps,status,match_time,last_update,transaction_hash,maker_orders[],trader_side,timestamp` | trade ID ↔ taker order ID / maker_orders[].order_id ↔ hash tx; match y settlement separados |

**No** snapshot inicial de cuenta completo, sequence ni resume/replay publicados. Ante pérdida, REST CLOB `/data/order/{id}`, `/data/orders`, `/data/trades` son fuentes de reconciliación. Scope de clave Session Key limita visibilidad. No inferir que ausencia de mensaje trade equivale a ausencia de ejecución. [S09][S14][S16][S46]

### 9.4 Sports, RTDS/Chainlink y RFQ WS

**Sports** `wss://sports-api.polymarket.com/ws`: push de estado de encuentros, puntuaciones/lifecycle; control ping/pong según Sports AsyncAPI, sin snapshot/replay garantizado ni secuencia publicada. Información `/sports`, `/teams` Gamma es metadato, NO reemplaza log histórico de goles/puntos. [S10][S47]

**RTDS** `wss://ws-live-data.polymarket.com`: suscripción por `topic,type,filters`, mensaje `{"action":"subscribe","subscriptions":[{"topic":"crypto_prices","type":"update","filters":"btcusdt,ethusdt"},{"topic":"crypto_prices_chainlink","type":"*","filters":"{\"symbol\":\"eth/usd\"}"}]}`; texto `PING` cada **5 s**; envelope Polymarket timestamp ms y payload upstream timestamp ms/value. `prices.crypto.chainlink.twap` expone `symbol,timestamp,value,windowSeconds`, ventanas observadas de **30/60s**; Chainlink report E18 y validity timestamps segundos son representación upstream distinta. No hay garantía RTDS universal de frecuencia exacta, replay ni correspondencia de relojes con CLOB. [S11][S12][S49]

**RFQ Quoter** `wss://combos-rfq-gateway-quoter.polymarket.com/ws/rfq`: primer mensaje `auth` dentro de **30s**; servidor ping control frames cada **30s**, payload `rfq`, cliente pong, cierre posible sin inbound durante 2 min. Client→server familias `auth`,`RFQ_QUOTE`,`RFQ_QUOTE_CANCEL`,`RFQ_CONFIRMATION_RESPONSE`; server→client `auth response`,`RFQ_REQUEST`,`ACK_RFQ_QUOTE`,`ACK_RFQ_QUOTE_CANCEL`,`RFQ_CONFIRMATION_REQUEST`,`ACK_RFQ_CONFIRMATION_RESPONSE`,`RFQ_EXECUTION_UPDATE`,`RFQ_TRADE`,`RFQ_ERROR`. `*_e6` enteros strings E6, tiempos RFQ epoch ms. `RFQ_TRADE` es explícitamente **best-effort**, deduplicar por RFQ ID según spec; NO replay/secuencia documentados. El detalle de payload de cada una de las 13 familias no fue retranscrito íntegramente de AsyncAPI en esta revisión: **RESEARCH GAP** para implementar quoter WS únicamente desde este documento. [S48]

### 9.5 WS Recovery Matrix

| Stream | Snapshot inicial | Sequence | Gap detector | Replay/resume | REST reconcile | Reconnect |
|---|---|---|---|---|---|---|
| Market | sí: full `book` por asset | NOT DOCUMENTED | hash no especifica detector | no publicado | C `/book` | reconnect + subscription → nueva foto |
| User | no full cuenta | NOT DOCUMENTED | ninguno publicado | no publicado | C `/data/order/{id}`, `/data/orders`, `/data/trades` | nueva auth y reconcile |
| Sports | push live, no log | NOT DOCUMENTED | ninguno | no publicado | Gamma metadata ≠ replay | reconectar |
| RTDS | sin bootstrap genérico garantizado | NOT DOCUMENTED | ninguno | no publicado | feed-specific; no full RTDS archive | nueva suscripción |
| RFQ Quoter | workflow/eventos live | NOT DOCUMENTED | ninguno | no publicado, trade best-effort | requester status GET si se conoce RFQ ID | re-auth y status por RFQ |

## 10. Positions, CTF y operaciones on-chain

**CTF-era**: una condición binaria emite dos outcomes ERC-1155. `1.000000 pUSD` bloqueado ↔ `1 YES + 1 NO` (split/merge); outcome final winning share → `1.000000 pUSD` al redeem; resolución `Unknown`/50-50, si aplica a esa condición, paga `0.5` por cada lado completo. Estas conversiones son operaciones de contrato, **no endpoints REST CLOB de crear posiciones**; el SDK y Relayer sólo encapsulan calldata y envío. pUSD contrato y CTF en Polygon 137, direcciones §11. [S05][S05a][S25]

| Operación CTF | Destino/función ABI publicada | Argumentos críticos / approval previo | Resultado y reconciliación |
|---|---|---|---|
| split | adapter estándar o NegRisk CTF → `splitPosition(address collateralToken,bytes32 parentCollectionId,bytes32 conditionId,uint256[] partition,uint256 amount)` | collateral=pUSD; parentCollectionId=`bytes32(0)`; partition `[1,2]`; amount=atomic E6; allowance ERC20 a adapter | pUSD se consume, YES+NO mint, tx/receipt + balances ERC1155 |
| merge | mismo adapter → `mergePositions(address,bytes32,bytes32,uint256[],uint256)` | pUSD, zero parent, condition, `[1,2]`, amount atomic E6; ERC1155 `setApprovalForAll` al adapter | YES+NO consumidos, collateral devuelto; receipt/balances |
| redeem | adapter → `redeemPositions(address,bytes32,bytes32,uint256[] indexSets)` | pUSD, zero parent, condition, indexSets `[1,2]`; sin `amount`, redime saldo elegible, requiere resolución/payout; ERC1155 approval según ruta | tokens quemados y payout acreditado; receipt + balance/posición |
| outcome balance | Conditional Tokens `balanceOf`,`balanceOfBatch` (ERC1155) | wallet + token IDs | balance atomic; no equivale a Data API PnL |

La dirección concreta del **adapter** se elige por contexto de mercado CTF estándar vs CTF NegRisk: `0xAdA100...FcE1f` o `0xadA200...eAab`; contrato ERC1155 es Conditional Tokens `0x4D97...6045`. El SDK pinned resuelve `market.version` y el contexto `negRisk` antes de preparar calls. Las firmas/approvals de CLOB Exchange para trading son **adicionales** y diferentes de allowances de adapters para split/merge/redeem. [S05a][S34a][S34b]

**Protocol-v2:** la versión de Market/posición discrimina CTF vs `v2` en SDK: se obtiene Market por condition, el SDK resuelve protocolo (`PositionProtocol.CTF|V2` interno) y v2 `routerSplitCall`,`routerMergeCall`,`routerRedeemCall` sobre Router `0x1212...2600`, con PositionManager ERC1155 `0x006F...9fEF` y módulo binario o NegRisk. NO llamar CTF split sobre token v2 ni enviar su posición al antiguo adapter. Para un Combo v2 se canonicizan legs, `CombinatorialModule.prepareCondition(legs)` y luego `Router.split(comboConditionId,amount)`; SDK usa dos tx secuenciales para EOA o llamadas agrupadas en Deposit Wallet gasless. El contrato ABI exacto de todas las variantes v2 debe extraerse del SDK/ABI antes de una reimplementación que omita ese SDK: **RESEARCH GAP** de encoding genérico v2 aunque las rutas y direcciones han sido comprobadas. [S34b][S25][S05c]

**Cómo seguir un lifecycle:** `condition_id` → outcome/position ID → balances ERC1155 de wallet; trades offchain crean y transfieren tenencia en chain al settlement; Data v2 `/positions` refleja OPEN/REDEEMABLE/CLOSED pero no constituye recibo final de tx; final oracle payout → redeem contract tx → receipt y balance pUSD. `event end`, CLOB cierre, trade match, settlement, resolución, redeemable y redeem son siete estados distintos. [S05][S16][S27]

## 11. Contratos, direcciones, rutas y aprobaciones

Snapshot producción **Polygon mainnet (137), verificado 2026-09-17 UTC** contra registry oficial y environment TS pinned SHA `983a10a...817e5a0` [S25][S34]. Direcciones completas sólo donde verificadas; abreviaciones **sólo** en matrices posteriores que enlazan a este registro.

| Contrato / función de identidad | Dirección completa |
|---|---|
| pUSD / CollateralToken ERC20 proxy | `0xC011a7E12a19f7B1f670d46F03B03f3342E82DFB` |
| Conditional Tokens ERC1155 | `0x4D97DCd97eC945f40cF65F87097ACe5EA0476045` |
| CTF Exchange v2 standard | `0xE111180000d2663C0091e4f400237545B87B996B` |
| CTF NegRisk Exchange v2 | `0xe2222d279d744050d28e00520010520000310F59` |
| legacy CTF NegRisk Adapter | `0xd91E80cF2E7be2e162c6513ceD06f1dD0dA35296` |
| standard collateral adapter | `0xAdA100Db00Ca00073811820692005400218FcE1f` |
| NegRisk collateral adapter | `0xadA2005600Dec949baf300f4C6120000bDB6eAab` |
| Combo Exchange v3 | `0xe3333700cA9d93003F00f0F71f8515005F6c00Aa` |
| Protocol-v2 Router | `0x12121212006e4CD160D18e3f00711DA5c3372600` |
| PositionManager proxy | `0x006F54F7f9A22e0000CC2AB60031000000ae9fEF` |
| BinaryModule proxy | `0x1000008dD9001B968442c1000017eaE6E0dA00Ba` |
| NegRiskModule proxy | `0x200000900045e3B6259600682756002200028933` |
| CombinatorialModule proxy | `0x30000034706C7d8e12009DAB006Be20000c031A8` |
| AutoRedeemer | `0xa1200000d0002264C9a1698e001292D00E1b00af` |
| CollateralOnramp | `0x93070a847efEf7F70739046A929D47a521F5B8ee` |
| CollateralOfframp | `0x2957922Eb93258b93368531d39fAcCA3B4dC5854` |
| PermissionedRamp | `0xebC2459Ec962869ca4c0bd1E06368272732BCb08` |
| Deposit Wallet Factory | `0x00000000000Fb5C9ADea0298D729A0CB3823Cc07` |
| Deposit Wallet Beacon | `0x7A18EDfe055488A3128f01F563e5B479D92ffc3a` |
| Deposit Wallet Implementation | `0x58CA52ebe0DadfdF531Cde7062e76746de4Db1eB` |
| Proxy factory | `0xaB45c5A4B0c941a2F231C04C3f49182e1A254052` |
| Safe factory | `0xaacFeEa03eb1561C4e67d661e40682Bd20E3541b` |
| UMA adapter | `0x6A9D222616C90FcA5754cd1333cFD9b7fb6a4F74` |
| UMA Optimistic Oracle | `0xCB1822859cEF82Cd2Eb4E6276C7916e692995130` |

**Operación → ruta (snapshot, no sustituto de ABI) [S05a][S25][S34b]:**

| Operación | Destino | Función / entrada → salida | Confianza |
|---|---|---|---|
| CTF standard split / merge / redeem | standard collateral adapter + Conditional Tokens | funcs ABI §10; pUSD ↔ complete-set / winning outcome | ALTA CTF |
| CTF NegRisk split / merge / redeem | NegRisk collateral adapter | funciones según contexto SDK; pUSD ↔ CTF positions | ALTA ruta; validar ABI según operación |
| settlement ordinary | CTF Exchange v2 | signed Order+assets → settlement | ALTA |
| settlement NegRisk CTF | NegRisk CTF Exchange v2 | CTF NegRisk orders/assets → settlement | ALTA |
| old `convertPositions` | legacy NegRisk Adapter | NO(outcome) → complementary positions | ALTA como legacy, NO universal |
| v2 binary split/merge/redeem | Router + BinaryModule + PositionManager | condition, amount → ERC1155 v2 / collateral | ALTA ruta; firma calldata incompleta |
| v2 NegRisk conversion | NegRiskModule / Router (candidatos) | ABI exacta y discriminator de conversión **RESEARCH GAP** | **BLOCKED** |
| Combo prepare/split/merge | CombinatorialModule + Router + PositionManager | legs→condition; collateral↔Combo outcomes | ALTA ruta, ABI detallado incompleto |
| Combo trading settlement | Exchange v3 | RFQ signed Order → swap/settle | ALTA |
| auto redeem v2 | AutoRedeemer | redeemable v2 positions→collateral | ALTA rol, ABI no extraído |
| pUSD wrap / unwrap | CollateralOnramp/CollateralOfframp | supported collateral↔pUSD | ALTA dirección, ABI+asset route dinámica |
| gasless relay | Relayer + wallet account/contracts | owner-signed wallet calls → Polygon receipt | ALTA flujo |
| deploy Deposit | Factory → Beacon/implementation | deploy deterministic wallet | ALTA |
| session authorize/revoke | Deposit wallet `authorizeSessionSigner` / `revokeSessionSigner` | address, validUntil / address | ALTA |

**Approvals/allowances exactos por mecanismo [S05a][S34a]:**

| Asset | Owner | Spender/operator | Mecanismo | Requerido antes de |
|---|---|---|---|---|
| pUSD ERC20 | trading wallet | standard CTF Exchange | `approve` ERC20 | CTF ordinary BUY/settlement |
| ConditionalTokens ERC1155 | wallet | standard CTF Exchange | `setApprovalForAll` | CTF ordinary SELL |
| pUSD | wallet | NegRisk CTF Exchange | ERC20 allowance | CTF NegRisk BUY |
| ConditionalTokens ERC1155 | wallet | NegRisk CTF Exchange | ERC1155 operator | CTF NegRisk SELL |
| pUSD | wallet | standard collateral adapter | ERC20 allowance | split collateral CTF standard |
| ConditionalTokens ERC1155 | wallet | standard adapter | ERC1155 operator | merge/redeem standard |
| pUSD | wallet | NegRisk collateral adapter | ERC20 allowance | split CTF NegRisk |
| ConditionalTokens ERC1155 | wallet | NegRisk collateral adapter | ERC1155 operator | merge/redeem NegRisk CTF |
| pUSD | wallet | Exchange v3/v2 Router según función | ERC20 allowance | comprar/transformar v2/Combo, resolver spender por función |
| PositionManager ERC1155 | wallet | Exchange v3/Router/modules según operación | ERC1155 operator | vender/transformar v2/Combo |
| PositionManager ERC1155 | wallet | AutoRedeemer | ERC1155 operator | auto-redeem si aplicable |
| Order EIP712 | signer autorizado | CTF v2 Exchange/v3 verifyingContract | firma typed data | submit signed Order |
| Session Key | wallet owner | wallet registry | owner EIP712 + on-chain authorization | delegación temporal |

**No autorizar un spender por coincidencia de nombre**: el SDK pinned produce grafo de permisos leyendo allowance/ERC1155 state y sólo envía aprobaciones faltantes; el adapter NegRisk CLOB-v1 fue eliminado de `setupTradingApprovals` como spender universal. Los contratos proxy y módulos tienen address operativo proxy, NO implementation address como destino si la función no lo exige. Las direcciones/allowances son snapshot temporal: chequear registry/market protocol tras migración. [S25][S33][S34a]

## 12. Negative Risk: semántica, contract-version boundary y conversiones

**Tres ejes separados:** `Market.negRisk` indica un evento multiresultado con relación económica entre outcomes; `market.version`/contexto de posición determina **CTF-era frente a Protocol-v2**; `asset_id` identifica el token que CLOB negocia. El flag booleano `neg_risk` del book **no** identifica de forma única el ABI del contrato de conversión. El SDK vigente resuelve primero el Market por `conditionId`, después la versión y el adaptador/router de *split, merge y redeem*; esta resolución no constituye evidencia de que tenga un conversor universal NO→YES válido para las dos generaciones. [S04][S26][S34b]

**Invariante semántica según documentación:** para un evento exhaustivo y mutuamente excluyente de N outcomes conocidos, poseer `1 NO(A)` puede convertirse **atómicamente** en `1 YES(B)` para cada `B ≠ A` mediante el mecanismo NegRisk apropiado. Ejemplo de tres candidatos `A,B,Other`: antes `{NO(A):1}`; después `{YES(B):1, YES(Other):1}`; no se emite un YES(A). Este ejemplo representa el mecanismo **publicado para el adaptador CTF** y no documenta la ABI de Protocol-v2. La equivalencia económica entre un NO y la cesta complementaria no constituye por sí sola autorización para ejecutar un `convertPositions` en cualquier dirección. La fuente oficial llama atómica la conversión vía adaptador; el desglose exacto de eventos emitidos/gas no está especificado. [S26]

| Propiedad | CTF-era NegRisk | Protocol-v2 NegRisk | Evidencia/acción documental |
|---|---|---|---|
| Identificación de mercado | `conditionId`, `negRisk`, `market.version` | `conditionId`, versión v2, contexto Router/PositionManager | Gamma/CLOB + función `resolveMarketPositionContext` del SDK; nombres y esquema wire de todas las variantes `version`: RESEARCH GAP [S06][S34b] |
| Exchange settlement | NegRisk CTF Exchange `0xe2222d279d744050d28e00520010520000310F59` | no equiparar automáticamente con Exchange v3 / módulo NegRisk | registry §11 [S25] |
| Collateral split/merge/redeem | NegRisk CTF collateral adapter `0xadA2005600Dec949baf300f4C6120000bDB6eAab` | Protocol-v2 Router `0x12121212006e4CD160D18e3f00711DA5c3372600` | rutas separadas verificadas en SDK [S34b] |
| NO→complementary YES | adaptador NegRisk CTF antiguo `0xd91E80cF2E7be2e162c6513ceD06f1dD0dA35296`, semántica histórica; **deprecated para relayer** | **ABI, contract address, selector y metadata de evento NO VERIFICADOS** | fuente de concepto describe convert sin discriminar versión; changelog 2026-07-14 retira llamadas antiguas relayer desde 2026-07-17 [S26][S32] |
| Ruta de conversión live | prohibida vía relayer antiguo después del retiro; documentar ruta moderna exacta antes de usar | `NO LIVE CONVERSION UNTIL ROUTE VERIFIED` | bloqueo por contrato, no heurística |

**Divergencia preservada:** la página de conceptos conserva la explicación general «call convert on Neg Risk Adapter», mientras el changelog de 2026-07-14 marca la dirección antigua como retirada del Relayer y llama a `0xadA200...` adaptador actual para **acciones con colateral pUSD**. El cambio NO demuestra que esa segunda dirección implemente el mismo `convertPositions`; no reemplazar ABI por semejanza nominal. Una conversión on-chain exitosa debe identificarse por la transacción, logs y diferencias de balances; NO por un cambio en precios Gamma. [S26][S32][S25]

**Augmented NegRisk.** Un Event puede arrancar con outcomes nombrados, slots `Placeholder` sin nombre y `Other` explícito. Una clarificación en el bulletin board asigna un nombre a un placeholder sin que ello garantice inmutabilidad editorial del conjunto visible; tras cada naming, `Other` reduce su dominio residual. La documentación dice que placeholders sin nombre no aparecen en la UI y que si a resolución el resultado no fue nombrado corresponde a `Other`. `Other` NO es un asset con reglas estáticas independientes del conjunto de nombres; preservarlo como outcome propio y conservar sucesivas versiones de rules si se requieren interpretaciones históricas. No hay API first-party de versiones completas de todas las aclaraciones garantizada. [S26][S27]

**Capital y operaciones:** split bloquea colateral y crea complementarios; merge quema un set completo y devuelve colateral; conversión NegRisk transforma inventario entre outcomes del mismo evento sin prometer redención anticipada de colateral; redeem requiere payout final. Estas son cuatro operaciones diferentes y las tres primeras no deben confundirse con órdenes CLOB ni con Combo `collateral-return`. Ejemplo: un set `{YES(A), NO(A)}` de una share se mergea por 1 unidad de colateral; `NO(A)` aislado sólo se transforma en la cesta `YES(B≠A)` cuando el mecanismo NegRisk documentado y su versión lo permiten. [S05a][S26][S28b]

**Blocking contract de conversión v2:** falta una tupla comprobada `(market/version discriminator, event/condition identifier, target router/module address, exact ABI/function selector, argument mapping, allowance policy, transaction return/logs)`. Aunque el SDK confirma rutas Router para split/merge/redeem, NO se certifica `convertPositions` de v2. Estado: `NO LIVE CONVERSION UNTIL ROUTE VERIFIED`; clasificado como RESEARCH GAP de implementación (§24), no como ausencia demostrada de capability. [S34b][S25]

## 13. Combinatorial Positions ≠ NegRisk ≠ Combo/RFQ

**Combinatorial Positions:** una conjunción de legs, por ejemplo `YES(A) ∧ YES(B) ∧ NO(C)`, produce una condición derivada y dos posiciones complementarias `Combo YES` y `Combo NO` emitidas por el **Positions Framework**, no por el CTF ERC1155 original. `Combo YES` paga si todas las legs ganan; `Combo NO` si la conjunción no se cumple. Split de colateral crea el par; merge quema un par; al resolver algunas legs, una posición puede comprimirse a la exposición todavía no resuelta. `conditionId` de Combo, `positionId` YES/NO, `leg_position_ids` y `rfq_id` son namespaces diferentes. [S05c][S29]

**Combo RFQ:** mecanismo de cotización/ejecución entre requester y quoter para el activo combinatorial; NO es la operación de NegRisk y NO es automáticamente un order-book para cada Combo. Una request no está firmada en su creación; las quotes son firmadas por quoters; al aceptar, requester firma una **orden Exchange-v3**. Dirección producción: REST catálogo `https://combos-rfq-api.polymarket.com`, requester `https://combos-rfq-gateway-requester-api.polymarket.com`, quoter WS `wss://combos-rfq-gateway-quoter.polymarket.com/ws/rfq`, builder gateway `https://combos-rfq-gateway-builder.polymarket.com`. [S28][S29][S48]

| Requester HTTP | Auth | Wire crítico | Identity / recuperación |
|---|---|---|---|
| `GET https://combos-rfq-api.polymarket.com/v1/rfq/combo-markets?limit=50` | público | `{markets:[...],next_cursor}`, próximo request `cursor=next_cursor`; arrays `position_ids`, `outcomes`, `outcome_prices` alineados, índice 0 YES/1 NO | descubrir legs; metadatos actuales, no historiales [S28] |
| `POST https://combos-rfq-gateway-requester-api.polymarket.com/v1/requester/rfq/requests` | cinco headers CLOB L2 | `{signer_address,maker_address,signature_type,leg_position_ids,direction:"BUY"|"SELL",side:"YES",requested_size:{unit:"notional"|"shares",value_e6:"..."}}`; 2–50 IDs de legs únicas/compatibles. BUY pide presupuesto colateral incluidas fees; SELL shares. | `rfq_id`, `status`, `expires_at` epoch ms, `request.condition_id`, `yes_position_id`, `no_position_id`, `quote.quote_id`,`blended_price_e6`,`maker_amount_e6`,`taker_amount_e6`,`total_required_e6`,`net_receive_e6`. Por maker máximo 15 creaciones/min, 429 `RATE_LIMITED` [S28] |
| `GET https://combos-rfq-gateway-requester-api.polymarket.com/v1/requester/rfq/requests/{rfq_id}` | L2 fresco por request | `rfq_id` path, sin body; estado/request/quote/trade según progresión | sirve para estado **sólo si se conoce rfq_id** [S28] |
| `POST https://combos-rfq-gateway-requester-api.polymarket.com/v1/requester/rfq/requests/{rfq_id}/accept` | L2 + signed Exchange-v3 order | order firmado, exact wrapper en Requesters; `rfq_id` path, firma wallet compatible y deadline | aceptación ≠ fill; leer estado por ID, settlement/receipt cuando aparezca [S28] |
| `POST https://combos-rfq-collateral-return.polymarket.com/v1/collateral-return/plan` | doc muestra JSON `{wallet}` y sin Relayer key para lectura plan | propone `plan_hash`, posición, movimientos/operaciones, `net_pusd_out` | plan sujeto a posición/estado y no ejecuta nada [S28b] |
| `POST https://combos-rfq-collateral-return.polymarket.com/v1/collateral-return/submit` | `RELAYER_API_KEY`,`RELAYER_API_KEY_ADDRESS` + envelope de wallet firmado | `{plan_hash,envelope:{...}}`; mismo nonce/deadline/call incluidos en firma | devuelve trámite de ejecución; confirmar receipt y balances, no reutilizar plan tras mutación [S28b] |

`POST /requests` sin respuesta es **ambiguous write documentada**: NO hay idempotency key ni lookup sin el ID asignado por el servidor; repetir puede crear otra RFQ. `NO_QUOTES` puede llegar en `HTTP 200` con `status:"FAILED"`; no interpretarlo como error HTTP. EOA tipo 0 NO está soportada por gateway requester; Deposit tipo 3, Proxy tipo 1 y Safe tipo 2 sí. `expires_at` de la quote en el ejemplo de requester es una ventana de 5 segundos desde ready; overview también presenta 10 segundos de aceptación — **contradicción entre páginas**: para una quote concreta manda deadline `expires_at`, no asumir una duración fija. Quoters tienen ventana de 400 ms para competir y Last Look hasta 1 s según overview. [S28][S29]

**Order Exchange-v3:** domain `name="Polymarket CTF Exchange"`, `version="3"`, `chainId=137`, `verifyingContract=0xe3333700cA9d93003F00f0F71f8515005F6c00Aa`; no usar domain version `2` de orden CLOB en esta operación. En requesters, `makerAmount/takerAmount` se copian de los valores E6 exactos de quote; `tokenId=Combo YES position ID`, `side` 0 BUY/1 SELL, `builder=bytes32(0)` (no atribución Builder en ese gateway); Deposit Wallet firma payload externo `TypedDataSign` y entrega firma ERC-7739, Proxy/Safe firma `Order` directo. `timestamp` del ejemplo Exchange-v3 está en **segundos**, frente a milisegundos CLOB-v2. [S28][S15]

**Builder Gateway:** la documentación separa roles y headers: `POST /requests` y `POST /requests/{rfq_id}/accept` requieren **account headers + Builder headers**, mientras `GET /requests/{rfq_id}` después de aceptación exige account headers y pide **no enviar** Builder headers. Esos paths son relativos al gateway builder; base path prefijado y body completo para todas las variantes **RESEARCH GAP** — no asumir que la ruta requester completa y builder gateway tienen el mismo prefijo. [S28a]

**Collateral return** realiza un plan de descomposición/merge de posiciones compatibles, conserva riesgo residual y puede devolver parte de colateral ANTES de la resolución de todas las legs. Está soportado para Deposit, Proxy y Safe, no EOA. El plan puede enumerar `split,merge,redeem,split_on_condition,merge_on_condition,split_on_event,merge_on_event,convert_on_event,extract,inject,convert_to_yes_basket,merge_from_yes_basket,compress`, incluyendo valores de operación futuros no conocidos por el enum del SDK. `plan_hash` vincula el plan firmado al enviado. Esto no establece que exista una RPC genérica de usuario para conversión Negative Risk v2. [S28b]

## 14. Fees — cálculo, fuente efectiva y snapshot 2026-09-17 UTC

**Fee de plataforma:** makers no pagan fee de plataforma; takers en mercados fee-enabled pagan al match, no al crear orden. Para C shares y precio p en [0,1], `fee_USDC = C × feeRate × p × (1-p)`. Fee simétrica entre p y 1-p, máxima en p=0.5 para C constante. La página especifica **redondeo del importe final a cinco decimales**, importe positivo mínimo `0.00001 USDC`, y que fees por debajo del mínimo se redondean a **0**. NO se publica explícitamente la regla de empate a medio incremento, ni orden interno de operaciones intermedias. El contrato del fee page habla de USDC; pUSD es collateral efectivo on-chain de trading según §5. [S21][S05]

| Categoría | Coeficiente taker `feeRate` | Maker plataforma | Redistribución maker | `verified_at` |
|---|---:|---:|---:|---|
| Crypto | 0.07 | 0 | 20% | 2026-09-17 UTC [S21] |
| Sports | 0.05 | 0 | 15% | 2026-09-17 UTC [S21][S32] |
| Finance, Politics, Mentions, Tech | 0.04 | 0 | 25% | 2026-09-17 UTC [S21] |
| Economics, Culture, Weather, Other/General | 0.05 | 0 | 25% | 2026-09-17 UTC [S21] |
| Geopolitics | 0 | 0 | none | 2026-09-17 UTC [S21] |

**Discovery de fee vigente.** Gamma entrega flags `feesEnabled`, CLOB `GET /fee-rate?token_id=...` y alternativa `/fee-rate/{token_id}` devuelve `{base_fee:int64}` en **bps**; CLOB market info `GET /clob-markets/{condition_id}` contiene `fd` con `r,e,to` según contrato v2, y la página Fees publica coeficiente por categoría. Estas piezas no están documentadas como una única fórmula de conversión directa `base_fee↔feeRate`; el contrato oficial instruye leer parámetros por mercado. **RESEARCH GAP**: unir exactamente flags+config v2+base_fee para todas las rutas sin especulación. No meter fee de plataforma como campo del signed order actual (§7); CLOB lo aplica al match. [S21][S40a][S40b][S32a]

**Builder Fee, distinto:** al incluir un `builder:bytes32` con código habilitado en la orden, existe cargo adicional lineal `trade notional × bps / 10000`, independientemente del fee de plataforma; topes observados maker 50 bps/taker 100 bps, granularidad 1 bp, cambios sujetos a ventana del programa. Ausencia de código no equivale a fee builder obligatoria. Requester Combo gateway rechaza `builder` distinto de cero; usar su Builder gateway propio si corresponde. El SDK/usuario no debe deducir fee efectiva del midpoint ni de snapshots. [S35][S28]

## 15. Programas — cuatro ledgers distintos

| Programa | Elegibilidad / cálculo documentado | Frecuencia, umbrales y API | Snapshot/fuente |
|---|---|---|---|
| Maker Rebates | maker **filled** en mercado elegible; `fee_equivalent=C×feeRate×p×(1-p)`, asignación proporcional al pool distribuible de 20% Crypto, 15% Sports, 25% otras fee-enabled | distribución diaria pUSD; mínimo acumulado para pago **$1**. `GET CLOB /rebates/current` figura en spec pero auth/wire exacto aún gap | 2026-09-17 [S23][S21][S40] |
| Taker Rebates | solo trades **taker** elegibles; `wV = (shares×entryPrice USD) × (1−entryPrice) × categoryWeight × bonuses`; tier según ventana rolling 30 días | pago diario pUSD, mínimo para pago **$1**, tier/beneficio sobre operaciones **futuras**; tiers abajo | 2026-09-17 [S22] |
| Liquidity Rewards | órdenes resting elegibles, score por tamaño, distancias al midpoint, dos lados/participación relativa; config dinámica por market de min size/max spread/pool | pago diario medianoche UTC; mínimo **$1**. API config `GET /rewards/markets/current`, `/rewards/markets/{id}` y scoring endpoints §3; TWAP allocation especial agosto 2026 **TERMINÓ** | 2026-09-17 [S24] |
| Builder Fees | código builder bytes32 firmado en orden y fee sobre notional por maker/taker según ajuste perfil | additive a plataforma; códigos/tasas pueden cambiar y revocarse; no confundir con maker rebate ni taker rebate | 2026-09-17 [S35] |

**Taker rebate tiers y multiplicadores exactos — snapshot 2026-09-17 UTC [S22]:**

| Nivel | Tier | weighted volume últimos 30 días | Rebate futuro | Primer bono de nivel (pUSD) |
|---:|---|---:|---:|---:|
| 0 | None | < US$2.000 | 0% | — |
| 1 | Bronze | US$2.000 | 3% | US$10 |
| 2 | Silver | US$20.000 | 8% | US$50 |
| 3 | Gold | US$200.000 | 18% | US$250 |
| 4 | Platinum | US$1.000.000 | 32% | US$1.500 |
| 5 | Diamond | US$4.000.000 | 44% | US$7.500 |
| 6 | Obsidian | ≥ US$10.000.000 | 50% | US$25.000 |

Pesos categoría: Sports 1.0; Politics/Finance/Mentions/Tech 1.3; Economics/Culture/Weather/Other 1.7; Crypto 2.3; Geopolitics 0. Los bonos extra de categoría/evento son multiplicadores administrados por Polymarket, NO constantes universales. El tier sube y aplica desde que se alcanza; las reducciones y su posible gracia pueden seguir la política del programa; tolerancia exacta a eventos tardíos del ledger `NOT DOCUMENTED`. El programa fue anunciado con inicio **2026-05-28** y paga diariamente en pUSD. [S22]

**Campos observables para inventario de rewards**: Market Gamma `rewardsMinSize,rewardsMaxSpread,rewardsDailyRate` cuando estén publicados, CLOB `/rewards/markets/current` configuración; `GET /order-scoring`, `/orders-scoring` elegibilidad, `/rewards/user...` montos agregados y transacciones on-chain como prueba de pago. Score instantáneo ≠ entitlement final; `rate` del programa ≠ fee-rate del trade. Schema/auth precisos de los endpoints secundarios ya identificados como RESEARCH GAP en §3. [S06][S24][S40]

## 16. Resolution — lifecycle, fuentes de tiempo y payouts

**Principio:** `endDate` editorial ≠ resultado observable ≠ trading closed ≠ proposed ≠ disputado ≠ final oracle resolution ≠ redeemable ≠ redeemed. La pregunta y las reglas específicas del Market, fuente de resolución y clarificaciones on-chain prevalecen sobre inferencias por título o fecha. El documento oficial admite clarificación de edge cases en bulletin board, pero no cambio de intención fundamental. [S06][S27]

| Estado/etapa | Autoridad/identificador | Tiempo/duración | Resultado y carácter terminal |
|---|---|---|---|
| Event/Market end | Gamma `endDate`; rules | ISO según metadata, puede variar | cierre programado no prueba outcome ni payout |
| Outcome observable | resolución fuente definida por rules, externa | puede retrasarse respecto end | dato contextual, NO liquidación |
| Order book closed | Gamma/CLOB status y Market WS `market_resolved` cuando aplica | servicio event-time | detiene nuevas órdenes; orders existentes deben reconciliarse |
| UMA proposal | Optimistic Oracle + propuesta, proposer + bond | bond típicamente `750 pUSD` según docs, efectivo on-chain dinámico | no final; sujeto a disputa |
| Challenge/liveness | UMA Oracle | docs: **2 horas** desde proposal | sin disputa resolución aceptada al terminar ventana |
| First dispute | UMA + disputer bond (habitualmente igual) | abre segunda propuesta | NO terminal |
| Second proposal | UMA | otra challenge window | sin disputa finaliza; segunda disputa escala DVM |
| DVM escalation | UMA debate/votación | debate **24–48 h**; voto alrededor de **48 h**; caso disputado estimado **4–6 días** | no asumir deadline exacto por API static |
| Final outcome + payout vector | UMA result/CTF condition payout | tx/block timestamp chain | win 1/lose 0; excepción UNKNOWN/50-50 paga 0.5 a cada token binario |
| Redeemable | payout final + saldo elegible | posterior a resolution/settlement | habilita llamada on-chain, NO implica ya cobrado |
| Redeemed | adapter/Router receipt + balances | block inclusion | se queman ERC1155 elegibles, pUSD recibido |

**API:** datos actuales Gamma (`conditionId`, `resolved`, `closed`, `endDate`, `resolutionSource`, `outcomePrices`, `umaResolutionStatus` donde exista), `GET D2 /v2/resolutions` para lifecycle agregado y lectura on-chain UMA/CTF para payout final; Data v2 y SDK exponen posición `REDEEMABLE`. La presencia de `outcomePrices=[1,0]` en un JSON de mercado NO es un recibo de redemption. Joins: `conditionId` market → resolution record/condition, posición `(wallet,asset/positionId)` → payout, tx receipt/hash → saldo final. El contrato exacto de TODOS los campos de `GET /v2/resolutions`, incluidos enum/timestamp, sigue siendo RESEARCH GAP mientras su OpenAPI raw no haya sido parseado (§24); no inventar enum universal. [S27][S41][S33]

**Capital lock:** colateral de una YES/NO aislada queda inmovilizado como token de exposición hasta vender, completar set y mergear, o resolución+redeem; proposición no libera colateral. No mezclar bond UMA con colateral de posiciones. Fechas normales e incidentes son estimaciones de página oficial, no SLA. [S05a][S27]

## 17. Datos históricos, retención y capacidad de replay

La Data API v2 entró en producción según changelog **2026-09-04**, y sus rutas envuelven todos los payloads en `data`, con `pagination`/cursor opaco cuando aplica. v1 continúa en modo **frozen/legacy**. CLOB `/prices-history` existía antes; ruta preferente para nuevos datos históricos de precio es **`GET https://data-api.polymarket.com/v2/prices-history`** con selector exclusivo `interval` o `start`/`end` o `as_of`, `bucket_seconds` en segundos; paginación cursor. SDK `listPriceHistory` incluye decimal-string `price`, timestamp epoch ms y `resolutionSeconds`, pero **eso es transformación SDK**, no licencia para asignar tipos iguales a raw JSON v2, cuyos money/size son JSON numbers según changelog. [S32][S33][S41]

| Dataset | First-party CURRENT | Granularidad/cursor | Earliest, retención, SLA | ¿Replay determinista? |
|---|---|---|---|---|
| Price history | D2 `GET /v2/prices-history`; CLOB legacy `/prices-history` | time buckets y cursor D2; fidelity/interval CLOB | earliest y retention SLA: NOT DOCUMENTED | **no**: precios agregados ≠ órdenes |
| Trades públicos | D2 `GET /v2/trades`, CLOB L2 `/data/trades` | filas por match, cursor por API; tx hash puede llegar después | cobertura histórica completa/retención garantizada NOT DOCUMENTED | reconstruye operaciones observadas, NO intents/cancel/L2 |
| Wallet activity | D2 `/v2/activity` y `/v2/activity/combos`, v1 `/activity` legacy | cursores D2, tipo+tx cuando aplica | SLA de exhaustividad NOT DOCUMENTED | movimientos de wallet, no todas las cotizaciones |
| Positions actuales | D2 `/v2/positions`,`/v2/positions/combos`, balance ERC1155 onchain | snapshot/estado por wallet; cursor | retención de snapshots pasados NOT DOCUMENTED | balance actual no reproduce trayectoria exacta |
| Closed positions | D2 positions `status=CLOSED` / v1 `/closed-positions` frozen | cierre/agregados | origen y límites históricos por cuenta NOT DOCUMENTED | no orden por orden |
| Resolution | D2 `/v2/resolutions` + UMA/CTF logs y tx | eventos y bloc timestamps | historia chain existe desde deployment, pero ingestión API SLA NOT DOCUMENTED | puede reconstruir result chain con logs suficientes, no rules editoriales |
| Open orders | CLOB L2 `/data/orders`; `/data/order/{id}` | estado por ID/cursor | retención de órdenes terminales NOT DOCUMENTED | solo órdenes propias recuperables |
| Cancelled orders | CLOB `/data/order` si ID conocido; logs del cliente/WS | sin archivo histórico público de todos los cancels publicado | SLA/coverage NOT DOCUMENTED | NO full lifecycle universal |
| L2 snapshots | CLOB REST `/book`,`POST /books`, WS `book`; errores oficiales mencionan `GET /orderbook-history` | snapshots actuales; `/orderbook-history` sí aparece en error reference pero schema/coverage sin extraer | retención histórica full snapshots NOT DOCUMENTED | **NO certificado** |
| L2 deltas | Market WS `price_change` | live, sin secuencia/replay garantizados | archivo first-party integral histórico no establecido | **NO certificado** |
| Market rules versions | Gamma rules corrientes; bulletin board clarifications on-chain | snapshots editoriales vs logs cadena | archivo de versiones todas las modificaciones NOT DOCUMENTED | NO fiel al pasado sin captura propia |
| Fee history | fee NOW por category/market, changelog de modificaciones | cambios puntuales fecha | histórico per-market fee-effective total NOT DOCUMENTED | no reconstrucción histórica completa |
| Reward/rebate history | programas/docs + ledger de usuario/API reward; payouts chain | daily y stats | score completo por order/per market del pasado no garantizado | no simulación determinista de rewards |

**Respuesta precisa sobre archivo L2:** no se verificó un **archivo first-party público, completo y con SLA** de snapshots **y** deltas L2 que permita replay determinista. Pero NO afirmar categóricamente que «no existe histórico de books»: el Error Codes oficial contiene `GET /orderbook-history`, cuya semántica, coverage y retention siguen **RESEARCH GAP** y deben investigarse; existen snapshots REST actuales. Las observaciones L2 que no aparecen en price history/trades ni en un archivo L2 exhaustivo son **irreconstruibles desde esas APIs**. Para resolver gaps WS no existe `resume_from_sequence` publicado en Market AsyncAPI. [S18][S08][S45][S41]

## 18. Rate limits CURRENT — tabla oficial 2026-09-17 UTC

Fuente normativa para números: página viva de rate limits [S19], contrastada con cambios del 2026-06-01 [S32]. **Cloudflare por IP, ventanas móviles**; exceder suele **demorar/encolar**, no necesariamente responder 429 inmediatamente. CLOB trading agrega **dos buckets token-bucket por signer** independientes (orders y cancellations) [S20]. La página [S20] describe modo de advertencia a partir de 2026-07-24 durante dos semanas y futura activación con anuncio; NO proporciona en su texto una fecha inequívoca de activación observada al 2026-09-17, por lo que no afirmar enforcement efectivo sólo por el calendario. Header `Poly-RateLimit-Warning:true` documenta warning; al activarse, insuficiencia de tokens devuelve 429 con `Retry-After` en segundos. Rate limiting Cloudflare IP puede demorar en vez de emitir 429. `Retry-After` genérico de cada bucket IP NO documentado. Rate limits son dinámicos, estos números son snapshot. [S19][S32]

| Host/surface | Bucket por IP | Burst/window | Sustained/window |
|---|---|---:|---:|
| General | todos | 15.000/10 s | — |
| health `/ok` | health | 100/10 s | — |
| Gamma | general | 4.000/10 s | — |
| Gamma | `/events` | 500/10 s | — |
| Gamma | `/markets` | 300/10 s | — |
| Gamma | `/markets` + `/events` listing | 900/10 s | — |
| Gamma | `/comments`, `/tags`, `/public-search` | 200, 200, 350/10 s respectivamente | — |
| Data v1 frozen | general, trades, positions, closed positions | 1.000, 200, 150, 150/10 s | — |
| Data v2 | general `/v2` | 800/10 s | — |
| Data v2 | trades | 300/10 s | — |
| Data v2 | positions+combos, activity+combos, price history, status | 200, 200, 200, 100/10 s respectivamente | — |
| CLOB | general | 9.000/10 s | — |
| CLOB | GET balance-allowance, refresh allowance | 200, 50/10 s | — |
| CLOB book / books | market data | 1.500, 500/10 s | — |
| CLOB price / prices | market data | 1.500, 500/10 s | — |
| CLOB midpoint / midpoints | market data | 1.500, 500/10 s | — |
| CLOB price history / tick size | market data | 1.000, 200/10 s | — |
| CLOB `/trades`,`/orders`,`/notifications`,`/order` general ledger | ledger | 900/10 s | — |
| CLOB `/data/orders`,`/data/trades`,`/notifications` specific | ledger | 500, 500, 125/10 s | — |
| CLOB | API-key family | 100/10 s | — |
| CLOB `POST /order` | trading | 5.000/10 s | 120.000/10 min |
| CLOB `DELETE /order` | trading | 5.000/10 s | 120.000/10 min |
| CLOB `POST /orders` | trading | 2.000/10 s | 21.000/10 min |
| CLOB `DELETE /orders` | trading | 2.000/10 s | 15.000/10 min |
| CLOB `DELETE /cancel-all` | trading | 250/10 s | 6.000/10 min |
| CLOB `DELETE /cancel-market-orders` | trading | 1.500/10 s | 21.000/10 min |
| Bridge | general | 50/10 s | — |
| Relayer | `/submit` | 25/1 min | — |
| User PnL | analytics | 200/10 s | — |

**Buckets por signer [S20].** Signer = dirección vinculada a la credencial CLOB; eligibility de tier por volumen del **maker wallet** aun cuando maker≠signer; 30 días móviles, clasificación actualiza cada tres horas. Refill continuo; dos buckets independientes. `POST /order`: 1 token ORDER; `POST /orders`: cantidad de órdenes en batch no vacío; `DELETE /order`: 1 token CANCEL; `DELETE /orders`: número de IDs; `DELETE /cancel-all` y `/cancel-market-orders`: un token inicial + 1 por orden efectivamente cancelada; tier con deuda CANCEL puede mostrar balance negativo hasta el refill. Un batch cuyo costo exceda burst nunca será admitido; rechazo del gate es all-or-nothing aunque las respuestas por orden de un batch admitido puedan mezclar éxitos y rechazos.

| Tier signer | Volumen maker 30d USD | ORDER refill tok/s | ORDER burst | CANCEL refill tok/s | CANCEL burst | Deuda CANCEL admitida |
|---|---:|---:|---:|---:|---:|---|
| Standard | sin mínimo | 40 | 60 | 80 | 120 | Sí |
| Copper | 30.000 | 60 | 90 | 120 | 180 | Sí |
| Bronze | 50.000 | 80 | 120 | 160 | 240 | Sí |
| Silver | 100.000 | 200 | 300 | 400 | 600 | Sí |
| Gold | 500.000 | 400 | 600 | 800 | 1.200 | Sí |
| Platinum | 2.500.000 | 450 | 675 | 900 | 1.350 | No |
| Diamond | 5.000.000 | 525 | 787 | 1.050 | 1.575 | No |
| Elite | 10.000.000 | 600 | 900 | 1.200 | 1.800 | No |

Headers cuando se evalúa: `Poly-RateLimit-Remaining` (puede ser negativo para cancelaciones), `Poly-RateLimit-Reset` (UNIX estimación del fin de espera, no full refill), `Poly-RateLimit-Tier`; `Poly-RateLimit-Warning:true` en modo warning para peticiones que se rechazarían con enforcement; `Retry-After` segundos en 429. Si costo ≤ burst y tokens insuficientes, 429 durante enforcement; si costo > burst, cambiar tamaño de batch, esperar NO lo admite. La documentación NO confirma que enforcement ya estuviera activo en la fecha de sincronización, sólo explica el rollout anunciado. **Scopes:** tabla principal por IP y esta tabla por signer, no un throughput garantizado acumulativo. No inferir que el límite por IP puede usarse por cada API key.  Taker rebate wV, wallet activity, category weights y maker reward score tienen límites propios de negocio y no son cuotas HTTP. La API de requester RFQ publica además **15 POST create por rolling minute por `maker_address`**, HTTP 429 `RATE_LIMITED` [S28]. [S19][S20]

## 19. OpenAPI y AsyncAPI: inventario, divergencias y límites de extracción

**Autoridades descubribles.** El índice oficial `llms.txt` publica **seis OpenAPI de Prediction Markets** que requieren revisión (`gamma-openapi.yaml`, `clob-openapi.yaml`, `data-openapi.yaml`, `relayer-openapi.yaml`, `combos-rfq-openapi.yaml`, `bridge-openapi.yaml`) y un **OpenAPI Data v2 independiente** en `https://data-api.polymarket.com/v2/openapi.json`; el primer enlace de Data v2 del índice, `https:/data-api...`, está mal formado y aparece un segundo enlace correcto. Perps OpenAPI se excluye. Asimismo indexa los AsyncAPI market, user, sports y RFQ, más `/developers/open-api/connect-wss.json`; Perps AsyncAPI excluido. El hecho de que un spec se anuncie en el índice **no demuestra** que su cuerpo haya sido recuperado y parseado: conservar la distinción. [S01][S39][S40][S41][S42][S43][S44][S45][S46][S47][S48][S49]

### 19.1 OpenAPI — estado real de lectura y cobertura

| ID | Documento y URL exacta en §26 | Versión/host conocido | Paths / operaciones | Estado de esta auditoría |
|---|---|---|---|---|
| S39 | Gamma YAML | Gamma prod identificado por SDK | **NO MEDIDO** | enlazado por índice oficial; raw YAML no descargado ni parseado mecánicamente aquí; RESEARCH GAP para cobertura total |
| S40 | CLOB YAML | CLOB prod identificado por SDK | **NO MEDIDO** | índice oficial; raw no parseado; RESEARCH GAP para totalidad, en especial endpoints ajenos al catálogo focalizado |
| S41 | Data v2 OpenAPI JSON | `/v2`, host Data prod | **NO MEDIDO** | índice ofrece URL JSON real; no consta árbol completo de `paths` parseado; RESEARCH GAP para cobertura total |
| S41a | Data legacy YAML | Data v1 frozen | **NO MEDIDO** | índice oficial; separado de Data v2, sólo migración/compatibilidad |
| S42 | Relayer YAML | Relayer v2 prod | **NO MEDIDO** | índice, raw no parseado; RESEARCH GAP para totalidad |
| S43 | Combo/RFQ YAML | combo RFQ prod | **NO MEDIDO** | índice, raw no parseado; requester/builder gateways adicionales NO automáticamente cubiertos |
| S44 | Bridge YAML | bridge prod | **NO MEDIDO** | índice, raw no parseado; funding solamente |

**Gate de auditoría mecánica:** `every CURRENT OpenAPI operation → catalogued OR OUT_OF_SCOPE(reason)` permanece **NO APROBADO**; no se ha construido un manifiesto reproducible con `info.title`, `info.version`, `servers`, `paths`, verbos, tags y security schemes para cada YAML/JSON. Las filas de §3 son contratos importantes auditados por páginas oficiales y repos, **no se declaran equivalentes a un inventario exhaustivo**. En particular, la semántica exacta de operación de `/orderbook-history`, `GET /v2/resolutions`, notificaciones y algunas rutas builder/Bridge exige parseo y lectura adicional. No cambiar esta limitación a `NOT DOCUMENTED`: los documentos fuente existen. [S01][S18][S41]

### 19.2 AsyncAPI — inventario verificable

| ID | Documento, versión; host | Canales | Operaciones / tipos de mensaje | Extracción |
|---|---|---:|---|---|
| S45 | Market AsyncAPI **3.0.0**, `info.version=1.0.0`; `wss://ws-subscriptions-clob.polymarket.com/ws/market` | 1 `market` | **11 operaciones, 11 mensajes**: `subscriptionRequest`, `subscriptionRequestUpdate`, `ping`, `pong`, `book`, `priceChange`, `lastTradePrice`, `tickSizeChange`, `bestBidAsk`, `newMarket`, `marketResolved` | JSON visible; identificadores enumerados de `channels.market.messages` y `operations` |
| S46 | User AsyncAPI **3.0.0**, `info.version=1.0.0`; `/ws/user` mismo host | 1 `user` | **6 operaciones, 6 mensajes**: solicitud/actualización suscripción, ping/pong, `order`, `trade` | JSON visible; distinguir evento `order` de estado de orden |
| S47 | Sports AsyncAPI **3.0.0**, `info.version=1.0.0`; `wss://sports-api.polymarket.com/ws` | 1 sports | **3 operaciones/mensajes**: ping, pong, `sportsUpdate` | JSON visible; WS abierto sin `assets_ids`; servidor PING cada 5s, cliente PONG dentro de 10s según spec |
| S48 | RFQ AsyncAPI, `wss://combos-rfq-gateway-quoter.polymarket.com/ws/rfq` por SDK | **NO MEDIDO** | **NO MEDIDO** | vínculo JSON oficial, cuerpo no recuperado; RESEARCH GAP para mensaje por mensaje |
| S49 | `connect-wss.json` listado en índice; variante histórica | 1 market observado | **2 operaciones, 5 mensajes**, versus 11 en S45 | representación antigua/subconjunto: NO usar para suprimir mensajes actuales de S45; no resuelve discrepancias por sí sola |

*Detalle por familia de mensajes* (dirección relativa al cliente):

| Canal | Cliente → servidor | Servidor → cliente | Key y hora | Snapshot/delta; sequencing |
|---|---|---|---|---|
| Market | initial `{assets_ids:[tokenId],type:"market",custom_feature_enabled?,initial_dump?}`; update `{operation:"subscribe"|"unsubscribe",assets_ids:[...]}`; texto `PING` cada 10 s | `PONG`; `book`, `price_change`, `last_trade_price`, `tick_size_change`, `best_bid_ask`, `new_market`, `market_resolved` | `asset_id` token; `market` condition; `timestamp` string epoch **ms** en mensajes indicados | `book` fotografía agregada; `price_change` modifica niveles; hash en `book` y cambios NO es un número de secuencia; ordering/gap checksum/replay **NOT DOCUMENTED** [S45] |
| User | auth L2 + subscription `type:"user"`, filtro `markets` conditionIds; updates y texto heartbeat según spec | `order`, `trade`, PONG | IDs de orden/trade y condition; timestamps por field del mensaje, no un reloj universal | eventos de negocio propios; no snapshot total ni replay garantizado; reconciliar REST [S46][S09] |
| Sports | WS público; PONG al ping del servidor | `sportsUpdate` | `slug` exigido; `score` string, `last_update` ISO8601 | actualización de resultado, NO libro; secuencia, resume/replay **NOT DOCUMENTED** [S47] |
| RFQ | auth/subscription según spec, no reconstruir desde la definición de SDK | quotes, RFQ, trade según documentación prose | RFQ ID, quote ID, deadlines epoch ms cuando están publicados | catálogo exacto y resubscription: **RESEARCH GAP**, no asignar secuencias [S28][S48] |
| RTDS | JSON `subscribe` a `crypto_prices`, `crypto_prices_chainlink` y topics admitidos, PING texto según página | envelope `{topic,type,timestamp,payload}` | filtro dependiente del topic, source timestamp ms donde lo declare | no secuencia universal, replay y retention garantizados **NOT DOCUMENTED** [S11] |

**Divergencias conservadas:** Market WS `price_change` contiene hash con semántica de book state descrita como hash, pero no hay contrato público de algoritmo/verificación ni continuidad de secuencia; `book` llega al suscribir y tras trades, no equivale a todas las confirmaciones REST de un mismo instante. El spec `connect-wss` parcial no prevalece sobre el AsyncAPI Market más completo. El mercado CLOB expone `itode` y página de mercado aún menciona 250 ms; changelog fechado 2026-08-17 reduce crypto delay a 50 ms: para fecha efectiva prevalece changelog y se retiene contradicción, sin inferir tiempo para otros mercados. [S45][S49][S40b][S32]

## 20. SDKs oficiales y frontera protocolo/conveniencia

| SDK/repositorio oficial | Paquete/versión observada | Cobertura y abstracciones | Frontera verificable |
|---|---|---|---|
| TypeScript unificado [S34][S33] | `@polymarket/client`; changelog menciona **v0.10.0** al 2026-09-17; repo pinned `983a10a7579c95043d4099f60873ff7ea817e5a0` | `PublicClient` y `SecureClient`; Gamma/Data/CLOB/Relayer/positions/combos; signer adapters, auto-credentials, paginadores, conversión de decimales | métodos `fetchOrderBook`, `listMarkets`, `orderIds`, `tradeIds`, timestamps `Date` o epoch-ms normalizados **no son** automáticamente nombres wire REST; constatar JSON source/OpenAPI |
| Python unificado [S36] | `Polymarket/py-sdk`, versión de paquete puntual **NO VERIFICADA** | SDK oficial nuevo multi-surface; guía oficial de inicio y migración | no asumir paridad exacta de toda función TS sin inspección Python específica |
| Rust CLOB v2 [S20c] | `Polymarket/rs-clob-client-v2`; versión crate puntual **NO VERIFICADA** | órdenes/CLOB, firmas, WS según features del repositorio | guía general de SDKs menciona Rust; no usar readme antiguo que apunta a host pre-cutover como contrato vigente |
| TypeScript CLOB v2 anterior [S36b] | `@polymarket/clob-client-v2`; instalación actual en guía histórica CLOB v2, **migración a unificado sugerida en guía más reciente** | CLOB v2 y signer | CLOB v1 package `@polymarket/clob-client` ya no compatible producción desde 2026-04-28 |
| Python CLOB v2 anterior [S36c] | `py-clob-client-v2`; anterior a unificado | CLOB v2 | `py-clob-client` sin `-v2` es legacy v1, no usar en prod v2 [S32a] |
| Go | no SDK Go oficial certificado por esta revisión | — | un repositorio comunitario Go no es autoridad para firmar, schemas ni host |

**Versión vs comodidad del SDK:** `createSecureClient` obtiene/deriva credenciales y despliega Deposit Wallet si corresponde: es **orquestación**, no un endpoint `POST /createSecureClient`. El SDK hace `fetchTradingApprovalsState` con `eth_call` a ERC20/1155 y `setupTradingApprovals` mediante transacciones EOA o batch gasless; no convertir esos nombres en rutas CLOB. `prepareSplitMarketPosition` y merge/redeem seleccionan CTF-era o Router v2 después de resolver mercado/version: esto verifica discriminador funcional en SDK, pero **no** define universalmente conversión NegRisk v2. Los receipts de relayer poseen `transactionID` y polling; `POST /submit` no devuelve hash inmediato desde 2026-04-21. [S34a][S34b][S34c][S33][S32]

**Migraciones de 2026:** CLOB v2 producción 2026-04-28 usa dominio EIP-712 v2 y pUSD; biblioteca v1 y órdenes v1 no admitidas, órdenes abiertas antes del cutover no migraron. Data v2 prod 2026-09-04 usa wrappers `data` y paginación cursor; Data v1 sigue frozen. La guía histórica CLOB v2 aún indica instalar clientes v2 por paquete separado mientras la guía actual SDK Migration pide migrarlos al `@polymarket/client` unificado: ambas son fuentes oficiales con alcance temporal distinto, no equiparar versiones. [S32][S32a][S33][S37]

## 21. Changelog, deprecations, estado operacional

| Clasificación | Hecho y fecha efectiva / limitación | Fuente |
|---|---|---|
| CURRENT | CLOB **v2** en host `clob.polymarket.com` desde **2026-04-28**; Polygon137, pUSD, firma/dominio nuevos | [S32][S32a] |
| DEPRECATED / NO PROD | SDK/órdenes CLOB v1 no funcionan en producción; antiguas órdenes resting descartadas en cutover | [S32][S32a] |
| DEPRECATED | Relayer al viejo NegRisk Adapter `0xd91E...5296` completamente retirado desde **2026-07-17 00:00 UTC**; documentación identifica adapter colateral actual `0xadA2...6EAb` para acciones pUSD | [S32][S25] |
| CURRENT | Data v2 disponible **2026-09-04**, Data v1 frozen; Data v2 transforma wrappers y dinero/tamaño | [S32] |
| RECENTLY CHANGED | FOK/FAK éxito ya no trae necesariamente `transactionHashes` inline desde **2026-07-24**; devuelve `tradeIDs` y hash se recupera leyendo trade/settlement | [S32][S16] |
| RECENTLY CHANGED | `DELETE /orders` máx. **1000** desde 2026-06-15; Manage Orders mantiene ejemplo textual antiguo 3000: prevalece anuncio fechado, contradicción conservada | [S32][S16] |
| RECENTLY CHANGED | `GET /markets/keyset` `limit<=100` desde 2026-05-14 | [S32] |
| RECENTLY CHANGED | crypto taker delay **50 ms** desde 2026-08-17; endpoint market-info conserva texto de 250 ms | [S32][S40b] |
| RECENTLY CHANGED | crypto 5-min TWAP Chainlink **60 s** desde 2026-08-14, corrige regla 30 s introducida 2026-08-07; duración exacta por mercado desde rules | [S32][S12] |
| RECENTLY CHANGED | Data v1 redemption activity por outcome (una fila por cada outcome consumido, incluido perdedor payout0), desde 2026-08-10; no sumar filas como si fueran tx diferentes | [S32] |
| CURRENT | Sports taker coefficient 0.05 y pool maker 15% desde 2026-07-10, fee real siempre consulta por asset/mercado | [S32][S21][S23] |
| CURRENT / WARNING UNCERTAIN | signer token buckets página anuncia warning 2026-07-24 y futura enforcement; no fecha de activación confirmada en texto observado | [S20] |
| BETA | Perps SDK endpoints explícitamente `@experimental` pero Perps está FUERA de scope; no transferir su estado a Predictions | [S34] |

**No atribuir fecha de modificación global a `docs.polymarket.com`**: no se publicó una propiedad global `last changed` en `llms.txt`; el último evento de Predictions Changelog observado en fecha de revisión es **2026-09-04**. Las páginas dinámicas pueden modificarse sin nueva entrada en changelog. Para resolver una contradicción, usar snapshot con timestamp, changelog fechado, spec actual, SDK y, si persiste, declarar ambigüedad; nunca convertir una versión antigua en contrato v2. [S01][S32]

## 22. Seguridad, restricciones y fallos operacionales documentados

- **L1:** clave privada del EOA firma EIP-712 `ClobAuth` (timestamp/nonce) y órdenes si wallet no Deposit. Nunca es enviada al API; timestamp en headers de auth L1, `POLY_ADDRESS`, `POLY_SIGNATURE`, `POLY_NONCE`, `POLY_TIMESTAMP`. No se demuestra que la clave privada de maker proxy/Safe sea la misma que signer autorizado. [S03][S13][S34c]
- **L2:** `apiKey`,`secret`,`passphrase`; cada request autenticado incluye `POLY_ADDRESS`, `POLY_SIGNATURE` HMAC-SHA256, `POLY_TIMESTAMP` y key/passphrase; HMAC cubre método/path/body exactos conforme a API vigente. L2 no firma ni cambia payload EIP-712 Order, sólo autentica transporte. `GET /auth/api-keys` lista, `DELETE /auth/api-key` revoca la credencial actual: rota de forma verificable, no asumir TTL fijo o scopes inventados. [S03][S34c]
- **Builder / Relayer:** credenciales de Builder independientes y cabeceras propias; operaciones wallet gasless requieren su autorización; errores 429/5xx/timeout tras write crean ambigüedad. `POST /submit` devuelve `transactionID`, luego `GET /transaction` y RPC receipt para finalización; `STATE_NEW` no equivale a mined. [S13][S42][S32]
- **Aprobaciones:** ERC20 `approve(spender,amount)` y ERC1155 `setApprovalForAll(operator,true)` son autorizaciones on-chain persistentes, independientes de firma EIP-712 y API keys. La wallet owner/spender efectiva y token deben corresponder exactamente a la ruta CTF/v2; no aprobar contrato por semejanza de nombre. [S25][S34a]
- **Session keys:** no almacenar permisos de sesión como si fueran claves L2; la política está atada a autorización wallet y scope/expiry definidos en Session Keys. EOA/signer/Deposit Wallet pueden tener roles separados. Revocación L2 no implica `setApprovalForAll(false)` ni revocación onchain automática. [S14][S03]
- **Restricciones geográficas:** la operación de trading está sujeta a controles geográficos/jurisdiccionales expuestos por la plataforma; este documento no asume disponibilidad por país, no contiene procedimientos para evitarlos ni certifica elegibilidad de una cuenta. La referencia oficial ofrece **`GET https://polymarket.com/api/geoblock`**, sin credenciales de trading, en el host web `polymarket.com` (NO Gamma ni CLOB); responde `{blocked:boolean, ip:string, country:string, region:string}` sobre la IP solicitante. Una respuesta `blocked:true` implica que una orden nueva de esa procedencia se rechaza; la disponibilidad por wallet/país puede cambiar. Es fallo de elegibilidad, no transient retriable. No intentar eludir la restricción. [S18][S38]
- **Mantenimiento matching:** `425` durante arranque/mantenimiento y `503` en modo cancel-only según referencia Matching Engine Restarts; un restart puede imponer ventana post-only (~2 minutos en fuente), no probar mercado escribiendo repetidamente. Desconexión WS, pérdida de respuesta POST y latencia relayer no son prueba de fallo definitivo ni de éxito: consultar orderID/order hash, trades, relayer transactionID/chain receipt según correlación disponible. [S17][S18][S32]
- **RPC/on-chain:** Polygon gas, mempool/reorg, receipt y ERC1155 balance son superficies distintas del match off-chain. Confirmación WS de fill puede preceder `transactionHash` no nulo y wallet activity; no asignar atomicidad a un conjunto de respuestas HTTP de servicios separados. [S05a][S32]

## 23. Matrices de capabilities, IDs y flows documentales

### 23.1 Capability matrix (R = lectura, W = escritura; *auth* significa nivel de API/chain)

| Capability | Surface; operación exacta / contrato | Auth | Realtime | Histórico | Confianza |
|---|---|---|---|---|---|
| Descubrir events/markets | Gamma `GET /events`,`GET /markets`, slug/ID y keyset | pública | WS `new_market` sólo feature habilitada | Gamma lista state actual, versiones rules no garantizadas | Alta [S39][S45] |
| Metadata/rules/token join | Gamma Event → markets → `conditionId`, `clobTokenIds`; CLOB `GET /book` | pública | algunas flags WS | rules editoriales completas no garantizadas | Alta para IDs, media historización [S04][S06] |
| Book actual | CLOB `GET /book?token_id`, `POST /books` | pública | Market WS `book`,`price_change` | archivo L2 completo **no certificado** | Alta live, baja replay [S07][S45] |
| Best bid/ask, prices | CLOB `/price`,`/midpoint`,`/spread`, WS opt-in `best_bid_ask` | pública | sí parcial | price history D2 | Alta [S07][S45] |
| Público trades | D2 `/v2/trades`, CLOB `/data/trades` | pública / L2 en CLOB | `last_trade_price` sin orderIDs suficientes para reconciliar propios | coverage SLA ausente | Alta rutas [S16a][S41] |
| Fills propios | CLOB `GET /data/trades` con L2, user WS `trade` | L2 | sí | cursor/retención parcial | Alta [S09][S16a] |
| Place/batch | CLOB `POST /order`,`POST /orders` + signed EIP712 | L2 + EIP712 | user WS | órdenes propias por ID, coverage terminal desconocida | Alta en ruta, **no safe blind retry** [S15] |
| Order get/cancel/reconcile | CLOB `/data/order/{id}`, `/data/orders`, DELETE `/order`, `/orders`, `/cancel-all` | L2 | user WS `order`,`trade` | no todos los intents de mercado | Alta [S16][S46] |
| Balances/positions | D2 `GET /v2/positions`, CLOB balance; ERC1155 `balanceOf` | pública para D2, L2 balance, RPC chain | User WS fills, no guarantee balances | D2 positions snapshot | Alta [S05a][S41] |
| Split/merge/redeem | contratos CTF/Router, helpers SDK on-chain; NO endpoint CLOB de split | tx signer / relayer | chain receipts | on-chain logs | Alta CTF y v2 binary donde resolver versión [S34b] |
| NegRisk conversion | CTF adapter histórico vs module/protocol v2 | on-chain | receipt | logs | **Bloqueado para v2, NO LIVE CONVERSION UNTIL ROUTE VERIFIED** [S26][S32] |
| Combos/RFQ | Q REST, QR requester, quoter WS; Exchange v3 | según role, EIP712 v3 | RFQ WS | no replay completo probado | Media; catálogo AsyncRFQ pendiente [S28][S29][S48] |
| Fees | CLOB fee lookup `GET /fee-rate` y CLOB market-info, categories | pública | tick WS, fees no garantía event | changelog parcial | Alta actual [S21][S40a][S40b] |
| Rebates/rewards | programas, CLOB current reward configurations | pública/L2 según ledger | no stream accounting garantizado | score/payout histórico parcial | Alta programa, media historia [S22][S23][S24] |
| Resolution | Gamma + Data `/v2/resolutions` + UMA/chain | pública / RPC | market_resolved WS | registros chain | Media API schema incompleto [S27][S41] |
| Sports | Sports WS oficial | pública | sí | no replay/SLA | Alta feed, baja history [S47] |
| Crypto reference | RTDS Chainlink/TWAP, proveedor upstream definido | pública | sí | cobertura/SLA API no demostrado | Alta topics [S11][S12] |
| Full L2 history | `/orderbook-history` mencionado por error docs, sin schema/cobertura verificadas | desconocida por esa ruta | WS live | **no hay archivo completo certificado** | RESEARCH GAP [S18] |
| Contracts / settlement | Polygon137 CTF, Exchange, Router, Adapter, ERC1155 | RPC público R, signer W | logs/receipts | cadena desde deployment | Alta addresses snapshot, per-route verificar [S25][S34] |

### 23.2 Relationship map con IDs y fronteras

```text
Gamma Event.id, slug
  └─ Market.id, slug, conditionId, outcomes[i], clobTokenIds[i]
       ├─ CLOB GET /book?token_id=clobTokenIds[i]
       │    └─ WS market assets_ids=[clobTokenIds[i]]
       ├─ Signed EIP712 Order.tokenId=clobTokenIds[i]
       │    └─ POST /order → orderID=hash → GET /data/order/{orderID}
       │         └─ tradeIDs → GET /data/trades → trade.id / maker_orders[].order_id
       │              └─ transaction_hash → Polygon receipt → position balance
       └─ conditionId / resolution source → oracle proposal/dispute → payout
           └─ ERC1155 winning position → redeem → wallet pUSD
NegRisk: Event.negRisk → CTF historic NO conversion (adapter) [VERSION GATE]
          vs protocol v2 NegRisk module/Router [CONVERSION ABI NOT VERIFIED]
Combo: legs(positionIds v2) → derived combo condition/position
       → RFQ rfq_id → quote_id → Exchange v3 order hash → fill → combo position
```

**Joins no garantizados:** WS `last_trade_price` es público, no tiene por contrato todos los IDs necesarios para enlace con fill propio; `tradeID` de respuesta order debe consultarse en REST para tx; event id Gamma no se envía como order token; status `resolved` no implica `redeemed`. [S04][S15][S16][S27]

### 23.3 Flows de protocolo (no diseño de cliente)

**Read-only:** `GET G/events` (offset/limit, tags, closed) → escoger `Market` de `event.markets`/`GET G/markets` → extraer `conditionId` y token YES/NO por índice → CLOB `GET /book?token_id=...` snapshot → Market WS subscribe con `assets_ids` → procesar `book` y `price_change`, marcando `last_trade_price` como dato de ejecución y no mutación arbitraria de nivel → tras reconnect nuevo snapshot REST o `book` inicial; no existe resume/sequence o algoritmo completo de gap detect documentado. La transición snapshot REST ↔ WS **no trae token de atomicidad cross-protocol**; no certificar consistencia sin medidas empíricas. [S04][S07][S08][S45]

**Authenticated order:** EOA signer y maker/funder adecuados → L1 EIP712 ClobAuth timestamp/nonce → `POST /auth/api-key` o `GET /auth/derive-api-key` → L2 HMAC → revisar chain ERC20/1155 allowances para la ruta exacta → `GET /book` token/market flags + `GET /fee-rate` → convertir precio y cantidades según §5/7 → firmar `Order` v2 excluyendo DTO expiration → `POST /order` L2 wrapper → respuesta `orderID` y/o `tradeIDs`; User WS `order`/`trade` → `GET /data/order/{id}` y `GET /data/trades` → si FOK/FAK settlement tx hash falta, consultar trade hasta settle o FAILED → `DELETE /order` si existe saldo vivo. Timeout de POST nunca equivale a rechazo probado: estado desconocido hasta reconciliar. [S03][S15][S16][S32][S34c]

**Position:** pUSD ERC20 + allowance de spender correcto → contrato CTF `splitPosition` vía adapter correspondiente o Router `split` v2 → recibo y ERC1155 tokens/positionIDs → CLOB market trades opcionales → completar set `merge` si compatible → tras resolución y payout efectivo `redeem` CTF/Router → recibo y saldo pUSD. `SELL` en CLOB transfiere tokens con Exchange, no es `redeem`. [S05a][S34b]

**NegRisk:** validar version Market y evento `negRisk`/`augmentedNegRisk`; CTF-era NO complementario se transforma por adaptación histórica documentada sólo donde address/ABI y retiro de relayer no afecten; v2 Router/NegRisk module tiene **ruta universal de conversión pendiente**: `NO LIVE CONVERSION UNTIL ROUTE VERIFIED`. Un conjunto económico de otros YES no constituye automáticamente una transacción atómica disponible. [S26][S32][S34b]

## 24. Brechas verificadas y certificación contractual

### A. TRUE PROTOCOL / DOCUMENTATION GAPS

| Pregunta | Docs inspeccionadas; evidencia | Impacto | Verificación adicional |
|---|---|---|---|
| Market WS sequence global, gap detection y ordering guarantee | S45 describe hash y timestamps, no `sequence` ni `resume_from`; tampoco S08 asegura entrega sin gaps | imposible certificar reconstruct determinista solo live stream | experimentos con disconnect/concurrencia + confirmación formal soporte |
| Consistencia atómica REST `/book` vs mensaje WS `book` | S07 y S45 documentan ambas capturas, no barrera común ni snapshot version cross-protocol | race al bootstrap | comparar hash/levels bajo tráfico con captura y soporte |
| Replay/resume y retención User WS, Sports, RTDS | S46,S47,S11 no publican cursor histórico/resume | reconciliación REST/chains necesaria para pérdida WS | leer specs versionadas y experimentar reconnect controlado |
| Matching *price-time priority* en todos los escenarios y nivel exacto de atomicidad order ↔ chain | S17,S15 explican matching off-chain y settle onchain, no garantía formal global entre superficies | no asumir fairness/atomicidad distribuida | revisión contrato exchange y soporte |
| Retención SLA completa orders terminales, L2, rules, fee schedules, score históricos | S18,S41,S32 y corpus no publican SLA end-to-end | replay de mercado incompleto | consulta oficial de data retention, observación histórica |
| Exacto clock skew permitido para cada HMAC/L1, semántica de idempotency-key universal | S03,S15,S18 no definen tolerancia universal ni key idempotente HTTP | timeout write ambiguo | test controlado de stale timestamp/order hash duplicado en entorno autorizado |
| Activación efectiva del signer rate limiter | S20 todavía describe warning desde 2026-07-24 y posterior anuncio no incorporado al texto | no atribuir 429 live al gate sin headers | observar `Poly-RateLimit-Warning`, `Tier`, 429 y anuncio oficial |

**`NOT DOCUMENTED` no significa que el comportamiento no exista**, sólo que el contrato público inspeccionado no lo garantiza. Las preguntas siguientes **no** pueden reclasificarse como protocolo no documentado: tienen fuente oficial existente, pero aún sin extracción suficiente.

### B. UNRESOLVED RESEARCH GAPS — ESTADO: **NO VACÍO**

| ID | Fuente oficial disponible / extracción faltante | Impacto técnico concreto | Gate verificable para cerrarlo |
|---|---|---|---|
| RG-01 | OpenAPI YAML Gamma/CLOB/Relayer/Combo/Bridge + Data legacy, Data v2 JSON [S39][S40][S41][S42][S43][S44][S41a] no descargados/parseados mecánicamente en esta sesión; conteos y comparación operación→catálogo NO MEDIDOS | no certificar totalidad endpoints CURRENT ni input/output de ramas secundarias | obtener raw spec, parsear `paths`, seguridad, servers, operation IDs y diff con §3; documentar/OUT_OF_SCOPE cada operación |
| RG-02 | RFQ AsyncAPI JSON [S48] enlazado en llms pero no extraído íntegramente | no certificar todos los mensajes, su dirección/errores/recovery | parsear `channels`, `operations`, `components.messages`, probar endpoint indexado |
| RG-03 | CLOB `GET /orderbook-history` consta en official Error Codes [S18] pero falta mini-contract y límites históricos | respuesta a “¿existe full L2 archive?” queda parcial | extraer operación de S40, schema, auth, cursor, timestamps, coverage y SLA mediante autoridad |
| RG-04 | Data v2 `GET /v2/resolutions` descrito por changelog, raw field enum y timestamps no extraídos de S41 | DTO exacto de resolution lifecycle incompleto | parsear OpenAPI JSON + ejemplos + leer respuesta de operación real pública |
| RG-05 | NegRisk protocol v2: ABI/ruta exacta convert Positions, asset flow y autorización por versión no comprobados integralmente [S25][S34b] | riesgo de llamada equivocada/fondos en contrato incorrecto | obtener verificación oficial `market.version` → ABI oficial → contract addr → call inputs/outputs y recibo en contexto controlado; hasta entonces `NO LIVE CONVERSION UNTIL ROUTE VERIFIED` |
| RG-06 | Auditoría individual HTTP de TODOS los URLs de registry y GitHub SHA/path por referencia pendiente; se verificó el commit TS principal y archivos base pero no cada source secundario | provenance total no certificada | HEAD/GET con status+title por URL, y para cada permalink SHA/path pedir objeto GitHub específico |
| RG-07 | Exacto significado de `deferExec=true`, discrepancias de objetos webhook/notificaciones y rutas gateway secundarias no cerradas por schema original | no poder construir todo request opt-in sin documentación adicional | comparar Place Orders, OpenAPI completo y SDK tests de casos `true`, enumerar rutas faltantes y respuestas |

**Certificación de hardening:** NO APROBADA como “única referencia implementable sin navegar documentación” bajo los gates solicitados. Sí se documentan contratos críticos verificados, diferencias de versión y bloqueos operativos. **Nunca** afirmar `UNRESOLVED RESEARCH GAPS = NONE` para esta revisión. No se ha ejecutado una orden, conversión NegRisk v2 ni una certificación live; este es un análisis documental. [S01][S32]

Checklist de alcance: fuentes estables en §26 ✓; referencias efímeras excluidas del documento ✓; órdenes signed/DTO/wrapper separados ✓; fee rounding explícito ✓; buckets signer documentados ✓; contradicciones expuestas ✓; raw OpenAPI todos parseados ✗; RFQ AsyncAPI parseado ✗; catálogo de todas las operaciones OpenAPI certificado ✗; NegRisk v2 conversión certificada ✗; todos los URLs individualmente validados ✗; research gaps cero ✗.

## 25. Parámetros dinámicos, paginación y recuperación — consulta por fuente

### 25.1 Dynamic configuration matrix: no transportar snapshots como invariantes

| Setting dinámico | Fuente efectiva CURRENT | Fallback/limitación | Histórico verificable |
|---|---|---|---|
| token, estado, live/closed, reglas | Gamma market/event + CLOB market-info + oracle para resolución | flags de Gamma no sustituyen órdenes/settle | versiones editoriales no garantizadas [S04][S06] |
| tick size y min order size | `GET /book` y/o `GET /tick-size`, `GET /markets/{conditionId}` info campos compactos `mts`,`mos`; WS `tick_size_change` | si falta o contradicción => no firmar precio inventado | histórico completo de tick no garantizado [S07][S40b][S45] |
| fee efectiva y curva/category | `GET /fee-rate?token_id`, CLOB market-info `mbf`,`tbf`,`fd` | no asumir rate de categoría si asset tiene setting propio | cambios changelog incompletos [S21][S40a][S40b] |
| fee rounding | norma oficial redondeo 5 decimales, mínimo 0.00001 USDC, submínimos 0 | redondeo interno intermediarios NOT DOCUMENTED | versión docs/changelog [S21] |
| rewards score / maker config | CLOB current reward config y página program | ausencia de configuración ≠ elegible | historia completa no garantizada [S24] |
| rebate tiers, wVolume/category weights | programa oficial Taker, no proxy fee | fecha y 30d window / snapshot | payout histórico parcial [S22] |
| signer rate limit, tier/burst | buckets S20 + headers `Remaining`,`Reset`,`Tier`; IP S19 | página no confirma activación enforcement al 2026-09-17 | cambios sólo docs/headers [S20][S19] |
| crypto taker delay / market enabled | changelog fechado y market-info `itode`; durante conflicto no adjudicar cifra global a no-crypto | market info prose 250 ms contradice 50 ms changelog Aug17 | changelog [S32][S40b] |
| Chainlink TWAP ventana y source | market resolution rules y official Chainlink page; 5min 60s desde Aug14 | ventana depende tipo de mercado; no global | cambios fechados [S12][S32] |
| CTF/v2/Combo contract addresses | lista oficial contratos + SDK pinned production env + version market | hardcode de pUSD/Router sin verificar chain/version puede romper fondos | contratos y releases [S25][S34] |
| EIP712 domain name/version/verifyingContract | orden tipo + market version + dirección exchange correspondiente | no reutilizar firma v1 ni v3 para v2 | changelog v2 [S15][S32][S34d] |
| session key scope/expiration/revoke | session-key contract/page + estado wallet | no asumir scopes globales | blockchain/logs cuando aplique [S14] |
| API key active / revoked | L2 `GET /auth/api-keys`, DELETE actual | no TTL fijo oficialmente confirmado | registros propios, no archivo público universal [S34c] |

### 25.2 Pagination matrix

| Familia | Modelo actual; campos | Máximo / estabilidad | Contrato NO asumir |
|---|---|---|---|
| Gamma `/events`,`/markets`, series/tags | `limit`,`offset`, filtros, sort según endpoint | endpoint-dependiente; ordering mutable por actualizaciones | no hay snapshot isolation entre páginas [S39] |
| CLOB `GET /markets/keyset` | `after_cursor` → `next_cursor`, `limit` | `limit<=100` desde 2026-05-14 | no usar offset en keyset [S32] |
| CLOB `GET /data/orders`, `/data/trades` | `next_cursor` cursor opaco, `limit`, `data`, `count` según familia | máximo family-specific en referencia; no fijo global | cursor no representa estado chain atómico [S16][S16a] |
| Data v2 `/v2/*` paginados | `data`, `pagination` cursor opaco, query snake_case aliases | endpoint-specific; **offset no soportado**, según changelog | v1 schema, camelCase SDK y `data` raw no se intercambian [S32][S41] |
| Data v1 legacy | `limit`,`offset` según operación | frozen, operación-dependiente | no transferir paginación v1 a v2 [S30][S32] |
| Relayer transaction status | lookup `transactionID`, polling | no cursor universal | orderID no es relayer transactionID [S42][S32] |
| RFQ/Combo | IDs, statuses y paginación por operación publicada | schema completo OpenAPI/RFQ aún RG-01/RG-02 | no asumir paginador Data v2 [S28][S43] |

### 25.3 WS recovery matrix

| Stream | Initial bootstrap | Sequence / gap detection | Replay / resume | REST/chain reconciliation | Reconnect contract |
|---|---|---|---|---|---|
| Market WS | subscription devuelve `book` por asset; snapshot REST `/book` disponible | secuencia ninguna especificada, hash no es contador; ordering garantizado NOT DOCUMENTED | no `resume_from` publicado | REST `/book` por token; actualizar flags/fees market-info | reconectar y resuscribir; snapshot nuevo; consistencia cutover NOT DOCUMENTED [S45][S07] |
| User WS | subscribe L2 a `markets` conditionIDs; eventos futuros | no secuencia global | replay no publicado | CLOB `/data/orders`, `/data/order/{id}`, `/data/trades`, chain receipt | reauth/resubscribe; recuperar estado REST, terminal retention NOT DOCUMENTED [S46][S16] |
| Sports | mensaje `sportsUpdate`, no subscription assets | no secuencia | no resume | datos Sports actuales / Gamma según disponibilidad, sin ledger completo de cada score | WS+PING/PONG: server 5s y timeout 10s; no retransmisión documentada [S47] |
| RTDS | JSON subscribe topics/filtros | no secuencia universal | no replay | feeds upstream si ofrecen historial; no garantía equivalente first-party | reconectar y resuscribir; depender del topic [S11] |
| RFQ | autenticación/suscripción maker role | RG-02 | RG-02 | RFQ REST requester/quotes si operation soporta; exact schema RG-01 | RG-02; NO fabricar cursor de WS [S28][S48] |

### 25.4 Adversarial client-contract acceptance

| Operación | Información utilizable en este documento | Resultado de la prueba documental |
|---|---|---|
| Discover/fetch market | hosts/paths/filter/IDs/fechas §2–3 | contratos principales descritos; inventario total aún RG-01 |
| Book/WS/bootstrap | GET/POST, token, price/size, full-vs-delta §3,5,9,19,25 | live utilizable; gap/replay explícitamente no documentado |
| L1/L2/wallet | dominio, header, HMAC, key CRUD §4,7,11 | principal utilizable; signer key rotation TTL no universal |
| Construct/sign/submit order | signed EIP712 vs DTO vs wrapper, decimal+rounding, GTD §5,7 | principal utilizable; `deferExec=true` RG-07 |
| Retrieve/cancel/order fill | GET order, cursor trades, tradeID→hash, DELETE §3,8,23 | utilizable; eventual timeout no blind retry |
| Positions/split/merge/redeem | CTF vs v2 version dispatch, ABIs básicas y onchain balances §10–11 | rutas básicas utilizable; adapter/amount/protocol validar |
| NegRisk convert | §12 legacy/v2 separados | **BLOQUEADO** hasta RG-05 |
| Effective fees/rewards | §14–15 con matemática y valores verificados | lectura current utilizable, score history no garantizado |
| Resolution/history | §16–17 | lifecycle conceptual verificable; DTO completo v2 RG-04 y L2 historical RG-03 |
| Full API/WS coverage | §§3,19 | **NO CERTIFICADO**, RG-01 y RG-02 |


## 26. SOURCE REGISTRY — IDs persistentes, URLs oficiales y verificación diferenciada

**Timestamp de registro:** 2026-09-17 02:34:53 UTC. `GET confirmado` significa que durante las pasadas de esta investigación se obtuvo una representación HTTP legible de esa URL; `indexado` significa que el URL se recuperó del índice oficial S01 pero no quedó registrado un GET individual de su cuerpo; `raw NO parseado` impide atribuirle conteos de operaciones o cobertura plena. En GitHub, el SHA de la revisión fijada S34–S34d se corroboró por `fetch_commit` con API oficial; algunos paths también por `fetch` individual, otros únicamente dentro de la diff. Este registro deliberadamente **NO falsifica** el control de 67 URL independientes; RG-06 permanece abierto. Links sin sufijo `.md` son forma canónica navegable publicada en el índice S01, con contenido Markdown equivalente indexado.

| ID | Título | URL oficial durable | Tipo | Retrieval / verificación | Secciones respaldadas |
|---|---|---|---|---|---|
| S01 | Documentation Index / llms.txt | `https://docs.polymarket.com/llms.txt` | índice oficial | GET confirmado; 2026-09-17 02:34:53 UTC | corpus, inventario specs y alcance |
| S02 | API: Getting Started | `https://docs.polymarket.com/getting-started/api` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | hosts y overview |
| S03 | Wallets and Authentication | `https://docs.polymarket.com/trading/wallets-auth` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | wallet L1/L2, flujo credenciales |
| S04 | Markets & Events | `https://docs.polymarket.com/concepts/markets-events` | concepto oficial | indexado; 2026-09-17 02:34:53 UTC | Event/Market/identity |
| S05 | Positions & Tokens | `https://docs.polymarket.com/concepts/positions-tokens` | concepto oficial | indexado; 2026-09-17 02:34:53 UTC | condition, ERC1155, redeem |
| S05a | Manage Positions | `https://docs.polymarket.com/trading/positions/manage` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | split/merge/redeem |
| S05c | Combinatorial Positions | `https://docs.polymarket.com/trading/positions/combinatorial` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | legs/combinatorial module |
| S06 | Market Details | `https://docs.polymarket.com/market-data/market-details` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | market IDs/status/tokens |
| S07 | Prices and Order Books | `https://docs.polymarket.com/market-data/prices-order-books` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | book/prices/history |
| S07a | Prices & Orderbook | `https://docs.polymarket.com/concepts/prices-orderbook` | concepto oficial | indexado; 2026-09-17 02:34:53 UTC | precio UI/book semantics |
| S08 | Real-Time Data | `https://docs.polymarket.com/market-data/realtime-data` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | Market WS/recovery/features |
| S09 | Real-Time Order Updates | `https://docs.polymarket.com/trading/realtime-order-updates` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | User WS order/trade |
| S10 | Sports WebSocket / Real-Time Data | `https://docs.polymarket.com/api-reference/wss/sports` | referencia oficial | GET confirmado; schema de mensaje contrastado S47; 2026-09-17 02:34:53 UTC | sports endpoint y stream; fuente auxiliar S47 |
| S11 | Real-Time Data | `https://docs.polymarket.com/market-data/realtime-data` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | RTDS topic/filter/heartbeat |
| S12 | Chainlink TWAP Prices | `https://docs.polymarket.com/market-data/chainlink-twap` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | Chainlink/TWAP source |
| S13 | Wallets and Authentication / Relayer | `https://docs.polymarket.com/trading/wallets-auth` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | account/wallet relayer; complementar S42 |
| S14 | Session Keys | `https://docs.polymarket.com/trading/session-keys` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | session signer scope/revoke |
| S15 | Place Orders | `https://docs.polymarket.com/trading/place-orders` | guía oficial | GET en investigación previa; indexado; 2026-09-17 02:34:53 UTC | EIP712, DTO, submit, precision/rounding/GTD |
| S16 | Manage Orders | `https://docs.polymarket.com/trading/manage-orders` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | order/trade/cancel; contradicción batch |
| S16a | Get trades — CLOB | `https://docs.polymarket.com/api-reference/trade/get-trades` | REST referencia oficial | GET confirmado; 2026-09-17 02:34:53 UTC | wire {data,count,next_cursor,limit} |
| S17 | Matching Engine Restarts | `https://docs.polymarket.com/trading/matching-engine` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | 425/503/post-only restart |
| S18 | Error Codes | `https://docs.polymarket.com/resources/error-codes` | referencia oficial | indexado; 2026-09-17 02:34:53 UTC | HTTP/model, orderbook-history |
| S19 | Rate Limits | `https://docs.polymarket.com/api-reference/rate-limits` | referencia oficial | GET confirmado en auditoría; 2026-09-17 02:34:53 UTC | IP limits, throttle |
| S20 | CLOB Trading Rate Limits | `https://docs.polymarket.com/api-reference/trading-rate-limits` | referencia oficial | GET confirmado; 2026-09-17 02:34:53 UTC | signer token buckets, tiers, headers |
| S20c | Polymarket Rust CLOB client v2 | `https://github.com/Polymarket/rs-clob-client-v2` | repo oficial | repo en organización verificado; versión exacta no verificada; 2026-09-17 02:34:53 UTC | Rust, balance/update; version/SDK |
| S21 | Fees | `https://docs.polymarket.com/trading/fees` | guía oficial | GET confirmado en auditoría; 2026-09-17 02:34:53 UTC | fee formula/rounding/mínimo/category |
| S22 | Taker Rebate Program | `https://docs.polymarket.com/programs/taker-rebates` | programa oficial | GET confirmado en auditoría; 2026-09-17 02:34:53 UTC | 7 tier/threshold/weights/payout |
| S23 | Maker Rebates Program | `https://docs.polymarket.com/programs/maker-rebates` | programa oficial | indexado; 2026-09-17 02:34:53 UTC | pool category/maker payout |
| S24 | Liquidity Rewards | `https://docs.polymarket.com/programs/liquidity-rewards` | programa oficial | indexado; 2026-09-17 02:34:53 UTC | scoring/current config |
| S25 | Contracts | `https://docs.polymarket.com/resources/contracts` | registry oficial | indexado; direcciones contrastadas TS env; 2026-09-17 02:34:53 UTC | direcciones polygon/audits/proxies |
| S26 | Negative Risk Markets | `https://docs.polymarket.com/concepts/negative-risk` | concepto oficial | indexado; 2026-09-17 02:34:53 UTC | NegRisk/augmented/Other/legacy conversion |
| S27 | Resolution | `https://docs.polymarket.com/concepts/resolution` | concepto oficial | indexado; 2026-09-17 02:34:53 UTC | UMA/Oracle/redeem/liveness |
| S28 | Combo Requesters | `https://docs.polymarket.com/trading/combos/requesters` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | RFQ requester, thresholds/IDs |
| S28a | Combos for Builders | `https://docs.polymarket.com/trading/combos/builders` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | builder gateway |
| S28b | Collateral Return | `https://docs.polymarket.com/trading/combos/collateral-return` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | combo collateral return |
| S29 | How Combos Work | `https://docs.polymarket.com/trading/combos/overview` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | RFQ and combinatorial definitions |
| S30 | Data API v2 release — Predictions Changelog | `https://docs.polymarket.com/changelog/predictions` | changelog oficial | GET confirmado; 2026-09-17 02:34:53 UTC | v1 frozen, D2 cursor/wrapper/host |
| S31 | Public Analytics | `https://docs.polymarket.com/market-data/public-analytics` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | trades/price history/analytics |
| S32 | Predictions Changelog | `https://docs.polymarket.com/changelog/predictions` | changelog oficial | GET confirmado; 2026-09-17 02:34:53 UTC | todos hitos 2026/contradicciones |
| S32a | Migrating to CLOB V2 | `https://docs.polymarket.com/v2-migration` | migration guide oficial | GET confirmado por búsqueda; 2026-09-17 02:34:53 UTC | v1/v2 orders/SDK migration |
| S33 | SDK Changelog | `https://docs.polymarket.com/changelog/sdks` | changelog oficial | GET confirmado; 2026-09-17 02:34:53 UTC | SDK versions/data wrappers/migrations |
| S34 | ts-sdk environments.ts — commit pinned | `https://github.com/Polymarket/ts-sdk/blob/983a10a7579c95043d4099f60873ff7ea817e5a0/packages/client/src/environments.ts` | SDK oficial, permalink SHA | commit y path GET confirmados; 2026-09-17 02:34:53 UTC | host, chain, addresses |
| S34a | ts-sdk approvals.ts — commit pinned | `https://github.com/Polymarket/ts-sdk/blob/983a10a7579c95043d4099f60873ff7ea817e5a0/packages/client/src/actions/approvals.ts` | SDK oficial, permalink SHA | path GET confirmado; 2026-09-17 02:34:53 UTC | ERC20/1155 approval workflows |
| S34b | ts-sdk positions.ts — commit pinned | `https://github.com/Polymarket/ts-sdk/blob/983a10a7579c95043d4099f60873ff7ea817e5a0/packages/client/src/actions/positions.ts` | SDK oficial, permalink SHA | path GET confirmado; 2026-09-17 02:34:53 UTC | CTF vs Router v2 split/merge/redeem |
| S34c | ts-sdk auth.ts — commit pinned | `https://github.com/Polymarket/ts-sdk/blob/983a10a7579c95043d4099f60873ff7ea817e5a0/packages/client/src/actions/auth.ts` | SDK oficial, permalink SHA | path GET confirmado; 2026-09-17 02:34:53 UTC | exact API credential CRUD/headers |
| S34d | ts-sdk typed-data tests — commit pinned | `https://github.com/Polymarket/ts-sdk/blob/983a10a7579c95043d4099f60873ff7ea817e5a0/packages/client/src/actions/orders/typed-data.test.ts` | SDK oficial, permalink SHA | path en diff de commit; independiente GET no confirmado; 2026-09-17 02:34:53 UTC | deposit signed typed data/domain |
| S35 | Builder Fees | `https://docs.polymarket.com/programs/builders/fees` | programa oficial | indexado; 2026-09-17 02:34:53 UTC | attribution/additional maker/taker builder fees |
| S36 | Official Python unified SDK | `https://github.com/Polymarket/py-sdk` | repo oficial | repo en organización confirmado; 2026-09-17 02:34:53 UTC | unified python sdk |
| S36a | Legacy Python CLOB client | `https://github.com/Polymarket/py-clob-client` | repo oficial, legacy | repo en organización confirmado; 2026-09-17 02:34:53 UTC | legacy notifications/examples, NO protocolo v2 |
| S36b | Previous TypeScript CLOB V2 client | `https://github.com/Polymarket/clob-client-v2` | repo oficial | repo en organización confirmado; 2026-09-17 02:34:53 UTC | former sdk and migration boundary |
| S36c | Previous Python CLOB V2 client | `https://github.com/Polymarket/py-clob-client-v2` | repo oficial | repo en organización confirmado; 2026-09-17 02:34:53 UTC | former sdk and migration boundary |
| S37 | SDK Migration to Unified SDK | `https://docs.polymarket.com/getting-started/migrate-from-previous-sdks` | guía oficial | GET confirmado; 2026-09-17 02:34:53 UTC | unified, old SDK replacement |
| S38 | Geographic Restrictions | `https://docs.polymarket.com/api-reference/geoblock` | referencia oficial | GET por search verificado; 2026-09-17 02:34:53 UTC | compliance; GET polymarket.com/api/geoblock |
| S39 | Gamma OpenAPI YAML | `https://docs.polymarket.com/api-spec/gamma-openapi.yaml` | OpenAPI oficial | URL en S01; raw NO parseado; 2026-09-17 02:34:53 UTC | Gamma path matrix; RG-01 |
| S40 | CLOB OpenAPI YAML | `https://docs.polymarket.com/api-spec/clob-openapi.yaml` | OpenAPI oficial | URL en S01; raw NO parseado; 2026-09-17 02:34:53 UTC | CLOB REST; RG-01 |
| S40a | Get fee rate | `https://docs.polymarket.com/api-reference/market-data/get-fee-rate` | REST referencia oficial | GET en auditoría previa; 2026-09-17 02:34:53 UTC | fee base bps by token |
| S40b | Get CLOB market info | `https://docs.polymarket.com/api-reference/markets/get-clob-market-info` | REST referencia oficial | GET confirmado en auditoría; 2026-09-17 02:34:53 UTC | market trading flags/fee curve/taker delay contradiction |
| S41 | Data API v2 OpenAPI | `https://data-api.polymarket.com/v2/openapi.json` | OpenAPI oficial | URL correcto S01; raw NO parseado; 2026-09-17 02:34:53 UTC | D2 endpoints/wire/RG-01,RG-04 |
| S41a | Legacy Data API OpenAPI YAML | `https://docs.polymarket.com/api-spec/data-openapi.yaml` | OpenAPI oficial | URL en S01; raw NO parseado; 2026-09-17 02:34:53 UTC | Data v1/out-of-scope except migration |
| S42 | Relayer OpenAPI YAML | `https://docs.polymarket.com/api-spec/relayer-openapi.yaml` | OpenAPI oficial | URL en S01; raw NO parseado; 2026-09-17 02:34:53 UTC | relayer methods/transactions |
| S43 | Combo RFQ OpenAPI YAML | `https://docs.polymarket.com/api-spec/combos-rfq-openapi.yaml` | OpenAPI oficial | URL en S01; raw NO parseado; 2026-09-17 02:34:53 UTC | RFQ REST/maker vs requester |
| S44 | Bridge OpenAPI YAML | `https://docs.polymarket.com/api-spec/bridge-openapi.yaml` | OpenAPI oficial | URL en S01; raw NO parseado; 2026-09-17 02:34:53 UTC | funding/withdrawal only |
| S45 | Market AsyncAPI JSON | `https://docs.polymarket.com/asyncapi.json` | AsyncAPI 3.0.0 v1.0.0 | GET JSON confirmado; enumerado; 2026-09-17 02:34:53 UTC | market channel/11 ops/messages |
| S46 | User AsyncAPI JSON | `https://docs.polymarket.com/asyncapi-user.json` | AsyncAPI 3.0.0 v1.0.0 | GET JSON confirmado; enumerado; 2026-09-17 02:34:53 UTC | user channel/6 ops/messages |
| S47 | Sports AsyncAPI JSON | `https://docs.polymarket.com/asyncapi-sports.json` | AsyncAPI 3.0.0 v1.0.0 | GET JSON en auditoría previa; 2026-09-17 02:34:53 UTC | sports channel/3 ops/messages |
| S48 | RFQ AsyncAPI JSON | `https://docs.polymarket.com/asyncapi-rfq.json` | AsyncAPI oficial | indexado S01; body NO extraído; 2026-09-17 02:34:53 UTC | RFQ WS; RG-02 |
| S49 | connect-wss legacy/subset AsyncAPI | `https://docs.polymarket.com/developers/open-api/connect-wss.json` | AsyncAPI oficial listado | indexado; variante parcial observada; 2026-09-17 02:34:53 UTC | documentary mismatch vs market asyncapi |

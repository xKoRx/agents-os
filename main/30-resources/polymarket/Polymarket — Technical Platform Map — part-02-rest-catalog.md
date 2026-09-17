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


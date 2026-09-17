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


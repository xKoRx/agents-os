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


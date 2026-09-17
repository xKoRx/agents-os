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

**API:** datos actuales Gamma (`conditionId`, `resolved`, `closed`, `endDate`, `resolutionSource`, `outcomePrices`, `umaResolutionStatus` donde exista), `GET D2 /v2/resolutions` para lifecycle agregado y lectura on-chain UMA/CTF para payout final; Data v2 y SDK exponen posición `REDEEMABLE`. La presencia de `outcomePrices=[1,0]` en un JSON de mercado NO es un recibo de redemption. Joins: `conditionId` market → resolution record/condition, posición `(wallet,asset/positionId)` → payout, tx receipt/hash → saldo final. El contrato raw de `GET /v2/resolutions`, sus enums, filtros, timestamps y respuesta está expandido directamente desde OpenAPI en §3.4.1. El SDK oficial normaliza a camelCase, convierte sentinelas y fechas [S41][S34f]; ninguno de sus getters reemplaza la confirmación de payout o redemption en cadena. [S27][S41][S33]

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

**Respuesta precisa sobre archivo L2:** no se verificó un **archivo first-party público, completo y con SLA** de snapshots **y** deltas L2 que permita replay determinista. Pero NO afirmar categóricamente que «no existe histórico de books»: el Error Codes oficial contiene `GET /orderbook-history`, que NO está inventariado en OpenAPI S40; su semántica, cobertura y retención son **NOT DOCUMENTED** y no deben asumirse; existen snapshots REST actuales. Las observaciones L2 que no aparecen en price history/trades ni en un archivo L2 exhaustivo son **irreconstruibles desde esas APIs**. Para resolver gaps WS no existe `resume_from_sequence` publicado en Market AsyncAPI. [S18][S08][S45][S41]

**RG-03 verificación 2026-09-17 14:48 UTC:** El OpenAPI CLOB raw [S40] **NO incluye** `GET /orderbook-history` en su mapa de `paths` (54 paths). La página de errores [S18] lo menciona, pero esto no define request/response, orden, retención o completitud. Pruebas GET públicas sin credenciales, cuerpo máximo 3 KB: HTTP 400 para `CLOB/orderbook-history?startTs=1700000000&limit=1` → `{"error":"either market or asset_id must be provided"}`; HTTP 200 para `CLOB/orderbook-history?asset_id=98022490269692409998126496127597032490334070080325855126491859374983463996227&startTs=1789600000&limit=1` → `{"count":5740599,"data":[{"market":"0x1fad72fae204143ff1c3035e99e7c0f65ea8d5cd9bd1070987bd1a3316f772be","asset_id":"98022490269692409998126496127597032490334070080325855126491859374983463996227","timestamp":"1762984370871","hash":"9e7ac2c2306868d557dd0b4a0e421b6f14024ce1","bids":[{"price":"0.01","size":"1110000"},{"price":"0.02","size":"60005.12"},`. **Conclusión documental:** no existe aquí un contrato certificable de archivo L2 íntegro y ordenado, ni una promesa de replay; `prices-history` y trades son datasets distintos. Capability de backfill L2 por este endpoint = `DISABLED/NOT DOCUMENTED`; para replay propio debe capturarse evidencia `book`/`price_change` y reconcilaciones en tiempo de observación. No afirmar que el endpoint nunca existió ni que se comprobó retención completa. [S18][S40][S45]

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


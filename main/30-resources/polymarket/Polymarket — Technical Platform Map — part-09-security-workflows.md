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


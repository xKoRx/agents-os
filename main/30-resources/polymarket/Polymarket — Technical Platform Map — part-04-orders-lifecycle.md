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


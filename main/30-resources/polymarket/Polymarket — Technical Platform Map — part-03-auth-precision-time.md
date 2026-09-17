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


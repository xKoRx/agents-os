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
| RG-01 | PARTIAL 2026-09-17 14:48 UTC: 7/7 OpenAPI raw recuperados y parseados, 163 operaciones; comparación literal en §19.1 y schemas Data críticos §3.4.1; 0 rutas Data no coinciden literal. | inventario mecánico cerrado, falta triage de operaciones CLOB/Gamma/Relayer clasificadas ambiguas y expansión de DTOs trading críticos | confirmar discrepancias, schema/seguridad y excluir secundarias con razón antes de marcar PASS |
| RG-02 | CLOSED M0 2026-09-17 14:48 UTC: RFQ AsyncAPI descargado HTTP 200 y parseado: 1 canales, 13 operaciones, 13 mensajes; contratos en §19.3 | Combo/RFQ condicionado, OUT_OF_SCOPE MVP inicial; no prometer routing/recovery end-to-end | reabrir sólo al incorporar Combo/RFQ con gateway requester y exchange-v3 cert |
| RG-03 | CLOSED M0 2026-09-17 14:48 UTC: raw CLOB S40 NO enumera la ruta `/orderbook-history`; GET públicos 400,200; schema/SLA/ordering no publicados; respuesta en §17 | histórico L2 completo NO certificado, backfill L2 DISABLED; recorder propio obligatorio como dato de diseño | sólo reabrir ante especificación oficial completa o certificación empírica del archivo; no inferir replay |
| RG-04 | CLOSED M0 2026-09-17 14:48 UTC: `GET /v2/resolutions` OpenAPI raw request+response+enums/timestamps expandido en §3.4.1, API vs SDK separadas en §16 | resolution lifecycle diseñable sin equiparar end/proposal/resolved/redeemed; chain payout autoridad final | revisar changes de spec por fecha; pruebas públicas read-only según parámetros reales |
| RG-05 | NegRisk protocol v2: ABI/ruta exacta convert Positions, asset flow y autorización por versión no comprobados integralmente [S25][S34b] | riesgo de llamada equivocada/fondos en contrato incorrecto | obtener verificación oficial `market.version` → ABI oficial → contract addr → call inputs/outputs y recibo en contexto controlado; hasta entonces `NO LIVE CONVERSION UNTIL ROUTE VERIFIED` |
| RG-06 | Auditoría individual HTTP de TODOS los URLs de registry y GitHub SHA/path por referencia pendiente; se verificó el commit TS principal y archivos base pero no cada source secundario | provenance total no certificada | HEAD/GET con status+title por URL, y para cada permalink SHA/path pedir objeto GitHub específico |
| RG-07 | PARTIAL 2026-09-17 14:48 UTC: CLOB S40 confirma PUT y GET cache balance/allowance, SDK pinned fuerza `deferExec=false`; TRUE no documentado y DISABLED, Builder CRUD mismatch auth identificado | modo normal `false` puede diseñarse; Builder auth alternativo prohibido hasta resolver conflicto; notificaciones OUT_OF_SCOPE | verificar Builder auth/relayer variantes si quedan mandatory, de otro modo cerrar scoped exclusion |

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



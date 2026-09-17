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

**`NOT DOCUMENTED` no significa que el comportamiento no exista**, sólo que el contrato público inspeccionado no lo garantiza. Los RG que siguen conservan su identidad y evidencia histórica. Su estado vigente por fila distingue cierre para diseño de habilitación live; las ausencias genuinas del protocolo permanecen en la tabla A y no se convierten artificialmente en certezas.

### B. Research Gaps RG-01…RG-07 — CLOSED FOR M0 DESIGN; live and optional gates tracked separately

| ID | Fuente oficial disponible / extracción faltante | Impacto técnico concreto | Gate verificable para cerrarlo |
|---|---|---|---|
| RG-01 | CLOSED INVENTORY / DESIGN CONTRACTS 2026-09-17: 7/7 official raw OpenAPI, 163 operations; 42 Gamma + 66 CLOB + 20 Data-v2 + 19 Data-legacy + 7 Relayer + 4 RFQ + 5 Bridge. Every formerly MISSING Gamma/CLOB/Relayer operation triaged in §19.1; Data exact 20/20; critical wire objects expanded in §19.1.1 and Data §3.4.1. | Engine MVP routes available; legacy/social/Bridge/Combo and optional analytics excluded with reasons. SDK-vs-S40 L1/L2 auth contradiction retained, live auth requires later integration proof, not invented contract. | schema names absent from components: none; verification of capability matrix and security gate still required |
| RG-02 | CLOSED M0 2026-09-17 14:48 UTC: RFQ AsyncAPI descargado HTTP 200 y parseado: 1 canales, 13 operaciones, 13 mensajes; contratos en §19.3 | Combo/RFQ condicionado, OUT_OF_SCOPE MVP inicial; no prometer routing/recovery end-to-end | reabrir sólo al incorporar Combo/RFQ con gateway requester y exchange-v3 cert |
| RG-03 | CLOSED M0 2026-09-17 14:48 UTC: raw CLOB S40 NO enumera la ruta `/orderbook-history`; GET públicos 400,200; schema/SLA/ordering no publicados; respuesta en §17 | histórico L2 completo NO certificado, backfill L2 DISABLED; recorder propio obligatorio como dato de diseño | sólo reabrir ante especificación oficial completa o certificación empírica del archivo; no inferir replay |
| RG-04 | CLOSED M0 2026-09-17 14:48 UTC: `GET /v2/resolutions` OpenAPI raw request+response+enums/timestamps expandido en §3.4.1, API vs SDK separadas en §16 | resolution lifecycle diseñable sin equiparar end/proposal/resolved/redeemed; chain payout autoridad final | revisar changes de spec por fecha; pruebas públicas read-only según parámetros reales |
| RG-05 | CLOSED FOR DESIGN / LIVE BLOCKED 2026-09-17: legacy CTF `convertPositions` [S50], pUSD CTF adapter ABI/asset flow [S51], production addr + version and outcome dispatch [S34][S34b][S34g] verified; v2 module addr known, conversion ABI/selector not published/verified | Astra can design versioned CTF/v2 routing with v2 conversion disabled; neither CTF conversion nor v2 conversion is certified live, `NO LIVE CONVERSION UNTIL ROUTE VERIFIED` | enabling live requires official v2 ABI and protocol tests, on-chain runtime/approval check, version/event ID proof, receipt+balance validation; no real transactions in M0 |
| RG-06 | CLOSED MATERIAL 2026-09-17 14:59 UTC: 72 source IDs / 69 distinct URLs individually requested; 71 HTTP200 readable, 1 failures; detailed statuses+titles+SHA §26.1; critical failures none | source provenance verified for critical MVP sources; secondary broken URLs classified in §26.1 | re-audit dynamic versions after change; noncritical links still require repair |
| RG-07 | CLOSED FOR DESIGN / OPTIONAL MODES DISABLED 2026-09-17: `deferExec=false` SDK pinned, true disabled; CLOB PUT/GET balance-allowance schemas, GET/books, NegRisk path alias, rewards market endpoint, v1 heartbeats, Relayer credential endpoint triaged §19.1.1; Builder CRUD/alt auth explicitly disabled. | mandatory single-order, L2 balance and cancellations have documented contracts, opt-in modes withheld; no assumption heartbeats imply order cancellation. | reopen only if Builder or deferExec=true promoted to required scope; never use production credentials in research |

**Certificación M0 — DESIGN_READY: PASS (documental, 2026-09-17).** Los siete RG han sido cerrados para las decisiones arquitectónicas del Engine MVP, con exclusiones o rutas fail-closed explícitas: RG-01 7/7 OpenAPI y 163 operaciones inventariadas/triadas; RG-02 RFQ AsyncAPI 13 operaciones/13 mensajes y RFQ fuera del MVP inicial; RG-03 no existe un contrato verificable de archivo L2 completo, por lo que backfill L2 queda DISABLED y el recorder propio es obligatorio; RG-04 DTOs Data v2 de resoluciones/posiciones/trades/actividad extraídos; RG-05 CTF pUSD adapter documentado en Solidity oficial pero conversión CTF/v2 live DISABLED y ABI de conversión v2 no verificada; RG-06 72 IDs/69 URLs consultados, 71 respuestas legibles y un fallo secundario S37 por límite de descarga, sin fuente crítica fallida; RG-07 modos opcionales `deferExec=true` y Builder no certificados, DISABLED. Esto certifica suficiencia del conocimiento para **diseñar**, NO cliente Go implementado, integración, verificación de bytecode desplegado, ejecución live, rentabilidad ni certificación integral de toda la plataforma. [S39][S40][S41][S48][S50][S51]

**Gates separados:** `M0_DESIGN_READY=PASS`; `FULL_PLATFORM_CONTRACT_CERTIFIED=NO`; `ENGINE_IMPLEMENTED=NO`; `LIVE_EXECUTION_CERTIFIED=NO`; `NEGRISK_CTF_LIVE=DISABLED`; `NEGRISK_V2_LIVE=DISABLED`; `L2_HISTORICAL_BACKFILL=DISABLED`; `RFQ_COMBOS=OUT_OF_SCOPE_MVP`; `DEFER_EXEC_TRUE=DISABLED`; `BUILDER_OPTIONAL_MODES=DISABLED`. Live order/auth exige integración y reconciliación comprobadas en fases posteriores: discrepancias SDK-vs-OpenAPI no son licencia para inventar headers. [S34][S40]

**Checklist M0:** OpenAPI 7/7 y 163 operaciones ✓; AsyncAPI RFQ 13/13 ✓; operaciones MVP triadas y schemas críticos ✓; resolution DTO ✓; histórico L2 no garantizado y backfill bloqueado ✓; discriminación CTF/v2 documentada y conversión live bloqueada ✓; provenance crítica verificada, S37 no crítico pendiente de retrieval completo ✓; `RG pendientes que impiden arquitectura = 0` ✓. `FULL PLATFORM CONTRACT CERTIFICATION` sigue pendiente y no es condición de M0.

### C. Matriz de aceptación Astra/Fable — sólo diseño

| Capacidad | Estado del knowledge pack | Boundary obligatorio para M1 |
|---|---|---|
| Event/Market/Token/Condition, discovery, Sports | DESIGN_READY: §§2–3,19; schemas oficiales inventariados | no equiparar Gamma ID, condition ID y token ID; tomar valores dinámicos por mercado |
| CLOB REST, books, Market/User WS | DESIGN_READY: §§3,8–9,19,25 | sin secuencia/replay garantizados: snapshot, staleness, read-only fail-closed y reconciliación |
| Recorder, histórico y replay | DESIGN_READY: §§17,24–25 | captura propia desde el inicio; NO asumir archivo histórico L2 determinista |
| Auth L1/L2, firmas, órdenes, fills y cancels | DESIGN_READY documental: §§3–8,19,23–25 | designar integración/contract tests obligatorios para discrepancias SDK-vs-spec; live deshabilitado hasta validación |
| Positions/CTF, protocol-v2 y resolution Data v2 | DESIGN_READY: §§3,10–12,16,19 | version dispatch explícito, cadena como autoridad de settlement; no equiparar timestamps ni positions |
| NegRisk conversion | DESIGN_READY como capacidad versionada con live DISABLED: §12, RG-05 | CTF fuente Solidity verificada, deployment/approvals no; v2 ABI desconocida: prohibido ejecutar o inventar contrato |
| Fees, rewards, limits, incentives | DESIGN_READY: §§14–15,18,25 | parámetros/versiones efectivas dinámicas; no hardcodear snapshot 2026-09-17 |
| RFQ/Combos, deferExec=true, Builder | OUT_OF_SCOPE / DISABLED inicial: RG-02/07 | promover sólo mediante contrato adicional, sin contaminar core actual |

**Handoff M1:** Astra y Fable reciben el proyecto raíz, índice y sus once partes como corpus de protocolo, y Edge Research Consolidado. ASTRA diseña boundaries, modelo, recorder/replay, recovery, strategy runtime y gates; FABLE cuestiona. El owner revisa antes de congelar. `M0_DESIGN_READY` NO significa `M1_DESIGN_FROZEN`.

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



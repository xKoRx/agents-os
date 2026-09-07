---
type: resource
schema_version: 1
status: active
area: "[[Echo]]"
sources: ["[[Echo — Fuentes de arquitectura y producto 2026-09-06]]", "[[Echo Forge — Fuentes de arquitectura y producto 2026-09-06]]", "[[Echo + Echo Forge — Evidencia de revisión independiente 2026-09-06]]"]
last_verified: "2026-09-07"
confidence: high
aliases: []
tags:
  - kind/resource
created: "2026-09-07"
updated: "2026-09-07"
---

# Echo + Echo Forge — Architecture Durability and Contract Review — Fable 5.1

> [!info] Precisión de implementación — 2026-09-07
> [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]] mantiene B/C1–C7 y ningún TOP, y concreta Echo SDK como autoridad. Su §16 verifica que Campaign/unique registry protegen namespaces/replay pero no prueban unicidad de dos Builders intra-wave; no retirar discriminador host antes de ese gate. Se corrige cualquier lectura de «ruta Campaign inerte» como prueba suficiente para eliminar sufijos: el path de publicación aún puede agregarlos.

> [!info] Freeze del contrato SDK — 2026-09-07
> [[Echo SDK — Canonical Contract Final Freeze Review — Fable 5.1]] cierra la cadena: B/C-1…C-7 de esta revisión intactas; el contrato Echo SDK queda en B con FR-1…FR-5 (identidad por inputs, taxonomía métrica, Scope sin `valuation`, wire agnóstico de schema, revisión de registro) y ningún TOP.

## Síntesis vigente

Revisión arquitectónica independiente (Cursor, Claude Fable 5.1, effort high) del V1 simplificado de Echo + Echo Forge y del contrato [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] (Astra). Pregunta única: ¿el conjunto forma una arquitectura que conviene **congelar y construir** sin trampa estructural que obligue a reescribir identidad, ledger económico, journal, protocolo Forge↔Echo, EAs o atribución histórica poco después de terminar el producto? Sin estimaciones de plazo, sin análisis de performance, sin nueva auditoría de producto, read-only fuera del vault.

Disposición por clases (autoridad de lectura de este documento):

- **RATIFIED**: todo lo no listado abajo como corregido/decisión/diferido — grafo de identidad, StrategyVersion, magic, PromotionRecord, ingestión individual, propiedad de artefactos, `reference_bindings`, Reference authority, modelo de tiempo, `economic_commands`, PortfolioVersion como agregado único, cadena acíclica.
- **CORRECTED** (correcciones acotadas, ninguna es TOP): C-1 `CanonicalStrategyID` debe ser función pura sin `HOST_KEY`; C-2 FINAL CLOSE es aserción de cierre, la economía sale de deals; C-3 coverage con evidencia positiva del collector y tabla hermana, sin hook en el EA exportado; C-4 reconciliación UNKNOWN exige campo de correlación visible en broker o política explícita de ambigüedad; C-5 reserva de riesgo como estado del comando, no entidad nueva; C-6 `trade_routing` una fila por evento/operación, EXPECTED derivado de comandos; C-7 O1–O3 pasan de bloqueo owner a default técnico.
- **OWNER DECISION**: sólo el catálogo `CC` de instrumentos del esquema `YYMMCCQQQQ` (ratificación de una lista corta; no bloquea registry/unicidad).
- **TARGETED TOP**: ninguno sobrevivió a la revisión.
- **DEFERRED**: `strategy_identity_aliases` hasta que la recuperación histórica lo necesite; netting; hook de salud en el EA exportado; escisión selección/asignación de PortfolioVersion; MT4 int64/varlen.
- **LEAVE UGLY**: §12, veinte ítems fuera del camino crítico.

**Decisión final: B — FREEZE AFTER BOUNDED CORRECTIONS.**

## Autoridad, corte y reglas de lectura

**S** = source inspeccionado en esta sesión (Symphony HEAD/master `db8a022703082fd7ee9d1e15243c5d1b2feaf578`; Echo HEAD local `e25165ba2e57a86b7cdcbd78d44406f66fc9ba23`, master remoto `04c16bd` no releído). **P** = evidencia física fechada de [[Echo + Echo Forge — Evidencia de revisión independiente 2026-09-06]], no recertificada. **D** = decisión owner/frozen. **I** = propuesta (Astra o esta revisión). **U** = no demostrado. Nada I se promueve a D por publicar este documento. Prioridad: source → P → D → Resources → historia → inferencia.

Checkpoint verificado en source: NORMAL A cerrado; B1A `185825c` (ownership global ETCD CAS en `sqx/adapters/mt5/global_ownership.go`), B1B `ef65dd1` (`MaximumAttempts: 0`, sin límites wall-clock), B2 `db8a022` (`OpenAttempt`, jobs preservados entre attempts) — **S, coinciden con lo reportado**. Finalist V2 C1/C2: **no implementado**; policy vigente `finalist_promotion@1.0.0`, output `sqx-finalist-promotion-output.v1`, modo TOP_PROJECTION, `promotionFinalists` copia `TopProjection.Entries` — **S**. SQX long-running D pendiente. Temporal: `sqx/go.mod` declara v1.35.0, workspace resuelve v1.44.1 — S, ya documentado. El source no avanzó respecto al checkpoint de Astra.

### 1. Executive verdict

1. **Entendimiento**: sí. Forge fabrica y admite estrategias con evidencia reproducible; Echo observa la Reference como verdad, copia a Execution bajo mandato y evalúa calidad/fidelidad sobre hechos crudos. El producto es trading real del owner, no plataforma.
2. **¿V1 fundamentalmente sano?** Sí. El grafo identidad→versión→magic→binding→hecho→comando es acíclico, cada concepto tiene un solo escritor y las seams de evolución (plataforma en versión, cuenta/broker en binding, deals como economía irreducible, versión de policy/algoritmo/fórmula) ya existen.
3. **¿Congelar?** Sí, tras siete correcciones acotadas que caben dentro de las slices ya propuestas.
4. **Defecto material más importante**: ninguno bloqueante en el diseño. En source, `CanonicalStrategyID` lee `HOST_KEY` (S) — nondeterminismo latente de identidad, hoy inerte en la ruta Campaign; corregir antes de sellar versiones.
5. **Sobreingeniería más importante**: reserva de riesgo como entidad separada, `trade_routing` por destinatario con CAS y hook de salud en el EA exportado para coverage.
6. **Subespecificación más importante**: cómo se correlaciona un deal del broker con un `command_id` tras crash, dado que el comment MT5 no es confiable para transportar el UUID.
7. **Decisión más cara de cambiar después**: el sello de StrategyVersion y la identidad de hechos crudos (origin position key + deals); todo lo histórico cuelga de ellos.
8. **Recomendación**: B — congelar con correcciones acotadas; NEXT EXACT sin esperar ratificación de O1/O3.

### 2. Product thesis

- **Echo Forge** (Symphony `sqx`) genera estrategias con SQX (Builder→robusto→WFM→Apply→export MT5→backtest físico→reconcile→score→rank), decide `FINALIST_PROMOTION` con evidencia sellada, aloja identidad canónica (GeneratedStrategy V2, `canonical_strategy_id`, `StrategyRef`), y — por D — es autoridad del `magic`. Es fábrica y admisor; no opera dinero.
- **Echo** recibe Finalistas promovidos (ingestión con recibo), enrola la versión ejecutable en una cuenta Reference DEMO, observa hechos crudos de esa cuenta como verdad, enruta comandos económicos a cuentas Execution bajo policies, mantiene journal/analytics (Lab), y evoluciona hacia PortfolioVersion + apply + riesgo.
- **Producto integrado**: cadena reproducible desde estrategia generada hasta operaciones reales en tens de cuentas MT5 de brokers/prop firms, con Strategy Quality (Reference forward vs baseline) y Execution Fidelity (Execution vs Reference bajo policy) computables desde hechos crudos con atribución por versión.
- **Fuera de V1**: netting, MT4 nuevo, batch ingestion, provisioning automático, multi-tenant, futuros, ML/optimizador avanzado, event sourcing genérico, UI amplia, backfill histórico completo.

Reconstrucción propia (TRACK A): Strategy = linaje lógico nacido una vez en Builder; Finalist = miembro estructural de una Decision de promoción; Reference = observación canónica en cuenta designada; Execution = réplica bajo mandato; Strategy Quality ≠ Execution Fidelity ≠ Forge SQX↔MT5 Fidelity; Ingestion ≠ Provisioning ≠ Activation ≠ Capital allocation. **No hay discrepancia semántica con la tesis existente**; ningún track se detuvo.

### 3. Astra contract review

| Propuesta Astra | Evidencia | Veredicto | Razón material | Corrección mínima |
|---|---|---|---|---|
| StrategyVersion content-addressed (canonical + plataforma + digest ejecutable + inputs efectivos + contexto runtime + dependencias), sellado post-compile | S: no existe en domain; `DurableArtifactRef` = store+bucket+key+size+sha256; inputs observados excluidos de `scope_digest` | CONFIRM | Frontera correcta: bytes distintos → versión distinta; reubicación/broker no cambian versión; `target_platform` es la seam MT4/MT5/futuro | Dependencias V1 = manifiesto explícito vacío para EA SQX autocontenido |
| Strategy / StrategyVersion / ReferenceBinding separados | D identidad V2; S sin binding en Echo | CONFIRM | Tres ciclos de vida distintos | Ninguna |
| Magic pertenece a Strategy, int64, Forge-owned, nunca reciclado; no es autoridad de versión | D owner 24-08; S: `MagicNumber *int64` requerido en TaskSpec, Java fallback `888111`, sin registry | CONFIRM | OPEN pin resuelve versión; magic sólo resuelve Strategy | Registry antes de Apply; Campaign rechaza magic de config; fallback Java inalcanzable en ruta Campaign |
| Rollover: misma cuenta + mismo magic + dos versiones activas prohibido con exposición vieja | S: EAs SQX gestionan posiciones por magic+símbolo | CONFIRM (necesidad técnica) | Dos EAs con mismo magic se pisan posiciones: interferencia económica, no sólo atribución | Default técnico, no owner decision |
| Clave de ingestión `H(namespace, wave_key, canonical, version_ref)` + única secundaria `(namespace, decision_ref, version_ref)` | S: `BuildIngestKey` = sha256(`wave::strategy::version`) sin namespace; adapter HTTP productivo ausente | CONFIRM | Preserva semántica frozen; 409 en misma wave/versión con Decision distinta es fail-closed aceptable | Definir `wave_key` exacto para flujos Generic no-Campaign en la slice WIRE |
| PromotionRecord recibo/provenance, no autoridad de membresía; V1/V2 coexisten | S: `DecisionRef` = `HashIdentity(decision.v1, …, inputDigest)` | CONFIRM | Membresía queda en Forge Decision | Ninguna |
| Artefactos: Forge evidencia, Echo copia operativa verificada; identidad = SHA/size/schema | S: `VerifyArtifactStream` size+sha256 | CONFIRM | Recuperación no depende de MinIO de Forge | bytea PG aceptable para EX5/config |
| Hechos crudos OPEN/MODIFY/DEAL/FINAL CLOSE/COVERAGE | S: EA actual emite OPEN/CLOSE sin deal IDs, CLOSE con `NowUnixMillis` | MODIFY | Deals son la economía irreducible; FINAL CLOSE debe ser aserción de cierre (volumen 0 probado) sin fabricar totales | Estado `CLOSED_INCOMPLETE_ECONOMICS` si faltan deals; coverage a tabla hermana |
| Identidades de evento (trade_id, source_event_id, origin key, order/deal/position, command_id) | S: `ReferenceTicket int32` en OPEN, `int64` en CLOSE; journal UNIQUE `(trade_id, account_id)` | CONFIRM | Ninguna redundante; origin key evita doble trade_id por collector duplicado | Ensanchar tickets a int64 en DTOs (ya en BWC) |
| Modelo de tiempo (broker+basis, observed, received, recorded, as_of) | S: `NowUnixMillis` = `TimeCurrent()`; 045 agrega `*_event/*_recorded` | CONFIRM | Colapsar broker/observed hace incorrecta la fidelidad futura | `received_at` se conserva por costo nulo |
| `REFERENCE_COVERAGE.v1` con hook de readback en EA exportado si hace falta | S: sin heartbeat/coverage en Reference EA | MODIFY | Hook en EA exportado toca cada versión y añade trabajo de plataforma | Collector enumera charts (`CHART_EXPERT_NAME`), `TERMINAL_TRADE_ALLOWED`, conexión, sesión y cursores; hook DEFER |
| `economic_commands` durable, único por `(routing_key, recipient, operation, seq)`, replay devuelve mismo id | S: `mm_engine` genera UUIDv7 nuevo por invocación; Execution EA dedupe por `command_id`; `OrderSend` antes de `Journal.Add` | CONFIRM | Sin él un replay StateFun crea intención económica nueva | Insert-before-send en misma transacción que routing final |
| Broker UNKNOWN reconciliado por command id/cuenta/historia/ids | S: EA no emite deal_id/POSITION_IDENTIFIER; comment MT5 truncable | MODIFY | UUID de 36 chars no cabe confiable en comment (31); sin campo correlación la reconciliación es heurística | Exigir campo visible en broker (p. ej. magic por comando en Execution) o política explícita: ambigüedad → UNKNOWN, no resend |
| `trade_routing` con fila por destinatario y CAS PENDING→final | S: planner sólo telemetría | MODIFY | Autoridad necesaria (NOT_REQUESTED vs MISSING), forma sobredimensionada | Una fila por `(source_event_id, operation)` con universo y resultados; EXPECTED se deriva de `economic_commands` |
| Reserva de riesgo como entidad durable separada (Reality Check) | S: sin implementación | MODIFY | Reserva siempre nace de un comando; segunda tabla = segunda autoridad | Columnas `reserved_risk`, `reservation_state` en `economic_commands` + serialización por cuenta |
| PortfolioVersion agregado único | S: 039 `strategy_portfolio_versions`, inmutabilidad sólo por COMMENT | CONFIRM | Ciclo de vida único | Trigger anti-UPDATE/DELETE en versiones publicadas |
| Bridge confirma al EA sólo tras ACK Kafka; Core persiste raw antes de fanout | S: `Publish` async fire-and-forget; planner y journal consumen `echo.reference-events.v1` en paralelo; journal absorbe errores `Save*` | CONFIRM | Origen de D-01/D-03 | Ninguna |
| O1–O3 como decisiones owner previas a NEXT EXACT | — | MODIFY | Son necesidades técnicas o defaults; sólo CC es política | Ver §11 |

### 4. Cinco cosas que deben estar bien ahora

1. **Sello de StrategyVersion post-compile y pin en OPEN.** Versionar antes de bytes finales o resolver versión por "current" al CLOSE/retry reescribe atribución histórica.
2. **Identidad de hechos crudos**: origin position key `(server, account_registration, platform, position_id)` única por OPEN aceptado; deals únicos por `(cuenta física, deal_id)`; raw inmutable persistido antes de enrutar; `trade_id` como linaje lógico. Todo Quality/Fidelity futuro cuelga de esto.
3. **Idempotencia del efecto económico**: comando durable antes de enviar, clave única de operación, replay devuelve el mismo `command_id`, UNKNOWN bloquea resend. Hoy `mm_engine` mintea UUID por invocación (S).
4. **Magic int64 end-to-end desde registry Forge, asignado antes de stampear, nunca reciclado**, con migración versionada del layout binario del EA (`TradeMapRecord.magic_number int`, `strategy_id uchar[64]` — S).
5. **Denominador de routing y snapshot de policy aplicada sellados en la decisión**, no filas mutables (`account_strategy_risk_policy` con `version`/`valid_until` — S). Sin esto Fidelity no distingue NOT_REQUESTED de MISSING.

### 5. Identity / version verdict

**RATIFICADO** el grafo: GeneratedStrategy → `canonical_strategy_id` (normalización pura del basename publicado con token `{CampaignRef}_gNNNNNN`) → `StrategyRef` (UUID) → `StrategyVersionRef` (content-addressed) → magic (Strategy, registry Forge) → `reference_bindings` (versión × cuenta × magic × prueba de enrollment) → OPEN pin (`version_ref`, `binding_ref`) → linaje Execution por `trade_id`/`command_id`.

Corrección C-1 (S): `CanonicalStrategyID` consulta `os.Getenv("HOST_KEY")` y recorta sufijos `.xxx` alfanuméricos de 3–16 chars cuando no coinciden con el host; el comentario del archivo afirma lo contrario. Hoy la ruta Campaign termina en `.z<dígito>` (2 chars) y no dispara la heurística — no se encontró `zNN` de dos dígitos en repo ni vault — pero una identidad canónica dependiente del entorno del host que la calcula es inaceptable como base de versiones y de ingestión. Mínimo: función pura con spec fija y golden tests; el hostKey se maneja en path/colección, como ya declara el propio archivo. Echo nunca recomputa el canónico: lo recibe.

B1 evaluado: recompilación byte-distinta, compilador, dependencias, params, nueva optimización → nueva versión (correcto, conservador, Forge controla). Reubicación de artefactos y cambio de broker → misma versión (correcto). MT4→MT5 y adaptadores futuros → `target_platform`. Sin fallo concreto. B2: nada por fusionar ni añadir; no crear RuntimeInstance/Deployment. B3: magic no es autoridad de versión; la unicidad y no-reciclaje son el invariante, el formato semántico es presentación. B4: la restricción de rollover es consecuencia directa de "magic estable entre versiones" + gestión de posiciones por magic en el EA; el costo (cuenta distinta o drenar) es bajo y no fuerza refactor.

### 6. Raw fact / effect verdict

Modelo mínimo durable:

- **Hechos**: DEAL como economía irreducible (deal_id, order_id, position_id, volumen, precio, fees, tiempo broker + basis, tiempo observado). OPEN = posición abierta + pin + riesgo inicial + contexto; MODIFY = cambio SL/TP; FINAL CLOSE = aserción de cierre con volumen restante 0 y último tiempo económico; si el set de deals está incompleto el trade queda `CLOSED_INCOMPLETE_ECONOMICS`, nunca totales fabricados. Hedging-only V1 difiere netting limpiamente porque `position_id` y deals ya son primera clase.
- **Comandos**: `economic_commands` con `command_id`, `routing_id`, destinatario, operación, `operation_sequence`, payload sellado, estado (`EXPECTED→SENT→ACKED|REJECTED|UNKNOWN→RECONCILED`), `reserved_risk`, `reservation_state`. Reintento de transporte = mismo `command_id`; reintento económico = nueva `operation_sequence` con motivo tras reconciliación; corrección = comando nuevo con `supersedes`.
- **Broker UNKNOWN**: el Execution EA persiste la intención antes de `OrderSend` (hoy es al revés, S) y bindea order/deal/position al resultado; tras crash, reconcilia por campo de correlación visible en broker. El comment MT5 (31 chars, truncable/sobrescribible) no sirve para el UUID. Opciones para la slice E-EFFECT: magic por comando en cuentas Execution (el magic de Execution no es identidad, es linaje de comando por D/Astra) o tag corto derivado; si no hay campo, la reconciliación por `(magic, símbolo, lado, volumen, ventana)` con más de un candidato → UNKNOWN persistente, alerta, sin resend automático. Default seguro: no reenviar nunca sin match positivo único.
- **Denominador de routing**: una fila `trade_routing` por `(source_event_id, operation)` con universo considerado, excluidos + motivo, policy snapshot ref, sello. EXPECTED = filas de `economic_commands` con ese `routing_id`. CLOSE usa los destinatarios que abrieron (hoy `emitCloseCommands` usa `ExecutionLookupResp`, S — correcto).
- **Coverage**: `reference_coverage` hermana (no dentro de `raw_trade_events`): intervalos por collector/cuenta con conexión, `TERMINAL_TRADE_ALLOWED`, inventario de charts (símbolo, TF, nombre de experto), sesión de mercado, cursores; intervalos idénticos consecutivos se coalescen. VALID_NO_SIGNAL requiere todos positivos; permiso per-EA se prueba en el readback de enrollment y se invalida si el inventario de charts cambia. Hook en el EA exportado: DEFER.

### 7. Portfolio / risk verdict

PortfolioVersion (candidatos+selección+asignación+restricciones+razones, inmutable al publicar) + reserva ligada a comandos + apply físico con reconciliación **forma un núcleo durable**. Modificaciones necesarias: (a) inmutabilidad por trigger/permisos, no por COMMENT (S: Hasura puede actualizar); (b) reserva como estado de `economic_commands` con serialización por cuenta (`SELECT … FOR UPDATE` en fila de cuenta o advisory lock) — sobrevive señales concurrentes, fill parcial (conversión), rechazo (liberación), ACK perdido (hold), crash (durable), supersesión de PortfolioVersion (la reserva no depende de la versión). Escisión selección/asignación: no; se añade sólo si aparece cadencia o autoridad distinta. Cuatro autoridades no conflated: PortfolioVersion (intención de asignación), `economic_commands` (intención por trade), reserva en comando (exposición en vuelo), raw/positions (exposición observada).

### 8. Persistence minimality

| Concepto | Clase | Justificación exacta |
|---|---|---|
| `strategy_versions` | KEEP | Autoridad de identidad de versión, inmutable, FK de pin y binding |
| `strategy_promotions` | KEEP | Idempotencia de operación e historial de recibos |
| `strategy_identity_aliases` | DEFER | Sólo lo necesita la recuperación histórica; fuera del camino crítico |
| `reference_bindings` | KEEP | Atribución histórica y recuperación; un enrollment canónico por versión |
| extensiones `raw_trade_events` | KEEP | Integridad del hecho crudo (pin, deals, clocks); extender migración 029, no tabla nueva |
| `reference_coverage` | KEEP (nuevo, hermana) | Evita inflar la tabla económica inmutable con intervalos operativos |
| `trade_routing` | KEEP simplificado | Autoridad del denominador; una fila por evento/operación |
| `economic_commands` | KEEP | Idempotencia del efecto, outbox, recuperación |
| reservas de riesgo | MERGE | Estado del comando que reserva; segunda tabla sólo si aparece reserva sin comando |
| cambios PortfolioVersion | KEEP | Inmutabilidad enforced sobre 039 |

### 9. Material cross-system contradictions

1. **Magic con tres fuentes hoy** (S): D dice registry Forge; `ApplySelectedRun.MagicNumber` viene de config de wave; Java exporter cae a `888111`; Echo `magic_number_override int4`. Impacto: identidad de Reference no canónica hasta que exista el allocator. Fix: registry alimenta Apply, Campaign rechaza magic de config, override Echo a int64 — ya en slices Astra; esta revisión sólo añade que ningún enrollment nuevo se considere canónico antes.
2. **`strategy_definitions` con dos escritores** (S): Hasura y autoprovisión `ensureJournalParentRows` (`ON CONFLICT DO NOTHING`). Impacto: filas placeholder `magic_*` compiten con el espejo canónico. Fix: columnas de provenance protegidas, autoprovisión deshabilitada para el namespace nuevo, inserción sólo por ingestión.
3. **Comando económico no idempotente ante replay** (S): `NewCoreCommand` mintea UUIDv7 por invocación; planner y journal consumen el mismo tópico en grupos distintos; Bridge publica async sin ACK al EA. Impacto: intención económica duplicada o hecho perdido sin error. Fix: `economic_commands` insert-before-send y raw-before-route (ya en contrato; se confirma material).
4. **`CanonicalStrategyID` dependiente de entorno** (S, nueva): ver §5 C-1.

Ciclo (G2): no se pudo construir ninguno. Allocation→Apply→compile→seal→Promotion→handoff→ingestion→binding→observation→routing/policy es lineal; `client_config` al collector depende de binding registrado, no al revés. Temporal declared/resolved no es contradicción arquitectónica.

### 10. Future-stress matrix

| Escenario | Clase | Nota |
|---|---|---|
| 100 estrategias | NO CORE CHANGE | — |
| 1.000 estrategias | NO CORE CHANGE | Coverage por cuenta, no por estrategia; magic 9999/mes/símbolo suficiente |
| Decenas de cuentas MT5 | ADDITIVE | Cuentas, bindings, collectors; un enrollment canónico por versión se mantiene |
| Broker/prop firm adicional | ADDITIVE | `account_registration` + revisión de symbol mapping; binding pinea broker |
| Múltiples hosts Forge | NO CORE CHANGE | B1A/B2 ya lo resuelven en Forge |
| Netting | BOUNDED MIGRATION | Deals y `position_id` ya son primera clase; falta adaptador de posición neta y certificación |
| Nuevo algoritmo Portfolio | ADDITIVE | `algorithm/version` en PortfolioVersion |
| Nueva fórmula analytics | ADDITIVE | Versión de fórmula en publicación; raw intacto |
| Retiro MT4 | NO CORE CHANGE | Cohorte legacy aislada |
| Proyecto Futuros | ADDITIVE (proyecto aparte) | `target_platform` en versión, plataforma en binding, raw schema versionado |

Ningún CORE REWRITE; no se requiere seam adicional.

### 11. O1/O2/O3 disposition

- **O1** — `reference_bindings` + un enrollment canónico por versión: **TECHNICAL DEFAULT, ratificación opcional**. Sin binding no hay atribución de versión (necesidad); dos Reference canónicas para la misma versión exigen regla de agregación que no existe en V1 (default: una canónica, otras `SHADOW`).
- **O2** — magic: (a) Forge canónico estable + override Execution command-local: **NO LONGER A QUESTION** (D + source); (b) asignación antes de Apply: **NO LONGER A QUESTION** (los bytes llevan el magic); (c) catálogo `CC`: **OWNER DECISION** acotada — propuesta default: sembrar desde el enum de símbolos Forex ya configurado en Forge, fail-closed ante símbolo sin código. No debe bloquear registry/unicidad: el formato es pluggable.
- **O3** — prohibición de versiones concurrentes misma cuenta con exposición vieja: **TECHNICAL DEFAULT, ratificación opcional**. Alternativa (cuenta distinta) ya es la recomendada.

Consecuencia: `ECHO-FORGE-LIVE-IDENTITY-WIRE-V1-NORMAL` puede empezar sin esperar O1/O3; el allocator sólo necesita la lista CC.

### 12. Fifteen (twenty) things we can leave ugly

1. IDs legacy `magic_*` en journal sin backfill.
2. `strategy_definitions` editable por Hasura en nombre/etiquetas (sólo provenance protegida).
3. Lab Clean con tiempos "recorded" sin conciencia de versión; lector nuevo aparte.
4. `v_trade_execution_delta` INNER JOIN intacta; el denominador nuevo vive en routing/comandos.
5. Dos conceptos de portfolio (grupos de cuentas vs portfolios de estrategias) coexistiendo.
6. Gateway como host de ingestión, sin servicio nuevo (la auth sí es P0, no ugly).
7. EX5/config operativos en `bytea` PG; sin MinIO en Echo.
8. Attach manual de Reference con runbook y prueba `MANUAL_VERIFIED`.
9. `current_version` como puntero manual nunca auto-avanzado.
10. Cohorte MT4 legacy sin port int64/varlen.
11. Decisions Finalist V1 legibles por dispatch, nunca convertidas.
12. `strategy_identity_aliases` inexistente hasta la recuperación histórica.
13. Analytics en moneda única.
14. Sin batch ingestion; cliente itera.
15. Coverage como etiqueta derivada; sin framework de monitoreo/SLO.
16. `received_at` y `recorded_at` ambos, aunque analytics use uno.
17. Campo `MagicNumber` en TaskSpec para flujos Generic; en Campaign el registry gana y la discrepancia falla.
18. Pin Temporal 1.35.0 vs 1.44.1 resuelto en release, no en arquitectura.
19. Envelope binario del EA con un header versionado mínimo; sin framework de serialización.
20. Código Adaptive deprecado y segundo consumer legacy del tópico permanecen.

### 13. Freeze matrix

| Contrato | Disposición |
|---|---|
| Strategy identity | FREEZE WITH BOUNDED CORRECTION (C-1 función pura) |
| StrategyVersion | FREEZE NOW |
| magic | FREEZE NOW; catálogo CC: OWNER POLICY REQUIRED (no bloqueante) |
| Promotion membership | FREEZE NOW (D V2; C1/C2 pendientes de implementación) |
| ingestion | FREEZE NOW (precisar `wave_key` Generic en WIRE) |
| artifact ownership | FREEZE NOW |
| runtime binding | FREEZE NOW |
| Reference authority | FREEZE NOW |
| raw facts | FREEZE WITH BOUNDED CORRECTION (C-2) |
| time model | FREEZE NOW |
| coverage | FREEZE WITH BOUNDED CORRECTION (C-3) |
| routing authority | FREEZE WITH BOUNDED CORRECTION (C-6) |
| economic command | FREEZE NOW |
| broker UNKNOWN | FREEZE WITH BOUNDED CORRECTION (C-4, dentro de la slice E-EFFECT) |
| PortfolioVersion | FREEZE NOW (inmutabilidad enforced) |
| risk reservation | FREEZE WITH BOUNDED CORRECTION (C-5 merge) |

### 14. Final decision

**B. FREEZE AFTER BOUNDED CORRECTIONS.** Ninguna corrección es TOP; todas caben en slices ya definidas por Astra (WIRE, MAGIC/SEAL, RAW, ROUTING/COMMANDS) o en una línea de Forge (`CanonicalStrategyID`).

### 15. NEXT EXACT

- **Factory**: `ECHO-FORGE-FINALIST-MODEL-V2-CORE-PROMOTION-WARNINGS-STRUCTURAL-GATES-NORMAL-C1` (sin cambio).
- **Echo architecture**: `ECHO-FORGE-LIVE-IDENTITY-WIRE-V1-NORMAL` incluyendo C-1 (`CanonicalStrategyID` pura + golden tests) y `wave_key` Generic; después `FORGE-MAGIC-ALLOCATION-AND-VERSION-SEAL-V1-NORMAL` con CC sembrado por default.
- **Targeted TOP sobreviviente**: ninguno.
- **No volver a diseñar**: grafo de identidad, sello de versión, semántica de magic, rollover misma cuenta, clave de ingestión, propiedad de artefactos, modelo de tiempo, comando económico, PortfolioVersion agregado único, arquitectura MT5 V2/V3.

### 16. Disagreements with Astra (TRACK K)

1. **O1–O3 como bloqueo owner** — TOO CONSERVATIVE. Evidencia: son consecuencias de D y del EA. Impacto: NEXT EXACT detenido por ratificaciones no necesarias. Alternativa: defaults técnicos + lista CC. Recomendación: §11.
2. **Reserva de riesgo como entidad** — TOO COMPLEX. Evidencia: toda reserva nace de un comando. Impacto: segunda autoridad de exposición en vuelo. Alternativa: estado en `economic_commands`. Recomendación: C-5.
3. **Coverage vía hook en EA exportado** — TOO COMPLEX / UNDER-SPECIFIED. Evidencia: sin heartbeat en EA (S); MQL5 permite inventario de charts desde el collector. Impacto: trabajo de plataforma por versión. Recomendación: C-3.
4. **Reconciliación UNKNOWN sin campo de correlación definido** — UNDER-SPECIFIED. Evidencia: comment MT5 31 chars; EA no emite deal/position ids (S). Impacto: recuperación heurística ambigua. Recomendación: C-4.
5. **`trade_routing` por destinatario con CAS** — TOO COMPLEX (leve). Recomendación: C-6. En todo lo demás material: ASTRA IS CORRECT; NO CHANGE.

## Evidencia y provenance

Source Symphony `db8a022` y Echo `e25165ba` inspeccionados read-only con orientación Graphify y dos exploraciones delegadas (Forge: identidad, magic, promotion, ingest key, artefactos, B1/B2, Temporal; Echo: Reference/Execution EA, SDK domain, StateFun planner/MM/journal/close, migraciones 001/029/039/043/045, Gateway, Bridge). Resources leídos íntegros: [[Echo + Echo Forge — Arquitectura de producto, gaps y roadmap de cierre 2026]], [[Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan]], [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] y las tres fuentes en `sources`. D: [[Echo - Auditoria POC e Identidad Forge-Echo 2026-08-23]], [[2026-08-23-durable-strategy-identity-v2-storage-support]], [[2026-09-04-echo-forge-campaign-builder-supply-identity]], [[2026-09-06-echo-forge-finalist-model-v2]], [[2026-09-06-echo-forge-mt5-fencing-and-cancellation-v3]], [[2026-09-06-forge-ingestion-runtime-live-authority-v1]]. Sin tests, builds, DB/Mongo/MinIO/ETCD/Kafka/Temporal, broker, deploy ni mutación de source.

## Límites y contradicciones

Echo master remoto `04c16bd` no releído (sin objeto local); runtime vivo no recertificado; P sigue fechado 2026-09-06. La viabilidad de `CHART_EXPERT_NAME` y de magic por comando en Execution es I basada en la API MQL5 documentada, no probada físicamente aquí. La ausencia de `zNN` de dos dígitos es evidencia de repo/vault, no garantía de SQX. Ninguna propuesta I de este documento es D; el owner ratifica el freeze B y la lista CC.

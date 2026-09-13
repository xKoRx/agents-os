---
type: resource
schema_version: 1
status: active
area: "[[Echo]]"
sources:
  - "[[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]"
  - "[[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]]"
  - "[[Echo + Echo Forge — Architecture Durability and Contract Review — Fable 5.1]]"
  - "[[Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan]]"
last_verified: "2026-09-07"
confidence: high
aliases: []
tags:
  - kind/resource
created: "2026-09-07"
updated: "2026-09-07"
---

# Echo SDK — Canonical Contract Final Freeze Review — Fable 5.1

## Síntesis vigente

Revisión independiente final (Cursor, Claude Fable 5.1, effort high) de [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]] (Astra) con una sola pregunta: ¿es suficientemente sólido para congelarse como contrato canónico de larga vida entre Echo Forge y Echo? Read-only fuera del vault; sin nueva auditoría de producto, sin roadmap, sin estimaciones, sin performance. **S** = source leído en esta sesión (Symphony `db8a022`, Echo `e25165ba`, ambos HEAD local); **D** = decisión owner/frozen; **I** = propuesta (Astra o esta revisión); **U** = no demostrado. Nada I se promueve a D por publicar esta nota.

**Disposición: B — FREEZE AFTER BOUNDED CORRECTIONS.** Cinco correcciones FR-1…FR-5, todas incorporables en S0 sin abrir otra slice. Ningún TOP. Ningún CORE REWRITE bajo el stress de §13.

### 1. Veredicto ejecutivo

1. **Entiendo el objetivo:** un lenguaje semántico compartido, aditivo por años, donde Forge produce evidencia sellada y Echo la ingiere sin heredar autoridad de generación ni de activación.
2. **Modelo canónico fundamentalmente sano:** sí. Identidad ≠ ejecución ≠ evidencia, DEAL irreducible, sets sellados por inputs exactos, ingestion sin efectos, evolución por capabilities.
3. **Echo SDK como autoridad congelable:** sí, en `v3/sdk/contracts` como módulo anidado stdlib-only.
4. **Defecto material más importante:** TradeSet/MetricSet/Evaluation nuevos incluyen el digest de *resultado* en su identidad (§7 y §10 del contrato). Rompe idempotencia de retry, esconde no-determinismo como «otra generación» y contradice el patrón S ya probado en Forge (`NewMetricSetRef`/`NewTradeSetRef` derivan identidad de inputs + semántica, no de payload). FR-1.
5. **Sobreingeniería más importante:** canonicalizador `echo-wire-json.v1` con normalización decimal dependiente de schema; se simplifica a perfil agnóstico de schema con validación aparte. FR-4.
6. **Subespecificación más importante:** regla de taxonomía métrica inconsistente (`return.r_pips` codifica base en key, `pnl.net` codifica base en key *y* declara basis NET/GROSS, drawdown usa basis). FR-2.
7. **Decisión más cara de cambiar después:** taxonomía `key/unit/basis/formula` (propaga a DB, policies, scores, front, fixtures) y las recetas de identidad de sets.
8. **Disposición final:** B. Freeze tras FR-1…FR-5 dentro de S0.

### 2. Cinco decisiones de alto riesgo

| # | Decisión | Propuesta actual | Veredicto | Por qué es caro después | Corrección exacta |
|---|---|---|---|---|---|
| 1 | ScopeV1 | Bloques opcionales tipados `subject/series/market/research/execution/portfolio/valuation/window` + `required_capabilities` | RATIFY con FR-3 | Scope digest participa en toda identidad de evidencia; una dimensión duplicada en dos autoridades se fosiliza | FR-3: retirar `valuation` de ScopeV1; `currency/pnl_basis/risk_basis/equity_basis` viven sólo en `MetricSet.defaults` y `Metric.basis/unit` |
| 2 | Identidad vs digest de contenido | Refs nuevos de TradeSet/MetricSet/Evaluation incluyen `content_digest`/`results_digest`/`result_payload_sha256` | MODIFY (FR-1) | Identidad histórica no se recalcula; una receta que depende del output impide lookup pre-cómputo y duplica autoridad ante no-determinismo | FR-1: identidad = pregunta exacta (scope, producer semántico, inputs exactos, schema, as_of); contenido = campo sellado write-once con conflicto explícito |
| 3 | Wire/hash canónico | `echo-wire-json.v1` con orden de claves, escape mínimo, normalización de decimales sólo en campos tipados, retención unknown, `H()`/`D()` | SIMPLIFY (FR-4) | Un perfil que necesita el schema para canonizar se implementa distinto en Go/JS/MQL y produce digests divergentes permanentes | FR-4: `C()` agnóstico de schema (sin normalizar decimales; validador rechaza decimales no canónicos y tokens numéricos no seguros); dos funciones hash nombradas y nunca mezcladas |
| 4 | Frontera NormalizedOperation | `TradingFact → NormalizedOperation → TradeSet → MetricSet`; `operation_ref` estable por tupla origen | RATIFY con FR-5 | Dos sets con el mismo `operation_ref` y economía distinta serían indistinguibles a nivel registro | FR-5: `record_digest!` (D sobre el registro sin sí mismo) y `supersedes_evidence_refs?` |
| 5 | Taxonomía métrica | Keys mixtas (`win_rate`, `return.r_pips`, `pnl.net`, `execution.missing_ratio`) + `unit` + `basis` + `formula` | MODIFY (FR-2) | Migrar keys después toca DB/policies/scores/UI/fixtures/históricos | FR-2: regla §6 de esta nota; `return.r_pips/r_money` → `return.total` + basis `R_PIPS/R_MONEY`; `pnl.net` → `pnl.total` + basis `NET` |

### 3. Matriz de identidad de contenido

| Objeto | Identidad | Digest de contenido | ¿Content-addressing necesario? | Por qué | Disposición |
|---|---|---|---|---|---|
| StrategyVersion | `H("echo-strategy-version.v1",[canonical,platform,exec_sha,inputs_sha,ctx_sha,deps_sha])` (I ratificado por Fable, no en S) | Es la identidad | **SÍ** | La versión *es* el paquete ejecutable; bytes distintos = versión distinta | FREEZE; no tocar |
| ArtifactRef | `sha256 + size` (+ kind/schema/platform); locator separado | Es la identidad | **SÍ** | Integridad de bytes independiente de ubicación; `VerifyArtifactStream` S | FREEZE (mapping `store_id` ya acotado por Astra) |
| Evaluation | Propuesto `H(subject,scope,producer_sem,inputs,result_schema,result_payload_sha256)` | `result_payload_sha256` | **NO** en identidad | Evidencia de una invocación: identidad = qué se preguntó; resultado distinto para la misma pregunta es conflicto a exhibir, no segunda Evaluation | MODIFY FR-1: quitar `result_payload_sha256` de la receta; sellarlo como campo write-once |
| TradeSet | Propuesto incluye `content_digest`, `completeness_digest` | `content_digest` (NDJSON lógico) + `payload.sha256` (bytes) | **NO** en identidad | Coincide con S `NewTradeSetRef(evaluation,scope,parser,schema)`: identidad por inputs/semántica, payload fingerprint en `Header` | MODIFY FR-1 |
| MetricSet | Propuesto incluye `results_digest` | `results_digest` | **NO** en identidad | Coincide con S `NewMetricSetRef(evaluation,scope,catalog,calculator,formula_set)`; el retry debe converger al mismo ref antes de calcular | MODIFY FR-1 |
| HandoffManifest / PromotionRecord | `Idempotency-Key = H("forge-echo-ingest.v1",[ns,wave,canonical,version_ref])` semántico + `promotion_record_id` | `payload_digest` sobre `C(body)` | **NO** (ya correcto) | Clave semántica + digest de contenido → 200 replay / 409 conflicto; es exactamente el patrón que FR-1 generaliza | FREEZE |
| Score / Ranking | S `NewScoreRef(subject,algorithm,impl,params,inputs)`: por inputs | Payload separado | **NO** | Ya consistente con FR-1 | FREEZE |

**Regla general FR-1 (freeze candidate):** `ref = H(tag, [lo que se pidió])` — subject/scope digest, producer semántico, inputs exactos con roles, schema/catálogo/fórmulas, `as_of`. `content_digest`/`results_digest`/`completeness`/`counts` son campos sellados. Escribir el mismo `ref` con distinto digest de contenido es `CONTRACT_CONFLICT` visible (patrón ya cubierto por el skill `write-once-conflict-triage`), nunca un set silencioso adicional. Un productor que no es determinista debe llevar la fuente de variación a `settings_digest`/versión o a un input explícito; no la esconde en la identidad. Se conserva íntegro «inputs distintos ⇒ generación distinta aunque el número coincida».

### 4. Scope — RATIFY con FR-3

Ortogonalidad verificada: `subject` (de qué trata), `series` (cómo se muestreó y de qué motor/entorno; `role` sólo live), `market` (instrumento/TF), `research` (qué celda/stage/muestra define membresía), `execution` (qué cuenta/broker/binding físico define la serie live), `portfolio` (qué PortfolioVersion), `window` (qué selección temporal), `required_capabilities`. FlowRun/StageExecution/build/host quedan como provenance, correcto. `execution.runtime_binding_ref` es scope y no provenance porque la serie live *es* la observación bajo ese binding.

**FR-3.** `valuation {currency, pnl_basis, risk_basis, equity_basis}` no es coordenada de muestra: es base de cálculo. Hoy aparece tres veces (Scope, `MetricSet.defaults`, `Metric.basis`) y entra al `scope_digest`, por lo que dos MetricSets con métricas idénticas pueden tener scopes distintos, o un Scope NET puede envolver métricas GROSS sin contradicción detectable. Corrección: retirar el bloque de ScopeV1; `MetricSet.defaults` conserva la herencia explícita; `Metric.basis/unit` son la única autoridad por métrica; `currency` de una serie live se deriva de `execution.account_ref` en provenance, no del scope. Ningún otro cambio de shape.

Stress: nuevo broker → `execution.broker_server_ref` (NO CHANGE); nueva dimensión analítica descriptiva → bloque opcional (ADDITIVE), con capability si afecta comparabilidad (MINOR); netting → bloque `position_model?` + capability (MINOR); Futures → `market.specification_ref?` aditivo (ADDITIVE); nueva dimensión WFM → campo en `research` + capability si define muestra (MINOR); nuevo algoritmo Portfolio → `portfolio_version_ref` (NO CHANGE). Lector viejo ante bloque desconocido: puede verificar `scope_digest` (canonicalización agnóstica, FR-4) y conservar la evidencia, pero no puede derivar/comparar mientras haya capability requerida no soportada; Astra ya lo fija y se ratifica. Precisión menor: `required_capabilities` del Scope cubre semántica del scope; el del envelope cubre el mensaje; no se fusionan.

### 5. NormalizedOperation — RATIFY con FR-5

La separación es correcta: TradingFact es realidad observada por fuente (DEAL economía irreducible; OPEN/MODIFY/CLOSE_ASSERTION proyecciones útiles), NormalizedOperation es normalización analítica con lineage (`source_evidence_refs`, `broker.deal_refs`, `economic_command_refs`, `reference_operation_ref`) y `missing_fields` explícitos; TradeSet aporta scope/producer/defaults; MetricSet consume inputs exactos. Nada del registro pertenece sólo a raw (los IDs broker son refs de lineage, no autoridad económica) ni sólo a set (`strategy_ref!`/`instrument_id!` por fila son redundantes bajo StrategySubject pero necesarios para sets de cuenta/portfolio; el validador exige igualdad con el subject cuando aplica).

| Fuente / caso | Mapeo sin inventar semántica |
|---|---|
| SQX histórico | REQUIRED origen/side/símbolo/tiempos/precio; volumen/risk/deals/broker IDs `UNSUPPORTED` con razón; `strategy_ref` existe tras adopción registry (S) |
| MT5 tester | Agregado de report + IDs de tester bajo namespace tester; economía DERIVED; nunca role REFERENCE |
| Reference live | DEAL-level lineage conservado; `CLOSED` sólo con ledger reconciliado, si no `CLOSED_INCOMPLETE_ECONOMICS`; `initial_risk` requiere snapshot |
| Execution live | Igual Reference + `economic_command_refs`; correlación ambigua = UNKNOWN, no match inventado |
| Parciales / late fees | Deals intactos; estado `PARTIALLY_CLOSED`/`CLOSED_INCOMPLETE_ECONOMICS`; corrección = nuevo set (G28) |
| Netting futuro | POSITION_IDENTIFIER ya primera clase; reversal exige bloque `attribution` + capability; MINOR, no rewrite |
| Futures futuro | `quantity.unit=CONTRACT + specification_ref`, `Price.specification_ref`, fact `CASH_ADJUSTMENT` nuevo + capability; ADDITIVE/MINOR |

**FR-5.** El contrato declara «corrección conserva origen y genera nueva revisión» y ordena payload «por operation_ref y revisión única seleccionada», pero NormalizedOperationV1 no tiene campo de revisión. Dos TradeSets con la misma `operation_ref` y economía distinta son indistinguibles a nivel registro (identidad ambigua, fuera de la deuda válida). Corrección mínima: `record_digest!: D("echo-operation.v1", registro sin record_digest)` y `supersedes_evidence_refs?: Ref[]`. `operation_ref` sigue siendo linaje estable; duplicado de `operation_ref` dentro de un set sigue inválido.

### 6. Regla semántica de métricas — FR-2 (candidate freeze authority)

- **KEY RULE.** `key` nombra la **estadística** calculada (qué se mide: `win_rate`, `profit_factor`, `return.total`, `return.expectancy`, `drawdown.max`, `drawdown.max_relative`, `duration.mean`, `execution.missing_ratio`, `slippage.mean`). Sintaxis `[a-z0-9_]+(\.[a-z0-9_]+)*`, ≤128 bytes; el punto es namespace, no semántica: ningún consumidor parsea segmentos. La key **nunca** codifica unidad, moneda, base, ventana, muestra ni fórmula. Cambiar el significado de una key es MAJOR; se crea key nueva. Nombres planos del catálogo Forge (`profit_factor`, S) son válidos como keys canónicas cuando la estadística coincide; el adapter mapea, no renombra históricos.
- **BASIS RULE.** `basis` selecciona la **serie de valoración o denominador** sobre la que se computa la estadística cuando existe más de una legítima: `NET`, `GROSS`, `PIPS`, `R_PIPS` (profit_pips/initial_risk_pips), `R_MONEY` (net/initial_risk_money), `EQUITY_CLOSED_NET`, `EQUITY_INTRADAY_NET`, `CLOSED_OPERATIONS`, `EXPECTED_COMMANDS`, `PRICE`. Enum abierto de strings gobernado por catálogo; el catálogo declara las bases permitidas por key (puede ser una sola). `basis!` es obligatorio en la representación resuelta (herencia explícita desde `MetricSet.defaults` permitida). Distinta base ⇒ `NOT_COMPARABLE` salvo conversión versionada declarada. No existe base `AUTO`.
- **UNIT RULE.** `unit` es la **dimensión del valor** (`RATIO`, `PERCENT`, `PROBABILITY`, `MONEY`+currency, `PIP`/`POINT`+spec, `PRICE`+spec, `R`, `SECOND`, `COUNT`, `BOOL`, `SERIES_REF`). El catálogo fija exactamente **una** unit por `(key, basis)`; `unit!` viaja resuelta en el wire para consumidores sin Go y el validador rechaza `(key,basis,unit)` no registrado. Tabla de reglas de representación de Astra (PRICE/PIP/MONEY/PERCENT/RATIO/DURATION/BOOL/SERIES) se ratifica sin cambios.
- **FORMULA RULE.** `formula {id, version, definition_digest}` es el algoritmo exacto; cambiarla nunca altera key/basis/unit y crea nuevo MetricSet, jamás muta históricos. Prohibido duplicar `(key, basis, formula)` en un set.
- **SELECTOR RULE.** Score, Ranking, policies, UI y fixtures referencian métricas con `MetricSelector {key!, basis!, formula_id?}`; `basis` es obligatorio cuando el catálogo admite más de una para la key. Un selector sólo por key es inválido. Esto elimina el riesgo de mezclar R pips y R money bajo un mismo nombre sin reintroducir keys que codifican base.

| Ejemplo | key | basis | unit | formula (ilustrativa) |
|---|---|---|---|---|
| Win rate | `win_rate` | `CLOSED_OPERATIONS` (y `NET`/`GROSS` para definir «gana») | `RATIO` 0..1 | `closed_wins_over_closed_count@1`; fuente percent 60 → adapter versionado |
| Profit factor | `profit_factor` | `NET` \| `GROSS` \| `R_PIPS` \| `R_MONEY` | `RATIO` | `sum_wins_over_abs_sum_losses@1`; sin pérdidas ⇒ `INSUFFICIENT/NO_LOSSES`, nunca 0/∞ |
| PnL gross | `pnl.total` | `GROSS` | `MONEY` + currency | `sum_gross@1` |
| PnL net | `pnl.total` | `NET` | `MONEY` + currency | `sum_complete_net@1`; sólo con costes completos en la misma moneda |
| R pips | `return.total` | `R_PIPS` | `R` | `sum_profit_pips_over_initial_risk_pips@1`; riesgo ≤0/null ⇒ no calculable |
| R money | `return.total` | `R_MONEY` | `R` | `sum_net_over_initial_risk_money@1` |
| Drawdown money | `drawdown.max` | `EQUITY_CLOSED_NET` \| `EQUITY_INTRADAY_NET` | `MONEY` + currency | `max_peak_to_trough@1` |
| Drawdown porcentaje | `drawdown.max_relative` | `EQUITY_CLOSED_NET` \| `EQUITY_INTRADAY_NET` | `PERCENT` | `max_peak_to_trough_over_peak@1`; denominador = peak equity, input exacto |
| Execution missing ratio | `execution.missing_ratio` | `EXPECTED_COMMANDS` | `RATIO` | `missing_over_expected@1`; sin coverage ⇒ `INSUFFICIENT` |
| Slippage price / pips | `slippage.mean` | `PRICE` \| `PIPS` | `PRICE` \| `PIP` (+spec) | `mean_signed_fill_minus_reference@1` |
| Duration | `duration.mean` | `EVENT_TIME` | `SECOND` | `mean_close_minus_open@1`; basis de reloj probada o `UNKNOWN` |

Deltas exactos sobre el contrato: §4 fila R y §8 tabla/ejemplos (`return.r_pips`/`return.r_money` → `return.total`+basis; `pnl.net` → `pnl.total`+`NET`), fixtures G27 y G33 usan selectores; se añade `MetricSelector` a `analytics.go`. El legado Lab (`ProfitFactorR/ProfitFactorMoney`, `MaxDrawdownR/MaxDrawdownMoney`, S) codifica base en el nombre de columna y permanece como proyección legacy identificada.

### 7. Wire / hash — SIMPLIFY (FR-4)

**Qué requiere bytes canónicos:** sólo estructuras que entran a un digest: Scope (`scope_digest`), subject, producer semántico, lista de inputs, calculator, keys solicitadas, resultados/completeness sellados, registros NormalizedOperation (FR-5 y líneas NDJSON) y el body del HandoffManifest (`payload_digest`). **Qué requiere sólo digest de contenido:** payload NDJSON (`content_digest` lógico + `payload.sha256` de bytes), artefactos. **Qué es JSON normal:** receipts, GET, errores, proyecciones.

**FR-4a — perfil agnóstico de schema.** `C()` = ordenar todas las claves por bytes UTF-8, arrays en orden declarado, escape mínimo (comilla, backslash, U+0000–001F), UTF-8 válido sin BOM, tokens pasados tal cual. **Sin normalización decimal dentro del canonicalizador**: los decimales ya son strings en el wire; el validador (paso separado, con schema) rechaza decimales no canónicos (`"1.50"`, `"+1"`, `"1e3"`, `"-0"`), tokens numéricos no enteros seguros, `null` tipado y claves duplicadas. Mismo resultado para payloads válidos, cero conocimiento de schema en `C()`, implementable en MQL5/JS sin librería de canonicalización. G25 pasa de «normalizar decimal tipado» a «rechazar decimal no canónico». Recetas `H()`/`D()`, `payload_digest` y todos los tags se conservan.

**FR-4b — dos funciones hash, nombradas.** El `H(tag,[…])` = SHA256 del array JSON compacto es la receta I de Astra para identidades **nuevas** (StrategyVersionRef, Idempotency-Key, sets). El `HashIdentity` vigente en Forge (S `sqx/core/domain/persistence_identity.go:94`) es `sha256(namespace + "\n" + join(parts,"\n"))` y gobierna los refs legacy de Evaluation/MetricSet/TradeSet/Score/Decision. El contrato debe nombrarlos distinto (`contracts/wire.HashTagged` vs legacy Forge) y prohibir recomputar refs legacy con la receta nueva o refs nuevos con la legacy. No es error factual de Astra; es precisión obligatoria para S0.

**Unknown fields e idempotencia:** correcto como está. `Idempotency-Key` modela igualdad semántica; `payload_digest` modela igualdad de contenido; el productor construye el body una vez y lo conserva write-once, por lo que un unknown field distinto bajo la misma key es legítimamente 409. No usar RFC 8785: cambiaría identidades ratificadas sin beneficio.

### 8. Módulo SDK — A (nested `v3/sdk/contracts`)

Se confirma A. Consecuencias materiales verificadas en S: Symphony `sqx/go.mod` declara `go 1.24` / `toolchain go1.24.5` y consume `xKoRx/sdk` vía `replace ../../sdk`; Echo `v3/sdk/go.mod` declara `go 1.25.5` con Kafka/StateFun/etcd/OTel. Opción B (paquete dentro del módulo SDK existente) arrastraría ese grafo a Symphony y forzaría MVS de OTel/etcd/uuid compartidos: rechazada por dependencia. Opción C (`echo/contracts` top-level) daría un tag más corto pero ninguna aislación adicional y contradice la dirección owner «Echo SDK posee el contrato»: rechazada por no material. Condiciones S0 (no defectos): `contracts/go.mod` declara `go 1.24` o el baseline acordado, nunca 1.25.5 a ciegas; Symphony en dev puede usar `replace` local, la release CI usa módulo pinneado con `GOPRIVATE`/credenciales git o vendoring, `GOWORK=off`; tag `v3/sdk/contracts/v1.0.0` tras gate S0; el directorio `v3` en el path es directorio, no sufijo de major, y ya funciona para `echo/v3/sdk` (S). Migración Forge→Echo no mueve el módulo: cambia productores, no semantic IDs.

### 9. TradeSet / MetricSet — RATIFY (con FR-1)

TradeSet no duplica raw: referencia `source_evidence_refs`, payload por ArtifactRef y counts acotados (coincide con `TradeSetEvidence` S). MetricSet no es base analítica universal: Metric es valor contenido, no entidad global; snapshots/UI siguen proyecciones. Nueva fórmula ⇒ nuevo MetricSet sin mutar el anterior. Mismo número con inputs distintos ⇒ evidencia distinta (identidad por inputs, FR-1). Sets grandes viajan por ArtifactRef con `content_digest` estable ante recompresión (G32).

### 10. Compatibilidad aditiva — RATIFY

Unknown optional preservado lossless; métrica/warning desconocido conservado sin score; enum de side/status/autoridad desconocido ⇒ `UNSUPPORTED_CAPABILITY`; fact económico desconocido bloquea completeness de la partición; `required_capabilities` en scope y envelope; minor/major definidos; decimales string; IDs string; ausente ≠ null ≠ cero ≠ UNKNOWN. Escenarios: Forge viejo → Echo nuevo (PASS, campos opcionales nuevos ausentes); Forge nuevo → Echo viejo (opcional no crítico PASS; capability requerida ⇒ 422, sin downgrade); bloque analítico nuevo (ADDITIVE); fact económico crítico nuevo (MINOR + capability, fail-closed en completeness); dimensión de scope que cambia membresía (MINOR + capability; lector viejo almacena opaco, no deriva); fórmula nueva (NO CHANGE de schema); productor nuevo tras migración (NO CHANGE). Un lector que no entiende una dimensión crítica falla cerrado; no calcula.

### 11. Handoff Forge→Echo — RATIFY

`member_proof.strategy_ref` repetido es aserción cruzada verificada por igualdad, no autoridad duplicada. `tested_executable_sha256/tested_inputs_sha256` repiten digests del manifest de versión: útiles como igualdad obligatoria (G09/G10), no drift porque cualquier discrepancia es 422. Evidence analítica opcional no bloquea. Nueva evidencia se enlaza por sidecar inmutable o nueva promoción, no editando el body aceptado. Una Version puede promoverse en varias waves (G04). V1 histórico usa adapter explícito sin downgrade disfrazado (G03). Nada por corregir.

### 12. Dos proyectos, un contrato — RATIFY

[[Echo Forge — Factory V2 Completion]] y [[Echo — Live Platform V1]] pueden avanzar en paralelo tras el pin S0 con fixtures golden y consumidores fake. Única sincronización real: el corpus S0 (`contracts/testdata/v1/manifest.json`) es propiedad de una PR en Echo SDK con revisión cruzada; ningún repo cambia el significado de un fixture unilateralmente. No aparece un tercer proyecto. FR-1…FR-5 caen en S0 antes del pin, por lo que no generan cambios coordinados posteriores.

### 13. Stress futuro

| Escenario | Clase | Nota |
|---|---|---|
| 100 / 1.000 Strategies | NO CONTRACT CHANGE | Manifests pequeños, payloads por ArtifactRef |
| Muchas StrategyVersions por años | NO CONTRACT CHANGE | Seal ratificado; sets referencian version_ref |
| Decenas de cuentas MT5 | NO CONTRACT CHANGE | `execution` block por serie |
| Nuevo broker / prop firm | NO CONTRACT CHANGE | `broker_server_ref`/`account_registration_ref` |
| Nuevas fórmulas | NO CONTRACT CHANGE | formula id/version + nuevo MetricSet |
| Nuevos score/ranking | NO CONTRACT CHANGE | algoritmo/params/inputs exactos |
| Nuevos algoritmos Portfolio | NO CONTRACT CHANGE | nueva PortfolioVersion |
| Forge dentro de Echo | NO CONTRACT CHANGE | cambia `producer`, no semantic IDs ni refs |
| MT4 retirado | NO CONTRACT CHANGE | cohorte legacy aislada |
| Netting | MINOR CONTRACT EXTENSION | bloque `position_model`/`attribution` + capability; deals ya primera clase |
| Futures | MINOR CONTRACT EXTENSION | `CONTRACT` + spec ref + fact `CASH_ADJUSTMENT`; sin reinterpretar LOT/pips |

Ningún MAJOR BREAK ni CORE REWRITE. No se construye ninguna capacidad futura ahora; los seams ya existen.

### 14. Anti-big-bang — CONFIRMADO

El freeze no exige reescribir Lab, journal, Decisions históricas, MT4, UI, mover el repo Forge, retirar el SDK externo, migrar MetricSets ni recalcular históricos. Todo path nuevo convive con adapters legacy identificados; FR-1…FR-5 sólo afectan tipos aún no implementados.

### 15. Correcciones de Astra revisadas

| Decisión Astra | Disposición | Razón material |
|---|---|---|
| Echo SDK como autoridad, módulo puro anidado | CONFIRM | §8 |
| Sustituir autoridad wire externa y rechazo total de unknown | CONFIRM | Aditividad correcta |
| ScopeV1 tipado con capabilities | CONFIRM con FR-3 | `valuation` duplicado |
| Refs nuevos con digest de resultado | MODIFY (FR-1) | Idempotencia/no-determinismo; S contradice |
| `echo-wire-json.v1` con normalización decimal en `C()` | MODIFY (FR-4) | Implementabilidad cross-language |
| Keys `return.r_pips`/`return.r_money`, `pnl.net` | MODIFY (FR-2) | Regla inconsistente |
| PF sin pérdidas ⇒ INSUFFICIENT; win_rate RATIO; R sin AUTO | CONFIRM | Semántica correcta |
| NormalizedOperation V1 y tabla de disponibilidad por fuente | CONFIRM con FR-5 | Revisión de registro |
| TimeWindow `[start,end)` + adapter legacy | CONFIRM | — |
| HandoffManifestV1 e ingestion §12 | CONFIRM | — |
| F01 HOST_KEY: pureza y retiro de sufijo como operaciones distintas | CONFIRM | Ya en Fable §5 |
| E01–E10 / F01–F08 | CONFIRM | No reabiertas |
| Deuda §17 | CONFIRM + §16 de esta nota | — |
| Ningún TOP | CONFIRM | — |

### 16. Deuda acotada — NO ARREGLAR AHORA

| Ítem | Por qué es seguro | Frontera que lo aísla | Trigger de limpieza |
|---|---|---|---|
| Legacy `HashIdentity` newline en Forge | Refs históricos verificables con su algoritmo | Función nombrada distinta; adapter registra `{legacy_ref, canonical_ref}` | Nunca por rutina; sólo si un consumidor exige recomputar legacy |
| `BuildIngestKey` = `sha256(wave::strategy::version)` sin namespace | Sin adapter HTTP productivo (S) | Nuevo wire usa Idempotency-Key | Retiro cuando no quede código que lo invoque |
| Lab Clean columnas con base en nombre (`*R`/`*Money`) | Proyección legacy identificada | MetricSet nuevo con selectores | Lector que necesite `(key,basis,unit)` migra ese lector |
| `MetricSnapshot`/edge=coverage/risk=1-edge | Etiquetado legacy | Score nuevo con propósito | Feature UI que exija Score canónico |
| R AUTO en outcomes viejos | `BASIS_UNPROVEN` | Nuevo recompute con inputs exactos | Nunca reescribir |
| Journal histórico sin version/binding | Raw conservado | `attribution_status=LEGACY_UNVERIFIED` | Sidecar si aparece evidencia exacta |
| `sqx.Trade` externo como decoder V1 | Única salida canónica es SDK Echo | Adapter a NormalizedOperation | Sin payloads V1 en el borde |
| Catálogo Forge `MetricsCatalogVersion 1.0.0` con nombres planos y `PNLBasisHint` informativo | Mapeo explícito a selectores | Adapter F02 | Nueva producción canónica del productor MT5 |
| `Scope` JSON legacy en evidencias Forge | Digest original intacto | Adapter + `unavailable_dimensions` | Borde nuevo soporta typed Scope |
| Sufijos host adoptados en canonical IDs | No renombrar evita ruptura de refs | F0 certifica antes de retirar en nuevas generaciones | Nunca «cleanup» de adoptados |
| `replace ../sdk` local en Symphony dev | Sólo desarrollo | Release CI con módulo pinneado | Cuando se publique `v3/sdk/contracts/v1.0.0` |
| Toolchain Echo 1.25.5 vs Symphony 1.24 | `contracts` declara baseline ≤ 1.24 | go.mod del módulo anidado | Cuando Symphony suba toolchain |
| Fórmulas float64 internas | Decimal en el borde | formula/rounding versionados | Error de precisión material |
| Copias huérfanas pre-commit | Nunca receipt parcial | GC por referencias con grace | Volumen observable |
| Sin generador universal JS/MQL | Corpus común | Bindings mínimos | Duplicación demostrada |
| MT4 protocolo viejo | Cohorte separada | Sin int64 truncado | Migración voluntaria con proof |

### 17. Freeze matrix

| Área | Clasificación | Condición |
|---|---|---|
| Echo SDK authority | FREEZE NOW | — |
| SDK module boundary | FREEZE NOW | Baseline Go y acceso privado son checks S0, no diseño |
| StrategyVersion | FREEZE NOW | Receta intacta |
| ArtifactRef | FREEZE NOW | Mapping `store_id` ya acotado |
| Scope | FREEZE WITH BOUNDED CORRECTION | FR-3 |
| Time model | FREEZE NOW | — |
| TradingFact | FREEZE NOW | Correcciones Fable C-2/C-3 ya integradas por Astra |
| NormalizedOperation | FREEZE WITH BOUNDED CORRECTION | FR-5 |
| TradeSet | FREEZE WITH BOUNDED CORRECTION | FR-1 |
| Metric | FREEZE WITH BOUNDED CORRECTION | FR-2 |
| MetricSet | FREEZE WITH BOUNDED CORRECTION | FR-1, FR-2 |
| Score | FREEZE NOW | Selector FR-2 aplica a sus inputs |
| Ranking | FREEZE NOW | — |
| Promotion/Handoff | FREEZE NOW | C1/C2 son implementación, no contrato |
| Wire compatibility | FREEZE NOW | — |
| Canonical hashing | FREEZE WITH BOUNDED CORRECTION | FR-4 |
| Ingestion | FREEZE NOW | Gates físicos E1 son certificación, no diseño |
| Runtime binding | FREEZE NOW | — |
| Economic command | FREEZE NOW | — |
| Coverage | FREEZE NOW | — |
| Netting / Futures | DEFER | Seams disponibles |

**TARGETED TOP REQUIRED: ninguno.**

### 18. Decisión final

**B — FREEZE AFTER BOUNDED CORRECTIONS.** Cinco correcciones FR-1…FR-5, todas de tipos/recetas/fixtures aún no implementados, incorporables en S0 sin abrir otra slice ni tocar identidades ratificadas. Sin TOP. Pendiente de ratificación owner del freeze; esta nota no crea D.

### 19. Cerrado — no rediseñar de nuevo

Echo SDK como autoridad en `v3/sdk/contracts`; StrategyVersionRef y su receta; Idempotency-Key y payload_digest; identity ≠ execution ≠ evidence; magic Forge-owned estable; pin al OPEN; Reference post-broker; DEAL irreducible y CLOSE_ASSERTION; ScopeV1 sin `valuation`; regla identidad-por-inputs/contenido-sellado; regla key/basis/unit/formula/selector; TradingFact → NormalizedOperation → TradeSet → MetricSet; TimeWindow `[start,end)` con adapters; `echo-wire-json.v1` agnóstico de schema con `H()`/`D()`; unknown-field retention; capabilities como mecanismo de evolución; membership ≠ rank; ingestion ≠ activation/capital; tres propósitos de fidelidad/calidad; una PortfolioVersion; los dos únicos proyectos. Reabrir sólo con evidencia S/P material.

### 20. Next exact

- **CONTRACT:** abrir S0 NORMAL en Echo incorporando FR-1…FR-5 en la SPEC antes de escribir tipos: recetas de ref sin digest de resultado, `MetricSelector`, ScopeV1 sin `valuation`, `C()` agnóstico + validador, `record_digest`; ajustar G25/G27/G33 y añadir un fixture de conflicto write-once (mismo ref, distinto content_digest ⇒ `CONTRACT_CONFLICT`).
- **FORGE:** C1/C2 desde B2 y F0 (canonicalizer puro + prueba intra-wave) sin esperar S0; F2 tras pin S0.
- **ECHO:** S0 → E0 → E1 con productor fake; A0 sólo para inputs nuevos.
- **PARALELO:** S0 ∥ F0/F1. Tras pin: F2 ∥ E0/E1 ∥ A0.
- **DEBE ESPERAR:** F2 allocation real (catálogo CC owner), integración física real (ambos outputs certificados).
- **NO AUDITAR DE NUEVO:** identidad/version/magic, live authority, B1/B2, Scope, sets, taxonomía métrica, wire, módulo SDK, handoff, ingestion.

## Evidencia y provenance

- Autoridades leídas íntegras: las cuatro `sources`; Decision `80-agents/memory/public/decision/echo/2026-09-06-forge-ingestion-runtime-live-authority-v1.md`; feedback y checkpoints de [[Echo — Live Platform V1]] y [[Echo Forge — Factory V2 Completion]].
- Source S (read-only, orientación Graphify previa): Symphony `db8a022` — `sqx/core/domain/persistence_identity.go` (`hashIdentity` newline L94; `NewEvaluationRef` L397; `NewMetricSetRef` L413; `NewTradeSetRef` L425; `NewScoreRef` L445), `sqx/core/domain/persistence_contracts.go` (`MetricSetEvidence` L220, `TradeSetEvidence` L290), `sqx/core/evaluation/catalog.go` (nombres planos, `MetricUnit`, `PNLBasisHint`, `MetricsCatalogVersion="1.0.0"`), `sqx/core/evaluation/canonical_scope.go`, `sqx/go.mod` (`go 1.24`, `toolchain go1.24.5`, `replace ../../sdk`). Echo `e25165ba` — `v3/sdk/go.mod` (`go 1.25.5`, deps infra), `v3/sdk/lab/formulas/formulas.go` (`RBasis auto/money/pips`), `v3/sdk/lab/domain/types.go::MetricSnapshot` (`ProfitFactorR/Money`, `MaxDrawdownR/Money`), `go.work`.
- No se ejecutaron tests/builds, ni DB/Mongo/MinIO/ETCD/Kafka/Temporal, ni MT4/MT5/broker, ni deploy; ningún archivo fuera del vault fue modificado. Graphify se usó como orientación en Symphony; el índice Graphify del vault no se refresca por la restricción read-only fuera del vault (cache externo), igual que en la sesión Astra.

## Límites y contradicciones

- FR-1…FR-5 son I; el owner ratifica el freeze B y las correcciones. No se patchó el contrato Astra: no se halló error factual; se enlazó esta disposición desde su cabecera.
- StrategyVersionRef «ratificado» es I confirmado por dos revisiones, no código S; no se altera.
- La afirmación de que el nested module funciona con `v3` como directorio se apoya en que `echo/v3/sdk` ya existe y compila en el workspace (S), no en una publicación por proxy verificada; S0 lo prueba con `GOWORK=off`.
- Decidir `contracts/go.mod` `go 1.24` frente a subir Symphony es operativo de S0, no contractual.
- El legado Lab/Forge se describe por source estático; no se afirma comportamiento runtime.

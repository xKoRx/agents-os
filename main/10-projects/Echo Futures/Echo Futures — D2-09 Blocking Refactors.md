---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D1 Analysis Pack]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
  - "[[Echo Futures — D2-05 Instrument Session Provider]]"
  - "[[Echo Futures — D2-06 Market Runtime]]"
  - "[[Echo Futures — D2-07 Execution Runtime]]"
  - "[[Echo Futures — D2-08 Strategy Runtime]]"
aliases:
  - Echo Futures D2-09
  - EF Blocking Refactors
  - Q16 Echo Futures
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-design
created: "2026-09-28"
updated: "2026-09-28"
---

# Echo Futures — D2-09 Blocking Refactors (Q16)

## Propósito

Cerrar `Q16 — Blocking Refactor`: clasificar cada gap heredado de D1 y cada superficie del diseño D2 como `REUSE / ADAPT / REPLACE / NEW / DEFERRED_NON_BLOCKING`, demostrar que ninguna capacidad requerida para V1 depende silenciosamente de una pieza legacy incompatible, y habilitar (si no hay blocker) la integración final de D2 en [[Echo Futures Architecture Candidate V1]].

No implementa código, no reabre D2-01..08 sin contradicción material, no rediseña el modelo target congelado, no abre D3/Astra ni D4/D5/D6, no investiga providers ni certifica transports.

## 1. Executive verdict

**Primary Manager closure — 2026-09-28:** Q16 y D2-09 quedan aceptados. El único repair del review final fue reclasificar la implementación física `ReferenceEvent → Signal` como `DEFERRED_MANDATORY / Iteration 2`; V1 Futures conserva sólo el `Signal` canonical runtime y el boundary Core reservado. La auditoría de identities y la excepción replay para `operation_id/order_id` se aceptan con el alcance V1 documentado.

```text
D2-09 STATUS: MANAGER_CLOSED

Q16 = CLOSED
BLOCKING_ARCHITECTURE = NONE
CORE REWRITE = NOT_REQUIRED
OWNER DECISIONS REQUIRED = NONE
```

- No existe ningún gap que impida construir V1 con los seams ya congelados. El hypotheses manager (`Q16 = CLOSED`, `NO CORE REWRITE`, set `NEW/ADAPT/REPLACE` para D5/D6) se confirma **y sobrevive el intento de refutación**: cada superficie candidata a blocker fue contrastada contra source y contra los contratos congelados, y todas caen en categorías A–G sin usar `BLOCKING_ARCHITECTURE`.
- El register de 7 ítems blocking de D1 queda **reconciliado**: cinco son superficies NEW ya diseñadas en D2-04..08, una es ADAPT/REPLACE acotado (DayBoundary) y una está `DEFERRED_TO_THE_LAB` por decisión owner (Trade/Lab). Ninguno requiere hoy un refactor de Echo existente para que V1 sea construible.
- La auditoría transversal de identidades contra EXACT_REPLAY cierra **sin contradicción**: `signal_id` ya es replay-stable (corrección D2-08); `operation_id`/`order_id`/`decision_id`/action ids se demuestran correctos como identidades de ejecución LIVE irrepetible bajo M1/M2, **fuera** del boundary de replay congelado en V1; la propiedad transversal queda congelada para cualquier identidad futura que entre a output determinista.
- Las garantías StateFun/Kafka (EXACTLY_ONCE egress, read_committed, transaction timeout, checkpoint coupling) **no están configuradas hoy** en el `module.yaml` físico (verificado en baseline): clasificadas `IMPLEMENTATION_REQUIRED` con acceptance en D5/D6. No se afirma que producción ya ofrezca esa garantía.
- `DT-EF-REFERENCE-SIGNAL-03` queda confirmado como `DEFERRED_MANDATORY / Iteration 2`: V1 Futures no depende del planner Reference legacy (sección 5.3).

## 2. Authorities / baselines

| Autoridad | Baseline | Rol |
|---|---|---|
| [[Echo Futures]] | vault HEAD al inicio del worker (`5af8e18f`, ≥ baseline mínimo `2c4bc4fd` "close D2-08 and open Q16 gate") | Decisiones owner D2-01..03, estados y cierres D2-04..08, roadmap. |
| [[Echo Futures — D1 Analysis Pack]] | aceptado por owner 2026-09-26 | Register de refactors D1 (§6) y matriz Q1. |
| D2-04 Operation/Order/Fill/Position | MANAGER_CLOSED | Lifecycle, M1/M2, recovery authority, reuse map §9. |
| D2-05 Instrument/Session/Provider | MANAGER_CLOSED | Catalogs, provider domain, R15–R18, reuse map §21. |
| D2-06 Market Runtime | MANAGER_CLOSED (OD-C1 ratificada) | Market runtime, EXACT_REPLAY boundary, reuse map §23. |
| D2-07 Execution Runtime | MANAGER_CLOSED (OD-D2-07-1 cerrada) | Bridge sibling, M2 journal, routing 3 caminos, reuse map §23. |
| D2-08 Strategy Runtime | MANAGER_CLOSED | Strategy engine, Signal identity determinística, reuse map §21. |
| `xKoRx/echo` | `origin/master = 372af59a7b83604781346613da01e3d510ea1360` (fetch re-verificado sin delta en esta sesión) | Source físico V3; inspección puntual, no repo-wide audit. |

Artifacts D4/D5-M1A (Simulator/Topstep SPEC) tratados como históricos; ninguna conclusión de este gate proviene de ellos.

Spot-checks físicos ejecutados en esta sesión (clon `~/aranea/work/d4-shot1-20260925/echo`, worktree en baseline):

- `v3/core/deploy/flink-statefun/develop/module.yaml`: los specs `io.statefun.kafka.v1/egress` **no declaran delivery semantics** ⇒ default documentado AT_LEAST_ONCE (confirma D2-04 R2 / D2-08 R2).
- Cero `type Signal` en `v3/**.go` (confirma D2-08 §21: Signal/strategy_engine = NEW).
- `v3/sdk/utils.GenerateUUIDv7` existe (confirma el generador citado por D2-04 §2.1).
- `v3/sdk/mm/pip_size.go` = `PipSizeCanonical` convención FX (confirma que pips es pieza legacy unit-scope, aislable).

## 3. D1 register reconciliation

El register D1 (7 ítems "blocking para implementar el diseño") se actualiza contra las decisiones D2 vigentes:

| # | Ítem D1 | Estado tras D2 | Clasificación Q16 |
|---|---|---|---|
| 1 | Signal boundary limpio separado de ReferenceEvent | Resuelto por diseño: contrato `Signal` D2-03 + boundary Core reservado para futura compatibilidad Reference; `ReferenceEvent` queda LEGACY_ONLY en V1 Futures. La implementación física `ReferenceEvent → Signal` pertenece a DT-EF-REFERENCE-SIGNAL-03 / Iteration 2. | NEW (Signal/runtime) + DEFERRED_MANDATORY (adapter/migración Reference) + LEGACY_ONLY (path Reference actual) |
| 2 | Operation/Order/Fill identities + lifecycle | Resuelto por D2-04 (aggregate, guards, M1/M2, recovery). `CoreCommand`/`ExecutionResult` permanecen wire legacy. | NEW (domain package + `echo/operation`) |
| 3 | Instrument/Contract + hot mapping | Resuelto por D2-05 (catálogos, binding contexts, pin único). Patrón symbol-mapping REUSE/EXTEND. | NEW (catálogos) + REUSE (patrón hot) |
| 4 | TradingSession/calendar separado de Account DayBoundary | Resuelto por D2-05B/§11 (tres autoridades separadas). Mecanismo DayBoundary legacy incompatible ⇒ reemplazo acotado del camino Futures. | NEW (Calendar) + ADAPT/REPLACE (DayBoundary mechanism, R18) |
| 5 | MoneyManagement stateful sobre Operation | Resuelto por D2-04/D2-08 (`mm_state` en `echo/operation`; `MMEngineFn` stateless-TTL = REPLACE; patrones = ADAPT; `sdk/mm` = REUSE/EXTEND). | REPLACE (estado) + ADAPT (patrones) + REUSE (calculators) |
| 6 | Provider/ProviderProgram/versioned RuleSet | Resuelto por D2-05C (dominio nuevo; `prop_rulesets` legacy shape REPLACED para path Futures; ProviderProgram de seis props **no** es requisito D2). | NEW (provider domain) |
| 7 | Trade projection/provenance para Lab | `DEFERRED_TO_THE_LAB` por owner (2026-09-26). V1 lleva `run_mode`/`run_id` (I11) para no cerrar la puerta. | DEFERRED (no blocker; no reabrir) |

Conclusión: **ningún ítem D1 queda como refactor bloqueante de Echo existente**. Se convirtieron en obligaciones de construcción D5/D6 con clasificación explícita.

## 4. Auditoría transversal de identidades — replay-stable

Mandato D2-08: chequear toda identidad generada por Echo/domain/runtime que participe en correctness/dedup/ordering/correlation/replay; no asumir que UUIDv7 runtime-generated es replay-stable.

### 4.1 Inventario y clases

| Identidad | Origen | Clase | Decisión |
|---|---|---|---|
| `signal_id` | `echo/strategy_engine` | **REPLAY-STABLE (determinística)** | Ya corregida por D2-08 §5/§6: derivada de run identity + `strategy_id` + `strategy_eval_seq` + `signal_seq`; sin RNG ni wall clock. EXACT_REPLAY regenera la misma identidad. |
| `strategy_eval_seq` / `strategy_cycle_seq` / `signal_seq` | strategy island | REPLAY-STABLE (escalares monotónicos) | Checkpointeados/journalizados; replay los reconstruye del journal. |
| `owner_input_seq` / `runtime_ts` | cada isla | REPLAY-STABLE | Journalizados (D2-06 §15/§18). |
| `stream_seq` / `event_ts` / `authority_epoch` | market inputs | REPLAY-STABLE | Inputs canónicos journalizados; guards `stream_seq` (I5). |
| `timer_id + generation` | DomainClock | REPLAY-STABLE | Todo `TimerFired` admitido journalizado (D2-06 I15/§16); stale generation = NO-OP determinístico. |
| `BarId` / `session_id` / `stream_id` | derivadas | REPLAY-STABLE | Determinísticas por construcción: `(stream_id,timeframe,bucket_open_utc)`, `(calendar_id,session_date)`, `(instrument_id,contract_id)`. |
| `operation_event_seq` | `echo/operation` | REPLAY-STABLE (runtime ordering) | Sello del state owner; replay-acotado a runtime ordering/stale-protection (D2-04 R12). |
| `operation_id` | `echo/operation` (UUIDv7) | **LIVE-IRREPEATABLE (fuera del boundary de replay V1)** | Decisión demostrada en §4.2: se mantiene UUIDv7. |
| `order_id` / `client_order_id` | `echo/operation` (UUIDv7) | LIVE-IRREPEATABLE | Ídem §4.2; estabilidad **dentro de la vida del comando** es requisito M2 (misma key en retry/reconnect/redelivery). |
| `decision_id` (MM) | `echo/operation` (UUIDv7) | LIVE-IRREPEATABLE | Correlaciona Orders de una misma decisión MM; fuera del replay boundary. |
| `cancel_id` / `replace_request_id` | `echo/operation` / adapter actions | LIVE-IRREPEATABLE | Action identities estables ante redelivery (M2); fuera del replay boundary. |
| `request_id` (Admission/Reservation) | `echo/provider_rules` | LIVE-IRREPEATABLE | Dedup request/result account-keyed; fuera del replay boundary. |
| `ProviderForceClose.decision_id` | `echo/provider_rules` | LIVE-IRREPEATABLE | Idempotencia del fan-out safety; correctness no depende de su estabilidad (intent idempotente + guards); fuera del replay boundary. |
| `provider_execution_id` / `provider_order_id` | **venue** | EXTERNAL NATIVE | Se preserva identidad nativa; prohibida síntesis para correctness (D2-07-R1); dedup `(execution_account_id, provider_execution_id)`. |
| `run_id` / `run_mode` | run | RUN IDENTITY | Parte del initial RunManifest inmutable; `signal_id` deriva del run original (`replayed_run_id` preservado). |
| `binding_id` / `calendar_id` / `rule_set_id` / `provider_id` / `program_id` / `account_strategy_id` / `strategy_id` / `instrument_id` / `contract_id` / `account_id` | config | CONFIG IDENTITY | Declaradas/distribuidas hot; no generadas por runtime. |

### 4.2 Decisión demostrada: `operation_id` / `order_id` permanecen UUIDv7

Pregunta §11 del mandato: ¿EXACT_REPLAY requiere preservar esas mismas identidades? **No, en V1 — y la demostración es estructural, no de conveniencia:**

1. **Alcance del boundary de replay.** El EXACT_REPLAY congelado (D2-06 §19/§22) reproduce *market-dependent decisions* del run live real y explícitamente **no toca el venue**; la autoridad de execution recovery permanece en D2-04/D2-05, fuera del replay de mercado. El boundary de replay no re-materializa Operations ni re-emite Orders ⇒ ninguna fixture de replay compara `operation_id`/`order_id`.
2. **Claim del dominio de ejecución, deliberadamente acotado.** D2-04 R5/R12 congela "same ordered input stream ⇒ same decisions" como propiedad de dominio y **renuncia** a persistir el stream completo de inputs de ejecución y a prometer replay exacto de sesión live. No existe en V1 un mecanismo cuyo output determinista incluya `operation_id`.
3. **Crash safety no depende de estabilidad de identidad.** Bajo M1 (2PC state↔egress), un comando es visible en el topic sólo si el checkpoint con su estado commiteó; ante abort, ambos hacen rollback ⇒ una identidad regenerada post-crash **jamás convive con un artefacto físico del intento abortado** (D2-04 §5.6-M1, caso 5). Bajo M2, el adapter garantiza misma `client_order_id` ⇒ a lo sumo un side effect físico (journal durable write-ahead + resolución contra venue), sin blind retry. La estabilidad requerida de `client_order_id` es **intra-vida del comando** (retry/reconnect/redelivery), no inter-regeneración.
4. **Correlación usa el valor persistido, no una regeneración.** La correlación evento→operación es adapter-owned (D2-04 §8.2): el adapter stampea `operation_id`+`order_id` desde su submission registry al enviar y devuelve esos mismos valores; todo consumidor referencia el valor persistido atómicamente con el primer checkpoint que pudo permitir escape del comando.

**Preference manager considerada** ("hacerla estable suele ser más simple"): migrar `operation_id` a identidad derivada sería posible sin entidades nuevas — `(account_strategy_id, strategy_cycle_seq)` ya identifica unívocamente el ciclo (D2-08 §7) — pero cambiaría D2-04 §2.1, PG PKs y el contrato del adapter **sin necesidad demostrada en V1**, y el mandato prohíbe rediseñar sin contradicción demostrable. Queda registrado como **camino de migración natural** si una iteración futura extiende EXACT_REPLAY al dominio de ejecución: entonces esas identidades deben migrar a la familia determinística (§4.3). Es una nota de Iteración 2, no deuda de V1.

**Corrección documental aplicada:** ninguna contradicción de arquitectura en D2-04; la aclaración D2-07-R1 (prohibición de sintéticos para Fill identity) ya está alineada en el cierre D2-08 del proyecto (se eliminó el wording `orderId:seq`). Este artifact congela la clasificación; no modifica D2-04.

### 4.3 Propiedad congelada + familia conceptual

```text
domain-generated identity that is part of deterministic output
must be replay-stable
```

Familia conceptual (sin congelar encoding/hash):

```text
DeterministicDomainID(
  run_identity,        # run_id del RunManifest inmutable
  owner_identity,      # isla/aggregate dueño (p.ej. strategy_id)
  owner_event_seq,     # secuencia monotónica del dueño (p.ej. strategy_eval_seq)
  kind,                # p.ej. signal
  local_seq            # p.ej. signal_seq
)
```

Única instanciación V1: `signal_id`. No se crea un ID framework (mandato §10): la familia es una regla de diseño que cualquier identidad futura que entre a decision log/digest de replay debe satisfacer.

### 4.4 Consistencia EXACT_REPLAY transversal (mandato §27)

| Riesgo | Estado transversal | Veredicto |
|---|---|---|
| Random identity | `signal_id` determinística; ejecución fuera del boundary (§4.2) | Sin contradicción |
| Wall clock | `DomainClock`/`runtime_ts`; `time.Now()` prohibido en dominio; anti-patrón legacy `maxIntentAgeMs` (`execution_planner.go`) **no se promueve** al camino nuevo (D2-08 §21: fan-out usa event-time/`valid_until`) | Sin contradicción |
| Unrecorded ordering | `owner_input_seq` per-island + journal de merges multi-stream; sin total order global reclamado | Sin contradicción |
| Unrecorded config | Regla ConfigTransition material (D2-06 §20); initial manifest inmutable; replay nunca lee config corriente | Sin contradicción |
| Non-deterministic collection iteration | La lógica pura debe ser determinística ante el mismo input; la disciplina de implementación (sin iteración de maps no ordenada en decisiones) es obligación de acceptance D5/D6, no cambio de arquitectura | Deuda de verificación (categoría D) |
| Current config reads during replay | Prohibido y ya bloqueado por diseño: REPLAY/BACKTEST inyectan snapshots/manifests (D2-05 §19, D2-06 §20) | Sin contradicción |
| Eventual cache como authority | Prohibido en todos los seams: admission lineariza en `echo/provider_rules` (R15), fan-out lineariza target set en su isla (D2-08 §8), PG jamás recovery authority (D2-04 R11) | Sin contradicción |

## 5. Strategy / Signal refactors

### 5.1 Strategy runtime

- `echo/strategy_engine` y el contrato `Signal` **no existen en V3** (verificado: cero `type Signal`). Clasificación: **NEW_REQUIRED_FOR_V1** (isla StateFun key `strategy_id`, triggers declarativos, egress `echo.signals.v1` EXACTLY_ONCE).
- `strategy_config.go` (`StrategyConfigFn`): **REUSE patrón KVS / LEGACY_ONLY contenido** — es execution-policy config, no runtime de Strategy.
- `execution_planner.go` (`ExecutionPlannerFn`): **ADAPT patrón / REPLACE flujo** — el fan-out validado (kache + filtro por cuenta + broadcast por key) deviene `echo/signal_fanout` consumiendo `Signal` con event-time; el flujo Reference→planner queda LEGACY_ONLY.

### 5.2 Signal / ReferenceEvent migration (mandato §13)

- Target final congelado: `ReferenceEvent → Core compatibility adapter → Signal → canonical runtime` (D2-08 §20). **En V1 Futures sólo se reserva ese boundary; el adapter físico no es requisito de implementación.** Cuando se ejecute DT-EF-REFERENCE-SIGNAL-03 en Iteration 2, traducirá a `source=REFERENCE` y convergerá al mismo camino canónico; no habrá segundo runtime económico permanente.
- **V1 Futures no depende del planner Reference legacy:** el camino canónico nace en `echo/strategy_engine`; el path legacy `ExecutionPlanner→MMEngine→CoreCommand→Bridge` sigue para MT/Forex sin ser prerequisito del camino nuevo. Verificado en D2-08 §20/§21 y §23 (reuse map): ninguna pieza NEW del camino Futures consume ReferenceEvent.
- `DT-EF-REFERENCE-SIGNAL-03` queda **DEFERRED_MANDATORY / Iteration 2** (migración completa del execution path reference y tabla de traducción de acciones reference→intent). No bloquea V1.

## 6. Operation / MM refactors (mandato §14)

| Pieza legacy | Clasificación | Detalle |
|---|---|---|
| `MMEngineFn` — modelo de estado (`PendingMM` TTL 30s, stateless por request, output único `CoreCommand`) | **REPLACE** | El MM Futures vive como plugin dentro de `echo/operation` con `mm_state` duradero, checkpointeado con la recovery authority, decisiones multi-trigger. |
| `MMEngineFn` — patrones (join Account/Instrument snapshots, `SendAfter` para delays, egress per-account `echo.commands.{account}.v1`) | **ADAPT** | Reutilizados: join de snapshots para contexto MM; `SendAfter` → `DomainClock`; convención per-account reutilizada por la familia nueva `echo.order-commands.{account}.v1`. |
| `sdk/mm` calculators (`Calculator`, `fixed_lot`, `fixed_risk`, `CalculationInput/Result`) | **REUSE/EXTEND** | Primitivas puras unit-agnostic; se extienden a unidades instrument-spec (`TickValue/TickSize/ContractSize` ya presentes en `InstrumentSnapshot`). |
| `sdk/mm/pip_size.go` (`PipSizeCanonical`) | **LEGACY_ONLY** | Pips no entran al camino Futures; sin imports desde el path nuevo. |
| `ExecutionStoreFn` / `OpenExecution` | **REPLACE (autoridad) + compatibilidad** | Su modelo single-fill no representa Order 1→N Fill ni adds; sobrevive como proyección de compatibilidad del path legacy hasta retiro. |
| `CoreCommand` / `ExecutionResult` | **ADAPT (wire DTO) / LEGACY_ONLY** | Continúan en la path legacy; el camino nuevo usa `OrderRequest` y las cinco familias normalizadas. |
| `CloseHandlerFn` / `CloseCommand` / automation evaluator | **REUSE (safety plane)** | El flatten account-wide existente entrega `ForceClose` como intent al state owner; nunca es el `CLOSE_ALL` de Strategy. |

## 7. Instrument / Contract refactors

- Catálogos `Instrument`/`Contract`/`ContractIdentifier`/`InstrumentMapping` + `ExchangeCalendar`: **NEW_REQUIRED_FOR_V1** (no existen como dominio; `InstrumentSnapshot` legacy mezcla instrumento económico con símbolo físico de broker y no tiene expiry/session — gap D1 cerrado por diseño D2-05).
- Hot symbol mapping (`symbol_mapping_handler.go`, Gateway→Kafka compactado→cache): **REUSE/EXTEND patrón** para distribuir los nuevos catálogos (`echo.exchange-calendars.v1` etc. con tombstones).
- `InstrumentSnapshot`: REUSE como observación runtime; **no** source-of-truth de specs nuevas.
- No hay refactor bloqueante: el mapping legacy Forex/MT sigue operando sin cambios durante la coexistencia (`DT-EF-CROSS-MARKET-INSTRUMENT-02` revisa unificación post-freeze).

## 8. Calendar / session refactors

- `CalendarResolver` (`sdk/calendar` puro), `session_id=(calendar_id,session_date)`, `NamedTradingWindow`, `NextSessionTransition`: **NEW_REQUIRED_FOR_V1**.
- `DayBoundaryCache` + `prop_rulesets.daily_reset_*` (`account_sync.go@b0f8f1ce`): **REUSE concepto / ADAPT-REPLACE mecanismo** para Futures (R18): cache-forever + fallback UTC 23:00 + asunción "fase nueva ⇒ account_id nuevo" son incompatibles con re-binding in-place; el camino Futures usa config DayBoundary explícita hot/readiness-safe en `echo/provider_rules`, fail-closed (`DAY_BOUNDARY_UNRESOLVED` ⇒ `DENY_NEW_RISK`). El mecanismo legacy permanece para cuentas legacy.
- Fallback UTC 23:00: **prohibido en el camino Futures** (defecto si aparece), LEGACY_ONLY para el path actual.

## 9. Market Runtime gaps (mandato §16)

Distinguimiento aplicado: `NEW_REQUIRED_FOR_V1` (implementación prevista del diseño) ≠ `BLOCKING_REFACTOR_OF_EXISTING_ECHO` (no existe ninguno en esta área).

| Componente | Clasificación |
|---|---|
| `echo/market_stream` (authority/current/last-known/readiness) | NEW_REQUIRED_FOR_V1 |
| `echo/market_analytics` (forming/closed bars, grid, MTF) | NEW_REQUIRED_FOR_V1 |
| Feed adapters / candidates + contratos market-events/state/bars | NEW_REQUIRED_FOR_V1 |
| `DomainClock` (SDK library) | NEW_REQUIRED_FOR_V1 |
| `MarketHistorySource` seam | NEW_REQUIRED_FOR_V1 |
| `ReplayDriver` offline + RunManifest/ReplayAnchor/DeterministicInputLog | NEW_REQUIRED_FOR_V1 |
| StateFun/kache/`SendAfter`/OTel/egress transaccional patterns | REUSE |
| MMEngine join pattern → read-only MarketContext | ADAPT |
| Legacy MT feed/InstrumentSnapshot como autoridad de mercado | **DO NOT PROMOTE** (REPLACE_FOR_FUTURES: no adaptar Bridge MT feed como market-data authority; no vendor bars como bar authority) |
| Recording retention/archival, replay-from-midpoint, distributed replay, depth/book | DEFERRED (D2-06 §23) |

## 10. Provider domain gaps (mandato §17)

| Componente | Clasificación |
|---|---|
| `Provider` / `ProviderProgram` / `ProviderRuleSet` versionado / `ProviderAccountBinding` | NEW_REQUIRED_FOR_V1 |
| `echo/provider_rules(account_id)` (Stage-1 linearizado, capacity projection `firm_by_operation`+`live_reservations`, DayBoundary state, routing index) | NEW_REQUIRED_FOR_V1 |
| `CalendarResolver` (consumido por admission) | NEW_REQUIRED_FOR_V1 (ver §8) |
| `DayBoundaryCache` mecanismo | ADAPT/REPLACE para Futures (R18); legacy intacto |
| `echo.prop_rulesets` legacy shape | REPLACE para path Futures (sin program/version/provenance); legacy durante migración |
| AutomationEvaluator typed-evaluation pattern | REUSE patrón |
| `ClientConfig`/`AccountState` | REUSE input operativo (update debe llegar al owner account-keyed) |
| ProviderProgram "six-props config" de D5-M1A | **NO es requisito D2** — histórico; el RuleSet es typed families + params, sin DSL ni mega-enums |
| Cohorte ~6 props / rollout Topstep→Lucid→… | Dirección D6 (decisión owner 2026-09-28); **no** dependencia D2 |

## 11. Execution / Bridge gaps (mandato §18)

| Componente | Clasificación |
|---|---|
| Futures Bridge (proceso sibling) | **NEW V1 component** |
| `ExecutionAdapter` (componente interno transport-specific) | NEW V1 component |
| `SimExecutionAdapter` (primer path D2/D6 de implementación) | NEW V1 component |
| Journal M2 write-ahead (durability domain del side-effect owner) | **NEW V1 correctness component** |
| Real external adapter (ProjectX/NT/Tradovate/Rithmic/CQG candidate) | **D6** (OD-D2-07-1 cerrada: selección diferida a D6 con acceso autorizado) |
| Refactor del Bridge MT legacy | **NOT_REQUIRED** (`MT_ONLY` preservado: pipes/EA/ticket snapshots intactos; sin evidencia en contra) |
| Bridge patterns (sesión per-account, breaker, consumer, kache, telemetría) | REUSE (duplicación KISS en el sibling; sin bridge-framework) |
| Kafka consumer behavior nuevo (`read_committed`, commit tras outcome/journal) | ADAPT |

## 12. Persistence / projections (mandato §19)

Confirmado consistente con lo congelado (sin contradicción):

- **StateFun state = hot recovery authority** (checkpoints + replay ingress + egress transaccional). **Kafka transactional fact path = durable boundary** (`echo.operation-projections.v1`, misma frontera de checkpoint; R14). **PG = projection/query only**, jamás recovery authority ni decisión de Orders (R11/R14).
- `ExecutionStore` legacy = compatibility path (REPLACE como autoridad, retenido).
- `trade_journal`/`canonical_operations` = boundary analítico REUSE intacto; Operation→Trade diferido a The Lab.
- Sin event sourcing global, sin tablas de eventos, sin saga (R9 KISS). Post-terminal y late fills usan el mismo fact path durable (R13/R14).
- Migraciones PG nuevas (`operations`/`orders`/`fills`/`contract_positions`): NEW (implementación D5), numeración coordinada en vuelo.

## 13. Config / kache authority (mandato §20)

Contraste congelado y consistente: **kache/read model = visibilidad eventual, jamás authoritative acceptance.**

| Uso | Autoridad | kache rol |
|---|---|---|
| Provider admission Stage-1 | `echo/provider_rules(account_id)` (linearization point, R15) | prefilter/read model |
| Fan-out target set | isla `echo/signal_fanout` en su punto de procesamiento (D2-08 §8) | read model de la isla |
| Mapping Instrument→Contract | resolución única dentro de `echo/operation` al materializar (pin) | hot distribution |
| Calendar | dataset + resolver puro; readiness fail-closed | hot distribution (`echo.exchange-calendars.v1`) |
| Strategy config | config efectiva por ciclo; pinned activo + pending prospectivo (D2-08 §14) | distribución |
| MM config | pinneada en snapshot de Operation (D2-01) | distribución |

Ningún seam permite que visibilidad eventual sustituya a la autoridad: verificado en D2-05 R15, D2-08 §8, D2-04 R11.

## 14. Units / pips (mandato §15)

- **Limpio para D5 (ya congelado, falta implementar):** canon D2-05 §7 — `price` decimal, deltas en ticks/precio, `tick_size`/`point_value`/`tick_value` derivado, quantity en contratos con `qty_min/step`; sin pips como unidad universal. Extensión de `sdk/mm` a instrument-spec.
- **Permanece en legacy Forex/MT:** `pips`, `PipSizeCanonical`, `risk_pips` y todo el path Reference. No se fuerza limpieza repo-wide de Forex.
- **Aislamiento:** el camino Futures no importa `pip_size.go`; política de marcadores `DT-EF-*` en código para toda limitación temporal (regla del proyecto).
- **DT explícita:** la constraint V1 ya está congelada en el proyecto ("Unidades cross-market — constraint V1"); la limpieza legacy queda como **deuda candidata Iteración 2 con ID/alcance pendiente de ratificación owner** (estado ya registrado; no bloquea V1 ni abre `BLOCKED_OWNER_DECISION` para este gate). `DT-EF-UNITS-04` (pips FX vs ticks futures, deuda D1-A1) queda absorbida por este mismo carril Iteration 2.

## 15. Scale implications (mandato §21)

Ningún freeze D2 introduce estructuralmente `feed×account`, `bars×account`, `indicators×account` ni `strategy eval×account`:

- Market: una stream/builders/analytics por `stream_id`; account invisible al subscription engine (D2-06 §5/§24).
- Strategy: 1 evaluación por trigger; 1 indicator set; fan-out posterior (D2-08 §22).
- Costos N legítimos por naturaleza: decisiones MM por Operation; notificaciones de mercado hacia op keys que **declaran** ese requisito (opt-in, D2-08 §12); execution sessions N según transport (D2-07 §25).
- `ACCOUNTSTRATEGY_CYCLE_LAG` acota el backlog a un ciclo futuro diferido — sin crecimiento ilimitado por cuenta.
- Capacidad física (100–200 cuentas, throughput StateFun, reconnect storm, journal I/O, consumer-per-account) se **certifica en D6**; la topología no la impide estructuralmente (partición compartida keyed-by-account = cambio local de routing, no de boundary).

## 16. Classification matrix

Categorías: **A** NEW_REQUIRED_FOR_V1 · **B** ADAPT_REQUIRED_FOR_V1 · **C** REPLACE_REQUIRED_FOR_V1 · **D** D6_CERTIFICATION · **E** DEFERRED_MANDATORY_ITERATION_2 · **F** LEGACY_ONLY · **G** REMOVE_LATER.

| # | Gap / pieza | Categoría |
|---|---|---|
| 1 | SDK domain package puro (Operation/Order/Fill/enums/máquina de transiciones/guards, `MMPlugin`, `ExecutionEvent`, `SimExecution`) | A |
| 2 | `echo/signal_fanout`, `echo/operation`, `echo/operation_projector`, shape-replace position projection | A |
| 3 | `echo/strategy_engine` + `echo.signals.v1` + trigger contract | A |
| 4 | `echo/market_stream`, `echo/market_analytics`, feed contracts, `DomainClock`, `MarketHistorySource`, `ReplayDriver` + recording | A |
| 5 | Catálogos Instrument/Contract/Calendar + distribución hot | A |
| 6 | Provider domain + `echo/provider_rules` + capacity projection + routing index | A |
| 7 | Futures Bridge sibling + `ExecutionAdapter` + `SimExecutionAdapter` + journal M2 | A |
| 8 | Boundary/seam Core para futura compatibilidad `ReferenceEvent → Signal` | E — placement/contract congelado en D2; implementación del adapter + migración física = DT-EF-REFERENCE-SIGNAL-03 / Iteration 2 |
| 9 | Migraciones PG `operations/orders/fills/contract_positions` + projector materialization | A |
| 10 | Patrones `MMEngineFn` (join/SendAfter/egress per-account) → dentro de `echo/operation` | B |
| 11 | Patrón `ExecutionPlannerFn` → `echo/signal_fanout` (Signal, event-time) | B |
| 12 | Mecanismo DayBoundary → config hot explícita en `provider_rules` (R18) | B |
| 13 | kache/ConfigCache/symbol-mapping patterns → nuevos catálogos | B |
| 14 | Snapshot KVS (acc/inst) extendido con specs de Contract | B |
| 15 | Bridge patterns → duplicados/adaptados en el sibling; consumer `read_committed`/commit-tras-outcome | B |
| 16 | `ExecutionStoreFn` como autoridad | C (REPLACE autoridad; compat path retenido) |
| 17 | Estado `MMEngineFn`/`PendingMM`/`PendingPlanning` | C |
| 18 | `PositionSnapshot` MT ticket-shape → Position neta `(account, contract)` | C |
| 19 | `prop_rulesets` legacy shape → `ProviderRuleSet` versionado | C (sólo path Futures) |
| 20 | `ExecutionResult` single-result → cinco familias normalizadas | C |
| 21 | Journal EA post-side-effect → journal M2 write-ahead | C |
| 22 | Fallback UTC 23:00 DayBoundary | C (prohibido en Futures path) |
| 23 | Config egress EXACTLY_ONCE + `read_committed` + transaction timeout + retentions | D |
| 24 | Selección/implementación/certificación M2 del transport externo real + entitlement/host | D |
| 25 | Benchmarks: 100–200 cuentas, throughput StateFun/tick, reconnect storm, journal I/O, latency admission/reservation | D |
| 26 | Certificación ReplayDriver con golden recording + decision log | D |
| 27 | Store físico del journal M2 (fsync/corruption semantics) | D |
| 28 | Retention de `echo.operation-projections.v1` y recording horizon; lag del projector | D |
| 29 | Disciplina determinista de implementación (sin iteración de colecciones no ordenada en decisiones; sin `time.Now()` en dominio; assertions live/replay) | D (verificación) |
| 30 | `DT-EF-REFERENCE-SIGNAL-03` migración completa reference path | E |
| 31 | `DT-EF-FX-PROP-01` provider rules para props Forex | E |
| 32 | Limpieza pips legacy (ID/alcance pendiente ratificación owner, ya registrada) | E |
| 33 | `DT-EF-CROSS-MARKET-INSTRUMENT-02` revisión unificación Instrument/binding | E |
| 34 | `DT-EF-POSITION-RECONCILIATION-05` | E (DEFERRED_EDGE_CASE; reabrir con evidencia) |
| 35 | Recording archival/object storage; replay-from-midpoint; distributed replay; depth/book | E |
| 36 | `ReferenceEvent`/`CoreCommand`/`ExecutionResult`/`CloseResult`/`ExecutionPolicy` como contratos legacy; Bridge MT/pipes/EA; `PendingMM`/`PendingPlanning`; `pip_size.go`; `DayBoundaryCache`+UTC fallback (path legacy); `trade_journal`/`canonical_operations` como boundary analítico | F |
| 37 | Cleanup legacy V1/V2 source/docs | G |

`BLOCKING_ARCHITECTURE`: **ningún ítem**.

## 17. Mandatory Iteration-2 debts

Deuda explícita (ya registrada en authorities; consolidada aquí como no bloqueante):

1. `DT-EF-REFERENCE-SIGNAL-03` — migración del execution path reference al boundary canónico y retiro del coupling legacy.
2. `DT-EF-FX-PROP-01` — enforcement de provider rules para las props Forex actuales de Echo (first-party rules + mismo enforcement).
3. Limpieza pips legacy — deuda candidata; ID/alcance pendiente ratificación owner (absorbe `DT-EF-UNITS-04`).
4. `DT-EF-CROSS-MARKET-INSTRUMENT-02` — evaluar si el split Instrument→Contract sustituye/enriquece el mapping Forex/CFD.
5. `DT-EF-POSITION-RECONCILIATION-05` — política de divergencia lógico↔físico (sólo con evidencia real).
6. Recording archival/retención extendida, replay desde midpoint, replay distribuido, depth/book (D2-06 §23).
7. Cleanup legacy V1/V2 y retiro futuro de compatibility paths (ExecutionStore, prop_rulesets, DayBoundaryCache legacy) cuando el path legacy se retire.
8. Nota de migración de identidades: si una iteración futura extiende EXACT_REPLAY al dominio de ejecución, `operation_id`/`order_id`/`decision_id` migran a `DeterministicDomainID` (§4.2/§4.3).

## 18. D5/D6 implementation obligations

**D5 (Foundations):**
- Construir las superficies A (ítems 1–9 de la matriz) sobre los patrones REUSE/B congelados.
- Declarar en `module.yaml` los egress nuevos con `EXACTLY_ONCE` + transaction timeout ≤ broker `transaction.max.timeout.ms`; consumers de comandos con `read_committed`; producer idempotente con in-flight limitado (orden por key).
- Domain package puro sin imports de Kafka/StateFun/PG/wall clock (boundary Q14); `DomainClock` obligatorio.
- Migraciones PG + projector idempotente/stale-safe por `operation_event_seq`; retention del topic de proyecciones dimensionada.
- Acceptance determinismo: fixtures live/replay de Signals (`signal_id` estable), guards idempotentes, casos D2-04 A–F/D2-06 A–L/D2-07 A–L/D2-08 A–L como suite de regresión.

**D6 (Multi-Prop E2E + Scale):**
- Selección del primer transport externo real **con acceso autorizado efectivo** y cierre de sus gates M2 (customTag retention, ambiguous-submit atomicity, negative/recovery semantics, execution identity, history horizon) + entitlement/host (Topstep: dispositivo personal, sin VPS/relay).
- Certificación física de la config EXACTLY_ONCE/read_committed declarada en D5 (carry D2-04 R2 / D2-06 R-D2-06-5 / D2-08 R2).
- Benchmarks de capacidad y presión (ítems 25/28), certificación ReplayDriver con golden (ítem 26), store del journal con fsync/corruption semantics (ítem 27).
- Cierre E2E shadow/demo/sim autorizado; requisitos V1 de transport real y 200-account capacity demo se pagan aquí.

## 19. Q16 closure

```text
Q16 = CLOSED

Criterio 1 — cada gap D1/D2 → decisión explícita:
  CUMPLE (matriz §16: 37 ítems clasificados A–G; cero sin clasificar).

Criterio 2 — ninguna capacidad requerida para V1 depende
silenciosamente de una pieza legacy incompatible:
  CUMPLE — toda pieza legacy incompatible tiene reemplazo explícito
  en el camino Futures (C: ítems 16–22) o está confinada a LEGACY_ONLY (F);
  el único acoplamiento permitido es por patrones REUSE/ADAPT declarados.
  El camino canónico Futures no consume ReferenceEvent/ExecutionPlanner/
  MMEngine/ExecutionStore/PositionSnapshot/prop_rulesets/DayBoundaryCache
  para ninguna de sus capacidades (verificado contra D2-04..08 §9/§21/§23).

BLOCKING_ARCHITECTURE: NONE — no existe gap que impida construir V1
con los seams congelados; todo "gap" restante es implementación prevista
(categoría A) o certificación (D).
CORE REWRITE: NOT_REQUIRED (Q1 owner-accepted y re-confirmado).
```

La hipótesis manager queda **confirmada tras desafío**: la refutación buscó (a) contradicción source-vs-boundary (module.yaml sin EXACTLY_ONCE: no es contradicción de diseño, es config required declarada por las propias autoridades; `time.Now()` en planner legacy: no promovido; DayBoundary cache-forever: reemplazo acotado ya congelado), (b) dependencia silenciosa del camino Futures en legacy (no existe: §19 closure criterio 2), (c) identidad aleatoria en output determinista (no existe: §4). Ninguna refutación prosperó.

## 20. Residual risks

1. **La corrección config (EXACTLY_ONCE etc.) es requisito, no comportamiento actual:** si D5 despliega sin declarar las delivery semantics, las garantías M1/journal/signals **no existen**. Mitigación: obligations §18-D5 + acceptance D6 ítem 23.
2. **M2 vendor evidence:** ningún transport tiene hoy M2 probado físicamente; la clase MARKET sin history-by-tag/idempotencia nativa queda `UNSUPPORTED_FOR_V1_EXACT_SUBMISSION`. Riesgo de schedule D6 si el transport elegido no cierra gates.
3. **Throughput StateFun con triggers granulares** (carry R-D2-06-1): mitigación congelada es migración de topología sin cambio de contratos; benchmark D6 puede forzar esa migración temprana.
4. **Determinismo de implementación:** la disciplina (colecciones ordenadas, sin wall clock) es verificable sólo con suites; un defecto aquí no aparece en diseño sino en QA — cobertura de casos A–L de D2-04..08 como regresión permanente.
5. **Deuda pips sin ID ratificado:** la ratificación owner del ID/alcance de limpieza legacy sigue abierta por registro previo; no afecta V1 pero debe cerrarse antes de Iteración 2 para no acumular deuda sin dueño.
6. **Coexistencia de caminos:** durante la migración conviven path legacy y nuevo; el riesgo de drift de patrones duplicados (R12 D2-07) se mitiga con la regla de re-extracción al tercer consumidor.

## Fuentes

- [[Echo Futures]] — decisiones owner D2-01..03, cierres D2-04..D2-08, rollout D6, Q gate.
- [[Echo Futures — D1 Analysis Pack]] — register §6, matriz Q1, deuda no bloqueante.
- [[Echo Futures — D2-04 Operation Order Fill Position]] — §2.1 identidades, §5.1/5.6 idempotencia, §9 reuse map, R1–R14.
- [[Echo Futures — D2-05 Instrument Session Provider]] — §7 unidades, §11 DayBoundary, §21 reuse map, R15–R18.
- [[Echo Futures — D2-06 Market Runtime]] — §15/§16/§18 identidades/journal, §19 EXACT_REPLAY, §23 reuse map, OD-C1.
- [[Echo Futures — D2-07 Execution Runtime]] — §3 R1 identity, §5/§23 sibling/reuse, §24 gates D6, OD-D2-07-1.
- [[Echo Futures — D2-08 Strategy Runtime]] — §5/§6 signal identity, §10 MM, §21 reuse map, correcciones manager.
- `xKoRx/echo@372af59a7b83604781346613da01e3d510ea1360` — spot-checks: `module.yaml` (egress sin delivery semantics), ausencia `type Signal` en `v3/`, `v3/sdk/utils` `GenerateUUIDv7`, `v3/sdk/mm/pip_size.go`.

## Handoff

```text
D2-09 STATUS:
MANAGER_CLOSED

Q16:
CLOSED

Q16 ARTIFACT:
main/10-projects/Echo Futures/Echo Futures — D2-09 Blocking Refactors.md

ARCHITECTURE CANDIDATE:
main/10-projects/Echo Futures/Echo Futures Architecture Candidate V1.md

AGENTS-OS BASELINE:
5af8e18fb4da0464105985c2dc5310c98869d1c5 (≥ mínimo 2c4bc4fd)

FINAL AGENTS-OS SHA:
ed628b02a37fccf59430b19afb8ca5e9c0d0f164 (HEAD persistido al cierre; los
artefactos quedaron absorbidos por los sync commits 29d0847c/ee551ccb/ed628b02)

ECHO BASELINE:
372af59a7b83604781346613da01e3d510ea1360 (fetch sin delta; spot-checks puntuales)

EXECUTIVE VERDICT:
Q16 CLOSED sin BLOCKING_ARCHITECTURE; CORE REWRITE NOT_REQUIRED.
Register D1 reconciliado a 37 ítems A–G; superficies nuevas = implementación
prevista D5/D6, no refactors bloqueantes de Echo. Identidades auditadas:
signal_id determinística (D2-08); operation_id/order_id UUIDv7 se mantienen
como identidades de ejecución LIVE fuera del boundary EXACT_REPLAY V1
(demostrado §4.2), con propiedad + familia DeterministicDomainID congeladas
para toda identidad futura en output determinista. EXACTLY_ONCE egress =
IMPLEMENTATION_REQUIRED (module.yaml no lo declara hoy). ReferenceSignal
migration = DEFERRED_MANDATORY Iteration 2 sin dependencia de V1.

CORE REWRITE:
NOT_REQUIRED

REPLAY-STABLE IDENTITY DECISION:
signal_id = DeterministicDomainID(run, strategy, eval_seq, signal_seq) — ya
congelada. operation_id/order_id/decision_id/action ids = LIVE-IRREPEATABLE
(UUIDv7) fuera del replay boundary V1; correctness por M1 2PC + M2 journal;
estabilidad intra-vida de client_order_id es requisito M2. Propiedad congelada:
identidad generada que participe de output determinista debe ser replay-stable.

NEW_REQUIRED_FOR_V1:
domain package puro; echo/{operation,signal_fanout,operation_projector,
strategy_engine,market_stream,market_analytics,provider_rules}; DomainClock;
MarketHistorySource; ReplayDriver+recording; catálogos Instrument/Contract/
Calendar; provider domain; Futures Bridge sibling + ExecutionAdapter +
SimExecutionAdapter + journal M2; migraciones PG. El adapter físico ReferenceEvent→Signal NO es obligación V1 Futures (Iteration 2).

ADAPT_REQUIRED_FOR_V1:
patrones MMEngineFn (join/SendAfter/egress per-account); ExecutionPlannerFn→
signal_fanout; DayBoundary mechanism→hot config provider_rules (R18);
kache/symbol-mapping patterns→catálogos; snapshot KVS+Contract specs; Bridge
patterns→sibling; consumer read_committed/commit-tras-outcome.

REPLACE_REQUIRED_FOR_V1:
ExecutionStore (autoridad; compat retenido); PendingMM/PendingPlanning;
PositionSnapshot ticket→Position neta (account,contract); prop_rulesets shape
(path Futures); ExecutionResult→5 familias; journal EA→M2 write-ahead;
fallback UTC 23:00 (prohibido en Futures).

D6_CERTIFICATION:
EXACTLY_ONCE/read_committed config; transport externo real (selección+M2+
entitlement/host); benchmarks 200 cuentas/throughput/reconnect/journal;
ReplayDriver golden; journal store fsync; retentions+projector lag;
disciplina determinista de implementación.

DEFERRED_ITERATION_2:
DT-EF-REFERENCE-SIGNAL-03; DT-EF-FX-PROP-01; limpieza pips (ID owner pending);
DT-EF-CROSS-MARKET-INSTRUMENT-02; DT-EF-POSITION-RECONCILIATION-05;
recording archival/midpoint/distributed/depth; cleanup legacy; nota migración
de identidades si replay de ejecución se extiende.

LEGACY_ONLY:
ReferenceEvent/CoreCommand/ExecutionResult/CloseResult/ExecutionPolicy;
Bridge MT/pipes/EA; PendingMM/PendingPlanning; pip_size.go;
DayBoundaryCache+UTC fallback (path legacy); prop_rulesets legacy;
trade_journal/canonical_operations (boundary analítico).

Q GATE:
Q2 CLOSED · Q3 CLOSED · Q4 CLOSED · Q5 CLOSED · Q6 CLOSED · Q7 CLOSED ·
Q8 CLOSED · Q9 CLOSED · Q10 CLOSED · Q11 CLOSED · Q14 CLOSED ·
Q15 DEFERRED_TO_THE_LAB_BY_OWNER · Q16 CLOSED (Q12/Q13 → D4)

D2 STATUS:
MANAGER_CLOSED

OWNER DECISIONS REQUIRED:
NONE

MATERIAL RISKS:
config EXACTLY_ONCE es requisito no comportamiento; M2 vendor sin evidencia
física hoy (MARKET sin history-by-tag queda gated); throughput StateFun carry;
determinismo de implementación verificable sólo por suites; deuda pips sin ID
ratificado; drift de patrones duplicados legacy/nuevo durante coexistencia.

NEXT:
Primary Manager review only.
Do not start D3/Astra.
```

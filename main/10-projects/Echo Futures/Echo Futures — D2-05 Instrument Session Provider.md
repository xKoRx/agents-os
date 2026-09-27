---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D1 Analysis Pack]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
  - "[[Echo Futures — D2-05A Instrument Contract]]"
  - "[[Echo Futures — D2-05B Session Calendar]]"
  - "[[Echo Futures — D2-05C Provider Program Rules]]"
aliases:
  - Echo Futures D2-05
  - EF Instrument Session Provider
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-design
created: "2026-09-26"
updated: "2026-09-26"
---

# Echo Futures — D2-05 Instrument / Session / Provider (Integrated Candidate)

> [!info]+ Integration Scribe
> Candidato integrado por el TOP worker de D2-05B actuando como **D2-05 Integration Scribe** (no es un cuarto TOP). Inputs exclusivos: [[Echo Futures — D2-05A Instrument Contract]] (`READY_FOR_INTEGRATION`, blob `6eb671f2`), [[Echo Futures — D2-05B Session Calendar]] (`READY_FOR_INTEGRATION`, blob `8058aec0`), [[Echo Futures — D2-05C Provider Program Rules]] (`READY_FOR_INTEGRATION`, blob `637c62b8`), más las decisiones congeladas [[Echo Futures]] D2-01..03 y [[Echo Futures — D2-04 Operation Order Fill Position]] (R1–R14). Verificación física: los tres blobs observados en HEAD `76836cae` del vault coinciden exactamente con los aprobados por el SUBMANAGER (sin input drift); baseline Echo re-verificada `origin/master = 372af59a7b83604781346613da01e3d510ea1360` (fetch, sin delta). Este archivo REEMPLAZA completamente el draft autoescrito invalidado; ninguna conclusión proviene de él. No implementa código, no cierra D2-05, no avanza a D2-06.

## 1. Executive verdict

```text
D2-05 INTEGRATION STATUS: READY_FOR_SUBMANAGER_REVIEW
```

La integración de A+B+C produce una arquitectura única y legible sin agregar una cuarta capa ni resolver contradicciones por invención: **A aporta la identidad económica y su resolución física** (Instrument canónico → Contract expiry-specific pinneado una vez por Operation, con mapping hot por binding y external identifiers por fuente); **B aporta la autoridad temporal de mercado** (ExchangeCalendar como dataset owner-managed + resolver puro en proceso, session/trade date como dato, ventanas nombradas para Strategy, account day separado); **C aporta la autoridad de negocio/reglas** (Provider → ProviderProgram → (fase opcional provider-local) → ProviderRuleSet versionado, binding en la Account, enforcement en dos gates + plano safety asíncrono). D2-04 conserva íntegro el ownership del lifecycle: la Operation sigue materializándose antes de MM, la terminación sigue exigiendo guards, y ningún gate provider cambia un solo estado del aggregate.

Los tres seams cruzados quedaron cerrados y congelados en los repairs A-R1/A-R2, B-R1/B-R2 y C-R1..C-R5, y esta integración los verifica compatibles sin reabrirlos: (1) `Instrument.calendar_ref → calendar_id` es el único binding runtime hacia el CalendarResolver — el resolver no recibe `product_group` ni `exchange`, y `product_group`/`exchange` son llaves de reglas de C, no de sesión; (2) `session_id = (calendar_id, session_date)` es unívoco por construcción (un calendario = una semántica de producto/sesión); (3) las primitivas que C consume de B son exactamente `SessionState/SessionDate/SessionBoundaries/NextSessionTransition` por `calendar_id` — B jamás publica provider policy; (4) la reserva de exposición vive en un segundo state owner (`echo/provider_rules`, key `account_id`) coordinado por protocolo checkpoint-atómico con `echo/operation` (key `account_id:account_strategy_id`), sin fusionar owners.

`OWNER DECISIONS REQUIRED: NONE` — los tres TOPs lo declaran y la integración no descubrió contradicción nueva que lo cambie. Quedan ratificaciones técnicas ordinarias del manager (nombres físicos de functions/topics/tablas, enums de reason, campos aditivos de provenance), listadas en §24. La integración NO es PASS ni CLOSED: el SUBMANAGER decide el siguiente gate.

## 2. Minimal entity model

| Entidad | Autoridad | Una línea |
|---|---|---|
| `Instrument` | A | Identidad económica/canónica: `instrument_id`, `quote_currency`, `exchange` (metadata/reglas), `product_group` (único agrupador de caps/reglas C), `calendar_ref` (único binding runtime hacia B). Sin taxonomía adicional. |
| `Contract` | A | Contrato listado expiry-specific tradable: `contract_id`, año/mes, `tick_size`, `point_value` (`tick_value` derivado), `qty_min/step`, `active`. Hereda exchange/grouping de su Instrument; no duplica nada. |
| `ContractIdentifier` | A | External identifier por `(contract_id, source, context)`; `source` es namespace de adapter/transporte, jamás identidad Provider. |
| `InstrumentMapping` | A | Fila corriente `(mapping_context, binding_id, instrument_id) → contract_id`; hot; `MARKET_DATA` (feed) y `EXECUTION` (Account vía `execution_binding_id`) por separado. |
| `ExchangeCalendar` | B | Dataset owner-managed: `calendar_id` (= una semántica completa de producto/sesión), tz IANA, `weekly_base` + overrides fechados (`HOLIDAY_CLOSED/EARLY_CLOSE/SPECIAL_SESSION`), `calendar_version` + `revision_hash`. |
| `NamedTradingWindow` | B | Config referenciable por `window_id` (`EXCHANGE_SUBSET` sobre un calendario, o `CLOCK` en tz propia); Strategy referencia id, nunca offsets. |
| `Provider` | C | Owner de negocio/policy de la firma; NO transport. |
| `ProviderProgram` | C | Producto real de la firma; punto de anclaje estable de reglas y bindings. |
| `ProviderRuleSet` | C | Única pieza con version/provenance explícita: familias tipadas de reglas por `(provider, programa[, fase])`; UNKNOWN jamás es ALLOWED. |
| `ProviderAccountBinding` | C | Config corriente de la Account (1:1): provider, programa, `phase?`, autoridad RuleSet resuelta, transporte+entitlement, `day_boundary` reference. |
| `Operation/Order/Fill/Position` | D2-04 | Aggregate por `account:strategy`; lifecycle congelado; Position física neta `(account, contract)`. |
| `AccountStrategy` | D2-01..03 | `Account + Strategy + MoneyManagement`, intacto; el binding provider es de la Account, no del AccountStrategy. |
| Resolvers de dominio | B/A | `sdk/calendar` (resolver puro, dataset inyectado) y resolución Instrument→Contract→identifier; paquetes Go puros sin infra (boundary Q14). |
| State owners | D2-04+C | `echo/operation` (key `account_id:account_strategy_id`), `echo/signal_fanout` (key `strategy_id`), `echo/provider_rules` (key `account_id`) — tres funciones StateFun con keys distintas; jamás se fusionan. |

## 3. Identities + cardinalities

```text
Instrument 1 → 0..N Contract                     (identity: contract_id)
Contract 1 → 0..N ContractIdentifier             (identity: (contract_id, source, context); inversa única)
Instrument 1 → 0..N InstrumentMapping            (identity: (mapping_context, binding_id, instrument_id))
Instrument 1 → 1 ExchangeCalendar (resoluble)    (vía calendar_ref; Futures V1 fail-closed)
ExchangeCalendar 1 → 1 sesión por trade date     (session_id = (calendar_id, session_date))
Provider 1 → 0..N ProviderProgram                (program N → 1 provider)
(programa[, fase]) → ≤1 ProviderRuleSet efectivo (cero efectivos ⇒ DENY_NEW_RISK fail-closed)
Account 1 → 0..1 ProviderAccountBinding activo   (re-binding = reemplazo in-place + audit facts)
AccountStrategy → Operation: 1 → 0..1 no terminal (D2-02)
Operation → Order → Fill: 1 → 0..N → 1 → 0..N    (D2-04)
Account+Contract → Position: 1 → 0..1 neta       (D2-04 R8)
```

Invariantes de identidad integrados: una Operation es **mono-contract** (todo su ciclo sobre el contract pinneado); `contract_id` es identidad interna Echo, nunca un ID universal de vendor (C-E08); current-Contract selection ≠ vendor external-identifier selection (dos resoluciones secuenciales, jamás fusionadas); la identidad del binding de calendario es 1:1 Instrument→calendar_id, sin dimensión de grupo dentro del calendario.

## 4. Instrument / Contract / external identifiers

De A final, sin cambios: `Instrument` porta las cinco llaves del modelo (`instrument_id` AUTHORITY; `quote_currency` CONFIG; `calendar_ref` CONFIG→calendar_id única referencia runtime de sesión, obligatoria y resoluble para todo Instrument Futures habilitado — falta ⇒ `CALENDAR_UNRESOLVED` fail-closed, sin default 24×7; `exchange` y `product_group` AUTHORITY config-of-record para reglas/onboarding de C, ajenos al resolver). `Contract` porta identidad de expiración explícita + specs económicas config-of-record (`tick_size`, `point_value`, `tick_value` derivado para eliminar la clase de inconsistencia, qty rules) + `active` operacional; **sin lifecycle timestamps autoritativos en V1** (C-E07: autoridad desconocida, deuda explícita del backtester futuro). `ContractIdentifier` resuelve el string literal del vendor por `(source, context)`; `source` es la config declarada de un adapter/fuente (mismo namespace que los adapters D6), nunca Provider. Los identifiers no participan del mapping; se resuelven en un segundo paso local al consumidor que conoce su `source`; identifier ausente para el `(source, context)` requerido = fail-closed.

## 5. Contract mapping + binding contexts

Mapping hot con identidad por binding concreto: `(mapping_context, binding_id, instrument_id) → contract_id`. Varios bindings de feed (`MARKET_DATA`: `databento-main`, `databento-backup`) y varios de ejecución (`EXECUTION`: `projectx-topstep`, `nt-kronos`) coexisten por instrumento, cada uno con su Contract corriente propio y rolando en momentos distintos. Ownership: la fila es del mapping; la definición del binding pertenece a su consumidor — `MARKET_DATA` a la config del runtime de mercado, `EXECUTION` a la config de la Account (`Account.execution_binding_id`, territorio Account/transport D2-04+C). Cadena completa por lado: market runtime resuelve `Instrument + market-data binding → current Contract` y después `Contract + source → external identifier (MARKET_DATA)` para suscribir; la materialización resuelve `Instrument + Account.execution_binding_id → current Contract` (pin + specs embebidas en el snapshot D2-04) y después `Contract + source (del adapter) → external identifier (EXECUTION)` para operar. Dos cuentas con bindings distintos pueden pinnear Contracts distintos para el mismo instrumento; las Positions quedan netas por `(account, contract)` y no interactúan. Resolución exactamente una vez, dentro de `echo/operation` en las guards de materialización; después de CREATED ningún path consulta el mapping (pin + specs viven en el estado del aggregate); hot path sin I/O (kache).

## 6. Hot manual rollover semantics

Congelado de A: owner-manual, hot, **estrictamente prospectivo**. Toda Operation nueva resuelve el mapping corriente de su execution binding al materializarse y pinnnea el resultado; un hot update posterior afecta sólo materializaciones futuras. OPEN/add/REDUCE/CLOSE sobre una Operation viva usan siempre el Contract pinneado, aunque el mapping corriente haya rolado. REDUCE/CLOSE sobre contrato viejo usa el Contract pinneado + su identifier corriente; si el venue lo rechaza (contrato expirado/inactivo) la Order queda `REJECTED` fail-visible y MM/safety plane deciden — **nunca silent remap, nunca auto-roll, nunca auto-migración, nunca synthetic order sobre el contrato nuevo**. Mapping eliminado con Operation viva: la Operation existente no se ve afectada (nada la re-resuelve); las materializaciones nuevas cuya fila falte fallan la guard (`CONTRACT_RESOLUTION_FAILED`, sin Operation). El rollover de exposición es procedimiento operacional owner (cerrar la Operation vieja + abrir la nueva); Echo no automatiza ni sugiere. La raza en el borde del rollover es determinística por construcción: cada materialización resuelve con el estado commiteado que tenga el kache del state owner en ese momento, con telemetría de config-change.

## 7. Economic unit semantics

Canon V1 para MM: `price` (decimal, `quote_currency`); deltas en **ticks** o precio absoluto; `tick_size` / `point_value` / `tick_value` derivado (Contract); `quantity` en **contratos** enteros con `qty_min/step`. P&L/exposición monetaria por Operation = Σ fills firmados × Δpuntos × `point_value` en `quote_currency`; **pips eliminados del camino nuevo** (confined al path legacy Reference). Las specs económicas que Echo usa son config-of-record inicializada de evidencia venue/exchange; el venue es autoridad de lo que ejecuta; `InstrumentSnapshot` (venue-observado) es observación runtime, no fuente de specs. Cross-check de specs venue-vs-config al conectar: mismatch fail-visible, sin auto-corrección. Seam declarado (no diseñado aquí): conversión FX para cuentas en moneda ≠ `quote_currency` — bloqueante de sizing fixed-risk en MM, no de este modelo.

## 8. ExchangeCalendar / ExchangeSession

De B final: el calendario es **datos + un resolver puro**, no un engine. UN `ExchangeCalendar` = UNA semántica completa de producto/sesión (`calendar_id`); dos productos con semánticas distintas = dos calendar_id (NQ/MNQ comparten `CME_EQ_INDEX` vía `calendar_ref`). Shape: `timezone` IANA; `weekly_base[]` (recurrencia semanal con `trade_date_shift`); `overrides{}` fechados por civil date local de inicio de sesión (`HOLIDAY_CLOSED | EARLY_CLOSE | SPECIAL_SESSION`, con `session_date` explícito y `corrected_at`); `calendar_version` monotónico + `revision_hash` del snapshot. Precedencia congelada: override fechado > weekly base > `CLOSED(NO_SESSION)` fail-closed. Sesión = `[open, close]` con `breaks[]` internos opcionales (los gaps de maintenance CME son huecos entre sesiones, no breaks); una sesión por trade date en V1. Resolver puro `sdk/calendar` sin I/O, dataset inyectado: `SessionState(calendar_id, instant) → OPEN|BREAK|CLOSED`, `SessionBoundaries`, `NextSessionTransition`; sin `product_group` ni `exchange` ni provider timezone en la firma. Distribución hot: PG source-of-truth → Gateway → topic compactado `echo.exchange-calendars.v1` (patrón symbol-mapping con tombstone) → kache; readiness fail-closed (`CALENDAR_NOT_READY`). El exchange availability recorta todo: barras, ventanas de Strategy y (vía C) evaluación de ventanas provider.

## 9. Session/trade date

Cuatro conceptos de tiempo jamás colapsados: `instant` (UTC RFC3339Nano, event-time del evento/Core), `civil_local_date` (derivado IANA), `session_date`/trade date (**dato de la sesión** vía `trade_date_shift`/override — Sunday 17:00 CT → lunes; sin fórmula universal CME), `account_day` (reset horario del ruleset de la cuenta, autoridad separada §11). Cadena: event instant → `calendar_ref` del Instrument → wall clock en tz del calendario → sesión contenedora (precedencia §8) → `session_date`. `session_id = (calendar_id, session_date)` unívoco por construcción (repair B-R1: un calendario no puede expresar dos semánticas). Instante en break interno → `BREAK` con session_date de la sesión contenedora; entre sesiones → `CLOSED(no_session)`, sin session_date, nada fabrica bucket (métrica `EVENT_OUTSIDE_SESSION`). Time authority: IANA-only, tzdata embebida por release (cubre Windows Kronos), prohibido offset fijo en cualquier capa nueva.

## 10. Named Strategy windows

`NamedTradingWindow` = config pura referenciable por `window_id` (`"NY_OPEN"`, `"LONDON"`, `"CME_RTH"`, custom), dos kinds: `EXCHANGE_SUBSET` (recorta sesiones de un calendario; hereda feriados/early closes por construcción) y `CLOCK` (ventana de reloj en tz IANA propia, opcionalmente por weekdays). La Strategy referencia `window_id` en su config — cero offsets hardcodeados. Disponibilidad efectiva = `window_open ∧ exchange_session_open(contract del Instrument)`: el exchange cerrado gana siempre; una ventana que excede availability se recorta con warning de validación de config. El StrategyEngine entrega `WindowContext {window_open_utc, window_close_utc, window_date, session_date?, session_state}`; las transiciones se derivan exclusivamente de `NextSessionTransition` (timers calculados, nunca hardcodeados). S1 (NY Opening Range 30m) resuelve con `NY_OPEN` (CLOCK 09:30–10:00 ET) ∩ sesión CME del NQ.

## 11. Provider overlays vs ExchangeSession vs Account DayBoundary

Tres autoridades separadas por congelación (S-E06/S-E07/S-E08), demostradas con Topstep (flat 3:10 PM CT con NQ abierto hasta 4:00 PM CT):

| Autoridad | Dueño | Define | Nunca |
|---|---|---|---|
| **ExchangeSession/Calendar** | B (dataset + resolver) | cuándo el exchange/producto acepta negociación; session/trade date; boundaries de barras | provider policy; reset de cuenta; no muta por overlays |
| **ProviderProgram overlay** | C (ProviderRuleSet) | allowed-new-risk window, forced-flat cutoff (tz IANA del provider), holiday/early-close policy del programa; combina opcionalmente `SessionBoundaries` de B | no escribe el calendario; no define session_date; `Exchange OPEN ∧ Provider DENY_NEW_RISK` es estado representable por construcción |
| **Account DayBoundary** | dominio de cuenta (Echo V3: `prop_rulesets.daily_reset_timezone/time` + `DayBoundaryCache`) | reset diario contractual: daily HWM, prev_day_close, acumuladores provider diarios (C los resetea al cruzar el boundary, caso F) | no es ExchangeSession; no cambia Contract ni trade/session date; el fallback UTC-23:00 legacy está prohibido para cuentas Futures (day boundary explícito exigido, fail-closed) |

## 12. Provider / ProviderProgram / optional Phase / ProviderRuleSet

De C final: `Provider` es identidad canónica de la firma como **policy owner** (no ProjectX/NinjaTrader/Tradovate/Rithmic/CQG — esos son transports con entitlement separado). `ProviderProgram` es el producto real (Trading Combine, Express Funded, LucidDaily); las diferencias de reglas viven en el RuleSet, no en columnas del programa; prohibidos enums artificiales de tipo de programa. **Fase = dimensión opcional provider-local**: el corpus no demuestra ningún caso de mismo programa + fase distinta con reglas operativas materialmente distintas (Combine/XFA/Live Funded son programas distintos; TradeDay Sim/Live comparten reglas runtime); el binding porta `phase` sólo para programas que declaren fases con evidencia first-party; fase no declarada ⇒ fail-closed; `ProviderDecision.phase` es nullable. `ProviderRuleSet` es la única entidad con version/provenance obligatoria: `rule_set_id`, `(provider, programa[, fase])`, `version` monotónica, `ACTIVE|SUPERSEDED`, `effective_at`, `source_refs` obligatorias (sin provenance la versión no se activa), payload tipado de familias (§ de C: allowed new-risk window, forced-flat cutoff, permitted instruments, PER_ORDER, caps compartidos, daily loss, trailing, automation entitlement, copy claim-by-claim, overnight/weekend, news, consistency warn-only, payout/administrativas fuera del runtime), `reset_semantics` tipado. Sin versión efectiva ⇒ `DENY_NEW_RISK{NO_RULESET_AUTHORITY}`. `UNKNOWN` jamás significa ALLOWED. Principios transversales: las salidas (REDUCE/EXIT/CLOSE) jamás se bloquean; sin liquidación inventada (flatten sólo con regla tipada que lo declare — corpus V1: ninguna por defecto); caps preventivos para órdenes nuevas, breach pasivo por mercado = fail-visible.

## 13. Account binding + execution transport separation

`ProviderAccountBinding` (config corriente de la Account, 1:1, reemplazo in-place + audit facts, sin framework de versiones — C-R1 R5): `account_id`; `provider_id + program_id (+ phase? declarada)`; `rule_set_id + rule_set_version` (provenance de la autoridad resuelta, hot); `transport {transport_id: PROJECTX|NINJATRADER_BRIDGE|TRADOVATE_API|RITHMIC|CQG|SIM_EXECUTION, entitlement: ALLOWED|CONDITIONAL|FORBIDDEN|UNKNOWN, conditions[]}`; `day_boundary` (referencia a la autoridad de reset de la cuenta); `enabled`. **AccountStrategy permanece exactamente `Account + Strategy + MoneyManagement`**; el binding es de la Account y todas sus AccountStrategies comparten la autoridad provider. Separaciones congeladas: platform support ≠ API entitlement (Lucid soporta NT/CQG/Rithmic sin entitlement direct-API conocido); entitlement UNKNOWN/FORBIDDEN ⇒ binding no habilitable para automatización y, si deviene en caliente, semántica de revocación (§16); `AccountState` de Echo (ACTIVE/CLOSE_ONLY/INACTIVE) es autoridad independiente que se conjunciona con la admisión provider (`AcceptsOpens() ∧ provider_admission == ALLOW`), sin fusionarse.

## 14. Integrated OPEN/materialization flow

```text
Strategy (evalúa cuando window ∩ exchange availability OPEN)
  ↓ Signal{instrument_id, …} (D2-03, sin contract/provider/sizing)
fan-out echo/signal_fanout (key strategy_id; pre-filtro kache: AccountState + DENY_NEW_RISK — optimización, no autoridad)
  ↓ por cada AccountStrategy habilitada
echo/operation (key account_id:account_strategy_id) — guards de materialización (D2-04 §3.1 + C §8):
  1. signal válida (valid_until)            2. compatibilidad Strategy↔MM
  3. Stage-1 provider admission (autoridad: echo/provider_rules vía admission snapshot kache-fed;
     evalúa AccountState, programa/fase/RuleSet efectivo, automation entitlement, permitted
     instruments, Contract/calendar resolvability, allowed new-risk window (tz provider +
     SessionState de B), daily-loss/trailing/news state) → ALLOW | DENY_NEW_RISK
  4. resolución Instrument + Account.execution_binding_id → current Contract (binding EXECUTION)
  5. pin contract_id + specs económicas embebidas + sello direction (R2)
  ↓ ALLOW ⇒ Operation CREATED (existe ANTES de MM/Orders; DENY ⇒ ProviderDecision durable, sin Operation)
MoneyManagement (plugin en echo/operation; snapshot de cuenta/instrumento; decide 0..N Orders)
```

La denegación de materialización (Stage 1) es la única denegación sin Order: ocurre antes de construirla. Una Operation recién creada con TODAS sus entry orders denegadas en Stage 2 no se borra: si MM desiste, `TERMINAL(ENTRY_REJECTED)` con la causa provider en provenance.

## 15. Integrated Order/reservation/egress flow

```text
MM produce Order request (qty, side, tipo)
  ↓ Stage-2 gate (dentro de echo/operation, después de MM, antes del egress transaccional):
  a. PER_ORDER (max contracts/order): chequeo local exacto, |delta| ≤ cap
  b. caps compartidos (max exposure account/instrument/product_group):
     ExposureReservationRequest → echo/provider_rules (key account_id, ÚNICO punto serializado)
     retiene la Order en PENDING_SUBMIT (estado D2-04 existente) hasta ExposureReservationResult
     decisión en la MÉTRICA TIPADA de la familia (GROSS: Σ|firm|+Σ|reserved|+|delta| ≤ cap;
     NET_ABS: max(n+R⁺, R⁻−n) ≤ cap; GROUP_WEIGHTED: pesos sobre product_group) — sin fórmula plana
     GRANTED ⇒ {rule_set_id, rule_set_version, cap_family, scope} como epoch del grant
  c. guard de egress: (1) estado de cuenta — ENTITLEMENT_REVOKED/INACTIVE/CLOSE_ONLY/
     PHYSICAL_STATE_UNTRUSTED/instrumento-forbidden/forced-flat activo ⇒ suprime emisión ⇒
     Order REJECTED{source: PROVIDER_GATE, decision_id} + release; (2) epoch del grant — si la
     autoridad cambió desde el GRANT ⇒ ReservationRevalidate en el owner serializado:
     VALID ⇒ emitir; INVALID ⇒ REJECTED{PROVIDER_GATE} + release, sin egreso
  ↓
egress transaccional EXACTLY_ONCE → echo.order-commands.{account_id}.v1 → adapter (M2 idempotencia) → venue
  ↓
Fill(s) inmutables → firm += q / reserved(request) −= q (piso 0) en el mismo checkpoint
  ↓
Operación/Order/Position proyecciones + provider capacity updates (protocolo R2.5:
CapacityUpdate cumulative, ReservationFinalization{VENUE_FINAL}, ReservationAdjust)
```

Finalidad de reserva venue-autoritativa: sólo `FILLED` (consume), `REJECTED` venue-confirmado (release inmediato), `ORDER_EXECUTION_FINAL/VENUE_FINAL` (resolución por tag sobre open+history, capacidad ya exigida por R10/M2), modify-decrease ACK (`ReservationAdjust`) liberan — **el enum terminal CANCELLED/EXPIRED por sí solo nunca libera**; `PENDING_FINALITY` es `reservation.finality_state` (estado interno del reservation record en `echo/provider_rules`), **no** `Order.status` y sin estados nuevos de Order. Modify-increase reserva antes de emitir el modify; modify-decrease libera sólo tras ACK; replace = nueva reserva para la Order nueva + finalidad de la vieja (over-count conservador). Fill post-finality ⇒ `PROVIDER_CAP_BREACH_POST_FINALITY` fail-visible, sin auto-repair. Linearization point de hot updates: la cola serializada por key de `echo/provider_rules` — detección y decisión ocurren en el mismo punto; un comando nunca escapa con una autoridad ya detectada como vieja. Salidas (REDUCE/EXIT/close-orders del safety) **bypassan el gate** (I-C6) y pasan por M1/M2 intactos; el bypass nunca es autorización de transporte. DOS state owners: `echo/operation` (key `account:strategy`) posee Order/Operation/exposición lógica; `echo/provider_rules` (key `account_id`) posee reserva/capacidad/admisión — protocolo checkpoint-atómico idempotente entre ambos, skew siempre en dirección fail-safe (deniega de más, jamás otorga de más).

## 16. Provider safety flow

```text
clock/calendar/account/risk/rules update → echo/provider_rules reevalúa (autoridad corriente)
  ├─ regla con flatten explícito disparada (forced-flat cutoff, daily-loss declarado con
  |  flatten, news/holiday con flatten declarado):
  |    ProviderForceClose{account_id, reason, rule_ref, decision_id}
  |      → hacia cada key account:strategy viva de la cuenta
  |      → intent de terminación requested_by=SAFETY_PLANE (R3 D2-04)
  |      → cancela Orders vivas + emite close-orders por el path normal (gate no aplica a salidas)
  |      → TERMINAL(SAFETY_FLATTEN) SÓLO cuando guards D2-04: exposure==0 ∧ 0 live orders ∧ intent
  └─ cambios sin safety intent: instrumento prohibido ⇒ deny adds; cap bajado ⇒ ReservationRevalidate/
  |  denegación de nuevas reservas + PROVIDER_EXPOSURE_OVER_LIMIT fail-visible sin liquidación;
  └─ entitlement revocado (re-binding a programa FORBIDDEN/UNKNOWN):
       DENY_NEW_RISK permanente + SUSPENSIÓN de TODA emisión automatizada (incluida gestión MM)
       + SUSPENDED_ENTITLEMENT (flag operacional sobre Operations afectadas — NO Operation.status,
       NO termination intent) + operador: (a) attestation operator_authorized_close_only ⇒
       re-emisión sólo de cierres; (b) flatten manual en la plataforma del provider ⇒
       POSITION_MISMATCH fail-visible resuelta por operador. Re-habilitación: manual del binding.
       NUNCA ForceClose automático (emitirlo podría ser en sí la actividad prohibida).
```

El estado físico no confiable también corta new risk: `POSITION_MISMATCH` vigente, observación stale/ausente o breach ⇒ `PHYSICAL_STATE_UNTRUSTED` ⇒ `DENY_NEW_RISK` hasta reconvergencia del comparador D2-04 §7.3 u operador; sin reconciliation repair (`DT-EF-POSITION-RECONCILIATION-05` diferido). El plano safety del owner (automations RFC-005, emergency close) sigue operando en paralelo, intacto.

## 17. Hot vs pinned semantics

| Clase | Elementos |
|---|---|
| **PINNED / SNAPSHOTTED** (inmutable en la vida de la entidad) | `Operation.contract_id` (pin al materializar, D2-01); specs económicas del Contract embebidas en el snapshot de Operation (`tick_size`, `point_value`/`tick_value`, `qty_min/step`); `direction` sellada por la Signal (R2); config MM efectiva del snapshot (D2-01/04, sin revisiones); calendar snapshot input de un run histórico (manifiesto: `revision_hash` + payload + transiciones); RuleSet snapshot inyectado cuando un run simula un ProviderProgram |
| **DYNAMIC / HOT** (vigencia prospectiva) | `InstrumentMapping` corriente por binding (afecta sólo materializaciones futuras); `ProviderRuleSet` autoridad corriente (reevaluación inmediata al publicarse; safety actúa en vivo sólo vía intents); `ProviderAccountBinding` corriente (re-binding in-place); `ExchangeCalendar` live config (dataset append-fechado, overrides corrigen como nueva versión); estado de Account (AccountState); estado de admisión provider (admission snapshot); estado de riesgo provider (daily/trailing/news) |
| **PROVENANCE-ONLY** (registro, no autoridad) | `rule_set_id/rule_set_version` en cada `ProviderDecision` y en el epoch de cada GRANT; `admission_decision_id` en Operation (referencia a la decisión que la admitió); `calendar revision_hash`/metadata de snapshots del manifiesto del run; `rejection{source: PROVIDER_GATE, decision_id}` en Orders denegadas; audit facts de re-binding (Kafka/OTel) |

Ninguna provenance crea un framework genérico de versiones (D2-01): son referencias/payloads puntuales con retención de topics/OTel o del run artifact.

## 18. Provenance

Contrato único `ProviderDecision {decision_id UUIDv7; account_id; account_strategy_id?; operation_id?; kind: ADMIT_OPERATION|DENY_NEW_RISK|ADMIT_ORDER|DENY_ORDER|SAFETY_FORCE_CLOSE; provider_id; program_id; phase?; rule_set_id; rule_set_version; rule_family; reason tipado; evaluated_at; exposure_state_as_of?}`. Persistencia en dos canales, ambos checkpoint-atómicos: decisiones de `echo/provider_rules` por su egress transaccional `echo.provider-decisions.v1` (projector PG eventual); decisiones dentro de `echo/operation` (admisión de materialización, DENY_ORDER) como record `PROVIDER_DECISION` por el egress de proyecciones/facts R14 (`echo.operation-projections.v1`). Operation guarda **sólo referencias** (`admission_decision_id` aditivo; `termination` conserva su shape D2-04 con el decision_id del intent). Calendar provenance: manifiesto del run con `{calendar_id → (revision_hash, snapshot_payload[, transiciones])}` — el anchor es el snapshot grabado, no un puntero; el resolver recibe dataset inyectado, nunca un anchor (B-R2). OTel complementa, no sustituye los facts durables. Sin history engine genérico, sin tablas de eventos (R9 intacto).

## 19. LIVE / REPLAY / BACKTEST contract

Misma lógica de dominio (paquetes Go puros, sin infra — boundary Q14) para: identidad Instrument; semántica económica Contract; CalendarResolver y session_date; NamedTradingWindow; reglas provider tipadas cuando el run simula un ProviderProgram; Strategy/Signal; MM; semántica Operation. **LIVE** consume hot config vigente (kache). **REPLAY/BACKTEST** inyecta snapshots/config inputs explícitos del run: el calendario se resuelve contra el **snapshot payload del manifiesto del run**, nunca contra la config mutable actual; una rerun what-if puede inyectar el dataset actual — la divergencia de hashes es visible, jamás silenciosa. **Provider RuleSet histórico:** A/B/C congelan familias+parámetros y version/provenance del RuleSet, pero no una política completa de grabación de RuleSet histórico para sesiones live; el seam mínimo congelado aquí (sin inventar entidad): un run que simula un ProviderProgram declara en su manifiesto el input de autoridad — `{provider, programa[, fase]} → (rule_set_id, rule_set_version, snapshot payload/hash)` — con el **mismo patrón run-input provenance del calendario** (anchor = snapshot grabado; registro obligatorio en el proceso consumidor; sin servicio de revisiones); riesgo residual declarado en §23 (procesos sin provenance registrada y drift de valores owner-managed). D2-04 ya acotó el claim general: mismo stream ordenado ⇒ mismas decisiones; recorded streams/ordering es del workstream D2 Market/Replay — no se reabre.

## 20. D2-04 lifecycle integration

Intacto y verificado punto por punto: la Operation se materializa ANTES de MM (la admisión provider Stage-1 es un guard más de la materialización, al nivel de `valid_until`/pin/direction); el order gate Stage-2 vive después de MM y antes del egress (una Order denegada nunca entra al command topic: sin comando físico, sin journal de adapter, sin pregunta M2); `ForceClose != TERMINAL` (intents R3; TERMINAL exige guards); el pin de Contract y el snapshot MM de una Operation viva jamás son mutados por hot updates de reglas/calendario/mapping; **no se agregó ningún `Order.status`** (`PENDING_FINALITY` es `reservation.finality_state`; `SUSPENDED_ENTITLEMENT` es flag operacional; `REJECTED{PROVIDER_GATE}` reutiliza el enum existente con provenance estructural aditiva); `TERMINAL(ENTRY_REJECTED)` reutilizado para entradas denegadas con causa en provenance; fills post-terminal siguen el path R13; Position sigue siendo observación física neta `(account, contract)` y trust guard del gate, jamás mutador del lifecycle; la familia de egress/projections R14 transporta también los `PROVIDER_DECISION` internos.

## 21. Echo V3 REUSE/EXTEND/ADAPT/REPLACE map

Integrado de los tres TOPs (sólo piezas ya verificadas por ellos; blobs @ `372af59a`):

| Pieza V3 | Disposición | Evidencia (path · blob) |
|---|---|---|
| InstrumentSnapshot | REUSE (path legacy) / no es fuente de specs del dominio nuevo | `v3/sdk/domain/snapshots.go` · `d319d0a3` |
| MMEngineFn | ADAPT → resolución explícita + pin en `echo/operation` | `v3/core/internal/functions/mm_engine.go` · `e725ceb0` |
| SymbolMappingHandler (+topic `echo.symbol-mappings.v1`) | REUSE/EXTEND — patrón hot config (Hasura→topic compactado→tombstone) para todos los catálogos nuevos | `v3/gateway/internal/symbol_mapping_handler.go` · `a9364d4a` |
| ConfigCache / kache | REUSE (ready channel + lectura in-process) / EXTEND con caches instrument/contract/mapping/calendars/windows/provider | `v3/core/internal/config_cache.go` · `eecc6f9e`; `v3/sdk/kache/account_configs.go` · `2991979b` |
| DayBoundaryCache + `prop_rulesets.daily_reset_*` | REUSE (autoridad account_day separada) / EXTEND fail-closed (day boundary explícito Futures; fallback UTC-23:00 prohibido en camino nuevo) | `v3/core/internal/functions/account_sync.go` · `b0f8f1ce`; `001_schema_baseline.up.sql` · `a186be35` |
| ExecutionPolicy | ADAPT (separa binding/MM/knobs; pips legacy-only) | `v3/sdk/domain/execution_policy.go` · `295f7ea2` |
| StrategyConfigFn | REUSE (patrón KVS config) | `v3/core/internal/functions/strategy_config.go` · `b89a9a1a` |
| AutomationEvaluatorFn + typed evaluators/registry + AutomationCache/TriggerCache | REUSE (patrón chain snapshot→evaluación sin I/O→egress exactly-once; familias tipadas) — `echo/provider_rules` replica la forma, autoridad distinta | `automation_evaluator.go` · `9503410e`; `core/internal/automation/evaluator.go` · `bf97b13a`; `cache.go` · `39a461e3` |
| ClientConfig / AccountState / TradingWhitelist | REUSE (autoridad operacional de cuenta + whitelist canónica, complementa permitted-instruments) | `v3/sdk/domain/client_config.go` · `587eb5c4` |
| Gateway CloseHandler (CloseBatch/CloseAll) | REUSE (patrón safety account-wide) → apunta a intents R3 del aggregate nuevo | `v3/core/internal/functions/close_handler.go` · `8dba9731` |
| Gateway automation handlers/news evaluator | REUSE/ADAPT (transporte webhook→Kafka de catálogos; precedentes de familias news) | `v3/gateway/internal/automation/handler.go` · `5f0a99e2`; `news_blackout_evaluator.go` · `4bda7e10` |
| Gateway automation ScheduleActionExecutor (MEN-1) | REUSE (precedente LoadLocation tz-safe) | `v3/gateway/internal/automation/executor.go` (LoadLocation line ~396) |
| strategy_history contracts (IANA validation, RFC3339Nano) | REUSE (precedente de validación tz e instants UTC) | `v3/sdk/contracts/strategy_history.go` · `e43bc48b` |
| `echo.prop_rulesets` (legacy) | REUSE (concepto) / REPLACE (shape): identity `prop_firm` + enum `phase_type` + columnas planas sin version/provenance = anti-patrón corregido; su FK alimenta el DayBoundary durante la transición | `001_schema_baseline.up.sql` · `a186be35` |
| Bridge mapper/symbol_mapping_cache | REUSE legacy (detransform edge); unificación futura = `DT-EF-CROSS-MARKET-INSTRUMENT-02` | `v3/bridge/internal/mapper.go` · `76a1b1de` |
| Provider/Program/RuleSet/Binding + `echo/provider_rules` + CalendarResolver + catálogos calendario/ventanas | NEW (no existen en V3; grep 0 hits en ambos TOPs) | — |

## 22. Migration implications

Transición conceptual (orden compatible con legacy V3, sin big bang): (1) nuevos catálogos/config en PG (instruments/contracts/identifiers/mappings; exchange_calendars; trading_windows; providers/programs/rule_sets/bindings) — alta owner via Hasura; (2) hot distribution: handlers Gateway + topics compactados + kache (patrón existente); (3) Instrument/Contract mapping con bindings (`MARKET_DATA`/`EXECUTION`) conviviendo con `symbol_mappings` legacy (el bridge MT sigue su path); (4) CalendarResolver + readiness fail-closed (sin calendario no se opera Instrument Futures; el legacy MT no consulta el resolver); (5) Provider binding/RuleSet (onboarding con provenance; sin RuleSet efectivo ⇒ cuenta no admite riesgo); (6) Stage-1 admission como guard de materialización en el aggregate nuevo (no toca ExecutionPlannerFn legacy); (7) Contract pinning + snapshot specs (dominio puro + `echo/operation`); (8) Order reservation/gate con `echo/provider_rules` (protocolo R2.5); (9) safety intents (`ProviderForceClose`) en paralelo con el CloseHandler legacy; (10) coexistencia temporal: `symbol_mappings` y `prop_rulesets` legacy permanecen para el path Forex/CFD/Reference hasta su migración (deudas `DT-EF-FX-PROP-01`/`DT-EF-CROSS-MARKET-INSTRUMENT-02`); `prop_rulesets` alimenta el DayBoundary existente mientras dure. Ningún paso exige reescritura de Core (Q1 owner-accepted).

## 23. Risks/debts (consolidado)

- **Curación owner de `product_group`/`calendar_ref`/calendarios/RuleSets:** datos owner-managed incorrectos degradan caps/sesiones sin error runtime (el resolver resolvería "correctamente" un calendario equivocado); mitigaciones: validación de config, fail-closed de readiness/unresolved, hash visible en runs; residual de la misma clase que el symbol mapping de hoy. (A R-G, B R1, C fidelidad de valores.)
- **FX para MM:** cuentas no-USD sobre contracts USD exigen conversión FX en MoneyManagement — seam declarado, bloqueante de sizing fixed-risk, no de identidad. (A R-B.)
- **Old Contract venue behavior:** cierre sobre contrato expirado/inactivo depende del venue (`ContractNotActive` etc.); fail-visible por diseño; el borde exacto post-deactivation sigue UNKNOWN no bloqueante (Front E §22). (A R-E/Caso H.)
- **Calendar/tzdata historical provenance:** tzdata/regla civil entre releases — visible por identifier en manifiesto, no recuperable; correcciones de fechas ya operadas sólo como nueva versión (`corrected_at`) — hash hace la divergencia visible. (B R2.)
- **Venue finality trust:** release de reservas exige finalidad venue-autoritativa (open+history por tag); un venue que contradice su propio history rompe a cualquier cliente — `PROVIDER_CAP_BREACH_POST_FINALITY` fail-visible, sin repair. (C R2.1.)
- **PHYSICAL_STATE_UNTRUSTED:** mientras la base física esté inconsistente/stale, los opens quedan pausados fail-closed (las salidas fluyen); reconvergencia u operador reabre. (C R2.4.)
- **Provider policy ingestion/drift:** las firmas cambian política unilateralmente; Echo depende del refresh owner del catálogo (no auto-detección); binding stale = riesgo operacional del owner, mitigado por fail-closed de admisión y alertas. (C §16.)
- **UNKNOWN evidence:** Tradeify automation/copy y FundedNext copy = UNKNOWN (no activables como hard rules; advisory); Lucid allowed-window/4:45 retirado por C-R5; activar hard rules exige reconciliación de evidence authority (decisión SUBMANAGER). (C R2.7/C-R5.)
- **Latencia del reservation hop:** un hop interno adicional in-process en la emisión (mensajería entre funciones del mismo runtime); a medir en D6. (C R1.)
- **Deuda legacy:** migración pips/symbol_mappings/prop_rulesets (`DT-EF-FX-PROP-01`, `DT-EF-CROSS-MARKET-INSTRUMENT-02`, limpieza pips pendiente de ratificación owner); resolución histórica de contratos por fecha para el backtester (sin lifecycle timestamps); caps físicos inclusivos (Position como input de reserva) DEFER. (A/B/C.)

## 24. Owner decisions

`OWNER DECISIONS REQUIRED: NONE` — los tres TOPs declaran NONE y la integración no descubrió contradicción nueva (§20 del mandato). Ratificaciones técnicas ordinarias para el manager (no owner, no cambian semántica): (1) nombres físicos de functions/topics/tablas nuevos (`echo/provider_rules`, topics config/decisions/admission, tablas catálogo — C §17; `echo.exchange-calendars.v1`, `echo.trading-windows.v1`, `echo.exchange_calendars`, `echo.trading_windows` — B; instruments/contracts/identifiers/mappings — A); (2) firma del API del resolver y primitivas provider (`SessionState/SessionDate/SessionBoundaries/NextSessionTransition` por `calendar_id`); (3) requisito de build `_ "time/tzdata"`; (4) snapshot-en-manifiesto como anchor de run (calendario y RuleSet simulado); (5) enums/flags/campos aditivos de C §17 (`reason` tipado, `admission_decision_id`, `rejection{PROVIDER_GATE}`, `SUSPENDED_ENTITLEMENT`, `phase?` nullable, epoch del GRANT + `ReservationRevalidate`).

## 25. Acceptance cases A–H

- **A — rollover manual (PASS-BY-DESIGN):** mapping `(EXECUTION, projectx-topstep, NQ)→NQZ6`; Operation A materializa (pin `NQZ6` + specs embebidas); owner rola la fila a `NQH7`; Operation B nueva resuelve `NQH7`; A sigue `NQZ6` en adds/reduces/fills y su Position vive en `(account, NQZ6)`. Ningún retarget (A Caso A).
- **B — feed/execution identifiers differ (PASS-BY-DESIGN):** Strategy emite `instrument_id=NQ` agnóstica; el feed resuelve `(MARKET_DATA, databento-main, NQ)→NQZ6` + identifier `(databento, MARKET_DATA)=X`; la Account resuelve `(EXECUTION, projectx-topstep, NQ)→NQZ6` + identifier `(projectx, EXECUTION)=CON.F.US.ENQ.H25 (Y)`; X≠Y, mismo Contract Echo; rollover de feed y ejecución en momentos distintos sin tocar Operations. (A Casos B/A-R1-1/2/3.)
- **C — Exchange open, Provider blocks (PASS-BY-DESIGN):** `SessionState(CME_EQ_INDEX, t)=OPEN` y `AccountState=ACTIVE`, pero admission snapshot `DENY_NEW_RISK` (p. ej. ventana provider cerrada, `WINDOW_CLOSED`) ⇒ la OPEN no se acepta: **no hay Operation, ni MM, ni Orders**; `ProviderDecision{DENY_NEW_RISK}` durable; los cierres de otras Operations de la cuenta siguen fluyendo. (C Caso C.)
- **D — forced flat (PASS-BY-DESIGN):** RuleSet declara cutoff 3:10 PM CT; `echo/provider_rules` dispara `ProviderForceClose` hacia cada key viva ⇒ intent `requested_by=SAFETY_PLANE`; cancela Orders working, emite close-orders (gate no aplica a salidas); `TERMINAL(SAFETY_FLATTEN)` sólo al cumplirse guards D2-04 — **no instant TERMINAL**; un fill tardío post-terminal va al path R13. (C Caso D.)
- **E — early close (PASS-BY-DESIGN):** override fechado `EARLY_CLOSE 13:15 CT` en `CME_EQUITY_INDEX`; LIVE: 13:14 OPEN, 13:16 CLOSED(no_session), `NextSessionTransition` → apertura dominical; REPLAY con el snapshot anclado del manifiesto: mismas resoluciones byte-idénticas (mismo resolver + mismo dataset inyectado); barras cierran el día en 13:15 por el contrato D2-06. (B Casos E/B-R2-CASE-2.)
- **F — Account DayBoundary (PASS-BY-DESIGN):** al cruzar el boundary de la cuenta (tz+reset del binding, vía DayBoundaryCache), `echo/provider_rules` resetea acumuladores diarios (daily HWM, prev-day-close, deny por daily-loss expira) con `reset_semantics` tipado; no toca ExchangeSession/trade-date de B ni Contract; una Operation viva no muta. (B Caso F, C Caso F.)
- **G — live RuleSet update (PASS-BY-DESIGN):** nueva versión ACTIVE ⇒ reevaluación inmediata; decisiones nuevas portan `rule_set_version` nueva; Operations vivas conservan pin+snapshot. Con safety intent (cutoff alcanzado, daily-loss con flatten declarado): `ProviderForceClose` ⇒ intents. Sin intent: instrumento prohibido ⇒ deny adds; cap bajado ⇒ grants outstanding `ReservationRevalidate` (epoch cambió ⇒ INVALID ⇒ `REJECTED{PROVIDER_GATE}` + release, sin egreso; C-R3-B), exposición ya física ⇒ `PROVIDER_EXPOSURE_OVER_LIMIT` fail-visible sin liquidación; entitlement revocado ⇒ suspensión de emisión + `SUSPENDED_ENTITLEMENT` + operador, **nunca ForceClose automático**. (C Caso G/C-R3-B/C.)
- **H — old Contract edge (PASS-BY-DESIGN):** Operation A (pin `NQZ6`) activa tras el rollover; MM emite CLOSE con `contract_id=NQZ6` + identifier corriente de `NQZ6`; el venue ejecuta o rechaza (`REJECTED` fail-visible); **jamás** current mapping, jamás remap silencioso; la migración de exposición es decisión owner explícita. (A Caso H.)

## Evidencia

- Children integrados (blobs verificados en HEAD `76836cae` del vault, idénticos a los aprobados por el SUBMANAGER): [[Echo Futures — D2-05A Instrument Contract]] · `6eb671f2`; [[Echo Futures — D2-05B Session Calendar]] · `8058aec0`; [[Echo Futures — D2-05C Provider Program Rules]] · `637c62b8`. Los detalles, repairs y casos de cada TOP viven en sus artefactos; este candidato integra, no duplica ni reabre.
- Autoridades congeladas: [[Echo Futures]] (D2-01/02/03 OWNER_CLOSED; Q6/Q7/Q10 `D1_INPUT_SUFFICIENT_FOR_D2`), [[Echo Futures — D2-04 Operation Order Fill Position]] (CLOSED R1–R14), [[Echo Futures — D1 Analysis Pack]] (Front E/C/D synthesis), [[CONTRACT + SESSION SEMANTICS — AUTHORITATIVE EVIDENCE]] (S-E01..S-E09, C-E01..C-E08), [[FUTURES PROP UNIVERSE — AUTHORITATIVE EVIDENCE MATRIX]] (matriz autoritativa de automatización/copy — sólo como provenance de afirmaciones de C).
- Baseline Echo re-verificada para esta integración: `xKoRx/echo origin/master = 372af59a7b83604781346613da01e3d510ea1360` (fetch re-hecho, sin delta). Blobs de source citados en §21 tal como los verificaron los TOPs.

## Handoff

```text
D2-05 INTEGRATION STATUS: READY_FOR_SUBMANAGER_REVIEW

INTEGRATED ARTIFACT: main/10-projects/Echo Futures/Echo Futures — D2-05 Instrument Session Provider.md

CHILD INPUTS (blobs verificados == aprobados, sin drift):
A: main/10-projects/Echo Futures/Echo Futures — D2-05A Instrument Contract.md · 6eb671f2466c5d89ba71686b45f2e4c32d1b033f (READY_FOR_INTEGRATION)
B: main/10-projects/Echo Futures/Echo Futures — D2-05B Session Calendar.md · 8058aec0edbf852b38fb5bce92304a2a032dd56a (READY_FOR_INTEGRATION)
C: main/10-projects/Echo Futures/Echo Futures — D2-05C Provider Program Rules.md · 637c62b810ec8723dd421267ffccc583691a584e (READY_FOR_INTEGRATION)

ECHO BASELINE: 372af59a7b83604781346613da01e3d510ea1360 (fetch re-verificado, sin delta)

INTEGRATED MODEL:
A aporta identidad: Instrument canónico (instrument_id, quote_currency, exchange, product_group,
calendar_ref) → Contract expiry-specific con specs económicas; mapping hot por binding
(mapping_context, binding_id, instrument_id); external identifiers por (source, context);
pin único en materialización; rollover owner-manual prospectivo. B aporta tiempo de mercado:
ExchangeCalendar = dataset por semántica de producto (weekly_base + overrides fechados,
precedencia override>base>fail-closed) + resolver puro sdk/calendar; session_date como dato;
session_id=(calendar_id, session_date) unívoco; NamedTradingWindow (∩ exchange); account_day
separado; IANA-only + tzdata embebida. C aporta negocio/reglas: Provider→Program→(fase opcional
provider-local)→RuleSet versionado con provenance; binding en la Account (entitlement de
transporte separado); enforcement Stage-1 (guard de materialización, ALLOW|DENY_NEW_RISK) +
Stage-2 (gate post-MM/pre-egress con reserva serializada en echo/provider_rules) + safety
asíncrono por intents. D2-04 conserva el lifecycle íntegro. Tres state owners con keys
distintas (operation account:strategy / provider_rules account_id / signal_fanout strategy_id).

CROSS-TOP CONSISTENCY:
calendar_ref único binding runtime A→B; resolver sin product_group/exchange (B-R1/A-R2);
session_id=(calendar_id,session_date) colisión-imposible por cardinalidad;
(exchange, product_group, instrument_id) = llaves de reglas de C, ortogonales a la sesión;
C consume de B exactamente SessionState/SessionDate/SessionBoundaries/NextSessionTransition
por calendar_id y jamás recibe provider policy de B; dos resoluciones separadas
(current Contract ≠ vendor identifier); dos state owners de enforcement sin fusión
(protocolo checkpoint-atómico, skew fail-safe). Sin contradicción cross-TOP nueva.

ENFORCEMENT:
Stage-1 = guard de materialización (sin Operation si DENY; AccountState ∧ provider = conjunción
de autoridades independientes). Stage-2 = post-MM/pre-egress: PER_ORDER local; caps compartidos
por reserva serializada en métrica tipada (GROSS/NET_ABS/GROUP_WEIGHTED), PENDING_SUBMIT hasta
GRANT; guard de egress doble (estado de cuenta + epoch del grant con ReservationRevalidate);
finalidad venue-autoritativa libera (PENDING_FINALITY = reservation.finality_state, nunca
Order.status); salidas jamás bloqueadas; PHYSICAL_STATE_UNTRUSTED fail-closed; safety con
flatten sólo vía intents; entitlement revocado ⇒ suspensión, jamás ForceClose automático.

HOT/PINNED:
PINNED: contract_id + specs económicas + direction + config MM del snapshot de Operation;
calendar snapshot input de run; RuleSet snapshot inyectado en runs que simulan ProviderProgram.
HOT: mapping por binding, RuleSet corriente, binding de cuenta, calendario live, AccountState,
admission/risk state — todo prospectivo, jamás muta pinned. PROVENANCE-ONLY: rule_set epoch en
decisiones/grants, admission_decision_id, revision_hash/snapshots del manifiesto,
rejection{PROVIDER_GATE}. Sin generic revision framework.

LIVE/REPLAY/BACKTEST:
Misma lógica de dominio pura (identity, contract economics, resolver, ventanas, reglas provider
tipadas, Strategy/MM/Operation). LIVE consume hot config vigente. REPLAY/BACKTEST inyecta los
snapshots explícitos del run: calendario contra snapshot payload del manifiesto (anchor =
snapshot grabado, no puntero; byte-idéntico al re-inyectar); RuleSet simulado declara
{programa → (rule_set_id, version, snapshot)} con el mismo patrón run-input provenance (seam
mínimo congelado, sin entidad nueva). Divergencias de hash visibles, nunca silenciosas.

ECHO V3 REUSE/ADAPT:
REUSE: kache/ConfigCache, SymbolMappingHandler (patrón hot config), DayBoundaryCache+prop_rulesets
(account_day separado; EXTEND fail-closed sin fallback UTC), automation chain/typed evaluators,
ClientConfig/AccountState/whitelist, CloseHandler (patrón safety), strategy_history (IANA/UTC),
MMEngineFn/ExecutionPolicy (ADAPT). REPLACE de shape: prop_rulesets (identity por prop_firm +
enum de fase) → catálogos provider versionados. NEW: Provider/Program/RuleSet/Binding,
echo/provider_rules, CalendarResolver, catálogos calendario/ventanas, catálogos
Instrument/Contract/mapping. Migration en 10 pasos compatibles con legacy, sin big bang,
sin reescritura de Core.

ACCEPTANCE A-H:
A PASS-BY-DESIGN (rollover manual, pin intacto)
B PASS-BY-DESIGN (bindings feed/execution, identifiers distintos, Strategy agnóstica)
C PASS-BY-DESIGN (exchange OPEN ∧ provider DENY_NEW_RISK ⇒ sin Operation)
D PASS-BY-DESIGN (ProviderForceClose = intent; TERMINAL sólo por guards)
E PASS-BY-DESIGN (early close via override; LIVE/REPLAY idénticos con snapshot anclado)
F PASS-BY-DESIGN (account day reset independiente; sin tocar sesión ni Contract)
G PASS-BY-DESIGN (reglas nuevas prospectivas; revalidación de grants; revocación = suspensión)
H PASS-BY-DESIGN (cierre sobre contrato viejo pinneado; venue rejection fail-visible)

OWNER DECISIONS REQUIRED:
NONE (ratificaciones técnicas manager: nombres físicos, firma del resolver, tzdata embebida,
anchor snapshot-en-manifiesto, enums/campos aditivos de provenance)

MATERIAL RISKS:
curación owner de catálogos (product_group/calendar_ref/calendarios/valores de reglas) sin
error runtime; FX para MM no-USD (seam); old-contract venue behavior UNKNOWN de borde;
tzdata/regla civil entre releases (visible, no recuperable); venue finality trust
(post-finality contradiction = fail-visible); PHYSICAL_STATE_UNTRUSTED pausa opens;
provider policy drift owner-managed; UNKNOWN evidence (Tradeify/FundedNext copy) no activable;
latencia del reservation hop (medir D6); deuda legacy pips/symbol_mappings/prop_rulesets.

PROJECT NOTE:
D2-05 = INTEGRATION_CANDIDATE_READY_FOR_SUBMANAGER_REVIEW (reemplaza el estado contaminado
READY_FOR_MANAGER_REVIEW). NOT CLOSED. NOT READY_FOR_PRIMARY_MANAGER UNTIL SUBMANAGER REVIEW.
DO NOT ADVANCE D2-06.

NEXT: SUBMANAGER review only.
```

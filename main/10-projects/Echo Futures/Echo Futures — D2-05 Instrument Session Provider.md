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

## Primary Manager Repair — R15–R18

Primary Manager review marcó `D2_05_MANAGER_REVIEW = CORRECTION_REQUIRED` sobre el candidato integrado. Este repair es **targeted integration repair**: no reabre A/B/C, no cambia D2-04, no implementa código y no avanza D2-06.

- **R15 — Stage-1 admission authority:** el snapshot kache deja de ser autoridad de aceptación. Toda OPEN candidata se lineariza mediante `AdmissionRequest → echo/provider_rules(account_id) → AdmissionResult`. El owner account-keyed serializa el request contra RuleSet/binding/account-state/risk/time updates. Kache queda sólo como pre-filtro/read model. ALLOW es válido según el orden de esa cola; si una actualización se procesa antes, el request ve la autoridad nueva. El guard Stage-2/egress permanece como defensa posterior.
- **R16 — capacity projection completa:** `echo/provider_rules(account_id)` mantiene `firm_by_operation[operation_id]` + `live_reservations`, no un net opaco por Contract. Después de **todo Fill Echo** — ENTRY, ADD, REDUCE, EXIT, safety close y late/reconciled Fill — `echo/operation` emite un update cumulativo con identidad y exposición firmada de la Operation. Así GROSS = suma de absolutos por Operation, NET_ABS = net firmado por scope y GROUP_WEIGHTED aplica pesos del RuleSet, sin portfolio aggregate. Replay no duplica porque el update es cumulativo y monotónico por `operation_event_seq`.
- **R17 — deterministic ForceClose fan-out:** `echo/provider_rules` enumera el catálogo/routing index completo de AccountStrategies de la Account (ACTIVE, disabled y close-only incluidos) y envía el mismo intent a cada key `account:account_strategy`. Una key sin Operation es no-op idempotente. V1 usa soft-disable/retención de la routing identity; no se hard-tombstonea una AccountStrategy mientras pueda poseer una Operation no terminal. PG jamás participa de correctness.
- **R18 — DayBoundary Futures hot:** el `DayBoundaryCache` físico actual es sólo precursor conceptual. Su contrato real es lazy DB + cache forever sin invalidación por account_id y fallback UTC 23:00, incompatible con re-binding in-place. Futures usa config explícita hot/readiness-safe dentro del owner `echo/provider_rules(account_id)`; falta/invalid config ⇒ `DAY_BOUNDARY_UNRESOLVED` + DENY_NEW_RISK. Un update se lineariza en la misma cola account-keyed, preserva acumuladores actuales y reprograma prospectivamente el próximo boundary sin retro-recalcular días pasados ni reutilizar el cache mutable legacy como autoridad de dominio.

`OWNER_DECISIONS_REQUIRED = NONE`.

## 1. Executive verdict

```text
D2-05 REPAIR STATUS: READY_FOR_MANAGER_REVIEW
```

La integración de A+B+C produce una arquitectura única y legible sin agregar una cuarta capa ni resolver contradicciones por invención: **A aporta la identidad económica y su resolución física** (Instrument canónico → Contract expiry-specific pinneado una vez por Operation, con mapping hot por binding y external identifiers por fuente); **B aporta la autoridad temporal de mercado** (ExchangeCalendar como dataset owner-managed + resolver puro en proceso, session/trade date como dato, ventanas nombradas para Strategy, account day separado); **C aporta la autoridad de negocio/reglas** (Provider → ProviderProgram → (fase opcional provider-local) → ProviderRuleSet versionado, binding en la Account, enforcement en dos gates + plano safety asíncrono). D2-04 conserva íntegro el ownership del lifecycle: la Operation sigue materializándose antes de MM, la terminación sigue exigiendo guards, y ningún gate provider cambia un solo estado del aggregate.

Los tres seams cruzados quedaron cerrados y congelados en los repairs A-R1/A-R2, B-R1/B-R2 y C-R1..C-R5, y esta integración los verifica compatibles sin reabrirlos: (1) `Instrument.calendar_ref → calendar_id` es el único binding runtime hacia el CalendarResolver — el resolver no recibe `product_group` ni `exchange`, y `product_group`/`exchange` son llaves de reglas de C, no de sesión; (2) `session_id = (calendar_id, session_date)` es unívoco por construcción (un calendario = una semántica de producto/sesión); (3) las primitivas que C consume de B son exactamente `SessionState/SessionDate/SessionBoundaries/NextSessionTransition` por `calendar_id` — B jamás publica provider policy; (4) la reserva de exposición vive en un segundo state owner (`echo/provider_rules`, key `account_id`) coordinado con `echo/operation` (key `account_id:account_strategy_id`) por mensajería checkpointeada idempotente (C-R2.5: el Fill y la emisión del `CapacityUpdate` son atómicos en la frontera del operation owner; la aplicación en provider_rules puede atrasarse — skew fail-safe que jamás otorga de más), sin fusionar owners.

`OWNER DECISIONS REQUIRED: NONE` — los tres TOPs lo declaran y la integración no descubrió contradicción nueva que lo cambie. Quedan ratificaciones técnicas ordinarias del manager (nombres físicos de functions/topics/tablas, enums de reason, campos aditivos de provenance), listadas en §24. La integración NO es PASS ni CLOSED: el SUBMANAGER decide el siguiente gate.

## 2. Minimal entity model

| Entidad / state | Autoridad | Una línea |
|---|---|---|
| `Instrument` | A | Identidad económica/canónica: `instrument_id`, `quote_currency`, `exchange`, `product_group`, `calendar_ref`. |
| `Contract` | A | Tradable expiry-specific; Operation lo resuelve y pinnea una vez. |
| `ContractIdentifier` | A | External identifier por fuente/contexto; jamás identidad Echo/Provider. |
| `InstrumentMapping` | A | `(mapping_context, binding_id, instrument_id) → contract_id`, hot y prospectivo. |
| `ExchangeCalendar` / `NamedTradingWindow` | B | Autoridad temporal de exchange/Strategy; resolver puro por `calendar_id`. |
| `Provider` / `ProviderProgram` / `ProviderRuleSet` | C | Autoridad business/policy; RuleSet es la única pieza con version/provenance explícita. |
| `ProviderAccountBinding` | C | Config account-scoped corriente: provider/program/phase?, RuleSet authority, transport entitlement y DayBoundary explícito. |
| `AccountStrategy` | D2-01..03 | Sigue siendo `Account + Strategy + MoneyManagement`; provider config no entra aquí. |
| `Operation/Order/Fill/Position` | D2-04 | Lifecycle congelado; `echo/operation` key `account_id:account_strategy_id`. |
| `echo/provider_rules` state | C + R15–R18 | Owner key `account_id` de Stage-1 admission, RuleSet/binding/account/risk state, DayBoundary efectivo, `firm_by_operation`, `live_reservations` y routing index de AccountStrategies. Es una proyección/autoridad de enforcement, NO owner del lifecycle de Operation. |
| `AccountStrategyRoutingIndex` | R17 | Read model/config completo por Account para fan-out safety. Incluye disabled/close-only; no usa PG. |
| Resolvers puros | A/B/R18 | Contract resolver, CalendarResolver y DayBoundary resolver/config semantics inyectables en LIVE/REPLAY/BACKTEST. |

State owners congelados:
```text
echo/signal_fanout   key strategy_id
echo/operation       key account_id:account_strategy_id
echo/provider_rules  key account_id
```
No se crea portfolio aggregate ni se fusionan owners.

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

`ProviderAccountBinding` sigue siendo config corriente 1:1 de la Account, reemplazada in-place con audit facts y sin revision framework:

```text
account_id
provider_id
program_id
phase?                    # sólo si ese programa declara fase provider-local
rule_set_id/rule_set_version   # provenance/autoridad corriente, no versión del binding
transport {
  transport_id
  entitlement
  conditions[]
}
day_boundary {
  timezone                # IANA
  reset_time              # local wall clock
  reset_semantics         # familias que resetean / no resetean
}
enabled
```

`AccountStrategy` permanece exactamente `Account + Strategy + MoneyManagement`. Todas las AccountStrategies de la cuenta comparten ProviderProgram/RuleSet/DayBoundary y transport entitlement; ninguna de esas cosas se embute en AccountStrategy.

Separaciones congeladas:

- Provider business identity ≠ transport.
- platform support ≠ API entitlement; UNKNOWN/FORBIDDEN nunca se interpreta como permitido.
- `AccountState` de Echo y provider admission son autoridades distintas, ambas procesadas por el owner account-keyed para Stage-1.
- DayBoundary ≠ ExchangeSession ≠ Provider trading overlay.
- Para Futures V1 el DayBoundary efectivo es **config explícita obligatoria**. Falta, timezone inválida, reset inválido o config aún no ready ⇒ `DAY_BOUNDARY_UNRESOLVED` y `DENY_NEW_RISK`. No existe fallback UTC 23:00 en el camino nuevo.

### DayBoundary hot/update semantics

El source legacy `DayBoundaryCache` no es autoridad canónica para Futures: físicamente hace lazy-load desde PG y cachea forever por `account_id`, asumiendo que un cambio de fase crea otra account; D2-05 congela re-binding in-place con el mismo account_id. Para Futures, `echo/provider_rules(account_id)` recibe la config DayBoundary por el mismo control-plane hot/readiness-safe de binding/rules y la procesa en su cola serializada.

Estado mínimo: `effective_day_boundary`, `last_reset_at`, `next_reset_at` y acumuladores diarios. Un update de config:

1. se lineariza como evento en la cola `account_id`;
2. preserva los acumuladores actuales — no resetea al aplicar config ni reconstruye días pasados;
3. sustituye la autoridad para decisiones futuras;
4. recalcula `next_reset_at` con la nueva timezone/reset y un `not_before` que no precede al `next_reset_at` ya comprometido bajo la autoridad anterior; así un cambio después de un reset no introduce un segundo reset inmediato y un cambio antes del próximo reset no ejecuta el boundary viejo después de activarse la autoridad nueva;
5. el siguiente crossing qualifying bajo la nueva autoridad ejecuta un único reset y actualiza `last_reset_at/next_reset_at`.

El mismo resolver/config-transition contract es inyectable en replay/backtest; el cache mutable legacy de live no forma parte del dominio reproducible.

## 14. Integrated OPEN/materialization flow

```text
Strategy
  ↓ Signal{instrument_id,...}
echo/signal_fanout (key strategy_id)
  - kache AccountState/admission snapshot puede prefiltrar
  - es OPTIMIZATION/read model, nunca authority
  ↓ candidate OPEN por AccountStrategy
echo/operation (key account_id:account_strategy_id)
  1. guards locales baratos: signal válida, AccountStrategy existente, compatibilidad Strategy↔MM
  2. Instrument.calendar_ref → CalendarResolver(B)
     falta/no ready ⇒ CALENDAR_UNRESOLVED ⇒ sin Operation
  3. AdmissionRequest{
       request_id, account_id, account_strategy_id, signal_id,
       instrument_id, exchange, product_group,
       calendar_id/session_state/session_date/session_boundaries,
       evaluated_event_time
     }
     ↓
     echo/provider_rules(account_id)   # LINEARIZATION POINT Stage-1
       serializa request contra:
       - RuleSet efectivo / binding / entitlement
       - AccountState corriente
       - provider timezone/window/cutoff policy
       - daily/trailing/news risk state
       - DayBoundary authority/readiness
       - permitted instrument scopes
     ↓
     AdmissionResult{ALLOW|DENY_NEW_RISK, decision_id, rule_set_id/version, reason}
  4. DENY ⇒ ProviderDecision durable; NO Operation
  5. ALLOW ⇒ echo/operation re-chequea guards locales que pueden haber expirado mientras esperaba
     (valid_until / existencia del binding local de AccountStrategy); AdmissionResult conserva
     provenance de su punto de linearización
  6. ResolveExecutionContract(Instrument, Account.execution_binding_id) → ResolvedContract
     una sola lookup/validación; fallo ⇒ CONTRACT_RESOLUTION_FAILED ⇒ sin Operation
  7. pin contract_id + specs económicas + direction
  8. Operation CREATED (antes de MM/Orders)
  ↓
MoneyManagement
```

### R15 — authority y orden

`echo/provider_rules(account_id)` es la **única autoridad de aceptación provider**. El admission snapshot compactado/kache-fed sigue existiendo para fan-out temprano, observabilidad y reducción de carga, pero una lectura fresca de ese snapshot nunca reemplaza `AdmissionRequest`.

RuleSet/binding/account/risk/DayBoundary updates y AdmissionRequests se procesan en la misma cola account-keyed:

- `AdmissionRequest` procesado antes de `RuleSetUpdate v6` ⇒ ALLOW/DENY bajo v5 es válido y queda con provenance v5.
- `RuleSetUpdate v6` procesado primero ⇒ el request debe evaluar v6.
- no se promete simultaneidad física global: la cola del owner es el punto de linearización.

Un ALLOW no congela provider safety para siempre. Si la autoridad cambia después del result, Stage-2 + guard de egress + epoch/`ReservationRevalidate` siguen vigentes antes de cualquier efecto físico. Por eso un OPEN puede materializarse válidamente bajo v5 y luego no emitir ninguna Order bajo v6; eso no contradice Stage-1 porque el ALLOW fue correcto en su linearization point.

## 15. Integrated Order/reservation/egress flow

```text
MM produce Order request
  ↓
Stage-2 dentro de echo/operation
  a. PER_ORDER local
  b. shared caps:
     ExposureReservationRequest
       → echo/provider_rules(account_id)
       → decisión serializada en GROSS | NET_ABS | GROUP_WEIGHTED
       → GRANTED / DENIED
  c. GRANTED retiene Order PENDING_SUBMIT
  d. egress guard:
     account/entitlement/safety/trust state
     + epoch RuleSet/cap authority
     si epoch cambió → ReservationRevalidate en provider_rules
  e. VALID → egress EXACTLY_ONCE → adapter → venue
     INVALID → REJECTED{PROVIDER_GATE} + release
```

### Capacity authority — R16

`echo/provider_rules(account_id)` mantiene conceptualmente:

```text
firm_by_operation[operation_id] = {
  instrument_id,
  contract_id,
  product_group,
  cumulative_signed_exposure,
  last_operation_event_seq
}

live_reservations[request_id/order_id] = {
  operation_id,
  cap_family,
  scope,
  signed_requested_capacity,
  cumulative_filled_qty,
  finality_state,
  grant_epoch
}
```

La capacidad firme NO se infiere sólo de una Order que tuvo reserva. Después de **cada Fill Echo aceptado por D2-04**, sea ENTRY, ADD, REDUCE, EXIT, safety close o late/reconciled Fill, el operation owner emite en la misma frontera de checkpoint de ese Fill:

```text
CapacityStateUpdate {
  operation_id
  operation_event_seq
  instrument_id
  contract_id
  product_group
  cumulative_signed_exposure
  reservation_order_id?             # sólo si ese Order posee reserva
  reservation_cumulative_filled_qty?
}
```

El mensaje es cumulativo. `echo/provider_rules` guarda `last_operation_event_seq` por Operation e ignora replay/stale updates; cuando existe reservation component, actualiza **en la misma invocación account-keyed** la exposición firme y el consumo de esa reserva. Un Fill de salida no necesita reserva previa: el `cumulative_signed_exposure` basta para cambiar `firm_by_operation`. Partial exit sólo modifica capacity por el Fill real recibido; el intent de Order nunca libera firm capacity.

Métricas derivadas desde esa proyección, sin portfolio aggregate:

- **NET_ABS:** suma firmada por scope y aplica el envelope de reservas vivas de la familia.
- **GROSS:** `Σ abs(cumulative_signed_exposure por Operation)` por scope + contribución conservadora de reservas vivas. Dos Strategies opuestas `+4/-3` ⇒ NET_ABS 1 y GROSS 7.
- **GROUP_WEIGHTED:** las mismas contribuciones por Operation/reserva multiplicadas por pesos tipados del RuleSet sobre `product_group`.

La Operation sigue siendo owner de su lifecycle/exposición lógica. `firm_by_operation` es una **capacity projection autoritativa para enforcement** dentro del owner account-keyed, no otro aggregate.

### Reservation finality / modify / replace

Se conserva C-R2/C-R3: `CANCELLED/EXPIRED` no liberan por enum; `reservation.finality_state=PENDING_FINALITY` permanece hasta `VENUE_FINAL/ORDER_EXECUTION_FINAL`; FILLED consume; REJECTED venue-confirmado libera; modify-increase reserva delta antes de emitir; modify-decrease libera sólo tras ACK; replace usa reserva propia y mantiene la vieja hasta finality. `PENDING_FINALITY` NO es `Order.status`.

### Idempotency / skew

- request/result dedup por `request_id`;
- `CapacityStateUpdate` cumulativo + `operation_event_seq` ⇒ duplicate Fill replay no duplica firm capacity;
- Fill + emisión del CapacityStateUpdate son atómicos en la frontera del operation owner; aplicación ocurre después en provider_rules;
- grant/result es atómico dentro del owner provider_rules;
- ningún release ocurre por intención de salida, sólo por Fill/finality/ACK autorizados;
- skew conocido que vuelva la proyección física/lógica no confiable activa `PHYSICAL_STATE_UNTRUSTED` y corta NEW_RISK; no hay reconciliation repair.

Ejemplos: OPEN +4 seguido de exit Fill -2 ⇒ `firm_by_operation=+2`; S1 +4 y S2 -3 ⇒ NET_ABS=1/GROSS=7; reentrega del mismo update seq/cumulative ⇒ capacity idéntica.

## 16. Provider safety flow

```text
clock/calendar/account/risk/rule update
  → echo/provider_rules(account_id)

regla con flatten explícito
  → ProviderForceClose{account_id, decision_id, reason, rule_ref}
  → enumerate AccountStrategyRoutingIndex(account_id)
  → Send intent to EVERY echo/operation(account_id:account_strategy_id)
       ACTIVE binding
       DISABLED binding
       CLOSE_ONLY binding
     key sin Operation → no-op idempotente
     key con Operation → termination intent requested_by=SAFETY_PLANE
                        → cancel live Orders + close path
                        → TERMINAL sólo por guards D2-04
```

### R17 — deterministic fan-out

No existe wildcard StateFun y PG no participa de correctness. El fan-out usa el catálogo/config routing completo de AccountStrategies para la Account, disponible en el control-plane/kache que ya alimenta fan-out. V1 congela una regla de lifecycle simple: **disable es soft; la routing identity de una AccountStrategy no se hard-tombstonea mientras pueda poseer una Operation no terminal**. En práctica, el registro se conserva para safety fan-out durante la vida operativa de la Account; GC físico queda fuera del hot path y sólo puede ocurrir tras certificar que no existe Operation viva. Así provider_rules no necesita descubrir "sólo las vivas": envía a todas las keys conocidas y las vacías hacen no-op.

Caso obligatorio: Account A con AS1 ACTIVE+Operation, AS2 sin Operation y AS3 disabled+Operation. Forced-flat envía el mismo `decision_id` a AS1/AS2/AS3; AS1 y AS3 registran el termination intent, AS2 no-op. Replay es idempotente por `decision_id`/intent identity; ninguna Operation viva se omite.

Cambios sin safety intent siguen separados: instrumento prohibido/cap bajado ⇒ deny adds y revalidation; entitlement revoked ⇒ DENY_NEW_RISK + suspensión de emisión + `SUSPENDED_ENTITLEMENT` + operador, **sin ForceClose automático**. `ForceClose != TERMINAL` permanece literal.

## 17. Hot vs pinned semantics

| Clase | Elementos |
|---|---|
| **PINNED / SNAPSHOTTED** | `Operation.contract_id`; specs económicas del Contract embebidas en Operation; `direction`; config MM efectiva; snapshots de Calendar/RuleSet/DayBoundary inyectados en un run histórico. |
| **DYNAMIC / HOT** | InstrumentMapping corriente por binding; ProviderRuleSet; ProviderAccountBinding; AccountState; ExchangeCalendar live config; provider risk state; **DayBoundary efectivo Futures**; routing catalog de AccountStrategies. |
| **READ MODEL / OPTIMIZATION** | admission snapshot compactado/kache: prefilter + observabilidad, nunca linearization authority de Stage-1. |
| **PROVENANCE-ONLY** | `ProviderDecision.rule_set_id/version`, `admission_decision_id`, grant epoch, calendar/run hashes/snapshots, binding audit facts, DayBoundary config transition facts. |

### R15 hot admission ordering

`AdmissionRequest`, RuleSet/binding/account-state/risk/DayBoundary updates se serializan en `echo/provider_rules(account_id)`. El orden procesado define la autoridad efectiva del request. Un result ALLOW conserva esa provenance aunque un update posterior cambie la cuenta; Stage-2/egress es la defensa para comandos todavía no emitidos.

### R18 DayBoundary update ordering

El update de DayBoundary se procesa en esa misma cola. Al activarlo:

- acumuladores diarios actuales permanecen;
- no existe reset retroactivo ni reset provocado sólo por cambiar config;
- la config vieja deja de gobernar crossings futuros desde el linearization point;
- `next_reset_at` se recalcula prospectivamente con la nueva config usando como piso el boundary futuro ya comprometido/activation watermark, evitando ejecutar un segundo reset del mismo estado inmediatamente después de un reset anterior;
- el primer crossing qualifying bajo la nueva autoridad ejecuta un único reset.

Ejemplo: misma Account, reset viejo 16:00 CT, re-binding a 17:00 CT. Si el update se procesa antes de las 16:00, 16:00 viejo no se ejecuta y el próximo qualifying es 17:00. Si se procesa después de que 16:00 ya reseteó, no se crea un segundo reset a las 17:00 ese mismo ciclo; la próxima frontera nueva se agenda para el siguiente qualifying 17:00. La autoridad nueva jamás usa timezone vieja después de activarse.

No se crea `DayBoundaryVersion`: esto es config hot + estado mínimo del owner.

## 18. Provenance

`ProviderDecision` sigue siendo el fact mínimo con `decision_id, account_id, account_strategy_id?, operation_id?, kind, provider/program/phase?, rule_set_id/version, rule_family, reason, evaluated_at`.

Con R15, la decisión **Stage-1** nace en `echo/provider_rules` junto con `AdmissionResult` y sale por su egress transaccional; `echo/operation` sólo referencia el `decision_id` si finalmente materializa. Los DENY de shared-cap también nacen en provider_rules; un PER_ORDER local puede registrar su ProviderDecision en la frontera transaccional de operation. Operation guarda referencias, no snapshots de history.

DayBoundary re-binding/config update produce audit/provenance fact con config efectiva y activation instant; no crea entidad versionada. Calendar/run provenance y RuleSet snapshot-in-manifest permanecen como estaban. PG sigue siendo proyección eventual, nunca correctness/recovery authority.

## 19. LIVE / REPLAY / BACKTEST contract

La misma lógica de dominio pura se usa en los tres modos para Instrument/Contract, CalendarResolver/session_date, NamedTradingWindow, ProviderRuleSet evaluators, DayBoundary resolver, Strategy/Signal/MM y Operation semantics.

**LIVE** consume config hot. Stage-1 no acepta desde un snapshot eventual: siempre lineariza en `echo/provider_rules(account_id)`. DayBoundary live usa la config explícita del binding/rules, no el `DayBoundaryCache` mutable legacy.

**REPLAY/BACKTEST** inyecta inputs explícitos del run:

- Calendar snapshot payload + revision hash/transitions;
- ProviderRuleSet snapshot/provenance si se simula un programa;
- DayBoundary config inicial + transiciones efectivas de re-binding/reset authority;
- Contract/catalog inputs necesarios.

El resolver DayBoundary es el mismo concepto en live y offline: timezone IANA + reset local + reset semantics + transición prospectiva. Un replay nunca consulta el cache live ni el fallback UTC 23:00. Recorded streams/ordering general sigue siendo seam de D2 Market/Replay y no se diseña aquí.

## 20. D2-04 lifecycle integration

D2-04 permanece intacto:

- Operation se materializa antes de MM. Stage-1 es un **request/response de aceptación** previo a materialización; no crea otro aggregate.
- Operation owner sigue `account_id:account_strategy_id`; provider_rules no posee lifecycle, sólo admission/capacity/safety projection account-scoped.
- Stage-2 vive después de MM y antes de egress.
- Capacity updates derivados de Fills no mutan Operation: Operation emite su exposición cumulativa; provider_rules mantiene una proyección para enforcement.
- exits/safety closes siguen el lifecycle normal y sus Fills actualizan la capacity projection igual que entradas/adds.
- ForceClose sigue siendo termination intent; TERMINAL exige guards.
- Contract/MM snapshot permanece pinneado; hot rule/day-boundary/calendar/mapping updates no lo mutan.
- `PENDING_FINALITY` es reservation state, no Order.status; `SUSPENDED_ENTITLEMENT` es flag operacional.
- Fill truth sigue inmutable; late/reconciled fills actualizan Operation y capacity projection, nunca synthetic repair.
- Position sigue `Account+Contract` y trust guard; no se transforma en portfolio aggregate.

## 21. Echo V3 REUSE/EXTEND/ADAPT/REPLACE map

| Pieza V3 | Disposición final | Evidencia / razón |
|---|---|---|
| InstrumentSnapshot | REUSE legacy observation / no source-of-truth de specs nuevas | `v3/sdk/domain/snapshots.go` · `d319d0a3` |
| MMEngineFn | ADAPT hacia Contract pin explícito | `v3/core/internal/functions/mm_engine.go` · `e725ceb0` |
| SymbolMappingHandler / compacted config pattern | REUSE/EXTEND para nuevos catálogos | `symbol_mapping_handler.go` · `a9364d4a` |
| ConfigCache / kache | REUSE patrón readiness/read model; **admission kache no es authority Stage-1** | caches actuales |
| **DayBoundaryCache + prop_rulesets.daily_reset_*** | **REUSE concepto/cálculo local; ADAPT/REPLACE mecanismo para Futures** | `v3/core/internal/functions/account_sync.go` · blob `b0f8f1ce`: comentarios físicos dicen cache forever, sin TTL/invalidation porque fase nueva⇒account_id nuevo; además fallback UTC 23:00. Incompatible con ProviderAccountBinding re-binding in-place del mismo account_id. Futures usa hot config account-keyed en provider_rules, explicit/readiness-safe, sin fallback. |
| ExecutionPolicy | ADAPT/SPLIT | binding/MM/knobs legacy mezclados |
| StrategyConfigFn | REUSE patrón KVS config | `b89a9a1a` |
| AutomationEvaluatorFn / typed evaluators | REUSE patrón typed evaluation + egress | precursor de provider rules, autoridad distinta |
| ClientConfig / AccountState | REUSE input operativo; AccountState update debe llegar al owner provider_rules para R15 | `587eb5c4` |
| CloseHandler account-wide | REUSE patrón de acción safety, **no** descubrimiento de keys | fan-out nuevo usa routing index AccountStrategy, no PG/wildcard |
| `echo.prop_rulesets` legacy | REUSE concepto / REPLACE shape | sin program/version/provenance y acoplado al DayBoundary legacy |
| Provider domain / provider_rules / CalendarResolver / capacity projection / AccountStrategyRoutingIndex | NEW | no existen como dominio V3 |

La corrección R18 es explícita: ya no se clasifica DayBoundaryCache como REUSE directo de autoridad/cache. Sólo se reaprovechan semánticas/calculadores útiles; el cache/update contract se reemplaza para Futures.

## 22. Migration implications

Secuencia conceptual, sin big bang:

1. crear catálogos A/B/C y distribución hot/readiness-safe;
2. mantener symbol mappings/prop_rulesets legacy sólo para el path actual;
3. introducir CalendarResolver y ContractResolver Futures;
4. introducir `echo/provider_rules(account_id)` con RuleSet/binding/account-state/DayBoundary state;
5. publicar `AdmissionRequest/AdmissionResult`; kache admission queda prefilter/read model;
6. añadir capacity projection `firm_by_operation` + `live_reservations` y `CapacityStateUpdate` cumulativo desde cada Fill de Operation;
7. conservar reservation finality/modify/replace/egress revalidation;
8. materializar `AccountStrategyRoutingIndex` desde config y congelar soft-disable/routability para safety fan-out;
9. adaptar el DayBoundary Futures: dejar de usar lazy immutable cache/fallback; binding hot explícito → provider_rules;
10. safety intents account-wide se fan-out determinísticamente a todas las AccountStrategy keys;
11. replay/backtest recibe snapshots/transiciones de Calendar/RuleSet/DayBoundary, nunca caches live.

No se modifica el path legacy MT/Forex en este workstream. No se crea portfolio aggregate, workflow engine ni calendar service.

## 23. Risks/debts (consolidado)

- **Admission hop R15:** Stage-1 agrega un request/response account-keyed antes de materializar. Es costo de correctness; kache prefilter evita carga inútil. Medir latencia en D6.
- **Capacity projection R16:** `firm_by_operation` puede ir detrás del operation owner durante tránsito de mensajes. Updates son cumulativos/idempotentes; cualquier estado físico/lógico conocido como stale/mismatch activa `PHYSICAL_STATE_UNTRUSTED` y corta NEW_RISK. No auto-repair.
- **Opposite Operations:** GROSS requiere per-Operation exposure; NET_ABS y GROUP_WEIGHTED deben usar la métrica tipada del RuleSet. La proyección account-keyed puede crecer con #Operations vivas/históricas retenidas, acotable por cleanup después de terminal+finality.
- **Safety routing R17:** retener routing identities de AccountStrategy implica soft-delete/GC diferido. Es deuda operacional pequeña a cambio de cobertura determinista; hard GC no pertenece al hot path.
- **DayBoundary R18:** cambios de timezone/reset in-place requieren transición prospectiva y run provenance. El source legacy no sirve como autoridad hot; cualquier fallback UTC 23:00 en el camino Futures es defect.
- **Provider policy drift:** sigue siendo owner-managed; Echo no descubre cambios de firma automáticamente.
- **Venue finality trust:** unchanged; un venue que contradice history-by-tag produce breach fail-visible.
- **FX MM, old-contract behavior, calendar/tzdata history, UNKNOWN provider claims y deudas legacy pips/symbol mappings** permanecen como en los child artifacts; ninguna cambia por R15–R18.

## 24. Owner decisions

`OWNER DECISIONS REQUIRED: NONE`.

R15–R18 son correcciones técnicas dentro de autoridades ya congeladas. Quedan sólo ratificaciones de implementación: nombres físicos de mensajes/functions/topics/tables; shape exacto de `AdmissionRequest/Result`, `CapacityStateUpdate`, routing index y config DayBoundary; enums/reasons/provenance fields. Ninguna cambia identidad, lifecycle ni autoridad de producto.

## 25. Acceptance cases A–H + Primary Manager R15–R18

### A–H originales

- **A — rollover manual:** Operation A pin NQZ6; mapping hot a NQH7 sólo afecta B nueva; A nunca retargetea.
- **B — feed/execution IDs:** Strategy usa NQ; feed/exec bindings e identifiers difieren sin contaminar Strategy.
- **C — exchange open/provider blocks:** Session OPEN no basta. Stage-1 `AdmissionRequest` se lineariza en provider_rules; DENY ⇒ no Operation.
- **D — forced flat:** intent fan-out determinista a todas las AccountStrategy keys; Operation TERMINAL sólo por guards D2-04.
- **E — early close:** Calendar override + snapshot de run reproducen session boundary/date.
- **F — Account DayBoundary:** reset account-scoped no modifica ExchangeSession ni Contract; Futures usa config hot explícita, no cache forever.
- **G — RuleSet update:** decisiones nuevas ven la versión según orden account-keyed; grants no emitidos revalidan; Operation conserva Contract/MM snapshot.
- **H — old Contract:** REDUCE/CLOSE sigue contract pinneado; venue rejection visible; nunca remap.

### R15-A — hot deny before OPEN

`provider_rules` procesa v6=DENY y luego `AdmissionRequest`. La cola account-keyed evalúa v6 ⇒ DENY; no Operation.

### R15-B — OPEN linearizes before update

`AdmissionRequest` procesa ALLOW bajo v5; después llega v6. El result conserva v5 provenance y Operation puede materializar si sus guards locales siguen válidos. Antes de efecto físico, Stage-2/egress usa autoridad corriente/epoch; v6 puede impedir la Order. Race semánticamente definida.

### R16-A — reduction updates capacity

Operation firm +4. EXIT Fill -2 actualiza exposición lógica a +2 y emite `CapacityStateUpdate{cumulative_signed_exposure:+2}`; provider_rules reemplaza el valor cumulativo ⇒ firm capacity +2. Intent sin Fill no cambia capacity.

### R16-B — opposite Strategies

S1 exposure +4 y S2 -3 bajo la misma Account: `firm_by_operation={S1:+4,S2:-3}`. NET_ABS = |+1| = 1; GROSS = |4|+|−3| = 7. No portfolio aggregate.

### R16-C/D — replay + partial exit

Mismo `operation_event_seq`/cumulative update reaplicado ⇒ no cambio. Partial exit sólo reduce `cumulative_signed_exposure` por la qty realmente filled.

### R17 — forced-flat full coverage

AS1 ACTIVE+live, AS2 empty, AS3 disabled+live. Routing index contiene las tres identities; ForceClose se envía a las tres. AS1/AS3 registran intent, AS2 no-op. Replay mismo decision_id es idempotente. PG no se consulta.

### R18 — binding changes DayBoundary

Mismo account_id: old 16:00 CT → re-binding 17:00 CT. Update se lineariza en provider_rules, preserva acumuladores y reemplaza autoridad prospectiva; no se vuelve al cache legacy. Si 16:00 aún no ocurrió, el boundary viejo deja de gobernar y el próximo qualifying es 17:00. Si 16:00 ya reseteó, el update no dispara otro reset a 17:00 ese mismo ciclo; agenda el siguiente qualifying 17:00. Falta/invalid config ⇒ DAY_BOUNDARY_UNRESOLVED + DENY_NEW_RISK. Replay inyecta la misma transición.

## Evidencia

- Child artifacts A/B/C permanecen sin cambios en este repair; se consumen como autoridad congelada.
- Echo baseline físico re-verificado: `372af59a7b83604781346613da01e3d510ea1360`.
- R18 contrastado contra `v3/core/internal/functions/account_sync.go` blob `b0f8f1ce`: `DayBoundaryEntry` documenta "Cache forever" porque fase nueva implica account_id nuevo; `DayBoundaryCache` es lazy DB sin invalidación y cuentas sin ruleset usan UTC 23:00. Esa semántica es incompatible con re-binding Futures in-place y queda clasificada ADAPT/REPLACE para el path nuevo.
- D2-04 R1–R14 permanece autoridad de Operation/Order/Fill/Position, M1/M2, finality y recovery.

## Handoff

```text
D2-05 REPAIR STATUS:
READY_FOR_MANAGER_REVIEW

INTEGRATED ARTIFACT:
main/10-projects/Echo Futures/Echo Futures — D2-05 Instrument Session Provider.md

AGENTS-OS SHA:
<PIN_AFTER_COMMIT>

R15 ADMISSION AUTHORITY:
Stage-1 ya no acepta desde kache. AdmissionRequest/Result se lineariza en
echo/provider_rules(account_id), en la misma cola que RuleSet/binding/account/risk/DayBoundary
updates. Kache queda prefilter/read model. Request antes de update usa autoridad vieja con
provenance; update primero obliga autoridad nueva. Stage-2/egress revalidation permanece.

R16 CAPACITY PROTOCOL:
provider_rules mantiene firm_by_operation + live_reservations. Cada Fill Echo, incluidos
REDUCE/EXIT/safety/late fills, produce CapacityStateUpdate cumulativo con operation_id,
operation_event_seq, instrument/contract/product_group y cumulative_signed_exposure; replay
es idempotente. NET_ABS deriva net firmado; GROSS suma abs por Operation; GROUP_WEIGHTED
aplica pesos. Reservation consumption/finality sigue por Order sin portfolio aggregate.

R17 FORCE-CLOSE FANOUT:
provider_rules enumera AccountStrategyRoutingIndex completo por account (ACTIVE/disabled/
close-only) y envía el intent a cada key account:strategy. Key sin Operation = no-op;
disabled+Operation recibe intent. Routing identity se retiene/soft-disable mientras pueda
existir Operation viva. PG no participa; replay por decision_id es idempotente.

R18 DAYBOUNDARY:
DayBoundaryCache legacy = REUSE conceptual / ADAPT-REPLACE mecanismo. Futures exige config
DayBoundary explícita hot/readiness-safe en provider_rules; sin autoridad => DAY_BOUNDARY_UNRESOLVED
+ DENY_NEW_RISK, sin UTC 23:00. Re-binding se lineariza account-keyed, preserva acumuladores,
recalcula próximo qualifying boundary prospectivamente y no usa timezone vieja después de
activarse. Mismo resolver/config transitions son inyectables en replay/backtest.

CHILD ARTIFACTS CHANGED:
NO

ARCHITECTURE DELTA:
Stage-1 correctness pasa al owner account-keyed; capacity state pasa de per-order implícito a
proyección cumulativa por Operation + reservas; safety fan-out deja de asumir discovery de
keys vivas; DayBoundary Futures deja de depender del cache legacy immutable. Instrument,
Contract, Calendar, Provider domain, Operation lifecycle, pinning y AccountStrategy no cambian.

OWNER DECISIONS REQUIRED:
NONE

RESIDUAL RISKS:
latencia de Admission/Reservation hops; lag de capacity projection se vuelve fail-closed cuando
la base física/lógica es untrusted; routing identities requieren GC diferido; DayBoundary hot
transitions requieren tests de DST/re-binding; provider policy drift sigue owner-managed.

NEXT:
Primary Manager review only.
```


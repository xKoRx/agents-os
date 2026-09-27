---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D1 Analysis Pack]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
aliases:
  - Echo Futures D2-05B
  - EF Session Calendar
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-design
created: "2026-09-26"
updated: "2026-09-26"
---

# Echo Futures — D2-05B Session / Calendar

> [!info]+ Workstream D2-05B
> Diseño técnico V1 de `ExchangeCalendar / ExchangeSession / session (trade) date / NamedTradingWindow` y sus seams con `ProviderProgram` (TOP C), `Instrument/Contract` (TOP A), Account DayBoundary y el contrato de barras para D2-06. Autoridad de evidencia: `main/30-resources/futures/CONTRACT + SESSION SEMANTICS — AUTHORITATIVE EVIDENCE.md` (Front E, `Q7_EVIDENCE = SUFFICIENT`). Respeta sin reabrir D2-01 (snapshot + contract pinning), D2-02 (fan-out + single Operation), D2-03 (Signal + Strategy/MM boundary) y el lifecycle congelado de [[Echo Futures — D2-04 Operation Order Fill Position]]. Baseline físico verificada: `xKoRx/echo origin/master = 372af59a7b83604781346613da01e3d510ea1360` (fetch re-verificado, sin delta). No implementa código productivo, no cierra D2-05 y no avanza a D2-06. Este artefacto REEMPLAZA el draft auto-autorizado previo del SUBMANAGER (marcado inválido en commits `ce05b46b`/`e536718e` del vault); su contenido fue descartado y ninguna conclusión de este documento proviene de él.

## SUBMANAGER REPAIR — 2026-09-26 (B-R1 / B-R2)

- **R-B1 (session identity vs product-group overrides):** la versión review introducía `product_groups[]` en el calendario y `applicable_groups[]` en los overrides, con resolver `(calendar_id, instant, group)` pero `session_id = (calendar_id, session_date)` — dos groups con early closes/special sessions/breaks distintos producían dos `ResolvedSession` distintos con el MISMO session_id. Reparado por la **familia A**: un `ExchangeCalendar` representa exactamente UN grupo producto/sesión semántico; la dimensión `product_group` desaparece del calendario y del API del resolver. Dos semánticas distintas = dos `calendar_id` distintos ⇒ la colisión de identidad es estructuralmente imposible. Ediciones: §3.1 (shape + cardinalidad), §3.2 (precedencia + resolver sin `group`), §5, §7 (primitivas sin `group`), §12 (seam TOP A/C), §13 (caso B-R1-CASE-1; ejemplo del caso E ajustado), §14-R5.
- **R-B2 (revision_hash: pin real vs drift detection):** la versión review afirmaba a la vez que el run registra `{calendar_id → revision_hash}` y que "el resolver acepta el anchor como pin de dataset", sin mecanismo que recupere el dataset antiguo — un hash sólo detecta drift. Reparado cerrando la semántica del anchor por la vía SÍ-reproducible: **el anchor es el par `(revision_hash, snapshot_payload)`** (más la secuencia de transiciones si el run consumió >1 versión) **grabado en el manifiesto del run**; el resolver nunca recibe un anchor — recibe un **dataset inyectado**; recuperar el anchor = leer el manifiesto. Garantía exacta definida y acotada; sin servicio de revisiones ni framework (§10, caso B-R2-CASE-2).

## 1. Verdict

`D2-05B_STATUS: READY_FOR_SUBMANAGER_REREVIEW` (repair B-R1/B-R2 incorporado; partes aceptadas del review no reabiertas)

- El modelo V1 es un **calendar dataset configurado por el owner + un resolver puro en proceso**. No hay calendar microservice, no hay segundo market runtime, no hay engine de exchange-calendar ontology, no hay framework genérico de revisiones (espíritu D2-01).
- Las tres autoridades del mandato quedan congeladas por separado y nunca se fusionan: **ExchangeSession/ExchangeCalendar** (cuándo acepta negociación el exchange/producto), **ProviderProgram trading window/forced-flat** (overlay restrictivo del prop, TOP C) y **Account DayBoundary** (reset diario contractual de la cuenta, dominio Echo existente). La evidencia S-E06/S-E07/S-E08 lo exige; el caso Topstep (flat 3:10 PM CT con NQ abierto hasta 4:00 PM CT) lo demuestra.
- Time authority: **IANA timezone semantics** (`America/Chicago`, `America/New_York`, `Europe/London`), jamás offset UTC fijo (S-E02). Instants persistidos en UTC RFC3339Nano; reglas de schedule persistidas como hora local de pared + nombre IANA.
- El calendario es **datos, no fórmulas**: weekly base recurrente + overrides fechados (cierre feriado, early close, special open) con precedencia explícita. El trade date lo asigna cada sesión como dato (`trade_date_shift`); no existe fórmula universal CME (Front E: `UNKNOWN_GENERALIZATION`).
- `NamedTradingWindow` es **config referenciable por `window_id`** desde Strategy (dos kinds: subset de calendario exchange, o ventana de reloj propia), resuelta por fecha/DST vía IANA; la disponibilidad efectiva de una Strategy es la **intersección** ventana ∩ exchange, y un exchange cerrado siempre gana.
- El seam de Provider es **read-only**: el provider rule gate (TOP C) consume primitivas del `CalendarResolver` (estado de sesión, session_date, próxima transición) y compone sus propias ventanas/cutoffs; el overlay jamás muta `ExchangeSession` ni el calendario.
- Account DayBoundary permanece siendo la autoridad existente de Echo (`prop_rulesets.daily_reset_timezone` IANA + `daily_reset_time` + `DayBoundaryCache`); se reutiliza, se mantiene fuera del calendario de exchange, y el **fallback silencioso UTC-23:00 queda prohibido para cuentas Futures** (fail-closed).
- Determinismo LIVE/REPLAY/BACKTEST: resolución pura de `(calendar_id, instant)` sobre un dataset inyectado; los datos son append-fechados con hash de snapshot y el anchor de un run es **el snapshot grabado en su manifiesto** (hash + payload), no un puntero: una rerun puede re-materializar exactamente el dataset histórico, y una corrección posterior del calendario nunca cambia silenciosamente un replay ya corrido (§10).
- `OWNER DECISIONS REQUIRED: NONE`. Toda la decisión es técnica bajo los requisitos owner ya congelados ([[Echo Futures]] §Trading Sessions/Calendario, Q7). Quedan ratificaciones técnicas ordinarias para el manager: nombres físicos de tablas/topics/campos (§10), nombres del API del resolver (§3/§7) y el requisito de tzdata embebida en el build (§2).

## 2. Time authority (congelado)

- **Regla:** toda hora de schedule (open/close/break/reset/cutoff) se expresa como **hora local de pared en una zona IANA nombrada** y se transforma a instantes en el momento de resolver. Prohibido persistir, configurar o hardcodear offsets fijos (`UTC-6`, `GMT+2`) en cualquier capa del camino nuevo: la evidencia S-E02 y el §14 de Front E lo clasifican como INFERENCE_FOR_ECHO obligatoria (CST/CDT cambia el offset dos veces al año).
- **Resolución:** Go `time.LoadLocation(IANA)` (patrón ya usado en `strategy_history.go::validateHistoryTimezone` y en gateway `automation/executor.go` MEN-1). **Requisito de build (congelado):** los binarios Core/Gateway/backtester importan `_ "time/tzdata"` para que las reglas DST se resuelvan idénticamente en todos los nodos (Linux Zeus/Hera/Kronos **y Windows Kronos**, donde el tzdata del OS no está garantizado). La versión de tzdata queda fijada por la release (verificable en D6); un cambio de regla civil (p. ej. abolición de DST) entre la corrida live y un replay posterior es riesgo residual aceptado y visible vía el anchor de §10, no se persigue versionando tzdata por evento (YAGNI).
- **Reloj:** toda semántica de mercado (resolución de sesión de un evento de feed/ejecución, bucketing de barras, transiciones de sesión) consume el **instant del evento** (event-time del venue/feed ya presente en contratos D2-04: `executed_at`, `TimestampMs`); los gates sin evento de mercado (admisión de riesgo, ventanas de provider) consumen event-time de Core (`NowFunc`, patrón existente). Clock skew queda en diseño de implementación, igual que R8 de D2-04; no cambia el modelo.
- **Cuatro conceptos de tiempo distintos, jamás colapsados** (frozen vocabulary):

| Concepto | Definición | Autoridad |
|---|---|---|
| `instant` | timestamp UTC del evento/decisión (RFC3339Nano) | venue/feed/Core event-time |
| `civil_local_date` | fecha civil del instant en una tz IANA nombrada | derivado por IANA |
| `session_date` / trade date | fecha operativa que el exchange atribuye a una sesión; puede diferir de la civil (domingo 17:00 CT → trade date lunes, S-E01) | dataset del calendario (§4) |
| `account_day` | día contractual de la cuenta delimitado por su reset horario | DayBoundary de la cuenta (§8) |

- La Strategy nunca resuelve horas ni offsets: recibe ventanas/contexto ya resueltos (§6). Un cambio de DST dentro de una sesión no requiere caso especial: la sesión sigue corriendo y los instantes de sus boundaries ya fueron resueltos por IANA.

## 3. Calendar model (congelado)

### 3.1 Shape de datos

```text
ExchangeCalendar {
  calendar_id          — identidad canónica (ej: "CME_GLOBEX_EQUITY_INDEX")
  exchange             — ej: "CME"
  timezone             — IANA del calendario (ej: "America/Chicago")
  weekly_base[]        — schedule recurrente semanal:
      { start_weekday, start_local_time, close_local_time(|+días), breaks[], trade_date_shift }
  overrides{}          — overrides fechados, key = civil date local de INICIO de sesión:
      { kind: HOLIDAY_CLOSED | EARLY_CLOSE | SPECIAL_SESSION,
        open_local?, close_local?, breaks[]?, session_date?,
        corrected_at }
  calendar_version     — monotónico; revision_hash = sha256 del snapshot completo
}
```

- **Cardinalidad congelada (repair B-R1): un ExchangeCalendar representa exactamente UN grupo producto/sesión semántico.** No existe la dimensión `product_group` dentro del calendario ni selectors por grupo en overrides/resolver: dos product groups con schedules que difieren (o pueden diferir) son **dos `calendar_id` distintos**, cada uno con su dataset completo. N Instruments pueden compartir un `calendar_id` sólo si son el mismo grupo semántico; si divergen, el owner crea un calendario nuevo y rebindea (hot, prospectivo — §14-R5). Esta cardinalidad es lo que hace sesuda la identidad de §3.2 sin ontology ni taxonomía de groups.
- `trade_date_shift` es el dato que resuelve el trade date sin fórmula universal: para NQ todas las filas weekly_base llevan `trade_date_shift = +1` (sesión que arranca domingo 17:00 CT → trade date lunes), cubriendo S-E01 con data en lugar de regla. Un override que define una sesión especial debe llevar `session_date` explícito.
- `breaks[]` son ventanas cerradas **internas** a una sesión (productos con lunch/mid-session break). Los gaps entre sesiones (p. ej. el maintenance CME 16:00–17:00 CT de NQ) NO se modelan como break interno: en el dataset NQ cada sesión es `[17:00 → 16:00(+1)]` y el maintenance es simplemente el hueco entre sesiones consecutivas. El estado BREAK queda en el modelo para productos que lo necesiten; para el calendario equity index CME el dataset no define breaks internos.
- Constraints V1 (congeladas, declaradas en el modelo): **una sesión por trade date por calendario**; sesiones consecutivas pueden quedar separadas por gaps de mantenimiento. Un producto futuro que exigiera dos sesiones por trade date extiende el modelo con `session_seq`, sin cambiar el resto.
- No asumo fórmula CME universal ni precargo décadas de datos (Front E §16): el dataset V1 cubre el weekly base + overrides vigentes y futuros conocidos; el owner administra las filas igual que hoy administra el symbol mapping y el rollover manual.

### 3.2 Precedencia de resolución (congelada)

```text
para (calendar_id, civil_date D local de inicio de sesión):
  1. overrides[D] si existe → esa fila gana completa
  2. si no existe override → weekly_base por start_weekday = weekday(D)
  3. si ninguna fila aplica → CLOSED (NO_SESSION) para esa fecha
```

- El override es **reemplazo total del schedule del día** (close temprano, cierre completo o sesión especial), no un patch de campo: menos ambigüedad, mismo patrón de "el dato específico gana" que usa D2-04 para venue-authoritative state.
- La resolución es una **función pura** del paquete de dominio `sdk/calendar` (Go puro, sin imports de Kafka/StateFun/PG — mismo boundary Q14 que D2-04):

```text
SessionState = { OPEN | BREAK | CLOSED }
ResolvedSession(calendar_id, instant) →
  { state, session_id, session_open_utc, session_close_utc, session_date,
    breaks_utc[], next_transition_utc, next_transition_kind }
```

- `CLOSED` distingue `in_break` (pertenece a la sesión que lo contiene; session_date asignado) de `no_session` (ninguna sesión lo posee; `session_date` nulo). `next_transition_utc` es la materia prima para timers de cierre de sesión y para el seam de provider (§7), **calculada siempre desde el dataset — prohibido un timer live con horas hardcodeadas**.
- Identidad de sesión: `session_id = (calendar_id, session_date)`. Con la cardinalidad repair B-R1 (un calendario = un grupo semántico; una sesión por trade date por calendario) es **unívoca por construcción**: dos sesiones semánticamente distintas viven en `calendar_id` distintos y jamás comparten session identity, aunque compartan la misma session_date civil/trade date (caso B-R1-CASE-1). Es la clave que D2-06 usará para barras session-scoped.

### 3.3 Distribución (igual al patrón existente)

- Fuente de verdad: PG (`echo.exchange_calendars`; overrides embebidos en la fila como JSONB — un snapshot por `calendar_id`). El Gateway publica el snapshot completo al topic compactado `echo.exchange-calendars.v1` (key = `calendar_id`, tombstone en delete), siguiendo exactamente el patrón hot-update de `symbol_mapping_handler.go`; el consumo en proceso es kache (compacted topic → memoria, ready channel). Sin I/O en el hot path de decisiones.

## 4. Session / trade date semantics (congelado)

Cadena canónica de resolución:

```text
event instant (UTC)
   → (calendar_id del Instrument, §12)
   → local wall clock en calendar.timezone (IANA, DST-aware)
   → sesión contenedora según weekly_base/overrides + precedencia §3.2
   → session_date (dato de la sesión, no fórmula)
```

- Una sesión que **comienza el día civil anterior** a su trade date se cubre con `trade_date_shift = +1` (S-E01: Sunday session → Monday trade date). Las cuatro fechas del §2 permanecen distintas y cada consumidor usa la que corresponde: bars session-scoped usan `session_date`; el reporte humano usa `civil_local_date`; el reset de cuenta usa `account_day`; el timestamp físico es siempre `instant` UTC.
- Instante **dentro de un break interno** → `state = BREAK`, session_date de la sesión contenedora (la sesión sigue siendo la misma; para trading es no-abierta).
- Instante **entre sesiones** (maintenance CME) → `state = CLOSED(in_break=false)`, sin session_date. Regla congelada para consumidores: un instante entre sesiones **no abre ni extiende bucket de sesión**; el evento se registra con métrica fail-visible (`EVENT_OUTSIDE_SESSION`) y ningún barrado session-scoped lo fabrica (§9).
- Un override de feriado puede **reasignar el trade date** de una pre-open dominical (caso demostrado en CME notices): por eso el override lleva `session_date` explícito en vez de heredar el shift recurrente ciegamente.

## 5. Holiday / early-close / maintenance — precedencia (congelada)

- Precedencia completa: `override fechado > weekly base` (§3.2). La exigencia S-E05 (schedules pueden diferir por product group) se satisface **por cardinalidad** (repair B-R1): cada grupo que difiere tiene su propio `calendar_id` con sus propias filas; no existe contaminación posible porque no hay semántica por-group dentro de un calendario. No existe tercer nivel (p. ej. override de contract): la granularidad mínima es el calendario del grupo; nada material en la evidencia exige per-contract.
- Los overrides son **filas fechadas**: el row de ayer no cambia cuando se agrega el de mañana (§10 determinismo). CME finaliza su calendario ~2 semanas antes del feriado (Front E §16): la ventana de corrección real es corta y la política congelada es: overrides de fechas futuras son editables libremente; una corrección sobre una fecha ya operada se aplica como nueva versión de la fila con `corrected_at` y bump de `calendar_version` — visible por hash, nunca reescrita en silencio.
- Early close: el override define `close_local` (y opcionalmente breaks); todo lo que sigue al close temprano es `CLOSED`. Holiday: `kind = HOLIDAY_CLOSED` cierra la fecha; la sesión siguiente es la del próximo weekly start (u otro override). Special session (p. ej. apertura dominical adelantada con trade date post-feriado): `kind = SPECIAL_SESSION` con open/close/`session_date` completos.
- Los horarios concretos de cada feriado son **datos owner-managed** con CME first-party como autoridad externa (`cmegroup.com/trading-hours` + notices); este diseño no congela ninguna fecha específica. Los valores usados en los casos §13 son ilustrativos del mecanismo, no afirmaciones de calendario real 2026.

## 6. Named Strategy windows (congelado)

- `NamedTradingWindow` es **config pura referenciable**, no un engine: identity = `window_id` canónico (`"NY_OPEN"`, `"LONDON"`, `"CME_ETH"`, `"CME_RTH"`, o custom del owner); vive en `echo.trading_windows` (PG) distribuido por topic compactado `echo.trading-windows.v1` (mismo patrón §3.3); la Strategy lo referencia por id en su config — **cero offsets en Strategy** (requisito owner).
- Dos kinds, deliberadamente simples:

```text
NamedTradingWindow {
  window_id
  kind: EXCHANGE_SUBSET | CLOCK
  // EXCHANGE_SUBSET: recorta sesiones de un ExchangeCalendar
  calendar_id, local_open, local_close   // dentro de la sesión del exchange
  // CLOCK: ventana de reloj propia, independiente de exchange
  timezone (IANA), local_open, local_close, weekdays[]
}
```

- `EXCHANGE_SUBSET` (ej: `CME_RTH` = 08:30–15:00 CT dentro de la sesión CME) hereda por construcción feriados/early closes/maintenance del calendario: nunca excede availability.
- `CLOCK` (ej: `NY_OPEN` = 09:30–10:00 America/New_York; `LONDON` = 08:00–17:00 Europe/London) se resuelve por fecha civil en su propia tz. **Regla congelada de interacción:** la disponibilidad efectiva de la Strategy es `window_open ∧ exchange_session_open(contract del Instrument)` — un exchange cerrado (feriado, maintenance, early close) gana siempre aunque la ventana de reloj esté abierta. El §19 de Front E es la evidencia: la misma semántica de calendario gobierna la interpretación de la ventana.
- Una ventana que excede availability no es error: la intersección simplemente la recorta, con **warning de validación de config** al guardarla (técnico, no owner decision).
- Contexto que el StrategyEngine entrega a la Strategy en cada evaluación (frozen contract, sirve a S1): `WindowContext { window_open_utc, window_close_utc, window_date (civil en tz de la ventana), session_date (si hay exchange bound), session_state }`. S1 resuelve su opening range con `NY_OPEN` (CLOCK 09:30–10:00 ET) + intersección con la sesión CME del NQ: si el exchange abre tarde o hay feriado, la ventana simplemente no se materializa ese día.
- Eventos de transición (session/window open-close) que StrategyEngine pueda consumir (event cadence D1: "session open/close/holiday transition") se derivan **exclusivamente** de `next_transition_utc` del resolver (timers calculados, nunca hardcodeados). Quién materializa esos eventos en el stream es decisión D2-06/Strategy runtime; D2-05B congela que la fuente de verdad de la transición es el resolver.

## 7. Provider overlay seam (congelado — para TOP C)

- D2-05B **no diseña** `ProviderRuleSet`; deja el contrato de input/output para que TOP C exprese `Exchange = OPEN ∧ Provider = NO_NEW_RISK` y forced-flat **sin tocar `ExchangeSession`**.
- Lo que `CalendarResolver` ofrece al provider rule gate (read-only, determinístico, idéntico en los tres modos):

```text
SessionState(calendar_id, instant)          → OPEN | BREAK | CLOSED(+detalle)
SessionDate(calendar_id, instant)           → session_date | null
SessionBoundaries(calendar_id, instant)     → open_utc, close_utc, breaks_utc[]
NextSessionTransition(calendar_id, instant) → (utc, OPEN_START | SESSION_END | BREAK_START | BREAK_END)
```

- Lo que el provider posee y compone por fuera del calendario (datos de TOP C): su allowed window (absoluta o como offsets sobre boundaries del exchange), su forced-flat cutoff y su resume time. Ejemplos de composición legal con las primitivas: "flat 15:10 CT todos los días" = cutoff propio del provider, el gate consulta `SessionState` en ese instant para saber si el exchange estará abierto; "flat 15 min antes del close" = cutoff derivado de `SessionBoundaries(...).close_utc`; early-close day con auto-liquidación (Topstep holiday policy) = el provider lee el close temprano desde `SessionBoundaries` y aplica su política de offset sobre él.
- Invariante congelado: **el overlay nunca escribe** el calendario ni `ExchangeSession`; `Exchange = OPEN ∧ Provider window closed` es un estado alcanzable y representable por construcción (evidencia S-E06/S-E07). El resultado de la denegación de riesgo nuevo y del forced-flat es un asunto del plano provider/safety: el forced-flat entra al state owner de D2-04 como **intent de terminación** (`ForceClose`, R3 — jamás TERMINAL instantáneo), no como evento de calendario.

## 8. Account DayBoundary separation (congelado)

- Autoridad real auditada en Echo V3: `prop_rulesets.daily_reset_timezone` (IANA, default `America/Chicago`) + `daily_reset_time` (default 16:00) en migración baseline; `DayBoundaryCache`/`DayBoundaryEntry` en `account_sync.go` detecta el cruce de día (`calculateDayStart` = reset local en tz del ruleset, persistido como instant UTC), guarda `prev_day_close` y alimenta `daily_hwm_*`; el `EnrichedAccountSnapshot` entrega esos datos al `AutomationEvaluatorFn` (RFC-005) que evalúa reglas diarias sin I/O.
- **REUSE como autoridad separada:** `account_day` sigue definiéndose por reset horario del ruleset, sin consultar jamás el calendario de exchange. Daily HWM, daily loss y cualquier regla diaria del provider consumen `account_day`, nunca `session_date`; un early close o feriado **no mueve** el reset diario de la cuenta (es un término contractual del programa, no un hecho de mercado).
- **Lo que NO hereda Futures:** el fallback silencioso de cuentas sin ruleset (`UTC + 23:00` hardcodeado en `DayBoundaryCache`) queda **prohibido en el camino Futures**: un AccountStrategy Futures exige day boundary explícito en su config (fail-closed en la validación del binding, `ACCOUNT_DAYBOUNDARY_REQUIRED`). El path legacy MT sigue funcionando como hoy; no se muta.
- La separación es bidireccional: el reset de cuenta puede ocurrir con el exchange abierto o cerrado (caso F, §13), y ninguna de las dos transiciones toca a la otra ni a la Operation (D2-04: el account snapshot es contexto de MM, no mutador del lifecycle).
- KISS: no se mueve `DayBoundary` al paquete `sdk/calendar`; sigue siendo primitiva del dominio de cuenta (`account_day(instant) → day_key`), extendida sólo con la validación fail-closed de arriba.

## 9. Bar contract para D2-06 (congelado — sin diseñar bar builder)

**Congelado por D2-05B:**

1. El bucketing **puede** consultar `CalendarResolver`; el bucketing session-scoped **debe** usar `session_id = (calendar_id, session_date)` como identidad de sesión — prohibido bucket por medianoche UTC o civil date sin session context (Front E §19).
2. Ningún bucket **cruza** un boundary de open/close ni un break interno; una transición a `BREAK`/`CLOSED` cierra la barra forming en ese boundary. Qué pasa al reabrir (continuación vs nueva barra) es decisión de D2-06.
3. Holiday/early close afectan boundaries **sólo a través del dataset** (§5); la lógica de barras no contiene conocimiento de feriados.
4. LIVE/REPLAY/BACKTEST resuelven boundaries con **el mismo resolver + el dataset anclado del run** (§10); un modo distinto jamás infiere boundaries por regla propia.
5. Un evento en `CLOSED(no_session)` no fabrica bucket; métrica fail-visible `EVENT_OUTSIDE_SESSION`.
6. La transición de sesión es fuente de eventos open/close **sólo** vía `next_transition_utc` (§6): prohibido un scheduler con horas hardcodeadas que compita con el resolver.

**Decide D2-06 (explícitamente NO congelado aquí):** alineación de buckets intra-sesión, visibilidad de forming bars, política de late/out-of-order events y corrección de closed bars, consolidación multi-timeframe, warmup/persistencia del estado de barras. D2-04 ya reservó recorded streams/ordering para el workstream D2 Market/Replay; este contrato no reabre eso.

## 10. LIVE / REPLAY / BACKTEST determinism (congelado)

- **Source of truth:** PG owner-managed (`echo.exchange_calendars`, `echo.trading_windows`); distribución hot por topics compactados (`echo.exchange-calendars.v1`, `echo.trading-windows.v1`) vía Gateway→Kafka con el patrón symbol-mapping (publish + tombstone), cache en proceso vía kache con ready channel (patrón RFC-007/`ConfigCache`). Sin I/O remoto en el hot path; el resolver es paquete puro alimentado por el snapshot en memoria.
- **Startup readiness fail-closed:** hasta que el dataset de los calendarios referenciados esté cargado, la evaluación de Strategy y la admisión de riesgo nuevo quedan bloqueadas con `CALENDAR_NOT_READY` (métrica + gate), igual filosofía que el whitelist RFC-007. Prohibido defaultear a 24×7 o "assume open" ante calendario ausente; un Instrument sin binding de calendario resoluble es `CALENDAR_UNRESOLVED` y bloquea igual (fail-closed, §12).
- **Replay de ayer no depende del calendario mutable de hoy — semántica del anchor cerrada (repair B-R2):** el dataset es append-fechado (overrides por fecha; fechas pasadas no se mutan, se corrigen como nueva versión con `corrected_at` + bump de `calendar_version`). El anchor de un run **NO es un puntero que el resolver resuelva**: es **el snapshot grabado en el manifiesto del run** — `{calendar_id → (revision_hash, snapshot_payload)}`, más la secuencia ordenada de transiciones `(hash, snapshot_payload, effective_from)` si el run consumió más de una versión. El registro es **obligatorio para todo proceso que consuma calendarios para decisiones**: un run offline lo graba al inyectar su dataset; un proceso live lo graba al arrancar y en cada hot update que consume (provenance del run). Recuperar el dataset del anchor = leer el manifiesto (snapshots JSON de KBs; retention = la del propio run artifact; sin servicio de revisiones, sin framework).
- **API sin anchors (repair B-R2):** el resolver recibe **un dataset inyectado**, nunca un anchor — live/kache sirve el snapshot actual; REPLAY/BACKTEST inyecta el snapshot (o la secuencia de snapshots) grabado en el manifiesto para reproducibilidad exacta, o el actual para una rerun what-if deliberada. No existe `resolver(anchor)`: no hay API que físicamente no pueda recuperar lo que promete.
- **Garantía exacta congelada:** re-inyectar el snapshot grabado en el mismo resolver produce **byte-idénticas** las session boundaries, session_dates, boundaries de barras y resoluciones de ventanas del run original. Lo que NO garantiza: (a) reproducir decisiones de un proceso que consumió el calendario sin registrar provenance (el registro es obligatorio por contrato, pero no retroactivo a procesos que no lo cumplieron); (b) idéntica resolución de tzdata/regla civil entre releases distintas (residual §2/R2 — el manifiesto registra también el identifier de release/tzdata para hacer esa divergencia visible); (c) el anchor vive y muere con el retention del run artifact. Una corrección posterior sigue siendo append-versionada: la rerun con dataset actual diverge del hash grabado ⇒ visible y atribuible, nunca silenciosa. No hay stamps de calendario por evento ni snapshots por tick (YAGNI; la ventana de corrección real es corta, §5).
- El hot update del mapping/calendario afecta **decisiones nuevas** (nuevas evaluaciones, nuevas barras); no retargetea barras cerradas ni Operaciones vivas — misma filosofía D2-01 (pin al crear, cambios prospectivos).
- El backtester futuro inyecta `Clock`/event-time y el dataset; el resolver es el mismo binario de dominio (Q14 boundary: paquete puro sin infra).

## 11. Echo V3 disposition (source audit, baseline `372af59a`, blobs verificados)

| Pieza V3 | Disposición | Evidencia física (path · blob · razón) |
|---|---|---|
| `DayBoundaryCache` / `DayBoundaryEntry` / `calculateDayStart` / `parseResetTime` | **REUSE (patrón+autoridad) / EXTEND** (validación fail-closed de day boundary explícito; prohibir fallback UTC-23:00 en camino Futures) | `v3/core/internal/functions/account_sync.go` · `b0f8f1ce` · lines 33–86 entry+cache, 300–320 `calculateDayStart`, 273–298 parse; fallback UTC 23:00 en 45–50 y `CheckAndUpdateDayCrossing` |
| `prop_rulesets.daily_reset_timezone` / `daily_reset_time` | **REUSE** (schema authority del account day; ya IANA) | `v3/sdk/postgres/migrations/001_schema_baseline.up.sql` · lines 643–644 |
| `AccountSnapshot` / `EnrichedAccountSnapshot` | **REUSE intacto** (transporte de datos de día para reglas diarias; sin coupling a calendario) | `v3/sdk/domain/snapshots.go` · `d319d0a3` · lines 16–43 y 283–310 |
| `AutomationEvaluatorFn` + `core/internal/automation/evaluator.go` | **REUSE** (consume daily HWM/prev-day-close enriquecido; no toca calendario) | `v3/core/internal/functions/automation_evaluator.go` · `9503410e`; `v3/core/internal/automation/evaluator.go` · `bf97b13a` |
| kache (`sdk/kache`) | **REUSE** como cache de lectura de calendars/windows | `v3/sdk/kache/README.md`, `v3/sdk/kache/account_configs.go` · `2991979b` |
| `ConfigCache` core (RFC-007, ready channel, fail-closed) | **REUSE (patrón)** para readiness de calendario (`CALENDAR_NOT_READY`) | `v3/core/internal/config_cache.go` · `eecc6f9e` |
| Gateway `SymbolMappingHandler` (Hasura event → topic compactado + tombstone) | **REUSE (patrón)** para hot update de calendars/windows | `v3/gateway/internal/symbol_mapping_handler.go` · `a9364d4a` · lines 42–175 |
| `validateHistoryTimezone` + instants RFC3339Nano (strategy history) | **REUSE (precedente)** de validación IANA y convención de instants UTC | `v3/sdk/contracts/strategy_history.go` · `e43bc48b` · lines 713–723 |
| Gateway automation `ScheduleActionExecutor` (MEN-1 tz-safe, fallback UTC) | **REUSE (precedente)** de `LoadLocation`; su fallback UTC con warning es pattern aceptable sólo para scheduling interno, **no** para semántica de trading | `v3/gateway/internal/automation/executor.go` · line 396 |
| Concepto exchange calendar/session/trading-hours | **NEW** (no existe en V3; grep `trading_hours|exchange_calendar|ExchangeCalendar` = 0 hits) | repo `372af59a` |
| `module.yaml` ingress/egress + topics `echo.*.v1` | **REUSE (mecanismo)** para registrar los 2 topics nuevos | `v3/core/deploy/flink-statefun/develop/module.yaml` |

- `account_sync.go` (el hot path actual de day-crossing) queda **intacto** en V1 para el path MT legacy; el camino Futures exige day boundary explícito en config del binding (§8) — es EXTEND de validación, no refactor del existing.

## 12. Contracts for A / C (seams que deben respetar)

**TOP A — Instrument/Contract (seam semántico post-repair B-R1):**
- El requisito semántico es **un binding resoluble 1:1 Instrument → calendar_id**: cada Instrument resuelve exactamente un calendario (el de su exchange/product-session group); N Instruments pueden compartir el mismo `calendar_id` sólo si son el mismo grupo semántico. La forma del campo la fija TOP A en su repair — `calendar_ref` directo en Instrument o `(exchange, product_group) → calendar_id` mapeado son formas equivalentes y aceptables; D2-05B no impone nombres de campos, sólo exige: resoluble en el mismo hot-config snapshot que el mapping Instrument→Contract (un solo join en kache), 1:1, y **sin dimensión de grupo dentro del calendario** (dos groups con schedules que divergen = dos calendar_ids; prohibido re-introducir `applicable_groups`/selectors).
- Fail-closed: Instrument sin binding resoluble ⇒ `CALENDAR_UNRESOLVED`; Strategy no evalúa y risk no admite (no default a 24×7).
- El pin de `contract_id` en Operation (D2-01) **no pinnea calendario**: si un rollover cambia de Contract dentro del mismo grupo semántico, el calendario es el mismo; si un día existiera contrato de otro grupo, es una Operation nueva (nuevo pin) que resuelve su calendario al crearse. Session semantics de una Operation viva no muta por hot updates.

**TOP C — Provider/Program/RuleSet:**
- El provider rule gate consume **sólo** las primitivas read-only de §7 (sin parámetro de grupo: el `calendar_id` del Instrument ya identifica la semántica completa); la ventana allowed y el forced-flat cutoff son datos del ProviderProgram (su propia config, su propia tz/offsets), nunca filas del calendario de exchange.
- `Exchange OPEN ∧ Provider NO_NEW_RISK` debe ser representable sin mutar `ExchangeSession`; la denegación es del gate, no del calendario.
- Forced-flat ⇒ intent `ForceClose` al state owner D2-04 (R3): nunca TERMINAL instantáneo, nunca un "session close event" que terminalize Operaciones.
- Si una regla diaria del provider (daily loss) necesita día, usa `account_day` (§8), no `session_date`.

## 13. Casos obligatorios

### Caso C — Exchange OPEN + provider blocks (S-E06/S-E07)

Martes 15:30 CT sobre NQ (calendario `CME_GLOBEX_EQUITY_INDEX`, sesión arrancada lunes 17:00 CT, trade date martes): `SessionState` → `OPEN`, `session_date = martes`, `close_utc` = 16:00 CT. ProviderProgram (Topstep Express, ilustrativo) tiene forced-flat 15:10 CT ⇒ su gate deniega la admisión de un nuevo OPEN Signal con `NO_NEW_RISK`; `ExchangeSession` **permanece OPEN** (16:00), el calendario no se muta, y las Operaciones ya vivas siguen gestionándose por D2-04 hasta el intent de forced-flat, que llega como `ForceClose` (intent, no TERMINAL instantáneo). Un OPEN Signal a las 15:05 CT (antes del cutoff) pasa el gate del provider y sigue su camino normal: las dos autoridades conviven en el mismo instant sin colapsar.

### Caso E — Early close (override cambia boundary; LIVE y REPLAY resuelven igual)

Fila override en el calendario `CME_EQUITY_INDEX` (valores **ilustrativos** del mecanismo, no calendario real): `{date: 2026-12-24, kind: EARLY_CLOSE, close: 13:15 CT, session_date: 2026-12-24}`. LIVE: evento 13:14 CT → `OPEN` (close resuelto 13:15); evento 13:16 CT → `CLOSED(no_session)`, `EVENT_OUTSIDE_SESSION` si algún feed emite; `NextSessionTransition` apunta a la apertura dominical 17:00 CT del día 27 (trade date lunes 28). REPLAY de ese día con el mismo `calendar_id` + dataset anclado (§10): mismas filas, mismas resoluciones, mismos boundaries de barras — el bucketing cierra el día en 13:15 por la cláusula 2/3 del §9. Si el owner corrige el close a 13:30 **después** de haber corrido el replay, `calendar_version` sube y el hash del manifiesto del replay diverge: la diferencia es visible, no silenciosa.

### Caso F — Account day reset distinto del exchange close

Cuenta con ruleset `daily_reset_timezone = America/New_York`, `daily_reset_time = 17:00` (ilustrativo de un reset 5 PM ET contractual). 17:00 ET = 16:00 CT: `DayBoundaryCache.CheckAndUpdateDayCrossing` detecta el cruce, persiste `prev_day_close`, resetea `daily_hwm_*` y `EnrichedAccountSnapshot` se lo entrega al evaluator (RFC-005) — en el mismo instant el exchange entra a su gap de mantenimiento (16:00–17:00 CT), y las dos transiciones son **independientes**: ninguna consulta a la otra. Dirección opuesta: domingo 18:00 ET (17:00 CT) abre la nueva sesión de exchange con trade date lunes mientras el `account_day` de esa cuenta aún no cruzó (cruzó a las 17:00 ET del domingo): el HWM diario sigue reflejando el día contractual, no el session_date del exchange. No se modifica `ExchangeSession`, no se cambia el Contract, y una Operation viva no sufre ninguna mutación por el reset de cuenta (sólo cambia el contexto de riesgo que MM lee).

### Caso B-R1-CASE-1 — dos groups con early close distinto no colisionan (repair B-R1)

Dos product groups del mismo exchange con early closes distintos el mismo día D (valores ilustrativos): equity index cierra 13:15 CT y rates cierra 12:00 CT. Bajo la cardinalidad repair B-R1 son **dos filas de calendario distintas** — `CME_EQUITY_INDEX` y `CME_RATES` — cada una con su propio override para D (13:15 y 12:00 respectivamente). `ResolvedSession("CME_EQUITY_INDEX", D 12:30)` → `OPEN` con `session_id = (CME_EQUITY_INDEX, D)` y close 13:15; `ResolvedSession("CME_RATES", D 12:30)` → `CLOSED(no_session)` — la jornada de rates ya terminó a las 12:00 y su `session_id` fue `(CME_RATES, D)`. Ambos comparten session_date D y **jamás comparten session identity**: la colisión del defecto B-R1 es estructuralmente imposible porque un calendario ya no puede expresar semántica distinta por group — la dimensión no existe en el modelo ni en el API. Si mañana los dos groups divergen en un feriado adicional, el owner corrige cada calendario por separado; si un owner decide que dos grupos son el mismo grupo semántico, comparten `calendar_id` y por definición comparten TODA la semántica — no hay estado intermedio posible.

### Caso B-R2-CASE-2 — rerun con anchor X tras corrección de feriado (repair B-R2)

Run original R1 (replay/backtest) inyectó el snapshot S1 (hash h1) de `CME_EQUITY_INDEX`, cuyo override de la fecha F decía `HOLIDAY_CLOSED`; el manifiesto de R1 grabó el anchor `{CME_EQUITY_INDEX → (h1, S1)}`. Después el owner corrige: F era en realidad `EARLY_CLOSE 13:15` ⇒ nueva versión S2 (hash h2, `corrected_at` posterior). **Rerun inyectando el anchor grabado (S1):** boundaries **byte-idénticos** a R1 — F cerrado completo, sin barras ese día, mismas session_dates adyacentes — porque el resolver es el mismo binario de dominio y el dataset es el mismo snapshot (garantía exacta §10). **Rerun con dataset actual (S2):** boundaries distintos — F opera hasta 13:15 — y los hashes h1 (manifiesto R1) ≠ h2 (manifiesto R2) hacen la divergencia **visible y atribuible**, jamás silenciosa. Lo que la rerun con X **NO** garantiza: (a) reproducir decisiones de un proceso live que consumiera el calendario sin registrar provenance — el registro es obligatorio por contrato pero no retroactivo; (b) idéntica resolución de reglas civiles/tzdata si la rerun corre sobre una release distinta — visible por el identifier de release/tzdata del manifiesto, no recuperable (residual §2); (c) persistencia más allá del retention del run artifact — el anchor vive y muere con su manifiesto (declaración operacional; no hay store de revisiones).

## 14. Riesgos / unknowns

- **R1 — Calidad del dataset owner-managed:** un override faltante o erróneo produce boundaries incorrectos y no es detectable automáticamente (misma clase de riesgo que un symbol mapping equivocado hoy). Mitigación: fail-closed en readiness/unresolved, warnings de validación de config, hash visible en runs; residual aceptado por KISS y consistente con el modelo operacional owner (rollover manual).
- **R2 — tzdata:** la corrección DST depende del tzdata embebido por release; un cambio de regla civil entre live y replay es residual visible-por-anchor pero no corregible sin nueva release (§2). Verificación de build (import `_ "time/tzdata"` en Windows Kronos) es requisito de D6.
- **R3 — Semántica de cutoffs provider heterogéneas:** absolutas, offsets sobre close, "N min antes del close" y políticas de early-close conviven (evidencia Topstep/Lucid en D1); D2-05B garantiza las primitivas, pero la correcta composición por programa es riesgo/carga de TOP C — si una regla no es expresable con las primitivas de §7, debe escalar antes de congelar D2-05C.
- **R4 — Eventos en tiempo cerrado:** feeds reales pueden emitir durante maintenance/entre sesiones (settlement prints, timestamps sucios); la regla es determinística (no fabrica bucket, métrica), pero el volumen esperado y su tratamiento en el feed path es de D2-06/TOP de feed.
- **R5 — Divergencia entre grupos que compartían calendario (post repair B-R1):** si dos productos que operaban sobre el mismo `calendar_id` necesitan schedules distintos, el owner crea un calendario nuevo con dataset completo y rebindea los Instruments afectados (hot, prospectivo); la historia anterior al split era idéntica por definición, así que el rebind no altera semántica histórica. No se pre-construye merging/inheritance entre calendarios.
- **R6 — Reloj/admisión:** los gates sin evento de mercado usan event-time de Core; clock skew entre nodos puede mover un gate por el borde del cutoff (mismo residual que R8 de D2-04; implementación, no modelo).

## 15. Owner decisions

`OWNER_DECISIONS_REQUIRED = NONE`. El diseño vive dentro de los requisitos owner ya congelados (sesiones nombradas sin offsets, igualdad LIVE/REPLAY/BACKTEST, hot config, KISS/YAGNI, cross-market no futures-locked — el modelo no usa nada futures-specific: calendario+ventanas son genéricos). Ratificaciones técnicas ordinarias para el manager (no cambian semántica): (1) nombres físicos `echo.exchange_calendars` / `echo.trading_windows` / `echo.exchange-calendars.v1` / `echo.trading-windows.v1`; (2) firma del API del resolver en `sdk/calendar`; (3) requisito de build `_ "time/tzdata"`; (4) el campo `revision_hash` como anchor de run para replay/backtest.

## Evidencia

- Vault: [[Echo Futures]] (requisito Trading Sessions/Calendario; Q7; decisiones D2-01/02/03; reviews D2-04), [[Echo Futures — D1 Analysis Pack]] (Front E manager synthesis; blocking refactor register #4; DayBoundaryCache no reemplaza session), `main/30-resources/futures/CONTRACT + SESSION SEMANTICS — AUTHORITATIVE EVIDENCE.md` (matriz S-E01..S-E09; §12–§19; fuentes CME/ProjectX/Topstep first-party listadas en su §26).
- Repo físico: clon `~/aranea/work/d4-shot1-20260925/echo`, `git fetch` re-verificado con `origin/master = 372af59a7b83604781346613da01e3d510ea1360`; blobs citados en §11 vía `git rev-parse 372af59a:<path>`.
- Externas (vía Front E): CME trading hours + Globex holiday calendar + notice 2026-04-20 (Sunday→trade date), Topstep allowed trading times/forced-flat + holiday hours, ProjectX realtime contract identity.

## Handoff

```text
D2-05B STATUS: READY_FOR_SUBMANAGER_REVIEW

ARTIFACT: main/10-projects/Echo Futures/Echo Futures — D2-05B Session Calendar.md

ECHO BASELINE: 372af59a7b83604781346613da01e3d510ea1360 (sin delta, fetch re-verificado)

CALENDAR MODEL: ExchangeCalendar = dataset config owner-managed (weekly_base recurrente +
overrides fechados HOLIDAY_CLOSED/EARLY_CLOSE/SPECIAL_SESSION con applicable_groups; key de
override = civil date local de inicio de sesión) + resolver puro sdk/calendar sin I/O.
Precedencia congelada: override fechado > weekly base > CLOSED(NO_SESSION) fail-closed.
Sesión = [open, close] con breaks internos opcionales; una sesión por trade date (V1).
session_id = (calendar_id, session_date); distribución hot = patrón symbol-mapping
(Gateway → topic compactado + tombstone → kache). Sin microservice, sin segundo runtime.

FROZEN TIME SEMANTICS: IANA-only (prohibido offset fijo; tzdata embebida por release).
Event-time del evento/Core para toda resolución (skew = implementación). Cuatro conceptos
separados: instant UTC / civil_local_date / session_date (dato de la sesión, trade_date_shift,
sin fórmula universal) / account_day (reset del ruleset). S-E01 cubierto por dato
(Sunday 17:00 CT → session_date lunes). Entre sesiones = CLOSED(no_session): nada fabrica
bucket; BREAK interno conserva session_date.

BAR CONTRACT FOR D2-06: session-scoped bars usan session_id (prohibido midnight/civil sin
session context); ningún bucket cruza open/close/break (break cierra forming; resume lo
decide D2-06); feriados/early-close sólo via dataset; misma autoridad+anchor en
LIVE/REPLAY/BACKTEST; CLOSED(no_session) no fabrica bucket (métrica fail-visible);
transiciones de sesión sólo vía next_transition_utc (timers calculados, no hardcodeados).
NO congelado (decide D2-06): alineación intra-sesión, forming visibility, late/corrections,
multi-TF, warmup/persistencia.

ECHO V3 REUSE/ADAPT: DayBoundaryCache+prop_rulesets REUSE como autoridad account_day
separada (EXTEND: day boundary explícito fail-closed para Futures; fallback UTC-23:00
prohibido en camino nuevo, path legacy intacto); EnrichedAccountSnapshot+automation
REUSE intacto; kache/ConfigCache ready-channel REUSE como distribución+readiness;
symbol_mapping_handler REUSE como patrón hot-update; strategy_history IANA/RFC3339Nano
REUSE como precedente; calendario/sesión/ventanas = NEW (no existen en V3).

CONTRACTS FOR A/C: TOP A — binding (exchange, product_group)→calendar_id a nivel Instrument
(sin session data en Contract; sin pin de calendario en Operation; CALENDAR_UNRESOLVED
fail-closed). TOP C — gate provider consume sólo primitivas read-only del resolver
(SessionState/SessionDate/SessionBoundaries/NextSessionTransition); allowed window y
forced-flat son datos ProviderProgram; forced-flat = intent ForceClose D2-04 (R3), jamás
TERMINAL instantáneo; reglas diarias del provider usan account_day, no session_date.

OWNER DECISIONS REQUIRED: NONE (ratificaciones técnicas manager: nombres físicos, firma
del resolver, tzdata embebida, revision_hash como run anchor).

MATERIAL RISKS: dataset owner-managed incorrecto no auto-detectable (hash/anchor lo hace
visible); tzdata residual ante cambio de regla civil; composición de cutoffs heterogéneos
es carga de TOP C; eventos en tiempo cerrado requieren tratamiento en feed path (D2-06).
```

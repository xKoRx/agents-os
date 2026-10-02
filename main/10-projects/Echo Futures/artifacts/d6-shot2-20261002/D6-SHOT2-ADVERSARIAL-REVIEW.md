# Echo Futures — D6 Shot 2 — Final Adversarial Implementation Review

**Shot:** D6 Shot 2 — ADVERSARIAL REVIEW (independiente, sobre el candidato Shot 1)
**Role:** TOP Independent Adversarial Reviewer / Principal Futures Execution Systems Auditor (no implementador, no Manager, no Owner; sin cambios de código, sin remediation)
**Date:** 2026-10-02
**Project:** [[Echo Futures]]
**Trigger:** `D6_SHOT1_IMPLEMENTATION = READY_FOR_ADVERSARIAL_REVIEW` @ `0e9741a5` (post F-MGR-01/02/02B)
**Verdict:** `D6_SHOT2_ADVERSARIAL = REMEDIATION_REQUIRED` (0 BLOCKER · 2 HIGH · 8 MEDIUM)

---

## 1. Candidate identity

| Item | Value | Verification |
|---|---|---|
| Repository | `xKoRx/echo`, worktree `~/aranea/work/d6-shot1-20261001/echo` | working tree limpio durante todo el review |
| Branch | `feature/d6-shot1-execution-vertical` | local == `origin` |
| Expected HEAD | `0e9741a56afe6911e52480fb9f2fe86a47aae427` | `git rev-parse` — **MATCH** |
| Diff base | `f0c82905d4eaf825c08e04f0bb97cab73e616ba5` (N1 baseline) | `git merge-base f0c82905 0e9741a5 = f0c82905` ⇒ FF puro |
| Delta | 76 archivos, +10,850 / −152 | `git diff --stat` — coincide con lo declarado |
| Review scope | diff completo `f0c82905..0e9741a5` + autoridades congeladas + N1/C1 evidencia + estado DEV | |

Authorities consumed: D6 Final Design Freeze (2026-10-01) §1–§17; D6-SHOT1-IMPLEMENTATION + F-MGR-01/02/03 + F-MGR-02B; N1 physical evidence (read-only vertical + final binding); C0/C1/C1-R1; GAU50 preflight artifacts (`d6-earn2trade-preflight-20260930/`: PASS-1, PREFLIGHT, PASS-2); D4/D5 frozen contracts (via freeze §0/§2).

## 2. Methodology

- Lectura directa del núcleo de ejecución: `adapters/ninjatrader/adapter.go` (962 líneas, completo), `helpers.go`, `internal/session/session.go` (completo), `adapters/journalfs/journal.go` (transiciones + `sameIntent` + fsync), `core/ntx/{server,frame,observations}.go`, diffs del stack STOP_MARKET (`domain/operation.go`, `operation/{engine,mm,wire}.go`, `gerardmm.go`, `capabilities/adapter.go`, `futuresruntime/runtime.go` envelope), `internal/binding/loader.go`.
- 4 líneas de auditoría paralelas independientes (mismo SHA verificado): (H/I) GAU50 rules vs fuente first-party + timezone/DST; (G/J/K) freshness/warm-up/replay adversarial; (N) reproducción independiente de la cobertura changed-logic; (L/O/P/Q) AddOn authority, compatibilidad C# estática, egress-disabled y scope.
- Ejecución read-only: suites `go test -race -count=1` del candidato; reproducción de los 3 coverprofiles; ETCD DEV vía MCP read-only (list por existencia exacta — el fuzzy-matching conocido del MCP se neutralizó verificando la existencia de cada clave con `list_keys` antes de leer valor).
- No se mutó producto, ETCD, deployment ni configs; no se instalaron AddOns; `ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0` durante el review.

## 3. Adversarial matrix A–Q (resumen; detalle §4–§9)

| Frente | Veredicto | Evidencia clave |
|---|---|---|
| A Account identity | **PASS** | Name-primary con unique-match + cross-check Id en las 4 superficies (AddOn staged `EchoExecutionAddOn.cs:812-830`, feed AddOn `678-710`, hello defence + `VerifyBinding` `adapter.go:205-219`, `domain/provider.go:396` Validate fail-closed); drift ⇒ `PROVIDER_ACCOUNT_ID_DRIFT` degradación, jamás remap; ETCD real: `provider-account-ref="RJARA114411201551"` (exacta, size 17), `provider-external-account-id` sigue como hint. Wrong account ⇒ REJECTED fail-closed en AddOn (529-533) y MISMATCH ⇒ lane no resuelta |
| B Double submit | **PASS** | Dedup en el bridge ANTES de todo side-effect: `HasPhysicalIntent` → `DUPLICATE_SUBMIT_SUPPRESSED` + reconcile (`session.go:308-341,374-385`; ATP EXE-04); at-most-once por autorización de journal (`adapter.go:612-653,732-735`); Reconcile nunca resubmite (`784-787`); `ResubmitApprovedByAbsence` inalcanzable en lane V1; AddOn sin dedup pero server-side garantiza 1 frame (buffer-1 waiter + map-delete elimina double-resolve; seq tracker rechaza frames duplicados). Ningún ordering legal produce doble submit físico. Crash windows: PREPARED-crash ⇒ resubmit legal por identidad idéntica (`Prepare` idempotente + `sameIntent` con StopPrice); SUBMITTING-crash ⇒ AMBIGUOUS; ctx-cancel ⇒ record SUBMITTING → barrier → AMBIGUOUS |
| C M1/M2 | **PASS** | Secuencia física exacta: capability gate pre-journal (`adapter.go:553`) → `Prepare` fsync (`journal.go:220-227`) → `RecordEvidence` → `MarkSubmitting` fsync (`606`) → lane write punto-de-no-retorno (`612`); VENUE_BOUND sólo con orders-family + `Order.OrderId` nativo (`411-416`), jamás por `command_result` (`629-631`); fsync antes de cada retorno mutante (`journal.go:176-178`); transiciones con guardas de estado y sin regresión (`283-357`); command_result antes que observación = ACCEPTED evidencia de transporte only; observación antes que result = VENUE_BOUND correcto; reject tardío sobre TERMINAL = no-op (`404-406`) |
| D STOP_MARKET | **PASS** (con gate G-STOP pendiente Shot 3 por diseño) | Pila completa: enum + `Order.StopPrice` + Validate dual (stop requerido, limit prohibido) en domain/engine/capabilities → `OrderCommand.StopPrice` → envelope `stop_price` (`runtime.go:293,308`) → `sameIntent` con nivel (`journal.go:240`) → GerardMM `protectiveOrder` emite `STOP_MARKET/StopPrice` (`gerardmm.go` diff) con tighten monotónico contra `StopPrice` (`503-513`); crossed→MARKET intacto (`TerminalReasonProtectiveStopCrossed`; lados opuestos por dirección); STOP_MARKET excluido de `SupportedOrderTypes` (`adapter.go:152`) y rechazado **pre-journal** (`551-556`); AddOn mapea `OrderType.StopMarket` nativo 1:1, sin síntesis ni transformación; sin client-side stop |
| E Cancel/Replace/Late fill | **PASS** | Fill-gana-carrera: fills dedup por `ExecutionId` (`adapter.go:438-443`) y conservados aunque la orden muera; terminal no regresa (`journal.go:327-329`, `adapter.go:404`); cancel duplicado post-restart ⇒ `REJECTED "cancel target not found"` (sin efecto); replace duplicado reenvía términos idénticos (NT Change in-place = físicamente idempotente); tighten-vs-fill race: fill ⇒ TERMINAL, replace posterior ⇒ REJECTED limpio; qty con partial fill: semántica absoluta NewQty + avail por MM |
| F Reconciliation | **PASS** | found→VENUE_BOUND/TERMINAL; PREPARED-absent ⇒ `not_sent` (nunca autorizado); absent+fills ⇒ TERMINAL por historial con fills recuperados; absent+MAY_HAVE_EXECUTED ⇒ `MarkAmbiguous` + `M2_UNRESOLVED_ABSENCE` (`adapter.go:864-875`); VENUE_BOUND desaparecido del venue ⇒ AMBIGUOUS (VENUE_BOUND ∈ `MayHaveExecuted`, `journal.go:34-38`) — coincide con §5.5 fail-visible; UnknownLiveOrders ⇒ quarantine fail-visible, nunca cancel/adopt, y mantiene NEW_RISK off (`session.go:477-484`); lanes V1 jamás prueban negación autoritativa |
| G Market freshness | **FAIL (F-S2-02 HIGH)** + MEDIUM | Núcleo sólido: fold max monotónico, age > liveness, UNKNOWN fail-closed en 3 superficies, pinning por stream demandado, 600s⇒STALE⇒0 señales E2E genuino. **Vector "fresh event_ts but dead transport": VULNERABLE** — evaluación input-driven sin timer + liveness desactivado ⇒ feed muerto-silencioso queda FRESH congelado (F-S2-02) |
| H GAU50 rules | **PASS** (1 EVIDENCE_GAP documentado) | Cap GROSS 6 / ventana 15:50 CT half-open / DD 2000 EOD-trailing — CORRECTOS vs PASS-1:99/83/117/400; DLL 1100 5pm-5pm CT open+closed+commissions correcto en kind/monto/ventana, basis `INITIAL_BALANCE` sin declaración first-party (F-S2-06); consistency `breached ⟺ best_day×100 ≥ 30×total` con `big.Rat`, ==30% ⇒ BREACHED **CORRECTO** ("30% or more" PASS-1:403 + "must be below 30%" PASS-1:80); monitoring-only verificado (BREACHED ⇒ admission ALLOW, `consistency_test.go:138-152`; cero refs en admission/reservation/sweepSafety); total≤0 ⇒ UNDETERMINED; sin división ni overflow |
| I Account state/time | **PASS con F-S2-05 MEDIUM** | `time.LoadLocation` + tzdata embebido + wall-clock por instante ⇒ DST correcto por construcción (sin test de transición — nota); day-boundary del engine delegado al ingester (stateless, replay-safe). **Config real ETCD desalineada**: `day-boundary-tz=America/New_York` + reset `17:00` ⇒ boundary 16:00 CT vs ciclo 5pm CT del programa (F-S2-05) |
| J Warm-up/REBUILD | **PASS con F-S2-07 MEDIUM** | Bucketing `Truncate(5m)` alineado, offsets 0/60/120/299s deterministas, OHLC verificado contra el fold REAL, dup/out-of-order fail-closed, 51 H4 + 20×5m fail-closed, anchor digest sellado sobre todo el corpus (determinista, tamper-probado), candidates-antes-de-RUN_START, cero `time.Now()`, byte-determinismo probado. **Gate de cobertura cuenta presencia, no completitud** (F-S2-07) |
| K EXACT_REPLAY/BACKTEST | **PASS con F-S2-08 MEDIUM** | EXACT_REPLAY seguro por construcción (capture-as-consumed + replay exclusivo del corpus + driver envenenado); sentinel `""` compone byte-idéntico D5 (3 tests). BACKTEST: freshness mode-blind (F-S2-08), hoy inerte (reloj cabalga event_ts) pero sin test de invarianza |
| L AddOn authority | **PASS con F-S2-01 HIGH (staged)** | Cero autoridad de dominio (validación = term-shape + binding identity only); mismatch ⇒ REJECTED fail-closed; grep discipline feed AddOn intacto (sólo inversión de identidad permitida). **F-S2-01**: reconnect del AddOn de ejecución resetea `execSeq=0` con session persistente ⇒ tracker rechaza todo ⇒ lane funcionalmente muerto (fail-closed) |
| M Protocolo `echo.ntx.v1` | **PASS con F-S2-04 MEDIUM** | hello-first + constant-time token + deadline 5s; 64KB cap; seq por sesión estricto; malformed/oversized ⇒ reject+drop; idle timeout; correlación por command_id con waiter buffer-1 (sin deadlock por resultado tardío); WriteCommand valida antes de escribir. **Sin fencing de sesión activa**: una conexión vieja aún viva puede seguir inyectando frames (requiere token + doble conexión) |
| N Coverage claim | **PASS** | Reproducido independiente: raw 1202/1279 = **94.0%** (declarado 94.1%), ajustado con sólo exclusiones verificadas legítimas **98.4% ≥ 95%** (penalizando futuresvertical: 98.0%). FF range correcto. 17 statements gap real: ninguno en rules engine ni dedup; destacables: happy-path propagación LIMIT/STOP al frame nunca testado (`adapter.go:575-586`), `ParseAccountData` happy-path, swallows de journal sin documentar (`414-415,422-423`) |
| O Compatibilidad NT 8.1.8.3 | **PASS (estático) / PHYSICAL_DEFERRED** | Firmas == superficie refleccionada §3 (CreateOrder 10-arg, Submit/Cancel/Change(IEnumerable), OrderAction, TIF); mapping 1:1 sin transformación; `Order.Id` session-scoped sólo como feedback; `order.Name` retention correctamente diferida a G-ID-Retention. **Riesgo físico Shot 3**: `CreateOrder/Submit/Cancel/Change` desde `execReader`/Timer threads sin Dispatcher marshaling (feed AddOn usa el patrón correcto); AddOn sin `SetDefaults/Name`. No se declara ejecución física certificada |
| P Egress disabled | **PASS — STRUCTURALLY_DISABLED (4 barreras independientes)** | (1) capability gate: M2 mandatorio todo UNKNOWN ⇒ `StaticEligible=false` ⇒ §22 jamás abre; STOP_MARKET rechazado pre-journal; (2) sin proceso/servicio del bridge (verificado ps+systemd); (3) ETCD: `futures-bridge/accounts` (lista de sesiones) **NO EXISTE** ⇒ splitCSV("") = 0 cuentas incluso con binario; binding presente pero no consumido; (4) AddOn ejecución staged NO instalado; feed AddOn en lane write-only sin familia de comandos. No es "nadie lo llamó aún" |
| Q Scope creep | **PASS con F-S2-09 MEDIUM** | Diff mapea 1:1 al scope §15 (§3+§5+§6+§4.2+§9+§10+carried fixes); Must-NOT respetados; cero provider-code en Strategy/MM; warm-up 711 LOC proporcionado; guard anti-drift razonable. **F-S2-09**: binario ELF 33.4MB commiteado accidentalmente en `14b0d72b` |

## 4. Findings

Estándar aplicado: sólo defectos que amenazan materialmente correctness / safety / recoverability / replay / provider-rule compliance / physical execution / frozen semantics. Sin findings de estilo.

---

### F-S2-01 — HIGH — AddOn de ejecución (staged): seq rewind en reconnect inutiliza el execution lane

**CONTRACT / INVARIANT VIOLATED:** Freeze §11 "AddOn reconnect | … seq discipline rejects stale/duplicate frames" presupone que tras un reconnect el lane se recupera y re-sincroniza; el comportamiento implementado convierte todo reconnect en degradación permanente hasta restart de NT. Área del pass standard: execution transport / recovery.

**EVIDENCE:** `v3/futures-bridge/addon-ninjatrader/EchoExecutionAddOn.cs:424` — en reconnect, `execSeq = 0` mientras `execSessionId` persiste (creado una vez, línea 56). El bridge exige seq estrictamente monótonica por sesión (`adapter.go:269` → `tracker.Accept`; `ntfeed/tracker.go:64-67` rechaza `seq <= LastSeq` como anomalía).

**FAILURE TIMELINE:** (1) AddOn conecta, sesión `S`, seq 1..N; (2) drop de TCP/NT reconnect; (3) AddOn reconecta con el MISMO `session_id=S` y `execSeq=0`; (4) primer frame post-reconnect `seq=1 <= LastSeq=N` ⇒ rechazado counted; (5) todo frame posterior igualmente rechazado ⇒ sin command_results ni observaciones de órdenes ⇒ `EventStreamLive=false` ⇒ readiness down permanente hasta restart de NinjaTrader. Fail-closed (ninguna acción incorrecta), pero funcionalmente rompe el lane exactamente en el escenario que el freeze §11 declara resuelto ("AddOn reconnects (proven in N1)").

**WHY EXISTING TESTS DID NOT CATCH IT:** los tests del bridge usan un harness AddOn falso que regenera sesión/seq por conexión (semántica `ntx.Conn`); no existe test del ciclo real del AddOn C# staged (shadow-compile only). El gap C#/Go no está cubierto por ningún test de contrato de reconnect.

**REQUIRED ACCEPTANCE CRITERIA:** tras un reconnect físico del AddOn de ejecución, el bridge acepta los frames de la nueva conexión y el lane converge a `EventStreamLive=true` sin restart de NT. Mínimo: (a) nuevo `session_id` por conexión O seq continuado por sesión persistente — cualquiera que sea la semántica elegida, un test de contrato la fija en ambos lados (harness Go + comportamiento C# documentado/verificado en el drill de Shot 3); (b) drill físico G-E2E incluye ≥1 reconnect con evidencia post-reconnect aceptada.

**NOTA DE ALCANCE:** el build es STAGED (no instalado; `ORDERS_SENT=0` intacto). No afecta el egress-disabled invariant; afecta el candidato del lane físico que Shot 3 instalará — debe remediarse antes de G-E2E.

---

### F-S2-02 — HIGH — Freshness input-driven: un feed muerto-silencioso queda FRESH para siempre

**CONTRACT / INVARIANT VIOLATED:** Freeze §4.2: "STALE if no arrival within `liveness_bound` … (detects a dead feed)" — el modelo congelado de frescura incluye el detector de feed muerto; y la propiedad requerida por este review: "stale/unknown serving authority must not enable NEW RISK". Un transporte muerto sirve FRESH congelado ⇒ enablement de new risk sobre una autoridad de facto stale.

**EVIDENCE:** `v3/core/internal/functions/futures_market_stream.go:336,471` — `egressStreamState` (donde se evalúa freshness contra el reloj) sólo se invoca desde `handleCandidate`/`handleControl`; grep: cero timers/`SendAfter`/tickers de re-evaluación. Liveness desactivado: `marketExpectedActive=false` hardcodeado (`:556-560`), deuda V1 documentada en Shot 1 §7.4. El comentario del código — "The lag bound (event_ts age) already detects a dead/lagging feed" (`:558-559`) — es un **overclaim**: el age bound sólo se evalúa cuando llega un input; un feed totalmente silencioso nunca re-dispara la evaluación y el último snapshot FRESH queda congelado en el read model que readiness/admission consumen (`views.go:102-113,172-178`).

**FAILURE TIMELINE:** (1) feed vivo, trade a las T con event_ts T ⇒ FRESH servido; (2) el feed muere silenciosamente (drop del subscription/NT↔Tradovate sin mensajes downstream); (3) sin arrivals, la freshness nunca se re-evalúa ⇒ FRESH congelado indefinidamente; (4) señal generada en el último tick antes de la muerte pasa admission con freshness pineada FRESH ⇒ new risk habilitado con transporte muerto; BBO desactualizado ⇒ entrada MARKET ciega + protective stop nivelado del último precio conocido. Ya-abierto queda protegido venue-side (STOP_MARKET), y sin ticks no nacen señales nuevas — la ventana de exposición es la señal-en-vuelo→admit; pero es exactamente el vector que el frente G ordena intentar ("fresh event timestamp but dead transport") y falla.

**WHY EXISTING TESTS DID NOT CATCH IT:** todos los tests de freshness alimentan eventos (input-driven) — el caso sin-eventos-posteriores no tiene test; el E2E s07 prueba lag, no silencio. La deuda liveness está documentada como conocida (§7.4) pero sin un test que congele la propiedad "el gate externo compensa mientras tanto" ni un surface que la haga visible.

**REQUIRED ACCEPTANCE CRITERIA:** un feed que deja de entregar eventos durante > `freshness_bound` mientras el runtime está en modo live no puede sostener `market_freshness=FRESH`: o (a) el liveness bound queda cableado con fuente de "mercado esperado activo" (calendario o equivalente config), o (b) un mecanismo equivalente de re-evaluación por tiempo degrada el snapshot servido a STALE tras el bound, con superficie de razón visible. Mínimo aceptable para Shot 3: la deuda queda cubierta por uno de los dos mecanismos ANTES de G-E2E, con test determinista del feed-silencioso.

---

### F-S2-03 — MEDIUM — Sin guard de `event_ts` futuro; frontier de freshness inmutable ante fuentes adelantadas

**CONTRACT:** Freeze §4.2 (age = now − max(event_ts)); el evento futuro produce edad negativa ⇒ FRESH perpetuo hasta que el wall clock alcance el ts venenoso. `ControlSourceSwitch`/`ControlRecoveryBarrier` no resetean la evidencia (`futures_market_stream.go:376-415`) ⇒ un solo evento con ts futuro envenena el frontier de la sesión. `Evaluate` no clampa (`freshness.go:131`); la validación de envelope sólo rechaza `IsZero()` (`ingress.go:74`); el test pina el comportamiento (`freshness_test.go:50-55`). El freeze no define el guard ⇒ gap de spec. Mitigación: N1 verificó el reloj del dev-win correcto y el AddOn propaga `e.Time` fielmente; el vector requiere una fuente de venue adelantada.

**REQUIRED ACCEPTANCE CRITERIA:** un evento con `event_ts` > reloj dominio + tolerancia config no puede dejar el frontier en edad negativa (clamp o rechazo contado con razón visible), y el frontier se re-ancla en el source switch/recovery barrier.

---

### F-S2-04 — MEDIUM — `echo.ntx.v1` sin fencing de sesión activa

**CONTRACT:** Frente M: "old-session frames could mutate new-session state". `serveConn` reemplaza `s.conn` sin cerrar la conexión previa (`server.go:260-263`) y el tracker acepta frames de cualquier sesión conocida con seq válida propia; el adapter resuelve waiters y actualiza vistas sin verificar que la sesión del frame sea la sesión activa (`adapter.go:350-365,370-388`).

**FAILURE TIMELINE (requiere token + doble conexión viva):** (1) conexión A autenticada; (2) conexión B (mismo AddOn con bug, o impostor con el token) autentica ⇒ `s.conn=B`; (3) A sigue viva y enviando `orders/executions/command_result` con su seq propia ⇒ tracker las acepta ⇒ mutan `a.orders`, resuelven waiters, avanzan el journal. Fail-visible parcial (los comandos salen sólo por B), pero la evidencia puede mezclar sesiones. En el modelo de amenaza congelado (LAN confiable, un AddOn, token en ETCD) el vector es de robustez, no de safety primaria; hoy un solo AddOn staged existe.

**REQUIRED ACCEPTANCE CRITERIA:** al autenticar una nueva conexión, la sesión previa deja de ser aceptada como evidencia (drop activo o fencing por session_id actual en el adapter), o un test documenta la decisión y su dependencia del modelo de amenaza LAN.

---

### F-S2-05 — MEDIUM — Day boundary del binding real desalineado con el ciclo CT del programa (ETCD activo + default del loader)

**CONTRACT:** Frente I / GAU50 account state: DLL/DD de E2T corren en ciclo **5pm–5pm CT** (PASS-1:78,404).

**EVIDENCE:** ETCD DEV real (lectura read-only hoy): `/echo/development/futures-bridge/accounts/E2T-GAU50-01/binding/day-boundary-tz = "America/New_York"` (existencia exacta verificada por list; size 16) con `day-boundary-reset = "17:00"` ⇒ boundary a 16:00 CT (CDT) — **1 hora antes** del cierre real del día de cuenta del provider. Además el default del loader es la misma tz equivocada para bindings nuevos (`internal/binding/loader.go:31,51`).

**FAILURE TIMELINE:** hoy latente: `DailyLossBreached/TrailingBreached` los provee el account-state plane externo (aún sin productor vivo; enforcement Shot 3), y el engine consume snapshots como autoridad (`state.go:66-70`). Cuando el plane keyee el día de cuenta por el binding, entre 16:00 y 17:00 CT Echo considera "día nuevo" mientras el provider sigue en el día anterior ⇒ riesgo de considerar limpiado un estado de breach que el provider aún sostiene.

**REQUIRED ACCEPTANCE CRITERIA:** antes de G-E2E: `day-boundary-tz` del binding E2T-GAU50-01 corregido a `America/Chicago` con reset `17:00` (o el equivalente exacto del ciclo del programa) con read-back doble; default del loader cambiado o hecho obligatorio para `NINJATRADER_BRIDGE` (Validate fail-closed sin tz explícita).

---

### F-S2-06 — MEDIUM (EVIDENCE_GAP) — Basis del DLL sin declaración first-party; cita verbatim de consistency ausente

**CONTRACT:** Frente H: valores GAU50 vs SourceRefs; "Do NOT assume".

**EVIDENCE:** el materialization declara `daily_loss{ABSOLUTE, 1100 USD, basis INITIAL_BALANCE}`; la fuente first-party establece kind/monto/ventana (5pm–5pm CT, open+closed+commissions, PASS-1:78,404) pero **no declara** la base numérica del cómputo (`INITIAL_BALANCE` es la inferencia implementada — razonable para una Evaluation de balance fijo, no citada). Análogo: el boundary `>=` de consistency está soportado por dos formulaciones FACT convergentes ("30% or more", "must be below 30%", PASS-1:403,80), pero el vault no conserva la frase verbatim del artículo oficial. No es material para safety (consistency es monitoring-only, y DLL/DD flags hoy vienen del plane externo), pero la cadena de provenance debe cerrarse antes del primer egress.

**REQUIRED ACCEPTANCE CRITERIA:** antes de OD-D6-1/G-E2E: capturar en los SourceRefs (o en un delta del preflight) la frase literal de la fuente oficial para (a) la base del DLL y (b) el boundary de consistency; si la fuente contradice `INITIAL_BALANCE` o el `>=`, es config-act con provenance.

---

### F-S2-07 — MEDIUM — Gate de cobertura del warm-up cuenta presencia, no completitud

**CONTRACT:** Freeze §10: ≥17 días de sesión ("17 sessions × 3-4 H4 regions"); requisito 51 H4 + 20×5m fail-closed.

**EVIDENCE:** `warmup.go:178-194` — `bucketCounts` cuenta buckets **distintos por `Truncate`** dentro de cada región H4: un corpus con 1 bucket-5m por región H4 durante 17 días pasa el gate de 51 "H4 cubiertas" con ~1% de la historia real; los gaps intra-día son "diagnostic report, never a gate" (`warmup.go:210-215`) y `BuildPublishingPlan` nunca consulta `Gaps()`. La readiness assertion del anchor es data decorativa (`warmup_test.go:659-664`).

**FAILURE TIMELINE:** BarsRequest del provider con barras espaciadas (datos faltantes) ⇒ corpus esparso pasa el gate ⇒ WARMUP "completo" ⇒ analytical READY ⇒ señales sobre S1/S2 alimentados de historia degenerada. La fidelidad byte-idéntica se prueba contra corpus completo sintético, no contra esparso.

**REQUIRED ACCEPTANCE CRITERIA:** el gate exige densidad mínima por región H4 (p.ej. buckets 5m presentes ≥ umbral por región, o sesiones completas) o el plan de publicación adjunta el reporte de gaps al anchor y el readiness falla si los gaps superan el umbral; test con corpus esparso ⇒ `WARMUP_INCOMPLETE`.

---

### F-S2-08 — MEDIUM — Freshness mode-blind: sin invarianza BACKTEST

**CONTRACT:** Frente K: D6 live additions no contaminan EXACT_REPLAY/BACKTEST.

**EVIDENCE:** ningún branch por `RunMode` en el camino freshness (`runtime.go:107-115`, `views.go:302-323`, pinning `engine.go:594`); el harness siembra freshness en BACKTEST (`harness.go:239-246`). Hoy inerte: el reloj virtual cabalga el event time (`harness.go:535-546`, edad≈0⇒FRESH). Un driver BACKTEST que adelante el reloj >30s respecto del último event_ts (p.ej. salto a cierre de sesión) servirá STALE y bloqueará señales de BACKTEST — semántica D6-live filtrada a BACKTEST, sin test de invarianza que lo congele.

**REQUIRED ACCEPTANCE CRITERIA:** test de invarianza: BACKTEST con salto de reloj > freshness_bound produce las mismas señales/decisiones que sin la dimensión (o la dimensión se desactiva explícitamente fuera del modo LIVE), y EXACT_REPLAY con freshness grabada re-reproduce byte-idéntico (cierra también el gap de replay K-2).

---

### F-S2-09 — MEDIUM — Binario ELF de 33.4 MB commiteado accidentalmente

**CONTRACT:** Frente Q / higiene del árbol auditado.

**EVIDENCE:** `v3/futures-bridge/futures-bridge` = ELF x86-64 Go sin strip (33,406,528 bytes), **AGREGADO en `14b0d72b`** (commit F-MGR-01), ausente en `f0c82905`; sin entrada de build/deploy que lo referencie (el despliegue corre desde `/home/kor/opt/echo-dev/releases/<sha>/`). Artefacto `go build` por descuido.

**IMPACT:** no material para runtime safety (nunca se ejecuta del árbol) pero contamina el historial (33 MB permanentes salvo rewrite) y crea ambigüedad de procedencia ejecutable en un vertical cuyo valor es la salida auditada.

**REQUIRED ACCEPTANCE CRITERIA:** eliminar del branch + `.gitignore` del path (o regla de build); registrar la decisión sobre el blob histórico.

---

### F-S2-10 — MEDIUM — G-EGRESS-0: el grep-gate del feed AddOn no está automatizado

**CONTRACT:** Freeze §14 G-EGRESS-0 ("structural grep gates… demonstrated by tests + deployment state").

**EVIDENCE:** el gate existe como verificación manual del Shot 1 (re-grep @ `4b05d6f8`); no hay test/script en el repo que haga grep de `EchoFeedAddOn.cs` contra APIs de mutación (`grep` en `*.go`/Makefile/scripts: cero referencias al source del AddOn).

**REQUIRED ACCEPTANCE CRITERIA:** test automatizado (o script canónico invocado por la suite) que failing-closed detecte `Submit|Change|Cancel|Flatten|CreateOrder` en el feed AddOn y la ausencia de familias de comando en `echo.ntfeed.v1`.

---

### Notas no-elevadas (registradas, sin severidad de finding)

- **AddOn staged robustez:** comando malformado ⇒ `ERROR` (no `REJECTED`) — inalcanzable con bridge conforme (`WriteCommand` valida antes de escribir); falta priming de executions tras start/reconnect ⇒ re-publicación de historial (dedup nativo aguanta, calidad de evidencia menor que el patrón N1); contadores heartbeat muertos (warning ya registrado).
- **Guard anti-drift:** dereference antes de nil-check (`rulesets.go:98/102,107/111`) — panic sólo si el guard corre con familias ausentes: inalcanzable con el embed real (guard CI-only); 16 mutaciones reales vs 14/15 documentadas (drift doc); mutación `consistency_percent_drifted` sin caso de test.
- **DST:** ventana provider correcta por construcción (tzdata + wall-clock por instante); sin test de transición (congelar el invariant en nov/mar es barato).
- **Cobertura:** swallows de error de journal en el path de observación (`adapter.go:414-415,422-423`) justificados como "fail-visible at the barrier" pero no documentados en la lista de exclusiones F-MGR-01; happy-path LIMIT/STOP frame propagation sin test (gates físicos de Shot 3 lo ejercitarán).
- **Thread affinity C#:** CreateOrder/Submit/Cancel/Change desde background threads sin Dispatcher marshaling — riesgo físico explícito que G-E2E debe demostrar (freeze §14.13); no es defecto del candidato, es el scope físico de Shot 3.
- **Pin→admit window (F-6):** freshness pineada una vez; materialize no re-chequea — consistente con el diseño frozen (pin del requester + protección venue-side); riesgo nuevo limitado a un hop.
- **Domingo Globex:** ventana Mon-Fri deja fuera el evening dominical — fail-closed, documentado en el JSON.
- **Preexistente:** race `-race` de `futures-projector/adapters/kafka` (baseline `f0c82905`, fuera de alcance, registrada en Shot 1 §7.1).

## 5. Tests y harnesses ejecutados

- `go test -race -count=1` `v3/futures-bridge/...` — **13 pkgs ok, exit 0** (reproducido en este review).
- `go test -race -count=1` `v3/sdk/futures/...` y `v3/core` (functions, futuresruntime, futuresvertical, config/futures) — en curso al cierre del análisis; los mismos paquetes corrieron limpios (0 FAIL, Go 1.27.1) durante la reproducción de cobertura del frente N (con profile), que es la evidencia primaria de suites verdes usada aquí.
- Reproducción independiente de cobertura changed-logic (script propio del reviewer, `/tmp/d6cov-shot2/`): 3 coverprofiles + git-diff slicing; raw 1202/1279 = 94.0%, ajustado 98.4% ≥ 95% — **COVERAGE_CLAIM: PASS**.
- ETCD RO: 18 claves del subtree `futures-bridge` listadas por existencia exacta; `futures-bridge/accounts` ABSENT; `binding/provider-account-ref` exacta (17 bytes); `binding/day-boundary-tz = America/New_York` (F-S2-05).
- Deployment RO: `ps` + `systemctl list-units` — sin proceso ni unit de futures-bridge; relay feed en release `170a4581` (lane N1 read-only operativo).
- Grep-discipline re-ejecutado por el reviewer sobre `EchoFeedAddOn.cs` (mutaciones: cero; sólo comentario header).

## 6. Residual risks (aceptados con justificación, no bloquean)

1. **Ventana pin→admit** (freshness degrada entre pin y ALLOW): frozen design; mitigada por stop venue-side ya-abierto y por la ventana de un hop.
2. **Thread affinity física y retention `order.Name`/`OrderId`**: gates físicos Shot 3 (G-E2E/G-ID-Retention) — no certificables estáticamente.
3. **Negación autoritativa ausente en lane V1** (`ResubmitApprovedByAbsence` jamás emitido): conservador — produce AMBIGUOUS permanentes en crash-window SUBMITTING; costo operativo (entrada perdida), nunca doble submit.
4. **Sin enforcador vivo de DLL/DD/consistency inputs** (plane externo pendiente): enforcement real queda condicionado a Shot 3; el seam es el contrato frozen.
5. **Doble-writer organizacional** (sin fencing estructural de segundo bridge host): MVP una cuenta; riesgo registrado en F-S2-04.

## 7. Pass/fail rationale

El candidato es arquitecturalmente fiel al freeze: las tres capas de identidad, el M2 journal con punto-de-no-retorno bien ubicado, el dedup pre-side-effect, la reconciliación fail-closed, el stack STOP_MARKET completo y el egress estructuralmente muerto (4 barreras) resistieron el ataque directo; cobertura y reglas GAU50 se reprodujeron independientemente. No hay BLOCKER y ninguna vía legal encontrada produce wrong-account, doble submit físico, VENUE_BOUND sin evidencia venue, stop sintético ni contaminación de replay.

Sin embargo, el pass standard exige **cero HIGH sin resolver** en freshness y execution transport, y hay exactamente dos:

- **F-S2-02 (freshness):** un feed muerto-silencioso sirve FRESH congelado y habilita new risk en la ventana señal-en-vuelo→admit — el vector adversarial explícito del frente G falla; el propio freeze define el liveness bound como parte del modelo fail-closed.
- **F-S2-01 (execution transport):** el AddOn de ejecución staged rompe el lane en el primer reconnect (seq rewind con sesión persistente) — el escenario §11 que el diseño declara resuelto.

Ambos son remediables con cambios acotados y no invalidan la arquitectura; por eso el veredicto es **REMEDIATION_REQUIRED** (routing normal del plan de shots: Shot 3 abre con remediation antes del ladder físico), no un re plano.

## 8. Shot 3 acceptance inputs (orden de remediación sugerido)

1. F-S2-01: semántica de sesión/seq del reconnect AddOn (código C# + contrato de test Go) — antes de instalar el AddOn.
2. F-S2-02: liveness bound cableado (calendario o re-evaluación por tiempo) + test feed-silencioso — antes de G-REALTIME.
3. F-S2-05: fix ETCD `day-boundary-tz` + default loader — antes del account-state plane.
4. F-S2-03/04/06/07/08/10: guards de frescura, fencing ntx, provenance DLL/consistency, densidad warm-up, invarianza BACKTEST, grep-gate automatizado.
5. F-S2-09: limpieza del binario commiteado.
6. Los gates físicos congelados se mantienen: OD-D6-1 → G-REALTIME → G-STOP → G-ID-Retention → G-HORIZON → G-E2E (incluye drill de reconnect, que ejercita F-S2-01) → G-PERF.

## 9. Handoff final

```text
D6_SHOT2_ADVERSARIAL =
REMEDIATION_REQUIRED

CANDIDATE_SHA:
0e9741a56afe6911e52480fb9f2fe86a47aae427

BLOCKERS:
0

HIGH:
2 (F-S2-01 AddOn staged seq-rewind rompe lane tras reconnect; F-S2-02 feed muerto-silencioso queda FRESH y habilita new risk)

MEDIUM:
8 (F-S2-03 event_ts futuro sin guard + frontier sin reset; F-S2-04 ntx sin fencing de sesión; F-S2-05 day-boundary real 17:00 America/New_York = 16:00 CT desalineado con 5pm CT; F-S2-06 EVIDENCE_GAP basis DLL + cita verbatim consistency; F-S2-07 warm-up gate presencia≠completitud; F-S2-08 freshness mode-blind BACKTEST sin invarianza; F-S2-09 binario 33.4MB commiteado; F-S2-10 grep-gate egress no automatizado)

FINDINGS:
F-S2-01 seq rewind AddOn ejecución inutiliza lane tras reconnect (fail-closed, staged)
F-S2-02 freshness input-driven: feed silencioso FRESH-forever, liveness off + overclaim en comentario
F-S2-03 sin clamp de event_ts futuro; frontier sin reset en control paths
F-S2-04 echo.ntx.v1 acepta frames de sesión vieja viva (sin fencing)
F-S2-05 binding real ETCD day-boundary desalineado 1h con ciclo DLL/DD CT
F-S2-06 basis INITIAL_BALANCE del DLL y verbatim de consistency sin cita first-party
F-S2-07 warm-up coverage gate pasa corpus esparso (presencia sin densidad)
F-S2-08 BACKTEST hereda freshness sin test de invarianza (hoy inerte)
F-S2-09 ELF 33.4MB commiteado en 14b0d72b (higiene/procedencia)
F-S2-10 G-EGRESS-0 grep-gate manual, sin test automatizado

WRONG_ACCOUNT_SAFETY:
PASS

DOUBLE_SUBMIT_SAFETY:
PASS

M1_M2:
PASS

STOP_MARKET:
PASS

CANCEL_REPLACE_LATE_FILL:
PASS

RECONCILIATION:
PASS

MARKET_FRESHNESS:
FAIL (F-S2-02)

GAU50_RULES:
PASS (F-S2-06 EVIDENCE_GAP documentado; boundary ==30% correcto según fuente)

WARMUP_REBUILD:
PASS (F-S2-07 densidad del gate)

EXACT_REPLAY_BACKTEST:
PASS (F-S2-08 invarianza BACKTEST sin test)

NTX_PROTOCOL:
PASS (F-S2-04 fencing)

ADDON_AUTHORITY:
PASS

COVERAGE_CLAIM:
PASS (98.4% ajustado reproducido; raw 94.0%)

NINJATRADER_COMPATIBILITY:
PASS (estático) / PHYSICAL_DEFERRED (thread affinity + retention = gates Shot 3)

PHYSICAL_EGRESS_DISABLED:
PASS (4 barreras independientes, STRUCTURALLY_DISABLED)

SCOPE_CREEP:
PASS (F-S2-09 higiene)

OWNER_DECISION_REQUIRED:
NONE (ningún finding requiere decisión owner; F-S2-06 es provenance, no conflicto de fuentes; OD-D6-1 permanece como gate de Shot 3, no solicitado aquí)

SHOT3_INPUTS:
(1) remediar F-S2-01 y F-S2-02 antes de cualquier paso físico (G-REALTIME/G-E2E los ejercitan); (2) F-S2-03..08,10 remediables en software con tests congelantes; (3) F-S2-05 = config act ETCD + default loader con read-back doble; (4) F-S2-06 = completar provenance antes de primer egress; (5) F-S2-09 = limpieza de árbol; (6) ladder físico congelado intacto: OD-D6-1 → G-REALTIME → G-STOP → G-ID-Retention → G-HORIZON → G-E2E → G-PERF; (7) G-E2E debe incluir reconnect drill que demuestre el fix de F-S2-01 y thread affinity

NEXT_MANAGER_ACTION:
REMEDIATION_REQUIRED → Primary Manager adjudica F-S2-01..10 (aprueba/refuta/cada severity) y autoriza la remediación de Shot 3 ANTES de cualquier cambio de código. No iniciar Shot 3 físico ni OD-D6-1 desde esta sesión.
```

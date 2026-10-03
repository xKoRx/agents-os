# Echo Futures — D6 Shot 3 — Pre-Egress Remediation (F-S2-01..F-S2-10)

**Shot:** D6 Shot 3 — PRE-EGRESS REMEDIATION (sin ladder físico; sin OD-D6-1)
**Role:** TOP Senior Remediation Lead (no Manager, no Owner, no adversarial reviewer)
**Date:** 2026-10-02
**Project:** [[Echo Futures]]
**Baseline before:** `xKoRx/echo@0e9741a56afe6911e52480fb9f2fe86a47aae427` (`feature/d6-shot1-execution-vertical`, candidato Shot 2, re-verificado al iniciar: worktree limpio, HEAD == baseline)
**Final SHA:** `5001ec2cce259cfee2d9656d19a1187061315809` (9 commits FF sobre `0e9741a5`; push FF verificado `origin == local HEAD`)
**Trigger:** `D6_SHOT2_ADVERSARIAL = REMEDIATION_REQUIRED` (0 BLOCKER · 2 HIGH · 8 MEDIUM, aceptados por el Primary Manager)
**Authorities:** D6 Final Design Freeze §4.2/§5/§6/§9/§10/§11/§14; Shot 1 + Manager QA (F-MGR-01/02/02B); D6-SHOT2-ADVERSARIAL-REVIEW (los 10 findings adjudicados); D4/D5 frozen contracts; Earn2Trade first-party corpus (preflight 2026-09-30 + bounded evidence repair 2026-10-02).
**Verdict:** `D6_SHOT3_REMEDIATION = READY_FOR_OWNER_PHYSICAL_EGRESS_GATE`

## 0. Hard safety

`PHYSICAL_EGRESS = DISABLED` — sin cambios estructurales: (1) capability gate M2 todo UNKNOWN ⇒ `SubmissionCapabilitiesReady=false` (testeado); (2) bridge sin desplegar ni correr y lista de sesiones `futures-bridge/accounts` **no existe** en ETCD (sólo se mutó `binding/day-boundary-tz`); (3) `EchoExecutionAddOn` sigue STAGED — el shadow-compile produce un DLL en `C:\Users\TEMP` del dev-win, nunca instalado en NinjaTrader; (4) feed AddOn instalado intacto (SHA byte-idéntico a Shot 1, guard G-EGRESS-0 verde). `ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0`. Master y PROD intocados.

## 1. Remediación por finding

### F-S2-01 — AddOn de ejecución: reconnect session/seq — PASS
- **STATUS:** PASS (código C# + contrato Go congelado por tests).
- **ROOT CAUSE:** `EnsureExecLane` reseteaba `execSeq=0` en cada reconnect manteniendo el `execSessionId` persistido (creado una vez) — la peor combinación: sesión persistente + secuencia rebobinada ⇒ el tracker rechaza todo frame post-reconnect y el lane muere hasta restart de NT.
- **CHANGE:** cada conexión (re)exitosa del execution lane genera una NUEVA identidad de sesión (`execSessionId = Guid.NewGuid()`) con su secuencia en 0 — la semántica `ntx.Conn` (sesión por conexión) que el fencing de sesión activa (F-S2-04) exige para poder distinguir y supersedar sesiones. Comentario en fuente fija el contrato.
- **TEST:** `ntx.TestServerActiveSessionFencing` congela el contrato bidireccional: primera conexión OK; reconnect con NUEVO session id + seq reiniciada en 1 aceptado; frame duplicado rechazado por disciplina de seq; rewind dentro de sesión activa rechazado fail-closed; frames de la sesión supersedada jamás llegan al handler. Sin ejecución de órdenes.
- **EVIDENCE:** shadow-compile físico dev-win `EXEC_EXIT=0`, SHA256 `b2a29a3608cf1e1b767844156c8d03f23fd324e668fab1efde97489fd885729a` (byte-verify local/remoto). El drill físico de reconnect con evidencia post-reconnect aceptada permanece en G-E2E (gate físico congelado, NO ejecutado aquí).
- **SHA:** `77214b4b`

### F-S2-02 — Feed muerto-silencioso queda FRESH — PASS
- **STATUS:** PASS (mecanismo equivalente de re-evaluación por tiempo, opción (b) del review).
- **ROOT CAUSE:** la evaluación de frescura era input-driven: `egressStreamState` sólo corría desde `handleCandidate`/`handleControl`; sin arrivals no había re-evaluación y el último snapshot FRESH quedaba congelado; el liveness bound estaba desactivado (`marketExpectedActive=false`, deuda V1) y el comentario del código sobreestimaba al age bound.
- **CHANGE:** self-timer checkpointed del owner (flag `futures_ms_freshness_timer` + mensaje interno `futures_ms_freshness_tick`): cada hecho canónico aceptado arma el tick (periodo = mitad del bound más apretado, 15s con los defaults 30s/60s); el tick re-evalúa contra el reloj owner, re-sirve el snapshot con razón visible y se re-encadena mientras LIVE — un feed silencioso decae a STALE (age bound) a más tardar `bound + period` después de su último evento. El tick es observación de tiempo: NO consume owner input seq, NO se journaliza. Heartbeats/tráfico de transporte jamás refrescan evidencia de evento (sólo hechos canónicos pliegan); `marketExpectedActive` permanece false (deuda de calendario documentada, invariante intacta).
- **TEST:** `SilentFeedDecaysWithoutArrivals` (fresh → reloj avanza > bound sin eventos → tick → STALE con `EVENT_TS_AGE_EXCEEDS_FRESHNESS_BOUND`; tick consume 0 owner input; encadena; recuperación con hecho nuevo); `SilentFeedControlOnlyStillDecays` (sólo control durante el silencio también degrada); `NoEvidenceIsUnknown` (startup sin eventos) ya congelado; UNKNOWN/STALE bloquean new risk (consumidores existentes, regresión verde).
- **EVIDENCE:** suites `-race` verdes; snapshot con `freshness` + `freshness_reason` visible en `echo.futures.market-stream-state`.
- **SHA:** `0731b02f`

### F-S2-03 — event_ts futuro / frontier sin reset — PASS
- **STATUS:** PASS.
- **ROOT CAUSE:** `ObserveEvent` pliega máximos monotónicos sin guard: un evento materialmente futuro produce edad negativa ⇒ FRESH perpetuo hasta que el wall clock alcance el ts venenoso; `ControlSourceSwitch`/`ControlRecoveryBarrier` no re-anclaban la evidencia ⇒ un solo evento venenoso envenenaba el frontier de toda la sesión de autoridad.
- **CHANGE:** (1) bound config `future_event_skew` (default 5s, validado ≥ 0 fail-closed en `FreshnessBounds.Validate`): un evento con `event_ts` más de skew adelante del runtime_ts de admisión NO se pliega — veneno CONTADO (`FutureEventsRejected` + `LastFutureEventTs` en la evidencia y en el snapshot servido, razón `EVENT_TS_IN_FUTURE` en telemetría WARN); jamás clamp silencioso. (2) El frontier se re-ancla en las transiciones de autoridad congeladas: source switch (siempre) y recovery barrier con `InvalidatesContinuity` (el mismo camino demote/seed de D2-06B R7) — la primera evidencia válida de la nueva autoridad re-siembra.
- **TEST:** `FutureEventTsNeverEstablishesFresh` (veneno no establece FRESH, contado con traza, frontier intacto; skew pequeño dentro del bound pliega normal; veneno posterior no extiende el frontier; skew negativo falla cerrado); `FrontierResetsOnAuthorityTransitions` (switch y barrier resetean a UNKNOWN y re-siembra); sdk `TestFreshnessBounds_FutureEventSkewValidated` + `TestFreshnessEvidence_ObserveFutureEvent`.
- **EVIDENCE:** snapshot `future_events_rejected` visible; suites `-race` verdes.
- **SHA:** `0731b02f`, `a12146ec`

### F-S2-04 — Fencing de sesión activa echo.ntx.v1 — PASS
- **STATUS:** PASS (fencing mínimo consistente con el modelo de sesión existente; sin sistema de leases).
- **ROOT CAUSE:** `serveConn` reemplazaba `s.conn` sin cerrar la conexión previa y el adapter resolvía waiters/vistas sin verificar que la sesión del frame fuera la activa ⇒ una conexión vieja viva podía seguir inyectando evidencia.
- **CHANGE:** doble barrera, sindistributed-lease: (1) server: al autenticar una nueva sesión cierra INMEDIATAMENTE la conexión supersedada (fencing) con rechazo visible en el sink (`session superseded by …; previous connection fenced`); (2) adapter: todo frame no-hello con `SessionID` distinta a la sesión activa se rechaza como evidencia contada (`frame from superseded session`) — nunca toca vistas, journal, dedup de ejecuciones ni waiters. El hello de la nueva sesión es el único punto de transferencia de autoridad.
- **TEST:** `ntx.TestServerActiveSessionFencing` (A activa → B autentica → conexión A cerrada por el server; frame tardío de A jamás entregado; B continúa normal) y `adapters/ninjatrader.TestAdapterSupersededSessionFencing` (segunda barrera: frame orders de sesión supersedada rechazado, journal permanece SUBMITTING; frame idéntico bajo la sesión activa produce VENUE_BOUND).
- **EVIDENCE:** suites `-race` verdes; adversarial acceptance exacta del review cubierta.
- **SHA:** `77214b4b`

### F-S2-05 — Day boundary timezone desalineado — PASS
- **STATUS:** PASS (config-act ETCD DEV + default del loader, con read-back doble; PROD intocado).
- **ROOT CAUSE:** ETCD DEV `binding/day-boundary-tz = America/New_York` con reset `17:00` ⇒ boundary 16:00 CT — una hora antes del cierre real del día de cuenta 5pm CT del programa; el default del loader arrastraba la misma tz equivocada.
- **CHANGE:** (1) ETCD DEV `/echo/development/futures-bridge/accounts/E2T-GAU50-01/binding/day-boundary-tz` = `America/Chicago` (escritura guardada: pre-lectura exacta `America/New_York` → SetVar → read-back exacto del writer → lectura plana independiente por MCP RO; size 15; `day-boundary-reset = 17:00` y las 8 claves hermanas intactas; herramienta efímera eliminada, nunca commiteada). (2) `internal/binding.Load`: default `DefaultDayBoundaryTimezone = America/Chicago` (ciclo CT del programa, IANA por nombre — DST-correcto por construcción) y validación fail-closed `time.LoadLocation` en la carga (una tz no cargable ya no degrada silenciosamente a UTC downstream). (3) Los bindings sin tz explícita heredan el default correcto.
- **TEST:** `TestLoad_DayBoundaryTimezone` — default Chicago; tz no cargable falla cerrado; transiciones DST 2026 congeladas (17:00 America/Chicago = 22:00 UTC en CDT / 23:00 UTC en CST, spring-forward y fall-back).
- **EVIDENCE:** ETCD read-back doble (writer + MCP RO); el fix es efectivo para el bridge cuando el ladder físico lo despliegue (hoy sin proceso; sin efecto en el relay feed).
- **SHA:** `d059d691`

### F-S2-06 — Provenance DLL basis + consistency verbatim — PASS
- **STATUS:** PASS (NO `BLOCKED_EVIDENCE`: la reparación acotada de evidencia first-party CERRÓ ambos gaps; y la fuente CONTRADIJO el basis implementado ⇒ config-act con provenance, según el mandato).
- **ROOT CAUSE:** el corpus preflight establecía kind/monto/ventana del DLL pero no su base numérica; la implementación había inferido `INITIAL_BALANCE`; la frase verbatim del boundary de consistencia no estaba conservada.
- **CHANGE:** (1) Bounded evidence repair (exactamente 2 fuentes first-party, 2026-10-02): artículo oficial "How is My Daily Loss Calculated?" — verbatim: "The PnL resets at the beginning of the trading day and is taken from the balance you start the day with" ⇒ el basis del DLL es el balance de INICIO del día 5pm-5pm CT (`PREV_DAY_CLOSE`), NO el balance inicial; y "Maintain Consistency" — verbatim: "no single trading day can account for 30% or more of your total PnL" ⇒ el boundary `>=` del engine (==30% ⇒ BREACHED) queda CONFIRMADO por la fuente, sin cambio semántico. (2) Config-act con provenance: `gau50-eval-v1.json` `daily_loss.basis INITIAL_BALANCE → PREV_DAY_CLOSE` + 2 SourceRefs nuevos con las citas verbatim + URLs + retrieved_at (7 SourceRefs totales); notes actualizadas (el EOD DD conserva `INITIAL_BALANCE` — la fuente lo confirma: watermark capada en el balance inicial). (3) Guard anti-drift actualizado: exige `PREV_DAY_CLOSE` y rechaza 16 mutaciones (incluida la nueva `dll_basis_drifted` hacia INITIAL_BALANCE).
- **TEST:** `TestGAU50EvalV1_FrozenShape` (7 SourceRefs, claims verbatim presentes); tabla de drift con 16 mutaciones; `config/futures` verde.
- **EVIDENCE:** las citas verbatim quedan en los SourceRefs del materialization (el artefacto deployable); sin investigación amplia (2 fetches first-party, ni uno más).
- **SHA:** `749b2a99`

### F-S2-07 — Warm-up gate presencia≠completitud — PASS
- **STATUS:** PASS (criterio determinista y replayable anclado a los requisitos congelados; sin framework genérico de calidad de datos).
- **ROOT CAUSE:** `bucketCounts` contaba presencia de buckets distintos por `Truncate`: un corpus con 1 bucket-5m por región H4 durante 17 días pasaba el gate de 51 "H4 cubiertas" con ~1% de la historia real; `Gaps()` era diagnóstico y `BuildPublishingPlan` nunca lo consultaba.
- **CHANGE:** `WarmupRequirements.Min5mPerH4Region` (default congelado **8** — 40 minutos de historia entregada por región contada, la densidad que el corpus de la derivación congelada 17-sesiones entrega efectivamente en sus regiones contadas): una región H4-equivalente con menos de 8 buckets 5m distintos NO cuenta hacia `MinH4Bars`. `WithDefaults` valida fail-closed (negativos, techo físico 48). Determinista y puro (sin relojes); los huecos interiores dentro de una región suficientemente densa siguen siendo diagnóstico `Gaps()` (nunca segundo gate silencioso); las regiones parciales de borde (2 buckets) no cuentan.
- **TEST:** `TestCorpusInput_Validate_DensityFloor` — corpus denso 51/51 con defaults (el gate aceptado no se mueve); corpus esparso 1-bucket/región (17 días, misma presencia de regiones) ⇒ WARMUP_INCOMPLETE por Validate Y por `BuildPublishingPlan` (el run no arranca); hueco interior en región densa sigue contando con `Gaps()` no vacío; regiones de borde parciales no suman; rebuild determinista 3×; piso validado fail-closed. Los corpora de fidelidad S09 (deliberadamente 1-bucket/región) declaran su forma con `Min5mPerH4Region: 1` explícito — la regresión de fidelidad de valores queda intacta y la declaración visible.
- **EVIDENCE:** suites warmup + S09 `-race` verdes.
- **SHA:** `6b53b19a`

### F-S2-08 — Freshness mode-blind BACKTEST/EXACT_REPLAY — PASS
- **STATUS:** PASS (aislamiento EXPLÍCITO por modo, no inercia accidental).
- **ROOT CAUSE:** ningún branch por `RunMode` en el camino freshness: el owner evaluaba `fn.now()` incondicionalmente; en BACKTEST/EXACT_REPLAY la no-contaminación era accidental (el reloj virtual cabalgaba event_ts) y un driver con salto de reloj serviría STALE filtrando semántica D6-live a modos deterministas.
- **CHANGE:** el owner recibe el modo del proceso que sirve (`SetRunMode(cfg.Run.RunMode)` inyectado por el constructor del runtime, F-S2-08): la dimensión freshness — evaluación Y timer de silencio — existe SÓLO en `RunModeLive`; BACKTEST/EXACT_REPLAY sirven el sentinel no-configurado `""` (la semántica D5 congelada, consumida como `configured=false` por pinning/readiness) y NUNCA arman el timer ⇒ cero dependencia de wall clock. El mismo input en modos deterministas produce el mismo resultado sin importar el avance del reloj.
- **TEST:** `LiveOnlyDimensionIsolation` (mismo candidato con reloj +10min: LIVE ⇒ STALE con razón; BACKTEST/EXACT_REPLAY ⇒ `""` sin razón, sin timers); `TickOnNonLiveOwnerIsInert` (defensa en profundidad: tick sobre owner no-LIVE no egresa, no encadena, no arma); regresión vertical s12 BACKTEST/EXACT_REPLAY completa verde (D5 intacto).
- **EVIDENCE:** suites `-race` verdes (functions, futuresruntime, futuresvertical).
- **SHA:** `0731b02f`, `5001ec2c`

### F-S2-09 — ELF 33.4MB commiteado — PASS
- **STATUS:** PASS.
- **ROOT CAUSE:** `go build` accidental commiteado en `14b0d72b` (F-MGR-01) — sin referencia de build/deploy (el despliegue corre desde `/home/kor/opt/echo-dev/releases/<sha>/`).
- **CHANGE:** `git rm --cached v3/futures-bridge/futures-bridge` + regla `.gitignore` del path (`v3/futures-bridge/futures-bridge`) — el mecanismo mínimo consistente con las convenciones del repo. Sin rewrite de historia (el blob 33MB permanece en `14b0d72b` como registro; decisión documentada aquí). Verificado: ningún artifact fuente requerido eliminado (el delta del commit es exactamente 1 path binario + 5 líneas de .gitignore).
- **TEST:** árbol limpio; `git status` sin binarios; guard de higiene natural (el path ignorado no vuelve).
- **EVIDENCE:** commit `bfe07e61`.
- **SHA:** `bfe07e61`

### F-S2-10 — G-EGRESS-0 grep-gate automatizado — PASS
- **STATUS:** PASS (test automatizado failing-closed en la suite del repo).
- **ROOT CAUSE:** la verificación estructural del feed AddOn existía sólo como grep manual del Shot 1.
- **CHANGE:** `v3/futures-bridge/addon-ninjatrader/egress_guard_test.go` — 4 tests: (1) `EchoFeedAddOn.cs` tras stripping de comentarios (`//`, `/* */`) NO contiene llamadas mutantes `\.Submit\(|\.Change\(|\.Cancel\(|\.Flatten\(|\.CreateOrder\(` (los comentarios jamás confundidos con llamadas; word-boundaries excluyen identificadores); (2) el feed AddOn no referencia familias command en su fuente; (3) el schema Go ntfeed es exactamente las 8 familias de observación sin familia command; (4) auto-chequeo del detector: el AddOn de ejecución stageado (que INTENCIONALMENTE contiene las APIs de ejecución) SÍ dispara los patrones — el gate nunca puede pudrirse en no-op silencioso.
- **TEST:** los 4 PASS; cualquier commit futuro que introduzca una llamada mutante en el feed AddOn rompe la suite.
- **EVIDENCE:** suite `addon-ninjatrader` verde en `go test ./...` del bridge.
- **SHA:** `fe4ea11b`

## 2. Cobertura (metodología reproducible aceptada, BASE `0e9741a5`)

Script `changed_coverage.py` (artefacto Shot 1, sin cambios) ∩ coverprofiles de las suites scoped (`-count=1`, go1.27.1): **raw 135/137 = 98.5% ≥ 95% SIN exclusiones necesarias**. Per-file: `rulesets.go` 100% (1/1) · `futures_market_stream.go` 97.4% (76/78) · `runtime.go` 100% (12/12) · `adapter.go` 100% (3/3) · `server.go` 100% (16/16) · `loader.go` 100% (7/7) · `freshness.go` 100% (4/4) · `warmup.go` 100% (16/16). Exclusiones documentadas (2, ambas clase canónica F-MGR-01): `futures_market_stream.go:676` floor `1s` del periodo (alcanzable sólo con bounds ≤ 1ns — Validate exige positivos y ninguna config realista lo produce) y `:704` retorno de error de `load` en el tick (falla sólo si el sequencer del stream keyeado no construye — imposible por routing keyeado). Reproducción: regenerar los 3 profiles con los comandos de las suites y correr `python3 changed_coverage.py 0e9741a5 . bridge.out sdk.out core.out`.

## 3. Shadow compile NinjaTrader 8.1.8.3 (dev-win 192.168.31.132)

Método Shot 1 (transporte efímero http.server + `curl.exe` + SHA256 byte-verify en ambos lados; servidor apagado al cierre; DLLs sólo en `C:\Users\TEMP`, NADA instalado):

- `EchoFeedAddOn.cs` — SHA256 `581a7087b1b870c78ac43e67027e5edaacf59134f4bf5f03d8b9aec9d7fd5ae4` (byte-idéntico a Shot 1: sin cambios de source en esta remediación) — **FEED_EXIT=0, 0 errores, 0 warnings**, contra `NinjaTrader.Core.dll` + `NinjaTrader.Gui.dll` + `WindowsBase.dll` físicas.
- `EchoExecutionAddOn.cs` (con el fix F-S2-01) — SHA256 `b2a29a3608cf1e1b767844156c8d03f23fd324e668fab1efde97489fd885729a` — **EXEC_EXIT=0, 0 errores**, 3 warnings PREEXISTENTES de Shot 1 (sobrecarga `CreateOrder` obsoleta CS0612 — gate G-STOP/G-E2E; contadores `market_events/account_events` CS0649 — lane de market no cableada en el build stageado, heartbeat visible en 0). Ningún warning nuevo.

## 4. Regresión de invariants aceptados (adversarial coverage re-run)

Suites completas `go test -race -count=1` verdes sobre el FINAL_SHA: `v3/futures-bridge/...` (15 pkgs ok) · `v3/sdk/futures/...` (ok) · `v3/core` functions + futuresruntime + config/futures + futuresvertical completa `-timeout 30m` (ok). Cobertura adversarial re-ejecutada: wrong account (`TestVerifyBindingDriftFailsClosed`, `TestVerifyBindingNameMismatchFailsClosed`, hello defence), double submit (`DUPLICATE_SUBMIT_SUPPRESSED`, exactamente-1-comando), M1/M2 (ciclo de barrera, journal fsync paths), STOP_MARKET (matriz domain/engine/wire, rechazo pre-journal, protective resting), cancel/replace/late-fill (fill-gana-carrera, replace dup, tighten), reconciliation (found/absent/history/quarantine), account identity (3 capas, ref durable), provider rules (GAU50 cap/ventana/safety-inputs/consistency + guard 16 mutaciones), warm-up (fidelidad S09 + coverage/densidad), EXACT_REPLAY/BACKTEST (s12 byte-idéntico + aislamiento F-S2-08), market freshness (s07 vertical + suites de functions), session fencing (2 tests nuevos). Sin rediseño de componentes aceptados.

## 5. Estado ETCD DEV (única mutación de infraestructura)

| Clave | Antes | Después | Verificación |
|---|---|---|---|
| `futures-bridge/accounts/E2T-GAU50-01/binding/day-boundary-tz` | `America/New_York` (16B) | `America/Chicago` (15B) | pre-lectura exacta + read-back writer + MCP RO independiente; hermanas intactas (9 claves del binding) |

`futures-bridge/accounts` (lista de sesiones del bridge) SIGUE sin existir ⇒ el bridge sigue sin sesiones aunque hubiera binario. PROD intocado. Relay feed sin restart (no lo requiere).

## 6. Handoff final

```text
D6_SHOT3_REMEDIATION =
READY_FOR_OWNER_PHYSICAL_EGRESS_GATE

BASELINE:
0e9741a56afe6911e52480fb9f2fe86a47aae427

FINAL_SHA:
5001ec2cce259cfee2d9656d19a1187061315809 (9 commits FF sobre el baseline; origin == HEAD verificado)

FINDINGS_CLOSED:
F-S2-01 PASS (reconnect = nueva sesión por conexión + seq 0; contrato Go congelado; C# compila contra 8.1.8.3 real)
F-S2-02 PASS (timer de silencio checkpointed LIVE: feed muerto decae a STALE ≤ bound+period sin eventos; heartbeat jamás refresca)
F-S2-03 PASS (future_event_skew 5s fail-closed; veneno contado con traza visible; frontier re-ancla en switch/barrier)
F-S2-04 PASS (server cierra la conexión supersedada + adapter rechaza frames de sesión no-activa; 2 tests adversariales)
F-S2-05 PASS (ETCD DEV America/Chicago read-back doble; loader default Chicago + LoadLocation fail-closed; DST 2026 testeado)
F-S2-06 PASS (bounded repair first-party: verbatim DLL basis = balance de inicio del día ⇒ basis corregido a PREV_DAY_CLOSE como config-act con provenance; verbatim consistency confirma el boundary >=; 7 SourceRefs; guard 16 mutaciones)
F-S2-07 PASS (Min5mPerH4Region default 8; corpus esparso 1-bucket/región ⇒ WARMUP_INCOMPLETE por Validate y por plan; determinista)
F-S2-08 PASS (freshness LIVE-only por SetRunMode del runtime; BT/ER sirven "" D5 y jamás arman timer; invarianza con salto de reloj testeada)
F-S2-09 PASS (ELF des-trackeado + .gitignore; blob histórico registrado; sin source eliminado)
F-S2-10 PASS (G-EGRESS-0 automatizado: 4 tests failing-closed con auto-chequeo del detector)

RESIDUAL_FINDINGS:
NONE (notas no-elevadas del review permanecen registradas sin severidad: robustez AddOn stageada, thread affinity C# = gates físicos Shot 3)

EVIDENCE_GAPS:
NONE (F-S2-06 cerrado con citas verbatim first-party en SourceRefs; el drill físico de reconnect permanece en G-E2E por diseño congelado, no es gap de evidencia software)

TESTS:
go test -race -count=1: v3/futures-bridge/... 15 pkgs ok · v3/sdk/futures/... ok · v3/core functions+futuresruntime+config/futures+futuresvertical(-timeout 30m) ok; suites de regresión adversarial del §4 todas PASS

COVERAGE:
changed-logic (BASE 0e9741a5, script aceptado): raw 135/137 = 98.5% ≥ 95% sin exclusiones; 2 statements canónicos inalcanzables documentados (floor 1s de bounds degenerados; load-error del tick)

NINJATRADER_8_1_8_3_COMPILE:
PASS (shadow-compile físico de AMBOS AddOns contra las DLL instaladas: 0 errores; feed byte-idéntico a Shot 1 sin warnings; execution con los 3 warnings preexistentes registrados; hashes byte-verify; ejecución NO instalada — staged)

PHYSICAL_EGRESS:
DISABLED

ORDERS_SENT:
0

ORDERS_MODIFIED:
0

ORDERS_CANCELLED:
0

OWNER_DECISION_REQUIRED:
NONE para esta remediación. El gate OD-D6-1 (autorización de egress físico, control-plane) permanece REQUIRED e inmediato antes de G-REALTIME/G-STOP/G-E2E — NO solicitado en esta sesión.

NEXT_MANAGER_ACTION:
If READY_FOR_OWNER_PHYSICAL_EGRESS_GATE: Primary Manager asks Owner for OD-D6-1 explicit authorization before the first physical order. Ladder físico congelado intacto: OD-D6-1 → G-REALTIME → G-STOP → G-ID-Retention → G-HORIZON → G-E2E (incluye drill de reconnect que ejercita F-S2-01 y thread affinity) → G-PERF. No ejecutar órdenes físicas. No comenzar el ladder. No emitir EF_D6_E2E_PASS.
```

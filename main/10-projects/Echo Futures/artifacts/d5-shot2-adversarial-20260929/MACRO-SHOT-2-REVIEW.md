# ECHO FUTURES — D5 MACRO SHOT 2 — ADVERSARIAL REVIEW + EXACT REPLAY ACCEPTANCE

**Role:** TOP Principal Adversarial Systems Reviewer / Quant Runtime Verification Lead
**Fecha:** 2026-09-29
**Método:** 8 reviewers adversariales paralelos (A–H) con particiones acotadas + consolidación TOP + implementación física de D5-S12 (infraestructura de verificación, product code congelado).

## Executive

```text
MACRO_SHOT_2_REVIEW = COMPLETE
baseline reviewed   = xKoRx/echo feature/d5-foundations @ 4c41ee773f45665df163d46cd21b4ccb2842f489 == origin (clean; origin/master 372af59a)
S12 status          = COMPLETE (test-only, commit 9275fa74 en feature/d5-shot2-adversarial): MKT-10..13 + REC-04 + goldens S1/S2 + GerardMM same-input/same-decision + BACKTEST determinismo + journal vivo
findings            = 4 BLOCKER · 32 MAJOR · 28 MINOR · 1 refutado (F-G-03)
highest-risk        = F-A-01 (timers de barra/sesión son sends inmediatos: semántica de barras inservible en runtime Flink real, livelock de sesión) y F-C-01 (ventana cancel-ACK→finality libera el claim: double-spend de exposición reducible + INVERSIÓN física demostrada)
ADVERSARIAL_RESULT  = FINDINGS
```

No se emite `D5 CLOSED` ni `EF_D5_FOUNDATION_PASS`. Vuelve al Primary Manager.

## 1. Git evidence

```text
base SHA         = 4c41ee773f45665df163d46cd21b4ccb2842f489 (feature/d5-foundations, == origin/feature/d5-foundations)
review branch    = feature/d5-shot2-adversarial (creada desde exactamente el baseline)
final SHA        = 9275fa74 ("test(s12): exact replay + backtest acceptance harness (Shot 2 review infrastructure)")
dirty state      = clean tras el commit
sólo superficies test/replay/review cambiadas = SÍ (3 archivos nuevos, todos bajo v3/core/internal/futuresvertical/, package test-harness ya no-productivo; product behavior = READ ONLY, cero diffs en product code)
worktrees        = worktrees Shot 1 intactos (wt-bridge/market/operation/provider/rb/rc/rm/rp/strategy/vertical); no afectados
```

## 2. Findings register (consolidado A–H + TOP)

Clasificación por mandato §23. Un root cause = un finding. Nota: F-G-03 del reviewer G ("HEAD no compila") quedó **REFUTADO**: los archivos S12 estaban a mitad de escritura en el worktree compartido durante su build; el árbol final compila y la suite completa (S11+S12) pasa. El baseline 4c41ee77 es limpio.

### BLOCKER (4)

| ID | Autoridad violada | Source | Trigger/expected/actual | Riesgo |
|---|---|---|---|---|
| **F-A-01** | D2-06C §7/§9/§12 (TimerFired por deadline, scheduling DomainClock), MKT-14/15 | `futures_market_analytics.go:685-694` (`ensureBarTimer`→`ctx.Send` inmediato), `:829-840` (session timer ídem); `futuresvertical/bus.go:431` ignora delay | R1 ejecutado: 1 trade → 5000 mensajes internos sin quiescer (livelock de cadena de sesiones) + BAR_CLOSED prematuro (barra cerrada por el primer trade, no por el boundary) + sin siguiente input la barra jamás cierra | Semántica de barras/trigger inservible en LIVE real; MKT-14/15 sin cobertura real (tests existentes con MockContext que nunca entrega sends). Dirección: `ctx.SendAfter(boundary−now)` + cancelación por `(timer_id, generation)` |
| **F-C-01** | D4-A2 A2-I3 (no double-spend), A2-I8, W2 (post-ACK available reducible=0 hasta finality), W3, EXP-04/07 | `operation/claims.go:174` (`ComputeClaims` excluye órdenes no-live con `QExecMax>0`); `engine_inputs.go:649-655`, `:833-869` | Reproducido: LONG x=2 → EXIT SELL2 → ForceClose ✓ → cancel ACK (QExecMax=2 retenido ✓) → replan crea SEGUNDO SELL2 (claim hueco) → late fill del EXIT cancelado + fill del reemplazo → **x_o=−2: inversión física** con breach visible | Viola la garantía central de no-inversión en la carrera cancel+fill que el diseño declara tolerar. Dirección: claims suman órdenes no-live con remanente sin finality (o flag `finality_pending`) |
| **F-D-01** | D4-A2 §7 (fórmulas por scope tipado), D2-05C L131/135 | `provider/capacity.go:94-135` (`buildEnvelope` no filtra por scope), `:140-171`, `:298-302` | Probe: cap NET_ABS scope="ES" cap=5; firm ES +10, NQ −10; request ES BUY 1 ⇒ GRANT (suma account-wide N=0); scoped correcto = DENY (11>5). Dirección inversa: GROSS scopeado niega headroom real | Over-authorize 3× cap (NET_ABS sub-cuenta) o over-deny (GROSS scopeado) siempre que la policy use scopes. Ningún test cubre scope≠account-wide. Dirección: filtrar buckets por scope del cap |
| **F-E-01** | D4-B2 §17/§18 (TP dinámico por QUOTE, no resting order), S09 profit termination precedence, MM-17 | `operation/mm.go:10-27` (MMTriggerKind sin QUOTE/AccountStateUpdate), `operation/engine.go:105-117`; grep: 8 call sites de invokeMM, todos fact-driven | Entry MARKET llena, precio corre a TP → `Evaluate` jamás se re-invoca → `remainingProfit==0` inalcanzable; salida sólo por stop de pérdida | La política económica de TP=1500 está muerta: el único exit sistemático es la pérdida. Dirección: trigger QUOTE/AccountStateUpdate en la superficie MM (Shot 3) |

### MAJOR (32)

| ID | Partición | Resumen (autoridad · source · defecto) |
|---|---|---|
| F-A-02 | market | Absorb de timer stale PISA el estado del timer vigente (`futures_market_analytics.go:647-654`): firing gen1 stale resetea `barTimers`, luego gen2 vigente también se absorbe → barra forming eterna. Reproducido |
| F-A-03 | market | Regresión de versión de calendario mata PERMANENTEMENTE la cadena de sesiones (`:600-611` + `:434`): upsert v1 sobre v2 deja `sessionTmr` sin re-agenda; jamás re-agenda prospectivo (D2-06C §12). Reproducido |
| F-A-04 | market | Autoridad de calendario elegida por iteración de map (`:403-407`, `:729-733`): 60 trials idénticos → grid distinto (56/4). No-determinismo mismo-input/mismo-output |
| F-A-05 | market | Isla `echo/market_analytics` no journaliza NADA (`:130-131` journal/runID declarados, nunca usados): timers, requirements, calendar, barriers sin recording → EXACT_REPLAY de la isla imposible (D2-06C §15/§16, S02/S03) |
| F-B-01 | strategy | S1 nunca reporta `Outcome.CycleOpen` (cero asignaciones; S2 sí): config pending se promueve a mitad de ciclo técnico (SPEC §23; `engine.go:258`). Reproducido: OPEN_CYCLE_LONG promueve v2 con OR congelada v1 |
| F-B-02 | strategy | Admisión tardía (>5m S1) → error duro `sig.Validate` (valid_until ≤ created_at) → estado no persiste, dedup re-abre → poison-message, redelivery infinito, owner bloqueado (D4-B3 §11; `engine.go:245-249`) |
| F-B-03 | strategy | `technicalReference` (`s1.go:625-627`) valida reach-back pero no contigüidad del grid: hueco intra-ventana → stop técnico INCORRECTO emitido (97.25 en vez de fail-closed). Reproducido |
| F-C-02 | operation | `OrderModifyObservation` stale regrasa términos vigentes, sin dedup por ActionID, `VenueStatus` sin validar (REJECTED muta), sin guard terminal (`engine_inputs.go:667-724`). Reproducido: QExecMax 4→2→1 con venue en 4 |
| F-C-03 | operation | CLOSE/CLOSE_ALL(k+1) NO invalida el OPEN diferido (`PendingNextCycleOpen`); el ciclo cerrado resucita al converger terminalidad (`engine.go:474-481`, `:1035-1043`; ADM-03). Reproducido |
| F-C-04 | operation | Revalidate VALID sobre orden muerta → flip EGRESS_AUTHORIZED + reservation leak perpetuo account-wide (`engine_inputs.go:104-143`, `:146-180`, `:603-618`). Reproducido (releases=0) |
| F-C-05 | operation | Modify-decrease aceptado deja `ModifyIntent` vivo → lockout silencioso de todo modify futuro de la orden (`engine_inputs.go:688-698` vs `:714/:717`; `:905-906`). Reproducido: MODIFY 2→1 → cero efectos |
| F-C-06 | operation | `DeliveryDedup` evacuado en materialización → re-delivery del OPEN original re-entra como MANAGEMENT_SIGNAL → ADD expansivo desde duplicado (`engine.go:652`, `:439-442`; D2-04 §6). Reproducido |
| F-C-07 | operation | `ExposureReservationRelease` sin campo qty (`wire.go:197-205`): modify-decrease aceptado libera el GRANT COMPLETO con remanente ejecutable → under-reserva account-wide (D4-A2 A2-I4/W5). El test `TestEXP05` consagra el defecto |
| F-C-08 | operation | Conflicto de revalidate = `errStatic` poison-pill job-wide (asimétrico con admission que hace telemetry+nil) → failover loop de TODO el job (`engine_inputs.go:112-116` vs `engine.go:541-543`) |
| F-D-02 | provider | `MODIFY_DECREASE_ACK` sin CapacityStateUpdate previa libera la reservation COMPLETA (`reservation.go:538-552`: key ausente ⇒ remaining=0, RELEASED) → over-commit físico en la ventana (fail-open). Probe reproducido |
| F-D-03 | provider | Effects con `RouteAccountStrategyID` vacío (grant desconocido, input no validado) → `OperationOwnerKey` error → Invoke error → redelivery infinito = head-of-line blocking de TODA la cola provider de la cuenta (`reservation.go:325/:251`, `admission.go:64`, `futures_provider_rules.go:220-263`) |
| F-D-04 | provider | `Reservations` jamás se contrae (cero `delete` en el paquete): grant #257 wedge fail-closed tras 256 grants totalmente liberados (hardscalper V1 los supera) (`reservation.go:176-178`) |
| F-D-05 | provider | Eviction de `RevalidateOutcome` (bound 512) + re-evaluación sin consultar `res.Grant.State` → INVALID retroactivo sobre grant ya EGRESS_AUTHORIZED; simétrico: re-grant resetea `Remaining` (double-count) (`reservation.go:449-462`, `:297-306`, `:199-200`). A3-I4/I5 |
| F-E-02 | gerardmm | `RuleSetAvailable=false` no niega new risk: entry/add emitidos sin autoridad de reglas (contrato propio `operation/mm.go:71-73`; `gerardmm.go:68-113/119-229/514-645`). Probe: qty=20 sin RuleSet |
| F-E-03 | gerardmm | ADDs omiten el chequeo local PER_ORDER (sólo entry lo consulta; `operation/provider.go:12-17` excluye PER_ORDER del pipeline): ADD qty=10 > cap 5 con ratio 2.0 legal. Reproducido |
| F-E-04 | gerardmm | P0 de sizing usa marca exit-side; §9 exige executable-side (ask LONG/bid SHORT): D0 subestimado en el spread → q0 sobredimensionado; pérdida real > budget por contrato (`operation/mm.go:53-59`, `gerardmm.go:154-171`) |
| F-F-01 | bridge | Gate NEW_RISK decorativo en el boundary de side effect: `handleSubmit` sólo exige Connected+Authenticated; con AMBIGUOUS activo un submit NUEVO se transmite físicamente (`session.go:295-344`; TestF1 demostrado). EXE-05/D2-07A §15.5 |
| F-F-02 | bridge | El consumer Kafka nunca commitea offsets (`command_consumer.go:66` AutoCommit off + cero `Commit()`): at-most-once — handler error o restart = mensajes SALTADOS (Initial=OffsetNewest sin offset). La cadena "offset+journal ⇒ DUPLICATE_SUBMIT_SUPPRESSED" (D2-07C §13/§23-C) es inalcanzable con Kafka real; el riesgo residual es PÉRDIDA, no duplicado |
| F-F-03 | bridge | Crash pre-transporte livelockea tras restart real: cursor de step sólo avanza con transmisiones → `ErrCrashInjected` para siempre; AFTER_SUBMITTING mata el propio recovery barrier en cada arranque (`sim_adapter.go:229`, `session.go:208-217`; TestF4) |
| F-F-04 | bridge | Reconciliación 100% journal-driven: `open_order_snapshot` declarada PROVEN pero ningún puerto `ListOpenOrders`; orden viva desconocida por el journal = invisible (D2-07A §17.7; `sim_adapter.go:517-585`) |
| F-G-01 | projection | Proyección `futures_operations` se CONGELA en la operación anterior al reabrir operación el mismo owner: seq reinicia por operación (`engine.go:628/649/653`) vs guard `>` por owner (`pgstore/store.go:87`, PK `066:107`). POC: op-2 convida seq<48 jamás aplica → fila muestra op-1 TERMINAL durante op-2 (D2-04 L252/357, Budgets §17 catch-up) |
| F-G-02 | runtime | `Compose` inyecta `DeterministicIDAllocator` también para LIVE (`runtime.go:109` incondicional; la ruta productiva `main.go:538-540` usa Compose): IDs no-UUIDv7 `fop-000001`, contador compartido sin mutex (data race), colisión tras restart con IDs históricos (D2-04 §2.1/§2.2) |
| F-G-04 | read-model | `SnapshotReadModel.bars` acumula cada barra cerrada sin evicción (`snapshot.go:42-44`; `ApplyBarsSnapshot` PutBar por snapshot): memoria sin techo con duración de run (Budgets §4.1) |
| F-G-06 | routing | El gate/publisher PRODUCTIVO publica fill sin `account_strategy_id` a path 1 con key = account pelada → en production module.yaml entra a `echo/operation` → `ParseOperationOwnerKey` falla → loop de redelivería sobre dirección fantasma (`adapter.go:251-278`, `gate.go:68`; el filtro de correlación existe SOLO en el harness `bridge.go:373-379`) |
| F-G-08 | recovery | REC-03 (Gate D5) sin implementación ni test: cero ocurrencias de `COLD_RECOVERY_REQUIRED` en el repo; la rama fría no tiene seam fail-visible ni failure-injection |
| F-TOP-01 | replay | `context_reads[]` de cada decisión NUNCA se persiste en el path LIVE: el function shell llama `engine.Handle` que descarta el scope (`futures_strategy_engine.go:156`); `LiveScope.Reads()` no tiene consumidor de producción (D4-A1 §6.2/§7: reads son parte del journal en la frontera de commit). Evidencia componente existe (S12); productización = D6/Shot 3. (Consolidación de F-H-01) |
| F-TOP-02 | replay | Los módulos degradan errores tipados del ReplayScope (MISSING/MISMATCH) a `NotReadyReason` fail-closed silencioso (`s1.go:583-599`): un corpus corrupto/drop no produce fallo de replay ruidoso — la divergencia sólo la detecta el comparador del harness (MKT-12 exige "deterministic replay failure"; SPEC §8.3 hard failures). Dirección: propagar IsReplayContextFailure como error duro en modo replay. Descubierto por S12 (TestS12_ReplayFailures) |

### MINOR (28)

F-A-06 (contenido canónico sin publicar a `TopicFuturesMarketCanonical`; refs penden), F-A-07 (payload QUOTE/TRADE malformado ignorado silencioso en ladders), F-A-08 (ingress crudo no-parseable descartado sin evidencia), F-B-04 (horizonte dedup fan-out 1024 por-entrega colapsa a N=200: 6 señales → redelivery re-emite 200), F-B-05 (`signal_fanout` acepta Signals de otra estrategia), F-B-06 (requirements S1 desviados de D4-B3 §3; session-transition seam muerto), F-B-07 (TRADE desordenado hace rollback del día), F-B-08 (triggers sin pin de StreamID configurado), F-C-09 (reciclaje de identidad de acción `repl:<order>:v1` → dedup provider puede devolver grant cacheado equivocado), F-C-10 (MaxFillsRetained = wedge permanente job-wide; comentario contradice código), F-C-11 (MaxOrdersRetained nunca enforced), F-C-12 (egress key=CommandID sin orden SUBMIT→CANCEL por orden en multi-partición), F-C-13 (operation_event_seq con gaps + mutación post-terminal benigna), F-D-06 (guard seq por-order vs write cumulativo por-operation: rollback de firm cross-orden), F-D-07 (sin defensa overflow int64 en envelope math), F-D-08 (replay de deny mezcla provenance: DecisionID original con autoridad corriente), F-D-09 (estado muerto ReleaseDedup), F-E-05 (HardMonetaryHeadroom ausente = +infinito en vez de fail-closed), F-E-06 (decode mm_state silencia corrupción numérica → re-add post-corrupción), F-E-07 (MANAGEMENT_SIGNAL(OPEN) omite precedencia profit exit), F-F-05 (dedup de acciones sólo in-memory; ActionIDs del journal jamás consultado; re-cancel post-restart = 2 transmisiones), F-F-06 (dedup de fills in-memory: restart re-publica fills de non-terminal; absorbido por Core FillDedup), F-F-07 (SessionGeneration campo muerto: stale-owner detection no implementada), F-F-08 (estado sin bound en corrida larga: mapa de journal completo en memoria, O(N²) en storms), F-F-09 (wiring productivo del sim venue crea venue vacío por arranque: contradice contrato "survives process death"; evidencia EXE-04 cross-restart sólo in-process), F-F-10a/b (guard transporte fail-open si ReadinessInputs errora; sameIntent omite ContractID), F-G-05 (raw-ingress no verifica identidad payload-vs-owner; fallback legacy acepta cualquier Input JSON), F-G-07 (poison-pill sin DLQ en projector: registro inválido detiene el consumer group para siempre).

### NOT_A_FINDING (verificaciones positivas que RESISTIERON el ataque)

- **Zero blind duplicate physical submit** (núcleo S10): resiste en los 9 puntos de inyección — todo camino que puede duplicar transmisión pasa por el guard durable `(execution_account_id, client_order_id)` + idempotencia nativa; EXE-04 probado en unidad y vertical. Celdas AMBIGUOUS (6/7) fallan hacia pérdida (F-F-02), nunca hacia segunda orden física.
- **Sin fallback a current state en replay**: `ReplayScope` estructuralmente no puede (`replay.go:19-24`, sin campo ReadModel); MKT-12 dirección no-fallback garantizada.
- **Position nunca es autoridad lógica**: cero referencias en el motor Operation; raw-ingress dropea POSITION/SESSION; no existe synthetic Fill por delta (grep exhaustivo).
- **canonical_event_id != stream_seq**: separación correcta en toda la cadena (ingress/canonicalize/guard); sin content-dedup (MKT-05 sobrevive); conflicto same-seq fail-visible.
- **GROUP_WEIGHTED/WEIGHTED_GROSS/WEIGHTED_NET_ABS**: correctos — recálculo independiente (Python) reproduce TODOS los literales de los tests; fail-closed de pesos verificado (doble barrera). (La remediación C no tiene defecto residual; el defecto está en GROSS/NET_ABS scopeados, F-D-01.)
- **Fórmulas GerardMM**: recálculo independiente exacto en los 9 valores borde; exit ⟺ P≥TP; decimales exactos (big.Rat en todo el path); funded fail-closed completo; XOR de branch aritméticamente imposible de violar; no martingale; stop monotónico.
- **REC-04 run provenance**: sellada en la identidad misma (DeriveSignalID hashea RunMode+RunID); facts/grants transportan provenance; S12 la verifica físicamente (TestS12_REC04).
- **Virtual DomainClock**: cero wall-clock en rutas de decisión D5 (grep completo; los `time.Now` son LIVE-defaults sobreescritos por Compose o telemetría/transporte por contrato).
- **N=200 estructural**: Strategy eval=1 por isla; market singletons por stream; 1 Signal → exactamente 200 deliveries (pineado); trabajo account-local; sin multiplicación de subscripciones/indicadores.
- **Hot-path DB**: cero I/O síncrona de PG en tick/Strategy/MM/provider (grep).
- **066 SQL**: up/down coherentes, tipos exactos (bigint + decimal canónico), sin mm_state (test dedicado), guardias pinneadas textualmente.
- **Projector (salvo F-G-01)**: commit-after-apply, redelivery/stale/future-seq/catch-up convergen (tests), no recovery authority, no mm_state.
- **Venue translation pin**: `AccountStrategyID` excluido del submit view; órdenes venue idénticas ante correlaciones distintas (imposible contaminar).
- **M1**: state+egress en la misma transacción del handler; guard `CommandPublished` (D2-04 I13); ReadCommitted.
- **1 evaluación → 1 Signal → N deliveries**: verificado estructuralmente (SCL-01).
- **Bounded state owners Operation**: evicción total en TERMINAL/open; caps de dedup (salvo F-C-10/11 y F-G-04).
- **Obs §20**: 22 puntos wired en superficies productivas, measurement-only (ningún owner decide por métricas).
- **F-G-03 REFUTADO** (ver nota en Executive/Git evidence).

## 3. S12 evidence (D5-S12 COMPLETE — infraestructura test-only @ 9275fa74)

Superficie nueva (3 archivos, `v3/core/internal/futuresvertical/`, product code intacto):

- `replay_driver.go` — ReplayDriver: `RecordStrategyDecision` (capture-as-consumed vía `marketctx.LiveScope` real) / `ReplayStrategyDecision` (`marketctx.ReplayScope` + **read model envenenado**: toda view con valor y versión "poisoned" — prueba estructural de no-fallback) / `AssertExactReplay` (identidad: absorbed/evaluated/eval_seq/cycle_seq/signal_id; semántica: JSON canónico de Signals + SignalDetails byte-equal + post-state byte-equal; **sin tolerancia**) / `CorruptContextReads` (5 modos) / `PoisonedReadModel`.
- `s12_exact_replay_test.go` — MKT-10/11/12/13 componente + goldens:
  - `TestS12_S1_ExactReplay_Golden_Breakout` — OPEN breakout con stop 21695 exacto; corpus de reads: ordinales densos 1-based, sin reads de stream ajeno; replay byte-idéntico sobre modelo envenenado; golden JSON pineado (`"intent": "OPEN"`, `"run_mode": "LIVE"`, eval_seq 61, stop 21695).
  - `TestS12_S1_ExactReplay_SecondDecision` — CLOSE_ALL stop-hit de la MISMA run: 2ª decisión con su propio corpus.
  - `TestS12_S2_ExactReplay_Golden_Pullback` — S2 (60 H4 + 20 5m, BB 20/2.0 population): OPEN LONG con basis 21598.80/lower 21592.68 (poblacional) y stop; replay exacto.
  - `TestS12_ReplayFailures_FailVisible` — MKT-12: mutate-value/digest ⇒ corpus corrupt tipado en `NewReplayScope`; swap-keys/drop ⇒ no-fallback (cero signals, NotReadyReason — ver F-TOP-02) + Close strict detecta; extra-read ⇒ `REPLAY_CONTEXT_READ_UNUSED`; corpus vacío ⇒ sin fallback.
  - `TestS12_ReplayAnchor_MissingCorruptWrongDigest` — MKT-13: `REPLAY_ANCHOR_MISSING` / `REPLAY_ANCHOR_INVALID` (kind, digest mismatch vs manifest) + `RunManifest.VerifyInitial` falla visible ante initial reescrito.
  - `TestS12_GerardMM_SameInput_SameDecision_Golden` — fórmulas congeladas con referencia independiente big.Rat (remaining TP, loss budget en 5 bordes) + sizing entry qty=2 verificado a mano (2000/(50pt×$20)) + determinismo entre managers frescos (byte-equal).
- `s12_backtest_test.go` — pipeline:
  - `TestS12_Backtest_DoubleRun_Deterministic` — BACKTEST = run nuevo determinista: 2 verticals frescos, mismo run identity pinneado, inputs históricos idénticos → Signals/Commands/Facts/ProviderFacts **byte-idénticos**; golden: OPEN→CLOSE_ALL, provenance BACKTEST/bt-golden-1.
  - `TestS12_REC04_RunProvenanceIsolation` — LIVE vs BACKTEST mismo input: cada Signal/Command/Fact porta su propia provenance; signal_ids distintos entre runs (identidad sellada); cero run-id ajeno en la evidencia del otro.
  - `TestS12_RunJournal_OrderedRecordingLive` — RUN_START (control frozen, delivery test-only) activa el recording: RUN_START inline + 1 ref por input canónico aceptado, owner_input_seq estrictamente creciente, runtime_ts no-decreciente, identity+order coordinate por entrada, digest presente; manifest inmutable con anchor identity sellada; `VerifyAnchor` OK.
  - `TestS12_RunJournal_DeadWithoutRunStart` — sin RUN_START: cero entries/manifests (missing recording detectable fail-visible).

Corpus golden: generado determinísticamente por los fixtures (geometry idéntica a los fixtures verticales congelados; VirtualClock; IDs deterministas) — reproducible bit-a-bit desde el commit. Evidencia al vuelo en el run de tests; sin bins commiteados.

**Corpus coverage de igualdad**: 100% de las decisiones comparadas a nivel componente (S1: 2 decisiones con corpus propio; S2: 1; GerardMM: matriz golden completa) + 100% de la evidencia de pipeline comparada byte-a-byte (signals+commands+facts+provider facts en BACKTEST×2 y LIVE vs BACKTEST). Contador verificado por `require.Len`, no por afirmación.

**Límites D6 documentados** (no convertidos en PASS): persistencia productiva de context_reads[] en el journal (F-TOP-01); re-ejecución del warm-up corpus del anchor por el lane; replay físico Kafka; SessionWindow proyectada por el harness (no por el lane); medición numérica Budgets.

## 4. ATP matrix (casos relevantes al Shot 2)

| ATP case | Evidencia existente | Evidencia adversarial nueva | Veredicto |
|---|---|---|---|
| MKT-01/02 (identity vs seq) | unit tests | A: separación correcta; conflicto same-seq fail-visible | PASS |
| MKT-03/05 (redelivery/identical trades) | unit tests | A: guard NOOP pre-mutación; sin content-dedup | PASS |
| MKT-06/07 (switch vs rollover) | unit tests | A: barrier epoch correcto; nota sin enforcement de fuente post-switch (ventana acotada) | PASS (nota) |
| MKT-08 (crash/order recovery) | unit tests | A: JournalBuilder assertions | PASS |
| MKT-09 (late correction) | s1_test | B: corrección no re-evalúa; estado intacto | PASS |
| **MKT-10 (ContextRead capture)** | marketctx unit | S12 TestS12_S1/S2: capture-as-consumed, ordinales densos, memoización, sin foreign-stream | **PASS (componente)** |
| **MKT-11 (exact replay context)** | marketctx/engine unit | S12: replay byte-idéntico sobre modelo envenenado (S1×2, S2) | **PASS (componente; D6 golden pipeline)** |
| **MKT-12 (missing/extra read)** | marketctx unit | S12 TestS12_ReplayFailures: 5 modos + empty; no-fallback OK; loudness degradada → **F-TOP-02** | PASS no-fallback / **FAIL loudness** |
| **MKT-13 (anchor)** | market unit | S12 TestS12_ReplayAnchor + TestS12_RunJournal (anchor sellado en manifest vivo) | PASS contrato / D6 golden |
| **MKT-14 (timer close sin tick)** | test MockContext (falsa confianza) | A R1/R3: **VIOLADO** (F-A-01/F-A-02) | **FAIL** |
| **MKT-15 (break grid)** | test manual filtrado | A: lógica pura correcta, mecanismo roto por F-A-01/03 | **FAIL (mecanismo)** |
| MKT-16 (stale ≠ READY) | unit tests | A: layering correcto | PASS |
| CAL-01..04 | calendar tests | (A: F-A-03/04 afectan hot path del calendario) | PASS puro / FAIL hot-path |
| S1-01..13 | s1_test | B: exactos salvo F-B-03 (stop con huecos) y F-B-01 (CycleOpen) | 11/13 PASS, 2 FAIL |
| S2-01..09 | s2_test | B: exactos (population stddev, same-boundary, basis CLOSE_ALL) | PASS |
| SIG-01..04 | fanout tests | B: determinismo OK; F-B-05 (signal foráneo aceptado) | 3/4 PASS |
| ADM-01..05 (local) | operation tests | C: F-C-03 (deferred OPEN sobrevive CLOSE) | 4/5 PASS, 1 FAIL |
| EXP-01..08 | operation tests | C: F-C-01 (EXP-04/07 violados en la carrera), F-C-07 (EXP-05 consagra defecto) | **FAIL crítico** |
| TERM-01/02/04/05 | operation tests | C: terminalidad correcta, duplicate finality no-op, post-terminal seguro | PASS |
| TERM-03 (EXE) | bridge sim | F: PASS con inyección | PASS |
| PRV-01..11 | provider tests | D: F-D-02/04/05 (modify-decrease, wedge, retroactive INVALID) | parcial FAIL |
| MM-01..18 | gerardmm tests | E: fórmulas exactas; F-E-01 (TP inalcanzable), F-E-02/03/04 | 14/18 PASS, 4 FAIL |
| EXE-01..13 | bridge tests | F: EXE-04/09/13 PASS; EXE-05 (new risk gate) **FAIL**; EXE-11 parcial (F-F-06); kafka real inalcanzable (F-F-02) | parcial FAIL |
| REC-01 | restart_idempotency_test | G: PASS | PASS |
| REC-02 | projector tests | G: stale seq no-op | PASS |
| REC-03 (cold recovery) | — | G: **AUSENTE en el repo** (F-G-08) | **INCOMPLETE** |
| **REC-04 (provenance isolation)** | — | S12 TestS12_REC04 | **PASS** |
| SCL-01 (N=200) | fanout structural | G+B: verificado; F-B-04 (horizonte dedup) | PASS estructural / deuda D6 |
| SCL-02 (account isolation) | vertical tests | G: PASS | PASS |
| Budgets §20 | obs_points_test | G: 22 puntos wired | PASS (medición D6) |

## 5. Hard-budget review

- **200-account topology**: estructuralmente conforme (eval=1, singletons de mercado por stream, 200 deliveries pineado por test, account work account-local). Medición numérica = D6.
- **Bounded-state checks**: 1 violador de producción (**F-G-04** bars map del read model); F-B-04 (dedup fan-out vs N); harness-only unbounded (bus/collector/correlation index — contrato demo); F-F-08 (bridge journal en memoria O(órdenes ever)); F-D-04 (Reservations sin contracción); F-C-10/11 (caps Operation no enforced o wedge). Inventario completo en el reporte G.
- **Hot-path DB absence**: verificado por grep — cero I/O síncrona PG en owners futures.
- **Provider revalidation**: mandatory every-grant presente sin fast-path; defectos: F-D-05 (eviction rompe one-shot), F-C-04 (revalidate sobre orden muerta), F-C-08 (conflicto = poison-pill).
- **M1/M2**: M1 intacto (transacción única state+egress, guard CommandPublished); M2 journal fsync sólido (corrupción fail-visible, AMBIGUOUS nunca GC) con los gaps F-F-01/02/03/04.
- **Recording/replay topology**: stream owner graba (manifest+refs+inline); **analytics no journaliza** (F-A-05); **contenido canónico sin publicar** (F-A-06); **context_reads no persistidas** (F-TOP-01); journal vivo demostrado por S12 con RUN_START.

## 6. Commands (evidencia física real)

```text
git rev-parse HEAD                → 4c41ee773f45665df163d46cd21b4ccb2842f489 (== origin/feature/d5-foundations)
git status/worktree list          → clean; worktrees Shot 1 intactos
git checkout -b feature/d5-shot2-adversarial (desde 4c41ee77)

cd v3/sdk     && GOTMPDIR=/home/kor/aranea/gotmp go test ./futures/...   → ok ×13 packages
cd v3/core    && GOTMPDIR=/home/kor/aranea/gotmp go test ./internal/futuresvertical/ ./internal/functions/ ./internal/futuresruntime/
                                                                         → ok (futuresvertical 15.8s incl. S11+S12)
cd v3/futures-bridge     && go test ./...                                → ok ×9 packages
cd v3/futures-projector  && go test ./...                                → ok (pgstore, projector)
go test ./internal/futuresvertical/ -run TestS12 -v                     → 8/8 PASS (S1×2, S2, FailVisible×5+empty, Anchor, GerardMM×4, Backtest, REC04, Journal×2)
git commit -m "test(s12): ..."                                          → 9275fa74; árbol clean
```

Reproducers de reviewers ejecutados FUERA del repo (`/home/kor/aranea/gotmp/{repro,falsify,rg01-poc,reviewd-echo,reviewer_e_probe}` vía módulos scratch con `replace`): F-C-01..06, F-B-01..08, F-D-01..05, F-F-01..05, F-A-01..04, F-G-01 (POC projector), F-E-02/03.

## 7. Existing tests challenged (falsa confianza)

- `TestFuturesMarketAnalytics_TimerClosesWithoutNextTick_MKT14` + `BarClosedDeliveryOnNaturalClose` + `InternalBreakTruncates_MKT15` (A): MockContext graba sin entregar sends y los tests disparan el firing a mano — enmascaran F-A-01/02/03 por completo. MKT-14/15 sin cobertura real.
- `TestEXP05_ModifyDecreaseReleasesReservation` (C): **consagra F-C-07** — aserta el release completo sin campo qty como comportamiento correcto.
- `TestEXP04_CancelRequestRace` + `TestTERM02_TerminalBlockedByPendingFinality` (C): mitades complementarias del escenario F-C-01; jamás inyectan el late fill del EXIT tras el replan — la conjunción de ambos ES el blocker.
- `TestComputeClaims` (C): sin órdenes CANCELLED/EXPIRED con QExecMax>0 — el hueco de accounting es invisible.
- `TestEngine_ConfigCycleActivation_*` (B): módulo scripteado que reporta cycleOpen — validan el motor, no los módulos reales (F-B-01 invisible).
- Capacity/provider tests (D): todos `Scope: "account-wide"` — la dimensión scope no tiene ni un test (F-D-01 invisible); `TestRelease_ModifyDecreaseAndFinality` pre-alimenta el CapacityUpdate — el path fail-open sin evidencia no existe en tests.
- gerardmm tests (E): sin caso `RuleSetAvailable=false`; adds sin ratio>1 (F-E-02/03 invisibles).
- Bridge (F): paquete `adapters/kafka` cero tests contra broker — la semántica commit/redelivery más citada por las autoridades es la menos probada (F-F-02); `TestEXE05` nunca despacha submit nuevo con ambigüedad activa.
- Projector (G): ningún escenario cross-operación sobre el mismo owner_key (F-G-01 invisible); `TestCompose_RegistersAllSixOwners` compone LIVE con allocator determinista sin pinnear formato (F-G-02 consagrado).

## 8. Shot 3 inputs (hallazgos que requieren corrección; NO corregidos aquí)

Prioridad sugerida para el Primary Manager:
1. **F-A-01 (+F-A-02/03/04)** — scheduling real de timers (SendAfter + generation cancel/replace), re-agenda prospectiva de calendario, binding determinista stream→calendar. Sin esto, la semántica de barras no es certificable en runtime real.
2. **F-C-01 (+F-C-02/07)** — accounting de claims post-cancel-ACK + wire de release con cantidad + dedup/monotonicity de modify observations. Garantía central D4-A2.
3. **F-D-01/02/04/05** — scope-aware capacity, release fail-closed sin evidencia, contracción de reservations, one-shot de revalidation ante eviction.
4. **F-E-01/02/03/04** — trigger de mercado/PnL para GerardMM (TP vivo), RuleSetAvailable fail-closed, PER_ORDER en adds, marca executable-side.
5. **F-B-01/02/03** — CycleOpen de S1, absorb de señal expirada, contigüidad del grid en technicalReference.
6. **F-F-01/02** — NEW_RISK gate en el boundary + commit de offsets (pérdida → at-least-once).
7. **F-G-01/02/06/08** — identidad de proyección por operation_id (o seq por owner), UUIDv7 en LIVE, correlation gate en el publisher productivo, REC-03 seam.
8. **F-TOP-01/02 + F-A-05/06** — persistencia de context_reads, loudness de replay, journal de analytics, publicación del contenido canónico (paquete EXACT_REPLAY product-ready para D6).

## 9. Exit status

```text
MACRO_SHOT_2_REVIEW = COMPLETE
ADVERSARIAL_RESULT  = FINDINGS (4 BLOCKER · 32 MAJOR · 28 MINOR)
S12                 = COMPLETE (test-only @ 9275fa74)
No se emite D5 CLOSED ni EF_D5_FOUNDATION_PASS. No se inicia Shot 3.
```

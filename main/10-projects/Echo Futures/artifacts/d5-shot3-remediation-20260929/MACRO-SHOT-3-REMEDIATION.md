# ECHO FUTURES — D5 MACRO SHOT 3 — CORRECTION + FINAL VERIFICATION

**Role:** TOP Principal Remediation Engineer / Systems Correctness Lead
**Fecha:** 2026-09-30
**Método:** 8 lanes de remediación en paralelo (worktrees por lane sobre la branch de integración) + integración TOP con suites completas + verificación final (S12, EXACT_REPLAY con corpus LIVE, BACKTEST×2, propiedades adversariales, ATP).

## A. Executive

```text
MACRO_SHOT_3_REMEDIATION = COMPLETE
final SHA                = 5f9fadde (origin/feature/d5-shot3-remediation == local, tree clean)
blockers                 = 5/5 CLOSED (F-A-01, F-C-01, F-D-01, F-E-01, F-MGR-01)
majors aceptados         = 30 CLOSED · 1 DUPLICATE (F-TOP-01→F-MGR-01) · 1 DEFERRED_TO_D6 (F-A-05)
majors restantes         = 0 abiertos; 0 REJECTED
S12 final                = PASS 13/13 (incl. corpus LIVE→EXACT_REPLAY byte-exact y BACKTEST×2 byte-idéntico)
recomendación            = REMEDIATION COMPLETE → decisión de gate D5 al Primary Manager (EF_D5_FOUNDATION_PASS sigue UNSET)
```

No se emite `D5 CLOSED` ni `EF_D5_FOUNDATION_PASS` (§28). Vuelve al Primary Manager.

## B. Git evidence

```text
base             = 9275fa74 (feature/d5-shot2-adversarial, publicada a origin ANTES de bifurcar; Shot 1 = feature/d5-foundations 4c41ee77 intacta)
branch           = feature/d5-shot3-remediation (creada desde exactamente 9275fa74)
final commit     = 5f9fadde
remote SHA       = origin/feature/d5-shot3-remediation = 5f9fadde (== local)
dirty state      = clean (git status: 0)
commits          = 49 (41 por-finding/seam + 8 merges --no-ff de lanes)
files changed    = 71 archivos, +7035/−329
lanes            = shot3/lane-{a-market,b-strategy,c-operation,d-provider,r-recording,f-bridge,e-mm,g-runtime} (0 commits sin mergear; retenidas para review independiente)
master           = NO modificado; sin force-push; sin rebase de branches publicadas
```

Commits por finding (resumen; lista completa en `git log --oneline 9275fa74..5f9fadde`): ver sección C/D.

## C. BLOCKER closure matrix

| Finding | Authority | Original reproducer | Fix | Verification | Status |
|---|---|---|---|---|---|
| **F-A-01** | D2-06C §7/§9/§12; MKT-14/15 | 1 trade → 5000 mensajes sin quiescer + BAR_CLOSED prematuro por el primer trade | `7f565b2f`: `ensureBarTimer`/`sendSessionTimer` usan `ctx.SendAfter(boundary−now)`; bus vertical gana `FireAt` + reloj (honra delay en `Drain`/`DrainStep`/`DrainWithPolicy`); MockContext con reloj controlable + `DeliverDue` | trade antes del boundary → barra forming (`TestFuturesMarketAnalytics_TimerClosesWithoutNextTick_MKT14`, `TestFuturesVertical_TimerFiresAtBoundary_BoundedQuiescence`); BAR_CLOSED exactamente 1× en el boundary; sin cadena recursiva ni livelock (`<50` mensajes vs 100k budget) | **CLOSED** |
| **F-C-01** | D4-A2 A2-I3/A2-I8/W2/W3; EXP-04/07 | LONG→cancel ACK→replan→late Fill → x_o=−2 (inversión física) | `1ae5e79e`: `ComputeClaims` suma `QExecMax>0` de TODAS las órdenes con evidencia venue de fills adicionales (CANCELLED/EXPIRED/residuo FILLED); sólo `TERMINAL_EXECUTION_FINAL` (y REJECTED) liberan; sin notion de claim paralelo | `TestFC01_CancelAckKeepsClaimSafeLONG/SHORT` (reproducer portado in-repo, resultado SEGURO: sin segunda orden, exposición 0, sin breach); `TestEXP04/07`, `TestTERM02` verdes en la conjunción completa | **CLOSED** |
| **F-D-01** | D4-A2 §7; D2-05C L131/135 | NET_ABS scope=ES cap=5 con ES+10/NQ−10 concedía ES BUY 1 (netting account-wide N=0) | `a36720fb`: cada cap evalúa SÓLO los buckets de su universo tipado (account-wide / instrument / product-group) en GROSS, NET_ABS y WEIGHTED_GROSS/WEIGHTED_NET_ABS; sin string matching genérico | `capacity_scope_test.go` con valores esperados calculados a mano independientes de los helpers: ES BUY 1 ⇒ DENY (11>5); instrument/product-group/account-wide + coexistencia cross-scope | **CLOSED** |
| **F-E-01** | D4-B2 §17/§18; MM-17; S09 | P_day cruza TP → `profitExit` jamás invocado (sólo exits por pérdida) | `03140c65`: trigger `ACCOUNT_ECONOMICS` en la superficie MM + Input de economics update al engine (dedup por UpdateID, serializado, sin polling ni owner nuevo); gerardmm `onAccountEconomics` §17.3→§17.5; el mismo GerardMM, dentro de echo/operation | E2E vertical: exposición activa + update autoritativo PnL≥TP → `TerminationIntent MONETARY_PROFIT_OBJECTIVE` → cero new risk → exit seguro de qty reducible, SIN nuevo Fill/OrderFinal en el cruce (`TestAccountEconomicsTrigger_*` ×6 + `economics_trigger_vertical_test.go`); PnL stale ⇒ fail-closed | **CLOSED** |
| **F-MGR-01** | D4-A1 §6.2/§7 (Manager) | LIVE nunca produce el corpus: `engine.Handle` descarta el LiveScope | `d6d1c811`+`0bcf3906`: el fn del strategy engine crea su `LiveScope`, llama `HandleWithScope` y emite `DECISION_EVIDENCE` (reads ordenados + identidad de decisión, sellado por digest) en la MISMA transacción del commit (persist+egress); sin RUN_START el recording queda muerto como antes | `TestS12_LiveDecision_EvidenceFromJournal_ReplaysExactly`: corpus extraído DEL JOURNAL persistido (no sintético) → ReplayScope sobre read model envenenado → identidad 100%, semántica 100%, context-read equality exacta; corrupt/missing/digest/unused fallan tipados y visibles; `RecordingDeadWithoutArming` preserva opt-in | **CLOSED** |

## D. MAJOR triage (32/32 sin omisiones)

| Finding | Decisión | Reason | Fix commit / test si ACCEPTED |
|---|---|---|---|
| F-A-02 | ACCEPTED | viola invariant del blocker (stale NO-OP sin matar timer vivo); reproducido | `5ff76ac3` · `TestFuturesMarketAnalytics_StaleTimerFiringNoopPreservesLiveTimer` |
| F-A-03 | ACCEPTED | regresión de versión mata cadena de sesiones (D2-06C §12); reproducido | `790f20c1` · `TestFuturesMarketAnalytics_CalendarUpsertRearmsSessionChain` |
| F-A-04 | ACCEPTED | no-determinismo map-iteration (D2-06C same-input/same-output); reproducido 56/4 grids | `61176060` · `TestFuturesMarketAnalytics_CalendarAuthorityDeterministic` |
| F-A-05 | DEFERRED_BY_FREEZE→D6 | journal del analytics island = paquete "EXACT_REPLAY product-ready"; el Manager promovió a blocker sólo el context_read de estrategia (F-TOP-01); tocarlo ahora reabría la superficie de Lane A sin mandato | — (documentado como D6) |
| F-B-01 | ACCEPTED | SPEC §23: promoción de config pendiente a mitad de ciclo; reproducido | `db3cf385` · test de ciclo del S1 real |
| F-B-02 | ACCEPTED | D4-B3 §11: señal expirada = absorb, no poison loop; reproducido | `357d0f00` · engine/s1 tests |
| F-B-03 | ACCEPTED | D4-B3: hueco intra-ventana ⇒ stop técnico INCORRECTO en vez de fail-closed; reproducido (97.25) | `72250a3d` · contigüidad exigida; fixture S12 corregido (54→66 buckets, ver §F) |
| F-C-02 | ACCEPTED | observación modify stale regrasa términos (D4-A2 §10); reproducido 4→2→1 con venue en 4 | `a0c14119` · dedup por ActionID + ACCEPTED/CONFIRMED sólo + guard terminal |
| F-C-03 | ACCEPTED | ADM-03: CLOSE no invalida OPEN diferido; reproducido | `dbf4fac0` · PendingNextCycleOpen limpiado |
| F-C-04 | ACCEPTED | revalidate VALID sobre orden muerta ⇒ EGRESS_AUTHORIZED + leak perpetuo; reproducido | `78d725bb` · release en vez de autorizar |
| F-C-05 | ACCEPTED | ModifyIntent vivo tras decrease aceptado ⇒ lockout; reproducido | `50c37c8b` · intent limpiado al aplicar outcome |
| F-C-06 | ACCEPTED | D2-04 §6: DeliveryDedup evacuado ⇒ ADD desde duplicado; reproducido | `03736931` · dedup sobrevive materialización |
| F-C-07 | ACCEPTED | D4-A2 A2-I4/W5: release sin qty libera grant completo; TestEXP05 consagraba el defecto | `5d02adcf` (seam wire) + `b782c56a` (emit con `ReleasedQExecMax`) · TestEXP05 corregido a release quantity-accurate |
| F-C-08 | ACCEPTED | conflicto revalidate = poison-pill job-wide (asimétrico con admission); reproducido | `80bf4a44` · telemetry+absorb; duplicado de causa raíz cerrado en `891521e2` (qty malformada en modify obs ⇒ absorb, `TestFC08_Dup_*`) |
| F-D-02 | ACCEPTED | MODIFY_DECREASE_ACK sin evidencia liberaba TODO (fail-open); probe reproducido | `7c8d6b9a` · fail-closed sin evidencia; con evidencia libera `min(stored, released)` |
| F-D-03 | ACCEPTED | efectos a owner fantasma ⇒ redelivery infinito de la cola provider; reproducido | `de08500a` · absorb con telemetría en admission; jamás efectos a dirección inexistente |
| F-D-04 | ACCEPTED | Reservations sin contracción ⇒ wedge fail-closed en grant #257; reproducido | `2190d1bb` · contracción en convergencia de full-release (257 ciclos verdes) |
| F-D-05 | ACCEPTED | A3-I4/I5: eviction de outcome + re-eval ⇒ INVALID retroactivo / re-grant resetea Remaining; reproducido | `76b3be9d` · one-shot consultando `Grant.State` |
| F-E-02 | ACCEPTED | contrato mm.go: RuleSetAvailable=false niega new risk; probe qty=20 sin RuleSet | `efdd437d` · deny fail-closed entry/add; exits siguen vivos |
| F-E-03 | ACCEPTED | D4-B2: ADDs saltaban PER_ORDER (qty 10 > cap 5 legal); reproducido | `c9b3c4df` · PER_ORDER gatea el add path |
| F-E-04 | ACCEPTED | §9: sizing executable-side (ask LONG/bid SHORT); reproducido | `54419fb0` · preferencia por quote autoritativo; fallback a mark documentado (ver §J) |
| F-F-01 | ACCEPTED | EXE-05/D2-07A §15.5: NEW_RISK gate decorativo; TestF1 reproducido | `8843b3dc` · gate en el boundary del side effect; 0 transmisiones con ambigüedad activa |
| F-F-02 | ACCEPTED | D2-07C §13/§23-C: offsets jamás commiteados ⇒ at-most-once (pérdida); reproducido | `f55226b7` · commit sólo tras durabilidad M2 (at-least-once + guard journal ⇒ DUPLICATE_SUBMIT_SUPPRESSED demostrado); broker real = D6 (seam-tested) |
| F-F-03 | ACCEPTED | crash pre-transporte livelockea tras restart; TestF4 reproducido | `ece903ab` · re-drive desde journal durable; sin blind resend |
| F-F-04 | ACCEPTED | D2-07A §17.7: orden viva desconocida = invisible; reproducido | `79b3d200` · port ListOpenOrders + cuarentena fail-visible (never cancelled/adopted); superficie in-process (ver §J) |
| F-G-01 | ACCEPTED | D2-04 L252/357: seq por operación vs guard `>` por owner ⇒ proyección congelada; POC reproducido | `8d087ccb` · watermark OwnerEventSeq monotónica por owner; 066/projector intactos |
| F-G-02 | ACCEPTED | D2-04 §2.1/§2.2: LIVE con allocator determinista + data race + colisión post-restart; consagrado por TestCompose | `5c98b7e2` · UUIDv7 en LIVE (formato pineado), determinista sólo en runs deterministas, mutex; BACKTEST×2 sigue byte-idéntico |
| F-G-04 | ACCEPTED | Budgets §4.1: bars del read model sin techo; reproducido | `6ac7ca04` · retención por (stream,timeframe) config-driven (default 256 ≥ máximo reach-back); reads byte-idénticos dentro de la ventana alcanzable |
| F-G-06 | ACCEPTED | D2-07C: fill sin account_strategy_id publicado a path 1 con key account pelada ⇒ redelivery loop en dirección fantasma; reproducido | `0ad4826c` (gate de correlación en el ingress echo/operation) + `9e0a31fd`/`5f9fadde` (lado publisher: enriquecimiento desde journal SPEC §18/§20 ANTES de publicar + cuarentena en fuente de op-events no atribuibles; pin de topología extendido a las superficies de correlación) |
| F-G-08 | ACCEPTED | ATP REC-03 ausente (cero COLD_RECOVERY_REQUIRED); reproducido por ausencia | `871ea133` · seam fail-visible `COLD_RECOVERY_REQUIRED` antes de componer owners, sin reconstrucción de estado de trading desde proyecciones; introspección física de checkpoints = D6 |
| F-TOP-01 | DUPLICATE | promovido por el Manager a F-MGR-01 BLOCKER (misma causa raíz); no se duplica | cerrado vía `d6d1c811`+`0bcf3906` |
| F-TOP-02 | ACCEPTED | MKT-12/SPEC §8.3: fallos tipados de replay degradados a NotReadyReason silencioso; descubierto por S12 | `a361d66b` · `IsReplayContextFailure` ⇒ error duro en modo replay (LIVE NotReady intacto, pineado); expectativa de S12 re-pineada (ver §F) |

## E. MINOR disposition (28)

- **Fixed as consequence:** ninguno más allá de los ya cubiertos por las causas raíz de blockers/majors (el duplicado F-C-08 de qty malformada era una superficie NUEVA no registrada, tratada comoduplicate del root F-C-08; sin otros MINORs tocados).
- **Left intentionally:** los 28 MINORs registrados (F-A-06..08, F-B-04..08, F-C-09..13, F-D-06..09, F-E-05..07, F-F-05..10a/b, F-G-05, F-G-07) quedan sin fix por mandato §13 (no estética, no scope creep). Nota: el gap BreakEnd-delivery hacia strategies encontrado por Lane A comparte causa raíz con F-B-06 (session-transition seam muerto) y queda documentado como limitación aceptada de D5, no fijado.

## F. Final S12 evidence

```text
TestS12_Backtest_DoubleRun_Deterministic        PASS  (BACKTEST×2 byte-idéntico: signals+commands+facts+provider facts)
TestS12_REC04_RunProvenanceIsolation            PASS  (LIVE vs BACKTEST: provenance sellada por run, cero cross-run)
TestS12_RunJournal_OrderedRecordingLive         PASS  (RUN_START → journal vivo: refs ordenados, manifest sellado)
TestS12_RunJournal_DeadWithoutRunStart          PASS  (sin armar: cero evidencia — detectable fail-visible)
TestS12_S1_ExactReplay_Golden_Breakout          PASS  (replay byte-idéntico sobre read model envenenado)
TestS12_S1_ExactReplay_SecondDecision           PASS  (2ª decisión, corpus propio)
TestS12_S2_ExactReplay_Golden_Pullback          PASS
TestS12_ReplayFailures_FailVisible              PASS  (5 modos de corrupción: ahora con error tipado duro — F-TOP-02)
TestS12_ReplayAnchor_MissingCorruptWrongDigest  PASS
TestS12_GerardMM_SameInput_SameDecision_Golden  PASS  (fórmulas congeladas byte-idénticas, sin re-pin)
TestS12_LiveDecision_EvidenceFromJournal_ReplaysExactly  PASS  (NUEVO, F-MGR-01: corpus del path LIVE real)
TestS12_LiveDecision_EvidenceFailures_FailVisible        PASS  (NUEVO: corrupt/tamper del journal visible)
TestS12_LiveDecision_RecordingDeadWithoutArming          PASS  (NUEVO: opt-in por isla preservado)
```

Re-pins de S12 (justificados, ninguno para "poner verde"): (1) F-B-03 demostró que el fixture S1 tenía un defecto aritmético (premarket declarado 66 buckets, alimentados 54; el golden 21695 fue calculado a través del hueco) — reparado a 66 contiguos: los VALORES del golden quedaron byte-idénticos, sólo `strategy_eval_seq` 61→73 (warm-up correcto de 72 barras); (2) `TestS12_ReplayFailures_FailVisible` consagraba el downgrade silencioso (F-TOP-02) — ahora exige el error tipado; (3) tabla de fallos del corpus LIVE de integración actualizada al contrato MKT-12 tras el fix F-TOP-02. BACKTEST×2 y REC-04 siguen byte-idénticos.

## G. ATP matrix

Veredicto final caso-por-caso con evidencia corriente en el árbol final: **`atp-final-matrix.md`** (mismo directorio). **115 casos: 111 PASS · 0 FAIL · 2 INCOMPLETE · 2 DEFERRED_TO_D6** (más mitades D6 anotadas en REC-03, EXE-01/02/04/08, MKT-11/13 y Budgets §20). Los 212 nombres de tests citados fueron verificados mecánicamente contra el árbol (existen como `func Test...`); toda fila PASS lleva tests corridos verdes en esta sesión.

- **INCOMPLETE (2)**: MKT-07 (rollover ≠ source switch: la propiedad exacta sin fixture dedicado; evidencia cercana verde en pin de contrato + MKT-06) y TERM-03 (ForceClose con bridge caído → reconexión reconcile-first: escenario exacto sin test; evidencia cercana EXE-09 + BridgeRestart + F4).
- **DEFERRED_TO_D6 (2)**: EXE-14 y SCL-03 (ítems vendor/físicos).
- **Cambios de veredicto vs Shot 2**: MKT-14/15 FAIL→PASS, MKT-12 loudness FAIL→PASS (F-TOP-02), S1 11/13→13/13, SIG 3/4→4/4, ADM 4/5→5/5, EXP→8/8, PRV→11/11, MM 14/18→18/18, EXE→13 PASS (+EXE-14 D6), REC-03 INCOMPLETE→PASS como seam software.
- **Abiertos reflejados**: lineage físico REC-03 = D6; Kafka real seam-tested (F-F-02); gap BreakEnd-delivery (F-B-06, sin fix por decisión) anotado en MKT-15; 066 equal-seq siblings anotado en REC-02; sin productor QUOTE en V1 (casos QUOTE estructurales).

## H. Adversarial regression (rerun sobre el árbol final)

Propiedades re-ejecutadas (todas verdes; comandos en `atp-final-matrix.md`):

- **Market**: boundary de timer, session transition, late correction (MKT09), canonical duplicado (MKT03), conflicto same-seq (MKT02), ordering/epoch barrier (MKT06), readiness (MKT16), timer stale NO-OP con timer vivo, re-agenda prospectiva de calendario, autoridad determinista, quiescencia acotada (18/18 PASS).
- **Strategy**: S1 goldens exact-replay ×2, S2 golden, ciclo S1 (CycleOpen en boundary), fan-out N=200 estructural (SCL-01), absorción de señales expiradas sin poison.
- **Operation**: carrera cancel/fill LONG+SHORT (F-C-01 reproducers), modify/fill, replace overlap (EXP07), múltiples reducing orders (EXP01/02), ForceClose, late Fill, terminalidad (TERM02/04/05), malformed modify absorbida.
- **Provider**: caps scopeados (GROSS/NET_ABS/WEIGHTED ×2 direcciones + coexistencia), grant stale/revalidate one-shot, release fail-closed, contracción 257 ciclos, ghost-route absorb (31 tests).
- **GerardMM**: entry (con sizing executable-side), loss budget, profit objective (cruce sin nuevos facts), adverse/favorable add, partial fill consume intent, profit termination precedencia, missing funded config fail-closed, RuleSetAvailable=false.
- **Bridge**: 9 ventanas de crash (tabla exacta de estado journal), restart, redelivery, AMBIGUOUS, zero blind duplicate physical submit (EXE-04/05/07), EXE-01..13 completos, offsets tras durabilidad, cuarentena de op-event no atribuible.
- **Replay**: corpus LIVE real → EXACT_REPLAY exacto; goldens S1/S2/GerardMM; BACKTEST determinista ×2; corrupt/missing/unused fail-visibles.
- **Projection**: redelivery/stale/catch-up/duplicados (REC-02) + cross-operación sobre el mismo owner (F-G-01).

## I. Commands (evidencia física)

```text
cd ~/aranea/work/d5-foundations-20260929/echo
git checkout -b feature/d5-shot3-remediation 9275fa74 && git push origin feature/d5-shot2-adversarial
# 8 lanes en worktrees shot3/lane-* (evidencia RED→GREEN por finding en lane-evidence/lane-*.md)
cd v3/sdk               && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 ./futures/...              → ok ×13 packages
cd v3/core              && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 ./internal/...             → ok (functions, futuresvertical 25s incl. S12, futuresruntime, automation)
cd v3/futures-bridge    && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 ./...                      → ok ×7 (55 tests; nine crash windows + EXE-01..13)
cd v3/futures-projector && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 ./...                      → ok ×3
cd v3/core && go test -count=1 -run TestS12 -v ./internal/futuresvertical/                             → 13/13 PASS
git push origin feature/d5-shot3-remediation                                                           → 5f9fadde
```

## J. Remaining limitations (estrictamente separadas)

**D5 accepted limitation** (documentadas, no bloquean el gate): proyección 066 dropea snapshots hermanos equal-seq de un mismo evento hasta el evento siguiente (converge; 066 congelado); GROUP_WEIGHTED evalúa su universo tipado como weights map declarado (semántica Shot-1 congelada, tests de fórmula intactos); F-E-04 usa fallback documentado a mark cuando no hay evidencia de quote (sin modelo de spread inventado); cuarentena F-F-04 es superficie in-process/report (los estados del journal congelados no tienen estado quarantine); sin productor QUOTE en V1 (superficie QUOTE estructural).

**D6 work**: F-A-05 journal del analytics island (paquete EXACT_REPLAY product-ready); productor QUOTE / QUOTE-trigger kind en superficie MM; broker Kafka real (los offsets/journal están seam-tested); transportes vendor físicos; medición numérica Budgets §20; introspección física de lineage de checkpoints (REC-03) y automatización de pins; re-ejecución del warm-up corpus por el lane.

**Known bug (candidato a finding, NO fijado — requiere autorización del Manager)**: el path congelado Fill/OrderFinal (`afterFact`, early-return GMM-I15) no re-abre el exit §18 tras la finality de un protective-cancel; el seam ACCOUNT_ECONOMICS lo completa por §19, pero el gap del path congelado merece finding propio.

**Unresolved blocker**: ninguno. **Unresolved major**: ninguno (30 CLOSED, 1 DUPLICATE, 1 DEFERRED_TO_D6).

## Exit status

```text
MACRO_SHOT_3_REMEDIATION = COMPLETE
EF_D5_FOUNDATION_PASS    = UNSET (decisión del Primary Manager)
D5                       = IN_PROGRESS (esperando gate)
```

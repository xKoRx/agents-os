---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo Futures]]"
sprint: 2026-09-24--2026-09-30
start: 2026-09-24
due: 2026-09-30
progress: 45
repo: "xKoRx/echo-futures"
jira:
prs:
aliases:
  - Echo Futures D5 Prop Economics
tags:
  - kind/project
  - area/echo
  - echo-futures
  - prop-economics
created: "2026-09-24"
updated: "2026-09-25"
---

# Echo Futures — D5 Prop Economics

## 🎯 Objetivo

- Validar cuantitativamente la hipótesis económica de Echo Futures sobre las **principales futures prop firms**, midiendo desde `evaluation comprada` hasta `primer retiro real de cash`.
- Determinar, por prop/plan y política simulada, `q_withdraw`, evaluations esperadas por retiro, cash burn, activaciones, probabilidad de retiro dentro de N attempts y EV neto.
- Consumir el simulator v0 certificado de D4 sin reabrir su matemática.

## 📊 Estado actual

- **D5.4 FAIR-NULL + REALISM BRIDGE EJECUTADO — 2026-09-25.** Fair null verdadero por etapas (p_eval=4/7, p_bulto=1/3, p_qualify=1/2 con reload compartiendo p_qualify verificado en source) ejecutado en el engine certificado `cdef2b6b`: EV +$691/mes IND (−62% vs linked p=0.50 de Shot C) y P(month>0)=0.565 — el null fair sigue POSITIVO pero frágil. Realismo de sesión finita (kernel D5.3 exacto, identidades I1–I4 PASS): la positividad NO es robusta — el bracket mensual de diagnóstico cruza el signo entre sqrt(ρ)≈1.4 y 2 (σ√T de sesión en unidades del loss cap); bajo eso degrada al piso de quema de fees (≈−$4.9k/mes). Edge requerido: qualify/reload es la etapa más elástica (+$171/pp; +2.1pp para +$1k/mes, +7.9pp para +2k, +28.8pp para +5k); eval se satura en +$3.4k. Puente Gerard/Tradesfera: 8 hipótesis falsables, todas NO_DATA/NEEDS_MARKET_DATA. `D5_FAIR_NULL_PASS = REVIEW`; recomendación manager `NEEDS_MARKET_DATA` (calibración del reloj de varianza + estimación empírica de p por etapa con ICs). Detalle en §D5.4 Fair-Null + Realism Bridge y artefactos `/home/kor/aranea/work/d5-m1a-shotd-fairnull-20260925/` (fuera del vault).
- **D5-M1A-P150 SHOT B AUDITORÍA ADVERSARIAL — 2026-09-24.** Auditoría independiente completada contra el HEAD local congelado `1dc1fa6afaaabe99ac8648f8c11e293fa9acd17c` (árbol limpio, sin mutaciones): veredicto **AUDIT_FINDINGS** sin BLOCKER de código. A1–A11 PASS: D4 no-regresión probada por byte-equality old-vs-new binarios y gate 47/47; DP del producto ≡ referencia independiente exacta en todas las celdas; MC en 5σ; reloj portfolio exacto (payouts @7/12/17, STOP ocupa slot, pay4 imposible en 20 sesiones); correlación PERFECT_COPY verificada a nivel evento; ledger exacto (49/149/2000/1800/1770); resource safety fail-closed verificado. Hallazgo B-01 MAJOR (proceso): la rama NUNCA se publicó en remoto (el repo no tiene remote) — la corrección pre-Shot-B del manager no se ejecutó; B-02 MINOR: samples congelados difieren por 1 ULP de dp_reference al reconstruir desde HEAD. `D5_TOPSTEP_POLICY_AUDIT_B = REVIEW`; next `PUBLISH_AND_VERIFY_REMOTE_SHA` → `MANAGER_REVIEW_FOR_SHOT_C`. Detalle en §Shot B.
- **D5-M1A-P150 SHOT C EJECUTADO — 2026-09-24.** Publicación remota verificada (`github.com/xKoRx/echo-futures`, remote SHA == audit baseline `1dc1fa6a…`, B-01 CLOSED), correction commit `6f7ae58` (B-03) y certified result commit `cdef2b6` (B-02) publicados y verificados. Matriz congelada completa ejecutada bajo protocolo pre-declarado: región positiva ql=150 desde p=0.50 (+$1,838/mes); break-even mensual p*≈0.509 (ql=300), ≈0.561 (500), ≈0.646 (1000), ≈0.675 (1500), ≈0.691 (2000); PERFECT_COPY iguala la EV pero colapsa P(month>0) y engorda ambas colas; margen del horizonte K=4 +$230..$3,669/mes según p (material sólo con ql bajo y p alto). Certificación completa verde. `D5_TOPSTEP_POLICY_RESULT_C = REVIEW`; next `MANAGER_REVIEW_SHOT_C`. Detalle en §Shot C.
- **D5-M1A TOPSTEP SPEC FREEZE — 2026-09-24.** SPEC funcional + técnica del fast track Topstep congeladas en [[D5-M1A — Topstep Functional SPEC]] y [[D5-M1A — Topstep Technical SPEC]] sobre el modelo D5.3 ACEPTADO: lifecycle PURCHASE_EVALUATION→WITHDRAWAL_RECEIVED|BURNED|INCOMPLETE, kernel 1D finite-horizon (sin `(e,m)`), MLL EOD trailing+lock, consistencia 55%, winning days, MAX_ELIGIBLE 90/10 cap $2,000, ledger con `I_act`, presupuesto de error C2, matriz `sqrt(ρ_full)∈{0.1,0.25,0.5,1,2,4}×adds{0..4}` delta=0, aceptancia T1–T8 intactos + S-subset Topstep (S09/S10/S13/S17/S21/S23/S24 DEFERRED a M1B) + fixtures TS-F01..16, y paquetes Shot A/B/C preparados sin ejecutar. Sin código, sin simulación, sin TPT, sin Tier-2. `D5_TOPSTEP_SPEC_PASS = REVIEW`; next action `MANAGER_ACCEPT_AND_DISPATCH_SHOT_A` (la aceptación debe ratificar SD-1..SD-4). Detalle canónico en §D5-M1A Topstep Spec Freeze.
- **D5.3 GOD FINDINGS CORRECTION — 2026-09-24.** G53-01..04 cerrados por contrato (estado suficiente multisesión con historia continua; presupuesto global de error por observable; censura de muestra separada de incertidumbre poblacional; `I_act=1{activación completada}` con débito `I_act·activation_fee`) y G53-05..10 incorporadas; matriz S01–S18 reconciliada (4 CORRECTED, 4 EXTENDED, 10 UNCHANGED) + fixtures obligatorios S19–S26. Verificado contra GOD review: kernel, flujos, `(e,m)`, `u_m(m,m)=0`, S10 y martingala finite-horizon sin cambios. Sin código, sin SPEC, sin Tier-2, sin cambio de clase de modelo. `D5_SESSION_MODEL_CORRECTIONS = REVIEW`; siguiente acción `MANAGER_ACCEPT_SESSION_MODEL`. Detalle canónico en §D5.3 GOD Findings Correction.
- **D5.3 SESSION MODEL REVIEW — 2026-09-24.** Diseño entregado en §D5.3 Session Model Review: Brownian sin drift con reloj de varianza y kernel conjunto de primer evento/supervivencia a horizonte finito; running maximum para TPT PRO. `WithdrawalPolicy` y `PricingSnapshot` separados de reglas. TPT = `ECONOMICS_ONLY` para el target automatizado. GOD review devolvió `MATH_REVISE` (ver §GOD Mathematical Review); su incorporación es la sección D5.3 GOD Findings Correction, que prevalece donde las corrige. No hay código, nuevas SPECs ni aceptación del owner. Esta sección D5.3 prevalece sobre drafts anteriores en los seis puntos del mandato; ver bloqueos precisos al final.

- **D5.1 CLOSED / D5_RULE_UNIVERSE_PASS ACCEPTED por owner.** Tiering congelado: Tier-1 = Topstep + Take Profit Trader; Tier-2 = Apex Trader Funding + MyFundedFutures + Tradeify.
- D4 cerrado con `G4C accepted` sobre simulator v0 `d4f42a41946f12231b75e4eb65b90d132731be0d`.
- KPI primario: `q_withdraw = P(evaluation comprada → primer retiro real recibido)`.
- Pass/funded son estados diagnósticos, no éxito final.
- Tier-1 congelado por owner: **Topstep** y **Take Profit Trader**. Estas dos props definen el primer vertical slice funcional D5.
- Tier-2 congelado por owner: **Apex Trader Funding**, **MyFundedFutures** y **Tradeify**. Se investigan/modelan después de certificar Tier-1, salvo conflicto que afecte el contract común.
- Productos concretos: Topstep 50K Trading Combine Standard Path → XFA Standard; Take Profit Trader 50K Test → PRO; Tier-2 mantiene provisionalmente Apex 50K EOD→EOD PA, MFFU 50K Builder Default y Tradeify 50K Growth.
- FTMO Futures: KEEP_WATCHLIST. Producto lanzado oficialmente el 2026-09-17; Growth/Pro 50K ya tienen reglas y payout lifecycle públicos, pero sólo llevan 7 días en mercado al corte D5 y no reemplazan todavía una Tier-1 madura.
- Lucid/Alpha Futures/TradeDay/etc.: fuera del primer corte salvo evidencia que justifique reemplazar una Tier-1.
- No existe todavía evidencia de `q_withdraw` real para ninguna prop. El `q=10%` de D4 es fixture matemático, no benchmark.
- **D5.2A/D5.2B capturadas 2026-09-24 (REVIEW).** Paquetes oficiales reutilizados. En D5.3 el mandato owner resuelve TS-1 a cap $2,000 y TPT-1 a 60 trading days; TS-3 y TPT-2 ya estaban resueltos. TS-2 queda histórico fuera del scope sin recovery. Contrato y gap matrix anteriores son drafts parcialmente superseded por §D5.3 Session Model Review; allí están los bloqueos vigentes. Sin código; D4 intacto; Tier-2 no investigado.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo-futures | master / feature/d5-m1a-topstep (por crear) | `d4f42a41946f12231b75e4eb65b90d132731be0d` | [[D5-M1A — Topstep Functional SPEC]] (REVIEW) | [[D5-M1A — Topstep Technical SPEC]] (REVIEW) | M1A SPEC FREEZE a aceptación owner; implementación no autorizada |

## ✅ Tareas

> - [x] D5.1 validar universo y tiering; congelar paths concretos #owner/agent #type/research #area/echo
> - [x] D5.2A extraer rules oficiales Topstep 50K hasta cash withdrawal (REVIEW a aceptación owner) #owner/agent #type/research #area/echo
> - [x] D5.2B extraer rules oficiales TPT 50K hasta cash withdrawal (REVIEW a aceptación owner) #owner/agent #type/research #area/echo
> - [ ] D5.2C capturar Tier-2 Apex/MFFU/Tradeify después del Tier-1 vertical slice #owner/agent #type/research #area/echo
> - [ ] D5.2 extraer rules oficiales versionadas hasta cash withdrawal #owner/agent #type/research #area/echo
> - [r] D5.3 diseñar session-aware null model, contratos de retiro/precios y clasificación TPT; diseño persistido, gate REVIEW a revisión matemática y aceptación owner #owner/agent #type/research #area/echo
> - [x] D5-M1A congelar SPEC funcional+técnica Topstep fast track (kernel 1D, lifecycle, matriz, fixtures, Shot A/B/C); `D5_TOPSTEP_SPEC_PASS=REVIEW` a aceptación owner #owner/agent #type/research #area/echo
> - [ ] D5-M1A Shot A/B/C implementación→verificación adversarial→certificación sobre SPEC freeze aceptado #owner/agent #type/dev #area/echo #blocked
> - [ ] D5.4 definir experiments null + conditional-edge + recovery sobre cada ruleset #owner/agent #type/research #area/echo
> - [ ] D5.5 congelar SPEC técnica mínima de adapters/rules simulator #owner/agent #type/dev #area/echo
> - [ ] D5.6 implementar/ejecutar simulaciones sólo después de SPEC freeze #owner/agent #type/dev #area/echo #blocked
> - [ ] D5.7 emitir comparación factual por `q_withdraw`, attempts/withdrawal, cash burn y EV #owner/agent #type/research #area/echo #blocked

## 📆 Bitácora

- **2026-09-24 — Shot B P150 (auditoría adversarial independiente ejecutada, sin código).** Target congelado: HEAD local `1dc1fa6afaaabe99ac8648f8c11e293fa9acd17c` de `feature/d5-m1a-p150` (árbol limpio; verificación completa contra export read-only `git archive` en /tmp, sin tocar el repo; precondition de publicación remota FALLIDA — el clone no tiene ningún remote, hallazgo B-01 MAJOR de proceso). Verificador independiente construido desde el texto de policy congelada (cadena absorbente propia en retícula $50 con Gauss–Seidel + backward induction de horizonte finito + MC propio, sin código del producto): coincide EXACTO con `ComputeDP` del producto en todas las celdas auditadas (probabilidades de payout/burn por etapa, E[sessions], E[pre-balance|pay] a 8+ decimales) y las 3 fronteras (p→0: −$49; p→1: path 4600/5200/5800, 17 sesiones, +$5112). D4 no-regresión probada físicamente: gate 47/47 @1e6 en cgroup y byte-equality de binarios old(d4f42a4)-vs-new en `simulate` 200k y `cohort` 50k exactos; histograma acotado @2e6; race verde. Reloj de portfolio exacto (payouts @7/12/17; STOP ocupa slot; pay4 requiere 22 > 20 sesiones); correlación PERFECT_COPY lockstep verificada evento-a-evento con fixture determinista de 2 cuentas; ledger exacto en cents; caps fail-closed y SIGINT limpio verificados. Samples congelados reproducen los 4 claims económicos (1 ULP de diff en dp_reference = B-02 MINOR). Veredicto **AUDIT_FINDINGS** (forzado por B-01; cero BLOCKER de código); `D5_TOPSTEP_POLICY_AUDIT_B = REVIEW` no aceptado; Shot C no ejecutado. Next `PUBLISH_AND_VERIFY_REMOTE_SHA` → `MANAGER_REVIEW_FOR_SHOT_C`; detalle y disposición en §Shot B.
- **2026-09-24 — Shot C P150 (publish/freeze + experimento completo + certificación).** PHASE 0: repo autoridad creado (`gh repo create xKoRx/echo-futures --private`), push de master + feature/d5-m1a-p150 sin mutación, remote SHA == `1dc1fa6a…` (B-01 CLOSED; freeze). PHASE 1: corrección B-03 (`6f7ae58`, .gitignore + regresión trivial), certificación pre-experimento en cgroup (go test, race, D4 validate 47/47 @1e6, p150-verify 23/23, coverage 96.0%, determinismo byte-idéntico same-build), regeneración B-02 de los 4 samples (`cdef2b6`, diffs 1-ULP sólo en dp_reference), push y verificación remota. Protocolo congelado antes de ejecutar (sample sizes 100k/celda, seeds 424242/424243, reglas de confianza 5σ, sweep y contorno declarados). Ejecución: 2 matrices congeladas NDJSON + 240 per-cell outputs completos + sweep K3/K4 40 sesiones + bisección DP exacta (verificador fuera del repo; export `git archive`). Crosscheck matriz↔per-cell byte-idéntico. Desviación registrada: dominio max_payouts∈{3,4} impide MC de STOP_AFTER_1/2 → marginales por atribución + DP (ver §Shot C). `D5_TOPSTEP_POLICY_RESULT_C = REVIEW`.
- **2026-09-24 — INCIDENTES OOM #1/#2 (recovery + causa física) + SIMULATION RESOURCE SAFETY CONTRACT + Shot A P150 entregado.** Cadena completa: (a) forense de kernel (syslog dumps 17:44–19:43, 12 OOMs globales) probó que el ofensor físico era un **swarm externo de procesos node/vite/esbuild del front Echo v3** (`d3-shot3-correction-20260924/echo/v3/front`, hasta 9,141 procesos "MainThread", ~70 GiB anon + 3.3 GiB page tables) que tumbo daedalus dos veces (reboots ~19:45 y 20:27); (b) tercer episodio capturado EN VIVO y contenido (SIGTERM a workers esbuild huérfanos + el `vite build` activo murió: 45→3.9 GiB usados); (c) echo-futures quedo EXONERADO por tabla de tareas del kernel (top Go family 478 MB) pero con UN vector acotado propio corregido: cohort retenía 3 slices O(N) (~24 B/cohort medidos; 5e9 cohorts ≈ 120 GB) — reemplazado por QuantileStore bounded (exacto ≤1e6, histograma arriba; resultados idénticos en toda escala certificada, orden RNG intacto); (d) contrato durable: `internal/resources` (Budget/Plan/Guard/RunBatched/WorkerBudget/QuantileStore) + wrappers `scripts/safe-run|safe-test|safe-sim|safe-validate` (systemd user cgroup MemoryHigh=4G/MemoryMax=6G/SwapMax=1G/TasksMax=128/CPU=400%/GOMEMLIMIT=3GiB/GOMAXPROCS=4, autoverificado dentro del scope, fail-closed sin fallback) + tests de regresión de crecimiento acotado; (e) micro-certificación en cgroup: N→2N→4N→8N acotado, escenarios 1/2/4/8 flat ~8 MB, leak test 10×cohort 1e6 sin crecimiento (72–86 MB), trade-only flat 4 MB hasta 1e7 runs, race verde 103 MB pico; `D5_RESOURCE_SAFETY_PASS = PASS`; (f) Shot A P150 COMPLETADO bajo el contrato: `internal/p150` con los 14 fixtures del dispatch (23 checks) PASS, DP exacto ≡ MC dentro de 5σ, coverage 96.0%, matriz NDJSON con break-even, samples reales con hallazgo económico visible (p=0.55/ql=2000: net −$2,824/mes P(>0)=5.5%; p=0.60/ql=150: +$6,486 P(>0)=97.9% — el break-even está entre ambos; PERFECT_COPY muestra cola superior correlacionada P95 +$5,890 vs +$88 independiente). Commits `321335f` (resource safety), `1103002` (Shot A), `1dc1fa6` (gofmt) en `feature/d5-m1a-p150` sobre `d4f42a4`. `D5_TOPSTEP_POLICY_IMPL_A = REVIEW`; sin matriz completa (Shot C), sin Shot B. Next `MANAGER_REVIEW_IMPL_A` (+ acción owner externa: contener el respawn vite/esbuild del front v3 con su propio cgroup).

- **2026-09-24 — D5-M1A Topstep spec freeze (SPEC_FREEZE ejecutado, sin código).** Bootstrap Agents-OS + router aranea + contrato de ambientes; autoridades leídas completas (§D5.2A, §D5.3 con GOD review y correcciones C1–C6, aceptación Manager con override Topstep-first, SPECs D4, math review) y baseline certificado verificado físicamente: checkout local en `d4f42a41946f12231b75e4eb65b90d132731be0d`, tree limpio, master. Creadas [[D5-M1A — Topstep Functional SPEC]] y [[D5-M1A — Topstep Technical SPEC]]: lifecycle completo con BURNED/INCOMPLETE, structural null (drift 0, delta 0, execution cost 0, cash personal activo), semántica Combine (sesión 17:00→15:10 CT, ratchet EOD + lock, consistencia 55% con igualdad dura, renovación FIXED_30D con tie SD-3) y XFA (I_act, reset a 0, MLL −2000→lock 0, winning days 5×150 con publicación 16:00, MAX_ELIGIBLE floor_cent(min(0.5·B,2000))≥125, 90/10 Aeropay, MLL→0 tras primer payout), TradePolicy de referencia SD-1 (G=L=100, h0=1, escaleras prefijo de {−30,−50,−70,−90}), kernel 1D verbatim del GOD con muestreo de ley conjunta, representación dual imágenes/espectral sin Euler de producción, estado suficiente C1 (A jamás omitido), presupuesto de error C2 (7 componentes + etiquetas), S14 adaptado a identidad general de snapshots, matriz 6×5=30 puntos delta=0, aceptancia T1–T8 intactos + S01–S08/S11–S12/S14–S20/S22/S25–S26 (S07/S13/S17/S09/S10/S21/S23/S24 DEFERRED explícitos a M1B) + TS-F01..TS-F16, paquetes Shot A (implementación), B (verificación adversarial contra commit exacto, sin arreglar código) y C (corrección+certificación) listos sin ejecutar. Cambios al vault: 2 SPECs nuevas + este planner; change_log en journal. `D5_TOPSTEP_SPEC_PASS = REVIEW`; no se acepta el gate; sin implementación. Next action `MANAGER_ACCEPT_AND_DISPATCH_SHOT_A`.
- **2026-09-24 — D5.3 GOD findings correction (CORRECT_AND_REVIEW ejecutado).** Mandato de corrección de contrato: incorporar fielmente los findings aceptados del GOD review sin cambiar la clase de modelo. C1: separación estado local de difusión / estado suficiente económico-de-política multisesión con dimensión continua de historia (fixture negativa `[1700,700,600]` vs `[1400,900,700]`). C2: presupuesto global de error con ε_kernel/ε_history/ε_composition/ε_truncation/ε_horizon/ε_oracle/ε_MC, inequality `(sup g − inf g)·TV(P,Q)`, acumulación Σδ_i sin cancelación y etiquetas RIGOROUS_BOUND/EMPIRICAL_CONVERGENCE/MONTE_CARLO_UNCERTAINTY. C3: `qhat_final_sample∈[S/N,(S+U)/N]` como cota muestral, envolvente η=sqrt(log(2/α)/(2N)) como contrato conservador no exclusivo, masas exactas de solver como caso determinista propio. C4: `I_act=1{activación completada}`, débito `I_act·activation_fee`, identidad de pricing `68(1+n)+130·I_act`. C5: G53-05..10 incorporadas (empates geométricos deterministas, masa singular `δ_{m0}`, τ_D vs ζ, martingala finite-horizon, predicados estrictos sin epsilon, ν como perfil/vector). C6: S01–S18 reconciliados (4 CORRECTED: S10/S12/S14/S18; 4 EXTENDED: S01–S03/S09; 10 UNCHANGED) + S19–S26. /verify 10/10 contra GOD review: ninguna fórmula aceptada alterada. `D5_SESSION_MODEL_CORRECTIONS = REVIEW`, sin segundo GOD shot requerido por regla del manager; next action `MANAGER_ACCEPT_SESSION_MODEL`. Sin código, SPEC, simulación ni Tier-2; change_log consolidado en este planner por alcance expreso.

- **2026-09-24 — D5.3 diseño, change_log consolidado en el planner.** Seleccionado kernel Brownian conjunto con horizonte finito y máximo para PRO; definidas actualizaciones EOD, consistencia estricta TPT, winning days, políticas de retiro, tres snapshots de precios y pruebas analíticas/oráculo independiente. TS-1 resuelto a $2,000 y TPT-1 a 60 trading days por mandato owner. TPT permanece Tier-1 económica, sin permiso de automatización. Verificaciones documentales y fuentes oficiales focalizadas; no se ejecutó simulación ni se reabrió D4. Por instrucción expresa de editar sólo este archivo, no se modifica tarea puente, memoria, journal externo ni Agents-OS core; la continuidad queda aquí. `D5_SESSION_MODEL_PASS = REVIEW`, `Next action = MATH_REVIEW`.

- **2026-09-24 — D5-M1 Tier-1 rule capture (RESEARCH + CONTRACT DISCOVERY).** Bootstrap Agents-OS + autoridades (planner D5, SPECs D4, matemática MATH_GO, proyecto padre, contrato de ambientes) cargados; ninguna operación de infraestructura. Captura por dos agentes de research con contrato de evidencia (sólo fuentes oficiales topstep.com/help.topstep.com y takeprofittrader.com/try.takeprofittrader.com/zendesk oficial; secundarias sólo SECONDARY_FLAG) + verificación adversarial del manager con re-fetch verbatim de las 6 páginas load-bearing Topstep y 5 páginas load-bearing TPT (WebFetch 403 en Zendesk ⇒ reader MCP; el artículo de suscripciones TPT 15141145057053 no re-fetchable en sesión ⇒ cita del agente + doble corroboración cruzada). Resultado: paquetes D5.2A/D5.2B completos, economics ledger por prop (account balance ≠ personal cash), registro RULE_CONFLICT (TS-1, TS-2, TS-3 resuelto, TPT-1, TPT-2 resuelto), unknowns consolidados (8 Topstep + 9 TPT), contrato normalizado candidato `PropRuleSet` y gap matrix de simulator con 4 SUPPORTED, 7 SMALL_EXTENSION, 7 MATERIAL_EXTENSION, 8 DEFER. Hallazgo material para D5: ambos drawdowns Tier-1 son trailing (EOD Topstep/TPT-Test, intraday TPT-PRO) ⇒ la barrera estática de D4 sobreestimaría p_pass bajo null ⇒ MATERIAL_EXTENSION de capa de sesiones. Gate `D5_TIER1_RULES_CAPTURED` → REVIEW. Sin código; D4 intocado; Tier-2 no investigado.
- **2026-09-24 — Owner freeze D5.1.** Owner redefine tiers: Tier-1 = Topstep + Take Profit Trader; Tier-2 = Apex + MyFundedFutures + Tradeify. `D5_RULE_UNIVERSE_PASS` aceptado. Estrategia de entrega cambia a Tier-1-first: primer hito funcional = reglas reales Topstep/TPT + lifecycle purchase→WITHDRAWAL_RECEIVED + null-model economics reproducible; Tier-2 no bloquea este hito.
- **2026-09-24 — D5.1 manager start.** Bootstrap y skill `technical-project-manager` cargados; D4 confirmado documentalmente CLOSED/G4C accepted @ `d4f42a41946f12231b75e4eb65b90d132731be0d`. Checkout local reportado en D4 no está montado en esta sesión, por lo que no se reejecutó Git/tests físicos; no existe contradicción material y el baseline certificado se conserva. Web oficial actual valida las cinco Tier-1 propuestas. Freeze propuesto: Topstep 50K Trading Combine Standard→XFA Standard; Apex 50K EOD→EOD PA; MFFU 50K Builder Default; Tradeify 50K Growth→Growth Sim Funded; TPT 50K Test→PRO. FTMO Futures KEEP_WATCHLIST por lanzamiento 2026-09-17. D5.1 queda en REVIEW a aceptación del owner.
- **2026-09-24** — D5 creado tras cierre/certificación de D4. Scope corregido: success = primer retiro real, no funded. Primer corte Tier-1 = Topstep, Apex, MyFundedFutures, Tradeify y Take Profit Trader; FTMO Futures watchlist por lanzamiento reciente.

## 🧭 Decisiones

- `q_withdraw` es el KPI principal.
- No asumir 10%, 20% ni ninguna tasa de retiro.
- No usar pass/funded como proxy de éxito.
- Reglas deben venir de fuentes oficiales y quedar date/version stamped.
- El manager no implementa antes de congelar un contract común y resolver ambigüedades materiales.
- No reabrir D4 salvo contradicción reproducible.
- Para D5.1 se prefieren paths de ~50K con lifecycle único hasta primer payout; variantes con bifurcaciones materiales se difieren salvo necesidad.
- Topstep: modelar purchase path Standard ($49/mes + $149 activation al aprobar) y XFA payout path Standard; la variante No Activation Fee queda sensitivity posterior, no segundo producto base.
- Apex: EOD 50K, no Intraday Trailing, para mantener una barrera EOD representable y comparable.
- MFFU: Builder 50K Default, no Add-On, para evitar duplicar MLL variants.
- Tradeify: Growth 50K, no Select, porque Growth tiene funded payout path fijo; Select introduce elección Flex/Daily después del pass.
- TPT: Test 50K → PRO; PRO+ live es transición posterior y no requisito para first withdrawal.
- FTMO Futures no entra al Tier-1 D5 inicial hasta tener más madurez del producto futures.
- **Tiering owner 2026-09-24:** Tier-1 = Topstep + Take Profit Trader. Tier-2 = Apex Trader Funding + MyFundedFutures + Tradeify.
- **Delivery strategy:** certificar primero un vertical slice Tier-1 completo; Tier-2 se monta sobre el contract/engine certificado sin ampliar arquitectura por adelantado.
- **Primer hito funcional D5-M1:** Topstep 50K y TPT 50K deben poder simular `PURCHASE_EVALUATION → ... → WITHDRAWAL_RECEIVED | BURNED` bajo null model, con reglas reales versionadas y outputs económicos obligatorios.

## 🔗 Docs / Links

- [[Echo Futures]]
- [[Echo Futures — Simulator v0]]
- [[D4 — Simulator v0 Functional SPEC]]
- [[D4 — Simulator v0 Technical SPEC]]
- [[D5-M1A — Topstep Functional SPEC]]
- [[D5-M1A — Topstep Technical SPEC]]
- [[echo-futures-astra-math-review]]


## D5.1 — Universe freeze package (ACCEPTED)

Captured at: 2026-09-24.

| Provider | Concrete path | Why this path | Official evidence for D5.1 |
|---|---|---|---|
| Topstep | 50K Trading Combine — Standard purchase path → XFA Standard payout path | canonical 50K; purchase economics explicit; funded path explicit | https://help.topstep.com/en/articles/14289835-topstep-pricing-and-payment-questions · https://help.topstep.com/en/articles/8284197-trading-combine-parameters · https://help.topstep.com/en/articles/8284215-express-funded-account-parameters · https://help.topstep.com/en/articles/8284233-topstep-payout-policy |
| Apex Trader Funding | 50K EOD Evaluation → 50K EOD Performance Account | exact 50K EOD lifecycle; avoids intraday-trailing variant | https://apextraderfunding.com/help-center/eod-trailing-drawdown-accounts/eod-evaluations/ · https://apextraderfunding.com/help-center/eod-trailing-drawdown-accounts/eod-performance-accounts-pa/ |
| MyFundedFutures | 50K Builder — Default MLL → Sim Funded | one fixed plan; no activation fee; explicit first-payout buffer and 80/20 split | https://help.myfundedfutures.com/en/articles/14290805-builder-plan-50k-a-comprehensive-guide |
| Tradeify | 50K Growth Evaluation → Growth Sim Funded | fixed payout policy; avoids Select Flex/Daily branch | https://help.tradeify.co/en/articles/10495915-growth-evaluation-accounts · https://help.tradeify.co/en/articles/11083796-growth-funded-account-payout-policy · https://help.tradeify.co/en/articles/10495917-how-do-i-get-funded-after-passing-an-evaluation |
| Take Profit Trader | 50K Test → PRO | direct simulated-funded stage with day-one payout; PRO+ not needed for first withdrawal | https://takeprofittrader.com/ · https://try.takeprofittrader.com/TPT-FAQs-nf40-4-0725 |
| FTMO Futures | WATCHLIST: Growth/Pro 50K | launched 2026-09-17; rules exist but product is only 7 days old at capture | https://ftmo.com/en/press-release/ftmo-launches-ftmo-futures/ · https://ftmo.com/en/futures/comparison-table/ |

### Research dispatches for D5.2

These are rule-capture research one-shots, not the later three implementation shots.

Common output contract for every provider: exact product/path; every material rule from purchase through WITHDRAWAL_RECEIVED; official URL; captured_at=2026-09-24; phase; raw wording summary; normalized field candidate; confidence; RULE_CONFLICT entries; missing facts; simulator relevance. Secondary sources may only discover contradictions and never establish a rule.

1. **Topstep 50K** — extract only Trading Combine Standard purchase path + XFA Standard payout path. Include recurring fee/reset, activation, MLL/DLL/consistency/max contracts, funded scaling, winning-day eligibility, payout cap/split, post-withdrawal balance effects and copy/account limits. Do not research Consistency XFA or No Activation Fee except to record why excluded.
2. **Apex 50K EOD** — extract only EOD Evaluation→EOD PA. Include current evaluation purchase/renewal/reset economics, 30-day access/activation deadline, EOD threshold/DLL, PA activation cost, tier scaling/DLL, payout eligibility/caps/split, inactivity and account/copy restrictions. Do not research Intraday Trailing.
3. **MFFU 50K Builder Default** — extract only Builder Default. Include current non-promotional list price and renewal/reset behavior, no activation fee, EOD MLL/DLL, Sim Funded buffer, 50% payout consistency, qualifying days, first payout amount/cap, 80/20 split, inactivity and post-payout MLL behavior. Do not model Add-On.
4. **Tradeify 50K Growth** — extract only Growth Evaluation→Growth Sim Funded. Include current price/reset economics, EOD trailing/DLL, minimum days, activation fee, funded drawdown, payout minimum/balance threshold, first payout cap, payout split, payout cadence, inactivity/copy/account limits. Do not research Select except conflicts that affect Growth terminology.
5. **TPT 50K Test→PRO** — extract only 50K Test→PRO. Include current subscription/reset and PRO activation/tech fee if any, 3-day/consistency/EOD evaluation rules, PRO intraday drawdown/buffer/news restrictions, 80/20 split, day-one/daily payout semantics, inside-buffer withdrawal closure/50% split, processing path to actual cash, copy/account limits. PRO+ only as continuation_state after first payout, not success condition.

### Gate control

| Gate | State | Acceptance |
|---|---|---|
| D5_RULE_UNIVERSE_PASS | **ACCEPTED** | Owner froze Tier-1=Topstep/TPT and Tier-2=Apex/MFFU/Tradeify |
| D5_TIER1_RULES_CAPTURED | **REVIEW** | Complete official Topstep + TPT rule packets through actual cash receipt (paquetes D5.2A/D5.2B + conflictos + unknowns en este planner, captured_at 2026-09-24) |
| D5_SESSION_MODEL_CORRECTIONS | **REVIEW** | G53-01..04 cerrados por contrato y G53-05..10 incorporadas sin cambio de clase de modelo; revisión directa contra §GOD Mathematical Review en §D5.3 GOD Findings Correction |
| D5_TOPSTEP_SPEC_PASS | **REVIEW** | SPEC funcional+técnica M1A congeladas (kernel 1D, lifecycle Topstep, matriz 6ν×5adds, S-subset + TS-F01..16, Shot A/B/C preparados); aceptación owner ratifica SD-1..SD-4 y habilita Shot A |
| D5_RESOURCE_SAFETY_PASS | **PASS** | Contrato externo (cgroup systemd fail-closed) + interno (budgets/guards/bounded quantiles) certificados in-cgroup; regresiones de crecimiento acotado en suite |
| D5_TOPSTEP_POLICY_IMPL_A | **REVIEW** | Shot A P150 implementado y verificado (14 fixtures/23 checks PASS, DP≡MC 5σ, coverage 96.0%); a revisión manager; sin matriz completa ni Shot B |
| D5_TOPSTEP_POLICY_RESULT_C | **REVIEW** | Shot C ejecutado: B-01 CLOSED (remoto xKoRx/echo-futures @ `cdef2b6` verificado; chain 1dc1fa6a→6f7ae58→cdef2b6), B-02/B-03 absorbidos, matrices congeladas completas + break-even DP/MC + sweep de horizonte; certificación completa verde (D4 47/47, P150 23/23, race, cov 96.0%, determinismo); detalle en §Shot C |
| D5_TOPSTEP_POLICY_AUDIT_B | **REVIEW** | Shot B auditoría adversarial independiente sobre HEAD local congelado `1dc1fa6afaaabe99ac8648f8c11e293fa9acd17c`: veredicto AUDIT_FINDINGS — sin BLOCKER de código; B-01 MAJOR de proceso (rama sin publicar en remoto, precondition PUBLISH_AND_FREEZE_SHOT_A_HEAD incumplida); A1–A11 PASS (D4 47/47, cohort/simulate byte-idénticos, DP independiente ≡ producto, MC en 5σ, reloj portfolio, correlación, ledger, resource safety); detalle en §Shot B |
| D5_TIER1_RULE_CONTRACT_PASS | BLOCKED | Normalize only Tier-1 first, preserving prop-specific exceptions |
| D5_TIER1_SIM_GAP_PASS | BLOCKED | Classify every Tier-1 rule as SUPPORTED/SMALL_EXTENSION/MATERIAL_EXTENSION/DEFER |
| D5_TIER1_SPEC_PASS | BLOCKED | Freeze minimum functional+technical extension for Tier-1 lifecycle |
| D5_TIER1_IMPL_PASS | BLOCKED | Three-shot implementation/audit/correction on exact certified baseline |
| D5_TIER1_ECON_PASS | BLOCKED | Null-model Monte Carlo produces required q_withdraw/cash/burn/tail metrics |
| D5_TIER2_EXPANSION | BLOCKED | Only after Tier-1 engine/spec is certified |


## D5.2A — Topstep 50K Standard rule packet (captured_at 2026-09-24)

Producto congelado: **50K Trading Combine — Standard purchase path** ($49/mes + $149 activación) → **50K Express Funded Account (XFA) — Standard payout path**. Variantes excluidas y NO investigadas como producto: No Activation Fee, Consistency XFA, DLL add-on en checkout (offer que dobla caps — registrada sólo como ambigüedad, sensibilidad posterior). Fuentes oficiales: `help.topstep.com` + `topstep.com`. Confianza: HIGH = declaración oficial explícita; MISSING = no encontrado en páginas oficiales.

### Fase 1 — Trading Combine 50K (Standard)

| campo | valor normalizado | evidencia oficial (cita) | fuente | conf |
|---|---|---|---|---|
| purchase_cost | 49 USD por ciclo de 30 días (base; impuestos aparte) | "Standard Path: '$49/month'" · "Listed prices are base costs only." | help.topstep.com/en/articles/14289835 | HIGH (status list-vs-promo = unknown) |
| recurring | 49 USD cada 30 días, auto-renew; cancel manual irreversible (sin resubscribe); pago fallido: 2 reintentos y baja; resets deshabilitados durante retry | "It Rebills every 30 days from your original sign-up date." · "attempt to process the charge two more times before the subscription is canceled." | help.topstep.com/en/articles/8284121 | HIGH |
| reset_cost | 49 USD; reset total (balance, MLL, consistency, días → day one); empuja rebill +30d; máx 2/día; 1 Reset Credit gratis por rebill (emitidos ≥2025-12-11 expiran en 1 año) | "A Reset returns your Trading Combine® to its original starting balance" · "Limit: 2 Resets per account each day." · "Resetting your account pushes your Rebill date out 30 days" | help.topstep.com/en/articles/8284128 · /10370307 · /14289835 | HIGH |
| expiration | sin límite de tiempo para pasar; activo hasta pasar o cancelar | "Active until you pass and earn an Express Funded Account® (XFA) — or until you cancel. No time limit for passing." | help.topstep.com/en/articles/8284121 | HIGH |
| inactivity | MISSING para Combine (sólo XFA tiene cláusula 30 días) | — | — | MISSING |
| profit_target | 3,000 USD (tabla oficial del artículo de consistency) | "$3,000 Profit Target" · "$50K → <$1,650" (ejemplo 55%) | help.topstep.com/en/articles/8284208 | HIGH |
| MLL | 2,000 USD; trailing sobre balance END-OF-DAY, nunca baja; monitoreado en tiempo real intradía; lock permanente en balance inicial (50,000); base = Net P&L realizado+no realizado; breach → liquidación resto del día + inelegible para funding hasta Reset (la suscripción sigue corriendo) | "It rises as your end-of-day balance grows, but never moves down." · "Once it reaches your starting balance, it locks permanently." · "monitored in real time throughout the session" · "liquidated for the rest of the trading day and becomes ineligible for funding until you Reset." | help.topstep.com/en/articles/8284204 | HIGH |
| daily_loss | none por defecto; add-on opcional 1,000 USD (50K) fijado en checkout; trigger = flatten hasta próxima sesión 5PM CT, NO es violación | "The Daily Loss Limit (DLL) is optional" · "$50K Account: $1,000" · "it's a forced break for the rest of that session." | help.topstep.com/en/articles/10490293 | HIGH |
| consistency | 55% Consistency Target: mejor día ≤ 55% del Profit Target; línea dura sin redondeo; si se excede el target sube dinámicamente a Best Day ÷ 0.55 (corregir sólo con ganancia de días posteriores) | "Your single best day of profit must stay at or below 55% of your Profit Target." · "55% is a hard line." · "new target = 'Best Day ÷ 0.55'" | help.topstep.com/en/articles/8284208 | HIGH |
| minimum_days | 2 días de trading; día de trading = 5:00 PM CT → 3:10 PM CT del día calendario siguiente | "You can pass in as few as 2 days." · "The trading day runs from 5:00 PM CT through 3:10 PM CT the next calendar day." | help.topstep.com/en/articles/8284208 · /8284197 | HIGH (si el día requiere ≥1 trade: implícito) |
| max_position | 5 minis / 50 micros; micros:minis 10:1; sólo futuros de lista permitida (sin forex/spot) | "$50K | 5 | 50" · "Micros and minis count at a 10:1 ratio." | help.topstep.com/en/articles/8284197 · /8284206 | HIGH |
| scaling_evaluación | none (límites flat; el Scaling Plan es objetivo de XFA) | ver /8284223 y límites flat en /8284197 | help.topstep.com/en/articles/8284223 | HIGH |
| sesión/overnight | cierre obligatorio 3:10 PM CT días hábiles; reanuda 5:00 PM CT; sin overnight ni fin de semana; feriados: cerrar 15 min antes del early close, si no auto-liquidación | "All positions must be closed by 3:10 PM CT every weekday." · "Topstep does not permit holding positions from one session to the next." | help.topstep.com/en/articles/8284206 · /13350348 | HIGH |
| news | sin flatten obligatorio; full-size contra news programada = estrategia prohibida; trades afectados por releases sin excepciones ni Reset credits | "Topstep doesn't require you to flatten positions during economic releases" · "Purposefully trading your full Maximum Position Size directly into a scheduled major news event" (prohibido) | help.topstep.com/en/articles/8284211 · /10305426 | HIGH |
| conducta_prohibida | spoofing; off-market; posiciones opuestas entre cuentas propias; trading coordinado/copiado que pooling riesgo; ventaja técnica/AI/HFT; account stacking multi-perfil; VPN/proxy/geo-evasión; posición a <2% del price limit; trading para terceros; disputas de pago; abuso de SIM | "holding opposite positions across multiple accounts simultaneously" · "using software, AI, ultra-high speed systems... to gain an unfair advantage" · "VPNs, proxy services, TOR... are not permitted." | help.topstep.com/en/articles/10296582 · /10305426 | HIGH |
| account_limits | Combines simultáneos ilimitados bajo un perfil; Practice 150K gratis (1) con suscripción activa | "There's no limit to the number of Trading Combines you can have" | help.topstep.com/en/articles/8284197 · /8284134 | HIGH |
| failure_rules[] | MLL breach → liquidación + inelegible hasta Reset; conducta prohibida → warning/delección de día/reset/cierre/denial de payout; consistencia no falla la cuenta (sólo bloquea pass hasta corregir); DLL no es violación; refund 28 días sólo compra nueva sin actividad | ver filas MLL/DLL/consistency | /8284204 · /10490293 · /8284208 · /8284197 | HIGH |

### Pass / Activation

| campo | valor normalizado | evidencia oficial | fuente | conf |
|---|---|---|---|---|
| pass_transition | target + ≥2 días de trading + best day ≤55%; estado refleja ≤30 min; el Combine CIERRA y su suscripción auto-cancela; ganancias NO se transfieren; activación desde el Trade Report (elección de tipo/size de XFA, locked después) | "The subscription tied to the passed Trading Combine will auto-cancel, and the account will close." · "you activate your Express Funded Account® (XFA) directly from your Trade Report." | help.topstep.com/en/articles/8284208 · /8284197 · /8284217 | HIGH |
| activation_deadline | MISSING — sin plazo documentado | — | /8284217 | MISSING |
| activation_cost | 149 USD one-time por XFA ganado (Standard path); no reembolsable; XFA sin mensualidad | "Standard Path — $149, charged once per XFA earned." · "No refunds on Activation Fee purchases" | /14289835 · /8284217 · /8284117 | HIGH |
| failed_activation | estado de pérdida sin refund; recuperación paga: Back2Funded 599 USD (≤2 reactivaciones por XFA, 30 días calendario desde cierre, sólo cierre por violación PRE-primer-payout; tras Back2Funded todo resetea a cero) o nuevo Combine | "$50K XFA — $599" · "Up to 2 Reactivations per Express Funded Account." · "Once a Payout is taken from an XFA, it is no longer eligible for Back2Funded." | /12060405 · /8284117 · /14289835 | HIGH (ventana: ver RULE_CONFLICT TS-2) |

### Fase 2 — XFA 50K Standard (payout path Standard)

| campo | valor normalizado | evidencia oficial | fuente | conf |
|---|---|---|---|---|
| starting_reference | buying power 50K; BALANCE nominal inicia en 0; MLL arranca en −2,000 | "Your balance starts at $0 and grows from your trading profits." · "your MLL starts at -$2,000" | /8284215 · /8284204 | HIGH |
| MLL_funded | 2,000 USD; trailing sobre MÁXIMO balance EOD, nunca baja; lock en 0 cuando el balance alcanza 2,000 (= buffer/safety net: la cuenta no puede caer bajo 0); breach → liquidación y cierre permanente al fin del día | "Once your balance reaches $2,000, the MLL locks at $0 permanently." · "Your account is permanently closed." | /8284204 · /8284215 | HIGH |
| daily_loss_funded | add-on opcional 1,000 (si se eligió en Combine permanece de por vida de la cuenta; requerido en plataformas ≠ TopstepX); trigger = temporary violation, flatten hasta próxima sesión | "The DLL stays with the account for its full lifetime." · "A Daily Loss Limit applies to accounts on platforms other than TopstepX." | /10490293 · topstep.com/express-funded-account-rules | HIGH |
| max_position_funded | Scaling Plan por niveles de balance (ejemplo textual 50K: 2 minis / 20 micros); nunca sube intradía; >10 s en exceso = review; tabla completa de tiers es imagen (parcial) | "Follow the Scaling Plan — the max contracts you can hold at one time — based on your current account balance." · "Your max contracts do not increase mid-session." | /8284223 · /8284215 | HIGH concepto / MEDIUM tiers |
| consistency_funded | NONE en Standard (tabla Parameters: "❌"); la 40% es del path Consistency (excluido) y se resetea tras cada payout | "Consistency target: ❌" (columna Standard) | /8284215 · /8284208 | HIGH (ver TS-3) |
| winning_days | 5 winning days de ≥150 USD Net P&L; no consecutivos; el día lockea 4:00 PM CT; el día del request no cuenta para el próximo ciclo | "5 winning days of $150+ Net P&L. Days don't need to be consecutive." · "your 5-day count restarts" (tras cada payout) | /8284233 | HIGH |
| buffer_safety_net | MLL lock en 0 = piso absoluto; policy recomienda construir balance hasta MLL=0 antes del primer payout | "trails upward, locking at $0 once the balance reaches $2,000" | /8284204 · /8284233 | HIGH |
| payout_eligibility | 5 winning days $150+ + ganancia neta ≥0.01 desde el último payout (PRIMER payout exento) + compliance limpio + ventana de request Sun 5 PM – Fri 5 PM CT (feriados fuera) | "Positive net profit since your last Payout... at least $0.01... Your first Payout is exempt." · "Available during CME market hours: Sunday 5 PM CT – Friday 5 PM CT" | /8284233 | HIGH |
| payout_cap | por request: min(50% del balance, cap por tamaño); 50K Standard cap = 2,000 USD; mínimo de request 125 USD; caps completos: 50K 2,000/3,000 (Std/Consistency), 100K 3,000/4,000, 150K 5,000/6,000 | "Max Payout per request: 50% of your account balance up to the cap below." · "$50K | Standard | $2,000" · "Minimum Payout: $125" | /8284233 | HIGH (ver RULE_CONFLICT TS-1) |
| payout_split | 90/10 (trader 90%) en payouts XFA; regla legacy: 100% de los primeros 10,000 USD de profits vitalicios para dashboards pre-2026-01-12 (población MEDIUM) | "90/10 profit split — you keep 90%" · "You receive 100% of your first $10,000 in lifetime profits." (contexto legacy) | /8284233 | HIGH / MEDIUM legacy |
| payout_processing | aprobación interna 1–3 días hábiles; métodos: Aeropay (US) instantáneo fee 0; Prop-to-Brokerage (US) mismo día fee 0 si request ≤12 PM CT; Wise 1–3 días fee 0; ACH 1–3 días fee 30; Wire/SWIFT 5–10 días fee 30; no payouts en feriados | "Internal approval can take 1-3 business days" · "ACH (US): 1-3 business days, $30 fee." | /8284233 · /13350348 | HIGH |
| payout_invalidation | review de compliance/conducta/ToU; sólo bancos a nombre propio; W-9/W-8BEN obligatorio; DLL temp-violation posterga; MLL post-request NO clawback de payout aprobado; copy trading auto-disabled durante procesamiento; inelegibilidad por felony/disciplina NFA-CFTC/deuda de clearing/chargeback | "payouts only to bank accounts in your own name; tax forms (W-9/W-8BEN) required." · "Hitting MLL after a request doesn't affect an already-deducted payout." | /8284233 · topstep.com/express-funded-account-rules | HIGH |
| balance_effect | el monto se deduce del balance al aprobarse; la XFA sigue operable de inmediato | "Payout amounts are subtracted from the balance once approved." · "Funds transfer immediately on request (XFA can resume trading)" | /8284233 · topstep.com/express-funded-account-rules | HIGH |
| drawdown_effect | MLL seteado a 0 PERMANENTE tras el primer payout (queda en 0); balance restante = piso efectivo de pérdida | "Your MLL is set to $0 after your first Payout... The remaining balance becomes your effective loss floor." | /8284233 | HIGH |
| continuation_state | misma XFA sigue tradendose; conteo de 5 winning days reinicia; regla ≥0.01 aplica al próximo payout; Back2Funded perde elegibilidad tras cualquier payout | "After each Payout: ... your 5-day count restarts." | /8284233 | HIGH |
| closure_conditions | MLL breach = cierre permanente; inactividad >30 días puede cerrar (sin holds); cierre voluntario de XFA elegible paga ≤50% del Reward Balance cap 5,000 (resto se pierde); Topstep puede cerrar en cualquier momento; máx 5 XFA activos (Shoulder Tap: 1) | "XFAs with no trading activity for more than 30 days may be closed." · "up to 50% of your current Reward Balance, capped at $5,000" · "You can hold up to 5 active XFAs at a time." | /8284215 · topstep.com/express-funded-account-rules | HIGH |

### Economics ledger Topstep (PERSONAL CASH; balances = nominales simulados)

- PURCHASE: −49 USD (ciclo 1 Combine 50K Standard, +impuestos).
- SUBSCRIPTION_RENEWAL: −49 cada 30 días mientras el Combine esté activo; sigue tras MLL breach; auto-cancela al pasar.
- RESET_REBUY: −49 por reset (económicamente = nuevo attempt con F; conserva suscripción y corre rebill +30 días); Reset Credit gratis por rebill.
- ACTIVATION: −149 al activar XFA (una vez por XFA ganado).
- FUNDED_FEE: 0 (XFA sin mensualidad).
- OTHER_REQUIRED_COST: L2 DOM 38 USD/mes (opcional); comisiones por trade auto-deductadas del nominal (SCHEDULE NO CAPTURADO — unknown); Back2Funded 599 USD (condicional, ≤2×, pre-payout).
- WITHDRAWAL_RECEIVED: +0.90 × min(0.50 × balance, 2000) − fee método (0 Aeropay/Brokerage, 30 ACH/Wire); request mínimo 125. Ejemplo cap: request 2,000 → 1,800 netos (Aeropay) / 1,770 (ACH).

## D5.2B — TPT 50K Test→PRO rule packet (captured_at 2026-09-24)

Producto congelado: **50K Test** (evaluación) → **50K PRO** (sim-funded con payout day-one). PRO+ sólo como continuation_state posterior al primer retiro (no requisito de éxito). Fuentes oficiales: `takeprofittrader.com`, `try.takeprofittrader.com/TPT-FAQs-nf40-4-0725`, `takeprofittraderhelp.zendesk.com` (help desk oficial), `/terms`.

### Fase 1 — 50K Test

| campo | valor normalizado | evidencia oficial (cita) | fuente | conf |
|---|---|---|---|---|
| purchase_cost | LIST 170 USD/mes (MEDIUM — derivado de 3 promos oficiales consistentes: 40%→102, 30%→119, 50%→85); promo vigente NOFEE40 = 102 USD/mes con 40% lifetime discount y activación 130 waived de por vida | "you'd be getting a $50k account for just $102 flat" · "$119 flat" (NOFEE30) · "$85 flat" (NOFEE50) | zendesk 29660646764445 · 36337706971677 · 35985020984605 | HIGH promo / MEDIUM list |
| recurring | mensual, mismo día calendario; NO auto-cancela por breach (cancelar manualmente); intento final de pago fallido → expira sin reactivación | "You will be charged a subscription fee each month on the same calendar day" · "if the final payment attempt fails, your account will expire." | zendesk 15141145057053 | HIGH (re-fetch directo falló 403/reader; corroborado por 15140989806493 y FAQ) |
| refund | 72 h sólo si cuenta sin usar/sin tradear, menos 75 USD | "we will refund you within 72 hours... minus a $75 fee" | takeprofittrader.com/terms | HIGH |
| reset_cost | 99 USD (50K Test); resets ilimitados; NO cambia la fecha de renewal | "50K $99" · "there are no limits to test resets" · "this will not change the subscription renewal date" | zendesk 15140989806493 · FAQ | HIGH |
| expiration | sin time limit para pasar; expira sólo por renewal fallido; sin política de inactividad documentada | "there is no time limit to reach your profit target" | zendesk 15141145057053 | HIGH |
| profit_target | 3,000 USD (tabla oficial) | "$50,000 | 6 Contracts | $3,000 | $2,000" | zendesk 15170265979165 | HIGH |
| drawdown | 2,000 USD EOD TRAILING: el floor sigue el MÁXIMO balance EOD hacia arriba y lockea en el balance inicial (50,000); el breach se ENFORCEA intradía incl. no realizado → liquidación inmediata | "the drawdown for test accounts is calculated only at the end of the trading day" · "the minimum account balance follows your highest end-of-day balance upward... until it reaches the original starting balance... it stops trailing and remains fixed." · "If your account drops to the Minimum Account Balance at any time — through realized or unrealized losses — the account is immediately liquidated" | zendesk 15170265979165 | HIGH (semántica EOD vs intradía: ver TPT-2) |
| daily_loss | none en Test | "no daily loss limits" | FAQ | HIGH |
| consistency | best day < 50% del net profit total al momento del pass; breach NO falla la cuenta: el profit goal sube a 2 × best day | "your best trading day must be below 50% of your total net profits" · "Updated Profit Goal > High Profit Day's Net P/L × 2" · "you have not failed the test account" | zendesk 15170316538013 | HIGH |
| minimum_days | 3 días de trading con ≥1 trade (cuentas compradas antes del 2026-08-17: 5 días — cambio versionado, no conflicto) | "you must trade for a minimum of 3 trading days. A trading day is defined as any day in which you place at least one trade." | zendesk 15170316538013 | HIGH |
| max_position | 6 minis / 60 micros (micros 10×); sólo productos CME/CBOT/NYMEX/COMEX aprobados | "you can trade up to 60 micro contracts" | zendesk 15169066911133 · 15172629238301 | HIGH |
| sesión/overnight | sin overnight; ventana 6 PM–5 PM ET; auto-close 4:55 PM ET; feriados: perder el close ajustado = liquidación | "Positions cannot be carried from one trading day into the next" · "TPT will automatically close any open position at 4:55 PM Eastern" | zendesk 15170347090461 | HIGH |
| news | permitido en Test | "You're allowed to trade the news." | FAQ | HIGH |
| copy/limits | copy trading entre cuentas propias permitido (copiers aprobados: Tradesyncer, TradeCopia, Affordable Indicators, Replikanto Compliance, nativo); Tests simultáneos ilimitados; máx 5 funded activos; máx 10 activaciones de test aprobado por 30 días rolling; counter-positions entre cuentas propias prohibidas (liquidación de ambas); Cooldown 60 días por tocar rolling adjusted loss limit (bloquea compras/resets/activaciones) | "you can trade as many accounts simultaneously as you'd like" · "The limit is 5 active funded accounts per person" · "activate up to 10 successfully passed tests within a span of 30 calendar days" | FAQ · zendesk 15172695563933 · 34431176505245 | HIGH límites / MEDIUM Cooldown |
| failure_rules[] | tocar MAB (realizado o no realizado) = liquidación inmediata; exceder posición; productos/horarios no aprobados o_hold past close; counter-positions; bots/algos; consistencia NO falla | "If your account drops to the Minimum Account Balance at any time... immediately liquidated" · UTP: "may result in profit forfeiture, account reset, account closure, or removal" | zendesk 15170265979165 · 34431153546397 | HIGH |

### Pass / PRO activation

| campo | valor normalizado | evidencia oficial | fuente | conf |
|---|---|---|---|---|
| pass_transition | target + ≥3 días + consistencia; la suscripción del Test AUTO-CANCELA al pasar; activación manual en dashboard (fee/contrato/POA firmado); sin deadline documentada | "Once you successfully pass your trading test, your subscription will be automatically canceled." · "you must still manually complete the activation steps in your dashboard" | FAQ · zendesk 15141145057053 · 17239170507805 | HIGH (deadline MISSING) |
| activation_cost | 130 USD one-time al activar PRO (0 con NOFEE credit); sin mensualidad PRO | "Pay a one time $130 PRO Account setup fee, and ZERO monthly fees after that" · "no ongoing monthly fees with a PRO or PRO+ Account" | takeprofittrader.com · zendesk 28923632631581 | HIGH |
| starting_reference | 50,000 nominal (mismo buying power que el Test; sin scaling) | "you're at the exact same buying power in your PRO Account that you had in your test account. No gimmicks or 'scaling'" | takeprofittrader.com · zendesk 15171769361053 | HIGH |
| failed_pro | PRO reset 649 USD (50K), hasta 3×, conservando retiros day-one; si el estado de suscripción PRO queda disabled → cierre permanente sin reset; si no → nuevo Test | "50k PRO Reset: $649" · "we allow you to reset your PRO Account up to three times per account" · "if the PRO subscription status is disabled, the PRO account is completely closed" | zendesk 15171895352733 | HIGH |

### Fase 2 — 50K PRO

| campo | valor normalizado | evidencia oficial | fuente | conf |
|---|---|---|---|---|
| drawdown | 2,000 USD INTRADÍA trailing sobre PEAK balance (realizado + NO realizado, tiempo real); nunca excede el balance inicial; lock en 50,000; MAB tocado (realizado o no) = liquidación inmediata | "The Trailing Drawdown is calculated intraday using your peak balance, which includes realized gains and unrealized gains. The drawdown trails intraday" · "will never exceed your starting account balance" | zendesk 15171769361053 · 15171820366109 | HIGH |
| buffer | buffer = máximo drawdown; 50K → umbral 52,000 de balance para retirar al 80% | "your maximum drawdown or buffer zone is $2,000… you will need to reach a balance of $52,000 in order to start withdrawing at 80%" · tabla "50k $52,000" | zendesk 15172219527581 · FAQ | HIGH |
| daily_loss | none documentada en PRO (ausencia en el artículo de reglas PRO) | — | zendesk 15171769361053 | MEDIUM (ausencia) |
| max_position/scaling | sin scaling en ninguna cuenta; el límite de posición sigue aplicando (6/60 implícito por mismo buying power; UTP #2) | "No scaling plan on any account" | FAQ · zendesk 34431153546397 | HIGH / MEDIUM número |
| consistency | none en PRO | "No, there is no consistency rule in the PRO account." | FAQ | HIGH |
| payout_eligibility | day-one y DIARIO; split 80% sólo con balance ≥ buffer (52,000 en 50K) | "In a PRO account you can withdraw from day-one and daily" · "you must build a buffer on the account first" | FAQ · zendesk 15172219527581 | HIGH |
| min_max_withdrawal | sin máximo declarado; sin mínimo declarado PRO→wallet; wallet→bank ≤250 USD tiene fee 50 (>250 gratis) | "No, there is no maximum withdrawal amount." · "a withdrawal of $250 or less from your wallet... $50 withdrawal fee" | FAQ · zendesk 15172354954525 | HIGH |
| payout_split | 80/20 sobre retiros sobre buffer (20% se descuenta automáticamente al solicitar); 90/10 es sólo PRO+ (post-review) | "the profit split is 80/20, where the trader keeps 80%" · "commission is calculated and subtracted automatically" | zendesk 15172219527581 · 15172253980061 | HIGH |
| daily_payout | requests diarios; balance PRO se actualiza 8–9 PM EST; requiere FLAT (sin posiciones ni órdenes) al momento del request | "This is updated daily between 8PM - 9PM EST" · "traders must have no open positions or working orders at the exact moment" | zendesk 15172253980061 | HIGH |
| inside_buffer | permitido pero CIERRA el PRO permanentemente (sin reactivación ni reset); split de las ganancias tomadas: 50% si ≤60 días / 80% si >60 días (CONFLICTO de reloj: ver TPT-1) | "it'll close that account and those profits will be at a 50% profit split" · "once canceled, the PRO account cannot be reactivated or reset" | FAQ · zendesk 15172219527581 | HIGH mecánica / CONFLICTO reloj |
| withdrawal_effect | trailing lockea en 50,000 y deja de moverse; retiro sobre buffer deja la cuenta viva con el drawdown invariado (inferencia por lock + retiros diarios; sin frase textual explícita) | "The drawdown continues to trail profits until it reaches your starting balance; once it reaches that level, it no longer moves." | zendesk 15171769361053 · FAQ | MEDIUM |
| processing | PRO→wallet automatizado 5–10 segundos; wallet→bank: Plaid (US) real-time o ACH 1–2 días hábiles; PayPal/Wise (intl) ≤12 business hours; gates: KYC, tax form, contrato PRO+POA, AML name-match | "the account-to-wallet withdrawal process will take 5-10 seconds" · "payouts are processed through Plaid and are typically real-time" | zendesk 15172253980061 · 15172296875165 | HIGH |
| cash_semantics | cash real a banco/PayPal/Wise (wallet también gastable en TPT); denegación sólo por 4 causas: fondos insuficientes, posiciones/órdenes abiertas al pedir, mantenimiento Tradovate, API caída | "the funds are now in your Wallet and available to be paid out" · "denied, but only for one of four reasons" | zendesk 15172253980061 · 37697356049949 | HIGH |
| PRO+ continuation | upgrade por review (sin umbral fijo); al subir, el PRO se congela con 5,000 de ganancia retenida (share del trader retirable según split PRO; balance negativo de PRO+ se descuenta de ahí); PRO+ arranca en 0 con EOD drawdown −2,000, sin buffer, 90/10; todo trading/retiro posterior en PRO+; NO afecta el primer retiro (ocurre en PRO) | "$5,000 in profit... frozen" · "the PRO+ account would start at $0 with an EOD drawdown of -$2,000" · "all future trading and withdrawals must be done on the PRO+ account only." | zendesk 15171978600349 · 36337706971677 | HIGH |
| reglas_extra_PRO | sin bots/algos; salir antes de limit-up/down; ≥1 día de trading por semana calendario (Dom–Vie); sin posiciones 1 min antes/durante/1 min después de FOMC statement, NFP, CPI | "no positions 1 min before/during/1 min after" (FOMC statements, NFP, CPI) | zendesk 15171769361053 | HIGH |

### Economics ledger TPT (PERSONAL CASH; balances Test/PRO = nominales SIM)

- PURCHASE: −170/mes list (MEDIUM) o −102/mes NOFEE40 (HIGH) por 50K Test.
- SUBSCRIPTION_RENEWAL: mismo monto cada mes calendario mientras el Test esté activo; no auto-cancela al fallar una regla.
- RESET_REBUY: −99 reset Test (ilimitado, no mueve renewal); −649 reset PRO (≤3×, condicional post-failure).
- ACTIVATION: −130 al activar PRO (0 con NOFEE).
- FUNDED_FEE: 0 recurrente.
- OTHER_REQUIRED_COST: comisiones nominales 4.50 USD round-turn mini / 1.50 micro, descontadas del balance nominal en Test y PRO (afectan velocidad a target/buffer, no cash personal directo).
- WITHDRAWAL_RECEIVED: +0.80 × monto retirado sobre buffer (dentro de buffer: cierre + 50%/80% según reloj 60d; −50 fee si wallet→bank ≤250).

## D5 — RULE_CONFLICT register

| id | provider | tema | fuente A | fuente B | estado |
|---|---|---|---|---|---|
| TS-1 | Topstep | cap por tamaño frente a headline genérico de XFA | help.topstep.com/en/articles/8284233 | help.topstep.com/en/articles/8284215 · topstep.com/express-funded-account-rules | RESUELTO por mandato owner D5.3: $2,000 para 50K XFA Standard sin DLL add-on; no hay conflicto material del path congelado. |
| TS-2 | Topstep | ventana de decisión Back2Funded: 30 días calendario (Help Center 12060405, actualizado 2026-08-14, ampliado desde 2026-05-29) vs 7 días (topstep.com/express-funded-account-rules, actualizado 2025-06-26) | help.topstep.com/en/articles/12060405 | topstep.com/express-funded-account-rules | RULE_CONFLICT ABIERTO (página marketing stale) — Help Center más nuevo gana por jerarquía §regla comercial 8; no material para first withdrawal (recuperación post-failure). |
| TS-3 | Topstep | consistencia en XFA Standard: frase del artículo de consistency ("choose Standard or Consistency as your Payout path") vs tabla de Parameters (Standard: ❌) | help.topstep.com/en/articles/8284208 | help.topstep.com/en/articles/8284215 | RESUELTO — Standard no tiene consistency target (tabla + eligibility del Payout Policy sin consistencia). |
| TPT-1 | TPT | reloj inside-buffer, tabla abreviada frente a nota explícita de trading days | zendesk 15172219527581 (tabla) | zendesk 15172219527581 (nota) | RESUELTO por mandato owner D5.3: trading days; ≤60 split 50%, >60 split 80%. No reabrir como días calendario. |
| TPT-2 | TPT | Test drawdown: "calculated only at the end of the trading day" vs liquidación inmediata intradía incl. unrealized (mismo artículo) | zendesk 15170265979165 | zendesk 15170265979165 | RESUELTO como semántica normalizada: el trailing se ACTUALIZA EOD; el breach se ENFORCEA intradía incl. unrealized. |

SECONDARY_FLAGS: ninguno que contradiga fuente oficial (secundarias Topstep consultadas corroboran $3,000/$2,000/EOD-lock; TPT no usó secundarias).

## D5 — Unknowns consolidados (captured_at 2026-09-24)

Topstep: status list-vs-promo del precio $49; inactividad en Combine; deadline de activación XFA; si el día de trading requiere ≥1 trade (implícito); tabla completa de scaling tiers (imagen no textual); frequency cap de payouts (ninguno declarado); población exacta del legacy "100% primeros $10K"; schedule de comisiones por trade (no capturado en ninguna página oficial).
TPT: list price $170 no impreso directamente (derivado triple-consistente); deadline de activación PRO; destino del $130 si el PRO falla después; mínimo PRO→wallet; "no daily loss" explícito en PRO; frase textual del efecto del retiro sobre el drawdown lockeado; inactividad Test; número de reintentos de pago; cutoff horario fijo de payout request.

## D5.3 draft histórico — Contrato normalizado candidato (PropRuleSet)

**Superseded parcialmente por §D5.3 Session Model Review.** Los importes de compra/activación/renovación pertenecen a `PricingSnapshot`; el momento y monto elegido de retiro pertenecen a `WithdrawalPolicy`. El draft se conserva como antecedente, no como contrato implementable. Cap Topstep congelado = $2,000; reloj inside-buffer TPT = trading days. No implementar desde este bloque.

```text
PropRuleSet
  provider: enum {TOPSTEP, TPT}
  product: string                      # "50K Trading Combine → XFA Standard" | "50K Test → PRO"
  captured_at: date                    # 2026-09-24
  currency: USD
  reference_balance: money             # nominal de cuenta (50,000)

  evaluation:
    purchase_cost: money               # TS 49/30d | TPT 170 list (promo separado)
    recurring_cost: money|none
    recurring_calendar: enum {FIXED_30D, CALENDAR_MONTH}
    reset_cost: money                  # TS 49 | TPT 99
    target: money                      # 3,000 ambos
    drawdown: money                    # 2,000 ambos
    drawdown_mode: EOD_TRAILING_LOCK_AT_START        # ambos Tier-1 en evaluación
    breach_enforcement: REALTIME_INCL_UNREALIZED     # ambos (TS monitoreo real-time; TPT liquidación inmediata)
    daily_loss: money|none             # TS none base (add-on excluido) | TPT none
    minimum_days: int                  # TS 2 | TPT 3
    consistency:
      kind: enum {BEST_DAY_MAX_PCT_OF_TARGET, BEST_DAY_MAX_PCT_OF_NET_AT_PASS}
      pct: percent                     # TS 55 | TPT 50
      breach_behavior: enum {RAISE_TARGET_DYNAMIC, RAISE_GOAL_2X_BEST_DAY}
    max_position: {minis: int, micros: int}          # TS 5/50 | TPT 6/60
    failure_rules[]:                   # drawdown breach, conducta, productos/horarios

  funded:
    activation_cost: money             # TS 149 | TPT 130 (promo waives)
    balance_start: money               # TS 0 (nominal) | TPT 50,000 (nominal recentered)
    drawdown: money                    # 2,000 ambos
    drawdown_mode: enum {EOD_TRAILING_LOCK_AT_START, INTRADAY_TRAILING_LOCK_AT_START}
                                       # TS XFA = EOD | TPT PRO = INTRADAY (peak incl. unrealized)
    daily_loss: money|none
    min_winning_days: {count: int, threshold: money} | none    # TS 5×150 | TPT none
    consistency: none                                # ambos sin consistencia en funded
    max_position: fixed | balance_tiered             # TPT 6/60 fijo | TS scaling tiers
    scaling: enum {NONE, BALANCE_TIERS}
    buffer_threshold: money|derived    # TS lock MLL en 0 | TPT start+drawdown (52,000)
    payout_eligibility:
      TOPSTEP: winning_days 5×150 + net_since_last ≥ 0.01 (first exempt) + window Sun5PM–Fri5PM CT + compliance
      TPT: day_one + balance ≥ buffer_threshold + flat al solicitar
    payout_cap: {pct_of_balance, cap, min_request}   # TS {50%, 2000, 125} | TPT {none, none, none}
    payout_split: percent              # TS 90 | TPT 80 (primer retiro)
    failure_rules[]

  withdrawal:
    requested_amount: money            # política del trader (M1: primera elegible)
    trader_cash_received: money        # requested × split − fee(método)
    balance_effect: DEDUCT_ON_APPROVAL # TS explícito | TPT equivalente
    drawdown_effect: enum {MLL_LOCK_0_PERMANENT, TRAILING_LOCKED_UNCHANGED}
    continuation_state: enum {SAME_ACCOUNT, CLOSED_INSIDE_BUFFER_50_80}

  economics:
    purchase_cash_flow      = −purchase_cost
    recurring_cash_flows    = −recurring × ciclos_activos − resets × reset_cost
    activation_cash_flow    = −activation_cost (condicional al pass)
    withdrawal_cash_flow    = +trader_cash_received
    other_cash_flows[]      # TS: DOM 38/mes opcional, Back2Funded 599 ≤2×; TPT: PRO reset 649 ≤3×

topstep:                            # extensiones específicas
  reset_credit_por_rebill (1 gratis, expira 1a); rebill pushed +30d por reset
  micros:minis 10:1; ventana payout Sun5PM–Fri5PM CT; aprobación 1–3 días hábiles
  fees método {Aeropay 0, Brokerage 0 same-day ≤12PM CT, ACH 30, Wire 30}
  post-payout: MLL=0 permanente + conteo 5 winning days reinicia; mín request 125
  Back2Funded 599 (≤2×, 30d desde cierre, sólo pre-payout); límite 5 XFA
  inactividad 30d; cierre voluntario ≤50% cap 5000; XFA balance arranca en 0

tpt:                                # extensiones específicas
  promos lifetime (NOFEE40: 40% + waiver 130); renewal mismo día calendario
  comisiones nominales (4.50 RT mini / 1.50 micro) contra balance en Test y PRO
  inside-buffer withdrawal → cierre permanente + split 50/80 (reloj 60d en conflicto TPT-1)
  PRO reset 649 ≤3×; counter-positions prohibidas; máx 5 funded; 10 activaciones/30d rolling
  PRO extra: ≥1 día trading/semana; no bots; exit antes de limit-up/down; FOMC/NFP/CPI ±1 min
  PRO+ (continuation): freeze 5,000, EOD DD −2,000, sin buffer, 90/10
```

Regla de fidelidad: ningún campo común recibe semántica que no le corresponda; toda excepción material vive en `topstep:`/`tpt:`. Balances nominales y personal cash permanecen separados en todo el contrato.

## D5.4 draft — Simulator capability gap matrix (base: D4 certificado d4f42a4)

**Delta D5.3:** sesiones/flatten obligatorio y compatibility TPT ya no son DEFER: se diseñan en §D5.3 Session Model Review. Trading fees quedan excluidos explícitamente del structural null; pricing sale de PropRuleSet. La matriz siguiente conserva el diagnóstico inicial, no autoriza implementación desde sus simplificaciones.

| capability requerida por Tier-1 | clasificación | detalle / consecuencia de simulador |
|---|---|---|
| barreras de fase + economics F/A/C/W + cohort IID | SUPPORTED | núcleo D4 intacto; reset/rebuy ≈ attempt IID con su fee |
| max_position (5/50, 6/60) | SUPPORTED | `hMax` ya existe como invariante; bajo política fija no cambia la matemática; ratio 10:1 irrelevante en dinero normalizado |
| re-centrado de referencia (XFA balance=0 vs PRO=50,000 nominal) | SUPPORTED | offset de referencia; la equity de fase B arranca en 0 relativo |
| comisiones contra equity nominal (TPT 4.50/1.50; Topstep schedule MISSING) | SMALL_EXTENSION | costo fijo por cierre de trade restado de E en el event loop; rompe la equivalencia exacta D/(T+D) — contabilizar, no ignorar; requiere schedule Topstep (unknown) |
| minimum trading days (TS 2 / TPT 3) | SMALL_EXTENSION | gate de pass sobre la capa de sesiones (condicionado al MATERIAL de sesiones) |
| renovaciones/calendario de suscripción (30d / mes calendario; rebill push por reset) | SMALL_EXTENSION | contabilidad de calendario sobre la duración del attempt; sin cambio matemático |
| payout request→receipt (estados + split + fee método + min request) | SMALL_EXTENSION | transición WITHDRAWAL_REQUESTED→RECEIVED; request→receipt sin riesgo de pérdida de la suma (TS sin clawback; TPT denials operativos) — no cambia el modelo central |
| payout caps/split como función de balance (TS min(50%,2000)/90-10 min 125; TPT 80-20) | SMALL_EXTENSION | función determinista de cash sobre el estado de balance en el primer retiro |
| buffer threshold TPT (52,000 → habilita 80%) | SMALL_EXTENSION | umbral que gatea split/withdrawal |
| capa de sesiones/días (día de trading, PnL diario, marca EOD, winning days, day locks 3:10/4:00 PM CT) | MATERIAL_EXTENSION | D4 no tiene dimensión temporal: se requiere grid de sesiones con PnL diario agregado; habilita min-días, winning days, consistencia y las marcas EOD del trailing |
| EOD trailing drawdown con lock en balance inicial (TS Combine MLL, TS XFA MLL, TPT Test) | MATERIAL_EXTENSION | estado de máximo balance EOD; bajo proceso null continuo, floor trailing ≥ floor estático ⇒ p_pass_trailing ≤ D/(T+D): la barrera estática de D4 SOBREESTIMARÍA p_pass |
| intraday trailing drawdown sobre peak incl. unrealized (TPT PRO) | MATERIAL_EXTENSION | estado path-dependent del running max con ratchet continuo; cambia la semántica de barreras/kernel |
| consistencia (TS 55% target dinámico Best Day÷0.55; TPT 50% gate al pass con goal 2× best day) | MATERIAL_EXTENSION | requiere distribución diaria del path (sesiones) y target/gate dinámicos → condición de pass path-dependent |
| payout eligibility por winning days (TS 5×150 + net≥0.01 + ventana) | MATERIAL_EXTENSION | condición de transición dependiente de sesiones |
| scaling funded por balance (TS XFA tiers, prohibición intradía) | MATERIAL_EXTENSION | límite de posición = función escalonada del balance |
| DLL add-on Topstep (1,000, flatten sin falla; dobla caps — offer excluida) | DEFER | opcional en el path base; no quema ni invalida; sensibilidad posterior |
| restricciones de sesión/overnight (flatten 3:10 PM CT / 4:55 PM ET / feriados) | DEFER | sin modelo de tiempo no existen posiciones overnight; simplificación estructural declarada |
| news restrictions (TS conducta; TPT PRO FOMC/NFP/CPI ±1 min) | DEFER | restricción conductual/ventanas puntuales; no barrera económica del null model |
| conducta prohibida / copy trading / account limits / Cooldown 60d | DEFER | exclusiones, no barreras económicas; multi-cuenta fuera de M1 |
| activation deadlines | DEFER | no existen en ninguna de las dos props (MISSING documental) |
| Back2Funded 599 ≤2× (TS) y PRO reset 649 ≤3× (TPT) | DEFER | recuperación paga condicional post-failure; capturada en ledger; entra como sensibilidad si el owner la pide |
| post-withdrawal continuation (TS MLL=0 + restart conteo; TPT cuenta sobrevive) y payouts #2+ | DEFER | éxito D5-M1 = primer WITHDRAWAL_RECEIVED; capturado como continuation_state |

Síntesis del gap: el núcleo matemático D4 (first-passage exacto, adds self-financing, lifecycle, cohort, economics) se conserva; la extensión dominante es UNA capa de sesiones/días (MATERIAL) que habilita trailing EOD, consistencia, min-días y winning days; el trailing intraday de TPT PRO es la segunda pieza MATERIAL; el resto son extensiones locales o diferimientos explícitos.

## D5 — Evidence register (captured_at 2026-09-24)

- Jerarquía aplicada: official current documentation > official FAQ/terms > official pricing/product page > secondary (sólo SECONDARY_FLAG). Secundarias jamás establecieron una regla.
- Re-verificación verbatim del manager (fetch directo en sesión): Topstep 14289835 (pricing), 8284204 (MLL), 8284208 (consistency, confirma target $3,000 explícito), 8284233 (payout policy, confirma tabla de caps por tamaño), 8284215 (XFA parameters), 8284197 (TC parameters); TPT 15170265979165 (Rule 3: tabla $50,000/6/$3,000/$2,000 + mecánica EOD completa), 15172219527581 (profit split + buffer + inside-buffer), 15172253980061 (PRO→wallet), 29660646764445 (NOFEE40: $102 plana + waiver $130).
- Captura de campo por agentes de research con cita verbatim por regla: resto de URLs listadas en D5.2A/D5.2B (Topstep: 18 artículos Help Center + express-funded-account-rules; TPT: 30 artículos zendesk + FAQ + homepage + terms). Freshness registrada por página (Topstep Help Center mayormente jun–ago 2026, varios "updated this week"; topstep.com/express-funded-account-rules stale 2025-06-26; TPT zendesk may–sep 2026, Rule 5 y PRO Rules 2026-09-22; FAQ TPT sin fecha visible).
- Re-fetch NO reverificable en sesión: TPT 15141145057053 (Test subscriptions) — WebFetch 403 + reader error ×2 ⇒ confidence apoyada en cita verbatim del agente + doble corroboración cruzada (reset article y NOFEE40 FAQ oficiales).
- /verify: 12/12 ítems del mandato cumplidos (fuente oficial por regla, capture date, contradicciones en RULE_CONFLICT, proveedor/producto/fase en toda regla, requested≠received separados, nominal≠personal cash separados, q=10% no usado, contratos reproducibles, gap completo, cero código, D4 intocado, Tier-2 no investigado).

## D5 — Reuse (artefactos autoridad D5)

Sobreviven como autoridad: paquete de reglas Topstep (§D5.2A), paquete TPT (§D5.2B), contrato normalizado candidato (§D5.3 draft), RULE_CONFLICT register (§D5), unknowns consolidados (§D5), simulator capability matrix (§D5.4 draft), evidence register (§D5). No se crearon abstracciones genéricas adicionales sin evidencia.

REUSABLE_BEHAVIOR_CANDIDATES (para rule-capture Tier-2 futuro): (1) capturar schedule de comisiones/data fees explícitamente — quedó MISSING en Topstep; (2) extraer precio list desde la tabla/API de pricing cuando el HTML es JS-rendered (caso TPT $170 derivado); (3) registrar `updated_at` de cada artículo vía API del help desk cuando la página no muestra fecha; (4) fetch cruzado marketing site + help desk siempre — las páginas marketing se desactualizan (causa de TS-2); (5) snapshot archive (p.ej. Wayback) de cada URL citada en captured_at para inmunidad ante ediciones futuras.


## Manager Review — D5.2 Tier-1 Rule Capture — 2026-09-24

Status: **REVIEW_WITH_FINDINGS**. El paquete de research es materialmente bueno y suficiente para continuar el diseño, pero NO está listo para `D5_TIER1_RULES_CAPTURED=ACCEPTED` todavía.

### Findings

1. **TS-1 no es un RULE_CONFLICT material.** La página XFA usa un headline genérico "up to $5,000*" y remite explícitamente al Payout Policy para el cap por account size. El Payout Policy vigente fija 50K XFA Standard = **$2,000**. Resolver TS-1 a `$2,000` para el path congelado sin DLL add-on.
2. **TPT automation compatibility = BLOCKER de producto, no DEFER.** PRO Rules prohíbe trading bots/algos y exige ejecución manual. La Trade Copier Policy sí permite copiar entre cuentas propias, pero sólo mediante copiers aprobados/platform-native; un copier custom no está aprobado por defecto. Antes de invertir en soporte TPT para Echo Futures debe determinarse si el target operativo será manual-reference + approved copier, o si TPT queda economics-only / NO_GO para automation.
3. **WithdrawalPolicy falta como contrato separado.** Las reglas no determinan por sí solas cash EV. Topstep permite elegir requested amount dentro de min/cap; TPT permite dos rutas materialmente distintas: esperar buffer y retirar 80%, o retirar dentro del buffer cerrando PRO con split 50%/80% según antigüedad. D5 debe modelar `WithdrawalPolicy` separada de `PropRuleSet`.
4. **TPT inside-buffer path es material para q_withdraw.** Como success = primer cash real, cerrar dentro del buffer puede lograr WITHDRAWAL_RECEIVED antes de alcanzar $52K. No se puede ignorar sin congelar explícitamente una policy.
5. **TPT pricing debe ser snapshot/scenario.** List price 50K = $170/month; homepage vigente muestra $102/month bajo 40% promo y promo docs indican activation $130 waived para cuentas elegibles. No mezclar precio promocional con regla estructural.
6. **Principal gap matemático: session boundary.** D4 no tiene tiempo/días. EOD trailing, consistency y winning-days necesitan una definición estocástica del estado al cierre de sesión; no basta agregar contadores. Antes de Shot A debe congelarse un session-aware null model o una abstracción equivalente validada matemáticamente.
7. **Commissions/costs:** no mezclar schedules incompletos. O capturar schedules comparables de ambas props o congelar explícitamente `execution_cost_model=0` para el primer structural-null result y correr sensibilidad después.

### Required resolutions before SPEC freeze

- R1: Topstep 50K Standard payout cap = $2,000 for the frozen path.
- R2: Decide TPT operational compatibility posture: `AUTOMATION_COMPATIBLE | MANUAL_REFERENCE_ONLY | ECONOMICS_ONLY | DROP_TIER1`.
- R3: Freeze first-withdrawal policies to simulate; minimum required: `MAX_ELIGIBLE` and TPT `CLOSE_INSIDE_BUFFER` vs `WAIT_FOR_BUFFER`.
- R4: Freeze pricing scenarios: list/base vs current promo snapshot.
- R5: Produce a mathematically reviewed session-aware extension design before implementation.
- R6: Resolve execution-cost posture for M1.

### Gate

`D5_TIER1_RULES_CAPTURED` remains **REVIEW_WITH_FINDINGS**.
Do not start implementation. Next action: resolve R1–R6, then freeze Functional/Technical SPEC.


## D5-M1 — Tier-1 Prop Economics Vertical Slice

### Observable outcome

Using the certified D4 simulator baseline, reproduce the complete real-rule lifecycle for:
- Topstep 50K Trading Combine Standard → XFA Standard;
- Take Profit Trader 50K Test → PRO;

from evaluation purchase until either:
- `WITHDRAWAL_RECEIVED`; or
- `BURNED`.

The first milestone is **not** “support prop rules generically”. It is a bounded research capability that answers, under the null model, for each Tier-1:
- `P(pass evaluation)`;
- `P(funded | pass)`;
- `P(payout eligible | funded)`;
- `P(first withdrawal | funded)`;
- `q_withdraw`;
- expected evaluations / first withdrawal;
- burn/activation counts;
- no-withdrawal probability after 5/10/20/50 evaluations;
- expected cash per evaluation;
- cumulative cash before first withdrawal;
- cash P5/P50/P95;
- net cash per 10 and 100 evaluations;
- minimum/trading-day path where the rules make time relevant.

### Delivery sequence

1. **Rules capture — Topstep and TPT only.**
   Official sources, exact 50K path, capture date, conflicts and ambiguities.
2. **Normalization.**
   Create a common lifecycle/rule contract plus explicit prop-specific exceptions.
3. **Simulator gap analysis.**
   Map every required rule to `SUPPORTED | SMALL_EXTENSION | MATERIAL_EXTENSION | DEFER`.
4. **SPEC freeze.**
   Functional + technical SPEC for the minimum D4 extension required by Topstep/TPT.
5. **Three development shots.**
   Shot A implementation; Shot B fresh independent falsification; Shot C accepted corrections + certification.
6. **Null experiments.**
   No synthetic edge first. Produce Tier-1 economics from real rules.
7. **Owner gate.**
   Only after M1 passes, expand to Tier-2 and conditional edge/hardscalping sensitivities.

### Explicit non-goals M1

- Apex/MFFU/Tradeify implementation.
- FTMO Futures.
- empirical strategy edge.
- NinjaTrader/Echo integration.
- historical futures backtest.
- multi-prop generic framework beyond what Topstep/TPT force.
- payout #2+ optimization unless a rule is required to compute first withdrawal correctly.

## D5.3 Session Model Review — 2026-09-24

### Mandato, autoridad y decisiones que prevalecen

Diseño matemático, no Functional/Technical SPEC. Baseline certificado: `d4f42a41946f12231b75e4eb65b90d132731be0d`; [[D4 — Simulator v0 Functional SPEC]], [[D4 — Simulator v0 Technical SPEC]] y [[echo-futures-astra-math-review]] permanecen CLOSED/intactos. Esta sección sustituye los drafts D5.3/D5.4 sólo donde afectan sesiones, trailing, contadores/consistencia, retiro, precios y compatibilidad TPT. Los paquetes D5.2 se reutilizan; no se repite research de firmas ni se amplía Tier-1.

| Decisión | Resultado de este diseño |
|---|---|
| Modelo v1 recomendado | `CLOCKED_BROWNIAN_SESSION_KERNEL`: Brownian continuo sin drift, reloj de varianza explícito, kernel conjunto de primer evento/supervivencia a fin de intervalo; máximo intradía para TPT PRO |
| Costes de ejecución M1 estructural | `execution_cost_model = ZERO_STRUCTURAL_NULL`, explícito y separado de cash fees; no representa ejecución neta real |
| Synthetic edge en sesiones | Sólo `delta=0`; rechazar `delta≠0` en este modelo. D4 legacy retiene su contrato synthetic y T7/T8 |
| TS-1 | RESUELTO por mandato owner: Topstep 50K XFA Standard sin DLL add-on, cap bruto $2,000/request |
| TPT-1 | RESUELTO por mandato owner: ≤60 trading days → 50%; >60 trading days → 80% al cerrar dentro del buffer |
| TPT para el target Echo automatizado | `ECONOMICS_ONLY`; permanece comparación económica Tier-1, no candidato aprobado para ejecutar bots |
| Éxito | `WITHDRAWAL_RECEIVED` con cash externo neto positivo; request, aprobación y wallet son estados intermedios |
| Gate / próximo paso | `D5_SESSION_MODEL_PASS = REVIEW` / `MATH_REVIEW`; sólo el owner acepta |

### A1 — Qué información falta y por qué contadores no bastan

D4 entrega `P(τ_U<τ_L)=(x−L)/(U−L)` sin modelar `τ`. La misma probabilidad corresponde a cualquier volatilidad positiva constante, pero cambiar la volatilidad cambia radicalmente cuántos eventos ocurren antes del cierre. No se puede inferir de D4 una distribución de PnL diario, cantidad de días, coste de renovaciones ni winning days. Tampoco se puede muestrear una duración independiente del lado de salida: ambos están correlacionados.

En cada tramo de posición constante se necesita la ley conjunta de `(τ, tipo_de_evento, estado_en_τ)` si un evento ocurre antes del próximo límite temporal, o `(estado_al_límite | ningún_evento_previo)` y su probabilidad de supervivencia. El endpoint sin condicionar puede pertenecer a un path que ya quebró. En TPT PRO, además hace falta el running maximum y el orden temporal de sus incrementos y descensos: un máximo y un mínimo de sesión sin orden no determinan si hubo drawdown. Se requiere kernel con absorción continua, no reconstruir un camino ficticio desde el retorno diario.

### A2 — Alternativas examinadas

| Candidato | Compatibilidad con D4 y adds | Sesgo / auditoría null | Complejidad / reproducibilidad | Decisión |
|---|---|---|---|---|
| A. Brownian continuo, horizonte finito, implementado con pasos Euler/retornos Gaussianos | Mismo proceso en el límite; una malla finita pierde primeros cruces y orden de adds | Ignora cruces entre nodos, típicamente sobreestima supervivencia y subestima ratchet. Media gaussiana cero no demuestra null para el proceso detenido implementado | Media; reproducible con seed+malla, pero resultados dependen de malla y correcciones | Rechazado como motor de referencia v1; útil sólo como contraste con convergencia |
| B. Kernel Brownian conjunto de sesión/primer evento, extendido a `(equity, máximo)` cuando corresponde | D4 es su marginal de salida sin deadline. Conserva precios de adds y bookkeeping, tiempo correlacionado y censura correcta | Cero sesgo estructural de discretización temporal en la ley matemática; aproximación numérica exige error declarado. Martingala auditable | Media para barreras fijas; alta pero acotada para PRO antes del lock. Seed + versión de kernel/tolerancias/calendario determinan resultado | **SELECCIONADO**: una ley continua con dos estados mínimos de kernel según fase |
| C. Una distribución de retorno diario encima de los wins/losses D4 | Generalmente incompatible: dobla fuentes de PnL o pierde la relación entre exposición, adds y duración | Puede forzar media cero diaria y aun así sesgar ruina, consistencia y q. Calibrar varianza no recupera el orden del path | Baja y reproducible, pero la reproducción no valida la ley | Rechazado. Si la distribución incluye exactamente todos los eventos y máximos condicionados, ya es B |
| D. CTMC/random walk en retícula o reloj de número fijo de trades por día | Admite adds sólo con estados alineados; las duraciones implícitas dependen de política. Retícula no preserva Brownian/D4 salvo límites controlados | Overshoot, redondeo de barreras y muestreo artificial de EOD cambian la probabilidad. Puede ser martingala de otro modelo | Media; excelente como oráculo independiente de refinamiento | Rechazado para producción v1; aceptado como oráculo numérico con límites y refinamiento |

Un Brownian bridge es una forma de realizar B, no una licencia para muestrear endpoint, máximo y cruces independientemente. Una bridge bajo dos barreras debe condicionarse a supervivencia y respetar el primer evento; PRO requiere también el máximo continuo y su dependencia con la absorción. El contrato elegido fija esa ley aunque la futura revisión técnica elija una representación numérica equivalente.

### A3 — Proceso, tiempo y política de exposición mínimos

Usar unidades normalizadas de precio de D4: `dS_t = σ_z(t) dW_t`, drift cero, con reloj `v(t)=∫σ_z(u)²du`. `σ_z(t)` es determinista, piecewise constant y positivo en ventanas activas; fuera de ellas no hay posición ni exposición. Para referencia puede expresarse `ν_session=∫session σ_z²dt`, pero no se debe identificar un día calendario con una unidad Brownian sin declarar esa escala. Una sesión más corta reduce `ν` bajo la misma tasa por hora; no se renormaliza silenciosamente a un día completo.

`σ`, `G`, `L`, `h0`, lista finita de adds y `hMax` son inputs hipotéticos identificados en cada escenario. No hay estimación empírica, cifra base de q ni escala de volatilidad inferible de D4. La familia `q_withdraw(ν, TradePolicy, WithdrawalPolicy, calendario, settlement)` es la salida correcta hasta congelar escenarios; variar ν es sensibilidad estructural, no edge. Los límites de posición y unidades de contrato deben validarse en el escenario; no introducir scaling ficticio. Una v1 puede usar exposición siempre dentro del mínimo límite permitido y dejar scaling variable fuera.

Política de trading de referencia propuesta: abrir al inicio de cada ventana activa; cerrar por TP/SL o breach; reabrir inmediatamente tras TP/SL mientras la ventana siga abierta; ningún límite artificial de trades/día. Usar el último evento antes de cada corte determinista y liquidar la posición superviviente a su precio condicionado. No llevar posición ni add pendiente a la sesión siguiente. Cortes de noticias/early close son ventanas exógenas versionadas, con flat obligatorio y reapertura posterior; no crean trading days adicionales. No se impone un profit stop diario implícito ni se deja de operar por tocar $3,000 intradía. Las decisiones de pass/retiro de esta v1 se evalúan sobre el snapshot diario completo; es una política EOD explícita, no afirmación de que la firma prohíba terminar antes.

La política EOD puede perder ganancias logradas intradía antes de que se reconozca pass/eligibility; esa diferencia frente a una política de flatten temprano es real y debe etiquetarse. Optimizar stopping intradía sería otro escenario, no un arreglo que pueda inventar el coding agent. El modelo continuo tiene tiempos de decisión discretos para retiros: evita la política patológica «cerrar en el primer instante con ganancia >0», cuyo ínfimo en Brownian puede ser cero sin un primer beneficio positivo bien definido.

El proceso nominal self-financing sigue siendo `E_t = E_0 + ∫H_u dS_u`. Con `0<h0≤H≤hMax<∞` durante exposición, un número finito de adds por trade y horizontes acotados, `E[E_{t∧τ}]=E_0` y `E[(E_{t∧τ}−E_0)²]=E[∫_0^{t∧τ}H_u²σ_z(u)²du]`. Cierre/reapertura sin costes no cambia equity. Para un tiempo de éxito ilimitado, no basta invocar optional stopping: verificar absorción/integrabilidad o reportar censura y cotas; no asegurar media terminal cero sin esas condiciones.

Los adds mantienen exactamente `Y=b+h·s`, `h'=h+Δh`, `b'=b−Δh·s`, `Y'=Y`. Son acciones adaptadas al estado actual, nunca al futuro endpoint de una bridge; conservar orden y exclusión de adds fuera de barreras D4. **Lo que no se conserva como claim universal es la invariancia de p frente a sizing:** con sesiones, trailing y day gates, cambiar H cambia duración y distribución diaria aun sin drift. Tampoco se aplica `D/(T+D)` al ruleset real.

### A4 — Contrato matemático del kernel seleccionado

Para cada estado Z y tiempo de varianza restante V hasta el próximo corte exógeno, definir `τ = inf{v≥0: ocurre una barrera económica o un evento de trading}`. El kernel devuelve exactamente una de estas ramas, con su masa conjunta:

- `EVENT`: `(τ≤V, tipo, Z_τ)`, con tiempo, precio, equity y máximo si corresponde. Se consume τ del reloj; un trade nuevo no reinicia el tiempo restante.
- `SURVIVED_TO_BOUNDARY`: `(τ>V, Z_V)`. Se conserva toda la masa superviviente; no se sustituye `Z_V` por una normal incondicional ni por la barrera que se habría tocado después.

En Topstep y TPT Test el loss floor es constante dentro de cada sesión. Entre eventos, los niveles de precio son los de D4 reemplazando `−Drawdown` por el floor vigente; el phase upper absorbente está desactivado en modo prop EOD. `lowerEvent` es el siguiente add elegible o la barrera inferior terminal; `upperEvent` es TP. Con `a<x<b`, `ℓ=b−a` y varianza V, la densidad subprobabilidad de endpoint superviviente es:

`k_V(x,y) = (2/ℓ) Σ_{n≥1} sin[nπ(x−a)/ℓ] sin[nπ(y−a)/ℓ] exp[−n²π²V/(2ℓ²)]`, para `a<y<b`.

Su integral es supervivencia. Las densidades conjuntas de salida por unidad de varianza son `f_a(v|x)=½ ∂_y k_v(x,y)|_{a+}` y `f_b(v|x)=−½ ∂_y k_v(x,y)|_{b−}`. Integrar salidas hasta V más supervivencia da 1. La mezcla fija el evento y su duración; si sobrevive se usa `k_V/∫k_V`. Al integrar `f_b` hasta infinito se recupera exactamente `(x−a)/(b−a)`. El cambio de tiempo determinista convierte v en hora de calendario; no se muestrea una duración independiente. Esta formulación es derivación matemática del modelo propuesto y queda sujeta a revisión.

Para TPT PRO antes del lock usar equity `e` y máximo `m`, ambos relativos al inicio de fase, con `m≥max(0,e)` y `F(m)=min(0,m−D)`, D=$2,000. Entre acciones `de=h·dW_v`, `dm` sólo aumenta cuando e marca máximo; matar el proceso al tocar `e≤F(m)`. Los TP/SL/adds se mapean a niveles de e con el bookkeeping vigente y compiten con ese killing. La ley requerida es la distribución conjunta del primer evento `(τ,tipo,e_τ,m_τ)` o supervivencia `(e_V,m_V)`, nunca dos draws marginales independientes.

Caracterización suficiente para revisión/realización numérica: semigrupo detenido de `(e,m)` con generador interior `𝓛=(h²/2)∂²_e`, frontera absorbente `e=F(m)` y fronteras de trading etiquetadas según el primer evento. En la diagonal `e=m<D`, las funciones backward del dominio cumplen `∂_m u(e,m)|_{e=m}=0`; al alcanzar `m=D` se empalma al kernel 1D con floor fijo 0. Condición inicial de semigrupo identidad y datos de frontera de cada evento fijan la ley; las acciones add/close cambian coeficientes/estado sólo después del evento. El máximo no se resetea al cerrar trades ni al terminar días. Tras lock, almacenarlo completo deja de ser necesario para reglas de primera extracción: bastan `locked=true` y F=0.

La ley es exacta; una implementación de series/inversión/PDE puede ser aproximada. El gate no promete un sampler exacto de PRO aún construido ni una solución cerrada para q. No se admite anunciar «exacto» si el evaluador usa malla sin cota de error. La revisión matemática debe aceptar la realización y presupuesto de error antes de SPEC freeze; si no resulta viable, volver a REVIEW del diseño, no sustituirlo silenciosamente por retornos diarios.

### A5 — Estado de sesión y orden de eventos

Estado mínimo adicional al de D4: identificadores de fase/sesión; timestamp y tiempo de varianza restante; balance realizado relativo B; equity E; balance inicial del día `B_open`; PnL realizado del día y provisional; flag de entrada/round-trip; siguiente add; máximo EOD `H_EOD`; floor F y flag lock; máximo intradía M sólo para PRO no lockeado; trading days `N`; winning days `W`; best locked day `A`; snapshot publicado y su session_id; ledger de retiros/settlement; próxima fecha de renovación. Phase equity 0 representa 50,000 nominales en Combine/Test/PRO y 0 en XFA. La referencia nominal nunca es depósito personal.

| Boundary | Modelo y etiqueta |
|---|---|
| Topstep | Sesión abre 17:00 `America/Chicago`, flatten/lock del PnL diario 15:10 del siguiente día habilitado; winning-day publication 16:00. El intervalo 15:10–16:00 no añade PnL ni otra sesión |
| TPT | Trading day 18:00–17:00 `America/New_York`; hard flatten 16:55. Mantener plano hasta el corte. Snapshot de dashboard posterior, publicado en ventana 20:00–21:00 Eastern; no es una segunda sesión |
| Holidays / DST | Calendario de sesiones versionado, IANA timezone y versión tzdb; incluir early close y fines de semana. No usar UTC−5 fijo ni timezone de Chile |
| TPT publicación durante sesión siguiente | Si el snapshot previo aún no está publicado, la policy espera plana antes de request. No combinar balance de ayer con PnL abierto de hoy. Fijar latencia de publicación en el escenario; 21:00 Eastern es supuesto conservador posible, no SLA |
| Inactividad / edad | Días de actividad son por session_id con ejecución, no por fecha civil ni número de trades. PRO age se reinicia al activar; los días Test no cuentan. El contador PRO usa ≥1 round-trip; la liquidación EOD del trade abierto completa el round-trip |

Secuencia de cierre de sesión para sobrevivientes:

1. Resolver cualquier breach intradía, incluido tocar floor al límite: tiene prioridad absoluta y no puede ser rescatado por el endpoint final ni por un retiro. Conservar prioridad D4 phase-loss > trade-close > add; en empate con hard close, cerrar antes de ejecutar un add o reabrir. Un empate exacto tiene probabilidad cero en el modelo regular, pero las fixtures deben ser deterministas.
2. Liquidar posición superviviente a `S_close` condicionado, cancelar órdenes y fijar `B_close=E_close`. No generar precio ni PnL adicionales durante publication lag.
3. Calcular `d=B_close−B_open` en fases sin transferencias; en general excluir débitos de payout/deposit de d. Comisiones nominales entrarían aquí y en equity cuando se devenguen; M1 estructural usa 0. No mezclar fees personales de compra/activación con PnL del día.
4. Actualizar `N←N+1{actividad}`, `A←max(A,d,0)` y, sólo XFA, `W←W+1{actividad y d≥150}`. Cada session_id una vez; los contadores se publican cuando corresponde. Pérdidas no borran best day ni W. Sin actividad no hay winning day, aunque exista un crédito externo.
5. Aplicar ratchet EOD donde corresponda y volver a validar solvencia frente al nuevo floor. Registrar lock. En PRO no hacer un segundo ratchet EOD: ya se aplicó continuamente.
6. Evaluar pass EOD y transicionar sólo después de publicación/activación; reset de variables de fase y del historial diario, sin transferir profit de evaluación. Primer funded trade en una nueva ventana completa elegible de esta policy. Publicar eligibility XFA sólo a las 16:00; retirar usando snapshot autorizado y cuenta flat.

Para EOD trailing: `H_j=max(H_{j−1},B_close,j)`, `H_0=0`, `F_j=min(0,H_j−2000)`, `F_0=−2000`; dentro del día j se aplica `F_{j−1}`. Equivalente `F_j=max(F_{j−1},min(0,B_close,j−2000))`. Nunca decrece; lock permanente cuando H alcanza 2000. Para PRO: `M_t=max(0,sup_{u≤t}E_u)`, `F_t=min(0,M_t−2000)` continuamente, incluso ganancias no realizadas. Un add self-financing no produce nuevo máximo por sí mismo. Un retiro tampoco baja F/M. En XFA el primer payout fuerza F=0 aunque el ratchet no hubiese llegado allí.

### A6 — Consistencia y winning days

Definir `P=B_close` como net profit acumulado relativo de evaluación y `A=max(0,d_1,…,d_N)` con días cerrados. La evaluación permanece activa si falta consistencia; no quema la cuenta ni borra pérdidas.

- **Topstep Combine:** `N≥2`, `P≥3000` y `A≤0.55·P`. Target efectivo `T_TS=max(3000,A/0.55)` sin redondeo de elegibilidad. El provisional intradía usa `max(A_locked,d_current,0)`; se congela al cierre, no se sustituye por máximo intradía de equity. Más profit en el mismo día eleva también ese día y puede elevar el target. El diseño EOD no adelanta el pass por haber tocado el target viejo. Fuente focal: [Consistency at Topstep](https://help.topstep.com/en/articles/8284208-consistency-at-topstep).
- **TPT Test:** `N≥3`, `P≥3000` y `A<0.50·P`, estrictamente. Registrar frontera `P>2A`; `max(3000,2A)` solo no basta porque admitiría igualdad cuando `P=2A`. Comparar mediante productos cruzados con reglas numéricas explícitas; no reemplazar `<` por `≤` ni por un epsilon favorable. Fuente focal: [Rule 5: Be Consistent](https://takeprofittraderhelp.zendesk.com/hc/en-us/articles/15170316538013-Rule-5-Be-Consistent).
- **Topstep XFA Standard:** no consistency gate. W cuenta días con PnL neto final ≥150; cinco días no consecutivos habilitan el componente de días. Una ganancia intradía de 150 que termina en 149.99 no cuenta. El primer request está exento de profit positivo desde un payout previo; no está exento de balance suficiente, mínimo, cap ni receipt.

### A7 — Compatibilidad exacta y límites de D4

Preservado: proceso null sin drift, bookkeeping self-financing, barreras continuas sin overshoot, adds finitos adversos, prioridad de eventos de D4, aislamiento cash/nominal, seed explícita y fixtures legacy. Superseded sólo para el modo D5: ausencia de tiempo, phase-upper como pass instantáneo, resultados terminales siempre ±target/stop, cash W constante y fees C deterministas. Un cierre por horario produce un PnL interior; los fees recurrentes y el cash retirado son variables del path.

La compatibilidad de barreras estáticas se exige al desactivar gates y trailing **y también** quitar liquidaciones forzadas/reset de trade por sesión, o llevar el primer horizonte a infinito. Entonces el marginal de eventos es D4 y la probabilidad de evaluación +3000/−2000 es 0.4. Mantener un cierre finito puede alterar el trade win rate y no tiene por qué recuperar T1–T3; exigirlo ocultaría una contradicción.

Un intervalo matemático de duración cero es identidad de kernel (`K_0=I`), no un trade instantáneo ni un día ganado. Una sesión configurada con duración cero se rechaza; la fixture K0 no ejecuta business events. Desactivar `EOD_update` congela el floor, pero no elimina automáticamente flatten, day gates o reloj. Separar boundaries de mera observación de cierres económicos permite verificar `K_{u+v}=K_uK_v` sin introducir resets. El modo legacy D4 sigue accesible y no necesita simular días para sus T1–T8.

`delta` de D4 perturba un lado terminal sin definir tiempos ni paths condicionados. No existe una extensión única a sesiones: censurar una salida alterada antes de EOD puede crear sesgo inadvertido. Por eso D5 v1 acepta sólo null; `delta≠0` en sesiones es configuración inválida. Un futuro modelo de edge necesitará una ley temporal propia y revisión independiente; no reinterpretar delta como drift físico.

Reproducibilidad: seed + configuración normalizada + IDs/versiones de RuleSet, TradePolicy, WithdrawalPolicy, PricingSnapshot, calendario/tzdb, kernel y tolerancias. Determinismo de orden RNG y serialización. D5 debe repetir sus propios bytes en el mismo entorno soportado; no se promete igualdad bit a bit de muestras D4 vs D5, pues muestrear tiempos consume RNG adicional. La igualdad requerida entre motores es de ley; D4 legacy conserva su contrato original.

### B1 — WithdrawalPolicy separada de reglas

`PropRuleSet` determina una correspondencia legal `AllowedRequests(state)`, mínimos/caps/split/buffer, flatness, ventanas y efectos en cuenta. `WithdrawalPolicy` elige dentro de ella. El contrato conceptual mínimo es: `policy_id/version`; `decision_schedule`; `eligibility_state`; `requested_amount_policy(state, allowed_set)`; `close_account_if_required`; `continuation_policy`; `minimum_positive_external_cash`; `settlement_profile_id`. Estado de elegibilidad distingue `NOT_ELIGIBLE`, `ELIGIBLE_ABOVE_BUFFER`, `ELIGIBLE_CLOSE_REQUIRED`, `AWAITING_DAY_LOCK`, `AWAITING_PUBLICATION`, `PENDING_REQUEST`, `PENDING_RECEIPT` y `UNKNOWN_RULE`. Un campo material desconocido invalida el escenario de reglas completas; nunca se interpreta como permitido.

Convención monetaria: R es débito **bruto** de profit nominal autorizado por la firma; `w=s·R` es entitlement del trader tras split; `c=w−f(w,method)−external_fees` es cash recibido. Seleccionar sólo requests que dejan `c>0`, respetan unidad monetaria de retiro y mínimos oficiales; `minimum_positive_external_cash=0.01 USD` es decisión de policy, no mínimo de firma. Redondear R hacia abajo a centavos para requests; no redondear el proceso Brownian ni los gates de consistencia. Los tests analíticos de martingala preceden el redondeo de retiro.

| Policy | Trigger y requested_amount_policy | close_account_if_required / continuación |
|---|---|---|
| Topstep `MAX_ELIGIBLE` | Primer snapshot/ventana permitida con W≥5, R=`floor_cent(min(0.5·B,2000))`≥125 y cash externo positivo. B es balance XFA relativo, no 50,000+profit | false; flat mientras se procesa. Al aprobar: B←B−R, F←0, reset del ciclo de winning days; cuenta sigue abierta. Absorber experimento sólo en receipt |
| TPT `WAIT_FOR_BUFFER` | Primer snapshot con profit retirable sobre buffer y cash positivo; en escenario `RETAIN_BUFFER`, R=`floor_cent(max(B−2000,0))`, s=0.8. B=2000 exacto da R=0 y **no** éxito | false; conservar buffer, flat mientras request/settlement; registrar cuenta abierta al receipt |
| TPT `CLOSE_INSIDE_BUFFER` | Primer snapshot de PRO con 0<B≤2000 y R=`floor_cent(B)` que produce cash positivo; split s=0.5 si N_PRO≤60, s=0.8 si N_PRO>60. No esperar al día 61 de forma implícita. Si el primer snapshot disponible ya tiene B>2000, usar la misma extracción sobre buffer de WAIT para totalizar la policy, sin cierre | true sólo cuando la ruta lo exige; confirmar cierre total antes de request inside-buffer. Cuenta `CLOSED_FOR_WITHDRAWAL`, nunca confundir con BURNED. Sin reapertura/reset; receipt aún puede ser éxito |

Estas son políticas de decisión en snapshots EOD, no máximos globales de EV ni claims de óptimo. En `CLOSE_INSIDE_BUFFER`, si el neto es cero/negativo por fees, continuar al siguiente día; no fabricar success por un retiro de $1 que no llega como cash. La ruta conservadora sobre buffer es una hipótesis explícita `RETAIN_BUFFER` pendiente de precisión documental del monto máximo, como se indica en B4; no convierte una interpretación en regla permanente.

### B2 — Request no equivale a cash

Lifecycle mínimo: `PURCHASE_EVALUATION → EVALUATION → PASSED → FUNDED → ELIGIBLE → WITHDRAWAL_REQUESTED → APPROVED/DEBITED → WALLET_CREDITED (TPT) → WITHDRAWAL_RECEIVED`. Ramas: `BURNED`, `CLOSED_FOR_WITHDRAWAL`, `RETRYABLE_OPERATIONAL_FAILURE`, `DENIED`, `INCOMPLETE`. El estado económico terminal de cuenta y el estado de liquidación del cobro son ejes distintos: cerrar PRO para retirar no quema el entitlement; un cash pendiente no se contabiliza como recibido. No sumar a K una cuenta de prop ni saldo wallet aún no remitido.

Policy v1: permanecer flat desde decisión hasta receipt; no reutilizar wallet para comprar otra evaluación. Reintentar errores transitorios sin recrear el débito ni recontar el retiro; un rejection definitivo no se convierte en burn matemático. `SettlementProfile=IDEAL_COMPLIANT` puede fijar aprobación/remesa eventual cierta, compliance/KYC satisfechos y latencia explícita, pero resultados se etiquetan **condicionales a settlement ideal**, no probabilidades empíricas de recibir dinero. Latencias/fallos operativos alternativos deben ser inputs, sin porcentajes inventados. Nunca inferir probabilidad 1 real por documentación de plazo típico.

Para TPT, `w≤250` incurre fee de wallet 50; `w>250`, fee de firma 0, más posibles costes del método. El test aplica al monto wallet→externo, no a R antes del split. Sin cartera previa y primera remesa completa, w es el importe de esa remesa. Ejemplos aritméticos, sin calibración: R=200 y s=.5 ⇒ w=100, c=50; R=300 y s=.8 ⇒ w=240, c=190; R=400 y s=.8 ⇒ w=320, c=320, todos con external_fees=0. [Withdrawal Fees](https://takeprofittraderhelp.zendesk.com/hc/en-us/articles/15172354954525-Withdrawal-Fees) y [PRO→Wallet](https://takeprofittraderhelp.zendesk.com/hc/en-us/articles/15172253980061-How-to-Withdraw-from-PRO-Account-to-the-Wallet) respaldan separar split, wallet y remesa.

### B3 — Efecto económico que sí puede afirmarse sin simular

Sea `J=1{receipt externo positivo}`, I=activación pagada y `C_path` todos los costes personales del attempt. Entonces `q_π=P(J=1)`, `W_π=E[c|J=1]`, `EV_attempt,π=E[Jc−C_path]=q_πW_π−E[C_path]`; J≤I. La factorización de fases usa probabilidades **condicionales**, no presume independencia entre ellas. Registrar por separado `P(account_open_at_receipt|J=1)`; no equivale a survival indefinida.

| Policy | q y expected attempts | Cash condicional / survival / EV |
|---|---|---|
| MAX_ELIGIBLE | El monto máximo no crea eligibility; bajo mismos tiempos y settlement flat, cambiar R dentro del allowed set no cambia q antes del primer receipt | Mayor R aumenta cash en ese mismo estado si fees netos son monótonos; deja menos colchón y el payout fuerza F=0. No deducir de esto optimalidad global ante otros tiempos/policies |
| WAIT_FOR_BUFFER | Expone más tiempo a ruina antes de retirar; un threshold de buffer no es payout por sí mismo | Busca split 80% y continuidad; cash condicional depende del exceso observado al decision time y fees. Survival al receipt bajo flat/sin fallos operativos se conserva; survival posterior no modelada |
| CLOSE_INSIDE_BUFFER | Puede convertir caminos que fallarían antes de buffer en éxitos. Sólo bajo mismo path acoplado, mismos decision times y settlement ideal, con fallback sobre buffer idéntico, el evento de éxito de WAIT está contenido en el de CLOSE | En rutas de cierre, survival de cuenta =0 aunque haya cash; split 50%/80% y fees pueden producir menos cash condicional. La selección de paths cambia W; no hay ranking general de EV |

Con attempts IID y q>0, `E[N_attempts]=1/q`, `E[failures_before_success]=(1−q)/q`, `P(no withdrawal in n)=(1−q)^n`. Con costes de duración aleatoria, no reemplazar `E[C_path]` por F+A constantes. Si rewards/costs por attempt son integrables y los attempts son IID hasta éxito, `E[cash acumulado hasta éxito]=EV_attempt/q`; incluye el coste del intento exitoso. q=0 ⇒ espera infinita, no dividir por cero. Cohortes con fechas progresivas, promociones que expiran, distintos calendarios o presupuesto limitado no son IID; reportar simulación/recursión por calendario y no usar geometric por defecto.

### B4 — Límite documental del buffer

La fuente oficial fija buffer 52,000 y cierre obligatorio para retirar dentro de él, pero la frase sobre 80% del total no da una ecuación inequívoca del monto máximo conservando cuenta. El draft anterior tampoco aportaba una frase explícita del balance/floor post-retiro. Por eso `R=B−2000` queda como escenario conservador `RETAIN_BUFFER`, no certificación de todo `AllowedRequests`. [Profit Split & Withdrawal Rules](https://takeprofittraderhelp.zendesk.com/hc/en-us/articles/15172219527581-PRO-Account-Profit-Split-Withdrawal-Rules).

Pregunta concreta antes de certificar la fila TPT de reglas completas: **«En un PRO 50K con balance $52,500 y MAB ya fijo en $50,000, ¿cuál es el máximo débito bruto retirable manteniendo el PRO abierto: $500 o más? ¿Qué balance y MAB quedan después? Con balance exactamente $52,000, ¿hay algún monto positivo retirable sin cerrar? Confirmen también el mínimo PRO→wallet y que las tablas ≤60/>60 cuentan días con trading efectivo desde activación PRO».** No se contactó al vendor. La unidad trading days y el corte 60/61 ya están congelados por owner; se pide definición operativa fina, no reabrir ese freeze.

### C — PricingSnapshot y contabilidad temporal

Contrato conceptual separado: `snapshot_id/version`, provider/product, `captured_at=2026-09-24`, currency USD, source_refs, confidence, evaluation_initial, renewal_amount, renewal_calendar, activation_amount, taxes/other_personal_costs, promo_code, purchase_eligibility_window, entitlement_scope, evidence_status. `PropRuleSet` referencia eventos de cobro/cancelación y entitlement; no contiene precios promocionales como semántica permanente. Una compra conserva su snapshot/entitlement; nuevos attempts no heredan descuentos salvo que el escenario lo declare elegible.

| Snapshot requerido | Compra | Renovación mientras evaluación siga activa | Activación | Semántica |
|---|---:|---|---:|---|
| `TOPSTEP_STANDARD_CURRENT` | 49 | 49 cada 30 días desde compra | 149 | Snapshot actual del path Standard; no afirmar tarifa eterna ni plan sin activation. No DLL add-on |
| `TPT_LIST` | 170 | 170 cada mes calendario | 130 | Escenario list congelado; evidencia original MEDIUM, derivado de promos oficiales, no promover a captura directa |
| `TPT_NOFEE40_SNAPSHOT` | 102 | 102 cada mes calendario para compra elegible | 0 | NOFEE40, descuento y waiver ligados al entitlement comprado; no extender automáticamente a futuras compras |

Fuentes reutilizadas de D5.2: [Topstep pricing](https://help.topstep.com/en/articles/14289835-topstep-pricing-and-payment-questions) y [NOFEE40 FAQ](https://takeprofittraderhelp.zendesk.com/hc/en-us/articles/29660646764445). No se vuelve a validar todo el pricing de firmas; estos son escenarios al corte, no cotizaciones futuras. Reset/recovery queda fuera del attempt base: después de burn, cancelar evaluación y comprar un attempt nuevo. La firma no siempre cancela por burn; la cancelación es una acción de policy que evita renovaciones posteriores, no un hecho de RuleSet.

`C_path = F_initial + Σ_{r∈renewals_before_cancellation}F_r + I·A + other_personal_costs`. La activación sólo se cobra cuando ocurre; PnL nominal no paga fees personales. El reloj de renovación es calendario, aunque no se haya operado ese día. Declarar timestamps, cancelación por pass y por burn, timezone de billing y convención de aniversarios de meses cortos. Si la fuente no fija simultaneidad exacta entre pass/cancel y rebill, el escenario debe fijar `billing_tie_order` y reportar sensibilidad de un cargo; no decidirlo por orden accidental del event loop.

Identidad de control en el mismo path TPT y misma policy, con n renovaciones, activación I y misma remesa: `K_NOFEE40−K_LIST=68·(1+n)+130·I`. Cambiar sólo pricing conserva todos los estados nominales, días y q cuando no hay restricción de presupuesto y las policies no dependen de cash personal. Si cambia q, hay acoplamiento indebido o un budget rule que debe declararse. No restar los $130 waived otra vez como rebate. Fees de payout pertenecen al settlement/fee schedule referenciado; no son comisiones de trading.

El structural null v1 **excluye comisiones/slippage nominales en ambas firmas** para preservar la auditoría de martingala y comparabilidad, como permite R6 del manager. Se conservan fees personales de compra, renovación, activación y remesa. Resultado se etiqueta `STRUCTURAL_NULL_ZERO_EXECUTION_COST`; no llamarlo cash EV real neto de ejecución. Un futuro coste nominal convierte la martingala gross en supermartingala neta y requiere schedule comparable, cuándo se cobra por fill/add/close y test de contabilización única.

### D — TPT operational compatibility gate

**Clasificación para el target actual Echo Futures: `ECONOMICS_ONLY`.** El proyecto busca ejecución automatizada y escalable; las reglas PRO prohíben bots/algos y requieren ejecución manual. Una autorización limitada de copia entre cuentas propias mediante herramientas aprobadas no aprueba señales ejecutadas automáticamente, adds algorítmicos ni un copier custom de Echo. Evidencia oficial reconsultada el 2026-09-24: [PRO Account Rules](https://takeprofittraderhelp.zendesk.com/hc/en-us/articles/15171769361053-PRO-Account-Rules), actualizado 2026-09-22, y [Trade Copier Policy](https://takeprofittraderhelp.zendesk.com/hc/en-us/articles/34431176505245-Trade-Copier-Policy).

No se elige `DROP_TIER1`: la comparación económica solicitada sigue siendo útil. `MANUAL_REFERENCE_ONLY` requeriría que el owner adopte un objetivo manual y una herramienta aprobada concreta; no se asume ese cambio. `AUTOMATION_COMPATIBLE` carece de respaldo. Esta clasificación económica es final para el scope actual y no necesita inventar permiso ni esperar al vendor. Para una futura propuesta de integración, el gate de esa **variante** será `BLOCKED_VENDOR_CLARIFICATION` hasta respuesta escrita: **«¿Permiten en PRO 50K que Echo/NinjaTrader genere y ejecute automáticamente entradas, adds, exits y gestión de órdenes? Si sólo admiten referencia manual, ¿qué acciones de gestión pueden automatizarse y está aprobado explícitamente nuestro copier custom/versionado, o debemos usar uno de su lista?»** Sin respuesta afirmativa específica se mantiene exclusión de automatización; no se envió la pregunta.

### E — Acceptance tests nuevos, evidencia y oráculo

Son requisitos propuestos; **ninguno se declara ejecutado** en este mandato sin código. Mantener T1–T8 sobre D4 legacy; añadir los siguientes sin cambiar sus resultados certificados.

| ID | Caso / oracle | Aceptación esperada |
|---|---|---|
| S01 static-barrier limit | Sesiones/gates/trailing/flatten off o primer V→∞; conservar política D4 | Integral de flujo upper = `(x−a)/(b−a)`; media de tiempo de salida Brownian en varianza `(x−a)(b−x)`; T1–T4 recuperados, eval +3000/−2000 =0.4 |
| S02 zero/no-update | K0; boundaries sólo de observación; floor-update off | K0 identidad, sin contador ni RNG/acción de negocio; `K_{u+v}=K_uK_v`; floor fijo. No exigir equivalencia D4 si todavía hay liquidación forzada |
| S03 finite-horizon mass | Kernel 1D serie/flujo, varios x y V | `∫k_V+∫_0^V(f_a+f_b)=1`, no masa negativa, endpoints condicionados interiores. Validar ley conjunta tiempo/lado, no sólo win rate |
| S04 EOD monotonic | B EOD: 0→800→300→2200→1000, sin breach previo | F: −2000→−1200→−1200→0→0. Ganancia unrealized que se pierde antes de EOD no eleva floor EOD |
| S05 locked trail | Alcanzar lock en EOD o PRO y luego subir/bajar equity sin breach | F=0 permanentemente; trades/días/payout no lo bajan. XFA payout fuerza 0 aun si antes era negativo |
| S06 Topstep consistency | Días [1650,1350]; [1800,1200]; luego +300; fixture provisional de día aún abierto | Primer caso pass por igualdad 55%; segundo no pass con P=3000; tercero P=3300, A=1800 sí. Pérdidas no reducen A; target ≥3000 y fórmula A/.55 sin redondeo |
| S07 TPT consistency | Días [1500,1000,500] vs [1500,1000,500.01]; [1400,900,700] | 50% exacto no pass; >3000 en segundo sí; tercero P=3000 y best<1500 sí. Dos días nunca bastan; target no es absorción intradía |
| S08 activity/winning | XFA días netos [150,−50,149.99,200,150,150,150] | W=5 tras siete días; una sesión con 100 trades sólo incrementa una vez. Pico intradía≥150 y EOD<150 no cuenta; quinto día no elegible antes de publication. Día sin actividad/transferencia no cuenta |
| S09 PRO intraday max | Path E:0→1000 unrealized→500 realizado→−1000; otro path llega a 2000 | F:−2000→−1000→−1000 y breach en −1000, aunque EOD posterior hipotético recupere. En segundo lock0 al tocar 2000, sin esperar EOD. Add/close preservan M |
| S10 drawdown analytical | Equity Brownian constante, sin EOD/fees ni controles intermedios, M0=E0=0 | Antes de drawdown D, `P(M_τ≥m)=exp(−m/D)`; llegar al lock m=D tiene prob. e⁻¹. Con target T≥D y lock floor0, `P(hit T before burn)=e⁻¹·D/T`. No confundir con q del ruleset |
| S11 self-financing/null | Adds de T2/T3 con cierres finitos; comparar balance antes/después y martingala detenida a horizonte fijo | Y_before=Y_after; `E[E_{t∧τ}]=E0`; segundo momento igual a varianza integrada esperada. No exigir p_trade=.5 si terminal ahora incluye EOD interior |
| S12 cash identity | TS B=5000 ⇒ R=2000, split .9 y fee0; TPT ejemplos B2; dos callbacks del mismo request | TS B'=3000, c=1800, F'=0. En todos `K=−C_path+Jc`, sin 50K como cash; un solo débito y crédito. Request/aprobación/wallet con J=0; receipt externo positivo J=1 |
| S13 closure/age | PRO age 60 vs61, profit positivo, misma petición inside-buffer; fines de semana y días Test | Split .5 vs .8, PRO cerrado para siempre, cash puede recibirse; días calendario, Test e inactividad no inflan edad. Ningún cierre se etiqueta éxito antes del receipt |
| S14 pricing identity | TPT list vs promo, paths y stream emparejados, n renovaciones | `ΔK=68(1+n)+130I`; q, equity y días idénticos sin budget. TS 30d ≠ TPT mes calendario; burn cancela por policy, no por cancelación ficticia de firma |
| S15 chronology | DST, early close, news cut, carry a publicación en sesión siguiente, snapshot repetido | Flat en cortes, sin eventos fantasma ni día duplicado; tiempos RNG conservados; nunca operar con snapshot obsoleto al solicitar |
| S16 isolation/reproducibility | Mismo seed+versiones; delta0 vs null; delta≠0 con session model | D5 idéntico consigo mismo; delta0 misma ruta null; delta≠0 rechazado. D4 legacy T7/T8 intactos |
| S17 policy coupling | Mismos paths/decision schedule/settlement ideal para WAIT y CLOSE con fallback idéntico | Cada path exitoso WAIT también exitoso CLOSE, salvo fallo de implementación del coupling. No imponer orden a W ni EV; supervivencia de rutas cerradas=0 |
| S18 incomplete/IID | Guard de tiempo antes de terminar; cohortes IID fixture q=.1 y calendario progresivo distinto | No convertir alive/pending en BURNED ni excluirlos del denominador. Para N intentos, S recibidos y U sin resolver: q∈[S/N,(S+U)/N]. Geometric sólo en modo IID; q=.1 exclusivamente fixture |

S10 se deriva de la distribución del máximo antes de drawdown Brownian y del hitting estático después de lock; referencia primaria de control: Landriault, Li y Zhang, [On the Frequency of Drawdowns for Brownian Motion Processes, §2](https://arxiv.org/abs/1403.1183). La composición `e⁻¹D/T` es derivación de este diseño, no cifra de la firma. Hace falsable el tratamiento del máximo incluso cuando los endpoints de sesión parezcan razonables.

**Límite de validación analítica:** las piezas 1D, martingala a horizonte fijo, ratchets deterministas, contadores/consistencia, ledger y límite S10 son analíticamente comprobables. No se dispone aquí de fórmula cerrada para el q completo de sesiones + adds + trailing + políticas + calendario. Una comprobación del ledger y de media cero no certifica ese q.

**Oráculo numérico independiente propuesto:** resolver la ecuación backward de difusión mediante cadena Markov/finite-volume en retícula de `(e,m)` para PRO, y 1D para EOD, con operadores explícitos de add/close/fin de día y backward induction sobre los estados diarios discretos. No reutilizar el sampler ni su función de crossing probability. Comparar primero sin adds, luego un add y finalmente ciclos cortos de 2–7 sesiones con consistencia/withdrawal. Las ventanas deterministas y estados de políticas son los mismos; la representación del proceso y RNG deben ser independientes. Alternativa de contraste adicional: Brownian bridges condicionadas en malla refinada, conservando orden y máximos; un Euler de pasos más pequeños solo no certifica ausencia de cruces omitidos.

Para cada oracle usar mallas Δ, Δ/2, Δ/4 y ampliar dominios truncados; imponer barreras absorbentes desplazadas hacia dentro/fuera para acotar sensibilidad a no alineación. Si no se demuestra una cota rigurosa, etiquetar la estimación de error como empírica, no exacta. Las políticas sobre regiones abiertas (consistencia `<`) requieren ensayos de ambos lados. Congelar presupuesto propuesto `ε_num≤10⁻⁴` para probabilidades y `≤$0.01` para medias cash de fixtures acotadas; validar que el resultado sea estable dentro de él antes de usarlo. Para comparación Monte Carlo analítica aceptar `|p_hat−p|≤5√[p(1−p)/N]+ε_num`; con oracle usar incertidumbre del oracle más MC, sin absorber un sesgo sistemático aumentando sólo N. La revisión puede ajustar presupuestos por justificación, pero el coding agent no puede eliminarlos.

A horizonte no acotado, reportar masa pendiente y extender horizonte hasta cota declarada, o dejar `INCOMPLETE`. Un technical guard de D4 no se transforma en timeout económico. Si el experimento introduce un plazo de abandono, es otra policy con outcome `ABANDONED` y costes explícitos. No publicar `1/q`, cash hasta primer retiro ni EV infinito-horizonte desde runs censurados como si todos hubieran terminado.

### F — Bloqueos remanentes y handoff sin matemática implícita

| Pendiente | Impacto y responsable de resolución |
|---|---|
| Revisión del kernel conjunto, frontera de máximo, sampler/evaluador y presupuesto de error | `MATH_REVIEW` antes de freeze; diseño propuesto, no certificación numérica. Elegir método técnico que realice la ley ya definida; si no viable, devolver al diseño |
| Aceptación owner de v1 | Gate sigue REVIEW; incluye policy de trading/retiro EOD, structural null con coste nominal0 y TPT economics-only. Ninguna SPEC ni implementación autorizada por este gate |
| Escenarios concretos de ν/TradePolicy/calendario | Inputs obligatorios sin defaults inferidos del hitting kernel D4; congelar matriz de sensibilidad y calendario/tzdb antes de ejecutar resultados. No requiere suponer edge |
| `AllowedRequests` TPT sobre/en buffer y mínimo PRO→wallet | Pregunta B4 pendiente; puede estudiarse `RETAIN_BUFFER` como escenario declarado, pero no certificar como regla completa ni elegir policy económicamente superior |
| Billing y publicación/settlement | Fijar timestamps/perfil, convención meses cortos y empates rebill/cancel; snapshot TPT usa balance publicado. Latencias/fallos no medidos sólo pueden ser escenarios condicionados, no «q real» |
| Schedules de ejecución comparables / scaling completo | No bloquean structural null explícito con exposición conservadora; sí bloquean proclamar economics neta real o implementar scaling no capturado |
| Integración TPT automatizada | Excluida por `ECONOMICS_ONLY`; no bloquea research matemático. Una variante manual o custom necesita gate propio y permiso vendor explícito donde no esté documentado |

R1–R6 del review anterior: R1 resuelto por freeze; R2 clasificado ECONOMICS_ONLY; R3 contratos y policies propuestos con B4 abierto; R4 snapshots definidos; R5 diseño entregado, revisión matemática pendiente; R6 structural null zero execution cost propuesto explícitamente. Ningún resultado económico ni ranking de policies fue calculado. Permanece el estado del gate de captura D5.2 hasta aceptación owner; este trabajo no lo acepta por sustitución.

**Handoff autorizado ahora:** revisar matemáticamente esta sección y resolver los inputs/fuentes materiales listados. **No iniciar Functional/Technical SPEC, código ni experimentos en este mandato.** `D5_SESSION_MODEL_PASS = REVIEW`. `Next action = MATH_REVIEW`. Agents-OS actualizado: **sí, continuidad y change_log dentro del planner único; core/journal externo/tarea puente intactos por alcance expreso**.


## Manager Decision — D5.3 ready for GOD math review — 2026-09-24

**Verdict:** READY_FOR_GOD_MATH_REVIEW. No implementation authorized.

### Manager assessment

- The selected 1D finite-horizon killed-Brownian kernel is the correct class of model to preserve first-event/survival semantics at EOD; counters layered on D4 would be invalid.
- The technically dangerous surface is the TPT PRO process `(equity, running_max)` with intraday trailing floor and the diagonal/max boundary condition. This must be independently validated before any SPEC freeze.
- D5 introduces a new sensitivity input absent from D4: session variance `ν`. Under finite horizons, q and day-count outcomes depend on `ν`; D4 cannot identify it. D5 results must therefore be reported as `q_withdraw(ν, TradePolicy, WithdrawalPolicy, calendar, settlement)` until a calibration source is explicitly introduced.
- The proposed always-in-market/reopen-until-session-close policy is a **scenario trading policy**, not a prop rule. It may be used for structural null experiments only if frozen and labeled as such.
- TPT remains `ECONOMICS_ONLY` for the automated Echo target; this does not block mathematical comparison but forbids interpreting TPT as an integration candidate.
- `AllowedRequests` TPT and vendor settlement details do not block the kernel review; they do block final rules completeness / cash-EV certification for TPT.
- No code, Functional SPEC or Technical SPEC is authorized before math review.

### GOD review must decide

1. correctness/normalization of the finite-horizon 1D killed Brownian kernel and boundary flux formulas;
2. whether the proposed event-time + surviving-endpoint sampling contract is sufficient and unbiased;
3. correctness of the `(e,m)` running-maximum formulation for TPT PRO, including the diagonal boundary condition and lock transition;
4. validity of analytical test S10 and other claimed invariants;
5. optional-stopping/martingale claims under finite sessions + adaptive bounded adds + forced EOD liquidation;
6. whether the proposed independent numerical oracle can falsify the production sampler with a defensible error budget;
7. whether the model is implementable with bounded complexity or should be simplified before SPEC freeze.

### Gate

`D5_SESSION_MODEL_PASS` remains **REVIEW**.
Next action: **GOD_MATH_REVIEW**.

## GOD Mathematical Review — D5.3

### Baseline, alcance y decisión — 2026-09-24

**Verdict: MATH_REVISE. Recommended next action: CORRECT_AND_REVIEW. `D5_SESSION_MODEL_PASS = REVIEW`.** La clase de modelo es viable. El kernel 1D, la condición diagonal del máximo y la composición analítica de S10 son correctos bajo las condiciones precisadas abajo. No hay contradicción material que reabra D4. Sí hay correcciones obligatorias en el contrato del oráculo multisesión, el presupuesto de error global, las cotas con censura y la definición del indicador de activación. No congelar SPEC hasta incorporar y revisar estas correcciones.

Autoridades leídas: [[Echo Futures]], este planner —especialmente §D5.3 y §Manager Decision—, [[Echo Futures — Simulator v0]], ambas SPECs D4 y [[echo-futures-astra-math-review]]. Baseline D4 `d4f42a41946f12231b75e4eb65b90d132731be0d` comprobado por `git rev-parse HEAD` en su checkout, sin cambios locales. Baseline documental del planner antes de esta revisión: commit `0ddb83ce`. Esta sección es la disposición vigente de la revisión; los bloques anteriores se conservan como propuesta e historia, no como aceptación posterior.

Método: derivaciones independientes de flujo, Itô, problemas backward y cambio de tiempo; contraejemplos deterministas y pequeñas evaluaciones numéricas de fórmulas, sin implementar ni ejecutar un simulador. La única consulta externa fue la referencia matemática primaria ya citada para S10; no se investigaron firmas, precios ni marketing. Ningún resultado de implementación, convergencia PDE o Monte Carlo nuevo se declara certificado.

### Blocking findings

No se encontró un BLOCKER de inviabilidad de la difusión elegida. **G53-01 a G53-04 son MAJOR y bloquean SPEC freeze** porque todavía permiten contratos de validación o identidades falsas. No son defectos que autoricen sustituir el modelo por retornos diarios. Las condiciones técnicas de G53-06 y los teoremas de las secciones siguientes deben quedar explícitos en el handoff.

### Major findings

**G53-01 — Dimensión real del oráculo de consistencia. Severity: MAJOR.**

- **Claim audited:** §E propone PDE/cadena 1D para EOD o 2D `(e,m)` para PRO, con backward induction sobre «estados diarios discretos», para comparar ciclos de 2–7 sesiones con consistencia/retiros.
- **Expected mathematics:** 1D/2D describe la difusión local entre acciones, condicionada a los demás estados. El valor económico multisesión depende también de variables continuas de historia, además de los contadores discretos.
- **Problem found:** el contrato no especifica la representación ni el error del best day A, máximo EOD H, balance inicial diario y estado de trade/policy. No son todos discretos. Contraejemplo: días `[1700,700,600]` y `[1400,900,700]` producen igual P=3000, N=3, H_EOD=3000 y F=0, pero A=1700 frente a 1400. El primero falla ambas consistencias; el segundo las satisface. Sus vecindades contienen el mismo desacuerdo, no es sólo una igualdad de probabilidad cero.
- **Corrected formulation:** declarar por separado el semigrupo local condicionado y el estado suficiente de la recursión de valor. Conservar/integrar las variables continuas de historia, mediante cuadratura, mallas adicionales o condicionamiento que mantenga su ley conjunta; refinar también esas dimensiones. No sumar P como estado independiente de e cuando son idénticos en el snapshot, pero tampoco omitir A. Un oráculo 1D/2D sin esa extensión sólo certifica fixtures locales o sin consistencia.
- **Impact on D5:** evitar que dos motores compartan una reducción de estado incorrecta y coincidan en un q sesgado; reconocer la complejidad adicional sin exigir una PDE monolítica de todas las dimensiones.
- **Blocks SPEC freeze:** sí; cerrar el alcance de validación y la representación matemática de la historia antes del freeze. No se exige implementarla en esta revisión.

**G53-02 — Error numérico local, global y de cash no son intercambiables. Severity: MAJOR.**

- **Claim audited:** §E propone `ε_num≤10⁻⁴` para probabilidades y `≤$0.01` para medias cash, comparando sampler y oráculo mediante tolerancia MC adicional.
- **Expected mathematics:** cada tolerancia debe identificar observable, horizonte, norma, acumulación por composición y fuentes de error separadas; un presupuesto por probabilidad no determina el error de una expectativa monetaria.
- **Problem found:** no se fija si 10⁻⁴ corresponde a una llamada, una sesión o al resultado completo. Con reaperturas ilimitadas no hay un número determinista fijo de llamadas. Tampoco 10⁻⁴ implica un centavo: aun disponiendo de una cota de distancia de variación total de 10⁻⁴, un payoff de rango $2,000 admite error de $0.20. Controlar sólo una probabilidad escalar es todavía más débil. Renovaciones sin horizonte acotado dan costes no acotados.
- **Corrected formulation:** fijar presupuestos globales por fixture/observable y separar `ε_prod`, `ε_oracle`, `ε_trunc`, `ε_history`, `ε_tail` y error estadístico. Con K llamadas y cotas uniformes δ_i de variación total, el error de ley se acota por `Σ_i δ_i`; con número aleatorio, justificar una cota esperada equivalente o truncar K y conservar explícitamente su masa residual. Para payoff g en `[g_min,g_max]`, `|E_P g−E_Q g|≤(g_max−g_min)·TV(P,Q)`; para costes no acotados se necesita además una cota de momento/cola monetaria. Alternativamente, controlar directamente el error débil del observable de cash.
- **Impact on D5:** un kernel preciso o una coincidencia MC no certifican automáticamente q ni el centavo prometido. Mantener las metas para fixtures acotadas es razonable; prometerlas para toda economía infinita sin una cota adicional no lo es.
- **Blocks SPEC freeze:** sí; adoptar el contrato de aceptación desglosado de §Numerical oracle verdict. El trabajo numérico posterior deberá demostrarlo.

**G53-03 — S18 confunde censura de la muestra con incertidumbre sobre q. Severity: MAJOR.**

- **Claim audited:** para N intentos simulados, S recibidos y U sin resolver, `q∈[S/N,(S+U)/N]`.
- **Expected mathematics:** ese intervalo encierra la proporción final de esa muestra, no necesariamente el parámetro poblacional q. La incertidumbre de Monte Carlo permanece cuando U=0.
- **Problem found:** con N=1, S=1, U=0 se publicaría `q=1`, aunque un modelo con q=1/2 produce exactamente esa observación con probabilidad 1/2. Es una falsificación directa de la afirmación literal.
- **Corrected formulation:** escribir `q_hat_completed∈[S/N,(S+U)/N]`. Para N fijo de attempts IID, un intervalo conservador de confianza `1−α` para q es `[max(0,S/N−η), min(1,(S+U)/N+η)]`, `η=sqrt(log(2/α)/(2N))`; también sirve la envolvente de límites binomiales exactos para todos los conteos finales entre S y S+U. Añadir incertidumbre numérica por separado. Si S y U son masas exactas de un solver, entonces sí `q∈[p_received,p_received+p_unresolved]` es una cota poblacional determinista. Tamaño muestral elegido adaptativamente exige una confidence sequence o diseño equivalente, no reutilizar sin más el intervalo de N fijo.
- **Impact on D5:** no sobrecertificar q, `1/q` ni probabilidades de no retiro. No se asume censura independiente para la envolvente pathwise; sí se requiere el muestreo declarado para su capa estadística.
- **Blocks SPEC freeze:** sí; reemplazar S18 y el contrato de reporting correspondiente.

**G53-04 — Activación ocurrida ≠ fee positivo pagado. Severity: MAJOR.**

- **Claim audited:** §B3 define I como «activación pagada» y exige `J≤I`; §C/S14 usa I en la identidad promo/lista.
- **Expected mathematics:** todo retiro implica una activación/funding anterior, aunque la tarifa de activación sea cero. El indicador de lifecycle debe ser independiente del precio.
- **Problem found:** en `TPT_NOFEE40_SNAPSHOT`, fee de activación=0. Si «pagada» significa desembolso positivo, un retiro produce J=1 e I=0; `J≤I` es falso y `ΔK=68(1+n)+130I` pierde el ahorro de activación. Si se pretendía «activación ocurrida», la definición escrita debe corregirse.
- **Corrected formulation:** `I_act=1{activación completada}`, `J≤I_act`; `C_path=F_initial+ΣF_renewal+I_act·a_snapshot+C_other`. El cash pagado por activación es `I_act·a_snapshot`, no el indicador. Para mismos paths sin restricciones de presupuesto: `K_NOFEE40−K_LIST=68(1+n)+130 I_act`. Usar otro símbolo para la tarifa evita colisión con A=best day.
- **Impact on D5:** conservar separación nominal/cash y comparaciones de pricing; ninguna modificación a D4 ni al modelo de difusión.
- **Blocks SPEC freeze:** sí; corregir definición y fixtures S12/S14. Es una corrección contractual, no investigación de pricing.

### Minor / informational findings

**G53-05 — Los empates no son universalmente de probabilidad cero. Severity: MINOR.** **Claim audited:** §A5 dice que «un empate exacto tiene probabilidad cero en el modelo regular». **Expected mathematics:** el tiempo de hitting de una barrera separada de un punto inicial interior no tiene átomo en un deadline determinista positivo; barreras coincidentes sí se alcanzan juntas con probabilidad positiva. **Problem found:** una barrera de SL puede coincidir exactamente con el floor; TP con lock también. La frase es demasiado amplia, aunque la prioridad ya propuesta es correcta. **Corrected formulation:** limitar el argumento de probabilidad cero al empate tiempo aleatorio/deadline bajo no degeneración; definir todos los empates geométricos y los estados iniciales sobre frontera mediante operadores deterministas. **Impact on D5:** conservar phase-loss > close > add; en hard close no add ni reapertura; lock se actualiza aunque coincida con TP. **Blocks SPEC freeze:** no por sí solo; incorporar la precisión sin relajar prioridades.

**G53-06 — Máximo correcto, pero ley conjunta potencialmente mixta. Severity: INFO.** **Claim audited:** §A4 usa `(e,m)`, `L=(h²/2)∂ee` y `∂m u=0` en diagonal. **Expected mathematics:** son correctos para h constante entre eventos y estado de policy condicionado; el kernel es una medida, no necesariamente una densidad 2D ordinaria. **Problem found:** ninguno en esas fórmulas. Hay una trampa de implementación: partiendo de e<m, sobrevivir sin volver a m tiene probabilidad positiva y deja masa en `m_final=m_initial`. Con h=0 aparece además una masa puntual de identidad. **Corrected formulation:** preservar explícitamente esas componentes, fronteras de evento y transición al lock; no normalizar sólo una densidad respecto de `de dm`. **Impact on D5:** requisito del sampler/oráculo, detallado abajo. **Blocks SPEC freeze:** no es una refutación del modelo; el contrato de realización debe incluirlo.

**G53-07 — S10 es exacto con dos tiempos de muerte diferentes. Severity: INFO.** **Claim audited:** cola exponencial del máximo y `e⁻¹D/T` tras lock. **Expected mathematics:** la exponencial para todo m pertenece al drawdown sin cap; el proceso con floor bloqueado cambia esa cola después de D. **Problem found:** la composición propuesta para T≥D es correcta; no debe convertir la primera expresión en un test del proceso capped para m>D. **Corrected formulation:** usar `τ_D` para drawdown sin lock y `ζ` para muerte con lock; fórmulas y extensión a T<D abajo. **Impact on D5:** conservar S10 como control independiente, con nombres y condiciones explícitos. **Blocks SPEC freeze:** no por sí solo.

**G53-08 — Martingala nominal local, no identidad de lifecycle con resets/retiros. Severity: INFO.** **Claim audited:** media nominal cero con adds, sesiones y flatten. **Expected mathematics:** verdadera para la integral de trading detenida; evaluar condicionalmente desde el inicio de cada fase o llevar ganancias acumuladas sin borrar historia. **Problem found:** ninguno para el proceso declarado; sería falso aplicarlo al saldo que se reinicia al activar o se debita al retirar, o al subconjunto de sobrevivientes. **Corrected formulation:** exposición predecible, acotada y sin anticipación; transferencias/reset separados de `∫H dS`; condiciones de stopping explicadas abajo. **Impact on D5:** sizing puede cambiar q sin crear drift. **Blocks SPEC freeze:** no.

**G53-09 — Consistencia determinista válida; igualdad exige contrato explícito. Severity: INFO.** **Claim audited:** Topstep `P≥3000,N≥2,A≤.55P`; TPT `P≥3000,N≥3,A<.50P`. **Expected mathematics:** predicados válidos sobre snapshot cerrado. **Problem found:** ninguno en los predicados. Brownian continuo no garantiza que toda variable derivada carezca de átomos: killing, stopping por policy, redondeo de requests y días sin exposición pueden crearlos. **Corrected formulation:** conservar exactamente `<` frente a `≤`; no usar probabilidad cero ni epsilon favorable para borrar la diferencia. **Impact on D5:** S06–S08 siguen obligatorios, incluida igualdad exacta. **Blocks SPEC freeze:** no.

**G53-10 — ν es familia de relojes, no calibración implícita. Severity: MINOR.** **Claim audited:** `q_withdraw(ν,TradePolicy,WithdrawalPolicy,calendar,settlement)`. **Expected mathematics:** depende de la varianza por ventana y su correspondencia con decisiones de calendario; un único escalar basta sólo bajo una forma temporal y asignación entre ventanas ya congeladas. **Problem found:** la notación abreviada puede ocultar grados de libertad que §A3 sí admite al definir σ piecewise constant. **Corrected formulation:** interpretar ν como vector/perfil de varianzas de ventanas, o como multiplicador de un perfil determinista versionado. **Impact on D5:** sensibilidad reproducible sin inventar volatilidad; matriz mínima abajo. **Blocks SPEC freeze:** no como fórmula abreviada; sí deben declararse los inputs de cualquier experimento concreto.

### 1D kernel verdict

**Aceptado.** Sea `ℓ=b−a`, `r=(x−a)/ℓ`, `λ_n=n²π²/(2ℓ²)`. En reloj de varianza de PRECIO, el generador es `½∂yy` y:

`k_V(x,y)=(2/ℓ) Σ_{n≥1} sin(nπr) sin[nπ(y−a)/ℓ] exp(−λ_n V)`.

Es una densidad subprobabilidad, no una densidad ya normalizada a 1. La ortogonalidad de los senos produce la identidad inicial en sentido débil. Para V>0 la serie resuelve la ecuación de calor con Dirichlet en a,b. Su masa es:

`Q_x(V)=∫_a^b k_V(x,y)dy=(2/π) Σ_{n≥1} [(1−(−1)^n)/n] sin(nπr) exp(−λ_n V)`.

Los flujos propuestos tienen signos y factores correctos. En forma explícita, por unidad de varianza:

`f_a(v|x)=+(1/2)∂_y k_v(x,a+)=(π/ℓ²) Σ_{n≥1} n sin(nπr) exp(−λ_n v)`.

`f_b(v|x)=−(1/2)∂_y k_v(x,b−)=(π/ℓ²) Σ_{n≥1} (−1)^(n+1) n sin(nπr) exp(−λ_n v)`.

Aunque los sumandos cambien de signo, las funciones completas son no negativas. `Q'_x(v)=−f_a(v|x)−f_b(v|x)`; por tanto `Q_x(V)+∫_0^V(f_a+f_b)dv=1`. La normalización incluye ambas masas de salida, no sólo el endpoint.

Las probabilidades acumuladas, útiles para evitar integrar una serie mal condicionada en v=0, son:

`U_x(V)=P(τ≤V,exit=b)=r−(2/π)Σ_{n≥1}[(−1)^(n+1)/n]sin(nπr)exp(−λ_n V)`.

`L_x(V)=P(τ≤V,exit=a)=1−r−(2/π)Σ_{n≥1}[1/n]sin(nπr)exp(−λ_n V)`.

Así `U_x(∞)=r` y `L_x(∞)=1−r`, recuperando D4. La integración término a término hasta v=0 requiere límite/regularización; no justificarla por convergencia absoluta allí. El tiempo medio de salida es `(x−a)(b−x)` en varianza de precio. En coordenadas de EQUITY con `de=h dW_v`, usar `h²V` en el kernel unitario o coeficiente `h²/2`; en calendario, el flujo se multiplica por `σ²(t)`. No multiplicar dos veces por h² ni confundir varianza de precio con varianza de equity.

**Ley conjunta suficiente:** es una mezcla disjunta de `f_a(v)dv δ_a`, `f_b(v)dv δ_b`, para `0<v≤V`, y `k_V(x,y)dy` con etiqueta `τ>V`. No existe un endpoint superviviente que haya que muestrear también en la rama de salida. Muestrear primero esas tres masas y luego tiempo condicionado al lado, o primero tiempo condicionado a salida y lado según `f_b(v)/(f_a(v)+f_b(v))`, da la ley correcta. En la rama superviviente usar `k_V/Q_x(V)`. No usar r para elegir el lado independientemente de la duración finita.

**Límites:** V↓0 desde x interior da Q→1 y `k_V dy⇒δ_x`; las masas de salida tienden a 0. V→∞ da Q→0 y salida eventual cierta con masas r,1−r; el endpoint condicionado a supervivencia rara converge a `(π/(2ℓ))sin[π(y−a)/ℓ]dy`. Para V>0 fijo y x↓a, salida lower→1, tiempo→0, Q→0; x↑b es simétrico. Exactamente en una frontera, absorber a tiempo 0 antes de llamar al kernel interior. Los límites conjuntos x→frontera y V→0 no son uniformes: no sustituirlos por una tolerancia de empate.

**Evidencia aritmética independiente, no certificación de sampler:** a=0,b=1,x=.25,V=.1 da Q=.553175891850086, L=.429195269138053 y U=.0176288390118612; suman 1 a precisión de máquina. La masa upper eventual es .25, muy distinta de su masa antes de V. Con V=1, Q=.0064749699291492, L=.746762514183855, U=.246762515886996. Evaluaciones de las series con 1,000 términos; no prueban estabilidad uniforme para V pequeño o puntos casi absorbidos. La realización deberá cambiar de representación, por ejemplo imágenes para tiempos cortos y espectral para largos, con cotas de truncación y sin clipping silencioso.

### Session composition / event semantics verdict

**Aceptado con estado aumentado.** Brownian tiene strong Markov en los tiempos de hitting. En cada tramo se congela h y el estado que determina barreras; al ocurrir un evento se aplica la acción no anticipativa, se consume su τ de varianza y se vuelve a condicionar desde el estado alcanzado. El calendario, fase, trade/add index, floor, historial diario y policy tienen que formar parte del estado de control. `(e,m)` solo no vuelve Markov a cualquier estrategia adaptada con memoria omitida.

Los resets de precio relativo `s←0` al reabrir son cambios de coordenadas; no resetean equity de fase, máximo, reloj ni historial de días. Al hard close, una supervivencia se liquida en su endpoint condicionado. En una frontera meramente observacional se aplica Chapman–Kolmogorov; al liquidar y reiniciar trade/adds se compone semigrupo con un operador económico, y no se exige la misma igualdad que sin esa acción.

La política de referencia de G,L positivos fijos, h acotado, lista finita de adds y cortes exógenos localmente finitos no explota en una sesión: cada trade completo mueve la equity continua desde su apertura por G o −L. La continuidad uniforme en un horizonte compacto impide infinitos movimientos consecutivos de tamaño al menos `min(G,L)>0`; hay sólo finitos adds por cada trade. Una futura política con targets decrecientes a cero no hereda esta prueba y necesita una condición de no explosión propia. Un guard informático no puede etiquetar el resto como burn.

En EOD, breach frente al floor vigente se resuelve antes de flatten/snapshot. El ratchet `F_new=max(F_old,min(0,B_close−D))` no crea PnL. Para un sobreviviente con D>0 tampoco lo quema por sí solo: si el candidato nuevo es B_close−D está debajo del saldo; si llega a 0, B_close≥D; si no sube, el sobreviviente ya estaba sobre F_old. La revalidación sigue siendo útil como invariante y para transferencias separadas. PRO no recibe un segundo ratchet EOD.

### TPT PRO running-max verdict

**Aceptado; no corregir la diagonal a reflexión normal.** Antes de lock, `Ω={(e,m):0≤m<D, m−D<e≤m}`. Con coeficiente h fijo entre eventos:

`dE_v=h dW_v`, `M_v=max(m,sup_{s≤v}E_s)`, `dM_v≥0`, `1{E_v<M_v}dM_v=0`.

El par es strong Markov para el segmento condicionado. Para u suave, Itô da `du=h u_e dW_v+(h²/2)u_ee dv+u_m dM_v`. Puesto que dM vive en E=M, el dominio backward tiene `u_m(m,m)=0`. **No** es `u_e=0`, ni `u_e+u_m=0`, ni una condición de flujo forward que pueda copiarse sin derivación. Para valor terminal g y tiempo restante v, la ecuación interior es `∂_v u=(h²/2)u_ee`, con dato inicial g, dato absorbente/cemetery en `e=m−D` y datos de evento/continuación donde corresponda. En formulación por tiempo calendario hacia delante del contrato, es `∂_t u+(h²σ²(t)/2)u_ee=0`.

Control de coordenadas: para gap `d=m−e` y `w(d,m)=u(m−d,m)`, la condición es `w_d(0,m)+w_m(0,m)=0`; imponer `w_d=0` salvo que w sea independiente de m cambiaría el proceso. Esta identidad es útil para auditar una formulación alternativa del oráculo.

Al llegar por primera vez a m=D, la continuidad exige E=D. Desde `(D,D)` el floor queda en 0. El valor se empalma con la solución locked 1D; para límites desde estados `(e,m)` con m↑D y e<D, la traza compatible es el valor locked iniciado en e. No se absorbe el path como éxito salvo que un target analítico independiente lo mande. El máximo puede descartarse para reglas de primera extracción sólo si ninguna policy retenida lo consulta; floor/locked y demás historia relevante permanecen.

Adds y close/reopen conservan E, por tanto M. Cambiar h cambia la velocidad de varianza futura, no el máximo ya recorrido. Un reset de fase sí inicializa una cuenta/fase nueva según contrato; no confundirlo con cerrar un trade. En flat, E y M quedan constantes. Retiros son saltos de débito separados y no reducen el floor histórico.

**Competencia de eventos:** detener en el primer hit del conjunto drawdown ∪ SL ∪ TP ∪ add ∪ lock, o integrar lock como transición interna equivalente. Evaluar el máximo hasta ese instante, no el máximo hipotético posterior de toda la sesión. El floor móvil puede interceptar un descenso antes del add que era elegible al inicio; no basta calcular un floor estático al abrir el segmento. En un empate de pérdida con SL/add, domina pérdida. En TP=lock, conservar lock además de cerrar; en el deadline no reabrir. Las condiciones de boundary rewards se ponen sólo en las fronteras alcanzables antes de otras absorciones.

**Realización viable sin tiny Euler:** resolver/invertir el semigrupo o resolvente con esas fronteras y sus medidas de salida, o usar una construcción de excursiones/bridges con control del primer cruce. El dominio pre-lock está acotado (`−D<e<D`, `0≤m<D`), aunque la PDE es degenerada. Eso hace viable el problema local; no prueba un coste uniforme para todos los ν, policies o todos los estados diarios. Una malla PDE determinista puede aproximar la ley continua sin pasos Euler de paths, siempre declarando su error.

**Componente singular que debe preservarse:** si e0<m0, los paths que no vuelven a m0 mantienen M=m0. Sin otras barreras intermedias, la masa superviviente en esa línea a tiempo V es `k^{(m0−D,m0)}_{h²V}(e0,y)dy δ_{m0}(dm)`. Se añade la componente que sí actualizó el máximo y las medidas de salida. Ignorar la línea elimina probabilidad real. Desde e0=m0 y h≠0, en tiempo positivo el máximo aumenta inmediatamente casi seguramente; ello no permite ignorar la línea después de un add o una caída que deja e<m. Para h=0 el operador es identidad mientras no haya un evento determinista.

### S10 analytical oracle verdict

**Aceptado como igualdad exacta, no aproximación.** Definir por separado `τ_D=inf{v:M_v−E_v=D}` para Brownian sin cap y `ζ=inf{v:E_v≤min(0,M_v−D)}` para el proceso con lock. Sin otros stops ni horizonte finito, empezando E=M=0:

`P(M_{τ_D}≥z)=exp(−z/D)`, z≥0.

La cola del máximo al primer drawdown en Brownian sin drift está corroborada por [Landriault, Li y Zhang, §2, ecuaciones (2.6)–(2.7)](https://arxiv.org/html/1403.1183v1#S2). La siguiente derivación y el empalme capped se verifican aquí de forma independiente.

Para alcanzar un nivel c antes de drawdown, desde `m−D<e≤m<c`, la solución armónica es `u_c(e,m)=((e−m+D)/D) exp(−(c−m)/D)`. Es lineal en e, vale 0 en el floor, 1 en `(c,c)`, y cumple `u_m(m,m)=0`. En `(0,0)` da `exp(−c/D)`. Para c=D coincide con el proceso capped hasta lock, de modo que `P(lock before burn)=e⁻¹`.

Para target intradía T≥D, la continuidad obliga a pasar primero por `(D,D)`. Strong Markov da la probabilidad condicional locked `P_D(hit T before 0)=D/T`. Por tanto:

`P_0(hit T before ζ)=e⁻¹ D/T`, T≥D.

El caso T=D incluye el factor 1. Para `0<T<D`, el target puede ganar antes del lock y la fórmula correcta es `exp(−T/D)`. Para el máximo del proceso capped al morir:

`P(M_ζ≥z)=exp(−z/D)` si `0≤z≤D`; `P(M_ζ≥z)=e⁻¹D/z` si `z≥D`.

No exigir la cola exponencial más allá de D al motor capped. Con D=2000,T=3000, la probabilidad analítica de este fixture es `.24525296078096157`; la probabilidad de lock es `.36787944117144233`. Ninguna es q_withdraw del ruleset EOD.

**Condiciones:** equity continua, drift y costes nominales cero, ningún reset del máximo, target observado continuamente, sin retiro/cancelación anticipada ni gates de día. El target T≥D no puede ocurrir antes del lock; un target EOD, cambiante o condicionado a consistencia sí invalida ese argumento. Con h constante no nulo el resultado no depende de h. Con exposición predecible variable, se conserva por cambio de tiempo de martingala continua si el reloj cuadrático tiene suficiente recorrido para alcanzar la absorción —por ejemplo, exposición total en varianza infinita en paths no terminados— y no hay interrupciones de policy que eliminen outcomes. Acotación superior sola no basta: exposición apagada para siempre puede dejar paths sin resolver. h=0, deadline finito y calendario con oportunidad finita no satisfacen el fixture. Pure equity hitting/drawdown sin relojes ni otras reglas conserva esa invariancia; no atribuir un efecto de sizing a cualquier regla de path indistintamente.

**Oracle adicional sensible al tiempo, derivado del mismo boundary-value problem:** para h constante, `κ=sqrt(2λ)/|h|`, T≥D y λ>0, en reloj v de varianza de precio:

`E_0[exp(−λτ_T);τ_T<ζ]=exp[−κD coth(κD)]·sinh(κD)/sinh(κT)`.

La parte pre-lock se obtiene con `u(e,m)=[sinh(κ(e−m+D))/sinh(κD)] exp[−κ coth(κD)(D−m)]`, que satisface `Lu=λu`, kill y diagonal; la parte locked es el resolvente de hitting en (0,T). Su límite λ↓0 recupera S10. Este control sí detecta algunas leyes de duración incorrectas que el mero pass rate no detectaría. No es una fórmula directa de probabilidad antes de una sesión: obtener esa CDF requeriría inversión adicional validada. Para D=h=1,T=1.5, los valores son `.21477390832873927` en λ=.125 y `.14846893086020618` en λ=.5; calculados por evaluación de la fórmula, sin paths.

### Martingale / optional-stopping verdict

**Aceptado a horizonte finito.** Escribir la riqueza nominal de trading como `X_t=X_0+∫_0^t H_s σ(s)dW_s`. Para `|H_s|≤hMax`, exposición predecible y `∫_0^Tσ²(s)ds<∞`, la integral es una martingala cuadrado-integrable. Para cualquier stopping time τ:

`E[X_{T∧τ}]=X_0`, `E[(X_{T∧τ}−X_0)²]=E[∫_0^{T∧τ}H_s²σ²(s)ds]≤hMax²ν_[0,T]`.

«Adaptado» solo no es el contrato completo del integrando. Las decisiones de add en hitting times continuos se ejecutan con información actual y el nuevo h actúa después del evento; una exposición simple `H=Σh_i·1_(τ_i,τ_{i+1}]`, con h_i medible en `F_{τ_i}`, cumple el contrato. No usar el endpoint futuro de una bridge para decidir el add pasado.

`b'=b−Δh s`, `h'=h+Δh` da algebraicamente `b'+h's=b+hs`. El flatten sin coste cambia holdings/cash interno de trading a igual mark y desde entonces H=0. No crea drift. Reapertura self-financing conserva esa propiedad, incluida exposición adaptativa y simetría short si se habilitase. Se puede alterar la distribución y el promedio condicionado a sobrevivir; eso no es drift de la población completa.

D4 conserva la invariancia de hitting con sólo dos valores terminales fijos y stopping válido. D5 ya tiene valores interiores al EOD, trailing, gates y transferencias, de modo que `P(win)=L/(G+L)` no se obtiene de media cero para todo experimento. El sizing puede cambiar varianza realizada por sesión, distribución diaria y q_withdraw sin producir edge en la integral nominal.

No extrapolar `E[X_{T∧τ}]=X_0` a T=∞ sólo porque τ sea finito casi seguramente. Hace falta UI, stopping acotado u otra condición suficiente. Contraejemplo pertinente: una vez lockeado, Brownian desde D y floor 0, sin target ni retiro, toca 0 a.s. pero `E[X_ζ]=0≠D`; el tiempo medio de hitting es infinito y no hay UI. La familia detenida a cada horizonte finito sí tiene media D. Fees personales, resets de fase y débitos de payout son operaciones distintas y no satisfacen por sí mismos esa identidad nominal.

### Consistency / day-state verdict

**Aceptados los predicados propuestos.** En evaluación sin transferencias, `P=Σd_j`, `A=max(0,d_1,…,d_N)` con días finalizados; N cuenta sólo sesiones con actividad. Topstep permite `[1650,1350]`; TPT rechaza `[1500,1000,500]` y admite `[1400,900,700]`. `P≥max(3000,2A)` es incorrecto para TPT: se requieren separadamente `P≥3000` y `P>2A`.

No hay patología de definición al reentrar sin costes: el número de trades completos es finito a.s. bajo la política fija y la ganancia del día es la suma del realizado más el flatten final. Cien trades de un día siguen contando como un día. No se puede obtener N≥3 subdividiendo artificialmente una ventana, ni definir una sesión por el número de cierres. N cuenta actividad, no rentabilidad.

Para una política fija no degenerada y observaciones a tiempos deterministas, las distribuciones vivas de profit suelen tener densidad, lo que puede hacer nula la masa en la igualdad relevante. Ese argumento no es una licencia universal: stopping diario en un profit exacto crea un átomo, flat crea ganancia 0, los burns crean masas de frontera y las fixtures fuerzan igualdades. El contrato debe resolverlas aun cuando sean nulas en una subfamilia. No redondear equity/consistencia a centavos; el redondeo explícito de requests pertenece a otra operación.

### ν / scaling verdict

**Aceptada la familia de escenarios; rechazado un q null universal.** Dependen materialmente del reloj: exits por sesión, supervivencia/kill antes de cada close, adds ejecutados, PnL y best day, hitting del máximo/lock, winning days, p_pass, q_withdraw, duración, renovaciones y distribución de cash. El costo de compra fijo o una identidad aritmética de ledger no dependen por sí mismos de ν; el número de veces que se cobra sí puede depender.

Sea D una escala de equity y h_ref una exposición de referencia legal. Usar `ẽ=e/D`, `m̃=m/D`, `ṽ=h_ref²v/D²`, `h̃=h/h_ref`. Por ventana i, `ρ_i=h_ref²ν_i/D²` es adimensional. Permanecen ratios `G/D`, `L/D`, distancias de add `h_ref Δs/D`, profit target/D, winning-day threshold/D, buffer/D, caps/D y ratios de size. Por sí sola, `ν/D²` sería dimensionalmente incorrecta si ν está en unidades de precio² y h no se ha normalizado.

Escalar todos los niveles monetarios nominales por c y las distancias de precio por c con h fijo exige escalar ν por c²; entonces se conserva la ley de estados normalizados en las mismas sesiones. Escalar h por c y ν por 1/c² con barreras monetarias fijas también conserva la ley equivalente si se reescalan los add levels en precio y se conserva la policy normalizada. Los límites de contratos, enteros de size, tick/centavo, fees y umbrales que no se escalen rompen la invariancia. Los fees personales fijos no alteran q si las policies no consultan presupuesto, pero sí alteran cash normalizado/EV; mantener barreras y ν equivalentes no convierte snapshots económicos diferentes en idénticos.

**Grid mínimo propuesto, puramente adimensional:** para cada policy/exposición frozen, `sqrt(ρ_full)∈{0.1,0.25,0.5,1,2,4}` —equivalentemente `ρ_full∈{.01,.0625,.25,1,4,16}`— con la misma forma temporal declarada. Comparar no-add y cada política de adds requerida, y WAIT/CLOSE donde corresponda. Añadir el control h=0 sólo como fixture matemática de no exposición, no como default válido del scenario. Refinar donde cambien q o las colas de días; seis puntos no certifican monotonicidad, y q no tiene por qué ser monótono en ν bajo consistencia/ratchet.

Para early close usar el ν de la ventana realmente operable, sin renormalizar. Con noticias o publication waits, mantener un vector de ventanas y sus varianzas: igual varianza total repartida distinto entre dos ventanas con flatten/reset intermedio puede cambiar resultados. Un σ(t) distinto dentro de una única ventana sin decisiones temporales internas da la misma ley de outcomes en varianza, pero cambia el mapa a timestamps de eventos; éste importa cuando compite con billing o settlement. El grid no inventa una volatilidad empírica ni una escala de mercado.

### Numerical oracle verdict

**Independencia potencial, no certificación ya conseguida.** Un finite-volume/CTMC implementado independientemente puede falsificar un sampler espectral/semigrupo. Si producción también usa la misma PDE, stencil, interpolación o crossing routine, llamarlo «otro solver» no garantiza independencia; necesitan otra representación y controles analíticos separados. Compartir las reglas escritas es necesario; compartir un operador de transición incorrecto como única evidencia deja un fallo común. Los fixtures deterministas de ledger/consistencia y S10 deben impedirlo.

El oráculo local PRO puede construirse con saltos simétricos de equity y actualización `m←max(m,e_new)`, killing al floor y lock correcto, sin reutilizar probabilities del production kernel. Su límite debe reproducir la condición backward demostrada. No modelar el máximo mediante un Brownian independiente ni reflexión normal de un proceso 2D ordinario. Su resolución de historia multisesión es la obligación G53-01.

**Contrato de convergencia obligatorio:**

1. Refinar espacio Δ,Δ/2,Δ/4; refinar independientemente paso temporal/cuadratura/inversión y las dimensiones continuas de historia. Mostrar estimaciones y diferencias; añadir nivel si no hay régimen estable. Richardson sólo con orden observado y justificado, no asumido en esquinas/discontinuidades.
2. Alinear floor, diagonal, lock, TP/SL/add y umbrales del fixture. Cuando no sea posible, desplazar ambas direcciones y medir sensibilidad. Las barreras de supervivencia anidadas dan cotas por inclusión; mover una frontera de policy/consistencia puede no ordenar q y no debe presentarse automáticamente como bracket riguroso.
3. Pre-lock tiene dominio acotado. Para el locked/EOD no acotado, aumentar el dominio truncado y llevar masa de escape como desconocida o acotarla. No convertir un borde artificial superior en retiro ni reflejarlo sin control. Repetir con dominio ampliado y separar cola monetaria de probabilidad de escape.
4. Verificar conservación/positividad, medidas de frontera y masa singular `M=m0`; identidad a tiempo 0; semigrupo sin acciones; first-event ordering; empalme locked. Una renormalización o clipping de probabilidad no sustituye una cota.
5. Comparar distribución conjunta: sub-CDF `P(τ≤v,side=a/b)`, supervivencia/endpoint, ley de M y dependencia con E, además de q final. El mean-zero no detecta todos los errores de killing.
6. Llevar un presupuesto global de error de composición, historia, truncación y horizonte. Tres mallas estables son evidencia empírica; sin enclosure/error theorem no decir «cota rigurosa» ni «sampler exacto».

**Aceptación numérica:** conservar `ε_num_global≤10⁻⁴` en probabilidades de los fixtures locales/finito-horizonte expresamente definidos. Para cash de fixtures acotadas, `≤$0.01` es una meta separada: exigir control directo de la expectativa o distancia de ley compatible con su rango. Identidades de ledger y casos deterministas deben coincidir a la precisión aritmética del contrato, no consumir una tolerancia MC de un centavo. Una tolerancia exploratoria mayor para q completo, por ejemplo 10⁻³ absoluto, puede declararse antes de correr como screening; no satisface por sustitución el gate 10⁻⁴ ni autoriza un ranking cuya diferencia esté dentro de incertidumbre. El presupuesto de un resultado completo debe congelarse según su uso, no heredarse de un kernel.

Con referencia analítica p, usar test binomial exacto o intervalo con cobertura declarada; la regla 5σ es una aproximación aceptable cuando Np y N(1−p) son suficientemente grandes. Para p cercano a 0/1 no usar una banda degenerada de plug-in. Si el oráculo entrega `[p_o−ε_o,p_o+ε_o]`, exigir compatibilidad con el intervalo MC ampliado por el presupuesto del production sampler, manteniendo además las anchuras máximas predefinidas. Reportar por separado sesgo numérico y SE; elegir niveles/ajuste por múltiples fixtures antes de inspeccionar resultados. Para medias cash, usar SE sólo con varianza finita y un régimen estadístico defendible, o intervalos conservadores para payoffs acotados; no imponer normalidad de colas pesadas.

El 10⁻⁴ numérico NO exige SE Monte Carlo de 10⁻⁴. A modo de coste, `5 sqrt(.25/N)≤10⁻⁴` requeriría N≥625,000,000 en el peor p; MC de tamaño menor puede validar con su incertidumbre explícita, pero no demostrar por sí solo ausencia de sesgo 10⁻⁴. El presupuesto pequeño se sustenta en análisis/convergencia/control independiente, no en aceptar una banda 5σ ancha.

### Censoring / infinite attempt horizons verdict

**Aceptados pending/live separados de BURNED y el requisito IID; corregir G53-03.** Un receipt pendiente después de cerrar cuenta no es burn, ni success antes de cash. Si un settlement ideal asegura receipt eventual, puede contarse como éxito eventual lógicamente probado para un observable de horizonte infinito, pero sigue pendiente para cash recibido antes de un deadline. No mezclar esos dos observables.

Para usar geometric en ejecuciones secuenciales, cada attempt debe terminar/resolverse a.s., tener probabilidad de éxito común q>0, ser independiente de los anteriores y no depender de presupuesto/entitlements/calendario heredados. El lifecycle completo, incluidas renovaciones y settlement, forma parte del attempt. Un intento que permanece vivo para siempre puede impedir iniciar el siguiente: una sucesión hipotética de Bernoulli independientes no representa entonces la operación secuencial.

Si `N*=inf{i:J_i=1}` y los pares `(J_i,K_i)` son IID, donde `K_i=J_i c_i−C_i` incluye el intento exitoso, `E[N*]=1/q`, `P(N*>n)=(1−q)^n` y, si `E|K_i|<∞`, `E[Σ_{i=1}^{N*}K_i]=E[K_i]/q`. No hace falta independencia entre coste y éxito dentro del mismo attempt. La prueba usa que `{N*≥i}` depende sólo de attempts anteriores. Sin presupuesto suficiente para comprar indefinidamente o con purchase times dependientes de duración, no trasladar estas expresiones automáticamente al calendario real.

Para hazards de éxito variables, `P(no success through n)=∏_{i=1}^n(1−q_i^cond)`, donde `q_i^cond=P(J_i=1 | J_1=…=J_{i−1}=0)` corresponde al experimento de attempts realmente iniciables. No usar probabilidades marginales ni asumir que renovación/mes/promo preserve q. Cohortes simultáneas/copiadas requieren su dependencia conjunta.

Tiempo finito casi seguro no garantiza duración media, número medio de renovaciones ni cash medio finitos. Para cash acumulado hasta retiro se requieren integrabilidad absoluta de los costes/rewards y control de colas, además de eventual receipt y reinicio. Una pequeña masa pendiente no da un pequeño error monetario si puede seguir pagando renovaciones ilimitadas. `q_L=0` impide una cota superior finita de `1/q`; con `0<q_L≤q≤q_U`, el intervalo transformado es `[1/q_U,1/q_L]`. Para cuantiles cash con censura se necesitan bounds de CDF o masa residual suficiente; no reportar cuantiles sólo entre paths resueltos como si fueran incondicionales.

### Required corrections before SPEC

1. **G53-01:** separar dimensión de difusión local de historia multisesión; fijar estado suficiente y dimensiones/cuadraturas que el oráculo debe validar. Incluir el par de historiales con igual P,N,H,F y distinto A como negativo obligatorio.
2. **G53-02:** definir presupuestos globales de probabilidad y cash por fixture/observable; límites de composición y colas, cobertura MC, fuentes de incertidumbre separadas y qué evidencia será empírica frente a rigurosa. No exigir un sampler ya implementado para aprobar la matemática, pero sí un contrato verificable.
3. **G53-03:** reemplazar la cota literal de q en S18 por cota de completación muestral más intervalo estadístico; preservar la alternativa de masas exactas del solver.
4. **G53-04:** definir I_act por activación ocurrida independientemente de la tarifa; propagar a ledger, S12 y S14.
5. Incorporar G53-05/06: empates geométricos, componentes singulares del máximo, h=0, fronteras iniciales y endpoint condicionado. Conservar la diagonal `u_m=0`; cambiarla a Neumann normal sería un error.
6. Separar τ_D de ζ en S10; conservar condiciones de cambio de tiempo y añadir al menos un control de duración conjunta. Mantener el límite D4 sólo al desactivar efectivamente deadlines/flatten/gates pertinentes.

### Accepted analytical tests

- **S01–S03:** correctos con reloj/unidades explícitos, supervivencia más ambos flujos, y semigrupo sólo sin acción económica en el corte. Añadir sub-CDF por lado para detectar coupling incorrecto, puntos próximos a cada frontera y régimen V pequeño/grande.
- **S04–S09:** ratchets, lock, consistency, winning days y máximo continuo aceptados. Igualdades, estados iniciales de frontera y prioridades siguen siendo fixtures deterministas aunque una subfamilia tenga densidad.
- **S10:** aceptado para drawdown sin cap y composición capped tal como se distingue arriba; añadir T<D y T=D, y resolvente con λ>0. No es un oracle del q EOD completo.
- **S11:** aceptado para trading nominal de una fase o ganancias acumuladas sin resets, con exposición predecible acotada, horizonte fijo y todos los paths detenidos incluidos.
- **S12–S14:** identidades y cronología monetarias aceptadas después de corregir I_act; fixture adicional obligatoria: activación exenta, receipt positivo, `J=I_act=1`, fee de activación=0.
- **S15–S16:** cronología/determinismo y aislamiento delta aceptados. Calendario/tolerancias son inputs versionados, no una fuente de drift.
- **S17:** inclusión de éxitos WAIT dentro de CLOSE aceptada con mismo path hasta divergencia, decision schedule idéntico, fallback idéntico y settlement ideal que asegura cash positivo en cada cierre elegido. No implica dominancia de importe/EV ni sigue siendo universal con denegaciones dependientes de ruta.
- **S18:** separación de outcomes y geometric IID aceptados después de corregir el intervalo y exigir terminación/resolución de cada attempt.
- **Controles nuevos:** oráculo del máximo no actualizado, prueba de coordenadas de diagonal, invariancia de escala adimensional y negativo de estado A omitido. Son contratos analíticos para implementación futura, no tests ejecutados en esta revisión.

### Rejected/replaced analytical tests

- Rechazado `q∈[S/N,(S+U)/N]` como garantía poblacional de una muestra MC. Reemplazo: G53-03.
- Rechazado `J≤1{fee_activation>0}`. Reemplazo: `J≤I_act` incluso con waiver.
- Rechazada cualquier certificación de q con consistencia basada sólo en e o `(e,m)` y contadores enteros omitiendo historia continua. Reemplazo: semigrupos locales condicionados más recursión de estado suficiente.
- Rechazado inferir error global/cash del 10⁻⁴ de una llamada o de un pass rate; sustituir por presupuestos observables y control de composición/cola.
- Rechazados como ampliaciones indebidas, no como fórmulas realmente demostradas por el draft: cola exponencial capped para m>D; `e⁻¹D/T` a deadline EOD; invariancia general de q frente a sizing; martingala de saldos reiniciados o cash; igualdad de ley diaria inferida de mean-zero; normal incondicional en supervivencia; tiempos y lado independientes.

### Exact residual blockers / handoff

**Bloqueos matemáticos residuales de freeze:** incorporar G53-01 a G53-04 en el contrato propuesto y revisar su cierre; incluir las condiciones de realización y tests precisados. Esta revisión aporta las fórmulas corregidas, pero no marca la propuesta anterior como corregida/aceptada automáticamente. No se encontró necesidad de rediseñar la clase de proceso ni de reabrir D4.

**Inputs de escenario aún requeridos:** perfil/vector ν y grid, TradePolicy/WithdrawalPolicy, calendario de ventanas/publicación/billing/settlement y criterio de horizonte/tail. `AllowedRequests` TPT y mínimos/settlement siguen bloqueando certificación de reglas completas/cash real; no invalidan los kernels ni impiden estudiar un escenario hipotético etiquetado `RETAIN_BUFFER`/`IDEAL_COMPLIANT`. Integración TPT permanece `ECONOMICS_ONLY` y fuera de esta revisión.

**Owner gate:** no aceptado. **Gate:** `D5_SESSION_MODEL_PASS = REVIEW`. **Recommended next action:** `CORRECT_AND_REVIEW`. No Functional SPEC, Technical SPEC ni código autorizados o creados.

**Agents-OS actualizado: sí.** Change_log de esta revisión y continuidad quedan exclusivamente en esta sección del planner por mandato de alcance: dictamen, evidencia, correcciones y blockers persistidos; core, journal externo, tarea puente y baseline D4 intactos. **STOP.**


## Manager Decision — GOD MATH_REVISE accepted — 2026-09-24

**Manager verdict:** ACCEPT_FINDINGS_AND_CORRECT. D5.3 model class remains accepted in principle; SPEC freeze remains blocked only by incorporation and review of G53-01..G53-04 plus the minor contractual clarifications already enumerated by the GOD review.

### Findings disposition

- **G53-01 ACCEPTED / REQUIRED:** multisesion oracle state must carry sufficient continuous history beyond local diffusion state, including best-day history A and any other continuous path statistic consumed by consistency/policy.
- **G53-02 ACCEPTED / REQUIRED:** freeze observable-level global error budgets; local kernel tolerance cannot be promoted to end-to-end probability/cash guarantees.
- **G53-03 ACCEPTED / REQUIRED:** S18 must distinguish sample-completion bounds from population-probability uncertainty; exact-mass solver bounds remain a separate valid case.
- **G53-04 ACCEPTED / REQUIRED:** lifecycle indicator becomes `I_act=1{activation completed}`; activation cash cost is `I_act * activation_fee(snapshot)`, which may be zero.
- **G53-05/G53-06 ACCEPTED as contract clarifications:** geometric ties and singular maximum mass must be explicit in the implementation contract.
- **G53-07..G53-10 ACCEPTED as conditions/constraints:** preserve exact S10 scope, finite-horizon martingale scope, strict consistency predicates, and ν as a vector/profile or scaled deterministic shape.

### Reuse / no-redesign constraint

The correction agent MUST reuse the GOD formulas and findings. It is not authorized to select a new stochastic model, new oracle family, or alternative prop lifecycle. If a required correction cannot be integrated without changing the selected model class, return `PLAN_CONFLICT` instead of redesigning.

### Next gate

Correction target:
`D5_SESSION_MODEL_CORRECTIONS = REVIEW`

After manager review of the corrected contract:
- if all G53-01..04 are closed exactly and no new math is introduced, manager may accept `D5_SESSION_MODEL_PASS` without another GOD shot;
- if the correction changes kernel mathematics, TPT-PRO maximum dynamics, S10, martingale claims, or numerical-oracle model class, a second GOD review is mandatory.

No Functional SPEC / Technical SPEC / implementation before this correction review.


## D5.3 GOD Findings Correction — 2026-09-24

### Alcance, autoridad y resultado

Esta sección incorpora al contrato D5.3 los findings G53-01..G53-04 aceptados por el manager (§Manager Decision — GOD MATH_REVISE accepted) y las precisiones contractuales G53-05..G53-10. Supersede exclusivamente las cláusulas afectadas de §D5.3 Session Model Review (§B3 indicador de activación, §C identidad de pricing, §E contratos S10/S12/S14/S18 y presupuesto del oráculo numérico); todo lo demás del diseño permanece. La disposición matemática vigente sigue siendo §GOD Mathematical Review; aquí no se corrige ninguna fórmula del GOD review, se incorpora. Baseline certificado D4 `d4f42a41946f12231b75e4eb65b90d132731be0d` intacto; baseline documental del planner antes de esta corrección: commit `58c66326`. Clase de modelo: **SIN CAMBIO**. No hay código, Functional SPEC, Technical SPEC, ejecución de simulador, research nuevo de props ni Tier-2. No se requiere segundo GOD shot según la regla del manager: ninguna corrección toca kernel, dinámica `(e,m)`, condición diagonal, S10, semántica de martingala ni clase del oráculo. La aceptación es del manager; `D5_SESSION_MODEL_CORRECTIONS = REVIEW`.

### C1 — G53-01 CLOSED_BY_CONTRACT: estado local de difusión vs estado suficiente multisesión

Se separan dos niveles de estado que el contrato anterior dejaba implícitos.

**LOCAL DIFFUSION STATE — consumido por el kernel por llamada, entre acciones económicas:**

| Fase | Estado local mínimo |
|---|---|
| EOD/static-floor (Topstep Combine, TPT Test, XFA, PRO ya locked) | `e` (equity de fase relativa), `current_floor` F vigente, `current_trade_state` (posición h, book b, próximo add elegible, barreras TP/SL del tramo), `time_remaining` V en reloj de varianza hasta el próximo corte exógeno |
| TPT PRO pre-lock | `e`, `m` (running maximum), `current_trade_state`, `time_remaining` |

**MULTISESSION ECONOMIC/POLICY STATE — estado suficiente consumido por las reglas de lifecycle y por la recursión de valor del oráculo:** cumulative phase PnL `P`; trading-day count `N`; best closed-day profit `A`; Topstep XFA winning-day count `W`; trailing floor/lock vigentes; fase actual; activation state `I_act`; payout eligibility state; renewal/billing state; PRO age donde aplique; withdrawal/settlement state (request/aprobación/wallet/receipt pendientes).

Cláusulas contractuales:

1. `(e,m)` —ni su marginal 1D— es suficiente para el lifecycle completo. La composición strong-Markov exige el estado de control completo (calendario, fase, índice de trade/add, floor, historial diario, policy) según el GOD verdict de composición; omitir memoria hace no-Markov cualquier estrategia adaptada que la consulte.
2. Las dimensiones continuas de historia (`P`, `A`, `H_EOD`, `B_open`, relojes de edad/renovación) se representan y refinan INDEPENDIENTEMENTE de la malla de difusión local: el oráculo debe conservar/integrar su ley conjunta mediante cuadratura, mallas adicionales o condicionamiento, y refinar también esas dimensiones (Δ, Δ/2, Δ/4) en el estudio de convergencia. La elección de representación es decisión de SPEC/implantación: este contrato exige conservar la ley, no fija un algoritmo.
3. No se duplica estado: `P` no se añade como coordenada independiente de `e` cuando son idénticas en el snapshot; `A` nunca se omite.
4. **Fixture negativa obligatoria (GOD):** historiales `[1700,700,600]` y `[1400,900,700]` comparten `P=3000`, `N=3`, `H_EOD=3000`, `F=0`, pero `A=1700` vs `A=1400`; el primero falla ambas consistencias (1700>1650; 1700≥1500) y el segundo las satisface (1400≤1650; 1400<1500). Deben permanecer distinguibles (S19). Un oráculo 1D/2D sin la dimensión de historia sólo certifica fixtures locales o sin consistencia.

### C2 — G53-02 CLOSED_BY_CONTRACT: presupuesto global de error

Se elimina cualquier implicación «error local del kernel ≤1e-4 ⇒ error final de q ≤1e-4». Componentes declarados por separado: `ε_kernel` (llamada/solver local), `ε_history` (representación de historia continua), `ε_composition` (acumulación sobre K transiciones compuestas), `ε_truncation` (truncamiento de dominio), `ε_horizon` (masa no resuelta a horizonte), `ε_oracle` (residuo del oráculo independiente), `ε_MC` (incertidumbre estadística Monte Carlo).

Cada observable certificado exige un presupuesto GLOBAL declarado. Mínimo: (A) probabilidades de fixtures analíticas/locales; (B) `q_withdraw` end-to-end; (C) expected cash; (D) outputs de cola/cuantiles.

Inequality del GOD para payoff acotado g: `|E_P[g]−E_Q[g]| ≤ (sup g − inf g)·TV(P,Q)`. Una distancia de ley de 1e-4 sobre un payoff de rango $2,000 admite $0.20: NO se afirma precisión de un centavo desde un error de probabilidad 1e-4 salvo que el rango del payoff lo soporte matemáticamente.

Composición: con K llamadas y cotas uniformes δ_i de variación total, el error de ley se acota por `Σδ_i`; NO se asume cancelación. Con K aleatorio o no acotado se exige control de cola/truncamiento con masa residual explícita.

Targets semánticos congelados (no implementación): (i) fixtures analíticas locales de probabilidad retienen error global de fixture ≤1e-4; (ii) identidades deterministas de cash son EXACTAS hasta la representación aritmética y no consumen tolerancia; (iii) `q` end-to-end exploratorio puede usar una tolerancia separada declarada de 1e-3 SOLO etiquetada exploratoria/screening; no sustituye el gate de certificación; (iv) la tolerancia de certificación final se congela ANTES de observar resultados.

Todo error reportado lleva etiqueta: `RIGOROUS_BOUND` (enclosure/error theorem), `EMPIRICAL_CONVERGENCE` (estudio de refinamiento) o `MONTE_CARLO_UNCERTAINTY` (SE/IC). Sin enclosure theorem no se declara «cota rigurosa» ni «sampler exacto».

### C3 — G53-03 CLOSED_BY_CONTRACT: censura de muestra vs incertidumbre poblacional

Se reemplaza la afirmación poblacional `q∈[S/N,(S+U)/N]` por tres objetos distintos:

1. **Fracción de completación muestral:** `qhat_final_sample ∈ [S/N, (S+U)/N]` — propiedad de la muestra, nunca del parámetro poblacional q.
2. **Incertidumbre poblacional IID (q desconocido):** para N fijo de attempts IID, la envolvente conservadora 1−α del GOD queda retenida como contrato conservador válido pero NO como único método permitido: `η=sqrt(log(2/α)/(2N))`, IC poblacional `[max(0, S/N−η), min(1, (S+U)/N+η)]` con unresolved asignados conservadoramente; alternativa igualmente válida: envolvente binomial exacta sobre todos los conteos finales entre S y S+U. Tamaño muestral elegido adaptativamente exige confidence sequence o diseño equivalente, no reutilizar el intervalo de N fijo.
3. **Masas exactas de solver:** cuando S y U son masas de probabilidad reales de un solver numérico (no frecuencias muestrales), `q ∈ [p_received, p_received+p_unresolved]` SÍ es cota poblacional determinista.

Propagación obligatoria de la distinción a: evaluaciones por retiro, probabilidad de no retiro, cash acumulado y horizontes censurados. Con `0<q_L≤q≤q_U` el intervalo transformado es `[1/q_U, 1/q_L]`; JAMÁS se divide por una cota inferior `q_L=0` para emitir una estimación finita de attempts; la masa pendiente/incomplete se reporta explícita.

### C4 — G53-04 CLOSED_BY_CONTRACT: lifecycle de activación vs precio

Definiciones corregidas: `I_act = 1{activación completada}` (indicador de lifecycle, independiente del precio); `J = 1{WITHDRAWAL_RECEIVED}`; `J ≤ I_act` siempre. El débito personal de activación es `I_act · activation_fee(pricing_snapshot)`, que puede ser cero. Identidad económica corregida: `C_path = initial_purchase + renewals + I_act·activation_fee + other_personal_costs`. Fixture de pricing: bajo path de lifecycle idéntico y sin acoplamiento de presupuesto, `K_NOFEE40 − K_LIST = 68(1+n) + 130·I_act`.

**Fixture obligatoria nueva:** activación completada + activation_fee=0 + retiro recibido ⇒ `I_act=1`, `J=1`, `J≤I_act` se cumple, débito de activación=0 (S20).

Higiene de símbolos: la tarifa de activación se escribe `activation_fee`/`a_act`; el símbolo `A` queda reservado a best day. El invariant D4 legacy `J≤I` no se toca en su archivo; esta corrección rige el contrato D5.3.

### C5 — G53-05..G53-10 incorporadas sin rediseño

**G53-05 (empates geométricos):** prioridad determinista conservada: phase-loss > trade-close > add; en hard close no hay add ni reapertura; lock se actualiza aunque coincida con TP. El argumento de probabilidad cero se LIMITA al empate entre tiempo aleatorio de hitting y deadline determinista bajo no degeneración; barreras geométricas coincidentes (SL=floor, TP=lock) pueden ocurrir con probabilidad positiva y se resuelven por operadores deterministas; estados iniciales sobre frontera se absorben a tiempo 0 por operador, nunca por tolerancia.

**G53-06 (masa singular del máximo):** la ley de transición de `(e,m)` es una medida, potencialmente mixta. Desde `e0<m0`, los paths que no vuelven a `m0` conservan `M=m0` con masa superviviente `k^{(m0−D,m0)}_{h²V}(e0,y)dy·δ_{m0}(dm)`; todo sampler/oráculo futuro DEBE preservar esa línea más las medidas de salida y la transición al lock; con `h=0` el operador es identidad mientras no haya evento determinista. Prohibido normalizar sólo una densidad respecto de `de dm`.

**G53-07 (dos tiempos de muerte):** `τ_D=inf{v:M_v−E_v=D}` (drawdown sin cap) y `ζ=inf{v:E_v≤min(0,M_v−D)}` (muerte capped/locked). Fórmulas S10 idénticas al GOD review: `P(M_{τ_D}≥z)=exp(−z/D)` para z≥0; armónica `u_c(e,m)=((e−m+D)/D)·exp(−(c−m)/D)`; `P_0(hit T before ζ)=e⁻¹·D/T` para T≥D (T=D incluido); `exp(−T/D)` para 0<T<D; `P(M_ζ≥z)=exp(−z/D)` si 0≤z≤D y `=e⁻¹·D/z` si z≥D. Anclas: D=2000, T=3000 → `.24525296078096157`; lock `.36787944117144233`. Prohibido exigir la cola exponencial más allá de D al proceso capped.

**G53-08 (alcance de martingala):** `E[X_{T∧τ}]=X_0` aplica a ganancias nominales self-financing de trading a horizonte finito con exposición predecible acotada; NO aplica a saldos reiniciados al activar, saldos debitados por payout ni subconjuntos de sobrevivientes. Claims a T=∞ exigen UI/stopping acotado u otra condición suficiente.

**G53-09 (predicados estrictos intactos):** Topstep `A ≤ 0.55·P`; TPT `A < 0.50·P` con `P≥3000` y `P>2A` separados. La semántica de igualdad/desigualdad estricta se conserva EXACTA; prohibido borrarla con probabilidad cero o epsilon favorable; las fixtures de igualdad (S06/S07) siguen obligatorias.

**G53-10 (ν como familia):** `ν` es un vector/perfil de varianzas por ventana `{ν_i}` o un multiplicador escalar de un perfil determinista versionado congelado. Un escalar es INSUFICIENTE si existen múltiples ventanas con acciones de timing distintas y su forma no está congelada. Cuadratura adimensional: `ρ_i=h_ref²·ν_i/D²`; grid mínimo `sqrt(ρ_full)∈{0.1,0.25,0.5,1,2,4}`; el grid no inventa volatilidad empírica.

### C6 — Matriz de aceptación analítica reconciliada

Estados: UNCHANGED (test queda igual), CORRECTED (cláusula sustituida por la versión GOD), EXTENDED (test conservado + controles GOD añadidos).

| ID | Estado | Razón exacta |
|---|---|---|
| S01 | EXTENDED | kernel y flujos aceptados sin cambio; GOD exige sub-CDF por lado (`U_x(V)`, `L_x(V)`), puntos próximos a cada frontera y regímenes V pequeño/grande con reloj/unidades explícitos (varianza de precio vs equity; no multiplicar dos veces por h²) |
| S02 | EXTENDED | identidad semigrupo `K_{u+v}=K_uK_v` sólo en fronteras meramente observacionales sin acción económica; estados iniciales en frontera absorbidos a tiempo 0 por operador |
| S03 | EXTENDED | ley conjunta tiempo/lado ya exigida; añadir conservación con ambas masas de salida y límites no uniformes x→frontera / V→0 (prohibido sustituirlos por tolerancia de empate) |
| S04 | UNCHANGED | ratchet EOD `H_j=max(H_{j−1},B_close,j)`, `F_j=min(0,H_j−2000)` aceptado tal cual |
| S05 | UNCHANGED | lock permanente; XFA payout fuerza F=0; aceptado tal cual |
| S06 | UNCHANGED | predicado Topstep aceptado; igualdad exacta 55% sigue obligatoria (G53-09 la reafirma) |
| S07 | UNCHANGED | predicado TPT estricto aceptado; `P>2A` separado de `P≥3000`; sin epsilon |
| S08 | UNCHANGED | actividad/winning days aceptado tal cual |
| S09 | EXTENDED | máximo continuo aceptado; añadir control de máximo-no-actualizado (masa singular M=m0 → S21) e identidad de coordenadas `w_d(0,m)+w_m(0,m)=0` como auditoría de formulación alternativa |
| S10 | CORRECTED | alcance corregido a dos tiempos de muerte τ_D/ζ (G53-07); fórmulas idénticas; cola exponencial sólo pre-cap; T<D con `exp(−T/D)`; no es oracle del q EOD completo; cobertura de regímenes en S23 |
| S11 | UNCHANGED | martingala nominal aceptada a horizonte finito; alcance G53-08 declarado en C5 |
| S12 | CORRECTED | indicador de activación corregido a `I_act`; añade fixture de activación fee=0 (S20) |
| S13 | UNCHANGED | cierre/edad aceptado tal cual |
| S14 | CORRECTED | identidad de pricing corregida: `K_NOFEE40−K_LIST=68(1+n)+130·I_act` |
| S15 | UNCHANGED | cronología/calendario aceptada tal cual |
| S16 | UNCHANGED | aislamiento/reproducibilidad aceptada tal cual |
| S17 | UNCHANGED | inclusión de éxitos WAIT⊂CLOSE aceptada bajo condiciones GOD: mismo path hasta divergencia, decision schedule idéntico, fallback idéntico, settlement ideal con cash positivo en cada cierre elegido |
| S18 | CORRECTED | cota de completación muestral separada de incertidumbre poblacional (G53-03); masas exactas de solver como caso propio; terminación a.s. de cada attempt requerida para geometric |

**Additions obligatorias (nuevas fixtures; ninguna ejecutada en este mandato):**

| ID | Fixture (fuente) | Aceptación esperada |
|---|---|---|
| S19 | missing-history-A negative (G53-01) | `[1700,700,600]` vs `[1400,900,700]`: mismo P=3000, N=3, H_EOD=3000, F=0, A distinto ⇒ desenlaces de consistencia distintos; un oráculo con estado insuficiente debe fallar este control |
| S20 | zero-fee activation (G53-04) | activación completada + fee 0 + receipt ⇒ `I_act=1`, `J=1`, `J≤I_act`, débito de activación=0 |
| S21 | singular M=m0 (G53-06) | desde `e0<m0`: masa en `m_final=m0` preservada según `k^{(m0−D,m0)}_{h²V}(e0,y)dy·δ_{m0}(dm)`; `h=0` ⇒ masa identidad; prohibida normalización como densidad 2D |
| S22 | geometric barrier tie (G53-05) | SL=floor y TP=lock coincidentes: prioridad pérdida>close>add; lock se actualiza aunque coincida con TP; estado inicial en frontera absorbido a tiempo 0 por operador determinista, no por tolerancia |
| S23 | S10 regime coverage (G53-07) | T<D ⇒ `exp(−T/D)`; T=D ⇒ `e⁻¹`; T>D ⇒ `e⁻¹·D/T`; cola capped `P(M_ζ≥z)` para z>D ⇒ `e⁻¹·D/z`; anclas D=2000/T=3000: `.24525296078096157` y lock `.36787944117144233` |
| S24 | duration-sensitive resolvent (GOD) | `E_0[exp(−λτ_T); τ_T<ζ] = exp[−κD·coth(κD)]·sinh(κD)/sinh(κT)` con `κ=√(2λ)/|h|`, T≥D; anclas D=h=1, T=1.5: `.21477390832873927` (λ=.125) y `.14846893086020618` (λ=.5); `λ↓0` recupera S10 |
| S25 | exact mass vs MC censoring (G53-03) | `N=1,S=1,U=0` ⇒ `qhat_final_sample=1` SIN certificar q poblacional (IC η aplicable); masas de solver ⇒ `q∈[p_received,p_received+p_unresolved]` determinista; ambas vías etiquetadas por separado en todo reporte |
| S26 | scale-invariance (GOD ν/scaling) | escalar niveles monetarios y distancias de precio por c con h fijo exige `ν×c²` y conserva la ley de estados normalizados; `ρ_i=h_ref²ν_i/D²` adimensional; enteros de contratos/tick/fees no escalados rompen la invariancia; `h=0` sólo como fixture matemática de no exposición |

### Tabla de cierre

| Finding | Status | Sección canónica corregida | Residual uncertainty | SPEC blocker |
|---|---|---|---|---|
| G53-01 | **CLOSED_BY_CONTRACT** | C1 (estados locales + estado suficiente + fixture negativa + refinamiento independiente) | representación numérica de la historia continua (cuadratura/malla/condicionamiento) se elige en SPEC; el contrato fija la obligación, no el algoritmo | SPEC freeze sigue bloqueado hasta aceptación manager de esta sección |
| G53-02 | **CLOSED_BY_CONTRACT** | C2 (siete componentes ε, presupuestos A–D, inequality, Σδ_i, targets semánticos, etiquetas de evidencia) | demostración numérica por componentes es trabajo de implementación futura; presupuestos semánticos ya congelados | ídem |
| G53-03 | **CLOSED_BY_CONTRACT** | C3 + S18/S25 corregidos | elección del método de confianza (envolvente η, binomial exacto, confidence sequence) abierta bajo contrato | ídem |
| G53-04 | **CLOSED_BY_CONTRACT** | C4 + S12/S14 corregidos + S20 | ninguno material | ídem |

G53-05..G53-10: incorporadas como precisiones contractuales en C5 y en las filas EXTENDED/CORRECTED de C6; sin cierre requerido (el manager ya las aceptó como clarifications/conditions).

### /verify — comparación directa contra el GOD review

1. G53-01 tiene contrato canónico corregido: C1 (estados locales tabulados, estado suficiente enumerado, fixture negativa obligatoria, representación/refinamiento independiente de la malla local). ✓
2. G53-02 tiene contrato canónico corregido: C2 (componentes ε separados, presupuestos por observable A–D, inequality del GOD, acumulación Σδ_i, targets semánticos, etiquetas). ✓
3. G53-03 tiene contrato canónico corregido: C3 (qhat muestral, envolvente η como ejemplo conservador no exclusivo, masas exactas de solver, propagación, prohibición de dividir por q_L=0). ✓
4. G53-04 tiene contrato canónico corregido: C4 (I_act, J≤I_act, débito `I_act·activation_fee`, C_path, fixture `68(1+n)+130·I_act`, fixture fee cero, separación de símbolos A vs activation_fee). ✓
5. Ninguna fórmula aceptada del GOD fue cambiada: kernel `k_V`, `Q_x`, `f_a`, `f_b`, `U_x`, `L_x`, condición diagonal `u_m(m,m)=0`, generador `L=(h²/2)∂²_e`, masa singular `δ_{m0}`, S10 (τ_D/ζ), resolvente y transición al locked 1D — todos citados verbatim. Las únicas expresiones alteradas respecto del draft PRE-GOD (`I` en S12/S14, intervalo literal de S18) son exactamente las correcciones que el propio GOD prescribió. ✓
6. `(e,m)` y `u_m=0` sin cambios: declarados intactos en C5/G53-06; prohibida la sustitución por reflexión normal o Neumann. ✓
7. Fórmulas S10 idénticas al GOD: C5/G53-07 y S23 reproducen las expresiones del veredicto S10 sin alteración. ✓
8. No se creó código. ✓
9. No se creó Functional SPEC ni Technical SPEC. ✓
10. No hubo research Tier-2. ✓

### Bloqueos residuales exactos

1. SPEC freeze permanece bloqueado hasta que el manager revise y acepte esta sección (gate `D5_SESSION_MODEL_CORRECTIONS`).
2. Trabajo futuro bajo contrato ya fijado (no bloquea el contrato): representación de historia continua de C1; demostración numérica de C2 por componentes; elección del método de confianza de C3.
3. Inputs de escenario sin cambios respecto del handoff GOD: perfil/vector ν + grid, TradePolicy/WithdrawalPolicy, calendario de ventanas/publicación/billing/settlement, criterio de horizonte/cola.
4. Sin cambios: pregunta B4 `AllowedRequests` TPT (bloquea certificación de reglas completas/cash real de TPT, no los kernels); TPT `ECONOMICS_ONLY`; `RETAIN_BUFFER`/`IDEAL_COMPLIANT` como escenarios etiquetados.

### Reuse / improve

Artefactos reutilizables producidos (todos dentro de esta sección): contrato corregido del session model; contrato de estado suficiente; contrato de certificación numérica; identidades de ledger corregidas; matriz de tests reconciliada. `REUSABLE_BEHAVIOR_CANDIDATES = NONE`. Observación de proceso (real, no fabricada): el formato GOD que incrusta su cláusula «Corrected formulation» por finding hizo esta reconciliación determinista; conviene repetirlo en futuros reviews GOD. Segunda: los findings no tienen registro machine-readable fuera del prose del planner; extraer G53-01..10 exigió parseo manual del documento completo.

### Gate

`D5_SESSION_MODEL_CORRECTIONS = REVIEW`. `D5_SESSION_MODEL_PASS` sigue REVIEW y NO se auto-acepta. No se inicia SPEC. Next action: `MANAGER_ACCEPT_SESSION_MODEL` (sin segundo GOD shot: ninguna corrección cambió kernel, `(e,m)`, diagonal, S10, martingala ni clase de oráculo). Agents-OS actualizado: **sí** — change_log y continuidad consolidados en este planner único por mandato de alcance; core, journal externo y tarea puente intactos. **STOP.**


## Manager Acceptance — D5.3 Session Model PASS — 2026-09-24

**Decision:** ACCEPTED.

Evidence:
- GOD review returned `MATH_REVISE`, not NO_GO.
- G53-01..G53-04 are now `CLOSED_BY_CONTRACT`.
- G53-05..G53-10 were incorporated as constraints/clarifications.
- Correction pass explicitly changed no accepted kernel mathematics, no `(e,m)` dynamics, no diagonal condition, no S10, no martingale semantics, and no oracle model class.
- A second GOD shot is therefore NOT required by the frozen manager rule.

Gate:
- `D5_SESSION_MODEL_CORRECTIONS = ACCEPTED`
- `D5_SESSION_MODEL_PASS = ACCEPTED`

### Owner priority override — Topstep results first

Owner priority for the next delivery is to obtain a decision-quality Topstep economic experiment as soon as possible, while continuing the broader D5 project afterward.

Delivery is therefore split:

#### D5-M1A — TOPSTEP FAST TRACK

Goal:
simulate **Topstep 50K Trading Combine Standard → XFA Standard → first withdrawal received | burned** under the accepted structural-null session model and produce decision-quality economics.

This milestone MUST NOT implement TPT PRO running-maximum support.

Required Topstep capabilities only:
- finite-horizon 1D killed-Brownian session kernel;
- session clock / EOD boundary;
- forced EOD flat;
- EOD trailing MLL with lock;
- evaluation consistency 55%;
- minimum trading-day requirement;
- XFA winning-day counting;
- XFA payout eligibility;
- payout cap/min/split;
- purchase/renewal/activation cash ledger;
- first withdrawal receipt state;
- cohort statistics / censoring / error reporting;
- explicit `nu` sensitivity grid.

Explicit defer from M1A:
- TPT PRO `(e,m)` kernel;
- TPT inside-buffer policies;
- Tier-2 providers;
- empirical market edge;
- synthetic delta;
- execution commissions/slippage;
- Echo/NinjaTrader integration.

#### D5-M1B — TPT / full Tier-1 completion

Runs after M1A unless a Topstep result or defect changes the project decision.

### D5-M1A decision outputs

At minimum for every declared `nu` / TradePolicy scenario:
- `P(pass evaluation)`;
- `P(first withdrawal | funded)`;
- `q_withdraw`;
- expected evaluations / first withdrawal;
- no-withdrawal probability after 5/10/20/50 purchased evaluations;
- expected cash per evaluation;
- expected cumulative cash before first withdrawal;
- cash P5/P50/P95 before first withdrawal;
- net cash / 10 and /100 evaluations;
- expected trading days / first withdrawal;
- unresolved/censored mass;
- numerical + Monte Carlo uncertainty separately.

### Decision use

M1A is a **structural-null decision surface**, not an empirical profitability claim. It can answer whether Topstep contractual asymmetry alone produces positive personal cash EV under the frozen null/session policies and which `nu` regions are viable. It does NOT prove that the eventual real strategy has those `nu`, edge, fill quality or operational compatibility.

Next action:
`TOPSTEP_SPEC_FREEZE`.

No coding authorized until Topstep Functional/Technical SPECs are frozen.


## D5-M1A Topstep Spec Freeze — 2026-09-24

### Alcance y resultado

Ejecutado el mandato `TOPSTEP_SPEC_FREEZE` del override owner (Topstep results first). Productos: [[D5-M1A — Topstep Functional SPEC]] (comportamiento observable: lifecycle, Evaluation, XFA, TradePolicy SD-1, modos 0–4 adds, outputs obligatorios, matriz, aceptancia, prohibiciones de interpretación) y [[D5-M1A — Topstep Technical SPEC]] (extensión mínima de D4: paquete `internal/topstep` con zero-diff de `internal/sim`, kernel 1D finite-horizon con la ley aceptada verbatim y muestreo de ley conjunta, motor de sesiones, estado suficiente C1, ledger `I_act`, presupuesto de error C2, reproducibilidad versionada, y paquetes SHOT A/B/C preparados). Sin código, sin ejecutar simulación ni Monte Carlo, sin TPT PRO `(e,m)`, sin Tier-2, sin research de otras props. D4 permanece CLOSED y verificado físicamente en su checkout (`d4f42a41946f12231b75e4eb65b90d132731be0d`, tree limpio).

### Decisiones embebidas que la aceptación del gate debe ratificar

| SD | Decisión propuesta | Alternativa registrada |
|---|---|---|
| SD-1 | TradePolicy de referencia: G=L=100, h0=1, adds qty 1 en prefijos de {−30,−50,−70,−90} (k=0..4) | k=2 vía T3 {−20,−40}; cualquier otra escalera requiere mandato owner |
| SD-2 | Perfil ν: σ constante dentro de la ventana activa única; input adimensional `ρ_full` con `ν_E=ρ_full·D²`, D=2000; grid `sqrt(ρ_full)∈{0.1,0.25,0.5,1,2,4}` | otra forma temporal exige `νProfileId` nuevo y re-freeze |
| SD-3 | Billing: FIXED_30D desde compra; empate rebill/cancelación gana cancelación; sensibilidad de un cargo reportada | orden inverso de empate |
| SD-4 | Método de payout de referencia: Aeropay fee 0 | ACH/Wire $30 como sensibilidad fuera de la matriz |

### Defer explícito (M1B o fuera)

S09/S10/S21/S23/S24 (existen sólo para soporte `(e,m)` PRO), S07/S13/S17 (lifecycle/policy TPT), TPT completo, Tier-2, delta≠0, execution costs, resets/Back2Funded in-attempt, DLL add-on, variantes No Activation Fee/Consistency XFA, payouts #2+.

### Gate y handoff

- `D5_TOPSTEP_SPEC_PASS = REVIEW` (no auto-aceptado).
- Aceptación owner ⇒ habilita SHOT A (paquete en Technical SPEC §14.1) con baseline `d4f42a4` + commit de freeze; Shot B verifica el commit exacto de Shot A sin arreglar producto; Shot C absorbe sólo regresiones aceptadas.
- La ejecución de la matriz de 30 puntos NO es parte del cierre de Shot C; se autoriza por separado con tamaños de corrida congelados antes de observar resultados (C2.iv).
- Agents-OS actualizado: sí — 2 SPECs nuevas en el proyecto, planner actualizado (estado, tareas, gates, bitácora, links, esta sección), change_log en `80-agents/journal/logs/`. D4, Echo y Forge intactos. **STOP.**


## Manager Erratum — Multi-Payout Economics Required — 2026-09-24

Owner clarified the actual D5 economic thesis: the experiment must not stop at first withdrawal. A fair per-trade process may have poor first-withdrawal conversion but positive personal cash EV through repeated XFA payout cycles. Therefore first-withdrawal remains a diagnostic KPI, not the complete Topstep economic verdict.

### Required Topstep M1A extension before Shot A

Model XFA Standard payout cycles through at least:
- payout #1;
- payout #2;
- payout #3;
- payout #4;

with an optional #5 sensitivity if the current rules permit the account to remain XFA.

After each payout:
- apply actual account-balance debit;
- MLL remains locked at 0;
- reset the five-winning-day counter;
- require positive net profit since previous payout;
- apply 50%-of-balance rule, 50K Standard cap and 90/10 split;
- preserve account until MLL breach, vendor transition/call-up, or explicit experiment horizon.

Add outcomes/state:
- PAYOUT_1_RECEIVED ... PAYOUT_4_RECEIVED;
- XFA_BURNED;
- CALLED_UP_LIVE / VENDOR_TRANSITION as a censoring/transition state where applicable;
- INCOMPLETE.

### Current-rule correction

Topstep does NOT guarantee or require a fixed “5 payouts then Live” transition. Current official rule states Live call-up is case-by-case by Risk Team and may occur earlier or later; number of payouts is not a deterministic threshold. Therefore “take 3–4 payouts to avoid Live” cannot be encoded as a factual rule.

For structural economics, provide scenarios:
1. NO_CALLUP_BEFORE_PAYOUT_N (N=1..4) — conditional scenario, explicitly not a rule claim;
2. CALLUP_CENSORING — once an externally supplied/vendor-calibrated call-up model exists;
3. STOP_AFTER_N_PAYOUTS — trader policy, not vendor avoidance guarantee.

### New required metrics

In addition to q_first_withdraw:
- P(reach payout k | evaluation purchased), k=1..4;
- P(reach payout k | XFA activated);
- expected payout count per evaluation;
- expected payout count per activated XFA;
- expected net external cash over payout horizon N;
- EV per evaluation for N=1,2,3,4;
- marginal EV contribution of payout #2/#3/#4;
- cash distribution / 100 evaluations for each horizon N;
- account survival after each payout;
- payout-cycle duration and winning-day count.

### Gate impact

The existing Topstep SPEC freeze must be amended before implementation.
`D5_TOPSTEP_SPEC_PASS` remains REVIEW.
Shot A is BLOCKED until the Functional/Technical SPECs include multi-payout lifecycle and call-up censoring semantics.

This erratum does not change D5.3 stochastic mathematics; after first payout Topstep remains a 1D locked-floor process.


## Owner Policy Override — D5-M1A-P Topstep Discrete Policy Economics — 2026-09-24

This override is owner-authorized and supersedes the previous immediate M1A experiment matrix, without deleting the accepted Brownian/session model. The Brownian kernel remains the later realism path; the next 3-shot milestone is a bounded discrete-policy economics experiment designed to answer the owner's exact Topstep question quickly and reproducibly.

### Primary policy

Provider/product:
- Topstep 50K Trading Combine Standard → XFA Standard.
- pricing: $49 evaluation, $149 activation.
- payout: 50% of XFA balance capped at $2,000 gross, 90/10 split.
- Chile reference settlement: Wire/SWIFT fee $30; report gross, trader-after-split, and external-cash-received separately.

Trading Combine:
- target day 1: +$1,500 before max loss / MLL failure;
- target day 2: +$1,500 before max loss / MLL failure;
- both successful days satisfy 50% best-day share, inside the 55% consistency target;
- a loss outcome in either day is BURNED for this policy;
- pass probability under linked Bernoulli hit-rate p is analytically p².

XFA payout cycle #1:
- first funded trading day: target +$4,000 before $2,000 loss; success counts as winning day #1 and locks MLL at $0 at EOD;
- then require 4 additional winning days to reach the first five-day requirement;
- harvest-day win = +$500;
- harvest-day loss cap is configurable and is a FIRST-CLASS experiment input, not fixed: $500 / $1,000 / $1,500 / $2,000;
- after winning-day eligibility is satisfied, continue until XFA balance >= $4,000 if necessary, then request exactly $2,000 gross;
- first payout external reference cash = $2,000 - 10% split - $30 Wire/SWIFT fee = $1,770.

XFA payout cycles #2+:
- after each payout, MLL remains $0 and the winning-day counter resets;
- require FIVE NEW winning days >= $150, not four;
- same +$500 / configurable-loss harvest process;
- require positive net profit since previous payout and balance >= $4,000 before requesting the fixed $2,000 gross;
- payout request day does not count toward the next five-day cycle.

Payout horizon:
- primary owner policy: STOP_AFTER_3_PAYOUTS;
- hard configurable maximum: 4;
- payout #4 is sensitivity only;
- never intentionally burn an XFA to free a slot; STOP means stop trading that account. Vendor call-up remains external/censored because Topstep does not publish a deterministic payout-count threshold.

Probability inputs:
- primary linked hit-rate p applies to the abstract daily objective event in all stages;
- grid: 0.50, 0.51, 0.525, 0.55, 0.575, 0.60, 0.625, 0.65;
- implementation MAY expose stage-specific p_eval / p_bulto / p_harvest overrides, but primary reports keep them linked;
- p is explicitly "probability that the session policy hits its positive target before its loss cap", NOT raw per-trade win rate and NOT a claim of market edge.

Portfolio:
- normalized month = 20 trading sessions plus actual-calendar mode;
- 5 concurrent account pipelines;
- modes: INDEPENDENT and PERFECT_COPY;
- after evaluation/XFA natural burn, a new Combine may start next trading session;
- after STOP_AFTER_N, that XFA remains stopped and continues occupying an XFA slot unless an external closure/call-up is supplied;
- report same-day multiple-MLL events because Topstep currently identifies multiple accounts hitting MLL in one day / account stacking patterns as responsible-trading/compliance risk.

### Required output

For every (p, harvest_loss, max_payouts, correlation_mode):
- p_pass;
- P(payout #1/#2/#3/#4 | evaluation);
- P(payout #1/#2/#3/#4 | activated XFA);
- evaluations purchased;
- activations;
- XFA burns;
- payout count;
- external cash received;
- evaluation + activation costs;
- net economic P&L;
- 20-session expected monthly P&L with 5 pipelines;
- P(month > 0), P5/P50/P95;
- probability of >=1 payout;
- account-days / payout;
- same-day multi-MLL count/rate;
- stopped-XFA slot occupancy;
- requested/approved/received amounts separately;
- settlement-latency sensitivity for international Wire/SWIFT.

### Interpretation guard

This is a synthetic POLICY hit-rate experiment. At p=0.50, asymmetric outcomes such as +$500/-$2,000 are NOT zero-EV trading; their nominal one-day expectancy is negative. The experiment asks whether prop contractual asymmetry can nevertheless make PERSONAL CASH EV positive. It must not be labeled a fair-market Brownian result or empirical strategy evidence.

### Three-shot delivery

Exactly three shots:
A. implement discrete policy engine + exact/DP reference + MC/monthly portfolio runner;
B. independently falsify probabilities, ledger, payout cycles, correlation and official-rule semantics; no product fixes;
C. correct accepted findings, certify, and RUN the full p × harvest_loss × payout_horizon × correlation matrix. Shot C must deliver the final decision table; no fourth shot.

Gate:
`D5_TOPSTEP_POLICY_SPEC_PASS = ACCEPTED_BY_OWNER`.
`D5_TOPSTEP_POLICY_IMPL_PASS = PENDING`.
Next action: DISPATCH_SHOT_A.


## D5-M1A-P — Three-shot execution package — 2026-09-24

### Shot A — Policy simulator implementation
Implement the owner-frozen discrete Topstep policy only. Required: exact finite-state/DP reference where tractable + Monte Carlo portfolio runner; linked/stage-specific hit probabilities; 50K Combine 2-day policy; XFA $4k bulto + $500 harvest cycles; configurable harvest loss; 3-payout primary / 4 max; 5-pipeline 20-session and actual-calendar modes; independent/perfect-copy correlation modes; current Topstep fee/payout ledger; compliance counters. No Brownian kernel implementation in this shot. Gate: `D5_TOPSTEP_POLICY_IMPL_A = REVIEW`.

### Shot B — Independent adversarial audit
Fresh context, exact Shot A commit immutable. Independently recompute closed-form/DP controls: Combine pass = p_eval² under the frozen two-day policy; winning-day/reset semantics; fixed-$2k payout eligibility; payout-cycle state transitions; ledger; month accounting; independent vs perfect-copy distributions; censoring. Verify current-rule mappings against official captured rules. Create adversarial boundary fixtures. No product fixes. Gate: `D5_TOPSTEP_POLICY_AUDIT_B = REVIEW`.

### Shot C — Correction, certification and experiment
Correct only accepted Shot B findings, promote useful reproducers to regression tests, rerun complete quality gate, then execute the FULL frozen matrix. Required final report includes primary STOP_AFTER_3 and payout#4 sensitivity; p grid; harvest-loss grid; 5-pipeline monthly economics; correlation extremes; international settlement sensitivity; P5/P50/P95; compliance counters; break-even contours. This shot MUST return the actual decision table and certified commit. No fourth shot. Gate: `D5_TOPSTEP_POLICY_RESULT_C = REVIEW`.

### Manager acceptance rule
Only the owner/manager accepts A/B/C gates. The next active assignment is Shot A only.


## Owner Policy Correction — D5-M1A-P150 — 2026-09-24

This section SUPERSEDES the prior D5-M1A-P harvest target of +$500. The correct owner policy uses the minimum Standard-XFA winning-day threshold: **+$150** on qualification days.

### Probability semantics

Primary sensitivity input:
`p_objective_hit = P(session policy hits its positive target before its declared loss cap)`.

This is NOT automatically raw per-trade win rate. A future hardscalping submodel may map `p_trade` and intra-session management into `p_objective_hit`; that mapping is outside this discrete-policy milestone.

Linked primary grid:
`p_objective_hit ∈ {0.50, 0.51, 0.525, 0.55, 0.575, 0.60, 0.625, 0.65, 0.70, 0.75}`.

Optional stage overrides remain allowed:
`p_eval`, `p_bulto`, `p_qualify`.

### Frozen owner policy

#### Trading Combine 50K
- Day 1 objective: +$1,500 before loss cap / MLL failure.
- Day 2 objective: +$1,500 before loss cap / MLL failure.
- Any natural MLL breach burns the evaluation.
- Two successful days yield total +$3,000 with largest-day share 50%, inside Topstep's 55% consistency target.
- Under linked p and one objective event/day, analytical fixture: `P(pass)=p²`.

#### XFA payout cycle #1
- XFA starts balance 0, MLL -$2,000.
- First funded session "bulto": target +$4,000 before $2,000 loss / MLL breach.
- Bulto success: balance=$4,000; this is winning day #1; at EOD MLL locks to $0.
- Bulto failure: natural XFA burn.
- Then require FOUR additional winning days with target +$150 each, because Topstep Standard requires five winning days >=$150 and the +$4,000 day already counts as day #1.
- Qualification-day loss amount is an explicit config. Primary owner case: `qualify_loss=2000`; sensitivities: 150, 300, 500, 1000, 1500, 2000.
- A qualification loss does NOT automatically mean burn unless balance reaches the MLL floor. Apply the actual balance debit and continue if alive.
- Once 5 winning days are complete, request the fixed $2,000 gross only when balance >=$4,000. If eligibility is complete but balance<4,000, continue the same qualification policy until balance>=4,000 or natural burn.

Expected no-loss path:
0 → +4000 → +150 → +150 → +150 → +150 = 4600;
request 2000 gross; post-payout balance=2600.

#### XFA payout cycle #2
- Winning-day counter resets to zero after payout #1.
- First post-payout session "reload bulto": target +$2,000; primary loss cap $2,000.
- If success from balance 2600: balance=4600 and counts as winning day #1.
- Then require FOUR additional +$150 winning days to reach five new winning days.
- Expected no-loss balance before request: 5200.
- Request fixed $2,000 gross; expected no-loss post-payout balance=3200.
- If reload bulto loses $2,000 but account remains above MLL, primary policy is `CONTINUE_IF_ALIVE`; do not invent an intentional burn. Continue qualification/recovery until eligibility + balance>=4000 or natural burn.

#### XFA payout cycle #3
- Same mechanics: counter reset; reload bulto target +$2,000 / primary loss cap $2,000; four additional +$150 winning days; then fixed $2,000 gross if eligible and balance>=4000.
- Expected no-loss balance path: 3200 → 5200 → 5800 → payout 2000 → 3800.
- Primary owner policy: `STOP_AFTER_3_PAYOUTS`.
- Payout #4 remains sensitivity only if requested by owner; no deterministic vendor call-up threshold is assumed.

### Official-rule semantics preserved

Current Topstep Standard XFA requires:
- 5 winning days of at least $150;
- days need not be consecutive;
- the payout-request trading day does not count toward the next five-day cycle;
- after each payout the 5-day count restarts;
- after the first payout there must be positive net profit since the previous payout;
- payout request is 50% of account balance up to the 50K Standard cap of $2,000;
- profit split is 90/10;
- MLL resets/locks at $0 after payout.

### Required experiment axes

Primary matrix:
- linked `p_objective_hit` grid above;
- `qualify_loss ∈ {150,300,500,1000,1500,2000}`;
- payout horizon = 3;
- payout #4 sensitivity;
- 5 account pipelines;
- 20-session normalized month plus explicit-calendar mode;
- INDEPENDENT vs PERFECT_COPY account correlation.

Required stage-level outputs:
- `P(pass)`;
- `P(bulto1 success | XFA)`;
- `P(payout1 | XFA)`;
- `P(payout1 | evaluation purchased)`;
- `P(payout2 | payout1)`;
- `P(payout3 | payout2)`;
- natural-burn probability in each stage;
- expected sessions in each stage;
- expected account balance entering/leaving each payout cycle.

Required portfolio outputs:
- evaluations/month;
- activations/month;
- XFA burns/month;
- payout1/2/3 counts;
- external cash/month;
- total fees/month;
- net cash/month;
- P(month>0), P5/P50/P95;
- active/stopped XFA slot occupancy;
- same-day multi-MLL diagnostics;
- break-even contour in (`p_objective_hit`, `qualify_loss`).

### Interpretation

At linked `p_objective_hit=0.50`, a +150/-2000 qualification objective has negative nominal expectancy; this experiment is intentionally testing whether Topstep's external payoff asymmetry can overcome that at the personal-cash level. Do not label it a fair-market trading result.

The accepted Brownian/session model is not deleted; it remains the later realism bridge. This P150 discrete policy is the immediate three-shot economics experiment.


## Manager Dispatch Override — Shot A P150 — 2026-09-24

The prior Shot A package using +$500 harvest targets is SUPERSEDED. The only authorized active assignment is D5-M1A-P150.

Shot A must implement the discrete policy from §Owner Policy Correction — D5-M1A-P150, including:
- Combine +1500/+1500;
- first XFA bulto +4000/-2000;
- qualification target +150;
- configurable qualification loss;
- payout #1 with 1 bulto day + 4 additional +150 days;
- payout #2/#3 with +2000 reload bulto + 4 additional +150 days, with five new winning days per cycle;
- natural CONTINUE_IF_ALIVE after non-terminal losses;
- STOP_AFTER_3 primary;
- 5-pipeline monthly runner and independent/perfect-copy extremes.

Gate remains `D5_TOPSTEP_POLICY_IMPL_A = REVIEW`.


## Shot A — P150 Delivery Evidence (REVIEW) — 2026-09-24

Repo/branch: `xKoRx/echo-futures` @ `feature/d5-m1a-p150` (local, sin push). Baseline D4 CLOSED: `d4f42a41946f12231b75e4eb65b90d132731be0d` (intacto en semántica; `internal/sim` sólo recibió plumbing de resource-safety: variantes Context, guard checkpoints, RESOURCE PLAN en stderr, caps fail-closed — sin cambio de resultados ni RNG order; gate D4 47/47 re-verificado verde).

| campo | valor |
|---|---|
| commits | `321335f` resource-safety contract · `1103002` Shot A · `1dc1fa6` gofmt |
| paquete | `internal/p150` (engine, DP, single MC, portfolio MC, matrix, verify, CLI) + `internal/resources` (contrato) + `scripts/safe-run` family |
| tests | `go test ./...` verde (3 paquetes); `go test -race` verde (102 MB pico, 1:58); `sim p150-verify` = 14 fixtures / 23 checks PASS |
| coverage | `internal/p150` 96.0% (≥95% mandato); `internal/resources` con regresión de crecimiento acotado (falla si reaparece O(total_paths)) |
| fixtures analíticos | P(pass)=p² (4 valores de p); consistencia 50%≤55% (con control 60% que falla); bulto = winning day #1; payout requiere exactamente 4 adicionales de +150; reset W tras payout; 5 NUEVOS días por ciclo; gate balance≥4000 (elegible con 2600 no paga, cruza en 4100); split 1800; Wire 1770; débito gross (4600→2600); CONTINUE_IF_ALIVE + burn por tocar floor; byte-identical same-seed; DP≡MC dentro de 5σ predeclarada (7 comparaciones) |
| sample outputs | `scenarios/p150/samples/*.json` (4 celdas, 100k runs): p=.55/ql=2000 IND net −$2,824 P(>0)=5.5%; misma celda PERFECT_COPY net −$2,828 con P95 +$5,890 (cola correlacionada) vs +$88 IND; p=.50/ql=2000 net −$3,372 P(>0)=1.6%; p=.60/ql=150 net +$6,487 P(>0)=97.9% |
| matrices | `scenarios/p150/matrix_primary.json` (10 p × 6 ql × 2 correlaciones, horizonte 3) y `matrix_payout4_sensitivity.json` (horizonte 4, meses 40) — CONGELADAS, NO ejecutadas (entrega de Shot C) |
| limits (declarados) | 1) miss de día de evaluación = MLL-breach por política del owner (congela P(pass)=p²; el matiz EOD-trailing del día 2 queda absorbido por el cap declarado); 2) settlement: cash contado al request, fee Wire −30; latencia de recepción diferida (requiere modo calendario explícito); 3) explicit-calendar mode subsumido por `month_sessions` N arbitrario (sin fechas); 4) renovaciones $49/30d fuera del mes normalizado de 20 sesiones; 5) reset/Back2Funded fuera de scope (recovery = nueva evaluación comprada); 6) cuantiles >1e6 muestras en modo histograma (error ≤1 bin, documentado) |
| determinismo | mismo seed+config ⇒ JSON byte-idéntico (misma toolchain go1.27.1); DP con iteración ordenada (map range era no-determinístico en último bit) |
| resource evidence | RESOURCE PLAN en stderr de todo comando no trivial; caps `ECHO_FUTURES_MAX_RUNS/MAX_COHORTS`; scaling N/2N/4N/8N acotado; leak test 10× estable; race 103 MB pico dentro de cgroup 6G |

Root cause incidentes (owner-observed ~128 GB; kernel-verificado): swarm externo node/vite/esbuild del front Echo v3 (fuera de este repo; acción de contención sugerida: cgroup propio o eliminar el loop de rebuild). Por qué falló el recovery #1: los guards internos aún no estaban certificados ni eran externos; el árbol ni siquiera compilaba al momento del incidente #2 y quedaba un binario viejo no-acotado en /tmp (eliminado). Complejidad vieja cohort: O(N) residente (3×8 B×N) + sort in-place; nueva: O(workers×batch + bounded aggregators) — plateau medido 84 MB @1e6 → 64 MB @2e6.


## Manager Review — D5-M1A-P150 Shot A provisional — 2026-09-24

**Verdict:** TECHNICALLY_PROMISING / SOURCE_FREEZE_REQUIRED.

The Shot A handoff is internally coherent and shows no immediate semantic blocker: P150 state machine implemented, DP and MC cross-check, deterministic output restored, bounded-resource contract, D4 regression suite reported green, race reported green, and sample cells discriminate negative vs positive economic regions as expected.

However, manager acceptance of `D5_TOPSTEP_POLICY_IMPL_A` is NOT yet granted because the implementation branch is reported as local-only and is not inspectable through the repository authority from this manager session.

Mandatory pre-Shot-B correction:
1. publish/push `feature/d5-m1a-p150` without additional source mutation;
2. report the exact remote HEAD;
3. the immutable Shot B baseline MUST be the final code commit after formatting, currently reported as `1dc1fa6`, not the intermediate implementation commit `1103002`;
4. if pushing produces or requires any source/content change, report the new final HEAD and do not silently preserve `1dc1fa6` as the audit target.

Process note:
- `D5_RESOURCE_SAFETY_PASS` is supported by strong reported evidence and the owner-observed host recovery, but the external front-v3 Vite/esbuild swarm is a separate Echo-front incident and should receive its own durable containment outside Echo Futures.
- The D4 cohort memory change touches a certified component. Shot B MUST explicitly verify semantic equivalence / RNG-order invariance and D4 T1–T8 / 47-47 regression evidence rather than treating the plumbing claim as trusted.

Gate:
- `D5_TOPSTEP_POLICY_IMPL_A = REVIEW`
- next action: `PUBLISH_AND_FREEZE_SHOT_A_HEAD`, then independent Shot B against that exact commit.


## Shot B — Independent Adversarial Audit — D5-M1A-P150 — 2026-09-24

**Verdict: AUDIT_FINDINGS.** Gate `D5_TOPSTEP_POLICY_AUDIT_B = REVIEW` (no self-accepted). Recommended next: resolve B-01 (owner/manager publishes the branch), then `MANAGER_REVIEW_FOR_SHOT_C`. No product code was fixed, no policy changed, Shot C not executed; the audited tree was never mutated (verified: clean status, HEAD unchanged before/after).

**Frozen audited commit:** `1dc1fa6afaaabe99ac8648f8c11e293fa9acd17c` — local HEAD of `feature/d5-m1a-p150` in the workspace clone `/home/kor/aranea/work/echo-futures-simulator-v0-20260924/echo-futures`, clean tree, 3 commits over D4 baseline `d4f42a41946f12231b75e4eb65b90d132731be0d` (`321335f` resource safety, `1103002` Shot A, `1dc1fa6` gofmt). All verification ran against a read-only `git archive` export in `/tmp/shotb/repocopy` (verifier-only code lives only there and in `/tmp/shotb/verify`, never in the product path).

### Findings

| ID | Severidad | Alcance | Descripción |
|---|---|---|---|
| B-01 | MAJOR (proceso, no código) | Precondition | La rama `feature/d5-m1a-p150` NO está publicada remotamente: el clone no tiene ningún remote configurado (`git remote -v` vacío). La corrección pre-Shot-B obligatoria del manager (`PUBLISH_AND_FREEZE_SHOT_A_HEAD`) no se ejecutó. Shot B congeló el HEAD local `1dc1fa6` y auditó contra él; la cadena de inmutabilidad hacia el repositorio autoridad queda rota hasta que el owner publique y reporte el HEAD remoto exacto. Acción: owner/manager (publicar sin mutación y verificar que el SHA remoto == `1dc1fa6afaaabe99ac8648f8c11e293fa9acd17c`); no es trabajo de Shot C. |
| B-02 | MINOR | Reproducibilidad de artefactos | Los 4 samples congelados `scenarios/p150/samples/*.json` NO son byte-idénticos al re-ejecutarlos desde el commit congelado en la misma toolchain go1.27.1: diffs de 1 ULP en campos `dp_reference` (3–9 campos por celda, p.ej. `p_payout2_given_payout1` 0.03222546134898663 vs …662). La identidad byte dentro de una misma compilación sí se cumple (fixture F13 verde + re-ejecuciones). Causa probable: samples generados desde una compilación intermedia anterior al fix de iteración ordenada del DP (`sortedCentsKeys`). Impacto económico nulo (1e-16 relativo). Shot C: regenerar los samples desde el commit final o acotar el reclamo de byte-identity a misma-binario. |
| B-03 | MINOR | Higiene | `.gitignore` eliminó `/sim` y `*.test` y sólo añadió `build/`: un binario compilado en la raíz (`go build ./cmd/sim`) vuelve a ensuciar `git status`. Shot C puede restaurar las dos líneas. |
| B-04 | INFO | Alcance declarado | Settlement: cash contado al request con fee Wire −30, latencia de recepción diferida; renovaciones $49/30d fuera del mes normalizado. Limitaciones ya declaradas por Shot A; deben permanecer etiquetadas en la tabla de decisión final de Shot C. |
| B-05 | INFO | Correlación | PERFECT_COPY degenera a lockstep total: los 5 pipelines comparten la misma config (mismas probabilidades de etapa) y el mismo uniforme por sesión, por lo que estados divergentes entre cuentas son inalcanzables; el modo no ejercita manejo de estados divergentes (no existe tal camino). Verificado a nivel de evento con fixture determinista de 2 cuentas. |
| B-06 | INFO | Semántica | Un día de cualificación perdido debita el `qualify_loss` completo aunque la distancia restante al floor sea menor (la cuenta quema en ese paso). El débito es cosmético: la cuenta es terminal y el balance residual nunca se usa. |

### Auditorías 1–11 (evidencia resumida)

- **A1 Source delta (PASS).** Delta exacto vs `d4f42a4` clasificado: nuevo `internal/p150` (engine/DP/MC/portfolio/matrix/verify/CLI), nuevo `internal/resources`, nuevos `scripts/safe-run|safe-test|safe-sim|safe-validate`, nuevos `scenarios/p150/*`, README; en `internal/sim` sólo plumbing resource-safety (batching + guards + caps + RESOURCE PLAN en stderr): los cuerpos de loop y el orden RNG son idénticos (probado por byte-equality A2); `cmd/sim` sólo enruta `p150*` y añade signal handling. Sin expansión de scope.
- **A2 D4 non-regression (PASS).** Gate D4 completo 47/47 (`sim validate --runs 1000000 --seed 42`: T1:2, T2:4, T3:7, T4:2, T5:5, T6:7, T7:1, T8:3, INV:16, allPass=true) bajo cgroup. Binario viejo (build de `d4f42a4`) vs binario nuevo con mismos seeds: `simulate` 200k runs y `cohort` 50k cohorts (modo exacto, bajo el límite 1e6) **byte-idénticos** — igualdad exacta old O(N) vs nuevo QuantileStore demostrada, no asumida. Sobre el umbral: cohort 2e6 corre en modo histograma declarado (`quantile_mode=histogram(scenario-derived-range)`), regresiones de crecimiento acotado (`TestCohortMemoryBoundedAcrossScales`, `TestQuantileStoreMemoryBoundedAcrossScales`) verdes en suite. `go test ./...` y `go test -race ./...` verdes en cgroup. Sin cambio semántico de CLI/JSON (sólo RESOURCE PLAN en stderr, sancionado por el contrato de resource safety).
- **A3 Policy state machine (PASS).** Modelo de referencia independiente construido desde el texto de policy congelada (sin importar el engine): P(pass)=p² verificado (MC producto .249678@p=.5, .302391@p=.55; consistencia 1500/3000=50%≤55% con control 60% que falla); paths de saldo sin pérdida confirmados exactos en p→1 (DP: pre-balances 4600/5200/5800; bulto=winning day #1; 4 días +150 adicionales; payout débita gross 2000; reset W; 5 NUEVOS días por ciclo; gate balance≥4000 — elegible con 2600 no paga, cruza en 4100); pérdidas: débito del loss configurado, CONTINUE_IF_ALIVE sobre el floor, burn sólo al tocar floor (bulto miss quema natural; qualify miss a 0 quema); STOP_AFTER_3 nunca burn intencional.
- **A4 Ledger (PASS).** Cents exactos: eval 4900, activation 14900 (una sola vez, cobrada en el pass; eval quemada no paga activation — trace 7b actFee=0; sin duplicación posible: único sitio de asignación), gross 200000, split 180000 (90/10), Wire 3000, external 177000; el XFA se debita 2000 gross (4600→2600, trace 7a), nunca 1800/1770; ledger personal (`Ledger.Net()`) separado del balance nominal; nueva evaluación comprada tras burn natural (portfolio p→0: evals=20, evalBurns=20, activations=0). Identidad 3 payouts: net=+5112 = 3×1770−49−149.
- **A5 Exact DP (PASS).** Verificador independiente (cadena absorbente propia sobre retícula $50 con Gauss–Seidel + backward induction de horizonte finito + MC propio, tres algoritmos independientes entre sí): coincidencia con `ComputeDP` del producto **exacta a 8+ decimales en todas las celdas auditadas** (p∈{.50,.51,.55}×ql2000 y {p=.60,p=.75,p=.55}×ql150: pay1|XFA, pay2|pay1, pay3|pay2, E[sessions] XFA/attempt, E[pre-balance|pay] cada una). Conservación de probabilidad = 1.000000000000 en todas las celdas. Fronteras: p→0 ⇒ 1 sesión, cash −49; p→1 ⇒ path sin pérdida determinista, 17 sesiones, cash +5112. Nota de auditoría: la única discrepancia histórica (E[sessions], diff = masa en rutas terminal-tras-sesión-inline) resultó ser un bug de MI verificador, no del producto; corregido y re-verificado.
- **A6 Monte Carlo (PASS).** Criterio predeclarado 5σ, N=1e6 fijo por celda, seed 4242. MC producto vs DP independiente: p=.50/2000 pay1|XFA .032057 vs .0313111 (2.1σ); p=.55/2000 .051076 vs .0505584 (1.3σ), pay2|pay1 .050631 vs .0528311 (1.2σ); p=.60/150 .599649 vs .5999956; p=.75/150 .749055 vs .7500000; E[sessions] y E[pre-balance|pay1] dentro de 5σ en las 4 celdas (p.ej. sessions 17.1548 vs 17.176998). Sin re-tuning de N.
- **A7 Portfolio time model (PASS).** p→1, 1 pipeline, 20 sesiones: sessions_used=17.0000, pay1=pay2=pay3=1.0000, stoppedEOM=1, activeEOM=0, net=+5112 — el reloj exacto payout1@s7, payout2@s12, payout3@s17 con STOP ocupando slot sin consumir sesiones. Burn→replace: nueva Combine al día siguiente (p→0: evals=20=sessions). Evaluación consume 2 sesiones y XFA arranca en la siguiente; payout resuelve al EOD del 5º día ganador sin consumir sesión extra (declarado); ningún pipeline ejecuta dos policy days por sesión (1 Step máximo por sesión en `runMonth`). Máximo físico: 3 payouts requieren 17 sesiones ≤ 20; con horizonte 4 en mes de 20 sesiones pay4=0 (necesita 22; la matriz de sensibilidad usa month_sessions=40, consistente). Traces adversariales de mano confirmados por fixture determinista.
- **A8 Correlation (PASS).** Regla replicada a nivel evento: un uniforme compartido por sesión, cada pipeline lo compara contra su propia probabilidad de etapa — fixture determinista de 2 cuentas con schedule explícito muestra eventos idénticos cuenta-por-cuenta, CONTINUE_IF_ALIVE, quema simultánea al tocar floor (multi-MLL mismo día) y replace la sesión siguiente. Expectación preservada: evals/mes IND 45.424 vs PC 45.425 (p=.5, 5000 meses) y 39.47 vs 39.38 (samples p=.55). Distribuciones diferen como corresponde: samples congelados p=.55/2000 P95 +$88 IND vs +$5890 PC, P(>0) 5.5% vs 8.7%, P5 −$4246 vs −$5175; mi reproducción p=.5: multi-MLL cuentas 37.8 IND vs 42.5 PC en 14.0 vs 8.5 eventos (PC concentra ~5 cuentas/evento = lockstep). Sin acoplamiento accidental en INDEPENDENT (substreams PCG por pipeline; promedio 2.55 cuentas/evento < 5).
- **A9 Resource safety (PASS).** `safe-run --verify-only` autoverifica MemoryHigh=4G/MemoryMax=6G/SwapMax=1G/TasksMax=128/CPU=400% dentro del scope real y falla cerrado (sin fallback); todas las ejecuciones de esta auditoría (suite, race, D4 gate, samples, 2e6 cohorts) corrieron dentro del cgroup. Caps fail-closed verificados: `ECHO_FUTURES_MAX_RUNS=1000` rechaza validate 1e6 y p150 5000; `ECHO_FUTURES_MAX_COHORTS=100` rechaza cohort 5000 — todos con `RESOURCE_LIMIT` antes de ejecutar. SIGINT → cancelación limpia entre batches con `ErrResourceLimit` (sin leak, proceso termina). Memoria O(workers×batch+agregadores): sin O(total_paths) sobre el umbral (histograma 2e6 OK); worker budget global = 1 (serial, sin pools anidados). Echo Front fuera de scope (incidente externo).
- **A10 Sample claims (PASS con B-02).** Las 4 celdas congeladas reproducen los valores entregados: p=.55/2000 IND net −$2,824.0 P(>0)=5.5%; p=.50/2000 net −$3,372.3; p=.60/150 net +$6,486.6 P(>0)=97.9%; PERFECT_COPY p=.55 net −$2,827.9 (media ≈ independiente) con P95 +$5,890 vs +$88 IND. Distinción declarada: reproducibilidad determinista misma-binario (cumple, F13) vs acuerdo estadístico cross-build (cumple dentro de ruido MC; diffs = 1 ULP en dp_reference, ver B-02).
- **A11 Rule semantics (PASS, sin RULE_CONTRACT_DEFECT).** Cada regla del paquete capturado §D5.2A mapea a la implementación congelada: 5 winning days ≥$150 no consecutivos (WinningDayThreshold/RequiredWinningDays, W reset por payout, día de request no cuenta); cap min(50%·B, $2,000) con gate B≥4000 (RequestGate=2) y mínimo $125 no ligante; split 90/10 → $1,800; MLL −2000 EOD-trailing con lock 0 tras bulto/tras payout (matiz EOD del día 2 absorbido por la policy owner declarada miss=MLL-breach); ganancia neta positiva desde el último payout para payouts ≥2 queda implícita y garantizada por el gate (post-payout ≥2000 < 4000 ≤ balance); renewal $49/30d y settlement latency fuera del mes normalizado (limitaciones declaradas #2/#4); máx 5 XFA coherente con 5 pipelines. Ninguna regla congelada contradice su autoridad capturada.

### Disposición solicitada

1. Owner/manager: resolver B-01 publicando `feature/d5-m1a-p150` sin mutación y reportando el SHA remoto (debe ser `1dc1fa6afaaabe99ac8648f8c11e293fa9acd17c`).
2. Manager: disponer B-02/B-03 (pueden absorberse en Shot C) y B-04..B-06 informativas.
3. Si B-01 se cierra con SHA idéntico, este informe habilita `MANAGER_REVIEW_FOR_SHOT_C` sin re-auditoría; si el SHA remoto difiere, Shot B debe re-congelarse contra el nuevo HEAD.

Gate:
- `D5_TOPSTEP_POLICY_AUDIT_B = REVIEW`
- next action: `PUBLISH_AND_VERIFY_REMOTE_SHA` → `MANAGER_REVIEW_FOR_SHOT_C`


## Manager Decision — Shot B substantive acceptance — 2026-09-24

**Verdict:** AUDIT_SUBSTANTIVELY_ACCEPTED / REMOTE_FREEZE_PENDING.

Shot B independently validated the frozen P150 implementation semantics and economic smoke results against commit `1dc1fa6afaaabe99ac8648f8c11e293fa9acd17c` in a read-only export:
- D4 regression PASS;
- state machine PASS;
- independent DP PASS;
- Monte Carlo agreement PASS;
- portfolio clock PASS;
- correlation semantics PASS;
- ledger PASS;
- resource safety PASS;
- sample claims PASS;
- captured-rule semantics PASS.

No BLOCKER or MAJOR product defect was found.

Finding disposition:
- B-01 MAJOR process: ACCEPTED as publication/chain-of-custody defect only. It does NOT invalidate the mathematical/product audit because the exact local commit was frozen and audited read-only. It MUST be closed before Shot C by publishing the branch and verifying the remote SHA is byte-identical to `1dc1fa6afaaabe99ac8648f8c11e293fa9acd17c`.
- B-02/B-03 MINOR: carry to Shot C only if source/content changes are required; B-02 has zero economic impact.
- B-04/B-05/B-06 INFO: documented limitations/observations; not blockers.

Manager gate:
- `D5_TOPSTEP_POLICY_AUDIT_B = ACCEPTED_SUBSTANTIVE`
- `D5_TOPSTEP_POLICY_RESULT_C = BLOCKED_REMOTE_FREEZE`

Interpretation:
The synthetic P150 model now has independent verification. Therefore the existence of both negative and positive economic regions in the reported smoke cells is confirmed **within the frozen synthetic model**. This is not yet an empirical trading-profit claim. The final economic decision requires Shot C's complete frozen matrix and break-even contours.

Next action:
`PUBLISH_AND_VERIFY_REMOTE_SHA` → if remote HEAD equals audited SHA exactly, immediately dispatch Shot C; otherwise re-freeze/audit the changed head before Shot C.

## Shot C — PUBLISH/FREEZE + FULL MATRIX CERTIFIED RUN — 2026-09-24

**Verdict: SHOT_C_EXECUTED — matriz completa certificada; `D5_TOPSTEP_POLICY_RESULT_C = REVIEW` (no self-accepted).** Chain of custody: audit baseline `1dc1fa6afaaabe99ac8648f8c11e293fa9acd17c` publicado en el repositorio autoridad `github.com/xKoRx/echo-futures` (repo creado privado 2026-09-24; remote SHA verificado byte-idéntico, B-01 CLOSED) → correction commit `6f7ae58` (B-03: `.gitignore` recupera `/sim` y `*.test` + regresión trivial `internal/p150/gitignore_test.go`; cero cambio de math/policy) → certified result commit `cdef2b6` (B-02: 4 samples congelados regenerados desde el build certificado; diffs 1-ULP confinados a `dp_reference`, secciones MC byte-idénticas). Remote HEAD en `cdef2b6b29502285b904fbe067d4e6aadd7d2419` verificado tras push.

Certificación re-ejecutada en cgroup sobre el commit certificado: `go test ./...` verde; `go test -race ./...` verde; D4 `sim validate` 47/47 @1e6; `sim p150-verify` 23/23; coverage `internal/p150` 96.0% (≥95%); determinismo byte-idéntico same-build (cross-build: sólo dp_reference 1-ULP = B-02 reproducido y cerrado); resource caps auto-verificados por safe-run.

Experimento ejecutado bajo protocolo congelado ANTES de ejecutar (artefactos y logs: `/home/kor/aranea/work/d5-m1a-shotc-20260924/` — PROTOCOL.md, matrices NDJSON, 240 per-cell full outputs, sweep, DP verifier). Matrices congeladas sin modificar: primary 10p×6ql×2corr, K=3, 5 pipelines, 20 sesiones, N=100k/celda, seed 424242; payout4 K=4, 40 sesiones, seed 424243. Crosscheck matriz↔per-cell byte-idéntico (CROSSCHECK OK). Break-even MC-independiente: bisección sobre EV per-attempt exacto de `ComputeDP` (verificador fuera del repo producto, export read-only `git archive`).

**Resultados owner (INDEPENDENT, K=3, 20 sesiones, 5 pipelines):** ql=150 ya es POSITIVO en el baseline p=0.50 (+$1,838/mes, P(month>0)=0.737, P5 −2,511 / P50 1,909 / P95 6,731; evals 34.2, activaciones 8.3, burns 30.1, pay1/2/3 2.30/0.39/0.00, cash externo $4,755, fees $81). El incremento pequeño que convierte la policy en positiva depende de ql: ql=150 → positivo desde p=0.50 (break-even por debajo del grid; DP per-attempt p*≈0.388); ql=300 → p*≈0.509 (MC bracket 0.50–0.51; DP 0.4705); ql=500 → p*≈0.561 (DP 0.5352); ql=1000 → p*≈0.646 (DP 0.6180); ql=1500 → p*≈0.675 (DP 0.6457); ql=2000 → p*≈0.691 (DP 0.6591). El cruzado mensual (MC) es sistemáticamente más pesimista que el per-attempt (DP) por censura del borde del mes (attempt en curso con costos pagados y payout no realizado); ambos etiquetados (EMPIRICAL_CONVERGENCE grid / RIGOROUS_BOUND per-attempt). Región negativa profunda: ql≥1000 y p≤0.60 (peor celda razonable p=0.50/ql=2000: −$3,373/mes, P(month>0)=0.016).

**Correlación:** EV esperado idéntico entre INDEPENDENT y PERFECT_COPY (diferencias <0.2%, p.ej. 1,838.5 vs 1,831.7 en p=0.50/ql=150), pero las distribuciones NO se mezclan y son cualitativamente distintas: PERFECT_COPY es lockstep — P(month>0) cae de 0.737→0.458 (p=0.50/ql=150) y 0.909→0.610 (p=0.55), P5 −5,175 vs −2,511, P95 16,465 vs 6,731: cola correlacionada bimodal. Same-day multi-MLL: eventos/mes menores en PERFECT_COPY (6.0 vs 9.2 en p=0.50/ql=150) porque los 5 pipelines tocan MLL el mismo día como UN evento multi-cuenta (diagnóstico compliance: eventos vs cuentas separados).

**Horizonte de payout:** contrafactual exacto K=4−K=3 (40 sesiones, semilla común 424242): +$230/mes (p=0.50/ql=150), +$565 (0.55/150), +$1,123 (0.60/150), +$1,908 (0.65/150), +$3,669 (0.75/150); +$5.5 (0.55/ql=2000), +$74.8 (0.60/ql=500). En el mes de 20 sesiones payout #4 es imposible por el reloj de política (22 sesiones mínimas, Shot B). Marginales per-attempt exactos (DP): en ql=150 el margen de dejar vivir a los sobrevivientes crece con p (pay3: $56→$703 por attempt de p=0.50→0.75): en el rango alto de p la rentabilidad SÍ depende de los payouts #2/#3; en ql≥1000 los horizontes son casi irrelevantes (d4 ≈ $0.01). Desviación de protocolo registrada: el dominio congelado del producto restringe max_payouts∈{3,4} (validación fail-closed), por lo que no existen corridas MC de STOP_AFTER_1/2 sin cambio de source prohibido en Shot C; los marginales #2/#3 se reportan como atribución de eventos (1770×E[pay_k]) + DP exacto K=1..4, etiquetados ATTRIBUTION_NOT_COUNTERFACTUAL.

**No probado / guardas:** modelo sintético de hit-rate (null estructural: drift 0, delta 0, sin costos de ejecución); `p_objective_hit` NO es win-rate de mercado ni evidencia empírica; settlement contado al request con fee Wire −30 y latencia diferida (B-04); renovaciones $49/30d fuera del mes normalizado; reset/Back2Funded fuera de scope; PERFECT_COPY degenera a lockstep total sin estados divergentes (B-05); qualify_loss se debita completo aunque el remanente al floor sea menor (B-06, cosmético). Compliance: same-day multi-MLL llega a 14.0 eventos/37.8 cuentas por mes en ql=2000 — señal material del patrón account-stacking que Topstep vigila. Next action: `MANAGER_REVIEW_SHOT_C` con recomendación CONDITIONAL_GO hacia el puente de realismo (estimación empírica de p_objective_hit y sesiones antes de capital).


## Manager Decision — Shot C accepted as synthetic economics result — 2026-09-25

**Verdict:** `D5_TOPSTEP_POLICY_RESULT_C = ACCEPTED_SYNTHETIC`.

The complete P150 matrix, chain of custody, independent Shot B audit, D4 regression, DP/MC consistency, resource safety, and final certified commit `cdef2b6b29502285b904fbe067d4e6aadd7d2419` are accepted as sufficient evidence for the following claim:

> Within the frozen discrete P150 policy model, Topstep economics contain a material positive-EV region. In the primary five-pipeline/20-session experiment, ql=150 is positive throughout the tested linked-p grid, including p_objective_hit=0.50 (+~$1.84k/month expected), and the break-even contour worsens sharply as qualification loss increases.

This gate does **not** authorize capital deployment or claim empirical profitability.

### Mandatory semantic correction before real-world GO

`p_objective_hit=0.50` is a synthetic session-objective probability, not a universal zero-edge/fair-market condition when target/loss distances are asymmetric.

For a driftless continuous fair process with static absorbing barriers, the candidate fair-hitting probabilities for the owner's ql=150 policy are stage-specific:
- evaluation +1500 / -2000: `p_eval,fair = 2000/(1500+2000) = 4/7 ≈ 0.5714286`;
- first XFA bulto +4000 / -2000: `p_bulto,fair = 2000/(4000+2000) = 1/3`;
- reload +2000 / -2000: `p_reload,fair = 1/2`;
- qualification +150 / -150: `p_qualify,fair = 1/2`.

Therefore the linked-p=.50 cell is NOT itself proof that a zero-edge market process beats the prop.

### Next mandatory gate — D5.4 FAIR-NULL / REALISM BRIDGE

Before GO_MVP/capital:
1. run a stage-specific fair-null experiment using the accepted session-aware model, not linked p;
2. incorporate finite-session/EOD unresolved probability rather than assuming every session hits target or loss;
3. then estimate empirical `p_eval`, `p_bulto`, `p_reload`, and `p_qualify` from the selected Gerard/mean-reversion/hardscalping strategy;
4. compare empirical confidence intervals to the certified break-even surface;
5. include execution costs and current provider compliance constraints before deployment.

Manager disposition:
- synthetic economics hypothesis: **PASS**;
- "coin/no-edge beats Topstep" hypothesis: **PROMISING, NOT YET CERTIFIED**;
- real-money MVP: **CONDITIONAL / WAIT FOR D5.4**;
- simulator/three-shot milestone: **CLOSED SUCCESSFULLY**.

Next action: `D5.4_FAIR_NULL_REALISM_BRIDGE`.

## D5.4 Fair-Null + Realism Bridge — EJECUTADO 2026-09-25

**Verdict: ejecutado completo bajo protocolo congelado pre-ejecución; `D5_FAIR_NULL_PASS = REVIEW` (no self-accepted).** Producto certificado `xKoRx/echo-futures @ cdef2b6b29502285b904fbe067d4e6aadd7d2419` (árbol limpio, source intacto; verificador externo en `/home/kor/aranea/work/d5-m1a-shotd-fairnull-20260925/` — PROTOCOL.md congelado antes de observar, configs, outputs, `verifier/partb_kernel.py`, `verifier/partc_driver.py`). Sin implementación de estrategia real, sin market calibration, sin cambio de policy P150.

### Semántica verificada

El producto expone overrides `p_eval`, `p_bulto`, `p_qualify`; la etapa reload comparte `p_qualify` (`internal/p150/account.go`, `StageProb` rama default — evidencia en source). Para ql=150 el fair reload = 1/2 coincide exactamente con el fair qualify, por lo que el override existente basta y NO se cambió source.

### Parte A — True fair null (engine certificado, seed 424244, N=100k, 5 pipelines, 20 sesiones, K=3, ql=150)

| campo | linked p=0.50 (Shot C, seed 424242) | FAIR NULL stage-specific (IND) | FAIR NULL (PERFECT_COPY) |
|---|---|---|---|
| EV mensual | +$1,838.5 | +$691.3 | +$723.6 |
| P(month>0) | 0.737 | 0.565 | 0.395 |
| P5 / P50 / P95 | −2,511 / 1,909 / 6,731 | −3,989 / 337 / 6,035 | −5,675 / −2,715 / 16,220 |
| evals / activaciones / mes | 34.2 / 8.3 | 34.9 / 11.1 | 34.9 / 11.0 |
| pay1 / pay2 / pay3 | 2.298 / 0.385 / 0.004 | 1.966 / 0.318 / 0.003 | 1.978 / 0.320 / 0.003 |
| cash externo / fees totales | $4,755 / $80.6 (settlement) | $4,048 / $3,425 (eval 1,709 + act 1,648 + settle 69) | $4,073 / $3,419 |
| DP exacto p_pass | (0.5)² = 0.25 | (4/7)² = 0.3265306… | idéntico |

Lectura: con probabilidades de primer-hit por etapa (eval 4/7, bulto 1/3, qualify/reload 1/2) el null fair MANTIENE EV positivo (+$691/mes) pero cae 62% respecto de la celda linked p=0.50: p_bulto 0.5→0.333 reduce pay1 (2.30→1.97) y p_eval 0.571>0.5 encarece activaciones (8.3→11.1 × $149) — las fees de activación consumen casi la mitad del edge aparente del linked null. Esto CERTIFICA la corrección semántica del manager: linked p=0.50 NO es zero-edge; el fair null verdadero es otra celda y es menos generosa, aunque sigue positiva por la asimetría de barreras estáticas (target más cercano que loss en eval, y cap de payout $2,000 contra fees fijos).

### Parte B — Finite session realism (kernel D5.3 exacto)

Modelo: BM driftless en reloj de varianza con barreras estáticas +G/−L; por sesión de presupuesto ν_s = ρ·L², leyes exactas de dos barreras en tiempo finito (series del kernel de calor en intervalo). Identidades PASS: conservación ≤1.1e-16; límite ν→∞ recupera los fair nulls exactos; martingala p_T·G − p_L·L + S·E[Y|surv] = 0 a ≤5e-13; límite ν→0 acotado por truncación de serie (<1e-6). Enmienda pre-ejecución registrada: por concatenación de segmentos Brownianos (Markov fuerte + barreras estáticas), P_stage_hit(n,ρ) = p_TARGET(n·ν_s) — sin DP de retícula. E[sesiones a resolución de etapa] = (G/L)/ρ.

Superficie (p_TARGET de UNA sesión, por etapa, sobre la grilla adimensional D5.3 sqrt(ρ) = σ√T / L):

| sqrt(ρ) | eval (fair .5714) | bulto (fair .3333) | qualify/reload (fair .5) | E[sesiones] eval / bulto / qual |
|---|---|---|---|---|
| 0.1 | ~0 | ~0 | ~0 | 75 / 200 / 100 |
| 0.25 | 0.0027 | ~0 | 0.0001 | 12 / 32 / 16 |
| 0.5 | 0.1336 | 0.0001 | 0.0455 | 3 / 8 / 4 |
| 1.0 | 0.4473 | 0.0454 | 0.3146 | 0.75 / 2 / 1 |
| 2.0 | 0.5704 | 0.2719 | 0.4954 | 0.19 / 0.5 / 0.25 |
| 4.0 | 0.5714 | 0.3332 | 0.5000 | 0.05 / 0.12 / 0.06 |

Traducción mensual de diagnóstico (SÓLO aproximaciones etiquetadas, no economía certificada): brazo pesimista FIRST_SESSION_RESOLVED (supervivientes tratados como pérdida completa) y brazo optimista RESOLUTION_CONDITIONAL (masa no resuelta eliminada; el proceso carried verdadero queda entre ambos): sqrt(ρ)=1 → [−$4,467, −$2,569]/mes (ambos negativos); sqrt(ρ)=2 → [−$252, +$368] (cruce de signo); sqrt(ρ)≥4 → ≈ fair null (+$691); sqrt(ρ)≤0.25 → piso de quema de fees ≈−$4.9k/−$6.8k. Conclusión: la positividad del fair null discreto NO es robusta a duración finita de sesión; se sostiene sólo cuando la sesión típicamente resuelve (σ√T ≳ 1.5–2 × loss cap). Cuál régimen es el real es una pregunta de DATOS, no de modelo. Nota declarada: las etapas con winning-day counting (qualify/reload) son además ν-sensibles en probabilidad eventual (día ganador exige PnL diario ≥$150; su probabilidad por sesión cae con ν), efecto de segundo orden no simulado aquí.

### Parte C — Edge requirement (bisección en espacio MC mensual, CRN seed 424245, N=50k, tol $25)

Margen de deterioro hasta break-even (el fair null ya está sobre 0, el break-even informativo es hacia abajo): eval −7.4pp (p_eval 0.5714→0.4974, prácticamente moneda), bulto −4.9pp, qualify −4.2pp, uniforme −1.84pp en las tres etapas. Edge ASCENDENTE sobre el fair null para objetivos mensuales (5 pipelines):

| objetivo/mes | sólo eval | sólo bulto | sólo qualify (incl. reload) | uniforme | combinado (greedy) |
|---|---|---|---|---|---|
| break-even | ya positivo (margen −7.4pp) | ya positivo (−4.9pp) | ya positivo (−4.2pp) | ya positivo (−1.84pp) | = qualify |
| +$1k | +3.7pp → p 0.608 | +2.3pp → 0.356 | +2.1pp → 0.521 | +0.84pp | +2.1pp en qualify |
| +$2k | +17.1pp → 0.742 | +10.6pp → 0.439 | +7.9pp → 0.579 | +3.2pp | +7.9pp en qualify |
| +$5k | INALCANZABLE (satura +$3,417 con p_eval→1) | +44.7pp → 0.780 | +28.8pp → 0.788 | +9.6pp | +28.8pp en qualify |

Elasticidad (marginal $/mes por +1pp, Δ=+0.01, N=100k seed 424244): qualify +$171 > bulto +$138 > eval +$89; uniforme +$406 (superaditivo). **Etapa más valiosa: qualify/reload** (parámetro compartido en el producto; se satura última; con asignación greedy todo el presupuesto de edge va ahí). El brazo sólo-eval no puede llegar a +$5k/mes ni con evaluación perfecta: el throughput de payouts lo limita p_bulto=1/3.

### Parte D — Gerard bridge (consumo de reports; ningún claim asumido)

Fuentes: [[gerard-garcia-dr]] (RESEARCH_PASS), [[tradesfera-dr]] (RESEARCH_PARTIAL), [[psicologo-del-trading-dr]] (RESEARCH_NO_GO — sin reglas mecanizables, excluido). Hipótesis falsables mecanizables sobre (p_eval, p_bulto, p_reload, p_qualify): (1) NEG_REC DCA adverso con stop a promedio [OBSERVED media] → reduce P(pérdida completa de sesión) pero aumenta frecuencia de burn al floor; medible en p_loss de etapa vs burn rate; NO_DATA. (2) Killzones / filtro time-of-day [OBSERVED media] → condiciona ν por sesión: p_T(ν_kz) > p_T(ν_all) es falsable con datos tick; NEEDS_MARKET_DATA. (3) POS_PYR piramidado con stop BE [OBSERVED media] → sesga el reparto TARGET/LOSS/SURVIVED a favor de target con cola izquierda recortada; NO_DATA. (4) VAR_RISK progresión tras pérdida [UNKNOWN] → cambia p efectiva por intento; falsable A/B contra riesgo plano; NO_DATA. (5) RAND_ENTRY "entradas al azar con gestión" [UNKNOWN, el propio report lo marca especulación] → si fuera cierto, el fair null de la Parte A ES el modelo económico directo; NO_DATA. (6) Tradesfera mean-reversion con TP corto y win-rate alto [EXPLÍCITO] → mapea a mejora de p_qualify (ventana chica 150/150) y quizá p_eval; target empírico: p_qualify ≥ 0.521 da +$1k/mes sobre fair null; el 26.7% de funding rate es self-reported (sesgo declarado); NEEDS_MARKET_DATA. (7) Selectividad "cuando no, quietos" [EXPLÍCITO] → menos sesiones/mes con p por sesión mayor; interactúa con el reloj de 20 sesiones; falsable con datos; NEEDS_MARKET_DATA. (8) R4 stop-loss desconocido → la elección de qualify_loss ya tiene superficie certificada (Shot C); la estimación empírica debe reportarse junto al ql elegido; NEEDS_MARKET_DATA.

### Decisión (bloque fijo)

- **FAIR_NULL_EV:** +$691/mes INDEPENDENT (+$724 PERFECT_COPY); 5 pipelines, 20 sesiones, K=3, ql=150, seed 424244, N=100k — positivo pero −62% vs linked p=0.50.
- **FAIR_NULL_P_POS:** 0.565 IND (0.395 PC).
- **FINITE_SESSION_RANGE:** bracket de diagnóstico [−$4,467, −$2,569]/mes en sqrt(ρ)=1; [−$252, +$368] en sqrt(ρ)=2; ≈+$691 en sqrt(ρ)≥4; piso ≈−$4.9k a −$6.8k en sqrt(ρ)≤0.25. Cruce de signo entre sqrt(ρ)≈1.4 y 2 — bracket no riguroso, etiquetado diagnóstico.
- **BREAK_EVEN_EDGE_REQUIRED:** ya sobre break-even; margen de deterioro: eval −7.4pp / bulto −4.9pp / qualify −4.2pp / uniforme −1.84pp. Ascendente: +$1k exige +2.1pp (qualify) a +3.7pp (eval); +$2k exige +7.9pp (qualify) a +17.1pp (eval); +$5k inalcanzable por eval solo.
- **MOST_VALUABLE_STAGE_TO_IMPROVE:** qualify/reload (+$171/pp; comparte parámetro con reload en el producto).
- **EMPIRICAL_TARGETS:** p_bulto ≥ 0.356 (+$1k/mes) y ≥ 0.439 (+$2k); p_qualify/reload ≥ 0.521 y ≥ 0.579; p_eval ≥ 0.608 y ≥ 0.742; uniforme fair+0.84pp / +3.2pp / +9.6pp para +1k/+2k/+5k. Toda estimación empírica debe venir con IC y ejecución/fees reales antes de comparar contra esta superficie.

**Manager recommendation: NEEDS_MARKET_DATA.** La decisión económica está bloqueada por dos preguntas que sólo datos responden: (a) el régimen de ν real (σ√T de sesión vs loss cap — la Part B muestra que el signo del null depende de eso), y (b) la estimación empírica de p_eval/p_bulto/p_reload/p_qualify con ICs de la estrategia seleccionada (Parte D: 8 hipótesis, ninguna con datos hoy). Con datos: estimar p por etapa → comparar contra esta superficie y la de break-even de Shot C → entonces GO_REAL_STRATEGY_VALIDATION o NO_GO. Verificaciones respetadas: linked p=0.50 nunca llamado zero-edge; ningún edge empírico inventado; policy P150 intocada; fair-null y calibración de mercado separados.

Gate: `D5_FAIR_NULL_PASS = REVIEW`. Next action: `MANAGER_REVIEW_D54` → decisión de adquisición de datos de mercado (tick/1m NQ-MNQ-ES-MES con timestamps y sesiones versionadas, per Parte D/§10 gerard-garcia-dr).


## Manager Decision — D5.4 Fair-Null accepted; market calibration now binding — 2026-09-25

**Verdict:** `D5_FAIR_NULL_PASS = ACCEPTED_BOUNDED`.

Accepted evidence:
- stage-specific fair-null semantics correct the linked-p=.50 simplification;
- certified P150 engine with p_eval=4/7, p_bulto=1/3, p_reload=p_qualify=1/2 remains positive in the discrete eventual-resolution experiment (~+$691/month IND, 5 pipelines, 20 sessions, ql=150);
- sensitivity/elasticity identifies qualify/reload as the highest-value stage to improve;
- no empirical edge was invented;
- source remained on certified commit and the verifier remained external.

Critical limitation:
- the positive fair-null result is NOT robust to arbitrary finite-session variance. D5.4 Part B is a diagnostic bracket, not a certified market-calibrated cash forecast.
- `rho` must be calibrated from actual instrument/session/exposure data. A common dimensionless rho across stages is a sensitivity device, not a claim that real dollar variance scales with each stage loss cap.
- unresolved-to-EOD paths must be represented using actual session data / the accepted session-aware model before capital deployment.

Manager interpretation:
- structural prop asymmetry under a truly driftless first-hitting process: **SUPPORTED**;
- monthly profitability under real NQ/MNQ/ES/MES sessions: **UNKNOWN UNTIL DATA**;
- Gerard/mean-reversion edge requirement appears modest in the low-ql regime, but stage probabilities must be estimated empirically with confidence intervals;
- no further generic simulator architecture is authorized before calibration.

New gate:
- `D5_MARKET_CALIBRATION_PASS = BLOCKED_DATA`.

Mandatory next work:
1. acquire/identify historical futures data for the exact target instruments and trading windows;
2. measure realized variance-clock distributions by session/window;
3. map those distributions to stage-specific `rho_eval`, `rho_bulto`, `rho_reload`, `rho_qualify`;
4. replay the P150 lifecycle with TARGET/LOSS/SURVIVED_TO_EOD rather than diagnostic bracketing;
5. only after that, test Gerard/Tradesfera entry/management rules and estimate empirical stage hit probabilities with confidence intervals and costs.

Capital decision remains:
`REAL_MONEY_MVP = WAIT_FOR_D5_MARKET_CALIBRATION`.

Next action:
`D5.5_MARKET_DATA_AND_SESSION_CALIBRATION`.

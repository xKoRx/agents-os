---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[EF-CAMPAIGN-MODES-I0-LOCAL]]"
  - "[[EF-CAMPAIGN-MODES-I0-IMPLEMENTATION-RETURN]]"
  - "[[EF-CAMPAIGN-MODES-DESIGN]]"
  - "[[EF-S04-INTEGRATION-RECONCILIATION]]"
  - "[[Echo Futures — Optimización de Campañas]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-29"
updated: "2026-10-29"
---


# EF-CAMPAIGN-MODES-I0-VERIFY-RETURN

Retorno ONE-SHOT de I0-S2 (verificación adversarial independiente). Verificador TOP LOCAL fresco (ZCode/GLM-5.3-Flash, host Hefesto); no manager, no implementador, no Owner. Producto y tests del autor READ_ONLY (sólo lecturas + `git` de inspección); harness y fixtures sintéticos en workspace propio. Cero motores de campaña, compras, trading, deploy ni mutaciones de infraestructura. PRO_CHAT_POOL_DELTA: UNKNOWN.

## STATUS

**FINDINGS** — el candidato NO alcanza VERIFY_PASS: 4 hallazgos P1 y 6 P2 confirmados de forma independiente (reproducibles), más 1 P3. La arquitectura cumple el contrato de proyección (proyección pura, sin spawn/egress, legacy intacto, scopes separados) y la E2E real R03 concilia correctamente, pero la exactitud económica del proyector falla en los caminos con refund, linaje de conversión, fase funded y cutoff. Los falsificadores confirmados NO están cubiertos por la suite del autor (34/34 pasa con los defectos presentes): cobertura ≠ exactitud económica, demostrado empíricamente en un módulo con 99,8% de coverage declarado. Sin corrección de producto por este shot; el manager adjudica y emite I0-S3.

## BASE_SHA / CANDIDATE_SHA

- BASE_SHA: `2baf319ddcba622d9557bc9f23a13787b44c58a7` — verificado ancestro directo del candidato (`git merge-base --is-ancestor` PASS); dos commits del implementador (`a324fda9` implementación, `b964e13d` verificación del autor).
- CANDIDATE_SHA: `b964e13df59e20b06349eb7e0ad4f4ed057d04a0` — HEAD de `feature/ef-campaign-modes-i0` en worktree `~/go/src/github.com/xKoRx/echo-i0`, readback `origin/feature/ef-campaign-modes-i0 == HEAD` verificado. Sin reset/merge/rebase; trabajo ajeno intacto (checkouts `echo`, `echo-clf`, `echo-integration` no tocados). Único estado sin trackear: `__pycache__` del propio módulo (bytecode, no código).

## SOURCE_DIFF

`git diff 2baf319d..b964e13d`: CREATE `economics_report.py` (621 líneas), CREATE `test_economics_report.py` (515), MODIFY `research_lab.py` (+19/−1), CREATE 4 artefactos SDD `specs/FEAT-CHALLENGE-HISTORY/changes/CHANGE-001-*`. Coincide con lo declarado por S1: el delta a `research_lab.py` es exactamente `cmd_economics` + wiring del subcomando opt-in (inspeccionado hunk por hunk; `run`/`resume`/`_run_one`/`_census`/`characterize`/`adjudicate`/selector 25% byte-idénticos). Ningún cambio en SDK/Core/driver Go, catálogos, presets ni planes sellados.

## INDEPENDENT_E2E

Ejecutado el CLI real `research_lab.py economics --attempt ~/echo-work/runs/R03-PROTECTED-CLOSE/lab/LAB-SG-ORB-CH300-30M-R750` como proceso de producción, dos corridas: exit 0 ambas, salida **byte-idéntica** (`cmp`). Resultado conciliado contra una reconciliación independiente escrita desde la evidencia cruda (sin reutilizar helpers del reporter): `cash_final` declarado 0 USD == proyectado independiente 0 USD == residual 0; `eval_cost_gross` 8040 USD == PURCHASE 6960 + RENEWAL 1080 independiente; U=58 == cuentas con cargo distintas; P_U=10 == pass_events distintos; cost_per_pass 804 USD == `research_funding.cost_per_pass` declarado; q NOT_OBSERVED con razón localizada (sin payout en scope); aggregate NOT_COMPOSABLE; umbral THRESHOLD_NOT_ADJUDICATED (sin adjudicación automática del 1/3). CAMPAIGN_OPEN 5000 USD tratado como magnitud de apertura para conciliación, no como adjudicación de caja disponible; identidad de instancia (campaign_id + sha256 del receipt), scope ISOLATED y simulation_scope UNKNOWN conservados. Determinismo, no-spawn y bytes sellados: ver abajo.

## FINDINGS

Disposición por falsificador (esperado / real / localizador / fixture / disposición). Fixtures en `~/echo-work/i0-s2-verify/fixtures/`; registro consolidado `~/echo-work/i0-s2-verify/verify_findings.json` (sha256 `2e1ac2c0f022213e…`). Semántica de referencia verificada en el contrato Go sellado `v3/backtester/platform_campaign.go` del mismo candidato.

### P1 (bloquean READY_FOR_OWNER_REVIEW)

- **F1 (E1) — La identidad de cash ignora los REFUND: residual contable falso.** Esperado: opening 200 + compra 100 + refund 100 + final declarado 200 ⇒ residual 0 y coste neto 0. Real: `cash_identity_residual = 100 USD` (`cash_final_projected = 100 USD`); el coste neto sí es correcto (`eval_cost_net = 0 USD`). Causa: la fórmula de `cash_residual` y `cash_final_projected` usa `eval_cost_gross` y no incluye término refund (`economics_report.py:254-255` y `:434`); la clase REFUND existe pero no entra en la identidad. Fixture `fixtures/e1_refund.json`. Corrección mínima: sumar `refunds` (o sustituir gross por net) en la identidad proyectada y documentar la clase REFUND en la misma.
- **F2 (E2/E2r) — Q se adjudica con `paid_out` solamente, sin linaje pase/activación.** Esperado: compra + crédito de payout sobre AccountID coincidente pero sin pase challenge y sin activación funded ⇒ NO declarar conversión compra→primer cobro. Real (forma realista de Go, donde un pago acreditado emite también `PAYOUT_COLLECTED`, `platform_campaign.go:861`): `Q=1, q_roots=['A1'], status=OBSERVED, q=1/1`. Causa: el bucle de q_roots exige únicamente `paid_out`; `passed` y `activated` se calculan y quedan muertos (`economics_report.py:369-381`), contradiciendo el linaje compra→intento→pase→activación→payout declarado en C04 y en el propio mensaje de commit. Fixture `fixtures/e2r_q_real.json` (y `e2_q_lineage.json`). Corrección mínima: exigir `passed and activated` para q_roots; sin esa demostración, derivar a `lineage_gaps`/status INCOMPLETE_LINEAGE (nunca OBSERVED).
- **F3 (E3) — `review_at` (pre-activación) cuenta como funded iniciada.** Esperado: cuenta con `review_at` y estado `PASS_REVIEW`, sin activación funded ⇒ NO entre las funded iniciadas. Real: `N_funded_initiated = 1`. Causa: `_account_funded_evidence` acepta `review_at` y `credentials_at` como evidencia (`economics_report.py:199-201`, y `funded_since` `:341-349`); el contrato Go muestra que el ciclo real es PASS_REVIEW(review_at) → CREDENTIALS_PENDING(credentials_at) → recién entonces `activateFunded`/`CompliantAt` (`platform_campaign.go:680-692`), por lo que ambos timestamps son PRE-activación y su uso infla N_funded_initiated y la frontera de fase. Fixture `fixtures/e3_review.json`. Corrección mínima: eliminar `review_at`/`credentials_at` de la evidencia funded (conservar `compliant_at`, stage LIVESIM, `gross_paid>0`, `payouts>0`, estados funded) y alinear `funded_since` con la misma frontera.
- **F4 (E4) — Conciliación con cutoff compara proyección parcial contra `cash_final` terminal: residual falso.** Esperado: con un efecto post-cutoff, conciliar contra el saldo observado al cutoff o declarar evidencia insuficiente; no informar el residual como error contable del motor. Real: compra post-cutoff de 100 ⇒ `cash_identity_residual = -100 USD` con `post_cutoff_effects_excluded=1` (el efecto quedó excluido de métricas pero el `cash_final` declarado es terminal). Causa: `cash_residual = declared_cash_final − proyección(live)` sin referencia de frontera; la variable `cash_after_final` (último saldo observado) se calcula y queda muerta en `economics_report.py:247-255`. Fixture `fixtures/e4_cutoff.json`. Corrección mínima: cuando `cutoff_applied` y existen efectos post-cutoff, reconciliar contra el último `cash_after` observado ≤ cutoff o emitir `UNKNOWN (frontier mismatch)`; jamás un residual firmado como mismatch contable.

### P2

- **F5 (E5a) — `_ts` es comparación lexicográfica y no normaliza offsets RFC3339.** Esperado: `2026-03-01T01:00:00+02:00` (= 2026-02-28T23:00Z) antes de cutoff `2026-03-01T00:00:00Z` se incluye, y `2026-02-28T23:30:00-01:00` (= 2026-03-01T00:30Z) se excluye. Real: al revés (el primero excluido como post_cutoff, el segundo incluido); `eval_cost_gross = 200 USD` vs 100 correcto. Causa: `_ts` devuelve el string sin normalizar (`economics_report.py:129-134`); `post_cutoff` y `credited_before_cutoff` comparan strings (`:177`, `:194`, `:287`). Fixture `fixtures/e5_ts.json`. Corrección mínima: normalizar a UTC (parseo RFC3339) antes de comparar; timestamp no parseable ⇒ UNKNOWN, no orden posicional.
- **F6 (E5b) — Los efectos post-cutoff NO permanecen listados en el reporte.** Esperado (docstring del módulo `:142` y help del CLI «stay listed but excluded from metrics»): aparecen con `post_cutoff=true`. Real: el efecto desaparece del output; sólo queda el contador `post_cutoff_effects_excluded`. Causa: `project_campaign` reasigna `effects = live` y el retorno publica esa lista (`economics_report.py:220-222`, `:507`). Fixture `fixtures/e5_ts.json` (efecto `e5-a`). Corrección mínima: publicar la lista completa con el flag `post_cutoff` (el docstring ya describe ese contrato).
- **F7 (E5c) — Evento sin timestamp se cuenta bajo cutoff sin marca.** Esperado: respecto a un cutoff aplicado, un efecto sin `at` es UNKNOWN en la frontera, no inclusión silenciosa. Real: `post_cutoff=False` ⇒ entra en métricas sin flag alguno. Causa: `bool(cutoff and at and at > cutoff)` degrada «desconocido» a «antes del cutoff» (`economics_report.py:177`). Fixture `fixtures/e5_ts.json` (efecto `e5-c`). Corrección mínima: `cutoff_relation: UNKNOWN` visible y conteo en `completeness` cuando `at` falta con cutoff aplicado.
- **F8 (E6) — Fees de activación computan como gasto operativo funded.** Esperado: el fee de setup/activación pagado tras credenciales pero antes de la activación funded NO computa como `F_op` funded. Real: `F_op_funded_external = 500 USD` (STOW_FEE 400 + PLATFORM_FEE 100). Causa: `funded_since` devuelve `credentials_at` y clasifica con `e.at >= since` (`economics_report.py:341-358`); en el flujo Go real los setup fees se cobran exactamente en ese intervalo, en el tick previo a `activateFunded` (`platform_campaign.go:684-692` y `1276-1293`), por lo que con evidencia realista el falso positivo ocurre siempre. Fixture `fixtures/e6_fee.json`. Corrección mínima: frontera de fase = activación (`compliant_at`/LIVESIM), no credenciales; o excluir los fees de setup de `F_op` funded y clasificarlos como coste de activación.
- **F9 (E8) — Revisiones vs ejecuciones distintas son indistinguibles y el gasto no vigente desaparece del total.** Esperado: distinguir revisión del mismo receipt de una ejecución distinta (run_id/attempt dir) o declarar UNKNOWN; el gasto real de ambas ejecuciones no debe salir de los totales sin rastro. Real: dos attempts con mismo `campaign_id`, `run_id` distinto y bytes distintos se colapsan como revisiones; `total_visible_eval_cost_net_current = 100 USD` y los 200 USD de la ejecución no vigente no aparecen en ningún total (quedan sólo listados en `all_revisions`), sin UNKNOWN de relación física. Causa: la política de revisión usa únicamente campaign_id + bytes (`economics_report.py:563-589`, totales `:597-600`); run_id se reporta pero no participa. Fixtures `fixtures/e8_attempt_alpha.json` + `e8_attempt_beta.json`. Corrección mínima: si difiere `run_id`/attempt dir ⇒ ejecución separada o `UNKNOWN_EXECUTION_RELATION`; totalizar también las revisiones no vigentes (spend visible por revisión).
- **F10 (E2c) — Crédito presente pero no atribuible ⇒ «cero observado» fabricado.** Esperado: crédito en cash-events con pagos atribuidos a una cuenta externa ⇒ atribución UNKNOWN (distinguir cero observado de ausencia de observación). Real: `Q=0, status=OBSERVED, q=0/1`. Causa: con `credits>0`, sin q_roots y sin gaps (el gap exige `not payments`), la cascada cae en `OBSERVED` (`economics_report.py:383-390`). Fixture `fixtures/e2c_q_attrib.json`. Corrección mínima: cuando hay efecto de payout sin raíz atribuible ⇒ status UNKNOWN/INCOMPLETE_LINEAGE; OBSERVED sólo con linaje demostrado.

### P3 (menor, no bloquea por sí solo)

- **F11 — `sums_by_assignment_reconcile: True` es una constante.** Se emite sin cálculo y no refleja conflictos (`economics_report.py:435`). Corrección mínima: derivarla de los agregados o renombrarla como declaración estática.
- **Contraste E2 (Q=1 con status NOT_OBSERVED):** con un pago CREDITED sin cash-effect de payout, el reporte entrega `q_roots=['A1']` (Q=1) junto a `status=NOT_OBSERVED` (`fixtures/e2_q_lineage.json`): los dos campos se contradicen en el mismo documento. Misma raíz que F2/F10.

### REFUTED (falsificadores no sostenidos)

- **E7 — compras repetidas/bundles: comportamiento correcto.** Dos PURCHASE del mismo AccountID ⇒ raíz única con `repeat_charges` visible, bundle `units_declared=2` suma 2, bundle sin cardinalidad ⇒ UNKNOWN_CARDINALITY con denominador `None` (sin denominador favorable inventado), compra pagada no provisionada permanece en U. Fixture `fixtures/e7_units.json`.
- **E8b — re-lectura del mismo receipt: idempotente.** Mismo archivo dos veces ⇒ 1 campaign, `re_read_receipts_ignored=1`, sin duplicación de efectos.

## REPRO_REFS

- Harness: `~/echo-work/i0-s2-verify/` (persistente en host) — `fixtures_e1_e4.json.py` (sha256 `fd7bcc02d9d4ecec…`), `fixtures_e2e8.py` (`b6ded2856c7c94c9…`), `sentinel_no_spawn.py` (`d3cb3b5439fc5d21…`), `verify_findings.json` (`2e1ac2c0f022213e…`), `e2e_run1.json` (`48719a0f7cca4f78…`). Los fixtures importan el módulo del candidato por path (lectura); las expectativas independientes están calculadas a mano en cada script, no mediante helpers del autor.
- E2E: `python3 …/campaign-lab/research_lab.py economics --attempt ~/echo-work/runs/R03-PROTECTED-CLOSE/lab/LAB-SG-ORB-CH300-30M-R750 --out <out>` ×2 + `cmp`.
- Sentencia Go de referencia: `v3/backtester/platform_campaign.go:680-692` (PASS_REVIEW→CREDENTIALS_PENDING→activateFunded), `:861` (pago acreditado emite PAYOUT_COLLECTED), `:1276-1293` (setup fees pre-activación).
- Clasificación de activos: fixtures E1–E6/E8 = DISPOSABLE_REPRODUCER hoy, PERMANENT_REGRESSION_CANDIDATE al corregirse (protegen residual, linaje Q, frontera funded, cutoff y offsets); `sentinel_no_spawn.py` = HARNESS_TOOLKIT_CANDIDATE; comando E2E R03 doble corrida = E2E_CANDIDATE (ya propuesto por S1; reproducción independiente verificada aquí).

## LEGACY_COMPATIBILITY

DEMONSTRADO en esta sesión: suites del lab re-ejecutadas en el candidato — `test_economics_report` 34/34 OK y `test_campaign_lab + test_research_lab + test_s02_trials + test_s02_trials_reconcile` 124/124 OK. Diff auditado: selector 25%, `_census`, `characterize`, `adjudicate`, `run`/`resume` byte-idénticos; sin reinterpretación de 25%/5.000/120/4 payouts ni de V1/Unclipped en el código nuevo. El reporte nuevo no alimenta al selector (verificado por diff y por flujo: `cmd_economics` sólo lee y escribe `--out`).

## NO_SPAWN

DEMONSTRADO por tres vías independientes: (1) imports del módulo: sólo `hashlib`, `json`, `decimal`, `fractions`, `pathlib` (sin subprocess/socket/os.system/Popen); (2) sentinel dinámico propio en wrapper (`sentinel_no_spawn.py`: Popen/run/check_*, os.system/execv*/fork/posix_spawn/spawnv, socket.socket/create_connection/getaddrinfo sustituidos por excepciones antes de importar el CLI) ejecutando el subcomando real: exit 0 y salida idéntica a la corrida plana; (3) sin imports del SDK/Go ni invocación de run/resume en el camino de `economics` (diff + lectura). Inputs sellados byte-intactos: sha256 de `result.json` (`37b1bcad…`), `plan.json` y `receipt.json` idénticos antes/después de las corridas.

## COVERAGE

99,8% statement del módulo nuevo: EXECUTOR_REPORTED (no re-medido en este shot; `pip3`/coverage ausentes, método `sys.settrace` del autor no re-ejecutado). La cobertura no se acepta como demostración de exactitud económica: los 10 hallazgos F1–F10 viven dentro del módulo cubierto y la suite del autor pasa 34/34 con todos ellos presentes, porque los tests del autor codifican el mismo criterio defectuoso que el código (mismo oráculo, no contraejemplos). Los caminos críticos rotos (identidad de cash, linaje Q, frontera funded, cutoff) exigen contraejemplos independientes — provistos en REPRO_REFS para I0-S3.

## S04_REMAINING

Censo V1 de S04-F01 RECONOCIDO en sus términos (EXECUTOR_REPORTED, conservado con localizadores del retorno S1: planes r4 52/52, r5 15/15, hefesto 5/5, R01 26/26, todos `STRATEGIC_ENTRY_BUDGET_V1`; SG desparejadas): no reabierto, sin re-ejecución de campañas. Pendiente de aceptación S04: equivalencia de intérprete V1 linaje vs master exactamente en R>headroom positivo (fixture Go de frontera, FUERA de Allowed Files de I0 — dependencia registrada, alcance: test Go + superficie de test, sin tocar `STRATEGIC_ENTRY_BUDGET_V1`, `MM_ENTRY_BUDGET_UNCLIPPED_V1` ni `qualification_guard`). S04-F02 sigue CONFIRMED con seam declarado no portado. La prueba Go de frontera es otro incremento; este shot sólo registra dependencia y alcance.

## NOT_EXECUTED

Suites Go de producto y `-race` (sin gcc en host); fixture Go de frontera S04-F01; port del guard de cualificación; campañas/compras/trading/deploy; GOD-COMPOSITION; re-medición de coverage; persistencia git del vault en esta superficie (ver UNKNOWN).

## UNKNOWN

- PRO_CHAT_POOL_DELTA: UNKNOWN (no observable desde este shot).
- Relación física entre dos attempts con mismo campaign_id y bytes distintos (revisión vs ejecución distinta): UNKNOWN por diseño actual — es exactamente el defecto F9; la corrección debe decidir o declarar.
- Persistencia git de agents-os en esta superficie: el vault `main/` no tiene `.git` accesible en este host/sesión (verificado hasta la raíz), por lo que el paso «master directo con HEAD reconciliado + readback remoto» no pudo ejecutarse; los archivos quedan persistidos create-only en el vault y el delta queda declarado aquí. No se inventa SHA remoto (regla del paquete I0-LOCAL). Fricción registrada en feedback.
- Equivalencia de intérprete V1 (heredada de S04, fuera de alcance).
- W por cuenta cuando `payments[]` no atribuye créditos (residual visible declarado por el propio reporter; no re-verificado con evidencia real que lo contenga).

## NEXT

1. **Manager adjudica F1–F11** (severidad y alcance de corrección); recomendación: F1–F4 son bloqueantes de READY_FOR_OWNER_REVIEW (residual falso, Q sin linaje, funded inflada, cutoff mal conciliado); F5–F10 correctivos en el mismo pase de I0-S3; F11 cosmético.
2. **I0-S3** (GLM LOCAL fresco, ≤120 min) corrige sobre el mismo SHA base y candidate verificados aquí, integrando los falsificadores de `~/echo-work/i0-s2-verify/` como regresiones permanentes (los que demostraron defectos se conservan tal cual), con gate completo re-ejecutado (34+N tests, 124 suites, E2E doble, sentinel).
3. Re-verificación independiente sólo del delta corregido puede ser focal (los REFUTED E7/E8b no requieren repetición si su código no cambia).
4. El manager y el programa Echo Futures permanecen abiertos; sin autoaceptación de gate Owner desde este shot.

## AGENTS_OS_PATHS_SHA

- `10-projects/Echo Futures/artifacts/backtester/EF-CAMPAIGN-MODES-I0-VERIFY-RETURN.md` (este archivo, create)
- `80-agents/journal/agent-runs/2026-10-29-zcode-glm-5.3-flash-echo-campaign-modes-i0-s2.md` (create)
- `80-agents/journal/logs/2026-10-29-echo-campaign-modes-i0-s2.md` (create, change_log)
- Commit Agents-OS: NOT_EXECUTED (vault sin `.git` accesible en esta superficie; ver UNKNOWN).

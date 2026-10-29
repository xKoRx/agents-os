---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[EF-CAMPAIGN-MODES-DESIGN]]"
  - "[[EF-CAMPAIGN-MODES-I0-LOCAL]]"
  - "[[EF-S04-INTEGRATION-RECONCILIATION]]"
  - "[[Echo Futures — Optimización de Campañas]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-28"
updated: "2026-10-28"
---

# EF-CAMPAIGN-MODES-I0-IMPLEMENTATION-RETURN

Retorno ONE-SHOT de I0-S1 (contrato/reporting económico opt-in). Ejecutor GLM-5.3-Flash LOCAL en Hefesto vía ZCode; ROLE NORMAL; un writer; cero motores de campaña, compras, trading ni deploy. Estado entregado: **IMPLEMENTATION_CANDIDATE** (no autoacepta gate Owner; verificación adversarial I0-S2 pendiente). Agent model: `account:zai-individual-coding-plan/GLM-5.3-Flash` (identificador efectivo del host); PRO_CHAT_POOL_DELTA: UNKNOWN.

## STATUS

`IMPLEMENTATION_CANDIDATE` — candidato de producto completo, E2E real conciliado, sin verificación independiente (I0-S2 NOT_DISPATCHED) y sin aceptación Owner.

## BASE_SHA / BRANCH_REAL / CANDIDATE_SHA

- BASE_SHA: `2baf319ddcba622d9557bc9f23a13787b44c58a7` (verificado: master = integration/backtest-runtime = origin/master al inicio; sin repetir merge/reset).
- BRANCH_REAL: `feature/ef-campaign-modes-i0` (NO existía; creada desde el SHA exacto en worktree nuevo `~/go/src/github.com/xKoRx/echo-i0`; checkouts `echo` (s04@ae1b09bc), `echo-clf` (3c0c683c) y `echo-integration` (2baf319d) sin tocar; WIP ajeno: ninguno).
- CANDIDATE_SHA: `b964e13df59e20b06349eb7e0ad4f4ed057d04a0` (HEAD de la rama tras push, con readback `origin/feature/ef-campaign-modes-i0 == HEAD`); commit de implementación `a324fda9` (padre directo de la base).

## DIFF_SCOPE

- CREATE `v3/backtester/tools/tradesgerard/campaign-lab/economics_report.py` — proyección pura (sin subprocess/red/reloj/randomness).
- CREATE `v3/backtester/tools/tradesgerard/campaign-lab/test_economics_report.py` — 34 tests de contrato.
- MODIFY `v3/backtester/tools/tradesgerard/campaign-lab/research_lab.py` — sólo `cmd_economics` + subcomando `economics` (opt-in; run/resume/_run_one/_census/characterize/adjudicate/prepare intactos).
- CREATE `specs/FEAT-CHALLENGE-HISTORY/changes/CHANGE-001-campaign-modes-i0-economics{,.PLAN,.TASKS,.VERIFICATION}.md` — artefactos SDD del change bajo la feature existente.
- READ_ONLY verificado: SDK/Core/driver Go, `catalog-v1.json`, `R02-HISTORICAL-MANIFEST.json`, presets, planes/receipts sellados, tests existentes, `campaign_lab.py`, `s02_trials.py`, guard (no existe en el corte).

## SPEC_PLAN_TASKS_REFS

SPEC/PLAN/TASKS/VERIFICATION materializados ANTES de código: `specs/FEAT-CHALLENGE-HISTORY/changes/CHANGE-001-campaign-modes-i0-economics.md` (delta + mapping §4.2 + GWT), `.PLAN.md` (Allowed/New/Prohibited Files + estrategia + rollback), `.TASKS.md` (T1–T8), `.VERIFICATION.md` (evidencia del autor). Sin segunda SPEC contradictoria de FEAT-CHALLENGE-HISTORY; autoridad de diseño enlazada (C04 §§4.2, 5–7, 14, 17).

## S04_SOURCE / BUILD / TEST / ACCEPTANCE / DEPLOY

| Eje | Estado | Nota |
|---|---|---|
| SOURCE | DEMONSTRADO (pre-existente, 2baf319d) | No se repitió; usado read-only |
| BUILD | EXECUTOR_REPORTED (sin delta nuevo de este shot) | No se reconstruyó producto |
| TEST | EXECUTOR_REPORTED para suites Go; suites del lab re-ejecutadas locales | 124/124 OK en este corte |
| ACCEPTANCE | ABIERTA | S04-F01 ahora DEMONSTRATED_AT_PLAN_LEVEL (ver abajo); equivalencia de intérprete NO demostrada |
| DEPLOY | NOT_EXECUTED | Ninguno; PROD congelado |

## S04_F01_DISPOSITION — DEMONSTRATED_AT_PLAN_LEVEL (hallazgo material confirmado)

Censo de planes efectivos sellados de las 26 nativas por `entry_budget_policy` + hash (sin re-ejecutar campañas):

| Root | Planes nativas | entry_budget_policy |
|---|---|---|
| `~/echo-work/runs/challenge-history-20261018-r4/plans/{FULL,CANARY}/*/plan.json` | 52 (26+26) | `STRATEGIC_ENTRY_BUDGET_V1` 52/52 |
| `.../challenge-history-20261018-r5/plans/*/plan.json` | 15 | V1 15/15 |
| `.../challenge-history-20261018-hefesto/plans/*/plan.json` | 5 | V1 5/5 |
| `~/echo-work/runs/R01-HIST-20261021/lab/LAB-NATIVE-*/plan.json` | 26 | V1 26/26 |

Las variantes SG llevan el campo ausente (desparejado por contrato). **La afirmación del retorno de integración «nativos = shrink legacy con entry_budget_policy vacío» queda refutada a nivel de planes efectivos.** Consecuencia directa: los resultados históricos nativos corrieron bajo el intérprete del linaje (ae1b09bc: V1 sin pre-veto, `head` sólo como evidencia; el finalizer resuelve la sala), mientras master 2baf319d define V1 como decline del manager (`TG_ENTRY_BUDGET_EXCEEDS_HEADROOM`); por tanto la equivalencia NO está demostrada exactamente cuando riesgo solicitado > headroom positivo. Alcance exacto restante: fixture Go de frontera (R>headroom+, igualdad, floor cruzado, controles) requiere superficie de test Go FUERA de los Allowed Files de I0 → registrado para la adjudicación de aceptación S04; sin migración V1→Unclipped, sin cambio de runtime, los receipts históricos conservan su intérprete. Censo completo con hashes en `/tmp/s04-f01-census.json` (volcado de resumen en el change_log del día).

## S04_F02_DISPOSITION — CONFIRMED (seam registrado, no portado)

`qualification_guard.py` ausente en 2baf319d (verificado en el worktree del slice). Seam para adaptación posterior: `research_lab.py::_run_one` (subprocess.run directo, línea ~720) y `resume --execute` (mismo camino). I0 NO lo importa ni lo salta; el reporter es no-spawn y no convierte esto en permiso de lanzamiento. Requisito previo de I1/I2a (cualquier ejecución futura exige portar/adaptar el guard por cambio explícito).

## COVERAGE / INPUT_CHECKSUMS

- Statement coverage módulo nuevo: 514/515 = **99,8%** (piso 95%; única línea fuera: guarda trivial `return None` de `funded_since`). Críticas primero: identidad/dedup/conflictos/cutoff/linaje cubiertas por tests dedicados.
- Suites del lab sin regresión: `test_campaign_lab + test_research_lab + test_s02_trials + test_s02_trials_reconcile` = 124/124 OK.
- Inputs sellados byte-intactos (sha256, sólo lectura): result.json `37b1bcad…`, receipt.json `e36f48c6…`, plan.json `a03a4d18…` (attempt E2E); catálogo census `3bb019a9…`.

## TEST_COMMANDS_AND_RECEIPTS

```
python3 -m unittest test_economics_report            # OK 34/34
python3 -m unittest test_campaign_lab test_research_lab test_s02_trials test_s02_trials_reconcile   # OK 124/124
python3 research_lab.py economics --attempt ~/echo-work/runs/R03-PROTECTED-CLOSE/lab/LAB-SG-ORB-CH300-30M-R750 --out /tmp/i0-e2e-run1.json   # exit 0, ~1.0s
python3 research_lab.py economics --attempt <mismo> --out /tmp/i0-e2e-run2.json && cmp run1 run2       # BYTE-IDÉNTICO
```

## REPORT_EXAMPLES (E2E real, no sintético)

Attempt `R03-PROTECTED-CLOSE/lab/LAB-SG-ORB-CH300-30M-R750` (CHALLENGE_ONLY + ResearchCostAccumulationV1):
- identity: campaign_id `campaign-lab-s04-lab-sg-orb-ch300-30m-r750`, mode CHALLENGE_ONLY → interpretación pública CHALLENGE; scope ISOLATED; instrument NQ; window UNKNOWN (localizado).
- units: **U=58** (58 cargos PURCHASE con cuenta; U_status KNOWN); eval_cost gross/net **8.040 USD**; sin refunds.
- challenge: **P_U=10**; pass_fraction_per_unit = 10/58 (numerator/denominator exactos + fracción reducida 5/29); **cost_per_pass = 804 USD** == `research_funding.cost_per_pass` declarado del result.
- reconciliation: **cash_identity_residual = 0 USD** (cash_final proyectado 0 == declarado 0); 94 efectos; 1 sin EventID (CAMPAIGN_OPEN, OPENING sin flujo); 0 conflictos; 0 duplicados.
- conversion: **q NOT_OBSERVED** (`NO_PAYOUT_EFFECT_OBSERVED_IN_SCOPE`) — nunca 0 ni fabricado.
- aggregate entre campañas: `NOT_COMPOSABLE`; umbral: `THRESHOLD_NOT_ADJUDICATED`.
- Determinismo: doble corrida byte-idéntica (`cmp`); sentinel dinámico no-spawn/egress PASS (Popen/run/system/execv/socket parcheados); sin imports de red/proceso en el módulo.

## IDENTITY_SCOPE_MAPPING (C04 §4.2 → implementado)

Definición = (campaign_mode + campaign_policy + research_cash_policy + digest canónico del request); instancia = campaign_id **con scope key (campaign_id, sha256 result)** — no se asume unicidad global; ejecución = run_id derivado (no prueba ejecución física) + attempt dir; revisión = sha256 del result; efectos = EventID/CauseID/AccountID cuando Go los emitió (researchCharge), sino UNKNOWN localizado; deduplicación e idempotencia SÓLO dentro del scope; relacturas del mismo SHA ignoradas (contador visible); revisión posterior (mismo campaign_id, bytes distintos) sustituye el derivado y conserva todas las revisiones listadas; comparación = ISOLATED por artefacto; batch independiente NUNCA se etiqueta SIMULATION; tiempo económico = `at` de eventos/pass_events, orden de archivo preservado (sin reordenar por timestamp); cutoff excluye sin anticipar.

## RECEIPT_REVISION_POLICY

Re-lectura del mismo receipt (mismo SHA) ⇒ idempotente, efectos no duplicados. Mismo campaign_id con SHA distinto ⇒ revisión: la última en el orden de entrada es la derivación vigente (`is_current_revision`), las anteriores quedan listadas en `all_revisions`; el agregado sólo consume derivaciones vigentes; ninguna revisión fabrica una compra. Mismo EventID con términos distintos ⇒ CONFLICTO visible sin mutación; idéntico ⇒ idempotente.

## LEGACY_TO_PROJECTION_MAPPING

`cash_events` (CAMPAIGN_OPEN/PURCHASE/RENEWAL/STOW_FEE/PLATFORM_FEE/EXTERNAL_RESEARCH_CONTRIBUTION/PAYOUT_COLLECTED) → clases OPENING/EVAL_COST/EXTERNAL_COST/FINANCING/PAYOUT_CREDIT; `payments[]` (REQUESTED→APPROVED→DEBIT_PENDING→PROCESSED→CREDITED/REJECTED_RULE, ID `<account>/payout/<seq>`) → ciclo de pago (approved-only ≠ caja); `pass_events` → P_U acotado por cutoff; `accounts[]` → U/provisión/estados (paridad de vocabulario testeada contra research_lab); `research_funding` declarado → conciliación. CAMPAIGN legacy funcional, 25%, 5.000, 4 payouts, V1/Unclipped, ResearchCash, FIRST_PASS: sin reinterpretación (identidades conservadas).

## NO_SPAWN_EVIDENCE

Test dinámico (subprocess.Popen/run, os.system/execv, socket.socket/create_connection parcheados → build_report completa); módulo sin imports subprocess/socket/urllib/http; CLI `economics` delega a `build_report`/`write_report` y no invoca run/resume; E2E real ejecutado como proceso con exit 0 y sin engines.

## LEGACY_COMPATIBILITY

124/124 suites del lab existentes OK en el candidato; `_census`/`characterize`/`row_from_char`/`adjudicate` y el selector 25% byte-idénticos (sin delta en el diff); defaults y receipts históricos intactos.

## NOT_EXECUTED

Fixture Go de frontera S04-F01 (fuera de Allowed Files); guard de cualificación (no existe en el corte; no portado); I0-S2 (verificación adversarial), I0-S3, GOD-COMPOSITION; campañas/compras/trading/deploy; suites Go de producto; tests `-race` (sin gcc en host); coverage de `research_lab.py` completo (delta propio sin ramas críticas).

## UNKNOWN

Equivalencia de intérprete V1 entre linaje y master (sólo la divergencia source está demostrada); window/instrument para artifacts que no los declaran (UNKNOWN localizado); W por cuenta cuando `payments[]` no atribuye créditos (residual visible); PRO_CHAT_POOL_DELTA; receipts físicos completos del verificador CLOUD de integración (no recuperados en este shot; mismos términos declarados por C04).

## REUSABLE_ASSETS

- `economics_report.py` + `test_economics_report.py`: PERMANENT_REGRESSION (protegen el contrato opt-in y la paridad de vocabulario de estados).
- E2E real R03: E2E_CANDIDATE reproducible con el comando documentado.
- Censo S04-F01: evidencia de aceptación S04 (harness one-off, receipt en change_log).

## FEEDBACK

- El censo F01 tomó la forma de globs distintos por root (`plans/*/plan.json` vs `lab/*/plan.json` vs `out/*/*/batch-outcome.json`): un manifiesto de run-roots vigentes en el vault ahorraría la re-derivación en cada auditoría focal (candidato a runbook, no creado por rutina).
- `pip3`/coverage no disponibles en Hefesto; el método stdlib `sys.settrace` debería anotarse como recepción estándar de coverage Python del host.

## CLOSE_SCOPE

Cerrado EXCLUSIVAMENTE este worker I0-S1 (ZCode/GLM-5.3-Flash LOCAL). El manager de Optimización de Campañas y el programa Echo Futures permanecen ABIERTOS; planner del manager NO escrito por este worker. Agents-OS: master directo con HEAD reconciliado (ff a `21a2735`, que incluye el corte `5fe3995`), create-only de tres archivos propios, push con readback remoto; sin rama/PR/force.

## AGENTS_OS_PATHS_SHA

- `10-projects/Echo Futures/artifacts/backtester/EF-CAMPAIGN-MODES-I0-IMPLEMENTATION-RETURN.md` (este archivo, create)
- `80-agents/journal/agent-runs/2026-10-28-zcode-glm-5.3-flash-echo-campaign-modes-i0-s1.md` (create)
- `80-agents/journal/logs/2026-10-28-echo-campaign-modes-i0-s1.md` (create)
- SHA del commit Agents-OS: ver change_log (readback tras push).

## NEXT

**I0-S2** — TOP LOCAL fresco (GPT-6 Sol), ≤90 min, sobre CANDIDATE_SHA `b964e13d` exacto (rama `feature/ef-campaign-modes-i0`), con retorno `EF-CAMPAIGN-MODES-I0-VERIFY-RETURN.md`; sin autoaceptación. La disposición F01 y el alcance del fixture Go quedan para adjudicación del manager junto con el retorno S2.

---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[EF-CAMPAIGN-MODES-DESIGN]]"
  - "[[Echo Futures — Optimización de Campañas]]"
  - "[[EF-CAMPAIGN-MODES-I0-LOCAL]]"
aliases:
  - EF-CAMPAIGN-MODES-GO-S02-RETURN
tags:
  - kind/doc
created: "2026-10-29"
updated: "2026-10-29"
---

# EF-CAMPAIGN-MODES-GO-S02-RETURN

**STATUS: IMPLEMENTATION_CANDIDATE** (con residuals declarados; NO es aceptación Owner ni certification; GO-S03 es el siguiente paso y NO fue ejecutado por este shot).

## Identidad de la entrega

| Campo | Valor |
|---|---|
| BASE_SHA | `2baf319ddcba622d9557bc9f23a13787b44c58a7` (origin/master reconciliado al iniciar; sin avance material del master durante el shot) |
| BRANCH | `feature/ef-campaigns-go` (publicada en origin con readback: `git ls-remote` == local `062b6df77845d2042e398bb6174700e80bb58b60`) |
| CANDIDATE_SHA | `062b6df77845d2042e398bb6174700e80bb58b60` |
| BUILD_ID | binario `echo-backtest` go1.27.1 linux/amd64 `-trimpath -buildvcs=true`, SHA256 `e416636670b055c246af535e0c379ff7718ee91841a5e4ff2e7e4a8bdacaebbb` (receipt `~/echo-work/c06-s02/echo-backtest-c06-s02`) |
| DIFF_SCOPE | 103 archivos, +14.972/−14.639, 7 commits (`a9b24896` SDD, `e0e4acbc` W1, `b9be5dbe` W2, `141fceb8` W3, `653b58ce` W4, `ef44fc4f` lifts, `062b6df7` W5+fixes); SDD del change en `specs/FEAT-EF-CAMPAIGNS-GO/` (SPEC/PLAN/TASKS/VERIFICATION); registrado en `specs/SPECS.md` como FEAT-EF-CAMPAIGNS-GO |
| AGENTS_OS_PATHS_SHA | vault `main/` NO es git en este host (publicación create-only + sync del repo de publicación); retorno en `10-projects/Echo Futures/artifacts/backtester/EF-CAMPAIGN-MODES-GO-S02-RETURN.md`; run-register `80-agents/journal/agent-runs/2026-10-29-zcode-glm-5.3-flash-echo-c06-go-s02.md`; corte documental consumido `b67fa72e` (master documental observado `baa8668` sin delta Echo Futures pertinente — verificado por diff de paths) |
| PRO_CHAT_POOL_DELTA | UNKNOWN (sin observabilidad del pool desde esta superficie) |

## REUSE_MAP (sobre el corte 2baf319d)

Reutilizado sin duplicar: `RunPlatformCampaign` + `PlatformCampaignRequest.Validate` como único owner de admisión (`platform_campaign.go`); compartimentos/rotación física `PreserveAccounts/SelectPreservedAccount/AddPreservedAccount` + `parkedAccountControl/Timer` (`platform_registry.go`); composición de authorities `composeAccount/composePoolSealedAuthorities/NewSealedMoneyManagerCatalog/WireSealedMoneyManagers/SealedAccountPolicy` (`compose_account.go`, SDK config); motor causal/reloj/scheduler/EnqueueControl/ExpectedContextDigest (run/driver); fanout `Linearize/ApplyTargetSet`; batch/receipts/identidad `RunPlatformBatch/readBatchComplete/CanonicalJSONDigest` (`platform_search.go`, `experiment.go`); dinero `units.Money/Price`; `ComposePlatformSpec` (gemelo v2 nuevo `ComposePlatformSpecV2`); CLI existente (11 subcomandos intactos; `lab` añadido, no reemplaza); guard fuente = linaje Clutifx `qualification_guard.py`/`qualification_ledger.py` (contrato porteado a Go, sin merge Clutifx). Extensión del driver para composición: quirúrgica (compartimentos simultáneos por AccountID con orden de visita determinista; sin segundo engine/scheduler/cursor — paridad monocuenta byte-idéntica probada).

## PYTHON_DISPOSITION

Retirados del árbol activo 55 .py + 9 .pyc (PRODUCTO 10, TEST 15, HISTORICO 19, EXPERIMENTAL 1 `compare_events.py`; registro por archivo con consumidores y reemplazo en `v3/backtester/tools/tradesgerard/GO_ONLY_PYTHON_RETIREMENT.md`). Disposiciones: REUSE_GO `campaign_lab.py` (identidad S01 ya en JSON); IMPLEMENT_GO `research_lab.py`+`s02_trials.py` (lab CLI Go); RETIRE_REFERENCE_ONLY el resto (26 nativas corren por `RunPlatformBatch`; reportes por `campaign_economic_report.go`; guard por `qualification_admission.go`). AJENO intacto por bytes: `v3/hasura/scripts/build_lab_v4_metadata.py` (10.445 B), `v3/sdk/postgres/scripts/compile_rollout_sql.py` (7.981 B). JSON/catálogos/runbooks/evidencia histórica intactos. Makefile/CI sin referencia Python (verificado). Cero `.py`/`__pycache__` bajo `v3/backtester` al cierre.

## GO_ONLY

Probado físicamente: PATH sandbox sin `python3` (`~/echo-work/c06-s02/w5/nopython-bin/`) ejecuta build, tests, `lab migrate` (89/89), guard y reporte. Grep del flujo oficial: cero invocaciones Python (hits = comentarios de linaje Go, enumerados en el registro de retiro). Sin venv/pip/wrapper/exec.

## R01_R12_MATRIX

| Req | Estado | Evidencia |
|---|---|---|
| R01 una Campaign, factories compartidas | DELIVERED | `TestCampaignV2Matrix_A01_SameFactoriesServeEveryModality`; MM/Strategy por factories sin editar Campaign/scheduler; plugin platformproof de test |
| R02 CHALLENGE N cuentas + relevo | DELIVERED | E2E N=3 pase/pérdida/pausa con una activa, sin rewarmup/replay (`campaign_modes_v2_test.go`) |
| R03 FUNDED N seeds | DELIVERED | E2E N=3: pagadora ×2 luego pierde, no pagadora, pendiente; denominador completo |
| R04 etapas aisladas comparables | DELIVERED | CHALLENGE vs FUNDED = dos jobs con scopes/cajas separados (batch receipts por identidad) |
| R05 SIMULATION 1×1 | DELIVERED | E2E 4000→4140 conciliada; compra tras crédito; nominal/pending no financian (`TestCampaignV2E2E_ApprovedPayoutNeverFinancesOrMovesCash`) |
| R06 multi-asociación/multi-perfil | DELIVERED (con límites) | composición 2 asociaciones/2 RuleSets simultáneas, mercado/reloj/caja únicos, desempate determinista; límites: MM heterogéneo por asociación y FUNDED multi-asociación siguen fail-closed (superficie de request no implementada) |
| R07 evidencia/KPI/legacy Go | DELIVERED | 19 kinds versionados, emisor idempotente, Q(H) con linaje causal y orden verificado (fix F2), adaptador legacy sin inferencia |
| R08 flujo sin Python | DELIVERED | lab validate/plan/prepare/run/resume/report/compare/migrate/qualify/export; Go-only físico (A13) |
| R09 migración | DELIVERED | matriz 104 filas: 26 MIGRATED (SAME_SEMANTICS legacy-path), 63 SG + 15 aliases CATALOG_VALIDATED (NEW_EXPERIMENT `budget_semantics`), censo delta CERO; sin receipts/catálogos mutados |
| R10 causalidad/replay/idempotencia | DELIVERED | resume KISS (COMPLETE digest-verified reutiliza; incompleto ⇒ rerun aislado mismo RunID/nuevo Attempt); mismo ID+payload replay, distinto payload conflicto; failure mid-run ⇒ INCOMPLETE nunca COMPLETE (`TestCampaignV2Matrix_A14_BatchFailureThenRerunIsolatedAttempt`) |
| R11 G0–G5 + V1 + guard | DELIVERED (parcial D05) | guard Go G4/G5 en 5 puertas + lab run/resume siempre; S04-F01 fixture frontera (decline V1 vs Unclipped finalizer, igualdad, piso; sin renombres); D05 funded-only histórico permanece decisión Owner/retester — ninguna corrida histórica fue desbloqueada por este shot |
| R12 pruebas físicas + capacidad | DELIVERED (con residual) | suites + E2E reales + capacidad medida; residual: coverage parcial y sin `-race` (host) |

## EXECUTION_MATRIX / GATES_PER_IDENTITY

- Ejecutado físicamente: E2E deterministas TEST_ONLY (CHALLENGE N=3, FUNDED N=3, SIMULATION 1×1, composición 2×2, long/short bajo LOW_FIRST y HIGH_FIRST) sobre corpus sintético rotulado; censo 89 materializado/validado + 5 filas SEALED con plan digest real (MR-08, ORB-NATIVE-C02..C05) leídas de run roots existentes.
- **NO se ejecutó ninguna campaña económica histórica real** (26/63/89): D01/D02, budget, ventana y D05 requieren inputs Owner; catálogo validado ≠ campañas corridas. FUNCTIONALLY_TESTED cubre la mecánica; ECONOMIC_RESULT: 0.
- BLOCKED por diseño fail-closed (no defecto): TGMM/RG sealed-policy binding en controlador v2 (declina nombrado); FUNDED multi-asociación simultánea; CloseSafety v2; composición con OHLC sin camino predeclarado.

## TEST_COMMANDS_RECEIPTS

Receipts crudos en `~/echo-work/c06-s02/`: `baseline-fails.txt`/`baseline-cmd-fails.txt` (oráculo `2baf319d`), `final-root-suite.log`, `final-cmd-suite2.log`, `w5/capacity.md` (+`receipts/capacity-*.log`), `w5/migration-nopython.json`, `w0-inventory.md`. Comandos clave: `go test github.com/xKoRx/echo/v3/backtester -run 'CampaignV2|CampaignComposition|CampaignEconomic|CampaignReport|CampaignLegacy|CampaignCash|TestCampaignV2GapFill' -count=1` → ok; suites completas con conjunto de fallos IDÉNTICO al baseline (18 raíz + 5 cmd, todos ambientales pre-existentes: reserva 8GiB vs tmpfs, fault-injection Reconciled, TG parity); binario SHA256 arriba reproducible con `go build -trimpath -buildvcs=true`.

## COVERAGE

Media por función de los archivos nuevos (perfil `w5/cover.out`): contract 89,5 / events 91,0 / report 95,8 / adapter 90,6 / modes 84,8 / accounts 88,1 / composition 82,3 / admission 91,8 / migrate 82,5%. **Bajo el piso 95% en varios archivos: residual DECLARADO, no maquillado** — los huecos son ramas fail-closed profundas y superficies de presentación; invariantes (economía exacta, identidad, causalidad, fail-closed, idempotencia) están cubiertos primero; sin tests tautológicos ni ramas inventadas. GO-S03/S04 pueden cerrar el delta.

## PERFORMANCE_MEASURED

Trayectoria 1×1 con N rotaciones por pase (proceso aislado): N=100 → 101 adquisiciones, 13,97 s wall, 23,45 s CPU, 629 MB RSS pico, artifact 15,1 MB lineal en evidencia; N=10 → 1,3 s/67 MB; N=1 → 0,24 s/30 MB. Slope RSS ≈ 4–6 MB por unidad adquirida (compartimentos preserved + evidencia declarada; no buffer oculto). Cancel mid-run: goroutines 2→2, sin huérfanos. Es capacidad DEL HOST medido; sin promesa de escala infinita ni de 100 engines físicos.

## FINDINGS resueltos en-shot (integridad)

1. **F2 (W5): Q(H) calificaba créditos con pase/activación posteriores al crédito** — `campaignQualityLineageComplete` ahora exige orden causal completo (compra→intento→pase→activación ANTES del crédito); el repro de W5 quedó como regresión.
2. Canary del gate: digest declarado malformado ahora se valida ANTES de resolver receipts-dir (`RECEIPT_DIGEST_INVALID`); test aislado de cwd; `out/` contaminación (commiteada por error por W4) retirada del árbol.
3. Hallazgos W0 confirmados: guard fuente hallado en linaje Clutifx; README storage corregido (tiers 8GiB/2GiB reales); payout bifurcado {2300,3000} TGMM vs perfil respetado por binding.

## NOT_EXECUTED

Campañas económicas históricas reales (todas); D01/D02/D05 (decisión Owner); validación de reglas comerciales reales de props (perfiles TEST_ONLY únicamente); `-race`; MD de runbooks históricos sin reescritura; merge a master/release/deploy/LIVE (prohibidos por mandato).

## UNKNOWN

Consumo Pro/pool; comportamiento QUOTE/MixedMinute en composición sin E2E (implementado); `prepareFixtureScope` multi-compartimento; ventana canaria/last-contract del guard (régimen lab estricto sin WINDOW_REGISTRY — decisión documentada W4); rows de migración con roots no presentes en este host (ABSENT con causa, no inventadas).

## REUSABLE_ASSETS

Guard Go + ledger (`qualification_admission.go`); lab CLI; matriz de migración reproducible (`lab migrate`); emisor/proyección de eventos económicos; fixtures deterministas platformproof NY; harness de capacidad; corpus de falsificadores iniciales (matriz W5) para GO-S03; receipts y baselines de regresión en `~/echo-work/c06-s02/`.

## SUBAGENT_RECEIPTS

Modelo efectivo único: **GLM-5.3-Flash** (sesión y workers clf-flash; sin sustituciones). W0 inventario (1 despacho OK); W1 (OK, 37 tests); W2 (OK, 21 tests); W3 (OK, 7 tests + paridad byte-idéntica); W4 primer intento MUERTO por red a mitad (trabajo heredado auditado y completado por W4-bis: 4 defectos corregidos incl. pánico fail-open); W5 corrió ~80 min y MURIÓ por **quota del host** (capacidad): dejó capacity/e2e/matrix/coverage; W5-bis NO despachable (quota) ⇒ cierre por el integrador. **Consecuencia declarada: la matriz funcional de W5 no tiene independencia de autor** (mismo modelo que los owners); GO-S03 es el contrapeso previsto por el planner. Worktree final limpio; sin reset/force; rama I0 Python intacta como referencia.

## PRÓXIMO PASO (fuera de este shot)

GO-S03 GOD LOCAL sobre CANDIDATE_SHA `062b6df77845d2042e398bb6174700e80bb58b60` exacto, con corpus/harness propios y Read-only sobre el producto. Este worker cierra exclusivamente GO-S02; manager y programa permanecen abiertos.

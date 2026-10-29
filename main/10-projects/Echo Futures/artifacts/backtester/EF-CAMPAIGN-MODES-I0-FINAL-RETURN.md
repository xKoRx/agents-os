---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[EF-CAMPAIGN-MODES-I0-LOCAL]]"
  - "[[EF-CAMPAIGN-MODES-I0-VERIFY-RETURN]]"
  - "[[EF-CAMPAIGN-MODES-I0-IMPLEMENTATION-RETURN]]"
  - "[[EF-CAMPAIGN-MODES-DESIGN]]"
  - "[[Echo Futures — Optimización de Campañas]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-29"
updated: "2026-10-29"
---


# EF-CAMPAIGN-MODES-I0-FINAL-RETURN

Retorno ONE-SHOT de I0-S3 (corrección final del reporter económico). Worker GLM LOCAL fresco (ZCode/GLM-5.3-Flash, host Hefesto); no manager, no verificador I0-S2. Alcance exclusivo: reporter opt-in y sus pruebas del mismo owner. Sin CHALLENGE/FUNDED/SIMULATION, sin runtime Go, sin campañas, sin deploy, sin merge a master de producto. PRO_CHAT_POOL_DELTA: UNKNOWN.

## STATUS

**READY_FOR_OWNER_REVIEW** — F1–F11 todos CORRECTED_AND_VERIFIED (4 P1 + 6 P2 + 1 P3, cero pendientes), E7/E8b refutados preservados sin cambio de mecanismo, gate completo re-ejecutado con recibos reales sobre el FINAL_SHA. El gate Owner y el challenge adversarial del manager sobre el delta permanecen abiertos; este shot no auto-acepta nada.

## BASE_SHA / CANDIDATE_SHA / FINAL_SHA

- BASE_SHA: `2baf319ddcba622d9557bc9f23a13787b44c58a7` (ancestro verificado del candidato).
- CANDIDATE_SHA: `b964e13df59e20b06349eb7e0ad4f4ed057d04a0` — HEAD de `feature/ef-campaign-modes-i0` en worktree `~/go/src/github.com/xKoRx/echo-i0` al inicio; `origin == HEAD == b964e13d` verificado por fetch antes de escribir; único estado sin trackear: `__pycache__` (bytecode derivado, preservado como WIP de reconocimiento, sin commitear).
- FINAL_SHA: **`a98914c79b35900fdba51b1fd1403cf4d63bfd9f`** (corrección del reporter: sólo `economics_report.py` + `test_economics_report.py`; push con readback). SHA final de la rama incluyendo el append SDD del VERIFICATION del change: **`4ff327247f3c369ce3aded5bc577bcebc64ecc61`** (push con readback, `origin == HEAD`).

## FINDINGS_DISPOSITION

| Hallazgo | Disposición | Corrección / evidencia focal |
|---|---|---|
| F1 refunds fuera de identidad (P1) | CORRECTED_AND_VERIFIED | REFUND entra en `cash_final_projected`/`cash_identity_residual` exactamente una vez. Apertura 200 + compra 100 + refund 100 + final 200 ⇒ residual `0 USD`, proyectado `200 USD`, coste neto `0 USD` (E1) |
| F2 Q sin linaje (P1) | CORRECTED_AND_VERIFIED | q_root exige compra pagada → pase → activación aplicada → payout acreditado dentro de un scope. Sin costuras ⇒ `PAYOUT_WITHOUT_PROVEN_LINEAGE` visible, `Q=0, q_roots=[], INCOMPLETE_LINEAGE`, nunca OBSERVED (E2r/E2; desaparece la contradicción q_roots+NOT_OBSERVED) |
| F3 funded inflada (P1) | CORRECTED_AND_VERIFIED | `review_at`/`credentials_at` (pre-activación Go) excluidos de evidencia funded; frontera declarada = `compliant_at` + LIVESIM + gross_paid>0 + payouts>0 + estados instalados. E3 ⇒ `N_funded_initiated=0`. Nota de evidencia publicada en el reporte |
| F4 cutoff vs terminal (P1) | CORRECTED_AND_VERIFIED | Residual firmado sólo con frontiers equivalentes; con efectos post/UNKNOWN ⇒ `UNKNOWN (CUTOFF_FRONTIER_MISMATCH…)` + `cutoff_bounded_residual` contra el último `cash_after ≤ cutoff` (E4: bounded `0 USD`) |
| F5 timestamps string (P2) | CORRECTED_AND_VERIFIED | RFC3339 parseado y comparado en UTC (offsets normalizados, strings originales preservados como evidencia); cutoff declarado ilegible ⇒ `LAB_ECONOMICS_UNREADABLE_CUTOFF`; instantes sin offset nunca se ordenan posicionalmente (E5a BEFORE/E5b AFTER correctos; test naive permanente) |
| F6 post-cutoff desaparece (P2) | CORRECTED_AND_VERIFIED | Todos los efectos permanecen listados con `cutoff_relation` (`AFTER_CUTOFF` excluido de métricas solamente); `effect_summary` desglosa por relación (E5: 4 listados, gross 100) |
| F7 timestamp ausente (P2) | CORRECTED_AND_VERIFIED | `UNKNOWN_CUTOFF_RELATION` explícito, excluido de la ventana y de pass_events acotados; `window_totals_complete=False` y contadores en completeness; jamás incluido silenciosamente como anterior al corte (E5c) |
| F8 fees funded (P2) | CORRECTED_AND_VERIFIED | Frontera = `compliant_at` (fecha programada declarada — nota explícita de que no prueba instante de activación); fee ≥ frontera ⇒ `F_op_funded_external`; fee < frontera ⇒ nuevo `F_activation_setup_external`; sin cuenta/frontera/instante ⇒ UNKNOWN visible (E6: F_op `0 USD`, activación `500 USD`) |
| F9 attempts vs revisiones (P2) | CORRECTED_AND_VERIFIED | Supersesión probada SOLO por run_id igual no nulo (`PROVEN_SAME_REVISION`); distinto/ausente ⇒ `UNKNOWN_EXECUTION_RELATION` con `is_current_revision: null`, ambos attempts listados con su spend, totales conjuntos `UNKNOWN (NOT_COMPOSABLE…)` + `attempt_visibility` estructurado; `PROVEN_DISTINCT_ECONOMIC_INSTANCE` = vocabulario declarado nunca afirmado sin provenance. Ni suma automática ni autoridad last-input arbitraria (E8: spends `200/100` visibles, total UNKNOWN) |
| F10 crédito sin atribución (P2) | CORRECTED_AND_VERIFIED | Payout observado + compras sin raíz probada ⇒ `INCOMPLETE_LINEAGE` (nunca `Q=0 OBSERVED`); totales monetarios por clase preservados y gaps visibles (E2c: `INCOMPLETE_LINEAGE Q=0`, gap `CREDIT_ATTRIBUTION_UNKNOWN`, `W_credits 400 USD`) |
| F11 reconcile constante (P3) | CORRECTED_AND_VERIFIED | `sums_by_assignment_reconcile` DERIVADO de `research_funding` declarada vs sumas observadas (purchase/renewal/other/total): True sólo completa/sin conflictos/ventana completa; False en conflicto/mismatch; UNKNOWN con razón; checks estructurados en `sums_by_assignment_detail`. Evidencia real R03: True con 4/4 MATCH (6960/1080/0/8040 USD) |
| E7 / E8b (refutados) | PRESERVED | Comportamiento S1 intacto: repeat purchases/UNKNOWN_CARDINALITY y re-lectura idempotente re-verificados sobre fixtures congelados |

Semántica adjudicada aplicada sin interpretaciones nuevas: ninguna corrección requirió decisiones económicas fuera de la adjudicación del manager (no hay dependencia que devolver).

## REGRESSION_EVIDENCE

- `test_economics_report`: **51/51 OK** (34 originales − 2 TCR + 17 falsificadores permanentes nuevos, incl. cutoff ilegible y timestamp naive; método y denominador: unittest sobre el árbol del worktree).
- Suites legacy del lab: **124/124 OK** (`test_campaign_lab + test_research_lab + test_s02_trials + test_s02_trials_reconcile`); referencia previa 124/124 sin deltas.
- TCR declarado (sólo donde el test codificaba el criterio defectuoso): `test_revision_supersedes_without_fabricating_purchase` (el fixture ahora demuestra provenance con run_id igual; el intent —supersesión sin compras fabricadas— se conserva y se endurece) y `test_seed_without_purchase…` (renombrado a fee phase stays unknown; sus assertions F_op=70/unattributed=50 eran el defecto F3/F8). Ninguna assertion debilitada; cada caso adversarial TCR quedó cubierto por un falsificador permanente nuevo.
- `research_lab.py`: byte-idéntico al candidato (el subcomando `economics` no requirió ajuste; diff verificado).

## INDEPENDENT_PROBES

- Re-verificación propia sobre los **fixtures congelados** del harness I0-S2 (`~/echo-work/i0-s2-verify/fixtures/*.json`, checksums preservados, archivos y scripts del verificador NO modificados): **25/25 PASS** (`~/echo-work/i0-s3-verify/reverify_frozen_fixtures.py`) cubriendo F1–F10 + E7 + E8b con expectativas calculadas a mano.
- Los scripts históricos del harness S2 re-ejecutados sin tocar: E1–E4/E2c ahora reportan el defecto **no reproducible** (REFUTED = comportamiento correcto); E2r lleva veredicto de etiqueta fija (registro histórico de S2, no re-evalúa) con salida corregida visible; la sección E5 del script S2 no es re-ejecutable tal cual porque lee el campo `post_cutoff` del formato antiguo, reemplazado por `cutoff_relation` según F6 — el caso está cubierto por el probe propio y por tests permanentes.
- E7/E8b: cobertura explícita de preservación (probe + Oracle2/Oracle9/Oracle11 sin cambios de mecanismo).

## E2E_RECEIPTS

CLI real `research_lab.py economics --attempt ~/echo-work/runs/R03-PROTECTED-CLOSE/lab/LAB-SG-ORB-CH300-30M-R750` (sin cutoff, proceso de producción): **3 corridas exit 0, salidas BYTE-IDÉNTICAS** (`cmp`), sha256 de la salida `fb59eac1edc5fbc3d0d6379c1bd7dd66856abb49f7799d7f776de252b8196bd9` (idéntica también bajo sentinel). Reconciliación independiente del reporte: `cash_identity_residual 0 USD`; proyectado `0 USD == declarado 0 USD`; U=58 KNOWN; P_U=10; `cost_per_pass 804 USD` (`exact_fraction 8040/10`) == `research_funding.cost_per_pass` declarado; `sums_by_assignment_reconcile True` derivado con 4/4 checks MATCH (purchase 6960, renewal 1080, other 0, total 8040 — todas contra las sumas observadas de efectos); conversion `NOT_OBSERVED` (sin payout en scope, razón localizada); agregado `8040 USD`; W_net `0 USD`; N_funded 0; 94 efectos todos `NO_CUTOFF_APPLIED`. Checksums de inputs sellados idénticos pre/post: result.json `37b1bcadbb5e37760b5546fd8eae6e8abae76d88239f90b2bbcd3bc6ed436bef`, plan.json `a03a4d18c8ae9dc014c6e0759a429cf98e3c6e35296fb6dc6c70193bf5913d43`, receipt.json `e36f48c664c744488f5de6b0b65249300c454119ddba9e0fbb36974dd99eaef0`.

## COVERAGE

**100,0% statement del módulo (408/408)**, medido con método explícito: tracer `sys.settrace` corriendo la suite completa del reporter (51 tests), denominador = líneas de statements ejecutables del AST de `economics_report.py` (script persistente `~/echo-work/i0-s3-verify/coverage_settrace.py`). Única línea descubierta en la primera medición (`lost_policy`, rama alcanzable con entrada real del vocabulario legacy) quedó cubierta con un test mínimo; no hay ramas muertas ni cobertura artificial.

## NO_SPAWN

DEMONSTRADO por tres vías: (1) imports del módulo: sólo `datetime`, `hashlib`, `json`, `decimal`, `fractions` (+`pathlib` local); sin subprocess/socket/os.system/Popen; (2) sentinel dinámico del harness S2 **sin modificar** (`sentinel_no_spawn.py`, sha256 `d3cb3b5439fc5d21…`) parcheando Popen/run/check_*/os.system/execv*/fork/posix_spawn/spawnv/socket antes de importar el CLI y ejecutando el subcomando real: **exit 0, salida idéntica** a la corrida plana; (3) sin invocación de run/resume en el camino de `economics` (el subcomando sólo lee y escribe `--out`; diff de `research_lab.py` vacío). Inputs sellados byte-intactos (checksums arriba).

## LEGACY_COMPATIBILITY

DEMONSTRADO: 124/124 suites legacy re-ejecutadas en el FINAL_SHA; `research_lab.py` byte-idéntico al candidato; selector 25%, `_census`, `characterize`, `adjudicate`, `run`/`resume` intocados; sin reinterpretación de 25%/5.000/120/4 payouts ni de V1/Unclipped; el E2E legado sin cutoff conserva los números brutos (U=58, P_U=10, 8040 USD == receipt S2). Sin cambios Go/SDK/driver/catálogos/presets (diff contra base = sólo los 2 archivos permitidos + SDD).

## S04_REMAINING

Sin cambios respecto al retorno I0-S2 (fuera de alcance de este shot): S04-F01 semántica de equivalencia del intérprete V1 pendiente de fixture Go de frontera (otro incremento, fuera de Allowed Files); S04-F02 guard run/resume no portado. Ambos siguen registrados como dependencias de la aceptación S04; este shot no los reabre ni re-ejecuta.

## NOT_EXECUTED / UNKNOWN

- NOT_EXECUTED: campañas nuevas, backtests comerciales, trading, deploy, merge a master de producto, suites Go de producto/`-race` (sin gcc), fixture Go de frontera S04-F01, GOD-COMPOSITION, I1/I2a/I3/I4.
- UNKNOWN: PRO_CHAT_POOL_DELTA (no observable desde este shot). Relación física entre attempts con mismo campaign_id y run_ids distintos: el reporter ahora la declara `UNKNOWN_EXECUTION_RELATION` con evidencia visible — la decisión económica de si dos ejecuciones son instancias distintas sigue siendo del manager/Owner, no del reporter. Equivalencia de intérprete V1 (heredada de S04, fuera de alcance). W por cuenta cuando `payments[]` no atribuye créditos (residual visible declarado; no hay evidencia real que lo contenga en R03).

## REUSABLE_ASSETS

- `~/echo-work/i0-s2-verify/` (harness del verificador, INTACTO con checksums registrados — evidencia, no desechable) y `~/echo-work/i0-s3-verify/` (propios): `reverify_frozen_fixtures.py` (25 checks contra fixtures congelados) y `coverage_settrace.py` (cobertura con denominador AST, re-ejecutable sin dependencias).
- 17 falsificadores permanentes dentro del owner (`I0S3FalsifierRegressions`): protegen residual/refunds, linaje Q completo, frontera funded, cutoff/frontier, offsets UTC, efectos listados/UNKNOWN, attempts/revisión por provenance, crédito sin atribución y reconcile derivado.
- Comando E2E R03 triple-corrida + `cmp` + checksums = recibo de determinismo re-ejecutable.
- Clasificación del reporter para futuros shots: los campos nuevos (`cutoff_relation`, `cutoff_bounded_residual`, `F_activation_setup_external`, `attempt_visibility`, `sums_by_assignment_detail`) son superficie de lectura del manager; ningún consumidor downstream existe todavía.

## AGENTS_OS_PATHS_SHA

- `10-projects/Echo Futures/artifacts/backtester/EF-CAMPAIGN-MODES-I0-FINAL-RETURN.md` (este archivo, create)
- `80-agents/journal/agent-runs/2026-10-29-zcode-glm-5.3-flash-echo-campaign-modes-i0-s3.md` (create)
- `80-agents/journal/logs/2026-10-29-echo-campaign-modes-i0-s3.md` (create, change_log)
- Repo echo: `specs/FEAT-CHALLENGE-HISTORY/changes/CHANGE-001-campaign-modes-i0-economics.VERIFICATION.md` (append sección I0-S3, commit `4ff32724…` push con readback)
- Commit Agents-OS: NOT_EXECUTED — el vault `main/` no expone `.git` accesible en esta superficie (verificado: `main/.git` ausente, `git rev-parse` fatal hasta la raíz); persistencia create-only y delta declarado aquí, sin inventar SHA remoto, sin crear ramas ni PR en Agents-OS. Mecanismo de sincronización vigente: el mismo documentado por I0-S1/S2 (sincronización del vault gestionada fuera de este host; el manager valida en su superficie).

## PRO_CHAT_POOL_DELTA

UNKNOWN (no observable desde este shot).

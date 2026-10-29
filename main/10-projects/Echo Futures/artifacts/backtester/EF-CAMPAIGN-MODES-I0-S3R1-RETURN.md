---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[EF-CAMPAIGN-MODES-I0-LOCAL]]"
  - "[[EF-CAMPAIGN-MODES-I0-FINAL-RETURN]]"
  - "[[EF-CAMPAIGN-MODES-I0-VERIFY-RETURN]]"
  - "[[EF-CAMPAIGN-MODES-DESIGN]]"
  - "[[Echo Futures — Optimización de Campañas]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-29"
updated: "2026-10-29"
---


# EF-CAMPAIGN-MODES-I0-S3R1-RETURN

Retorno ONE-SHOT de I0-S3R1 (reparación focal de los cuatro hallazgos residuales G1–G4 del manager sobre I0-S3, precisión C05-R1). Worker GLM LOCAL fresco (ZCode/GLM-5.3-Flash, host Hefesto); no manager, no verificador, un writer. Alcance exclusivo G1–G4: NO se reabre F1–F11 ni se rediseña el reporter. Sin campañas, compras, trading, deploy ni merge a master de producto. PRO_CHAT_POOL_DELTA: UNKNOWN.

## STATUS

**READY_FOR_MANAGER_REVIEW** — G1–G4 todos CORRECTED_AND_VERIFIED con falsificadores permanentes que reproducen el defecto contra el HEAD pre-reparación; gate completo re-ejecutado en verde; E7/E8b refutados y F1–F11 sin regresión (re-verificación 25/25 sobre fixtures congelados S2). El gate Owner y el challenge del manager sobre este delta permanecen abiertos; este shot no auto-acepta nada y no despacha I1–I4.

## BASE_SHA / REPAIR_SHA

- BASE: `4ff327247f3c369ce3aded5bc577bcebc64ecc61` — HEAD de `feature/ef-campaign-modes-i0` en `~/go/src/github.com/xKoRx/echo-i0` al inicio; `origin == HEAD == 4ff32724` verificado por fetch antes de escribir; único estado sin trackear: `__pycache__` (bytecode derivado, preservado sin commitear). Implementación S3 `a98914c7` intacta como ancestro.
- REPAIR_SHA: **`bab3bef170f52d93ab649eb4de973a2bf1e2a5df`** — push con readback (`origin/feature/ef-campaign-modes-i0 == HEAD == bab3bef1`, verificado por fetch posterior). Diff: sólo `economics_report.py` (+252/−58 netos de sección), `test_economics_report.py` (+249) y append de la sección I0-S3R1 en el VERIFICATION SDD; `research_lab.py` byte-idéntico; nada Go/SDK/runtime/guard/launcher/presets.

## G1–G4 DISPOSITION (todas CORRECTED_AND_VERIFIED)

| Hallazgo | Corrección | Evidencia focal |
|---|---|---|
| G1 (P1) RunID ≠ attempt/revision | Supersesión probada SOLO por provenance explícita declarada (`execution.attempt_id` igual no nulo + `revision_index` cadena completa 0..n-1). RunID derivado (`compose.go::DeriveRunID`) no prueba nada: mismo campaign_id + mismo run_id + dos SHA distintos ⇒ `UNKNOWN_EXECUTION_RELATION`, `is_current_revision: null`, ambos gastos per-attempt visibles, totales conjuntos NOT_COMPOSABLE, sin autoridad last-input ni suma automática como dos compras. RunIds distintos/ausentes ⇒ igual UNKNOWN. Misma SHA releída ⇒ E8b intacto | Falsificador `test_g1_equal_run_id_with_distinct_bytes…` (alpha/beta run-SAME ⇒ UNKNOWN, spends 100/200 visibles) + control positivo `test_g1_declared_attempt_provenance…` (`att-R` + cadena ⇒ PROVEN_SAME_REVISION, agregado consume sólo revisión declarada actual) |
| G2 (P1) funding encolado ≠ instalada | `_account_funded_evidence` sin `compliant_at` programado ni `FUNDING_INSTALL_PENDING` (encolado Go `platform_campaign.go:783`; acreditado instalado sólo tras aplicar el control en contexto `:901–904`). Evidencia instalada: `terms.stage_id` LIVESIM del contexto final (`c.state.currentTerms`, `:1127`), `gross_paid>0`, `payouts>0`, estados operativos funded instalados (`TRANSITION_PENDING`/`PAYOUT_PENDING`). Nuevos `funded_initiated_status` (KNOWN/UNKNOWN con razón) y `funded_evidence_unknown_account_ids`. `STOW_FEE`/`PLATFORM_FEE` siguen clasificados setup/activación, no F_op (F8 intacto). La activación del linaje q usa la misma evidencia endurecida | Falsificador `test_g2_enqueued_funding…` (FUNDING_INSTALL_PENDING + compliant_at futuro + stage EVALUATION ⇒ N=0, status UNKNOWN, cuenta listada, conversión INCOMPLETE_LINEAGE por `PAYOUT_WITHOUT_PROVEN_LINEAGE`) + control positivo `test_g2_installed_livesim_context…` (LIVESIM instalado ⇒ N=1 KNOWN). R03 real: N_funded 0 con status KNOWN |
| G3 (P1) Q completo con gaps | `_q_status`: OBSERVED sólo con raíces y CERO `lineage_gaps`; con gaps, `Q`/`Q_proven` conservan raíces probadas y `q` queda None (nunca fracción completa 1/2 sobre cohorte incompleta). Orden causal verificado sólo contra instantes parseables existentes (crédito antes de pase/compra ⇒ `CAUSAL_ORDER_CONTRADICTED`; nunca orden por posición JSON). Pago CREDITED sin ningún efecto de payout en el scope ⇒ `PAYMENT_CREDITED_WITHOUT_CASH_EFFECT`; totales cash siguen visibles | Falsificadores: cohorte A probada + B payout sin pase ⇒ `Q_proven=1`, status `INCOMPLETE_LINEAGE`, q=None; `credit_at < pass_at` ⇒ gap causal; CREDITED sin cash effect ⇒ gap homónimo; `W_credits` preservado en los tres |
| G4 (P2) reconciliación parcial | `_sums_by_assignment`: True exige declaración comparable COMPLETA (purchase/renewal/other/total_spend, 4/4) coincidente, sin conflictos, ventana completa; parcial coincidente ⇒ `UNKNOWN` con `PARTIAL_DECLARATION (k/4)` en `sums_by_assignment_detail.reason` (checks visibles); mismatch ⇒ False (precede a parcial) | Falsificador `test_g4_partial_declaration…` (2/4 coincidentes ⇒ UNKNOWN PARTIAL) + control positivo `test_g4_complete_four_field_match…` (4/4 ⇒ True). R03 real permanece True con 4/4 MATCH |

Controles preservados: E7/E8b refutados sin cambio de mecanismo; F1–F11 **25/25** re-verificados sobre los fixtures CONGELADOS del harness I0-S2 (`~/echo-work/i0-s2-verify/` intacto con checksums). La sección E5 del script histórico S2 sigue no re-ejecutable tal cual (lee el campo antiguo `post_cutoff`); el caso permanece cubierto por tests permanentes y probe propio (limitación ya registrada por S3, sin cambio).

## REPRODUCTION_AGAINST_PRE_REPAIR_HEAD

Los falsificadores se crearon ANTES de parchear producto y se ejecutaron contra `4ff32724`: **7 FAIL + 2 ERROR** (los ERROR son los campos nuevos aún inexistentes: `funded_initiated_status`, `Q_proven`), con los 51 tests preexistentes en verde — los defectos G1–G4 estaban vivos y verdes bajo la suite S3. Tras el parche: 62/62 OK. Workspace propio: `~/echo-work/i0-s3r1-verify/` (recibos E2E, checksums pre/post).

## REGRESSION_EVIDENCE y TCR

- `test_economics_report`: **62/62 OK** (51 de S3 + 9 falsificadores/controles G1–G4 + 2 TCR endurecidos + 2 tests de ramas alcanzables; unittest sobre el árbol del worktree).
- Suites legacy del lab: **124/124 OK** (`test_campaign_lab + test_research_lab + test_s02_trials + test_s02_trials_reconcile`).
- TCR declarado (mismo criterio de S3, sólo donde el test codificaba el criterio corregido): `test_revision_supersedes_without_fabricating_purchase` (provenance run_id —ya no demostrativa tras G1— sustituida por provenance explícita attempt_id+cadena; intent conservado y endurecido) y `test_f11_reconcile_true_only_from_real_comparison` (fixture declara ahora los cuatro campos comparables; intent conservado y endurecido). Ninguna assertion debilitada; cada caso adversarial TCR queda cubierto por falsificadores permanentes nuevos.

## E2E_RECEIPTS

CLI real `research_lab.py economics --attempt ~/echo-work/runs/R03-PROTECTED-CLOSE/lab/LAB-SG-ORB-CH300-30M-R750` (sin cutoff, proceso de producción): **2 corridas exit 0, salidas BYTE-IDÉNTICAS** (`cmp`), sha256 de la salida `0c949f1315e44e6678ed38ef43c888f6a3e4773ffa4f78c548f41ba4badba982`. Reconciliación: `cash_identity_residual 0 USD`; proyectado `0 USD == declarado 0 USD`; U=58 KNOWN; P_U=10; `cost_per_pass 804 USD` (`exact_fraction 8040/10`) == `research_funding.cost_per_pass` declarado; `sums_by_assignment_reconcile True` con **4/4 checks MATCH** (purchase 6960, renewal 1080, other 0, total 8040); conversion `NOT_OBSERVED`; agregado `8040 USD`; `N_funded 0` con `funded_initiated_status KNOWN` (sin cuentas con señales programadas/encoladas); `Q_proven` presente (0); revisión `SINGLE_ATTEMPT`. Corrida bajo sentinel **BYTE-IDÉNTICA** a la plana. Checksums de inputs sellados idénticos pre/post: result.json `37b1bcadbb5e37760b5546fd8eae6e8abae76d88239f90b2bbcd3bc6ed436bef`, plan.json `a03a4d18c8ae9dc014c6e0759a429cf98e3c6e35296fb6dc6c70193bf5913d43`, receipt.json `e36f48c664c744488f5de6b0b65249300c454119ddba9e0fbb36974dd99eaef0`.

## COVERAGE

**100,0% statement del módulo (445/445)**, método `sys.settrace` con denominador AST (`~/echo-work/i0-s3-verify/coverage_settrace.py`, re-ejecutado sin modificar; suite 62/62). Las dos ramas descubiertas en la primera medición post-parche (`parse_money` numérico y `W_attribution` UNATTRIBUTED sin payments) y una tercera preexistente (pass_event sin instante bajo cutoff) quedaron cubiertas con tests mínimos; no hay ramas muertas ni cobertura artificial.

## NO_SPAWN

DEMONSTRADO: (1) imports del módulo sólo stdlib puro (datetime/hashlib/json/decimal/fractions + pathlib local); (2) sentinel dinámico del harness S2 **sin modificar** (`sentinel_no_spawn.py`) ejecutando el subcomando real: exit 0, salida byte-idéntica; (3) sin invocación run/resume en el camino de `economics` (`research_lab.py` byte-idéntico, diff vacío). Inputs sellados byte-intactos (checksums arriba).

## LEGACY_COMPATIBILITY

DEMONSTRADO: 124/124 suites legacy en el REPAIR_SHA; `research_lab.py` byte-idéntico; selector 25%, `_census`, `characterize`, `adjudicate`, `run`/`resume` intocados; sin reinterpretación de 25%/5.000/120/4 payouts ni de V1/Unclipped; E2E legado sin cutoff conserva los números brutos (U=58, P_U=10, 8040 USD == receipt S2). Los campos nuevos (`Q_proven`, `q_note`, `funded_initiated_status`, `funded_evidence_unknown_account_ids`, gaps `CAUSAL_ORDER_CONTRADICTED`/`PAYMENT_CREDITED_WITHOUT_CASH_EFFECT`) son superficie de lectura del manager; no hay consumidor downstream (ninguno existe desde S3).

## NOT_EXECUTED / UNKNOWN

- NOT_EXECUTED: campañas nuevas, backtests comerciales, trading, deploy, merge a master de producto, suites Go/`-race` (sin gcc), S04-F01/F02 (fuera de alcance, sin reapertura), GOD-COMPOSITION, I1–I4.
- UNKNOWN: PRO_CHAT_POOL_DELTA (no observable desde este shot). La decisión económica de si dos ejecuciones con igual RunID son instancias distintas sigue siendo del manager/Owner — el reporter ahora declara la relación `UNKNOWN_EXECUTION_RELATION` siempre que falte provenance explícita (incluido el caso run_id igual con bytes distintos). El vocabulario de provenance explícito (`execution.attempt_id`/`revision_index`) no existe hoy en evidencia Go real: con evidencia actual, todo grupo de bytes distintos queda UNKNOWN por diseño (C05-R1: no se exige nueva API para I0).

## REUSABLE_ASSETS

- `~/echo-work/i0-s3r1-verify/` (propio): recibos E2E dobles + sentinel, checksums pre/post de inputs sellados, reconciliación de invariantes R03.
- 9 falsificadores/controles permanentes (`I0S3R1FalsifierRegressions`) dentro del owner: protegen provenance de revisión (G1), frontera funded instalada (G2), linaje Q con gaps/causalidad/cash (G3) y completitud del reconcile (G4).
- Harnesses previos reutilizados sin modificar: `~/echo-work/i0-s2-verify/` (sentinel + fixtures congelados) y `~/echo-work/i0-s3-verify/` (coverage + re-verify 25/25).

## AGENTS_OS_PATHS_SHA

- `10-projects/Echo Futures/artifacts/backtester/EF-CAMPAIGN-MODES-I0-S3R1-RETURN.md` (este archivo, create)
- `80-agents/journal/agent-runs/2026-10-29-zcode-glm-5.3-flash-echo-campaign-modes-i0-s3r1.md` (create)
- `80-agents/journal/logs/2026-10-29-echo-campaign-modes-i0-s3r1.md` (create, change_log)
- Repo echo: `specs/FEAT-CHALLENGE-HISTORY/changes/CHANGE-001-campaign-modes-i0-economics.VERIFICATION.md` (append sección I0-S3R1, commit `bab3bef1…` push con readback)
- Commit Agents-OS: NOT_EXECUTED — el vault `main/` sigue sin `.git` accesible en esta superficie (verificado en S1–S3; mecanismo de sincronización gestionado fuera del host; el manager valida en su superficie). Persistencia create-only y delta declarado aquí, sin inventar SHA remoto.

## PRO_CHAT_POOL_DELTA

UNKNOWN (no observable desde este shot).

## NEXT

Manager challenge del delta `bab3bef1` (diff 4ff32724..bab3bef1: reporter + tests + SDD). No autoaceptación de gate Owner; I1–I4 y GOD-COMPOSITION siguen sin despachar; manager y programa Echo Futures permanecen abiertos.

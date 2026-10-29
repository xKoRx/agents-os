---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[EF-CAMPAIGN-MODES-I0-LOCAL]]"
  - "[[EF-CAMPAIGN-MODES-I0-S3R1-RETURN]]"
  - "[[EF-CAMPAIGN-MODES-DESIGN]]"
  - "[[Echo Futures — Optimización de Campañas]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-29"
updated: "2026-10-29"
---


# EF-CAMPAIGN-MODES-I0-S3R2-RETURN

Retorno ONE-SHOT de I0-S3R2 (microfix final M1–M4 del manager sobre I0-S3R1, precisión C05-R2 del diseño). Worker GLM LOCAL fresco (ZCode/GLM-5.3-Flash, host Hefesto); no manager, no verificador, un writer, sin subagentes. Alcance exclusivo M1–M4: NO se reabren F1–F11 ni G1–G4 como criterios generales ni se rediseña el reporter. Sin campañas, motores, compras, trading, deploy ni merge a master de producto. PRO_CHAT_POOL_DELTA: UNKNOWN.

## STATUS

**READY_FOR_MANAGER_REVIEW** — M1–M4 todos CORRECTED_AND_VERIFIED con falsificadores permanentes que reproducen los defectos contra el HEAD pre-reparación `bab3bef1` (11 checks FAIL con la suite 62/62 en verde); gate completo re-ejecutado en verde; E7/E8b refutados y F1–F11/G1–G4 sin regresión (re-verificación 25/25 sobre fixtures congelados S2). El challenge del manager sobre este delta y el gate Owner permanecen abiertos; este shot no auto-acepta nada y no despacha I1–I4 ni GOD-COMPOSITION.

## BASE_SHA / REPAIR_SHA

- BASE: `bab3bef170f52d93ab649eb4de973a2bf1e2a5df` — HEAD de `feature/ef-campaign-modes-i0` en `~/go/src/github.com/xKoRx/echo-i0` al inicio; `origin == HEAD == bab3bef1` verificado por fetch antes de escribir; único estado sin trackear: `__pycache__` (bytecode derivado, preservado sin commitear). Implementación S3R1 intacta como ancestro.
- REPAIR_SHA: **`8105ef6a657e02a319a9df7fa79d4671d6b10932`** — push con readback (`origin/feature/ef-campaign-modes-i0 == HEAD == 8105ef6a`, verificado por fetch posterior). Diff del commit: sólo `economics_report.py` (+389/−100 netos junto con tests y SDD), `test_economics_report.py` y append de la sección I0-S3R2 en el VERIFICATION SDD; `research_lab.py` byte-idéntico (diff 0); nada Go/SDK/runtime/guard/launcher/presets/receipts.

## M1–M4 DISPOSITION (todas CORRECTED_AND_VERIFIED)

| Hallazgo | Corrección | Evidencia focal |
|---|---|---|
| M1 (P1) mapping `research_funding` sellado | `FUNDING_SUM_KINDS`/`FUNDING_TOTAL_KINDS` con la asignación exacta del productor Go (`platform_research.go::finishResearchFunding`): `other_spend` = STOW_FEE+PLATFORM_FEE; `total_spend` = PURCHASE+RENEWAL+ambos fees. RESET_PAID NO tiene término comparable Go: su presencia en la ventana ⇒ reconciliación `UNKNOWN` con razón explícita (nunca True, nunca renombrado a fees) | Falsificador: PURCHASE100+RENEWAL60+STOW_FEE400+PLATFORM_FEE100 con declaración {100/60/500/660} ⇒ True 4/4 checks con kinds Go visibles (en BASE devolvía False por mapear other→RESET_PAID). Control negativo: mismo fixture + RESET_PAID 30 ⇒ UNKNOWN "RESET_PAID effects have no comparable Go research_funding term" con los 4 checks coincidentes visibles. TCR al test G4 positivo S3R1 (`test_g4_complete_four_field_match_stays_true`) al mapping Go con intent preservado y endurecido. R03 real permanece True 4/4 MATCH |
| M2 (P1) Q exige primer cobro positivo corroborado | `credited_payments` exige `net > 0` (CREDITED con net≤0 nunca es pago recibido, pagador ni evidencia de conversión). Corroboración de cash por cuenta y ventana: un PAYOUT_COLLECTED POSITIVO dentro del cutoff window, atribuido a la misma cuenta, o no atribuido (Go no estampa cuenta en el cash de payout) sólo mientras la atribución W de campaña reconcilia (`credits == credited_payments`). Reversos, cash post-cutoff, cash atribuido a otra cuenta y pooled no reconciliado NUNCA acreditan el primer cobro; atribución sólo desde el array de pagos, sin enlace inventado por importe/fecha | Falsificadores: (a) crédito positivo pre-cutoff + único PAYOUT_COLLECTED post-cutoff ⇒ Q=0 INCOMPLETE_LINEAGE, W_credits 0 en ventana (BASE: Q=1 OBSERVED); (b) CREDITED net 0 + sólo reverso ⇒ Q=0 + gap `CREDIT_ATTRIBUTION_UNKNOWN` visible (BASE: Q=1 OBSERVED sin gaps); net −5 ⇒ nunca acredita; (c) cash atribuido a B no acredita A ⇒ Q=0 (BASE: Q=1); (d) pooled 900 vs pagos 400 no reconciliado ⇒ Q=0 con `RESIDUAL 500` visible (BASE: Q=1 OBSERVED). Preservados: dos payouts positivos de una raíz Q=1 con pooled reconciliado (Oracle5), reverso posterior legítimo conserva el primer crédito (Oracle5), crédito sin ningún cash ⇒ gap homónimo (G3) |
| M3 (P2) setup sin AccountID | `_classify_setup_costs` (sustituye a `_classify_f_op`/`_funded_frontier`): STOW_FEE/PLATFORM_FEE son setup POR KIND Go (`paySetupFees` emite `cashEvent` sin AccountID, siempre pre-activación): todo el monto en ventana ⇒ `F_activation_setup_external` a nivel campaña (ejemplo 400+100=500), `F_op_funded_external` 0 (cero por vocabulario Go — ningún kind legacy produce coste externo post-activación — no por adivinanza) y atribución por cuenta UNKNOWN, sin inferir account_id de orden de archivo, account_id de fixture o `compliant_at` programado | Falsificador: STOW_FEE400+PLATFORM_FEE100 sin account_id (forma Go real) ⇒ F_activation `500 USD`, F_op `0 USD`, account_id None preservado en los efectos (BASE: F_activation 0 con todo en unattributed). Los dos tests que codificaban la clasificación por frontera compliant_at recibieron TCR al criterio por kind (intent "fees nunca F_op" conservado) |
| M4 (P2) revisión con request incompatible | `_attempt_groups`: la provenance declarada (attempt_id igual no nulo + cadena de revisiones completa 0..n-1) exige además el request sellado INMUTABLE (request no vacío e idéntico por canonical JSON en toda la cadena). Request/config/policy distintos ⇒ NO `PROVEN_SAME_REVISION`: `UNKNOWN_EXECUTION_RELATION`, `is_current_revision: null`, ambos spends visibles, agregado NOT_COMPOSABLE. El RunID sigue siendo identidad de inputs (`compose.go::DeriveRunID`), no física | Falsificador: mismo campaign_id + `att-X` + revision_index 0,1 con `spec_version` distinto en el request ⇒ UNKNOWN_EXECUTION_RELATION, spends 120/240 visibles, agregado `UNKNOWN (NOT_COMPOSABLE…)` (BASE: PROVEN_SAME_REVISION con agregado 240 compuesto). El control positivo G1 (request idéntico + cadena declarada) permanece PROVEN_SAME_REVISION |

Controles preservados: E7/E8b refutados sin cambio de mecanismo; F1–F11 y G1–G4 re-verificados **25/25** sobre los fixtures congelados del harness I0-S2 (`~/echo-work/i0-s2-verify/` intacto con checksums, vía `~/echo-work/i0-s3-verify/reverify_frozen_fixtures.py` sin modificar).

## REPRODUCTION_AGAINST_PRE_REPAIR_HEAD

El arnés `~/echo-work/i0-s3r2-verify/falsifiers_m1_m4.py` se creó ANTES de parchear producto y se ejecutó contra `bab3bef1`: **11 checks FAIL** — M1 True→False (mapeo other→RESET_PAID), M2a/b/c/d acreditaban Q=1 (dos de ellos OBSERVED) con cash post-cutoff, net≤0+reverso, cash de B y pooled no reconciliado, M3 registraba el setup en unattributed con F_activation 0, M4 declaraba PROVEN_SAME_REVISION y componía el agregado 240 — con la suite preexistente **62/62 en verde**: los defectos M1–M4 estaban vivos y en verde bajo S3R1. Tras el parche: **14/14 PASS**.

## REGRESSION_EVIDENCE y TCR

- `test_economics_report`: **69/69 OK** (62 de S3R1 + 7 falsificadores permanentes M1–M4 nuevos en `I0S3R2FalsifierRegressions`; unittest sobre el árbol del worktree).
- Suites legacy del lab: **124/124 OK** (`test_campaign_lab + test_research_lab + test_s02_trials + test_s02_trials_reconcile`).
- TCR declarado (mismo criterio: sólo donde el test codificaba el criterio corregido adjudicado, 3): `test_g4_complete_four_field_match_stays_true` (fixture RESET_PAID-como-other_spend sustituido por fees Go-faithful; intent —4/4 completo ⇒ True— conservado y endurecido al mapping Go), `test_seed_without_purchase_is_not_a_root_and_fees_are_setup_by_kind` y `test_fee_without_activation_evidence_is_campaign_setup_by_kind` (la clasificación por frontera compliant_at era el criterio corregido por M3; F_op sigue 0 y el intent "fees nunca F_op / nunca atribuidas por timestamp" se conserva). Ninguna assertion debilitada; cada caso adversarial TCR queda cubierto por los falsificadores permanentes M1/M3 nuevos.

## E2E_RECEIPTS

CLI real `research_lab.py economics --attempt ~/echo-work/runs/R03-PROTECTED-CLOSE/lab/LAB-SG-ORB-CH300-30M-R750` (sin cutoff, proceso de producción): **2 corridas exit 0, salidas BYTE-IDÉNTICAS** (`cmp`), sha256 de la salida `3921d13ea6681859f8f35460121c10d0e2fdc66613da0464484dd009d9d92892` (difiere del de S3R1 porque los checks del reconcile ahora declaran los kinds Go — cambio adjudicado M1; la exigencia del gate es determinismo de la doble corrida, que se cumple). Reconciliación: `cash_identity_residual 0 USD`; proyectado `0 USD == declarado 0 USD`; U=58 KNOWN; P_U=10; `cost_per_pass 804 USD` (`exact_fraction 8040/10`) == `research_funding.cost_per_pass` declarado; `sums_by_assignment_reconcile True` con **4/4 checks MATCH** bajo el mapping Go (purchase 6960 / renewal 1080 / other 0 vía STOW_FEE+PLATFORM_FEE / total 8040); conversion `NOT_OBSERVED`; agregado `8040 USD`; `N_funded 0` con `funded_initiated_status KNOWN`; `Q_proven` presente (0); revisión `SINGLE_ATTEMPT`. Corrida bajo sentinel (`sentinel_no_spawn.py` del harness S2 intacto) **BYTE-IDÉNTICA** a la plana. Checksums de inputs sellados idénticos pre/post (diff vacío en `~/echo-work/i0-s3r2-verify/inputs_{before,after}.sha`): result.json `37b1bcadbb5e37760b5546fd8eae6e8abae76d88239f90b2bbcd3bc6ed436bef`, plan.json `a03a4d18c8ae9dc014c6e0759a429cf98e3c6e35296fb6dc6c70193bf5913d43`, receipt.json `e36f48c664c744488f5de6b0b65249300c454119ddba9e0fbb36974dd99eaef0`.

## COVERAGE

**100,0% statement del módulo (442/442)**, método `sys.settrace` con denominador AST (`~/echo-work/i0-s3-verify/coverage_settrace.py`, re-ejecutado sin modificar; suite 69/69). El denominador bajó de 445 a 442 porque `_classify_f_op`/`_funded_frontier` (5 sentencias con 3 ramas) fueron sustituidos por `_classify_setup_costs` (2 sentencias) conforme a M3; no hay ramas muertas ni cobertura artificial.

## NO_SPAWN

DEMONSTRADO: (1) imports del módulo sólo stdlib puro (datetime/hashlib/json/decimal/fractions); (2) sentinel dinámico del harness S2 **sin modificar** (`sentinel_no_spawn.py`) ejecutando el subcomando real: exit 0, salida byte-idéntica; (3) sin invocación run/resume en el camino de `economics` (`research_lab.py` byte-idéntico, diff vacío). Inputs sellados byte-intactos (checksums arriba).

## LEGACY_COMPATIBILITY

DEMONSTRADO: 124/124 suites legacy en el REPAIR_SHA; `research_lab.py` byte-idéntico; selector 25%, `_census`, `characterize`, `adjudicate`, `run`/`resume` intocados; sin reinterpretación de 25%/5.000/120/4 payouts ni de V1/Unclipped; E2E legado sin cutoff conserva los números brutos (U=58, P_U=10, 8040 USD == receipt). F1–F11 y G1–G4 sin regresión (25/25 frozen + suite 69/69 que incluye sus falsificadores permanentes). Los campos/vocabulario nuevos de este shot son: asignación de `checks` por kinds Go (`other_spend`→STOW_FEE/PLATFORM_FEE), razón `RESET_PAID…no comparable Go term`, corroboration por cuenta del gap `PAYMENT_CREDITED_WITHOUT_CASH_EFFECT`, `F_op_phase_note` por kind y `request_immutable` interno del grupo; no hay consumidor downstream (ninguno existe desde S3).

## NOT_EXECUTED / UNKNOWN

- NOT_EXECUTED: campañas nuevas, backtests comerciales, trading, deploy, merge a master de producto, suites Go/`-race` (sin gcc), S04-F01/F02 (fuera de alcance, sin reapertura), GOD-COMPOSITION, I1–I4.
- UNKNOWN: PRO_CHAT_POOL_DELTA (no observable desde este shot). La semántica de `other_spend`/`total_spend` ante evidencia que contenga kinds fuera del catálogo Go congelado sigue siendo fail-closed (`LAB_ECONOMICS_UNKNOWN_CASH_KIND`); ningún kind nuevo fue agregado al vocabulario. La decisión de si una futura evidencia Go declarará `execution.attempt_id`/`revision_index` (hoy inexistentes en receipts reales) sigue abierta para el manager/Owner — con evidencia actual toda revisión queda UNKNOWN por diseño (C05-R1/R2: no se exige nueva API para I0).

## REUSABLE_ASSETS

- `~/echo-work/i0-s3r2-verify/` (propio): arnés de falsificadores M1–M4 (14 checks), recibos E2E dobles + sentinel, checksums pre/post de inputs sellados.
- 7 falsificadores permanentes (`I0S3R2FalsifierRegressions`) dentro del owner: mapping Go del funding (M1 + control negativo reset), corroboration de primer cobro (M2a–d) y provenance de revisión con request inmutable (M4), más el falsificador M3 de setup sin cuenta.
- Harnesses previos reutilizados sin modificar: `~/echo-work/i0-s2-verify/` (sentinel + fixtures congelados), `~/echo-work/i0-s3-verify/` (coverage + re-verify 25/25), `~/echo-work/i0-s3r1-verify/` (recibos previos, sólo lectura).

## AGENTS_OS_PATHS_SHA

- `10-projects/Echo Futures/artifacts/backtester/EF-CAMPAIGN-MODES-I0-S3R2-RETURN.md` (este archivo, create)
- `80-agents/journal/agent-runs/2026-10-29-zcode-glm-5.3-flash-echo-campaign-modes-i0-s3r2.md` (create)
- `80-agents/journal/logs/2026-10-29-echo-campaign-modes-i0-s3r2.md` (create, change_log)
- Repo echo: `specs/FEAT-CHALLENGE-HISTORY/changes/CHANGE-001-campaign-modes-i0-economics.VERIFICATION.md` (append sección I0-S3R2, commit `8105ef6a…` push con readback)
- Commit Agents-OS: NOT_EXECUTED — el vault `main/` sigue sin `.git` accesible en esta superficie (verificado en S1–S3R1; mecanismo de sincronización gestionado fuera del host; el manager valida en su superficie). Persistencia create-only y delta declarado aquí, sin inventar SHA remoto.

## PRO_CHAT_POOL_DELTA

UNKNOWN (no observable desde este shot).

## NEXT

Manager challenge del delta `8105ef6a` (diff `bab3bef1..8105ef6a`: reporter + tests + SDD). No autoaceptación de gate Owner; I1–I4 y GOD-COMPOSITION siguen sin despachar; manager y programa Echo Futures permanecen abiertos.

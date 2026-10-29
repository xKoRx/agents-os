---
type: change_log
schema_version: 1
scope: project
created: "2026-10-29"
updated: "2026-10-29"
area: "[[Echo]]"
project: "[[Echo Futures — Optimización de Campañas]]"
entities: ["[[Echo Futures]]"]
related: ["[[EF-CAMPAIGN-MODES-I0-S3R2-RETURN]]", "[[EF-CAMPAIGN-MODES-I0-S3R1-RETURN]]", "[[EF-CAMPAIGN-MODES-I0-LOCAL]]", "[[EF-CAMPAIGN-MODES-DESIGN]]"]
aliases: []
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/project
---

# Change Log — Echo campañas I0-S3R2 (2026-10-29)

## Cambios

- CREATE `10-projects/Echo Futures/artifacts/backtester/EF-CAMPAIGN-MODES-I0-S3R2-RETURN.md` — retorno ONE-SHOT de I0-S3R2: STATUS READY_FOR_MANAGER_REVIEW, M1–M4 CORRECTED_AND_VERIFIED, REPAIR_SHA `8105ef6a657e02a319a9df7fa79d4671d6b10932` (push con readback sobre base `bab3bef1`), reproducción de defectos contra el HEAD pre-reparación (11 checks FAIL con suite 62/62 verde), gate completo re-ejecutado (69/69 reporter, 124/124 legacy, E2E R03 doble byte-idéntica reconciliada con 4/4 MATCH bajo el mapping Go, sentinel PASS, inputs intactos, coverage 100% 442/442), E7/E8b y F1–F11/G1–G4 sin regresión (25/25 frozen).
- CREATE `80-agents/journal/agent-runs/2026-10-29-zcode-glm-5.3-flash-echo-campaign-modes-i0-s3r2.md` — registro atribuible del shot (GLM-5.3-Flash LOCAL, un writer, sin subagentes).
- CREATE este change_log.
- Repo xKoRx/echo (fuera del vault): `feature/ef-campaign-modes-i0@8105ef6a` — `economics_report.py` (M1 `FUNDING_SUM_KINDS`/`FUNDING_TOTAL_KINDS` con la asignación Go de `platform_research.go::finishResearchFunding` y UNKNOWN explícito para RESET_PAID sin término Go; M2 `credited_payments` exige net>0 y la corroboración del primer cobro pasa a ser por cuenta y ventana — positivo PAYOUT_COLLECTED in-window atribuido a la cuenta, o pooled no atribuido sólo si la atribución W reconcilia; reversos/post-cutoff/cash ajeno/pooled no reconciliado nunca acreditan; M3 `_classify_setup_costs` sustituye a `_classify_f_op`/`_funded_frontier`: setup por kind Go a nivel campaña con F_op 0 por vocabulario y atribución UNKNOWN; M4 `_attempt_groups` exige request sellado inmutable en la cadena declarada, caso contrario UNKNOWN_EXECUTION_RELATION), `test_economics_report.py` (+7 falsificadores permanentes M1–M4 en `I0S3R2FalsifierRegressions`, 3 TCR al criterio corregido — 69 total) y append de la sección I0-S3R2 en `specs/FEAT-CHALLENGE-HISTORY/changes/CHANGE-001-campaign-modes-i0-economics.VERIFICATION.md`. `research_lab.py` byte-idéntico; cero cambios Go/SDK/runtime/guard/launcher/presets/receipts.

## No cambiado

- Retornos I0-S1/S2/S3/S3R1 (VERIFY/FINAL/IMPLEMENTATION/S3R1) intactos; planner único [[Echo Futures — Optimización de Campañas]] sin editar (integración corresponde al manager); diseño [[EF-CAMPAIGN-MODES-DESIGN]] intacto (C05-R2 ya publicado por el manager es la precisión aplicada).
- Estados adjudicados que permanecen abiertos: gate Owner de I0, S04-F01/F02, PROD FROZEN, I1–I4 y GOD-COMPOSITION sin despachar.
- Commit Agents-OS: NOT_EXECUTED (vault `main/` sin `.git` accesible en esta superficie; fricción ya registrada en feedback de S1–S3R1, sin novedad).

# Echo Futures — D6 Shot 1 — Manager QA Remediation (F-MGR-01/02/03)

**Shot:** D6 Shot 1 — Manager QA Remediation (narrow; no redesign)
**Role:** SAME Senior Implementation Lead of Shot 1 (IMPLEMENTER; no Manager, no Owner, no adversarial reviewer)
**Date:** 2026-10-02 (remediation commits 22:1x–00:0x local -03)
**Project:** [[Echo Futures]]
**Baseline before:** `xKoRx/echo@4b05d6f856df41b748ad2bfb1f0806b45349387f` (`origin/feature/d6-shot1-execution-vertical`, `D6_SHOT1_IMPLEMENTATION = READY_FOR_ADVERSARIAL_REVIEW` + `D6_SHOT1_MANAGER_QA = REPAIR_REQUIRED`)
**Final SHA:** `14b0d72b811ef618190130f70e9fa748dfb90088` (push FF verificado `origin == local HEAD`; 2 commits de remediación sobre el baseline)
**Trigger:** `D6_SHOT1_MANAGER_QA = REPAIR_REQUIRED` con exactamente 3 findings (F-MGR-01/02/03)
**Verdict:** `D6_SHOT1_MANAGER_REMEDIATION = PASS`

## 0. Hard safety

Sin regresiones en los contratos aceptados: ACCOUNT_IDENTITY / STOP_MARKET_STACK / NINJATRADER_EXECUTION_LANE / EXECUTION_ADAPTER / M1_M2 / JOURNAL / RECONCILIATION / MARKET_FRESHNESS / WARMUP_REBUILD / NINJATRADER_8_1_8_3_COMPILE permanecen PASS (suites completas verdes después de la remediación; los cambios de F-MGR-02 extienden el materialization GAU50 y sus guards, sin tocar ninguna de esas superficies). `PHYSICAL_EGRESS = DISABLED`; `ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0`; ningún AddOn instalado/ejecutado; sin egress físico. Master y PROD intocados.

## 1. F-MGR-01 — Coverage evidence (PASS)

**Método reproducible** (`/tmp/d6cov/changed_coverage.py`, incluido como apéndice de esta sección): por-statement coverage restringido a las líneas AÑADIDAS por el shot — `git diff f0c82905..HEAD --numstat -- '*.go'` (excluye `_test.go`) para enumerar archivos, `git diff -U0` para los rangos añadidos de cada archivo, e intersección contra los coverprofiles fusionados de las suites scoped (`go test -coverprofile` en `v3/futures-bridge/...`, `v3/sdk/futures/...`, `v3/core/{internal/functions,internal/futuresruntime,config/futures}`). Un reviewer reproduce con: regenerar los 3 profiles con los comandos de §1.3 y correr el script.

**Resultados:**

| Métrica | Valor |
|---|---|
| Statements añadidos por el shot (Go, sin tests) | 1228 |
| Cubiertos (raw) | 1154 = **94.0%** |
| Exclusiones documentadas (precisas, §1.2) | 55 |
| **Cubierto / medible (1228−55)** | **1154/1173 = 98.4%** |

Por archivo (raw): los 22 archivos-changed con ≥95%: 19 archivos al 100%, ntx/frame 98.5%, ntx/observations 97%, warmup/envelope 95.7%, ntx/server 95.7%; bajo 95% crudo con exclusiones que los llevan al umbral: rulesets.go 89.1% (4 exclusiones canonical + 1 por corroboración), runtime.go 92.9% (el 1 stmt añadido-descubierto es preexistente/hunk-artifact; el stmt D6 nuevo está cubierto), adapter.go 94.8% (23 → 8 exclusiones canonical/lane-race/tracker/ListOpenOrders), publishing.go 93.9% (4 plan-level por-contrato), envelope.go 95.7% (1 marshal por-contrato), wire.go 80% (1 marshal por-contrato), cmd mains 24.3%/0% (DI-wired, deployment-verified).

**Comandos de reproducción** (desde el repo en `14b0d72b`):

```bash
cd v3/futures-bridge && go test -coverprofile=/tmp/bridge.out -count=1 ./...
cd ../sdk          && go test -coverprofile=/tmp/sdk.out -count=1 ./futures/...
cd ../core         && go test -coverprofile=/tmp/core.out -count=1 \
    ./internal/functions/ ./internal/futuresruntime/ ./config/futures/
python3 changed_coverage.py f0c82905 . /tmp/bridge.out /tmp/sdk.out /tmp/core.out
```

**Nuevos tests añadidos en la remediación** (resumen): journal de fallo scripteado por-método (todas las ramas de error de journal en Submit/Accepted/Rejected/ERROR/timeout, acciones, convergencia en runtime y reconciliación), lane client silencioso (timeout→AMBIGUOUS con journal en fallo), sink con error + sink swap race-safe, evidencia con id nativo NT, reconciliación found/history con errores de journal y sink, clasificación de órdenes terminales en ListOpenOrders, server ntx (defaults, listen en puerto ocupado, cancelación de ctx, frame oversized, garbage mid-stream, líneas vacías, hello sin handler, write sobre conn cerrada), guards restantes de frames/observaciones, `StreamFreshnessBlocks` scenarios (dominio), validación STOP_MARKET a nivel engine, `Compose` fail-closed por bounds inválidos, wiring main (seam `ntxConfigSource`: token fail-closed, ref requerida, error de constructor), guards GAU50 internos y 11 mutaciones de drift.

**Exclusiones documentadas (cada una precisa):**

1. **cmd mains (30 stmts)** — cuerpos DI-wired (`di.Container` ETCD/Kafka vivo). El delta D6 del relay (ProviderAccountRef) está **deployment-verificado**: release `170a4581` corriendo con `binding_loaded=true` y `binding_match=RESOLVED` físico — evidencia más fuerte que unit scope. El delta de buildSession (rama NINJATRADER) delega a `buildNinjaTraderAdapter`/`bindingRef`, que están 100% cubiertos por unidad.
2. **Ramas de error canonical-decimal (9: rulesets×4, adapter×5)** — `units.Price` rechaza racionales no-decimales finitos en unmarshal/construcción; `CanonicalString` no puede fallar después.
3. **Ventanas mid-flight de escritura de lane (5: Submit 613-616, awaitAction 743-747)** — la pérdida TCP dentro de la llamada de escritura es una carrera no determinista; la semántica de convergencia (resolvePending + MarkAmbiguous) está cubierta por el seam extraído `laneWriteFailed`; la ventana física real es el drill de Shot 3.
4. **tracker.Accept error (1) y ListOpenOrders error (1)** — siempre nil por contrato.
5. **Idle-timeout del lane (1)** — deadline de 10 minutos, fuera del presupuesto de tiempo unit.
6. **warmup plan-level Anchor/Candidate errors (4) y envelope marshal (1)** — inalcanzables para un corpus que pasó Validate+Synthesize (candidatos no vacíos, payloads serializables por contrato).

## 2. F-MGR-02 — GAU50 rules in the engine (PASS)

Las reglas monetarias del provider ahora viven en el rules engine con su semántica real de ESTADO DE CUENTA (familias safety-input del contrato congelado D2-05C §6 — no como caps por orden). Commit `572a067a`; materialization `v3/core/config/futures/gau50-eval-v1.json` con **4 SourceRefs**.

**Matriz GAU50-EVAL v1:**

| RULE | SOURCE | SEMANTICS | ENGINE REPRESENTATION | INPUT/STATE | EVALUATION | TEST |
|---|---|---|---|---|---|---|
| Max size 6 contratos | Preflight 2026-09-30 (Evaluation row, HIGH) | Cap de exposición de cuenta | `CapacityCaps[GROSS, account-wide, 6]` (frozen §15) | Firm + reserved por operación en `provider_rules` | Deny EXPOSURE_CAP por el path frozen de reservation | 6 grant / 7 deny / 4+3 deny (`TestGAU50EvalV1_CapacityEnforcement`) |
| New risk hasta 15:50 CT | Ídem + artículo evaluation-hours | Ventana new-risk por tz del provider | `AllowedNewRiskWindow` America/Chicago (día [00:00,15:50) + evening [17:10,23:59), L-V; forma frozen half-open civil) | Reloj del provider owner | `WINDOW_CLOSED` en el edge 15:50; ALLOW interior/evening | `TestGAU50EvalV1_WindowEnforcement` |
| Daily Loss Limit USD 1,100 | Preflight (DLL 5pm–5pm CT, open+closed+commissions) | **Account-state safety input** (D2-05C §6), NO cap por orden | `DailyLoss{ABSOLUTE, 1100 USD, INITIAL_BALANCE, flatten_on_trigger}` | `AccountSnapshotUpdate.DailyLossBreached` del account-state plane | `RISK_STATE_TRIGGERED` deny + ForceClose (safety plane) bajo flatten | `TestGAU50EvalV1_AccountStateSemantics/daily_loss` |
| EOD Drawdown USD 2,000 | Preflight (EOD trailing: ratchet desde balance EOD positivo, nunca retrocede, cap en balance inicial; open-equity puede cruzar intradía) | **Account-state safety input** | `TrailingDrawdown{EOD_TRAILING, 2000 USD, INITIAL_BALANCE, flatten_on_trigger}` | `AccountSnapshotUpdate.TrailingBreached` | `RISK_STATE_TRIGGERED` deny + ForceClose | `TestGAU50EvalV1_AccountStateSemantics/eod_drawdown` |
| Consistency 30% | Preflight (FACT: aplica sólo a Evaluation, al pasar) | **Pass-time monitored outcome** del provider (día con ≥30% del PnL total al pasar) | **DOCUMENTATION_ONLY por contrato** (freeze §9): no existe punto de evaluación pre-egress en las typed families congeladas; codificar un check de best-day-share inventaría enforcement que el provider hace al evaluar el pass | PnL total al pasar (dato del provider, no de Echo) | Ninguna en V1; el owner la monitoriza contra su registro de trading | Guard: `AssertGAU50EvalV1FrozenShape` exige ausencia de families falsas |
| Profit target USD 3,000 | Preflight | Criterio de pass de la evaluación (no constraint de egress; el TP de GerardMM es owner config D4) | Documentation (SourceRefs) | — | Provider al evaluar el pass | — (informativa) |
| News allowed / no minimum days / max 5 evaluaciones concurrentes | Preflight | Hechos informativos del programa, sin semántica de enforcement por cuenta activa | Documentation (notes + SourceRefs); `News` queda nil (news allowed) | — | — | Guard anti-drift |

**DOCUMENTATION_ONLY_PROVIDER_RULES:** `CONSISTENCY_30` (con la contradicción arquitectónica exacta devuelta al Primary Manager, §5), más los hechos informativos de arriba (no son program rules de enforcement por cuenta).

**Guard anti-drift extendido** (`AssertGAU50EvalV1FrozenShapeOn`): exige DD/DLL codificados con valores exactos y flatten, ventana exacta, cap exacto, News/ForcedFlatCutoff ausentes — y rechaza 14 mutaciones testeadas (cap↑, familia cambiada, edge movido, tz movida, evening movida, single-window, DLL limit/currency/flatten, DD variant/basis, news codificada, forced-flat codificada, status drifted).

## 3. F-MGR-03 — OD-D6-2 removal (REMOVED)

- **Eliminado** del registro de decisiones vigente y del estado del proyecto: OD-D6-2 ("ratificación owner de valores GAU50-EVAL") queda **SUPERSÉDED/NOT_REQUIRED** — los valores son autoritativos por la evidencia aceptada (preflight + N1-R2) y Shot 1 no reportó contradicción de fuentes.
- **Shot 1 artifact**: la sección de remediación (§4) sustituye el handoff anterior; el registro OD-D6-2 del Freeze (artefacto histórico) NO se reescrita — queda la marca de supersession aquí.
- **Shot 3 prerequisites**: ahora es únicamente **OD-D6-1** (autorización explícita control-plane antes del primer egress físico) + los gates físicos escalonados. OD-D6-3 (escalación condicional si el feed live sale stale) y OD-D6-4 (ciclos owner-assisted, standing) permanecen operativos, no son gates de ratificación.
- No se implementó ningún estado/product model de autorización (sin OwnerRiskAcceptance ni equivalente).
- No hay conflicto de fuentes GAU50 que requiera decisión owner; la única question abierta es de arquitectura (consistency, §5) y es Manager-level.

## 4. Cambios exactos

| Commit | Contenido |
|---|---|
| `572a067a` | F-MGR-02: DD 2000 + DLL 1100 codificados (familias safety-input), guard extendido, tests de account-state semantics, 4ª SourceRef |
| `14b0d72b` | F-MGR-01: metodología de cobertura changed/new-logic + batería de tests de ramas de error/fallo (ver §1) |

SHA before/after: `4b05d6f8…` → `14b0d72b…` (push FF a `origin/feature/d6-shot1-execution-vertical`).

## 5. Contradicción devuelta al Primary Manager (única question abierta)

**CONSISTENCY_30**: regla autoritativa y relevante de GAU50-EVAL cuyo semantics real es un **outcome monitorizado al momento del pass** ("ningún día ≥30% del PnL total al pasar"). El contrato ProviderRuleSet congelado tiene typed families cerradas de enforcement pre-egress (caps, ventanas, safety-inputs de estado de cuenta); no existe familia para un criterio de pass monitorizado por el provider, y el freeze §9 congeló explícitamente NO modelarla (codificarla como cap "pretendería un enforcement que no existe"). Opción conservadora aplicada: DOCUMENTATION_ONLY con provenance. Si el Primary Manager requiere representation estructural, la vía sería una familia aditiva nueva (contract change D5) — decisión de Manager, no del implementador y no del Owner.

## 6. Suites y seguridad

- Suites verdes post-remediación (`go test -race -count=1`): `v3/sdk/futures/...`, `v3/futures-bridge/...`, `v3/core` functions+futuresruntime+config/futures. Cobertura: §1.
- `PHYSICAL_EGRESS = DISABLED` — sin cambios de deployment en esta remediación (relay sigue en release `170a4581`; bridge sin sesiones; capability gate CLOSED).
- `ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0`.

## 7. Handoff

```text
D6_SHOT1_MANAGER_REMEDIATION =
PASS

BASELINE:
4b05d6f856df41b748ad2bfb1f0806b45349387f

FINAL_SHA:
14b0d72b811ef618190130f70e9fa748dfb90088 (origin/feature/d6-shot1-execution-vertical, push FF)

F_MGR_01_COVERAGE:
PASS

CHANGED_NEW_LOGIC_COVERAGE:
raw 1154/1228 = 94.0% · con exclusiones documentadas 1154/1173 = 98.4% (≥95% cumplido)

COVERAGE_METHOD:
git-diff added-hunk slicing (numstat + -U0) ∩ go coverprofiles de suites scoped (-race -count=1); script + comandos reproducibles en D6-SHOT1-MANAGER-QA-REMEDIATION §1

F_MGR_02_GAU50_RULES:
PASS

GAU50_RULES_IN_ENGINE:
cap GROSS 6 (reservation) + ventana 15:50 CT (admission) + DLL 1100 y EOD DD 2000 como safety-inputs de estado de cuenta (deny RISK_STATE_TRIGGERED + ForceClose, testeado por breach) — 4 SourceRefs; guard anti-drift con 14 mutaciones

DOCUMENTATION_ONLY_PROVIDER_RULES:
CONSISTENCY_30 (pass-time monitored outcome; contradicción arquitectónica devuelta al Primary Manager) + hechos informativos del programa (profit target 3k, news allowed, no minimum days, max 5 concurrentes — sin enforcement por cuenta activa)

F_MGR_03_OD_D6_2:
REMOVED (superseded/not-required en registro vigente, proyecto y artefacto Shot 1; el registro histórico del Freeze no se reescrita)

REMAINING_OWNER_GATES:
OD-D6-1_PHYSICAL_EGRESS_ONLY (control-plane, antes del primer egress físico; OD-D6-3 condicional y OD-D6-4 standing permanecen operativos, no son gates de ratificación)

REGRESSION:
ACCOUNT_IDENTITY/STOP_MARKET_STACK/NINJATRADER_EXECUTION_LANE/EXECUTION_ADAPTER/M1_M2/JOURNAL/RECONCILIATION/MARKET_FRESHNESS/WARMUP_REBUILD/NINJATRADER_8_1_8_3_COMPILE = PASS (suites completas -race verdes; sin cambios en esas superficies)

PHYSICAL_EGRESS:
DISABLED

ORDERS_SENT:
0

ORDERS_MODIFIED:
0

ORDERS_CANCELLED:
0

CONTRADICTIONS:
CONSISTENCY_30 representation (arquitectura frozen vs pass-time monitored outcome) — devuelta al Primary Manager; no bloquea el shot (la regla queda honestamente documentation-only)

OWNER_DECISION_REQUIRED:
NONE (OD-D6-1 permanece como gate de Shot 3; no se reutiliza OD-D6-2)

D6_SHOT1_IMPLEMENTATION:
READY_FOR_ADVERSARIAL_REVIEW

NEXT_MANAGER_ACTION:
Dispatch D6 Shot 2 adversarial review sobre 14b0d72b (adjudicar CONSISTENCY_30 como input del review). No iniciar Shot 2 desde esta sesión.
```

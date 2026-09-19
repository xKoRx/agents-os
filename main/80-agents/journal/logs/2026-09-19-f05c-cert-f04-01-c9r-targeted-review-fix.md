---
type: change_log
schema_version: 1
scope: session
created: "2026-09-19"
updated: "2026-09-19"
area: "[[Echo]]"
project: "[[Echo + Echo Forge — Deferred Certification Backlog]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo]]"
related:
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-19-f05c-cert-f04-01-c9r-targeted-review-fix

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (nuevo delta fechado `2026-09-19 — Delta de corrección de revisión C9R` con veredicto `SOURCE_READY_FOR_MANAGER_REVIEW` + actualización de `Estado de entrada` + actualización de `Próxima tarea única recomendada para NORMAL` (estado vigente tras C9R, Consumidas ampliada con C9R, próximo paso único = revisión manager sobre `87a3ab9…66faa42` → release → RERUN-5); CERT-F04-01 permanece `BLOCKED` con el fix ampliado esperando revisión)
  - `10-projects/Echo Forge/Echo Forge.md` (entrada de bitácora 2026-09-19 — Session checkpoint C9R)
  - `80-agents/journal/agent-runs/2026-09-19-zcode-glm-5.3-flash-f05c-cert-f04-01-c9r-targeted-review-fix.md` (creado)
  - `xKoRx/symphony` — commit único `66faa42debba18cd0dd09de127ae1374ea2a07f0` en rama `codex/f05-seal-apply-authority-fix` (parent exacto `87a3ab944c5ce706ac3fe7766fa86af32189cc05`, publicado en origin; 3 archivos del allow-list, 199+/0−; efectos de código documentados aquí y en el delta C9R)

## Motivo

- Ejecución de la misión `F05C-CERT-F04-01-C9R` (targeted manager review fix): cerrar los dos hallazgos de revisión del source C9 — el validador del fan-in del final reretester conservaba `DecisionRef` y demás carriers pero no comparaba la nueva autoridad `ApplyEvaluationRef`, y faltaban pruebas del boundary que demostraran rechazo ante mutaciones de esa autoridad — sin rediseñar el fix C9 y sin ejecutar gates posteriores.

## Fuentes usadas

- Mandato maestro F05C-CERT-F04-01-C9R (baseline inmutable `87a3ab9…`, R1–R3, allowed files, prohibiciones, formato de handoff).
- Delta C9 (`80-agents/journal/logs/2026-09-19-f05c-cert-f04-01-c9-apply-authority-fix.md`) y contrato canónico [[Echo Forge — F-04 Magic allocation, version seal and handoff]] (reemplazo contractual de `EvaluationRef` por el final reretester, fail-closed sin fallback, `contract_conflict` como categoría de error); source del worktree C9 (`generic_workflow.go`, `durable_apply_selected_run_workflow.go`, tests C9); reglas del repo `.agents/rules/10-anti-test-masking.md`, `01-stack-and-tooling.md` y guard canónico `check-test-masking.sh`.

## Resolución aplicada

- R1: `validateFinalReretesterFanoutOutput` (`sqx/workflows/generic_workflow.go`) agrega la comparación explícita `artifact.ApplyEvaluationRef != input.ApplyEvaluationRef` → error `contract_conflict` (`capabilities.ErrContractConflict`) y ningún resultado parcial. Semántica preservada: referencia Apply válida se conserva byte-exact; input histórico sin Apply sigue fluyendo vacío; la salida no puede inventar, borrar ni sustituir la referencia; `EvaluationRef` continúa reemplazándose por la evaluación del final reretester; el resto de validaciones, cardinalidades, orden y semántica zero-output (G22) intactas; sin fallback, lookup ni recuperación silenciosa.
- R2: `TestFinalReretesterFanoutFailsClosedOnApplyAuthorityMutations` — 3 negativos (drop / replace por otro SHA256 válido / fabricar sobre input vacío) que fallan antes de aceptar el fan-in y abortan el workflow sin etapas posteriores; RED demostrado contra `87a3ab9` (3 FAIL) y GREEN tras R1. `TestSealCompositeApplyFanoutAssemblerHandsExactPerMemberAuthority` — compuesto integrado en memoria que encadena los runners reales (`runDurableApplySelectedRun` → `runFinalReretesterFanout` → `runForgeSealHandoff`) con actividades externas simuladas y compile lineage por fixture, interceptando el request real a `forge_seal_handoff_v1` y verificando por StrategyRef: `ApplyEvaluationRef` producida por Apply, `EvaluationRef` final distinto, `CompileEvaluationRef` correcta y ausencia de cruces entre miembros (no simula el fan-in ni fabrica el carrier final). `TestFinalReretesterFanoutRejectsMutatedOutputBoundaries` — complemento con 4 tests reales de las ramas de rechazo restantes del validador modificado (key inconsistente, StrategyRef ajeno, EvaluationRef no SHA256, carriers alterados).
- R3: 37 fallos históricos (21 `sqx/workflows` + 16 `sqx/activities/worker`) reproducidos en dos worktrees limpios (`c1d24c1` y `66faa42`) con `-count=1` y condiciones equivalentes: conjuntos idénticos por identidad de test y por causa normalizada (diff = 0 en ambos paquetes). Clasificación: 16 workflows = harness del test sin activity `flow_run_start` registrada; 5 workflows = clases contractuales internas de la simulación MT5 backtest/compiler (p. ej. `durable backtest: carrier ausente para output exact key`); 16 worker = fixture físico `../../../mt5-export.htm` ausente. Cero fallos nuevos o agravados por el delta; ningún test contractual Apply/final reretester/promotion/seal fallando por C9/C9R.

## Validación

- Cobertura función-nivel del código modificado: `validateFinalReretesterFanoutOutput` **100%** (80% pre-R2 por 4 ramas preexistentes de la misma función; cubiertas con tests reales, sin inflar números), `runForgeSealHandoff` 100%, `validateApplyCarrier` 100%, `runDurableApplySelectedRun` 95.5% (residual defensivo igual a C9); `sqx/core/runtime` PASS completo; gofmt limpio en los 3 archivos; `go vet ./sqx/workflows/` limpio; builds con los 2 fallos preexistentes demostrados en `87a3ab9` pristine vía stash (`go.work` → `pebbe/zmq4` sin headers libzmq del entorno; `sqx/tools` main redeclarado C6R) — ajenos al delta; anti-test-masking: guard canónico del repo PASS sobre el delta C9→C9R, diff de tests 100% aditivo (199+/0−), cero skips, sin tests preexistentes modificados.
- Publicación verificada: `git ls-remote origin codex/f05-seal-apply-authority-fix` == `66faa42…` == HEAD local; parent exacto `87a3ab9…`; `origin/codex/f05-release-prep` intacto en `c1d24c1…`; diff vs C9 == exactamente los 3 archivos del allow-list; worktrees temporales R3 eliminados sin residuo; sin merge, sin tag, sin release, sin rollout, sin RERUN-5, sin MT5 físico.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, sin credenciales ni secretos; las deudas documentales previas (contraseña SSH en el `AGENTS.md` del repo, Loki sin ingestión del worker) permanecen en sus deltas originales, no reproducidas aquí.

## Rollback

- El fix vive sólo en la rama feature `codex/f05-seal-apply-authority-fix` (sin merge a la rama productiva): revertir = `git revert 66faa42` o re-alinear la rama a `87a3ab9` en local/origin; ningún runtime ni release consumió el commit. Vault append-only (revertir = eliminar el delta C9R, la entrada de bitácora, este log y el agent-run). Worktrees temporales ya eliminados.

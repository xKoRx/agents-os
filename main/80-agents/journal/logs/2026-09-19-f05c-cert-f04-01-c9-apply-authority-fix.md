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

# 2026-09-19-f05c-cert-f04-01-c9-apply-authority-fix

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (nuevo delta fechado `2026-09-19 — Delta de corrección source C9` con veredicto `SOURCE_FIX_READY_FOR_REVIEW` + actualización de `Estado de entrada` + actualización de `Próxima tarea única recomendada para NORMAL` (estado vigente tras C9, próximo paso único = revisión manager → release → RERUN-5, nota `MT5_PROCS=0` cerrada, C9 añadido a Consumidas); CERT-F04-01 permanece `BLOCKED` con el fix publicado esperando revisión)
  - `10-projects/Echo Forge/Echo Forge.md` (entrada de bitácora 2026-09-19 — Session checkpoint C9)
  - `80-agents/journal/agent-runs/2026-09-19-zcode-glm-5.3-flash-f05c-cert-f04-01-c9-apply-authority-fix.md` (creado)
  - `xKoRx/symphony` — commit único `87a3ab944c5ce706ac3fe7766fa86af32189cc05` en rama `codex/f05-seal-apply-authority-fix` (parent exacto `c1d24c1…`, publicado en origin; 6 archivos del allow-list; efectos de código documentados aquí y en el delta C9)

## Motivo

- Ejecución de la misión `F05C-CERT-F04-01-C9` (Fix Apply Authority lineage → Source Ready for Review): corregir en source el cuarto defecto determinístico demostrado por RERUN-4 — el assembler del seal entregaba la Evaluation del final reretester como `ApplyEvaluationRef` porque ambas autoridades compartían el campo `EvaluationRef` del carrier. Sin release, sin rollout, sin RERUN-5, sin reabrir certificaciones anteriores.

## Fuentes usadas

- Mandato maestro F05C-CERT-F04-01-C9 (contrato de corrección, allowed files, tests T1–T7, gates, stop conditions).
- Backlog deferred (estado RERUN-4 `BLOCKED` con RCA anclada) y delta RERUN-4; source del baseline `c1d24c1…` (`generic_workflow.go`, `durable_apply_selected_run_workflow.go`, `forge_seal_handoff.go`, `steps/steps.go`, `core/runtime/config.go`); reglas del repo `.agents/rules/10-anti-test-masking.md` y `01-stack-and-tooling.md`.

## Resolución aplicada

- Contrato C9: campo `ApplyEvaluationRef` (`apply_evaluation_ref,omitempty`) en `runtime.StrategyArtifact`, aditivo (payloads históricos sin el campo decodifican sin autoridad); establecido exclusivamente desde el resultado exitoso de Durable Apply tras las validaciones existentes de identidad y formato; `EvaluationRef` sigue avanzando por etapa (el final reretester lo reemplaza por contrato) y `CompileEvaluationRef` intacto.
- Assembler `runForgeSealHandoff`: consume `carrier.ApplyEvaluationRef`; fail-closed (`contract_conflict`) ante carrier con compile lineage sin autoridad Apply y ante miembros duplicados; exclusión de carriers sin compile lineage y semántica G22 de membresía cero preservadas; sin fallback a `EvaluationRef`, sin lookup latest, sin buscar por StrategyRef.
- Consumer `forge_seal_handoff.go` sin cambios (verificó actuar correctamente); `steps/steps.go` sin cambio (copia por valor del carrier en la ruta del final reretester preserva físicamente el campo; demostrado en source; `rebindExportedObject` sin callers en producción).
- Tests T1–T7: RED demostrado contra worktree temporal @ `c1d24c1` + campo inerte (4 tests de lógica FALLAN); GREEN completo con el fix; consumer contract-freeze (rechazos con firma exacta del error RERUN-4) PASS en ambos lados; suites de paquetes modificados con conjuntos de fallo idénticos al baseline (21 workflows / 16 worker, clases preexistentes documentadas); `gofmt`/`go vet` limpios; `go build` OK salvo `sqx/tools` preexistente; coverage de funciones modificadas 100% (`runForgeSealHandoff`), 100% (`validateApplyCarrier`), 95.5% (`runDurableApplySelectedRun`, residual defensivo); anti-test-masking OK (diff de tests 100% aditivo, cero skips, sin tests preexistentes modificados).
- Preflight de seguridad pendiente de RERUN-4 CERRADO: captura viva `MT5_PROCS=0` 2026-09-19T18:43:13Z vía `mt5-kronos-operator` read-only (metatester64/terminal64/metaeditor64 = 0; `sqx-mt5-worker` singleton = 1); sin detener procesos, sin ejecución física, sin credenciales nuevas.

## Validación

- Publicación verificada: `git ls-remote origin codex/f05-seal-apply-authority-fix` == `87a3ab944c5ce706ac3fe7766fa86af32189cc05` == HEAD local; parent exacto `c1d24c1…`; `origin/codex/f05-release-prep` intacto en `c1d24c1…`; diff vs baseline == exactamente los 6 archivos del allow-list (646+/9−); escaneo de secretos del diff limpio; sin merge, sin tag, sin release, sin rollout.
- Evidencia de tests y cobertura en el worktree de la misión `~/aranea/work/f04-cert-f04-01-c9/symphony-c9` (commit publicado; worktrees temporales de RED y de comparación baseline eliminados sin residuo).

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, sin credenciales ni secretos (la deuda documentada de la contraseña SSH en el `AGENTS.md` del repo permanece registrada en el delta C7, no reproducida aquí).

## Rollback

- El fix vive sólo en la rama feature `codex/f05-seal-apply-authority-fix` (sin merge a la rama productiva): revertir = eliminar la rama en origin/local; ningún runtime ni release consumió el commit. Vault append-only (revertir = eliminar el delta C9, la entrada de bitácora, este log y el agent-run). Allocations write-once sin efecto que revertir.

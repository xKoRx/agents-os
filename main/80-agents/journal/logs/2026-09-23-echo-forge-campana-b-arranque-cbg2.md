# Change Log — 2026-09-23 Echo Forge Campaña B (arranque + CB-G2)

Sesión: mandato CAMPAÑA B (SELECTED COHORT → SQX TICK RETEST → MT5). Recuperación de autoridades, diseño congelado e implementación CB-G2 en branch aislada de symphony (sin merge a master, sin push, sin flota/DEV/PROD). Veredicto software: CB-G2 PASS (regresión == baseline).

## Repositorio symphony (fuera del vault, branch `feature/sqx-campaign-b`)

- `dc151e4` feat(campaign-b): contrato de entrada del cohort seleccionado — runtime `selection_cohort.snapshot_ref` + `BatchOriginSelectionCohort` + binding batch-level en `BatchKeys`; validación fail-closed (exclusión mutua con watcher.import); dispatch watcher porta sólo el binding; bootstrap workflow `runSelectionCohortBootstrap`; activity `resolve_selection_cohort` (re-derivación de identidad del snapshot, artefacto OUTPUT/STRATEGY_SQX exacto por Builder Evaluation, membresía `REPROCESSED` insert-once, identidad canónica vía StrategyIdentityReader); tests runtime + activity (6 casos).
- `3847cad` docs(campaign-b): SPEC `FEAT-SQX-IMPORT-CAMPAIGN-B` §2.1 (decisión CB-G2), §4 gates y §5 desbloqueo parcial (Import G7 cumplido).
- Base `9a69243` (== `origin/master`, verificado por fetch + read-back); worktree externo `/home/kor/aranea/work/campaign-b-20260923/symphony` con symlink `../sdk` → checkout canónico.

## Verificación

- Build verde en paquetes relevantes (`sqx/core/...`, `sqx/activities/...`, `sqx/workflows/...`, `sqx/adapters/...`, `sqx/cmd/sqx-worker`); fallo `sqx/tools` pre-existente (varios main brownfield).
- Regresión por nombre: `sqx/workflows` 21 fallos y `sqx/activities/worker` 16 fallos idénticos al baseline (MT5 reconcile/score incluidos, pre-existentes); `sqx/core/runtime` y `sqx/activities/watcher` verdes; gofmt/vet limpios en el delta (16 archivos sin formatear pre-existentes).

## Sistema 2

- Creado `10-projects/Echo Forge/Echo Forge — Campaña B.md` (materializado por contrato): objetivo, estado CB-G2, entregable, tareas CB-G0..G7, decisiones D-B1..D-B5, bitácora.
- Actualizado `10-projects/Echo Forge/Echo Forge.md`: tarea puente de Campaña B, bullet de estado actual, entrada de bitácora 2026-09-23, `updated: 2026-09-23`.

## Decisiones congeladas (resumen)

- D-B1 entrada = sección declarativa + bootstrap interno (no task source; espejo D10).
- D-B2 participación REPROCESSED (is_origin=false) insert-once.
- D-B3 tick retest = retester durable `stage=retester` (el final reretester exige DecisionRef de Apply, ausente en cohort importado); modo tick/OOS vive en el CFX (owner §3).
- D-B4 semántica PASS separada: pipeline / validación de estrategia / fallo técnico.
- D-B5 seal V2 (handoff Echo) fuera de B-v1: exige linaje Apply+Compile y readback magic; sin Apply no hay magic estampado ⇒ 0 manifests.

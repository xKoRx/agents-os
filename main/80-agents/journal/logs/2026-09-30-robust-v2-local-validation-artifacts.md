---
type: change_log
schema_version: 1
scope: session
created: "2026-09-30"
updated: "2026-09-30"
area: "[[Echo]]"
project: "[[Echo Forge — Robust Run Selection V2]]"
application:
entities:
  - "[[Echo Forge — Robust Run Selection V2]]"
related:
  - "[[Echo Forge — Operación Real V2]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-09-30-echo-forge-robust-v2-local-validation-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Robust Run Selection V2 — Local Validation V1 vs V2 (wave2a)

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - `10-projects/Echo Forge — Robust Run Selection V2/ROBUST-V2-LOCAL-VALIDATION.md` (creado)
  - `10-projects/Echo Forge — Robust Run Selection V2/ROBUST-V2-LOCAL-VALIDATION.csv` (creado)
  - `10-projects/Echo Forge — Robust Run Selection V2/artifacts/local-validation-20260930/` (creado: strategies.tsv, v1_candidates.tsv, v2_candidates.tsv, details.json, five_cases.json, v2_stage_counts.json)
  - `10-projects/Echo Forge — Robust Run Selection V2/Echo Forge — Robust Run Selection V2.md` (estado, tarea, bitácora, docs/links)
  - `80-agents/journal/agent-runs/2026-09-30-zcode-glm53-robust-v2-local-validation.md` (creado)
  - `80-agents/journal/feedback/system-1/2026-09-30-echo-forge-robust-v2-local-validation-session-feedback.md` (creado)

## Motivo

- Mandato de Local Validation Lead: ejecutar V1 vs V2 sobre los mismos datos reales de la cohorte wave2a y reportar cambios/rejections/sanity, sin product code ni tuning.

## Fuentes usadas

- [[ROBUST-V2-DESIGN-FREEZE]]; nota de proyecto; bundle `c52-wave2a-20260929` (cells.tsv SHA `3e0dac…` == manifest, verificado también contra `~/aranea/work/forge-recovery-c52-20260928/artifacts/`); spec `flow-recovery-c52-wave2a.json`; repo `xKoRx/symphony` @ `origin/feature/robust-selection-v2-shot1` `bc50bbb`.

## Resolución aplicada

- Veredicto `LOCAL_VALIDATION_PASS`: mismo set de 16 rechazadas; 6 FAIL-SEVERE de V1 → WARN en V2; 13/18 rank1 cambiados, 13/13 a menor `R_retdd`; cliff 26/214 (12,15%); sin defecto de implementación. Hallazgo de lineage registrado: el payload `cells.tsv` con hash `3e0dac…` existe íntegro (el finding "zero bytes" corresponde a otra copia); los aggregates/picks del bundle son otra materialización (discrepancia Optimizer-vs-WFM ya registrada).

## Validación

- SHA256 verificado (bundle vault == workspace original); probe con asertos internos (sobrevivientes == picks 34/34); `go vet` limpio; regresiones `./sqx/core/wfm/... ./sqx/adapters/wfm/binding/...` PASS tras eliminar el probe; `git status` limpio en worktree y clon base; worktree removido.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos ni paths sensibles (sólo rutas relativas del vault/workspace registradas por la entidad).

## Rollback

- Revertir este commit para retirar los artefactos de validación; el repo `xKoRx/symphony` no tiene cambios que revertir.

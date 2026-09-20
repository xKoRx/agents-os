---
type: change_log
schema_version: 1
scope: session
created: "2026-09-20"
updated: "2026-09-20"
area: "[[Personal]]"
project: "[[POC-S05 — New Market Maturation]]"
application:
entities:
  - "[[POC-S05 — New Market Maturation]]"
  - "[[Polymarket Engine — MVP]]"
  - "[[Polymarket Engine — POC Shared Unblocker]]"
related:
  - "[[2026-09-20-zcode-glm-5.3-flash-pe004-regularizacion]]"
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

# 2026-09-20-pe004-post-shared-regularization

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Personal/Polymarket Engine/POC-S05 — New Market Maturation.md` — edición local quirúrgica desde blob baseline `5bd4c261a4176eb39b51bad4727b979cac574a12` (vault HEAD `c6e61a17`); identidad, hipótesis, cohortes O/B/W/C, parámetros v1 y F01–F20 preservados; sin recreación de nota.

## Motivo

- El proyecto [[Polymarket Engine — POC Shared Unblocker]] publicó INTEGRATION_SHA `9d0512a` (rama `feature/shared-poc-unblocker`, 8 commits SFG rebasados sobre `feature/research-strategies-v01@f070496`, sin push, Review humana pendiente). La SPEC y el roadmap de PE-004 describían el estado previo (SFG-05 como CR propuesto, dependencias contra `25f578a`, fixtures 20); había que regularizar la nota contra los contratos reales sin implementar la POC.

## Fuentes usadas

- Notas: [[POC-S05 — New Market Maturation]] (planner único), [[Polymarket Engine — POC Shared Unblocker]] (handoffs, matriz, receipts), [[Polymarket Engine — MVP]] (sólo lectura; tarea puente ya existente en `[r]`).
- Repositorio: `xKoRx/polymarket-engine` checkout `feature/research-strategies-v01@f070496` + worktree `polymarket-engine-shared@9d0512a`; inspección de símbolos y tests dirigidos re-ejecutados por esta sesión (build PASS; `TestSFG05*`, SFG03/Replay, SFG01/07, `TestSFG06NewMarketKnownAtDedup`/`NoticeEdges` PASS).

## Resolución aplicada

- Callout y estado: `OB_SPEC_READY_SHARED_VERIFIED`; `PE004_OB_START_ALLOWED=true` (`READY_WITH_RESTRICTIONS`, baseline arranque `9d0512a`); `PE004_W_START_ALLOWED=false` (`WS_COHORT_BLOCKED`); `ENGINE_MERGE_PENDING_OWNER_REVIEW` documentado.
- Dependencias: matriz SFG re-estado contra `9d0512a` (`VERIFIED_9d0512a`/`EXISTS_9d0512a`/`MISSING_CONFIRMED`); hallazgo SFG-05 marcado RESUELTO; CR SFG-05 y CR SFG-01 `SUPERSEDED_BY_IMPLEMENTATION` (historia preservada).
- SPEC técnica: contratos consumibles con firmas reales; salida PE-004 definida como claves canónicas `pe004.*` dentro de `FrameObservation sfg05_v1` (sin inventar campos de API; identidad la porta `ObservedFrame`).
- Roadmap: Track O/B (A0–B3, C2, C3) y Track W (C1 condicional a `WS_COHORT_READY`); cada WP con dependencias, gate, archivos permitidos/prohibidos, contratos, fixtures, tests, PASS/FAIL, evidencia, política de datos ausentes y cierre. A0 anota preflight git ya ejecutado; ninguna tarea marcada completa.
- Fixtures: corpus 20→22 (F21 sensibilidad de digest, F22 aislamiento de instancias) con columna de tests nombrados; F03/F04 marcadas W-condicionales para E2E; DoD A=22.
- Gates/mandato: regla de autorización del coding agent (`INTEGRATION_SHA`, `ENGINE_INTEGRATION_PASS`, `POC_START_ALLOWED`, `WS_COHORT_READY`), prohibiciones ampliadas (no reimplantar shared, no merge/push de la rama shared), primera tarea exacta = A1 + B1 sobre `FrameObserver`.

## Validación

- Linter canónico: 0 hallazgos sobre la nota POC-S05 (FAILs CL-06/11/15/21 restantes son corpus-wide preexistentes, ajenos a este cambio).
- Graphify: `GRAPHIFY_NOT_RUN` (no instalado en esta máquina; retrieval por búsqueda directa).
- Nota materializada sin script por ser edición de entidad existente; archivos journal (`change_log`, `agent_run`) materializados vía `materialize_schema_note.py`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- `git checkout c6e61a17 -- "10-projects/Personal/Polymarket Engine/POC-S05 — New Market Maturation.md"` y eliminar los dos archivos journal nuevos; sin efectos laterales fuera del vault (engine y datasets intactos).

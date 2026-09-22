---
type: change_log
schema_version: 1
scope: session
created: "2026-09-21"
updated: "2026-09-21"
area: "[[Personal]]"
project: "[[Echo Forge]]"
application:
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge — Import Task V1]]"
related:
  - "[[Echo + Echo Forge — Environment Contract]]"
  - "[[2026-09-21-echo-forge-import-task-v1]]"
aliases:
  - "Import V1 review MR-1/MR-2 y preparación G7 2026-09-21"
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
  - area/personal
  - project/echo-forge
---

# Change Log — 2026-09-21 · Import V1 — review MR-1/MR-2 y preparación G7

## Cambios

- Repo `xKoRx/symphony` rama `feature/sqx-import-task-v1`: push FF `5e495ae → 3d04d68` (1 commit). Master intacto `745bc8b`; flota 0.2.105 intocada; nada arrancado ni desplegado.
- Review técnica MR-1/MR-2 con evidence pack nuevo `specs/FEAT-SQX-IMPORT-TASK-V1/REVIEW-MR1-MR2-20260921.md` (TECHNICAL_REVIEW_CLEAN en ambos; aprobación formal sigue en manager).
- Corrección de autoridad proyecto/plugin en SPEC §4.1/§4.2 + nueva §12: proyecto SQX local `EchoForgeImportExporter` (código) y plugin `EchoForgeOverviewExporter` (CustomAnalysis); runbook ya era consistente.
- Runbook G7 §2: receta con `custom_analysis_plugin=EchoForgeOverviewExporter` (download_config falla cerrado sin él); §1.4 clarificada; nueva §5 (G7 de un host = certificación parcial).
- SPEC §4.3 reescrita: binding single-FlowRun en tres capas + gap multi-host declarado (selección global cross-host NO existe en V1; requiere amendment futuro cross-FlowRun). TOP-DECISIONS: D7 precisado + sección de correcciones + estado G7 = parcial.
- Test nuevo `sqx/core/domain/producer_flowrun_binding_test.go` (2 tests verdes) fijando el binding single-FlowRun de clasificación y ranking.
- Anexo nuevo `specs/FEAT-SQX-IMPORT-TASK-V1/RUNBOOK-DEV-AISLADO-OPCION-B.md` (candidato DEV PREPARED/PENDING_RT1; verificación RO: namespace `sqx-dev` existe, ETCD `/symphony/development/` 40 keys, cola compartida `sqx-main-queue` excluida).
- Actualizada la nota de proyecto [[Echo Forge — Import Task V1]] (tareas + bitácora) y memoria `echo-import-task-v1-state`.

## Motivo

Mandato owner IMPORT V1 (review y cierre físico): revisar MR-1/MR-2, resolver discrepancia de nombres del proyecto SQX, determinar alcance multi-host con contratos y tests, y preparar el runtime DEV aislado opción B sin autorizar ni arrancar nada.

## Validación

- Suites dominio/runtime/activities/workflows/adapters/cmd: fail-set de la rama idéntico al baseline `745bc8b` (21+1 nombres; 0 regresiones nuevas); paquete domain completo verde con los tests nuevos.
- Push FF verificado (`origin/feature/sqx-import-task-v1 == 3d04d68`, `origin/master == 745bc8b`).
- Efecto lateral detectado y no commiteado: benchmark reescribe `specs/FEAT-SQX-STRATEGY-EVALUATION/fixtures/phase4_performance.json` (preexistente; restaurado).

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos; valores ETCD citados no-secretos (namespace, colas, rutas).

## Rollback

- Revertir el commit `3d04d68` en la rama (docs + tests, sin código productivo) y revertir la nota de proyecto; nada de infraestructura fue mutado.

---
type: change_log
schema_version: 1
scope: session
created: "2026-09-22"
updated: "2026-09-22"
area: "[[Personal]]"
project: "[[Echo Forge]]"
application:
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge — Import Task V1]]"
related:
  - "[[Echo + Echo Forge — Environment Contract]]"
  - "[[2026-09-21-import-v1-review-g7-prep]]"
aliases:
  - "Import V1 reviews independientes y RT-1 2026-09-22"
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

# Change Log — 2026-09-22 · Import V1 — reviews independientes, fixes y solicitud RT-1

## Cambios

- Rama `feature/sqx-import-task-v1`: push FF `3d04d68 → 6ad247a → bed8d31 → 329ee94` (master intacto `745bc8b`; flota intocada; nada arrancado).
- **Reviews independientes (mandato owner: revisor externo):** ronda 1 con dos agentes verificadores adversariales de contexto fresco (runs `dwfrun-aa80d4e6`) sobre `3d04d68`: MR-1 **APPROVED** (10/10 claims PASS) y MR-2 **CHANGES_REQUIRED** (MAJOR H-1: recovery import con constantes Builder ⇒ retry post-crash roto; sin test). Ronda 2 (run `dwfrun-3d728aaa`) sobre el delta: **MR-2 APPROVED** (K1–K8 PASS). Headers de ambos amendments actualizados (INDEPENDENT REVIEW APPROVED / RATIFICACIÓN OWNER PENDIENTE).
- **Fixes en rama (`6ad247a`):** Fix A recovery por contrato de productor (`producerContractForStage`, fail-closed; ruta Builder byte-idéntica); Fix B tests del validador de ranking con evidencia import (accept/unregistered/builder-metricset-cross); Test A de recovery con evidencia import REAL persistida por la ruta de producción; Fix C binding del databank de entrada del plugin parametrizado (`input` import / `output` builder — defecto de integración propio detectado en la preparación: el plugin habría leído un databank vacío en G7); Fix D mensajes de error por contrato. `bed8d31`: fixture del benchmark restaurado (efecto lateral de tests, arrastrado por error en 6ad247a).
- **Preflight G7 opción B** (§6 de `RUNBOOK-DEV-AISLADO-OPCION-B.md`): control-plane verificado RO (flota `sqx-prop`/`sqx-main-queue` vía ETCD production; candidato `sqx-dev`/`sqx-import-cert-v1` con 0 pollers; PG DEV 192.168.31.220/trading_systems; Mongo forge; MinIO 192.168.31.92:9000; 11 `.sqx` auténticos en `running/wave_2/xau/base/`; convención `00_configs/` con `.cfx` por stage — sin `EchoForgeImportExporter.cfx` aún). Host-level NO ejecutable: canal `aranea-ssh` 503 (upstream caído; proxy 401 sin token OK) y Mongo RO `session not found`; sin llave directa (no side-channels).
- **Solicitud RT-1 precisa emitida:** `specs/FEAT-SQX-IMPORT-TASK-V1/RT1-REQUEST-G7-OPCION-B.md` (host propuesto sqx-ulab-kronos sujeto a preflight; comando/plantilla con `ENV=import-cert` y prefix ETCD `/symphony/import-cert-dev/`; binario SHA256 desde `bed8d31`; lista cerrada de 5 recursos modificados; ventana ≤2 h; teardown; rollback; 4 condiciones previas).
- Nota de proyecto y memoria actualizadas.

## Motivo

Mandato owner: reviews independientes con veredicto formal, preflight de lectura del runtime DEV-B, y solicitud RT-1 precisa; sin arrancar worker si RT-1 sigue bloqueado.

## Validación

- Verificada por los revisores independientes (no por la sesión implementadora): K1–K8 PASS en ronda 2, con ejecución propia de tests scoped (7/7 recovery, 4/4 ranking scoped, 3/3 binding cfx, dominio -count=1 en 0) y diffs contra baseline.
- Fail-set de `sqx/workflows`+`sqx/activities/worker` = 21 fallos pre-existentes (causa raíz única del harness `flow_run_start`), idéntico al baseline.
- Push FF verificado; worktree limpio al cierre.

## Compartibilidad

- **Scope:** local · **Redacción revisada:** sin secretos (bearer/tokenes no copiados; endpoints no-secretos citados).

## Rollback

- Revertir los tres commits de la rama (tests/docs/fixes con tests nuevos) y revertir notas del vault; ninguna infraestructura fue mutada.

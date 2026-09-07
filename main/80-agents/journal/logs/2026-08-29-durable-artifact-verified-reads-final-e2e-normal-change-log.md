---
type: change_log
schema_version: 1
scope: session
created: "2026-08-29"
updated: "2026-08-29"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[AGENTS OS]]"
related:
  - "[[2026-08-29-durable-artifact-verified-reads-final-e2e-normal]]"
  - "[[2026-08-29-durable-verified-reads-exporter-double-execution]]"
aliases: []
confidence: verified
source_session: DURABLE-ARTIFACT-VERIFIED-READS-FINAL-E2E-NORMAL
source_feedbacks:
  - "[[2026-08-29-symphony-worker-observability-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-29-durable-artifact-verified-reads-final-e2e-normal-change-log

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambios de estado certificados

- DURABLE-ARTIFACT-VERIFIED-READS-FINAL-E2E-NORMAL intento release `0.2.79` sobre baseline autorizado `1f0880c` terminó `BLOCKED / CLOSED`: doble ejecución de la tarea `overview_exporter` (subida fantasma 17:48:38Z fuera del historial Temporal + intento registrado 17:50:51) produjo dos versiones de `metadata/export_run.json` y el write-once falló cerrado con `CONTRACT_CONFLICT` non-retryable; workflow `Failed`, FlowRun `1e560644-8b39-4ddb-bede-eb2c98e33238` `FAILED` tras builder COMPLETED. Sin fix, sin re-run, sin Temporal Reset, cero cambios de código. Ver [[2026-08-29-durable-artifact-verified-reads-final-e2e-normal]] y [[2026-08-29-durable-verified-reads-exporter-double-execution]].
- Release `0.2.79` (`vcs.revision=1f0880c…`, SDK pin `ea09cc1…`, linux symphony sha256 `692f8c21…`, windows sqx-mt5-worker sha256 `d8f285f7…`) publicada en MinIO y aplicada por stager en Zeus/Hera/Windows MT5 (rotación de PIDs de pollers); Kronos Linux (PID 710524) no rotó en la sesión y queda pendiente de verificación.
- Gates BASELINE y LOAD-BEARING SOURCE INTEGRITY PASS: los 8 archivos Apply blob-idénticos a `2fa17010`, carriers congelados en `1e25640`/`ce21d25`/`5e93c7c`/`8619a50`/`5e3c2b3`, intervalo `2fa17010..1f0880c` sólo chores (`baadc35`, `6d30d0f`, `1f0880c`); foreign dirty `go.work.sum` preservado; estado APPLY_VERIFIED_READS_CORRECTION sigue `CERTIFIED_FOR_FINAL_E2E` y el cierre de Artifact Verified Reads vuelve a quedar `PENDING`.

## Archivos creados/actualizados

- Creada decisión [[2026-08-29-durable-artifact-verified-reads-final-e2e-normal]] y known-error [[2026-08-29-durable-verified-reads-exporter-double-execution]].
- Creado agent run [[2026-08-29-zcode-glm-5-3-flash-durable-verified-reads-final-e2e]] y feedback [[2026-08-29-symphony-worker-observability-session-feedback]].
- Actualizado checkpoint del proyecto [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]] (session checkpoint 2026-08-29 + bitácora + línea de fase) y nota interna [[agents-os-operating-continuity]].

## Decisiones de alcance

- No se crearon L0/L1 (sin transcript persistible ni pedido explícito); no se ejecutó reindex Graphify por deuda de frontmatter preexistente ya documentada.
- La herramienta de diagnóstico read-only creada en `scratch/` durante la sesión fue eliminada al cierre; el worktree queda con `go.work.sum` (foreign), `input/example/config.json` (mutación operacional del intake canónico: bump `example_flow_24` + wave/request_id nuevos) y `deploy/manifest.json` + `deploy/0.2.79/` (salida del release canónico), igual que en los E2E certificados previos.

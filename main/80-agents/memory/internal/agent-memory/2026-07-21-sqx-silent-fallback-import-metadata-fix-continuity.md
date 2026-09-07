---
type: agent_memory
scope: continuity
created: "2026-07-21"
updated: "2026-07-21"
area: symphony
project: "[[Symphony]]"
application: "[[Echo Forge]]"
entities:
  - "[[Symphony]]"
related:
  - "[[2026-07-20-sqx-requestid-traceid-alignment-continuity]]"
aliases: []
confidence: verified
load_policy: active
tags:
  - kind/continuity
  - scope/session
---

# SQX Silent Fallback Import Metadata Fix Continuity

## Estado

- **Fix aplicado**: `project_activity.go` ya no traga errores de `import_metadata` cuando el task es exporter (`overview_exporter`, `wfm_exporter` o `project` con `MetadataExport=true`). Propaga el error original y hace `telemetry.RecordError`.
- **Fallback preservado** para tasks `project` puros (sin `MetadataExport`) — ese path no es crítico para `classify_and_rank`.
- **Tests**: nuevo `TestProjectActivity_Execute_ExporterImportMetadataFailure_PropagatesError` cubre el contrato. Build + `go test ./sqx/...` verde, vet limpio, Graphify reindexado.
- **NO se hizo deploy todavía**. El código está en working tree (sin commit). Confirmar con rjara si quiere bump a v0.1.127 + deploy a Zeus.

## Causa raíz real del workflow `1784605033`

NO fue el bug del fix v0.1.126 (ese estaba bien y se valida con el log: `request_id=cbcd95cb...` propagado correctamente). Fue una cadena distinta:

1. Builder (Event 5) corrió en Zeus, OK.
2. Overview exporter (Event 11) corrió en `sqx-ulab-kron-0` (Kronos) y terminó con `status=ok, output_count=0, sqx_exit_code=0`. El plugin Java no produjo metadata pero no falló.
3. `import_metadata` falló silenciosamente (graceful fallback en `project_activity.go:144-150`).
4. `classify_and_rank` (Event 17) reventó con `ErrMetadataMissing` non-retryable.

## Atención para próxima sesión

1. **Kronos sigue siendo un agujero negro**: no respondió por SSH en `192.168.31.102`. Cualquier `overview_exporter` puede volver a caer ahí y reproducir el mismo patrón. Antes de validar E2E, corroborar estado real de Kronos (vía consola o deployer-watcher) y considerar sacarlo del `task_queue` `sqx-main-queue`.
2. **Bug B no se fixeó en código**: la falta de output del plugin Java no tiene validación adicional (más allá de los chequeos de cardinalidad que ya existen en `ImportMetadataStep.Execute`). Si después del deploy sigue habiendo exporters que terminan con 0 outputs, hay que mirar los `.cfx` y el `sqx_raw_log` del plugin Java, no el código Go.
3. **Si rjara pide deploy**, bumpear `deploy/manifest.json` a v0.1.127 y correr `./deploy_sqx.sh 0.1.127`. Recomendar lanzar primero 1 solo `example_flow_13` y revisar logs antes de paralelizar.
4. **PR potential**: si van a mergear a develop, recordar reglas de PR (Spanish, ≤20 archivos, template, version bump en README).

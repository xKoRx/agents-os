---
type: agent_memory
scope: project
created: 2026-07-15
updated: 2026-09-09
index_priority: never
indexable: false
load_policy: manual
memory_state: archived
tags:
  - kind/agentmemory
  - tech/temporal
  - project/symphony
---

# Continuidad Operativa: Heartbeats en Actividades de Temporal

## Contexto
El usuario solicitó asegurar que todas las actividades del pipeline configuradas bajo `input/example/config.json` inicialicen correctamente el envío de heartbeats periódicos de Temporal (cada 6 segundos). Esto es crítico para prevenir que actividades de larga duración expiren por heartbeat timeouts durante su procesamiento.

## Acciones Tomadas
Se agregaron llamadas a `instrumentation.StartHeartbeat` con intervalo configurado (por defecto 6 segundos) en las siguientes actividades de `sqx/activities/worker/`:

1. `ClassifyAndRankActivity` (`classify_and_rank.go`)
2. `EvaluateWFMActivity` (`evaluate_wfm.go`)
3. `SelectRobustRunActivity` (`robust_activity.go`)
4. `ApplySelectedRunActivity` (`robust_activity.go`)
5. `ExportMT5EAActivity` (`robust_activity.go`)
6. `GenerateReportActivity` (`generate_report.go`)
7. `LoadLogicalTypesActivity` (`load_ranked_types.go`)
8. `ImportMetadataActivity` (`import_metadata.go`)

Todas las actividades fueron modificadas usando `instrumentation.StartHeartbeat(ctx, etcdClient, message)` y deteniendo el ticker usando `defer hb.Stop()`. Las que no poseían el cliente ETCD en su estructura pasaron `nil`, lo cual por defecto realiza fallback a 6 segundos conforme a `sqx/core/instrumentation/heartbeat.go`.

## Estado del Sistema
- La compilación del módulo `sqx` es correcta.
- Pruebas automatizadas en `sqx/activities/worker/...` pasan exitosamente.

---
type: agent_memory
scope: internal
created: "2026-07-12"
updated: "2026-07-12"
load_policy: manual
indexable: false
tags:
  - kind/agent-memory
  - scope/internal
---

# Implementación de Aislamiento por RequestID y Corrección del Builder en Echo Forge

## Contexto y Cambios
En esta sesión se resolvió de raíz la redundancia de subflujos en Echo Forge aplicando los siguientes cambios:

1. **Corrección del Builder (`project_activity.go`)**:
   - Se removió el bloque `startedEmpty` que vaciaba el lote de salida del builder. Ahora se devuelven siempre las llaves generadas. Esto hace que `currentBatch` no esté vacío y el workflow filtre los tipos lógicos de forma correcta (sólo ~45 tipos lógicos en lugar del universo completo de 281).

2. **Aislamiento por `RequestID`**:
   - Se eliminó por completo `BYPASS_RUN_ID` en el adaptador MongoDB y en los scripts de despliegue (`deploy_sqx.sh`).
   - Se propagó de forma explícita el `RequestID` (Tracking ID) en los contratos (`ClassifyRequest`, `LoadLogicalTypesRequest`) y en las firmas de actividades.
   - Las actividades inyectan el `RequestID` en el contexto mediante `contextx.SetRequestID`, garantizando que todas las consultas de MongoDB filtren de manera estricta por `run_id = RequestID`.

3. **Aislamiento en MinIO**:
   - Se introdujo `getStoragePrefix` en `steps.go` para estructurar las rutas de MinIO físicas como `wave_<wave_key>/<request_id>/...` en lugar de la raíz de la ola, logrando separación física total de los archivos generados en ejecuciones paralelas o repetidas de la misma wave.

## Estado del Sistema
- Se compiló y desplegó la versión `0.1.95` del SQX Worker a Zeus. El stager remoto descargó el release y reinició el servicio correctamente.
- Se diagnosticó el fallo "Workflow history size exceeds limit" (52MB) en la corrida `sqx-main-00_configs-v18-NDX-H1-L-1783883763`: se debió a que corrió con la versión `0.1.94` anterior a la corrección del builder, lo que generó 90 subflujos concurrentes de forma redundante y saturó la historia de Temporal.
- Se configuró el cliente de configuración dinámica de Temporal en el servidor `192.168.31.46` creando `/etc/temporal/dynamicconfig.yaml` y vinculándolo en `/etc/temporal/production.yaml`. Los límites de tamaño de historia se incrementaron a:
  - `limit.historySize.error`: 512 MB (antes 50 MB)
  - `limit.historySize.warn`: 256 MB (antes 10 MB)
  - `limit.historyCount.error`: 200,000 (antes 50,000)
  - `limit.historyCount.warn`: 50,000 (antes 10,000)
- Todas las pruebas pasaron exitosamente y el servicio de Temporal fue reiniciado sin problemas.


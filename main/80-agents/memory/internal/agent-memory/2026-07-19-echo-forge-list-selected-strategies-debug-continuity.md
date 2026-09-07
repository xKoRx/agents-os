---
type: agent_memory
scope: session
created: 2026-07-19
updated: 2026-07-19
area: "[[Symphony]]"
project: "[[Echo Forge]]"
application: "[[SQX Worker]]"
entities:
  - "[[SQX Worker]]"
related: []
aliases: []
confidence: verified
source_session: b9bb616a-68b8-4b5a-9c88-8fe504513514
tags:
  - kind/internal-memory
  - scope/session
---

# Echo Forge List Selected Strategies Debug - Continuity

## Estado de la Ejecución y Contexto
- **Última Corrida Evaluada**: `sqx-main-00_configs-v1-NDX-H1-L-1784481761` (Trace ID: `1cb3f6a7cc3d98b8336670a567db0076`).
- **Problema Detectado**: La actividad `list_selected_strategies` en el worker de Zeus retorna `count: 0` debido a que no tiene inyectado el `RequestID` en el contexto Go. El driver de MongoDB de forma predeterminada cae en el fallback del `TraceID` de OpenTelemetry del Span context. Si hay cualquier desajuste o desconexión en la propagación de spans entre Temporal y la actividad, se realiza la consulta a la base de datos con un filtro inválido o vacío.

## Avance de la Sesión
1. **Implementación de Opciones**: Añadimos la opción funcional `WithInput` en `context_envelope.go` e inyectamos correctamente las claves del lote actual `current.Keys` en las peticiones a `NewListSelectedStrategiesRequest` dentro de `generic_workflow.go`.
2. **Build y Despliegue**: Generamos el build local `0.1.121` de Linux/amd64 usando `./deploy_sqx.sh 0.1.121`, actualizamos `manifest.json` y validamos que `deployer-watcher` lo subiera a MinIO.
3. **Actualización Remota**: Ejecutamos el stager en Zeus para forzar la actualización a la `0.1.121` y validamos que el worker se reiniciara y levantara el nuevo binario.
4. **Verificación Directa**: Escribimos el script de testeo `verify_run_id_issue_bin` en Zeus. Al ejecutarlo contra MongoDB, comprobamos que cuando viaja el RequestID, la consulta retorna los 7 registros robustos seleccionados correctamente, pero retorna 0 cuando el contexto del adapter lee el ID vacío o erróneo de la actividad.

## Próximos Pasos (Backlog)
- Corregir el adapter de MongoDB (`getRunID(ctx)`) para que **retorne un error** si `contextx.GetRequestID(ctx)` está vacío, en lugar de recurrir al fallback del `TraceID` de telemetría.
- Hacer que todas las actividades del worker (especialmente `list_selected_strategies`) validen que el `RequestID` no sea vacío al inicio, y aborten/fallen explícitamente en lugar de fallar silenciosamente y continuar con listas vacías.
- Refactorizar `evaluate_wfm` para independizarla por estrategia en tareas de Temporal separadas y optimizar los tiempos de ejecución en paralelo.

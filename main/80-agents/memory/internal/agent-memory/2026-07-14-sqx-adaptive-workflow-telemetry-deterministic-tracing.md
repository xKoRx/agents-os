---
type: agent_memory
scope: project
tags:
  - kind/learning
  - project/symphony
  - area/sqx
created: 2026-07-14
updated: 2026-09-09
index_priority: never
indexable: false
load_policy: manual
memory_state: archived
---

# Continuidad Cognitiva: Telemetría Determinista en SQX Workflows (GAP EF-G09)

En esta sesión se resolvió el GAP EF-G09 que causaba divergencias y caídas durante el replay de los workflows adaptativos debido a la generación no determinista de spans de OpenTelemetry dentro del código de Temporal.

## Contexto y Cambios
1. **Modelos de Entrada Modificados**:
   - Se agregaron campos `Telemetry telemetry.Context` a las estructuras `WaveInput` y `TypeInput` en [contracts.go](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/sqx/core/adaptive/contracts.go) para habilitar la propagación limpia del contexto de tracing.

2. **Eliminación de Helpers No Deterministas**:
   - Se removieron por completo las funciones `startAdaptiveSpan` y `recordAdaptiveError` de [adaptive_workflow.go](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/sqx/workflows/adaptive_workflow.go) ya que utilizaban llamadas no deterministas directas a `telemetry.StartSpan` y `context.Background()`.

3. **Trazado Determinista de Spans**:
   - En `AdaptiveSQXWorkflow`, se utiliza la actividad de Temporal `begin_workflow_span` para registrar el span padre de forma determinista y actualizar el contexto de telemetría si este no cuenta con un `SpanID` válido.
   - En `AdaptiveTypeWorkflow` (child workflow), se registra el span de grupo mediante la actividad `begin_group_span` al inicio de su ejecución.
   - Se propagó el contexto `tctx.Telemetry` a todas las actividades internas y sub-llamadas correspondientes, incluyendo `runBuilderStage`, `verifyMetadata`, `classifyAndRank`, `forkTypeWorkflows`, `processIntakeIteration` y `runProjectStage`.

4. **Registro Seguro de Errores**:
   - Se reemplazaron todas las llamadas a `recordAdaptiveError` con logs deterministas y seguros usando `workflow.GetLogger(ctx).Error(...)` o retornando el error directamente para su captura nativa por Temporal.

5. **Pruebas y Mocks**:
   - Se registraron mocks para `begin_workflow_span` y `begin_group_span` en [adaptive_mocks_test.go](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/sqx/workflows/adaptive_mocks_test.go).
   - Se verificó que todas las pruebas en `./sqx/workflows/...` y lints pasaran de forma exitosa.
   - Se actualizó el índice de Graphify Personal (`graphify-personal update .`).

6. **Propagación en Procesos Batch (echo-lab-worker)**:
   - Se corrigió la pérdida de trazabilidad en los jobs `lab.materialize_lab_strategy_metric_snapshots`, `lab.materialize_lab_equity_curves` y `lab.recompute_strategy_canonical_and_outcomes` ejecutados por `echo-lab-worker`.
   - Se modificaron [main.go](file:///Users/rodrigojara/go/src/github.com/xKoRx/echo/v3/lab-worker/cmd/lab-worker/main.go) y [main.go (lab-materialize-pg)](file:///Users/rodrigojara/go/src/github.com/xKoRx/echo/v3/lab-worker/cmd/lab-materialize-pg/main.go) para extraer el trace context desde la variable de entorno `TRACEPARENT` usando `propagation.TraceContext{}.Extract(...)` al iniciar la ejecución. Esto asocia correctamente las ejecuciones del lab-worker con la traza padre que las gatilló de manera transversal para todos los comandos del CLI.
   - **Despliegue Producción**: Los cambios locales del lab-worker en `v3/lab-worker` fueron compilados localmente usando `./build_v3.sh lab-worker` y desplegados de forma atómica al servidor de producción `192.168.31.71` (donde corren mediante systemd timer/oneshot) ejecutando `./deploy-prod.sh lab-worker`. Adicionalmente, se forzó la ejecución manual del servicio systemd para propagar las trazas.
   - Se validó el build, tests y lints de `lab-worker` y se actualizó el índice de Graphify de `echo`.

7. **Remoción de Spam de Jaeger y Redespliegue del Watcher**:
   - Se eliminó la creación del span de telemetría `"watcher_fsnotify.poll"` en el método `Poll` de [fsnotify_watcher.go](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/sqx/adapters/watcher-fsnotify/fsnotify_watcher.go#L95-L98) para evitar spam de trazas periódicas en Jaeger (cada 3 segundos).
   - **Fuga de Procesos (Mitigación)**: Al cerrar el watcher con `screen -XS watcher quit`, los procesos hijos (como `go run`) y los binarios compilados en segundo plano pueden quedar huérfanos/dangling. Se deben buscar y matar manualmente (`pkill -9 -f ...`) antes de reiniciar el watcher para evitar que el binario antiguo siga reportando a Jaeger.
   - Se empaquetó y compiló el worker para producción en la versión `0.1.120` mediante `./deploy_sqx.sh 0.1.120`.
   - Se actualizó el manifiesto local [deploy/manifest.json](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/deploy/manifest.json) a la versión `0.1.120`, la cual fue detectada y sincronizada a MinIO por el `deployer-watcher`.
   - Se reinició el watcher de archivos en segundo plano en la sesión de `screen` dedicada (`watcher`), validando que inició correctamente y cargó el nuevo código sin instrumentar el span de polling.


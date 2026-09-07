---
type: agent_memory
scope: project
tags:
  - kind/learning
  - project/symphony
  - area/sqx
created: 2026-07-15
updated: 2026-07-15
---

# Continuidad Cognitiva: Resolución GAP EF-G08 - Ajuste de Timeouts en Adaptive Workflow

En esta sesión se resolvió el GAP EF-G08 modificando los timeouts restrictivos de las actividades en el flujo de trabajo adaptativo para soportar de manera robusta tareas de larga duración.

## Contexto y Cambios

1. **Ajuste de Opciones de Actividad**:
   - Se modificó la función [mainActivityOptions()](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/sqx/workflows/adaptive_workflow.go#L550-L560) en `sqx/workflows/adaptive_workflow.go`.
   - Se reemplazaron los límites restrictivos previos (10 min de ejecución y 15 min de schedule) por los siguientes parámetros de mejores prácticas de Temporal:
     - `HeartbeatTimeout`: Establecido en 2 minutos para permitir la detección rápida de caídas del worker (fallos en ejecución del Builder que pueden durar hasta 2 días).
     - `StartToCloseTimeout`: Incrementado a 5 días (`5 * 24 * time.Hour`) para proporcionar una ventana segura y suficiente a campañas de generación largas.
     - `ScheduleToCloseTimeout`: Incrementado a 10 días (`10 * 24 * time.Hour`) para considerar esperas en cola de tareas y ejecución completa.
     - `WaitForCancellation`: Establecido en `true` para asegurar que las tareas liberen recursos y limpien sus directorios locales ordenadamente en cancelaciones.
     - `RetryPolicy`: Modificado para permitir reintentos infinitos (`MaximumAttempts: 0`) con backoff exponencial e intervalo inicial de 1 minuto hasta un máximo de 30 minutos, protegiendo contra errores transitorios de disco o red.

2. **Impacto en Colas Adicionales**:
   - La función `withMT5Queue` hereda estos nuevos límites y políticas globales, manteniendo únicamente el override específico de la cola de tareas (`TaskQueue: adaptive.QueueMT5`), asegurando consistencia y robustez en la ejecución de backtests de MetaTrader 5.

3. **Verificación Técnica**:
   - `go vet ./sqx/workflows/...` se ejecutó de forma limpia.
   - `go test -count=1 ./sqx/workflows/...` pasó exitosamente sin fallos.
   - Se actualizó el índice de Graphify Personal (`graphify-personal update .`).

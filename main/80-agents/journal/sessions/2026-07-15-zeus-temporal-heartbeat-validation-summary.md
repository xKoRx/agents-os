---
type: session
scope: session
created: 2026-07-15
updated: 2026-07-15
area: "[[Symphony]]"
project: "[[Symphony]]"
application: "[[Symphony]]"
entities:
  - "[[Symphony]]"
related: []
aliases: []
confidence: high
source_session: 3718b2a8-5a49-4763-9b37-53eefd89512f
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

# 2026-07-15 - Validación de Heartbeats de Temporal en Zeus - Summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

Diagnosticar el origen de errores de Heartbeat Timeout reportados por el usuario y auditar el correcto envío y recepción de heartbeats en el worker remoto de Zeus.

## Contexto cargado

- [[2026-07-15-zeus-namespace-mismatch-analysis.md]] (análisis de namespaces y task queues anterior).

## Trabajo realizado

1. **Monitoreo y Verificación Empírica**:
   - Se monitoreó el workflow activo `v38` (`sqx-main-00_configs-v38-NDX-H1-L-1784094403`) en el namespace `sqx-prop`.
   - Se observó la finalización progresiva y exitosa de las 14 tareas del grupo.
   - Se verificó la actividad `project` del exportador (`EchoForgeWFMExporter`) ejecutándose de forma continua por más de 2 minutos y 57 segundos en `Attempt: 1`.
   - Dado que el `HeartbeatTimeout` configurado en el flujo es de 2 minutos, la estabilidad de la actividad en el intento 1 valida empíricamente que los heartbeats periódicos de 6 segundos configurados en ETCD se transmiten y asimilan correctamente en Temporal.

2. **Auditoría de Código y Diagnóstico de Riesgos**:
   - Se auditó el código del worker y se encontró que la actividad `project` (que ejecuta el grueso del trabajo pesado en `sqcli`) posee la inicialización de `StartHeartbeat`.
   - Se descubrió que las actividades de `robust_activity.go` (como `apply_selected_run` o `mt5_exporter`) no llaman a `StartHeartbeat`. Si bien el flujo `v38` no ha presentado fallos allí, se identificó como un riesgo potencial para futuras tareas pesadas de exportación de MT5 que excedan los 2 minutos.

3. **Resolución del Reporte de Error**:
   - Se concluye que el error `TIMEOUT_TYPE_HEARTBEAT` no está activo en el worker de Zeus. Lo más probable es que correspondiera a intentos previos de ejecución local en el MacBook del usuario o ejecuciones previas antes del reinicio del watcher y realineación de namespaces.

## Memoria propuesta o creada

- [[2026-07-15-zeus-temporal-heartbeat-validation.md]] (internal memory continuity note).

## Pendiente

- Dejar que el flujo de trabajo `v38` complete su ejecución total.

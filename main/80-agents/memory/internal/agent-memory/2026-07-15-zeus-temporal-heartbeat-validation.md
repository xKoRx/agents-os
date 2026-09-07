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

# Continuidad Cognitiva: Validación de Heartbeats de Temporal en Zeus

En esta sub-sesión se auditó y validó el estado de los heartbeats en el worker de Zeus para descartar fallos de timeout de heartbeat.

## Hallazgos y Diagnóstico

1. **Estado de Ejecución Actual**:
   - Se validaron las ejecuciones activas de `v38` en el namespace `sqx-prop`.
   - Todas las 14 tareas hijas del grupo se completaron con éxito de forma rápida.
   - La tarea de exportación `EchoForgeWFMExporter` (ejecutada mediante la actividad `project` en el parent workflow) se ejecutó durante más de 2 minutos y 57 segundos, manteniéndose estable en `Attempt: 1`.
   - Como el `HeartbeatTimeout` está configurado a `2 * time.Minute`, esto confirma de manera empírica que el goroutine de heartbeat (`StartHeartbeat` con frecuencia de 6s obtenida de ETCD) está transmitiendo heartbeats de forma correcta al clúster de Temporal.

2. **Auditoría de Código y Posibles Riesgos Futuros**:
   - Las actividades que ejecutan comandos de larga duración en `generic_workflow.go` usan la actividad `project`, la cual posee `StartHeartbeat` integrado.
   - Las actividades en `robust_activity.go` (como `apply_selected_run` y `mt5_exporter` que llaman a `sqcli` para exportaciones pesadas) **no** invocan a `StartHeartbeat`.
   - Aunque no se detectaron fallos activos en esta ejecución de `v38` (completó la exportación y el pipeline sigue sano), si en el futuro alguna actividad de `robust_activity` excede los 2 minutos, podría fallar por `HeartbeatTimeout`.

3. **Origen del Error del Usuario**:
   - El mensaje `TIMEOUT_TYPE_HEARTBEAT` no se originó en el worker de Zeus durante este flujo de trabajo. Pudo haber sido provocado por ejecuciones locales huérfanas en el MacBook del usuario o ejecuciones previas antes del reinicio y realineación de namespaces.

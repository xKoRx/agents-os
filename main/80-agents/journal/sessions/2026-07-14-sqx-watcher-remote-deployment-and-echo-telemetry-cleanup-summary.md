---
type: session
scope: session
created: 2026-07-14
updated: 2026-07-14
area: "[[Symphony]]"
project: "[[Symphony]]"
application: "[[Symphony]]"
entities:
  - "[[Symphony]]"
  - "[[Echo]]"
related: []
aliases: []
confidence: high
source_session: db9fa999-41f5-48df-acdc-68aeccd5701d
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

# 2026-07-14 - Despliegue Remoto de sqx-watcher y Limpieza de Telemetría en Echo - Summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

Desplegar `sqx-watcher` de forma remota y automatizada en la VM **Zeus** (`192.168.31.101`) y silenciar los spans de OpenTelemetry redundantes en `echo-lab-worker` (`192.168.31.71`).

## Contexto cargado

- [[symphony-zeus-troubleshooting.md]] (credenciales y direccionamiento IP).
- [implementation_plan.md](file:///Users/rodrigojara/.gemini/antigravity/brain/db9fa999-41f5-48df-acdc-68aeccd5701d/implementation_plan.md) (plan de despliegue).

## Trabajo realizado

1. **Compilación e Integración**:
   - Modificado [deploy_sqx.sh](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/deploy_sqx.sh) para compilar el watcher junto con el worker.
   - Modificado [deploy/manifest.json](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/deploy/manifest.json) para incluir el artefacto del watcher.
2. **Auto-Upgrade del Watcher**:
   - Implementado en `sqx-watcher` ([main.go](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/sqx/cmd/sqx-watcher/main.go)) un loop de verificación que cierra el proceso si el symlink `/opt/symphony/current` se actualiza.
3. **Aprovisionamiento Remoto (Zeus)**:
   - Modificado `/usr/local/sbin/symphony-stager` en Zeus para descargar el binario `sqx-watcher`.
   - Creado y habilitado el servicio `/etc/systemd/system/symphony-watcher.service`.
4. **Validación E2E y Corrección de Carreras de E/S**:
   - Detectado fallo temporal de E/S (`unexpected end of JSON input`) por la escritura asíncrona de `scp`.
   - Modificado [steps.go](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/sqx/activities/watcher/steps.go) agregando un loop de reintentos con backoff al leer el JSON principal.
   - Validado E2E enviando un flujo completo que inició exitosamente en Temporal.
5. **Silenciado de Spans en Echo**:
   - Comentados los spans raíz de OpenTelemetry en `echo-lab-worker` (`materialize_curves.go`, `materialize_snapshots.go`, `recompute.go`) ya que corresponden a tareas systemd programadas (cron) y solo generaban ruido en Jaeger.
   - Recompilado y desplegado de forma atómica a `192.168.31.71` usando `./deploy-prod.sh lab-worker`.
6. **Grafos de Conocimiento**:
   - Ejecutado `graphify-personal update .` en los repositorios de `symphony` y `echo`.

## Artifacts creados o modificados

- [deploy_sqx.sh](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/deploy_sqx.sh) (compila watcher).
- [main.go](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/sqx/cmd/sqx-watcher/main.go) (detección de auto-upgrade).
- [steps.go](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/sqx/activities/watcher/steps.go) (reintentos en validate_spec).
- [manifest.json](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/deploy/manifest.json) (versión 0.1.122).
- `/usr/local/sbin/symphony-stager` y `/etc/systemd/system/symphony-watcher.service` (remotos en Zeus).
- `materialize_snapshots.go`, `materialize_curves.go`, `recompute.go` (comentados los spans raíz en `echo`).

## Memoria propuesta o creada

- [[2026-07-15-sqx-watcher-remote-deployment.md]] (internal memory continuity note).

## Decisiones

- **Desactivar telemetría de cron jobs**: Las ejecuciones recurrentes de base de datos no aportan valor en Jaeger y ensucian el timeline global, por lo que se comentaron sus spans y timers, manteniendo la telemetría solo para flujos interactivos o iniciados con un parent `TRACEPARENT`.

## Pendiente

- Monitorear Jaeger para verificar la total ausencia de spans aislados de `echo-lab-worker` en ejecuciones programadas automáticas subsiguientes.

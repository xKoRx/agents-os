---
type: session
scope: session
created: 2026-06-27
updated: 2026-06-27
area: "[[Personal]]"
project: "[[Symphony]]"
application: "[[Echo Forge]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[2026-06-27-echo-forge-retester-concurrency-failure-raw]]"
aliases: []
confidence: high
source_session: 4af42ce7-35ef-4f46-9445-a0a05872312a
load_policy: manual
indexable: false
index_priority: never
tags:
  - app/echo-forge
  - app/echoforge
  - area/personal
  - kind/session
  - project/symphony
  - scope/session
---
# 2026-06-27 - Echo Forge Retester Concurrency Failure - Summary

> [!info]+ Session summary L1
> Resumen operativo de la resolución de la falla del Retester en el pipeline adaptativo.

## Objetivo

- Diagnosticar y corregir la falla recurrente en el paso `02_retester_full` de Echo Forge en el worker Zeus.

## Contexto cargado

- Monorepo Symphony (módulo `symphony/sqx`).
- Base de datos Postgres (`postgres_echo_prod_readonly`) y bases de datos MongoDB (`forge`).
- Historial de workflows en Temporal.

## Trabajo realizado

- Identificación del problema: Múltiples child-workflows ejecutan actividades de `project` en paralelo para diferentes tipos lógicos en la misma VM. Como todos comparten la misma ruta local `/home/kor/sqx/user/projects/02_retester_full`, se produce una condición de carrera (race condition) donde limpian y sobrescriben el disco simultáneamente, rompiendo la ejecución de `sqcli`.
- Implementación de la solución:
  - Modificación en `sqx/activities/worker/pipeline/step.go`: Se añade el método `GetProjectName()` al objeto `State` para construir dinámicamente un nombre de proyecto local único concatenando el tipo lógico sanitizado de la tarea (`st.Task.Source.LogicalType`) si está disponible.
  - Modificación en `sqx/activities/worker/steps/steps.go`: Se delega la función local `getProjectName` a `st.GetProjectName()`.
  - Modificación en `sqx/activities/worker/pipeline/hooks/cleanup_databanks.go`: Se utiliza `st.GetProjectName()` en lugar de lógica local no-concurrente para limpiar directorios de manera aislada en disco.
- Despliegue y verificación:
  - Se corrieron los tests unitarios (`go test ./sqx/...`) de forma exitosa.
  - Se compiló y generó la release `0.1.24` localmente mediante `./deploy_sqx.sh 0.1.24`.
  - Se actualizó el manifiesto `deploy/manifest.json` y el deployer sincronizó los binarios con MinIO.
  - Se reinició el servicio del worker Zeus (`symphony-worker.service`) constatando su reactivación exitosa con la versión `0.1.24` en ejecución.

## Artifacts creados o modificados

- [step.go](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/activities/worker/pipeline/step.go) (Modificado)
- [steps.go](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/activities/worker/steps/steps.go) (Modificado)
- [cleanup_databanks.go](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/activities/worker/pipeline/hooks/cleanup_databanks.go) (Modificado)
- [manifest.json](file:///Users/rjara/go/src/github.com/xKoRx/symphony/deploy/manifest.json) (Modificado)

## Memoria propuesta o creada

- Ninguna nueva L3 o ADR fue necesaria, ya que se trató de una corrección técnica de regresión (bug fix) de la lógica existente de aislamiento físico.

## Decisiones

- Aislar los directorios locales del disco del worker basándonos en el tipo lógico sin cambiar las rutas lógicas/prefijos en MinIO, de manera que no se rompan las dependencias físicas entre etapas de la wave.

## Pendiente

- Monitorear las ejecuciones subsiguientes en Temporal para verificar que el pipeline complete la fase de admisión adaptativa sin colisiones físicas.

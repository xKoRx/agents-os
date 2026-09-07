---
type: session
scope: session
created: "2026-07-13"
updated: "2026-07-13"
area: "[[Symphony]]"
project: "[[Symphony Portal]]"
application: "[[Symphony]]"
entities:
  - "[[Symphony]]"
related: []
aliases: []
confidence: high
source_session: "593d3469-39c8-4712-a3ac-f56e47665073"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

# Continuidad Operativa: Corrección de Duplicación de Prefijo en apply_selected_run

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Diagnosticar y solucionar error de descarga de estrategia en la actividad `apply_selected_run` de la ejecución de robust run en Symphony.
- Levantar el watcher, deployer y desplegar la versión corregida.

## Contexto cargado

- Leído `agents-os.md` y perfil de usuario.
- Analizada la actividad `ApplySelectedRunActivity.Execute` en `robust_activity.go` y su respectiva prueba `robust_activity_test.go`.

## Trabajo realizado

- **Corrección de Prefijo Duplicado:** Se implementó una lógica de coincidencia flexible en `robust_activity.go` para usar directamente `base.sqx` si `StrategyID` ya incluye instrumento/timeframe.
- **Búsqueda Dinámica con Fallback:** Si falla la descarga directa de la estrategia en MinIO, se listan los objetos del directorio padre para buscar dinámicamente un archivo `.sqx` que contenga el `StrategyID` en su nombre de archivo (resolviendo prefijos como `WF_Matrix_-_` que surgen por `UploadPrefixFilters`).
- **Control de Entornos:** Se modificaron `run_watcher.sh` y `run_deployer.sh` para restaurar la variable `ENV` y evitar que el archivo `.env` local anulara el entorno `production` forzado por línea de comandos.
- **Reinicio Limpio:** Se eliminaron procesos de Go huérfanos (`go-build` daemons) que competían por los archivos en `input/`, y se iniciaron limpiamente las sesiones de screen del watcher y deployer en modo `production` (namespace `sqx-prop` de Temporal).
- **Despliegue exitoso:** Se compiló y desplegó la versión **`0.1.116`** de Symphony, la cual fue tomada de forma inmediata por el worker de Zeus.

## Artifacts creados o modificados

- [robust_activity.go](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/sqx/activities/worker/robust_activity.go) (modificado)
- [robust_activity_test.go](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/sqx/activities/worker/robust_activity_test.go) (modificado)
- [run_watcher.sh](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/run_watcher.sh) (modificado)
- [run_deployer.sh](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/run_deployer.sh) (modificado)
- [deploy/manifest.json](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/deploy/manifest.json) (modificado, actualizado a `0.1.116`)

## Memoria propuesta o creada

- Memoria de continuidad interna en [2026-07-13-apply-selected-run-prefix-duplication-fix.md](file:///Users/rodrigojara/obsidian/SecondBrain/main/80-agents/memory/internal/agent-memory/2026-07-13-apply-selected-run-prefix-duplication-fix.md)
- Feedback de sesión en [2026-07-13-apply-selected-run-prefix-duplication-fix-feedback.md](file:///Users/rodrigojara/obsidian/SecondBrain/main/80-agents/journal/feedback/system-1/2026-07-13-apply-selected-run-prefix-duplication-fix-feedback.md)

## Decisiones

- Incorporar listado dinámico de MinIO en la descarga de estrategias para blindar el pipeline ante prefijos añadidos en tareas intermedias.

## Pendiente

- Esperar finalización del flujo v28 y validar la generación del EA.
- Refactorizar para separar la exportación de MT5 EA en una tarea explícita (`mt5_exporter`) en lugar de mantenerla camuflada en la actividad de robust run.

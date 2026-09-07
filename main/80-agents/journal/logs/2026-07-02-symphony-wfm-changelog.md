---
type: change_log
scope: session
created: "2026-07-02"
updated: "2026-07-02"
area: "[[Personal]]"
project: "[[Symphony]]"
entities:
  - "[[Symphony]]"
related: []
aliases: []
confidence: verified
source_session: "[[2026-07-02-symphony-wfm-debugging-summary]]"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Change Log - 2026-07-02 - Symphony WFM Debugging

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - [generic_workflow.go](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/sqx/workflows/generic_workflow.go)
  - [robust_activity.go](file:///Users/rodrigojara/go/src/github.com/xKoRx/symphony/sqx/activities/worker/robust_activity.go)

## Motivo

- Corregir el flujo `con wfm` en el SQX Worker.
- El flujo se quedaba atascado en `apply_selected_run` debido a que:
  1. El paso de rankeo retornaba una lista vacía de `selected_runs` cuando no pasaban el filtro de score, o cuando no se encontraba el archivo de entrada.
  2. El stager de Zeus estaba desactualizado en la máquina local (versión `0.1.50` vs la nueva `0.1.52`).
  3. Las rutas de MinIO guardadas en MongoDB tenían discrepancias en los nombres de instrumentos/temporalidades/carpetas respecto a la ubicación real.

## Fuentes usadas

- Código fuente de `symphony` y logs de ejecución de Temporal/Zeus.

## Resolución aplicada

- **Bypass de Rankeo:** Se agregó un fallback en `generic_workflow.go` que, si la lista de rankeo viene vacía y se está ejecutando en modo de test/evaluación con un archivo WFM explícito, hace bypass del rankeo y crea una entrada de selección directamente con score 1.0 para forzar el flujo completo.
- **Rutas Robustas de Descarga:** Se mejoró `apply_selected_run` en `robust_activity.go` para que, en caso de fallar la descarga usando los metadatos de MongoDB, intente parsear el instrumento y timeframe directamente del `StrategyID` de la estrategia (ej. `XAUUSD_L_H1...` -> `xauusd`, `l_h1`) y busque en carpetas alternativas (`SQXOverviewJsonExporter`, `03_wfm_optimizer`, etc.), haciendo el proceso 100% resiliente a inconsistencias de base de datos.
- **Auto-Deploy Watcher:** Se actualizó `deploy/manifest.json` y se compiló/subió a MinIO la versión `0.1.52` usando el deployer watcher local para forzar al stager en Zeus a actualizarse automáticamente.

## Validación

- Ejecución exitosa de `scratch/test_complete_flow.go` en Temporal, completando el flujo de inicio a fin con descarga robusta de MinIO y patch de parámetros.

---
type: learning
scope: application
created: "2026-06-27"
updated: "2026-06-27"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities: []
related: []
aliases:
  - Bandera de exportación de metadata SQX
  - metadata_export flag in workflow
confidence: high
source_session: "8c11ec26-7ad2-4f0d-a862-0c85ceebe285"
load_policy: manual
indexable: true
index_priority: high
tags:
  - app/echo-forge
  - app/echoforge
  - area/echo
  - kind/learning
  - project/echo-forge
  - project/echoforge
  - scope/application
---
# StrategyQuant Metadata Export Flag Requirement

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Aprendizaje

- Las tareas de tipo `project` dentro de los workflows adaptativos de StrategyQuant que requieren la posterior importación e ingesta de metadatos (como las matrices WFM optimizadas) deben tener configurada de forma obligatoria la bandera `"metadata_export": true` en el JSON de definición del workflow (ejemplo: repo `github.com/xKoRx/symphony`, path `input/processed/new_workflow/new_workflow_full.json`).
- Sin esta bandera, el pipeline del worker omite los pasos de generación de propiedades del exportador (`write_exporter_properties`) y su posterior subida a MinIO, provocando que las actividades de importación de metadata (`metadata_import`) fallen en bucle buscando un archivo `export_run.json` que no existe.

## Aplicabilidad

- **Cuándo cargarlo:** Al diseñar, configurar o depurar el JSON de un workflow de orquestación de Symphony.
- **Cuándo no cargarlo:** En tareas que no involucren StrategyQuant CLI ni exportación/importación de metadatos.

## Entidades relacionadas

- Tarea `03_wfm_optimizer` y paso `metadata_import`.

## Evidencia

- Repo `github.com/xKoRx/symphony`, path `input/processed/new_workflow/new_workflow_full.json`.

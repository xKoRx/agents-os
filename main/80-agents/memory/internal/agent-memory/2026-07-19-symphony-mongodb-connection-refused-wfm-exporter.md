---
type: agent_memory
schema_version: 1
scope: project
created: 2026-07-19
updated: 2026-09-09
memory_state: archived
area: "[[Personal]]"
project: "[[symphony]]"
load_policy: manual
indexable: false
index_priority: never
tags:
  - agent/internal
  - kind/agent-memory
  - project/symphony
  - scope/project
---

# Symphony MongoDB Connection Refused in WFM Exporter

## Continuidad
- The user ran `example_flow_4` configuration (`20260719_152300_config.json`) which generated and optimized strategies.
- The `wfm_exporter` task completed successfully, but under the hood, the `import_metadata` step failed to save WFM matrices into MongoDB because of a transient `connection refused` error at `192.168.31.221:27017` from Zeus.
- Because of the graceful fallback policy in CHANGE-002, the `wfm_exporter` task did not abort the workflow.
- However, when the workflow reached the `evaluate_wfm` task, it tried to query the matrices from MongoDB. Since the matrices were never imported, it failed with `wfm matrix not found` and retried indefinitely, causing zombie workflows.

## Actions taken
1. Inspected running/active workflows in Temporal and terminated the zombie/stuck `example_flow_4` workflow.
2. Verified MongoDB status and verified that connectivity is now working properly.
3. Created a Go script (`scratch/import_my_failed_run.go`) to download `wfm_matrices.ndjson` and `export_run.json` from MinIO under prefix `wave_test/ndx/l_h1/example_flow_4/v1/7b943490d6511d29b0b751165d4ca046/metadata` and import them manually to MongoDB with the correct `RunID`.
4. Successfully completed the manual import. Verified that the matrices are now queryable in MongoDB.

## Señales de carga

- Cargar sólo para [[symphony]] cuando aparezcan `connection refused`, matrices WFM ausentes después de exportar o retries persistentes de `evaluate_wfm`.

## Próxima acción

- Confirmar primero si el error vigente coincide con esta cadena causal antes de aplicar cualquier recuperación.

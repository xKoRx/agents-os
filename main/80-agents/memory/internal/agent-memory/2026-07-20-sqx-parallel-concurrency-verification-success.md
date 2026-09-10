---
type: agent_memory
schema_version: 1
scope: project
created: 2026-07-20
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

# Symphony Parallel Concurrency Verification Success

## Continuidad
- The user requested executing at least three workflows concurrently to verify that the WFM metadata collision fix (release `0.1.125`) is robust and does not crash or corrupt database entries.
- We analyzed the origin of the legacy "14 runs matrix residue" and found it stems from StrategyQuant's internal databank cache of the shared project folder (`custom`), which is not cleared between different runs.
- When exporting, the SQX exporter plugin outputs both the active run's strategies and the residual legacy strategies into the same `wfm_matrices.ndjson` file.
- The new Go parser fix (release `0.1.125`) resolves this by scoring the strategies based on name matching and discarding the lower-scoring legacy residues before saving to MongoDB.

## Actions taken
1. Triggered Flows 9, 10, and 11 concurrently (`example_flow_9`, `example_flow_10`, `example_flow_11`).
2. Resolved potential Temporal Workflow ID collisions by introducing a 3-second delay copy timestamp when launching the flows.
3. Recursively updated nested config references in parallel runs via `prepare_parallel.go` to prevent template file sharing conflicts.
4. Monitored the concurrent executions to completion. All three workflows completed with status `Completed` on the `sqx-prop` Namespace.
5. Inspected MongoDB collections `selected_robust_runs` for all three flows. Verified that they contain only valid, configured run counts (6 to 9 runs) and no 14-run residue entries whatsoever.
6. Cleaned up scratch scripts and debris from the repository workspace to maintain a clean git state.

## Señales de carga

- Cargar sólo al trabajar con [[symphony]] sobre concurrencia, residuos WFM o la release histórica `0.1.125`.

## Próxima acción

- Tratar la corrida como evidencia histórica y volver a verificar el comportamiento en el source vigente.

---
type: agent_memory
scope: internal
created: 2026-07-31
updated: 2026-07-31
area: "[[Echo]]"
project: "[[Echo Forge - Trade List Export Contrato Remoto]]"
entities:
  - "[[ExportTradeListActivity]]"
  - "[[EchoForgeTradeListExporter]]"
related:
  - "[[trade-list-exporter-local-path-cross-worker]]"
  - "[[2026-07-31-temporal-activity-contract-remote-only]]"
confidence: high
load_policy: when_entity_loaded
indexable: false
index_priority: never
tags:
  - kind/agentmemory
  - agent/internal
  - project/echo-forge
---

# Continuidad — rediseño trade_list export/upsert (sin paths locales)

- Problema canónico: [[trade-list-exporter-local-path-cross-worker]]. Diseño
  cerrado el 2026-07-31 en opción A (activity única). Regla generalizada en
  [[2026-07-31-temporal-activity-contract-remote-only]].
- Planificador único del trabajo: [[Echo Forge - Trade List Export Contrato Remoto]]
  (T1-T8, archivos permitidos por tarea). Gap `EF-G32` §10.9 del `G6_HANDOFF`.
- Estado: **cero código escrito**. Lo siguiente es que un agente ligero ejecute
  T1 en adelante; no re-diseñar ni re-auditar, la nota ya trae archivo y línea.
- **Corrección de rumbo del owner (misma noche).** Rechazó dos decisiones mías y
  tenía razón en ambas; quedaron revertidas:
  - La key MinIO ya **no** es `waves/.../requests/<request_id>/runs/<run_id>/.../trades.v1.ndjson.gz`
    sino `<folder de la task>/<canonical_strategy_id>.trades.ndjson.gz` vía
    `BuildMinIOPath`. Yo la defendí por costo de migración e ignoré que el repo
    **ya tenía firmada** la decisión EF-G27 (`paths.go` L8-27: mecanismo único,
    sin segmentos de ejecución, y nombra a `trade_list_exporter`). Lección: antes
    de defender el statu quo, buscar si existe una decisión previa que lo
    prohíba.
  - Los directorios locales son solo `databanks/input` y `databanks/output`, con
    limpieza antes y después. Mi objeción ("`CleanProjectDatabanks` podría borrar
    a mitad de vuelo") era falsa: `MaxConcurrentActivityExecutionSize: 1`
    serializa las activities, y el riesgo real era el que él señaló (un dir que
    nadie limpia contamina las tasks siguientes).
- Decisiones que NO deben reabrirse sin motivo nuevo: gzip se mantiene (cambia el
  nombre, no los bytes); trades no van a Mongo; el pipeline legacy de 4 steps
  **sí** se borra (D11); la key la construye el caller y el adapter la recibe
  (D12); no hay `_SUCCESS` remoto (D13); el recibo de publicación (EF-G33) queda
  diseñado y fuera de alcance.
- Reglas nuevas publicadas: extensión de
  [[2026-07-31-storage-path-deterministic-by-logical-identity]] (naming del trade
  list + "un adapter no construye rutas") y
  [[2026-07-31-task-local-dirs-input-output-only]].
- Ojo con el efecto colateral querido: al cerrar el skip de `trade_count == 0`
  el pipeline fallará ruidosamente en `06_trade_list` mientras EF-G28 esté
  abierto. Es intencional; si rjara lo reporta como regresión, explicar antes de
  revertir.
- Fricción menor recurrente: `graphify-personal query` sobre el repo `symphony`
  devolvió ruido para trade list (archivos nuevos/untracked no están en el
  grafo). Aplicar la regla de rechazar el resultado y buscar enfocado; no gastar
  turnos reintentando el grafo.

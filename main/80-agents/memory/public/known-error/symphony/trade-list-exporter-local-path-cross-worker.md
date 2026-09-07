---
type: known_error
scope: application
created: "2026-07-31"
updated: "2026-07-31"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
application: "[[sqx-worker]]"
entities:
  - "[[StrategyQuant X]]"
  - "[[Symphony]]"
  - "[[MinIO]]"
  - "[[MongoDB]]"
related:
  - "[[2026-07-26-trade-list-package-complete-and-nonretryable]]"
  - "[[trade-list-exporter-minio-prefix-mismatch-robust-sqx]]"
aliases:
  - trade_list_exporter local path affinity
  - act_upsert_trade_list wrong worker
  - NDJSONPath cross-host
confidence: high
source_session: "2026-07-31-trade-list-upsert-affinity"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - app/sqx-worker
  - area/echo
  - kind/knownerror
  - project/echo-forge
  - scope/application
  - tech/temporal
  - tech/minio
---

# Trade List — `trade_list_exporter` deja paths locales; `act_upsert_trade_list` puede correr en otro worker

> El workflow parte el flujo en dos activities Temporal sin sticky/affinity.
> `trade_list_exporter` escribe `trades.ndjson.gz` + manifest en disco del
> worker A y devuelve `NDJSONPath` local. Luego el workflow llama
> `act_upsert_trade_list(scope, manifest, ndPath)`, que puede schedularse
> en worker B (sin ese archivo). Violación del invariante: cada activity
> debe ser autosuficiente; no puede depender de estado local de otra.

## Síntoma

- Tras `trade_list_exporter` OK, `act_upsert_trade_list` falla al leer
  `ndPath` (archivo inexistente) o errores de firma Temporal
  (`expects exactly 1 argument, got 3` si hay skew de binarios).
- Cluster multi-worker (Zeus/Hera/Kronos) en la misma task queue.

## Causa

- Split export → upsert pasa rutas de filesystem entre activities.
- Temporal no garantiza el mismo host para activities consecutivas
  sin session/sticky queue.

## Fix (diseño cerrado 2026-07-31, pendiente de implementar)

- **Una sola activity**: `trade_list_exporter` exporta, sube el paquete a MinIO y
  upsertea el manifest en Mongo antes de retornar. `act_upsert_trade_list`,
  `actUpsertTradeList` y `ProjectActivity.UpsertTradeList` se retiran.
- Output solo con identificadores remotos (`scope`, `artifact_key`,
  `artifact_sha256`, tamaños, `trade_count`). Prohibido cualquier campo de
  filesystem; se verifica con un test de reflexión.
- Descartado sticky/session: ataría el pipeline a la topología del cluster.
- Regla generalizada: [[2026-07-31-temporal-activity-contract-remote-only]].
- **Se arreglan en el mismo PR dos incumplimientos adyacentes** descubiertos al
  revisar el diseño:
  - La key MinIO del trade list ignoraba EF-G27 (metía
    `requests/<request_id>/runs/<run_id>`). Pasa a
    `<folder de la task>/<canonical_strategy_id>.trades.ndjson.gz` vía
    `BuildMinIOPath`. Ver extensión en
    [[2026-07-31-storage-path-deterministic-by-logical-identity]].
  - El exporter escribía en un tercer directorio local que nadie limpiaba. Pasa a
    `databanks/output`, con limpieza antes y después. Ver
    [[2026-07-31-task-local-dirs-input-output-only]].
- Plan T1-T8: [[Echo Forge - Trade List Export Contrato Remoto]] · gap `EF-G32`
  en `specs/FEAT-SQX-STRATEGY-EVALUATION/G6_HANDOFF.md` §10.9.

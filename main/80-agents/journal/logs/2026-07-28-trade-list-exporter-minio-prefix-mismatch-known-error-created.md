---
type: change_log
scope: session
created: "2026-07-28"
updated: "2026-07-28"
project: "[[Echo Forge - Cierre de Etapa 4]]"
entities:
  - "[[Symphony]]"
  - "[[sqx-worker]]"
  - "[[Echo Forge]]"
related:
  - "[[trade-list-exporter-minio-prefix-mismatch-robust-sqx]]"
aliases: []
confidence: verified
source_session: "2026-07-28-echo-forge-trade-list-exporter-mismatch"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - project/echo-forge
  - change/created
---

# Change Log — 2026-07-28 — KE `trade-list-exporter-minio-prefix-mismatch-robust-sqx` creado

## Resumen

Se identifica y documenta un nuevo Known Error en Symphony: el activity
`trade_list_exporter` busca el `.sqx` robusto bajo el prefijo plano
`output/robust/`, mientras que `04_optimizer_robust` lo está subiendo bajo
`wave_test/<instr>/<dir>/<strat>/<ver>/<trace>/04_optimizer_robust/`. El
mismatch hace que el exporter falle en los 4 reintentos con
`failed to stat object sqx-strategies/output/robust/...: The specified key does not exist.`

## Hechos verificados

- Worker en Zeus ejecutó `0.2.1` (patch sobre `0.2.0`) y versionado
  correcto del `config.json` para `example_flow_38`.
- Las fases `01_builder`, `02_retester`, `03_optimizer` y
  `04_optimizer_robust` corrieron sin error y subieron `.sqx` a MinIO.
- `mc ls -r minio-worker/sqx-strategies/` confirma los `.sqx` robustos en
  `wave_test/.../<trace>/04_optimizer_robust/` y la ausencia total de
  claves bajo `output/robust/`.
- El `RobustRunSetup` se persiste con `TargetStrategyArtifact =
  output/robust/<id>_robust.sqx` (en
  `sqx/activities/worker/robust_activity.go:285`), key plana que
  `trade_list_exporter` consume como `sourceKey` en
  `sqx/activities/worker/trade_list_exporter_activity.go:198`.

## Resolución aplicada

- Se crea el KE `trade-list-exporter-minio-prefix-mismatch-robust-sqx`
  en `80-agents/memory/public/known-error/symphony/` con síntoma,
  causa raíz, evidencia y mitigaciones operativa y duradera.
- No se modifica código de Symphony por instrucción explícita del
  usuario ("encuentra el problema, no lo arregles").
- El KE queda enlazado a la decisión
  `2026-07-27-trade-list-exporter-type-internal-project-mapping` y al
  skill `echo-forge-testing` para que la futura cobertura E2E de
  `trade_list_exporter` incluya este escenario.

## Validación

- El KE fue inferido desde logs de worker (`/var/log/symphony/symphony-worker.log`)
  cruzados con `mc ls -r` del bucket `sqx-strategies` y revisión del
  código en `sqx/activities/worker/robust_activity.go` y
  `sqx/activities/worker/trade_list_exporter_activity.go`.
- La confianza del KE queda en `high` (evidencia reproducible al primer
  intento y patrón de error consistente en los 4 reintentos).
- Se ejecuta reindex dirigido de Graphify para `symphony` tras crear el
  KE, de modo que el grafo refleje el nuevo nodo y su relación con
  `MinIO` y `Echo Forge`.

## Archivo(s)

- `80-agents/memory/public/known-error/symphony/trade-list-exporter-minio-prefix-mismatch-robust-sqx.md` (nuevo)

## Próximo paso

- Esperar instrucción humana para elegir entre mitigación operativa
  (rewrite del `TargetStrategyArtifact`) o arreglo durable
  (helper único de prefijo jerárquico en `RobustSelection` +
  `04_optimizer_robust`).

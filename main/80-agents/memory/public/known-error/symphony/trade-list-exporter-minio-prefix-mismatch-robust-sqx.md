---
type: known_error
scope: application
created: "2026-07-28"
updated: "2026-07-28"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
application: "[[sqx-worker]]"
entities:
  - "[[StrategyQuant X]]"
  - "[[Symphony]]"
  - "[[MinIO]]"
related:
  - "[[sqx-watcher]]"
  - "[[2026-07-27-trade-list-exporter-type-internal-project-mapping]]"
aliases:
  - trade_list_exporter falla en descarga robust
  - output/robust key no existe
  - 04_optimizer_robust prefijo incorrecto
confidence: high
source_session: "2026-07-28-echo-forge-trade-list-exporter-mismatch"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - app/sqx-worker
  - area/echo
  - kind/known-error
  - project/echo-forge
  - scope/application
  - tool/strategyquant
  - tech/minio
---

# Trade List Exporter — Mismatch de prefijo MinIO entre `04_optimizer_robust` y `trade_list_exporter`

> El activity `trade_list_exporter` busca los `.sqx` robustos bajo el prefijo
> plano `output/robust/`, mientras que `04_optimizer_robust` (Robust Run
> activity) los está subiendo bajo
> `wave_test/<instr>/<dir>/<strat>/<ver>/<trace>/04_optimizer_robust/`. El
> resultado: el activity falla con `failed to stat object ... The specified
> key does not exist` y todos los reintentos (4) reproducen el mismo error.

%% Routing: area/project/application/entities/related usan links canónicos. %%

## Síntoma

- Workflow `sqx-main-00_configs-v1-NDX-H1-L-<id>` progresa correctamente
  por `01_builder`, `02_retester`, `03_optimizer` y `04_optimizer_robust`,
  subiendo artefactos `.sqx` a MinIO sin errores.
- Al entrar a la fase `trade_list_exporter`, el log muestra cuatro
  reintentos con el mismo error:
  ```text
  ERROR Activity error. Namespace sqx-prop TaskQueue sqx-main-queue
  WorkerID <id>@sqx-ulab-zeus-0@ WorkflowID sqx-main-00_configs-v1-NDX-H1-L-<id>
  RunID <run> ActivityType trade_list_exporter Attempt N Error
  error descargando estrategia robusta desde MinIO: error obteniendo objeto:
  failed to stat object sqx-strategies/output/robust/<prefix>_Strategy_<X>.<Y>.z0_robust.sqx:
  The specified key does not exist.
  ```
- Los IDs concretos que el activity intentó y no encontró (en la sesión
  2026-07-28 sobre `example_flow_38`):
  - `NDX_L_H1_example_flow_38_v1_Strategy_6.1.16.z0_robust.sqx`
  - `NDX_L_H1_example_flow_38_v1_Strategy_6.1.23.z0_robust.sqx`
  - `NDX_L_H1_example_flow_38_v1_Strategy_1.1.23.z0_robust.sqx`

## Causa raíz

El `RobustSelection` (en `sqx/activities/worker/robust_activity.go:285`)
persiste el setup con `TargetStrategyArtifact` como una key **plana**:

```go
TargetStrategyArtifact: fmt.Sprintf("output/robust/%s_robust.sqx", eval.StrategyID),
```

Sin embargo, `04_optimizer_robust` (mismo flujo) **sí sube** los
artefactos a la ruta jerárquica del bucket. Inspección con
`mc ls -r minio-worker/sqx-strategies/` confirma que las claves reales son:

```text
wave_test/ndx/l_h1/example_flow_38/v1/<trace>/04_optimizer_robust/NDX_L_H1_example_flow_38_v1_Strategy_<X>.<Y>.z0_robust.sqx
```

El activity `trade_list_exporter`
(`sqx/activities/worker/trade_list_exporter_activity.go:187-199`) usa el
`TargetStrategyArtifact` directamente como `sourceKey` para
`DownloadObjectToPath`, por lo que busca la key plana que **no existe**.
El error se repite en cada estrategia robusta procesada por el
`WorkflowTradeList` y el exporter nunca llega a producir `trades.v1.ndjson.gz`
ni el manifest `trade-manifest.v1.json`.

## Detección

- Mensaje típico: `failed to stat object sqx-strategies/output/robust/...: The specified key does not exist.`
- Cuatro reintentos consecutivos con la misma key indican que no es un
  fallo transitorio de MinIO sino un mismatch de prefijo.
- Verificación directa con `mc ls -r minio-worker/sqx-strategies/ | grep <strategy_id>`
  muestra el `.sqx` robusto bajo `wave_test/.../<trace>/04_optimizer_robust/`,
  nunca bajo `output/robust/`.

## Mitigación operativa (workaround)

Mientras el bug no se arregle, las opciones para destrabar el flujo son:

1. **Reescribir `TargetStrategyArtifact`** justo antes del
   `trade_list_exporter` para apuntar a la ruta real (usar el helper
   existente que compone `wave_test/<instr>/<dir>/<strat>/<ver>/<trace>/04_optimizer_robust/`).
2. **Actualizar el writer de `RobustSelection`** para que guarde el
   `TargetStrategyArtifact` con el mismo prefijo que usa `04_optimizer_robust`
   al subir.
3. **Aceptar un fallback en `trade_list_exporter`** que, si la key plana
   falla, intente resolver bajo el prefijo jerárquico
   `wave_test/<...>/<trace>/04_optimizer_robust/<basename>`.

## Mitigación duradera (código)

Hay dos arreglos posibles; **recomendado** el #1 para mantener una sola
fuente de verdad del prefijo real.

1. **Recomendado**: en `robust_activity.go` donde se construye el setup,
   componer el `TargetStrategyArtifact` con el helper de key jerárquica
   (mismo helper que usa `04_optimizer_robust` para subir). De ese modo
   `trade_list_exporter` recibe un path válido sin necesidad de fallback.
2. Alternativamente, en `trade_list_exporter_activity.go`, antes del
   `DownloadObjectToPath`, resolver la key plana contra el bucket
   jerárquico cuando falle el primer stat.

Adicionalmente, agregar un test E2E que:
- Cree un `SelectedRobustRun` con un `StrategyID` conocido.
- Verifique que el `RobustRunSetup` resultante tiene un
  `TargetStrategyArtifact` que existe físicamente en MinIO (stat OK).
- Ejerce el `trade_list_exporter` end-to-end sobre ese setup y asserta
  `trades.v1.ndjson.gz` y `trade-manifest.v1.json` en `trade_list/output_path`.

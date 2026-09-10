---
type: agent_memory
scope: internal
created: 2026-07-28
updated: 2026-09-09
index_priority: never
indexable: false
load_policy: manual
memory_state: archived
tags:
  - kind/agent_memory
  - kind/known_error
  - tech/go
  - app/echo-forge
  - topic/sqx
  - topic/trade-list
---

# Continuidad Operativa: bug path fantasma `C:/EchoForge/Builds/TradeList`

## Estado
- Fix aplicado en working tree (sin commit). 3 archivos modificados:
  - `sqx/core/runtime/config.go` —新增 `GetSQXTradeListOutputDir(project)` Linux-canónica.
  - `sqx/activities/worker/trade_list_exporter_activity.go` — reescritura del bloque properties.
  - tests en `trade_list_exporter_activity_test.go` y `core/runtime/config_test.go`.
- Build, `go vet` y `go test ./activities/worker/... ./core/runtime/...` verdes.

## Causa raíz (multi-defecto)
El directorio fantasma `/home/kor/sqx/C:/EchoForge/Builds/TradeList/` NO era un solo bug. Eran **3 defectos encadenados** en `trade_list_exporter_activity.go`:

1. **Nombre de properties incorrecto.** La activity escribía `trade_list_exporter.properties`. El plugin Java `EchoForgeTradeListConfig.load(project)` ignora ese nombre y lee `exporter.properties`. El plugin caía a defaults (`~/SQX_exports/trade_list`).
2. **Property name incorrecto.** La activity escribía `strategy.output_path` (propiedad nativa SQX para exporters MT5, no aplicable al exporter custom). El plugin Java no la reconocía.
3. **Default Windows-style en ETCD.** `trade_list/output_path=C:/EchoForge/Builds/TradeList/` + `resolveTLPath` la prefijaba con `/home/kor/sqx`, generando el path fantasma aunque el plugin nunca lo leyera.

## Fix
- Nueva fn canónica `runtime.GetSQXTradeListOutputDir(project)` alineada con `GetSQXOverviewOutputDir`: `<sqx_data_base>/user/projects/<project>/tradelist`.
- `tlPropsName` cambiado a `"exporter.properties"` (const + comentario referencing el .java).
- Properties ahora sólo contiene `wave_key`, `stage`, `source_folder`, `output_dir` (claves que el plugin Java realmente consume).
- Eliminado `resolveTLPath` y el `execution_params.properties` redundante (YAGNI).
- Eliminado el default `C:/EchoForge/...` y la dependencia ETCD `trade_list/output_path`.

## Convención canónica para exporters custom Java de SQX
Cualquier exporter custom (`EchoForgeTradeListExporter`, futuros) debe:
1. Properties filename: **`exporter.properties`** (NO `<name>_exporter.properties`).
2. Properties location: `user/projects/<project>/exporter.properties`.
3. Output dir: vía `runtime.GetSQX<Kind>OutputDir(project)` — Linux-canónica, sin `C:/`.
4. No usar `strategy.output_path`: es nativa MT5, no aplicable a exporters custom.

## Próximo paso
- Rebuild 0.2.3 (PATCH) + redeploy a Zeus/Hera/Kronos + re-correr `example_flow_39`.
- Limpiar manualmente `/home/kor/sqx/C:/` en los 3 workers antes del redeploy.

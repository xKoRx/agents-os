---
type: known_error
scope: application
created: "2026-07-27"
updated: "2026-07-27"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
application: "[[sqx-watcher]]"
entities:
  - "[[StrategyQuant X]]"
  - "[[Symphony]]"
related:
  - "[[sqx-watcher]]"
aliases:
  - validate_configs busca .cfx en raíz
  - config_folder ignorado por watcher
  - .cfx file not found al pipeline
confidence: high
source_session: "2026-07-27-echo-forge-trade-list-exporter"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - app/sqx-watcher
  - area/echo
  - kind/knownerror
  - project/echo-forge
  - scope/application
  - tool/strategyquant
---

# SQX Watcher — `validate_configs` ignora `config_folder` del `config.json`

> El step `validate_configs` del pipeline del `sqx-watcher` busca los
> archivos `.cfx` en la **raíz** del watch dir, no en el subdirectorio
> declarado por `config_folder` (p.ej. `00_configs`).

%% Routing: area/project/application/entities/related usan links canónicos. %%

## Síntoma

- `input/example/config.json` declara:
  ```json
  "config_folder": "00_configs"
  ```
- El step `validate_configs` falla con:
  `file not found: builder_test.cfx` (o `retester_test.cfx`,
  `optimizer_test.cfx`, `trade_list_test.cfx`).
- El log muestra que el watcher resolvió la ruta como
  `<watch_root>/builder_test.cfx` en lugar de
  `<watch_root>/00_configs/builder_test.cfx`.
- El watcher tampoco es recursivo: ignora subdirectorios.

## Causa raíz

`sqx/adapters/watcher-fsnotify` registra el watch sólo sobre el root
configurado (`/var/lib/symphony/input/`). El builder del pipeline
(`sqx/activities/watcher/pipeline/builder.go`) compone la ruta de
búsqueda del `.cfx` con `path.Join(<watchRoot>, <config_name>)`
cuando debería usar
`path.Join(<watchRoot>, <config_folder>, <config_name>)`.

En la sesión 2026-07-27 se confirmó que el `config_folder` no se
inyecta al resolver la ruta — sólo se lee para informar al log.

## Mitigación operativa (workaround)

Hasta que el bug se arregle en el builder, copiar los `.cfx` a la
raíz del watch dir:

```bash
WORKER=zeus
WATCH=/var/lib/symphony/input
scp input/00_configs/*.cfx kor@192.168.31.101:$WATCH/
```

Caveat: el watcher limpia los `.cfx` de la raíz con rapidez tras
procesar el `config.json`, por lo que esta copia debe hacerse
inmediatamente antes de dropear el `config.json` o re-copiarse
si el flujo se reintenta.

## Mitigación duradera (código)

En `sqx/activities/watcher/pipeline/builder.go`, en el step
`validate_configs`, cambiar la resolución de ruta de:

```go
candidate := path.Join(watchRoot, cfgName)
```

a:

```go
folder := strings.TrimSpace(spec.ConfigFolder)
if folder == "" {
    folder = "."
}
candidate := path.Join(watchRoot, folder, cfgName)
```

Adicionalmente, `sqx/adapters/watcher-fsnotify` debería exponerse
como recursivo (`fsnotify.NewRecursiveWatcher`) o el watcher
debería normalizar rutas relativas a `00_configs/` desde el
`config.json` antes de invocar el builder.

---
type: decision
scope: public
created: "2026-07-27"
updated: "2026-07-27"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
application: "[[EchoForgeTradeListExporter]]"
entities:
  - "[[TradeListArtifactWriter]]"
  - "[[ProjectActivity]]"
  - "[[GenericWorkflow]]"
related:
  - "[[2026-07-26-trade-list-package-complete-and-nonretryable]]"
  - "[[Echo Forge - Cierre de Etapa 4]]#Fase 3 (T3.1-T3.7)"
aliases:
  - trade_list_exporter sin exporter_project
  - internal-project-mapping
  - implicit-exporter-binding
confidence: verified
source_session: "2026-07-27-echo-forge-trade-list-exporter"
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - tech/sqx
  - tech/contract
  - scope/public
  - app/echo-forge
---

# Trade list exporter — `type` internaliza el binding al `exporter_project`

## Contexto

El `input/example/config.json` declaraba explícitamente:
```json
{
  "type": "trade_list_exporter",
  "exporter_project": "EchoForgeTradeListExporter",
  "source_folder": "04_optimizer_robust",
  ...
}
```

El `exporter_project` era ruido para el operador: el `type` ya
identifica unívocamente la actividad de Temporal que ejecutará la
tarea (`trade_list_exporter_activity`), y esa actividad ya conoce el
proyecto Java (`EchoForgeTradeListExporter`) que debe invocar via
`sqcli`. Mantener el campo en el JSON abría dos puertas a errores:

1. **Drift**: si el operador escribe un `exporter_project` distinto
   al que el worker espera para `trade_list_exporter`, la actividad
   cae con `Class with name '<X>' doesn't exist` en SQX.
2. **Acoplamiento**: cualquier renaming del plugin (p.ej.
   `EchoForgeTradeListV2Exporter`) obliga a actualizar el JSON de
   input además del binario del worker.

## Decisión

Eliminar `exporter_project` del JSON de input para el tipo
`trade_list_exporter`. El mapping
`type → exporter_project` vive exclusivamente en el worker
(`sqx/workflows/generic_workflow.go` y
`sqx/activities/worker/trade_list_exporter_activity.go`).

JSON vigente:

```json
{
  "type": "trade_list_exporter",
  "source_folder": "04_optimizer_robust",
  "folder": "04_trade_list",
  "config": "trade_list_test.cfx"
}
```

El worker despacha esta entrada al switch de
`generic_workflow.go` que invoca directamente
`exportTradeListActivity` — el `ProjectActivity` builder genérico
(que sí leería `exporter_project`) no se usa en este camino.

## Rationale

- **Single source of truth**: el binding al plugin Java vive en el
  código que lo invoca. El JSON de input describe intención, no
  wiring interno.
- **Sin drift**: ya no existe el campo que el operador pueda errar.
- **Compatible con el patrón `type → activity`**: el resto de
  tipos del workflow (`apply_selected_run`, `generate_report`,
  `export_mt5_ea`, etc.) ya funcionaban sin declarar internals
  en el JSON. `trade_list_exporter` ahora es coherente con esa
  convención.

## Consecuencias

- **Positivas**: configuración de input más limpia; imposible
  romper el binding desde el JSON.
- **Operacional**: ningún cambio en el resto de tipos
  (`project`, `optimizer`, etc.) — `exporter_project` sigue
  siendo válido para esos porque ahí el builder genérico sí
  lo lee.
- **Negativas**: si en el futuro hay más de un exporter Java
  para trade lists, el binding deja de ser 1:1 con el `type`
  y habría que reintroducir el campo (o crear un nuevo
  `type`). Hoy no es el caso: solo existe
  `EchoForgeTradeListExporter`.

## Alternativas descartadas

- **Mantener `exporter_project` opcional como override**: añade
  una superficie de error sin benefició claro. Si en el futuro
  hay override, se introduce explícitamente y con tests
  asociados.
- **Eliminar `type` y dejar solo `exporter_project`**: rompe el
  switch del workflow y obliga a un dispatcher genérico por
  nombre de proyecto Java, que es justamente el acoplamiento
  que queremos evitar.

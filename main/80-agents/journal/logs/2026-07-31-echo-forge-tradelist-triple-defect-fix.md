---
type: change_log
scope: project
created: 2026-07-31
updated: 2026-07-31
area: "[[Echo]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
entities:
  - "[[Echo Forge - Cierre de Etapa 4]]"
  - "[[2026-07-29-sqx-trade-list-exporter-source-order-count-zero]]"
related:
  - "[[EchoForgeTradeListExporter]]"
confidence: verified
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/changelog
  - scope/project
  - project/echo-forge
  - area/echo
---

# Change log — trade_list_exporter triple defect fix

## Qué cambió

- L3: [[2026-07-29-sqx-trade-list-exporter-source-order-count-zero]] actualizado con causa confirmada (orphan `getMainResultKey` + discovery Go + naming local) y estado de fix.
- Continuidad interna: [[2026-07-31-echo-forge-tradelist-triple-defect-fix]].
- Código symphony (working tree, sin commit): `EchoForgeTradeListExporter.java`, `ProductionSQXTradeSource.java`, `trade_list_exporter_activity.go`, `steps/trade_lists.go` + tests.

## Motivo

Owner pidió reevaluar RCA y fijar el bug que bloquea cierre Etapa 4 / trade list.

## Validación

- `go test ./sqx/activities/worker/ -run 'ExportTradeList|FindTradeList|EnrichTradeList'` OK.
- `go test ./sqx/activities/worker/steps/` OK.
- Compilación Java local no disponible (sin JRE); pendiente en worker/deploy.

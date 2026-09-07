---
type: change_log
scope: project
created: 2026-07-31
updated: 2026-07-31
area: "[[Echo]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
entities:
  - "[[Echo Forge - Cierre de Etapa 4]]"
  - "[[EchoForgeTradeListExporter]]"
  - "[[2026-07-29-sqx-trade-list-exporter-source-order-count-zero]]"
confidence: verified
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/changelog
  - scope/project
  - project/echo-forge
  - area/echo
  - change/updated
---

# Change log — recurrencia Trade List Exporter en flow 57

## Qué cambió

- Se actualizó [[2026-07-29-sqx-trade-list-exporter-source-order-count-zero]] con la recurrencia post-EF-G27 observada en workers `0.2.11`.
- Se actualizó [[Echo Forge - Cierre de Etapa 4]] para mantener abierto el primer bug del cierre de fase 4 y evitar atribuir flow 57 al path mismatch ya corregido.

## Evidencia consolidada

- Las 17 estrategias NDX/H1 llegaron a `05_reretester`; la seleccionada por `a672af99…` existe con 35.954 bytes.
- El plugin abre una estrategia por actividad, pero resuelve `Main: XAUUSD_darwinex/D1`; obtiene cero órdenes cerradas y genera `partial 0/1/1` sin `_SUCCESS`.
- Attempts 1–7 reproducidos en Zeus, Hera y Kronos.
- `06_trade_list`, Mongo `trade_lists` y artefactos remotos permanecen vacíos porque el flujo falla antes de `act_upsert_trade_list`.

## Límite del diagnóstico

La causa inmediata está verificada. No se aisló todavía dónde se contamina físicamente el `result_key`; no se registra como hecho una hipótesis más profunda.

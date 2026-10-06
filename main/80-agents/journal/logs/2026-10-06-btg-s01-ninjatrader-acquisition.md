---
type: change_log
schema_version: 1
scope: session
created: "2026-10-06"
updated: "2026-10-06"
area: "[[Echo]]"
project: "[[Echo Futures]]"
entities:
  - "[[Echo Futures]]"
related:
  - "[[BTG-S01-NINJATRADER-ACQUISITION]]"
aliases: []
confidence: verified
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-10-06-btg-s01-ninjatrader-acquisition

## Cambio

- Creado `10-projects/Echo Futures/artifacts/backtester-stage2-real/BTG-S01-NINJATRADER-ACQUISITION.md` mediante materializador schema v1; documenta mecanismo oficial de exportación, boundaries y acción mínima para adquirir histórico NT.

## Motivo

- El Owner eligió NinjaTrader como fuente; el inventory no localizó un original legible y negó acceso a la caché, sin probar ausencia.

## Fuentes usadas

- [[BTG-S01-DATASET-INVENTORY]], [[Echo Futures — BT-S01 Backtester V1 Design]], source NDJSON certificado, runbook SSH y documentación oficial NT enlazada en el artifact.

## Resolución aplicada

- `BLOCKED_EXTERNAL`: exportador GUI existente; corpus y suficiencia no adquiridos/verificados. No cambiar D6 ni permisos. Export TXT preservado desde su entrega no equivale a original NTD byte a byte.

## Validación

- Materialización contractual y lint strict de los dos paths; revisión estática de evidencia, URLs, límite de claims y source DatasetSource. Sin suite de producto ni run certificatorio.

## Compartibilidad

- Scope local; redacción sin secretos, paths absolutos del vault, dumps ni memoria interna.

## Rollback

- Revertir únicamente este commit documental si se rechaza la evidencia; ningún runtime, original ni repo de producto fue modificado.

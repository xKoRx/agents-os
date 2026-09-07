---
type: session
scope: session
created: 2026-07-09
updated: 2026-07-09
area: "[[Meli]]"
project: "[[Destaques de Precio]]"
application: "[[vis-items-loader-tagging]]"
entities:
  - "[[Destaques de Precio]]"
  - "[[vis-items-loader-tagging]]"
related: []
aliases: [tp-price-discount-motors-to-process-test]
confidence: high
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

# TP Price Discount Motors — summary

## Objetivo

- Reemplazar el handler `ConsumerPriceDiscountMotors` con un TP de prueba.

## Contexto cargado

- [[Destaques de Precio]], [[vis-items-loader-tagging]], RFC de Previous Price Motors y contrato del handler.
- Graphify: consulta enfocada; devolvió ruido de templates junto a las notas de iniciativa.

## Trabajo realizado

- Preparados blueprints locales para input BigQueue, transformación y output BigQueue.
- Contrato: `vis-items-history-save-test` → mapear `msg.item_id/seller_id/category_id` a `id/sellerId/categoryId` → `topic-item-to-process-test`, con filtros `process:price_before_discount_motors` y `vertical:motors`.
- Intento de crear `tp-price-discount-motors-to-process-test` mediante Fury CLI.

## Artifacts creados o modificados

- Blueprints en `cli-services/tp/` del repositorio `vis-items-history`.
- El backend devolvió 500; reintento devolvió `TSA-DUPLICATED_SERVICE_ERROR`, pero el template no es consultable.

## Memoria propuesta o creada

- Known error: servicio TP huérfano tras creación 500.

## Decisiones

- No crear inputs/operations/outputs ni versión mientras el template no sea legible.

## Pendiente

- Limpiar el servicio huérfano desde Template Processing/Fury y reintentar la creación.

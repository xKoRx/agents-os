---
type: known_error
scope: area
created: 2026-07-09
updated: 2026-07-09
area: "[[Meli]]"
project: "[[Destaques de Precio]]"
application: "[[vis-items-loader-tagging]]"
entities:
  - "[[Destaques de Precio]]"
  - "[[vis-items-loader-tagging]]"
related: []
aliases:
  - TP creation 500 duplicate service
  - template processing orphaned service
confidence: high
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - area/meli
  - application/vis-items-loader-tagging
---

# Template Processing — servicio huérfano después de 500

## Síntoma

- Crear un TP devuelve HTTP 500.
- Reintentar el mismo nombre devuelve `TSA-DUPLICATED_SERVICE_ERROR`.
- `templates details/list` no encuentra el template y crear inputs devuelve `TSA-TEMPLATE_NOT_FOUND_ERROR`.

## Causa

- La creación registra/reserva el nombre antes de completar el template o deja un estado parcial no visible en el endpoint de templates.

## Impacto

- El nombre no se puede reutilizar y no se pueden crear inputs, operations ni outputs.

## Detección

- Verificar siempre `list` y `details` después de un POST con 500 antes de reintentar.

## Mitigación

- No seguir creando componentes ni versiones.
- Solicitar cleanup/rollback del servicio huérfano a Template Processing/Fury; luego reintentar con el mismo nombre.

## Evidencia

- [[2026-07-09-tp-price-discount-motors-creation-summary]]
- Comandos Fury observados el 2026-07-09 en [[vis-items-loader-tagging]].

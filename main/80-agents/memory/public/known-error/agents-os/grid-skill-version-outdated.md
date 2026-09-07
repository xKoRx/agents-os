---
type: known_error
scope: integration
created: 2026-07-14
updated: 2026-07-14
area: "[[Meli]]"
project: "[[AGENTS OS - Evaluación y Adopción]]"
entities:
  - "[[AGENTS OS]]"
  - "[[Meli]]"
related:
  - "[[2026-07-14-agents-os-grid-meli-publicacion-summary]]"
aliases:
  - Grid skill version mismatch
  - Grid 426 skill_version_outdated
confidence: verified
source_session: codex-session-2026-07-14-agents-os-grid-publicacion
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - project/agents-os
  - integration/grid
---

# Grid upload rechazado por skill desactualizada

## Síntoma

- `POST /api/v1/engine/run` devuelve `skill_version_outdated` y HTTP 426.
- El servidor indica una versión requerida mayor que la declarada por la skill local.

## Causa

- Drift entre la versión instalada de la skill de Grid y el contrato vigente del servidor.

## Impacto

- El upload no se ejecuta; no se crea documento ni versión.

## Detección

- Ejecutar el endpoint del engine y revisar `current_version`/`latest_version` en la respuesta.

## Mitigación

- Actualizar la skill oficial de Grid a la versión requerida y reintentar con un nuevo `idempotency_key`.
- No usar `skip_version_check` salvo autorización explícita del usuario.

## Evidencia

- [[2026-07-14-agents-os-grid-meli-publicacion-summary]] — Grid rechazó `3.6.3`, aceptó `3.6.4` y publicó el documento privado `01KXGAY6QKSZWEBR5SCY5JSWCE`.

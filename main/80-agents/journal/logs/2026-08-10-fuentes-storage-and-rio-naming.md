---
type: change_log
scope: session
created: 2026-08-10
updated: 2026-08-10
area: "[[Meli]]"
project:
application:
entities:
  - "[[Fuentes — Workspace de repositorios]]"
  - "[[rio-playmaker]]"
  - "[[rio-controlplane-clickhouse]]"
  - "[[rio-controlplane-fury]]"
  - "[[rio-controlplane-flink]]"
  - "[[rio-controlplane-kafka]]"
  - "[[rio-controlplane-signals]]"
  - "[[rio-controlplane-kms]]"
  - "[[rio-controlplane-observability]]"
  - "[[rio-sdk-events]]"
  - "[[rio-materializer]]"
related:
  - "[[agent-constitution]]"
aliases:
  - sources storage created
  - rio checkout naming corrected
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/meli
  - change/created
  - change/updated
---

# Fuentes como storage y naming local RIO

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `70-templates/storage.md`
  - `30-resources/storage/fuentes.md`
  - `80-agents/agents-os/agent-constitution.md`
  - `30-resources/applications/rio-*.md`
  - `~/fuentes/rio-*/`
  - `~/fuentes/graphify-signals.json`

## Motivo

- Evitar que agentes confundan el nombre del remote con el nombre local y vuelvan a clonar repositorios completos dentro del vault.

## Resolución aplicada

- Se renombraron los 10 checkouts locales al patrón `rio-*`.
- Se actualizaron los paths y aliases de las aplicaciones.
- Se creó [[Fuentes — Workspace de repositorios]] como entidad `storage` y `70-templates/storage.md` como su template.
- La constitución ahora exige resolver [[Fuentes — Workspace de repositorios]] antes de clonar o generar grafos.

## Validación

- Existen 10 directorios locales `rio-*` bajo `~/fuentes` y ninguno con el prefijo remoto.
- El grafo mergeado fue regenerado con Graphify en `~/fuentes/graphify-signals.json`.
- El vault no contiene repositorios completos ni directorios `fuentes/`.

## Rollback

- Renombrar los checkouts al estado anterior solo mediante una decisión explícita; mantener [[Fuentes — Workspace de repositorios]] y la regla constitucional.

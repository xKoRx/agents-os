---
type: change_log
scope: session
created: 2026-08-10
updated: 2026-08-10
area: "[[Meli]]"
project:
application:
entities:
  - "[[AGENTS OS]]"
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
  - rio sources relocated
  - no repositories in vault
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
  - change/updated
---

# Reubicación de fuentes RIO y regla de vault

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `80-agents/agents-os/agent-constitution.md`
  - `30-resources/applications/rio-*.md` (paths de workspace)
  - `/Users/rjara/fuentes/graphify-signals.json`
  - `/Users/rjara/fuentes/rio-*/` (10 repositorios y grafos individuales)

## Motivo

- Los repositorios completos y sus grafos no deben vivir dentro del vault de Obsidian.

## Resolución aplicada

- Se reubicaron los 10 repositorios desde el vault a `/Users/rjara/fuentes/`.
- Se regeneró el grafo mergeado con Graphify y se nombró `graphify-signals.json`.
- Se retiró del vault la carpeta `fuentes/` y el grafo mergeado anterior.
- Se agregó a la constitución la prohibición de agregar repositorios completos al vault.
- Las aplicaciones conservan sus notas de referencia y ahora apuntan a `~/fuentes/rio-*/`.

## Validación

- Existen 10 repositorios Git bajo `/Users/rjara/fuentes/`.
- `graphify-signals.json` fue generado por `graphify merge-graphs` con los 10 grafos.
- Resultado: 41.629 nodos y 85.431 aristas.
- El vault no contiene la carpeta `fuentes/`.

## Rollback

- Mover nuevamente los repositorios al workspace anterior y restaurar el JSON anterior solo si se solicita explícitamente; conservar la regla constitucional.

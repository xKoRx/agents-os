---
type: change_log
scope: project
created: 2026-07-28
updated: 2026-07-28
area: "[[Meli]]"
project: "[[Hito 2 - vis-items-loader-tagging]]"
entities:
  - "[[Hito 2 - vis-items-loader-tagging]]"
  - "[[vis-items-loader-tagging]]"
related:
  - "[[Implementación Hito 2 - Destaques de Precio]]"
confidence: verified
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/changelog
  - area/meli
  - app/vis-items-loader-tagging
  - feature/destaques-de-precio

# 2026-07-28 — Motor masivo agnóstico

## Cambio

- Se extrajo la maquinaria durable de scroll desde el handler Motors a `pkg/process/massive`: `Run`, `Settings`, `Spec`, `Engine`, retry/backoff, validación, límites y métricas derivadas por prefijo.
- El handler `vehicle_price_highlight_motors_massive_handler.go` quedó limitado al wiring y a la especificidad Motors: query de góndola y mensajes unitarios.
- Se eliminó el modelo `models.VehiclePriceHighlightMotorsRun`; el contrato durable ahora es `massive.Run`.
- Los middlewares legacy `pkg/middlewares/search_batch_*` no se migraron.

## Validación

- `go test ./...` PASS.
- `go vet ./...` PASS.
- `git diff --check` PASS.

## Continuidad

- El proceso durable queda preparado para futuros consumidores mediante un `massive.Spec`; el gate funcional G2 y la operación/carga de la Fase 2 siguen pendientes.

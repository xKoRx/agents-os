---
type: change_log
schema_version: 1
scope: project
created: 2026-08-25
entities:
  - "[[rio-playmaker]]"
  - "[[rio-sdk-events]]"
related:
  - "[[Crear Context]]"
tags:
  - kind/change-log
  - area/meli
  - project/crear-context
---

# 2026-08-25 — Descripciones de PR reescritas para Crear Context

## Qué cambió

- `10-projects/Meli/Crear Context/Descripción PR — rio-playmaker.md` — reescrita completa sobre `feature/new-component-context @ e33966b2e` (6 commits, 25 archivos +1914/−22, suite 3181 tests). La anterior describía `1cd184a`, previo al code review, a la separación `inputs`/`outputs` y a la normalización de contenedores.
- `10-projects/Meli/Crear Context/Descripción PR — rio-sdk-events.md` — reescrita completa sobre `feature/new-component-context @ 4966eaa` (8 commits, 10 archivos +652/−10, suite 701 tests + gate PASS). La anterior describía `e670af8`.
- `10-projects/Meli/Crear Context/Crear Context.md` — tabla de entrega y bitácora actualizadas con los SHAs, diffstats y suites reales, más los dos bloqueantes abiertos.

## Contenido nuevo pedido por el owner

Las dos descripciones explican que `inputs` es configuración ingresada por el usuario, leída de `component_definition.parameters`, y `outputs` son datos generados por el control plane describiendo la infraestructura provisionada, leídos de `_values`. Nunca se mezclan y siempre salen del mismo service slot.

## Bloqueantes levantados

- **SDK:** `build.gradle` declara `version = '1.4.0'` y el CHANGELOG tiene el heading `## [1.4.0]` bajo `[Released]`, en una rama feature. El release productivo sale desde `master`. Segunda señal: el artefacto que consume Playmaker es `0.0.7-component-context`.
- **Playmaker:** el diff commiteado arrastra `docs/specs/swagger.yaml` con reordenamientos espurios que la suite genera en cada corrida.

## Notas

Las notas de la entrega descartada (`(entrega descartada)`) se conservan sin tocar, como registro histórico.

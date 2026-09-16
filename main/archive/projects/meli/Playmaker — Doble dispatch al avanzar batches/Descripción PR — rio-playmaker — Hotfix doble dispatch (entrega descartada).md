---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Playmaker — Doble dispatch al avanzar batches]]"
  - "[[rio-playmaker]]"
aliases:
  - PR rio-playmaker hotfix duplicate deployments
  - descripción PR doble dispatch Playmaker
tags:
  - kind/doc
  - project/playmaker-double-dispatch
  - application/rio-playmaker
  - area/meli
created: "2026-08-26"
updated: "2026-08-27"
---

# Descripción PR — rio-playmaker — Hotfix doble dispatch

## Propósito

Fuente local de la descripción publicada del hotfix de doble dispatch en el PR #1079.

## Description

Dos callbacks de componentes distintos podían evaluar el mismo batch siguiente sin materializar y dispararlo dos veces. Este cambio serializa cada transición por `pipelineExecutionId + nextBatchOrder` usando Fury Lock.

El listener adquiere la lease antes de abrir la transacción fresca, relee prerrequisitos y materialización desde la base, y termina en no-op cuando el batch ya está completo. La contención se reintenta con backoff acotado y coalescing local; si el lock no confirma ownership, el flujo falla cerrado y no despacha.

### Cambios

* Agrega `lockclient:5.0.0` y WorkQueues `4.0.0`, namespace Fury Lock configurable y una identidad estable por ejecución y orden de batch; el cliente valida la identidad Fury canónica del servicio antes de iniciar.
* Mantiene una lease con TTL configurable de 1 a 7 segundos, 5 por defecto, sin renovación; la sección crítica debe terminar dentro de ese límite.
* Conserva relectura fresca, idempotencia por componentes materializados, retries coalescidos, cancelación de callbacks obsoletos y métricas de adquisición, contención, indisponibilidad, agotamiento, fallo de release y hold duration.
* Elimina la barrera específica del avance anterior, sin modificar otros usos legítimos del proyecto.

### Límites y operación

Los retries son locales y finitos. Una indisponibilidad del lock, rechazo del scheduler o agotamiento no despacha y requiere un callback posterior o recuperación operativa. El release fallido se registra; la lease expira según su TTL. No se agregan migraciones, cambios de API ni cambios de control planes.

## How Has This Been Tested?

* `withoutLock_whenConcurrentCallbacksReadSameSnapshot_thenDispatchesTwice`: exactamente 2 dispatches, reproduciendo el defecto.
* `withSharedFuryLock_twoIndependentListenersProduceExactlyOneDispatch`: exactamente 1 dispatch con backend de lock compartido.
* Cobertura de contención, identidades distintas, indisponibilidad y excepciones unchecked, scheduler rejection, retries obsoletos, release exacto, materialización parcial e identidades incompletas.
* `./gradlew test jacocoTestReport --no-daemon`: 3.237 tests, 0 fallas, 0 errores y 2 skipped.
* `./gradlew check --no-daemon` y `git diff --check`: PASS.

## Issue

`SIG-186` — deployments duplicados al avanzar batches en Playmaker.

## Notas internas

El body se generó desde cero con `zord author pr-description` usando backend Codex `gpt-5.6-terra`, luego se completó con los resultados locales verificados y se publicó en el PR #1079.

---
type: decision
scope: project
created: 2026-07-28
updated: 2026-07-28
area: "[[Meli]]"
project: "[[Fase 2 — Proceso Masivo por Site vía items_batch_search — Loader Tagging]]"
application: "[[vis-items-loader-tagging]]"
entities:
  - "[[Fase 2 — Proceso Masivo por Site vía items_batch_search — Loader Tagging]]"
  - "[[vis-items-loader-tagging]]"
  - "[[vis-sdk-go]]"
related:
  - "[[Hito 2 - vis-items-loader-tagging]]"
aliases:
  - regularización periódica de góndola Motors
  - scheduler masivo de Destaque de Precio
confidence: verified
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - area/meli
  - app/vis-items-loader-tagging
  - feature/destaques-de-precio
  - phase/2
---

# Regularización periódica de góndola usa runs durables por site

## Contexto

- La góndola de Destaque de Precio debe regularizarse de manera periódica y
  obligatoria; un reproceso manual de IDs no cubre esa necesidad operativa.
- Fase 2 ya implementa un trigger por site y una cadena durable de scroll, pero
  no incluye el scheduler ni un lock de runs por site.

## Decisión

- Usar el proceso masivo de Fase 2 como camino canónico para la regularización
  periódica por site.
- Un scheduler externo invoca el trigger según la cadencia operativa.
- Mientras no exista lock o deduplicación, el scheduler debe evitar runs
  solapados para el mismo site.
- Reservar `BulkService` para reprocesos manuales de listas conocidas, no para
  la cobertura periódica completa de la góndola.

## Rationale

- El driver de Fase 2 conserva `context_id` y `page_number` en mensajes
  durables, procesa una página por ejecución y no acumula la góndola completa
  en memoria.
- El fan-out reutiliza el processor unitario existente y permite reentregas
  sin crear una segunda implementación de las reglas de precio.

## Consecuencias

- La salida a producción requiere configurar scheduler, tópico driver,
  consumer, allowlist, límites finitos y observabilidad por site.
- Antes de fijar la cadencia se debe validar latencia real, TTL del cursor y
  carga representativa.
- La ausencia actual de exclusión mutua por site queda como riesgo operativo
  explícito y follow-up de robustez.
- Antes de habilitar la periodicidad se debe detectar un cursor sin avance y
  agregar correlación por `run_id`/`page_number`; las métricas actuales son
  agregadas y no cuentan ítems reales.

## Alternativas descartadas

- Ejecutar periódicamente `BulkService`: requiere preparar la lista completa,
  queda ligado al request y no conserva progreso durable.
- Barrer toda la góndola dentro del trigger: excede el tiempo de ejecución y
  obliga a reiniciar desde cero ante fallas.

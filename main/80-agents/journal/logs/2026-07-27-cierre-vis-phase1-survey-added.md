---
type: change_log
scope: project
created: 2026-07-27
updated: 2026-07-27
area: "[[Meli]]"
project: "[[Fase 1 — Modelo de Señales Price Discount — Loader Tagging]]"
entities:
  - "[[Fase 1 — Modelo de Señales Price Discount — Loader Tagging]]"
  - "[[Cierre VIS]]"
related:
  - "[[Hito 2 - vis-items-loader-tagging]]"
confidence: verified
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/changelog
  - area/meli
  - app/vis-items-loader-tagging
  - phase/1
---

# 2026-07-27 — Encuesta de cierre de dudas Fase 1

## Cambio

- Se agregó una encuesta al proyecto agente para cerrar decisiones de contrato, compatibilidad, atomicidad, calendario, rollout y continuidad de Fases 2–3.
- Cada pregunta quedó vinculada a una salida concreta del plan o a un gate.
- La revisión posterior reclasificó F4 como dependencia del spec funcional y eliminó `signals` como supuesto de contrato de entrada; el código actual usa `process:<id>` y `filters.modified_fields`.
- Se actualizó el plan y la checklist: F4 quedó fuera del alcance del loader; F7 pasó a ser mapping técnico derivado del código.

## Validación

- Las respuestas cerraron el alcance, atributos, compatibilidad legacy, atomicidad, calendario y proceso masivo; quedan C2–C5 para las fases posteriores y el mapping de F7 para la lectura técnica.
- El proyecto conserva una sola nota como planificador; la encuesta vive dentro de esa nota y no crea un plan paralelo.

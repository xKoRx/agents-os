---
type: prompt
schema_version: 1
status: active
area: "[[Personal]]"
target: "agent"
prompt_version: 1
inputs:
  - fase o tarea acotada
  - nota planificadora canónica
  - evidencia disponible
outputs:
  - cambios verificables
  - actualización de estado y bitácora
application:
project:
aliases: []
related: []
tags:
  - kind/prompt
created: "2026-08-10"
updated: "2026-08-10"
---

# Executor de fase de agente

## Propósito

Encargar una fase o tarea acotada preservando la nota del proyecto como único planificador durable.

## Contrato de entrada

- Una tarea concreta y sus criterios de aceptación.
- La ruta o link de la nota planificadora y las fuentes que deben verificarse.

## Contrato de salida

- Implementación acotada y comandos de validación con resultado.
- Estado de tareas, progreso y bitácora actualizados en el planificador.

## Prompt

```text
Ejecuta únicamente la fase o tarea indicada. Usa la nota planificadora como fuente de verdad, valida las fuentes afectadas y no declares completado un resultado sin evidencia reproducible. Actualiza la tarea, el estado y la bitácora en el mismo cambio material. Si falta acceso o autoridad para una dependencia externa, detente, conserva la fuente única existente y registra el bloqueo con el siguiente paso exacto.
```

## Límites

- No reemplaza una skill ni autoriza cambios fuera de la fase asignada.
- No crea un plan paralelo ni marca como Done una tarea puente humana.

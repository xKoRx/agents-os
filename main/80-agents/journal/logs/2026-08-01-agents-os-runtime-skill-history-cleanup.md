---
type: change_log
scope: session
created: 2026-08-01
updated: 2026-08-01
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[AGENTS OS - Hot Path y Cierre Silencioso]]"
  - "[[skill-contract]]"
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - project/agents-os
  - change/updated
---

# AGENTS OS — limpieza de historia en skills runtime

## Motivo

Los `Finish Tasks` y `Progress Log` mezclaban estado e historia de desarrollo
con procedimientos que el agente debe leer completos durante una ejecución.
Esto contradecía `skill-contract.md` y duplicaba información ya presente en el
cuerpo de las skills, proyectos o logs previos.

## Cambio

- Se revisaron las 22 skills que contenían esos headings.
- Se retiraron las secciones de implementación y progreso cuando no cambiaban
  una decisión runtime.
- No se creó memoria nueva: los hechos durables relevantes ya estaban
  incorporados en los procedimientos o fuentes canónicas existentes.
- `sqx-temporal-failure-audit` conservó su checklist por ejecución, renombrado
  a `Evidence Completion Gate` para no confundirlo con backlog de desarrollo.
- El proyecto controlador dejó de instruir que se agreguen esos bloques a las
  skills y registró la limpieza como estado real.

## Validación

- La búsqueda `^## (Finish Tasks|Progress Log)` sobre `80-agents/skills/*/SKILL.md`
  no devuelve resultados.
- El procedimiento durable de cada skill permanece en su cuerpo.
- El doctor conserva sus hallazgos previos no relacionados; esta limpieza no
  introdujo nuevas referencias rotas.

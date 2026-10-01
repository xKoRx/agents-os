---
type: learning
schema_version: 1
scope: application
created: "2026-10-01"
updated: "2026-10-01"
area: "[[Meli]]"
project: "[[Playmaker — Context en emisores existentes]]"
application: "[[rio-playmaker]]"
entities:
  - "[[rio-playmaker]]"
related:
  - "[[SPEC Funcional — Context transversal en RIO]]"
aliases:
  - "Flujo funcional versus mecanismo interno de Playmaker"
confidence: high
source_session: "01a0f2b3-8e01-7130-8ef6-ac26a639e079"
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/application
  - tech/rio
---

# Verificar invocaciones antes de describir flujos de Playmaker

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Aprendizaje

- Antes de describir un flujo existente en una SPEC de Playmaker, comprobar su entrada real (endpoint, scheduler o llamada interna), cadena de invocaciones, guards y operación publicada en un commit identificado. Una mención en chat o el nombre de un método no demuestra un flujo funcional independiente.
- Distinguir flujo funcional, mecanismo interno y operación del contrato. Un mecanismo invocado puede reutilizar `PROVISION` sin crear una operación o API `RETRY`; no contarlo como otro flujo funcional por su nombre.
- Código y configuración versionada acreditan implementación. Declarar uso efectivo en producción requiere evidencia de la release/configuración/runtime; conservar explícita esa brecha cuando no se ha verificado.

## Aplicabilidad

- **Cuándo cargarlo:** al evaluar alcance, corregir afirmaciones de existencia o redactar SPECs sobre rutas existentes de Playmaker.
- **Cuándo no cargarlo:** para diseñar una capacidad nueva que ya está identificada como propuesta, o trabajo ajeno a rutas y emisores de Playmaker.

## Entidades relacionadas

- [[rio-playmaker]], [[Playmaker — Context en emisores existentes]].

## Evidencia

%% Cita de fuente, NO prosa narrativa: link a sesión/log/archivo + una línea de qué la respalda. No re-parafrasear el aprendizaje ya destilado arriba (constitución: memorias compactas). %%

- Fuente: [[2026-10-01-playmaker-context-flows-corrected]] — audit por commit y corrección de la clasificación tras el cuestionamiento reportado por el owner.

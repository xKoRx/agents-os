---
type: learning
schema_version: 1
scope: project
created: "2026-08-25"
updated: "2026-08-25"
area:
project: "[[Estandarización de Scopes RIO]]"
application: "[[RIO]]"
entities:
  - "[[Estandarización de Scopes RIO]]"
related:
  - "[[Scopes RIO - Discovery de Integraciones y Persistencia]]"
aliases: []
confidence: verified
source_session: "[[2026-08-25-scopes-rio-discovery-project-created]]"
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/project
  - area/meli
  - project/scopes-rio
---

# scope-is-multidimensional-and-not-a-transversal-carrier

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Aprendizaje

- En Signals/RIO, `scope` no es hoy un carrier transversal: el runtime `SCOPE`, el ambiente lógico, el segmento Fury, los auth scopes y el parámetro `scope` de `/signals/context` tienen autoridades y transportes distintos.
- Los frontends seleccionan Playmaker por `baseURL`; los eventos de deployment llevan ambiente y componente, pero no scope; por lo tanto un refactor debe introducir un contexto tipado con provenance antes de cambiar routing o persistencia.

## Aplicabilidad

- **Cuándo cargarlo:** Al diseñar o revisar propagación de scopes entre front, Playmaker, BigQueue, control planes, Materializer y storage.
- **Cuándo no cargarlo:** Para resolver una ruta o configuración puntual de una aplicación sin impacto en la semántica transversal de RIO.

## Entidades relacionadas

- [[Estandarización de Scopes RIO]]
- [[Scopes RIO - Discovery de Integraciones y Persistencia]]

## Evidencia

%% Cita de fuente, NO prosa narrativa: link a sesión/log/archivo + una línea de qué la respalda. No re-parafrasear el aprendizaje ya destilado arriba (constitución: memorias compactas). %%

- Fuente: [[Scopes RIO - Discovery de Integraciones y Persistencia]] — Matriz as-is y secciones de semántica, transporte, persistencia y seams; cortes HEAD con evidencia `repo + commit + path + líneas`.
- Fuente: [[2026-08-25-scopes-rio-discovery-project-created]] — Registro de creación del proyecto agente, evidencia y validación de cierre.

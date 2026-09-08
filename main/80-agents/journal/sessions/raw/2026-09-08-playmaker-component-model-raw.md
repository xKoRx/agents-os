---
type: raw_session
schema_version: 1
scope: session
created: "2026-09-08"
updated: "2026-09-08"
area: "[[Meli]]"
project:
application: "[[rio-playmaker]]"
entities:
  - "[[rio-playmaker]]"
related:
  - "[[Playmaker — Doble dispatch al avanzar batches]]"
aliases: []
confidence: verified
source_session:
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-raw.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# 2026-09-08-playmaker-component-model-raw

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: [[Codex]]
- Proyecto o entidad: [[rio-playmaker]]
- Objetivo de la sesión: aclarar el modelo de dominio de despliegue de Playmaker.

## Transcript

Usuario: “qué diferencia hay entre un component y un component run en playmaker?”

Agente: explicó que `Component` es la identidad lógica y `ComponentRun` es su ejecución dentro de una `PipelineExecution`.

Usuario: “y cuando está desplegado qupe es? un service?”

Agente: explicó `Service` como slot operativo del componente en un ambiente y `Deployment` como intento de deploy/redeploy.

Usuario: “un pipeline vs pipeline execution?”

Agente: distinguió la definición reusable del pipeline de una corrida concreta.

Usuario: “ese component son estáticos no? siempre son los mismos?”

Agente: precisó que la identidad lógica suele persistir entre ejecuciones, aunque su configuración puede versionarse.

Usuario: “component - component definition y component run?”

Agente: distinguió entidad lógica, versión de configuración y ejecución que referencia ambas.

Usuario: “cuando se genera el service? cuando vuelve el componentrun del cp? o antes?”

Agente: verificó en `PipelineDeployServiceImpl.enrichWithServiceIds` que el `Service` se crea antes del dispatch del CP, durante la preparación del deploy; el callback actualiza su estado y outputs.

## Evidencia externa

- 

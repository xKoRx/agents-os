---
type: learning
schema_version: 1
scope: project
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities: []
related:
  - "[[2026-09-04-forge-campaign-v2-stop-policy-schema-mismatch]]"
aliases: []
confidence: high
source_session: ECHO-FORGE-CAMPAIGN-V2-STOP-POLICY-SCHEMA-BOUNDARY-FIX-NORMAL
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/project
  - project/echo-forge
---

# 2026-09-04-nested-domain-schema-authority

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Aprendizaje

- No reutilizar el discriminator de schema del contrato padre como autoridad de un contrato anidado independiente; cada boundary debe proyectar explícitamente hacia la authority propia del contrato destino.

## Aplicabilidad

- **Cuándo cargarlo:** al mapear wrappers versionados hacia policies, intents, snapshots o cualquier contrato anidado con validación propia.
- **Cuándo no cargarlo:** cuando el campo pertenece al mismo contrato y su authority es explícitamente compartida.

## Entidades relacionadas

- [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]] · [[2026-09-04-forge-campaign-v2-stop-policy-schema-mismatch]]

## Evidencia

%% Cita de fuente, NO prosa narrativa: link a sesión/log/archivo + una línea de qué la respalda. No re-parafrasear el aprendizaje ya destilado arriba (constitución: memorias compactas). %%

- Fuente: [[2026-09-04-forge-campaign-v2-stop-policy-schema-boundary-fix]] — T1–T3 prueban ownership independiente y T4–T5 preservan el contrato v2/BWC v1.

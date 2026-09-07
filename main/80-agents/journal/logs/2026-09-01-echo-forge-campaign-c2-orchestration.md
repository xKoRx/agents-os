---
type: change_log
schema_version: 1
scope: session
created: "2026-09-01"
updated: "2026-09-01"
area:
project:
application:
entities: []
related: []
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-01-echo-forge-campaign-c2-orchestration

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]
  - xKoRx/symphony: runtime, binding, registry, worker activities, workflow, worker wiring y pruebas C2

## Motivo

- Se ejecutó la fase C2 del modelo ECHO-FORGE-CAMPAIGN-STOP-POLICY-V1-C2-ORCHESTRATION-NORMAL sobre el baseline exacto `bcd44eef2f2df23b839db90e167e58fac8e6e91c`; commit final `f8bc04bb2441bfd16f836d940cf66e174b41c72b` publicado en `origin/master`.

## Fuentes usadas

- Modelo C2 pegado por el usuario, checkpoint C1 y código/test del repositorio.

## Resolución aplicada

- Se incorporó configuración estricta `forge_campaign`, snapshot canónico, materialización determinista de waves y routing `config_source_wave`; se agregaron ports/adapters PostgreSQL, activities `forge_campaign_*`, parent `ForgeCampaignWorkflow`, child GenericSQXWorkflow exacto y registro del worker. Se preservaron C3, release/deploy y los dos dirty files extranjeros.

## Validación

- Pasaron pruebas focalizadas, integración PostgreSQL, race focalizado, vet, compile del worker y `git diff --check`. Las suites amplias mantienen fallos baseline por fixture `mt5-export.htm` ausente y tests legacy sin `flow_run_start` registrado.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir el commit C2 publicado manteniendo fuera del staging los dos archivos dirty extranjeros; cualquier rollback debe respetar el gate de baseline.

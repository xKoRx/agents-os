---
type: change_log
schema_version: 1
scope: session
created: "2026-09-02"
updated: "2026-09-02"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities:
  - "[[Symphony]]"
  - "[[sqx-watcher]]"
related: []
aliases: []
confidence: high
source_session: "ECHO-FORGE-C3-RESUME-FROM-PUBLISHED-0.2.85-NORMAL"
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-02-echo-forge-c3-config-source-wave-known-error

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `80-agents/memory/public/known-error/symphony-config-source-wave-legacy-cfg.md`

## Motivo

- Se registró el error reusable de procedencia `cfg_id`/`config_minio_key` legacy dentro de una ola nueva.

## Fuentes usadas

- Evidencia read-only del run `d7693ebe-4ea8-4c10-a65e-c45d676ac788`, PostgreSQL y logs worker; checkpoint del proyecto del 2026-09-02.

## Resolución aplicada

- Crear el known error como memoria pública compacta para que futuras certificaciones detengan el gate antes de aceptar promoción o Campaign.

## Validación

- Validado contra la fila nueva `bb242481-d755-43a1-8425-61cce5ce03eb` y la fila legacy `69b44c2c-adcf-4bb0-be6e-c8997ccda3cc`; no se modificó la base ni el repositorio de producto.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- No aplica: cambio de memoria, no de producto.

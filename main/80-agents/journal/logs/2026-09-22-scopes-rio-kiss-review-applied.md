---
type: change_log
schema_version: 1
scope: session
created: "2026-09-22"
updated: "2026-09-22"
area: "[[Meli]]"
project: "[[Estandarización de Scopes RIO]]"
application:
entities:
  - "[[RIO]]"
  - "[[rio-playmaker]]"
  - "[[rio-controlplane-flink]]"
  - "[[rio-sdk-events]]"
related:
  - "[[SPEC técnica — Routing KISS por scope en rio-playmaker]]"
  - "[[POC KISS — Routing de scopes en Playmaker]]"
  - "[[SPEC técnica — Continuidad de scope en control planes RIO]]"
  - "[[scope-naming-standard]]"
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

# 2026-09-22-scopes-rio-kiss-review-applied

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated / conflict-resolution
- **Archivo(s):**
  - `10-projects/Meli/Estandarización de Scopes RIO/SPEC técnica — Continuidad de scope en control planes RIO.md`
  - `10-projects/Meli/Estandarización de Scopes RIO/SPEC técnica — Routing KISS por scope en rio-playmaker.md`
  - `10-projects/Meli/Estandarización de Scopes RIO/agentes/POC KISS — Routing de scopes en Playmaker.md`
  - `10-projects/Meli/Estandarización de Scopes RIO/Estandarización de Scopes RIO.md`
  - `30-resources/rio-atlas/architecture/scope-naming-standard.md`

## Motivo

- Incorporar el review independiente sin convertir la POC en un framework genérico ni agregar persistencia antes de necesitarla.

## Fuentes usadas

- Review adjunto por el usuario, basado en refs remotas frescas de Playmaker, Flink, SDK y control planes.
- Verificación directa de los dos deployment trigger producers activos en Playmaker.
- Verificación directa de KVS, Pub/Sub y jobs durables de Flink GCP.
- Contratos existentes de `BigQueueMessage`, `BigQueueFilters`, `sendWithFilters` y mqclient 3.4.9.

## Resolución aplicada

- Se acepta que `unresolved=legacy` era fail-open; el runtime canónico ahora resuelve una lane al startup o no arranca.
- Se incluyen ambos trigger producers y el result producer de Playmaker.
- Se deshabilita timeout processing en alpha en vez de persistir una lane para retry.
- Flink GCP/KVS/PubSub y cualquier path durable quedan fuera del golden deploy y deshabilitados por configuración existente.
- No se implementan classifier de cuatro estados, carrier, `expectedScope`, cambios SDK ni framework común.
- Fury/BigQueue pasa a gate obligatorio de plataforma y la generalización espera un segundo caso real.

## Validación

- Los documentos distinguen etiquetas funcionales `production/staging` de tokens runtime `prod/stage`.
- La matriz contractual incluye startup fail-closed, mismatch/missing/malformed, producers completos, paths durables off y rollback con drain.
- Los documentos modificados pasan lint estricto sin findings.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Restaurar las versiones anteriores de los cinco documentos y eliminar este change log; no existen cambios de código ni infraestructura.

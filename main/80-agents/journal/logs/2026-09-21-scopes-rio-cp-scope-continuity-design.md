---
type: change_log
schema_version: 1
scope: session
created: "2026-09-21"
updated: "2026-09-21"
area: "[[Meli]]"
project: "[[Estandarización de Scopes RIO]]"
application:
entities:
  - "[[RIO]]"
  - "[[rio-controlplane-flink]]"
  - "[[rio-sdk-events]]"
related:
  - "[[SPEC técnica — Continuidad de scope en control planes RIO]]"
  - "[[SPEC técnica — Routing KISS por scope en rio-playmaker]]"
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

# 2026-09-21-scopes-rio-cp-scope-continuity-design

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `10-projects/Meli/Estandarización de Scopes RIO/SPEC técnica — Continuidad de scope en control planes RIO.md` (created)
  - `10-projects/Meli/Estandarización de Scopes RIO/Estandarización de Scopes RIO.md` (updated)

## Motivo

- Diseñar la Fase 3 de la POC alpha para que los control planes preserven el filtro `scope:x` desde el trigger hasta el result y documentar qué componentes comunes ya existen en los repos vigentes.

## Fuentes usadas

- Refs remotas refrescadas el 2026-09-21 para `rio-sdk-events`, Flink, Kafka, ClickHouse, Fury, Observability, KMS y Signals.
- Contratos `BigQueueMessage`, `BigQueueFilters` y `BigQueueClient.sendWithFilters` de `rio-sdk-events`.
- Controllers, carriers internos y publishers de deployment/actions de los control planes; patrón de tags arbitrarios en `vis-items-loader-tagging`.

## Resolución aplicada

- La Fase 3 queda definida como continuidad de scope en CPs con Flink como piloto de deployment trigger/result.
- El contrato extrae exactamente un `scope:x`, lo transporta fuera del payload de dominio, valida `expectedScope` y publica el mismo tag; legacy sin filtro permanece compatible y malformed/mismatch falla cerrado.
- La promoción del helper a `rio-sdk-events` ocurre desde la segunda adopción; Fury queda al final por necesitar continuidad durable en reconciliadores.

## Validación

- La SPEC no contiene placeholders, mantiene una línea por párrafo/bullet y enlaza su tarea de Review desde el proyecto.
- Baselines remotas y capacidades de envelope/publicación filtrada fueron verificadas directamente en Git; no se modificó código ni worktrees de producto.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Eliminar la SPEC y revertir las actualizaciones del proyecto (fila de Fase 3, tarea de Review y checkpoint/decisión); no existen cambios de código ni infraestructura.

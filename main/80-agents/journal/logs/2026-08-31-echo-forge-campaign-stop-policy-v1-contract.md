---
type: change_log
schema_version: 1
scope: session
created: "2026-08-31"
updated: "2026-08-31"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application:
entities: []
related:
  - "[[2026-08-31-forge-campaign-stop-policy-v1-contract]]"
aliases: []
confidence: verified
source_session: "ECHO-FORGE-CAMPAIGN-STOP-POLICY-V1-CONTRACT-TOP"
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-31-echo-forge-campaign-stop-policy-v1-contract

## Cambio

- **Tipo:** created
- **Archivo(s):** Decision L3 `2026-08-31-forge-campaign-stop-policy-v1-contract` y checkpoint append-only de `Echo Forge - Arquitectura de Datos y Migración de Persistencia`.

## Motivo

- Congelar un contrato implementable y auditable para Forge Campaign antes de entregar código a un agente NORMAL.

## Fuentes usadas

- Source real `xKoRx/symphony@9c90a2f75108c729eaee6a0906eb9b057f3af970`, checkpoints Promotion Core, physical cert `0.2.83`, Promotion Result Surface y config isolation.

## Resolución aplicada

- Se congelaron aggregate, identidad, config, lifecycle, schema PG, parent Temporal, wave mapping, acumulación, stop precedence, failure semantics, query model, slicing y certificación física. No hubo cambios de source, migrations, commits ni push.

## Validación

- Auditoría read-only de los símbolos exigidos; HEAD y `origin/master` iguales al baseline autorizado; foreign dirty preexistente preservado. Schema notes materializadas desde el contrato AGENTS OS.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos; los paths locales no forman parte de la Decision reusable.

## Rollback

- Eliminar la Decision y este log, y retirar sólo el checkpoint append-only de esta sesión; Symphony no requiere rollback porque no fue modificado.

---
type: raw_session
scope: session
created: "2026-07-23"
updated: "2026-07-23"
area: "[[Symphony]]"
project:
application: "[[Symphony]]"
entities:
  - "[[Symphony]]"
  - "[[sqx-instrument-sync]]"
  - "[[Zeus]]"
  - "[[Hera]]"
  - "[[Kronos]]"
related: []
aliases: []
confidence: verified
source_session:
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
  - area/symphony
---

# SQX instrument sync v3 — identidad total bit-a-bit

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: Cursor (GLM-5.2)
- Proyecto o entidad: [[Symphony]] / skill `sqx-instrument-sync`
- Objetivo de la sesión: Reescribir la skill y el script `sync_user_data_zeus.sh` para garantizar identidad bit-a-bit de `~/sqx/user/data` entre Zeus/Hera/Kronos, incluyendo DBs H2, tras feedback del operador.

## Transcript

```
Pegar aquí la sesión completa.
```

## Evidencia externa

- Script versionado: `.agents/skills/sqx-instrument-sync/scripts/sync_user_data_zeus.sh` (hash `767b4a1b...`).
- Skill v3.0.0 y RUNBOOK.md en `.agents/skills/sqx-instrument-sync/`.
- Pruebas en cluster real 2026-07-23: Hera/Kronos divergían en `data_futures.h2.db` y `data_stock.h2.db`; tras sync los 3 hosts quedaron con hash maestro `1383ab9e...` (27 entradas), EQUAL, idempotente.
- Script desplegado en Zeus como `~/sync_user_data_zeus.sh`.

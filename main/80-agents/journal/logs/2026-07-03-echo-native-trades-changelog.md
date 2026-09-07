---
type: change_log
scope: session
created: "2026-07-03"
updated: "2026-07-03"
area: "[[Personal]]"
project: "[[Echo]]"
application: "[[Echo]]"
entities:
  - "[[Echo]]"
related: []
aliases: []
confidence: verified
source_session: "ca7312d2-f138-4a35-9af2-87ea17b79c1b"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-07-03 - Echo - Native Trades Persistence Fix - Changelog

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `v3/clients/mt4/execution_agent_v3.mq4`
  - `v3/clients/mt5/execution_agent_v3.mq5`
  - `v3/sdk/domain/trade_journal.go`
  - `v3/sdk/postgres/trade_journal_open.go`
  - `v3/sdk/postgres/trade_journal_repository.go`
  - `v3/sdk/domain/journal_open_test.go`

## Motivo

- Corregir el fallo de persistencia de las operaciones nativas (tanto manuales como automáticas) en la tabla `trade_journal`. Las manuales no se guardaban debido a la falta de `strategy_id` en el backend, y las automáticas no se guardaban debido a la omisión de la serialización de metadatos de apertura (`strategy_id`, `magic_number`, `symbol`, `side`, `lot_size`) en el JSON `"execution_result"` enviado por el EA.

## Fuentes usadas

- Inspección de base de datos de desarrollo y producción de Echo.
- Inspección de los logs del backend y código fuente de EAs.

## Resolución aplicada

- **EA (MQL4/MQL5):** Se actualizó `EnqueueNativeOpenResult` para serializar y enviar todos los metadatos de apertura requeridos.
- **Go Backend (Domain):** Se agregó el campo `Origin` a `TradeJournalEntry` y se actualizaron los mappers para asignar `SourceType = "NATIVE"` y `Origin = "NATIVE"` al detectar operaciones nativas, además de asignar `"NATIVE"` como default para `strategy_id` si está vacío.
- **Go Backend (Postgres):** Se actualizaron los inserts y updates de SQL para persistir el valor de la columna `origin`.

## Validación

- Se agregaron unit tests en `journal_open_test.go` que comprueban tanto el mapeo nativo manual como el automático.
- Ejecución exitosa de pruebas unitarias locales en los paquetes de dominio y base de datos:
  - `go test -v ./v3/sdk/domain/...` -> PASS
  - `go test -v ./v3/sdk/postgres/...` -> PASS

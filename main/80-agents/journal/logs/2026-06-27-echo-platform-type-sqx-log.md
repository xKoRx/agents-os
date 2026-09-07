---
type: change_log
scope: session
created: "2026-06-27"
updated: "2026-06-27"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[echo]]"
entities:
  - "[[echo-forge]]"
  - "[[echo]]"
related: []
aliases: []
confidence: verified
source_session: "1ee0d77f-17a7-4fd9-9ced-d2e0ff8f1703"
load_policy: manual
indexable: false
index_priority: never
tags:
  - app/echo
  - area/echo
  - kind/changelog
  - project/echo-forge
  - project/echoforge
  - scope/session
---
# Change Log: Add SQX to Platform Types

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - Repositorio `echo`:
    - `v3/docs/postgres/echo.sql`
    - `v3/front/sql/005_accounts_platform_type.sql`
    - `v3/front/src/views/admin/AccountDetailView.vue`
    - `v3/front/src/views/admin/AccountsView.vue`
    - `v3/sdk/postgres/migrations/001_schema_baseline.up.sql`
    - `v3/sdk/postgres/scripts/rollout_v3_production_idempotent.sql`
    - `v2/docs/postgres/echo.sql`
    - `v2/front/sql/005_accounts_platform_type.sql`
    - `v2/front/src/views/admin/AccountDetailView.vue`
    - `v2/front/src/views/admin/AccountsView.vue`

## Motivo

- Permitir que las cuentas de trading registren la plataforma 'SQX' (StrategyQuant X) como su tipo de plataforma de trading (al igual que MT4, MT5, cTrader, etc.) para soportar la ingesta y publicación automática en el flujo de Echo Forge.

## Fuentes usadas

- Base de datos relacional y código de frontend de la aplicación Echo.

## Resolución aplicada

- Añadido el tipo `'SQX'` al tipo enumerado `platform_type_enum` en todas las migraciones, baselines y scripts SQL (tanto en la versión v2 como v3).
- Modificadas las vistas de administración de cuentas de usuario en Vue (v2 y v3) para incluir la opción `StrategyQuant X` (ID `'SQX'`) y mostrar el icono `ph-cpu` correspondiente.
- Ejecutada la instrucción DDL `ALTER TYPE echo.platform_type_enum ADD VALUE 'SQX'` en la base de datos de desarrollo mediante MCP `postgres_echo_mcp_readwrite`.

## Validación

- La base de datos de desarrollo fue actualizada exitosamente y la consulta a `enum_range` confirma que el nuevo valor es parte del tipo enumerado.

---
type: agent_memory
schema_version: 1
scope: project
created: 2026-07-05
updated: 2026-08-11
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[Echo]]"
related:
  - "[[agent-constitution]]"
aliases:
  - prod database ddl and mcp alignment
confidence: verified
load_policy: manual
indexable: false
index_priority: low
tags:
  - agent/internal
  - kind/agent-memory
  - scope/project
  - project/agents-os
---

# Prod Database DDL & MCP Alignment

## Continuidad

## Contexto
- El MCP `postgres_echo_mcp_readwrite` apunta a la base de datos `echo_mcp` (usada para queries MCP o aislamiento), no a la base de datos real de producción `echo` de la aplicación.
- La base de datos de producción real se llama `echo` y corre en `192.168.31.220:5432`.
- El entorno local (host Mac) tiene conectividad directa al puerto Postgres de `192.168.31.220`.

## Procedimiento para DDLs / Migraciones en Producción
Para aplicar de manera segura un cambio de base de datos en producción sin depender de `psql` (que no está instalado localmente en Mac ni en el host remoto del core `192.168.31.71`):

1. **Crear archivo SQL temporal**: Crear un archivo `.sql` en `v3/sdk/postgres/migrations/` (ej: `999_temp_migration.up.sql`).
2. **Ejecutar a través del toolkit**: Correr el ejecutable local del toolkit `apply-migration` especificando las variables de entorno de producción:
   ```bash
   PGHOST=192.168.31.220 \
   PGPORT=5432 \
   PGDATABASE=echo \
   PGUSER=echo_user \
   PGPASSWORD=<secret-ref:echo-prod-postgres> \
   PGSSLMODE=disable \
   ./bin/toolkit/apply-migration --migration=999_temp_migration.up.sql
   ```
3. **Limpieza**: Eliminar el archivo SQL temporal de la máquina local tras validar la ejecución.

## Señales de carga

- Cargar manualmente sólo al ejecutar o revisar DDLs de la base productiva Echo.
- El locator `echo-prod-postgres` es independiente del acceso a workers; no asumir que comparte valor sin verificación explícita.

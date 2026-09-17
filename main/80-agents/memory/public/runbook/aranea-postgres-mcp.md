---
type: runbook
schema_version: 1
scope: area
created: "2026-09-11"
updated: "2026-09-11"
area: "[[Aranea]]"
project: "[[AGENT-PLATFORM - MCP Access Plane]]"
application:
entities:
  - "[[Aranea]]"
  - "[[Echo]]"
related:
  - "[[aranea-mcps-expert]]"
  - "[[aranea-mcp-capability-plane]]"
  - "[[aranea-ssh-mcp]]"
  - "[[aranea-mongodb-mcp]]"
aliases:
  - runbook PostgreSQL MCP Aranea
  - aranea-postgres
  - mcp postgres
confidence: verified
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/area
  - area/aranea
  - tech/mcp
  - tech/postgresql
  - action/mcp-postgres
---

# aranea-postgres-mcp

## Propósito

Operar PostgreSQL de Echo mediante dos capabilities con ambientes distintos. La selección de ambiente/capability pertenece a [[aranea-mcps-expert]]; este runbook posee la mecánica y los hechos operativos de PostgreSQL MCP.

## Contrato verificado

| Capability | Endpoint | Ambiente | Database | Rol observado | Authority |
|---|---|---|---|---|---|
| `aranea-postgres-ro` | `http://mcps.lab.aranea.cl:3001/mcp` | PROD | `echo` | `mcp_echo_prod_ro` | read-only |
| `aranea-postgres-rw` | `http://mcps.lab.aranea.cl:3002/mcp` | DEV | `echo-develop` | `mcp_echo_dev_rw` | read/write |

Verificado físicamente el 2026-09-11: PROD puede leer tablas `echo.*` y no posee INSERT/UPDATE/DELETE/TRUNCATE; DEV ejecutó lectura y un probe DDL/DML temporal con rollback. `SUPERUSER`, `CREATEDB` y `CREATEROLE` no forman parte del contrato normal del MCP DEV.

## Precondiciones

- El target es Aranea, no MELI/corporativo.
- Elegir ambiente antes de capability: PROD→RO, DEV→RW.
- La capability aparece conectada en el cliente.
- No pedir, imprimir ni persistir passwords/bearers.

## Procedimiento

1. **Fijar ambiente.** Para evidencia productiva usar `aranea-postgres-ro`. Para cualquier lectura o mutación de `echo-develop` usar `aranea-postgres-rw`; usar RW para una lectura DEV no obliga a mutar.
2. **Validar identidad cuando haya duda de routing.** Ejecutar `SELECT current_user, current_database(), current_setting('server_version');`. PROD esperado: `mcp_echo_prod_ro / echo`. DEV esperado: `mcp_echo_dev_rw / echo-develop`.
3. **Acotar queries.** Preferir columnas/predicados/counts/agregados específicos; usar `LIMIT` en exploración cuando no cambie la semántica. Preferir `EXPLAIN` a `EXPLAIN ANALYZE` salvo ejecución real intencionada y segura.
4. **Gate de mutación DEV.** Identificar target exacto en DEV, fijar blast radius y post-condición, ejecutar con `aranea-postgres-rw` y verificar nuevamente en DEV. No verificar una mutación DEV consultando PROD.
5. **Pruebas reversibles.** Para certificar RW usar transacción/tabla temporal/rollback cuando sea posible. No crear databases/roles ni exigir privilegios de cluster como smoke normal.
6. **No inferir éxito por envelope.** Si el contenido devuelve `Error validating query`, `permission denied`, timeout u otro error textual, tratarlo como fallo aunque MCP reporte `isError=false`.
7. **Enrutar fallos.** Capability ausente/`401`/handshake → [[aranea-mcp-capability-plane]]. Permission denied en PROD para escritura es boundary esperado. Timeout → estrechar/optimizar. No degradar a `psql` agent-first si MCP cubre la acción.

## Runtime desplegado

En host `mcps`, el backend PostgreSQL MCP usa `local/postgres-mcp:0.3.0-15c8e33` y una conexión fija por proceso. No asumir selección dinámica de database por llamada. Los proxies autenticados externos permanecen en 3001/3002; no crear profiles/sandboxes/endpoints adicionales como workaround automático.

La configuración de secrets/runtime del host vive bajo `/opt/mcp/postgres/runtime/`; documentar paths y nombres, nunca contenido secreto.

## Validación

```text
PROD RO: current_user=mcp_echo_prod_ro current_database=echo
DEV RW:  current_user=mcp_echo_dev_rw  current_database=echo-develop
Environment match: PASS
Mutation verification: same environment
Cluster-admin privileges required: no
Secrets exposed: no
```

## Rollback / recuperación

Ante routing incorrecto, no mutar. Confirmar `current_user/current_database`, aislar si el fallo es cliente/proxy/backend y corregir el plano MCP. No ampliar privilegios ni crear infraestructura auxiliar para satisfacer un test que contradice este contrato.

## Evidencia

Reportar capability, ambiente, database, identidad observada, operación, resultado material, mutación/post-check y boundary si aplica.

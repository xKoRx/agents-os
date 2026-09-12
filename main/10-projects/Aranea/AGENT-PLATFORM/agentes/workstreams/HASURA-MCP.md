---
type: note
status: done
area: "[[Aranea]]"
parent: "[[AGENT-PLATFORM - MCP Access Plane]]"
created: "2026-09-12"
updated: "2026-09-12"
tags:
  - area/aranea
  - tech/mcp
  - tech/hasura
---

# HASURA MCP — workstream del MCP Access Plane

> Componente del proyecto [[AGENT-PLATFORM - MCP Access Plane]]. **No es un proyecto paralelo.**
>
> Deployment obligatorio: [[AGENT-PLATFORM - MCP Access Plane - Architecture]]. Operación mecánica: [[aranea-hasura-mcp]].

## Objetivo

Materializar dos capabilities MCP sobre el **admin/control plane de Hasura**:

- `aranea-hasura-prod-ro`: PROD estrictamente read-only para inspección administrativa.
- `aranea-hasura-dev-admin`: DEV con autoridad administrativa Hasura.

Apollo MCP queda descartado para este workstream: cubre GraphQL data-plane, pero no metadata/DDL/`run_sql`. El CRUD de datos ya tiene PostgreSQL MCP/direct data-plane propio.

## Veredicto — PASS / CLOSED

Ambas capabilities quedaron desplegadas y certificadas end-to-end desde Cursor el 2026-09-12.

```text
DEV  aranea-hasura-dev-admin  -> http://mcps.lab.aranea.cl:3006/mcp -> PASS / CLOSED
PROD aranea-hasura-prod-ro     -> http://mcps.lab.aranea.cl:3005/mcp -> PASS / CLOSED
```

## DEV — PASS / CLOSED

Target real:

```text
Hasura DEV: 192.168.31.75:8080
host: docker-echo-dev
engine: Hasura GraphQL Engine CE v2.38.0
metadata DB: hasura_dev_metadata
```

Path:

```text
Cursor / Daedalus
  -> bearer por capability
  -> http://mcps.lab.aranea.cl:3006/mcp
  -> Nginx auth proxy
  -> backend Hasura MCP interno
  -> stdio->Streamable HTTP wrapper
  -> Hasura DEV :8080
```

Evidencia material:

- `mcps` alcanza `/v1/version` DEV con `HTTP 200`;
- `/v1/metadata` sin admin secret → `401`;
- backend MCP sin host port;
- request MCP sin bearer a `:3006/mcp` → `401`;
- `initialize` autenticado → `HTTP 200` + session id;
- `tools/list` → 9 tools administrativas;
- Daedalus → endpoint MCP → `HTTP 200`;
- Cursor real → `get_version`: Hasura CE `v2.38.0`;
- Cursor real → `get_inconsistent_metadata`: metadata consistente;
- capability vista por Cursor: `user-aranea-hasura-dev-admin`.

Tool surface DEV certificada:

```text
apply_metadata
clear_metadata
drop_inconsistent_metadata
export_metadata
get_inconsistent_metadata
get_schema
get_version
reload_metadata
run_sql
```

Cliente Daedalus:

```text
secret file: ~/.config/aranea/secrets/ARANEA_HASURA_MCP_DEV_ADMIN_BEARER
mode: 0600
env: ARANEA_HASURA_MCP_DEV_ADMIN_BEARER
```

Cursor referencia la env var; no contiene bearer literal.

## PROD — PASS / CLOSED

Target real:

```text
Hasura PROD: 192.168.31.48:8080
host: docker-hasura
engine: Hasura GraphQL Engine CE v2.38.0
metadata DB: hasura_metadata
```

Path:

```text
Cursor / Daedalus
  -> bearer por capability
  -> http://mcps.lab.aranea.cl:3005/mcp
  -> Nginx auth proxy
  -> strict-RO Hasura MCP interno
  -> stdio->Streamable HTTP wrapper
  -> Hasura PROD :8080
```

### Hardening PROD aplicado

El flag upstream `--read-only` no se aceptó como boundary suficiente porque mantenía `reload_metadata` y `run_sql` registrados.

Se construyó una variante Aranea desde el mismo commit pinneado que elimina ambas tools de la superficie PROD y además ejecuta el servidor con `--read-only`, impidiendo que se registren los mutadores de metadata upstream.

Artefactos:

```text
base: local/hasura-mcp:1.0.0-9ba59f2-prod-ro
base image id: sha256:36efa1aef5ceb428446fb6670159a8e2eb1d5c12eb45314f299119cb723b02c6
http: local/hasura-mcp-http:1.0.0-9ba59f2-prod-ro-mcpproxy6.7.16
http image id: sha256:d36ac06076a6272f3527e41de36540f51217808b143a694211f4cab8b20e076c
architecture: amd64
```

Tool surface PROD certificada server-side — exactamente 4:

```text
export_metadata
get_inconsistent_metadata
get_schema
get_version
```

Ausentes por diseño:

```text
apply_metadata
clear_metadata
drop_inconsistent_metadata
reload_metadata
run_sql
```

Esto elimina el camino MCP para metadata mutation, DDL, DML, views/functions y cualquier `run_sql` productivo.

Evidencia material:

- request sin bearer a `:3005/mcp` → `401`;
- `initialize` autenticado → `HTTP 200` + session id;
- `tools/list` server-side → exactamente las 4 tools RO;
- backend MCP sin host port;
- Cursor real → `get_version`: Hasura CE `v2.38.0`;
- Cursor real → `get_inconsistent_metadata`: metadata consistente;
- capability vista por Cursor: `user-aranea-hasura-prod-ro`.

Cursor también reportó `mcp_auth` en el inventario cliente. No apareció en `tools/list` server-side; por tanto no forma parte de la superficie Hasura PROD certificada ni amplía su autoridad.

Cliente Daedalus:

```text
secret file: ~/.config/aranea/secrets/ARANEA_HASURA_MCP_PROD_RO_BEARER
mode: 0600
env: ARANEA_HASURA_MCP_PROD_RO_BEARER
```

Cursor referencia la env var; no contiene bearer literal.

## Backend MCP adoptado

Source: `sanjay3290/graphql-engine`, implementación MCP bajo `cli/cmd/mcp-server/`.

Commit pinneado:

```text
9ba59f273daf42205919e6d43e27d2876a6e0b32
```

Base DEV local:

```text
local/hasura-mcp:1.0.0-9ba59f2
architecture: amd64
```

La imagen publicada `sanjay3290/hasura-mcp:1.0.0` no ofrecía manifest `linux/amd64`; se descartó y se construyó localmente desde source pinneado.

El upstream es stdio-only. Aranea usa `mcp-proxy` `6.7.16` para exponer Streamable HTTP interno; Nginx sigue siendo el único listener host-facing, coherente con el access plane.

## Arquitectura y secretos

Invariantes cerrados:

1. bearer cliente→MCP separado del Hasura admin secret;
2. admin secret nunca se entrega a Cursor/Daedalus/agente;
3. backend MCP no publica host port;
4. Nginx auth proxy es el único puerto publicado;
5. secretos montados server-side read-only;
6. imágenes/source/versiones pinneadas;
7. `mcps` es appliance Docker/Portainer, no workstation/jump host;
8. PROD no expone `run_sql` ni metadata mutation;
9. tool surface server-side es parte del contrato de autoridad y debe conservarse ante upgrades.

Transferencias puntuales de secrets pueden usar Daedalus como bridge, sin imprimir valores y eliminando copias intermedias cuando corresponda.

## Operación futura

La mecánica queda en [[aranea-hasura-mcp]]. Cualquier upgrade/rebuild debe preservar:

```text
PROD tools = export_metadata,get_inconsistent_metadata,get_schema,get_version
DEV tools  = apply_metadata,clear_metadata,drop_inconsistent_metadata,export_metadata,get_inconsistent_metadata,get_schema,get_version,reload_metadata,run_sql
```

Si una versión futura cambia el upstream o la tool surface, reabrir este workstream sólo por drift material; no redescubrir la arquitectura completa.

## Veredicto final

- DEV: `PASS / CLOSED`.
- PROD: `PASS / CLOSED`.
- Workstream Hasura MCP: `PASS / CLOSED`.

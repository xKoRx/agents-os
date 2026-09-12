---
type: runbook
schema_version: 1
scope: area
created: "2026-09-12"
updated: "2026-09-12"
area: "[[Aranea]]"
project: "[[AGENT-PLATFORM - MCP Access Plane]]"
entities:
  - "[[Aranea]]"
related:
  - "[[aranea-mcps-expert]]"
  - "[[AGENT-PLATFORM - MCP Access Plane - Architecture]]"
  - "[[HASURA MCP — workstream del MCP Access Plane]]"
aliases:
  - aranea hasura mcp
  - runbook Hasura MCP Aranea
confidence: verified
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/area
  - area/aranea
  - tech/mcp
  - tech/hasura
---

# aranea-hasura-mcp

## Propósito

Operar y diagnosticar las capabilities Hasura del MCP Access Plane de Aranea sin repartir el Hasura admin secret a los clientes. El routing agent-facing vive en [[aranea-mcps-expert]] y la topología común en [[AGENT-PLATFORM - MCP Access Plane - Architecture]].

## Capabilities

| Ambiente | Capability | Endpoint | Autoridad | Estado |
|---|---|---|---|---|
| DEV | `aranea-hasura-dev-admin` | `http://mcps.lab.aranea.cl:3006/mcp` | administración Hasura | PASS end-to-end |
| PROD | `aranea-hasura-prod-ro` | `http://mcps.lab.aranea.cl:3005/mcp` | inspección estrictamente read-only | pendiente de materializar/certificar |

## Runtime Hasura verificado

### PROD

- Host actual: `192.168.31.48` (`docker-hasura`).
- Hasura GraphQL Engine CE `v2.38.0`.
- Container: `hasura-graphql`.
- Endpoint: `http://192.168.31.48:8080`.
- Metadata DB: `hasura_metadata`.
- `/v1/version` responde `200` desde `mcps`.
- `/v1/metadata` sin admin secret responde `401`.
- Admin secret existe en el runtime Hasura; su valor no se registra aquí.

### DEV

- Host actual: `192.168.31.75` (`docker-echo-dev`).
- Hasura GraphQL Engine CE `v2.38.0`.
- Container: `hasura-graphql`.
- Endpoint: `http://192.168.31.75:8080`.
- Metadata DB: `hasura_dev_metadata`.
- `/v1/version` responde `200` desde `mcps`.
- `/v1/metadata` sin admin secret responde `401`.
- Admin secret existe en el runtime Hasura; su valor no se registra aquí.

## Backend MCP adoptado

Source: fork `sanjay3290/graphql-engine`, MCP bajo `cli/cmd/mcp-server/`.

Commit pinneado:

```text
9ba59f273daf42205919e6d43e27d2876a6e0b32
```

Imagen local base verificada en `mcps`:

```text
local/hasura-mcp:1.0.0-9ba59f2
```

Build local `linux/amd64`; no usar la imagen publicada `sanjay3290/hasura-mcp:1.0.0` porque durante la instalación no ofrecía manifest `linux/amd64`.

El upstream es stdio-only. En Aranea se envuelve con `mcp-proxy` pinneado para exponer Streamable HTTP interno, manteniendo Nginx bearer como único puerto host-facing.

## DEV — deployment certificado

Topología:

```text
Cursor / Daedalus
  -> Authorization: Bearer capability token
  -> mcps.lab.aranea.cl:3006/mcp
  -> Nginx auth proxy
  -> hasura-mcp-dev-admin:8000/mcp
  -> stdio Hasura MCP
  -> http://192.168.31.75:8080
```

Invariantes:

- backend MCP sin host port;
- bearer cliente→MCP vive sólo en proxy/cliente;
- Hasura admin secret vive server-side en `mcps` y se monta read-only al backend;
- `restart=unless-stopped`;
- red Docker privada `mcp-hasura`;
- no persistir valores de secrets en Agents-OS, Cursor JSON, prompts ni logs.

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

Certificación material DEV:

- request sin bearer a `:3006/mcp` → `401`;
- `initialize` autenticado → `HTTP 200` + MCP session id;
- `tools/list` → 9 tools anteriores;
- Daedalus → `mcps.lab.aranea.cl:3006/mcp` → `HTTP 200`;
- Cursor real → `get_version` devuelve Hasura CE `v2.38.0`;
- Cursor real → `get_inconsistent_metadata` confirma metadata consistente;
- capability reportada por Cursor: `user-aranea-hasura-dev-admin`.

Cliente Daedalus:

- secret file: `~/.config/aranea/secrets/ARANEA_HASURA_MCP_DEV_ADMIN_BEARER` mode `0600`;
- env: `ARANEA_HASURA_MCP_DEV_ADMIN_BEARER` cargada desde `.zshenv`;
- Cursor referencia `${env:ARANEA_HASURA_MCP_DEV_ADMIN_BEARER}`; nunca contiene el bearer literal.

## PROD RO — boundary obligatorio

El modo `--read-only` upstream **no se considera suficiente por sí solo**.

Source audit verificado:

- oculta `apply_metadata`, `clear_metadata` y `drop_inconsistent_metadata` cuando `ReadOnly=true`;
- mantiene `reload_metadata` expuesto;
- mantiene `run_sql` expuesto y confía en el flag `read_only` del request/Hasura;
- por tanto no cumple todavía el contrato Aranea de PROD estrictamente read-only por tool surface.

Antes de cerrar `aranea-hasura-prod-ro`, el backend PROD debe exponer únicamente operaciones de inspección que no puedan mutar metadata/cache/datos. Como mínimo, la certificación debe demostrar tool surface reducida y negative tests para metadata writes, DDL y DML.

## Operación

### Elegir capability

- inspección/admin DEV → `aranea-hasura-dev-admin`;
- inspección PROD → `aranea-hasura-prod-ro` una vez certificado;
- nunca usar DEV para inferir estado PROD ni usar PROD como workaround para una tarea DEV.

### DEV mutation discipline

Antes de una mutación:

1. identificar objeto exacto y estado actual;
2. declarar cambio y post-condición;
3. aplicar sólo la mutación necesaria;
4. verificar metadata consistente y objeto final en DEV;
5. no promover cambios a PROD desde el MCP por accidente.

### Troubleshooting

- capability ausente → revisar env/handshake según [[aranea-mcp-capability-plane]];
- `401` → bearer cliente→proxy; no tocar admin secret;
- handshake MCP falla con backend Up → revisar wrapper stdio→HTTP y logs del backend;
- `get_version` falla pero handshake pasa → revisar reachability `mcps` → Hasura target;
- tool esperada ausente → comparar `tools/list` con este runbook antes de cambiar policy.

## Hard Rules

- `mcps` es appliance de servicios MCP Docker/Portainer, no workstation/jump host: no instalar ni depender de `psql`, `mongosh`, Hasura CLI u otros clientes ad-hoc en el host.
- No entregar Hasura admin secret a Cursor/Daedalus/agente.
- No publicar backend Hasura MCP directamente al host.
- No usar Docker image `latest` ni artefactos no pinneados.
- No confiar en nombre de container, README o flag `--read-only` como prueba de autoridad; certificar tool surface y negative tests.
- Si hay que transferir un secret hacia `mcps`, usar un bridge temporal controlado sin imprimir el valor y eliminar copias intermedias cuando corresponda.

## Validación

```text
Environment: DEV|PROD
Capability: aranea-hasura-*
Hasura target: host:port + version
Proxy auth: 401 unauthenticated
MCP initialize: PASS
Tools surface: expected
Backend host port: none
Upstream secret exposed to client: no
Metadata consistency: PASS when applicable
Mutation authority: matches environment contract
```

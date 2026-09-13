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

## Capabilities certificadas

| Ambiente | Capability | Endpoint | Autoridad | Estado |
|---|---|---|---|---|
| DEV | `aranea-hasura-dev-admin` | `http://mcps.lab.aranea.cl:3006/mcp` | administración Hasura | PASS / CLOSED end-to-end |
| PROD | `aranea-hasura-prod-ro` | `http://mcps.lab.aranea.cl:3005/mcp` | inspección estrictamente read-only | PASS / CLOSED end-to-end |

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

Base DEV verificada:

```text
local/hasura-mcp:1.0.0-9ba59f2
linux/amd64
```

La imagen publicada `sanjay3290/hasura-mcp:1.0.0` no ofrecía manifest `linux/amd64` durante la instalación; Aranea construye localmente desde source pinneado.

El upstream es stdio-only. Aranea lo envuelve con `mcp-proxy` `6.7.16` para exponer Streamable HTTP interno; Nginx bearer sigue siendo el único listener host-facing.

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

Containers:

```text
hasura-mcp-dev-admin
hasura-mcp-auth-dev-admin
```

Tool surface DEV certificada server-side:

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

```text
secret file: ~/.config/aranea/secrets/ARANEA_HASURA_MCP_DEV_ADMIN_BEARER
env: ARANEA_HASURA_MCP_DEV_ADMIN_BEARER
mode: 0600
```

Cursor referencia `${env:ARANEA_HASURA_MCP_DEV_ADMIN_BEARER}`; nunca contiene el bearer literal.

## PROD RO — deployment certificado

El `--read-only` upstream no se aceptó como boundary suficiente porque mantenía `reload_metadata` y `run_sql` registrados. Se construyó una variante Aranea que elimina ambas tools de la superficie y ejecuta además el servidor con `--read-only`, por lo que los mutadores de metadata upstream tampoco se registran.

Artefactos PROD RO:

```text
base: local/hasura-mcp:1.0.0-9ba59f2-prod-ro
base image id: sha256:36efa1aef5ceb428446fb6670159a8e2eb1d5c12eb45314f299119cb723b02c6
http: local/hasura-mcp-http:1.0.0-9ba59f2-prod-ro-mcpproxy6.7.16
http image id: sha256:d36ac06076a6272f3527e41de36540f51217808b143a694211f4cab8b20e076c
architecture: amd64
```

Topología:

```text
Cursor / Daedalus
  -> Authorization: Bearer capability token
  -> mcps.lab.aranea.cl:3005/mcp
  -> Nginx auth proxy
  -> hasura-mcp-prod-ro:8000/mcp
  -> strict-RO Hasura MCP
  -> http://192.168.31.48:8080
```

Containers:

```text
hasura-mcp-prod-ro
hasura-mcp-auth-prod-ro
```

Tool surface PROD certificada server-side — exactamente 4:

```text
export_metadata
get_inconsistent_metadata
get_schema
get_version
```

No existen en la superficie PROD:

```text
apply_metadata
clear_metadata
drop_inconsistent_metadata
reload_metadata
run_sql
```

Por construcción no existe tool SQL en PROD, por lo que DDL/DML/creación de views/functions no tienen camino MCP. Metadata mutation tampoco tiene tool registrada.

Certificación material PROD:

- request sin bearer a `:3005/mcp` → `401`;
- `initialize` autenticado → `HTTP 200` + MCP session id;
- `tools/list` server-side → exactamente las 4 tools RO anteriores;
- backend MCP sin host port;
- Cursor real → `get_version`: Hasura CE `v2.38.0`;
- Cursor real → `get_inconsistent_metadata`: metadata consistente;
- capability reportada por Cursor: `user-aranea-hasura-prod-ro`.

Cursor también reportó `mcp_auth` en su inventario cliente. Esa entrada no apareció en `tools/list` server-side del backend PROD, que fue certificado con exactamente 4 tools Hasura; por tanto `mcp_auth` no se considera parte de la superficie Hasura ni amplía la autoridad upstream.

Cliente Daedalus:

```text
secret file: ~/.config/aranea/secrets/ARANEA_HASURA_MCP_PROD_RO_BEARER
env: ARANEA_HASURA_MCP_PROD_RO_BEARER
mode: 0600
```

Cursor referencia `${env:ARANEA_HASURA_MCP_PROD_RO_BEARER}`; nunca contiene bearer literal.

## Invariantes de deployment

- backend MCP sin host port;
- bearer cliente→MCP vive sólo en proxy/cliente;
- Hasura admin secret vive server-side en `mcps` y se monta read-only al backend;
- `restart=unless-stopped`;
- red Docker privada `mcp-hasura`;
- Nginx canónico es el único container que publica `3005`/`3006`;
- no persistir valores de secrets en Agents-OS, Cursor JSON, prompts ni logs;
- `mcps` es appliance Docker/Portainer, no workstation/jump host.

## Operación

### Elegir capability

- inspección administrativa PROD → `aranea-hasura-prod-ro`;
- inspección o administración DEV → `aranea-hasura-dev-admin`;
- CRUD de datos genérico → preferir PostgreSQL MCP, no Hasura admin MCP;
- nunca usar DEV para inferir estado PROD ni usar PROD como workaround para una tarea DEV.

### PROD discipline

En PROD sólo son válidas operaciones cubiertas por las 4 tools certificadas. Si una tarea exige SQL, metadata mutation, reload o cualquier cambio, detenerse: esa autoridad no existe en `aranea-hasura-prod-ro` y no debe abrirse dinámicamente como workaround.

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
- tool esperada ausente/sobrante → comparar `tools/list` server-side con este runbook antes de cambiar policy;
- `mcp_auth` visible sólo en cliente no cuenta como tool Hasura mientras no aparezca en `tools/list` server-side.

## Hard Rules

- `mcps` es appliance de servicios MCP Docker/Portainer, no workstation/jump host: no instalar ni depender de `psql`, `mongosh`, Hasura CLI u otros clientes ad-hoc en el host.
- No entregar Hasura admin secret a Cursor/Daedalus/agente.
- No publicar backend Hasura MCP directamente al host.
- No usar Docker image `latest` ni artefactos no pinneados.
- No confiar en nombre de container, README o flag `--read-only` como prueba de autoridad; `tools/list` server-side es evidencia material.
- PROD no expone `run_sql`: no agregarlo sólo para una tarea puntual.
- Si hay que transferir un secret hacia `mcps`, usar un bridge temporal controlado sin imprimir el valor y eliminar copias intermedias cuando corresponda.

## Validación

```text
Environment: DEV|PROD
Capability: aranea-hasura-*
Hasura target: host:port + version
Proxy auth: 401 unauthenticated
MCP initialize: PASS
Tools surface: expected exact set
Backend host port: none
Upstream secret exposed to client: no
Metadata consistency: PASS when applicable
Mutation authority: matches environment contract
```

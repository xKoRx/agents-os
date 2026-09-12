---
type: note
status: active
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

## Estado actual — 2026-09-12

### DEV — PASS / CLOSED

`aranea-hasura-dev-admin` está desplegado y certificado end-to-end.

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

### PROD — NEXT

Target real:

```text
Hasura PROD: 192.168.31.48:8080
host: docker-hasura
engine: Hasura GraphQL Engine CE v2.38.0
metadata DB: hasura_metadata
```

`mcps` alcanza `/v1/version` PROD con `HTTP 200`; `/v1/metadata` sin admin secret → `401`.

Puerto objetivo:

```text
http://mcps.lab.aranea.cl:3005/mcp
```

Aún no desplegado/certificado.

## Backend MCP adoptado

Source: `sanjay3290/graphql-engine`, implementación MCP bajo `cli/cmd/mcp-server/`.

Commit pinneado:

```text
9ba59f273daf42205919e6d43e27d2876a6e0b32
```

Imagen base local construida en `mcps`:

```text
local/hasura-mcp:1.0.0-9ba59f2
architecture: amd64
```

La imagen publicada `sanjay3290/hasura-mcp:1.0.0` no ofrecía manifest `linux/amd64`; se descartó y se construyó localmente desde source pinneado.

El upstream es stdio-only. DEV usa wrapper pinneado `mcp-proxy` para exponer Streamable HTTP interno; Nginx sigue siendo el único listener host-facing, coherente con el access plane.

## Auditoría de seguridad — PROD RO

El flag upstream `--read-only` **no es suficiente como autoridad Aranea**.

Source audit:

- oculta `apply_metadata`, `clear_metadata` y `drop_inconsistent_metadata` cuando `ReadOnly=true`;
- mantiene `reload_metadata` registrado;
- mantiene `run_sql` registrado y delega read-only al flag/request Hasura;
- por tanto la superficie no satisface todavía PROD estrictamente read-only.

### Contrato PROD obligatorio

Debe permitir sólo inspección:

- `export_metadata`;
- `get_inconsistent_metadata`;
- `get_version`;
- `get_schema`;
- opcionalmente SQL diagnóstico únicamente si el boundary demuestra que no puede ejecutar DDL/DML bajo ninguna entrada.

Debe impedir por tool surface/policy:

- `apply_metadata`;
- `clear_metadata`;
- `drop_inconsistent_metadata`;
- `reload_metadata` si se mantiene criterio de cero mutación administrativa;
- DDL/DML;
- creación/modificación de views/functions;
- cambios de relationships/permissions/triggers/actions/remotes.

No cerrar PROD por nombre del container, README ni `--read-only`; requiere `tools/list` y negative tests reales.

## Arquitectura y secretos

Invariantes:

1. bearer cliente→MCP separado del Hasura admin secret;
2. admin secret nunca se entrega a Cursor/Daedalus/agente;
3. backend MCP no publica host port;
4. Nginx auth proxy es el único puerto publicado;
5. secretos montados server-side read-only;
6. imágenes/source/versiones pinneadas;
7. `mcps` es appliance Docker/Portainer, no workstation/jump host; no instalar clientes ad-hoc como `psql`, `mongosh` o Hasura CLI.

Transferencias puntuales de secrets pueden usar Daedalus como bridge, sin imprimir valores y eliminando copias intermedias cuando corresponda.

## Próximo gate

Construir/materializar `aranea-hasura-prod-ro` en `:3005` con superficie realmente RO y certificar:

```text
unauthenticated -> 401
initialize authenticated -> PASS
tools/list -> sólo tools RO aprobadas
backend host port -> none
metadata mutation -> impossible/denied
DDL -> denied
DML -> denied
Cursor real -> get_version/export_metadata/get_inconsistent_metadata PASS
```

## Veredicto

- DEV: `PASS / CLOSED`.
- PROD: `NEXT`, bloqueado sólo por hardening/certificación del boundary RO; runtime, reachability, source y arquitectura ya están resueltos.

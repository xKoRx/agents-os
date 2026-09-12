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

## Objetivo

Materializar dos capabilities MCP separados sobre Hasura, manteniendo monotonicidad de autoridad en cada capa:

- `aranea-hasura-prod-ro`: PROD estrictamente read-only.
- `aranea-hasura-dev-rw`: DEV read/write limitado al GraphQL data-plane.

Fuera de scope: metadata management, migrations, DDL, `run_sql`, administración Hasura, Actions/Remote Schemas/Event Triggers y cambios de permisos.

## Estado — discovery 2026-09-12

- El access plane existente corre en el LXC dedicado `mcps`; `mcps.lab.aranea.cl` es el endpoint estable. Los capabilities actuales ocupan `3000`–`3004`. **No se reservan 3005/3006 hasta inspeccionar binds/runtime reales.**
- Echo versiona metadata Hasura bajo `xKoRx/echo/v2/hasura`.
- `v2/hasura/config.yaml` apunta a `http://hasura.lab.aranea.cl:8080`; se trata como pista de PROD hasta verificar runtime vivo.
- El mismo archivo contiene un `admin_secret` en texto plano. Valor deliberadamente no registrado aquí. Debe considerarse comprometido, rotarse y eliminarse del repo/historial operativo antes de usar este carril como authority source.
- Metadata inspeccionada muestra roles `admin` y `user` en tablas trackeadas; no se encontró un rol MCP dedicado. `admin` es demasiado amplio y `user` no demuestra el scope requerido.
- DEV no tiene todavía host/port/GraphQL endpoint/version/auth mode demostrado desde source disponible. La existencia conocida de `hasura_dev_metadata` no autoriza inferir esos datos.
- Auth runtime PROD/DEV (JWT, webhook, unauthorized role u otro) sigue sin evidencia suficiente. El admin secret no será usado como credencial upstream del agente.

## Decisión candidata — pendiente de gate runtime

Preferir un MCP GraphQL genérico/GraphQL-native sobre un MCP administrativo de Hasura.

Candidato principal: **Apollo MCP Server**, pinneado por release/artefacto después de verificar el target Linux y digest. Motivos:

- Streamable HTTP.
- Queries/introspection GraphQL sin exponer metadata API ni `run_sql`.
- PROD puede usar `mutation_mode: none` como barrera estructural adicional.
- DEV puede usar `mutation_mode: explicit` para exponer sólo mutations predefinidas, evitando ad-hoc mutations por defecto.
- La seguridad efectiva sigue descansando en una credencial upstream no-admin + permisos Hasura del rol dedicado.

Descartado como default para este workstream: `sanjay3290/hasura-mcp-server`, porque su superficie incluye metadata management y `run_sql`; su `--read-only` documentado no reduce suficientemente el boundary requerido.

## Boundary target

### PROD

- Client → MCP: bearer exclusivo `ARANEA_HASURA_MCP_PROD_RO_BEARER` (nombre candidato, pendiente de freeze final).
- MCP → Hasura: token/credencial de servicio no-admin que resuelva exclusivamente a `mcp_prod_ro`.
- Hasura role `mcp_prod_ro`: `select` explícito sólo sobre tablas/vistas necesarias; sin insert/update/delete.
- MCP: query/introspection; mutations estructuralmente disabled.
- Metadata API, `run_sql`, DDL, migrations y admin tools: inexistentes en tool surface.

### DEV

- Client → MCP: bearer exclusivo `ARANEA_HASURA_MCP_DEV_RW_BEARER` (nombre candidato, pendiente de freeze final).
- MCP → Hasura: token/credencial de servicio no-admin que resuelva exclusivamente a `mcp_dev_rw`.
- Hasura role `mcp_dev_rw`: CRUD explícito sólo sobre entidades aprobadas.
- MCP: queries/introspection + mutations predefinidas (`explicit`) como default inicial; ampliar sólo con evidencia de necesidad.
- Metadata API, `run_sql`, DDL, migrations y admin tools: inexistentes en tool surface.

## Gates antes de instalar

1. Verificar runtime vivo de Hasura PROD y DEV: host, port, version, `/v1/graphql`, metadata DB y ubicación del deployment.
2. Verificar auth real de ambas instancias y demostrar cómo emitir/obtener una credencial de servicio no-admin con rol fijo.
3. Inventariar schema/tablas/vistas/functions expuestos y congelar permisos mínimos de `mcp_prod_ro` / `mcp_dev_rw`.
4. Inspeccionar binds/compose efectivos en `mcps` y sólo entonces reservar puertos nuevos.
5. Verificar Apollo MCP Server release/artefacto exacto, config efectiva, tool surface y digest; no `latest`.
6. Diseñar fixtures seguros para los gates PROD query/mutation-denied y DEV controlled-mutation.
7. Rotar/eliminar la credencial Hasura expuesta en `xKoRx/echo/v2/hasura/config.yaml` sin registrar el valor en Agents-OS.

## Veredicto actual

`BLOCKED` para instalación. El diseño de boundary es viable, pero faltan autoridad upstream y runtime DEV/PROD demostrados. No avanzar a deployment ni Cursor config hasta cerrar esos gates.

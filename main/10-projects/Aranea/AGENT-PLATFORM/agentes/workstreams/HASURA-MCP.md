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
> Deployment obligatorio: [[AGENT-PLATFORM - MCP Access Plane - Architecture]]. No inventar una topología específica para Hasura.

## Objetivo actualizado

Materializar dos capabilities MCP sobre el **admin/control plane de Hasura**, no un wrapper GraphQL de data-plane:

- `aranea-hasura-prod-ro`: PROD estrictamente read-only para inspección administrativa.
- `aranea-hasura-dev-admin`: DEV con autoridad administrativa Hasura.

Necesidad owner explícita para DEV:

- crear/reemplazar vistas mediante SQL y trackearlas en Hasura;
- crear/actualizar relationships;
- administrar permissions;
- administrar Event Triggers/hooks;
- administrar Actions;
- administrar Remote Schemas;
- trackear/untrackear tables/views/functions;
- inspeccionar y resolver metadata inconsistente;
- ejecutar `run_sql` cuando la operación administrativa lo requiera.

**Apollo MCP queda descartado para este workstream**: sirve para GraphQL data-plane, pero no administra metadata ni DDL/`run_sql`. Para CRUD de datos ya existe acceso PostgreSQL directo y no se justifica introducir otra capability sólo para eso.

## Arquitectura obligatoria

Hasura debe reutilizar el blueprint canónico:

```text
Daedalus / agente
  -> bearer por capability
  -> mcps.lab.aranea.cl:<puerto>
  -> Nginx auth proxy
  -> backend Hasura MCP interno SIN host port
  -> Hasura destino
```

Secretos separados:

1. bearer cliente→MCP, montado sólo en el proxy;
2. Hasura admin secret/credencial upstream, montado sólo en el backend MCP.

El admin secret **nunca** va a Cursor, env del cliente, prompt ni documentación.

Puertos `3005` y `3006` estaban libres en discovery real del 2026-09-12, pero deben volver a verificarse antes de bindear. No se consideran reservados por documentación.

## Estado de discovery — 2026-09-12

### Access plane

- `mcps` confirmado como LXC Docker + Portainer.
- `3000`–`3004` ocupados por SSH, PostgreSQL RO/RW y Mongo Forge RO/RW.
- PostgreSQL y Mongo confirman el patrón proxy Nginx + backend interno + bearer separado.
- `docker compose ls` estaba vacío: el runtime actual usa containers standalone/Portainer con `restart=unless-stopped`.
- Arquitectura congelada en [[AGENT-PLATFORM - MCP Access Plane - Architecture]].

### Hasura runtime

- `hasura.lab.aranea.cl` **no resuelve actualmente** desde `mcps`; no usar ese hostname como autoridad viva.
- El checkout local consultado de Echo no entregó referencias runtime actuales útiles para PROD/DEV.
- La existencia histórica de `xKoRx/echo/v2/hasura` y de metadata DBs conocidas (`hasura_metadata`, `hasura_dev_metadata`) sirve sólo como pista; no autoriza inferir endpoints vivos.
- PROD y DEV siguen sin host/port/version/deployment demostrado.

### Credenciales históricas

- Existe un hallazgo previo de `admin_secret` versionado en configuración Hasura histórica de Echo. Su valor no se registra aquí.
- Antes de usar ese material como authority source hay que verificar si sigue vigente; si sigue siendo válido, debe rotarse y eliminarse del source operativo correspondiente.

## Candidato MCP administrativo

Candidato actual: implementación comunitaria `sanjay3290/hasura-mcp` / source mantenido en `sanjay3290/graphql-engine`, `cli/cmd/mcp-server/`.

Superficie documentada relevante:

- `export_metadata`
- `apply_metadata`
- `reload_metadata`
- `clear_metadata`
- `get_inconsistent_metadata`
- `drop_inconsistent_metadata`
- `run_sql`
- `get_version`
- `get_schema`

Modo `--read-only` documentado:

- deshabilita operaciones de metadata mutantes relevantes;
- fuerza `run_sql` a lectura.

Esto lo hace conceptualmente apto para `aranea-hasura-prod-ro`, **pero no se congela hasta auditar source y probar el boundary real**.

### Gap de transporte

El candidato está documentado como **stdio-only**. El MCP Access Plane de Aranea expone HTTP detrás de Nginx.

Por tanto, antes de instalar hay que resolver uno de estos caminos sin romper [[AGENT-PLATFORM - MCP Access Plane - Architecture]]:

1. demostrar que una versión actual soporta HTTP aunque la documentación inspeccionada no lo refleje;
2. usar un bridge stdio→Streamable HTTP mantenido y pinneable;
3. como último recurso, build/fork mínimo y reproducible que agregue transporte HTTP.

No usar stdio local en cada cliente ni repartir el Hasura admin secret a Daedalus como workaround.

## Boundary target

### PROD — `aranea-hasura-prod-ro`

Debe permitir:

- exportar/inspeccionar metadata;
- inspeccionar schema/version/inconsistencias;
- SQL diagnóstico estrictamente read-only;
- comprobar objetos/relationships/permissions/triggers/actions/remotes existentes.

Debe rechazar:

- `apply_metadata` mutante;
- clear/drop metadata;
- DDL;
- DML;
- creación/modificación de views/functions;
- cambios de relationships/permissions/triggers/actions/remotes.

La certificación exige negative tests reales; no basta confiar en `--read-only` o en el README.

### DEV — `aranea-hasura-dev-admin`

Debe permitir administración Hasura completa necesaria por el owner:

- `run_sql` para DDL/DML administrativas;
- `CREATE OR REPLACE VIEW` y funciones cuando proceda;
- track/untrack metadata;
- relationships;
- permissions;
- Event Triggers/hooks;
- Actions;
- Remote Schemas;
- resolución de metadata inconsistente.

El backend puede requerir Hasura admin secret upstream, pero éste queda server-side en `mcps` y separado del bearer de la capability.

## Gates antes de instalar

1. Identificar **runtime vivo** de Hasura PROD y DEV: host, port, version, endpoint y ubicación del deployment.
2. Identificar auth real y credenciales administrativas de ambas instancias sin imprimir valores.
3. Auditar source del candidato MCP: `--read-only`, `run_sql`, metadata writes, secret handling, HTTP client, timeouts/logging.
4. Resolver y pinnear el transporte HTTP compatible con el access plane.
5. Elegir artefacto reproducible: image digest confiable o build local desde commit upstream pinneado. No `latest`.
6. Volver a verificar binds `3005/3006` antes de usarlos.
7. Materializar proxy/backend/secrets según [[AGENT-PLATFORM - MCP Access Plane - Architecture]].
8. Certificar PROD negative tests y DEV admin positive tests desde cliente real.
9. Sólo después agregar las capabilities a Daedalus/Cursor y actualizar [[aranea-mcps-expert]].

## Veredicto actual

`BLOCKED` para deployment, **no por diseño** sino por runtime Hasura aún no identificado y por el gap de transporte/auditoría del MCP candidato.

La arquitectura de access plane ya está congelada y **no debe volver a auditarse completa** durante este workstream salvo drift material.

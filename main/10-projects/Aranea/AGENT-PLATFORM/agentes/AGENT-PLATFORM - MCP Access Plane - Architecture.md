---
type: note
status: active
area: "[[Aranea]]"
parent: "[[AGENT-PLATFORM - MCP Access Plane]]"
created: "2026-09-12"
updated: "2026-09-16"
confidence: verified
aliases:
  - aranea-mcp-access-plane-architecture
  - MCP Access Plane Architecture
  - arquitectura MCP Aranea
tags:
  - area/aranea
  - tech/mcp
  - architecture/access-plane
---

# AGENT-PLATFORM - MCP Access Plane - Architecture

> Arquitectura canónica para **agregar, reemplazar o reinstalar capabilities MCP en Aranea**. Este documento evita redescubrir el deployment en cada integración.
>
> Proyecto padre: [[AGENT-PLATFORM - MCP Access Plane]]. Router agent-facing: [[aranea-mcps-expert]].

## Regla principal

Para nuevos MCPs de servicios/datos, el patrón default es:

```text
Cliente / agente
  │
  │ HTTP MCP + Authorization: Bearer <capability-token>
  ▼
mcps.lab.aranea.cl:<puerto dedicado>
  │
  ▼
Nginx auth proxy de ESA capability
  ├─ único container de la capability que publica host port
  ├─ valida bearer cliente→MCP
  ├─ template montado read-only
  ├─ bearer montado read-only desde archivo local de mcps
  └─ proxy_pass por red Docker privada
         │
         ▼
Backend MCP
  ├─ NO publica puerto al host
  ├─ imagen/release/source pinneado; no usar latest
  ├─ recibe credencial del servicio destino separada del bearer
  ├─ credencial montada read-only cuando el backend la necesita
  └─ comparte sólo la red Docker de su familia/capability
         │
         ▼
Servicio destino
(PostgreSQL / MongoDB / Hasura / Kafka / Flink / etc.)
```

**No introducir un patrón distinto sólo porque un nuevo MCP lo haga más fácil.** Una desviación requiere evidencia material y decisión explícita en [[AGENT-PLATFORM - MCP Access Plane]].

## Boundary del host `mcps` — appliance de servicios MCP

`mcps` es un **LXC dedicado a alojar servicios MCP containerizados mediante Docker/Portainer**. No es workstation, jump host ni host de administración general.

Hard rules:

- No instalar clientes de servicios destino en el host (`psql`, `mongosh`, Hasura CLI, Kafka CLI, Flink CLI, etc.) para discovery, troubleshooting o convenience.
- No depender de herramientas de administración del servicio destino instaladas en el LXC.
- No convertir `mcps` en punto de acceso directo a PostgreSQL, MongoDB, Hasura, Kafka, Flink u otros backends.
- Discovery y administración se hacen desde consumidores autorizados usando capabilities MCP, o desde la autoridad operativa propia del servicio cuando el MCP aún no existe.
- Docker/Portainer y herramientas base de inspección del runtime (`docker`, `ss`, `find`, `cat`/`sed` sobre configuración propia del MCP) sí pertenecen al boundary.
- Tooling auxiliar debe vivir en container/artefacto explícito y descartable o en el host de administración correspondiente.

**Invariante:** `mcps` aloja y expone capabilities MCP; no se usa como cliente ad-hoc de los servicios que esas capabilities administran.

## Boundaries de seguridad

### 1. Dos secretos distintos

Nunca confundir:

1. **Bearer cliente → MCP proxy**: autentica a Daedalus/Hermes/u otro consumidor contra la capability.
2. **Credencial backend MCP → servicio destino/backend privado**: PostgreSQL password, Hasura admin secret, token upstream o bearer backend privado cuando la implementación lo requiere.

El cliente no recibe la credencial real del servicio destino/backend. El backend no necesita conocer el bearer del cliente.

### 2. Secretos server-side

Convención verificada en `mcps`:

```text
/opt/mcp/<familia>/runtime/proxy/           # templates Nginx
/opt/mcp/<familia>/runtime/proxy-secrets/   # bearer cliente→MCP
/opt/mcp/<familia>/runtime/secrets/         # credenciales upstream/backend privadas
```

Los secretos se montan read-only al container correspondiente. No registrar valores en Agents-OS, repos, prompts, Cursor config ni logs.

### 3. Backend interno

El backend MCP no publica host port. Sólo el proxy de la capability expone el puerto estable de `mcps.lab.aranea.cl`.

Redes Docker privadas verificadas:

```text
mcp-postgres
mcp-mongo-forge
mcp-hasura
mcp-kafka
mcp-flink
```

### 4. Un proxy por capability

RO/RW, PROD/DEV o cualquier autoridad distinta se materializa como capability separada cuando el contrato lo exige. Cada capability tiene bearer y backend/configuración upstream propios.

No usar bearer universal para múltiples capabilities.

## Nginx auth proxy canónico

Imagen verificada:

```text
nginx@sha256:5616878291a2eed594aee8db4dade5878cf7edcb475e59193904b198d9b830de
```

Contrato:

- `restart=unless-stopped`;
- template `/run/mcp/mcp.conf.template` read-only;
- bearer cliente montado read-only;
- arranque materializa config, descarta variable temporal y ejecuta Nginx foreground;
- `401` cuando el bearer no coincide;
- `proxy_pass` sólo al backend de la red Docker privada;
- buffering desactivado y timeouts compatibles con sesiones MCP largas cuando corresponde.

No copiar tokens materializados desde Nginx a documentación.

## Runtime verificado — 2026-09-13

### Inventario de capabilities y puertos

| Puerto | Capability | Autoridad | Topología |
|---:|---|---|---|
| `3000` | `aranea-ssh` | perfiles viewer/operator | excepción existente: `ssh-mcp` publica directamente y aplica su propio bearer/policy |
| `3001` | `aranea-postgres-ro` | PROD RO | Nginx auth → PostgreSQL MCP interno |
| `3002` | `aranea-postgres-rw` | DEV RW | Nginx auth → PostgreSQL MCP interno |
| `3003` | `aranea-mongo-forge-ro` | PROD RO | Nginx auth → MongoDB MCP interno |
| `3004` | `aranea-mongo-forge-rw` | DEV RW | Nginx auth → MongoDB MCP interno |
| `3005` | `aranea-hasura-prod-ro` | PROD strict RO | Nginx auth → strict-RO Hasura MCP interno |
| `3006` | `aranea-hasura-dev-admin` | DEV admin | Nginx auth → Hasura MCP interno |
| `3007` | `aranea-kafka-dev-admin` | DEV admin | Nginx auth → Kafka MCP interno |
| `3008` | `aranea-flink-dev-admin` | DEV admin | Nginx auth → Flink MCP interno |

**Antes de asignar un puerto nuevo, verificar runtime vivo con `docker ps` + `ss -lntp`; este inventario documenta estado, no reserva puertos futuros.**

### PostgreSQL

Backend pinneado:

```text
local/postgres-mcp:0.3.0-15c8e33
```

Red: `mcp-postgres`.

El backend RO real usa:

```text
user = mcp_echo_prod_ro
host = postgresql.lab.aranea.cl
port = 5432
database = echo
access-mode = restricted
transport = streamable-http
listen interno = 0.0.0.0:8000
```

Deuda conocida: el container histórico `postgres-mcp-echo-dev-ro` está mal nombrado respecto de su target efectivo PROD/RO. No propagar ese error a capabilities nuevas.

Runbook: [[aranea-postgres-mcp]].

### MongoDB Forge

Backend pinneado:

```text
local/mongodb-mcp:2.1.1-2e8eae9
```

Red: `mcp-mongo-forge`.

Los backends RO/RW no publican host ports y los proxies usan el digest Nginx canónico.

Runbook: [[aranea-mongodb-mcp]].

### Hasura

Source MCP pinneado:

```text
repo: sanjay3290/graphql-engine
commit: 9ba59f273daf42205919e6d43e27d2876a6e0b32
MCP version: 1.0.0
```

El upstream es stdio-only. Aranea usa `mcp-proxy` `6.7.16` para exponer Streamable HTTP **dentro** de `mcp-hasura`; Nginx sigue siendo el único listener host-facing.

DEV:

```text
capability: aranea-hasura-dev-admin
endpoint: http://mcps.lab.aranea.cl:3006/mcp
target: http://192.168.31.75:8080
Hasura: CE v2.38.0
metadata DB: hasura_dev_metadata
backend image: local/hasura-mcp:1.0.0-9ba59f2
containers: hasura-mcp-dev-admin + hasura-mcp-auth-dev-admin
```

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

PROD:

```text
capability: aranea-hasura-prod-ro
endpoint: http://mcps.lab.aranea.cl:3005/mcp
target: http://192.168.31.48:8080
Hasura: CE v2.38.0
metadata DB: hasura_metadata
base image: local/hasura-mcp:1.0.0-9ba59f2-prod-ro-h1fix
http image: local/hasura-mcp-http:1.0.0-9ba59f2-prod-ro-h1fix-mcpproxy6.7.16-g010fix
http rollback (tag retenido): local/hasura-mcp-http:1.0.0-9ba59f2-prod-ro-mcpproxy6.7.16
containers: hasura-mcp-prod-ro + hasura-mcp-auth-prod-ro
```

El flag upstream `--read-only` no fue aceptado como boundary suficiente porque mantenía `reload_metadata` y `run_sql`. La variante Aranea elimina ambas registrations y además ejecuta `--read-only`.

Tool surface PROD certificada server-side — **exactamente 3** (desde H1 fix 2026-09-15):

```text
get_inconsistent_metadata
get_schema
get_version
```

`export_metadata` fue eliminado de la superficie PROD-RO por el remediation H1 (expone `database_url` con credenciales upstream embebidas). No existe `run_sql`, `reload_metadata`, `export_metadata` ni metadata mutators en PROD. Por construcción no existe camino MCP para DDL/DML/creación de views/functions ni cambios de metadata.

Cursor puede mostrar una tool cliente `mcp_auth`; no apareció en `tools/list` server-side y no forma parte de la autoridad Hasura.

Runbook: [[aranea-hasura-mcp]]. Workstream cerrado: [[HASURA MCP — workstream del MCP Access Plane]].

### Kafka DEV

Backend adoptado y pinneado:

```text
repo:   wklee610/kafka-mcp
commit: 0b3bf477ac482468fbd9bbafedf056d0ee83f325
image:  local/kafka-mcp:2.0.0-0b3bf47-inc1-fm3.0.1
```

Red: `mcp-kafka`.

`aranea-kafka-dev-admin` publica sólo el proxy en `:3007/mcp`; el backend no publica host port. La imagen Aranea fija FastMCP `3.0.1` y parchea `alter_configs` para usar `incremental_alter_configs`, evitando revertir propiedades no objetivo. Superficie certificada: 19 tools. PROD queda diferido como capabilities separadas futuras; no reutilizar DEV.

Runbook: [[aranea-kafka-mcp]].

### Flink DEV

Backend adoptado y pinneado:

```text
repo:   vaquarkhan/flink-mcp-enterprise-server
version: 0.3.1
commit: 981bbeff3ed7f897ca7c5bde20f36669d5e93bc4
image:  local/flink-mcp:0.3.1-981bbef-aranea2-flink1.14
```

Red: `mcp-flink`.

`aranea-flink-dev-admin` publica sólo el proxy en `:3008/mcp`; backend `flink-mcp-dev-admin` sin host port. El proxy no reenvía el bearer del cliente: usa un bearer backend privado separado, validado server-side mediante registry hash-only. La variante Aranea conserva el approval HMAC upstream como default fail-closed, pero DEV ejecuta con `MCP_FLINK_APPROVAL_REQUIRED=false` detrás del bearer proxy y allowlist explícita. Superficie certificada: exactamente 22 tools y **cero SQL tools** contra Flink `1.14.3`.

El host/runtime plane no se mezcla dentro del backend Flink MCP. Filesystem, Docker, config bind-mounted y lifecycle de `docker-echo-dev` usan `aranea-ssh` + profile `docker-echo-dev-operator`, root-equivalent sólo para DEV. Source-of-truth del stack: Portainer stack `1`; host path `/var/lib/docker/volumes/portainer_data/_data/compose/1/docker-compose.yml`.

Runbooks: [[aranea-flink-mcp]] y [[aranea-ssh-mcp]]. Workstream DEV cerrado: [[Flink MCP — workstream del MCP Access Plane]]. PROD `aranea-flink-prod-ro` queda diferido.

## Excepción existente: SSH MCP

`aranea-ssh` en `:3000` no usa Nginx porque el upstream desplegado ya implementa bearer/policies y publica directamente. Es una **excepción existente**, no el blueprint default para nuevos MCPs.

Runbook: [[aranea-ssh-mcp]].

## Deployment actual

El runtime MCP usa containers standalone/Portainer con `restart=unless-stopped`; no depende de un Compose canónico del access plane.

No introducir Compose como requisito implícito. Estandarizar deployment sería un cambio separado.

## Blueprint para agregar una capability nueva

### Gate A — discovery

1. Identificar servicio destino real: host, puerto, versión, ambiente y auth sin instalar clientes ad-hoc en `mcps`.
2. Definir capability y autoridad exactas antes de instalar.
3. Seleccionar upstream MCP existente; pinnear release/commit/image. No `latest`.
4. Verificar transporte. Upstream stdio-only requiere bridge HTTP pinneado sin romper esta arquitectura.
5. Verificar puertos vivos en `mcps`.

### Gate B — materialización

1. Crear `/opt/mcp/<familia>/runtime/{proxy,proxy-secrets,secrets}` según necesidad.
2. Crear red Docker privada `mcp-<familia>`.
3. Levantar backend MCP sin host port.
4. Montar credencial upstream/backend sólo donde corresponda, read-only.
5. Levantar Nginx auth proxy separado usando el digest canónico o sucesor explícitamente aprobado.
6. Montar template + bearer read-only en proxy.
7. Publicar sólo el puerto del proxy.
8. `restart=unless-stopped` salvo decisión explícita distinta.

### Gate C — cliente

1. Bearer independiente por capability.
2. Secret file fuera de Cursor JSON; Cursor referencia env var.
3. Validar `VAR=SET` sin imprimir valor.
4. Endpoint estable `http://mcps.lab.aranea.cl:<puerto>/<path MCP>`.

### Gate D — certificación

Mínimo:

```text
unauthenticated request -> 401
bearer válido -> initialize MCP PASS
backend host port -> none
secret mounts -> RO
capability/tool surface -> exact authority contract
PROD mutation path -> absent or rejected by construction/policy
DEV mutation/admin path -> positive test sólo cuando corresponda
upstream/backend credential exposed to client -> no
restart policy -> unless-stopped
client real (Cursor/Daedalus) -> PASS
```

`tools/list` server-side es evidencia material de authority cuando la seguridad depende de la superficie expuesta.

No cerrar una capability sólo porque `curl` responda o el container esté `Up`.

## Anti-patrones

No hacer:

- instalar `psql`, `mongosh`, Hasura CLI, Kafka CLI, Flink CLI u otros clientes de servicio en `mcps`;
- usar `mcps` como jump host/workstation;
- publicar backend MCP directo al host por comodidad;
- poner admin secret/password/token upstream en Cursor o prompts;
- reutilizar bearer cliente→MCP como credencial upstream/backend;
- usar `latest`;
- bearer universal para authorities distintas;
- saltar a acceso directo al servicio cuando el MCP falla;
- asumir authority por nombre de container, README o flags sin certificar runtime/tool surface;
- redescubrir esta topología desde cero salvo drift material.

## Discovery mínimo ante drift

```bash
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'
docker network ls
ss -lntp | grep -E ':(300[0-9])\b' || true
```

Si sigue compatible con este contrato, continuar usando esta nota como autoridad. Auditar mounts/commands sólo cuando exista drift material o el nuevo servicio lo exija.

## Fuentes de evidencia

Arquitectura consolidada desde runtime real de `mcps` y certificaciones E2E al 2026-09-13:

- `docker ps` / `ss -lntp` para puertos;
- `docker inspect` de proxies/backends PostgreSQL, MongoDB, Hasura, Kafka y Flink;
- handshakes MCP reales con bearer;
- `tools/list` server-side para boundaries certificadas;
- validaciones end-to-end desde Daedalus/Cursor;
- mounts, imágenes y redes Docker efectivos;
- árbol `/opt/mcp` efectivo;
- certificación host/runtime de `docker-echo-dev-operator` y source-of-truth Portainer del stack Flink DEV.

No se almacenan valores de bearer, passwords, admin secrets ni private keys en esta nota.

---
type: note
status: active
area: "[[Aranea]]"
parent: "[[AGENT-PLATFORM - MCP Access Plane]]"
created: "2026-09-12"
updated: "2026-09-12"
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

> Arquitectura canónica para **agregar, reemplazar o reinstalar capabilities MCP en Aranea**. Este documento existe para evitar redescubrir el deployment en cada nueva integración.
>
> Proyecto padre: [[AGENT-PLATFORM - MCP Access Plane]].

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
  ├─ imagen/release pinneada; no usar latest
  ├─ recibe credencial del servicio destino separada del bearer
  ├─ credencial montada read-only cuando el backend la necesita
  └─ comparte sólo la red Docker de su familia/capability
         │
         ▼
Servicio destino
(PostgreSQL / MongoDB / Hasura / etc.)
```

**No introducir un patrón distinto sólo porque un nuevo MCP lo haga más fácil.** Una desviación requiere evidencia material y decisión explícita en [[AGENT-PLATFORM - MCP Access Plane]].

## Boundaries de seguridad

### 1. Dos secretos distintos

Nunca confundir:

1. **Bearer cliente → MCP proxy**: autentica a Daedalus/Hermes/u otro consumidor contra la capability.
2. **Credencial backend MCP → servicio destino**: PostgreSQL password, Hasura admin secret, token upstream, etc.

El cliente no recibe la credencial real del servicio destino. El backend no necesita conocer el bearer del cliente.

### 2. Secretos server-side

Convención verificada en `mcps`:

```text
/opt/mcp/<familia>/runtime/proxy/          # templates Nginx
/opt/mcp/<familia>/runtime/proxy-secrets/  # bearer cliente→MCP
/opt/mcp/<familia>/runtime/secrets/        # credenciales upstream del backend, cuando aplica
```

Los archivos de secretos se montan **read-only** al container correspondiente. No registrar sus valores en Agents-OS, repos, prompts, Cursor config ni logs.

### 3. Backend interno

El backend MCP no debe publicar host port. Sólo el proxy de la capability expone el puerto estable de `mcps.lab.aranea.cl`.

Los pares proxy/backend comparten una red Docker privada por familia. Ejemplos verificados:

- `mcp-postgres`
- `mcp-mongo-forge`

### 4. Un proxy por capability

RO/RW, PROD/DEV o cualquier autoridad distinta se materializa como capability separada cuando el contrato lo exige. Cada capability tiene su propio proxy/bearer y su propio backend o configuración upstream cuando corresponde.

No usar un bearer universal para todas las capabilities.

## Nginx auth proxy canónico

Imagen verificada:

```text
nginx@sha256:5616878291a2eed594aee8db4dade5878cf7edcb475e59193904b198d9b830de
```

El container auth:

- usa `restart=unless-stopped`;
- monta template en `/run/mcp/mcp.conf.template`;
- monta bearer en `/run/secrets/daedalus.bearer`;
- al arrancar lee el bearer, materializa `/etc/nginx/conf.d/mcp.conf`, hace `unset` de la variable temporal y ejecuta Nginx foreground;
- responde `401` cuando el bearer no coincide;
- hace `proxy_pass` al hostname del backend dentro de la red Docker privada;
- mantiene buffering desactivado y timeouts compatibles con sesiones MCP largas cuando el transporte lo requiere.

No copiar el token ya materializado desde `/etc/nginx/conf.d/mcp.conf` a documentación.

## Runtime verificado — 2026-09-12

### Puertos

| Puerto | Capability actual | Topología |
|---:|---|---|
| `3000` | `aranea-ssh` | excepción existente: `ssh-mcp` publica directamente y aplica su propio bearer/policy |
| `3001` | `aranea-postgres-ro` | Nginx auth → backend PostgreSQL MCP interno |
| `3002` | `aranea-postgres-rw` | Nginx auth → backend PostgreSQL MCP interno |
| `3003` | `aranea-mongo-forge-ro` | Nginx auth → backend MongoDB MCP interno |
| `3004` | `aranea-mongo-forge-rw` | Nginx auth → backend MongoDB MCP interno |
| `3005` | libre al discovery 2026-09-12 | no reservado automáticamente |
| `3006` | libre al discovery 2026-09-12 | no reservado automáticamente |

**Antes de asignar un puerto nuevo, volver a verificar `docker ps` + `ss -lntp`; que estuviera libre en esta fecha no lo reserva.**

### PostgreSQL

Backends:

```text
local/postgres-mcp:0.3.0-15c8e33
```

Auth proxies:

```text
nginx@sha256:5616878291a2eed594aee8db4dade5878cf7edcb475e59193904b198d9b830de
```

Red:

```text
mcp-postgres
```

Mounts verificados:

```text
postgres-mcp-auth-ro:
  /opt/mcp/postgres/runtime/proxy/mcp-ro-final.conf.template
    -> /run/mcp/mcp.conf.template RO
  /opt/mcp/postgres/runtime/proxy-secrets/daedalus-ro.bearer
    -> /run/secrets/daedalus.bearer RO

postgres-mcp-auth-rw:
  /opt/mcp/postgres/runtime/proxy/mcp-rw-final.conf.template
    -> /run/mcp/mcp.conf.template RO
  /opt/mcp/postgres/runtime/proxy-secrets/daedalus.bearer
    -> /run/secrets/daedalus.bearer RO

postgres-mcp-echo-dev-ro:
  /opt/mcp/postgres/runtime/secrets/mcp_echo_prod_ro
    -> /run/secrets/mcp_echo_prod_ro RO

postgres-mcp-echo-dev-rw:
  /opt/mcp/postgres/runtime/secrets/mcp_echo_dev_rw
    -> /run/secrets/mcp_echo_dev_rw RO
```

El backend RO arranca realmente con:

```text
user = mcp_echo_prod_ro
host = postgresql.lab.aranea.cl
port = 5432
database = echo
access-mode = restricted
transport = streamable-http
listen interno = 0.0.0.0:8000
```

**Deuda conocida de naming:** el container `postgres-mcp-echo-dev-ro` está mal nombrado respecto de su target efectivo PROD/RO. No propagar ese error a capabilities nuevas; corregirlo sólo en un cambio separado con validación de consumidores.

### MongoDB Forge

Backends:

```text
local/mongodb-mcp:2.1.1-2e8eae9
```

Red:

```text
mcp-mongo-forge
```

Auth proxies RO/RW usan el mismo digest Nginx canónico y montan:

```text
/opt/mcp/mongo-forge/runtime/proxy/mcp-ro.conf.template
/opt/mcp/mongo-forge/runtime/proxy/mcp-rw.conf.template
/opt/mcp/mongo-forge/runtime/proxy-secrets/daedalus-ro.bearer
/opt/mcp/mongo-forge/runtime/proxy-secrets/daedalus-rw.bearer
```

Los backends Mongo no publican host ports.

## Excepción existente: SSH MCP

`aranea-ssh` en `:3000` no usa el sidecar Nginx porque el upstream desplegado ya implementa autenticación bearer/policies y publica directamente `192.168.31.219:3000->3000`.

Esto es una **excepción existente**, no el blueprint default para nuevos data/service MCPs. Si un nuevo backend puede demostrar un boundary equivalente sin Nginx, documentar la equivalencia y obtener decisión explícita antes de apartarse del patrón proxy/backend.

## Deployment actual

`docker compose ls` estaba vacío durante el discovery 2026-09-12. Los containers actuales existen como runtime standalone/Portainer con `restart=unless-stopped`.

No introducir Compose como requisito implícito para una capability nueva. Adoptarlo para estandarizar deployment sería un cambio separado del access-plane runtime y debe decidirse explícitamente.

## Blueprint para agregar una capability nueva

### Gate A — discovery

1. Identificar servicio destino real: host, puerto, versión, ambiente y auth.
2. Definir capability y autoridad exactas antes de instalar.
3. Seleccionar upstream MCP existente; pinnear release/commit/image. No `latest`.
4. Verificar transporte. El access plane expone HTTP MCP; un upstream sólo-stdio requiere resolver ese gap **sin romper esta arquitectura**.
5. Verificar puertos vivos en `mcps`; no asumir libres por documentación histórica.

### Gate B — materialización en `mcps`

1. Crear `/opt/mcp/<familia>/runtime/{proxy,proxy-secrets,secrets}` según necesidad.
2. Crear red Docker privada `mcp-<familia>`.
3. Levantar backend MCP sin host port.
4. Montar credencial upstream sólo en backend, read-only.
5. Levantar Nginx auth proxy separado usando el digest canónico o su sucesor explícitamente aprobado.
6. Montar template + bearer read-only en proxy.
7. Publicar sólo el puerto del proxy.
8. Usar `restart=unless-stopped` salvo decisión explícita distinta.

### Gate C — cliente

1. Crear bearer independiente por capability.
2. Guardarlo localmente fuera de Cursor JSON; Cursor sólo referencia la env var correspondiente.
3. Validar que el proceso cliente hereda `VAR=SET` sin imprimir valor.
4. Endpoint estable: `http://mcps.lab.aranea.cl:<puerto>/<path MCP>`.

### Gate D — certificación

Mínimo:

```text
unauthenticated request -> 401
bearer válido -> handshake MCP PASS
backend -> no host port
secret mounts -> RO
capability/tool surface -> coincide con autoridad
PROD mutation/admin negative test -> rechazado cuando corresponda
DEV mutation/admin positive test -> sólo si corresponde
servicio destino -> credencial nunca entregada al cliente
restart policy -> unless-stopped
client real (Cursor/Daedalus) -> PASS
```

No cerrar una capability sólo porque `curl` responda o el container esté `Up`.

## Anti-patrones

No hacer:

- backend MCP publicado directamente al host por comodidad;
- admin secret/password del servicio destino en Cursor o en un prompt;
- bearer cliente→MCP reutilizado como credencial upstream;
- `latest` como imagen de backend/proxy;
- un único proxy con bearer universal para múltiples authorities;
- saltar a acceso directo al servicio cuando el MCP falla;
- asumir que los nombres de containers reflejan ambiente/authority sin inspeccionar runtime;
- volver a redescubrir esta topología desde cero salvo evidencia de drift.

## Discovery mínimo ante sospecha de drift

No repetir auditoría completa. Verificar sólo:

```bash
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'
docker network ls
ss -lntp | grep -E ':(300[0-9])\b' || true
```

Si eso sigue siendo compatible con este contrato, usar este documento como autoridad y continuar. Auditar mounts/commands sólo cuando el nuevo servicio los necesite o exista drift material.

## Fuentes de evidencia

Arquitectura congelada desde runtime real de `mcps` el 2026-09-12:

- `docker ps` / `ss -lntp` para puertos publicados;
- `docker inspect` de proxies/backends PostgreSQL y MongoDB;
- template Nginx PostgreSQL RO;
- mounts y redes Docker efectivos;
- árbol `/opt/mcp` efectivo.

No se almacenan valores de bearer, passwords ni admin secrets en esta nota.

---
type: note
status: active
area: "[[Aranea]]"
parent: "[[AGENT-PLATFORM - MCP Access Plane]]"
created: "2026-09-12"
updated: "2026-09-17"
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

> Arquitectura canónica para agregar, reemplazar o reinstalar capabilities MCP Aranea. Proyecto padre: [[AGENT-PLATFORM - MCP Access Plane]]. Router para agentes: [[aranea-mcps-expert]]. Matriz fechada de acceso Cursor/ZCode/Codex y necesidades Echo/Forge: [[Daedalus — Development Agents MCP Access & Gaps]]. Las operaciones de cada familia viven en sus runbooks, no aquí. **Inventario CURRENT reconciliado al 2026-09-17: 13 capabilities `:3000`–`:3012`.** No es un nuevo smoke de runtime ni certificación implícita de todos los clientes.

## Regla principal

Para un nuevo MCP de servicio/datos, patrón default:

```text
Cliente / coding agent (Daedalus)
  -> HTTP MCP + bearer dedicado cliente->capability
  -> mcps.lab.aranea.cl:<puerto de la capability>
  -> Nginx auth proxy específico (ÚNICO host port publicado; bearer+template RO)
  -> red Docker privada de familia
  -> backend MCP sin host port, imagen/source/release pinneados
  -> credencial upstream separada, montada RO sólo donde sea necesaria
  -> servicio destino autorizado
```

No introducir una topología distinta por conveniencia. Desviación sólo con evidencia material y decisión explícita en el proyecto padre. Excepción preexistente: `aranea-ssh` sirve bearer/policy directamente en `:3000` sin Nginx; no convierte esa excepción en blueprint para servicios nuevos. etcd FastMCP usa HTTP nativo internamente; MinIO/Temporal usan bridge stdio→HTTP pinneado; ambos respetan proxy bearer separado y backend sin host port.

## Boundary del host mcps

`mcps` es LXC dedicado a servicios MCP Docker/Portainer, NO workstation/jump host. Prohibido instalar clientes de los servicios destino (`psql`, `mongosh`, Hasura/Kafka/Flink CLI, etc.) en el LXC para discovery o troubleshooting. Discovery/administración mediante MCP autorizado desde consumidor, o autoridad operativa nativa del servicio si la capability aún no existe. Docker, Portainer, `ss`, `find` y lectura de configuración propia MCP sí están dentro de este boundary. Tooling auxiliar, si hace falta, vive en artefacto/container descartable explícito o management host correspondiente. Para operar/reparar el appliance usar management path `mcps-ops` y [[aranea-mcp-plane-operator]], nunca un MCP alojado en el propio `mcps`.

## Seguridad: identidades, red y deployment

**Dos secretos no intercambiables:** bearer cliente→proxy y credencial backend→servicio destino. La segunda nunca se entrega a Daedalus/Hermes ni se persiste en sus configuraciones, el vault, prompts o logs. Bearer por capability separado, no universal.

```text
/opt/mcp/<familia>/runtime/proxy/           # Nginx template
/opt/mcp/<familia>/runtime/proxy-secrets/   # bearer cliente-MCP
/opt/mcp/<familia>/runtime/secrets/         # identidad upstream/backend
```

Mounts sensibles read-only; backend no publica host port; proxy único listener de familia con red Docker privada (`mcp-postgres`, `mcp-mongo-forge`, `mcp-hasura`, `mcp-kafka`, `mcp-flink`, `mcp-observability`, `mcp-temporal`, `mcp-minio`, `mcp-etcd` según familia). Cuando el backend necesita egress al servicio, no volver `--internal` una red que rompa ese egress. Las autoridades PROD/DEV y RO/RW distintas exigen capabilities/identidades separadas cuando el contrato lo requiera.

**Nginx canónico:** `nginx@sha256:5616878291a2eed594aee8db4dade5878cf7edcb475e59193904b198d9b830de`. `restart=unless-stopped`, template y bearer RO, startup que materializa config y descarta variables temporales, 401 sin bearer, proxy_pass privado, buffering/timeouts compatibles con MCP. No documentar el valor del token materializado. Backend/imagen pinneada (commit/release/digest), nunca `latest`; rollback por familia en su runbook.

**Deployment vigente:** containers standalone/Portainer y `restart=unless-stopped`; no existe Compose canónico del access plane. No introducir Compose como requisito o rediseño implícito.

## Inventarios fechados

### HISTORICAL — 2026-09-13: nueve capabilities

El despliegue inicial registraba sólo `:3000`–`:3008` (SSH; PostgreSQL RO/RW; Mongo RO/RW; Hasura PROD-RO/DEV-admin; Kafka DEV-admin; Flink DEV-admin). Este snapshot no se usa como inventario vigente.

### CURRENT — 2026-09-17: trece capabilities

| Puerto | Capability | Autoridad certificada / frontera |
|---:|---|---|
| `3000` | `aranea-ssh` | perfiles viewer/operator, H2 enforcement tool-level; Windows evidence SYSTEM se consume RO con `mt5-kronos-operator`, no viewer SFTP |
| `3001` | `aranea-postgres-ro` | Echo PROD `mcp_echo_prod_ro`, restricted/RO |
| `3002` | `aranea-postgres-rw` | Echo DEV `mcp_echo_dev_rw`, data RW, no asumir schema CREATE |
| `3003` | `aranea-mongo-forge-ro` | Mongo Forge PROD RO, 18 tools |
| `3004` | `aranea-mongo-forge-rw` | Mongo Forge DEV RW, 27 tools |
| `3005` | `aranea-hasura-prod-ro` | Hasura PROD strict-RO, **3 tools** post-H1, sin `export_metadata` |
| `3006` | `aranea-hasura-dev-admin` | Hasura DEV admin, 9 tools |
| `3007` | `aranea-kafka-dev-admin` | Kafka DEV, 19 tools; NO PROD |
| `3008` | `aranea-flink-dev-admin` | Flink REST DEV, 22 tools, sin SQL; NO PROD |
| `3009` | `aranea-observability-ro` | ARGUS Grafana/Prometheus/Loki, 22 tools RO; sin Jaeger toolset |
| `3010` | `aranea-temporal-ro` | Temporal SQX, 28 tools RO, namespace allowlist, no mutadores |
| `3011` | `aranea-minio-rw` | MinIO S3 **RW** (2026-09-18 noche), 9 tools, identidad = key owner full (todos los buckets; put/delete reales certificados); ex `aranea-minio-ro` |
| `3012` | `aranea-etcd-ro` | etcd RO, 4 tools, prefijos/secret-name filtrados; sin mutadores |

`3000` es la excepción SSH, `3001`–`3012` siguen el boundary auth proxy/backend. La tabla registra certificación de familias (según runbooks); **NO prueba que Cursor, ZCode y Codex tengan individualmente las 13**. Cursor obtuvo 11 previas + nuevo trío Temporal/MinIO/etcd probado 3/3; normalización ZCode/Codex 10/10 al 2026-09-16, trío 3010–3012 incorporado por patcher kor el 2026-09-17 y runtime funcional certificado por chain 2026-09-18; **rename 3011 → `aranea-minio-rw` (2026-09-18 noche): Cursor aplicado, ZCode/Codex pendiente de patcher kor** (bearer sin cambio de valor). Confirmar herramientas en el cliente real antes de afirmar disponibilidad. Comprobar puertos vivos con `docker ps`+`ss -lntp` antes de asignar uno nuevo.

## Familias y contratos específicos

### Temporal — 2026-09-17

Upstream `stevekinney/temporal-mcp` npm `0.2.1`; wrapper `mcp-proxy 6.7.16`+fix g010; imagen `local/temporal-mcp-http:0.2.1-mcpproxy6.7.16-g010fix`; backend `temporal-mcp-ro` uid 1000 sin host port en `mcp-temporal`, proxy `temporal-mcp-auth-ro :3010`. Temporal server 1.31.2 gRPC `192.168.31.46:7233` (NO confundir con Traefik UI :8080); config server-side `hardReadOnly`+`allowedNamespaces [sqx-dev,sqx,sqx-prop]`, 28 tools RO, namespace externo DENIED. El frontend interno no tiene TLS/API key: boundary agent-facing bearer+RO+allowlist. Ninguna llamada start/signal/cancel/terminate es parte de esta capability. [[aranea-temporal-mcp]].

### MinIO S3 RO — 2026-09-17

Upstream `txn2/mcp-s3` v1.4.0 pinneado; backend `minio-mcp-ro` imagen `local/minio-mcp-http:1.4.0-mcpproxy6.7.16-g010fix` (Go stdio + mcp-proxy fix), proxy `minio-mcp-auth-ro :3011`, red privada `mcp-minio`, S3 target `192.168.31.92:9000`. Identidad upstream: service account hija con policy embedded, NO admin; effective allow = padre ∩ policy, ListBucket `deploy` y `examples`, GetObject `deploy/worker/sqx/*` y objetos `examples`; DENY `*backup*`. 9 tools registradas; put/copy/delete se muestran upstream pero read-only los rechaza server-side. No generalizar el Get a resultados Forge arbitrarios ni usar RO para publicar releases. [[aranea-minio-mcp]].

### etcd RO — 2026-09-17

Gateway greenfield FastMCP autorizado por mandato del MCP-trio, imagen `local/etcd-mcp-ro:0.1.0`, HTTP streamable nativo backend `etcd-mcp-ro` sin host port, proxy `etcd-mcp-auth-ro :3012`, red `mcp-etcd`. Servicio: cinco miembros `192.168.31.250-.254`, gateway v3 JSON `/v3/kv/range`, timeout 3s. Cuatro tools read-only; deny-by-default 8 prefixes, branch MinIO sensible excluida, regex secret-name en todas las rutas, caps 200 keys/4KB, sin `put`/`delete`/`txn`/`watch`. El cluster subyacente permanece sin TLS/auth: no convertir acceso directo anónimo en autoridad de agentes ni declarar hardening cerrado. Workstream separado [[ETCD — Seguridad y Hardening — workstream del MCP Access Plane]]. [[aranea-etcd-mcp]].

### PostgreSQL

Imagen `local/postgres-mcp:0.3.0-15c8e33`, red `mcp-postgres`. RO real: `mcp_echo_prod_ro@postgresql.lab.aranea.cl:5432/echo`, restricted Streamable HTTP, backend :8000 interno. Container histórico llamado `postgres-mcp-echo-dev-ro` está mal nombrado respecto al target PROD: no propagar su nombre como authority. RW es data DEV, no schema CREATE por inferencia. E-05 aplicó 063 en DEV usando `run_sql` de Hasura admin bajo su contrato. [[aranea-postgres-mcp]].

### MongoDB Forge

Imagen pinneada `local/mongodb-mcp:2.1.1-2e8eae9`, red `mcp-mongo-forge`, backend RO/RW sin host ports y proxies Nginx por capability separados. RO 18 tools, RW 27; conexión normal `connectionId=preconfigured`, no URIs arbitrarias. [[aranea-mongodb-mcp]].

### Hasura

Upstream MCP `sanjay3290/graphql-engine` commit `9ba59f273daf42205919e6d43e27d2876a6e0b32`, MCP v1.0.0 stdio bridged por mcp-proxy 6.7.16 + fix g010. DEV `aranea-hasura-dev-admin :3006` → Hasura CE 2.38.0 `.75:8080`, imagen base `local/hasura-mcp:1.0.0-9ba59f2`, metadata dev, **9 tools**: `apply_metadata`, `clear_metadata`, `drop_inconsistent_metadata`, `export_metadata`, `get_inconsistent_metadata`, `get_schema`, `get_version`, `reload_metadata`, `run_sql`. PROD `aranea-hasura-prod-ro :3005` → `.48:8080`, CE 2.38.0, imagen strict RO `local/hasura-mcp-http:1.0.0-9ba59f2-prod-ro-h1fix-mcpproxy6.7.16-g010fix`, rollback tag anterior retenido. PROD expone EXACTAMENTE `get_inconsistent_metadata`, `get_schema`, `get_version`; `export_metadata` eliminado H1 por exponer credenciales upstream, `run_sql`/reload/mutadores ausentes. Un flag upstream `--read-only` NO bastaba por sí solo. `mcp_auth` UI Cursor no es tool del backend salvo presente en `tools/list` server-side. El bug GAP-ECHO-010 de hijo stdio compartido muerto está reparado con g010 (nueva sesión), no extrapolar a SSH/Flink. [[aranea-hasura-mcp]].

### Kafka DEV

Upstream `wklee610/kafka-mcp` commit `0b3bf477ac482468fbd9bbafedf056d0ee83f325`; imagen `local/kafka-mcp:2.0.0-0b3bf47-inc1-fm3.0.1`, red `mcp-kafka`, backend interno, proxy :3007, 19 tools. Pin FastMCP 3.0.1 y patch `alter_configs` a `incremental_alter_configs` para no revertir settings ajenos. PROD diferido con identidades separadas `aranea-kafka-prod-ro`/`aranea-kafka-prod-ops` (NO desplegadas). [[aranea-kafka-mcp]].

### Flink DEV

Upstream `vaquarkhan/flink-mcp-enterprise-server` 0.3.1 commit `981bbeff3ed7f897ca7c5bde20f36669d5e93bc4`; imagen `local/flink-mcp:0.3.1-981bbef-aranea2-flink1.14`, red `mcp-flink`, proxy :3008, backend sin host port. Proxy bearer cliente ≠ bearer backend privado. Approval HMAC upstream fail-closed por default, `MCP_FLINK_APPROVAL_REQUIRED=false` sólo en DEV detrás de proxy/allowlist. 22 tools, CERO SQL, Flink 1.14.3. Host/filesystem/Docker/config/lifecycle separado: `aranea-ssh` + `docker-echo-dev-operator` root-equivalent DEV; source-of-truth Portainer stack 1 (`/var/lib/docker/volumes/portainer_data/_data/compose/1/docker-compose.yml`). PROD `aranea-flink-prod-ro` diferido/no desplegado. [[aranea-flink-mcp]], [[aranea-ssh-mcp]].

### Observabilidad y SSH

ARGUS `aranea-observability-ro :3009` = `grafana/mcp-grafana` v1.4.2 digest pinneado, `--disable-write`, toolsets search/datasource/prometheus/loki/dashboard, 22 tools read-only, sin Jaeger toolset aunque datasource exista; no administra alertas/dashboards. [[aranea-observability-mcp]]. SSH `aranea-ssh :3000` excepción con bearer/policy propia, H2 viewer tool-level; `mt5-kronos-operator` no-admin consume evidence JSON publicado SYSTEM, report freshness ≤15 min para deploy, reviewer `mt5-kronos+sftp-download` DENIED; `echo-runtime-prod` es viewer sin mutación. [[aranea-ssh-mcp]], [[SSH MCP — workstream del MCP Access Plane]].

## Blueprint de nueva capability (NO ejecutar sin gap demostrado)

**Gate A — discovery:** servicio real host/puerto/versión/ambiente/auth sin instalar clientes en mcps; operación mínima, identity, scope, upstream existente pinneado o excepción autorizada; transporte validado; puerto disponible verificado vivo.

**Gate B — materialización:** runtime dir/proxy-secrets/upstream secrets scoped, red Docker de familia, backend sin host port ni latest, upstream credential RO mount, proxy Nginx bearer dedicado como único listener, template+bearer RO, `restart=unless-stopped`, rollback exacto. Cambiar authority PROD/RO a RW exige capability/identidad separada y decisión owner, NO flip de flag.

**Gate C — consumer:** credencial cliente por capability en archivo fuera de mcp.json cuando cliente soporta env, referencia real al chain; `VAR=SET` sin revelar valor, endpoint estable `mcps.lab.aranea.cl`. ZCode/Codex pueden diferir semánticamente de Cursor; exigir prueba independiente con config propia. [[aranea-mcp-capability-plane]].

**Gate D — certificación:** `401` sin bearer, handshake válido, backend sin host port, secret mounts RO, `tools/list` autoridad exacta, rechazo negativo de mutadores PROD/RO, probes positivos acotados DEV cuando corresponda, no upstream credential al cliente, restart y rollback, E2E consumidor identificado. `tools/list` del servidor prevalece sobre etiqueta del container/flag. `Up` o `curl 200` aislado NO son certificación; no confundir smoke de Cursor con ZCode/Codex.

## Anti-patrones y drift

NO: clientes ad-hoc en `mcps`, jump host, backend expuesto, secreto upstream en Cursor/vault/chat, bearer universal, bearer proxy reutilizado upstream, tags `latest`, acceso directo para saltarse MCP, aprobación `auto` tratada como owner, PROD por capability DEV, viewer ampliado para solucionar SFTP Windows, MinIO RO usado para escritura, etcd endpoint anónimo usado para writes, Telegram gateway Hermes supuesto MCP de Daedalus. Si la capability existente no cubre operación: documentar target, verbo, policy denial y alternativa autorizada antes de pedir nueva.

Discovery mínimo por management path autorizado:

```bash
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'
docker network ls
ss -lntp | grep -E ':(300[0-9]|301[0-2])\b' || true
```

Sólo ampliar inspección mounts/commands ante drift material. Actualizar router+runbook+inventario tras un cambio certificado, no reconstruir el plane cada vez.

## Fuentes y alcance de evidencia

Arquitectura original consolidada desde `docker ps`/`ss`, `docker inspect`, tool surface y smoke E2E de 2026-09-13. Adiciones 2026-09-15/17 por runbooks [[aranea-observability-mcp]], [[aranea-temporal-mcp]], [[aranea-minio-mcp]], [[aranea-etcd-mcp]] y bitácora del proyecto padre. La presente actualización reconcilia documentación ya certificada: no afirma haber ejecutado un nuevo probe live. Ningún bearer/password/API secret/private key se registra aquí.
---
type: runbook
schema_version: 1
scope: area
created: "2026-09-13"
updated: "2026-09-13"
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
  - "[[AGENT-PLATFORM - MCP Access Plane - Architecture]]"
  - "[[Data streaming — Kafka, Flink, EMQX]]"
aliases:
  - runbook Flink MCP Aranea
  - aranea flink mcp
  - mcp flink
  - aranea-flink-dev-admin
  - docker-echo-dev-operator
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
  - tech/flink
  - tech/statefun
  - action/mcp-flink
---

# aranea-flink-mcp

## Propósito

Operar Apache Flink / Stateful Functions DEV de Aranea con dos superficies complementarias y explícitas:

- `aranea-flink-dev-admin` para el control plane Flink vía REST/MCP;
- `aranea-ssh` con profile `docker-echo-dev-operator` para el host/runtime plane cuando la acción necesita filesystem, Docker, Compose, logs, exec o lifecycle del stack.

El routing agent-facing vive en [[aranea-mcps-expert]], la mecánica común del plano MCP en [[aranea-mcp-capability-plane]], el acceso host genérico en [[aranea-ssh-mcp]] y la arquitectura/deployment común en [[AGENT-PLATFORM - MCP Access Plane - Architecture]].

PROD queda fuera de este runbook operativo: `aranea-flink-prod-ro` está diferido y no debe sustituirse con autoridad DEV.

## Capability certificada

| Ambiente | Capability | Endpoint | Autoridad | Estado |
|---|---|---|---|---|
| DEV | `aranea-flink-dev-admin` | `http://mcps.lab.aranea.cl:3008/mcp` | administración Flink REST DEV | PASS / CLOSED end-to-end |
| DEV host/runtime | `aranea-ssh` + `docker-echo-dev-operator` | `http://mcps.lab.aranea.cl:3000/` | root operator sobre `docker-echo-dev` | PASS / CLOSED end-to-end |

No existe capability Flink PROD certificada. `aranea-flink-prod-ro` pertenece al workstream PROD diferido.

## Runtime DEV verificado

```text
host/LXC:        docker-echo-dev
LAN IP:          192.168.31.75
runtime:         Docker / Portainer
compose project: flink
containers:      statefun-master, statefun-worker
image:           apache/flink-statefun:3.2.0-java11
Flink:           1.14.3
Flink commit:    98997ea
StateFun:        3.2.0
JobManager REST: http://192.168.31.75:8082 -> container :8081
JobManager RPC:  host :6123
HA:              none
TaskManagers:    1
slots:           2 total / 0 available at certification
```

Job operativo observado al certificar:

```text
name:    StatefulFunctions
job id:  974f0479256bc8ffe71fe962750e9c90
state:   RUNNING
vertices: 14/14 RUNNING
subtasks: 28/28 RUNNING
parallelism: 2
```

Flujo observado: Kafka ingress/journals -> `functions` -> Kafka egress (`echo-core-commands`, `system-events`, `automation-actions`, `close-commands`).

Configuración relevante observable:

```text
parallelism.default=2
execution.checkpointing.mode=AT_LEAST_ONCE
checkpoint interval=120s
checkpoint timeout=5m
state backend=rocksdb
incremental checkpoints=true
savepoints=file:///opt/flink/savepoints
checkpoints=file:///opt/flink/checkpoints
restart strategy=fixed-delay, 3 attempts / 5s
```

## Backend MCP adoptado

Upstream pinneado:

```text
repo:    vaquarkhan/flink-mcp-enterprise-server
release: 0.3.1
commit:  981bbeff3ed7f897ca7c5bde20f36669d5e93bc4
license: Apache-2.0
```

Patch Aranea:

```text
patch sha256: e0b683e8927fc888b986826b56b28655de54bc6f65f8d5fcacafe4cf4041a9b1
image:        local/flink-mcp:0.3.1-981bbef-aranea2-flink1.14
image id:     sha256:d99ee2567c706801700c5415f6c4445c8d76c9cc1e6ffd91c0d578fccf61a4a9
```

El patch conserva el comportamiento upstream fail-closed por defecto y agrega `MCP_FLINK_APPROVAL_REQUIRED`; el default sigue siendo `true`. En DEV se fija `false` para evitar HMAC por cada mutación, porque el boundary real queda en bearer externo + allowlist/scopes explícitos. El cliente Daedalus/Cursor no recibe el approval secret.

Compatibilidad Flink 1.14.3 corregida:

- `get_flink_config`: `/config` -> `/jobmanager/config`;
- cancel: `PATCH /jobs/:jobid?mode=cancel` con body `{}`;
- trigger savepoint: `target-directory`;
- stop job: `targetDirectory`;
- `delete_jar`: `DELETE /jars/:jarid`;
- `dispose_savepoint`: `POST /savepoint-disposal` con `savepoint-path`;
- status async para savepoint, rescale y savepoint disposal.

SQL tools quedan excluidas porque no existe SQL Gateway verificado en este runtime.

## Deployment certificado

Topología:

```text
Cursor / Daedalus
  -> Authorization: Bearer capability token
  -> mcps.lab.aranea.cl:3008/mcp
  -> flink-mcp-auth-dev-admin (Nginx)
  -> flink-mcp-dev-admin:8090
  -> Flink DEV REST 192.168.31.75:8082
```

Containers/red:

```text
backend: flink-mcp-dev-admin
proxy:   flink-mcp-auth-dev-admin
network: mcp-flink
```

Invariantes certificados:

- backend sin host port;
- Nginx es el único listener host-facing en `3008`;
- proxy usa el digest Nginx canónico del Access Plane;
- `restart=unless-stopped`;
- bearer cliente->proxy separado del bearer privado proxy->backend;
- backend auth registry hash-only;
- mounts de secrets/JAR staging read-only donde corresponde;
- backend corre como `nobody`;
- source/release/patch/image pinneados;
- valores de bearer/private keys nunca se documentan.

Paths operativos server-side, sólo como ubicación y nunca para imprimir contenido:

```text
/opt/mcp/flink/runtime/proxy-secrets/daedalus-dev-admin.bearer
/opt/mcp/flink/runtime/secrets/backend-http.bearer
/opt/mcp/flink/runtime/secrets/backend-auth.tokens
/opt/mcp/flink/runtime/jars
```

## Tool surface certificada

`tools/list` server-side devolvió exactamente 22 tools:

```text
cancel_job
delete_jar
dispose_savepoint
get_cluster_info
get_flink_config
get_job
get_job_config
get_job_exceptions
get_job_metrics
get_job_status
get_rescale_status
get_savepoint_disposal_status
get_savepoint_status
list_checkpoints
list_jars
list_jobs
list_taskmanagers
rescale_job
run_jar
stop_job
trigger_savepoint
upload_jar
```

No existen tools SQL en esta capability.

## Certificación material 2026-09-13

Boundary/auth:

```text
unauthenticated :3008/mcp -> 401
wrong bearer                -> 401
authenticated initialize    -> 200 + Mcp-Session-Id
protocol                    -> 2024-11-05
tools/list                  -> 22 exactas
SQL tools                   -> none
backend host port           -> none
```

`get_cluster_info` vía MCP retornó:

```text
taskmanagers=1
slots-total=2
slots-available=0
jobs-running=1
flink-version=1.14.3
flink-commit=98997ea
```

`list_jobs` retornó el job `StatefulFunctions` RUNNING con id `974f0479256bc8ffe71fe962750e9c90`.

La implementación Java responde `tools/call` como `text/event-stream`; un parser que espere JSON plano puede producir falsos negativos. Para certificar manualmente, parsear los eventos `data:` del SSE.

Daedalus y Cursor fueron certificados contra el endpoint real, y Cursor ejecutó lecturas reales del cluster/job.

## Cliente Daedalus / Cursor

Secret cliente:

```text
~/.config/mcp/secrets/flink-mcp-dev-admin.bearer
mode: 0600
env:  ARANEA_FLINK_MCP_DEV_ADMIN_BEARER
```

Loader:

```text
~/.config/mcp/aranea-env.sh
```

Cursor:

```text
name: aranea-flink-dev-admin
url:  http://mcps.lab.aranea.cl:3008/mcp
Authorization: Bearer ${env:ARANEA_FLINK_MCP_DEV_ADMIN_BEARER}
```

Nunca persistir el bearer literal en `~/.cursor/mcp.json` ni en Agents-OS.

## Host/runtime operator — `docker-echo-dev-operator`

Lifecycle de Docker/systemd/filesystem no pertenece al MCP Flink. Para eso se usa `aranea-ssh` con el profile dedicado:

```text
profile:    docker-echo-dev-operator
target:     root@192.168.31.75
authority:  operator / writable / root
key:        dedicada a este profile
transport:  aranea-ssh MCP
```

Certificación E2E vía `run-command`:

```text
host=docker-echo-dev
user=root
Docker client/server=29.1.3
Docker Compose=v5.0.1
statefun-master=running
statefun-worker=running
MCP result isError=false
```

Este profile autoriza el host DEV completo y por diseño es root-equivalent. Usarlo sólo para el target `docker-echo-dev`; no extrapolarlo a otros hosts ni a PROD.

Operaciones normales:

- leer/escribir configuración y archivos del stack DEV;
- `docker inspect`, logs, stats y exec;
- restart/stop/start cuando la tarea lo requiera;
- manipular el stack DEV con rollback y post-condición explícitos;
- transferir archivos vía `aranea-ssh` cuando corresponda.

## Source-of-truth del stack Flink/StateFun

La aparente ausencia de `/data/compose/1/docker-compose.yml` en el host era engañosa: `/data` pertenece al container Portainer y está respaldado por el volumen `portainer_data`.

Compose original exacto:

```text
Portainer stack id: 1
Portainer path:      /data/compose/1/docker-compose.yml
Host path real:      /var/lib/docker/volumes/portainer_data/_data/compose/1/docker-compose.yml
sha256:              92573189cd375b2dedb1da697b7f39496b1866643ecf1f41eb963912ab79148c
```

Config persistente bind-mounted:

```text
/root/statefun/conf/flink-conf.yaml -> /opt/flink/conf/flink-conf.yaml:ro
/root/statefun/modules              -> /opt/statefun/modules:ro
```

Persistencia runtime del stack:

```text
Portainer /data/compose/1/statefun/checkpoints -> /opt/flink/checkpoints
Portainer /data/compose/1/statefun/savepoints  -> /opt/flink/savepoints
```

En el host corresponden bajo:

```text
/var/lib/docker/volumes/portainer_data/_data/compose/1/statefun/
```

No crear un segundo `compose.yaml` en `/root/statefun`: el stack Portainer es la autoridad declarativa.

## Disciplina de lifecycle

El Compose original se recuperó completo, pero Docker Compose v5 calcula `config-hash` distinto al que quedó grabado por el stack vigente y `--dry-run up -d` propone `Recreate` de ambos containers. Por tanto:

- **cambios sólo en bind-mounted config/modules:** editar `/root/statefun/...`, validar y usar restart controlado de los containers necesarios;
- **cambios de topology/env/ports/volumes/imagen:** editar/deployar mediante el stack Portainer canónico y tratar el redeploy como recreación explícita;
- **no** ejecutar `docker compose up -d` desde el host contra el YAML recuperado como operación rutinaria sólo porque el contenido parezca equivalente;
- antes de mutar lifecycle, fijar target, blast radius, rollback y post-condición;
- después de restart/redeploy, verificar Flink REST, TaskManager/slots y job state en el mismo ambiente.

El mismatch de config-hash no prueba que el YAML recuperado sea incorrecto; es drift de implementación/versionado Compose/Portainer respecto del runtime actual. No perseguir igualdad de hash a ciegas.

## Qué superficie usar

| Necesidad | Superficie |
|---|---|
| cluster/jobs/status/metrics/config observable | `aranea-flink-dev-admin` |
| savepoint/rescale/cancel/stop/JAR | `aranea-flink-dev-admin` |
| editar `flink-conf.yaml` o módulos | `aranea-ssh` + `docker-echo-dev-operator` |
| Docker logs/inspect/exec | `aranea-ssh` + `docker-echo-dev-operator` |
| restart containers | `aranea-ssh` + `docker-echo-dev-operator` |
| topology/env/ports/volumes/image | Portainer stack + operator, con redeploy controlado |
| SQL Gateway | no disponible/verificado; no inventar tool |
| PROD | fuera de scope; `aranea-flink-prod-ro` diferido |

## Troubleshooting

- capability ausente en Cursor -> revisar env/restart/handshake según [[aranea-mcp-capability-plane]];
- `401` -> bearer cliente->Nginx; no tocar Flink;
- `400` en GET autenticado -> un GET no-MCP puede ser inválido; ejecutar handshake real;
- tool call aparentemente vacío -> revisar `Content-Type: text/event-stream` y parsear `data:` SSE;
- backend MCP Up pero Flink tools fallan -> verificar reachability `mcps -> 192.168.31.75:8082` y Flink REST antes de tocar proxy;
- operación necesita filesystem/Docker -> usar `docker-echo-dev-operator`, no agregar shell arbitrario al MCP Flink;
- `docker compose up -d` propone recreate inesperado -> no continuar por inercia; usar Portainer source-of-truth y disciplina de lifecycle;
- SQL requerido -> blocker de capability/runtime; no improvisar SQL Gateway;
- necesidad PROD -> abrir workstream PROD strict-RO separado.

## Hard Rules

- Aranea-only; nunca usar contra MELI/corporativo.
- DEV admin no autoriza PROD.
- No saltar `aranea-flink-dev-admin` con REST directo agent-first cuando la tool MCP cubre la operación.
- No meter shell/Docker arbitrario dentro del backend Flink MCP; host/runtime pertenece a `aranea-ssh`.
- No publicar el backend MCP al host.
- No imprimir bearer tokens, backend bearer, private keys ni approval secrets.
- No agregar SQL tools sin SQL Gateway real y certificación explícita.
- No crear una segunda fuente declarativa del stack fuera de Portainer.
- No usar `docker compose up -d` rutinariamente contra el YAML del volumen Portainer mientras el dry-run implique recreación no solicitada.
- Para mutaciones: target + blast radius + rollback + post-condición + verificación en DEV.

## Validación

```text
Environment:            DEV
Flink capability:       aranea-flink-dev-admin
Flink endpoint:         http://mcps.lab.aranea.cl:3008/mcp
Proxy unauthenticated:  401
MCP initialize/tools:   PASS / 22 exactas
SQL surface:            none
Backend host port:      none
Flink target:           192.168.31.75:8082
Host operator:          aranea-ssh / docker-echo-dev-operator
Operator identity:      root@docker-echo-dev
Portainer stack id:     1
Stack source-of-truth:  /var/lib/docker/volumes/portainer_data/_data/compose/1/docker-compose.yml
DEV E2E:                PASS / CLOSED
PROD authority:         none / deferred
Secrets exposed:        no
```

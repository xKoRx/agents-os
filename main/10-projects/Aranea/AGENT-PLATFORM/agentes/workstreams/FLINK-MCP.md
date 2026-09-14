---
type: note
status: dev-closed
area: "[[Aranea]]"
parent: "[[AGENT-PLATFORM - MCP Access Plane]]"
created: "2026-09-13"
updated: "2026-09-13"
tags:
  - area/aranea
  - tech/mcp
  - tech/flink
---

# Flink MCP — workstream del MCP Access Plane

> Componente del proyecto [[AGENT-PLATFORM - MCP Access Plane]]. **No es un proyecto paralelo.**
>
> DEV está **PASS / CLOSED**. PROD queda diferido y se abrirá como fase separada strict-RO.

## Objetivo

Materializar dos capabilities MCP separadas por ambiente para Apache Flink:

- `aranea-flink-dev-admin`: administración operacional Flink DEV vía REST/MCP;
- `aranea-flink-prod-ro`: inspección estrictamente read-only de Flink PROD, diferida.

El lifecycle/filesystem/Docker del host DEV no se mezcla dentro del backend Flink MCP: se resuelve mediante `aranea-ssh` + profile `docker-echo-dev-operator`.

## Estado

```text
DEV aranea-flink-dev-admin        PASS / CLOSED
DEV docker-echo-dev-operator      PASS / CLOSED
Daedalus integration              PASS
Cursor integration                PASS
PROD aranea-flink-prod-ro         DEFERRED / NOT IMPLEMENTED
```

Runbook canónico: [[aranea-flink-mcp]].

## Runtime DEV certificado

```text
host/LXC:        docker-echo-dev
LAN IP:          192.168.31.75
runtime:         Docker / Portainer
compose project: flink
StateFun image:  apache/flink-statefun:3.2.0-java11
containers:      statefun-master, statefun-worker
Flink:           1.14.3
commit:          98997ea
StateFun:        3.2.0
JobManager REST: http://192.168.31.75:8082 -> container :8081
JobManager RPC:  host :6123
HA:              none
TaskManagers:    1
slots:           2 total / 0 free at certification
```

Job observado:

```text
name:      StatefulFunctions
job id:    974f0479256bc8ffe71fe962750e9c90
state:     RUNNING
vertices:  14/14 RUNNING
subtasks:  28/28 RUNNING
parallelism: 2
```

## Source-of-truth del stack

La label histórica:

```text
/data/compose/1/docker-compose.yml
```

no es una ruta host normal: es el path dentro de Portainer. El volumen `/data` del container Portainer está respaldado por `portainer_data`.

Authority declarativa real:

```text
Portainer stack id: 1
Portainer path:      /data/compose/1/docker-compose.yml
Host path real:      /var/lib/docker/volumes/portainer_data/_data/compose/1/docker-compose.yml
sha256:              92573189cd375b2dedb1da697b7f39496b1866643ecf1f41eb963912ab79148c
```

Config bind-mounted:

```text
/root/statefun/conf/flink-conf.yaml
/root/statefun/modules
```

Persistencia runtime:

```text
/var/lib/docker/volumes/portainer_data/_data/compose/1/statefun/checkpoints
/var/lib/docker/volumes/portainer_data/_data/compose/1/statefun/savepoints
```

Docker Compose v5 calcula hashes distintos a los labels del runtime vigente y `--dry-run up -d` propone recreación. Por tanto no usar el YAML recuperado con `docker compose up -d` como operación rutinaria. Bind-mounted config se cambia + restart controlado; topology/env/ports/volumes/image se cambian vía stack Portainer con redeploy explícito.

## Backend MCP adoptado

```text
repo:    vaquarkhan/flink-mcp-enterprise-server
release: 0.3.1
commit:  981bbeff3ed7f897ca7c5bde20f36669d5e93bc4
license: Apache-2.0
```

Patch Aranea:

```text
sha256:   e0b683e8927fc888b986826b56b28655de54bc6f65f8d5fcacafe4cf4041a9b1
image:    local/flink-mcp:0.3.1-981bbef-aranea2-flink1.14
image id: sha256:d99ee2567c706801700c5415f6c4445c8d76c9cc1e6ffd91c0d578fccf61a4a9
```

Compatibilidad corregida para Flink 1.14.3:

- config `/jobmanager/config`;
- cancel `PATCH /jobs/:jobid?mode=cancel`;
- savepoint `target-directory`;
- stop `targetDirectory`;
- delete JAR;
- dispose savepoint;
- status async savepoint/rescale/disposal.

`MCP_FLINK_APPROVAL_REQUIRED` mantiene default upstream fail-closed `true`; DEV lo fija `false` porque la autoridad se aplica por bearer externo + allowlist/scopes. El approval secret no se entrega a clientes.

No hay SQL Gateway verificado y no se exponen tools SQL.

## Deployment MCP certificado

```text
Cursor / Daedalus
  -> bearer capability
  -> mcps.lab.aranea.cl:3008/mcp
  -> flink-mcp-auth-dev-admin (Nginx)
  -> flink-mcp-dev-admin:8090
  -> Flink REST 192.168.31.75:8082
```

Runtime MCP:

```text
network: mcp-flink
backend: flink-mcp-dev-admin
proxy:   flink-mcp-auth-dev-admin
backend host port: none
proxy host port:   3008
restart:            unless-stopped
```

Auth separation:

```text
client bearer -> Nginx
private backend bearer -> backend
backend registry -> hash-only
```

Secrets nunca se registran en Agents-OS.

## Tool surface DEV certificada

Exactamente 22 tools:

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

SQL surface: none.

## Certificación MCP

```text
unauthenticated :3008/mcp -> 401
wrong bearer -> 401
initialize -> 200 + Mcp-Session-Id
protocol -> 2024-11-05
tools/list -> 22 exactas
get_cluster_info -> PASS
list_jobs -> PASS
backend host port -> none
Daedalus -> PASS
Cursor -> PASS
```

El backend Java responde tools/call como `text/event-stream`; los probes manuales deben parsear eventos `data:` SSE.

## Host/runtime operator certificado

`aranea-ssh` incorpora:

```text
profile:    docker-echo-dev-operator
target:     root@192.168.31.75
authority:  operator / writable / root
key:        dedicada
readOnly:   false
```

E2E vía MCP `run-command`:

```text
host=docker-echo-dev
user=root
Docker client/server=29.1.3
Docker Compose=v5.0.1
statefun-master=running
statefun-worker=running
isError=false
```

Este profile es intencionalmente root-equivalent para DEV. No concede autoridad PROD ni sobre otros hosts.

## Boundary congelado

```text
aranea-flink-dev-admin
  = Flink REST/control plane
  = cluster/jobs/checkpoints/savepoints/rescale/JAR/config observable

aranea-ssh + docker-echo-dev-operator
  = host/runtime plane
  = filesystem/config files/Docker/logs/exec/restart/redeploy
```

No introducir shell arbitrario dentro del MCP Flink para cubrir lifecycle del host.

## PROD diferido

`aranea-flink-prod-ro` deberá ser capability separada con bearer propio y tool surface estrictamente de lectura. No reutilizará DEV admin ni `docker-echo-dev-operator`. La ausencia de mutadores en `tools/list` server-side será parte de la certificación PROD strict-RO.

No diseñar ni implementar PROD dentro del cierre DEV.

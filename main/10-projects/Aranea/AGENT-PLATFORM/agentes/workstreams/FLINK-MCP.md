---
type: note
status: in-progress
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
> Deployment target MCP: `mcps.lab.aranea.cl`. Cliente inicial: Daedalus. Ambiente DEV inicial: `docker-echo-dev`.

## Objetivo

Materializar dos capabilities MCP separadas por ambiente para Apache Flink:

- `aranea-flink-dev-admin`: administración operacional completa de Flink DEV, incluyendo inspección, jobs, configuración y lifecycle/restarts cuando la implementación real lo permita de forma explícita y verificable.
- `aranea-flink-prod-ro`: inspección estrictamente read-only de Flink PROD, a implementar después de cerrar DEV.

La fase activa es exclusivamente DEV. PROD queda diferido y no debe bloquear ni ampliar el rollout inicial.

## Scope DEV activo

`aranea-flink-dev-admin` debe permitir administrar Flink DEV sin depender de SSH como primer mecanismo normal. La superficie objetivo incluye, según el deployment/version real:

- cluster, JobManager, TaskManagers y health;
- jobs, status, plan, vertices/operators, parallelism, exceptions;
- checkpoints, savepoints, metrics, backpressure y watermarks cuando la API real lo permita;
- submit/cancel/stop/restart/rescale jobs cuando Flink soporte la operación;
- upload/run/delete JARs si forman parte del deployment real;
- cambios de configuración con scope y post-condición explícitos;
- lifecycle operacional del servicio Flink DEV, incluyendo restart cuando el runtime real lo requiera y exista un boundary controlable.

DEV tiene autoridad administrativa real. Antes de una mutación se fija target, blast radius y post-condición y se verifica el resultado en el mismo ambiente.

## Scope PROD diferido

`aranea-flink-prod-ro` será una capability separada con bearer propio y tool surface estrictamente de lectura. No reutilizará la autoridad DEV ni expondrá submit/cancel/savepoint/JAR/config/lifecycle mutations. Su diseño se abrirá sólo después de cerrar DEV.

## Estado

`DISCOVERY / IN-PROGRESS — DEV FIRST`.

Confirmado por el owner para este workstream:

```text
MCP server host: mcps.lab.aranea.cl
DEV target host: docker-echo-dev
initial client: Daedalus
phase 1: aranea-flink-dev-admin
phase 2: aranea-flink-prod-ro
```

## Runtime DEV verificado — 2026-09-13

```text
host: docker-echo-dev.aranea.local
LAN IP: 192.168.31.75
runtime: Docker
compose project label: flink
StateFun image: apache/flink-statefun:3.2.0-java11
containers: statefun-master, statefun-worker
Flink: 1.14.3
commit: 98997ea
JobManager REST: http://192.168.31.75:8082 -> container :8081
JobManager RPC host port: :6123
HA: none
TaskManagers: 1
slots: 2 total / 0 free
jobs running at discovery: 1
```

REST `GET /overview`, `GET /jobmanager/config` y `GET /taskmanagers` respondieron `HTTP 200` desde el host DEV. `mcps` alcanzó `http://192.168.31.75:8082/overview` con `HTTP 200`, por lo que el path de red MCP→Flink DEV está validado.

La configuración observable incluye `parallelism.default=2`, `state.backend=rocksdb`, checkpoints cada `120s`, `execution.checkpointing.mode=AT_LEAST_ONCE`, savepoints en `file:///opt/flink/savepoints` y checkpoints en `file:///opt/flink/checkpoints`.

### Drift detectado

Las labels Docker de `statefun-master` indican:

```text
compose_project=flink
compose_workdir=/data/compose/1
compose_files=/data/compose/1/docker-compose.yml
```

pero `/data/compose/1/docker-compose.yml` ya no existe en el host. Por tanto esas labels son provenance histórica/stale y no deben usarse como autoridad para lifecycle/restart hasta localizar el stack real vigente.

## MCP plane verificado — 2026-09-13

`mcps.lab.aranea.cl` tiene ocupados `3000` a `3007`; `3008` estaba libre al discovery y queda como candidato para `aranea-flink-dev-admin`, sujeto a materialización sin drift concurrente.

Patrón live confirmado:

- backend MCP privado sin host port;
- Nginx auth proxy como único listener host-facing;
- redes Docker `mcp-*` por familia;
- `restart=unless-stopped` según arquitectura canónica;
- `mcps -> Flink DEV` reachability PASS.

Kafka DEV admin (`aranea-kafka-dev-admin` en `:3007`) es el precedente operativo inmediato a replicar para layout, bearer proxy, network, secrets y certificación.

## Backend MCP candidato

Candidato preferido para DEV: `vaquarkhan/flink-mcp-enterprise-server` release `0.3.1` / Apache-2.0.

Razones materiales: transporte HTTP nativo, bearer, health/readiness/metrics, policy/allowlist, tool surface read y write separable, operaciones Flink REST/SQL administrativas y Docker non-root. Antes de freeze de imagen deben validarse compatibilidad real con Flink `1.14.3`, tool surface exacta y endpoints write contra la API disponible en este runtime.

El lifecycle de Docker/systemd no pertenece naturalmente al REST de Flink. Para reinicios de `statefun-master`, `statefun-worker` o stack se reutilizará `aranea-ssh` con un perfil operator acotado a `docker-echo-dev`, en vez de introducir shell arbitrario dentro del MCP Flink.

## Arquitectura heredada

Ambas capabilities deben reutilizar [[AGENT-PLATFORM - MCP Access Plane - Architecture]]: backend MCP interno sin host port, Nginx bearer proxy por capability como listener host-facing, bearer cliente→MCP independiente de cualquier credencial upstream, source/release/dependencies pinneados y secretos fuera de repos/config de Cursor.

Para DEV, la autoridad administrativa debe existir en la tool surface certificada y no depender de prompts de buena conducta. Para PROD, la ausencia de mutadores en `tools/list` server-side será parte del contrato strict-RO.

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
> Deployment target MCP: `mcps.lab.aranea.cl`. Cliente inicial: Daedalus. Ambiente DEV activo: `docker-echo-dev`.

## Objetivo

Materializar dos capabilities MCP separadas por ambiente para Apache Flink:

- `aranea-flink-dev-admin`: administración operacional completa de Flink DEV, incluyendo inspección, jobs, configuración y lifecycle/restarts mediante los boundaries existentes que correspondan.
- `aranea-flink-prod-ro`: inspección estrictamente read-only de Flink PROD, a implementar después de cerrar DEV.

La fase activa es exclusivamente DEV. PROD queda diferido y no debe bloquear ni ampliar el rollout inicial.

## Scope DEV activo

`aranea-flink-dev-admin` debe permitir administrar Flink DEV sin depender de SSH como primer mecanismo normal. La superficie objetivo incluye, según soporte real de Flink 1.14.3 y del MCP adoptado:

- cluster, JobManager, TaskManagers y health;
- jobs, status, plan, vertices/operators, parallelism, exceptions;
- checkpoints, savepoints, metrics, backpressure y watermarks cuando la API real lo permita;
- submit/cancel/stop/rescale jobs cuando Flink soporte la operación;
- upload/run/delete JARs si forman parte del deployment real;
- SQL DDL/DML cuando exista SQL Gateway real y se certifique;
- cambios de configuración/lifecycle del runtime por el boundary operacional existente, sin convertir el MCP Flink en shell remoto arbitrario.

DEV tiene autoridad administrativa real. Antes de una mutación se fija target, blast radius y post-condición y se verifica el resultado en el mismo ambiente.

## Runtime DEV verificado — 2026-09-13

Host:

```text
hostname: docker-echo-dev.aranea.local
LAN IP:   192.168.31.75
runtime:  Docker
compose project label: flink
```

Containers observados:

```text
statefun-master  apache/flink-statefun:3.2.0-java11
statefun-worker  apache/flink-statefun:3.2.0-java11
```

Flink efectivo:

```text
Flink version: 1.14.3
commit:        98997ea
StateFun:      3.2.0
HA:            none
execution:     DETACHED
REST internal: 8081
REST host:     192.168.31.75:8082 -> statefun-master:8081
RPC host:      :6123 -> statefun-master:6123
TaskManagers:  1
slots:         2 total / 0 free
jobs:          1 running
```

REST probes locales certificados:

```text
GET /overview            -> HTTP 200
GET /jobmanager/config   -> HTTP 200
GET /taskmanagers        -> HTTP 200
```

Configuración material observada incluye:

```text
parallelism.default=2
execution.checkpointing.mode=AT_LEAST_ONCE
execution.checkpointing.interval=120s
execution.checkpointing.timeout=5min
state.backend=rocksdb
state.backend.incremental=true
state.savepoints.dir=file:///opt/flink/savepoints
state.checkpoints.dir=file:///opt/flink/checkpoints
restart-strategy=fixed-delay
restart-strategy.fixed-delay.attempts=3
restart-strategy.fixed-delay.delay=5s
high-availability=none
```

### Drift Compose detectado

Las labels Docker declaran:

```text
project=flink
service master=statefun-master
compose workdir=/data/compose/1
compose file=/data/compose/1/docker-compose.yml
```

pero el archivo `/data/compose/1/docker-compose.yml` no existe actualmente en el namespace del host. El lifecycle/restart no debe depender de ese path hasta ubicar la fuente Compose real o certificar una operación equivalente por container/service.

## Backend MCP candidato

Candidato preferido para evaluación material:

```text
repo: vaquarkhan/flink-mcp-enterprise-server
release: 0.3.1
license: Apache-2.0
```

Motivo: expone lectura Flink y write tools explícitas para savepoint/rescale/JAR/run/stop/cancel/SQL, HTTP MCP, health/readiness/metrics, policy/allowlist y controles de escritura. Antes de adoptar se debe verificar compatibilidad efectiva contra Flink 1.14.3 y congelar source/release exactos.

El MCP Flink administra la superficie Flink REST/SQL. Lifecycle de Docker/servicio/config de host se mantiene separado y debe reutilizar el boundary operacional existente (`aranea-ssh` con perfil operator acotado) en vez de agregar shell arbitrario al MCP Flink.

## Scope PROD diferido

`aranea-flink-prod-ro` será una capability separada con bearer propio y tool surface estrictamente de lectura. No reutilizará la autoridad DEV ni expondrá submit/cancel/savepoint/JAR/config/lifecycle mutations. Su diseño se abrirá sólo después de cerrar DEV.

## Estado

`DISCOVERY / IN-PROGRESS — DEV FIRST`.

Confirmado:

```text
MCP server host: mcps.lab.aranea.cl
DEV target host: docker-echo-dev / 192.168.31.75
Flink REST DEV: http://192.168.31.75:8082
Flink: 1.14.3 / StateFun 3.2.0
initial client: Daedalus
phase 1: aranea-flink-dev-admin
phase 2: aranea-flink-prod-ro
```

Aún no están congelados como hechos: SQL Gateway availability, source exacto/tag/commit del backend MCP, compatibilidad write API completa con Flink 1.14.3, puerto de `mcps`, transport/path final, tool surface certificada y mecanismo exacto de lifecycle Docker.

## Arquitectura heredada

Ambas capabilities deben reutilizar [[AGENT-PLATFORM - MCP Access Plane - Architecture]]: backend MCP interno sin host port, Nginx bearer proxy por capability como listener host-facing, bearer cliente→MCP independiente de cualquier credencial upstream, source/release/dependencies pinneados y secretos fuera de repos/config de Cursor.

Para DEV, la autoridad administrativa debe existir en la tool surface certificada y no depender de prompts de buena conducta. Para PROD, la ausencia de mutadores en `tools/list` server-side será parte del contrato strict-RO.

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
> Deployment target MCP: `mcps.lab.aranea.cl`. Cliente inicial: Daedalus. Ambiente DEV a descubrir/administrar inicialmente: `docker-echo-dev`.

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
DEV target host a inspeccionar: docker-echo-dev
initial client: Daedalus
phase 1: aranea-flink-dev-admin
phase 2: aranea-flink-prod-ro
```

Aún no están congelados como hechos: deployment real de Flink en DEV, versión, containers/services, JobManager/REST endpoint, puertos, auth/TLS, deployment mode, HA, paths/config, implementación MCP, puerto de `mcps`, transport/path MCP y mecanismo exacto de lifecycle. Esos datos se incorporarán sólo después de discovery read-only y evidencia material.

## Arquitectura heredada

Ambas capabilities deben reutilizar [[AGENT-PLATFORM - MCP Access Plane - Architecture]]: backend MCP interno sin host port, Nginx bearer proxy por capability como listener host-facing, bearer cliente→MCP independiente de cualquier credencial upstream, source/release/dependencies pinneados y secretos fuera de repos/config de Cursor.

Para DEV, la autoridad administrativa debe existir en la tool surface certificada y no depender de prompts de buena conducta. Para PROD, la ausencia de mutadores en `tools/list` server-side será parte del contrato strict-RO.

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

# Flink MCP / aranea-flink-ro — workstream del MCP Access Plane

> Componente del proyecto [[AGENT-PLATFORM - MCP Access Plane]]. **No es un proyecto paralelo.**
>
> Deployment target: `mcps.lab.aranea.cl`. Cliente inicial: Daedalus.

## Objetivo

Materializar `aranea-flink-ro` como capability MCP centralizada para diagnóstico estructurado de Apache Flink desde agentes, evitando depender de SSH como primer mecanismo de inspección.

## Scope inicial

- Autoridad estrictamente read-only.
- Inspección objetivo: cluster, JobManager, TaskManagers, jobs, estado, vertices/operators, parallelism, exceptions, checkpoints, metrics, backpressure, watermarks cuando la API real lo permita y configuración observable.
- Operaciones fuera de scope y prohibidas en esta capability: submit/cancel/stop/restart jobs, rescale, trigger/dispose savepoints, upload/delete/run JARs y cualquier mutación de configuración o cluster.

## Estado

`DISCOVERY / IN-PROGRESS`.

Aún no están congelados ni registrados como hechos: deployment real de Flink, versión, JobManager/REST endpoint, puertos, auth, TLS, deployment mode, HA, credenciales, implementación MCP, puerto de `mcps` ni transport/path cliente. Esos datos se incorporarán sólo después de discovery read-only y evidencia material.

## Targets confirmados del workstream

```text
server: mcps.lab.aranea.cl
capability: aranea-flink-ro
initial client: Daedalus
```

## Boundary RO congelado

La capability debe aplicar defense in depth: bearer propio cliente→MCP, tool surface MCP exclusivamente de lectura y upstream Flink REST mantenido dentro del boundary privado existente. Si un MCP candidato mezcla mutadores con lectura y no permite eliminarlos o denegarlos de forma verificable antes de alcanzar Flink, no es apto para `aranea-flink-ro`.

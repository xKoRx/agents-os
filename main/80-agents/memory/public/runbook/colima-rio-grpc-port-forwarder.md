---
type: runbook
schema_version: 1
scope: user
created: "2026-10-08"
updated: "2026-10-08"
area: "[[Meli]]"
project: "[[Kafka — Ambiente local con servicios reales]]"
application:
entities:
  - "[[RIO]]"
  - "[[rio-controlplane-kafka]]"
related:
  - "[[2026-10-08-kafka-local-compose-review-session-feedback]]"
aliases:
  - Colima rio
  - perfil rio E2E
confidence: high
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/user
---

# Colima `rio` — VM de E2E local con forwarder gRPC

## Propósito

- Levantar la VM Colima `rio` (4 CPU / 8 GB / 40 GB, contexto Docker `colima-rio`) donde corre el ecosistema RIO local (Kafka CP, playmaker, ClickHouse CP, Flink CP) con los puertos publicados accesibles desde el Mac.

## Precondiciones

- Perfil ya creado (`colima start --profile rio --cpu 4 --memory 8 --disk 40 --vm-type vz --mount-type virtiofs`), una sola vez.
- Contexto Docker activo del usuario: `colima` (VM default con MySQL compartido). No cambiarlo.

## Procedimiento

1. Arrancar con forwarder gRPC: `LIMA_HOME=$HOME/.colima/_lima LIMA_SSH_PORT_FORWARDER=false limactl start colima-rio`. Colima 0.8.1 fuerza el forwarder SSH, que muere con SIGKILL y deja los puertos sin llegar al host.
2. Usar la VM antepuesta a cada comando: `DOCKER_CONTEXT=colima-rio docker compose …`.
3. Detener con `LIMA_HOME=$HOME/.colima/_lima limactl stop colima-rio`.

## Validación

- Un contenedor con `-p 127.0.0.1:<puerto>:…` responde desde el host (curl distinto de `000`) en el primer intento.

## Rollback / recuperación

- `colima stop --profile rio` borra el contexto `colima-rio`; recrearlo con `docker context create colima-rio --docker host=unix://$HOME/.colima/rio/docker.sock`.
- `colima start` cambia el contexto activo; volver con `docker context use colima`.

## Evidencia

- 2026-10-08: forwarder SSH → `000` en 10/10 intentos; gRPC → 200 al primer intento. Stack Kafka CP medido en ~610 MB (CP 231 MB, broker 380 MB). Ver [[2026-10-08-claude-code-opus-5-5-kafka-local-compose-review]].

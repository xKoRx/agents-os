---
type: decision
schema_version: 1
scope: application
created: "2026-08-14"
updated: "2026-08-14"
area: "[[Echo]]"
project: "[[Echo Forge - Optimización de Latencia WFM Exporter]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge]]"
  - "[[Symphony]]"
related:
  - "[[2026-07-31-task-local-dirs-input-output-only]]"
  - "[[2026-07-31-temporal-activity-contract-remote-only]]"
aliases:
  - one vm one worker one task
  - sqx worker serial execution
  - no local worker concurrency
confidence: verified
source_session: owner-confirmation-2026-08-14
load_policy: when_application_loaded
indexable: true
index_priority: critical
tags:
  - kind/decision
  - scope/application
  - application/echoforge
  - area/echo
  - tech/temporal
  - tech/sqx
  - priority/critical
---

# Decision: Echo Forge ejecuta una sola task por worker

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Las VMs SQX ejecutan trabajo físico mediante workers de Echo Forge.
- El diseño operativo vigente es `1 VM = 1 worker` y cada worker admite una sola activity/task simultánea (`MaxConcurrentActivityExecutionSize: 1`).
- Un workflow Temporal puede despachar muchas activities. Temporal distribuye ese trabajo entre VMs/workers, pero cada worker lo consume secuencialmente.
- En planes anteriores, agentes confundieron el fan-out del workflow con concurrencia dentro de un worker y propusieron locks, scopes y aislamiento local innecesarios.

## Decisión

> [!danger]+ Invariante vinculante
> **1 VM = 1 worker = 1 task en ejecución. No existe concurrencia dentro de un worker.**

1. Un worker nunca atiende dos tasks/activities a la vez.
2. Una task termina —incluyendo cleanup y publicación— antes de que ese worker empiece la siguiente.
3. Los recursos locales compartidos de SQX (`databanks/input`, `databanks/output`, `overview/`, properties y proyecto instalado) se reutilizan secuencialmente.
4. La concurrencia del pipeline solo ocurre entre workers alojados en VMs distintas.
5. Todo agente que planifique o implemente Echo Forge debe tratar esta regla como precondición, no como riesgo abierto.
6. Cambiar esta regla requiere una decisión arquitectónica separada, aprobación explícita del owner y modificación previa del contrato de concurrencia del worker.

## Rationale

- La serialización ya es la protección del recurso físico SQX.
- Agregar otra exclusión local duplica una garantía existente, aumenta complejidad y latencia, y crea estados de espera/cancelación que el diseño no necesita.
- La regla fue confirmada explícitamente por el owner y ya tenía evidencia previa en [[2026-07-31-task-local-dirs-input-output-only]].

## Consecuencias

- **Prohibido por YAGNI:** locks de filesystem, mutexes, semáforos, slots host-locales, coordinadores locales, clones del proyecto o workspaces/scopes por request cuya única justificación sea evitar concurrencia dentro del worker.
- No se crean sticky workers, task queues por host ni afinidad de estrategia a VM para resolver este problema.
- El cleanup local sigue siendo obligatorio donde el contrato de la task lo requiera, pero es secuencial y no necesita lock.
- Una feature que divida un batch en una task por estrategia puede fan-out a la task queue normal: Temporal reparte entre workers disponibles y cada worker mantiene ejecución serial.
- Reviews y planes deben rechazar cualquier mecanismo de concurrencia local salvo que enlacen una decisión posterior, explícitamente aprobada, que reemplace esta invariante.

## Alternativas descartadas

- **Lock host-local “por seguridad”:** descartado; protege una concurrencia imposible bajo el contrato vigente.
- **Scope/hash/directorio por estrategia para aislar ejecuciones simultáneas:** descartado cuando su única motivación es concurrencia local.
- **Más de un proceso worker por VM:** fuera de la arquitectura actual y no puede asumirse anticipatoriamente.

## Evidencia y trazabilidad

- [[2026-07-31-task-local-dirs-input-output-only]] documenta `MaxConcurrentActivityExecutionSize: 1` y que las activities se serializan por host.
- [[Echo Forge - Trade List Export Contrato Remoto]] aplicó el mismo contrato para limpiar `databanks/input` y `databanks/output` sin locks.
- Confirmación directa del owner: 2026-08-14.

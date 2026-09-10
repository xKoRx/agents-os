---
type: learning
schema_version: 1
scope: global
created: "2026-09-09"
updated: "2026-09-09"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os-agent-project-workflow]]"
  - "[[agents-os-entity-update]]"
aliases:
  - checkpoint append-only no declara vigencia
  - estados históricos redactados como vigentes
confidence: verified
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/global
  - project/agents-os
  - tech/agents-os
---

# Un checkpoint append-only no declara qué está vigente

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Aprendizaje

- La bitácora append-only garantiza que nada se pierde; no garantiza que se sepa qué rige hoy. Un agente que la lee de arriba a abajo encuentra varios estados escritos en presente y tiene que inferir la vigencia por fecha, que es justo la inferencia que el sistema promete evitar.

## Por qué importa

- El diseño append-only es lo que más valor entrega en continuidad y no debe cambiarse: el costo no está en acumular historia, está en no rotularla. La regla que falta es de escritura, no de estructura.

## Aplicabilidad

- Cualquier nota de proyecto o checkpoint de continuidad con bitácora acumulativa, sea de agente o humana.

## Cómo aplicarlo

- Mantener un único bloque de estado vigente e inequívoco al tope de la nota; la historia va debajo y en pasado.
- Al superar un estado, reescribir el vigente en lugar de agregar otro en presente. Un bloque histórico se rotula como no vinculante en el mismo cambio que lo reemplaza.
- Es la misma regla de atemporalidad que ya rige para specs, extendida a la nota de proyecto: el documento describe un estado objetivo, no su propia historia de edición.

## Evidencia

- Seis sesiones con el mismo costo de lectura: [[2026-09-03-echo-forge-release-0-2-87-gate-w-session-feedback]] ("los checkpoints históricos de release mezclan estado superseded"), [[2026-09-04-crear-context-session-feedback]] ("varios estados históricos aún redactados como vigentes"), [[2026-09-05-echo-forge-reretester-fix-retest-session-feedback]] ("exigiría leer fechas").

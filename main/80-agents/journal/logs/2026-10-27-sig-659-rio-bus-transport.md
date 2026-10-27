---
type: change_log
schema_version: 1
scope: session
created: "2026-10-27"
updated: "2026-10-27"
area: "[[Meli]]"
project: "[[SIG-659 — Discovery & CLI]]"
application: "[[rio-playmaker]]"
entities:
  - "[[SIG-659 — Discovery & CLI]]"
related:
  - "[[rio-sdk-events]]"
  - "[[rio-controlplane-kafka]]"
  - "[[RIO]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-10-27-sig-659-rio-bus-transport

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Meli/SIG-659 — Discovery & CLI/SIG-659 — Discovery & CLI.md`
  - `10-projects/Meli/SIG-659 — Discovery & CLI/agentes/SIG-659 — RIO Bus (implementación).md` (created)

## Motivo

- El owner arranca el transporte del P0 (Discovery como primer cliente de un mecanismo de mensajería agnóstico playmaker ↔ CP) y pidió dejar en el proyecto lo que se va a hacer, con una propuesta de solución.

## Fuentes usadas

- Spellbook: SIG-635, SIG-644, SIG-671, SIG-697 y SIG-699 leídas por CLI; búsqueda de una spec de transporte sin resultados.
- Código en refs remotas: `rio-playmaker@origin/develop 0c0e319c9`, `rio-sdk-events@origin/master b928149` y ramas `discovery-v2-0*`, `rio-controlplane-kafka@origin/develop f4b5701`.
- RAG `dev-training-ue` (capacitación Fury de BigQueue): filtros habilitados por tópico, ack por HTTP 200 y reintento hasta TTL.

## Resolución aplicada

- Estado actual, próximo paso, sección "🚌 Transporte — RIO Bus" (resumen del diseño cerrado por el owner y puntos abiertos), tareas `F1·bus`, fila del SDK en la tabla de entrega, bitácora, decisión de reparto y decisión de diseño del transporte.
- Creadas en Spellbook SIG-718 (funcional) y SIG-719 (técnica) del RIO Bus, en `draft` e hijas de la epic SIG-659; contenido remoto verificado contra el local.
- Segunda iteración con el owner: filtros múltiples confirmados en mqclient (`Filters(List<String>)`), scope como string configurado y DD-7/DD-8 (línea del SDK y entrada del reader) en la técnica; ambas specs sin preguntas abiertas.
- Tercera iteración: un solo consumer por app y scope hacia `POST /rio-bus`; `RioBusReader` global ejecuta el process desde `RioBusProcessRegistry`; DD-4 reescrito con sus consecuencias.
- Revisión de consistencia (v4 de ambas specs): body obligatorio, `RioBusRejectedException` unchecked, excepción en `parse` = `REJECTED`, DD-1/DD-2/DD-3 alineados con el consumer por scope, y publicación al arrancar dentro del alcance del funcional.
- Revisión final KISS/YAGNI (v5): publicación de Discovery en el SDK (`DiscoveryContractProvider` + `DiscoveryContractPublisher`, DD-9), configuración `rio.bus` (`topic`, `scope: ${SCOPE}`, `segment-id`), `RioBusPublisher` concreto y registry dentro de `RioBusReader`. SIG-718/719 pasadas a `review`.
- Proyecto de agente creado con el plan de implementación (3 fases, 4 controles humanos); `validate_plan.py` sin errores; tarea puente en el padre.

## Validación

- `lint.py --strict` sobre la nota del proyecto, el proyecto de agente y este log.
- `validate_plan.py` sobre el proyecto de agente: phases=3 gates=3 dispatches=3 errors=0.
- Relectura por CLI de SIG-718 y SIG-719: tipo, estado, padre y contenido idéntico al local.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir la nota del proyecto a su contenido del 2026-10-22 (sección del transporte, tareas `F1·bus` y entradas del 2026-10-27).
- SIG-718 y SIG-719 quedan en `draft`; si se descartan, se quitan como hijas de SIG-659 y se borran en Spellbook. 

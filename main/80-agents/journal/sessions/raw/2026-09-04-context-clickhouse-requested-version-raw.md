---
type: raw_session
schema_version: 1
scope: session
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Meli]]"
project: "[[Adopción de Context en Control Planes]]"
application: "[[rio-controlplane-clickhouse]]"
entities:
  - "[[RIO]]"
related:
  - "[[Plan de implementación — Context en ClickHouse]]"
aliases: []
confidence: verified
source_session:
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-raw.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# 2026-09-04-context-clickhouse-requested-version-raw

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: Codex desktop
- Proyecto o entidad: [[Adopción de Context en Control Planes]] / [[rio-controlplane-clickhouse]]
- Objetivo de la sesión: Aclarar por qué Context v1 no permite retirar `params`, especificar el estado solicitado faltante y cerrar la sesión con continuidad documental.

## Transcript

```
User: Comparte el veredicto de la revisión de Context en ClickHouse y pregunta por qué existen blockers si Context trae todo lo que hoy contiene params.

Agent: Distingue cobertura de keys de semántica temporal. Verifica que params contiene la configuración efectiva de la solicitud actual, mientras context.component.lastDeployedVersion.inputs pertenece al último deployment completado y puede faltar en el primero. Concluye que esto bloquea retirar params o usar last-deployed como autoridad en PROVISION/UPDATE, pero no bloquea una adopción aditiva de Context. Separa los gaps de Materialized View, Kafka y target Java como blockers de paths o etapas específicas.

User: Entiende que falta el estado actual y propone agregar un current junto a lastVersion, ambos del mismo tipo.

Agent: Recomienda evitar current por ambiguo y modelar requestedVersion y lastDeployedVersion. Ambos pueden compartir EffectiveInputs, pero no el mismo DTO: requested todavía no posee outputs; last-deployed es histórico. Los valores pueden coincidir en un redeploy, pero no es una garantía y normalmente difieren en update/rollback.

User: Pide documentar la decisión, dejar la especificación y cerrar la sesión para continuar con otro modelo.

Agent: Actualiza el plan, la nota de proyecto, el change log y el agent run previo con el contrato objetivo, invariantes, ejemplo, tests, gates y rework humano observado; ejecuta validación contractual, lint dirigido y refresh del índice local.
```

## Evidencia externa

- `rio-controlplane-clickhouse` → `src/main/java/com/mercadolibre/rio/controlplane/clickhouse/deployment/adapter/rest/DeploymentTriggerMapper.java`
- `rio-sdk-events` → `src/main/java/com/mercadolibre/rio/sdk/events/deployment/context/Component.java`
- `rio-sdk-events` → `src/main/java/com/mercadolibre/rio/sdk/events/deployment/context/LastDeployedVersion.java`

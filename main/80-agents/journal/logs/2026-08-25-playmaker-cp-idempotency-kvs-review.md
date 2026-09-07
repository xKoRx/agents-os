---
type: change_log
schema_version: 1
scope: project
created: "2026-08-25"
updated: "2026-08-25"
area: "[[Meli]]"
project: "[[Playmaker — Doble dispatch al avanzar batches]]"
application: "[[rio-playmaker]]"
entities: []
related:
  - "[[playmaker-deployment-idempotency-and-cp-kvs]]"
  - "[[rio-controlplane-kafka]]"
  - "[[rio-controlplane-flink]]"
  - "[[rio-controlplane-clickhouse]]"
  - "[[rio-controlplane-fury]]"
aliases: []
confidence: verified
source_session: 2026-08-25-playmaker-cp-idempotency-kvs-review
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/project
  - app/rio-playmaker
  - topic/idempotency
---

# 2026-08-25-playmaker-cp-idempotency-kvs-review

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated / deleted / conflict-resolution
- **Archivo(s):**
  - `30-resources/rio-atlas/architecture/playmaker-deployment-idempotency-and-cp-kvs.md`
  - `30-resources/rio-atlas/00-index.md`
  - `30-resources/rio-atlas/log.md`
  - `10-projects/Meli/Playmaker — Doble dispatch al avanzar batches/Playmaker — Doble dispatch al avanzar batches.md`
  - `10-projects/Meli/Playmaker — Doble dispatch al avanzar batches/Auditoría independiente — Informe del doble dispatch.md`
  - `80-agents/memory/public/decision/rio/2026-08-25-playmaker-cp-idempotency-boundary.md`

## Motivo

- Revisar si el KVS de los Control Planes puede validar idempotencia suficiente para el fix de deployments duplicados de Playmaker y dejar explícito el límite entre deduplicación downstream y unicidad del avance lógico.

## Fuentes usadas

- `rio-playmaker`: `DataProductActionLockImpl` con claim create-only, owner token, TTL y release condicionado.
- `rio-controlplane-kafka` y `rio-controlplane-flink`: `IdempotencyGuard`, claves por `deployment_id`, 409/CAS, stale takeover, TTL y finalize CAS.
- `rio-controlplane-clickhouse`: estado KVS disponible pero `claimStart` no cableado al flujo y claim sólo JVM-local en la implementación actual.
- `rio-controlplane-fury`: convergencia por natural key + `specHash`, complementada por CAS para la primera creación.
- Nota canónica del incidente de Playmaker y su flujo de deploy.

## Resolución aplicada

- Se documentó que Kafka/Flink deduplican el mismo `deployment_id`, no dos IDs distintos para el mismo service o batch lógico.
- Se clasificó el fix necesario en tres capas: claim atómico del batch, reserva/constraint de máximo un activo por service y CP como backstop del mismo comando.
- Se dejó la decisión reusable en [[2026-08-25-playmaker-cp-idempotency-boundary]].

## Validación

- Contrato de schema `resource`: PASS, errors=0.
- Se actualizó el catálogo del RIO Atlas y la bitácora append-only; la cobertura dirigida confirmó la nueva página en el índice.
- `graphify-obsidian update`: bloqueado por 11 errores y 6 warnings preexistentes en skills/memorias no relacionadas; no se modificaron esos archivos.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir las ediciones de documentación listadas; no hubo cambios de código en los repos externos.

## Addendum — hotfix del listener y refactor durable

- **Tipo:** conflict-resolution / updated.
- **Motivo:** el owner descartó cambios de DB/entidades/estados/CPs y el enfoque `ComponentRun.DISPATCHING` para el parche inmediato; pidió separar un hotfix acotado de la solución durable.
- **Resolución:** hotfix con mutex KVS create-only en `BatchCompletedEventListener`, clave `pipeline_execution_id + next_batch_order`, espera con exponential backoff fuera de DB y detección `already_materialized` mediante deployments existentes del mismo group; refactor posterior con tópico externo, publicación recuperable y lógica atómica/consistente que cubra también cross-execution.
- **Deprecación:** `feature/adhoc-double-dispatch`, PR #1064 y la recomendación `PENDING → DISPATCHING` quedan históricos/superseded; la auditoría independiente conserva evidencia, pero muestra un warning de no implementación.
- **Documentación de implementación:** la nota principal detalla alcance, archivos, secuencia transaccional, algoritmo `all/none/partial`, pruebas, pros, contras, rama propuesta y mensaje al equipo.
- **Código/repos externos:** sin cambios; rama `hotfix/serialize-batch-completed-listener` sólo propuesta, todavía no materializada.
- **Validación documental:** `validate_schema_contract.py` PASS; lint strict de las seis notas canónicas modificadas PASS con `ERROR=0 WARN=0`. `30-resources/rio-atlas/log.md` conserva su exención derivada sin frontmatter y falla sólo si se fuerza como path explícito.
- **Graphify:** reindex intentado y bloqueado con exit `44` por 11 errores y 6 warnings preexistentes fuera del cambio (`signals-func-spec-authoring`, `signals-tech-spec-authoring`, `zsh-modifier-breaks-git-show-sha-path` y references sin frontmatter); no se ampliaron para no mezclar iniciativas.

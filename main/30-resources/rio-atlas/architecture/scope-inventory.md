---
type: resource
schema_version: 1
status: active
area: "[[Meli]]"
project: "[[Estandarización de Scopes RIO]]"
last_verified: 2026-08-12
confidence: high
sources:
  - "[[RIO]]"
  - "[[Fury — Inventario live de infraestructura y BigQueue]]"
tags:
  - kind/resource
  - tech/rio
created: 2026-08-12
updated: 2026-08-19
cssclasses:
  - wide
---

# RIO — Inventario y propuesta de scopes

> [!warning] Nota generada
> Fuente: `~/fuentes/rio-inspector/rio-scopes.json`. Propuesta: `rio-scope-policy.json`. No editar las tablas a mano.

## Síntesis vigente

Fecha `2026-08-12T21:20:55-04:00`. Fury registra **88 scopes**: **50 legacy**, **26 nonprod** y **12 nonsite**.

Infra observable: **22/23** BigQueue con consumer activo; **0/15** Streams con sink activo; **3/3** Work Queues con worker group; **42/42** Web con Fury route.

Fury Config Orchestrator tiene release `APPROVED` para **42/88** scopes. En **39** la versión desplegada coincide, en **2** difiere y en el resto la versión desplegada o el latest no están expuestos por ambas superficies.

## Modelo objetivo

- **Legacy:** Runtime cuyo metadata.segment reportado por Fury es legacy. Es estado de migración: se mueve a nonsite (prod) o nonprod (resto) antes de tomar nombre canónico.
- **Segmented:** Runtime asignado explícitamente a nonprod o nonsite. RIO aporta el nombre base y Fury agrega el segmento al nombre visible.
- Contrato mínimo en cada repositorio: `prod`, `stage` y `alpha`.
- Ambientes adicionales: `beta` y `gamma`, sólo cuando existan end-to-end.
- Segmentos: `prod → nonsite`; `stage|alpha|beta|gamma → nonprod`.
- RIO define el nombre base `<ambiente>-<rol>[-<qualifier>]`; Fury agrega siempre `-<segmento>` y materializa el nombre visible (`alpha-api` → `alpha-api-nonprod`).

## Propuesta ejecutiva

- **Propuesta:** Usar la segmentación obligatoria de KMS como primer slice vertical del estándar.
- **Qué ganamos:** Cumplimiento, salida de legacy, naming verificable, canary/rollback y plantilla reusable para RIO.
- **Qué implica:** Confirmar el nombre aceptado por Fury; desacoplar profile del último token; crear scope+routes; desplegar, probar y mover tráfico gradualmente.

> [!warning] Piloto KMS · deadline 2026-09-09
> `test` → base RIO `alpha-api` → visible Fury `alpha-api-nonprod`. `test-nonprod` queda sólo como bridge si el flujo obligatorio lo exige. KMS usa hoy el último token de SCOPE como Spring profile; con el sufijo Fury nonprod/nonsite cargaría el profile físico en vez del ambiente lógico.

## Routing de ambientes

1. El front resuelve `frontend` y `backend` por eje: queryParam → cookie MeliLab → `prod`.
2. nginx sirve el build de frontend y el front traduce `backend` al header estándar de scope para Fury routes.
3. Playmaker valida el scope y estampa el tag `scope:<environment_scope>` en cada mensaje.
4. El consumer Fury filtra por ese tag y vuelve a validar el scope como defensa en profundidad.

> Los filtros BigQueue transportan tags de negocio arbitrarios; `scope:<x>` sigue el patrón productivo verificado. Falta confirmar si Fury filtra server-side: si no, prod usa un topic separado y nonprod comparte topic+filtro.

## Propuesta por aplicación

### `rio-controlplane-clickhouse`

Mínimo por tipo con naming <env>-<role>-<segment>. Consumers ya consolidados por grupo; Streams sujetos a decisión; el job de test queda marcado para retiro.

| Cambio | Ambiente | Scope | Tipo | Segmento / destino |
|---|---|---|---|---|
| RETIRAR | prod | `bq-prod-nonsite` | bigqueue | prod-consumer-nonsite |
| RETIRAR | prod | `consumer-prod` | bigqueue | prod-consumer-nonsite |
| RETIRAR | prod | `prod` | web | prod-api-nonsite |
| RETIRAR | prod | `prod-deployment-events` | stream | prod-events-nonsite |
| RETIRAR | stage | `stage` | web | stage-api-nonprod |
| RETIRAR | stage | `stage-events` | stream | stage-events-nonprod |
| RETIRAR | alpha | `bq-test-nonprod` | bigqueue | alpha-consumer-nonprod |
| RETIRAR | alpha | `jobs1-test` | job | alpha-job-nonprod |
| RETIRAR | alpha | `test` | web | alpha-api-nonprod |
| RETIRAR | alpha | `test-events` | stream | alpha-events-nonprod |
| AGREGAR | prod | `prod-api-nonsite` | web | nonsite |
| AGREGAR | prod | `prod-consumer-nonsite` | bigqueue | nonsite |
| AGREGAR | prod | `prod-events-nonsite` * | stream | nonsite |
| AGREGAR | stage | `stage-api-nonprod` | web | nonprod |
| AGREGAR | stage | `stage-consumer-nonprod` | bigqueue | nonprod |
| AGREGAR | stage | `stage-events-nonprod` * | stream | nonprod |
| AGREGAR | alpha | `alpha-api-nonprod` | web | nonprod |
| AGREGAR | alpha | `alpha-consumer-nonprod` | bigqueue | nonprod |
| AGREGAR | alpha | `alpha-events-nonprod` * | stream | nonprod |
| AGREGAR | alpha | `alpha-job-nonprod` | job | nonprod |

### `rio-controlplane-flink`

Un runtime por tipo y grupo. runtime-status y el web de materializer se colapsan en api salvo particularidad; consumers de test/staging consolidados.

| Cambio | Ambiente | Scope | Tipo | Segmento / destino |
|---|---|---|---|---|
| RETIRAR | prod | `bq-consumer-nonsite` | bigqueue | prod-consumer-nonsite |
| RETIRAR | prod | `consumer-prod` | bigqueue | prod-consumer-nonsite |
| RETIRAR | prod | `production` | web | prod-api-nonsite |
| RETIRAR | prod | `rio-sdk-events-prod` | stream | prod-events-nonsite |
| RETIRAR | prod | `runtime-status-nonsite` | web | prod-api-nonsite |
| RETIRAR | stage | `consumer-stage` | bigqueue | stage-consumer-nonprod |
| RETIRAR | stage | `rio-sdk-events-stage` | stream | stage-events-nonprod |
| RETIRAR | stage | `stage` | web | stage-api-nonprod |
| RETIRAR | stage | `staging-consumer-nonprod-nonprod` | bigqueue | stage-consumer-nonprod |
| RETIRAR | stage | `staging-nonprod` | web | stage-api-nonprod |
| RETIRAR | alpha | `bq-consumer-nonprod` | bigqueue | alpha-consumer-nonprod |
| RETIRAR | alpha | `develop` | web | alpha-api-nonprod |
| RETIRAR | alpha | `jobs-test-nonprod` | job | alpha-job-nonprod |
| RETIRAR | alpha | `materializer-test-nonprod` | web | alpha-api-nonprod |
| RETIRAR | alpha | `rio-sdk-events-test` | stream | alpha-events-nonprod |
| RETIRAR | alpha | `test` | web | alpha-api-nonprod |
| RETIRAR | alpha | `test-nonprod` | web | alpha-api-nonprod |
| AGREGAR | prod | `prod-api-nonsite` | web | nonsite |
| AGREGAR | prod | `prod-consumer-nonsite` | bigqueue | nonsite |
| AGREGAR | prod | `prod-events-nonsite` * | stream | nonsite |
| AGREGAR | stage | `stage-api-nonprod` | web | nonprod |
| AGREGAR | stage | `stage-consumer-nonprod` | bigqueue | nonprod |
| AGREGAR | stage | `stage-events-nonprod` * | stream | nonprod |
| AGREGAR | alpha | `alpha-api-nonprod` | web | nonprod |
| AGREGAR | alpha | `alpha-consumer-nonprod` | bigqueue | nonprod |
| AGREGAR | alpha | `alpha-events-nonprod` * | stream | nonprod |
| AGREGAR | alpha | `alpha-job-nonprod` | job | nonprod |

### `rio-controlplane-fury`

De 6 a 4 tipos por grupo. inbound/outbound colapsados en api salvo criterio 3; orchestrator normalizado a consumer; pusher a events; TP como processor.

| Cambio | Ambiente | Scope | Tipo | Segmento / destino |
|---|---|---|---|---|
| RETIRAR | prod | `inbound-nonsite` | web | prod-api-nonsite |
| RETIRAR | prod | `orchestrator-nonsite` | bigqueue | prod-consumer-nonsite |
| RETIRAR | prod | `outbound-nonsite` | web | prod-api-nonsite |
| RETIRAR | prod | `prod-low--tp-nonsite` | template_processing | prod-processor-nonsite |
| RETIRAR | prod | `prod-nonsite` | web | prod-api-nonsite |
| RETIRAR | prod | `pusher-sink-prod-nonsite` | stream | prod-events-nonsite |
| RETIRAR | stage | `pusher-sink-stage-nonprod` | stream | stage-events-nonprod |
| RETIRAR | stage | `stage-nonprod` | web | stage-api-nonprod |
| RETIRAR | alpha | `inbound-nonprod` | web | alpha-api-nonprod |
| RETIRAR | alpha | `orchestrator-nonprod` | bigqueue | alpha-consumer-nonprod |
| RETIRAR | alpha | `outbound-nonprod` | web | alpha-api-nonprod |
| RETIRAR | alpha | `prod-default-test--tp` | template_processing | alpha-processor-nonprod |
| RETIRAR | alpha | `prod-test--tp-nonprod` | template_processing | alpha-processor-nonprod |
| RETIRAR | alpha | `pusher-sink-test-nonprod` | stream | alpha-events-nonprod |
| RETIRAR | alpha | `test-nonprod` | web | alpha-api-nonprod |
| AGREGAR | prod | `prod-api-nonsite` | web | nonsite |
| AGREGAR | prod | `prod-consumer-nonsite` | bigqueue | nonsite |
| AGREGAR | prod | `prod-events-nonsite` * | stream | nonsite |
| AGREGAR | prod | `prod-processor-nonsite` | template_processing | nonsite |
| AGREGAR | stage | `stage-api-nonprod` | web | nonprod |
| AGREGAR | stage | `stage-consumer-nonprod` | bigqueue | nonprod |
| AGREGAR | stage | `stage-events-nonprod` * | stream | nonprod |
| AGREGAR | stage | `stage-processor-nonprod` | template_processing | nonprod |
| AGREGAR | alpha | `alpha-api-nonprod` | web | nonprod |
| AGREGAR | alpha | `alpha-consumer-nonprod` | bigqueue | nonprod |
| AGREGAR | alpha | `alpha-events-nonprod` * | stream | nonprod |
| AGREGAR | alpha | `alpha-processor-nonprod` | template_processing | nonprod |

### `rio-controlplane-kafka`

Un Web y un consumer por grupo; se retira el par legacy/segmented duplicado de producción.

| Cambio | Ambiente | Scope | Tipo | Segmento / destino |
|---|---|---|---|---|
| RETIRAR | prod | `production` | web | prod-api-nonsite |
| RETIRAR | prod | `rio-consumer` | bigqueue | prod-consumer-nonsite |
| RETIRAR | prod | `rio-consumer-nonsite` | bigqueue | prod-consumer-nonsite |
| RETIRAR | alpha | `bq-kafka-materialize-test-nonprod` | bigqueue | alpha-consumer-nonprod |
| RETIRAR | alpha | `rio-consumer-test-nonprod` | bigqueue | alpha-consumer-nonprod |
| RETIRAR | alpha | `test` | web | alpha-api-nonprod |
| RETIRAR | alpha | `test-nonprod` | web | alpha-api-nonprod |
| AGREGAR | prod | `prod-api-nonsite` | web | nonsite |
| AGREGAR | prod | `prod-consumer-nonsite` | bigqueue | nonsite |
| AGREGAR | stage | `stage-api-nonprod` | web | nonprod |
| AGREGAR | stage | `stage-consumer-nonprod` | bigqueue | nonprod |
| AGREGAR | alpha | `alpha-api-nonprod` | web | nonprod |
| AGREGAR | alpha | `alpha-consumer-nonprod` | bigqueue | nonprod |

### `rio-controlplane-kms`

Piloto de la migración obligatoria: RIO define alpha-api y Fury materializa alpha-api-nonprod. test-nonprod es sólo bridge si Fury lo exige.

| Cambio | Ambiente | Scope | Tipo | Segmento / destino |
|---|---|---|---|---|
| RETIRAR | prod | `prod` | web | prod-api-nonsite |
| RETIRAR | stage | `stage` | web | stage-api-nonprod |
| RETIRAR | alpha | `test` | web | alpha-api-nonprod |
| AGREGAR | prod | `prod-api-nonsite` | web | nonsite |
| AGREGAR | stage | `stage-api-nonprod` | web | nonprod |
| AGREGAR | alpha | `alpha-api-nonprod` | web | nonprod |

### `rio-controlplane-observability`

Un Web y un consumer por grupo; se consolida el consumer productivo legacy/segmented.

| Cambio | Ambiente | Scope | Tipo | Segmento / destino |
|---|---|---|---|---|
| RETIRAR | prod | `consumer-prod` | bigqueue | prod-consumer-nonsite |
| RETIRAR | prod | `consumer-prod-nonsite` | bigqueue | prod-consumer-nonsite |
| RETIRAR | prod | `prod` | web | prod-api-nonsite |
| RETIRAR | alpha | `consumer-test-nonprod` | bigqueue | alpha-consumer-nonprod |
| RETIRAR | alpha | `test` | web | alpha-api-nonprod |
| AGREGAR | prod | `prod-api-nonsite` | web | nonsite |
| AGREGAR | prod | `prod-consumer-nonsite` | bigqueue | nonsite |
| AGREGAR | stage | `stage-api-nonprod` | web | nonprod |
| AGREGAR | stage | `stage-consumer-nonprod` | bigqueue | nonprod |
| AGREGAR | alpha | `alpha-api-nonprod` | web | nonprod |
| AGREGAR | alpha | `alpha-consumer-nonprod` | bigqueue | nonprod |

### `rio-controlplane-signals`

Consumer de señales replicado por grupo; la app no expone runtime Web. Cada consumer recibe sólo eventos de su ambiente.

| Cambio | Ambiente | Scope | Tipo | Segmento / destino |
|---|---|---|---|---|
| RETIRAR | alpha | `bq-consumer-nonprod` | bigqueue | alpha-consumer-nonprod |
| AGREGAR | prod | `prod-consumer-nonsite` | bigqueue | nonsite |
| AGREGAR | stage | `stage-consumer-nonprod` | bigqueue | nonprod |
| AGREGAR | alpha | `alpha-consumer-nonprod` | bigqueue | nonprod |

### `rio-materializer`

Un runtime principal, un stream y un work queue por grupo. Variantes api/test/dev y el ex-beta se colapsan en alpha; beta/gamma sólo si son ambientes reales end-to-end.

| Cambio | Ambiente | Scope | Tipo | Segmento / destino |
|---|---|---|---|---|
| RETIRAR | prod | `production` | web | prod-api-nonsite |
| RETIRAR | prod | `stream-production` | stream | prod-events-nonsite |
| RETIRAR | prod | `work-queues-production` | work_queue | prod-worker-nonsite |
| RETIRAR | stage | `api-stage` | web | stage-api-nonprod |
| RETIRAR | stage | `stage` | web | stage-api-nonprod |
| RETIRAR | stage | `stream-stage` | stream | stage-events-nonprod |
| RETIRAR | stage | `work-queues-stage` | work_queue | stage-worker-nonprod |
| RETIRAR | alpha | `api-test` | web | alpha-api-nonprod |
| RETIRAR | alpha | `api2-test` | web | alpha-api-nonprod |
| RETIRAR | alpha | `dev` | web | alpha-api-nonprod |
| RETIRAR | alpha | `stream-test` | stream | alpha-events-nonprod |
| RETIRAR | alpha | `test` | web | alpha-api-nonprod |
| RETIRAR | alpha | `work-queues-test` | work_queue | alpha-worker-nonprod |
| AGREGAR | prod | `prod-api-nonsite` | web | nonsite |
| AGREGAR | prod | `prod-events-nonsite` * | stream | nonsite |
| AGREGAR | prod | `prod-worker-nonsite` | work_queue | nonsite |
| AGREGAR | stage | `stage-api-nonprod` | web | nonprod |
| AGREGAR | stage | `stage-events-nonprod` * | stream | nonprod |
| AGREGAR | stage | `stage-worker-nonprod` | work_queue | nonprod |
| AGREGAR | alpha | `alpha-api-nonprod` | web | nonprod |
| AGREGAR | alpha | `alpha-events-nonprod` * | stream | nonprod |
| AGREGAR | alpha | `alpha-worker-nonprod` | work_queue | nonprod |

### `rio-playmaker`

Playmaker define los grupos end-to-end: un Web, un consumer y un stream por grupo. Los múltiples webs de test y los ex beta/gamma se colapsan en alpha.

| Cambio | Ambiente | Scope | Tipo | Segmento / destino |
|---|---|---|---|---|
| RETIRAR | prod | `bq-consumer-production` | bigqueue | prod-consumer-nonsite |
| RETIRAR | prod | `bq-production-nonsite` | bigqueue | prod-consumer-nonsite |
| RETIRAR | prod | `deployment-production` | stream | prod-events-nonsite |
| RETIRAR | prod | `production` | web | prod-api-nonsite |
| RETIRAR | stage | `bq-consumer-stage-nonprod` | bigqueue | stage-consumer-nonprod |
| RETIRAR | stage | `deployment-stage` | stream | stage-events-nonprod |
| RETIRAR | stage | `stage` | web | stage-api-nonprod |
| RETIRAR | alpha | `bq-consumer-test-nonprod` | bigqueue | alpha-consumer-nonprod |
| RETIRAR | alpha | `bq-test-nonprod` | bigqueue | alpha-consumer-nonprod |
| RETIRAR | alpha | `deployment-serverless-test` | stream | alpha-events-nonprod |
| RETIRAR | alpha | `frontend-test` | web | alpha-api-nonprod |
| RETIRAR | alpha | `stage-nonprod` | web | alpha-api-nonprod |
| RETIRAR | alpha | `test` | web | alpha-api-nonprod |
| RETIRAR | alpha | `test-front1-nonprod` | web | alpha-api-nonprod |
| RETIRAR | alpha | `test-front2-nonprod` | web | alpha-api-nonprod |
| RETIRAR | alpha | `test2` | web | alpha-api-nonprod |
| RETIRAR | alpha | `test3` | web | alpha-api-nonprod |
| AGREGAR | prod | `prod-api-nonsite` | web | nonsite |
| AGREGAR | prod | `prod-consumer-nonsite` | bigqueue | nonsite |
| AGREGAR | prod | `prod-events-nonsite` * | stream | nonsite |
| AGREGAR | stage | `stage-api-nonprod` | web | nonprod |
| AGREGAR | stage | `stage-consumer-nonprod` | bigqueue | nonprod |
| AGREGAR | stage | `stage-events-nonprod` * | stream | nonprod |
| AGREGAR | alpha | `alpha-api-nonprod` | web | nonprod |
| AGREGAR | alpha | `alpha-consumer-nonprod` | bigqueue | nonprod |
| AGREGAR | alpha | `alpha-events-nonprod` * | stream | nonprod |

### `rio-sdk-events`

El SDK no levanta runtimes Fury; publica el mismo contrato environment_scope para prod, stage y alpha.

| Cambio | Ambiente | Scope | Tipo | Segmento / destino |
|---|---|---|---|---|
| AGREGAR | prod | `prod-contract-nonsite` | contract | nonsite |
| AGREGAR | stage | `stage-contract-nonprod` | contract | nonprod |
| AGREGAR | alpha | `alpha-contract-nonprod` | contract | nonprod |

## Estado actual por scope

| Aplicación / scope | Tipo | Segmento | Infra | Fury config desplegada | Latest approved | Comparación |
|---|---|---|---|---|---|---|
| `rio-controlplane-clickhouse/bq-prod-nonsite` | bigqueue | nonsite | consumer activo · 2 | no expuesta | no encontrada | not_reported |
| `rio-controlplane-clickhouse/consumer-prod` | bigqueue | legacy | consumer activo · 1 | no expuesta | no encontrada | not_reported |
| `rio-controlplane-clickhouse/prod` | web | legacy | Fury route | no expuesta | no encontrada | not_reported |
| `rio-controlplane-clickhouse/prod-deployment-events` | stream | legacy | sink pausado · 1 | no expuesta | no encontrada | not_reported |
| `rio-controlplane-clickhouse/stage-events` | stream | legacy | sink pausado · 1 | no expuesta | no encontrada | not_reported |
| `rio-controlplane-clickhouse/test-events` | stream | legacy | sink pausado · 1 | no expuesta | no encontrada | not_reported |
| `rio-controlplane-clickhouse/bq-test-nonprod` | bigqueue | nonprod | consumer activo · 2 | no expuesta | no encontrada | not_reported |
| `rio-controlplane-clickhouse/jobs1-test` | job | legacy | no aplica | no expuesta | no encontrada | not_reported |
| `rio-controlplane-clickhouse/stage` | web | legacy | Fury route | no expuesta | no encontrada | not_reported |
| `rio-controlplane-clickhouse/test` | web | legacy | Fury route | no expuesta | no encontrada | not_reported |
| `rio-controlplane-flink/bq-consumer-nonsite` | bigqueue | nonsite | consumer activo · 2 | cfg-0.0.3 | cfg-0.0.3 | current |
| `rio-controlplane-flink/consumer-prod` | bigqueue | legacy | consumer pausado · 1 | cfg-0.0.2 | cfg-0.0.2 | current |
| `rio-controlplane-flink/consumer-stage` | bigqueue | legacy | consumer activo · 1 | 3.0.1783028253891 | 3.0.1783028253891 | current |
| `rio-controlplane-flink/production` | web | legacy | Fury route | cfg-0.0.3 | cfg-0.0.3 | current |
| `rio-controlplane-flink/rio-sdk-events-prod` | stream | legacy | sink pausado · 1 | cfg-0.0.2 | cfg-0.0.2 | current |
| `rio-controlplane-flink/runtime-status-nonsite` | web | nonsite | Fury route | cfg-0.0.7 | cfg-0.0.7 | current |
| `rio-controlplane-flink/bq-consumer-nonprod` | bigqueue | nonprod | consumer activo · 3 | cfg-0.0.8 | cfg-0.0.8 | current |
| `rio-controlplane-flink/develop` | web | legacy | Fury route | 3.0.1763467433945 | 3.0.1763467433945 | current |
| `rio-controlplane-flink/jobs-test-nonprod` | job | nonprod | no aplica | 3.0.1775666088247 | 3.0.1775666088247 | current |
| `rio-controlplane-flink/materializer-test-nonprod` | web | nonprod | Fury route | 3.0.1778185887555 | 3.0.1778185887555 | current |
| `rio-controlplane-flink/rio-sdk-events-stage` | stream | legacy | sink pausado · 1 | cfg-0.0.2 | cfg-0.0.2 | current |
| `rio-controlplane-flink/rio-sdk-events-test` | stream | legacy | sink pausado · 1 | cfg-0.0.10 | cfg-0.0.10 | current |
| `rio-controlplane-flink/stage` | web | legacy | Fury route | cfg-0.0.9 | cfg-0.0.9 | current |
| `rio-controlplane-flink/staging-consumer-nonprod-nonprod` | bigqueue | nonprod | consumer activo · 1 | 3.0.1784664733593 | 3.0.1784664733593 | current |
| `rio-controlplane-flink/staging-nonprod` | web | nonprod | Fury route | cfg-0.0.27 | cfg-0.0.27 | current |
| `rio-controlplane-flink/test` | web | legacy | Fury route | cfg-0.0.15 | cfg-0.0.15 | current |
| `rio-controlplane-flink/test-nonprod` | web | nonprod | Fury route | 3.0.1784584727753 | 3.0.1784584727753 | current |
| `rio-controlplane-fury/inbound-nonsite` | web | nonsite | Fury route | no expuesta | no encontrada | not_reported |
| `rio-controlplane-fury/orchestrator-nonsite` | bigqueue | nonsite | consumer activo · 1 | no expuesta | no encontrada | not_reported |
| `rio-controlplane-fury/outbound-nonsite` | web | nonsite | Fury route | no expuesta | no encontrada | not_reported |
| `rio-controlplane-fury/prod-low--tp-nonsite` | template_processing | nonsite | no aplica | no expuesta | no encontrada | not_reported |
| `rio-controlplane-fury/prod-nonsite` | web | nonsite | Fury route | no expuesta | no encontrada | not_reported |
| `rio-controlplane-fury/pusher-sink-prod-nonsite` | stream | nonsite | sin sink HTTP directo | no expuesta | no encontrada | not_reported |
| `rio-controlplane-fury/inbound-nonprod` | web | nonprod | Fury route | no expuesta | no encontrada | not_reported |
| `rio-controlplane-fury/orchestrator-nonprod` | bigqueue | nonprod | consumer activo · 1 | no expuesta | no encontrada | not_reported |
| `rio-controlplane-fury/outbound-nonprod` | web | nonprod | Fury route | no expuesta | no encontrada | not_reported |
| `rio-controlplane-fury/prod-default-test--tp` | template_processing | legacy | no aplica | no expuesta | no encontrada | not_reported |
| `rio-controlplane-fury/prod-test--tp-nonprod` | template_processing | nonprod | no aplica | no expuesta | no encontrada | not_reported |
| `rio-controlplane-fury/pusher-sink-stage-nonprod` | stream | nonprod | sin sink HTTP directo | no expuesta | no encontrada | not_reported |
| `rio-controlplane-fury/pusher-sink-test-nonprod` | stream | nonprod | sin sink HTTP directo | no expuesta | no encontrada | not_reported |
| `rio-controlplane-fury/stage-nonprod` | web | nonprod | Fury route | no expuesta | no encontrada | not_reported |
| `rio-controlplane-fury/test-nonprod` | web | nonprod | Fury route | no expuesta | no encontrada | not_reported |
| `rio-controlplane-kafka/production` | web | legacy | Fury route | no expuesta | cfg-0.0.1 | deployed_version_not_exposed |
| `rio-controlplane-kafka/rio-consumer` | bigqueue | legacy | consumer activo · 1 | cfg-0.0.2 | cfg-0.0.2 | current |
| `rio-controlplane-kafka/rio-consumer-nonsite` | bigqueue | nonsite | consumer activo · 3 | cfg-0.0.2 | cfg-0.0.2 | current |
| `rio-controlplane-kafka/bq-kafka-materialize-test-nonprod` | bigqueue | nonprod | consumer activo · 3 | cfg-0.0.5 | cfg-0.0.5 | current |
| `rio-controlplane-kafka/rio-consumer-test-nonprod` | bigqueue | nonprod | consumer activo · 2 | 3.0.1781881907797 | 3.0.1781881907797 | current |
| `rio-controlplane-kafka/test` | web | legacy | Fury route | cfg-0.0.9 | cfg-0.0.9 | current |
| `rio-controlplane-kafka/test-nonprod` | web | nonprod | Fury route | no expuesta | no encontrada | not_reported |
| `rio-controlplane-kms/prod` | web | legacy | Fury route | no expuesta | no encontrada | not_reported |
| `rio-controlplane-kms/stage` | web | legacy | Fury route | no expuesta | no encontrada | not_reported |
| `rio-controlplane-kms/test` | web | legacy | Fury route | no expuesta | no encontrada | not_reported |
| `rio-controlplane-observability/consumer-prod` | bigqueue | legacy | consumer activo · 1 | cfg-0.0.1 | cfg-0.0.1 | current |
| `rio-controlplane-observability/consumer-prod-nonsite` | bigqueue | nonsite | consumer activo · 1 | 3.0.1784041760064 | 3.0.1784041760064 | current |
| `rio-controlplane-observability/prod` | web | legacy | Fury route | cfg-0.0.3 | cfg-0.0.3 | current |
| `rio-controlplane-observability/consumer-test-nonprod` | bigqueue | nonprod | consumer activo · 2 | no expuesta | no encontrada | not_reported |
| `rio-controlplane-observability/test` | web | legacy | Fury route | no expuesta | no encontrada | not_reported |
| `rio-controlplane-signals/bq-consumer-nonprod` | bigqueue | nonprod | consumer activo · 1 | cfg-0.0.1 | cfg-0.0.1 | current |
| `rio-materializer/production` | web | legacy | Fury route | no expuesta | no encontrada | not_reported |
| `rio-materializer/stream-production` | stream | legacy | sink pausado · 1 | no expuesta | no encontrada | not_reported |
| `rio-materializer/work-queues-production` | work_queue | legacy | worker group activo · 1 | no expuesta | no encontrada | not_reported |
| `rio-materializer/api-stage` | web | legacy | Fury route | no expuesta | no encontrada | not_reported |
| `rio-materializer/api-test` | web | legacy | Fury route | no expuesta | no encontrada | not_reported |
| `rio-materializer/api2-test` | web | legacy | Fury route | no expuesta | no encontrada | not_reported |
| `rio-materializer/dev` | web | legacy | Fury route | no expuesta | no encontrada | not_reported |
| `rio-materializer/stage` | web | legacy | Fury route | no expuesta | no encontrada | not_reported |
| `rio-materializer/stream-stage` | stream | legacy | sink pausado · 1 | no expuesta | no encontrada | not_reported |
| `rio-materializer/stream-test` | stream | legacy | sink pausado · 1 | no expuesta | no encontrada | not_reported |
| `rio-materializer/test` | web | legacy | Fury route | no expuesta | no encontrada | not_reported |
| `rio-materializer/work-queues-stage` | work_queue | legacy | worker group activo · 1 | no expuesta | no encontrada | not_reported |
| `rio-materializer/work-queues-test` | work_queue | legacy | worker group activo · 1 | no expuesta | no encontrada | not_reported |
| `rio-playmaker/bq-consumer-production` | bigqueue | legacy | consumer activo · 3 | 3.0.1778627308622 | 3.0.1778627308622 | current |
| `rio-playmaker/bq-production-nonsite` | bigqueue | nonsite | consumer activo · 1 | 3.0.1783372804994 | cfg-0.0.1 | different |
| `rio-playmaker/deployment-production` | stream | legacy | sink pausado · 1 | 3.0.1769190068558 | cfg-0.0.1 | different |
| `rio-playmaker/production` | web | legacy | Fury route | cfg-0.0.4 | cfg-0.0.4 | current |
| `rio-playmaker/bq-consumer-stage-nonprod` | bigqueue | nonprod | consumer activo · 3 | 3.0.1779483169773 | 3.0.1779483169773 | current |
| `rio-playmaker/bq-consumer-test-nonprod` | bigqueue | nonprod | consumer activo · 3 | cfg-0.0.5 | cfg-0.0.5 | current |
| `rio-playmaker/bq-test-nonprod` | bigqueue | nonprod | consumer activo · 1 | cfg-0.0.1 | cfg-0.0.1 | current |
| `rio-playmaker/deployment-serverless-test` | stream | legacy | sink pausado · 1 | 3.0.1768355906077 | 3.0.1768355906077 | current |
| `rio-playmaker/deployment-stage` | stream | legacy | sink pausado · 1 | cfg-0.0.1 | cfg-0.0.1 | current |
| `rio-playmaker/frontend-test` | web | legacy | Fury route | cfg-0.0.5 | cfg-0.0.5 | current |
| `rio-playmaker/stage` | web | legacy | Fury route | cfg-0.0.5 | cfg-0.0.5 | current |
| `rio-playmaker/stage-nonprod` | web | nonprod | Fury route | 3.0.1779822017542 | 3.0.1779822017542 | current |
| `rio-playmaker/test` | web | legacy | Fury route | cfg-0.0.6 | cfg-0.0.6 | current |
| `rio-playmaker/test-front1-nonprod` | web | nonprod | Fury route | no expuesta | no encontrada | not_reported |
| `rio-playmaker/test-front2-nonprod` | web | nonprod | Fury route | no expuesta | no encontrada | not_reported |
| `rio-playmaker/test2` | web | legacy | Fury route | cfg-0.0.2 | cfg-0.0.2 | current |
| `rio-playmaker/test3` | web | legacy | Fury route | cfg-0.0.6 | cfg-0.0.6 | current |

## Contrato de extensión

Secrets y KVS están reservados como tipos de recurso. Hasta que exista collector se registran `not_collected`, nunca `ausentes`.

## Evidencia y provenance

- Runtime, segmentos, bindings y routes: Fury service graph read-only.
- Config deployed: `metadata.application_config_version`; latest approved: Config Orchestrator batch por aplicación/scope.
- Config de código: resolución del checkout local con commit/branch registrados; no se presenta como Fury config.
- Propuesta: `rio-scope-policy.json`, curada y separada de los hechos.

## Relaciones

- Proyecto: [[Estandarización de Scopes RIO]]
- Spec: [[scope-naming-standard]]
- Routing: [[scope-compatibility-matrix]]

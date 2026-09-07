---
type: resource
schema_version: 1
status: active
area: "[[Meli]]"
project: "[[Estandarización de Scopes RIO]]"
sources:
  - "[[Fury — Inventario live de scopes RIO (2026-08-12)]]"
  - "[[scope-inventory]]"
  - "[[integration-map]]"
  - "[[deploy-request-path]]"
last_verified: 2026-08-12
confidence: verified
aliases:
  - Matriz de compatibilidad de scopes RIO
  - RIO scope compatibility matrix
  - Inventario 4 scopes RIO
  - Playmaker to CP scope matrix
tags:
  - kind/resource
  - tech/rio
  - project/scopes-rio
created: 2026-08-12
updated: 2026-08-12
cssclasses:
  - wide
---

# RIO — Matriz de routing de scopes (Inventario 4)

## Síntesis vigente

Este es el resultado de `Inventario 4`: la matriz **end-to-end de routing a nivel de scope** que conecta cada canal BigQueue con el scope de [[rio-playmaker]] que lo produce/consume y el scope de cada control plane que lo atiende. Se construyó cruzando el grafo de canales de [[integration-map]], el transporte de [[deploy-request-path]] y los scopes de [[scope-inventory]], y se **cerró el eslabón canal↔scope** con la superficie que faltaba: `fury services bigq consumers list` por repo, que lista `consumer name · scope · delivery mode · test · status`. Los bindings `topic↔scope` y el rol `producer/consumer` se verificaron además contra los `application*.yml` de cada repo (bloques `events.bigqueue.topics` anotados `PRODUCER`/`CONSUMER`).

**Hallazgo central para el estándar:** la combinación **`canal` + `segmento Fury`** es la clave de routing observable en esta superficie, no una prueba suficiente de compatibilidad funcional. Un mismo canal en un mismo segmento es atendido por scopes con nombres completamente distintos en cada CP. Ejemplo — `rio-deployment-trigger` segmento `nonprod`: lo consumen `bq-kafka-materialize-test-nonprod` (kafka), `bq-consumer-nonprod` (flink), `bq-test-nonprod` (clickhouse), `orchestrator-nonprod` (fury) y `consumer-test-nonprod` (observability). El nombre del scope no permite inferir mecánicamente ni el canal ni el segmento, pero compartir `(canal, segmento)` tampoco demuestra por sí solo compatibilidad de contrato, versión, sitio, aislamiento lógico o tráfico real.

## Alcance probado y gate pendiente

La matriz prueba **topología y estado de registro**: qué consumer está asociado a qué scope, sobre qué canal y segmento, y si Fury lo reporta `running` o `paused`. Para declarar compatibilidad end-to-end todavía se requiere un manifiesto verificable con al menos `application`, `scope`, `lane/celda lógica`, `role/workload`, `channel físico`, `infra-segment`, dirección `produce|consume`, contrato/schema y versión compatible, sitio/tenant cuando aplique, y evidencia operacional dentro de una ventana acordada. Hasta que ese manifiesto exista, `(canal, segmento)` se usa como clave de routing necesaria, no como criterio suficiente de compatibilidad.

**Cobertura actual:** 40 consumidores BigQueue mapeados (39 `running`, 1 `paused`) sobre 7 aplicaciones. El service graph agregó `rio-controlplane-signals/deployment-consumer--nonprod`, unido a `bq-consumer-nonprod` y al topic `rio-deployment-trigger--nonprod.rio-playmaker`. [[rio-controlplane-kms]], [[rio-materializer]] y [[rio-sdk-events]] no tienen consumers BigQueue runtime. Los **triggers** viajan por BigQueue con entrega HTTP push; los **results/status** vuelven por BigQueue como `PRODUCER` del CP → `CONSUMER` de Playmaker.

## Convención de segmento y canales canónicos

**Segmento Fury (verificado en código):** el sufijo del consumidor codifica el segmento de data-plane, no el ambiente lógico.

| Sufijo consumidor | Segmento Fury | Ambiente lógico asociado | Evidencia |
|---|---|---|---|
| `--nonprod` | `nonprod` | test / stage | `application-nonprod.yml`: "in nonprod the action result/trigger topics carry a `-test` suffix" |
| `--nonsite` | `nonsite` | production | `application-nonsite.yml`: "prod == nonsite for the data-plane segment" |

**Canales canónicos (logical topics, verificados como `PRODUCER`/`CONSUMER` en `application*.yml`):**

| Canal (logical) | Kind | Producer | Consumers | Transporte |
|---|---|---|---|---|
| `rio-action-trigger` | trigger | [[rio-playmaker]] (web) | kafka, flink, clickhouse | BigQueue (HTTP push) |
| `rio-deployment-trigger` | trigger | [[rio-playmaker]] (web) | kafka, flink, clickhouse, fury, observability | BigQueue (HTTP push) |
| `rio-data-product-changed` | notification | [[rio-playmaker]] (web) | observability | BigQueue (HTTP push) |
| `rio-action-result` | result | kafka, flink, clickhouse | [[rio-playmaker]] | BigQueue async |
| `rio-deployment-result` | result | kafka, flink, clickhouse, fury | [[rio-playmaker]] | BigQueue async |
| `rio-component-runtime-status` | status | flink | [[rio-playmaker]] | BigQueue async |
| `provisioning-result` | result | kafka (declarado) | — sin consumidor live | BigQueue async |
| `component-registry` (?) | registry | ? | [[rio-playmaker]] (`component-registry-test--nonprod`) | BigQueue — canal nuevo, verificar |

> [!warning] Drift de nombre físico a verificar
> Playmaker publica el trigger de acción con nombre físico distinto según perfil: `rio-actions-trigger` (plural) en `application-production.yml:65` y `application-test3.yml`/`beta`/`local`, vs `rio-action-trigger` (singular) por env var `BIGQUEUE_TOPIC_RIO_ACTION_TRIGGER__NONPROD_TOPIC_NAME` en `test`/`stage`/`staging-nonprod`. Los CP consumen el singular. Como los nombres físicos vienen de inyección Fury (env vars), el default plural puede no aplicar en runtime; es un **riesgo de mismatch a confirmar**, no una ruptura probada.

## Matriz end-to-end por canal (producer scope → consumer scope, por segmento)

Cada fila es un canal en un segmento; las celdas son los scopes que lo atienden hoy. `PM` = [[rio-playmaker]].

### Triggers (Playmaker → control planes)

| Canal | Segmento | Producer (PM, web) | kafka | flink | clickhouse | fury | observability |
|---|---|---|---|---|---|---|---|
| `rio-action-trigger` | nonprod | `test` / `stage` | `rio-consumer-test-nonprod`, `bq-kafka-materialize-test-nonprod` | `bq-consumer-nonprod` | `bq-test-nonprod` | — | — |
| `rio-action-trigger` | nonsite | `production` | `rio-consumer-nonsite` | `bq-consumer-nonsite`, ⚠️`consumer-prod` (paused) | `bq-prod-nonsite`, `consumer-prod` | — | — |
| `rio-deployment-trigger` | nonprod | `test` / `stage` | `bq-kafka-materialize-test-nonprod`, `rio-consumer-test-nonprod` | `bq-consumer-nonprod` | `bq-test-nonprod` | `orchestrator-nonprod` | `consumer-test-nonprod` |
| `rio-deployment-trigger` | nonsite | `production` | `rio-consumer-nonsite` | `bq-consumer-nonsite` | `bq-prod-nonsite` | `orchestrator-nonsite` | `consumer-prod-nonsite` |
| `rio-data-product-changed` | nonprod | `test` / `stage` | — | — | — | — | `consumer-test-nonprod` |
| `rio-data-product-changed` | nonsite | `production` | — | — | — | — | `consumer-prod` |

### Results / status (control planes → Playmaker)

| Canal | Segmento | Producer (CP scope) | Consumer (PM scope) |
|---|---|---|---|
| `rio-action-result` | nonprod | kafka/flink/clickhouse (scope de test-nonprod) | `bq-test-nonprod`, `bq-consumer-stage-nonprod` (stage) |
| `rio-action-result` | nonsite | kafka/flink/clickhouse (scope prod/nonsite) | `bq-consumer-production` |
| `rio-deployment-result` | nonprod | kafka/flink/clickhouse/fury (test-nonprod) | `bq-consumer-test-nonprod`, `bq-consumer-stage-nonprod` (stage) |
| `rio-deployment-result` | nonsite | kafka/flink/clickhouse/fury (prod/nonsite) | `bq-consumer-production` |
| `rio-component-runtime-status` | nonprod | flink (test-nonprod) | `bq-consumer-test-nonprod` |
| `rio-component-runtime-status` | nonsite | flink (prod/nonsite) | `bq-consumer-production`, `bq-production-nonsite` |
| `component-registry` (?) | nonprod | ? (verificar) | `bq-consumer-test-nonprod` |

> El producer del result es la **misma runtime del CP** que consumió el trigger, provisionó infra y publica el resultado (mismo scope consumidor; el `application.yml` declara ambos topics en el mismo perfil). Por eso el "producer scope" del result coincide con el scope consumidor del trigger del mismo CP y segmento.

## Matriz inversa — 40 consumidores BigQueue (scope que atiende cada canal)

Fuente directa: service graph read-only normalizado (2026-08-12). `seg` = `consumer.metadata.segment`; no se infiere del sufijo.

### [[rio-playmaker]] — consume results/status (rol orchestrator)

| Consumer | Scope | Canal | seg | Estado |
|---|---|---|---|---|
| `rio-action-result-consumer--nonprod` | `bq-test-nonprod` | `rio-action-result` | nonprod | running |
| `actions-consumer--nonsite` | `bq-consumer-production` | `rio-action-result` | nonsite | running |
| `result-stage--nonprod` | `bq-consumer-stage-nonprod` | `rio-action-result` (stage) | nonprod | running |
| `deployment-result--nonprod` | `bq-consumer-test-nonprod` | `rio-deployment-result` | nonprod | running |
| `deployment-result--nonsite` | `bq-consumer-production` | `rio-deployment-result` | nonsite | running |
| `deployment-result-stage--nonprod` | `bq-consumer-stage-nonprod` | `rio-deployment-result` (stage) | nonprod | running |
| `deployment-result-stage-legacy` | `bq-consumer-stage-nonprod` | `rio-deployment-result` (stage legacy) | — | running |
| `component-runtime-status--nonprod` | `bq-consumer-test-nonprod` | `rio-component-runtime-status` | nonprod | running |
| `component-runtime-status--nonsite` | `bq-consumer-production` | `rio-component-runtime-status` | nonsite | running |
| `component-runtime-status-flink--nonsite` | `bq-production-nonsite` | `rio-component-runtime-status` | nonsite | running |
| `component-registry-test--nonprod` | `bq-consumer-test-nonprod` | `component-registry` (?) | nonprod | running |

### [[rio-controlplane-kafka]] — consume triggers (rol CP)

| Consumer | Scope | Canal | seg | Estado |
|---|---|---|---|---|
| `rio-action-trigger-consumer--nonprod` | `bq-kafka-materialize-test-nonprod` | `rio-action-trigger` | nonprod | running |
| `rio-action-trigger-iso--nonprod` | `rio-consumer-test-nonprod` | `rio-action-trigger` | nonprod | running |
| `consumer-action-legacy` | `bq-kafka-materialize-test-nonprod` | `rio-action-trigger` (legacy) | nonprod | running |
| `rio-action-trigger-consumer--nonsite` | `rio-consumer-nonsite` | `rio-action-trigger` | nonsite | running |
| `rio-action-trigger-iso--nonsite` | `rio-consumer-nonsite` | `rio-action-trigger` | nonsite | running |
| `rio-consumer-legacy` | `rio-consumer` | `rio-action-trigger` (legacy) | — | running |
| `deployment-trigger-consumer--nonprod` | `bq-kafka-materialize-test-nonprod` | `rio-deployment-trigger` | nonprod | running |
| `rio-deployment-trigger-iso--nonprod` | `rio-consumer-test-nonprod` | `rio-deployment-trigger` | nonprod | running |
| `deployment-trigger-consumer--nonsite` | `rio-consumer-nonsite` | `rio-deployment-trigger` | nonsite | running |

### [[rio-controlplane-flink]] — consume triggers (rol CP)

| Consumer | Scope | Canal | seg | Estado |
|---|---|---|---|---|
| `rio-action-consumer--nonprod` | `bq-consumer-nonprod` | `rio-action-trigger` | nonprod | running |
| `rio-action-consumer--nonsite` | `bq-consumer-nonsite` | `rio-action-trigger` | nonsite | running |
| `actions-trigger--nonsite` | `consumer-prod` | `rio-action-trigger` | nonsite | **paused** |
| `rio-deployment-consumer--nonprod` | `bq-consumer-nonprod` | `rio-deployment-trigger` | nonprod | running |
| `rio-deployment-consumer--nonsite` | `bq-consumer-nonsite` | `rio-deployment-trigger` | nonsite | running |
| `cloud-controller-stage` | `consumer-stage` | trigger (action/deployment, no desambigua el nombre) | nonsite | running |
| `cloud-controller-stage-nonprod` | `bq-consumer-nonprod` | trigger (ambiguo) | nonprod | running |
| `cloud-controller-staging` | `staging-consumer-nonprod-nonprod` | trigger (ambiguo) | nonprod | running |

### [[rio-controlplane-clickhouse]] — consume triggers (rol CP)

| Consumer | Scope | Canal | seg | Estado |
|---|---|---|---|---|
| `rio-action-consumer--nonprod` | `bq-test-nonprod` | `rio-action-trigger` | nonprod | running |
| `actions-consumer--nonsite` | `consumer-prod` | `rio-action-trigger` | nonsite | running |
| `rio-action-prod-consumer--nonsite` | `bq-prod-nonsite` | `rio-action-trigger` | nonsite | running |
| `deployment-consumer--nonprod` | `bq-test-nonprod` | `rio-deployment-trigger` | nonprod | running |
| `deployment-consumer-nonsite--nonsite` | `bq-prod-nonsite` | `rio-deployment-trigger` | nonsite | running |

### [[rio-controlplane-fury]] — consume deployment-trigger (rol orchestrator/inbound)

| Consumer | Scope | Canal | seg | Estado |
|---|---|---|---|---|
| `deployment-trigger-consumer--nonprod` | `orchestrator-nonprod` | `rio-deployment-trigger` | nonprod | running |
| `deployment-trigger-consumer--nonsite` | `orchestrator-nonsite` | `rio-deployment-trigger` | nonsite | running |

### [[rio-controlplane-observability]] — consume dp-changed + deployment-trigger (rol CP)

| Consumer | Scope | Canal | seg | Estado |
|---|---|---|---|---|
| `dp-changed-consumer--nonprod` | `consumer-test-nonprod` | `rio-data-product-changed` | nonprod | running |
| `dp-changed-consumer-prod--nonsite` | `consumer-prod` | `rio-data-product-changed` | nonsite | running |
| `rio-deployment-consumer--nonprod` | `consumer-test-nonprod` | `rio-deployment-trigger` | nonprod | running |
| `rio-deployment-consumer--nonsite` | `consumer-prod-nonsite` | `rio-deployment-trigger` | nonsite | running |

### [[rio-controlplane-signals]] — consume deployment-trigger

| Consumer | Scope | Canal | seg | Estado |
|---|---|---|---|---|
| `deployment-consumer--nonprod` | `bq-consumer-nonprod` | `rio-deployment-trigger` | nonprod | running |

## Dimensiones separadas (las 4 que el estándar no debe fundir)

El proyecto exige mantener separados **ambiente lógico**, **segmento Fury**, **rol/runtime** y **aplicación**. La matriz muestra que hoy un solo token de scope intenta cargar varias de estas dimensiones a la vez, de forma inconsistente por repo.

| Dimensión | Qué es | Cómo se expresa hoy (inconsistente) | Señal confiable |
|---|---|---|---|
| Ambiente lógico | test / stage / production | token del scope (`test`, `stage`, `production`, `prod`) | perfil Spring efectivo ([[scope-inventory]]) |
| Segmento Fury | legacy / nonprod / nonsite del runtime o binding | sufijo del nombre, metadata runtime y metadata del consumer pueden diferir | `metadata.segment` del runtime y del binding, por separado |
| Rol / runtime | orchestrator, consumer, inbound, outbound, web, job, stream | prefijo del scope en CP Fury; ausente o implícito en otros | nombre del consumidor + tipo de scope |
| Aplicación | qué CP atiende el canal | nombre del repo, no del scope | `.fury application_name` |

**Contradicción de ejemplo (verificada):** flink `consumer-stage` está clasificado `Productive` en Fury pero carga perfil `stage`, y su consumidor `cloud-controller-stage` corre en segmento `nonsite`. Ambiente lógico (stage), criticidad Fury (Productive) y segmento (nonsite) apuntan a tres cosas distintas en un mismo scope.

## Hallazgos nuevos de Inventario 4

1. **`clickhouse` consume ambos triggers** (`rio-action-trigger` + `rio-deployment-trigger`) y publica `rio-action-result`/`rio-deployment-result`. Esto **cierra el gap** que [[integration-map]] dejaba abierto ("clickhouse consume trigger pero no se detectó su canal de result"): el result de clickhouse existe y viaja por los mismos topics `rio-*-result` en segmento nonsite/nonprod.
2. **`observability` consume `rio-deployment-trigger`** además de `rio-data-product-changed` — su rol no es sólo notificación; reacciona al trigger de deployment (`rio-deployment-consumer--{nonprod,nonsite}`).
3. **`consumer-prod` (flink) reforzado como `retirement-candidate`:** su único consumidor `actions-trigger--nonsite` está `paused`, y el mismo canal `rio-action-trigger` nonsite ya lo atiende `bq-consumer-nonsite/rio-action-consumer--nonsite` en `running`. La ruta pausada es **redundante** con una activa → argumento fuerte de retiro (aún requiere último mensaje + owner humano antes de ejecutar).
4. **Canal nuevo `component-registry`:** el consumidor `component-registry-test--nonprod` (playmaker) no corresponde a ninguno de los 7 canales de [[integration-map]]. Es un canal no mapeado; falta identificar su producer y contrato. **No inventar el nombre del canal**: verificar en `application*.yml` / código antes de canonizarlo.
5. **Publicación cross-segment (flink):** `application-prod.yml` documenta que `consumer-prod` (scope legacy) publica a topics del segmento `nonsite` vía `withSegmentID`; el runtime y el segmento del topic no coinciden por construcción. Es deuda de naming que el estándar debe hacer explícita o eliminar.
6. **Drift de nombre físico de topic** (`rio-actions-trigger` plural vs `rio-action-trigger` singular entre perfiles de Playmaker) — ver aviso arriba; verificar env vars inyectadas por Fury.
7. **Consumidores `legacy`/`iso`/`cloud-controller` coexisten** sobre el mismo canal y segmento (ej. kafka nonprod: `rio-action-trigger-consumer--nonprod`, `rio-action-trigger-iso--nonprod`, `consumer-action-legacy` los tres sobre `rio-action-trigger`). Duplicación transitoria que impide una relación 1:1 canal↔scope.

## Evidencia y provenance

- **Link canal↔scope:** service graph read-only `FuryApi.get_scopes()` + consumers BigQueue normalizados en `~/fuentes/rio-inspector/rio-scopes.json` (2026-08-12): 40 consumidores, 39 `running`, 1 `paused`.
- **Bindings topic↔scope y rol producer/consumer:** service graph para 7 apps con consumers + bloques `events.bigqueue.topics` y `bigqueue.*-topic` en los perfiles de código para semántica producer/consumer.
- **Grafo de canales:** [[integration-map]] (generado por [[rio-inspector]]). **Transporte y ciclo de vida:** [[deploy-request-path]]. **Scopes base:** [[scope-inventory]].
- No se persiste el dump crudo de la CLI (invariante 12); la matriz se regenera repitiendo las superficies indicadas.

## Límites y contradicciones

- La superficie de consumidores prueba **registro y estado operacional actual** (running/paused), no el timestamp del último mensaje, tráfico HTTP de triggers ni owner humano. Esta matriz no mantiene una categoría genérica de uso/desuso.
- El **producer** de un trigger no aparece como consumidor: Playmaker publica por HTTP push. El "producer scope" de triggers se deriva del scope web de Playmaker por ambiente (`test`/`stage`/`production`), no de esta superficie. Confirmar contra tráfico real si se requiere prueba de publicación.
- Canales `component-registry` y `provisioning-result` quedan **sin cerrar**: el primero no está en integration-map; el segundo está declarado en kafka pero sin consumidor live. Ambos requieren una pasada de código dedicada.
- Los consumidores `cloud-controller-*` (flink) no desambiguan canal por nombre; se marcan como trigger sin precisar action/deployment hasta verificar su binding en `application*.yml`.
- Snapshot del 2026-08-12; regenerar antes de cualquier decisión de migración o retiro.

## 🔗 Relaciones
- resultado de `Inventario 4` de [[Estandarización de Scopes RIO]]
- se apoya en [[scope-inventory]] · [[integration-map]] · [[deploy-request-path]]
- parte de [[00-index|RIO Atlas]]
- documenta [[rio-playmaker]] · [[rio-controlplane-kafka]] · [[rio-controlplane-flink]] · [[rio-controlplane-clickhouse]] · [[rio-controlplane-fury]] · [[rio-controlplane-observability]]

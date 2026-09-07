---
type: resource
schema_version: 1
status: active
area: "[[Meli]]"
project: "[[Estandarización de Scopes RIO]]"
sources:
  - "[[Fury — Inventario live de scopes RIO (2026-08-12)]]"
  - "[[scope-inventory]]"
last_verified: 2026-08-12
confidence: verified
aliases:
  - Modelo de segmentación Fury RIO
  - Fury segmentation model
  - segmentos nonprod nonsite legacy RIO
  - business segment meli infra segments
tags:
  - kind/resource
  - tech/rio
  - tech/fury
  - project/scopes-rio
created: 2026-08-12
updated: 2026-08-12
cssclasses:
  - wide
---

# Fury — Modelo de segmentación aplicado a RIO

## Síntesis vigente

Fury separa el **business segment** (a qué negocio pertenece el usuario/app: `meli`) de los **infra-segments** (en qué partición de infraestructura vive cada recurso). El `fury list-segments` del usuario devuelve business segment `meli` con infra-segments: `arg`, `bra`, `col`, `mex`, `rla` (site-specific), `nonsite` (prod sin sitio), `nonprod` (test/stage), `legacy` (partición vieja sin segmentar) y `platform`. Cada recurso segmentable (BigQueue topic, KVS container) se resuelve dentro de un infra-segment; la CLI opera con `fury <cmd> --segment meli` y `fury set-business-segment`.

**Lo importante para scopes RIO:** Fury registra un segmento efectivo para el runtime compute en `metadata.segment`, y cada recurso/binding segmentable registra además el suyo. Un mismo scope puede mezclar segmentos: el runtime, un topic, un consumer, un Stream físico o un KVS no tienen por qué coincidir. Por eso el inventario conserva `runtime_segment` y los segmentos de recurso por separado; un renombre de scope no cambia ninguno de esos hechos.

**Regla de mapeo vigente (derivada del código, no de un contrato explícito):**

| Ambiente lógico | Infra-segment de datos | Evidencia en código |
|---|---|---|
| test / stage | `nonprod` | `application-nonprod.yml`: "in nonprod the action result/trigger topics carry a `-test` suffix" |
| production (sin sitio) | `nonsite` | `application-nonsite.yml`: "prod == nonsite for the data-plane segment" |
| production (por sitio) | `arg` / `bra` / `col` / `mex` / `rla` | [[rio-controlplane-fury]] `application-prod.yml`: `segment: arg` para KVS `pusher-mappings-prd` |
| (viejo, a eliminar) | `legacy` | KVS de clickhouse, idempotencia de kafka test, `consumer-prod` de flink |

## Cómo lo declara cada recurso

- **BigQueue:** `segment-id` (o `segment_id`) por topic. El SDK `mqclient` aplica `ProducerBuilder.withSegmentID(...)` al publicar y el broker **rechaza** el publish si el segmento no coincide con el del topic provisionado (comentario en flink `application-prod.yml`). Por eso flink en `consumer-prod` (scope legacy) publica **cross-segment** a `nonsite`: el runtime vive en un segmento pero fuerza el `segmentId` del topic destino.
- **KVS:** `segment-id` por container. `withSegmentId(...)` sólo se llama si el valor no está en blanco (test `KvsConfigTest`); en blanco = routing por defecto (que hoy resuelve a la partición legacy en varios CP).
- **Scope / perfil:** algunos repos derivan el segmento del último token del `SCOPE` (flink: "derives ... from the last `-`-delimited segment of `$SCOPE`"), otros lo fijan por perfil (`application-<segmento>.yml`). No hay un mecanismo único.

## Estado runtime live (corte 2026-08-12)

El service graph read-only de Fury registra **88 runtimes** y entrega `metadata.segment` en todos: **50 `legacy`**, **26 `nonprod`** y **12 `nonsite`**. Este conteo reemplaza las 14 marcas derivadas del grid como medida del segmento runtime. No equivale al inventario de todos los recursos asociados: un runtime `nonsite` puede usar un recurso `legacy` y viceversa.

Caso verificado: `rio-controlplane-observability/consumer-prod-nonsite` tiene runtime `nonsite`, región BigQueue `us-east-1-single-nonsite` y consumer `rio-deployment-consumer--nonsite` `running` en `nonsite`. El grid anterior lo rotulaba `legacy` al colapsar una hipótesis de KVS sobre todo el scope.

### Deuda de recursos `legacy` derivada desde código

El análisis anterior marcó **14 filas de scope con exposición potencial a `legacy` derivada desde código/configuración**. Es una métrica histórica distinta y no debe aparecer como KPI del estado live: varios scopes pueden compartir un recurso, y una configuración condicional no demuestra el valor efectivo. Antes de convertirla en backlog hay que inventariar los recursos provisionados y sus `segment-id` efectivos.

- **[[rio-controlplane-clickhouse]]** — KVS en `legacy` en test/stage/prod (toda la app); los topics ya están en `nonprod`/`nonsite`. Es la mayor deuda de migración KVS.
- **[[rio-controlplane-kafka]]** — KVS de idempotencia de action-triggers con `segment-id: legacy` en `application-test.yml`, conviviendo con topics `nonprod`; scope `rio-consumer` en perfil legacy.
- **[[rio-controlplane-flink]]** — `consumer-prod` es un scope legacy que publica cross-segment a `nonsite`; candidato a retiro (ver [[scope-compatibility-matrix]]).
- **[[rio-controlplane-observability]]** — KVS con `segment-id` por env var sin default: el código sólo prueba que, sin inyección, el cliente se construye sin segmentación explícita; falta verificar el valor live y su resolución efectiva antes de etiquetar sus cinco scopes como `legacy`.

## Qué habilita la capability para el proyecto

- **Separar identidad de placement:** el nombre puede declarar intención, pero Fury registra el placement efectivo del runtime y de cada recurso. El inventario y cualquier migración deben leer esos campos, no el último token del nombre.
- **Grupos de test aislados:** es un objetivo de diseño, no una capability demostrada por este inventario. La revalidación live de `fury list-segments` sólo enumera `arg`, `bra`, `col`, `mex`, `rla`, `nonsite`, `nonprod`, `legacy` y `platform`; no expone subsegmentos arbitrarios como `nonprod-alpha`. Los consumidores `*-iso-*` prueban que existen rutas duplicadas dentro de `nonprod`, pero no prueban aislamiento por `segmentId`. El mecanismo debe validarse con Fury; mientras tanto, topics/containers físicamente separados o una capability aprobada son alternativas, no decisiones.
- **Migración legacy → segmentado como objetivo medible:** cada runtime o recurso confirmado en `legacy` es un ítem distinto. El reporte visual cuenta los 50 runtimes live; los recursos asociados requieren su propio inventario antes de planificar la migración.

## Evidencia y provenance

- `fury list-segments` (business segment `meli` + infra-segments) y `fury set-business-segment --help`, ejecutados y revalidados 2026-08-12 desde checkouts RIO en [[Fuentes — Workspace de repositorios]].
- `furycli.furyapi.FuryApi.get_scopes()` sobre `applications/<app>/services`, normalizado en `~/fuentes/rio-inspector/rio-scopes.json`, aporta `metadata.segment` runtime y los segmentos/bindings live de BigQueue, Streams y Work Queues.
- Declaraciones `segment`/`segment-id`/`segment_id` y comentarios en `application*.yml` de [[rio-playmaker]], [[rio-controlplane-kafka]], [[rio-controlplane-flink]], [[rio-controlplane-clickhouse]], [[rio-controlplane-fury]], [[rio-controlplane-observability]].
- `withSegmentID`/`withSegmentId` en SDK `mqclient` y tests de KVS (clickhouse `KvsConfigTest`).

## Límites y contradicciones

- No se accedió a la doc oficial de Fury sobre segmentación (SPA no renderizable por fetch, y el MCP de Fury no quedó conectado en la sesión); el modelo aquí se deriva de la CLI autenticada + código. Confirmar con plataforma la semántica exacta de `nonsite` vs sitios y el rol de `platform`.
- El mapeo ambiente→segmento es una **regla observada**, no un contrato declarado; hay excepciones (flink usa `segment-id: prod` para su KVS, distinto de `nonsite`).
- No hay evidencia de que `segmentId` acepte valores arbitrarios por lane dentro de `nonprod`; diseñar sobre `nonprod-<lane>` queda bloqueado hasta validación explícita de Fury.
- El snapshot de deuda `legacy` es del 2026-08-12; regenerar antes de planificar la migración.

## 🔗 Relaciones
- sustenta [[scope-naming-standard]] · [[scope-compatibility-matrix]]
- amplía [[scope-inventory]]
- parte de [[00-index|RIO Atlas]] · proyecto [[Estandarización de Scopes RIO]]

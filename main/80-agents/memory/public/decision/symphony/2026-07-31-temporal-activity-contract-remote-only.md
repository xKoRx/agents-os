---
type: decision
scope: application
created: 2026-07-31
updated: 2026-07-31
area: "[[Echo]]"
project: "[[Echo Forge - Trade List Export Contrato Remoto]]"
application: "[[sqx-worker]]"
entities:
  - "[[Symphony]]"
  - "[[ExportTradeListActivity]]"
related:
  - "[[trade-list-exporter-local-path-cross-worker]]"
  - "[[2026-07-26-trade-list-package-complete-and-nonretryable]]"
  - "[[2026-07-31-storage-path-deterministic-by-logical-identity]]"
aliases:
  - contrato remoto entre activities temporal
  - ef-g32-decision
  - no local paths between activities
confidence: verified
source_session: cursor-2026-07-31-trade-list-remote-contract-design
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/application
  - app/sqx-worker
  - area/echo
  - tech/temporal
  - priority/high
---

# Decision: el contrato entre activities Temporal es remoto o no existe

## Contexto

Symphony corre sus activities en una task queue compartida por Zeus, Hera y
Kronos. `trade_list_exporter` devolvía `ndjson_path` (ruta del worker que lo
ejecutó) y el workflow se la pasaba a `act_upsert_trade_list`, que Temporal
podía schedular en otro host. Ver [[trade-list-exporter-local-path-cross-worker]].

## Decisión

**Ninguna activity puede recibir en su input, ni publicar en su output, una ruta
de filesystem.** El contrato solo transporta identificadores alcanzables desde
cualquier worker: claves de scope, keys de object storage, checksums, manifests.
El disco local es detalle de implementación privado de la activity.

Corolario operativo: si dos pasos consecutivos comparten un archivo local, no son
dos activities — son una. Se fusionan, y el borde de la activity se pone donde el
estado ya es remoto.

Aplicación concreta (`EF-G32`): `trade_list_exporter` exporta, sube el paquete a
MinIO y upsertea el manifest en Mongo antes de retornar; `act_upsert_trade_list`
se retira porque su firma tomaba un path local.

## Alternativas descartadas

1. **Sticky worker / session / task queue por host.** Resuelve el síntoma atando
   el pipeline a la topología del cluster y rompiendo el balanceo entre workers.
2. **Export sube a MinIO y una segunda activity solo escribe Mongo.** Cumple el
   invariante, pero agrega un round-trip y más historia de Temporal sin quitar
   ningún riesgo: el upsert Mongo es una llamada de milisegundos que no necesita
   aislamiento propio.
3. **Pasar el contenido del artefacto por el payload de Temporal.** Descartada:
   los NDJSON son de tamaño arbitrario y la historia de un workflow no es un
   bus de datos.

## Consecuencias

- La unidad de retry se vuelve gruesa: un fallo transitorio de Mongo re-ejecuta
  el export (minutos de `sqcli`). Aceptable porque cada borde es idempotente
  (MinIO compara sha256, Mongo hace upsert por clave natural). Si el costo
  molesta, el patrón de escape es un **recibo de publicación** en una key
  determinística que permita saltar la parte caras en el reintento.
- Los errores de contrato deben marcarse con
  `temporal.NewNonRetryableApplicationError`: un wrapper de tipo propio solo
  funciona si la `RetryPolicy` declara su nombre en `NonRetryableErrorTypes`, y
  asumirlo sin declararlo hace que los errores de contrato reintenten días.
- Los skips silenciosos son incompatibles con este contrato: si el scope no se
  puede derivar o el artefacto sale vacío, la activity falla. Devolver "éxito
  sin publicar" convierte un bug en datos falsos.

## Trazabilidad

- Plan de implementación: [[Echo Forge - Trade List Export Contrato Remoto]].
- Gap en el repo: `specs/FEAT-SQX-STRATEGY-EVALUATION/G6_HANDOFF.md` §10.9 (EF-G32)
  y orden de remediación en §10.8.

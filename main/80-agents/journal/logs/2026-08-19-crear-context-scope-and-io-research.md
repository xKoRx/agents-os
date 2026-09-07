---
type: change_log
schema_version: 1
scope: session
created: "2026-08-19"
updated: "2026-08-19"
area: "[[Meli]]"
project: "[[Crear Context]]"
application:
entities:
  - "[[Crear Context]]"
  - "[[rio-playmaker]]"
related:
  - "[[signals-context-flow]]"
  - "[[deploy-component]]"
  - "[[deploy-request-path]]"
  - "[[playmaker-deploy-flow]]"
aliases:
  - Crear Context scope correction
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

# Crear Context — cierre forense de fuente I/O y matriz AS-IS

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** conflict-resolution + forensic-discovery + implementation + updated
- **Archivo(s):**
  - `10-projects/Meli/Crear Context/Crear Context.md`
  - `30-resources/rio-atlas/journeys/deploy-component.md`
  - `30-resources/rio-atlas/journeys/deploy-request-path.md`
  - `30-resources/rio-atlas/architecture/playmaker-deploy-flow.md`
  - `30-resources/rio-atlas/architecture/signals-context-flow.md`

## Motivo

- Cerrar con evidencia de código la fuente distribuida del I/O y la matriz campo-a-campo antes de la SPEC técnica.
- Mantener el alcance create-only: Context efímero, sin persistencia, sin reemplazar `parameters` y sin adopción por CPs.
- Corregir la divergencia del pipeline descubierta al actualizar Playmaker e implementar un contrato v1 ejecutable sin convertirlo en un nuevo wire contract.

## Fuentes usadas

- Instrucción explícita del owner de [[Crear Context]] sobre no persistencia y alcance create-only.
- Conversación del owner con Flor: el CP recibe variables resueltas; el front configura el mapping y Playmaker cruza properties con outputs antes del dispatch.
- Código local de Playmaker, SDK, ambos fronts, Kafka/Flink/ClickHouse/Fury CP, materializer y CPs adicionales descubiertos; branch/HEAD y archivos:línea quedaron registrados en [[signals-context-flow]].
- Graphify se usó para descubrir relaciones/call sites; el source abierto fue la evidencia primaria.
- Pull `--ff-only`: Playmaker pasó de `8887122` a `d1741b8`; `fa73018a` añadió resolución de parameters al pipeline. SDK permaneció en `9d86eb8`.

## Resolución aplicada

- [[signals-context-flow]] quedó como fuente canónica con universo `28/28`, tres paths, inputs y outputs por campo, persistencia, productor→consumidor, front nuevo/legacy, dirección, sensibilidad, aliases, registry y gaps.
- [[Crear Context]] quedó reducido a findings, decisiones de alcance, confirmaciones humanas/runtime y links al Atlas; no duplica la matriz.
- Los journeys corrigieron el diagrama del pipeline nuevo y documentaron el gap `gcp-kafka-topic`/aliases entre routing Playmaker y allowlists CP.
- Se crearon ramas `feature/SIG-573-component-context` en SDK y Playmaker. SDK define el envelope immutable/versionado; Playmaker calcula el objeto desde params crudos + efectivos + relaciones y lo conserva sólo en `DispatchRequest` interno. Los adapters siguen ignorando Context.
- Se realineó el contrato SDK para preservar sin sustitución `configured_value`, valor efectivo consumidor y output runtime productor. `direction`, `value_type`, `sensitivity`, completeness e issue codes son metadata suplementaria, no códigos que reemplacen el dato.
- `ParameterResolutionService` ahora puede devolver `resolvedParameters + resolutionMetadata`; ambos parsers capturan componente/data product/ambiente productor, `outputPath`, objeto crudo de `service.values`, path runtime y fragmento sustituido en la misma pasada que ya resolvía el deploy. La firma pública previa sigue delegando y conserva compatibilidad.
- `ComponentContextBuilder` dejó de fabricar output productor desde el valor consumidor. Cruza raw + effective + metadata, mantiene producer path y consumer path separados, conserva wrappers, marca `resolved=false`/issues cuando falta prueba y filtra campos/tipos por el catálogo demostrado.
- La auditoría final detectó que `DestinationParseServiceImpl` filtra y reindexa `destinations[]`. El resultado interno ahora preserva `configuredPath → consumerPath`; Context expone ambos paths y obtiene el placeholder desde la ubicación cruda correcta sin una segunda resolución.
- Se retiró `gcp-kafka-topic` del catálogo ejecutable de Context: aunque Kafka CP tenga parser, el routing vigente de Playmaker lo manda al catch-all de materializer. La matriz mantiene `14 AUDITADO`, pero la derivación segura queda en 13 tipos; el resto falla cerrada como `UNSUPPORTED`.
- La evidencia visual final del owner confirmó que el front configura las keys consumidoras `chv7_jdbc_url`, `chv7_table_created`, `chv7_crud_user_created` y `chv7_crud_user_password` contra los placeholders `${chv7.jdbc_url}`, `${chv7.table_created}`, `${chv7.crud_user_created}` y `${chv7.crud_user_password}`. Se registró como mapping del front, no como output runtime; el source ClickHouse mantiene el mismatch camelCase/anidado y no demuestra `crud_user_password`.
- La integración crea Context sólo en el pipeline y lo transporta en `DispatchRequest`. `BigQueueDispatchAdapter` mantiene exactamente `request.params()` como payload y `MaterializerRestAdapter` sólo usa IDs. Legacy/componente y materializer directo quedan como gap explícito; no se calcula un objeto para descartarlo.

## Validación

- Inspección source con líneas de ambos paths, routing, parsers/builders y merge hacia ambos `values`; búsqueda de consumidores por keys/placeholders/projections.
- `rio-sdk-events`: `./gradlew test jacocoTestCoverageVerification` exitoso. `rio-playmaker`: `./gradlew --include-build ../rio-sdk-events test jacocoTestCoverageVerification` exitoso; tests focalizados cubren literal, placeholder exacto, alias/reindexación de paths, wrapper `.value`, SQL embebido, output ausente, topología parcial, routing GAP unsupported, campos excluidos, params idénticos y ausencia de Context en el wire.
- El refresh final de `origin/feature/parse-params-pipeline`, `origin/develop` y `origin/master` fue bloqueado por el allowlist de red. La comparación se hizo con las refs locales disponibles; la rama vieja `origin/feature/parse-params` no estaba presente y no se integró ninguna ref.
- Las notas modificadas no producen findings del lint contractual.
- Reindex incremental ejecutado después del delta: `graphify-obsidian update` pasó el gate `ERROR=0 WARN=0`, reutilizó el índice para archivos sin cambios y actualizó las notas modificadas. `explain "signals-context-flow"` y `explain "Crear Context"` resolvieron a sus fuentes canónicas.
- `git diff --check` pasó en ambos repos. La búsqueda source no encontró entity/repository/save/log de `ComponentContext` o `ParameterResolutionResult`; los `toString` del SDK omiten los tres niveles de valores y la identidad productora.
- Los MCP del proceso de release y de security review no estaban disponibles; se usaron los wrappers Gradle de cada repo y una revisión estática local como fallback, sin agregar dependencias.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir los deltas de las notas listadas y registrar una decisión reemplazante; no borrar este log de auditoría.

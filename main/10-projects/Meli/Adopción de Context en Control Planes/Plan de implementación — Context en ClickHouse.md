---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Adopción de Context en Control Planes]]"
  - "[[Crear Context]]"
  - "[[Crear Context - Discovery de Params en CPs]]"
  - "[[rio-controlplane-clickhouse]]"
aliases:
  - Plan Context ClickHouse
  - Context adoption ClickHouse
tags:
  - kind/doc
  - project/context-adoption
  - app/rio-controlplane-clickhouse
created: "2026-09-04"
updated: "2026-09-04"
---

# Plan de implementación — Context en ClickHouse

## Propósito

Definir una migración escalable, explícita y backward-compatible desde `DeploymentTriggerMessage.params` hacia Context en `rio-controlplane-clickhouse`, eliminando el `Map<String,Object>` del dominio de ejecución, preservando la procedencia field-level y dejando el contrato temporal del SDK confinado al adapter de entrada.

Este documento es un plan, no una implementación. La revisión fue read-only sobre `feature/new-component-context @ 7de630c6`, con base `develop @ 75f2ea5e`; no se modificó el repositorio ni se ejecutaron suites que escribieran artefactos de build.

## Contenido

## Veredicto

La implementación actual no debe evolucionar incrementalmente desde el overlay de `DeploymentTriggerMapper`; debe reemplazarse. La decisión central es **no agregar `ComponentContext` al `DeploymentRequestedEvent` ni seguir materializando un `Map<String,Object>` como contrato interno**. El SDK y sus mapas pertenecen al adapter de transporte. El dominio debe recibir una proyección tipada por `component_type × operation`, más un reporte de resolución sin valores.

El contrato v1 tampoco permite retirar `params`: aunque `context.component.lastDeployedVersion.inputs` pueda contener las mismas keys que `params`, pertenece a la última versión desplegada, no a la versión solicitada, y falta en el primer deploy. Para `PROVISION` y `UPDATE`, usarlo como autoridad puede restaurar los valores anteriores durante un cambio. La eliminación total de `params` requiere que Context incorpore los inputs efectivos de la versión solicitada y, para campos derivados de relaciones, bindings inequívocos hacia sources y destinations.

## Diagnóstico del diseño actual

- `DeploymentTriggerMapper` convierte `params` a camelCase y después copia todas las entradas utilizables de `component.lastDeployedVersion.inputs` sobre el mismo mapa. La precedencia es semánticamente incorrecta para create/update porque la fuente es histórica y declarativa, mientras `params` contiene el valor efectivo de la solicitud actual.
- El overlay es genérico: no conoce tipo de componente, operación, campo semántico, requiredness, sensibilidad ni procedencia. Una key nueva del productor entra al dominio sin revisión del consumidor.
- La conversión de `Map<String,String>` vuelve todo string salvo una lista manual de siete campos. Esto degrada números y booleanos, depende de heurísticas JSON y acepta shapes sin un contrato por campo. El blocker principal no depende de que existan placeholders residuales: aun con ambos carriers completamente resueltos, sus versiones pueden ser distintas.
- `sources[]`, `destinations[]` y `outputs` no participan. Materialized View y Kafka connector, que necesitan relaciones, quedan fuera del modelo.
- La procedencia se pierde al escribir sobre `event.data`. Los commands sólo ven un valor final y no pueden distinguir Context válido, Context ausente, Context ambiguo, fallback o default.
- La métrica `rio.controlplanes.deployments.inputs_resolved` cuenta keys presentes, no campos realmente consumidos. No incluye tipo, operación, campo ni motivo de fallback; tampoco registra inputs inválidos sin equivalente en params y no tiene tests de tags.
- El cambio acopla todo el CP a la versión temporal del SDK y fuerza Java 25 porque las clases del jar están compiladas con major version 69. La compatibilidad de `1.5.0` y su target Java deben verificarse, no asumirse.
- El evento `DeploymentRequestedEvent` es un carrier legacy del SDK cuyo `data` está parametrizado como `Map<String,Object>`. Introducir Context allí sólo trasladaría el problema y ampliaría el acoplamiento.
- Hay dos gaps de baseline que deben cerrarse antes del rollout: el command de Materialized View exige además `viewWarehouseName`, `viewSchemaName` y `viewName`, aunque el resumen de contrato sólo enumera source/destination/raw SQL; y `ResourceOwnershipValidator` no soporta `kafka-to-clickhouse`, pese a que `ProcessDeploymentUseCase` lo invoca antes del dispatch para todos los tipos.

## Arquitectura propuesta

### Boundary de transporte

`DeploymentEventController` recibe el wire y llama a `DeploymentTriggerMessageAdapter`. Sólo el paquete `deployment.adapter.in.bigqueue` importa `DeploymentTriggerMessage` y las clases `deployment.context` del SDK.

Clases concretas:

- `DeploymentTriggerMessageAdapter`: extrae metadata autoritativa del envelope, copia defensivamente `params` y delega Context al reader temporal.
- `SdkComponentContextReader`: única clase que conoce `ComponentContext`, `Component`, `LastDeployedVersion` y `RelatedComponent` de `0.0.1-component-version-identity`; al migrar a `1.5.0` cambia esta clase y sus contract tests, no el dominio.
- `IncomingDeployment`: record interno con `DeploymentMetadata`, `ContextSnapshot` opcional y `LegacyEffectiveParams`; no es persistente.
- `DeploymentMetadata`: `deploymentId`, `deploymentGroupId`, `componentId`, `componentName`, `componentType`, `operation`, `dataProductId`, `environmentId`, `publishedAt`. Estos campos salen del trigger, nunca de `params` ni de Context.
- `ContextSnapshot`: modelo interno que conserva por separado la identidad de `own.requestedVersion`, sus `effectiveInputs` cuando el wire futuro los provea, `own.lastDeployedVersion.effectiveInputs`, `own.lastDeployedVersion.runtimeOutputs` y los inputs/outputs de `sources[]` y `destinations[]`. El reader v1 representa la ausencia de requested inputs sin inventarlos desde `lastDeployedVersion`; no aplasta carriers ni expone el tipo del SDK.
- `LegacyEffectiveParams`: wrapper exclusivo del adapter de compatibilidad. Encapsula camel/snake case y la precedencia legacy top-level → `parameters`; ningún command recibe el mapa.

Como el request se procesa async, `IncomingDeployment` debe ser inmutable y hacer copia defensiva profunda de colecciones antes de abandonar el controller. No se comparte estado mutable entre el thread HTTP y el executor.

### Resolución por contrato

`DeploymentRequestResolverRegistry` selecciona un resolver por `ResolutionKey(componentType, operation)`. No hay un overlay común ni reflection.

Resolvers iniciales:

- `MergeTreeDeploymentResolver`
- `MaterializedViewDeploymentResolver`
- `KafkaConnectorDeploymentResolver`

Cada resolver construye uno de los records del sealed hierarchy `ClickHouseDeploymentSpec`: `MergeTreeDesiredState`, `MergeTreeDeprovisionSpec`, `MaterializedViewProvisionSpec`, `KafkaConnectorProvisionSpec` o `KafkaConnectorDeprovisionSpec`. Los commands reciben el tipo exacto; `DeploymentDataExtractor` queda sólo dentro del adapter legacy y desaparece del dominio al terminar la migración.

`FieldResolver` es una utilidad pequeña, no un framework genérico. Recibe un `SemanticField`, una lista ordenada y explícita de candidatos ya tipados, un validator y la política de fallback. Devuelve el valor efectivo y un `FieldResolution` sin guardar valores. Los candidatos posibles son `TRIGGER_METADATA`, `CONTEXT_REQUESTED_INPUT`, `CONTEXT_SELF_OUTPUT`, `CONTEXT_SOURCE_OUTPUT`, `CONTEXT_DESTINATION_OUTPUT`, `PARAMS_EFFECTIVE` y `DEFAULT`.

`ResolutionReport` acompaña la spec y registra por enum allowlisted: campo, fuente seleccionada, outcome y motivo. Los commands no deciden procedencia; sólo ejecutan una spec válida.

`ResolutionMode` se configura por tipo y operación con cuatro estados: `PARAMS_ONLY`, `SHADOW`, `CONTEXT_PREFERRED` y `CONTEXT_REQUIRED`. En `SHADOW` se ejecuta exactamente la spec legacy y se compara con la candidata de Context sin loguear valores. En `CONTEXT_REQUIRED`, un campo requerido inválido o ausente falla antes de ownership/DDL y nunca cae silenciosamente a params.

### Dominio y side effects

`ProcessDeploymentUseCase` debe operar con `ResolvedDeployment<? extends ClickHouseDeploymentSpec>`, no con `DeploymentRequestedEvent`. El registry de handlers usa la clase de spec o `ResolutionKey`, no `Map<String, Command<...>>` con `null` para operaciones no soportadas.

`ResourceOwnershipValidator` recibe un `ResourceOwnershipSpec` tipado. `DeploymentEventPublisher` recibe `DeploymentMetadata`; el adapter BigQueue traduce esa metadata al `DeploymentResultMessage`. Así el SDK sigue presente en adapters de entrada/salida, pero no gobierna commands, ownership ni estado.

El KVS no cambia. Continúa persistiendo únicamente `deploymentId`, `materializationId`, `operationType`, `status`, `errorMessage`, `createdAt` y `updatedAt`; Context, params, specs y reportes de resolución son efímeros.

## Flujo antes y después

```text
Antes
DeploymentTriggerMessage { params, context }
  → camelCase(params)
  → overlay genérico de lastDeployedVersion.inputs
  → DeploymentRequestedEvent.data : Map<String,Object>
  → DeploymentDataExtractor
  → commands
```

```text
Después
DeploymentTriggerMessage { metadata, params, context }
  → DeploymentTriggerMessageAdapter
  → IncomingDeployment { metadata, ContextSnapshot, LegacyEffectiveParams }
  → DeploymentRequestResolverRegistry(componentType, operation)
  → ResolvedDeployment<TypedSpec> + ResolutionReport
  → typed ownership validator
  → typed command
  → DeploymentResultMessage
```

## Matriz de ownership y resolución

| Tipo / operación | Campo semántico | Autoridad durante la transición | Autoridad objetivo | Regla |
|---|---|---|---|---|
| Todos / todas | IDs, tipo, operación, data product, timestamp | Trigger metadata | Trigger metadata | Nunca leer desde params o Context; conflicto de identidad se rechaza. |
| MergeTree / PROVISION, UPDATE | `warehouseName`, `schemaName`, `tableName` | `PARAMS_EFFECTIVE` | inputs tipados de la versión solicitada | `lastDeployedVersion.inputs` no participa; UPDATE conserva spec completa porque el command crea si la tabla no existe. |
| MergeTree / PROVISION, UPDATE | `engineName`, `orderBy`, `primaryKey`, `partitionBy`, `tableFields`, `skipIndexes`, `ttl`, `settings`, `comment`, `script` | `PARAMS_EFFECTIVE` o default explícito | inputs tipados de la versión solicitada | Decoder por campo; sin heurística “empieza con `{` o `[`”. `rawSql` queda deprecated y fuera del contrato deseado. |
| MergeTree / DEPROVISION | warehouse/schema/table de la infraestructura creada | params efectivos en shadow | output propio tipado o `ResourceHandle` del último deploy | Operación destructiva: si Context y params discrepan, fail closed; no elegir por fallback silencioso. `serviceName` queda bridge legacy hasta unificarlo con `warehouseName`. |
| Materialized View / PROVISION | source warehouse/schema/table | params efectivos en shadow | output tipado de la relación source seleccionada por binding | `sources[]` sólo es usable si existe binding inequívoco por id/rol y output schema conocido; nunca buscar por nombre o igualdad de valor. |
| Materialized View / PROVISION | destination warehouse/schema/table | params efectivos en shadow | output tipado de la relación destination seleccionada por binding | Misma regla para `destinations[]`. |
| Materialized View / PROVISION | view warehouse/schema/name y `rawSql` | params efectivos | inputs tipados de la versión solicitada | No se derivan del vecino. Resolver primero el contrato real `view*` versus `mv_*`; el SQL sigue validándose contra los identificadores resueltos. |
| Materialized View / UPDATE, DEPROVISION | — | No soportado | Decisión de producto/command pendiente | Rechazar explícitamente antes del dispatch; no depender de un `Map.get()` que retorna `null`. PROVISION actual es upsert interno. |
| Kafka connector / PROVISION | `sourceTopicName` | params efectivos en shadow | output tipado de source Kafka enlazado por binding | No inferir `brokers/servers`; este command usa broker list de configuración de la app. |
| Kafka connector / PROVISION | `destinationCluster`, `destinationDatabase`, `destinationTable` | params efectivos en shadow | output tipado de destination ClickHouse enlazado por binding | Requiere contrato estable de outputs y cardinalidad/rol explícitos. |
| Kafka connector / PROVISION | `consumerGroup`, `messageFormat`, `transformQuery`, `partitions`, `localCopyTtl` | params efectivos/defaults | inputs tipados de la versión solicitada | Validación de identifiers y SQL se conserva después de resolver. |
| Kafka connector / PROVISION | `serviceName`, `clusterType` | params operacionales | sección operacional tipada del request | No pertenecen a outputs topológicos hasta que el owner defina ese contrato. |
| Kafka connector / UPDATE | params tratados hoy como create | Pendiente | Decisión explícita | No activar Context hasta definir idempotencia y semántica; el código actual no distingue UPDATE de PROVISION. |
| Kafka connector / DEPROVISION | componentId, service/cluster locator | trigger + params efectivos | trigger + `ResourceHandle` propio tipado | Resolver primero el gap de ownership; discrepancias de locator fallan cerrado. |

## Evolución necesaria de Context

El dominio puede tiparse de inmediato sin esperar al SDK. La eliminación total de params, en cambio, necesita un contrato wire posterior a v1 con estos hechos separados:

- `requestedVersion`: versión que se intenta desplegar y sus inputs efectivos después de resolver referencias.
- `lastDeployedVersion`: versión que dejó ejecutándose el último deployment completado, sus inputs efectivos y sus outputs runtime.
- `relations`: identidad y dirección actuales, más un binding estable por component id y semantic role cuando un consumidor necesita elegir una relación concreta.
- `typedData`: payload versionado por `schemaId + schemaVersion`, validado en el productor y deserializado por el CP a records locales. El SDK global no debe incorporar un sealed subtype Java por cada componente del ecosistema; la compilación tipada pertenece al contrato owner del CP y el wire puede transportar un objeto schema-bound sin volver a `Map<String,Object>`.

Mientras ese contrato no exista, el reader v1 puede exponer maps sólo dentro del anti-corruption layer. La proyección de Context a fields usa codecs explícitos por tipo de productor y versión de schema; una key desconocida nunca entra al dominio.

### Semántica de versión solicitada y versión desplegada

No se usa el nombre `currentVersion`: durante el dispatch, “current” puede significar la configuración solicitada o la infraestructura actualmente desplegada. Los nombres contractuales son `requestedVersion` y `lastDeployedVersion`.

Contrato objetivo ilustrativo:

```java
record RequestedVersion(
    long version,
    EffectiveInputs effectiveInputs
) {}

record LastDeployedVersion(
    long version,
    EffectiveInputs effectiveInputs,
    RuntimeOutputs outputs
) {}
```

Ambos records comparten el value object `EffectiveInputs` porque sus valores deben obedecer el mismo schema por tipo de componente y versión de contrato. No son el mismo record: `requestedVersion` todavía no tiene outputs, mientras `lastDeployedVersion` representa un resultado histórico y sí puede tenerlos. Compartir un DTO único con outputs opcionales permitiría estados inválidos y facilitaría que un consumidor volviera a confundir ambas autoridades.

Invariantes del contrato:

- `requestedVersion` debe existir en todo trigger que pretenda operar en `CONTEXT_REQUIRED`; durante compatibilidad, su `version` debe coincidir con `context.component.version`.
- `requestedVersion.effectiveInputs` debe corresponder exactamente a la definición solicitada y al mismo resultado post-resolución que hoy se publica en `params`; no puede construirse desde el último deployment completado.
- `lastDeployedVersion` es nullable en el primer deploy y nunca completa campos ausentes de `requestedVersion` durante `PROVISION` o `UPDATE`.
- Los valores de ambas versiones pueden coincidir en un redeploy, pero la igualdad no es una garantía contractual. En un update o rollback pueden diferir y la precedencia siempre corresponde a `requestedVersion` para desired state.
- Los outputs pertenecen sólo a `lastDeployedVersion` hasta que el deployment solicitado termine; para deprovision deben identificar el recurso realmente creado, idealmente mediante un `ResourceHandle` tipado.
- Si el payload v1 sólo contiene `component.version` y `lastDeployedVersion`, el adapter marca `requestedVersion.effectiveInputs` como ausente y el resolver mantiene fallback field-level a `params`. Nunca copia inputs históricos como sustituto.

Ejemplo de update:

```text
requestedVersion.version = 11
requestedVersion.effectiveInputs.ttl = 30
lastDeployedVersion.version = 10
lastDeployedVersion.effectiveInputs.ttl = 7
```

El valor ejecutable es `30`. Que ambos objetos contengan la key `ttl` no implica que representen el mismo estado.

## Fallback exacto

1. Resolver metadata desde el trigger y validar consistencia de IDs/tipo con Context cuando exista.
2. Buscar el candidato Context permitido por la matriz del campo; `lastDeployedVersion.inputs` nunca es candidato para PROVISION/UPDATE.
3. Validar tipo, shape, cardinalidad, binding y placeholder residual antes de seleccionar el candidato.
4. Si el modo permite fallback, buscar sólo ese campo en `LegacyEffectiveParams`, conservando la precedencia actual top-level → nested `parameters` y aliases documentados.
5. Aplicar default únicamente cuando el command actual ya tiene uno explícito; no crear defaults para campos requeridos.
6. Registrar una resolución por campo. No copiar keys adicionales ni construir un mapa combinado.
7. En operaciones destructivas o ante conflicto de identidad/resource locator, rechazar en vez de elegir una fuente por precedencia.

## Observabilidad segura

Reemplazar la métrica actual por `rio.controlplanes.deployment.input_resolution_total`, emitida exclusivamente desde `ResolutionTelemetry` después de resolver la spec.

Tags allowlisted:

- `controlplane=clickhouse`
- `component_type=clickhouse-mergetree|clickhouse-mat-view|kafka-to-clickhouse`
- `operation=provision|update|deprovision`
- `field=<SemanticField.tagValue()>`
- `source=trigger_metadata|context_requested_input|context_self_output|context_source_output|context_destination_output|params|default|none`
- `outcome=resolved|params_fallback|context_missing|context_invalid|context_unusable|missing_required|shadow_match|shadow_mismatch`

No agregar `reason` libre. Si hace falta granularidad, usar un enum acotado como `context_absent`, `field_absent`, `invalid_type`, `unresolved_placeholder`, `ambiguous_relation`, `binding_missing` o `identity_conflict`. Nunca incluir valores, keys no allowlisted, SQL, component names, IDs, deployment IDs, usernames, passwords ni serialized Context.

Dashboards mínimos: cobertura de Context por tipo/operación/campo, tasa de fallback por motivo, paridad shadow por campo y failures `CONTEXT_REQUIRED`. Los umbrales de promoción deben acordarse con el owner; no se inventa un porcentaje desde este plan.

## Estrategia de tests

- Unitarios del adapter: ausencia de Context, maps vacíos, copia defensiva, compatibilidad de snake/camel/nested params y fixtures JSON del contrato temporal; v1 debe producir requested inputs ausentes y nunca inferirlos desde last-deployed.
- Unitarios de resolvers: un test de ownership y precedencia por cada `SemanticField`; Context ausente, inválido, inutilizable, ambiguo, stale y con placeholder; fallback field-level; default permitido; conflicto fail-closed.
- Unitarios de specs/codecs: structured inputs reales, números, booleanos, listas, TTL, settings, table fields y skip indexes; unknown fields rechazados o ignorados en el adapter, nunca propagados al command.
- Contract tests: golden payload emitido por Playmaker para `0.0.1-component-version-identity` y otro para la versión que introduzca `requestedVersion.effectiveInputs`; verificar primer deploy, update con valores distintos, redeploy, rollback y ausencia backward-compatible. Verificar también target Java del jar antes de cambiar el runtime de la app.
- Integración controller → resolver → command fake: mensaje legacy sin Context produce la misma spec; Context + params equivalentes mantiene comportamiento; `lastDeployedVersion.inputs` stale no pisa params; typed Context sin params funciona cuando el modo sea required; Context parcial cae sólo en el campo permitido.
- Integración por componente: MergeTree PROVISION/UPDATE/DEPROVISION; Materialized View PROVISION y rechazo explícito de UPDATE/DEPROVISION; Kafka PROVISION/DEPROVISION y decisión explícita para UPDATE.
- Regresión de lifecycle: idempotencia, STARTED/COMPLETED/FAILED, publicación de resultados y KVS mínimo permanecen iguales.
- Seguridad: ninguna métrica/log/toString contiene values, raw SQL, nombres, IDs o secretos; los mensajes de validación nombran sólo el campo semántico y un reason enum.
- Coverage: cubrir primero paths críticos y luego alcanzar al menos 95% del código nuevo, conforme a la preferencia global del owner.

## Plan incremental y commits

1. `revert(deployment): remove generic context input overlay` — retirar `mergeContextInputs`, el parser heurístico y la métrica gruesa; conservar el comportamiento legacy desde params y dejar un test explícito de que last-deployed inputs no pisan el valor efectivo.
2. `build(deps): isolate temporary context sdk contract` — encapsular imports del SDK en `SdkComponentContextReader`, documentar el salto a `1.5.0` y restaurar Java 21 si el artefacto definitivo es compatible; si no lo es, separar la migración de runtime como cambio propio.
3. `refactor(deployment): introduce immutable inbound deployment model` — agregar `DeploymentMetadata`, `ContextSnapshot`, `LegacyEffectiveParams` e `IncomingDeployment`, sin cambiar commands.
4. `feat(deployment): add field resolution report and bounded telemetry` — agregar enums, `ResolutionReport`, `ResolutionTelemetry` y tests de tags; comenzar en `PARAMS_ONLY`.
5. `refactor(deployment): type merge-tree requests` — crear specs/resolver MergeTree y adaptar ownership/commands con paridad exacta, todavía desde params.
6. `feat(deployment): shadow merge-tree context resolution` — comparar únicamente campos autorizados; no usar `lastDeployedVersion.inputs` para create/update y no activar deprovision hasta tener `ResourceHandle` confiable.
7. `fix(deployment): align materialized-view wire contract` — cerrar `view*` versus `mv_*`, cardinalidad/binding y operaciones soportadas con fixtures producer-consumer.
8. `refactor(deployment): type materialized-view provisioning` — resolver source/destination por binding y outputs tipados, manteniendo view/raw SQL desde requested inputs o params bridge.
9. `fix(connector): establish supported operations and ownership policy` — resolver el rechazo actual de ownership y definir UPDATE antes de adoptar Context.
10. `refactor(connector): type kafka connector requests` — separar inputs propios, source output, destination output y routing operacional; adaptar create/delete commands.
11. `feat(deployment): enable context-preferred rollout by contract key` — canary por tipo/operación, con rollback a `SHADOW`/`PARAMS_ONLY` sin cambiar payloads.
12. `build(deps): migrate context reader to rio-sdk-events 1.5.0` — cambiar sólo dependency, reader y golden fixtures; ninguna clase de dominio debe importar el SDK.
13. `feat(deployment): require typed context for migrated paths` — activar `CONTEXT_REQUIRED` sólo después de cerrar producer coverage, shadow parity y paths legacy/materializer.
14. `refactor(deployment): remove legacy params bridge` — eliminar cada field de `LegacyEffectiveParams` cuando su matriz esté completa; retirar `params` del wire recién cuando todos los paths del CP estén required.

## Gates de rollout

- Gate 0 — baseline verde y operaciones reales documentadas, incluidos los gaps de MV y Kafka ownership.
- Gate 1 — dominio tipado con paridad params-only y sin cambios de DDL/output/KVS.
- Gate 2 — shadow sin mismatches no explicados y observabilidad segura por field.
- Gate 3 — producer entrega `requestedVersion.effectiveInputs`, demuestra paridad con los `params` efectivos de la misma solicitud y provee bindings tipados para el path candidato.
- Gate 4 — context-preferred canary reversible por tipo/operación.
- Gate 5 — context-required con cobertura de pipeline nuevo y cualquier path legacy/materializer que llegue al CP.
- Gate 6 — retiro field-level de params y, finalmente, del carrier completo.

## Riesgos, supuestos y preguntas abiertas

- Confirmar si `1.5.0` se publicará compatible con Java 21. La branch temporal no justifica por sí sola migrar el runtime productivo a Java 25.
- Confirmar el contrato producer-consumer real de Materialized View: el command exige diez fields, mientras el frontend inspeccionado emite `mv_warehouse_name` y no demuestra `view_schema_name`/`view_name` en el mismo shape.
- Confirmar cardinalidad máxima y roles semánticos de `sources[]`/`destinations[]` para MV y connector. Dirección sola no basta si puede haber más de una relación elegible.
- Acordar y publicar `requestedVersion.effectiveInputs` en Context, manteniendo `lastDeployedVersion` como estado histórico. Sin esa separación no existe fuente Context correcta para el desired state de PROVISION/UPDATE.
- Definir un `ResourceHandle` estable para deprovision. No usar configuración actual para borrar infraestructura histórica.
- Resolver si Kafka connector UPDATE es create idempotente o no soportado y cómo participa en ownership.
- Verificar que todos los paths que llegan al endpoint construyen Context; el pipeline legacy, el safety limit de 200 KiB y cualquier dispatch sin Context impiden activar required globalmente.
- Confirmar outputs tipados por versión de MergeTree/Kafka. No usar `component_type_registry` como autoridad hasta que su publisher y semántica estén demostrados.
- No cambiar persistencia KVS, cifrado de outputs, shapes de completion events ni lifecycle de infraestructura dentro de esta adopción salvo un bug bloqueante con evidencia separada.
- No inventar aliases `view*`, `mv_*`, `brokers/servers`, rutas por component name o mappings por igualdad de strings/valores.

## Propuesta concreta de cambios de código

Archivos a retirar o reducir: `deployment/adapter/rest/DeploymentTriggerMapper.java` deja de fusionar datos; `deployment/application/command/DeploymentDataExtractor.java` se limita al adapter legacy y luego se elimina; `shared/telemetry/Metrics.java` retira `incrementDeploymentInputSource`.

Paquetes nuevos sugeridos:

```text
deployment/adapter/in/bigqueue/
  DeploymentTriggerMessageAdapter.java
  SdkComponentContextReader.java
  LegacyEffectiveParams.java
deployment/domain/
  DeploymentMetadata.java
  IncomingDeployment.java
  ContextSnapshot.java
  ClickHouseDeploymentSpec.java
  MergeTreeDesiredState.java
  MergeTreeDeprovisionSpec.java
  MaterializedViewProvisionSpec.java
  KafkaConnectorProvisionSpec.java
  KafkaConnectorDeprovisionSpec.java
deployment/application/resolution/
  DeploymentRequestResolver.java
  DeploymentRequestResolverRegistry.java
  FieldResolver.java
  ResolutionMode.java
  SemanticField.java
  FieldSource.java
  ResolutionOutcome.java
  ResolutionReport.java
  MergeTreeDeploymentResolver.java
  MaterializedViewDeploymentResolver.java
  KafkaConnectorDeploymentResolver.java
deployment/adapter/telemetry/
  ResolutionTelemetry.java
```

El orden de cambio debe preservar una regla: primero tipar y demostrar paridad desde params, después conectar Context en shadow, y sólo al final cambiar la fuente efectiva. Así el refactor de dominio y la migración de datos no quedan mezclados en el mismo commit ni en el mismo riesgo operativo.

## Fuentes

- `rio-controlplane-clickhouse` — branch `feature/new-component-context @ 7de630c6`, base `develop @ 75f2ea5e`, commits `88742f4d`, `74d0fd4b`, `7de630c6`.
- `rio-controlplane-clickhouse` — `deployment/adapter/rest/DeploymentTriggerMapper.java`, `deployment/application/ProcessDeploymentUseCase.java`, `deployment/application/command/DeploymentDataExtractor.java`, `DeployMaterializedView.java`, `DeployKafkaConnectorDeployment.java`, `connector/model/ConnectorParams.java`, `deployment/ResourceOwnershipValidator.java` y `shared/telemetry/Metrics.java`.
- `rio-sdk-events:0.0.1-component-version-identity` — bytecode local inspeccionado: `DeploymentTriggerMessage`, `DeploymentRequestedEvent` y records de `deployment.context`, compilados con major version 69.
- [[Crear Context]] — semántica vigente de inputs, outputs, última versión desplegada y cobertura del productor.
- [[Crear Context - Discovery de Params en CPs]] y [[Adopción de Context en Control Planes]] — consumo field-level, boundaries, mismatches y rollout.

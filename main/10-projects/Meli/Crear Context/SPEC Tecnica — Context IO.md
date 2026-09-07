---
type: doc
schema_version: 1
status: archived
area: "[[Meli]]"
related:
  - "[[Crear Context]]"
  - "[[rio-playmaker]]"
  - "[[signals-context-flow]]"
aliases:
  - SPEC Tecnica Context IO
  - contrato Context IO
  - SPEC Tecnica Context de componente
tags:
  - kind/doc
  - project/crear-context
created: "2026-08-19"
updated: "2026-08-24"
---

# Spec Técnica: Context de componente

**Estado:** draft · **Fecha:** 2026-08-20 · **Dueño:** rjara (Signals) · **Funcional asociado:** SIG-573 · **Reemplaza:** la versión del 2026-08-19, escrita para el envelope rico que se descartó

---

## Propósito

Fijar cómo se implementa el Context definido en SIG-573: el contrato serializable en [[rio-sdk-events]], la derivación en [[rio-playmaker]], el punto de integración con el despacho y el delta exacto contra las bases limpias de las branches vigentes. El porqué, las historias y los criterios de aceptación viven en el funcional y no se repiten acá.

## Alcance

Playmaker calcula un `ComponentContext` efímero por request de deployment y lo publica como campo opcional de primer nivel del `DeploymentTriggerMessage`. No se persiste, no altera `params`, y ningún control plane necesita cambios para que este spec se cumpla: el contrato del mensaje ignora campos desconocidos, así que un consumidor que no conoce el campo se comporta exactamente como antes.

Esta iteración se implementa desde bases limpias: no reutiliza las branches ni el código de las dos entregas abandonadas. La derivación topológica, el punto de integración, la query batcheada de slots, la regla fail-closed de importados y la redacción de logs siguen siendo decisiones del diseño, pero deben implementarse y probarse nuevamente. El contrato vigente usa objetos para Data Product y componente, agrega `id` en los vecinos e incluye los outputs del propio componente.

> [!warning] Mirror histórico — no implementar desde esta nota
> La fuente de desarrollo vigente es `rio-playmaker` → `.sdd/features/new-component-context/2-technical/spec.md` (SIG-590), que ya define el flag de outputs apagado por defecto, el gate cross-data-product y el plan T-01..T-22. Este archivo queda archivado para conservar trazabilidad y no debe competir como fuente canónica.

**Fuera de alcance:** lo que declara SIG-573, y además —explícito porque la versión anterior de esta spec los especificaba— no hay contratos por tipo de componente ni lista blanca (RF-2), no hay filtrado de outputs por dirección, no hay `completeness` ni códigos de issue, y no se valida nada contra el `output_schema` del registry de tipos.

---

## Contenido

- [[SPEC Tecnica — Context IO#1. Contrato de datos — rio-sdk-events|1. Contrato de datos — rio-sdk-events]] · [[SPEC Tecnica — Context IO#2. Derivación — rio-playmaker|2. Derivación]] · [[SPEC Tecnica — Context IO#3. Punto de integración|3. Punto de integración]] · [[SPEC Tecnica — Context IO#4. Seguridad|4. Seguridad]] · [[SPEC Tecnica — Context IO#5. Delta contra lo implementado|5. Delta contra lo implementado]] · [[SPEC Tecnica — Context IO#6. Decisiones de diseño|6. Decisiones de diseño]] · [[SPEC Tecnica — Context IO#7. Verificación|7. Verificación]]

---

## 1. Contrato de datos — rio-sdk-events

Paquete `com.mercadolibre.rio.sdk.events.deployment.context`. Records inmutables, Jackson con `PropertyNamingStrategies.SnakeCaseStrategy`, `@JsonIgnoreProperties(ignoreUnknown = true)` y `@JsonInclude(NON_NULL)`. El subpaquete pertenece a `deployment` porque el contrato solo existe dentro de `DeploymentTriggerMessage`; un paquete raíz `events.context` comunicaría erróneamente un contexto transversal del SDK.

```
ComponentContext
|- dataProduct     DataProduct           { id, name, teamName, environment }
|- component       Component             { id, name, type, lastDeployedVersion }
|                   \- lastDeployedVersion   LastDeployedVersion { version, outputs }
|- sources         List<RelatedComponent>
\- destinations    List<RelatedComponent>

RelatedComponent   { id, name, type, outputs }
```

`Component` y `RelatedComponent` comparten `id` / `name` / `type`; `DataProduct` comparte `id` / `name` y agrega `teamName` / `environment`. La procedencia la da la estructura, no el nombre del campo. La clase de vecinos se llama `RelatedComponent` porque amarra a la tabla `component_relations`.

| Campo | Tipo Java | Wire | Nulabilidad | Origen |
|---|---|---|---|---|
| `ComponentContext.dataProduct` | `DataProduct` | `data_product` | obligatorio | data product del componente en despliegue |
| `ComponentContext.component` | `Component` | `component` | obligatorio | componente que se despliega |
| `ComponentContext.sources` | `List<RelatedComponent>` | `sources` | obligatorio, puede ir vacío | `component_relations` activas donde el componente es destino |
| `ComponentContext.destinations` | `List<RelatedComponent>` | `destinations` | obligatorio, puede ir vacío | `component_relations` activas donde el componente es origen |
| `DataProduct.id` | `Long` | `id` | obligatorio | `DataProductModel.getId()` |
| `DataProduct.name` | `String` | `name` | obligatorio | `DataProductModel.getName()` |
| `DataProduct.teamName` | `String` | `team_name` | nulable | `DataProductModel.getTeamName()`, columna `team_name` |
| `DataProduct.environment` | `String` | `environment` | obligatorio | `DataProductModel.getEnvironment()`, columna `environment` con default `legacy`. Ver **PT-1** en §9 |
| `Component.id` | `Long` | `id` | obligatorio | `ComponentModel.getId()` |
| `Component.name` | `String` | `name` | obligatorio | `ComponentModel.getName()` |
| `Component.type` | `String` | `type` | nulable | `ComponentModel.getComponentTemplateCode()` |
| `Component.lastDeployedVersion` | `LastDeployedVersion` | `last_deployed_version` | **nulable** | `null` cuando el componente no tiene ningún deploy completado en el ambiente destino |
| `LastDeployedVersion.version` | `String` | `version` | obligatorio dentro del objeto | semver del último deploy completado del slot |
| `LastDeployedVersion.outputs` | `Map<String, String>` | `outputs` | obligatorio, puede ir vacío | `ServiceModel.getValues()` del **propio** componente en el ambiente destino |
| `RelatedComponent.id` | `Long` | `id` | obligatorio | `ComponentModel.getId()` del vecino; en una copia importada, el de **la copia** |
| `RelatedComponent.name` | `String` | `name` | obligatorio | `ComponentModel.getName()` del vecino |
| `RelatedComponent.type` | `String` | `type` | nulable | `ComponentModel.getComponentTemplateCode()` del vecino |
| `RelatedComponent.outputs` | `Map<String, String>` | `outputs` | obligatorio, puede ir vacío | `ServiceModel.getValues()` del vecino en el ambiente destino, o del componente original si es una copia importada autorizada |

### 1.1 Invariantes

- **Inmutabilidad real.** Listas y mapas se copian en el constructor y se exponen como no modificables. Nadie muta un Context después de construido.
- **Extensible en deserialización.** Los campos desconocidos se ignoran, así que agregar un campo al contrato no rompe a un consumidor viejo. Es la propiedad que hace aditivo todo este cambio.
- **`outputs` nunca es `null`.** Un vecino que no publicó nada se informa con mapa vacío, jamás omitido ni nulo (RF-3).
- **`Component.lastDeployedVersion` es nulo o completo.** No existe el objeto con `version` nula: sin deploy completado el campo entero va `null` y no aparece en el JSON.
- **`toString()` redactado.** `ComponentContext`, `Component`, `LastDeployedVersion` y `RelatedComponent` imprimen identidad y conteos, nunca valores de output. `DataProduct` puede imprimirse completo porque no transporta valores.
- **Sin validación de esquema.** El contrato no valida los outputs contra el `output_schema` de ningún tipo: fuera de alcance por el funcional.
- **Sin `schema_version` propio.** El Context viaja dentro del mensaje y hereda el versionado del mensaje.

### 1.2 Versionado del SDK

La base productiva es `rio-sdk-events:1.3.1` y no contiene `ComponentContext`. El cambio es aditivo en el wire y en la API pública: se agrega el contrato nuevo y `DeploymentTriggerMessage` conserva un constructor con la firma anterior además del constructor canónico con `context`. Se publica como `1.4.0` por feature nueva, no por breaking change contra producción.

Mientras el PR no esté mergeado se usa versión de test `0.0.2-component-context` resuelta por `mavenLocal()`. No se reutiliza `0.0.1-component-context`: esa coordenada fue publicada localmente por la branch abandonada y podría resolver un artefacto incompatible sin error evidente.

---

## 2. Derivación — rio-playmaker

`ComponentContextBuilder`, en `com.mercadolibre.rio.playmaker.service`, es el único productor. Expone un solo método público, invocado una vez por componente despachado.

| Elemento | Fuente | Regla |
|---|---|---|
| `ComponentContext.sources` / `ComponentContext.destinations` | `ComponentRelationRepository.findActiveByComponentId` | **Topológica.** Toda relación activa entra, exista o no una referencia del componente a los outputs del vecino. Se deduplica por id de vecino conservando el orden en que aparecen las relaciones. |
| `RelatedComponent.outputs` | `ServiceModel.getValues()` del vecino en el ambiente destino | **Topológica.** Lo que el control plane publicó es evidencia por construcción, no inferencia. Sin slot o sin valores, mapa vacío. |
| `LastDeployedVersion.outputs` | `ServiceModel.getValues()` del **propio** componente en el ambiente destino | Es el slot que el despacho ya tiene cargado: no agrega query. |
| `LastDeployedVersion.version` | `DeploymentRepository.findLastCompletedSemver` sobre el slot propio | La definición del slot es estado deseado y ya apunta a la versión que se está desplegando, así que la versión corriendo sale del historial de deployments. |

Lo que sigue prohibido es deducir una relación o un valor por igualdad de nombre: la derivación lee topología y lee lo que el CP escribió, y nada más.

### 2.1 Resolución de outputs

`service.values` es un JSON plano que cada control plane escribe al terminar un deployment. Un valor puede venir crudo (`"orders"`) o envuelto (`{"value": "orders", "type": "string", "sensitive": false}`). El builder desenvuelve el miembro `value` y lo lleva a `String`, espejando exactamente la regla de retrocompatibilidad del resolver de parámetros: lo que llega al CP dentro de `context` es el mismo valor efectivo que hoy le llega sustituido dentro de `params`.

Un valor que es objeto y **no** tiene miembro `value` —los anidados de ClickHouse tipo `readOnlyCredential.{username, created}`— no es representable en `Map<String, String>` y queda fuera del mapa. En v1 eso se conserva, pero deja de ser silencioso: se loguea a nivel WARN el conteo y las **claves** descartadas. Las claves no son secreto; los valores sí. Aplanarlas es una decisión de contrato pendiente, no un bug de la derivación: ver **PT-2** en §9.

### 2.2 last_deployed_version

Se puebla en dos pasos sobre el mismo slot, el `ServiceModel` del componente en el ambiente destino.

1. `findLastCompletedSemver` devuelve el semver del último deployment **de deploy** terminado en completado. El status se persiste como `<action>_<status>` —`deploy_completed`, `undeploy_completed`—, así que el filtro tiene que ser igualdad contra `deploy_completed` y no un sufijo: `LIKE '%completed'` también matchea `undeploy_completed` y devolvería la versión de un undeploy como si fuera la versión corriendo. El `LIMIT` se aplica en base pasando un `Pageable` de un elemento.
2. `LastDeployedVersion.outputs` sale de `ServiceModel.getValues()` de ese mismo slot, con la resolución de §2.1.

Sin semver completado, `Component.lastDeployedVersion` va `null` completo (CA-8).

### 2.3 Vecinos importados — fail closed

Un vecino con `ComponentModel.getSourceComponentId()` distinto de `null` es una copia importada de otro data product y no tiene outputs propios: viven en el slot del componente **original**. La copia solo existe una vez aprobada la importación, así que el estado de la copia es la señal de autorización.

1. Si `sourceComponentId` es `null`, es un componente propio y sus outputs salen de su propio slot.
2. Si es copia, se exige que `ComponentModel.getStatus()` sea `IMPORTED` **y** que el componente original exista.
3. Con ambas condiciones se leen los outputs del slot del original, en el mismo ambiente.
4. Si falta cualquiera de las dos, `RelatedComponent.outputs` va vacío y se loguea WARN con el id de la copia (RF-4, CA-5).

`RelatedComponent.id` y `RelatedComponent.name` son siempre los de **la copia**, nunca los del original: el control plane configura contra la entidad que existe en su data product. Sin este fail-closed, la derivación topológica leería outputs a través de un límite de data product que nadie concedió.

### 2.4 La derivación nunca rompe un deployment

RF-7 es una garantía de código, no una intención. El método público envuelve **todo** su cuerpo en un `try` y devuelve `null` ante cualquier `RuntimeException`. Eso incluye la validación de argumentos: hoy los `Objects.requireNonNull` de entrada están fuera del `try`, así que un argumento nulo propaga NPE al despacho y rompe un deploy que antes funcionaba. La validación va adentro del `try`, o se reemplaza por retorno temprano de `null`.

El llamador refuerza la garantía: `BatchDispatchServiceImpl` trata el `null` como "publicar sin context", no como error.

---

## 3. Punto de integración

El Context se construye dentro del despacho de cada componente del pipeline, **después** de resolver los parámetros y **antes** de armar el objeto de dispatch. Ese orden es obligatorio: el valor canónico de un campo es el de `params` post-resolución.

```
BatchDispatchServiceImpl.dispatchItem
 |- createDeploymentAttempt
 |- ParameterResolutionService.resolveComponentParameters      (preexistente)
 |- ComponentContextBuilder.build                              (nuevo)
 \- buildDispatchRequest -> DispatchRequest.context
     \- evento AFTER_COMMIT -> BigQueueDispatchAdapter
         \- DeploymentTriggerMessage.context -> topic rio-deployment-trigger
```

`DeploymentTriggerMessage` gana `context` nullable en última posición y **conserva el constructor sin ese campo**, para que los puntos de construcción que no derivan Context compilen y publiquen sin cambios. No se toca `DeploymentOperation.PROVISION` ni la operación que Playmaker declara en el mensaje: es preexistente y ajena al Context.

**Prerequisito de rama:** `rio-playmaker/feature/new-component-context` parte de `develop` @ `0524ce49e`, que debe contener el fix de resolución de parámetros y la garantía de despacho posterior al commit de outputs. Si esa base no contiene ambas propiedades, la branch debe actualizarse antes de implementar la derivación.

### 3.1 Orden y disponibilidad de outputs

Los outputs de un componente existen recién después de que ese componente desplegó y el control plane respondió. El pipeline ya lo garantiza: el batch topológico siguiente se despacha después del commit de la transacción que procesó el resultado del anterior. La derivación se apoya en esa garantía y no la reimplementa. Un upstream sin desplegar no es un error, es un vecino con `outputs` vacío (CA-4, E2E-2).

### 3.2 Performance: costo en queries

Por componente despachado, con el slot propio ya cargado por el despacho:

| Query | Cantidad |
|---|---|
| relaciones activas del componente | 1 |
| resolución del componente original de un importado | 1 por vecino importado |
| slots de vecinos, `findByComponentIdInAndEnvironmentId` | 1 batcheada |
| semver del último deploy completado | 1, con `LIMIT` en base |

Nunca una query por vecino para leer outputs. Los outputs del propio componente no agregan query: reusan el slot que el despacho ya trajo.

### 3.3 Cobertura por request path

| Path | Cubierto | Motivo |
|---|---|---|
| Pipeline nuevo | Sí | Es el único que arma el objeto de dispatch y el único cuyo adapter publica el campo. |
| Legacy / componente | No | Tiene resolver propio y no usa el objeto de dispatch del pipeline. |
| Materializer directo | No | El adapter opera solo con identificadores y no consume params. |

No se calcula un Context para descartarlo en los paths no cubiertos: sin canal de salida no aporta comportamiento ni evidencia.

---

## 4. Seguridad

Los `outputs` son valores publicados por los control planes y pueden contener credenciales: `jdbcUrl`, usuarios, passwords de ClickHouse. Reglas que el código debe cumplir, y que son requisitos del contrato, no recomendaciones.

- **No persistir, no loguear.** El Context es efímero y no tiene tabla. `toString()` de cada record emite identidad y conteos, nunca valores (CWE-532).
- **Excepciones sin documento.** Una `JsonProcessingException` de Jackson arrastra el documento ofensor, que trae los valores: se loguea solo el nombre de la clase de la excepción, nunca el mensaje ni el stack. Mismo criterio para cualquier `RuntimeException` de la derivación (CWE-209).
- **Autorización por límite de data product.** El fail-closed de §2.3 es el control de acceso, no una optimización: sin él la derivación topológica leería outputs de otro data product sin concesión (CWE-862). Es el único punto del builder que cruza ese límite y por eso es la única regla que no puede degradarse a best effort.
- **Riesgo aceptado en la vigencia de la importación.** El registro de autorizaciones tiene expiración y estado revocado, de modo que el status de la copia prueba aprobación histórica y no vigencia al momento del deploy. El funcional cerró que se confía en el estado importado y no se revalida por deploy. Queda anotado como riesgo conocido.
- **Logging del payload completo apagado por default.** El flag `bigqueue.log-deployment-trigger-payload` serializa el mensaje entero —`params` y `context`— a nivel DEBUG. Queda en `false` en `application.yml`, con el comentario que explica por qué, y no se prende en ambientes compartidos. Es diagnóstico opt-in, no observabilidad.
- **Ensanchamiento declarado.** La derivación topológica amplía el conjunto de valores sensibles que viajan: hoy viajan solo los outputs que el frontend referenció con un placeholder; con el Context viajan todos los outputs publicados de todos los vecinos activos. El Context no abre un canal nuevo. La información sensible viaja resuelta y sin cifrado adicional, exactamente como hoy viaja en `params`.
- **Deuda preexistente que este spec no cierra.** Los valores no están garantizados como pre-cifrados vía KMS: el resolver sustituye placeholders por texto plano y el cliente KMS no tiene llamadores demostrados. El Javadoc del SDK no debe afirmar cifrado que el contrato no puede verificar.

---

## 5. Delta contra lo implementado

Branches vigentes: [[rio-sdk-events]] en `feature/new-component-context`, base `master` @ `9d86eb8`; [[rio-playmaker]] en `feature/new-component-context`, base `develop` @ `0524ce49e`. Ambas parten limpias y no reutilizan código de `feature/SIG-573-component-context` ni `feature/component-context`.

### 5.1 rio-sdk-events

| Hoy | Objetivo |
|---|---|
| No existe `ComponentContext` ni el paquete de contexto | Agregar `deployment.context.ComponentContext(DataProduct dataProduct, Component component, List<RelatedComponent> sources, List<RelatedComponent> destinations)` con los records anidados `DataProduct`, `Component`, `LastDeployedVersion` y `RelatedComponent` |
| `DeploymentTriggerMessage` termina en `publishedAt` | Agregar `context` nullable en última posición y conservar el constructor anterior que delega con `null` |
| `version = '1.3.1'` | `0.0.2-component-context` mientras dure el PR, `1.4.0` al mergear |

Cada record anidado nuevo repite `@JsonNaming` y `@JsonIgnoreProperties(ignoreUnknown = true)` —el patrón que ya usa `RelatedComponent`—: la anotación no se hereda del record externo. `LastDeployedVersion.toString()` tiene que estar redactado desde el primer commit: es el primer lugar del contrato por donde viajan outputs del propio componente.

### 5.2 rio-playmaker

| Hoy | Objetivo |
|---|---|
| el builder recibe `lastVersion` como `String` | recibe además el slot propio, para poblar `LastDeployedVersion.outputs` sin query nueva |
| `new ComponentContext(dataProduct.getName(), lastVersion, ...)` | armado de `DataProduct` y `Component` como objetos, con `Component.lastDeployedVersion` anidado |
| `new RelatedComponent(peer.getName(), peer.getComponentTemplateCode(), outputs)` | `new RelatedComponent(peer.getId(), peer.getName(), peer.getComponentTemplateCode(), outputs)` |
| resuelve outputs solo de vecinos | resuelve además los del propio componente, reusando el mismo helper de unwrap |

### 5.3 Bugs a cerrar en la misma pasada

| # | Dónde | Qué pasa | Fix |
|---|---|---|---|
| B-1 | `DeploymentRepository.findLastCompletedSemver` | el `LIKE` por sufijo `completed` matchea también `undeploy_completed`: un undeploy completado se reporta como versión corriendo y, con el contrato nuevo, además define los `outputs` de `last_deployed_version` | igualdad contra `deploy_completed`, compuesto desde `DeploymentAction.DEPLOY` y `DeploymentStatus.COMPLETED` en vez de un sufijo |
| B-2 | `ComponentContextBuilder.build` | los `Objects.requireNonNull` de entrada están fuera del `try`: un argumento nulo propaga NPE al despacho y rompe un deploy, contra RF-7 | validación dentro del `try`, o retorno temprano de `null` |
| B-3 | `ComponentContextBuilder.outputs` | un valor objeto sin miembro `value` se descarta sin dejar rastro | conservar el descarte, pero loguear WARN con conteo y claves descartadas |

---

### 5.4 Archivos afectados

`rio-sdk-events`:

| Archivo | Estado |
|---|---|
| `deployment/context/ComponentContext.java` | **NUEVO** — contrato completo con `DataProduct`, `Component`, `LastDeployedVersion` y `RelatedComponent` anidados |
| `deployment/context/ComponentContextTest.java` | **NUEVO** — cubre serialización, compatibilidad, inmutabilidad, invariantes y redacción |
| `deployment/DeploymentTriggerMessage.java` | **MODIFICADO** — agrega `context` nullable en última posición y conserva el constructor anterior |
| `deployment/DeploymentTriggerMessageTest.java` | **MODIFICADO** — cubre ausencia cuando es nulo y round-trip cuando está presente |
| `CHANGELOG.md` | **MODIFICADO** — la entrada vigente describe el envelope descartado (data product, environment, component y endpoint identities) |
| `build.gradle` | **MODIFICADO** — versión |

`rio-playmaker`:

| Archivo | Estado |
|---|---|
| `service/ComponentContextBuilder.java` | **MODIFICADO** — armado del contrato nuevo, outputs del propio componente, B-2 y B-3 |
| `repository/DeploymentRepository.java` | **MODIFICADO** — B-1 |
| `service/pipeline/impl/BatchDispatchServiceImpl.java` | **MODIFICADO** — pasa el slot propio al builder |
| `service/ComponentContextBuilderTest.java` | **MODIFICADO** — cubre el contrato nuevo y las regresiones de B-1 y B-2 |
| `service/pipeline/DispatchRequest.java` | **SIN CAMBIOS** — ya transporta el `context` |
| `service/pipeline/impl/BigQueueDispatchAdapter.java` | **SIN CAMBIOS** — ya lo pasa al mensaje |
| `build.gradle` | **MODIFICADO** — versión del SDK; el retiro de `mavenLocal()` va al mergear |

---

## 6. Decisiones de diseño

Decisiones técnicas de esta iteración. No repiten las decisiones cerradas del funcional: esas están en SIG-573.

- **DD-1 — Los outputs del propio componente se leen del slot que el despacho ya cargó**, no con una query nueva. Alternativa descartada: incluir el id propio en el batch de vecinos, que agrega una query por despacho para un dato que ya está en memoria.
- **DD-2 — El semver del último deploy se filtra por igualdad contra `deploy_completed`**, no por sufijo. Obliga a componer el valor desde `DeploymentAction` y `DeploymentStatus` en vez de hardcodear el string, y es lo que cierra B-1.
- **DD-3 — El fail-closed de importados es control de acceso, no degradación best effort.** Es la única regla de la derivación que no puede caer al camino de "devolver algo": ante cualquier duda sobre la autorización, `outputs` vacío.
- **DD-4 — Un output objeto sin miembro `value` se descarta, con WARN de conteo y claves.** Alternativa descartada para v1: aplanar con claves punteadas, que mandaría credenciales de escritura a todos los vecinos activos. Ver **PT-2**.
- **DD-5 — El SDK sube a `1.4.0` porque agrega una feature compatible.** `ComponentContext` no existe en `1.3.1` y el constructor anterior de `DeploymentTriggerMessage` se conserva; no se declara breaking change contra producción.
- **DD-6 — La derivación devuelve `null`, nunca un Context parcial.** Sin `completeness` ni issue codes, "parcial" no es representable: el mensaje sale con `context` completo o sin `context`.

---

## 7. Verificación

En el SDK:

- Serialización: `data_product`, `component` y `last_deployed_version` en snake_case; `context` ausente del JSON cuando es nulo; un campo desconocido en el JSON de entrada se ignora al deserializar.
- Inmutabilidad de `sources`, `destinations` y de cada `outputs`.
- `toString()` de `ComponentContext`, `Component`, `LastDeployedVersion` y `RelatedComponent` no contiene ningún valor de output.
- `Component.lastDeployedVersion` nulo serializa sin la clave.

En playmaker:

- Topología: solo entrantes, solo salientes, ambas, ninguna; vecino repetido deduplicado.
- Vecino sin slot y vecino con slot sin valores: presente con `outputs` vacío.
- Importado autorizado: outputs del original, `id` y `name` de la copia. Importado con status distinto: outputs vacíos. Original inexistente: outputs vacíos.
- Unwrap: valor crudo, valor envuelto, y objeto sin miembro `value` descartado y logueado.
- `last_deployed_version`: sin deploy completado va `null`; con un `undeploy_completed` más reciente que el `deploy_completed` gana el deploy, que es la regresión de B-1; outputs del slot propio presentes.
- Argumento nulo al builder: devuelve `null` y no lanza, que es la regresión de B-2.
- Una sola query de slots para N vecinos.

No regresión, criterio duro: `params` byte a byte idéntico antes y después del cambio, y un request sin Context produce un mensaje con el campo ausente.

---

## 8. Rollback y bloqueantes de merge

Rollback es revertir el commit. El Context es efímero, aditivo y todavía no consumido por ningún control plane; el campo del mensaje es nullable, así que revertir el productor deja a los consumidores en su comportamiento previo sin coordinación. No hay estado que revertir ni migración que deshacer.

Bloqueantes de merge:

- SDK publicado en versión productiva `1.4.0` y `mavenLocal()` retirado de `rio-playmaker/build.gradle`.
- El PR del SDK mergeado antes que el de Playmaker.
- `bigqueue.log-deployment-trigger-payload` en `false` en el yml que se mergea.

---

## 9. Preguntas técnicas abiertas

No son acuerdos del equipo: son puntos que la implementación tiene que resolver y que el funcional no fija.

- **PT-1 — `DataProduct.environment` es el atributo del data product, no el ambiente destino del deployment.** SIG-573 declara la fuente como `data_product.environment`, que es una columna de `data_product` con default `legacy`. El ambiente destino sigue viajando en los campos planos del mensaje y no se duplica dentro del Context. Vale confirmarlo con el equipo: si lo que un control plane necesita es el ambiente destino, el campo está mal nombrado para lo que va a leer.
- **PT-2 — Aplanar outputs anidados queda fuera de v1.** `Map<String, String>` no representa `readOnlyCredential.{username, created}`. Aplanar con claves punteadas lo haría representable, pero también mandaría credenciales de escritura a todos los vecinos activos, que es exactamente lo que evitaba el filtrado por dirección del diseño descartado. Se resuelve cuando un control plane concreto lo pida, con la decisión de seguridad tomada aparte.
- **PT-3 — Los mismatches de keys entre lo que un CP publica y lo que otro espera** —Kafka publica `servers` y el contrato de Flink espera `brokers`; ClickHouse publica camelCase y los fronts esperan snake_case— pasan a ser observables porque el Context expone la key real. Este spec no los corrige ni los normaliza: los deja medibles.

---

## 10. Aplicaciones afectadas

| Aplicación | Cambio | Orden |
|---|---|---|
| [[rio-sdk-events]] | contrato del Context: objetos `DataProduct`, `Component` y `LastDeployedVersion`, `id` en `RelatedComponent`, versión nueva | 1 |
| [[rio-playmaker]] | derivación, armado del contrato nuevo, outputs del propio componente, los tres bugs de §5.3 | 2 |
| Control planes (kafka, clickhouse, flink, signals, fury, observability) | ninguno: reciben el campo y lo ignoran | — |
| [[rio-frontend]] y `ads-signals-frontend` | ninguno en esta iteración | — |
| [[rio-materializer]] | ninguno: su adapter no consume el Context | — |

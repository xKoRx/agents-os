---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Crear Context]]"
  - "[[rio-playmaker]]"
  - "[[signals-context-flow]]"
aliases:
  - Guía Component Context
  - guía implementación SIG-573
tags:
  - kind/doc
  - project/crear-context
created: "2026-08-19"
updated: "2026-08-19"
---

# Guía de implementación — Component Context

**Spec:** [SIG-573](https://spellbook.adminml.com/projects/SIG/specs/SIG-573) · **Branches:** `feature/SIG-573-component-context` (rio-sdk-events, base `9d86eb8`) y `feature/component-context` (rio-playmaker, base `dac615f47`) · **Estado:** implementado y verificado, PR bloqueado por versión del SDK

## Propósito

Explicar, cambio por cambio, qué hace la implementación del Component Context, por qué cada pieza está donde está, y cómo los tests aseguran el comportamiento. Es la guía de lectura del diff: sirve para revisar el PR y para retomar el trabajo sin releer el código completo.

## Contenido

Problema y root cause · contrato v1 y las tres decisiones que lo explican · cambios en rio-sdk-events (`ComponentContext`, campo `context` del mensaje, CHANGELOG) · cambios en rio-playmaker (`ComponentContextBuilder`, `findLastCompletedSemver`, `DispatchRequest`, punto de creación, publicación) · cobertura de tests suite por suite y lo que **no** aseguran.

---

## 1. Qué problema resuelve

Un control plane recibe hoy, en el mensaje de deployment, identificadores, tipo de componente, criticidad y `params`: un mapa de variables **ya resueltas** por Playmaker. Recibe `"broker:9092"` sin saber que ese valor salió del vecino Kafka. No sabe qué componentes lo rodean, qué publica cada uno, ni en qué versión quedó su propio último deploy.

El root cause no es que el front arme mal el contrato: es que **el mensaje de deployment transporta valores, no contexto**. La información que los explica ya existe en Playmaker — en las relaciones activas y en los outputs que los propios CP publicaron y Playmaker persistió — pero nunca cruza hacia el CP.

La solución es una entidad `Context`, efímera y calculada por request, que viaja en el mensaje de deployment de cada componente. La v1 transporta topología y outputs de vecinos; el canal queda abierto para otras clases de información sin renegociar el mecanismo.

## 2. El contrato v1

```
Context (por componente)
├─ dataProduct        — nombre del data product dueño
├─ lastVersion        — semver del último deployment completado (nullable)
├─ sources[]          → RelatedComponent
└─ destinations[]     → RelatedComponent

RelatedComponent = name · type · outputs (Map<String,String>, ya resuelto)
```

Tres decisiones que explican la forma:

- **Outputs resueltos, no passthrough.** El valor persistido en `service.values` puede venir envuelto como `{type, value, sensitive}`. El builder desenvuelve a `.value`, igual que hace el resolver de parámetros, para que al CP le llegue el valor efectivo y no el sobre de almacenamiento.
- **Derivación topológica, no referencial.** Toda relación activa entra al Context, exista o no un placeholder `${...}` que la referencie. Un vecino que todavía no desplegó se reporta con `outputs` vacío, no se descarta. Antes se filtraba por referencia, y eso hacía que el Context saliera vacío si el front dejaba de escribir placeholders.
- **`sources`/`destinations`, no `input`/`output`.** Se evaluó renombrar y se mantuvo el naming que ya existe en base de datos y en el contrato del SDK.

## 3. Cambios en rio-sdk-events

Branch `feature/SIG-573-component-context`, 4 commits sobre `9d86eb8`. Diff: 5 archivos, +280/-4.

### 3.1 `ComponentContext` (nuevo, 105 líneas)

`src/main/java/com/mercadolibre/rio/sdk/events/context/ComponentContext.java`

Un `record` inmutable con el record anidado `RelatedComponent`. Serialización `snake_case` vía `@JsonNaming`, `@JsonIgnoreProperties(ignoreUnknown = true)` para que el contrato pueda crecer sin romper consumidores, y `@JsonInclude(NON_NULL)`.

Cuatro propiedades que el diseño defiende activamente:

1. **Inmutabilidad real.** El constructor compacto hace `List.copyOf` de las listas y `Collections.unmodifiableMap(new LinkedHashMap<>(outputs))` de los outputs. Mutar la colección del caller después de construir no se filtra hacia adentro, y el `LinkedHashMap` preserva el orden de publicación.
2. **Validación en construcción.** `dataProduct` en blanco y `RelatedComponent.name` en blanco lanzan `IllegalArgumentException`; `outputs` con claves o valores nulos también. Un Context mal formado no existe.
3. **`toString()` redactado.** Ambos records sobreescriben `toString()` para emitir identidad y **conteos**, nunca valores. `RelatedComponent.toString()` además omite las claves. Es la defensa contra el logging accidental de credenciales: los outputs de un vecino pueden incluir un password.
4. **`lastVersion` nullable.** Un componente que nunca completó un deploy no tiene versión, y eso es un estado ordinario, no un error.

### 3.2 `DeploymentTriggerMessage` — campo `context`

Se agrega `ComponentContext context` como último componente del record, **nullable**, y se conserva un constructor de compatibilidad de 14 argumentos que delega con `context = null`.

Ese constructor no es decoración: es lo que mantiene el cambio aditivo. Agregar un componente al record canónico rompería la compilación de todos los call sites existentes. Con él, los seis productores preexistentes de Playmaker (undeploy ×3, inactivación de componente, `DeploymentServiceImpl`, `DeploymentTimeoutJob`) y sus tests siguen compilando y publicando exactamente el mismo mensaje que antes. Del lado consumidor, `@JsonIgnoreProperties(ignoreUnknown = true)` garantiza que un CP que ignora el campo se comporta igual que siempre.

Esto resuelve la aparente contradicción con el ADR: el ADR posterga **cambios en los CP y su adopción**, no el envío. Enviar un campo nullable que nadie está obligado a leer no requiere tocar ningún CP.

### 3.3 `CHANGELOG.md` y `build.gradle`

Entrada nueva en el CHANGELOG y versión bajada a `0.0.1-component-context` para pruebas. **Ambos están desalineados con el código entregado** — ver el reporte de review; la entrada describe el envelope rico que se descartó y declara una versión que el build no usa.

## 4. Cambios en rio-playmaker

Branch `feature/component-context`, 1 commit sobre `dac615f47`. Diff: 12 archivos, +683/-14.

### 4.1 `ComponentContextBuilder` (nuevo, 264 líneas)

`src/main/java/com/mercadolibre/rio/playmaker/service/ComponentContextBuilder.java`

El corazón del cambio. Un `@Service` con cuatro dependencias — `ObjectMapper`, `ComponentRelationRepository`, `ServiceRepository`, `ComponentRepository` — y un único método público `build(component, dataProduct, environment, lastVersion)`.

El flujo interno, en orden:

1. **Clasificar la topología.** Una sola query, `relationRepository.findActiveByComponentId`, trae todas las relaciones activas donde el componente participa en cualquiera de los dos lados. El bucle las reparte: si el componente es el `destination`, el otro extremo es un `source`; si es el `source`, el otro es un `destination`. Los `LinkedHashMap` por id deduplican relaciones repetidas preservando el orden. Una auto-relación aparece legítimamente en los dos lados.
2. **Resolver el origen de las copias importadas.** Una copia importada no publica nada propio; publica el componente original. Para cada vecino con `sourceComponentId != null`, `origin()` valida que el estado sea `Imported` y que el original exista, y devuelve el id del original. Cualquier otro estado devuelve vacío y el caller **retiene los outputs**: falla cerrado, para no leer al otro lado de un límite de data product sin autorización.
3. **Leer los outputs en batch.** `services()` arma el conjunto de ids a buscar — el original cuando hay import autorizado, el propio vecino en el resto — y hace **una** query `findByComponentIdInAndEnvironmentId`. Es explícitamente un batch para no caer en una query por vecino.
4. **Resolver valores.** `outputs()` parsea el JSON de `service.values`; `resolve()` desenvuelve `{...,"value":X,...}` a `X` y deja el resto tal cual, con `toString()`. Un JSON ilegible degrada a mapa vacío sin tumbar el Context.
5. **Ensamblar.** `related()` construye un `RelatedComponent` por vecino, con outputs vacíos cuando corresponde retenerlos.

Dos invariantes explícitas en el diseño:

- **Nunca romper un deploy que antes funcionaba.** El `try/catch (RuntimeException)` de `build()` convierte cualquier fallo interno en `null`, y el trigger se publica sin context. (Con una salvedad: las tres validaciones `Objects.requireNonNull` quedaron **fuera** del `try`, así que la garantía no cubre argumentos nulos — es uno de los findings del review.)
- **Nunca loguear un valor.** Los dos `catch` loguean el **tipo** de la excepción, nunca su mensaje, porque un fallo de parseo sobre `service.values` arrastra el documento ofensor y ese documento contiene credenciales. El comentario en el código lo dice, y es exactamente el tipo de comentario que se gana el lugar.

### 4.2 `DeploymentRepository.findLastCompletedSemver` (nuevo)

Query JPQL que devuelve el semver del deployment completado más reciente para un slot de servicio, ordenado por `id DESC`, con `Pageable` para aplicar el `LIMIT` en base de datos.

Existe porque `service.componentDefinition` es **estado deseado**: en el momento del dispatch ya apunta a la versión que se está desplegando, así que no puede responder "en qué versión quedó el deploy anterior". La respuesta sale del historial. El `LIKE CONCAT('%', :statusSuffix)` es consecuencia de que el status se persiste como `<action>_<status>` — y es también el origen de un bug de corrección que el review detalla.

### 4.3 `DispatchRequest` — campo `context`

Se agrega `ComponentContext context` al record del carrier interno del pipeline, documentado como nullable cuando la derivación se salta o falla. Es el vehículo desde el punto de creación hasta el adapter.

### 4.4 `BatchDispatchServiceImpl` — punto de creación

Se inyecta el builder y se agregan dos métodos privados:

- `lastCompletedSemver(service)` — corta temprano si no hay servicio o id, y consulta la query nueva.
- `context(item, group, lastVersion)` — corta temprano si el `ComponentDefinition` no tiene componente, y delega al builder con el componente, su data product y el environment del grupo.

El punto de creación es deliberado: se ejecuta **después** de la resolución de parámetros y dentro del despacho por item, que a su vez corre después del commit del batch topológico anterior. Ese orden es lo que garantiza que los outputs de los upstream ya estén persistidos y sean legibles. Si un upstream no desplegó, el vecino sale con outputs vacíos en lugar de fallar.

### 4.5 `BigQueueDispatchAdapter` — publicación

Un solo argumento nuevo: `request.context()` pasa al constructor de 15 argumentos de `DeploymentTriggerMessage`. Es el punto donde el Context cruza al wire. Los adapters del materializer y el path legacy no cambian, y por lo tanto siguen publicando sin context.

## 5. Cómo los tests aseguran el comportamiento

Verificación corrida en esta sesión, no heredada:

| Repo | Comando | Resultado |
|---|---|---|
| rio-sdk-events | `./gradlew test jacocoTestCoverageVerification` | **696 tests PASSED, 0 failed**, gate de cobertura 88.8% superado |
| rio-playmaker | `./gradlew test` | **3141 tests PASSED, 0 failed** |

### 5.1 `ComponentContextTest` — 7 tests sobre el contrato del SDK

Cubren el contrato serializable, no la lógica: `snake_case` con los cuatro campos, round-trip que conserva los outputs resueltos, tolerancia a campos desconocidos, `lastVersion` ausente, rechazo de identidad en blanco, inmutabilidad frente a la mutación de la colección del caller, y — el más importante — que `toString()` no filtra ni el valor `sup3rs3cret` ni la clave `password`. Ese último test es lo que convierte la redacción en una garantía verificada y no en una intención.

### 5.2 `ComponentContextBuilderTest` — 12 tests sobre la derivación

Con mocks de los tres repositorios, cada test aísla una regla del contrato y varios están anclados al criterio de aceptación de la spec:

| Test | Qué asegura |
|---|---|
| `carriesIdentity`, `allowsNullLastVersion` | identidad y versión se transportan tal cual llegan |
| `reportsBothDirections` (CA-3) | dos entradas y una salida se clasifican en el lado correcto |
| `resolvesWrappedOutputs` (RF-2/CA-6) | el wrapper `{type,value,sensitive}` se desenvuelve; los escalares y números pasan como string |
| `keepsUndeployedPeer` (RF-3/CA-4) | un vecino sin deploy conserva su slot con outputs vacíos — la regla central del cambio a derivación topológica |
| `resolvesAuthorizedImportAgainstOriginal` (RF-4) | un import autorizado resuelve contra el componente original, conservando el nombre de la copia |
| `withholdsUnauthorizedImportOutputs` (RF-4) | estado distinto de `Imported` ⇒ outputs vacíos, y el test **planta un valor `leaked:9092`** en el servicio de la copia para probar que no se filtra |
| `withholdsOutputsWhenOriginalMissing` | original irresoluble ⇒ mismo fallo cerrado, con el mismo valor trampa |
| `degradesToNullOnFailure` (CA-7) | una excepción del repositorio produce `null`, no una excepción propagada |
| `degradesUnreadableOutputs` | JSON corrupto ⇒ outputs vacíos y el vecino sigue reportado |
| `deduplicatesPeers` | relación repetida ⇒ un solo `RelatedComponent` |
| `handlesSelfRelation` | auto-relación aparece en los dos lados, como la topología la declara |

Los dos tests con valor trampa (`leaked:9092`) son la parte más valiosa de la suite: no verifican que el código "funcione", verifican que **no filtre**. Un test de autorización que solo comprueba `isEmpty()` sin plantar un valor recuperable no prueba nada.

### 5.3 `BigQueueDispatchAdapterTest` — 2 tests sobre el wire

`whenRequestCarriesContext_thenContextTravelsInTheMessage` captura el mensaje publicado y verifica con `assertSame` que el Context viaja, y además que `params` no se alteró. `whenRequestHasNoContext_thenMessageStaysBackwardCompatible` verifica que sin context el mensaje sale con `context == null`. Juntos son la prueba de que el cambio es aditivo en el wire.

### 5.4 Lo que los tests **no** aseguran

Declarado explícitamente, porque un gap silencioso es peor que un gap conocido:

- **El punto de creación en `BatchDispatchServiceImpl` no tiene cobertura.** El builder se inyecta como `mock(ComponentContextBuilder.class)` sin una sola aserción sobre la interacción: nadie verifica que se lo llame, ni con qué componente, data product, environment o `lastVersion`.
- **`findLastCompletedSemver` no tiene ningún test.** La query nueva no se ejecuta en ninguna suite, y con ella el bug de `undeploy_completed` que el review documenta.
- **Outputs anidados sin clave `value`** (un objeto JSON legítimo) no están cubiertos, y el código los descarta en silencio.
- **`outputs` con clave o valor nulo** — la validación existe en el SDK pero ningún test la ejercita (`Map.of()` no admite nulos, hace falta un `LinkedHashMap`).

## 6. Fuentes

- Review completo y findings: reporte de code review de esta sesión.
- Descripción de PR por repo: [[Descripción PR — rio-playmaker]] · [[Descripción PR — rio-sdk-events]]
- Contrato y decisiones: [[Crear Context]] · [[SPEC Funcional — Context IO]] · [[SPEC Tecnica — Context IO]] (esta última **desalineada**: describe el envelope rico ya descartado)
- Provenance del flujo de I/O: [[signals-context-flow]]

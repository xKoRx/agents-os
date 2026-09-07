---
type: resource
schema_version: 1
status: active
area: "[[Meli]]"
sources:
  - "[[rio-playmaker]]"
  - "[[rio-sdk-events]]"
  - "[[rio-controlplane-fury]]"
last_verified: 2026-08-19
confidence: high
aliases:
  - deploy component journey
  - component contract flow
  - flujo del contrato de componente
  - journey deploy component RIO
tags:
  - kind/resource
cssclasses:
  - wide
created: 2026-08-10
updated: 2026-08-19
---

# RIO — Journey: deploy de componente (contrato de I/O, as-is)

> [!info] Vista de journey del [[00-index|RIO Atlas]]
> Cómo el **contrato de inputs/outputs de un componente** cruza el sistema al desplegar: quién lo define, quién lo transforma, cómo viaja y quién lo consume. Estado **as-is** revalidado el 2026-08-19. Producido por [[Onboarding Signals]]. La propuesta de cambio vive en el proyecto [[Crear Context]].

## Síntesis vigente

El contrato de facto está distribuido: los CP/materializer definen las keys que consumen y los outputs que producen; el front construye en `ComponentDefinition.parameters` la configuración y el mapping hacia esos outputs; los outputs runtime vuelven a `deployment.values`/`service.values`. Playmaker **persiste `parameters` tal como llega**, pero antes del dispatch ambos paths resuelven placeholders/destinations contra los outputs persistidos. Por eso el CP recibe un mapa efectivo, no referencias pendientes. Ningún borde valida todavía el shape completo contra un contrato vigente por `component_type`.

**Flujo punta a punta:**
1. **Front proyecta/configura el mapping** → `POST/PATCH /data-products/{dp}/components/{c}/definitions` con `ComponentDefinitionRequestDTO.parameters` (Map JSON, `@NotEmpty`). El front arma el JSON: `destinations[]` y placeholders `${dp.component[env].property}`. No es autoridad del valor runtime ni del contrato final que acepta el CP. (`ComponentDefinitionController.java:53,118`)
2. **Playmaker persiste tal cual** → `ComponentDefinitionModel.parameters` (JSON, `JsonType`). “Crudo” describe esta persistencia, no todos los dispatches.
3. **Path legacy/componente: resuelve** → `DeploymentServiceImpl.resolveComponentParameters:957-987`: (a) `DestinationParseServiceImpl` reemplaza referencias dentro de `destinations[]`; (b) `ParameterParseServiceImpl.parse` reemplaza `${...}` leyendo `ServiceModel.values`, donde quedaron outputs de despliegues anteriores (`getPropertyValue:253-288`). Busca el componente por nombre/ambiente y exige un service `running`; no prueba lineage mediante `component_relations` ni que la key pertenezca al output declarado del tipo.
4. **Path pipeline: comparte los parsers, no el método legacy** → `BatchDispatchServiceImpl` llama `ParameterResolutionService.resolveWithMetadata`; éste encadena `DestinationParseService` + `ParametersParseService` una vez y devuelve JSON resuelto + facts del lookup + mappings de path generados por filtrado/reindexación. `parseParams` deserializa sólo ese JSON; el builder recibe raw, mapa efectivo y metadata de la misma pasada. `BigQueueDispatchAdapter.buildTriggerMessage` continúa publicando únicamente `request.params()`.
5. **Arma el trigger** → ambos paths construyen `DeploymentTriggerMessage(... params, DeploymentSchemaVersion.CURRENT ...)`; `params: Map<String,Object>` está marcado *"opaque to the SDK"*.
6. **Publica a BigQueue** → topic `rio-deployment-trigger`.
7. **CP recibe (push)** → deserializa `BigQueueMessage<DeploymentTriggerMessage>` y rutea por `componentType`.
8. **CP interpreta el contrato** → cada handler/parser lee sus keys concretas. El contrato efectivo vive en esos consumidores y sus output builders, no en el tipo genérico `Map`.

**Confirmación del equipo (2026-08-19):** “al control plane le llegan todas las variables resueltas”; Playmaker hace el mapping de properties con outputs. Esto coincide con el código actualizado. La flecha informal `CP outputs → front → Playmaker → CP` debe leerse así: el front permite configurar referencias a outputs; el valor real proviene de `service.values`, Playmaker lo resuelve y el CP consumidor recibe `params` efectivos.

**Validaciones existentes (parciales, no contractuales):** DTO exige mapa no vacío (`@NotEmpty`); `ParametersParseService.validate` comprueba referencias que logra interpretar; `validateCatalogSignalParameters` valida campos/rangos puntuales solo para catalog-signal; los parsers fallan ante componente/property inexistente o service no `running`. **No** hay validación integral del shape de `parameters` contra el tipo de componente: `SchemaValidator.validateParams` existe, pero no tiene call sites productivos en create/update/deploy, y `component_type_registry.input_schema/output_schema` no está conectado a ese borde.

### Traducción precisa del comentario del equipo

> “Lo parsea con los outputs y properties del componente, pero sin saber de dónde salen y sin validaciones.”

- Es correcto **para el path legacy** si “sin saber de dónde salen” significa “sin lineage/contrato tipado”: el placeholder aporta un nombre y una key; Playmaker encuentra el `service.values[key]`, pero no demuestra mediante relación + schema que sea un output válido, su dirección, alias o sensibilidad.
- “Sin validaciones” es una simplificación: hay checks de existencia/estado y reglas específicas; falta la **validación contractual completa por `component_type`**.
- En HEAD actualizado también describe el **path pipeline nuevo**, aunque mediante `ParameterResolutionService` y no mediante `DeploymentServiceImpl.resolveComponentParameters`; siguen siendo call paths separados.

## Dolor (por qué es mal diseño)

- **Contrato distribuido y sin autoridad única** — el front proyecta gran parte de los inputs/referencias; el consumidor y output builder del CP definen lo que realmente se acepta/devuelve.
- **Contrato sin esquema enforced en el borde ("opaco")** — `params` es `Map<String,Object>` "opaque to the SDK". Hay transformación y validaciones parciales, pero no un esquema tipado que cruce a los CP. Los errores de forma/casing recién explotan en el CP — de ahí el `// TEMP DEBUG` que loguea el body crudo (`DeploymentTriggerController.kt:104-128`).
- **Convención implícita y duplicada** — inputs=`${...}`, outputs=`destinations[]`, y un `component_type_registry.input_schema/output_schema` que no se usa aquí → doble fuente sin garantía.
- **Lineage incompleto** — ambos resolvers buscan por nombre y outputs vigentes; la relación estructural y el lookup de values no forman un contrato único ni prueban producer→output.
- **Acoplamiento temporal** — ambos paths exigen dependencias y properties resolubles en `service.values`; la resolución no equivale a validación contractual.
- **Interpretación dispersa en cada CP** — cada handler lee "keys mágicas"; el contrato vive replicado en N control planes.
- **Seguridad** — `params` lleva valores sensibles pre-encriptados (KMS, SIG-72) pero el CP loguea params/body en claro ("TEMP DEBUG", CWE-532 anotado en el propio código).
- **Versionado frágil** — `schemaVersion` global sobre un mapa opaco; guard "descartar si > CURRENT", sin contrato estructural.

## Evidencia y provenance

- Trazado de primera mano en código local; fork legacy/pipeline y persistencia de outputs revalidados el 2026-08-19.
- Archivos clave: `ComponentDefinitionModel.java`, `DeploymentServiceImpl.java:891-987`, `ParameterParseServiceImpl.java:253-319`, `DestinationParseServiceImpl.java:64-215`, `ParameterResolutionService.java:28-40`, `BatchDispatchServiceImpl.java:157-164,378-391`, `BigQueueDispatchAdapter.java:80-96`, `DeploymentResultHandlerImpl.java:375-426`, `SchemaValidator.java:24`, `DeploymentTriggerMessage.java`.
- `last_verified: 2026-08-19` · `confidence: high`; cobertura cerrada `28/28` tipos en [[signals-context-flow]].

## Límites y contradicciones

- **Matriz cerrada:** [[signals-context-flow]] contiene el universo `28/28`, inputs y outputs field-level, materializer/storage, consumidores, aliases, sensibilidad y evaluación del registry. Los tipos sin handler o con evidencia runtime insuficiente quedaron explícitamente como GAP/NO APLICA.
- **Context realineado, cobertura parcial:** el pipeline captura en la misma pasada `configured value → service.values/output path → resolved fragment → effective value`; no fabrica output si falta metadata. Context permanece interno en `DispatchRequest`. Legacy/componente y materializer directo aún no crean el objeto, por lo que no se declara implementación completa.
- **`CLAUDE.md` de playmaker desactualizado:** dice endpoint `/sdk/context`; la ruta real del bootstrap de señales es `/signals/context` (`SignalsController.java:32,57`). Ese endpoint es una vista read-only de señales por app/env, **no** integra relaciones ni resuelve placeholders (`transports=null`, `SignalsServiceImpl.java:119`).
- **Encriptación:** el contrato dice que valores sensibles van pre-encriptados por KMS, pero no se ubicó el punto exacto de cifrado en playmaker.

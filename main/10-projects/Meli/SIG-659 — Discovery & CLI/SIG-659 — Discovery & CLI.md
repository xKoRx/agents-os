---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P1
area: "[[Meli]]"
parent:
sprint:
start: 2026-10-19
due:
progress: 0
repo: https://github.com/melisource/fury_rio-playmaker
jira:
prs:
aliases:
  - SIG-659
  - Discovery & CLI
  - Discovery V2
  - Discovery v2 de RIO
  - proyecto discovery de RIO
  - contratos de componentes CP
tags:
  - kind/project
  - area/meli
created: "2026-10-19"
updated: "2026-10-22"
---

# SIG-659 — Discovery & CLI

%% Naming: SIG-659 — Discovery & CLI es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ SIG-659 — Discovery & CLI
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** —
> _parent / sprint / repo / jira / prs son opcionales._

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> `owner: me` → **proyecto humano**: la iniciativa/esfuerzo que conduces tú.
> `owner: agent` → **proyecto de agente**: un curro delegado, con detalle pesado que escribe y sigue un agente. Casi siempre es subproyecto de uno humano y vive en la subcarpeta `agentes/` de su iniciativa.
> `root: true` solo en **iniciativas raíz** (sin `parent`). Todo subproyecto debe setear `parent`; si no, aparece como huérfano en [[Panel de Proyectos]].
>
> **Tarea puente:** cuando este proyecto es `owner: agent`, en su proyecto **padre** debe existir UNA sola tarea humana que lo representa (arrancar + seguimiento). Así tu cockpit ve una línea por curro delegado, no las tareas internas del agente. Ejemplo, en el padre:
> `- [ ] [[SIG-659 — Discovery & CLI]] arrancar + seguimiento #owner/me #type/supervision #area/meli`

## 🎯 Objetivo

- Llevar a producción la epic [SIG-659](https://spellbook.adminml.com/projects/SIG/specs/SIG-659) (Discovery & CLI): que cada control plane de [[RIO]] declare un **contrato versionado** de sus componentes y lo publique vía [[rio-sdk-events]], para que [[rio-playmaker]] lo valide, lo versione y lo use como fuente de verdad de operaciones, timeouts, grants, validación, importabilidad, relaciones y contexto, en vez de yml o código hardcodeado.
- El formato del contrato está en la SPEC técnica [SIG-635](https://spellbook.adminml.com/projects/SIG/specs/SIG-635) (Discovery v2). La epic SIG-659 organiza su implementación en 10 specs hijas; el deck del kickoff está en [Grid — Discovery & CLI Kickoff](https://grid.adminml.com/d/01M51AD6PAM7119Q6AVW89VMYH/view?slide=1).
- Mi rol: dev senior de la iniciativa. Desarrollo (paquetes 1 y 2: SDK V2 e ingesta en playmaker) y hago el seguimiento del resto de los paquetes y de la migración de los CPs con sus owners.
- Fuera de este proyecto: [SIG-672 MCP for signals](https://spellbook.adminml.com/projects/SIG/specs/SIG-672) (va después de la epic), la migración física de la tabla del registry, el endpoint administrativo de ownership/activación/rollback y la implementación de monitores (specs separadas según SIG-635).

## 📊 Estado actual

- **2026-10-19 — Proyecto creado.** La epic y sus 10 hijas están en `draft`, sin tasks en Spellbook, todas creadas por dmuena. Los paquetes de trabajo no tienen responsables.
- Las specs hijas son **esqueletos**: objetivo, estado actual y dependencias. Ninguna tiene criterios de aceptación ni SPEC técnica. Antes de implementar, el P0 tiene que pasar por refinamiento (fase F0).
- Contrasté lo que la epic dice que "ya existe" contra el código (`origin/develop`). Hay **seis desvíos** que cambian el tamaño y el enfoque del P0; están en [[#🔬 Línea base verificada en código]]. El más importante: **hoy ningún CP publica su capability**, así que el canal V1 no existe en la práctica y U2 + U7 no son una migración sino una primera adopción.
- **2026-10-22 — Specs técnicas de contrato por CP en review.** bkikuta publicó [SIG-695](https://spellbook.adminml.com/projects/SIG/specs/SIG-695) (ClickHouse), [SIG-696](https://spellbook.adminml.com/projects/SIG/specs/SIG-696) (Flink), [SIG-697](https://spellbook.adminml.com/projects/SIG/specs/SIG-697) (Kafka), [SIG-698](https://spellbook.adminml.com/projects/SIG/specs/SIG-698) (Fury) y [SIG-699](https://spellbook.adminml.com/projects/SIG/specs/SIG-699) (envelope genérico de trigger/resultado V2, no el CP de signals). Cubren el **contenido** de los contratos, pero ninguna, ni [SIG-644 SDK V2](https://spellbook.adminml.com/projects/SIG/specs/SIG-644), cubre la publicación CP → playmaker ni el registro en MySQL: ese tramo del P0 no tiene spec. Hallazgos de la revisión en la bitácora.
- **Próximo paso:** cerrar F0. Revisar los desvíos con dmuena, llevar las decisiones al kickoff y escribir la SPEC técnica de [SIG-671](https://spellbook.adminml.com/projects/SIG/specs/SIG-671).

## 🧭 Qué implica el P0

El P0 es el **núcleo**: sin él no hay contrato que leer y el resto de la epic (P1, P2 y el MCP) no tiene de dónde sacar datos. Son tres specs que forman una cadena:

| Spec | Qué es en concreto | Tipo de trabajo | Size epic |
|---|---|---|---|
| [SIG-673 Schema Rules by Component Type](https://spellbook.adminml.com/projects/SIG/specs/SIG-673) | Escribir el contrato V2 (JSON) de cada `component_type` de cada CP: operaciones, `input_schema`/`output_schema` por operación, relaciones con cardinalidad, `importable`, `user_visible`/`available_on_import` por output, `execution_timeout`, `context_requirements`/`context_exports`. | Acuerdo con los owners de los CPs, no código. Su salida son los fixtures válidos que usan todos los demás. | S |
| [SIG-671 Update component type](https://spellbook.adminml.com/projects/SIG/specs/SIG-671) | Construir el canal CP → playmaker: modelo V2 tipado y publicador en el SDK (U1–U3), ingesta V2 en playmaker con validación, ownership y versionado inmutable (U4–U6), adopción en cada CP (U7) y guía + métrica (U8). | Código en `rio-sdk-events`, `rio-playmaker` y cada CP. Es el camino crítico. | M–L |
| [SIG-677 Provide CP Schema Config](https://spellbook.adminml.com/projects/SIG/specs/SIG-677) | Exponer desde playmaker el contrato ACTIVE por operación, para el front, el resto de la epic y el MCP. | Código en `rio-playmaker`. Ya existe `GET /v2/reference/component-types`, pero con el modelo V1 aplanado. | XS–S |

**Por qué hay que refinarlo antes de codear:**

- **El problema real es más grande de lo que dice la spec.** La epic asume que el canal V1 "funciona" y que el SDK sólo evoluciona. En el código, el SDK trae el record `CPCapabilityMessage` como stub (SIG-191) sin publicador, ningún CP lo envía y el registry sólo se llena posteando a mano (`scripts/seed-component-types.sh`). U2 es un publicador nuevo (scheduler + heartbeat + topic) y U7 es la primera integración en cada CP.
- **Esto abre una simplificación.** Si en producción no hay productores V1, la coexistencia V1/V2 de SIG-635 podría reducirse a "lo que ya está en la tabla". Hay que confirmarlo antes de decidirlo (ver P-1 y P-2).
- **El alcance P0 ya está recortado en la spec** (allowlist estática de owners, sólo ACTIVE, sin DEPRECATED/RETIRED). Falta escribirlo como criterios de aceptación verificables.
- **Hay decisiones de formato abiertas que tocan el contrato** (grants por operación, ACTIVE por cloud, monitores). Si el contrato se congela sin cerrarlas, P1 obliga a un bump major.
- **El registry ya permite varias versiones por tipo** (`UNIQUE (component_type, version_major, version_minor, version_patch)`), aunque el código hoy sobrescribe una fila por tipo. Hay que ver qué cambia de verdad la "migración física del registry" que la epic marca como bloqueante de U6.

**Salida de F0:** SPEC técnica de SIG-671 (y de SIG-677) con criterios de aceptación, decisiones cerradas por el equipo, sizes revalidados y owner asignado por paquete.

## 🔬 Línea base verificada en código

Verificado el 2026-10-19 sólo leyendo refs remotas: `rio-playmaker@origin/develop 34efd36ed` · `rio-sdk-events@origin/master 80b1993` · CPs en `origin/develop` (kafka `f4b5701`, clickhouse `332b2b89`, flink `00292044`, fury `c12a2b61`, kms `1168240`, observability `9a9f130`, signals `10a98bc`). Es volátil: revalidar antes de escribir cada SPEC técnica.

### Desvíos respecto de la epic

| # | La epic dice | El código muestra | Impacto |
|---|---|---|---|
| D-1 | "El canal V1 funciona: SDK → BigQueue → `/events/cp-components`" ([SIG-671](https://spellbook.adminml.com/projects/SIG/specs/SIG-671)) | `CPCapabilityMessage` es un stub en `rio-sdk-events` (sin publicador, scheduler ni heartbeat). Ningún CP lo publica. `bigqueue.cp-components-topic` está en el yml de playmaker pero ningún código lo lee. | U2 y U7 son trabajo nuevo, no una evolución. Probablemente subestimados. |
| D-2 | "Los CPs usan `rio-sdk-events` 1.1.1–1.3.1" | kafka, flink, fury y signals usan 1.3.1; clickhouse usa 1.6.1; **kms y observability no dependen del SDK**. El SDK va en 1.7.0 (sin tag de release; último release `1.6.1`). | Cada CP sube varias versiones del SDK de una vez. Hay que decidir si kms y observability publican contrato. |
| D-3 | `PipelineContextResolver` envía el contexto completo ([SIG-676](https://spellbook.adminml.com/projects/SIG/specs/SIG-676)) | `PipelineContextResolver` sólo resuelve DP + pipeline. El contexto que reciben los CPs lo arma `ComponentContextService.build()`, invocado desde `DispatchRequestFactory.buildContext()`; si falla, despacha sin contexto. | SIG-676 apunta a la clase equivocada y dice "en la lib". La proyección es del lado de playmaker; el SDK sólo trae el record `ComponentContext`. |
| D-4 | Timeouts "hardcodeados 300 s / 600 s" ([SIG-679](https://spellbook.adminml.com/projects/SIG/specs/SIG-679)) | Son dos cosas. Deployments: `DeploymentTimeoutConfig` con yml por tipo (flink-sql 1800, kafka-fury-streams 1800, fury-streams-kafka 1800, clickhouse-mergetree 300, collector-signal 180; default 600). Actions: constantes `DEFAULT_ACTION_TIMEOUT_SECONDS = 300` / `MAX = 600` en `ActionServiceImpl`. | SIG-679 tiene que cubrir ambos. `dispatch-grace-seconds` queda fuera del contrato según SIG-635. |
| D-5 | Grants "sin dependencias dentro de la epic" ([SIG-670](https://spellbook.adminml.com/projects/SIG/specs/SIG-670)) | El nivel de acceso tiene que viajar en el contrato (decisión tomada), así que depende de 673 + 671. El deck sí lo marca así. | Inconsistencia entre la spec y el deck; corregir la spec. |
| D-6 | La migración física del registry bloquea U6 | La tabla `component_type_registry` ya tiene unique por `(component_type, major, minor, patch)`. Es el código el que sobrescribe una fila por tipo (`findFirstByComponentTypeOrderByLastSeenAtDesc`), y un comentario anota una migración pendiente a `UNIQUE(component_type)`, que va en sentido contrario a V2. | Hay que confirmar qué spec es y qué pretende antes de darla por bloqueante. |

### Confirmado tal como dice la epic

- **Ingesta:** `CpCapabilityConsumerController` → `ComponentTypeRegistryServiceImpl.upsert()`. Sobrescribe por `component_type`, convierte una versión inválida en `0.0.0`, descarta `supported_actions` y el endpoint es `permitAll`. Tabla `component_type_registry` (SIG-271).
- **Grants:** `ConfiguredActionPermissionProvider` (`app.action-authorization`) resuelve en este orden: action exacta → familia → permiso exacto → `*`. Las `read-actions` sólo exigen Tiger. ACME se aplica vía `ActionAuthorizationService` y, sin configuración, deniega (fail closed). Es lo que construimos en [[SIG-616 — Autorización de operaciones por equipo]].
- **Import:** `ComponentMetadataAllowlist.IMPORTABLE_TYPES` es un `Set.of` fijo con 9 tipos (`aws-msk-topic`, `gcp-kafka-topic`, `stream-signal`, `bigqueue-signal`, `clickhouse-mergetree`, `clickhouse-mat-view`, `clickhouse-ref-view`, `gcs-bucket`, `s3-bucket`). Se usa en `ComponentCatalogController` y `ComponentCatalogServiceImpl`.
- **Validate:** `SchemaValidator.validateParams` no tiene llamadas en producción (sólo tests). Usa networknt `json-schema-validator` 1.5.2 en Draft 7, el mismo dialecto que exige SIG-635.
- **Relations:** `ComponentRelationServiceImpl.create()` y `PipelineRelationsServiceImpl.updateRelations()` no validan qué tipos de componente se pueden conectar.
- **Actions:** flujo separado (`ActionController`, `ActionServiceImpl`, topic `rio-actions-trigger`, KVS de resultados y de lock), detrás del flag `app.actionsFramework.enabled`.
- **PROVISION hardcodeado** en `DeploymentServiceImpl`, `DispatchRequestFactory` y `DeploymentTimeoutJob`.

### Component types por CP (detectados por literales en el código, no por registro)

| CP | Stack | SDK | Component types |
|---|---|---|---|
| [[rio-controlplane-kafka]] | Java | 1.3.1 | `aws-msk-topic`, `gcp-kafka-topic`, `kafka-topic` |
| [[rio-controlplane-clickhouse]] | Java | 1.6.1 | `clickhouse-mergetree`, `clickhouse-mat-view`, `clickhouse-ref-view`, `kafka-to-clickhouse` |
| [[rio-controlplane-flink]] | Java 25 | 1.3.1 | `flink-sql`, `gcp-flink-sql`, `gcp-flink-job`, `aws-flink-job` |
| [[rio-controlplane-fury]] | Kotlin | 1.3.1 | `kafka-fury-streams`, `fury-streams-kafka`, `kafka-fury-bigqueue`, `fury-bigqueue-kafka`, `kafka-fury-kvs`, `kafka-fury-http` |
| [[rio-controlplane-signals]] | Java | 1.3.1 | `catalog-signal` (más `bigqueue-signal` / `stream-signal` según [[RIO]]; confirmar) |
| [[rio-controlplane-kms]] | Java 25 | — | No provee componentes; API de secretos |
| [[rio-controlplane-observability]] | Java | — | No provee componentes; jobs y eventos de DP |

## ❓ Preguntas abiertas

### Pendientes de SIG-635 (kickoff)

- **K-1** ¿La activación automática requiere aprobación para productores nuevos? Recomendación de la spec: sólo al registrar o cambiar ownership.
- **K-2** ¿ACTIVE por `component_type` o por `component_type` + cloud? Recomendación: por `component_type` hasta que exista un caso real.
- **K-3** ¿Cuánto se retienen los contratos DEPRECATED antes de RETIRED? Recomendación: una ventana operativa. No bloquea P0 (P0 sólo usa ACTIVE).
- **K-4** Monitores: ¿metadata u operations `CREATE`/`DELETE_MONITOR`? Recomendación: metadata ahora; ejecución en [SIG-598](https://spellbook.adminml.com/projects/SIG/specs/SIG-598) / [SIG-609](https://spellbook.adminml.com/projects/SIG/specs/SIG-609).

### Nuevas, salidas de la línea base

- **P-1** ¿Qué hay hoy en `component_type_registry` en stg y prod, y quién lo cargó (seed manual)? Query chica y dirigida; la base de testing no sirve como evidencia.
- **P-2** ¿Quién consume `GET /v2/reference/component-types` hoy ([[ads-signals-frontend]], [[rio-frontend]])? Define si SIG-677 evoluciona ese endpoint o crea uno nuevo, y si hace falta mantener V1.
- **P-3** Si ningún CP publica V1, ¿mantenemos la coexistencia V1/V2 de SIG-635 o basta con tratar las filas existentes como legacy?
- **P-4** ¿kms y observability publican contrato, o quedan fuera porque no proveen componentes?
- **P-5** Formato del nivel de acceso dentro de cada operation ([SIG-670](https://spellbook.adminml.com/projects/SIG/specs/SIG-670)). Es una ampliación compatible de SIG-635, pero tiene que estar en el contrato antes de congelar los fixtures.
- **P-6** ¿Cuál es la spec de "migración física del registry", quién la tiene y qué cambia, dado D-6?
- **P-7** Dueño del `component_type` en P0 (U5): ¿dónde vive la allowlist estática (yml de playmaker) y cómo se mapea el principal de BigQueue a `producer.service_name`, si el endpoint hoy es `permitAll`?
- **P-8** ¿El contrato vive en cada CP (JSON generado desde el modelo tipado del SDK) o en un repo central? SIG-635 recomienda generarlo desde el modelo tipado.

### Partes de SIG-635 sin spec asignada

- `user_visible`: ocultar outputs no visibles y cifrarlos en reposo.
- Pinning del contrato por deployment (UPDATE, ACTION y DEPROVISION usan la versión fijada).
- Referencias KMS en el contexto proyectado.

## 🗺️ Plan por fases

```text
F0 Refinamiento P0 ─▶ F1 P0 núcleo ─┬─▶ F2 P1 config → contrato ─┐
  (decisiones, SPEC técnica)         │   (contra fixtures U3)      ├─▶ Cierre epic ─▶ SIG-672 MCP (fuera)
                                     └─▶ F3 P2 comportamiento nuevo┘
```

- **F0 — Refinamiento del P0.** Entender el problema y dejar la SPEC técnica lista. Gate: SPEC técnica de SIG-671 aprobada por el equipo, decisiones K-1, K-2, K-4 y P-1 a P-8 cerradas, sizes revalidados y responsables asignados.
- **F1 — P0 núcleo.** Contratos por CP (SIG-673), canal SDK → playmaker (SIG-671, U1–U8) y exposición (SIG-677). Gate: al menos un CP publica V2 en stg, playmaker lo ingiere, versiona y lo expone por operación, con E2E local reproducible ([[RIO E2E local]]).
- **F2 — P1, configuración a contrato.** Timeout, Grants, Validate e Import (`importable`). Puede arrancar en paralelo con F1 una vez que existan los fixtures (U3). Gate: cada capacidad lee del contrato con fallback a la configuración actual para tipos sin contrato V2.
- **F3 — P2, comportamiento nuevo.** Relations, Context y `available_on_import`. Gate: relaciones y contexto validados contra el contrato en E2E.
- **Cierre.** Los 5 CPs con contrato V2 en producción, yml y `IMPORTABLE_TYPES` retirados, guía para owners publicada y métrica `discovery_contract_ingestion_total` con alerta.

## 🧱 Entrega de desarrollo

%% Esta sección siempre queda disponible. En proyectos que cambian código, configuración ejecutable, schemas o infraestructura, es obligatoria: una fila por repo/branch, con SPEC funcional y técnica enlazadas antes de implementar. En proyectos no técnicos, reemplazar la tabla por `_No aplica — <motivo>._`. %%

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| [`rio-sdk-events`](https://github.com/melisource/fury_rio-sdk-events) | — | `master` | [SIG-671](https://spellbook.adminml.com/projects/SIG/specs/SIG-671) (U1–U3, U8) · [SIG-676](https://spellbook.adminml.com/projects/SIG/specs/SIG-676) | Pendiente (F0) | Sin branch: falta SPEC técnica |
| [`rio-playmaker`](https://github.com/melisource/fury_rio-playmaker) | — | `develop` | [SIG-671](https://spellbook.adminml.com/projects/SIG/specs/SIG-671) (U4–U6) · [SIG-677](https://spellbook.adminml.com/projects/SIG/specs/SIG-677) · [SIG-679](https://spellbook.adminml.com/projects/SIG/specs/SIG-679) · [SIG-670](https://spellbook.adminml.com/projects/SIG/specs/SIG-670) · [SIG-678](https://spellbook.adminml.com/projects/SIG/specs/SIG-678) · [SIG-675](https://spellbook.adminml.com/projects/SIG/specs/SIG-675) · [SIG-674](https://spellbook.adminml.com/projects/SIG/specs/SIG-674) · [SIG-676](https://spellbook.adminml.com/projects/SIG/specs/SIG-676) | Pendiente (F0) | Sin branch: falta SPEC técnica |
| [`rio-controlplane-kafka`](https://github.com/melisource/fury_rio-controlplane-kafka) | — | `develop` | [SIG-673](https://spellbook.adminml.com/projects/SIG/specs/SIG-673) · [SIG-671](https://spellbook.adminml.com/projects/SIG/specs/SIG-671) (U7) | Pendiente | Sin branch: falta contrato acordado |
| [`rio-controlplane-clickhouse`](https://github.com/melisource/fury_rio-controlplane-clickhouse) | — | `develop` | [SIG-673](https://spellbook.adminml.com/projects/SIG/specs/SIG-673) · [SIG-671](https://spellbook.adminml.com/projects/SIG/specs/SIG-671) (U7) | Pendiente | Sin branch: falta contrato acordado |
| [`rio-controlplane-flink`](https://github.com/melisource/fury_rio-controlplane-flink) | — | `develop` | [SIG-673](https://spellbook.adminml.com/projects/SIG/specs/SIG-673) · [SIG-671](https://spellbook.adminml.com/projects/SIG/specs/SIG-671) (U7) | Pendiente | Sin branch: falta contrato acordado |
| [`rio-controlplane-fury`](https://github.com/melisource/fury_rio-controlplane-fury) | — | `develop` | [SIG-673](https://spellbook.adminml.com/projects/SIG/specs/SIG-673) · [SIG-671](https://spellbook.adminml.com/projects/SIG/specs/SIG-671) (U7) | Pendiente | Sin branch: falta contrato acordado |
| [`rio-controlplane-signals`](https://github.com/melisource/fury_rio-controlplane-signals) | — | `develop` | [SIG-673](https://spellbook.adminml.com/projects/SIG/specs/SIG-673) · [SIG-671](https://spellbook.adminml.com/projects/SIG/specs/SIG-671) (U7) | Pendiente | Sin branch: falta contrato acordado |
| [`rio-controlplane-kms`](https://github.com/melisource/fury_rio-controlplane-kms) · [`rio-controlplane-observability`](https://github.com/melisource/fury_rio-controlplane-observability) | — | `develop` | — | — | Por decidir (P-4) |

## 🧩 Subproyectos

```base
filters:
  and:
    - 'type == "project"'
    - 'file.hasLink(this.file)'
views:
  - type: cards
    name: Subproyectos
    order:
      - file.name
      - note.status
      - note.priority
```

## ✅ Tareas

> [!note]+ Ownership y tarea puente
> `#owner/me` = tuya · `#owner/agent` = de un agente · sin owner = clasifícala.
> El board es **adaptativo según `owner` del frontmatter**:
> - **Proyecto humano** (`owner: me`): muestra tus tareas y las **tareas puente** (`#type/supervision`) que representan proyectos de agente. Las tareas de agente **no** aparecen acá; viven en su propio proyecto.
> - **Proyecto de agente** (`owner: agent`): muestra las tareas del agente.

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. Tipos: #type/dev #type/admin #type/research #type/pr-review #type/supervision. Flags: #blocked #waiting #urgent. Ver [[convenciones]]. %%
> %% F0 — Refinamiento del P0 %%
> - [ ] **F0** Leer [SIG-635](https://spellbook.adminml.com/projects/SIG/specs/SIG-635) completa contra la [[#🔬 Línea base verificada en código]] y anotar dudas propias #owner/me #type/research #area/meli
> - [ ] **F0** Revisar con dmuena los desvíos D-1 a D-6 antes del kickoff #owner/me #type/admin #area/meli
> - [ ] **F0** Resolver P-1 y P-2: contenido real de `component_type_registry` en stg/prod y consumidores de `GET /v2/reference/component-types` #owner/me #type/research #area/meli
> - [ ] **F0** Resolver P-6: ubicar la spec de migración física del registry y su owner, y confirmar si de verdad bloquea U6 #owner/me #type/research #area/meli
> - [ ] **F0** Kickoff: cerrar K-1, K-2, K-4 y P-3 a P-8, y registrar cada respuesta en 🧭 Decisiones #owner/me #type/admin #area/meli
> - [ ] **F0** Proponer el formato del nivel de acceso por operation (P-5) como ampliación compatible de SIG-635 #owner/me #type/dev #area/meli
> - [ ] **F0** Revisar con bkikuta [SIG-695](https://spellbook.adminml.com/projects/SIG/specs/SIG-695)–[SIG-699](https://spellbook.adminml.com/projects/SIG/specs/SIG-699): huecos del canal, choques con SIG-644, relaciones asimétricas, `clickhouse-ref-view` y CP de signals #owner/me #type/pr-review #area/meli
> - [ ] **F0** Escribir la SPEC técnica de [SIG-671](https://spellbook.adminml.com/projects/SIG/specs/SIG-671) (U1–U8, alcance P0 con criterios de aceptación) con `signals-tech-spec-authoring` #owner/me #type/dev #area/meli
> - [ ] **F0** Escribir la SPEC técnica de [SIG-677](https://spellbook.adminml.com/projects/SIG/specs/SIG-677) (endpoint por operación, compatibilidad con el endpoint actual) #owner/me #type/dev #area/meli
> - [ ] **F0** Proponer ajuste de sizes con la línea base (U2 y U7 son trabajo nuevo) y actualizar SIG-671, SIG-676 y SIG-670 en Spellbook #owner/me #type/admin #area/meli
> - [ ] **F0** Asignar responsables por paquete de trabajo; tomar los paquetes 1 (SDK V2) y 2 (ingesta V2) #owner/me #type/admin #area/meli
> - [ ] **F0** Pedir specs (o dueño) para las partes de SIG-635 sin spec: `user_visible`, pinning por deployment, referencias KMS #owner/me #type/admin #area/meli
> %% F1 — P0: SIG-673 contratos por CP %%
> - [ ] **F1·673** Agendar el acuerdo de contratos con los owners de los CPs #owner/me #type/admin #area/meli
> - [ ] **F1·673** Contrato V2 de [[rio-controlplane-kafka]]: `aws-msk-topic`, `gcp-kafka-topic`, `kafka-topic` #owner/me #type/dev #area/meli
> - [ ] **F1·673** Contrato V2 de [[rio-controlplane-clickhouse]]: `clickhouse-mergetree`, `clickhouse-mat-view`, `clickhouse-ref-view`, `kafka-to-clickhouse` #owner/me #type/dev #area/meli
> - [ ] **F1·673** Contrato V2 de [[rio-controlplane-flink]]: `flink-sql`, `gcp-flink-sql`, `gcp-flink-job`, `aws-flink-job` #owner/me #type/dev #area/meli
> - [ ] **F1·673** Contrato V2 de [[rio-controlplane-fury]]: los 6 tipos `kafka-fury-*` / `fury-*-kafka` #owner/me #type/dev #area/meli
> - [ ] **F1·673** Contrato V2 de [[rio-controlplane-signals]]: confirmar tipos (`catalog-signal`, `bigqueue-signal`, `stream-signal`) #owner/me #type/dev #area/meli
> - [ ] **F1·673** Revisar que los contratos cumplan el perfil JSON Schema y los límites de SIG-635, y congelarlos como fixtures válidos #owner/me #type/pr-review #area/meli
> %% F1 — P0: SIG-671 canal CP → playmaker %%
> - [ ] **F1·U1** `rio-sdk-events`: modelo V2 tipado (envelope, contract, operations, relations, anotaciones de outputs) + validación local previa a publicar #owner/me #type/dev #area/meli
> - [ ] **F1·U2** `rio-sdk-events`: publicador V2 (un mensaje por `component_type`, heartbeat, topic BigQueue) #owner/me #type/dev #area/meli
> - [ ] **F1·U3** Fixtures JSON compartidos SDK ↔ playmaker, válidos e inválidos #owner/me #type/dev #area/meli
> - [ ] **F1·U4** `rio-playmaker`: ingesta V2 (discriminar por `schema_version`, envelope, perfil JSON Schema, límites, `reason_code` sin payload en logs) #owner/me #type/dev #area/meli
> - [ ] **F1·U5** `rio-playmaker`: dueño del `component_type` con allowlist estática y autenticación del productor #owner/me #type/dev #area/meli
> - [ ] **F1·U6** `rio-playmaker`: hash canónico server-side, versiones inmutables y selección ACTIVE atómica #owner/me #type/dev #area/meli
> - [ ] **F1·U8** Guía para owners de CPs + métrica `discovery_contract_ingestion_total` con alerta #owner/me #type/dev #area/meli
> - [ ] **F1·677** `rio-playmaker`: exponer el contrato ACTIVE por operación ([SIG-677](https://spellbook.adminml.com/projects/SIG/specs/SIG-677)) #owner/me #type/dev #area/meli
> - [ ] **F1·U7** Adopción V2 en [[rio-controlplane-kafka]] (subir SDK desde 1.3.1) #owner/me #type/supervision #area/meli
> - [ ] **F1·U7** Adopción V2 en [[rio-controlplane-clickhouse]] (SDK 1.6.1) #owner/me #type/supervision #area/meli
> - [ ] **F1·U7** Adopción V2 en [[rio-controlplane-flink]] (subir SDK desde 1.3.1) #owner/me #type/supervision #area/meli
> - [ ] **F1·U7** Adopción V2 en [[rio-controlplane-fury]] (Kotlin, subir SDK desde 1.3.1) #owner/me #type/supervision #area/meli
> - [ ] **F1·U7** Adopción V2 en [[rio-controlplane-signals]] (subir SDK desde 1.3.1) #owner/me #type/supervision #area/meli
> - [ ] **F1·gate** E2E: un CP publica V2 en stg/local, playmaker lo ingiere, versiona y expone por operación #owner/me #type/dev #area/meli
> %% F2 — P1: configuración a contrato %%
> - [ ] **F2·679** Timeout por contrato: `DeploymentTimeoutConfig` (yml por tipo) y constantes 300/600 de `ActionServiceImpl` ([SIG-679](https://spellbook.adminml.com/projects/SIG/specs/SIG-679)) #owner/me #type/dev #area/meli
> - [ ] **F2·670** Grants por operation leídos del contrato, con fallback a `ConfiguredActionPermissionProvider` ([SIG-670](https://spellbook.adminml.com/projects/SIG/specs/SIG-670)) #owner/me #type/dev #area/meli
> - [ ] **F2·678** Conectar `SchemaValidator` al `input_schema` de cada operación con errores claros ([SIG-678](https://spellbook.adminml.com/projects/SIG/specs/SIG-678)) #owner/me #type/dev #area/meli
> - [ ] **F2·675** `contract.importable` reemplaza a `IMPORTABLE_TYPES` ([SIG-675](https://spellbook.adminml.com/projects/SIG/specs/SIG-675)) #owner/me #type/dev #area/meli
> %% F3 — P2: comportamiento nuevo %%
> - [ ] **F3·674** Validar relaciones por tipo y cardinalidad según `relations` del contrato ([SIG-674](https://spellbook.adminml.com/projects/SIG/specs/SIG-674)) #owner/me #type/dev #area/meli
> - [ ] **F3·676** Proyectar sólo el contexto declarado (`context_requirements` / `context_exports`) en `ComponentContextService` ([SIG-676](https://spellbook.adminml.com/projects/SIG/specs/SIG-676)) #owner/me #type/dev #area/meli
> - [ ] **F3·675** `available_on_import` por output en imports y contexto importado ([SIG-675](https://spellbook.adminml.com/projects/SIG/specs/SIG-675)) #owner/me #type/dev #area/meli
> %% Cierre %%
> - [ ] **Cierre** Retirar yml de timeouts, permisos por tipo e `IMPORTABLE_TYPES` una vez que todos los CPs tengan V2 ACTIVE en producción #owner/me #type/dev #area/meli
> - [ ] **Cierre** Seguimiento del arranque de [SIG-672 MCP for signals](https://spellbook.adminml.com/projects/SIG/specs/SIG-672) sobre el registry poblado #owner/me #type/supervision #area/meli

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label]of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any)dv.paragraph("_Sin tareas._");}
const owner=((dv.current().owner)==="agent")?"agent":"me";
const all=dv.current().file.tasks.array();
const primary=all.filter(t=>has(t,`owner/${owner}`));
const loose=all.filter(t=>!has(t,"owner/me")&&!has(t,"owner/agent"));
dv.header(3, owner==="agent"?"🤖 Tareas del agente":"🧍 Mis tareas");
board(primary);
if(loose.length){dv.header(3,"🧺 Sin owner (clasificar)");render(loose);}
```

%% Rollup de iniciativa — descomentar solo en proyectos padre para ver las tareas #owner/me (incluye puentes) de todos los subproyectos, agrupadas por nota. Cambiar la ruta por la carpeta de esta iniciativa. Nunca muestra tareas de agente.
```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
const ord={" ":0,"/":1,"r":2,"x":3,"X":3,"-":4};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
const pages=dv.pages('"10-projects/CARPETA-DE-LA-INICIATIVA"');
for(const p of pages.sort(x=>x.file.name)){const t=p.file.tasks.array().filter(x=>has(x,"owner/me")&&x.status!=="x"&&x.status!=="X").sort((a,b)=>(ord[a.status]??9)-(ord[b.status]??9));if(t.length){dv.el('h4',p.file.link);render(t);}}
```
%%

## 📆 Bitácora

%% Log diario para las dailies. Una línea por día con lo avanzado / blockers. %%
- **2026-10-22** — Reparto del P0: Brenda (bkikuta) toma los contratos; Rodrigo toma canal y transporte. Relevado en código (playmaker `origin/develop@ca4fe6be`, SDK `origin/master@b9281493`, kafka `origin/develop@f4b5701e`): el único canal es push HTTP a `POST /events/cp-components` (permitAll, sin identidad de productor); `bigqueue.cp-components-topic` (`controlplanes-components` / `-test`) existe en config pero ningún código lo lee, y topics y consumers se configuran en Fury, no en el repo; el registry `component_type_registry` sólo lo leen el upsert y `GET /v2/reference/component-types` (sidebar del front y CLI vía BFF); `scripts/seed-component-types.sh` está vacío y el seed real es `docs/runbook-seed-component-registry-test.md`; las ramas `discovery-v2-00..05` del SDK no tienen transporte y borran `CPCapabilityMessage`, que playmaker todavía compila. Kafka: tres nombres de tipo (`aws-msk-topic`, `gcp-kafka-topic` y el alias `kafka-topic`), output `servers` (no `brokers`), ACME por el fallback `*` y `peek` como read-action sin ACME, incluido en importados; `gcp-kafka-topic` se enruta a `MATERIALIZER_REST` en playmaker y su peek no funciona en el CP.
- **2026-10-22** — Decisiones del owner: Discovery sin coexistencia V1/V2 (el V1 nunca se publicó), despliegue big bang (al llegar a prod todo component type tiene contrato) y playmaker agnóstico (asume lo que declara el CP, incluido access_level, sin pisos propios). Comentarios publicados en SIG-635, SIG-644, SIG-671, SIG-695, SIG-697 y SIG-698, verificados contra el contenido remoto. En SIG-699 se comentó que el título no corresponde, que falta el contrato del CP de signals (catalog-signal, bigqueue-signal, stream-signal) y que el trigger V2 cambia el protocolo de despliegue vigente, por lo que debería ir en una spec aparte.
- **2026-10-22** — Revisión de SIG-695 a SIG-699 contra SIG-635, SIG-644 y el código. Falta: canal de publicación (cuándo y cómo publica el CP, el pedido desde playmaker), registro en MySQL, autenticación del productor y guardia de versión en CI. Choques con el SDK: `context_exports` no string (Kafka, ClickHouse), `orchestration.role` fuera del enum (ClickHouse) y `access_level` descartado como campo desconocido. Relaciones asimétricas: `clickhouse-mergetree` no acepta como input a `flink-sql` ni a `clickhouse-mat-view`. Faltan contratos de `clickhouse-ref-view` y de `rio-controlplane-signals`.
- **2026-10-19** — Proyecto creado desde la epic SIG-659, la técnica SIG-635, las 10 specs hijas y el deck del kickoff. Línea base verificada en código: seis desvíos (D-1 a D-6); el más relevante es que ningún CP publica capability hoy.

## 🧭 Decisiones

- **Tomadas en la epic:** el nivel de acceso de Grants se declara dentro de cada operation del contrato; los responsables se definen al sumar personas a los paquetes de trabajo.
- **Cerradas en SIG-635:** ver su `decision_ledger` (ACTION como operation nombrada, schemas por operación, JSON como único formato aceptado, lifecycle propiedad de playmaker, identidad del productor desde el transporte autenticado, entre otras).
- **Alcance P0 (deck):** allowlist estática para el dueño del `component_type` y sólo ACTIVE, sin ciclo DEPRECATED/RETIRED.
- _Las decisiones de K-1 a K-4 y de P-1 a P-8 se registran aquí cuando el equipo las cierre._

## 🔗 Docs / Links

- Epic: [SIG-659 Discovery & CLI — contratos de componentes CP](https://spellbook.adminml.com/projects/SIG/specs/SIG-659)
- Contrato técnico: [SIG-635 Discovery v2 — formato de contratos de componentes CP](https://spellbook.adminml.com/projects/SIG/specs/SIG-635)
- Specs hijas: [SIG-673](https://spellbook.adminml.com/projects/SIG/specs/SIG-673) · [SIG-671](https://spellbook.adminml.com/projects/SIG/specs/SIG-671) · [SIG-677](https://spellbook.adminml.com/projects/SIG/specs/SIG-677) · [SIG-679](https://spellbook.adminml.com/projects/SIG/specs/SIG-679) · [SIG-670](https://spellbook.adminml.com/projects/SIG/specs/SIG-670) · [SIG-678](https://spellbook.adminml.com/projects/SIG/specs/SIG-678) · [SIG-675](https://spellbook.adminml.com/projects/SIG/specs/SIG-675) · [SIG-674](https://spellbook.adminml.com/projects/SIG/specs/SIG-674) · [SIG-676](https://spellbook.adminml.com/projects/SIG/specs/SIG-676) · [SIG-672](https://spellbook.adminml.com/projects/SIG/specs/SIG-672)
- SDK V2: [SIG-644 Discovery V2 — Implement contracts on SDK](https://spellbook.adminml.com/projects/SIG/specs/SIG-644) (ramas `feature/discovery-v2-00` a `-05` en `rio-sdk-events`, sin mergear)
- Contratos por CP: [SIG-695 ClickHouse](https://spellbook.adminml.com/projects/SIG/specs/SIG-695) · [SIG-696 Flink](https://spellbook.adminml.com/projects/SIG/specs/SIG-696) · [SIG-697 Kafka](https://spellbook.adminml.com/projects/SIG/specs/SIG-697) · [SIG-698 Fury](https://spellbook.adminml.com/projects/SIG/specs/SIG-698) · [SIG-699 Envelope de trigger/resultado V2](https://spellbook.adminml.com/projects/SIG/specs/SIG-699)
- Antecedente V1: [SIG-191 CP Capability Discovery — Self-registration and Schema Registry](https://spellbook.adminml.com/projects/SIG/specs/SIG-191)
- Specs a coordinar (según SIG-635): [SIG-5 RIO Actions Framework](https://spellbook.adminml.com/projects/SIG/specs/SIG-5) · [SIG-573](https://spellbook.adminml.com/projects/SIG/specs/SIG-573) / [SIG-590](https://spellbook.adminml.com/projects/SIG/specs/SIG-590) (Context de componente) · [SIG-598](https://spellbook.adminml.com/projects/SIG/specs/SIG-598) / [SIG-609](https://spellbook.adminml.com/projects/SIG/specs/SIG-609) (monitores) · [SIG-610](https://spellbook.adminml.com/projects/SIG/specs/SIG-610) (undeploy)
- Deck del kickoff: [Grid — Discovery & CLI Kickoff](https://grid.adminml.com/d/01M51AD6PAM7119Q6AVW89VMYH/view?slide=1)
- Proyectos relacionados: [[Crear Context]] (origen de `ComponentContext`), [[SIG-616 — Autorización de operaciones por equipo]] (grants actuales), [[RIO E2E local]] (ambiente para el gate de F1), [[SIG-610 — Seguimiento de inactivación]]
- Apps: [[rio-playmaker]] · [[rio-sdk-events]] · [[RIO]]

## 💡 Ideas

%% Captura ideas sueltas del proyecto al final. Si maduran, promover a tarea o a nota de idea (70-templates/idea.md). %%

### Backlog de ideas

- 

### Motivos / principios

- 

### Memoria pública / interna

%% Opcional para proyectos de agentes o conocimiento: definir qué memoria gobierna el sistema y cuál gobierna el agente, y por qué existe cada una. %%
- **Memoria pública:** 
- **Memoria interna:** 
- **Motivo:** 

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
start: 2026-08-10
due:
progress: 0
repo: https://github.com/melisource/fury_rio-playmaker
jira:
prs:
aliases:
  - Crear Context
  - Component Context
  - Context de componente
  - Backend-owned Context
  - Context inputs/outputs
tags:
  - kind/project
  - area/meli
  - project/crear-context
created: 2026-08-10
updated: 2026-09-07
cssclasses:
  - wide
---

# Crear Context

> [!info] Estado
> **Las dos copias SDD estaban alineadas con el challenge del 2026-08-25; la iteración 1.5 aún debe reflejarse en ellas.** El funcional remoto es [SIG-573](https://spellbook.adminml.com/projects/SIG/specs/SIG-573) y la técnica [SIG-590](https://spellbook.adminml.com/projects/SIG/specs/SIG-590); su sincronización en Spellbook sigue pendiente. El trabajo vive en `feature/new-component-context` para Playmaker y `feature/component-version-identity` para el SDK.
>
> **Los valores de `outputs` viajan siempre (decisión del owner, 2026-08-25).** El flag `rio.context.outputs.enabled` lo había introducido un agente, no el equipo: se eliminó. Los valores sensibles los cifra el **control plane** antes de persistirlos en `_values`, así que Playmaker sólo reenvía material ya protegido — `ControlPlaneClient.encrypt` es código muerto acá porque el cifrado no es su responsabilidad. Esto **deroga DT-27 y T-18 de SIG-590 y cierra PT-1**, que ya no bloquea ningún paso. No se truncan mapas: desde 2026-09-03 hay un safety limit de 200 KiB sobre el mensaje completo; si lo excede, se omite el Context entero y el deploy continúa.
>
> **Antecedente del contrato (2026-08-25): inputs y outputs separados.** Esa forma quedó publicada en `1.4.0` y fue reemplazada por la iteración 1.5 descrita abajo. `rio-sdk-events:1.5.0` ya está publicado y Playmaker consume esa versión definitiva. La resolución muerta de inputs de relacionados y la selección de ambientes soft-deleted quedaron corregidas.
>
> Cómo se escriben estas specs: [[signals-func-spec-authoring]] y [[signals-tech-spec-authoring]]; la regla que manda sobre las dos es `que-es-una-spec.md`.

> [!info] Iteración 1.5 — contrato SDK alineado (2026-09-04)
> La entrega actual no es la iteración 2. Conserva `Component.version`, no introduce `requested` ni `CurrentVersion`, reemplaza `lastDeployedVersion` por `latestVersion`, y deja `latestVersion` con `inputs + outputs`; cada relacionado expone sus `outputs` directamente. La configuración de la operación actual sigue viajando en `DeploymentTriggerMessage.params`. Se adelantó únicamente la base de escalamiento `ContextValues` sealed con `Inputs` y `Outputs`, manteniendo ambos como objetos JSON planos. El Context aplica ahora a deploy y undeploy; actions es una extensión posible, fuera de este PR.

> [!success] Review Zord del PR #1068 — corrección aplicada (2026-09-05)
> Zord completó 7/7 revisores sobre Playmaker `b1ef46ac3` y produjo 27 observaciones brutas. El finding confirmado de `resolveInputs(slot)` se corrigió en `e56811006`: `RelatedComponent` publica sólo `outputs`, ya no resuelve parámetros que descartaba ni pierde outputs válidos por una referencia interna fallida. Se agregó `rio.playmaker.context.derivation.duration_ms` para medir en Datadog el tiempo síncrono completo antes de decidir si conviene un snapshot/DataLoader transversal. La selección vigente del último ambiente se conserva para data products en migración; el SDK temporal y la doble serialización del mensaje completo permanecen como decisiones explícitas. El body remoto de #1068 fue actualizado al contrato real.

> [!success] Review David del PR #1068 — soft-delete corregido (2026-09-07)
> El comentario era aplicable y se resolvió en el boundary de persistencia: `ComponentContextService` usa `findByDataProductIdInAndDeletedAtIsNull`, por lo que tanto la coincidencia exacta como el fallback normalizado operan sólo sobre ambientes activos. `20f34308c` agrega pruebas para los dos caminos con un ambiente eliminado y otro activo.

> [!abstract] Entrega — branches vigentes (2026-09-07)
> | Repo | Branch | Base | Estado | Descripción de PR |
> |---|---|---|---|---|
> | [[rio-playmaker]] | `feature/new-component-context` @ `bd5536205`, pusheada | `develop` @ `b45eb328e` | [PR #1068](https://github.com/melisource/fury_rio-playmaker/pull/1068) mergeable, 5 checks exitosos, 1 omitido y review requerido; consume `rio-sdk-events:1.5.0` e incluye la corrección de soft-delete | [[Descripción PR — rio-playmaker]] |
> | [[rio-sdk-events]] | release `1.5.0` publicada desde `master` | `master` | Contrato definitivo disponible; Playmaker ya no depende de una versión de prueba | [[Descripción PR — rio-sdk-events]] |
>
> **Baseline validado el 2026-09-07:** sobre `bd5536205`, después de integrar `develop`, la suite completa reportó 3597 tests, 0 fallas, 0 errores y 2 skipped preexistentes; `./gradlew check` también pasó. Se preservaron la precarga batch, el guard de 200 KiB, la derivación best effort, la métrica de duración y las correcciones de review.
>
> **Dependencia cross-repo cerrada:** `rio-sdk-events:1.5.0` está publicado y Playmaker lo consume. Quedan como gates humanos el review/merge de #1068, la validación de preproducción y la sincronización de las SPECs remotas en Spellbook.
>
> **PR remoto verificado:** [#1068](https://github.com/melisource/fury_rio-playmaker/pull/1068) apunta a `bd5536205`, GitHub lo reporta `MERGEABLE` y terminó con 5 checks exitosos, 1 omitido y ninguno pendiente o fallando. `mergeStateStatus: BLOCKED` corresponde al gate de review, no a conflictos. El comentario de David sobre soft-delete quedó corregido; falta publicar la respuesta humana y completar la aprobación.
>
> **Abandonadas:** `feature/component-context` (playmaker) y `feature/SIG-573-component-context` (sdk-events). No se reutiliza código de ninguna de las dos. [[Descripción PR — rio-playmaker (entrega descartada)]], [[Descripción PR — rio-sdk-events (entrega descartada)]] y la [[Guía de implementación — Component Context]] describen esa entrega descartada: quedan como registro histórico, no como guía vigente.

## 📐 Contrato iteración 1.5 (vigente en la branch SDK)

```
ComponentContext
|- username        String
|- dataProduct     DataProduct           { id, name, teamName, environment }
|- component       Component             { id, name, type, version, latestVersion }
|                   \- latestVersion     LatestVersion { version, inputs: Inputs, outputs: Outputs }
|- sources         List<RelatedComponent>
\- destinations    List<RelatedComponent>

RelatedComponent   { id, name, type, outputs: Outputs }

ContextValues (sealed) permits Inputs, Outputs
```

- **Fuera de esta iteración:** no existe `requested` ni `RequestedVersion`; `Component.version` sigue identificando la definition que se despliega.
- **Compatibilidad de valores:** `Inputs` y `Outputs` son tipos Java distintos, pero Jackson los serializa como el mismo objeto plano de claves/valores; no aparece una capa `values` en el wire.
- **Operación actual:** su configuración permanece en `DeploymentTriggerMessage.params`; por eso no existe `CurrentVersion` dentro del Context.
- **Última versión propia:** `latestVersion.inputs` contiene la configuración ingresada por el usuario y `latestVersion.outputs` la información generada por el CP.
- **Relacionados:** exponen `outputs` directamente; no llevan `inputs` ni un wrapper de versión.
- **Alcance de uso:** deploy y undeploy en esta entrega; actions podría reutilizarlo después, pero queda fuera de alcance.
- **Plan de evolución:** iteración 2 = contrato más trabajado y agnóstico; iteración 3 = tipificación de atributos.
- **`RelatedComponent.id` es el de la copia**, nunca el del original, incluso cuando los outputs se leen del original: el CP configura contra la entidad que existe en su data product.
- **Se cayeron del contrato:** `component.properties`, `mappings`, `Reference`, `issues`, `completeness`, `origin`, `schemaVersion`, `operation`, y el filtrado de outputs por dirección. Consecuencia abierta: si una importación no está autorizada, el CP recibe `outputs` vacío sin poder distinguirlo de "el vecino no desplegó".
- **La operación del mensaje NO se toca.** `DeploymentOperation.PROVISION` sigue hardcodeada en el dispatch: es código preexistente, ajeno al Context, y derivar `PROVISION`/`UPDATE` cambiaría lo que reciben los CP. Se intentó y se revirtió.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| [[rio-sdk-events]] | `master` @ `8732ee47e` | `master` @ `9d86eb8` | `rio-playmaker` → `.sdd/features/new-component-context/1-functional/spec.md` (SIG-573) | `rio-playmaker` → `.sdd/features/new-component-context/2-technical/spec.md` (SIG-590) | [PR #43](https://github.com/melisource/fury_rio-sdk-events/pull/43) mergeado; contrato publicado como `1.4.0` desde `master` |
| [[rio-playmaker]] | `feature/new-component-context` @ `658f8f615` | `develop` @ `28b929c9e` | `rio-playmaker` → `.sdd/features/new-component-context/1-functional/spec.md` (SIG-573) | `rio-playmaker` → `.sdd/features/new-component-context/2-technical/spec.md` (SIG-590) | [PR #1068](https://github.com/melisource/fury_rio-playmaker/pull/1068) draft; implementación y diff requieren revisión de alcance. Pendientes: sincronizar SIG-590, separar o justificar ClickHouse/Swagger, ejecutar suite Playmaker y validar preproducción |

> [!note] Autoridad y rollout
> La fuente implementable es la copia SDD de SIG-590 en el repo de Playmaker. No existe flag de outputs ni truncamiento. La enmienda del 2026-08-25 agrega `inputs` al contrato del SDK con rollout compatible y deja su población en Playmaker como T-24. Spellbook live no se modificó en esta sesión; la paridad de publicación sigue pendiente.

## 🔄 Cambio de foco (2026-08-19)

> [!note] Sección histórica
> Describe la decisión de ese día. Lo que sobrevive es la **derivación topológica**; los `issues`, `completeness`/`PARTIAL` y el filtrado de outputs por dirección se cayeron en las pasadas posteriores. El contrato vigente es el de arriba.

La corrección del equipo invalidó la derivación del prototipo, no su envelope. El contrato serializable se conserva; cambia **de dónde sale la evidencia**.

- **Antes (referencial):** un componente relacionado entraba al Context solo si el componente en despliegue referenciaba uno de sus outputs con `${...}`. Los endpoints sin outputs referenciados se filtraban y desaparecían. Consecuencia: si el front deja de escribir placeholders, el Context sale vacío.
- **Ahora (topológico):** toda relación activa entra. Los outputs se leen del resultado del CP persistido en el `service` del par. Un par sin outputs se reporta con issue, no se descarta.
- **Regla de evidencia que se conserva:** los **outputs** pasan a ser topológicos porque leer el `service` de un par no infiere nada — es leer lo que el CP escribió. Los **mappings** siguen siendo referenciales: sigue prohibido deducir un mapping por igualdad de nombre o valor. Esta separación preserva la regla anti-invención del discovery sin bloquear la corrección.
- **Nuevo en alcance:** componentes importados de otro Data Product resuelven sus outputs contra el componente **original** (`component.source_component`), validando estado `Imported`; y los outputs de ClickHouse se filtran por dirección de la relación, que además es control de seguridad.
- **Naming:** se evaluó renombrar a `input`/`output` y se decidió **mantener `sources`/`destinations`**, que ya existe en base de datos y en el contrato del SDK.
- **Se conserva del ADR:** efímero, create-only, sin persistencia, sin **consumo** por los CP, `parameters` intacto.
- **Corrección de foco 2026-08-19 (segunda pasada):** el spec funcional se había encajonado en el I/O. El Problema es que **los CP no tienen información** — el mensaje de deployment transporta valores resueltos y opacos, no contexto. La entidad Context es el **vehículo de información hacia los CP**; el I/O es su primer caso de uso, no la tesis. Alcance v1 = **crear el Context y enviarlo en el mensaje**.
- **Enviar ≠ adoptar (resuelve la aparente contradicción con el ADR):** el ADR posterga *cambios en los CP* y su *adopción*, no el envío. `DeploymentTriggerMessage` ignora campos desconocidos, así que agregar `context` nullable es aditivo y ningún CP requiere cambios. La primera implementación fue más allá del ADR: dejaba el Context fuera del wire y lo afirmaba en un test; corregido.

### Hallazgo que motivó el cambio

El flujo real es `cp (outputs) → front → playmaker (mapeo) → cp (variables resueltas)`. Los outputs los produce el **control plane**: `DeploymentResultHandlerImpl.storeResultOutput()` toma el `output` del CP y lo escribe en `deployment._values` y en `service._values`. Playmaker ya tiene los datos; el front hace un round-trip que no agrega información. Ese es el root cause del spec, más filoso que "el front arma el contrato".

### Dependencia de orden

Los outputs de un componente no existen hasta que ese componente desplegó y el CP respondió. La rama de flor ya lo garantiza: el batch topológico siguiente se despacha recién tras el commit del resultado del anterior. El Context se apoya en esa garantía; si un upstream no desplegó, sale `PARTIAL` en vez de fallar.

## 🎯 Objetivo

Crear un Context efímero por componente, publicarlo como campo opcional de `DeploymentTriggerMessage` sin persistirlo ni alterar `params`, separar la configuración del usuario (`inputs`) de los resultados de provisionamiento (`outputs`) y dejar la adopción por los control planes para iniciativas posteriores.

## 📊 Estado actual

`rio-sdk-events:1.5.0` ya está publicado y Playmaker lo consume en `feature/new-component-context @ bd5536205`. El [PR #1068](https://github.com/melisource/fury_rio-playmaker/pull/1068) está sincronizado con `develop @ b45eb328e`, sin conflictos y mergeable; terminó con 5 checks exitosos, 1 omitido y ninguno pendiente o fallando. La suite completa posterior al merge reportó 3597 tests, 0 fallas, 0 errores y 2 skipped; `./gradlew check` pasó. El gate restante es review humana. Pendientes externos: validación en preproducción y sincronización de SIG-573/SIG-590 en Spellbook.

## Resumen de findings (histórico)

> [!warning] No usar como contrato vigente
> Las secciones históricas siguientes conservan el discovery que llevó a diseños descartados. La autoridad de implementación es `rio-playmaker` → `.sdd/features/new-component-context/2-technical/spec.md`.

- El contrato I/O vigente no tiene una fuente única: el CP/materializer define de facto qué keys consume y qué outputs devuelve; el front configura/proyecta el mapping en `parameters`, `properties_map`, `destinations[]`, presets y placeholders; Playmaker persiste los outputs y resuelve ese mapping antes del dispatch.
- Confirmación del equipo: al CP no deben llegar placeholders ni “keys por resolver”; recibe en `params` todas las variables ya resueltas por Playmaker. El JSON guardado desde el front es configuración/provenance, no la autoridad del valor runtime.
- En Playmaker actualizado (`d1741b8`), el pipeline nuevo y el legacy resuelven `${...}` contra `service.values` y desenvuelven wrappers `.value`; el pipeline lo hace mediante `ParameterResolutionService` desde el commit `fa73018a`.
- El result de CP/materializer se mezcla top-level y termina, sin aliases ni flatten, en el mismo JSON de `deployment.values` y `service.values`.
- El prototipo anterior mezclaba hechos distintos: cuando el placeholder era exacto, reconstruía el supuesto output productor con el valor efectivo consumidor. Esa igualdad no demuestra aliases, wrappers, coerciones ni transformaciones.
- La realineación captura en la misma pasada del resolver el output crudo leído de `service.values`, su `output_path`, el `consumer_path` y el fragmento realmente sustituido; el builder ya no relee ni recalcula y no fabrica outputs cuando falta evidencia.
- El contrato conserva los valores originales: `configured_value`, `value` efectivo y `outputs[*].value` runtime. `direction`, `value_type`, `sensitivity` y los issue codes son metadata suplementaria; no reemplazan los valores por códigos.
- Los P0 vigentes son: contrato ClickHouse camel/anidado vs front snake/plano; y aliases/routing que hacen que tipos visibles no lleguen al CP esperado.
- `component_type_registry` no valida create/update/deploy, no tiene publisher demostrado, genera un shape incompatible con JSON Schema Draft 7 y sólo contiene seeds Kafka stale.
- Existen campos sensibles sin trazabilidad completa: password condicional de ClickHouse persistido sin wrapper, logging completo de params en Fury y punto de cifrado pre-dispatch no demostrado.

## Decisiones que habilitaron diseños descartados (histórico)

- La iniciativa sólo creará en [[rio-playmaker]] un objeto `Context` efímero, calculado por request.
- `Context` no tendrá tabla, snapshot, backfill ni lifecycle persistido.
- `parameters`/properties continúan sin cambios; no se eliminan, sustituyen ni migran.
- Los control planes no consumirán `Context` en esta iniciativa.
- Context v1 sólo puede derivar datos cuya fuente/consumo está demostrado en [[signals-context-flow]]; un GAP no se rellena por convención o nombre.
- El envelope v1 de SDK separa identidad, `component.properties` consumidoras, `sources`/`destinations` con outputs runtime demostrados, mappings y `COMPLETE|PARTIAL|UNSUPPORTED`. Es extensible en serialización e immutable; su `toString` omite valores e identidades productoras.
- Para cada campo consumido, el valor canónico de Context debe ser el de `params` **después** de `ParameterResolutionService` y justo antes del dispatch. `ComponentDefinition.parameters` crudo sólo puede aportar configuración original y referencias de lineage; nunca reemplazar el valor efectivo ni actuar como contrato autoritativo del CP.
- Configured path, producer path, consumer path y valor sustituido se conservan separados. `DestinationParseService` entrega la correspondencia de paths cuando filtra/reindexa `destinations[]`; el builder no intenta reconstruirla desde el array efectivo. Un mapping queda `resolved=false` y genera issue cuando la misma pasada del resolver no aporta evidencia; no se infiere por igualdad de nombres o valores.
- La matriz conserva `14 AUDITADO`, pero Playmaker sólo habilita derivación ejecutable para 13 tipos con consumer efectivo y evidencia field-level. `gcp-kafka-topic` queda `UNSUPPORTED` por su GAP de routing actual y `aws-flink-sql-job` por falta de contrato field-level; ningún tipo copia parameters arbitrarios.
- Context viaja sólo en el `DispatchRequest` interno del pipeline. `BigQueueDispatchAdapter` continúa construyendo `DeploymentTriggerMessage` exclusivamente con `request.params()`; no se persiste Context ni se envía a los CP.
- La forma del contrato puede fijarse como v1, pero su derivación no está completa para todos los request paths: pipeline BigQueue y el `DispatchRequest` del adapter materializer están cubiertos; legacy/componente y el materializer directo quedan fuera hasta disponer de un carrier interno útil, sin calcular y descartar objetos sólo para aparentar cobertura.
- La SPEC técnica debe distinguir pipeline nuevo, legacy y materializer, y probar que el comportamiento actual de `parameters` permanece idéntico.
- El registry no puede tratarse hoy como autoridad contractual; cualquier rol futuro requiere una decisión explícita después de resolver sus gaps.
- ADR de alcance: [[2026-08-19-crear-context-ephemeral-create-only|Crear Context es efímero y create-only]].

## Gaps humanos/runtime pendientes

- Confirmar `component_type` y versión de template activos por ambiente para storage, GCP Kafka y aliases del front.
- Confirmar el alcance de rollout de la rama vigente de Flor (`feature/parse-params-pipeline` en las refs remotas actuales): el fix inicial de placeholders ya está en releases productivas, pero el endurecimiento de fallas por componente/batch aún no está mergeado a `develop/master`.
- Obtener evidencia redactada de cualquier publisher/seed runtime de capabilities y su semver real.
- Identificar el punto efectivo de cifrado KMS y el catálogo de campos redactados.
- Confirmar fleet/role Fury activo por ambiente; los outputs difieren entre orchestrator y router legacy.
- Confirmar quién inyecta `system_id`, `environment` y `criticality` cuando no vienen del adapter.
- Confirmar consumidores externos de outputs que la búsqueda local clasificó como “no consumidos”.
- Decidir el punto de creación para legacy/componente y materializer directo. Hoy no comparten `DispatchRequest`; crear Context para descartarlo no aporta comportamiento ni evidencia.
- Confirmar si `UPDATE` y `DEPROVISION` entrarán en una iteración posterior del pipeline: el builder soporta la operación, pero el punto conectado hoy crea Context para `PROVISION`.
- Determinar si la ausencia de una key en `service.values` debe abortar el deploy como hoy o producir un Context observable por otro mecanismo; actualmente el resolver falla antes de que exista `DispatchRequest`.

## ✅ Tareas

- [x] Discovery y matriz canónica en [[signals-context-flow]].
- [x] Spec funcional reescrito y publicado en SIG-573 (en review).
- [x] Spec técnica escrita **desde cero** y publicada en SIG-590; SIG-589 eliminada.
- [x] Plan de tasks (T-01..T-22) en `.sdd/features/new-component-context/3-tasks/tasks.md` del repo de playmaker.
- [x] Ramas `feature/new-component-context` creadas locales en los dos repos.
- [x] **PT-1 cerrada (2026-08-25):** no hay nada que cifrar del lado de Playmaker — los valores llegan cifrados del control plane. El flag y la cota de tamaño se eliminaron.
- [ ] **Enmendar SIG-573** con lo que pide §13 de SIG-590: reescribir la decisión cerrada de autorización con su predicado literal, y cambiar "copia importada" por "vecino en otro data product" en RF-6. (RF-4 ya no necesita enmienda: los valores viajan siempre.)
- [ ] **Sincronizar SIG-590 en Spellbook** con las enmiendas de la remediación y de T-24 (DT-24, DT-27, DT-28 eliminada, DT-31, DT-32, DT-33, PT-11, §5.5, §5.7, §7.2, §7.4, Q6/Q8, métricas y la nueva medición de tamaño). La copia SDD del repo está enmendada pero `.sdd/` está gitignoreado y no viaja en el PR.
- [ ] Pasar SIG-590 a review con el equipo.
- [ ] Resolver PT-2 a PT-10 de SIG-590.
- [x] Implementar y validar T-01..T-06 en `rio-sdk-events`: cinco records en `deployment.context`, campo opcional en el trigger, Javadoc normativo, `0.0.2-component-context`, CHANGELOG, suite y cobertura.
- [x] **T-23 challenge SDK:** `inputs` agregado a `LastDeployedVersion` y `RelatedComponent`, compatibilidad validada, suite/cobertura verdes y branch pusheada en `d6903aa`.
- [x] **T-24 productor Playmaker (2026-08-25):** Playmaker puebla `inputs` desde `component_definition.parameters` del mismo service slot que origina los `outputs` — la resolución devuelve el `ServiceModel` y los dos mapas salen de ahí, así que la estructura garantiza que no se mezclen. Gate cross-data-product aplicado a los dos mapas, revisión de sensibilidad hecha (negativo débil: `parameters` es JSON libre del usuario) y nueva medición de tamaño. Pusheado en `e33966b2e`.
- [x] **PRs abiertos:** SDK [#43](https://github.com/melisource/fury_rio-sdk-events/pull/43) mergeado y Playmaker [#1068](https://github.com/melisource/fury_rio-playmaker/pull/1068) en draft. Descripciones en [[Descripción PR — rio-sdk-events]], [[Descripción PR — rio-playmaker]] y [[Descripción PR — rio-playmaker — Crear Context (zord authoring)]].
- [x] Release `1.4.0` del SDK publicado desde `master` y dependencia de Playmaker actualizada.
- [x] **PR Playmaker listo para review:** body de [#1068](https://github.com/melisource/fury_rio-playmaker/pull/1068) reemplazado por [[Descripción PR — rio-playmaker]], 12/12 threads de David respondidos, C01 propio corregido y cinco checks verdes sobre `0a23579e9`.
- [ ] Antes del merge de Playmaker: publicar `rio-sdk-events 1.5.0` desde `master`, cambiar el pin de `0.0.2-component-version-identity` al semver definitivo y sincronizar SIG-573/SIG-590 en Spellbook.
- [ ] Antes del merge de Playmaker: validar la branch en preproducción.
- [r] [[Crear Context - Code Review Remediation]] arrancar + seguimiento #owner/me #type/supervision #area/meli
- [/] [[Crear Context - Discovery de Params en CPs]] arrancar + seguimiento #owner/me #type/supervision #area/meli

## 📆 Bitácora

- **2026-09-07 — SDK productivo, soft-delete y sincronización final:** Playmaker pasó de la dependencia temporal a `rio-sdk-events:1.5.0` en `7eaf93ab7`. El comentario de David se resolvió en `20f34308c` filtrando ambientes eliminados desde la query `findByDataProductIdInAndDeletedAtIsNull`; se agregaron pruebas para la coincidencia exacta y el fallback normalizado con un ambiente eliminado y otro activo. La branch se sincronizó con `develop @ b45eb328e`; el único conflicto fue aditivo en `CHANGELOG.md` y se conservaron ambas entradas. El merge quedó en `bd5536205`, pusheado y verificado contra origin. Suite completa: 3597 tests, 0 fallas, 0 errores, 2 skipped; `./gradlew check` PASS. GitHub reporta #1068 mergeable, con 5 checks exitosos, 1 omitido y ninguno pendiente o fallando; el estado BLOCKED corresponde únicamente al review requerido.

- **2026-09-03 (safety limit y versión de test)** — El `DeploymentTriggerMessage` completo se mide antes de publicar; `rio.playmaker.context.size` conserva el tamaño candidato incluso si supera la cota. Hasta 200 KiB viaja con Context; por encima, o si la medición falla, se registra `rio.playmaker.context.discarded` con `reason:too_large|measurement_failed` y se publica sin el campo, nunca truncado. En las pruebas funcionales el máximo observado era 4–5 KB. Branch principal `0a23579e9`, branch de test `9cc84fb06`, ambas pusheadas y al día con `develop @ be48d89a9`; `0.0.6-component-context-test` terminó exitosamente en Fury. Suite completa: 3578 tests, 0 fallas, 0 errores, 2 skipped y JaCoCo PASS. El body del PR y la respuesta #2 de David quedaron actualizados. Confirmado además que `username` ya sale de `claims.getUsername()` del Tiger token y sólo atraviesa `pipeline_execution.created_by` → `deployment_group.created_by` → Context; no se deriva del group id.

- **2026-09-03 (cierre de PR)** — Se revalidó [#1068](https://github.com/melisource/fury_rio-playmaker/pull/1068) contra `origin/feature/new-component-context @ f49789d2c` y `develop @ be48d89a9`: 32 archivos, +2563/−54. El body remoto se reemplazó por una versión sin detalles obsoletos, los 12 threads de David quedaron respondidos sin resolverlos en su nombre y el comentario propio C01 fue corregido. Rerun local: 3574 tests, 0 fallas, 0 errores, 2 skipped y JaCoCo PASS; cinco checks remotos verdes y reviewer automático sin findings. BigQueue no documenta un hard limit individual, pero desaconseja mensajes sobre 200 KB; un guard futuro debe omitir el Context entero cuando el mensaje completo exceda el presupuesto, nunca truncarlo. Pendientes reales de merge: release definitivo del SDK, sincronización de SIG-573/SIG-590 y validación runtime de `0.0.5-component-context-test`.

- **2026-09-03** — **Contrato cerrado y ramas pusheadas.** `feature/new-component-context` @ `97065eb17` y `feature/new-component-context-test` @ `ba63a3d63`, las dos con `develop` mergeado y con `origin` apuntando al mismo commit: el force-push que figuraba como bloqueante desde el 2026-09-01 **ya ocurrió**. Playmaker consume `rio-sdk-events:0.0.1-component-version-identity` (rama `feature/component-version-identity` @ `8932dec`). Lo que cerró el contrato: `ComponentContext.username` como `String` nullable resuelto del tiger token vía `group.getCreatedBy()`; `Component.version` y `LastDeployedVersion.version` de `String` a `@NotNull Long` y con el significado de **id de `component_definition`** —el `parameters["version"]` era un semver retirado, 76 de 2193 definiciones—; el tipo del vecino sin fallback a `component_template`; sólo un `imported` viaja con datos; y sin denylist de `sensitive`. **Hecho de contrato que no hay que perder:** una llave puede aparecer en `inputs` y en `outputs` con valores distintos y **`outputs` es la autoridad** — el caso ejemplar es `topic_name`, lógico en `inputs` y físico desplegado en `outputs`, con 952 coincidencias de llave en `playmkrprod`, 557 eco puro y 395 con valor distinto, 361 de ellas `topic_name` de `aws-msk-topic`; por eso no se resta a `outputs` lo que ya está en `inputs`. **Dos afirmaciones propias corregidas:** el flag `sensitive` **sí tiene productor** —`ClickHouseGrantedTableCreator` en `rio-materializer`, sobre passwords ya cifradas con KMS, con al menos 48 filas de `service` y 52 de `deployment` en `playmkrprod`—, así que "métrica clavada en 0" era falso y el relevamiento que lo concluyó había excluido `rio-materializer`; y el hallazgo de que `last_deployed_version` no se poblaba nunca por falta de un param `version` quedó **superado**, porque el campo ya no lee `parameters`. La razón para no filtrar `sensitive` es la paridad con `params`, no la ausencia de productor. **Fuera de alcance nuevo:** las referencias con environment explícito (`${comp[production].prop}`), 8 definiciones en toda la base. Los textos aprobados de **DD-7** y **DD-14** quedaron congelados en `/Users/rjara/context-pendiente-documentacion.md` hasta validar la versión funcional y son autoritativos. Pendiente real: `fury create-version 0.0.4-component-context-test`.

- **2026-09-01 (5)** — Commit `ed23aa76a`: **los `inputs` ahora llegan resueltos** —pasan por el mismo `ParameterResolutionService` que resuelve `params`, así que desaparece la asimetría del template `${vecino.propiedad}`— y **los componentes importados se resuelven** siguiendo `sourceComponentId` hasta el original, con el ambiente del original por nombre más el fallback de normalización, y **sin ninguna autorización**, que es lo que `params` ya hace. Corregido un error propio de las pasadas anteriores: una copia importada vive **dentro** del data product que importa; lo que apunta afuera es `sourceComponentId`, así que el bullet de "sin camino cross-data-product" era falso. Métrica nueva `rio.playmaker.context.size` (histograma en bytes). [[Descripción PR — rio-playmaker]] **acortada y limpiada** según el principio del owner —*la misma data que `params`, pero estructurada y con sentido*—: se sacaron todas las menciones de logging, el párrafo del snapshot que envejece, "verbatim", la explicación de la semántica de `unresolved`, dos puntos de la guía de revisión y el caveat de evidencia. Se agregó un **diagrama Mermaid** del flujo de dispatch con `classDef` marcando lo nuevo contra lo preexistente, validado con `mermaid@11` (parse + render) y revisado visualmente. Suite **3451 tests** / 0 fallas / 0 errores / 2 skipped; diff 27 archivos +2238/−54. Sigue pendiente el force-push. El PR remoto no se tocó.

- **2026-09-01 (4)** — Dos correcciones de código sobre la rama (`ed23aa76a`, amend) reflejadas en [[Descripción PR — rio-playmaker]]. **Guard de ambiente:** `Component.last_deployed_version` se omite cuando el último deployment completado es de otro ambiente, contado como `env_mismatch`; la causa es que `BatchDispatchServiceImpl.resolveService` resuelve el service por id sin filtrar por ambiente (`findAllById`), así que la coincidencia no está garantizada por construcción. El guard es conservador: con environment o id null no asume mismatch. **Semántica de `unresolved`:** ya no cuenta documentos ausentes o en blanco, porque un componente sin `parameters` o sin `_values` es un estado normal; como el resolver se invoca dos veces por entidad, eso le ponía al contador un piso de ruido estructural que lo volvía inalertable. Hoy `unresolved` = documento presente pero malformado, más versión ausente, y la métrica pasa a **tres** razones. **Agregado:** que `inputs` viaja **pre-resolución** —`params` pasa por `resolveComponentParameters` y expande `${vecino.propiedad}`, el Context lee `component_definition.parameters` crudo—, así que un consumidor puede recibir el template literal; queda como pregunta abierta para el primer CP que adopte el campo. Suite **3451 tests** / 0 fallas / 0 errores / 2 skipped; diff 27 archivos +2238/−54. **Dato corregido contra la evidencia:** me pasaron que `ContextValueResolverTest` subía a 11 casos y tiene **9** (9 `@Test` en el fuente y 9 en el XML; el total 3433→3435 lo explican íntegramente los 23→25 de `ComponentContextServiceTest`). Sigue pendiente el force-push. El PR remoto no se tocó.

- **2026-09-01 (3)** — Branch reescrita a **un único commit convencional** `ed23aa76a` rebasado sobre `develop @ 1f3e741b0`, y [[Descripción PR — rio-playmaker]] corregida sobre ese estado. Cambios de fondo pedidos por el owner: la sección `Descripción` se reescribió **autocontenida, sin usar como base ningún documento** —ni el funcional, ni el técnico, ni una descripción anterior—, partiendo del cambio mismo y conservando el árbol ASCII del contrato. Se agregaron cuatro cosas que faltaban: un bloque titulado **"Lo que no cambia"** que consolida los cinco no-cambios de riesgo, que **el snapshot envejece y nadie lo refresca** —se calcula en el dispatch, no se persiste, un consumidor no debe asumir vigencia—, que **la prohibición de loguear cruza el boundary hacia el consumidor** (el javadoc de `ComponentContext` lo declara textualmente y ningún CP tiene regla propia), y el **caveat de evidencia dentro del cuerpo del PR** y no sólo en las notas internas. Checklist: conventional commits pasa a `[x]` y desaparecen las notas de squash merge y de commits no convencionales. Suite **3451 tests** / 0 fallas / 0 errores / 2 skipped preexistentes. **Bloqueante que queda:** falta force-push, `origin` sigue en `3c788a390` y los checks verdes son del código viejo. El PR remoto no se tocó.

- **2026-09-01 (2)** — [[Descripción PR — rio-playmaker]] **reescrita de cero** contra el código del worktree `rio-playmaker-context-yagni`, porque el cuerpo remoto de #1068 y la versión anterior de la nota afirmaban cuatro cosas que ya no existen en el código: validación de contrato en el productor, acceso cross-data-product con autorización de importación aprobada ligando el par `(copia, original)`, equivalencia de ambientes con `EnvironmentType` normalizando `Test`/`Sandbox`, y Context obligatorio con falla de derivación que cuesta el deployment. Ninguna frase se heredó. El estado descrito: Context opcional y campo nullable, dos mapas por entidad siempre del mismo service slot, vecino de otro data product con mapas vacíos, vecino sin tipo resoluble omitido, `ValueEnvelope` compartido reemplazando tres unwrap bespoke, dos counters con etiquetas disjuntas, `DeploymentSchemaVersion.CURRENT` en `1`. Evidencia: 27 archivos +2238/−54 contra `develop @ fe899d5a4`, 3422 tests / 0 fallas / 0 errores / 2 skipped preexistentes. **Bloqueantes levantados:** el estado descrito no está commiteado ni pusheado (21 archivos de diferencia contra HEAD `3c788a390`, +173/−1350, repartidos entre índice y working tree), los checks remotos verdes corrieron sobre el código anterior, y los commits intermedios no son convencionales. El PR remoto no se tocó: la skill sólo prepara el recurso del vault.

- **2026-08-27** — Dogfood del nuevo Authoring Zord sobre `feature/new-component-context`: `pr-description` generó una nueva descripción para Playmaker a partir de diff, commits, SIG-573, SIG-590, tasks y progreso; `document` generó [[Documento técnico — rio-playmaker — visión general]], un overview de 647 palabras para onboarding. El zord pasó 458 tests y build TypeScript; la suite Playmaker no se ejecutó en esta sesión. Se dejaron visibles como bloqueantes el alcance ajeno de ClickHouse/Swagger, `graphify-out/` sin trackear y la discrepancia entre `componentTemplateCode` y la clave de routing descrita por SIG-590.

- **2026-08-26 (2)** — El cuerpo listo para GitHub de [[Descripción PR — rio-playmaker]] fue traducido completamente al español por instrucción explícita del owner. Se preservaron el orden y el alcance del template del repo, pero se adaptaron encabezados, narrativa, checklists, guía de review y evidencia de pruebas; el PR remoto #1068 sigue sin modificaciones.

- **2026-08-26** — [[Descripción PR — rio-playmaker]] mejorada sobre el estado real de [PR #1068](https://github.com/melisource/fury_rio-playmaker/pull/1068): branch `658f8f615` mergeada con `develop @ 0324375e8`, 25 archivos +1943/−27, 3250 tests verdes, JaCoCo 100% en las tres clases principales del Context y 5/5 checks remotos PASS. La narrativa ahora sigue problema → contrato → flujo de dispatch → hotspots de review, corrige el SDK stale (`1.4.0` ya está mergeado/publicado) y deja visibles los bloqueantes reales: sincronizar SIG-590 y retirar `swagger.yaml`. El cuerpo remoto no se modificó: la skill `pr-description` sólo prepara el recurso del vault.

- **2026-08-25 (5)** — **Descripciones de PR de los dos repos reescritas** sobre el estado real de hoy: [[Descripción PR — rio-playmaker]] (`e33966b2e`, 6 commits, 25 archivos, 3181 tests) y [[Descripción PR — rio-sdk-events]] (`4966eaa`, 8 commits, 10 archivos, 701 tests + gate PASS). Las anteriores describían la entrega previa al code review y estaban desactualizadas en identidad, contenido y bloqueantes. Las dos explican ahora la distinción que pidió el owner: **`inputs` es configuración ingresada por el usuario** (`component_definition.parameters`) y **`outputs` son los datos que generó el control plane describiendo la infraestructura que provisionó** (`_values`), nunca mezcladas y siempre del mismo slot. Bloqueantes levantados: el SDK fija `version = '1.4.0'` en una rama feature con el CHANGELOG ya en heading de release —eso sale desde `master`—, y Playmaker arrastra `docs/specs/swagger.yaml` en el diff commiteado.

- **2026-08-25 (4)** — **Contenedores del contrato normalizados parejo (DT-33)** y verificación de cobertura por batch. Las cuatro listas/mapas hacen `null → vacío`; antes sólo `inputs` lo hacía y los otros tres tiraban NPE, lo que habría reventado a un CP al deserializar un payload sin la clave. SDK en `0.0.6-component-context-null-safe` (701 tests, gate PASS), Playmaker apuntando ahí (3181 tests). Confirmado además que el Context se genera **en todos los batches** —`safelyBuildContext` está en `dispatchItem`, dentro del único `dispatchBatch` que usan los tres caminos de dispatch—, y que el batch N recibe un Context más rico que el N−1 porque los outputs del batch anterior ya están escritos.

- **2026-08-25 (3)** — **T-24 implementada: Playmaker puebla `inputs`.** `LastDeployedVersion.inputs` sale de `deployment.componentDefinition.parameters` del mismo deployment; `RelatedComponent.inputs` de `service.componentDefinition.parameters` del **mismo slot** que aporta los outputs — la resolución devuelve el `ServiceModel` y los dos mapas salen de ahí, así que la estructura garantiza que nunca se publique la configuración de una entidad junto a los resultados de otra (DT-32). `OutputResolver` pasó a `ContextValueResolver` con `resolveInputs`/`resolveOutputs`: la única diferencia entre los dos es desenvolver o no el envelope del CP, y los inputs **no** lo desenvuelven porque una clave de configuración con un campo `value` es data del usuario (DT-31). Suite 3181 tests verdes, cobertura 99-100%. Corregido de paso: `build.gradle` apuntaba a `0.0.5-component-context`, versión que no existe — la real es `0.0.5-component-context-inputs`. Detalle en [[Crear Context - Code Review Remediation]].

- **2026-08-25** — Challenge solicitado: separar configuración de usuario (`inputs`) de resultados generados por CP (`outputs`) en vez de mezclarlos en un único mapa. La evaluación confirma que es un cambio aditivo viable si el SDK normaliza payloads antiguos sin `inputs` a `{}` y conserva los constructores previos. Se actualizaron la SPEC funcional, SIG-590 local, tasks y progreso; la branch del SDK incorpora los campos, copias inmutables, `toString` redactado para ambos mapas, pruebas de wire/legacy y versión de test `0.0.5-component-context-inputs`. Gate completo: 699 tests y `jacocoTestCoverageVerification` PASS; commit `d6903aa` pusheado a `origin/feature/new-component-context`. Poblar los mapas en Playmaker queda explícitamente fuera del delta de branch pedido y se registra como T-24. Riesgo a resolver en T-24: `inputs` no hereda automáticamente el cifrado de los outputs del CP.

- **2026-08-25** — **Code review de `feature/new-component-context` en Playmaker, y remediación completa en la misma sesión.** El review salió BLOQUEADO por un falso positivo (el SDK `0.0.4-component-context` no resolvía: faltaba VPN) más 13 findings. El owner aceptó 12, corrigió uno —el unwrap de `{value:…}` es deliberado y replica `ParameterParseServiceImpl`— y amplió dos hacia decisiones de diseño: **los `outputs` se emiten siempre** (`rio.context.outputs.enabled` lo había colado un agente; los valores sensibles ya vienen cifrados del control plane) y **el Context nunca se corta por tamaño**. Eso **deroga DT-27 y T-18 de SIG-590 y cierra PT-1**, que dejó de bloquear el paso 7 del plan de entrega porque ya no hay flag que encender. Ejecución y evidencia en [[Crear Context - Code Review Remediation]]: 3174 tests verdes, cobertura de las clases del Context en 99-100%. El CHANGELOG de Playmaker ahora nombra `rio-sdk-events:1.4.0`; `build.gradle` sigue en la versión de prueba hasta el release desde `master`. **Pendiente:** sincronizar las enmiendas de SIG-590 en Spellbook — la copia SDD del repo está en `.gitignore` y no viaja en el PR.

- **2026-08-25** — Se creó el proyecto de comprensión [[Crear Context - Discovery de Params en CPs]] para auditar los 7 control planes y los boundaries front/Playmaker/materializer antes de implementar Context en los CPs. La tarea puente queda en WIP; el discovery no se mezcla con el delivery de Context.
- **2026-08-24** — [[Descripción PR — rio-playmaker]] compactada: la sección `Description` se reescribió con bullets cortos y un párrafo problema/solución al frente, en vez de párrafos largos, calibrando el tono contra cinco PRs reales de `rio-playmaker` (#1010, #1026, #1036, #1047, #1059) que trajo el usuario como referencia. Sin cambios de evidencia: mismos SHAs, mismo diffstat, mismo gate de merge por versión de prueba del SDK. Cambio solo en el vault, el PR real en GitHub no se tocó.
- **2026-08-24** — Las dos ramas quedan **commiteadas y pusheadas**: `rio-sdk-events @ e670af8` (3 commits, 10 archivos +463/−10) y `rio-playmaker @ 1cd184a` (2 commits, 19 archivos +1367/−12, rama creada en el remoto). Suites de la sesión: SDK 696 tests / 0 fallas + `jacocoTestCoverageVerification` PASS; Playmaker 3145 tests / 0 fallas / 2 skipped. Descripciones de PR reescritas y **alineadas entre sí** en estructura y voz, cada una con el template `.github` de su repo: [[Descripción PR — rio-sdk-events]] y [[Descripción PR — rio-playmaker]]. **Un solo gate de merge**, el mismo de los dos lados: los dos repos apuntan a la versión de prueba `0.0.3-component-context`, así que el orden es merge del SDK → release `1.4.0` desde `master` → merge de Playmaker. El resto es higiene previa sin impacto en código ni tests: squashear los commits `versión` y `ok` del SDK, restaurar el newline de su `build.gradle`, confirmar el renombre del heading del `CHANGELOG`, y restaurar `docs/specs/swagger.yaml` en Playmaker, que la suite ensucia sola.
- **2026-08-24** — Descripciones de PR escritas para las dos entregas vigentes: [[Descripción PR — rio-playmaker]] sobre `feature/new-component-context` (working tree contra `develop @ 0524ce49e`) y [[Descripción PR — rio-sdk-events]] sobre `feature/new-component-context @ aac690d`. Suites corridas en la sesión: Playmaker 3.144 tests / 0 fallas / 2 skipped, SDK 696 tests / 0 fallas + `jacocoTestCoverageVerification` PASS. Las dos notas anteriores se renombraron a `(entrega descartada)`. En la misma pasada se formalizó el procedimiento: la mecánica de descripciones de PR salió de `signals-code-review` y pasó a la skill propia [[pr-description]], con su cara humana en [[Descripciones de PR — recurso del proyecto en el vault]]. Bloqueantes levantados: Playmaker sin commits y con seis archivos sin trackear, base 14 commits detrás de `origin/develop`, dependencia pinneada a la versión de prueba del SDK, y ruido de newline en `swagger.yaml`; SDK con versión de prueba `0.0.3-component-context` y commit `versión` en español contra su propio `CODING_GUIDELINES.md`.
- **2026-08-24** — SDK T-01..T-06 implementado desde la base limpia `master @ 9d86eb8` en `feature/new-component-context`: cinco records top-level bajo `deployment.context`, `DeploymentTriggerMessage.context` nullable con constructor compatible, `schema_version` intacto, Javadoc de no-cifrado/no-logs/snapshot, versión de prueba `0.0.2-component-context` y CHANGELOG. Suite completa + `jacocoTestCoverageVerification` PASS. La SPEC canónica se resolvió al repo `rio-playmaker/.sdd/features/new-component-context/`; los mirrors del vault quedaron archivados. T-07 sigue pendiente: merge y release `1.4.0` exclusivamente desde `master`.
- **2026-08-20** — **Spec técnica reescrita de cero y republicada como SIG-590**; SIG-589 eliminada. Se descarta la implementación anterior completa: ramas nuevas `feature/new-component-context` en los dos repos, sin reutilizar código. La spec pasó por un challenge de cuatro clases (Sage, Cleric, Ranger, Paladin) que devolvió dos CRITICAL y dos HIGH, todos integrados. Los tres hallazgos que cambiaron el diseño: el gate de autorización cross-data-product tiene que colgar de la comparación de data products y no de `sourceComponentId` —`component_relations` permite un vecino foráneo que no es copia—, la aprobación tiene que ligar el par `(copia, original)` y el `requestingDataProduct` o hay confused deputy, y el cifrado KMS que el contrato asume es código muerto. Detalle en `80-agents/journal/logs/2026-08-20-crear-context-technical-spec-from-scratch.md`.
- **2026-08-20** — Cuarta pasada del contrato: campos planos a objetos (`data_product`, `component`, `component.last_deployed_version`) más `id` en `RelatedComponent` y outputs del propio componente. Funcional SIG-573 reescrito de cero con el usuario; **spec técnica escrita de cero y publicada como [SIG-589](https://spellbook.adminml.com/projects/SIG/specs/SIG-589)** (draft), con el delta por repo y los tres bugs a cerrar en la misma pasada. Se borró el discovery por tipo de componente de la spec técnica: el contrato nuevo no tiene lista blanca ni contratos por tipo (RF-2). El código de las dos branches queda por detrás del spec. Detalle en `80-agents/journal/logs/2026-08-20-crear-context-technical-spec-rewrite.md`.
- **2026-08-19** — Code review de la entrega en los dos repos, con suites corridas en la sesión: rio-sdk-events 696 tests verdes y gate de cobertura 88.8% superado; rio-playmaker 3141 tests verdes. Resultado: **aprobado con reservas**, 4 findings de corrección (sufijo `%completed` que captura undeploy, garantía "never throws" incompleta, outputs anidados descartados en silencio, `findById` por vecino importado contra el batch del resto) y 5 de documentación/dead code (CHANGELOG del SDK, javadoc de sensibilidad, constraints decorativos, SPEC técnica desalineada, commit `wip` en la branch del SDK). Guía de lectura del diff en [[Guía de implementación — Component Context]]; descripciones de PR por repo desde el template `.github` de cada uno. Skill de revisión creada: `signals-code-review`.
- **2026-08-19** — Discovery cerrado y prototipo realineado; suites completas y cobertura exitosas. Detalle único en `80-agents/journal/logs/2026-08-19-crear-context-scope-and-io-research.md`.
- **2026-08-19** — Corrección de foco del spec funcional: el problema es la falta de información en los CP, no la inversión del contrato I/O. Context redefinido como vehículo de información; v1 = crear y enviar en el mensaje. `DeploymentTriggerMessage.context` agregado con constructor de compatibilidad; adapter del pipeline lo publica. Suites verdes.
- **2026-08-19** — Contrato simplificado y reimplementado de cero: se descartó el envelope rico (properties/mappings/issues/completeness) por `dataProduct`+`lastVersion`+`sources`/`destinations`. Outputs pasan a viajar resueltos. Spec condensado y publicado en SIG-573. Entrega squasheada en `feature/component-context`, 1 commit sobre develop. Detalle en `80-agents/journal/logs/2026-08-19-crear-context-simplified-contract-and-squash.md`.
- **2026-08-19** — Cambio de foco a derivación topológica tras corrección del equipo. Prototipo referencial preservado en commit antes del rediseño. Implementación nueva sobre la rama de flor, con SDK local `1.5.0-SIG573-LOCAL`. 14 tests nuevos del builder y suite completa de playmaker en verde. SPECs funcional y técnica en este proyecto.

## Links al Atlas

- [[signals-context-flow]] — fuente canónica: provenance, universo, matrices field-level, productores→consumidores, registry, mismatches y preguntas.
- [[deploy-component]] — journey del contrato distribuido y su dolor.
- [[deploy-request-path]] — mapa de transporte de los tres paths.
- [[playmaker-deploy-flow]] — transacción, batches, dispatch async y result loop.
- [[Onboarding Signals]] — contexto de aprendizaje del ecosistema.

## Resuelto: el javadoc callampa del SDK

`ComponentContext` en `rio-sdk-events 1.4.0` lleva en su javadoc una prohibición dirigida a los consumidores: *"Consumers MUST NOT log this context or any input or output value at any level"*, más la advertencia de que ninguno de los dos mapas viene cifrado y que el snapshot es del dispatch y no del consumo.

**El problema no es que sea falso, es que no es de nadie.** Lo escribimos nosotros en esta misma iniciativa, así que es una regla que nos dimos a nosotros mismos y que después se citó como si fuera una norma externa. No hay ningún mecanismo que la haga cumplir: es texto en un javadoc de una librería, y depende de la buena fe de cada equipo que la lea. Presentarla como control de seguridad es engañoso, y arrastrarla a la descripción de un PR sólo genera ruido y preguntas que nadie puede responder.

**Resuelto en la iteración 1.5** — `31b674d` elimina la prohibición de logging y las afirmaciones incorrectas sobre cifrado del Javadoc de `ComponentContext` y `DeploymentTriggerMessage`. La documentación queda limitada a forma, semántica y alcance del contrato; el PR #46 tampoco incluye esa regla.

Si más adelante se quiere un control real sobre la exposición de valores, el camino es una allowlist por tipo de componente, y eso es alcance de la iniciativa **discovery**, no de un javadoc.

## Estado al 2026-09-03

Ramas sincronizadas con `develop @ be48d89a9` (entraron los 9 commits de `import-authorization-legacy-status`, `migrate-skip-draft-components` y `migrate-skip-unapproved-imports`; el único conflicto fue `CHANGELOG.md`, resuelto conservando las dos entradas de `[Unreleased]`).

| Repo | Rama | HEAD | Estado |
|---|---|---|---|
| `rio-playmaker` | `feature/new-component-context` | `0a23579e9` | Safety limit y remediación final commiteados y pusheados; local y origin coinciden |
| `rio-playmaker` | `feature/new-component-context-test` | `9cc84fb06` | Merge de la principal pusheado, preservando el log de `BigQueueDispatchAdapter`; tag `0.0.6-component-context-test` terminado exitosamente |
| `rio-sdk-events` | `feature/component-version-identity` | `8932dec` | versión de prueba `0.0.1-component-version-identity` publicada; playmaker la pinnea |

**El contrato creció en tres campos y perdió una dependencia falsa:**

- `ComponentContext.username` — el usuario que disparó el deploy, desde `group.getCreatedBy()`, que `PipelineDeployServiceImpl:128` resuelve del tiger token. Cero queries nuevas.
- `Component.version` — el `component_definition` que se está desplegando. El par con `last_deployed_version.version` es lo que vuelve accionable el snapshot, porque el trigger no llevaba ningún otro identificador de la configuración en vuelo.
- `LastDeployedVersion.version` — pasó a `Long` con el id de la definición desplegada. Antes leía `parameters["version"]`, el semver retirado, y el campo se suprimía en ~96% de los dispatches. Ver [[rio-versiona-un-componente-por-el-id-de-su-component-definition]].
- El tipo de un vecino sale sólo de `component_template_code`, sin fallback a `component_template`. El fallback nunca disparaba y esa columna guarda ULIDs y nombres de display, nunca un tipo de ruteo.

**Alcance cerrado:** sólo un componente **imported** viaja con sus datos; una referencia que nombra otro data product sin importación viaja con identidad y mapas vacíos, que es lo que ya hacía `resolveSlot`. Las referencias con environment explícito (8 definiciones en toda la base) quedan fuera de alcance. Ver [[que-alcanza-una-referencia-de-params-versus-el-context]].

**Descartado con fundamento:** filtrar `outputs` por el flag `sensitive`. Esos valores están cifrados con KMS, y `params` ya publica lo mismo hoy vía `${}` — filtrar sólo en el Context no arregla nada y rompe la paridad con el mecanismo que se reemplaza. El `password` en claro de `DeploymentCommandResult.forCreateMV` es bug del CP de ClickHouse, dueño ajeno, fuera de alcance.

**Validación posterior a las versiones (2026-09-03):** el smoke funcional publicado muestra `username`, identidad del data product, `Component.version`, `last_deployed_version` con su definición/inputs/outputs y relaciones source/destination con valores resueltos. La suite local quedó en **3578 tests, 0 fallas, 0 errores y 2 skipped**, con `jacocoTestCoverageVerification` PASS; `ComponentContextService` quedó en 99,6% line y 96,2% branch. El safety limit se probó por debajo, exactamente en y por encima de 200 KiB, y ante un fallo de medición.

La auditoría asistida confirmó que los **12 comentarios de David están abordados**. Se corrigieron además cuatro gaps encontrados al revalidar: el ambiente stub del camino v1 ahora se hidrata antes de resolver imports; los originales importados, ambientes y slots se cargan en batches en vez de N+1; la query de slots usa `LEFT JOIN` para no perder filas legacy; y `context.derivation:success` se cuenta al construir el request, no después de publicar. Las respuestas 3 y 8 de `/Users/rjara/pr-1068-respuestas-david.md` quedaron corregidas: `rio-materializer` sí produce `sensitive:true`, y la versión ya sale de `component_definition.id`.

Zord ejecutó sus siete revisores con Claude sobre el estado efectivo contra `origin/develop`. El límite bundled de USD 0,50 era insuficiente y devolvía `zords: []`; se elevó temporalmente a USD 1,00 para la ejecución y luego se restauró, sin dejar cambios en el CLI. Resultado final: **security 0 findings**, `human-review.needsHumanReview = false`, sin critical ni high después de corregir la query batch con `LEFT JOIN FETCH`. Quedan observaciones medium/low de arquitectura y un riesgo real: `ComponentContextService.build()` sigue ejecutándose una vez por componente del batch. Resolverlo bien exige un snapshot/DataLoader por batch que comparta deployments, relaciones, vecinos, ambientes, slots y resolución de placeholders; queda fuera de este PR. El supuesto N+1 de `resolveEnvironment` no aplica al batch normal —recibe el ambiente completo— y el único stub conocido es `createSingle`, que despacha `List.of(deltaEntry)`.

**Pendiente:** registrar el DataLoader/snapshot por batch como optimización posterior, sincronizar SIG-573/SIG-590, publicar el SDK definitivo y validar el runtime. `0.0.6-component-context-test`, creada desde `9cc84fb06`, terminó exitosamente en Fury.

Ojo con [[rio-playmaker-claude-md-colision-de-mayusculas-bloquea-rebase]]: obliga a mergear en vez de rebasear y ensucia el árbol de forma permanente, de ahí el `--skip-dirty-check`.

## Contrato cerrado — 2026-09-03

Ramas **pusheadas** y al día con develop: `feature/new-component-context` @ **`0a23579e9`** y `feature/new-component-context-test` @ **`9cc84fb06`**, las dos con `origin` apuntando al mismo commit. SDK en `feature/component-version-identity` @ `8932dec`, versión **`0.0.1-component-version-identity`**, que es la que consume Playmaker. La versión **`0.0.6-component-context-test`** terminó exitosamente en Fury; falta validación runtime.

Lo que cerró el contrato:

- **`ComponentContext.username`** — `String` nullable: el usuario que disparó el deployment, resuelto de su tiger token vía `group.getCreatedBy()`.
- **`Component.version`** y **`LastDeployedVersion.version`** — de `String` a **`@NotNull Long`**, y son el **id de `component_definition`**, no un semver. El `parameters["version"]` era un semver retirado, presente en 76 de 2193 definiciones. Iguales cuando se redespliega la misma definición, mayor cuando avanzó, menor en un rollback.
- **El tipo del vecino perdió el fallback a `component_template`.**
- **Sólo un `imported` viaja con datos.**
- **Sin denylist de `sensitive`**: los valores marcados están cifrados y `params` ya publica lo mismo vía `${}`.

**`outputs` es la autoridad, y esto hay que no perderlo:** una llave puede aparecer en `inputs` y en `outputs` con valores **distintos**. El caso ejemplar es `topic_name` — `inputs` lleva el nombre lógico, `outputs` el físico desplegado. En `playmkrprod`: 952 coincidencias de llave, 557 eco puro y **395 con valor distinto**, 361 de ellas `topic_name` de `aws-msk-topic`. Un CP que lea `topic_name` de `inputs` se conecta a un tópico que no existe. Por eso no se resta a `outputs` lo que está en `inputs`.

**Corrección de una afirmación que circuló como cierta:** el flag `sensitive` **sí tiene productor** — `ClickHouseGrantedTableCreator` en `rio-materializer` lo escribe en `true` sobre las passwords CRUD y readonly de ClickHouse, inmediatamente después de cifrarlas con KMS, y en `playmkrprod` hay al menos 48 filas de `service` y 52 de `deployment` con el flag. El relevamiento que concluyó lo contrario había excluido `rio-materializer`. La razón para no filtrar es la paridad con `params`, no la ausencia de productor. Ver [[clickhouse-controlplane-plaintext-password-en-output-de-deployment]] para el caso distinto del `password` en claro, que va sin envelope ni flag.

Los textos aprobados de **DD-7** y **DD-14** viven congelados en `/Users/rjara/context-pendiente-documentacion.md` hasta validar la versión funcional, y son autoritativos: se incorporan literalmente a SIG-590, no se reescriben.

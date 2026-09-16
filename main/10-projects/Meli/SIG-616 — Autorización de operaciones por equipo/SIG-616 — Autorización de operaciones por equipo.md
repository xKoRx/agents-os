---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P2
area: "[[Meli]]"
parent:
sprint:
start: 2026-09-14
due:
progress: 75
repo: https://github.com/melisource/fury_rio-playmaker
jira:
prs:
  - https://github.com/melisource/fury_rio-playmaker/pull/1169
  - https://github.com/melisource/fury_rio-playmaker/pull/1178
aliases:
  - SIG-616
  - Autorización por equipo en Playmaker
tags:
  - kind/project
  - area/meli
created: "2026-09-14"
updated: "2026-09-16"
---

# SIG-616 — Autorización de operaciones por equipo

%% Naming: SIG-616 — Autorización de operaciones por equipo es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ SIG-616 — Autorización de operaciones por equipo
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P2 · **Sprint:** —
> _parent / sprint / repo / jira / prs son opcionales._

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> `owner: me` → **proyecto humano**: la iniciativa/esfuerzo que conduces tú.
> `owner: agent` → **proyecto de agente**: un curro delegado, con detalle pesado que escribe y sigue un agente. Casi siempre es subproyecto de uno humano y vive en la subcarpeta `agentes/` de su iniciativa.
> `root: true` solo en **iniciativas raíz** (sin `parent`). Todo subproyecto debe setear `parent`; si no, aparece como huérfano en [[Panel de Proyectos]].
>
> **Tarea puente:** cuando este proyecto es `owner: agent`, en su proyecto **padre** debe existir UNA sola tarea humana que lo representa (arrancar + seguimiento). Así tu cockpit ve una línea por curro delegado, no las tareas internas del agente. Ejemplo, en el padre:
> `- [ ] [[SIG-616 — Autorización de operaciones por equipo]] arrancar + seguimiento #owner/me #type/supervision #area/meli`

## 🎯 Objetivo

- Diseñar e implementar la autorización server-side de operaciones de componentes por equipo en `rio-playmaker`, tomando como referencia [SIG-616 en Spellbook](https://spellbook.adminml.com/projects/SIG/specs/SIG-616).
- Asegurar que Playmaker autorice con identidad Tiger validada, ownership persistido del Data Product y rol ACME; el cambio debe ser reutilizable en actions, deployments y demás mutaciones sin trasladar esa responsabilidad a los control planes.

## 📊 Estado actual

- **Slice 3 publicado:** `feature/operation-authorization-by-team-f3@25a50c10c`, con base exacta `feature/operation-authorization-by-team-f2@626585ca9`, está publicado en [PR #1178](https://github.com/melisource/fury_rio-playmaker/pull/1178) y listo para review. Protege las siete rutas de mutación/deploy de componentes con `DEV_AND_UP`; `/data-products/v2` conserva explícitamente el comportamiento pre-F3. Suite local: 3.868 tests, 0 fallas, 2 skips preexistentes; build exitoso. Gate de datos productivos y smoke Tiger/ACME no productivo siguen pendientes.
- **Slice 4 en rama local:** `feature/operation-authorization-by-team-f4@cf4544b1a`, derivada de `origin/feature/operation-authorization-by-team-f3@1a8b4d972`. Protege relaciones directas y las cinco mutaciones de pipeline, incluido deploy, con ownership persistido y `DEV_AND_UP`; suite forzada: 3.925 tests, 0 fallas, 2 skips. Cobertura diferencial F4: 100,00% line (91/91) / 100,00% branch (16/16); cobertura global: 97,15% line (14.331/14.752) / 91,45% branch (3.935/4.303). Gate de datos y smoke externo siguen pendientes por falta de acceso.
- **Avance posterior de F3:** después de crear F4, `origin/feature/operation-authorization-by-team-f3` avanzó a `1f39b5561`. F4 conserva el base seleccionado `1a8b4d972`; el commit externo relaja el fail-closed de ownership incompleto y contradice la decisión vigente de Slice 4, por lo que no se incorporó silenciosamente.
- **Fase actual:** Slice 1 está implementado en `feature/operation-authorization-by-team-f1@fbf05159e` y publicado en [PR #1169](https://github.com/melisource/fury_rio-playmaker/pull/1169). Slice 2 / [SIG-623](https://spellbook.adminml.com/projects/SIG/specs/SIG-623) está en `feature/operation-authorization-by-team-f2@626585ca9`, contiene el head funcional `7cac00089` de Slice 1 y debe incorporar `fbf05159e` antes de continuar su entrega.
- **Evidencia de Slice 1:** commit `fbf05159e` en `feature/operation-authorization-by-team-f1`, sincronizado con `origin/develop@073f6a190` mediante el merge `9310ab7b5`; los cuatro tests afectados y `./gradlew check` pasaron, con `2` skips preexistentes. CI, cobertura, dependencias, análisis estático y workflow remoto terminaron correctamente. El feedback útil del review quedó aplicado sin mezclar la precondición legacy `systemId` con el autorizador transversal.
- **Pendiente operacional:** smoke ACME/Data Product no productivo; no se ejecutó por falta de credenciales apropiadas.
- **Persistencia acordada:** esta nota conserva la continuidad interna. En Spellbook, [SIG-621](https://spellbook.adminml.com/projects/SIG/specs/SIG-621) es la SPEC funcional padre y [SIG-622](https://spellbook.adminml.com/projects/SIG/specs/SIG-622) / [SIG-623](https://spellbook.adminml.com/projects/SIG/specs/SIG-623) son sus SPECs técnicas hijas.
- **Roadmap posterior a Actions:** las SPECs locales de Slice 3, 4 y 5 están creadas. Cada slice contiene sus propios tests, smoke, gate de datos y criterios de salida; no existe un gate final de pruebas separado. La publicación como hijas de SIG-621 está pendiente de reautenticar la CLI de Spellbook.
- Esta nota es la única fuente de verdad interna del proyecto: contiene baseline externo, decisiones del owner, evidencia del código, exclusiones y riesgos residuales.
- La SPEC SIG-616 de Spellbook se usa como requerimiento de origen aunque figure como `technical`. No se bloquea el avance por su clasificación: las nuevas SPECs explicitan su relación y los overrides deliberados.
- El ownership vive en `DataProduct.teamName`; los componentes pertenecen a un Data Product. La condición canónica de componente importado es una autorización de importación activa y aprobada, consultada mediante `ImportAuthorizationRepository.existsApprovedByImportedComponentId(componentId)`. `sourceComponentId` no sirve como discriminador porque también se completa en clones de migración v1→v2.
- La primera vertical se limita a Actions component-bound de Signals: `catalog-signal + start/stop`. Legacy, otras tecnologías, precreation, polling, deployments y otras mutaciones quedan fuera de esa entrega.
- El [PR 1126](https://github.com/melisource/fury_rio-playmaker/pull/1126) aporta la consulta ACME y casos de autorización para delete/inactivate; se refactorizará progresivamente para converger al mecanismo común, sin adoptar `PipelineAuthorizationService.assertAdminAccess` como contrato transversal definitivo.
- La primera implementación del autorizador común se extraerá desde ese comportamiento existente. Delete e inactivate serán consumidores de regresión con `DEPLOYER_AND_UP`; Actions Signals será el primer consumidor funcional nuevo con `DEV_AND_UP`.
- PR 1126 ya está mergeado en `origin/develop` (`1a4caf093`); la versión final valida el grant contra `teamName + projectCode`.
- ACME no puede precargarse correctamente sólo con el username: `/grants/user-grants/{username}` no informa el rol de `OwnerProjectGrant`. La verificación precisa requiere `username + teamName + Tiger headers` y luego match exacto de `projectCode`.
- Se definieron sólo dos niveles ACME: `DEV_AND_UP` con committer o superior y `DEPLOYER_AND_UP` con deployer o superior para delete/inactivate. `READ` no es una policy del autorizador: permanece Tiger-only en la frontera HTTP.
- Pipeline deploy está incluido; su ausencia en la lista original se considera un error documental. Las rutas enumeradas expresamente por SIG-616 se protegen aunque alguna esté marcada `@Deprecated`; el legacy no enumerado queda fuera y se identifica mediante allow-list explícita.

## 🧱 Entrega de desarrollo

%% Esta sección siempre queda disponible. En proyectos que cambian código, configuración ejecutable, schemas o infraestructura, es obligatoria: una fila por repo/branch, con SPEC funcional y técnica enlazadas antes de implementar. En proyectos no técnicos, reemplazar la tabla por `_No aplica — <motivo>._`. %%

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| `rio-playmaker` | `feature/operation-authorization-by-team-f1` | `origin/develop@073f6a190` sincronizada por merge | [SIG-621](https://spellbook.adminml.com/projects/SIG/specs/SIG-621), iniciativa derivada de [SIG-616](https://spellbook.adminml.com/projects/SIG/specs/SIG-616) | [SIG-622 — Slice 1](https://spellbook.adminml.com/projects/SIG/specs/SIG-622) | Implementado en `fbf05159e`; [PR #1169](https://github.com/melisource/fury_rio-playmaker/pull/1169) actualizado; smoke no productivo pendiente |
| `rio-playmaker` | `feature/operation-authorization-by-team-f2@626585ca9` | contiene `origin/feature/operation-authorization-by-team-f1@7cac00089` | [SIG-621](https://spellbook.adminml.com/projects/SIG/specs/SIG-621) | [SIG-623 — Slice 2](https://spellbook.adminml.com/projects/SIG/specs/SIG-623) | Rama existente; debe incorporar `fbf05159e` de Slice 1 antes de continuar su entrega |
| `rio-playmaker` | `feature/operation-authorization-by-team-f3@25a50c10c` | `feature/operation-authorization-by-team-f2@626585ca9` | [SIG-621](https://spellbook.adminml.com/projects/SIG/specs/SIG-621) | [[SPEC técnica — Slice 3 — Mutaciones y deployments de componentes]] | Implementado y publicado en [PR #1178](https://github.com/melisource/fury_rio-playmaker/pull/1178); gate de datos y smoke Tiger/ACME pendientes |
| `rio-playmaker` | `feature/operation-authorization-by-team-f4@cf4544b1a` | `origin/feature/operation-authorization-by-team-f3@1a8b4d972` | [SIG-621](https://spellbook.adminml.com/projects/SIG/specs/SIG-621) | [[SPEC técnica — Slice 4 — Relaciones y pipelines]] | Implementado localmente; listo para revisión técnica; coverage diferencial 100% line/branch; gates externos pendientes |
| `rio-playmaker` | Pendiente — rama de Slice 5 | Head aprobado de Slice 4 | [SIG-621](https://spellbook.adminml.com/projects/SIG/specs/SIG-621) | [[SPEC técnica — Slice 5 — Actions restantes]] | SPEC local creada; publicación Spellbook e implementación pendientes |

## 🧠 Diseño técnico consolidado

> [!info] Diseño listo para ejecución incremental
> SIG-621, SIG-622 y SIG-623 están creadas en Spellbook. Las SPECs locales de Slice 3, 4 y 5 están cerradas para publicación. Slice 1 ya está implementado en `feature/operation-authorization-by-team-f1`; la ejecución continúa con Slice 2 desde ese head.

### Fuentes y autoridad

| Fuente | Rol | Autoridad |
|---|---|---|
| [SIG-616 en Spellbook](https://spellbook.adminml.com/projects/SIG/specs/SIG-616) | Requerimiento de origen, escrito por terceros | Fuente funcional; sus omisiones o ambigüedades deben registrarse, no corregirse silenciosamente |
| Conversación y decisiones registradas en esta nota | Alcance y decisiones del proyecto | Fuente de verdad para el diseño acordado por el owner |
| `origin/develop` de `fury_rio-playmaker` | Comportamiento implementado | Evidencia técnica; base observada `1a4caf093` |
| [PR 1126](https://github.com/melisource/fury_rio-playmaker/pull/1126) | Implementación ACME existente | Base a refactorizar, no arquitectura transversal definitiva |

Esta separación es deliberada: un requerimiento de la SPEC, una decisión del proyecto y una inferencia del código no son equivalentes.

### Baseline funcional extraído de la SPEC externa

La SPEC exige autorización server-side para mutaciones y operaciones de componentes mediante identidad Tiger validada, ownership persistido y rol ACME. Define allow-list finita, clasificación server-side y default deny dentro de los casos protegidos.

Inventario funcional indicado por la SPEC:

- Crear, actualizar, eliminar y modificar diseño o metadatos de componentes.
- Crear, actualizar y eliminar relaciones.
- Crear/eliminar componentes de pipeline y modificar topología, diseño o relaciones.
- Provisionar, desprovisionar e inactivar.
- Ejecutar Actions mutantes sobre componentes de origen.
- Permitir read Actions declaradas con Tiger válido, sin exigir ACME.

Reglas transversales heredadas:

- `team-dev-and-up` equivale a `admin`, `maintainer`, `deployer`, `committer`.
- Los componentes importados no habilitan Actions mutantes; la importación no transfiere ownership.
- Una Action mutante de precreación se rechaza porque no existe un componente de origen persistido.
- Origen y destino de una relación deben pertenecer al mismo Data Product; cross-DP es inválido.
- `platformTeams` y `tempAllCanEdit` no conceden autorización bajo el nuevo guard.
- Tiger ausente/inválido, ownership faltante, rol insuficiente, ACME no verificable o recursos inconsistentes rechazan sin side effects.

Correcciones o decisiones del proyecto sobre la SPEC:

- La matriz general `team-dev-and-up` de la SPEC no reemplaza la política ya mergeada para delete/inactivate: esas dos operaciones conservan deliberadamente `DEPLOYER_AND_UP`. Es una excepción más restrictiva aprobada por el owner, no una contradicción pendiente.
- Pipeline deploy también está incluido aunque su ruta real fue omitida en el inventario original.
- Las Actions se clasifican por `component_type + actionName`; el nombre por sí solo no alcanza.
- Kafka/ClickHouse declaradas de lectura permanecen Tiger-only; no se agregará ACME por precaución local.
- Polling no recibe lógica nueva; cualquier contradicción preexistente se trata separadamente.
- Legacy se identifica y excluye explícitamente de la primera etapa.
- Primera vertical funcional: sólo `catalog-signal + start/stop` sobre componente persistido.

### Problema y frontera de responsabilidad

Tiger autentica al caller, pero no demuestra que pueda modificar un recurso cuyo dueño es otro equipo. La autorización necesita combinar:

- Username validado por Tiger.
- Ownership persistido en Playmaker: `DataProduct.teamName + DataProduct.projectCode`.
- Rol retornado por ACME para ese usuario y equipo.
- Nivel exigido por la operación.

Playmaker es el enforcement point. Los handlers y Control Planes no consultarán Tiger ni ACME. Toda denegación debe ocurrir antes de locks, persistencia, KVS, BigQueue o llamadas externas.

### Principios

- **KISS:** una clase concreta de autorización, sin pareja `interface/impl`.
- **YAGNI:** sin motor de policies, Aspects, annotations ni legacy en la primera entrega.
- **SOLID pragmático:** Tiger autentica; el caso de uso resuelve el target; el autorizador encapsula ACME y roles.
- **Default deny dentro del alcance:** una Action desconocida de Signals no se presume de lectura.
- **Fuente persistida:** tipo, ownership e importación salen de Playmaker, no del request.
- **Evolución por consumidores reales:** primero se extrae el comportamiento existente; después se agregan nuevas operaciones.

### Alcance incremental

| Etapa | Alcance | Cambio funcional |
|---|---|---|
| Slice 1 | Extraer autorizador desde PR 1126 y migrar delete/inactivate | Ninguno: refactor compatible de la política existente |
| Slice 2 | Corregir principal Tiger e integrar `catalog-signal + start/stop` | Sólo Signals agrega una restricción nueva |
| Slice 3 | Mutaciones y deployments de componentes | `DEV_AND_UP` en todas las rutas enumeradas; tests y rollout en el mismo PR |
| Slice 4 | Relaciones y pipelines, incluido pipeline deploy | `DEV_AND_UP`, same-DP y tests/rollout en el mismo PR |
| Slice 5 | Actions restantes de Flink, ClickHouse y lecturas allow-listed | Whitelist completa, default deny y tests/rollout en el mismo PR |

### Niveles ACME

| Nivel | Roles | Uso |
|---|---|---|
| `DEV_AND_UP` | `admin`, `maintainer`, `deployer`, `committer` | Escrituras SIG-616, incluido Signals `start/stop` |
| `DEPLOYER_AND_UP` | `admin`, `maintainer`, `deployer` | Delete e inactivate provenientes del PR 1126 |

Las Actions de lectura quedan fuera del autorizador común y continúan protegidas sólo por Tiger. No se agregarán más niveles sin un caso funcional nuevo.

### Actions: clasificación inicial

La whitelist se define mediante el par `component_type + actionName`, nunca sólo por nombre:

| Tipo persistido | Action | Clasificación | Requisito |
|---|---|---|---|
| `catalog-signal` | `start` | Mutación operacional | Tiger + `DEV_AND_UP` |
| `catalog-signal` | `stop` | Mutación operacional | Tiger + `DEV_AND_UP` |

Reglas asociadas:

- Una Action desconocida sobre `catalog-signal` se rechaza.
- Otros tipos conservan el comportamiento actual hasta que una SPEC los incorpore.
- Kafka y ClickHouse read Actions siguen Tiger-only, tal como indica la SPEC.
- Un componente importado según `ImportAuthorizationRepository.existsApprovedByImportedComponentId(componentId)` no puede ejecutar una Action mutante. No se usa `sourceComponentId` para esta decisión.
- Precreation queda fuera; `catalog-signal + start/stop` sin componente persistido debe terminar rechazado.
- Polling no obtiene una política nueva, no cambia `ActionKvsEntry` y no agrega `resultVisibility`.

Inventario técnico observado para evitar clasificar sólo por nombre:

- Signals: `catalog-signal + start/stop`.
- Kafka: `aws-msk-topic`, `gcp-kafka-topic` y el tipo transicional `kafka-topic` con `peek` de lectura.
- Flink: `start/stop` sobre sus tipos configurados; fuera de la primera vertical.
- ClickHouse: `clickhouse-mat-view + start-materialized-view/stop-materialized-view`; lecturas `execute-query`, `describe-table`, `list-warehouse`, su alias legacy aún consumido `list-warehouses-for-team`, `list-database`, `list-tables` y `ping`. Slice 5 excluye `ping` por no estar declarado en SIG-616 y exige medir su uso antes del rollout.

La reutilización de nombres como `start/stop` entre tecnologías demuestra que `actionName` solo no es una clave de política segura. Los ejemplos prefijados de la SPEC no deben copiarse sin contrastarlos con los contratos reales.

### Estado objetivo de Tiger

`CustomAuthorizationFilter` ya valida Tiger, pero hoy guarda el token crudo como principal y los services vuelven a resolver el username. El objetivo incremental es:

- Validar Tiger una sola vez.
- Publicar el username como principal en `SecurityContext`.
- No registrar ni exponer el token crudo.
- Eliminar del filtro la allow-list duplicada de rutas. Con Bearer válido publica username; con token ausente, malformado, inválido o expirado continúa sin Authentication. `SecurityConfig` queda como única fuente de verdad: `permitAll` continúa y `.authenticated()` responde `401` mediante un `AuthenticationEntryPoint` explícito.
- Migrar sólo los call sites tocados por cada vertical; no hacer una migración masiva de los 67 usos observados.

Evidencia actual en `origin/develop`:

- `CustomAuthorizationFilter` llama `TigerTokenService.getAuthToken`, descarta el username y guarda el Bearer token como principal.
- El filtro duplica las rutas públicas declaradas en `SecurityConfig`.
- Un token inválido se transforma en `ServletException`; debe comprobarse el status HTTP real fuera de `ControllerExceptionHandler`.
- Existe una rama que registra el token crudo al fallar validación.
- `ActionServiceImpl` vuelve a llamar Tiger en component-bound, precreation y polling.
- No se observaron consumidores productivos actuales del `SecurityContext` fuera del filtro.

### Por qué ACME no es middleware

El cliente actual expone:

```java
getUserGrants(username, headers)
getOwnerProjectGrants(username, teamName, headers)
```

El commit `7737f053d` documenta que `/grants/user-grants/{username}` no incluye el rol de `OwnerProjectGrant`. Por tanto, no permite precargar todos los permisos útiles usando sólo el username.

La consulta precisa requiere `username + teamName + Tiger headers`. ACME no recibe `projectCode`; el autorizador debe comparar localmente que el grant corresponda exactamente a `teamName + projectCode`.

Consecuencia: sólo Tiger es middleware. ACME se consulta después de que el caso de uso resuelve el target persistido.

El PR 1126 está mergeado en `origin/develop` mediante `1a4caf093`. Sus dos call sites productivos son `PipelineComponentDeleteServiceImpl` y `ComponentInactivationServiceImpl`, ambos a través de `PipelineAuthorizationService.assertAdminAccess` y `AuthorizationUtils.requireDeployerOrAbove`.

### Autorizador común

Se creará una única clase concreta, provisionalmente `OperationAuthorizationService`, que:

- Reutiliza `AcmeClient.getOwnerProjectGrants`.
- Recibe caller, `teamName`, `projectCode`, headers Tiger y nivel requerido.
- Valida scope completo y match exacto de proyecto.
- Mantiene centralizadas las listas de roles.
- Falla cerrado ante falta de permiso o imposibilidad de verificar ACME y preserva el `403` observable de los consumidores actuales. Diferenciar indisponibilidad con `5xx` queda fuera de estos slices.
- Realiza una sola invocación lógica a `AcmeClient.getOwnerProjectGrants` por `require`; la paginación y sus HTTP GET internos permanecen encapsulados en el cliente.
- No conoce Actions, componentes, pipelines ni controllers.

Contrato conceptual:

```java
authorizationService.require(
    username,
    teamName,
    projectCode,
    DEV_AND_UP,
    headers);
```

No habrá un autorizador por nivel ni una interfaz con una sola implementación.

### Primeros consumidores

La validación mergeada actualmente sigue este camino:

```text
PipelineAuthorizationService.assertAdminAccess
    → AuthorizationUtils.requireDeployerOrAbove
    → AcmeClient.getOwnerProjectGrants
```

Se refactorizará así:

1. Extraer la política a `OperationAuthorizationService`.
2. Migrar `PipelineComponentDeleteServiceImpl` con `DEPLOYER_AND_UP`.
3. Migrar `ComponentInactivationServiceImpl` con `DEPLOYER_AND_UP`.
4. Incorporar `ActionServiceImpl` como primer consumidor funcional nuevo con `DEV_AND_UP`.

`PipelineAuthorizationService.assertWriteAccess` y otros helpers con consumidores distintos no se eliminan por arrastre. `AuthorizationUtils.requireDeployerOrAbove` puede retirarse cuando no tenga consumidores productivos.

### Flujo de Signals

```text
[MODIFIED] Tiger filter
    → valida una vez y publica username
[MODIFIED] ActionController + ActionResultController
    → pasan el username de Authentication; no aceptan identidad cliente
[MODIFIED] ActionServiceImpl
    → resuelve DP + componente + environment
    → clasifica tipo + Action
    → rechaza importados
[NEW] OperationAuthorizationService
    → consulta owner-project por username + team
    → valida projectCode + DEV_AND_UP
[MODIFIED] ActionServiceImpl
    → sólo tras allow carga deployment, guarda KVS y publica
[UNCHANGED] Signals Control Plane
```

El ownership no vive en `ServiceModel`; vive en `DataProductModel`. `ActionServiceImpl.fetchComponentInHierarchy` ya valida que Data Product, componente y environment pertenezcan a la misma jerarquía. `teamName` o `projectCode` incompletos en una operación moderna protegida producen rechazo fail-closed.

### Errores

| Condición | Respuesta esperada |
|---|---|
| Tiger ausente o inválido | `401 Unauthorized` |
| Recurso persistido inexistente | `404 Not Found` |
| Scope dueño incompleto | Rechazo fail-closed; semántica exacta en SPEC técnica |
| Rol insuficiente para team + project | `403 Forbidden` |
| Signals desconocida o importada | `403 Forbidden` |
| ACME no disponible/no verificable | `403 Forbidden` en estos slices para preservar compatibilidad; una diferenciación `5xx` requiere cambio posterior explícito |

Ningún mensaje expone miembros del equipo, grants, tokens o detalles internos de ACME.

El `403` no afirma que una indisponibilidad sea idéntica a falta de rol; es una decisión incremental para no cambiar el contrato observable mientras se extrae el autorizador. Logs y métricas internas deben distinguir ambas causas sin filtrar grants ni identidad sensible.

### Rutas y flujos posteriores ya identificados

- Component deploy moderno: `POST /data-products/{dataProductId}/components/{componentId}/environments/{environmentId}/deployments`.
- Component undeploy moderno: `DELETE .../deployments/{deploymentId}`.
- Pipeline deploy: `POST /data-products/{name}/environments/{envName}/pipeline/deploy`; su omisión en la SPEC original es un error documental.
- El deploy de pipeline puede calcular deltas `DEPLOY` y `UNDEPLOY`; se autoriza una vez antes del cálculo y los efectos.
- Relaciones deben comprobar que origen y destino pertenezcan al mismo Data Product; los IDs en body requieren tratamiento propio.
- `/services/{serviceId}/actions/**` y rutas `@Deprecated` reemplazadas por RFC-002 quedan fuera de la primera etapa. En particular, `POST /services/{serviceId}/actions/code` es mutante, sigue activo y constituye un riesgo residual explícito que necesitará una SPEC posterior; no se lo trata como lectura ni se asume deprecated.
- Legacy se excluye por allow-list explícita de entrypoints modernos, no porque falte ownership.
- `tempAllCanEdit` fue localizado en `QueryServiceImpl`; no participa en los flujos de estos dos slices y no concede autorización en futuras integraciones.

### Estrategia de pruebas

Primero se cubren los caminos críticos y luego al menos 95% del código nuevo.

- En rutas `.authenticated()`, Tiger válido publica username y token ausente/inválido/expirado retorna `401`; el token no aparece en logs.
- Rutas `permitAll` continúan sin token, con Bearer válido y con Bearer inválido/expirado; el filtro no mantiene paths públicos.
- Delete e inactivate conservan `DEPLOYER_AND_UP`: admin/maintainer/deployer permiten; committer y roles inferiores rechazan.
- Signals `start/stop` permiten con `DEV_AND_UP`; Action desconocida e importado rechazan. Tipo y Action se comparan por igualdad exacta, case-sensitive y sin trim/aliases.
- Grant de otro team o proyecto no habilita.
- `AcmeClientImpl` se valida con fixture contractual representativo de `owner-project`; la convención real de `projectCode` se confirma con smoke no productivo, nunca haciendo depender CI de ACME.
- Rol insuficiente y ACME no verificable retornan `403`; observabilidad interna diferencia la causa.
- Deny/error no guarda `ActionKvsEntry` ni publica BigQueue.
- Allow guarda y publica exactamente una vez.
- Kafka, Flink, ClickHouse, polling, callbacks y legacy no cambian ni consultan ACME en esta etapa. Precreation no consulta ACME, pero debe rechazar explícitamente `catalog-signal + start/stop` para no abrir un bypass sin componente persistido.

### Slices de implementación

El proyecto se ejecuta como **un gate documental y cinco slices de código**. Tests, observabilidad, smoke, gate de datos y ausencia de side effects son parte del PR de cada slice; no existe una entrega o gate final de pruebas.

#### Gate 0 — SPECs técnicas y tasks locales

Sin cambios de código. Se crea y revisa una SPEC técnica por slice, se derivan sus tasks dentro del documento y se fija como base el head aprobado de la entrega anterior.

#### Slice 1 — Extraer el autorizador usando los consumidores existentes

Objetivo: obtener una base transversal probada sin agregar una restricción funcional nueva.

- Crear una sola clase concreta de autorización.
- Reutilizar `AcmeClient.getOwnerProjectGrants`.
- Centralizar `DEV_AND_UP` y `DEPLOYER_AND_UP` en un enum pequeño consumido por una clase concreta, sin estrategias ni interfaces.
- Migrar delete e inactivate con `DEPLOYER_AND_UP`.
- Retirar `AuthorizationUtils.requireDeployerOrAbove` al quedar sin consumidores.
- Mantener `PipelineAuthorizationService.assertWriteAccess` y helpers no relacionados.
- Preservar la matriz allow/deny y el `403` existente ante ACME no verificable.
- Probar team/proyecto incorrectos, todos los roles, ACME fallido y ausencia de efectos.

Gate de salida: los dos consumidores existentes usan la misma implementación y no existe regresión funcional accidental.

#### Slice 2 — Actions mutantes de Signals end-to-end

Objetivo: incorporar el primer comportamiento nuevo de SIG-616.

- Publicar username desde Tiger en `SecurityContext` sin exponer el token.
- Hacer que Actions consuma la identidad validada sin volver a invocar Tiger.
- Clasificar por estado persistido `catalog-signal + start/stop`.
- Rechazar Action Signals desconocida, componente importado según autorización de importación aprobada y scope incompleto.
- Invocar el autorizador con `DEV_AND_UP` después de resolver la jerarquía y antes de contexto de deployment, KVS o BigQueue.
- Mantener Kafka, Flink, ClickHouse, polling, callbacks y legacy sin cambios ni llamadas ACME.
- En precreation, rechazar `catalog-signal + start/stop` sin consultar ACME, porque no existe target persistido que autorizar.
- Agregar pruebas unitarias e integración para allow/deny/error y cero side effects.

Gate de salida: Signals queda protegido end-to-end y todo lo fuera de alcance conserva su comportamiento.

#### Slice 3 — Mutaciones y deployments de componentes

Objetivo: integrar `DEV_AND_UP` en las cinco mutaciones de `ComponentController` y en component deploy/undeploy, usando el principal Tiger validado y la jerarquía persistida antes de cualquier efecto lateral.

La implementación, tests, gate de datos, smoke no productivo y evidencia de coverage viven en [[SPEC técnica — Slice 3 — Mutaciones y deployments de componentes]] y se entregan en un único PR.

#### Slice 4 — Relaciones y pipelines

Objetivo: proteger create/update/delete de relaciones con same-DP y owner persistido, y migrar PUT/design/relations/component-create/pipeline-deploy al autorizador común con `DEV_AND_UP`.

La implementación, tests cross-DP, verificación de cero side effects, gate de datos, smoke y coverage viven en [[SPEC técnica — Slice 4 — Relaciones y pipelines]] y se entregan en un único PR.

#### Slice 5 — Actions restantes

Objetivo: completar la whitelist exacta `component_type + actionName` para Flink, ClickHouse y las lecturas declaradas por SIG-616, exigir origin + `DEV_AND_UP` en mutaciones y aplicar default deny a todo par desconocido.

La matriz parametrizada, integración HTTP, inventario de pares, smoke y coverage viven en [[SPEC técnica — Slice 5 — Actions restantes]] y se entregan en un único PR.

### Descomposición de Slice 1 y Slice 2

| Orden | Task conceptual | Gate de término |
|---|---|---|
| T-01 | Corregir principal Tiger y respuesta `401` | Username como principal, token fuera de logs, tests de seguridad verdes |
| T-02 | Extraer autorizador y migrar delete/inactivate | Una implementación; comportamiento `DEPLOYER_AND_UP` intacto |
| T-03 | Implementar whitelist Signals | Sólo `catalog-signal + start/stop` usa `DEV_AND_UP` |
| T-04 | Integrar Actions antes de side effects | Sin llamadas directas a Tiger/ACME ni efectos al rechazar |
| T-05 | Verificar exclusiones y regresión | Tecnologías/rutas fuera de alcance no cambian |
| T-06 | Observabilidad y error mapping | `401/403/404` estables; causas ACME distinguibles internamente sin datos sensibles |

Las tasks definitivas viven en cada SPEC local y se materializarán recién al comenzar la implementación.

### Gates pendientes

- [x] Tratar SIG-616 como requerimiento de origen aunque figure como técnica; relacionar las nuevas SPECs sin bloquear por clasificación.
- [x] Confirmar `catalog-signal + start/stop` y `DEV_AND_UP`.
- [x] Componentes importados: Action mutante denegada; la importación no transfiere ownership.
- [x] Precreation: `catalog-signal + start/stop` no se habilita sin componente persistido.
- [x] Polling no recibe policy nueva ni llamadas ACME en estos slices.
- [x] Confirmar PR 1126 mergeado en `origin/develop` (`1a4caf093`).
- [x] Confirmar contrato ACME: `username + teamName + headers`; `projectCode` se valida localmente.
- [x] Preservar `403` ante ACME no verificable en estos slices; evaluar `5xx` como mejora posterior.
- [x] La SPEC de Slice 2 fija `401` como estado objetivo de Tiger y exige una prueba de integración; el status actual exacto no bloquea el diseño.
- [x] Definir branch/base limpias después de aprobar SPEC y tasks.

### Prompt maestro de validación independiente

```text
Actúa como Principal/Staff Backend Engineer y revisor independiente de seguridad y Specification-Driven Development. Necesito que audites el proyecto SIG-616 de autorización de operaciones por equipo en rio-playmaker. No implementes código, no edites Spellbook y no modifiques la nota durante la primera revisión: entrega hallazgos basados en evidencia.

Fuentes obligatorias, en este orden:

1. SPEC externa (no fue escrita por el owner de este proyecto):
   https://spellbook.adminml.com/projects/SIG/specs/SIG-616
2. Proyecto y diseño consolidado, única fuente interna de decisiones:
   /Users/rjara/obsidian/SecondBrain/main/10-projects/Meli/SIG-616 — Autorización de operaciones por equipo/SIG-616 — Autorización de operaciones por equipo.md
3. Repositorio:
   /Users/rjara/fuentes/rio-playmaker
4. PR ya mergeado que debe reutilizarse/refactorizarse:
   https://github.com/melisource/fury_rio-playmaker/pull/1126
5. Base técnica a inspeccionar:
   origin/develop, merge observado 1a4caf093.

No confíes en el checkout actual como base limpia: puede contener cambios de otro trabajo. Usa lecturas de origin/develop o un mecanismo no destructivo. No borres, resetees ni sobrescribas cambios locales.

Objetivo de la auditoría:

Validar la trazabilidad completa desde la SPEC externa hasta el diseño y los slices propuestos. Determina si el diseño es correcto, seguro, KISS, YAGNI, SOLID pragmático, modular y escalable sin esconder autorización en controllers o Control Planes.

Comprueba directamente en SPEC, PR, historial y código; no aceptes estas afirmaciones sin evidencia:

- Qué mutaciones, deployments, undeploy, inactivate, relaciones, pipelines y Actions exige proteger la SPEC.
- Qué Actions son de lectura y por qué permanecen Tiger-only.
- Si pipeline deploy fue omitido documentalmente pero comparte la misma semántica mutante.
- Reglas para componentes importados, precreation, cross-DP, platformTeams y tempAllCanEdit.
- Contratos reales de Actions: el clasificador debe usar component_type + actionName.
- Rutas modernas y legacy reales; identifica bypasses posibles sin ampliar silenciosamente el alcance.
- Contrato real de ACME: parámetros de getUserGrants y getOwnerProjectGrants, forma del payload, paginación, roles y filtro de projectCode.
- Confirma o refuta que getUserGrants(username) no entrega roles OwnerProjectGrant suficientes.
- Confirma que getOwnerProjectGrants recibe username + teamName + Tiger headers, pero no projectCode.
- Confirma que teamName y projectCode vienen del DataProduct persistido y revisa registros modernos con ownership incompleto.
- Estado real de CustomAuthorizationFilter, SecurityConfig, SecurityContext, duplicación de validación Tiger, logs de token y respuesta HTTP ante fallo.
- Detección canónica de componentes importados: intenta refutar expresamente el uso de `sourceComponentId` contrastándolo con migraciones v1→v2 y `ImportAuthorizationRepository.existsApprovedByImportedComponentId`.
- Todos los call sites productivos de PipelineAuthorizationService.assertAdminAccess y AuthorizationUtils.requireDeployerOrAbove.
- Orden exacto de resolución, consulta ACME y side effects en delete, inactivate y ActionServiceImpl.
- Status HTTP actual cuando ACME falla y compatibilidad de preservar `403` en estos slices, dejando una eventual diferenciación `5xx` fuera de alcance.

Evalúa especialmente esta arquitectura propuesta:

- Sólo Tiger es middleware y publica username en SecurityContext cuando el Bearer es válido; `SecurityConfig`, no el filtro, gobierna `permitAll` y el `401` de rutas autenticadas.
- ACME no es middleware porque la consulta precisa requiere conocer teamName.
- Existe una sola clase concreta OperationAuthorizationService, sin interface/impl ni estrategias prematuras.
- El autorizador recibe caller, teamName, projectCode, headers y nivel; encapsula AcmeClient, roles y errores.
- Delete e inactivate son los primeros consumidores de regresión con DEPLOYER_AND_UP.
- ActionServiceImpl es el primer consumidor funcional nuevo con DEV_AND_UP.
- Signals sólo protege catalog-signal + start/stop, rechaza combinaciones desconocidas e importados detectados mediante una autorización de importación activa/aprobada y valida antes de deployment context, KVS y BigQueue.
- Read Actions, polling, otras tecnologías y legacy no cambian en la primera entrega. Precreation no consulta ACME, pero rechaza el mismo par `catalog-signal + start/stop` antes de KVS/BigQueue para cerrar ese bypass mínimo.
- @RequiresCapability queda documentada como evolución futura, no implementación actual.

Busca problemas de seguridad, TOCTOU, ownership incorrecto, queries duplicadas, dependencias HTTP filtradas al dominio, fallos fail-open, inconsistencias de status, bypass por rutas alternativas, ruptura de tests y abstracciones innecesarias. Distingue siempre entre:

A. Requerimiento textual de la SPEC.
B. Decisión explícita del owner registrada en el proyecto.
C. Hecho comprobado en el código o PR.
D. Inferencia o propuesta pendiente.

Formato obligatorio de salida:

1. Veredicto: GO, GO WITH CHANGES o NO-GO para crear la SPEC técnica.
2. Resumen ejecutivo de máximo 10 puntos.
3. Matriz de trazabilidad: requisito/decisión → evidencia → componente propuesto → test → estado.
4. Hallazgos ordenados por severidad P0-P3, cada uno con evidencia exacta (archivo y línea, commit o sección de SPEC), impacto y corrección mínima.
5. Contradicciones entre SPEC, proyecto y código.
6. Evaluación de los dos slices: independencia, riesgo, criterio de salida y si el orden es correcto.
7. Decisiones faltantes que bloquean la SPEC técnica; no conviertas preferencias menores en blockers.
8. Cambios textuales concretos recomendados para la nota del proyecto, sin aplicarlos.
9. Lista final de afirmaciones verificadas y afirmaciones que no pudiste verificar.

Reglas de calidad:

- No inventes contratos ACME ni comportamiento de Spellbook.
- Si una fuente no está accesible, decláralo y reduce la confianza del hallazgo.
- Prioriza fuentes primarias y código real sobre comentarios secundarios.
- No propongas microservicios, frameworks de policies, interfaces de una sola implementación, annotations o generalizaciones sin consumidores reales.
- No confundas autenticación, obtención de grants y decisión de autorización.
- No apruebes el diseño sólo porque parece razonable: intenta refutarlo.
```

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
> - [x] Pulir el diseño consolidado y cerrar los gates de Actions Signals #owner/me #type/research #area/meli
> - [x] Ejecutar validación independiente del diseño y resolver hallazgos #owner/me #type/research #area/meli
> - [x] Definir la relación con SIG-616: requerimiento de origen, sin bloquear por su clasificación técnica #owner/me #type/dev #area/meli
> - [x] Crear y revisar la SPEC técnica local de Slice 1 — autorizador común #owner/me #type/dev #area/meli
> - [x] Crear y revisar la SPEC técnica local de Slice 2 — Actions mutantes de Signals #owner/me #type/dev #area/meli
> - [x] Derivar y acordar las tasks ejecutables dentro de ambas SPECs locales #owner/me #type/dev #area/meli
> - [x] Crear SIG-621 y colgar SIG-622 / SIG-623 como SPECs técnicas hijas #owner/me #type/admin #area/meli
> - [r] Definir branch/base limpias e implementar SIG-622 — implementado y listo para revisión; smoke no productivo pendiente #owner/me #type/dev #area/meli
> - [ ] Incorporar `origin/feature/operation-authorization-by-team-f1@fbf05159e` en `feature/operation-authorization-by-team-f2` y continuar SIG-623 sin rehacer Slice 1 #owner/me #type/dev #area/meli
> - [x] Crear la SPEC técnica local de Slice 3 — mutaciones y deployments de componentes #owner/me #type/dev #area/meli
> - [x] Crear la SPEC técnica local de Slice 4 — relaciones y pipelines #owner/me #type/dev #area/meli
> - [x] Crear la SPEC técnica local de Slice 5 — Actions restantes #owner/me #type/dev #area/meli
> - [ ] Publicar Slice 3, 4 y 5 como SPECs técnicas hijas de SIG-621 en Spellbook; la CLI requiere reautenticación #owner/me #type/admin #area/meli #blocked

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
- **2026-09-14** — Se revisó SIG-616 y el código de Playmaker. Se acordó iniciar por el diseño de autorización reusable antes de tocar rutas o control planes.
- **2026-09-14** — Se acotó la primera vertical a `catalog-signal + start/stop`; se evaluó y luego descartó un interceptor ACME al comprobar que el grant preciso requiere conocer el team. Se excluyeron legacy/precreation/polling y se documentó el refactor evolutivo del PR 1126.
- **2026-09-14** — Se cerraron los niveles `READ`, `DEV_AND_UP` y `DEPLOYER_AND_UP`; se confirmó PR 1126 mergeado, se incorporó pipeline deploy y se definió legacy por entrypoints `@Deprecated`/RFC-002.
- **2026-09-14** — Se verificó el contrato ACME: `getUserGrants(username)` no contiene roles `OwnerProjectGrant`; se descartó ACME como middleware y la consulta precisa quedó en un autorizador reutilizable llamado desde el caso de uso tras resolver `teamName + projectCode`.
- **2026-09-14** — Se acordó una sola implementación concreta del autorizador: se extrae desde delete/inactivate sin cambiar su política y luego se incorpora Actions Signals como primer caso nuevo.
- **2026-09-14** — Se consolidó en esta única nota el baseline de la SPEC, evidencia técnica, arquitectura, dos slices, pruebas, gates y prompt de validación independiente.
- **2026-09-14** — La revisión cruzada corrigió un supuesto crítico: `sourceComponentId` también existe en clones de migración y no identifica importación. Se adoptó `ImportAuthorizationRepository.existsApprovedByImportedComponentId`, se fijó compatibilidad `403` para fallos ACME, `401` como objetivo Tiger comprobable por integración y el rechazo mínimo de Signals mutante en precreation.
- **2026-09-14** — Se redactaron y corrigieron las dos SPECs técnicas. El revisor cerró con `AGREED`. Por decisión del owner se mantienen sólo en el vault; no se creó ni editó ninguna SPEC en Spellbook.
- **2026-09-14** — Una segunda revisión detectó el caso `permitAll + Bearer inválido`. Se eliminó la duplicación de paths en el filtro y se dejó la decisión de acceso a `SecurityConfig`. Se rechazaron tests automatizados contra ACME real: se acordaron fixture contractual determinista + smoke no productivo. El revisor respondió `AGREED`.
- **2026-09-14** — Por instrucción posterior del owner se creó [SIG-621](https://spellbook.adminml.com/projects/SIG/specs/SIG-621) como SPEC funcional padre y se publicaron [SIG-622](https://spellbook.adminml.com/projects/SIG/specs/SIG-622) y [SIG-623](https://spellbook.adminml.com/projects/SIG/specs/SIG-623) como SPECs técnicas hijas, todas en Draft y sin cambios de alcance.
- **2026-09-15** — Se implementó SIG-622 en `rio-playmaker` desde `origin/develop@1a4caf093`, en el worktree aislado `rio-playmaker-sig-622`. Se creó `OperationAuthorizationService`, se migraron exclusivamente delete/inactivate con `DEPLOYER_AND_UP`, se retiraron los helpers obsoletos solicitados y se preservaron `systemId`, orden, guards, side effects y `403`.
- **2026-09-15** — Se corrigió el finding de observabilidad: las denegaciones registran el `access_level` y los errores de ACME sólo el `exception_type`, sin datos sensibles. La suite completa quedó verde; el commit `1abadb005` fue publicado en `feature/operation-authorization-by-team-f1`. SIG-623 no fue implementado; queda pendiente el smoke ACME/Data Product no productivo.
- **2026-09-15** — Se creó [PR #1169](https://github.com/melisource/fury_rio-playmaker/pull/1169) con la descripción basada en el template del repo, se sincronizó la rama con `origin/develop@e02b2b09f` mediante el merge `5d9ed7f0f` y se dejó listo para revisión. La suite local sobre ese head reportó 3.785 tests, 0 fallas y 0 errores; CI remoto quedó en curso. Zord estándar se ejecutó; su revisor transversal RIO falló al iniciar y no publicó comentarios.
- **2026-09-15** — Se restauró el contrato previo de `no owning team` para `teamName` o `projectCode` ausentes y se preservó la causa de excepciones ACME en `SecurityException`; commit `7fbb7efcf` publicado. La suite focalizada de 60 tests pasó sin fallas ni errores.
- **2026-09-15** — Se fijó la continuidad de implementación: Slice 2 / SIG-623 debe comenzar desde `origin/feature/operation-authorization-by-team-f1@7fbb7efcf`. No debe partir desde `develop`, cherry-pickear parcialmente ni recrear el autorizador de Slice 1.
- **2026-09-15** — Se cubrieron las ramas faltantes de ownership/ACME en `a367b6690` y se aplicó el feedback del PR en `b71b6bec6`: precondición compartida sin incorporar `systemId` al autorizador transversal, `cause` ACME preservada internamente y protegida por un test HTTP contra filtración anidada, y logs de denegación con team/project sin username ni tokens. Suite completa: 3.788 tests, 0 fallas y 2 skips preexistentes.
- **2026-09-15** — Se sincronizó la rama con `origin/develop@a78db6ede` mediante el merge `e5b1ab7c8`, se repitió la suite completa con 3.830 tests, 0 fallas y 2 skips, se publicó el head y se respondieron los cuatro comentarios de review con la evidencia de su aplicación. CI, cobertura, dependencias y workflow terminaron en verde; quedan aprobación humana y smoke no productivo.
- **2026-09-15** — Se corrigió el contrato de falla ACME en `7cac00089`: `OperationAuthorizationService` vuelve a descartar la excepción interna, el unit test exige `cause == null` y se retiró el test HTTP agregado para una causa que ya no existe. Suite completa: 3.829 tests, 0 fallas y 2 skips; la respuesta del review y la descripción del PR se actualizaron en consecuencia.
- **2026-09-15** — Se crearon las SPECs técnicas locales de Slice 3, 4 y 5. Cada entrega incorpora su propia matriz de tests, gate de datos, smoke no productivo y coverage; se descartó un gate final separado. La publicación en Spellbook quedó pendiente porque la sesión de la CLI expiró.
- **2026-09-15** — La revisión cruzada de Slice 5 confirmó `list-warehouses-for-team` en el contrato de CP ClickHouse y en un consumidor activo de rio-frontend; se mantuvo como alias legacy explícito. También se convirtió `ping` en un check nominal del gate de inventario previo al rollout.
- **2026-09-16** — Se evaluaron los cuatro comentarios nuevos del PR #1169 contra el código y la SPEC. Se aplicaron las mejoras de helpers estáticos y estructura de tests en `fbf05159e`: matriz de roles parametrizada, `@InjectMocks`, `assertNull` y ownership centralizado en `AuthorizationUtilsTest`, conservando un smoke por consumidor con mensaje y orden. No se aplicó la propuesta de unir `requireOperationOwnership` con `OperationAuthorizationService.require` porque `systemId` es una precondición legacy exclusiva de delete/inactivate y no forma parte del contrato transversal. Los tests focalizados, `./gradlew check` y todos los checks remotos materiales pasaron; las cuatro respuestas cordiales se publicaron y verificaron en GitHub.

## 🧭 Decisiones

- **D1 — Primer cambio funcional sólo Signals.** La primera restricción nueva protege `catalog-signal + start/stop` sobre componentes existentes; el refactor previo de delete/inactivate no cambia su política. No incluye legacy, otras tecnologías ni polling. En precreation sólo se rechaza ese mismo par para cerrar el bypass, sin consulta ACME ni policy general nueva.
- **D2 — Sólo Tiger es middleware.** Tiger se valida una vez en la frontera HTTP y publica el username. ACME se consulta desde un autorizador reutilizable cuando el caso de uso ya conoce el scope persistido.
- **D3 — Whitelist de tipo + Action.** Una Action desconocida sobre `catalog-signal` se rechaza; tecnologías fuera del alcance conservan su comportamiento hasta contar con SPEC propia.
- **D4 — Services consumidores con una sola validación.** Actions resuelve el target y llama una vez a un autorizador concreto con caller, `teamName`, `projectCode` y nivel antes de cualquier side effect; no consume `AcmeClient` ni implementa listas o parsing de roles.
- **D5 — PR 1126 converge por refactor.** Se reutiliza `AcmeClient.getOwnerProjectGrants`; la API acoplada a pipeline y la política estática se refactorizan a medida que se incorporan casos reales.
- **D6 — Annotation al final, no ahora.** `@RequiresCapability` se evaluará sobre services cuando exista repetición comprobada; queda documentada como evolución final y fuera de alcance inicial.
- **D7 — Playmaker es el enforcement point.** Los CPs siguen procesando eventos defensivamente, pero no resuelven Tiger ni ACME; reciben sólo requests ya autorizados por Playmaker.
- **D8 — SPECs y tasks antes de código.** Se cierra diseño, se valida el requerimiento de origen y se acuerda una SPEC por vertical con sus tasks antes de definir branch/base e implementar.
- **D9 — Dos niveles ACME cerrados.** `DEV_AND_UP` y `DEPLOYER_AND_UP`; delete/inactivate conservan los tres roles del PR 1126 y el resto de escrituras SIG-616 usa los cuatro roles dev+. `READ` queda Tiger-only fuera del autorizador.
- **D10 — Pipeline deploy incluido y legacy explícito.** La ruta moderna de pipeline deploy debe incorporarse a la SPEC. Toda ruta enumerada expresamente por SIG-616 se protege aunque esté marcada `@Deprecated`; las rutas legacy no enumeradas quedan fuera.
- **D11 — ACME preciso, no precarga incompleta.** No se usa `getUserGrants(username)` para permisos por proyecto. El autorizador reutiliza `getOwnerProjectGrants(username, teamName, headers)` y valida el `projectCode` persistido.
- **D12 — Una implementación, consumidores incrementales.** No habrá `interface/impl` ni un autorizador por nivel. Delete e inactivate migran primero como regresión; Signals consume la misma clase con otra política.
- **D13 — Importación por evidencia canónica.** Una Action mutante se considera importada sólo cuando `ImportAuthorizationRepository.existsApprovedByImportedComponentId(componentId)` lo confirma; `sourceComponentId` no decide porque también representa linaje de migración.
- **D14 — Compatibilidad de errores ACME.** Rol insuficiente y ACME no verificable fallan cerrado con `403` en estos slices. Se distinguen mediante observabilidad interna; migrar indisponibilidad a `5xx` requiere una decisión futura explícita.
- **D15 — Ruta mutante legacy visible.** `POST /services/{serviceId}/actions/code` no es lectura ni se presume deprecated; queda fuera de estos slices como riesgo residual y deberá integrarse mediante una SPEC posterior.
- **D16 — `systemId` es elegibilidad local, no scope ACME.** Delete e inactivate conservan el rechazo si falta `systemId` para no cambiar el PR 1126, pero la precondición vive localmente en esos consumidores; el autorizador transversal sólo recibe username, team y project.
- **D17 — `401` pertenece a la cadena de seguridad.** El filtro no conoce paths: sólo establece username ante Bearer válido o continúa sin Authentication. `SecurityConfig` es la única fuente de verdad; `permitAll` continúa incluso con Bearer inválido y `.authenticated()` activa el `AuthenticationEntryPoint` de `401`.
- **D18 — Publicación autorizada posteriormente.** La decisión inicial fue mantener la documentación sólo local. El owner la reemplazó explícitamente el 2026-09-14 al ordenar crear SIG-621 y sus dos SPECs técnicas hijas en Spellbook.
- **D19 — Contrato determinista, realidad como smoke.** El mapping ACME se prueba en CI con fixture representativo y la igualdad real de `projectCode` se valida en un smoke no productivo. No se introduce una dependencia live de ACME en la suite automatizada.
- **D20 — Slice 2 hereda Slice 1.** La base obligatoria vigente de la siguiente fase es `origin/feature/operation-authorization-by-team-f1@fbf05159e`. La implementación de SIG-623 debe consumir el `OperationAuthorizationService` y `OperationAccessLevel` ya creados, sin comenzar desde `develop` ni reimplementar ese trabajo; la rama `feature/operation-authorization-by-team-f2@626585ca9` debe incorporar este head.
- **D21 — Pruebas por slice, sin gate final.** Cada SPEC técnica contiene su matriz crítica, regresión, gate de datos, smoke y coverage. El PR de cada slice no queda listo sin esa evidencia y no existe una fase posterior dedicada a probar todo el proyecto.
- **D22 — Encadenamiento secuencial.** Slice 3 parte del head aprobado de Slice 2, Slice 4 del head aprobado de Slice 3 y Slice 5 del head aprobado de Slice 4. Ninguna entrega recrea el autorizador ni se basa directamente en `develop` mientras dependa de cambios aún no mergeados.
- **D23 — Alias ClickHouse probado y `ping` bloqueante de rollout.** `list-warehouses-for-team` permanece allow-listed porque CP ClickHouse aún lo registra y rio-frontend lo consume. `ping` no se incorpora sin respaldo funcional, pero su uso se mide explícitamente y bloquea el rollout si aparece un consumidor real.

## 🔗 Docs / Links

- [SIG-616 — Spellbook](https://spellbook.adminml.com/projects/SIG/specs/SIG-616)
- [SIG-621 — SPEC funcional: Autorización de operaciones por equipo](https://spellbook.adminml.com/projects/SIG/specs/SIG-621)
- [SIG-622 — SPEC técnica Slice 1: autorizador común](https://spellbook.adminml.com/projects/SIG/specs/SIG-622)
- [SIG-623 — SPEC técnica Slice 2: Actions mutantes de Signals](https://spellbook.adminml.com/projects/SIG/specs/SIG-623)
- [[SPEC técnica — Slice 1 — Autorizador común de operaciones]]
- [[SPEC técnica — Slice 2 — Actions mutantes de Signals]]
- [[SPEC técnica — Slice 3 — Mutaciones y deployments de componentes]]
- [[SPEC técnica — Slice 4 — Relaciones y pipelines]]
- [[SPEC técnica — Slice 5 — Actions restantes]]
- [PR 1126 — Autorización ACME para inactivate/delete](https://github.com/melisource/fury_rio-playmaker/pull/1126)
- [DataProductModel — `teamName`](file:///Users/rjara/fuentes/rio-playmaker/src/main/java/com/mercadolibre/rio/playmaker/model/DataProductModel.java)
- [ImportAuthorizationRepository — detección canónica de importados](file:///Users/rjara/fuentes/rio-playmaker/src/main/java/com/mercadolibre/rio/playmaker/repository/ImportAuthorizationRepository.java)

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

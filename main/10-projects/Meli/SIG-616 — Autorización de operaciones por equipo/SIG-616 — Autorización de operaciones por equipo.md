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
progress: 90
repo: https://github.com/melisource/fury_rio-playmaker
jira:
prs:
  - https://github.com/melisource/fury_rio-playmaker/pull/1169
  - https://github.com/melisource/fury_rio-playmaker/pull/1172
  - https://github.com/melisource/fury_rio-playmaker/pull/1178
  - https://github.com/melisource/fury_rio-playmaker/pull/1181
  - https://github.com/melisource/fury_rio-playmaker/pull/1182
aliases:
  - SIG-616
  - Autorización por equipo en Playmaker
tags:
  - kind/project
  - area/meli
created: "2026-09-14"
updated: "2026-09-23"
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

- **Actualización F5 — cierre de mutaciones, supersede las dos viñetas históricas de Slice 5 más abajo:** a pedido del owner, `feature/operation-authorization-by-team-f5@141eacbc5` protege por YAML las mutaciones de Data Products, config/rename de pipeline, definiciones e import authorizations que faltaban en la UI actual de Signals. El guard usa owner persistido, deniega ownership incompleto y elimina el bypass de platform team de F4 cuando hay regla configurada. La auditoría se hizo sobre `ads-signals-frontend@origin/develop:9bf76ffc`; Playmaker no es dueño de favoritos personales ni Entities. [PR #1182](https://github.com/melisource/fury_rio-playmaker/pull/1182) está actualizado. Pasaron 31 selectores focalizados, dos checks L0/LOCAL_STACK con cleanup y 4.107 pruebas en regresión completa (0 fallas, 2 skips). Las ramas test3 nuevas son `feature/sig-616-auth-p5-committer-test3-v23@9b2b7d1f2` y `feature/sig-616-auth-p5-viewer-test3-v24@8f91234e4`; los builds Fury `0.1.19-p5-committer-allowed` y `0.1.20-p5-viewer-denied` terminaron `FINISHED`. La CI de PR #1182 pasó en el build #5492. No hubo deploy; smoke F1 y review humano pendientes. La ampliación y sus excepciones están en [[SPEC técnica — Slice 5 — Actions restantes]] como addendum aprobado.
- **Slice 2 publicado:** `feature/operation-authorization-by-team-f2@2e1d1c8955e`, con base `develop@625f491d218e`, está actualizado en [PR #1172](https://github.com/melisource/fury_rio-playmaker/pull/1172). Tiger publica username, `ActionService` no conserva overloads ni revalida headers, y `catalog-signal + start|stop` exige `DEV_AND_UP` mediante un provider config-backed. No se agregaron reglas para imports, precreation o pares desconocidos. Los comentarios de Ale y Feli fueron respondidos y resueltos; el smoke Tiger/ACME no productivo pasó y su captura quedó adjunta al PR.
- **Slice 3 mergeado:** [PR #1178](https://github.com/melisource/fury_rio-playmaker/pull/1178) fue mergeado a `develop` como `19d70a6cf`; su rama remota fue eliminada. Todos sus threads quedaron resueltos. El cascade señalado por Ale fue trasladado explícitamente a Slice 4; no quedan comentarios de F3 pendientes para Slice 5.
- **Variantes de test Slice 3:** `feature/sig-616-auth-p3-committer-test3-v17@70604efa8` y `feature/sig-616-auth-p3-viewer-test3-v18@c1f6829a0` quedaron publicadas. Fury terminó [0.1.11-p3-committer-matrix](https://web.furycloud.io/rio-playmaker/versions/detail/0.1.11-p3-committer-matrix) y [0.1.12-p3-viewer-denied](https://web.furycloud.io/rio-playmaker/versions/detail/0.1.12-p3-viewer-denied). Ninguna se desplegó.
- **Slice 4 en review:** `feature/operation-authorization-by-team-f4@e75ca90d9`, con base `develop` y merge-base funcional `19d70a6cf`, está sin conflictos en [PR #1181](https://github.com/melisource/fury_rio-playmaker/pull/1181). El comentario nuevo de compatibilidad era válido: el guard cascade anulaba el bypass histórico de equipos plataforma. La corrección publicada conserva ese bypass y deja el guard configurado para el resto. Pasaron 3.995 tests locales, contratos y coverage diferencial 98,95%; los checks visibles de CI, coverage, dependencies y workflow terminaron `SUCCESS`, el review está `APPROVED` y queda smoke manual. GitHub aún informa `mergeStateStatus=BLOCKED` pese a `MERGEABLE`.
- **Variantes de test Slice 4:** `feature/sig-616-auth-p4-committer-test3-v19@632ce2bf9` y `feature/sig-616-auth-p4-viewer-test3-v20@a4ddafb86` incorporan `e75ca90d9`. Fury terminó [0.1.15-p4-committer-allowed](https://web.furycloud.io/rio-playmaker/versions/detail/0.1.15-p4-committer-allowed) y [0.1.16-p4-viewer-denied](https://web.furycloud.io/rio-playmaker/versions/detail/0.1.16-p4-viewer-denied) en `FINISHED`. El mock `ml-ads-signals` se excluyó del bypass de plataforma sólo en esas ramas; `0.1.13`/`0.1.14` quedaron superadas. No hubo deploy.
- **Slice 5 sincronizado y publicado:** `feature/operation-authorization-by-team-f5@a89fcffcb` integró F4 `e75ca90d9` y corrigió la matriz Flink en [PR #1182](https://github.com/melisource/fury_rio-playmaker/pull/1182), con base vigente y `MERGEABLE`. Los permisos `start/stop` se configuran por familias abstractas `flink-sql` y `flink-job` en YAML; sus miembros concretos son `flink-sql`/`gcp-flink-sql` y `aws-flink-job`/`gcp-flink-job`. Quitar la regla familiar desactiva el guard adicional para ambos proveedores. Conserva F2–F4 y agrega sólo validación a Actions existentes, sin cambiar casos de uso, reads, imports ni precreation. Pasaron 25 selectores, ambos checks L0/LOCAL_STACK con cleanup, contratos y `./gradlew check` (4.086 tests, 0 fallas, 2 skips preexistentes). La [CI #5490](https://rp-ci-java.furycloud.io/job/rio-playmaker/5490/) falló antes del checkout por certificado no confiable al descargar el repositorio de pipelines; cobertura y dependencias se abortaron. Smoke Tiger/ACME no productivo pendiente. La descripción actualizada está en [[Descripción PR — rio-playmaker — Slice 5]].
- **Variantes de test Slice 5:** `feature/sig-616-auth-p5-committer-test3-v21@ca35f0b04` y `feature/sig-616-auth-p5-viewer-test3-v22@6c7260690` parten de F5 `a89fcffcb`. Fury terminó [0.1.17-p5-committer-allowed](https://web.furycloud.io/rio-playmaker/versions/detail/0.1.17-p5-committer-allowed) y [0.1.18-p5-viewer-denied](https://web.furycloud.io/rio-playmaker/versions/detail/0.1.18-p5-viewer-denied) en `FINISHED`. El mock ACME vive sólo bajo `test3` y no está en el PR; cada rama pasó 4.101 tests con 0 fallas y 2 skips. No hubo deploy ni smoke remoto.
- **Evidencia de Slice 1:** commit `fbf05159e` en `feature/operation-authorization-by-team-f1`, sincronizado con `origin/develop@073f6a190` mediante el merge `9310ab7b5`; los cuatro tests afectados y `./gradlew check` pasaron, con `2` skips preexistentes. CI, cobertura, dependencias, análisis estático y workflow remoto terminaron correctamente. El feedback útil del review quedó aplicado sin mezclar la precondición legacy `systemId` con el autorizador transversal.
- **Evidencia no productiva:** los smokes ACME/Data Product de Slices 1 y 2 se ejecutaron exitosamente; la evidencia de Slice 2 está adjunta en [PR #1172](https://github.com/melisource/fury_rio-playmaker/pull/1172).
- **Persistencia acordada:** esta nota conserva la continuidad interna. En Spellbook, [SIG-621](https://spellbook.adminml.com/projects/SIG/specs/SIG-621) es la SPEC funcional padre y [SIG-622](https://spellbook.adminml.com/projects/SIG/specs/SIG-622) / [SIG-623](https://spellbook.adminml.com/projects/SIG/specs/SIG-623) son sus SPECs técnicas hijas.
- **Roadmap posterior a Actions:** las SPECs locales de Slice 3, 4 y 5 están creadas. Cada slice contiene sus propios tests, smoke, gate de datos y criterios de salida; no existe un gate final de pruebas separado. La publicación de Slice 3–5 como hijas de SIG-621 sigue pendiente.
- Esta nota es la única fuente de verdad interna del proyecto: contiene baseline externo, decisiones del owner, evidencia del código, exclusiones y riesgos residuales.
- La SPEC SIG-616 de Spellbook se usa como requerimiento de origen aunque figure como `technical`. No se bloquea el avance por su clasificación: las nuevas SPECs explicitan su relación y los overrides deliberados.
- El ownership usado por autorización vive en `DataProduct.teamName + projectCode`; el tipo de Action component-bound proviene de `ComponentModel.componentTemplateCode`. La autorización de Actions no incorpora una condición especial para componentes importados.
- La primera vertical se limita a Actions component-bound de Signals: `catalog-signal + start/stop`. Legacy, otras tecnologías, precreation, polling, deployments y otras mutaciones conservan su comportamiento en esa entrega.
- El [PR 1126](https://github.com/melisource/fury_rio-playmaker/pull/1126) aportó la consulta ACME y los casos de autorización para delete/inactivate; Slice 1 los llevó al mecanismo común sin adoptar `PipelineAuthorizationService.assertAdminAccess` como contrato transversal definitivo.
- `OperationAuthorizationService` se extrajo desde ese comportamiento existente. Delete e inactivate son consumidores de regresión con `DEPLOYER_AND_UP`; Actions Signals agrega `DEV_AND_UP` mediante una capa de permisos configurables.
- PR 1126 ya está mergeado en `origin/develop` (`1a4caf093`); la versión final valida el grant contra `teamName + projectCode`.
- ACME no puede precargarse correctamente sólo con el username: `/grants/user-grants/{username}` no informa el rol de `OwnerProjectGrant`. La verificación precisa requiere `username + teamName + Tiger headers` y luego match exacto de `projectCode`.
- Se definieron sólo dos niveles ACME: `DEV_AND_UP` con committer o superior y `DEPLOYER_AND_UP` con deployer o superior para delete/inactivate. `READ` no es una policy del autorizador: permanece Tiger-only en la frontera HTTP.
- Pipeline deploy está incluido; su ausencia en la lista original se considera un error documental. Las rutas enumeradas expresamente por SIG-616 se protegen aunque alguna esté marcada `@Deprecated`; el legacy no enumerado queda fuera y se identifica mediante allow-list explícita.

## 🧱 Entrega de desarrollo

%% Esta sección siempre queda disponible. En proyectos que cambian código, configuración ejecutable, schemas o infraestructura, es obligatoria: una fila por repo/branch, con SPEC funcional y técnica enlazadas antes de implementar. En proyectos no técnicos, reemplazar la tabla por `_No aplica — <motivo>._`. %%

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| `rio-playmaker` | `feature/operation-authorization-by-team-f1` | `origin/develop@073f6a190` sincronizada por merge | [SIG-621](https://spellbook.adminml.com/projects/SIG/specs/SIG-621), iniciativa derivada de [SIG-616](https://spellbook.adminml.com/projects/SIG/specs/SIG-616) | [SIG-622 — Slice 1](https://spellbook.adminml.com/projects/SIG/specs/SIG-622) | Mergeado en `develop`; smoke no productivo ejecutado exitosamente |
| `rio-playmaker` | `feature/operation-authorization-by-team-f2@2e1d1c8955e` | `develop@625f491d218e` | [SIG-621](https://spellbook.adminml.com/projects/SIG/specs/SIG-621) | [SIG-623 — Slice 2](https://spellbook.adminml.com/projects/SIG/specs/SIG-623) | Implementado y publicado en [PR #1172](https://github.com/melisource/fury_rio-playmaker/pull/1172); review comments resueltos y smoke no productivo aprobado |
| `rio-playmaker` | `feature/operation-authorization-by-team-f3` | `develop` | [SIG-621](https://spellbook.adminml.com/projects/SIG/specs/SIG-621) | [[SPEC técnica — Slice 3 — Mutaciones y deployments de componentes]] | Mergeado por [PR #1178](https://github.com/melisource/fury_rio-playmaker/pull/1178) como `19d70a6cf`; todos los threads resueltos |
| `rio-playmaker` | `feature/operation-authorization-by-team-f4@e75ca90d9` | `develop` (F3 `19d70a6cf`; tip observado `9a559dfb3`) | [SIG-621](https://spellbook.adminml.com/projects/SIG/specs/SIG-621) | [[SPEC técnica — Slice 4 — Relaciones y pipelines]] | [PR #1181](https://github.com/melisource/fury_rio-playmaker/pull/1181) sin conflictos; checks visibles y review aprobados; deploy/smoke manual pendientes; merge state `BLOCKED` |
| `rio-playmaker` | `feature/operation-authorization-by-team-f5@a89fcffcb` | `feature/operation-authorization-by-team-f4@e75ca90d9` | [SIG-621](https://spellbook.adminml.com/projects/SIG/specs/SIG-621) | [[SPEC técnica — Slice 5 — Actions restantes]] | Publicado en [PR #1182](https://github.com/melisource/fury_rio-playmaker/pull/1182); familias Flink en YAML y pruebas locales completas aprobadas; CI bloqueada por certificado y smoke pendiente |

## 🧠 Diseño técnico consolidado

> [!info] Diseño listo para ejecución incremental
> SIG-621, SIG-622 y SIG-623 están creadas en Spellbook. Las SPECs locales de Slice 3, 4 y 5 están cerradas para publicación. Las cinco ramas están implementadas y encadenadas; quedan los reviews y gates externos de cada slice.

### Fuentes y autoridad

| Fuente | Rol | Autoridad |
|---|---|---|
| [SIG-616 en Spellbook](https://spellbook.adminml.com/projects/SIG/specs/SIG-616) | Requerimiento de origen, escrito por terceros | Fuente funcional; sus omisiones o ambigüedades deben registrarse, no corregirse silenciosamente |
| Conversación y decisiones registradas en esta nota | Alcance y decisiones del proyecto | Fuente de verdad para el diseño acordado por el owner |
| `origin/develop` de `fury_rio-playmaker` | Comportamiento implementado | Evidencia técnica; base observada `1a4caf093` |
| [PR 1126](https://github.com/melisource/fury_rio-playmaker/pull/1126) | Implementación ACME existente | Base a refactorizar, no arquitectura transversal definitiva |

Esta separación es deliberada: un requerimiento de la SPEC, una decisión del proyecto y una inferencia del código no son equivalentes.

### Baseline funcional extraído de la SPEC externa

La iniciativa exige autorización server-side para mutaciones y operaciones de componentes mediante identidad Tiger validada, ownership persistido y rol ACME. La implementación incorpora validaciones de manera incremental sin redefinir el catálogo ni el comportamiento de operaciones no configuradas.

Inventario funcional indicado por la SPEC:

- Crear, actualizar, eliminar y modificar diseño o metadatos de componentes.
- Crear, actualizar y eliminar relaciones.
- Crear/eliminar componentes de pipeline y modificar topología, diseño o relaciones.
- Provisionar, desprovisionar e inactivar.
- Ejecutar Actions mutantes sobre componentes de origen.
- Permitir read Actions declaradas con Tiger válido, sin exigir ACME.

Reglas transversales heredadas:

- `team-dev-and-up` equivale a `admin`, `maintainer`, `deployer`, `committer`.
- Los componentes importados conservan el comportamiento existente; la autorización adicional usa el team/project persistido del Data Product.
- Precreation conserva su comportamiento y queda fuera de la autorización component-bound.
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

- **KISS:** un puerto mínimo para resolver permisos y un adapter config-backed; sin motor de policies, jobs o cache.
- **YAGNI:** sin motor de policies, Aspects, annotations ni legacy en la primera entrega.
- **SOLID pragmático:** Tiger autentica; el caso de uso resuelve el target; el autorizador encapsula ACME y roles.
- **Aditividad:** un par no configurado no recibe autorización nueva ni se clasifica como deny.
- **Fuente persistida:** tipo y ownership salen de Playmaker, no del request.
- **Evolución por consumidores reales:** primero se extrae el comportamiento existente; después se agregan nuevas operaciones.

### Alcance incremental

| Etapa | Alcance | Cambio funcional |
|---|---|---|
| Slice 1 | Extraer autorizador desde PR 1126 y migrar delete/inactivate | Ninguno: refactor compatible de la política existente |
| Slice 2 | Corregir principal Tiger e integrar `catalog-signal + start/stop` | Sólo Signals agrega una restricción nueva |
| Slice 3 | Mutaciones y deployments de componentes | `DEV_AND_UP` en todas las rutas enumeradas; tests y rollout en el mismo PR |
| Slice 4 | Relaciones y pipelines, pipeline deploy y cascade de Data Product | Guards exactos config-backed; `DEV_AND_UP` salvo cascade `DEPLOYER_AND_UP`; relaciones same-DP obligatorias por SIG-616 y sin ownership inmutable |
| Slice 5 | Actions mutantes restantes de Flink y ClickHouse | Agrega pares y niveles a la configuración sin modificar otras Actions |

### Niveles ACME

| Nivel | Roles | Uso |
|---|---|---|
| `DEV_AND_UP` | `admin`, `maintainer`, `deployer`, `committer` | Escrituras SIG-616, incluido Signals `start/stop` |
| `DEPLOYER_AND_UP` | `admin`, `maintainer`, `deployer` | Delete e inactivate provenientes del PR 1126 |

Las Actions de lectura quedan fuera del autorizador común y continúan protegidas sólo por Tiger. No se agregarán más niveles sin un caso funcional nuevo.

### Actions: autorización configurada

La clave de autorización es el par exacto `component_type + actionName`, nunca sólo el nombre:

| Tipo persistido | Action | Clasificación | Requisito |
|---|---|---|---|
| `catalog-signal` | `start` | Mutación operacional | Tiger + `DEV_AND_UP` |
| `catalog-signal` | `stop` | Mutación operacional | Tiger + `DEV_AND_UP` |

Reglas asociadas:

- Un par ausente de `app.action-authorization.permissions` conserva su comportamiento actual.
- Otros tipos reciben autorización sólo cuando su par exacto aparece en la configuración activa del scope.
- Kafka y ClickHouse read Actions siguen Tiger-only, tal como indica la SPEC.
- Los componentes importados siguen la misma autorización por team/project persistido; no existe un guard especial de importación.
- Precreation queda fuera y conserva su comportamiento.
- Polling no obtiene una política nueva, no cambia `ActionKvsEntry` y no agrega `resultVisibility`.

Inventario técnico observado para evitar clasificar sólo por nombre:

- Signals: `catalog-signal + start/stop`.
- Kafka: `aws-msk-topic`, `gcp-kafka-topic` y el tipo transicional `kafka-topic` con `peek` de lectura.
- Flink: `start/stop` sobre sus tipos configurados; fuera de la primera vertical.
- ClickHouse: `clickhouse-mat-view + start-materialized-view/stop-materialized-view` queda configurado con `DEV_AND_UP`; las lecturas existentes no reciben autorización ACME nueva.

La reutilización de nombres como `start/stop` entre tecnologías demuestra que `actionName` solo no es una clave de política segura. Los ejemplos prefijados de la SPEC no deben copiarse sin contrastarlos con los contratos reales.

### Estado de Tiger

`CustomAuthorizationFilter` valida Tiger una vez y publica el username como principal:

- Validar Tiger una sola vez.
- Publicar el username como principal en `SecurityContext`.
- No registrar ni exponer el token crudo.
- Eliminar del filtro la allow-list duplicada de rutas. Con Bearer válido publica username; con token ausente, malformado, inválido o expirado continúa sin Authentication. `SecurityConfig` queda como única fuente de verdad: `permitAll` continúa y `.authenticated()` responde `401` mediante un `AuthenticationEntryPoint` explícito.
- Los consumidores productivos de `ActionService` usan una sola firma con username; no existe un overload basado en headers.
- La migración no se extiende a services ajenos a Actions.

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

Existe una única clase concreta, `OperationAuthorizationService`, que:

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

No habrá un autorizador por nivel ni una interfaz artificial alrededor de `OperationAuthorizationService`. El puerto `ActionPermissionProvider` existe por la necesidad explícita de reemplazar la fuente config-backed por Discovery sin tocar consumidores.

### Consumidores implementados

La autorización transversal quedó implementada sobre la base de Slice 1:

```text
PipelineAuthorizationService.assertAdminAccess
    → AuthorizationUtils.requireDeployerOrAbove
    → AcmeClient.getOwnerProjectGrants
```

El flujo vigente queda así:

1. `PipelineComponentDeleteServiceImpl` conserva su autorización `DEPLOYER_AND_UP` mediante `OperationAuthorizationService`.
2. `ComponentInactivationServiceImpl` conserva su autorización `DEPLOYER_AND_UP` mediante el mismo servicio.
3. `ActionServiceImpl` recibe el username ya validado por Tiger y delega en `ActionAuthorizationService` sólo cuando el par `component_type + actionName` está configurado.
4. `ActionAuthorizationService` resuelve el nivel mediante `ActionPermissionProvider` y delega la validación efectiva en `OperationAuthorizationService`.

`PipelineAuthorizationService.assertWriteAccess` y otros helpers con consumidores distintos no se eliminan por arrastre. `AuthorizationUtils.requireDeployerOrAbove` puede retirarse cuando no tenga consumidores productivos.

### Flujo de Signals

```text
[MODIFIED] Tiger filter
    → valida una vez y publica username
[MODIFIED] ActionController + ActionResultController
    → pasan el username de Authentication; no aceptan identidad cliente
[MODIFIED] ActionServiceImpl
    → resuelve DP + componente + environment
    → consulta el permiso para tipo + Action
[NEW] ConfiguredActionPermissionProvider
    → carga permisos desde app.action-authorization.permissions
[NEW] ActionAuthorizationService
    → si el par está configurado, delega la autorización
[EXISTING] OperationAuthorizationService
    → consulta owner-project por username + team
    → valida projectCode + nivel configurado
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
| Par `component_type + actionName` configurado con rol insuficiente | `403 Forbidden` |
| Par no configurado, import o precreation | Conserva el comportamiento previo; esta iniciativa no agrega una regla |
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
- Signals `start/stop` permiten con `DEV_AND_UP` cuando el par exacto está configurado. Un par no configurado, import o precreation conserva el comportamiento previo. Tipo y Action se comparan por igualdad exacta, case-sensitive y sin trim/aliases.
- Grant de otro team o proyecto no habilita.
- `AcmeClientImpl` se valida con fixture contractual representativo de `owner-project`; la convención real de `projectCode` se confirma con smoke no productivo, nunca haciendo depender CI de ACME.
- Rol insuficiente y ACME no verificable retornan `403`; observabilidad interna diferencia la causa.
- Deny/error no guarda `ActionKvsEntry` ni publica BigQueue.
- Allow guarda y publica exactamente una vez.
- Kafka, Flink, ClickHouse, polling, callbacks, imports, precreation y legacy no reciben reglas de negocio nuevas en esta etapa.

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
- Configurar el par exacto `catalog-signal + start/stop` con nivel `DEV_AND_UP`.
- Mantener sin cambios los pares no configurados, imports y precreation.
- Invocar el autorizador con `DEV_AND_UP` después de resolver la jerarquía y antes de contexto de deployment, KVS o BigQueue.
- Mantener Kafka, Flink, ClickHouse, polling, callbacks y legacy sin cambios ni llamadas ACME.
- Agregar pruebas unitarias e integración para allow/deny/error y cero side effects.

Gate de salida: Signals queda protegido end-to-end y todo lo fuera de alcance conserva su comportamiento.

#### Slice 3 — Mutaciones y deployments de componentes

Objetivo: integrar `DEV_AND_UP` en las cinco mutaciones de `ComponentController` y en component deploy/undeploy, usando el principal Tiger validado y la jerarquía persistida antes de cualquier efecto lateral.

La implementación, tests, gate de datos, smoke no productivo y evidencia de coverage viven en [[SPEC técnica — Slice 3 — Mutaciones y deployments de componentes]] y se entregan en un único PR.

##### Casos manuales para probar Slice 3 en test3

Precondición común: desplegar sólo en `jarita-test3`, usar un Data Product de prueba con `teamName=ml-ads-signals` y `projectCode=authorization-smoke-test`, identidad Tiger válida y recursos propios identificables para cleanup. No ejecutar estas variantes en production, staging ni otro scope.

| Caso | Versión | Acción | Resultado esperado |
|---|---|---|---|
| Allow de mutaciones | `0.1.7-p3-committer-allowed` | Crear, actualizar, eliminar, modificar design y ejecutar el patch compatible de nombre/código/template sobre un componente del Data Product de prueba | La operación conserva su respuesta y efectos previos; ACME permite por `committer` (`DEV_AND_UP`) |
| Allow de deployment | `0.1.7-p3-committer-allowed` | Deploy y undeploy por la ruta component-centric y por cada ruta deprecated/compatible cubierta por F3 | La operación se ejecuta una sola vez y conserva el contrato previo |
| Deny sin efectos | `0.1.8-p3-viewer-denied` | Repetir los nueve entrypoints cubiertos por los siete casos de uso | `403`; no hay save/update/delete, attach de definition, dispatch, KVS, BigQueue ni llamadas externas posteriores al guard |
| Jerarquía inválida | Ambas | Usar `componentId` persistido bajo otro `dataProductId` en delete y patch compatible | Rechazo antes de ACME y antes de cualquier efecto; nunca `204` silencioso |
| Identidad inválida | Ambas | Omitir Tiger o usar token inválido sobre un entrypoint autenticado | `401`; no se consulta ACME ni se ejecutan efectos |
| Ownership incompleto | Ambas | Probar un recurso legacy sin `teamName` o `projectCode` | Se preserva exactamente el comportamiento pre-F3; sólo se omite el guard nuevo |
| Fuera de alcance | Ambas | `POST /data-products/v2`, cascade de `DELETE /data-products/{id}`, relaciones/pipelines y Actions no listadas | No atribuir un cambio a F3; el cascade requiere seguimiento explícito y no se valida con estas versiones |

Evidencia mínima: versión y commit desplegados, request sanitizado, status/response, comprobación de side effects o de su ausencia y cleanup de todos los recursos creados.

#### Slice 4 — Relaciones y pipelines

Objetivo: proteger create/update/delete de relaciones con owners persistidos y exigir same-DP antes de autorizar, migrar PUT/design/relations/component-create/pipeline-deploy al autorizador común con `DEV_AND_UP` y cubrir el cascade de Data Product con `DEPLOYER_AND_UP`, todo por configuración exacta.

La implementación, rechazo cross-DP, verificación de cero side effects, smoke y coverage viven en [[SPEC técnica — Slice 4 — Relaciones y pipelines]] y se entregan en un único PR. La decisión del 2026-09-24 reemplaza la compatibilidad cross-DP que se había documentado para F4; antes del deploy hay que comprobar si existen relaciones cross-DP persistidas y planificar su reparación.

#### Slice 5 — Actions restantes

Objetivo: agregar a la misma configuración los pares mutantes existentes de Flink y ClickHouse con su nivel de permiso. Las lecturas y los pares no configurados conservan su comportamiento previo; no existe default deny.

La matriz parametrizada, integración HTTP, inventario de pares, smoke y coverage viven en [[SPEC técnica — Slice 5 — Actions restantes]] y se entregan en un único PR.

### Descomposición de Slice 1 y Slice 2

| Orden | Task conceptual | Gate de término |
|---|---|---|
| T-01 | Corregir principal Tiger y respuesta `401` | Username como principal, token fuera de logs, tests de seguridad verdes |
| T-02 | Extraer autorizador y migrar delete/inactivate | Una implementación; comportamiento `DEPLOYER_AND_UP` intacto |
| T-03 | Configurar permisos de Signals | Sólo `catalog-signal + start/stop` agrega validación `DEV_AND_UP` |
| T-04 | Integrar Actions antes de side effects | Sin llamadas directas a Tiger/ACME ni efectos al rechazar |
| T-05 | Verificar exclusiones y regresión | Tecnologías/rutas fuera de alcance no cambian |
| T-06 | Observabilidad y error mapping | `401/403/404` estables; causas ACME distinguibles internamente sin datos sensibles |

Las tasks definitivas viven en cada SPEC local y se materializarán recién al comenzar la implementación.

### Gates pendientes

- [x] Tratar SIG-616 como requerimiento de origen aunque figure como técnica; relacionar las nuevas SPECs sin bloquear por clasificación.
- [x] Confirmar `catalog-signal + start/stop` y `DEV_AND_UP`.
- [x] Componentes importados: conservan el comportamiento existente; no se agrega una política especial.
- [x] Precreation: conserva el comportamiento existente y no consulta ACME por esta iniciativa.
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
- Confirma que imports y precreation conservan el comportamiento previo; revisa además cross-DP, platformTeams y tempAllCanEdit sin inventar políticas nuevas.
- Contratos reales de Actions: el clasificador debe usar component_type + actionName.
- Rutas modernas y legacy reales; identifica bypasses posibles sin ampliar silenciosamente el alcance.
- Contrato real de ACME: parámetros de getUserGrants y getOwnerProjectGrants, forma del payload, paginación, roles y filtro de projectCode.
- Confirma o refuta que getUserGrants(username) no entrega roles OwnerProjectGrant suficientes.
- Confirma que getOwnerProjectGrants recibe username + teamName + Tiger headers, pero no projectCode.
- Confirma que teamName y projectCode vienen del DataProduct persistido y revisa registros modernos con ownership incompleto.
- Estado real de CustomAuthorizationFilter, SecurityConfig, SecurityContext, duplicación de validación Tiger, logs de token y respuesta HTTP ante fallo.
- Verifica que la iniciativa no introduzca dependencias de importación ni reglas basadas en `sourceComponentId` o `ImportAuthorizationRepository`.
- Todos los call sites productivos de PipelineAuthorizationService.assertAdminAccess y AuthorizationUtils.requireDeployerOrAbove.
- Orden exacto de resolución, consulta ACME y side effects en delete, inactivate y ActionServiceImpl.
- Status HTTP actual cuando ACME falla y compatibilidad de preservar `403` en estos slices, dejando una eventual diferenciación `5xx` fuera de alcance.

Evalúa especialmente esta arquitectura propuesta:

- Sólo Tiger es middleware y publica username en SecurityContext cuando el Bearer es válido; `SecurityConfig`, no el filtro, gobierna `permitAll` y el `401` de rutas autenticadas.
- ACME no es middleware porque la consulta precisa requiere conocer teamName.
- Existe una sola clase concreta OperationAuthorizationService, sin interface/impl ni estrategias prematuras.
- El autorizador recibe caller, teamName, projectCode, headers y nivel; encapsula AcmeClient, roles y errores.
- Delete e inactivate son los primeros consumidores de regresión con DEPLOYER_AND_UP.
- ActionServiceImpl incorpora validación aditiva para los pares configurados y delega en `ActionAuthorizationService`.
- Signals sólo protege `catalog-signal + start/stop` cuando el par está configurado, validando antes de deployment context, KVS y BigQueue.
- Actions no configuradas, imports, precreation, read Actions, polling, otras tecnologías y legacy no reciben reglas nuevas.
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
> - [r] Revisar [PR #1181](https://github.com/melisource/fury_rio-playmaker/pull/1181) y completar gate de datos + smoke Tiger/ACME de Slice 4 #owner/me #type/pr-review #area/meli
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
- **2026-09-14** — La revisión cruzada corrigió un supuesto crítico: `sourceComponentId` también existe en clones de migración y no identifica importación. Se propuso entonces usar `ImportAuthorizationRepository` y rechazar Signals mutante en precreation; ambas decisiones fueron reemplazadas el 2026-09-21 al confirmar que la iniciativa no debe crear reglas de negocio.
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
- **2026-09-16** — Slice 4 se rebasó sobre `origin/feature/operation-authorization-by-team-f3@1f39b556`, restauró el fail-closed de ownership incompleto y cerró dos rondas de code review. La rama `feature/operation-authorization-by-team-f4@0f37f7b29` se publicó y se creó [PR #1181](https://github.com/melisource/fury_rio-playmaker/pull/1181), no draft, con base F3 verificada. Suite forzada: 3.927 tests, 0 fallas, 2 skips; cobertura diferencial 100% line/branch. Gate de datos y smoke Tiger/ACME continúan pendientes antes del merge/rollout.
- **2026-09-16** — Slice 5 se publicó como `feature/operation-authorization-by-team-f5@d721b908e` con base F4 y [PR #1182](https://github.com/melisource/fury_rio-playmaker/pull/1182) listo para review. La revisión confirmó el flujo Tiger/ACME de la SPEC; no quedan findings propios de F5. Se documentó el inventario nominal y los gates de inventario vivo/smoke no productivo.
- **2026-09-21** — Se corrigió el alcance de la iniciativa en toda la cadena: autorización estrictamente aditiva, sin reglas nuevas para imports, precreation o pares no configurados y sin default deny. Slice 2 quedó en `90667a5db` con `ActionPermissionProvider` y adapter de configuración por scope; Slice 3 en `119207a71`, Slice 4 en `ccce34382` y Slice 5 en `6363d7e0e`. Se actualizaron las descripciones de PR, se respondieron y resolvieron los comentarios de Ale y Feli en PR #1172 y se alinearon la SPEC técnica y este proyecto.
- **2026-09-22** — El smoke no productivo Tiger/ACME de Slice 2 pasó; la captura de evidencia quedó adjunta en [PR #1172](https://github.com/melisource/fury_rio-playmaker/pull/1172). Se actualizó la descripción del PR y el estado del proyecto con el head `2e1d1c8955e`.
- **2026-09-22** — Slice 3 se sincronizó con `develop@e26cf2baa` y quedó publicado en `8f9482210`. Se resolvieron los dos findings válidos del bot agregando validación de jerarquía previa en delete y patch compatible; la suite completa, los 17 selectores focalizados y todos los checks remotos pasaron. Las variantes test3 quedaron en `bfe69310f`/`c4a493fb5`, y Fury terminó exitosamente `0.1.7-p3-committer-allowed` y `0.1.8-p3-viewer-denied`. Los dos checks `LOCAL_STACK` no corrieron por Docker no disponible; no hubo deploy ni smoke mutable.
- **2026-09-23** — Slice 3 fue mergeado a `develop@19d70a6cf` y su rama remota se eliminó. Slice 4 se regularizó de forma aditiva/config-backed, incorporó el cascade pedido por Ale y quedó en `d792b902b` tras merges conservadores `7c9195a65` y `d792b902b`. Pasaron 20 selectores, ambos checks `LOCAL_STACK`, suite forzada, 100% de coverage diferencial y todos los checks remotos; los threads de #1178/#1181 fueron clasificados, respondidos y resueltos. Las variantes `test3` `0.1.13-p4-committer-allowed` y `0.1.14-p4-viewer-denied` terminaron `FINISHED`, sin deploy.
- **2026-09-23** — Un comentario posterior de #1181 detectó una regresión real: el cascade configurado denegaba a miembros plataforma sin grant del owner. Se publicó `e75ca90d9`, que conserva el bypass heredado, con tests que cargan `application.yml` y `DataProductAccessService` reales. La suite forzada pasó con 3.995 tests (0 fallas, 2 skips), coverage diferencial 98,95%. Se actualizaron las ramas test3; las versiones `0.1.15`/`0.1.16` terminaron `FINISHED`, sin deploy. Los checks visibles y el review quedaron aprobados; smoke manual pendiente y merge state `BLOCKED`.
- **2026-09-23** — F5 incorporó el último HEAD F4 `e75ca90d9` en `dfc26fda7`, resolviendo sólo los conflictos de la lista config-backed y `ActionAuthorizationServiceTest`. Se conservaron los diez pares F5, las reglas F4 y el bypass plataforma. La diferencia F4→F5 queda en nueve archivos sin cambios en los casos de uso; pasaron 24 selectores, dos checks locales con cleanup, contratos y 4.077 tests completos (0 fallas, 2 skips). Se publicó la rama y se actualizó [PR #1182](https://github.com/melisource/fury_rio-playmaker/pull/1182), cuya base y mergeability quedaron correctas. Smoke Tiger/ACME no productivo pendiente.
- **2026-09-23** — El comentario humano de [PR #1182](https://github.com/melisource/fury_rio-playmaker/pull/1182#discussion_r4038849416) señaló que la matriz F5 tenía aliases Flink no reconocidos por Control Plane y omitía GCP. F5 `a89fcffcb` reemplazó los permisos concretos Flink por familias `flink-sql`/`flink-job` y un mapa explícito de miembros en YAML; F2–F4 siguen en `permissions`. Se confirmó la semántica aditiva: pares no configurados no activan ACME nuevo. La diferencia F4→F5 afecta 11 archivos, sin cambiar casos de uso. Pasaron 25 selectores, dos checks locales con cleanup, contratos y 4.086 tests completos (0 fallas, 2 skips); el PR se publicó y permanece `MERGEABLE`. La CI #5490 falló antes del checkout por certificado no confiable del repositorio de pipelines; cobertura y dependencias se abortaron. Smoke Tiger/ACME no productivo pendiente.
- **2026-09-23** — Se crearon desde F5 las variantes mock `test3` committer `ca35f0b04` y viewer `6c7260690`, en ramas separadas. Cargan el YAML F5 y prueban los diez pares: el primero permite `DEV_AND_UP`, el segundo lo deniega. Contratos y suites completas pasaron en ambas ramas (4.101 tests, 0 fallas, 2 skips cada una). Fury completó `0.1.17-p5-committer-allowed` y `0.1.18-p5-viewer-denied` en `FINISHED`; no se desplegaron.

## 🧭 Decisiones

- **D1 — Primer cambio funcional sólo Signals.** La primera restricción nueva protege `catalog-signal + start/stop` sobre componentes existentes; el refactor previo de delete/inactivate no cambia su política. Legacy, otras tecnologías, polling, imports y precreation conservan su comportamiento.
- **D2 — Sólo Tiger es middleware.** Tiger se valida una vez en la frontera HTTP y publica el username. ACME se consulta desde un autorizador reutilizable cuando el caso de uso ya conoce el scope persistido.
- **D3 — Configuración aditiva de tipo + Action.** Sólo un par exacto presente en la configuración recibe la validación nueva. Un par desconocido conserva su comportamiento anterior; la ausencia en configuración no implica deny.
- **D4 — Services consumidores con una sola validación.** Actions resuelve el target y llama una vez a un autorizador concreto con caller, `teamName`, `projectCode` y nivel antes de cualquier side effect; no consume `AcmeClient` ni implementa listas o parsing de roles.
- **D5 — PR 1126 converge por refactor.** Se reutiliza `AcmeClient.getOwnerProjectGrants`; la API acoplada a pipeline y la política estática se refactorizan a medida que se incorporan casos reales.
- **D6 — Annotation al final, no ahora.** `@RequiresCapability` se evaluará sobre services cuando exista repetición comprobada; queda documentada como evolución final y fuera de alcance inicial.
- **D7 — Playmaker es el enforcement point.** Los CPs siguen procesando eventos defensivamente, pero no resuelven Tiger ni ACME; reciben sólo requests ya autorizados por Playmaker.
- **D8 — SPECs y tasks antes de código.** Se cierra diseño, se valida el requerimiento de origen y se acuerda una SPEC por vertical con sus tasks antes de definir branch/base e implementar.
- **D9 — Dos niveles ACME cerrados.** `DEV_AND_UP` y `DEPLOYER_AND_UP`; delete/inactivate conservan los tres roles del PR 1126 y el resto de escrituras SIG-616 usa los cuatro roles dev+. `READ` queda Tiger-only fuera del autorizador.
- **D10 — Pipeline deploy incluido y legacy explícito.** La ruta moderna de pipeline deploy debe incorporarse a la SPEC. Toda ruta enumerada expresamente por SIG-616 se protege aunque esté marcada `@Deprecated`; las rutas legacy no enumeradas quedan fuera.
- **D11 — ACME preciso, no precarga incompleta.** No se usa `getUserGrants(username)` para permisos por proyecto. El autorizador reutiliza `getOwnerProjectGrants(username, teamName, headers)` y valida el `projectCode` persistido.
- **D12 — Autorizador concreto y fuente de permisos reemplazable.** `OperationAuthorizationService` permanece como una clase concreta y única. Para Actions existe el puerto mínimo `ActionPermissionProvider`, hoy implementado por un adapter de configuración, de modo que Discovery pueda reemplazar sólo la fuente sin afectar consumidores.
- **D13 — Sin política especial para imports.** Esta iniciativa no determina ni altera la autorización de importación. Las Actions sobre componentes importados conservan el comportamiento previo y no dependen de `ImportAuthorizationRepository`.
- **D14 — Compatibilidad de errores ACME.** Rol insuficiente y ACME no verificable fallan cerrado con `403` en estos slices. Se distinguen mediante observabilidad interna; migrar indisponibilidad a `5xx` requiere una decisión futura explícita.
- **D15 — Ruta mutante legacy visible.** `POST /services/{serviceId}/actions/code` no es lectura ni se presume deprecated; queda fuera de estos slices como riesgo residual y deberá integrarse mediante una SPEC posterior.
- **D16 — `systemId` sólo es precondición legacy.** Delete e inactivate preservan la validación de `systemId` únicamente cuando `environment == legacy`; los Data Products modernos no adquieren esa restricción. El autorizador transversal sólo recibe username, team y project.
- **D17 — `401` pertenece a la cadena de seguridad.** El filtro no conoce paths: sólo establece username ante Bearer válido o continúa sin Authentication. `SecurityConfig` es la única fuente de verdad; `permitAll` continúa incluso con Bearer inválido y `.authenticated()` activa el `AuthenticationEntryPoint` de `401`.
- **D18 — Publicación autorizada posteriormente.** La decisión inicial fue mantener la documentación sólo local. El owner la reemplazó explícitamente el 2026-09-14 al ordenar crear SIG-621 y sus dos SPECs técnicas hijas en Spellbook.
- **D19 — Contrato determinista, realidad como smoke.** El mapping ACME se prueba en CI con fixture representativo y la igualdad real de `projectCode` se valida en un smoke no productivo. No se introduce una dependencia live de ACME en la suite automatizada.
- **D20 — Slice 2 hereda Slice 1.** La rama publicada `feature/operation-authorization-by-team-f2@90667a5db` consume `OperationAuthorizationService` y `OperationAccessLevel` de Slice 1 sin reimplementarlos. Las siguientes ramas permanecen encadenadas sobre el head de su slice anterior.
- **D21 — Pruebas por slice, sin gate final.** Cada SPEC técnica contiene su matriz crítica, regresión, gate de datos, smoke y coverage. El PR de cada slice no queda listo sin esa evidencia y no existe una fase posterior dedicada a probar todo el proyecto.
- **D22 — Encadenamiento secuencial.** Slice 3 parte del head aprobado de Slice 2, Slice 4 del head aprobado de Slice 3 y Slice 5 del head aprobado de Slice 4. Ninguna entrega recrea el autorizador ni se basa directamente en `develop` mientras dependa de cambios aún no mergeados.
- **D23 — Sólo mutaciones comprobadas en Slice 5.** Los pares mutantes existentes de Flink y ClickHouse se agregan a la configuración. Reads, aliases y `ping` no adquieren autorización ACME ni bloquean por ausencia en configuración.
- **D24 — Configuración por scope, contrato estable.** `app.action-authorization.permissions` es la fuente actual por ambiente/scope. Los consumidores dependen de `ActionPermissionProvider`; una carga futura desde Discovery, job o bootstrap reemplaza el adapter sin cambiar `ActionServiceImpl` ni `ActionAuthorizationService`.
- **D25 — Same-DP en relaciones.** El owner indicó el 2026-09-24 aplicar la invariante explícita de SIG-616 pese a la decisión previa de F4 de preservar cross-DP. Create/update/delete rechazan extremos de Data Products distintos antes de autorización y mutación; update puede mover ambos extremos juntos a otro Data Product con autorización de owner actual y solicitado. Esta decisión requiere auditar datos cross-DP antes del rollout.

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
- [PR #1172 — Slice 2: Actions mutantes de Signals](https://github.com/melisource/fury_rio-playmaker/pull/1172)
- [PR #1178 — Slice 3: mutaciones y deployments de componentes](https://github.com/melisource/fury_rio-playmaker/pull/1178)
- [PR #1181 — Slice 4: relaciones y pipelines](https://github.com/melisource/fury_rio-playmaker/pull/1181)
- [PR #1182 — Slice 5: Actions restantes](https://github.com/melisource/fury_rio-playmaker/pull/1182)
- [DataProductModel — `teamName`](file:///Users/rjara/fuentes/rio-playmaker/src/main/java/com/mercadolibre/rio/playmaker/model/DataProductModel.java)

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

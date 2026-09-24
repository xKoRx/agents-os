# SIG-616 — Slice 4: relaciones, pipelines y cascade de Data Product

## Metadatos

- Tipo: Technical SPEC
- Estado: Ajuste same-DP y tests de review en curso; pruebas manuales pendientes
- SPEC funcional: [SIG-621](https://spellbook.adminml.com/projects/SIG/specs/SIG-621)
- Requerimiento: [SIG-616](https://spellbook.adminml.com/projects/SIG/specs/SIG-616)
- Aplicación: `rio-playmaker`
- PR: [#1181](https://github.com/melisource/fury_rio-playmaker/pull/1181)
- Rama: `feature/operation-authorization-by-team-f4`
- Base del PR: `develop`; F3 fue incorporado en `19d70a6cf` y el tip observado al cierre es
  `9a559dfb3` (cambio posterior sólo de metadata de agentes, sin conflictos con F4)
- Merge inicial de F3: `7c9195a65`
- Implementación regularizada: `e8b957c47`
- Merge final de `develop`, sin cambio de árbol: `d792b902b`
- Corrección del bypass de plataforma: `e75ca90d9`
- HEAD vigente: `e75ca90d98fba2dc4e4ef35686e2f38cf8462402`

## Objetivo y límites

Fase 4 agrega guards configurables a casos de uso existentes de relaciones y pipeline, más el
cascade iniciado por `DELETE /data-products/{id}` trasladado desde el review de F3. Es aditiva:

- no crea endpoints ni casos de uso nuevos;
- conserva las reglas funcionales de topology, ownership y estados; en relaciones exige same-DP como pide SIG-616 y rechaza cross-DP con `400`;
- no vuelve inmutable el ownership de una relación: update puede cambiar endpoints dentro del mismo Data Product;
- un par no configurado conserva el flujo anterior y no invoca ACME por el guard nuevo;
- el nivel exigido sale sólo de `app.action-authorization.permissions`;
- los guards nuevos con `teamName` o `projectCode` incompletos se omiten por compatibilidad;
- los consumidores anteriores a F3 conservan su semántica fail-closed;
- component delete e inactivate de F1 continúan en `DEPLOYER_AND_UP` sin cambios.

Los headers Tiger se propagan porque `AcmeClient` los necesita. La identidad de los casos migrados
se obtiene de `Authentication.getName()` en el controller y se pasa explícitamente; los services de
F4 no vuelven a extraerla desde headers.

## Alcance exacto y matriz configurada

| Scope | Operación | Endpoint | Caso de uso | Nivel inicial |
|---|---|---|---|---|
| `component-relation` | `create` | `POST /component-relations` | `ComponentRelationServiceImpl.create` | `DEV_AND_UP` |
| `component-relation` | `update` | `PUT /component-relations/{componentRelationId}` | `ComponentRelationServiceImpl.update` | `DEV_AND_UP` |
| `component-relation` | `delete` | `DELETE /component-relations/{componentRelationId}` | `ComponentRelationServiceImpl.delete` | `DEV_AND_UP` |
| `pipeline` | `replace-topology` | `PUT /data-products/{name}/environments/{envName}/pipeline` | `PipelineWriteServiceImpl.writePipeline` | `DEV_AND_UP` |
| `pipeline` | `update-design` | `PATCH /data-products/{name}/pipeline/design` | `PipelineDesignServiceImpl.updateDesign` | `DEV_AND_UP` |
| `pipeline` | `update-relations` | `PATCH /data-products/{name}/pipeline/relations` | `PipelineRelationsServiceImpl.updateRelations` | `DEV_AND_UP` |
| `pipeline` | `create-component` | `POST /data-products/{name}/pipeline/components` | `ComponentCreateServiceImpl.createComponent` | `DEV_AND_UP` |
| `pipeline` | `deploy` | `POST /data-products/{name}/environments/{envName}/pipeline/deploy` | `PipelineDeployServiceImpl.deploy` | `DEV_AND_UP` |
| `data-product` | `cascade-delete-components` | `DELETE /data-products/{id}` | `DataProductServiceImpl.delete` | `DEPLOYER_AND_UP` |

No incluye config patch, rename, reads, Actions, precreation, polling, imports ni endpoints legacy
adicionales.

## Arquitectura config-backed

```text
app.action-authorization.permissions
  -> ConfiguredActionPermissionProvider.findExactAccessLevel(scope, operation)
    -> ActionAuthorizationService.requireOperationIfConfigured(...)
      -> OperationAuthorizationService.require(..., accessLevel)
        -> AcmeClient.getOwnerProjectGrants(...)
```

`findExactAccessLevel` no aplica el fallback `component-type: "*"`. Por eso entradas heredadas como
`*:create`, `*:update`, `*:delete`, `*:update-design` o `*:deploy` no activan por accidente una
relación, un pipeline o un Data Product. Remover una de las nueve entradas desactiva sólo ese guard.
La lista puede reemplazarse por scope sin modificar consumidores.

No existe un segundo provider ni un motor de policies. No hay niveles hardcodeados dentro de los
casos de uso F4.

## Contrato de relaciones

### Create

1. Conserva las validaciones previas de existencia, soft delete, self-loop y pertenencia de cada component al Data Product declarado.
2. Exige que los Data Products persistidos de source y destination tengan el mismo ID; cross-DP retorna `400` antes de ACME o save.
3. Autoriza el owner persistido con `component-relation:create`.
4. Sólo después mapea, completa auditoría con el username propagado y guarda.

### Update

1. Conserva el lookup de la relación y el rechazo si ya fue borrada.
2. Conserva las validaciones previas de los extremos solicitados y exige que ambos pertenezcan al mismo Data Product antes de ACME o save.
3. Autoriza los owners persistidos distintos del estado actual y del solicitado con `component-relation:update`.
4. Sólo después ejecuta el mapper existente, auditoría y save.

F3 permitía cambiar source/destination Data Product; el ajuste solicitado por el owner aplica la invariante same-DP de SIG-616 a la relación solicitada. Update puede trasladar ambos extremos juntos a otro Data Product, autorizando el owner anterior y el nuevo. Una relación cross-DP histórica puede actualizarse a una relación válida dentro de un solo Data Product; su delete queda rechazado hasta reparar el dato.

### Delete

1. Resuelve la relación persistida y conserva el rechazo si ya fue borrada.
2. Exige same-DP en los extremos persistidos antes de ACME o save.
3. Autoriza su owner persistido con `component-relation:delete`.
4. Sólo después completa `deletedAt/deletedBy` y guarda.

## Contrato de pipeline

Cada caso conserva `PipelineAuthorizationService.assertWriteAccess` y todas las validaciones de
negocio previas. F4 agrega el guard exacto contra el `DataProductModel` persistido antes del primer
side effect. Si la entrada no está configurada, la llamada es no-op y el orden relativo entre las
validaciones existentes no cambia.

- `replace-topology`: antes de `checkAndIncrementVersion` y cualquier persistencia.
- `update-design`: después de resolver todos los components pedidos y antes de mutar metadata.
- `update-relations`: después de versión, components, engine guard y self-loop; antes de add/remove
  o incrementar versión.
- `create-component`: después de lookups y duplicate pre-check; antes de versionar o guardar.
- `deploy`: después de resolver Data Product, environment y pipeline; antes de freeze, rollback,
  delta, desired-state hash, execution, runs, groups o dispatch.

Pipeline deploy autoriza una sola vez el Data Product completo; no autoriza component por component.

## Cascade de `DELETE /data-products/{id}`

Ale señaló en PR #1178 que `DataProductServiceImpl.delete()` podía llamar
`ComponentServiceImpl.deleteByDataProductId(...)` sin pasar por la autorización del delete
individual. F4 lo corrige sin cambiar el contrato del delete:

1. `DataProductController.delete` toma el username de `Authentication.getName()`.
2. `DataProductServiceImpl.delete` conserva blockers, lookup, status/deleted checks, snapshots y la
   precondición histórica `assertPrivilegedRole`.
3. Si el precheck histórico autorizó por pertenencia a un equipo plataforma, conserva ese bypass.
   Para los demás usuarios ejecuta una vez `data-product:cascade-delete-components` contra el
   Data Product persistido.
4. Sólo después inicia el cascade, borra notifications, publica el evento y guarda el soft delete.
5. `ComponentServiceImpl.deleteByDataProductId` recibe username explícito para auditoría; conserva
   headers sólo para cancelaciones downstream existentes.

Un deny impide delete de components, notifications, evento y save. Si la entrada no existe o el
ownership está incompleto, sólo se omite el guard nuevo y permanece la semántica previa, incluida la
precondición heredada del delete del Data Product.

El comentario de compatibilidad en #1181 detectó que, antes de `e75ca90d9`, el guard adicional
anulaba el bypass de `cross-dps-rio`/`ml-ads-signals`. El precheck ahora informa si autorizó por
equipo plataforma y sólo el cascade omite su guard en ese caso. Los demás consumidores del precheck
conservan su flujo. En scopes Fury de test, el bypass preexistente por `FURY_IS_TEST_SCOPE` sigue
omitiendo el precheck histórico; el guard F4 permanece activo para poder probarlo con mocks.

## Identidad y compatibilidad

- Controllers de relaciones, topology mutante, pipeline deploy y Data Product delete usan el
  principal autenticado.
- Los services usan el username propagado para auditoría cuando corresponde.
- `PipelineTopologyController` conserva `TigerTokenService` sólo para el GET no migrado.
- Headers Tiger siguen llegando a `OperationAuthorizationService`/ACME.
- Ownership incompleto no convierte el guard nuevo de F4 en deny.

## Comentarios de review

| Origen | Clasificación | Decisión |
|---|---|---|
| PR #1178, Ale: cascade elude delete individual | Válido, trasladado a F4 | Implementado con guard único antes del cascade y tests de cero side effects; respuesta publicada en el thread original. |
| PR #1181, bot: ownership inmutable en relation update | No aplicable | F3 ya permitía modificar esos campos con `ComponentRelationMapper.updateModelFields`. Prohibirlo sería lógica nueva. Se conserva el baseline y se autorizan owners actual y solicitados. |
| PR #1181, kmontero: plataforma pierde bypass en cascade | Válido; regresión F4 | Corregido en `e75ca90d9`: el guard nuevo respeta el bypass histórico sólo para miembros plataforma. Test con `application.yml` real, `DataProductAccessService` real, sin owner grant, más casos deny/allow y cero side effects. |
| PR #1181, dmuena: same-DP en relaciones | Válido por SIG-616; reemplaza la decisión local previa de compatibilidad cross-DP | Se exige same-DP en create/update/delete antes de autorización y mutación; el rechazo es `400`. El rollout requiere comprobar relaciones cross-DP persistidas antes de desplegar. |
| PR #1181, dmuena: `FURY_IS_TEST_SCOPE` cambia el flujo | Válido como cambio observable; esperado para probar el guard por scope | El precheck histórico se omite en test scope y el guard F4 sigue gobernado por la configuración efectiva; se agregan tests de allow/deny con ACME simulado. |
| PR #1178, comentarios restantes | Heredados/ya corregidos en F3 | La base sincronizada ya contiene las correcciones; no se duplican. Hallazgos fuera de alcance van a F5. |

## Archivos productivos

- Config/provider: `application.yml`, `ActionPermissionProvider`,
  `ConfiguredActionPermissionProvider`, `ActionAuthorizationService`.
- HTTP: `ComponentRelationController`, `PipelineTopologyController`,
  `PipelineDeploymentController`, `DataProductController`.
- Implementación: `ComponentRelationServiceImpl`, `PipelineWriteServiceImpl`,
  `PipelineDesignServiceImpl`, `PipelineRelationsServiceImpl`, `ComponentCreateServiceImpl`,
  `PipelineDeployServiceImpl`, `DataProductServiceImpl`, `ComponentServiceImpl` y sus interfaces.

No hay endpoints, modelos, tablas ni migraciones nuevos. La invariante same-DP de SIG-616 pasa a validarse en el servicio de relaciones.

## Evidencia automatizada

Evidencia inicial sobre `d792b902b` y regresión final sobre `e75ca90d9`:

| Evidencia | Resultado |
|---|---|
| 20 selectores focalizados de `.testing/impact.json` | PASS |
| `./scripts/validate-repository-contract.sh --staged` | PASS |
| `./scripts/validate-testing-contract.sh --staged` | PASS |
| `./scripts/run-agentic-testing-contract.sh` | PASS |
| `AT-000-S01:L0-LOCAL_STACK` | PASS, MySQL/app local y cleanup certificado |
| `AT-180-S18:L0-LOCAL_STACK` | PASS, success/failure/timeout y cleanup certificado |
| `./gradlew check --rerun-tasks --no-daemon --no-build-cache` | PASS sobre `e75ca90d9`: 3.995 tests, 0 fallas, 0 errores, dos skips preexistentes |
| `./gradlew jacocoTestReport --no-daemon --no-build-cache` | PASS |
| Coverage de líneas ejecutables agregadas contra F3 | 94/95, 98,95% |
| Coverage global de líneas | 14.350/14.784, 97,06% |
| Test de compatibilidad plataforma con configuración real | PASS: `application.yml` real, `DataProductAccessService` real y owner grant ausente |
| `git diff --check` | PASS |

El primer intento local detectó Docker inactivo y luego Compose no registrado como plugin. Se
inició Colima y se registró el plugin Homebrew ya instalado; la ejecución final completa pasó. No se
ejecutó smoke remoto ni se desplegó ninguna versión.

## Matriz manual para variantes mock

| Operación | Endpoint | Precondiciones | Mock/rol | Entrada | Resultado esperado y side effects |
|---|---|---|---|---|---|
| Crear relación | `POST /component-relations` | Components existentes; payload válido | committer | `component-relation:create=DEV_AND_UP` | Allow; relación creada. |
| Crear relación | mismo endpoint | Mismo dataset aislado | viewer | misma | `403`; no save ni auditoría. |
| Pipeline deploy | `POST /data-products/{name}/environments/{env}/pipeline/deploy` | Pipeline con delta | committer | `pipeline:deploy=DEV_AND_UP` | `202`/flujo vigente; execution/run/dispatch según delta. |
| Pipeline deploy | mismo endpoint | Mismo fixture | viewer | misma | `403`; sin freeze posterior, delta, execution, run ni dispatch. |
| Cascade delete | `DELETE /data-products/{id}` | DP borrable, sin blockers; grant histórico admin/maintainer y grant del owner suficiente | admin/maintainer | `data-product:cascade-delete-components=DEPLOYER_AND_UP` | Allow; cascade/event/save vigentes. |
| Cascade delete | mismo endpoint | DP borrable; pertenencia a equipo plataforma | miembro plataforma sin grant del owner | misma | Allow por bypass histórico; cascade/event/save vigentes. |
| Cascade delete | mismo endpoint | DP borrable, sin blockers; actor no-plataforma en `test3` | committer o viewer | misma | `403`; cero mutaciones posteriores. |
| Operación sin entrada | cualquiera anterior | Quitar sólo el par en scope test | cualquiera | ausente | Flujo previo; el guard nuevo no llama ACME. |
| Ownership incompleto | operación F4 | DP sin team o project | cualquiera | presente | Se omite sólo el guard nuevo; continúa el flujo heredado. |

## Variantes no productivas

- `feature/sig-616-auth-p4-committer-test3-v19@632ce2bf9`, versión
  [`0.1.15-p4-committer-allowed`](https://web.furycloud.io/rio-playmaker/versions/detail/0.1.15-p4-committer-allowed).
- `feature/sig-616-auth-p4-viewer-test3-v20@a4ddafb86`, versión
  [`0.1.16-p4-viewer-denied`](https://web.furycloud.io/rio-playmaker/versions/detail/0.1.16-p4-viewer-denied).

Ambas ramas incorporan `e75ca90d9`; los mocks están restringidos al profile `test3` y no forman
parte de la rama del PR. La configuración de prueba excluye al team mock `ml-ads-signals` de
`app.acmeClient.platform-teams` para que el smoke ejercite el guard; un test valida esa separación.
Las versiones anteriores `0.1.13`/`0.1.14` quedaron superadas por esta corrección. Los nuevos
builds terminaron `FINISHED` y aún no se desplegaron; las pruebas manuales no se declaran ejecutadas.
El caso real de bypass plataforma está cubierto por test automatizado con configuración real; las
variantes mock `test3` excluyen deliberadamente al team mock de plataforma. Si
`FURY_IS_TEST_SCOPE=true`, además se omite la precondición histórica antes de evaluar membresía
plataforma, por lo que esas variantes no sirven como prueba manual de dicho bypass.

## Riesgos y gates pendientes

- Checks visibles del nuevo HEAD (`continuous-integration`, `code-coverage`, `dependencies`, `workflow`) en `SUCCESS`; review `APPROVED`. GitHub aún informa `mergeStateStatus=BLOCKED`, sin conflictos (`MERGEABLE`); no se infiere habilitación para merge.
- Builds Fury test3 terminados `FINISHED`; falta deploy no productivo.
- Pruebas manuales sobre esas variantes; no se declaran aprobadas antes de ejecutarlas.
- No se realizará versión estable ni deployment productivo.
- AppSec especializado no estaba disponible; se hizo revisión manual de identidad, scope
  persistido, precedencia, wildcard y side effects, más la regresión completa.

## Criterios de aceptación

- Las nueve operaciones usan configuración para activación y nivel.
- Wildcards de components no activan relation/pipeline/Data Product.
- Ausencia de entrada u ownership incompleto conserva compatibilidad aditiva.
- Deny ocurre antes del primer side effect.
- Create/update/delete de relaciones rechazan cross-DP antes de ACME y persistencia; update conserva cambios de endpoints cuando ambos pertenecen al mismo Data Product.
- Cascade autoriza una vez el Data Product persistido y no muta al denegar.
- El bypass heredado de equipos plataforma permite el cascade sin owner grant adicional.
- Username proviene del principal; headers quedan por ACME/downstreams existentes.
- Delete/inactivate heredados continúan en `DEPLOYER_AND_UP`.
- El diff contra F3 contiene sólo F4 y el cascade trasladado.

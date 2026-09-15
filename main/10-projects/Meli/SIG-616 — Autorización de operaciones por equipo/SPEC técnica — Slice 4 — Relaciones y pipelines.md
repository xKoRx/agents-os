# SIG-616 — Slice 4: relaciones y pipelines

## Metadatos

- Tipo: Technical SPEC
- Estado inicial: Draft
- SPEC funcional: [SIG-621](https://spellbook.adminml.com/projects/SIG/specs/SIG-621)
- Requerimiento de origen: [SIG-616](https://spellbook.adminml.com/projects/SIG/specs/SIG-616)
- Dependencia: Slice 3 aprobado e implementado
- Aplicación: `rio-playmaker`

## Objetivo

Aplicar la autorización por equipo a las relaciones entre componentes y a las mutaciones modernas de pipeline. Las relaciones deben resolver sus extremos desde persistencia, pertenecer a un único Data Product y autorizar `DEV_AND_UP` contra ese owner. Los cambios de pipeline deben resolver el Data Product por nombre y autorizar antes de versionar, persistir topología, modificar relaciones, crear componentes o iniciar un pipeline deploy.

El slice también protege `pipeline deploy`, porque un despliegue de pipeline puede generar deltas `DEPLOY` y `UNDEPLOY` y crear ejecuciones antes de despachar trabajo. Se autoriza una vez contra el Data Product antes de calcular o persistir esos efectos.

## Alcance

### Relaciones directas

| Operación | Ruta | Caso de uso | Requisito |
|---|---|---|---|
| Crear relación | `POST /component-relations` | `ComponentRelationServiceImpl.create` | Misma DP + Tiger + `DEV_AND_UP` |
| Actualizar relación | `PUT /component-relations/{componentRelationId}` | `ComponentRelationServiceImpl.update` | Relación persistida + misma DP + Tiger + `DEV_AND_UP` |
| Eliminar relación | `DELETE /component-relations/{componentRelationId}` | `ComponentRelationServiceImpl.delete` | Relación persistida + misma DP + Tiger + `DEV_AND_UP` |

### Pipeline

| Operación | Ruta | Caso de uso | Requisito |
|---|---|---|---|
| Reemplazar topología/configuración | `PUT /data-products/{name}/environments/{envName}/pipeline` | `PipelineWriteServiceImpl.writePipeline` | Tiger + `DEV_AND_UP` |
| Modificar diseño | `PATCH /data-products/{name}/pipeline/design` | `PipelineDesignServiceImpl.updateDesign` | Tiger + `DEV_AND_UP` |
| Modificar relaciones | `PATCH /data-products/{name}/pipeline/relations` | `PipelineRelationsServiceImpl.updateRelations` | Tiger + `DEV_AND_UP` |
| Crear componente | `POST /data-products/{name}/pipeline/components` | `ComponentCreateServiceImpl.createComponent` | Tiger + `DEV_AND_UP` |
| Desplegar pipeline | `POST /data-products/{name}/environments/{envName}/pipeline/deploy` | `PipelineDeployServiceImpl.deploy` | Tiger + `DEV_AND_UP` |

Pipeline component delete e inactivate permanecen en `DEPLOYER_AND_UP` y continúan consumiendo el autorizador común implementado en Slice 1.

### No incluye

- Mutaciones de componentes y component deployment cubiertas por Slice 3.
- Actions, precreation, polling o service-level actions.
- Reparar o migrar relaciones cross-DP ya persistidas.
- Permitir relaciones cross-DP: se rechazan como inválidas.
- `PATCH /data-products/{name}/environments/{envName}/pipeline/components/{componentName}/config`, que no forma parte del inventario de rutas de SIG-616.
- Remover `platformTeams` o `tempAllCanEdit` de comportamientos ajenos; ninguno puede conceder acceso en las rutas de este slice.
- Nuevas tablas, cambios de schema, cache ACME, annotations o AOP.

## Arquitectura objetivo

```text
HTTP request
  -> Spring Security / CustomAuthorizationFilter [UNCHANGED]
       publica username en Authentication.principal
  -> controllers de relations o pipeline [MODIFIED]
       pasan username + headers
  -> repositorios Playmaker [UNCHANGED]
       resuelven DataProduct, relation, components, environment y pipeline
  -> validación de consistencia [MODIFIED]
       relation.source.dp == relation.destination.dp
       request source/destination pertenecen al mismo DataProduct
       environment y pipeline pertenecen al DataProduct del path
  -> OperationAuthorizationService [UNCHANGED]
       require(username, teamName, projectCode, headers, DEV_AND_UP)
  -> mutación o dispatch [MODIFIED]
```

## Contrato de relaciones

### Create

1. Resolver los Data Products y componentes indicados por el request.
2. Comprobar que ambos componentes están activos y pertenecen a los Data Products declarados.
3. Exigir `sourceDataProductId == destinationDataProductId`.
4. Autorizar `DEV_AND_UP` contra ese Data Product persistido.
5. Mapear y guardar la relación.

### Update

1. Resolver la relación activa por `componentRelationId`.
2. Resolver sus extremos persistidos y comprobar que pertenecen al mismo Data Product.
3. Resolver los extremos solicitados y aplicar la misma validación.
4. Exigir que la relación actual y la resultante pertenezcan al mismo Data Product; cambiar una relación hacia otro owner se rechaza en vez de autorizar sólo con el scope nuevo.
5. Autorizar contra el owner persistido y recién entonces actualizar y guardar.

### Delete

1. Resolver la relación activa.
2. Resolver source y destination persistidos, sin aceptar IDs cliente alternativos.
3. Comprobar same-DP y autorizar contra ese owner.
4. Recién entonces establecer `deletedAt/deletedBy` y guardar.

Las relaciones cross-DP devuelven error de validación y no generan llamada ACME ni escritura. Un recurso inexistente o una relación cuyos extremos no pueden verificarse falla cerrado.

## Contrato de pipeline

Cada caso de uso resuelve `DataProductModel` por el nombre del path y utiliza su `teamName + projectCode`. `PipelineAuthorizationService.assertWriteAccess`, basado en `DataProductAccessService.canAccess`, no participa en las rutas migradas porque sus compatibilidades históricas no implementan el contrato ACME exacto de SIG-616.

El orden común es:

1. Resolver Data Product y recursos necesarios para demostrar consistencia del path.
2. Autorizar `DEV_AND_UP` mediante `OperationAuthorizationService`.
3. Ejecutar validaciones de versión y precondiciones funcionales sin mutar estado antes del allow.
4. Recién entonces incrementar versiones, crear/eliminar componentes o relaciones, guardar snapshots, crear ejecuciones y despachar.

En `PipelineWriteServiceImpl`, el guard ocurre antes de `checkAndIncrementVersion`, `computeDiff` y cualquier `save`. En `PipelineDesignServiceImpl`, ocurre antes de mutar `designMetadata`. En `PipelineRelationsServiceImpl`, ocurre antes del version check que pueda incrementar y antes de `applyAdd/applyRemove`. En `ComponentCreateServiceImpl`, ocurre antes del duplicate pre-check, version increment y persistencia. Los pre-checks que sólo resuelven el target pueden preceder al guard; ningún detalle sensible del estado de la pipeline se devuelve a un caller no autorizado.

## Pipeline deploy

`PipelineDeployServiceImpl.deploy` resuelve Data Product, environment y pipeline desde persistencia, autoriza `DEV_AND_UP` y sólo después ejecuta:

- `DeploymentFreezeService.enforcePipelineDeploy` y el freeze por component types.
- Resolución de rollback configs.
- Cálculo y filtrado de deltas.
- Cálculo del desired-state hash e idempotency checks.
- Creación de `PipelineExecution` y `ComponentRun`.
- Enriquecimiento de services y dispatch por `DeploymentGroupService`.

La autorización se evalúa una vez para el Data Product completo antes de calcular los deltas `DEPLOY`, `UNDEPLOY` o `SKIP`. No se autoriza por componente ni se repite ACME dentro del loop.

## Identidad

Los handlers mutantes reciben username desde `Authentication`. Las firmas de los services incorporan ese username y dejan de invocar `TigerTokenService` en los caminos tocados. Los métodos de lectura que no forman parte de este slice conservan su contrato.

`PipelineTopologyController` puede mantener `TigerTokenService` mientras algún método de lectura no migrado lo necesite; las operaciones mutantes de esta SPEC no deben usarlo para revalidar la identidad.

## Decisiones de diseño

### DD-1: Same-DP se valida con modelos persistidos antes del guard

**Decisión**: Source y destination se resuelven desde `ComponentRepository`, se comprueba su Data Product real y sólo entonces se selecciona el scope de autorización.

**Fundamentación**: Los IDs del body son referencias de entrada, no ownership. Autorizar primero con `sourceDataProductId` cliente permitiría escoger un team conveniente y mutar una relación perteneciente a otro owner.

### DD-2: Update de relación no permite trasladar ownership

**Decisión**: La relación persistida y la relación resultante deben pertenecer al mismo Data Product.

**Fundamentación**: Autorizar únicamente el estado nuevo omite el permiso sobre el recurso que se está modificando; exigir permisos sobre dos owners agregaría un caso cross-DP que SIG-616 declara inválido.

### DD-3: Las rutas migradas consumen `OperationAuthorizationService` directamente

**Decisión**: Los services de esta SPEC invocan el autorizador común con `DEV_AND_UP`; no agregan un segundo guard de pipeline ni reutilizan `DataProductAccessService.canAccess`.

**Fundamentación**: `platformTeams` y `tempAllCanEdit` son compatibilidades históricas que no conceden autorización bajo SIG-616. Mantenerlas en el camino protegido crearía dos fuentes de policy.

### DD-4: Pipeline deploy se autoriza una vez antes del delta

**Decisión**: Un allow por Data Product precede el cálculo del delta y cubre todos los efectos de la ejecución.

**Fundamentación**: El pipeline es el recurso solicitado y todos sus componentes pertenecen al mismo Data Product. Autorizar cada delta multiplica llamadas ACME sin aumentar la precisión del scope.

## Archivos afectados

### Archivos modificados

| Archivo | Cambio |
|---|---|
| `controller/ComponentRelationController.java` | Pasar username autenticado. |
| `controller/PipelineTopologyController.java` | Pasar username a PUT, design, relations y component create. |
| `controller/PipelineDeploymentController.java` | Pasar username al pipeline deploy. |
| `service/ComponentRelationService.java` | Incorporar username a create/update/delete. |
| `service/PipelineWriteService.java` | Mantener username explícito y adoptar el guard común. |
| `service/PipelineDesignService.java` | Incorporar username. |
| `service/PipelineRelationsService.java` | Incorporar username. |
| `service/ComponentCreateService.java` | Reutilizar username autenticado para autorización y auditoría. |
| `service/PipelineDeployService.java` | Incorporar username. |
| `service/impl/ComponentRelationServiceImpl.java` | Same-DP, owner persistido y guard antes de save. |
| `service/impl/PipelineWriteServiceImpl.java` | `DEV_AND_UP` antes de versionado y escrituras. |
| `service/impl/PipelineDesignServiceImpl.java` | `DEV_AND_UP` antes de modificar diseño. |
| `service/impl/PipelineRelationsServiceImpl.java` | `DEV_AND_UP` antes de cambios de versión/relaciones. |
| `service/impl/ComponentCreateServiceImpl.java` | `DEV_AND_UP` antes de versionado y create. |
| `service/impl/PipelineDeployServiceImpl.java` | `DEV_AND_UP` antes de freeze, delta, ejecución y dispatch. |

### Tests modificados o nuevos

| Archivo | Cobertura esperada |
|---|---|
| `service/impl/ComponentRelationServiceImplTest.java` y `integration/ComponentRelationControllerIntegrationTest.java` | Create/update/delete, same-DP, owner persistido y ausencia de save. |
| `unit/service/PipelineWriteServiceImplTest.java` | Guard antes de versionado y persistencia. |
| `unit/service/PipelineDesignServiceImplTest.java` | Guard antes de mutar metadata. |
| `unit/service/PipelineRelationsServiceImplTest.java` | Guard, same-DP implícito y ausencia de version/save. |
| `unit/service/ComponentCreateServiceTest.java` y `integration/PipelineComponentCreateControllerIntegrationTest.java` | Guard antes de duplicate/version/save. |
| `unit/service/PipelineDeployServiceImplTest.java`, `integration/PipelineDeployControllerIntegrationTest.java` y `integration/PipelineDeployFlowIntegrationTest.java` | Guard antes de freeze/delta/lifecycle/dispatch. |

## Errores

| Condición | Respuesta |
|---|---|
| Tiger ausente o inválido | `401` desde Spring Security |
| Data Product, relation, component, environment o pipeline inexistente/inconsistente | `404` |
| Source y destination iguales o pertenecientes a Data Products diferentes | Error de validación sin llamada ACME ni side effects |
| Update intenta trasladar una relación a otro Data Product | Error de validación sin side effects |
| Scope owner incompleto | `403` fail-closed sin llamada ACME |
| Rol insuficiente, grant cruzado o ACME no verificable | `403` |
| Version conflict o precondición funcional posterior al allow | Conserva el status actual (`409`, `412` o `422`) |

## Observabilidad

- Reutilizar las causas de baja cardinalidad del autorizador y agregar `cross_data_product_relation` para rechazos locales de relaciones.
- No registrar username, token, grants ni headers Tiger.
- No registrar como mutation/deploy exitoso ningún request rechazado por autorización.
- Los logs de pipeline execution y dispatch sólo aparecen después del allow.

## Estrategia de pruebas y gate del PR

Los tests pertenecen al PR de este slice. El PR no queda listo para merge sin la matriz crítica verde y al menos 95% de coverage del código nuevo.

- Relaciones: allow para los cuatro roles `DEV_AND_UP`; deny para rol inferior, grant cruzado, scope incompleto y ACME fallido.
- Relaciones: create/update/delete same-DP; cross-DP; self-loop; extremos inexistentes; update que intenta cambiar de owner; delete con relación borrada.
- Ausencia de side effects: deny no llama `save`, `saveAll`, update de versión ni auditoría de delete.
- Pipeline: cada una de las cinco rutas invoca una sola vez el autorizador con el Data Product persistido.
- Pipeline: deny no llama `checkAndIncrementVersion`, `componentSaveHelper.save`, `applyAdd/applyRemove`, lifecycle, repositories de execution/run ni `DeploymentGroupService`.
- Pipeline deploy: allow conserva idempotencia, filtros, `force`, freezes y deltas; deny ocurre antes de todos ellos.
- Verificar que `platformTeams` y `tempAllCanEdit` no conceden acceso.
- Ejecutar regresión de pipeline component delete e inactivate para asegurar que continúan en `DEPLOYER_AND_UP`.
- Ejecutar integración HTTP de `401/403/404` y los status funcionales preexistentes.

## Gate de datos y rollout

Antes del rollout se mide la completitud de `teamName + projectCode` en los Data Products que poseen relaciones, pipelines activos o ejecuciones recientes. Los cross-DP existentes no se migran, pero deben cuantificarse para confirmar que el nuevo guard no intenta normalizarlos ni modificarlos accidentalmente.

El smoke no productivo incluye una relación same-DP permitida, una cross-DP rechazada y un pipeline deploy permitido/denegado con identidades reales. La evidencia forma parte del PR y no se posterga a otra fase.

Rollback: revert del PR. No hay migraciones de datos ni cambios en el contrato de eventos.

## Tasks ejecutables

1. Propagar username autenticado por controllers e interfaces de relaciones y pipeline.
2. Implementar same-DP y owner persistido en create/update/delete de `ComponentRelationServiceImpl`.
3. Reemplazar el acceso histórico por `OperationAuthorizationService + DEV_AND_UP` en PUT pipeline, design, relations y component create.
4. Integrar pipeline deploy antes de freeze, delta, lifecycle y dispatch.
5. Agregar tests unitarios e integración para allow/deny, cross-DP, resource consistency y cero side effects.
6. Ejecutar gate de datos, smoke no productivo, regresión focalizada y coverage como parte del mismo PR.

## Criterios de aceptación

- Create, update y delete de relaciones resuelven ambos extremos persistidos, exigen same-DP y autorizan `DEV_AND_UP` contra ese owner.
- Las cinco mutaciones de pipeline autorizan contra `teamName + projectCode` persistidos antes de modificar versiones, topología, relaciones, componentes o ejecuciones.
- Pipeline deploy se autoriza una vez antes de calcular deltas y no crea execution/run ni publica cuando rechaza.
- `platformTeams` y `tempAllCanEdit` no habilitan ninguna ruta protegida.
- Pipeline component delete e inactivate conservan `DEPLOYER_AND_UP`.
- Los tests, smoke y verificaciones de este slice se entregan en el mismo PR; no existe un gate final separado.

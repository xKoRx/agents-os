# SIG-616 — Slice 3: mutaciones y deployments de componentes

## Metadatos

- Tipo: Technical SPEC
- Estado inicial: Draft
- SPEC funcional: [SIG-621](https://spellbook.adminml.com/projects/SIG/specs/SIG-621)
- Requerimiento de origen: [SIG-616](https://spellbook.adminml.com/projects/SIG/specs/SIG-616)
- Dependencia: Slice 2 aprobado e implementado
- Aplicación: `rio-playmaker`

## Objetivo

Aplicar el autorizador común de operaciones a todas las mutaciones de componentes y a los flujos modernos de deploy y undeploy enumerados por SIG-616. Cada operación debe usar la identidad Tiger ya validada, resolver el Data Product y los recursos relacionados desde persistencia, exigir `DEV_AND_UP` sobre `teamName + projectCode` y autorizar antes de cualquier escritura, lock, llamada externa o dispatch.

La autorización pertenece a Playmaker. Materializer, Control Planes, KVS y BigQueue reciben trabajo sólo después de que Playmaker haya validado identidad, ownership, consistencia del recurso y rol ACME.

## Alcance

### Rutas protegidas

| Operación | Ruta | Caso de uso | Requisito |
|---|---|---|---|
| Crear componente | `POST /data-products/{dataProductId}/components` | `ComponentServiceImpl.create` | Tiger + `DEV_AND_UP` |
| Actualizar componente | `PUT /data-products/{dataProductId}/components/{componentId}` | `ComponentServiceImpl.update` | Tiger + `DEV_AND_UP` |
| Eliminar componente | `DELETE /data-products/{dataProductId}/components/{componentId}` | `ComponentServiceImpl.delete` | Tiger + `DEV_AND_UP` |
| Modificar diseño | `PATCH /data-products/{dataProductId}/components/{componentId}/design` | `ComponentServiceImpl.updateComponentDesign` | Tiger + `DEV_AND_UP` |
| Modificar code/template por ruta compatible | `PATCH /data-products/{dataProductId}/components/{componentId}/name/{name}/code/{code}/component_template/{component_template}` | `ComponentServiceImpl.updateNameCodeById` | Tiger + `DEV_AND_UP` |
| Deploy de componente | `POST /data-products/{dataProductId}/components/{componentId}/environments/{environmentId}/deployments` | `ComponentDeploymentServiceImpl.deploy` | Tiger + `DEV_AND_UP` |
| Undeploy de componente | `DELETE /data-products/{dataProductId}/components/{componentId}/environments/{environmentId}/deployments/{deploymentId}` | `ComponentDeploymentServiceImpl.undeploy` | Tiger + `DEV_AND_UP` |

La ruta compatible de modificación de `name/code/component_template` conserva su contrato mientras exista porque SIG-616 la enumera expresamente. Su retiro pertenece a una migración separada; estar marcada `@Deprecated` no la exime del guard.

### No incluye

- Relaciones entre componentes.
- Escrituras de pipeline, pipeline deploy o cambios de topología.
- Actions component-bound, precreation o service-level.
- Cambios en delete/inactivate de pipeline ya integrados con `DEPLOYER_AND_UP`.
- Nuevos roles, cache ACME, annotations, AOP o un motor genérico de policies.
- Cambios en contratos de eventos, tablas o payloads de Control Plane.

## Arquitectura objetivo

```text
HTTP request
  -> Spring Security / CustomAuthorizationFilter [UNCHANGED]
       publica username validado en Authentication.principal
  -> ComponentController o ComponentDeploymentController [MODIFIED]
       pasa username + headers al caso de uso
  -> repositorios Playmaker [UNCHANGED]
       resuelven DataProduct y recursos relacionados
  -> OperationAuthorizationService [UNCHANGED]
       require(username, teamName, projectCode, headers, DEV_AND_UP)
  -> caso de uso [MODIFIED]
       ejecuta persistencia, freeze checks, llamadas externas o dispatch
```

`OperationAuthorizationService` y `OperationAccessLevel.DEV_AND_UP` se consumen como fueron definidos por Slice 1. Este slice no agrega otra abstracción de autorización.

## Identidad y contrato interno

Los controllers obtienen `Authentication.getName()` y lo pasan como `username` a los services. Los services no vuelven a llamar `TigerTokenService`; los headers permanecen disponibles exclusivamente para la consulta ACME y para dependencias downstream que ya los requieren.

Las firmas conceptuales quedan así:

```java
ComponentResponseDTO create(
    String username,
    Map<String, String> headers,
    ComponentRequestDTO request,
    Long dataProductId);

ComponentDeploymentResponseDTO deploy(
    String username,
    Long dataProductId,
    Long componentId,
    Long environmentId,
    Long definitionId,
    Map<String, String> headers);
```

Las demás mutaciones siguen la misma regla: identidad explícita, scope persistido y headers sólo como transporte hacia ACME o integraciones ya existentes.

## Orden obligatorio de las mutaciones de componentes

1. Spring Security valida Tiger y publica username.
2. El service resuelve un Data Product activo por `dataProductId`.
3. Cuando existe `componentId`, resuelve un componente activo y comprueba que pertenece al Data Product del path.
4. Invoca `OperationAuthorizationService.require` con `teamName`, `projectCode` y `DEV_AND_UP`.
5. Ejecuta las validaciones funcionales propias de la operación.
6. Recién entonces escribe el componente o invoca servicios con efectos laterales.

En create, el Data Product se resuelve y autoriza antes de mapear y persistir tanto componentes nuevos como importados. En delete, la autorización ocurre antes de cancelar autorizaciones de importación, invalidar autorizaciones, modificar auditoría o guardar el soft delete. En update y patches, la autorización ocurre antes de mutar el modelo o ejecutar queries de update.

La ruta `PATCH .../name/{name}/code/{code}/component_template/{component_template}` debe resolver primero el componente y comprobar su pertenencia al Data Product; no puede delegar directamente en `componentRepository.updateNameCodeById` porque ese update no constituye por sí solo una validación de resource consistency.

## Orden obligatorio de deploy y undeploy

1. Resuelve el componente y comprueba que pertenece al Data Product del path.
2. Resuelve el environment o el slot de servicio y comprueba que pertenece al mismo componente y Data Product.
3. En undeploy, resuelve el deployment y comprueba que pertenece al slot esperado.
4. Autoriza `DEV_AND_UP` contra el Data Product persistido.
5. Ejecuta freeze checks, `findOrCreate`, creación de deployment, undeploy o dispatch.

Un path con IDs existentes pero incompatibles se rechaza igual que un recurso no encontrado y nunca llega al autorizador con ownership inferido del request. La autorización no se obtiene desde `definitionId`, `serviceId`, headers de negocio ni ningún campo cliente.

## Decisiones de diseño

### DD-1: Autorizar dentro del caso de uso después de resolver el target persistido

**Decisión**: Cada service resuelve el Data Product y la jerarquía del recurso y luego invoca `OperationAuthorizationService` antes del primer efecto lateral.

**Fundamentación**: El controller no tiene una fuente confiable para `teamName` y `projectCode`, y un interceptor genérico no puede verificar que component, environment, slot y deployment forman la jerarquía indicada por el path. El service ya posee los repositorios y el punto exacto anterior a los efectos.

### DD-2: Reutilizar el principal de Spring Security en todos los entrypoints tocados

**Decisión**: `ComponentController` y `ComponentDeploymentController` pasan username desde `Authentication`; `ComponentServiceImpl` y `ComponentDeploymentServiceImpl` dejan de resolverlo nuevamente con `TigerTokenService`.

**Fundamentación**: Tiger ya fue validado en la frontera HTTP. Revalidarlo agrega llamadas, duplica errores y permite que dos capas discrepen sobre la identidad usada para autorizar y auditar.

### DD-3: Mantener `DEV_AND_UP` para estas operaciones

**Decisión**: Las siete rutas usan `DEV_AND_UP`. La excepción `DEPLOYER_AND_UP` continúa limitada a pipeline component delete e inactivate.

**Fundamentación**: SIG-616 define estas mutaciones para `admin`, `maintainer`, `deployer` y `committer`. Extender la excepción de los consumidores preexistentes cambiaría el contrato funcional sin un requerimiento que lo respalde.

## Archivos afectados

### Archivos modificados

| Archivo | Cambio |
|---|---|
| `controller/ComponentController.java` | Obtener username autenticado y pasarlo a cada mutación. |
| `controller/ComponentDeploymentController.java` | Obtener username autenticado para deploy y undeploy. |
| `service/ComponentService.java` | Incorporar username a las firmas mutantes. |
| `service/ComponentDeploymentService.java` | Incorporar username a deploy y undeploy. |
| `service/impl/ComponentServiceImpl.java` | Resolver scope persistido, exigir `DEV_AND_UP` y retirar revalidación Tiger de los flujos tocados. |
| `service/impl/ComponentDeploymentServiceImpl.java` | Validar jerarquía completa y autorizar antes de freeze/deployment/undeploy. |

### Tests modificados o nuevos

| Archivo | Cobertura esperada |
|---|---|
| `controller/ComponentControllerTest.java` y/o `unit/controller/ComponentControllerTest.java` | Propagación del principal y contratos HTTP existentes. |
| `controller/ComponentDeploymentControllerTest.java` | Propagación del principal en deploy y undeploy. |
| `service/impl/ComponentServiceImplTest.java` | Matriz allow/deny, pertenencia y ausencia de side effects. |
| `service/impl/ComponentDeploymentServiceImplTest.java` | Jerarquía DP/component/environment/deployment y orden del guard. |
| `integration/ComponentControllerIntegrationTest.java` | Protección efectiva de las cinco rutas de componente. |
| `integration/DeploymentControllerTest.java` y `integration/UndeployControllerTest.java` | `401/403/404`, allow y no dispatch en deny. |

No se agregan archivos productivos nuevos salvo que la implementación necesite un helper privado para evitar duplicación local dentro de una de las dos clases.

## Errores

| Condición | Respuesta |
|---|---|
| Tiger ausente, malformado, inválido o expirado | `401` desde Spring Security |
| Data Product, componente, environment, slot o deployment inexistente/inconsistente | `404` sin llamada ACME cuando todavía no existe un target confiable |
| `teamName`, `projectCode` o username nulo/blanco | `403` fail-closed y sin llamada ACME |
| Grant ausente, insuficiente o de otro team/project | `403` |
| ACME no verificable | `403` fail-closed con causa distinguible en observabilidad |
| Validación funcional posterior al allow | Conserva el status actual de la operación |

Las respuestas no exponen grants, miembros de equipo, tokens ni detalles internos de ACME.

## Observabilidad

- Registrar el resultado de autorización mediante las causas de baja cardinalidad existentes en `OperationAuthorizationService`.
- No registrar username, Bearer token, payloads de grants ni headers Tiger.
- Mantener logs de creación, update, delete, deploy y undeploy sólo después de una autorización exitosa cuando describan un efecto realizado.
- Las métricas actuales de negocio no registran éxito cuando el guard rechaza la operación.

## Estrategia de pruebas y gate del PR

Los tests pertenecen al PR de este slice. El PR no queda listo para merge si la matriz crítica de esta SPEC no está verde y el código nuevo no alcanza al menos 95% de coverage.

- Permitir cada ruta con `admin`, `maintainer`, `deployer` y `committer` del team + project exactos.
- Rechazar roles inferiores, no miembros, grant de otro team, grant de otro project, scope incompleto y error ACME.
- Verificar `401` sin invocar controllers cuando Tiger no produce identidad válida.
- Verificar `404` para component ajeno al Data Product, environment ajeno, slot ajeno y deployment ajeno al slot.
- Verificar que deny/error no llama `save`, query de update, cancelación/invalidation de importaciones, freeze service, `findOrCreate`, `v2Create` ni `undeploy`.
- Verificar que allow ejecuta una sola llamada lógica al autorizador y conserva la respuesta, auditoría y eventos existentes.
- Cubrir create normal e importado; update; delete; design patch; patch compatible; deploy con `definitionId` implícito y explícito; undeploy.
- Ejecutar regresión focalizada de los tests existentes de componentes, deploy y undeploy.

## Gate de datos y rollout

Antes de habilitar el PR se debe medir cuántos Data Products alcanzados por estas rutas carecen de `teamName` o `projectCode` y comprobar que el `projectCode` persistido coincide exactamente con ACME. El resultado aceptable es cero registros afectados o una remediación/aceptación explícita antes del rollout; no se implementa fallback permisivo.

El PR incluye un smoke no productivo con un Data Product real y dos identidades: una `DEV_AND_UP` que permite y otra sin grant que rechaza. El smoke prueba al menos una mutación de componente y un deploy o undeploy sin convertir ACME live en dependencia de CI.

Rollback: revert completo del PR. No hay migraciones de datos, cambios de schema ni cambios en contratos de eventos.

## Tasks ejecutables

1. Propagar username autenticado por los controllers e interfaces de componentes y deployments.
2. Integrar `OperationAuthorizationService` con `DEV_AND_UP` en las cinco mutaciones de `ComponentServiceImpl`.
3. Cerrar la validación de pertenencia en la ruta compatible de `name/code/component_template` antes del update directo.
4. Integrar el guard y la jerarquía completa en deploy y undeploy antes de efectos laterales.
5. Agregar la matriz unitaria e integración HTTP, verificar ausencia de efectos y alcanzar al menos 95% de coverage nuevo.
6. Ejecutar gate de datos, smoke no productivo y regresión focalizada como evidencia del mismo PR.

## Criterios de aceptación

- Las siete rutas enumeradas exigen Tiger + `DEV_AND_UP` contra el owner persistido del Data Product.
- Ninguna ruta autoriza con team, project, role o ownership provenientes del request.
- Component, environment, slot y deployment se validan contra la jerarquía persistida antes de autorizar.
- Todo rechazo ocurre antes de persistencia, freeze checks con efectos, llamadas externas o dispatch.
- La identidad se valida una vez en la frontera HTTP y se reutiliza para autorización y auditoría.
- Los tests y gates de este slice se entregan dentro del mismo PR; no existe una fase posterior de pruebas.

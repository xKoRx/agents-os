# SIG-616 — Slice 5: Actions restantes

## Metadatos

- Tipo: Technical SPEC
- Estado inicial: Draft
- SPEC funcional: [SIG-621](https://spellbook.adminml.com/projects/SIG/specs/SIG-621)
- Requerimiento de origen: [SIG-616](https://spellbook.adminml.com/projects/SIG/specs/SIG-616)
- Dependencia: Slice 4 aprobado e implementado
- Aplicación: `rio-playmaker`

## Objetivo

Completar la allow-list server-side de Actions definida por SIG-616. Las Actions mutantes de Flink y ClickHouse exigen un componente de origen persistido y `DEV_AND_UP`; las Actions de lectura declaradas requieren Tiger válido pero no membership ACME; toda combinación desconocida de `component_type + actionName` se rechaza antes de KVS, BigQueue o llamadas directas a Control Plane.

Este slice extiende el mecanismo incorporado para Signals sin convertirlo en un motor genérico de policies. La clasificación es una tabla finita, exacta y propiedad de Playmaker.

## Alcance

### Matriz component-bound

| Tipo persistido | Action | Clasificación | Requisito |
|---|---|---|---|
| `catalog-signal` | `start`, `stop` | Mutante | Tiger + `DEV_AND_UP`; ya cubierto por Slice 2 |
| `flink-sql` | `start`, `stop` | Mutante | Tiger + origen + `DEV_AND_UP` |
| `flink-job` | `start`, `stop` | Mutante | Tiger + origen + `DEV_AND_UP` |
| `aws-flink-sql` | `start`, `stop` | Mutante | Tiger + origen + `DEV_AND_UP` |
| `aws-flink-job` | `start`, `stop` | Mutante | Tiger + origen + `DEV_AND_UP` |
| `clickhouse-mat-view` | `start-materialized-view`, `stop-materialized-view` | Mutante | Tiger + origen + `DEV_AND_UP` |
| `aws-msk-topic` | `peek` | Lectura | Tiger |
| `gcp-kafka-topic` | `peek` | Lectura | Tiger |
| `kafka-topic` | `peek` | Lectura | Tiger |
| `clickhouse-mergetree` | `execute-query`, `describe-table`, `list-warehouse`, `list-warehouses-for-team`, `list-database`, `list-tables` | Lectura | Tiger |

La comparación de tipo y Action es exacta, case-sensitive y sin trim, aliases ni normalización. `component_type` proviene de `ComponentModel.componentTemplateCode` para component-bound. Un par no presente en la tabla es `DENY`, aunque el Control Plane sea capaz de procesarlo.

`list-warehouses-for-team` no es una expansión por simetría: `fury_rio-controlplane-clickhouse` lo registra como `ClickHouseActionContract.ACTION_LIST_WAREHOUSES`, `ListWarehousesAction.supportedAction()` aún lo atiende y su deprecación indica mantenerlo hasta que Playmaker migre. Además, `fury_rio-frontend/api/services/warehouses.ts#dispatchWarehouseLookup` invoca ese literal contra Playmaker. Se conserva como alias legacy explícito de lectura junto a `list-warehouse` para no convertir un consumidor existente en `DENY`.

### Matriz precreation

| Par solicitado | Resultado |
|---|---|
| Cualquier par clasificado como mutante | `403`, sin ACME, KVS ni BigQueue |
| Par de lectura incluido en la allow-list | Tiger-only; conserva el flujo de precreation |
| Par desconocido | `403`, sin KVS ni BigQueue |

El `component_type` cliente sólo se usa para clasificar. Nunca concede ownership, rol ni permiso mutante. Una Action mutante no puede ejecutarse en precreation porque no existe componente persistido cuyo origen y owner puedan verificarse.

### Service-level read

`POST /services/{serviceId}/actions/peek` permanece Tiger-only. `ServiceActionsServiceImpl.peekMessages` resuelve el `ServiceModel` y su deployment antes de invocar Kafka Control Plane. La ruta tiene una Action fija y no consulta ACME; un `serviceId` inexistente o sin deployment válido conserva su `404` actual.

### No incluye

- Nuevas Actions fuera de la matriz anterior.
- `ping`, porque no forma parte de la allow-list declarada por SIG-616.
- `POST /services/{serviceId}/actions/code`, que requiere una SPEC funcional/técnica propia por ser una mutación activa fuera del inventario original.
- Cambios en long polling, `ActionKvsEntry`, callbacks, visibilidad de resultados o TTL.
- Autorización en los Control Planes.
- Cache ACME, annotations, AOP, expressions o registry dinámico.

## Arquitectura objetivo

```text
ActionController [MODIFIED]
  -> username desde Authentication
  -> ActionServiceImpl [MODIFIED]
       resuelve target persistido cuando existe
       ActionAuthorizationPolicy [NEW, local y finita]
         (componentTemplateCode, actionName) -> MUTATING | READ | DENY
       MUTATING -> origen persistido + OperationAuthorizationService DEV_AND_UP
       READ -> Tiger ya validado, sin ACME
       DENY -> 403
       allow -> deployment context -> KVS -> BigQueue

ServiceActionsController / ServiceActionsServiceImpl [MODIFIED]
  -> peek fijo -> Tiger-only -> Kafka Control Plane

Control Planes [UNCHANGED]
```

## Contrato de clasificación

La clasificación se representa con una estructura cerrada y sin configuración externa:

```java
enum ActionAccess {
  MUTATING,
  READ
}

record ActionKey(String componentType, String actionName) {}

Map<ActionKey, ActionAccess> ACTION_POLICY;
```

La ausencia de una clave equivale a `DENY`; no existe valor `UNKNOWN_ALLOW`. La estructura puede vivir como tipos privados de `ActionServiceImpl` o en una clase package-private `ActionAuthorizationPolicy` si el test unitario directo reduce complejidad. No se expone como bean extensible ni se carga desde properties.

`catalog-signal + start|stop` se mueve a la misma tabla para que exista una sola clasificación server-side. El comportamiento de Slice 2 no cambia.

## Orden component-bound obligatorio

1. Tiger valida y publica username en la frontera HTTP.
2. `fetchComponentInHierarchy` resuelve Data Product, componente y environment y conserva `404` ante inconsistencias.
3. La policy clasifica usando `component.getComponentTemplateCode()` y `actionName`.
4. Si es `DENY`, retorna `403` sin consultar ACME ni cargar deployment context.
5. Si es `MUTATING`, verifica `ImportAuthorizationRepository.existsApprovedByImportedComponentId(componentId)` y rechaza componentes importados.
6. Si es `MUTATING`, exige `DEV_AND_UP` contra `teamName + projectCode` persistidos.
7. Si es `READ`, no consulta importación ni ACME.
8. Sólo después del allow resuelve deployment context, guarda KVS y publica BigQueue.

Un `sourceComponentId` de migración sin autorización de importación aprobada no convierte al componente en importado. La única fuente para esa decisión es `ImportAuthorizationRepository`.

## Orden precreation obligatorio

1. Tiger valida y publica username.
2. Se resuelve el Data Product para conservar el `404` actual.
3. La policy clasifica el par exacto recibido.
4. `MUTATING` o ausencia de policy retorna `403` sin ACME ni efectos.
5. `READ` continúa por el flujo existente y publica con `component_template = componentType`.

No se consulta `OperationAuthorizationService` en precreation. Un input cliente nunca puede transformar una Action mutante en lectura porque la policy usa pares exactos.

## Service-level Kafka peek

La ruta fija `/services/{serviceId}/actions/peek` obtiene su identidad de Spring Security y no revalida Tiger en `ServiceActionsServiceImpl`. Antes de llamar `KafkaControlPlaneClient.peek`, resuelve el service y el deployment que contiene el topic real. Al ser read allow-listed no exige ACME y puede operar sobre un componente importado.

Los headers Tiger se propagan a Kafka Control Plane por el contrato existente; no se interpretan para ownership dentro de ese cliente.

## Decisiones de diseño

### DD-1: Una tabla exacta de pares en vez de reglas por nombre

**Decisión**: La policy se indexa por `ActionKey(componentType, actionName)`.

**Fundamentación**: `start/stop` existe en Signals y Flink con payloads y efectos distintos; `peek` también puede aparecer en más de una tecnología. Una regla basada sólo en `actionName` amplía permisos cuando se incorpora un tipo nuevo.

### DD-2: Ausencia de policy significa deny

**Decisión**: Todo par no enumerado retorna `403` antes de side effects.

**Fundamentación**: La capacidad de un Control Plane no es una concesión de autoridad. Una Action nueva debe entrar mediante una SPEC que la clasifique explícitamente.

### DD-3: Read Actions no consultan ACME

**Decisión**: Los pares `READ` requieren Tiger válido y resource consistency, pero no membership del owner.

**Fundamentación**: SIG-616 concede las lecturas allow-listed a toda identidad Tiger válida. Consultar ACME por precaución cambiaría el contrato funcional y bloquearía lecturas legítimas sobre componentes importados.

### DD-4: La allow-list permanece estática y local

**Decisión**: La policy se versiona con Playmaker y no se descubre desde Control Planes, properties o base de datos.

**Fundamentación**: Una fuente dinámica puede ampliar permisos sin review de código y separar la autorización del deploy que la aplica. La matriz actual es pequeña y finita.

## Archivos afectados

### Archivo nuevo opcional

| Archivo | Propósito |
|---|---|
| `service/ActionAuthorizationPolicy.java` | Encapsular la tabla exacta si mantenerla privada en `ActionServiceImpl` dificulta el test directo. |

### Archivos modificados

| Archivo | Cambio |
|---|---|
| `service/impl/ActionServiceImpl.java` | Clasificación completa, default deny, mutating/read e importados. |
| `controller/ServiceActionsController.java` | Reutilizar principal Tiger validado en service-level peek. |
| `service/ServiceActionsService.java` | Incorporar username sólo si el contrato de auditoría lo necesita; no para ACME. |
| `service/impl/ServiceActionsServiceImpl.java` | Mantener peek Tiger-only y sin revalidación de identidad. |

### Tests modificados o nuevos

| Archivo | Cobertura esperada |
|---|---|
| `service/impl/ActionServiceImplTest.java` | Matriz completa, imported/origin, precreation y ausencia de efectos. |
| `controller/ActionControllerTest.java` | Propagación de identidad y contratos existentes. |
| `integration/ActionPreCreationIntegrationTest.java` | Read allow, mutating deny y unknown deny. |
| `integration/SignalsControllerIntegrationTest.java` | Regresión de Signals `start/stop`. |
| `controller/ServiceActionsControllerTest.java`, `service/impl/ServiceActionsServiceImplTest.java` y `integration/ServiceActionsControllerIntegrationTest.java` | Kafka peek Tiger-only, resource lookup y ausencia de ACME. |

No se modifican `ActionsTriggerProducer`, `ActionKvsRepository`, DTOs de eventos ni Control Planes.

## Errores

| Condición | Respuesta |
|---|---|
| Tiger ausente o inválido | `401` desde Spring Security |
| Data Product, componente, environment, service o deployment inexistente/inconsistente | `404` |
| Par `component_type + actionName` desconocido | `403` sin ACME ni side effects |
| Action mutante en precreation | `403` sin ACME ni side effects |
| Componente importado intenta Action mutante | `403` |
| Scope incompleto, rol insuficiente, grant cruzado o ACME no verificable en mutación | `403` |
| Read allow-listed | No consulta ACME; conserva errores funcionales posteriores |
| Deployment activo inexistente después del allow | `409` actual |

## Observabilidad

- Reutilizar `unknown_action_pair`, `imported_component`, `invalid_scope`, `insufficient_role` y `acme_unavailable` como causas de baja cardinalidad.
- Registrar clasificación como `mutating`, `read` o `deny`, sin username, token, payload ni grants.
- No registrar SQL, datos de Action ni outputs de Kafka/ClickHouse en logs de autorización.
- Mantener logs de dispatch sólo después del allow.

## Estrategia de pruebas y gate del PR

Los tests pertenecen al PR de este slice. El PR no queda listo para merge sin la matriz completa de pares, los caminos críticos de seguridad y al menos 95% de coverage del código nuevo.

- Test parametrizado de cada par exacto de la matriz y de variantes de case, espacios, alias y nombre correcto con tipo incorrecto.
- Cada Action mutante permite los cuatro roles `DEV_AND_UP` y rechaza rol inferior, no miembro, grant cruzado, scope incompleto y error ACME.
- Cada Action mutante rechaza un componente importado aprobado; un `sourceComponentId` sin import authorization aprobada continúa como origin.
- Cada read allow-listed funciona con Tiger válido sin invocar ACME y también sobre componente importado.
- Precreation permite sólo reads de la tabla; mutating y unknown no guardan KVS ni publican BigQueue.
- Component-bound deny no llama `fetchDeploymentContext`, KVS ni producer; allow guarda una vez y publica una vez.
- Kafka service-level peek valida service/deployment, no llama ACME y no cambia el contrato del Control Plane.
- Regresión de Signals `catalog-signal + start|stop`, polling, callbacks y result visibility.
- Integración HTTP para `401/403/404/409` y `202` en los pares permitidos.

## Rollout

Antes de habilitar el PR se obtiene un inventario de `componentTemplateCode + actionName` observado para confirmar que no existen pares productivos legítimos fuera de la allow-list. El gate debe buscar `ping` explícitamente: si tiene consumidores reales, el PR no se habilita hasta decidir su incorporación o migración en la SPEC funcional. Cualquier otro par adicional sigue la misma regla; no se agrega un fallback permisivo.

El smoke no productivo cubre al menos una mutación Flink o ClickHouse permitida, la misma operación con identidad sin grant, un componente importado rechazado, una lectura ClickHouse Tiger-only y Kafka peek. La evidencia se adjunta al mismo PR.

Rollback: revert del PR. No hay migraciones de datos ni cambios de eventos.

## Tasks ejecutables

1. Implementar la tabla exacta `ActionKey -> ActionAccess` y mover Signals al clasificador único.
2. Integrar Flink y ClickHouse mutantes con origin check y `DEV_AND_UP` antes de side effects.
3. Integrar las Actions de lectura component-bound y precreation sin ACME.
4. Aplicar default deny a todo par desconocido y cerrar todos los bypass de precreation.
5. Verificar Kafka service-level peek como Tiger-only con resource consistency.
6. Ejecutar matriz parametrizada, integración HTTP, smoke, inventario de pares y coverage dentro del mismo PR.

## Criterios de aceptación

- La tabla server-side contiene todos y sólo los pares declarados por SIG-616.
- Flink y ClickHouse mutantes exigen componente origin persistido y `DEV_AND_UP` exacto.
- Reads allow-listed requieren Tiger válido, permiten componentes importados y no consultan ACME.
- Precreation deniega toda mutación y todo par desconocido antes de KVS/BigQueue.
- Un Action nuevo o una combinación tipo/Action desconocida falla cerrado.
- Signals, polling, callbacks y contratos de eventos conservan su comportamiento.
- Los tests, inventario y smoke de este slice forman parte del mismo PR; no existe un gate final separado.

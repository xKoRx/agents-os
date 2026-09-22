# Technical Specification — Slice 2: autorización de Actions mutantes de Signals

**Feature**: SIG-616 / Slice 2  
**Owner**: rjara  
**Project**: Signals (`rio-playmaker`)  
**Status**: Review  
**Deriva de**: [SIG-621 — Autorización de operaciones por equipo](https://spellbook.adminml.com/projects/SIG/specs/SIG-621)

## Objetivo

Agregar una validación de autorización a las Actions component-bound existentes `catalog-signal + start|stop`, usando la identidad Tiger validada y el ownership persistido del Data Product. La autorización ocurre antes de resolver deployment context, guardar el estado `PENDING` en KVS o publicar en BigQueue.

El cambio es aditivo: no crea Actions, endpoints ni estados; tampoco cambia el comportamiento de pares no configurados, componentes importados, precreation, polling o Actions de lectura.

## Arquitectura

```text
CustomAuthorizationFilter [MODIFIED]
  └── valida Tiger una vez
      └── TigerUsernameAuthentication [NEW]
          └── principal = username; nunca Bearer token

ActionController / ActionResultController [MODIFIED]
  └── pasan Authentication.getName()
      └── ActionService [MODIFIED]
          └── una firma por operación, con username explícito
              └── ActionServiceImpl [MODIFIED]
                  ├── resuelve jerarquía persistida [UNCHANGED]
                  ├── ActionAuthorizationService [NEW]
                  │   └── ActionPermissionProvider [NEW PORT]
                  │       └── ConfiguredActionPermissionProvider [NEW ADAPTER]
                  │           └── app.action-authorization.permissions [NEW CONFIG]
                  └── deployment context → KVS → BigQueue [UNCHANGED]

OperationAuthorizationService [UNCHANGED, SLICE 1]
  └── team + project + access level → ACME
```

## Contrato de configuración

La fuente inicial de permisos es la configuración activa de Spring:

```yaml
app:
  action-authorization:
    permissions:
      - component-type: catalog-signal
        action: start
        access-level: DEV_AND_UP
      - component-type: catalog-signal
        action: stop
        access-level: DEV_AND_UP
```

`application.yml` entrega el valor común y cualquier `application-{scope}.yml` puede reemplazar la lista para su scope. La comparación de `component-type` y `action` es exacta, case-sensitive y sin normalización.

`ActionPermissionProvider` expone:

```java
Optional<OperationAccessLevel> findAccessLevel(
    String componentType,
    String actionName);
```

La ausencia de configuración significa “sin validación ACME adicional”; el caso de uso continúa con su comportamiento existente.

## Comportamiento

### Actions component-bound

| Tipo persistido | Action | Resultado adicional |
|---|---|---|
| `catalog-signal` | `start` | Requiere `DEV_AND_UP` |
| `catalog-signal` | `stop` | Requiere `DEV_AND_UP` |
| Cualquier tipo | Cualquier otro nombre | Ninguna regla nueva |

`DEV_AND_UP` permite los roles `admin`, `maintainer`, `deployer` y `committer` sobre el team y project persistidos del Data Product.

Los componentes importados siguen la misma tabla. El slice no agrega una condición de importación ni consulta `ImportAuthorizationRepository`.

### Precreation y polling

`triggerPreCreationAction` mantiene su comportamiento y no consulta `ActionAuthorizationService`, porque no existe un componente persistido al cual aplicar la configuración component-bound. `getActionResult` conserva sus reglas de acceso y polling; recibe el username validado por la frontera y no ejecuta una segunda validación Tiger.

## Orden obligatorio

1. `CustomAuthorizationFilter` valida Tiger y publica el username.
2. `ActionController` pasa `Authentication.getName()` a `ActionService`.
3. `ActionServiceImpl` resuelve Data Product, componente y environment persistidos; inconsistencias conservan el `404` existente.
4. `ActionAuthorizationService` consulta `ActionPermissionProvider` con `component.getComponentTemplateCode()` y `actionName`.
5. Si no existe configuración, el flujo continúa sin una validación nueva.
6. Si existe configuración, `OperationAuthorizationService` valida username, team, project y access level.
7. Sólo después de un allow se resuelven deployment context, KVS y BigQueue.

Una denegación o error ACME en el paso 6 produce `403` antes de los side effects.

## Identidad Tiger

`CustomAuthorizationFilter` es la única capa que interpreta el Bearer token. Con Tiger válido crea `TigerUsernameAuthentication`; con token ausente, malformado, inválido, expirado o username vacío continúa sin `Authentication`. `SecurityConfig` decide si la ruta es `permitAll` o `.authenticated()` y responde `401` mediante su `AuthenticationEntryPoint`.

`ActionService` conserva headers porque `AcmeClient` necesita propagarlos, pero la identidad de negocio llega siempre como `username`. No existe un overload que vuelva a derivar el usuario desde headers dentro del service.

## Design Decisions

### DD-1: Una sola identidad explícita en `ActionService`

**Decisión**: todas las operaciones de `ActionService` reciben username y no conservan overloads que revaliden Tiger.

**Fundamentación**: `ActionService` es una interfaz interna del único módulo de Playmaker y todos sus consumidores productivos se migran en el mismo cambio. Mantener dos caminos permitiría identidades distintas entre filtro y service y prolongaría una API obsoleta sin compatibilidad externa que preservar.

### DD-2: Puerto estable con adapter de configuración

**Decisión**: `ActionAuthorizationService` depende de `ActionPermissionProvider`; `ConfiguredActionPermissionProvider` es la implementación inicial.

**Fundamentación**: la matriz debe variar por scope y, posteriormente, puede provenir de Discovery. El puerto evita acoplar los consumidores al mecanismo de carga. No se agregan jobs, cache, bootstrap dinámico ni selector de fuente hasta que exista ese requerimiento.

**Alternativa descartada**: constantes en `ActionServiceImpl`. Acoplan el caso de uso genérico a tipos de componente concretos y obligan a modificar consumidores cuando cambie la fuente.

### DD-3: Autorización aditiva, sin clasificación global

**Decisión**: sólo un par configurado activa ACME; un par ausente no se clasifica como read, mutating ni deny.

**Fundamentación**: la iniciativa agrega validaciones a operaciones existentes. Un default-deny, una whitelist completa o el rechazo de precreation/imports modificarían reglas de negocio no definidas por este slice.

## Archivos afectados

### Archivos nuevos

| Archivo | Propósito |
|---|---|
| `filter/TigerUsernameAuthentication.java` | Principal Tiger con username |
| `service/ActionAuthorizationService.java` | Aplica el access level resuelto antes de side effects |
| `service/ActionPermissionProvider.java` | Puerto independiente de la fuente de permisos |
| `config/ConfiguredActionPermissionProvider.java` | Adapter de `@ConfigurationProperties` |

### Archivos modificados

| Archivo | Cambio |
|---|---|
| `filter/CustomAuthorizationFilter.java` | Publica username y no token |
| `config/SecurityConfig.java` | Mantiene la decisión de autenticación HTTP |
| `controller/ActionController.java` | Propaga username autenticado |
| `controller/ActionResultController.java` | Propaga username autenticado |
| `service/ActionService.java` | Firmas internas con username explícito |
| `service/impl/ActionServiceImpl.java` | Delega autorización sin reglas Signals ni Tiger parsing |
| `src/main/resources/application.yml` | Configura `catalog-signal start/stop` |

No cambian DTOs, eventos, `ActionKvsRepository`, `ActionsTriggerProducer` ni Control Planes.

## Manejo de errores

| Condición | Resultado |
|---|---|
| Tiger ausente o inválido en ruta autenticada | `401` desde Spring Security |
| Jerarquía persistida inexistente o inconsistente | `404` existente |
| Par configurado con scope incompleto, grant insuficiente o ACME no verificable | `403`, sin KVS ni BigQueue |
| Par no configurado | Comportamiento existente |
| Deployment activo inexistente luego de autorizar | `409` existente |

Las respuestas y logs no exponen token, grants ni miembros del equipo.

## Estrategia de tests

- Binding de `component-type`, `action` y `access-level` mediante `@ConfigurationProperties`.
- Resolución exacta de pares configurados y no configurados.
- Propagación de username desde filtro y controllers; ausencia de una segunda validación Tiger.
- `catalog-signal start/stop` con `DEV_AND_UP` y denegación antes de side effects.
- Par no configurado, componente importado y precreation conservan el comportamiento existente.
- Polling conserva algoritmo, timeout y control de acceso.
- Suite completa de `rio-playmaker` mediante `./gradlew check`.

El smoke no productivo debe cubrir una operación autorizada, la misma operación denegada y un par no configurado con Tiger/ACME reales. No forma parte de la suite automatizada.

## Rollout y rollback

Los scopes heredan la lista base y pueden reemplazarla en `application-{scope}.yml`. Antes de rollout se valida que los Data Products target tengan `teamName + projectCode` coherentes con ACME.

Rollback: revertir el slice o retirar las entradas del scope correspondiente. No hay migraciones de datos ni cambios de contrato de eventos.

## Fuera de alcance

- Crear Actions, endpoints o casos de uso.
- Rechazar componentes importados o inferir ownership desde su origen.
- Modificar precreation, lecturas, polling, callbacks o visibilidad de resultados.
- Configurar Flink o ClickHouse; pertenecen a slices posteriores.
- Implementar Discovery, jobs, cache o refresh dinámico del provider.
- Migrar usos de `TigerTokenService` ajenos a `ActionService`.

## Criterios de aceptación

- Tiger publica username y nunca el Bearer token como principal.
- Todos los consumidores productivos de `ActionService` usan las firmas con username.
- `ActionServiceImpl` no depende de `TigerTokenService` ni contiene constantes Signals.
- La configuración activa determina el access level de cada par exacto.
- `catalog-signal start/stop` exige `DEV_AND_UP` antes de side effects.
- Un par no configurado, un componente importado y precreation conservan su comportamiento previo.
- La fuente de permisos puede reemplazarse implementando `ActionPermissionProvider` sin modificar consumidores.

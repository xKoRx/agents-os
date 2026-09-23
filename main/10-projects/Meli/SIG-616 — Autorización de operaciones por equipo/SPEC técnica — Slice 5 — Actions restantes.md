# Technical Specification — Slice 5: configuración de Actions mutantes restantes

**Feature**: SIG-616 / Slice 5  
**Owner**: rjara  
**Project**: Signals (`rio-playmaker`)  
**Status**: Review  
**Deriva de**: [SIG-621 — Autorización de operaciones por equipo](https://spellbook.adminml.com/projects/SIG/specs/SIG-621)

## Objetivo

Configurar autorización `DEV_AND_UP` para las Actions mutantes existentes de Flink y ClickHouse materialized views. Slice 5 reutiliza el mecanismo config-backed de Slice 2 y no agrega lógica al caso de uso genérico. Las reglas Flink se expresan por familia abstracta en YAML y los tipos concretos se declaran como miembros de esa familia.

El cambio es aditivo: no crea Actions, no clasifica lecturas, no rechaza pares desconocidos y no modifica precreation, imports, polling, eventos ni Control Planes.

## Arquitectura

```text
ActionServiceImpl [UNCHANGED]
  └── ActionAuthorizationService [UNCHANGED]
      └── ActionPermissionProvider [PORT; DOCUMENTATION UPDATED]
          └── ConfiguredActionPermissionProvider [FAMILY RESOLUTION ADDED]
              └── app.action-authorization [YAML: permissions, component-families, family-permissions]

OperationAuthorizationService [UNCHANGED]
  └── DEV_AND_UP antes de deployment context, KVS y BigQueue

Discovery / bootstrap dinámico [FUTURE, OUT OF SCOPE]
  └── implementará ActionPermissionProvider sin cambiar consumidores
```

## Matriz configurada

| Regla YAML | Tipos persistidos alcanzados | Action | Access level |
|---|---|---|---|
| Permiso exacto `catalog-signal` | `catalog-signal` | `start`, `stop` | `DEV_AND_UP` heredado de Slice 2 |
| Familia `flink-sql` | `flink-sql`, `gcp-flink-sql` | `start`, `stop` | `DEV_AND_UP` |
| Familia `flink-job` | `aws-flink-job`, `gcp-flink-job` | `start`, `stop` | `DEV_AND_UP` |
| Permiso exacto `clickhouse-mat-view` | `clickhouse-mat-view` | `start-materialized-view`, `stop-materialized-view` | `DEV_AND_UP` |

La comparación de tipo y Action es exacta para los permisos previos; las familias sólo incluyen los miembros concretos listados en YAML. `flink-job` es nombre de familia, no tipo persistido. `aws-flink-sql` no figura como miembro. Un par ausente de la configuración conserva su comportamiento y no recibe una validación ACME nueva. Retirar una regla de `family-permissions` desactiva el guard adicional para todos los miembros de esa familia y Action.

## Comportamiento preservado

- Las Actions de lectura existentes continúan con su autenticación y ejecución actuales.
- `triggerPreCreationAction` no consulta `ActionAuthorizationService`.
- Los componentes importados usan la misma autorización por team/project persistido que cualquier otro componente; no existe un guard adicional de importación.
- Polling, callbacks, visibilidad de resultados, KVS y eventos mantienen sus contratos.
- `POST /services/{serviceId}/actions/peek` y `POST /services/{serviceId}/actions/code` no cambian en este slice.

## Design Decisions

### DD-1: Slice 5 configura permisos por familia Flink

**Decisión**: definir familias, miembros concretos y permisos por familia en `app.action-authorization` de YAML. ClickHouse y las reglas F2–F4 permanecen en `permissions`. El adapter resuelve permiso exacto, luego familiar y finalmente wildcard.

**Fundamentación**: `ActionPermissionProvider` ya separa el enforcement del origen de los permisos. El mapa explícito evita inferir una familia desde nombres y permite apagar AWS y GCP con una sola regla abstracta. Duplicar la matriz en constantes o en una segunda policy generaría dos fuentes de verdad.

### DD-2: Pares ausentes no implican deny

**Decisión**: un par no configurado mantiene el flujo existente.

**Fundamentación**: el objetivo de la iniciativa es agregar validaciones a mutaciones identificadas, no definir una taxonomía completa de Actions ni cambiar contratos de negocio ajenos.

### DD-3: Discovery reemplaza el adapter, no los consumidores

**Decisión**: los Control Planes podrán informar tipos, Actions y niveles mediante una futura implementación de `ActionPermissionProvider`.

**Fundamentación**: el contrato actual ya devuelve `Optional<OperationAccessLevel>` para un par exacto. No es necesario introducir ahora job, cache, refresh o bootstrap remoto.

## Archivos afectados

### Archivos modificados

| Archivo | Cambio |
|---|---|
| `src/main/resources/application.yml` | Agrega familias y permisos Flink, y el par ClickHouse |
| `config/ConfiguredActionPermissionProvider.java` | Resuelve miembros de familia configurados antes del wildcard |
| `service/ActionPermissionProvider.java` | Documenta la resolución de familias |
| `config/ConfiguredActionPermissionProviderTest.java` | Verifica binding YAML, miembros concretos y apagado de familia |
| `service/ActionAuthorizationServiceTest.java` | Verifica delegación de los pares configurados |
| `service/impl/ActionServiceImplTest.java` | Verifica autorización previa a side effects y preservación de otros flujos |
| `controller/ActionController.java` | Documenta `403` para denegaciones de pares configurados |
| `docs/specs/swagger.yaml` | Refleja la respuesta `403` del endpoint component-bound |
| `docs/sig-616-slice-5-verification.md` | Matriz, rollout y smoke reproducible |

No se agrega `ActionAuthorizationPolicy` ni se modifican DTOs, productores, KVS o Control Planes.

## Manejo de errores

| Condición | Resultado |
|---|---|
| Tiger ausente o inválido | `401` existente |
| Recurso persistido inexistente o inconsistente | `404` existente |
| Par configurado con grant insuficiente, scope incompleto o ACME no verificable | `403`, sin KVS ni BigQueue |
| Par no configurado | Comportamiento existente |
| Deployment activo inexistente luego de autorizar | `409` existente |

## Estrategia de tests

- Cada par configurado se resuelve con `DEV_AND_UP`.
- Variantes de tipo/Action no exactas no activan una autorización nueva.
- Una denegación ACME ocurre antes de deployment context, KVS y BigQueue.
- Reads, pares desconocidos e imports conservan el dispatch existente.
- Precreation no invoca `ActionAuthorizationService`.
- Binding de configuración y soporte de distintos `OperationAccessLevel`.
- Suite completa mediante `./gradlew check`.

El smoke no productivo debe ejecutar un par configurado permitido y denegado, un par no configurado, precreation y un componente importado con el mismo owner persistido.

## Rollout y rollback

Las listas YAML base se aplican a todos los scopes y pueden reemplazarse desde `application-{scope}.yml`. Antes de rollout se contrastan los miembros configurados con los contratos efectivos de los Control Planes y el ownership persistido con ACME.

Rollback: retirar los permisos familiares del scope o revertir el PR. No hay migración de datos ni cambio de eventos.

## Fuera de alcance

- Default-deny global o allow-list de lecturas.
- Nuevos endpoints, Actions o casos de uso.
- Reglas especiales para componentes importados.
- Cambios en precreation, polling o service-level Actions.
- Discovery, jobs, cache o refresh dinámico.
- Autorización dentro de Control Planes.

## Criterios de aceptación

- La matriz de Slice 5 vive en configuración y no en constantes Java.
- Cada par configurado exige `DEV_AND_UP` antes de side effects.
- Pares no configurados, lecturas, imports y precreation conservan su comportamiento.
- `ActionServiceImpl` permanece genérico y no conoce tipos concretos.
- Una futura fuente Discovery puede implementar `ActionPermissionProvider` sin modificar consumidores.

## Estado de implementación — 2026-09-23

F5 `a89fcffcb` integra F4 `e75ca90d9` en [PR #1182](https://github.com/melisource/fury_rio-playmaker/pull/1182). La matriz combinada mantiene los guards configurados de F2–F4 y suma los diez pares F5: ocho combinaciones Flink por familia y dos ClickHouse exactas. El diff F4→F5 no modifica `ActionServiceImpl` ni otros casos de uso. Pasaron 25 selectores focalizados, dos checks L0/LOCAL_STACK con cleanup, contratos y `./gradlew check` con 4.086 tests, 0 fallas y 2 skips preexistentes. La [CI #5490](https://rp-ci-java.furycloud.io/job/rio-playmaker/5490/) falló antes del checkout por certificado no confiable del repositorio de pipelines, por lo que no aporta validación remota de este HEAD. El smoke Tiger/ACME no productivo permanece pendiente.

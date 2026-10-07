# Technical Specification — Slice 5: configuración de Actions mutantes restantes

> Seguimiento de review F4 (2026-09-24): evaluar en F5 si las dos variantes `require*IfConfigured` de `ActionAuthorizationService` admiten un helper privado sin mezclar lookup exacto de operaciones con fallback `*` de tipos de componente. No cambia la política ni agrega un segundo provider.

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

## Variantes de prueba test3 — 2026-09-23

| Rol mock | Rama y commit | Versión Fury | Expectativa F5 |
|---|---|---|---|
| committer | `feature/sig-616-auth-p5-committer-test3-v21@ca35f0b04` | [`0.1.17-p5-committer-allowed`](https://web.furycloud.io/rio-playmaker/versions/detail/0.1.17-p5-committer-allowed) | Permite los pares `DEV_AND_UP` configurados. |
| viewer | `feature/sig-616-auth-p5-viewer-test3-v22@6c7260690` | [`0.1.18-p5-viewer-denied`](https://web.furycloud.io/rio-playmaker/versions/detail/0.1.18-p5-viewer-denied) | Deniega los pares `DEV_AND_UP` configurados antes de side effects. |

Ambas ramas parten de F5 `a89fcffcb`, limitan `AcmeClientRoleMock` al profile `test3` y excluyen al team mock `ml-ads-signals` del bypass de plataforma sólo en esas variantes. Sus pruebas cargan el YAML real F5 para los diez pares. Pasaron contratos y `./gradlew check --no-daemon` con 4.101 tests, 0 fallas y 2 skips en cada rama. Fury informa `FINISHED` para ambos builds. No se desplegaron ni se ejecutó smoke remoto.

## Addendum aprobado por el owner — cierre de mutaciones de Signals, 2026-09-23

El owner amplió F5 después de detectar que el rol viewer aún podía editar descripción, visibilidad y configuración de componentes en test3. Las secciones anteriores describen el alcance original de Actions; este addendum las supersede para el cierre de F5. Se revisó `ads-signals-frontend@origin/develop:9bf76ffc` y se exigió autorización configurable en YAML para los casos de uso de Playmaker que crean, modifican o eliminan estado del agregado desde esa UI. No se agregan endpoints, Actions ni casos de uso.

| Mutación incorporada al guard de F5 | Scope/operación YAML | Owner |
|---|---|---|
| Crear/editar/cambiar estado de Data Product | `data-product:create/update/update-status` | Nuevo scope en create; owner persistido en update; también destino si cambia owner |
| Eliminar Data Product | `data-product:cascade-delete-components` de F4 | Owner persistido, sin bypass de platform team bajo el guard |
| Patch de configuración o rename en pipeline | `pipeline:update-component-config/rename-component` | Data Product persistido |
| Crear/editar/activar/eliminar definición | `component-definition:create/update/activate/delete` | Data Product del componente persistido |
| Solicitar/resolver import authorization | `import-authorization:request/resolve` | DP solicitante o DP de origen persistido, respectivamente |

Permanecen los guards de F2–F4 para componentes, relaciones, topología, deploy, undeploy, inactivation y Actions. El nivel es `DEV_AND_UP` para escrituras ordinarias y `DEPLOYER_AND_UP` para delete destructivo y resolve; las reglas exactas viven en `application.yml`. Un scope incompleto deniega. Las operaciones sin regla conservan sus checks anteriores. Algunos checks legacy de Data Product pueden exigir un rol más alto en producción.

Los POST de lookup/peek y generación de SQL son lecturas. Favoritos personales y freezes mantienen sus controles propios; Entities pertenece a Rio Entity Service, por lo que no puede autorizarse desde Playmaker. La ruta Flink `POST /v2/services/:id/actions/code` existe en el proxy, pero la UI actual sólo usa GET; precreation con `serviceId=0` carece de owner persistido y sigue excluida por la SPEC. La matriz exacta está en `docs/sig-616-slice-5-verification.md` del repositorio.

F5 quedó en `feature/operation-authorization-by-team-f5@141eacbc5` y [PR #1182](https://github.com/melisource/fury_rio-playmaker/pull/1182). Pasaron 31 selectores focalizados, ambos checks L0/LOCAL_STACK con cleanup y `./gradlew test --rerun-tasks --no-daemon` con 4.107 pruebas, 0 fallas, 0 errores y 2 skips preexistentes. El smoke F1 y la aprobación humana del PR siguen pendientes. Se crearon dos nuevas ramas temporales test3: `feature/sig-616-auth-p5-committer-test3-v23@9b2b7d1f2` y `feature/sig-616-auth-p5-viewer-test3-v24@8f91234e4`; ambas pasaron las pruebas focalizadas. Sus versiones Fury son `0.1.19-p5-committer-allowed` y `0.1.20-p5-viewer-denied`, ambas en `FINISHED`. No se desplegaron.

## Addendum — mutaciones configurables, 2026-10-06

La decisión D27 de [[SIG-616 — Autorización de operaciones por equipo]] reemplaza la denegación por ownership incompleto descrita arriba: si falta cualquiera de teamName o projectCode (null, vacío o espacios), se omite el permiso adicional por proyecto. Tiger y los controles de negocio permanecen activos. OperationAuthorizationService es la única implementación de esa aplicabilidad; ActionAuthorizationService resuelve la configuración y delega, sin repetir la condición.

Todas las mutaciones de componentes y pipeline dentro del alcance de SIG-616 usan el provider de configuración. Start/stop de Signals y Flink y las materialized views de ClickHouse ya están declaradas por par o familia. Las rutas de borrado por nombre e inactivación se incorporan con reglas exactas pipeline:delete-component y pipeline:inactivate-component, con DEPLOYER_AND_UP como valor base. Los consumidores dejan de fijar el rol en Java. Las reglas exactas de pipeline no heredan el wildcard de componentes.

Cambiar el nivel en YAML cambia el rol exigido. Retirar una regla REST omite sólo este guard adicional; retirar una Action del catálogo mutante la convierte en desconocida y el dispatch la rechaza. La elegibilidad legacy por systemId, los locks, blockers, auditoría y publicación after-commit conservan su comportamiento. El POST legacy de código Flink y las solicitudes/administración de freeze mantienen las exclusiones ya descritas; crear una solicitud de excepción sólo persiste PENDING y no dispara deploy ni modifica el pipeline.

Implementación en feature/configurable-component-lifecycle-permissions, desde develop@d99f89fce. El PR apunta a develop. Evidencia requerida: YAML binding, servicios consumidores, HTTP/H2 con nivel modificado/regla retirada/ownership incompleto, fallos ACME sin efectos, escenarios existentes de start/stop, contrato completo, stacks aislados con cleanup y regresión. Gate humano previo a merge.

### Corrección del addendum — familia Fury

La revisión anterior comprobó start/stop de Signals y Flink y las materialized views de ClickHouse, pero omitió los pushers Fury. La implementación del Control Plane acepta start/stop en kafka-fury-streams, fury-streams-kafka, kafka-fury-bigqueue, fury-bigqueue-kafka y kafka-fury-kvs. Esos diez pares faltaban en el YAML de Playmaker y el dispatch los rechazaba antes de consultar ACME. La familia fury-pusher y sus dos reglas DEV_AND_UP se incorporan al mismo PR #1275 hacia develop. Los pares desconocidos siguen rechazándose y la omisión de ACME por team O project ausente sólo aplica a Actions declaradas.

La prueba HTTP/H2 con el YAML anterior reprodujo 403 para todos los pares Fury; con la familia agregada devuelve 202, guarda PENDING y publica una sola Action con tipo, verbo y caller correctos. Las pruebas adicionales cubren rol insuficiente, ACME no disponible, owner incompleto, token ausente y eliminación de la regla familiar sin convertirla en lectura.

Publicación verificada: PR #1275 hacia develop, HEAD 2a097e580eab451e85fc749adc83d0c3c1d218ea, Draft y descripción vacía. Pasaron 439 pruebas focalizadas, 4.666 de regresión y 96 selectores; el check de stack health sigue bloqueado por conexión Colima/MySQL y su cleanup está certificado. Esta evidencia sólo valida la admisión y el dispatch local de Playmaker; la ejecución del Control Plane desplegado requiere su validación correspondiente.


## Addendum — ClickHouse y versión de Actions completas, 2026-10-07

D30 completa los otros tres pares implementados y no declarados identificados en la auditoría: `kafka-to-clickhouse:pause-kafka-connector` y `resume-kafka-connector` usan `DEV_AND_UP`; `clickhouse-mat-view:describe-materialized-view` se declara como lectura Tiger-only. Junto con los diez pares start/stop Fury de D29 son trece pares faltantes cubiertos por PR #1275. No se cambia el contrato del Control Plane: pause/resume conserva la validación de template, ownership, deployment activo y soporte on-premise. `ping`, start/stop genéricos del conector y el retry interno `reconcile-kafka-connector-cleanup` permanecen excluidos.

`ConfiguredActionPermissionProviderTest` prueba el YAML real y `ComponentAuthorizationIntegrationTest` comprueba dispatch autorizado, viewer/ACME fallido, falta de Tiger, ownership incompleto y rechazo de pares cruzados entre templates. Describe publica con Tiger sin consultar ACME. `feature/configurable-component-lifecycle-permissions@1be7fb63b` pasó 96 selectores, 4.688 tests y los hooks obligatorios; cobertura 97,24%. El stack health quedó bloqueado por Connection refused Colima/MySQL, con cleanup certificado, y loopback/Kafka no se ejecutaron. Fury confirmó `0.0.1-acme-actions-complete` en FINISHED, habilitada y tipo test, para ese HEAD con tests de build habilitados. Los cinco checks de CI #5987 terminaron SUCCESS. Review humano y validación desplegada siguen pendientes.


## Corrección de review — Binding de pause/resume, 2026-10-07

PR #1275 vincula los selectores de las dos Actions de `kafka-to-clickhouse` al recurso autorizado. `component_id`, `data_product_id/name` y `target_deployment_id` se derivan de las referencias persistidas y el deployment activo; `service_name`, `cluster_type` y `clickhouse.cluster` se resuelven desde los parámetros de su definición. Playmaker rechaza input contradictorio con 400 y metadata ausente/ inválida o cloud con 409 antes de KVS/BigQueue; no toma routing cliente como fallback. Sólo publica los campos usados por el worker. La política de omisión ACME por equipo O proyecto ausente se conserva (D27).

`run-connector-action-contract-check.sh` genera mensajes desde HTTP/H2 y los reproduce en `PauseKafkaConnectorAction`/`ResumeKafkaConnectorAction` reales del CP fijado en `97fcf076152c58711e7c5b483cc58555647e6423`, con validator real y adapters SQL/KVS simulados. El contrato pasó y certificó cleanup de su workspace propio. El contrafactual envelope A/data B reproduce el riesgo previo; la solicitud corregida A→B no publica mensaje. No acredita DDL desplegado ni conectividad remota. Commit `47c2344c3d3ec51aac578f14c019a52b1bbd3370` pusheado en PR #1275 y cuerpo verificado. Pasaron 96 selectores, 4.720 tests (cero fallas/errores, dos skips preexistentes), 97,25% de líneas, seis replays del consumidor y hooks pre/post-commit. Stack local falló por MySQL Connection refused; loopback/Kafka no corrieron. Cleanup certificado de `rio-playmaker-agentic-22154`, archive de contrato y worktree CP propio. CI 5990 pasó cuatro checks y falló coverage; el follow-up posterior corrige ese gate. La versión anterior `0.0.1-acme-actions-complete` no incluye este fix.


## Follow-up — Respuestas y cobertura, 2026-10-07

Se respondieron y verificaron los dos comentarios en [policy](https://github.com/melisource/fury_rio-playmaker/pull/1275#discussion_r4208369370) y [binding](https://github.com/melisource/fury_rio-playmaker/pull/1275#discussion_r4208369705). CI 5990 pasó cuatro checks pero falló PR coverage (78,82% < 90%; ConnectorActionData 71,87%), porque MeliCov computa las líneas con branches parciales como no cubiertas. El commit `933eeb8d0461c871f1fab50967e611a6520c9aef` agrega 32 tests de metadata inválida/nulos/routing legacy; no cambia producción ni umbrales. Los fixtures distinguen ID del componente 2001 y DP 1001. Pasaron 97 selectores, 4.752 tests en 384 suites (cero fallas/errores, dos skips), 97,26% global JaCoCo y 93,75% strict-local del helper, validadores y hooks pre/post-commit. Stack MySQL falló por Connection refused; cleanup certificado de rio-playmaker-agentic-50666. Push y cuerpo final verificados; los cinco checks de CI 5994 SUCCESS, coverage PR 95,29%, helper 93,75% y global MeliCov 94,93%. Respuesta al P1 actualizada y leída/verificada. No nueva versión, merge ni deploy.


## Integración con develop — Conflictos #1275, 2026-10-07

Merge `da9bb431289da0d2d5719538ed886dda65e39c35` une `933eeb8d0` con `develop@b0b076b51`. Mantiene el revert de herencia de entidades de #1254 y los fixes D27–D31. Sólo impact.json requirió resolución manual: elimina cuatro selectores de suites borradas y conserva todos los tests adicionales de permisos/binding. Pasaron 93 selectores y 4.687 tests en 380 suites, sin fallas/errores y con dos skips; 97,23% global JaCoCo y 93,75% helper strict-local. 23 archivos del PR permanecen byte-identical; docs/scenarios y manifiesto se combinaron. Sin cambios manuales de Java; hooks de conflicto, validadores y post-commit PASS. Stack MySQL exit 1 por Connection refused, loopback/Kafka no ejecutados y cleanup certificado de rio-playmaker-agentic-87924. Push y cuerpo verificados; GitHub MERGEABLE y cinco checks de CI 6015 SUCCESS; cobertura PR 95,29%, helper 93,75% y global MeliCov 94,91%. La versión anterior no incluye este merge.

- **Review y descripción #1275, 2026-10-07:** Fix 0a5a01f76 resuelve únicamente routing necesario para pause/resume, con regresión de Kafka detenido y binding persistido. Runner genera fixtures frescos. D27 conservada y ambos comentarios nuevos respondidos; cuerpo ejecutivo publicado y verificado. Merge 526c1115c integra develop a4e2829ad (#1270), conserva 21 archivos propios idénticos y mantiene diff de 26 archivos. 93 selectores y 4.703 tests PASS, 97,24% JaCoCo y 97,01% helper; stack MySQL bloqueado y cleanup certificado. GitHub MERGEABLE; CI #6029: cinco checks SUCCESS; PR coverage 97,72%, helper 97,01% y overall MeliCov 94,92%. [[2026-10-07-playmaker-pr1275-routing-review]].

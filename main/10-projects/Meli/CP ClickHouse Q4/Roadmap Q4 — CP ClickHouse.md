---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[CP ClickHouse Q4]]"
  - "[[rio-controlplane-clickhouse]]"
  - "[[rio-playmaker]]"
  - "[[ads-signals-frontend]]"
  - "[[Import de Refreshable Materialized Views externas]]"
  - "[[Plan de implementación — Context en ClickHouse]]"
aliases:
  - Roadmap CP ClickHouse Q4
  - Roadmap ClickHouse Q4
  - Backlog ClickHouse Q4 ordenado
  - Avance ClickHouse Q4
tags:
  - kind/doc
  - area/meli
  - app/rio-controlplane-clickhouse
created: "2026-10-27"
updated: "2026-10-27"
---

# Roadmap Q4 — CP ClickHouse

## Propósito

Roadmap completo de Q4 2026 para ClickHouse en RIO, con dos personas (Rodrigo Jara y Florencia Sicre). Cubre **todo** el backlog del trimestre más los huecos encontrados en el código, ordenado por valor. Cada entregable es una capacidad funcional en producción. La capacidad disponible se muestra con números, para que lo que no alcance sea una decisión explícita y no un recorte silencioso. Es la base para acordar el plan con Flor; los juicios de valor y las estimaciones son la propuesta de este documento. Plan interno: vive sólo en este proyecto.

## Contenido

### 1. Avance de Q4 a la fecha

En octubre, el bloque **Refreshable Table** del backlog pasó de no existir a estar casi completo en producción:

| Capacidad | Estado | Evidencia |
|---|---|---|
| Crear refreshable desde RIO | En `master` | CP #294 (9-oct), PM #1265 (8-oct), front #736 (13-oct) |
| Start / stop de refreshable | En `master` | CP #346 (15-oct); front #788, #800, #783 |
| Borrar refreshable | En `master` | CP #346 y #356 (20-oct), ownership #355 |
| Importar refreshable existente | Desarrollado y certificado E2E 8/8 | CP #362, PM #1328, front #816; falta la última prueba (permisos) |
| E2E local de ClickHouse (acelera todo lo que sigue) | En `develop` | CP #342, PM #1288 y #1332 (26-oct); suite de regresión física CP #349 |

En el mismo período entraron CODEC con precisión DateTime64 (CP #291) y el alta del warehouse vía configuración (CP #309). Otros miembros del equipo avanzaron en paralelo sobre `kafka-to-clickhouse` y los clusters Hydra; ese trabajo no está en este backlog ni en la capacidad de este plan.

En resumen: de los cuatro ítems de Refreshable Table, tres están en producción y el cuarto está desarrollado. El resto del backlog arranca ahora con la infraestructura de prueba ya armada.

### 2. Capacidad contra backlog

Supuestos de este documento, no estándar del equipo: quedan 9 semanas (28-oct → 31-dic) y se descuenta la última semana de diciembre. Se asume un 70 % de foco, porque el resto se va en soporte, reviews y otros proyectos. Las tallas S ≈ 0,5, M ≈ 1, L ≈ 2-3 y XL ≈ 3+ son personas-semana.

- **Capacidad:** 2 personas × 8 semanas × 70 % ≈ **11 personas-semana** (16 con foco total).
- **Backlog pendiente estimado:** ≈ **21 personas-semana** más Control, que no tiene definición y no se puede estimar.

| Bloque | Pendiente | Estimación propia (p-s) |
|---|---|---|
| Refreshable (cierre del import, credenciales, limpieza de importadas) | P0 | 1,5 |
| Salud del refresh (hueco nuevo) | — | 1 |
| Context v2 sin duplicidad | P0 | 1 |
| Credenciales (permisos admin, lib, soporte de la lib) | P0 / P1 | 2,5 |
| Warehouse (provision, start-stop, deprovision) | P0 | 4,5 |
| Vista normal (provision, deprovision, start-stop, import y credenciales) | P1 / P2 | 3,25 |
| Import explícito de MergeTree (hueco nuevo) | — | 1 |
| Dictionary | P2 | ≈ 2 (sin diseño) |
| Control | P2 | sin definir |
| Multi-source (tres tipos, un refactor compartido) | P3 | ≈ 4 |

Varias tallas bajan respecto de la planilla porque el código ya resuelve parte del trabajo (§5). Aun así no entra todo:

- **Con 70 % de foco (≈ 11 p-s)** entran todos los P0 más los dos huecos nuevos (≈ 11 p-s).
- **El desglose por desarrollo suma ≈ 31 días por persona** (≈ 12,5 p-s en total) contra ≈ 28 disponibles: P0, P1 y los huecos entran; el import de vista normal y el de MergeTree (≈ 10 días) quedan en riesgo en la última semana. Detalle en [[Plan Q4 ClickHouse — semana a semana]].
- **Multi-source (P3), Dictionary y Control (P2) quedan sobre la línea** incluso con foco total.

Este documento no saca nada del trimestre: lo que no alcanza se presenta como decisión del líder, con tres opciones: sumar capacidad, aceptar que se corre o bajarle prioridad a otra cosa.

### 3. Reglas del roadmap

- **Entregable = capacidad funcional.** Está hecho cuando un usuario de RIO puede hacer algo nuevo en producción, de punta a punta: CP, Playmaker y front según corresponda, con un caso en `.lore/ecosystem/cases/` en PASS.
- **PR habilitante permitido, con tres condiciones:** no cambia comportamiento visible, trae sus tests y un entregable con nombre lo consume en su misma ventana.
- **Orden por valor y prioridad del backlog.** Primero lo que más gana el usuario por unidad de esfuerzo; lo casi terminado va antes; lo que depende de terceros se pide el primer día.
- **Si se aprieta, se mueve la cola.** Nunca se deja un entregable a medias.

### 4. Qué significa "ClickHouse full"

Cada objeto ClickHouse que RIO administra tiene su ciclo de vida completo donde la operación tiene sentido: provision, update, deprovision, start/stop, import, describe, estado de runtime y credenciales. A eso se suma el warehouse como componente y un camino para que el usuario lea con sus propias keys.

| Componente | Provision / update | Deprovision | Start / stop | Import | Estado runtime | Credenciales | Falta para full |
|---|---|---|---|---|---|---|---|
| MergeTree (`clickhouse-mergetree`) | ✅ | ✅ | n/a | ⚠️ implícito | n/a | ⚠️ se pierden en ALTER | Context v2; decidir import explícito |
| Vista incremental (`clickhouse-mat-view`) | ✅ | ✅ | ✅ | ✅ | ✅ RUNNING/STOPPED | ⚠️ se pierden en ALTER | Context v2 |
| Vista refreshable (`clickhouse-ref-view`) | ✅ | ✅ (⚠️ importadas) | ✅ | 🟡 en rama | ⚠️ no ve refresh fallido | ⚠️ se pierden en ALTER | Cerrar import, limpieza de importadas, salud del refresh, Context v2 |
| Kafka → ClickHouse (`kafka-to-clickhouse`) | ✅ | ✅ | ✅ pause/resume | n/a | ✅ | ✅ | — |
| Vista normal | ❌ | ❌ | n/a | ❌ | n/a | ❌ | Tipo nuevo completo |
| Warehouse (`clickhouse-warehouse`) | ❌ | ❌ | ❌ | n/a | ❌ | API key | Tipo nuevo completo (SIG-705) |
| Lectura con keys del usuario | — | — | — | — | — | ❌ | Lib de consumo |

Dictionary, Control y multi-source también son parte del backlog de Q4; su lugar en el plan lo define la capacidad (§2).

#### Huecos que no están en el backlog

Encontrados al contrastar `origin/develop`; ninguno aparece en la planilla.

- **Salud del refresh en refreshable (gap real, prioridad alta).** El CP publica estado de runtime de las vistas sólo cuando se ejecuta start o stop (`ActionTriggerController.publishRuntimeStatus`); nada consulta `system.view_refreshes`. Una refreshable cuyo refresh falla cada hora sigue mostrándose como RUNNING. Para un componente cuyo único trabajo es refrescar, eso es una falla silenciosa. Reutiliza `ComponentRuntimeStatusPublisher`, que ya existe. Talla estimada M.
- **Import explícito de MergeTree.** Si la tabla ya existe, `DeployTableDeployment` toma el camino de diff y la **altera** para que calce con lo declarado. Adoptar una tabla externa hoy significa modificarla en el primer deploy. Las vistas sí tienen import con marcador y sin alteración. Hay que decidir si full exige el mismo contrato para tablas; si sí, reutiliza el marcador `created by Rio` y el patrón de `ImportMatViewCommand`.
- **Limpieza al deprovisionar vistas importadas.** Entra en R1; no tiene fila propia en la planilla.
- **Refresh manual (`SYSTEM REFRESH VIEW`).** Se decide junto con la semántica de stop (§10).

### 5. Estado real de cada ítem contra el código

Verificado en `rio-controlplane-clickhouse@origin/develop 4007bd28`, `rio-playmaker@origin/develop 0c0e319c9` y `ads-signals-frontend@origin/develop`.

| Ítem del backlog | Prioridad / talla | Estado real | Evidencia |
|---|---|---|---|
| Deprovision refreshable | P0 · M | **Hecho en `master`**, salvo la limpieza de vistas importadas | `DeploymentHandlerRegistry` registra `clickhouse-ref-view` × `DEPROVISION` con `DeleteMaterializedViewDeployment`; PR #346 de Flor (15-oct) en `master` vía release `202610.21.1`. Hueco: para una vista importada no se borra la clave KVS `import:{user}` ni se revoca el token KMS (TODO explícito). |
| Start-stop refreshable | P0 · S | **Hecho en `master`** en CP, Playmaker y front | CP: `StartMaterializedViewAction`/`StopMaterializedViewAction` (`ATTACH` / `DETACH … PERMANENTLY`) y `ActionDispatcher.supportsComponent` acepta `clickhouse-ref-view`. PM: `action-permissions` start/stop para `clickhouse-ref-view`. Front: `clickhouse-refreshable-table/adapter.ts` con start/stop. |
| Import refreshable view | P0 · XL | **Desarrollado**; falta la última prueba (permisos) y el push de Playmaker | Ver [[Import de Refreshable Materialized Views externas]]: CP #362, PM #1328, front #816; E2E local 8/8. El bloqueo del push de Playmaker era #1332, mergeado el 26-oct: ya se puede sincronizar con develop y pasar el gate Cleric. |
| Import refreshable — credenciales | P0 · S | **Operacional, no de código**: el endpoint de precarga ya existe | `MatViewImportController` (`POST /clickhouse/mat-view/import-credentials`) + `MatViewCredentialService` (KVS `import:{user}`, cifrado CKAAS). Falta conseguir user/pass de las vistas existentes y cargarlas. |
| Context v2 — credenciales sin duplicidad | P0 · M | **Abierto, con semilla en la rama de import** | `DeploymentCommandResult.forAlterMv` no devuelve credenciales y `forAlterTable` sólo las devuelve al rotarlas; un ALTER deja la versión nueva sin las keys. La rama de import agregó `forAlterMv(…, username, encryptedPassword)`: es el patrón a generalizar. |
| Warehouse provision | P0 · sin talla | **Spec técnica en draft** ([SIG-705](https://spellbook.adminml.com/projects/SIG/specs/SIG-705), Flor) | Hoy nada crea servicios Cloud: `ClickHouseCloudApiClientImpl` sólo lista; `warehouses.yml` es estático; no hay tipo `clickhouse-warehouse`. |
| Warehouse start-stop | P0 · XL | Abierto | Sin código. Con el cliente Cloud de escritura es un cambio de estado del servicio, no un XL. |
| Warehouse deprovision | P0 · L | Abierto | Sin código. Mismo cliente; el riesgo está en la seguridad del borrado, no en el volumen. |
| Cambio permisos de admin | P0 · N/A | **Decisión pendiente**, bloquea import y warehouse | Admin del CP vía Fury Secrets (`ClickHouseClientFactory`). Hay que definir el nivel mínimo para crear usuarios, leer DEFINER ajenos y operar la API Cloud. |
| Lib de consumo de permisos | P0 · N/A | Abierto, depende de un contrato de outputs estable | Los outputs entregan tokens KMS, no texto plano (`EncryptionServiceImpl` → `rio-controlplane-kms`). Ningún endpoint expone las keys al usuario. |
| Implementación de lib | P1 | Después de la lib | — |
| Provision normal view | P1 · M | Abierto; gate de demanda en prod | No existe tipo de vista normal. |
| Deprovision normal view | P1 · M | Abierto | Reutiliza `DeleteMatViewCommand` (`DROP VIEW`). |
| Start-stop normal view | P2 · S | Abierto; **definir la semántica** | Una vista normal no procesa nada en background: `DETACH` sólo la deja inconsultable. Hay que acordar qué espera el usuario antes de implementarlo. |
| Import normal view (+ credenciales) | P2 · L + XL | Después del gate de demanda | Reutiliza `ImportMatViewCommand` y la precarga, que sólo necesitan un DEFINER. |
| Dictionary | P2 | Abierto | Feature nueva sin diseño. |
| Control | P2 | **Sin definir** | La planilla no describe qué es; hay que aclararlo antes de estimarlo. |
| Multi-source (incremental, refreshable, normal) | P3 · XXL × 3 | Abierto | El supuesto de una fuente está fijo en seis lugares (`MaterializedViewRequest`, `MaterializedViewIdentifierExtractor`, `SqlSecurityValidator`, `DeployMaterializedView`, `AlterMvRefreshCommand`, `DescribeMatViewQuery`). Es un refactor compartido, no tres XXL. |

### 6. Priorización por valor

El valor es la propuesta de este documento, a validar con Flor con dos datos que hoy no están: cuántas refreshable hay en producción y cuántos teams esperan crear warehouse.

| Entregable (lo que el usuario puede hacer) | Backlog | Valor | Por qué |
|---|---|---|---|
| R1 Adoptar refreshable existentes y borrarlas limpio | P0 | Alto | Ya desarrollado: valor casi gratis |
| F1 Ver que su refreshable está fallando | Hueco | Alto | Hoy un refresh fallido se ve RUNNING en producción |
| F2 Crear su warehouse desde RIO | P0 | Alto | Destraba el onboarding de teams nuevos |
| R2 Seguir viendo sus keys después de un ALTER | P0 | Alto | Un ALTER deja la versión nueva sin credenciales |
| R3 Leer ClickHouse con sus propias keys | P0 / P1 | Alto | Habilita el consumo; depende de R2 |
| F3 Prender, apagar y borrar su warehouse | P0 | Medio-alto | Ahorro de costo e higiene |
| R4 Vistas normales con ciclo de vida completo e import | P1 / P2 | Por medir | Depende de la demanda real en producción |
| F4 Adoptar una tabla MergeTree sin alterarla | Hueco | Medio | Hoy adoptar una tabla externa la modifica |
| Dictionary, Control, multi-source | P2 / P3 | Por definir | Sobre la línea de capacidad (§2) |

### 7. Roadmap de entregables

El plan con fechas, responsables y días vive en [[Plan Q4 ClickHouse — semana a semana]], y contiene sólo ítems de la planilla. Los entregables de esta sección son el análisis funcional de esos ítems; F1 (salud del refresh), F4 (import de MergeTree) y la limpieza de importadas en R1 son hallazgos propios fuera de la planilla, y entran sólo si se decide reemplazar otro ítem.

#### R1 — Adoptar refreshable existentes

- **Hecho cuando:** un usuario importa su refreshable desde la UI en producción, RIO la gestiona sin alterarla, y al borrarla no quedan la clave KVS `import:{user}` ni el token KMS.
- **Trabajo:** la última prueba del import (permiso pendiente); sincronizar Playmaker con develop (ya incluye #1332), pasar el gate Cleric y hacer push; precargar las credenciales de las vistas reales con sus owners; y un PR chico de limpieza en el deprovision de importadas. El usuario DEFINER externo no se borra, porque no es de RIO (§9).
- **En paralelo:** decidir con Flor los permisos mínimos del usuario admin del CP (P0 del bloque Credenciales).

#### F1 — Ver si mi refreshable falla

- **Hecho cuando:** una refreshable cuyo último refresh falló aparece con estado de error en RIO, con la hora del último refresh exitoso.
- **Trabajo:** leer `system.view_refreshes` y publicar el estado por `ComponentRuntimeStatusPublisher`, que ya existe. Es terreno de Flor (SIG-640) y llena la semana en que los pedidos de warehouse están en manos de terceros.

#### R2 — Keys siempre vigentes

- **Hecho cuando:** después de un ALTER de MergeTree, vista incremental o refreshable, la versión desplegada nueva tiene las mismas keys, y ningún flujo genera un segundo juego de credenciales.
- **PR habilitante:** una credencial única que viaje en todos los resultados (`forCreateTable`, `forAlterTable`, `forCreateMV`, `forAlterMv`), generalizando lo que la rama de import ya hizo en `forAlterMv`. Lo consumen R2, R3 y R4.
- **Antes de empezar:** verificar si Playmaker ya conserva los outputs previos cuando el CP no los reenvía. Si los conserva, R2 se reduce a reenviarlos desde el CP.

#### F2 — Crear mi warehouse

- **Hecho cuando:** un team pide un warehouse desde RIO y queda con un servicio principal read/write y uno secundario read-only, visibles en discovery y usables para crear tablas, según SIG-705.
- **PR habilitante (primera semana):** cliente de escritura de ClickHouse Cloud con create, update, cambio de estado y delete; espera acotada del estado final y reconsulta ante un resultado incierto. Lo consumen F2 y F3. El endpoint de cambio de estado se confirma contra la [OpenAPI oficial](https://api.clickhouse.cloud/v1).
- **Coordinación:** el front de Teams → Warehouses (SIG-690/691) tiene otros responsables; alinear su contrato con este `PROVISION`.

#### R3 — Leer con mis keys

- **Hecho cuando:** un consumidor obtiene las credenciales read-only de una tabla de su data product y ejecuta una query contra ClickHouse.
- **Incluye** la lib de consumo (P0) y su soporte inicial (P1).
- **Decisión previa (§8):** qué es "la lib": un SDK que descifre el token KMS de los outputs, un endpoint del CP o mostrarlas en la UI.

#### F3 — Prender, apagar y borrar mi warehouse

- **Hecho cuando:** un team detiene su warehouse desde RIO y lo vuelve a levantar con los datos intactos, y puede borrarlo con confirmación explícita.
- **Trabajo:** cambio de estado y delete sobre el cliente de F2. El borrado reutiliza el patrón `confirmationToken` de `DeleteResourceDeployment`.

#### R4 — Vistas normales completas

- **Hecho cuando:** un usuario crea, borra e importa vistas normales desde RIO, con sus credenciales.
- **PR habilitante:** variante de vista (`INCREMENTAL`, `REFRESHABLE`, `PLAIN`), que sólo cambia el builder DDL, el validador SQL y los grants. El import reutiliza `ImportMatViewCommand` y la precarga de credenciales, que sólo necesitan un DEFINER.
- **Antes de empezar:** la query de demanda en producción y la semántica de start-stop (§8).
- **Riesgo:** el import de vista normal queda en la última semana hábil y es lo primero que se mueve si el plan se atrasa.

#### F4 — Adoptar MergeTree sin alterarla

- **Hecho cuando:** un usuario adopta en RIO una tabla MergeTree existente sin que el primer deploy la modifique.
- **Trabajo:** el contrato de import que ya tienen las vistas (marcador `created by Rio`, patrón de `ImportMatViewCommand`), aplicado a `DeployTableDeployment`.

#### Sobre la línea de capacidad

Dictionary (P2), Control (P2, sin definir) y multi-source (P3). Multi-source es un solo refactor compartido por los tres tipos de vista (§5), y R4 deja la base preparada. La decisión se lleva al líder con los números de §2.

### 8. Cómo avanzar más rápido

1. **Dos lanes sin pisarse.** Vistas y credenciales viven en SQL dentro de ClickHouse; warehouse vive en la API de Cloud. Los únicos archivos compartidos son `DeploymentHandlerRegistry`, `ClickHouseComponentTypes`, `ResourceOwnershipValidator` y `DeploymentCommandResult`: cambiarlos en PRs chicos, y quien llegue segundo hace el rebase.
2. **Checklist de alta de operación.** Cada operación o tipo nuevo toca siempre los mismos puntos. Se escribe una vez y se usa en cada entregable:
   - CP: `ClickHouseComponentTypes`, `DeploymentHandlerRegistry.standard()`, `ResourceOwnershipValidator` y la factory en `DeploymentCommandResult`; para acciones, `ActionDispatcher.supportsComponent` y `ClickHouseActionContract`.
   - Playmaker `application.yml`: `action-permissions`, las dos tablas de `deployment-routing`, `use-group` y la lista de tipos; además `ComponentMetadataAllowlist`, `MetricTags` y `CostComponentType`.
   - Front: `src/technologies/<tipo>/adapter.ts`, `registry.ts`, `catalog.ts` y `relations.ts`.
   - E2E: un caso nuevo en `.lore/ecosystem/cases/`, copiando el más cercano (hoy pasan cinco casos ClickHouse).
3. **Un doc de diseño corto por entregable, dentro de este proyecto,** escrito antes de su ventana. Para F2 ya existe SIG-705 como referencia.
4. **Pedidos a terceros el primer día:** el permiso de la última prueba del import, la API key Cloud con escritura, el contrato de aprobación RIO y las credenciales de las vistas existentes.
5. **Demo al cerrar cada entregable:** cada dos semanas hay algo funcionando que mostrar, y el avance queda visible.

### 9. Para la conversación con Flor

1. **Avance a la fecha** (§1): sirve para responder el cuestionamiento con evidencia.
2. **Validar el orden por valor** (§6), con dos datos: cuántas refreshable hay en producción y qué teams esperan crear warehouse.
3. **Confirmar las lanes** y el acuerdo sobre los cuatro archivos compartidos.
4. **Decisiones:**
   - Semántica de stop en refreshable: `DETACH PERMANENTLY` (hoy) o `SYSTEM STOP VIEW` (pausa el refresh y mantiene la lectura).
   - Semántica de start-stop en vista normal.
   - Qué es "la lib" de R3: SDK, endpoint o UI.
   - Permisos mínimos del usuario admin del CP y alcance de la API key Cloud.
   - Qué es "Control" en la planilla.
5. **Llevar al líder la línea de capacidad** (§2) con una propuesta conjunta.
6. **Repartir los pedidos a terceros** y fijar la demo de R1 y F1 (6-nov).

### 10. Riesgos y preguntas abiertas

- **Semántica de stop en refreshable.** Hoy stop es `DETACH … PERMANENTLY`, que deja la vista inconsultable. `SYSTEM STOP VIEW` / `SYSTEM START VIEW` pausan sólo el refresh y mantienen la lectura.
- **Usuario DEFINER externo al borrar importadas.** No es de RIO: borrarlo puede romper a otros consumidores. La propuesta es revocar sólo lo que RIO creó (clave KVS y token KMS); relacionado con PA-1 del import.
- **Merge de outputs en Playmaker.** No está verificado y define el tamaño de R2.
- **Warehouse:** el contrato de aprobación RIO y la confirmación de API key en observabilidad siguen "pendiente de acuerdo" en SIG-705. Si no se resuelven en la primera semana, F2 se corre y empuja a F3.
- **Foco real.** La estimación asume 70 % de foco. Si el soporte o los otros proyectos se comen más, lo primero que se mueve es la cola de cada lane (R4, F4).
- **Checkout local desactualizado:** el clon principal del CP está 215 commits detrás de `origin/develop`, y su `graphify-out` también.

## Fuentes

- Historial `--first-parent` desde el 2026-10-01 de `rio-controlplane-clickhouse@origin/develop`, `rio-playmaker@origin/develop` y `ads-signals-frontend@origin/develop`; pertenencia a `origin/master` verificada para CP #294, #346, #356 y #309.
- `rio-controlplane-clickhouse@origin/develop 4007bd28` (2026-10-26) y rama `feature/refreshable-view-import@377e3dcc`: `ClickHouseComponentTypes`, `DeploymentHandlerRegistry`, `ActionDispatcher`, `ActionTriggerController.publishRuntimeStatus`, `DeployTableDeployment`, `DeploymentCommandResult`, `ImportMatViewCommand`, `MatViewCredentialService`, `ClickHouseCloudApiClientImpl`; `system.view_refreshes` sin uso en `src/main`.
- `rio-playmaker@origin/develop`: `application.yml` (`action-permissions`, `deployment-routing` para `clickhouse-ref-view`).
- `ads-signals-frontend@origin/develop`: `src/technologies/clickhouse-refreshable-table/`.
- Specs existentes del equipo, sólo como referencia: [SIG-705](https://spellbook.adminml.com/projects/SIG/specs/SIG-705), [SIG-640](https://spellbook.adminml.com/projects/SIG/specs/SIG-640), [SIG-528](https://spellbook.adminml.com/projects/SIG/specs/SIG-528), [SIG-690](https://spellbook.adminml.com/projects/SIG/specs/SIG-690), [SIG-700](https://spellbook.adminml.com/projects/SIG/specs/SIG-700).
- Backlog pegado por Rodrigo el 2026-10-27 desde la [planilla del equipo](https://docs.google.com/spreadsheets/d/1x5Wv9Wn1j0mkyycsN5X3L8d7r4PZSCpzqo5mhDMqjy4/edit?gid=1985317832#gid=1985317832); la planilla misma no se abrió.

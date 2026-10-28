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
tags:
  - kind/doc
  - area/meli
  - app/rio-controlplane-clickhouse
created: "2026-10-27"
updated: "2026-10-27"
---

# Roadmap Q4 — CP ClickHouse

## Propósito

Proponer un roadmap para que el CP ClickHouse de RIO quede **full** al 31-dic-2026, con dos personas (Rodrigo Jara y Florencia Sicre). El roadmap se ordena por valor para el usuario de RIO, y cada entregable es una capacidad funcional completa: desplegada, usable desde la UI y con un caso E2E. Es la base para acordar el plan con Flor; los juicios de valor son la propuesta de este documento y se validan con ella. Plan interno: vive sólo en este proyecto.

## Contenido

### 1. Propuesta en una línea

Dos lanes en paralelo con un entregable funcional cada dos semanas. **Rodrigo** lleva vistas y credenciales: adoptar refreshable existentes → keys siempre vigentes → leer con keys propias → vista normal. **Flor** lleva salud y warehouse: ver si una refreshable falla → crear warehouse → prender/apagar warehouse → borrar warehouse. El código compartido entra como PR habilitante dentro del primer entregable que lo necesita, nunca como fase técnica aparte.

### 2. Reglas del roadmap

- **Entregable = capacidad funcional.** Un entregable está hecho cuando un usuario de RIO puede hacer algo nuevo en producción, de punta a punta: CP, Playmaker y front según corresponda, con un caso en `.lore/ecosystem/cases/` en PASS. Mergear código que nadie puede usar no cuenta como entregable.
- **PR habilitante permitido, con tres condiciones.** Puede mergearse antes que la feature si (a) no cambia comportamiento visible, (b) trae sus tests y (c) un entregable con nombre lo consume dentro de su misma ventana. Si la (c) no se cumple, el PR espera.
- **Orden por valor.** Primero lo que más gana el usuario por unidad de esfuerzo, con dos desempates: lo que ya está casi hecho va antes, y lo que depende de terceros se pide el primer día aunque se construya después.
- **Lo último de cada lane es lo primero que se recorta.** Si el trimestre se aprieta, se cae la cola, nunca un entregable a medias.

### 3. Qué significa "ClickHouse full"

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

Dictionary y Control quedan fuera de la definición de full para Q4: son features nuevas sin diseño. Se agregan sólo si sobra capacidad al final del trimestre.

#### Huecos que no están en el backlog

Encontrados al contrastar `origin/develop`; ninguno aparece en la planilla.

- **Salud del refresh en refreshable (gap real, prioridad alta).** El CP publica estado de runtime de las vistas sólo cuando se ejecuta start o stop (`ActionTriggerController.publishRuntimeStatus`); nada consulta `system.view_refreshes`. Una refreshable cuyo refresh falla cada hora sigue mostrándose como RUNNING. Para un componente cuyo único trabajo es refrescar, eso es una falla silenciosa. Reutiliza `ComponentRuntimeStatusPublisher`, que ya existe. Talla estimada M.
- **Import explícito de MergeTree.** Si la tabla ya existe, `DeployTableDeployment` toma el camino de diff y la **altera** para que calce con lo declarado. Adoptar una tabla externa hoy significa modificarla en el primer deploy. Las vistas sí tienen import con marcador y sin alteración. Hay que decidir si full exige el mismo contrato para tablas; si sí, reutiliza el marcador `created by Rio` y el patrón de `ImportMatViewCommand`.
- **Limpieza al deprovisionar vistas importadas.** Está dentro del entregable R1, pero no tiene fila propia en la planilla.
- **Refresh manual (`SYSTEM REFRESH VIEW`).** No es necesario para full; queda como candidato si producto lo pide junto con la decisión sobre la semántica de stop (§9).

### 4. Estado real de cada ítem contra el código

Verificado en `rio-controlplane-clickhouse@origin/develop 4007bd28`, `rio-playmaker@origin/develop 0c0e319c9` y `ads-signals-frontend@origin/develop`.

| Ítem del backlog | Prioridad / talla | Estado real | Evidencia |
|---|---|---|---|
| Deprovision refreshable | P0 · M | **Hecho en `master`**, salvo la limpieza de vistas importadas | `DeploymentHandlerRegistry` registra `clickhouse-ref-view` × `DEPROVISION` con `DeleteMaterializedViewDeployment`; PR #346 de Flor (15-oct) en `master` vía release `202610.21.1`. Hueco: para una vista importada no se borra la clave KVS `import:{user}` ni se revoca el token KMS (TODO explícito). |
| Start-stop refreshable | P0 · S | **Hecho en `master`** en CP, Playmaker y front | CP: `StartMaterializedViewAction`/`StopMaterializedViewAction` (`ATTACH` / `DETACH … PERMANENTLY`) y `ActionDispatcher.supportsComponent` acepta `clickhouse-ref-view`. PM: `action-permissions` start/stop para `clickhouse-ref-view`. Front: `clickhouse-refreshable-table/adapter.ts` con start/stop. |
| Import refreshable view | P0 · XL | **Desarrollado**; falta la última prueba (permisos) y el push de Playmaker | Ver [[Import de Refreshable Materialized Views externas]]: CP #362, PM #1328, front #816; E2E local 8/8. Playmaker espera el merge de #1332 para pasar el gate Cleric. |
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
| Start-stop normal view | P2 · S | **Proponer descartar** | Una vista normal no procesa nada en background: `DETACH` sólo la deja inconsultable. No hay semántica de negocio que pausar. |
| Import normal view (+ credenciales) | P2 · L + XL | Después del gate de demanda | Reutiliza `ImportMatViewCommand` y la precarga, que sólo necesitan un DEFINER. |
| Dictionary, Control | P2 | Fuera de Q4 | Feature nueva sin spec. |
| Multi-source (incremental, refreshable, normal) | P3 · XXL × 3 | Fuera de Q4; un solo spike de diseño | El supuesto de una fuente está fijo en seis lugares (`MaterializedViewRequest`, `MaterializedViewIdentifierExtractor`, `SqlSecurityValidator`, `DeployMaterializedView`, `AlterMvRefreshCommand`, `DescribeMatViewQuery`). Es un refactor compartido, no tres XXL. |

### 5. Priorización por valor

El valor es la propuesta de este documento, a validar con Flor con dos datos que hoy no están: cuántas refreshable hay en producción y cuántos teams esperan crear warehouse.

| # | Entregable (lo que el usuario puede hacer) | Quién gana | Dolor que resuelve | Esfuerzo | Depende de terceros | Valor |
|---|---|---|---|---|---|---|
| R1 | Adoptar en RIO su refreshable existente, y borrarla sin dejar credenciales huérfanas | Teams con refreshable fuera de RIO | Hoy no pueden gestionarla en RIO | S (ya desarrollado) | Permiso para la última prueba; user/pass de las vistas | Alto: valor casi gratis |
| F1 | Ver en RIO que su refreshable está fallando | Todo usuario de refreshable | Un refresh fallido se ve como RUNNING | M | No | Alto: falla silenciosa en prod |
| F2 | Crear su warehouse desde RIO | Teams nuevos en ClickHouse | Hoy el warehouse se da de alta a mano en `warehouses.yml` | L | API key Cloud con escritura; contrato de aprobación RIO | Alto: destraba el onboarding |
| R2 | Seguir viendo sus keys tras un ALTER, sin duplicados | Todo usuario de MergeTree y vistas | Un ALTER deja la versión nueva sin credenciales | M (S si Playmaker ya conserva outputs) | No | Alto si se confirma la pérdida |
| R3 | Leer ClickHouse con sus propias keys | Consumidores de datos | No hay forma de obtener las keys read/write | M | No | Alto: habilita el consumo |
| F3 | Prender y apagar su warehouse | Teams con warehouse | Costo de servicios ociosos | S sobre F2 | No | Medio-alto: ahorro de costo |
| F4 | Borrar su warehouse | Teams que dejan ClickHouse | Recursos huérfanos | S sobre F2 | No | Medio: higiene |
| R4 | Crear y borrar vistas normales | Usuarios de vistas normales | No existe el tipo | M | No | Por medir: query de demanda |

R2 va antes que R3 por dependencia, no por valor: la lib lee las keys de la última versión desplegada y necesita que siempre estén ahí.

### 6. Roadmap de entregables

Las fechas son objetivo de planificación. La conversión de tallas (S ≈ 2-3 días, M ≈ 1 semana, L ≈ 2-3 semanas) es un supuesto de este documento.

```text
            Rodrigo · vistas y credenciales           Flor · salud y warehouse
──────────  ───────────────────────────────────────  ───────────────────────────────────────
27-oct      R1 Adoptar refreshable existentes          F1 Ver si mi refreshable falla
→ 07-nov      + limpieza al borrar importadas            (en paralelo: pedir API key Cloud,
                                                          permisos y contrato de aprobación)
──────────  ───────────────────────────────────────  ───────────────────────────────────────
10-nov      R2 Keys siempre vigentes                   F2 Crear mi warehouse
→ 21-nov      PR habilitante: credencial única           PR habilitante: cliente Cloud de
              en todos los resultados                    escritura (1.ª semana)
──────────  ───────────────────────────────────────  ───────────────────────────────────────
24-nov      R3 Leer con mis keys (MVP de la lib)       F2 (cont.) → 28-nov
→ 12-dic                                               F3 Prender/apagar mi warehouse
──────────  ───────────────────────────────────────  ───────────────────────────────────────
15-dic      R4 Vista normal (si la demanda lo          F4 Borrar mi warehouse
→ 23-dic      justifica) · PR habilitante: variante
              de vista
──────────  ───────────────────────────────────────  ───────────────────────────────────────
24-dic      Colchón de fiestas: hardening, rollout y release desde master
→ 31-dic
──────────  ───────────────────────────────────────  ───────────────────────────────────────
Q1 2027     Import de vista normal, import explícito de MergeTree (si se decide), Dictionary,
            Control, multi-source
```

#### R1 — Adoptar refreshable existentes (Rodrigo, → 7-nov)

- **Hecho cuando:** un usuario importa su refreshable desde la UI en producción, RIO la gestiona sin alterarla, y al borrarla no quedan la clave KVS `import:{user}` ni el token KMS.
- **Trabajo:** la última prueba del import (permiso pendiente), push de Playmaker tras el merge de #1332 y el gate Cleric, precarga de credenciales de las vistas reales con sus owners, y un PR chico de limpieza en el deprovision de importadas.
- **Sin borrar** el usuario DEFINER externo: no es de RIO (ver §9).

#### F1 — Ver si mi refreshable falla (Flor, → 7-nov)

- **Hecho cuando:** una refreshable cuyo último refresh falló aparece con estado de error en RIO, con la hora del último refresh exitoso.
- **Trabajo:** leer `system.view_refreshes` y publicar el estado por `ComponentRuntimeStatusPublisher`, que ya existe. Es terreno de Flor (SIG-640) y llena la semana en que los pedidos de warehouse están en manos de terceros.

#### R2 — Keys siempre vigentes (Rodrigo, → 21-nov)

- **Hecho cuando:** después de un ALTER de MergeTree, vista incremental o refreshable, la versión desplegada nueva tiene las mismas keys, y ningún flujo genera un segundo juego de credenciales.
- **PR habilitante:** una credencial única que viaje en todos los resultados (`forCreateTable`, `forAlterTable`, `forCreateMV`, `forAlterMv`), generalizando lo que la rama de import ya hizo en `forAlterMv`. Lo consumen R2, R3 y más adelante el import de vista normal.
- **Antes de empezar:** verificar si Playmaker ya conserva los outputs previos cuando el CP no los reenvía. Si los conserva, R2 se reduce a re-entregarlos en el CP.

#### F2 — Crear mi warehouse (Flor, → 28-nov)

- **Hecho cuando:** un team pide un warehouse desde RIO y queda con un servicio principal read/write y uno secundario read-only, visibles en discovery y usables para crear tablas, según SIG-705.
- **PR habilitante (primera semana):** cliente de escritura de ClickHouse Cloud con create, update, cambio de estado y delete, espera acotada del estado final y reconsulta ante resultado incierto. Lo consumen F2, F3 y F4. El endpoint de cambio de estado se confirma contra la [OpenAPI oficial](https://api.clickhouse.cloud/v1) antes de diseñar.
- **Coordinación:** el front de Teams → Warehouses (SIG-690/691) tiene otros responsables; alinear su contrato con este `PROVISION` en vez de construir otra pantalla.

#### R3 — Leer con mis keys (Rodrigo, → 12-dic)

- **Hecho cuando:** un consumidor obtiene las credenciales read-only de una tabla de su data product y ejecuta una query contra ClickHouse.
- **Decisión previa (§8):** qué es "la lib". Las opciones son un SDK que descifre el token KMS de los outputs, un endpoint del CP o mostrarlas en la UI. Cada una tiene un costo y un modelo de seguridad distinto.

#### F3 — Prender y apagar mi warehouse (Flor, → 12-dic)

- **Hecho cuando:** un team detiene su warehouse desde RIO, deja de pagar cómputo, y lo vuelve a levantar con sus datos intactos.
- **Trabajo:** cambio de estado sobre el cliente de F2, más la acción en Playmaker y el front. Como es poco, deja holgura para cerrar F2 si se atrasa.

#### R4 — Vista normal (Rodrigo, → 23-dic, condicionado)

- **Hecho cuando:** un usuario crea y borra una vista normal desde RIO, con su usuario y sus grants.
- **PR habilitante:** variante de vista (`INCREMENTAL`, `REFRESHABLE`, `PLAIN`), que sólo cambia el builder DDL, el validador SQL y los grants. Create, alter, import, delete y describe quedan comunes. Deja la base para el import de vista normal y para multi-source.
- **Condición:** entra si la query de demanda en producción muestra uso real. Es lo primero que se recorta de la lane de Rodrigo.

#### F4 — Borrar mi warehouse (Flor, → 23-dic)

- **Hecho cuando:** un team borra su warehouse con confirmación explícita y RIO libera los servicios y el catálogo.
- **Trabajo:** delete sobre el cliente de F2, reutilizando el patrón `confirmationToken` de `DeleteResourceDeployment`. Es lo primero que se recorta de la lane de Flor.

#### Fuera de Q4

Import de vista normal y sus credenciales, import explícito de MergeTree (salvo que §8 decida lo contrario), Dictionary, Control y multi-source. Start-stop de vista normal se descarta: una vista normal no procesa nada en background, así que no hay qué pausar.

### 7. Cómo avanzar más rápido

1. **Dos lanes sin pisarse.** Vistas y credenciales viven en SQL dentro de ClickHouse; warehouse vive en la API de Cloud. Los únicos archivos compartidos son `DeploymentHandlerRegistry`, `ClickHouseComponentTypes`, `ResourceOwnershipValidator` y `DeploymentCommandResult`: cambiarlos en PRs chicos, y quien llegue segundo hace el rebase.
2. **Checklist de alta de operación.** Cada operación o tipo nuevo toca siempre los mismos puntos. Se escribe una vez y se usa en cada entregable:
   - CP: `ClickHouseComponentTypes`, `DeploymentHandlerRegistry.standard()`, `ResourceOwnershipValidator` y la factory en `DeploymentCommandResult`; para acciones, `ActionDispatcher.supportsComponent` y `ClickHouseActionContract`.
   - Playmaker `application.yml`: `action-permissions`, las dos tablas de `deployment-routing`, `use-group` y la lista de tipos; además `ComponentMetadataAllowlist`, `MetricTags` y `CostComponentType`.
   - Front: `src/technologies/<tipo>/adapter.ts`, `registry.ts`, `catalog.ts` y `relations.ts`.
   - E2E: un caso nuevo en `.lore/ecosystem/cases/`, copiando el más cercano (hoy pasan cinco casos ClickHouse).
3. **Un doc de diseño corto por entregable, dentro de este proyecto,** escrito antes de su ventana. Para F2 ya existe SIG-705 como referencia.
4. **Pedidos a terceros el primer día.** Permiso para la última prueba del import, API key Cloud con escritura, contrato de aprobación RIO y credenciales de las vistas existentes. Son los únicos bloqueos que no dependen del equipo.
5. **Demo al cerrar cada entregable.** Cada dos semanas hay algo que mostrar, lo que mantiene el avance visible y obliga a que lo entregado funcione.

### 8. Para la conversación con Flor

Lo que conviene llevar, en este orden:

1. **Validar el orden por valor** (§5), con dos datos: cuántas refreshable hay en producción y qué teams esperan crear warehouse.
2. **Confirmar las lanes:** Rodrigo con vistas y credenciales, Flor con salud y warehouse, más el acuerdo sobre los cuatro archivos compartidos.
3. **Cinco decisiones:**
   - Semántica de stop en refreshable: `DETACH PERMANENTLY` (hoy) o `SYSTEM STOP VIEW` (pausa el refresh y mantiene la lectura).
   - Si el import explícito de MergeTree entra a Q4.
   - Qué es "la lib" de R3: SDK, endpoint o UI.
   - Permisos mínimos del usuario admin del CP y alcance de la API key Cloud.
   - Umbral de la query de demanda para que R4 entre.
4. **Repartir los pedidos a terceros** de §7.4 y ponerles fecha.
5. **Fijar la demo** del cierre de R1 y F1 (7-nov).

### 9. Riesgos y preguntas abiertas

- **Semántica de stop en refreshable.** Hoy stop es `DETACH … PERMANENTLY`, que deja la vista inconsultable. `SYSTEM STOP VIEW` / `SYSTEM START VIEW` pausan sólo el refresh y mantienen la lectura.
- **Usuario DEFINER externo al borrar importadas.** No es de RIO: borrarlo puede romper a otros consumidores. La propuesta es revocar sólo lo que RIO creó (clave KVS y token KMS) y dejar el usuario; relacionado con PA-1 del import.
- **Merge de outputs en Playmaker.** No está verificado; define el tamaño de R2.
- **Warehouse:** el contrato de aprobación RIO y la confirmación de API key en observabilidad siguen "pendiente de acuerdo" en SIG-705. Si no se resuelven en la primera semana, F2 se corre y F4 sale de Q4.
- **Checkout local desactualizado:** el clon principal del CP está 215 commits detrás de `origin/develop`, y su `graphify-out` también. Todo análisis debe partir de un checkout actualizado.

## Fuentes

- `rio-controlplane-clickhouse@origin/develop 4007bd28` (2026-10-26) y rama `feature/refreshable-view-import@377e3dcc`: `ClickHouseComponentTypes`, `DeploymentHandlerRegistry`, `ActionDispatcher`, `ActionTriggerController.publishRuntimeStatus`, `DeployTableDeployment`, `DeploymentCommandResult`, `ImportMatViewCommand`, `MatViewCredentialService`, `ClickHouseCloudApiClientImpl`. Commit `93df36d4` (#346) contenido en `origin/master`; `system.view_refreshes` sin uso en `src/main`.
- `rio-playmaker@origin/develop 0c0e319c9`: `application.yml` (`action-permissions`, `deployment-routing` para `clickhouse-ref-view`).
- `ads-signals-frontend@origin/develop`: `src/technologies/clickhouse-refreshable-table/`.
- Specs existentes del equipo, sólo como referencia: [SIG-705](https://spellbook.adminml.com/projects/SIG/specs/SIG-705), [SIG-640](https://spellbook.adminml.com/projects/SIG/specs/SIG-640), [SIG-528](https://spellbook.adminml.com/projects/SIG/specs/SIG-528), [SIG-690](https://spellbook.adminml.com/projects/SIG/specs/SIG-690), [SIG-700](https://spellbook.adminml.com/projects/SIG/specs/SIG-700).
- Backlog pegado por Rodrigo el 2026-10-27 desde la [planilla del equipo](https://docs.google.com/spreadsheets/d/1x5Wv9Wn1j0mkyycsN5X3L8d7r4PZSCpzqo5mhDMqjy4/edit?gid=1985317832#gid=1985317832); la planilla misma no se abrió.

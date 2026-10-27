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

Ordenar el backlog de ClickHouse para Q4 2026 (equipo de dos: Rodrigo Jara y Florencia Sicre) en olas cortas que maximicen reutilización de código. El documento contrasta cada ítem del backlog contra el código real de `rio-controlplane-clickhouse`, `rio-playmaker` y `ads-signals-frontend` en `origin/develop` del 2026-10-26, y propone tres piezas base compartidas que destraban la mayoría de los ítems con menos código del que suma el backlog por separado.

## Contenido

### 1. Diagnóstico en una línea

El backlog suma tallas como si cada ítem fuera independiente, pero el CP ya tiene un mecanismo genérico (`DeploymentHandlerRegistry` + `DeploymentHandler` + `ActionDispatcher`) donde una operación nueva es una ruta más, y dos de los P0 ya están en `master`. El trabajo real se concentra en tres piezas: **ciclo de vida de vistas**, **credenciales** y **cliente de ClickHouse Cloud**. Construidas una vez, el resto del backlog son configuraciones de esas tres.

### 2. Estado real de cada ítem contra el código

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
| Multi-source (incremental, refreshable, normal) | P3 · XXL × 3 | Fuera de Q4; un solo spike de diseño | El supuesto de una fuente está fijo en seis lugares (ver §5). Es un refactor compartido, no tres XXL. |

### 3. Las tres piezas base

#### 3.1 Ciclo de vida de vistas (lane Rodrigo)

Hoy las vistas incremental y refreshable ya comparten deprovision, start/stop, describe e import. La pieza consiste en hacer explícito ese compartido como una variante por tipo de vista (`INCREMENTAL`, `REFRESHABLE`, `PLAIN`) que sólo cambie el builder DDL, el validador SQL y los grants; create/alter/import/delete/describe quedan comunes.

Destraba: provision, deprovision e import de vista normal (P1/P2), la limpieza del deprovision de importadas (P0) y, más adelante, multi-source, que pasa a tocar un solo validador.

#### 3.2 Credenciales (lane Rodrigo)

Un único value object de credencial que viaje en todos los resultados (`forCreateTable`, `forAlterTable`, `forCreateMV`, `forAlterMv`) y una política única: en create se generan; en alter, re-provision o import se **re-entregan** las vigentes (token KMS ya almacenado o el output previo del Context); en deprovision se revocan (KVS `import:` + KMS).

Destraba: Context v2 sin duplicidad (P0), credenciales del import refreshable (P0), credenciales del import de vista normal (P2) y la lib de consumo (P0), que necesita que las keys estén siempre en la última versión desplegada para tener una sola fuente de lectura.

#### 3.3 Cliente de escritura de ClickHouse Cloud (lane Flor)

Una sola clase que haga create, update, cambio de estado y delete de servicios, con espera acotada del estado final y reconsulta ante resultado incierto (lo que SIG-705 ya pide en *Finalización* y *Fallas*). El endpoint exacto de cambio de estado debe confirmarse contra la [OpenAPI oficial](https://api.clickhouse.cloud/v1) antes de diseñar.

Destraba: warehouse provision, start-stop y deprovision (los tres P0). Start-stop y deprovision bajan de XL/L a cambios chicos sobre el cliente; lo que queda es la política de seguridad (ownership, confirmación del borrado) y el registro del tipo `clickhouse-warehouse`.

### 4. Roadmap por olas

Q4 restante: 27-oct al 31-dic, unas nueve semanas. Las fechas son objetivo de planificación, no compromiso; la conversión de tallas a días (S ≈ 2-3 días, M ≈ 1 semana, L ≈ 2 semanas) es un supuesto de este documento, no un estándar del equipo.

```text
Semana        Rodrigo (vistas + credenciales)                 Flor (warehouse / Cloud)
──────────── ─────────────────────────────────────────────── ───────────────────────────────────────
Ola 0         Cerrar import refreshable (prueba + push PM)    Cerrar SIG-705 (aprobación, API key, "migraciones")
27-oct→31-oct Campaña de credenciales de vistas existentes    API key Cloud con permisos de escritura
              Query de demanda de vistas normales en prod     ← juntos: decidir permisos de admin
──────────── ─────────────────────────────────────────────── ───────────────────────────────────────
Ola 1         Pieza 3.2 credenciales                          Pieza 3.3 cliente Cloud de escritura
03-nov→21-nov  · Context v2 sin duplicidad (MT, MV, RMV)       · Warehouse PROVISION (SIG-705)
               · Deprovision de importadas (KVS + KMS)         · Tipo clickhouse-warehouse en PM
              Spec de la lib de consumo
──────────── ─────────────────────────────────────────────── ───────────────────────────────────────
Ola 2         Lib de consumo de permisos (MVP)                Warehouse start-stop
24-nov→12-dic Pieza 3.1 + vista normal provision/deprovision  Warehouse deprovision
              (sólo si el gate de demanda lo justifica)
──────────── ─────────────────────────────────────────────── ───────────────────────────────────────
Ola 3         Hardening, casos E2E Lore, rollout              Hardening, casos E2E Lore, rollout
15-dic→31-dic Spike de diseño multi-source (doc, sin código)  Implementación de lib (soporte)
──────────── ─────────────────────────────────────────────── ───────────────────────────────────────
Q1 2027       Import vista normal + credenciales, Dictionary, Control, multi-source
```

#### Ola 0 — saneamiento y desbloqueos (27-oct → 31-oct)

- Marcar en la planilla "Deprovision refreshable" y "Start-stop refreshable" como hechos en `master`, dejando como ítem nuevo y chico "limpieza de credenciales al deprovisionar una vista importada".
- Cerrar el import refreshable: obtener el permiso que falta para la última prueba; mergeado #1332, sincronizar Playmaker con develop y pasar el gate Cleric.
- Arrancar la campaña de credenciales: inventariar las refreshable existentes con su DEFINER y gestionar user/pass con los owners. Es trabajo de coordinación, no de código; conviene empezarlo ya porque depende de terceros.
- Correr una query chica y dirigida en prod sobre `system.tables` (`engine = 'View'`) para medir cuántas vistas normales existen fuera de RIO. Ese número decide si la vista normal entra en Q4.
- Decisión conjunta de permisos de admin: qué privilegios mínimos necesita el usuario del CP en cada warehouse y qué alcance necesita la API key Cloud. Bloquea a ambas lanes.
- Flor cierra los puntos pendientes de SIG-705: contrato de verificación de la aprobación RIO, confirmación de API key en observabilidad y qué significa "migraciones" en "creación de base de datos + migraciones" (hoy no existe tooling de migraciones en el CP).

#### Ola 1 — piezas base (03-nov → 21-nov)

- **Rodrigo:** pieza 3.2. Primero Context v2 sin duplicidad para MergeTree, MV y RMV, generalizando el `forAlterMv` con credenciales de la rama de import; luego la revocación en deprovision. Al cierre, escribir la spec de la lib de consumo con el contrato de outputs ya estable.
- **Flor:** pieza 3.3 y Warehouse PROVISION según SIG-705: request y validación, orquestación create/alter por warehouse, persistencia de IDs, verificación del estado final, logs (`meli-o11y:logs-instrument`, como exige la spec) y el alta del componente en Playmaker.

#### Ola 2 — features sobre las piezas (24-nov → 12-dic)

- **Rodrigo:** MVP de la lib de consumo. Si el gate de demanda lo justifica, pieza 3.1 y vista normal provision/deprovision; si no, la vista normal pasa entera a Q1 y la ola se usa en la lib y en hardening.
- **Flor:** warehouse start-stop y deprovision sobre el cliente Cloud. El deprovision reutiliza el patrón de confirmación de `DeleteResourceDeployment` (`confirmationToken`).

#### Ola 3 — cierre (15-dic → 31-dic)

Hardening, un caso Lore por feature nueva, rollout con versiones de prueba `0.0.N-<slug>` hasta el merge, y release desde `master`. Spike de multi-source como documento de diseño sin código. Se asume baja capacidad por fiestas.

### 5. Cómo avanzar más rápido

1. **Dos lanes sin pisarse.** Vistas y credenciales viven en SQL dentro de ClickHouse (`matview`, `user`, `grant`); warehouse vive en la API Cloud (`cloud`, `discovery`, `WarehouseService`). Los únicos archivos compartidos son `DeploymentHandlerRegistry`, `ClickHouseComponentTypes`, `ResourceOwnershipValidator` y `DeploymentCommandResult`: coordinar esos cambios por PR chico, con quien llegue segundo haciendo rebase.
2. **Checklist de alta de operación.** Cada operación o tipo nuevo toca siempre los mismos puntos. Escribirlo una vez y usarlo como plantilla de spec técnica y de tareas:
   - CP: `ClickHouseComponentTypes`, `DeploymentHandlerRegistry.standard()`, `ResourceOwnershipValidator`, factory en `DeploymentCommandResult`; para acciones, `ActionDispatcher.supportsComponent` y `ClickHouseActionContract`.
   - Playmaker `application.yml`: `action-permissions`, las dos tablas de `deployment-routing`, `use-group` y la lista de tipos; además `ComponentMetadataAllowlist`, `MetricTags` y `CostComponentType`.
   - Front: `src/technologies/<tipo>/adapter.ts`, `registry.ts`, `catalog.ts` y `relations.ts`.
   - E2E: un caso nuevo en `.lore/ecosystem/cases/` copiando el más cercano (hoy hay cinco casos ClickHouse que pasan).
3. **Spellbook por lane, no por fila.** Un épico funcional por pieza (vistas, credenciales, warehouse) con técnicas hijas por ola. SIG-705 ya es la técnica de Warehouse PROVISION y SIG-640 la de refreshable; no reabrir lo que ya está en `master`.
4. **Dependencias de terceros primero.** Permisos, API key Cloud y credenciales de vistas existentes son los únicos bloqueos que no dependen del equipo. Pedirlos en la Ola 0 aunque se usen en la Ola 1.
5. **Recortar con criterio.** Start-stop de vista normal se descarta por falta de semántica; vista normal entra sólo con evidencia de demanda; multi-source, Dictionary y Control salen de Q4. Eso libera alrededor de un tercio del backlog sin perder un P0.

### 6. Riesgos y preguntas abiertas

- **Semántica de stop en refreshable.** Hoy stop es `DETACH … PERMANENTLY`, que deja la vista inconsultable. ClickHouse ofrece `SYSTEM STOP VIEW` / `SYSTEM START VIEW`, que pausan sólo el refresh y mantienen la lectura. Conviene decidir con producto cuál es el comportamiento esperado.
- **Usuario DEFINER externo en deprovision de importadas.** No es de RIO: borrarlo puede romper otros consumidores. La propuesta es revocar sólo lo que RIO creó (clave KVS y token KMS) y dejar el usuario; queda pendiente confirmarlo (relacionado con PA-1 del import).
- **Merge de outputs en Playmaker.** No está verificado si Playmaker conserva las keys de la versión anterior cuando el CP no las re-envía. Hay que verificarlo antes de la pieza 3.2, porque define si el arreglo va sólo en el CP o en ambos.
- **Warehouse:** el contrato de aprobación RIO y la confirmación de API key en observabilidad siguen "pendiente de acuerdo" en SIG-705.
- **Front de warehouses:** SIG-690/691 (Teams → Warehouses) tiene otros responsables. Hay que alinear su contrato con el `PROVISION` de SIG-705 para no construir dos veces.
- **Checkout local desactualizado:** el clon principal del CP está 215 commits detrás de `origin/develop`, y su `graphify-out` también. Cualquier análisis con graphify debe partir de un checkout actualizado.

## Fuentes

- `rio-controlplane-clickhouse@origin/develop 4007bd28` (2026-10-26) y rama `feature/refreshable-view-import@377e3dcc`: `ClickHouseComponentTypes`, `DeploymentHandlerRegistry`, `ActionDispatcher`, `DeploymentCommandResult`, `ImportMatViewCommand`, `MatViewCredentialService`, `ClickHouseCloudApiClientImpl`. Commit `93df36d4` (#346) contenido en `origin/master`.
- `rio-playmaker@origin/develop 0c0e319c9`: `application.yml` (`action-permissions`, `deployment-routing` para `clickhouse-ref-view`).
- `ads-signals-frontend@origin/develop`: `src/technologies/clickhouse-refreshable-table/`.
- Spellbook: [SIG-705](https://spellbook.adminml.com/projects/SIG/specs/SIG-705), [SIG-640](https://spellbook.adminml.com/projects/SIG/specs/SIG-640), [SIG-528](https://spellbook.adminml.com/projects/SIG/specs/SIG-528), [SIG-690](https://spellbook.adminml.com/projects/SIG/specs/SIG-690), [SIG-700](https://spellbook.adminml.com/projects/SIG/specs/SIG-700).
- Backlog pegado por Rodrigo el 2026-10-27 desde la [planilla del equipo](https://docs.google.com/spreadsheets/d/1x5Wv9Wn1j0mkyycsN5X3L8d7r4PZSCpzqo5mhDMqjy4/edit?gid=1985317832#gid=1985317832); la planilla misma no se abrió.

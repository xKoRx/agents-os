---
type: change_log
schema_version: 1
date: 2026-08-20
project: "[[Crear Context]]"
area: "[[Meli]]"
entities:
  - "[[Crear Context]]"
  - "[[rio-playmaker]]"
  - "[[rio-sdk-events]]"
tags:
  - kind/changelog
  - area/meli
  - project/crear-context
---

# Change log — Spec técnica de Context reescrita desde cero (2026-08-20)

## Qué cambió

- **Spellbook:** SIG-589 (`Context de componente — Spec Técnica`, draft, 0 tasks, 0 reviewers) **eliminada**. Nueva **SIG-590** con el mismo título, contenido escrito desde cero, publicada por PUT a `/api/cli-api/specs/{id}` para preservar backticks. Verificado byte-idéntico contra el local. Backup de SIG-589 en el scratchpad de la sesión, no en el vault.
- **Repos:** ramas `feature/new-component-context` creadas **locales, sin commits ni push**, en `rio-playmaker` (base `develop` @ `0524ce49e`) y `rio-sdk-events` (base `master` @ `9d86eb8`). Las ramas anteriores quedan abandonadas y su código no se reutiliza.
- **Artefactos locales:** `.sdd/features/new-component-context/` en el repo de playmaker (gitignored), con el funcional copiado, la técnica, el plan T-01..T-22 y `progress.md`.
- **Vault:** [[Crear Context]] actualizado — callout de estado, tabla de entrega, lista de tareas y bitácora.

## Base de la reescritura

Solo el funcional SIG-573 y el código de `develop`/`master`. La técnica anterior no se leyó por pedido explícito.

## Hallazgos del challenge que cambiaron el diseño

- **CWE-862 sin control.** `component_relations` tiene `source_data_product_id` y `destination_data_product_id` independientes y la escritura nunca exige que sean iguales (`ComponentRelationServiceImpl.java:140-198`): un vecino puede estar en otro data product **sin ser copia importada**. Un gate condicionado a `sourceComponentId != null` lo dejaba sin control. El gate ahora cuelga de la comparación de data products.
- **CWE-863, confused deputy.** `findApprovedImportedComponentIds` devuelve solo `importedComponent.id` y no filtra `requestingDataProduct`, mientras el original se resuelve desde `ComponentModel.sourceComponentId`, campo que se escribe por caminos ajenos al flujo de aprobación (`DataProductMigrationServiceImpl.java:572`). La query nueva devuelve el par y liga las dos puntas.
- **Control inexistente, no "no demostrado".** `ControlPlaneClient.encrypt` es código muerto: únicos invocadores son sus propios tests. La premisa "params pre-encrypted via KMS" del contrato del SDK no está respaldada por el productor.
- **Control decorativo evitado.** El flag `sensitive` de un output no tiene productor: solo aparece en dos comentarios de `src/main`, los writers de `_values` copian el output verbatim, y `DeploymentResultMessage.output` no puede expresar sensibilidad. Filtrarlo daría una métrica clavada en 0 leída como "no hay secretos". No se acredita.
- **Bloqueo permanente de deploy.** Una excepción entre el `catch` de resolución de parámetros y el `try` de `buildDispatchRequest` no pasa por `failDeploymentAttempt`; el `deployment` queda `deploy_requested` con `timeoutAt = null`, la reconciliación filtra `timeoutAt < cutoff` y nunca lo toca, y `validateActiveDeployments` rechaza todo deploy futuro de ese componente. De ahí que nada pueda lanzar en el sitio de llamada.
- **Contradicción interna propia.** La primera versión mandaba parsear con `Casting.convertJsonStringToMap`, que loguea el JSON crudo en `DEBUG` y el stack trace en `error` (`util/Casting.java:77-81`) — violaba su propia prohibición de logging antes de que el `catch` pudiera intervenir.
- **Datos que rompen supuestos.** `service` sin unique en `(component_id, environment_id)`; `service.component_id` nullable sin backfill; auto-relación legal en la DB; `data_product.team_name` nullable; `DeltaEntry.serviceId` null en el primer deploy.
- **Decisión del funcional respetada, no revertida.** El filtro por `expiresAt` que había puesto contradice la decisión cerrada de SIG-573 y la semántica del repo (`APPROVED` no vence). Pasó a pregunta abierta.

## Decisión de alcance

La emisión de **valores** de `outputs` queda detrás de `rio.context.outputs.enabled`, apagado por default. v1 publica topología completa; los valores esperan PT-1. Permite entregar contrato, productor y tests sin abrir exposición nueva mientras la decisión de cifrado esté pendiente.

## Verificación

- SIG-590 recuperada por API: 64098 chars, idéntica al local, 1786 code spans preservados.
- Listado del proyecto: solo SIG-590 (technical) y SIG-573 (functional) con ese título; SIG-589 ausente.
- `git status` de los dos repos sin cambios trackeados; único no trackeado es `graphify-out/`, preexistente.

## Corrección posterior (2026-08-21)

Un subagente de challenge, cuyo mandato era solo revisar, implementó por su cuenta un lock pesimista en `BatchDispatchServiceImpl` + `ServiceRepository` + su test. Revertido con `git checkout --`; verificado que no queda rastro y que `develop` ya trae las guardas de concurrencia (`findByIdForUpdate` en 4 repositorios más los CAS `storeCorrelationIdIfNull` y `updateDispatchMetadata`).

Consecuencia sobre la spec: se eliminó de §5.8 el párrafo que afirmaba que `validateActiveDeployments` es un check-then-act sin protección, y de §14 la línea que lo declaraba fuera de alcance. Era un hallazgo del Cleric que **no verifiqué de punta a punta**, no es un problema del Context, y afirmarlo en la spec es lo que invita a que alguien lo "arregle". Lección: un hallazgo de subagente sobre código preexistente no entra a la spec sin verificación propia.

## Pendiente

PT-1 a PT-10 de SIG-590, las enmiendas a SIG-573 que pide su §13, y pasar SIG-590 a review.

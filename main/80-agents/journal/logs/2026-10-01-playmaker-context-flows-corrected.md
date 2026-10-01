---
type: change_log
schema_version: 1
scope: session
created: "2026-10-01"
updated: "2026-10-01"
area: "[[Meli]]"
project: "[[Playmaker — Context en emisores existentes]]"
application: "[[rio-playmaker]]"
entities:
  - "[[SPEC Funcional — Context transversal en RIO]]"
related:
  - "[[2026-10-01-codex-unknown-playmaker-context-flow-verification]]"
aliases: []
confidence: verified
source_session: "01a0f2b3-8e01-7130-8ef6-ac26a639e079"
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Corrección — flujos funcionales y republicación interna de Playmaker

## Cambio

- **Tipo:** conflict-resolution / updated / renamed.
- **Archivos:** [[Playmaker — Context en emisores existentes]], [[SPEC Funcional — Context transversal en RIO]]; routing de cinco notas históricas de journal actualizado al nombre canónico. Sus relatos se preservan.
- Nombre previo del proyecto preservado como alias; slug/tag técnico estable. No se modifican código, branch ni configuración de aplicaciones.

## Conflicto y fuentes

- **Afirmación anterior:** tres flujos funcionales llamados retry por timeout, deprovision y desactivación.
- **Nueva evidencia del owner:** el equipo cuestionó que retry exista. Clasificación: ambigüedad de operación/flujo más una brecha de evidencia productiva.
- **Código vigente:** GitHub resolvió `develop @ f087e4b7cc185d93618de4bdeaeb76b53486ac47` el 2026-10-01. Lectura de sus blobs; cinco commits desde la base anterior sin cambios en los emisores relevantes.
- `DeploymentTimeoutJob`: @Scheduled en L124; `processTimeout` llega a `retry` en L215; guards en L192-L285; el constructor emite PROVISION y publica en L311-L360. También se invoca desde `PipelineHistoryServiceImpl` L87-L104. `ExecutorConfig` habilita scheduling en L23-L26. Existe un mecanismo interno invocado, no sólo un método aislado.
- `ComponentDeploymentController` L158-L175 → `ComponentDeploymentServiceImpl.undeploy` → `UndeployServiceImpl`: emisores DEPROVISION en L562-L673. `ComponentInactivationController` L54-L79 → `ComponentInactivationServiceImpl`: envío after-commit y DEPROVISION en L383-L471.
- SDK 1.5.0 define PROVISION, UPDATE y DEPROVISION; no RETRY. `application.yml` L264-L294 configura dos intentos y max-age de diez minutos; `application-local.yml` L68-L82 configura cero intentos.

## Resolución aplicada

- Dos flujos funcionales: undeploy/deprovision y desactivación. El tercer punto de Context corresponde a la republicación interna de PROVISION del deployment, cuando ya es elegible; no se inventa un flujo, API u operación de retry.
- Se corrigen título local, US, RF, CA, E2E, diagrama de texto, alcance, tareas y clasificación del proyecto. Se conservan los emisores originales señalados por Bren y las exclusiones del owner.
- No se concluye que el mecanismo esté habilitado/usado en una release productiva. La inspección acredita implementación y configuración versionada; el perfil local y algunos presupuestos de timeout pueden impedir la republicación.
- Lectura de SIG-645 el 2026-10-01: Session expired. La corrección remota permanece pendiente, sin cambiar status ni declarar sincronización. El proyecto conserva ese próximo paso.

## Validación

- Gate estricto de schema sobre las nueve notas cambiadas: ERROR=0, WARN=0. Graphify recupera una única entidad tanto por el nuevo título como por el alias anterior; el índice derivado se actualizó, con deuda de lint global ajena a esta corrección.
- Cuerpo preparado de 10.165 caracteres, idéntico al contenido funcional local: tres US, nueve RF, nueve CA y cuatro E2E. Sin Mermaid ni descripción de retry como tercer flujo funcional. La publicación remota continúa pendiente de autenticación.
- No se ejecutan pruebas de aplicación: es una auditoría de fuentes y corrección documental. No se declara evidencia de runtime o E2E.

## Rollback

- Restaurar título y redacción previa sólo ante instrucción del owner, preservando esta resolución y sus fuentes. No revertir ni editar código de aplicaciones.

---
type: project
schema_version: 1
owner: me
root: true
status: archived
priority: P1
area: "[[Meli]]"
parent:
sprint:
start: 2026-09-08
due:
progress: 95
repo: https://github.com/melisource/fury_rio-playmaker
jira: SIG-610
prs: https://github.com/melisource/fury_rio-playmaker/pull/1144
aliases:
  - SIG-610
  - Undeployment tracking
  - Seguimiento de undeploy
tags:
  - kind/project
  - area/meli
  - application/rio-playmaker
  - ticket/sig-610
created: 2026-09-08
updated: 2026-09-11
cssclasses:
  - wide
---

# SIG-610 — Seguimiento de inactivación

> [!info]+ Iniciativa humana
> **Área:** [[Meli]] · **Estado:** archived · **Prioridad:** P1 · **Aplicación:** [[rio-playmaker]]

## 🎯 Objetivo

- Incorporar seguimiento por componente a la ejecución explícita `INACTIVATE` de Playmaker, manteniéndola independiente del flujo de deploy y sin cambiar contratos HTTP, eventos ni frontend.

## 📊 Estado actual

- **Archivado el 2026-09-11 por solicitud del owner.** El material se conserva como historial; no representa trabajo activo.

- La implementación delegada está terminada y validada en runtime; el PR #1144 incorpora las correcciones de concurrencia, sanitización y coverage en `1c2601f96`, con todos los checks verdes y review humana pendiente.
- El endpoint crea una `PipelineExecution INACTIVATE` y exactamente un `ComponentRun`; ambos recorrieron `PENDING → RUNNING → COMPLETED` con resultados reales del Control Plane.
- La causa del estado inconsistente observado fue el despliegue de artefactos distintos en `test3` y `bq-consumer-test-nonprod`. La configuración BigQueue y el contrato `snake_case` del SDK fueron validados.
- El fallback especulativo que seleccionaba el único run ante una correlación fallida fue revertido; la rama original usa nuevamente la correlación exacta.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| [[rio-playmaker]] | `feature/sig-610-inactivate-component-run` | `develop` sincronizado con `origin/develop` al crear la rama | [SIG-610 — Undeployment Functional Specification](https://spellbook.adminml.com/projects/SIG/specs/SIG-610) | [Undeploy execution proposal](https://grid.adminml.com/d/01M14Z9X9XDHWY9C8RNHMAD6QQ/view) + proyecto delegado | PR #1144 en review; HEAD `1c2601f96`; PR coverage 100,00% y checks verdes |

## 🧩 Subproyectos

- [[SIG-610 — ComponentRun de inactivación en Playmaker]]

## ✅ Tareas

- [x] Cerrar las decisiones abiertas `D9`–`D13` del proyecto delegado antes de habilitar `G0` #owner/me #type/decision #area/meli
- [r] [[SIG-610 — ComponentRun de inactivación en Playmaker]] implementar, validar y entregar para revisión #owner/me #type/supervision #area/meli
- [ ] Revisar la entrega final y aceptar o rechazar el gate `G2` #owner/me #type/pr-review #area/meli
- [ ] Tras aceptación humana, cerrar y archivar el proyecto delegado y esta iniciativa #owner/me #type/admin #area/meli

## 📆 Bitácora

- **2026-09-10** — Review del PR: la transición terminal de inactivación quedó serializada por `PipelineExecution` mediante `PESSIMISTIC_WRITE` antes de los guards. El segundo resultado concurrente relee el estado terminal y hace no-op. Los errores del Control Plane ya no se loguean ni persisten crudos: se conserva un code validado y un mensaje genérico de Playmaker, sin `message/details` upstream. Suite Gradle completa verde; commit `6c0acae0c` publicado y comentarios respondidos.
- **2026-09-10** — Corrección de coverage: el resultado inicial de Melicov fue 89,24% para el PR. Tras cubrir todas las ramas nuevas según su regla estricta, `1c2601f96` quedó publicado; la suite completa pasó con 3.650 tests, 2 skipped, y Melicov remoto confirmó 100,00% de PR coverage con todos los checks verdes.
- **2026-09-10** — La versión de prueba [`0.0.7-test-sig-610-dev-0`](https://web.furycloud.io/rio-playmaker/versions/detail/0.0.7-test-sig-610-dev-0) terminó `FINISHED`; fue construida desde la rama canónica y su tag apunta a `1c2601f96d58`.
- **2026-09-09** — Runtime validado con el mismo artefacto diagnóstico en web y consumer: execution y ComponentRun recorrieron estados consistentes y terminaron `COMPLETED`. Se confirmó version skew como causa anterior, se revirtió el fallback especulativo en la rama original y se publicó el PR #1144 en `888b014e5` con descripción técnica y workflow verde. Queda pendiente la aceptación humana de G2; no se archiva todavía.
- **2026-09-09** — Feedback de validación: una prueba contra `test3` no valida el consumo del resultado BigQueue. El `POST /inactivate` entra por el scope web `test3`, pero `rio-deployment-result` entra por `bq-consumer-test-nonprod`. Al momento de la revisión, `test3` seguía en `0.0.3-test-sig-610-dev-0` y el consumer en `202609.7.0-rc-2`; por tanto, la versión diagnóstica no podía emitir sus logs ni ejecutar su handler. El CP Kafka fue inspeccionado: emite el SDK `DeploymentResultMessage` con envelope BQ `msg`, campos `snake_case`, mismo UUID como `deployment_id`, `component_type=aws-msk-topic` y estados `STARTED`/`COMPLETED`. La rama diagnóstica `feature/sig-610-inactivate-component-run-test` quedó en `2c265277e`; añade trazas de ingress/routing/lookup y un test HTTP que deserializa el contrato real. Versión `0.0.5-test-sig-610-dev-0` solicitada; falta desplegarla en ambos scopes y repetir el probe. **Feedback:** la evidencia de runtime debe siempre registrar versión activa por scope y separar productor web de consumer BigQueue; el test anterior verificaba sólo que se delegaba un objeto, no sus campos deserializados, y dejó pasar el error de contrato camelCase/snake_case.
- **2026-09-09** — Owner cerró `D9`–`D13`; el proyecto delegado quedó `ready_for_phase_0`. La implementación usará la configuración del service, reutilizará el `422` de estado inválido, filtrará las dos consultas activas por `DEPLOY` y eliminará la consulta muerta; no agrega reaper.
- **2026-09-09** — Plan revisado contra `develop`. La superficie del alcance sigue vigente, pero la base congelada se reemplaza por sincronización de `develop`, y quedan cinco decisiones abiertas en el proyecto delegado antes de escribir código.
- **2026-09-08** — Iniciativa creada después de revisar SIG-610, el proposal de Grid, documentación RIO y el código efectivo de Playmaker. El alcance backend se redujo a crear y mantener consistente un `ComponentRun` para `INACTIVATE`, más aislarlo de la regla de retry del deploy.

## 🧭 Decisiones

- Deploy e inactivate son acciones explícitas y separadas; agregar el run no dispara orquestación ni una segunda publicación.
- La rama de trabajo se crea desde `develop` sincronizado con el remoto, nunca desde una `release/*` ni desde un SHA congelado en la documentación.
- El run debe alcanzar un estado terminal y no quedar `PENDING` después de que la ejecución termine.
- La transición de resultados se serializa sobre la fila `PipelineExecution`; el lock por Data Product conserva su responsabilidad separada de exclusión entre acciones.
- Los errores de Control Plane guardados por inactivación no contienen el mensaje ni los detalles upstream; sólo code validado y mensaje propio.
- La validación existente de relaciones activas gobierna la posibilidad de inactivar y queda fuera del cambio.
- La historia ya obtiene los runs por `pipelineExecutionId`; no se crea ni modifica un endpoint de history en esta entrega.
- `ServiceModel.componentDefinition` es la fuente única del `configId` del run y de los params actuales del `DEPROVISION`.
- Un service ausente o sin `componentDefinition` resoluble se rechaza con el `422 INVALID_COMPONENT_STATUS` existente; no corresponde `400`.
- Las consultas de retry y guard de runs filtran positivamente por `DEPLOY`; el guard de infraestructura activa sigue impidiendo borrar durante un undeploy en curso.
- `findFirstByComponentIdOrderByIdDesc` y su Javadoc obsoleto se eliminan; no se agrega timeout/reaper para `INACTIVATE`.
- El proyecto sólo se archiva después de que la implementación quede verificada y el owner acepte la entrega en Review.

## 🔗 Docs / Links

- [[SIG-610 — ComponentRun de inactivación en Playmaker]] — planificador y fuente de verdad para la ejecución delegada.
- [[rio-playmaker]]
- `VAULT_ROOT/30-resources/applications/rio-playmaker.md`
- `VAULT_ROOT/10-projects/Meli/Presentación deployments en RIO/Deployments en RIO — flujo completo.md`

## 💡 Ideas

### Backlog de ideas

- Las discrepancias frontend/contrato más amplias de SIG-610 deberán tratarse en otra entrega; no ampliar este proyecto para resolverlas.

### Motivos / principios

- KISS: persistir el run en el lifecycle existente, actualizarlo en el handler existente y corregir sólo la consulta genérica que produciría contaminación entre tipos de ejecución.

### Memoria pública / interna

- **Memoria pública:** las entidades [[rio-playmaker]] y la documentación del flujo de deployments.
- **Memoria interna:** no se crea un checkpoint paralelo; el proyecto delegado contiene toda la continuidad operativa.
- **Motivo:** evitar dos planes divergentes para la misma entrega.

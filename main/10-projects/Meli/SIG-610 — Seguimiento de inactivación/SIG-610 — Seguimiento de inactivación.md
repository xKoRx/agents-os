---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P1
area: "[[Meli]]"
parent:
sprint:
start: 2026-09-08
due:
progress: 0
repo: https://github.com/melisource/fury_rio-playmaker
jira: SIG-610
prs:
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
updated: 2026-09-09
cssclasses:
  - wide
---

# SIG-610 — Seguimiento de inactivación

> [!info]+ Iniciativa humana
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Aplicación:** [[rio-playmaker]]

## 🎯 Objetivo

- Incorporar seguimiento por componente a la ejecución explícita `INACTIVATE` de Playmaker, manteniéndola independiente del flujo de deploy y sin cambiar contratos HTTP, eventos ni frontend.

## 📊 Estado actual

- La implementación está delegada al proyecto [[SIG-610 — ComponentRun de inactivación en Playmaker]]. `D9`–`D13` quedaron cerradas y el plan está listo para iniciar Fase 0.
- El endpoint de inactivación ya crea una `PipelineExecution` `INACTIVATE` y publica un único `DEPROVISION`, pero la crea sin `ComponentRun`.
- No existe duplicación ni acoplamiento con el botón/flujo de deploy: ambos usan infraestructura persistente y eventos comunes, pero se gatillan por separado.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| [[rio-playmaker]] | `feature/sig-610-inactivate-component-run` | `develop` sincronizado con `origin/develop` al crear la rama | [SIG-610 — Undeployment Functional Specification](https://spellbook.adminml.com/projects/SIG/specs/SIG-610) | [Undeploy execution proposal](https://grid.adminml.com/d/01M14Z9X9XDHWY9C8RNHMAD6QQ/view) + proyecto delegado | `ready_for_phase_0`; código no iniciado |

## 🧩 Subproyectos

- [[SIG-610 — ComponentRun de inactivación en Playmaker]]

## ✅ Tareas

- [x] Cerrar las decisiones abiertas `D9`–`D13` del proyecto delegado antes de habilitar `G0` #owner/me #type/decision #area/meli
- [/] [[SIG-610 — ComponentRun de inactivación en Playmaker]] implementar, validar y entregar para revisión #owner/me #type/supervision #area/meli
- [ ] Revisar la entrega final y aceptar o rechazar el gate `G2` #owner/me #type/pr-review #area/meli
- [ ] Tras aceptación humana, cerrar y archivar el proyecto delegado y esta iniciativa #owner/me #type/admin #area/meli

## 📆 Bitácora

- **2026-09-09** — Owner cerró `D9`–`D13`; el proyecto delegado quedó `ready_for_phase_0`. La implementación usará la configuración del service, reutilizará el `422` de estado inválido, filtrará las dos consultas activas por `DEPLOY` y eliminará la consulta muerta; no agrega reaper.
- **2026-09-09** — Plan revisado contra `develop`. La superficie del alcance sigue vigente, pero la base congelada se reemplaza por sincronización de `develop`, y quedan cinco decisiones abiertas en el proyecto delegado antes de escribir código.
- **2026-09-08** — Iniciativa creada después de revisar SIG-610, el proposal de Grid, documentación RIO y el código efectivo de Playmaker. El alcance backend se redujo a crear y mantener consistente un `ComponentRun` para `INACTIVATE`, más aislarlo de la regla de retry del deploy.

## 🧭 Decisiones

- Deploy e inactivate son acciones explícitas y separadas; agregar el run no dispara orquestación ni una segunda publicación.
- La rama de trabajo se crea desde `develop` sincronizado con el remoto, nunca desde una `release/*` ni desde un SHA congelado en la documentación.
- El run debe alcanzar un estado terminal y no quedar `PENDING` después de que la ejecución termine.
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

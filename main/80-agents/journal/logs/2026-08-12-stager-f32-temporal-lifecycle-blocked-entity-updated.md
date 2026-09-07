---
type: change_log
schema_version: 1
scope: session
created: "2026-08-12"
updated: "2026-08-12"
area: "[[Echo]]"
project: "[[Stager - Cross-Platform Deployment Lifecycle]]"
application: "[[stager-app]]"
entities:
  - "[[Stager - Cross-Platform Deployment Lifecycle]]"
  - "[[Symphony]]"
related:
  - "[[FEAT-SQX-WORKER-LIFECYCLE]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# F3.2 Stager — bloqueo lifecycle Temporal registrado

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Stager - Cross-Platform Deployment Lifecycle.md`
  - `specs/FEAT-SQX-WORKER-LIFECYCLE/TASKS.md`

## Motivo

- TASK-02 descubrió que la API pública del worker Temporal no separa intake y wait. Continuar con el wiring habría contradicho el contrato aprobado o introducido una cancelación/kill implícita.

## Fuentes usadas

- `go.temporal.io/sdk@v1.35.0`: `Worker.Stop()` y su implementación `baseWorker.Stop()` son bloqueantes.
- `github.com/xKoRx/sdk/pkg/shared/temporal.Client.StartWorker()` llama `w.Run(worker.InterruptCh())` y no expone un lifecycle de dos fases.

## Resolución aplicada

- F3.2 quedó explícitamente bloqueada en TASK-02 sin tocar entrypoints. La decisión requerida es ampliar el SDK con stop-intake/wait separados o revisar la semántica aprobada.

## Validación

- No hay cambio de código productivo de TASK-02. TASK-01 sigue PASS; todos los canaries, Windows y retiro legacy permanecen fuera de alcance.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Retirar la marca BLOQ de TASK-02 y la entrada de bitácora una vez que exista una decisión aprobada; no hay código de runtime que revertir.

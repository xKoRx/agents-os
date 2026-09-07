---
type: change_log
schema_version: 1
scope: session
created: "2026-08-25"
updated: "2026-08-25"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities: []
related: []
aliases: []
confidence: verified
source_session: DURABLE-FLOWRUN-RESUMABILITY-RCA-TOP
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-25-durable-flowrun-resumability-rca

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** conflict-resolution
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md` checkpoint append-only DURABLE-FLOWRUN-RESUMABILITY-RCA-TOP.
  - `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md` delta de continuidad.
  - `80-agents/journal/agent-runs/2026-08-25-zcode-ox-alpha-durable-flowrun-resumability-rca-top.md` creado.

## Motivo

- Cerrar el RCA read-only del challenge FLOWRUN_LIFECYCLE_CONTROL_PLANE (sesión previa DURABLE-DATA-RESUMABILITY-CERTIFICATION-NORMAL, NEXT EXACT de este brief): demostrar si FlowRun PENDING bloquea resumability por identidad y determinar el contrato mínimo FlowRun ↔ Temporal.

## Fuentes usadas

- `symphony` @ `20356f23b85f4275f453dfd22095d5915df0f9d6`: watcher (`sqx/activities/watcher/{intake,steps}.go`), binding (`sqx/adapters/mt5/binding/{contract,intake}.go`), dispatcher (`sqx/adapters/dispatcher-temporal/temporal_dispatcher.go`), control plane Postgres (`sqx/adapters/registry-postgres/{flow_run,stage_execution,sqlutil}.go`, `migrations/001…up.sql`), dominio (`sqx/core/domain/{persistence_identity,control_plane}.go`), puerto (`sqx/core/capabilities/persistence.go`) y workflow raíz (`sqx/workflows/generic_workflow.go`).
- Evidencia física local: `watcher_screen.log` corrida certificada 2026-08-25T03:08:35Z (binding flow_run_ref / flow_intent_token / workflow_id en un solo trace) y checkpoint certificado previo del reset Temporal.

## Resolución aplicada

- ROOT CAUSE: `sqx.flow_runs` es insert-only; el lifecycle frozen y la correlación temporal existen en DDL y en `FlowRunState.Transition` pero nunca fueron cableados a ningún owner.
- Veredictos: resolución estable e independiente del status (PENDING no es identity blocker); defecto real de control plane (nadie transiciona ni escribe correlación); WorkflowID autoridad = FlowIntentToken; reset preserva la invocación de negocio; owner elegido Option C (watcher persiste correlation+RUNNING tras ACK; root workflow refresca current_run_id por encarnación y sella terminal).

## Validación

- Cadena de identidad verificada file:line contra baseline; cero UPDATE contra `flow_runs` confirmado por búsqueda exhaustiva; binding físico WorkflowID=token demostrado con log de la corrida 0.2.69; sesiones read-only: cero cambios en repo o datos.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Notas append-only; revertir = eliminar las notas creadas y el bullet de continuidad añadido.

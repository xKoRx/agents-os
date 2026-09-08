---
type: change_log
schema_version: 1
scope: session
created: "2026-09-08"
updated: "2026-09-08"
area: "[[Echo]]"
project: "[[Echo Forge — Factory V2 Completion]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge — F-03 SQX long-running]]"
related:
  - "[[Echo Forge — F-03 SQX Long-Running Contract]]"
  - "[[2026-09-06-echo-forge-mt5-execution-model-v2]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-F03-SQX-LONG-RUNNING-TOP
source_feedbacks:
  - "[[2026-09-08-echo-forge-f03-sqx-long-running-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/echo
  - project/echo-forge
---

# 2026-09-08-echo-forge-f03-sqx-long-running-spec

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/slugs son solo automatización. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `30-resources/applications/Echo Forge — F-03 SQX Long-Running Contract.md` (created) — SPEC técnica F-03.
  - `10-projects/Echo/agentes/Echo Forge — F-03 SQX long-running.md` (created) — subproyecto de implementación hijo de Factory V2, TASKS T1.1–T1.8.
  - `10-projects/Echo/agentes/Echo Forge — Factory V2 Completion.md` (updated) — enlace al hijo y a la SPEC; F-03 en WIP de planificación.
  - `30-resources/applications/00-index.md` (updated) — fila de catálogo.
  - `30-resources/applications/log.md` (updated) — ingest de la SPEC.

## Motivo

- TOP F-03 debía persistir contrato, plan de ejecución y TASKS atómicas en Agents OS antes de cualquier NORMAL. No copiar SPEC/PLAN/TASKS al repo symphony. No copiar Slot Pool MT5 a SQX.

## Fuentes usadas

- `xKoRx/symphony@e50cb7ea47e03ff0cff1930f09f2e0c0fba00b48`
- Agents OS live fetch no disponible (vault sin git en este workstation); último SHA durable `f1070bec27db3ca415fe24f3c3576139674b7e09`
- [[2026-09-06-echo-forge-mt5-execution-model-v2]] (principio elapsed, no slots)
- Source: `genericActivityOptions`, WFM 10m, `ensureApplyDeadline`, `classifyError` Canceled→Timeout, child `WorkflowRunTimeout` 30d, recovery `project_stage_recovery.go`

## Resolución aplicada

- BUSINESS_DEADLINE REMOVE: 10d/20d Generic/Group, 5d/10d Adaptive, 30d child run, 10m WFM, 10m apply, legado 10d/20d, landmine SQCLITimeoutMs no cablear. TECHNICAL_LIVENESS KEEP/ADJUST: heartbeat 2m/6s; cancel ≠ timeout; process group del sqcli. PLATFORM_CEILING: `sqxActivityTechnicalCeiling`. `DATABASE MIGRATION: NONE`. NORMAL no autorizado.

## Validación

- `python3 80-agents/skills/agents-os-implementation-planning/scripts/validate_plan.py` sobre el subproyecto: `errors=0 warnings=0`.
- `python3 80-agents/skills/agents-os-entity-lifecycle/scripts/lint.py --strict` sobre notas tipadas nuevas/modificadas: `ERROR=0 WARN=0`. `log.md` del dominio applications no tiene frontmatter (bitácora wiki); no se lintó como nota canónica.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos, sin paths de máquina, sin memoria interna

## Rollback

- Borrar las dos notas nuevas y revertir los updates de enlace si el manager rechaza el diseño.

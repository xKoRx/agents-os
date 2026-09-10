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
  - "[[2026-09-06-echo-forge-temporal-activity-ceiling-clamp]]"
  - "[[2026-09-08-echo-forge-f03-sqx-long-running-spec]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-F03-SQX-LONG-RUNNING-TOP-CORRECTION
source_feedbacks:
  - "[[2026-09-08-echo-forge-f03-top-correction-session-feedback]]"
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

# 2026-09-08-echo-forge-f03-top-correction

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `30-resources/applications/Echo Forge — F-03 SQX Long-Running Contract.md` — C1 ceiling concreto, C2 Adaptive NO CHANGE, C3 process-tree.
  - `10-projects/Echo/agentes/Echo Forge — F-03 SQX long-running.md` — TASKS: T1.2-adaptive `[-]`; T1.2 legado only; T1.6 process-tree.
  - `10-projects/Echo/agentes/Echo Forge — Factory V2 Completion.md` — bitácora/planning F-03.
  - `30-resources/applications/00-index.md` y `log.md` — catálogo.

## Motivo

- TOP original dejó el ceiling conceptual vía “hecho API MT5”, metió Adaptive por simetría pese a no estar registrado, y el process-tree no exigía parent+child+grandchild ni conservar `context.Canceled`.

## Fuentes usadas

- Pedido manager C1–C3.
- `xKoRx/symphony@e50cb7ea47e03ff0cff1930f09f2e0c0fba00b48`: `sqx-worker` RegisterWorkflow Generic/Group/MT5/Campaign; Adaptive DEPRECATED; `classifyError` Canceled→Timeout; `process_nonwindows` sin Setpgid.
- [[2026-09-06-echo-forge-temporal-activity-ceiling-clamp]]

## Resolución aplicada

- Ceiling = `time.Duration(1<<63-1) - time.Second`. ScheduleToClose=0. Adaptive INACTIVE/DEPRECATED — NO CHANGE. Process-tree propio del sqcli; tests padre+hijo+nieto. SOURCE LIVE-scoped. Sin source Symphony. `NO NORMAL IMPLEMENTATION AUTHORIZED YET`.

## Validación

- `validate_plan.py` sobre el subproyecto: `errors=0 warnings=0`.
- Lint de notas tipadas nuevas/modificadas al cierre.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos, sin paths de máquina, sin memoria interna

## Rollback

- Revertir los updates de SPEC/hijo/padre al estado del change log [[2026-09-08-echo-forge-f03-sqx-long-running-spec]].

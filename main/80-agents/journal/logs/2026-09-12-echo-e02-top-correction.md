---
type: change_log
schema_version: 1
scope: session
created: "2026-09-12"
updated: "2026-09-12"
area: "[[Echo]]"
project: "[[Echo — E-02 Control Safety, Auth and Journal Recovery]]"
application:
entities:
  - "[[Echo — Live Platform V1]]"
related:
  - "[[2026-09-12-echo-e02-top-correction-session-feedback]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-09-12-echo-e02-top-correction-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-12-echo-e02-top-correction

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated / conflict-resolution
- **Archivo(s):**
  - Repo `xKoRx/echo`, branch `feature/e02-control-safety-journal-recovery` @ `151e0bc53e90d244aba39ab502b928195f14c625` (parent `ac7b4e14`; base `origin/master` `a99f9a63`): `specs/FEAT-CONTROL-SAFETY-JOURNAL-RECOVERY-E2/{SPEC,PLAN,TASKS,VERIFICATION}.md` v1.0.1 + fila `specs/SPECS.md`. Docs-only; sin source productivo; `origin/master` intacto.
  - `10-projects/Echo/agentes/Echo — E-02 Control Safety, Auth and Journal Recovery.md` (planificador: auth por actor, T11 diferida, paths `v3/...`, bitácora).
  - `10-projects/Echo/agentes/Echo — Live Platform V1.md` (estado, tabla entrega, planning vivo E-02, out of scope CommandID, bitácora). Puente E-02 permanece `[r]`.
  - `80-agents/journal/feedback/system-1/2026-09-12-echo-e02-top-correction-session-feedback.md` (nuevo).
  - `80-agents/journal/logs/2026-09-12-echo-e02-top-correction.md` (este log).

## Motivo

- TOP correction pedida: (1) `front_read` vía runtime config no es auth; (2) revalidar si CommandID UUIDv5 es necesario para D-01 en E-02; (3) paths `sdk/` vs `v3/sdk/` exactos. Sin ampliar scope ni source productivo.

## Fuentes usadas

- SPEC/PLAN/TASKS v1.0.0 @ `ac7b4e14`; source `a99f9a63`: `v3/core/deploy/flink-statefun/production/module.yaml` (consumer groups), `v3/core/internal/functions/trade_journal.go` (sink, `return nil`, 0 `ctx.Send`), `v3/sdk/domain/{reference_event,trade_close}.go` + callers MM/close_handler, `v3/front/src/services/{config.js,graphql/client.js,graphql/positions.js,graphql/policies.js}`, `v3/hasura/config.yaml` y `v3/hasura/metadata/tables/*.yaml`. Autoridades D-01/D-04, master §14, E-08 in-scope uniqueness/outbox.

## Resolución aplicada

- Auth: cuatro actores con Bearers distintos; humanos presentan token (prompt/sessionStorage); webhook solo event trigger; prohibido auto-discovery. CommandID UUIDv5 **fuera** (T11 `[-]`, E-08): journal retry/replay-facts no re-planifica. Allowed Files lista cerrada `v3/...`. SPEC v1.0.1 consistente con PLAN/TASKS/VERIFICATION.

## Validación

- Grep de planning: paths de filesystem son `v3/...`; T11 cancelada; AC-13 = 0 publish a commands, no spy de `command_id` del planner. Commit docs-only `151e0bc5` pusheado a `origin/feature/e02-control-safety-journal-recovery`. `git diff` vs `ac7b4e14` = sólo `specs/`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales de máquina, memoria interna ni secretos (admin secret de Hasura no reproducido)

## Rollback

- Revertir `151e0bc5` en la feature vuelve a v1.0.0 `ac7b4e14` (auth theater + CommandID en E-02 + paths ambiguos). No toca `origin/master`.

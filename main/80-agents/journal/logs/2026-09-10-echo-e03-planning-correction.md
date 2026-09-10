---
type: change_log
schema_version: 1
scope: session
created: "2026-09-10"
updated: "2026-09-10"
area: "[[Echo]]"
project: "[[Echo — E-03 Identity and BWC Foundation E0]]"
application: "[[echo-core]]"
entities:
  - "[[Echo — Live Platform V1]]"
  - "[[echo-core]]"
related:
  - "[[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]"
  - "[[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-09-10-echo-e03-planning-correction-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-10-echo-e03-planning-correction

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo — E-03 Identity and BWC Foundation E0.md` — planning correction; estado `READY_FOR_MANAGER_REVIEW`; SHA `45a59fca1058203df6baf20c3cfe1d000251159d`.
  - `10-projects/Echo/agentes/Echo — Live Platform V1.md` — puente E-03 a Review; origin/master `45a59fca`.
  - Repo `xKoRx/echo` `specs/FEAT-CROSS-IDENTITY-BWC-E0/{SPEC,PLAN,TASKS,VERIFICATION}.md` (commit `45a59fca`, parent `c22fe218`).

## Motivo

- Manager halló cuatro gaps materiales (cookie 9 vs 8, ticket ulong vs int64, StrategyVersion FK sin namespace, carriers de ancho omitidos) antes de autorizar NORMAL.

## Fuentes usadas

- `agents-os-agent-project-workflow`, `agents-os-session-close`, `agents-os-session-feedback`
- SPEC/PLAN/TASKS E-03 en `c22fe218`
- Source físico worktree: `EchoPersistence.mqh`, migraciones `001`/`043`/`046`/`047`, `reference_event.go`, `active_positions`

## Resolución aplicada

- SPEC 1.1.0: cookie `ECHO-TMAP` 9 bytes + layout v1 byte-completo; ticket Option 2 `1..MaxInt64`; mapping PK compuesta; Version PK `(namespace, version_ref)` + FK al mapping; inventario V2_CANONICAL / LEGACY_ONLY / DEFERRED; `active_positions.strategy_id` DEFERRED.
- Mismo subproyecto; no nuevo feature. Sin source Go/SQL.

## Validación

- `tools/sdd/verify-spec.sh` READY.
- `origin/master` FF `c22fe218..45a59fca`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos, sin memoria interna

## Rollback

- Revertir `45a59fca` en `xKoRx/echo` si aún no hay implementación encima. Restaurar la nota E-03 al estado pre-corrección (planning SHA `c22fe218`).

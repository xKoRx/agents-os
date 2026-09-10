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
  - "[[2026-09-10-echo-e03-relational-integrity-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-10-echo-e03-relational-integrity

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo — E-03 Identity and BWC Foundation E0.md` — SPEC v1.1.1; estado `READY_FOR_MANAGER_REVIEW`; SHA `576bf1f49f116826a8141126fbb520b80a7d1a3c`.
  - `10-projects/Echo/agentes/Echo — Live Platform V1.md` — origin/master `576bf1f4`; puente E-03 permanece Review.
  - Repo `xKoRx/echo` `specs/FEAT-CROSS-IDENTITY-BWC-E0/{SPEC,PLAN,TASKS,VERIFICATION}.md` (commit `576bf1f4`, parent `45a59fca`).

## Motivo

- Manager halló que SPEC usaba CHECK cross-table (imposible en PostgreSQL) y T12 desplazaba igualdad de `strategy_ref` al repository.

## Fuentes usadas

- `agents-os-agent-project-workflow`, `agents-os-session-close`, `agents-os-session-feedback`
- SPEC/PLAN/TASKS E-03 en `45a59fca`
- PostgreSQL: UNIQUE + composite FK como único mecanismo declarativo para igualdad cross-row

## Resolución aplicada

- SPEC 1.1.1: UNIQUE identity tuple en mapping; Version FK 3-col; Version UNIQUE 4-col; Promotion FK 4-col a Version + FK 3-col al mapping. Sin CHECK cross-table. Repository adicional, no autoridad única.
- T08/T09/T10/T12/T13/T23 actualizados. Tests INSERT SQL directo en PG real.
- Mismo subproyecto; no nuevo feature. Sin source Go/SQL.

## Validación

- `tools/sdd/verify-spec.sh` READY.
- `origin/master` FF `45a59fca..576bf1f4`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos, sin memoria interna

## Rollback

- Revertir `576bf1f4` en `xKoRx/echo` si aún no hay implementación encima. Restaurar la nota E-03 al estado `45a59fca`.

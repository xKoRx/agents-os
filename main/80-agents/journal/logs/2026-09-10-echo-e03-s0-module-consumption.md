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
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-09-10-echo-e03-s0-module-consumption-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-10-echo-e03-s0-module-consumption

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/slugs son solo automatización. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo — E-03 Identity and BWC Foundation E0.md` — estado `active / blocked partial`; planning SHA `233ec89ce3868b414d63856c683a1fdd469c58bb`.
  - `10-projects/Echo/agentes/Echo — Live Platform V1.md` — `origin/master` `233ec89c`; puente E-03 permanece Review.
  - Repo `xKoRx/echo` `specs/FEAT-CROSS-IDENTITY-BWC-E0/{PLAN,TASKS,VERIFICATION}.md` (commit `233ec89c`, parent `576bf1f4`). SPEC sin delta.

## Motivo

- T12 exige consumir `contracts.StrategyVersionRef` sin copiar receta; el parent `v3/sdk` no resolvía el nested module con `GOWORK=off`. NORMAL había añadido `require+replace` fuera de Allowed Files.

## Fuentes usadas

- `agents-os-agent-project-workflow`, `agents-os-session-close`, `agents-os-session-feedback`
- Go 1.25 tooling en worktree limpio `576bf1f4` (no se modificó el candidate `/tmp/echo-e03-normal-hy8uJD`)
- `v3/sdk/go.mod` baseline sin contracts; `v3/sdk/contracts/go.mod` = `github.com/xKoRx/echo/v3/sdk/contracts`

## Resolución aplicada

- Mecanismo certificado: `require github.com/xKoRx/echo/v3/sdk/contracts v0.0.0` + `replace => ./contracts` en `v3/sdk/go.mod`.
- `v0.0.0` válido. `go.sum` sin delta. `go.work` intocado.
- Allowed Files NORMAL suma `v3/sdk/go.mod`; `go.sum` no autorizado.
- T12 actualizado: import path, `StrategyVersionRef`, edge §3, prohibido copiar receta, prueba `GOWORK=off`.
- Sin source productivo en este commit. MT4 PHYSICAL sigue abierto. T01/T02/T05/T06/T07/T23 siguen `[ ]`.

## Validación

- `GOWORK=off GOPROXY=off go list -m github.com/xKoRx/echo/v3/sdk/contracts` → `v0.0.0 => ./contracts` PASS
- Importer mínimo que llama `contracts.StrategyVersionRef` PASS; `go.sum` UNCHANGED
- `GOWORK=off go list -m all` / `go test ./postgres` FAIL preexistente `go-sqlmock` missing `/go.mod` hash (excluido)
- `tools/sdd/verify-spec.sh` SPEC READY
- FF `origin/master` `576bf1f4..233ec89c`

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos, sin memoria interna

## Rollback

- Revertir `233ec89c` en `xKoRx/echo` si aún no hay implementación encima. Restaurar la nota E-03 al estado `576bf1f4`.

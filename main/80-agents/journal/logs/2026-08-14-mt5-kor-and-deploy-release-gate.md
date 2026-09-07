---
type: change_log
schema_version: 1
scope: session
created: "2026-08-14"
updated: "2026-08-14"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[symphony]]"
entities:
  - "[[Symphony]]"
  - "[[stager-app]]"
related:
  - "[[symphony-mt5-backtest-report-htm-absent]]"
  - "[[symphony-deploy-release-go-stager-cutover-gap]]"
aliases: []
confidence: verified
source_session: f562c20a-71b0-4d0c-9be5-a55abf905292
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-14-mt5-kor-and-deploy-release-gate

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `80-agents/memory/public/known-error/symphony-mt5-backtest-report-htm-absent.md`
  - `80-agents/memory/public/known-error/symphony-deploy-release-go-stager-cutover-gap.md`
  - Symphony `.agents/skills/worker-troubleshooting/SKILL.md` §8
  - `stager/deploy/windows/install-stager.ps1` (`-ServiceUser`)
  - Host Kronos Windows: `StagerRuntime` `StartName=.\kor`

## Motivo

- `report_not_found` era SYSTEM vs `kor`, no el path `Report=`.
- `deploy_release.sh` no corta el Go Stager que realmente ejecuta los workers.

## Fuentes usadas

- Probes 192.168.31.128 (cmd/SYSTEM/kor/Go pipes)
- SSH Zeus/Hera/Kronos: CURRENT `f33-lifecycle`, `stager.timer` inactive
- Windows `StagerReconcile` 1 min, env MinIO máquina vacío

## Resolución aplicada

- Servicio Windows como `kor`. Known-errors actualizados. Gate documentado para el próximo E2E.

## Validación

- HTML 28332 bytes con `os/exec`+pipes como `kor`. Worker `KoR` con Temporal `:7233`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos nuevos; credenciales ya canónicas en skills Symphony

## Rollback

- `sc.exe config StagerRuntime obj= LocalSystem` y restart; no revertir el known-error.

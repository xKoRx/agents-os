---
type: known_error
schema_version: 1
scope: application
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
  - "[[stager-go-requires-current-pending-bridge]]"
aliases:
  - deploy_release.sh no corta a Go Stager
  - CURRENT f33-lifecycle vs 0.2.x
  - stager.timer inactive
confidence: verified
source_session: f562c20a-71b0-4d0c-9be5-a55abf905292
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
  - area/echo
  - tech/stager
  - project/echo-forge
---

# symphony-deploy-release-go-stager-cutover-gap

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- `./deploy_release.sh` publica `deploy/manifest.json` semver (`0.2.x`) a MinIO y copia `input/example` al watcher local, pero los workers productivos siguen en release `f33-lifecycle` de Go Stager.

## Causa

- Linux (Zeus/Hera/Kronos): el proceso vivo es `/opt/stager/releases/f33-lifecycle/bin/symphony` vía `stager-runtime`. `stager.timer` está **inactive**; no hay one-shot que reconcilie MinIO. `target.yaml` pide `entrypoint: bin/run-symphony`; `deploy_sqx.sh` publica `bin/symphony` + `bin/start-symphony-worker.sh`, no `run-symphony`.
- `/opt/symphony/CURRENT=0.2.40` es rastro Bash legacy; no es el binario en ejecución.
- Windows: `StagerReconcile` corre cada 1 min como SYSTEM, `CURRENT=f33-lifecycle`, y el entorno máquina no tiene `MINIO_*` / `STAGER_BUCKET`. El runtime sí corre el worker como `kor`.
- `wait_for_worker_rollout` default 35s no cubre timer Windows (1 min) ni drain `shutdown_timeout: infinite`.

## Impacto

- Un E2E disparado por `deploy_release.sh` corre contra binarios `f33-lifecycle`, no contra la versión recién compilada. Linux y Windows pueden divergir si uno reconcilia y el otro no.

## Detección

- Linux: `cat /opt/stager/state/CURRENT`; `systemctl is-active stager.timer`; `ps` del `bin/symphony` bajo `/opt/stager/releases/`.
- Windows: `Get-Content C:\ProgramData\Stager\state\CURRENT`; owner de `sqx-mt5-worker.exe`; env `MINIO_ENDPOINT`/`STAGER_BUCKET` de la tarea `StagerReconcile`.
- Comparar `.version` de `mc cat aranea/worker/sqx/manifest.json` vs CURRENT de Stager, no vs `/opt/symphony/CURRENT`.

## Mitigación

- No tratar `deploy_release.sh` como cutover de Go Stager hasta alinear entrypoint, habilitar reconciliación Linux, inyectar env MinIO en `StagerReconcile`, y esperar CURRENT=semver en los cuatro hosts antes de copiar `input/`.
- `deploy_release.sh` siempre hace bump de `strategy` (`example_flow_2` → `example_flow_3`).

## Evidencia

- 2026-08-14 Zeus/Hera/Kronos: timer inactive, runtime active, CURRENT `f33-lifecycle`, worker bajo `/opt/stager/releases/f33-lifecycle`.
- Windows: CURRENT `f33-lifecycle`, releases `f28-canary`/`f33-lifecycle`/`f33-rollback`, env MinIO máquina vacío, `StagerRuntime` StartName `.\kor`.

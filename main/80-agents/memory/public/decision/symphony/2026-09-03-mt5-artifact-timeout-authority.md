---
type: decision
schema_version: 1
scope: project
created: "2026-09-03"
updated: "2026-09-03"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-09-03-mt5-artifact-timeout-retry-loop]]"
  - "[[2026-09-03-deploy-release-only]]"
aliases:
  - MT5_ARTIFACT_TIMEOUT_AUTHORITY
  - mt5.timeout task authority
confidence: verified
source_session: ECHO-FORGE-MT5-TIMEOUT-RETRY-AND-RELEASE-ISOLATION-V1-TOP
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
  - tech/mt5
  - tech/temporal
---

# 2026-09-03-mt5-artifact-timeout-authority

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Contrato congelado FEAT-SQX-MT5-PIPELINE-ARTIFACTS: `mt5.timeout` gobierna cada backtest; StartToClose = task timeout + 2m; retry MaximumAttempts=3; functional `backtest_timeout`/`report_not_found` no activan retry de infra.
- Runtime 0.2.87 tenía dos autoridades: Temporal usaba task timeout; ArtifactRunner usaba ETCD `mt5/backtest_timeout=2h` bajo prefijo `sqx-mt5-worker`. Legacy `mt5_backtest` sigue en `mt5/backtest_timeout_ms` y no se tocó.

## Decisión

- Para `mt5_backtest_artifact` V1 la única autoridad física es el task `mt5.timeout`. ArtifactRunner parsea `params.Request.MT5.Timeout` y cancela el proceso ~ese timeout. Temporal conserva +2m para journals/evidence/cleanup.
- ETCD `mt5/backtest_timeout` no tiene autoridad sobre ArtifactRunner V1. Puede permanecer para legacy. No se elimina la key ni se cambia `mt5_backtest`.
- Retry de backtest: MaximumAttempts=3, Initial=5s, Backoff=2, MaxInterval=30s, NonRetryable `source_not_found`/`contract_error`. Compile conserva MaximumAttempts=0 vía `mt5CompileArtifactRetryPolicy()` para no mutar su contrato ni tests prohibidos.
- Functional timeout: Job Object drain + `ArtifactTaskResult{status:failed, error_code:backtest_timeout}` con `error==nil` ⇒ un physical attempt, sin retry Temporal.

## Rationale

- Dos relojes independientes convertían el StartToClose en cancel de infra y el retry ilimitado en un loop de 47m. Unificar en el timeout del task restaura el contrato congelado sin tocar el runner legacy.

## Consecuencias

- Fuente en `67db6f94c50a33a9a18359ac62c15d43a20a5694`. Physical 0.2.87 no cambia. Próximo release 0.2.88 debe salir `--release-only`. Compile permanece unlimited hasta autorización explícita.

## Alternativas descartadas

- Hacer que ArtifactRunner lea el mismo ETCD 2h: contradice el contrato task-timeout y no explica la cadencia 47m.
- Cambiar compile a MaximumAttempts=3 en esta sesión: rompe `mt5_compile_workflow_test.go`, archivo no permitido.

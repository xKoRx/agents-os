---
type: known_error
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
  - "[[2026-09-03-mt5-artifact-timeout-authority]]"
  - "[[2026-09-03-temporal-activity-started-deferred]]"
  - "[[2026-09-03-deploy-release-only]]"
  - "[[2026-09-03-orphan-mt5-after-cancel]]"
aliases:
  - MT5_ARTIFACT_TIMEOUT_RETRY_LOOP
  - dual timeout authority
  - MaximumAttempts 0 unlimited
confidence: verified
source_session: ECHO-FORGE-MT5-TIMEOUT-RETRY-AND-RELEASE-ISOLATION-V1-TOP
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
  - project/echo-forge
  - tech/mt5
  - tech/temporal
---

# 2026-09-03-mt5-artifact-timeout-retry-loop

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- `mt5_backtest_artifact` relanza terminal64 cada ~47m sin tope. Evidencia 0.2.87: 17:05:20Z, 17:52:26Z, 18:39:54Z, 19:28:00Z, 20:15:10Z.

## Causa

- Task `mt5.timeout=45m` → Temporal StartToClose 47m. ArtifactRunner V1 leía ETCD `mt5/backtest_timeout=2h` y armaba `context.WithTimeout` con esa key. Temporal cancela a 47m antes de que venza 2h; el runner clasificaba `context.Canceled` como error de infraestructura. `mt5ArtifactRetryPolicy().MaximumAttempts=0` = retry infinito. Cadencia observada = StartToClose, no el 2h de ETCD.

## Impacto

- Slot único del worker MT5 ocupado. Release wrapper dispara FlowRun de producto. Smoke/CERT imposibles. Runtime 0.2.87 sigue vivo con este contrato; HEAD `67db6f9` lo corrige en fuente.

## Detección

- DescribeWorkflowExecution `pendingActivities`: activityId `mt5_backtest_artifact`, attempt creciente, lastFailure infra. No usar ausencia de `ActivityTaskStarted` como falta de dispatch. Prefijo ETCD `sqx-mt5-worker` (no `sqx-worker`).

## Mitigación

- Contener el FlowRun accidental con un CancelWorkflow al Generic parent exacto. Fuente: ArtifactRunner usa `params.Request.MT5.Timeout`; retry backtest MaximumAttempts=3; functional `backtest_timeout` retorna result+err=nil. Physical 0.2.87 no incorpora el fix. NO cerrar [[2026-09-03-orphan-mt5-after-cancel]] hasta smoke físico disposable PASS.

## Evidencia

- WorkflowID `sqx-main-v1-11ab7b0e-cbbc-42f7-b029-ab749d53a1b2` RunID `01a06829-77ad-7e88-80b5-5e19513d7ba5` FlowRunRef `0f4d89eb-293d-48ce-8356-2ab242fc7edf`. Commits `67db6f94c50a33a9a18359ac62c15d43a20a5694` y `7047a9c112502dcb68387745149eed95405b0aae`.

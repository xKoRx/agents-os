---
type: change_log
schema_version: 1
scope: session
created: "2026-09-03"
updated: "2026-09-03"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[Symphony]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-09-03-mt5-artifact-timeout-retry-loop]]"
  - "[[2026-09-03-temporal-activity-started-deferred]]"
  - "[[2026-09-03-mt5-artifact-timeout-authority]]"
  - "[[2026-09-03-deploy-release-only]]"
  - "[[2026-09-03-cursor-grok-4-6-echo-forge-mt5-timeout-retry-release-isolation]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-MT5-TIMEOUT-RETRY-AND-RELEASE-ISOLATION-V1-TOP
source_feedbacks:
  - "[[2026-09-03-echo-forge-mt5-timeout-retry-release-isolation-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-03-echo-forge-mt5-timeout-retry-release-isolation

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]] checkpoint append-only
  - [[agents-os-operating-continuity]] delta operativo
  - [[2026-09-03-mt5-artifact-timeout-retry-loop]]
  - [[2026-09-03-temporal-activity-started-deferred]]
  - [[2026-09-03-mt5-artifact-timeout-authority]]
  - [[2026-09-03-deploy-release-only]]
  - symphony `67db6f94c50a33a9a18359ac62c15d43a20a5694` y `7047a9c112502dcb68387745149eed95405b0aae` (fuera del vault)

## Motivo

- Contención del FlowRun accidental 0.2.87 y corrección de autoridad de timeout/retry + aislamiento release/product run. C3 y ORPHAN_MT5 no se cierran.

## Fuentes usadas

- DescribeWorkflowExecution pendingActivities; PostgreSQL FlowRun; Windows process tree; ETCD prefijo `sqx-mt5-worker`; fuente `sqx/workflows/mt5_artifact_workflow.go` y `sqx/adapters/mt5/artifact_runner.go`.

## Resolución aplicada

- Un CancelWorkflow al Generic parent exacto. ArtifactRunner V1 usa task `mt5.timeout`. Retry backtest max 3. `--release-only` en el wrapper. Compile retry intacto (MaximumAttempts=0).

## Validación

- Tests focales Go/race/vet PASS; `bash deploy_release_test.sh` PASS; HEAD==origin/master==`7047a9c`; CURRENT físico 0.2.87; terminal64=0 metatester64=0.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad de máquina, secretos ni memoria interna

## Rollback

- Revertir `7047a9c` luego `67db6f9` en symphony. Notas L3 permanecen como evidencia histórica. No rollback del CancelWorkflow.

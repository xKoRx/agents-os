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
  - "[[2026-09-01-release-version-authority]]"
aliases:
  - deploy_release --release-only
  - RELEASE_ONLY
confidence: verified
source_session: ECHO-FORGE-MT5-TIMEOUT-RETRY-AND-RELEASE-ISOLATION-V1-TOP
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
  - tech/release
---

# 2026-09-03-deploy-release-only

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- `deploy_release.sh` publicaba release, bump de strategy, mutaba `input/example/config.json` y copiaba `input/example` → `input/`. Watcher disparaba un FlowRun. Release 0.2.87 ocupó el slot MT5 con `example_flow_25`.

## Decisión

- Flag explícito `./deploy_release.sh --release-only <version>` (antes o después de posicionales). Hace authority, build/package, manifest, publish, wait manifest, wait rollout. No bump, no muta `input/example/config.json`, no copia a `input/`, no asegura watcher sólo para input delivery, no dispara Workflow.
- Default sin flag: comportamiento histórico.

## Rationale

- Separar RELEASE de PRODUCT RUN es requisito para certificar cancelación MT5 sobre un binario nuevo sin contaminar el slot.

## Consecuencias

- Próximo 0.2.88 debe invocarse `--release-only`. Commit `7047a9c112502dcb68387745149eed95405b0aae`. Tests en `deploy_release_test.sh`.

## Alternativas descartadas

- Cambiar el default a release-only: rompe backward compatibility del wrapper.

---
type: change_log
schema_version: 1
scope: session
created: "2026-09-02"
updated: "2026-09-02"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities: []
related:
  - "[[2026-09-02-release-wrapper-inflight-manifest-preflight-race]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-RELEASE-WRAPPER-INFLIGHT-PREFLIGHT-FIX-NORMAL
source_feedbacks:
  - "[[2026-09-02-echo-forge-release-wrapper-inflight-preflight-fix-normal-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-02-echo-forge-release-wrapper-inflight-preflight-fix-normal

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated / deleted / conflict-resolution
- **Archivo(s):**
  - `xKoRx/symphony/deployer/cmd/release-authority/main.go`
  - `xKoRx/symphony/deployer/cmd/release-authority/main_test.go`
  - `xKoRx/symphony/deploy_release.sh`
  - `xKoRx/symphony/deploy_release_test.sh`

## Motivo

- Resolver `RELEASE_WRAPPER_IN_FLIGHT_MANIFEST_PREFLIGHT_RACE` sin publicar una nueva release ni aceptar `DIVERGENT`.

## Fuentes usadas

- Baseline autorizado `48997d773e91dec9b8fe57fbd1650e8d8beb8b57`, known-error del race y contrato operativo C3.

## Resolución aplicada

- `verifyTarget` valida todos los remotos contra el manifest local y clasifica subsets exactos como `PARTIAL_EXACT_MATCH`; el wrapper permite sólo las transiciones `AVAILABLE→AVAILABLE/PARTIAL_EXACT_MATCH/EXACT_MATCH` y `EXACT_MATCH→EXACT_MATCH`.
- Se preservan fail-closed, write-once, monotonicidad del manifest, manifest como commit point y resume explícito sólo `EXACT_MATCH`.

## Validación

- `go test`, `go test -race`, `go vet`, Bash syntax, wrapper S1–S17, `go test ./internal/di`, `git diff --check` y autoridad real read-only pasaron.
- `HEAD == origin/master == 2b4dff61bc0597204e6eeb1c920882cd5b77cd59`; sólo cuatro Allowed Files fueron commitados.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir el commit `2b4dff61bc0597204e6eeb1c920882cd5b77cd59` si el owner autoriza rollback; no tocar MinIO ni artifacts físicos.

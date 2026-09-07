---
type: change_log
schema_version: 1
scope: session
created: "2026-09-01"
updated: "2026-09-01"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities: []
related: []
aliases: []
confidence: verified
source_session: unavailable
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-01-release-authority-fix

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `repo=xKoRx/symphony:deploy_release.sh`
  - `repo=xKoRx/symphony:deployer/cmd/release-authority/main.go`
  - `repo=xKoRx/symphony:deployer/core/planner/simple.go`

## Motivo

- Se implementó la corrección de autoridad de versión para cerrar RC-A/B/C/F/H/I sin tocar Campaign, SQX workflows, stager, migraciones ni `deploy/manifest.json`.

## Fuentes usadas

- [[2026-09-01-release-authority-stale-manifest-rollback]], baseline/HEAD/origin del repositorio y matriz de tests de la sesión.

## Resolución aplicada

- `release-authority` usa `di.InitSelective("deployer-watcher", WithEnvironment(ENV), WithEtcd, WithMinIO)`, lee manifest/prefixes desde el mismo MinIO productivo, falla cerrado ante estado remoto desconocido, exige ACK exacto para gaps, y verifica targets por SHA256/size. El planner rechaza HeadObject/remote-read failures, colisiones divergentes y downgrade de manifest; watcher publica manifest al final.

## Validación

- Commit `ee61d3d0b3b53416e80b231522342482322e556e` pushed to `origin/master`; targeted/race/vet/bash gates PASS. Broad `go test ./... -count=1` conserva únicamente el failure baseline `deployer/adapters/manifest-json/stager_publisher_test.go:75`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin credenciales, secretos, dumps ni paths absolutos de máquina

## Rollback

- Revertir el commit `ee61d3d0b3b53416e80b231522342482322e556e` únicamente con autorización explícita; no restaurar un manifest git stale durante un deployer activo.

---
type: change_log
schema_version: 1
scope: session
created: "2026-09-01"
updated: "2026-09-01"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities: []
related: []
aliases: []
confidence: verified
source_session: ECHO-FORGE-RELEASE-AUTHORITY-STDOUT-ISOLATION-FIX-NORMAL
source_feedbacks:
  - "[[2026-09-01-echo-forge-release-authority-stdout-isolation-fix-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-01-echo-forge-release-authority-stdout-isolation-fix

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated / conflict-resolution
- **Archivo(s):**
  - `xKoRx/sdk/pkg/shared/etcd/cache.go`
  - `xKoRx/symphony/deployer/cmd/release-authority/main.go`
  - `xKoRx/symphony/deployer/cmd/release-authority/main_test.go`
  - `xKoRx/symphony/go.mod`, `sqx/go.mod`, `deployer/go.mod`
  - checkpoint de proyecto y known-error de Echo Forge

## Motivo

- Resolver la contaminación de stdout que impedía a `deploy_release.sh` parsear la autoridad de release y cerrar el blocker source-level C3-B.

## Fuentes usadas

- Bootstrap, checkpoint y known-error canónicos; source gates exactos; tests targeted/race/vet; harness S1-S10; acceptance real production read-only separado por stdout/stderr.

## Resolución aplicada

- SDK `c85594440f6755443ceb97ec4e333cd0ddb5b0ed` elimina el debug accidental; Symphony `02fabffe958854ab30e017301a8c30aaada527ac` reserva `machineOut`, redirige `os.Stdout` a `os.Stderr` hasta después de DI close y actualiza los tres pins al pseudo-version canónico `v0.0.0-20260902001205-c85594440f67`.

## Validación

- Ambos commits fueron pushed a `master`; M1-M6 y todos los gates autorizados pasan; real no-ACK retorna exit 1 con JSON limpio y ACK/target retornan exit 0; manifest `0.2.78` y estado físico no cambiaron.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- No se requiere rollback; la recuperación física futura debe usar las nuevas source authorities y no publicar en esta sesión.

---
type: change_log
schema_version: 1
scope: session
created: "2026-08-13"
updated: "2026-08-13"
area: "[[Echo Forge]]"
project: "[[Stager - Cross-Platform Deployment Lifecycle]]"
application: "[[Stager]]"
entities:
  - "[[Stager - Cross-Platform Deployment Lifecycle]]"
related:
  - "[[2026-08-12-stager-f32-server-updated-preflight-pending]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# F3.R — Runtime Stager cooperativo local PASS

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `stager/internal/runtime/{runtime.go,runtime_test.go,systemd_test.go}`
  - `stager/cmd/stager-runtime/service_windows.go`
  - `stager/deploy/{linux,windows}/**`, `stager/docs/RUNTIME.md`
  - `stager/specs/STAGER-DEPLOYMENT-LIFECYCLE/**`
  - `10-projects/Echo Forge/agentes/Stager - Cross-Platform Deployment Lifecycle.md`

## Motivo

- El owner exige que una parada ordenada no corte trabajo aceptado que puede durar días.

## Fuentes usadas

- Conversación owner del 2026-08-13.
- Implementación local de Stager y contrato F3.R aprobado dentro de su SDD.

## Resolución aplicada

- Se agregó el valor exacto `shutdown_timeout: infinite`; el runtime espera cooperativamente sin kill.
- Linux evita el límite de systemd y sus señales directas al hijo; Windows reporta checkpoints SCM durante la espera.
- El deploy remoto se retiene hasta recibir sudo interactivo, sin extraer ni automatizar credenciales.

## Validación

- PASS: `go test ./...`, `go vet ./...`, `git diff --check`, builds Linux/Windows.
- Pack Linux creado con SHA-256 `89a9ce427c6e0e5919df0eb5d35616773bdd9f15be4723e6edeff4c611af1d43`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos.

## Rollback

- Revertir a binario/unidad/configuración previos restaura el timeout anterior; no toca releases, `CURRENT`, `RUNNING`, `PENDING` ni receipts.

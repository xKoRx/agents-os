---
type: change_log
schema_version: 1
scope: session
created: "2026-08-10"
updated: "2026-08-10"
area: "[[Echo]]"
project: "[[Stager - Cross-Platform Deployment Lifecycle]]"
application: "[[stager-app]]"
entities:
  - "[[Stager]]"
related:
  - "[[Echo Forge]]"
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

# Stager F1.8 — G1 rejected

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Stager - Cross-Platform Deployment Lifecycle.md`
  - `10-projects/Echo Forge/Echo Forge.md`
  - repo `stager` + `specs/STAGER-DEPLOYMENT-LIFECYCLE/{PLAN.md,TASKS.md,VERIFICATION.md}`

## Motivo

- Completar exclusivamente F1.8 mediante revisión adversarial de crash consistency y decidir G1 sin aceptar waivers implícitos ni avanzar F2.

## Fuentes usadas

- [[Stager - Cross-Platform Deployment Lifecycle]], SDD `STAGER-DEPLOYMENT-LIFECYCLE`, diff F1 y fuentes `internal/activation`, `internal/staging/runner.go` y `cmd/stager/main.go` del repo `stager`.

## Resolución aplicada

- F1.8 quedó terminada con G1 `REJECTED/BLOCKED`: seis incumplimientos contractuales se reprodujeron mediante overlay efímero y se registraron dos gaps adicionales de fault matrix, `RunOnce`, Windows y wiring. El proyecto avanzó `progress: 44→47`, la tarea puente conservó WIP y F2 quedó no autorizada. No se modificó implementación ni runtime.

## Validación

- PASS: `go test -count=1 -race ./...`, `go vet ./...`, builds `linux-amd64`/`windows-amd64` y `git diff --check`. FAIL esperado: seis assertions adversariales ejecutadas con overlay fuera del repo. Allowed Files F1.8 limitados a `PLAN.md`, `TASKS.md` y `VERIFICATION.md`; el diff de revisión respeta el límite.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin credenciales, valores de entorno, paths absolutos de máquina ni evidencia de hosts

## Rollback

- Revertir sólo las actualizaciones documentales de F1.8 y restablecer `progress: 44` si la revisión se invalida formalmente; no tocar la implementación F1.3-F1.7 ni presentar G1 como aceptado sin nueva evidencia independiente.

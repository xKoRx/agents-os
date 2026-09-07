---
type: change_log
schema_version: 1
scope: session
created: "2026-08-31"
updated: "2026-08-31"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application:
entities: []
related:
  - "[[2026-08-31-echo-forge-finalist-promotion-result-surface]]"
aliases: []
confidence: verified
source_session: "ECHO-FORGE-FINALIST-PROMOTION-RESULT-SURFACE-INDEPENDENT-ASSEMBLY-FIX-NORMAL"
source_feedbacks:
  - "[[2026-08-31-symphony-result-surface-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-31-echo-forge-finalist-promotion-result-surface-config-isolation

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):** `sqx/core/forge/result.go`, `sqx/core/forge/result_test.go`

## Motivo

- La interpretación conjunta de `rankings` y `promotion` contaminaba ambas Result Surfaces cuando fallaba una sola projection.

## Fuentes usadas

- Baseline autorizado `a9360a8e572d27b5adcb92c94e5cde0a3851df48`, contrato Finalist Promotion Result Surface V1 y checkpoint previo del proyecto.

## Resolución aplicada

- Se valida el root JSON/objeto una vez y se parsean projections independientes con `json.RawMessage`; cada sección conserva su status y la autoridad hermana se resuelve antes del error contractual.

## Validación

- PASS: `go test ./sqx/core/forge`, `go test ./sqx/core/domain ./sqx/core/capabilities`, `go test ./sqx/core/...`, variantes `-race -cover`, `go vet ./sqx/core/forge/...` y `git diff --check`. Commit `9c90a2f75108c729eaee6a0906eb9b057f3af970`; `HEAD == origin/master`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir `9c90a2f75108c729eaee6a0906eb9b057f3af970`; no requiere migrations, workflow, Promotion Core, Campaign ni cambios de schema.

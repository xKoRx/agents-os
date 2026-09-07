---
type: change_log
schema_version: 1
scope: session
created: "2026-08-31"
updated: "2026-08-31"
area:
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application:
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-08-31-codex-unknown-finalist-promotion-v1-supersedes-guard]]"
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

# 2026-08-31-finalist-promotion-v1-supersedes-guard

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `sqx/core/domain/decision.go`
  - `sqx/core/domain/decision_test.go`
  - `sqx/adapters/registry-postgres/migrations/010_finalist_promotion_no_supersedes.up.sql`
  - `sqx/adapters/registry-postgres/migrations/010_finalist_promotion_no_supersedes_test.go`
  - `sqx/adapters/registry-postgres/migrations/runner.go`

## Motivo

- Promotion V1 congeló `Supersedes = nil`, pero la validación de dominio permitía un `FINALIST_PROMOTION` con supersession fuera del digest y del contrato immutable.

## Fuentes usadas

- [[2026-08-30-finalist-promotion-v1-core]], contrato de Promotion V1 y migration 009 preservados sin modificación.

## Resolución aplicada

- `validateFinalistPromotionV1()` rechaza cualquier `Supersedes != nil`; FinalistPromotionContentDigestV1 permanece sin Supersedes; migration 010 agrega un CHECK solo para `FINALIST_PROMOTION`; optimizer mantiene su supersession histórico.

## Validación

- T1/T2/T3/T4 PASS; domain, migrations, DecisionStore targeted y `go vet` afectados PASS; no physical E2E ejecutado por alcance.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir el commit `43eb5bed85d5404b79181425971eba9c534c25a6` si fuera necesario; migration 010 no modifica 009 ni elimina la columna/FK `supersedes`.

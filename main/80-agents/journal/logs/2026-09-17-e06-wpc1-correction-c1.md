---
type: change_log
schema_version: 1
scope: session
created: "2026-09-17"
updated: "2026-09-17"
area: "[[Echo]]"
project: "[[Echo — E-06 Reference Enrollment and Binding]]"
application:
entities:
  - "[[Echo — E-06 Reference Enrollment and Binding]]"
related:
  - "[[Echo — Live Platform V1]]"
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
  - area/echo
---

# 2026-09-17-e06-wpc1-correction-c1

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo — E-06 Reference Enrollment and Binding.md` — nuevo bullet de estado `E06_WPC1_C1_READY_FOR_MANAGER_REVIEW`, tabla de entrega @ `32332c04`, entrada de bitácora de la corrección C1 WP-C1.

## Motivo

- Mandato correctivo del Manager sobre la entrega WP-C1 (`1bebb67d`): `ReferenceReadback.Validate()` no exigía el `broker_connected` explícito de SPEC §7.2 ni los conteos del inventario declarado con `inventory_completeness=KNOWN`.

## Fuentes usadas

- SPEC v1.2.2 §7.2 (`specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/SPEC.md` en `xKoRx/echo`).
- `v3/sdk/domain/reference_readback.go` y suites de tests en `1bebb67d` y `32332c04`.

## Resolución aplicada

- Corrección implementada en repo `xKoRx/echo` commit único `32332c04` (push FF `1bebb67d..32332c04` sobre `feature/e06-reference-enrollment-binding`): C1-A `broker_connected` obligatorio no-nil con inferencia prohibida; C1-B KNOWN exige `position_count`/`pending_count` presentes y no negativos (nil nunca se convierte en cero); C1-C tri-state `*_trade_allowed` intacto. Golden del digest recalculado por el campo explícito con verificación independiente byte-exacto (Go↔Python + sha256sum). Evidencia completa en `specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/VERIFICATION.md` §WP-C1 CORRECTION C1 y TASKS.md.

## Validación

- PG REAL PASS: PostgreSQL 17.11 descartable, `run.sh` ×2, `sdk/domain` plain/race PASS, T09 5/5 `-race`; failing sets idénticos por nombre al baseline `1bebb67d` (postgres 53=53, gateway 30=30); vet y builds OK; diff limitado a allowed files; veredicto `E06_WPC1_C1_READY_FOR_MANAGER_REVIEW` pendiente de Manager review.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- `git revert 32332c04` en `xKoRx/echo` (commit único, sin dependencias posteriores); la entidad del vault se restaura del historial de Obsidian/Git.

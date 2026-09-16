---
type: change_log
schema_version: 1
scope: session
created: "2026-09-16"
updated: "2026-09-16"
area: "[[Echo]]"
project: "[[Echo Forge — F-05-I Cohesive release and read surfaces]]"
application:
entities:
  - "[[Echo Forge]]"
related: []
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

# 2026-09-16-f05i-t2-keyset-pagination-fix

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo Forge — F-05-I Cohesive release and read surfaces.md` — tarea F05I-T2 (línea del tablero), `## 📊 Estado actual` (nuevo bloque "Corrección T2") y `## 📆 Bitácora` (nueva entrada).

## Motivo

- Defecto confirmado por manager: la paginación de campañas de F05I-T2 perdía silenciosamente registros empatados en `created_at`. El estado del proyecto debía reflejar la corrección publicada sin cambiar el estado Review de T2 ni los de T3/T4.

## Fuentes usadas

- `xKoRx/symphony@3da8b470239a15f62d87f16559feada409e2d611` (diff de 2 archivos: `sqx/adapters/registry-postgres/forge_campaign_list.go`, `forge_campaign_list_test.go`).
- Ejecución real de tests: `go test ./sqx/adapters/registry-postgres/ -run 'TestListForgeCampaigns'` PASS; `-race` PASS; `go vet` PASS; gofmt/diff-check OK; prueba cruzada del test de regresión (FALLA con predicado anterior, PASS con corrección).
- Verificación remota: `origin/codex/f05-release-prep` = `3da8b47`, ancestro de `d77342d5a49cb393f92e1a85f998c5614a1cd6bb`.

## Resolución aplicada

- T2 registra: defecto (pérdida silenciosa en empates), causa técnica (predicado tuple `(created_at, id) < ($1,$2)` compara `id` descendente contra orden `created_at DESC, id ASC`), SHA correctivo `3da8b47`, test de regresión `TestListForgeCampaignsPersistenceTieTimestampsKeysetTraversal`, resultados reales y manager review pending. T2 permanece `[r]` Review; T3/T4 sin cambios; F-05-I/F-05-C no cerradas.

## Validación

- Hechos verificados contra el repo real (SHA, ascendencia, resultados de tests) al momento de la edición. Validación de retrieval pendiente al cierre (query enfocada Graphify).

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir los tres bloques editados en la nota del proyecto; el rollback del código vive en `xKoRx/symphony` (revert de `3da8b47`), no en el vault.

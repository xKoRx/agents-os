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

# 2026-09-16-f05i-t1-parser-trailing-data-fix

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo Forge — F-05-I Cohesive release and read surfaces.md` — tarea F05I-T1 (línea del tablero), `## 🧱 Entrega de desarrollo` (celda T1), `## 📊 Estado actual` (nuevo bloque "Corrección T1") y `## 📆 Bitácora` (nueva entrada).
  - `80-agents/journal/agent-runs/2026-09-16-zcode-glm-5.3-flash-f05i-t1-parser-trailing-data-fix.md` — creado (agent_run de la ejecución correctiva).

## Motivo

- Defecto confirmado por manager en `sqx/core/releasematrix.Parse` (F05I-T1): la verificación de trailing data vía `dec.More()` no garantiza el fin del documento JSON — More hace peek del siguiente byte y devuelve false ante `}` o `]` pendientes, por lo que una matriz válida seguida de cualquiera de esos caracteres era aceptada. El estado del proyecto debía registrar defecto, causa, SHA correctivo, tests reales y manager review pending, manteniendo T1 en Review.

## Fuentes usadas

- `xKoRx/symphony@2c5d34f5acde958e93a8e5382bca35be5c96b667` (diff de 2 archivos: `sqx/core/releasematrix/releasematrix.go`, `releasematrix_test.go`; 52 inserciones, 3 deletions).
- Ejecución real de tests: demostración previa del defecto (`TestParseTrailingDataAfterValidMatrix` FALLA contra `dec.More()` con `}` y `]`); con la corrección `go test ./sqx/core/releasematrix/...` PASS, `-race` PASS, `go vet` PASS, `go build` PASS, gofmt/diff-check OK; `release-matrix.json` sin cambios.
- Verificación remota: `origin/codex/f05-release-prep` = `2c5d34f` (fast-forward `5295f1c..2c5d34f`), `5295f1c` ancestro, baseline `b57bfb2` ancestro.

## Resolución aplicada

- T1 registra: defecto (trailing data `}`/`]` aceptada), causa (`dec.More()` no garantiza fin de documento), SHA correctivo `2c5d34f`, test de regresión `TestParseTrailingDataAfterValidMatrix` (5 casos obligatorios desde `Embedded()`), resultados reales y manager review pending. T1 permanece `[r]` Review; T2–T4 sin cambios; T5/T6/T7 pendientes; F-05-I/F-05-C no cerradas; ningún gate físico marcado.

## Validación

- Hechos verificados contra el repo real (SHAs, ascendencia, diff limitado a 2 archivos, resultados de tests, artefacto intacto, dirty ajeno preservado) al momento de la edición. Retrieval Graphify NOT_RUN: el CLI no está disponible en esta máquina; journal está excluido del índice y la nota de proyecto se resolvió por búsqueda enfocada de título canónico.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir los cuatro bloques editados en la nota del proyecto y eliminar el agent_run creado; el rollback del código vive en `xKoRx/symphony` (revert de `2c5d34f`), no en el vault.

---
type: change_log
schema_version: 1
scope: session
created: "2026-09-08"
updated: "2026-09-08"
area: "[[Echo]]"
project: "[[Echo — Live Platform V1]]"
application: "[[echo-core]]"
entities: ["[[Echo — E-01 Canonical SDK Foundation S0]]", "[[Echo — Live Platform V1]]"]
related: ["[[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]", "[[Echo SDK — Canonical Contract Final Freeze Review — Fable 5.1]]"]
aliases: []
confidence: verified
source_session:
source_feedbacks: ["[[2026-09-08-echo-e01-contracts-s0-session-feedback]]"]
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Echo E-01 contracts S0 — cierre por delta (implementación)

## Cambio

- **Tipo:** updated (entidad Sistema 2) + created (journal).
- Subproyecto [[Echo — E-01 Canonical SDK Foundation S0]]: progreso 0 → 100; WPs WP-A…WP-F `[x]`; bitácora con commit de implementación y gates.

## Evidencia de código

- Repo `xKoRx/echo`, branch `master`: commit `f1070bec` `feat(sdk): implement canonical contract S0` (152 archivos, sólo `v3/sdk/contracts/**`) sobre baseline SDD `182614297138c8c6fa0f02cd6aa8a5decf151479` (parent `04c16bd2bd7b69725560873950a5d6b067fd3a4f`).
- Gates: `GOWORK=off go test ./...` PASS; `-race -cover` PASS; `go vet` PASS; gofmt limpio; coverage contracts 95.1% / wire 97.0% / fakeconsumer 95.5%; stdlib-only y `go 1.24` verificados por test (`TestModule_GoVersionAndStdlibOnly`, `TestImports_StdlibOnly`).
- Corpus `testdata/v1/manifest.json` G01–G36 + `write-once-conflict/`; goldens verificados contra receta reimplementada en Python; schema `schema/echo-contracts-v1.schema.json` regenera sin drift (`SCHEMA_REGEN=1`).
- Sin push, sin tag, sin cambios fuera de `v3/sdk/contracts/**`.

## Corrección operativa (publicación)

- Push `HEAD:master` sin force tras gate completo (`origin/master == 04c16bd2`, cadena exacta `18261429`+`f1070bec`, ancestro OK, árbol limpio). Remoto verificado: `origin/master == f1070bec27db3ca415fe24f3c3576139674b7e09`.

## Corrección acotada UTF-8

- Commit `c2472ca953b54954431b476df9b65ce1b5aa9631` (parent `f1070bec`), publicado fast-forward: `Canonicalize` rechaza UTF-8 inválido en raw JSON y en Go values (walk reflexivo pre-encode, sin reemplazo U+FFFD); `Validate` lo marca `INVALID_WIRE`. Tests nuevos: string value, object key, no-ASCII válido preservado. Gates PASS; wire 96.9%.

## Corrección 2: prevalidación UTF-8 cycle-safe

- Commit `6cf39edfbd1f16eca82753f42527b170b50b66f0` (parent `c2472ca9`), publicado fast-forward: walk UTF-8 con ciclo-detección por camino activo y field set idéntico a encoding/json; tests de ciclos ptr/map/slice, referencias compartidas y campos no serializados.

## Corrección 3: boundary de serialización (Marshaler/TextMarshaler)

- Commit `aafa2f62` (parent `6cf39edfbd1f16eca82753f42527b170b50b66f0`), publicado fast-forward: el pre-walk UTF-8 de `Canonicalize` ahora decide por valor si encoding/json lo reemplaza con salida de `json.Marshaler`/`encoding.TextMarshaler` (value receiver) o de sus variantes pointer-receiver exactamente donde el valor es addressable (`CanAddr()`, espejo de `condAddrEncoder`); method sets promovidos de embebidos reemplazan el valor completo; keys de map con TextMarshaler saltan internals; campos exportados promovidos de structs embebidos no exportados se observan; elementos de array se prevalidan. `[]byte` (base64), `json.RawMessage` (verbatim + validación del pipeline) y ciclos/referencias compartidas sin cambios de contrato.
- Evidencia stdlib: probes físicos contra go1.25.5 (`GOROOT/src/encoding/json/encode.go`): struct con `MarshalJSON` en `*T` desciende a campos cuando no es addressable (top-level por valor, valores de map, interfaces); `typeFields` promociona embebidos no exportados; `appendCompact` valida sintaxis pero no UTF-8; `appendString` escapa bytes inválidos a `\ufffd`.
- Tests: 13 nominales nuevos en `canonicalize_test.go` con `MarshalJSON`/`MarshalText` reales (value/pointer receiver, nil pointer, salida JSON inválida, salida UTF-8 inválida, TextMarshaler con map keys y `time.Time`, embebidos, arrays, `[]byte`, `RawMessage`); se eliminó el bloque "Marshaler" tautológico del test anterior. Gates PASS; coverage contracts 95.1% / wire 97.0% / fakeconsumer 95.5%; sólo `v3/sdk/contracts/wire/{canonicalize,canonicalize_test}.go` modificados.
- Limitación registrada: resolución de sombras/ambigüedad de `typeFields` (BFS por profundidad) no espejada; sobre-recorrido patológico falla del lado seguro.

## No tocado

- Resources frozen, SPEC/PLAN/TASKS, Symphony, Lab, `v3/sdk/go.mod`, `go.work`. Verifier (VERIFICATION.md) y pin/corpus publicable quedan para manager/verificador.

## Journal

- Agent runs: [[2026-09-08-zcode-glm-5.3-flash-echo-e01-contracts-s0]], [[2026-09-08-zcode-glm-5.3-flash-echo-e01-s0-serialization-boundary]]
- Feedback: [[2026-09-08-echo-e01-contracts-s0-session-feedback]], [[2026-09-08-echo-e01-s0-serialization-boundary-feedback]]
- L0/L1: no creados (sin transcript; cierre por delta solicitado).
- Graphify: sin reindex (sólo notas journal no indexables + una nota de proyecto ya indexada; refresh pendiente al cierre de fase si procede).

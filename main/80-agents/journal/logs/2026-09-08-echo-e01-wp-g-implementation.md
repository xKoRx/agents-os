---
type: change_log
schema_version: 1
scope: session
created: "2026-09-08"
updated: "2026-09-08"
area: "[[Echo]]"
project: "[[Echo — E-01 Canonical SDK Foundation S0]]"
application: "[[Echo — Live Platform V1]]"
entities:
  - "[[Echo — E-01 Canonical SDK Foundation S0]]"
related:
  - "[[Echo SDK — Canonical Contract Final Freeze Review — Fable 5.1]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-09-08-echo-e01-wp-g-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-08-echo-e01-wp-g-implementation

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):** `xKoRx/echo/v3/sdk/contracts/wire/canonicalize.go`, `xKoRx/echo/v3/sdk/contracts/wire/canonicalize_test.go`, nota E-01, tarea puente del padre.

## Motivo

- Implementar la decisión TOP opción B para que `C()` tenga autoridad canónica sobre bytes JSON y no replique internals privados de `encoding/json`.

## Fuentes usadas

- SPEC/TASKS del contrato, source/tests actuales de `wire`, decisión TOP WP-G y gates físicos del repo.

## Resolución aplicada

- Se eliminó el pre-walk reflectivo y la selección duplicada de fields/map keys/tags; raw `[]byte`/`json.RawMessage` conserva byte-gate estricto y otros valores pasan primero por `encoding/json` con HTML escaping deshabilitado. WP-G quedó Done y la tarea puente pasó a Review.

## Validación

- Commit `f403e6d76cf1c2777458cbfcd82ded3c26b7a01d` sobre `2be12e23ca05dcbb184a6589e13f68bbd917e417`; push fast-forward verificado; test, race/cover y vet PASS; contracts 95.1%, wire 95.6%; gofmt/source gate/corpus checks PASS; árbol remoto limpio.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir el commit `f403e6d7` si el manager solicita rollback; no se usó force-push ni se modificaron goldens.

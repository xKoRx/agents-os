---
type: change_log
schema_version: 1
scope: session
created: "2026-09-08"
updated: "2026-09-08"
area: "[[Echo]]"
project: "[[Echo — E-01 Canonical SDK Foundation S0]]"
application:
entities: ["[[Echo — E-01 Canonical SDK Foundation S0]]"]
related: ["[[Echo SDK — Canonical Contract Final Freeze Review — Fable 5.1]]", "[[Echo — Live Platform V1]]"]
aliases: []
confidence: verified
source_session:
source_feedbacks: ["[[2026-09-08-echo-e01-canonicalization-boundary-session-feedback]]"]
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Echo E-01 — canonicalization boundary resolution (TOP decision)

## Cambio

- **Tipo:** updated (entidad Sistema 2) + created (journal).
- Subproyecto [[Echo — E-01 Canonical SDK Foundation S0]]: sección Estado actual (corrección de frontera decidida, `IMPLEMENTATION_CORRECTION`), work packages (+WP-G pendiente T26–T29), tareas (+WP-G `[ ]`), bitácora (entrada TOP con decisión, keep/remove de `2be12e23`, tests y gates), decisiones (frontera canónica sobre bytes JSON, sin mirror de internals).
- Estado del subproyecto se mantiene `implementation complete / verification pending`; sin marcar E-01 complete; sin commit en repo (SDD sin modificación: TASKS T02 sin contradicción, corpus intacto).

## Evidencia

- Análisis TOP one-shot sobre HEAD `2be12e23` (árbol limpio): mirror ~350 líneas contenido en `v3/sdk/contracts/wire/canonicalize.go`; probes físicos go1.25.5 validan que ciclos, Marshaler inválido y UTF-8 inválido de marshalers quedan cubiertos por error stdlib + byte-gate existente; FR-4a frozen define `C()` sobre payloads. Detalle en [[2026-09-08-zcode-glm-5.3-flash-echo-e01-canonicalization-boundary-decision]].
- Pendiente: manager acepta decisión → NORMAL nuevo implementa WP-G (T26–T29) en `v3/sdk/contracts/wire/canonicalize{,_test}.go`.

## Graphify

- Recomendado: reindex targeted de la nota del subproyecto (`10-projects/Echo/agentes/`) vía `agents-os-graphify-maintenance` al cierre del día.

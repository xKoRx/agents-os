---
type: feedback
schema_version: 1
scope: session
created: "2026-08-30"
updated: "2026-08-30"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[2026-08-30-durable-optimizer-output-cardinality-correction]]"
  - "[[2026-08-30-durable-optimizer-wf-matrix-cardinality-rca]]"
  - "[[2026-08-30-durable-project-stages-recovery-fault-certification]]"
aliases: []
confidence: verified
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/feedback
  - scope/session
---

# 2026-08-30-optimizer-cardinality-correction-session-feedback

## Gap

- El defecto del golden 0.2.81 sobrevivió a una suite verde porque el fake `prePutStorage` de Slice 2 colapsa payloads = published keys: ya aplicaba implícitamente la clasificación de publicación que era justo la semántica bajo test, así que ningún test podía expresar "raw 2 / publishable 1" y el gate en capa equivocada quedó sin cobertura. Un fake que pre-aplica la semántica que el SUT debe ejercitar convierte tests verdes en ceguera estructural, no en seguridad.
- La detección fue exclusivamente física (golden E2E), la etapa más lenta y cara del ciclo; el RCA/CORRECTION de hoy lo confirma: los gates de invariantes de contrato (cardinalidad, unicidad) deben testear la relación entre capas (raw vs publishable), no sólo cada capa contra un fake que asume el invariante.

## Pain Pattern Candidate

- "Test fakes que codifican el invariante bajo test": al diseñar un fake, preguntar explícitamente si puede expresar el escenario que rompe el invariante; si no puede, ese escenario no está testeado y el test no certifica nada sobre él.

## Acción sugerida

- Señal positiva a preservar: el procedimiento de [[embedded-postgres-maven-dns-timeout]] (PG manual desde `.txz` + `TEST_POSTGRES_DSN` + DB virgen por invocación) permitió correr hoy los targeted PG (61s) y la concurrencia ×10 (86.6s) sin redescubrimiento — mantener ese runbook como ruta canónica para cualquier sesión que necesite registry-postgres.

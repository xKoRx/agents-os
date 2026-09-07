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
  - "[[AGENTS OS]]"
related:
  - "[[2026-08-29-symphony-worker-observability-session-feedback]]"
aliases: []
confidence: verified
source_session: DURABLE-PROJECT-STAGES-RECOVERY-SLICE2-PRODUCER-OUTPUT-NORMAL
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/feedback
  - scope/session
---

# 2026-08-30-project-stages-recovery-slice2-session-feedback

%% Feedback solicitado explícitamente por el owner al cierre de la sesión. %%

## Contexto

- Sesión de implementación Slice 2 (record-before-put) sobre `xKoRx/symphony`; resultado PASS/CLOSED. Fricciones reales detectadas durante tests y diseño.

## Fricción

- Los steps del pipeline llaman `activity.GetInfo`/`RecordHeartbeat` incondicionalmente, así que TODO test unitario que ejecute upload/execute fuera del `testsuite` de Temporal panica con "Not an activity context" — obliga a envolver cada llamada en `env.ExecuteActivity` aunque el step bajo test no necesite nada de Temporal (fricción recurrente; ya había costado tiempo en slices anteriores).
- El backend MinIO de tests (`writeOnceTestBackend` en `artifact_store_test.go`) indexa objetos con el prefijo `"<bucket>/<key>"` implícito en el path y no está documentado en el helper; dos tests nuevos fallaron por sembrar/leer sin el prefijo antes de deducirlo del código.
- El presupuesto de 12 archivos choca con el radio real de los fakes de test: hacer fail-closed estricto a nivel steps por una capability nueva habría obligado a editar 3 archivos de test fuera del budget (resolveSpy); se resolvió con fail-closed a nivel Activity + semántica P0 documentada, pero el patrón "capability nueva ⇒ editar fakes en N archivos" se repetirá en el próximo slice que toque estos resolves.

## Pain Pattern Candidate

- Steps acoplados al contexto de actividad de Temporal en cualquier punto de su ejecución (no sólo I/O real): hace los tests unitarios de steps más caros de lo necesario y empuja a cubrir todo vía `env.ExecuteActivity`, más lento y con errores envueltos menos precisos para `errors.Is`.

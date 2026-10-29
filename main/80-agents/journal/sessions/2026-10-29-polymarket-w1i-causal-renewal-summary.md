---
type: session
schema_version: 1
scope: session
created: "2026-10-29"
updated: "2026-10-29"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine]]"
related:
  - "[[Research — Causal Metadata Renewal W1-i 2026-10-29]]"
  - "[[Plan — Single Episode Pilot v3 W1-i 2026-10-29]]"
aliases: []
confidence: high
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

# 2026-10-29-polymarket-w1i-causal-renewal-summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Mandato W1-i (one-shot GLM-5.3-Flash Max, offline): implementar la **opción B adjudicada por Metis** (prereg PE-005-R1 v2 §4) — renovación causal de evidencia para metadata idéntica — más la receta temporal serial V3 con deadlines absolutos; pruebas y commit LOCAL; sin captura, sin live, sin cambio de estrategia, sin adquisición. Excepción técnica acotada al freeze del checkout de investigación.

## Contexto cargado

- Bootstrap AgentsOS (constitución + perfil + continuidad global + índice de skills); HEAD `853c0e4` y rama `w0/offline-causal-replay-20261027` verificados; fixture W1-h untracked leída; prereg v2 §4 y Plan v2 W1-h; fuente real `regimes/{reducer,service,prospect}`, `capture`, `persist`, `cmd/engine/{record,clob_observe}`.

## Trabajo realizado

- Política pura `EvaluateRenewedConstraint` (`internal/regimes/renewal.go`): ancla de frescura en la última renovación admitida bajo doble cota (`received_wall≤t` Y `capture_seq≤seq`), por dimensión, fail-closed, determinista.
- Cuarentena AsOf con doble cota real enviada (`prospect.go`+`service.go`): `quarantine_at` viaja al gate; wall futuro no contamina; marca sin wall queda admitida (conservador).
- 15 tests nuevos: sondas puras del contrato + integración sobre store real (sondas W1-e, no-lookahead drain, contrato del ledger, receta V3 con reloj virtual).
- Bloqueador preciso declarado y wiring NO enviado roto: `migrations/0025_regime_observations.sql` requerido por el contrato y denegado (hook + allowlist); contrato fijado por tests; paso mecanizado en el Plan v3 §4.
- Sin lock nuevo: sin patrón compatible en el repo; exclusión = obligación del supervisor (documentada), `internal/capture` intacto.
- Fixture W1-h committeada byte-idéntica (SHA del prereg) — expectativas v1 válidas porque la semántica de producción no cambió.

## Artifacts creados o modificados

- Repo: commit `9e2c6b7dd26e70a53b05499a2d682ef33f1dac27` (6 archivos, +1773/−14, árbol limpio, sin push).
- OUT: `validated-baseline/w1-i-causal-renewal-20261029/` (`evidence-manifest.json`, `test-receipt.md`, binario `engine` sha256 `ba75bfb1…cb03b`).
- Vault: INFORME + PLAN V3 (doc), summary/feedback/agent_run (journal), change_log (sección añadida al log consolidado), continuidad (bullet (21)).

## Memoria propuesta o creada

- Ninguna en memoria interna global (sin delta transferible nuevo; las lecciones de fricción van al feedback).

## Decisiones

- Rechazar la elusión con `observed_at`/`last_observed_at` mutables (veredictos falsos en cortes retroactivos T0/T10/T20→T16) ⇒ migración 0025 como único camino válido; precisarla como bloqueador y seguir con lo entregable.
- No reescribir la fixture W1-h: sin cambio de semántica enviada, sus expectativas siguen válidas; preservar v1 byte-idéntica.
- Receta V3: 6×13,5 min + observes de 1 min = 88 min < 90 con margen 2 min; tramo+observe < TTL.

## Pendiente

- Shot siguiente (con autorización): crear `migrations/0025` + wiring reducer/service (≈40 líneas mecanizadas, Plan v3 §4) + re-corrida de regresión; recién entonces la receta V3 es adjudicable para captura.
- Lock de data-dir: bloqueo separado (sin patrón compatible en repo).

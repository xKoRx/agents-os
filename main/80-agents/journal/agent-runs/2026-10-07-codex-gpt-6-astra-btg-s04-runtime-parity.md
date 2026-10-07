---
type: agent_run
schema_version: 1
scope: session
created: "2026-10-07"
updated: "2026-10-07"
area:
project: "[[Echo Futures]]"
application:
entities: []
related: []
aliases: []
agent_surface: "[[Codex]]"
agent_model: gpt-6-astra
model_source: host
task_type: testing
task_complexity: high
outcome: partial
verification: failed
evaluator: agent
user_rework: unknown
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — BTG S04 runtime parity

## Trabajo

- Verifier LOCAL ONE-SHOT delegado de S04; modelo gpt-6-astra comunicado por coordinador desde turn_context del host. No se infiere por capacidad.
- Sólo dos nuevos archivos de pruebas `btg_s04_runtime_test.go` y `btg_s04_parity_adversarial_test.go` en core/internal/futuresvertical del clone de auditoría; cero producto/deploy/egress real.

## Evidencia

- SHA auditado `1bf45050780554c1135edc619bf01a8a4b04ba08`. Informe canónico receptor: [[BTG-S04-GOD-ADVERSARIAL]]. Fragmento y hashes en workspace `aranea/work/btg-s04-god-20261007/evidence/runtime/summary.md`.
- Diferencial acotado API pública backtester versus seis owners StateFun: PASS con NO_ADDS y CONFIGURED; mismos hechos, MM inputs/decisiones, comandos, señales, provider y terminal comparados estructuralmente.
- Repro propio RED: fill ADD adverso deja exposición7/protección5; favorable deja7/2 al finalizar cancelación. Repro sustitución runtime RED. Partial/cancel/late/duplicate PASS. Cinco regresiones existentes dirigidas PASS.
- No se certifica accounting runtime físico, transporte, D6, replay continuo entre cuentas ni toda paridad. No se cambia el baseline ni acepta gate.

## Resultado

- Outcome: partial respecto de amplitud B; hallazgos entregados al auditor padre. User rework: unknown.
- Sesión de worker cerrada por mandato explícito; no se cierra el programa ni Primary. Quota/tokens: UNKNOWN; no consumo Pro Chat confirmado.

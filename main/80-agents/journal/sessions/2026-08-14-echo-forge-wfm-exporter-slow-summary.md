---
type: session
schema_version: 1
scope: session
created: "2026-08-14"
updated: "2026-08-14"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge]]"
  - "[[Symphony]]"
related:
  - "[[2026-08-14-echo-forge-wfm-exporter-slow-raw]]"
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

# Diagnóstico wfm_exporter lento — handoff a corrección

> [!info]+ Session summary L1
> Resumen operativo. Para el agente de corrección, la evidencia completa (file:line incluidos) vive en [[2026-08-14-echo-forge-wfm-exporter-slow-raw]].

## Objetivo

- Explicar por qué la ejecución Temporal `sqx-main-00_configs-v1-XAUUSD-H1-L-1786733372` demoró tanto y proponer mejora.

## Conclusiones

- El workflow real duró 74 min; el 77.8% (57.6 min) es UNA activity `project` con task `wfm_exporter` (`EchoForgeWFMExporter`), 12 estrategias, en kron-0, sin retries.
- Causa raíz 1: el pipeline ejecuta el proyecto SQX **dos veces** (`steps.go:598-616` luego `steps.go:1013-1046` borra y repite); log SQX muestra 26m39s por ejecución, 2× ≈ 57.6 min.
- Causa raíz 2: el plugin exporta matriz 6x9 completa con reflexión Java por acceso a trade, loop serial single-thread (`EchoForgeWFMExporter.java:122-134, 265-288, 1076-1116`).
- No hay baseline (único run `sqx-main-*` en 90 días del namespace `sqx-prop`).

## Propuesta para corrección (en orden)

- P1: eliminar la doble ejecución en exporters (74 → ~46 min).
- P2: cachear reflexión + exportar solo vecindario 3x3 (junto a P1: 74 → ~20 min).
- P3 (opcional): particionar batch entre Zeus/Hera/Kronos; requiere project dirs por request.
- P4: higiene — heartbeat con progreso, timeouts sqcli, `MaximumAttempts` finito, fix `output_count`.

## Pendiente

- Agente de corrección toma P1+P4 primero (worker Go, tests en `project_activity_test.go`), medir próximo run, luego decidir P2 (plugin Java). Tarea registrada en el backlog de [[Echo Forge]].

---
type: feedback
schema_version: 1
scope: session
created: 2026-10-18
updated: 2026-10-18
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
related:
  - "[[2026-10-18-zcode-glm53-sqx144-cpu-utilization]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM 5.3 Flash (account:zai-individual-coding-plan/GLM-5.3-Flash)
agent_run: "[[2026-10-18-zcode-glm53-sqx144-cpu-utilization]]"
session_goal: Diagnóstico de rendimiento CPU SQX 144 en flota Forge con evidencia física
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
---

# Session Feedback — 2026-10-18 — sqx144-cpu-utilization

## Context

Mandato one-shot de rendimiento sobre la flota SQX 144 (Zeus/Hera/Kronos): diagnosticar la subutilización de CPU, forense del incidente Hera 05:05:43Z y dictamen Q1–Q10, todo read-only. Related run: [[2026-10-18-zcode-glm53-sqx144-cpu-utilization]].

## Hallazgos operativos (lo aprendido)

- **La evidencia decisiva era local y ya existía**: sysstat (sar) con historial diario en los 3 hosts + los logs por-run de SQX (`user/log/StrategyQuant`) + los logs JSON del worker dieron CPU real, fases y config sin lanzar nada. Prometheus/ARGUS no cubre la flota (sólo se scrapea a sí mismo) — para futuro diagnóstico de rendimiento, sar + logs > instrumentación nueva.
- **La unidad "Builder" de Forge es un proyecto de 2 tareas SQX** (genética + CustomAnalysis inyectada por `postProcessCFX`); medir "el builder" como una fase mezcla 3% de trabajo paralelo con 96% de fase secuencial. Cualquier throughput-conversation futura debe separarlas desde el enunciado.
- **`JAVA_TOOL_OPTIONS` vive en el drop-in systemd, no en scripts**: el contrato JVM efectivo de sqcli se compone por precedencia (JTO primero, sqcli.config después; duplicados gana el último). La skill/wrapper histórica de 142 está desactualizada como descripción del runtime.
- **Fricción menor**: el MCP SSH aplana here-docs y comandos multi-línea (conocido, re-confirmado) — trabajar con one-liners python -c; `sudo` está bloqueado por policy en role operator (correcto), lo que impidió leer journalctl de sistema para el incidente; la evidencia sustituta (`last -x`, sysstat LINUX RESTART, logs del worker) fue suficiente y/o mejor.
- **El manager reportó "run_sqcli.sh no existe en 144" y "wrapper con JVM 4GB"**: ambos datos de la skill antigua resultaron desactualizados (144 tiene run_sqcli.sh con 34g/55g, y Forge no usa wrapper alguno). Lección: los contratos de lanzamiento deben verificarse en disco por host antes de razonar sobre ellos.

## Sugerencias

- Si el owner quiere observabilidad continua de CPU por fase: node_exporter en los 3 hosts + dashboards ARGUS (hoy sólo sar 10-min retenido).
- Los ítems 4–6 de REMEDIATION-PLAN (paralelizar overview CustomAnalysis, re-armar proyecto en re-despacho) son las únicas palancas reales de throughput y requieren decisión de producto.

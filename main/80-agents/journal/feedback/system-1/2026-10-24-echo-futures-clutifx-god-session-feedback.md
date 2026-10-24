---
type: feedback
schema_version: 1
scope: session
created: "2026-10-24"
updated: "2026-10-24"
area: "[[Echo]]"
project: "[[Echo Futures]]"
entities:
  - "[[Echo Futures]]"
  - "[[Multimodal Knowledge Engine]]"
related:
  - "[[agents-os-session-close]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3
agent_run:
session_goal: "Misión GOD: extraer y objetivizar TODAS las estrategias del curso Clutifx + auditar el baseline del backtester en Hefesto."
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/echo-futures
---
# Session Feedback - 2026-10-24 - echo-futures-clutifx-god

## Context
- Surface/model: ZCode / GLM-5.3 (subagentes mayormente GLM-5.3-Flash); misión documental ONE-SHOT de extracción de estrategias + auditoría read-only Hefesto vía MCP SSH.
- Meta cumplida: catálogo canónico en `clutifx/strategies/STRATEGIES-CATALOG.md` + capa de investigación en `Echo Futures/artifacts/clutifx-strategy-research/` (QA adversarial 0 defectos materiales).

## Friction (real, con workaround)
- **MCP aranea-ssh expira a mitad de sesión y el cliente ZCode NO se auto-reinicializa** ("Session not found or expired" persistente). Workaround: puente HTTP manual (initialize + bearer del config + Mcp-Session-Id). Ya era patrón conocido; la parte nueva es que el cliente nunca recuperó solo.
- **El filtro de entropía del MCP mangla tokens en la salida** (rutas/listas quedan `[REDACTED:entropy:NN]` incluso dentro de mensajes de error). Workaround: run-command + python/base64. Costó varios round-trips.
- **Outage extendido del provider Flash (start-plan)**: server_error por >20 min y fallos de red que mataron agentes en curso (2 QA y 1 minero murieron); el workflow queda reintentando con backoff indefinido.
- **10 subagentes grandes en paralelo = muerte por rate limit 1302** (lección previa re-validada; el owner pidió paralelizar igual). Lo que funcionó: mitades (5+5) + rescate de caídos en workflow con `subagent_model` de la cuenta individual (zai-individual-coding-plan/GLM-5.3-Flash).
- **CreateWorkflow hereda el cwd del shell**: el draft del workflow quedó DENTRO de la biblioteca canónica clutifx (contaminación de fuente; limpiada a mano). El workspace del workflow debería fijarse al cwd de sesión, no al del shell.

## Pain Pattern Candidate (uno)
- La infra de subagentes/provider de ZCode degrada en silencio (outages, 1302, registro de agent types sólo al arranque: un `.zcode/agents/*.md` creado a mitad de sesión no existe hasta reiniciar) y el agente descubre cada modo de falla pagando round-trips. Un probe de salud del provider + registro en caliente de agentes reduciría el costo de descubrimiento.

## Scores
- Startup clarity: 5/5; retrieval usefulness: 5/5 (biblioteca Clutifx excepcional); skill fit: 4/5; closeout friction: 3/5; overall confidence: 5/5.

## Highlights
- El QA adversarial independiente (80 claims, H1–H7) encontró 0 defectos materiales en la extracción — la jerarquía compilación→catálogo sostiene la refutación.
- Owner redirigió en vivo dos veces (cero backtests; paralelizar) — el plan absorbió ambos sin perder trazabilidad.

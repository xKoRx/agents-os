---
type: feedback
schema_version: 1
scope: session
created: 2026-09-12
updated: 2026-09-12
area: "[[Echo]]"
project: "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
entities:
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
  - "[[Echo Forge]]"
related:
  - "[[AGENTS OS]]"
  - "[[2026-09-12-aranea-mcp-execution-gap-session-feedback]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: builtin:zai-coding-plan/GLM-5.3-Flash
agent_run:
session_goal: Ejecutar T2.12 PHYSICAL F-04 usando el deployment plane canónico de Symphony (corrección del manager)
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/agents-os
  - agent/system1
---

# Session Feedback - 2026-09-12 - f04-deployment-plane-contract-gap

## Context

- Agent surface: [[ZCode]]
- Agent model: builtin:zai-coding-plan/GLM-5.3-Flash
- Session goal: desplegar el build F-04 `d645ed6` con el deployment plane canónico (`deploy_release.sh` → deployer-watcher → MinIO → Stager) y ejecutar el run físico XAUUSD
- Main entity: [[Echo Forge — F-04 Magic allocation, version seal and handoff]]
- Skills used: bootstrap, sqx-deployer (Symphony), session-close
- Artifacts changed: proyecto F-04 (bitácora + estado), este feedback

## Scores

- Startup clarity: 4
- Retrieval usefulness: 4
- Skill fit: 5
- Template fit: 4
- Closeout friction: 2
- Overall confidence: 4

## What Complicated The Session Most

- Observation: el diagnóstico del feedback anterior ([[2026-09-12-aranea-mcp-execution-gap-session-feedback]], "T2.12 BLOCKED — ARANEA MCP por falta de capability de ejecución") quedó refutado: el deployment plane canónico corre desde la estación local y no requiere operator en ningún host; release `0.2.97` se publicó y rodó al fleet completo (~2 min) vía Stager sin tocar los hosts. La corrección del manager era correcta.
- Why it was hard: el bloqueo real resultó ser un defecto de contrato entre dos piezas frozen — `ParseMagicV1AllocationIdentity` (Magic V1, T1) parsea `<INSTRUMENT>_<D>_...` del canonical id, pero el registro productivo F-01 emite `<43-char-key>_<43-char-hash>`; los 4 durable applies fallan cerrado (`unknown direction token`) antes de cualquier INSERT. Los tests CONTRACT pasaron porque los fixtures codificaban el formato imaginado — mismo patrón de gap de fixture ya visto en el corpus S0 (E-04 P0). Sólo el físico lo revela.
- Proposed improvement: (1) al certificar contratos identity, añadir un gate CONTRACT que valide el formato contra datos reales del registro (row de `sqx.strategies`) y no sólo contra fixtures sintéticos; (2) surface MCP de ETCD (hoy se accedió con un probe Go one-off con credenciales leídas de ETCD, password jamás impresa); (3) `C:\ProgramData\Stager` en mt5-kronos es ilegible para echo-dev incluso con perfil operator no elevado — falta evidencia CURRENT/PENDING legible en Windows; (4) el MCP Mongo forge devolvió "session not found" toda la sesión.

## Most Useful Part Of Sistema 1

- What helped: la skill `sqx-deployer` + el orquestador `deploy_release.sh` (fail-closed con `release-authority` AUTO) hicieron el despliegue mecánico y verificable por evidencia durable (CURRENT/ACTIVATION.json/pollers); el monitoreo por PG del control plane (stage_executions/decisions/strategy_magic) resultó mucho más legible que los logs MCP truncados para seguir el flujo en vivo.

---
type: learning
schema_version: 1
scope: area
created: "2026-10-26"
updated: "2026-10-26"
area: "[[Echo]]"
project: "[[Echo Futures — Optimización de Campañas]]"
application:
entities:
  - "[[Echo Futures]]"
related: []
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: true
index_priority: low
tags:
  - kind/learning
  - scope/area
  - area/echo
---

# 2026-10-26-clf-q03-close-continuity

## Aprendizaje

- El host **Hefesto ES la máquina local del agente** (hostname `hefesto`, IP LAN 192.168.31.164, checkout `~/go/src/github.com/xKoRx/echo-clf`): si el MCP `aranea-ssh` expira («Session not found or expired»), el trabajo sobre Hefesto puede continuar directamente con herramientas locales sin degradar nada.
- El motor valida la identidad de build del plan (`build.commit` == revisión del binario, `tree_clean` == árbol REALmente limpio, fanout/schedule referencias por strategy-id): al mutar plantillas de un ciclo anterior hay que estampar commit/binario y reasociar TODAS las referencias; los `.pyc` trackeados rompían `tree_clean` (ya ignorados, commit `978e1803`).
- Estado Q03 cerrado: STR-001/003/004 implementadas y cualificadas G0–G4 en NQU6 (0 `CHALLENGE_PASSED` ⇒ G5 elegible=0); recibos sellados en `~/echo-work/clutifx-backtest/q03/receipts/` con guard verificado `BLOCKED/G4_NO_PASS`; entregables espejados en el vault `artifacts/clutifx-strategy-research/q03/`.

## Aplicabilidad

- **Cuándo cargarlo:** cualquier sesión sobre Echo Futures / ClutiFX en Hefesto, o al diagnosticar expiración del MCP aranea-ssh.
- **Cuándo no cargarlo:** trabajo Meli/corporativo u operaciones Forge en flota remota.

## Entidades relacionadas

- [[Echo Futures]] — [[Echo + Echo Forge — Environment Contract]]

## Evidencia

- Ejecución CLF-Q03 (2026-10-25/26): 3 commits pusheados con readback (`978e1803`), 9 corridas físicas NQU6, guard verificado con recibos reales; agent-run y change_log en el journal.

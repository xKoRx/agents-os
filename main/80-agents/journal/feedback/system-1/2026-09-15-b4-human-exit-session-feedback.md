---
type: session_feedback
schema_version: 1
date: 2026-09-15
project: "[[HERMES — Bootstrap & Self-Sufficiency]]"
area: "[[Aranea]]"
tags:
  - kind/feedback
  - area/aranea
  - system-1
---

# 2026-09-15 — B4 human exit session feedback

## Fricción

- **Recurrencia 3ª del anti-patrón stdin en ssh combinado, forma nueva:** no fue el heredoc-through-sudo ya documentado en `2026-09-15-b33-observability-session-feedback`, sino `mcps-ops "cat bearer" | ssh host 'bash -s' <<heredoc` — el heredoc ganó el stdin de ssh y `cat >` dentro del script consumió el resto del script como si fuera el bearer (447B de texto de script en el file destino; el bearer jamás cruzó). Detectado por sha mismatch pre-declarado y re-ejecutado separando pipe y script; daño cero. Regla reforzada: un stream stdin = un consumidor; pipe y heredoc nunca en el mismo ssh.

## Gaps

- Ninguno nuevo material. La lección reusable (validar llamadas del probe contra la superficie real del backend antes de congelar aserciones; falsos NOT_SET por `HOME` equivocado en sondas del chain) quedó incorporada en la skill vault `[[aranea-mcp-plane-operator]]` y el runbook capability-plane, no como gap abierto.
- Recordatorio heredado: Graphify seguía degradado al cierre B3.3 (query timeout / índice stale); esta sesión no lo usó para retrieval y no creó feedback Graphify dedicado — la recomendación de corrida `agents-os-graphify-maintenance` sigue abierta.

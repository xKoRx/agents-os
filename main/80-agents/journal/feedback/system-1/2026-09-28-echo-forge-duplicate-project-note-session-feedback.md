---
type: feedback
schema_version: 1
scope: system
created: "2026-09-28"
updated: "2026-09-28"
area: "[[Echo Forge — Operación Real V2]]"
project: "[[Echo Forge — Operación Real V2]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
related: []
aliases: []
confidence: verified
load_policy: manual
indexable: true
index_priority: low
tags:
  - kind/feedback
  - scope/system
# Feedback sesión 2026-09-28 — Echo Forge freeze fleet fan-out

## Pain Pattern Candidate

- **Nota de proyecto canónica DUPLICADA en dos carpetas del vault:** `10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2.md` (canónica activa, 264+ líneas con bitácora 14.ª/15.ª y artefactos) vs `10-projects/Echo Forge/Echo Forge — Operación Real V2.md` (copia stale, 152 líneas, sin bitácora 14.ª). En cold start sin routing preciso, el agente puede editar la copia stale (ocurrió en esta sesión; revertido) y partir el historial en dos fuentes. Mismo patrón de riesgo para todo el árbol `10-projects/Echo Forge/`.

## Evidencia

- Edición inicial aplicada por error a la copia stale; revertida y aplicada a la canónica tras contrastar bitácora 14.ª/updated. Registrado en `80-agents/journal/logs/2026-09-28-echo-forge-fleet-fanout-freeze.md`.

## Remedio propuesto

- Consolidación puntual con `agents-os-entity-lifecycle` (mergear la copia stale en la canónica, redirigir/eliminar el duplicado, verificar inbound links). No ejecutado en la sesión: fuera del mandato y requiere decisión de lifecycle.

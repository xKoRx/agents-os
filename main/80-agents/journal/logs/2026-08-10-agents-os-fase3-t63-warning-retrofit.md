---
type: change_log
schema_version: 1
status: active
created: 2026-08-10
updated: 2026-08-10
tags:
  - kind/change-log
  - project/agents-os
---

# T6.3 — Retrofit de warnings legacy

## Propósito

Registrar la clasificación y resolución auditable de los warnings del corpus.

## Contenido

- Migración canónica: páginas Aranea, runbooks, tickets, una decisión y memorias internas.
- Exclusión: sólo paths exactos de derivados, evidencia sin provenance, instrucciones de host y artefactos gestionados por plugin.
- Seguridad: `30-resources/APIs.md` fue saneado para no retener credenciales.
- Validación: lint/gate `0 ERROR / 0 WARN`, schema contract `0`, Graphify `5118` nodos / `6101` edges, Doctor `0/0/0` y Context Router E2E `14/14` con 0 misses.

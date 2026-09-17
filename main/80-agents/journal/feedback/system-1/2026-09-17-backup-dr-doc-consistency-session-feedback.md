---
type: feedback
scope: session
created: "2026-09-17"
updated: "2026-09-17"
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[2026-09-17-backup-dr-d0-documentation-consistency]]"
aliases: []
agent: "Ariadna (Hermes Agent, glm-5.3-flash)"
session_goal: "Saneamiento documental D0 del dominio Backup/DR"
source_session: "[[2026-09-17-backup-dr-d0-doc-consistency-raw]]"
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - area/aranea
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-summary.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# 2026-09-17-backup-dr-doc-consistency-session-feedback

> [!info]+ Session feedback (event-driven)
> Fricción real detectada durante D0 (no ritual de cierre).

## Pain points

- **Retrieval reintroduce histórico**: los 4 runbooks de `04-backups/` seguían `indexable: true`, `index_priority: high`, `confidence: medium` después de que R0 marcara sólo el README del directorio como HISTORICAL. Un agente que consulta un runbook individual recibe instrucciones de 2026-06-30 como si estuvieran vigentes. Neutralización individual (banner + indexable:false) requerida, no bastan índices ni READMEs.
- **Búsqueda por ID incompleto**: localizar tickets `018-021` por glob `*018-*` devolvía 0 resultados porque el patrón real es `2026-07-02-018-...`; `grep -rl` inicial falló por espacios en paths. Costó 2-3 iteraciones de discovery.

## Pain Pattern Candidate

- "README-only deprecation" como anti-patrón de vault: marcar deprecaciones a nivel de directorio deja los archivos hoja recuperables con autoridad operativa. Regla propuesta: deprecar hoja por hoja.

## Sugerencias

- Considerar en [[agents-os-hygiene-cycle]] un check de consistencia: archivos con `status: deprecated/superseded` referenciados por índices con `status: active`.
- Observado durante el close (2026-09-17): lint gate global con deuda preexistente (ERROR=213, WARN=67 a nivel vault; el auto-refresh de Graphify continuó en modo derivado). Fuera del alcance D0; candidato para un hygiene cycle dedicado.
- Discovery: los tickets con fecha-prefijo (`2026-07-02-018-...`) no se encuentran por glob del número solo (`*018-*`); buscar por prefijo de fecha o grep de contenido.

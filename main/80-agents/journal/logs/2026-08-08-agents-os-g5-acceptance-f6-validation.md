---
type: change_log
scope: project
created: 2026-08-08
updated: 2026-08-08
area: "[[Personal]]"
project: "[[AGENTS OS - Fase 2]]"
entities:
  - "[[AGENTS OS]]"
  - "[[AGENTS OS - Fase 2]]"
related:
  - "[[agents-os-bootstrap]]"
  - "[[agents-os-context-retrieval]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-08-08-agents-os-f6-surface-smoke-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/project
  - project/agents-os
---

# Change log — G5 aceptado y validación parcial F6

## Cambio

- **Tipo:** updated
- **Archivo:** [[AGENTS OS - Fase 2]].
- G5 pasó de `review` a `accepted`; F6 avanzó con T6.1, T6.4 y T6.6 cerradas.

## Motivo

- El owner pidió validar G5, corregir sólo si existía una desviación y avanzar
  a la fase siguiente.

## Fuentes usadas

- [[AGENTS OS - Fase 2]] y el registro del piloto F5.
- [[agents-os-bootstrap]], [[agents-os-context-retrieval]] y
  `agents-os-doctor/BENCHMARK.md`.

## Resolución aplicada

- G5 aceptado: fuentes canónicas, rollback y doctor estricto siguieron
  íntegros. Se conserva NO-GO temporal para retrofit masivo hasta verificar el
  rescan de caches de plugins path-based en una vista real.
- F6: cold/warm/swap, Graphify disponible y fallback por búsqueda dirigida
  verifican continuidad; se reindexó el grafo.
- T6.4 decide no adoptar watcher: 279 operaciones del query log tuvieron 2.9%
  de miss proxy y p95 de 598 ms, sin fricción medible de reindex manual.
- T6.2/T6.3 quedan WIP, sin falsificar éxito: Codex fresco alcanzó bootstrap
  pero fallaron hooks/plugins antes del reporte final; Claude CLI reportó
  reglas de permisos inválidas.

## Validación

- `agents-os-doctor --strict`: `HIGH=0 MEDIUM=0 LOW=0`.
- `graphify-obsidian update`: 5471 nodos, 6291 aristas.
- `explain`, `affected` y query dirigida resolvieron la entidad canónica;
  al ocultar el binario, la búsqueda dirigida conservó la fuente de startup.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos ni paths absolutos de máquina.

## Rollback

- Revertir la actualización de estado de G5/F6 en el planificador; no se
  modificaron fuentes runtime ni el layout del piloto.

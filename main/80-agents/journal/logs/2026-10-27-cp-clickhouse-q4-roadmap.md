---
type: change_log
schema_version: 1
scope: session
created: "2026-10-27"
updated: "2026-10-27"
area: "[[Meli]]"
project: "[[CP ClickHouse Q4]]"
application: "[[rio-controlplane-clickhouse]]"
entities:
  - "[[CP ClickHouse Q4]]"
related:
  - "[[Roadmap Q4 — CP ClickHouse]]"
  - "[[Import de Refreshable Materialized Views externas]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-10-27-cp-clickhouse-q4-roadmap

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `10-projects/Meli/CP ClickHouse Q4/CP ClickHouse Q4.md`
  - `10-projects/Meli/CP ClickHouse Q4/Roadmap Q4 — CP ClickHouse.md`

## Motivo

- El owner pidió ordenar el backlog de ClickHouse de Q4 para un equipo de dos, buscando reutilización, y documentar la propuesta completa en un proyecto nuevo.

- Iteración 2 (mismo día): el owner aclaró que el proyecto es interno, sin Spellbook, y que la meta es un ClickHouse full al cierre de Q4. Se agregó la definición de full, dos huecos fuera del backlog (salud del refresh en refreshable, import explícito de MergeTree) y se reemplazaron los épicos propuestos por docs internos de diseño.

- Iteración 3 (mismo día): el owner pidió priorizar por valor y que cada entregable sea funcional. El roadmap pasó de olas por pieza técnica a ocho entregables funcionales en dos lanes, con PRs habilitantes dentro del entregable que los consume y una agenda para acordarlo con Flor.

## Fuentes usadas

- Backlog pegado en la sesión (la planilla no se abrió).
- Código read-only: `rio-controlplane-clickhouse@origin/develop 4007bd28` y rama `feature/refreshable-view-import@377e3dcc`; `rio-playmaker@origin/develop 0c0e319c9`; `ads-signals-frontend@origin/develop`.
- Spellbook por CLI: SIG-705, SIG-640, SIG-528, SIG-690, SIG-461; proyecto CCN archivado.
- Vault: proyecto de import refreshable y plan de Context en ClickHouse.

## Resolución aplicada

- Proyecto raíz P0 con estado, entrega, tareas por ola y decisiones marcadas como propuestas; doc de roadmap con matriz backlog vs código, tres piezas base, olas y riesgos.

## Validación

- `lint.py --strict` sobre ambas notas: ERROR=0 WARN=0.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Borrar la carpeta `10-projects/Meli/CP ClickHouse Q4/` y este log.

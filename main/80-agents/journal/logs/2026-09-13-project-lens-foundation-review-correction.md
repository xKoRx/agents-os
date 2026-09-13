---
type: change_log
schema_version: 1
scope: session
created: "2026-09-13"
updated: "2026-09-13"
area: "[[Personal]]"
project: "[[Project Lens]]"
application:
entities:
  - "[[Project Lens — Foundation v0.1]]"
  - "[[Project Lens]]"
related: []
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

# 2026-09-13-project-lens-foundation-review-correction

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Personal/Project Lens/agentes/Project Lens — Foundation v0.1.md` — **actualizado** con las 4 correcciones load-bearing del FOUNDATION REVIEW del owner (arquitectura y roadmap ACCEPTED, sin reabrir decisiones): (1) Identity/API — Project identity == source Note path; API re-addressada por path (`/projects/{path...}`, nuevo `/projects/resolve` como convenience fail-closed, `tasks?project=<path>`); rutas Vue `/project/*path`; regla de identidad explícita en el contrato y en el domain model. (2) Generic Vault boundary — Frontmatter VO convertido a map YAML crudo genérico (el EntityEnvelope de Agents-OS queda como proyección de la capa Agents-OS en `internal/index`); Task separada en extracción raw (vault/parse) vs Task projection (index); split de dos capas conceptuales documentado en `internal/index` sin paquetes nuevos; T03/T06/T07/T15 alineados. (3) Scan consistency — congelado best-effort scan + immutable snapshot + atomic publication/swap en error model, arquitectura y T06; sin locking ni infra adicional. (4) MCP rationale — deferred por falta de consumidor agent-facing; reopen trigger = necesidad demostrada de query/retrieval programático sobre Lens; Graphify declarado NO-sustituto en non-goals, roadmap F8 y bitácora. Bitácora y Estado actual actualizados con la entrada FOUNDATION REVIEW.
  - `10-projects/Personal/Project Lens/Project Lens.md` — **actualizado** (1 línea): backlog MCP deja de afirmar "hoy Graphify cubre retrieval de agentes"; usa el reopen trigger del owner.

## Motivo

- Corrección del owner tras el review de la fundación: 4 observaciones load-bearing sobre identidad de API, frontera genérica del core, semántica de consistencia del scan y rationale del deferral de MCP.

## Fuentes usadas

- Mandato FOUNDATION REVIEW: CORRECTION del owner (2026-09-13) con las 4 correcciones numeradas.

## Resolución aplicada

- Cambios quirúrgicos sobre el mismo planner; ninguna decisión accepted reabierta (stack Go+Vue 3, Markdown authority, in-memory index, Graphify/SQLite deferred, roadmap F1–F5, subagent model, package topology intactos). Sin proyecto nuevo, sin product code.

## Validación

- Adversarial consistency pass ejecutado exclusivamente sobre las 4 correcciones: sin residuos de name-as-identity en API/router/tasks/domain; sin semántica Agents-OS residual en `internal/vault`/`internal/parse`; invariante de rebuild (T09) compatible con la nueva semántica de scan (se rescanea vault estático); sin capas ceremoniales nuevas. Lint `--strict` sobre las notas tocadas tras el cambio.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Restaurar ambas notas desde git (`git checkout <prev> -- "10-projects/Personal/Project Lens/agentes/Project Lens — Foundation v0.1.md" "10-projects/Personal/Project Lens/Project Lens.md"`); borrar este log. Sin efectos fuera del vault.

---
type: skill
schema_version: 1
name: agents-os-resource-wiki
scope: global
created: 2026-07-02
updated: 2026-08-10
description: Maintain 30-resources/ as a compiled, incrementally-maintained LLM Wiki. Use when ingesting a source into resources, answering a question against the resources wiki, keeping a domain's 00-index.md and log.md current, filing a good answer back as a page, or running a wiki lint/health pass. Pages are canonical Sistema 2 docs created from templates; Graphify remains a derived index. Do not confuse the curated wiki (source of truth in 30-resources/) with Graphify's throwaway --wiki output.
aliases:
  - agents-os-resource-wiki
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - action/resource-wiki
  - tech/agents-os
  - tech/graphify
  - scope/global
---

# AGENTS OS Resource Wiki

## Purpose

Operar `30-resources/` como una **wiki compilada**: evidencia fuente inmutable
se integra en páginas canónicas mantenidas, con provenance, freshness y
lifecycle explícitos. `00-index.md` selecciona qué abrir; Graphify es sólo el
índice derivado.

Esta skill es lazy-loaded por `agents-os-bootstrap`. No leerla en startup salvo que
la tarea sea ingerir/consultar/mantener contenido en `30-resources/`.

## Minimal Read

Canonical create: use `materialize_schema_note.py` per `note-types.md`; never hand-copy frontmatter.

1. `30-resources/00-RESOURCE-WIKI.md` — reglas y esquema de la wiki (autoridad operativa).
2. `../_shared/note-types.md` — Sistema 1 vs Sistema 2 y política de templates.
3. El tipo/mapping resuelto por `materialize_schema_note.py`; no abrir templates
   candidatos en bloque.
4. El `00-index.md` del dominio afectado, y sólo las páginas que la operación toque.

## Contrato de dominio activo

La autoridad completa vive en `30-resources/00-RESOURCE-WIKI.md`. Para ejecutar:

- Un dominio activo tiene en su raíz exactamente un `00-index.md` (`type:
  index`, `status: active`) y un `log.md`.
- Una carpeta sin ese par no se promueve implícitamente a dominio.
- `_sources/` es opcional, inmutable y está fuera de Graphify; cada origen
  relevante conserva una nota `type: source` resoluble.

## Frontera con otros artefactos (respuesta a "skill vs runbook vs memoria")

- **Esta skill = el CÓMO con criterio.** Orquesta ingest/query/lint, decide qué
  páginas tocar, cómo sintetizar y cuándo marcar contradicción. Involucra juicio.
- **Runbook `resource-wiki-lint-reindex` = la parte MECÁNICA.** Reindex de Graphify +
  validación de cobertura del índice + detección de huérfanos, con validación y
  rollback. La skill **lo invoca**, no lo reinventa.
- **Memoria/aprendizaje** = un QUÉ/POR-QUÉ que sesga criterio futuro (ej. "las queries
  semánticas de Graphify necesitan el nombre canónico de la entidad"). No va acá; va a
  `80-agents/memory/`.

## Procedure

### Ingest
1. Clasificar la fuente y resolver el dominio activo. Si es un dominio nuevo,
   materializar `00-index.md` por contrato + `log.md` antes de ingerir páginas.
2. Registrar provenance materializando `type: source`: `source_url` o `repo` +
   `path`; guardar captura bajo `_sources/` sólo si aporta evidencia durable.
3. Leer la fuente y seleccionar las páginas afectadas mediante el índice. No
   abrir todo el dominio por defecto.
4. Integrar en páginas canónicas materializadas por tipo. En páginas de
   conocimiento, actualizar `sources`; cambiar `last_verified` sólo tras
   contraste y asignar `confidence` según el contrato.
5. Reconciliar contradicciones y reemplazos: no borrar en silencio ni crear
   copias `-v2`; usar lifecycle/source links definidos por el contrato.
6. Actualizar el `00-index.md` (una fila vigente + una línea + meta que ayude a
   seleccionar) y su `updated`.
7. Append a `log.md`: `## [YYYY-MM-DD] ingest | <fuente> → <páginas tocadas>`.
8. Si cambió una entidad canónica existente, seguir `agents-os-entity-update`.

### Query
1. Retrieval barato primero: leer el `00-index.md` del dominio; para relaciones
   cruzadas o paths, `graphify-obsidian query/explain/path` con **nombre canónico**.
2. Abrir sólo las páginas relevantes. Sintetizar con citas a las páginas
   canónicas; verificar que desde ellas la provenance resuelva a notas source.
   Si la vigencia afecta la respuesta y `last_verified` es insuficiente,
   verificar la fuente o declarar el gap.
3. Si la respuesta tiene valor duradero, **archivarla como página nueva** (compounding)
   y actualizar índice + log. No dejar que muera en el chat.

### Lint (salud)
1. Invocar el runbook `resource-wiki-lint-reindex` (parte mecánica).
2. Validar por dominio activo: casing exacto y catálogo raíz único; `log.md`;
   filas vigentes; provenance resoluble; `_sources/` excluida; timestamps y
   lifecycle coherentes; huérfanos, contradicciones y conceptos sin página.
3. Staleness es event-driven. No marcar stale sólo por edad: exigir fuente
   nueva relevante, query sensible a vigencia o cadencia declarada por dominio.
4. Proponer próximas ingestas/preguntas. Registrar en `log.md` (`lint`).

## Hard Rules

- Toda página es Sistema 2 → **desde template**; si falta, crearlo antes/igual cambio.
- La página *es* el doc canónico; no crear copias paralelas que driftean.
- `00-index.md` se actualiza en cada ingest — índice stale = deuda.
- Toda página de conocimiento nueva o materialmente reescrita por ingest enlaza
  sus notas `source`; no usar texto libre o paths de máquina como provenance.
- `last_verified` significa verificación real, no fecha de edición.
- No indexar `_sources/`, `trash/`, `*.json` ni outputs de Graphify (ver
  `.graphifyignore`).
- No confundir la wiki curada (verdad, `30-resources/`) con `--wiki` de Graphify
  (derivado, `graphify-out/`).
- Naming canónico según `90-system/convenciones.md`.

## Output

```text
Operación:            ingest | query | lint
Dominio:
Fuente / pregunta:
Páginas creadas/tocadas:
Provenance resoluble: sí/no
Freshness/confidence:
Índice actualizado:   sí/no
Log actualizado:      sí/no
Contradicciones/huérfanos:
Próxima acción:
```

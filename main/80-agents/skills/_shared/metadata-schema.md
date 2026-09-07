---
type: doc
schema_version: 1
status: active
created: 2026-06-27
updated: 2026-09-03
tags:
  - kind/doc
  - kind/system
  - tech/agents-os
---

# Agent Memory System Metadata Schema

Guía humana para usar metadata S1. Los sets exactos de tipos, campos,
versiones, tags, secciones y templates viven únicamente en
`schema-contract.md`, cuyo bloque JSON es la autoridad ejecutable para S1 y
S2. Esta nota explica semántica y criterio; no mantiene tablas paralelas.

## Propósito

Definir la semántica humana de metadata S1 y dirigir a la autoridad ejecutable sin duplicar sus tablas.

## Contenido

## Frontera de autoridad

- `schema-contract.md`: contrato exacto y versionado.
- `note-types.md`: frontera conceptual S1/S2 y forma de cada artefacto.
- `90-system/convenciones.md`: convenciones humanas de Sistema 2.
- `agents-os-entity-lifecycle/scripts/lint.py`: lint legacy durante F1; en F2
  debe consumir el contrato ejecutable sin copiar constantes.
- `validate_schema_contract.py`: gate de contrato y cobertura de templates.

## Envelope

Toda nota creada bajo el contrato declara `type`, `schema_version`, `created`,
`updated` y `tags`. Sistema 1 agrega `scope`. Campos de routing como `area`,
`project`, `application`, `entities`, `related`, `aliases` y `slug` se usan
sólo si cambian retrieval o navegación.

Principio:

```text
Pocas propiedades, bien usadas.
Tags precisos.
Links explícitos.
Nada de YAML ceremonial.
```

## Semántica de `schema_version`

- Una nota nueva usa la versión `current` de `schema-contract.md`.
- Una nota sin versión es legacy read-only hasta que una modificación real
  justifique migrarla.
- Una versión no soportada se rechaza; no se adivina compatibilidad.
- Un cambio incompatible crea versión y migrador explícito.
- Los templates siempre usan la versión actual; no se crean notas desde un
  template legacy.

## Reglas duras de Sistema 1

- Las notas S1 no usan `status` ni `draft`.
- `scope` es singular; relaciones múltiples viven en `entities`.
- `agent_memory` vive bajo `80-agents/memory/internal/` y no reemplaza verdad
  pública ni entidades canónicas.
- `share_scope` se reserva para trazabilidad compartible: `team` sólo si no
  contiene identidad, paths locales, memoria interna ni preferencias privadas.
- `indexable` e `index_priority` describen retrieval; exclusiones reales se
  aplican por path y `.graphifyignore`.
- Links de routing usan el título Obsidian canónico. Variantes humanas viven
  en `aliases`; slugs técnicos viven en `slug`, tags o paths semánticos.
- Memoria obsoleta se elimina o reemplaza con change log; no se conserva como
  una segunda autoridad activa.

## Campos de retrieval

- `load_policy` decide cuándo una nota puede entrar al contexto.
- `memory_state` controla el lifecycle de memoria interna: `active`, `superseded` o `archived`; no reemplaza el `status` de entidades Sistema 2.
- `continuity_key` identifica un único slot de continuidad por entidad o preocupación. El camino normal actualiza ese slot en el mismo archivo; `supersedes` y `superseded_by` se usan sólo cuando el scope exige reemplazo físico.
- `indexable` decide elegibilidad para el índice derivado.
- `index_priority` ordena preferencia, no autoridad.
- `confidence` expresa calidad de evidencia, no estado de lifecycle.
- `source_session` enlaza procedencia cuando existe; no obliga a crear una
  sesión artificial.

Los valores permitidos y su obligatoriedad por tipo se consultan en el bloque
ejecutable de `schema-contract.md`.

## Tags

Los tags filtran; frontmatter y links enrutan. Toda nota usa el tag canónico
`kind/<type-kebab>` y las notas S1 materializan `scope/<scope>` al crearse.
Los prefijos de routing permitidos y tags vagos prohibidos viven en el
contrato ejecutable.

## Nombres de journal

Los artefactos de journal usan nombres humanos estables:

```text
80-agents/journal/sessions/raw/YYYY-MM-DD[-HHMM]-<human-topic>-raw.md
80-agents/journal/sessions/YYYY-MM-DD[-HHMM]-<human-topic>-summary.md
80-agents/journal/feedback/system-1/YYYY-MM-DD-<human-topic>-session-feedback.md
80-agents/journal/feedback/graphify/YYYY-MM-DD-<human-topic>-graphify-feedback.md
80-agents/journal/logs/YYYY-MM-DD-<human-topic>.md
```

IDs externos, UUIDs y hashes son metadata, no títulos ni filenames.

## IDs semánticos

El ID es el path bajo la raíz de memoria sin `.md`; no se agrega un campo `id`
paralelo. Usar segmentos lowercase kebab-case y nombres humanos estables.

## Criterio de creación

Crear memoria reusable sólo cuando sea vigente, scoped, enlazada a entidades y
cambie una decisión futura. No crearla para progreso puntual, comandos crudos,
debug temporal, consejo vago o verdad que pertenece a una entidad S2.

## Validación

```bash
python3 80-agents/skills/_shared/scripts/validate_schema_contract.py
```

Este gate debe quedar verde antes de crear o modificar contratos/templates.

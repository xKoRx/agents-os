---
type: change_log
scope: session
created: "2026-07-25"
updated: "2026-07-25"
area: "[[Personal]]"
project: "[[AGENTS OS - Hot Path y Cierre Silencioso]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os]]"
  - "[[agent-constitution]]"
  - "[[agents-os-bootstrap]]"
  - "[[agents-os-context-retrieval]]"
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
  - area/personal
  - project/agents-os
  - change/updated
---

# Hot Path Iteration — P1 Hot Path aplicado

## Cambio

- **Tipo:** updated (5 archivos canónicos)
- **Archivo(s):**
  - `80-agents/skills/agents-os-bootstrap/SKILL.md` — reescrito como la única
    máquina de estados del startup (modos cold / warm / swap-entity).
  - `80-agents/agents-os/agents-os.md` — adelgazado a mapa conceptual +
    routing; eliminados los dos procedimientos de startup duplicados y el
    ritual "cargar en cada mensaje".
  - `80-agents/skills/agents-os-context-retrieval/SKILL.md` — corregida la
    contradicción del Context Router (entry layer por intención, no
    waterfall estricto).
  - `80-agents/skills/_shared/metadata-schema.md` — `load_policy: always`
    declarado "closed club": solo constitución, perfil y UNA nota global
    interna. Prohibido para memorias de dominio.
  - `80-agents/agents-os/agent-constitution.md` — Mandamiento 16
    reformulado: "toda sesión con delta durable deja continuidad", no
    "toda sesión".

## Motivo

- El diagnóstico del brief de ChatGPT (preservado en
  `00-inbox/AGENTS OS Hot Path/agents-os-hot-path-brief.md`) mostró que el
  startup vivía en al menos tres versiones casi idénticas, pesaba ~21-24k
  tokens antes de cargar contexto de entidad (objetivo histórico ~3k), y
  obligaba a cargar memoria interna de dominio marcada `always` sin filtro.
- El Mandamiento 16 original generaba ruido: agents escribían notas internas
  "por cumplir el mandamiento" sin valor real (patrón observado en feedbacks
  del 2026-07-22 a 2026-07-25).
- La tabla del Context Router decía "nunca saltar capas" pero arrancaba
  relaciones/código en capa 2 — contradicción interna que confundía al agente.

## Fuentes usadas

- Brief de ChatGPT `agents-os-hot-path-brief.md` (sección "Propuesta: AGENTS
  OS Hot Path").
- Auditoría local previa del turno (P0) que confirmó los hallazgos.
- `80-agents/agents-os/agent-constitution.md` (mandamientos 10 y 16).
- `_shared/metadata-schema.md` (política de `load_policy`).
- ADR `token-economy-indexing-architecture` (preservado; este cambio lo
  implementa, no lo contradice).

## Resolución aplicada

- **Máquina de estados única:** `agents-os-bootstrap` define 3 modos
  (cold/warm/swap) con reglas claras de qué cargar, cuándo invalidar y cuándo
  omitir la orientation note. `agents-os.md` ya no tiene procedimiento.
- **Metadata routing:** solo UNA nota global interna puede ser `always`
  (`agents-os-operating-continuity.md`); las de dominio deben usar
  `when_*_loaded`. Esto se codificó en `metadata-schema.md` y en Hard Rules
  del bootstrap.
- **Context Router coherente:** la tabla ahora declara **entry layer** por
  intención y condición de escalado, no secuencia obligatoria. Las Hard Rules
  eliminaron "no saltar capas" en favor de "no cargar cuerpo sin selección
  previa".
- **Mandamiento 16 basado en valor:** el agente escribe memoria interna
  cuando hay delta durable (decisión, fricción, aprendizaje o continuidad
  real). Sesiones sin delta no tocan memoria por ritual.
- **`session-close` des marcado como always-load en la guía:** la sección
  "Carga Dinámica de Skills" ahora lista solo `bootstrap` + `context-retrieval`
  como always-load, y deja `session-close` como invocable por pedido
  explícito. (Esto se alinea con P2 pero ya quedó sembrado acá.)

## Validación

- Lectura cruzada: bootstrap ↔ agents-os.md ya no compiten; solo el bootstrap
  tiene procedimiento.
- `metadata-schema.md` y bootstrap coinciden en la regla "una sola nota
  global always".
- `context-retrieval` ya no se contradice con la tabla de intenciones.
- Mandamiento 16 coherente con la regla base de constitución "memorias
  compactas y autoentendibles" (no inflar contexto).
- El ADR `token-economy-indexing-architecture` sigue siendo canónico y este
  cambio lo realiza sin tocarlo.

## Compartibilidad

- **Scope:** local — todos los cambios son específicos del vault personal.
- **Redacción revisada:** sin identidad, paths locales, secretos ni memoria
  interna expuesta.

## Pendiente (inmediato)

- P2 Silent Close — reescribir `session-close` para cierre por delta +
  feedback event-driven + reporte default 1-2 líneas.
- P3 Doctor + Benchmark — crear skill `agents-os-doctor` y definir gate E2E.
- Migración de la nota global interna `agents-os-operating-continuity.md`
  (~270 líneas) — compactar secciones que ya son historia auditable fuera
  de la línea always (Changelog TP, ChatGPT pack, MCP catalogs). No se tocó
  en P1 para no mezclar con el refactor de contratos.

## Rollback

- Revertir los 5 archivos editados a su estado previo al P1.
- El ADR `token-economy-indexing-architecture` no fue tocado; no requiere
  rollback.
- Los archivos P0 (memoria Symphony, skill-authoring refs, PROJECT-STATE)
  son independientes y pueden quedarse aunque se revierta P1.

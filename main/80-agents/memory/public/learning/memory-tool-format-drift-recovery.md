---
type: learning
scope: agent
created: "2026-06-30"
updated: "2026-06-30"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
  - "[[Memory System]]"
related:
  - "[[~/.hermes/memories/MEMORY]]"
aliases: []
confidence: high
source_session: "[[2026-06-30-1636-aranea-docs-storage-batch-summary]]"
load_policy: never
indexable: true
index_priority: medium
tags:
  - kind/learning
  - scope/agent
  - area/personal
  - project/agents-os
---

# Learning: Cuando MEMORY.md drift-ea, **rewrite limpio**, no patch

> [!info]+ Learning
> **Aprendido:** 2026-06-30 · **Estado:** accepted

## Situación

El memory tool rechaza patches incrementales sobre `~/.hermes/memories/MEMORY.md` cuando el archivo en disco no puede hacer round-trip (estado de drift detectado internamente).

## Diagnóstico

El mensaje reporta:
> "file on disk has content that wouldn't round-trip through the memory tool
> (likely added by the patch tool, a shell append, a manual edit, or a
> concurrent session). A snapshot was saved to *.bak.{timestamp}. Resolve
> the drift first — either rewrite the file as a clean §-delimited list
> of entries, or move the extra content out — then retry."

## Regla aprendida

Cuando esto ocurre:

1. **NO intentar patch incremental** — el memory tool seguirá rechazando.
2. **Hacer rewrite completo** del archivo en formato `§-delimited`
   (cada línea empieza con `§`, sin frontmatter, contenido lineal) que el
   memory tool pueda round-trippear.
3. **Conservar TODAS las entradas previas**, solo compactar prosa y
   eliminar duplicación.
4. **Marcar explícitamente** las entradas nuevas vs heredadas (fecha en
   cada bloque `§ ----- Fecha`).
5. **No usar `write_file` con la ruta `.bak`** — el snapshot lo maneja
   el memory tool al hacer replace.

## Por qué funciona

El formato `§-delimited` es el round-trip canónico que el memory tool
espera. Patches que mezclan secciones con distintos prefijos, o que
agregan bloques con frontmatter ajeno, rompen el parser y disparan la
guarda anti-pérdida silenciosa (issue #26045 referenciado en el mensaje
de error).

## Anti-patrón observado

Tentar la opción "replace" sobre un MEMORY.md en estado de drift
causa el mismo rechazo. La única salida limpia es el rewrite total.

## Referencias

- Issue Hermes: #26045
- Plantilla de fallback: `§` prefix en cada línea

---
type: change_log
scope: project
created: 2026-07-04
updated: 2026-07-04
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os-hygiene-review]]"
tags:
  - kind/changelog
  - area/personal
  - project/agents-os
---

# 2026-07-04 — `agents-os-hygiene-review` = validar + regularizar TODO el Sistema 1

## Motivo

Pedido del owner: la skill de higiene debe tener el comportamiento para **validar y
regularizar todo el Sistema 1**, no una revisión parcial. Encodea el audit manual que se
corrió esta sesión para volverlo repetible.

## Cambios (`agents-os-hygiene-review/SKILL.md`)

- **Propósito** reescrito a validar **y** regularizar (detección + fix, no solo detección).
- **Nuevo scope `full-system-1`**: corpus completo (skills, memoria pública, docs Sistema 1,
  índices de wiki) auditado contra todos los principios sin importar fecha de cambio.
- **Delegación obligatoria a subagente** para scopes amplios (protege el propio contexto =
  economía de tokens); greps mecánicos los hace el agente, lecturas cualitativas el subagente.
- **System 1 Alignment Checks** (renombrado y ampliado): suma compacidad, budget soft-ceiling,
  agnosticismo de cliente, y clasificación skill/runbook/memoria — sobre los ya existentes
  (índice/tag/grafo, define==implement, frontmatter, links/alias/naming).
- **Fix Policy** partida en auto-fixes mecánicos (frontmatter, links no ambiguos, frescura de
  índice, lenguaje de cap) vs proposal-only estructural (procedimientos que compiten,
  reclasificación de artefactos, compactación de memorias).
- **Hard Rules**: no reescribir memorias en masa; verificar hallazgos de subagente; regularizar
  dentro del borde seguro, escalar lo estructural como propuesta.
- **Output**/reporte actualizado; "Required sections" convertido en puntero al contrato de
  Output (dogfooding "una fuente por hecho").

## Validación

- La skill ahora describe el mismo procedimiento que se ejecutó a mano esta sesión.
- Sin duplicación interna (secciones de reporte no se re-listan).

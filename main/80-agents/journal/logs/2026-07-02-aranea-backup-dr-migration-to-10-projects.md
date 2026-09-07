---
type: change_log
scope: session
created: "2026-07-02"
updated: "2026-07-02"
area: "[[Aranea]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
related:
  - "[[10-projects/Aranea]]"
  - "[[10-projects/Aranea/README]]"
  - "[[20-areas/Aranea]]"
  - "[[30-resources/aranea/00-index]]"
  - "[[30-resources/aranea/03-storage/backup-dr/00-INDEX]]"
  - "[[30-resources/aranea/05-tickets/README]]"
  - "[[30-resources/aranea/03-storage/backup-dr/DIFF-CONCEPTUAL]]"
aliases:
  - "aranea backup-dr migration 10-projects"
  - "convención PARA 10-projects por área"
confidence: verified
source_session: "2026-07-02 telegram ariadna"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-07-02 — Migración Backup/DR de `30-resources/` a `10-projects/Aranea/`

## Cambio

- **Tipo:** updated (movimiento de archivos + corrección de frontmatter + creación de índices)
- **Archivos:**
  - **Movidos** (15 archivos):
    - `30-resources/aranea/03-storage/backup-dr/BACKUP-DR-OWNER-PROJECT.md` → `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT.md`
    - `30-resources/aranea/03-storage/backup-dr/agent-project-00..08-policy-and-doc-cleanup.md` (9 archivos) → `10-projects/Aranea/agentes/`
    - `30-resources/aranea/05-tickets/2026-07-02-018..021-owner-task-*.md` (4 archivos) → `10-projects/Aranea/05-tickets/`
  - **Creados** (2 archivos):
    - `10-projects/Aranea/README.md` (índice de proyectos del área)
    - `80-agents/journal/logs/2026-07-02-aranea-backup-dr-migration-to-10-projects.md` (este log)
  - **Actualizados** (5 archivos):
    - `30-resources/aranea/03-storage/backup-dr/00-INDEX.md` — reescrito como índice de docs evergreen, link al proyecto nuevo
    - `30-resources/aranea/03-storage/backup-dr/DIFF-CONCEPTUAL.md` — nota de migración agregada
    - `30-resources/aranea/00-index.md` — referencias a tickets/proyectos actualizadas
    - `30-resources/aranea/05-tickets/README.md` — marca como "legacy" (histórico)
    - `20-areas/Aranea.md` — link al proyecto owner en lugar de propuesta deprecated
  - **Frontmatter corregido** (14 archivos):
    - `BACKUP-DR-OWNER-PROJECT.md`: `area: "[[Personal]]"` → `[[Aranea]]`, agregados `owner: me`, `root: true`, `priority: P1`, `start: 2026-07-02`, `parent` → `design_ref`
    - 9× `agent-project-*.md`: `area: "[[Personal]]"` → `[[Aranea]]`, `area/personal` → `area/aranea`
    - 4× `2026-07-02-018..021-*.md`: `area: "[[Personal]]"` → `[[Aranea]]`, `area/personal` → `area/aranea`, rutas relativas rotas → link canónico
    - `30-resources/aranea/03-storage/backup-dr/00-INDEX.md`: `area: "[[Personal]]"` → `[[Aranea]]`
    - `30-resources/aranea/05-tickets/README.md`: `area: "[[Personal]]"` → `[[Aranea]]`, `status: active` → `legacy`
  - **Rutas corregidas en cuerpo** (2 archivos):
    - `agent-project-00`: `../DESIGN-PROPOSAL.md` y `../PROPUESTA-COMPLETA-ITER4.md` → rutas absolutas desde nueva ubicación
    - 4× tickets 018-021: `[[../03-storage/backup-dr/BACKUP-DR-OWNER-PROJECT]]` → `[[BACKUP-DR-OWNER-PROJECT]]` (link canónico)

## Motivo

- **Convención del vault violada**: el proyecto Backup/DR era un **proyecto con plazo y tareas** (project owner, 9 subproyectos, 4 owner-tasks, calendario, DoD), pero vivía en `30-resources/aranea/03-storage/backup-dr/`. Esa ubicación es para **documentación evergreen** (diseño, runbook, checklist, policy), no para proyectos con plazo.
- **Owner correction 2026-07-02**: *"todo proyecto que tiene plazo y tareas se guarda en 10-projects. de ahí quiero poner carpetas por área que en este caso es aranea y dentro de esa carpeta que pongas este proyecto, que son las tareas a realizar. en resources va la documentación, esa que es prácticamente evergreen"*.
- **Convención aplicada** (de `[[90-system/convenciones]]` + skill `second-brain-vault-conventions`):
  - Proyecto con deadline/goal → `10-projects/<área>/<proyecto>`
  - Documentación evergreen → `30-resources/<área>/`
  - Carpeta por área dentro de `10-projects/`: en este caso `10-projects/Aranea/`
  - Subproyectos de agente → `<proyecto>/agentes/`
  - Tickets formales → `<proyecto>/05-tickets/`

## Fuentes usadas

- [[90-system/convenciones]] — `Regla de proyectos humanos vs proyectos de agente` + estructura del vault.
- `second-brain-vault-conventions` skill — `Pick the right folder` section, `Application vs Tool`, `Wikilinks — relative paths between folders`, `Common pitfalls`.
- [[20-areas/Aranea]] — área de Aranea.
- [[30-resources/aranea/00-index]] — índice de docs evergreen de Aranea.
- [[30-resources/aranea/03-storage/backup-dr/00-INDEX]] — índice previo del refactor Backup/DR.
- [[30-resources/aranea/05-tickets/README]] — índice histórico de tickets.

## Resolución aplicada

1. **Crear** `10-projects/Aranea/` con subcarpetas `agentes/` y `05-tickets/`, más `README.md` índice.
2. **Mover** el `BACKUP-DR-OWNER-PROJECT.md` (proyecto owner) a `10-projects/Aranea/` con:
   - `area: "[[Aranea]]"` (estaba `[[Personal]]`, incorrecto).
   - `owner: me`, `root: true`, `priority: P1` (campos de template project agregados).
   - `parent: "[[BACKUP-DR-DESIGN]]"` → `design_ref: "[[BACKUP-DR-DESIGN]]"` (era incorrecto tener parent hacia un doc de recursos).
3. **Mover** los 9 `agent-project-*` a `10-projects/Aranea/agentes/` (siguiendo patrón de `10-projects/AGENTS OS/agentes/`). `parent: "[[BACKUP-DR-OWNER-PROJECT]]"` se preserva (link canónico, sobrevive al move).
4. **Mover** los 4 tickets formales 018-021 a `10-projects/Aranea/05-tickets/`. Rutas relativas en `related:` reescritas a link canónico.
5. **Dejar** en `30-resources/aranea/03-storage/backup-dr/` solo la **documentación evergreen** (BACKUP-DR-DESIGN, RUNBOOK, CHECKLIST, policy, inventory-template, REQUEST-CHANGES, DIFF-CONCEPTUAL, RESTORE-DRILL-TEMPLATE, 00-INDEX reescrito).
6. **Actualizar** `30-resources/aranea/00-index.md`, `20-areas/Aranea.md`, `30-resources/aranea/05-tickets/README.md` y `30-resources/aranea/03-storage/backup-dr/DIFF-CONCEPTUAL.md` con referencias a la nueva ubicación.

## Validación

- ✅ `BACKUP-DR-OWNER-PROJECT.md` está en `10-projects/Aranea/` con frontmatter completo y correcto.
- ✅ Los 9 `agent-project-*` están en `10-projects/Aranea/agentes/` con `parent` preservado.
- ✅ Los 4 tickets 018-021 están en `10-projects/Aranea/05-tickets/` con `area/aranea` y links canónicos.
- ✅ `00-INDEX.md` de backup-dr/ actualizado para reflejar la nueva estructura.
- ✅ Auditoría de links rotos con `search_files` (patrón `03-storage/backup-dr/(BACKUP-DR-OWNER-PROJECT|agent-project)`): **0 resultados** → ningún link apunta a la ruta vieja.
- ✅ `20-areas/Aranea.md` actualizado: "[[30-resources/aranea/03-storage/DESIGN-PROPOSAL]]" → "[[10-projects/Aranea/BACKUP-DR-OWNER-PROJECT]]".
- ✅ `30-resources/aranea/00-index.md` actualizado: líneas 119-120 ahora apuntan a `[[../../10-projects/Aranea/...]]`.
- ⚠️ `[[backup-policy]]` en ticket 020 (link a un archivo `.yaml`, no `.md`): no resuelve en Obsidian pero es **pre-existente** al move, no introducido por este cambio. Anotado para próximo ciclo de hygiene.
- ⚠️ `RESTORE-DRILL-TEMPLATE.md` y `BACKUP-DR-RUNBOOK.md` y `BACKUP-DR-CHECKLIST.md` y `REQUEST-CHANGES.md` mantienen `parent: "[[BACKUP-DR-OWNER-PROJECT]]"` en su frontmatter. Esto es semánticamente válido (indican a qué proyecto sirven), pero técnicamente no son `type: project`, así que Dataview no los trata como subproyectos. Decisión: dejar como está (no es regresión introducida por este cambio).

## Consecuencias / Follow-ups

- **Next steps para el agente operativo**:
  - Reindexar Graphify (`graphify-obsidian update`) — la jerarquía cambió.
  - Validar queries enfocadas: `aranea backup-dr owner-project`, `agent-project-02`, `ticket 2026-07-02-018`.
  - Si algún script externo referencia rutas absolutas del filesystem (no wikilinks), actualizar.
- **Próxima sesión del agente**:
  - Si owner aprueba los 4 tickets 018-021, mover el proyecto a `status: active` y crear las tareas internas de cada agent-project.
  - Considerar si las otras 3 iniciativas de Aranea (Propuesta de storage, Observabilidad, Restore drills independientes) también deben migrar a `10-projects/Aranea/` o quedarse como sub-carpetas de `30-resources/aranea/`. **Decisión del owner**.

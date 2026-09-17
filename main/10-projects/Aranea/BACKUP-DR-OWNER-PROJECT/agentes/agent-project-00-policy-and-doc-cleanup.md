---
title: "agent-project-00 — Policy and doc cleanup"
type: project
schema_version: 1
owner: agent
root: false
status: done
status_detail: "DONE 2026-09-17: alcance julio ejecutado en R0 (marks deprecated en 5 docs de 03-storage, README 04-backups HISTORICAL, índice actualizado) y completado en D0: advertencias individuales en 9 docs legacy, índices alineados, wikilinks corregidos, tickets verificados. Evidencia: change_log 2026-09-17-backup-dr-d0-documentation-consistency."
priority: P2
progress: 100
icon: 🧹
slug: agent-project-00-policy-and-doc-cleanup
area: "[[Aranea]]"
project: "[[AGENTS OS]]"
created: 2026-07-01
updated: 2026-09-17
tags:
  - kind/project
  - area/aranea
  - project/agents-os
  - agent/owner
  - domain/backup
related:
  - "[[BACKUP-DR-DESIGN]]"
  - "[[../../../../30-resources/aranea/03-storage/DESIGN-PROPOSAL]]"
  - "[[../../../../30-resources/aranea/03-storage/PROPUESTA-COMPLETA-ITER4]]"
parent: "[[BACKUP-DR-OWNER-PROJECT]]"
cssclasses: wide
---

# 🧹 Agent Project 00: Policy and doc cleanup

## 🎯 Objetivo

Limpiar el vault de docs históricos/contradictorios y dejar el espacio docs listo para los 8 agent-projects siguientes. **NO toca infraestructura.**

## 📊 Estado actual

- **DONE (2026-09-17).** Alcance julio ejecutado durante R0 (2026-09-16): frontmatter deprecated en `DESIGN-PROPOSAL.md`, `PROPUESTA-COMPLETA-ITER4.md`, `BACKUP-SYSTEM.md`, `AUDIT.md`, `TOPOLOGY-AUDIT.md`; `04-backups/README.md` marcado HISTORICAL; `00-index.md` y capturas actualizadas (R0 §11).
- **Complemento D0 (2026-09-17)**: advertencia HISTORICAL individual al inicio de los 9 documentos legacy, `indexable: false` en los recuperables por retrieval, índices evergreen/área/proyectos alineados, wikilinks rotos corregidos y tickets 018-021 verificados (`open`, vigentes). Detalle: change log `2026-09-17-backup-dr-d0-documentation-consistency`.

## Scope

- Marcar `DESIGN-PROPOSAL.md` y `PROPUESTA-COMPLETA-ITER4.md` como deprecated.
- Actualizar ticket 013 a `superseded-by-backup-dr-design`.
- Crear índice `backup-dr/00-index.md`.
- Validar que todos los wikilinks internos del set backup-dr/* resuelven.

## Out of scope

- Tocar infraestructura.
- Modificar pools, VGs, LVs.
- Crear tickets nuevos.

## Required inputs

- [[BACKUP-DR-DESIGN]] (este refactor).
- [[BACKUP-DR-OWNER-PROJECT]].

## Required owner permissions

Ninguno. Lectura únicamente.

## Required credentials / secrets

Ninguno.

## Required maintenance window

Ninguno. Cambios solo a docs.

## Dependencies

Ninguna. Es el primer subproyecto.

## Protected resources

Todos los recursos protegidos listados en BACKUP-DR-DESIGN §2.

## Risks

| Riesgo | Mitigación |
|---|---|
| Wikilink roto en set backup-dr/* | Validar con `obsidian-graph` o grep antes de cerrar. |
| DESIGN-PROPOSAL queda huérfano | Marcar deprecated con link al nuevo. |

## Safety gates

- Cambio solo a docs. Sin tocar infraestructura.
- Diff visible en commit.

## Implementation plan

1. Crear `backup-dr/00-index.md` con links a los 16 archivos.
2. Editar `../../../../30-resources/aranea/03-storage/DESIGN-PROPOSAL.md` frontmatter: agregar `superseded_by: "[[BACKUP-DR-DESIGN]]"` y `status: deprecated`.
3. Editar `../../../../30-resources/aranea/03-storage/PROPUESTA-COMPLETA-ITER4.md` frontmatter: `status: deprecated`.
4. Editar ticket 013 frontmatter: `status: superseded`.
5. Validar wikilinks con search_files.

## Validation plan

- `ls backup-dr/` muestra los 16 archivos.
- Todos los `[[wikilinks]]` resuelven (no broken).
- Frontmatter deprecation visible en Obsidian graph.

## Rollback plan

`git revert` del commit.

## Evidence to collect

- Output de `ls backup-dr/`.
- Output de validación de wikilinks.
- Diff de cambios en `DESIGN-PROPOSAL.md`.

## Expected artifacts

- `00-index.md` nuevo.
- 3 archivos existentes con frontmatter updated.
- 1 ticket con status updated.

## Definition of Done

- [ ] Los 16 archivos backup-dr/* existen.
- [ ] DESIGN-PROPOSAL.md marcado deprecated.
- [ ] PROPUESTA-COMPLETA-ITER4.md marcado deprecated.
- [ ] Ticket 013 marcado superseded.
- [ ] Wikilinks válidos.
- [ ] Commit con diff visible.

## Linked owner tasks

Ninguno (no bloqueante).

## ✅ Tareas

- [x] **AGENT-TASK-00-1**: crear `00-index.md`. — EJECUTADO en R0 (índice evergreen existe y fue re-validado en D0).
  - agent_project: 00
  - depends_on: nada
  - blocked_by: nada
  - target_system: filesystem
  - commands_allowed: write_file, patch
  - commands_forbidden: ninguno que toque infra
  - expected_output: `00-index.md` con índice de los 16 archivos.
  - evidence_required: file_exists, file_size > 0.
  - validation: `ls -la backup-dr/00-index.md`.
  - rollback: `rm backup-dr/00-index.md`.
  - tags: [agent, doc-cleanup]

- [x] **AGENT-TASK-00-2**: marcar DESIGN-PROPOSAL como deprecated. — EJECUTADO en R0 (frontmatter) + D0 (banner HISTORICAL individual).
  - agent_project: 00
  - depends_on: nada
  - blocked_by: nada
  - target_system: filesystem
  - commands_allowed: patch
  - commands_forbidden: ninguno destructivo
  - expected_output: frontmatter con `superseded_by` y `status: deprecated`.
  - evidence_required: diff.
  - validation: grep `status: deprecated` en DESIGN-PROPOSAL.md.
  - rollback: `git checkout HEAD~ -- DESIGN-PROPOSAL.md`.
  - tags: [agent, doc-cleanup]

- [x] **AGENT-TASK-00-3**: marcar PROPUESTA-COMPLETA-ITER4 como deprecated. — EJECUTADO en R0 + D0 (banner individual).
  - tags: [agent, doc-cleanup]

- [x] **AGENT-TASK-00-4**: ticket 013. — RESUELTO-equivalente: el ticket quedó como registro histórico con cuerpo "Registro histórico de ejecución" y status `done` (el ticket SÍ fue ejecutado); sin autoridad operativa sobre decisiones actuales. No se altera su status porque `done` es su hecho histórico real.
  - tags: [agent, doc-cleanup]

- [x] **AGENT-TASK-00-5**: validar wikilinks backup-dr/*. — EJECUTADO en D0: pase determinista sobre el set (detallado en change log D0); links rotos reales corregidos.
  - agent_project: 00
  - depends_on: 00-1
  - blocked_by: nada
  - target_system: filesystem
  - commands_allowed: search_files, read_file
  - commands_forbidden: ninguno
  - expected_output: lista de wikilinks rotos (target: 0).
  - evidence_required: log con conteo.
  - validation: `grep -r '\[\[[^]]*\]\]' backup-dr/ | sort -u` revisado.
  - rollback: N/A (read-only).
  - tags: [agent, validation]

---

## Requirements

### Functional requirements
- FR-001: Todos los 16 archivos del refactor deben existir.
- FR-002: Wikilinks entre ellos deben ser válidos.

### Non-functional requirements
- NFR-001: Cambios solo a metadata (frontmatter), no al cuerpo del DESIGN-PROPOSAL histórico.

### Safety requirements
- SAFE-001: Ningún cambio a infraestructura.

### Observability requirements
- OBS-001: N/A (este subproyecto no produce eventos operacionales).

### Documentation requirements
- DOC-001: Mantener histórico accesible (no borrar docs viejos).

### Acceptance criteria
- AC-001: 16 archivos backup-dr/* existen.
- AC-002: 0 wikilinks rotos.
- AC-003: DESIGN-PROPOSAL.md, PROPUESTA-COMPLETA-ITER4.md, ticket 013 todos marcados deprecated/superseded.

---

**Status**: done (julio vía R0 + complemento D0; sin deuda documental abierta de este subproyecto).
**Sesión cerrada por instrucción del owner**: 2026-07-01.

## 📆 Bitácora

- **2026-08-10** — Migrado de `agent-project` legacy a `project` v1 sin activar la ejecución; owner, parent, lifecycle, progress, tags y secciones quedaron contractuales.

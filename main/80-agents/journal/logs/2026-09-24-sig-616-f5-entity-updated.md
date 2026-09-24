---
type: change_log
schema_version: 1
scope: session
created: "2026-09-24"
updated: "2026-09-24"
area: "[[Meli]]"
project: "[[SIG-616 — Autorización de operaciones por equipo]]"
application: "[[rio-playmaker]]"
entities:
  - "[[SIG-616 — Autorización de operaciones por equipo]]"
related:
  - "[[Descripción PR — rio-playmaker — Slice 5]]"
  - "[[2026-09-24-codex-unknown-sig-616-f5-sync]]"
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

# Actualización F5 de SIG-616 — 2026-09-24

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Meli/SIG-616 — Autorización de operaciones por equipo/SIG-616 — Autorización de operaciones por equipo.md`
  - `10-projects/Meli/SIG-616 — Autorización de operaciones por equipo/Descripción PR — rio-playmaker — Slice 5.md`

## Motivo

- La nota de proyecto y la descripción PR local todavía señalaban F5 `141eacbc5`, las variantes v23/v24 y resultados anteriores de CI/Fury.

## Fuentes usadas

- Hashes locales/remotos de Git; `gh pr view/checks 1182`; `fury list-versions`; confirmaciones de `fury create-version`.

## Resolución aplicada

- F4 `40d5f9b22` se integró en F5 `85a0c3bfc` y se publicó en PR #1182. Las ramas mock `v25@edff29c26` y `v26@4f1e29e6` quedaron publicadas; Fury aceptó `0.1.21-p5-committer-allowed` (`#1740`) y `0.1.22-p5-viewer-denied` (`#1741`).
- Se actualizaron el estado canónico de SIG-616 y la descripción PR local, manteniendo el merge conservador sin cambios fuera de los commits integrados.

## Validación

- Worktrees limpios tras push; PR #1182 `MERGEABLE`; sus cinco checks terminaron `SUCCESS` en CI #5498; builds Fury #1740/#1741 `FINISHED`. No hubo deploy ni smoke.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Restaurar las dos notas de SIG-616 desde el historial local y retirar este change log si se revierte el registro documental. Los commits y builds remotos requieren revertirse por separado.

---
type: known_error
schema_version: 1
scope: application
created: "2026-09-03"
updated: "2026-09-03"
area: "[[Meli]]"
application: "[[rio-playmaker]]"
entities:
  - "[[rio-playmaker]]"
related: []
aliases:
  - CLAUDE.md y Claude.md duplicados
  - cannot rebase you have unstaged changes en playmaker
confidence: high
source_session: 9c1f9d46-34d9-4921-809f-b823fb3343f1
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
---

# `CLAUDE.md` y `Claude.md` colisionan en macOS y bloquean rebase en rio-playmaker

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- `git status` muestra ` M Claude.md` de forma permanente, sin que nadie lo haya editado, y volver a hacer `git checkout --` no lo limpia.
- `git rebase` y `git cherry-pick` se niegan a arrancar con `cannot rebase: you have unstaged changes`, incluso cuando `git status` parece limpio.

## Causa

- El repo trackea **dos rutas que difieren sólo en mayúsculas**: `CLAUDE.md` y `Claude.md`. En un filesystem case-insensitive como el de macOS existe un solo archivo en disco, así que una de las dos rutas queda reportada como modificada para siempre.
- Mientras las dos apuntaron al mismo blob la colisión era invisible. El commit `e147842ae` de `develop` (`[TEST - NO MERGE] chore(aoc): initialize AOC context and session hooks`, PR #1111) le agregó el bloque `@AGENTS.md` sólo a `CLAUDE.md`, los blobs divergieron y la colisión se volvió visible.

## Impacto

- Bloquea cualquier `rebase` o `cherry-pick` en el repo hasta que se enmascare el archivo. Afecta a todos los que trabajen sobre `develop` en macOS, no sólo a una rama.

## Detección

- `git ls-files | grep -i '^claude.md$'` devuelve dos rutas.
- `git status --short` muestra ` M Claude.md` con el working tree recién clonado o recién limpiado.

## Mitigación

- Workaround para poder rebasar: `git update-index --assume-unchanged Claude.md`. **Sacarlo después** con `--no-assume-unchanged` para no dejar estado oculto que confunda al siguiente.
- Fix de fondo: borrar el duplicado del índice con `git rm --cached Claude.md` y dejar una sola ruta. El contenido vigente es el de `CLAUDE.md`, que es el que actualiza la tooling de AOC. Requiere coordinarlo en `develop`, no en una rama feature.

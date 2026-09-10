---
type: known_error
schema_version: 1
scope: global
created: "2026-09-09"
updated: "2026-09-09"
area: "[[Meli]]"
project:
application: "[[rio-playmaker]]"
entities:
  - "[[rio-playmaker]]"
related: []
aliases:
  - CLAUDE.md siempre modificado
  - Claude.md fantasma en git status
  - git case collision macOS
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/global
  - area/meli
  - app/rio-playmaker
  - tech/git
---

# Colisión de mayúsculas en git deja un archivo eternamente modificado

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- `git status` reporta un archivo como modificado de forma permanente, sin que nadie lo haya editado. `git checkout -- <archivo>` no lo limpia: sólo cambia cuál de dos nombres aparece sucio.
- El caso observado es `CLAUDE.md` en un repo Meli, pero aplica a cualquier par de rutas que difieran únicamente en mayúsculas.

## Causa

- El índice contiene **dos entradas** cuyos paths difieren sólo en capitalización, con blobs distintos. Se generan cuando alguien agrega la variante nueva desde un filesystem case-sensitive (Linux, CI) mientras la vieja ya estaba versionada.
- En macOS el filesystem es case-insensitive (`core.ignorecase=true`), así que sólo puede existir **un** archivo físico. Git lo compara contra las dos entradas y una de ellas siempre difiere.
- No es un agente, un hook ni una herramienta tocando el archivo. Es un defecto del índice del repo.

## Impacto

- Ruido permanente en `git status` que enmascara cambios reales y contamina cualquier verificación de working tree limpio, incluidos los gates de planes de trabajo y los checks post-tooling.
- Alta probabilidad de que se le atribuya la falla a la herramienta o al agente equivocado.

## Detección

```bash
git ls-files | grep -i "<nombre>"          # dos entradas que sólo difieren en mayúsculas
git config core.ignorecase                 # true en macOS
git rev-parse :RUTA_A :RUTA_B              # blobs distintos
git hash-object RUTA_EN_DISCO              # coincide con uno solo de los dos
```

## Mitigación

- **Local, no destructiva y reversible:** dejar en disco el blob canónico con `git checkout -- <variante-canónica>` y silenciar la entrada fantasma con `git update-index --skip-worktree <variante-obsoleta>`. Revertir con `--no-skip-worktree`. Esto limpia `git status` sin ocultar cambios reales, porque en ese filesystem la ruta duplicada no puede editarse de forma independiente.
- **Definitiva:** requiere un commit al repo que elimine una de las dos entradas del índice (`git rm --cached <variante-obsoleta>`). Es un cambio compartido y necesita PR; no se resuelve en el checkout de una persona.
- Nunca commitear el archivo para "arreglarlo": eso sólo mueve la suciedad a la otra entrada.

## Evidencia

- `rio-playmaker`, 2026-09-09: índice con `CLAUDE.md` (blob de 11580 bytes, agregado 2026-06-01 por la iniciativa de contexto para agentes) y `Claude.md` (11492 bytes, agregado 2026-02-05). El contenido del primero es superconjunto del segundo: agrega el bloque de referencia a `AGENTS.md`. En disco existía sólo un archivo y `git status` mostraba una de las dos entradas modificada de forma persistente.

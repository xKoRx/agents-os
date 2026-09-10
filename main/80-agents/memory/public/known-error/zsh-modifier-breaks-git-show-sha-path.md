---
type: known_error
schema_version: 1
scope: tool
created: "2026-08-24"
updated: "2026-08-24"
area:
project:
application:
entities: []
related: []
aliases: []
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/tool
  - scope/tool
---

# zsh-modifier-breaks-git-show-sha-path

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- `git show "$SHA:$PATH"` en zsh falla con `fatal: argumento ambiguo '<sha><basura>': revisión desconocida o ruta fuera del árbol de trabajo`, aunque el SHA y el path existan. La ruta que reporta el error aparece mutilada (`0524ce49ee/rio/...` en vez de `0524ce49e:src/main/java/com/mercadolibre/rio/...`).

## Causa

- zsh interpreta `:s`, `:h`, `:t`, `:r` y compañía como **modificadores de expansión de parámetro**. En `$B:src/main/...` el `:s` dispara el modificador de sustitución y se come parte del string. Las comillas dobles **no** lo evitan: el modificador se aplica en la expansión, no en el quoting.

## Impacto

- Auditar código contra un commit base —el patrón de una spec técnica— falla en silencio o con un error que apunta al lado equivocado, y es fácil concluir que el archivo no existe en esa revisión.

## Detección

- El error nombra una ruta que no escribiste, con el SHA pegado a un fragmento del path.

## Mitigación

- Armar la referencia completa en **una sola variable** antes de expandirla: `REF="$SHA:$PATH"; git show "$REF"`.
- O inlinear el SHA literal: `git show "0524ce49e:src/main/..."`.
- O volcar a archivo y trabajar sobre él: `git show "$REF" > /tmp/x.java`.

## Evidencia

- Reproducido el 2026-08-24 auditando `rio-playmaker` contra `develop @ 0524ce49e` y `rio-sdk-events` contra `master @ 9d86eb8`.

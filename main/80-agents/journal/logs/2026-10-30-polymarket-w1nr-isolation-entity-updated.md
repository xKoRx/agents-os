---
type: change_log
schema_version: 1
scope: session
created: "2026-10-30"
updated: "2026-10-30"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine — MVP]]"
related:
  - "[[Research — Default Suite Isolation W1-nR 2026-10-30]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-10-30-polymarket-w1nr-isolation-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - project/polymarket-engine
---

# 2026-10-30-polymarket-w1nr-isolation-entity-updated

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md`
  - `10-projects/Personal/Polymarket Engine/Polymarket Engine — Continuidad Five-POC 2026-09-20.md`
  - `10-projects/Personal/Polymarket Engine/Research — Default Suite Isolation W1-nR 2026-10-30.md` (creado)

## Motivo

- El estado vigente del proyecto cambió en un hecho verificable: la suite por defecto de `cmd/researchpilot` **ya no** puede reanalizar el episodio sellado ni sobrescribir rutas de evidencia, y la corrección está committeada localmente. Es verdad actual del proyecto, no progreso de sesión: la siguiente persona que corro la suite debe heredar el hecho, no la narración del disparo.

## Fuentes usadas

- Ejecuciones de comandos de este disparo: preflight de seguridad (`safe: true`, sin problemas), focal `-run '^TestW1NR'`, skip histórico `-run '^TestW1JAnalysisRevisionSealedEpisode$' -v`, suite de tres paquetes, build, `gofmt -l` y `git diff --check`.
- Repo `polymarket-engine`, rama `w0/offline-causal-replay-20261027`, commit local `4acf954407ede3e5bb42d057f35d7b2c7f02c913` (sin push).
- Informe canónico de este disparo: [[Research — Default Suite Isolation W1-nR 2026-10-30]].

## Resolución aplicada

- `[[Polymarket Engine — MVP]]`: se añadió el estado vigente W1-nR al inicio de «📊 Estado actual», se registró la tarea del disparo en «✅ Tareas» y una línea en «📆 Bitácora»; la aceptación de W1-n se conserva en su bloque original, sin reescribir historia.
- `[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]`: se añadió una sección de cierre con los hechos observables de W1-nR (causa, corrección, verificaciones, commit) y el límite explícito de que la medición de los hashes sellados corresponde al supervisor.
- Nota nueva de research con el detalle completo, incluida la tabla de fees y la adjudicación de la regla de L.

## Validación

- Verificado por comandos: preflight de seguridad verde antes y después de cada edición de fuente; focal, skip histórico, suite de tres paquetes y build verdes; `gofmt -l` vacío; `git diff --check` limpio; árbol de trabajo limpio tras el commit.
- **Vacío de validación declarado:** la medición de los 90 hashes sellados y de la lista final de archivos no la hizo esta sesión; el preflight sólo informa `sealed_unchanged: true` y esta sesión no escribió en rutas selladas. La certificación de preservación corresponde al supervisor.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir el commit local `4acf954` en `w0/offline-causal-replay-20261027` devuelve el árbol a `6249aabdd3bb3a0d7adb02a6c56e4bcb516599c1`, con el estado previo de W1-n (suite no aislada). Las notas del vault se corrigen editando los bloques agregados en esta sesión.
---
type: decision
schema_version: 1
scope: project
created: "2026-09-01"
updated: "2026-09-02"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities:
  - "[[Symphony]]"
related:
  - "[[2026-09-01-release-authority-stale-manifest-rollback]]"
  - "[[2026-09-02-release-wrapper-inflight-manifest-preflight-race]]"
aliases:
  - version allocation AUTO
confidence: verified
source_session: ECHO-FORGE-RELEASE-WRAPPER-INFLIGHT-PREFLIGHT-FIX-NORMAL
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
---

# 2026-09-01-release-version-authority

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Una versión de release identifica un conjunto immutable de artifacts.
- Hoy AUTO bumpea `published.version+1` (MinIO si `mc` existe, si no el manifest git local) y solo rechaza colisión en `deploy/<version>/` local.
- C3 demostró: published `0.2.78` < prefixes `0.2.79`–`0.2.83`, leftover `9.9.13`, overwrite de `0.2.79`, rollback del manifest git.

## Decisión

- Si `PUBLISHED_MANIFEST_VERSION` < `REMOTE_MAX` de la línea productiva `0.2.x` (o local materialized max de esa línea): estado `INCONSISTENT_RELEASE_AUTHORITY`; AUTO fail-closed. No publicar otra release hasta reconocerlo.
- `REMOTE_MAX` naive de todos los semver (incluye `9.9.13`) no es base de bump. Los leftovers `9.9.x` / `1.0.0` incompletos son evidencia, no autoridad.
- Si el prefix remoto `worker/sqx/<target>/` existe: exact-resume solo con hashes+revision idénticos; cualquier divergencia es `VERSION_COLLISION`, fail-closed, jamás overwrite/reuse.
- Target libre: `> published` AND `> remote_max(0.2.x)` AND `> local_max(0.2.x)` AND prefix remoto inexistente.
- El publisher no debe aceptar un manifest local de versión menor que la última publicada sin un flag explícito de rollback.
- La corrección quedó implementada y publicada en `xKoRx/symphony` commit `ee61d3d0b3b53416e80b231522342482322e556e`: `release-authority` concentra la asignación, `--target` hace preflight remoto, el planner verifica bytes por SHA256 y la manifest es monotónica.

## Rationale

- Un id de versión que apunta a dos conjuntos de bytes destruye la convergencia del stager (`verifyInstalled` sobre destination existente).
- AUTO que solo mira el manifest publicado ignora prefixes ya materializados y recrea colisiones (`0.2.79`).
- Bumpear desde `REMOTE_MAX` naive incluye leftovers `9.9.x` y no es autoridad de producción.

## Consecuencias

- C3-B no se retoma con `0.2.79`. El candidato tras el fix de tooling es `0.2.84` desde `441ea061`, sin restaurar `deploy/manifest.json` git `0.2.78`.
- No se borran prefixes históricos.
- El fix cabe en `deploy_release.sh` + tests del release tooling; no toca Forge product code.
- El próximo candidato operativo sigue siendo `0.2.84`, pero requiere `SQX_RELEASE_AUTHORITY_ACK_MAX=0.2.83` y debe construirse desde `ee61d3d0b3b53416e80b231522342482322e556e`; esta sesión no ejecutó recovery físico.

## Alternativas descartadas

- Bumpear ciegamente a `REMOTE_MAX+1` incluyendo `9.9.14`: reabre la línea de leftovers de prueba.
- Reusar `0.2.79` porque MinIO ahora tiene bytes C3: los stagers conservan el árbol Aug-29 y `stage()` no re-descarga un destination existente.
- Limpiar `mc rm` de `0.2.79`–`0.2.83` como primera solución: destruye evidencia e historia immutable.

## Estado vigente — 2026-09-02

- `release-authority --target X` clasifica `AVAILABLE` cuando el target remoto está vacío, `PARTIAL_EXACT_MATCH` cuando el conjunto remoto es un subconjunto no vacío de `expected` y cada objeto remoto coincide en key, tamaño, SHA-256 y bytes, `EXACT_MATCH` cuando ambos conjuntos son iguales, y `DIVERGENT` ante cualquier extra, mismatch, error de lectura o incertidumbre material.
- `PARTIAL_EXACT_MATCH` sólo es tolerable en el segundo preflight de una ejecución cuyo estado inicial fue `AVAILABLE`; un estado inicial `EXACT_MATCH` permite únicamente `EXACT_MATCH`. AUTO continúa exigiendo `AVAILABLE` al asignar un candidato nuevo.
- Un target igual a `published` continúa requiriendo `EXACT_MATCH`; `PARTIAL_EXACT_MATCH` nunca representa una release publicada ni mueve el commit point fuera del manifest remoto.
- La autoridad física vigente es `0.2.85`, con candidato `0.2.86`; el fix de control quedó en Symphony `2b4dff61bc0597204e6eeb1c920882cd5b77cd59` y no requiere reconstruir ni republicar `0.2.85`.

## Revalidación independiente — 2026-09-02

- La lectura real sin ACK confirmó `published=0.2.85`, `remote_line_max=0.2.85`, `local_line_max=0.2.85`, `authority_state=CONSISTENT`, `candidate_version=0.2.86`; `--target 0.2.85` devolvió `EXACT_MATCH` y `--target 0.2.86` devolvió `AVAILABLE`, ambos con JSON machine-readable limpio en stdout.

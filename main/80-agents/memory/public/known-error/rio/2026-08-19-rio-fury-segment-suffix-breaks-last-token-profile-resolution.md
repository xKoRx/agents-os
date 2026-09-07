---
type: known_error
schema_version: 1
scope: project
created: "2026-08-19"
updated: "2026-08-19"
area: "[[Meli]]"
project: "[[Estandarización de Scopes RIO]]"
application:
entities:
  - "[[RIO]]"
  - "[[rio-controlplane-kms]]"
related:
  - "[[scope-naming-standard]]"
  - "[[fury-segmentation-model]]"
aliases:
  - Fury suffix breaks Spring profile
  - nonprod profile por SCOPE suffix
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
  - area/meli
  - project/scopes-rio
  - tech/rio
  - tech/fury
---

# El sufijo de segmento Fury rompe la resolución de profile por último token

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- Un scope segmentado como `test-nonprod` o `alpha-api-nonprod` activa el Spring profile `nonprod` en vez del ambiente lógico esperado; si `application-nonprod.yml` no existe, la aplicación queda con configuración incompleta o incorrecta.

## Causa

- Fury agrega siempre `-<segment>` al nombre materializado, mientras algunas aplicaciones RIO calculan el profile tomando el último token de `SCOPE`. Ese token pasa a ser placement físico (`nonprod/nonsite`), no ambiente lógico (`prod/stage/alpha`).

## Impacto

- La migración de legacy a scopes segmentados puede desplegar con el profile equivocado, seleccionar recursos de otro ambiente o fallar al arrancar. El target de naming correcto no elimina el riesgo mientras profile y segmento sigan acoplados.

## Detección

- Buscar código que derive profiles, environment o configuración mediante `split(SCOPE, "-")`, `endsWith(...)` o el último token; verificar el profile efectivo usando un nombre materializado terminado en `nonprod/nonsite`.

## Mitigación

- Resolver explícitamente `scope materializado → environment_scope → profile/config`; mantener el segmento como placement independiente. Cubrir al menos `prod-api-nonsite`, `stage-api-nonprod` y `alpha-api-nonprod` con tests de selección de configuración antes de migrar routes o tráfico.

## Evidencia

- `rio-controlplane-kms`: `src/main/java/com/mercadolibre/rio/controlplane/kms/util/ScopeUtils.java` toma el último token y `src/main/resources/application.yml` lo usa como `spring.profiles.active`; existen profiles `prod`, `stage` y `test`, no `nonprod/nonsite`.
- [[Estandarización de Scopes RIO]] registra `rio-controlplane-kms/test` como piloto de segmentación con deadline 2026-09-09.

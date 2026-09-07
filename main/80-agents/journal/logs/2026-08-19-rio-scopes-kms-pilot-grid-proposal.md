---
type: change_log
schema_version: 1
scope: session
created: "2026-08-19"
updated: "2026-08-19"
area: "[[Meli]]"
project: "[[Estandarización de Scopes RIO]]"
application:
entities:
  - "[[Estandarización de Scopes RIO]]"
  - "[[RIO]]"
  - "[[rio-controlplane-kms]]"
related:
  - "[[scope-naming-standard]]"
  - "[[scope-inventory]]"
  - "[[2026-08-19-rio-fury-segment-suffix-breaks-last-token-profile-resolution]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: team
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-19-rio-scopes-kms-pilot-grid-proposal

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** conflict-resolution
- **Archivo(s):**
  - `10-projects/Meli/Estandarización de Scopes RIO/Estandarización de Scopes RIO.md` (updated — propuesta ejecutiva, piloto KMS, tareas, decisiones y preguntas abiertas)
  - `30-resources/rio-atlas/architecture/scope-naming-standard.md` (updated — nombre base RIO vs materialización Fury, routing front/back y filtro `scope:<x>`)
  - `30-resources/rio-atlas/architecture/scope-inventory.md` y `30-resources/grids/rio-scope-inventory.html` (regenerated — propuesta 2026-08-19 sobre baseline factual 2026-08-12)
  - `rio-inspector: rio-scope-policy.json`, `scope_inventory.py` y `rio-scopes.json` (updated — policy vigente y render-from-snapshot con refresh de propuesta)
  - `80-agents/memory/public/known-error/rio/2026-08-19-rio-fury-segment-suffix-breaks-last-token-profile-resolution.md` (created)

## Motivo

- La notificación Fury exige segmentar `rio-controlplane-kms/test` antes del 2026-09-09. El usuario aclaró que RIO define `<environment>-<role>` y Fury agrega siempre `-<segment>`; el grid y la spec conservaban textos incompatibles con esa autoridad y con la verificación reciente de filtros BigQueue.

## Fuentes usadas

- Correo de Fury compartido por el usuario; [[Estandarización de Scopes RIO]]; [[scope-naming-standard]]; snapshot reconciliado [[scope-inventory]]; `rio-controlplane-kms` `ScopeUtils.java` y archivos `application-*.yml`; evidencia de tags arbitrarios BigQueue ya registrada en el proyecto.

## Resolución aplicada

- KMS queda como primer slice vertical: base `alpha-api`, visible Fury `alpha-api-nonprod`, con `test-nonprod` sólo como bridge si la remediación lo exige. La propuesta completa usa selectores independientes `frontend/backend`, header de scope hacia Fury routes y topic compartido con filtro `scope:<x>`; profile/config se desacopla del sufijo físico.

## Validación

- Policy JSON parseada, generador Python compilado, render ejecutado sobre el snapshot reconciliado de 88 scopes, HTML inspeccionado en navegador, switch KMS verificado y consola sin errores. El refresh live Fury falló por acceso a los 10 service graphs, por lo que no se alteró ni se presentó como nuevo el corte factual.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales de máquina, memoria interna ni secretos

## Rollback

- Revertir la policy/generador y regenerar desde el mismo snapshot; las fuentes factuales del corte 2026-08-12 no fueron recollectadas ni reemplazadas.

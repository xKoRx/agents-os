---
type: change_log
schema_version: 1
scope: session
created: "2026-08-12"
updated: "2026-08-12"
area: "[[Meli]]"
project: "[[Estandarización de Scopes RIO]]"
application:
entities:
  - "[[Estandarización de Scopes RIO]]"
  - "[[scope-naming-standard]]"
  - "[[RIO]]"
related:
  - "[[scope-inventory]]"
  - "[[fury-segmentation-model]]"
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

# 2026-08-12-scopes-rio-nomenclatura-consolidada

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `30-resources/rio-atlas/architecture/scope-naming-standard.md` (updated — nueva sección "Estándar de Nomenclatura": gramática `<environment>-<role>[-<qualifier>]-<segment>`, vocabulario canónico de `role` por tipo de runtime, 4 criterios de excepción para múltiples scopes del mismo tipo+ambiente, regla trazable `consolidation_decision`, ejemplos aplicados; reemplaza la subsección "Gramática y grupos"; BR10 y BR12 reconciliadas)
  - `~/fuentes/rio-inspector/rio-scope-policy.json` (rewritten — schema 3: target_model con gramática/vocabulario/reglas nuevas; 10 apps re-nombradas a la forma triple, mínimo por (ambiente×tipo), webs extra colapsados en `api`, beta/gamma plegados en alpha, 10 bloques `consolidation_decisions` con proposed_action+justificación. Total objetivo 88→71)
  - `~/fuentes/rio-inspector/scope_inventory.py` (updated — copy del template HTML/Markdown corregido para describir el naming triple; los chips de retiro ahora muestran el segmento actual con `legacy` destacado + conteo legacy en la nota; nueva sección factual "Separación de ambientes hoy" y la sección de routing marcada como "propuesta · aún NO implementado" para separar hechos de propuesta)
  - `30-resources/grids/rio-scope-inventory.html` + `30-resources/rio-atlas/architecture/scope-inventory.md` + `~/fuentes/rio-inspector/rio-scopes.json` (regenerated — propuesta recomputada desde el snapshot existente sin colectar Fury live; grid verificado en navegador con nombres triples y KPI 88→71)
  - `10-projects/Meli/Estandarización de Scopes RIO/Estandarización de Scopes RIO.md` (updated — bitácora con la decisión de owner y la aplicación a policy+grid)

## Motivo

- Encargo del usuario (owner): fijar nomenclatura definitiva y criterios para cuándo se permite más de un scope del mismo tipo por ambiente, derivados de la conversación. El usuario decidió, contra la iteración anterior, que el segmento **sí** va en el nombre como último token renderizado desde `metadata.segment` real de Fury (el nombre es un render del estado real, no puede mentir; disuelve el bug original `consumer-prod-nonsite`).

## Fuentes usadas

- Datos vivos: `~/fuentes/rio-inspector/rio-scopes.json` (service graph Fury, 88 scopes) y `~/fuentes/rio-inspector/rio-scope-policy.json` (target state). Evidencia clave de que el segmento es eje independiente del nombre: `rio-controlplane-fury/prod-default-test--tp` = `env=Test, segment=legacy` pese a "prod" en el nombre.
- **Hallazgo de estado actual (routing):** hoy NO existe routing por ambiente lógico. El único eje de separación es el segmento físico (`nonsite`/`nonprod`) vía `ProducerBuilder.withSegmentID`; los topics se sufijan `--nonsite`/`--nonprod` (ej. `rio-deployment-trigger--nonprod.rio-playmaker`). Todos los scopes nonprod (test/stage/alpha) consumen los MISMOS topics `--nonprod`. `mqclient Filters` sólo expone `modified_fields` (MATCH_ANY). La sección "Routing entre ambientes" del grid era propuesta, no estado actual.
- Notas base: [[scope-naming-standard]], [[Estandarización de Scopes RIO]].

## Resolución aplicada

- Convención canónica `<environment>-<role>[-<qualifier>]-<segment>` con los tres tokens obligatorios; sin nombres pelados (`prod-api-nonsite`, no `prod`). Segmento ∈ {nonsite, nonprod} desde Fury; `legacy` no es objetivo (se migra).
- Baseline "1 scope por (ambiente × tipo de runtime)"; excepción sólo por criticidad/blast-radius, alertas/observabilidad, endpoints/contrato o aislamiento mandado, siempre documentada.
- Regla `consolidation_decision` para apps con scopes redundantes o tokens fuera del vocabulario: `collapse`/`keep_split` con justificación contra los criterios; la ratifica el equipo en Alineación.
- `rio-scope-policy.json` reescrita con el naming triple, colapso a mínimo por tipo, plegado de beta/gamma en alpha y 10 `consolidation_decisions` justificadas. Grid, inventario Markdown y snapshot JSON regenerados y verificados (render-from-snapshot, sin Fury live). Naming se mantiene `#blocked` hasta ratificación de Signals: la propuesta queda lista para llevar a Alineación, no aprobada.

## Validación

- Ejemplos aplicados verificados contra el snapshot: clickhouse (prod/alpha) y fury (6→4 tipos mínimos). BR10/BR12 quedaron consistentes con la nueva gramática (sin contradicción interna en el doc).

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales de máquina persistidos, memoria interna ni secretos.

## Rollback

- Cambio aditivo/reversible: restaurar la subsección "Gramática y grupos" previa y el texto original de BR10/BR12 en `scope-naming-standard.md`, y borrar la línea de bitácora en la nota de proyecto.

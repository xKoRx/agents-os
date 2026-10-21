---
type: learning
schema_version: 1
scope: area
created: "2026-10-20"
updated: "2026-10-20"
area: "[[Meli]]"
project: "[[CP Flink local]]"
application:
entities: ["[[rio-controlplane-flink]]", "[[RIO E2E local]]"]
related: []
aliases: []
confidence: verified
source_session: "52f1d97c-f4aa-484d-a98b-a2563272cae2"
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/area
  - area/meli
  - tech/git
---

# PR apilado tras un squash merge de su base

## Aprendizaje

- Cuando el PR base se mergea como **squash** (commit con un solo padre), develop no contiene la historia de la rama base y el PR apilado muestra conflictos add/add en todos los archivos que creó la base. El orden que funciona es mergear primero la **rama base final** en la apilada (conflictos reales y acotados) y después `develop`, que ya resulta trivial porque su árbol es igual a la punta de la base. Ningún rebase ni force-push.
- Un merge limpio no basta: revisar los contratos que la base cambió después de que se cortó la rama apilada. En Flink, PR 1 volvió idempotente a `create()` y movió `describeApp` a la vista de salud, lo que habría roto el UPDATE de PR 2 y la expectativa de un test, aun sin conflicto textual.
- Comparar los nombres de los métodos `@Test` de ambos padres contra el resultado, para demostrar que la resolución no perdió tests.

## Aplicabilidad

- **Cuándo cargarlo:** al sincronizar un PR apilado de RIO cuya base ya se mergeó, o cuando GitHub marca DIRTY un PR apilado justo después del merge de su base.
- **Cuándo no cargarlo:** bases mergeadas con merge commit normal (dos padres) o PRs no apilados.

## Entidades relacionadas

- [[CP Flink local]] · [[rio-controlplane-flink]]

## Evidencia

- Fuente: [[2026-10-20-flink-pr211-pr213-sync-updated]]: `0b60e64b` tiene un solo padre; #211 pasó de DIRTY a BLOCKED (sólo falta review) con `9d3253ac` (kiss) + `67081cde` (develop).

---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Import de Refreshable Materialized Views externas]]"
  - "[[ads-signals-frontend]]"
  - "[[10-projects/Meli/Import de Refreshable Materialized Views externas/Descripción PR — rio-playmaker]]"
  - "[[10-projects/Meli/Import de Refreshable Materialized Views externas/Descripción PR — rio-controlplane-clickhouse]]"
  - "[[10-projects/Meli/Import de Refreshable Materialized Views externas/Descripción PR — lore]]"
aliases: []
tags:
  - kind/doc
  - project/import-de-refreshable-materialized-views-externas
created: "2026-10-21"
updated: "2026-10-24"
---

# Descripción PR — ads-signals-frontend

ads-signals-frontend · `feature/refreshable-view-import` @ `36749c94b3248f212003183458dce2f044dd044b` · base `origin/develop` @ `e679afecb35b6e6d9ecf62cf6cbcf115c6efa256` · 20 commits · 22 files changed, 1801 insertions(+), 304 deletions(-) · [draft #816](https://github.com/melisource/fury_ads-signals-frontend/pull/816) · SIG-700 / SIG-703 · jest 122 suites / 3390 tests, lint 0 errors / 385 warnings, typecheck 123 inherited diagnostics (2026-10-24) · versión de prueba `0.0.2-import-ref-view-ch`.

> [!warning] Bloqueantes
> **Typecheck rojo heredado:** `npm run typecheck` termina con exit 2 y 123 diagnósticos; la lista normalizada es idéntica a la de develop, pero el comando no está verde.
> **Orden de rollout:** CP (#362) y Playmaker (#1328) antes del frontend.

## Propósito

Conservar el cuerpo verificable del PR junto al proyecto, con el template del repo y enlazado a los PRs hermanos.

## Contenido

Cuerpo del PR listo para pegar, seguido de notas internas que no van al PR.

---

[description]: https://img.icons8.com/material-sharp/24/000000/document.png
[checkmark]: https://img.icons8.com/material-sharp/24/000000/checkmark.png
[checklist]: https://img.icons8.com/material-sharp/24/000000/check-all.png
[testing]: https://img.icons8.com/material-sharp/24/000000/test-partial-passed.png

# ![alt text][description] PR Description

## What is the current behavior?

A refreshable materialized view that already exists in ClickHouse cannot be brought into a pipeline. The Refreshable Table form only creates new views, and the materialized view import modal is limited to incremental views.

## What is the expected behavior with the new change?

The Refreshable Table form offers **Import external refreshable view**: the user picks warehouse, schema and view name, reviews owner, source, destination and SQL, confirms, and the component is prefilled as an external reference.

- The imported SQL is normalized only in its header: `DEFINER` and `SQL SECURITY` are removed up to the main `AS SELECT`, while `WHERE` predicates, literals and comments stay intact. `SHOW CREATE` projections such as `window` are quoted.
- Source, destination, write mode and SQL stay read-only during review. The first save is allowed without adding source or destination components to the pipeline.
- After the first successful deployment the external view is fully read-only and the form says so. A failed first deployment keeps the previous behavior.
- A missing owner and a missing ClickHouse user produce distinct blocking messages.
- The materialized view modal directs refreshable definitions to the Refreshable Table form. External incremental views and MergeTree references keep their current behavior.

The feature was developed together with the local RIO ecosystem E2E ([Playmaker #1332](https://github.com/melisource/fury_rio-playmaker/pull/1332)): the import journey runs in Lore against local Playmaker and the ClickHouse control plane, using the drag-and-drop tool added in [Lore #21](https://github.com/melisource/fury_lore/pull/21).

# ![alt text][testing] Testing

## How to test the new behavior?

1. Deploy, in order, ClickHouse control plane [0.0.3-import-ref-view-ch](https://web.furycloud.io/rio-controlplane-clickhouse/versions/detail/0.0.3-import-ref-view-ch), Playmaker [0.0.2-import-ref-view-ch](https://web.furycloud.io/rio-playmaker/versions/detail/0.0.2-import-ref-view-ch) and this frontend [0.0.3-import-ref-view-ch](https://web.furycloud.io/ads-signals-frontend/versions/detail/0.0.3-import-ref-view-ch).
2. Preload the import credential of the view owner, then open a data product and drag **Refreshable Table** onto the canvas.
3. Click **Import external refreshable view**, choose warehouse, schema and view, click **Search refreshable view** and **Confirm import**. Check owner, source and destination in the preview.
4. Save: the node appears as Not Deployed. Deploy it: the view keeps its UUID, DDL and target data in ClickHouse.
5. Reopen the node: every field is read-only, there is no Save and the form shows "This external view is deployed. Its configuration is read-only."

Automated checks on `f599fa78b`:

- `NODE_ENV=test npx jest src/__tests__/technologies src/__tests__/node-config-modal tests/unit/api/external-materialized-views`: 129 suites, 3692 tests passed.
- `npm run lint`: 0 errors, 375 warnings.
- `npm run typecheck`: exit 2 with 122 diagnostics; the normalized list matches develop.
- Local E2E `rio-ecosystem all clickhouse-refreshable-view-import`: Lore run `run_mvmmx1oa2d7d9a404d` passed 5/5 scenarios (import and save, first deploy, reprovision, read-only after deploy) and 8/8 backend checks.

# ![alt text][checkmark] Related Issue

[SIG-700](https://spellbook.adminml.com/projects/SIG/specs/SIG-700) · [SIG-703](https://spellbook.adminml.com/projects/SIG/specs/SIG-703) · [CP #362](https://github.com/melisource/fury_rio-controlplane-clickhouse/pull/362) · [Playmaker #1328](https://github.com/melisource/fury_rio-playmaker/pull/1328)

# ![alt text][checklist] PR Checklist

- [x] I carefully reviewed the code before creating this PR.
- [x] I made sure the `diff` clearly represents my changes.
- [x] I made sure this PR doesn't make sense to split into smaller PRs.
- [x] I verified that my code style and scaffolding follow the project standards.
- [x] I made sure my changes don't affect any functionality other than this PR.
- [x] I added/modified the necessary `tests` for the component or functionality I'm implementing.
- [x] I ran the `tests` and made sure they pass.
- [x] I updated the `CHANGELOG.md` file with the change in the `[Unreleased]` section under `Fixed` or `Added` as appropriate.
- [ ] I made sure to update the README with the new behavior, if applicable. — not applicable

---

## Notas internas — NO van al PR

- PA-1 a PA-5 siguen abiertas.
- La E2E del 2026-10-24 encontró que la externa desplegada mostraba "Refresh parameters and the query can change"; corregido en `36749c94b` y cubierto por el escenario `clickhouse-refreshable-view-import-readonly`.
- Correcciones de la auditoría: bloqueo de Save acotado a adapters con `managesExternalReferenceReadOnly` (MV y MergeTree externos vuelven al comportamiento de develop), tests del primer deploy fallido en form y modal, nota contradictoria en revisión de import, mensajes excluyentes de owner, CHANGELOG deduplicado.
- Abiertos de baja severidad: el normalizador no limpia `DEFINER = 'x'` ni cabeceras con CTE (falla cerrado con "Unsupported SQL"); el preview de MV cambió su presentación (mismos textos).

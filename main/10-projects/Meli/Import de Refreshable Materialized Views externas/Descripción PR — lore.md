---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related: ["[[Import de Refreshable Materialized Views externas]]", "[[lore]]", "[[10-projects/Meli/Import de Refreshable Materialized Views externas/Descripción PR — rio-playmaker]]", "[[10-projects/Meli/Import de Refreshable Materialized Views externas/Descripción PR — rio-controlplane-clickhouse]]", "[[10-projects/Meli/Import de Refreshable Materialized Views externas/Descripción PR — ads-signals-frontend]]"]
aliases: []
tags:
  - kind/doc
  - project/import-de-refreshable-materialized-views-externas
created: "2026-10-23"
updated: "2026-10-24"
---

# Descripción PR — lore

lore · `feature/rio-ecosystem-drag-and-drop` @ `edb5fc01103c6aa197ca11a23bdfc50742342013` · base `origin/develop` @ `e1c05efa266f8a243f92d5da1d86d1881cd870a6` · 5 commits · 11 files changed, 277 insertions(+), 6 deletions(-) · [draft #21](https://github.com/melisource/fury_lore/pull/21) · vitest runner 18 files / 277 tests, typecheck PASS, lint 0 errors / 437 warnings (2026-10-24).

> [!note] Sin bloqueantes propios
> El repo no tiene template `.github` de PR; se usan las secciones mínimas (qué cambia, por qué, cómo se probó, relacionado).

## Propósito

Conservar el cuerpo verificable del PR junto al proyecto, enlazado a los PRs hermanos.

## Contenido

Cuerpo del PR listo para pegar, seguido de notas internas que no van al PR.

---

## What changes

Browser agents get a generic `browser_drag_and_drop` tool that drags one element onto another using `sourceRef` and `targetRef` from the latest `browser_snapshot`.

- `BrowserSession.dragAndDrop` uses Playwright `dragTo`, which sends real mouse input; in Chromium it produces HTML5 drag events when the source is `draggable`.
- Both refs go through the same validation and active-origin check as `browser_click`. Identical source and target refs are rejected without touching the page.
- The tool counts against the scenario tool budget like a click, is offered by both model drivers and is not advertised to native agents.
- The agent prompt lists the tool among the ref consumers and asks for a fresh snapshot after dropping. README and CHANGELOG document it.

## Why

Scenarios could not exercise interfaces that are driven by drag and drop, such as adding a component from a library onto a canvas. The tool has no product-specific logic.

## How it was tested

- `npx vitest --run tests/unit/runner`: 18 files, 277 tests passed. Covers ref validation, identical refs, unavailable sessions, a host without drag support, the active-origin check and a real Chromium drop.
- `npm run typecheck`: passed. `npm run lint`: 0 errors, 437 warnings.
- Used by the RIO ecosystem import scenarios ([Playmaker #1328](https://github.com/melisource/fury_rio-playmaker/pull/1328), local E2E initiative [Playmaker #1332](https://github.com/melisource/fury_rio-playmaker/pull/1332)): Lore run `run_mvmmx1oa2d7d9a404d` dragged the Refreshable Table card onto the pipeline canvas and passed 5/5 scenarios.

## Related

SIG-700 · [CP #362](https://github.com/melisource/fury_rio-controlplane-clickhouse/pull/362) · [frontend #816](https://github.com/melisource/fury_ads-signals-frontend/pull/816) · [Playmaker #1328](https://github.com/melisource/fury_rio-playmaker/pull/1328)

---

## Notas internas — NO van al PR

- HEAD `1381004` (2026-10-24): CI verde tras agregar el guard de Chromium al spec de drag. `dependencies` rojo por vulnerabilidades de develop, no del PR.

- Una ref obsoleta espera el timeout de acción (8 s) y devuelve un mensaje genérico de timeout, igual que `click`.
- Librerías de drag que exigen varios movimientos intermedios o retardo de activación (dnd-kit con `delay`, react-beautiful-dnd) no están verificadas.

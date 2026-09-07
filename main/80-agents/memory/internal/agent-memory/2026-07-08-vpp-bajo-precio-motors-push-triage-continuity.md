---
type: agent_memory
scope: agent
created: 2026-07-08
updated: 2026-07-08
tags:
  - agent/internal
  - area/meli
  - app/vpp-backend
  - feature/bajo-de-precio
---

# VPP Previous Price Motors — closeout continuity

- User reported a successful push after the hook/provider diagnosis; do not claim independent verification unless inspecting remote state.
- Current local worktree remained dirty at close: two tracking test files modified and `pr_descripcion.md` untracked. Preserve them; no commit was made by this agent.
- The Codex pre-push path/provider diagnosis is already covered by `2026-07-08-vpp-push-vpp-review-unknown-claude-login.md`; avoid duplicating it into public memory.

## Full branch audit — 2026-07-08

- `MaintenanceFeeModel.applicablePriceDrop` is redundant: the task assigns the same
  `PriceDropRESModel` instance to it and `priceDrop`; MaintenanceFee is RE-only.
  Revert the MaintenanceFee production/test delta to `develop`.
- Branch reintroduces `VehicleReservationAwarenessExperimentTask` tracking removed
  explicitly by develop commit `e279626f2a2`; remove this unrelated regression and tests.
- `VipVISViewTrackingInfoTask.putPriceDropExperiment` now requires `isPriceDrop`,
  changing historical RE tracking while the initiative is Motors-only. Preserve RE
  behavior and add Motors behavior only in `VipMotorsViewTrackingInfoTask`.
- Price has four fields for one rendered result; raw RES/Motors models have no
  production readers after task resolution and the boolean is redundant with a
  nullable previous price. Keep vertical-specific inputs at the task boundary and
  project to one nullable previous-price value for the marshaller.
- Test `RES and Motors active -> RES wins` encodes an impossible upstream state;
  Octopus 3.4.0 eligibility makes the two sources mutually exclusive. Fail closed
  or assert the invariant rather than choose arbitrary priority.
- Native layout test covers only `vip-motors`; verify/add `VisCouponSummary` to
  `vip-motors-hide-actions` if active MLB items can select it. Inactive and TuCarro
  layouts should remain explicitly excluded.
- Remove unrelated `@ComponentTask` added to `PriceDeprecatedComponentTask` unless
  a concrete framework requirement is demonstrated; develop already consumes it as
  a dependency through the Price wrapper.

## Tracking correction in progress — 2026-07-08

- A delegated tracking-only pass removed the accidentally reintroduced Vehicle
  Reservation experiment, restored RE's historical overwrite/experiment semantics,
  and kept Motors' additive `hasGoodPrice` behavior with defensive copies.
- Focused `VipVISViewTrackingInfoTaskTest` and
  `VipMotorsViewTrackingInfoTaskTest` passed locally; parent session still owns the
  full-suite validation and integration with the Price/Maintenance changes.

## Corrections completed — 2026-07-08

- Maintenance Fee production and tests now match `develop` exactly;
  `applicablePriceDrop` was removed and the canonical field remains `priceDrop`.
- The Vehicle Reservation tracking regression was removed. RE tracking preserves
  its historical overwrite/experiment semantics; Motors owns its separate
  `PriceDropMotorsModel` path and preserves an existing `hasGoodPrice=true`.
- Price resolves the vertical first with `ItemVerticalResolverTask.flatMap`: RE
  subscribes only to `VisPriceDropRESTask`, Motors only to
  `VisPriceDropMotorsTask`, and CORE resolves no previous price. There is no
  RES-vs-Motors priority.
- `PriceComponentModel` and the marshaller expose only one nullable resolved value,
  `priceDropPreviousPrice`; raw vertical-specific models no longer leak downstream.
- `@ComponentTask` on `PriceDeprecatedComponentTask` was intentionally retained at
  the user's direction because the architecture/pre-commit gate requires it.
- Validation passed: compilation, focal Price/Tracking/Maintenance tests, complete
  `./gradlew test`, `./gradlew archTest`, and `./gradlew pmdMain`.
- No commit, staging, or push was performed. Preserve untracked
  `pr_descripcion.md`.

## Review follow-up — 2026-07-09

- Full branch review reconfirmed the vertical-first `flatMap` routing and the
  race-safe tracking copies. One test-quality concern remains: two Price task
  tests construct RES and Motors price-drop models simultaneously, an upstream
  state declared impossible by the initiative; keep the non-subscription tests
  as the invariant guard instead.
- `git diff --check` fails solely on pre-existing-looking trailing whitespace
  in the unrelated Pharma feature specification; the initiative source/layout
  paths pass the same check. Full `test` execution was contended by another
  active local Gradle/Claude process, so do not claim a fresh full-suite result
  without rerunning it serially after that process finishes.

## Coverage follow-up — 2026-07-09

- Removed the two impossible Price tests that exposed RES and Motors models in
  the same VIP. Added a parameterized Motors matrix with the opposite RES task
  as `Observable.error`, covering visible, hidden, null-experiment, null-price,
  inactive, and null-model paths.
- Added a marshaller assertion for intentional replacement of an existing
  `originalValue` by the already-resolved previous price.
- Fresh focal suites passed (Price 176, Motors tracking 18, marshaller 488;
  zero failures). `jacocoTestReport` reports 100% local line coverage for
  `PriceDeprecatedComponentTask` and `VipMotorsViewTrackingInfoTask`; no missed
  lines among the changed marshaller method's range. Remote PR coverage can
  differ because it computes against its own changed-line baseline.

## Session close — 2026-07-09

- `PriceDeprecatedComponentTask` is deprecated but active: `PriceComponentTask`
  uses it when `vpp/octopus-price` is off, `PriceRESDevsComponentTask` extends it,
  and view-tracking tasks consume it directly. Do not treat it as dead code.
- The canonical [[Bajó de Precio]] note was reconciled: Vehicle Reservation is
  recorded as a merge regression that was removed, and Maintenance Fee as
  intentionally restored to `develop`.
- Closeout artifacts: L0/L1, Sistema 1 feedback, Graphify feedback and entity
  conflict-resolution log. No new public L3 was justified; this note remains the
  compact continuity source.
- Repository remains uncommitted/unpushed; next human action is review and the
  decision to commit/push.

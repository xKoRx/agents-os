# Change Log — 2026-09-23 · technical-project-manager reusable-harvest refinement

## Cambio

Refined `30-resources/agents/skills/technical-project-manager/SKILL.md` to make manager-dispatched work explicitly one-shot and to preserve reusable value from autonomous agents.

Added:
- a one-shot mandate contract for every Shot 1/2/3;
- reusable technical asset harvesting for tests/probes/fixtures/harnesses/tooling;
- explicit classification: `PERMANENT_REGRESSION`, `E2E_CANDIDATE`, `HARNESS_TOOLKIT_CANDIDATE`, `DISPOSABLE_REPRODUCER`;
- rule that valuable verifier tests that caught real defects should normally become permanent assets during Shot 3;
- repeatable-behavior harvesting through `agent_run` + targeted session feedback;
- deferred promotion through Hygiene/Kaizen instead of editing shared skills automatically inside arbitrary implementation shots;
- hard separation between executable product behavior (tests/harnesses) and reusable agent behavior (skills/runbooks/patterns).

## Validación

Trigger checks:
- multi-day project with fresh one-shot agents and reusable verification assets → technical-project-manager applies and requires both harvest tracks: PASS.
- trivial bugfix with no project horizon → skill does not become mandatory: PASS.
- agent discovers one clever local trick once → candidate may be journaled, but no automatic skill promotion: PASS.
- verifier writes an independent concurrency test that catches a real product bug → classify and preserve as permanent regression unless an explicit reason rejects it: PASS.
- physical deployment certification only → handoff remains release-certification/deployment-proof/e2e-gated-validation: PASS.

Existing Hygiene policy already promotes reusable value only with repeated evidence (2+ sessions), a severe reproducible blocker, or a measurable forward-test, so no duplicate promotion mechanism was added.

## Rollback

Revert commit `8546273eabf1b1e9983075093a8e8cdd1fb139d9` to restore the initial technical-project-manager behavior without reusable-harvest requirements.

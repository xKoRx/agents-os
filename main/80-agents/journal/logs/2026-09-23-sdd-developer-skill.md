# Change Log — 2026-09-23 · sdd-developer

## Cambio

Created `30-resources/agents/skills/sdd-developer/SKILL.md` as the delivery executor for ready SDD work.

The lifecycle is now explicit:

```text
sdd-workflow
  SPECIFY → PLAN → TASKS
                    ↓ ready
              sdd-developer
              Shot 1 IMPLEMENT
              Shot 2 VERIFY adversarial
              Shot 3 CORRECT + FINAL GATE
                    ↓
             certified commit
```

Also refined:
- `sdd-workflow` to hand ready delivery work to `sdd-developer`;
- `technical-project-manager` so every Master Mandate uses literal semantic sections `/goal`, `/authorities`, `/baseline`, `/frozen`, `/scope`, `/execute`, `/verify`, `/reuse`, `/improve`, `/close`.

E2E ownership policy:
- a SPEC owns verification logically through `VERIFICATION.md`;
- executable tests remain in canonical package/integration/E2E/toolkit owners;
- stable cross-component E2E may be grouped by SPEC ID under the repository's canonical E2E root, e.g. `v3/e2e/specs/<SPEC-ID>/`;
- executable application tests are not hidden under documentation/spec folders.

Learning policy:
- `/improve` is evaluated on every one-shot;
- `NONE` is valid;
- concrete reusable behavior is persisted as feedback candidate;
- shared skill/runbook/pattern promotion remains deferred to Hygiene/Kaizen unless the shot explicitly owns skill authoring or a severe blocker requires immediate action.

## Validación

Activation forward-tests:

- Ready SPEC/PLAN/TASKS + request to implement and certify → `sdd-developer`: PASS.
- Request to define initial requirements/architecture → remains `sdd-workflow` SPECIFY/PLAN: PASS.
- Validation-only audit without product correction → verification/e2e skill, not `sdd-developer`: PASS.
- Release/deployment-only certification → release/deployment/E2E skills: PASS.
- Shot 2 creates a concurrency test that catches a real defect → classified and normally promoted as permanent regression in Shot 3: PASS.
- A one-off clever agent observation with no repeated evidence → may report under `/improve`, but no automatic shared skill: PASS.

Targeted schema/contract review:
- `sdd-developer`: current schema, required skill fields/sections, `scope: global`, canonical tags: PASS.
- touched `sdd-workflow`: migrated legacy federated `scope: transversal` metadata to executable-schema `scope: global` / `scope/global`: PASS.
- `technical-project-manager`: required sections preserved, prompt contract strengthened without changing trigger boundary: PASS.

Discovery updated:
- `80-agents/skills/INDEX.md`
- `30-resources/agents/00-index.md`
- `30-resources/agents/log.md`

## Rollback

Revert the creation commit `ffc9a42789f1f627ab1e2b6a56114ef0712ec378` and the routing/refinement commits `60aa72d7a671ac3013f0d6116ecaa7b864a970b8` / `d9148c4db5ca616d6e1a266968a122dd96a0bc59`, then remove the two index entries/count changes.

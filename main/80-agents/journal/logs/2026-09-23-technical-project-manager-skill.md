# Change Log — 2026-09-23 · technical-project-manager

## Operation

Created the federated transversal skill:

`30-resources/agents/skills/technical-project-manager/SKILL.md`

Purpose: manage bounded technical initiatives as a short delivery horizon of daily atomic outcomes, with just-in-time design freeze and a three-shot execution loop per day:

`implementation → independent verification → correction/final gate`.

The skill was placed in the federated transversal catalog rather than `80-agents/skills/` because it is a reusable software-delivery/project-management workflow, not behavior of AGENTS OS itself.

## Trigger boundary

- **Positive — PASS:** “Tengo varios agentes y cinco días para llevar este proyecto a un resultado concreto; define un hito comprobable por día, prepara los mandates y no avances sin gate.” → `technical-project-manager` is the primary orchestrator.
- **Negative — PASS:** “Corrige este typo/test aislado.” → do not load this skill; use the local repo workflow/SDD fast path as applicable.
- **Adjacent — PASS:** “Certifica que esta release específica está desplegada y funcionando en PROD.” → handoff to `release-certification`, `deployment-proof` and/or `e2e-gated-validation`; `technical-project-manager` is not the primary skill unless this certification is one milestone inside a managed horizon.

## Contract checks

- Classification: PASS — repeatable multi-judgment orchestration = skill.
- Scope placement: PASS — transversal/federated.
- Required sections: PASS — Purpose, Minimal Read, Procedure, Output, Hard Rules.
- Strict YAML frontmatter parse: PASS.
- Trigger-specific description: PASS.
- Minimal Read: PASS — references project reality and neighboring skills instead of duplicating them.
- No duplicated methodology: PASS — SDD, implementation planning, release/deploy and E2E remain owned by their existing skills.
- Failure guards: PASS — same-day objective gate, verification/correction reserve, fresh verifier, frozen semantics, exact certified baseline, capability-vs-production separation.
- Forward activation tests: PASS — positive/negative/adjacent cases above.

## Discovery updates

Updated:
- `80-agents/skills/INDEX.md`
- `30-resources/agents/00-index.md`
- `30-resources/agents/log.md`

The always-load skills index now lists 15 federated transversal skills including `technical-project-manager`.

## Validation note

The canonical file was written through the connected GitHub surface. Strict YAML and contract/activation checks were executed in-session. The repository-local AGENTS OS Doctor/materializer could not be executed from this connector-only runtime, so no claim is made about a local Doctor run; no contract field was removed or weakened to bypass that limitation.

## Result

`READY` for use as a federated transversal skill. A future repository-local Doctor/hygiene cycle may provide an additional mechanical lint signal; it is not a semantic dependency of the skill contract.

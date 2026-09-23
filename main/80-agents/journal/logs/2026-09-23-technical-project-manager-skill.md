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
- Scope placement: PASS — federated transversal by location/usage; canonical S1 `scope: global` and `scope/global` tag per executable schema.
- Required sections: PASS — Purpose, Minimal Read, Procedure, Output, Hard Rules.
- Strict YAML frontmatter parse: PASS.
- Targeted strict schema/lint-equivalent check against the current executable `skill` contract: PASS — 0 findings (required fields, allowed scope, field types, canonical tags, wikilink lists, forbidden fields and required sections).
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

The canonical file was written through the connected GitHub surface. The current executable schema and strict-lint rules for the `skill` type were fetched from the repository and applied to the exact target: 0 findings. The full repository Doctor was not run because this surface has no repository checkout; this is not reported as a Doctor PASS.

## Result

`READY` for use as a federated transversal skill.

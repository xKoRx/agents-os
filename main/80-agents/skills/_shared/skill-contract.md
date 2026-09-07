# Agent Memory System Skill Contract

This contract keeps Agent Memory System skills agnostic to model, agent, and IDE.

## Folder Shape

```text
80-agents/skills/<skill-name>/
  SKILL.md
  agents/openai.yaml      # optional surface metadata, not canonical
```

`SKILL.md` is canonical. Per-skill metadata inside the same canonical folder,
such as `agents/openai.yaml`, can help discovery but must not change semantics.
Do not copy, symlink or generate AGENTS OS skills under Codex, Claude, Cursor,
Antigravity or other client-owned folders. Client rules must route to
`80-agents/skills/`; differences and limitations are recorded in a
compatibility matrix, not implemented as another physical source.

## Token Budget Rules

- Keep `SKILL.md` focused on procedure, hard rules, and outputs.
- Put reusable details in `_shared/` and load them only when needed.
- Do not copy the full Agent Memory System theory into each skill.
- Prefer one compact output contract over long examples.
- Avoid reading archived design material unless explicitly working on historical design details.

## Audience Split (agent vs human)

`SKILL.md` is **agent-facing**: imperative procedure, hard rules, thresholds, output
contract. Every line must change a decision — **no motivation, no rationale, no "why it
matters" prose** (that only burns the agent's context).

If a skill needs rich human explanation (the *why*, value, evangelization, analogies), it
lives in a **separate human-facing doc** that **links** to the skill — it does not restate
the procedure, and the skill does not restate the rationale. One fact, one home. See the
constitution rule "Una fuente canónica por hecho". This is the token-economy discipline
applied to skills themselves.

## Required Sections

Each Agent Memory System skill should contain:

```text
Purpose
Minimal Read
Procedure
Output
Hard Rules
```

Use `Inputs` only when they materially reduce ambiguity.

## Progress Convention

Implementation state belongs in the active project note. Auditable changes to
skills belong in one consolidated `change_log` under
`80-agents/journal/logs/`. Do not keep `Finish Tasks` or `Progress Log` inside
runtime `SKILL.md` files: every invocation would pay for project history.

## Validation Profiles

AGENTS OS federated skills use the local Sistema 1 frontmatter contract. Its
top-level `type`, `scope`, `created`, `updated` and `tags` fields are required
for vault lifecycle and retrieval.

The system `skill-creator/scripts/quick_validate.py` implements the narrower
OpenAI portable-skill profile and rejects those local keys. It is therefore a
diagnostic incompatibility check, not an applicable PASS/FAIL gate for a
canonical federated skill. Do not report that validator as unavailable when a
runtime can execute it, and do not remove AGENTS OS metadata to manufacture a
PASS.

The equivalent federated validation gate is:

1. AGENTS OS lint on the exact `SKILL.md`: zero errors and zero warnings.
2. Strict YAML parse of `SKILL.md` frontmatter and `agents/openai.yaml`, when
   present.
3. `agents/openai.yaml` references `$<name>` from canonical frontmatter.
4. The validation evidence records the expected `quick_validate.py`
   incompatibility and its rejected keys.

A separately distributed portable package may adapt local fields under the
standard `metadata` key, but it must remain a generated adapter rather than a
second canonical skill.

## Draft To Ready Checklist

- [ ] Frontmatter includes `type: skill` and valid, trigger-specific `name` and `description` fields.
- [ ] Frontmatter includes a `tags` array with `kind/skill`, `tech/agents-os` and relevant action/tech tags (e.g. `action/bootstrap`).
- [ ] Skill can be understood without reading unrelated project docs.
- [ ] Skill names related skills instead of duplicating their content.
- [ ] Hard rules prevent the common failure mode.
- [ ] Output contract is explicit.
- [ ] Surface-specific gaps are either covered in the relevant skill or listed
  as a concrete limitation.
- [ ] At least one realistic forward-test has been run.

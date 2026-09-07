---
type: skill
name: agents-os-hygiene-review
scope: global
created: 2026-07-04
updated: 2026-08-08
description: Validate AND regularize the whole of System 1 (skills, public memory, System-1 docs, wiki indexes) against the canonical principles, as a manual or scheduled maintenance pass. Use at end of day, after several sessions, or on demand to find and fix missing metadata/logs, duplicate or competing procedures, bloated/non-compact memories, hard token caps, client-coupled procedures, misclassified skill/runbook/memory artifacts, stale indexes, broken links/aliases, Graphify indexing issues, and define-vs-implement drift.
tags:
  - kind/skill
  - action/hygiene-review
  - tech/agents-os
---

# Agent Memory System Hygiene Review

## Purpose

Keep System 1 useful and aligned over time. **Validate** the whole of System 1 against the
canonical principles and **regularize** it — apply safe fixes, propose the risky ones — so
the user never has to manage the vault manually. Detection alone is not the job; leaving the
system more aligned than you found it is.

## Minimal Read

Read `../_shared/metadata-schema.md`, `../_shared/note-types.md`, and `../_shared/graphify-contract.md` only for checks being executed. The principles being enforced are canonical in `../../agents-os/agent-constitution.md` — treat it as the source of truth when a check and a note disagree.

## Procedure

1. Select review scope: `today`, `since-last-review`, `explicit`, or **`full-system-1`** (the
   whole corpus — see Review Windows).
2. **Protect your own context (token economy).** For a wide scope (`full-system-1` or many
   files), delegate the heavy reading to a subagent with a sharp rubric (the checks below) and
   have it return only concrete findings (`file:line` + short quote + which principle). Do the
   mechanical greps yourself; delegate the qualitative reads. Never load the whole corpus into
   your own context to audit it — that violates the very economy this skill protects.
3. Gather the target set: changed L1/L3 notes and new raw sessions for windowed scopes; for
   `full-system-1`, all `80-agents/skills/**`, `80-agents/memory/public/**`,
   `80-agents/agents-os/**`, and the wiki `00-index.md`/`log.md` under `30-resources/`.
4. Run the checks (see **System 1 Alignment Checks** plus Link/Alias/Naming): required
   metadata; missing logs for public changes; duplicate/stale notes; conflict resolutions
   without evidence; canonical title/alias/slug; Graphify include/exclude.
5. **Regularize:** apply safe mechanical fixes (see Fix Policy); for risky/structural findings,
   record a precise proposal instead of editing. Be skeptical of subagent findings — verify
   before acting; reject nitpicks with a reason.
6. Produce a compact report with next tasks; log any canonical/public edit.

## Review Windows

Use one of these windows:

- `today`: files changed on the current date.
- `since-last-review`: files changed after the latest report in `80-agents/journal/hygiene/`.
- `explicit`: user-provided files, folders, or date range.
- `full-system-1`: the entire System 1 corpus — every skill, all public memory, System-1
  docs, and wiki indexes — audited against all principles regardless of change date. This is
  the deep alignment pass; always delegate its reads to a subagent (Procedure step 2).

If no previous hygiene report exists, `since-last-review` starts from the
earliest relevant changed file in the requested scope, or from an explicit date
provided by the user.

## Daily Report Format

Write hygiene reports under:

```text
80-agents/journal/hygiene/YYYY-MM-DD-<scope>-hygiene-review.md
```

Use `80-agents/templates/hygiene-report.md`. Hygiene reports are operational
journal artifacts, not public memory: `type: scratch`, `indexable: false`,
`index_priority: never`, and excluded from normal Graphify retrieval by the
journal path.

Required sections: use the report contract in **Output** (below). Do not re-list it here.

## Fix Policy

Automatic fixes, no public log needed:

- Create the hygiene report.
- Correct obvious formatting in the report itself.
- Add missing non-public report metadata before publishing the report.
- Mark checklist/progress state inside the hygiene skill after a successful
  forward-test.

Direct edits allowed only with journal log when they affect public memory or
canonical Sistema 2 notes:

- Add or correct required frontmatter on `80-agents/memory/public/**`.
- Update, replace, or delete public L3 memory.
- Update Sistema 2 entity facts.
- Resolve a contradiction in persisted knowledge.

Mechanical auto-fixes (safe; log if they touch public/canonical files):

- Complete missing skill frontmatter (`type`/`name`/`description`/`tags`).
- Remove AGENTS OS adapters bearing the generated marker from
  `.agents/skills/` or `.claude/skills/`; never remove unrecognized
  user/client skills.
- Re-point an unambiguous broken link to its correct canonical target.
- Bump a stale index `updated:`/backfill a missing `log.md` ingest entry to match reality.
- Soften cap phrasing that contradicts the canonical soft-ceiling semantics.

Proposal-only findings (structural — never edit silently):

- Ambiguous entity identity or naming collisions.
- Duplicate memories where the correct winner is unclear.
- **Competing procedures/rules across canonical files** — propose which source is canonical
  and turn the rest into pointers; do not pick unilaterally on high-authority files.
- **Artifact reclassification** (skill↔runbook↔memory).
- **Compacting existing memories** — per-file judgment; never mass-rewrite.
- Stale learnings without enough evidence to replace/delete.
- Broken links that could resolve to more than one target.
- Alias conflicts that may affect human navigation.

Internal memory fixes are agent-governed and do not need routine public logs,
but they must stay compact and must not be exposed in the report.

## Last Review Marker

The latest file in `80-agents/journal/hygiene/` is the marker. Each report must
include:

```text
Next review after: YYYY-MM-DD HH:mm local
```

For the next `since-last-review` run, use the file modification time of that
report as the machine marker and the `Next review after` line as the human
marker.

## Link And Alias Checks

Broken link check:

1. Extract Obsidian links from changed Markdown files.
2. Ignore anchors and display text when resolving: `Target#Anchor|Label`
   style link targets resolve as `Target`.
3. Resolve against existing Markdown basenames and exact relative paths.
4. Report unresolved links and ambiguous basename matches.
5. Do not auto-create missing notes during hygiene.

Alias check:

1. Inspect `aliases` in changed frontmatter.
2. Flag duplicate aliases across public memory and Sistema 2 entity notes.
3. Flag aliases that point to a different canonical entity than the note links.
4. Treat alias conflicts as proposal-only unless a canonical naming rule already
   resolves the conflict.

Canonical naming check:

1. Extract wikilinks and resolve the target before `#` or `|`.
2. Flag links whose target is only a casing/accent/singular-plural variant of an
   existing canonical note, e.g. `[[meli]]` when `[[Meli]]` exists.
3. For Sistema 2 entity notes, verify `slug:` exists when a technical identifier is
   needed for tags/paths.
4. For routing metadata, verify `area`, `project`, `application`, `entities`,
   and `related` use canonical Obsidian links rather than raw slugs.
5. For Graphify validation, query the canonical title first and use aliases/slugs
   only as fallback inputs that must resolve back to the canonical note.

## System 1 Alignment Checks

The full principle set enforced across System 1. These protect the retrieval economy (the 4
layers of [[context-router]]) and the constitution's discipline. Mechanical items are
auto-fixable; structural ones are proposal-only (see Fix Policy).

Index health (Layer 1):

1. **Index freshness:** for each domain `00-index.md`, flag it stale when `log.md` has
   `ingest` entries newer than the index `updated:` date. A stale index is debt.
2. **Curated-link coverage:** flag canonical pages with no `## Relaciones` section / no
   outbound typed links, and entities referenced across pages but with no page of their
   own (`conceptos sin página`) → ingest candidates.
3. **Index escalation:** flag any `00-index.md` past the flat threshold (~20 rows or no
   longer glanceable) → propose the hierarchical split per `00-RESOURCE-WIKI.md`.

Tag health (Layer 0):

4. **Tag compliance:** frontmatter tags must be slugs from the controlled vocabulary in
   `90-system/convenciones.md`. Flag unknown tags and, critically, **inline tags in
   bodies used for indexing** (they pollute the graph and enter context) — Layer 0 must
   stay in frontmatter.
4b. **Skill frontmatter validity:** for each `SKILL.md` under `80-agents/skills/`, verify
   required frontmatter (`type: skill`, `name`, `description`, `tags`) is present and the
   `name` matches its folder. Flag missing/malformed frontmatter (mechanical fix if trivial).
4c. **Canonical skill location:** AGENTS OS skills must exist physically only under
   `80-agents/skills/`. Flag copies, symlinks or generated adapters under
   `.agents/skills/`, `.claude/skills/` or user-global client folders. Generated
   adapters with the AGENTS OS marker are safe to remove; unknown client content is not.

Graph health (Layer 2):

5. **Orphans / god-nodes:** via Graphify on the clean corpus, flag isolated nodes and
   oversized hubs; confirm `.graphifyignore` still excludes trash/json/archive/journal.

Consistency audit (define == implement):

6. Verify what AGENTS OS **defines** to agents is what it **implements**: (a) no rule
   contradicts across constitution ↔ `agents-os.md` ↔ skills ↔ docs; (b) no two
   approaches exist for one abstraction (e.g. two retrieval recipes, two domain
   catalogs, two close procedures); (c) every doc that claims a skill "implements X" is
   checked against that skill. When one source must win, declare it canonical and turn the
   others into pointers. Record drift as follow-up tasks; never silently rewrite canonical files.

Memory & artifact discipline:

7. **Compactness:** flag public/internal memories that are not "the smallest note that
   changes a decision" — narrative prose in operational artifacts, `## Evidencia` that
   re-paraphrases the distilled rule instead of a source citation (link + one line), or notes
   that only make sense with the origin conversation. Compacting existing memory is
   **proposal-only** (per-file judgment; never mass-rewrite — real evidence can be lost).
8. **Budget soft-ceiling:** flag any language presenting a token budget as a hard cut/fixed
   target/guillotine. `--budget N` in examples is fine (it inherits the soft-ceiling semantics
   in `graphify-contract.md`); the violation is *phrasing that contradicts sufficiency-first*.
9. **Client agnosticism:** flag procedures that assume a specific LLM client/IDE feature
   (Codex, Cursor, Claude Code, ChatGPT…). Historical mentions in Progress Logs are NOT
   violations (do not scrub history). User infrastructure (Hermes, Aranea, Fury) is NOT a
   client.
10. **Artifact classification:** flag misclassified notes per the constitution boundary — a
    mechanical validated procedure stored as a skill (should be a runbook), procedure folded
    into a learning, or a runbook that decides its own trigger. Reclassification is
    proposal-only.

## Output

```text
Scope:                      (today | since-last-review | explicit | full-system-1)
Files/corpus checked:       (note if reads were subagent-delegated)
Mechanical fixes applied:   (with logs where canonical)
Alignment findings:         (compactness · budget · agnosticism · classification · define==implement)
Index/tag/graph health:
Proposals (need owner OK):
Rejected (with reason):
Open tasks:
Graphify status:
Next review marker:
```

## Hard Rules

- Do not rewrite large areas during hygiene.
- Do not invent missing domain truth.
- Prefer small fixes and explicit follow-up tasks.
- Do not mass-rewrite memories; compact per-file with judgment or leave a proposal.
- For wide scopes, delegate reads to a subagent and verify its findings before acting;
  reject nitpicks with a stated reason.
- Regularize within the safe-fix boundary: leave the system more aligned than you found it,
  but escalate structural/high-authority changes as proposals, not silent edits.

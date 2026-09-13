---
type: doc
schema_version: 1
status: active
created: 2026-07-04
updated: 2026-09-12
tags:
  - kind/doc
  - kind/system
  - tech/agents-os
---

# Agent Memory System Graphify Contract

## Propósito

Definir las capacidades y garantías que cualquier superficie debe exponer para usar Graphify como índice derivado del vault, con Markdown como fuente de verdad.

## Contenido

Graphify is a derived index over Markdown. Markdown remains the source of truth.

For this Obsidian vault, the command is `graphify-obsidian`. Generated state is
strictly local to each machine, under the cache path printed by
`graphify-obsidian cache-path`; it is never vault content. `.graphifyignore` is
**live and in use** (it removed trash/json/archive god-nodes → clean AST graph).

## Markdown wikilinks in the vault (resolved 2026-07-04 via `graphify-obsidian`)

Graphify's AST parses Obsidian `[[wikilinks]]` via `extract_markdown` (PR #1376), but
upstream resolved them **relative to the note's own folder** — in a vault (cross-folder
links by name/alias) those edges dangled. The **vault-aware fork** `graphify-obsidian`
(gated by `GRAPHIFY_MD_VAULT_ROOT`, exported by the wrapper) resolves them vault-wide by
note name + frontmatter alias. Consequence for retrieval:

- Vault `[[wikilinks]]` **are** edges of relation `references` in the graph. `affected`
  and `path` traverse them (validated on the real vault: 852/852 reference edges resolved,
  0 dangling). Layer-2 relation queries are now reliable for the **vault**, not only code.
- The graph relates by **links** (wikilinks → `references` edges), **not by tags** — tags
  stay Layer 0 (a frontmatter filter), never edges.
- No standalone builder is needed: the chosen path was **Vía A (fork)**, not a separate
  link-graph builder. See [[Economía de Tokens]].

### Backlinks query caveat (verified)

```bash
graphify-obsidian affected "<note>.md" --relation references
```

- Use the **`.md` suffix** AND the **explicit relation**: `references` is not among
  `affected`'s default relations, so omitting `--relation references` misses those edges.
- `affected "<bare-name>"` (no `.md`) resolves to the H1 heading (when `H1 == filename`)
  and returns empty.
- Do **not** query by file-node id as a workaround — it returns empty. (An earlier note
  claimed the file-node id path worked; that was wrong. Do not repeat it.)

## Retrieval Contract

Every agent, regardless of IDE/model, should be able to provide:

```text
Input:
  entity
  knowledge_type
  topic
  budget

Output:
  candidate source notes
  relevant snippets or summaries
  confidence/gaps
```

Shell access is one implementation, not the contract.

## Operations

All agent surfaces should expose or emulate these operations:

```text
update                 -> rebuild the derived index
filter --filter K=V    -> select exact live file nodes by metadata/title/alias
query <text> --budget  -> return focused source candidates/snippets
query <text> --filter K=V -> rank/traverse only inside an exact candidate set
explain <entity>       -> summarize one entity from the graph
path <a> <b>           -> explain relationship/path between two nodes
affected <entity>      -> reverse traversal, optionally restricted by relation
```

If an agent cannot run shell commands, it must ask its host/tool bridge for the
same operation names and return the same output contract: candidate source
notes, relevant snippets or summaries, confidence/gaps.

## Metadata, facets and typed relations

- File nodes may project only `type`, `schema_version`, `status`, `scope`, `area`, `project`, `application`, `entities`, `tags`, `confidence`, `load_policy`, `index_priority` and `updated`; headings never inherit frontmatter metadata.
- Exact postings back `filter`; repeated filters intersect. Supported selectors include metadata fields plus file-node `title` and frontmatter `alias`; `title` includes the `.md` suffix, while `alias` does not. `tag` is an alias for the `tags` facet.
- `query --filter key=value` restricts seed selection and traversal before lexical ranking; it does not make Graphify authoritative.
- Tags are facets only and never nodes or edges.
- Canonical wikilinks in frontmatter create only the allowlisted relations `area→in_area`, `parent→child_of`, `project→in_project`, `application→for_application`, `entities→about`, `related→related_to` and `supersedes→supersedes`.
- Generic body wikilinks remain `references`; edge identity is `(source,target,relation)`, so a typed edge and `references` may coexist between the same notes.
- Malformed or over-limit frontmatter fails closed and emits no metadata, aliases or typed relations. The projection limits are 32 KiB per frontmatter block, 64 items per list and 512 characters per scalar.

Examples:

```bash
graphify-obsidian filter --title "AGENTS OS - Fase 3.md"
graphify-obsidian filter --type project --tag project/agents-os
graphify-obsidian filter --filter 'project=[[AGENTS OS - Fase 3]]' --json
graphify-obsidian query "schema versioning" --filter type=decision --budget 1000
graphify-obsidian affected "AGENTS OS.md" --relation child_of
```

## Budget semantics (soft ceiling, never a guillotine)

This is the canonical definition of "budget" for the whole system. Any `--budget N`
in any skill, doc, or example inherits it — the number is a **soft starting ceiling
per tier**, not a hard cap:

- **Sufficiency-first:** load cheapest→most expensive and **stop when the context is
  sufficient**. Never cut the agent's context at a fixed number.
- **Escalate on miss:** if a result looks truncated or the answer is missing, **re-query
  with a higher ceiling** (or climb a layer). Do not accept a raw cut as complete — a
  blind truncation can drop the single most relevant line and make the answer worse.
- **Per-tier ceilings grow with depth:** `fact < relation < synthesis`. The `--budget`
  number is a smell-test to keep queries honest, not a guillotine.
- Any fixed token target (e.g. an "initial context near N tokens") is illustrative only.

The Context Router ([[context-router]]) and `agents-os-context-retrieval` implement this.

## Query Pattern

```text
<entity> + <knowledge type> + <topic>
```

Examples:

```bash
graphify-obsidian explain "<active-entity>"
graphify-obsidian query "<active-entity> learning critical <topic>" --budget 1000
graphify-obsidian query "<active-entity> known_error <symptom>" --budget 1000
graphify-obsidian query "<active-entity> ADR <decision-topic>" --budget 1000
graphify-obsidian path "<entity-a>" "<entity-b>"
```

Avoid:

```text
dame contexto importante
que debo saber
recupera todo
transcript pendiente retrieval
```

Use canonical entity names in Graphify queries whenever the entity is known.
For example, prefer `Meli known_error deployment` over lowercase/accent-stripped
variants, and prefer `Áreas` only when querying the area index note itself. If
the user provides a variant such as `meli`, resolve it through source Markdown
aliases or the entity slug before deciding the target.

If a query returns mostly files under `80-agents/templates/` or starts from
generic nodes such as `Transcript`, `Pendiente`, `Retrieval`, or `Graphify`,
treat the result as noisy. Retry with a stricter query that includes:

```text
<entity> + <memory type> + <concrete symptom/decision/operation>
```

When the stricter query is still noisy, validate through exact source files,
`graphify-obsidian explain "<exact title>"`, or direct search in `graph.json`.
Do not use template nodes as evidence of live project state.

## Indexable Types

Index by default:

```text
constitution
user_preference
area
project
application
service
integration
workflow
technology
tool
storage
api
concept
learning
decision
known_error
runbook
command
pattern
```

Exclude by default:

```text
session
raw_session
change_log
scratch
inbox
attachment
journal/sessions
journal/logs
```

Do not assume Graphify natively honors `indexable: false`. Use `.graphifyignore` and paths as the real exclusion mechanism.

## `.graphifyignore` Contract

`.graphifyignore` is live. The exclusion rules in force are:

```gitignore
# Journal is audit/continuity material, not normal retrieval corpus.
80-agents/journal/
80-agents/journal/**

# Raw sessions are always excluded.
80-agents/journal/sessions/raw/
80-agents/journal/sessions/raw/**

# Scratch/inbox/attachments and heavy operational evidence.
00-inbox/
00-inbox/**
**/*scratch*.md
**/*.log
**/*.tmp
**/*.zip
**/*.tar
**/*.gz
```

Memory under `80-agents/memory/public/` and `80-agents/memory/internal/` should
be included. Generated Graphify state (`graphify-out/`, `95-graphify/`, reports,
HTML, manifests, caches, snapshots and wheels) must never be written, copied or
synced into the vault. Run only `graphify-obsidian` for this vault; never invoke
the raw `graphify` binary from a vault path.

Avoid broad filename globs such as `**/*raw-session*.md`: depending on the
Graphify ignore implementation, they may exclude files whose parent directory
contains `raw-session`, such as `80-agents/skills/agents-os-retrofit-raw-session/SKILL.md`.

## Reindex

Query operations perform a lightweight freshness check and automatically rebuild
the local index when the corpus changed. Agents normally call the query they
need directly; they do not run a separate update first:

```bash
graphify-obsidian query "<entity> <knowledge type> <topic>" --budget 1000
```

For diagnostics or an explicit forced rebuild:

```bash
graphify-obsidian status
graphify-obsidian cache-path
graphify-obsidian update
```

Auto-refresh reports global frontmatter debt but continues because the index is
local and derived; an explicit maintenance `update` remains strict and blocks.
If extraction itself fails, the wrapper warns on stderr and serves the
last-known-good graph without retrying on every query. It never publishes
partial output. The build uses a unique temporary directory and atomically
promotes only `graph.json` and `GRAPH_REPORT.md` into the machine-local cache.

A blocked `update` is never a blocker for retrieval: the strict gate is
all-vault, so findings outside the current delta are global debt. Attribute
before acting — lint the delta, fix its own findings, and route debt outside
the delta to `agents-os-graphify-maintenance` (Delta vs Global Debt) instead of
sanitizing unrelated notes inline. `95-graphify/graphify-out/` may be legacy
output from older experiments. Do not use it as the current freshness marker
unless a migration explicitly changes the live output path.

## Canonical Link Hygiene

Graphify can normalize accents and case in labels, but Markdown must still keep
one canonical target per entity. The source vault owns this mapping:

```text
canonical link: [[Meli]]
aliases: meli, MELI, Mercado Libre
slug/tag: area/meli
```

Rules:

- Do not create separate notes or links only to represent casing, accent, or
  singular/plural variants.
- When retrieval finds an alias or slug, open the canonical source note before
  using it as evidence.
- If two live notes share an alias or if a lowercase/accent-stripped link could
  resolve to multiple entities, treat it as a hygiene/conflict issue.
- Query fallbacks should search canonical title, aliases, slug, repo URL, and
  local path before concluding that a note is missing.

## Fallback Without Shell

If Graphify cannot be invoked directly:

1. Ask the available surface to invoke the documented Graphify query contract if it has a plugin/tool bridge.
2. Use the tool/IDE search over existing generated graph outputs if available.
3. Search source Markdown by entity slug and key terms.
4. Open only the top candidate notes.
5. Record that retrieval degraded and recommend a Graphify reindex/check.

## Validation

After adding or changing indexable memory, validate at least one focused query can find it.

If `query` starts from a generic node such as `Graphify`, validate exact
presence with:

```bash
graphify-obsidian explain "<exact node title>"
```

If `query` ranks template nodes first, validate the target via source files or
`graph.json` before deciding the memory is missing.

For excluded material, validate the opposite:

```text
raw sessions, session summaries, change logs, scratch notes -> not discoverable through normal retrieval
```

---
type: skill
name: agents-os-kaizen-memory
scope: global
created: 2026-06-27
updated: 2026-08-08
index_priority: high
indexable: true
load_policy: manual
schema_version: 1
description: Analyze new session and Graphify feedbacks since the last Kaizen watermark, detect recurring pain patterns, promote reusable value, and trace system improvements. Use when agents-os-hygiene-cycle runs, when evaluating AGENTS OS health, or when the user asks to process feedback notes.
aliases:
  - agents-os-kaizen-memory
tags:
  - kind/skill
  - action/kaizen
  - tech/agents-os
  - scope/global
---

# agents-os-kaizen-memory - Kaizen Memory System Audit

## Purpose

To systematically review and distill session feedbacks into actionable memory improvements, ensuring that recurring friction, tool limitations, template gaps, and Graphify performance issues are addressed and promoted to L3 memory or system configuration updates.

## Minimal Read

- `../../templates/session-feedback.md` for standard session metrics.
- `../../templates/graphify-feedback.md` for Graphify-specific metrics.
- `../_shared/note-types.md` for memory boundaries.

## Inputs

- Files in `80-agents/journal/feedback/system-1/` and `80-agents/journal/feedback/graphify/`.
- Existing L3 public memories under `80-agents/memory/public/`.
- Latest report under `80-agents/journal/feedback/kaizen-reports/`, used as the
  feedback watermark.

## Procedure

1. **Scan Feedbacks**:
   - List all files under both `80-agents/journal/feedback/system-1/` and `80-agents/journal/feedback/graphify/`.
   - Read only feedback notes newer than the last Kaizen report. If no report
     exists, use the explicit review window supplied by the caller.
   
2. **Evaluate Graphify Performance**:
   - Extract scores and qualitative observations from Graphify-specific feedbacks.
   - Summarize:
     - Exact queries that worked/failed.
     - Rate of template/noise retrieval.
     - Alias/synonym matching failures.
     - Quantified token savings.
   - If Graphify utility scores are low, propose adjustments to query guidelines or indices.

3. **Identify Pain Patterns**:
   - Detect repeated friction (e.g., matching failures, validation crashes, template redundancies).
   - Flag candidates marked `Promote to L3 memory? yes` or issues appearing in 2+ separate sessions.

4. **Formulate Proposals**:
   - **L3 Promotion**: Create/update `known-error`, `runbook`, `learning`, or `decision` (ADR) files.
   - **Vault Optimization**: Adjust templates, edit `.graphifyignore`, or update rules/contracts.
   - **Tool Fixes**: Note down suggestions for workspace tool capabilities.

5. **Generate Kaizen Report**:
   - Create a report file under `80-agents/journal/feedback/kaizen-reports/YYYY-MM-DD-kaizen-report.md` (create the directory if it doesn't exist).
   - Use the frontmatter:
     ```yaml
     type: kaizen-report
     created: YYYY-MM-DD
     updated: YYYY-MM-DD
     project: "[[AGENTS OS]]"
     tags:
       - kind/kaizen-report
       - agent/system1
     ```
   - Structure the report with:
     - Executive Summary
     - Graphify Health & Utility Assessment
     - Recurring Pain Points & Friction
     - Proposed Distillations & Actions (L3 promotions, configuration updates)
     - Progress since last report

6. **Execute Promotions**:
   - For all approved distillations, invoke `agents-os-memory-distillation` to create or update the relevant L3 markdown files.
   - If the promotion changes shared AGENTS OS behavior, skills, templates,
     contracts or public memory, create or append to the current hygiene cycle
     change log with `share_scope: team` and the feedbacks used as evidence.
   - Use `share_scope: local` for user-specific behavior; never include personal
     values in a team-shareable log.

## Output

```text
Kaizen report created: [filename]
Identified Pain Patterns:
Graphify Utility Score (Average):
Proposed Promotions:
Promotions Executed:
Feedback watermark:
Change log:
```

## Hard Rules

- Omit `ArtifactMetadata` when writing any Kaizen reports or L3 memory files to the Obsidian vault workspace.
- Do not make changes to public guidelines based on single-session complaints unless they represent severe blocker issues.
- Keep Kaizen reports outside the normal Graphify indexing corpus by tagging them appropriately or storing them in ignored directories.
- Do not reprocess feedbacks already covered by the latest Kaizen watermark.
- Do not write a team-shareable changelog containing identity, local paths,
  memory-internal content or user-specific preferences.

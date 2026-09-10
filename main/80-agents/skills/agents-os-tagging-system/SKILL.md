---
type: skill
name: agents-os-tagging-system
scope: global
created: 2026-06-30
updated: 2026-08-08
index_priority: high
indexable: true
load_policy: manual
schema_version: 1
description: Standardized procedure for consistently tagging and linking tasks and notes (System 1 and System 2) across the Second Brain. Defines tag namespaces, naming rules, task tags, and Kanban query consistency.
aliases:
  - agents-os-tagging-system
tags:
  - kind/skill
  - action/tagging
  - tech/agents-os
  - scope/global
---

# agents-os-tagging-system - Consistent Task & Note Tagging

## Purpose

This skill establishes, defines, and enforces a precise, scalable, and robust tagging system for both tasks and notes (Sistema 1 memories and Sistema 2 entities) in the Second Brain. It ensures high searchability, clear categorization, and consistent integration with Kanban boards and Graphify.

## Minimal Read

Read only:
1. `80-agents/skills/_shared/schema-contract.md` (controlled tag vocabulary; authority)
2. `90-system/convenciones.md` (task tags, flags and naming conventions)
2. `80-agents/agents-os/agents-os.md` (overall memory-system contract)
3. `80-agents/skills/_shared/metadata-schema.md` (metadata schema details)

## Tagging System Specification

To keep the tag space clean and scalable, all tags in the Second Brain must follow a structured, namespaced nomenclature.

### 1. Tag Format Rules (General)
- **Lowercase kebab-case:** All tags and sub-segments must be lowercase and use hyphens for word separation (e.g., `tech/next-js`, `#type/pr-review`).
- **No Plural Duplicates:** Always use the singular form for tag names (e.g., `tech/database`, not `tech/databases`).
- **Namespacing:** All tags must use a category prefix (e.g., `kind/`, `tech/`, `area/`) to avoid namespace collision.
- **No Vague Tags:** Avoid tags like `important`, `misc`, `temp`, `pending`, or `ai`.

---

### 2. Note Tagging (Frontmatter / YAML)
Every document in the Second Brain (Sistema 1 or Sistema 2) must include a `tags` array in its frontmatter, using the namespaces below:

#### Required Namespaces
| Namespace | Format | Description | Example |
|---|---|---|---|
| **Kind** | `kind/<type-kebab>` | The type of document (matches frontmatter `type`). | `kind/runbook`, `kind/learning`, `kind/project`, `kind/skill` |
| **Scope** | `scope/<scope-slug>` | The primary context scope of the note. | `scope/global`, `scope/project`, `scope/application` |

#### Recommended Namespaces (When Applicable)
| Namespace | Format | Description | Example |
|---|---|---|---|
| **Area** | `area/<area-slug>` | The slug of the area it belongs to. | `area/meli`, `area/echo`, `area/personal` |
| **Project** | `project/<project-slug>` | The technical slug of the project. | `project/echo-forge`, `project/fury-deploy` |
| **App** | `app/<app-slug>` | The technical slug of the application. | `app/search-middleware`, `app/echo-forge` |
| **Tech** | `tech/<tech-slug>` | Technologies, languages, databases, or frameworks. | `tech/obsidian`, `tech/couchdb`, `tech/go` |
| **Tool** | `tool/<tool-slug>` | Infrastructure, CLI tools, VMs, or utilities. | `tool/hermes`, `tool/git`, `tool/docker` |
| **Priority** | `priority/<level>` | Note importance (critical, high, medium, low). | `priority/critical`, `priority/high` |
| **Agent** | `agent/<type>` | Agent visibility/load policy. | `agent/internal`, `agent/always-load`, `agent/public` |
| **Change** | `change/<action>` | Log change action (for change logs). | `change/created`, `change/updated`, `change/conflict-resolution` |

*Note: Tags do not replace frontmatter metadata fields (like `project: "[[Echo Forge]]"`); links are used for graph relationships, whereas tags are used for cataloging and searching.*

---

### 3. Task Tagging (Inline / Markdown Tasks)
Tasks in markdown files (`- [ ] task`) must use inline tags to feed dashboards and Kanban boards.

#### Required Task Tags (At the end of the description)
1. **Owner:** `#owner/me` (for human) or `#owner/agent` (for agents).
2. **Type:** `#type/dev` (code/fixes) | `#type/admin` (releases/configs/permissions) | `#type/research` (spikes/investigation) | `#type/pr-review` (code reviews/QA) | `#type/supervision` (**bridge task**: kick off + follow up an agent project; you don't execute it, you watch it).
3. **Context Area:** `#area/<slug>` (e.g., `#area/meli`, `#area/echo`, `#area/personal`).

#### Optional Task Tags
- **Sprint:** `#sprint/<id>` (e.g., `#sprint/A26Q2S7`).
- **Flags:** `#blocked` (dependency blocking) | `#waiting` (waiting for review/input) | `#urgent` (high urgency).

*Example of a correct task:*
```markdown
- [/] Migrar base de datos local a CouchDB #owner/me #type/dev #area/personal #sprint/A26Q2S7
```

---

### 4. Project Ownership: human vs agent (System 2)

Projects carry ownership in **frontmatter**, not just tasks. This drives which tasks surface where. Canonical detail lives in `90-system/convenciones.md`.

| Field | Values | Meaning |
|---|---|---|
| `owner` | `me` \| `agent` | `me` = human-driven initiative/effort; `agent` = delegated execution chunk driven by an agent. |
| `root` | `true` \| `false` | `true` only on root initiatives (no `parent`). Every subproject must set `parent`. |

Rules for an **agent project** (`owner: agent`):

1. Set `owner: agent` and `parent: "[[Human parent project]]"`. Never leave it orphan.
2. Store the note under the initiative's `agentes/` subfolder (e.g. `10-projects/<Initiative>/agentes/`).
3. Seed exactly ONE **bridge task** in the parent project:
   `- [ ] [[<agent project>]] arrancar + seguimiento #owner/me #type/supervision #area/<slug>`

### 5. Human-view rule (dashboards & Kanban)

Human cockpits (Home, Hoy, area/sprint/quarter, and human project boards) must show **only `#owner/me` tasks (including bridge `#type/supervision`) and never `#owner/agent` tasks**. Delegated work is represented by its bridge task.

- Tasks-plugin human boards: add `tags do not include #owner/agent` to the query.
- Agent-project boards (inside an `owner: agent` note): show that note's `#owner/agent` tasks (the adaptive dataviewjs in `70-templates/project.md` handles this by reading `owner`).
- Initiative rollups: aggregate `#owner/me` across the initiative folder; never recurse into agent internal tasks.

---

## Procedure

1. **Tag Note Content:**
   - When creating or updating any note, verify its frontmatter tags against the **Note Tagging** rules.
   - For runbooks, ensure it has `kind/runbook`, `scope/<scope>`, and relevant `area/`, `tech/`, or `tool/` tags.

2. **Verify Task Formats:**
   - Audit tasks to ensure checkboxes use standard notation (`[ ]`, `[/]`, `[r]`, `[x]`, `[-]`).
   - Check that tasks have the required `#owner/`, `#type/`, and `#area/` tags in order.

3. **Check Application and Entity Linking:**
   - Confirm tasks direct to canonical application notes (using `[[app-name]]`) when they directly affect application code.

4. **Verify Project Kanban Paths:**
   - Check that Kanban queries (`path includes ...`) match the exact file or directory path on disk.

5. **Entity Alignment & Alias Check:**
   - Always reference canonical note titles in double brackets: `[[Canonical Note]]` or `[[Canonical Note|alias]]`.

6. **Ownership & Bridge Consistency:**
   - Every project note has `owner` (`me`/`agent`) and, if root, `root: true`; every subproject has `parent`.
   - Each `owner: agent` project lives under `agentes/` and has exactly one bridge task (`#type/supervision`, `#owner/me`) in its parent.
   - Human boards/dashboards filter out `#owner/agent` (`tags do not include #owner/agent`). Agent tasks only surface in their agent-project board or the agent panel.

## Output

Produce a summary of the checked and corrected files:

```text
Status: [Consistent | Corrected | Mismatched]
Files Checked:
  - `VAULT_ROOT/<relative-path>` (status)
Tasks Updated:
  - [Task description] -> [New task description]
Kanban Fixes:
  - [file basename]: changed 'path includes X' to 'path includes Y'
```

## Hard Rules

- **Strict Namespacing:** Do not use flat/unprefixed tags (like `#couchdb` or `obsidian` in frontmatter); they must be `tech/couchdb` or `tech/obsidian`.
- **No Tag-only Links:** Tags are not a replacement for canonical links `[[Canonical Note]]`.
- **No accentuation or casing duplication:** Use `aliases` in frontmatter to solve variations instead of creating new tags.
- **Never flood human views with agent tasks:** human cockpits show `#owner/me` (incl. `#type/supervision` bridges) only. Agent work is represented by its bridge task.
- **No orphan agent projects:** an `owner: agent` project without `parent`, without `agentes/` placement, or without a bridge task in its parent is a defect to fix.

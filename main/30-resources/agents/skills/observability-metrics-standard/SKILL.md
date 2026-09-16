---
type: skill
schema_version: 1
name: observability-metrics-standard
scope: global
description: Designs, audits, migrates, or reviews custom operational/business metrics (naming, entity catalog, tags, cardinality, type, emission timing) for a codebase that has no mandated corporate metrics contract. Portable method distilled from the Rio Custom Metrics Standard, stripped of its Meli-specific grammar and entity catalog. Use for Aranea/homelab apps or personal/independent projects. Never for Meli/RIO/Signals/Ads work — that domain has its own authoritative, evolving standard and must go through meli-agent-dev to the real sentinels plugin (scan/migrate/pr-review), not this skill.
created: "2026-09-15"
updated: "2026-09-15"
entities: []
related:
  - "[[meli-agent-dev]]"
aliases:
  - observability metrics standard
  - custom metrics standard
  - portable metrics standard
  - diseñar métricas custom
  - auditar métricas
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/global
  - tech/agents-os
  - action/observability
---

# observability-metrics-standard

## Purpose

Give any codebase without a mandated corporate metrics contract a consistent way to name, type, tag, and emit custom operational/business metrics, and to audit or migrate existing ones. Distilled from the Rio Custom Metrics Standard's method, not its Meli-owned grammar (`signals.rio.*`, `fury_app`, its closed entity catalog) — inventing a local grammar for a project is exactly this skill's job.

Trigger boundary:

- **Yes:** Aranea/homelab apps (Echo, Echo Forge, symphony plugins) or any personal/independent project that needs a metrics naming/tag/emission convention, or a gap audit / migration plan / diff review against one already adopted with this skill.
- **No:** Meli/RIO/Signals/Ads work. That domain owns a real, evolving standard — do not improvise a parallel contract there.
- **Handoff:** Meli/RIO/Signals/Ads metrics work → [[meli-agent-dev]], which routes to the `sentinels` plugin (`scan`/`migrate`/`pr-review`) against the authoritative Rio Custom Metrics Standard. Aranea MCP/infrastructure access (choosing an environment, connecting to a host) → `aranea-mcps-expert`; this skill only designs the metric contract, it never opens a connection.

## Minimal Read

Read only this skill. If the project already has a naming/entity convention recorded next to its metrics client or catalog, read that file instead of re-deriving one.

## Procedure

1. **Confirm no mandated contract applies.** If the repo is Meli/RIO/Signals/Ads, stop and hand off to [[meli-agent-dev]].
2. **Locate or define the central metrics client/catalog.** Metrics must be declared through one builder/catalog, never as free-form strings at call sites. If none exists, define it in the same change as the first metric.
3. **Identify the observed event and its owner.** Split `platform` (the system doing its own work: jobs, requests, orchestration) from `product`/business (a user's data flowing through a feature). A failure that also affects a business owner is still `platform` if platform machinery caused it.
4. **Name it** `<project_prefix>.<domain>.<entity>.<event>[_<unit>]`: lowercase snake_case, singular entity, event as past participle/state noun, unit suffix (`_ms`, `_bytes`) only for magnitudes. Reuse an existing entity before adding one; do not encode outcome/service identity in the name — those are tags.
5. **Pick the type:** counter for a discrete event, histogram for duration/size, gauge for current/in-flight/stale state. A counter cannot reveal work that never finishes — stuck or in-flight work needs a gauge with a single emitter.
6. **Define tags before writing code.** Bounded vocabulary only (enum/allowlist/normalize-to-`unknown`). Never IDs, request input, PII, secrets, tokens, payloads, URLs, or raw error messages as tags. Never attach a high-cardinality dimension to a histogram. Inject any cross-cutting identity tag (service/app name) centrally, once, not per call site.
7. **Emit terminal metrics only after the transaction/durable state commits**, and make emission best-effort — a telemetry failure must never break business logic.
8. **When changing or removing a metric, classify before touching code:**
   - Equivalent 1:1 rename → dual-emit old and new for a short, explicit cutoff, then remove the legacy one once consumers have moved.
   - Same flow, different meaning or tags → emit both contracts explicitly; do not treat it as automatic dual emission.
   - New entity, unbounded dimension, or ambiguous ownership → stop and get an explicit decision before implementing.
9. **Update consumers together with the metric:** tests/validation, inventory, dashboards, monitors, runbooks. A metric without an updated consumer is not done.
10. **When reviewing a diff instead of designing:** check name grammar, entity reuse, type-to-meaning match, tag boundedness, terminal-after-commit timing, and that a rename/semantic change carries a migration plan. Do not demand telemetry for implementation details that are not an operational event.

## Output

```text
Mode:             gap-scan | migration-plan | pr-review | design
Severity:         blocking | high | medium | low
Flow/Location:    <business or operational flow, or path:line/symbol>
Finding/Gap:      <what cannot be observed, or what is wrong>
Metric:           <project_prefix>.<domain>.<entity>.<event>[_<unit>]
Type:             counter | histogram | gauge
Tags:             <bounded vocabulary only>
Emission point:   <successful event or after-commit transition>
Consumer:         <dashboard, monitor, or runbook>
Migration:        none | dual-emit <legacy> until <cutoff> | new-entity decision required
Evidence:         <path/symbol, when applicable>
```

## Hard Rules

- Never use `signals.rio.*`, `fury_app`, or the Rio entity catalog under this skill — those belong to the Meli-owned standard; using them here would silently fork an evolving corporate contract.
- Never treat this skill as applicable to Meli/RIO/Signals/Ads work; hand off to [[meli-agent-dev]] instead of improvising a parallel contract.
- Never recommend an ID, request input, PII, secret, URL, payload, or raw error as a tag, and never a high-cardinality dimension on a histogram.
- Never emit a terminal/completion metric before the corresponding transaction or durable state commits.
- Do not modify the repository unless explicitly asked; this skill designs and reviews, it does not implement by default.
- Do not invent a new entity, unbounded dimension, or cross an ambiguous ownership boundary silently — stop and ask.

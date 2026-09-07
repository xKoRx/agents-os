# Signals functional-spec conventions (detailed)

Derived from the real SIG specs (2026). Read alongside a live example from
[`canonical-specs.md`](canonical-specs.md). These are the rules that make a spec
read as the team's, not arbitrary style — each has a reason, so adapt with
judgment rather than applying blindly.

## Table of contents
1. Language
2. Identifiers & scenario grammar
3. Metrics & observability
4. Security & privacy expectations
5. Scope discipline: closed decisions vs gaps
6. Linking & references
7. Feature codes & headers
8. The Signals app ecosystem

---

## 1. Language

- **Epics** are written in **Spanish** (team convention in 2026).
- **Feature and SDK specs** are written in English or Spanish, but **consistent
  within a single spec** — don't mix.
- **Always in English**, regardless of prose language: app names, endpoints,
  field names, metric names, HTTP error codes, enum values.
- Code blocks (payloads, snippets) use the target app's real language and real
  field names — copy the actual contract, don't invent placeholder shapes.

## 2. Identifiers & scenario grammar

Numbered identifiers make specs referenceable in review and in tickets. The team's actual set (from the reference specs of dmuena/cmontecinos/fecaputo) is **`US-N` / `RF-N` / `CA-N` / `E2E-N`**:

| Prefix | Meaning | Seen in |
|--------|---------|---------|
| `US-N` | User Story | SIG-263 |
| `RF-N` | Requisito Funcional (table row, with Prioridad `Debe`/`Podría`) | SIG-543, SIG-541 |
| `CA-N` | Criterio de Aceptación | SIG-543, SIG-541 |
| `E2E-N` | End-to-end test scenario (Gherkin ES: Dado/Cuando/Entonces) | SIG-263 |
| `E-N` | Evidence row (bug/incident) | SIG-547 |

> **Do NOT number `BR-N` or `SEC-N`.** No spec from the team's reference authors numbers business rules or security items. Business rules, when needed, go as a **prose section** (`## Business Rules` / reglas en prosa), not as `BR-1`. Security debt goes in prose under scope/out-of-scope, not as `SEC-N`. (Older specs like SIG-462 used `BR-N`/`SEC-N`, but that is not the current team convention.)

- **User stories:** `**As a** {role}, **I want to** {action}, **So that**
  {benefit}.` followed by a checkbox `**Acceptance Criteria:**` list. Spanish
  variant: `Como **{rol}**, quiero {…}, para que {…}.`
- **Scenarios:** `Given … / When … / Then …`. Prefix `🔴` marks a scenario that
  must be in the first QA pass. Name each one: `E2E-1: 🔴 Happy path — …`,
  `E2E-2: 🔴 Blocked — …`.
- **RF priority column** uses `Debe / Debería / Podría` (must / should / could).
- **Validation-order tables** (a strong SIG-462 pattern): `# | Condition |
  Response`, where Response is `` `422 — ERROR_CODE` ``. Listing checks in order
  makes the implementation contract unambiguous.
- **Error-message table:** `Scenario | HTTP Status | Error Code | Message`, with
  `ERROR_CODE` in `UPPER_SNAKE_CASE` and the user-facing message quoted.

## 3. Metrics & observability

Any spec that touches the data path must define its observability.

**Naming:** `advertising.signals.{component}.{name}{tag:value}`

Real examples:
```
advertising.signals.collector.partition_key.fallback{reason:unconfigured}
advertising.signals.collector.partition_key.fallback{reason:resolved_null}
advertising.signals.collector.partition_key.fallback{reason:invalid_expression}
advertising.signals.sdk.kafka.publish.attempts{status:success}
advertising.signals.sdk.kafka.publish.duration
advertising.signals.sdk.circuit.breaker.state
```

- **Split failure reasons by tag**, not by separate metric names. The team draws a
  hard line between *misconfiguration* (`reason:unconfigured`), *data absent at
  runtime* (`reason:resolved_null`), and *bad expression* (`reason:invalid_
  expression`) — because the operational response to each differs.
- **Allowed dimensions:** `event_type`, `site_id`, `destination_id`,
  `destination_type`, `environment`, `criticality`, `status`, `mode`.
- **Forbidden in metrics:** resolved key values, any payload content, user data
  extracted from the payload, and high-cardinality IDs (per-file `signal_id`,
  Kafka offsets, raw error strings, full URLs). Those belong in OTel spans or
  logs. This is both a cardinality and a privacy rule.
- SDK metric namespace is canonicalized under `advertising.signals.sdk.*`
  (SIG-205). When renaming legacy metrics, document it as an old → canonical
  table (see SIG-551).

## 4. Security & privacy expectations

Every spec should be able to answer these, even if only to say "N/A":

- No dynamic `eval` / injection surface (closed grammar for JSONPath, templates,
  etc.), with explicit depth/length limits on parsed inputs.
- External inputs (e.g. `destination.properties`) are **not trusted** — validate
  in the service layer, not just at the edge.
- Malformed payloads must not crash the pipeline.
- Metrics and logs never record sensitive resolved values.
- Known-but-deferred security issues go in a **prose** Security/Out-of-scope note
  with severity (CRITICAL/HIGH/…) and why they're deferred — not silently omitted,
  and not numbered `SEC-N` (that prefix is not team convention).

(The session may also auto-invoke `meli-security-expert` when the spec involves
application code — let it, and fold its findings into the Security section.)

## 5. Scope discipline: closed decisions vs gaps

Three distinct sections, never merged:

- **Alcance / Scope (In & Out)** — an explicit **Out of scope / Fuera de alcance**
  is *mandatory*. It's the team's primary defense against scope creep, and it
  tells the implementer what deliberately isn't theirs to build.
- **Decisiones cerradas para v1** — choices already made and *not* open to debate
  in this spec. State them so reviewers don't relitigate settled ground.
- **Gaps y decisiones pendientes** — what still must be decided, before or during
  implementation. An undocumented gap becomes a sprint surprise; naming it is how
  it gets an owner.

## 6. Linking & references

- Reference sibling specs as `SIG-N` in prose.
- Put the full URL in a **Referencias** or **Specs hijas** section:
  `https://spellbook.adminml.com/projects/SIG/specs/SIG-N`.
- Link **Grid** docs when they hold the scenario/gap detail:
  `https://grid.adminml.com/d/{id}/view`.
- An epic lists its children explicitly and links them with
  `spellbook specs children add`.

## 7. Feature codes & headers

- Optional feature code `NNN-nombre-descriptivo` (e.g.
  `005-inactive-component-soft-delete`) ties together the coordinated specs of one
  feature (functional + technical + per-app children). Use it when several specs
  orbit the same feature.
- A header block at the top is common for feature specs:
  ```
  **Feature**: `NNN-name`
  **Status**: Draft
  **Version**: 1.1.0
  **Date**: YYYY-MM-DD
  **Context**: SIG-#### (Spellbook) | Companion: SIG-####
  ```

## 8. The Signals app ecosystem

Name the impacted apps explicitly; these are the usual suspects:

| App | Role |
|-----|------|
| `ads-signals-catalog` | Signal & destination catalog; config API; write-time validation |
| `ads-signals-collector-api` | Receives signals, resolves config, publishes to destinations (Kafka, BQ, ClickHouse, streams) |
| `ads-signals-sdk-go` | Official Go SDK |
| `ads-signals-sdk-node` | Official Node.js SDK |
| `ads-signals-sdk-java` | Official Java SDK (usually a later rollout phase) |
| `ads-signals-frontend` / `rio-frontend` | RIO UI — component & signal forms |
| `rio-playmaker` | RIO backend — pipelines, component config, deploy to control planes |
| `rio-controlplane-*` | Control planes (kafka, flink, …) consuming deploy messages |
| `entity-service` | Entities/schemas referenced by components |
| `rio-report` | Cost reporting (extracted from vis-sre-tools) |

When in doubt about which app owns a behavior, read the closest canonical spec —
the "Aplicaciones impactadas" / "Impacto Cross-App" sections there are the best
current map of responsibilities.

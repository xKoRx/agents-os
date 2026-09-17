# Rio sunset update workflow

## Current integration status

The Fury CLI **is required only to create the immutable version with `fury create-version`**; the capability preflight must stop before work begins when it is unavailable. Fury catalog reads and deploy operations use HTTP against `https://web.furycloud.io`, reusing the operator's existing authenticated browser session. The skill never performs a login, never submits credentials, and never opens an authentication flow: an unauthenticated or expired session stops the external phase and is reported as such.

Verified on 2026-09-16 against `rio-controlplane-fury`, version `202605.27.0-feat-tp-inbound.20`. Each row states what was observed, not what is assumed.

| Capability | Status | Endpoint and evidence |
| --- | --- | --- |
| Authoritative sunset source | **VERIFIED** | `GET /api/proxy/dependency_catalog/artifacts/{app}/versions/{version}?page=1&size={n}` returns `general_information`, `dependencies[]`, and `page{current,size,total_pages,total}`. Each dependency carries `id`, `name`, `technology`, `version`, `severity`, `sunset_add`, `sunset_use`, `banning`, `issues[]`. |
| Sunset date | **VERIFIED** | `dependencies[].sunset_use` (calendar date) and `issues[].use_sunset` (ISO-8601, `Z`). This is the build-blocking deadline: the UI labels the column "After this deadline, you won't be able to build a version using this library." `sunset_add` is a separate, earlier restriction and must not be substituted for it. |
| Target version | **VERIFIED** | `dependencies[].issues[].upgrade_to`, a purl such as `pkg:maven/org.springframework/spring-webmvc@7.0.9`. The target is the substring after the final `@`. It is structured data, so it is never derived from prose and never defaulted to `latest`. |
| Sunset identity | **VERIFIED** | `issues[].id` (e.g. `5971996`), stable per issue, paired with `dependencies[].id`. |
| Evidence reference | **VERIFIED** | `https://web.furycloud.io/engineering/applications/{app}/artifact-details/version/{version}/detail`, plus `issues[].reason`, `issues[].category`, `issues[].severity`, and `issues[].advisor`. |
| Artifact versions to inspect | **VERIFIED** | `GET /api/proxy/dependency_catalog_v2/applications/{app}/scopes?pageNumber=1&size={n}` lists each scope with its deployed `version`; `GET /api/proxy/dependency_catalog/artifacts/{app}/latest` gives the latest artifact. |
| Scope: test vs productive | **VERIFIED — and the obvious field is a trap** | See "Identifying a test scope" below. The deploy screen reads `GET /api/proxy/fury_read/applications/{app}/scopes?show_new_criticality=true`. Its boolean `productive` **cannot be used to authorize a deploy**: it reports `false` for genuinely productive scopes. The reliable signal is `criticality === "test"`. |
| Commit → immutable build binding | **VERIFIED** | `GET /api/proxy/versions/repositories/{repo}/versions?page=0&maxResults={n}` returns an array whose entries carry `id`, `repository_name`, `version`, `branch`, **`commit`** (full SHA), `status`, `disabled`, `username`, `created_at`, and a `tags` object including `type`, `productive`, `branch_type`, `build_url`, `architectures`. The SHA binding is `commit`. |
| Active deployment check | **VERIFIED** | `GET /api/proxy/deployments/deployments?application={app}&active=true` returns the currently active deployments, and the same path without `active` returns history. Entries carry `id`, `service` (the scope), `build` (the version), `status`, `active`, `type`, `strategy`, `service_type`, `username`, `created_at`, `previous_build`. |
| Deployment identity for the report | **VERIFIED** | the numeric `id` of the deployment record, alongside its `service` and `build`. |
| Deploy pipelines surface | **OBSERVED** | This application is on "Hands-off Changes": `GET /api/proxy/deployment_pipelines/pipelines?application={app}&page=1&page-size={n}&paginated=true` returns a paginated envelope (`elements`, `page`, `page_count`, `total_count`, `is_last_page`), and `GET /api/proxy/deployments/internal/feature_flags/show_hands_off` gates the surface. A legacy view exists alongside it. |
| Deploy configuration screen | **VERIFIED** | `/engineering/applications/{app}/deployment-pipelines/hands-off/configure-deployment?mode=handsoff` — the same path for every application. It loads the deployable versions from `GET /api/proxy/versions/repositories/fury_{app}/versions?page=0&maxResults={n}&withValidations=true`, the selectable scopes from `GET /api/proxy/fury_read/applications/{app}/scopes?show_new_criticality=true`, the concurrency check from the active-deployments endpoint, and a quota from `GET /api/proxy/traceability/traceability-status/application/{app}/remaining-deploys`. The wizard then offers optional steps, a scheduling choice, and a `Validate & Continue` action, followed by an `Execute pipeline` action. |
| Deploy pipeline structure and monitoring | **VERIFIED** | Observed on 2026-09-16 during a deploy a human performed deliberately on `rio-controlplane-clickhouse`, scope `test`. See "Deploy pipeline contract" below. |
| Deploy and finish **request payloads** | **VERIFIED** | Captured on 2026-09-16 during a deploy a human performed deliberately, by instrumenting the page's own `fetch` and `XMLHttpRequest`. See "Deploy and finish requests" below. |

Observed sample, for reference on how the contract materializes: of 161 dependencies, 5 carried a sunset date, and exactly 1 fell inside the window evaluated that day — `org.springframework/spring-webmvc` at `6.2.12`, `sunset_use` `2026-09-18`, issue `5971996` ("Arbitrary Code Injection", SECURITY, CRITICAL), `upgrade_to` target `7.0.9`.

All nine phases are now backed by verified contracts, including both deploy mutations. What remains unproven is the flow as a whole: no complete `$rio-sunset-update <project>` run has been executed end to end, and only `rio-controlplane-fury` (sunsets) and `rio-controlplane-clickhouse` (deploy) were exercised. The skill must never fabricate an endpoint, a sunset item, a target version, a project command, a branch, a PR, a build, or a deployment.

Two further constraints apply:

- The allowlist names are Fury **applications**, whose Fury project is `dps-rio`. Phase 2 checkout identity and phase 8 scope ownership must both be checked against the application name, not against a Fury project named after the allowlist entry.
- An application whose scopes response is empty, or of a library type with no scopes, cannot be deployed to test. The flow stops at scope resolution rather than attempting a deploy.

## Identifying a test scope

This is the highest-risk decision in the flow. Measured on 2026-09-16 across the scopes of **all eleven allowlisted projects** — around 140 scopes — plus a field-by-field comparison on `rio-controlplane-clickhouse` against the deploy screen's own "Productive" badge:

| Signal | Verdict |
| --- | --- |
| `criticality === "test"` | **The only reliable positive signal.** It held for all 6 non-productive scopes and for none of the 8 productive ones. |
| `productive === false` from `fury_read` scopes | **Unsafe. Never grant on this.** It reported `false` for 5 scopes the UI marks Productive, including the scope literally named `prod`. Trusting it authorizes a production deploy. |
| `productive === true` from any endpoint | Usable only to **deny**. |
| The scope's name | **Unsafe in both directions.** `test-events` and `stage-events` are productive despite their names; `bq-stage-nonprod` is not productive despite "stage". Never infer from the name, and never substring-match on `test`, `stage`, `nonprod`, or `prod`. |
| `dependency_catalog_v2` scopes `productive` | Incomplete — it covered 5 of 14 scopes — so absence proves nothing. Usable only to deny. |

**The rule lives in a script, not in this prose.** Save the scopes response to a file and run:

```text
node skills/rio-sunset-update/scripts/validate-scope.mjs --project <proyecto> --scope <scope> --scopes-file <ruta.json>
```

A non-zero exit is a complete stop, and its exit code — not this document — is what authorizes the deploy. The script is the gate precisely so that an agent which never opens this file still cannot reach production. Never re-implement the decision by hand, never proceed on a rejection, and never pass a payload that was edited after being fetched.

What the script enforces, all of which must pass:

1. The scope was named explicitly by the operator. Never offer, guess, complete, or default one.
2. Exactly one entry in the `fury_read` scopes response has `name` equal to that string, literally.
3. That entry's `criticality` is exactly `test` — the only signal that authorizes.
4. `productive` is not `true`, in any response. It can only deny, never authorize.
5. The name carries no `stage` segment. **Stage does not count as a test environment**, and it must be rejected even though its `criticality` is also `test`, which is the one thing `criticality` alone cannot distinguish. The name is used only to deny, never to grant.
6. The entry belongs to the supplied application when the payload declares an application.
7. Nothing is ambiguous: no match, several matches, a malformed or empty response, missing `criticality`.

Deny by default. If the evidence is not present and unambiguous, the scope is treated as productive and rejected, whatever its name suggests.

### What the eleven-project measurement showed

- **No scope anywhere has `criticality: test` together with `productive: false` while actually being productive.** The two conditions together held across all eleven projects, which is the evidence the gate rests on.
- **Neither condition is sufficient alone.** `rio-controlplane-fury` has `prod-default-test--tp` and `prod-test--tp-nonprod` with `criticality: test` **and** `productive: true`. Dropping the productive denial would accept both. Meanwhile `prod`, `production`, `consumer-prod` and `prod-nonsite` across several projects carry `productive: false` and are caught only by `criticality`. Each signal covers the other's blind spot.
- **`stage` has more than one spelling.** Besides `stage`, `api-stage` and `bq-stage-nonprod`, `rio-controlplane-flink` uses `staging-nonprod` and `staging-consumer-nonprod-nonprod`. A pattern matching only `stage` misses `staging`, so both are listed.
- **`dev` and `develop` also appear with `criticality: test`** (`rio-materializer` and `rio-controlplane-flink`). They are treated as non-test environments too, by the same deny-only-by-name rule. Revisit if the team decides a development scope is an acceptable target.
- **`rio-sdk-events` has no scopes at all**, confirming it cannot receive a test deploy. A run for it stops at scope resolution.

## Deploy pipeline contract

Observed end to end on 2026-09-16: `rio-controlplane-clickhouse`, scope `test`, pipeline `318145`, deployment `37346549`.

A hands-off pipeline is a sequence of steps, and the deploy is only its first one:

| # | `do` | `execution_data` |
| --- | --- | --- |
| 1 | `deploy` | `application`, `service` (the scope), `build` (the version), `strategy` (`blue_green`), `swap_interval`, `swap_block_size` |
| 2 | `wait` | `minutes` |
| 3 | **`finish`** | `application`, `service`, `build`, `strategy`, `deployment_id` |

**The `finish` step requires an explicit click; it does not complete on its own.** When the deployment reaches its `Effective` state the screen offers a `Finish` button, labelled "Finish or Rollback, if you don't it will be automatically finished in 14 days". The step sits at `running` until that button is pressed, and pressing it is what closes the deployment and **releases the scope**. The flow ends there: **never press `Instant Termination`**, and never rollback unless a human asks for it.

This resolves what would otherwise look like a conflict with the prohibition on performing a finish. That prohibition is about promoting to a productive environment. Finishing a deployment on a `criticality: test` scope is the concluding act of the test deploy itself, and leaving it unfinished would strand the scope. So the skill presses `Finish` for a validated test scope, after the confirmation from phase 8, and still never promotes, never deploys anything productive, and never terminates instantly.

Pipeline-level fields: `id`, `name` (`handsoff-YYMMDD-HHMM`), `description` (carries the intent and version), `status`, `completion` (0–100), `user` (the human), `validated`, `preauthorized`, `maintenance_window_compliant`, `retry_and_skip_supported`, `metadata`.

Each step target carries `status` and `last_attempt.deployment_id`, which is how a pipeline step is tied to the deployment record it produced.

### The stated target version may not exist — verify it in the registry

**The authoritative source can name a version that does not exist.** Verified on 2026-09-17: for `rio-controlplane-flink`, Fury's own `issues[].upgrade_to` gave `pkg:maven/org.apache.tomcat.embed/tomcat-embed-core@10.1.58`, and the artifact registry that the project builds against has no `10.1.58` at all — it carries `10.1.52` through `10.1.57`, then `10.1.59` and `10.1.60`. The version was skipped upstream.

Applying it produced a build that failed at the `install_dependencies` stage, which Fury classified as `user_error`. So an unverified target does not fail late and loudly; it fails as a broken build that looks like the change's fault.

So after extracting `targetVersion`, and **before editing anything**, confirm it exists in the registry the project resolves from. The project declares that registry in its own build configuration; read it from there rather than assuming one. For a Maven-style registry:

```text
GET <registry>/<group-with-slashes>/<artifact>/maven-metadata.xml
```

and require `targetVersion` to appear among the listed versions.

If it is absent, **stop for that item** and report: the component, the target the source stated, and the versions the registry actually offers around it. Exclude it from the batch exactly as a blocked item. **Never substitute a nearby version on your own** — not the next one up, not the newest, not the closest. The neighbouring version may well be the right answer, but choosing it is a human decision, and silently retargeting is the same failure as defaulting to `latest`.

This check is also what keeps the earlier prohibition honest: a target taken from structured data is only trustworthy if the data is true, and here it was not.

### Check for work already in flight, before touching anything

Run this **in phase 3, before classification and before any edit**. A sunset that someone is already fixing does not need a second fix, and a second fix is worse than none: it creates a competing change, a conflicting pin, and review load for a patch that will be thrown away.

For each eligible item, look for an existing effort covering it:

1. List the repository's open pull requests and read their titles and changed files.
2. List recently built versions in Fury and note which branches they came from. A branch with a run of recent builds is active work, even when its pull request is not obvious.
3. For any candidate branch, read the manifest **on that branch** and check whether the component's declaration or pin already moves to or past the target version.

**The decision is per item, never all-or-nothing.** Each eligible sunset is judged on its own, and the batch is whatever remains uncovered. Given three eligible sunsets:

| Already covered by an open PR or active branch | The run does |
| --- | --- |
| none of the three | attacks all three, in one batch and one pull request |
| two of the three | attacks **only the remaining one**, still one pull request |
| all three | **nothing** — no branch, no pull request, no build, no deploy |

An item that is covered **leaves the batch entirely**: it is not edited, not committed, and not counted toward whether a pull request is worth opening. Report it as `already in flight`, naming the pull request or branch and what that work sets the component to, so the reader can see it was seen and deliberately skipped rather than missed.

When nothing is left to attack, the run still produces its report — listing every eligible sunset and who is already handling it — and stops there. That report is the deliverable; a run that finds all the work already in progress has succeeded, not failed.

Judge coverage by intent, not by string equality with `targetVersion`. Observed in practice: the sunset asked for tomcat-embed `10.1.58` on a Spring Boot 3.5 line, while an open pull request migrating the project to Spring Boot 4 moved the same pin to `11.0.24` — a different version that resolves the same sunset, and in the same change also resolves a second eligible item (`spring-webmvc`, whose target required Spring Boot 4 anyway). A naive equality check would have called that "not covered" and opened a redundant pull request, which is exactly what happened before this rule existed.

When the sunset deadline is close and the in-flight work may not land in time, that tension is a **human decision**: report both the deadline and the in-flight effort, and let a person choose between waiting and a stopgap. Never decide it silently in either direction.

### Session expiry is a first-class failure mode

An authenticated session can lapse **mid-run**, and it does not announce itself cleanly. Observed in practice, across two different systems in the same run:

- The code host accepted the page load but refused the pull request creation with a generic "there was an error creating your PullRequest" and no stated cause. The real reason was that the single-sign-on session had lapsed. A naive reading blames repository policy and abandons the run for the wrong reason — which is exactly what happened.
- Fury returned HTTP 405 with an identity-provider error payload, and the page was redirected to the SSO provider, rather than returning a clean 401.

So: **before every mutation, confirm the session is alive**, cheaply — a read whose shape is known. And when a mutation fails with a generic or structurally odd error, **check the session before concluding any other cause**. Never infer policy, permissions, or a changed contract from an error that an expired session would produce identically.

When the session has lapsed, stop the affected external phase, report exactly which system needs re-authentication, and wait. Never attempt the login, never submit credentials, never accept a token or a verification code from the operator, and never retry the mutation in a loop hoping it clears — repeated identical failures are a stop, not a signal to keep trying.

### How Fury is driven: API first, UI only as a fallback

Every Fury interaction — reads and both mutations — is performed by calling the documented endpoints from a context that already carries the operator's authenticated session. The point is that the run needs no visible navigation, no clicking, and no screen-scraping: it is a sequence of HTTP calls whose payloads are recorded below, so it behaves the same whether or not anyone is watching a window.

Driving the interface is the **fallback**, used only when a call is refused in a way that the documented contract does not explain, or when an endpoint has visibly changed. Falling back is a reportable event, not a silent retry: say which call failed and why the interface was used instead.

Two hard limits on the fallback, both learned the hard way:

- **Never substitute a code host's web editor for a local edit.** Those editors reject synthetic input and virtualize their content, so what was written cannot be read back and verified before committing. Committing unverifiable content to a real repository is not an acceptable fallback.
- **Never treat repeated interface failures as something to push through.** Two attempts that fail the same way are a stop, with the reason reported. Observed in practice: pull request creation refused twice by the code host with a generic error and no stated cause, most likely a repository or organization policy. The correct response was to stop, confirm that nothing had been created, and hand it to a human — not to keep clicking.

### Deploy and finish requests

Captured on 2026-09-16 from a real run: `rio-controlplane-clickhouse`, scope `bq-test-nonprod`, version `2026.9.15`, pipeline `319038`, deployment `37353413`.

The wizard issues several calls; only two of them mutate. The others (`spider/entities/search`, `deployments/strategies/advice`, `deployment_advisor/api/v1/intents/advice`, `deployment_pipelines/pipelines/validate-creation`, `deployments/strategies/advice/preflight-validations?type=monitors`) are advisory or validating and are POSTs despite not creating anything.

**1. Create the pipeline.** `POST /api/proxy/deployment_pipelines/pipelines`

```json
{
  "name": "handsoff-<YYMMDD-HHMM>",
  "description": "Hands Off Changes pipeline — intent: Release — version: <version>",
  "steps": [
    { "do": "deploy", "over": [{ "application": "<app>", "service": "<scope>", "build": "<version>",
                                 "strategy": "blue_green", "swap_block_size": 100, "swap_interval": 30 }] },
    { "do": "wait",   "over": [{ "minutes": 1 }] },
    { "do": "finish", "over": [] }
  ],
  "scheduled_start_date": null,
  "on_alert": { "abort_after_minutes": 1440 },
  "on_abort": { "rollback_active_deployments": true },
  "maintenance_window_compliant": false,
  "metadata": { "opsgenie": { "enabled": false } }
}
```

Note that `build` here is the version string, not the build object. `scheduled_start_date` **must always be `null`** — that is how "start immediately" is expressed, and a date here would be the scheduling this skill is forbidden from doing. Send exactly one entry in the deploy step's `over`, for the single validated test scope.

**2. Finish the deployment.** `PUT /api/proxy/deployments/deployments/{deploymentId}/finish`

```json
{ "swap_block_size": 100, "swap_interval": 60 }
```

The `finish` step is declared in the pipeline with an empty `over`, and it stays `pending` until this PUT arrives. That is why finishing is an explicit act and not something the pipeline completes on its own.

### Monitoring to a stable state

| Purpose | Call |
| --- | --- |
| Pipeline progress | `GET /api/proxy/deployment_pipelines/pipelines/{pipelineId}` → `status`, `completion`, `steps[].status` |
| Pipeline list for an application | `GET /api/proxy/deployment_pipelines/pipelines?application={app}&page=1&page-size={n}&paginated=true` → paginated `elements` |
| Deployment progress | `GET /api/proxy/deployments/deployments/{deploymentId}` → `status`, `active`, `signals` |
| Current action signals | `GET /api/proxy/deployments/deployments/{deploymentId}/actions/current_action/signals` |
| Per-step events | `GET /api/proxy/deployments_events/events?deployment_id={deploymentId}&step_name={step}` |
| Rollback history | `GET /api/proxy/deployments/deployments/{deploymentId}/rollback/cause/history` |
| Component diff | `GET /api/proxy/deployments/deployments/{deploymentId}/components_diff` |

Observed deployment `status` progression for a successful run: `effective` → `finishing` → `finished`, with `active` flipping to `false` at the end. `rollbacked` also exists. Step statuses: `pending`, `running`, `completed`, with `RUNNING`/`FINISHED` on targets. `signals` reports granular progress: `containers_started`, `booted`, `application_up`, `sidecars_up`, `swapped_in`, `receiving_traffic`, `swapped_out`, `created`, `failed_instances`, `failed_swapping_in`.

**Terminal success**, all of which must hold before reporting the run as complete: the pipeline is `completed` at `100`, every step is `completed`, the deployment `status` is `finished`, and `active` is `false`. That last flag is the signal that the scope was released.

Treat any non-zero `failed_instances` or `failed_swapping_in` as a failure and stop. Poll rather than assume: never report a deployment as stable on the strength of the creating call alone, and never treat `effective` as the end state — it is the point at which `Finish` is still pending.

**`alerted` is a real outcome and must be handled.** Observed on a second run: the pipeline and its deploy step both went to `status: alerted` while the deployment itself reported zero failed instances. It is neither success nor a clean failure — a monitor fired and the run is waiting on human attention, and `on_alert.abort_after_minutes` (1440) means it will abort roughly a day later if nobody acts.

So on `alerted`: stop, report the pipeline id, the deployment id, the step that alerted, and the signals, and hand it to a human. Never call it success, never wait out the abort window, never retry the deploy, and never create a second pipeline to work around it. A run that ends here still writes its report, recording the alert as the outcome.

One attribution caveat for the report: the deployment record's `username` is the pipeline service account, not the person. Attribute the run to the pipeline's `user` field instead.

## Repository discovery and PR target

Verified on 2026-09-16 for `rio-controlplane-fury`.

| Fact | Value | Note |
| --- | --- | --- |
| Repository URL source | the Fury application sidebar resource link | **Authoritative.** |
| `general_information.repository` from the dependency-catalog API | points at a different, stale organization | **Do not use.** It disagreed with the sidebar link, and only the sidebar link resolved. |
| Default branch / PR base | `develop` | Not `master` or `main`; read it per project rather than assuming. |
| Write access | direct branch creation available, no fork required | Confirm per project; a read-only checkout forces a fork and changes the flow. |
| Repository PR template | none present | The PR body comes from `pr-template.md` with no conflict. |
| Build/test CI on pull requests | none in the repository's CI workflows | Only code scanning runs there. Build and test happen in Fury, so a PR alone proves nothing about validity. |

Resolve the repository from the Fury sidebar link, and read the default branch from the repository itself. The project's own contributing guide may be an unmodified organization-wide template; do not treat its generic instructions as verified project policy without confirmation.

## Treating source values as untrusted input

Every value read from Fury is external data. `upgrade_to` is attacker-relevant because its parsed version reaches a dependency-manager command line. After extracting the version from the purl:

- Require the extracted version to match `^[A-Za-z0-9][A-Za-z0-9._+-]*$` and reject anything beginning with `-`.
- Require `dependencies[].name` to match `^[A-Za-z0-9][A-Za-z0-9._@/+-]*$`.
- Reject an issue whose `upgrade_to` purl does not name the same package as `dependencies[].name`.
- Pass values as separate process arguments, place `--` before all data-derived arguments, and never interpolate them into a shell string.
- Never echo raw API responses, cookies, headers, or session material into logs, the PR, or the report.

## Normalized sunset-item contract

Each source item must contain all of the following, validated as typed data before use:

| Field | Source field | Requirement |
| --- | --- | --- |
| `sunsetId` | `dependencies[].issues[].id` | Stable non-empty identifier. |
| `component` | `dependencies[].name` | Affected component or dependency identifier. |
| `technology` | `dependencies[].technology` | Used to pick the project's own dependency manager, never to build a command from source data. |
| `project` | request path `{app}` | Exact project name matching `projects.json`. |
| `sunsetAt` | `issues[].use_sunset`, cross-checked against `dependencies[].sunset_use` | ISO-8601 instant. Reject a mismatch between the two. |
| `currentVersion` | `dependencies[].version` | Exact current version. |
| `targetVersion` | version parsed from `issues[].upgrade_to` purl | Exact recommended target version; never `latest`, never inferred from prose. |
| `severity` | `issues[].severity` | Reported, never used to skip a gate. |
| `evidenceReference` | artifact-details URL + `issues[].reason` | Stable source reference sufficient for PR review. |

Reject missing, ambiguous, malformed, or cross-project data. Do not print raw source responses or authentication material.

Passing external values as separate process arguments does not by itself prevent option injection: a value such as `--upload-pack=…` is still interpreted as a flag. Therefore `sunsetId`, `component`, `currentVersion`, and `targetVersion` must additionally match `^[A-Za-z0-9][A-Za-z0-9._@/+-]*$`, any value beginning with `-` must be rejected, and `--` must precede all data-derived arguments in every command.

## Phases and resumability

1. **Input gate (no network/mutation):** run `node skills/rio-sunset-update/scripts/validate-input.mjs <nombre_del_proyecto>`. It accepts exactly one literal allowlisted project. Any error stops here.
2. **Preflight:** obtain the checkout as described in "Obtaining the project checkout" below, then verify its identity equals the supplied project and that `git status --porcelain` is empty. Check existing code-host and Fury authentication non-interactively only. Missing or expired credentials stop the affected external phase; never invoke login and never ask for a password, token, or verification code.
3. **Discovery:** read the scopes response to learn which artifact versions are deployed, then read the dependency catalog for the relevant version, paginating with `page`/`size` until `page.total` is covered. Enumerate **every** dependency that carries a sunset date — never stop at the first, and never sample: paginate the catalog to completion before filtering. A dependency may carry several issues, so collect all of them. Then keep the ones whose `upgrade_to` yields a valid target version. At runtime select the inclusive window of 15 calendar days **counting the execution date itself as day 1**: from the start of the current day through the end of `current day + 14 days`, in an explicitly displayed IANA timezone and offset. Both boundaries are inclusive, so a sunset expiring today and one expiring on day 15 are both eligible. Compute the window per execution; never persist it and never schedule it. Deduplicate by `(sunsetId, component, targetVersion)`. Zero eligible items is a complete no-op: no branch, PR, deploy, or report.

A run processes the **entire eligible set for the project as one batch**. It never iterates one sunset at a time into separate branches or separate pull requests. If two issues on the same component resolve to different targets, keep the highest target that satisfies both and record both issue IDs against it; if they conflict irreconcilably, exclude that component from the batch and record it as blocked rather than guessing.
4. **Plan and update:** show the normalized plan and evidence before mutation. Resolve the dependency manager and validation commands from versioned configuration in the checked-out project, not from this registry or source data. Pass all validated values as separate process arguments; never concatenate shell strings. Limit changes to manifests, lockfiles, and migrations directly required by eligible items.

Before editing anything, classify how the project actually supplies the component. A sunset component is frequently **not** declared in the manifest, so a version string rewrite is invalid and must not be attempted blindly. The classification decides the outcome:

| Case | How it appears | Action | | --- | --- | --- | | Declared directly with a literal version | an explicit dependency line naming the component and version | Bump that single line to `targetVersion`. | | Managed by a platform/BOM the project declares | the component is absent, but a BOM or platform artifact is declared | **Stop and report.** Reaching `targetVersion` requires a BOM bump whose blast radius is not confined to this component. | | Managed by a build plugin's dependency management | the component is absent and its version tracks a plugin's release train | **Stop and report.** Reaching `targetVersion` may require a major plugin upgrade, which is not a mechanical change. | | Overridable by a documented pin the project already uses | the project already demonstrates an override idiom for managed versions | Propose the override, but apply it only after explicit human approval, because an override silently diverges from the managed set. | | Purely transitive with no declaration or override | none of the above | **Stop and report.** |

Only the first case is applied automatically. Never invent a declaration, never add a component that the project did not declare, and never substitute a different version from the one the source states.

A blocked item must be **actionable without further digging**. "Managed elsewhere" is not a finding; naming what manages it is. For every blocked item, read the project's own manifest and record: the managing artifact (the platform, BOM, or build plugin), its currently declared version, and the literal manifest line that declares it. Add the override idiom the project already demonstrates, if it uses one, quoting the existing example rather than inventing syntax. The reader should be able to go straight to the decision — bump the manager, pin an override, or wait — without reopening the build file to find out who is in charge.

Record the manager from the manifest only. Never guess which release train carries the target version, never assert that a particular manager version would resolve the sunset, and never state a compatibility claim that was not verified. If the manifest does not make the manager identifiable, say exactly that instead of inferring one.

Classify **every** item in the batch before editing, then split the set in two: `applied` and `blocked`. Apply all `applied` items together in one working set, so a single batch carries every mechanically safe update. A `blocked` item never stops the batch — it is carried into the PR body and the report with its classification and evidence, so the run still delivers the safe updates while making the human decisions explicit. If the batch has **no** `applied` items, the run stops after this phase with the classification report and opens no PR.
5. **Validation:** confirm first that the project's toolchain can actually run here — the build tool at the version its wrapper pins, the required language runtime, and reachable dependency registries. **Validation that cannot be executed is not a pass.** If the toolchain or the registry is unavailable, stop with `VALIDATION_UNAVAILABLE`, keep the edit uncommitted, report which capability is missing, and do not open a PR; do not fall back to reasoning about whether the change looks safe. Then run the project's defined build, tests, lint, and/or typecheck **once over the whole batch**, and inspect the diff. Any failure blocks commit, push, PR, and deploy for the entire batch; never silently drop the offending item and retry, because the remaining set was validated only in its presence. Report which item the failure implicates so a human can exclude it deliberately and re-run. An empty diff is a no-op.
6. **Branch and PR — exactly one per project:** the branch name derives only from the validated project name, never from the item set or the date, so every run for a project lands on the same branch and reruns are idempotent. **Read the prefix convention from the repository instead of choosing one**: list the existing remote branches and use the prefix the project actually uses. In the verified case that prefix was `feature/`, and it is not cosmetic — the project's Fury builds run under `gitflow`, where `tags.branch_type` is derived from the branch prefix, so an unrecognized prefix such as `chore/` can mean no build is produced at all, which in turn means no immutable build to bind and no deploy. Prefix wrong, flow dead. Before creating anything, look for an open pull request from that branch for this project:

   - **An open PR exists:** reuse it. Add only the items it does not already cover, and regenerate its body so it describes the full current set. Never open a second PR for the same project.
   - **No open PR exists:** create the branch and open one PR.

One run produces at most one pull request, carrying every applied item in the batch. The PR uses `pr-template.md`, including the window, per-item previous and target versions, files changed, evidence, validations, and the blocked items with their classification. Do not include unrelated changes.
7. **Immutable build:** **Fury does not build on push.** A pushed branch produces no version by itself — verified: a freshly pushed commit had no entry in the versions collection, and the Versions screen offers no create control. The version has to be created explicitly, from the project checkout, with the Fury CLI:

   ```text
   fury create-version
   ```

That is the whole command — let Fury name the version. Observed names follow a `<numeric>-<branch-derived-suffix>` shape, such as `0.0.14-fix-update-vulnerabilities`. Create the version **from the PR's branch, at the PR head commit**, so the `commit` field of the resulting version is the SHA the next gate requires. Never create a version from a dirty worktree, from a different branch, or after moving HEAD.

**The command returns before the version is built.** Creation is asynchronous, so the command exiting successfully proves nothing about the build. Poll until the version reaches a terminal state, at `/engineering/applications/{app}/versions` or its endpoint:

   ```text
   GET /api/proxy/versions/repositories/fury_{app}/versions?page=0&maxResults={n}
   ```

Match on `commit` equal to the PR head SHA, never on branch or recency, and wait for `status`. `FINISHED` is the only state that allows the run to continue. Any other terminal state is a **validation failure**, not a retry prompt: this build is what validates the change, so a build that does not finish means the change is not validated, and the run stops with the PR in place and no deploy. Report the version name and its state. Never create a second version to try again, and never fall back to an earlier build.

This step needs the Fury CLI on the host, which is a sixth required capability and was **absent** in the verified environment. Without it, stop with `BUILD_CREATION_UNAVAILABLE`, report that the CLI is missing, and leave the pull request in place — do not deploy an older build that merely shares the branch.

Then, once a version exists, save the repository's versions response to a file and run the gate, which decides mechanically rather than by reading:

   ```text
   node skills/rio-sunset-update/scripts/validate-build.mjs --sha <pr-head-sha> --versions-file <ruta.json>
   ```

It accepts only a build whose `commit` equals the full 40-character PR head SHA exactly, whose status is finished, which is not disabled, and which is not productive; it rejects a short SHA, a missing build, and two usable builds for the same commit. A non-zero exit stops the flow. Never compare by branch name, version string, or recency, and never use the working tree, an implicit base branch, or an unbound artifact. Record the accepted `version` and `commit` together; every later phase refers to that pair.
8. **Scope and confirmation:** only now ask the operator for a test scope, and resolve it through the gate in "Identifying a test scope" above. Reject blank, missing, ambiguous, cross-application, or non-test scopes. Never grant on the `productive` boolean and never on the scope's name. Show project, PR SHA, immutable build, and resolved scope; require an immediate explicit confirmation.
9. **Test deploy:** before any mutation, read the active deployments for the application and stop if one already targets the same `service` as the resolved scope. A conflict or HTTP 409 is a resumable stop; never create a second deployment. Then, only after the explicit confirmation from phase 8, create the pipeline with the verified request in "Deploy and finish requests", carrying exactly one deploy target and `scheduled_start_date: null`. Record the pipeline `id` and the `deployment_id` from `steps[].over[].last_attempt`. Monitor as described in "Deploy pipeline contract"; on `alerted`, stop and hand it to a human. When the deployment reaches `effective`, issue the finish request to release the scope, and stop only at terminal success as defined there. Never issue an instant termination, never roll back unless a human asks, and never promote, auto-merge, deploy a productive scope, or schedule execution.
10. **Report:** once the test deployment reaches a stable state, generate the run document from `report-template.md`. It records every mapped sunset, its expiry date, the PR opened for it, and the scope actually deployed. Write it as described in "Where the report is written" below, and state the absolute path in the final summary. Include only values observed in earlier phases — never a planned, assumed, or placeholder PR, scope, or deployment ID. If a phase stopped early, the report states that phase's stop reason instead of inventing a result, and a run that produced no eligible items produces no report. Publishing the document to an external destination such as Drive is optional and requires an already-authorized connector; a missing or expired connector blocks only the upload, never the local file.

## Obtaining the project checkout

The skill never searches the filesystem for a repository and never clones silently. It works from a checkout the operator points at, and if there is none, it offers to clone — with the operator deciding both whether and where.

1. **Ask for the checkout path** for the supplied project, unless the operator already gave one at invocation.
2. **If a usable checkout is provided**, continue to the identity and cleanliness checks. Nothing is cloned.
3. **If the operator has no local clone**, ask a single explicit question: clone it, or stop?
   - **Declines** — stop immediately, reporting that the run cannot continue without a checkout of the project. This is a clean no-op: nothing was read, edited, branched, or deployed.
   - **Accepts** — ask for the destination directory. Never pick one, never default to the current directory, and never reuse the directory holding this skill.
4. **Clone**, with these constraints:
   - The clone URL comes from the Fury application's GitHub sidebar link, which is authoritative. Never use the `repository` field from the dependency-catalog API: it was observed pointing at a stale organization.
   - The destination must be an empty or non-existent directory. Never clone over, into, or on top of existing content, and never delete anything to make room.
   - Authentication is non-interactive only. If the existing credential is missing or expired, stop and report it; do not start a login flow and do not accept a token from the operator.
   - Pass the project name and destination as separate process arguments, already validated by the input gate, with `--` before data-derived arguments.
5. **After cloning**, run the same identity and cleanliness checks as for a pre-existing checkout. A fresh clone is not assumed to be correct.

Record in the report whether the checkout was pre-existing or cloned during the run, and the path used. A cloned repository is left in place: the skill does not delete it afterwards.

## Where the report is written

The destination is explicit, never improvised, and never inside the project.

1. If the operator named an output directory when invoking the skill, use it.
2. Otherwise use the directory the skill was invoked from.

**Never write the report inside the project checkout**, and never inside any Git worktree the run touched. The skill requires a clean worktree and inspects its own diff, so a report dropped there would either dirty the tree or, worse, ride along into the commit and the pull request. If the resolved directory turns out to be inside the checkout, stop and ask for a destination rather than picking one.

Filename, deterministic and collision-safe:

```text
rio-sunset-update-<project>-<YYYYMMDD-HHMM>.md
```

Report the absolute path in the final summary, so the operator never has to hunt for it. Writing this local file is the deliverable and always happens, whatever happens with Drive.

### Drive destination

Reports accumulate in one place, so they can be read as a history rather than hunted for.

**When Drive access is already configured:** look for a folder named `Sunsets history`. If it does not exist, create it. Every report this skill produces, from then on, goes there. Do not create a second folder when one already exists, do not rename or reorganize anything else, and if several folders share that name, ask which to use rather than guessing.

**When Drive access is not configured:** ask whether the operator wants to configure it.

- **Yes** — give the step-by-step for their client and **wait** for them to finish, then re-check and proceed with the folder logic above. Never attempt the authorization flow on their behalf, and never ask for a credential, token, or authorization code.
- **No** — write the local file only. Say so plainly in the final summary and show the absolute path, leaving the operator to decide what to do with it. This is a normal outcome, not a failure, and it never blocks the run.

An expired or failing connector is treated the same as "not configured": the local file still exists, and the upload is reported as the only thing that did not happen.

## Failure and resumption matrix

| Checkpoint | Failure behavior | Safe resume point |
| --- | --- | --- |
| Input / allowlist | No network or mutation | Re-run with one exact project. |
| Source / credentials | Preserve local state; no login | Re-run after a documented source or existing credential is available. |
| Checkout / worktree | No edits | Clean or select the correct checkout manually. |
| No eligible items / empty diff | No branch, PR, or deploy | Re-run when source data changes. |
| Update / validation | No commit, push, PR, or deploy | Correct only required files, then revalidate. |
| Classification: no applied items | No branch or PR; blocked items reported | Decide the BOM/plugin bumps by hand, then re-run. |
| Branch / PR | Reuse the project's single deterministic branch and its open PR | Re-run; the existing PR is updated, never duplicated. |
| Build / scope | No deploy | Re-run after exact build or valid test scope exists. |
| Active deploy / conflict | Do not create another deploy | Monitor or resolve the existing deployment externally, then re-check. |
| Report write / upload | Deployment already happened; do not repeat it | Re-emit the document from recorded phase results only. |

## Required final phase summary

Report discovery, update, validations, branch/PR, build, deploy, and report separately. Report only identifiers and safe metadata; never record credentials, tokens, or raw sensitive responses.

# Rio sunset update workflow

## Current integration status

Discovery and every verification read are read-only HTTP against `https://web.furycloud.io`, reusing the operator's existing authenticated browser session. The Fury CLI is **not** used for reads, but it **is** required for exactly one write: `fury create-version`, which creates the immutable build (see "Immutable build" in the phases below). Deploy and Finish go through the session as documented there. The skill never performs a login, never submits credentials, and never opens an authentication flow: an unauthenticated or expired session stops the external phase and is reported as such.

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

- The name the operator supplies is a Fury **application**, not a Fury project. For the RIO applications the Fury project is `dps-rio`, but that mapping is not something to assume for an arbitrary application. Phase 2 checkout identity and phase 8 scope ownership must both be checked against the application name, never against a Fury project named after it.
- An application whose scopes response is empty — a library or SDK — has nothing to deploy to. That is a normal shape, not a block: the run skips the scope question and the deploy phase. See "Projects with no deployable scope" below.

## Validar el proyecto contra Fury

The input gate checks shape only; it carries no list of accepted projects, deliberately, so the skill is not confined to a fixed roster. Existence is therefore the **first network step**, before any checkout, branch, or edit:

```text
GET /api/proxy/tracing_api/applications/{app}
```

Measured on 2026-09-17: a real application answers `200` with a `project_id` (`rio-controlplane-kafka`, `rio-sdk-events`), and a name that does not exist answers `404` (`proyecto-inexistente-xyz-123`). So the distinction the allowlist used to make is available from the platform itself, and from the platform it stays correct as applications are created and retired.

Rules:

- A literal `404` stops the run. Report the name as Fury does not know it, and do not guess a correction: a typo that resolves to a different real application would send the whole flow at the wrong project.
- A `404` is distinguishable from a failed read: a `5xx`, a timeout, a network error, or any other non-`200` that is not a `404` — including a `200` whose body is missing `project_id` — is **not** evidence the project is unknown. Never infer "nonexistent application" from a call that simply failed to answer; that conflates "Fury told us no" with "we could not ask Fury", and the first network call of the whole flow is the wrong place to misdiagnose which one happened.
- An authentication failure here is **not** a missing project. It is the session-expiry case ("Session expiry is a first-class failure mode"), and it must be reported as a block, never as a nonexistent application.
- Any other failed read (not a `404`, not session-expiry) stops the run as a block too, reported as "could not verify the project against Fury", never as "project unknown".
- Confirming existence authorizes nothing else. Checkout identity, scope ownership and the build binding are still each checked on their own.

## Projects with no deployable scope

Read the scopes response before asking the operator anything about deploying:

```text
GET /api/proxy/fury_read/applications/{app}/scopes?show_new_criticality=true
```

An empty list is the expected answer for a library or SDK — measured on 2026-09-17, `rio-sdk-events` returns `200` with **0 scopes** while `rio-controlplane-kafka` returns 6. A library is consumed by other applications, so there is no environment of its own to deploy into.

When the list is empty:

- **Skip the scope question and the whole deploy phase.** Do not ask which scope to use, do not offer to create one, and do not present a chosen scope for confirmation — there is nothing to confirm.
- **Do not treat it as a failure or a block.** The pull request is the complete deliverable for such a project; the run ends successfully after it.
- Say so explicitly in the summary and in the report: the project has no deployable scope, so the change was validated by build and tests only, and its effect on consumers is verified when they pick the new version up. That last sentence matters — a library's blast radius is larger than a service's, and no test deploy of this run exercised it.
- The outcome is the applied one, qualified as without-deploy. It must not be reported as `ACTION_REQUIRED`, which means a person has to decide something, nor as `STOPPED`.

An empty list is distinguishable from a failed read: a failed read has no `200`. Never infer "no scopes" from an error, a timeout, or a redirect to a login page — those are blocks.

## Identifying a test scope

This is the highest-risk decision in the flow. Measured on 2026-09-16 across the scopes of **the eleven RIO applications surveyed** — around 140 scopes — plus a field-by-field comparison on `rio-controlplane-clickhouse` against the deploy screen's own "Productive" badge:

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

### A conflicting deployment may already be the fix

When an active deployment blocks the scope, do **not** stop at "blocked by a conflict". First read what that deployment is shipping: fetch the catalog for its `build` and check whether the component still carries the sunset there. This is the same reasoning as the in-flight check for pull requests, applied to deploys.

- **The in-flight build already resolves it** — the right outcome is "someone is already fixing this, wait", not a block. Name the deployment, its build, its branch, and who started it. Say plainly that no redeploy is needed once it finishes, and **do not** re-run to force a deploy on top: that would be redundant work on a scope another person is mid-way through.
- **The in-flight build does not resolve it** — then it is a genuine conflict. Stop, report it as resumable, and never create a second deployment for the same scope.

Verified on `rio-controlplane-kafka`: a Path B redeploy of `test-nonprod` was blocked by an active deployment of `202609.17.0-rc-1` from `release/202609.17.0`, started by another person. That build carries `kafka-clients` 3.9.2 and `mqclient` 3.4.9, neither with a sunset — so it resolves both overdue items on its own. Reporting that as merely "blocked" would have understated it and invited a pointless re-run.

### Two remediation paths: code fix, or redeploy only

Not every sunset needs a code change, and assuming otherwise is why a run can classify everything as "blocked" while the actual fix is trivial. Decide the path **per item**, right after classification:

**A literal version is not proof of the resolved version.** A `resolutionStrategy.force`, a constraint, or a platform/BOM can keep an older version even when the manifest line says the target (reproduced offline in Gradle: manifest `2.0.0`, resolved `1.0.0`, build green). So an item is reported as applied only after the **effective** version is confirmed with the native manager (for example `gradle dependencyInsight` / `dependencies`, or `mvn dependency:tree`) or from the catalog of the new build, and it satisfies `targetVersion`. If it does not, the item is not applied: report it as blocked with the manager that overrides it, and do not deploy on its behalf.

**Path A — code fix.** The manifest supplies a version that does not satisfy the target. Edit, validate, open the PR, create the version from the PR head, deploy to a test scope. This is the path the phases below describe.

**Path B — redeploy only.** The manifest **already** satisfies the target; the sunset appears solely because one or more deployed scopes still run an older artifact built before the code was fixed. There is nothing to edit, so there is no PR. The remedy is to build the current base branch and redeploy the affected scopes.

Verified in practice: `rio-controlplane-clickhouse` reported `java-melitk-secrets` as an expired sunset, and `develop` already declared `1.3.9` — the target — directly in `build.gradle`. The finding came only from stale artifacts in `stage`, `test-events` and `stage-events`. A run that treats that as "blocked" reports a code problem that does not exist.

To take Path B, all of this must hold, and each is checked, not assumed:

1. The manifest on the base branch declares, pins, or otherwise supplies a version that satisfies the target. Read it; never infer it from the catalog.
2. The affected scopes are identified explicitly — the ones whose deployed artifact carries the sunset — and named in the report. Never redeploy a scope that is not affected.
3. Each affected scope passes the **same** scope gate as any deploy: `validate-scope.mjs`, with `criticality` exactly `test`. Productive and stage scopes are reported, never touched.
4. The version is created from the base branch at its current head, with a clean worktree — not from a PR, because there is no PR, and not from an arbitrary commit. The build gate runs against that **base SHA** (`validate-build.mjs --sha <base-sha>`) in place of the PR head SHA that phases 7 and 8 otherwise require, and the effective version of each affected component is confirmed in that build's catalog, as above.
5. The operator confirms explicitly before the deploy, as always.

Report Path B distinctly. Do not call it `applied` — nothing was applied — and do not call it `blocked` either. Say that the code already satisfies the target and which scopes need a redeploy. If every affected scope turns out to be productive or stage, the outcome is `ACTION_REQUIRED` with that stated plainly: the fix is a redeploy that only a human may perform there.

A completed Path B run ends as `REDEPLOY_ONLY` (see the outcomes table): no PR exists, and the summary and report name the base SHA, the build, and each redeployed scope instead of a PR head.

### Check for work already in flight, before touching anything

Run this **in phase 3, before classification and before any edit**. A sunset that someone is already fixing does not need a second fix, and a second fix is worse than none: it creates a competing change, a conflicting pin, and review load for a patch that will be thrown away.

For each eligible item, look for an existing effort covering it:

1. List the repository's open pull requests and read their titles and changed files.
2. List recently built versions in Fury and note which branches they came from. A branch with a run of recent builds is active work, even when its pull request is not obvious.
3. For any candidate branch, read the manifest **on that branch** and check whether the component already reaches the target there. Coverage takes more than one shape, and looking only for a higher version number misses two of them: - the declaration or pin **moves to or past** the target; - the pin is **removed**, handing the version back to a platform or BOM that already supplies the target or better; - an **upgrade of the manager** (platform, BOM, or build plugin) carries the component along.

   All three count. Verified in practice: for `rio-materializer`, open PR #728 covered a `netty-handler` sunset by *deleting* the override that pinned it to `4.2.7.Final`, letting Spring Boot's BOM manage it up to exactly the `4.2.17.Final` the sunset asked for. A check that only looked for the string `4.2.17.Final` in the manifest would have found nothing and called it uncovered.

**The skill's own work is not "someone else's".** The deterministic branch and pull request this skill opened on an earlier run are not work in flight by another person. If the run finds its own PR, it does not stop at `ALL_IN_FLIGHT`: it resumes from the last completed checkpoint (PR open → build → scope → deploy → Finish → report), after re-reading the PR's **current** head SHA and re-running the build gate against it. Only a branch or PR that is not the skill's deterministic one counts as other people's effort.

A failed listing — step 1 or step 2 above returning an error, a timeout, or an empty result because the call itself did not succeed — is **not** evidence that nothing is in flight. Only an empty result from a call that actually succeeded means that. Treating a failed listing as "nothing in progress" is exactly the failure this whole check exists to prevent: it would let the run open a pull request for a sunset someone is already fixing, the "competing change" this section opens by warning against. A failed listing stops the run as a block, the same way a failed existence check or a failed scopes read does elsewhere in this document — it is never silently read as a green light to proceed.

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

Observed deployment `status` progression for a successful run: `effective` → `finishing` → `finished`, with `active` flipping to `false` at the end. `waiting_application` also occurs, early, while instances are still coming up — it is a normal in-progress state, not a stall. `rollbacked` also exists. Never treat an unlisted status as terminal: an unrecognized value means keep polling or stop and report, never assume success. Step statuses: `pending`, `running`, `completed`, with `RUNNING`/`FINISHED` on targets. `signals` reports granular progress: `containers_started`, `booted`, `application_up`, `sidecars_up`, `swapped_in`, `receiving_traffic`, `swapped_out`, `created`, `failed_instances`, `failed_swapping_in`.

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
- **A value that comes back redacted is a value that was not read.** Tooling that scrubs secrets can match on shapes that are not secrets: observed in practice, version strings like `202608.4.2` were returned as `[BLOCKED: JWT token]` by a false positive on dotted numeric strings. Never use, parse, or compare a value that arrived redacted, truncated, or otherwise altered, and never reconstruct what it "probably" was. Either obtain it cleanly — for instance by transforming the string before reading it back — or stop and report the field as unreadable. A silently mangled version is worse than a missing one: it produces a comparison that looks successful and is wrong.

## Normalized sunset-item contract

Each source item must contain all of the following, validated as typed data before use:

| Field | Source field | Requirement |
| --- | --- | --- |
| `sunsetId` | `dependencies[].issues[].id` | Stable non-empty identifier. |
| `component` | `dependencies[].name` | Affected component or dependency identifier. |
| `technology` | `dependencies[].technology` | Used to pick the project's own dependency manager, never to build a command from source data. |
| `project` | request path `{app}` | Exact application name as supplied and confirmed against Fury. Reject any item whose application differs. |
| `sunsetAt` | `issues[].use_sunset`, cross-checked against `dependencies[].sunset_use` | ISO-8601 instant. Reject a mismatch between the two. |
| `currentVersion` | `dependencies[].version` | Exact current version. |
| `targetVersion` | version parsed from `issues[].upgrade_to` purl | Exact recommended target version; never `latest`, never inferred from prose. |
| `severity` | `issues[].severity` | Reported, never used to skip a gate. |
| `evidenceReference` | artifact-details URL + `issues[].reason` | Stable source reference sufficient for PR review. |

Reject missing, ambiguous, malformed, or cross-project data. Do not print raw source responses or authentication material.

Passing external values as separate process arguments does not by itself prevent option injection: a value such as `--upload-pack=…` is still interpreted as a flag. Therefore `sunsetId`, `component`, `currentVersion`, and `targetVersion` must additionally match `^[A-Za-z0-9][A-Za-z0-9._@/+-]*$`, any value beginning with `-` must be rejected, and `--` must precede all data-derived arguments in every command.

## Phases and resumability

1. **Input gate (no network/mutation):** run `node skills/rio-sunset-update/scripts/validate-input.mjs <project_name>`. It accepts exactly one slug-formed project and at most the one literal flag; it does **not** check existence. Any error stops here. Existence is the first network step of phase 2 — see "Validar el proyecto contra Fury".
2. **Preflight:** obtain the checkout as described in "Obtaining the project checkout" below, then verify its identity equals the supplied project and that `git status --porcelain` is empty. Check existing code-host and Fury authentication non-interactively only. Missing or expired credentials stop the affected external phase; never invoke login and never ask for a password, token, or verification code.
3. **Discovery — query at the application level, across segments.** Do **not** discover from a single artifact version. Each deployed scope runs its own version with its own dependency set, so a version-scoped read silently misses sunsets that exist elsewhere in the application. Verified on 2026-09-17 for `rio-controlplane-clickhouse`: reading the catalog for the latest version found **5** dependencies with sunsets, while the application-level view returned **9** — and the ones missed included an **already-expired** sunset (`java-melitk-secrets` 1.3.3, due 2026-07-31) plus a second, older instance of a component already found at a different version. The version-scoped read looked complete and was not.

   Use the aggregated endpoint, passing every segment the application has, and paginate to completion:

   ```text
   GET /api/proxy/dependency_catalog_v2/applications/{app}/dependencies
       ?pageNumber=1&size={n}
       &filter_by=with-sunsets:true
       &filter_by=segment:{each segment}
   ```

   Its companion `.../dependencies/summary` returns the counts the UI shows — `With sunsets`, `Reached sunsets`, `Critical/High/Medium issues`. **Use those counts as a cross-check**: if the number of items discovered does not match `With sunsets`, discovery is incomplete and the run must stop rather than proceed on a partial set. `Reached sunsets` is the count of already-expired ones, and a non-zero value there must never come out of a run reported as having nothing to do.

   Each item carries `name`, `version`, `technology`, `sunset`, `sunset_add`, `suggested`, `latest`, `status`, `banning` and `issues_summary`. The same component can appear more than once, at different versions, because different scopes run different artifact versions — treat each as its own item and deduplicate only on an exact `(component, version, target)` match, never on component alone.

   **Never take the target version from the `suggested` field.** It looks like a target and is not one: it is a free-text remediation note, and it sometimes carries prose instead of, or mixed with, a version. Observed on `rio-controlplane-kafka`:

   ```text
   suggested = "pkg:maven/org.apache.kafka/kafka-clients@3.9.2"
   suggested = "This version has a memory leak bug;  | 1.1.1"
   suggested = "A client application is experiencing memory leak issues related to this SDK
                version. While still under investigation, we have decided to release a new
                version containing a feature that allows reverting to the default compression
                implementation if needed;  | 3.4.8"
   ```

   The version is sometimes there, after a `|`, and sometimes the whole string is a sentence. Parsing that is exactly the "derive the target from prose" failure this skill forbids. Take the target only from `issues[].upgrade_to`, which is a structured purl. `suggested` may be quoted in the report as context for a human, never used as a value.

   For the per-issue detail behind an item, the version-scoped catalog is still the right read, paginating with `page`/`size` until `page.total` is covered. Enumerate **every** dependency that carries a sunset date — never stop at the first, and never sample: paginate the catalog to completion before filtering. A dependency may carry several issues, so collect all of them. Then keep the ones whose `upgrade_to` yields a valid target version. At runtime, eligibility has **only an upper bound**: every sunset due on or before the end of `current day + 14 days` is eligible, counting the execution date itself as day 1, in an explicitly displayed IANA timezone and offset. **There is no lower bound — already-expired sunsets are eligible too, and they come first.** A sunset whose date has passed is not stale news: it is already blocking builds of that project, so it is more urgent than one still approaching, not less. Compute the horizon per execution; never persist it and never schedule it.

   **Ask the operator for the horizon — after discovery, not before.** Discovery is read-only, so run it first over *every* sunset the application has, then ask with the real counts in hand. A blind question is worth less than an informed one:

   > Found 9 dependencies with sunsets: **1 already expired**, 2 due within 15 days, 6 later. > Which do you want to update? > 1. Expired + next 15 days (recommended) > 2. All open sunsets, whatever the date > 3. A different horizon — how many days?

   Rules for that question:

   - **Already-expired items are never optional.** They are in every choice, because their builds are already blocked. The question only moves the *upper* bound. - Ask every run. **Never store the answer as a default**, and never carry it between runs. - State the resulting horizon date explicitly once chosen, and record it in the plan, the pull request and the report, so a reader knows what was considered and what was not. - If the chosen horizon yields more than a handful of applicable items, say so and confirm before proceeding: they all land in **one** pull request, and a very large batch is harder to review and riskier to revert than the deadline pressure usually justifies. - If the operator is not available to answer, use expired + 15 days and say that the default was applied. Never silently widen the horizon.

   Sort each eligible item into one of two buckets, and carry the label through the plan, the pull request and the report:

   | Bucket | Condition | Meaning | | --- | --- | --- | | `overdue` | date is before the start of the current day | The deadline already passed; builds using this library are already blocked. | | `due` | date falls from the start of today through the end of day 15 | Approaching. |

   Both buckets go into the same batch and the same pull request. List `overdue` items first, everywhere they appear, so a reader sees what is already broken before what is about to break. Anything due after day 15 stays out of the batch and is reported for visibility only. Deduplicate by `(sunsetId, component, targetVersion)`. Zero eligible items is a complete no-op: no branch, PR, deploy, or report.

   A run processes the **entire eligible set for the project as one batch**. It never iterates one sunset at a time into separate branches or separate pull requests. If two issues on the same component resolve to different targets, keep the highest target that satisfies both and record both issue IDs against it; if they conflict irreconcilably, exclude that component from the batch and record it as blocked rather than guessing.
4. **Plan and update:** show the normalized plan and evidence before mutation. Resolve the dependency manager and validation commands from versioned configuration in the checked-out project, not from this registry or source data. Pass all validated values as separate process arguments; never concatenate shell strings. Limit changes to manifests, lockfiles, and migrations directly required by eligible items.

   Before editing anything, classify how the project actually supplies the component. A sunset component is frequently **not** declared in the manifest, so a version string rewrite is invalid and must not be attempted blindly. The classification decides the outcome:

   | Case | How it appears | Action | | --- | --- | --- | | Declared directly with a literal version | an explicit dependency line naming the component and version | Bump that single line to `targetVersion`, then confirm the **effective** version (see below). | | Managed by a platform/BOM the project declares | the component is absent, but a BOM or platform artifact is declared | **Stop and report.** Reaching `targetVersion` requires a BOM bump whose blast radius is not confined to this component. | | Managed by a build plugin's dependency management | the component is absent and its version tracks a plugin's release train | **Stop and report.** Reaching `targetVersion` may require a major plugin upgrade, which is not a mechanical change. | | Overridable by a documented pin the project already uses | the project already demonstrates an override idiom for managed versions | Propose the override, but apply it only after explicit human approval, because an override silently diverges from the managed set. | | Purely transitive with no declaration or override | none of the above | **Stop and report.** |

   Only the first case is applied automatically. Never invent a declaration, never add a component that the project did not declare, and never substitute a different version from the one the source states.

   A blocked item must be **actionable without further digging**. "Managed elsewhere" is not a finding; naming what manages it is. For every blocked item, read the project's own manifest and record: the managing artifact (the platform, BOM, or build plugin), its currently declared version, and the literal manifest line that declares it. Add the override idiom the project already demonstrates, if it uses one, quoting the existing example rather than inventing syntax. The reader should be able to go straight to the decision — bump the manager, pin an override, or wait — without reopening the build file to find out who is in charge.

   Record the manager from the manifest only. Never guess which release train carries the target version, never assert that a particular manager version would resolve the sunset, and never state a compatibility claim that was not verified. If the manifest does not make the manager identifiable, say exactly that instead of inferring one.

   Classify **every** item in the batch before editing, then split the set in two: `applied` and `blocked`. Apply all `applied` items together in one working set, so a single batch carries every mechanically safe update. A `blocked` item never stops the batch — it is carried into the PR body and the report with its classification and evidence, so the run still delivers the safe updates while making the human decisions explicit. If the batch has **no** `applied` items, the run stops after this phase with the classification report and opens no PR.
5. **Validation:** confirm first that the project's toolchain can actually run here — the build tool at the version its wrapper pins, the required language runtime, and reachable dependency registries. **Validation that cannot be executed is not a pass.** If the toolchain or the registry is unavailable, stop with `VALIDATION_UNAVAILABLE`, keep the edit uncommitted, report which capability is missing, and do not open a PR; do not fall back to reasoning about whether the change looks safe. Then run the project's defined build, tests, lint, and/or typecheck **once over the whole batch**, and inspect the diff. Any failure blocks commit, push, PR, and deploy for the entire batch; never silently drop the offending item and retry, because the remaining set was validated only in its presence. Report which item the failure implicates so a human can exclude it deliberately and re-run. An empty diff is a no-op.
6. **Branch and PR — exactly one per project:** the branch name derives only from the validated project name, never from the item set or the date, so every run for a project lands on the same branch and reruns are idempotent. **Read the prefix convention from the repository instead of choosing one**: list the existing remote branches and use the prefix the project actually uses. In the verified case that prefix was `feature/`, and it is not cosmetic — the project's Fury builds run under `gitflow`, where `tags.branch_type` is derived from the branch prefix, so an unrecognized prefix such as `chore/` can mean no build is produced at all, which in turn means no immutable build to bind and no deploy. Prefix wrong, flow dead. Before creating anything, look for an open pull request from that branch for this project:

   - **An open PR exists:** reuse it. Add only the items it does not already cover, and regenerate its body so it describes the full current set. Never open a second PR for the same project. - **No open PR exists:** create the branch and open one PR.

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
3. **If the operator has no local clone**, ask a single explicit question: clone it, or stop? - **Declines** — stop immediately, reporting that the run cannot continue without a checkout of the project. This is a clean no-op: nothing was read, edited, branched, or deployed. - **Accepts** — ask for the destination directory. Never pick one, never default to the current directory, and never reuse the directory holding this skill.
4. **Clone**, with these constraints: - The clone URL comes from the Fury application's GitHub sidebar link, which is authoritative. Never use the `repository` field from the dependency-catalog API: it was observed pointing at a stale organization. - The destination must be an empty or non-existent directory. Never clone over, into, or on top of existing content, and never delete anything to make room. - Authentication is non-interactive only. If the existing credential is missing or expired, stop and report it; do not start a login flow and do not accept a token from the operator. - Pass the project name and destination as separate process arguments, already validated by the input gate, with `--` before data-derived arguments.
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

Upload the report as a native Google Doc, not as a raw `.md` file. A markdown file sitting in Drive is unreadable as a document — no headings, no tables, no formatting — and is not what "goes to Drive" means here. Convert on upload (`mimeType: application/vnd.google-apps.document`, or the client's equivalent conversion option) so the result opens as an editable Doc with the report's headings, tables, and links rendered, titled the same as the local filename minus the `.md` extension. The local `.md` file on disk is unaffected either way — this only changes the format of the Drive copy. Use whatever Google Workspace connector or skill the operator's environment already provides for creating Docs and uploading with conversion, rather than hand-rolling the Drive API call.

**When Drive access is not configured:** ask whether the operator wants to configure it.

- **Yes** — give the step-by-step for their client and **wait** for them to finish, then re-check and proceed with the folder logic above. Never attempt the authorization flow on their behalf, and never ask for a credential, token, or authorization code.
- **No** — write the local file only. Say so plainly in the final summary and show the absolute path, leaving the operator to decide what to do with it. This is a normal outcome, not a failure, and it never blocks the run.

An expired or failing connector is treated the same as "not configured": the local file still exists, and the upload is reported as the only thing that did not happen.

## Failure and resumption matrix

| Checkpoint | Failure behavior | Safe resume point |
| --- | --- | --- |
| Input shape | No network or mutation | Re-run with one slug-formed project. |
| Project unknown to Fury | No checkout, branch, or edit | Re-run with the name Fury spells, once confirmed. |
| Source / credentials | Preserve local state; no login | Re-run after a documented source or existing credential is available. |
| Checkout / worktree | No edits | Clean or select the correct checkout manually. |
| No eligible items / empty diff | No branch, PR, or deploy | Re-run when source data changes. |
| Update / validation | No commit, push, PR, or deploy | Correct only required files, then revalidate. |
| Classification: no applied items | No branch or PR; blocked items reported | Decide the BOM/plugin bumps by hand, then re-run. |
| Branch / PR | Reuse the project's single deterministic branch and its open PR | Re-run; the existing PR is updated, never duplicated. |
| Build / scope | No deploy | Re-run after exact build or valid test scope exists. |
| No scope at all (library) | Not a failure: PR stands, deploy skipped | Nothing to resume; consumers verify on upgrade. |
| Active deploy / conflict | Do not create another deploy | Monitor or resolve the existing deployment externally, then re-check. |
| Report write / upload | Deployment already happened; do not repeat it | Re-emit the document from recorded phase results only. |

## Migration attempt mode — `--attempt-migration`

An opt-in mode for the case the default run can only report: a sunset whose target is governed by a BOM or build plugin, where reaching it means upgrading the manager. The default flow never does this, because the blast radius is not confined to the component. This mode attempts it anyway, under a hard cap, and **never deploys**.

**When it may run.** Only when the default classification found at least one manager-governed item for the project. If there is nothing of that shape, refuse and say so — there is nothing to attempt. Ask for explicit confirmation before the first attempt, stating that it will create up to three real builds.

**The loop, capped at three attempts. The cap is hard.**

1. Change the manager's declared version toward what the sunset requires — the plugin or BOM version, read from the manifest, never invented.
2. Create the version and monitor it as phase 7 does.
3. `FINISHED` → stop the loop, go to "What it delivers" below. Any other terminal state → diagnose, apply one further change, and go back to step 1.
4. After the third failure, stop. **Never ask for three more, never raise the cap, never restart the mode in the same run.** An uncapped loop with a human approving each round is an uncapped loop.

**Diagnosis, with honest limits.** What is verified as readable from the version record is `tags.stage` (the stage that failed, such as `install_dependencies`) and `tags.type_error` (such as `user_error`). Combined with the registry check and the manifest, that is enough for coarse diagnosis — it was enough to identify a non-existent target version. It is **not** enough for source-level failures. Richer detail lives in the build logs, whose access requires a separate authentication and **has not been verified**. Until it is, say in the report which failures could only be classified coarsely, rather than implying a precise diagnosis.

**What it delivers.**

The pull request is always a **draft**, whose title and body state plainly that the change is unverified and that merging is a human decision. That never changes. What depends on the build is everything after it:

- **The build failed** — no deploy. Nothing is deployed on the strength of a build that did not finish. Continue to the next attempt, or stop if the third one is spent.
- **The build finished** — the run **completes every remaining phase, exactly as the normal flow does**: the scope gate, the explicit confirmation, the deploy to test, monitoring to a stable state, and `Finish` to release the scope. Deploying to a test scope is how runtime breakage in a framework migration gets found, and refusing to do it would leave a draft nobody can evaluate. Only a productive scope stays out of reach, and the scope gate already guarantees that.

  Say plainly in the report that the migration builds and runs in test, and that **this is not proof it is production-ready**: a green build plus a healthy test scope does not cover every runtime path. The merge decision stays with a person.

- After three failures, outcome `MIGRATION_UNVERIFIED`, and the final document must say, in its own words and without softening:

  > No fue posible completar la actualización. Se hicieron 3 intentos y los 3 fallaron. Esta no es > una actualización de versión: es una migración crítica que necesita atención humana dedicada.

  followed by, per attempt: the change made, the stage that failed, the `type_error`, and whether the diagnosis was precise or coarse. The value of a failed run is the map of obstacles it leaves.

Never present a capped-out migration as progress, and never let it block the deadline reporting the default run would have produced: the sunset is still unresolved and still has a date.

## Naming the outcome: "no pull request" is not one thing

Several very different results all end without a pull request, and they must not read alike. A run that found an unhandled deadline expiring tomorrow looks, in a careless summary, exactly like a run that found nothing — and the first one needs a person today.

State the outcome as one of these, by name, in the first line of both the summary and the report:

| Outcome | What happened | Needs a human? |
| --- | --- | --- |
| `NOTHING_ELIGIBLE` | No sunset falls on or before day 15. | No. |
| `ALL_IN_FLIGHT` | Every eligible sunset is already being fixed by someone. Name them. | No. |
| `ACTION_REQUIRED` | Eligible sunsets exist, are **not** covered by anyone, and cannot be updated mechanically. | **Yes — this is the loud one.** |
| `APPLIED` | A pull request was opened with the applied batch. | Review it. |
| `REDEPLOY_ONLY` | Path B finished: no PR was needed, the build from the base SHA was validated, and the affected test scopes were redeployed. | Review the report; productive and stage scopes still need a human. |
| `APPLIED_NO_DEPLOY` | A pull request was opened, and the project has **no** scope to deploy to — a library or SDK. | Review it; consumers verify on upgrade. |
| `STOPPED` | A gate failed or a capability was missing. Name the gate. | Yes. |
| `MIGRATION_UNVERIFIED` | `--attempt-migration` used all three attempts and none finished. | **Yes — critical.** |

A migration attempt whose build finished ends as `APPLIED`, like any other completed run — the mode is recorded, and the draft-and-unverified caveat travels with it. There is no separate "green but stopped" outcome, because a green build means the run continues.

`ACTION_REQUIRED` is the outcome most likely to be misread as harmless, so it carries the most weight. When reporting it, lead with the nearest deadline and whether it has already passed, say plainly that nobody is working on it, and give the classification and the named manager so the reader can act without re-deriving anything. If any such item is `overdue`, or falls within a couple of days, say so in the first sentence.

Never let a blocked item be reported as though the run had nothing to do. "Nothing I can safely automate" and "nothing that needs doing" are opposite results.

`APPLIED_NO_DEPLOY` exists for the same reason: without it, a library run would have to borrow either `APPLIED` — claiming a test deploy that never happened — or `STOPPED`, which reads as a failure and would send someone looking for a scope that does not exist. Keep the two facts together in one sentence: the change was applied, and nothing was deployed because there is nowhere to deploy it.

## Required final phase summary

Report discovery, update, validations, branch/PR, build, deploy, and report separately. Report only identifiers and safe metadata; never record credentials, tokens, or raw sensitive responses.

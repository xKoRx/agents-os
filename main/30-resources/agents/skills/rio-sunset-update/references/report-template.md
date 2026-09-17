# Rio sunset update — run report

Fill every field from values observed during the run. Never emit a planned, assumed, or placeholder PR, scope, or deployment ID. If a phase stopped early, replace that phase's values with its stop reason. A run with no eligible sunsets produces no report at all.

- Project (exact Fury application name): `<project>`
- Executed at: `<ISO-8601 with offset>`
- Window evaluated (inclusive, execution day counts as day 1): `<start ISO-8601 with offset>` through `<end ISO-8601 with offset>`
- Timezone used: `<IANA timezone and offset>`
- Run outcome: `<completed | stopped at phase N>`

## Mapped sunsets

Every sunset found inside the window, whether or not it could be updated.

| Sunset ID | Component/dependency | Expiry date | Previous version | Target version | Outcome | Managed by | Evidence reference |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<id>` | `<component>` | `<expiry ISO-8601 with offset>` | `<previous>` | `<target>` | `applied` or the blocking classification | `<managing artifact @ declared version, for blocked rows>` | `<reference>` |

## Ya en curso — excluidos del lote

Eligible sunsets that another effort is already resolving. Listed so the reader can see they were seen and deliberately skipped. These were not edited, committed, or counted toward opening a PR.

| Sunset ID | Component/dependency | Expiry date | Handled by | That work sets it to |
| --- | --- | --- | --- | --- |
| `<id>` | `<component>` | `<expiry>` | `<PR number or branch>` | `<version>` |

## Sunsets con fecha fuera de la ventana

Informative only, so nothing dated is invisible to the reader. These were found in the catalog but fall outside the evaluated window, so this run did not act on them. List every one; do not truncate.

| Sunset ID | Component/dependency | Expiry date | Current version | Target version | Days until expiry |
| --- | --- | --- | --- | --- | --- |
| `<id>` | `<component>` | `<expiry>` | `<current>` | `<target>` | `<n>` |

## Pull request

One pull request carries the whole applied batch for this project.

| Field | Value |
| --- | --- |
| Pull request | `<pr url or number>` |
| Reused an existing open PR | `<yes | no>` |
| Base branch | `<base branch read from the repository>` |
| Applied sunset IDs | `<ids>` |
| PR commit SHA | `<sha>` |
| Immutable build for that SHA | `<build id>` |

- Files changed: `<files>`
- Native project commands executed: `<commands from versioned project configuration>`
- Validation results: `<build/tests/lint/typecheck>`

## Test deployment

| Field | Value |
| --- | --- |
| Scope requested by the operator | `<scope>` |
| Scope `criticality`, as resolved read-only | `test` |
| Scope ownership check | `belongs to <project>` |
| Contradicting signals found | `none` |
| Pipeline ID | `<pipeline id>` |
| Deployment ID | `<deployment id>` |
| Version deployed | `<build>` |
| Pipeline final state | `completed, 100%` |
| Deployment final state | `finished`, `active: false` (scope released) |
| Finish pressed | `yes` |

No production deployment, promotion, finish, terminate, or auto-merge was performed, and no default scope was stored.

## Destino del documento

| Field | Value |
| --- | --- |
| Local path | `<absolute path>` |
| Drive | `uploaded to "Sunsets history"` / `folder created and uploaded` / `not configured, local only` / `operator declined` |

## Notes and blocks

- `<phase-by-phase notes, stop reasons, or "none">`

Never include credentials, tokens, or raw source responses in this document.

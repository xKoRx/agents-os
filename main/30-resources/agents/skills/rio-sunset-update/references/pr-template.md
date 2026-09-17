## Rio sunset update

- Project: `<project>`
- Query window: `<start ISO-8601 with offset>` through `<end ISO-8601 with offset>` (inclusive)
- Source status: `<verified | blocked>`

This pull request carries **every** applied sunset update for this project in one batch. There is
at most one open sunset pull request per project; reruns update this one rather than opening another.

### Applied in this PR

| Sunset ID | Component/dependency | Sunset date | Previous version | Target version | Evidence reference |
| --- | --- | --- | --- | --- | --- |
| `<id>` | `<component>` | `<date>` | `<previous>` | `<target>` | `<reference>` |

### Found but not applied — needs a human decision

These are inside the window but are not declared with a literal version in the manifest, so no
mechanical update exists. Each row states why.

| Sunset ID | Component/dependency | Sunset date | Current version | Target version | Classification | Managed by (artifact and declared version) | Evidence reference |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<id>` | `<component>` | `<date>` | `<current>` | `<target>` | `<managed by BOM / managed by build plugin / transitive only / conflicting targets>` | `<managing artifact @ version, as declared in the manifest, or "not identifiable from the manifest">` | `<reference>` |

For each row, quote the manifest line that declares the manager, and the project's existing
override idiom if it has one. Do not assert which manager version would resolve the sunset unless
that was verified.

### Already in flight — excluded from this PR

Eligible sunsets that another effort is already resolving, so this PR leaves them alone.

| Sunset ID | Component/dependency | Sunset date | Handled by | That work sets it to |
| --- | --- | --- | --- | --- |
| `<id>` | `<component>` | `<date>` | `<PR number or branch>` | `<version>` |

### Change and validation

- Files changed: `<files>`
- Native project commands executed: `<commands from versioned project configuration>`
- Results: `<build/tests/lint/typecheck>`
- PR commit SHA: `<sha>`
- Immutable build identifier for that SHA: `<build>`

No deploy is requested by this PR. A separate, explicit test-scope selection and final confirmation are required after the immutable build is ready.

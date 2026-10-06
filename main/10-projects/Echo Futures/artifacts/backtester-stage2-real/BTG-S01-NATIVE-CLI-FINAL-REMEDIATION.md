# BTG-S01 Native CLI Final Remediation

## Status

Local scoped verification passed on `codex/btg-s01-native-cli-final-remediation` at `e63254875b84b9ebe91b26ca138bb5c19843113a`, based on `6ef303f57739f0b2a44288f387b377d145eeceac`. The source branch is pushed and clean; a docs-only verification commit `a8e85129856b9ff2602e8e230b35b1d20684b927` follows it. Independent TOP review returned `REMEDIATION_REQUIRED_EXACT_ONCE_GATE`: it confirmed a separate F11 LOW close-forwarding issue requiring one fresh worker. The review independently passed sealed-failure reproduction and byte equality against legacy source `198f29f44bc6e58dd445c9a9b5ee1adfdade2ae9`; those results belong to the reviewer, not this worker. This is a reference-only code remediation; original Windows history was not transferred, `REAL_RUN=NOT_RUN`, and no historical owner acceptance or historical finding closure is claimed.

## Scope and change

The change addresses only F09 owned-cursor cleanup and F10 preparation scope language. After `NewRun` accepts a native source cursor, an early spool-directory error previously returned without closing that CLI-owned cursor. The CLI now closes the cursor on error returns from native run and reproduction. It does not invoke `Finish` on this error path. On normal completion, ownership is relinquished immediately after the existing single `Finish` call. If cleanup also fails, error wrapping preserves both the initial operational error and the cleanup error for `errors.Is`/`errors.As` inspection.

Preparation scope now explicitly says it does not adjudicate source authenticity. `OHLC_1M_MODEL_V1`, the no-adds functional baseline, caller-controlled horizons, the `AvailableAt` boundary, and BBO/live-parity limits are retained. No Strategy, GerardMM, risk, or shared engine changes were made.

## Verification evidence

- Exact public `run` and `reproduce` blocker cases were RED on the base: each left one extra snapshot descriptor. The permanent Linux `/proc/self/fd` regression is green on the fix and contains no runtime skip. Normal `Finish` closure, error-cause preservation when close fails, sealed-artifact/source-integrity checks, and the F10 contract are covered by directed tests.
- Directed cleanup/scope and applicable CLI routing/pipeline/source-fold tests passed; F08 account-day identity cases passed under `-race`; `go vet ./v3/backtester/cmd/echo-backtest` passed.
- Changed-production-block coverage is 42/42 (100%), no exclusions. Raw whole CLI package coverage was 66.1%; it is not presented as changed-block coverage. Audit: `/home/kor/aranea/work/btg-s01-20261006/reports/native-cli-final-remediation/cli-probes/changed-production-coverage.json`, profile SHA-256 `221b02af1fd0094b6382682f4ae1712a6359ca80d54d071cf2603b4da6679ac6`.
- The default-GC (`GOGC=100`) fresh-process synthetic E2E passed prepare, complete run/reproduce, sealed incomplete run/reproduce and source-identity/mixed-source rejections. It then stopped in the test's final frozen-baseline build: inherited `GOWORK` omitted the temporary `git archive` module. This is **partial / no pass for the whole E2E**; the final comparison in this attempt was not reached. A direct `GOWORK=off` build also fails because this checkout's backtester module has no `go.sum`. Logs: `/home/kor/aranea/work/btg-s01-20261006/reports/native-cli-final-remediation/cli-probes/fresh-process-e2e-gogc100.log` and `fresh-process-e2e-gogc-off-timeout.log`. No further E2E retry was run.
- Independent TOP review report: `/home/kor/.codex/worktrees/btg-s01-native-cli-final-remediation-review-record/main/10-projects/Echo Futures/artifacts/backtester-stage2-real/BTG-S01-NATIVE-CLI-FINAL-REMEDIATION-REVIEW.md` (SHA-256 `beaa7514acf6cb51fc33d7a97d7fe26759b47b9f6e379795607d5ddf0b217ba6`). It records the separate F11 LOW exact-once close-forwarding issue; the coordinator has dispatched a fresh worker. Its legacy byte-equality pass is independently attributed and does not change this worker's `FAILED_HARNESS` E2E status.

All executions used synthetic fixtures and remain `REFERENCE_ONLY`. The S2/MM code path is the shared implementation; fixture provenance is synthetic and is not the original Windows corpus, a performance baseline, or a historical adjudication.

## Offline command templates

Run from `v3/backtester`. Use the repository's actual workspace and offline module cache to build:

```sh
env GOPROXY=off GOSUMDB=off GOFLAGS=-mod=readonly GOWORK=<explicit-worker.go.work> \
  go build -o <cli-binary> ./cmd/echo-backtest
```

These are templates, not executed historical commands or run IDs. The caller must supply and adjudicate the exact contract, build, source descriptor, and horizons from the original files; no defaults are inferred.

```sh
<cli-binary> prepare-functional-nt --input <explicit-input.json> --out <prepared-dir>
<cli-binary> run --spec <prepared-dir>/runspec.json --nt-source-config <descriptor.json> --out <artifact-dir>
<cli-binary> reproduce --result <actual-artifact> --nt-source-config <descriptor.json> --out <rerun-dir>
```

`prepare-functional-nt` accepts the explicit input and output paths. `run` consumes the prepared `runspec.json`; `reproduce` consumes an actual sealed artifact. No actual historical run was performed.

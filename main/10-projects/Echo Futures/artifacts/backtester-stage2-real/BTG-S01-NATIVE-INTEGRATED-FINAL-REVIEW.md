---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
project: "[[Echo Futures]]"
related:
  - "[[Echo Futures]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01 Native Integrated Final Review

## Propósito

Independent TOP LOCAL one-shot final review of frozen native CLI plus the F08 account-day correction. **Verdict: REMEDIATION_REQUIRED** for BT2-F09 MEDIUM and BT2-F10 LOW. F08, byte-exact integration, bounded critical domain behavior and coverage gates PASS. ROOT owns handoff to a fresh NORMAL remediation worker; this reviewer made no product edits.

Reviewed source `198f29f44bc6e58dd445c9a9b5ee1adfdade2ae9`, branch `codex/btg-s01-native-cli`; producer's later `6ef303f57739f0b2a44288f387b377d145eeceac` adds verification documentation only. Detached review target remained clean. Independent F08 source `171fc712e56d731493befeef5c54a2620f25d31a`; reference C `e2e15a3559034a3ed08c04f247baf4919e20b2ff`. SDK `407e03dd` and native adapter `e44b741e` are accepted dependencies, not newly adjudicated here.

Scope is local synthetic/reference evidence. No Owner acceptance, historical finding closure, acquisition, profitability, campaign, FUNDED/scaling, live equivalence, trading, D6/infra/ACL or canonical master mutation. Actual 13 NT exports were inventoried, but full transfer remains POLICY_DENIED and original corpus NOT_ACQUIRED; historical SMOKE/LONGIT/RERUN remain NOT_RUN.

## Contenido

### Findings requiring remediation

| ID | Severity | Trigger and observation | Required behavior / owner |
|---|---|---|---|
| BT2-F09 | MEDIUM | Public `cmdRun` with valid native spec/descriptor and an ordinary file blocking `out/<RunID>` opens a cursor, then returns the original spool-create error. Immediately one extra unlinked snapshot FD remains. Public `cmdReproduce` from a valid sealed native artifact reproduces the same path. | Close the owned cursor before returning after successful `NewRun`, preserving the original error. ROOT assigns a fresh NORMAL CLI worker; observed locations `cmd/echo-backtest/run.go:110–112` and `reproduce.go:306–308`. |
| BT2-F10 | LOW | Prepared manifest Scope omits the explicit source-authenticity boundary required by frozen CLI SPEC line19. | State that preparation does not adjudicate source authenticity in Scope. Preserve `OHLC_1M_MODEL_V1` Fidelity, NO_ADDS and the existing horizon/BBO/LIVE disclosures. ROOT assigns the same fresh worker. |

F09 proof is narrowly about ownership at return. Native adapter unlinks its private snapshot before exposing the cursor; no persistent named snapshot file was observed. Standalone CLI process exit closes FDs; Go finalization may close them later. `GOGC=off` isolates immediate ownership: snapshot FD count 0→1 after run, then 1→2 after reproduce; named private paths remained empty. Normal `Finish` closes its own cursor. This is an inherited early-return pattern newly carrying native snapshot resources, not a claim of permanent disk leakage or wrong financial result.

Constructor inspection and the changed-source probe did not reproduce a `NewRun` constructor leak: composition validation precedes cursor opening, and `openDatasetCursor` is its last step. Native `Open` cleans the snapshot on failed receipt validation. No shared constructor/ResultWriter API change is justified by this evidence. Writer/install/admission failures share suspicious early-return structure but were not independently exercised and are not additional reproduced findings.

F10 actual Scope: `FUNCTIONAL_NO_ADDS_BASELINE; WARMUP_IS_CALLER_SUPPLIED; coverage.from_is_first_available_at_and_prior_interval_is_not_included; NOT_OBSERVED_BBO_OR_LIVE_PARITY`. Missing sentence: preparation does not adjudicate source authenticity. This is metadata/SPEC nonconformance; OHLC fidelity does not imply auto-REAL and no false historical execution was inferred.

### F08 independent result and immutable integration

Same exact break slice on reference C fails native and legacy with `ACCOUNT_DAY_FAILED` at `2026-10-05T22:00:00Z`; fixed171 passes both. Warmup `2026-10-05T20:59:00Z` lies within previous17→current17 Chicago account-day interval. The source gap21→22Z is the legitimate16→17 break, not missing session coverage. Actual initial observation remains Warmup; natural reset remains22Z; Plan ordinal IDs and ledger IDs stay separate, no warmup ordinal or operation is created. Initial account-day balances/day PnL/traded-operation count/inventory are independently asserted.

Before/at/after17, year transition, 23h/25h DST days using civil boundaries, EndExclusive no-reset, selector/config mapping, invalid timezone visibility and zero warmup operation issuance PASS. Calendar-only long boundary probes place TradeStart at EndExclusive−1ns; they are not S2 readiness evidence. Directed S04 transitions/cashflow, Driver/Plan DST, selector, native closed-sequence and late-control paths PASS under race.

Valid legacy UTC00 and after-Chicago17 result+record byte oracles are unchanged from C: UTC00 678137 bytes SHA256 `ccb6ea20de11d53b0bc7fa6c15c84f31068d4445dd13edcb193b964c939a958b`; after17 678131 bytes SHA256 `1e876c3f557b631f04f7a381e480b574107ea21c9919e401491b87fe4f99fadc`.

All six F08 files equal171 byte-for-byte in198f: `v3/backtester/run.go`, new `account_day_identity_regression_test.go` and four account-day SDD files. SDK/core, native adapter, simexecution, OHLC driver, market context and functional profile boundaries remain byte-exact to C. Hash inventory is external `integration-proof.json`; no inferred equivalence or merge/cherry provenance substitute.

### CLI boundaries and meaningful domain evidence

Descriptor decoding is closed, rejects unknown fields/trailing documents and requires corpus/version/durable reference/timestamp convention plus explicit stream/path/tick bindings. Physical relocation and a deliberately misleading ES filename preserve logical NQ identity when bytes and explicit binding match. Post-factory receipt mutation fails visibly with `SOURCE_CHANGED`. Full corpus/version/durable/digest identity is checked before `NewRun`; native/legacy mixed routes reject and do not fall through.

Preparation uses shared FunctionalNQEvalSpec, explicit Build/contract/horizon and one selected NQ physical stream. Real NQ tick0.25 and point20 USD, SIM100k EVAL uniform2000/1500, NO_ADDS, fee2.49, one adverse slippage tick and modeled bid/ask1/1, Chicago17 weekly calendar remain unchanged. Observed From is first AvailableAt; exact caller Warmup is retained and the preceding interval is explicitly omitted under existing V1 coverage, with no auto-shift or holiday/roll inference. Manifest logical/physical receipts, raw discontinuities and config/model/calendar/profile digests were inspected.

Independent fresh-process real shared S2/GerardMM synthetic long stop scenario PASS129.517s: 52 source H4 regions allow 51 full eligible H4 closes after the explicitly skipped first interval, literal BB window10×100+9×104, signal low97.5/close100.5, quantity30, entry102.5 at TradeStart+5m and stop fill99.5 at+6m despite interval high200/low90. COMPLETE economics independently match gross−1800 USD, two fees149.4 USD and net−1949.4 USD. No warmup signal or record beyond horizon. 12127 OPEN and SOURCE_CLOSE pairs; OPEN omits future closed OHLC. Independent big-endian length framing of every closed source ref gives `sha256:a8e057a6e6797566d081ed5e9708c5bca06900b52d66de593bdc8945818c7e57`, exactly matching footer input sequence. Fresh sealed reproduction is IDENTICAL after removing prepared and sibling RunSpec files.

A separate tiny fresh-process truncated horizon produces sealed `SOURCE_COVERAGE_INCOMPLETE`, consumes exactly one closed source (declared2 includes the preceding omitted interval), and reproduces IDENTICAL without sibling specs. Prefix digest `sha256:4edc67cfa29899e4eda363895b7846c6c92dd070907ebdbf3ac5ecd487db903b`. An independent mid-interval reservation probe has one OPEN, no future source, zero folded refs and honest INCOMPLETE Finish before contractual horizon.

Fresh binary legacy C-versus198f uses identical explicit NDJSON and RunSpec bytes; artifact bytes equal SHA256 `d5325ae6cf99725a9e7e23dab1951b1e8fb60468f29a41179a636f5b504c5ad7`. Spec SHA256 `63ef1fded7a5475284751265a548688bbd024ff2d2968dbf7ec6bb9c0c5bd79b`, dataset SHA256 `2797e2471c5e7b4725e6156258a3cd39d7477ea9dc7926eec822f63a7d0b9b6a`. This three-minute CLI fixture honestly finishes FAILED because S2 warmup is insufficient; it proves exact legacy transport, not a completed historical/domain run. The two independent valid legacy COMPLETE oracles above provide separate state evidence.

Year0000 parser-valid source plus explicitly typed contract2026 before Chicago17 materializes Plan.Start year−1. Public preparation returns the visible marshal error `time.Time: year outside of range [0,9999]`. This falsifies an impossible-marshal coverage exclusion; it is coverage evidence, not a software finding or authentic historical input. Guard retained and counted.

### Exact coverage and validation

| Scope | Covered/denominator | Raw/applicable | Exclusions |
|---|---:|---:|---:|
| F08 whole touched instrumentation blocks | 10/10 | 100% | 0 |
| CLI all new/changed blocks across main/run/reproduce/nt_source/prepare_nt | 186/192 | 96.875% | 0 |
| Integrated F08+CLI | 196/202 | 97.0297% | 0 |

Mapping counts each complete Go instrumentation block intersecting any added/replaced source line versus C, including adjacent unchanged statements; whole new helper files are included. F08's last block includes two unchanged statements; the producer's narrow8-new-statement figure lies wholly within these covered10 and is not an arithmetic defect. `audit_changed_coverage.py` independently regenerates the combined map and source-byte checks. Profiles come from this reviewer's directed producer-test rerun plus independently written probes; producer profile hash `3ef6ca34d38dcc940e08ed5397aff727aa9c79a7083ac6005471ac9bf8dec56a` was checked but not used as a percentage claim. No OS/error/unreachable blanket exclusion. Whole package63.9% and sequenceCursor.Next whole-function5/7 are separate scopes; unchanged guards outside the diff remain visible, not silently declared unreachable.

CLI six remaining unhit changed statements are explicitly retained: filepath.Abs error, descriptor malformed tail, preparation NewSource error, FunctionalNQEvalSpec error, preparation malformed tail, and the caller-controlled cmdReproduce route selection. Native caller-controlled source execution and inherited F07 late-admission behavior have directed evidence; full arbitrary control scripts were not newly exhaustively audited.

Independent F08 race7.477s; directed race10.509s; zero-operation follow-up PASS. CLI directed producer tests race1.332s, independent fast race1.496s, deterministic F09 race1.218s, fresh actual domain129.517s, fresh tiny failure+legacy4.477s. Targeted Go vet packages PASS. All test/build subprocesses run under `unshare --user --map-root-user --net`, offline module environment and explicit package/regex; no broad `go test ./...`, unknown seeds/suites or external network. Staticcheck unavailable, not installed. Initial reviewer-only compile/oracle mistakes are retained in external setup logs and are not product findings.

### Handoff and evidence location

Heavy evidence and disposable copies live under Aranea-root-relative `work/btg-s01-20261006/reports/native-integrated-final-review/`. Key files: `findings-capsule.json`, `cli-f09-capsule.log`, `cli-independent-fast-final.log`, `cli-independent-domain-final.log`, `cli-independent-short-process.log`, `f08-independent.log`, `f08-reference-red-oracles.log`, `f08-directed-race.log`, `f08-proof.json`, `integration-proof.json`, `cli-coverage-independent.json`, coverage profiles and vet logs. Independent probes live in `cli-probes/v3/backtester/cmd/echo-backtest/reviewer_cli_{fast,domain,short_process}_test.go` and `f08-probes/v3/backtester/reviewer_f08{,_oracle}_test.go`.

Reproduce F09 with the capsule disposable source and `GOGC=off`, isolated Go race regex `^TestReviewerCLIResourceFailureScope$`; expected behavior on frozen198f is original spool error plus residual cursor FD before return. A fresh remediation review must use the same inputs and expect no FD increment. F10 is exact Scope metadata correction. Preserve original errors, F08 six-byte provenance, domain/source boundaries, sealed reproduction and exact legacy artifacts. No product changes were made by this reviewer.

ROOT remains open. This worker closes only its own review session. Feedback NONE (no demonstrated Sistema1 gap); reusable skill candidates NONE. Model host `gpt-6.1-sol`, Codex surface, ProChat0. Agent-run and change-log are separate session evidence; no master/sync/.sync edits.

## Fuentes

Actual frozen repository AGENTS/CONSTITUTION/rules and CLI/F08 SDD; OWNER-S2-BARS-AUTHORITY, FUNCTIONAL-BASELINE-PROFILE and FINDINGS from ROOT's canonical evidence lane; accepted independent C review document `83a71f1aa4fb600c5ec91dc38a9201db1bb29d44`; frozen171 account-day verification; producer CLI coverage map inspected; independently executed tests/profiles/proofs listed above. Findings closure belongs to ROOT and subsequent fresh reviewer, not this artifact.

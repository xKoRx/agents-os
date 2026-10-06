# Z2 Implementation Report — MKE Z.AI Provider Migration (adapter `zai`)

- **Verdict: PASS**
- **Implementer:** Z2 (implementer one-shot)
- **Date:** 2026-10-06
- **Repository:** `/home/kor/mke/multimodal-knowledge-engine`
- **Branch:** `feature/v2-layered-knowledge-model`
- **Baseline HEAD:** `20ad4de4af2619796b294cf6cb1de8860486318c`
- **Final SHA:** `bd2edc1db5486e716323bb17d7fb7e8545e7db52`
- **Pushed:** NO (per mandate; the manager pushes after adversarial review)
- **Working tree:** clean (only the pre-existing untracked `wt/` worktree, untouched)

## Commits (atomic, in order)

| SHA | Message |
|---|---|
| `5ee737b` | feat(providers): add zai adapter for Z.AI OpenAI-compatible chat completions |
| `964fca4` | feat(cli): wire zai vlm backend into provider selection and usage help |
| `bd2edc1` | feat(probe): add zai backend to probe-runtime capability probe |

## Files added / modified

Added:
- `internal/providers/zai/zai.go` — the adapter (504 lines).
- `internal/providers/zai/zai_test.go` — dedicated httptest suite (869 lines, fixture key `test-key-123` only; no real credential anywhere).

Modified:
- `cmd/mke/main.go` — `buildProvider()` `zai` case, default `--vlm` error message, usage `--vlm` provider enumeration, `runProcess` flag description.
- `cmd/mke/pipeline.go` — `pipelineUsage` `--vlm` provider enumeration, `runPipeline` flag description.
- `cmd/mke/probe.go` — `probeUsage` backend list, `executeProbe` switch + unknown-backend error, `probeVLM` `case "zai"`.

## Gates (all run at final HEAD `bd2edc1`)

1. `go build ./...` — **PASS** (silent, exit 0).
2. `go vet ./...` — **PASS** (silent, exit 0).
3. `go test ./... -count=1` — **PASS** (21 packages ok, 0 FAIL):

```
ok  	mke/cmd/mke	59.930s
ok  	mke/internal/benchmark	33.981s
ok  	mke/internal/claims	0.016s
ok  	mke/internal/evidence	118.549s
ok  	mke/internal/knowledge	0.093s
ok  	mke/internal/media	32.993s
ok  	mke/internal/pipeline	107.252s
ok  	mke/internal/provenance	0.012s
ok  	mke/internal/providers	0.006s
ok  	mke/internal/providers/capability	0.020s
ok  	mke/internal/providers/contract	0.221s
ok  	mke/internal/providers/glm	0.572s
ok  	mke/internal/providers/lmstudio	0.383s
ok  	mke/internal/providers/ollama	0.390s
ok  	mke/internal/providers/openrouter	0.268s
ok  	mke/internal/providers/recorded	0.015s
ok  	mke/internal/providers/whisper	4.415s
ok  	mke/internal/providers/zai	0.277s
ok  	mke/internal/publish	0.021s
ok  	mke/internal/runstate	0.576s
ok  	mke/internal/sko	0.019s
```

Note: `gofmt -l` flags ~20 pre-existing files at baseline (e.g. `internal/media/*.go`, `cmd/mke/live_contracts_test.go`) — pre-existing drift at `20ad4de`, not touched. All new/modified files are gofmt-clean.

## Implementation decisions

- **Sibling adapter, frozen boundary.** `internal/providers/zai` implements `providers.VLMProvider` without touching the frozen `providers.go` contract. Mechanics (HTTP client wiring, bounded retry loop, `DefaultBackoff` linear-capped, `classifyTransport`/`classifyStatus`, capability markers, `errorDetail`, `extractJSONObject`, DTO style, test style) are copied from `openrouter` as mandated. Constants copied from openrouter: `DefaultMaxRetry=2`, `DefaultTimeout=120s`, backoff base 500ms capped 5s, `maxBodyBytes=32<<20`.
- **Identity.** `adapter = "zai"`; `Model` default `glm-5.3-flash` (`MKE_ZAI_MODEL`); no `openrouter.*` anywhere in provenance/audit.
- **Env contract.** `MKE_ZAI_API_KEY` (missing → fatal auth-class error before any network, same as siblings; CLI maps it to invalid input exit 2), `MKE_ZAI_BASE_URL` (default `https://api.z.ai/api/paas/v4`), `MKE_ZAI_JSON_MODE` (default **on**; `false`/`0`/`no`/`off` disable, same bool grammar as openrouter), `MKE_ZAI_REASONING_EFFORT` (default `max`).
- **Request mapping.** POST `{base}/chat/completions`; `model`, `temperature: 0`, `stream: false`, **no `max_tokens`**; `thinking: {"type":"enabled"}` always + `reasoning_effort` from config; `response_format: {"type":"json_object"}` when JSON mode on; system prompt as a separate `system` string message; text parts concatenated with the same evidence-ID preamble as openrouter, then ordered `image_url` data-URL parts (`data:<MediaType>;base64,<b64>`, empty MediaType → `image/png`), order preserved exactly.
- **Error mapping.** 429/5xx/transport-timeout/other-network → retryable; 404 → unsupported; capability-marker gap → unsupported; 401/403 → fatal auth; other 4xx → fatal; empty `choices` → retryable (R-B01 anomaly family, budget ends retry-exhausted); empty/whitespace `content` → retryable (recovers on replay; persists → retry-exhausted); present-but-malformed content → fatal. Caller cancellation stays fatal.
- **Response mapping.** `RequestID = providers.RequestIdentity(req)`; `ProviderRequestID = ResponseID = id`; `Model` = echoed `model` with configured fallback; `OutputSchemaID` passthrough; `Structured` = extracted JSON object of the final `content` (fence-tolerant, identical to openrouter); `Usage` passthrough of prompt/completion/total (backend already includes reasoning tokens in completion; never recomputed); `Warnings`: JSON-mode-disabled degradation + `finish_reason=length` truncation.
- **Audit.** `zai.endpoint`, `zai.response_id`, `zai.created`, `zai.model`, `zai.model_requested`, `zai.http_status`, `zai.finish_reason`, `zai.json_mode`, `zai.temperature`, `zai.reasoning_effort`, `zai.thinking`, `zai.content_bytes` — sanitized, never the key, never `reasoning_content`.
- **Secret scrubbing.** Configured key replaced with `[redacted]` in error details (openrouter technique) and — see deviation 3 — also in response-derived strings (content before parsing, id, model, finish_reason, audit values).
- **CLI smoke checks (no credential, no network).** `mke process … --vlm zai` without `MKE_ZAI_API_KEY` → `mke: --vlm zai requires MKE_ZAI_API_KEY to be set`, exit 2. `mke probe-runtime --backend zai --host-class ci` without key → `status:"BLOCKED"` row, exit 0, no dial.

## Test coverage (mandated cases → tests, all in `internal/providers/zai/zai_test.go`)

auth absent before any call; basic request serialization (model/temperature/stream/no-max_tokens/thinking/reasoning_effort/response_format); system+text mapping; single image data URL (exact bytes + media type + `image/png` fallback); 3-image order preservation + evidence IDs in preamble; JSON mode on/off via env (+off ⇒ no `response_format` + warning + audit); thinking/reasoning settings via env; usage parsing (backend total respected); model echo + configured fallback; response id parsing; 429→retryable; 502/500→retryable; 404→unsupported; 401/403→fatal; capability-gap→unsupported; plain 400→fatal; empty choices→retry-exhausted (retryable inner); empty content recovers on retry; persistent empty content→retry-exhausted; malformed content→fatal (no structured output); fenced JSON tolerated; timeout→retryable; retry exhaustion→`ClassRetryExhausted` (3 calls at budget 2); retry-then-success; caller cancellation→fatal; key never in error (hostile echo → `[redacted]`); key never in Structured/Audit/Warnings/Model/ResponseID; `reasoning_content` never in Response/Structured/Audit (and usage still the backend total); `finish_reason=length` warns; `ConfigFromEnv` defaults and overrides; request identity content-addressed.

## Deviations from the design (with reason)

1. **`live_contracts_test.go` / `live_readiness_test.go` were not modified.** The mandate expected provider enumerations there, but both files drive the pipeline exclusively via `recorded:<script>` fixtures and enumerate no provider names (verified by reading them in full). The actual provider enumerations live in `cmd/mke/probe.go` (backend switch + usage), `cmd/mke/main.go` and `cmd/mke/pipeline.go` help texts — `zai` was added to all of those. No credential or network is involved anywhere.
2. **`pipeline.go` help also gained `openrouter`.** Its `--vlm` enumeration had pre-existing drift (listed only `glm` and `recorded`, although `buildProvider` accepts `openrouter`). Since the mandate requires help/usage that enumerates providers to be updated and accurate, the text now lists `glm`, `openrouter`, `zai`, `recorded`. Same for the two stale flag descriptions (`VLM backend: glm | recorded:…` → now including `openrouter | zai`). Documentation-only; no semantic change.
3. **Scrubbing extended one step beyond openrouter's exact mechanics.** The mandate states the configured key must be removed from any provider-returned text entering Response/Audit/errors; openrouter only scrubs error details. The zai adapter additionally scrubs the assistant content before parsing and every response-derived audit/response string. Pinned by `TestKeyNeverReachesStructuredOrAudit`.
4. **Probe forces `cfg.JSONMode = false` for the zai contract suite** (probe-scope only), mirroring openrouter's probe rationale: the malformed-output contract case needs the backend free to answer with prose. The adapter env default remains ON as designed.
5. **`ProviderRequestID` is set to the response `id`** (identical to openrouter's behavior; the design only specified `ResponseID`).

## Intactness of sibling adapters (explicit confirmation)

`internal/providers/openrouter/`, `internal/providers/glm/`, `internal/providers/recorded/` are byte-identical to baseline — none appear in the diff:

```
$ git diff --stat 20ad4de..HEAD
 cmd/mke/main.go                    |  17 +-
 cmd/mke/pipeline.go                |   5 +-
 cmd/mke/probe.go                   |  34 +-
 internal/providers/zai/zai.go      | 504 +++++++++++++++++++++
 internal/providers/zai/zai_test.go | 869 +++++++++++++++++++++++++++++++++++++
 5 files changed, 1419 insertions(+), 10 deletions(-)
```

`wt/` untouched; no network calls to Z.AI; no push; no real API key used or present.

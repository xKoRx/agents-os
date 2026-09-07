---
type: decision
schema_version: 1
scope: project
created: "2026-08-27"
updated: "2026-08-28"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[AGENTS OS]]"
related:
  - "[[2026-08-27-durable-sdk-minio-atomic-create]]"
aliases: []
confidence: verified
source_session: DURABLE-ARTIFACT-PLANE-WRITE-ONCE-FINAL-E2E-NORMAL
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
---

# 2026-08-27-durable-artifact-plane-write-once-final-e2e

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Baseline Symphony `5e3c2b39a62f1d953035281bb38146551a79dc0d`; SDK `ea09cc1bb8b34e661c8f31f887dce58613b0475a`; runtime pin `v0.0.0-20260827204048-ea09cc1bb8b3`.
- Release `0.2.77` publicada y activada. Linux `symphony` SHA256 `9a3554e26c77f0d10cf4bfbcd1f2764fb93b8b4183d785b539497559b5d44398`; Linux watcher `1e0808bc3febb4a966e208ec84b4653da1a680000be11c33e9985d91064308be`; Windows MT5 `6bdca2a633ad68be1428221ab004669c7a88dd3338c3988d9690af96a55bea92`.
- El binario publicado, vía `go version -m`, contiene `vcs.revision=5e3c2b39a62f1d953035281bb38146551a79dc0d` y `github.com/xKoRx/sdk v0.0.0-20260827204048-ea09cc1bb8b3 => ../sdk`; `SDK_PIN_RUNTIME: PASS`. El `+dirty` del módulo refleja el worktree operativo preexistente; no hubo cambios Go en esta sesión.

## Decisión

- `ARTIFACT_PLANE_WRITE_ONCE: CERTIFIED_CLOSED / FROZEN`.
- Todo durable Evidence-backed es create-only físico: primer `X` inmutable; mismo `X` reconcilia a `ACK`; distinto `Y` devuelve `CONTRACT_CONFLICT`, incluido mismo tamaño, retry y concurrencia.
- Apply sella `RecoveryMetadata`; la reconciliación usa tamaño + SHA256 físico. `STAT_THEN_PUT_AUTHORITY: ZERO`, `DELETE_REPLACE: ZERO`, `ETAG_AS_DIGEST: ZERO`.

## Rationale

- FlowRun normal: `RequestID=cert-writeonce-normal-20260828-0148`, `FlowIntentToken/WorkflowID=e90dd24d-0520-4f20-9911-b0f39952ecb0`, `FlowRunRef=18232bf9-50b8-4219-a871-254d502bf3b8`, `WorkflowID=sqx-main-v1-e90dd24d-0520-4f20-9911-b0f39952ecb0`, `RunID=01a0460d-b753-718d-9028-3efc5689b7da`, `wave=writeonce-normal-20260828-0148`; Temporal `Completed`, sin reset.
- Workers activos en la release: Zeus `0.2.77` con `symphony` y watcher; Hera `0.2.77` con `symphony` (watcher no observado); Kronos `0.2.77` con `symphony` (watcher no observado); Windows MT5 `0.2.77`. Se detuvo el watcher transient antiguo `0.2.68` de Zeus y se activó `0.2.77`.
- Source audit exact baseline: los cinco writers congelados/shared son `UploadFromDiskExact` (`minio_storage.go:145`, caller `steps.go:1566`), `PutPayload` (`payload_store.go:19`, TradeSet/WFM/MT5), `PutApplySelectedRun` (`apply_selected_run.go:53`), `UploadArtifactFromPath` (`artifact_store.go:98`, MT5 activities/compiler) y `PutObjectFromPath` (`minio_storage.go:615`, MT5 compiler/robust activity). Todos delegan a `PutObjectIfAbsent` y reconciliación exacta.
- Ocurrencias restantes: deploy/stager (`deployer/adapters/storage-minio/storage.go:14,36,38`, `deployer/watcher/watcher.go:159`, `internal/tasks/process_workflow-document.go:534`, `internal/tasks/sqx_deploy_watcher.go:443`) operacionales; `generate_report.go:270` reportes mutables; `core/strategies/minio_uploader.go:187,266,330` config/input/markers; `trade_lists.go:347,415` legacy no product-wired; tests/interfaces no productivos. Resultado `EVIDENCE_BACKED_DIRECT_OVERWRITE_WRITERS: 0`, `LEGACY_TRADELIST_PRODUCT_WRITING: ZERO`.
- Path productivo confirmado: `ExportTradeListActivity → Stores.PersistTradeSet → PutPayload`; no se registran `WithTradeListWriter`, `WithTradeListReader` ni `act_upsert_trade_list`.

## Consecuencias

- Harness disposable `certification/write-once/final-e2e-20260827-02`: Strategy 46 bytes `b2b1b9c68cc12490ccfc512671cc0ad2b5ef4f4d4fcc4e83ccb364a8958ec135`; Strategy 38 bytes `735eb7f2ed8ed9ca5a7a66578e6791fcf9b374d00988f044e915f8b86d8f3539`; Payload 37 bytes `8dbc8956582b68ab46e7be87ddbaef3f733696ab6e0cdf796d7a2c0fca2c00dd`; Apply 35 bytes `b2d4da28f344c1ee7e1283052ccb20a6b0cd647ae46f7aa6bbe976757dde3b5f`; ArtifactRef raw hex `ec4c24b6f219ecbbe0a7b308459b2ee555ed75ca5fdde4dec03155f2f4f9b340`; PutObjectFromPath 36 bytes `813343895b9e915a205d567bb4088d3709a70d8fb5b3b5e7f50f2dcb0fd645c1`. En todos expected = físico.
- Concurrente: X `sha256:ea867db03ca558d946553eeed04c1840b35c2ffbf47c4780fc45a6c78d1671cc` ganó con `ACKNOWLEDGED`; Y `sha256:d488e96174644686e323e17f6974521d27752f50e73e8687a5fbfdd91866b08a` obtuvo `CONTRACT_CONFLICT`; final = X. `CONCURRENT_CREATE_ONLY: PASS`, `LAST_WRITER_WINS: NO`.
- FlowRun Strategy samples: `wave_writeonce-normal-20260828-0148/.../01_builder/...Strategy_4.1.15.z0.sqx`, size `156156`, expected/físico `sha256:db18ec5bea7f4ec2e23b5ea5d493e30cea673a3b399efe21249fb3281edf72c`; `.../01_builder/...Strategy_6.1.22.z0.sqx`, size `78754`, expected/físico `sha256:dfac4f39c507c63f642bc2da02999dab67532749129bef0d9f7691e5529995a5`.
- TradeSet real sample: `durable/trade-list/v1/18232bf9-50b8-4219-a871-254d502bf3b8/b7941521-bef9-44dd-a5a6-18fc0ea9b77b/sha256:389a171fe226b4fdc04003adc2d94502a306df533dbb40b79fcf54b127639ac0/73212ae9e6c61eb60954fc8f0daf8bbcb1061819c0c252756b024cd93de09226/trades.ndjson.gz`, size `1406`, expected/físico `sha256:4323945aeca78499bb9b5b42ca602be930569ef45339caabb359b97eb6e15ab5`; Mongo `trade_sets` coincide.
- Apply real sample: `durable/apply-selected-run/v1/18232bf9-50b8-4219-a871-254d502bf3b8/a74b55ea-5a41-42bd-82eb-c923c106ab46/c7dd0c1a-4bd9-468c-85b3-6f7adf0c15c0/strategy.sqx`, size `3882229`, expected/físico `sha256:18600437997d8f1ef774f4afbf9f44e6f7d99e40b5a6d25e65d8b3076e3bfbb2`; metadata física coincide: config `sha256:1002765236b03f3557f3569796e66be08680048eea911d1212e2349357e59d27`, decision `sha256:7310cb1db07d68ad3f7aaea1eb6af27e80a9c2a258adf58acef413acb9fd45d0`, producer `sqx-apply-selected-run.v1`, stage `c7dd0c1a-4bd9-468c-85b3-6f7adf0c15c0`.
- MT5 real: `MT5CompileArtifactWorkflow` completó `success`, batch `compile total 4 success 4 failed 0`; EX5 sample `durable/mt5-export/v1/18232bf9-50b8-4219-a871-254d502bf3b8/b7941521-bef9-44dd-a5a6-18fc0ea9b77b/sha256:389a171fe226b4fdc04003adc2d94502a306df533db40b79fcf54b127639ac0/08_mt5_ex5/final-b7941521-bef9-44dd-a5a6-18fc0ea9b77b.ex5`, size `178068`, ArtifactRef expected/físico `sha256:0b4bc03d2d736b438c2eb3d5eab2714be1debf7c21fa7ce59df8d5c0d3f3fbf6`. Esto certifica `UploadArtifactFromPath` y `MT5 Compiler → PutObjectFromPath → storageminio.Storage`; `MT5_WORKER_DIRECT_SDK_PUT: ZERO`.
- Same bytes → `ACK`; bytes diferentes y same-size/different-bytes → `CONTRACT_CONFLICT`; Apply `A+M2` → `CONTRACT_CONFLICT`; bytes/metadata originales preservados. `ORIGINAL_BYTES_PRESERVED: PASS`, `APPLY_METADATA_IMMUTABLE: PASS`, `PHYSICAL_EVIDENCE_RECONCILIATION: PASS`, `HISTORICAL_SOURCE_WRITE: ZERO`.
- `UNKNOWN_COMMIT_PHYSICAL_E2E: CERTIFIED_BY_SLICE1`; no se inyectó pérdida de respuesta sobre keys product-like.

## Alternativas descartadas

- No se hizo Temporal Reset, migration, schema change, recovery Retester/Optimizer ni código/commit. Harnesses temporales retirados; worktree dirty extranjero preservado.
- Verified reads queda separado. Siguiente track exacto: `DURABLE-ARTIFACT-VERIFIED-READS-RCA-TOP`.

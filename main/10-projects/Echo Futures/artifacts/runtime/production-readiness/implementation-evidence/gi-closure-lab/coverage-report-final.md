# Cobertura global EF-PROD (bloques únicos) — HEAD 5011d21e6d2edf3401b7e4666cd6b43809483042

**Global: 1982/2050 bloques = 96.68%** (umbral GOD-03 >=95%)

Denominador: todos los bloques de los archivos creados en el delta (sin exclusiones de código).
Batería: todos los paquetes de sdk/core/futures-bridge/futures-projector/bridge con skips declarados (tests heredados rotos/colgados; ver script).

| archivo | bloques cubiertos/total | % |
|---|---|---|
| v3/bridge/internal/fxpermit/permit.go | 66/66 | 100.0% |
| v3/core/cmd/echo-core/recovery_plane.go | 70/85 | 82.4% |
| v3/core/cmd/echo-runtime-control/cli_run.go | 20/22 | 90.9% |
| v3/core/cmd/echo-runtime-control/control.go | 87/88 | 98.9% |
| v3/core/cmd/echo-runtime-control/main.go | 11/13 | 84.6% |
| v3/core/internal/deployverify/deployverify.go | 96/96 | 100.0% |
| v3/core/internal/functions/owner_continuity.go | 31/33 | 93.9% |
| v3/core/internal/futuresruntime/recovery_gate.go | 77/78 | 98.7% |
| v3/core/internal/runtimecontrol/attestor.go | 50/51 | 98.0% |
| v3/core/internal/runtimecontrol/errors.go | 6/6 | 100.0% |
| v3/core/internal/runtimecontrol/guard.go | 35/35 | 100.0% |
| v3/core/internal/runtimecontrol/keys.go | 5/5 | 100.0% |
| v3/core/internal/runtimecontrol/kv.go | 22/22 | 100.0% |
| v3/core/internal/runtimecontrol/manifest_loader.go | 29/30 | 96.7% |
| v3/core/internal/runtimecontrol/offset_window.go | 37/37 | 100.0% |
| v3/core/internal/runtimecontrol/permits.go | 72/76 | 94.7% |
| v3/core/internal/runtimecontrol/readiness.go | 42/42 | 100.0% |
| v3/core/internal/runtimecontrol/registry.go | 35/38 | 92.1% |
| v3/core/internal/runtimecontrol/restore_exec.go | 52/56 | 92.9% |
| v3/core/internal/runtimecontrol/submitter.go | 102/106 | 96.2% |
| v3/futures-bridge/adapters/journalfs/observations.go | 279/288 | 96.9% |
| v3/futures-bridge/core/capabilities/observation_delivery.go | 7/7 | 100.0% |
| v3/futures-bridge/core/ntx/observation_ack.go | 19/20 | 95.0% |
| v3/futures-bridge/internal/permit/permit.go | 70/70 | 100.0% |
| v3/futures-projector/adapters/kafka/publisher.go | 21/23 | 91.3% |
| v3/futures-projector/adapters/memstore/authority.go | 28/28 | 100.0% |
| v3/futures-projector/adapters/pgstore/authority.go | 53/54 | 98.1% |
| v3/futures-projector/core/authority/fact_adapter.go | 21/21 | 100.0% |
| v3/futures-projector/core/authority/producer.go | 87/94 | 92.6% |
| v3/sdk/futures/accounting/revision_authority.go | 57/57 | 100.0% |
| v3/sdk/futures/domain/admission_context.go | 47/48 | 97.9% |
| v3/sdk/futures/domain/protection_capability.go | 22/22 | 100.0% |
| v3/sdk/futures/market/cursor.go | 90/90 | 100.0% |
| v3/sdk/futures/recovery/attestation.go | 53/54 | 98.1% |
| v3/sdk/futures/recovery/continuity.go | 17/17 | 100.0% |
| v3/sdk/futures/recovery/digest.go | 15/16 | 93.8% |
| v3/sdk/futures/recovery/errors.go | 3/3 | 100.0% |
| v3/sdk/futures/recovery/lineage.go | 40/41 | 97.6% |
| v3/sdk/futures/recovery/manifest.go | 60/64 | 93.8% |
| v3/sdk/futures/recovery/permit.go | 48/48 | 100.0% |

STATUS: M2-S01_PASS

REPO:
- path: `~/go/src/github.com/xKoRx/polymarket-engine` (checkout existente registrado; commit checkpoint `0912d39` en `main`, sin push ni tags)
- module: `github.com/xKoRx/polymarket-engine`
- Go: `1.27.0`
- toolchain: `1.27.1`

IMPLEMENTED:
- foundation: IDs nominales por namespace no intercambiables (`GammaEventID`, `GammaMarketID`, `IntentID`, `RunID`, `StrategyID`, `ExperimentID`, `VenueTradeID`, `FillKey`), `AssetKey{chain_id, protocol, token_contract?, wire_asset_id}`, `ConditionRef{protocol, raw_id}` (bytes32 para CTF), unión cerrada `ProtocolIdentity` (CTF/PROTOCOL_V2/UNKNOWN sin conversiones), decimal exacto coefficient+scale parseado desde lexema JSON con shopspring encapsulado (sin `float64`, sin `*big.Int` expuesto, overflow y `-0` rechazados/normalizados, forma canónica y serialización determinista), unidades `Price/Shares/CollateralAmount/BasisPoints/FeeCoefficient` con política de signo y conversión exacta bps→coeficiente, `RevisionRef{owner, namespace, entity_id, generation, revision, schema_version, content_hash}` con 9 owners cerrados, `Clock` (wall+mono por boot, `FakeClock` determinista, `SystemClock` como único `time.Now`), `SourceTime` con unknown explícito y precisión declarada, `VirtualTime` tipo distinto, error taxonomy tipada de 11 kinds estable bajo wrapping (`errors.Is`/`errors.As`), capability registry v1 fail-closed (8 capabilities frozen no habilitables: LIVE_EXECUTION, NEGRISK_CTF/V2_CONVERSION, L2_HISTORICAL_BACKFILL, DEFER_EXEC, BUILDER_OPTIONAL, COMBO, RFQ; unknown/missing/disabled → DENIED; sin `defaultAllow`), `ExecutionMode` (default `LIVE_DISABLED`) y `ActivationLease` como value contract (`RequestActivationLease` → `DISABLED`; sin emisor, sin secretos).
- config: TOML estricto versionado (`BurntSushi/toml`, schema v1 obligatorio, unknown fields rechazados con nombre exacto, defaults inequívocos, `LIVE_ENABLED` → FAIL `DISABLED` porque el registry v1 niega `LIVE_EXECUTION`, hash de revisión determinista sobre config normalizada, sin campos de secretos verificado por test reflect).
- archtest: mecanismo AST (`go/parser`, sin herramientas externas): dirección de imports (foundation no importa internos; config sólo foundation), sin `utils`/`common`, detección de ciclos, y gate de imports de estrategias reusable para S09/G-15b (unsafe/reflect/os/os-exec/net/syscall/plugin/cgo, goroutines propias, `time.Now`, `math/rand`) con fixtures probe en rojo (unsafe, net/http, goroutine, clock, random) y fixture neutral en verde.
- cmd: `cmd/engine` mínimo con subcomando `version` (module/commit/toolchain/config schema; commit estampado en build compilado), sin networking, sin SQLite, sin lógica de negocio.

QUALITY:
- go test: PASS (unit + property rapid + fixtures G-01)
- race: PASS (`go test -race ./...`; property con seed fija 20260917 verde, registrada en bitácora)
- vet: PASS; `go mod tidy` con sólo 3 dependencias directas (decimal, toml, rapid; cero transitivas inesperadas)
- coverage: 95.1% total (foundation 95.0%, config 97.8%, archtest 97.1%; cmd 83.9% — única excepción: `main`/`exitWith`, seam `os.Exit` no testeable sin matar el binario)

GATES:
- PASS: G-01 porción S01 (62 vectores IDs/decimal/unidades/fills; evidencia física en `testdata/foundation/evidence/g01.json` con hash de fixture `f6c2796f…`, expected/actual y build) · G-15b base mecánica (evidencia `evidence/g15b-base.json`; cierre con fixtures de redacción queda en S09/S12). Semilla de G-15 cubierta por la matriz fail-closed de capabilities en tests.
- NOT_RUN: G-02 (asignado a S10/S11), G-03 en adelante — no declarados.
- evidence: regenerable con `PM_ENGINE_EMIT_EVIDENCE=1 go test ./...`; integridad de evidencia re-verificada en cada corrida normal.

SCOPE:
- files/packages created: `go.mod`, `cmd/engine`, `internal/foundation`, `internal/config`, `internal/archtest` (+fixtures `testdata/`), `testdata/foundation` (vectores + evidencia). Sin paquetes futuros vacíos, sin migraciones, sin SQLite.
- explicit deferred work: tabla de ticks/redondeos P03 §5 → porción S05 de G-01 (el mandato ordering las rounding rules de órdenes a S02/protocol); el plan M2 corregido puntualmente (`go 1.23` → baseline 1.27, repo location resuelto) sin otras modificaciones; proyecto Agents-OS actualizado (estado `M2_FROZEN — S01 DONE`, tareas, bitácora) y run registrado en `80-agents/journal/agent-runs/2026-09-17-zcode-glm-5.3-flash-pm-engine-m2-s01-foundation.md`.

BLOCKERS:
- none

NEXT:
- M2-S02 + M2-S03 barriers
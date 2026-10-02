# Echo Futures — D6 Shot 1 — Real NinjaTrader Execution Vertical Implementation

**Shot:** D6 Shot 1 — IMPLEMENTATION (egress structurally disabled)
**Role:** TOP Senior Implementation Lead / IMPLEMENTER (no Manager, no Owner, no reviewer independiente)
**Date:** 2026-10-01 (implementación y evidencia UTC 22:0x–01:5xZ; despliegue DEV verificado 00:1x–00:20Z del 2026-10-02 local -03)
**Project:** [[Echo Futures]]
**Baseline:** `xKoRx/echo@f0c82905d4eaf825c08e04f0bb97cab73e616ba5` (`origin/feature/d6-n1-readonly-vertical`, `D6_N1 = PASS` — re-verificado al iniciar: worktree limpio, HEAD == origin)
**Branch del shot:** `origin/feature/d6-shot1-execution-vertical` @ `4b05d6f856df41b748ad2bfb1f0806b45349387f` (15 commits, FF sobre `f0c82905`; push FF verificado `origin == local HEAD`)
**Authorities:** D6 Final Design Freeze (2026-10-01) §3–§12/§14–§15; C1-R1 F1 (STOP_MARKET, Manager-accepted, congelado como autoridad de implementación); N1 physical evidence (read-only vertical + binding final); D4/D5 frozen contracts; GAU50 preflight (2026-09-30) + N1-R2 owner entitlement correction.
**Verdict:** `D6_SHOT1_IMPLEMENTATION = READY_FOR_ADVERSARIAL_REVIEW`

## 0. Hard safety

`ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0`, estructural y de despliegue:

- El feed AddOn (N1-certificado, único instalado en dev-win) mantiene **0** referencias a `Account.Submit/Change/Cancel/Flatten/CreateOrder` (grep re-ejecutado sobre el source final @ `4b05d6f8`); su única mutación es la inversión de resolución de cuenta (§3 del freeze), sin familia de comandos en `echo.ntfeed.v1` y sin lectura de canal.
- `EchoExecutionAddOn.cs` (el build con camino de comandos) es **STAGED, NO instalado** — vive como candidato Shot 3 compilado en sombra; ninguna sesión NT lo carga.
- El futures-bridge **no está desplegado ni corriendo** para la cuenta: la lista de sesiones (`futures-bridge/accounts`, ausente en ETCD ⇒ default vacío) no incluye `E2T-GAU50-01`; ningún consumidor de `echo.order-commands.*` activo.
- La readiness de ejecución queda fail-closed por diseño: el adapter `NINJATRADER_BRIDGE` declara **todas** las capacidades M2 mandatorias como `UNKNOWN` (cada una es un gate físico Shot 3) ⇒ `SubmissionCapabilitiesReady=false` ⇒ `StaticEligible=false` ⇒ la conjunción §22 jamás abre new risk; `STOP_MARKET` es rechazado **antes** de cualquier escritura de journal (gate de capability).
- M1 no emite comandos: el pipeline Core (Strategy→Operation→GerardMM→ProviderRuleSet→reservation) no fue tocado y no hay run LIVE autorizado.
- Únicas mutaciones de infraestructura de este shot (todas DEV, todas verificadas con read-back doble): 1 clave ETCD (`binding/provider-account-ref`) + restart controlado de `echo-nt-feed-relay` con release nueva del propio vertical. Master intocado; PROD intocado; el feed lane físico quedó operativo (`binding_match=RESOLVED`, mercado fluyendo, `malformed=0`).

## 1. Delta de arquitectura implementada (por scope)

| Scope | Entregado | Commits |
|---|---|---|
| S2 STOP_MARKET (F1) | Stack completo: enum `OrderTypeStopMarket` + `Order.StopPrice` + `Order.Validate` (stop requerido, limit prohibido) → `OrderRequest.StopPrice` → switch del engine → `OrderCommand.StopPrice` → proyección `stop_price` en `BridgeCommandEnvelope` → `SubmitOrder.Validate` (capabilities) → `sameIntent` con nivel de stop → GerardMM `protectiveOrder` emite `STOP_MARKET` con tighten monotónico contra `protective.StopPrice` (crossed→MARKET intacto) → sim declara el tipo y el venue lo almacena con nivel (sin modelo de marketability) | `a5cdb410` |
| S10 carried fixes | Publisher de execution-events viaja JSON crudo (`json.RawMessage`; `[]byte` plano viajaba base64 — mismo defecto corregido en N1 para market); capture del vertical espeja los bytes exactos; nota `ReadCommitted` del projector registrada como deuda preexistente (ver §7) | `a5cdb410` |
| S1 Account identity | Modelo 3 capas: `ProviderAccountBinding.ProviderAccountRef` (durable, autoridad) + `Validate()` fail-closed para `NINJATRADER_BRIDGE` sin ref + loader único (`internal/binding.Load`, duplicado de main eliminado) + relay hello Name-primario con drift de Id como degradación distinta `PROVIDER_ACCOUNT_ID_DRIFT` (bindings sin ref conservan comparación legacy) + inversión AddOn (Name-primary, match único, cross-check Id, DRIFT fail-closed) + clave ETCD escrita | `6be042a1`, `4b05d6f8` |
| S3/S4 Execution lane + adapter | `core/ntx` (schema `echo.ntx.v1`: framing/auth/seq idénticos al canal certificado + familias command/command_result; server bidireccional, una conexión AddOn activa) + `adapters/ninjatrader` (ExecutionAdapter completo sobre el seam congelado) + branch `NINJATRADER_BRIDGE` en `buildSession` (listener :9771, token ETCD requerido fail-closed, ref durable como autoridad de resolución) | `014c9744`, `4b05d6f8` |
| S5 M1/M2 + journal | Secuencia M2 congelada en el adapter: capability gate ANTES del journal → `PREPARED` fsync → `SUBMITTING` fsync ANTES de la escritura del lane (punto de no retorno) → UN comando → UNA espera acotada de `command_result`: ACCEPTED = evidencia de transporte (VENUE_BOUND exige evidencia venue de la familia orders con `Order.OrderId` nativo), REJECTED = negación autoritativa (TERMINAL), timeout/ERROR/fallo de lane = `AMBIGUOUS` (MAY_HAVE_EXECUTED), jamás re-submit ciego (test: exactamente 1 comando por identidad) | `014c9744` |
| S6 Reconciliation | Barrera sobre vistas venue vivas: found→`VENUE_BOUND`/TERMINAL; ausencia con MAY_HAVE_EXECUTED→`AMBIGUOUS` fail-closed (el lane V1 no prueba negación autoritativa fuera del snapshot vivo; `ResubmitApprovedByAbsence` jamás se emite sin ella); historial de executions→TERMINAL con fills recuperados (dedup por `ExecutionId` nativo); órdenes vivas no correlacionables→`UnknownLiveOrders` quarantine (fail-visible, nunca canceladas/adoptadas; test verifica que no sale comando) | `014c9744` |
| S7 Market freshness | `market.MarketFreshness` (FRESH/STALE/UNKNOWN; UNKNOWN bloquea) + evidencia plegada en `echo/market_stream` (sólo candidatos aceptados) + bounds por ConfigSnapshot (defaults 30 s/60 s = config, no invariantes) + composición de readiness (`ReadinessView.Freshness`; dimensión habilitada sólo en el camino serving live; replay/backtest conservan semántica D5) + defensa en admission (`DENY_MARKET_NOT_FRESH` vía frescura pineada por el requester) + razón visible `MARKET_DATA_NOT_FRESH` + E2E: feed con lag 600 s ⇒ STALE ⇒ 0 señales y denegación con señal forzada | 6 commits `07b4d824..28d23b63` (merge `6b2858a3`) |
| S8 GAU50-EVAL v1 | `v3/core/config/futures/gau50-eval-v1.json` (embed) — ACTIVE v1 EARN2TRADE/GAU50/EVALUATION con 3 SourceRefs (preflight 2026-09-30 + N1-R2 + freeze §9); únicas familias enforceables: `CapacityCaps[GROSS account-wide 6]` (6 grant / 7 deny / 4+3 deny por el path frozen de reservation) y `AllowedNewRiskWindow` hasta 15:50 CT (edge 15:50⇒`WINDOW_CLOSED`; interior/evening⇒ALLOW por admission); DD 2000 / DLL 1100 / consistencia 30% documentados NO codificados; guard de forma congelada que rechaza 6 mutaciones de drift | `763b0aa0` |
| S9 Warm-up/REBUILD | `sdk/futures/warmup`: síntesis 5m-exact determinista (4 TRADE O/H/L/C por bucket; Minute→5m agregado alineado al reloj), identidad clase C exacta del relay (auto-chequeo contra parsers Echo), `ReplayAnchor` refs+digest sellado, `PublishingPlan` (todos los candidates ANTES de RUN_START), requisitos 51 H4 + 20 5m fail-closed; regresión de fidelidad E2E: barras 5m/H4 byte-idénticas + warm-up values de S1/S2 idénticos a referencia independiente + manifest pinea el anchor | `c22847e5`, `d789b573` (merge `170a4581`) |
| G-EGRESS-0 | Estado de despliegue + tests: lista de cuentas vacía (default sin clave), bridge sin correr, capability gate CLOSED (`STOP_MARKET` excluido hasta G-STOP; M2 mandatorio UNKNOWN hasta los gates Shot 3), rechazo pre-journal de STOP_MARKET, `SubmissionCapabilitiesReady=false` testeado | todos |

## 2. Identidad de cuenta (S1) — implementación

Tres capas según el freeze §3: `E2T-GAU50-01` (Echo durable, jamás derivado de NT) → `provider-account-ref = RJARA114411201551` (NT `Name`, autoridad de binding; `Validate()` exige ref para transportes `NINJATRADER_BRIDGE`) → NT `Account.Id = "3"` (hint opcional; drift = degradación observable `PROVIDER_ACCOUNT_ID_DRIFT`, nunca remap ni datos de otra cuenta). Verificación runtime física post-despliegue: el relay nuevo (release `170a4581`, `vcs.revision` del shot) cargó el binding con la ref nueva (`binding_loaded=true, binding_error=""`), y la sesión AddOn REAL (`2f6a4d53…`, dev-win `192.168.31.132:63939 → daedalus:9770`) resolvió **`binding_match=RESOLVED`, `binding_id_drift=false`** en reconexión física — el modelo Name-primario opera contra la plataforma real.

## 3. Transporte de ejecución (S3/S4) — mapeo NT nativo

Reflexión física sobre las assemblies instaladas 8.1.8.3 (misma disciplina N1-R3) ANTES de codificar: `CreateOrder(Instrument, OrderAction, OrderType, TimeInForce, Int32, Double limit, Double stop, String signalName, String, CustomOrder)` (sobrecarga sin OrderEntry; marcada obsoleta — warning registrado para Shot 3), `Submit/Cancel/Change(IEnumerable<Order>)`, `TimeInForce ∈ {Day,Gtc,Ioc,Opg,Gtd}`, `OrderAction ∈ {Buy,BuyToCover,Sell,SellShort}`, `OrderEntry ∈ {Automated,Manual}`. El adapter mapea MARKET/LIMIT/STOP_MARKET 1:1 (sin transformación de tipos; STOP_MARKET rechazado pre-journal hasta G-STOP); cancel ack = estado `Cancelled` de la familia orders; replace = NT Change in-place (términos sobre el objeto vivo; jamás tipo nuevo); side→OrderAction es adaptación mecánica por posición neta actual, no decisión de trading. `command_result` es feedback de transporte: la verdad de lifecycle llega exclusivamente por orders/executions/positions (freeze §6.2/§6.3).

## 4. Tests, suites y cobertura

Comando canónico (`go test -race -count=1`, suites scoped; sin `go test ./...` global):

- `v3/sdk/futures/...` — 100% ok (incluye matriz STOP_MARKET domain/capabilities, protective resting shape, tighten/monotonicidad corregida, sameIntent stop-level, freshness, admission MARKET_NOT_FRESH, warmup 97.5%).
- `v3/futures-bridge/...` — 100% ok. Nuevos: harness de AddOn falso TCP real sobre `echo.ntx.v1` — ciclo de barrera, drift/mismatch fail-closed, happy path submit (venue-bound vía familia orders), reject autoritativo, timeout→AMBIGUOUS con exactamente-1-comando, STOP_MARKET rechazado pre-journal, partial-fill dedup+finalidad, matriz de reconciliación (found/absent/history/quarantine), replace accept/reject/ambiguous, fallo de lane, capability/egress gate.
- `v3/core/...` (functions, futuresruntime, futuresvertical ~8 min bajo race, config/futures) — 100% ok, incluyendo los verticales S07 freshness y S09 warm-up fidelity integrados.

Cobertura (paquete / anotaciones de lógica nueva):

- `core/ntx` 87.3% · `adapters/ninjatrader` 78.3% · `internal/binding` 100% · `sdk/futures/warmup` 97.5% · `core/config/futures` 78.9% (guard incluido).
- Nivel función (lógica nueva): evaluador freshness 100%; `pinStreamFreshness` 100%; folds de freshness del market_stream ≈97%; guard GAU50 100% de ramas (6 mutaciones de drift testeadas). Ramas sin cobertura declaradas: ventanas de timeout reales (cubiertas con timeouts acotados de test donde medibles), errores de accept TCP no-deterministas, y las ramas de `Connect/RestoreSubscriptions` tras deadline (camino físico que requiere lane caída real — gatillado en pruebas de Shot 3).

## 5. Compile evidence (C#)

- Método: shadow-compile en dev-win contra las DLL físicas (`C:\Program Files\NinjaTrader 8\bin\NinjaTrader.Core.dll` + `NinjaTrader.Gui.dll` + `WindowsBase.dll`, `csc.exe` .NET 4.x), transporte efímero http.server + `curl.exe` con verificación SHA256 byte-idéntica en ambos lados (patrón N1-R3), servidor apagado al cierre.
- `EchoFeedAddOn.cs` (SHA256 `581a7087b1b870c78ac43e67027e5edaacf59134f4bf5f03d8b9aec9d7fd5ae4` @ dev-win) — **FEED_EXIT=0, 0 errores, 0 warnings**.
- `EchoExecutionAddOn.cs` (SHA256 `9ec79f938194520208762785f075d6c740d3779d665f75f014976c69d72d1f7a` @ dev-win) — **EXEC_EXIT=0**; warnings registrados para Shot 3: sobrecarga `CreateOrder` obsoleta (existe la variante con `OrderEntry`), contadores `market_events/account_events` sin incrementar en este build (lane de market data no cableada en el AddOn de ejecución — su heartbeat los expone en 0, degradación visible).
- Instalación física: NO requerida ni ejecutada (mandato); el AddOn ejecución queda stageado como candidato Shot 3. El AddOn feed instalado sigue siendo el R3 @ f0c82905 (sin cambios en runtime NT).

## 6. Estado de despliegue DEV (verificado)

- **Relay:** `echo-nt-feed-relay` restart controlado → binario nuevo `/home/kor/opt/echo-dev/releases/170a4581…/nt-feed-relay` (`vcs.revision=170a4581… vcs.modified=false`, go1.27.1, SHA256 `3cacb2e7…36de24a`), PID 1388002, `NRestarts=0`. Journal: `binding_loaded=true`, reconexión física del AddOn con **`binding_match=RESOLVED` + `binding_id_drift=false`**, mercado fluyendo (`last_seq` creciente, `malformed=0`, `publish_errors=0`). Rollback documentado en `BUILD.md` de la release (repoint a `7af6210a`).
- **ETCD DEV:** `futures-bridge/accounts/E2T-GAU50-01/binding/provider-account-ref = "RJARA114411201551"` — escritura guardada (pre-lectura ABSENT obligatoria, SetVar, read-back exacto por el writer y lectura plana RO por MCP; 12 keys del binding, hermanas intactas; herramienta efímera eliminada, nunca commiteada). `futures-bridge/accounts` (lista de sesiones del bridge) **no existe** ⇒ sin sesiones (una lectura MCP temprana que reportaba `"17:00"` resultó un artefacto de matching difuso del MCP sobre `binding/day-boundary-reset`; el estado real se verificó con cliente etcd crudo por miembro).
- **Bridge:** sin binario desplegado ni proceso; `transport-id=NINJATRADER_BRIDGE` preexistente en la cuenta no tiene efecto sin la lista de sesiones.

## 7. Limitaciones conocidas y deuda

1. **Race preexistente (baseline f0c82905, no introducida por este shot):** `v3/futures-projector/adapters/kafka` falla con `-race` (`TestCommitOnlyAfterSuccessfulApply`, `TestRedeliveredKafkaRecordNoOpEndToEnd`) — verificada idéntica en el baseline limpio; sin tocar. La nota C1 §5.4 (`ReadCommitted` config del projector) sigue vigente como trabajo D6 futuro.
2. **Adapter NT `Capabilities` = todo UNKNOWN:** deliberado (G-ADAPTER/G-EGRESS-0). Cada claim es un gate físico Shot 3 nombrado en el código (G-ID-Retention, G-HORIZON, G-E2E, G-STOP). Los flips a PROVEN son cambio de Shot 3 con evidencia física.
3. **Síntesis 4×TRADE del warm-up:** implementada y verificada por fidelidad OHLC/warm-up (G-WARMUP software gate); la fidelidad contra barras NT REALES es el gate físico de Shot 3.
4. **Liveness bound de freshness sin calendario cableado** en el owner V1 (`marketExpectedActive=false`; documentado en código): el bound de lag ya cubre el escenario del freeze (feed demo ~600 s ⇒ STALE); el gate liveness queda para la integración de calendario.
5. **El feed AddOn instalado no se actualizó** (sigue R3): la inversión Name-primaria del feed AddOn viaja en source para el próximo ciclo owner-assisted (OD-D6-4); el defence activo hoy es el relay Name-primario + hello real (`RESOLVED` verificado). El AddOn de ejecución stageado incorpora ambas mejoras.
6. **Ventana evening 23:59:** la forma congelada half-open por día civil deja fuera el minuto 23:59–00:00 (borde de forma, documentado en el JSON; el edge mandatorio 15:50 CT es exacto).

## 8. Decisiones owner / contradicciones

- **OWNER_DECISION_REQUIRED: NONE** para este shot. OD-D6-2 (ratificación de valores GAU50-EVAL v1 antes del primer egress) permanece REQUIRED para Shot 3 según el freeze §16 — los valores materializados siguen la fuente aceptada, pero la ratificación es config-act owner.
- **CONTRADICTIONS: NONE** con el freeze. Desviación registrada: `external-contract-identifier` de la cuenta en ETCD es `"NQ 12-26"` (FullName NT) y no `NQZ6` — el adapter acepta cualquiera de las dos identidades en el mapeo de instrumento (config-only, sin cambio de contrato); registrado para reconciliación de config en Shot 3.

## 9. Handoff

```text
D6_SHOT1_IMPLEMENTATION =
READY_FOR_ADVERSARIAL_REVIEW

BASELINE:
f0c82905d4eaf825c08e04f0bb97cab73e616ba5 (origin/feature/d6-n1-readonly-vertical)

FINAL_SHA:
4b05d6f856df41b748ad2bfb1f0806b45349387f (origin/feature/d6-shot1-execution-vertical, push FF verificado)

ACCOUNT_IDENTITY:
PASS (3 capas: ref durable autoridad Validate fail-closed; relay Name-primario verificado en runtime físico RESOLVED+no-drift; AddOn inversion staged; ETCD ref escrita con read-back doble)

STOP_MARKET_STACK:
PASS (domain→engine→wire→envelope→journal/sameIntent→GerardMM→sim, regresiones verdes; protective resting STOP_MARKET con StopPrice asertado en sim; crossed→MARKET intacto)

NINJATRADER_EXECUTION_LANE:
PASS (echo.ntx.v1 con framing/auth/seq del canal certificado + command/command_result; server bidireccional testado; feed lane byte-inalterada y operativa)

EXECUTION_ADAPTER:
PASS (ExecutionAdapter completo; mapeo MARKET/LIMIT/STOP_MARKET contra superficie física 8.1.8.3 refleccionada; sin transformación de tipos; capability gate CLOSED: STOP_MARKET excluido hasta G-STOP, M2 mandatorio UNKNOWN)

M1_M2:
PASS (M1 intacto; M2: PREPARED y SUBMITTING durables antes de la escritura del lane — punto de no retorno; VENUE_BOUND sólo con evidencia venue de la familia orders; AMBIGUOUS en timeout/ERROR/lane-failure; jamás re-submit ciego — test exactamente-1-comando)

JOURNAL:
PASS (journalfs congelado reutilizado; sameIntent con nivel de stop; conflictos fail-visible; VENUE_BOUND/TERMINAL/AMBIGUOUS transiciones verificadas)

RECONCILIATION:
PASS (found→bind; ausencia→AMBIGUOUS fail-closed sin negación autoritativa en lane V1; historial→TERMINAL con fills recuperados dedup ExecutionId; UnknownLiveOrders quarantine fail-visible nunca cancelada/adoptada)

MARKET_FRESHNESS:
PASS (FRESH/STALE/UNKNOWN fail-closed sobre serving authority; UNKNOWN bloquea; lag 600 s ⇒ STALE ⇒ 0 señales + DENY_MARKET_NOT_FRESH con señal forzada; replay/backtest conservan semántica D5)

GAU50_RULESET:
PASS (GAU50-EVAL v1 ACTIVE con 3 SourceRefs; cap GROSS 6 por path frozen de reservation; 15:50 CT exacto por admission; DD/DLL/consistencia documentados NO codificados; guard anti-drift 6 mutaciones)

WARMUP_REBUILD:
PASS (síntesis 5m-exact determinista; envelopes clase C idénticos al relay; anchor sellado refs+digest; plan candidatos-antes-de-RUN_START; fidelidad E2E OHLC 5m/H4 byte-idéntica + warm-up values idénticos + manifest pinea anchor)

NINJATRADER_8_1_8_3_COMPILE:
PASS (shadow-compile físico de AMBOS AddOns contra las DLL instaladas: 0 errores; feed 0 warnings; execution warnings registrados para Shot 3; hashes byte-verify; ejecución NO instalada — staged Shot 3)

TESTS:
go test -race -count=1 scoped: v3/sdk/futures/... 100% ok; v3/futures-bridge/... 100% ok; v3/core functions+futuresruntime+futuresvertical(~8min)+config/futures 100% ok

COVERAGE:
core/ntx 87.3% · adapters/ninjatrader 78.3% · internal/binding 100% · warmup 97.5% · config/futures 78.9% (paquete); lógica nueva a nivel función ≈100% con ramas de deadline/lane-caída y accept-TCP declaradas no-medibles sin lane física (gates Shot 3); debt preexistente: futures-projector kafka -race (baseline f0c82905, sin tocar)

PHYSICAL_EGRESS:
DISABLED (lista de sesiones del bridge vacía; bridge sin correr; capability gate M2 UNKNOWN ⇒ SubmissionCapabilitiesReady=false testado; STOP_MARKET rechazado pre-journal; feed AddOn sin camino de comandos; execution AddOn stageado no instalado)

ORDERS_SENT:
0

ORDERS_MODIFIED:
0

ORDERS_CANCELLED:
0

OWNER_DECISION_REQUIRED:
NONE para este shot. (OD-D6-2 ratificación GAU50-EVAL v1 y OD-D6-1 autorización de egress físico permanecen REQUIRED para Shot 3, según freeze §16)

CONTRADICTIONS:
NONE con el freeze. Nota config: external-contract-identifier ETCD = "NQ 12-26" (FullName) — adapter acepta ambas identidades de instrumento; reconciliar en Shot 3

SHOT2_INPUTS:
(1) Doble-submit: revisar caminos timeout/redelivery/reconnect del adapter NT (§6.4 paso 4) y el suppression path del session dedup; (2) drift de Id y Name duplicado en resolución AddOn/relay (§3.2); (3) stale-feed enablement: cualquier camino a Signal o admission con STALE (S7: composición live-only, pinning del requester); (4) lifecycle del protective stop: tighten races, crossed-window, restart durante VENUE_BOUND stop (§5.5); (5) cancel/replace + late-fill races; (6) correctness del quarantine; (7) journal/sameIntent stop-level dedup; (8) entitlement/binding fail-closed; (9) valores GAU50-EVAL vs SourceRefs (OD-D6-2 pendiente); (10) fidelidad warm-up + anchor pinning; (11) authority creep del AddOn (§6.6) y scope creep vs §13; (12) race preexistente del futures-projector (fuera de alcance, registrada)

NEXT_MANAGER_ACTION:
Despachar D6 Shot 2 (adversarial review independiente sobre 4b05d6f8) sin cambios de código durante el review. Shot 3 permanece gated: OD-D6-1 (egress físico owner) + OD-D6-2 (ratificación de valores) + ladder físico G-REALTIME→G-STOP→G-ID-Retention→G-HORIZON→G-E2E→G-PERF. No emitir EF_D6_E2E_PASS.
```

---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Personal]]"
parent: "[[Polymarket Engine — MVP]]"
sprint:
start: 2026-09-20
due:
progress: 0
repo: "https://github.com/xKoRx/polymarket-engine"
jira:
prs:
aliases:
  - PE-030
  - Weather Forecast Mispricing
  - Weather
  - POC-S04
tags:
  - kind/project
  - area/personal
  - domain/trading
  - tech/polymarket
  - topic/prediction-markets
created: 2026-09-20
updated: 2026-09-20
---

# POC-S04 — Weather

> [!warning]+ PE-030 · proyecto y planner único · NO LIVE
> **Estado: `PE030_SPEC_AND_PLAN_READY_PENDING_ENGINE_INTEGRATION`** · Implementación `0%` · Research estadístico `NOT_VALIDATED` · Mercado real `REAL_MARKET_BLOCKED` · Datos reales `REAL_DATA_BLOCKED` · Fee real `REAL_UNVERIFIED` · Alpha `UNPROVEN` · LIVE `FORBIDDEN`. Fundaciones SFG-01/02/03/04/05/07 `INTEGRATED_PASS` sobre el INTEGRATION_SHA `9d0512a` (branch local `feature/shared-poc-unblocker`, sin push, Review owner pendiente); el arranque del coding agent requiere `PE030_START_ALLOWED` del manager. Esta nota contiene SPEC, matriz transversal, decisiones, fixtures y mandato. Los WPs Weather NO implementan cambios compartidos que otro owner deba cerrar primero.

## 🎯 Objetivo

POC offline, causal, determinista y falsable: un contrato meteorológico explícito + forecast ensemble íntegro conocido antes del frame → P(bucket) no calibrada → fair value diagnóstico → Economics del engine sobre precios/depth/fees as-of → assessment y eventual candidato sujeto a Risk → SCREEN / Strategy REPLAY / SHADOW virtual cuando sus datos son válidos. Nada de órdenes live, PnL fabricado ni conclusiones OOS desde fixtures. Engine durable reutilizable; Weather sólo implementa su diferencia meteorológica.

## 📊 Estado actual — reconciliación del 20-09-2026

**Autoridad separada:** `main@9ae5ddec1a0e52fdc0bbde608cd0504e644d05a5` = M4 certificado base; `feature/research-strategies-v01@25f578a502ce0c9e1ad27a93537a868a94533b34` = HEAD REMOTO de Research Strategies verificado mediante GitHub branch y source. El commit feature es checkpoint RS-V03 Fase C de Sports: snapshot intermedio de captura que seguía activa al hacer commit; **no certifica el resultado de la captura ni PE-030**. HEAD/worktree locales y cambios posteriores no visibles: `LOCAL_VERIFICATION_PENDING`, comparar nuevamente antes de comenzar. Baseline `7bd264d` histórico, NO autoridad. Investigación Weather recibida `2026-09-20T03:24Z` sigue siendo autoridad de dominio donde no contradiga source; su diagnóstico antiguo de remoto sólo README y SCREEN neutral-only queda explícitamente SUPERSEDIDO.

**Shared foundations verificadas físicamente por PE-030 (2026-09-20, sesión de regularización):** [[Polymarket Engine — POC Shared Unblocker]] entregó INTEGRATION_SHA `9d0512a912fcce4b9aefc152c7a89b090ff8df1d` y esta POC lo verificó contra el repo real: branch local `feature/shared-poc-unblocker` tips exactamente `9d0512a` en el worktree `polymarket-engine-shared`; commits SFG presentes en orden (`e01cb5a` SFG-07, `b61837c` SFG-01, `f1b05dc` SFG-02, `456c052` SFG-05, `7deea48` SFG-04, `1483aeb` SFG-03, `546f827` SFG-06, `38b8fb2` C2, integración `9d0512a`); contratos inspeccionados por símbolo sobre ese SHA (`internal/external/external.go::{Request,Admitted,Admit,AdmitSync,Load,Project,ErrFutureVintage,ErrContradictory,ErrInvalidIdentity,EnvelopeSchemaV1}`, `protocol.SurfaceExternal`, `strategy.Frame.Externals` + `DataRequirements.ExternalSources`, `strategy.FrameObserver/FrameObservation` en `observation.go`, `marketview.Projection::{New,Apply}`, `dataset.Guard`, `regimes.FeeSchedule/LevelCost`, `economics.BuildQuoteScheduled` en `scheduled.go`, `simulator.FillAtScheduled`, `experiment.RunStrategyReplay` en `strategy_replay.go` + `DECLARED_L2`); checkout principal de `feature/research-strategies-v01` = `f070496` limpio; **sin push** (remoto queda `origin/feature/research-strategies-v01@25f578a`; la branch shared NO existe en origin); sin procesos engine vivos; `.rs-v03-sports/` y `.rs-v03-negrisk/` intocados. Estado de integración: `INTEGRATION_SHA_PUBLISHED_PENDING_OWNER_REVIEW` — puente del padre en `[r]`, módulos shared congelados hasta Review y sin merge a `feature/research-strategies-v01`. Readiness heredado de la nota shared: PE-030 `READY_WITH_RESTRICTIONS` (SFG-01/02/03/04/07 requeridos PASS; 05 opcional para abstención); restricciones: semántica meteorológica (station/buckets/ensemble/normalización) ownership exclusivo PE-030, sin proveedor real ni I/O dentro de Strategy, fee venue `REAL_UNVERIFIED` (sólo `SYNTHETIC_FIXTURE`), M4 recertificado @ `9d0512a` `M4_CERTIFIED_NON_LIVE` 27/0/0/5 con aceptación manager pendiente. Baseline de arranque = `9d0512a` (o sucesor validado por el manager), condicionado a `PE030_START_ALLOWED`; primer WP: adapter Weather → `external_observation_v1` vía `external.AdmitSync` (WP B1); prohibido reimplementar admission/external, L2, replay/shadow, fees o dataset guard; handoff completo en la nota shared.

**Regla frozen padre** `[[Polymarket Engine — MVP]]`: Strategy sólo aporta su edge; discovery, books, Capture, Replay, Economics, Risk, Simulator, SHADOW, account y observabilidad son del engine. El padre reserva el External data seam («primera implementación concreta sólo cuando una POC promovida la necesite») y declara `ExternalObservation{source,source_key,event_time,receive_time,payload_version,quality}`: Weather es la POC promovida que activó ese seam, materializado por SFG-04 como `internal/external` con envelope `external_observation_v1` (esto SUPERSEDE el hallazgo «el diseño no constituye código», que era válido sólo contra `25f578a`). La semántica del payload (`weather.obs.v1`: estación, variable, unidad, ventana válida, miembros, pesos) es Weather-owned; el transporte/admisión NO se redefine. No crear framework universal ni esconder payload en Extras, Quality o Parameters.

**Source inspeccionado en branch exacta:** `cmd/engine/screen.go::{screenFactories,openScreenPipeline,loadJournal,routeNext,toStrategyFrame,applyOwnerRecord,depthExtras,runScreenConsolidated}`; `cmd/engine/screen_consolidated_test.go::TestConsolidatedTwoInstancesIsolatedAndDistinguishable,TestConsolidatedRunsBothPOCsEndToEnd`; `internal/strategy/api.go::{Strategy,Factory,Frame,DataRequirements,EvaluationContext,Assessment,ActionCandidate}`; `internal/strategy/pocs/pocdata/pocdata.go::{TopLevels,DepthFresh,DecodeSide}`; `internal/frames/frames.go::{AssetSnapshot,DeliveryFrame,RevisionRef}`; `internal/economics/economics.go::{WalkSide,ExecutableDepth,BuildQuote}`; `internal/regimes/feeresolver.go::{FeeEvidence,ResolveFee,FeeResolution}`; `internal/experiment/experiment.go::{RunManifest,Scorecard,RunShadow,shadowStrategyFor,fillCandidate,scorecardHash}`; `internal/replay/{replay.go,manifest.go}`; `internal/protocol/{protocol.go,marketws.go}`; `internal/capture/{capture.go,envelope.go}`; `internal/strategy/pocs/sports/sports.go`; además documentación frozen del padre. **Inspección estática, no go test/CI, no local checkout, no captura tocada.** Evidencia exacta en Docs/Links.

**Hallazgos de la inspección @ `25f578a` (revisión RS-v03) y su resolución sobre `9d0512a`:**
- SCREEN registra Neutral, NegRisk y Sports; `screen-consolidated` reutiliza un `screenPipeline` y ejecuta instancias aisladas. Los records marketws se enrutan incrementalmente entre cuts; tests de aislamiento y ambas POCs existen. Registración Weather sigue siendo extensión pequeña de registry, NO nuevo SCREEN. VIGENTE.
- `strategy.Frame` sin externals, `DataRequirements` sin external data, `protocol.Surface` cerrado y `screenPipeline.loadJournal()` filtrando sólo marketws → **RESUELTO por SFG-04 @ `9d0512a`**: `SurfaceExternal` aditiva, `Frame.Externals` proyectada por `external.Project` con causalidad `CaptureSeq <= CutSeq`, `DataRequirements.ExternalSources` obliga a declarar la fuente (fuente declarada ausente ⇒ instancia no arranca); compatibilidad con journals previos probada por la suite shared.
- `pocdata.TopLevels=6` full-book-only, deltas ignorados (depth fantasma), `Revision:1` fijo → **RESUELTO por SFG-01 @ `9d0512a`**: proyección owner compartida `marketview.Projection` aplica `price_change`, reemplaza niveles ante full book, revoca por epoch, maneja libros sospechosos y expone vistas L2 tipadas (`pocdata.ViewFromSnapshot/L2View/Capacity`) con estados Fresh/Stale/NoBase, capacidad y shortfall explícitos, truncamiento declarado y digests canónicos; fanout multi-asset por secuencia de captura. Weather NO construye una segunda vista L2.
- `economics.BuildQuote` con fee plana BPS×notional sin price-dependence → **RESUELTO por SFG-02 @ `9d0512a`**: `regimes.FeeSchedule` versionado (`SchedulePriceSquare`, `Provenance: SYNTHETIC_FIXTURE|REAL_UNVERIFIED`, coste `rate·p^e·(1−p)^e·take` por nivel, truncado 6dp), `economics.BuildQuoteScheduled/WalkSideDetailed` y `simulator.FillAtScheduled` con paridad quote↔simulator y oráculo aritmético `big.Rat` independiente. La fee real del venue sigue `REAL_UNVERIFIED` (gap U-02 abierto en la nota shared): Weather usa fees sintéticas explícitas y jamás presenta resultados como economía real certificada.
- `replay.RunObservation` no re-ejecutaba Strategy; SHADOW con fallback BBO×10 y fee unresolved → **RESUELTO por SFG-03 @ `9d0512a`**: `experiment.RunStrategyReplay` re-ejecuta Detect/Evaluate sobre frames journalizados y compara contra observaciones durables (determinismo a dos corridas, verificación de integridad previa); `RunManifest.Execution="DECLARED_L2"` elimina el fallback para estrategias declaradas (ACCEPT sin legs ⇒ `ExecutionBlocked`, nunca fill sintético); fee resuelta por activo; defecto preexistente de sombra `basketID` en `fillCandidate` corregido (`1483aeb`). SHADOW sigue siendo ejecución virtual: no envía órdenes al venue ni demuestra rentabilidad realizable.
- `new_market` raw/`Documented=false` → VIGENTE como NO-dependencia: tipado conservador y dedup de notices llegaron por SFG-06 (PARCIAL, `WS_COHORT_BLOCKED`, alcance exclusivo PE-004-W); `NOT_REQUIRED_BY_PE030_V1` sin cambios.
- `capture.Open` sin guard contra datasets activos → **RESUELTO por SFG-07 @ `9d0512a`**: `dataset.Guard` (identidad realpath + aliases symlink + manifests de contenido) cableado antes de `capture.Open` en screen/shadow; Weather lo reutiliza y jamás abre `.rs-v03-*`.

## 🧱 Entrega de desarrollo

| Repo | Branch | Base verificable | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| `xKoRx/polymarket-engine` | arranque desde `feature/shared-poc-unblocker` local `9d0512a912fcce4b9aefc152c7a89b090ff8df1d` (worktree `polymarket-engine-shared`, sin push, Review owner pendiente); sucesor sólo si el manager publica un `INTEGRATION_SHA` validado | `9d0512a` (rebase 8/8 sobre `f070496`; M4 recert 27/0/0/5 @ `9d0512a`, aceptación manager pendiente) | [SPEC funcional](#spec-funcional-v1) | [SPEC técnica](#spec-técnica-v1) | `SPEC_AND_PLAN_READY_PENDING_ENGINE_INTEGRATION`; SFG-01/02/03/04/07 `INTEGRATED_PASS@9d0512a`; arranque gated por `PE030_START_ALLOWED` |
| `xKoRx/agents-os` | `master` remoto; local no inspeccionado | este planner actualizado por commit independiente | esta nota | matriz + mandato aquí | nota única, no se modifica padre ni proyectos vecinos |

## 🧩 Subproyectos

Ninguno. PE-001 Sports Combinatorial NO es `poc-sports`: éste es PE-005-R1 Sports Reversion según `sports.StrategyID/HypothesisID`. Compartir infraestructura, no mezclar hipótesis.

## ✅ Tareas — planner único

> [!note]+ Estados y ownership
> Todos `[ ]` hasta evidencia real del coding agent. No pasar progress de 0 por research; registrar SHA, tests, paths y recibos en bitácora. Verificación read-only 2026-09-20: NO existe tarea puente POC-S04 en el padre (sólo la del Shared Unblocker, en `[r]`) ⇒ `PARENT_BRIDGE_PENDING`; crearla es acción del manager, no de este mandato. Nunca cerrar sesión completa salvo pedido explícito.

- [ ] **A0 | Autoridad y preflight:** re-verificar al arranque HEAD local y tip de `feature/shared-poc-unblocker` contra `9d0512a` (drift), permiso explícito `PE030_START_ALLOWED`, Review owner del shared (puente `[r]`→`[x]`), worktrees/writers concurrentes, data-dir seguro vía `dataset.Guard`, y fijar allowed-files reales por WP. La verificación física del SHA y de los símbolos SFG ya fue ejecutada por la sesión de regularización (bitácora 2026-09-20); NO redescubrir RS v0.1/0.2 ni re-validar los gates shared. #owner/agent #type/research #area/personal
- [ ] **A1 | Weather puro:** contratos, intervalos, validaciones, vintages, ensemble empírico, razones y F01–F16. Sin dependencia del provider ni core frozen. #owner/agent #type/dev #area/personal
- [ ] **B1 | Admission Weather fixture (PRIMERA TAREA):** adapter/codec Weather en paquete propio → `external.Request{Source:"weather-fixture", SourceKey, SchemaVersion:"weather.obs.v1", ReferenceTime=vintage del run, AvailableAt=provider_available_at, Payload, Quality}` → `external.AdmitSync` (envelope `external_observation_v1`, known-at engine-stamped, capture seq durable) → frame vía `external.Project`; tests de la capa Weather F03/F16/F20 + razones WX (las pruebas mecánicas de admisión —vintage futuro, hash, dedup, contradicción, restart, replay del canal— pertenecen a la suite shared y NO se duplican); no recorder propio ni I/O en Strategy. #owner/agent #type/dev #area/personal
- [ ] **B2 | Strategy + SCREEN:** Factory Weather en paquete propio, `DataRequirements.ExternalSources:["weather-fixture"]`, detect/evaluate sobre `Frame.Externals`, book vía `pocdata.ViewFromSnapshot/L2View/Capacity` (SFG-01), quote vía `economics.BuildQuoteScheduled` + `regimes.FeeSchedule{Provenance:SYNTHETIC_FIXTURE}` (SFG-02), Risk real demostrado, F02/F17–F19/F21/F22; edición del registry (`screenFactories`/`shadowStrategyFor`) sólo con ownership otorgado por el manager. #owner/agent #type/dev #area/personal
- [ ] **C1 | Strategy REPLAY/SHADOW/QA:** `experiment.RunStrategyReplay` (SFG-03) con manifest versionado, dos schedules con mismo digest, F01–F22 y properties, SHADOW `Execution="DECLARED_L2"` sólo Candidate.Legs + `simulator.FillAtScheduled`, sin fallback ni PnL inventado; abstenciones vía `FrameObserver` (SFG-05, opcional) para F03/F15/F20; go test/vet/race/regresión/cobertura, `dataset.Guard` y owner review. #owner/agent #type/dev #area/personal

## Matriz de shared foundation gates — SFG (estados verificados físicamente por PE-030 sobre `9d0512a`, 2026-09-20)

Estados: `INTEGRATED_PASS` = implementado y probado sobre el INTEGRATION_SHA real `9d0512a` (receipts de la nota shared re-ejecutados por su sesión de integración + símbolos verificados por esta POC); la integración a `feature/research-strategies-v01`, el push y la aceptación owner siguen pendientes ⇒ módulos shared READ-ONLY para Weather hasta Review. `WEATHER_OWNED` = trabajo específico de PE-030 todavía no implementado.

| Gate | Estado @ `9d0512a` | Evidencia física verificada | Obligación Weather |
|---|---|---|---|
| **SFG-01 — CAUSAL_L2** | `INTEGRATED_PASS` | `internal/marketview/projection.go::{New,Projection.Apply}` delta-aware (price_change aplicado, full book reemplaza niveles, revocación por epoch, libros sospechosos), vistas L2 tipadas `pocdata.ViewFromSnapshot/L2View/Capacity/FrameViews/Digest` con Fresh/Stale/NoBase, capacidad/shortfall honestos, truncamiento declarado, digests canónicos, fanout multi-asset; `cmd/engine/sfg01_l2_test.go`; commit `b61837c`. | Consumir las vistas; jamás segunda proyección L2, latest-lookup ni fallback BBO→size; abstain ante Stale/NoBase/shortfall. |
| **SFG-02 — FEE_CONTRACT** | `INTEGRATED_PASS` | `regimes.FeeSchedule` versionado + `LevelCost` (`schedule.go`), `economics.BuildQuoteScheduled/WalkSideDetailed` (`scheduled.go`), `simulator.FillAtScheduled` con paridad quote↔simulator; oráculo `big.Rat` independiente (`internal/regimes/schedule_test.go`, `internal/economics/sfg02_fee_test.go`, `internal/simulator/sfg02_parity_test.go`); commit `f1b05dc`. Fee venue real `REAL_UNVERIFIED` (U-02 ABIERTO): la procedencia `REAL_UNVERIFIED` no puede convertirse en `REAL_FEE_READY`. | Sólo `Provenance:SYNTHETIC_FIXTURE` declarada; resultados offline nunca se presentan como economía real certificada. |
| **SFG-03 — RESEARCH_RUNTIME** | `INTEGRATED_PASS` | `experiment.RunShadow` con `Execution="DECLARED_L2"` (sin fallback BBO; ACCEPT sin legs ⇒ `ExecutionBlocked`), fee por activo, `experiment.RunStrategyReplay` (`strategy_replay.go`) re-ejecutando evaluaciones contra observaciones durables a dos corridas con verificación de integridad; stubs de las tres clases de consumidor en `sfg03_consumers_test.go`; commit `1483aeb`. | Registrar Weather sobre el runtime existente; SHADOW estrictamente virtual; prohibido runtime nuevo o fills fabricados. |
| **SFG-04 — EXTERNAL_OBSERVATIONS** | `INTEGRATED_PASS` | `internal/external/external.go::{Request,Admitted,Admit,AdmitSync,Load,Project}` + `ErrFutureVintage/ErrContradictory/ErrInvalidIdentity`, envelope `external_observation_v1`, `protocol.SurfaceExternal`, `strategy.Frame.Externals` + `DataRequirements.ExternalSources`, proyección causal por `CaptureSeq<=CutSeq`, hash re-verificado al cargar, idempotencia por `(source,key,hash)`, rechazo de vintages futuros, compatibilidad de manifests previos; `internal/external/admission_test.go` + `cmd/engine/sfg04_external_test.go`; commit `7deea48`. Mapeo Weather congelado en «Contrato de admission Weather» (SPEC técnica). | Adapter/codec y semántica `weather.obs.v1` Weather-owned; el canal compartido NO se redefine ni duplica. |
| **SFG-05 — DESCRIPTIVE_OUTPUT** | `INTEGRATED_PASS` (opcional para Weather) | `strategy.FrameObserver/FrameObservation` (`observation.go`, schema `sfg05_v1`), observación durable por frame incluso con 0 oportunidades, scorecard sin last-wins (`ObservationCount/ObservationDigests`, hash legacy estable); `runtime_sfg05_test.go` + `shadow_sfg05_test.go`; commit `456c052`. | Sólo para diagnósticos de abstención F03/F15/F20; no crear Opportunities falsas para emitir métricas. |
| **SFG-06 — MARKET_LIFECYCLE** | `NOT_REQUIRED_BY_PE030_V1` | PARCIAL shared (`546f827`): tipado conservador `MarketWSNewMarket` + dedup `ParseNewMarketNotice/NoticeDedup/IdentityKey` PASS sobre muestras auténticas; Catalog projection/UniverseChanged/replay E2E `WS_COHORT_BLOCKED` con correctivo separado (owner: shared tras Review, o manager). | NO dependencia de PE-030; no tocar lifecycle desde Weather. |
| **SFG-07 — ISOLATED_DATASET** | `INTEGRATED_PASS` | `internal/dataset/guard.go::{Guard}` (identidad realpath + aliases symlink) + `manifest.go` con manifests de contenido; cableado antes de `capture.Open` en screen/shadow; `TestGuardRefusesActiveDirAndAliases`, `TestSFG07ActiveDirRefused`; commit `e01cb5a`. | Reutilizar el guard; datasets Weather siempre nuevos en t.TempDir desde fixtures sintéticas; jamás `.rs-v03-*` ni copias calientes de SQLite+WAL. |

### Capabilities reutilizables — NegRisk / Sports Reversion / base M4

| CAPABILITY | SOURCE SYMBOL + PROVEN BY (@ `9d0512a`) | WEATHER REUSE? | NOTA |
|---|---|---|---|
| Strategy/Factory/actor isolated | `strategy.Strategy/Factory/NewInstance`, `screenFactories`, `TestConsolidatedTwoInstancesIsolatedAndDistinguishable` | SÍ runtime | sólo registrar Weather (registry es manager-owned) |
| SCREEN multi-instance + forward cuts | `openScreenPipeline/routeNext/runScreenConsolidated`, tests `TestConsolidatedRunsBothPOCsEndToEnd` | SÍ pipeline | registro Weather; no reconstruir |
| Causal book durable + L2 as-of-cut | `books.Engine`, `marketview.Projection`, `pocdata.ViewFromSnapshot/L2View/Capacity` (SFG-01 PASS) | SÍ vistas | delta-aware y con shortfall honesto; prohibida una segunda vista Weather |
| Depth observed codec | `pocdata` (SFG-01 PASS) | SÍ vía vistas compartidas | Weather no invoca el codec crudo ni interpola depth |
| Economics con fee schedule | `economics.BuildQuoteScheduled/WalkSideDetailed`, `regimes.FeeSchedule/LevelCost` (SFG-02 PASS) | SÍ funciones puras | fee sintética `SYNTHETIC_FIXTURE`; fee venue `REAL_UNVERIFIED` |
| Simulator / virtual Account / basket | `simulator.FillAtScheduled`, `experiment.fillCandidate`, `account.NewCoordinator/PlanBasket` | SÍ infraestructura virtual | candidato leg completo; fallback BBO eliminado en `DECLARED_L2` |
| Risk | `risk.Policy/Snapshot` presentes en `experiment.RunShadow` | parcial: tipos disponibles, no asumir gate efectivo | demostrar enforcement real con test antes de afirmar Risk certificado Weather |
| Replay de evaluaciones | `experiment.RunStrategyReplay` (SFG-03 PASS) | SÍ runner compartido | determinismo a dos schedules; `capture.Verify` previo |
| SHADOW declarado | `experiment.RunShadow` `Execution="DECLARED_L2"` (SFG-03 PASS) | SÍ runner compartido | fills sólo desde `Candidate.Legs`; ACCEPT sin legs ⇒ `ExecutionBlocked` |
| Experiment manifest/scorecards | `experiment.RunManifest/Scorecard/scorecardHash` + `ObservationDigests` (SFG-05 PASS) | SÍ estructura de experiment | digest cubre observaciones descriptivas; cero oportunidades deja salida durable |
| Reasons/metrics | `strategy.Assessment{ReasonCodes,Metrics}` + `FrameObserver` (SFG-05, opcional) | SÍ | WX codes sólo en Weather; abstención sin Opportunity vía observer |
| External observations | `internal/external` (SFG-04 PASS) | SÍ canal compartido | adapter/codec Weather en paquete propio; canal NO se duplica |
| Dataset isolation | `dataset.Guard` (SFG-07 PASS) | SÍ guard compartido | cableado antes de `capture.Open`; t.TempDir siempre |
| Market lifecycle | `protocol.MarketWSNewMarket` PARCIAL (SFG-06) | NO NECESARIO | PE-004-W exclusivamente |

### Contrato de admission Weather — mapeo al envelope compartido (frozen; el canal SFG-04 ya está entregado)

**SUPERSEDE la «especificación mínima obligatoria para owner compartido» que esta POC redactó antes de la entrega shared:** aquella era una propuesta de seam; el contrato real puede diferir en detalles y manda (propuesta preservada en el historial de esta nota y en `80-agents/journal/logs/`). Contrato entregado @ `9d0512a` (fuente: `internal/external/external.go`): `Request{Source,SourceKey,SchemaVersion,ReferenceTime,AvailableAt,Payload []byte,Quality}` → `Admit/AdmitSync` stamping `KnownAt` (engine, UTC, jamás del caller) y `PayloadHash=sha256(payload)` → durable en lane EVIDENCE / clase RESEARCH_EVIDENCE con surface `external` y `RequestID="external=<source>;<key>;<hash12>"`; `Load` re-verifica el hash de cada record durable; `Project(records,cutSeq)` devuelve exactamente los records con `CaptureSeq<=CutSeq`, dedup por `(source,key)` — re-admisión idéntica colapsa, mismo key con hash distinto es `ErrContradictory` fail-closed — y proyecta a `strategy.ExternalFact{Source,SourceKey,SchemaVersion,ReferenceTime,KnownAt,PayloadHash,Quality,Payload,CaptureSeq}`. Errores tipados: `ErrFutureVintage` (ReferenceTime posterior a la admisión), `ErrContradictory`, `ErrInvalidIdentity`.

**Mapeo Weather frozen (adapter B1):**

| Campo envelope | Valor Weather | Regla frozen |
|---|---|---|
| `Source` | `weather-fixture` (POC offline) | identidad de fuente estable; un proveedor real futuro será un `Source` nuevo, nunca un re-cast del fixture |
| `SourceKey` | `<contract-id>/<station>/<variable>/<local-date>/<run_ref>` (ej. `SYN-WX-20260920-HIGH-UTC/SYN-EGLC/DAILY_MAX_TEMPERATURE/2026-09-20/20260919T00Z`) | incluye run_ref: vintages distintos ⇒ keys distintos (una revisión posterior jamás re-escribe el key de un run previo — eso dispararía `ErrContradictory`); re-admisión idéntica del mismo run ⇒ idempotente |
| `SchemaVersion` | `weather.obs.v1` | schema del payload Weather-owned y versionado; cambiar la forma ⇒ `weather.obs.v2` |
| `ReferenceTime` | referencia del run de forecast (vintage/issuance) | debe ser ≤ admisión (`ErrFutureVintage` si no); jamás la ventana válida futura del evento |
| `AvailableAt` | `provider_available_at` del run | obligatorio en Weather (no apoyarse en el fallback del engine que usa ReferenceTime si viene zero); la capa Weather verifica `AvailableAt <= KnownAt` y `AvailableAt <= frame.VirtualTime` |
| `Payload` | JSON verbatim `weather.obs.v1`: `{variable,unit,station_id,target_local_date,timezone,valid_window:[start,end),aggregation,run_ref,members:[{id,weight,value}],weights_model,quality_flags}` | bytes canónicos ⇒ `PayloadHash` sha256; todo lo meteorológico vive aquí, nunca en Extras/Quality/Parameters |
| `Quality` | etiqueta declarada `OK|PARTIAL|SUSPECT` | no es canal de payload |
| `KnownAt` | engine-stamped en admisión | identidad causal: join con el frame vía `CaptureSeq <= CutSeq` |
| `CaptureSeq` / `PayloadHash` | devueltos por `Admitted` | referencia durable obligatoria en manifest y digests |

**Distinción de timestamps (regla frozen):** `ReferenceTime`/run_ref (cuándo se emitió el forecast) ≠ `AvailableAt` (cuándo el proveedor lo publicó) ≠ `KnownAt` (cuándo el engine lo admitió) ≠ `valid_window` (a qué ventana del mundo aplica; dentro del payload) ≠ `frame.VirtualTime` (cut). Ninguno sustituye a otro; toda igualdad entre ellos debe ser una regla de contrato probada. Causalidad garantizada por el canal: un forecast admitido después del cut jamás aparece en ese frame (proyección por `CaptureSeq<=CutSeq` sobre journal inmutable — una revisión posterior no reescribe la información disponible en cuts históricos), vintage futuro rechazado en admisión, hash inválido impide admisión/carga, duplicado idéntico idempotente, contradicción falla cerrada, fuente requerida ausente ⇒ la instancia no arranca (vía `DataRequirements.ExternalSources`) o `WX_SOURCE_UNAVAILABLE` según el punto de fallo, y restart/replay preserva identidad y resultado (hash re-verificado al cargar). El adapter puede hacer I/O sólo durante ingestión/admisión (leer la fixture en el composition del test); Detect/Evaluate es puro: sin proveedores meteorológicos, sin filesystem, sin clock.

## MUST RESOLVE BEFORE CODING AGENTS START — estado transversal tras la entrega shared

| Orden | Gate / problema concreto | Estado | Owner / condición |
|---|---|---|---|
| 1 | Review humana de la branch shared + push/merge del `INTEGRATION_SHA 9d0512a` (o su sucesor validado) | `PENDING_OWNER_REVIEW` (puente del padre en `[r]`) | Manager/owner humano: validar receipts, integrar el árbol resultante y publicar el `INTEGRATION_SHA` definitivo; módulos shared congelados hasta entonces |
| 2 | Autorización explícita `PE030_START_ALLOWED` para arrancar el coding agent | `NOT_GRANTED` | Manager: sólo tras (1); sin ella el agent NO modifica el engine (documentación/fixtures aislados sólo con alcance autorizado expresamente) |
| 3 | Edición del registry (`screenFactories`/`shadowStrategyFor`) para registrar Weather | `MANAGER_OWNED` | Manager lo ejecuta u otorga permiso puntual en B2; Weather no abre el seam por su cuenta |
| 4 | Aceptación manager de la recert M4 @ `9d0512a` (`M4_ACCEPTANCE_PENDING`) | `PENDING` | Decisión humana; no bloquea la POC sintética offline y NO se convierte en `M4_CERTIFIED` heredada |

Resuelto por la entrega shared @ `9d0512a` (antes PRECONDITION en esta nota): SFG-04 external→durable→Frame→Strategy→replay; SFG-01 contrato L2 as-of-cut delta-aware; SFG-02 fee schedule versionado con oráculo independiente y paridad simulator; SFG-05 output descriptivo sin oportunidades; SFG-07 guard de datasets. No queda ningún bloqueador shared en la ruta crítica de PE-030; la POC offline sintética no depende de `new_market` ni de la cohorte W de PE-004.

## CAN BE RESOLVED INSIDE WEATHER — sin colisión

Contrato de market meteorológico, estación exacta, variable/unidad/timezone/ventana/DST, bucket algebra/Other, forecasts/vintages, ensemble weights/probabilidad no calibrada, quality flags Wx, interpretación de modelo→resolution domain, fixtures F01–F20 y codec Weather-specific bajo `internal/strategy/pocs/weather/**` (nombre final a validar en A0). Adapter **fixture-backed Weather** se acopla al seam SFG-04 ya entregado, no redefine capture. Gamma IDs reales, rounding/timezone contractual Londres, provider histórico/terms/bias quedan como real-data/validation-only; no impedir núcleo offline. Sin observaciones sintéticas presentadas como reales.

## Blocker ledger depurado

| Legacy ID | Clasificación nueva | Estado/acción |
|---|---|---|
| B-ENG-01 | `RESOLVED_BY_REGULARIZATION_2026-09-20` | HEAD local `f070496` + tip shared `9d0512a` verificados físicamente, checkout limpio, sin writers concurrentes; A0 conserva sólo un drift-check barato al arranque. |
| B-ENG-02 | `RESOLVED_BY_RS` para supuesto neutral-only; `RESOLVED_BY_SFG-04` para external; `RESOLVED_BY_SFG-01` para L2 | cerrado sin duplicar blockers; el estado vigente vive en la matriz SFG. |
| B-RULE-01 | `REAL_DATA_ONLY` | IDs Gamma/Condition/assets, regla exacta timezone/rounding/fallback/revision. Londres REFERENCE_ONLY. |
| B-EXEC-01 | `RESOLVED_BY_SFG-01` + `RESOLVED_BY_SFG-02`; metadata real `REAL_DATA_ONLY` | fee venue real sigue `REAL_UNVERIFIED` (U-02 abierto); market-specific fee/tick/min-size/book permanecen real-only. |
| B-DATA-01 | `VALIDATION_ONLY` (historia de miembros) + prospective data `REAL_DATA_ONLY` | no backfill pseudo-point-in-time; capturar vintages nuevos cuando autorizado. |
| B-LIC-01 | `REAL_DATA_ONLY` | licencia comercial/terms, station-grid correction; no gasto ni permisos requeridos para fixtures offline. |
| B-OPS-01 | `RESOLVED_BY_SFG-07` | `dataset.Guard` cableado; generación dataset sintético nuevo en t.TempDir; no tocar `.rs-v03-*`. |

## SPEC funcional v1 — Weather exclusivo, frozen para núcleo offline

**Tesis:** ensemble disponible y reproducible antes de cada cut puede diferir de precios ejecutables, sin asumir superioridad. Universo inicial sintético `SYN-WX-20260920-HIGH-UTC`, nunca market real. Candidatos reales documentados: Londres high/low, Helsinki high, Shanghai high Sep 20 2026. Londres-high reference `https://polymarket.com/event/highest-temperature-in-london-on-september-20-2026`, estación contractual EGLC, NOAA/NWS metric `https://www.weather.gov/wrh/timeseries?site=eglc`, brackets observados <=16,17…25,>=26 °C. Faltan IDs Gamma/conditions/assets, TZ exacta de day, transformación entero/rounding, fee/book → real INELIGIBLE. A resolución NOAA, B pronóstico Open-Meteo Ensemble (grilla ≠ EGLC), C label settlement contractual; mantener distintos. Forecast histórico member-level insuficiente: captura prospectiva después, no validación estadística mañana.

**Success offline:** `WeatherContract→admission causally valid→ensemble complete→bucket probabilities→model fair value→valid depth+fee→assessment/risk→SCREEN`, mismos artifacts y outputs en Strategy REPLAY y SHADOW con candidate legs reales del fixture; INCONCLUSIVE si fee/spatial/contract desconocidos. Nada de orders, ML grande, Gaussian inventada, recorder exclusivo, data lookup/clock/HTTP en callbacks ni resolución final como feature. Walk-forward OOS/Brier/log loss/reliability/net executable economics/capacity/capital lock son experimento POSTERIOR, no gate de POC sintética.

## SPEC técnica v1

### WX-BASE-V1 — sintético completo, sin licencia ni API

Event `SYN-WX-20260920-HIGH-UTC`; five separate binary Markets `SYN-M-B0..B4`, Conditions `SYN-C-B0..B4`, YES `SYN-Y-B0..B4`, NO `SYN-N-B0..B4`; estación `SYN-EGLC`, `DAILY_MAX_TEMPERATURE`, source synthetic integer Celsius **already published domain (NO rounding)**; local `2026-09-20`, zone `UTC`, half-open `[2026-09-20T00:00:00Z,2026-09-21T00:00:00Z)`, aggregation max. Buckets exhaustive on integer domain: B0 `<=18`, B1 `=19`, B2 `=20`, B3 `=21`, B4 `>=22`. Source missing ⇒ no payout invented. Rule revision immutable known_at <= frame. Station/source exact equality.

Vintage base reference `2026-09-19T00:00Z`, available `06:10Z`, received `06:11Z`, frame `12:00Z` same date; ten complete uniform model-weight members maxima `[18,19,19,20,20,20,21,21,22,23]`; probabilities `[.10,.20,.30,.20,.20]` exactly. YES ask books: B0 `0.12×100`, B1 `0.19×100`, B2 `0.24×20`+`0.27×80`, B3 `0.205×100`, B4 `0.21×100`. Default buy 10 shares. Synthetic fee ONLY `shares×0.05×price×(1-price)`; one-level B2 0.24 effective 380bps on notional; B2 notional 2.40, fee .0912, expected payout 3.00, net +.5088 / +.05088/share. B4 expected payout 2.00 < notional 2.10 ⇒ REJECT. F19 at ask .29: notional 2.90, gross +.10, fee .10295, net -.00295. **Synthetic arithmetic not market edge**; no universal feeRate assumed. Multi-level fee remains SFG-02 if needed.

**Typed concepts** (reuse actual HEAD types, names not structs frozen): `WeatherMarketContract`: event/market/condition/yes/no asset IDs, bucket, rules revision/hash known_at, payout source/station/variable/unit/domain, rounding enum, IANA timezone+local date+window, aggregation/fallback/revision cutoff/provenance. `ForecastVintage`: provider/run/model/version/reference/availability/received/valid window/raw hash/revision/terms; `WeatherForecast`: variable/unit/target station or declared grid/member set/IDs/weights/series/quality; `WeatherObservation`: observation/publication/receive, preliminary/final/revision/hash/label-only isolation; `WeatherOutcomeBucket`: lower/upper inclusivity and explicit Other-complement only. `∀x in published resolution domain: exactly one bucket` unless rules explicitly permit exceptions. REAL unknown payout-affecting detail => CONTRACT_AMBIGUOUS, not default.

**Causal invariants:** `rules_known_at <= frame`; `forecast_reference <= provider_availability <= received_at <= frame`; `capture_seq <= frame.CutSeq` with ACK durable; valid window complete; station/grid mapping explicit; variable/unit exact or authorised rational transform (`°F=°C×9/5+32`), no invented rounding, provider version/raw hash. No last-known-before-run substitutes on REPLAY, no source init interpreted as public availability; later resolution observations are ONLY label post-frame. Missing member rejects, never renormalize hidden missing mass. Uniform weights model-assumed (`model_version="wx-uniform-v1"` frozen en el payload), finite/nonnegative, sum positive; `P(B)=Σw(member∈B)/Σw`, sum 1, exactly one bucket/member, `UNCALIBRATED`, uncertainty measured member_count/dispersion, unknown calibration error/station bias; deterministic forecast diagnostic only (`fair_value absent`, no candidate). Decimal exact/integer boundary. `fair_yes=p`, `fair_no=1-p`; Economics executable ask/depth and fee bounds; gross-midpoint NOT executable edge; fees unknown INCONCLUSIVE; insufficient depth REJECT; net<=0 reject; Risk real enforcement to be demonstrated, no orders.

**Weather reasons:** `WX_CONTRACT_AMBIGUOUS, WX_SOURCE_UNAVAILABLE, WX_RULE_VERSION_MISMATCH, WX_STATION_MISMATCH, WX_VARIABLE_MISMATCH, WX_UNIT_MISMATCH, WX_LOCAL_DATE_MISMATCH, WX_VALID_WINDOW_MISMATCH, WX_BUCKET_OVERLAP, WX_BUCKET_GAP, WX_BUCKET_UNMAPPABLE, WX_FORECAST_AFTER_FRAME, WX_AVAILABILITY_UNKNOWN, WX_MEMBER_SET_INCOMPLETE, WX_WEIGHTS_INVALID, WX_PROBABILITY_INVALID, WX_PROBABILITY_MASS_INVALID, WX_DETERMINISTIC_UNCALIBRATED, WX_SPATIAL_MAPPING_UNCALIBRATED, WX_FEE_UNRESOLVED, WX_DEPTH_INSUFFICIENT, WX_COSTS_ERASE_EDGE, WX_RESOLUTION_LEAKAGE`. Reusar reason vocabulary engine cuando coincide. F03/F15/F20 diagnostics requieren SFG-05 output sin Opportunity; no crear falsas opportunities para emitir métricas.

### Fixtures F01–F20 — inputs y expected explícitos; 0 ejecutadas hoy

Todas heredan WX-BASE-V1 salvo delta; escribir archivos exclusivos Weather sólo al iniciar B1 tras `PE030_START_ALLOWED`, tests offline sin Internet. Synthetic namespace/hash obligatorio. Los escenarios mecánicos de admisión (vintage futuro, hash alterado, duplicado idéntico, contradicción, reinicio, replay del canal, ausencia de fuente) están probados en la suite shared (receipts SFG-04) y NO se duplican como fixtures Weather: los fixtures Weather re-prueban esas rutas sólo a nivel semántico propio (razón WX emitida, no-model/no-Economics, diagnóstico frame-level).

| ID | Delta/input explícito | Expected + gate |
|---|---|---|
| F01 | base five binary Market/Condition/token mappings y 5 buckets exhaustivos | VALID; Economics no llamado; PASS |
| F02 | members `[18,19,19,20,20,20,21,21,22,23]` peso 1, books base BUY B2 size10 | `P=[.10,.20,.30,.20,.20]`; B2 net +.5088 (+.05088/share) bajo fee fixture/quote válida; B4 REJECT; sólo SHADOW virtual |
| F03 | provider availability `2026-09-19T12:05Z` > frame `12:00Z` | `WX_FORECAST_AFTER_FRAME`, no probabilities/candidate/Economics, reason frame-level SFG-05, REJECT |
| F04 | station `SYN-EGLL` vs `SYN-EGLC` | `WX_STATION_MISMATCH`, no model, REJECT |
| F05 | variable `DAILY_MIN_TEMPERATURE` vs max | `WX_VARIABLE_MISMATCH`, no model, REJECT |
| F06 | target local date `2026-09-21` | `WX_LOCAL_DATE_MISMATCH`, no model, REJECT |
| F07 | `Europe/London` local `2026-10-25`, `[2026-10-24T23:00Z,2026-10-26T00:00Z)` 25h; hourly 15 except included 23:00Z value21 | max 21, 25 samples, PASS; no 24h assumption |
| F08 | published bucket `68°F`, member `20°C`, exact conversion allowed | `68°F`, exactly one bucket, PASS |
| F09 | value exactly `18°C` B0 inclusive <=18 | B0 exactly once, PASS |
| F10 | integer buckets 18/19/20/21/explicit `Other`; member22 | Other=complement, exactly once, PASS |
| F11 | bucket intervals `[18,20]` and `[20,22]`; input20 | `WX_BUCKET_OVERLAP`, reject contract before Economics |
| F12 | buckets <=19 and >=21 no Other; integer20 | `WX_BUCKET_GAP`, reject contract |
| F13 | third member weight `-0.1` (also test nonfinite) | `WX_WEIGHTS_INVALID`, no normalization/probabilities |
| F14 | injected p `[.4,.4,.4,0,0]` sum1.2 | `WX_PROBABILITY_MASS_INVALID`, reject output |
| F15 | deterministic point20 no ensemble/error model | `WX_DETERMINISTIC_UNCALIBRATED`, INCONCLUSIVE, absent FV/ActionCandidate, frame-level diagnostic |
| F16 | frame 12:00Z, rules v2 known_at11:50Z, payload rules v1 | `WX_RULE_VERSION_MISMATCH`, reject stale version |
| F17 | valid B2 but fee kind UNRESOLVED | probability diagnostic permitted, quote `FeeResolved=false`, `WX_FEE_UNRESOLVED`, INCONCLUSIVE, no Risk action |
| F18 | BUY B2 size10 but ask depth only 0.24×5 | filled5, remaining5, `WX_DEPTH_INSUFFICIENT`, no candidate |
| F19 | B2 p=.30, ask .29×10, synthetic fee effective355bps | gross +.10, fee .10295, net -.00295; `WX_COSTS_ERASE_EDGE`, REJECT |
| F20 | resolution observation published 2026-09-21T00:05Z injected as frame feature at 2026-09-20T12:00Z | `WX_RESOLUTION_LEAKAGE`, no model/candidate, later label allowed ONLY post-resolution |
| F21 | B2 en ventana del cut pero `depth_source_ms` fuera de freshness (Stale según `pocdata.L2View`) | `WX_BOOK_STALE`, abstain: no quote, no candidate, estado declarado en assessment; PASS si 0 orders |
| F22 | cut sin book base para el token (NoBase) | `WX_BOOK_NO_BASE`, abstain inmediato sin fallback BBO, diagnóstico frame-level durable (SFG-05); PASS si 0 orders |

**Properties (WEATHER_OWNED):** member order independence, exact probability mass, no overlap/gap, deterministic serialization+hashes, different schedules same Strategy/Frame digest, no label leakage, missing member reject, stale/NoBase abstain sin fallback. Las propiedades de admisión (no future external admission, duplicate idempotente vs conflicto fail-closed, rule revision as-of, restart identity, replay del canal) pertenecen al contrato compartido ya probado (SFG-04): Weather las consume, no las re-implementa. Safety priority F03/F11/F12/F16/F17/F18/F19/F20/F21/F22; diagnóstico frame-level cuando F03/F15/F20/F22 dejen cero oportunidades vía SFG-05. No synthetic observations described as payout real.

### Experiment manifest, risk and stopping

Pin engine SHA/branch, Weather schema/model/weights, contract rule hash, synthetic vs real tag, forecast raw hash/reference/availability/receive/member-set, external record seq/ref, Frame cut/revision/time, books full snapshot/depth/fee IDs+time, evaluation assessment/metrics/reasons, Risk policy revision and enforcement result, simulator scenario and digest. Repeated identical fixture/manifest/seed → identical substantive output under two schedules; hash must cover diagnostic metrics. Counters for refusal by reason, age, member completeness, bucket mass, stale depth, fee unresolved, rule mismatch, frame ineligible, replay mismatch. STOP if contract payout ambiguous, data after frame, frozen ownership conflict, unresolved fees claimed executable, BBO fabricated as L2, attempt live or active dataset touched.

## Roadmap actualizado — máximo 3 fases y gates por WP

| WP/Phase | Owner | Depends on | Allowed files / interfaces (freeze A0) | Input→output | PASS / FAIL |
|---|---|---|---|---|---|
| A0 / A | Weather coding agent, READ-ONLY | common manager confirms SFG receipts; remote25f baseline | NONE to modify: `git status`, source/owners/branch/data-dir, allowed-files list; NEVER `.rs-v03-sports/` | reconcile local HEAD and shared contracts → exact file manifest | PASS `A0_HEAD_VERIFIED`; FAIL local drift/frozen collision |
| A1 / A | Weather domain | A0; SFG-04 not needed for pure model | new `internal/strategy/pocs/weather/**` + Weather `testdata/**` ONLY if A0 ownership permits; `go.mod` unchanged | synthetic WX-BASE→contracts/probabilities F01–F16 | PASS exact tests and properties; FAIL guesses/float/leak |
| B1 / B | Weather data | A1 + `PRECONDITION_SHARED_SFG-04` | Weather-specific codec/admission in approved weather package only; common Capture/Frames READ-ONLY | fixture raw→shared ExternalObservation→durable Frame → tests F03/16/20 | PASS cut+hash+replay; FAIL hidden channel/network inside Strategy |
| B2 / B | Weather strategy | B1 + SFG-01/02 contract receipts + SFG-05 diagnostic seam | new Weather Factory/Strategy, small registry edits `cmd/engine/screen.go` and `internal/experiment/experiment.go` only under dedicated ownership/permission; no new runner | P(bucket)→Economics→assessment/Risk→SCREEN F17–19 | PASS quote from same cut, no synthetic book fallback; FAIL private fee/unchecked risk |
| C1 / C | Weather QA | B2 + SFG-03/07 safety | Weather tests/fixtures, runner changes only if common owner approved; do not edit frozen core | SCREEN→Strategy REPLAY→SHADOW valid legs→cert receipt | PASS F01–F20, two schedules/digests, regression tests, isolated dataset, true non-live; FAIL any fabricated PnL/fill |

**Gates finales:** `A0_HEAD_VERIFIED`; `A1_OFFLINE_MODEL_PASS`; `B1_EXTERNAL_ADMISSION_PASS`; `B2_SCREEN_PASS`; `C1_NONLIVE_CERTIFIED`. `PE030_IMPLEMENTATION_READY` significa código/tests verificados, no plan redactado; hoy sólo `PE030_PLAN_RECONCILED / SHARED_BLOCKER_CONFIRMED`. Real contract readiness/point-in-time member archive/OOS/live separados y no PASS. No fijar el 95% M4 previo como prueba Weather: cumplir floor actual por paquete tocado tras implementación, sin denominator games.

## 📆 Bitácora

- **2026-09-20 — preparación original:** Deep Research destilado, nota creada, WX-BASE-V1 y F01–F20 descritos, 0 código/tests, HEAD local no inspeccionado. Diagnóstico de SCREEN neutral-only era provisional y queda corregido abajo.
- **2026-09-20 — auditoría/reconciliación RS v0.3:** branch remota `feature/research-strategies-v01@25f578a502ce0c9e1ad27a93537a868a94533b34` verificada; código de Strategy/SCREEN/pocdata/Economics/FeeResolver/Capture/Frames/Replay/Experiment/Sports y tests de SCREEN inspeccionado. SCREEN ya multi-Strategy; external pipeline ausente; L2 top6 full-only; fees de BuildQuote uniformes; SHADOW fee unresolved y fallback size10; outputs sin opp ausentes. SFG-01..07 clasificados, blockers antiguos depurados, critical path/mandato reescritos. **Cero cambios engine, cero lectura/escritura de dataset Sports, cero tests ejecutados, no se modifica padre/PE-001/PE-004, sesión no cerrada.** HEAD local/CI/Graphify y bridge del padre no verificados por alcance/acceso.

## 🔗 Docs / Links — evidencia persistente

- Padre `[[Polymarket Engine — MVP]]` y sus secciones frozen M1.4/Strategy/External data seam; research `[[Polymarket — Edge Research Consolidado 2026-09-16]]`; platform `[[Polymarket — Technical Platform Map — synced 2026-09-17]]`.
- Engine branch SHA: https://github.com/xKoRx/polymarket-engine/commit/25f578a502ce0c9e1ad27a93537a868a94533b34 ; M4 main https://github.com/xKoRx/polymarket-engine/commit/9ae5ddec1a0e52fdc0bbde608cd0504e644d05a5 . Source paths en sección Estado actual, inspeccionados a SHA exacta; evidencias de aislamiento: `cmd/engine/screen_consolidated_test.go`, y `internal/strategy/pocs/{sports,negrisk}`. No afirmar tests ejecutados aquí.
- Weather real reference: https://polymarket.com/event/highest-temperature-in-london-on-september-20-2026 ; NOAA station: https://www.weather.gov/wrh/timeseries?site=eglc ; Open-Meteo Ensemble: https://open-meteo.com/en/docs/ensemble-api ; model availability https://open-meteo.com/en/docs/model-updates ; terms https://open-meteo.com/en/pricing ; Polymarket contracts https://docs.polymarket.com/concepts/markets-events ; Gamma https://docs.polymarket.com/market-data/discover-markets ; book https://docs.polymarket.com/market-data/prices-order-books ; fee https://docs.polymarket.com/trading/fees . Research adjunto contiene evidencia ID `E-*`, sin asumir que enlaces de sesión efímeros son fuente del vault.

---

# MANDATO DE IMPLEMENTACIÓN — PE-030 (RECONCILIADO RS-V03)

Actúa como coding agent de **Weather exclusivamente**. Autoridad: esta nota + `xKoRx/polymarket-engine@feature/research-strategies-v01` HEAD real verificado al iniciar; `main@9ae5dde` sólo baseline M4; **no** usar versiones previas de la nota como autoridad. No volver a investigar meteorología, Polymarket básico, RS v0.1/0.2 ni rediseñar engine. Bootstrap mínimo Agents-OS; verificar que shared manager publicó recibos/commit SHA para `PRECONDITION_SHARED_SFG-04`, contrato SFG-01, SFG-02 y seam SFG-05 antes de tocar integración; si falta, A1 offline puede avanzar, B1/B2 deben quedar BLOCKED sin inventar workaround.

**Orden:** A0 read-only local HEAD/status/concurrencia/frozen ownership/data-dir y allowed-files exactos, comparar contra 25f; A1 Weather contracts/model/F01–F16 en package propio; B1 consumir external seam común ya terminado con fixture-backed adapter, durable capture ACK, Frame causal/replay; B2 registrar Factory en `screenFactories`/`shadowStrategyFor` existentes, no construir otros runners ni Economics, F17–F19 y Risk comprobado; C1 SCREEN, Strategy REPLAY, SHADOW con `ActionCandidate.Legs` y profundidad/fee válidas, F01–F20, properties, go test/vet/race/cobertura/regresión, manifests/hashes y review humano. RunShadow legacy fallback sin legs prohibido para Weather; fees unresolved → INCONCLUSIVE, nunca net PnL; si el common runner aún no resuelve fees, SHADOW sólo evidencia operativa virtual y reportar economía INCONCLUSIVE, no certificar retorno.

**Allowed files:** A0 debe fijar `branch/HEAD + exact paths + writers + owner` en esta nota. Weather únicos nuevos bajo `internal/strategy/pocs/weather/**` y testdata Weather si owner lo ratifica; cambios registry puntuales `cmd/engine/screen.go`, `internal/experiment/experiment.go` sólo si ownership otorgado; `internal/strategy/api.go`, `internal/frames/**`, `internal/capture/**`, `internal/protocol/**`, `internal/economics/**`, `internal/regimes/**`, `internal/replay/**`, `internal/simulator/**` READ-ONLY Weather por defecto; las mejoras SFG pertenecen a un único owner compartido. NO editar padre, PE-001, PE-004, Sports Reversion, NegRisk, global research, Platform Map, `.rs-v03-sports/`, sync.sh, `.sync`, go.mod sin justificación. No push engine salvo mandato separado. No checkout/reset/rebase/clean de trabajo de otros. No código live/órdenes/network dentro Strategy/secretos.

**No bloqueo de data real en A1:** synthetic market completo y dataset t.TempDir propio; source real IDs/rules/fees/terms no precondición offline. Si se descubre cambio incompatible en HEAD, dejar delta, reason y owners exactos en bitácora y continuar A1 independiente sin intervenir frozen. Si aparecen tests PASS sólo de modelo, reportar `A1_OFFLINE_MODEL_PASS` y no declarar SCREEN/REPLAY/SHADOW. `0%` hasta evidencia física, después progreso por WPs realmente terminados. No hacer cierre ritual de Agents-OS; al terminar entregar evidence y tarea Weather a Review, no marcar puente humano Done.

**Evidencia obligatoria:** manifest con engine_SHA, shared gate SHA/receipts, contract/model/rules/forecast hashes, external capture refs+known-at+cut, L2 source revision/epoch, fee schedule+revision, Risk policy check, fixture ID, assessments/reasons/metrics y scorecard hash. Tests deben demostrar look-ahead rechazado, bucket overlap/gap, members incompletos, fee/depth unknown, costs erase edge, zero-opportunity diagnostics, multi-instance isolation, two replay schedules parity, 0 venue orders y 0 modificaciones data-dir activo. Si gate compartido no está listo, reportar `BLOCKED_BY_SHARED_SFG-xx` con A1 entregado; NO pasarle la pelota al owner por decisiones Weather menores ni inventar estado ready.

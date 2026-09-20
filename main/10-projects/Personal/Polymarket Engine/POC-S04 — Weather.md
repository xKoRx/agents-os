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
> **Estado: `PE030_PLAN_RECONCILED / SHARED_BLOCKER_CONFIRMED`** · Implementación `0%` · Research estadístico `NOT_VALIDATED` · Contratos reales `REAL_DATA_BLOCKED` · Alpha `UNPROVEN` · LIVE `FORBIDDEN`. Esta nota contiene SPEC, matriz transversal, decisiones, fixtures y mandato. Los WPs Weather NO implementan cambios compartidos que otro owner deba cerrar primero.

## 🎯 Objetivo

POC offline, causal, determinista y falsable: un contrato meteorológico explícito + forecast ensemble íntegro conocido antes del frame → P(bucket) no calibrada → fair value diagnóstico → Economics del engine sobre precios/depth/fees as-of → assessment y eventual candidato sujeto a Risk → SCREEN / Strategy REPLAY / SHADOW virtual cuando sus datos son válidos. Nada de órdenes live, PnL fabricado ni conclusiones OOS desde fixtures. Engine durable reutilizable; Weather sólo implementa su diferencia meteorológica.

## 📊 Estado actual — reconciliación del 20-09-2026

**Autoridad separada:** `main@9ae5ddec1a0e52fdc0bbde608cd0504e644d05a5` = M4 certificado base; `feature/research-strategies-v01@25f578a502ce0c9e1ad27a93537a868a94533b34` = HEAD REMOTO de Research Strategies verificado mediante GitHub branch y source. El commit feature es checkpoint RS-V03 Fase C de Sports: snapshot intermedio de captura que seguía activa al hacer commit; **no certifica el resultado de la captura ni PE-030**. HEAD/worktree locales y cambios posteriores no visibles: `LOCAL_VERIFICATION_PENDING`, comparar nuevamente antes de comenzar. Baseline `7bd264d` histórico, NO autoridad. Investigación Weather recibida `2026-09-20T03:24Z` sigue siendo autoridad de dominio donde no contradiga source; su diagnóstico antiguo de remoto sólo README y SCREEN neutral-only queda explícitamente SUPERSEDIDO.

**Shared foundations integradas (2026-09-20):** [[Polymarket Engine — POC Shared Unblocker]] entregó INTEGRATION_SHA `9d0512a912fcce4b9aefc152c7a89b090ff8df1d` (branch `feature/shared-poc-unblocker`, rebase sobre `feature/research-strategies-v01@f070496`, sin push, pendiente Review del owner). Estado esta POC: `READY_WITH_RESTRICTIONS` — SFG-01/02/03/04/07 re-validados PASS sobre ese SHA (05 opcional para abstención); el canal `internal/external` + `protocol.SurfaceExternal` + `strategy.Frame.Externals` EXISTE y está probado sobre ese SHA, lo que SUPERSEDE puntualmente el hallazgo «ruta externa no existe» (verificado contra el árbol integrado, no contra `25f578a`); la semántica meteorológica (station/buckets/ensemble/forecast normalization) sigue siendo ownership exclusivo de PE-030. Baseline de arranque = `9d0512a`; primer WP: adapter Weather → `external_observation_v1` vía `external.AdmitSync` (WP B1); prohibido reimplementar admission/external, L2, replay/shadow o dataset guard; handoff completo en la nota shared.

**Regla frozen padre** `[[Polymarket Engine — MVP]]`: Strategy sólo aporta su edge; discovery, books, Capture, Replay, Economics, Risk, Simulator, SHADOW, account y observabilidad son del engine. El diseño padre declara `ExternalObservation{source,source_key,event_time,receive_time,payload_version,quality}` y un External data seam implementable sólo cuando lo requiera una POC. **Ese diseño no constituye código:** la branch inspeccionada no materializa una ruta externa E2E; Weather es el primer consumidor y SFG-04 debe asignarse a owner común. No crear framework universal ni esconder payload en Extras, Quality o Parameters.

**Source inspeccionado en branch exacta:** `cmd/engine/screen.go::{screenFactories,openScreenPipeline,loadJournal,routeNext,toStrategyFrame,applyOwnerRecord,depthExtras,runScreenConsolidated}`; `cmd/engine/screen_consolidated_test.go::TestConsolidatedTwoInstancesIsolatedAndDistinguishable,TestConsolidatedRunsBothPOCsEndToEnd`; `internal/strategy/api.go::{Strategy,Factory,Frame,DataRequirements,EvaluationContext,Assessment,ActionCandidate}`; `internal/strategy/pocs/pocdata/pocdata.go::{TopLevels,DepthFresh,DecodeSide}`; `internal/frames/frames.go::{AssetSnapshot,DeliveryFrame,RevisionRef}`; `internal/economics/economics.go::{WalkSide,ExecutableDepth,BuildQuote}`; `internal/regimes/feeresolver.go::{FeeEvidence,ResolveFee,FeeResolution}`; `internal/experiment/experiment.go::{RunManifest,Scorecard,RunShadow,shadowStrategyFor,fillCandidate,scorecardHash}`; `internal/replay/{replay.go,manifest.go}`; `internal/protocol/{protocol.go,marketws.go}`; `internal/capture/{capture.go,envelope.go}`; `internal/strategy/pocs/sports/sports.go`; además documentación frozen del padre. **Inspección estática, no go test/CI, no local checkout, no captura tocada.** Evidencia exacta en Docs/Links.

**Hallazgos verificables y correcciones de plan:**
- SCREEN registra Neutral, NegRisk y Sports; `screen-consolidated` reutiliza un `screenPipeline` y ejecuta instancias aisladas. Los records marketws se enrutan incrementalmente entre cuts; tests de aislamiento y ambas POCs existen. Registración Weather es extensión pequeña, NO nuevo SCREEN.
- `strategy.Frame` mantiene `{Ordinal,CutSeq,Assets,Quality,RevisionVector,VirtualTime}` y `frames.DeliveryFrame` no contiene external observations. `DataRequirements` no expresa external data. `protocol.Surface` sólo admite gamma/clobrest/marketws/datav2; `capture.Envelope.validate()` rechaza data surface desconocida. `screenPipeline.loadJournal()` filtra `surface=marketws`. **External source→Capture→Frame→Strategy→Replay NO EXISTE como ruta aprobada verificable.**
- `pocdata.TopLevels=6`: levels de último full book codificados en `AssetSnapshot.Extras`, `depth_source_ms`; `DepthFresh` compara con `LastSourceMs`. Deltas no actualizan esa profundidad: tras delta se rechaza, no se interpola. `applyOwnerRecord` / `screenApply` consumen Book, no construyen L2 delta-aware; revision de snapshot se establece `Revision:1` en esa proyección. El book engine durable tiene reducer propio, pero no equivale automáticamente a su exposición a Strategy en mismo cut. Reusar `pocdata` sólo como codec PROVISIONAL para una cantidad totalmente cubierta por niveles observados y frescos; jamás llamarlo L2 general.
- `economics.BuildQuote` hace sweep correcto de niveles que recibe y maneja POINT/INTERVAL/UNRESOLVED; fee POINT/INTERVAL = coeficiente BPS × notional total. `regimes.ResolveFee` no inventa base_fee↔feeRate ni aplica trade-observed fee fuera de su capture_seq. **No demuestra fórmula de fee Weather price-dependent/multinivel**, rounding ni revisions per-token acopladas al mismo cut. No calcular fees en Weather; cotización real no concluyente hasta SFG-02.
- `experiment.RunShadow` selecciona Strategy vía `manifest.StrategyID`, `fillCandidate` usa leg(s), `pocdata.DepthFresh`, Simulator y coordinator virtual; PERO pasa `FeeUnresolved` al simulator, el scorecard etiqueta `VirtualPnLNet` como gross notional/inconclusive, y para ACCEPT sin candidate legs mantiene fallback BBO + profundidad sintética size=10. **Weather exige leg válido y nunca usa fallback; SHADOW es diagnóstico virtual, NO rentabilidad neta**. `Scorecard.StrategyMetrics` conserva sólo últimas métricas de assessments, y `scorecardHash` no incluye todas las métricas; cuando Detect retorna cero oportunidades no hay Assessment/Metrics de abstención.
- `replay.RunObservation` reproduce reducers/books/regimes por manifest y schedules; `replay.Manifest` verifica segment pins y `DeliveryFrame` se puede resolver, pero esa API sola NO vuelve a ejecutar una Strategy Weather. `RunShadow` sí la ejecuta sobre records/cuts y Simulator: separar los tres niveles en SFG-03.
- `protocol.marketws` reconoce `new_market`, conserva raw y `Documented=false`: NO es trabajo ni dependencia inicial Weather. `capture.Open` hace recovery/boot y `screen`/`shadow` lo invocan: no abrir `.rs-v03-sports/`, ni copiar SQLite+WAL activos en caliente ni commitear snapshots mid-capture.

## 🧱 Entrega de desarrollo

| Repo | Branch | Base verificable | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| `xKoRx/polymarket-engine` | `feature/research-strategies-v01` remoto; branch/worktree local a confirmar read-only | remoto `25f578a502ce0c9e1ad27a93537a868a94533b34` (main M4 `9ae5dde`) | [SPEC funcional](#spec-funcional-v1) | [SPEC técnica](#spec-técnica-v1) | PLAN_RECONCILED; PRECONDITION_SHARED_SFG-04 y contratos SFG-01/02/05 pendientes |
| `xKoRx/agents-os` | `master` remoto; local no inspeccionado | este planner actualizado por commit independiente | esta nota | matriz + mandato aquí | nota única, no se modifica padre ni proyectos vecinos |

## 🧩 Subproyectos

Ninguno. PE-001 Sports Combinatorial NO es `poc-sports`: éste es PE-005-R1 Sports Reversion según `sports.StrategyID/HypothesisID`. Compartir infraestructura, no mezclar hipótesis.

## ✅ Tareas — planner único

> [!note]+ Estados y ownership
> Todos `[ ]` hasta evidencia real del coding agent. No pasar progress de 0 por research; registrar SHA, tests, paths y recibos en bitácora. La tarea puente humana del padre es una dependencia de consistencia no editable por el mandato de aislamiento; comprobarla read-only y dejar `PARENT_BRIDGE_PENDING` si falta; no inventar su existencia. Nunca cerrar sesión completa salvo pedido explícito.

- [ ] **A0 | Autoridad y preflight:** comprobar HEAD local/branch, worktree concurrente, ownership, frozen policies, shared SFG closure receipts, data-dir seguro; fijar allowed-files reales por WP. NO redescubrir RS v0.1/0.2. #owner/agent #type/research #area/personal
- [ ] **A1 | Weather puro:** contratos, intervalos, validaciones, vintages, ensemble empírico, razones y F01–F16. Sin dependencia del provider ni core frozen. #owner/agent #type/dev #area/personal
- [ ] **B1 | Admission Weather fixture:** adapter/codec Weather exclusivamente, evidence envelope compartido ya certificado por SFG-04, causal cut y F03/F16/F20; no recorder propio. #owner/agent #type/dev #area/personal
- [ ] **B2 | Strategy + SCREEN:** Factory, registry existente, DataRequirements real, detect/evaluate, quote vía Economics común según SFG-01/02, Risk, F17–F19, SCREEN aislado. #owner/agent #type/dev #area/personal
- [ ] **C1 | Strategy REPLAY/SHADOW/QA:** misma evidence/versioned manifest, dos schedules, F01–F20 y properties, SHADOW sólo Candidate.Legs + Simulator con inputs válidos, sin fallback, no PnL económico inventado; go test/vet/race/regresión/cobertura y owner review. #owner/agent #type/dev #area/personal

## Matriz de shared foundation gates — SFG (estado sobre REMOTO 25f578a, no certificación local)

| Gate | Estado | Evidencia / riesgo | Decisión / owner y condición PASS |
|---|---|---|---|
| **SFG-01 — CAUSAL_L2** | `PARTIAL_SHARED_CAPABILITY` | `pocdata.TopLevels=6`, full-book-only `depth_source_ms`; delta vuelve stale; proyección `applyOwnerRecord` fija revision 1 y no expone toda revisión/epoch/known-at de Books a Strategy. | Owner Books/Frames + Research Strategies: congelar contract as-of-cut: asset, cut_seq, revision/epoch, source/received time, quality, side+levels con truncation/coverage, delta y gap handling. Ruta KISS aceptable para Weather offline: full fresco de seis niveles si cubre 100% size; tras delta abstain; no latest. Para PE-004 L2 evolutivo puede requerir seam completo distinto; misma API/ownership, no dos codecs paralelos. Prueba full→delta→cut (stale), refresh→cut (fresh), epoch→fence, size>depth rechazado, replay mismos hashes. |
| **SFG-02 — FEE_CONTRACT** | `PARTIAL_SHARED_CAPABILITY` | `regimes.ResolveFee` conserva incertidumbre; `economics.BuildQuote` aplica BPS uniforme × notional total, sin demostrar fee Weather por fill/level dependiente de precio, redondeo, market/version cut. Sports fija fees por params; SHADOW usa UNRESOLVED. | Owner Regimes/Economics/Simulator: fijar única semántica venue per-token/per-cut, fee kind+evidence/revision/formula/rounding, coste sumado por fill level cuando el schedule lo exige y bounds honestos. No resolver con fee Weather privada. Para offline fee fixture de un solo nivel puede adaptarse a BPS efectivo documentado, **no** certificar sweep multinivel ni fee real con ello. Tests fee price-dependent dos niveles ≠ fee plana, unresolved/suspect veto, revision futura no entra, rounding de fee exacto y simulator parity. |
| **SFG-03 — RESEARCH_RUNTIME** | `PARTIAL_SHARED_CAPABILITY` | SCREEN/SCREEN-consolidated/factories y SHADOW selector+Simulator existen. `replay.RunObservation` = market state, no Strategy execution; delivery replay conserva frames, SHADOW re-ejecuta Strategy pero fallback sin legs inventa size 10 y fees no resueltas. | Owner Runtime/Experiment: reutilizar registry y `RunShadow`, registrar Weather; especificar Strategy replay reproducible desde manifest+frames+externals, exigir Candidate.Legs y prohibir fallback Weather. SCREEN → Strategy replay → SHADOW pruebas con assessment/digest equivalentes, 0 venue orders. No crear runtime nuevo. |
| **SFG-04 — EXTERNAL_OBSERVATIONS** | `MISSING_CONFIRMED` | `protocol.Surface` enum cerrado, Capture data valida known surface, `DeliveryFrame`/`strategy.Frame`/DataRequirements sin external; screen/experiment sólo routean marketws. Diseño del padre NO implementado. | **Owner común Engine/Frames/Capture/Strategy/Replay, consumidor inicial PE-030. PRECONDITION antes de B1/B2.** Mínimo seam descrito abajo; pruebas de durability, cut, replay, leak y backwards compatibility. Weather no puede improvisarlo. |
| **SFG-05 — DESCRIPTIVE_OUTPUT** | `PARTIAL_SHARED_CAPABILITY` | Assessment.Metrics+Reasons sirven cuando existe Opportunity; SCREEN imprime por evaluation; `Scorecard.StrategyMetrics` último assessment solamente y hash excluye métricas; cero opportunities pierde reasons/calibration. PE-004 lo necesita especialmente, Weather para abstention. | Owner Strategy Runtime/Experiment: único frame-level result opcional versionado `{strategy,instance,frame,metrics,reasons,calibration}` (o mecanismo existente si branch posterior lo demuestra), durable y reproducible incluso 0 candidates; scorecard digest incluye outputs, no last-wins. Preservar API anterior o migrar con versioning. Tests zero-opp abstention visible; dos estrategias no mezcladas; cambio reason cambia hash; no acción ni PnL. |
| **SFG-06 — MARKET_LIFECYCLE** | `NOT_REQUIRED_BY_PE030_V1` | `new_market` raw/documented=false, PE-004 owner; Weather v1 usa mercados ya descubiertos y synthetic IDs para fixture. | NO dependencia previa Weather; no tocar Protocol lifecycle desde PE-030. |
| **SFG-07 — ISOLATED_DATASET** | `PARTIAL_SHARED_CAPABILITY` | `capture.Open` abre boot/recovery; screen y RunShadow lo usan y experiment persiste SQLite. Dataset de captura Sports sigue escribiéndose al snapshot 25f. | Owner QA/infra: crear siempre dataset **nuevo en t.TempDir desde fixtures sintéticas** para Weather E2E; paths no coincidentes con `.rs-v03-sports/` ni data-dir activo, verifica prefix/realpath, no symlink, sin acceso de escritura al original. Si se usa material histórico, esperar captura detenida y obtener snapshot coherente usando mecanismo oficial de backup/snapshot con manifest y hash; nunca `cp` arbitrario de DB+WAL activos. Abrir sólo copia; manifest/verify, correr SCREEN/REPLAY/SHADOW y comparar hash del origen inmutable. No pruebas destructivas durante planificación. |

### Capabilities reutilizables — NegRisk / Sports Reversion / base M4

| CAPABILITY | SOURCE SYMBOL + PROVEN BY | WEATHER REUSE AS-IS? | CHANGE REQUIRED? |
|---|---|---|---|
| Strategy/Factory/actor isolated | `strategy.Strategy/Factory/NewInstance`, `screenFactories`, `TestConsolidatedTwoInstancesIsolatedAndDistinguishable` | SÍ runtime | sólo registrar Weather y seam external compartido |
| SCREEN multi-instance + forward cuts | `openScreenPipeline/routeNext/runScreenConsolidated`, tests `TestConsolidatedRunsBothPOCsEndToEnd` | SÍ pipeline | registro Weather; no reconstruir |
| Causal book durable | `books.Engine`, `capture.OpenView`, replay M4 y owner docs | SÍ reducer | proyección L2 as-of SFG-01 para consumidor |
| Depth observed codec | `pocdata.EncodeLevels/DepthFresh/DecodeSide` Sports/NegRisk | CONDICIONAL sólo full fresco top6 | SFG-01 si requiere delta-depth/más niveles |
| Economics + fee uncertainty | `economics.WalkSide/BuildQuote`, `regimes.ResolveFee` | SÍ funciones puras en scope válido | SFG-02 price-dependent fee/multilevel/as-of; sin fee privada |
| Simulator / virtual Account / basket | `simulator.FillAt`, `experiment.fillCandidate`, `account.NewCoordinator/PlanBasket` | SÍ infraestructura virtual | candidato leg completo; nunca fallback BBO synthetic 10 |
| Risk | `risk.Policy/Snapshot` presentes en `experiment.RunShadow` | parcial: tipos disponibles, no asumir gate efectivo | código observado crea `riskPolicy/riskSnapshot` y usa `_ =` para ambos: test de enforcement real es requisito antes de afirmar Risk certificado Weather |
| Replay | `replay.NewReplayer/RunObservation/BuildManifest`, `experiment.RunShadow` | SÍ market-state y shadow runner | SFG-03 Strategy replay reproducible + SFG-04 external refs |
| Experiment manifest/scorecards | `experiment.RunManifest/Scorecard/scorecardHash` | SÍ estructura de experiment | SFG-05 para zero-opp/metrics/hash; versioned Weather evidence refs |
| Reasons/metrics | `strategy.Assessment{ReasonCodes,Metrics}` y tests Sports | SÍ si existe opp | SFG-05 sin opportunity; WX codes sólo en Weather |
| Fixtures/test loaders | `cmd/engine/screen_consolidated_test.go::newScreenJournalFixture`, Go t.TempDir, M4 fixture corpus | SÍ patrón, NO copiar data viva | Weather F01–F20 propios, SFG-07 safe isolation |
| Market lifecycle | `protocol.MarketWSEnvelope.Documented=false` para new_market | NO NECESARIO | PE-004 exclusivamente |
| External observations | contrato conceptual padre vs Surface/Frame source | NO | SFG-04 dueño engine antes de integrar Weather |

### SFG-04 — especificación mínima obligatoria para owner compartido (NO implementar desde Weather)

**Scope generalizable por necesidad real, un consumidor:** `ExternalObservation` immutable envelope version `external.v1` con `{source,source_key,event_time,provider_available_at?,received_at,known_at,payload_version,quality,artifact_hash,artifact_ref,provider_version}`; raw Weather payload con forecast reference, valid window, member IDs/weights, station/grid+units/rules hash va en **codec Weather**, no en engine. `source_key` estable y payload hash identifican identidad/revisión; same key+same hash idempotente, conflicting hash crea nueva revisión/version o conflict explícito, jamás overwrite. No admitir source time retroactivo como known-at. `provider_available_at <= received_at <= frame.VirtualTime`, `external capture_seq <= frame.CutSeq`, rules version known_before cut. Ausencias materiales => ineligible/abstain, no latest fallback.

**Capa común requerida:** adapter externo obtiene bytes con I/O fuera de callbacks y los entrega a un ingreso autorizado; incorporar superficie/DTO y redaction-policy explícitos a `internal/protocol/**` + `internal/capture/**` preservando SurfaceUnknown fail-closed y compatibilidad de journals previos; Capture mismo journal/lane EVIDENCE con ACK durable antes de frame; owner/reducer externo por key conserva revisión y calidad; `frames.DeliveryFrame` expone refs/payload versionado snapshot as-of barrier, `strategy.Frame` recibe proyección inmutable y `DataRequirements` permite exigir fuente/freshness sin quebrar estrategias antiguas; `cmd/engine/screen.go` y `internal/experiment/**` enrutan records externos por cut (no filtrar sólo marketws), `internal/replay/**`/manifest incluyen hashes y prueban equivalencia. Payload permitido inline sólo si límites de frame/capture lo admiten y se versiona; si ref-only, materializarlo ANTES de callbacks, sin filesystem/DB I/O durante Strategy. No reusar `Quality`, `AssetSnapshot.Extras`, Parameters ni protocolo MarketWS ficticio como transporte. No multiplicar adapters ni inventar generic REST SDK.

**Compatibility:** zero external requirements reproduce EXACTAMENTE Neutral/NegRisk/Sports; journals antiguos replay sin cambio de digest; unknown source/schema falla cerrado; nuevas pruebas golden `external-before-cut`, `external-after-cut`, duplicate, conflict, revision, missing payload/hash, corrupt raw, frame retention budget, mode parity, two instances, 0 network inside Strategy. Congelar owner y allowed files una sola vez para evitar que PE-001/PE-004/Weather editen api.go/frames.go/capture a la vez. **Gate PASS** sólo con código + tests en branch compartida publicada y SHA/recibo, o si branch más nueva demuestra contrato equivalente físicamente; no aceptar documento como implementación.

## MUST RESOLVE BEFORE CODING AGENTS START — sólo transversal

| Orden | Gate / problema concreto | POCs | Owner único / mínimo fix | Files bajo ownership común | Prueba de cierre | Complejidad / colisión |
|---|---|---|---|---|---|---|
| 1 | `PRECONDITION_SHARED_SFG-04` — no existe ingreso external→durable→Frame→Strategy→replay, Weather no puede integrar sin romper frozen | PE-030 directamente; PE-001/PE-004 sólo si luego usan external | manager del engine asigna 1 owner de core; entregar seam mínimo v1 arriba, no Weather agents | `internal/protocol/**`, `internal/capture/**`, `internal/frames/**`, `internal/strategy/api.go`, `cmd/engine/screen.go`, `internal/experiment/**`, `internal/replay/**` sólo con freeze exacto | E2E fixture external antes/después del cut + replay parity + tests antiguos | MEDIA/ALTA, **colisión HIGH si Weather improvisa**. A1 puro puede ejecutarse independiente; B1/B2 no empezar hasta PASS. |
| 2 | `PRECONDITION_SHARED_SFG-01` — contrato L2 truncado/full-only y sin provenance completa | PE-001, PE-004, PE-030 | owner Books/Frames fija shared policy: para offline usar top6 full-fresh y cubrir size, abstain tras delta; sólo extender delta-aware si los requisitos PE-001/004 lo exigen | `internal/books/**`, `internal/frames/**`, `cmd/engine/screen.go`, `internal/strategy/pocs/pocdata/**` | full→delta stale, re-full, epoch fence, size>observed depth, deterministic cut | MEDIA; **colisión MED/ALTA** si cada POC modifica el codec. Gate cerrado por contrato explícito y tests antes de integración en paralelo; no exige full L2 para A1. |
| 3 | `PRECONDITION_SHARED_SFG-02` — precio-dependencia, fee schedule y multi-level no expresados por fee plana; ownership disperso en params | PE-001, PE-004 (economics), PE-030 | owner Regimes/Economics decide única API fee schedule+revision+rounding/known-at; preservar unresolved; para offline sintético single level conversión documentada sólo como fixture | `internal/regimes/**`, `internal/economics/**`, `internal/simulator/**`, `internal/experiment/**` | 2 niveles distintos vs fee plana, unresolved veto, previous fee not overwritten, simulator parity | MEDIA; **colisión ALTA** si Strategies implementan tarifas privadas. Antes de paralelismo aprobar ruta compartida o recortar explícitamente offline sólo a caso quoteable y fee conocida. |
| 4 | `PRECONDITION_SHARED_SFG-05` — abstention sin Opportunity no deja reason/metrics; scorecard last-wins y digest incompleto | PE-004 principalmente; PE-030 para F03/F15/F20, PE-001 si requiere diagnóstico | owner Experiment/Strategy define frame-level diagnostics durable/hashed mínimo, sin inventar ActionCandidate; no duplicar scorecard por POC | `internal/strategy/api.go`, `internal/strategy/runtime.go`, `cmd/engine/screen.go`, `internal/experiment/**` | 0 opp genera reason/quality, dos instancias aisladas, cambio metric cambia digest y no PnL | MEDIA; **colisión MEDIA/ALTA** si POC crea output propio. A1 puede devolver reasons internamente mientras gate compartido pendiente. |

**No bloqueadores antes de iniciar dominio Weather:** SFG-03 runtime ya existente → sólo preflight de integración/permisos antes B2; SFG-06 `NOT_REQUIRED`; SFG-07 procedimiento t.TempDir sin cambio productivo. Necesaria una autoridad de manager sobre congelamiento de paths; no lanzar tres agentes a editar módulos compartidos simultáneamente. El owner no tiene que decidir implementación meteorológica menor.

## CAN BE RESOLVED INSIDE WEATHER — sin colisión

Contrato de market meteorológico, estación exacta, variable/unidad/timezone/ventana/DST, bucket algebra/Other, forecasts/vintages, ensemble weights/probabilidad no calibrada, quality flags Wx, interpretación de modelo→resolution domain, fixtures F01–F20 y codec Weather-specific bajo `internal/strategy/pocs/weather/**` (nombre final a validar en A0). Adapter **fixture-backed Weather** se acopla al seam SFG-04 ya entregado, no redefine capture. Gamma IDs reales, rounding/timezone contractual Londres, provider histórico/terms/bias quedan como real-data/validation-only; no impedir núcleo offline. Sin observaciones sintéticas presentadas como reales.

## Blocker ledger depurado

| Legacy ID | Clasificación nueva | Estado/acción |
|---|---|---|
| B-ENG-01 | `STILL_BLOCKING_IMPLEMENTATION` únicamente preflight local/ownership; no investigación RS | branch remota source inspeccionada, HEAD local/worktree no. A0 fija SHA antes escritura; preflight es común a todos y no implica cambiar engine. |
| B-ENG-02 | `RESOLVED_BY_RS` para supuesto neutral-only; `MERGED_INTO_SFG-04` para external; `MERGED_INTO_SFG-01` para L2 | eliminar afirmación 9ae5dde como baseline único; no duplicar blockers. |
| B-RULE-01 | `REAL_DATA_ONLY` | IDs Gamma/Condition/assets, regla exacta timezone/rounding/fallback/revision. Londres REFERENCE_ONLY. |
| B-EXEC-01 | `MERGED_INTO_SFG-01` + `MERGED_INTO_SFG-02`; metadata real `REAL_DATA_ONLY` | L2/fees common preconditions; market-specific fee/tick/min-size/book aún real-only. |
| B-DATA-01 | `VALIDATION_ONLY` (historia de miembros) + prospective data `REAL_DATA_ONLY` | no backfill pseudo-point-in-time; capturar vintages nuevos cuando autorizado. |
| B-LIC-01 | `REAL_DATA_ONLY` | licencia comercial/terms, station-grid correction; no gasto ni permisos requeridos para fixtures offline. |
| B-OPS-01 | `MERGED_INTO_SFG-07` | generación dataset sintético nuevo en t.TempDir; no tocar `.rs-v03-sports/`. |

## SPEC funcional v1 — Weather exclusivo, frozen para núcleo offline

**Tesis:** ensemble disponible y reproducible antes de cada cut puede diferir de precios ejecutables, sin asumir superioridad. Universo inicial sintético `SYN-WX-20260920-HIGH-UTC`, nunca market real. Candidatos reales documentados: Londres high/low, Helsinki high, Shanghai high Sep 20 2026. Londres-high reference `https://polymarket.com/event/highest-temperature-in-london-on-september-20-2026`, estación contractual EGLC, NOAA/NWS metric `https://www.weather.gov/wrh/timeseries?site=eglc`, brackets observados <=16,17…25,>=26 °C. Faltan IDs Gamma/conditions/assets, TZ exacta de day, transformación entero/rounding, fee/book → real INELIGIBLE. A resolución NOAA, B pronóstico Open-Meteo Ensemble (grilla ≠ EGLC), C label settlement contractual; mantener distintos. Forecast histórico member-level insuficiente: captura prospectiva después, no validación estadística mañana.

**Success offline:** `WeatherContract→admission causally valid→ensemble complete→bucket probabilities→model fair value→valid depth+fee→assessment/risk→SCREEN`, mismos artifacts y outputs en Strategy REPLAY y SHADOW con candidate legs reales del fixture; INCONCLUSIVE si fee/spatial/contract desconocidos. Nada de orders, ML grande, Gaussian inventada, recorder exclusivo, data lookup/clock/HTTP en callbacks ni resolución final como feature. Walk-forward OOS/Brier/log loss/reliability/net executable economics/capacity/capital lock son experimento POSTERIOR, no gate de POC sintética.

## SPEC técnica v1

### WX-BASE-V1 — sintético completo, sin licencia ni API

Event `SYN-WX-20260920-HIGH-UTC`; five separate binary Markets `SYN-M-B0..B4`, Conditions `SYN-C-B0..B4`, YES `SYN-Y-B0..B4`, NO `SYN-N-B0..B4`; estación `SYN-EGLC`, `DAILY_MAX_TEMPERATURE`, source synthetic integer Celsius **already published domain (NO rounding)**; local `2026-09-20`, zone `UTC`, half-open `[2026-09-20T00:00:00Z,2026-09-21T00:00:00Z)`, aggregation max. Buckets exhaustive on integer domain: B0 `<=18`, B1 `=19`, B2 `=20`, B3 `=21`, B4 `>=22`. Source missing ⇒ no payout invented. Rule revision immutable known_at <= frame. Station/source exact equality.

Vintage base reference `2026-09-19T00:00Z`, available `06:10Z`, received `06:11Z`, frame `12:00Z` same date; ten complete uniform model-weight members maxima `[18,19,19,20,20,20,21,21,22,23]`; probabilities `[.10,.20,.30,.20,.20]` exactly. YES ask books: B0 `0.12×100`, B1 `0.19×100`, B2 `0.24×20`+`0.27×80`, B3 `0.205×100`, B4 `0.21×100`. Default buy 10 shares. Synthetic fee ONLY `shares×0.05×price×(1-price)`; one-level B2 0.24 effective 380bps on notional; B2 notional 2.40, fee .0912, expected payout 3.00, net +.5088 / +.05088/share. B4 expected payout 2.00 < notional 2.10 ⇒ REJECT. F19 at ask .29: notional 2.90, gross +.10, fee .10295, net -.00295. **Synthetic arithmetic not market edge**; no universal feeRate assumed. Multi-level fee remains SFG-02 if needed.

**Typed concepts** (reuse actual HEAD types, names not structs frozen): `WeatherMarketContract`: event/market/condition/yes/no asset IDs, bucket, rules revision/hash known_at, payout source/station/variable/unit/domain, rounding enum, IANA timezone+local date+window, aggregation/fallback/revision cutoff/provenance. `ForecastVintage`: provider/run/model/version/reference/availability/received/valid window/raw hash/revision/terms; `WeatherForecast`: variable/unit/target station or declared grid/member set/IDs/weights/series/quality; `WeatherObservation`: observation/publication/receive, preliminary/final/revision/hash/label-only isolation; `WeatherOutcomeBucket`: lower/upper inclusivity and explicit Other-complement only. `∀x in published resolution domain: exactly one bucket` unless rules explicitly permit exceptions. REAL unknown payout-affecting detail => CONTRACT_AMBIGUOUS, not default.

**Causal invariants:** `rules_known_at <= frame`; `forecast_reference <= provider_availability <= received_at <= frame`; `capture_seq <= frame.CutSeq` with ACK durable; valid window complete; station/grid mapping explicit; variable/unit exact or authorised rational transform (`°F=°C×9/5+32`), no invented rounding, provider version/raw hash. No last-known-before-run substitutes on REPLAY, no source init interpreted as public availability; later resolution observations are ONLY label post-frame. Missing member rejects, never renormalize hidden missing mass. Uniform weights model-assumed, finite/nonnegative, sum positive; `P(B)=Σw(member∈B)/Σw`, sum 1, exactly one bucket/member, `UNCALIBRATED`, uncertainty measured member_count/dispersion, unknown calibration error/station bias; deterministic forecast diagnostic only (`fair_value absent`, no candidate). Decimal exact/integer boundary. `fair_yes=p`, `fair_no=1-p`; Economics executable ask/depth and fee bounds; gross-midpoint NOT executable edge; fees unknown INCONCLUSIVE; insufficient depth REJECT; net<=0 reject; Risk real enforcement to be demonstrated, no orders.

**Weather reasons:** `WX_CONTRACT_AMBIGUOUS, WX_SOURCE_UNAVAILABLE, WX_RULE_VERSION_MISMATCH, WX_STATION_MISMATCH, WX_VARIABLE_MISMATCH, WX_UNIT_MISMATCH, WX_LOCAL_DATE_MISMATCH, WX_VALID_WINDOW_MISMATCH, WX_BUCKET_OVERLAP, WX_BUCKET_GAP, WX_BUCKET_UNMAPPABLE, WX_FORECAST_AFTER_FRAME, WX_AVAILABILITY_UNKNOWN, WX_MEMBER_SET_INCOMPLETE, WX_WEIGHTS_INVALID, WX_PROBABILITY_INVALID, WX_PROBABILITY_MASS_INVALID, WX_DETERMINISTIC_UNCALIBRATED, WX_SPATIAL_MAPPING_UNCALIBRATED, WX_FEE_UNRESOLVED, WX_DEPTH_INSUFFICIENT, WX_COSTS_ERASE_EDGE, WX_RESOLUTION_LEAKAGE`. Reusar reason vocabulary engine cuando coincide. F03/F15/F20 diagnostics requieren SFG-05 output sin Opportunity; no crear falsas opportunities para emitir métricas.

### Fixtures F01–F20 — inputs y expected explícitos; 0 ejecutadas hoy

Todas heredan WX-BASE-V1 salvo delta; escribir archivos exclusivos Weather sólo mañana luego de A0, tests offline sin Internet. Synthetic namespace/hash obligatorio.

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

**Properties:** member order independence, exact probability mass, no overlap/gap, deterministic serialization+hashes, no future external admission, rule revision as-of, duplicate same ID/hash idempotence vs conflicting hash fail, different schedules same Strategy/Frame digest, no label leakage, missing member reject. Safety priority F03/F11/F12/F16/F17/F18/F19/F20; scorecard output when F03/F15/F20 yield zero opportunities must test SFG-05. No synthetic observations described as payout real.

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

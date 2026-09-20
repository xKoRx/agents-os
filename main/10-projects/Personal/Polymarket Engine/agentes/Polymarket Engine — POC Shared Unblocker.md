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
due: 2026-09-21
progress: 0
repo: "https://github.com/xKoRx/polymarket-engine"
jira:
prs:
aliases:
  - Polymarket POC Shared Unblocker
  - Strategy Factory Shared Foundations
  - SFG Shared Gates
  - PE001 PE030 PE004 Unblocker
tags:
  - kind/project
  - area/personal
  - domain/trading
  - tech/polymarket
  - topic/prediction-markets
created: 2026-09-20
updated: 2026-09-20
---

# Polymarket Engine — POC Shared Unblocker

> [!warning]+ Proyecto agente de integración, no POC ni nueva arquitectura
> **Padre:** [[Polymarket Engine — MVP]] · **Consumidores:** [[POC-S03 — Sports Combinatorial]] (PE-001), [[POC-S04 — Weather]] (PE-030), [[POC-S05 — New Market Maturation]] (PE-004). **Estado:** `PROJECT_PERSISTED / LOCAL_MATERIALIZER_AND_BRIDGE_PENDING / IMPLEMENTATION_NOT_STARTED`. `progress: 0` mide ejecución. Un solo agente developer es owner de TODOS los módulos compartidos durante este mandato; mañana los agentes POC sólo escriben sus paquetes propios. **LIVE_DISABLED**, sin órdenes reales.

## 🎯 Objetivo

Eliminar ANTES del sprint de POCs los bloqueos transversales demostrados por las tres reconciliaciones del 2026-09-20, reutilizando RS v0.1–v0.3, M1/M2 frozen y M4 no-live. Entregar un contrato común efectivamente compilado/probado para profundidad L2 causal, fees/quotes correctas, Strategy SCREEN→REPLAY→SHADOW, salida descriptiva sin oportunidades, observaciones Weather externas y datasets aislados. Investigar y, sólo en la medida necesaria para el alcance integral PE-004, cerrar la proyección `new_market` tipada con identidad/tiempos correctos. **No implementar lógica Sports Combinatorial, modelo probabilístico Weather ni detector/cohortes Maturation:** los desarrolladores PE-001/030/004 son sus owners. No probar alpha ni exigir datasets reales para certificar los contratos offline.

**Resultado global `POC_SHARED_FOUNDATIONS_READY`:** SFG-01/02/03/04/05/07 tienen test y receipt PASS en un baseline de código único; SFG-06 PASS para cohorte W si se implementa, o `WS_COHORT_BLOCKED` explícito sin bloquear la cohorte O/B y el núcleo común; se publican un manifest de contratos, ownership y handoffs de los tres consumidores. `REAL_DATA_READY`, profitability, venue fills y LIVE no forman parte del gate. Si un requisito crítico no puede resolverse sin reabrir contrato frozen no autorizado, estado `SHARED_FOUNDATIONS_PARTIAL/CONTRACT_DECISION_REQUIRED`, con el resto efectivamente entregado y sin PASS ficticio.

## 📊 Estado actual

- Fuentes de verdad: padre y tres hijos arriba. Los tres proyectos reportan `READY_AFTER_SHARED_GATE`, implementación 0% y matrices SFG reconciliadas; las observaciones se basan en inspección remota, NO tests locales. Este proyecto centraliza ownership y recibos, sin reemplazar los planners propios. La creación de este archivo por integración GitHub usa el esquema del template `70-templates/project.md`; la materialización por script, lint/Graphify, registro change_log, sync y puente padre **NO ejecutados en esta sesión remota** y deben reconciliarse en el preflight local sin duplicar o sobrescribir archivos.
- Engine: `main@9ae5ddec1a0e52fdc0bbde608cd0504e644d05a5` es M4 histórico; `feature/research-strategies-v01@25f578a502ce0c9e1ad27a93537a868a94533b34` es último HEAD REMOTO inspeccionado el 20-09. **HEAD LOCAL desconocido y puede avanzar.** No existe branch `master` en engine. `25f578a` contiene un checkpoint *mid-capture* RS v0.3, no evidencia cerrada o backup consistente. No borrar, modificar, abrir en modo escritor, copiar DB+WAL en caliente, detener proceso, commitear snapshots activos ni ejecutar SCREEN/SHADOW contra `.rs-v03-sports/`.
- Símbolos ya existentes en feature: `cmd/engine/screen.go::{screenFactories,screenPipeline,toStrategyFrame}`, `screen-consolidated`; `internal/experiment/experiment.go::{RunShadow,shadowStrategyFor,fillCandidate,Scorecard}`; Strategy/Factory/runtime, Capture/Books/Frames/Regimes, Economics/Simulator/Account/Risk. Reutilizar, no reconstruir. `internal/strategy/pocs/pocdata/pocdata.go`: `TopLevels=6`, `DepthFresh` valida full-book timestamp, delta deja depth stale; `frames.AssetSnapshot.Levels` es un contador y `Extras` no implica full depth. `economics.BuildQuote` utiliza BPS×notional, no prueba fees price-dependent/rounding market-specific. `strategy.Frame`/`frames.DeliveryFrame` carecen de observaciones externas tipadas; Capture/protocol rechazan surface desconocida; screen carga sólo marketws. `experiment.Scorecard.StrategyMetrics` es last-wins por Assessment; 0 opportunities pierde métricas y `scorecardHash` no cubre todas. `new_market` es conocido en parser pero sólo raw, no lifecycle tipado/proyectado. `RunShadow` tiene fallback de 10 shares sintéticas desde BBO para ACCEPT sin Candidate, inaceptable para los nuevos consumidores. Las afirmaciones son del remoto `25f578a`; P0 verifica contra local antes de escribir.
- No hay ningún PASS implementado por crear el planner. Baseline de M4 certificó versión ANTERIOR; un nuevo commit no hereda ese certificado. El agente registra regresión y resultado no-live nuevo, nunca `M4_CERTIFIED_NON_LIVE` sobre otro SHA sin recertificar el harness adecuado.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| `xKoRx/polymarket-engine` | Crear worktree exclusivo `feature/shared-poc-unblocker` sólo después de verificar que el nombre está libre y no hay cambios ajenos; partir del último commit estable de `feature/research-strategies-v01` identificado en P0 | Referencia remota `25f578a`; **pin real local obligatorio** antes de código | `## SPEC funcional v1` en esta nota y SFG de los tres hijos | `## SPEC técnica v1` en esta nota, contratos M1/M2 frozen y símbolos reales por P0 | PLANNED / CODE_NOT_STARTED |
| `xKoRx/agents-os` | `master`, edición local mediante mecanismo canónico de vault/autosync | Nota remota creada; SHA local, writers y sync por verificar | Esta nota es planner único de este esfuerzo | `## Matriz SFG`, WPs, gates, test matrix y handoffs aquí | PROJECT_PERSISTED / LOCAL_VALIDATION_PENDING |

**Ownership / allowed files:** sólo el agente de este proyecto puede modificar código compartido indispensable en `internal/books/`, `internal/frames/`, `internal/economics/`, `internal/regimes/`, `internal/strategy/api.go` y runtime, `internal/protocol/`, `internal/capture/`, `internal/replay/`, `internal/experiment/`, `cmd/engine/` y sus tests cuando un WP enumera paths exactos y evidencia demuestra necesidad; no es licencia para editar todos esos directorios. Default read-only; P0 fija manifest exacto de allowed files por WP y mínimo cambio. Puede crear tests/fixtures de contrato compartido en directorio canónico del engine, decidido en P0. **No tocar** paquetes POC `pocs/{sports,negrisk,sportscombinatorial,weather,maturation}` ni notas S03/S04/S05, módulos trading live, wallet/order/signer, M4 certificates originales, secrets, active RS datasets, `go.mod` por comodidad o schema DB sin necesidad demostrada. Cambios comunes se hacen en worktree exclusivo, commits locales por gate sólo si policy permite; **no push ni merge automático**. Padre solo para una tarea puente única vía writer local, después de verificar conflictos; no overwrite remoto de 428 KB.

## 🧩 Subproyectos

Ninguno. Este es un proyecto de agente hermano de S03/S04/S05, no su padre ni una nueva Strategy. **Puente requerido en padre, pendiente de edición segura local:** `- [ ] [[Polymarket Engine — POC Shared Unblocker]] arrancar + seguimiento; desbloquear contratos SFG-01/02/03/04/05/07 y evaluar SFG-06; Review humana. #owner/me #type/supervision #area/personal`. Detectar task equivalente y reutilizarla; no duplicar. El agente la mueve a `[r]` al entregar, nunca `[x]`. Si parent conflictivo, `PARENT_BRIDGE_PENDING` y registrar blocker, no sobrescribir trabajo ajeno.

## ✅ Tareas

- [ ] **P0.1 — Bootstrap y autoridad:** workflow Agents-OS, identidad única y cambios concurrentes; HEAD/status/branch/worktrees/commits ambos repos; captura viva y owner; `AGENTS.md`, policy de commits, frozen map; tomar baseline/test baseline sólo en workspace aislado. Registrar evidencia y reconciliar materializer/lint/Graphify/change_log de esta nota sin recrear la identidad. #owner/agent #type/admin #area/personal
- [ ] **P0.2 — Contratos actuales y seguridad:** inspeccionar todos los SFG contra HEAD real y tests, trazar consumidores y paths/owners exactos; levantar worktree aislado sin afectar capture y reservar `cmd/`/Frames/Economics/Experiment; preparar fixture journal nueva en temp dir y negative guard de data-dir; añadir puente único al padre sólo con writer seguro. #owner/agent #type/research #area/personal
- [ ] **A1 — SFG-07 dataset isolation:** helper/guard en la capa de composición o tests según necesidad; nunca `capture.Open` sobre data-dir activo ni `cp` caliente; fixture sintética desde cero o bundle coherente restaurado a directorio descartable; protección realpath/symlinks, hash original antes/después, negative test y receipt. #owner/agent #type/dev #area/personal
- [ ] **A2 — SFG-01 L2 as-of-cut:** contrato único de snapshot por asset+cut/seq/epoch/revision/quality/source+received time, lados ordenados, coverage/truncation explícitos y profundidad actualizada por deltas o invalidada hasta refresh; no fallback BBO→size, `Levels` count no implica liquidity. Conservar invariantes FIFO/frozen y compatibilidad; prueba dos assets same cut, full→delta→cut, epoch/gap, six-level capacity y parity por schedules. Reusar Books reducer/pocdata si sirve, no codec/DB alternativos. #owner/agent #type/dev #area/personal
- [ ] **A3 — SFG-02 fee+economics:** oracle independiente de fee vigente por schedule/market/token/cut, precio/quantity y rounding; corregir sólo seam necesario de Regimes→Economics→Simulator preservando interval/unresolved y Quote API compatible; test un nivel/dos niveles, fee revision before/after cut, fee missing, negative net, simulator parity, Sports dos patas y Weather una; no hardcode global 0.05 ni equiparar base bps con feeRate. Si fórmula real no está contractual/verificable, fail closed + fixture-only adapter explícito; no declarar REAL_FEE_READY. #owner/agent #type/dev #area/personal
- [ ] **B1 — SFG-05 output descriptivo sin opportunities:** implementar mecanismo mínimo compartido de frame-level research output versionado, métricas+reasons+quality+calibration y provenance, emitido y persistido aunque `Detect` devuelva cero; scorecard agrega por estrategia/frame sin last-wins y digest cubre contenido; backward compatibility Strategy API o migración versionada estricta; 0 fake Opportunity, Candidate, ACCEPT, orders o fills. Tests 0 opportunities, 2 instancias aisladas, changing reason changes digest, replay parity. #owner/agent #type/dev #area/personal
- [ ] **B2 — SFG-04 ExternalObservations Weather fixture-backed:** canal mínimo `provider fixture → admission typed/schema/version/known_at/received_at/hash → Capture durable → Frame as-of-cut → Strategy projection → manifest/replay` con surface admitida y idempotencia; en DataRequirements exigir soporte sin zero substitute, no network/I/O en Strategy, no usar Extras/Quality/Parameters como payload oculto, no framework vendor genérico. Tests future arrival reject, duplicate same/different hash, restart/round-trip, old manifest compatibility, two schedule parity; no proveedor real ni entrenamiento. #owner/agent #type/dev #area/personal
- [ ] **B3 — SFG-03 pipeline end-to-end:** adaptar composición/registry/selector y REPLAY para que Strategy se vuelva a evaluar en al menos dos schedules con mismo digest/assessments, manifests completos y mode fences; SHADOW sólo Candidate.Legs con BookView causal y fee resuelta para fills, o `INCONCLUSIVE/DATA_BLOCKED` sin fill ficticio. Mantener fixture-neutral legacy sólo en su alcance explícito; PE004 descriptiva exige cero ActionCandidate y scorecard válido. Tests consumer stubs de un basket dos legs, Weather one-leg con external y PE004 zero-opp; no implementar estrategias de las POCs, no registrar factories que aún no existen. #owner/agent #type/dev #area/personal
- [ ] **C1 — SFG-06 new_market lifecycle, alcance condicional de cierre:** comprobar contra HEAD si tipado/proyección existen; si faltan y tiempo/cambios permitidos, extender parser/capture→Catalog→UniverseChanged de forma mínima, identity namespace y known-at correctos, replay/dedup; WS timestamp no implica created_at. Test raw→journal→catalog y out-of-order; si no cabe, publicar `WS_COHORT_BLOCKED` con archivos/test/owner y PE004 O/B desbloqueada. No crear collector general. #owner/agent #type/dev #area/personal
- [ ] **C2 — Regresión + handoff triple:** compilar y correr test/vet/race, cobertura real según policy, tests de compatibilidad M4/RS y safety no-live; test de fixture journal inmutable, manifest/hashes, dos schedules; verificar diff/allowed files y no push. Publicar matrix SFG por consumidor, SHA final, comandos+recibos, branch/worktree y tres contratos de uso copiables (sin modificar las notas POC), actualizar progreso/bitácora y dejar puente padre `[r]` sólo tras evidencia. #owner/agent #type/testing #area/personal

## SPEC funcional v1

**Consumidores y criterios de entrada.** PE001 A prueba payouts sin dependencia compartida; B/C consumen depth/fee/runtime. PE030 A modela ensemble offline; B/C consumen external+depth/fee/runtime y opcional abstention output. PE004 A calcula métricas y cohortes O/B offline; B/C consumen descriptive output/runtime/depth causal, mientras W usa lifecycle. Un gate real-data/alpha no bloquea pruebas offline. No cambiar las tres hipótesis para acomodar el engine. La capacidad común debe ser un contrato reutilizable con productor owner, consumidor tipado, estado de calidad, provenance y tests; un solo owner por archivo. Una capacidad puede declararse NO_REQUIRED por un consumidor específico sin fingir PASS global.

**SFG-01**: un cut C fija todos los assets, mismo universo/revisiones/regímenes conocidos; L2 tiene price×size y limites explícitos, asset/epoch/capture sequence/source time/receive time/revision/hash/quality. Nivel truncado no es depth total; cobertura positiva de la cantidad solicitada puede certificarse si niveles son frescos y suman capacidad requerida. Deltas actualizan snapshot desde reducer verificado o invalidan la vista hasta full fresco; ningún latest lookup en Strategy. Invariante old epoch/gap/over-budget→INELIGIBLE/UNKNOWN, no SELL a asks ni BUY a bids.

**SFG-02**: Economics puro calcula sweep con foundation.Decimal. Modelo fee por market/schedule/version/cut y redondeo exacto cuando documentado; POINT/INTERVAL/UNRESOLVED/SUSPECT preservados; para valores unknown no ACCEPT ni fill neto declarado; no duplicar pricing en POCs. Verificar fee por nivel si es dependiente de price, contra oracle independiente, y paridad Simulator. Nunca prometer fee real por un ejemplo sintético.

**SFG-03**: usar mismo Factory/Strategy y entrada causal SCREEN, REPLAY (evaluaciones, no sólo delivery), SHADOW virtual. Registración futura de factories de PE001/030/004 sigue propiedad del manager mañana y no es prerrequisito hoy; pruebas de contrato con factories stub sin identidad PE propia. No fabricar book/fees para producir fills. SHADOW no requiere fills en observer descriptivo. Runners pueden escribir en su dataset: eso NO es lectura estricta; prohibido data-dir activo.

**SFG-04**: ExternalObservation v1 mínimo: identity source/key, schema/version, event/reference/available/received/known-at, payload/ref/hash, quality, dedup/contradiction, cut/revision; bytes raw durables antes de estrategia. Capture surface, Frame, Strategy, runner y replay versionados; ingreso weather fixture respaldado por raw con same input digest reproducible; missing/late data WAITING_DATA/INCONCLUSIVE sin current/latest backfill. La semántica meteorológica (station, buckets, ensemble) permanece PE030.

**SFG-05**: research frame observation output con métricas/denominadores/reasons por instance/strategy/run/frame y hash de contenido completo; persiste sin oportunidad y coexiste con evaluación clásica, no se usará Candidate como portador de métricas. PE004 puede devolver zero opportunities manteniendo observaciones auditables; Weather puede registrar abstenciones. Digest canonical por orden, no mezcla o last-wins.

**SFG-06**: marketws `new_market` reconocible tipado con Gamma market ID vs condition vs asset IDs distintos; raw durables, known-at=admission, retries/dedup y first-notice sin antedatar con timestamp venue; proyectar a Catalog si mínimo permitido; cohorte O existing NO depende de W; creation-known no se inventa.

**SFG-07**: input-only fresh fixtures generadas en temp workdir o backup consistente detenido/verificado/restaurado; `.rs-v03-sports/` excluido y proceso activo protegido; no escritura indirecta por `capture.Open`, `screen`/`shadow`. Nunca certificar `25f578a` como snapshot completo ni incorporar WAL/JOURNAL activos en commits. Datos reales quedan fuera del contrato shared PASS.

## SPEC técnica v1

**P0 obligatorio:** antes de escribir, verificar rama/HEAD/status/owners/policies/repo local y comparación SHA remoto; inspeccionar `cmd/engine/screen.go`, `internal/strategy/api.go`+runtime, `internal/frames/`, `internal/books/`, `internal/economics/`, `internal/regimes/`, `internal/experiment/`, `internal/replay/`, `internal/protocol/`, `internal/capture/`, `internal/catalog/`; seleccionar código existente y materializar paths exactos por WP. Los paths de ownership de arriba son CANDIDATOS/owners, no whitelist en bloque. Crear branch/worktree exclusivo sin tocar el checkout que ejecuta RS capture. Si branch ya existe, inspeccionarla en vez de sobrescribirla. No cambiar un contrato M1/M2 frozen incompatiblemente: preferir extensión aditiva versionada y tests; una ruptura requiere decisión concreta del owner, registrar `CONTRACT_DECISION_REQUIRED` y continuar gates independientes.

**Contrato de evidencias por gate:** `ID,baseline SHA,final SHA,changed files,exported symbols/contracts,fixtures,cmd/exit/test names,coverage,consumer matrix,reason,rollback,original dataset hash(before/after),known limitations`. Estados separados `NOT_STARTED,IN_PROGRESS,PASS,PARTIAL,BLOCKED,NOT_REQUIRED`. `PASS` sólo si test realmente corrido; existencia de test y lectura de source se marca `EXISTING_NEEDS_TEST`. En commit nuevo baseline M4 certificate stale por identidad hasta recertificación; no tocar certificate previo. Registry/suite smoke de las POCs puede usar doubles/stubs, pero **no afirmar que PE001/030/004 ya corren si sus packages no existen**.

**Orden crítico:** P0→SFG-07→SFG-01→SFG-02→SFG-05→SFG-04→SFG-03→regresión/handoff. SFG-03 puede desarrollarse incrementalmente, pero PASS sólo tras tests del resto. SFG-06 puede iniciarse después de P0 en scope independiente, pero el agente único prioriza primero SFG-01/02/04/05. Un fallo SFG-06 NO consume el tiempo crítico de las otras tres POCs. Si soporte compartido ya es correcto, escribir sólo test y cerrar gate, sin cambio ornamental. No generar migración innecesaria, proveedores HTTP, estrategia propia ni framework universal.

**Pruebas nuevas requeridas (nombres de intención, no símbolos preexistentes):** `TestSFG07ActiveDirRefused`, `TestSFG01FullDeltaEpochCutAndCapacity`, `TestSFG02PriceDependentTwoLevelsAndUnknownFee`, `TestSFG05ZeroOpportunityObservationDurableDigest`, `TestSFG04ExternalKnownAtReplayNoLeak`, `TestSFG03ThreeConsumerContractParity`, `TestSFG06NewMarketKnownAtDedup`. El ejecutor fija ubicaciones/nombres Go reales en P0; ninguna prueba está marcada ejecutada todavía. Fixtures aisladas, oracle fee independiente y casos negativos FIRST. Quality gate: `go build ./...`, `go vet ./...`, `go test ./... -count=1`, `go test -race ./... -count=1`, coverage >=95% por paquete modificado cuando aplique según policy actual sin trucar denominador, `go mod tidy` sólo comprobación diff/no cambios innecesarios, `git diff --check`, `git status`; archtest/safety/regresión M4/RS suites seleccionadas y harness certify de nuevo baseline SI se pretende certificar M4. No test E2E contra active capture. Un `go test` rojo no se reporta PASS.

## Matriz SFG — backlog inicial sin receipts de implementación

| Gate | Consumidores | Baseline feature remoto | Owner único | Condición de PASS | Estado inicial |
|---|---|---|---|---|---|
| SFG-01 L2 causal | PE001, PE030, PE004 | `pocdata` top6; delta stale; frame sin full L2 probado | Books/Frames/composition: ESTE agente | two assets same-cut, full/delta/epoch/gap/truncation/size, fee-independent quote inputs y replay parity | NOT_STARTED; partially implemented |
| SFG-02 fees | PE001, PE030; PE004 sólo si economía posterior | Economics BPS×notional, fee schedule sin oracle per-level | Regimes/Economics/Simulator: ESTE agente | oracle independiente, price-dependent 2 niveles, rounding, POINT/INTERVAL/UNKNOWN/fee revision, no false ACCEPT | NOT_STARTED; partially implemented |
| SFG-03 runtime | Todos | factories SCREEN+SHADOW existentes, REPLAY de Strategy no demostrado, neutral fallback fake size10 | Strategy/Replay/Experiment/composition: ESTE agente | same fixture strategy SCREEN→strategy REPLAY→SHADOW, 2 schedules parity, 0 orders y observer 0 fills | NOT_STARTED; partially implemented |
| SFG-04 external | PE030 (PE001/004 no requieren) | no Surface/Frame/Strategy external fields | Capture/Frames/Strategy/Replay/composition: ESTE agente | external fixture durable→frame→replay, known-at cutoff/leak, dedup, old manifest compat | NOT_STARTED; missing |
| SFG-05 descriptive | PE004; PE030 abstención opcional | 0-opportunity metrics lost, last-wins+hash missing | Strategy/Experiment/composition: ESTE agente | durable zero-opp output, metric reasons included hash, isolated and deterministic no candidate | NOT_STARTED; missing |
| SFG-06 lifecycle | PE004 cohorte W ONLY | `new_market` raw, no verified typed Catalog projection | Protocol/Catalog: ESTE agente | raw→ACK→type→Catalog→UniverseChanged/replay, dedup/known-at, NO created_at inference | NOT_STARTED; optional relative to O/B |
| SFG-07 dataset | Todos | capture.Open may mutate; active RS mid-capture | QA/composition: ESTE agente; RS capture owner remains separate | fixture tempdir, realpath guard, active dir unmodified, no hot SQLite copy, restore only stopped coherent bundle | NOT_STARTED; prerequisite |

## Gates y Definition of Done

**G0 PREFLIGHT PASS:** current HEAD/source/owners verified; branch/worktree isolated; no active capture mutated; this note reconciled against local schema/materializer/lint and one parent bridge safely created/reused; baseline tests or explicit evidence of pre-existing failure. Local mismatch invalidates inferred source paths, not the existence of this project. **G1 SAFETY PASS:** SFG-07 negative tests and dataset isolation. **G2 MARKET PASS:** SFG-01+02 with oracle/negative tests. **G3 DATA/OUTPUT PASS:** SFG-04+05 tests/backwards compatibility. **G4 PIPELINE PASS:** SFG-03 parity across three contract stubs/modes and no real orders/fills; optional SFG-06 status recorded. **G5 HANDOFF PASS:** regression, coverage, exact commit SHA, manifest/schema/owner map, local-note sync and three handoffs with exact first WP/expected inputs; no false inherited M4 certification. `POC_SHARED_FOUNDATIONS_READY` ONLY if G0–G5 PASS, SFG-01/02/03/04/05/07 PASS and no shared blocker on PE001-B/C, PE030-B/C, PE004-B/C. PE004 W optionally `WS_COHORT_BLOCKED` with isolated followup; explicit `FULL_POC_SCOPE_READY` additionally requires SFG-06 PASS. If SFG-06 deferred, DO NOT claim that the entire original PE004 W scope is unblocked; state only O/B ready.

**Failure policy:** if a test fails: reproduce once after fixing the demonstrated root cause, record FAIL then recovery receipt, no endless retries. If frozen contract requires incompatible change: stop only affected gate, describe exact API delta/consumer and request approval at closure; continue independent gates. If test runtime budget tight: prioritize causality/unknown-fee/zero-opp/no-active-dir and deliver honest PARTIAL. No follow-up messages to owner mid-task for routine design decisions. No network trading activity, no push, no background promises.

**Handoff manifest to POC agents:** for each consumer declare `SFG requirements and statuses; feature base SHA; branch+integration commit(s); exact symbols+signatures and files; format/version; fixtures+test commands; allowed POC paths vs prohibited shared paths; known limitations; migration/replay compatibility; deterministic runner invocation using disposable dataset; first task; block reason if not PASS`. Preserve the baseline owner of each POC and do not write their project notes; manager can propagate receipts after the shared project is reviewed. Do not alter M1/M2 frozen or their original cert receipts.

## 🧭 Decisiones

- D01 Un solo proyecto agente y un solo writer compartido; no cuarto strategy/bot.
- D02 Shared dependencies code once, no per-POC monkeypatch; typed/versioned additive interfaces, no generic framework without consumer.
- D03 Safety SFG-07 precedes any test opening Capture; synthetic fixture is enough for PASS, real RS capture finalization belongs to its owner.
- D04 PE004 descriptive output is valid with zero opportunities/orders/fills; prospective trade variant PE004-B outside scope.
- D05 Weather model/station/buckets in PE030; only transport/admission external generalizes.
- D06 SFG-06 priority after critical shared gates; full PE004 W readiness requires PASS, no silent scope reduction.
- D07 Each gate technical acceptance by manager per canonical policy; human owner review/bridge never agent Done; no push.

## 📆 Bitácora

- **2026-09-20 — Proyecto creado remotamente:** leído schema project v1, `70-templates/project.md`, workflow de proyecto agente y tres planners reconciliados en `xKoRx/agents-os@master`; definido owner único, SPEC, SFG-01…07, tests y WPs. Código NO implementado; engine local/Agents-OS local, materializer, schema lint, Graphify, parent bridge y change_log pendientes de reconciliación mediante herramientas locales autorizadas. Remote feature `25f578a` es checkpoint de captura; no se tocó. Primera acción del ejecutor: P0.1. Esta nota es el planner único.
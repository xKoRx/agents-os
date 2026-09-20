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

> [!warning]+ PE-030 · fuente única de planificación · NO LIVE
> **Estado:** `PROJECT_PERSISTED / OFFLINE_CORE_CONDITIONAL / REAL_DATA_BLOCKED / LOCAL_ENGINE_GATE_PENDING` · **Hipótesis:** PE-030 · **Progreso de implementación:** 0%. Investigación no es código probado. Esta nota es el planner, SPEC, registro de bloqueos y mandato de desarrollo; no usar chats o documentos externos como planner alternativo. Trading real prohibido.

## 🎯 Objetivo

Construir una POC de Weather Forecast Mispricing determinista y falsable: identificar semántica de liquidación, admitir forecasts conocidos causalmente antes de cada frame, asignar miembros de ensemble a buckets, obtener probabilidades de modelo **NO calibradas**, evaluar únicamente precios/costes ejecutables mediante Economics y Risk existentes y emitir señales explicables en SCREEN/REPLAY/SHADOW no-live. Primera entrega: **contrato sintético completo + fixtures offline**; no simular que se dispone de contrato real válido ni de edge estadístico.

**Aceptación:** dominio Weather correcto, F01–F20 y properties aprobadas, Strategy integrada sólo tras gate de compatibilidad, SCREEN → REPLAY → SHADOW certificado en dataset descartable, manifiesto reproducible, sin I/O en callbacks, órdenes reales, recorder privado ni Economics paralelo. La validación OOS de alpha es posterior y no se declara con fixtures.

## 📊 Estado actual y fuentes de autoridad

- **Research recibido, 2026-09-20:** `PE-030 — Weather Forecast Mispricing — Deep Research & Implementation Handoff` (investigación aportada por owner, snapshot `2026-09-20T03:24Z`, estado propio `PE030_RESEARCH_PARTIAL`, evidencia IDs `E-*`; su información material queda destilada aquí y sus enlaces primarios están en Docs/Links). No atribuir al research inspección de código que no realizó.
- **Agents-OS:** `xKoRx/agents-os@master`; `POC-S04 — Weather.md` comprobado ausente inmediatamente antes de crear; vecino `POC-S05 — New Market Maturation.md` ya existía. Reconciliar checkout local/autosync antes de editar esta nota. No modificar nota padre ni otras POC ni recursos globales. No ejecutar cierre completo de sesión salvo pedido del owner.
- **Engine remoto comprobado:** `xKoRx/polymarket-engine@main` = `9ae5ddec1a0e52fdc0bbde608cd0504e644d05a5` (19-09-2026); **no es garantía de HEAD local**. Research identificaba erróneamente el remoto como sólo README: la inspección posterior de GitHub confirmó archivos reales. Baseline `7bd264d` es histórico. RS v0.3 local, worktree, cambios de agentes y repositorios de datos activos **NO inspeccionados**; gate A0 obligatorio antes de escribir engine.
- **Gap REAL comprobado en remoto 9ae5dde:** `internal/strategy/api.go::Frame` contiene Ordinal, CutSeq, Assets, Quality, RevisionVector y VirtualTime, pero **no ExternalObservations**; `internal/frames/frames.go::DeliveryFrame` tampoco transporta una colección Weather. `cmd/engine/screen.go::toStrategyFrame` proyecta sólo esos campos; `runScreen` únicamente acepta `fixture-neutral` y `capture.Open(data-dir)` puede escribir boot/recovery. Está prohibido meter forecasts en `Quality`, `AssetSnapshot.Extras` o RunContext.Parameters como canal oculto para eludir un contrato congelado. Confirmar si RS v0.3 local ya resuelve esta brecha; si no, requiere cambio aditivo explícito de seam frozen y autorización de ownership antes de integración B1. **A1 offline sigue desbloqueada después de A0.**
- **Economics remoto comprobado:** `internal/economics/economics.go`: `WalkSide`, `BookView`, `BuildQuote`, `Quote`, `FeeResolution`; `BuildQuote` maneja fee POINT/INTERVAL/UNRESOLVED y trabaja con decimal exacto. No duplicar fee/depth. Su fee POINT son bps efectivos sobre notional; la fixture Weather convierte su fórmula *sintética* a bps efectivos verificados para una única price level; nunca extrapolar a fees reales.
- **Mercado real:** candidatos Londres-high/low, Helsinki-high y Shanghai-high 20-09-2026; Londres-high referencia NOAA/NWS EGLC, pero Event/Market/Condition/asset IDs, definición contractual exacta del día/timezone, redondeo del valor publicado, fee/tick/min-size y books no están demostrados. **NINGÚN contrato real admitido**. No inventar esos datos.
- **Datos:** Open-Meteo Ensemble es candidato prospectivo, no archivo member-level retrospectivo de largo plazo; run initialization ≠ availability. Licencia comercial y calibración estación↔grilla pendientes. **No permitir señal real con estos huecos.**
- **Estado verificable de preparación:** 20 fixtures especificadas aquí, 0 fixtures nativas escritas; 0 tests PE-030 ejecutados; 0 capturas meteorológicas autorizadas; SPEC Weather v1 **congelada sólo para dominio offline**, integración engine `PENDING_A0`, estadística `NOT_VALIDATED`, LIVE `FORBIDDEN`.

### Bloqueos exactos y resolución autónoma

| ID | Bloqueo | Afecta | Acción resolutiva / condición de salida | Owner | Estado |
|---|---|---|---|---|---|
| B-ENG-01 | HEAD local RS v0.3/branch/dirty/owners no verificables remotamente | B1/C1, paths de escritura; NO modelo A1 | WP-A0 read-only: git status/branch/HEAD; inspección de código y política frozen; registrar mapa de allowed files. No reset/rebase/checkout destructivo. | coding agent | PENDING |
| B-ENG-02 | Remoto `9ae5dde` no expone Weather en `DeliveryFrame` ni `strategy.Frame` ni registro SCREEN | B1/C1, no A1 | A0 comprueba delta local; si falta, especificar mínimo cambio aditivo, versionar frame/payload y preservar replay; detener escrituras a contrato frozen hasta aprobación autorizada. No workaround por metadata opaca. | coding agent / owner del módulo frozen | CONDITIONAL |
| B-RULE-01 | Gamma IDs/token mapping + ventana diaria timezone + entero/rounding + fallback/revision sin demostración completa | mercados reales | Recuperar Gamma Event por slug, raw/hash y reglas íntegras; demostrar TZ/published-value semántica en fuente contractual; si falta, `CONTRACT_AMBIGUOUS` y abstención. | research/data agent | REAL_DATA_BLOCKED |
| B-EXEC-01 | Fee real por market/token, tick, min size, L2 as-of no demostrados | edge ejecutable real | Gamma/CLOB market+book+fees as-of y persistir refs; `INCONCLUSIVE` si falta. | data/engine | REAL_DATA_BLOCKED |
| B-DATA-01 | Miembros ensemble point-in-time históricos insuficientes; provider availability y received-at no archivados | backtest histórico | No backfill; captura prospectiva de raw/hash/run/availability/received; evaluación OOS posterior. | research/data | VALIDATION_BLOCKED |
| B-LIC-01 | Términos del servicio gratuito/uso comercial y corrección station-grid no certificados | comercial/live | No acceso pago ni comercial en v1; verificar licencia/atribución y medir bias OOS antes de elevar calidad real. | owner si requiere gasto/licencia | NOT_ON_OFFLINE_PATH |
| B-OPS-01 | `screen`/`shadow` pueden abrir Capture y escribir; datadir activo desconocido | pruebas C | Usar exclusivamente fixture dataset copiado en path temporal descartable, verificar aislamiento y capturas no modificadas; `OpenView` cuando se requiera lectura estricta. | coding agent | GATE |

**Regla:** ante bloqueo externo, continuar solamente WPs que no dependan de él. Si B-ENG-02 implica modificar contrato frozen sin autorización, declarar `PE030_PREPARATION_PARTIAL / ENGINE_CHANGE_BLOCKED` y entregar A1 offline + evidencia; no afirmar SCREEN/SHADOW certificados. No derivar al owner decisiones de bajo nivel que el source pueda resolver.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| `xKoRx/polymarket-engine` | remoto `main`; **branch local por fijar A0** | remoto inspeccionado `9ae5ddec1a0e52fdc0bbde608cd0504e644d05a5`; local **UNKNOWN** | [SPEC funcional v1](#spec-funcional-v1) | [SPEC técnica v1](#spec-técnica-v1) | WEATHER_OFFLINE_DOMAIN_FROZEN / INTEGRATION_LOCAL_GATE_PENDING |
| `xKoRx/agents-os` | `master` remoto; local UNKNOWN | nota PE-030 creada en commit independiente; comprobar checkout local y autosync | esta nota | esta nota + schema project v1 | proyecto persistido; lint/Graphify locales pendientes |

## 🧩 Subproyectos

Ninguno. No crear un segundo planner, recorder o proyecto autónomo de proveedores.

## ✅ Tareas

> [!note]+ Fuente única y estado
> Todas comienzan `[ ]`; cambiarlas a `[/]`, `[r]`, `[x]` únicamente con evidencia real en esta nota. `progress: 0` mide implementación, no páginas de research. El padre requiere una sola tarea puente humana `[[POC-S04 — Weather]] arrancar + seguimiento #owner/me #type/supervision #area/personal`; **no editar el padre ahora** por aislamiento concurrente: al reconciliar local, crearla sólo si falta y si su escritura está autorizada. El agente jamás cierra la tarea puente por sí solo.

- [ ] **A0 — preflight obligatorio / freeze local:** HEAD/worktree/owners/RS v0.3/Frame seam, allowed files, dataset activo, reason taxonomy, versiones y cambios paralelos; mapear delta contra esta SPEC; detener si incompatible. #owner/agent #type/research #area/personal
- [ ] **A1 — Weather contracts + modelo:** implementar núcleo puro, bucket mapping, ensemble v1, validadores y F01–F16 con datos sintéticos sin tocar frozen ni red. #owner/agent #type/dev #area/personal
- [ ] **B1 — integración Strategy/Economics:** Factory, Universe, requirements, frame/admission seam autorizado, Detect/Evaluate/Economics/Risk; F17–F19, SCREEN aislado. #owner/agent #type/dev #area/personal
- [ ] **B2 — adapter fixture-backed y captura común:** payload Weather versionado, causalidad, idempotencia, raw/provenance, F03/F16/F20; proveedor real explícitamente excluido si licencias/contrato no pasan. #owner/agent #type/dev #area/personal
- [ ] **C1 — REPLAY/SHADOW/certificación:** F01–F20 y properties, reproducibilidad por hash, SCREEN→REPLAY→SHADOW, regresión M4 y cobertura actual, pruebas en dataset descartable, evidencia y entrega a review del owner. #owner/agent #type/dev #area/personal

## SPEC funcional v1

**Hipótesis falsable:** un ensemble *disponible antes del frame* podría estimar probabilidades de buckets distintas de asks ejecutables; sólo un experimento posterior OOS con labels, costs y capacity demostrará si hay ventaja. Un score positivo en una fixture no prueba rentabilidad, precisión ni liquidez real. Unidad de análisis: Event meteorológico con N markets binarios por bucket; cada Market/Condition mapea YES/NO asset IDs, no un token multi-outcome.

**Universo v1:** sólo `SYN-WX-20260920-HIGH-UTC` para lógica y pruebas. Londres high `https://polymarket.com/event/highest-temperature-in-london-on-september-20-2026` queda **REFERENCE_ONLY, no admission real**. Otros candidatos: Londres low, Helsinki high (EFHK) y Shanghai high (ZSPD), todos 20-09-2026 y sin IDs comprobados en research. No fijar una estación por geocodificación. Fuentes A/B/C: A resolución contractual NOAA/NWS WRH EGLC (`https://www.weather.gov/wrh/timeseries?site=eglc`, viewer metric, datos preliminares/revisables); B forecast Open-Meteo Ensemble (grilla, no equivalente certificado a EGLC); C payout/label contractual capturado posteriormente, no reescribirlo desde observaciones climatológicas ajenas. NCEI/Meteostat opcionales NO verificados para payout.

**Flow obligatorio:** Catalog → Weather contract/data admission → Capture común → Frame causal → Strategy.Detect → Economics → Strategy.Evaluate → Risk → SCREEN; después los *mismos inputs* en REPLAY → SHADOW virtual. Ningún I/O, wall-clock, HTTP, secrets, fee calculator privado o recorder privado dentro de Strategy. Real-mode no habilitado por v1.

**Outcome:** un escenario se agrega sobre la ventana contractual precisa y se asigna a exactamente un bucket en el dominio del valor **publicado que determina payout**; no aplicar rounding físico arbitrario. `Other` es complemento del conjunto explícito sólo cuando las reglas lo definen. Si zona horaria, rounding, bucket o source cambian el winner y no están resueltos → abstención. Forecast determinista sin distribución → diagnóstico, sin fair value ni ActionCandidate.

**Señal:** `fair_value_yes=P(bucket)`; `fair_value_no=1-P(bucket)` son outputs de modelo UNCALIBRATED. Economics existente determina sweep ask/size, VWAP, fees/cost bounds y requerimiento capital; `probability - midpoint` NO es edge. Fee UNRESOLVED, depth insuficiente o net <= 0 ⇒ cero candidato ejecutable. Risk aplica sólo después y sólo sobre una assessment aceptada con inputs completos; no crear órdenes reales.

**Experimento posterior (NO ejecutar ahora):** captura prospectiva, labels post-resolution, train/test cronológico agrupado por Event, Brier/log-loss/reliability por bucket/horizonte/estación, benchmark precio contemporáneo, net payoff as-of, capacity y capital lock. Ni señales sintéticas ni intervalos de ensemble son probabilidades calibradas.

## SPEC técnica v1

### Contrato sintético FROZEN `WX-BASE-V1`

| Campo | Valor explícito |
|---|---|
| Event | `SYN-WX-20260920-HIGH-UTC` |
| Markets | `SYN-M-B0`, `SYN-M-B1`, `SYN-M-B2`, `SYN-M-B3`, `SYN-M-B4` |
| Conditions | `SYN-C-B0` … `SYN-C-B4`, uno por Market |
| YES/NO tokens | `SYN-Y-B0`…`SYN-Y-B4`; `SYN-N-B0`…`SYN-N-B4` |
| Estación / variable | `SYN-EGLC` / `DAILY_MAX_TEMPERATURE` |
| Source/domain | sintética; valor publicado entero en °C, **no existe etapa rounding** |
| Día, timezone y ventana | `2026-09-20`, `UTC`, `[2026-09-20T00:00:00Z,2026-09-21T00:00:00Z)` |
| Agregación | máximo sobre timestamps dentro de ventana half-open |
| Buckets | B0 `T<=18`, B1 `T=19`, B2 `T=20`, B3 `T=21`, B4 `T>=22`, integer-domain exhaustivo |
| Source missing | inválido, no ganador inventado |
| Revisiones | `rules_hash` inmutable; únicamente revisión known_at <= frame_ts |
| Provenance | prefijo `SYN`, schema/rules/model/fixture hash, sin apariencia de mercado real |

**Vintage base:** reference `2026-09-19T00:00:00Z`; availability `2026-09-19T06:10:00Z`; received `2026-09-19T06:11:00Z`; frame `2026-09-19T12:00:00Z`. Diez miembros completos, weights de modelo uniformes `1`, máximas publicadas sintéticas `[18,19,19,20,20,20,21,21,22,23]` → `P(B0..B4)=[0.10,0.20,0.30,0.20,0.20]`, suma exacta 1.

**Books YES sintéticos:** B0 ask `0.12×100`; B1 `0.19×100`; B2 `0.24×20` + `0.27×80`; B3 `0.205×100`; B4 `0.21×100`. Cantidad requerida 10 shares, si no se especifica otra. Para fixture *exclusivamente*, `fee = shares × 0.05 × price × (1-price)`; para la capa `economics.BuildQuote` representar la tarifa efectiva de un único nivel por `fee_bps=0.05×(1-price)×10000`: B2 a `0.24` = **380 bps** sobre notional; F19 `0.29` = **355 bps**. No hardcodear esta fórmula para Polymarket real; en sweeps multinivel hace falta una política fee de régimen explícita, no una tasa media inventada.

**B2 BUY 10:** notional `2.40`; fee `0.0912`; cost `2.4912`; expected payout `3.00`; net `+0.5088` total / `+0.05088` por share → ACCEPT sintético sólo si Economics reporta ese resultado sin costes adicionales y Risk aprueba. **B4 BUY 10:** expected payout `2.00`, notional `2.10` antes de fee ⇒ REJECT. No representar fills reales.

### Data contracts conceptuales (reusar tipos de HEAD; NO son structs aprobados)

| Contract | Campos requeridos / invariantes |
|---|---|
| `WeatherMarketContract` | event_id, market_id, condition_id, yes/no asset_id, bucket_id, rules version/hash+known_at, resolution URL/source, station_id, variable, published unit/domain, explicit rounding enum, local date, timezone IANA, `[start,end)`, aggregation, fallback, revision cutoff, provenance. `UNKNOWN` semántico real bloquea. |
| `ForecastVintage` | provider/model/version/run/reference, publication optional, provider availability **obligatoria real**, received_at obligatorio, target station/grid exacto, forecast validity, revision, raw SHA/hash, terms ref. No version sobrescrita. |
| `WeatherForecast` | vintage ref, station/grid mapping declarado, variable, unidad, series/aggregation target, member_set_id, expected member IDs/count, members + weights, quality+calibration flag. Missing member NO renormalizar. |
| `WeatherObservation` | observation_time, publication_time, received_at, station, variable, published value/unit, prelim/final/revision, quality, source hash, eligibility para cutoff; resolución posterior sólo label, nunca feature pasada. |
| `WeatherOutcomeBucket` | predicate en resolution domain, lower/upper e inclusividad, explicit Other=complement; exactly-one assignment y cobertura sobre dominio declarado. |

**Numéricos:** usar `foundation.Decimal` y dominio entero cuando fuente publica integer por contrato. Conversión física exacta `°F=°C×9/5+32` en racional/decimal; una conversión NO define rounding. Evitar float64 en límites. Validar negativos, intervalos solapados/gaps/Other, días DST de 23/25 horas, missing preliminary/final y versión de reglas. Si el forecast modela decimales pero payout es entero y no existe transformación contractualmente probada: `WX_CONTRACT_AMBIGUOUS`, sin probabilidades operables para mercado real.

**Causal admission:** `rules_known_at <= frame_ts`; `forecast_reference_time <= provider_availability_time <= received_at <= frame_ts`; `valid_window` debe cubrir exactamente ventana contractual o permitir derivar todos los timestamps sin extrapolación; station/grid mapping explícito; variable/unit compatibles; provider version y raw hash persistidos antes de evaluación. Issue/init time solo NO prueba disponibilidad. Si provider availability desconocida para datos históricos → `WX_AVAILABILITY_UNKNOWN` / ABSTAIN. `receive_time` pertenece a envelope `ExternalObservation` real si existe; Weather payload conserva tiempos meteorológicos sin duplicar campos top-level innecesarios. Capturar bytes/hash con Capture común; REPLAY sólo artefactos inmutables, nunca consultar endpoint "latest".

**Modelo `wx-empirical-ensemble-v1`:** validar member set completo, pesos finitos/no negativos y suma positiva; v1 uniformes por *suposición declarada*, no pesos oficiales ni calibración. Agregar cada serie sobre la ventana, transformar al resolution domain sólo con regla explícita, asignar exactamente un bucket; `P(Bi)=sum(weights of members in Bi)/sum(all valid declared weights)`; escala positiva legítima se normaliza, faltantes/members inválidos no. Con uniformes conservar conteos/N y suma exacta. Output versionado `calibration=UNCALIBRATED`, `weight_policy=UNIFORM_MODEL_ASSUMPTION`, uncertainty medida `{dispersion,member_count}`, no medida `{calibration_error,station_bias,model_error,transform_error}`. Nunca intervalo de confianza inventado ni Gaussian por defecto.

**Reasons propuestos, deduplicar con enum/taxonomy real en A0:** `WX_CONTRACT_AMBIGUOUS`, `WX_SOURCE_UNAVAILABLE`, `WX_RULE_VERSION_MISMATCH`, `WX_STATION_MISMATCH`, `WX_VARIABLE_MISMATCH`, `WX_UNIT_MISMATCH`, `WX_LOCAL_DATE_MISMATCH`, `WX_VALID_WINDOW_MISMATCH`, `WX_BUCKET_OVERLAP`, `WX_BUCKET_GAP`, `WX_BUCKET_UNMAPPABLE`, `WX_FORECAST_AFTER_FRAME`, `WX_AVAILABILITY_UNKNOWN`, `WX_MEMBER_SET_INCOMPLETE`, `WX_WEIGHTS_INVALID`, `WX_PROBABILITY_INVALID`, `WX_PROBABILITY_MASS_INVALID`, `WX_DETERMINISTIC_UNCALIBRATED`, `WX_SPATIAL_MAPPING_UNCALIBRATED`, `WX_FEE_UNRESOLVED`, `WX_DEPTH_INSUFFICIENT`, `WX_COSTS_ERASE_EDGE`, `WX_RESOLUTION_LEAKAGE`. Faltas contractuales previas a Economics → no llamada a Economics/Risk. Fee desconocida → assessment `INCONCLUSIVE`, no candidate; forecast determinista → diagnóstico `INCONCLUSIVE` sin fair value.

### Mapa de integración — autoridad código remoto inspeccionado vs local

| Requerimiento | Símbolo / archivo observado en `9ae5dde` | Resolución / dueño | Estado |
|---|---|---|---|
| Lifecycle/Factory/Universe/DataRequirements/Evaluate | `internal/strategy/api.go::{Strategy,Factory,UniverseSpec,DataRequirements,EvaluationContext}` | Strategy owner; `UniverseSpec` sólo Name/Markets, `DataRequirements` sólo MaxBookAge/MaxMetadataAge/MinAssets/AllowsCoalescing; no external req tipada en remoto | REMOTE_VERIFIED / LOCAL_UNKNOWN |
| Causal frame | `internal/frames/frames.go::{DeliveryFrame,AssetSnapshot,RevisionRef}` | Frames owner, snapshot de book BBO + `Levels` número, NO price×size depth ni forecast | REMOTE_VERIFIED / SEAM_GAP |
| Projection SCREEN | `cmd/engine/screen.go::toStrategyFrame`, `runScreen` | composición: sólo fixture-neutral, Frame sin Weather, `capture.Open` potencialmente escribe | REMOTE_VERIFIED / SEAM_GAP |
| Runtime | `internal/strategy/runtime.go::{NewInstance,DeliverFrame}` | actor serial, journal runtime durable | REMOTE_VERIFIED |
| Economics | `internal/economics/economics.go::{BookView,WalkSide,BuildQuote,Quote}` | BBO no basta; obtener L2 mismo cut de Books, fee `regimes.FeeResolution` as-of; sin duplicar cálculo | REMOTE_VERIFIED / L2_SEAM_GAP |
| Registry / Catalog / capture / replay / risk / simulator / experiment | `internal/catalog/**`, `internal/capture/**`, `internal/books/**`, `internal/replay/**`, `internal/risk/**`, `internal/simulator/**`, `internal/experiment/**` según árbol remoto | contratos exactos y ownership locales se verifican en A0; no asumir que source es idéntico a RS v0.3 | DIRECTORY_VERIFIED / SYMBOLS_PENDING |

**Decisión de integración si A0 confirma el gap:** definir cambio *aditivo mínimo* que preserve inmutabilidad, durability y replay: observaciones meteorológicas versionadas en el `DeliveryFrame` causal y su proyección `strategy.Frame`, con refs de capture/hash/revision y payload resoluble sin I/O en callbacks; cotización L2 + fee del mismo cut entregada a Economics fuera de Strategy. No usar `Quality`, `Extras`, parámetros de arranque ni lecturas latest como transporte de payload; no tocar módulos frozen sin autorización de su owner/policy. Si la rama local ya dispone de `ExternalObservations`/`DepthQuote` adecuados, reutilizarlos y descartar este cambio propuesto. Cualquier modificación a hash/digest, journal o backwards compatibility necesita tests de replay/vintages antes de PASS. No hay fundamento para declarar G4 PASS hoy.

### Fixtures offline F01–F20 — entrada y salida obligatorias

Todo caso hereda `WX-BASE-V1` salvo delta explícito. Outputs no son trades reales. Cada fixture debe materializarse en archivos exclusivos PE-030 durante implementación, con input/output JSON deterministas y hashes; no crear archivos de engine durante esta preparación.

| ID | Input/delta concreto | Expected output y gate |
|---|---|---|
| F01 | Contrato base cinco mercados binarios B0..B4, dominio entero, ventana UTC | `VALID`, cinco condition/token mappings; contrato PASS, Economics no llamado. |
| F02 | Diez miembros `[18,19,19,20,20,20,21,21,22,23]` peso 1, frame `2026-09-19T12:00Z`, books base; BUY B2 size 10 | `P=[.10,.20,.30,.20,.20]`, B2 net `+0.5088` (`+0.05088/share`) usando fee effective 380bps; B4 REJECT, Risk sólo puede recibir B2 si permitido; SCREEN sintético. |
| F03 | Mismos miembros, `provider_availability=2026-09-19T12:05Z` vs frame `12:00Z` | `WX_FORECAST_AFTER_FRAME`, no probabilidades/opportunity/Economics; REJECT. |
| F04 | `forecast.station=SYN-EGLL` vs `SYN-EGLC` | `WX_STATION_MISMATCH`, no modelo/Economics; REJECT. |
| F05 | Forecast `DAILY_MIN_TEMPERATURE` vs contract `DAILY_MAX_TEMPERATURE` | `WX_VARIABLE_MISMATCH`, no modelo; REJECT. |
| F06 | `forecast.local_date=2026-09-21` vs contract `2026-09-20` | `WX_LOCAL_DATE_MISMATCH`, no modelo; REJECT. |
| F07 | Contrato `Europe/London` local `2026-10-25`, `[2026-10-24T23:00Z,2026-10-26T00:00Z)`, 25 muestras hourly a 15°C salvo hora incluida `2026-10-25T23:00Z` a 21°C | máximo `21`, 25h exactas, temporal PASS; no truncar a 24 muestras. |
| F08 | Bucket publicado `68°F`, member `20°C`, conversión autorizada exacta sin rounding | `68°F` asignado exactamente una vez; PASS. |
| F09 | Member `18°C`, B0 `T<=18`, B1 `T=19` | asignación B0 una vez, no B1; PASS. |
| F10 | Integer domain con buckets explícitos `18,19,20,21,Other` y member `22` | Other=complement, miembro asignado una sola vez; PASS. |
| F11 | Buckets `[18,20]` y `[20,22]`; valor de prueba `20` | contrato inválido antes del modelo `WX_BUCKET_OVERLAP`; REJECT, no Economics. |
| F12 | Buckets `T<=19` y `T>=21` sin Other; entero `20` | `WX_BUCKET_GAP`, contrato REJECT antes del modelo. |
| F13 | Ensemble base con weight del tercer miembro `-0.1` (variante non-finite rechazada igualmente) | `WX_WEIGHTS_INVALID`; sin normalización/probabilidades/Economics. |
| F14 | Modelo inyecta `P=[0.4,0.4,0.4,0,0]` sum=1.2 | `WX_PROBABILITY_MASS_INVALID`, REJECT, ningún candidate. |
| F15 | Sólo point forecast `20°C`, sin member set ni error calibrado | `WX_DETERMINISTIC_UNCALIBRATED`, `INCONCLUSIVE`, fair_value absent, no ActionCandidate. |
| F16 | Frame `2026-09-19T12:00Z`, rules v2 `known_at=11:50Z`, payload aún v1 | `WX_RULE_VERSION_MISMATCH`; REJECT (no usar versión vieja). |
| F17 | B2 válido, fee `UNRESOLVED` | probabilidades diagnósticas pueden existir; Economics `FeeResolved=false`, assessment `INCONCLUSIVE`, `WX_FEE_UNRESOLVED`, Risk no recibe acción. |
| F18 | B2 BUY size 10, ask book únicamente `0.24×5` | `Sweep.Filled=5`, `Remaining=5`; `WX_DEPTH_INSUFFICIENT`, REJECT, Risk no acción. |
| F19 | B2 `p=.30`, ask `0.29×10`, fee synthetic effective 355bps, size 10 | gross +`0.10` total; fee `0.10295`; net `-0.00295` total, `WX_COSTS_ERASE_EDGE`, REJECT. |
| F20 | Resolution observation publicada `2026-09-21T00:05Z`, inyectada como feature frame `2026-09-20T12:00Z` | `WX_RESOLUTION_LEAKAGE`, REJECT feature; label permitido sólo en evaluación posterior, no cambia Detect. |

**Property tests adicionales:** permutar miembros no altera P; masa exacta y exactly-one; determinismo bytes/manifest/output; serialización estable de IDs/time/decimals; `received_at > frame` jamás aparece en Frame; revisión known_at consistente; duplicate same key/hash idempotente, same key/different hash conflict; mismo replay bajo batch schedules diferentes; labels posteriores aisladas; member set incompleto rechaza sin renormalizar. F03/F11/F12/F16/F17/F18/F19/F20 son gates de seguridad prioritarios. Si un test contradice el engine real, registrar evidencia y resolver contrato antes de alterar expectativa silenciosamente.

### Reproducibilidad, observabilidad y stopping

Manifest mínimo: engine HEAD+branch, Weather schema/model/version/weights, contract/rules hash, fixture ID/source synthetic, forecast reference/availability/received/raw hash/member set, frame cut seq/ts, book capture refs, fee version/kind, model probs/reasons, quote/assessment, risk revision, replay output digest. Métricas: admission accepted/rejected por reason, forecast age, missing members, bucket mass, rule revision mismatch, frames ineligible, incomplete depth/fees, evaluations INCONCLUSIVE, replay mismatch. No secrets ni logs de dumps.

**Stop:** cambios ajenos/worktree conflictivo; contrato que altera payout sin semántica; modificación frozen no autorizada; inexistencia de observación causal dentro del Frame; fee/depth unresolved para señal ejecutable; revisión retroactiva; look-ahead; intento live. Separar error de infraestructura (FAIL) de inconclusión por datos (ABSTAIN). No degradar un blocker a PASS por tests puramente sintéticos.

## Roadmap y work packages (máximo tres fases)

### Fase A — Contratos y modelo puro

**WP-A0 · PRE-FLIGHT / GATE DE AUTORIDAD (sin editar archivos).** Owner: agente desarrollo. Entrada: este planner, repo engine local y policies de ownership; salida: branch, HEAD, status/dirty, diff contra baseline, owners, RS v0.3, interfaces exactas, esquema y registry de reasons, frozen map, datadir/captura activos y **allowed-files manifest por WP**. Read-only comandos de inspección; `git status --short --branch`, `git rev-parse HEAD`, `git log -n 5 --oneline`, búsquedas enfocadas y source real. Determinar si `ExternalObservations` y `DepthQuote` existen ahora y si `screen` sigue neutral-only. PASS `A0_HEAD_VERIFIED` sólo con path+símbolo+commit+owners reales, separación entre lo que funciona offline y los cambios frozen; FAIL con lista exacta de incompatibilidades. No checkout/reset/clean/rebase sobre trabajo de otros. Si A0 confirma seam congelado, A1 puede continuar en scope nuevo permitido, B1 espera autorización específica.

**WP-A1 · DOMAIN CONTRACTS / MODEL.** Owner: domain/strategy agent. Depende A0. Allowed nuevos **propuestos, no autorizados hasta A0**: `internal/strategy/weather/**`, `testdata/strategy/weather/**` o directorios weather equivalentes que permita el ownership real; no editar core ni go.mod/go.sum. Entradas: contrato synthetic + fixtures F01–F16. Outputs: codec/validación pura, interval algebra integer/decimal, vintage causality, ensemble membership, probabilities, typed errors reused, tests offline/props. PASS `A1_OFFLINE_MODEL_PASS`: F01–F16 + properties relevantes, sin red/clock/I/O ni dependencias nuevas, cobertura floor existente y errores explicables. FAIL: cualquier fallback inventado, floating rounding no contractual, member perdido o probabilidad no conservada.

### Fase B — Strategy, Economics, data admission

**WP-B1 · ENGINE STRATEGY + SCREEN.** Owner: strategy/integration. Depende A1 y gate de seam. Allowed condicionales existentes, **lectura solamente hasta autorización/freeze A0**: `internal/strategy/api.go`, `internal/frames/frames.go`, `cmd/engine/screen.go`, `internal/economics/economics.go` (reusar, no reimplementar), ownership real Catalog/Books/Regimes/Risk. Preferir sólo añadir paquete Weather, Factory/registro en composición y adaptación puntual si contrato local ya soporta campos. Si falta external observation o L2 as-of, elevar delta aditivo + rollback/tests a owner de frozen; NO escribir esas rutas sin permiso. Inputs: payload/versioned artifact + Frame cut + L2 as-of fee + contrato; output: Detect candidatos no vinculantes → Economics.BuildQuote → Evaluate → Risk → SCREEN no-live. F17–F19 y tests de veto obligatorios. PASS `B1_SCREEN_PASS` únicamente si Strategy recibe datos por seam causal legítimo, tokens exactos, no HTTP en callbacks y book/fees mismo cut. FAIL ante neutral-only sin integración, BBO usado como L2 o fee inventada.

**WP-B2 · WEATHER ADMISSION FIXTURE-BACKED.** Owner: data/integration. Depende A0/A1; B1 para certificación end-to-end. Allowed condicionales: nuevos archivos exclusivos Weather de adapter/codec en directorio aprobado A0; `internal/capture/**` y `internal/frames/**` READ-ONLY salvo permiso frozen explícito. Input: raw fixture + meta availability/received + version/rules hash; output: ExternalObservation tipada versionada/admitida + Capture común y Frame causal/replay. Tests F03/F16/F20 + duplicates/conflict/revision. PASS `B2_ADMISSION_PASS` si capture y replay preservan exactamente bytes/refs; sin proveedor real, fixtures son suficientes. **Open-Meteo real es otro gate:** B-RULE-01/B-EXEC-01/B-DATA-01/B-LIC-01 PASS; no agregar HTTP provider por anticipación ni requerirlo para offline.

### Fase C — Ejecución no-live, certificación

**WP-C1 · SCREEN → REPLAY → SHADOW.** Owner: experiment/QA. Depende B1/B2 fixture-backed. Allowed condicionales: Weather-specific tests/fixtures y archivos `cmd/engine/**`, `internal/experiment/**`, `internal/replay/**`, `internal/simulator/**` sólo si A0 asigna y owner permite; módulos frozen READ-ONLY por defecto. Nunca usar datadir de captura activa: crear copia descartable con hash/pin y verificar cero mutaciones al original. Probar F01–F20, determinismo dos schedules, manifest hashes, quotes/fee/depth, Risk deny-alls y SHADOW sólo fill virtual. Regresión M4, `go test ./...`, `go vet ./...`, `go test -race ./...` si entorno permite, coverage floor real por paquete tocado sin denominator games, diff/test recibos. PASS `C1_NONLIVE_CERTIFIED` sólo si todas las rutas reales del experimento funcionan: no presentar tests de funciones aisladas como SCREEN/REPLAY/SHADOW ejecutados.

**Critical path:** A0 → A1 → B1 + B2 fixture-backed → C1. Provider real fuera del critical path. Si B1 bloqueado por frozen, entregar A1 completo y gate `ENGINE_CHANGE_BLOCKED` con patch plan, sin fabricar certificación. Sin fechas ficticias ni autorizaciones implícitas.

### Gates y readiness

| Gate | Estado inicial | PASS exige |
|---|---|---|
| G0 market/reference | PASS research, real blocked | referencia y blockers IDs/TZ/rounding explícitos |
| G1 weather sources | PASS research | A resolución ≠ B forecast ≠ C verification documentados |
| G2 temporal design | PASS SPEC only | admission causal validado F03/F20 para código PASS |
| G3 probability design | PASS SPEC only | F02/F13/F14/F15 en código PASS |
| G4 engine compatibility | **PARTIAL/FAIL local** | HEAD local y seam Weather/L2/fee comprobados, frozen authorization si aplica |
| G5 fixtures | 20 SPECIFIED/0 EXECUTED | 20/20 nativas PASS sin red |
| G6 handoff | DOCUMENTED / ALLOWED_FILES_PENDING | A0 paths exactos y SPEC local freeze, mandato sin ambigüedad |
| G7 adversarial | PASS conceptual/offline | tests causales/económicos reales sin contradicción |
| `PE030_IMPLEMENTATION_READY` | **NO aún** | G4 + G6 PASS y núcleo offline integrado/implementable; no confundir con validación OOS |
| `REAL_DATA_READY` | NO | contrato real completo + licence + vintages + Economics real |
| `LIVE_READY` | FORBIDDEN | fuera del scope PE-030 v1 |

## 🧭 Decisiones

- D01 — Sin contrato real admitido; synthetic WX-BASE-V1 es única autoridad de la POC offline; Londres-high EGLC referencia solamente.
- D02 — Cada bracket es binary Market con YES/NO tokens; identity nunca inferida de UI.
- D03 — Buckets exactly-one en published payout domain; unknown rounding/TZ/source/fallback fail closed.
- D04 — Uniform ensemble counts como assumption `UNCALIBRATED`, no Gaussian ni calibración inventada.
- D05 — Forecast point-only diagnóstico sin fair value/candidate; faltantes no se renormalizan.
- D06 — Point-in-time `availability <= received <= frame`; jamás backfill histórico pseudo-vintage.
- D07 — Reusar Foundation decimal, Economics depth/fees, Capture/Frame, Simulator/Risk; no nueva librería ni servicio por defecto.
- D08 — No nearest-station adjustment ni grid→EGLC corrección sin OOS; calidad `UNCALIBRATED_SPATIAL` para prospectivo.
- D09 — El remoto `9ae5dde` tiene un gap comprobado de transporte Weather y SCREEN neutral-only; A0 decide contra HEAD local, no autoriza cambio frozen.
- D10 — SCREEN/REPLAY/SHADOW exclusivamente no-live, dataset aislado; ningún resultado sintético significa alpha.

## 📆 Bitácora

- **2026-09-20 — Preparación documental:** integrado Deep Research del owner, verificados `POC-S04` libre y `POC-S05` vecino, fuente del engine remoto `9ae5dde` y seam faltante `ExternalObservations`/L2/SCREEN; SPEC offline y 20 escenarios cerrados, 5 WPs y mandato embebidos. No se ejecutó motor ni test, ni se modificó el engine. Pendientes reales: inspección HEAD local A0, autorización frozen si procede, lint/Graphify local y puente en padre (no editar padre en esta sesión por aislamiento). No se cierra sesión AGENTS OS.

## 🔗 Docs / Links y evidence registry

- Autoridad padre: [[Polymarket Engine — MVP]]. Hipótesis canónica: [[Polymarket — Edge Research Consolidado 2026-09-16]]. Plataforma: [[Polymarket — Technical Platform Map — synced 2026-09-17]]. `main/80-agents/agents-os/agents-os.md` (bootstrap canónico en `main/80-agents/skills/agents-os-bootstrap/SKILL.md`).
- Evidencia engine SHA: https://github.com/xKoRx/polymarket-engine/commit/9ae5ddec1a0e52fdc0bbde608cd0504e644d05a5 ; source: `internal/strategy/api.go`, `internal/frames/frames.go`, `cmd/engine/screen.go`, `internal/economics/economics.go` en dicho SHA. HEAD local posterior DESCONOCIDO.
- Polymarket Londres-high real (REFERENCE ONLY): https://polymarket.com/event/highest-temperature-in-london-on-september-20-2026 ; Londres-low: https://polymarket.com/event/lowest-temperature-in-london-on-september-20-2026 ; Helsinki-high: https://polymarket.com/event/highest-temperature-in-helsinki-on-september-20-2026 ; Shanghai-high: https://polymarket.com/event/highest-temperature-in-shanghai-on-september-20-2026 .
- Mercado Event/Markets: https://docs.polymarket.com/concepts/markets-events ; discovery Gamma: https://docs.polymarket.com/market-data/discover-markets ; books: https://docs.polymarket.com/market-data/prices-order-books ; fees: https://docs.polymarket.com/trading/fees .
- NOAA resolución EGLC: https://www.weather.gov/wrh/timeseries?site=eglc ; ensemble: https://open-meteo.com/en/docs/ensemble-api ; availability: https://open-meteo.com/en/docs/model-updates ; single-runs: https://open-meteo.com/en/docs/single-runs-api ; licensing/pricing: https://open-meteo.com/en/pricing .
- Evidence IDs del research aportado: `E-PM-LON-H`, `E-PM-MODEL`, `E-PM-CATALOG`, `E-PM-BOOK`, `E-PM-FEE`, `E-NOAA-EGLC`, `E-OM-ENS`, `E-OM-AVAIL`, `E-OM-RUN`, `E-OM-TERMS`, `E-ENG-01/02`. Sus conclusiones están delimitadas arriba, **no reutilizar marcadores de citas temporales de ChatGPT como fuente persistente**.

## 💡 Ideas

- Post-POC: captura prospectiva por estación/horizonte, label market settlement con revisión conocida, estudio Brier/log-loss y station-grid bias. NO abrir ML pesado, proveedor comercial, nuevos microservicios ni LIVE en v1.

---

# MANDATO DE IMPLEMENTACIÓN — PE-030

**Ejecuta este mandato al retomar el proyecto. No reabrir research meteorológico ni editar otro planner.** Fuente única: esta nota `[[POC-S04 — Weather]]`, padre sólo lectura, Deep Research destilado aquí. Repositorios: `xKoRx/agents-os` para planner y `xKoRx/polymarket-engine` para desarrollo. Baseline remoto comprobado `9ae5ddec1a0e52fdc0bbde608cd0504e644d05a5`; baseline histórico `7bd264d` NO vigente; HEAD local y RS v0.3 requieren gate A0. Prohibido producción/live, órdenes, secretos, paid API, recorder Weather, I/O/clock en callbacks, duplicar Economics, backfill que filtre futuro, operar sobre captura activa o tocar otros POCs.

**Orden irrevocable:** (1) bootstrap mínimo Agents-OS y leer estado/tareas de esta nota; (2) A0 read-only y registrar SHA/status/branch/owners/symbols/allowed-files y compat delta; (3) comprobar si local ya trae ExternalObservation→Frame→Strategy y L2/fee as-of: si no, diseñar cambio aditivo mínimo pero **no escribir frozen sin aprobación**; (4) con A0 aceptado implementar A1 puro + F01–F16 offline; (5) B1/B2 con seam autorizado, F17–F20, mismos data refs en SCREEN; (6) C1 REPLAY/SHADOW en dataset descartable y certificar; (7) actualizar tareas/bitácora/progress por evidencia y presentar a owner en Review sin cerrar tarea puente.

**Allowed files:** NO existe permiso global. A0 debe registrar manifest exacto por WP dentro de esta nota; candidatos exclusivamente `internal/strategy/weather/**` y Weather-specific testdata nuevos; adiciones puntuales en `cmd/engine/**`/adapter sólo tras resolver ownership; `internal/strategy/api.go`, `internal/frames/**`, `internal/capture/**`, `internal/economics/**`, `internal/replay/**` son READ-ONLY por defecto y se vuelven editables sólo bajo autorización owner/policy registrada. Nunca modificar parent Agents-OS, POC-S05/Sports, `sync.sh`, `.sync`, data-dir activo ni módulos frozen no autorizados. Revisar HEAD y diff antes de cada continuación, no pisar agentes concurrentes.

**Evidencia exigida:** paths+symbols+SHA A0; contratos y F01–F20 input/expected real en tests nativos; `go test`/vet/race/coverage y regresión; hashes de dataset/frames/model/rules/forecast/book/fees/manifest; outputs SCREEN/REPLAY/SHADOW correlacionables; pruebas específicas anti-lookahead, bucket overlap/gap, missing member, fees/depth y neutralización de edge. No presentar fixture synthetic como mercado real ni inferir alpha con tests. Gate final `PE030_IMPLEMENTATION_READY` sólo cuando source local, seams, allowed files, SPEC y tests pertinentes estén verificados; `REAL_DATA_BLOCKED` queda hasta contrato real y proveedor autorizado; `LIVE_READY=FORBIDDEN`.

**Primera acción sin preguntas al owner:** ejecutar `WP-A0` read-only, registrar compatibilidad exacta y allowed files; luego comenzar A1 sólo si gate pasa. Escalar exclusivamente una decisión material sobre modificación frozen/licencia/pago si es inevitable. En caso de bloqueo no saltarlo: entregar núcleo A1 y recibo `ENGINE_CHANGE_BLOCKED`, con archivos, símbolos, menor cambio propuesto, pruebas y autorización requerida. Jamás afirmar que SCREEN/REPLAY/SHADOW pasó si no se ejecutó.

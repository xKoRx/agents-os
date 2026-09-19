---
type: agent_run
schema_version: 1
scope: session
created: "2026-09-19"
updated: "2026-09-19"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
entities:
  - "[[Polymarket Engine]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash (zai-individual-coding-plan/GLM-5.3-Flash)
model_source: host
task_type: coding
task_complexity: high
outcome: success
verification: run
evaluator: agent
user_rework: unknown
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — 2026-09-19-zcode-glm-research-strategies-v01

## Trabajo

- **Objetivo:** mandato RESEARCH STRATEGIES v0.1 — implementar dos estrategias experimentales (POC-S01 NegRisk complete-set, POC-S02 Sports pre-match reversion) sobre el engine certificado `9ae5dde`, ejecutar SCREEN/REPLAY/SHADOW y producir scorecards para decidir qué hipótesis merece investigación posterior. Branch `feature/research-strategies-v01`, sin push, LIVE_DISABLED.
- **Fase A (`7eb3532`):** screen runner extraído a pipeline compartido (`screenPipeline`: journal+store+books replay+dispatcher con owners por asset); registro de factories reemplazando el hardcode del fixture; comando `screen-consolidated` (mismo frame, copias inmutables, a N instancias aisladas; manifest consolidado que cuenta decisiones por instancia sin sumar PnL ni dedupear oportunidades entre estrategias); specs frozen de ambas POCs en la nota canónica; gate A con dos instancias distinguibles e aisladas, determinismo y equivalencia instancia≡run-solo.
- **Fase B (`9d737ae`):** `internal/strategy/pocs/pocdata` (codec top-N asks/bids para `AssetSnapshot.Extras` con frescura anclada al source ms del book — profundidad que un delta movió es detectable como stale, jamás usada en silencio); `internal/strategy/pocs/negrisk` (PE-002: elegibilidad exige membership/exhaustiveness VERIFIED, sin Other mutable, protocol CTF|V2 y fee POINT/INTERVAL/UNRESOLVED-declarada; detección preliminar por best asks; evaluación con sweep+fee por leg vía `economics.BuildQuote` sobre profundidad observada, edge por conjunto, `CONDITIONAL_UNEXECUTABLE` en todo ACCEPT); `internal/strategy/pocs/sports` (PE-005-R1: referencia = mediana de los spreads previos propios — el frame actual jamás entra a su propia referencia; kickoff verificable obligatorio o señales bloqueadas; taker-only v0.1, maker rechazado UNCALIBRATED en factory; entrada = sweep sobre ask depth observada, gate económico = reversion al nivel de referencia (mediana de mids) paga el round trip; breakeven bid B* por candado de fees al bound superior; medición reverted/not_reverted/window_open contra B* dentro de la ventana); wiring: routing incremental de records entre cuts (frames = cortes forward de la grabación; corre un defecto estructural: antes todos los frames veían el estado final), filtrado del carril RUNTIME en la carga del journal, factories registradas, gate G-15b extendido a los tres paquetes nuevos; ramas defensivas demostrablemente inalcanzables eliminadas por política del owner (dos casos: Remaining>0 tras sizing acotado por depth; división por size>0), con Sub/Div/Mul reales de frontera exacta cubiertos por tests de inputs extremos (4096 dígitos).
- **Fase C (`0d6a635`):** `RunShadow` con selección de factory por `manifest.StrategyID` (neutral default preservado) y routing incremental entre cuts; `fillCandidate`: candidatos acotados llenan por leg desde profundidad OBSERVADA vía `simulator.FillAt` en el ledger virtual y las canastas multi-leg pasan por la máquina SEQUENTIAL frozen (`PlanBasket`/`TransitionBasket`: PLANNED→RESERVED→EXECUTING→COMPLETED, o →BLOCKED_UNKNOWN→ABANDONING→RESIDUAL_HELD con rechazos); scorecard extendido con métricas por estrategia y contabilidad de canastas (aditivo; la paridad del fixture neutral intacta); evidencia `testdata/experiment/evidence/rs_v01_shadow.json` (emit/re-check): ambas POCs shadow E2E sobre un mismo journal sellado con fills, paridad de hash de scorecard en journals frescos, outcomes INCONCLUSIVE honestos; CLI `experiment shadow --param k=v` repetible.
- **Datos reales (read-only):** `catalog sync --kind events --max-pages 2` contra Gamma (397 entidades, 3 cuarentenas, `page_budget_exhausted` esperado); evento NegRisk 30829 `democratic-presidential-nominee-2028` pineado por GET directo (128 mercados negRisk=true, negRiskOther=false); `record` 45 s del WS de 6 tokens YES (57–224 niveles reales por asset); SCREEN consolidado y SHADOW reales ejecutados → honestamente **0 candidatos**: los constraints de régimen de esos mercados quedan fuera del techo Gamma offset≤2000 (brecha documentada) y la exhaustividad del evento no es verificable hoy; `DATA_BLOCKED` con causa exacta en `testdata/research-v01/EVIDENCE.md` + outputs commiteados. REPLAY del journal real desde un manifest: digest de observación idéntico `5a5bb186…` en schedules batch y 1.
- **No implementado a propósito:** capacidades nuevas de protocolo (sync por ids, keyset), consumo directo del catálogo por las estrategias (canal v0.1 = params versionados con provenance de `catalog inspect`), maker queue, conversión NegRisk, órdenes.

## Verificación

- Regresión completa en cada checkpoint: `go build ./...`, `go vet ./...`, `go test ./...` (26→30 paquetes, 0 fallos), `go test -race` en paquetes tocados, `go mod tidy` sin diff, `git diff --check` limpio.
- Cobertura piso Agents-OS ≥95% por paquete (denominador tests-propios, atomic): negrisk 95.0, pocdata 95.7, sports 95.4, cmd/engine 95.0; resto sin regresión.
- Certificación física del SHA final: `engine experiment certify --repo-root . --baseline 0d6a63583d6ef105985544e9d6f9ae04e15e64b9` → `M4_CERTIFIED_NON_LIVE`, 27 PASS / 0 FAIL / 0 in-scope NOT_RUN / 5 diferidos live; un pin mal formado en una corrida previa devolvió correctamente `M4_STALE_CERTIFICATION` (matriz negativa del harness re-verificada de facto).

## Rework

- Re-trabajos intra-sesión: gramática del spec `--run` movida de coma a `;` (colisión con listas de assets); expectativas de tests corregidas cuando el modelo económico inicial resultó no-falsable (salida taker-taker a mid constante imposible → re-modelado al nivel de referencia medible); breakeven en forma bps eliminado como matemáticamente muerto para libros no cruzados (queda el bid de breakeven, que es lo que mide la reversión). Sin rework del owner.

## Estado

- Gates `RS-V01-A_PASS`, `RS-V01-B_PASS`, `RS-V01-C_PASS`; resultado global `RS_V01_PARTIAL_DATA` (datos reales aptos pendientes). Nota de identidad: mapeo canónico conservado S01=NegRisk / S02=Sports; tesis sports v0.1 registrada como revisión PE-005-R1, PE-001 permanece para iteración posterior.

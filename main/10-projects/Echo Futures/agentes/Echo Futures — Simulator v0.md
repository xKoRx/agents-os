---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo Futures]]"
sprint: 2026-09-24
start: 2026-09-24
due: 2026-09-24
progress: 100
repo: "xKoRx/echo-futures"
jira:
prs:
aliases:
  - Echo Futures Simulator v0
tags:
  - kind/project
  - area/echo
  - echo-futures
  - simulator-v0
created: "2026-09-24"
updated: "2026-09-24"
---

# Echo Futures — Simulator v0

## 🎯 Objetivo

- Implementar y certificar hoy el simulador estocástico v0 de Echo Futures bajo la matemática `MATH_GO`, sin datos históricos ni reglas reales de props.
- Entregar un CLI Go reproducible que pase T1–T8, permita escenarios null/synthetic-edge y simule lifecycle abstracto hasta FIRST_PAYOUT.

## 📊 Estado actual

- **G4C_REVIEW / SHOT 3 COMPLETO.** Commit de certificación `d4f42a41946f12231b75e4eb65b90d132731be0d` sobre `ad7fe60`: SF2-01 y SF2-02 corregidos, SF2-05 resuelto vía validación CLI, SF2-03/04 documentados, arnés de auditoría Shot 2 adoptado como tests permanentes. Sólo el owner puede aceptar G4C.
- **Evidencia Shot 3 (2026-09-24, HEAD `d4f42a4`):**
  - `go fmt` limpio · `go vet` limpio · `go test ./...` PASS · `go test -race ./...` PASS · coverage `internal/sim` **96.1%**.
  - `sim validate --runs 1000000 --seed 42`: **47/47 PASS**; dos corridas JSON 1M byte-identical (sha256 `c703a37d…`).
  - SF2-01: `stubRng` stateful con pointer receiver (`internal/sim/validation.go`); regresiones `TestStubRngStatefulMultiValue` ([0.2, 0.9] → 0.2 luego 0.9) y `TestStubRngMultiValueForcedLifecyclePath` (path forzado PASS_THEN_FAIL cash −160).
  - SF2-02: `pFundedGivenPass = 0` cuando `passes = 0` (`internal/sim/lifecycle.go`); regresiones `TestZeroPassPundedGivenPassIsZero` y `TestCLIZeroPassLifecycleJSON` (runs=1 seed=1 → exit 0, JSON válido sin NaN).
  - SF2-05: `validateSeed` rechaza seed > MaxInt64 con error preciso en validate/simulate/cohort (flag y scenario JSON); frontera MaxInt64 aceptada; límite documentado en README.
  - SF2-03: re-arm del edge por trade documentado (README + comentario contractual en `internal/sim/trade.go`) y protegido por `TestAuditSyntheticEdgeSemantics` (sin fuga a trade 2; re-arm sólo con escalera propia).
  - SF2-04: limitación del epsilon de empates documentada en README (frontera medida ~1e-7 absoluto a escala 100; prioridad congelada phase > trade > add intacta).
  - Arnés Shot 2 adoptado en `internal/sim/audit_shot2_test.go` (trackeado): 11/11 PASS (T2/T3/T8 exactos con DP independiente, T6 cash identities, event priority/epsilon, edge semantics, cohort identities, matriz de config, propiedades self-financing/kernel/optional-stopping).
  - Samples idénticos a Shot 1 (sin cambio estadístico material): t2 1M seed 42 pWin 0.499499 / reach 0.769441 / cond 0.349526; lifecycle 200k pPass 0.401025 / pFundedGivenPass 0.2487 / q 0.099735 / meanCash 19.5512; cohort 100k meanAttempts 10.0093 / P50 7 / P95 29 / payoutWithin10 0.65234.
- Matemática cerrada en [[echo-futures-astra-math-review]].
- Funcional congelado en [[D4 — Simulator v0 Functional SPEC]].
- Técnico congelado en [[D4 — Simulator v0 Technical SPEC]].
- **Evidencia Shot 1 (2026-09-24):**
  - Repo local aislado: `~/aranea/work/echo-futures-simulator-v0-20260924/echo-futures`, branch `master`, HEAD `ad7fe609c8b6503cdc7b803d5c33d8eb3efdcff9`, Go 1.27.1 linux/amd64, módulo `github.com/xKoRx/echo-futures`, sin dependencias externas, sin remote.
  - `go test ./...` PASS · `go test -race ./...` PASS · coverage `internal/sim` **96.0%** (core nuevo; total 95.9%).
  - `sim validate --runs 1000000 --seed 42`: **47/47 PASS** (T1–T8 + invariantes) en ~6.5 s; dos corridas byte-identical (JSON).
  - Sample `simulate` (t2, 1M): pWin 0.4995, pReachAdd 0.7694 (10/13), pWinGivenAdd 0.3495. Sample `simulate` lifecycle (200k): pPass 0.401, pFundedGivenPass 0.2487, q 0.0997, meanCash 19.55. Sample `cohort` (100k): meanAttempts 10.009, meanFailures 9.009, P50=7, P95=29, payoutWithin10 0.6523.
  - Limitations documentadas en README (null driftless sin costes/slippage, barreras estáticas, edge one-shot, cohort IID, float64, sólo first payout).
- **Evidencia Shot 2 (2026-09-24, auditoría independiente @ ad7fe60):**
  - Reproducción: `go test ./...` PASS, `go test -race ./...` PASS, coverage 96.0% `internal/sim`, `validate` 1M seed 42 → 47/47 PASS y **byte-idéntico** (texto diff vacío, JSON `cmp` idéntico) en dos corridas; `go vet` limpio.
  - Checks independientes con DP exacto de primer paso escrito desde cero (sin código del engine): T2 total 1/2, condicional 35/100, reach 10/13; T3 total 1/2, post-add1 0.4, post-add2 1/5, barreras 40/3 y −160/3, reach escalera completa 5/8, AddsUsed=2; T8 total 15/26, condicional 0.45, E[X]=200/13, reach invariante 10/13; todos contra MC 200k dentro de 5σ.
  - Lifecycle: identidad por buckets `meanCash == (failEval·(−110) + passThenFail·(−160) + payouts·1340)/runs` exacta; ledgers forzados −110/−160/+1340; activación cobrada al PASAR; J≤I.
  - Cohort: `meanFailures == meanAttempts − payoutFraction` exacto; identidad `meanCash = meanAttempts·(−(F+C)) + meanActivations·(−A) + payoutFraction·W` exacta; censura al cap correcta; payoutWithin sobre todos los cohortes; ledger enumerado 3 intentos (cash 1070).
  - Event priority: empates exactos fase>trade>add verificados; frontera epsilon medida (0.5×tol → fase, 2×tol → trade; ~1e-7 absoluto a escala 100).
  - Synthetic edge: armado sólo tras último add ejecutado (add inalcanzable + delta=1.0 corre limpio y byte-igual a null); delta=0 mismo consumo RNG; pEff fuera de [0,1] hard-error en ambos signos sin clipping; sin fuga entre trades; re-arm por trade documentado.
  - Config: matriz 50+ casos NaN/Inf/órdenes/deltas/caps/JSON estricto → todo fail-closed.
  - Property tests: self-financing aleatorio 5000/5000, kernel bounds 10k/10k, optional stopping con 3 escaleras aleatorias ×100k (pWin 0.5, E[X] 0) — PASS.
  - Arnés de auditoría: `internal/sim/audit_shot2_test.go` (UNTRACKED, sha256 prefijo 63fbfaa19d249c2e; 11/11 tests PASS; no toca código congelado; candidata a adopción en Shot 3 o descarte).
- Echo, Echo Forge, NinjaTrader y market data están fuera de scope. No se tocó ningún otro repo.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo-futures (local, sin remote) | master | empty/new repo | [[D4 — Simulator v0 Functional SPEC]] | [[D4 — Simulator v0 Technical SPEC]] | G4C_REVIEW @ d4f42a4 |

## Matriz requirement → evidence

| Requirement | Estado | Evidencia |
|---|---|---|
| Matemática first-passage/optional stopping | done | [[echo-futures-astra-math-review]] MATH_GO |
| Behavior v0 | done | [[D4 — Simulator v0 Functional SPEC]] |
| Technical contract v0 | done | [[D4 — Simulator v0 Technical SPEC]] |
| Repo code | done | `echo-futures` @ master ad7fe60 (kernel/trade/lifecycle/cohort/CLI + README + scenarios) |
| Independent audit | done | Shot 2 @ ad7fe60: sin blockers/majors; findings SF2-01/02 (MINOR) y SF2-03/04/05 (INFO); G4B accepted |
| Corrections/certification | done | Shot 3 @ d4f42a4: fixes SF2-01/02 + SF2-05 validado + SF2-03/04 documentados + arnés adoptado; gate completo verde; G4C review |

## Decisiones

| ID | status | resolution | source/evidence | phase consuming it |
|---|---|---|---|---|
| D4-01 | TECHNICAL_RESOLUTION | Go, standard library first, event-driven exact hitting kernel | Technical SPEC | Shot 1 |
| D4-02 | CONFIRMED | Simulation-first; no historical market data in v0 | [[Echo Futures]] | Shot 1 |
| D4-03 | TECHNICAL_RESOLUTION | LONG-only normalized process; short symmetry deferred | Technical SPEC | Shot 1 |
| D4-04 | TECHNICAL_RESOLUTION | Synthetic delta once after last executed adverse add | Astra review + Technical SPEC | Shot 1 |
| D4-05 | TECHNICAL_RESOLUTION | Single-threaded deterministic RNG in Shot 1 | Technical SPEC | Shot 1 |
| D4-06 | CONFIRMED | No real prop rules before null/synthetic engine certification | [[Echo Futures]] | Shots 1–3 |
| D4-07 | CONFIRMED | Synthetic edge v0 se rearma por trade cuando ese trade ejecuta el último adverse add; no existe edge once-per-attempt | Owner acceptance after Shot 2 + SPEC §8/§9 | Shot 3 / D5 handoff |
| D4-08 | CONFIRMED | Shot 3 corrige SF2-01 y SF2-02; SF2-03/04/05 se documentan sin rediseño | Owner acceptance after Shot 2 | Shot 3 |

## Gate control

| Gate | current state | phase agent responsibility | owner acceptance evidence | enables |
|---|---|---|---|---|
| G4A — Implementation | **accepted** (owner dispatch Shot 2, 2026-09-24) | implement, run all tests, move to review | T1–T8 + invariants + coverage + commit | Shot 2 |
| G4B — Independent audit | **accepted** (owner, 2026-09-24) | adversarially review code/results, move to review | findings SF2-01..05 + reproducción + arnés 11/11 | Shot 3 |
| G4C — Certified v0 | **review** (agent, 2026-09-24 @ d4f42a4) | fix only accepted findings, rerun evidence, move to review | clean T1–T8 + audit closure | D5 |

## Roadmap / phase packages

### Paquete autónomo Fase 1 — Shot 1: implementar simulator v0

**Misión exacta**

Implementar desde cero el repo/módulo Go del simulator v0 congelado, sin expandir scope.

**Precondiciones verificables**

- [[echo-futures-astra-math-review]] = MATH_GO.
- Functional SPEC y Technical SPEC = approved-for-implementation.
- G4A = pending.

**Lectura obligatoria**

- [[D4 — Simulator v0 Functional SPEC]].
- [[D4 — Simulator v0 Technical SPEC]].
- [[echo-futures-astra-math-review]].
- Esta nota: Estado actual, Decisiones, Gate control y este paquete.

**Decisiones cerradas**

- Go.
- exact first-passage kernel; no tick simulation.
- standard library first.
- repo nuevo aislado.
- T1–T8 son authority.
- no real prop rules.

**Implementación paso a paso**

1. Verificar que no exista un checkout/repo local conflictivo con `echo-futures`; registrar baseline.
2. Crear/usar repo local aislado y módulo `github.com/xKoRx/echo-futures`.
3. Implementar types/config validation.
4. Implementar exact hitting kernel.
5. Implementar self-financing position/add accounting.
6. Implementar trade event loop y phase barriers.
7. Implementar evaluation→funded→first-payout lifecycle/economics.
8. Implementar cohort IID.
9. Implementar CLI validate/simulate/cohort + JSON/text.
10. Implementar T1–T8 + deterministic invariants.
11. Ejecutar tests/race/coverage/1M validation.
12. Documentar comandos, limitations, evidence y commit.
13. Actualizar esta nota: tareas, estado, bitácora; dejar G4A en `review`.

**Archivos esperados**

- create: repo Go según Technical SPEC.
- modify: esta nota sólo para estado/evidencia.
- modify parent: sólo tarea puente de `[ ]`/`[/]` a `[r]` al entregar.

**No tocar**

- xKoRx/echo, Echo Forge, NinjaTrader.
- otras specs/proyectos.
- rules reales de props.
- infra/PROD/secrets.

**Spikes permitidos**

- sólo verificar versión Go y ausencia/presencia de repo local.
- cualquier otra incertidumbre = PLAN_CONFLICT.

**Tests y asserts**

- T1–T8 exactos.
- invariantes técnicos de Technical SPEC.
- go test ./...
- go test -race ./...
- >=95% coverage core.
- validate 1M seed 42.

**Entregables/Gate G4A**

- repo/path/branch/HEAD/go version;
- test/race/coverage;
- T1–T8 output;
- sample simulate/cohort;
- known limitations;
- commit SHA;
- G4A -> review.

**Handoff a Fase 2**

Shot 2 recibe commit inmutable + outputs; no redescubre matemática ni agrega features.

### Paquete autónomo Fase 2 — Shot 2: auditoría independiente

**Misión exacta**

Intentar falsificar la implementación de Shot 1 sin agregar features.

**Precondiciones verificables**

- G4A review y commit concreto.

**Lectura obligatoria**

- mismas tres autoridades + evidencia Shot 1.

**Decisiones cerradas**

- no cambiar mathematics/spec para hacer pasar tests.

**Implementación paso a paso**

1. Reproducir build/tests/validate.
2. Revisar kernel, event ordering, self-financing, lifecycle/economics, RNG.
3. Crear tests adversariales sólo cuando prueben un invariant congelado.
4. Reportar findings con severity y repro.
5. G4B -> review; no corregir salvo error trivial que impida ejecutar la auditoría.

**Archivos esperados**

- tests de auditoría si aportan evidencia; nota actualizada.

**No tocar**

- scope/feature expansion.

**Spikes permitidos**

- ninguno.

**Tests y asserts**

- reproducir T1–T8 y buscar counterexamples en boundaries.

**Entregables/Gate G4B**

- PASS o findings reproducibles.

**Handoff a Fase 3**

- lista cerrada de findings aceptables para corrección.

### Paquete autónomo Fase 3 — Shot 3: corrección y certificación

**Misión exacta**

Corregir únicamente findings válidos de Shot 2 y certificar v0.

**Precondiciones verificables**

- G4B review.

**Lectura obligatoria**

- authorities + findings Shot 2.

**Decisiones cerradas**

- no feature work.

**Implementación paso a paso**

1. Clasificar findings.
2. Corregir blockers/major válidos.
3. Rerun all evidence.
4. Dejar G4C review.

**Archivos esperados**

- sólo fixes/tests/docs necesarios.

**No tocar**

- D5/props reales.

**Spikes permitidos**

- ninguno.

**Tests y asserts**

- full Shot 1 gate + regression tests.

**Entregables/Gate G4C**

- certified commit + clean evidence.

**Handoff a Fase N+1**

- D5 recibe simulator v0 certificado; no reabre matemática.

## ✅ Tareas

> - [x] T1.1 verificar baseline/repo local y toolchain #owner/agent #type/dev #area/echo
> - [x] T1.2 implementar kernel + model + validation #owner/agent #type/dev #area/echo
> - [x] T1.3 implementar trade/recovery event loop #owner/agent #type/dev #area/echo
> - [x] T1.4 implementar lifecycle/economics/cohort #owner/agent #type/dev #area/echo
> - [x] T1.5 implementar CLI/scenarios #owner/agent #type/dev #area/echo
> - [x] T1.6 implementar T1–T8 + invariants #owner/agent #type/dev #area/echo
> - [x] T1.7 ejecutar test/race/coverage/1M validation y commit #owner/agent #type/dev #area/echo
> - [x] T1.8 dejar G4A review + handoff #owner/agent #type/dev #area/echo
> - [x] T2.1 auditoría independiente Shot 2 #owner/agent #type/pr-review #area/echo
> - [x] T3.1 corrección/certificación Shot 3 #owner/agent #type/dev #area/echo

## 📆 Bitácora

- **2026-09-24** — Proyecto de agente materializado para ejecución D4. Math/functional/technical contracts frozen. READY_FOR_SHOT_1; no código ejecutado todavía.
- **2026-09-24** — SHOT 1 iniciado (T1.1 WIP). Autoridades leídas en orden (math review, functional, técnico, proyecto padre); sin contradicciones detectadas. Baseline: Go 1.27.1 linux/amd64; no existe checkout local previo de `echo-futures` (sin conflicto); repo nuevo aislado en workspace externo `~/aranea/work/echo-futures-simulator-v0-20260924/echo-futures`, módulo `github.com/xKoRx/echo-futures`, branch `master`. Tarea puente del padre movida a WIP.
- **2026-09-24** — SHOT 1 COMPLETO, **G4A → review**. Commit `ad7fe609c8b6503cdc7b803d5c33d8eb3efdcff9` (21 archivos, árbol limpio, sin remote/push). Gates: `go test ./...` PASS; `go test -race ./...` PASS; coverage `internal/sim` 96.0%; `sim validate --runs 1000000 --seed 42` 47/47 PASS (~6.5 s) y reproducible byte-identical. Samples: simulate t2 1M (pWin 0.4995 / reach 0.7694 / cond 0.3495), simulate lifecycle 200k (pPass 0.401, q 0.0997), cohort 100k (meanAttempts 10.009, P50 7, P95 29). Nota de corrección durante el shot: el .gitignore inicial (`sim` sin anclar) había excluido `cmd/sim` e `internal/sim` del primer commit; detectado y corregido vía amend del commit raíz (repo nuevo, sin remote). Sin desviaciones de SPEC; el único caso ambiguo resuelto fue clasificar salidas de barrera por dirección del evento + equidad alcanzada con epsilon relativo (empates → fase, según prioridad congelada). Shot 2 (auditoría) queda BLOQUEADO hasta aceptación owner de G4A.
- **2026-09-24** — SHOT 2 COMPLETO (T2.1 DONE), **G4B → review**. G4A aceptado por owner vía despacho; commit auditado `ad7fe60` (árbol congelado, único delta = arnés de auditoría untracked). Reproducción completa: tests/race/coverage 96.0%/validate 1M byte-idéntico. Falsificación fallida: DP independiente de primer paso reproduce T2/T3/T8 al 1e-12, identidad de cash por buckets exacta, empates y epsilon verificados, edge semántica correcta (sin arming en add inalcanzable, sin fuga entre trades, delta=0 byte-null), cohort con identidades exactas y censura correcta, config 100% fail-closed, optional stopping con escaleras aleatorias verde. Findings: **SF2-01 MINOR** `stubRng` con receptor por valor no avanza por la interfaz `randomSource` (scripts multi-valor repiten `values[0]`; hoy invisible porque todos los usos existentes pasan un solo valor; trampa latente para tests futuros); **SF2-02 MINOR** `PFundedGivenPass = 0/0 = NaN` con 0 passes (texto imprime NaN exit 0; JSON falla con mensaje opaco; repro `--runs 1 --seed 1`); **SF2-03 INFO** re-arm del edge es por trade (consistente con SPEC §8.11+§9, documentar en certificación); **SF2-04 INFO** epsilon de empates clasifica diferencias <1e-9 relativo como tie (degenerado, money ≤ tol); **SF2-05 INFO** wrap uint64→int64 en seeds ≥2^63. qBE 0.0866726 explicado: fórmula analítica con `pPass` Monte Carlo observado del stream 6 (0.400177), delta-tolerance correcta → aceptable. Veredicto: **PASS_FOR_SHOT_3**; no se corrigió ningún finding (fuera de scope del shot).
- **2026-09-24** — **G4B ACCEPTED por owner.** Shot 3 desbloqueado. Correcciones obligatorias: SF2-01 (`stubRng` multi-value) y SF2-02 (`pFundedGivenPass` con 0 passes). SF2-03 queda congelado como comportamiento intencional: synthetic edge se rearma por trade después de ejecutar el último adverse add. SF2-04/05 se documentan; no requieren cambio de engine.
- **2026-09-24** — SHOT 3 COMPLETO (T3.1 DONE), **G4C → review**. Commit de certificación `d4f42a41946f12231b75e4eb65b90d132731be0d` sobre `ad7fe60` (11 archivos, +897/−15, árbol limpio, sin remote/push). Gate de entrada verificado (G4A/G4B accepted, delta permitido = sólo el arnés untracked). Cierre de findings: **SF2-01** `stubRng` convertido a stateful con pointer receiver + 10 call sites a `&stubRng{}` (el arnés usa su propio auditRng y no cambió); regresiones [0.2, 0.9] en orden y path forzado PASS_THEN_FAIL. **SF2-02** guard `passes == 0 ⇒ pFundedGivenPass = 0` con semántica congelada (el count `passes` conserva la info del denominador); repro runs=1/seed=1 verificado: exit 0, JSON válido, sin NaN. **SF2-05** `validateSeed` en los 3 comandos CLI (flag y scenario JSON): seed > MaxInt64 rechazado con error preciso, frontera MaxInt64 aceptada; sin cambio de firma de librería. **SF2-03/04** documentados (README + comentario en trade.go). Arnés Shot 2 adoptado trackeado (header actualizado a evidencia permanente, import json eliminado; 11/11 PASS). Calidad: fmt/vet limpios, test PASS, race PASS, coverage internal/sim 96.1%, validate 1M seed 42 47/47 PASS, dos JSON 1M byte-identical (sha256 c703a37d…). Samples vs Shot 1: sin cambio estadístico material (t2 pWin 0.499499/reach 0.769441/cond 0.349526; lifecycle pPass 0.401025/pFunded 0.2487/q 0.099735/meanCash 19.5512; cohort meanAttempts 10.0093/P50 7/P95 29/payoutWithin10 0.65234). Limitaciones residuales: funciones de librería aceptan uint64 (el bound MaxInt64 se aplica en el CLI, superficie v0; documentado); epsilon de empates relativo sin aritmética exacta. G4C queda en review — sólo el owner certifica.

## 🔗 Docs / Links

- [[Echo Futures]]
- [[D4 — Simulator v0 Functional SPEC]]
- [[D4 — Simulator v0 Technical SPEC]]
- [[echo-futures-astra-math-review]]

## Common executor rules

- Evidence order: executable tests/code > frozen specs > project note.
- Never invent or soften a formula to make a test pass.
- Preserve unrelated local work.
- No destructive git cleanup.
- No web/MCP research unless required only to operate the local repo; do not research product semantics.
- On contradiction with frozen math/spec: PLAN_CONFLICT and stop.
- Update this agent project continuously; it is the durable planner.
- Never accept your own gate; maximum state is `review`.

## Dispatch blocks

### SHOT_1

FASE_ASIGNADA=1
PAQUETE_CANONICO=Paquete autónomo Fase 1 — Shot 1: implementar simulator v0
GATE_REQUERIDO=none
TAREAS=T1.1-T1.8
SALIDA=working Go simulator + T1–T8 evidence + commit + G4A review
STOP=G4A review; forbidden Shot 2/D5 work

### SHOT_2

FASE_ASIGNADA=2
PAQUETE_CANONICO=Paquete autónomo Fase 2 — Shot 2: auditoría independiente
GATE_REQUERIDO=G4A accepted by owner
TAREAS=T2.1
SALIDA=independent audit + G4B review
STOP=G4B review; forbidden corrections/D5

### SHOT_3

FASE_ASIGNADA=3
PAQUETE_CANONICO=Paquete autónomo Fase 3 — Shot 3: corrección y certificación
GATE_REQUERIDO=G4B accepted by owner
TAREAS=T3.1
SALIDA=certified v0 + G4C review
STOP=G4C review; forbidden D5

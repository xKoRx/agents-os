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
progress: 80
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

- **SHOT 2 (auditoría independiente) en curso (T2.1 WIP).** G4A aceptado por owner (despacho Shot 2, 2026-09-24); commit bajo auditoría `ad7fe609c8b6503cdc7b803d5c33d8eb3efdcff9`.
- Matemática cerrada en [[echo-futures-astra-math-review]].
- Funcional congelado en [[D4 — Simulator v0 Functional SPEC]].
- Técnico congelado en [[D4 — Simulator v0 Technical SPEC]].
- **Evidencia Shot 1 (2026-09-24):**
  - Repo local aislado: `~/aranea/work/echo-futures-simulator-v0-20260924/echo-futures`, branch `master`, HEAD `ad7fe609c8b6503cdc7b803d5c33d8eb3efdcff9`, Go 1.27.1 linux/amd64, módulo `github.com/xKoRx/echo-futures`, sin dependencias externas, sin remote.
  - `go test ./...` PASS · `go test -race ./...` PASS · coverage `internal/sim` **96.0%** (core nuevo; total 95.9%).
  - `sim validate --runs 1000000 --seed 42`: **47/47 PASS** (T1–T8 + invariantes) en ~6.5 s; dos corridas byte-identical (JSON).
  - Sample `simulate` (t2, 1M): pWin 0.4995, pReachAdd 0.7694 (10/13), pWinGivenAdd 0.3495. Sample `simulate` lifecycle (200k): pPass 0.401, pFundedGivenPass 0.2487, q 0.0997, meanCash 19.55. Sample `cohort` (100k): meanAttempts 10.009, meanFailures 9.009, P50=7, P95=29, payoutWithin10 0.6523.
  - Limitations documentadas en README (null driftless sin costes/slippage, barreras estáticas, edge one-shot, cohort IID, float64, sólo first payout).
- Echo, Echo Forge, NinjaTrader y market data están fuera de scope. No se tocó ningún otro repo.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo-futures (local, sin remote) | master | empty/new repo | [[D4 — Simulator v0 Functional SPEC]] | [[D4 — Simulator v0 Technical SPEC]] | G4A_REVIEW @ ad7fe60 |

## Matriz requirement → evidence

| Requirement | Estado | Evidencia |
|---|---|---|
| Matemática first-passage/optional stopping | done | [[echo-futures-astra-math-review]] MATH_GO |
| Behavior v0 | done | [[D4 — Simulator v0 Functional SPEC]] |
| Technical contract v0 | done | [[D4 — Simulator v0 Technical SPEC]] |
| Repo code | done | `echo-futures` @ master ad7fe60 (kernel/trade/lifecycle/cohort/CLI + README + scenarios) |
| Independent audit | blocked | Shot 2 after G4A review |
| Corrections/certification | blocked | Shot 3 after G4B review |

## Decisiones

| ID | status | resolution | source/evidence | phase consuming it |
|---|---|---|---|---|
| D4-01 | TECHNICAL_RESOLUTION | Go, standard library first, event-driven exact hitting kernel | Technical SPEC | Shot 1 |
| D4-02 | CONFIRMED | Simulation-first; no historical market data in v0 | [[Echo Futures]] | Shot 1 |
| D4-03 | TECHNICAL_RESOLUTION | LONG-only normalized process; short symmetry deferred | Technical SPEC | Shot 1 |
| D4-04 | TECHNICAL_RESOLUTION | Synthetic delta once after last executed adverse add | Astra review + Technical SPEC | Shot 1 |
| D4-05 | TECHNICAL_RESOLUTION | Single-threaded deterministic RNG in Shot 1 | Technical SPEC | Shot 1 |
| D4-06 | CONFIRMED | No real prop rules before null/synthetic engine certification | [[Echo Futures]] | Shots 1–3 |

## Gate control

| Gate | current state | phase agent responsibility | owner acceptance evidence | enables |
|---|---|---|---|---|
| G4A — Implementation | **accepted** (owner dispatch Shot 2, 2026-09-24) | implement, run all tests, move to review | T1–T8 + invariants + coverage + commit | Shot 2 |
| G4B — Independent audit | pending | adversarially review code/results, move to review | audit findings/reproduction | Shot 3 |
| G4C — Certified v0 | pending | fix only accepted findings, rerun evidence, move to review | clean T1–T8 + audit closure | D5 |

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
> - [/] T2.1 auditoría independiente Shot 2 #owner/agent #type/pr-review #area/echo
> - [ ] T3.1 corrección/certificación Shot 3 #owner/agent #type/dev #area/echo #blocked

## 📆 Bitácora

- **2026-09-24** — Proyecto de agente materializado para ejecución D4. Math/functional/technical contracts frozen. READY_FOR_SHOT_1; no código ejecutado todavía.
- **2026-09-24** — SHOT 1 iniciado (T1.1 WIP). Autoridades leídas en orden (math review, functional, técnico, proyecto padre); sin contradicciones detectadas. Baseline: Go 1.27.1 linux/amd64; no existe checkout local previo de `echo-futures` (sin conflicto); repo nuevo aislado en workspace externo `~/aranea/work/echo-futures-simulator-v0-20260924/echo-futures`, módulo `github.com/xKoRx/echo-futures`, branch `master`. Tarea puente del padre movida a WIP.
- **2026-09-24** — SHOT 1 COMPLETO, **G4A → review**. Commit `ad7fe609c8b6503cdc7b803d5c33d8eb3efdcff9` (21 archivos, árbol limpio, sin remote/push). Gates: `go test ./...` PASS; `go test -race ./...` PASS; coverage `internal/sim` 96.0%; `sim validate --runs 1000000 --seed 42` 47/47 PASS (~6.5 s) y reproducible byte-identical. Samples: simulate t2 1M (pWin 0.4995 / reach 0.7694 / cond 0.3495), simulate lifecycle 200k (pPass 0.401, q 0.0997), cohort 100k (meanAttempts 10.009, P50 7, P95 29). Nota de corrección durante el shot: el .gitignore inicial (`sim` sin anclar) había excluido `cmd/sim` e `internal/sim` del primer commit; detectado y corregido vía amend del commit raíz (repo nuevo, sin remote). Sin desviaciones de SPEC; el único caso ambiguo resuelto fue clasificar salidas de barrera por dirección del evento + equidad alcanzada con epsilon relativo (empates → fase, según prioridad congelada). Shot 2 (auditoría) queda BLOQUEADO hasta aceptación owner de G4A.

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

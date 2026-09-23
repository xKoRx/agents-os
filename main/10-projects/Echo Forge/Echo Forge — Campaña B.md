---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Personal]]"
parent: "[[Echo Forge]]"
sprint:
start: 2026-09-23
due:
progress: 15
repo: xKoRx/symphony
jira:
prs:
aliases:
  - Echo Forge Campaign B
  - Campana B
tags:
  - kind/project
  - area/personal
created: "2026-09-23"
updated: "2026-09-23"
---

# Echo Forge — Campaña B

%% Naming: Echo Forge — Campaña B es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo Forge — Campaña B
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** —
> Vertical slice posterior a [[Echo Forge — Import Task V1]]: consumir el cohort seleccionado durable y llevarlo a evidencia física final.

## 🎯 Objetivo

- Ejecutar **CAMPAÑA B: SELECTED COHORT → SQX TICK RETEST → MT5**. Consumir el cohort seleccionado (SelectionSnapshot durable de la Campaña A, refs exactas) en un FlowRun NUEVO y producir evaluaciones Forge reales por ticks y evidencia MT5 durable, manteniendo identidad, recovery e idempotencia extremo a extremo. Campaña B NO descubre, clasifica, rankea ni selecciona: la selección nunca se re-ejecuta ni se re-puntúa.

## 📊 Estado actual

- **CB-G2 INTEGRADO A MASTER (2026-09-23, mandato manager — cierre V1 → operación V2).** `feature/sqx-campaign-b` (`dc151e4`+`3847cad`) integrada a `origin/master` por FF con **gate 4/4: build PASS** (só `sqx/tools` roto preexistente, intocado por el delta), **tests del delta PASS** (`sqx/core/runtime` y `sqx/activities/watcher` verdes), **cero regresiones nuevas** (fail-set 37/37 idéntico al baseline `9a69243` por nombre: workflows 21 + worker 16, comparado por diff de nombres), **review scoped PASS** (código leído: fail-closed, identidad re-derivada, watcher binding-only, bootstrap idempotente). Master `d07cc69` → HEAD `e41569b` (promoción del manifiesto 0.2.106; sin cambios de código); rama y worktree eliminados; el resolver viaja en la RC **0.2.106** (binario `vcs.revision=d07cc69, modified=false`, manifest confirmado en MinIO). Sin certificación física previa al merge por mandato: **la primera campaña real ([[Echo Forge — Campaign 001]]) pasa a ser parte de la validación operacional.** Pendientes de ejecución física de B (heredados a Campaign 001): CB-G1 review + freeze §3 del owner.
- **CB-G2 IMPLEMENTADO (2026-09-23, sesión de recuperación + diseño): `feature/sqx-campaign-b` @ `3847cad` (código `dc151e4` + docs SPEC) sobre baseline `origin/master @ 9a69243` (verificado; remoto = sólo `master`). RESULT software = PASS: fail-sets de `sqx/workflows` (21) y `sqx/activities/worker` (16) idénticos al baseline por nombre; `sqx/core/runtime` y `sqx/activities/watcher` verdes; gofmt/vet limpios en el delta.** Decisión de arquitectura congelada (SPEC §2.1): NO se extiende ningún task source; la entrada es la sección `selection_cohort.snapshot_ref` (ref exacta sha256 del SelectionSnapshot) resuelta por un bootstrap interno del workflow ANTES de la primera task (espejo del bootstrap import de D10; no es TaskSpec; jamás en tasks[]; cohort vacío fail-closed; mutuamente excluyente con watcher.import). El watcher porta sólo el binding; `resolve_selection_cohort` (worker) re-deriva la identidad del snapshot, resuelve el artefacto OUTPUT/STRATEGY_SQX exacto de la Builder Evaluation por entry y registra membresía `REPROCESSED` (is_origin=false, insert-once ⇒ retry converge). Stages B con CERO tipos nuevos de task: group `batch_size:1` (fanout vigente, sin host affinity) → retester durable (`stage=retester`, CFX tick OOS del owner) → `mt5_exporter` → `mt5_compiler` → `mt5_backtesting` (model real ticks, período OOS) → `mt5_reconcile_v1` + fidelidad `mt5_fidelity_shadow.v1` → ranking global → promotion (finalist decision). **Gap material congelado: `forge_seal_handoff` (promotion V2) queda FUERA de B** — exige linaje Apply+Compile EvaluationRefs y readback magic estampado; sin Apply (cohort importado sin WFM) el seal daría 0 manifests. Pipeline PASS vs STRATEGY VALIDATION PASS vs EXECUTION FAILURE definidos en el proyecto (ver Decisiones). Worktree externo `~/aranea/work/campaign-b-20260923/symphony` (rama local, sin push). Bloqueos de ejecución vigentes: owner congela §3 (período OOS, tick model, parámetros MT5, criterios A-vs-B) y CB-G1 NORMAL emitido/revisado.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/symphony | `master` @ `e41569b` (origin; CB-G2 integrado 2026-09-23 en `d07cc69`) | FF `9a69243..d07cc69` | Mandato owner 2026-09-23 + `specs/FEAT-SQX-IMPORT-CAMPAIGN-B/SPEC.md` (§2.1 congelada) | Mismo repo: runtime `selection_cohort`, activity `resolve_selection_cohort`, workflow `runSelectionCohortBootstrap` | **CB-G2 INTEGRADO con gate 4/4; CB-G1 review + owner §3 pendientes (gates de ejecución física en [[Echo Forge — Campaign 001]])** |

## 🧩 Subproyectos

```base
filters:
  and:
    - 'type == "project"'
    - 'file.hasLink(this.file)'
views:
  - type: cards
    name: Subproyectos
    order:
      - file.name
      - note.status
      - note.priority
```

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. Tipos: #type/dev #type/admin #type/research #type/pr-review #type/supervision. Flags: #blocked #waiting #urgent. %%
> - [x] CB-G0: baseline `origin/master @ 9a69243` verificado + autoridades recuperadas (SPEC B, Cross-FlowRun Reuse FROZEN, SelectionSnapshot, retester/MT5/seal) #owner/agent #type/dev
> - [x] CB-G2 (parcial código): contrato runtime `selection_cohort` + dispatch watcher + bootstrap workflow + activity `resolve_selection_cohort` con membresía REPROCESSED; tests runtime/activity; fail-sets == baseline @ `dc151e4` #owner/agent #type/dev
> - [x] Integración a master por mandato manager (gate 4/4: build, delta tests, fail-set 37/37 == baseline, review scoped) @ `d07cc69`; rama/worktree eliminados; RC 0.2.106 publicada #owner/me #type/dev
> - [ ] CB-G1: SPEC freeze con §2.1 + review manager independiente + NORMAL de Campaña B — gate de ejecución física en [[Echo Forge — Campaign 001]] C5 #owner/me #type/pr-review
> - [ ] CB-G2 (resto): test E2E de workflow del bootstrap (carrier llega a la primera task) + test de fanout group batch_size:1 con retester durable #owner/agent #type/dev
> - [ ] CB-G3: receta de campaña B (flow.json + CFX tick retest OOS + tasks MT5) como fixture de integración hermética #owner/agent #type/dev
> - [ ] CB-§3: owner congela parámetros (período OOS disjunto, tick model, spread/comisiones, parámetros MT5 build/agent/deposit, criterios A-vs-B, top_n) #owner/me #blocked
> - [ ] CB-G4: fidelity + promotion de Campaña B; decidir v1 vs ranking dedicado; seal V2 documentado como fuera de alcance sin Apply #owner/agent #type/dev
> - [ ] CB-G5: regresión completa + failing set documentado vs baseline #owner/agent #type/dev
> - [ ] CB-G6: certificación física (host autorizado, datos congelados, archivo auténtico) — requiere CB-G1 + CB-§3 #owner/me #blocked
> - [ ] CB-G7: reporte + cierre Agents-OS #owner/me #type/admin
> - [-] Push de `feature/sqx-campaign-b` — OBSOLETO: reemplazado por integración FF a master @ `d07cc69` (2026-09-23); rama eliminada #owner/me #type/dev

## 📆 Bitácora

%% Log diario para las dailies. Una línea por día con lo avanzado / blockers. %%
- **2026-09-23 (integración)** — Mandato manager (cierre V1 → operación V2): CB-G2 integrado a `origin/master` por FF con gate 4/4 (build PASS; delta tests PASS; fail-set 37/37 idéntico al baseline `9a69243` por nombre; review scoped PASS) → master `d07cc69`; rama `feature/sqx-campaign-b` y worktree `campaign-b-20260923` eliminados; el resolver viaja en RC 0.2.106. Certificación física de B NO exigida pre-merge: la validación pasa a ser operacional vía [[Echo Forge — Campaign 001]]. Siguiente: CB-G1 + freeze §3 como gates de ejecución física (C5 de Campaign 001).
- **2026-09-23** — Sesión de recuperación y arranque: baseline `9a69243` verificado (remoto sólo master; worktree externo nuevo); SPEC B borrador congelado encontrada en repo; autoridades mapeadas (SelectionSnapshot inmutable con re-derivación de identidad, Cross-FlowRun Reuse CERTIFIED_CLOSED/FROZEN, retester durable `sqx-retester.v1`, MT5 export/compile/backtest durables con reconcile+fidelidad, promotion + seal F-04). Arquitectura congelada con un único componente nuevo (input selection_cohort vía bootstrap; cero tipos nuevos de task). Gap material identificado y congelado: el seal V2 exige linaje Apply+Compile y readback magic ⇒ fuera de B para cohort importado sin Apply. Implementación CB-G2 completa con tests y regresión == baseline; SPEC §2.1/§4/§5 actualizada @ `3847cad`. Siguiente exacto: CB-G1 (review + NORMAL) y freeze §3 del owner.

## 🧭 Decisiones

- **D-B1 (2026-09-23): entrada = sección `selection_cohort.snapshot_ref` + bootstrap interno**, no task source extendido. Razón: el cohort debe existir como carriers durables ANTES de la primera task (mismo problema que resolvió el bootstrap import D10); el watcher nunca toca el snapshot (independencia contractual worker/watcher preservada).
- **D-B2 (2026-09-23): participación REPROCESSED** vía `RecordFlowRunStrategy` insert-once en el bootstrap (idempotente; el mismo StrategyRef conserva identidad global v2; is_origin=false).
- **D-B3 (2026-09-23): SQX Tick Retest = retester durable (`stage=retester`)**, no el Final Reretester: el cohort importado no tiene DecisionRef de Apply (el final reretester lo exige fail-closed); el retester durable exige exactamente StrategyRef + Builder EvaluationRef, que la SelectionSnapshot porta. El modo tick/período OOS vive en el CFX declarado por task (owner §3), no en código Go.
- **D-B4 (2026-09-23): PASS/FAIL de Campaña B.** PIPELINE PASS = la estrategia atraviesa retester → exporter → compile → backtest con identidad durable íntegra (los fallos técnicos MT5 dropean al candidato sin matar el FlowRun, semántica vigente). STRATEGY VALIDATION PASS = la decisión de finalistas (promotion) sobre el ranking global de scores MT5/retest con los criterios cuantitativos que el owner congele en §3. EXECUTION FAILURE = fallo técnico (SQX, compile, MT5, worker, artefacto) — se registra como artefacto fallido y no invalida al cohort.
- **D-B5 (2026-09-23): seal/handoff Echo (promotion V2) fuera de B-v1.** `forge_seal_handoff` exige carriers con linaje Apply+Compile y readback magic estampado; sin etapa Apply (no hay WFM/robust selection en cohort importado) no hay magic estampado ⇒ el seal daría 0 manifests. Habilitarlo exige un hop de estampado de magic con autorización propia (work package separado, decisión owner).

## 🔗 Docs / Links

- Parent: [[Echo Forge]] · Sucesor operativo: [[Echo Forge — Operación Real V2]] · Predecesor: [[Echo Forge — Import Task V1]] · Entorno: [[Echo + Echo Forge — Environment Contract]]
- Repo: `specs/FEAT-SQX-IMPORT-CAMPAIGN-B/SPEC.md` (§2.1 decisión CB-G2) · `specs/FEAT-SQX-IMPORT-TASK-V1/SPEC.md` · `specs/FEAT-SQX-CROSS-FLOWRUN-REUSE/SPEC.md`
- Branch/worktree históricos eliminados tras integración (2026-09-23); commits en `master` @ `d07cc69` vía FF (`9a69243..3847cad`)

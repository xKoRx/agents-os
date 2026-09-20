---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo — Live Platform V1]]"
sprint:
start: 2026-09-20
due:
progress: 10
repo: xKoRx/echo
jira:
prs:
aliases:
  - Echo E-09
  - Execution copy reconciliation Execution Fidelity
  - E-09 Execution Copy
  - FEAT-EXECUTION-COPY-RECONCILIATION-FIDELITY-E9
tags:
  - kind/project
  - area/echo
  - agent/owner
created: "2026-09-20"
updated: "2026-09-20"
cssclasses:
  - wide
---

# Echo — E-09 Execution Copy Reconciliation and Execution Fidelity

%% Naming: Echo — E-09 Execution Copy Reconciliation and Execution Fidelity es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo — E-09 Execution Copy Reconciliation and Execution Fidelity
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Echo — Live Platform V1]] · **Repo:** `xKoRx/echo`
> Subproyecto de **implementación** de la fase E-09 / Execution copy, reconciliation and Execution Fidelity. No es Integration. El contrato WHAT vive en el SPEC de Echo; esta nota es HOW / ORDER / GATES.

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre [[Echo — Live Platform V1]] enlaza aquí. La supervisión humana del track live sigue en [[Echo — Producto Integrado]].

## 🎯 Objetivo

Medir Execution Fidelity desde los primeros trades como observación: emparejar el universo expected E-08 con los outcomes físicos observados en las cuentas de Execution, veredicto de reconciliación por operación, vector pequeño de fidelidad y métricas con denominador honesto (missing/extra/duplicate/reject/delay distintos). Principios: denominador = expected set retenido (invariante 17); `UNKNOWN != ZERO`; orden enviada ≠ ejecución confirmada; Reference fact ≠ EconomicCommand; Strategy Quality ≠ Execution Fidelity; INNER JOIN prohibido como fidelidad (D-21); reconciliación jamás publica una orden. Unlock: el owner ve si la copia fue fiel. Separación frozen: clase A (contratos/stores/proyecciones con hechos contractuales, hoy) vs clase B (integración condicionada: E-08 C3 + clase C + terminal real).

## 📊 Estado actual

- **E09_PLANNING_FROZEN v1.0.0 (2026-09-20):** SPEC/PLAN/TASKS/VERIFICATION + NORMAL-PROMPT @ `e892b3d7` en branch `feature/e09-execution-copy-reconciliation-fidelity` (base `c2e88a0d` = HEAD E-08 C2; master `5dd998f1` intacto; push FF, HEAD == origin). Migración 067 reservada (exclusiva E-09; disponibilidad verificada, no asumida, en baseline). Frozen: unidad de reconciliación = destinatario E-08 `(source_event_id, operation_kind, recipient_account_registration_ref)`; correlación primaria `command_ref` como CLAIM (jamás prueba de fill; la prueba es el DEAL set E-07 1:N); dedupe dual `source_event_id`+`fact_digest` (receta `echo-trade-fact-ref.v1` frozen C5 reusada); veredictos `PENDING/FILLED/PARTIAL/REJECTED/MISSING_EVIDENCED/UNKNOWN/SUPERSEDED/UNRESOLVED` con `MISSING_EVIDENCED` sólo con evidencia positiva (deadline de ACK jamás produce MISSING); extras/not-requested/duplicados visibles y separados (D-21); vector por operación UNKNOWN-aware (delay MEASURED sólo con basis UTC verificada); métricas con denominador expected set y read model NO autoridad; E-09 READ-ONLY sobre 001–066 (exporta `resolution_evidence` para las ops E-08, jamás aplica transiciones); exposición `CONSUMED` sin liberación por timeout (mandato frozen, exige evidencia de cierre o autoridad contable). **Dependencias exactas E-08 C3 registradas §16 (E08-C3-A gate antes de recover en `Router.Route` router.go:86/218; E08-C3-B `time.Now()` en `classifyCandidate` :274 y `DecisionAt` no restaurado) — no corregidas, no asumidas resueltas; bloquean sólo clase B.** Matriz EF-01…EF-16; gates: `PLANNING_FROZEN`; NORMAL pendiente (`NORMAL-PROMPT.md`). Next = **NORMAL clase A**.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo | `feature/e09-execution-copy-reconciliation-fidelity` | `c2e88a0d` (E-08 HEAD C2; master `5dd998f1` intacto) | `specs/FEAT-EXECUTION-COPY-RECONCILIATION-FIDELITY-E9/SPEC.md` v1.0.0 @ `e892b3d7` | `.../PLAN.md` + `.../TASKS.md` + `.../VERIFICATION.md` + `.../NORMAL-PROMPT.md` | E09_PLANNING_FROZEN @ `e892b3d7` · Next: NORMAL clase A (T00–T13) |

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> - [ ] E-09 T00–T02: baseline + failing sets, dominio execution_fidelity, migración 067 + harness #owner/agent #type/dev #area/echo
> - [ ] E-09 T03–T05: stores outcomes/duplicados + reconciliación CAS + read model métricas #owner/agent #type/dev #area/echo
> - [ ] E-09 T06–T09: pairing + reconciler + driver default OFF + wiring #owner/agent #type/dev #area/echo
> - [ ] E-09 T10–T13: matriz EF-01…EF-16, gates SOURCE/BWC, VERificación con evidencia, handoff Manager #owner/agent #type/dev #area/echo
> - [ ] E-09 clase B: ingesta viva + E2E + certificación semántica (gate Manager/owner; prerrequisitos SPEC §16 incl. E-08 C3) #owner/agent #type/dev #area/echo

## 🗺️ Roadmap (padre)

- [[Echo — Live Platform V1]] § Roadmap → «E-09 Execution copy, reconciliation and Execution Fidelity». Dependencias: E-08 (expected set/lineage/outbox; interfaces verificadas @ `c2e88a0d`, consumidas como base), E-02 recovery. Parallel: E-10/E-11 según su DAG.
- Preservaciones: Strategy Quality ≠ Execution Fidelity · Reference fact ≠ EconomicCommand · orden enviada ≠ ejecución confirmada · UNKNOWN ≠ ZERO · INNER JOIN prohibido · reconciliación jamás publica orden · CONSUMED sin liberación por timeout.

## 📆 Bitácora

- **2026-09-20 — E-09 TOP planning one-shot:** [[Echo — E-09 Execution Copy Reconciliation and Execution Fidelity]] SPEC/PLAN/TASKS/VERIFICATION + NORMAL-PROMPT v1.0.0 @ `e892b3d7` pusheados a `origin/feature/e09-execution-copy-reconciliation-fidelity` desde `c2e88a0d` (HEAD E-08 C2; docs-only, 5 archivos; master intacto `5dd998f1`). Baseline resuelto contra repos reales (ramas E-06 `b66dc5ff` / E-07 `3765f2ba` / E-08 `c2e88a0d` local=origin; migración 067 libre verificada en baseline). Frozen: correlación por destinatario E-08 con `command_ref` como claim y DEAL set E-07 como prueba; dedupe dual + duplicados append-only; veredictos con `MISSING_EVIDENCED` sólo con evidencia positiva; métricas con denominador expected set (invariante 17), read model no autoridad, p50/p95 POST; E-09 READ-ONLY sobre 001–066 y exportador de `resolution_evidence`; `CONSUMED` sin auto-release (mandato). Dependencias exactas E-08 C3-A/C3-B registradas en SPEC §16 con file:symbol:line (router.go:86/:218/:260/:274) — sin retoque, bloquean sólo clase B. Separación clase A (contratos/stores/proyecciones/métricas con fixtures, cero órdenes) vs clase B (ingesta viva, E2E, certificación semántica master §8). Worktree `/tmp/echo-e09-execution-copy-reconciliation-fidelity`. E-01…E-08 no reabiertos. Next = NORMAL (`NORMAL-PROMPT.md`).

## 🧭 Decisiones

- La unidad de reconciliación es el **destinatario E-08** (UNIQUE de `trade_routing_recipients`): el denominador es el expected set retenido, jamás un INNER JOIN de pares exitosos (invariante 17; D-21).
- `command_ref` propagado por el EA es **claim de atribución, no prueba**: el fill se demuestra con el DEAL set E-07 1:N (costos con signo, NULL ≠ 0, jamás último gana); claim sin corroboración ⇒ warning `ATTRIBUTION_UNVERIFIED`, jamás FILLED.
- `MISSING_EVIDENCED` exige **evidencia positiva** de no-fill; el vencimiento de un deadline de ACK jamás produce MISSING (master §8) — la ausencia de evidencia es `UNKNOWN` con razón durable.
- E-09 es **READ-ONLY sobre 001–066**: produce `resolution_evidence` exportable para las store-ops de reconciliación E-08 (`ResolveUnknownByEvidence`/`RepairOrphan`), jamás aplica transiciones en clase A; `CONSUMED` no se libera por timeout (sin autoridad contable, decisión Manager).
- Event time ≠ recorded time en todo el carril: delay MEASURED sólo con basis UTC verificada (invariante 15); replay actualiza metadatos de proceso, jamás timestamps económicos (invariante 13).
- Los defectos E-08 C3-A/C3-B son **dependencia exacta de clase B** (SPEC §16): clase A no los necesita; clase B exige C3 resuelto y verificado en su carril antes de su gate.

## 🔗 Docs / Links

- `specs/FEAT-EXECUTION-COPY-RECONCILIATION-FIDELITY-E9/` (SPEC/PLAN/TASKS/VERIFICATION/NORMAL-PROMPT) en `xKoRx/echo`.
- [[Echo — Live Platform V1]] · [[Echo — E-08 Routing EconomicCommand and Risk Reservation]] · [[Echo — E-07 Raw Facts DEAL Coverage Trade Lifecycle]] · [[Echo — E-06 Reference Enrollment and Binding]] · [[Echo — E-02 Control Safety, Auth and Journal Recovery]] · [[Echo — Producto Integrado]]
- [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] (§7 Command lineage and recovery; §8 invariantes 12/13/14/15/16/17/18)
- [[Echo + Echo Forge — Arquitectura de producto, gaps y roadmap de cierre 2026]] (§8 Execution Fidelity blueprint — autoridad semántica)
- [[Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan]] (D-21, H4, A11)
- [[Echo + Echo Forge — Deferred Certification Backlog]]

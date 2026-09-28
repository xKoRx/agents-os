---
type: agent_memory
schema_version: 1
scope: project
created: "2026-09-28"
updated: "2026-09-28"
area: "[[Echo]]"
project: "[[Echo Futures]]"
entities:
  - "[[Echo Futures]]"
related:
  - "[[Echo Futures — D2-09 Blocking Refactors]]"
  - "[[Echo Futures Architecture Candidate V1]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
  - "[[Echo Futures — D2-08 Strategy Runtime]]"
aliases: []
confidence: high
memory_state: active
continuity_key: "echo-futures/d2-09-worker"
load_policy: when_project_loaded
indexable: false
index_priority: high
tags:
  - kind/agent-memory
  - scope/project
  - agent/internal
  - area/echo
---

# Echo Futures — Continuidad D2-09 (Q16 + Integración Final)

## Continuidad

- Estado vigente: `D2-09 = READY_FOR_MANAGER_REVIEW` · `Q16 = CLOSED` · `EF_D2_DESIGN_PASS = READY_FOR_MANAGER_REVIEW` (NO PASS, NO CLOSED — decide Primary Manager). Baselines: Agents-OS inicio `5af8e18f` (≥ mínimo `2c4bc4fd`), Echo `372af59a` fetch sin delta.
- **Q16 cerrado sin `BLOCKING_ARCHITECTURE`; CORE REWRITE NOT_REQUIRED.** Matriz final de 37 ítems A–G en [[Echo Futures — D2-09 Blocking Refactors]] §16. Register D1 (7 ítems) reconciliado: 5 → NEW diseñado en D2-04..08; DayBoundary → ADAPT/REPLACE (R18); Trade/Lab → DEFERRED_TO_THE_LAB (no reabrir).
- **Decisión de identidades (corazón de Q16):** `signal_id` determinística (D2-08, intacta). `operation_id`/`order_id`/`decision_id`/action ids **permanecen UUIDv7** — demostración estructural: EXACT_REPLAY V1 (D2-06 §19/§22) no re-ejecuta el dominio de ejecución (D2-04 R12) ⇒ ninguna fixture compara esas IDs; correctness por M1 2PC (identidad regenerada jamás convive con artefacto físico abortado) + M2 journal. Propiedad congelada: identidad generada que participe de output determinista debe ser replay-stable; familia `DeterministicDomainID(run, owner, owner_event_seq, kind, local_seq)` instanciada hoy sólo por `signal_id`. Nota Iteración 2: si replay de ejecución se extiende, esas IDs migran a la familia (camino natural: `(account_strategy_id, strategy_cycle_seq)`).
- **EXACTLY_ONCE etc. = IMPLEMENTATION_REQUIRED, no comportamiento actual:** `module.yaml` verificado físicamente sin delivery semantics (egress default AT_LEAST_ONCE). Requisito de SPEC con acceptance D5/D6 (carry D2-04 R2 / D2-06 R5 / D2-08 R2).
- **`DT-EF-REFERENCE-SIGNAL-03` = DEFERRED_MANDATORY Iteration 2** confirmado: V1 Futures no depende del planner Reference legacy (camino canónico nace en `echo/strategy_engine`; adapter `ReferenceEvent→Signal` es seam hacia el mismo camino).
- **Artefactos creados:** [[Echo Futures — D2-09 Blocking Refactors]] (Q16) y [[Echo Futures Architecture Candidate V1]] — **nueva autoridad de lectura primaria de D2** (integra D2-04..08 sin copiarlos; Q gate table completa: Q2–Q11+Q14 CLOSED, Q15 DEFERRED_TO_THE_LAB_BY_OWNER, Q16 CLOSED, Q12/Q13→D4; OWNER_DECISIONS_REQUIRED=NONE). [[Echo Futures]] actualizado con sección D2-09.
- Pips: constraint V1 ya congelada; limpieza legacy = deuda Iteration 2 con ID/alcance **pendiente ratificación owner** (estado preexistente del proyecto; NO formulada como nueva owner decision — no bloquea este gate).
- Riesgos materiales registrados: config EXACTLY_ONCE es requisito no comportamiento; M2 vendor sin evidencia física (MARKET sin history-by-tag queda `UNSUPPORTED_FOR_V1_EXACT_SUBMISSION`); throughput StateFun carry; determinismo verificable sólo por suites; deuda pips sin ID ratificado; drift patrones duplicados durante coexistencia.
- No se implementó código, no se tocaron children A/B/C ni decisiones cerradas, no se abrió D3/Astra ni D4/D5/D6, no se seleccionó transport.

## Señales de carga

- Cargar cuando el Primary Manager revise D2-09 / Architecture Candidate V1, cuando se abra D3 (Astra) o D4 (SPEC/freeze: la matriz A–G de D2-09 §16 alimenta el SPEC y los shots), o al planificar D5/D6 (obligaciones D2-09 §18; gates D6 §24 de D2-07 + §18-D6).
- La decisión de identidades (UUIDv7 de ejecución vs DeterministicDomainID) debe preservarse en review: cualquier propuesta de "hacer todo determinístico" sin extender el replay boundary es sobre-ingeniería; cualquier extensión del replay a ejecución exige migrar las IDs.

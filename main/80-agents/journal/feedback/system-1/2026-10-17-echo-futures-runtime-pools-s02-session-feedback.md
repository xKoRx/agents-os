---
type: feedback
schema_version: 1
scope: session
created: "2026-10-17"
updated: "2026-10-17"
area: "[[Echo]]"
project: "[[Echo Futures — Runtime Pools]]"
entities:
  - "[[Echo Futures — Runtime Pools]]"
related:
  - "[[ECHO-FUTURES-RUNTIME-POOL-DESIGN]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run: "[[2026-10-17-zcode-glm53-echo-runtime-pools-s02-submanager]]"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/feedback
  - scope/session
---

# Feedback — S02 Echo Futures Runtime Pools (submanager + W0–W7)

## Qué funcionó

- Delegación one-shot con allowlist de archivos + freeze contractual (W0) + mandatos cerrados: 13/13 entregas integrables, 0 subdelegaciones, 0 violaciones de allowlist detectadas en los diffs revisados; los workers respetaron «R6 es cerrado» sin excepción.
- La revisión del submanager (re-ejecutar tests + spot-check de invariantes en el diff) detectó lo que los PASS de worker no demostraban: el defecto de evaluación de política (W1) fue encontrado por el E2E de W6, no por W1; el harness de falsificación independiente (W7) encontró 7 defectos que 6 workers habían pasado por alto, incluido el wiring de la política de presupuesto (QA-06: tests unitarios verdes, contrato inexponible end-to-end).
- Las reparaciones acotadas (mandato mínimo + archivos exactos + «tests ajenos byte-idénticos») cerraron 11 defectos en 4 rondas sin regressiones.

## Fricciones

- Freeze vs realidad: W0 congeló structs «cerrados» pero R6 exige read models que no cabían en ellos (W1 decidió additive-vs-PLAN_CONFLICT sin autoridad explícita); la prosa de un hallazgo contradecía a su propio oráculo (QA-06) y mandó el test — los mandatos futuros deberían derivar prosa de tests, no al revés.
- Labels stale en skips de tests («W1 defect» vigente tras el fix) costaron arqueología a dos workers; etiquetar skip por defecto+condición de desbloqueo.
- Ruido de baseline no documentado en los mandatos de cada worker: 5 fallos go test heredados y ~18 archivos gofmt-desformateados en HEAD hicieron que cada worker re-verificara lo mismo (W3 y W4/W6 lo estancaron con stash-verify); la lista de baseline debió viajar en el prompt desde el Paso 0 — lo hizo a partir de W4, pero temprano habría ahorrado ciclos.
- Cobertura ≥95% choca con ramas I/O no inyectables (journalfs como root) y con brazos defensivos; los workers justificaron por paquete, pero un convenio de «justified-unreachable» explícito ahorraría la negociación por-worker.

## Internal Memory

- Sin uso: la base de Agents-OS (constitución+continuidad+planner) bastó; la memoria de proyecto vive en el planificador y fue suficiente. La nota interna global («estado durable antes de repetir efectos») se aplicó literalmente en las verificaciones post-entrega (leer commit/diff real antes de aceptar el PASS del worker) y demostró valor (3 entregas con deficiencias fueron detectadas en revisión, no en producción).

## Score

- Sesión: 4/5 (entrega completa con QA adversarial y correcciones dentro de S02; descontado por las 2 rondas extra de reparación que un Paso 0 con oráculos E2E trade-level habría evitado).
- Componentes: ZCode Agent tool 5/5 (subagentes locales estables, contextos frescos reales); go test del repo 4/5 (determinista, ~2.5 min, pero baseline ruidoso); vault/Agents-OS 4/5.

## Pain Pattern Candidate

- «Contrato implementado ≠ contrato alcanzable»: tests unitarios verdes sobre una política que ninguna ruta de composición podía expresar (QA-06). Candidato a L3: exigir en todo gate de implementación un test de «alcance end-to-end del contrato» (composición→consumo) además del unitario.

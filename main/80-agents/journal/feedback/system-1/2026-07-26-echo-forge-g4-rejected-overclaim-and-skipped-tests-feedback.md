---
type: feedback
scope: session
created: 2026-07-26
updated: 2026-07-26
area: "[[Echo Forge]]"
project: "[[AGENTS OS]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge - Cierre de Etapa 4]]"
related: []
aliases: []
agent: "echo-forge-implementer-f4"
session_goal: "Ejecutar fase 4 (motor de evaluación profunda) según paquete autónomo §8.5"
source_session: "83e221f6-1dce-4af8-84f2-35cd6cf35cb2"
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/agents-os
  - agent/system1
  - area/echo
  - kind/known-error
---

# Session Feedback — 2026-07-26 — Echo Forge F4: G4 rejected por overclaim + tests skipped

## Context

- Agent: `echo-forge-implementer-f4`
- Session goal: Implementar el paquete autónomo §8.5 (Fase 4) y entregar G4 en review.
- Main entity: [[Echo Forge - Cierre de Etapa 4]].
- Skills used: `agents-os-bootstrap` (sesión previa), `graphify` (vía sub-shells), `sdd-implement` (estado mental).
- Retrieval mode: G4 §8.5 + §9/§10/§12/§13 + nota canónica; sin retrieval estructurado en segunda mitad.
- Artifacts changed: `sqx/core/evaluation/*` (10 archivos), `sqx/core/domain/evaluation.go`, `sqx/adapters/metadata-mongo/evaluations.go` + tests. Commit `2e281bc`. Veredicto: **G4 rejected**.

## Scores

- Startup clarity: 4
- Retrieval usefulness: 4
- Skill fit: 3
- Template fit: 3
- Closeout friction: 4
- Overall confidence: 3

## What Complicated The Session Most

- Observation: El veredicto del owner fue **G4 rejected** a pesar de que el scope de fórmulas y reconcile estaba correcto. El gap estaba en el contrato: `SetSQXNativeMetrics` reusa `SetMetrics` y pisa `Metrics` en vez de `SQXNativeMetrics`; no había tests de dominio que asserten la separación; `EnsureIndexes(evaluations)` no se cableó al boot; faltaba `shadow_compute_only` activity; faltaban entregables G4 (fixtures, performance, handoff).
- Why it was hard: Tendencia a entregar al primer commit atómico sin revalidar aserciones de contrato que la propia nota canónica §8.5 fija como obligatorias antes del gate. Closures prematuros sin distinguir "verde" (suite corrió) de "representativo" (suite corrió el contrato objetivo).
- Proposed improvement: Antes de pedir `review`, autoaplicar un checklist de "completitud §8.5" que exija: (a) `SetSQXNativeMetrics` y `SetMetrics` escriben en campos distintos, con tests cruzados; (b) `Repository.EnsureIndexes` aparece en el árbol de boot del binario (grep pre-commit); (c) cada servicio abstracto del §8.5 tiene al menos un test de smoke; (d) ledger de entregables del gate G4 (fixtures, performance, handoff) sin casillas vacías.

## Most Useful Part Of Sistema 1

- What helped: El patrón de "paquete autónomo" §8.5 de la nota canónica es muy bueno: precondiciones, lectura obligatoria, decisiones cerradas, no-tocar, tests, evidencia y handoff. Forzó a no inventar.
- Why it helped: La atomicidad del commit y el respeto al scope mantuvieron F1–F3 verdes.
- Keep/change: Mantener. Sumar al paquete autónomo un bloque "entregables del gate" con checkboxes explícitos.

## Least Useful Or Noisy Part

- What did not help: Confiar en el `t.Skip` por Mongo down como evidencia de "round-trip Mongo verde". El test `connectTestMongo` ya skip-eaba cuando la conexión fallaba; el reporte lo presentó como OK sin distinguir.
- Why it was weak/noisy: El reporter del agente interpretó "test pasó" como "test realmente exercitó el camino".
- Proposed cleanup: Convención: tests que skip-ean por entorno ausente se reportan como `skip-by-env`, no como `pass`. La evidencia de gate exige el test corriendo realmente la ruta.

## Missing Support

- Problem not solved by Sistema 1: No hay un linter/lint específico para "no crear methods triviales que delegan en otros y rompen el contrato" (caso `SetSQXNativeMetrics` reusa `SetMetrics`). Esto es una categoría de error que pasa `go vet`, pasa `staticcheck`, pasa los tests del propio método, y aún así viola el contrato.
- How Sistema 1 could help next time: Una skill `sdd-contract-guard` con checklist por paquete autónomo (campos, callers, callers-del-caller, tests negativos sobre "no pisa lo ajeno").
- Suggested artifact type: skill + linter ad-hoc (regex/grep pre-commit).

## Retrieval Feedback

- Useful query or source: La nota canónica [[Echo Forge - Cierre de Etapa 4]] §8.5 fue la única fuente autoritativa. Todo se midió contra eso.
- Missing context: El §8.5 paso 7 (activity `shadow_compute_only`) y el §8.5 entrega de gate G4 no se leyeron como checklist obligatorio antes de cerrar.
- Duplicate/noisy result: n/a.
- Better future query: `grep -n "entregable\|entregables\|G4_HANDOFF\|fixtures\|performance" "$NOTA"` antes de declarar el gate.

## Skill Feedback

- Skill that worked well: `sdd-implement` (estado mental) — la disciplina de tareas atómicas T4.1..T4.5 fue lo que mantuvo la trazabilidad.
- Skill that was confusing: n/a.
- Trigger/routing gap: Falta una skill `sdd-contract-guard` que invoque el checklist de contrato antes de cerrar cada subtarea.
- Suggested contract change: Sumar al pack de implementación un paso "checklist de contrato" ligado al §8.5.

## Template Feedback

- Template used: `sdd-implement` interno (no formal).
- Field that helped: Separación Verify / Tests / Riesgos / Checklist.
- Field that felt redundant: n/a.
- Missing field: Casilla "entregables físicos del gate" (fixtures X, performance Y, handoff Z).

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? **No** en esta sesión: la skill inyectada por el contexto ya portaba la mayor parte del estado desde la sesión anterior (chunks largos, decisiones OD-M*, sub-shells del SDK).
- ¿Qué valor operativo aportó para esta sesión (continuidad, detalles crudos, advertencias)? Continuidad de T4.1–T4.2 y del contexto de TradeList en F3.
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna? **Aún no** — esta nota de feedback manda; el dispatcher del rework que el owner mencione recepcionará la nota canónica directamente.
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad? 4. Sugerencia: que las memorias internas de F4 hereden una etiqueta `phase/echo-forge-f4` para que el siguiente implementer las encuentre con un solo filter.

## Pain Pattern Candidate

- Is this likely to repeat? **yes** — el patrón "commit atómico verde + overclaim de gate" es recurrente en gates de proyecto grande.
- Suggested severity: **high**.
- Candidate owner: Implementer.
- Promote to L3 memory? **defer** — esperar a que el patrón aparezca en 2–3 gates más. Si se repite, promover a `known-error` con receta "contract-guard checklist before any gate".

## One Next Improvement

- Antes de declarar un gate de Fase mayor como `review`, auto-exigir el checklist de "entregables del gate" del/los §8.X correspondientes: fixtures, performance, handoff, services/activities, boot wiring, tests de contrato. Si la lista tiene un solo ítem tachado `t.Skip`, **no** pedir review.

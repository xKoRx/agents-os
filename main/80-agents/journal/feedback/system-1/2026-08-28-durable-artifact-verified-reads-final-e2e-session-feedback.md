---
type: feedback
schema_version: 1
scope: session
created: 2026-08-28
updated: 2026-08-28
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
entities:
  - "[[Echo Forge]]"
  - "[[AGENTS OS]]"
related:
  - "[[2026-08-28-durable-artifact-verified-reads-final-e2e-normal]]"
aliases: []
agent_surface: "[[Codex]]"
agent_model: unknown
agent_run:
session_goal:
source_session: DURABLE-ARTIFACT-VERIFIED-READS-FINAL-E2E-NORMAL
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/agents-os
  - agent/system1
---

# Session Feedback - 2026-08-28 - durable artifact verified reads final e2e

## Context

- Agent surface: Codex
- Agent model: unknown
- Agent run: certification-only session; no product code changes.

## Fricción observada

- El despliegue operativo requirió distinguir procesos activos por path de release frente a un marker `CURRENT` de otro producto.
- La suite SDK completa no fue ejecutable como señal limpia por módulos privados ausentes, dependencias del sistema y drift de tests.
- La auditoría encontró un reader productivo de reconciliación que reconstruye identidad; el patrón merece una regla estática dedicada.

## Mejora sugerida

- Añadir al preflight una búsqueda específica de `StatObject/GetObject` que construya `DurableArtifactRef` dentro de branches `PersistenceModelV1`, y separar watcher/intake de worker release evidence.

## Resultado

- Feedback local de sesión; no indexable en Graphify. No contiene secretos ni rutas machine-specific.
- Session goal: certificación final de verified reads durable.
- Main entity: Echo Forge / xKoRx/symphony.
- Skills used: Agents OS bootstrap, session close, Graphify maintenance.
- Retrieval mode: cold-start scoped retrieval plus exact source audit.
- Artifacts changed: cinco notas Agents OS; ningún source code.

## Scores

Use 1-5, where 1 is poor and 5 is excellent.

- Startup clarity: 5/5.
- Retrieval usefulness: 4/5; el blocker productivo requirió auditoría source directa.
- Skill fit: 5/5.
- Template fit: 4/5.
- Closeout friction: 3/5 por suite SDK incompleta y despliegue multi-host.
- Overall confidence: 5/5 sobre el bloqueo; 0/5 para una certificación PASS global, correctamente no emitida.

## What Complicated The Session Most

- Observation: había que separar evidencia de release activa, intake watcher y workers durables.
- Why it was hard: coexistían cambios foreign dirty, releases históricas y un marker `CURRENT` no perteneciente al worker certificado.
- Proposed improvement: preflight que registre path de proceso, hash y origen de cada worker antes del intake.

## Most Useful Part Of Sistema 1

- What helped: bootstrap y continuidad del proyecto.
- Why it helped: fijó baseline, reglas de no-fix y persistencia de evidencia.
- Keep/change: mantener; añadir detector de reconstrucción de refs.

## Least Useful Or Noisy Part

- What did not help: suite SDK completa como gate operacional.
- Why it was weak/noisy: falló por módulos privados, libzmq, drift de tests y endpoint externo.
- Proposed cleanup: clasificar dependencias de entorno antes de usarla como señal de producto.

## Missing Support

- Problem not solved by Sistema 1: detectar automáticamente key→Stat/Get→ref en paths durables.
- How Sistema 1 could help next time: mantener query/rulebook de “digest inference from key”.
- Suggested artifact type: known_error + lint preflight.

## Retrieval Feedback

- Useful query or source: auditoría de `ReconcileApplySelectedRun` y boundary `FetchDurableToPath`.
- Missing context: matriz persistida de readers productivos por family.
- Duplicate/noisy result: Graphify incluyó nodos de fixtures/code en query amplio.
- Better future query: `Echo Forge known_error durable verified reads Apply reconcile digest key`.

## Skill Feedback

- Skill that worked well: session close y Graphify maintenance.
- Skill that was confusing: ninguno bloqueante.
- Trigger/routing gap: una auditoría de verified reads debería activar una checklist de `StatObject`.
- Suggested contract change: marcar construcción de refs desde storage metadata como fail-closed anti-pattern.

## Template Feedback

- Template used: feedback de sesión.
- Field that helped: friction/improvement.
- Field that felt redundant: scores para una sesión bloqueada.
- Missing field: release/worker matrix resumida.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? sí.
- ¿Qué valor operativo aportó para esta sesión (continuidad, detalles crudos, advertencias)? Aportó continuidad de release, workers y reglas de cierre.
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna? No; el known-error público contiene el RCA exacto.
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad? 4/5; conviene indexar explícitamente los blockers de runtime.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: high
- Candidate owner: Symphony Apply / storage boundary.
- Promote to L3 memory? yes

## One Next Improvement

- Añadir el detector key→Stat/Get→ref al RCA de Apply antes de reabrir la certificación.

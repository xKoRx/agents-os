---
type: feedback
schema_version: 1
scope: session
created: 2026-10-31
updated: 2026-10-31
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
entities:
  - "[[Polymarket Engine — MVP]]"
  - "[[AGENTS OS]]"
related:
  - "[[Research — E1 Fee Model Conformance W1-q 2026-10-31]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: minimax/MiniMax-M3.1-Flash
agent_run: "[[2026-10-31-zcode-minimax-m3.1-flash-polymarket-w1q-e1-conformance]]"
session_goal: Mapear FeeSchedule/economics para separar exactitud, elegibilidad y roles del modelo documentado e=1 sin cambiar historia
source_session:
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

# Session Feedback - 2026-10-31 - code-scout-w1q-e1-fees

## Context

- Agent surface: [[ZCode]] (fallback inline del code scout; **no** es un subagente y no se le atribuye independencia) · Agent model: `minimax/MiniMax-M3.1-Flash` · Agent run: [[2026-10-31-zcode-minimax-m3.1-flash-polymarket-w1q-e1-conformance]] · Session goal: mapear `FeeSchedule`/economics, los efectos laterales de tests en los dos paquetes y el seam reutilizable sin cambiar historia · Main entity: [[Polymarket Engine — MVP]] · Skills used: `agents-os-code-scout` + `../_shared/scout-contract.md` · Retrieval mode: `dispatch_id=w1q-e1-fees`, lectura dirigida de fuentes exactas del repo, sin discovery amplio · Artifacts changed: `scout-pack.json` en el shot y este feedback (persistido una vez, sin repetir el scout).

## Scores

- Startup clarity: 4 · Retrieval usefulness: 4 · Skill fit: 4 · Template fit: 3 · Closeout friction: 3 · Overall confidence: 4 (autoevaluación del fallback inline; la evidencia es el pack persistido y el uso que hizo de él el implementador).

## What Complicated The Session Most

- Observation: la superficie no expone búsqueda por símbolo (ni Glob ni Grep) y el hook denegó la lectura del runbook operativo del code scout con el literal `Outside immutable W1-q scope`; el scout tuvo que reconstruir ese paso desde el contrato compartido y la skill.
- Why it was hard: sin enumeración de callers no se puede cerrar el requisito "no romper el contrato legacy" por evidencia directa, y sin runbook el procedimiento pierde un control explícito; el pack tuvo que declarar ambos gaps en vez de resolverlos.
- Proposed improvement: exponer búsqueda por símbolo de sólo lectura para el fallback inline y marcar en la skill qué pasos del runbook son irremplazables (para que una denegación se reporte como degradación acotada y no como procedimiento improvisado).

## Most Useful Part Of Sistema 1

- What helped: el contrato de `FeeSchedule` (id, versión, provenance, rounding, rate decimal exacto, exponente positivo) más el taxonomy de errores dieron la línea base exacta para separar "elegibilidad del modelo documentado" de "contrato legacy", que fue la pregunta central del encargo.
- Why it helped: permitió un seam aditivo con reutilización de la aritmética y sin duplicar calculadores, y dejó explícito qué NO debía cambiarse (`LevelCost`, `TRUNCATE_6DP`, `BuildQuoteScheduled`).
- Keep/change: mantener; añadir el detalle de "qué contrato legacy queda congelado por el encargo" como campo explícito del dispatch.

## Least Useful Or Noisy Part

- What did not help: la ausencia de índice de código y de búsqueda por símbolo en esta superficie; el materializador de notas del vault tampoco era aplicable al scout (el pack es un artefacto del shot, no una nota canónica) y su escritura tuvo que esperar al cierre.
- Why it was weak/noisy: el contrato de scout exige feedback persistido por invocación, pero la superficie sin grounding de vault obliga a un artefacto intermedio que después debe volcarse a una nota del journal.
- Proposed cleanup: permitir que el pack de scout se persista directamente como feedback canónico cuando la ruta de vault esté autorizada, o declarar explícitamente el modo "pack en artefacto externo" con su regla de volcado.

## Missing Support

- Problem not solved by Sistema 1: el scout no puede afirmar "no hay otros callers" sin búsqueda por símbolo; quedó como gap declarado con mitigación (cambio aditivo + refactor que conserva firma, kinds y valores).
- How Sistema 1 could help next time: un modo de lectura por símbolo que devuelva rutas y líneas (no contenido masivo) bastaría para cerrar ese requisito.
- Suggested artifact type: extensión de la skill de code scout (sección de degradación por superficie sin búsqueda).

## Retrieval Feedback

- Useful query or source: `internal/regimes/schedule.go`, `internal/economics/scheduled.go`, `internal/economics/economics.go`, `internal/foundation/{decimal,units,errors}.go` y los tests existentes de ambos paquetes (`schedule_test.go`, `w1m_schedule_test.go`, `sfg02_fee_test.go`, `w1m_scheduled_test.go`, `economics_money_test.go`) — los tests existentes fijan los lexemes exactos que el refactor debía preservar.
- Missing context: el runbook del code scout (denegado) y el índice de código del repo.
- Duplicate/noisy result: ninguno; no se repitió discovery del vault ni de otros repos.
- Better future query: para el fallback inline, pedir el contrato del paquete y sus tests de contrato como puntos de entrada, en vez de un mapa general.

## Skill Feedback

- Skill that worked well: `agents-os-code-scout` en su secuencia de identidad → reglas → flujo → riesgos → mapa; el bloque de "test side effects" fue el que justificó no tocar la suite ni los escritores.
- Skill that was confusing: el contrato de scout pide "un scout por invocación" y la superficie no tiene subagentes: el fallback inline queda como modo declarado, y conviene que la skill diga qué evidencia NO puede producir ese modo (aquí: enumeración de callers).
- Trigger/routing gap: falta una regla explícita para el fallback inline cuando el vault está fuera de alcance y el pack debe vivir en un artefacto externo.
- Suggested contract change: añadir al contrato una cláusula de "degradación declarada del fallback inline" con la lista mínima de hechos que ese modo no puede afirmar.

## Template Feedback

- Template used: `80-agents/templates/session-feedback.md` (materializado con `materialize_schema_note.py`).
- Field that helped: `agent_surface`/`agent_model` y `source_session` dejaron la atribución del pack sin ambigüedad.
- Field that felt redundant: `application` vacío en una nota de proyecto sin app.
- Missing field: `dispatch_id`, que es la clave que el propio contrato de scout exige usar en el identificador del feedback; hoy vive sólo en el cuerpo y en el nombre del archivo.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? no — el fallback inline se ejecutó dentro de una sesión que ya había cargado la base del bootstrap; no correspondía una segunda lectura.
- ¿Qué valor operativo aportó para esta sesión (continuidad, detalles crudos, advertencias)? el aporte vino de la continuidad global ya en contexto (leer estado durable antes de repetir efectos laterales), que se aplicó al no repetir búsquedas ni efectos y al reportar las denegaciones sin variantes.
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna? no — el delta es de procedimiento de exploración en esta superficie y pertenece al feedback público y a la skill, no a la memoria interna global.
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad? 4 — es útil para advertencias recurrentes; en este turno no hubo una que lo justificara.

## Pain Pattern Candidate

- Is this likely to repeat? yes — el fallback inline sin búsqueda por símbolo ni con acceso parcial al vault parece una configuración recurrente de esta superficie.
- Suggested severity: low
- Candidate owner: responsable de la skill `agents-os-code-scout` (no el principal de este encargo)
- Promote to L3 memory? defer — la mejora pertenece a la skill/runbook del code scout, y este run no editó la skill por no tener hallazgo propio con validación de authoring.

## One Next Improvement

- Añadir al contrato de scout una **degradación declarada del fallback inline**: qué hechos no puede afirmar ese modo (enumeración de callers, ausencia de evidencia negativa) y cómo debe reportarlos, para que un pack inline nunca se lea como si fuera un subagente independiente.

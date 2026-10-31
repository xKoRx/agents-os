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
session_goal: Conformidad offline del modelo documentado de fee e=1 con fixtures sintéticos, sin piloto, sin capturas y sin tocar L
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

# Session Feedback - 2026-10-31 - polymarket-w1q-e1-conformance

## Context

- Agent surface: [[ZCode]] · Agent model: `minimax/MiniMax-M3.1-Flash` (reportado por el encargo y por el runtime, nunca inferido) · Agent run: [[2026-10-31-zcode-minimax-m3.1-flash-polymarket-w1q-e1-conformance]] · Session goal: conformidad offline del modelo documentado e=1 · Main entity: [[Polymarket Engine — MVP]] · Skills used: `agents-os-bootstrap`, `agents-os-context-retrieval`, `agents-os-code-scout` (inline-fallback), `agents-os-agent-run-register`, `agents-os-session-close` · Retrieval mode: bootstrap en cold start + fuentes exactas del repo y del vault, sin búsqueda amplia · Artifacts changed: 2 paths de producción + 2 tests (commit local `dee7a97`), informe canónico, 5 artefactos del shot y 6 notas de journal.

## Scores

- Startup clarity: 4 · Retrieval usefulness: 4 · Skill fit: 4 · Template fit: 4 · Closeout friction: 3 · Overall confidence: 4 (autoevaluación; la evidencia primaria es outcome/verification/rework y la revisión del supervisor).

## What Complicated The Session Most

- Observation: la revisión de fuente detectó que la rama MAKER de la vía documentada resolvía fee y caja **sin validar el dominio de precio** de los takes consumidos, porque la caminata de libro no valida precios; los tests de precio inválido sólo cubrían el rol TAKER.
- Why it was hard: la ruta documentada y la legacy comparten `FeeSchedule`, así que el dominio `(0,1)` quedaba ontologicalmente atado al rol que cobra, no al modelo; un rol que "no paga" se leía como "no aplica".
- Proposed improvement: en cualquier vía que use una curva por lado, el guard de dominio debe ejecutarse **una vez, antes** de bifurcar por rol; conviene un criterio explícito en la revisión ("¿qué valida cada rama?") y no sólo por aritmética.

## Most Useful Part Of Sistema 1

- What helped: el contrato de `FeeSchedule` y el taxonomy de errores (`KindUnsupported` = "bien formado pero fuera del contrato congelado") permitieron fail-closed en `e ≠ 1` sin tocar el contrato legacy; y el draft heredado de W1-q (modelo, unidades, redondeo no adjudicado, `REAL_FEE_READY=false`) llegó ya leído y con fuentes fechadas, así que el trabajo fue de implementación y no de re-investigación.
- Why it helped: separar "conformidad del modelo" de "certificación de cobro" evitó el modo de fallo más caro del dominio (afirmar un cobro que nadie observó).
- Keep/change: mantener. Falta un artefacto que ya no haya que reconstruir: el ledger de fuentes con Extractos literals reutilizables en el vault, no sólo summarized.

## Least Useful Or Noisy Part

- What did not help: la superficie de la sesión no expone búsqueda por símbolo (Glob/Grep) y el hook denegó el `python -c` inline y la lectura del runbook del code scout con el literal `Outside immutable W1-q scope`.
- Why it was weak/noisy: sin búsqueda por símbolo, enumerar callers fue imposible y quedó como gap declarado; sin runbook, el procedimiento del scout tuvo que reconstruirse desde el contrato y la skill.
- Proposed cleanup: exponer búsqueda por símbolo de sólo lectura en el harness para el code scout inline-fallback, y un allowlist explícito para `python -m json.tool` sobre rutas propias (no `python -c` libre).

## Missing Support

- Problem not solved by Sistema 1: validar que un camino **nuevo** de código cubre el dominio completo (no sólo el rol principal) no tiene herramienta: dependió de la lectura crítica del supervisor.
- How Sistema 1 could help next time: un checklist de revisión para "vía nueva sobre contrato existente" que fuerce enumerar las ramas (rols, lados, estados de la entrada) y sus guards.
- Suggested artifact type: checklist de revisión de producto (runbook corto), no memoria.

## Retrieval Feedback

- Useful query or source: `[[Research — Fee Formula Documentary W1-p 2026-10-31]]` (fórmula, unidades, precisión, cobro, roles y límites) y las fuentes exactas del repo (`internal/regimes/schedule.go`, `internal/economics/scheduled.go`, `internal/foundation/{decimal,units,errors}.go`) fueron suficientes y específicas.
- Missing context: faltaba el runbook operativo del code scout por la denegación del hook.
- Duplicate/noisy result: ninguno relevante; se evitó el discovery repetido del vault por instrucción de alcance.
- Better future query: para un encargo de conformidad, pedir el ledger de fuentes con Extractos y no sólo el resumen de la investigación previa.

## Skill Feedback

- Skill that worked well: `agents-os-code-scout` (el mapa de contrato, callers y tests side effects fue el insumo directo del seam) y `agents-os-agent-run-register` (el registro de crew resolvió la atribución superficie×modelo sin ambigüedad).
- Skill that was confusing: `agents-os-session-close` y su delta classifier: el encargo pedía un conjunto explícito de ocho notas (informe, resumen, feedback, run, log, feedback de scout y dos deltas de entidad), que es más que "persistir por delta"; la skill no dice cómo ejecutar un cierre por mandato con rutas prescritas.
- Trigger/routing gap: falta una vía declarada para "cierre por mandato con rutas canónicas prescritas" que no colisione con la regla de no cerrar automáticamente.
- Suggested contract change: documentar en la skill de cierre que un mandato explícito con rutas concretas prevalece sobre el delta classifier, y que la ejecución parcial se acepta con el delta ya autorizado.

## Template Feedback

- Template used: `80-agents/templates/{session-summary,session-feedback,agent-run,change-log}.md` y `70-templates/doc.md`, materializados con `materialize_schema_note.py`.
- Field that helped: `agent_surface`/`agent_model`/`model_source` del agent run, y `source_feedbacks` del change log.
- Field that felt redundant: `application` vacío en notas de sesión y en el agent run de un proyecto sin app.
- Missing field: el agent run no tiene un campo para "evidencia externa" (aprobación del supervisor o hashes verificados por el Root), que fue material en esta entrega.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? sí — sólo la nota global de continuidad operativa, como exige el bootstrap.
- ¿Qué valor operativo aportó para esta sesión (continuidad, detalles crudos, advertencias)? aportó la advertencia de leer estado durable antes de repetir efectos laterales y de no confundir un comando verde con el resultado real: se aplicó al no repetir corridas para obtener verde y al no afirmar una línea base roja que nunca se ejecutó.
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna? no: el único delta transferible (denegaciones del hook y ausencia de búsqueda por símbolo) es específico de este harness y pertenece al feedback público de esta sesión, no a la memoria interna global.
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad? 4 — es útil para el comportamiento transferible, pero no debe recibir estado de proyecto ni cifras de un turno.

## Pain Pattern Candidate

- Is this likely to repeat? yes — el patrón "una rama de rol salta los guards del dominio" es estructural en cualquier vía que bifurque por rol.
- Suggested severity: medium
- Candidate owner: supervisor de revisión de fuente
- Promote to L3 memory? defer — la lección es de revisión de producto, no de comportamiento del agente; queda como checklist candidato.

## One Next Improvement

- Convertir la enumeración de guards por rama (rol × lado × dominio) en una línea obligatoria de la revisión de fuente de las vías nuevas sobre contratos existentes, para que el defecto MAKER se detecte por criterio y no por lectura lucky.

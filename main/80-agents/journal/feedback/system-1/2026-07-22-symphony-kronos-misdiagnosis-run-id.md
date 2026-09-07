---
type: feedback
scope: session
created: "2026-07-22"
updated: "2026-07-22"
area: "[[Symphony Portal]]"
project: "[[Symphony]]"
entities:
  - "[[StrategyQuant X]]"
  - "[[sqx-instrument-sync]]"
related: []
aliases: []
agent: Claude Code (GLM-5.2)
session_goal: Diagnosticar fallo recurrente de Kronos en dos wfs de EchoForge
source_session: "2026-07-22-2022-symphony-kronos-sync-instruments-misdiagnosis"
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/symphony
  - agent/system1
---

# Session Feedback - 2026-07-22 - Symphony Kronos misdiagnosis run_id

## Context

- Agent: Claude Code (GLM-5.2).
- Session goal: Diagnosticar por qué Kronos seguía fallando dos wfs
  concretos tras los fixes de la sesión anterior.
- Main entity: [[Symphony]] / [[StrategyQuant X]] / [[sqx-instrument-sync]].
- Skills used: worker-troubleshooting, worker-ssh, echo-forge-testing,
  agents-os-session-close. (agents-os-bootstrap implícito.)
- Retrieval mode: skills + scripts `scratch/` + Temporal client + SSH
  directo a workers + MongoDB directo.
- Artifacts changed: ninguno del repo Symphony. Solo archivos scratch
  nuevos y memoria Obsidian.

## Scores

- Diagnosis accuracy: 2/5 — diagnóstico incorrecto (culpé a run_id,
  el usuario corrigió: era sync de instrumentos).
- Tool usage efficiency: 3/5 — usé bien SSH y Temporal, pero me
  concentré en MongoDB cuando la UI de SQX era la fuente obvia de
  verdad.
- Session pacing: 3/5 — muchas consultas, poca hipótesis
  estratégica.
- User friction: 2/5 — el usuario se frustró con un diagnóstico
  equivocado.

## What Worked Well

- Diagnóstico operativo (estado del servicio, versión, permisos)
  correcto y rápido.
- Identificación de que las dos waves corrían 100% en Kronos.
- Identificación de la actividad exacta que fallaba
  (`classify_and_rank`, evento 17→19) y el error exacto
  (`ErrMetadataMissing` non-retryable).
- Entrega final del prompt maestro para reescribir la skill fue
  completa y fundada en las brechas reales detectadas.

## What Was Hard

- **Confirmation bias**: una vez que vi `ErrMetadataMissing` y recordé
  el BUG-001 documentado en el backlog, encajé todo en esa hipótesis.
  No consideré seriamente que el builder simplemente no hubiera
  escrito nada.
- **Ceguera a UI**: el usuario descubrió la causa en la UI de SQX
  ("unresolved resources", `XAUUSD_darwinex` ausente). Yo no pensé en
  sugerir mirar la UI como fuente de diagnóstico. La UI de SQX no
  estaba en mi set de herramientas mentales.
- **Sobre-enfoque en datos**: pasé demasiado tiempo escarbando
  MongoDB cuando un `find ~/sqx/user/data -iname "*XAUUSD*"`
  comparado entre hosts habría revelado el problema en segundos.

- Observation: cuando un síntoma aparece en un solo worker, la raíz
  suele ser de datos/estado, no de código compartido.
- Why it was hard: el código compartido invita a buscar bugs
  transversales. La asimetría entre workers apunta a datos locales.
- Proposed improvement: añadir al runbook mental "verificar
  dependencias de proyecto en disco antes de culpar a código".

## Most Useful Part Of Sistema 1

- What helped: el L1 previo
  `2026-07-22-symphony-kronos-builder-failures-and-fixes` ya había
  dejado el addendum diciendo "workspace state, misterio abierto".
  Esa pista indicó que el problema no estaba cerrado.
- Why it helped: previno repetir las mismas hipótesis ya rebutidas.
- Keep/change: keep. L1 con addendums es muy valioso para sesiones
  encadenadas.

## Least Useful Or Noisy Part

- What did not help: nada ruidoso en esta sesión. Todo lo que cargué
  fue relevante.
- Why it was weak/noisy: N/A.
- Proposed cleanup: N/A.

## Missing Support

- Problem not solved by Sistema 1: ninguna nota previa documentaba
  que la skill `sqx-instrument-sync` solo cubre `History/`. Ese gap
  es exactamente el tipo de cosa que debería ser un L3 known-error
  **antes** de que alguien tropiece con él.
- How Sistema 1 could help next time: tener un L3 known-error por
  skill/herramienta con gaps conocidos, no solo por bug de código.
- Suggested artifact type: known-error orientado a herramienta (lo
  creé en esta sesión como
  `sqx-instrument-sync-history-only-verification-gap`).

## Retrieval Feedback

- Useful query or source: `scratch/` scripts para introspectar
  Temporal. Muy eficientes.
- Missing context: ningún indice apuntaba a las brechas de
  `sqx-instrument-sync`. Tuve que leer la skill entera para verlas.
- Duplicate/noisy result: N/A.
- Better future query: "qué verifica la skill sqx-instrument-sync"
  debería poder responderse con un único explain de graphify.

## Skill Feedback

- Skill that worked well: worker-troubleshooting y worker-ssh.
  Comandos listos para usar, precisos.
- Skill that was confusing: ninguna. Pero `sqx-instrument-sync`
  está incompleta — su contrato de `EQUAL` es engañoso porque solo
  cubre `History/`.
- Trigger/routing gap: cuando el usuario dice "las correcciones a
  Kronos no funcionaron", la skill `sqx-instrument-sync` debería
  auto-sugerirse como verificación previa. Hoy no lo hace.
- Suggested contract change: añadir a la skill un prefacio "lo que
  esta skill NO verifica" para forzar al agente a complementar con
  diffs de `Symbols/`, `Datasources/`, etc.

## Template Feedback

- Template used: raw-session, session-feedback.
- Field that helped: `source_session` para linaje.
- Field that felt redundant: ninguna.
- Missing field: un campo "diagnosis outcome: correct/incorrect" que
  obligue a autocalificar.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al
  iniciar? **No**. Arranqué directo con skills de worker.
- ¿Qué valor operativo aportó para esta sesión (continuidad,
  detalles crudos, advertencias)? N/A porque no la consulté.
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo
  agente en la memoria interna? **Sí**, creado:
  `2026-07-22-symphony-kronos-instrument-sync-gap.md`.
- ¿Qué tan útil te resulta tener este espacio privado fuera de la
  vista directa del usuario (1-5) y cómo podemos mejorar su utilidad?
  5. Crítico. Mejora: que agents-os-bootstrap lo recuerde de forma
  más prominente.

## Pain Pattern Candidate

- Is this likely to repeat? **yes**. Cualquier worker recién
  provisionado o re-imagingado puede tener desync de instrumentos.
- Suggested severity: **high**. Bloquea producción, se confunde con
  bugs de código.
- Candidate owner: rjara (mejora de skill).
- Promote to L3 memory? **done**. Se creó el L3 known-error
  `sqx-instrument-sync-history-only-verification-gap`.

## One Next Improvement

Agregar a agents-os-bootstrap un checklist "verifica memoria
interna" antes de empezar cualquier diagnóstico. Evitaría
re-diagnosticar cosas ya documentadas como pendientes.

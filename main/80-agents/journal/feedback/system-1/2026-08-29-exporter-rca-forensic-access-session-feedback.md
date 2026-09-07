---
type: feedback
schema_version: 1
scope: session
created: 2026-08-29
updated: 2026-08-29
area: "[[Echo]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
  - "[[2026-08-29-exporter-double-execution-root-cause]]"
aliases: []
agent_surface: "[[Cursor]]"
agent_model: claude-opus-5
agent_run: "[[2026-08-29-cursor-claude-opus-5-exporter-double-execution-rca-top]]"
session_goal: RCA read-only de la doble ejecución de overview_exporter que bloqueó el E2E final 0.2.79
source_session: DURABLE-VERIFIED-READS-EXPORTER-DOUBLE-EXECUTION-RCA-TOP
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/agentsos
  - agent/system1
---

# Session Feedback - 2026-08-29 - exporter-rca-forensic-access

## Context

- Agent surface: Cursor (Claude Opus 5 + subagentes read-only)
- Session goal: determinar qué ejecución produjo el primer `metadata/export_run.json` del run bloqueado
- Skills used: agents-os-bootstrap, agents-os-session-close
- Retrieval mode: memoria de continuidad + known-error + rollout local de la sesión previa
- Artifacts changed: decisión RCA, known-error, checkpoint proyecto, continuidad, agent-run, change log, feedback

## What Complicated The Session Most

- Observation: el laboratorio completo estuvo inalcanzable durante toda la sesión (Temporal, MinIO, PostgreSQL, Mongo y los tres workers), no sólo PG/Mongo como en agosto 26. Una RCA declarada read-only quedó sin ninguna fuente viva.
- Why it was hard: la sesión que vivió el incidente tampoco pudo leer logs de worker (SSH sólo password, Loki sin streams), así que la evidencia más discriminante —qué host ejecutó el primer intento— nunca existió y ya no puede existir. El RCA se cerró igual porque la evidencia física del objeto y el código bastaron, pero por suerte, no por diseño.
- Proposed improvement: el acceso read-only a la observabilidad runtime lleva tres pedidos abiertos. El delta nuevo es que la captura debe ocurrir **durante** el incidente: un E2E que falla debería volcar logs de worker y el `attempt` de las activities antes de que la evidencia se vuelva irrecuperable.

## Most Useful Part Of Sistema 1

- What helped: recuperar el rollout local de la sesión ZCode previa como fuente forense. Conservaba el historial Temporal completo y el cuerpo real del objeto en conflicto.
- Why it helped: sin eso el RCA habría quedado BLOCKED; con eso quedó CLOSED con causa raíz demostrada.
- Keep/change: keep, y elevarlo a reflejo — antes de declarar evidencia perdida, revisar los rollouts de las superficies usadas ese día.

## Least Useful Or Noisy Part

- What did not help: el known-error previo afirmaba «sin `ActivityTaskStarted`» y `attempt=1`; ambas eran inferencias presentadas como hechos y orientaron la investigación hacia infraestructura durante la primera mitad de la sesión.
- Proposed cleanup: ya corregido en la nota. Criterio a mantener: marcar explícitamente qué es inferencia cuando la herramienta que iba a medirlo falló.

## Missing Support

- Problem not solved by Sistema 1: captura forense automática en el momento del fallo del E2E.
- Suggested artifact type: runbook de recolección post-mortem del entorno durable.

## Retrieval Feedback

- Useful query or source: known-error + memoria de continuidad dieron el cold start exacto; el rollout local dio la evidencia dura.
- Missing context: ninguna de las notas distinguía inferencia de observación.

## Skill Feedback

- Skill that worked well: agents-os-bootstrap; agents-os-session-close (delta classifier).
- Suggested contract change: en notas de known-error, exigir que las afirmaciones inferidas se marquen como tales.

## Template Feedback

- Template used: feedback (copiado del canónico del 2026-08-26; `session_feedback` no resuelve en `materialize_schema_note.py`)
- Missing field: —

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna al iniciar? sí.
- Valor operativo: continuidad completa del track durable y del E2E bloqueado sin releer el proyecto.
- ¿Dejaste mensaje para el próximo agente? sí — checkpoint del RCA con causa raíz, descartes y NEXT EXACT.
- Utilidad del espacio privado (1-5): 5.

## Pain Pattern Candidate

- Is this likely to repeat? yes — tercera ocurrencia del mismo patrón.
- Suggested severity: high
- Candidate owner: proceso de certificación E2E (repo), no Sistema 1
- Promote to L3 memory? yes — «una afirmación que la herramienta de medición no llegó a producir debe registrarse como inferencia explícita, no como hecho; un RCA posterior heredará el error y perseguirá la hipótesis equivocada».

## One Next Improvement

- Volcado forense automático al fallar un E2E: historial Temporal con `attempt` por activity, logs de los workers involucrados y stat de los objetos en conflicto, persistidos junto a la evidencia del run.

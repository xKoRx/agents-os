---
type: feedback
schema_version: 1
scope: session
created: 2026-09-20
updated: 2026-09-20
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run: "[[2026-09-20-zcode-glm-5.3-flash-f3-hardening]]"
session_goal: "F3 Security Hardening del writer Loom (POC aislada): contención estructural por dirfd, journal de transacciones, validación adversarial independiente, contrato de integración"
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

# Session Feedback - 2026-09-20 - loom-f3-hardening

## Context

- Agent surface: [[ZCode]]
- Agent model: GLM-5.3-Flash
- Agent run: [[2026-09-20-zcode-glm-5.3-flash-f3-hardening]]
- Session goal: hardening de seguridad del writer F3 (POC aislada) hasta veredicto SECURITY_READY/PARTIAL/BLOCKED con validación adversarial independiente
- Main entity: [[Loom]]
- Skills used: agents-os-bootstrap, agents-os-context-retrieval (implícito), agents-os-agent-run-register, agents-os-session-feedback, agents-os-session-close
- Retrieval mode: búsqueda enfocada sobre el repo (git/lectura directa); Graphify no requerido (trabajo en repo externo)
- Artifacts changed: rama aislada feature/f3-writer-poc (78a8a23 + cfa0ebc), specs FEAT-F3-HARDENING y FEAT-F3-INTEGRATION, [[Loom]] (estado/bitácora), agent-run, change_log, esta feedback

## Scores

Use 1-5, where 1 is poor and 5 is excellent.

- Startup clarity: 5
- Retrieval usefulness: 4
- Skill fit: 5
- Template fit: 4
- Closeout friction: 4
- Overall confidence: 5

## What Complicated The Session Most

- Observation: basura acumulada de escrituras interrumpidas en notas del vault (10-projects/Personal/Loom/: Loom.md.tmp.840471.f2bc33dfdf65, Loom — Foundation v0.1.md.tmp.153247.b7d38be57ecb y otros .tmp.* hermanos): artefactos parciales de sesiones previas que ninguna regla de higiene detecta ni limpia.
- Why it was hard: son archivos de Sistema 2 que no se pueden borrar sin autorización del owner y confunden (parecen salidas del writer POC cuando son restos de tooling de edición).
- Proposed improvement: regla de higiene (agents-os-hygiene-review) que detecte `*.tmp.<pid>.<hex>` huérfanos en notas canónicas y proponga su limpieza; el patrón es reconocible por regex.

## Most Useful Part Of Sistema 1

- What helped: el materializador canónico (materialize_schema_note.py) para agent_run/change_log/feedback: cero dudas de frontmatter.
- Why it helped: la constitución prohíbe copiar templates a mano; el script deja la puerta de validación ya resuelta.
- Keep: tal cual; documentar mejor que validate_schema_contract.py valida el CONTRATO por tipo, no un archivo concreto.

## Least Useful Or Noisy Part

- What did not help: INDEX.md de skills cargado completo en cold start (~80 líneas de tabla) para una sesión que usó 3 skills.
- Why it was weak/noisy: el costo es estable y bajo, pero la sesión de coding puro apenas consume el catálogo.
- Proposed cleanup: ninguno urgente; el budget soft ya lo cubre.

## Missing Support

- Problem not solved by Sistema 1: no hay convención registrada para conservar la EVIDENCIA de repros de auditorías adversariales que vive en /tmp (los labs del revisor se pierden al reiniciar; esta vez el repo sólo archiva los outputs clave).
- How Sistema 1 could help next time: regla en agents-os-agent-project-workflow para copiar los repros ejecutables del auditor a specs/<FEAT>/evidence/adversarial/ cuando el veredicto depende de ellos.
- Suggested artifact type: convención documental (no tipo nuevo).

## Retrieval Feedback

- Useful query or source: memoria de proyecto (MEMORY.md del harness) + nota del proyecto [[Loom]]: reconstituyeron el estado de la POC en una lectura.
- Missing context: el leftover .tmp.* hizo dudar un momento si la POC había escrito al vault real; la nota del proyecto no dice que esas basuras son del tooling de edición.
- Duplicate/noisy result: ninguno.
- Better future query: n/a

## Skill Feedback

- Skill that worked well: agents-os-agent-run-register (materializar + convención de nombre).
- Skill that was confusing: agents-os-session-feedback con request explícito del owner en sesión limpia de AGENTS OS pero con fricción real de herramientas: la regla event-driven y la petición explícita conviven bien, pero el skill asume que feedback = fricción de AGENTS OS; la fricción aquí fue del entorno de trabajo (vault hygiene), no del sistema.
- Trigger/routing gap: ninguno bloqueante.
- Suggested contract change: permitir explícitamente feedback de fricción del ENTORNO (vault/repos/harness) además del de AGENTS OS interno.

## Template Feedback

- Template used: session-feedback (este), agent-run, change_log.
- Field that helped: agent_run enlazado en feedback (trazabilidad directa).
- Field that felt redundant: scoring de 6 dimensiones para sesiones de un solo mandato (quedó honesto pero forzado).
- Missing field: ninguno.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? sí (nota global always-load de continuidad).
- ¿Qué valor operativo aportó para esta sesión? los comportamientos transferibles (leer estado durable antes de repetir efectos; fail closed ante contradicción) calzaron exactamente con el mandato de seguridad; reforzó decisiones sin costo de búsqueda.
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna? no: el estado vive en la nota del proyecto y en los specs del repo (una sola fuente por hecho).
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad? 4; útil para lecciones cross-dominio, no para estado de proyecto (ahí las notas de proyecto ganan).

## Pain Pattern Candidate

- Is this likely to repeat? yes (los .tmp.* llevan varias sesiones acumulándose).
- Suggested severity: low
- Candidate owner: agents-os-hygiene-review
- Promote to L3 memory? defer (primero regla de detección en higiene; si se repite tras regla, promover).

## One Next Improvement

- Añadir a agents-os-hygiene-review un detector de `*.tmp.<pid>.<hex>` en notas canónicas del vault con propuesta de limpieza al owner.

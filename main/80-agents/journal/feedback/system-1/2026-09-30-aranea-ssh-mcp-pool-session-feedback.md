---
type: feedback
schema_version: 1
scope: session
created: 2026-09-30
updated: "2026-09-30"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[aranea-ssh-mcp]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run: "[[2026-09-30-zcode-glm-5.3-flash-d6-ninjatrader-c0]]"
session_goal: D6 C0 — certificación física NinjaTrader/Tradovate (Echo Futures)
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

# Session Feedback - 2026-09-30 - aranea-ssh-mcp pool agotado (recurrencia)

## Context

- Agent surface: [[ZCode]]
- Agent model: GLM-5.3-Flash (host)
- Agent run: [[2026-09-30-zcode-glm-5.3-flash-d6-ninjatrader-c0]]
- Session goal: certificación física C0 de NinjaTrader/Tradovate para Echo Futures D6
- Main entity: [[Echo Futures]]
- Skills used: agents-os-bootstrap, aranea-agent-dev (router), runbook aranea-ssh-mcp, runbook aranea-mcp-capability-plane
- Retrieval mode: vault lectura directa (bootstrap + runbooks); sin Graphify query
- Artifacts changed: artifact C0 Echo Futures; agent_run; esta feedback; delta en nota de proyecto

## Scores

- Startup clarity: 5
- Retrieval usefulness: 4
- Skill fit: 5
- Template fit: 4
- Closeout friction: 4
- Overall confidence: 4

## What Complicated The Session Most

- Observation: el plano `aranea-ssh` (:3000) estaba con pool de 64 sesiones agotado otra vez (503 + `/status` 200 `connections:[]`); obligó a `docker restart ssh-mcp` por management path antes de poder trabajar, cortando cualquier sesión MCP huérfana de otros consumidores.
- Why it was hard: la firma de pool agotado no distingue sesiones huérfanas de agentes legítimos en vuelo, y el restart es una mutación del appliance compartido; sin la receta exacta del runbook habría parecido "capability caída".
- Proposed improvement: TTL/límite de vida de sesiones MCP server-side (idle GC) o alerta when `connections:[]` con sesiones ≥ N por >X horas; hoy la única cura es restart manual recurrente.

## Most Useful Part Of Sistema 1

- What helped: el runbook [[aranea-ssh-mcp]] con la firma exacta del 503 (`connections:[]`), el orden de triage y el recovery documentado; el router aranea-agent-dev que obligó a leerlo antes de operar.
- Why it helped: convirtió un síntoma ambiguo en un procedimiento de 3 pasos con rollback; cero improvisación contra el appliance.
- Keep/change: keep; añadir al runbook la fecha de esta 2.ª ocurrencia documentada si vuelve a pasar.

## Least Useful Or Noisy Part

- What did not help: los nombres de tipo del materializador (`agent_run`/`feedback`) no son adivinables desde el nombre de template (`agent-run.md`); requerido un round-trip extra con resolve_schema_type.py.
- Why it was weak/noisy: inconsistencia guion-vs-katana menor, pero recurre en cada closeout nuevo.
- Proposed cleanup: aceptar el alias kebab-case en resolve_schema_type.py o listar los tipos válidos en el --help del materializador.

## Missing Support

- Problem not solved by Sistema 1: el cliente MCP raw-HTTP de esta superficie no soporta elicitation, así que todo comando no-safe en profiles operator con approval queda APPROVAL_UNAVAILABLE fail-closed — correcto, pero no está registrado como frontera por superficie en el runbook SSH (sólo aparece como anécdota en el triage 2026-09-26).
- How Sistema 1 could help next time: una línea en [[aranea-ssh-mcp]] por perfil: qué clase de comandos pasan sin elicitation y qué consumidor puede aprobarlos.
- Suggested artifact type: extensión de 2-3 líneas del runbook existente (no nota nueva).

## Retrieval Feedback

- Useful query or source: grep dirigido sobre 30-resources/aranea (topología, runbooks) resolvió dev-win/.132 y el runbook SSH sin leer carpetas amplias.
- Missing context: "win-dev" (nombre usado por el owner) no existe en el vault; sólo `dev-win`/.132. Un alias barato en la topología evitaría el round-trip de discovery.

## Context Efficiency

- context_high_water_mark: unknown (no expuesto por la superficie).
- main_context_growth_sources: lectura del contract de Echo Futures.md (56k tokens, vista parcial) y del preflight D6 completo; outputs de netstat/Get-ChildItem por MCP.
- avoidable_context_growth: la nota del proyecto es demasiado grande para el hot path; una sección D6 compacta al inicio habría evitado la lectura parcial larga.
- compaction_opportunity: sí — tras cerrar discovery/acceso y antes de escribir el artifact, un checkpoint durable (artifact ya escrito) habría permitido compaction sin perder autoridad.
- efficiency_assessment: REVIEW

### Optimization candidates

- change: añadir alias/cross-ref "win-dev = dev-win (.132)" en topología aranea; evidence: esta sesión gastó 4-5 probes en resolver el nombre; expected_impact: LOW; risk_to_quality: LOW.
- change: TTL/GC de sesiones MCP ssh server-side; evidence: pool agotado documentado 2.ª vez; expected_impact: MEDIUM; risk_to_quality: LOW.
- change: tipos válidos del materializador en --help; evidence: round-trip extra en cada closeout; expected_impact: LOW; risk_to_quality: LOW.

## Pain Pattern Candidate

- Pool del ssh-mcp sin GC de sesiones: recurrencia documentada (2026-09-18 y 2026-10-01) con la misma firma y la misma cura manual; merece promoción a known-error o fix server-side si vuelve.
- Refuerzo material (2026-10-01T03:33:09Z): un reinicio de `ssh-mcp` por un tercero cortó el poller de esta sesión a mitad de ventana y produjo 305 ticks vacíos que podrían leerse como "NT desconectado" — sólo el puerto local persistente + `docker inspect StartedAt` lo desmintieron. Los monitores largos sobre este plano deben registrar el StartedAt del contenedor como parte de su evidencia o terminar interpretando cortes ajenos como eventos del target.

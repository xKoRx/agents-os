---
type: feedback
schema_version: 1
scope: session
created: 2026-09-16
updated: 2026-09-16
area: "[[Echo]]"
project: "[[Echo — E-05 Analytics Convergence A0]]"
entities:
  - "[[Echo — E-05 Analytics Convergence A0]]"
  - "[[AGENTS OS]]"
related:
  - "[[Echo — Live Platform V1]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: builtin:zai-coding-plan/GLM-5.3-Flash
agent_run:
session_goal: "Reanudar el rollout operacional E-05 en SHARED DEV (063 + Hasura + smoke GraphQL) bajo la enmienda Manager que retira 061 como precondición."
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

# Session Feedback - 2026-09-16 - echo-e05-shared-dev-rollout

## Context

- Agent surface: [[ZCode]]
- Agent model: builtin:zai-coding-plan/GLM-5.3-Flash
- Agent run: ninguno — sesión operacional (migración/metadata/smoke), sin segmentos de generación de código.
- Session goal: rollout 063+Hasura+smoke en SHARED DEV con `DEV_ROLLOUT_PASS`.
- Main entity: [[Echo — E-05 Analytics Convergence A0]]
- Skills used: agents-os-bootstrap, aranea-agent-dev, aranea-mcps-expert, runbooks aranea-postgres/hasura-mcp, agents-os-session-close.
- Retrieval mode: lectura focalizada (nota E-05, change log del bloqueo previo, runbooks MCP, source del backend Hasura MCP pinneado); sin Graphify CLI.
- Artifacts changed: nota E-05 (estado + bitácora + entregas), change log `2026-09-16-e05-shared-dev-rollout-pass.md`, este feedback. Cero commits en repos.

## Scores

Use 1-5, where 1 is poor and 5 is excellent.

- Startup clarity: 5
- Retrieval usefulness: 5
- Skill fit: 5
- Template fit: 4
- Closeout friction: 4
- Overall confidence: 5

## What Complicated The Session Most

- Observation: `export_metadata` del MCP Hasura (70,953B) excedió el presupuesto de render del cliente (50,000B) y `format: yaml` no compacta en el build desplegado, impidiendo componer el replace_metadata completo en contexto.
- Why it was hard: `apply_metadata` = `V2ReplaceMetadata` completo (verificado en source pinneado `9ba59f2`), así que aplicar el delta exigía el export íntegro; reconstruirlo a mano no era aceptable sobre metadata en vivo compartida.
- Proposed improvement: que el backend MCP ofrezca export compacto o paginado; entre tanto, la vía JSON-RPC directa al endpoint certificado con el bearer de capability local (documentada en el change log) es el workaround in-plane.

- Observation: `mcp_echo_dev_rw` no tiene CREATE en schema `echo`; la migración sólo podía ejecutarse como `echo_user`.
- Why it was hard: el runbook PostgreSQL MCP sugiere el MCP RW como canal natural de DEV; el DDL de migraciones queda fuera de su privilegio y el canal real fue `run_sql` del Hasura DEV admin (misma identidad `echo_user` que aplicó 062).
- Proposed improvement: anotar en [[aranea-postgres-mcp]]/[[aranea-hasura-mcp]] que las migrations de `echo` se aplican por `run_sql` DEV (o CI con admin secret), no por `aranea-postgres-rw`.

## Most Useful Part Of Sistema 1

- What helped: el change log del rollout bloqueado previo y los runbooks MCP con capabilities/authorities exactas.
- Why it helped: permitieron re-confirmar el preflight sin re-descubrir targets, y elegir mecanismos certificados a la primera.
- Keep/change: mantener el patrón change_log→reanudación; añadir los hallazgos de privilegio/naming al runbook si el patrón se repite.

## Least Useful Or Noisy Part

- What did not help: el smoke GraphQL inicial falló dos veces por naming default `echo_<tabla>` del `query_root` DEV antes de introspectar.
- Why it was weak/noisy: el naming no está documentado en el runbook Hasura ni en la nota E-05.
- Proposed cleanup: registrar el naming root-field DEV en el runbook Hasura para futuros smokes.

## Missing Support

- Problem not solved by Sistema 1: ninguna capability MCP ejecuta queries GraphQL role-scoped (el smoke readonly requirió curl dentro del contenedor vía `docker-echo-dev-operator`, con el admin secret expandido sólo dentro del contenedor).
- How Sistema 1 could help next time: una capability o tool certificada de "GraphQL probe readonly" eliminaría el desvío por el host.
- Suggested artifact type: extensión del runbook [[aranea-hasura-mcp]] con la receta actual (o capability nueva si se justifica).

## Retrieval Feedback

- Useful query or source: source de `cli/internal/mcp/handlers/metadata.go` @ `9ba59f2`, introspección `__type(query_root)`, y el change log `2026-09-16-e05-shared-dev-rollout-blocked.md`.
- Missing context: el runbook no documenta el límite de render del cliente ni la semántica replace de `apply_metadata`.
- Duplicate/noisy result: el exportMetadata duplica el contenido en la respuesta estructurada del cliente, duplicando el costo de contexto.
- Better future query: ver semántica de tools en el source del backend antes de usarlas sobre estado compartido.

## Skill Feedback

- Skill that worked well: aranea-mcps-expert + runbooks: ambiente antes que autoridad evitó tocar PROD en todo el rollout.
- Skill that was confusing: ninguna bloqueante.
- Trigger/routing gap: el runbook Hasura no cubre el flujo "aplicar yaml de metadata de un feature" end-to-end.
- Suggested contract change: añadir sección de operación "metadata apply por feature" al runbook Hasura (replace_metadata completo, presupuesto de render, vía JSON-RPC con bearer de capability).

## Template Feedback

- Template used: `session-feedback.md` materializado por contrato.
- Field that helped: separación fricción / missing support.
- Field that felt redundant: ninguna material.
- Missing field: ninguno.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? sí (nota global always-load; ubicación del repo Echo vía nota interna).
- ¿Qué valor operativo aportó para esta sesión (continuidad, detalles crudos, advertencias)? resolvió la ubicación canónica `~/go/src/github.com/xKoRx/echo` y las reglas de verificación de outcome real.
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna? no; el delta durable quedó en la nota E-05 y el change log.
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad? 5.

## Pain Pattern Candidate

- Is this likely to repeat? yes — el rollout 061 de E-03 a SHARED DEV enfrentará los mismos tres obstáculos (privilegio CREATE, export>render, naming GraphQL).
- Suggested severity: medium
- Candidate owner: [[aranea-hasura-mcp]] / [[aranea-postgres-mcp]] runbooks
- Promote to L3 memory? defer — está documentado en el change log; promover a runbook cuando se confirme el patrón en el rollout 061.

## One Next Improvement

- Documentar en los runbooks aranea el flujo real de metadata apply por feature (replace completo, límite de render, JSON-RPC con bearer de capability, naming `echo_<tabla>`) antes del rollout de 061.

## Context Efficiency

- `context_high_water_mark`: medio-alto (dos exportMetadata truncados de ~50k tokens de render cada uno).
- `efficiency_assessment`: GOOD — el workaround JSON-RPC archivo-a-archivo evitó reconstrucción manual de metadata y múltiples reintentos.
- `avoidable_context_growth`: los dos exports truncados iniciales; con export compacto del backend no habrían ocurrido.

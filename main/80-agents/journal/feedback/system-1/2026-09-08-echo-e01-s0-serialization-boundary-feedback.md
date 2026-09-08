---
type: feedback
schema_version: 1
scope: session
created: 2026-09-08
updated: 2026-09-08
area: "[[Echo]]"
project: "[[Echo — E-01 Canonical SDK Foundation S0]]"
entities:
  - "[[Echo — Live Platform V1]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run: "[[2026-09-08-zcode-glm-5.3-flash-echo-e01-s0-serialization-boundary]]"
session_goal: "Corrección 3: cerrar el boundary value→encoding/json→C() para Marshaler/TextMarshaler (value y pointer receiver)"
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/echo
  - agent/system1
---

# Session Feedback - 2026-09-08 - echo e01 s0 serialization boundary

## Context

- Agent surface: [[ZCode]] · model GLM-5.3-Flash (host). Run: [[2026-09-08-zcode-glm-5.3-flash-echo-e01-s0-serialization-boundary]].
- Session goal: el pre-walk UTF-8 reconocía `json.Marshaler` sólo con kind `Struct`; cerrar el boundary para pointer receivers, TextMarshaler, map keys y promoción de embebidos, sin reimplementar encoding/json.
- Main entity: [[Echo — E-01 Canonical SDK Foundation S0]]
- Skills used: agents-os-session-close, agents-os-agent-run-register (cierre explícito pedido por el prompt).
- Retrieval mode: cold start con bootstrap estándar; sin retrieval de vault más allá del estado E-01.
- Artifacts changed: 2 archivos `v3/sdk/contracts/wire/**` (commit `aafa2f62`), bitácora E-01, change_log consolidado, agent run, esta nota.

## Scores

- Startup clarity: 5
- Retrieval usefulness: 5
- Skill fit: 5
- Template fit: 4
- Closeout friction: 5
- Overall confidence: 5

## What Complicated The Session Most

- Observation: la semántica real de encoding/json es contraintuitiva y no se deduce de la doc: un struct con `MarshalJSON` en `*T` NO usa el método si el valor no es addressable (top-level por valor, valores de map, contenido de interfaz descienden a campos); los method sets promueven marshalers embebidos y reemplazan el struct completo; `RawMessage` implementa con value receiver.
- Why it was hard: el defecto previo nació de razonar con la doc conceptual (kind `Struct` + `Implements`); replicar eso habría introducido otra divergencia.
- Proposed improvement: para cualquier prevalidación que espeje un encoder, ejecutar primero un programa de prueba desechable contra stdlib en el toolchain exacto y convertir cada comportamiento observado en un test de paridad antes de diseñar el walk.

## Most Useful Part Of Sistema 1

- What helped: el patrón one-shot del manager: baseline exacto, allowed-files, contrato enumerado de casos y handoff con formato fijo.
- Why it helped: la lista de 13 casos funcionó como matriz de aceptación directa; cada caso se convirtió 1:1 en test nominal.
- Keep/change: mantener el contrato enumerado; añadir que los casos se redacten como comportamiento observable (input → output/error) y no como conceptos.

## Least Useful Or Noisy Part

- What did not help: nada material esta sesión.
- Why it was weak/noisy: -
- Proposed cleanup: -

## Missing Support

- Problem not solved by Sistema 1: -
- How Sistema 1 could help next time: -
- Suggested artifact type: -

## Retrieval Feedback

- Useful query or source: la fuente de verdad fue `GOROOT/src/encoding/json/encode.go` del toolchain (go1.25.5), no el vault.
- Missing context: -
- Duplicate/noisy result: -
- Better future query: -

## Skill Feedback

- Skill that worked well: agents-os-agent-run-register con template materializado, sin fricción.
- Skill that was confusing: -
- Trigger/routing gap: -
- Suggested contract change: -

## Template Feedback

- Template used: session-feedback + agent-run vía materialize_schema_note.py.
- Field that helped: `agent_run` enlazado en feedback mantiene la cadena evidencia→fricción.
- Field that felt redundant: secciones vacías (Retrieval/Skill/Template) en sesiones sin hallazgos; se dejaron con `-` explícito.
- Missing field: -

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? sí (nota global always-load del bootstrap).
- ¿Qué valor operativo aportó para esta sesión (continuidad, detalles crudos, advertencias)? la regla "verificar el outcome en la capa que posee la semántica" aplicó directo: la capa que posee la semántica era stdlib, no la doc.
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna? no; el delta quedó en bitácora E-01 y change_log.
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad? 5.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: medium
- Candidate owner: [[Echo — E-01 Canonical SDK Foundation S0]] / futuras prevalidaciones espejo de encoders.
- Promote to L3 memory? defer — la lección cabe en el feedback y en la bitácora; si aparece una cuarta divergencia encoding/json, promover regla "probar stdlib antes de diseñar walks espejo".

## One Next Improvement

- -

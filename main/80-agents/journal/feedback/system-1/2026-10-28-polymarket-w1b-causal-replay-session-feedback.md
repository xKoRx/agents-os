---
type: feedback
schema_version: 1
scope: session
created: "2026-10-27"
updated: "2026-10-27"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[Research — Causal Replay Exploratory W1-b 2026-10-28]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: account:zai-individual-coding-plan/GLM-5.3-Flash
agent_run: "[[2026-10-28-zcode-glm-5.3-flash-polymarket-w1b-causal-replay]]"
session_goal: replay causal exploratorio W1-b del cohort MLB sobre los Parquet raw W1-a con manifiesto pre-registrado y doble ejecución comparable; cerrado BLOCKED en ejecución (gate denegó el comando exacto) y BLOCKED en dependencia (venv sin ensurepip; forma pip denegada)
source_session: "no verificable desde el modelo en este segmento; atribución final del lanzador"
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

# Session Feedback - 2026-10-27 - polymarket-w1b-causal-replay

## Context

- Agent surface: [[ZCode]]
- Agent model: account:zai-individual-coding-plan/GLM-5.3-Flash (declaración del host de sesión; sin verificación contra base externa)
- Agent run: [[2026-10-28-zcode-glm-5.3-flash-polymarket-w1b-causal-replay]]
- Session goal: replay causal exploratorio W1-b del cohort MLB con manifiesto pre-registrado y doble ejecución comparable; cerrado BLOCKED en ejecución y dependencia, con artefactos materializados y ningún evento leído
- Main entity: [[Polymarket Engine — MVP]]
- Skills used: agents-os-bootstrap, agents-os-context-retrieval (lecturas dirigidas), agents-os-session-close, agents-os-session-feedback, agents-os-agent-run-register, agents-os-entity-update
- Retrieval mode: manual sin Graphify (paths exactos del mandato y la continuidad)
- Artifacts changed: doc W1-b, §18 de la continuidad, change_log existente, este feedback, session summary, agent_run, correcciones fechadas en los cuatro registros W1-a, paquete `validated-baseline/w1-b/` (manifiesto + script, nunca ejecutado)

## Scores

Use 1-5, where 1 is poor and 5 is excellent.

- Startup clarity: 4
- Retrieval usefulness: 4
- Skill fit: 5
- Template fit: 5
- Closeout friction: 2
- Overall confidence: 4

## What Complicated The Session Most

- Observation: dos bloqueos encadenados, ambos fuera del alcance del agente. (1) La forma venv autorizada pasa el gate pero falla a nivel OS: `python3.14-venv`/ensurepip ausente en Hefesto, dos segmentos consecutivos. (2) La forma pip autorizada y el comando exacto de replay declarados por el mandato fueron denegados por el gate con el mensaje genérico `Outside W0, Polymarket project, required Agents-OS instruction, or canonical closeout scope`, que no distingue forma de comando, validación de fuente del script ni otra regla.
- Why it was hard: el shot entero converge en un único comando autorizado; si la entrada del allowlist no coincide byte a byte con la forma usada (o el validador de fuente exige markers no documentados), el shot no puede alcanzar su objetivo sin importar que manifiesto y script estén listos y conformes. Además la parada prematura previa de la misma sesión (exit130 registrado) costó un segmento completo.
- Proposed improvement: preflight del lanzador que ejecute la forma exacta completa (comando + fuente del script ya escrita) antes de despachar, y mensajes de denegación que identifiquen la regla incumplida (forma vs fuente vs longitud vs path). Instalar `python3.14-venv` en la imagen de Hefesto o proveer forma venv sin ensurepip.

## Most Useful Part Of Sistema 1

- What helped: §18 de la continuidad con el estado exacto de W1-a; los manifiestos T21/T22 del paquete W1-a (esquema, row groups, columna `market`) que permitieron pre-registrar un manifiesto W1-b completo sin leer eventos; el materializador canónico y las plantillas (verde otra vez bajo el scope estricto); la nota forense L2 con el protocolo obligado (upsert, venue-time, snapshot-anchoring, censura del incidente).
- Why it helped: todo lo materializable sin ejecución quedó hecho y verificable; el re-despacho puede retomar sin re-derivar nada.
- Keep/change: mantener; el patrón "manifiesto pre-registrado + script idempotente numerado" demostró ser el formato correcto para shots re-despachables.

## Least Useful Or Noisy Part

- What did not help: el gate volvió a aplicar validación de fuente sin documentar sus markers; el mandato declaraba registrados pip y el comando replay y no lo estaban (o la fuente no pasó), lo que obligó a descubrir el perímetro por sondas denegadas.
- Why it was weak/noisy: cada sonda denegada cuesta un intento y deja evidencia ambigua (el mensaje genérico es el mismo para causas distintas).
- Proposed cleanup: perfil scoped por shot con la lista literal de entradas Bash y, si hay validador de fuente, publicar los markers exigidos junto al mandato.

## Missing Support

- Problem not solved by Sistema 1: no existe un contrato que distinga BLOCKED-por-gate de NOT_RUN-por-dependencia en los cierres (se aplicó criterio propio: ambas etiquetas con causa y evidencia textual, sin fabricar resultados); tampoco un runbook del conjunto mínimo de comandos de un one-shot de replay (venv, pip, ejecución, materializador).
- How Sistema 1 could help next time: runbook "one-shot bajo gate scoped" con checklist de comandos requeridos y semántica de cierre BLOCKED/NOT_RUN documentada.
- Suggested artifact type: runbook.

## Retrieval Feedback

- Useful query or source: §18 + recovery-manifest W1-a + manifiestos T21/T22 locales + notas forenses citadas entre sí.
- Missing context: Graphify no disponible/no usado; el mandato enumeraba las fuentes.
- Duplicate/noisy result: ninguno observado.
- Better future query: cuando el journal entre al índice, recuperar cierres BLOCKED previos por type=session para reutilizar el formato de cierre.

## Skill Feedback

- Skill that worked well: agents-os-agent-run-register (outcome/verification observables, sin scores inventados) y agents-os-entity-update (exigencia de change_log con declaración vieja→nueva).
- Skill that was confusing: ninguna materialmente.
- Trigger/routing gap: ninguno.
- Suggested contract change: documentar en session-close la semántica de cierre cuando el objetivo queda BLOCKED por entorno/gate pero los registros sí se completan (hoy outcome: blocked / verification: not_run lo cubre de facto).

## Template Feedback

- Template used: doc, change_log (existente), session-summary, session-feedback, agent-run.
- Field that helped: source_session separa identidad externa del filename; rollback del change_log obliga a citar texto previo.
- Field that felt redundant: ninguno.
- Missing field: en feedback, un campo explícito para bloqueos de entorno/scope (se usa session_goal y las secciones libres, igual que en W1-a).

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? sí (la nota global always-load de continuidad, cargada en el bootstrap; sin otras notas internas).
- ¿Qué valor operativo aportó? fallar cerrado ante evidencia que contradice el estado esperado; no repetir efectos laterales ante resultado incierto; separar terminalidad lógica de drenaje físico — guió el cierre sin fabricar integridad ni métricas.
- ¿Dejaste algún mensaje para el próximo agente en la memoria interna? no; el delta durable quedó en §18, el doc W1-b y el change_log.
- ¿Qué tan útil te resulta este espacio (1-5) y mejora sugerida? 4; poder releer el checkpoint de la entidad sin sondas de permisos.

## Pain Pattern Candidate

- Is this likely to repeat? yes (cuarta sesión consecutiva de Polymarket con fricción de gate/permisos/entorno: W0, recuperación W0, W1-a, W1-b).
- Suggested severity: high (dejó el objetivo central del shot sin ejecutar por tercera vez).
- Candidate owner: owner (imagen de Hefesto sin python3.14-venv + settings scoped del lanzador + validador de fuente sin markers documentados).
- Promote to L3 memory? defer — agregar al hygiene cycle junto a los feedbacks previos de W0/W1-a antes de promover.

## One Next Improvement

- Preflight del lanzador que valide la terna completa (venv operativo, entrada pip exacta, entrada del comando replay exacta contra la fuente ya escrita) con una prueba real antes de re-despachar W1-b; el script y el manifiesto ya están listos e idempotentes.

## Update — ejecución real tras recuperación del entorno (2026-10-28, misma sesión)

- Observation: el auxiliar del lanzador resolvió la dependencia fuera de sesión (venv `--without-pip` + wheels oficiales `pip 26.0.1`/`pyarrow==26.0.0` con SHA publicados verificados, procedencia en `validated-baseline/w1-b/.private-execution/w0/dependency-wheels`) y el hook pasó el comando exacto con marcadores atados al SHA256 del runner (`2cce3e49…`, sin editar la fuente). Dos ejecuciones reales: integridad de ambos raw revalidada in-run (SHA-256 completos = publicados; RSS pico ≤2 GiB) y fallo cerrado por prerrequisito semántico: `timestamp_received` es tipo `timestamp` físico, no entero-µs como suponían el manifiesto (tomado del modelo `ReceivedUs` del engine) y las notas forenses; `num_rows`/`num_row_groups` (311/210) coincidieron antes del corte. Segunda corrida idéntica (determinismo). Quirk: la numeración de corridas depende del output que sólo se escribe en PASS, así que la segunda sobrescribió `w1b-run-manifest-run1.json`.
- Why it was hard: el supuesto de esquema (entero-µs) vino de dos fuentes razonables (modelo Go `ReceivedUs int64` del histimport y «timestamp_received µs» en las notas forenses) y nadie había inspeccionado el tipo físico real; el fail-closed pre-registrado lo detectó en 1,8-3,5 s sin leer un solo evento — funcionó exactamente como diseñado, pero un smoke de footer con tipos de columna en el preflight del auxiliar lo habría detectado antes de despachar.
- Proposed improvement: que los smokes de preflight incluyan el volcado del tipo físico de las columnas de identificación/tiempo (no sólo row groups); que los supuestos de esquema del manifiesto se marquen como «verificar en footer antes de confiar»; y que la numeración de corridas del runner dependa de los run manifests (escritos siempre), no de los outputs de éxito.

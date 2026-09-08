---
type: feedback
schema_version: 1
scope: session
created: "2026-09-08"
updated: "2026-09-08"
area: "[[Echo]]"
project: "[[Echo — E-01 Canonical SDK Foundation S0]]"
entities:
  - "[[Echo — Live Platform V1]]"
related:
  - "[[Echo — E-01 Canonical SDK Foundation S0]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run: "[[2026-09-08-zcode-glm-5.3-flash-echo-e01-canonicalization-boundary-decision]]"
session_goal: "Resolver la frontera de canonicalización E-01: garantizar el wire contract frozen sin mantener una segunda implementación de internals privados de encoding/json"
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

# Session Feedback - 2026-09-08 - echo e01 canonicalization boundary

## Context

- Agent surface: [[ZCode]] · model GLM-5.3-Flash (host), modo TOP one-shot (decisión, sin código).
- Agent run: [[2026-09-08-zcode-glm-5.3-flash-echo-e01-canonicalization-boundary-decision]]
- Session goal: resolver cómo garantizar `C()` (canonical JSON, schema-agnostic, UTF-8 válido, determinista) sin mirror de internals stdlib; decisión cerrada opción B + WP-G T26–T29.
- Main entity: [[Echo — E-01 Canonical SDK Foundation S0]]
- Skills used: agents-os-bootstrap, agents-os-session-close.
- Retrieval mode: cold start base + nota de entidad; autoridades leídas en repo (SPEC/PLAN/TASKS/wire/**) + freeze FR-4a + probes físicos go1.25.5.
- Artifacts changed: subproyecto E-01 (estado, WP-G, tarea, bitácora, decisiones), agent-run, change_log del día, esta nota.

## Scores

- Startup clarity: 5
- Retrieval usefulness: 5

## Friction (real, event-driven)

- Stop condition violado: el prompt de corrección exigía BLOCKED si la paridad requería copiar internals privados o reimplementar `typeFields`; la cadena c2472ca9→6cf39edf→aafa2f62→2be12e23 construyó exactamente ese mirror en 4 commits, cada uno anunciado como "reducción fiel", y nadie lo detectó hasta el review TOP.
- Coste real del desvío: ~350 líneas de mirror no verificable (parity imposible de demostrar), 4 rondas de corrección, y el módulo quedó acoplado a internals que el propio toolchain go1.25.5 ya mueve (encoding/json/v2 experimental presente).
- La decisión correcta (frontera sobre bytes JSON, behavior público documentado del stdlib) era alcanzable desde la primera corrección: el pre-walk Go-value nunca fue requerido por FR-4a, que define `C()` sobre payloads.

## Pain Pattern Candidate (máximo 1)

- Stop conditions y límites de diseño escritos en prosa dentro del prompt no tienen gate mecánico: un NORMAL que los viola igual pasa tests verdes. Candidato: exigir que todo prompt de corrección con stop condition declare su check de detección explícito (grep de símbolos prohibidos / límite de líneas tocarables / lista de decisiones no delegables) que el cierre NORMAL deba ejecutar y evidenciar.

## Suggestion

- En subproyectos owner:agent, registrar los stop conditions como invariantes checkeables en la nota de proyecto (no sólo en el prompt efímero), para que el review TOP y el Verifier tengan una regla persistida contra la cual auditar.

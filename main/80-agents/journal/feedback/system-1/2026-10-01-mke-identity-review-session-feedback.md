---
type: feedback
schema_version: 1
scope: session
created: "2026-10-01"
updated: "2026-10-01"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run: "[[2026-10-01-zcode-glm53-mke-identity-adv-review]]"
session_goal: Adversarial review identidad MKE V2 (71b5a21) + cierre con feedback
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

# Session Feedback - 2026-10-01 - ZCode sandbox cwd reset fragiliza cd+git worktree

## Context

- Agent surface: [[ZCode]]
- Agent model: GLM-5.3-Flash
- Agent run: [[2026-10-01-zcode-glm53-mke-identity-adv-review]]
- Session goal: adversarial review identidad MKE V2 `71b5a21` + cierre con feedback pedido por el usuario
- Main entity: [[Multimodal Knowledge Engine]]
- Skills used: agents-os-bootstrap, agents-os-session-close, agents-os-agent-run-register, agents-os-session-feedback (leídos por path; ZCode Skill tool no resuelve skills del INDEX — ya documentado)
- Retrieval mode: bootstrap cold (constitución+perfil+continuidad+INDEX+registry) y lecturas enfocadas de la nota de proyecto; Graphify no requerido
- Artifacts changed: agent_run, feedback, change_log, nota de proyecto MKE

## Scores

- Startup clarity: 5
- Retrieval usefulness: 5
- Skill fit: 5
- Template fit: 4
- Closeout friction: 4
- Overall confidence: 5

## What Complicated The Session Most

- Observation: en un comando compuesto `mkdir X && cd X && git -C <repo> worktree add --detach wt <sha>`, el worktree aterrizó en la raíz del repo (`<repo>/wt`) en vez de `X/wt`, y el `cd wt` siguiente falló con "no such file or directory"; el sandbox de ZCode resetea el cwd del shell entre llamadas y el comportamiento de rutas relativas dentro del compuesto no fue el esperado.
- Why it was hard: el mensaje de git ("HEAD is now at…") sugería éxito en la ruta esperada; sólo `git worktree list` reveló la ubicación real. Dos intentos fallidos antes de localizar el worktree.
- Proposed improvement: convención documentada (o hook de constitución/memoria): en ZCode sandbox usar siempre paths absolutos para `git worktree add` y verificar con `git worktree list` inmediatamente; no confiar en `cd` persistente dentro de comandos compuestos.

## Most Useful Part Of Sistema 1

- What helped: la memoria del vault (`echo-dev-diagnosis-tooling-map`, `zcode-skill-tool-vault-skills`) y los agent-runs previos del mismo proyecto dieron el formato y los quirks conocidos sin re-descubrirlos.
- Why it helped: continuidad entre sesiones del mismo mandato (Shot 2/3 → remediation → review) con cero reconstrucción de contexto.
- Keep/change: keep; los agent-runs con sección "Aprendizaje" son especialmente reutilizables.

## Least Useful Or Noisy Part

- What did not help: nada ruidoso esta sesión; el INDEX de skills cargado en cold start no se usó más allá de routing a session-close (aceptable).
- Why it was weak/noisy: n/a.
- Proposed cleanup: n/a.

## Missing Support

- Problem not solved by Sistema 1: ningún gap de Sistema 1; la fricción fue del sandbox de ZCode, no del vault.
- How Sistema 1 could help next time: una nota L3 corta con las convenciones git-worktree/sandbox de ZCode evitaría repetir el tropiezo.
- Suggested artifact type: L3 memory (known-error/convención).

## Retrieval Feedback

- Useful query or source: lectura directa de la nota de proyecto y de la memoria MEMORY.md de ZCode.
- Missing context: nada.
- Duplicate/noisy result: nada.
- Better future query: n/a.

## Skill Feedback

- Skill that worked well: agents-os-session-close (delta classifier claro); agents-os-agent-run-register (template directo).
- Skill that was confusing: ninguno esta sesión.
- Trigger/routing gap: el ZCode Skill tool sigue sin resolver skills del INDEX (fallback por path funciona; ya documentado en memoria).
- Suggested contract change: ninguno.

## Template Feedback

- Template used: agent-run, session-feedback, change_log (via materialize_schema_note.py).
- Field that helped: `agent_run` en feedback enlaza evidencia de performance sin duplicar.
- Field that felt redundant: ninguna.
- Missing field: ninguna.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna al iniciar? sí (agents-os-operating-continuity, always-load).
- ¿Qué valor operativo aportó? verificación de estado durable antes de reintentar y separación baseline/delta — aplicada directo al protocolo de review.
- ¿Dejaste algún mensaje para el próximo agente? sí: estado del review en la nota de proyecto + agent-run; el fix del contador pertenece al implementador.
- ¿Útil el espacio privado (1-5)? 5.

## Pain Pattern Candidate

- Is this likely to repeat? yes (cada sesión que crea worktrees en ZCode sandbox).
- Suggested severity: low
- Candidate owner: system1 hygiene
- Promote to L3 memory? yes (convención: paths absolutos + verificación `git worktree list` en sandbox ZCode)

## One Next Improvement

- Registrar la convención sandbox/worktree como L3 compacta en la próxima higiene.

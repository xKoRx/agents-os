---
type: feedback
scope: session
created: 2026-07-23
updated: 2026-07-23
area: "[[Symphony]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[sqx-instrument-sync]]"
aliases: []
agent: Cursor (GLM-5.2)
session_goal: Reescribir skill + script de sync SQX para identidad total bit-a-bit
source_session: 2026-07-23-sqx-instrument-sync-v3-identidad-total
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

# Session Feedback - 2026-07-23 - sqx-instrument-sync-v3

## Context

- Agent: Cursor (GLM-5.2)
- Session goal: Reescribir `sqx-instrument-sync` para garantizar identidad bit-a-bit de `~/sqx/user/data` (incluye H2) entre Zeus/Hera/Kronos.
- Main entity: [[Symphony]] / `sqx-instrument-sync`
- Skills used: `worker-ssh`, `agents-os-bootstrap` (vía regla de usuario), `agents-os-session-close`.
- Retrieval mode: directo (entrada del usuario con referencias @archivos + sesión previa).
- Artifacts changed: `.agents/skills/sqx-instrument-sync/scripts/sync_user_data_zeus.sh`, `SKILL.md`, `RUNBOOK.md`.

## Scores

Use 1-5, where 1 is poor and 5 is excellent.

- Startup clarity: 4
- Retrieval usefulness: 4
- Skill fit: 4
- Template fit: 4
- Closeout friction: 4
- Overall confidence: 4

## What Complicated The Session Most

- Observation: `set -Eeuo pipefail` en bash interacciona mal con `grep -c` (falla con exit 1 al contar 0) y con funciones que devuelven valor por `echo` mientras imprimen logs por stdout.
- Why it was hard: el trap ERR disparaba abortos espurios en medio del diff. El `$(diff_manifest ...)` capturaba líneas de log como parte del valor de retorno, rompiendo la aritmética.
- Proposed improvement: documentar un patrón AGENTS OS para "devolver valor por stdout + loguear a stderr/archivo" en scripts bash (`emit()` helper que escribe solo a stderr/log). Sería un snippet reusable.

## Most Useful Part Of Sistema 1

- What helped: la skill `sqx-instrument-sync` previa (v2) dio contexto exacto del caso `XAUUSD_darwinex` y de las exclusiones runtime históricas.
- Why it helped: permitió rastrear por qué la versión anterior enmascaraba divergencias y justificar el cambio de contrato.
- Keep/change: keep. El feedback explícito del operador ("esto quedó mal") fue la señal más útil de toda la sesión.

## Least Useful Or Noisy Part

- What did not help: el system reminder de graphify aparece en cada tool call de shell. En una sesión puramente operacional (SSH a workers, script bash) donde no hay código Go que explorar, es ruido.
- Why it was weak/noisy: la skill actual vive en bash/markdown, no en el grafo de código Go. graphify no aporta nada aquí.
- Proposed cleanup: eximir el reminder de graphify cuando el cwd es `.agents/skills/` o cuando no hay archivos `.go` involucrados.

## Missing Support

- Problem not solved by Sistema 1: distinción entre proceso `symphony` worker y `sqcli` de SQX. Asumí que el worker activo impedía el sync y añadí un checkeo que el operador tuvo que corregir ("el worker activo no significa que SQX esté activo").
- How Sistema 1 could help next time: un known-error o learning sobre "qué procesos realmente bloquean el sync de `~/sqx/user/data`" evitaría repetir el falso positivo.
- Suggested artifact type: known-error en `80-agents/memory/public/known-errors/`.

## Retrieval Feedback

- Useful query or source: lectura directa de SKILL.md y script previos.
- Missing context: estado real del árbol `~/sqx/user/data` (tuvimos que mapearlo por SSH en runtime).
- Duplicate/noisy result: n/a.
- Better future query: n/a.

## Skill Feedback

- Skill that worked well: `worker-ssh` (pivoteo Zeus→Hera/Kronos claro y reusable).
- Skill that was confusing: ninguna.
- Trigger/routing gap: el feedback de graphify sigue apareciendo fuera de contexto (ver arriba).
- Suggested contract change: conditional graphify reminder.

## Template Feedback

- Template used: `raw-session.md`, `session-feedback.md`.
- Field that helped: `source_session` (separa ID externo del nombre humano).
- Field that felt redundant: nada.
- Missing field: quizás `ops_cluster` en raw-session para sesiones que tocan infraestructura real (workers, IPs, credenciales).

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna al iniciar? no (la sesión entró directo con contexto del operador).
- ¿Qué valor operativo aportó? n/a en esta sesión.
- ¿Dejaste algún mensaje para el próximo agente? sí, nota `2026-07-23-sqx-instrument-sync-v3-continuity.md` con hash del script, condiciones operacionales y próximos pasos.
- ¿Utilidad del espacio privado (1-5)? 4. Útil para señales de continuidad sin ruido en el vault público.

## Pain Pattern Candidate

- Is this likely to repeat? yes (la interacción `set -e` + `grep -c` + `echo` de retorno en bash se repite en cualquier script del estilo).
- Suggested severity: medium.
- Candidate owner: AGENTS OS.
- Promote to L3 memory? yes — candidato a learning o snippet de patrón bash.

## One Next Improvement

- Publicar un snippet/patrón AGENTS OS para scripts bash que devuelven valor por stdout y loguean por stderr (`emit()` + `log()` separados), para evitar el bug que costó 3 iteraciones en esta sesión.

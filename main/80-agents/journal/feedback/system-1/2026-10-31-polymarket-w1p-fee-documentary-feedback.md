---
type: feedback
schema_version: 1
scope: session
created: 2026-10-31
updated: 2026-10-31
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
entities:
  - "[[AGENTS OS]]"
  - "[[Polymarket Engine — MVP]]"
related:
  - "[[ZCode]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: minimax/MiniMax-M3.1-Flash
agent_run: "[[80-agents/journal/agent-runs/2026-10-31-zcode-minimax-m3.1-flash-polymarket-w1p-fee-documentary.md]]"
session_goal: W1-p — investigación documental de fuentes oficiales Polymarket sobre la fórmula de fee y el campo WS fee_rate_bps (as-of 2026-10-29)
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

# Session Feedback - 2026-10-31 - polymarket-w1p-fee-documentary

## Context

- Agent surface: [[ZCode]] (host `sqx-ulab-hefesto-0`).
- Agent model: `minimax/MiniMax-M3.1-Flash` (reportado por el host; sin fallback ni modelo alterno).
- Agent run: `2026-10-31-zcode-minimax-m3.1-flash-polymarket-w1p-fee-documentary.md`.
- Session goal: cerrar el paso documental de fee del mercado `5784455` con fuentes oficiales fechadas, sin capturas, sin código y sin tocar el gate de costes.
- Main entity: [[Polymarket Engine — MVP]] (área [[Personal]]; routing DEFAULT).
- Skills used: `agents-os-bootstrap`, `agents-os-context-retrieval`, `agents-os-code-scout` + `scout-contract` + runbook (inline-fallback), `agents-os-session-close`, `agents-os-session-feedback`, `agents-os-agent-run-register`, `agents-os-entity-update`, `materialize_schema_note.py`.
- Retrieval mode: lectura dirigida del vault (cold start con packs exactos ya inyectados) + WebFetch contra el índice oficial `docs.polymarket.com/llms.txt` y repos oficiales por API pública de GitHub.
- Artifacts changed: `validated-baseline/w1-p-fee-documentary-20261031/` (6 artefactos) y 8 notas/rutas del vault (informe nuevo + deltas en MVP y Continuidad + sesión + 2 feedbacks + agent run + change_log).

## Scores

- Startup clarity: 5
- Retrieval usefulness: 4
- Skill fit: 4
- Template fit: 4
- Closeout friction: 3
- Overall confidence: 4

## What Complicated The Session Most

- Observation: el hook de alcance denegó dos archivos que la propia allowlist de dominio permitiría (`raw.githubusercontent.com/Polymarket/ts-sdk/main/packages/client/src/actions/orders/estimate.ts` y `.../market.ts`, error literal `Outside immutable W1-p scope`), justo el código que calcularía la fee en el SDK oficial; además rechazó un `--dry-run` del materializador que no estaba en la forma exacta autorizada.
- Why it was hard: el código denegado era la lectura que habría cerrado el gap de la fórmula con exponente; sin él, esa parte queda como inferencia. Y el rechazo del `--dry-run` obligó a crear notas sin poder previsualizar la plantilla (riesgo de frontmatter incompleto, mitigado leyendo cada nota tras crearla).
- Proposed improvement: que el materializador acepte `--dry-run` como forma autorizada, y que el hook de alcance reporte qué URLs del allowlist de dominio quedan bloqueadas por el alcance, para que el principal sepa si puede aportarlas.

## Most Useful Part Of Sistema 1

- What helped: la secuencia canónica de cierre (`session-close` → `session-feedback` → `agent-run-register` → `entity-update` + `materialize_schema_note.py`) y el contrato de scout con su modo `inline-fallback` explícito.
- Why it helped: permitió cerrar sin inventar artefactos (no se creó L0/L1 extra ni memoria interna sin delta) y dejó el registro atribuible por superficie×modelo con outcome y verificación honestos ("investigación documental, no desarrollo ni tests").
- Keep/change: keep, sin cambios.

## Least Useful Or Noisy Part

- What did not help: los templates de feedback traen muchas secciones pensadas para sesiones de desarrollo (scores de sesión, commentary de memoria interna, nota Graphify) que en esta superficie acotada no aplican.
- Why it was weak/noisy: su llenado obliga a escribir "no aplica" en la mitad de la nota.
- Proposed cleanup: un template de feedback compacto para scouts/superficies acotadas (ya contemplado por el modo scout del contrato: bastaba `## Context` + bloque compacto).

## Missing Support

- Problem not solved by Sistema 1: no hay una forma canónica de registrar "evidencia de fuente externa" (URL + fecha propia + fecha de consulta + estado) dentro del vault; hoy quedó en un JSON de shot fuera del vault, y el ledger vive sólo en el artefacto del encargo.
- How Sistema 1 could help next time: un tipo `source_ledger` (o una sección estándar en `type: doc`) para documentos de investigación con fuentes externas, que haga explícita la separación entre evidencia directa, inferencia y claim no resuelto, y que NO se confunda con verdad canónica.
- Suggested artifact type: `type: doc` en `10-projects/<Área>/<Proyecto>/` con sección de fuentes, o un `type: research_note` nuevo si el Owner lo autoriza (esta sesión no crea taxonomía nueva por instrucción expresa).

## Retrieval Feedback

- Useful query or source: el índice oficial `docs.polymarket.com/llms.txt` como punto de entrada (evitó adivinar rutas); el changelog con fechas de vigencia; los cuerpos de contrato en `raw.githubusercontent.com/Polymarket/*` y los árboles de repos por `api.github.com/repos/Polymarket/*`.
- Missing context: la definición del sujeto de `fee_rate_bps`; la categoría/`rebateRate` del mercado `5784455`; el `MAX_FEE_RATE` desplegado el 29-10-2026.
- Duplicate/noisy result: el árbol recursivo de `ts-sdk` vino truncado, lo que obliga a no afirmar ausencia de "fee" en ese repo; los 404 de `Polymarket/{docs,polymarket-docs,exchange,exchange-core}` fueron ruido esperable.
- Better future query: partir de `llms.txt` y del changelog antes de cualquier árbol de repo; usar `contents` por directorio concreto cuando el árbol recursivo se trunca.

## Skill Feedback

- Skill that worked well: `agents-os-code-scout` + su runbook, aplicados inline: la secuencia identidad → reglas → fuentes → flujo → docs vs código → mapa congelado → feedback es exactamente la que ordenó esta tarea.
- Skill that was confusing: ninguno en lo estructural; la ambigüedad estuvo en el alcance de "código oficial" que el hook dejó pasar por dominio pero no por alcance.
- Trigger/routing gap: el contrato de scout no contempla explícitamente el caso "repos remotos vía WebFetch sin clonación", donde "fijar repo/ref/dirty" se traduce a "rama main consultada, sin tags, sin hashes de contenido".
- Suggested contract change: una línea en el runbook que, para repos remotos, sustituya "dirty" por "estado de la rama consultada + ausencia de hash de contenido" y declare el tree truncado como límite de cobertura.

## Template Feedback

- Template used: `80-agents/templates/session-feedback.md` (materializado) y `80-agents/templates/session-summary.md`.
- Field that helped: `agent_surface` + `agent_model` (obligan a atribuir modelo exacto y superficie canónica).
- Field that felt redundant: las secciones de scores y memoria interna en este tipo de sesión acotada.
- Missing field: un campo que registre explícitamente "denegaciones de herramienta" (URL + error literal), que en esta sesión fue evidencia de primer orden y hoy sólo queda en el artefacto del shot.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? sí — la nota global de continuidad, por el bootstrap obligatorio.
- ¿Qué valor operativo aportó para esta sesión (continuidad, detalles crudos, advertencias)? aportó la advertencia de no repetir efectos laterales ante resultado incierto y la regla de "resolver identidad desde la autoridad canónica", que evitó tratar el `fee_rate_bps` observado como identidad de negocio.
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna? no: no hubo delta durable interno (el estado del proyecto vive en sus notas); el informe y el ledger bastan.
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad? 4; útil como advertencia de método, poco útil para el contenido técnico, que debe quedar en el vault y en los artefactos del encargo.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: medium
- Candidate owner: Owner / responsable de hooks de alcance
- Promote to L3 memory? defer

## One Next Improvement

- Que los hooks de alcance enumeren explícitamente qué URLs del allowlist de dominio están bloqueadas (en vez de un error genérico `Outside immutable W1-p scope`), para que el principal pueda aportar esas páginas y el encargo documental no quede con un gap que no depende de la búsqueda.

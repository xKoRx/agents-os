---
type: feedback
schema_version: 1
scope: session
created: "2026-10-29"
updated: "2026-10-29"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
entities:
  - "[[Polymarket Engine]]"
related:
  - "[[2026-10-29-zcode-glm-5.3-flash-polymarket-w1g-economic-preregistration]]"
  - "[[2026-10-29-polymarket-w1g-economic-preregistration-summary]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: "account:zai-individual-coding-plan/GLM-5.3-Flash"
agent_run: "[[2026-10-29-zcode-glm-5.3-flash-polymarket-w1g-economic-preregistration]]"
session_goal: "W1-g: preregistro económico PE-005-R1 + paquete de adquisición mínima (especificación only) + correcciones W1-f + fees en fuentes primarias"
source_session: "W1-g one-shot ZCode × GLM-5.3-Flash Max"
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - agent/system1
---

# Session Feedback - 2026-10-29 - polymarket W1-g economic preregistration

## Context

- Agent surface: ZCode CLI en `sqx-ulab-hefesto-0` (perfil por-shot W1-g: Read/Glob/Grep declarados, WebFetch fuentes oficiales, Write/Edit canónicos, Bash mínimo).
- Agent model: `account:zai-individual-coding-plan/GLM-5.3-Flash`.
- Agent run: [[2026-10-29-zcode-glm-5.3-flash-polymarket-w1g-economic-preregistration]].
- Session goal: dos entregables sustantivos (preregistro económico ejecutable + paquete de adquisición en diseño) y correcciones W1-f sin repetir gates/tests/capturas.
- Main entity: [[Polymarket Engine]].
- Skills used: agents-os-bootstrap (cold start), materialize_schema_note.py (session/feedback/agent_run/doc).
- Retrieval mode: continuidad canónica + Read directo por referencias (sin Graphify: índice derivado no consultado en este shot).
- Artifacts changed: 3 notas nuevas W1-g, erratas en 2 notas W1-f, continuidad §18 (bullet 19 + siguiente paso), change_log, session/feedback/agent_run, OUT w1-g con recibos.

## Scores

Use 1-5, where 1 is poor and 5 is excellent.

- Startup clarity: 5
- Retrieval usefulness: 4
- Skill fit: 5
- Template fit: 4
- Closeout friction: 3
- Overall confidence: 5

## What Complicated The Session Most

- Observation: el perfil del shot declara herramientas Glob/Grep que NO existen en la superficie efectiva de este modelo, y el hook deniega `ls`/`find`/TodoWrite; el descubrimiento de archivos del vault tuvo que hacerse 100% por referencias dentro de la continuidad y prueba-y-error de Read.
- Why it was hard: sin Glob, verificar existencia/nombres de notas (p.ej. el consolidado PE-001…PE-030 en `30-resources/polymarket/`) requiere intentos; una lectura a esa ruta fue denegada por scope y la fuente del mecanismo se tomó de la fuente Go (primaria y suficiente, pero el path vault quedó sin verificar).
- Proposed improvement: que el perfil por-shot sólo declare herramientas existentes en la superficie, o que el hook permita un `ls` acotado al directorio del proyecto activo.

## Most Useful Part Of Sistema 1

- What helped: la continuidad Five-POC como índice viviente (paths exactos, hashes, lecciones de run-id y de gate) y el materializador canónico con dry-run.
- Why it helped: permitió descubrir todo el repo y los manifests sin inventar nombres y sin shell genérico.
- Keep/change: mantener; añadir en la continuidad un mini-índice de rutas canónicas del proyecto (nota padre, guía, consolidados) al final del §18.

## Least Useful Or Noisy Part

- What did not help: `AskUserQuestion`/`TodoWrite` bloqueados a nivel perfil en un shot one-shot larguísimo (el rastreo de progreso tuvo que vivir fuera de herramientas).
- Why it was weak/noisy: el bloqueo no evita trabajo pero sí quita trazabilidad intermedia.
- Proposed cleanup: para shots de investigación largos, permitir TodoWrite de sólo-lectura interna.

## Missing Support

- Problem not solved by Sistema 1: no existe un índice navegable de URLs de documentación Polymarket ya verificadas (cada shot re-404ea rutas adivinadas del schema WS/trades).
- How Sistema 1 could help next time: un recurso wiki `30-resources/polymarket/` con las URLs verificadas + fecha + clasificación VERIFIED/NOT_VERIFIED (la página existe como dominio wiki, este shot no pudo tocarla por scope).
- Suggested artifact type: página resource-wiki con `last_verified`.

## Retrieval Feedback

- Useful query or source: continuidad §18 bullets (W1-a…W1-f) como mapa de evidencias; `W1-C-MANIFEST.json` para formas shadow/compare ejecutadas reales.
- Missing context: ubicación exacta del "Edge Research Consolidado 2026-09-16" (fuente de las familias PE-001…PE-030); se trabajó sin él citando la fuente Go del engine.
- Duplicate/noisy result: no aplica (sin Graphify en el shot).
- Better future query: índice de rutas del proyecto en la continuidad.

## Skill Feedback

- Skill that worked well: agents-os-bootstrap (cold start mínimo suficiente) + materializer (dry-run antes de escribir evitó errores de ruta relativa vs absoluta: el materializador exige path vault-relativo).
- Skill that was confusing: ninguno nuevo; fricción menor: el materializador rechaza rutas absolutas aunque la sesión trabaje con absolutas en todo lo demás.
- Trigger/routing gap: no aplica.
- Suggested contract change: documentar en el contract que `materialize_schema_note.py` exige path relativo a VAULT_ROOT.

## Template Feedback

- Template used: doc (Sistema 2), session, feedback, agent_run, change_log existente.
- Field that helped: related/aliases/created-updated para trazabilidad entre las 3 notas W1-g.
- Field that felt redundant: `application` vacío en session/change_log para proyectos sin app.
- Missing field: en feedback, campo explícito "denegaciones de herramientas registradas" (aquí quedó en What Complicated).

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? sí (nota global always-load `agents-os-operating-continuity`).
- ¿Qué valor operativo aportó para esta sesión (continuidad, detalles crudos, advertencias)? reglas transferibles aplicadas: verificar estado durable ante incertidumbre, no repetir efectos laterales, fallar cerrado ante contradicción (usadas para las correcciones W1-f y el manejo de denegaciones).
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna? no (delta de proyecto vive en continuidad/canónicos; sin delta global durable).
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad? 4.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: medium
- Candidate owner: owner del perfil por-shot (lanzador).
- Promote to L3 memory? defer (acumular un shot más de evidencia sobre perfiles que declaran herramientas inexistentes).

## One Next Improvement

- Añadir al cierre de cada bullet de continuidad W-n una línea `Rutas canónicas:` con las 3–5 rutas más usadas del proyecto, para eliminar el descubrimiento por prueba-y-error en shots sin Glob.

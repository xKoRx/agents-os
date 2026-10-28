---
type: feedback
schema_version: 1
scope: session
created: 2026-10-28
updated: 2026-10-28
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
entities:
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
related:
  - "[[Research — Public Market Capture W1-d 2026-10-28]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: account:zai-individual-coding-plan/GLM-5.3-Flash
agent_run: "[[2026-10-28-zcode-glm-5.3-flash-polymarket-w1d-public-capture]]"
session_goal: W1-d continuación 3 — captura pública acotada one-shot
source_session: sess_409bd821-5e46-4f35-86bd-1a94aabecd22
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

# Session Feedback - 2026-10-28 - polymarket-w1d-public-capture

## Context

- Agent surface: [[ZCode]]
- Agent model: `account:zai-individual-coding-plan/GLM-5.3-Flash` (host-reported)
- Agent run: [[2026-10-28-zcode-glm-5.3-flash-polymarket-w1d-public-capture]]
- Session goal: aplicar candidatos W1-d, probar, seleccionar y capturar
- Main entity: [[Polymarket Engine — Continuidad Five-POC 2026-09-20]]
- Skills used: bootstrap (warm reuse), session-close, session-feedback, agent-run-register, materializador canónico
- Retrieval mode: normal (delta-only; bootstrap de la pasada 1 reutilizado, sin re-bootstrap retroactivo)
- Artifacts changed: checkout (extensión W1-d sin commit), preregistro v2, binario W1-d, 6 registros canónicos del vault

## Scores

Use 1-5, where 1 is poor and 5 is excellent.

- Startup clarity: 5
- Retrieval usefulness: 4
- Skill fit: 5
- Template fit: 5
- Closeout friction: 4
- Overall confidence: 4

## What Complicated The Session Most

- Observation: la lista de sufijos Engine autorizados omitió `catalog select`, el comando de selección (propio de este shot); record exige `--assets` reales y observe exige el manifiesto, así que sin selección la captura se detiene completa.
- Why it was hard: fabricar manifiesto o usar assets fixture está prohibido; el bloqueo se registra medido (1 denegación, 0 variantes después) en vez de evadirse.
- Proposed improvement: preflight del lanzador que recorra la CADENA completa en seco con fixtures (selección→observe→record→verify→manifest→replay), no solo formas sueltas.

## Most Useful Part Of Sistema 1

- What helped: materializador canónico disponible esta pasada (denegado en pasadas 1-2) y candidatos preservados en data-dir desde la pasada 2.
- Why it helped: la pasada 3 aplicó, compiló y pasó tests a la primera corrida; el cierre canónico salió limpio.
- Keep/change: mantener el patrón candidato→aplicación y el cierre con materializador.

## Least Useful Or Noisy Part

- What did not help: las 8 variantes de formas de la pasada 2 — desviación reconocida; esta pasada usó solo las formas exactas y bastó.
- Why it was weak/noisy: costo evitable de descubrimiento.
- Proposed cleanup: publicar siempre la lista COMPLETA de sufijos junto al prefijo del Engine.

## Missing Support

- Problem not solved by Sistema 1: n/a (el bloqueo es del perfil por-shot del lanzador, no de AGENTS OS).
- How Sistema 1 could help next time: nada nuevo.
- Suggested artifact type: n/a.

## Retrieval Feedback

- Useful query or source: change_log del proyecto (secciones W1-a..W1-c) para el formato de la sección (11) y la actualización de §18 sin duplicar historia.
- Missing context: nada material.
- Duplicate/noisy result: n/a.
- Better future query: n/a.

## Skill Feedback

- Skill that worked well: agents-os-agent-run-register y el flujo materializador+Edit.
- Skill that was confusing: ninguna.
- Trigger/routing gap: ninguno observado.
- Suggested contract change: ninguno.

## Template Feedback

- Template used: session-summary, session-feedback, agent-run, doc (todos via materializador).
- Field that helped: source_session y outcome/verification explícitos.
- Field that felt redundant: ninguno.
- Missing field: none.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna al iniciar? sí (global always-load en pasada 1; warm reuse después).
- ¿Qué valor operativo aportó? preservación de historia (revisión v2 del preregistro sin sobrescribir v1) y falla cerrada ante la denegación de selección.
- ¿Dejé mensaje para el próximo agente? sí — doc W1-d y §18 con el siguiente paso exacto (autorizar `catalog select`).
- Utilidad del espacio privado (1-5): 4.

## Pain Pattern Candidate

- Is this likely to repeat? yes — tercera pasada consecutiva con desalineación mandato↔gate (allowlist malformada; formas sin cachés; sufijo faltante), cada una con causa distinta.
- Suggested severity: medium (el preflight de formas exactas funcionó; falta preflight de cadena).
- Candidate owner: lanzador W1.
- Promote to L3 memory? defer — la corrección es del lanzador (preflight de cadena), no una regla transferible del agente.

## One Next Improvement

- Preflight de cadena con fixtures para todos los sufijos del shot antes del despacho.

## Actualización 2026-10-28 (pasada 4, misma sesión)

- **Corrección de la fricción registrada arriba:** la causa de la denegación de la pasada 3 NO fue un sufijo omitido — fue el argumento `--preregister`, que el código nuevo exige y el perfil del hook no incluía; `catalog select` sí estaba permitido. El perfil nuevo agregó únicamente ese argumento con destino exacto y el retry único corrió (historia de la atribución errónea preservada arriba, sin borrar).
- **Fricción nueva, medida y distinta:** la página Gamma acotada (comando exacto, 17:47:02Z) devolvió `[]` con HTTP 200 — cero candidatos elegibles. La regla ex ante se aplicó sin desviación: sin universo ampliado, sin WS, cadena NOT_RUN con causa. Hipótesis no verificada (sin variantes de sondeo): semántica server-side de `start_date_min` o estado real del catálogo en ese instante; un 200 con `[]` no distingue entre ambas.
- **Lección de sistema (repite el patrón W1-a/W1-b):** atribuir causas de gate sin preflight deja explicaciones parcialmente falsas registradas; la corrección fechada es el mecanismo correcto, pero el preflight real de forma+flag+fuente antes de afirmar reglas del hook sigue siendo la mejora pendiente.
- Scores de la pasada 4: retrieval 5, skill fit 5, closeout friction 4 (bloqueo ahora es de datos/regla, no de permisos), overall confidence 4.

---
type: feedback
schema_version: 1
scope: session
created: 2026-10-30
updated: 2026-10-30
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
entities:
  - "[[Polymarket Engine — MVP]]"
related:
  - "[[Research — Default Suite Isolation W1-nR 2026-10-30]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: minimax/MiniMax-M3.1-Flash
agent_run: "[[2026-10-30-zcode-minimax-m3.1-flash-polymarket-w1nr-isolation]]"
session_goal: aislar la suite por defecto de cmd/researchpilot para que no reanalice el episodio sellado ni sobrescriba evidencia
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

# Session Feedback - 2026-10-30 - polymarket-w1nr-isolation

## Context

- Agent surface: [[ZCode]]
- Agent model: minimax/MiniMax-M3.1-Flash
- Agent run: [[2026-10-30-zcode-minimax-m3.1-flash-polymarket-w1nr-isolation]]
- Session goal: aislar la suite por defecto de `cmd/researchpilot` (opt-in del test histórico, salida a scratch, exportación de recibos bajo opt-in) sin tocar código de producción ni reanalizar un episodio real.
- Main entity: [[Polymarket Engine — MVP]]
- Skills used: `agents-os-bootstrap`, `agents-os-context-retrieval`, `agents-os-agent-project-workflow`, `agents-os-agent-run-register`, `agents-os-entity-update`, `agents-os-session-close`, `agents-os-session-feedback`.
- Retrieval mode: lectura enfocada por rutas canónicas (sin Graphify en este disparo); el preflight de seguridad propio de la supervisión actuó como gate de forma previa.
- Artifacts changed: repo `polymarket-engine` (3 archivos de test, commits locales `4acf954` y `e4d201a`); en el vault, el informe de research W1-nR, la continuidad Five-POC, el MVP, el resumen de sesión, este feedback, el agent run y el change log de entidad.

## Scores

Use 1-5, where 1 is poor and 5 is excellent.

- Startup clarity: 4
- Retrieval usefulness: 3
- Skill fit: 4
- Template fit: 4
- Closeout friction: 3
- Overall confidence: 4

## What Complicated The Session Most

- Observation: el mandato exigía inventariar todos los tests y helpers alcanzables de los tres paquetes afectados, y enumerar sus rutas de salida; el hook de alcance denegó `grep`, `find` y `ls` sobre esos raíces, así que la enumeración real de archivos se hizo probando rutas con `Read` y apoyándose en la sugerencia «Did you mean?» del propio lector. En la continuación de la misma sesión, además, el flake de timing preexistente `TestStepSequenceWaitsForAbsoluteSlotStart` incidió en **dos** de las tres corridas registradas de la suite (199.512005 ms y 199.026946 ms frente al umbral de 200 ms), de modo que la suite completa no pudo declararse verde de forma fiable y fue necesario una tercera corrida registrada.
- Why it was hard: no había una forma autorizada de listar un directorio del repo; sin inventario completo, la afirmación «rutas no temporales corregidas» queda apoyada en el recuento del preflight (47 sitios de escritura sobre 36 archivos) y en la lectura de los archivos que sí se pudieron abrir, no en una lista exhaustiva producida por una herramienta. Y un flake que ya estaba documentado sigue consumiendo la confianza en el resultado de la suite, aunque se sepa que no es de este trabajo.
- Proposed improvement: permitir un listado/grep de solo lectura acotado a las raíces de los paquetes bajo auditoría, de modo que el inventario de fuentes exigido por el mandato sea reproducible por el agente y no dependa del sondeo por rutas.

## Most Useful Part Of Sistema 1

- What helped: el bootstrap por ventanas explícitas con verificación post-herramienta, más el contraste entre la continuidad y el informe W1-n sobre lo que la suite realmente hizo.
- Why it helped: el perfil global obliga a cargar el core y la entidad por delta, y la nota de research con su warning de rectificación fue la que permitió partir de hechos y no de las aserciones heredadas de W1-n.
- Keep/change: mantener.

## Least Useful Or Noisy Part

- What did not help: la búsqueda con `Read` sobre rutas plausibles para adivinar nombres de archivo.
- Why it was weak/noisy: cada intento fallido consume una llamada y devuelve poco; además el hook denegó varias de esas explorations por alcance.
- Proposed cleanup: en auditorías de fuentes, exponer el inventario de archivos del gate como parte de su salida, en lugar de obligar al agente a reconstruirlo.

## Missing Support

- Problem not solved by Sistema 1: el gate de seguridad previo informa un **recuento** de sitios de escritura y archivos fuente, pero no el inventario nominal; el agente debe reconstruirlo con lecturas adivinadas para poder afirmar qué rutas son no temporales.
- How Sistema 1 could help next time: que el informe del preflight exponga la lista de archivos y sus rutas de escritura, de modo que la corrección apunte a rutas concretas y verificables.
- Suggested artifact type: ninguno nuevo; es una mejora del informe del gate existente.

## Retrieval Feedback

- Useful query or source: las ventanas de continuidad y los informes W1-n/W1-m/W1-l W1-e leídos por ruta canónica.
- Missing context: el inventario de archivos de los tres paquetes, que no era recuperable con las herramientas permitidas.
- Duplicate/noisy result: la enumeración de rutas candidatas produjo many «File does not exist» sin valor de evidencia.
- Better future query: pedir al gate la lista de archivos que inventarió.

## Skill Feedback

- Skill that worked well: `agents-os-agent-project-workflow` (el informe de research y la nota del proyecto son el planificador único y evitaron mantener un plan paralelo) y `agents-os-session-close` (materializar con `materialize_schema_note.py` y luego rellenar, sin frontmatter escrito a mano).
- Skill that was confusing: `agents-os-session-close` pide inventario completo en modo detallado, pero el mandate pedía cierre materializado con artefactos concretos; la tensión entre «default report de 1-2 líneas» y el inventario completo se resolvió siguiendo el mandate, no la skill.
- Trigger/routing gap: ninguno detectado; el registro de skills y el enrutamiento por `agent-project-workflow` fueron suficientes.
- Suggested contract change: ninguno.

## Template Feedback

- Template used: `80-agents/templates/session-feedback.md` vía el contrato ejecutable.
- Field that helped: `agent_run` y `agent_surface`/`agent_model`, queallows enlazar el feedback con la evidencia de ejecución sin duplicarla.
- Field that felt redundant: `session_goal` convive con el objetivo del resumen L1; en un disparo con informe completo el objetivo queda duplicado en tres notas.
- Missing field: un campo para «denegaciones del hook» (herramienta, objetivo, motivo), que es evidencia de fricción y hoy sólo cabe en prosa libre.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? sí
- ¿Qué valor operativo aportó para esta sesión (continuidad, detalles crudos, advertencias)? aporta el criterio transferable de «ante un retry o resultado incierto, leer el estado durable y no repetir efectos laterales» y la separación entre verifying el outcome en la capa que posee la semántica y asumir el éxito por un exit 0; es exactamente la lección del incidente W1-n.
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna? no: el delta es estado de proyecto y ya quedó en las notas canónicas.
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad? 4; mejoraría con un puntero explícito desde la nota de proyecto a la sección de continuidad aplicable, para no releer el global cuando el detalle ya está en el informe.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: high
- Candidate owner: agent
- Promote to L3 memory? defer

## One Next Improvement

- Que el informe del gate de seguridad exponga el inventario nominal de archivos de fuente y sus rutas de escritura, de modo que una auditoría de rutas no temporales sea reproducible sin sondeo por rutas adivinadas.
- Y, para la clase de defecto que la revisión encontró: al reescribir un mecanismo que ya tenía garantías (en este caso la exportación de recibos bajo opt-in), conservar la lista explícita de precondiciones del mecanismo anterior (`code == 0`) y cubrir la ruta de fallo con una prueba, no sólo con el camino feliz.
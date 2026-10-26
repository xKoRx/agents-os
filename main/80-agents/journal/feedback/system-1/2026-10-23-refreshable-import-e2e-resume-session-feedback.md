---
type: feedback
schema_version: 1
scope: session
created: "2026-10-23"
updated: "2026-10-23"
area: "[[Meli]]"
project: "[[Import de Refreshable Materialized Views externas]]"
entities:
  - "[[AGENTS OS]]"
related: []
aliases: []
agent_surface: "[[Codex]]"
agent_model: unknown
agent_run: "[[2026-10-23-codex-unknown-refreshable-import-e2e-resume]]"
session_goal: "Alinear y certificar import refreshable externa en RIO local"
source_session: "01a16977-1898-7c71-bba7-35eedff7cffe"
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

# Session Feedback — refreshable import E2E resume

## Context

- [[Codex]], modelo raíz unknown, [[2026-10-23-codex-unknown-refreshable-import-e2e-resume]]. E2E local completado; root implementó y Luna hizo catastros read-only. Feedback explícitamente solicitado por el owner.
- Bootstrap se mantuvo warm. Nota de proyecto y paths conocidos dieron continuidad; las specs vigentes corrigieron premisas sobre tablas requeridas y separaron Save de Deploy.

## Scores

- Startup y recuperación 4/5; ajuste de skills 3/5; eficiencia 2/5 por repetición de gates y arranques; confianza en evidencia local 5/5 para el alcance probado. No son scores de desempeño del modelo.

## Skill Feedback

- La skill de autoría no daba una ruta para abrir un formulario nuevo dependiente de drag; Lore carecía de esa herramienta. Se descartó copy/paste porque sólo clona un nodo visual. Se agregó native HTML drag con DataTransfer y refs frescas, tests reales y un PR Lore separado autorizado. El canvas acepta el control accesible Zoom in como destino del drop.
- El caso necesitó un pipeline vacío, SQL externo previo y credenciales coherentes con un DEFINER real. Se descubrió la ausencia local de CKAAS/KVS y el mapper snake_case del endpoint documentado camelCase. No bastaba seedear componentes gestionados ni simular un resultado CP.
- Estado PM/flag externo y presencia de outputs no estaban cubiertos por los oráculos disponibles. Se añadieron checks genéricos, sin imprimir valores de credenciales, además de UUID/DDL/sentinel/usuario físicos.
- ClickHouse cambia los paréntesis exteriores AS SELECT al modificar COMMENT. La primera comparación literal falló; comparar JSON real permitió normalizar sólo ese formato y el marker autorizado. CA-7 luego demostró que el parser del CP tampoco aceptaba ese formato; se corrigió el feature con regresiones antes de la última certificación. La skill describe fixtures/oráculos/drag y conteo de deployments distintos; faltaba esta advertencia de serialización.
- Tests con textarea ocultaban el callback anterior de Monaco. La física encontró el falso error APPEND contra TO; una regresión que invoca el listener anterior reproduce el defecto sin importar una implementación falsa del editor.

## Operación y eficiencia

- Se añadieron screens y espera del grupo completo: un padre que sale no prueba que sus hijos terminaron. La regresión exige salida explícita; no usa la negación de kill como si errexit la convirtiera en assert.
- El arranque limpio encontró readiness de una ejecución previa en el log que screen anexaba. El helper ahora archiva el archivo antes de iniciar; una regresión con screen real reproduce y evita el falso readiness.
- La base E2E avanzó durante el trabajo. Doctor lo detectó al arrancar; se interrumpió antes de Lore, se limpió, mergeó y revalidó. Conviene fijar el SHA de base antes del certificado y registrar cualquier cambio concurrente.
- Los contratos obligan a repetir 61 selectores y dos stacks incluso por tooling/casos; no se rebajaron gates. Una separación de planes para tooling podría reducir costo, si el repo la define con cobertura adecuada.
- El bloqueo automático de down se resolvió con autorización explícita del owner para recrear datos. Se mantuvieron los recursos ajenos fuera de cambios y los secretos fuera de reportes. AOC no tuvo herramienta útil; la búsqueda de assets anunció autoactualizaciones no esperadas, sin instalar un workaround.

## Memoria Interna (Internal Memory)

- La base warm y la nota de proyecto fueron útiles para continuidad. No se creó memoria global redundante para el estado operativo; quedó en el proyecto. Root model unknown preservado y resultados de Luna separados, sin scores inventados.

## One Next Improvement

- Mapear cada CA a escenarios y oráculos antes del primer certificado. Omití inicialmente CA-7 pese a que el prompt pedía una acción posterior; la revisión tardía encontró un bug real y consumió otra batería. La autoría también debería enseñar el DDL canónico de ClickHouse y el baseline físico de definición. Riesgo bajo; evita falsos negativos sin debilitar identidad ni preservación.

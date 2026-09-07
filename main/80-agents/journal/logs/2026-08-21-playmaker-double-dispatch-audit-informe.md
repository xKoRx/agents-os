---
type: change_log
schema_version: 1
scope: session
created: "2026-08-21"
updated: "2026-08-21"
area: "[[Meli]]"
project: "[[Playmaker — Doble dispatch al avanzar batches]]"
application: "[[rio-playmaker]]"
entities:
  - "[[Playmaker — Doble dispatch al avanzar batches]]"
  - "[[Auditoría independiente — Informe del doble dispatch]]"
related:
  - "[[Prompt maestro — Auditoría independiente del doble dispatch]]"
  - "[[RIO]]"
aliases:
  - Change log auditoría doble dispatch
confidence: verified
source_session:
source_feedbacks: []
share_scope: team
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/meli
  - app/rio-playmaker
---

# 2026-08-21-playmaker-double-dispatch-audit-informe

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - `created` — `10-projects/Meli/Playmaker — Doble dispatch al avanzar batches/Auditoría independiente — Informe del doble dispatch.md` (`type: doc`, materializado por contrato)
  - `updated` — `10-projects/Meli/Playmaker — Doble dispatch al avanzar batches/Playmaker — Doble dispatch al avanzar batches.md`: `progress` 25 → 55, `## 📊 Estado actual` reescrito a post-auditoría, callout sobre las secciones 1–14, 3 tareas cerradas y 4 nuevas, 2 entradas de bitácora, 2 decisiones cerradas, link al informe
  - `created` — este change log

## Motivo

Cerrar la auditoría independiente en dos fases definida en [[Prompt maestro — Auditoría independiente del doble dispatch]] y dejar su resultado como fuente canónica del proyecto. El proyecto queda como planificador y estado; el informe concentra causa raíz, contraste, matriz de alternativas y diseño recomendado, sin duplicar el análisis en las dos notas.

## Fuentes usadas

- Repo `rio-playmaker`, rama `develop`, HEAD `0524ce49ef34`, refs remotas al 2026-08-20 23:29. Lectura read-only: sin cambios de código, schema ni refs, sin `git fetch`, sin ejecutar la suite.
- Código, migraciones, historial git y `meli/backlog.md` del repo, resueltos por `repo + path relativo` desde [[Fuentes — Workspace de repositorios]].
- Evidencia de DB, timestamps y stacktrace del incidente, provista en la nota de proyecto.

## Resolución aplicada

- Causa raíz confirmada desde código: el avance de batch actúa sobre una condición de nivel sin consumirla y el dispatch no transiciona el `ComponentRun`.
- Regresor confirmado con el diff: `dac615f47` (PR #1047, en develop 2026-08-19) movió `checkPrerequisites` a `AFTER_COMMIT` + `@Async` + `REQUIRES_NEW`, invirtiendo la carrera de *nadie avanza* a *todos avanzan*.
- Conflicto resuelto contra el diagnóstico previo: la afirmación de fase 1 de que los dos componentes de run_order 1 se duplicaron se degradó a hipótesis no verificada, porque la evidencia de DB muestra que `jarita-signal-test` completó bien. Registrado en el informe, no silenciado.
- Corrección aportada sobre la deuda conocida: los dos DEBT de `meli/backlog.md` están redactados en clave cross-execution y ninguno describe el doble avance intra-execution; uno referencia un método que ya no existe y ambos proponen un índice parcial que MySQL no soporta.
- Dos decisiones cerradas por evidencia: el lock de fila sobre `PipelineExecution` queda descartado como fix único, y Testcontainers MySQL 8 pasa a ser precondición para validar cualquier fix.
- No se creó memoria pública ni ADR: la selección de la alternativa sigue siendo acuerdo de equipo pendiente, así que no corresponde cristalizarla todavía.

## Validación

- Notas canónicas materializadas con `materialize_schema_note.py` (`doc` y `change_log`); sin frontmatter escrito a mano.
- Lint dirigido sobre las tres notas tocadas: ver resultado al cierre de la sesión.
- Sin paths absolutos de máquina nuevos en el vault; las referencias al repo usan `repo + path relativo`.
- Repo de trabajo verificado limpio antes y después (`graphify-out/` untracked, preexistente y ajeno a la tarea).

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos. Los identificadores citados son claves surrogadas internas y correlation IDs, sin PII ni credenciales.

## Rollback

- Borrar `Auditoría independiente — Informe del doble dispatch.md` y este change log.
- Revertir la nota de proyecto a `progress: 25` con el `## 📊 Estado actual` previo, quitando el callout, las tareas y decisiones agregadas y las dos entradas de bitácora del 2026-08-21 rotuladas "Auditoría" y "Hallazgo nuevo".
- No hay efectos fuera del vault: la auditoría no tocó código, DB ni refs.

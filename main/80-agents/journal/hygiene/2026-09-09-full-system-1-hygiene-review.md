---
type: scratch
schema_version: 1
scope: session
created: "2026-09-09"
updated: "2026-09-09"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[graphify]]"
  - "[[2026-09-09-kaizen-report]]"
aliases: []
confidence: high
source_session:
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/hygiene-report
  - kind/scratch
  - scope/session
---

# Full System 1 hygiene review

> [!info]+ Hygiene review
> Operational report. Excluded from normal Graphify retrieval.

## Review Window

- **Mode:** `full-system-1`
- **Scope:** todo el corpus de Sistema 1 — 40 skills y `_shared/`, 221 notas de memoria pública, 112 notas de memoria interna, `80-agents/agents-os/`, templates, journal y los índices/logs del wiki de recursos.
- **From:** 2026-09-03 (último reporte de higiene) · **To:** 2026-09-09
- **Next review after:** 2026-09-16, o antes ante 10 feedbacks nuevos o un blocker.

## Files Checked

- Lecturas cualitativas delegadas a dos subagentes con rúbrica cerrada (skills; memoria pública + docs + índices). Los greps mecánicos y las verificaciones de disco se hicieron en el agente principal, y todo hallazgo se verificó contra la fuente antes de editar.
- Gates ejecutables corridos directamente: `doctor.py`, `doctor.py --strict`, `lint.py --check/--strict/--gate`, `validate_schema_contract.py`, `lint_tags.py` y `graphify-obsidian status/update/explain`.

## Estado de los gates

| Gate | Antes | Después |
|---|---|---|
| `doctor.py` | HIGH=2 MEDIUM=0 LOW=0 · startup≈4996 | HIGH=0 MEDIUM=0 LOW=0 · startup≈5004 |
| `lint.py --check` | 32 ERROR / 5 WARN | 9 ERROR / 4 WARN |
| `lint.py --gate` | NO-GO (baseline vacío) | GO · `new=0` |
| `lint_tags.py` (memoria pública, requeridos) | 104 errores | 0 |
| `validate_schema_contract.py` | 0 errores | 0 errores |
| Graphify | `stale`, reindex bloqueado 6 sesiones | `fresh`, reindex verde |

## Fixes Applied

### Automáticos

- Crear este reporte y el reporte Kaizen del período.
- Poblar `lint-baseline-v1.json`, que existía desde 2026-08-11 con cero fingerprints y por eso mantenía el gate fail-closed contra deuda ajena. El baseline se emitió recién **después** de bajar la deuda de 32 a 9 errores, así que congela deuda real preexistente y no tapa nada introducido hoy.
- Corregir el bug de `slugify` en `lint_tags.py` y `fix_tags.py`: se removía el `_` antes de convertirlo en `-`, por lo que el gate exigía `kind/userpreference` y `kind/knownerror` contra un contrato que pide `kind/<type-kebab>`. Producía 104 errores fantasma en memoria pública.

### Ediciones directas con log

Todas trazadas en `journal/logs/2026-09-09-agents-os-hygiene-cycle.md`.

- **Club cerrado de `always`:** una decisión de release de Echo Forge entraba al cold start; pasó a `when_project_loaded`.
- **Lifecycle de continuidad:** una continuidad activa sin trigger scoped automático quedó en `when_project_loaded`; la nota global `-archive` quedó `memory_state: superseded` + `indexable: false`, coherente con su `superseded_by`.
- **Memoria interna:** 111 notas normalizadas. 106 checkpoints per-sesión de trabajo cerrado pasaron a `archived` + `manual` + `indexable: false` + `index_priority: never`; quedan 5 slots activos con trigger automático. Se borró un archivo de 0 bytes y se reparó una nota con dos bloques de frontmatter concatenados. La memoria interna es agent-governed, así que el detalle no se expone aquí.
- **Taxonomía duplicada:** `memory/public/known-errors/` (2 notas) se consolidó en `known-error/`; `memory/internal/known-errors/` (3 notas) quedó fuera del índice y con lifecycle válido, pendiente de reubicación; `journal/change-logs/` (3 notas) en `journal/logs/`; `journal/feedback/session/` (2 notas) en `feedback/system-1/`, donde Kaizen sí las recorre. Se borró el slot vacío `memory/public/constitution/`.
- **Metadata de memoria pública:** 5 tags `scope/replace-me`, 14 valores de `scope` fuera del enum, 18 tags `kind/knownerror`, 17 `load_policy` sin trigger concreto, 3 `load_policy` vacíos, 2 claves YAML duplicadas y 1 `supersedes: false`.
- **Skills:** 60 notas recibieron el tag canónico faltante; 10 skills sin `schema_version`/`load_policy`/`indexable`/`index_priority` quedaron migradas; `operational-healthcheck-policy` tenía `scope: global` con tag `scope/project`.
- **Portabilidad:** una decisión de Aranea persistía un path absoluto de máquina para una ruta del vault; el brief histórico del Hot Path, con paths de otra máquina, se archivó junto a su proyecto y `00-inbox/` quedó limpio.
- **Índices del wiki:** se creó `30-resources/grids/log.md` (dominio activo sin bitácora), se actualizó `rio-atlas/00-index.md` y la línea de dominios activos de `00-RESOURCE-WIKI.md`.
- **Descubribilidad de skills:** se agregó el alias con el nombre de la skill a las 40 `SKILL.md`. Ningún `[[skill-name]]` resolvía, porque el archivo siempre es `<dir>/SKILL.md`; eran ~341 links muertos, 60 de ellos desde memoria pública.
- **`.graphifyignore`:** se excluyó la continuidad interna per-sesión (intent == enforcement), se agregó `.trash/`, se repuntaron dos exclusiones a `signals-func-spec-authoring/references/` y se retiró la exclusión de un archivo borrado.
- **Gate nuevo:** `doctor.py` ahora valida el frontmatter requerido de cada skill y que `name` coincida con su carpeta. Es lo que mantuvo invisible durante semanas a las 10 skills sin migrar.

## Alignment Findings

### define == implement (corregidos)

- `agents-os-skill-authoring` instruía incluir `finish tasks` en un `SKILL.md` runtime, justo lo que `skill-contract.md` prohíbe y el doctor flaggea: toda skill nueva nacía violando el contrato.
- `agents-os-hygiene-review` listaba "marcar estado de progreso dentro de la skill de higiene" como fix automático sin log: la misma contradicción, con permiso de escritura silenciosa.
- `agents-os-context-retrieval` llevaba el tag `agent/alwaysload` con `load_policy: when_entity_loaded`. El doctor sólo evalúa el campo, así que el gate era ciego a un quinto miembro de un club cerrado de cuatro; cualquier ruteo por facets reinflaba el hot path.
- Dos catálogos de queries de Graphify con presupuestos distintos (1200 vs 1000): la skill de mantenimiento ahora apunta al contrato.
- Dos punteros de autoridad equivocados: el vocabulario de tags de frontmatter vive en `schema-contract.md`, no en `convenciones.md`.
- `context-router.md` quedó registrado en la tabla de fuentes canónicas de `agents-os.md` como modelo conceptual no ejecutable, que es lo que su propio callout declara.

### Agnosticismo

- Un caveat de sandbox nombraba un cliente concreto; ahora describe la restricción real (sin escritura en `~/.cache`).
- El perfil de superficie de bootstrap describía un startup que ya no existe (cargaba "memory prompt, profile, constitution, internal memory y contexto Graphify").

### Compactness y clasificación

- Un known error que se autodeclara diagnóstico refutado estaba en `when_error_matches` + `index_priority: high`: pasó a `manual` + `low`.
- El resto de candidatas a compactación y reclasificación queda como propuesta: son juicio por nota y hay evidencia real que se puede perder.

## Proposals (need owner OK)

1. **Nota canónica de Symphony.** 140 links de routing muertos con tres grafías (`[[Symphony]]` ×69, `[[xKoRx/symphony]]` ×63, `[[symphony]]` ×8). Requiere crear la entidad Sistema 2 y unificar; las variantes van a `aliases`.
2. **Cuatro contradicciones entre notas persistidas**, todas de dominio Echo/Symphony y ninguna resoluble sin el owner: estado de C3 / `CAMPAIGN_STOP_POLICY_V1` (`FROZEN/PASS` vs `BLOCKED`), placement del `sqx-watcher` (local vs los tres workers), la FK `subject_ref` de la migración 009 (se elimina vs se preserva) y qué artefacto ejecuta SQX Custom Analysis (`Snippets/**` vs `Snippets.jar`). Las cuatro cargan con `index_priority: high`.
3. **Descubribilidad de skills.** 36 de 39 skills no son invocables nativamente en ninguna superficie. Hay dos caminos excluyentes —generar router por skill, o declarar oficialmente el fallback por ruta con verificación de disponibilidad en bootstrap— y las sesiones que lo reportaron pidieron cosas distintas.
4. **Diagnóstico de capacidades por superficie en bootstrap.** Pedido tres veces en términos casi idénticos. Debe registrar qué exige el contrato, qué expone la superficie y qué control compensatorio se aplicó, para no afirmar que un gate corrió cuando no corrió.
5. **Modo reducido del template de feedback.** El Delta Classifier resolvió *si* cerrar, no *cuánto* llenar. Faltan el campo `mode: tactical|full` y el permiso explícito de omitir secciones sin hallazgo.
6. **69 notas de memoria pública sin `schema_version`.** Por contrato son read-only hasta migrar; 6 son known errors sin `## Mitigación`, que es el campo que cambia una acción.
7. **Cinco memorias públicas candidatas a compactación** (7,2–10,4 kB, con ledgers gate-por-gate, SHA256 y PIDs dentro de `## Decisión`) y cuatro reclasificaciones de artefacto, entre ellas un learning con un procedimiento invocable de cinco fases que se inyecta completo en cada carga de proyecto.
8. **Sub-dominios de `30-resources/aranea/` usan `README.md`** donde el contrato exige `00-index.md`; es también la causa de los links de carpeta rotos. Y su `00-index.md` tiene 85 filas contra un umbral de ~20.
9. **Wikilinks que no son entidades:** ~15 símbolos de código en `entities` y 5 IDs de sesión usados como links en `related`.
10. **Tres known errors bajo `memory/internal/known-errors/`.** No son continuidad: son L3 de dominio Symphony, específicos de tres flows de julio y agosto, sin metadata de retrieval y en un tercer home de taxonomía. Se les puso lifecycle válido y quedaron fuera del índice; decidir si se reubican en `memory/public/known-error/symphony/` generalizando el síntoma, o se eliminan porque su familia general ya existe ahí.
11. **`.tmp-rio-controlplane-flink-test/` dentro del vault** (2036 archivos, 25 MB, clone completo con `.git`). Viola el invariante 12, pero tiene trabajo sin commitear en `feature/test-deployment-context` que **no existe** en `~/fuentes/rio-controlplane-flink`. No lo toqué: sólo lo excluí del índice y del lint. Decidir si el WIP se rescata o se descarta.

## Rejected (with reason)

- `_shared/skill-contract.md` sin frontmatter: está excluido de Graphify a propósito y se lee de disco por nombre. La ausencia es coherente, no deuda.
- Paths `/home/kor/...` y `/home/hermes/...` en memorias de Symphony y Aranea: son hosts remotos reales, no referencias al vault. El invariante 11 aplica a rutas del vault.
- 13 errores de tag en `agents-os-entity-lifecycle/scripts/fixtures/`: son fixtures deliberadamente inválidos que el validador necesita. Se excluyeron del fixer, no se "arreglaron".
- Renombrar secciones en las dos skills de specs de Signals para satisfacer el linter: sus `## X` son el esqueleto de spec que la skill enseña, no secciones de la skill. Reestructurarlas por un gate rompería skills de uso diario. Quedan en el baseline como deuda declarada.

## Graphify

- **Status:** `fresh`. Primer reindex verde tras seis sesiones bloqueadas.
- **Validación:** `explain "AGENTS OS"` resuelve con 9 conexiones; `explain` sobre el runbook nuevo devuelve el nodo con relaciones tipadas (`references|about|in_project`, `references|in_area`).

## Open Tasks

- Las diez propuestas de arriba, ninguna iniciada.
- Los 9 ERROR y 4 WARN residuales del lint quedaron en el baseline: 5 son secciones de las skills de Signals y 4 son secciones faltantes en tres notas de proyecto/recurso.

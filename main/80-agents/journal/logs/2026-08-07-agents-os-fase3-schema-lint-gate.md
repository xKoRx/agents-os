---
type: change_log
scope: session
created: 2026-08-07
updated: 2026-08-08
area: "[[Personal]]"
project: "[[AGENTS OS - Fase 2]]"
entities:
  - "[[AGENTS OS - Fase 2]]"
related:
  - "[[agent-constitution]]"
  - "[[convenciones]]"
confidence: verified
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - project/agents-os
  - change/created
---

# Fase 3 — Schema S1/S2 + templates + lint all-vault + gate warn-first

Ejecución del "Paquete autónomo Fase 3 — Schema S1/S2" de [[AGENTS OS - Fase 2]].
Gate previo G2 `accepted` por el owner (2026-08-07). No se inició F4; G3 queda en
`accepted` por decisión explícita del owner (2026-08-08). F4 quedó habilitada,
pero no se inició en esta sesión.

## Aceptación del owner — 2026-08-08

El owner aprobó G3 después de revisar la corrección y su evidencia. El planner
pasó `G3: review → accepted`; la próxima tarea es T4.1 y la tarea puente del
proyecto padre permanece WIP hasta completar el proyecto de agente.

## Corrección de review — 2026-08-08 (evidencia vigente)

El owner rechazó la primera entrega para corregir tres falsos cierres. G3 pasó
`review → wip → review`; F4 no se inició.

### Bloqueantes corregidos

1. **Handoff F4 completo:** `methodology` (`draft|active|deprecated`) y `source`
   (`active|superseded|archived`) quedaron definidos en `convenciones.md`,
   implementados por `lint.py` y respaldados por templates S2 + fixtures
   válidas. `source` exige locator resoluble (`source_url` o `repo` + `path`).
2. **Sin falsos verdes de contrato:** el lint parsea frontmatter top-level y
   valida campos base S1/S2, campos core S2, lifecycle, owner/parent de proyecto,
   frontera de templates y reglas duras. `status` en S1 es ERROR también cuando
   se ejecuta como fixture aislada; `--gate` conserva exit 0 por D12.
3. **Frontera reconciliada:** se eliminó `70-templates/decision.md` (duplicaba el
   template S1 canónico de `80-agents/templates/`); `agent-profile.md` se movió
   a `70-templates/` por ser S2; action/monitor/skill completaron metadata. Las
   skills lifecycle, note-capture y entity-update seleccionan `convenciones.md`
   para S2 y `metadata-schema.md` solo para S1.

### Evidencia reproducida

- Templates `70-templates/` + `80-agents/templates/`: `ERROR=0 WARN=0
  notes_scanned=31` (exit 0).
- Fixtures válidas: `ERROR=0 WARN=0 notes_scanned=6` (exit 0), incluidas
  `methodology` y `source`.
- Fixtures inválidas: `ERROR=8 WARN=0 notes_scanned=8` (exit 1): bad status,
  missing created, missing updated, missing project owner, missing required
  status, S1 status, source sin locator y unknown type. Cada archivo prueba un
  assert independiente; `s1-with-status.md` aislada devuelve ERROR=1/exit 1.
- All-vault estricto: `ERROR=237 WARN=87 notes_scanned=471 sin_type=87
  tipos_desconocidos=60` (exit 1). Breakdown ERROR: missing-field=149,
  unknown-type=60, s1-status=24, bad-status=3, bad-owner=1. El aumento frente
  al baseline anterior es evidencia del enforcement corregido, no regresión de
  notas live; el retrofit masivo sigue fuera de F3.
- Read-only: hashes SHA-256 de todas las notas Markdown antes/después de
  `--check` idénticos (PASS).
- Doctor estricto: `HIGH=0 MEDIUM=0 LOW=0 startup_tokens≈4979` (exit 0).
- Gate real: `graphify-obsidian update` mostró `ERROR=237 WARN=87`, continuó y
  completó exit 0 (`5320 nodes, 6095 edges`).

### Archivos canónicos de la corrección

- Schemas: `90-system/convenciones.md`,
  `80-agents/skills/_shared/metadata-schema.md`.
- Enforcement: `80-agents/skills/agents-os-entity-lifecycle/scripts/lint.py`
  y fixtures `valid/` + `invalid/`.
- Templates: nuevos `70-templates/methodology.md`, `source.md` y
  `agent-profile.md`; reparados `action.md`, `monitor.md` y
  `80-agents/templates/skill.md`; retirados los templates mal ubicados
  `70-templates/decision.md` y `80-agents/templates/agent-profile.md`.
- Routing: skills `agents-os-entity-lifecycle`, `agents-os-note-capture` y
  `agents-os-entity-update`; referencia live reparada en `80-agents/crew/Ariadna.md`.
- Control: planner `AGENTS OS - Fase 2.md` y `README.md` del vault.
- Derivados regenerados por el test: `95-graphify/obsidian/`.

## Cambios canónicos (archivos tocados)

### T3.1 — Separación de autoridades S1/S2 (D4)
- **modify** `80-agents/skills/_shared/metadata-schema.md`: restringido a
  **Sistema 1** (memoria/journal/runtime/skills). El enum `type` quedó solo con
  tipos S1 (`constitution, user_preference, agent_memory, skill, learning,
  decision, known_error, runbook, command, pattern, feedback, session,
  raw_session, change_log, scratch`). Se removieron las filas de entidades S2 de
  "Type Defaults" y se agregó puntero a `convenciones.md`. Reafirmada la regla
  dura S1: las notas S1 **no** usan `status`.
- **modify** `90-system/convenciones.md`: nueva sección **"Schema de Sistema 2
  (autoridad)"** con tabla de tipos + `status` permitido por lifecycle + status
  requerido (piloto `area`/`project`/`application`) + campos base por tipo. S2
  define `status` por lifecycle; S1 no lo exige.

### T3.2 — Templates alineados (pasan lint)
- **modify** `70-templates/decision.md`: eliminado `status: accepted` ceremonial
  (`decision` es S1; S1 no usa status).
- Bendecidos como tipos reales (no drift accidental; tienen template + notas
  vivas) en el schema S2, con lo que sus templates pasan sin reescritura:
  `service-doc` (área Aranea, `draft|partial|active|template`), `agent` (crew,
  entidad), `monitor`, `action`, `context_pack`.
- Verificado: **todos** los templates de `70-templates/` y `80-agents/templates/`
  pasan el lint sin ERROR.

### T3.3 — Lint determinístico read-only all-vault + fixtures
- **create** `80-agents/skills/agents-os-entity-lifecycle/scripts/lint.py`:
  recorre todo el vault, honra `.graphifyignore` + dot-dirs (`.trash`, `.obsidian`,
  …) + cualquier `fixtures/`. **Nunca modifica archivos.** Modos `--check`
  (exit 1 si hay ERROR) y `--gate` (warn-first, exit 0 siempre). Aplica el schema
  (D4: el schema es documento; el script lo aplica). Severidades: ERROR
  (tipo desconocido, status inválido, status requerido ausente en piloto), WARN
  (sin type/frontmatter, status en nota S1, status en tipo sin lifecycle).
- **create** fixtures bajo `.../scripts/fixtures/{valid,invalid}/`:
  válidas (project/area/application/learning-S1) → ERROR=0; inválidas
  (unknown-type, bad-status, missing-status, s1-with-status) → ERROR=3, WARN=1.

### T3.5 — Gate PRE-EXECUTE warn-first en el wrapper (R13/D12)
- **modify** `95-graphify/dist/graphify-obsidian`: en el branch `update`, justo
  antes de invocar el extractor, corre `lint.py --gate` (warn-first). Reporta y
  cuenta violaciones **sin bloquear**; `update` completa igual. Los subcomandos
  `query/path/explain/affected` salen antes y **no** se tocan (no reindexan). El
  lint resuelve su propio `VAULT_ROOT`, así que lint el vault canónico (no la
  copia tmp). Fallback no bloqueante si falta `python3`/`lint.py`.
- **sync (derivado)** `~/bin/graphify-obsidian` regenerado desde la fuente
  canónica del vault (la copia en `~/bin` es derivada, no autoridad).

## Evidencia (comandos y resultados)

- Fixtures: `lint.py --check fixtures/valid` → `ERROR=0 WARN=0` (exit 0);
  `lint.py --check fixtures/invalid` → `ERROR=3 WARN=1` (exit 1), con mensajes
  accionables (allowed status listado).
- All-vault `lint.py --check`: `ERROR=63 WARN=111 notes_scanned=470 sin_type=87
  tipos_desconocidos=60` (exit 1). Templates: **cero** findings.
- All-vault `lint.py --gate`: mismo reporte, **exit 0** (no bloquea).
- `graphify-obsidian update` (wrapper canónico): imprimió el banner warn-first +
  conteo (`ERROR=63 WARN=111`), luego el extractor corrió y **update completó**
  (`5300 nodes, 6073 edges`), **exit 0**. Assert warn-first verificado.
- Doctor estricto: `HIGH=0 MEDIUM=0 LOW=0 startup_tokens≈4979` (exit 0) — verde.
- Sin cambios colaterales: el vault no es git repo; los únicos writes fueron
  artefactos derivados en `95-graphify/obsidian/` (en `.graphifyignore`).

Nota de reconciliación con el baseline: el baseline F0 (2026-08-06) contó 141
sin type / 63 variantes sobre **todo** el vault (1311 notas, incl.
archive/journal/trash). El lint corre sobre el **corpus** (post-`.graphifyignore`:
470 notas), por eso reporta 87 sin type / 60 tipos desconocidos. El drift es el
mismo fenómeno medido sobre distinto alcance; el gate warn-first no bloquea en
ninguno de los dos.

## Asserts del paquete F3 (estado)

- [x] Templates pasan lint (0 findings en ambos dirs de templates).
- [x] Tipos/status no definidos fallan con mensaje accionable (fixtures inválidas).
- [x] S1 no exige `status`; S2 define status por lifecycle (schema + lint).
- [x] El lint no modifica archivos en modo check (read-only; solo lee).
- [x] Gate warn-first NO bloquea `update` con el drift actual; emite reporte/
      conteo y `update` completa (exit 0).
- [x] El lint recorre todo el vault excluyendo `.graphifyignore` (470 notas).

## T3.4 — Plan de retrofit por área (NO ejecutado; solo plan)

Regla del paquete: **no** hacer retrofit masivo de notas live en F3 (solo
fixtures + piloto). Este es el plan; su ejecución es posterior a G3 y por área,
con sign-off del owner de cada área. El flip del gate a bloqueante (D12) queda
condicionado a completar el retrofit.

**Prioridad 1 — Personal / AGENTS OS (S1 core, owner: agent, bajo riesgo):**
- `internal_memory` (17) + `agent-memory` (3) + `memory` (2) → `agent_memory`.
- `known-error` (2) → `known_error`.
- `benchmark` (1, `agents-os-doctor/BENCHMARK.md`) → `doc`.
- 13 notas S1 sin frontmatter (INDEX/_shared/contratos): agregar `type: doc`
  donde aplique; varias son fragmentos de sistema (evaluar caso a caso).

**Prioridad 2 — Meli / Echo Forge (proyectos):**
- `agent-project` (10) → `project` + `owner: agent` (convención canónica de
  proyectos de agente; ver `convenciones.md`). Mayor cuidado: revisar tarea
  puente y `parent` de cada uno.
- `owner-task` (5) → revisar: fold a listas de tareas del proyecto o `action`.
- `contract` (1), `spec-alignment` (1) → `doc` (artefactos de spec).

**Prioridad 3 — Aranea / Echo (resources, vocab de área):**
- `ticket` (6), `design-proposal` (3), `design` (1), `contract-proposal` (1),
  `request-changes` (1), `form` (2), `strategy_evaluation` (2), `audit` (1),
  `drill-template` (1): el área decide converger a `doc`/`idea` o bendecir el
  tipo en un anexo scoped. `service-doc` ya bendecido (evaluar convergencia a
  `service`).
- bad-status (3): `BACKUP-DR-OWNER-PROJECT.md` (project `design-frozen` →
  `paused`/`active`); 2 índices con `design-frozen`/`legacy` → `archived`.
- ~60 páginas de `30-resources/` sin frontmatter: se tipifican en **Fase 4**
  (LLM Wiki), no en el retrofit de F3.

**Secuencia recomendada:** P1 (agent-owned, sin sign-off externo) → P2 → P3.
Tras cada tanda: correr `lint.py --check` y confirmar caída de ERROR; cuando el
corpus llegue a ERROR=0 sostenido, el owner decide el flip del gate a bloqueante.

---
type: doc
schema_version: 1
status: active
scope: project
project: "[[AGENTS OS]]"
area: "[[Personal]]"
created: 2026-09-13
updated: 2026-09-13
description: Notas de implementación P3-B — canonical-linter (motor, selftest, README). Decisiones, evidencia de los 7 requisitos del spec sección 5, resultados de la primera ejecución real y limitaciones.
aliases:
  - p3-implementation-notes
tags:
  - kind/doc
  - project/agentsos
  - tech/agents-os
---

# P3-B — Notas de implementación del Canonical Linter

- Rol: implementación (P3-B). Fecha: 2026-09-13. Entradas vinculantes: [[p3-canonical-model|p3-canonical-model]] (P3-A) y [[p3-canonical-linter-spec|p3-canonical-linter-spec]] (parent). Entregables: `canonical_linter.py` (motor, 20 checks), `selftest.py`, `README.md`, `results/run-<timestamp>.json` (única escritura) y este documento.
- Precedente de integración seguido: context-budget P2 — el harness (`rules.py`, `agents_os_conformance.py`) y el schema (`validate_schema_contract.py`) se importan resolviendo su ruta relativa a VAULT_ROOT en runtime; fork/copia prohibidos. `sys.dont_write_bytecode = True` evita `__pycache__` fuera del write scope.

## 1. Decisiones de implementación (con autoridad)

1. **Corpus y mapa físico.** Corpus vivo = `iter_vault_md` del harness menos fixtures (A8). Mapa físico propio (para resolución y CL-09) con las mismas exclusiones de directorios/archivos del harness más los prefijos de fixtures. Tres clases: `live` (corpus), `archive_path` (bajo `40-archive/`), `no_corpus` (journal, packaging `30-resources/agents-os/`, resultados derivados). El índice de resolución cubre `live ∪ archive_path` — journal/packaging no son destino canónico (agents-os.md: "auditoría o distribución, nunca autoridad vigente"; relation-maintenance: no enlazar sessions/logs): un link hacia ese material se reporta como no resuelto en CL-12.
2. **A8 — fixtures.** Se excluyen `80-agents/skills/_shared/fixtures/` (letra del spec) y también `80-agents/skills/agents-os-entity-lifecycle/scripts/fixtures/` (19 notas sintéticas de la misma clase). La extensión se declara en `THRESHOLDS`/`observations` y en el README; la diferencia con `.graphifyignore` (que no excluye fixtures) queda registrada como hallazgo de sistema.
3. **CL-01 (estrechamiento declarado).** El texto ratificado decía "`superseded_by` **o** `supersedes` no vacío con estado active". La autoridad citada lo contradice para `supersedes`: 00-RESOURCE-WIKI ("la nueva puede enlazar `supersedes`") hace de `supersedes`+active la sucesión canónica (3 casos reales en el corpus, incluida la continuidad global). El check emitido exige `superseded_by` no vacío (contradicción real: "no se conserva como una segunda autoridad activa", metadata-schema); `supersedes`+active se cuenta en evidencia sin hallazgo. Registrado en `ambiguities` del record para ratificación del parent.
4. **A5/A3 — clasificación de `status` fuera de contrato.** Para tipos s2, `status` cuenta como no-vigente/en-retiro sólo si está en el enum del tipo (`load_contract()`). Para tipos s1 (donde `status` está prohibido, p.ej. runbook) o tipo ausente, un `status` del set se cuenta como estado observado con dedup-cita a `lint.py:forbidden-field/bad-status/unknown-type`. Así CL-03 detecta el caso real `30-resources/runbooks/signals-code-review.md` (que el modelo espera) sin re-clasificar lo que lint.py ya emite.
5. **Deduplicación (requisito 7).** CL-02 omite agent_memory bajo `80-agents/memory/internal/` (doctor `check_internal_memory_lifecycle` emite ese FAIL) y cita el check-id con el conteo omitido. CL-03 omite memory/internal (mismo motivo). CL-11 excluye `supersedes`/`superseded_by` (scope de CL-04). CL-15 omite filas inexistentes/ambiguas (CL-14). CL-16 no re-emite existencia de destinos (L0 REGISTRY-DISK-PARITY + doctor `check_skill_index`) y lo registra en evidencia. CL-18 omite los destinos del set fijo M16 (`context-budget:CTX-12/M16`). CL-17 no re-escanea `AGENTS.md` (doctor `check_paths`). CL-14/15/16 citan DUAL-REGISTRY-DOMAIN-SYNC (A10) y nunca convierten la dualidad en FAIL.
6. **CL-10 (heurística declarada).** Disparadores: componente del path con forma `archiv*` (case-insensitive) o contenido con ≥2 notas y ≥50% en retiro/no-vigente; excluye `80-agents/memory/internal/` (scope del doctor) y directorios `sources/` (la provenance de la wiki usa `superseded` como lifecycle normal de una fuente). `max_verdict: WARN`; A1 queda como hallazgo de sistema.
7. **CL-14 con assets.** Tras fallar la resolución a nota (A9), la fila se verifica contra existencia física de cualquier archivo (p.ej. `[[config.toon]]` en `30-resources/vibe-coding/00-index.md` apunta a un asset real) — el check dice "archivo inexistente", no "nota inexistente".
8. **Extracción de links de cuerpo.** Se excluyen fenced code blocks e inline code spans (Obsidian no renderiza wikilinks dentro de código); reduce falsos positivos de links ilustrativos (`` `[[...]]` ``, `` `[[Proyecto raíz]]` ``) detectados en la primera pasada sobre el vault real.
9. **Records.** Schema del spec sección 6 + campos aditivos (`details`, `evidence`, `thresholds`, `severity` por check). `results_file` se añade sólo al stdout (el archivo no puede autoreferenciarse), paridad con context-budget. `git_head` informativo vía `git rev-parse` en VAULT_ROOT.

## 2. Evidencia de los 7 requisitos del spec sección 5

1. **Suite completa sobre el vault real con counts y findings por check**: `results/run-20260913-071448.json` (sección 3 abajo). Exit 1 por FAILs reales registrados (no se corrigen).
2. **FAIL/WARN demos en tempdir**: `selftest.py :: test_positivos_por_check` — FAIL demos para CL-01 (active+superseded_by), CL-06 (RIO/rio), CL-14 (fila `[[no-existe-cl14]]`), CL-18 (router → destino deprecated); WARN demos para CL-08 (alias duplicado), CL-10 (`archive/legacy/`), CL-12 (`[[nota-fantasma]]` + ambiguo), CL-19 (resource active sin `last_verified`). Todos los checks tienen caso positivo y negativo.
3. **Input malformado → SKIP/WARN motivado, nunca traceback**: `test_input_malformado` (frontmatter sin cerrar, bytes binarios, frontmatter con líneas raras, wikilink sin cerrar) + try/except por check en `run_checks` con SKIP `no ejecutable: <tipo>: <msg>` siempre motivado. Verificado también a nivel suite: `counts.skip == 0` ante malformado simple.
4. **Determinismo**: `test_determinismo` — dos `run_suite(write=False)` sobre el mismo vault producen JSON idénticos salvo `run`/`results_file` (comparación canónica con sort_keys).
5. **Baseline `git_head` informativo en VAULT_ROOT**: presente en el record (`git_head` del run final: `c94d99483db5…`); `test_git_head_y_schema_record` verifica la key y el schema del record.
6. **`git status` final limpio fuera del write scope**: verificado (sección 5); los únicos paths nuevos/mutados son los del write scope.
7. **Desduplicación demostrada**: además de los asserts del selftest (CL-02 omite memory/internal y cita al doctor), el run real registra dedup_cites en 13 de 20 checks (CL-01, CL-02 implícito, CL-03, CL-04, CL-07, CL-08, CL-09, CL-11, CL-12, CL-13, CL-14, CL-15, CL-16, CL-17, CL-18, CL-19, CL-20) con conteos de omisión en evidencia (p.ej. CL-18: "8 en set fijo M16 (omitidos)").

Resultado del selftest: **8/8 PASS** (`positivos_por_check`, `negativos_vault_limpio` (20 PASS), `exclusion_fixtures`, `determinismo`, `marker_ausente` (exit 2), `check_y_category_filters` (+exit 2 con check desconocido), `input_malformado`, `git_head_y_schema_record`).

## 3. Primera ejecución real (2026-09-13, run-20260913-071448)

Corpus vivo: 853 notas (`iter_vault_md` = 877 − 5 `_shared/fixtures` − 19 fixtures entity-lifecycle). Counts: **PASS 6 · FAIL 5 · WARN 9 · SKIP 0 · findings 1003**. Comando reproducible: `python3 80-agents/tools/canonical-linter/canonical_linter.py --vault-root <VAULT_ROOT>` (exit 1 por FAILs registrados).

| Check | Veredicto | Findings | Resumen de hallazgos (paths reales) |
|---|---|---|---|
| CL-01 | PASS | 0 | `supersedes`+active detectado como sucesión canónica (sin hallazgo, decisión 3). |
| CL-02 | PASS | 0 | Las notas superseded reales llevan `superseded_by`; slice memory/internal omitido por dedup doctor. |
| CL-03 | WARN | 1 | `30-resources/runbooks/signals-code-review.md:28` — `indexable: true` + `index_priority: high` en estado superseded (A3). |
| CL-04 | PASS | 0 | Todos los wikilinks de sucesión resuelven. |
| CL-05 | WARN | 2 | `30-resources/applications/rio-frontend.md:4`, `rio-materializer.md:4` — deprecated sin puntero estructurado en frontmatter (cumplen vía callout: WARN documental, nunca FAIL). |
| CL-06 | FAIL | 22 | Colisiones casefold: 6 estructurales (`00-index` ×13, `skill` ×48, `readme` ×11, `log` ×11, `index` ×3, `runbook` ×2) + 16 de identidad: réplicas Meli (`SIG-610 —…`, `Playmaker — Doble dispatch…`, `Onboarding Signals`, `Vulnerabilidades WebSec — RIO Foundation`), `echo forge wfm dashboard` (`10-projects/Echo Forge/agentes/` vs `30-resources/dashboards/echo-forge/`), `trading` (`20-areas/Trading.md` vs `30-resources/aranea/02-servicios/trading.md`), memorias duplicadas (`2026-09-06-echo-forge-finalist-model-v2` interno vs público; `qkvs-save-version-zero…` y `durable-retester…` en `known-error/rio|symphony` vs `known-errors/`). |
| CL-07 | PASS | 0 | Sin slugs duplicados. |
| CL-08 | WARN | 42 | Alias duplicados, casi todos entre réplicas de los mismos directorios Meli (p.ej. `Agent Memory System` en `10-projects/Personal/AGENTS OS/AGENTS OS.md` y `80-agents/agents-os/agents-os.md`; `C1 C2 Finalist V2`, `Contrato canónico Backup/DR`). |
| CL-09 | WARN | 1 | `40-archive/agents-os-drafts/_drafts/Agent Memory Properties.md:8` — copia archivada con `indexable: true` + `index_priority: high` (A7). |
| CL-10 | WARN | 5 | `archive/projects/meli/**` (Onboarding Signals, Playmaker — Doble dispatch, SIG-610 ×2, Vulnerabilidades WebSec) — A1: entra al corpus Graphify como notas vivas. |
| CL-11 | FAIL | 337 | Routing frontmatter roto, concentrado en: `[[Symphony]]` (85, en `entities` de contratos Echo Forge — concepto sin página), `[[xKoRx/symphony]]` (75, repo referenciado como entidad), `[[EchoForgeTradeListExporter]]` (16), `[[symphony]]` (13), `[[Onboarding Signals]]` (12, ambiguo por réplicas), `[[sqx-watcher]]`, `[[sqx-worker]]`. |
| CL-12 | WARN | 465 | Cuerpo: `[[Fuentes — Workspace de repositorios]]` (30), `[[Onboarding Signals]]` (25, ambiguo), `[[00-index]]` (12+9, ambiguo), `[[2026-09-06-echo-forge-finalist-model-v2]]` (11, ambiguo), `[[meli-agent-dev]]`/`[[aranea-agent-dev]]` (los routers no son basenames de nota ni alias), `[[Symphony]]` (7), notas de sesión con colisión. |
| CL-13 | WARN | 108 | Links vivos → archivadas: cluster `10-projects/Meli/Crear Context` (SPEC archived), links a `30-resources/runbooks/signals-code-review.md` (superseded), réplicas `archive/projects/meli/`. |
| CL-14 | FAIL | 3 | `30-resources/aranea/00-index.md:125,128,129` — filas hacia `agent-project-00` (renombrado), `backup-policy`, `backup-inventory-template` inexistentes. |
| CL-15 | FAIL | 4 | `applications/00-index.md:43,45` (rio-frontend, rio-materializer deprecated listados), `knowledges/00-index.md:40` (signals-knowledge deprecated), `methodologies/sdd/00-index.md:52` (fuente superseded listada como vigente). |
| CL-16 | PASS | 0 | INDEX.md sin destinos archive ni estados de vida; existencia deduplicada (REGISTRY-DISK-PARITY/doctor). |
| CL-17 | PASS | 0 | Todos los paths citados por bootstrap/constitución/continuidad/INDEX/perfil resuelven a disco. |
| CL-18 | FAIL | 1 | `30-resources/runbooks/signals-code-review.md` — destino del Minimal Read del router meli (`[[signals-code-review]]` en el cuerpo del router) en estado superseded: el mecanismo de routing enlaza la página retirada en lugar de `signals-code-review-runbook`. 8 destinos omitidos por dedup M16. |
| CL-19 | WARN | 7 | `30-resources/methodologies/data-mesh.md`, `30-resources/vibe-coding/{agents-v2,context-v2,prompts-v2,rules-toon,sdd-prompts-pack-v4}.md`, `30-resources/knowledges/claude-skills.md` — activos sin `last_verified` (dato de freshness). |
| CL-20 | WARN | 5 | `memory_state: archived` en notas `known_error`/`doc` bajo `80-agents/memory/internal/{agent-memory,known-errors}/` — uso informal del campo fuera de agent_memory. |

## 4. Hallazgos de sistema (sólo registrar; decisión del owner)

- **A1**: `archive/` raíz no declarado, con réplicas Meli dentro del corpus Graphify (CL-10, 5 directorios). Decisión pendiente: migrar a `40-archive/`, declarar la raíz o excluirla.
- **Router meli enlaza un runbook superseded** (CL-18): `30-resources/agents/skills/meli-agent-dev/SKILL.md` → `[[signals-code-review]]` (superseded) en vez de `[[signals-code-review-runbook]]`.
- **Índices wiki con filas no vigentes** (CL-15): applications (2 deprecated listadas), knowledges (1), methodologies/sdd (fuente superseded). Y filas rotas en `aranea/00-index.md` (CL-14).
- **Identidad duplicada por réplicas de directorio** (CL-06/CL-08/CL-12/CL-13): SIG-610, Playmaker — Doble dispatch, Onboarding Signals, Vulnerabilidades WebSec viven bajo `10-projects/Meli/`, `archive/projects/meli/` y `40-archive/projects/meli/`; memorias duplicadas entre `agent-memory/` y `public/{decision,known-error,known-errors}/`.
- **Concepto sin página**: `[[Symphony]]`/`[[symphony]]` (98 referencias de routing) y entidades técnicas (`xKoRx/symphony` como wikilink de entidad) sin nota canónica que resuelva.
- **Contrato vs práctica en s1** (A3): runbook federado con `status` fuera de contrato + `index_priority: high` (CL-03; lint.py ya cubre el forbidden-field).
- **Freshness**: 7 páginas resource/methodology activas sin `last_verified` (CL-19, dato, no veredicto).
- **Fixtures vs .graphifyignore**: el corpus Graphify incluye las fixtures sintéticas que este linter excluye (A8; diferencia registrada).

## 5. Verificación y estado git

- `git status --porcelain` inicial: limpio (sin salida). Final: sólo los paths del write scope (`80-agents/tools/canonical-linter/{canonical_linter.py,selftest.py,README.md,results/run-20260913-071448.json,artifacts/p3-implementation-notes.md}`).
- Selftest: 8/8 PASS con cleanup `rmtree` en `finally` (tempdirs fuera del vault).
- Determinismo verificado; sin mutación del vault; sin red/DB/daemon; sin `__pycache__` fuera del write scope.

## 6. Limitaciones y riesgos

- **Parser de frontmatter** (harness, regex simple): soporta listas multilínea y quoting básico; YAML avanzado (claves anidadas, bloque `|`) no se interpreta. Campos con wikilink fuera de ROUTING_FIELDS (p.ej. `sources`) no los verifica CL-11 (limitación declarada; CL-12 sólo cubre cuerpo).
- **Ruido mecánico honesto**: CL-06 reporta también las colisiones estructurales (`SKILL.md` ×48, `00-index.md` ×13, etc.) — son colisiones casefold reales mandadas por autoridad; se anotan en evidencia y la decisión es del owner (sin whitelist inventada). CL-12/CL-11 reportan cada link no resolvente, incluidos nombres de skill (`[[meli-agent-dev]]`) que en Obsidian tampoco resuelven.
- **CL-18 y el set M16**: el complemento exacto de CTX-12 depende de que M16 siga cubriendo su set fijo; si context-budget cambia su alcance, los `dedup_cites` deben revisarse.
- **Nombres de módulo cacheados**: importar harness/schema en el mismo proceso desde dos vaults distintos reutiliza el primer módulo cargado (contenido idéntico; el selftest precalienta desde el vault real para rutas estables).
- **Performance**: O(notas × links) con caches; run real ≈1s. Sin riesgo conocido en vaults de este tamaño.
- El linter NO sustituye a hygiene-review/relation-maintenance (siguen siendo las skills de ejecución con criterio); los mecaniza corpus-wide y sus salidas quedan como findings, nunca auto-fix.

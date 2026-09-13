# Canonical / Deprecation Linter (AGENTS OS, PHASE 3 — P3-B)

Linter determinista de higiene canónica y deprecación para AGENTS OS. Es el tercer pilar junto al Conformance Harness (correctness/contracts) y context-budget (efficiency/isolation): este pilar cubre **knowledge hygiene** — canonicalidad, deprecación, archive y referencias. Implementa los checks CL-01..CL-20 ratificados en `artifacts/p3-canonical-linter-spec.md` a partir del modelo de `artifacts/p3-canonical-model.md`.

Propiedades: Python 3.9+ stdlib only, determinista, read-only sobre todo el vault salvo `results/` propio, sin daemon/DB/red. **Nunca auto-corrige**: reporta findings con `recommended_action` propuesto para el owner.

## Qué chequea

| ID | Categoría | Regla (resumen) | Severidad | Autoridad principal |
|---|---|---|---|---|
| CL-01 | STATUS | Nota `active` con `superseded_by` no vacío (segunda autoridad activa) | FAIL | metadata-schema; 00-RESOURCE-WIKI |
| CL-02 | DEPRECATION | `superseded` sin `superseded_by` no vacío | FAIL agent_memory/source, WARN resto | note-types; doctor Check 7; 00-RESOURCE-WIKI |
| CL-03 | STATUS | Estado no-vigente/en-retiro con `indexable: true` + `index_priority` critical/high | WARN | constitución Memoria Interna; doctor Check 7 |
| CL-04 | DEPRECATION | `supersedes`/`superseded_by` cuyo wikilink no resuelve (inexistente FAIL, ambiguo WARN) | FAIL | schema-contract (canonical_wikilink); hygiene-review |
| CL-05 | DEPRECATION | `status` deprecated/deprecating sin `superseded_by` ni wikilink en `related`/`entities` | WARN | 00-RESOURCE-WIKI (el callout de cuerpo cuenta: nunca FAIL) |
| CL-06 | CANONICALITY | Dos notas vivas con basename idéntico casefold | FAIL | convenciones; context-retrieval Hard Rules |
| CL-07 | CANONICALITY | Dos notas vivas con el mismo `slug` no vacío | FAIL | convenciones; note-types |
| CL-08 | CANONICALITY | Mismo alias en dos notas vivas S2 o de memoria pública | WARN | hygiene-review (proposal-only) |
| CL-09 | ARCHIVE | Nota bajo `40-archive/` con `load_policy: always` o índice critical/high | WARN | doctor Check 3; bootstrap Hard Rules; materializer |
| CL-10 | ARCHIVE | Directorio con forma de archive fuera de `40-archive/` y no declarado | WARN report-only | agents-os.md (A1) |
| CL-11 | REFERENCES | Wikilink roto en campos de routing de frontmatter (`area`, `project`, `application`, `entities`, `related`, `parent`) | FAIL | convenciones; doctor Check 2 (manual) |
| CL-12 | BROKEN LINKS | Wikilink de cuerpo que no resuelve | WARN | hygiene-review; relation-maintenance |
| CL-13 | REFERENCES | Nota viva que enlaza a nota ARCHIVED (path `40-archive/` o estado archived/superseded) | WARN | relation-maintenance (unless intentional) |
| CL-14 | ROUTING | Fila de un `00-index.md` de dominio wiki activo apuntando a archivo inexistente | FAIL | 00-RESOURCE-WIKI (una fila por vigente) |
| CL-15 | ROUTING | Fila de un `00-index.md` de dominio activo apuntando a página no vigente o archivada | FAIL | 00-RESOURCE-WIKI (el índice deja una sola entrada vigente) |
| CL-16 | ROUTING | `80-agents/skills/INDEX.md` con destino bajo `40-archive/` (FAIL) o con estado de vida no vigente (WARN) | FAIL/WARN | bootstrap paso 3 |
| CL-17 | HOT-PATH | Paths VAULT_ROOT-relativos entre backticks en archivos DEFAULT-LOADED que no existen en disco | FAIL | constitución regla 11; doctor Check 1 (extensión de alcance) |
| CL-18 | HOT-PATH | Destino de routing del hot path (Minimal Reads de routers/prefs, cold steps) no vigente o archivado | FAIL | bootstrap Hard Rules; constitución regla 10 |
| CL-19 | METADATA | `type: resource`/`methodology` con `status: active` sin `last_verified` | WARN | 00-RESOURCE-WIKI (freshness event-driven) |
| CL-20 | METADATA | `memory_state` en nota cuyo tipo declarado ≠ `agent_memory` | WARN report-only | schema-contract; metadata-schema |

Sólo MACHINE-DETERMINISTIC produce FAIL (lista completa en el spec sección 2). "No parece actualizado" no es un check; la duplicación semántica no existe como check (sólo los proxies CL-06/CL-07/CL-08).

## Cómo correrlo

```bash
# suite completa (escribe results/run-<timestamp>.json y imprime resumen)
python3 80-agents/tools/canonical-linter/canonical_linter.py

# JSON a stdout + results; resumen a stderr
python3 80-agents/tools/canonical-linter/canonical_linter.py --json

# run dirigido por el operador: un solo check o una categoría
python3 80-agents/tools/canonical-linter/canonical_linter.py --check CL-14
python3 80-agents/tools/canonical-linter/canonical_linter.py --category ROUTING

# vault distinto al autodetectado
python3 80-agents/tools/canonical-linter/canonical_linter.py --vault-root /ruta/al/vault

# selftest (fixtures temporales fuera del vault; cleanup automático)
python3 80-agents/tools/canonical-linter/selftest.py
```

Exit codes: `0` sin FAIL · `1` con al menos un FAIL · `2` sin VAULT_ROOT (marker `80-agents/agents-os/agents-os.md` ausente), check/categoría desconocidos.

VAULT_ROOT se autodetecta subiendo desde la carpeta de la tool hasta encontrar el marker, igual que el harness y context-budget. El motor importa el harness y `load_contract()` resolviendo sus rutas relativas a VAULT_ROOT en runtime (fork prohibido, precedente context-budget).

## Algoritmo de resolución de wikilinks (A9, ratificado)

Target del link = texto antes de `|` (label) y de `#` (heading/bloque); `[[^bloque]]` y targets vacíos se ignoran; los headings no se validan (sólo la nota). Orden de resolución:

1. **Path relativo exacto** desde el directorio del archivo origen.
2. **Path VAULT_ROOT-relativo** (constitución regla 11) para targets con `/`.
3. **Basename exacto** case-sensitive único sobre corpus vivo + `40-archive/`.
4. **Basename casefold único**.
5. **Alias declarado exacto** (frontmatter `aliases`).

Múltiples candidatos sin match único → hallazgo WARN "ambiguo" con la lista de candidatos. El índice de resolución cubre **corpus vivo + `40-archive/`**: journal, packaging (`30-resources/agents-os/`) y resultados derivados NO son destino canónico (`agents-os.md`: "auditoría o distribución, nunca autoridad vigente"; relation-maintenance: no enlazar sessions/logs) — un link hacia ese material se reporta como no resuelto. En el escaneo de cuerpo se excluyen fenced code blocks e inline code spans (Obsidian no renderiza wikilinks dentro de código). Autoridades citadas: `agents-os-hygiene-review/SKILL.md` (Link And Alias Checks) y `graphify-contract.md` (semántica vault-wide).

Clase de vida (A5 ratificado): `no_vigente = memory_state ∈ {superseded, archived} ∪ status ∈ {archived, superseded}` (siempre dentro del enum por tipo resuelto vía `load_contract()`); `deprecated`/`deprecating` = sub-clase "en retiro". Para tipos s1 (donde `status` está prohibido) o tipo ausente, un `status` del set se cuenta como estado observado con dedup-cita a `lint.py` (decisión A3). `superseded_by:`/`supersedes:` vacíos se tratan como ausentes.

## Semántica de resultados

Veredictos PASS / FAIL / WARN / SKIP idénticos al harness; SKIP siempre con motivo; UNKNOWN nunca se convierte en PASS. Sin gate entre checks (todos estáticos); pre-flight: marker ausente → exit 2; harness/schema-contract/rules no importables → sólo los checks dependientes van a SKIP con motivo. Cada finding conserva `check_id, category, status, severity, path, line, observed, expected, evidence, confidence (EXACT|INFERRED), recommended_action, authority`. El record (`results/run-<timestamp>.json`) incluye `model` (clase A5 + algoritmo A9), `thresholds` declarados, `observations`, `ambiguities` y `dedup_cites` por check.

Desduplicación por scope (spec sección 2 y modelo sección 6): el linter NO re-emite lo ya cubierto por lint.py (required/empty/field-types/bad-status/forbidden-field/tags/unknown-type/template-boundary), el doctor (club always, INDEX↔disco, lifecycle continuity bajo memory/internal, paths de AGENTS.md), el harness L0 (REGISTRY-DISK-PARITY, CLOSED-CLUB-ALWAYS, DUAL-REGISTRY-DOMAIN-SYNC, vocabulario load_policy) ni context-budget CTX-12/M16 (frontmatter del set fijo del hot path) y CTX-13/M14 (duplicación textual). Cuando un scope solapa, el check cita el check-id ajeno en `dedup_cites` y omite el finding.

## Qué NO chequea

- "No parece actualizado" como criterio general (00-RESOURCE-WIKI prohíbe la cadencia global; CL-19 sólo reporta la presencia de `last_verified`).
- Duplicación semántica de contenido (regla 5): sólo proxies mecánicos CL-06/CL-07/CL-08; la competencia de fuentes canónicas es HUMAN-REVIEW proposal-only (hygiene-review).
- Elección del sucesor correcto en deprecaciones sin campo (CL-05 es WARN con proxy declarado).
- Drift entre callout renderizado y frontmatter; obediencia real de carga en sesión viva (UNOBSERVABLE); vigencia factual de notas activas.
- Duplicados cross-repo declarados fuera del vault (p.ej. aranea-mcps-expert).
- Existencia de filas de `INDEX.md` de skills: cubierta por L0 REGISTRY-DISK-PARITY y doctor (CL-16 sólo añade destinos archive y estados de vida).
- Vocabulario `load_policy` (WARN ya declarado del harness C09): los checks sólo consumen el valor (CL-09).
- Layout de la raíz del vault (A2: sin autoridad que lo fije).

## Cómo agregar un check

1. Añadir la función `cl_NN(ctx)` en `canonical_linter.py` con la firma `(ctx) -> (details, findings, dedup_cites, evidence)`; construir findings con `finding(...)` (cada regla cita su autoridad real; nunca decisión de producto sin autoridad).
2. Registrarla en `CHECKS` con `(id, categoría, severidad máxima, función, dependencias)` — las dependencias (`contract`, `harness`, `rules`) gobiernan el SKIP motivado.
3. Clasificarla: sólo MACHINE-DETERMINISTIC puede producir FAIL; HEURISTIC como máximo WARN (declarar el umbral/proxy en `THRESHOLDS`).
4. Verificar que no solape un scope ya cubierto (lint.py / doctor / harness L0 / context-budget); si solapa, omitir el finding y citar el check-id ajeno en `dedup_cites`.
5. Añadir caso positivo y negativo en `selftest.py` (fixtures en tempdir, nunca en el vault) y actualizar la tabla de este README.

## Limitaciones

- El parser de frontmatter es el del harness (regex simple, sin PyYAML): los valores multilínea de listas se soportan vía `parse_frontmatter`; los campos no listados en ROUTING_FIELDS con wikilinks (p.ej. `sources`) no se verifican por CL-11 (queda para CL-12 sólo si están en el cuerpo).
- CL-06 reporta toda colisión casefold sin whitelist: los grupos estructurales (SKILL.md, 00-index.md, log.md, README.md) son filenames por-directorio mandados por autoridad y se anotan como tales en la evidencia; la decisión de si son defecto es del owner.
- CL-05 no puede identificar AL sucesor desde un callout de cuerpo (proxy frontmatter declarado): un caso conforme vía callout (p.ej. rio-frontend) sigue apareciendo como WARN documental.
- CL-10 es heurístico (A1: ninguna autoridad fija la lista cerrada de raíces de archive); excluye `80-agents/memory/internal/` (scope del doctor) y directorios `sources/` (provenance de la wiki, donde `superseded` es lifecycle normal).
- Los findings sobre el vault real se registran, no se corrigen: las correcciones canónicas son propuestas (`recommended_action`) para el owner. Ver `artifacts/p3-implementation-notes.md` para decisiones de implementación y resultados de la primera ejecución.

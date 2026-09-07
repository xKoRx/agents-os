# tools/ — Bitácora

> Append-only, cronológico. Formato: `## [YYYY-MM-DD] <op> | <detalle>` con `<op>` ∈ `ingest | query | lint`.
> `grep "^## \[" log.md | tail -5` → últimas operaciones.

## [2026-07-04] ingest | Generalización del patrón wiki a `tools/`

- Creado `00-index.md` canónico (catálogo curado: [[graphify]], [[strategyquant-x]]).
- `README.md` demovido de `type: index` a doc de convenciones (`tools-conventions`) para
  evitar dos catálogos que compitan por el mismo dominio (regla "una fuente por hecho").
- Dominio `tools/` queda alineado con `applications/` (00-index.md + log.md).

## [2026-07-05] ingest | Reconciliación de `graphify` (wikilinks vault-aware + drift de setup)

- Fuentes ingeridas: [[graphify-contract]], known-error
  [[graphify-markdown-wikilink-and-backend-gaps]], proyecto [[Economía de Tokens]],
  continuidad interna `2026-07-04-graphify-obsidian-build-continuity`, + verificación
  contra el sistema vivo (Mac).
- **Capacidad añadida:** sección "Wikilinks del vault (fork vault-aware)" —
  `[[wikilinks]]` → edges `references` (852/852 validados 2026-07-04; 853/0 colgantes en la
  salida viva 2026-07-05) + caveat de query `affected "<nota>.md" --relation references`.
- **Drift de setup reconciliado:** host VM Hermes → **Mac**; path
  `~/.local/share/graphify-venv/` → **build aislado del fork** `~/.local/share/graphify-obsidian/venv/`
  (`graphify 0.9.5`); wrapper `~/.local/bin/graphify-obsidian` → **`~/bin/graphify-obsidian`**;
  `graphify`/`graphify-personal` confirmados en PyPI `graphifyy 0.8.39` (sin wikilinks);
  wrapper legacy `graphify-aranea` retirado; cifras del grafo y fecha de salida viva → 2026-07-05.
- Solo doc/wiki; no se tocó código ni wrapper. Change_log canónico en
  `80-agents/journal/logs/2026-07-05-graphify-resource-page-reconciliation.md`.

## [2026-07-07] ingest | `graphify-obsidian` 0.9.6 — enlaces tipados (scoped) + reconciliación de versión

- **Capacidad añadida (v0.9.6, commit `220fb0a`):** enlaces tipados en el cuerpo. Dentro de
  `## Relaciones`, un verbo canónico (`consume`, `decora`, `depende de`, `expone`,
  `reemplaza a`) antes del wikilink define el `relation` del edge (espacio→`_`). Solo se tipa
  ahí; fuera cae a `references` (una negación "no depende de [[X]]" NO forja el edge). Sin
  variantes bare. Contrato canónico en el ADR [[token-economy-indexing-architecture]].
- **Versión reconciliada:** build obsidian `0.9.5`→**`0.9.6`** en la página, runbook
  [[graphify-obsidian-install]] y `95-graphify/dist/` (wheel nueva desplegada, 0.9.5 removida;
  `BUILD.md` + nuevo `README.md`/changelog). PyPI Work/personal siguen en `0.8.39`.
- Change_log canónico en `80-agents/journal/logs/2026-07-07-typed-links-review-corrections.md`.

## [2026-08-11] ingest | `graphify-obsidian` 0.9.6.post2 — relaciones lossless

- **Capacidad añadida:** el grafo simple conserva el escalar legacy `relation` y agrega `relations` con todas las variantes semánticas del mismo par source-target; `affected`, `path`, `explain` y shortest path MCP consumen la representación completa.
- **Evidencia:** suite completa `2844 passed, 28 skipped`; Ruff verde; wheel SHA-256 `fd36205f41f9d9455c67f40cca1d191e1662b7c6f7146a9aebe23e56c57dc4a8`; instalación aislada verificada como `0.9.6.post2`; gate vault `0/0`; reindex `5138/6133`; Context Router `14/14` sin misses.
- Página [[graphify]], índice de tools, runbook [[graphify-obsidian-install]], known error [[graphify-frontmatter-alias-and-typed-edge-dedup-gaps]] y artefactos bajo `95-graphify/dist/` sincronizados. Change log canónico: [[2026-08-11-graphify-typed-relations-entity-updated]].

## [2026-08-11] lint | Auditoría base de AGENTS OS Fase 4

- Catálogo de tools completo; [[30-resources/tools/README|README]] confirmado como convención enlazada y no como tool; Graphify limpio y actualizado.

## [2026-08-26] ingest | local-agents-pipeline-cli → página canónica de tool + provenance + idea

- Ingresado el repo local `local-agents-pipeline-cli` desde `~/fuentes`, checkout `master` en `ac48d12`, remoto `melisource/fury_local-agents-pipeline-cli`.
- Creadas [[local-agents-pipeline-cli]], [[local-agents-pipeline-cli-source]] y [[2026-08-26-local-agents-pipeline-cli-review-gate]]; el repositorio completo permanece fuera del vault según [[Fuentes — Workspace de repositorios]].
- Verificación: notas nuevas con lint estricto verde; build OK, lint con 0 errores/11 warnings, 27 suites/426 tests OK y smoke de `list`/`assemble --dry-run`; se documentó que `feature/script-agents` no pertenece a `master`.
- Reindex global bloqueado por deuda all-vault ajena (12 errores/6 warnings); no se modificaron las fuentes del bloqueo.

## [2026-09-01] ingest | ads-signals-skills-marketplace → página canónica de tool + provenance

- Ingresado el repo `ads-signals-skills-marketplace` desde [[Fuentes — Workspace de repositorios]]; el repositorio completo permanece fuera del vault.
- Creadas [[ads-signals-skills-marketplace]] y [[ads-signals-skills-marketplace-source]]; actualizado el índice de tools con su contrato de catálogo, publicación y validación.
- Verificación sobre `feature/human-first-technical-writing@d1515df`: validador del marketplace verde con 3 skills, `git diff --check` verde y PR `melisource/fury_ads-signals-skills-marketplace#1` abierto con Code Reviewer aprobado sin issues.

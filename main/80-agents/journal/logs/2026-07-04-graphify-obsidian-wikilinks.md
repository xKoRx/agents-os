---
type: change_log
scope: global
created: 2026-07-04
updated: 2026-07-04
area: "[[Personal]]"
project: "[[Economía de Tokens]]"
entities:
  - "[[graphify]]"
  - "[[AGENTS OS]]"
related:
  - "[[token-economy-indexing-architecture]]"
tags:
  - kind/changelog
  - area/personal
  - project/agents-os
  - tech/graphify
---

# 2026-07-04 — graphify-obsidian: resolución de wikilinks vault-aware

Primer PoC de **código** del proyecto [[Economía de Tokens]]. Cierra el gap
"graphify no captura los `[[wikilinks]]` del vault" por la **vía A (fork de
graphify)**, no por un builder standalone.

## Diagnóstico afinado

El hallazgo previo (2026-07-03) era parcial. graphify **sí** tiene
`extract_markdown` (PR #1376) que parsea `[[wikilink]]`, headings y links
inline. El problema real: `_resolve_markdown_link` resuelve el target **relativo
al directorio de la nota** (hermanos). En un vault Obsidian `[[X]]` apunta por
**nombre de nota / alias** a una nota en cualquier carpeta → el edge caía en un
id fantasma que ninguna nota reclama → el grafo del vault se veía sin links pese
a estar densamente enlazado.

## Cambio en graphify (fork)

- Repo `/Users/rjara/fuentes/graphify`, rama `feat/obsidian-vault-wikilinks`,
  commit `9c393b7`. Solo `graphify/extract.py` (+136 líneas). `uv.lock` NO
  tocado; upstream `v8` intacto.
- Añadido resolver **vault-aware**: índice `stem → path` y `alias → path`
  (aliases leídos del frontmatter YAML, parser propio sin dependencia), cache
  por raíz (patrón del resolver de units de Pascal). Los `[[wikilinks]]`
  resuelven vault-wide; inline/ref-links siguen relativos.
- **Gated por `GRAPHIFY_MD_VAULT_ROOT`**: sin la env var, comportamiento
  byte-idéntico a upstream (relative-only). 68 tests de markdown verdes, ruff OK.
- El edge emite la ruta **real resuelta** de la nota destino → el post-pass
  `id_remap` de `extract()` lo canoniza al mismo id que el nodo-archivo destino
  → merge sin fantasmas.

## Compilado aislado + wrapper

- **Build aislado** en venv uv propio: `~/.local/share/graphify-obsidian/venv`
  (snapshot del fork, `graphify 0.9.5`, extras `[all]`). NO es `uv tool` para no
  pisar el `graphifyy` de PyPI: `graphify` (Work) y `graphify-personal` siguen en
  **0.8.39 intactos**. Aislamiento verificado.
- Wrapper `~/bin/graphify-obsidian`:
  - `REAL_BIN` → el build aislado (con guard si falta).
  - `export GRAPHIFY_MD_VAULT_ROOT="$TMP_DIR"` antes de extraer (los workers lo
    heredan).
  - rsync excluye ahora también `graphify-out/` / `graphify-out-*` — arrastrar
    uno viejo metía su caché AST (versionada por esquema, no por versión de
    paquete) y `update` reusaba extracciones sin wikilinks. Sin caché en el tmp
    la extracción es fresca sobre todas las notas.

## Validación (vault real, 576 notas)

- **852/852 reference edges resueltos, 0 colgantes.**
- Backlinks de hubs: `java-polycard-sdk` 9, `vpp-backend` 9, `vis-octopus-lib`
  7, `search-middleware` 14 (cross-folder por nombre y por alias).
- Criterios de aceptación del proyecto: **1 explain OK, 2 affected ≥3 OK
  (9+ vía file-node), 3 path OK, 4 sin nodos de trash/archive/json OK.**

## Caveat conocido (query de backlinks)

La consulta correcta de backlinks es
`graphify-obsidian affected "<nota>.md" --relation references` — con el sufijo
`.md` **y** la relación explícita (`references` no está en las relaciones por
defecto de `affected`). `affected "<nombre-pelado>"` (sin `.md`) cae en el nodo
**heading** `# nombre` cuando el H1 == filename → resultado vacío. Candidato a
mejora futura (dedupe H1↔file o ranking file-first), fuera de scope de este PoC.

## Pendiente

Capa de **contexto-mínimo con tope de tokens** sobre el link-graph + medición
con `graphify benchmark`.

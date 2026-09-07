---
type: change_log
scope: global
created: 2026-07-05
updated: 2026-07-05
area: "[[Personal]]"
project: "[[Economía de Tokens]]"
entities:
  - "[[graphify]]"
  - "[[AGENTS OS]]"
related:
  - "[[graphify-contract]]"
  - "[[graphify-markdown-wikilink-and-backend-gaps]]"
  - "[[token-economy-indexing-architecture]]"
tags:
  - kind/changelog
  - area/personal
  - project/agents-os
  - tech/graphify
---

# 2026-07-05 — Reconciliación de la página de recurso `graphify`

Pasada dedicada de **resource-wiki** sobre `30-resources/tools/graphify.md` (fechada
2026-07-02, quedó incompleta/desfasada). Solo **doc/wiki**: no se tocó código, fork ni
wrapper. Fuente de verdad usada: [[graphify-contract]], known-error
[[graphify-markdown-wikilink-and-backend-gaps]], ADR [[token-economy-indexing-architecture]],
proyecto [[Economía de Tokens]], continuidad interna
`2026-07-04-graphify-obsidian-build-continuity`, más verificación contra el sistema vivo (Mac).

## Verificación del sistema vivo (Mac, 2026-07-05)

- `~/bin/graphify-obsidian` → build **aislado del fork** `~/.local/share/graphify-obsidian/venv/bin/graphify`, **`graphify 0.9.5`** (único con wikilinks vault-aware). Confirmado con `--version`.
- `~/.local/bin/graphify` → PyPI `graphifyy` **0.8.39** (lo usan `graphify` Work y `graphify-personal`). Confirmado con `--version`.
- `~/.local/share/graphify-venv/` (lo que afirmaba la página) **NO existe**.
- `~/.local/bin/graphify-obsidian` (wrapper que afirmaba la página) **NO existe**; el wrapper real es `~/bin/graphify-obsidian`.
- `graphify-aranea` legacy **ya no está** en `~/bin`.
- Salida viva `95-graphify/obsidian/graph.json` (2026-07-05): **3311 nodos / 3898 edges (3038 `contains`, 853 `references`, 7 `calls`) / 276 comunidades, 100% EXTRACTED**; edges `references` sin colgantes (853/0).

## Cambios en `30-resources/tools/graphify.md`

1. **Wikilinks vault-aware (capacidad ausente):** nueva sección "Wikilinks del vault (fork
   vault-aware)" — `[[wikilinks]]` → edges `references` (852/852 validados 2026-07-04, 853/0
   en la salida viva), grafo relaciona por links no por tags, builder standalone descartado,
   sin `GRAPHIFY_MD_VAULT_ROOT` = idéntico a upstream. Incluye el **caveat de query**:
   `graphify-obsidian affected "<nota>.md" --relation references` (con `.md` **y** la relación
   explícita; nombre pelado → H1 vacío; no usar file-node id).
2. **Drift de setup reconciliado (VM Hermes → Mac):** frontmatter (`installed_host`,
   `installed_path` al venv aislado, `installed_version_obsidian: 0.9.5`,
   `installed_version_pypi: 0.8.39`, `wrapper_path: ~/bin/graphify-obsidian`; quitados
   `installed_in_vm` y `wrapper_legacy`); callout de estado; tabla "Comandos (estado por
   entorno)" reescrita con el backend real de los 3 wrappers; sección "Estado actual" → Mac,
   con bloque de reinstalación del build aislado; instalación histórica corregida
   (`/home/hermes/...` y `graphify . --mode deep` → wrapper `graphify-obsidian update`).
3. **Cifras/fechas stale:** grafo vivo y "última salida viva" → 2026-07-05; nota de versión
   del CLI marcada vigente en 0.9.5.
4. **Cruces canónicos:** añadidos a `related:` y a la sección Links (known-error, proyecto, ADR).

## Otros archivos

- `30-resources/tools/00-index.md`: `updated`/`reviewed` → 2026-07-05, "Última ingesta"
  actualizada. (La fila del catálogo ya mencionaba el fork/wikilinks; sin cambio de contenido.)
- `30-resources/tools/log.md`: entrada `[2026-07-05] ingest`.

## Validación

- Los 3 wikilinks nuevos resuelven a notas existentes (`graphify-markdown-wikilink-and-backend-gaps.md`,
  `token-economy-indexing-architecture.md`, `10-projects/Economía de Tokens/Economía de Tokens.md`).
- No se contradice el diagnóstico canónico de wikilinks; la página ahora lo refleja.
- Pendiente de operación (no de esta pasada): reindex de Graphify para que los nuevos edges
  `references` de `related:` entren al grafo.

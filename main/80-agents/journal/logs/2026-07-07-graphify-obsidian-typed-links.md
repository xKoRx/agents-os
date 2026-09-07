---
type: change_log
scope: global
created: 2026-07-07
updated: 2026-07-07
area: "[[Personal]]"
project: "[[AGENTS OS]]"
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

# 2026-07-07 — graphify-obsidian: soporte de enlaces tipados en el cuerpo

Implementación de enlaces tipados en el parser de Markdown de `graphify-obsidian`. Permite extraer relaciones específicas del grafo a partir de prefijos verbales en los enlaces de Obsidian.

## Rationale
Evita depender de modelos de lenguaje (LLM) costosos y estocásticos para mapear la estructura de dependencias duras del vault. Mapea deterministamente verbos a tipos de relación.

## Cambios Aplicados

### Código (Fork)
- Rama `feat/obsidian-vault-wikilinks`, commit en fork `/Users/rjara/fuentes/graphify`.
- Modificaciones en `graphify/extract.py`:
  - Declaración de `_MD_TYPED_WIKILINK_RE` y `_MD_TYPED_INLINE_LINK_RE` con verbos canónicos: `consume`, `decora`, `depende de`, `depende`, `expone`, `reemplaza a` y `reemplaza`.
  - Firma de `add_link` modificada para recibir el parámetro `relation` (por defecto `"references"`).
  - Modificación del bucle de parsing principal en `extract_markdown` para escanear y registrar primero los rangos (`spans`) de enlaces tipados, evitando que el extractor genérico posterior duplique los edges.
  - Reconstrucción de la wheel portátil y distribución en `95-graphify/dist/graphifyy-0.9.5-py3-none-any.whl`.

### Documentación
- Reconciliación en la página del recurso [graphify.md](file:///Users/rjara/obsidian/SecondBrain/main/30-resources/tools/graphify.md) para explicar la sintaxis y comportamiento de los enlaces tipados.

## Validación
- Test suite local `pytest tests/test_claude_md.py` passed.
- Scratch script `test_typed_links.py` validó con éxito que:
  - `consume [[vpp-backend]]` genera relación `consume`.
  - `depende de [[java-polycard-sdk]]` genera relación `depende_de`.
  - `[[search-middleware]]` genera la relación por defecto `references`.
  - `depende [[vis-octopus-lib]]` genera relación `depende`.
- Indexación de prueba en el vault local mediante `graphify-obsidian update` y verificación de edges resultantes en `graph.json` confirmada.

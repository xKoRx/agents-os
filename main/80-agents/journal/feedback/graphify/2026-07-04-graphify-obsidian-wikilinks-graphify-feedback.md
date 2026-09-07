---
type: feedback
scope: graphify
created: 2026-07-04
updated: 2026-07-04
area: "[[Personal]]"
project: "[[Economía de Tokens]]"
entities:
  - "[[AGENTS OS]]"
  - "[[graphify]]"
related:
  - "[[2026-07-04-graphify-obsidian-wikilinks]]"
aliases: []
agent: Claude Opus 4.8 (Claude Code)
session_goal: fork de graphify con extractor de wikilinks vault-aware + build aislado graphify-obsidian
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/graphify
  - project/agents-os
  - agent/system1
---

# Graphify Session Feedback - 2026-07-04 - wikilinks vault-aware

> [!NOTE]
> Sesión atípica: el objetivo fue **modificar** Graphify, no consultarlo. El
> feedback es sobre su arquitectura como base de la modificación.

## Context

- **Agent**: Claude Opus 4.8 (Claude Code).
- **Session goal**: agregar resolución de wikilinks vault-aware y compilar como `graphify-obsidian`.
- **Main entity/topic**: [[graphify]] / [[Economía de Tokens]].

## Utilidad y Valor Aportado

- **¿Qué tan útil fue como base de la modificación? (1-5):** 5. Arquitectura limpia y enchufable: contrato de extractor (`{nodes,edges}`), `validate.py`, post-pass `id_remap` que canoniza ids → el edge de wikilink hace merge sin fantasmas con solo emitir la ruta real. No tuve que tocar el pipeline.
- **Valor vs búsqueda manual:** el `git log` + la dispatch table + el docstring del `id_remap` explicaron el mecanismo exacto de canonización; sin eso habría emitido ids que no mergeaban.
- **Nodos/relaciones cruciales:** la relación `references` y el post-pass de remap (`_make_id(str(path))` y `_make_id(str(path.resolve()))`).

## Fricción y Entorpecimiento

- **Fricción principal:** el **caché AST versionado por esquema, no por versión de paquete**. `update` reusó extracciones stale (arrastradas en un `graphify-out/` viejo) y me dio resultados idénticos al baseline pese al fix. Costó un rato entender que era caché, no código.
- **Ruido/plantillas vacías:** `affected "<nombre>"` cae en el heading `# nombre` cuando H1==filename (colisión) → resultado vacío engañoso. La query correcta es `affected "<nota>.md" --relation references`.
- **Velocidad/budget/fallos:** `update` no acepta `--directed` (grafo del vault queda no-dirigido). `graph.html` se saltea >5000 nodos (no fatal).

## Usabilidad y Comprensión (Know-how)

- **¿Sabía usarla óptimamente?** sí para modificar; para consultar backlinks tardé por el caveat del heading y de `--relation`.
- **¿La doc guió?** `ARCHITECTURE.md` + docstrings del código: excelentes. La ayuda del CLI no aclara que `references` no está en las relaciones por defecto de `affected`.
- **¿Recurrí a comandos manuales?** sí, inspección directa de `graph.json` con Python para validar resolución (más rápido que iterar con el CLI).

## Propuestas de Mejora de la Herramienta

- Invalidar el caché AST cuando cambia el **código del extractor**, no solo el contenido del archivo (o exponer `--no-cache` en `update`).
- `affected`: incluir `references` en las relaciones por defecto (o documentarlo), y desempatar nombre-de-nota vs heading a favor del file-node.
- Permitir `--directed` en `update` para grafos de vault (los wikilinks son direccionales → backlinks reales).

## Estado de integración

Fix mergeado en el fork (rama `feat/obsidian-vault-wikilinks`), gated por
`GRAPHIFY_MD_VAULT_ROOT`, compilado como build aislado `graphify-obsidian`.
Candidato a upstream. Ver log `journal/logs/2026-07-04-graphify-obsidian-wikilinks.md`.

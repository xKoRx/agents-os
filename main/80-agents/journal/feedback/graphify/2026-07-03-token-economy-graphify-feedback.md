---
type: feedback
scope: graphify
created: 2026-07-03
updated: 2026-07-03
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
  - "[[graphify]]"
related:
  - "[[Economía de Tokens]]"
aliases: []
agent: Claude
session_goal: Evaluar Graphify para un sistema de indexación en tokens
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

# Graphify Session Feedback - 2026-07-03 - economía de tokens

## Context

- Agent: Claude
- Session goal: evaluar Graphify como capa de índice del vault y para código.
- Main entity/topic: [[graphify]] / [[Economía de Tokens]]

## Utilidad y Valor Aportado

- Utilidad (1-5): **2 para el vault (markdown), 5 para código.** En su propio repo dio 10.316 nodos / 17.320 edges con call-graph real. En markdown sin LLM es casi inerte.
- Valor vs grep: en código, altísimo (relaciones que grep no ve). En markdown, grep + índice curado le ganan.
- Nodos clave: en código, `explain`/`affected` sobre funciones. En markdown, ninguno útil (no captura wikilinks).

## Fricción y Entorpecimiento

- Entorpeció: sí. Un comando inventado (`update --mode deep`) + `rm graph.json` del runbook borró el grafo. La doc del vault estaba mal.
- Ruido: corpus contaminado (trash/json, 512+170 nodos) — purgado vía `.graphifyignore`.
- Fallos: extract semántico falló (r1 JSON inválido; Gemini free tier 429/quota 0).

## Usabilidad y Comprensión

- ¿Sabía usarlo óptimo? Al inicio no (doc del vault desactualizada). Tras leer el CLI real y el código, sí.
- Documentación: la del vault indujo a error (`--mode deep` va en `extract`, no `update`). Ya corregida.
- ¿Recurrí a grep? Sí, y resultó ser lo correcto para markdown curado.

## Propuestas de Mejora de la Herramienta

- Falta un **extractor estructural de markdown/wikilinks** (hoy solo semántico LLM). Nuestro builder propio lo suple emitiendo su schema.
- El default de backend (`gemini-3-flash`, 5 rpm free) es una trampa; documentar modelo/quota.
- `merge-graphs` + `--mcp` + `benchmark` son piezas muy útiles y poco visibles en la doc.

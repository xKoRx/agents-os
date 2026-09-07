---
type: known_error
scope: project
created: 2026-07-03
updated: 2026-07-04
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[Graphify]]"
  - "[[AGENTS OS]]"
related:
  - "[[graphify]]"
  - "[[token-economy-indexing-architecture]]"
aliases:
  - graphify no captura wikilinks
  - graphify markdown gaps
  - graphify backend pitfalls
  - graphify cli inventado
  - no borrar graph.json
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - area/personal
  - project/agents-os
  - tech/graphify
  - scope/project
---

# Graphify: markdown/wikilinks no capturados + pitfalls de backend

> [!success] Gap de wikilinks SUPERADO 2026-07-04 (vía A: fork `graphify-obsidian`)
> El síntoma/causa de abajo siguen siendo **referencia histórica útil** (explican por qué el
> vault-graph estaba colgante), pero el problema **ya está resuelto**: `graphify-obsidian`
> (fork vault-aware) convierte los `[[wikilinks]]` del vault en edges `references`. El
> **builder standalone** quedó **descartado** en favor del fork (ver § Mitigación). El
> **pitfall operacional** de más abajo (no inventar CLI / no borrar `graph.json`) **sigue
> vigente**. El extract semántico (LLM) sigue parqueado.

## Síntoma (histórico)

- `affected "<entidad>"` / `explain`/`path` vacíos entre notas markdown **pese a existir
  `[[links]]`** en los cuerpos. `_origin` del grafo 100% `ast`.
- `extract --mode deep` falla: con ollama **deepseek-r1** → "LLM returned invalid JSON";
  con Gemini free tier → 429 (`gemini-3-flash` 5 rpm) o quota 0 (`gemini-2.0-flash`).

## Causa (matizada 2026-07-04)

- **El diagnóstico original era parcial.** graphify **sí** parsea `[[wikilinks]]` vía
  `extract_markdown` (PR #1376); el gap real era que upstream los resolvía **relativo a la
  carpeta de la nota** → en un vault (links cross-folder por nombre/alias) los edges quedaban
  colgantes, dando el falso positivo de "no captura wikilinks". No era ausencia de extractor,
  era resolución no vault-wide.
- Los modelos **de reasoning** (r1) envuelven la salida en prosa → rompen el JSON estructurado
  (esto aplica al extract semántico, que sigue parqueado).
- El **free tier** de Gemini no alcanza para el extract del vault (varios chunks).

## Impacto (resuelto para el link-graph)

- **Antes:** el grafo del vault no tenía relaciones entre notas → `path`/`affected` inútiles.
- **Ahora:** con `graphify-obsidian` el link-graph funciona (852/852 edges `references`
  resueltos, 0 colgantes). El retrieval **semántico** sigue no disponible (extract parqueado),
  pero la Capa 2 **relacional** ya no depende de semántica.

## Detección

- (Histórico) `affected "<entidad>"` vacío pese a inbound links + `_origin` 100% `ast`.
- Hoy, si un backlink esperado sale vacío, sospechar primero del **caveat de query** (ver
  abajo) o de caché AST stale, **no** de un gap de captura.

## Mitigación / Resolución

- **RESUELTO — Vía A (fork `graphify-obsidian`):** resolver **vault-aware** en
  `graphify/extract.py` (índice stem + alias de frontmatter), gated por
  `GRAPHIFY_MD_VAULT_ROOT`. Rama `feat/obsidian-vault-wikilinks`, commit `9c393b7`, build
  aislado. Los `[[wikilinks]]` son edges `references`; el grafo relaciona por **links**, no
  por tags. Ver [[Economía de Tokens]].
- **Builder standalone — DESCARTADO (histórico).** El plan original de un builder propio que
  emitía `{nodes, edges}` y hacía `merge-graphs` quedó superado por el fork; no reimplementarlo.
- **Caveat de query de backlinks (verificado):** la consulta correcta es
  `graphify-obsidian affected "<nota>.md" --relation references` — con el sufijo `.md` **y** la
  relación explícita (`references` no está en las relaciones por defecto de `affected`).
  `affected "<nombre-pelado>"` (sin `.md`) resuelve al heading H1 → vacío. **NO** consultar por
  file-node id como workaround: da vacío (una nota vieja lo afirmaba; era incorrecto).
- Para el vault: operar con **índices curados** (`00-index.md` + tags) como capa primaria;
  `graphify-obsidian` para relaciones/lint. Semántica LLM sigue parqueada.
- Si algún día se necesita semántica: modelo **instruct** (no reasoning) y backend **pago**.

## Pitfall operacional: no inventar comandos ni borrar `graph.json`

Distinto de los gaps de extracción de arriba; es un error de **operación** que ya costó
un grafo (recurrente, bloqueante). Crítico para cualquier agente que corra Graphify —
incluida la fase de código.

- **Síntoma:** se recomienda/ejecuta un comando inexistente (p. ej. `update --mode deep`;
  `--mode deep` es de `extract`, NO de `update`) o un runbook hace `rm graph.json` → el
  grafo se pierde y hay que rebuildear.
- **Causa raíz:** doc del vault desactualizada + asumir flags de memoria en vez de verificar
  el CLI real.
- **Mitigación (regla dura):**
  1. **Verificar el CLI real ANTES de recomendar/ejecutar** (`--help` / repo), nunca de memoria.
  2. El `graph.json` vive en caché local fuera del vault y se regenera con
     `graphify-obsidian update`; nunca crear salidas `95-graphify/` en el vault.
  3. `update` = solo AST (gratis). La semántica (`extract`) queda parqueada (ver arriba).

## Evidencia

- Diagnóstico inicial: sesión 2026-07-03, repo local del fork de Graphify.
- Resolución 2026-07-04: fork vault-aware validado en el vault real (576 notas) — 852/852 edges
  `references` resueltos, 0 colgantes; backlinks de hubs OK (java-polycard-sdk 9,
  search-middleware 14, vpp-backend 9, vis-octopus-lib 7). Log:
  `journal/logs/2026-07-04-graphify-obsidian-wikilinks.md`.
- Pitfall operacional: feedbacks `2026-07-03-token-economy-*` (comando inventado + `rm graph.json`).

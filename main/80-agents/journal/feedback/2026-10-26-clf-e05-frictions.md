---
type: feedback
schema_version: 1
scope: session
created: "2026-10-26"
updated: "2026-10-26"
area: "[[Echo]]"
project: "[[Echo Futures — Optimización de Campañas]]"
entities:
  - "[[Echo Futures]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run: "[[80-agents/journal/agent-runs/2026-10-26-zcode-glm53-clf-e05-execution-certification]]"
session_goal: Mandato CLF-E05 (remediación source-driven + certificación de ejecución)
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - area/echo
---

# Session Feedback - 2026-10-26 - clf-e05 frictions

## Context

Mandato ONE-SHOT CLF-E05 sobre Hefesto vía MCP aranea-ssh + trabajo intensivo en vault.

## Friction 1 — subagente clf-flash sin cuota

El subagente `clf-flash` (tipo dedicado del workspace) falló al despachar con `exceed quota limit` (duración 5s, sin trabajo). Consecuencia: la FASE 3 se ejecutó inline. Sugerencia: si el tipo de agente misionero no tiene cuota garantizada, quitarlo del catálogo o documentar el fallback inline para no gastar un despacho por ciclo.

## Friction 2 — transporte SSH del MCP corrompe multilínea y redacta paths de alta entropía

`run-command` colapsa saltos de línea (heredocs y `python3 -c` multilínea mueren con SyntaxError) y el output redacta nombres de archivo/dir con alta entropía (`[REDACTED:entropy:N]`), incluyendo paths completos de resultados de `find`. Flujo seguro aprendido: escribir scripts en archivos locales → `sftp-upload` (SIEMPRE con profile explícito) → ejecutar por nombre → que el script imprima sólo resúmenes cortos; evitar heredocs inline y no confiar en paths crudos en la salida. Coste: 3 intentos perdidos antes de estabilizar el método.

## Friction 3 — sftp-upload sin profile escribe en otro host silenciosamente

`sftp-upload` sin el parámetro `profile` usó un default (`docker-echo-dev-operator`, root@192.168.31.75) en lugar de `hefesto`: el archivo "subido" no existía en Hefesto y el error de lectura (`No such file`) no delataba el destino equivocado. Sugerencia: exigir profile explícito o hacer fallar la llamada sin default implícito cuando hay más de un perfil operativo.

## Friction 4 — handoff K05 ausente

El mandato presupone `artifacts/clutifx-strategy-research/k05/CLF-K05-HANDOFF.json` producido por Daedalus; no existe en vault ni Hefesto. El ciclo fallback del mandato funcionó, pero medio ciclo de trabajo (FASE 4 y la semántica de E05-01) queda bloqueado por un artefacto que nadie produjo. Sugerencia: gate previo barato al inicio de mandatos dependientes de handoffs (verificar existencia antes de prometer fases).

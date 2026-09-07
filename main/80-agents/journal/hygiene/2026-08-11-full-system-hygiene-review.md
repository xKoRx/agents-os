---
type: scratch
schema_version: 1
scope: session
created: 2026-08-11
updated: 2026-08-11
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
  - "[[AGENTS OS - Fase 4]]"
related:
  - "[[agents-os]]"
  - "[[agent-constitution]]"
aliases: []
confidence: verified
source_session:
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/scratch
  - kind/hygiene-report
  - scope/session
---

# 2026-08-11 — Full-system hygiene review

> [!info]+ Hygiene review
> Auditoría base para [[AGENTS OS - Fase 4]]. Este reporte operacional queda fuera del retrieval normal de Graphify.

## Review Window

- **Mode:** explicit full-system audit.
- **Scope:** ideología, constitución, mapa, bootstrap, 28 skills core, 82 memorias públicas Markdown, Resource Wiki activa, schema/materializer, perfiles de agente, índices, logs, Doctor, Context Router y Graphify.
- **From:** 2026-08-11.
- **To:** 2026-08-11.
- **Next review after:** cuando una tarea P0/P1 de Fase 4 pase a WIP o tras un cambio de contrato/runtime; no por calendario vacío.

## Files Checked

- 62 Markdown bajo `80-agents/skills/**`, incluidos 28 entrypoints `SKILL.md` y sus contratos/referencias.
- 82 Markdown bajo `80-agents/memory/public/**`; después de la reparación no quedan archivos con extensión anómala en ese árbol.
- 3 Markdown bajo `80-agents/agents-os/**`.
- 17 pares/artefactos `00-index.md` y `log.md` bajo `30-resources/**`, incluidos 8 índices activos y el subdominio SDD.
- Cockpit [[AGENTS OS]], nueva [[AGENTS OS - Fase 4]], cuatro perfiles de superficie y dashboard `80-agents/crew/INDEX.md`.
- Outputs derivados `95-graphify/obsidian/graph.json` y `GRAPH_REPORT.md`.

## Fixes Applied

### Automatic

- Reindex Graphify ejecutado con gate previo `0/0`: `5267 nodes / 6355 edges`; corpus contaminante `trash=0 / archive=0 / json=0`; el clustering de comunidades es variable y no es gate.
- Password operativo de workers centralizado por instrucción posterior del owner en `80-agents/tools/echo-forge-worker-access/credentials.env`; el archivo plaintext está excluido de Graphify y su reemplazo/rotación queda P0 `#waiting` hasta autorización.

### Direct Edits With Logs

- Schema de `application` extendido con lifecycle transitorio `deprecating`, coherente con [[rio-materializer]] y [[rio-frontend]].
- Learning corrupto `hermes-dashboard-reverse-proxy-websocket-origin.md</path>` recuperado como `.md` canónico, migrado a schema v1 y con routing corregido a [[Aranea]].
- Links `file:///Users/...` y scratch client-owned removidos de memoria pública; repos externos quedaron expresados como `repo + path` y evidencia efímera como tal.
- Registro de dominios Resource Wiki actualizado; RIO Atlas recibió `log.md`; metadata, índices y bitácoras de applications, rio-atlas, methodologies y Aranea fueron reconciliados; lint registrado en dominios activos.
- Perfiles [[Codex]], [[Claude Code]] y [[Cursor]] dejaron de renderizar literales `specialty/status`.
- [[AGENTS OS - Fase 4]] materializada y compactada como backlog-only; cockpit padre actualizado con una sola tarea puente To Do.

## Findings

### Ideology And Authority

- **Sano:** bootstrap es la única máquina de startup; constitución, mapa y bootstrap coinciden. Presupuesto de contexto es sufficiency-first y los números son techos blandos. Markdown manda y Graphify es derivado. El registro superficie×modelo exige identidad exacta y no inferida.
- **Abierto P0:** [[token-economy-indexing-architecture]] conserva un waterfall “nunca saltar capas” y verbos tipados del body que contradicen Context Router y `graphify-contract` vigentes.
- **Abierto P1:** `agents-os-session-close` reimplementa partes de distillation y feedback; debe quedar como orquestador.
- **Abierto P1/P2:** índice de skills, política public-vs-internal y ejemplo de logging de entity-update presentan drift semántico menor frente al runtime actual.

### Metadata

- 13 de 28 skills y 76 de 82 memorias públicas siguen como legacy admitido por contrato; no son regresión, pero deben migrarse incrementalmente cuando se toquen.
- `operational-healthcheck-policy` tiene scope/tag incoherentes y estructura legacy; `agents-os-tagging-system` usa `Operational Procedure` en vez de la sección canónica.
- `agents-os-entity-update` (266 líneas) y `agents-os-hygiene-review` (251 líneas) superan el smell-test de compacción; no existe hard cap.

### Missing Logs

- Resuelto: RIO Atlas ya posee `log.md`; applications y methodologies registran las ingestas del 2026-08-11 y el backfill de Data Mesh.
- Contrato a aclarar: `backup-dr/00-index.md` comparte el log raíz de Aranea como subíndice, pero Doctor y Resource Wiki no expresan esa excepción de forma idéntica.

### Duplicates Or Stale Memory

- `design-frozen-pattern-for-homelab-refactor` mezcla learning, policy y runbook.
- `source-order-count-zero` conserva investigación obsoleta y bugs adicionales dentro del mismo known error.
- `memory-tool-format-drift-recovery` es procedural pero declara `load_policy: never`; debe reclasificarse.
- `agents-os-session-close` duplica procedimientos ya gobernados por skills especializadas.

### Broken Links And Portability

- Resuelto: el learning con filename `*.md</path>` ahora es recuperable por herramientas Markdown.
- Resuelto: no quedan locators `file:///` vivos en memoria pública salvo menciones normativas que prohíben ese formato.
- El índice raíz de Aranea sigue demasiado grande y mezcla catálogo con handover, decisiones, métricas y quick commands; requiere jerarquización, no un recorte automático.

### Alias Issues

- Alias `dashboard ws origin` debe resolver tras el reindex final; la corrupción del filename era la causa del miss.
- No se detectaron copias client-owned de skills core bajo `.agents/`, `.claude/`, `.cursor/` o `.gemini/`.

## Graphify

- **Status:** current; el reindex incorporó Fase 4 y el learning recuperado.
- **Action:** completada; gate global `0/0`, Doctor `0/0/0`, Context Router `14/14` con 0 misses y precision proxy 100%.
- **Validation queries:** alias `dashboard ws origin` resolvió exactamente 1 nodo; `explain "AGENTS OS - Fase 4"` resolvió el proyecto y sus relaciones; corpus excluido `trash=0 / archive=0 / json=0`.

## Proposals Rejected Or Deferred

- No se creó historial ficticio de `agent_run`; el primer run por superficie requiere evidencia real.
- No se migraron masivamente 76 memorias ni 13 skills legacy; se conserva migración-on-touch.
- No se compactó automáticamente Aranea ni los known errors complejos; separar autoridad e historia requiere juicio y queda en backlog.
- No se añadió un hard cap de tokens o líneas; la economía sigue sufficiency-first con smell-tests.

## Open Tasks

- Backlog canónico completo en [[AGENTS OS - Fase 4]]: 3 P0, 10 P1 y 6 P2, todas To Do y ninguna WIP/Review.
- Prioridad humana diferida: autorizar revisión de historial/rotación cuando corresponda; mientras tanto, los agentes usan `echo-forge-worker` y la tarea puente permanece To Do.

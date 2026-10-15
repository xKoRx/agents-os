---
type: feedback
schema_version: 1
scope: session
created: 2026-10-15
updated: 2026-10-15
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[Echo Futures]]"
related:
  - "[[TRADESGERARD-PERFORMANCE-MEMORY]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run: "80-agents/journal/agent-runs/2026-10-15-zcode-glm-5.3-flash-tradesgerard-perf-memory.md"
session_goal: "One-shot: iteración rápida del backtester TradesGerard (≥5× corto), separación de responsabilidades, equivalencia O11"
source_session: "GLM local one-shot 2026-10-15 (superficie ZCode, modelo GLM-5.3-Flash)"
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/agents-os
  - agent/system1
---

# Session Feedback - 2026-10-15 - echo futures perf memory

## Context

- Agent surface: [[ZCode]]
- Agent model: GLM-5.3-Flash (solicitado; servido según el harness)
- Agent run: [[2026-10-15-zcode-glm-5.3-flash-tradesgerard-perf-memory]]
- Session goal: rendimiento/memoria del backtester con equivalencia O11 (≥5×, clon JSON fuera, TZ cache, dataset in-memory)
- Main entity: [[Echo Futures]]
- Skills used: agents-os-bootstrap, agents-os-session-close, agents-os-agent-run-register
- Retrieval mode: Graphify no requerido; lectura directa de CONTROL/RESULTADO + código en el SHA sellado
- Artifacts changed: rama `glm/tradesgerard-perf-memory-20261015` @ `67e7ecf7` (xKoRx/echo, push verificado), [[TRADESGERARD-PERFORMANCE-MEMORY]], CONTROL (delta), artefactos en `/srv/echo-work/runs/perf-memory-20261015/`

## Lecciones técnicas probadas (problema/causa/corrección/prevención)

- **Problema 1 — Atribución incorrecta de lecturas:** el `rchar` alto del ciclo anterior se atribuyó a reconstrucción H1 sin evidencia suficiente. Causa: el churn real era serialización JSON de lecturas de contexto (`LiveScope.serve` materializaba ~320 KB de JSON + sha256 por evaluación) y re-parseos de strings en kernels, no I/O de disco. Corrección: pprof + contadores distinguieron bytes físicos (2 opens, 181k parses una vez) de trabajo lógico (92M consultas TZ servidas de caché). Prevención: exigir atribución por perfil de CPU/asignaciones antes de culpar I/O; los contadores `EVIDENCE` del CLI quedan como práctica.
- **Problema 2 — Serialización usada como copia:** `OwnerState.clone` (provider) y los sets dedup de Operation pagaban JSON round-trip / clonado total de mapas por Apply (53 % de todas las asignaciones del proceso). Corrección: clon tipado con oráculo JSON byte-idéntico y journal de undo para los sets compartidos (rollback byte-exacto probado). Prevención: la copia transaccional es un contrato semántico, no una implementación: elegir representación por costo medido y probarla contra el oráculo.
- **Problema 3 — Cálculos dentro de Strategy:** el módulo re-parseaba 60+ strings a `big.Rat` y reconstruía calendarios por barra; el JSON del estado del módulo viajaba por cada evaluación. Corrección: memo de decode por OwnerState (bytes comparados por evaluación) + espejos tipados con superficie de error exacta. Prevención: el estado persistido (JSON) es frontera de checkpoint, no el formato de trabajo del hot path.
- **Problema 4 — Falta de receta de lote reutilizable:** cada campaña re-escaneaba y re-copiaba el corpus (2 opens + 181k parses POR campaña). Corrección: `PreparedSource` sellada una vez por lote + cursores aislados; evidencia `source_file_opens=2` para 8 campañas completas. Prevención: la preparación inmutable es propiedad del lote, no de la campaña; exponer contadores de I/O física como evidencia estándar.

## Scores

- Startup clarity: 4
- Retrieval usefulness: 4
- Skill fit: 4
- Template fit: 4
- Closeout friction: 4
- Overall confidence: 5

## What Complicated The Session Most

- Observation: el mandato vive repartido entre CONTROL (283 líneas de historia densa), RESULTADO y el workspace externo; las rutas de artefactos sellados requieren cruzar dos árboles (`/srv/echo-work/runs/O11` + workspace de operabilidad) y el CSV de la matriz.
- Why it was hard: cada recibo sellado vive en un directorio distinto por attempt; la resolución del oráculo necesitó el CSV `o11-matrix-40-final.csv` como registro canónico.
- Proposed improvement: que el informe de matriz incluya un índice machine-readable config→out_dir (el CSV ya lo es; enlazarlo explícitamente desde CONTROL como autoridad de resolución).

## Most Useful Part Of Sistema 1

- What helped: CONTROL como fuente de identidad exacta (commit/binario/recibos) y la convención de recibos con digests por campaña — hicieron posible un comparador de equivalencia fuerte en minutos.
- Why it helped: identidad sellada + digests de eventos permitieron probar equivalencia byte-a-nivel-línea salvo identidad de build.
- Keep/change: mantener; añadir el puntero al CSV-canónico en el encabezado de CONTROL.

## Least Useful Or Noisy Part

- What did not help: historia cronológica mezclada con estado vigente en el mismo CONTROL (varias secciones «estado vigente» sucesivas).
- Why it was weak/noisy: fuerza leer 200+ líneas para encontrar el estado real.
- Proposed cleanup: mover cronología a secciones de historia al final (el vault ya lo intenta; seguirlo estrictamente).

## Missing Support

- Problem not solved by Sistema 1: nada bloqueante; la skill de bootstrap no está registrada en el catálogo de ZCode (se leyó por ruta directa).
- How Sistema 1 could help next time: publicar `agents-os-bootstrap` como skill invocable del cliente evita el fallback manual.
- Suggested artifact type: n/a.

## Retrieval Feedback

- Useful query or source: lectura directa de `TRADESGERARD-CONTROL.md` + `TRADESGERARD-OPERABILITY-RESULTADO.md`.
- Missing context: mapa config→directorio de resultados sellados (resuelto vía CSV).
- Duplicate/noisy result: n/a.
- Better future query: «matrix CSV como índice de oráculos de campaña».

## Skill Feedback

- Skill that worked well: agents-os-session-close (delta classifier claro para cierre autorizado por mandato).
- Skill that was confusing: n/a.
- Trigger/routing gap: bootstrap no registrada como skill de cliente.
- Suggested contract change: n/a.

## Template Feedback

- Template used: session-feedback + agent-run.
- Field that helped: contexto/lecciones con problema-causa-corrección-prevención.
- Field that felt redundant: varias secciones de puntuación para un cierre técnico.
- Missing field: n/a.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna al iniciar? sí (nota global always-load)
- ¿Qué valor operativo aportó? reglas de reintentos/identidad y fallar-cerrado aplicables a la verificación de recibos.
- ¿Dejaste algún mensaje para el próximo agente? continuidad del proyecto actualizada por delta en memoria interna del harness (archivo de proyecto) + informe vault.
- Utilidad del espacio privado (1-5): 4.

## Pain Pattern Candidate

- Is this likely to repeat? no
- Suggested severity: low
- Candidate owner: proyecto Echo Futures (resuelto en código)
- Promote to L3 memory? defer (las lecciones técnicas quedaron en este feedback y en el informe; son específicas del proyecto)

## One Next Improvement

- Índice machine-readable config→out_dir como autoridad de resolución de oráculos de campaña, enlazado desde CONTROL.

---
type: session
schema_version: 1
scope: session
created: "2026-08-15"
updated: "2026-08-15"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[Symphony]]"
entities:
  - "[[Symphony]]"
  - "[[stager-app]]"
related:
  - "[[2026-08-15-1055-echo-forge-mmlots-rollout-raw]]"
  - "[[stager-state-0600-runtime-kor]]"
  - "[[sqx-custom-analysis-loads-snippets-jar]]"
aliases: []
confidence: high
source_session: 7bfc3412-5936-4c7c-85b8-8dd1cf059569
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

# 2026-08-15-1055-echo-forge-mmlots-rollout-summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Validar overnight el fix `mmLots`, publicar `0.2.44` + `example_flow_8`, y cerrar si no reaparecen los fallos conversados.

## Contexto cargado

- [[Echo Forge]], [[sqx-custom-analysis-loads-snippets-jar]], skills deployer/SSH/troubleshooting/session-close.

## Trabajo realizado

- `example_flow_7`: 8/8 `.mq5` con `mmLots=0.1`; cero con `=0`. Export usó path `.sqx`.
- Stager `writeAtomic` 0644 desplegado; post-`0.2.44` state 644 y runtime `active` en Linux; Windows `CURRENT=0.2.44`.
- Serie de producto de vuelta a `0.2.x` (`0.2.43` overnight, `0.2.44` esta mañana).
- `example_flow_8` despachado: builder OK, OverviewExporter en curso.

## Artifacts creados o modificados

- `stager/internal/activation/store.go` (0644) + test; binario one-shot en flota Linux.
- Symphony release `0.2.44` + wave `example_flow_8`.
- [[stager-state-0600-runtime-kor]]

## Memoria propuesta o creada

- Known error de state `0600` vs runtime `kor`.

## Decisiones

- Los HTM ausentes de `example_flow_7` no reabren `mmLots=0`: el backtest falló por `tester.ini` path en Windows.

## Pendiente

- Owner acepta la tarea puente en [[Echo Forge]].
- Residual: `mt5_backtest_artifact` / `tester.ini` path (fuera de este hotfix).
- `example_flow_8` sigue corriendo; HTM de esta wave no se esperó.

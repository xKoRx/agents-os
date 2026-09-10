---
type: agent_memory
scope: project
project: "[[Echo Forge]]"
created: 2026-07-31
updated: 2026-09-09
memory_state: archived
entities:
  - "[[Echo Forge]]"
  - "[[Symphony]]"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/memory
  - kind/continuity
  - project/echo-forge
  - gap/ef-g28
---

# Continuidad — EF-G28 hotfix trade list exporter

## Hecho

Hotfix de reflexión SQX Build 142 desplegado. Smoke Zeus OK:
`trades=107`, `_SUCCESS`, `export_run status=complete` sobre
`NDX_L_H1_example_flow_57_v1_Strategy_4.1.19.h0`.

## Runtime real

SQX Custom Analysis ejecuta fuentes en
`/home/kor/sqx/user/extend/Snippets/SQ/CustomAnalysis/**`.
`user/libs/EchoForgeAutomator.jar` solo no basta.

## Código (repo symphony, sin commit)

- `sqx/exporter-plugin/src/SQ/CustomAnalysis/trades/TradeExtractionService.java`
- `sqx/exporter-plugin/src/SQ/CustomAnalysis/trades/ProductionSQXTradeSource.java`
- `sqx/exporter-plugin/src/SQ/CustomAnalysis/EchoForgeTradeListExporter.java`
- stubs `SampleTypes` + `StubSQXTradeSource`
- nota en `specs/FEAT-SQX-STRATEGY-EVALUATION/G6_HANDOFF.md` §10 / §10.4.0

## Próximo para otra IA

1. Correr flow E2E completo (`generic_workflow` + `trade_list_exporter`) y falsar `_SUCCESS` en MinIO/Mongo.
2. Completar EF-G28 A3: `SQXCapabilities` fail-closed + `javap -constants` versionado + test CI.
3. EF-G31: pipeline release debe sync **Snippets + JAR** y registrar hash en `deploy/manifest.json`.
4. EF-G29/G30: deferidos (owner controla instrumento/config).
5. Commit de los cambios del plugin (aún uncommitted).

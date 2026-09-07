---
type: storage
schema_version: 1
status: active
slug: fuentes
aliases:
  - fuentes
  - sources workspace
  - workspace de repositorios
tags:
  - kind/storage
  - storage/fuentes
created: 2026-08-10
updated: 2026-09-01
---

# Fuentes — Workspace de repositorios

## Propósito

- Workspace externo para checkouts completos de repositorios y grafos de código derivados de Graphify.
- **Alcance:** repositorios de Meli/RIO y herramientas internas relacionadas. Los repos del ecosistema Echo Forge viven en [[Echo — Workspace Go de repositorios]] (`~/go/src/github.com/xKoRx`).

## Ubicación y contrato

- **Path:** `~/fuentes`
- **Qué contiene:** repositorios completos, sus grafos individuales bajo `graphify-out/` y grafos mergeados como `graphify-signals.json`.
- **Índice operativo para agentes:** `~/fuentes/AGENTS.md` (listado de apps + grafos + comandos). Plataforma paraguas: [[RIO]]. Metodología base: [[data-mesh]].
- **Qué no contiene:** notas del vault, memoria de agentes ni repositorios completos bajo `VAULT_ROOT`.
- **Reglas de uso:** los checkouts locales usan nombres canónicos `rio-*`; el remote GitHub se conserva solo como procedencia. Antes de clonar o generar un grafo, resolver esta nota por su título canónico.

## Operación

- **Comandos seguros:** ejecutar Graphify desde `~/fuentes/<repo>`; usar `graphify update .` para un repo y `graphify merge-graphs ... --out ~/fuentes/graphify-signals.json` para el merge.
- **Backups / recuperación:** los repos son Git; no borrar worktrees ni grafos sin confirmar el destino y la recuperación.
- **Fuentes relacionadas:** [[rio-playmaker]], [[rio-controlplane-clickhouse]], [[rio-controlplane-fury]], [[rio-controlplane-flink]], [[rio-controlplane-kafka]], [[rio-controlplane-signals]], [[rio-controlplane-kms]], [[rio-controlplane-observability]], [[rio-sdk-events]], [[rio-materializer]], [[local-agents-pipeline-cli]], [[ads-signals-skills-marketplace]].

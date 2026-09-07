---
type: index
schema_version: 1
status: active
icon: 🔧
slug: tools-index
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: 2026-07-04
updated: 2026-09-01
reviewed: 2026-08-11
aliases:
  - tools index
  - índice de tools
  - catálogo de herramientas
cssclasses:
  - wide
tags:
  - kind/index
---

# 🔧 Tools — Índice

> [!info] Wiki compilada de recursos
> Catálogo curado del dominio `tools/` (software de terceros que uso, no desarrollo).
> El agente lo actualiza en cada *ingest*. Reglas:
> [[30-resources/00-RESOURCE-WIKI|Resource Wiki]] · Bitácora: `log.md` · Convenciones de
> páginas de tool: [[30-resources/tools/README|tools/README]].

## 📊 De un vistazo

- **Páginas:** 4 tools
- **Última ingesta:** 2026-09-01 (`ads-signals-skills-marketplace` — catálogo portable de skills para Claude y Codex)
- **Estado:** active

## 📂 Catálogo

| Tool | Una línea | Área | Vendor |
|---|---|---|---|
| [[graphify]] | Índice derivado sobre vault/código; el fork `graphify-obsidian` resuelve wikilinks y preserva lossless las relaciones semánticas que comparten source-target mediante `relation` + `relations`. | [[Personal]] | [safishamsi/graphify](https://github.com/safishamsi/graphify) |
| [[strategyquant-x]] | Tool comercial de generación/optimización de estrategias de trading (C# core + Java plugin + CLI); corre en VMs `sqx-ulab-*` de Aranea, orquestada por [[echo-forge]]. | [[Echo]] | [strategyquant.com](https://strategyquant.com) |
| [[local-agents-pipeline-cli]] | CLI `zord` que ejecuta Zords configurables en paralelo sobre diffs/PRs, sintetiza findings y permite fixes selectivos con varios providers de agentes. | [[Personal]] | [melisource/fury_local-agents-pipeline-cli](https://github.com/melisource/fury_local-agents-pipeline-cli) |
| [[ads-signals-skills-marketplace]] | Repositorio y catálogo versionado de skills portables para Claude y Codex, con contrato explícito de metadata, permisos, runtime y validación local. | [[Meli]] | [melisource/fury_ads-signals-skills-marketplace](https://github.com/melisource/fury_ads-signals-skills-marketplace) |

## 🚨 Salud (del último lint)

- **Huérfanos:** pendiente — correr `resource-wiki-lint-reindex` tras el próximo reindex.
- **Contradicciones:** ninguna detectada.
- **Conceptos sin página:** ninguno pendiente.

## 🔗 Links

- [[30-resources/00-RESOURCE-WIKI|Reglas de la Resource Wiki]]
- `log.md` — bitácora cronológica de este dominio
- [[30-resources/tools/README|tools/README]] — convención de páginas de tool (cómo agregar una tool)
- [[graphify]] — índice derivado sobre estas páginas

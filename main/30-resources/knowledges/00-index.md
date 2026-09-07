---
type: index
schema_version: 1
status: active
icon: 📚
slug: "knowledges-index"
area: "[[Meli]]"
project: "[[AGENTS OS]]"
created: "2026-08-18"
updated: "2026-09-01"
reviewed: "2026-09-01"
aliases:
  - knowledges index
  - índice de knowledges
  - external-resources index
  - knowledge bundles
cssclasses:
  - wide
tags:
  - kind/index
  - area/meli
---

# 📚 Knowledges — Índice

> [!info] Wiki compilada de recursos
> Catálogo curado del dominio `knowledges/`: **external-resources** de tipo *knowledge bundle* — repos externos de conocimiento curado que extienden esta Resource Wiki. Cada página es el **puntero canónico** al repo (no una copia). El agente lo actualiza en cada *ingest*. Reglas: [[30-resources/00-RESOURCE-WIKI|Resource Wiki]] · Bitácora: `log.md`.

## 📊 De un vistazo

- **Páginas:** 2 registros · 1 knowledge bundle activo
- **Última ingesta:** 2026-09-01 (reemplazo por [[ads-signals-knowledge-library]] — knowledge vigente de RIO)
- **Estado:** active

## 📂 Catálogo

| Página | Una línea | Meta |
|---|---|---|
| [[ads-signals-knowledge-library]] | Knowledge library vigente de RIO: arquitectura, flujos, servicios, operación, contratos, catálogo y evaluaciones; usar código actual para decisiones sensibles. | `~/fuentes/ads-signals-knowledge-library` · `confidence: medium` · `last_verified: 2026-09-01` |
| [[signals-knowledge]] | Bundle OKF anterior; conservado sólo como registro histórico. | `deprecated` · superseded by [[ads-signals-knowledge-library]] |

## 🚨 Salud (del último lint)

- **Integridad del repo activo:** `validate_library.rb` falla con 17 errores: 15 de freezes inválidos y 2 links locales rotos.
- **Frescura:** drift material contra `origin/master` en Signals, Fury, Observability y Playmaker; ver [[Revisión de ads-signals-knowledge-library]].
- **Regla de uso:** la knowledge guía retrieval; el código del servicio dueño define comportamiento vigente.

## 🔗 Links

- [[30-resources/00-RESOURCE-WIKI|Reglas de la Resource Wiki]]
- [[Onboarding Signals]] — proyecto de comprensión al que se asocia este dominio.
- [[Signals Knowledge Harness]] — proyecto que propone la harness de contribución de agentes.
- [[RIO]] · [[applications/00-index|Índice de applications]] — dominio espejo a contrastar.
- `log.md` — bitácora cronológica de este dominio.

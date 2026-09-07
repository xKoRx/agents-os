---
type: application
status: active
area: "[[Meli]]"
lang: Go
github: https://github.com/melisource/fury_vis-motors-mcp
path: ~/fuentes/vis-motors-mcp
aliases:
  - vis-motors-mcp
  - fury_vis-motors-mcp
tags:
  - area/meli
  - kind/application
created: 2026-06-24
updated: 2026-06-27
---

# vis-motors-mcp

> [!info]+ vis-motors-mcp
> **Lenguaje:** Go 1.26.4 · **Área:** [[Meli]]
> **GitHub:** [melisource/fury_vis-motors-mcp](https://github.com/melisource/fury_vis-motors-mcp) · **Path local:** `~/fuentes/vis-motors-mcp`

## 📝 Descripción

- Servidor **MCP** que da a agentes de IA (Maxwell, en la VPP) búsqueda semántica sobre specs de vehículos y pricing de trade-in, vía un pipeline **RAG sobre Fury VectorDB**.
- No es web app: su superficie MCP es **read-only** (search specs, listar modelos, trade-in, dealers). Las mutaciones (ingest/replace/delete) van por endpoints HTTP `/vehicles`, no por MCP.

## 🔧 Datos útiles

- **Repo:** `melisource/fury_vis-motors-mcp`
- **Path local:** `~/fuentes/vis-motors-mcp`
- **Stack / notas:** Go 1.26.4 · SDK MCP: `github.com/modelcontextprotocol/go-sdk` (actual **v1.4.1**) · OpenTelemetry · tools MCP: `search_vehicle_specs(_batch)`, `get_current_vehicle`, `list_vehicle_models`, `list_item_dealers`, `contact_dealer`, `estimate_trade_in_offers`, `show_contact_cta` · consumido por Maxwell (agente conversacional MELI) en la Vehicle Product Page.

## ✅ Tareas relacionadas

```tasks
sort by priority
not done
description includes vis-motors-mcp
short mode
hide task count
```

## 🔗 Links

- [Repo GitHub](https://github.com/melisource/fury_vis-motors-mcp)

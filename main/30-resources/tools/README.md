---
title: "Tools — convenciones de páginas (vendor / third-party)"
type: doc
status: active
icon: 🔧
slug: tools-conventions
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: 2026-07-01
updated: 2026-07-04
aliases:
  - Tools convenciones
  - convención de tools
  - third-party tools conventions
tags:
  - tools
  - third-party
  - vendor
  - kind/doc
  - area/personal
  - project/agents-os
cssclasses:
  - wide
---

# 🔧 Tools — convenciones de páginas (vendor / third-party)

> [!info] El catálogo vive en `00-index.md`
> Este doc guarda la **convención** de cómo se documenta una tool. El **catálogo curado**
> (capa 1 de retrieval) es [[30-resources/tools/00-index|tools/00-index]] — actualizarlo ahí en cada ingest,
> no acá. Reglas del dominio: [[30-resources/00-RESOURCE-WIKI|Resource Wiki]].

> **Tools = software de terceros** que uso en el homelab, proyectos Echo, AGENTS OS, etc.
>
> **Convención**: `type: tool`, `scope: tool`. Se diferencia de `applications/` (software propio desarrollado por mí).
>
> **Cuándo agregar una tool acá**: cada vez que uso un software de terceros en un workflow serio y necesito documentarlo (config, comandos, troubleshooting, versionado).

---

## 📂 Por área

### [[Personal]] (homelab, AGENTS OS)

- **[[graphify]]** — visualizador de grafos para Obsidian (HTML estático + JSON data). Genera `obsidian/graph.html` y `obsidian/graph.json` desde el vault. Usado en AGENTS OS para QA estructural del Second Brain.

### [[Echo]] (programas Echo, SQX, MT5, etc.)

- **[[strategyquant-x]]** — tool comercial de generación y optimización algorítmica de estrategias de trading. C# core + Java plugin + CLI invocable. Corre dentro de las VMs `sqx-ulab-*` en Aranea, orquestado por [[echo-forge]].

---

## 📝 Convención de archivos en `tools/`

Cada tool tiene un archivo `.md` con este frontmatter mínimo:

```yaml
---
type: tool              # fijo: tool (NO application)
status: active|legacy   # estado actual
scope: tool             # fijo: tool
area: "[[AreaName]]"    # área a la que pertenece
source_url: <url>       # vendor upstream
command:                # comandos CLI principales (lista)
  - cmd1
  - cmd2
entities:               # entidades Obsidian relacionadas
  - "[[Entity1]]"
load_policy: when_tool_loaded  # política de carga
indexable: true
index_priority: high|medium|low
aliases:                # nombres alternativos
  - Alias1
tags:
  - kind/tool           # fijo: kind/tool
  - third-party         # vendor / no propio
  - <tag-adicional>
---
```

**Diferencia con `applications/`**:

- **Tool** (esta carpeta): software de terceros. Tú lo **usas**, no lo **desarrollas**. Vendor mantiene el código.
- **Application** (`applications/`): software **propio**. Tú lo **desarrollas** y mantienes (ej: [[echo-forge]] en `xKoRx/symphony`).

Si una tool crece y se vuelve pieza central de un workflow documentado acá, sigue siendo tool — el crecimiento no la convierte en aplicación tuya.

---

## ➕ Cómo agregar una nueva tool

1. Crear `30-resources/tools/<nombre-kebab>.md` con el frontmatter de arriba.
2. Documentar: propósito, vendor, comandos clave, dónde corre (Aranea / cloud / local), entidades relacionadas, troubleshooting conocido, links a spec/vendor.
3. Agregar fila en el catálogo [[30-resources/tools/00-index|tools/00-index]] + entrada en `log.md` (ingest).
4. Si aplica, agregar entrada en el `00-index.md` general de `30-resources`.
5. Si la tool corre en Aranea, agregar nota en `02-servicios/` (servicios) o en el doc del nodo correspondiente.

---

## 🔗 Links

- **[[30-resources/00-RESOURCE-WIKI|Resource Wiki]]** — home/reglas del dominio de recursos.
- **[[30-resources/applications/00-index|applications/00-index]]** — catálogo de aplicaciones propias (convención análoga a la de tools).
- **[[AGENTS OS]]** — proyecto marco (este vault está bajo AGENTS OS).

---

## Source files

- `30-resources/tools/graphify.md` (existente desde antes)
- `30-resources/tools/strategyquant-x.md` (creado 2026-07-01, ticket 013)

## Captured

2026-07-01 — Creado este README con 2 tools (graphify, strategyquant-x). Inicia catálogo.
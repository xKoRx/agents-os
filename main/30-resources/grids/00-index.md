---
type: index
schema_version: 1
status: active
area: "[[Meli]]"
aliases:
  - grids
  - grids locales
tags:
  - kind/index
created: 2026-08-12
updated: 2026-09-08
---

# 📊 Grids locales

Carpeta para grids/tableros HTML autocontenidos que se ven de un vistazo y se comparten con equipos. Se abren en el navegador y no dependen de plugins de Obsidian. Cada grid debe documentar su fuente, estado de reproducibilidad y limitaciones.

## 📊 De un vistazo

- **Grids activos:** 2.
- **Fuentes de verdad:** `~/fuentes/rio-inspector/rio-scopes.json` para el estado Fury y [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599) para el contrato funcional; la nota y el HTML son vistas derivadas.
- **Reproducibilidad actual:** activa mediante `~/fuentes/rio-inspector/scope_inventory.py`; la vista narrativa sale directamente del generador.

## 📂 Catálogo

| Grid | Tema | Estado |
|---|---|---|
| `rio-scope-inventory.html` | Inventario Fury actualizado por aplicación y contrato funcional de SIG-599: catálogo acotado, adopción según necesidad, scopes frontend/backend y continuidad del ambiente. No propone topología física ni migración. | generado · schema v4 · corte Fury 2026-09-03 · publicado en Grid |
| `rio-deployments-critical-flow.html` | Presentación corta del flujo de deployments en RIO, tecnologías, ventanas de pérdida, muerte súbita de un CP y deuda técnica priorizada. | manual · schema v1 · verificado contra refs locales 2026-09-07 · sólo local |

## Convención

- Un archivo `.html` por grid, autocontenido (CSS/JS embebido), sin dependencias externas.
- Tono profesional y ligero: pensado para compartir con el equipo.
- La fuente factual vive en `rio-scopes.json` y el contrato funcional en SIG-599; el grid es la vista, no la fuente de verdad.
- Todo conteo del grid debe derivarse de la misma fuente normalizada y conservar provenance/timestamp.
- Datos y presentación son capas separadas: los datos viajan embebidos como `<script type="application/json" id="data">` y el layout se renderiza desde ahí. Reordenar un grid nunca debe tocar un número.

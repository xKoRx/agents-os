---
type: doc
status: draft
tags:
  - kind/doc
  - kind/system
  - tech/agents-os
created: 2026-06-27
updated: 2026-06-27
---

# 05 — Preguntas abiertas

[[agents-os|← Volver al índice]]

Estado de cada punto: **decidido** o **pendiente**. No inventar resoluciones donde dice pendiente.

## Decidido

- **Captura de raw**: el agente crea el placeholder L0; el usuario pega la sesión completa; el agente genera el resto. ✔
- **Graphify uniforme + doc base** entre agentes. ✔
- **Reindex manual para beta** con `graphify-obsidian update`; watcher queda post-beta. ✔
- **Higienización manual al cierre del día**, proceso aparte. ✔
- **Conflicto → resolver y registrar**; premisa de contexto enriquecido. ✔
- **Base del sistema = skills + reglas** (no MCP/servicio en MVP). ✔
- **Frontera Capa 1 / Capa 2** definida (qué es vs cómo se trabajó). ✔
- **Retrofit** desde raw para conocimiento futuro. ✔
- **Memoria pública/interna centralizada** en `80-agents/memory/public/` y `80-agents/memory/internal/`. ✔
- **Journal separado** en `80-agents/journal/` para sesiones y logs. ✔
- **Modelo sin `status` para memorias**: si ya no sirve, se elimina o reemplaza y se registra el cambio. ✔
- **Proyectos beta**: [[java-polycard-sdk]], [[search-middleware]], [[vis-octopus-lib]], [[vpp-backend]]. ✔
- **Superficies beta**: Codex, Claude, Cursor y Antigravity. ✔
- **Presupuesto orientativo inicial**: 3.000 tokens. ✔
- **Graphify del vault**: `graphify-obsidian`. ✔
- **Metadata beta**: definida en `80-agents/skills/_shared/metadata-schema.md`; modelo sin `status` ni `draft`, con `indexable`, `index_priority`, `load_policy`, `confidence`, routing links y defaults por tipo. ✔
- **Session summaries en beta**: quedan fuera del corpus normal de Graphify; si se incluyen más adelante deben pasar a `indexable: true` + `index_priority: low` con decisión explícita. ✔
- **IDs semánticos**: el ID beta es el path bajo `80-agents/memory/` sin `.md`; no se agrega propiedad `id`. Se usan rutas kebab-case, `aliases` para variantes y tags normalizados. ✔
- **Graphify agnóstico**: contrato común `update`, `query`, `explain`, `path`; si no hay shell, el agente usa un bridge/tool de la superficie que respete el mismo input/output. ✔
- **Validación real de `.graphifyignore`**: la exclusión por ruta de `80-agents/journal/`, raw sessions y logs quedó validada con placeholders L0/L1; además se registró el known error del patrón amplio `**/*raw-session*.md`. ✔
- **Reglas, cadencia y formato de higienización**: definidos en `agents-os-hygiene-review`, con reportes en `80-agents/journal/hygiene/`. ✔
- **Política de recorte de contexto**: definida en `agents-os-context-retrieval`; prioridad always-load, entidad, memorias criticas/altas y runbooks solo cuando aplican. ✔
- **Detección operativa de contradicción**: definida en `agents-os-conflict-resolution` con clasificación, edición directa cuando hay evidencia y log auditable. ✔

## Pendiente de definir

1. **Forward-test de adaptadores por superficie**: los adaptadores iniciales existen en `80-agents/adapters/`, pero falta probar el contrato Graphify en Claude, Cursor y Antigravity, especialmente cuando no haya shell directo.
2. **Forward-test de cierre con transcript real**: validar `agents-os-session-close` con una sesión completa provista por el usuario.
3. **Beta end-to-end en proyecto real**: ejecutar sesión 1, cierre, reindex, sesión 2 y reporte de métricas.

## Riesgos a vigilar (de la revisión de diseño)

- Dependencia fuerte de Graphify: ejecución agnóstica + reindex confiable.
- Calidad de la destilación en el cierre de sesión (lo que hace o quiebra el valor).
- Drift de entidades canónicas → la higienización debe atacarlo.
- Consistencia de nombres entre entidades y repos reales (usar alias para variantes).
- Resolución autónoma de conflictos exige logs buenos; si el agente resuelve mal, debe poder auditarse y revertirse.

---
type: doc
schema_version: 1
status: active
icon: 🧭
slug: context-router
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: 2026-07-03
updated: 2026-08-06
entities:
  - "[[AGENTS OS]]"
  - "[[agents-os]]"
  - "[[context-router]]"
related:
  - "[[token-economy-indexing-architecture]]"
  - "[[graphify]]"
aliases:
  - Context Router
  - contexto router
  - router de contexto
  - enrutador de contexto
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/doc
  - kind/concept
  - kind/system
  - area/personal
  - project/agents-os
---

# 🧭 Context Router

> [!info] Doc conceptual — no es la autoridad ejecutable
> Este documento explica **qué** es el Context Router y **por qué** importa. El
> **algoritmo ejecutable** (rutas por intención, capas, presupuestos, fallback y
> context pack) vive en la skill `agents-os-context-retrieval`, que **implementa**
> este router. Para ejecutar, sigue la skill; no dupliques su procedimiento aquí.

## Propósito

El **Context Router** es la capa de decisión que, ante una tarea, decide qué contexto cargar, desde qué capa, en qué orden y hasta qué punto. Es el query planner de [[Economía de Tokens]] y entrega el paquete mínimo suficiente.

La analogía: si las cuatro capas de indexación de [[token-economy-indexing-architecture]] son las herramientas, el Context Router es el conductor que decide cuál usar y hasta dónde. Sin él, el agente carga de más o de menos.

## Contenido

## Por qué importa (valor para el equipo)

- **Ahorro de tokens a escala:** un equipo de agentes cargando solo lo mínimo = costo
  real mucho menor por tarea.
- **Consistencia:** todos los agentes cargan contexto con la misma disciplina, auditable.
- **Mejor foco:** menos ruido en el contexto = mejores respuestas del modelo.
- **Medible:** cada carga declara qué trajo y por qué → base para benchmark y feedback.

## Idea central

Enruta **de barato a caro** según la intención (hecho · relación · síntesis · código · procedimiento) y se detiene cuando el contexto alcanza. El pipeline local objetivo es metadata/facets exactos → índice curado cuando aporte dominio → edges tipados o `references` → cuerpo Markdown seleccionado. El presupuesto es un techo blando por tier, nunca una guillotina; la skill `agents-os-context-retrieval` contiene el algoritmo ejecutable y este documento no lo duplica. La selección de **dominio** (Meli, Aranea/Echo, ninguno) ocurre antes, en el startup: es el domain gate de `agents-os-bootstrap` a partir del `area` de la entidad activa; este router decide la profundidad dentro de ese dominio.

## Ejemplo

Tarea: *"¿qué consume vpp-backend?"*

1. Resolver el file node exacto por título de archivo (`.md`) o alias de frontmatter.
2. Clasificar la intención como **relación**.
3. Consultar primero el edge tipado aplicable y luego `references`; abrir la sección de relaciones del cuerpo sólo si el grafo es insuficiente o la respuesta debe persistirse.
4. Entregar la relación verificada y su fuente, no el archivo entero.

## Relaciones

- [[token-economy-indexing-architecture]] — ADR: las 4 capas y roles (autoridad).
- Skill `agents-os-context-retrieval` — **implementa** el algoritmo de este router (autoridad ejecutable).
- [[30-resources/00-RESOURCE-WIKI|Resource Wiki]] — de dónde salen índice/links curados.
- [[graphify]] — selección exacta por metadata/facets y capa de relaciones; el fork `graphify-obsidian` proyecta frontmatter allowlisted, genera siete edges tipados y conserva los `[[wikilinks]]` como `references`.
- [[Economía de Tokens]] — proyecto que construye y mide todo esto.

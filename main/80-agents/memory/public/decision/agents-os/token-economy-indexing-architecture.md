---
type: decision
scope: project
created: 2026-07-03
updated: 2026-07-07
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
  - "[[Graphify]]"
related:
  - "[[agent-constitution]]"
  - "[[graphify]]"
  - "[[LLM Wiki]]"
  - "[[agents-os-tagging-system]]"
aliases:
  - arquitectura de indexacion economia de tokens
  - token economy indexing architecture
  - indices graphify vs llm wiki ADR
  - capas de retrieval
confidence: verified
source_session:
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - area/personal
  - kind/decision
  - priority/high
  - project/agents-os
  - project/agentsos
  - scope/project
---
# Arquitectura de Indexación para Economía de Tokens

## Contexto

- El vault existe para **economía de tokens**: un agente debe entender lo necesario
  cargando en su contexto **solo el mínimo**, sin basura.
- Conviven varios "métodos de indexación": tags/frontmatter, `00-index.md` curado
  (LLM Wiki), grafo AST de Graphify, y la extracción semántica de Graphify (LLM).
- Sin reglas claras se cae en dos fallas: (a) basura entra al contexto (nodos-god
  de JSON, trash, prosa completa); (b) se paga LLM para redescubrir lo que la wiki
  ya cura. Verificado 2026-07-02/03: corpus contaminado (512 trash + 170 json) y
  el free tier de Gemini no alcanza para la semántica del vault.

## Decisión

Retrieval en **4 capas, cada una filtra antes de la siguiente**. Nunca saltar capas;
al modelo entra solo el mínimo.

```
Capa 0  TAGS/frontmatter   → filtro GRATIS: "¿qué conjunto?"         (grep/dataview, 0 tokens LLM)
Capa 1  00-index.md (wiki)  → catálogo curado: "¿qué página abro?"   (leer 1 archivo)
Capa 2  graph.json (AST)    → relaciones/paths/lint                  (lectura programática mínima)
Capa 3  cuerpo de la nota   → SOLO lo elegido, SOLO el body          (lectura quirúrgica)
```

Roles fijos de cada índice:

- **LLM Wiki = capa semántica + retrieval primario (fuente de verdad).** Las conexiones
  se escriben curadas como `[[links]]` al ingerir; el `00-index.md` es el catálogo.
- **Graphify (modo `update`, AST, sin LLM) = índice estructural derivado.** Para
  auditoría/lint del grafo completo, `path`, `affected` y navegación. NO es verdad,
  se regenera. Se mantiene limpio vía `.graphifyignore`.
- **Tags = capa 0, filtro gratis.** Viven en **frontmatter** como slugs del vocabulario
  de `90-system/convenciones.md`. NUNCA tags inline en el cuerpo para indexar (ruido de
  grafo + entran al contexto). Linteados por `agents-os-tagging-system`.
- **Graphify semántico (`extract --mode deep`) = PARQUEADO.** Solo para proyectos de
  **código** y solo vía API paga cuando se justifique. No se usa en el vault de markdown.

Regla dura anti-basura: cargar **solo el body** de una nota (sin frontmatter ni bloques
`tasks`), y aplicar techos blandos de tokens por tier en cada query (suficiencia-first,
no guillotina; ver [[context-router]]).

### grep vs graphify vs semántica (tres herramientas, tres preguntas)

No se solapan; elegir la barata que responde la pregunta antes de escalar:

| Herramienta | Pregunta que responde | Costo |
|---|---|---|
| **grep / búsqueda de texto** | *¿dónde está?* — encontrar una cadena/nota exacta | gratis |
| **graphify (AST)** | *¿con qué se relaciona?* — edges, `path`, `affected`, lint | gratis (sin LLM) |
| **semántica (LLM)** | *¿qué significa?* — similitud conceptual, síntesis | caro (API paga) |

Corolario clave: **grep encuentra, graphify relaciona, la semántica significa.** Curar
`[[links]]` e índices reduce la necesidad de semántica. Y para relaciones **del vault**, el
fork **`graphify-obsidian`** (vault-aware) ya convierte los `[[wikilinks]]` en edges
`references` (resuelto 2026-07-04; sin builder standalone) → la Capa 2 relacional funciona
también en el vault, no solo en código. El grafo relaciona por **links** (wikilinks → edges
`references`), **no por tags** (los tags son Capa 0, filtro de frontmatter).

### Relaciones graphifeables: links tipados (input del builder)

La Capa 2 del vault ya funciona: `graphify-obsidian` emite un edge `references` por cada
`[[wikilink]]`. Los links tipados (**implementados 2026-07-07** en el fork) tipan esas
relaciones: el verbo distingue el `relation` del edge. Contrato:

- **Verbos canónicos (única forma aceptada):** `consume`, `decora`, `depende de`, `expone`,
  `reemplaza a` (case-insensitive). El verbo → `relation` reemplazando espacios por `_`
  (`depende de [[X]]` → `depende_de`, `reemplaza a [[Y]]` → `reemplaza_a`). **Sin variantes
  bare** (`depende`/`reemplaza` solos NO se tipan): dos nombres para la misma relación
  fragmentarían el grafo. Sin verbo canónico → `references`.
- **Scoping obligatorio a `## Relaciones`:** el parser tipa **solo** dentro de esa sección
  del cuerpo (los sub-headings más profundos la mantienen abierta; un heading hermano/padre
  la cierra). Fuera de ella un verbo es prosa —incluida una **negación** "no depende de
  [[X]]"— y el link cae a `references`. Esto es lo que preserva el determinismo. No en
  frontmatter, **nunca inline como tags**. Una relación = una línea (`grep`/diff-eable).
- **`RELATIONS.md`/MOC por dominio — descartado como fuente:** mantener una edge-list a
  mano es doble fuente de verdad (drift). La relación se escribe **una vez** en `## Relaciones`;
  el edge-list/MOC, si se quiere, se **genera** con `graphify-obsidian`, no se cura a mano.
  (Consistente con "una fuente canónica por hecho".)
- **Query:** los edges tipados, como `references`, no están en las relaciones por defecto de
  `affected` → recorrerlos exige `--relation <tipo>` explícito (ej. `affected "<nota>.md"
  --relation depende_de`). Ver [[Economía de Tokens]] y `graphify.md`.

## ¿Graphify (solo índices) aporta o estorba?

**Aporta — NO estorba — siempre que:** (1) el corpus esté limpio (`.graphifyignore`),
y (2) se use para lo que es bueno: **lint/auditoría del grafo completo** (huérfanos,
god-nodes, links rotos), `affected`/`path` y descubrimiento cross-dominio — cosas que
el `grep` sobre `00-index.md` no hace por sí solo.

**Estorba solo si:** se ensucia el corpus, o se lo usa como capa de retrieval/semántica
de markdown (ahí ganan los tags + el índice curado). A la escala actual su valor es
**acotado pero real**; el motor de ahorro de tokens son las capas 0-1, Graphify es el
auditor estructural de apoyo.

## Rationale

- Cada capa más barata filtra antes de la más cara → el contexto del modelo recibe el mínimo.
- Los tags en frontmatter permiten retrieval sin leer cuerpos (0 tokens LLM).
- La wiki curada da semántica confiable sin costo de extracción ni alucinaciones.
- Graphify AST es gratis (sin LLM) y cachea por hash: correrlo seguido cuesta casi nada.
- Markdown como fuente de verdad; Graphify como índice derivado y desechable.

## Consecuencias

- Se construye un **wrapper/capa delgada sobre `graph.json` + `00-index.md`** que emite
  el paquete mínimo de contexto con **techo blando por tier** (suficiencia-first, no
  guillotina; ver [[context-router]]). graphify queda intacto (no se parchea
  `site-packages`; fork editable solo si hiciera falta).
- El protocolo de 4 capas se documenta en la skill de retrieval y en el contrato de
  Graphify (`80-agents/skills/_shared/graphify-contract.md`).
- El **cómo cargar** (decidir qué capa/orden/presupuesto por tarea) se formaliza como el
  concepto [[context-router]], implementado por la skill de retrieval. Es la pieza de
  evangelización para el equipo.
- `00-RESOURCE-WIKI.md` y `graphify.md` referencian este ADR para el "aporta/estorba".
- La medición del ahorro (`graphify benchmark` + feedback/kaizen) es deseable pero
  opcional; ver idea en `30-resources/ideas/`.

## Alternativas descartadas

- **Solo Graphify (con semántica) sin wiki:** semántica LLM de markdown ruidosa/cara y
  free tier insuficiente; alucinaciones no confiables.
- **Solo wiki sin Graphify:** se pierde el lint/traversal del grafo completo y el
  `affected`/`path` programático.
- **Sin tags / tags inline en el cuerpo:** rompe el filtro gratis de capa 0 y ensucia
  el grafo con nodos-god.
- **Cargar notas completas (con frontmatter/tasks):** mete basura evitable al contexto.

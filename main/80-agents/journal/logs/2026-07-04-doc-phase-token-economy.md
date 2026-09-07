---
type: change_log
scope: project
created: 2026-07-04
updated: 2026-07-04
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[Economía de Tokens]]"
  - "[[context-router]]"
  - "[[token-economy-indexing-architecture]]"
  - "[[agents-os-hygiene-review]]"
  - "[[agents-os-context-retrieval]]"
tags:
  - kind/changelog
  - area/personal
  - project/agents-os
---

# 2026-07-04 — Fase documentación: barrido de caps + resto de docs (Economía de Tokens)

## Motivo

El owner pidió completar **toda la documentación primero** (código después, con otro
agente y contexto limpio) y fue enfático: **no debe quedar ningún cap duro de tokens** —
un corte en bruto puede tirar la línea más relevante y empeorar la respuesta.

## Cambios

- **Semántica de budget canónica (fix del cap):** nueva sección "Budget semantics" en
  `_shared/graphify-contract.md` — `--budget N` es **techo blando por tier**, escala
  on-miss, nunca guillotina; ningún target fijo de tokens. Todo `--budget` disperso
  (incl. el `1200` de `agents-os.md`) hereda esta definición sin editar cada sitio.
  Purgados además: `agents-os-bootstrap` ("keep under budget"→suficiencia-first),
  wording de `agents-os-context-retrieval`, nota en `agents-os-graphify-maintenance`.
- **`00-RESOURCE-WIKI.md`:** nueva sección "Escalado del índice (plano → jerárquico)"
  con umbral smell-test y patrón índice-de-índices (ref. `aranea/`).
- **ADR:** nueva subsección "Relaciones graphifeables: links tipados" — la relación se
  escribe 1 vez en `## Relaciones` del cuerpo (verbo→`relation`); `RELATIONS.md`/MOC a
  mano descartado (doble fuente); el edge-list se **genera** con el builder.
- **`agents-os-hygiene-review`:** nueva sección "Token-Economy & Consistency Checks"
  (frescura de índice, cobertura de links, escalado, compliance de tags capa 0,
  huérfanos/god-nodes) + **auditoría de consistencia DEFINE≠IMPLEMENTA recurrente**.
- **`tools/` alineado al patrón wiki:** creado `tools/00-index.md` (catálogo) + `log.md`;
  `README.md` demovido de `type: index` (slug `tools-index`) a `type: doc`
  (`tools-conventions`) para no tener dos catálogos que compitan.

## Diseño propuesto (NO aplicado — requiere aprobación)

- **Adelgazar `agents-os.md` § Retrieval:** hoy enseña su propia receta graphify con
  `--budget 1200` = **segundo método** que compite con el router (anti-patrón "2
  approaches para 1 abstracción"). Diff propuesto: reemplazar la receta por punteros al
  concepto ([[context-router]]) + implementación (`agents-os-context-retrieval`) +
  contrato (`graphify-contract`). Guard del proyecto: archivo de alta autoridad, no se
  edita sin aprobación explícita.

## Validación

- `grep -rniE "budget|guillotin|--budget|near [0-9]+ token"` sobre skills/agents-os/memory:
  ya no hay número presentado como cap; todos remiten a "Budget semantics".
- Referencias cruzadas coherentes (ADR ↔ router ↔ retrieval ↔ graphify-contract ↔ wiki).
- `tools/`: un solo catálogo (`00-index.md`); README sin tabla-índice duplicada.
- Reindex de Graphify pendiente al cierre de esta fase.

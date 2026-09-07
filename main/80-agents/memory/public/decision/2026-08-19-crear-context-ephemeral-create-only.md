---
type: decision
schema_version: 1
scope: project
created: "2026-08-19"
updated: "2026-08-19"
area: "[[Meli]]"
project: "[[Crear Context]]"
application:
entities:
  - "[[Crear Context]]"
  - "[[rio-playmaker]]"
related:
  - "[[signals-context-flow]]"
  - "[[deploy-component]]"
aliases:
  - Context efímero de componente
  - Crear Context sin persistencia
confidence: verified
source_session:
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/crear-context
---

# Crear Context es efímero y create-only

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- El I/O vigente ya existe distribuido entre `parameters`, relaciones, outputs de CP y `service/deployment.values`. Persistir otra representación calculada crearía duplicidad y riesgo de drift.
- El alcance de [[Crear Context]] es producir el objeto, no migrar el flujo existente ni lograr que los CP lo consuman.

## Decisión

- `Context` se calcula on-demand cada vez que Playmaker procesa el request correspondiente. No se crea tabla, repositorio, snapshot ni backfill.
- La iniciativa agrega modelo + builder + pruebas en paralelo. `parameters`/properties y sus consumidores permanecen sin cambios; el uso futuro de `Context` es otra iniciativa.

## Rationale

- Un objeto derivado usa la información vigente y evita sincronizar dos copias del mismo dominio.
- Separar creación de adopción limita el blast radius y permite comprobar el contrato sin alterar deploys actuales.

## Consecuencias

- La SPEC técnica debe excluir persistencia, migración front→backend y cambios en CPs.
- Antes del diseño se necesita una matriz I/O as-is exhaustiva para saber qué datos debe poder representar el builder.
- La no-regresión se demuestra preservando payload y comportamiento de `parameters`, no mediante un plan de cutover.

## Alternativas descartadas

- **Persistir Context por componente/definición:** descartado por duplicidad, drift y lifecycle ambiguo.
- **Reemplazar `parameters` dentro de la misma iniciativa:** descartado por estar fuera de alcance y aumentar innecesariamente el riesgo.
- **Adaptar inmediatamente todos los CP para consumir Context:** postergado a una iniciativa de adopción separada.

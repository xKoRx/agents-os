---
type: learning
scope: project
created: "2026-07-01"
updated: "2026-07-01"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[Destaques de Precio]]"
  - "[[Bajo y Muy Bajo Precio]]"
aliases:
  - no dividir contenido entre proyecto padre e hijo sin confirmar
  - parent child project ownership
confidence: high
source_session: "80-agents/journal/sessions/raw/2026-06-30-rfc-pricing-motors-fipe-mlb-hitos-raw.md"
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/project
  - project/agents-os
---

# Verificar dueño real del contenido antes de repartirlo entre proyecto padre e hijo

## Aprendizaje

Cuando una iniciativa tiene un proyecto padre en Sistema 2 con subproyectos hijos que representan hitos/fases (ej. `[[Destaques de Precio]]` con hijos `[[Bajó de Precio]]` y `[[Bajo y Muy Bajo Precio]]`), no asumir que una decisión nueva de diseño "pertenece" al padre solo porque afecta a un subconjunto (ej. un site) del alcance de un hijo. En esta sesión, una decisión de diseño (pivot FIPE para MLB) que era parte central del Hito 2 se registró primero en el proyecto padre y se excluyó del hijo (`Bajo y Muy Bajo Precio`), cuando en realidad esa decisión pertenecía enteramente al hijo — el usuario tuvo que corregirlo explícitamente.

## Aplicabilidad

- **Cuándo cargarlo:** al actualizar documentación/entidades Sistema 2 de un proyecto que tiene padre + subproyectos por hito/fase, especialmente si una nueva decisión cambia el alcance de un subconjunto (site, plataforma, dominio) dentro de un hito ya existente.
- **Cuándo no cargarlo:** proyectos sin jerarquía padre/hijo, o cuando el usuario ya indicó explícitamente a qué entidad pertenece la información.

## Regla operativa

- Antes de repartir contenido nuevo entre un proyecto padre y sus hijos, verificar contra los hijos existentes (nombre, alias, objetivo declarado) cuál es el dueño real, en vez de inferirlo por default hacia el padre.
- Si hay ambigüedad genuina sobre a qué proyecto pertenece una decisión, es preferible preguntar brevemente o declarar la asunción explícita al usuario, en vez de repartir el contenido de forma silenciosa entre padre e hijo.
- Un hito puede tener múltiples ramas de diseño (por site, por plataforma, etc.) sin dejar de ser el mismo proyecto: no fragmentar el hito en "lo que sí entra" vs "lo que se saca al padre" sin confirmación.

## Entidades relacionadas

- [[Destaques de Precio]] (padre / iniciativa)
- [[Bajo y Muy Bajo Precio]] (hijo, Hito 2 completo — incluye MLB vía FIPE y resto de sites vía Sugeridor)
- [[Bajó de Precio]] (hijo, Hito 1)

## Evidencia

- Fuente: `80-agents/journal/logs/2026-07-01-bajo-y-muy-bajo-precio-scope-correction-entity-updated.md` — corrección literal del owner (2026-06-30/07-01): "la parte 2 es en realidad el proyecto de Bajo y Muy Bajo de precio... esto es el hito 2".

---
type: change_log
scope: project
created: 2026-07-03
updated: 2026-07-03
area: "[[Meli]]"
project: "[[Refactor Polycard]]"
entities:
  - "[[Refactor Polycard]]"
  - "[[Single View Layout — Migración al Polycard SDK]]"
related:
  - "[[java-polycard-sdk]]"
  - "[[search-middleware]]"
confidence: high
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/meli
  - project/refactor-polycard
---

# Single View Layout SDK Migration — Project Created

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - Creado proyecto de agente `10-projects/Refactor Polycard/agentes/Single View Layout — Migración al Polycard SDK.md` (`owner: agent`, `parent: [[Refactor Polycard]]`).
  - Convertida la iniciativa `[[Refactor Polycard]]` de archivo plano a carpeta: `10-projects/Refactor Polycard.md` → `10-projects/Refactor Polycard/Refactor Polycard.md` (links por nombre, no se rompen).
  - Actualizado `[[Refactor Polycard]]`: agregada tarea puente `#owner/me #type/supervision` + línea de bitácora.

## Motivo

El TL de Search (Duvan) pidió mover la personalización de orden del Single view (Motors/VIS) — hoy en `MotorsSingleLayoutDeciderFactory` de search-middleware — hacia el Polycard SDK, porque el Single solo lo usa MOT/RE (VIS) y tenerlo en search-mid genera fricción en el refactor del flujo poly. El usuario pidió dejar el trabajo documentado como proyecto de agente para que otra IA lo ejecute a la perfección.

## Fuentes usadas

- Análisis de código en `/Users/rjara/fuentes/search-middleware` (develop) y `/Users/rjara/fuentes/java-polycard-sdk` (master).
- Conversación con el TL (contexto del pedido).
- Reglas AGENTS OS: `agents-os.md` (regla proyectos humano vs agente), `agents-os-agent-project-workflow`, `90-system/convenciones.md`.

## Resolución aplicada

- Enfoque decidido: **Opción B** (portar el factory al SDK como API pública), sobre A (bakear en default) y C (`DefaultLayoutDeciderV1_3`). Rationale en la nota del proyecto.
- Ramas `feature/single-view-layout-sdk-migration` creadas en ambos repos desde `origin/master` (SDK, base `820146c4bc`, versión 8.183.0) y `origin/develop` (search, base `14cc68ff17f`, consume 8.182.0).
- Ejecución (código + tests) NO realizada: el rol de esta sesión fue análisis + setup + documentación.

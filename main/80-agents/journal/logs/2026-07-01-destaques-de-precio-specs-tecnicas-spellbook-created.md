---
type: log
scope: entity-update
created: 2026-07-01
entities:
  - "[[Bajo y Muy Bajo Precio]]"
  - "[[RFC Destaques de Precio - Hito 2]]"
tags:
  - kind/log
  - area/meli
---

# Log — Specs técnicas de Destaques de Precio (Hito 2) creadas en Spellbook

## Qué cambió

- Se crearon 2 specs técnicos nuevos en Spellbook (previamente no existían; solo estaban las funcionales):
  - `Destaques de Precio — Polycard Search — Spec Técnica` (`9b8e70ce-f46a-497b-9df7-4b1ab2c99208`, proyecto `VMDUPPER`/Upper Funnel, status `review`).
  - `Destaques de Precio — VIP — Spec Técnica` (`93d572e8-4d58-4876-8e1c-71653b58f035`, proyecto `VISMDMID`/Mid Funnel, status `review`).
- Contenido migrado 1:1 desde `sb-main/01_Projects/previous-price-motors/Destaques de Precio — Polycard Search — Spec Técnica Propuesta.md` y `... VIP — Spec Técnica Propuesta.md`, con el header `Funcional:` re-apuntado a la spec funcional real en Spellbook.
- Cada spec técnica se linkeó como **dependencia** (`specs deps add`, no `children` — reservado a epics) de su spec funcional correspondiente (`2513a123-bdfe-481d-98d0-f7bfb3d572fe` Search, `ddf10fe9-af96-4208-9eac-01bfb71abfe5` VIP).
- Se prepararon tasks de implementación para ambas specs (7 para Search, 6 para VIP) y se guardaron localmente en `tasks-destaques-precio-search.json` / `tasks-destaques-precio-vip.json` — **no importadas** porque Spellbook exige que el spec esté en `ready_to_code` (requiere ≥1 aprobación) y ambas siguen en `review` al ser propuesta con puntos abiertos.
- Se actualizaron `[[Bajo y Muy Bajo Precio]]` y `[[RFC Destaques de Precio - Hito 2]]` con referencias, tareas y bitácora reflejando lo anterior.

## Por qué

- Pedido explícito del usuario: crear las specs técnicas de "precio bajo y muy bajo" para llevarlas a Spellbook, identificando los proyectos correctos con Nexus + Spellbook, y actualizar el proyecto con referencias y tareas.
- Los proyectos Spellbook correctos se identificaron vía `sb-main/03_Resources/config/nexus-config.json` (mapeo Nexus↔Spellbook): Search = Upper Funnel (`VMDUPPER`), VIP = Mid Funnel (`VISMDMID`), confirmado también por los códigos jira (`VMDUPPER-5`, `VISMDMID-4`) ya presentes en el frontmatter de `[[Bajo y Muy Bajo Precio]]`.

## Decisión explícita durante la sesión

- No se forzó la transición a `ready_to_code` de ninguna spec pese a que el import de tasks lo exige, porque ambas siguen siendo propuesta técnica sin aprobación real ni puntos abiertos resueltos. Se dejó ese paso como tarea pendiente para el usuario/equipo.

---
type: change_log
scope: global
created: 2026-07-04
updated: 2026-07-04
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agent-constitution]]"
  - "[[agents-os]]"
  - "[[agents-os-session-close]]"
tags:
  - kind/changelog
  - area/personal
  - project/agents-os
---

# 2026-07-04 — Auditoría amplia de consistencia del Sistema 1

## Motivo

El owner pidió auditar TODO el Sistema 1 (no solo el token-economy) contra los principios,
incluidos los nuevos de hoy. Auditoría mecánica (yo) + cualitativa (subagente). Hallazgos
reales corregidos; dos observaciones dejadas como decisión del owner.

## Cambios aplicados

- **Cierre de Sesión — deduplicado (mismo patrón que Retrieval):** había DOS procedimientos
  de cierre que competían y divergían (constitución 5 bullets vs `agents-os.md` 9 pasos;
  "L1 si aporta valor" vs "solo si aporta continuidad"). Fix: la skill `agents-os-session-close`
  es la **fuente canónica del procedimiento**; `agents-os.md` § Cierre → puntero; constitución
  § Cierre → solo reglas + declara la skill canónica. Una abstracción, una fuente.
- **Template `learning.md` — sección Evidencia:** aclarado que es **cita de fuente**
  (link + 1 línea), NO prosa narrativa (causa raíz del bloat de learnings). Alinea con la
  regla "memorias compactas".
- **Frontmatter de skills (validez):** `hermes-dashboard-recovery` (+`type: skill`, `tags`),
  `operational-healthcheck-policy` (+`description`).
- **ADR — lenguaje de cap:** "paquete mínimo con tope de tokens" → "techo blando por tier".

## Observaciones dejadas al owner (no arregladas)

- **8 learnings de AGENTS OS con `## Evidencia` inflada** (prosa que parafrasea el criterio ya
  destilado). Causa raíz corregida en el template; compactar las 8 existentes es una pasada de
  higiene aparte — NO se hace en masa al vuelo por riesgo de perder evidencia real (requiere
  juicio por archivo). Pendiente de OK como pasada dedicada.
- **`hermes-dashboard-recovery` es un runbook vestido de skill** + copia-espejo de una skill
  viva externa. Reclasificar/mover es decisión del owner (es un puente deliberado a infra suya).

## Rechazado (nitpick, no violación)

- "Codex" mencionado en Progress Logs de skills: es **historial** (quién forward-testeó), no
  acopla el procedimiento a un cliente. Borrarlo sería revisionismo sin beneficio. Se mantiene.

## Validación

- `agents-os.md` y constitución ya no tienen procedimientos de cierre que compitan.
- Frontmatter de skills: todas pasan el chequeo (type/name/description/tags).
- Veredicto del subagente: Sistema 1 mayormente alineado; sin deuda estructural general.

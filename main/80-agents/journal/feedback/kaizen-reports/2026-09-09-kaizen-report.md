---
type: kaizen-report
schema_version: 1
scope: session
created: "2026-09-09"
updated: "2026-09-09"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[2026-07-04-kaizen-report]]"
  - "[[2026-09-09-full-system-1-hygiene-review]]"
aliases: []
confidence: high
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/kaizen-report
  - scope/session
  - agent/system1
  - project/agents-os
---

# Kaizen Report — 2026-09-09

Ventana 2026-07-05 → 2026-09-09. **340 feedbacks** (294 `system-1`, 45 `graphify`, 1 `session`), casi 7× el umbral de ~50 que fijó el reporte anterior. Segundo reporte Kaizen del sistema, 67 días después del primero. Análisis agregado.

## Resumen ejecutivo

El sistema **escribe con disciplina excelente y no lee**. La captura es de primer nivel: 340 notas estructuradas, con severidad, propuesta y evidencia. La agregación no ocurrió sin pedido humano, y el 61% de esos feedbacks no es citado por ningún artefacto. Ese es el hallazgo central del período.

Salud por dimensión, sobre ~240 notas con score (1–5):

| Dimensión | Promedio | Tendencia jul→sep |
|---|---|---|
| Overall confidence | 4,67 | 4,60 → 4,73 → 4,65 |
| Startup clarity | 4,62 | 4,45 → 4,76 → 4,60 |
| Skill fit | 4,52 | plano |
| Retrieval usefulness | 4,36 | 4,32 → 4,34 → 4,41 |
| Template fit | 4,19 | 4,35 → 4,06 → 4,20 |
| **Closeout friction** | **3,38** | 3,53 → 3,32 → 3,34 |

El arranque está sano. El cierre es el peor score del sistema por margen, es el único cuya moda es 3 y no mejoró tras el rediseño de julio.

Dos tercios de las sesiones (64%) declaran que su dolor va a volver. De los 60 feedbacks `high`, sólo ~8 son del sistema; el resto es dominio.

## Dolores recurrentes

| # | Patrón | Recur. | Sistema/dominio | Estado tras esta corrida |
|---|---|---|---|---|
| P1 | Gate de lint all-or-nothing bloquea el reindex de un delta ya válido | 6 | Sistema | ✅ **CERRADO** — baseline poblado, gate GO, reindex verde |
| P2 | Graphify no escribe caché en sandbox → índice stale | 7 | Sistema | ⚠️ Abierto (documentado, no resuelto) |
| P3 | Fallback a `grep` porque Graphify no aporta sobre búsqueda dirigida | 17+20 | Sistema | ⚠️ Aceptado de facto |
| P4 | Ruido de nodos genéricos, plantillas, trash e históricos | 22 | Sistema | ⚠️ Parcial — `.trash/` ahora excluido |
| P5 | Skills canónicas no descubribles nativamente | 4 | Sistema | ⚠️ Abierto — 36/39 sin router; propuesta 3 |
| P6 | Rutas de scripts dentro de skills rotas o relativas al lugar equivocado | 4 | Sistema | ⚠️ Abierto |
| P7 | Ritual/template de cierre desproporcionado al valor de la sesión | 11 | Sistema | ⚠️ Parcial — propuesta 5 |
| P8 | La herramienta/MCP que la skill exige no está en la superficie | 12 | Sistema | ⚠️ Abierto — propuesta 4 |
| P10 | Subagentes: reporte final vacío, timeout 600s, sin heartbeat | 4 | Sistema | ✅ Promovido a runbook + known error |
| P11 | Checkpoints append-only mezclan estado superseded | 6 | Sistema | ✅ Promovido a learning |
| P12 | Divergencia contrato/skill ↔ CLI real | 4 | Sistema | ✅ Ampliado el known error de la familia |
| P13 | Overclaim: `PASS`/`CLOSED` sin verificación física | 11 | Mixto | ✅ Promovido a learning |
| P14 | Output masivo de herramientas inunda el contexto | 7 | Entorno | ⚠️ Abierto |
| P16 | El bootstrap no se disparó o su ruta no resolvió | 4 | Sistema | ⚠️ Abierto — es el punto único de falla |

P15 (búsqueda acotada tratada como prueba de ausencia) se cerró en el período con promoción a learning: es el único ciclo Kaizen completo de punta a punta —fricción, reproducción, promoción, cita de vuelta— y es el modelo a replicar.

## Salud de Graphify

Se degradó de herramienta de retrieval a gate de publicación que suele estar roto. Utilidad declarada **3,19/5** (era ~3,8 en julio), sobre 31 notas con score de 45. De 294 feedbacks de `system-1`, 109 mencionan Graphify como modo de retrieval y 20 declaran explícitamente que no se usó, casi siempre por índice stale.

La progresión de deuda bloqueante del gate fue 10 → 12 → 12 → 26 → 31 → 32 → **136 findings**. El mecanismo de baseline existía desde 2026-08-11 y estaba vacío: herramienta correcta, nunca adoptada. Esta corrida lo pobló y el reindex volvió a pasar.

Dónde sigue siendo útil, según los propios agentes: `explain` por **título exacto** de una entidad canónica, para verificar descubribilidad después de un cambio. Fuera de eso la búsqueda Markdown dirigida gana. La conclusión de julio se sostiene; lo que se redujo es la fracción de sesiones donde vale pagar el costo.

## Promesa vs realidad

| Promesa | Veredicto | Evidencia |
|---|---|---|
| Memoria persistente que evita reexplicar contexto | **Cumplida** | Startup 4,62/5; memoria interna consultada en 201 sesiones con utilidad 4,39/5. La única sesión que re-derivó todo fue la que no cargó el sistema |
| Retrieval por capas con el mínimo contexto suficiente | **Parcial** | 4,36/5 y la práctica sigue el modelo, pero `context_high_water_mark` vale `unknown` en las 12 notas que lo traen: no hay una sola medición de tokens en el corpus |
| Skills como procedimientos canónicos reusables | **Parcial / no en discovery** | Skill fit 4,52/5 —el contenido funciona— pero 36 de 39 skills no son invocables nativamente. El problema es el envase |
| Una fuente canónica por hecho | **Parcial** | Para dominio se cumple (7 casos en 340). Para skills y taxonomía no: una skill existió en dos lugares con la copia del vault **desactualizada**, y coexistían `known-error/` y `known-errors/` |
| Higiene/Kaizen como bucle que corre | **No cumplida** | 0 reportes Kaizen en la ventana; 3 ciclos de higiene, todos por pedido; 61% de feedbacks nunca citados; de las promociones L3 del período, sólo 2 hablaban del sistema |
| Portabilidad entre superficies | **Parcial** | 8 superficies produjeron feedback con el mismo contrato, lo que es portabilidad real; pero cada una rompe algo distinto y el sistema no tiene forma declarativa de saber qué falta |
| Agentes delegados / subagentes | **No cumplida** | No existía skill, runbook ni known error de delegación. El patrón G de julio acumuló 3 fallas nuevas y distintas |

## Lo que sobrevivió al forward-test

- **Cierre táctico → Delta Classifier.** Propuesto el 2026-07-04, en uso el 2026-07-06, luego generalizado a un clasificador con presupuesto explícito. Resolvió *si* cerrar; no movió el score de fricción.
- **Router en vez de copia para skills.** Nacido del hallazgo de la skill duplicada. Los routers del cliente pesan 1,5–1,8k y referencian el vault; las canónicas 6–15k. Eliminó la divergencia para esa familia.
- **Checkpoint append-only con `NEXT EXACT`.** El mecanismo de continuidad más elogiado del período (~15 notas). Su costo de vigencia es real pero secundario frente al beneficio; de ahí el learning nuevo en vez de un cambio de diseño.
- **Separación `agent_surface` / `agent_model` + `model_source`.** Limpió el campo sucio de julio y convirtió una ambigüedad en deuda declarada (105 `unknown`).

## Promociones aplicadas

- `runbook/reindex-bloqueado-por-deuda-global.md` — P1, 6 sesiones.
- `runbook/delegacion-a-subagentes.md` + `known-error/agents-os/subagente-devuelve-reporte-vacio.md` — P10, 4 sesiones y 3 modos de falla.
- `learning/agents-os/checkpoint-append-only-no-declara-vigencia.md` — P11, 6 sesiones.
- `learning/agents-os/pass-declarado-no-es-pass-verificado.md` — P13, 11 sesiones cruzando dominios.
- Ampliación de `known-error/agents-os/graphify-markdown-wikilink-and-backend-gaps.md` con el drift contrato↔CLI — P12, 4 sesiones.

## Propuestas que requieren decisión del owner

1. **Descubribilidad de skills** (P5): generar router por skill, o declarar el fallback por ruta con verificación de disponibilidad en bootstrap. Son caminos excluyentes.
2. **Diagnóstico de capacidades por superficie en bootstrap** (P8, portabilidad, delegación): pedido tres veces.
3. **Modo reducido del template de feedback** (P7): campo `mode: tactical|full` y permiso de omitir secciones sin hallazgo. Toca el contrato de cierre.

## Lo que no se pudo cuantificar

- **Consumo real de contexto.** El campo existe desde 2026-09-06 y vale `unknown` siempre. Todo lo dicho sobre economía de tokens en este reporte es cualitativo.
- **Utilidad de Graphify en 14 de sus 45 notas** y **severidad en 37 de 45**: el template de graphify-feedback divergió del de session-feedback y no exige esos campos.
- **Tiempo perdido por fricción.** Una sola nota lo mide (~10 min por subagente muerto).
- **Si las 209 notas nunca citadas contenían señal que se perdió.** Es exactamente el costo de no correr el bucle en 67 días.

## Watermark

- **Procesado hasta:** 2026-09-09.
- **Próximo reporte:** al acumular ~50 feedbacks nuevos, o en el ciclo de higiene del 2026-09-16 si la cadencia se mantiene semanal.

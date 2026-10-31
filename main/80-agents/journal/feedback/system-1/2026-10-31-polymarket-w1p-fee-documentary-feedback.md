---
type: feedback
schema_version: 1
scope: session
created: 2026-10-31
updated: 2026-10-31
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
entities:
  - "[[AGENTS OS]]"
  - "[[Polymarket Engine — MVP]]"
related:
  - "[[ZCode]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: minimax/MiniMax-M3.1-Flash
agent_run: "[[80-agents/journal/agent-runs/2026-10-31-zcode-minimax-m3.1-flash-polymarket-w1p-fee-documentary.md]]"
session_goal: W1-p — investigación documental de fuentes oficiales Polymarket sobre la fórmula de fee y el campo WS fee_rate_bps (as-of 2026-10-29)
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/agents-os
  - agent/system1
---

# Session Feedback - 2026-10-31 - polymarket-w1p-fee-documentary

## Context

- Agent surface: [[ZCode]] (host `sqx-ulab-hefesto-0`).
- Agent model: `minimax/MiniMax-M3.1-Flash` (reportado por el host; sin fallback ni modelo alterno).
- Agent run: `2026-10-31-zcode-minimax-m3.1-flash-polymarket-w1p-fee-documentary.md` (mismo run; esta nota recoge los findings de la revisión y su corrección).
- Session goal: cerrar el paso documental de fee del mercado `5784455` con fuentes oficiales fechadas, sin capturas, sin código y sin tocar el gate de costes.
- Main entity: [[Polymarket Engine — MVP]] (área [[Personal]]; routing DEFAULT).
- Skills used: `agents-os-bootstrap`, `agents-os-context-retrieval`, `agents-os-code-scout` + `scout-contract` + runbook (inline-fallback), `agents-os-session-close`, `agents-os-session-feedback`, `agents-os-agent-run-register`, `agents-os-entity-update`, `materialize_schema_note.py`.
- Retrieval mode: lectura dirigida del vault (cold start con packs exactos ya inyectados) + WebFetch contra el índice oficial `docs.polymarket.com/llms.txt` y repos oficiales por API pública de GitHub; 78 llamadas en la ventana medida `2026-10-31T11:35:38.606Z`–`2026-10-31T11:44:35.301Z`.
- Artifacts changed: `validated-baseline/w1-p-fee-documentary-20261031/` (6 artefactos) y 8 notas/rutas del vault (informe nuevo + deltas en MVP y Continuidad + sesión + 2 feedbacks + agent run + change_log).

## Scores

- Startup clarity: 5
- Retrieval usefulness: 4
- Skill fit: 4
- Template fit: 4
- Closeout friction: 3
- Overall confidence: 3

## Findings de la revisión de supervisión y corrección aplicada

Cinco hallazgos concretos sobre **mis propios artefactos**, todos corregidos en esta sesión (misma sesión, mismo agent_run, sin notas nuevas):

- **Fórmula no soportada:** generalicé la fórmula documentada a `C × rate × p^e × (1 − p)` sin respaldo y **rompí la simetría `p ↔ 1 − p`** que la propia fuente cita. Corrección: modelo restringido a la fórmula documentada, elegible sólo con `e = 1`; para `e ≠ 1` **no hay modelo** y no se propone forma alternativa; la correspondencia `fd`/`feeSchedule` y la unidad decimal de `rate` quedan como inferencia e hipótesis marcada. **Lección: cuando la fuente nombra un parámetro sin publicar la expresión, el modelo se acota al caso que la fuente sí sustenta; no se generaliza desde la semántica parcial.**
- **Historia rotulada más fuerte que la evidencia:** llamé "probada por régimen" a una fórmula cuya vigencia en el 29-10-2026 no está demostrada, y extendí a "toda categoría con rate 0.05" un anuncio que es específico de Sports. Corrección: la matriz rotula **anuncio documental previo** y **compatibilidad con los parámetros observados**, y §6 queda como anuncio + compatibilidad + **modelo retrospectivo condicional**, sin comisión cobrada ni implementación vigente demostradas; el **destino deportivo** del episodio se toma como dado (encargo + metadata W1-j) y lo no capturado es la etiqueta de política/rebate/override. **Lección: distinguir "lo que la fuente anuncia" de "lo que estaba vigente en la fecha del episodio", y no convertir una ausencia de etiqueta en desconocimiento del hecho que ya está dado.**
- **Precisión y lados:** afirmé un modo de redondeo que las docs no fijan, atribuí al redondeo de la fee cobrada una división entera que es del cálculo del **techo**, mezclé el redondeo de un **importe** con el significado de un **campo de tasa**, extendí `fee ≤ proceeds` como límite universal al lado BUY y traté USDC/pUSD como si fueran el mismo activo. Corrección: modo **no adjudicado** (banda conservadora declarada como hipótesis de modelado), BUY paga collateral adicional y SELL recibe proceeds netos, `fee ≤ proceeds` limitado al camino demostrado, caps por familia/versión sin asumir actividad histórica, y las dos etiquetas de activo conservadas con la unidad del modelo declarada y su incertidumbre.
- **Siguiente paso mal focalizado:** propuse un protocolo centrado en fee cobrada, settlement y micro-trade con capital real, que **no es el siguiente paso autorizado ni necesario para avanzar offline**. Corrección: el draft es ahora un **incremento estrictamente offline de conformidad del modelo** (e = 1, sin captura, sin re-score, sin cuenta ni fondos), con fixtures sintéticos **declarados y no implementados**, sin taxonomía de gates nueva y sin umbrales; el criterio de aceptación es conformidad del **modelo** con fuentes y supuestos, no prueba de cobro. **Lección: el siguiente paso propuesto debe ser el que desbloquea el objetivo del Owner, no el más riguroso en apariencia.**
- **Recibo y bloqueos:** inventé la ventana horaria de consultas (`11:05Z–11:45Z`) y registré sólo dos de las tres rutas denegadas, además de dar por hecho el contenido de archivos cuya URL había intentado. Corrección: ventana medida por el supervisor vía SQLite, tres rutas denegadas con el motivo verificado del filtro (`/actions`), **existencia y contenido no establecidos**, y la limitación de que WebFetch devuelve resúmenes de IA sin hashes de cuerpo. **Lección: no se inventa una marca temporal ni se afirma la existencia de un archivo sólo porque su URL se intentó.**

## What Complicated The Session Most

- Observation: el hook de alcance denegó **tres** archivos del SDK oficial (`packages/client/src/actions/orders/{estimate.ts,market.ts,settlement.ts}`) con `Outside immutable W1-p scope`, y el filtro resultaba ser el substring `/actions` (verificado por el supervisor en el código del hook), lo que bloquea precisamente las rutas de código del SDK.
- Why it was hard: esos archivos habríancontained la lógica de fee del SDK oficial; sin ellos, la parte de "verificación detallada del helper" queda como límite declarado, aunque el modelo documentado con `e = 1` no dependa de ellos. Además el hook rechazó un `--dry-run` del materializador por no ser la forma exacta autorizada.
- Proposed improvement: que el hook de alcance exponga qué URLs del allowlist de dominio quedan fuera de alcance, y que el materializador acepte `--dry-run`.

## Most Useful Part Of Sistema 1

- What helped: la secuencia canónica de cierre (`session-close` → `session-feedback` → `agent-run-register` → `entity-update` + `materialize_schema_note.py`) y el contrato de scout con su modo `inline-fallback` explícito.
- Why it helped: permitió cerrar sin inventar artefactos y dejar el registro atribuible por superficie×modelo con outcome y verificación honestos ("investigación documental, no desarrollo ni tests").
- Keep/change: keep, sin cambios.

## Least Useful Or Noisy Part

- What did not help: los templates de feedback traen muchas secciones pensadas para sesiones de desarrollo (scores de sesión, commentary de memoria interna, nota Graphify) que en esta superficie acotada no aplican.
- Why it was weak/noisy: su llenado obliga a escribir "no aplica" en la mitad de la nota.
- Proposed cleanup: un template de feedback compacto para scouts/superficies acotadas.

## Missing Support

- Problem not solved by Sistema 1: no hay una forma canónica de registrar evidencia de fuente externa (URL + fecha propia + fecha de consulta + estado + qué prueba y qué no) dentro del vault; quedó en un JSON de shot fuera del vault.
- How Sistema 1 could help next time: un tipo o sección estándar para documentos de investigación con fuentes externas, que haga explícita la separación entre evidencia directa, inferencia, hipótesis marcada y claim no resuelto, y que no se confunda con verdad canónica.
- Suggested artifact type: `type: doc` con sección de fuentes, o un tipo nuevo sólo si el Owner lo autoriza (esta sesión no crea taxonomía nueva por instrucción expresa).

## Retrieval Feedback

- Useful query or source: el índice oficial `docs.polymarket.com/llms.txt` como punto de entrada (evitó adivinar rutas); el changelog con fechas de vigencia; los cuerpos de contrato en `raw.githubusercontent.com/Polymarket/*` y los árboles de repos por `api.github.com/repos/Polymarket/*`.
- Missing context: la definición del sujeto de `fee_rate_bps`; la etiqueta de fee-category y `rebateRate` del mercado `5784455`; el `MAX_FEE_RATE` desplegado el 29-10-2026; el modo de redondeo de la fee cobrada.
- Duplicate/noisy result: el árbol recursivo de `ts-sdk` vino truncado; los 404 de `Polymarket/{docs,polymarket-docs,exchange,exchange-core}` fueron ruido esperable.
- Better future query: partir de `llms.txt` y del changelog antes de cualquier árbol de repo; usar `contents` por directorio concreto cuando el árbol recursivo se trunca.

## Skill Feedback

- Skill that worked well: `agents-os-code-scout` + su runbook aplicados inline: la secuencia identidad → reglas → fuentes → flujo → docs vs código → mapa congelado → feedback es exactamente la que ordenó esta tarea.
- Skill that was confusing: ninguno en lo estructural; la ambigüedad estuvo en el alcance de "código oficial" que el hook dejó pasar por dominio pero no por alcance.
- Trigger/routing gap: el contrato de scout no contempla explícitamente el caso "repos remotos vía WebFetch sin clonación", donde "ref/commit y dirty" se traduce a "rama main consultada, sin tags, sin hashes de contenido, árbol posiblemente truncado".
- Suggested contract change: una línea en el runbook que, para repos remotos, sustituya "dirty" por "estado de la rama consultada + ausencia de hash de contenido + estado de truncado" y declare el truncado como límite de cobertura.

## Template Feedback

- Template used: `80-agents/templates/session-feedback.md` (materializado) y `80-agents/templates/session-summary.md`.
- Field that helped: `agent_surface` + `agent_model` (obligan a atribuir modelo exacto y superficie canónica).
- Field that felt redundant: las secciones de scores y memoria interna en este tipo de sesión acotada.
- Missing field: un campo que registre explícitamente "denegaciones de herramienta" (URL + error literal) y "hallazgos de revisión aplicados", que en esta sesión fueron evidencia de primer orden.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? sí — la nota global de continuidad, por el bootstrap obligatorio.
- ¿Qué valor operativo aportó para esta sesión (continuidad, detalles crudos, advertencias)? aportó la advertencia de no repetir efectos laterales ante resultado incierto y la regla de resolver identidad desde la autoridad canónica, que evitó tratar el `fee_rate_bps` observado como identidad de negocio.
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna? no: no hubo delta durable interno; el informe, el ledger y el `prereg-draft.md` bastan.
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad? 4; útil como advertencia de método, poco útil para el contenido técnico, que debe quedar en el vault y en los artefactos del encargo.

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: medium
- Candidate owner: responsable del método de evidencia (agente) y del hook de alcance
- Promote to L3 memory? defer

## One Next Improvement

- Regla de método para evidencia documental: **una fuente se cita con lo que declara y nada más**: si la fuente nombra un parámetro sin publicar la expresión, el modelo se acota al caso sustentado; si no fija un modo de redondeo o una unidad, se declara no adjudicado; y una fecha de commit, un anuncio o una URL intentada nunca se elevan a prueba de vigencia, de despliegue o de existencia.

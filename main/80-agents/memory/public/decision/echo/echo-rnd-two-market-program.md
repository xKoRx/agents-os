---
type: decision
schema_version: 1
scope: project
created: '2026-10-28'
updated: '2026-10-27'
area: '[[Trading]]'
project: '[[Echo — I+D de Estrategias]]'
entities:
  - '[[Echo — I+D de Estrategias]]'
  - '[[Echo I+D — Futures]]'
  - '[[Estrategias IMOX — Forex y CFD con Echo Forge]]'
related:
  - '[[Echo I+D — Mapa de capacidades]]'
aliases: []
confidence: verified
load_policy: load when deciding ownership or boundaries of Echo strategy research
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - tech/agents-os
  - project/echo-rnd
---

# echo-rnd-two-market-program

## Contexto

El discovery encontró capacidades maduras de ejecución/cualificación Futures, gestión de investigación IMOX, extracción MKE y delivery técnico, pero ninguna autoridad única para una I+D Echo permanente entre mercados. El Owner pidió el 2026-10-27 materializar la unificación, conservar dos líneas paralelas y trabajar con un manager global y managers de mercado desde chats del proyecto Trading.

Las propuestas iniciales de crear una fábrica Futures aislada dejaron de ser el marco elegido. Un solo programa no implica un solo motor, mercado, conjunto de datos ni procedimiento técnico.

## Decisión

### Aceptación explícita del Owner

- Crear un programa permanente de I+D Echo con divisiones Forex/CFD y Futures.
- Mantener al Owner como stakeholder y decisor material; managers coordinan con él.
- Forex conserva SQX/Forge/EA. Futures conserva Echo Backtester; SQX es posible alternativa futura entre varias, no dependencia aceptada.
- Priorizar estrategias Futures por challenge y retiros funded, con NQ como único instrumento inmediato.
- No tratar las antiguas cuentas E2T como vigentes: el Owner indicó que nunca las operó.
- Hacer evolucionar metodología, skills y automatización con evidencia y acuerdo aplicable.
- Materializar organización y cerrar con continuidad; no ejecutar campañas, código de producto, cuentas ni producción en esta sesión.

### Diseño operativo aplicado dentro de ese mandato

- [[Echo — I+D de Estrategias]] es la iniciativa raíz de gestión.
- Reutilizar [[Estrategias IMOX — Forex y CFD con Echo Forge]] como división Forex; crear [[Echo I+D — Futures]] para la responsabilidad que faltaba.
- Crear `echo-rnd-manager` y `echo-futures-research-manager`; extender `imox-strategy-research` sin otra skill/planner Forex.
- Reutilizar `echo-retester-master` y el qualification runbook. Hacer explícita conformidad fuente/spec/código/operación y corregir excepciones textuales que contradecían G2C; los gates económicos/técnicos no se rebajan.
- Un único runbook común para la mecánica de registros, mandatos, retornos y mejora; operaciones físicas permanecen en sus autoridades.
- Cada investigación aporta a una celda o conjunto de celdas. Las capacidades de soporte indican celdas beneficiarias sin inventar alpha.
- WIP por defecto: una pregunta primaria por mercado, con workers de partes independientes; el Owner puede ajustar este default sin tratarlo como invariante.
- Mantener rutas e historia; reparentar iniciativas de investigación, conservar dependencias técnicas y una sola tarea puente donde aplica.
- Consolidar ocho pares de runbooks idénticos: autoridad federada y antiguas rutas core como redirecciones, sin eliminar historia.

### No decidido por esta reorganización

Perfil actual de Provider/Program/RuleSet, riesgo/MM nuevo, presupuesto experimental, selección de primera estrategia, ampliación de instrumentos/datos, implementación SQX-Futures, aceptación de entregas previas y producción. La matriz Futures v1 es propuesta, no shortlist ni evidencia de rentabilidad.

## Consecuencias

- Una entrada global y un planner por mercado permiten abrir chats separados sin duplicar la verdad.
- Forex continúa F0→F1→F2→F3 y conserva su objetivo táctico Owner de estudiar diez activos hasta el 31-12-2026; no se reinicia el rescate 142.
- Futures comienza con FUT-R01 para inventario/recibos/cobertura NQ y preparación del perfil económico/mandato. ClutiFX permanece secundaria y no bloquea otras fuentes.
- Optimización conserva su contrato acotado, incluyendo sus objetivos específicos; no se convierten en cuotas del programa.
- El objetivo de retirar exige evidencia posterior a challenge; un pase, una campaña terminada o P&L positivo no aceptan una estrategia.
- Cambios de método rutinarios dentro del mandato se validan y registran. Cambios materiales se deciden con el Owner; la auto-mejora no concede autonomía ilimitada.
- Producto/runtime, datos y flota conservan sus gates. Las notas unificadas no certifican disponibilidad física ni operación.

## Alternativas consideradas

- Extender Optimización para gobernar todo: descartado por mezclar laboratorio/entrega acotada con selección científica permanente y con Forex.
- Crear otro programa Forex o renombrar/duplicar IMOX: innecesario; existe responsabilidad equivalente y evidencia que debe conservarse.
- Crear una skill distinta por cada agente: innecesario; funciones reusables pueden ser utilizadas por muchas instancias.
- Mover físicamente todos los proyectos y fusionar motores/runbooks: coste y riesgo de enlaces/autoridad sin beneficio para este objetivo.
- Mantener iniciativas de investigación separadas sin padre común: sustituido por el mandato Owner de unificación.

## Fuentes y recuperación

- Mandato directo del Owner, conversación de diseño de Echo I+D, 2026-10-27.
- Discovery de `xKoRx/agents-os@81d4d6b00205855d223914f2c6d7ac70aebc5fa1`.
- [[Echo I+D — Mapa de capacidades]] para auditoría y autoridades.
- [[30-resources/runbooks/echo-rnd-cycle-runbook|Ciclo común]] para registro, handoff y mejora.

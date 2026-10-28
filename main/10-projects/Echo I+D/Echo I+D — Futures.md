---
type: project
schema_version: 1
owner: me
root: false
status: active
priority: P1
area: '[[Trading]]'
parent: '[[Echo — I+D de Estrategias]]'
start: '2026-10-27'
progress: 0
repo: xKoRx/echo
aliases:
  - Echo Futures I+D
  - Investigación continua Futures
tags:
  - kind/project
  - area/trading
  - project/echo-rnd
  - tech/futures
created: '2026-10-28'
updated: '2026-10-28'
related:
  - '[[Echo Futures]]'
  - '[[Echo I+D — Cobertura Futures]]'
---

# Echo I+D — Futures

## 🎯 Objetivo

Conducir la división Futures de [[Echo — I+D de Estrategias]]: descubrir, especificar, desarrollar mediante los owners técnicos, cualificar y evaluar estrategias que puedan pasar challenges y producir retiros funded con economía completa verificable.

Prioridad inmediata: **NQ**, aprovechando el trabajo existente y reduciendo incertidumbre útil para la futura salida a producción. La investigación no declara listo el runtime ni autoriza operaciones. La metodología admite otras familias, instrumentos y fuentes cuando el Owner amplíe el alcance.

## 📊 Estado actual

**2026-10-28 — FUT-R01 en curso: capital inicial confirmado y ficha de estrategia simplificada por el Owner; baseline/entrevista continúan, sin campaña nueva.**

- Existen motor, laboratorio, identidades, recibos y metodología técnica. [[Echo Futures — Optimización de Campañas]] sigue siendo planner de su entrega acotada y del laboratorio; no se duplica.
- [[30-resources/agents/skills/echo-retester-master/SKILL|echo-retester-master]] posee desarrollo/corrección y cualificación G0–G5. Se usa antes de desarrollar y antes de campañas.
- La matriz [[Echo I+D — Cobertura Futures]] contrasta las celdas con TG/FBC/ORB y MR01–MR10. Se incorporó MR10, ausente del mapa inicial, y se explicitó MR08 como reversión local dentro de un contexto tendencial. Son clasificaciones de reglas observadas; no prueban independencia, conformidad ni alpha.
- **Proveedor/programa actual: pendiente de decisión Owner.** E2T/GAU50 es escenario histórico versionado. El Owner aclaró que esas cuentas ya no sirven y nunca fueron operadas.
- **ClutiFX: histórico, excluido de nuevas investigaciones por decisión expresa del Owner.** Último estado consultado: [[10-projects/Echo Futures/artifacts/clutifx-strategy-research/e05r1/CLF-E05R1-STATUS|E05R1]], en REVIEW, sin elegibles G5. Conservar aprendizajes y descartes; reabrir sólo por nueva decisión expresa. K05/E05R1 superseden partes de Q04.
- Datos NQ y capacidad física deben revalidarse cuando se despache ejecución. La organización actual no prueba disponibilidad on-host.

`progress: 0` corresponde al arranque de esta línea, no a la investigación total ni al avance de sus componentes históricos.

## 🧱 Entrega de desarrollo

_No aplica a este planner de investigación. El trabajo Go, fixtures ejecutables, cambios del Backtester o configuración ejecutable se prepara y ejecuta en Hefesto dentro del proyecto técnico autorizado, con branch/base y SPECs. La gestión Cloud puede leer y discutir evidencia, pero no simula una certificación física._

## 🧩 Iniciativas y autoridades

| Trabajo | Autoridad y relación |
|---|---|
| Laboratorio y búsqueda acotada de geometría/MM | [[Echo Futures — Optimización de Campañas]], subproyecto de esta línea. Sus objetivos históricos de cinco candidatas/25% pertenecen a ese encargo; no son cuotas universales del programa. |
| TG/FBC/ORB/MR y campañas anteriores | [[TRADESGERARD-CONTROL]] y catálogo/recibos del lab; evidencia existente que debe mapearse a celdas, no reejecutarse por defecto. |
| ClutiFX | [[CLUTIFX-STRATEGIES-MASTER]], biblioteca MKE, K05 y E05R1; conocimiento histórico. No desarrollar ni investigar de nuevo salvo decisión expresa del Owner. |
| Universo de props | [[Echo Futures — Futures Prop Universe]], resultado histórico de D1 y punto de partida para actualización first-party cuando corresponda. |
| Economía de ciclo completo | [[Echo Futures — Prop Economics Experiment]], evidencia histórica reutilizable; no autoridad del producto actual. |
| Producto y runtime | [[Echo Futures]], [[Echo Futures — Runtime Pools]] y owners técnicos: dependencias para integración/promoción, con sus gates propios. |

## Roadmap de la línea

| Tramo | Pregunta y salida | Condición de avance |
|---|---|---|
| **FUT-R01 — Baseline NQ, cobertura efectiva y mandato económico** | Qué existe realmente, qué se reutiliza, qué perfil actual evaluar y cuál es la siguiente investigación que aporta información. | Inventario por identidad/celda, vigencia de evidencia, alternativas y decisión Owner preparada. |
| Especificación del experimento elegido | Qué comportamiento esperamos y qué resultado lo refutaría; fuente, operacionalización y MM separados. | Spec determinista revisable, datos/versiones, presupuesto y autorización de ejecución. |
| Implementación y cualificación | ¿El código y las operaciones se comportan como la teoría operacionalizada? | G0–G4 propios según retester; corregir o bloquear donde falte evidencia. |
| Histórico y economía completa | ¿El candidato conserva utilidad después de selección/costes y en challenge/funded? | G5 sólo cuando corresponda; receipts de fase, sensibilidad y limitaciones; revisión Owner. |
| Adopción o cierre de investigación | ¿Continuar, corregir, aparcar, rechazar o proponer adopción? | Evidencia conservada, cobertura actualizada, próxima celda definida. La adopción se remite al owner runtime. |

Cada vuelta puede terminar antes del histórico si refuta una regla, demuestra duplicidad, falta de datos o incompatibilidad. No saltar G2C/G4 cambiando el nombre del trabajo a “research”. No optimizar reiteradamente sobre datos ya vistos como si fueran holdout.

## Primer trabajo: FUT-R01

**Estado:** IN_PROGRESS — recuperación documental y entrevista; no motores ni código de producto. **Responsable:** manager Futures con el Owner. **Celdas:** transversal a las celdas NQ de la matriz; habilita su selección sin pretender cubrirlas científicamente.

### Alcance

1. Recuperar los HEAD/branches, catálogos, recibos y datasets necesarios por lectura enfocada. Distinguir evidencia actual, superseded, incompleta y pendiente de aceptación.
2. Mapear TG/FBC/ORB/MR/ClutiFX a hipótesis, variantes, configuración y MM. FBC es NY FIRST CANDLE; no usar su nombre como evidencia de failed breakout.
3. Identificar duplicados de señal demostrados, solapamientos por investigar y huecos reales de mecanismo/contexto.
4. Preparar la selección del Provider/Program/RuleSet actual usando fuentes oficiales vigentes, restricciones de automatización/sesión y compatibilidad del simulador. No elegirlo por las antiguas cuentas E2T ni comprar cuentas.
5. Presentar un primer mandato candidato y una alternativa de mecanismo distinto, con hipótesis, refutador, evidencia previa, datos, coste de preparación, gates y presupuesto pendiente o autorizado.
6. Coordinar dependencia runtime y capacidad compartida sin reabrir sus implementaciones.

### Salida verificable

- Una tabla por identidad con fuente, celda, SHA/recibo, gates, estado económico y aceptación separados.
- Decisiones requeridas para un perfil comercial actual; desconocidos explícitos.
- Una recomendación de primera investigación y alternativa, sin candidatos falsamente validados.
- Mandato siguiente listo para aceptación del Owner y actualización de matriz/planner.

**No incluye:** ejecución Go, motores, adquisición de datos, mutación de cuentas, producción ni auditoría exhaustiva nueva de ClutiFX. Si falta una prueba física, emitir un encargo acotado y autorizado para Hefesto.

## Mandato económico y operativo del Owner — vigente al 2026-10-28

**Fuente:** instrucciones iniciales, primera ronda del 2026-10-27 y corrección del Owner del 2026-10-28; horario America/Santiago. Las metas son aspiraciones de negocio; no tasas estimadas ni resultados ya conseguidos.

| Decisión aceptada | Implicación y límite |
|---|---|
| Ampliar y mejorar el trading efectivo; convertir sistemas existentes en operación y retiros | El programa es permanente. La entrega de investigación debe cambiar decisiones y habilitar utilidad económica; no se mide por cantidad de sistemas o documentos. |
| Hito al 31-12-2026: Echo Futures funcionando de forma fiable, al menos cinco estrategias challenge y cinco funded produciendo retiros, en al menos dos prop firms simultáneamente | Meta táctica de operación, no compromiso de factibilidad demostrado. Falta acordar superposición 5+5 y criterio de repetición/sostenibilidad; una configuración o MM no suma otra estrategia. La preparación runtime pertenece a sus owners. |
| Sistema modular y escalable a más cuentas/props | Mantener Strategy, variante, configuración, MM y Provider/Program/RuleSet separados. Escalar exige economía de caja, límites comerciales y dependencia entre cuentas; no sólo multiplicar contratos o señales. |
| Aspiración de al menos una cuenta con retiro por cada diez compradas | El retiro debe ser dinero recibido. Horizonte, unidad exacta de compra/intento y tratamiento de resets siguen abiertos. Treinta cuentas no garantizan tres retiros; la dependencia afecta la dispersión y el riesgo de financiación. |
| Aspiración confirmada en su sentido general: pasar un challenge de cada tres y cobrar en una de cada tres —idealmente una de cada dos— funded activadas | Owner confirma el embudo explicado, manteniéndolo como ideal y exigiendo medición. Horizonte, resets y condiciones de activación se precisarán; 1/3 y 1/2 no son probabilidades observadas ni gates técnicos. |
| Capital inicial Futures USD 4.000, separado del bankroll Forex de aproximadamente USD 2.000; no más aportes previstos | USD 5.000 queda superseded. Capital disponible no es presupuesto autorizado para gasto total. No asumir reposición ni transferencias Forex. |
| Objetivo de primer retiro USD 3.000 con split de 90% u 80% | Pendiente aclarar si USD 3.000 es importe previo al split o dinero recibido tras él. Es objetivo Owner, no regla verificada de un programa comercial. |
| Elegir al menos dos props por sus condiciones para trading algorítmico; idealmente sin consistencia | Preferencia por ausencia de consistencia, no exclusión absoluta acordada. Comparar programa, tamaño, fase, plataforma y reglas actuales; no mezclar evaluation, simulated funded y live. |
| Sin preferencia de rescate entre estrategias; buscar 5+5 preferentemente descorrelacionadas | Priorizar evidencia reutilizable, coste de refutación y aporte a cartera. No convertir el antiguo top cinco del lab en una selección aceptada. |
| Disponibilidad Owner: lunes a domingo de 08:00 a 23:30 | Registrar como disponibilidad personal declarada. No equivale a presupuesto de jobs, throughput, capacidad libre ni acceso verificado a Hefesto/Daedalus. |
| Describir estrategias algorítmicas por indicadores mediante setup, filtro y RR u objetivo–riesgo técnico | El Owner sustituye la propuesta de descomposición extensa por una ficha simple y objetiva. Strategy sigue siendo entidad propia; MM asociado a prop/etapa es otra entidad. |
| Documentar y preparar investigación de familias, indicadores, métricas y RR sobre esa ficha simple | [[FUT-R01-RESEARCH-MANDATE]] v2 conserva rigor y gates en sus autoridades existentes. No autoriza motores, código de producto, cuentas ni cambios de MM ejecutable. |

**Capital resuelto:** USD 4.000 de bankroll inicial para Futures; aproximadamente USD 2.000 separados para Forex. No se prevén nuevos aportes. La cifra anterior de USD 5.000 no se usa en escenarios vigentes. La planificación debe respetar capital finito; antes de cualquier gasto, acordar reserva, pérdida máxima tolerada, desembolsos por etapas y condición de parada. Esos límites siguen pendientes, no se deducen del saldo ni se fijan unilateralmente. Ningún plan puede prometer ausencia de pérdidas.

**Primer retiro objetivo:** USD 3.000; split indicado 90% u 80%, pendiente de elegir programa y verificar condiciones. Si los USD 3.000 fueran previos al split, corresponderían USD 2.700 al 90% o USD 2.400 al 80%, antes de otros cargos aplicables. Si el objetivo es recibir USD 3.000 después del split, se requiere otro importe previo. No asumir una de las interpretaciones ni que cualquier prop permita ese primer payout.

### Convenciones de medición propuestas para decisión

- Identificar cohortes de compras/intentos y horizonte de observación. Separar compras nuevas, resets, renovaciones, pases, pérdidas y pendientes; todos los desembolsos entran al ledger. Una cuenta pendiente no desaparece del denominador.
- Registrar la cadena compra → pase → activación funded → elegibilidad → solicitud → aprobación → cobro efectivo → retiros repetidos/supervivencia. No equiparar elegibilidad, aprobación o PnL virtual con dinero recibido.
- Para el embudo confirmado como aspiración, usar `q = P(pase) × P(activación | pase) × P(primer cobro | activación)`, con cohortes y horizontes compatibles. No requiere independencia entre etapas. Con activación de todos los pases, 1/3 × 1/3 = 1/9 (11,1%) y 1/3 × 1/2 = 1/6 (16,7%); son aritmética de objetivos, no estimaciones del sistema.
- Medir cash neto y calendario: dinero cobrado después de reparto/transferencia menos compras, resets, renovaciones, activación y operación externos. Comisiones/slippage ya descontados del PnL que genera el retiro no se descuentan una segunda vez. El saldo nominal funded no forma parte del bankroll.
- Una tasa de cobro de 1/10 sólo es útil junto al importe cobrado, coste total, tiempo hasta cobro, liquidez comprometida y riesgo conjunto. Si cada cuenta tuviera una probabilidad marginal de cobro del 10% dentro de un horizonte definido, el número esperado entre treinta cuentas sería tres. Esa probabilidad no está estimada para el sistema y la expectativa no garantiza tres cobros, incluso con cuentas independientes. La dependencia cambia la dispersión y el riesgo de financiar pérdidas simultáneas.
- Para autosostenimiento, evaluar capacidad de financiar el siguiente lote y mantener la reserva acordada durante secuencias adversas, además de cash neto positivo. Diferenciar reinversión y dinero disponible para el Owner. No se ha fijado aún política de reserva/riesgo.

## Ficha simple de estrategia — decisión Owner

El Owner pidió partir de reglas algorítmicas objetivas basadas en indicadores. La ficha de investigación tiene tres bloques:

| Bloque de Strategy | Contenido |
|---|---|
| **Setup** | Condición exacta de entrada long/short: indicador(es), parámetros, timeframe y comparación/cruce/evento. La confirmación de entrada forma parte de esta regla; no exigir otro bloque de trigger. |
| **Filtro** | Condición booleana opcional que permite o bloquea el setup, con parámetros explícitos. Si no se usa, declarar ninguno. |
| **Objetivo y riesgo técnico / RR** | Definición determinista de SL y TP, o riesgo/distancia base más RR; expresar distancia en ATR o unidades de precio del instrumento. No confundir esta geometría con dinero arriesgado por cuenta. |

**MM es otra entidad, asociada a prop y etapa.** Traduce la señal/geometría al riesgo económico, sizing y controles de cuenta aplicables según sus contratos vigentes. Prop, etapa y reglas conservan identidad/versiones. Describir este modelo no modifica contratos, reparto de responsabilidades efectivo ni implementación.

Fuente, versión, datos, configuración, costes, ejecución, trazas y gates siguen formando parte de la evidencia de investigación y del laboratorio. No se convierten en doce componentes obligatorios de la ficha de estrategia ni en un nuevo framework. Completar sólo lo necesario para que setup/filtro/objetivo–riesgo sean inequívocos y contrastables.

## Baseline recuperado — evidencia existente, no promoción

El corte técnico consultado es `xKoRx/echo@ae1b09bc10370806f7648f076c5fa0825c9efa4e`, no una certificación del HEAD o binario actual de Hefesto. [R03-STATUS](https://github.com/xKoRx/echo/blob/ae1b09bc10370806f7648f076c5fa0825c9efa4e/v3/backtester/tools/tradesgerard/campaign-lab/correction/s04/lab-r03/R03-STATUS.md) registra 89/89 filas `COMPLETE_RECONCILED`, 3.037 compras y 328 pases simulados (10,8%) para el perfil histórico; mantiene `OWNER_ACCEPTANCE=REVIEW` y nunca LIVE. Estas cifras no describen cuentas operadas ni la probabilidad de pase de una cartera seleccionada bajo reglas comerciales nuevas.

[R03-DECISION-STRATEGIES](https://github.com/xKoRx/echo/blob/ae1b09bc10370806f7648f076c5fa0825c9efa4e/v3/backtester/tools/tradesgerard/campaign-lab/correction/s04/lab-r03/R03-DECISION-STRATEGIES.md) permite priorizar revisión de identidades, no aprobarlas:

| Identidad histórica representativa | Compras → pases simulados | Lectura vigente para FUT-R01 |
|---|---|---|
| `LAB-SG-MR-09-R750` | 13 → 5 | Resultado preliminar con muestra limitada; revisar reglas, trazas, selección temporal y economía bajo perfil actual. |
| `LAB-SG-FBC-CH300-15M-R750` | 43 → 11 | Evidencia reutilizable para investigación; no prueba de retiro ni de conformance actual. |
| `LAB-SG-MR-06-R750` | 5 → 2 | `EVIDENCE_LIMITED`; no elevar el 40% a estimación robusta. |
| FBC 60m y ORB 30m, perfiles SG R750 | 44 → 9 y 58 → 10 | Shortlist exploratoria por debajo del antiguo umbral del encargo; no completar cinco candidatas por cuota. |

El informe utiliza categorías y perfiles de una campaña; no acredita igual número de mecanismos independientes. Su confirmación 60/20/20 se declara `RETROSPECTIVE_TEMPORAL_CONFIRMATION`, no OOS virgen. La cobertura de días elegibles no demuestra descorrelación de pérdidas ni operación multipool. El agregado reutiliza resultados previos válidos y correcciones: no atribuir todas las filas a un único binario sin el receipt correspondiente. Conservar la evidencia existente y completar sólo brechas materiales.

### Próximo paso preparado dentro de FUT-R01

[[FUT-R01-RESEARCH-MANDATE]] v2 usa la ficha simple aceptada: A) setups, filtros, objetivo/riesgo e indicadores; B) mapeo a familias/cobertura NQ; C) MM por prop/etapa, economía y cartera. Se reduce la descomposición propuesta a los tres bloques solicitados. El siguiente paso inmediato es describir lo existente con esa ficha y formular brechas concretas para la investigación. El prompt está preparado; no se considera ejecutado por haberlo escrito.

En paralelo lógico, completar el inventario de identidades/recibos reutilizables y preparar un retorno read-only de Hefesto sólo para datos físicos que falten: catálogo efectivo, versiones/builds, manifiestos, trazas/recibos existentes y capacidad compartida. Primero resolver disponibilidad y canal real; no inventar acceso. No lanzar replay, tests, backtests ni campañas con ese encargo. El WIP sigue siendo una pregunta primaria Futures: cerrar FUT-R01.

La salida será una primera hipótesis/experimento recomendado y una alternativa, con refutador, coste, dependencias y autorización necesaria; no un roadmap final prematuro ni una nueva lista indiscriminada de optimizaciones.

## Economía y evidencia

El objetivo es el recorrido **challenge → funded → retiro**, incluyendo supervivencia y costes. Registrar fase y modo efectivo; `CHALLENGE_PASSED` no demuestra retiro y una cuenta funded inicializada para estudio debe tener origen/supuestos explícitos.

Las métricas vigentes y los contratos viven en el lab y en el perfil versionado: todas las compras en el denominador, pases/pérdidas/pendientes separados, comisiones/slippage, fees/renovaciones, tiempo, sequías y sensibilidad. No reinterpretar los resultados históricos con reglas comerciales nuevas sin una nueva identidad de experimento.

Los perfiles Strategy, MM y Provider se mantienen separados. El resultado cambia si cambia uno de ellos; un candidato no hereda PASS ni rentabilidad de otra combinación. El gate trimestral es filtro de cómputo, no validación estadística suficiente. Un diagnóstico de imposibilidad con los trades observados no prueba imposibilidad universal de la fuente.

## ✅ Tareas

- [/] FUT-R01: reconciliar baseline, vigencia por identidad, cobertura NQ y decisiones económicas; entrevista y revisión documental iniciadas. #owner/me #type/research #area/trading
- [r] [[Echo Futures — Optimización de Campañas]] implementar y revisar el laboratorio por shots. Puente transferido desde Echo Futures, conservando REVIEW; no se acepta la entrega por la reorganización. #owner/me #type/supervision #area/echo
- [x] Confirmar capital inicial y separación por mercado: USD 4.000 Futures / aproximadamente USD 2.000 Forex, sin nuevos aportes previstos. #owner/me #type/research #area/trading
- [ ] Aclarar primer retiro USD 3.000 bruto/neto; fijar reserva, pérdida máxima, desembolsos por etapas, horizonte de cobro y sostenibilidad antes de compras. Conserva pendiente superposición 5+5 y perfil comercial/MM. #owner/me #type/research #area/trading
- [ ] Elegir el primer experimento y una siguiente pregunta de mecanismo diferente; luego despachar sólo el alcance autorizado. #owner/me #type/research #area/trading

Futures Prop Universe es una entrega histórica cerrada, normalizada de `complete` a `completed`; Prop Economics ya estaba cerrado. Enlazarlos no reactiva sus tareas ni equivale a certificar reglas actuales.

## 📆 Bitácora

- **2026-10-28 — corrección Owner** — Capital confirmado: USD 4.000 Futures y aproximadamente USD 2.000 Forex, separados, sin aportes adicionales previstos; USD 5.000 superseded. Embudo de pase/cobro confirmado como aspiración, no estimación. Primer retiro objetivo USD 3.000 con split 90%/80%, bruto/neto pendiente. Ficha Strategy simplificada a setup, filtro y RR/objetivo–riesgo técnico; MM por prop/etapa separado. Prompt v2 ajustado sin cambio de runtime ni relajación de gates. [[80-agents/journal/logs/2026-10-28-echo-futures-capital-simple-strategy|Registro de la corrección]].

- **2026-10-27 — primera ronda Owner** — Aceptados objetivo de trading efectivo, hito táctico 5 challenge + 5 funded retirando, mínimo dos props simultáneas, preferencia algorítmica/sin consistencia y disponibilidad personal amplia. Capital USD 4.000/5.000, asignación y denominadores permanecen abiertos. Revisados código y receipts existentes; MR10 incorporada a cobertura y MR08 reclasificada como híbrida. Prompt de investigación preparado y documentación autorizada; sin campañas, código de producto, promoción ni cierre de sesión. [[80-agents/journal/logs/2026-10-27-echo-futures-fut-r01-owner-mandate|Registro del cambio]].

- **2026-10-27** — Línea incorporada al programa único por mandato Owner. NQ inmediato, economía challenge+retiros, perfil comercial actual por seleccionar. Puente de Optimización transferido conservando REVIEW. Retester y runbook alineados con conformidad teoría→regla→código y sin excepciones de rareza que omitan G2C. No se ejecutaron campañas ni se aceptaron gates.

## 🧭 Decisiones y pendientes

Aceptadas: dos mercados dentro del mismo programa; Futures por Echo Backtester; NQ inmediato; prioridad económica challenge+funded; Owner decide lo material. La ampliación a otros instrumentos y SQX como generación adicional quedan aparcadas, sin ejecutar ni integrar.

**Confirmado el 2026-10-28:** capital Futures USD 4.000 y Forex aproximadamente USD 2.000 separados, sin aportes adicionales; ficha Strategy de tres bloques con MM por prop/etapa separado; sentido general del embudo como aspiración.

Pendientes: primer retiro USD 3.000 previo/posterior al split; reserva, pérdida máxima y desembolsos por etapas; detalle de intentos/resets y horizontes; sostenibilidad/reinversión; superposición 5+5; Provider/Program/RuleSet actual; primer experimento; riesgos/MM y capacidad física. ClutiFX está excluida de nuevas investigaciones por decisión vigente; no se vuelve a preguntar como prioridad de rescate. La taxonomía y el orden dentro de mecanismos siguen siendo propuestas, no una shortlist aceptada.

## 🔗 Docs / Links

- [[Echo — I+D de Estrategias]] · [[Echo I+D — Cobertura Futures]] · [[Echo I+D — Mapa de capacidades]].
- [[FUT-R01-RESEARCH-MANDATE]] — prompt maestro preparado, módulos acotados y retorno read-only de Hefesto.
- [[30-resources/agents/skills/echo-futures-research-manager/SKILL|Manager Futures]].
- [[30-resources/runbooks/echo-rnd-cycle-runbook|Ciclo de investigación y mejora]].
- [[30-resources/runbooks/echo-futures-strategy-qualification-runbook|Cualificación técnica Futures]].

## Entrada del próximo chat

> Actúa como manager Futures de Echo I+D. En una sesión nueva ejecuta el bootstrap de `xKoRx/agents-os`, branch `master`, vault `main/`, y carga `echo-futures-research-manager`. Lee el programa, esta nota y la matriz. Retoma **FUT-R01 en curso**: ya hubo primera entrevista y recuperación documental; no repitas preguntas resueltas. Conserva las metas 5 challenge + 5 funded con retiros y mínimo dos props simultáneas como objetivos, no logros. Capital ya confirmado: USD 4.000 Futures y aproximadamente USD 2.000 Forex separados, sin más aportes; no volver a preguntar 4k/5k ni asignación. Usa ficha Strategy simple de setup, filtro y objetivo/riesgo o RR; MM por prop/etapa es entidad aparte. Aclara sólo el bruto/neto del primer retiro objetivo USD 3.000 y los demás pendientes económicos registrados. Usa [[FUT-R01-RESEARCH-MANDATE]] v2 preparado y completa sólo brechas materiales del baseline. NQ exclusivo, ClutiFX histórico, E2T histórico, MM/RuleSet separados y gates G0–G5 vigentes. No motores, código de producto, compras, promoción ni cierre formal sin la autorización correspondiente.


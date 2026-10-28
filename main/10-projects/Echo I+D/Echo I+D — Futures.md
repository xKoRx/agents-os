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

**2026-10-28 — FUT-R01 en curso: DR-01, DR-03 y DR-04 recibidos con hallazgos materiales; DR-02 recibido PARCIAL sin certificación; RV-01 y consolidación pendientes. DR-03 completo: [[FUT-R01-DR-03-mecanismos-NQ-2026-10-28]]; ficha consultable: [[Echo Futures — DR-03 mecanismos NQ evidencia y cobertura]]. Sin ejecución ni cambios de producto.**

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

**Estado:** IN_PROGRESS — recuperación documental, mandato económico y preparación de investigación externa; no motores ni código de producto. **Responsable:** manager Futures con el Owner; submanager para consolidar los retornos del frente 2. **Celdas:** transversal a las celdas NQ de la matriz; habilita su selección sin pretender cubrirlas científicamente.

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

**Fuente:** instrucciones iniciales, primera ronda del 2026-10-27 y correcciones del Owner del 2026-10-28; horario America/Santiago. Las metas son aspiraciones de negocio; no tasas estimadas ni resultados ya conseguidos.

### Corrección económica: campañas prop, no cuenta propia convencional

El Owner aclara que la operativa buscada compra evaluaciones para resolverlas rápidamente —pase o pérdida— y obtener retiros funded mediante la asimetría entre desembolso real y cobro potencial. **Esperanza positiva por trade, profit factor mayor que uno, Sharpe positivo o preservar cada cuenta no son requisitos universales de admisión.** Riesgo alto y resolución rápida son políticas deliberadas a investigar con matemática y experimentos posteriores, no errores a corregir por defecto. Tampoco se declaran óptimos o rentables sin evidencia de campaña.

La unidad económica es señal × MM × RuleSet × campaña × caja. La referencia Owner **aproximadamente USD 400 por funded** debe contrastarse distinguiendo precio comercial, coste de la trayectoria que pasó y coste agregado de adquisición con fallos, resets, renovaciones y activaciones. No se adopta como precio oficial ni coste esperado verificado. La esperanza de cada trade es descriptiva; la decisión exige valorar cobros netos, costes, tiempos y capacidad de financiar intentos con USD 4.000, sin respaldo Forex. No imponer una reserva conservadora, riesgo bajo o duración indefinida de las funded como doctrina.

[[FUT-R01-RESEARCH-MANDATE]] v4 conserva el informe anterior como antecedente exploratorio con rectificaciones explícitas y cifras comerciales no certificadas. Define cuatro mandatos autocontenidos: DR-01 matemática de campañas/MM; DR-02 contratos y costes; DR-03 mecanismos/cobertura NQ; DR-04 indicadores/reglas/validación. Primero recomendado DR-01; los demás pueden investigar en paralelo con dependencias explícitas. RV-01 revisa independientemente los retornos y el submanager consolida; no hay votación de IAs ni ejecución ficticia. **DR-01 y DR-04 recibidos con hallazgos; DR-02 parcial; DR-03 recibido con hallazgos; RV-01 pendiente.** G0–G5 y el frente 1 mantienen sus autoridades.

| Decisión aceptada | Implicación y límite |
|---|---|
| Ampliar y mejorar el trading efectivo; convertir sistemas existentes en operación y retiros | El programa es permanente. La entrega de investigación debe cambiar decisiones y habilitar utilidad económica; no se mide por cantidad de sistemas o documentos. En Futures rige la corrección de campañas prop anterior. |
| Hito al 31-12-2026: Echo Futures funcionando de forma fiable, al menos cinco estrategias challenge y cinco funded produciendo retiros, en al menos dos prop firms simultáneamente | Meta táctica de operación, no compromiso de factibilidad demostrado. Superposición 5+5 confirmada: pueden coincidir, diferir o combinarse; cada función requiere su evidencia. Falta concretar repetición/sostenibilidad. Una configuración o MM no suma otra estrategia. La preparación runtime pertenece a sus owners. |
| Sistema modular y escalable a más cuentas/props | Mantener Strategy, variante, configuración, MM y Provider/Program/RuleSet separados. Escalar exige economía de caja, límites comerciales y dependencia entre cuentas; no sólo multiplicar contratos o señales. |
| Aspiración de al menos una cuenta con retiro por cada diez compradas | El retiro debe ser dinero recibido. Horizonte, unidad exacta de compra/intento y tratamiento de resets siguen abiertos. Treinta cuentas no garantizan tres retiros; la dependencia afecta la dispersión y el riesgo de financiación. |
| Aspiración confirmada en su sentido general: pasar un challenge de cada tres y cobrar en una de cada tres —idealmente una de cada dos— funded activadas | Owner confirma el embudo explicado, manteniéndolo como ideal y exigiendo medición. Horizonte, resets y condiciones de activación se precisarán; 1/3 y 1/2 no son probabilidades observadas ni gates técnicos. |
| Capital inicial Futures USD 4.000, separado del bankroll Forex de aproximadamente USD 2.000; no más aportes previstos | USD 5.000 queda superseded. Capital disponible no es presupuesto autorizado para gasto total. No asumir reposición ni transferencias Forex. |
| Objetivo de primer retiro USD 3.000 con split de 90% u 80% | Investigar ambos escenarios: importe previo al split y dinero recibido tras él, sin bloquear research. Es objetivo Owner, no regla verificada de un programa comercial. |
| Elegir al menos dos props por sus condiciones para trading algorítmico; idealmente sin consistencia | Preferencia por ausencia de consistencia, no exclusión absoluta acordada. Comparar programa, tamaño, fase, plataforma y reglas actuales; no mezclar evaluation, simulated funded y live. |
| Sin preferencia de rescate entre estrategias; buscar 5+5 preferentemente descorrelacionadas | Priorizar evidencia reutilizable, coste de refutación y aporte a cartera. No convertir el antiguo top cinco del lab en una selección aceptada. |
| Disponibilidad Owner: lunes a domingo de 08:00 a 23:30 | Registrar como disponibilidad personal declarada. No equivale a presupuesto de jobs, throughput, capacidad libre ni acceso verificado a Hefesto/Daedalus. |
| Describir estrategias algorítmicas por indicadores mediante setup, filtro y RR u objetivo–riesgo técnico | El Owner sustituye la propuesta de descomposición extensa por una ficha simple y objetiva. Strategy sigue siendo entidad propia; MM asociado a prop/etapa es otra entidad. |
| Documentar el informe exploratorio rectificado y preparar investigaciones ONE-SHOT separadas; luego consolidación del submanager | [[FUT-R01-RESEARCH-MANDATE]] v4 sustituye v3 para nuevos dispatches. No autoriza motores, código de producto, cuentas ni cambios de MM ejecutable. |

**Capital resuelto:** USD 4.000 de bankroll inicial para Futures; aproximadamente USD 2.000 separados para Forex. No se prevén nuevos aportes. La cifra anterior de USD 5.000 no se usa en escenarios vigentes. La planificación debe respetar capital finito; antes de cualquier gasto, acordar reserva si corresponde, pérdida máxima tolerada, desembolsos y condición de parada. Esos límites siguen pendientes, no se deducen del saldo ni se fijan unilateralmente. Ningún plan puede prometer ausencia de pérdidas.

**Primer retiro objetivo:** USD 3.000; split indicado 90% u 80%, pendiente de elegir programa y verificar condiciones. Si los USD 3.000 fueran previos al split, corresponderían USD 2.700 al 90% o USD 2.400 al 80%, antes de otros cargos aplicables. Si el objetivo es recibir USD 3.000 después del split, se requiere otro importe previo. No asumir una de las interpretaciones ni que cualquier prop permita ese primer payout.

### Convenciones de medición propuestas para decisión

- Identificar cohortes de compras/intentos y horizonte de observación. Separar compras nuevas, resets, renovaciones, pases, pérdidas y pendientes; todos los desembolsos entran al ledger. Una cuenta pendiente no desaparece del denominador.
- Registrar la cadena compra → pase → activación funded → elegibilidad → solicitud → aprobación → cobro efectivo → retiros repetidos o cierre/reemplazo. No equiparar elegibilidad, aprobación o PnL virtual con dinero recibido, ni supervivencia prolongada de cada cuenta con el objetivo de campaña.
- Para el embudo confirmado como aspiración, usar `q = P(pase) × P(activación | pase) × P(primer cobro | activación)`, con cohortes y horizontes compatibles. No requiere independencia entre etapas. Con activación de todos los pases, 1/3 × 1/3 = 1/9 (11,1%) y 1/3 × 1/2 = 1/6 (16,7%); son aritmética de objetivos, no estimaciones del sistema.
- Medir cash neto y calendario: dinero cobrado después de reparto/transferencia menos compras, resets, renovaciones, activación y operación externos. Comisiones/slippage ya descontados del PnL que genera el retiro no se descuentan una segunda vez. El saldo nominal funded no forma parte del bankroll.
- Una tasa de cobro de 1/10 sólo es útil junto al importe cobrado, coste total, tiempo hasta cobro, liquidez comprometida y riesgo conjunto. Si cada cuenta tuviera una probabilidad marginal de cobro del 10% dentro de un horizonte definido, el número esperado entre treinta cuentas sería tres. Esa probabilidad no está estimada para el sistema y la expectativa no garantiza tres cobros, incluso con cuentas independientes. La dependencia cambia la dispersión y el riesgo de financiar pérdidas simultáneas.
- Para autosostenimiento, evaluar capacidad de financiar el siguiente lote y mantener la reserva que el Owner eventualmente acuerde durante secuencias adversas, además de cash neto positivo. Diferenciar reinversión y dinero disponible para el Owner. No se ha fijado aún política de reserva/riesgo.

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

**Frente 2 — investigación:** [[FUT-R01-RESEARCH-MANDATE]] v4 contiene el informe exploratorio rectificado y cuatro prompts completos/autocontenidos: DR-01 matemática de campañas prop y MM; DR-02 contratos y costes actuales; DR-03 mecanismos y cobertura NQ; DR-04 indicadores, reglas y validación. RV-01 hace revisión independiente con los cuatro retornos; el submanager consolida después, no por mayoría. La IA externa estudia fuentes y contrasta su cápsula; el manager conserva recuperación interna y autoridad sobre Agents-OS. Primero recomendado DR-01; los otros pueden investigar en paralelo sin asumir resultados no recibidos. USD 3.000 bruto/neto se analizan como escenarios. Mandatos preparados, no ejecutados; no se han despachado agentes independientes ni recibido sus investigaciones. Las cifras y recomendaciones comerciales del antecedente no están certificadas para uso operativo.

**Frente 1 — integración:** por nueva instrucción Owner se avanza en planificación y diseño de convergencia del Backtester experimental con el modelo vigente del runtime. [[EF-BACKTEST-RUNTIME-INTEGRATION-PLAN]] pertenece a [[Echo Futures]] y reutiliza Runtime Pools/R6/GOD-05. Define composición compartida, módulos/config/MM, observaciones causales, pools y reproducción de sesiones. No reactiva S05 del antiguo laboratorio. El Owner informa pruebas PROD; el último receipt recuperado acredita DEV RO del 27-10, pendiente vincular evidencia posterior a entorno/binarios. El primer mandato técnico está preparado para recuperación read-only de Hefesto; no despachado ni ejecutado.

**Hallazgo económico del corte de código leído:** Platform contiene caja inicial USD 5.000, compras fijas y un modo research con financiación adicional; FUNDED_ONLY excluye adquisición. No acredita supervivencia con USD 4.000 ni dos props simultáneas. Conservar sus resultados históricos y versionar el nuevo experimento de caja finita; no reinterpretarlos ni repetirlos automáticamente. Fuentes y detalles en el plan de integración.

En paralelo lógico, completar el inventario de identidades/recibos reutilizables y preparar un retorno read-only de Hefesto sólo para datos físicos que falten: catálogo efectivo, versiones/builds, manifiestos, trazas/recibos existentes y capacidad compartida. Primero resolver disponibilidad y canal real; no inventar acceso. No lanzar replay, tests, backtests ni campañas con ese encargo. El WIP sigue siendo una pregunta primaria Futures: cerrar FUT-R01.

La salida será una primera hipótesis/experimento recomendado y una alternativa, con refutador, coste, dependencias y autorización necesaria; no un roadmap final prematuro ni una nueva lista indiscriminada de optimizaciones.

## Economía y evidencia

El objetivo es el recorrido **compra → challenge → funded → retiro(s)**, incluyendo costes, tiempos, fallos/reemplazos y financiación del siguiente intento. No maximizar por defecto la supervivencia de cada cuenta ni exigir expectativa positiva por trade. Registrar fase y modo efectivo; `CHALLENGE_PASSED` no demuestra retiro y una cuenta funded inicializada para estudio debe tener origen/supuestos explícitos.

Las métricas vigentes y los contratos viven en el lab y en el perfil versionado: todas las compras en el denominador, pases/pérdidas/pendientes separados, comisiones/slippage, fees/renovaciones, tiempo, sequías y sensibilidad. No reinterpretar los resultados históricos con reglas comerciales nuevas sin una nueva identidad de experimento.

Los perfiles Strategy, MM y Provider se mantienen separados. El resultado cambia si cambia uno de ellos; un candidato no hereda PASS ni rentabilidad de otra combinación. El gate trimestral es filtro de cómputo, no validación estadística suficiente. Un diagnóstico de imposibilidad con los trades observados no prueba imposibilidad universal de la fuente.

## ✅ Tareas

- [/] FUT-R01: reconciliar baseline, vigencia por identidad, cobertura NQ y decisiones económicas; entrevista y revisión documental iniciadas. #owner/me #type/research #area/trading
- [r] [[Echo Futures — Optimización de Campañas]] implementar y revisar el laboratorio por shots. Puente transferido desde Echo Futures, conservando REVIEW; no se acepta la entrega por la reorganización. #owner/me #type/supervision #area/echo
- [x] Confirmar capital inicial y separación por mercado: USD 4.000 Futures / aproximadamente USD 2.000 Forex, sin nuevos aportes previstos. #owner/me #type/research #area/trading
- [ ] Aclarar primer retiro USD 3.000 bruto/neto; fijar política de caja, pérdida máxima, desembolsos, horizonte de cobro y sostenibilidad antes de compras. Perfil comercial/MM sigue pendiente; superposición 5+5 ya confirmada. Investigar ambos escenarios bruto/neto mientras se decide. #owner/me #type/research #area/trading
- [x] Confirmar superposición 5+5: mismas estrategias, conjuntos distintos o mezcla; evidencia por función/combinación. #owner/me #type/research #area/trading
- [x] Persistir corrección Owner de campañas prop, informe exploratorio rectificado y cuatro mandatos DR separados más RV-01 en [[FUT-R01-RESEARCH-MANDATE]] v4; no exigir esperanza positiva por trade ni imponer riesgo conservador. #owner/me #type/research #area/trading
- [ ] Adjudicar DR-01–04 recibidos, completar RV-01 y consolidación del submanager; ninguna recepción acredita ejecución ni aceptación. #owner/me #type/research #area/trading
- [/] Coordinar el diseño de integración Backtester–runtime con [[Echo Futures]] mediante [[EF-BACKTEST-RUNTIME-INTEGRATION-PLAN]]; recuperación read-only de Hefesto preparada, sin ejecución. #owner/me #type/supervision #area/echo
- [ ] Elegir el primer experimento y una siguiente pregunta de mecanismo diferente; luego despachar sólo el alcance autorizado. #owner/me #type/research #area/trading

Futures Prop Universe es una entrega histórica cerrada, normalizada de `complete` a `completed`; Prop Economics ya estaba cerrado. Enlazarlos no reactiva sus tareas ni equivale a certificar reglas actuales.


- **DR-03 recibido (autodeclarado RESPONDIDO; RECEIVED_WITH_MATERIAL_FINDINGS):** [[FUT-R01-DR-03-mecanismos-NQ-2026-10-28]] conserva el retorno íntegro; [[Echo Futures — DR-03 mecanismos NQ evidencia y cobertura]] documenta errores y cobertura desconocida, requiere RV-01.
- **DR-04 recibido (autodeclarado RESPONDIDO; RECEIVED_WITH_MATERIAL_FINDINGS):** [[FUT-R01-DR-04-indicadores-reglas-validacion-NQ-2026-10-28]] conserva íntegro el retorno, con fallos de unidades, geometría, fills M1 y trazabilidad señalados para revisión adversarial; sin promoción ni ejecución.
- **DR-02 recibido (PARCIAL, sin certificación contractual):** [[FUT-R01-DR-02-contratos-prop-NQ-2026-10-28]] conserva la referencia y sus bloqueos; el submanager debe verificar reglas, costes, payouts, KYC y automatización antes de decisiones. No se autoriza compra ni operación.

## 📆 Bitácora

- **2026-10-28 — DR-03 recibido:** [[FUT-R01-DR-03-mecanismos-NQ-2026-10-28]] archivado íntegro y [[Echo Futures — DR-03 mecanismos NQ evidencia y cobertura]] indexado. Sin validar estrategias ni alterar gates. 
- **2026-10-28 — DR-04 recibido:** [[FUT-R01-DR-04-indicadores-reglas-validacion-NQ-2026-10-28]] archivado con transcripción completa y advertencia de inconsistencias; destinado al submanager/RV-01 sin modificar Strategy/MM, datos, G0–G5 ni runtime.

- **2026-10-28 — campañas prop y dispatch separado** — Owner corrige el marco: no gestionar una cuenta propia rentable por trade, sino resolver evaluaciones rápidamente y estudiar la asimetría coste/cobro mediante MM, contratos y campañas. Se preserva USD 400/funded como referencia no verificada de coste agregado. Informe anterior documentado como exploratorio y rectificado; mandatos DR-01–04 y RV-01 preparados en v4, no ejecutados. Continuidad actualizada, sin cambios de producto, gates, gasto ni cierre formal. [[80-agents/journal/logs/2026-10-28-echo-futures-research-runtime-plan|Registro consolidado, addendum de frente 2]].

- **2026-10-28 — dos frentes** — Owner confirma que 5+5 pueden coincidir o diferir, pide prompt completo del frente 2 y planificación/diseño de integración Backtester–runtime para reproducir sesiones con datos precisos. Prompt v3 autocontenido y diseño candidato preparados; fuentes/config/policies divergentes identificadas sin modificar producto ni declarar paridad. Se preserva la declaración Owner de pruebas PROD y se pide receipt actual. [[80-agents/journal/logs/2026-10-28-echo-futures-research-runtime-plan|Registro]].

- **2026-10-28 — corrección Owner** — Capital confirmado: USD 4.000 Futures y aproximadamente USD 2.000 Forex, separados, sin aportes adicionales previstos; USD 5.000 superseded. Embudo de pase/cobro confirmado como aspiración, no estimación. Primer retiro objetivo USD 3.000 con split 90%/80%, bruto/neto pendiente. Ficha Strategy simplificada a setup, filtro y RR/objetivo–riesgo técnico; MM por prop/etapa separado. Prompt v2 ajustado sin cambio de runtime ni relajación de gates. [[80-agents/journal/logs/2026-10-28-echo-futures-capital-simple-strategy|Registro de la corrección]].

- **2026-10-27 — primera ronda Owner** — Aceptados objetivo de trading efectivo, hito táctico 5 challenge + 5 funded retirando, mínimo dos props simultáneas, preferencia algorítmica/sin consistencia y disponibilidad personal amplia. Capital USD 4.000/5.000, asignación y denominadores permanecen abiertos. Revisados código y receipts existentes; MR10 incorporada a cobertura y MR08 reclasificada como híbrida. Prompt de investigación preparado y documentación autorizada; sin campañas, código de producto, promoción ni cierre de sesión. [[80-agents/journal/logs/2026-10-27-echo-futures-fut-r01-owner-mandate|Registro del cambio]].

- **2026-10-27** — Línea incorporada al programa único por mandato Owner. NQ inmediato, economía challenge+retiros, perfil comercial actual por seleccionar. Puente de Optimización transferido conservando REVIEW. Retester y runbook alineados con conformidad teoría→regla→código y sin excepciones de rareza que omitan G2C. No se ejecutaron campañas ni se aceptaron gates.

## 🧭 Decisiones y pendientes

Aceptadas: dos mercados dentro del mismo programa; Futures por Echo Backtester; NQ inmediato; prioridad económica challenge+funded; Owner decide lo material. La ampliación a otros instrumentos y SQX como generación adicional quedan aparcadas, sin ejecutar ni integrar.

**Confirmado el 2026-10-28:** capital Futures USD 4.000 y Forex aproximadamente USD 2.000 separados, sin aportes adicionales; ficha Strategy de tres bloques con MM por prop/etapa separado; sentido general del embudo como aspiración; superposición 5+5 libre (mismas, distintas o mezcla). Planificación/diseño del frente 1 autorizados. Para el frente 2 rige economía de campañas prop, sin expectativa positiva por trade como requisito universal y con políticas agresivas de resolución rápida dentro del espacio de investigación. Informe rectificado y cuatro DR separados más revisión preparados; consolidación posterior del submanager.

Pendientes: primer retiro USD 3.000 previo/posterior al split; política de caja, pérdida máxima y desembolsos; detalle de intentos/resets y horizontes; sostenibilidad/reinversión; Provider/Program/RuleSet actual; primer experimento; riesgos/MM y capacidad física. ClutiFX está excluida de nuevas investigaciones por decisión vigente; no se vuelve a preguntar como prioridad de rescate. La taxonomía y el orden dentro de mecanismos siguen siendo propuestas, no una shortlist aceptada.

## 🔗 Docs / Links

- [[Echo — I+D de Estrategias]] · [[Echo I+D — Cobertura Futures]] · [[Echo I+D — Mapa de capacidades]].
- [[FUT-R01-RESEARCH-MANDATE]] — v4: mandatos DR-01–04 y revisión RV-01. DR-01 recibido con hallazgos; DR-02 recibido parcial; DR-04 recibido con hallazgos ([[FUT-R01-DR-04-indicadores-reglas-validacion-NQ-2026-10-28]]). DR-03 recibido con hallazgos; RV-01 pendiente. El mandato v4 se conserva como fuente histórica de dispatch.
- [[EF-BACKTEST-RUNTIME-INTEGRATION-PLAN]] — diseño candidato del frente 1 bajo Echo Futures; paridad, ramas/contratos, hitos y mandato read-only de Hefesto.
- [[30-resources/agents/skills/echo-futures-research-manager/SKILL|Manager Futures]].
- [[30-resources/runbooks/echo-rnd-cycle-runbook|Ciclo de investigación y mejora]].
- [[30-resources/runbooks/echo-futures-strategy-qualification-runbook|Cualificación técnica Futures]].

## Entrada del próximo chat

> Actúa como manager Futures de Echo I+D. En una sesión nueva ejecuta el bootstrap de `xKoRx/agents-os`, branch `master`, vault `main/`, y carga `echo-futures-research-manager`. Lee el programa, esta nota y la matriz. Retoma **FUT-R01 en curso**: no repitas preguntas resueltas. Conserva las metas 5 challenge + 5 funded con retiros y mínimo dos props simultáneas como objetivos, no logros. Capital ya confirmado: USD 4.000 Futures y aproximadamente USD 2.000 Forex separados, sin más aportes. **Marco económico Owner: campañas prop, no rentabilidad de una cuenta propia; no exigir esperanza positiva por trade ni preservar cada evaluación. Estudiar políticas agresivas y resolución rápida bajo contratos, caja finita y matemática. USD 400/funded es referencia a contrastar con adquisición agregada.** Usa Strategy de setup, filtro y objetivo/riesgo o RR; MM por prop/etapa separado. Superposición 5+5 libre. Analiza USD 3.000 bruto/neto sin bloquear research. [[FUT-R01-RESEARCH-MANDATE]] v4 contiene el informe exploratorio rectificado y DR-01–04 autocontenidos más RV-01; DR-01 ya fue recibido con hallazgos materiales; DR-02 y DR-04 ya recibidos sin certificación; DR-03 recibido con hallazgos; RV-01 pendiente. Recibir los demás retornos, revisión independiente y consolidación del submanager sin votación ni inventar dispatches. Las cifras comerciales del antecedente no están certificadas. Para el frente 1 continúa [[EF-BACKTEST-RUNTIME-INTEGRATION-PLAN]] bajo su autoridad vigente; este delta no cambia su estado ni autoriza ejecución. NQ exclusivo, ClutiFX histórico, E2T histórico, MM/RuleSet separados y G0–G5 vigentes. No motores, código de producto, compras, promoción ni cierre formal sin autorización correspondiente.

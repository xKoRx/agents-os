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

**Actualización Owner posterior — 2026-10-28: integración en curso y nuevo frente C.** El Owner informa que S04 completa y sus variantes se están integrando en master; esto supersede PAUSED_OWNER, sin certificar merge, build, aceptación ni despliegue. A/B quedan pendientes de retorno. [[FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION]] incorpora tres capacidades requeridas del Backtester: CHALLENGE y FUNDED aisladas/comparables, seguidas de SIMULATION causal con caja común. El Backtester es responsabilidad funcional de esta línea: sus carencias necesarias se convierten en desarrollo priorizado mediante los owners técnicos existentes.

**Decisiones económicas ya resueltas:** USD 4.000 son caja para comprar challenges, no equity propia de trading; NQ exclusivo y Forex separado. Retiro sin objetivo fijo de USD 3.000: se evalúa importe/momento/política. Challenge busca pase o pérdida rápidos dentro de todas las reglas aplicables, sin caps prudenciales extra impuestos por defecto; 1/3 es umbral Owner para futuras campañas. Todo cash neto recibido se reinvierte. Una media positiva no certifica escalabilidad infinita ni autoriza compras. Diseño C01 y coordinación técnica preparados; no ejecutados por esta actualización.

**2026-10-28 — RV-01 y consolidado documental entregados: `NO_APTO_AUN`.** Expediente único: [[FUT-R01-INDICE]]; dictamen, reparación focal y siguiente propuesta: [[FUT-R01-RV-01-CONSOLIDADO]]. DR-01 sólo está disponible como captura editorial; DR-02 sigue PARCIAL; DR-03/04 están preservados completos según su ingestión. La independencia histórica de autoría no es acreditable: la entrega se clasifica como **AUTORREVISIÓN ADVERSARIAL DOCUMENTAL**. FUT-R01 sigue en curso por dependencias de entradas, contrato, datos y selección. Sesión documental cerrada con feedback; no hay aceptación Owner, ejecución ni cambios de producto o G0–G5.

- Existen motor, laboratorio, identidades, recibos y metodología técnica. [[Echo Futures — Optimización de Campañas]] sigue siendo planner de su entrega acotada y del laboratorio; no se duplica.
- [[30-resources/agents/skills/echo-retester-master/SKILL|echo-retester-master]] posee desarrollo/corrección y cualificación G0–G5. Se usa antes de desarrollar y antes de campañas.
- La matriz [[Echo I+D — Cobertura Futures]] contrasta las celdas con TG/FBC/ORB y MR01–MR10. Se incorporó MR10, ausente del mapa inicial, y se explicitó MR08 como reversión local dentro de un contexto tendencial. Son clasificaciones de reglas observadas; no prueban independencia, conformidad ni alpha.
- **Proveedor/programa actual: pendiente de decisión Owner.** E2T/GAU50 es escenario histórico versionado. El Owner aclaró que esas cuentas ya no sirven y nunca fueron operadas.
- **ClutiFX: histórico, excluido de nuevas investigaciones por decisión expresa del Owner.** Último estado consultado: [[10-projects/Echo Futures/artifacts/clutifx-strategy-research/e05r1/CLF-E05R1-STATUS|E05R1]], en REVIEW, sin elegibles G5. Conservar aprendizajes y descartes; reabrir sólo por nueva decisión expresa. K05/E05R1 superseden partes de Q04.
- Datos NQ y capacidad física deben revalidarse cuando se despache ejecución. La organización actual no prueba disponibilidad on-host.

`progress: 0` corresponde al arranque de esta línea, no a la investigación total ni al avance de sus componentes históricos.

## 🧱 Entrega de desarrollo

_Este planner es dueño de prioridades, requisitos funcionales y aceptación económica de las capacidades de Backtester necesarias para I+D. No contiene el código ni duplica el planner técnico: Go, fixtures, configuración y cambios del motor se entregan mediante [[Echo Futures — Optimización de Campañas]], con branch/base, SPECs y permisos vigentes. Una capacidad ausente se planifica como desarrollo; no se usa como motivo para abandonar la pregunta de investigación. Los owners de producto/runtime conservan arquitectura y gates físicos._

## 🧩 Iniciativas y autoridades

| Trabajo | Autoridad y relación |
|---|---|
| Laboratorio y búsqueda acotada de geometría/MM | [[Echo Futures — Optimización de Campañas]], subproyecto de esta línea. Sus objetivos históricos de cinco candidatas/25% se conservan con sus recibos. El umbral Owner para nuevas campañas challenge es 1/3; no se reetiquetan selecciones históricas. |
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

**Estado:** IN_PROGRESS — revisión RV-01 y consolidado terminados; selección del experimento pendiente por dependencias explícitas. **Responsable:** manager Futures con el Owner. **Celdas:** transversal a las celdas NQ de la matriz; habilita su selección sin pretender cubrirlas científicamente. Ver [[FUT-R01-INDICE]] para el expediente reunido.

### Alcance

1. Recuperar los HEAD/branches, catálogos, recibos y datasets necesarios por lectura enfocada. Distinguir evidencia actual, superseded, incompleta y pendiente de aceptación.
2. Mapear TG/FBC/ORB/MR/ClutiFX a hipótesis, variantes, configuración y MM. FBC es NY FIRST CANDLE; no usar su nombre como evidencia de failed breakout.
3. Identificar duplicados de señal demostrados, solapamientos por investigar y huecos reales de mecanismo/contexto.
4. Preparar la selección del Provider/Program/RuleSet actual usando fuentes oficiales vigentes, restricciones de automatización/sesión y compatibilidad del simulador. No elegirlo por las antiguas cuentas E2T ni comprar cuentas.
5. Presentar un primer mandato candidato y una alternativa de mecanismo distinto, con hipótesis, refutador, evidencia previa, datos, coste de preparación, gates y presupuesto pendiente o autorizado.
6. Coordinar la integración S04 y el desarrollo incremental de CHALLENGE/FUNDED/SIMULATION como capacidad de I+D, sin duplicar el trabajo activo ni modificar producto desde este planner.

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

[[FUT-R01-RESEARCH-MANDATE]] v4 conserva el informe anterior, la corrección Owner y las cápsulas DR-01–04/RV-01 como fuente histórica; sus encabezados de recepción no son el estado vigente. [[FUT-R01-RV-01-CONSOLIDADO]] adjudica el material efectivamente disponible con `NO_APTO_AUN` y una reparación focal. No certifica cuatro originales completos ni independencia histórica. Las aspiraciones económicas permanecen hipótesis; G0–G5 y el frente 1 mantienen sus autoridades.

| Decisión aceptada | Implicación y límite |
|---|---|
| Ampliar y mejorar el trading efectivo; convertir sistemas existentes en operación y retiros | El programa es permanente. La entrega de investigación debe cambiar decisiones y habilitar utilidad económica; no se mide por cantidad de sistemas o documentos. En Futures rige la corrección de campañas prop anterior. |
| Hito al 31-12-2026: Echo Futures funcionando de forma fiable, al menos cinco estrategias challenge y cinco funded produciendo retiros, en al menos dos prop firms simultáneamente | Meta táctica de operación, no compromiso de factibilidad demostrado. Superposición 5+5 confirmada: pueden coincidir, diferir o combinarse; cada función requiere su evidencia. Falta concretar repetición/sostenibilidad. Una configuración o MM no suma otra estrategia. La preparación runtime pertenece a sus owners. |
| Sistema modular y escalable a más cuentas/props | Mantener Strategy, variante, configuración, MM y Provider/Program/RuleSet separados. Escalar exige economía de caja, límites comerciales y dependencia entre cuentas; no sólo multiplicar contratos o señales. |
| Aspiración de al menos una cuenta con retiro por cada diez compradas | El retiro debe ser dinero recibido. Horizonte, unidad exacta de compra/intento y tratamiento de resets siguen abiertos. Treinta cuentas no garantizan tres retiros; la dependencia afecta la dispersión y el riesgo de financiación. |
| Challenge: umbral Owner 1/3 para las campañas nuevas; por encima se busca mejorar | Supersede el piso histórico 1/4 para trabajos futuros. No es promedio de mercado, probabilidad observada ni gate técnico. Antes de adjudicar se fijan unidad compra/cuenta/intento, resets y horizonte; se reportan ambas vistas sin escoger el denominador favorable. Las aspiraciones previas de cobrar en 1/3–1/2 funded siguen referencias; ahora se mide también importe medio neto por TODAS las funded iniciadas. |
| USD 4.000 son bankroll para comprar challenges; Forex aproximadamente USD 2.000 separado; sin aportes | No son saldo/equity de futuros propios ni tamaño nominal de cuentas prop. USD 5.000 queda histórico. El modelo puede estudiar agotamiento de la caja; ello no autoriza compras reales. Los cargos obligatorios requieren fuente identificada, sin fondos inventados. |
| El importe y el momento del retiro se determinan por resultados de campañas/simulaciones | USD 3.000 como objetivo fijo queda superseded. Se selecciona la mejor política dentro del espacio/horizonte evaluados y se valida temporalmente; split, mínimos, máximos, buffers y demora vienen del RuleSet. No fijar 500/2.000/5.000 por tomar literalmente ejemplos Owner. |
| MM: pasar o quemar rápido dentro del máximo permitido por reglas | No imponer un límite adicional prudencial de lotes/riesgo/pérdida acumulada. Respetar prop, broker, mercado y controles técnicos. El sizing exacto requiere propuesta/evidencia; no modificar la geometría de Strategy para rellenar riesgo. |
| Reinvierte el 100% de lo efectivamente cobrado | Sólo cash neto recibido aumenta bankroll disponible; solicitud/aprobación y PnL nominal no financian compras. No exigir reserva o retiro personal como decisión aún pendiente. |
| Campañas CHALLENGE y FUNDED primero; SIMULATION integral después | Misma Strategy puede evaluarse en ambas etapas con MM/ledger propios. Simulation encadena financiación real y después varias estrategias/pools/props. Concurrencia lógica no equivale a capacidad física ni cambia R6 implícitamente. |
| Elegir al menos dos props por sus condiciones para trading algorítmico; idealmente sin consistencia | Preferencia por ausencia de consistencia, no exclusión absoluta acordada. Comparar programa, tamaño, fase, plataforma y reglas actuales; no mezclar evaluation, simulated funded y live. |
| Sin preferencia de rescate entre estrategias; buscar 5+5 preferentemente descorrelacionadas | Priorizar evidencia reutilizable, coste de refutación y aporte a cartera. No convertir el antiguo top cinco del lab en una selección aceptada. |
| Disponibilidad Owner: lunes a domingo de 08:00 a 23:30 | Registrar como disponibilidad personal declarada. No equivale a presupuesto de jobs, throughput, capacidad libre ni acceso verificado a Hefesto/Daedalus. |
| Describir estrategias algorítmicas por indicadores mediante setup, filtro y RR u objetivo–riesgo técnico | El Owner sustituye la propuesta de descomposición extensa por una ficha simple y objetiva. Strategy sigue siendo entidad propia; MM asociado a prop/etapa es otra entidad. |
| Documentar el informe exploratorio rectificado y preparar investigaciones ONE-SHOT separadas; luego consolidación del submanager | [[FUT-R01-RESEARCH-MANDATE]] v4 sustituye v3 para nuevos dispatches. No autoriza motores, código de producto, cuentas ni cambios de MM ejecutable. |

**Capital y agresividad resueltos:** USD 4.000 de compras Futures; Forex separado, sin nuevos aportes. El Owner no desea caps prudenciales adicionales ni reserva impuesta por defecto: investigar resolución rápida y toda la pérdida comercial posible de los escenarios dentro de reglas. Una pérdida nominal de una funded no se vuelve a descontar del bankroll comercial. No confundir este marco de simulación con permiso de gastar, infringir reglas o retirar guardas técnicas.

**Retiro y reinversión resueltos:** el target fijo USD 3.000 queda superseded; buscar importe/momento/política que mejore la economía de campaña, incluido tiempo y efecto sobre posteriores cobros. Reinvierte el 100% del cash neto recibido. Horizonte, conjunto finito de políticas y criterio de selección deben quedar fijados antes de evaluación, sin llamar óptimo universal al máximo retrospectivo.

### Convenciones de medición propuestas para decisión

- Identificar cohortes de compras/cuentas e intentos y horizonte de observación. Separar compras nuevas, resets pagados/gratuitos, renovaciones, pases, pérdidas y pendientes; vincular intentos a la unidad comercial sin duplicar éxitos. Reportar ambas tasas; fijar unidad del 1/3 y tratamiento de resets antes de adjudicar. Todos los desembolsos entran al ledger. Una cuenta pendiente no desaparece del denominador.
- Registrar la cadena compra → pase → activación funded → elegibilidad → solicitud → aprobación → cobro efectivo → retiros repetidos o cierre/reemplazo. No equiparar elegibilidad, aprobación o PnL virtual con dinero recibido, ni supervivencia prolongada de cada cuenta con el objetivo de campaña.
- Para el embudo confirmado como aspiración, usar `q = P(pase) × P(activación | pase) × P(primer cobro | activación)`, con cohortes y horizontes compatibles. No requiere independencia entre etapas. Con activación de todos los pases, 1/3 × 1/3 = 1/9 (11,1%) y 1/3 × 1/2 = 1/6 (16,7%); son aritmética de objetivos, no estimaciones del sistema.
- Medir cash neto y calendario: dinero cobrado después de reparto/transferencia menos desembolsos externos una sola vez. En la combinación de etapas, adquisición incluye compras, resets/renovaciones de evaluación y activación; costes operativos funded excluyen esos cargos. Comisiones/slippage/cargos ya descontados del PnL o cash no se descuentan otra vez. El saldo nominal funded no forma parte del bankroll.
- Una tasa de cobro de 1/10 sólo es útil junto al importe cobrado, coste total, tiempo hasta cobro, liquidez comprometida y riesgo conjunto. Si cada cuenta tuviera una probabilidad marginal de cobro del 10% dentro de un horizonte definido, el número esperado entre treinta cuentas sería tres. Esa probabilidad no está estimada para el sistema y la expectativa no garantiza tres cobros, incluso con cuentas independientes. La dependencia cambia la dispersión y el riesgo de financiar pérdidas simultáneas.
- Para autosostenimiento, medir capacidad de financiar nuevos intentos, secuencias adversas, demoras y agotamiento con caja finita y reinversión del 100%. No imponer reserva no solicitada ni confundir media positiva con escala infinita. [[FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION]] fija el requerimiento y propone KPI/cohortes/casos para revisión.

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

**A/B:** [[FUT-R01-ITERACION-01]] conserva la ficha candidata PERSIST/cierre y la reparación contractual. El Owner retornará los resultados; no han sido recibidos ni aceptados aquí. B debe incorporar el delta de retiro variable, reinversión total, 1/3 y tipos de campaña, sin reiniciar investigación. MR06 sigue alternativa existente.

**Frente 1:** IN_PROGRESS_OWNER_REPORTED. El Owner informa integración S04 completa/variantes a master. Se retira la pausa anterior y se coordina con su manager/ejecutor actual; no se duplica ni se interviene el merge. [[EF-BACKTEST-RUNTIME-INTEGRATION-PLAN]] permanece antecedente que debe reconciliarse contra el corte aceptado y receipts de esa integración.

**Frente C:** [[FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION]] es el mandato funcional de los nuevos tipos. C01 GOD Cloud prepara diseño/KPI/delta mientras avanza S04; el manager técnico existente conduce su entrega. No crea otra fábrica ni autoriza backtests. El antiguo I01-C sólo era recuperación de datos y no debe confundirse con este frente.

**RV-01 se conserva:** NO_APTO_AUN para campaña definida/reproducible; integridad limitada, contrato/ruta/costes y observabilidad pendientes. No repetir DR-01–04 ni abrir DR-05. El nuevo requerimiento no acredita esos pendientes ni presupone rentabilidad.

### Cola priorizada de investigación y reutilización

Una pregunta primaria de investigación Futures; varios workers independientes y el desarrollo habilitante pueden avanzar coordinados. La capacidad de ejecutar etapas/múltiples estrategias no elimina admisión, presupuesto ni límites de Hefesto. El detalle técnico vive sólo en el planner del lab.

| Orden / estado | Resultado buscado | Dependencia / aceptación / responsable |
|---|---|---|
| 1 — WAITING_RETURN | Recibir y adjudicar I01-A/B; incorporar delta económico | Manager Futures + Owner; preservar trabajo válido, no reabrir los DR ni esperar toda la fábrica para revisar la señal/perfil |
| 2 — AHORA, DISEÑO PREPARADO | C01: contratos/KPI, reutilización y primer incremento challenge/funded/simulation | GOD Cloud ONE-SHOT; diseño candidato con estados, caja, admisión y casos; no implementación ni autoaceptación |
| 3 — EN CURSO INFORMADO POR OWNER | Reconciliar integración S04/variantes a master | Manager técnico existente; commit exacto, matriz de variantes, source/build/tests/aceptación separados. No declarar merge terminado por el reporte |
| 4 — DESPUÉS DE DISEÑO/BASE ACEPTADOS | CHALLENGE y FUNDED aisladas; solicitud dual para una Strategy | Planner lab, ejecutor técnico autorizado; MM/RuleSet/cohortes/ledger propios, KPI reconciliados. Resolver expresamente admisión funded-only frente a G4 |
| 5 — SIGUIENTE CAPACIDAD | SIMULATION causal 1×1; luego varias estrategias/pools y dos props con caja común | Reutilizar etapas/Platform; compras, activaciones, cobros y reinversión con USD 4.000. Sin caja ficticia ni resultados IID por duplicar cuentas |
| 6 — HANDOFF DE INVESTIGACIÓN | Primera nueva Strategy o refactor seleccionado, datos y cualificación | A/B adjudicados, evidencia necesaria disponible, mandato/budget/gates. Recuperación I01-C read-only sólo si falta evidencia; no nuevo preflight por inercia |
| 7 — ALTERNATIVA / RESERVA | Reconciliar MR06 o una pregunta incremental dentro de la celda | Activación por decisión/aprendizaje, una hipótesis y refutador. Nada de parrilla cartesiana ni nueva familia por otro MM |

Reutilizar preparación causal, datos, perfiles, contratos, fixtures y recibos válidos; invalidar sólo lo dependiente de cambios semánticos. Las nuevas capacidades son trabajo de I+D habilitante, no cobertura adicional de mecanismos ni estrategias. No bloquear análisis A/B por dependencias técnicas que no cambien su decisión.

## Economía y evidencia

El objetivo es el recorrido **compra → challenge → funded → retiro(s)**, incluyendo costes, tiempos, fallos/reemplazos y financiación del siguiente intento. No maximizar por defecto la supervivencia de cada cuenta ni exigir expectativa positiva por trade. Registrar fase y modo efectivo; `CHALLENGE_PASSED` no demuestra retiro y una cuenta funded inicializada para estudio debe tener origen/supuestos explícitos.

Las métricas vigentes y los contratos viven en el lab y en el perfil versionado: todas las compras en el denominador, pases/pérdidas/pendientes separados, comisiones/slippage, fees/renovaciones, tiempo, sequías y sensibilidad. No reinterpretar los resultados históricos con reglas comerciales nuevas sin una nueva identidad de experimento.

Los perfiles Strategy, MM y Provider se mantienen separados. El resultado cambia si cambia uno de ellos; un candidato no hereda PASS ni rentabilidad de otra combinación. El gate trimestral es filtro de cómputo, no validación estadística suficiente. Un diagnóstico de imposibilidad con los trades observados no prueba imposibilidad universal de la fuente.

## ✅ Tareas

- [/] FUT-R01: reconciliar baseline, vigencia por identidad, cobertura NQ y decisiones económicas; entrevista y revisión documental iniciadas. #owner/me #type/research #area/trading
- [r] [[Echo Futures — Optimización de Campañas]] implementar y revisar el laboratorio por shots. Puente transferido desde Echo Futures, conservando REVIEW; no se acepta la entrega por la reorganización. #owner/me #type/supervision #area/echo
- [x] Confirmar capital inicial y separación por mercado: USD 4.000 Futures / aproximadamente USD 2.000 Forex, sin nuevos aportes previstos. #owner/me #type/research #area/trading
- [x] Resolver economía Owner: USD 4.000 para comprar challenges, retiro variable, reinversión total y MM de resolución rápida dentro de reglas, sin caps prudenciales impuestos. 1/3 es umbral para campañas futuras; no son permisos de gasto. #owner/me #type/research #area/trading
- [ ] Fijar para el primer experimento Provider/Program/RuleSet, horizonte/seguimiento, políticas finitas de MM/retiro/compra, costes y financiación explícita de cargos obligatorios. #owner/me #type/research #area/trading
- [x] Confirmar superposición 5+5: mismas estrategias, conjuntos distintos o mezcla; evidencia por función/combinación. #owner/me #type/research #area/trading
- [x] Persistir corrección Owner de campañas prop, informe exploratorio rectificado y cuatro mandatos DR separados más RV-01 en [[FUT-R01-RESEARCH-MANDATE]] v4; no exigir esperanza positiva por trade ni imponer riesgo conservador. #owner/me #type/research #area/trading
- [x] Entregar RV-01 y consolidado de lo disponible, con reparación focal, fuentes críticas y dictamen `NO_APTO_AUN`; reunir los originales disponibles sin alterar sus bytes en [[FUT-R01-INDICE]]. Entrega documental no equivale a aceptación ni ejecución. #owner/me #type/research #area/trading
- [/] Preparar y adjudicar [[FUT-R01-ITERACION-01]]: ficha causal A y contrato/caja B, preservando las dependencias de RV-01. Prompts preparados; retornos A/B aún no recibidos. No repetir los cuatro DR ni reconstruir originales ausentes. #owner/me #type/research #area/trading
- [/] Coordinar el frente C y la integración S04 informada por Owner mediante el planner técnico existente: [[FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION]]. Reconciliar evidencia antes de nuevos despachos; no duplicar merge ni certificarlo. #owner/me #type/supervision #area/echo
- [ ] Elegir el primer experimento y una siguiente pregunta de mecanismo diferente; luego despachar sólo el alcance autorizado. #owner/me #type/research #area/trading

Futures Prop Universe es una entrega histórica cerrada, normalizada de `complete` a `completed`; Prop Economics ya estaba cerrado. Enlazarlos no reactiva sus tareas ni equivale a certificar reglas actuales.


- **DR-03 recibido (autodeclarado RESPONDIDO; RECEIVED_WITH_MATERIAL_FINDINGS):** [[FUT-R01-DR-03-mecanismos-NQ-2026-10-28]] conserva el retorno íntegro según ingestión; [[Echo Futures — DR-03 mecanismos NQ evidencia y cobertura]] enlaza su adjudicación en RV-01. Sin aceptación ni cualificación.
- **DR-04 recibido (autodeclarado RESPONDIDO; RECEIVED_WITH_MATERIAL_FINDINGS):** [[FUT-R01-DR-04-indicadores-reglas-validacion-NQ-2026-10-28]] conserva el retorno; errores de unidades, geometría, fills M1 y selección adjudicados en [[FUT-R01-RV-01-CONSOLIDADO]]. Sus fichas no son specs aceptadas.
- **DR-02 recibido (PARCIAL, sin certificación contractual):** [[FUT-R01-DR-02-contratos-prop-NQ-2026-10-28]] conserva 38 líneas sin URLs. RV-01 verifica sólo fuentes decisivas y corrige Rapid/caps/origen de órdenes; el vector completo por programa/fase/plataforma/cohorte sigue pendiente. No autoriza compra ni operación.

## 📆 Bitácora

- **2026-10-28 — tres campañas y nuevo mandato económico:** Owner informa integración S04 en curso; levanta el estado anterior de pausa, sustituye retiro fijo por política a evaluar, fija resolución rápida sin caps prudenciales extra dentro de reglas y umbral challenge 1/3, confirma reinversión total y caja de compras. I+D asume la capacidad funcional Backtester; prompts C01/manager/C02 preparados y coordinación en planner existente. A/B pendientes. Sin producto, backtests, gasto o cierre del manager. [[2026-10-28-echo-futures-campaign-types|Registro]].

- **2026-10-28 — siguiente iteración de la fábrica:** Owner pausa frente 1 por merge runtime→master y pide progreso por celdas, reutilización, iteraciones cortas y backlog inteligente. Se interpreta RV-01 por alcance, prepara I01-A/B y retorno técnico C diferido, registra una cola de seis resultados con dependencias y reserva MR06. Verificación oficial focal confirma los claims decisivos; no elige prop ni cierra perfiles. Sin código, campañas, gasto o cierre formal. [[2026-10-28-echo-futures-post-rv01-iteration|Registro]].

- **2026-10-28 — RV-01 y cierre documental:** [[FUT-R01-RV-01-CONSOLIDADO]] entregado con `NO_APTO_AUN`, 24 hallazgos y una reparación focal. [[FUT-R01-INDICE]] reúne los cinco blobs originales disponibles —cuatro retornos y mandato— sin cambios de contenido. Se actualizan enlaces/estado, se registra [[2026-10-28-echo-futures-rv01-session-feedback]] y se cierra esta sesión por instrucción Owner. Futures continúa; no se aceptan campañas, gates ni resultados de laboratorio. [[2026-10-28-echo-futures-rv01-consolidacion|Registro]].

- **2026-10-28 — DR-03 recibido:** [[FUT-R01-DR-03-mecanismos-NQ-2026-10-28]] archivado íntegro y [[Echo Futures — DR-03 mecanismos NQ evidencia y cobertura]] indexado. Sin validar estrategias ni alterar gates. 
- **2026-10-28 — DR-04 recibido:** [[FUT-R01-DR-04-indicadores-reglas-validacion-NQ-2026-10-28]] archivado con transcripción completa y advertencia de inconsistencias; destinado al submanager/RV-01 sin modificar Strategy/MM, datos, G0–G5 ni runtime.

- **2026-10-28 — campañas prop y dispatch separado** — Owner corrige el marco: no gestionar una cuenta propia rentable por trade, sino resolver evaluaciones rápidamente y estudiar la asimetría coste/cobro mediante MM, contratos y campañas. Se preserva USD 400/funded como referencia no verificada de coste agregado. Informe anterior documentado como exploratorio y rectificado; mandatos DR-01–04 y RV-01 preparados en v4, no ejecutados. Continuidad actualizada, sin cambios de producto, gates, gasto ni cierre formal. [[80-agents/journal/logs/2026-10-28-echo-futures-research-runtime-plan|Registro consolidado, addendum de frente 2]].

- **2026-10-28 — dos frentes** — Owner confirma que 5+5 pueden coincidir o diferir, pide prompt completo del frente 2 y planificación/diseño de integración Backtester–runtime para reproducir sesiones con datos precisos. Prompt v3 autocontenido y diseño candidato preparados; fuentes/config/policies divergentes identificadas sin modificar producto ni declarar paridad. Se preserva la declaración Owner de pruebas PROD y se pide receipt actual. [[80-agents/journal/logs/2026-10-28-echo-futures-research-runtime-plan|Registro]].

- **2026-10-28 — corrección Owner** — Capital confirmado: USD 4.000 Futures y aproximadamente USD 2.000 Forex, separados, sin aportes adicionales previstos; USD 5.000 superseded. Embudo de pase/cobro confirmado como aspiración, no estimación. Primer retiro objetivo USD 3.000 con split 90%/80%, bruto/neto pendiente. Ficha Strategy simplificada a setup, filtro y RR/objetivo–riesgo técnico; MM por prop/etapa separado. Prompt v2 ajustado sin cambio de runtime ni relajación de gates. [[80-agents/journal/logs/2026-10-28-echo-futures-capital-simple-strategy|Registro de la corrección]].

- **2026-10-27 — primera ronda Owner** — Aceptados objetivo de trading efectivo, hito táctico 5 challenge + 5 funded retirando, mínimo dos props simultáneas, preferencia algorítmica/sin consistencia y disponibilidad personal amplia. Capital USD 4.000/5.000, asignación y denominadores permanecen abiertos. Revisados código y receipts existentes; MR10 incorporada a cobertura y MR08 reclasificada como híbrida. Prompt de investigación preparado y documentación autorizada; sin campañas, código de producto, promoción ni cierre de sesión. [[80-agents/journal/logs/2026-10-27-echo-futures-fut-r01-owner-mandate|Registro del cambio]].

- **2026-10-27** — Línea incorporada al programa único por mandato Owner. NQ inmediato, economía challenge+retiros, perfil comercial actual por seleccionar. Puente de Optimización transferido conservando REVIEW. Retester y runbook alineados con conformidad teoría→regla→código y sin excepciones de rareza que omitan G2C. No se ejecutaron campañas ni se aceptaron gates.

## 🧭 Decisiones y pendientes

Aceptadas: dos mercados dentro del mismo programa; Futures por Echo Backtester; NQ inmediato; prioridad económica challenge+funded; Owner decide lo material. La ampliación a otros instrumentos y SQX como generación adicional quedan aparcadas, sin ejecutar ni integrar.

**Confirmado el 2026-10-28:** USD 4.000 para compras Futures y Forex separado; Strategy de tres bloques/MM separado; 5+5 pueden coincidir; dos props simultáneas como meta. Integración S04→master en curso según Owner, certificación pendiente de recibo. Retiro fijo USD 3.000 superseded; política a evaluar y cash recibido reinvertido al 100%. Challenge busca pase/pérdida rápidos dentro de reglas sin caps prudenciales extra; umbral 1/3 para futuras campañas. CHALLENGE/FUNDED separadas y SIMULATION integral son capacidad requerida de I+D, entregada por los owners técnicos existentes.

Pendientes materiales: A/B y selección de primera Strategy; programa/ruta contractual; horizonte/seguimiento; políticas concretas y evaluación temporal; costes no incluidos en compra y su fuente si existen; baseline integrado certificado; diseño C01 y decisión focal de admisión funded-only frente al G4 vigente; presupuesto/alcance del siguiente despacho físico. Ya no se pregunta por retiro fijo, reinversión o reserva prudencial. ClutiFX permanece excluida; RV-01 NO_APTO_AUN no se convierte en PASS por este mandato.

## 🔗 Docs / Links

- [[FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION]] — decisiones actuales, KPI propuestos y prompts del frente C.

- [[FUT-R01-ITERACION-01]] — siguientes prompts A/B y C diferido; requisitos de reutilización de la fábrica. El backlog vive en este planner.

- [[Echo — I+D de Estrategias]] · [[Echo I+D — Cobertura Futures]] · [[Echo I+D — Mapa de capacidades]].
- [[FUT-R01-INDICE]] — entrada única a mandato, retornos, trazabilidad de movimientos y cierre.
- [[FUT-R01-RV-01-CONSOLIDADO]] — RV-01: `NO_APTO_AUN`, hallazgos, correcciones, dependencias y propuesta de experimento más alternativa.
- [[FUT-R01-RESEARCH-MANDATE]] — v4 histórico preservado con corrección económica Owner; su estado de recepción quedó superseded por el índice y este planner.
- [[EF-BACKTEST-RUNTIME-INTEGRATION-PLAN]] — diseño candidato del frente 1 bajo Echo Futures; paridad, ramas/contratos, hitos y mandato read-only de Hefesto.
- [[30-resources/agents/skills/echo-futures-research-manager/SKILL|Manager Futures]].
- [[30-resources/runbooks/echo-rnd-cycle-runbook|Ciclo de investigación y mejora]].
- [[30-resources/runbooks/echo-futures-strategy-qualification-runbook|Cualificación técnica Futures]].

## Entrada del próximo chat

> Actúa como manager Futures de Echo I+D; bootstrap sólo si cold. Recupera este planner, [[FUT-R01-INDICE]] y [[FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION]]. A/B siguen pendientes de retorno; integrar su delta sin repetir DR. El Owner informa S04 completa/variantes en integración a master: pausa anterior superseded, no merge certificado. C es nuevo frente de tipos CHALLENGE/FUNDED/SIMULATION, distinto del antiguo I01-C de datos. I+D posee requisitos/prioridad económica del Backtester; planner técnico lab y owners existentes implementan/certifican. USD 4.000 para comprar cuentas, no futuros propios; Forex separado, NQ exclusivo. Retiro variable a evaluar, reinversión 100% del cash recibido; MM de pase/pérdida rápidos dentro de reglas sin caps prudenciales extra, umbral Owner 1/3 no media del mercado. Funded incluye quemadas y todas las iniciadas. Simulation usa caja causal, no multiplicación de ratios ni escala infinita por media positiva. Mantén G0–G5 y eleva cualquier conflicto funded-only/G4 como decisión concreta; no waiver. No código/gasto/campañas/cierre formal por preparar prompts. Reutiliza evidencia válida y coordina con manager S04 existente.

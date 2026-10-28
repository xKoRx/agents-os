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

**Actualización Owner posterior a RV-01 — 2026-10-28:** frente 1 **PAUSED_OWNER** mientras el runtime está en proceso de merge a master; no despachar integración ni nuevo preflight de ese frente. Frente 2 avanza en iteraciones cortas hacia una fábrica permanente con reutilización y backlog priorizado. [[FUT-R01-ITERACION-01]] prepara dos encargos Cloud (ficha causal y contrato/caja) y un retorno técnico diferido. Una ficha puede avanzar documentalmente aunque la campaña siga NO_APTO_AUN. No se afirma que el merge haya terminado ni se selecciona una prop/estrategia para ejecutar.

**2026-10-28 — RV-01 y consolidado documental entregados: `NO_APTO_AUN`.** Expediente único: [[FUT-R01-INDICE]]; dictamen, reparación focal y siguiente propuesta: [[FUT-R01-RV-01-CONSOLIDADO]]. DR-01 sólo está disponible como captura editorial; DR-02 sigue PARCIAL; DR-03/04 están preservados completos según su ingestión. La independencia histórica de autoría no es acreditable: la entrega se clasifica como **AUTORREVISIÓN ADVERSARIAL DOCUMENTAL**. FUT-R01 sigue en curso por dependencias de entradas, contrato, datos y selección. Sesión documental cerrada con feedback; no hay aceptación Owner, ejecución ni cambios de producto o G0–G5.

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

**Estado:** IN_PROGRESS — revisión RV-01 y consolidado terminados; selección del experimento pendiente por dependencias explícitas. **Responsable:** manager Futures con el Owner. **Celdas:** transversal a las celdas NQ de la matriz; habilita su selección sin pretender cubrirlas científicamente. Ver [[FUT-R01-INDICE]] para el expediente reunido.

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

[[FUT-R01-RESEARCH-MANDATE]] v4 conserva el informe anterior, la corrección Owner y las cápsulas DR-01–04/RV-01 como fuente histórica; sus encabezados de recepción no son el estado vigente. [[FUT-R01-RV-01-CONSOLIDADO]] adjudica el material efectivamente disponible con `NO_APTO_AUN` y una reparación focal. No certifica cuatro originales completos ni independencia histórica. Las aspiraciones económicas permanecen hipótesis; G0–G5 y el frente 1 mantienen sus autoridades.

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

**Frente 2 — Iteración 01:** [[FUT-R01-ITERACION-01]] convierte RV-01 en dos entregas acotadas: A) una ficha determinista candidata de persistencia de cierre NQ en FUT-NQ-PERSIST, con fuente, casos y observabilidad; B) un perfil contractual/caja y propuesta de dos MM por etapa con geometría fija. A/B pueden prepararse en paralelo; B no congela los MM mientras falte A o decisiones materiales. MR06 en FUT-NQ-REVERT es alternativa existente, pendiente de reconciliar y sin independencia presumida.

**RV-01 se conserva:** NO_APTO_AUN para campaña definida/reproducible; autorrevisión documental, corpus limitado y selección pendiente. H01 limita la integridad del expediente; no prohíbe especificar una hipótesis propia desde evidencia verificable. H02/H03 requieren programa/fase/ruta/costes completos; H04 exige separar lo observable, lo modelado y datos faltantes. No repetir los DR ni abrir DR-05. Recuperar originales existentes sólo si aportan a una decisión actual; no fabricarlos ni convertir la falta de un original en un bloqueo universal.

**Frente 1 — PAUSED_OWNER:** el Owner informa merge del runtime a master en proceso. Se conserva [[EF-BACKTEST-RUNTIME-INTEGRATION-PLAN]] como diseño candidato histórico, sin avanzar integración ni inspección física. El retorno de datos/recibos I01-C está preparado pero NO DESPACHABLE durante la pausa. Reanudar requiere confirmación Owner y baseline aceptado identificado; un HEAD nuevo no equivale a autorización, despliegue o certificación.

**Caja histórica:** conservar la evidencia del controlador con USD 5.000, compras fijas y financiación research; FUNDED_ONLY excluye adquisición. No acredita el nuevo objetivo de USD 4.000 ni dos props simultáneas. La valoración futura debe usar caja finita y eventos/costes propios del programa, sin reetiquetar ni repetir campañas válidas.

### Cola priorizada de investigación y reutilización

Esta tabla es el backlog único de esta iteración, dentro del planner existente. **Una pregunta primaria Futures**; varios workers pueden resolver componentes independientes. Los estados siguientes son planificación documental, no gates técnicos.

| Orden / estado | Resultado buscado | Dependencia y responsable | Reutilización / aceptación / parada |
|---|---|---|---|
| 1 — AHORA, preparado | I01-A: ficha de persistencia de cierre, evidencia, casos y observabilidad | Worker Cloud; RV-01 y cobertura. Selección definitiva Owner pendiente | Una regla determinista de tres bloques, sin parámetros libres ni nuevas cifras heredadas de papers. Casos y trazas esperadas reutilizables por semántica. Duplicidad o ambigüedad material ⇒ dependencia concreta |
| 2 — AHORA, preparado en paralelo | I01-B: perfil contractual completo, caja y propuesta MM | Worker Cloud; fuentes oficiales. MM finales dependen de geometría A y decisiones Owner | Un perfil y, si cabe, una alternativa con mismas columnas. Candidato documental inicial Rapid EOD 50K; no selección comercial. Campo indispensable desconocido ⇒ parar; no buscar firmas indefinidamente |
| 3 — ESPERA_OWNER | I01-C: datos/recibos existentes aplicables a A/B | Worker read-only Hefesto, sólo tras reanudación; no despachado | Manifiestos/contratos/ventanas/selección/recibos y brecha mínima. Nada de ejecución, nuevas capturas o certificado por existencia de archivos |
| 4 — ADJUDICACIÓN DOCUMENTAL / HANDOFF DIFERIDO | Adjudicar A/B documentalmente; preparar después una primera implementación/cualificación | Manager + Owner revisan A/B y decisiones pertinentes sin esperar C. Handoff técnico requiere además C, reanudación, dueño técnico, presupuesto y alcance aceptados | Decisión documental inmediata sobre retornos; después handoff por identidad y G0–G5 vigentes. Primera integración técnica completa antes de ampliar lote; no campañas por entregar specs |
| 5 — SIGUIENTE, alternativa | Reconciliar MR06 — Volatility Shock Snapback | Se activa si se prioriza alternativa o termina la decisión primaria | Reutilizar señal/evidencia existente; datos/calendario/perfil/caja sólo si compatibles. No otro desarrollo por desconocer su catálogo ni PASS heredado |
| 6 — RESERVA CON DISPARADOR | Una pregunta incremental dentro de la celda: filtro o geometría/salida | Sólo con aprendizaje de la baseline, hipótesis/refutador y nuevo intento declarados | Cambiar un eje con propósito y comparación predefinida. No preparar una parrilla horarios×filtros×RR×MM×props ni elegir variantes por una curva agradable |

La fábrica se mantiene con una unidad activa, la siguiente preparada y alternativas con disparador claro; no con campañas simultáneas implícitas. Agrupar preparación por calendario/datos/analytics/perfil cuando reduce trabajo, conservando identidades y resultados propios. Los requisitos de trazabilidad, oportunidades/vetos, reutilización causal, reintentos y capacidad están en [[FUT-R01-ITERACION-01#Condiciones de aceptación de una fábrica, para registrar antes de implementar|el contrato de la iteración]]; no certifican que el motor ya los satisfaga ni reabren frente 1.

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
- [x] Entregar RV-01 y consolidado de lo disponible, con reparación focal, fuentes críticas y dictamen `NO_APTO_AUN`; reunir los originales disponibles sin alterar sus bytes en [[FUT-R01-INDICE]]. Entrega documental no equivale a aceptación ni ejecución. #owner/me #type/research #area/trading
- [/] Preparar y adjudicar [[FUT-R01-ITERACION-01]]: ficha causal A y contrato/caja B, preservando las dependencias de RV-01. Prompts preparados; retornos A/B aún no recibidos. No repetir los cuatro DR ni reconstruir originales ausentes. #owner/me #type/research #area/trading
- [ ] **PAUSED_OWNER:** [[EF-BACKTEST-RUNTIME-INTEGRATION-PLAN]] y retorno técnico de Hefesto en espera mientras runtime se integra a master. Reanudar sólo con confirmación y baseline aceptado; sin ejecución. #owner/me #type/supervision #area/echo
- [ ] Elegir el primer experimento y una siguiente pregunta de mecanismo diferente; luego despachar sólo el alcance autorizado. #owner/me #type/research #area/trading

Futures Prop Universe es una entrega histórica cerrada, normalizada de `complete` a `completed`; Prop Economics ya estaba cerrado. Enlazarlos no reactiva sus tareas ni equivale a certificar reglas actuales.


- **DR-03 recibido (autodeclarado RESPONDIDO; RECEIVED_WITH_MATERIAL_FINDINGS):** [[FUT-R01-DR-03-mecanismos-NQ-2026-10-28]] conserva el retorno íntegro según ingestión; [[Echo Futures — DR-03 mecanismos NQ evidencia y cobertura]] enlaza su adjudicación en RV-01. Sin aceptación ni cualificación.
- **DR-04 recibido (autodeclarado RESPONDIDO; RECEIVED_WITH_MATERIAL_FINDINGS):** [[FUT-R01-DR-04-indicadores-reglas-validacion-NQ-2026-10-28]] conserva el retorno; errores de unidades, geometría, fills M1 y selección adjudicados en [[FUT-R01-RV-01-CONSOLIDADO]]. Sus fichas no son specs aceptadas.
- **DR-02 recibido (PARCIAL, sin certificación contractual):** [[FUT-R01-DR-02-contratos-prop-NQ-2026-10-28]] conserva 38 líneas sin URLs. RV-01 verifica sólo fuentes decisivas y corrige Rapid/caps/origen de órdenes; el vector completo por programa/fase/plataforma/cohorte sigue pendiente. No autoriza compra ni operación.

## 📆 Bitácora

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

**Confirmado el 2026-10-28:** capital Futures USD 4.000 y Forex aproximadamente USD 2.000 separados, sin aportes adicionales; ficha Strategy de tres bloques con MM por prop/etapa separado; sentido general del embudo como aspiración; superposición 5+5 libre (mismas, distintas o mezcla). Frente 1 PAUSED_OWNER por merge en proceso; diseño conservado sin avance. Para el frente 2 rige economía de campañas prop, sin expectativa positiva por trade como requisito universal y con políticas agresivas de resolución rápida dentro del espacio de investigación. Mandato y retornos disponibles reunidos; RV-01 y consolidado entregados con `NO_APTO_AUN`, independencia histórica no acreditada y reparación focal. La selección queda pendiente según sus dependencias. Owner solicita fábrica permanente, iteraciones cortas, reutilización y backlog priorizado; I01 prepara el primer paquete sin crear otra plataforma ni programa.

Pendientes: primer retiro USD 3.000 previo/posterior al split; política de caja, pérdida máxima y desembolsos; detalle de intentos/resets y horizontes; sostenibilidad/reinversión; Provider/Program/RuleSet actual; primer experimento; riesgos/MM y capacidad física. ClutiFX está excluida de nuevas investigaciones por decisión vigente; no se vuelve a preguntar como prioridad de rescate. La taxonomía y el orden dentro de mecanismos siguen siendo propuestas, no una shortlist aceptada.

## 🔗 Docs / Links

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

> Actúa como manager Futures de Echo I+D. Bootstrap vigente sólo si sesión nueva; lee este planner, [[FUT-R01-INDICE]] y [[FUT-R01-ITERACION-01]]. RV-01 terminó con NO_APTO_AUN para campaña, corpus limitado y autorrevisión documental; no repetir DR-01–04 ni abrir DR-05. El Owner pausó frente 1 mientras runtime está en merge a master: no integración, inspección física, implementación ni ejecución por inercia; no asumir merge terminado. Avanza en documentación A (ficha causal PERSIST/cierre) y B (perfil/caja, dos MM propuestos) dentro de una pregunta primaria. I01-C queda diferido. MR06 es alternativa existente. Usa el backlog de este planner y cierra cada iteración con decisión/evidencia/siguiente pregunta, conservando intentos y reutilizando sólo artefactos compatibles. Capital 4.000 Futures, cero aportes, Forex separado, NQ exclusivo; Strategy tres bloques y MM por prop/etapa separado. Esperanza positiva por trade no es gate universal; agresividad tampoco prueba utilidad. Mantén metas 5+5, dos props simultáneas y horizonte 31-12-2026 como objetivos. USD 3.000 bruto/neto, pago único/acumulado, prioridad rapidez–caja, desembolsos/pérdida y reinversión siguen pendientes; escenarios no autorizan gasto. G0–G5 vigentes. Sin cierre formal salvo pedido Owner.

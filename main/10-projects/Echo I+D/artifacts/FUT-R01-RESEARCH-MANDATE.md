---
type: prompt
schema_version: 1
status: active
area: "[[Trading]]"
target: "IA investigadora Cloud; roles A, B, C e integrador"
prompt_version: 1
inputs:
  - "Autoridades vigentes de Agents-OS y decisiones Owner de FUT-R01"
  - "Matriz de cobertura y baseline de código/recibos con identidad"
  - "Fuentes primarias de investigación y reglas comerciales actuales"
outputs:
  - "Anatomía y métricas propuestas con contratos verificables"
  - "Mapa reconciliado de mecanismos, duplicidades y brechas NQ"
  - "Comparación económica de programas prop y restricciones de cartera"
  - "Primer experimento recomendado y alternativa, con límites y refutadores"
project: "[[Echo I+D — Futures]]"
aliases:
  - "FUT-R01 — Prompt maestro de investigación"
related:
  - "[[Echo — I+D de Estrategias]]"
  - "[[Echo I+D — Cobertura Futures]]"
  - "[[Echo I+D — Mapa de capacidades]]"
tags:
  - kind/prompt
  - area/trading
  - project/echo-rnd
created: "2026-10-27"
updated: "2026-10-27"
---

# FUT-R01 — Investigación de fundamentos, cobertura y economía

## Propósito

Preparar decisiones para el siguiente experimento de Echo Futures: qué piezas debe declarar una estrategia, qué mecanismos cubre el inventario actual, qué mediciones añaden información y qué combinaciones Strategy × MM × RuleSet merecen validación económica para challenge y funded. Es un artefacto subordinado a FUT-R01, no un programa, manager, skill ni planner nuevo.

**Estado del encargo:** PREPARADO. La publicación del prompt no significa que el Deep Research completo haya sido ejecutado, aceptado ni despachado a Hefesto. Las revisiones documentales acotadas usadas para prepararlo no certifican estrategias ni props. Las decisiones comerciales y el calendario final siguen pendientes del Owner.

**Uso:** entregar las secciones de contrato y prompt a una IA que cubra los módulos secuencialmente, o asignar A, B y C a tres workers bajo un solo integrador. Cada worker devuelve un resultado acotado al manager; sólo el manager reconcilia y escribe las notas compartidas. No crear agentes permanentes ni procesos sin fin.

## Contrato de entrada

### Autoridad y estado vigente

Repositorio de gestión: `xKoRx/agents-os`, branch `master`, vault `main/`. En sesión nueva, bootstrap canónico desde `main/AGENTS.md` y guía `main/80-agents/agents-os/agents-os.md`; en sesión caliente, lectura sólo de deltas necesarios. Cargar `echo-futures-research-manager` y las autoridades aplicables; no reconstruir la organización.

Entradas obligatorias de alcance:

- [[Echo — I+D de Estrategias]] y [[Echo I+D — Futures]]: misión, decisiones aceptadas, pendientes y WIP.
- [[Echo I+D — Cobertura Futures]]: celdas existentes, mapeo de código y limitaciones; la taxonomía sigue siendo propuesta.
- [[Echo I+D — Mapa de capacidades]]: superficies y responsables.
- [[30-resources/runbooks/echo-rnd-cycle-runbook]]: identidades y contrato de investigación.
- [[30-resources/agents/skills/echo-retester-master/SKILL]] y [[30-resources/runbooks/echo-futures-strategy-qualification-runbook]]: gates G0–G5, sin reinterpretación por este prompt.

Si una IA no puede acceder a una entrada, debe indicar exactamente qué falta. Puede trabajar en las partes independientes con las fuentes recibidas y devolver una solicitud documental acotada. No afirmar haber leído un archivo privado, ejecutado un comando o inspeccionado un host por tener su URL o un resumen. Un worker externo no publica en el vault.

### Cápsula de decisiones Owner

1. Objetivo permanente: ampliar y mejorar el trading efectivo; convertir sistemas/automatizaciones en operación y retiros sostenibles. El programa incluye Forex/CFD y Futures, pero este encargo pertenece sólo a Futures.
2. Hito al 31-12-2026: Echo Futures fiable, modular y escalable; al menos cinco estrategias challenge y cinco funded produciendo retiros, en al menos dos props simultáneamente. Es una meta, no evidencia actual ni permiso para rebajar validación.
3. NQ es el único instrumento de ejecución autorizado. MNQ, otras patas, nuevos datasets o ampliaciones intermarket requieren decisión específica cuando corresponda. OHLCV 1m no acredita libro, colas ni fills intrabar observables.
4. Aspiración: al menos una cuenta con cobro por diez compradas; challenge 1/3 y retiro 1/3 o 1/2. Denominadores condicionales, horizonte, reinversión y repetición de cobros están abiertos.
5. Capital mencionado: USD 5.000 en la visión y cerca de USD 4.000 iniciales en la respuesta operativa. No resolver la diferencia por cuenta propia ni asumir asignación exclusiva a Futures. No hay compra autorizada.
6. Props: mínimo dos a la vez, elegidas por condiciones para automatización; idealmente sin consistencia. No existe proveedor/programa comercial actual aprobado. Earn2Trade/GAU50 es antecedente histórico, nunca prueba de cuentas reales.
7. No hay favorito de rescate entre TG/FBC/ORB/MR. Buscar diversidad medida y economía útil. ClutiFX es histórico y no se reabre sin decisión expresa.
8. Owner disponible lunes a domingo 08:00–23:30; no inferir throughput ni capacidad libre de Hefesto. Cloud dirige/investiga; Daedalus procesa fuentes locales cuando haga falta; Hefesto implementa y valida sólo con mandato autorizado.
9. Strategy, variante, configuración, MM y Provider/Program/RuleSet son identidades distintas. No alterar señal para corregir MM sin nueva hipótesis.

### Baseline y procedencia mínimos

Lectura documental disponible: `xKoRx/echo@ae1b09bc10370806f7648f076c5fa0825c9efa4e`. No es certificación del estado actual del host.

- TG: reversión de extremo estocástico, con grupos de filtros; FBC: dirección/color de primera vela cerrada, no failed breakout; ORB: ruptura confirmada por cierre fuera de rango inicial.
- MR01–MR10: extensiones/reclaims de VWAP/bandas, recuperación RSI, fallos de ruptura/rango/apertura, shock, pullback condicionado por tendencia, cierre RTH previo y agotamiento de secuencia. MR08 es híbrida de reversión local y contexto H1 tendencial. MR10 existía y faltaba en cobertura.
- R03 registra 89/89 filas reconciliadas, 3.037 compras/328 pases simulados en el perfil histórico, `OWNER_ACCEPTANCE=REVIEW`, nunca LIVE. Su 60/20/20 es confirmación temporal retrospectiva, no OOS virgen.
- Los resultados de configuraciones seleccionadas, cobertura de días o nombres de familias del lab no demuestran cartera independiente, primer payout ni repetición de retiros.
- Para detalle, abrir los enlaces exactos de código/recibos en el planner y la matriz. Reutilizar evidencia válida; no solicitar de nuevo campañas porque provienen de otro chat.

## Contrato de salida

Un informe por módulo asignado y una síntesis integrada. Se pueden devolver en conversación o como artefactos de investigación del proyecto según el canal autorizado; no crear ocho archivos por formalidad.

| Salida | Contenido exigido | Criterio de aceptación |
|---|---|---|
| A — Anatomía y medición | Descomposición, diccionario de métricas, funciones de indicadores, protocolo de combinación/ablación, efectos de salidas y RR | Cada componente tiene propósito, información disponible al decidir, regla comprobable y prueba de aporte o refutación; nada obliga a implementar otro framework. |
| B — Cobertura | Mapeo por identidad, mecanismos/variantes/contextos, redundancias y brechas | Trazabilidad a regla efectiva y fuente; separar hecho de interpretación; no contar distintas ventanas/MM como familias independientes. |
| C — Economía y cartera | Comparación de programas actuales, ruta challenge/funded/live/cobro, caja, escalamiento y dependencia | Fuentes oficiales fechadas; condiciones de fase y automatización explícitas; denominadores y costes sin mezcla ni doble conteo. |
| Síntesis | Qué reutilizar, corregir, investigar o aparcar; máximo tres experimentos candidatos, uno recomendado y una alternativa | Orden justificado por valor de información, coste y contribución; no puntuaciones fabricadas, garantías ni metas convertidas en probabilidades. |
| Retorno de brechas | Evidencia faltante, responsable/superficie y solicitud mínima | Distinguir lectura pendiente, incertidumbre científica, falta de datos, defecto técnico e incompatibilidad comercial. |

Cada módulo entrega además: decisiones que cambia, supuestos no resueltos, evidencia contraria más fuerte y qué resultado haría abandonar su recomendación.

**Presupuesto de investigación propuesto:** una entrega por módulo, una revisión integrada y una corrección enfocada de contradicciones materiales; sin gasto, nuevas campañas ni adquisición de datos. Para la comparación comercial, primera criba de hasta cuatro proveedores y hasta dos programas concretos por proveedor, deteniendo profundidad si falla una condición operativa esencial. Si no aparecen dos alternativas viables, documentar el bloqueo y justificar la ampliación antes de seguir explorando sin límite. No es un presupuesto de compras ni un compromiso de horas/throughput.

**Parada:** terminar cuando estén soportadas las decisiones del contrato, cuando falte una entrada indispensable o cuando el refutador descarte una línea. No seguir acumulando bibliografía sin cambio de decisión. Retorno al manager Futures y al Owner; ninguna recomendación se autopromueve a ejecución.

## Prompt

### Rol y pregunta

Actúa como investigador especializado al servicio del manager Echo Futures. Recibe `ROL=A`, `ROL=B`, `ROL=C` o `ROL=INTEGRADOR`. Si hay una sola IA, trabaja A→B→C y separa después una revisión crítica. No asumas independencia real por cambiar el rol del mismo modelo.

Pregunta principal: ¿qué base mínima y verificable nos permite reutilizar el inventario NQ, identificar sus concentraciones y elegir el siguiente experimento con utilidad económica potencial para challenge y retiros en al menos dos props?

Tu tarea es reducir incertidumbre y producir decisiones preparadas para laboratorio. La literatura, un indicador popular o una historia económica plausible no acreditan ventaja NQ ni rentabilidad en prop.

### Módulo A — Anatomía, métricas e indicadores

1. Proponer una anatomía compatible con las autoridades existentes: hipótesis/mecanismo; datos y disponibilidad causal; contexto/régimen; setup; filtros opcionales de elegibilidad; trigger; dirección y caducidad; invalidación; gestión/salida técnica; MM; ejecución; restricciones de cuenta; cartera; evidencia. Definir qué vive en Strategy y qué pertenece a otro componente. No diseñar ni implementar DSL, motor o runtime nuevo.
2. Distinguir setup de trigger y filtro. Un setup describe la condición preparada; el trigger determina el evento accionable; un filtro restringe elegibilidad bajo una hipótesis incremental. Precisar la máquina de estados cuando haga falta: creación, confirmación, expiración, consumo y rearme. No imponer complejidad a estrategias simples.
3. Para cada componente, entregar definición, campos mínimos, reloj/timezone, unidad, datos disponibles, caso positivo, caso negativo, invalidación/expiración y prueba en traza. Preservar la cadena Fuente/Hipótesis → Regla → Predicado efectivo → Caso positivo/negativo → Traza.
4. Organizar mediciones por función, no por ranking universal de indicadores. Considerar retornos/pendientes/canales para dirección y persistencia; profundidad/duración de retroceso; distancias normalizadas a VWAP/media/rango; extremos/rechazo; ATR/volatilidad para escala; volumen relativo por reloj; sesión y referencias previas. Estudiar RSI/Bollinger/EMA/VWAP sólo donde la hipótesis lo justifique. Precisar si volumen es agregado observable y qué información se pierde.
5. Investigar combinación sin redundancia: regla mínima y control; adición de un componente predeclarado; comparación y ablación; misma población elegible o explicación del cambio de selección; mismo riesgo/costes; beneficio incremental, señales perdidas y estabilidad temporal. La falta de aporte es resultado válido. Registrar todas las combinaciones probadas y limitar interacciones antes de probarlas.
6. Diferenciar SL de invalidación técnica, objetivo técnico de TP ejecutable, salida temporal y monetaria, break-even/trailing/scale-out de una señal nueva. Indicar qué necesita recorrido intrabar y qué no puede resolverse fielmente con OHLCV 1m.
7. Diferenciar RR de distancias planeadas, riesgo monetario neto de costes y payoff realizado. Cambiar TP/SL/timeout puede cambiar tasa de acierto, duración, secuencias, riesgo extremo y reglas de cuenta. No asumir RR óptimo por familia ni recalcular una curva multiplicando ganancias.
8. Entregar un diccionario acotado de métricas con fórmula/unidad, denominador, granularidad, necesidad de datos, sesgo y decisión que informa. Cubrir señal/oportunidad, ejecución, distribución neta de trades, MAE/MFE cuando sea medible, exposición/drawdown/duración, sequías, estabilidad temporal, selección múltiple y economía de cuenta. No usar Sharpe, PF, win rate o número de trades aisladamente como gate universal.
9. Proponer evaluación temporal compatible con datos ya usados: identificar selección y evaluación, contaminación, sensibilidad y regímenes; explicar qué puede aportar walk-forward/bootstrap/Monte Carlo y qué supuestos impiden usarlos. No suponer independencia de trades ni crear OOS retrospectivamente.
10. Incluir una ficha conceptual de una estrategia existente para demostrar la descomposición y una comparación de salidas/RR formulada como hipótesis. No inventar parámetros ganadores ni solicitar optimización masiva.

### Módulo B — Mecanismos y cobertura

1. Partir de la matriz vigente y del inventario; contrastar las reglas y conservar identidad de fuente/spec/código/configuración/MM. La clasificación preliminar puede corregirse con evidencia. No reabrir ClutiFX.
2. Separar mecanismos primarios, contextos, herramientas y implementaciones: persistencia/continuación; reversión de desequilibrio; transiciones de sesión; respuesta a información; transmisión intermarket; microestructura cuando haya datos. Apertura, volatilidad y RSI no crean automáticamente familias independientes.
3. Mapear TG, FBC, ORB y MR01–MR10 a componentes y celdas. Anotar incertidumbre de spec, duplicidad demostrada o sólo sospechada y evidencia económica con fase. No volver a llamar MR08 trend following puro por su nombre ni omitir MR10.
4. Investigar primero preguntas que reutilicen datos/capacidades NQ actuales y permitan refutar barato. Una celda vacía no obliga a llenarla. EVENT, INTERMARKET y FLOW requieren demostrar datos y alcance; enumerar qué falta sin comprar ni adquirirlos.
5. Para cada línea recomendada, entregar: hipótesis falsable; mecanismo económico o regularidad empírica con sus límites; fuente verificable; mercado/periodo de evidencia; datos/resolución; execution model; control/placebo; criterio de refutación; coste y dependencias; contribución incremental a cobertura; relación con otras estrategias; condición de parada/reapertura.
6. Al comparar papers, explicitar diferencias de activo, horizonte, sesión, comisiones, selección y ejecución. Un resultado en SPY u otro mercado no valida NQ. Distinguir acceso a texto completo de resumen.
7. Explicar qué evidencia permitiría decir que una línea puede encajar mejor con una prop: distribución y trayectoria netas, drawdown admisible, frecuencia, tiempos hasta objetivo/cobro y restricciones. No declarar una familia universalmente superior para props.
8. Seleccionar pocas preguntas con mayor valor de información; entregar al integrador hasta tres candidatos, sin convertirlos en campañas autorizadas.

### Módulo C — Economía de props y cartera

1. Construir una comparación con identidad Provider / Program / account size / phase / platform / RuleSet version / fecha de consulta. Distinguir evaluation, simulated funded y live-funded; una regla de otra fase no es intercambiable.
2. Verificar en fuentes oficiales actuales: elegibilidad del Owner pendiente cuando no conste; automatización y APIs; origen permitido de órdenes y restricciones de servidor/VPS/dispositivo; plataformas/conexiones; transición obligatoria a live; noticias; overnight/cierre; contratos/escalamiento; comisiones; drawdown intradía/EOD y referencia de actualización; daily loss; consistencia; días mínimos; fees, resets, renovaciones y activación; seguridad/buffer y payout; reparto; límites/frecuencia; copy trading, cobertura opuesta y multicuentas. Separar prohibición, permiso condicionado y desconocido. No asumir que "bots permitidos" resuelve la arquitectura de operación.
3. Hacer primero una criba de compatibilidad con la operativa algorítmica prevista y con todas las fases relevantes. Después comparar economía. La preferencia por ausencia de consistencia no autoriza ignorar precio, DD, elegibilidad de cobro, transición a live o restricciones multicuentas.
4. Definir unidades de seguimiento: cuenta, compra, intento/reset, renovación, pase, activación funded, primer cobro y cobros repetidos. Formular cohortes y horizonte; contabilizar pendientes/censura sin retirarlos del denominador. Pedir sólo aclaraciones que cambien materialmente la decisión.
5. Modelar `q = P(pase) × P(activación | pase) × P(cobro | activación)` para cohortes/horizontes compatibles. Las aspiraciones 1/3 y 1/3–1/2 no son parámetros estimados. No mezclar probabilidades marginales con condicionales ni dar por cierta activación de todos los pases.
6. Definir ledger: capital inicial + cobros recibidos netos de reparto/transferencia − desembolsos externos − retiros del Owner. Incluir compras, resets, renovaciones, activaciones, datos/operación y reglas de fecha de cobro; no descontar dos veces comisiones/slippage ya incorporados al PnL. El capital nominal de una cuenta funded y el PnL no retirado no son caja disponible.
7. Evaluar cuándo una tasa 1/10 puede generar cash positivo y cuándo no. Separar rentabilidad esperada, riesgo de agotar liquidez antes del cobro, necesidad de reserva, tiempo de recuperación y capacidad de financiar el siguiente lote. Proponer escenarios etiquetados, sin usar precios inventados como reglas reales ni recomendar tamaño de compra antes de autorización.
8. Evaluar cartera con PnL normalizado temporalmente, solapamiento de señales/posiciones, pérdidas simultáneas, régimen, dirección/sesión/evento, drawdowns coincidentes y colas, inactividad/frecuencia, hipótesis compartidas y dependencia de MM. Usar calendario alineado e incluir períodos sin posición; no interpretar ausencia de dato como cero. La normalización debe declararse y no ocultar riesgo absoluto.
9. Distinguir diversificación de estrategia, ejecución y contraparte. NQ comparte shocks; dos props no hacen independientes cuentas que replican la misma señal. Treinta compras no aseguran tres pagos por tener q objetivo 10%. Bootstrap/Monte Carlo deben respetar bloques/régimen/dependencia y disponibilidad de datos; no ejecutar simulaciones en este encargo.
10. Proponer cómo comparar una señal congelada con distintos MM/RuleSets y cómo someter cartera a restricciones conjuntas. La señal, el MM y el perfil conservan IDs distintos; cualquier cambio se registra, no se atribuye retrospectivamente a la misma estrategia.

### Integración y revisión

Consolidar los módulos sin promediar opiniones ni decidir por mayoría de IAs. Para cada conflicto, identificar autoridad, evidencia y alcance: hecho observado, hipótesis, inferencia, propuesta o decisión del Owner.

Entregar una síntesis con estas decisiones: qué evidencia se reutiliza; qué falta para calificar identidades actuales; qué componente/medición merece estudio; qué celda aportaría conocimiento; cuáles programas pasan la criba y qué queda desconocido; primer experimento recomendado y alternativa. Indicar responsable, dependencia, coste estimable o desconocido, criterio de aceptación y cancelación, y decisión material requerida.

Mantener G0–G5 exactamente en las autoridades vigentes. En particular, no omitir el trade propio reconciliado G2C ni el trimestre propio requerido G4 antes del histórico; rareza, funded o "research" no son excepciones. El gate trimestral filtra cómputo, no demuestra robustez estadística o payout. Si el contrato no encaja con una línea propuesta, devolver la incompatibilidad para decisión; no cambiarlo desde este informe.

No preparar el roadmap Q4 definitivo sin resolver las decisiones económicas y la capacidad real. Sí devolver dependencias y qué evidencia permitiría construir escenarios conservador/base/ambicioso.

### Protocolo de fuentes

- Priorizar investigación primaria, especificaciones originales, documentación oficial y evidencia reproducible. Para props, fuentes oficiales actuales y versión/fecha; una comparativa afiliada no es autoridad de reglas.
- Por afirmación decisiva: enlace exacto, sección, fecha consultada, fecha/publicación cuando exista, alcance, mercado/periodo y limitaciones. Marcar explícitamente si sólo se leyó un abstract.
- Separar citas de inferencias y conservar evidencia negativa. No copiar extensamente fuentes ni llenar el informe con referencias sin función.
- Si dos fuentes oficiales discrepan, conservar la contradicción y precisar programa/fase/fecha; no escoger silenciosamente la más favorable.
- No inventar acceso, resultados, precisión de métricas ni probabilidades. Declarar UNKNOWN/NOT_EVALUATED donde corresponda.

Puntos de partida ya localizados, no conclusiones suficientes:

- Bailey et al., [The Probability of Backtest Overfitting](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf): marco para estudiar sesgo por selección entre alternativas; no se adopta automáticamente como gate nuevo.
- Gao et al., [Market Intraday Momentum](https://profiles.wustl.edu/en/publications/market-intraday-momentum/), JFE 2018: referencia de persistencia temporal en SPY/ETFs; aquí se consultó el resumen institucional. No es validación NQ/prop.
- Topstep, [API Access](https://help.topstep.com/en/articles/11187768-topstepx-api-access) y [Live Funded Account Parameters](https://help.topstep.com/en/articles/10657969-live-funded-account-parameters), consultados el 27-10-2026 America/Santiago: ejemplo de restricciones que cambian por fase y arquitectura. La página API limita el origen de órdenes; la de live indica indisponibilidad de esa API y de estrategias automatizadas. Revalidar antes de seleccionar/comprar; estas páginas no constituyen elección comercial.

## Límites

### Mandato ONE-SHOT para recuperación física, preparado y no despachado

**Pregunta:** ¿qué evidencia física ya existente falta para reconciliar las identidades NQ y qué capacidad real podría asignarse al siguiente trabajo?

**Autoridad:** FUT-R01, manager Futures y autoridades técnicas canónicas de Hefesto. Un ejecutor local realiza bootstrap si corresponde y lee sólo el alcance necesario. No deducir permiso de ejecución de esta plantilla; confirmar canal, responsable y disponibilidad existentes.

**Entradas:** IDs y rutas de los gaps concretos del inventario; catálogo/configuraciones/specs, recibos R03 y manifiestos referenciados. El manager completa la lista de huecos antes de despachar; no pedir una auditoría exhaustiva de todo el host.

**Entregables:** un receipt de lectura con fecha/hora, repo/HEAD/branch/worktree observado, IDs efectivos de configuración/MM/perfil, build/binary asociado a cada receipt solicitado, localización/hash de datos y artefactos necesarios, cobertura temporal/sesión/roll/costes declarados, disponibilidad de trazas y aceptación; más capacidad compartida y trabajos activos observables. Identificar lo ausente o no comprobable. Datos voluminosos permanecen en su almacén; retornar referencias, no copiar todo el dataset.

**Presupuesto:** una pasada por las rutas autorizadas y una aclaración enfocada de discrepancias. Sin jobs nuevos, motores, tests, replay, backtest, instalaciones ni compras. No exportar secretos/credenciales ni asumir acceso inexistente.

**Refutador/Gates:** si no se puede vincular config/build/datos/receipt, declarar evidencia insuficiente; no rellenar por inferencia ni heredar PASS. Una lectura no recertifica G0–G5.

**Condición de parada:** evidencia solicitada recuperada, acceso ausente, autoridad contradictoria o paso que necesite mutación/ejecución fuera del alcance.

**Retorno:** registrar el receipt en la superficie canónica de evidencia del proyecto técnico, bajo la autorización de ese encargo, y devolver enlace al manager. No editar simultáneamente el planner compartido. Hasta despacharlo, no se considera trabajo iniciado en Hefesto.

### Fronteras comunes

No implementación ni cambios del Backtester/runtime; no campañas o optimizaciones; no compra/operación de cuentas; no cambio material de MM; no nuevos instrumentos; no reapertura de ClutiFX; no promoción por lectura documental; no nuevos gates, managers o skills; no procesos autónomos indefinidos. El integrador conserva un único WIP primario Futures y devuelve decisiones al Owner. La publicación de estas bases no es un cierre de sesión.


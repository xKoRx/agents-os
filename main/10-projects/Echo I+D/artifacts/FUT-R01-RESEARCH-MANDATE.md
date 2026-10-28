---
type: prompt
schema_version: 1
status: active
area: "[[Trading]]"
target: "IA investigadora Cloud; roles A, B, C e integrador"
prompt_version: 3
inputs:
  - "Cápsula autocontenida de decisiones Owner y baseline de FUT-R01"
  - "Adjuntos efectivamente suministrados y cobertura NQ provisional"
  - "Fuentes primarias y reglas oficiales actuales de props"
outputs:
  - "Fichas de Strategy: setup, filtro, RR u objetivo y riesgo técnico"
  - "Mapa de familias, redundancias y brechas NQ"
  - "Comparación de MM por prop/etapa y economía de caja"
  - "Primer experimento recomendado y alternativa"
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
updated: "2026-10-28"
---

# FUT-R01 — Frente 2: prompt maestro de Deep Research

## Propósito

Investigar fundamentos prácticos de estrategias algorítmicas objetivas para NQ. La ficha aceptada por el Owner tiene **setup, filtro y RR u objetivo–riesgo técnico**. **Strategy es una entidad; MM asociado a prop/etapa es otra.**

**Versión 3 — PREPARADO para uso externo; Deep Research completo NO EJECUTADO.** El Owner confirmó que las cinco estrategias challenge y las cinco funded pueden coincidir, diferir o combinarse. Capital: USD 4.000 Futures y aproximadamente USD 2.000 Forex separados, sin aportes adicionales previstos.

Esta versión separa investigación externa de recuperación interna: el investigador recibe una cápsula autocontenida. El manager conserva bootstrap, reconciliación del vault, valoración de evidencia y decisiones de producto. El frente 1 autorizado se documenta en [[EF-BACKTEST-RUNTIME-INTEGRATION-PLAN]], bajo [[Echo Futures]]; no lo sustituye este prompt.

## Contrato de entrada

El manager verifica que la cápsula refleje decisiones vigentes y adjunta sólo las fuentes necesarias. Los documentos no suministrados no se consideran leídos. Una IA externa puede ejecutar todo el encargo o tres workers acotados A/B/C con integración común. No requiere acceso a repositorios privados.

Autoridades internas del manager: [[Echo I+D — Futures]], [[Echo I+D — Cobertura Futures]], [[Echo I+D — Mapa de capacidades]], skill de manager Futures y gates/runbook de cualificación vigentes. No delegar al investigador la elección de cuál documento interno tiene autoridad.

## Contrato de salida

Informe con fuentes verificables, fichas simples, matriz de mecanismos/medidas/evidencia, cobertura provisional, comparación de programas y caja, primer experimento y alternativa. Toda conclusión distingue hechos, inferencias, propuestas y desconocidos. Su existencia no acepta hipótesis, selecciona prop ni autoriza gasto o ejecución.

## Prompt

Copiar íntegro el bloque siguiente:

```text
# ECHO FUTURES — FRENTE 2
## Deep Research: estrategias, cobertura, indicadores y economía prop

Actúa como un equipo de investigación cuantitativa y económica. Investiga evidencia externa y conviértela en decisiones investigables para Echo Futures. Puedes trabajar con una IA o repartir el encargo entre los módulos A, B y C, con una síntesis y revisión independiente comunes.

No ejecutes backtests, implementaciones, compras ni operaciones. No supongas acceso a repositorios, Hefesto, cuentas o conversaciones anteriores. La información interna disponible es esta cápsula y los adjuntos efectivamente suministrados. El manager conserva la autoridad sobre Agents-OS y el producto.

## 1. Pregunta central

¿Qué mecanismos y reglas objetivas merece investigar Echo Futures para construir estrategias algorítmicas de NQ útiles en challenges y funded, aportando cobertura y diversificación respecto del trabajo existente, con una economía compatible con USD 4.000 de capital inicial?

Necesitamos fundamentos prácticos: expresar setups, elegir filtros, establecer riesgo/objetivo técnico, combinar indicadores con una hipótesis y medir su utilidad. No buscamos indicadores populares por sí solos ni familias declaradas universalmente superiores.

## 2. Cápsula interna: decisiones y estado

- Instrumento ejecutable autorizado: NQ. MNQ y otros instrumentos no están autorizados.
- Capital inicial: USD 4.000 exclusivamente Futures, sin nuevos aportes previstos. Forex tiene aproximadamente USD 2.000 separados y no respalda este presupuesto.
- Meta táctica al 31-12-2026: cinco estrategias challenge y cinco funded generando retiros, en al menos dos propfirms simultáneamente. Pueden ser las mismas estrategias, distintas o una mezcla. Es un objetivo, no un resultado ni una factibilidad demostrada.
- Aspiración: al menos una cuenta con retiro por cada diez evaluaciones compradas. Embudo ideal: pase de 1/3 y cobro de 1/3–1/2 de las funded activadas. Son objetivos del Owner, no probabilidades estimadas.
- Primer retiro objetivo: USD 3.000. Analiza por separado monto bruto antes del split y monto neto recibido, con splits de 90% y 80%. Verifica los límites reales de cada programa; esta distinción no bloquea el research.
- Se prefieren props compatibles con trading algorítmico, idealmente sin consistencia y con economía favorable durante todo el ciclo. Ninguna prop/programa está seleccionada.
- Existe trabajo sobre TG/TradesGerard, FBC/NY First Candle, ORB y MR01–MR10. FBC usa dirección de una primera vela cerrada; ORB, ruptura de rango; MR08 incluye recuperación local condicionada a tendencia H1. No infieras las demás reglas por sus nombres.
- R03 aporta evidencia histórica simulada y confirmación temporal retrospectiva. No acredita OOS virgen, producción ni retiros reales. Variantes, timeframes y MM no equivalen automáticamente a estrategias independientes.
- ClutiFX permanece como histórico y no se reabre. Earn2Trade/GAU50 es antecedente histórico, no elección comercial actual.
- El baseline menciona OHLCV 1m; su cobertura física y otros datos no están certificados en este encargo.
- El frente 1 gestiona recuperación e integración Backtester–runtime. Tú entregas fundamentos, restricciones y experimentos propuestos; no diseñas otro motor ni repites campañas.

Si falta una regla interna, identifica el dato necesario y continúa la investigación externa que no depende de él.

## 3. Contrato simple de Strategy

Cada Strategy propuesta se expresa en sólo tres bloques:

1. SETUP: condición objetiva que produce una entrada; dirección, evento, precio/indicadores, parámetros y timeframe necesarios para reproducirla.
2. FILTRO: condición booleana opcional que permite o bloquea el setup. Puede ser ninguno.
3. OBJETIVO Y RIESGO / RR: stop y objetivo, o distancia de riesgo y RR, en ATR o unidades explícitas de precio. En NQ, indica puntos/ticks y conversión; evita una unidad “pip” ambigua.

Identidad y versión acompañan la ficha. No conviertas gobierno, cuenta, cartera, validación o arquitectura en bloques adicionales de Strategy.

MM es otra entidad, asociada a prop/programa/etapa: dimensiona contratos, riesgo monetario y controles conforme a sus reglas. Si una salida está gobernada por el MM existente, decláralo; no inventes otra regla de señal.

Hipótesis, fuentes, pruebas y costes pertenecen a fichas de investigación separadas. Las reglas deben ser deterministas; cualquier condición visual o discrecional necesita un predicado computable o se excluye.

## 4. Módulo A — Setups, filtros, indicadores, RR y métricas

Investiga cómo construir reglas objetivas y parsimoniosas:

- Clasifica medidas por función: dirección, extensión, rango, volatilidad, actividad/volumen y contexto temporal.
- Para cada indicador candidato, explica qué mide, qué datos necesita, cuándo están disponibles, su retraso/limitación y qué pregunta ayuda a responder. Un indicador no demuestra por sí solo una ventaja.
- Propón combinaciones motivadas por una hipótesis. Compara baseline simple, adición de un filtro y ablación. Evalúa redundancia, frecuencia perdida y valor incremental.
- Separa RR planeado de payoff realizado. Explica cómo stop/objetivo pueden cambiar duración, frecuencia de acierto, secuencias adversas y compatibilidad prop. No simules otro RR multiplicando una curva anterior.
- Propón un conjunto mínimo de métricas para decidir: frecuencia y sequías, expectativa neta, dispersión/colas, drawdown/recuperación, sensibilidad y estabilidad temporal. Define fórmula, denominador, datos y decisión que informa.
- Incluye pocas fichas ilustrativas de tres bloques, marcadas como hipótesis para validar; no entregues una lista interminable de recetas.

No busques parámetros “óptimos” sin un experimento definido.

## 5. Módulo B — Mecanismos, familias y cobertura

Construye una taxonomía económica compacta. Distingue persistencia/continuación/pullbacks, reversión de presión transitoria/excesos y rupturas aceptadas frente a fallidas/recuperaciones.

Trata apertura, sesiones, volatilidad y referencias como VWAP según su función real: pueden ser contexto, medición o parte de un mecanismo; no son automáticamente familias independientes. Eventos, relaciones entre mercados y microestructura son líneas condicionadas a datos y autorización.

Contrasta evidencia y contraevidencia en fuentes primarias. Declara si los resultados pertenecen a NQ, otros futuros, ETFs u otro mercado, y qué faltaría para transferirlos.

Relaciona provisionalmente los hallazgos con la cápsula TG/FBC/ORB/MR: cobertura probable, solapamiento posible y desconocidos. No certifiques equivalencia ni independencia sin reglas o señales verificadas.

Prioriza valor económico potencial, aprendizaje, reutilización y coste de refutación. Una celda vacía no obliga a desarrollarla.

## 6. Módulo C — Props, MM, caja y cartera

Criba hasta cuatro propfirms y hasta dos programas concretos por firma. Justifica una ampliación sólo si es necesaria para obtener al menos dos alternativas elegibles.

Usa condiciones oficiales vigentes a la fecha de consulta. Separa Provider/Program/tamaño/fase/plataforma/RuleSet. Verifica automatización, origen de órdenes/API, transición a live, drawdown y actualización intradía/EOD, consistencia, noticias, horarios, contratos, comisiones, suscripciones, activación, payouts, copy/multicuentas y restricciones pertinentes entre firmas. Si la elegibilidad depende del país o de un dato no suministrado, déjala condicionada.

Compara señales congeladas contra distintos MM y perfiles. No cambies la señal para compensar silenciosamente un problema monetario.

Modela conceptualmente compra→pase→activación→primer cobro→cobros posteriores, con horizonte, cohortes y cuentas pendientes explícitos. Incluye ambos escenarios del retiro USD 3.000 y las restricciones efectivas de pago.

Evalúa caja disponible hasta el primer cobro y continuidad de los siguientes intentos. Funded nominal, beneficio no cobrado y financiación adicional de investigación no son bankroll disponible. Incluye todos los costes sin duplicarlos y separa economía de una fase de economía del ciclo completo.

Propón reservas, desembolsos por etapas y condiciones de parada para decisión Owner; no autorices gasto ni inventes una reserva aceptada. Una tasa objetivo de 1/10 no demuestra autosostenimiento.

Para cartera, define medidas de solapamiento de señales/posiciones, pérdidas conjuntas, drawdowns simultáneos, exposición por dirección/sesión/régimen, colas y períodos sin operaciones. Dos props no vuelven independientes estrategias NQ replicadas. No supongas independencia para estimar supervivencia del bankroll.

Puedes hacer cálculos transparentes y escenarios algebraicos; no ejecutes backtests ni Monte Carlo en este encargo.

## 7. Ocho puntos por cada línea recomendada

Cada hipótesis priorizada debe incluir:

1. Hipótesis falsable.
2. Explicación económica propuesta o regularidad empírica.
3. Evidencia previa y fuente verificable, incluida contraevidencia.
4. Datos requeridos y disponibilidad causal.
5. Modelo de ejecución necesario y límites de observabilidad.
6. Criterio de refutación y control comparable.
7. Coste de implementación/validación, supuestos y desconocidos; no inventes throughput ni horas.
8. Aporte esperado a la cobertura existente.

Estos puntos pertenecen a investigación y no amplían los tres bloques de Strategy.

## 8. Entrega, fuentes, revisión y parada

Entrega un informe integrado con síntesis ejecutiva y tablas comparables:

- Anatomía simple y fichas ilustrativas.
- Mapa mecanismo→medida→regla→evidencia→limitación.
- Cobertura provisional, redundancias y brechas priorizadas.
- Comparación comercial/económica fechada.
- Primer experimento recomendado y una alternativa, con los ocho puntos anteriores.
- Decisiones reservadas al Owner y recuperación interna pendiente.

Distingue HECHO, INFERENCIA, PROPUESTA y DESCONOCIDO. Para cada afirmación material incluye URL, fuente, fecha y alcance. Usa papers y documentación primaria; las reglas comerciales deben proceder de páginas oficiales del programa concreto. Declara si sólo leíste un abstract. Marketing, backtests de terceros y resultados de otro mercado no son evidencia propia NQ. Reporta contradicciones y fuentes inaccesibles.

Conserva los gates G0–G5 existentes; no los redefinas ni declares superados sin sus autoridades. Rareza, pocas señales o destino funded no justifican omitir controles. No llames OOS virgen a información usada para seleccionar ni atribuyas fills intrabar observados a barras de un minuto.

Una revisión adversarial integra los módulos y busca contradicciones, redundancia, extrapolación, múltiples intentos y errores de caja. La decisión no se toma por votación de IAs.

Mandato ONE-SHOT: pregunta anterior; autoridad limitada a investigar; entradas de esta cápsula; entregables indicados; presupuesto de una entrega por módulo, una síntesis/revisión y una reparación focal si impide decidir. Detente cuando exista una decisión investigable o una dependencia indispensable identificada. Devuelve informe, fuentes, limitaciones y siguiente decisión; no prolongues la búsqueda para obtener un resultado favorable.

El manager incorporará el retorno a Agents-OS. No necesitas acceso al vault ni debes inventar registros internos, consumos de recursos o ejecución física. No cierres formalmente la sesión del programa.
```

## Límites

- Sólo investigación y análisis. Sin implementación, pruebas físicas, backtests, compras, operaciones ni promoción.
- No reconstruir el baseline completo dentro del Deep Research ni repetir campañas válidas.
- Los ocho criterios de investigación no agregan campos a la entidad Strategy.
- Los escenarios de USD 3.000 bruto/neto permiten investigar sin resolver esa decisión por el Owner.
- Mantener trazabilidad y gates existentes; no producir nuevas excepciones.
- El manager integra y persiste el retorno en sus superficies canónicas. Sin cierre formal de sesión salvo solicitud Owner.

---
type: doc
schema_version: 1
status: active
area: "[[Trading]]"
project: "[[Echo I+D — Futures]]"
related:
  - "[[Echo — I+D de Estrategias]]"
  - "[[Echo I+D — Futures]]"
  - "[[Echo Futures]]"
  - "[[30-resources/agents/skills/echo-futures-research-manager/SKILL]]"
  - "[[30-resources/agents/skills/echo-retester-master/SKILL]]"
aliases: []
tags:
  - kind/doc
  - area/trading
created: "2026-10-27"
updated: "2026-10-27"
---

# Echo I+D — Cobertura Futures

## Propósito

Organizar la diversidad de investigación de [[Echo I+D — Futures]] y hacer visible qué conocimiento aporta cada trabajo al objetivo Owner: estrategias capaces de pasar challenges y producir retiros en cuentas funded con economía completa evaluable. Esta matriz es una superficie de cobertura enlazada al planner de mercado; no es otro planner ni una lista de estrategias rentables.

**Decisiones Owner vigentes — 2026-10-27:** programa permanente con líneas Forex y Futures; ejecución Futures centrada por ahora en **NQ**; prioridad challenge y retiros; ampliación de instrumentos diferida. Las antiguas cuentas E2T no fueron operadas y no representan una cuenta vigente. Ningún proveedor comercial se selecciona por este documento.

**PROPOSAL — NOT ACCEPTED:** la taxonomía, las celdas iniciales y su orden de investigación son una propuesta de planificación. Su incorporación documental no constituye una shortlist aprobada, autorización de cómputo ni evidencia de alpha. El manager contrasta el inventario en `FUT-R01` y acuerda con el Owner la selección material. No se fija un número objetivo de familias ni estrategias.

## Contenido

### 1. Unidad de cobertura y conceptos

Una celda relaciona **mecanismo/tesis × instrumento de ejecución × contexto y horizonte × fase económica**. Sólo se materializan combinaciones que planteen una pregunta real; no se calcula un producto cartesiano ni un porcentaje sobre un universo infinito.

El vocabulario canónico de **familia, tesis, estrategia, variante, configuración, MM, campaña, run y celda** está en [[30-resources/runbooks/echo-rnd-cycle-runbook#Vocabulario mínimo|Vocabulario del ciclo común]]. La matriz aplica ese contrato: una familia no es un indicador ni una marca de trader; una tesis empírica no requiere inventar una explicación causal.

Una estrategia puede informar varias celdas; una celda puede requerir varias estrategias o terminar descartada. Cada proyecto de investigación enlaza la celda o conjunto acotado que pretende informar. El desarrollo de una capacidad compartida enlaza las celdas que desbloquea, sin fingir que el motor o el runtime son una estrategia. La evidencia vive una sola vez en su proyecto/recibo canónico; aquí se enlaza.

### 2. Taxonomía abierta por mecanismo

| Mecanismo o pregunta económica | Expresiones posibles | Qué no demuestra el nombre |
|---|---|---|
| Persistencia de información o presión direccional | Momentum, trend following, ruptura, continuación tras pullback | Un cruce o breakout no prueba persistencia explotable |
| Reversión de presión transitoria o desequilibrio de inventario | VWAP reclaim, recuperación de rango, exceso y rechazo | Alejarse de una media no obliga al precio a volver |
| Flujos ligados al reloj institucional | Apertura/cierre, transición de sesiones, rebalanceos, roll | Un horario favorable observado no demuestra un flujo causal |
| Respuesta a información exógena | Noticias macro, inventarios, decisiones de bancos centrales | Un calendario por sí solo no es una señal ni permite anticipar la sorpresa |
| Transmisión entre mercados y valor relativo | Confirmación intermarket, lead/lag, spreads | Correlación histórica no prueba liderazgo causal ni ejecutabilidad de ambas patas |
| Estructura temporal, carry y almacenamiento | Curva de futuros, roll yield, spreads de calendario | Backwardation/contango no implican ganancia intradía automática |
| Estacionalidad física y oferta/demanda | Ciclos agrícolas, energía, inventarios estacionales | Una pauta de calendario puede tener pocas observaciones independientes |
| Transferencia de riesgo y restricciones de participantes | Cobertura comercial, posicionamiento, desbalances forzados | Una historia económica plausible no valida el efecto después de costes |
| Microestructura y provisión de liquidez | Order flow, desequilibrio de libro, spread e inventario | Las barras de un minuto no reconstruyen cola, prioridad o fills pasivos |

Esta taxonomía no obliga a abrir todos los frentes. Volatilidad, régimen, sesión, dirección y horizonte son ejes de contexto. Market structure, volume profile, VWAP y auction market theory aportan definiciones/medidas que deben convertirse en tesis precisas. ML es una herramienta de estimación, no una familia económica por sí misma. Una expresión como liquidity sweep no acredita intención de otros participantes.

### 3. Ejes y restricciones de cada celda

- **Instrumento:** símbolo ejecutado, contrato físico, tick/point value, costes, calendario y roll. NQ es el foco actual; datos auxiliares de otro mercado requieren alcance declarado.
- **Horizonte:** tiempo de señal y duración de posición esperada, información disponible al decidir y resolución necesaria. No asignar frecuencias numéricas sin medirlas.
- **Contexto:** sesión, dirección, volatilidad/régimen y presencia de eventos; declarar el criterio antes del experimento.
- **Economía:** distinguir evaluación/challenge, funded y ciclo completo. Un pase es una transición, no un retiro; un payout simulado no es dinero realmente recibido. Identificar compras, renovaciones, activaciones, comisiones, slippage, restricciones, supervivencia, elegibilidad de retiro y cash neto sin doble conteo.
- **Provider/MM:** perfil versionado efectivo, ventanas/cierres, drawdown, límites y geometría de riesgo. El perfil E2T histórico no fija estos campos para el siguiente trabajo.
- **Fuente:** investigación propia, paper/documentación, curso o búsqueda asistida por herramientas. MKE se usa sólo cuando la fuente lo necesita. SQX puede ser una alternativa futura de generación para Futures; la aceptación técnica/económica debe recorrer Echo Backtester y su cualificación canónica, con integración y alcance previamente acordados.

Los gates G0–G5 vigentes siguen en `echo-retester-master`; esta matriz no crea excepciones para datos escasos, estudios llamados discovery o estrategias destinadas a funded. Si un nuevo diseño exige una política distinta, se presenta al Owner antes de ejecutarlo.

### 4. Celdas iniciales NQ para contraste en FUT-R01

**Condición de datos:** el último preflight físico citado aquí es del 2026-10-23, no una inspección actual del host. Describe NQ físico con OHLCV 1m y sin ticks; `FUT-R01` verificará qué manifiestos siguen vigentes. Las filas compatibles con barras no están por ello listas para ejecutar.

| ID de planificación | Tesis / contexto a investigar | Relación con trabajo existente | Datos y frecuencia cualitativa | Experimento que podría refutarla |
|---|---|---|---|---|
| FUT-NQ-PERSIST | Persistencia intradía tras impulso, ruptura o retroceso dentro de una sesión autorizada | ORB, MR08 Trend Pullback Mean Reclaim y parte de ClutiFX continuation | OHLCV 1m/HTF causales; oportunidades condicionadas a tendencia/impulso, frecuencia por medir | Comparar continuación con control equivalente en sesión, volatilidad, riesgo y costes; comprobar si desaparece fuera del régimen o periodo elegido |
| FUT-NQ-REVERT | Reversión después de una extensión transitoria dentro de un contexto definido | TG; MR01 VWAP Reclaim, MR02 Bollinger Failed Continuation, MR03 RSI Range Recovery, MR06 shock snapback, MR07 range fade | OHLCV/volumen causal; eventos de extensión, sin cuota de señales supuesta | Medir reversión neta frente a continuación adversa y control; refutar si el movimiento disponible no cubre costes o depende de umbrales escogidos después |
| FUT-NQ-OPEN | La apertura cash produce una transición diferenciable en dirección o persistencia | FBC **NY FIRST CANDLE**, ORB, MR05 Opening Drive Rejection | Barras de apertura y calendario/DST; elegibilidad por sesión no equivale a señal diaria | Contrastar con ventanas placebo y controles de volatilidad; separar efecto de apertura de una regla genérica de momentum/reversión |
| FUT-NQ-FAILED | Una ruptura no aceptada tiene una respuesta posterior distinta a una ruptura aceptada | MR04 Opening Range Failed Breakout; ClutiFX Failure Swing, con especificación y fuente propias | OHLC causal; definiciones precisas de intento, confirmación e invalidación; rareza por medir | Comprobar que los predicados separan conductas y no son réplicas de otra señal; comparar confirmaciones/invalidaciones predeclaradas |
| FUT-NQ-SESSION | La transición entre sesiones y referencias previas aporta información incremental | MR09 Previous RTH Close Magnet; variantes de sesión ClutiFX | Datos overnight/RTH, cierre previo, calendario y gaps; oportunidades condicionadas | Comparar referencias reales/placebo y comprobar si el efecto persiste dentro de la ventana efectivamente operable, con costes |
| FUT-NQ-EVENT | Una clase de sorpresa exógena produce continuación o reversión condicionada | No se acredita cobertura aceptada; noticias ClutiFX figura como dependencia de datos | Eventos con timestamp, versión y dato disponible al decidir; frecuencia marcada por eventos | Refutar si el efecto se explica por datos revisados, latencia/costes o selección retrospectiva de eventos; sin dataset adecuado no ejecutar |
| FUT-NQ-INTERMARKET | Otra serie aporta información causal incremental para operar NQ | SMT ClutiFX pendiente de datos; no equivale a un spread ejecutable | Serie auxiliar sincronizada, retrasos y calendario; `PARKED_SCOPE/DATA` hasta autorizar/verificar | Comparar contra NQ solo con las mismas ventanas; refutar si el aporte desaparece al respetar disponibilidad, costes y validación temporal |
| FUT-NQ-FLOW | Order flow o libro aportan una señal direccional o de liquidez aprovechable | No se acredita soporte de datos suficiente en el preflight 1m citado | Trades/quotes/libro según tesis; `BLOCKED_DATA`, frecuencia dependiente de eventos | Evaluar con datos/execution model adecuados; refutar si el efecto desaparece tras spread, prioridad, latencia o fills realizables |

Las filas OPEN, FAILED y SESSION son celdas útiles de contexto/tesis, **no familias independientes acreditadas**. Pueden pertenecer al mismo mecanismo que PERSIST o REVERT. No contar dos veces una hipótesis por cambiar nombre, indicador, sesión, variante o MM.

#### Estados separados al crear esta matriz

| Celda | Estado científico | Estado técnico | Estado económico |
|---|---|---|---|
| FUT-NQ-PERSIST | Tesis propuesta; evidencia existente por inventariar | Código relacionado; cualificación por identidad pendiente de lectura de recibos | Sin aceptación económica nueva por esta matriz |
| FUT-NQ-REVERT | Tesis propuesta; evidencia existente por inventariar | Código relacionado; cualificación por identidad pendiente de lectura de recibos | Sin aceptación económica nueva por esta matriz |
| FUT-NQ-OPEN | Tesis/contexto propuesto; posible solapamiento | FBC/ORB/MR relacionados; recibos por reconciliar en inventario | Sin aceptación económica nueva por esta matriz |
| FUT-NQ-FAILED | Tesis propuesta; fidelidad y operacionalización dependen de identidad | MR04/ClutiFX relacionados; no heredar PASS | Sin aceptación nueva; respetar resultados negativos y bloqueos existentes |
| FUT-NQ-SESSION | Tesis propuesta; compatibilidad temporal por comprobar | Código relacionado; calendario/AccountPolicy por fijar | Provider actual no seleccionado por este documento |
| FUT-NQ-EVENT | DISCOVERY | BLOCKED_DATA hasta demostrar fuente utilizable | NOT_EVALUATED en este programa |
| FUT-NQ-INTERMARKET | DISCOVERY | PARKED_SCOPE/DATA | NOT_EVALUATED en este programa |
| FUT-NQ-FLOW | DISCOVERY | BLOCKED_DATA | NOT_EVALUATED en este programa |

Las etiquetas de esta tabla describen la planificación de celdas. No sustituyen el vocabulario de gates/veredictos por identidad del qualifier ni borran resultados históricos. El manager mantiene el estado confirmado por referencias; si no existe evidencia, declara UNKNOWN/NOT_EVALUATED en vez de inferir PASS.

### 5. Ampliación futura de instrumentos — PARKED_SCOPE

| Universo futuro | Investigación que podría justificar abrirlo | Dependencia previa |
|---|---|---|
| ES/MES, RTY/M2K, YM/MYM | Persistencia, reversión, apertura y relaciones entre índices | Decisión Owner, contratos/datos/costes propios y evidencia de que añade cobertura útil |
| CL/MCL y otros futuros de energía | Inventarios, estructura temporal, estacionalidad y sesiones | Datos/eventos/calendario, riesgo de gaps y reglas del programa seleccionado |
| GC/MGC y otros metales | Riesgo macro, relaciones intermarket, sesiones y carry | Datos y semántica de contrato/roll, costes y factibilidad de riesgo |
| Tipos de interés | Noticias macro, curva y valor relativo | Contratos, unidades, datos sincronizados y capacidad de ejecución aplicable |
| FX futures | Sesiones, macro, persistencia y relaciones de divisas | Contratos CME/datos propios; permanece en Futures, no se confunde con Forex/CFD de IMOX |
| Agrícolas y otros físicos | Oferta/demanda, estacionalidad y curva | Calendarios particulares, datos fundamentales y limitaciones de horizonte/prop |

No son proyectos creados ni un backlog de ejecución. Micro y mini no se validan multiplicando P&L: la geometría discreta, coste relativo y ejecución requieren su propia evidencia. No inferir permiso de overnight, multileg o instrumento por aparecer en esta tabla.

### 6. Uso de la matriz y diversidad demostrada

1. Vincular una idea a una celda existente o explicar por qué añade una pregunta no cubierta.
2. Buscar tesis/estrategias/señales equivalentes antes de abrir trabajo. Reutilizar catálogo, código y recibos válidos.
3. Expresar hipótesis, control, refutación, datos, costes y límite del experimento. Una fuente fiel no es prueba de ventaja; separar incertidumbre documental de incertidumbre de mercado.
4. Priorizar mediante una razón legible: relevancia económica para challenge/retiro, valor de información, diferencia respecto a lo ya sabido, posibilidad de refutar barato, datos/capacidades y dependencias. No fabricar puntuaciones precisas sin fundamento.
5. Despachar sólo el trabajo acotado aceptado. El estado operativo/WIP y las tareas viven en [[Echo I+D — Futures]], no duplicados aquí.
6. Integrar resultado positivo, negativo o inconcluso con identidad/versiones, datos observados y condición para reabrir. Conservar intentos y datos ya usados en selección; no llamar OOS virgen a una ventana que influyó en el diseño.

La diversidad se examina en cuatro capas: mecanismo/tesis, reglas, señales y exposición/pérdidas. Un nombre diferente sólo prueba un nombre distinto. Un mismo mecanismo puede aportar diversificación en ciertos contextos, pero debe medirse y declararse su límite. No promover estrategias por “llenar” celdas.

La eficacia de cobertura se observa sobre el **subconjunto priorizado y versionado**: preguntas resueltas, descartes útiles, bloqueos retirados, duplicados evitados y decisiones económicas sustentadas. No se mide un porcentaje de todo el universo posible ni se incentiva crecimiento de filas/documentos como resultado.

### 7. Siguiente trabajo: FUT-R01

**Mandato a preparar con el manager:** inventario NQ por identidad y recibos, cobertura efectiva, dependencia de runtime y propuesta de perfil económico inicial. Leer deltas de las autoridades y mapear TG/FBC/ORB/MR/ClutiFX sin repetir campañas. Proponer una primera investigación y una alternativa de mecanismo distinto, justificando aprendizaje esperado y coste; la selección material corresponde al Owner.

La salida debe dejar visibles: qué existe, qué está vigente/superseded/REVIEW, qué datos faltan, qué celda se informa, qué hipótesis se refuta, qué gates aplican y qué presupuesto necesita el siguiente mandato. **FUT-R01 no es un comando de ejecución, un permiso de backtest ni autorización de cuentas o producción.** La matriz no depende de que ClutiFX funcione.

## Fuentes

**Corte de auditoría:** `xKoRx/agents-os@81d4d6b00205855d223914f2c6d7ac70aebc5fa1`. Las referencias de esta sección documentan lo leído para planificar; no certifican estado físico actual del host. Decisiones de alcance: instrucción Owner del 2026-10-27, conservada en [[Echo — I+D de Estrategias]].

- [Optimización de Campañas — autoridad del laboratorio, contratos e identidades](https://github.com/xKoRx/agents-os/blob/81d4d6b00205855d223914f2c6d7ac70aebc5fa1/main/10-projects/Echo%20Futures/agentes/Echo%20Futures%20%E2%80%94%20Optimizaci%C3%B3n%20de%20Campa%C3%B1as.md).
- [Preflight Hefesto 2026-10-23 — corpus NQ 1m y límites de datos](https://github.com/xKoRx/agents-os/blob/81d4d6b00205855d223914f2c6d7ac70aebc5fa1/main/10-projects/Echo%20Futures/artifacts/clutifx-strategy-research/HEFESTO-BASELINE-AUDIT.md). Sus cifras de recursos y sus observaciones históricas no sustituyen política posterior ni preflight actual.
- [ClutiFX K05 — source certification](https://github.com/xKoRx/agents-os/blob/81d4d6b00205855d223914f2c6d7ac70aebc5fa1/main/10-projects/Echo%20Futures/artifacts/clutifx-strategy-research/k05/CLF-K05-SOURCE-CERTIFICATION.md) y [fixtures de conformidad](https://github.com/xKoRx/agents-os/blob/81d4d6b00205855d223914f2c6d7ac70aebc5fa1/main/10-projects/Echo%20Futures/artifacts/clutifx-strategy-research/k05/CLF-K05-FIXTURE-SPECIFICATIONS.md).
- [ClutiFX E05R1 — estado posterior a correcciones](https://github.com/xKoRx/agents-os/blob/81d4d6b00205855d223914f2c6d7ac70aebc5fa1/main/10-projects/Echo%20Futures/artifacts/clutifx-strategy-research/e05r1/CLF-E05R1-STATUS.md). Mantiene `OWNER_ACCEPTANCE: REVIEW`; no promover conclusiones previas superseded ni generalizar una muestra a la familia.
- [Perfil E2T histórico versionado](https://github.com/xKoRx/agents-os/blob/81d4d6b00205855d223914f2c6d7ac70aebc5fa1/main/10-projects/Echo%20Futures/artifacts/tradesgerard/TRADESGERARD-PROP-PROFILE.md): evidencia de simulación, no selección actual de proveedor/cuenta.
- Código relacionado inspeccionado en `xKoRx/echo@ae1b09bc10370806f7648f076c5fa0825c9efa4e`: [FBC](https://github.com/xKoRx/echo/blob/ae1b09bc10370806f7648f076c5fa0825c9efa4e/v3/sdk/futures/strategies/fbc/fbc.go), [ORB](https://github.com/xKoRx/echo/blob/ae1b09bc10370806f7648f076c5fa0825c9efa4e/v3/sdk/futures/strategies/orb/orb.go), [TG](https://github.com/xKoRx/echo/blob/ae1b09bc10370806f7648f076c5fa0825c9efa4e/v3/sdk/futures/strategies/tg/tg.go), [MR01–MR04](https://github.com/xKoRx/echo/blob/ae1b09bc10370806f7648f076c5fa0825c9efa4e/v3/sdk/futures/strategies/mr/variants.go), [MR05–MR09](https://github.com/xKoRx/echo/blob/ae1b09bc10370806f7648f076c5fa0825c9efa4e/v3/sdk/futures/strategies/mr/variants2.go). Esta lectura acredita existencia/semántica identificada, no rentabilidad, independencia ni cualificación actual.

Autoridad vigente de gates: [[30-resources/agents/skills/echo-retester-master/SKILL]] y [[30-resources/runbooks/echo-futures-strategy-qualification-runbook]]. Autoridad de ciclo y mejora metodológica: [[30-resources/runbooks/echo-rnd-cycle-runbook]].

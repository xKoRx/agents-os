---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[Echo — Live Platform V1]]"
  - "[[Echo Forge — Factory V2 Completion]]"
aliases: []
tags:
  - kind/doc
  - area/echo
created: "2026-09-22"
updated: "2026-09-22"
---

# A — Product Contract — The Lab

## Propósito

Propuesta de contrato de producto para Rodrigo Jara, 22-09-2026. Estado: **PROPUESTA PENDIENTE DE RATIFICACIÓN**. El mandato del owner ratifica los objetivos indicados abajo; las elecciones técnicas de esta nota no sustituyen contratos frozen ni autorizan código, despliegues o trading. Pertenece a [[Echo — Producto Integrado]] y a su discovery existente. Implementación seguirá en los dos tracks Live Platform y Forge Factory; The Lab no constituye un tercer producto.

## Contenido

### Resultado de producto y autoridad

The Lab reconstruye una historia seleccionada por StrategyVersion, preserva operaciones individuales y permite analizarla mediante N algoritmos reproducibles. Secuencia de autoridad: evidencia original → operaciones canónicas durables → selección de historia → curvas → métricas → screener/rankings → portfolios → asignación mediante Echo. Ninguna capa derivada reescribe hechos de una capa anterior.

**Ratificado por el mandato:** exactamente TRAINING_DATA, PRE_REAL y REAL; dos fronteras A/B; SQX y MT5 entregados por Forge con operaciones verificables; una historia oficial seleccionada; IS/OOS dentro del entrenamiento; Reference observada desde B y Execution separada; corrección manual auditable ante interrupciones; N curvas; calidad separada de sizing; UI temporal, operaciones, calendario y screener; portfolios como destino. Sin backtesting de velas, simulación intrabar ni recuperación histórica automática en esta iteración.

**Propuesto para ratificación:** reglas de frontera y selección siguientes; EVENT_TIME validado en históricos; modelo de revisiones; algoritmos y fórmulas versionadas; estados de disponibilidad; extensión de handoff; secuencia del roadmap. Sus decisiones numeradas están en [[F — Decision Register]].

### Una historia publicada, no una historia inmutable para siempre

Cada StrategyVersion tiene una sola revisión publicada de historia analítica. Puede tener revisiones anteriores retenidas para auditoría y candidatos sin publicar. El puntero publicado se cambia explícitamente y nunca hay dos revisiones vigentes para la misma versión. Todas las consultas pinnean la revisión; una página no combina la curva de una revisión con métricas de otra.

Identidad de estrategia, StrategyVersion, versión de datos y cuenta son conceptos distintos. Mover la Reference de cuenta crea un binding con su intervalo y conserva la misma versión si reglas/código/parámetros efectivos no cambian. Un cambio de reglas o ejecutable requiere la clasificación de versión existente; un cambio de sizing se identifica por su política. No se asignan trades históricos de un ejecutable a otro para llenar huecos.

La vista inicial exige seleccionar una StrategyVersion. La futura vista longitudinal de la estrategia será una proyección identificada de versiones e intervalos, con miembros explícitos y fronteras visibles; no será una fusión anónima. Cada versión conserva su propio par A/B. No se introduce una cuarta etapa para una nueva versión.

### Dos fechas y tres períodos

Todas las fronteras se guardan como instantes UTC; la UI puede mostrarlas en America/Santiago junto con el timezone. La pertenencia se determina por **closed_at_event validado** de la operación completa:

| Período | Intervalo | Fuente seleccionada por defecto |
|---|---|---|
| TRAINING_DATA | t < A | TradeSet SQX final elegido, correspondiente a la versión y resultado correctos |
| PRE_REAL | A ≤ t < B | TradeSet MT5 de la misma versión, posterior al corte de entrenamiento |
| REAL | B ≤ t | Reference realmente observada por Echo, con binding y cobertura demostrados |

A es el primer instante posterior a **todo dato utilizado para generar, ajustar o seleccionar** esa versión, no el inicio de un OOS al que ya se miró para elegir finalistas. B es el inicio autorizado y demostrado de observación de esa versión por Reference; no es fecha de promoción, POST ni creación de una cuenta. A debe poder reconstruirse desde datos/configuración de investigación. B puede permanecer PENDING antes de observar: se representa como ausencia explícita, sin inventar fecha futura; PRE_REAL queda abierto hasta el as_of y REAL aparece «aún no iniciado». Si A no está probado, no se publica una partición oficial: se permite inspección de fuentes como evidencia provisional.

Propuesta semántica a ratificar: REAL significa **operativa observada**, incluyendo una Reference DEMO; el campo de entorno DEMO/REAL es obligatorio y visible. No presentar DEMO como dinero real. Si el owner reserva REAL exclusivamente a dinero real, hay que resolver primero dónde vive la observación DEMO sin romper los tres períodos del mandato.

Operación que abre antes de A/B y cierra después: se conserva completa y pertenece al intervalo de cierre. No se inventan una salida o un reparto de PnL en la frontera. La fuente designada para el intervalo debe demostrar el OPEN original, su riesgo y el cierre; el replay puede incluir warmup anterior a A. Un binding nuevo no presume observar una posición que nunca identificó. Las abiertas se muestran aparte y no entran en curvas de resultados cerrados hasta su cierre. Saldo realizado no equivale a equity marcada a mercado.

IS/OOS/WFM son anotaciones identificadas por evaluación/configuración/rango dentro de TRAINING_DATA. OOS no es sinónimo de PRE_REAL. Un replay MT5 retrospectivo posterior a A es validación histórica, no evidencia de que la selección se hubiera decidido prospectivamente.

### Selección, overlap y correcciones

1. Validar versión, scope, símbolo normalizado y especificación del instrumento, timezone, artefactos y contenido. La ausencia de estos datos no se cura cambiando labels.
2. Seleccionar un set autorizado por fuente/período en el manifiesto de historia. Cortar con intervalos semiabiertos. Los otros sets siguen siendo evidencia inspeccionable, sin sumar sus operaciones a la historia.
3. Dedupe dentro del origen mediante OperationRef estable; revisiones del mismo hecho se distinguen por record_digest. Misma referencia y contenido diferente sin cadena de corrección = conflicto.
4. Entre fuentes, sólo afirmar equivalencia de evento si existe prueba de la misma identidad económica: servidor/cuenta/registro de broker/deal o mapeo explícito validado. SQX y un backtest MT5 pueden producir caminos distintos; proximidad temporal y PnL similar no prueban equivalencia. La selección exclusiva por período evita concatenarlos; no fabrica un pareo.
5. En REAL, un cambio de Reference exige bindings no superpuestos o autoridad explícita para el overlap. Un evento observado por dos collectors conserva una sola selección. Execution continúa como serie por cuenta y no rellena Reference.
6. Una corrección manual aporta evidencia original, actor, motivo, supersedes y revisión nueva. Se recalculan derivados; la revisión anterior sigue resoluble. Un hueco de observación se representa como desconocido, nunca como días de retorno cero.

La publicación exige ausencia de conflictos de identidad en los miembros seleccionados. Cobertura parcial conocida puede publicarse con cortes y huecos visibles, pero bloquea algoritmos o métricas que requieren completitud. No todo dato incompleto impide consultar trades; sí impide afirmar comparabilidad donde falta la prueba.

### Curvas y significado económico

Cada CurveRun fija operaciones exactas, revisión, período/ventana, algoritmo y versión, configuración, basis/unidades, especificaciones y as_of. Se puede recalcular otra configuración sin reimportar operaciones. Reproducir la misma pregunta produce el mismo resultado y digest; un resultado distinto no sobrescribe uno anterior.

| Familia | Pregunta | Límite |
|---|---|---|
| Acumulado R | Resultado por riesgo inicial demostrado | Riesgo cero/desconocido → insuficiente; no SL final |
| Acumulado pips o ticks declarados | Movimiento capturado en un instrumento | No comparar unidades de activos diferentes como si fueran retorno |
| Capital virtual normalizado | Transformación de resultados con riesgo estándar | Política identificada; no depende del lotaje real cuando pretende normalizar |
| Capital por política de sizing | Contrafactual de tamaño sobre el mismo camino de trades | Concurrencia y costos explícitos; sin entradas/salidas alternativas |
| PnL/capital observado de cuenta | Impacto económico efectivamente observado | Incluye sizing, costos y flujos; no es ranking de calidad |

R no demuestra independencia matemática total de la gestión: el stop que define riesgo también es parte de la estrategia, los costos y restricciones pueden depender del tamaño. Preservar señal original, observación, riesgo inicial, política aplicada y escenario contrafactual como identidades distintas. Cambiar stop/trailing/entrada/salida necesita información de camino y un futuro simulador; los resultados finales no bastan.

### Métricas, screener y ranking

Las métricas fijan key+basis+unit+formula/version, CurveRun, ventana, frecuencia, costos, muestra y política de datos faltantes. La UI muestra cobertura, motivos de insuficiencia y procedencia. Nunca NULL→0; ningún ranking mezcla pips, R, USD y porcentaje sin receta declarada.

Primer screener: estrategia/versión, período, algoritmo/configuración, rango común, filtros y ordenamiento de métricas comparables. Un ordenamiento persistido se identifica mediante contrato Ranking existente y sus inputs; Score sólo si hay receta explícita. No inventar pesos «científicos» ni umbral de rentabilidad. Ranking de Forge = selección de fabricación; ranking de Lab = consulta analítica; elegibilidad y asignación = decisiones separadas. Se puede analizar un finalista perdedor sin habilitarlo para operar.

### Experiencia mínima verificable

Seleccionar versión → ver fuentes y estado → historia con A/B y tres franjas → escoger normalización → curva con eje temporal real → métricas → drilldown a operaciones → calendario de trades → screener con ordenamiento reproducible. Deben verse cambios de cuenta/versión, creación/promoción, inicio observado y gaps. Eventos macro sólo con fuente y fecha verificadas; son contexto, no causalidad automática. Sin feed macro no se bloquea este producto.

La curva inicial es de resultados realizados, con punto inicial y saltos de cierre; no suavizar inventando excursiones entre trades. El calendario distingue «cobertura completa sin cierres» de «sin observación». Permitir TRAINING_DATA/PRE_REAL/REAL y vista de toda la historia; métricas de período se recalculan en su ventana, no promedian métricas de subperíodos.

**Primer hito:** una estrategia auténtica y correctamente atribuida entrega ambos históricos, incluye datos PRE_REAL reales del replay posterior a A, publica su selección, produce al menos una curva normalizada soportada con métricas verificables, trades, calendario y screener. REAL puede estar pendiente. Recibir dos archivos superpuestos o mostrar todos los algoritmos como insuficientes no completa el hito.

### Endgame compatible

PortfolioVersion conserva miembros StrategyVersion/HistoryRevision/CurveRun, pesos, restricciones y policy refs. Correlaciones requieren grilla temporal común y cobertura; pesos y rebalanceos tienen vigencia. Su curva se calcula sobre contribuciones sincronizadas, no como promedio de DD individuales. Assignment a cuenta es otro objeto con autorización y ejecución E-08/E-09/E-12, seguimiento y retiro explícitos. Nada en una consulta o ranking activa trading.

## Fuentes

Mandato del owner de 22-09-2026; [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]; [[Echo SDK — Canonical Contract Final Freeze Review — Fable 5.1]]; [[Echo — Live Platform V1]]; [[Echo Forge — Factory V2 Completion]]. Evidencia física y contradicciones: [[C — Reality and Gap Matrix]]. Arquitectura: [[B — Architecture Decision Report]]. Implementación propuesta: [[D — Revised Roadmap]] y [[E — First Usable Vertical Slice]].

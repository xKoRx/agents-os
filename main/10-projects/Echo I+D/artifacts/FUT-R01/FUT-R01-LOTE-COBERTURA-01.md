---
type: doc
schema_version: 1
status: active
area: "[[Trading]]"
project: "[[Echo I+D — Futures]]"
related:
  - "[[Echo I+D — Cobertura Futures]]"
  - "[[FUT-R01-I01-SPEC]]"
  - "[[FUT-R01-I01-CONTRATOS]]"
  - "[[FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION]]"
  - "[[Echo Futures — Optimización de Campañas]]"
aliases:
  - "FUT-R01 lote de cobertura 01"
tags:
  - kind/doc
  - area/trading
  - project/echo-rnd
created: "2026-10-29"
updated: "2026-10-29"
---

# FUT-R01 — Lote de cobertura 01 y recepción I01-A/B

## Propósito

Convertir la investigación recibida y S04 en un lote comparativo finito, con preguntas de mercado y coste progresivo. La recomendación es **8 señales base —7 existentes y 1 nueva—, agrupadas en 6 preguntas, con un techo propuesto de 24 versiones de Strategy**. La primera entrega prepara una baseline por señal; no existe obligación de llenar las 24 ni de ejecutar todas las combinaciones.

**Estado:** propuesta del manager, **OWNER_ACCEPTANCE: REVIEW**. Preparación documental terminada; ejecución **NOT_DISPATCHED**. No declara specs ejecutables aceptadas, conformidad física, nuevas pruebas, rentabilidad ni independencia. FUT-R01 conserva el trabajo activo y [[Echo I+D — Futures]] su único planner. Este documento no abre seis iniciativas WIP ni sustituye el planner técnico de C.

**Corte de lectura:** Agents-OS master 5fe399572e640fd632bd8b25d745dbb3f0c2947c; Echo master 2baf319ddcba622d9557bc9f23a13787b44c58a7. Fecha de consolidación 29-10-2026 UTC; entradas I01-A/B fechadas 28-10-2026. Se usaron tres workers acotados de lectura: revisión A/B, cobertura y catálogo/coste S04. Sus análisis no son certificación técnica ni revisión históricamente independiente.

## Contenido

### 1. Decisión recomendada y qué no hace falta esperar

Empezar la preparación técnica por **FBC 15m + ORB 30m + MR04**: dirección de la primera vela, ruptura confirmada del rango y recuperación tras ruptura fallida. Es una pregunta de cobertura concreta sobre persistencia y fracaso en la apertura. Comparte calendario, barras y rangos, y reutiliza señales existentes.

Adelantar en paralelo la reconciliación documental de todas las ocho bases y la reparación focal de A/B. Después de medir coste y obtener las decisiones del primer paquete, abordar MR01/MR06/MR09/MR08. I01-A se prepara como una única baseline exploratoria, sin ser dependencia de las otras siete.

Las condiciones necesarias son diferentes según el trabajo:

| Trabajo | Entrada indispensable |
|---|---|
| Clasificar cobertura y comparar reglas | Fuente, predicados efectivos, identidades y evidencia disponible |
| Cerrar especificación y casos | Regla determinista, causalidad, unidades, disponibilidad de datos y semántica de órdenes |
| Valorar una campaña contra una prop | RuleSet por etapa/cohorte, enforcement, costes, payout, horizonte y modelo de ejecución declarados |
| Operar o certificar integración | Ruta real de órdenes, permisos, datos, pruebas físicas y aceptación de los owners correspondientes |

La ruta comercial pendiente no impide clasificar mecanismos. Tampoco puede sustituirse una incógnita material del contrato por un supuesto oculto para declarar viable la campaña.

### 2. Recepción y adjudicación focal I01-A/B

| Entrada | Dictamen del manager | Próximo cambio mínimo |
|---|---|---|
| I01-A — persistencia de cierre | Útil como hipótesis y ficha candidata; **LISTA_PARA_REVISION_DE_SPEC** se recibe, sin aceptación ejecutable. Su señal está definida; la geometría 1R es hipótesis propia, no conclusión del paper. | Resolver market/fill fuera del bracket y fill tardío. Conservar una sola baseline inicial. |
| I01-B — Rapid EOD 50K | **PARTIAL_DOCUMENTAL** reutilizable; no selección comercial ni certificación Echo. A ya está disponible: se resuelve la antigua dependencia documental de recepción, no los demás bloqueos. | Corregir dos inferencias y cerrar sólo los UNKNOWN materiales para la etapa que se pretenda valorar. |
| RV-01 | **NO_APTO_AUN** para una campaña contractual definida y reproducible. | Se mantiene por alcance; no exige rehacer DR-01–04 ni prohíbe preparar el lote. |

**A — reparación material de ejecución.** Una intención market puede tener un veto ANTES de enviarse si éste usa información causal disponible. Un fill ya ocurrido fuera de S/T, o después de solicitar cancelación por expiración, debe permanecer en la evidencia. Definir su tratamiento mediante Operation/MM/ejecución vigentes; no borrarlo retrospectivamente ni mover niveles para salvarlo. Si se quiere una entrada limitada por precio, eso requiere una regla explícita distinta. La repair debe aclarar el contrato y sus casos, no optimizar la geometría.

**B — cinco estrategias no equivalen a cinco cuentas.** La meta Owner es cinco estrategias challenge y cinco funded con retiros —pueden coincidir— en al menos dos firmas. El límite documental de tres SIM funded Rapid EOD no demuestra por sí solo incompatibilidad con cinco estrategias. Conservar el límite de cuentas; la asignación, rotación y simultaneidad pertenecen al diseño de C y al RuleSet.

**B — conflicto 3/4 contratos no acreditado por fase.** La ayuda específica indica tres minis en SIM; la tabla comercial extraída contiene 3/30 junto a lock +100 y 4/40 junto a floor 0, con categorías Evaluation, Sim Funded, Live y Payouts. La extracción aplanada no atribuye inequívocamente la segunda fila. Reconciliar fase antes de mantener una contradicción SIM confirmada. No adoptar cuatro contratos ni afirmar sin evidencia que la fila pertenece a LIVE.

**Precisión científica A.** Su contraste de precio contra ALWAYS_LONG tiene Z = sign(r_ROD) × r_LH − r_LH: Z es cero cuando el predictor es positivo y −2 × r_LH cuando es negativo. Es un contraste específico sobre invertir a short; no prueba por sí solo ambas direcciones de persistencia. Conservar resultados por signo y de la regla completa. No usar ese único contraste para descartar todo el mecanismo.

**Geometría y prop son preguntas diferentes.** En A, D = |P15:30 − cierre previo| fija SL y TP. Medir distribución de D, oportunidades, invalidaciones, relación con headroom y causas efectivas de salida. Que el stop técnico quede más allá de una barrera prop no es por sí solo un veto prudencial autorizado: importa la admisión real y el evento que termine exposición. Tampoco demuestra utilidad. Los datos M1 permiten ciertos análisis de referencias/retornos; no identifican toda secuencia de fills, stops, targets o enforcement.

### 3. Qué recuperamos de S04

El catálogo vigente enumera **26 configuraciones nativas**: 4 TG, 4 FBC, 3 ORB-CH300, 10 MR y 5 ORB-NATIVE. Su derivación SG produce 78 filas declaradas; elimina 15 alias de identidad tras normalizar ADD; quedan **63 SG únicas y 89 jobs en total**.

Los presupuestos históricos SG 250/500/750 y ATR14 × 1, RR 1:1 pertenecen a esas identidades. No son el nuevo MM-MAX ni límites universales. Un cambio de MM no es una nueva señal; cambiar stop/target técnico sí cambia la configuración de Strategy. El nombre histórico SG no altera esa separación conceptual.

R03 registra **89/89 COMPLETE_RECONCILED**, 3.037 compras y 328 pases simulados bajo su contexto histórico, con OWNER_ACCEPTANCE=REVIEW. Es evidencia que se recupera, no se vuelve a producir porque pertenezca a otra sesión. El 10,8% agregado no estima una tasa futura bajo otro MM, RuleSet o runtime.

Antecedentes para priorizar la lectura, sin ordenar ganadoras:

| Identidad histórica | Compras → pases simulados | Uso permitido ahora |
|---|---:|---|
| LAB-SG-MR-09-R750 | 13 → 5 | Revisar señal, exposición, geometría y causalidad del resultado |
| LAB-SG-FBC-CH300-15M-R750 | 43 → 11 | Baseline histórica de apertura para comparación trazable |
| LAB-SG-MR-06-R750 | 5 → 2 | **EVIDENCE_LIMITED**; cinco compras no estiman una probabilidad robusta |
| LAB-SG-ORB-CH300-30M-R750 | 58 → 10 | Referencia de ruptura de apertura bajo esa combinación exacta |
| LAB-SG-MR-04-R750 | 44 → 8 | Contraste de ruptura fallida; no cumple el nuevo umbral Owner en esa observación |
| LAB-SG-MR-01-R750 | 31 → 4 | Se incluye por la pregunta de valor/VWAP, no por liderazgo económico histórico |
| LAB-SG-MR-08-R500 | 29 → 2 | Prioridad física menor: antecedente débil; exige aporte incremental antes de más cómputo |

La apertura encabeza la preparación por reutilización y comparación interpretable, no por ser la ganadora del ranking. MR01/MR08 no reciben por cobertura un derecho a históricos caros; pueden quedar aparcadas al revisar evidencia existente. Estas cifras ya influyen en la prioridad de recuperación: sus periodos no son OOS virgen. No se transfieren a nativas, nuevas geometrías o MM-MAX.

La integración S04 está acreditada como **SOURCE** en el corte consultado. C04 conserva **S04_SEMANTIC_ACCEPTANCE: BLOCKED_EVIDENCE**, con planes efectivos/receipts F01/F02 pendientes. I0 figura NOT_STARTED / NOT_DISPATCHED al corte; el Owner informa continuidad del manager C. La lectura no certifica Hefesto, build ni equivalencia semántica de todas las variantes.

### 4. Ocho bases y seis preguntas de cobertura

Las filas son preguntas de investigación. PERSIST/REVERT son mecanismos amplios; OPEN/SESSION/FAILED aportan contextos o subtesis. No se declaran seis fuentes independientes de alpha.

| Pregunta / celda | Base propuesta y fuente | Qué se pone a prueba | Refutador o límite de utilidad |
|---|---|---|---|
| Persistencia de apertura — PERSIST × OPEN | **FBC 15m**, FBC-CH300-15M; **ORB 30m**, ORB-CH300-30M, contrastando identidad con ORB-NATIVE-C03 | Seguir color de primera vela frente a esperar cierre M1 fuera del rango. FBC no exige breakout. | Redundancia de señales/pérdidas; diferencia explicada por tiempo/geometría; coste o reglas que eliminen utilidad económica |
| Recuperación local con tendencia — REVERT condicionada a PERSIST | **MR08**, MR-08 | Contexto EMA20/50 H1 y recuperación del pullback M5 hacia EMA20 | Contexto sin aporte incremental; causalidad/warm-up defectuosos; mismas pérdidas que apertura; frecuencia insuficiente para el horizonte declarado |
| Fracaso de ruptura — REVERT × FAILED × OPEN | **MR04**, MR-04 | Intento fuera del rango inicial de 30m y recuperación interior, con referencia central | La confirmación no discrimina conducta; poco recorrido después de costes; duplicidad con otra reversión |
| Reversión de exceso — REVERT | **MR01**, MR-01; **MR06**, MR-06 | Extensión/reclaim respecto de VWAP frente a shock de rango M1 y confirmación contraria hacia EMA20 | Persistencia posterior al exceso; reversión insuficiente antes de salida; diferencia dominada por geometría o ejecución no observable |
| Gap y referencia anterior — REVERT × SESSION × OPEN | **MR09**, MR-09 | Gap/empuje inicial y recuperación hacia cierre RTH anterior | La referencia no aporta frente al control; concentración en pocas sesiones; roll/calendario invalida la señal |
| Persistencia de cierre — PERSIST, contexto de cierre | **I01-A**, FUT-NQ-PERSIST-ROD1530-V1, nueva | Signo del retorno desde cierre previo a 15:30 para el tramo final, con bracket propio | Efecto de precio no transferible a geometría/costes; admisión o barrera prop domina; sin aporte incremental; ejecución insuficientemente observable |

**No hay ocho recetas económicas ya congeladas.** Hay ocho señales seleccionadas para preparar el lote. La baseline de cada una debe fijar setup, filtro y geometría técnica con versión, separando el MM heredado. Donde la lógica antigua repartía salidas entre Strategy y MM, reconciliar el predicado y su owner; no atribuir silenciosamente el resultado de una combinación a otra.

En MR, una referencia objetivo congelada puede comprobarse en un cierre posterior de barra; no convertirla automáticamente en una orden limit intrabar. Se conserva el modo efectivo y se registra como nueva variante cualquier cambio de ejecución.

### 5. Secuencia de paquetes y trabajo compartido

**Recuperación previa, sin motor nuevo:** mapear las 89 filas por setup, geometría, MM, fuente y receipt; identificar qué permanece válido después del merge. El alcance amplio es lectura/clasificación, no 89 nuevas cualificaciones.

**Paquete 1 — apertura:** FBC15 + ORB30 + MR04. Primera entrega: tres baselines reconciliadas y su comparación. ORB y MR04 no son controles perfectamente emparejados: un mismo día puede romper y después recuperar. Conservar ambos eventos, no hacerlos artificialmente excluyentes. FBC cambia también instante y exposición; no atribuir toda diferencia de PnL a “persistencia frente a fracaso”.

**Paquete 2 — reversión y contexto:** MR09 + MR06, seguidas de MR01 + MR08 si su revisión justifica el coste. MR09/MR06 se recuperan documentalmente desde el principio; posponer su motor no es descarte económico. Agrupar implementación y casos por componentes compartidos, conservando decisiones por señal.

**Paquete 3 — nueva señal de cierre:** I01-A después de la reparación y la comprobación de datos. Puede prepararse en paralelo. Inicialmente una sola baseline, sin parrilla de horarios × RR × filtros.

Se comparten calendario/DST, rangos, referencias, indicadores causales, fixtures, corpus y analytics donde corresponda. El comportamiento dependiente de cuenta/MM puede alterar decisiones y estado: no se reutilizan fills ni se multiplican curvas como si fueran equivalentes. El alcance exacto de compartir un pase del motor requiere conformidad técnica, no se presume por el uso del mismo dataset.

### 6. Alternativas con sentido y cardinalidad

| Nivel | Cantidad propuesta | Condición |
|---|---:|---|
| Señales base | 8 | Siete existentes; una nueva |
| Primera preparación | 8 baselines | Primero tres del paquete de apertura |
| Versiones de Strategy del lote | **Hasta 24** | Techo total, no cuota; cada alternativa debe justificar qué pregunta añade |
| MM por etapa | Hasta 2 | CTRL 1 NQ y MAX entero admisible, propuestos en B, una vez congelada admisión |
| Cruces máximos de diseño | Hasta 48 por etapa | Sólo si llegaran las 24 y ambos MM; no son 48 jobs aprobados ni 96 históricos obligatorios |
| Props / etapas | Ampliación progresiva | Un perfil cerrado para el contraste inicial; segundo proveedor después de una comparación interpretable |

Una base puede originar hasta dos ramas simples:

- **Rama de salida/geometría:** mantiene señal/filtro y prueba una realización del movimiento identificada; por ejemplo, objetivo de referencia frente a RR fijado antes de la evaluación.
- **Rama de filtro/contexto:** mantiene geometría y pregunta por el aporte incremental de una condición causal.

Se comparan por separado contra la baseline. No cruzar automáticamente salida × filtro × horario × umbral × MM × prop. Las interacciones se abren sólo si el contraste deja una pregunta concreta, dentro del presupuesto aceptado.

**RR no es una parrilla universal.** Un target VWAP, centro del rango o cierre previo expresa una hipótesis distinta de 0,5R/1R/2R. Esos valores sólo podrían ser alternativas explícitas después de justificar su uso y declarar la selección; no se prescriben a las ocho bases. Cambiar SL/TP es nueva configuración de Strategy, no un ajuste invisible de MM.

El techo 24 permite iteraciones posteriores; no afirma que ya existan dieciséis alternativas justificadas. I01-A empieza con una, y sólo abriría otra rama después de resolver una pregunta de esa baseline.

MAX se estudia como política alineada con resolución rápida; CTRL permite medir su contribución. El máximo contractual no se declara óptimo por definición. El umbral 1/3 es criterio Owner para las campañas futuras, no media del mercado, estimación previa ni gate científico universal.

### 7. Métricas para decidir por etapa y por cobertura

Una fila de evidencia conserva Strategy/variante/params + MM + Provider/Program/RuleSet/etapa + datos/ventana/build/modelo de ejecución + receipt. Una señal, una cuenta, un intento y una compra no son el mismo denominador.

**Diagnóstico de oportunidades:** sesiones elegibles, datos inválidos, señales LONG/SHORT, horarios, distancias de stop/objetivo, duración, invalidaciones, vetos causales por MM/proveedor y causa de salida. Separar señal que no aparece de señal rechazada y de orden sin fill. MAE/MFE o secuencia intrabar sólo al nivel que el dato permite.

**Challenge:** pase, pérdida y pendientes, tiempo hasta resolución, compras/intentos/reset, coste agregado por pase, costes y restricciones activas. Una compra de cero pases no se divide silenciosamente por cero; el resultado conserva el coste y su condición. No eliminar cuentas abiertas al corte para mejorar el ratio.

**Funded:** cash neto recibido por todas las cuentas iniciadas, incluidas quemadas y las que no retiraron; distribución/tiempo a cobro; costes posteriores y estado pendiente. La comparación con coste de adquisición usa cohortes y activaciones consistentes, sin restar el mismo coste dos veces. El monto/tiempo del retiro es una política a comparar, no USD 3.000 fijados.

**Cartera:** oportunidades y posiciones simultáneas, dirección común, pérdidas y drawdowns coincidentes, PnL normalizado con método predeclarado y regímenes comunes, frecuencia y sesiones sin actividad. Usar un calendario elegible común: cero sólo cuando hay evidencia de no operar, no cuando faltan datos. Reportar diferencias de soporte y exposición, no sólo una correlación total.

Los resultados económicos separados no autorizan multiplicar tasa de pase por payout medio como prueba de caja. La trayectoria completa corresponde a SIMULATION, con funded condicionada, compras, retrasos, límites de cuenta y bankroll compartido de USD 4.000.

### 8. Embudo de coste, sin relajar G0–G5

1. **Reconciliar antes de ejecutar.** Leer catálogo, resultados y trazas existentes; deduplicar identidades demostradas; distinguir reutilizable, cambio semántico, ausente y desconocido. El merge no hace vigentes todos los receipts automáticamente.
2. **Cerrar ficha/casos y observabilidad.** Datos, calendario, versiones, primer predicado material y semántica de salida. Resolver contradicciones antes de implementar. Rechazar una entrada inválida evita un histórico inútil.
3. **G0/G1 → G2A/B/C → G3 por identidad.** Compartir preparación y fixtures; cada identidad ejecutable conserva G2C propio con round-trip ejecutado por el motor y conciliado. Ventanas cortas técnicas no son evaluaciones económicas completas.
4. **G4 únicamente con admisión completa.** Un contrato físico trimestral calificado, mínimo vigente de 45 sesiones elegibles; completar toda la ventana, sin detenerse al primer pase. Una aprobación es filtro de gasto de cómputo, no robustez ni probabilidad futura.
5. **G5 sólo para promovidas con recibos propios.** Preservar ventanas ya usadas en selección, correcciones y todos los intentos. No etiquetar como OOS virgen el histórico que ya orientó S04, esta selección o sus alternativas.

La discrepancia entre admisión funded-only y el G4 challenge vigente pertenece a la decisión focal D05 de C. Este lote no crea un waiver ni usa “screening” para disfrazar un histórico multicontrato.

**Herramientas existentes, alcance real:** plan/derive/prepare enumeran y materializan; characterize reconstruye datos de resultados/trazas existentes, no escanea señales nuevas sobre todo el mercado. search propone refinamientos; project es diagnóstico y su tape SESSION_BLOCKS sólo incluye días con trades y resultados a cierre. No certifica path intrabar, pase o caja. resume conserva trabajos terminados compatibles y genera retry para parciales: no es checkpoint intrabar.

En el runner leído, max-runs limita lanzamientos; _run_one usa subprocess.run sin timeout ni guard de cualificación visible. La autoridad exige ese guard. El manager C debe resolverlo por su superficie antes de admisión nueva; no se asume implementado por esta propuesta.

**Presupuesto que debe volver antes del dispatch físico:**

- Identidades y ventanas congeladas; máximo de nuevos jobs e intentos.
- Engine-minutes acumulados y wall time del paquete; límite por job.
- Capacidad real de Hefesto y concurrencia autorizada. Techo vigente global de seis motores incluidos oráculos, no permiso automático de usar seis.
- Cancelación/drenado con preservación de parciales y registro de motivo; reserva explícita para reparación acotada.
- Coste medido de una ventana corta representativa ya autorizada, reutilizando recibos comparables si existen; no calibración abierta ni un benchmark heredado tratado como actual.

No se promete una duración fija: la fuente no acredita throughput del corte integrado. Una interrupción por tiempo o presupuesto es INCOMPLETE/BUDGET_EXHAUSTED, no refutación, pérdida de cuenta ni QUARTER_NO_PASS inventado. Si se agota el presupuesto, devolver evidencia y coste antes de ampliarlo.

### 9. Backlog corto y activación por aprendizaje

| Reserva | Condición que justificaría abrirla |
|---|---|
| MR02 — Bollinger Failed Continuation | MR04 deja una pregunta sobre fracaso de ruptura fuera de la apertura |
| MR07 — Established Range Edge Fade | Hay necesidad de separar rechazo del borde de un rango establecido y recuperación posterior a ruptura |
| MR10 — Directional Sequence Exhaustion | MR06 deja abierta la diferencia entre shock de una barra y secuencia de cierres con contracción |
| TG SIG-B | Sus receipts aportan contraste barato o posible señal incremental frente a excesos VWAP/shock |
| MR05 — Opening Drive Rejection | Sólo tras reconciliar descartes/versiones previas y formular hipótesis distinta; cambiar MM no borra un descarte de señal |

MR03 queda inventariada, sin prioridad en este lote. ClutiFX permanece fuera de nuevas investigaciones. Intermarket, noticias como evento identificado y order flow esperan datos/alcance pertinentes; no se abre otro instrumento ni MNQ. Un shock de precio MR06 no equivale a una estrategia de noticias macro.

Una rama cerrada devuelve resultado —incluido duplicidad, datos insuficientes, defecto o refutación— y habilita escoger la siguiente reserva. No se activa toda la cola ni se crean managers permanentes nuevos.

### 10. Mandato siguiente preparado: LC01-PREP, ONE-SHOT documental

**Pregunta:** ¿cuáles de las ocho bases pueden entregarse al manager técnico como identidades inequívocas, con receipts reutilizables, reparaciones acotadas y coste físico presupuestable, empezando por FBC15/ORB30/MR04?

**Autoridad:** bootstrap canónico sólo al inicio cold; master de Agents-OS sin ramas/PRs; planner Futures, esta propuesta, cobertura, ciclo R&D, echo-retester-master y runbook de cualificación. C conserva su manager, planner y contratos aceptados. No cambiar gates, producto, RuleSet, MM material ni selección Owner.

**Entradas:** las ocho bases enumeradas; catálogo/manifiestos y receipts S04 actuales; A/B originales y esta adjudicación; corte C04 o sucesor vigente. Usar primero lo disponible; no pedir un nuevo preflight por inercia ni reconstruir originales ausentes.

**Entregables:** una tabla compacta por base con regla efectiva en tres bloques, geometría/MM separados, versión/build, datos/receipts, equivalencias demostradas, primera dependencia material y próxima acción. Primer paquete de tres baselines aptas para revisión o bloqueo preciso; mapa de invalidación/reutilización. Propuesta finita de alternativas sólo donde haya pregunta. Requisito de presupuesto concreto y guard para C, sin invadir su implementación.

**Presupuesto propuesto:** un ONE-SHOT Cloud, sin motor ni SSH ni campañas; máximo ocho fichas baseline y las tres reparaciones A/B de §2. Reutilizar el censo publicado de 89 y consultar sus registros; si los blobs físicos imprescindibles no están accesibles, emitir un mandato read-only a Hefesto que pida sólo esas rutas/identidades. No despachar ese acceso desde Cloud sin la autorización correspondiente. Ningún histórico ni refactor por efecto lateral.

**Refutador/gates:** una base no es READY por su nombre o por otro receipt. Causalidad, identidad y semántica deben ser trazables; UNKNOWN se conserva. Datos incompletos, equivalencia no demostrada o especificación material ambigua impiden congelarla. Cumplir el alcance documental no equivale a G0–G5 PASS.

**Condición de parada:** tabla completa o dependencia indispensable localizada; no bucles de investigación. Una reparación adicional que amplíe señal, instrumento, contrato o presupuesto retorna al manager.

**Retorno:** READY_FOR_SPEC_REVIEW / PARTIAL_WITH_EXACT_BLOCKERS, evidencias/path/hash, deltas, coste pendiente, próximas tres acciones y archivos canónicos publicados/verificados si el despacho incluye publicación. No cerrar el programa, ni hacer cierre completo/feedback del manager. Este mandato está preparado, no ejecutado ni autorizado para motores.

### 11. Decisiones que siguen abiertas

1. Aceptación Owner del alcance **8 bases / techo 24**, con primer paquete FBC15/ORB30/MR04. Es propuesta de gestión, no resultado estadístico ni cuota de ganadoras.
2. Freeze de las recetas efectivas, dos MM por etapa y primer RuleSet evaluable; monto/tiempo de payout se estudia como política finita.
3. Budget/ventana/capacidad y autorización del primer dispatch físico, tras el retorno técnico correspondiente.
4. Selección del segundo proveedor y ampliación multicuentas/portfolio, sin confundir preparación de señales con certificación comercial.

No se reabren capital, reinversión, retiro fijo, autonomía general, meta 5+5 ni los cuatro DR. La disponibilidad personal del Owner no acredita capacidad de Hefesto.

## Fuentes

- Instrucción Owner: recepción I01-A/B, continuidad de C con su manager y solicitud de lote con cobertura, sentido, variantes y coste acotado; contexto previo de USD 4.000, MM agresivo dentro de reglas, retiro variable y Strategy/MM separados.
- [[FUT-R01-I01-SPEC]]: commit 281cb003fa89ac1cc2ce369262d193aef83ec037; blob leído 1c2069fea46e98f736c4534889ceb218d3f35645.
- [[FUT-R01-I01-CONTRATOS]]: commit 5dd2eff729bcc881bd2698ce3e14c75de3225704; blob leído 37f5ff5c30d73d4b3905caf0423f8640e29098f8.
- [[FUT-R01-RV-01-CONSOLIDADO]], [[FUT-R01-INDICE]], [[Echo I+D — Cobertura Futures]], [[Echo I+D — Futures]]; DR-03/04 leídos con sus adjudicaciones, no adoptados como recetas aceptadas.
- [Catálogo S04](https://github.com/xKoRx/echo/blob/2baf319ddcba622d9557bc9f23a13787b44c58a7/v3/backtester/tools/tradesgerard/campaign-lab/catalog-v1.json), [runner y herramientas](https://github.com/xKoRx/echo/blob/2baf319ddcba622d9557bc9f23a13787b44c58a7/v3/backtester/tools/tradesgerard/campaign-lab/research_lab.py), [R03-STATUS](https://github.com/xKoRx/echo/blob/2baf319ddcba622d9557bc9f23a13787b44c58a7/v3/backtester/tools/tradesgerard/campaign-lab/correction/s04/lab-r03/R03-STATUS.md) y R03-DECISION-STRATEGIES, corroborado por el baseline del planner Futures.
- [[Echo Futures — Optimización de Campañas]]: C04 al corte Agents-OS señalado; SOURCE / evidencia semántica / implementación / aceptación se conservan separados.
- [Baltussen, Da, Lammers y Martens — Hedging demand and market intraday momentum, 2020](https://twoquants.com/wp-content/uploads/2021/02/2020_Baltussen_LAmmers_Martens_Intra-day-Momentum.pdf): evidencia de investigación de persistencia intradía, no del bracket concreto ni de economía prop. No se trasladan estadísticas del estudio a esta receta.
- [MFFU Rapid EOD 50K — ayuda específica](https://help.myfundedfutures.com/en/articles/16158363-rapid-eod-50k-a-comprehensive-look) y [tabla comercial Rapid EOD](https://marketing.myfundedfutures.com/plans/rapid-eod): verificación focal de fases/límites; no cierra RuleSet ni ruta Echo.
- [[30-resources/agents/skills/echo-futures-research-manager/SKILL]], [[30-resources/runbooks/echo-rnd-cycle-runbook]], [[30-resources/agents/skills/echo-retester-master/SKILL]] y [[30-resources/runbooks/echo-futures-strategy-qualification-runbook]].

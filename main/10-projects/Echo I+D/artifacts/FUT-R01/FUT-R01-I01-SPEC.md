---
type: doc
schema_version: 1
status: draft
area: "[[Trading]]"
project: "[[Echo I+D — Futures]]"
related:
  - "[[FUT-R01-INDICE]]"
  - "[[FUT-R01-RV-01-CONSOLIDADO]]"
  - "[[FUT-R01-ITERACION-01]]"
  - "[[Echo I+D — Cobertura Futures]]"
aliases:
  - "I01-A persistencia de cierre NQ"
tags:
  - kind/doc
  - area/trading
  - project/echo-rnd
  - tech/futures
created: "2026-10-28"
updated: "2026-10-28"
---

# ECHO FUTURES — FUT-R01 / I01-A — Strategy candidata de persistencia de cierre NQ

**Retorno al manager Futures:** LISTA_PARA_REVISION_DE_SPEC, **exclusivamente documental**. Una regla basal queda definida de manera verificable y diferenciable por sus predicados y horizonte de FBC/ORB/MR08; la independencia estadística/económica y ausencia de duplicación de señales **NO** están demostradas. La comparación contra identidades ejecutables requiere traza y corte técnico posterior. Si el manager exige ausencia probada de solapamiento antes de aceptar una identidad, la dependencia es esa reconciliación; no se la oculta.

**Pregunta:** ¿la dirección del retorno de NQ desde el cierre regular previo hasta las 15:30 de Nueva York contiene información útil sobre la dirección del retorno de 15:30 a 16:00, y puede esa Strategy alimentar después campañas CHALLENGE/FUNDED con MM separados?

**Fronteras:** NQ exclusivamente; USD 4.000 son caja comercial Futures para compras de evaluaciones, sin aportes ni financiación Forex. No es equity propia negociable ni sizing de NQ. Frente 1 **PAUSADO para este encargo** por instrucción Owner, aunque se ha informado integración S04 hacia master; esta entrega no verifica ni interviene tal integración. No hay implementación, lectura física de host, pruebas, backtest, campaña, costes medidos, prop elegida, gasto, aceptación Owner ni cierre formal. RV-01 permanece NO_APTO_AUN para campaña; DR-01 original y DR-02 íntegro siguen sin acreditarse. G0–G5: NOT_EXECUTED, sin cambio de gates. **METHOD_DELTA: NO_DELTA.**

## 1. Autoridad, origen y clasificación

- **R1 — SOURCE:** Baltussen, Da, Lammers y Martens, *Hedging Demand and Market Intraday Momentum*, Journal of Financial Economics 142 (2021), pp. 377–403, DOI https://doi.org/10.1016/j.jfineco.2021.04.029. PDF de trabajo primario consultado: https://twoquants.com/wp-content/uploads/2021/02/2020_Baltussen_LAmmers_Martens_Intra-day-Momentum.pdf ; introducción, §3.5 y apéndice A1. Predictor r_ROD: retorno desde el cierre de mercado precedente hasta justo ANTES de los 30 minutos finales; resultado r_LH: retorno de los últimos 30 minutos. Para NQ, tabla A1: ventana investigada 09:30–16:00, muestra histórica 1996-04-12 a 2020-05-01, 6.017 observaciones reportadas. El paper NO define el bracket ni una política prop para la ficha siguiente. El PDF de trabajo (2020) y el artículo publicado (2021) no son dos replicaciones independientes.
- **R2 — SOURCE de contrato NQ:** CME Group, https://www.cmegroup.com/markets/equities/nasdaq/e-mini-nasdaq-100.contractSpecs.html : símbolo NQ; multiplicador USD 20 por punto de índice; tick 0,25 puntos = USD 5 por contrato. La ventana 09:30–16:00 se toma de la delimitación de investigación R1, **no** como afirmación de que Globex cierra a las 16:00.
- **R3 — CONTRAEVIDENCIA acotada:** Carlo Rosa, *Understanding Intraday Momentum Strategies*, Journal of Futures Markets 42 (2022), DOI https://doi.org/10.1002/fut.22375 , https://onlinelibrary.wiley.com/doi/abs/10.1002/fut.22375 . Reporta que la predictibilidad overnight→última media hora de su estudio desaparece en el periodo OOS considerado y varía por régimen. No refuta por identidad la regla r_ROD de NQ aquí propuesta.
- **H1 — HYPOTHESIS/OPERATIONALIZATION propia:** todo el protocolo operativo de barras, igualdad, expiración, stop/objetivo 1:1, una oportunidad diaria, OCO y salida temporal que sigue. Es una adaptación explícita para NQ a una Strategy determinista; **no** es réplica de la estrategia ni reproducción de resultados del paper.
- **Antecedentes internos, no fuentes primarias de la regla:** [[FUT-R01-RV-01-CONSOLIDADO]] §§6,9,10; [[FUT-R01-ITERACION-01]]; [[Echo I+D — Cobertura Futures]]; DR-03 y DR-04 preservados como investigaciones recibidas con findings. Ninguno transfiere conformidad ni rentabilidad. Lectura documental en xKoRx/agents-os, branch master, al 2026-10-28.

## 2. Reconciliación de cobertura e identidad

**Identidad candidata NO registrada aún como Strategy ejecutable:** FUT-NQ-PERSIST-ROD1530-V1. Celda: FUT-NQ-PERSIST; contexto de cierre regular 15:30–16:00 NY. Una Strategy = setup + filtro + objetivo/riesgo técnico. MM, Provider/Program/RuleSet, etapa y sizing no son parte de esta identidad.

| Existente | Predicado/horizonte según cobertura, no según nombre | Solapamiento plausible | Aporte diferencial investigable y límite |
|---|---|---|---|
| FBC — NY_FIRST_CANDLE_V1 | Dirección por color de primera vela completa de 5/15/30/60m; doji sin entrada; extremo adverso como stop; una oportunidad en apertura | Días de impulso pueden coincidir en dirección; no basta mirar sesiones distintas | I01 usa cierre previo→15:30 y último tramo; no usa color inicial. Falta comparación causal de sesiones/señales para excluir equivalencia empírica. |
| ORB — NY_ORB_ADD_V1 | Rango inicial 5/15/30m y cierre M1 fuera del rango; variantes con add/rearme | Continuación direccional común, posible exposición al mismo trend day | I01 NO exige ruptura de máximo/mínimo de apertura y decide una sola vez a las 15:30. La novedad de predictor no acredita nueva familia independiente. |
| MR08 — Trend Pullback Mean Reclaim | Tendencia H1 EMA20/EMA50 con recuperación local M5 y objetivo EMA20; reversión local condicionada a tendencia | Puede alinearse direccionalmente con tendencia y coincidir en día/horario | I01 carece de evento de pullback/reclaim, EMA y filtro HTF. El contraste de oportunidades y colas aún falta. |

**Clasificación:** probable aporte de una regla/horizonte concreto de cierre aún no documentado entre esas tres identidades; duplicidad por señal/exposición **posible y no reconciliada físicamente**. No se cuenta como nueva familia, nueva cobertura científicamente lograda, nueva estrategia aceptada ni correlación baja. Reutilizar calendario, contratos, datos y receipting del Backtester cuando el owner técnico habilite la comparación; no leer ni mutar producto en I01-A. Ningún resultado del nombre de la celda demuestra independencia.

## 3. Strategy basal propuesta — versión única congelable

### BLOQUE A — SETUP

**Universo y reloj [H1]:** NQ CME, un contrato trimestral explícito por oportunidad, identificado por símbolo+vencimiento; precios sobre su rejilla 0,25 puntos. Días normales de mercado cash estadounidense, 09:30:00–16:00:00 en zona IANA America/New_York, con calendario de sesiones versionado; aplicar DST automáticamente, no offsets fijos ni hora de Chile. El corte 15:30 NY equivale a 19:30 UTC en EDT o 20:30 UTC en EST. Días de cierre temprano no generan oportunidad. Si la sesión inmediatamente anterior fue de cierre temprano, no se sustituye el cierre regular faltante por otro de un día aún más antiguo: referencia inválida para esta identidad. No inventar M1 sintética para días no negociados.

**Referencias [R1+H1]:** sean d la sesión NY actual y d−1 la sesión de mercado inmediatamente anterior. P0 = close de la vela M1 cerrada [15:59,16:00) de d−1. P1530 = close de la vela M1 cerrada [15:29,15:30) de d. Ambas deben ser precios NQ positivos, finitos, no sintéticos, sobre tick grid y del **mismo contrato real**: si hubo roll de contrato entre ellas, esta oportunidad queda DATA_INVALID_ROLL, sin serie continua back-adjusted silenciosa. La referencia del paper abarca overnight: NO reemplazar P0 por apertura 09:30 ni por primera hora.

**Predictor y evento [R1+H1]:** a las 15:30:00 NY, una vez disponible efectivamente el cierre de [15:29,15:30), calcular r_ROD = P1530 / P0 − 1 (adimensional); Δ = P1530 − P0 (puntos NQ). Sólo información existente hasta ese instante; NO utilizar high, low, close ni volumen de [15:30,16:00) para decidir. No hay lookback de indicadores ni umbral de volatilidad. No evaluar antes de 15:30 ni retrofechar un cálculo recibido tarde.

**Dirección [R1+H1]:** Δ > 0 → señal LONG (+1); Δ < 0 → SHORT (−1); Δ = 0 exactamente → NO_SIGNAL_ZERO (0). La fuente expresa un timing long si retorno positivo y short en otro caso; la rama **igualdad→0** es adaptación H1, no atribuirla al paper. Comparación exacta sobre precios discretos, sin epsilon optimizable ni redondeo adicional. Una oportunidad evaluable por sesión; ninguna reentrada, flip o segundo setup en ese día.

**Emisión/entrada [H1]:** después de concluir la evaluación de 15:30 se emite como máximo un intento de intención de entrada a mercado según el lado, junto con referencias y bracket técnico del bloque C. Vigencia [15:30:00,15:31:00) NY, exclusivamente después de recibir las barras causales. No ejecutar si el dato está disponible sólo a/desde las 15:31:00; registrar LATE_DATA, no reparar señal con un precio futuro. El primer precio negociable después de emisión determina ejecución física; el open M1 siguiente **no es fill certificado**. La intención no establece cantidad: MM y contrato de órdenes deciden admisión. Al expirar sin fill, cancelar y mantener señal registrada como NOT_FILLED/EXPIRED; no reintentar dentro de la sesión. Si un fill potencial no queda estrictamente entre stop y target del lado correcto, la ejecución se rechaza por ENTRY_GEOMETRY_INVALID; no desplazar niveles.

### BLOQUE B — FILTRO

**Ninguno [H1].** No RSI, volumen, VIX, EMA, condición de apertura, weekday ni ventana optimizada. Elegibilidad de sesión y calidad de datos son **precondiciones de evaluabilidad**, no filtros alpha. Se registran por separado: MISSING_PREV_CLOSE, MISSING_DECISION_BAR, EARLY_CLOSE, INVALID_CALENDAR, BAD_TIMESTAMP_OR_DST, INVALID_PRICE_OR_TICK, CONTRACT_MISMATCH/ROLL, LATE_DATA y cualquier gap crítico que impida afirmar que los endpoints fueron cerrados y observables. Datos faltantes posteriores a la señal afectan outcome/ejecución: no eliminan retroactivamente oportunidades emitidas.

### BLOQUE C — OBJETIVO / RIESGO TÉCNICO

**Geometría única [H1; no paper]:** cuando Δ ≠ 0, distancia D = |Δ| puntos NQ y dirección s = sign(Δ). Stop técnico S = P0. Objetivo técnico T = P1530 + s × D = 2 × P1530 − P0. Es un bracket **1R:1R teórico anclado al precio de decisión**: LONG tiene S < P1530 < T y SHORT tiene T < P1530 < S; D ≥ 0,25 puntos. S y T caen en la rejilla de 0,25 por construcción. **No se recalculan** por fill, spread, número de contratos, prop o MM. La igualdad exacta en un nivel activa su condición correspondiente; no añade buffer. R teórico en USD para un contrato = D × 20; el riesgo real depende del fill, costes, gaps y órdenes, y puede superar esa cantidad. No presentar 1:1 como RR realizado.

**Órdenes y eventos [H1]:** después de confirmar un fill de entrada, riesgo protector: intención de stop-market en S; objetivo: intención limit en T. Para clasificar datos de último negocio, la condición técnica long es precio ≤ S para stop y precio ≥ T para objetivo; short es precio ≥ S para stop y precio ≤ T para objetivo. **Estas condiciones de precio no son garantía de activación por broker**, de ejecución, ni de fill al nivel. El mecanismo efectivo puede depender de bid/ask, last, reglas de stop, orden OCO, latencia y cola; su contrato debe ser reconciliado por el owner técnico. No existe bracket activo antes del fill.

**Salida temporal [H1]:** si queda posición abierta al instante 16:00:00 NY, emitir solicitud market de cierre, cancelar órdenes hijas cuando corresponda y registrar ejecución efectiva. Esta hora es el límite de la tesis de cierre, **no** una promesa de fill a las 16:00 ni autorización de una prop a mantener abierta hasta entonces. Si un programa exige estar flat antes, esa combinación contractual queda INCOMPATIBLE para esta versión; cambiar horario crea otra hipótesis/versión, no un ajuste oculto.

**Precedencia [H1]:** después del fill de entrada, prevalece el **primer evento efectivamente observable** entre stop, objetivo y solicitud temporal, ordenado por timestamp/sequence confiable; una sola salida debe adjudicarse, con cancelación/ack de las demás. Si dos niveles caen dentro de una misma barra M1, el orden intrabar es UNKNOWN_INTRABAR_ORDER hasta obtener secuencia suficiente. Si coinciden con el corte temporal, su orden tampoco se inventa. Gaps pueden saltar niveles y no garantizan precio S/T. Si el stop/target se alcanzó por precios M1 pero no hay evidencia de trigger/fill, registrar POSSIBLE_TOUCH / EXECUTION_UNKNOWN. Nunca asignar de oficio “stop primero”, “target primero” ni “extremo conservador”.

**Separación de MM:** contratos NQ enteros; 1 NQ no siempre será admisible por riesgo o reglas. Si el riesgo técnico, márgenes, límites de pérdida o funded/challenge impiden comprar 1 contrato, **MM_VETO** sin tocar S/T. No sustituir MNQ, ensanchar stop, reducir distancia, recalcular objetivo ni transformar exposición nominal funded en caja. Salidas económicas/protectoras obligatorias del MM/RuleSet se registran con su propia causa y prioridad técnica efectiva; no se les atribuye condición original de Strategy.

## 4. Casos documentales de conformidad, sin ejecutar

Precios de ejemplo en puntos NQ y sobre tick 0,25; P0 de una sesión regular precedente del **mismo** contrato. Son fixtures narrativos, no backtests ni fills. El resultado observable queda condicionado a datos de ejecución.

| ID / condición | Dato de ejemplo | Resultado determinista / límite |
|---|---|---|
| C01 LONG positivo | P0=20.000,00; P1530=20.010,00 | A 15:30 se emite +1, D=10,00; S=20.000,00, T=20.020,00; R teórico 1 NQ=USD 200 antes de costes. Entrada sólo tras cierre causal, vigencia menor a 15:31. |
| C02 SHORT negativo | P0=20.000,00; P1530=19.992,50 | Se emite −1, D=7,50; S=20.000,00, T=19.985,00; R teórico USD 150/contrato antes de costes. |
| C03 cero/equidad | P0=P1530=20.000,00 | Resultado 0 NO_SIGNAL_ZERO, sin entrada ni bracket; no short por “otherwise” de la fórmula académica. |
| C04 mínimo tick | P0=20.000,00; P1530=20.000,25 | LONG, S=20.000,00, T=20.000,50, R teórico USD 5; no filtro de amplitud inventado. El MM puede vetar por coste/admisión. |
| C05 predictor futuro | Dato sólo de barra [15:30,15:31) muestra caída brusca | NO puede cambiar el signo de 15:30. Si se usó esa barra en setup, es lookahead y falla conformidad. |
| C06 dato insuficiente | Falta M1 [15:59,16:00) precedente, o cambia contrato durante roll | DATA_INVALID sin signo ni geometría; no arrastrar último P0 válido ni hacer splicing. |
| C07 sesión/DST | 15:30 NY en EDT o EST; día de cierre temprano | Decisión UTC varía según DST; en cierre temprano no existe oportunidad. Marca versión de calendario y razón. |
| C08 caducidad | Señal +1 válida, no se llenó antes de 15:31:00 | SIGNAL_EMITTED + NOT_FILLED/EXPIRED; no trade y no nuevo intento. Si la barra decisiva llegó tarde, INVALID/LATE_DATA, no entrada retrospectiva. |
| C09 entrada fuera de bracket | LONG con S=20.000 y T=20.020; precio negociable/fill potencial=20.021 | ENTRY_GEOMETRY_INVALID para ese intento. La oportunidad original permanece en journal. |
| C10 ambos niveles posibles | LONG C01, una M1 posterior contiene low=19.999,75 y high=20.020,25 | M1 muestra posibilidad de toque de ambos, no su orden ni fills. Resultado NEEDS_SEQUENCE / DATA_REQUIRED, sin fabricar pérdida o ganancia. |
| C11 ausencia de toque | LONG C01, toda M1 posterior registrada permanece estrictamente entre S y T hasta el corte | No se identifica trigger técnico en esa serie de último negocio; a 16:00 emitir TIME_EXIT si la posición seguía abierta. Fill/time/PnL aún requieren evidencia. |
| C12 igualdad al nivel | LONG C01, last registrado llega exactamente a S=20.000,00 o T=20.020,00 | Condición técnica de nivel inclusiva, pero orden efectiva y fill no se deducen del único OHLC. |
| C13 salida simultánea | Nivel y reloj marcan evento cercano a 16:00 sin secuencia fiable | Ambigüedad declarada; no imponer precedencia por preferencia del simulador ni comparar cash MM con ese dato. |
| C14 señal veto MM | Misma C01; MM-A admite, MM-B no admite 1 NQ por límite de cuenta | Mismo opportunity_id y niveles; dos decisiones de MM, distinto conjunto de fills. No eliminar el evento de B. |

Los ejemplos numéricos no afirman valores actuales de NQ, expectativa, rentabilidad, coste final, factibilidad contractual ni cuota de señales.

## 5. Trazabilidad de reglas y condiciones de observación

| Regla material | Fuente / clase | Evidencia verificable de conformidad | Rechazo o borde |
|---|---|---|---|
| r_ROD antecede a r_LH | R1 SOURCE; convención M1 H1 | P0 y P1530 disponibles al decision_time, ningún timestamp ≥15:30 alimenta signo | C05; lateness, calendarios o referencias inválidas |
| Precio NQ y tick | R2 SOURCE | Contract ID y precios grid 0,25; D puntos, r adimensional, R USD=20×D por contrato | C04, C06; fracción de contrato inválida |
| Predicción +/-/0 | R1 parcial + H1 igualdad | C01, C02, C03 | Igualdad→0 es adaptación; no alegar literalidad académica |
| Sesión/DST y solo un evento | R1 ventana investigada + H1 operacional | C07, C08; clave por sesión NY y calendario | Cierre anticipado, DST mapeado mal, reentrada |
| Ningún filtro alpha | H1 | Oportunidades en todo día elegible, cero y rechazos conservados | Datos inválidos no son “filtro rentable” |
| Stop, objetivo y vigencia | H1 | C01–C04, C08–C09; S/T fijos antes de fill, una intención de entrada | Alterar stop para MM cambia versión |
| Salida y precedencia | H1 | C10–C13; orden observable o DATA_REQUIRED; ack y fill separados | OHLC M1 no resuelve secuencia/fill |

**Identificable con M1 cerrada y timestamp fiable:** P0, P1530, signo/0, D, S/T, evento 15:30, disponibilidad tardía si se almacena ingest_time y, después, r_LH a partir del cierre de [15:59,16:00). M1 posterior permite excluir toque en la serie si todo el rango queda fuera de un nivel, o clasificar posibilidad de toque si lo incluye. Sin fiabilidad temporal de ingesta tampoco se certifica que el cierre ya estaba disponible al momento de decisión.

**Modelado pero NO observado por OHLC M1:** tiempo de envío, precio negociable, spread, latencia, participación/cola, órdenes mercado/stop/limit, fill parcial, comisiones, slip, secuencia stop-target dentro de la misma M1, estados OCO y liquidación protectora. No usar el high/low de una barra como recorrido con orden ficticio ni como garantía de precio límite. La caja, payouts y drawdown contractual no están contenidos en las barras.

**Dato/contrato adicional indispensable para resultado económico no ambiguo:** trades/ticks ordenados y, cuando corresponda, best bid/ask o quotes con timestamps; fuente de activación del stop y mark usado por prop; registros de órdenes/ack/fills; RuleSet por etapa y calendario de enforcement; fees/slippage y ledger de cobros efectivos; versionado de contrato, roll y calidad de sesiones. Si varias trayectorias compatibles con M1 cambian pase/pérdida/payout o ranking de MM, resultado DATA_REQUIRED. No se dan bounds ni fills “conservadores”.

## 6. Registro mínimo para futura ejecución, reutilizando contratos Echo

**No se propone otra BD, scheduler, DSL ni motor.** El frente técnico debe mapear estos atributos a los eventos/receipts ya disponibles y comunicar únicamente gaps concretos. Conservar primero la oportunidad causal; no inferirla de la muestra de trades que un MM dejó ejecutar.

| Nivel | Campos indispensables y semántica |
|---|---|
| Identidad/reproducibilidad | strategy_id, variant/config_version (incluye H1), source_ref, data_manifest/hash, contract_id/expiry, calendar_id/version, timezone, session_date_NY, build/engine/execution_model_version. |
| Oportunidad, evaluable o no | opportunity_id estable por Strategy+contract+sesión+decision_time; previous_close_bar_id+timestamp+P0; decision_bar_id+timestamp+P1530; bars_available_at; r_ROD; Δ; side (+1/−1/0/null); status de evaluabilidad; reason codes y datos faltantes. |
| Intención pura | signal_emitted_at, valid_from, expires_at, stop_S, target_T, nominal_D_points, technical_R_USD_per_NQ, time_exit_at, orden/posición intentada; cero/invalid conserva registro aunque no haya orden. |
| Vista por MM/etapa | opportunity_id idéntico como foreign key; mm_id/version, provider/program/size/stage/ruleset/cohort/account_id, state_before (saldo, trailing DD/HWM, contratos/posiciones/limites, si aplica), admission_decision, veto_reason, requested_qty_NQ_integer, order_intent_id, replay/config/receipt. Cada MM mantiene estado propio. |
| Vida física y salida | submit/ack/reject/cancel timestamps; broker/order IDs, bid/ask/last/mark y su fuente cuando existan; fill_id, fill_qty, fill_price, fees/slippage observados/modelados señalados como tales; stop/target/time/MM/prop exit_trigger, order sequence, exit fill, residual/cancel; UNKNOWN si no observable. |
| Resultado y caja | outcome_state (incluido ambiguous/data_required), realized/unrealized por cuenta, RuleSet DD/target/terminalidad; enlace a ledger compras/reset/activación/cargos, solicitud/aprobación/abono, cash neto realmente recibido, fecha y cuenta; no mezclar flujo contable con señal. |

**Comparación A vs B:** misma oportunidad externa y mismo S/T/time_exit, independientemente de cuántos trades admita cada MM. Comparar decisiones de admisión, no-fills, salida, estados posteriores y caja bajo el mismo calendario de observación. Si un MM consumió límite o perdió la cuenta, **mantener** las siguientes oportunidades externas con veto ACCOUNT_INACTIVE/NO_CASH según corresponda. No escalar una equity curve de un contrato por lotaje, no crear funded desconectadas de pases, no duplicar comisiones ni contabilizar solicitudes como cobro. La comparación concreta de dos MM y perfil prop corresponde a I01-B/C y manager, NO a esta ficha.

## 7. Anexo de investigación preregistrada

**Hipótesis de precio H_PRICE (falsable, antes de resultados):** en jornadas NQ elegibles no-cero, la estrategia de lado sign(r_ROD) tendrá rendimiento de precio en el tramo 15:30–16:00 mayor, en promedio, que mantener lado LONG en ese mismo tramo y en **las mismas fechas**. Definir r_LH = C1600 / P1530 − 1, donde C1600 es close de [15:59,16:00) del mismo contrato; medida adimensional no es PnL ejecutado. Contraste pareado Z_d = sign(r_ROD,d)×r_LH,d − r_LH,d; efecto de interés media(Z_d) > 0. La expectativa de persistencia podría derivarse de presión de cobertura de delta en la dirección del movimiento precedente; **explicación propuesta**, no gamma observado ni causa probada para estas operaciones. No atribuir al estudio una prueba causal nueva.

**Control fijo:** ALWAYS_LONG en el MISMO periodo 15:30–16:00 sobre las MISMAS jornadas evaluables no-cero. Se usa como control de precio; no se presenta como Strategy prop con el mismo bracket. Reportar también retorno sign(r_ROD)×r_LH, señal por signo, frecuencia y dependencia temporal. No alterar el control por resultados.

**Regla de refutación de H_PRICE:** calcular intervalo de confianza bilateral del 95% de media(Z_d) por bootstrap de bloques de semanas de mercado NY completas, remuestreando semanas y conservando los días dentro de cada semana, con 10.000 remuestras; si límite superior ≤0, se considera refutada la mejora positiva específica contra ese control en la muestra designada. Si límite inferior >0, hay evidencia a favor de ese contraste bajo el diseño; si el intervalo incluye 0, INCONCLUSO, **no** “refutado”. Una muestra o cobertura insuficiente sigue INCONCLUSO/DATA_REQUIRED, no se fuerza veredicto. G0–G5 siguen siendo independientes; no usar este test como sustituto.

**Contraevidencia y amenazas:** Rosa 2022 cuestiona extrapolación de un predictor overnight distinto; sus resultados no son rechazo de esta igualdad de predictores. La fuente R1 termina en 2020 y analiza una regularidad global, no una campaña prop de 2026. También pueden confundir el resultado drift direccional, overnight, shocks y régimen, degradación por publicación, selección de instrumentos, roll, fricción o calendario. La hipótesis de gamma no es medible con OHLC M1; para atribuirla causalmente se necesitarían datos de exposición/cobertura externos, fuera de esta ficha.

**Refutación económica separada:** H_ECON aún **NO está congelada** por faltar MM/programa/fees/horizonte. CHALLENGE evalúa pase, pérdida y duración por compras/intentos; FUNDED mide activaciones, requisitos y cobros recibidos; SIMULATION posteriormente conserva caja común finita USD 4.000 + 100% de abonos netos recibidos, sin aportes. PF, Sharpe, WR o expectativa por trade no son gates universales de admisión. Una distribución de caja no útil bajo un RuleSet/las políticas congeladas refutaría esa **combinación económica**, no necesariamente la regularidad H_PRICE. Una H_PRICE refutada tampoco prueba que toda otra Strategy o MM sea antieconómica.

**Selección y ventanas contaminadas conocidas:** R1 estudió 1974–2020 global y NQ específicamente 1996-04-12 a 2020-05-01; el diseño ya está expuesto públicamente. DR-03 propuso primero 2010–2026 y luego 2015–2026, primera hora→última hora y entrada al mediodía, pero eso NO fue esta regla y sus cifras no se heredan. DR-04 enumeró otras fichas/indicadores y cambios de MM; no se ejecutaron aquí. RV-01 reencauzó a cierre y registra R03 como confirmación temporal retrospectiva, NO OOS virgen. SSRN 4824172 expone resultados SPY y apéndice Nasdaq 2007–2024, conocido durante selección, pero no prueba esta adaptación ni cash. El corte posterior exacto, ventanas de tests de FBC/ORB/MR08, intentos de terceros, datos que vio cada agente y recepción física de datasets **son UNKNOWN**. No designar 2021–2026, R03 u otra ventana como holdout virgen sin registro previo verificable; no abrir parrilla de ventanas, RR, filtros o multiplicadores para rescatar resultados.

**Datos y modelo prerequisitos:** primero inventory de NQ por vencimiento, calidad de timestamps, resolución M1, DST/holidays, roll, disponibilidad de dos referencias y tramo LH. Para H_PRICE bastan closes verdaderamente observables y calendario; para estrategia con SL/TP y campañas se necesita modelo y secuencia física compatible con stop/limit/quotes, órdenes, reglas y cash. Si sólo hay OHLC M1, H_PRICE puede investigarse con limitaciones de mercado, pero trayectorias con bracket ambiguo quedan sin adjudicación económica. No resolver ello asignando extremos arbitrarios.

**Coste y límites:** esfuerzo documental marginal ya realizado; coste de acceso/retención de ticks/quotes, comisión NQ por ida/vuelta, market data, proveedor, API/bridge, cómputo de recibos y perfiles no está cotizado ni físicamente comprobado. No usar USD 1–2 de DR-03 como dato oficial ni el coste por acción SPY como proxy NQ. Como no hay permiso de ejecución/gasto, presupuesto de cómputo y cronograma permanecen NOT_AUTHORIZED. Primer incremento futuro: revisar semántica/identidades y mapear schema/eventos existentes; después datos y contrato; sólo tras aceptación, derivar G0–G5 técnicos sin saltos.

**Aporte a cobertura:** pregunta de persistencia condicionada al estado del día a las 15:30, distinta por predicado de apertura/rango inicial y reversión a media, en FUT-NQ-PERSIST. Resultado de cobertura CANDIDATE_SPEC_ONLY; no evidencia de independencia, diversidad de cola, edge ni cash. Cualquier coincidencia exacta de predicados/trazas que desautorice identidad separada debe llevar a DUPLICIDAD_POR_RECONCILIAR ante el manager, preservando esta ficha y sus negativos, sin cambiar candidato silenciosamente.

## 8. Dependencias, alternativa y handoff

| Decisión/nivel | Qué permite ahora / dependencia exacta | Dueño |
|---|---|---|
| Spec de Strategy | Congelar una baseline no optimizada, cases C01–C14, fuentes y refutador de precio. No permite ejecutar ni elevar G0. | Manager Futures revisa y Owner acepta/rechaza; respuesta I01-A. |
| Reconciliación técnica | Confirmar que la identidad no esté ya implementada semánticamente y mapear registros actuales de oportunidades, stop/TP/time, calendario e input clocks. Comparar señales/exposición con FBC/ORB/MR08 sin asumir independencia. | Owner Backtester/retester cuando termine integración; Frente 1 no tocar ahora. |
| Datos/ejecución | Verificar contrato real y M1, roll/calendario y secuencia stop/target/quotes/ordenes. Si no hay soporte, DATA_REQUIRED por perfil. Sin inventar fills/cotas. | I01-C sólo si manager lo coordina; owner técnico. |
| Perfil económico | Una ruta Provider/Program/Size/Stage/Platform con reglas, costos y cash verificables; dos MM distintos congelados sin cambiar S/T; horizonte y política de payout que permita valorar campañas. | I01-B + manager/Owner. |
| Admisibilidad contractual | El cierre 16:00, automatización o stop/target pueden ser incompatibles con una prop concreta; **no moverlos** dentro de V1. | Owner elige contrato o rechaza combinación, I01-B documenta. |

**Alternativa única enlazada, NO desarrollada:** [[Echo I+D — Cobertura Futures]] → **MR06 Volatility Shock Snapback**, celda FUT-NQ-REVERT: barra M1 extrema y siguiente cierre cruzando su mitad en sentido contrario, objetivo EMA20 M1. Es una identidad existente de reversión, no una nueva invención. Su propia spec/recibos necesitan reconciliación antes de cualquier ejecución. No reemplaza a FUT-NQ-PERSIST por una lectura selectiva de resultados.

**Retorno compacto al manager:**

- RESEARCH_QUESTION: FUT-NQ-PERSIST; persistencia r_ROD→r_LH antes de 16:00 NY; H_PRICE separada de caja/campaña.
- CURRENT_EVIDENCE: R1 primaria, R2 contrato NQ, R3 contraevidencia acotada; cobertura FBC/ORB/MR08; RV-01 NO_APTO_AUN.
- SOURCE_UNCERTAINTY: SOURCE para r_ROD y tick; OP/HIP para señal completa, igualdad, bracket, salida y refutador; UNRESOLVED para contratos, fills, datos, independencia y MM.
- EXPERIMENT: una ficha, control ALWAYS_LONG, C01–C14, criterio H_PRICE predeclarado, ningún resultado ejecutado.
- CONFORMANCE: documental únicamente; código/trace/receipts/gates NOT_EXECUTED.
- ECONOMICS: CHALLENGE/FUNDED/SIMULATION NOT_EVALUATED; caja USD 4.000, sin aportes; no cash simulado ni políticas MM inventadas.
- DECISION: LISTA_PARA_REVISION_DE_SPEC (no G0/G1); posible solapamiento a reconciliar con trazas; no declarar familia independiente.
- OWNER_ACCEPTANCE: PENDING.
- COVERAGE_DELTA: CANDIDATE_SPEC_ONLY, no PASS.
- NEXT_RESEARCH: manager recibe I01-A y contraste I01-B, solicita sólo gap técnico imprescindible después de reanudación; MR06 permanece alternativa.
- METHOD_DELTA: NO_DELTA; G0–G5 intactos.

**Control de publicación:** este archivo es el único destino documental autorizado para I01-A; no implica edición de planner, cobertura, originales DR ni worker B, no implica réplica en Hefesto/Graphify ni cierre de sesión.

---
type: project
schema_version: 1
owner: me
root: true
status: active
priority: P1
area: "[[Echo]]"
parent:
sprint: 2026-09-23--2026-09-30
start: 2026-09-23
due: 2026-09-30
progress: 2
repo:
jira:
prs:
aliases:
  - Futures Prop Automation
  - Echo Futures Trading
tags:
  - kind/project
  - area/echo
created: "2026-09-23"
updated: "2026-09-23"
---

# Echo Futures

%% Naming: Echo Futures es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo Futures
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** 2026-09-23 → 2026-09-30
> _parent / sprint / repo / jira / prs son opcionales._

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> `owner: me` → **proyecto humano**: la iniciativa/esfuerzo que conduces tú.
> `owner: agent` → **proyecto de agente**: un curro delegado, con detalle pesado que escribe y sigue un agente. Casi siempre es subproyecto de uno humano y vive en la subcarpeta `agentes/` de su iniciativa.
> `root: true` solo en **iniciativas raíz** (sin `parent`). Todo subproyecto debe setear `parent`; si no, aparece como huérfano en [[Panel de Proyectos]].
>
> **Tarea puente:** cuando este proyecto es `owner: agent`, en su proyecto **padre** debe existir UNA sola tarea humana que lo representa (arrancar + seguimiento). Así tu cockpit ve una línea por curro delegado, no las tareas internas del agente. Ejemplo, en el padre:
> `- [ ] [[Echo Futures]] arrancar + seguimiento #owner/me #type/supervision #area/personal`

## 🎯 Objetivo

- Convertir la idea inicial de operar futuros fondeados con alta intensidad y alto volumen en un sistema cuantitativo, reproducible y escalable sobre Echo + NinjaTrader, comenzando por definir y validar la operativa, la gestión monetaria y la economía real de las prop firms antes de implementar automatización.
- North star inicial: maximizar **cash neto extraído por unidad de capital real arriesgado y tiempo**, no maximizar balance nominal, cantidad de cuentas ni tasa de aprobación aislada.
- Escala objetivo de largo plazo: operar decenas de cuentas en paralelo (orden de magnitud aspiracional: 40–80) sin que la estrategia, la gestión de riesgo o la reconciliación dependan de trabajo manual por cuenta.

## 📊 Estado actual

- **2026-09-23 — Proyecto creado.** La idea está en fase de discovery operativo; no existe todavía estrategia, gestión monetaria, prop firm, instrumento ni arquitectura de ejecución congelados.
- Hipótesis del owner: estrategias de **win rate alto**, timeframes muy bajos, entradas/salidas rápidas y señales simples que pueden incluir estocásticos u otros filtros; Gerard García, Tradesfera y Psicólogo del Trading son fuentes iniciales de investigación, no autoridades mecánicas todavía.
- Hipótesis de gestión: usar un perfil agresivo al inicio y estudiar el método de hardscalping/recovery atribuido a Gerard García: cuando una posición evoluciona en contra y se cumple un trigger aún por reconstruir, aumentar exposición buscando un rebote y recalcular el objetivo/salida sobre la posición agregada.
- Hipótesis económica: aceptar una tasa alta de cuentas quemadas si el ciclo completo challenge/evaluation → funded → retiro mantiene valor esperado neto positivo después de fees, activaciones, resets, comisiones, slippage y restricciones de payout.
- El sistema debe distinguir **pasar la evaluación**, **sobrevivir funded** y **retirar dinero**; optimizar una sola de esas etapas puede empeorar la economía total.
- El target de 40–80 cuentas es un objetivo de capacidad futura, **no scope del MVP**. El primer vertical slice será una estrategia, una prop/configuración, un instrumento, una Reference y una Execution.
- **Gate actual: RESEARCH_ONLY.** No desarrollar bots NinjaTrader ni integración Echo hasta cerrar G0 Operativa y G1 Economía.

## 🧠 Hipótesis operativa inicial

La idea no se congela como “martingala” ni como “promediar pérdidas” hasta reconstruir evidencia suficiente. El proyecto tratará el hardscalping como una **secuencia de recuperación con aumento de exposición** y deberá identificar exactamente el mecanismo causal y sus límites.

La ventaja que se quiere validar combina cuatro piezas: una entrada base de alta probabilidad, permanencia corta en mercado, capacidad de aumentar exposición bajo condiciones concretas cuando el trade va adverso y un modelo económico de prop donde el downside real por intento está acotado por el coste del challenge/cuenta y sus reglas. La fuerza bruta viene del volumen y de la repetición; no reemplaza la necesidad de demostrar valor esperado positivo.

El riesgo principal es de cola: una técnica con win rate muy alto puede esconder pérdidas raras pero suficientemente grandes para destruir la cuenta. Por eso el KPI principal no será win rate sino **distribución completa de resultados y cash extraído después de cuentas fallidas**.

## 🗓️ Horizonte de entrega — máximo 7 días

**Outcome de horizonte:** terminar la semana con al menos una operativa mecanizable seleccionada, un backtest/replay reproducible con supuestos explícitos, simulación de challenge→funded→payout sobre reglas reales de al menos una prop candidata y un veredicto `GO | ITERATE | NO_GO` para congelar o no el MVP Echo Futures.

**No-goals de esta semana:** desarrollar integración Echo/NinjaTrader productiva, construir copier multi-account, soportar múltiples props, comprar una cohorte grande de cuentas o optimizar infraestructura. Si el research no demuestra una operativa suficientemente concreta, la semana termina en `NO_GO` o `ITERATE`, no en código por inercia.

| Día | Outcome observable | Gate |
|---|---|---|
| D1 | Contrato común de research congelado + entrevista Gerard realizada + tres mandatos one-shot listos/ejecutándose | Cada fuente tiene corpus delimitado y output contractual idéntico |
| D2 | Gerard + Tradesfera + Psicólogo del Trading reducidos a reglas mecánicas y 1–3 estrategias candidatas comparables | Cero regla material aceptada sin evidencia; ambigüedades marcadas |
| D3 | 1–2 estrategias seleccionadas y expresadas como máquina de estados; gestión hardscalping parametrizada | Entrada, add, sizing, SL/TP, salida y pérdida máxima son simulables |
| D4 | Backtest/replay reproducible sobre datos adecuados al path intratrade | Resultados incluyen trades, MAE/MFE, costs y sensibilidad básica |
| D5 | Simulador de prop + Monte Carlo sobre al menos un rule set real | Challenge→funded→primer payout, burn rate y cash neto reproducibles |
| D6 | Validación adversarial: OOS/periodos, slippage, comisiones, rachas, parameter sensitivity y reglas de prop | La tesis no depende de un único parámetro frágil ni de fills irreales |
| D7 | Decisión `GO | ITERATE | NO_GO`; si GO, SPEC MVP congelada y piloto económico dimensionado | Presupuesto, cuenta/plan, instrumento, estrategia y criterios de aborto definidos |

### Estrategia de research — tres one-shots + síntesis

No se investigará “todo el contenido” de cada creador. Cada one-shot buscará **extraer operativas automatizables** y deberá responder el mismo contrato. Esto permite comparar ideas y evita que el agente entregue una biografía o un resumen de YouTube.

1. **Gerard García — híbrido privado+público.** Primero el owner entrega libremente lo aprendido del curso. Luego se realiza una entrevista dirigida para cerrar huecos. En paralelo, un deep research público busca confirmar, refutar o completar parámetros usando videos, ejemplos y material accesible. El curso del owner tiene más peso para describir la técnica enseñada; evidencia pública sirve para contraste, no para sobreescribirla por popularidad.
2. **Tradesfera — deep research público one-shot.** Buscar setups repetidos, indicadores/parámetros, timing, gestión, pérdidas y evidencia de ejecución. Ignorar contenido motivacional/general salvo que cambie una regla.
3. **Psicólogo del Trading — deep research público one-shot.** Mismo contrato y mismo criterio de evidencia.
4. **Síntesis adversarial.** Un cuarto análisis recibe solo los tres outputs estructurados, no vuelve a navegar todo el corpus. Separa componentes compatibles: edge de entrada, filtros, recovery, sizing y salida; no crea un “Frankenstein” mezclando reglas sin evidencia.

### Contrato común de salida de cada deep research

Cada investigación debe entregar:

- Lista de videos/fuentes realmente usadas con URL/título/fecha o identificador reproducible y timestamp cuando exista.
- Instrumentos, sesiones y timeframes observados.
- Indicadores con parámetros exactos si son demostrables.
- Setup de entrada LONG y SHORT expresado condicionalmente.
- Condiciones de NO TRADE.
- SL/TP inicial y cualquier modificación posterior.
- Gestión monetaria inicial.
- Si existe averaging/add/recovery: trigger exacto, tamaño, cantidad máxima, precio medio y salida después de cada escalón.
- Pérdida máxima de una secuencia y criterio de abandono.
- Evidencia de operaciones ganadoras y perdedoras.
- Diferenciar `EXPLICIT` (el creador lo dice), `OBSERVED` (se ve repetidamente), `INFERRED` (deducción) y `UNKNOWN`.
- Una o más estrategias candidatas en pseudoreglas deterministas, sin código.
- Lista de ambigüedades que impedirían automatizar.
- Qué necesitaría validarse con datos antes de confiar en el edge.
- Veredicto por estrategia: `MECHANIZABLE | PARTIAL | DISCARDED`, sin puntajes subjetivos.

### Entrevista Gerard — método

La entrevista no parte preguntando veinte detalles aislados. El owner primero hace un **brain dump libre** de lo que recuerda del curso: cómo detecta setup, cómo entra, qué mira cuando va a favor/en contra, cuándo agrega, cómo cambia tamaño/SL/TP, cuándo acepta la pérdida y qué ejemplos recuerda. Después el entrevistador recorre el contrato G0 y pregunta únicamente lo que siga ambiguo.

El objetivo de la entrevista es convertir conocimiento tácito del owner en reglas falsables. Si algo se recuerda como “cuando parece que rebota”, queda `UNKNOWN` hasta precisar qué observable produce esa decisión.

### Criterio de selección rápida

Una estrategia no gana por parecer sofisticada. Para entrar a D3 debe cumplir simultáneamente:

- suficientemente mecánica para simularla sin interpretación visual humana;
- frecuencia suficiente para obtener muestra útil rápido;
- datos disponibles con resolución compatible con sus entradas/adds/salidas;
- costes de trading tolerables para su holding time;
- riesgo de cola cuantificable;
- compatible en principio con al menos una prop plausible;
- posibilidad de probar separadamente **entry edge**, **recovery** y **money management**.


## 🧾 D1 — Gerard García: extracción del curso v0

**Fuente:** brain dump + re-visionado reciente del curso privado por el owner + captura de la tabla de riesgo variable. Estado: `GERARD_V1_EXTRACTED / OBJECTIVIZATION_REQUIRED`.

### Estrategias/entradas recordadas

- **Nasdaq Opening Range:** observar los primeros 30 minutos y operar en 5m la ruptura del rango a favor de la dirección de ruptura, sin exigir cierre de vela. Asociada por el owner a hard scalping positivo.
- **H4 trend + LTF pullback:** identificar tendencia clara en H4 y buscar en temporalidad inferior entradas de pullback; ejemplo alcista: precio alcanza banda inferior de Bollinger en 5m y se busca recorrido hacia banda superior.
- **Nasdaq momentum por sesión:** sumarse a tendencia/momentum en sesión de Londres y en sesión de Nueva York, tratándolas como contextos separados.
- **Range breakout genérico:** formar rango durante un periodo X y entrar inmediatamente al romper, sin esperar confirmación de cierre.
- **Relevant high/low continuation/reversal:** si cierra por debajo de un mínimo relevante, entrar buscando continuación; si la vela rompe el mínimo pero recupera y cierra por encima, considerar entrada contraria. Simétrico para máximos.

Gerard prioriza la gestión sobre el edge de entrada y, según el recuerdo del owner, sostiene que la dirección inicial podría incluso decidirse aleatoriamente. Esto queda como afirmación a contrastar, no como edge certificado.

### Tres motores de gestión que deben probarse por separado

**A. Negative hardscalping / recovery intra-trade.** Ante movimiento adverso, agrega contratos y acerca las barreras de salida. Ejemplo recordado: 3 micros + 3 + 3. La intención declarada es conservar aproximadamente el riesgo monetario y el objetivo monetario mientras aumenta el tamaño total, por lo que el SL/TP en precio se comprimen alrededor del nuevo precio medio. Gerard decide trigger, distancia y sizing de forma altamente discrecional según volatilidad/espacio disponible; por tanto el proyecto no intentará copiar su ojo, sino parametrizar esos grados de libertad y buscar regiones robustas.

**B. Positive hardscalping / pyramiding.** Cuando la operación ya avanza con fuerza a favor, agrega exposición, mueve la protección hacia breakeven y deja correr una extensión grande; el owner recuerda objetivos del orden de 1:6. Debe tratarse como motor independiente del recovery adverso.

**C. Variable risk progression entre trades.** Captura suministrada: riesgo inicial 300, multiplicador 1.20 y reward:risk 1:1.5. La tabla visible muestra aproximadamente 300→360→432→518→622→746→896→1075 de riesgo por intento. Esta progresión no es equivalente al hardscalping intra-trade y requiere aclarar regla de reset, lotaje y objetivo real.


### Entrevista Gerard — decisiones cerradas v1

- **Recovery trigger original:** discrecional. En directos agrega exposición en distintos momentos para acelerar el retorno; no existe una condición mecánica única observada por el owner.
- **Sizing intra-trade:** variable. Parte pequeño y suma progresivamente; `3 + 3 + 3 micros` es un ejemplo habitual, no una constante. La distancia disponible depende de volatilidad, timeframe, riesgo monetario y expectativa de movimiento.
- **Autoridad del riesgo:** confirmada en dólares. Si la secuencia tiene riesgo máximo de, por ejemplo, 2K, cada aumento de contratos obliga a recalcular la distancia del SL desde el nuevo precio medio para que la pérdida monetaria siga aproximadamente en 2K. Lo mismo aplica al objetivo monetario; por eso las bandas se comprimen.
- **Positive hardscalping:** también discrecional. Debe objetivizarse con reglas medibles —persistencia direccional, velas consecutivas, desplazamiento ATR/R, breakout estructural o MFE— en vez de copiar decisiones visuales.
- **Variable risk:** tras un win vuelve al primer escalón y la intención declarada es que el siguiente ganador recupere todas las pérdidas previas y además termine positivo. La foto fue tomada mientras la hoja se modificaba; sus valores no son autoridad de fórmula.
- **Entry edge:** Gerard usa distintos modelos en vivo y prioriza la gestión sobre la precisión de entrada. La tesis “podría entrar con una moneda” queda como hipótesis experimental.
- **Fondeada:** el curso prioriza un arranque agresivo, buscando rápidamente profit grande o burn, y posteriormente sesiones menores para satisfacer payout/consistency. La regla exacta debe venir siempre de la prop vigente.
- **Instrumento/lotaje:** no congelar 3 micros, 30 micros ni MNQ/NQ como constantes. El contrato correcto es riesgo monetario + espacio de precio + límite de contratos.
- **Account size inicial:** 50K es el candidato actual. 150K queda como fase posterior si la economía mejora al escalar.

### Parámetros a objetivizar

- trigger de add por movimiento adverso: puntos/ticks, ATR, fracción del SL inicial, estructura o combinación;
- número máximo de adds;
- fracción de exposición usada en cada add;
- spacing fijo vs. progresivo;
- target monetario fijo vs. variable tras cada add;
- stop monetario fijo vs. reducido;
- criterio de positive hardscalping;
- condición de BE;
- extensión de target tras momentum favorable;
- multiplicador de variable risk entre trades;
- reset tras win y stop de secuencia/cuenta.

**Principio de validación:** una solución válida debe sobrevivir en un rango de parámetros. Si sólo funciona con un punto exacto de spacing/multiplicador, falla robustness.

### Baseline experimental obligatoria

1. **Random direction:** dirección 50/50 + gestión Gerard parametrizada.
2. **Entry-only:** cada entry model con SL/TP simple, sin recovery ni variable risk.
3. **Recovery delta:** mismo entry + hardscalping adverso.
4. **Positive hardscalping delta:** agregar pyramiding favorable.
5. **Variable-risk delta:** progresión entre trades.
6. **Full stack:** combinación final.

Esto permite localizar si el edge proviene de la entrada, del recovery, de la asimetría económica de la prop o de una mezcla.

### Fórmula útil para variable risk

Si el riesgo sigue `R_n = R_0 * m^n` y el ganador paga `b * R_n`, exigir que cualquier primer win tras una cadena de pérdidas recupere todo y deje siempre el mismo beneficio inicial conduce a:

`m = 1 + 1/b`

Para `b=1.5`, `m=1.6667`. Con `R_0=300`, una cadena idealizada sería aproximadamente `300 → 500 → 833 → 1389...`, y cualquier win dejaría aproximadamente +450 neto. Es una derivación matemática del objetivo descrito por el owner; no se atribuye a Gerard hasta confirmar su hoja.

### Modelo matemático provisional del recovery

Si después de cada add el objetivo monetario (P) y la pérdida monetaria máxima (R) permanecen constantes, para una posición long agregada con cantidad total (Q), precio medio ponderado (ar p) y valor monetario por punto/unidad (v):

- (SL = ar p - R/(Qv))
- (TP = ar p + P/(Qv))

Para short, los signos se invierten. Al aumentar (Q), ambas distancias en precio se reducen. Esto reproduce exactamente la intuición de “las bandas se juntan” descrita por el owner, pero queda `INFERRED` hasta confirmar que Gerard conserva dólares constantes y recalcula sobre el average price.

### Hallazgo sobre la tabla de riesgo variable

Con (R_0=300), multiplicador (m=1.20) y payoff (1.5R), la secuencia visible implica:

- win inmediato: +450 acumulado;
- una pérdida y luego win: +240;
- dos pérdidas y luego win: -12;
- tres pérdidas y luego win: aproximadamente -314;
- cuatro pérdidas y luego win: aproximadamente -677.

Por tanto, **esa tabla por sí sola no puede significar “cualquier siguiente win recupera todo y deja positivo”**. A 1:1.5, un multiplicador asintótico superior a ~1.667 sería necesario para garantizar recuperación total de una cadena arbitraria de pérdidas. Debe existir otra regla, un objetivo distinto o el recuerdo mezcla dos modelos. Además, la última pérdida acumulada visible en la captura no sigue limpiamente la progresión 1.20, por lo que esa fila requiere explicación antes de usarla.

### Modelo económico de prop recordado

- **Topstep 50K:** el owner recuerda coste aproximado 89 USD, sin activación, profit target 3K y pérdida permitida 2K. Todo debe verificarse contra reglas oficiales vigentes antes de simular dinero.
- **Evaluation:** filosofía sacrificial/agresiva. Ejemplo recordado: buscar +1.5K con -2K de riesgo; secuencias posteriores de +500/+1K y cambios de riesgo todavía requieren explicar qué regla de la prop las origina.
- **Funded:** buscar un primer día de beneficio muy grande (orden 3K–4K) y luego varios días pequeños (ejemplo 500×4) para llegar a retiro. El motivo reglamentario exacto está `UNKNOWN`.
- **Account inventory:** mantener cuentas suplentes y rotar/replicar operaciones. Las cuentas se tratan económicamente como intentos desechables si el coste real de burn es bajo frente al payout potencial.
- Props mencionadas: Topstep y Take Profit Trader como principales; Alpha Futures, Tradeify y Lucid como secundarias. Ninguna regla actual queda congelada hasta research oficial.


### Topstep — contraste oficial vigente 2026-09-24

El curso no es autoridad de reglas comerciales. Primer contraste con documentación oficial vigente:

- Trading Combine 50K: profit target 3K, Maximum Loss Limit 2K y consistency target 55%; puede aprobarse en dos días si el mejor día no supera 55% del beneficio total.
- Límite Combine 50K: 5 minis / 50 micros.
- No hay límite de Trading Combines activos publicado; sí hay máximo de **5 Express Funded Accounts activas**.
- Precio 50K actual: **49 USD/mes Standard** + 149 USD de activación sólo al pasar, o **95 USD/mes No Activation Fee**. El 89 USD del curso/recuerdo está desactualizado.
- XFA Standard: 5 winning days de 150+ para payout. XFA Consistency: mínimo 3 días y largest day <=40% del net profit.
- Para traders nuevos aplica split 90/10. El request es hasta 50% del balance y el cap 50K es 2K Standard / 3K Consistency, salvo promociones/configuraciones específicas.
- El patrón “gran primer día + varios días pequeños” encaja mejor con Standard actual; con Consistency 40%, un día de 4K exige al menos 10K netos para que represente <=40%.
- La economía `1 payout / 20 attempts` depende del pricing path. Ejemplo simplificado: 20×95 = 1,900 USD; un request de 2K con split 90/10 entrega 1,800 antes de otros costes, por lo que no alcanza break-even. Con Standard: 20×49 + 149 de activación de la única cuenta aprobada = 1,129; 1,800 netos dejan ~671 USD antes de otros costes.

**Conclusión:** el pricing path es una variable del modelo de estrategia, no una decisión administrativa.

### Implicación económica importante

Debe distinguirse **trading EV dentro de la cuenta** de **cash EV del negocio de prop**. Una operativa puede tener expectancy mediocre o incluso negativa sobre PnL nominal y aun así ser económicamente interesante para el owner si el downside real por evaluation está limitado al fee mientras un camino exitoso habilita payouts mucho mayores. El simulador G1 debe modelar ambos niveles y nunca usar el balance nominal de 50K como capital real invertido.

### Bloqueos restantes Gerard/G0

La entrevista de conocimiento queda suficientemente cerrada para avanzar. Ya no buscamos una regla secreta para los puntos discrecionales: pasan a ser parámetros experimentales.

Pendientes:
- confirmar, si aporta valor, la fórmula exacta de la hoja de variable risk;
- extraer 3–5 ejemplos completos para calibrar rangos razonables de spacing/adds;
- seleccionar dos entry models para D3;
- ejecutar research público de contraste, especialmente pérdidas y límites;
- cerrar una configuración como máquina de estados simulable antes de PASS G0.


## 🔬 M0 — Forense de operativa

### Fuentes iniciales

- **Gerard García:** cursos y videos que posee el owner + material público pertinente.
- **Tradesfera:** operativa pública, sesiones, explicaciones y ejemplos relevantes.
- **Psicólogo del Trading:** material público y cualquier contenido del owner que se incorpore explícitamente.
- Cada regla derivada debe guardar fuente, timestamp/lección, evidencia, nivel de confianza y si es suficientemente determinista para automatizar.

### Contrato mínimo a reconstruir por operador/estrategia

- Instrumento(s), sesión y horario efectivo.
- Timeframe de decisión y, si existe, timeframe de contexto.
- Setup completo de entrada: indicadores, parámetros, cruces/niveles, filtros, contexto y condiciones de no-trade.
- Tipo de orden y timing real de entrada.
- Tamaño inicial y unidad de sizing.
- SL y TP iniciales: distancia, fórmula y autoridad para modificarlos.
- **Trigger exacto de aumento de posición:** distancia adversa, estructura, indicador, tiempo, volatilidad u otra condición; no aceptar “cuando se da vuelta” como regla.
- Secuencia de tamaños: cantidad máxima de adds, multiplicador o escalera exacta y exposición total máxima.
- Precio medio ponderado después de cada add.
- Regla exacta de recálculo de SL/TP después de agregar exposición.
- Condición de scratch/breakeven, salida parcial y cierre forzado.
- Qué ocurre si continúa en contra después del último add.
- Stop diario, stop por sesión y número máximo de secuencias fallidas.
- Reglas de noticias, rollover, baja liquidez y desconexión.
- Evidencia de trades ganadores **y perdedores**; no inferir el modelo desde highlights.

### Output G0

G0 queda PASS únicamente cuando exista al menos una estrategia candidata expresable como una máquina de estados sin decisiones humanas ambiguas y con ejemplos que cubran entrada normal, recovery/add, salida ganadora y pérdida completa. Si una regla material sigue siendo “a ojo”, el bot queda bloqueado.

## 💰 M1 — Gestión monetaria y economía de prop

El proyecto modelará la cuenta por **capital económico realmente arriesgable**, no por el balance publicitado de 50K/100K. Cada programa de prop debe normalizar como mínimo: coste de evaluación, activación, resets, profit target, drawdown y su modalidad, daily loss, límites de contratos, consistency, días mínimos, restricciones de scaling/DCA/copier/automatización, reglas de payout, máximo de cuentas y cualquier condición capaz de invalidar esta operativa.

### Estados económicos mínimos

- **EVALUATION_AGGRESSIVE:** perfil orientado a maximizar la probabilidad/velocidad de llegar a funded bajo un presupuesto de intentos explícito.
- **FUNDED_PRE_PAYOUT:** política posiblemente distinta; optimiza probabilidad de llegar al primer retiro.
- **PAYOUT_PROTECTED:** después de retirar, estudiar si conviene reducir riesgo, reciclar beneficio o mantener agresividad.
- Estos nombres son estados de investigación, no reglas congeladas; el análisis puede demostrar que dos o los tres deben usar la misma política.

### Variables de la secuencia hardscalping

- Riesgo inicial (R_0).
- Número máximo de adds (N).
- Tamaño por escalón (q_i).
- Distancia/trigger de cada add.
- Precio medio ponderado de la posición agregada.
- SL/TP agregado y pérdida máxima si falla toda la secuencia.
- MAE/MFE, tiempo expuesto y coste real de comisión/slippage por secuencia.
- Riesgo acumulado por cuenta, por sesión y por conjunto de cuentas correlacionadas.

### Métricas económicas obligatorias

- Probabilidad de pasar evaluation antes de quemarla.
- Probabilidad de primer payout dado que se llegó a funded.
- Probabilidad y coste de ruina por etapa.
- Intentos esperados y coste esperado hasta primer payout.
- Cash neto esperado por intento y por cohorte de cuentas.
- Expected payout / challenge+activation+reset cost.
- Tiempo esperado hasta cashflow y capital lock.
- Distribución P5/P50/P95 y drawdowns; no evaluar solo promedio.
- Efecto de comisiones, slippage, fills parciales y latencia.
- Sensibilidad a rachas: una estrategia 90% WR debe demostrar qué ocurre con la cola del 10%, incluyendo secuencias consecutivas.
- Correlación entre 40–80 cuentas cuando todas siguen la misma Reference; multiplicar cuentas no multiplica independencia.

### Gate G1

No se compra escala ni se construye fan-out multi-account hasta que exista una región de parámetros con EV neto positivo bajo supuestos conservadores y sin depender de una única combinación extremadamente frágil.

## 🧪 M2 — Estrategias candidatas y simulación

- Partir con pocas estrategias mecánicas de alta frecuencia operativa y alto win rate potencial; estocásticos en TF bajos son **candidato**, no decisión.
- Elegir un solo mercado inicial después de evaluar liquidez, tick value, comisiones, horario y compatibilidad con las reglas de la prop.
- Para una lógica de adds y salidas rápidas, exigir resolución de datos suficiente para reconstruir el path intratrade; una barra OHLC que no resuelva el orden de eventos no puede certificar la estrategia.
- El simulador debe reproducir también la prop: challenge/funded/payout, no solo una curva PnL.
- Separar edge de entrada, lógica de recovery y money management para poder medir cuánto aporta y cuánto riesgo agrega cada componente.

## 🏗️ M3+ — Automatización después de validar la operativa

- **M3 — Vertical slice NinjaTrader:** una Reference + una Execution + SIM + un instrumento + una estrategia.
- **M4 — Integración Echo:** identidad, comandos idempotentes, fills, reconciliación, position truth, límites y observabilidad.
- **M5 — Primera evaluation real:** una cuenta/plan con autorización explícita del owner y presupuesto máximo conocido.
- **M6 — Primer payout y aprendizaje:** comparar simulación versus ejecución real, recalibrar slippage/fills/rules.
- **M7 — Scale-out:** fan-out controlado hacia múltiples cuentas solo después de evidencia de retiro; crecer por cohortes y no saltar directo a 40–80.

## 🚦 Gates del proyecto

| Gate | Condición | Estado |
|---|---|---|
| G0 — Operativa | Estrategia + hardscalping completamente mecánicos, incluidos casos de pérdida | **WIP** |
| G1 — Economía | EV de challenge→primer payout positivo con costes y rules reales | BLOCKED by G0 |
| G2 — Simulación | Replay/path intratrade y simulador de prop reproducibles | BLOCKED by G1 |
| G3 — Execution | Reference→Echo→Execution reconciliado en SIM | BLOCKED by G2 |
| G4 — Real pilot | Primera evaluation real dentro de presupuesto explícito | BLOCKED by G3 + owner |
| G5 — Withdrawal | Primer retiro y discrepancias sim/live entendidas | BLOCKED by G4 |
| G6 — Scale | Cohortes multi-account con límites, observabilidad y kill-switch | BLOCKED by G5 |


## 🧱 Entrega de desarrollo

%% Esta sección siempre queda disponible. En proyectos que cambian código, configuración ejecutable, schemas o infraestructura, es obligatoria: una fila por repo/branch, con SPEC funcional y técnica enlazadas antes de implementar. En proyectos no técnicos, reemplazar la tabla por `_No aplica — <motivo>._`. %%

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| Echo Futures runtime (repo por definir) | TBD tras G0/G1 | TBD | BLOCKED — congelar después de G0/G1 | BLOCKED — congelar después de G0/G1 | NOT STARTED |

## 🧩 Subproyectos

```base
filters:
  and:
    - 'type == "project"'
    - 'file.hasLink(this.file)'
views:
  - type: cards
    name: Subproyectos
    order:
      - file.name
      - note.status
      - note.priority
```

## ✅ Tareas

> [!note]+ Ownership y tarea puente
> `#owner/me` = tuya · `#owner/agent` = de un agente · sin owner = clasifícala.
> El board es **adaptativo según `owner` del frontmatter**:
> - **Proyecto humano** (`owner: me`): muestra tus tareas y las **tareas puente** (`#type/supervision`) que representan proyectos de agente. Las tareas de agente **no** aparecen acá; viven en su propio proyecto.
> - **Proyecto de agente** (`owner: agent`): muestra las tareas del agente.

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. Tipos: #type/dev #type/admin #type/research #type/pr-review #type/supervision. Flags: #blocked #waiting #urgent. Ver [[convenciones]]. %%
> - [x] D1: hacer brain dump + entrevista dirigida de Gerard y congelar su knowledge contract #owner/me #type/research #area/echo
> - [ ] D1: ejecutar research one-shot Gerard público para contraste #owner/agent #type/research #area/echo
> - [ ] D1: ejecutar research one-shot Tradesfera con contrato común #owner/agent #type/research #area/echo
> - [ ] D1: ejecutar research one-shot Psicólogo del Trading con contrato común #owner/agent #type/research #area/echo
> - [ ] Reconstruir una estrategia Gerard completa con evidencia y reglas mecánicas, incluyendo add/recovery y pérdida total #owner/me #type/research #area/echo
> - [ ] Investigar y mecanizar operativa relevante de Tradesfera #owner/me #type/research #area/echo
> - [ ] Investigar y mecanizar operativa relevante de Psicólogo del Trading #owner/me #type/research #area/echo
> - [ ] D2: síntesis adversarial de los tres outputs y seleccionar 1–3 candidatos mecanizables #owner/agent #type/research #area/echo
> - [ ] D3: congelar 1–2 máquinas de estado + modelo matemático del hardscalping #owner/me #type/research #area/echo
> - [ ] D3–D5: construir shortlist mínima de prop/plan y normalizar rules que afectan la operativa #owner/me #type/research #area/echo
> - [ ] D5: modelar challenge→funded→primer payout con fees, resets, drawdown, consistency, slippage y comisiones #owner/me #type/research #area/echo
> - [ ] D3: elegir primer instrumento y dataset después de cruzar microestructura + estrategia + rules de prop #owner/me #type/research #area/echo
> - [ ] D4: obtener backtest/replay reproducible de candidatos #owner/agent #type/research #area/echo
> - [ ] D6: ejecutar validación adversarial y robustness #owner/agent #type/research #area/echo
> - [ ] D7: emitir GO/ITERATE/NO_GO y, solo si GO, congelar SPEC del MVP #owner/me #type/supervision #area/echo
> - [ ] Cerrar G0 y G1 antes de autorizar implementación NinjaTrader/Echo #owner/me #type/supervision #area/echo

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label]of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any)dv.paragraph("_Sin tareas._");}
const owner=((dv.current().owner)==="agent")?"agent":"me";
const all=dv.current().file.tasks.array();
const primary=all.filter(t=>has(t,`owner/${owner}`));
const loose=all.filter(t=>!has(t,"owner/me")&&!has(t,"owner/agent"));
dv.header(3, owner==="agent"?"🤖 Tareas del agente":"🧍 Mis tareas");
board(primary);
if(loose.length){dv.header(3,"🧺 Sin owner (clasificar)");render(loose);}
```

%% Rollup de iniciativa — descomentar solo en proyectos padre para ver las tareas #owner/me (incluye puentes) de todos los subproyectos, agrupadas por nota. Cambiar la ruta por la carpeta de esta iniciativa. Nunca muestra tareas de agente.
```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
const ord={" ":0,"/":1,"r":2,"x":3,"X":3,"-":4};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
const pages=dv.pages('"10-projects/CARPETA-DE-LA-INICIATIVA"');
for(const p of pages.sort(x=>x.file.name)){const t=p.file.tasks.array().filter(x=>has(x,"owner/me")&&x.status!=="x"&&x.status!=="X").sort((a,b)=>(ord[a.status]??9)-(ord[b.status]??9));if(t.length){dv.el('h4',p.file.link);render(t);}}
```
%%

## 📆 Bitácora

%% Log diario para las dailies. Una línea por día con lo avanzado / blockers. %%
- **2026-09-23** — Proyecto creado y alcance corregido hacia operativa-first. Se registran como hipótesis: estrategias de alto win rate y TF bajo, hardscalping/recovery con aumento de exposición, gestión agresiva orientada a challenge/funded/payout y escalado futuro a decenas de cuentas. G0/G1 bloquean desarrollo hasta demostrar reglas mecánicas y economía positiva.
- **2026-09-23** — Activado management por `technical-project-manager`: horizonte máximo 7 días. Discovery se limita a tres one-shots paralelos (Gerard/Tradesfera/Psicólogo) bajo contrato común + entrevista Gerard; D2 síntesis, D3 mecanización, D4 backtest, D5 prop simulation, D6 robustness, D7 decisión y eventual freeze MVP.
- **2026-09-24** — Recibido primer brain dump del curso de Gerard + captura de risk table. Se separan tres motores: recovery adverso intra-trade, pyramiding positivo y variable-risk inter-trade. Derivado modelo provisional de bandas sobre average price y detectada contradicción útil en tabla 1.20/1:1.5: tras dos pérdidas, el siguiente win ya no recupera la secuencia.
- **2026-09-24** — Entrevista Gerard v1 suficientemente cerrada para avanzar: discrecionalidad pasa a parametrización experimental. Confirmado riesgo/TP monetario recalculado sobre average price. Derivada fórmula m=1+1/b para recovery geométrico constante y refrescada economía Topstep vigente; pricing path pasa a variable del simulador.

## 🧭 Decisiones

- **2026-09-23 — Echo Futures es una iniciativa raíz bajo [[Echo]], relacionada con [[Trading]], y no un tercer track de [[Echo — Producto Integrado]].**
- **2026-09-23 — Operativa-first:** estrategia, hardscalping, money management y prop economics se definen antes de arquitectura o desarrollo.
- **2026-09-23 — “Quemar cuentas hasta retirar” se modela como hipótesis económica falsable:** el criterio es cash neto y distribución de resultados, no pass rate ni win rate aislados.
- **2026-09-23 — No etiquetar la técnica de Gerard como martingala sin evidencia:** reconstruir trigger, sizing, límites y salida exactos.
- **2026-09-23 — Escala 40–80 cuentas es target de capacidad, no MVP:** el sistema escala por cohortes después de obtener evidencia real de payout.
- **2026-09-23 — Reference/Execution de Echo se conserva como dirección arquitectónica, pero su SPEC queda bloqueada hasta G0/G1.**
- **2026-09-23 — Horizonte máximo inicial = 7 días:** discovery operativo se comprime a 48h mediante tres research one-shot paralelos + entrevista Gerard; el resto del horizonte se dedica a mecanización, backtest/replay, prop simulation y validación adversarial.
- **2026-09-23 — Piloto “~20 cuentas de 10K” es una hipótesis ilustrativa, no una decisión:** cantidad, nominal, prop y presupuesto se dimensionan en D7 desde reglas y economía verificadas.

## 🔗 Docs / Links

- [[Echo]] — área de producto y automatización.
- [[Trading]] — área relacionada para operativa, prop firms y riesgo.
- [[Echo — Producto Integrado]] — producto vigente; Echo Futures se mantiene independiente para no alterar sus dos tracks congelados.
- [[Echo + Echo Forge — Environment Contract]] — será autoridad de ambiente si Echo Futures reutiliza infraestructura Echo/Aranea; no concede autorización de ejecución.

## 💡 Ideas

%% Captura ideas sueltas del proyecto al final. Si maduran, promover a tarea o a nota de idea (70-templates/idea.md). %%

### Backlog de ideas

- Cohortes de cuentas con perfiles de agresividad distintos para estimar experimentalmente la frontera pass-rate / payout-rate / burn-rate.
- Risk profile dinámico por estado económico de la cuenta en vez de una gestión única.
- Reference única con fan-out a muchas Executions y límites locales por cuenta.
- Simulador Monte Carlo sobre secuencias de trades reales para estimar costo hasta payout y riesgo de cola.
- Clasificar cuentas como inventario económico: evaluation, funded pre-payout, payout-protected, burned, retired.

### Motivos / principios

- **Operativa antes que software.**
- **Cash retirado > balance nominal > win rate.**
- **High win rate no elimina tail risk.**
- **Force brute solo sirve si el EV neto después de quemas es positivo.**
- **KISS:** una prop, un instrumento y una estrategia antes de multiplicar cuentas.
- **YAGNI:** no construir multi-prop, multi-market ni 80-account fan-out antes de demostrar primer payout.
- **Separación SOLID:** signal/strategy, recovery logic, money management, prop rules y execution deben ser medibles y reemplazables por separado.

### Memoria pública / interna

%% Opcional para proyectos de agentes o conocimiento: definir qué memoria gobierna el sistema y cuál gobierna el agente, y por qué existe cada una. %%
- **Memoria pública:** por definir cuando G0/G1 produzcan reglas reutilizables verificadas.
- **Memoria interna:** no requerida para crear el proyecto; continuidad vive en esta nota hasta que exista delta durable específico.
- **Motivo:** evitar convertir hipótesis tempranas en memoria canónica.

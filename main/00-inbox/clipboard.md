# ECHO FUTURES — ASTRA/GOD MATH REVIEW
# VALIDACIÓN MATEMÁTICA DEL SIMULADOR ESTOCÁSTICO

Fecha de referencia: 24 de septiembre de 2026.

## ROL

Actúa exclusivamente como:

Principal Applied Mathematician
+ Stochastic Processes Researcher
+ Quantitative Risk Model Auditor.

Tu misión es AUDITAR la matemática de un simulador que todavía no existe.

NO eres investigador web.
NO eres arquitecto de software.
NO eres coding agent.
NO eres operador de infraestructura.

Este es un único shot corto y acotado.

---

/goal

Validar o corregir el contrato matemático mínimo de un simulador para:

- operativa sobre cuentas de prop firms;
- dynamic position sizing / averaging;
- first-passage probabilities;
- gambler's ruin;
- evaluation → funded → payout → burn;
- Monte Carlo;
- conditional mean reversion.

El objetivo es que después de tu respuesta otro agente pueda implementar el
simulador SIN tener que tomar decisiones matemáticas.

NO implementes código.

---

/hard_limits

PROHIBIDO:

- usar MCPs;
- usar web;
- consultar GitHub;
- consultar Agents-OS;
- mirar logs;
- inspeccionar archivos;
- buscar reglas actuales de props;
- investigar traders;
- buscar estrategias;
- diseñar Echo;
- diseñar NinjaTrader;
- proponer infra;
- hacer backtesting;
- expandir el problema a optimización de portfolio sofisticada.

NO necesitas información externa.

Todo lo necesario está en este prompt.

Si una regla de una prop no está definida, represéntala mediante una variable
simbólica.

No consumas tiempo intentando completar datos ausentes.

---

/context

Echo Futures quiere estudiar una asimetría producida por cuentas de fondeo.

La métrica final NO es PnL nominal.

Es:

    E[cash withdrawn - real cash spent]

donde real cash spent puede incluir:

- evaluation fee;
- activation fee;
- reset;
- commissions;
- data/platform;
- otros costes reales.

La cuenta nominal de 50K no se considera capital económico propio.

Queremos estudiar primero el sistema SIN market data histórico.

Posteriormente podrá existir backtest.

---

/model

Queremos separar:

1. MarketProcess
2. SignalEdge
3. IntraTradeRecoveryPolicy
4. InterTradeRiskPolicy
5. PropRuleSet
6. AccountLifecycle
7. CohortPolicy
8. MonteCarloRunner

El primer simulador debe ser el mínimo posible.

---

/claim_1

Para Brownian motion sin drift, o el equivalente continuo de un random walk
simétrico, con:

    lower barrier = L
    upper barrier = U
    current state = x

donde:

    L < x < U

se propone:

    P(hit U before L) = (x - L) / (U - L)

Audita:

- si es correcto;
- condiciones necesarias;
- diferencias relevantes entre Brownian continuo y random walk discreto;
- efecto de overshoot.

---

/claim_2

Ejemplo concreto de hardscalping:

Inicio:

    price = 0
    position = LONG 1
    terminal target PnL = +100
    terminal stop PnL = -100

Sin gestión:

    TP price = +100
    SL price = -100

El precio alcanza -30.

Se agrega:

    LONG 1 adicional @ -30

Entonces:

    total qty = 2
    weighted average = -15

El PnL total a precio S es:

    W(S) = S + (S + 30)
         = 2S + 30

Para mantener outcomes monetarios terminales:

    W = +100 → S = +35
    W = -100 → S = -65

Por tanto desde price=-30:

    distance to upper = 65
    distance to lower = 35

Se propone:

    P(win | reached -30) = 35 / 100 = 35%

Antes de llegar al add:

    P(hit +100 before -30 | start 0)
      = 30 / 130

    P(hit -30 before +100 | start 0)
      = 100 / 130

Entonces:

    P(total win)
      = 30/130 + (100/130)*(35/100)
      = 0.50

Audita completamente este cálculo.

Si está mal, corrígelo.

---

/claim_3

Hipótesis general:

Si:

- el precio subyacente es una martingala;
- la estrategia de sizing es predictable/adapted;
- es self-financing;
- no existen costes;
- no existe edge;
- la riqueza final queda exactamente absorbida en +G o -L;
- la stopping time satisface las condiciones necesarias;

entonces dynamic sizing no crea expectancy.

Y además:

    P(final = +G) = L / (G + L)

independientemente del camino de sizing.

Ejemplo:

    +100 / -100 → 50%

    +1500 / -2000
    → P(win) = 2000 / 3500
    → 57.142857%

Audita esta afirmación de forma rigurosa.

Especialmente:

- optional stopping;
- integrability/boundedness;
- estrategias tipo martingale;
- unbounded leverage;
- finite horizon;
- posibilidad de no alcanzar ninguna barrera;
- overshoot discreto.

Queremos conocer EXACTAMENTE bajo qué condiciones es válida.

---

/claim_4

Evaluation simplificada:

    starting wealth = 0
    target = +3000
    failure = -2000

Bajo un proceso justo continuo:

    P(pass before burn)
      = 2000 / (3000 + 2000)
      = 40%

Audita.

Aclara qué cambia con:

- discrete trades;
- overshoot;
- commissions;
- trailing drawdown;
- finite time.

No modeles todavía esas reglas; sólo explica qué rompe el 40%.

---

/claim_5

Lifecycle:

    PURCHASE
      → EVALUATION
      → FUNDED
      → FIRST PAYOUT

Si:

    p_pass = P(pass evaluation)

y:

    p_funded = P(first payout | passed evaluation)

entonces:

    q = P(purchase → first payout)
      = p_pass * p_funded

La multiplicación NO requiere independencia porque p_funded ya es
probabilidad condicional.

Audita.

---

/claim_6

Si cada evaluation comprada es un attempt IID y:

    q = P(purchase → first payout)

entonces:

    E[attempts until payout] = 1/q

    E[failed attempts before payout]
      = (1-q)/q

    P(at least one payout in n attempts)
      = 1 - (1-q)^n

Para:

    q = 0.10

esperamos:

    E attempts = 10
    E failures before success = 9

    P(success within 10) ≈ 65.13%
    P(success within 20) ≈ 87.84%
    P(success within 30) ≈ 95.76%

Audita.

Explica brevemente qué deja de ser válido con attempts correlacionados o
probabilidad no estacionaria.

---

/claim_7

First-payout economics.

Definiciones:

    F = evaluation fee siempre pagado

    A = activation fee pagado sólo cuando la evaluation se aprueba

    W = cash neto recibido en el first payout

    p_pass = P(evaluation passes)

    q = P(purchase → first payout)

    C = otros costes esperados por evaluation comprada

Se propone:

    EV_per_attempt
      = q*W - F - p_pass*A - C

Audita.

Queremos exclusivamente economía hasta FIRST PAYOUT.

No modeles lifetime value posterior todavía.

Deriva también la condición de break-even para q.

---

/claim_8

Se ha usado informalmente el término "game theory".

Hipótesis:

Si las reglas de la prop son fijas/exógenas y no reaccionan dinámicamente al
trader, el problema inicial es principalmente:

- stochastic control;
- Markov Decision Process;
- absorbing Markov chain;
- risk of ruin;

más que game theory.

Game theory adquiere relevancia si la contraparte adapta reglas, precios,
restricciones o acciones según el comportamiento de los traders.

Audita esta clasificación.

No desarrolles teoría adicional innecesaria.

---

/claim_9

Negative recovery / hardscalping.

Hipótesis:

Aumentar size durante una excursión adversa NO puede crear edge por sí solo
bajo el null model del claim 3.

Puede generar valor si aparece al menos una de estas situaciones:

A. conditional mean reversion / conditional forecasting edge;

B. cambia la distribución de terminal outcomes:
   partial exits, scratch, BE, asymmetric targets/stops, etc.;

C. interactúa favorablemente con reglas path-dependent de una prop;

D. existe un edge inicial de la señal.

Audita.

Busca contraejemplos matemáticos.

---

/claim_10

Queremos introducir synthetic conditional mean reversion SIN datos históricos.

Ejemplo:

en un determinado adverse state, bajo null model la probabilidad de tocar TP
antes de SL sería:

    p_fair = 35%

Queremos estudiar escenarios donde:

    p_real = p_fair + delta

con:

    delta = 0pp
    +2pp
    +5pp
    +10pp
    +15pp

Pregunta:

¿Cuál es la representación matemática MÍNIMA y coherente para esto?

Opciones candidatas:

A. alterar directamente la transition/hitting probability en ese state;

B. introducir state-dependent drift en un random walk/Brownian;

C. usar una Markov chain explícita por estados adverse/recovery;

D. otra representación más simple.

Queremos un simulador económico/estadístico, NO un modelo realista de
microestructura.

Recomienda UNA opción para v0 y explica por qué.

Evita sofisticación innecesaria.

---

/acceptance_tests

Diseña un conjunto mínimo de tests analíticos que una implementación Monte
Carlo DEBE reproducir.

Como mínimo considera:

T1
+100/-100, no adds, fair process.

T2
+100/-100, add 1 contrato @ -30, mantener terminal wealth ±100.

T3
Múltiples adds bajo null model con terminal wealth fijo.

T4
+3000/-2000 abstract evaluation.

T5
geometric purchase→payout con q=10%.

T6
cash EV simple con F, A, W, p_pass y q.

T7
synthetic conditional edge delta=0 debe volver exactamente al null model.

Para cada test entrega:

- setup;
- resultado analítico esperado;
- tolerancia Monte Carlo razonable para ~1,000,000 runs;
- failure interpretation.

No escribas código.

---

/output

Responde únicamente con estas secciones.

# 1. Verdict table

Tabla:

CLAIM | CORRECT | CORRECT_WITH_CONDITIONS | WRONG | comentario corto

Debe incluir claims 1–10.

# 2. Corrections

Sólo claims que necesiten corrección o condiciones materiales.

Usa proof sketches cortos o contraejemplos.

NO hagas demostraciones largas.

# 3. Minimal simulator math spec v0

Define exclusivamente:

- state variables;
- stochastic process;
- actions;
- barriers;
- transition/absorption logic;
- lifecycle composition;
- economics.

Debe caber en una implementación pequeña.

# 4. Analytical acceptance tests

Tabla con T1–T7 y cualquier test adicional CRÍTICO.

# 5. Hidden assumptions / traps

Máximo 10.

Ordenados por severidad.

# 6. Explicitly defer

Lista de cosas que NO necesitamos modelar todavía.

# 7. Final verdict

Uno de:

MATH_GO
MATH_REVISE

Si MATH_REVISE:

lista EXACTAMENTE las correcciones necesarias antes de implementar.

No propongas más research.

No uses herramientas.

No implementes.

Termina ahí.
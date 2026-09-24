# Echo Futures — Astra/GOD Mathematical Review

**Fecha:** 2026-09-24  
**Estado:** MATH_GO  
**Rol:** auditoría matemática del simulador estocástico v0  
**Scope:** first-passage, martingala/optional stopping, lifecycle, economics, synthetic conditional edge.

## Verdict

Los 10 claims fueron aceptados: claims 2 y 5 como correctos sin correcciones materiales; los demás como correctos bajo condiciones explícitas.

## Correcciones/condiciones canónicas

### First-passage

Para Brownian sin drift con barreras fijas (L<x<U):

`P(hit U before L) = (x-L)/(U-L)`.

En random walk discreto la misma fórmula es exacta sólo si estado y barreras pertenecen a una retícula alcanzable sin overshoot. Con saltos/overshoot deben usarse valores de salida esperados, no recortar artificialmente a la barrera.

### Add self-financing — caso canónico

Inicio:

- price = 0;
- LONG 1;
- terminal PnL +100/-100.

Al llegar a -30 se agrega LONG 1:

- qty = 2;
- average = -15;
- riqueza antes y después del add = -30;
- nuevo TP price = +35;
- nuevo SL price = -65.

Desde -30:

`P(win | add) = 35%`.

Composición total:

`30/130 + (100/130)*(35/100) = 50%`.

Sin add, desde -30 la probabilidad de +100 antes de -100 también es 35%. El add cambia precios de salida y duración, no la probabilidad bajo el null model.

### Optional stopping / dynamic sizing

Sea:

`X_t = X_0 + ∫ H_s dS_s`.

Para concluir invariancia de expectancy se necesita:

- posición predecible e integrable;
- stopping time con absorción;
- conservación de esperanza / martingala detenida uniformemente integrable o condición suficiente equivalente;
- riqueza terminal exactamente en +G o -L;
- ausencia de costes/edge/overshoot material en el modelo.

Entonces:

`P(X_tau=G)=L/(G+L)`.

Payoff terminal acotado por sí solo no basta si la estrategia puede requerir exposición/pérdidas intermedias no integrables (martingale doubling clásico).

### Evaluation abstracta

Con target +3000 y failure -2000 bajo proceso justo continuo y barreras estáticas:

`P(pass)=2000/(3000+2000)=40%`.

Lo alteran overshoot, costes sobre equity, trailing drawdown, finite horizon y cualquier cambio en outcomes/path rules.

### Lifecycle

`q = P(purchase→first payout) = p_pass * P(first payout | passed)`.

No requiere independencia porque el segundo término es condicional.

Para attempts IID con conversión q:

- `E[attempts]=1/q`;
- `E[failures before payout]=(1-q)/q`;
- `P(at least one payout in n)=1-(1-q)^n`.

Con q=10%:

- attempts esperados = 10;
- failures esperados = 9;
- <=10 attempts: 65.1322%;
- <=20: 87.8423%;
- <=30: 95.7609%.

### Economics to first payout

`EV_attempt = q*W - F - p_pass*A - C`.

Donde:

- F = evaluation fee;
- A = activation fee pagada al aprobar;
- W = cash neto condicionado a recibir first payout;
- C = otros costes esperados por evaluation comprada.

Break-even:

`q_BE=(F+p_pass*A+C)/W`.

Debe cumplirse `q_BE <= p_pass`.

### Hardscalping

Separar:

1. win probability;
2. trading wealth expectancy;
3. personal cash expectancy.

Negative recovery no crea edge por size puro bajo null + optional stopping válido.

Puede aportar valor por:

- conditional forecasting/mean-reversion edge;
- exposición alineada con drift condicional;
- distribución terminal distinta;
- contractual asymmetry/limited liability de la prop.

La asimetría de cash personal no contradice la martingala del trading nominal.

### Game theory

Con reglas de prop fijas/exógenas el problema inicial es stochastic control / MDP / absorbing process / risk of ruin. Game theory requiere interacción estratégica entre decisiones de agentes.

## Minimal simulator math v0

### State

Por attempt:

- phase: EVALUATION | FUNDED | FAIL | FIRST_PAYOUT;
- realized phase equity B al inicio del trade;
- relative price s;
- long position h;
- bookkeeping term b;
- trade PnL `Y=b+h*s`;
- phase equity `E=B+Y`;
- next adverse add index;
- synthetic-edge available flag;
- personal cash K.

Config:

- F, A, C, W;
- phase barriers (-D_z, T_z);
- trade stop/target (-ell, G);
- initial h0;
- finite adverse add list;
- h_max;
- synthetic delta.

### Null process

`ds_t=dB_t`.

v0 no discretiza tiempo. Usa kernel exacto de first-passage entre el próximo evento inferior y superior.

### Actions

Open:
`s=0, b=0, h=h0`.

Add Δh at price s:
`h'=h+Δh`
`b'=b-Δh*s`

Esto conserva instantáneamente `Y`.

No partial exits. Close total on barrier. Inter-trade policy fija en v0.

### Barriers

Trade exits: `Y=-ell` y `Y=G`.

Phase barriers: `E=-D_z` y `E=T_z`.

Lower active price:

`a_term=max((-ell-b)/h, (-D_z-B-b)/h)`.

Upper active price:

`b_term=min((G-b)/h, (T_z-B-b)/h)`.

El próximo adverse add es un evento inferior sólo si está estrictamente entre lower barrier y current price.

Tie order:

1. phase barrier;
2. trade close;
3. add.

### Synthetic conditional edge v0

En un adverse state elegido, si el null hitting probability es `p0`, usar:

`p_delta=p0+delta`

con `0<=p_delta<=1`.

Astra recomienda para v0 aplicar esta perturbación una sola vez después del último add previsto, sin eventos intermedios pendientes. Esto modela un conditional hitting edge, no una dinámica física de mean reversion.

**Project note:** para representar mejor Gerard se prevé una extensión posterior de edge por adverse state; no mezclarla con el null engine hasta certificar el kernel.

### Lifecycle

PURCHASE → EVALUATION → FUNDED → FIRST_PAYOUT.

- purchase: charge F+C;
- evaluation lower: FAIL;
- evaluation upper: charge A, enter FUNDED, reset phase equity;
- funded lower: FAIL;
- funded upper: receive W, absorb FIRST_PAYOUT.

Under null/static barriers:

`p_pass=D_eval/(T_eval+D_eval)`

`p_funded=D_fund/(T_fund+D_fund)`

`q=p_pass*p_funded`.

## Analytical acceptance tests

For N≈1,000,000 independent runs, probability tolerance:

`5*sqrt(p*(1-p)/N)`.

| Test | Setup | Expected |
|---|---|---|
| T1 | fair, ±100, no adds | p=0.5; E[X]=0 |
| T2 | add +1 at -30, terminal ±100 | reach add=10/13; p(win|add)=0.35; total p=0.5; E[X]=0 |
| T3 | add +1 at -20 and -40, terminal ±100 | total p=0.5; E[X]=0 |
| T4 | evaluation +3000/-2000 | pass=0.4; burn=0.6 |
| T5 | IID purchase→payout q=0.1 | mean attempts=10; failures=9; success <=10/20/30 = 0.651322/0.878423/0.957609 |
| T6 | p_pass=.4; p_funded=.25; F=100 A=50 W=1500 C=10 | q=.1; EV=20; q_BE=.0866667 |
| T7 | T2 synthetic kernel delta=0 | identical to null |
| T8 | T2 with delta=.10 at adverse state | conditional win=.45; total win=15/26≈.5769231; E[X]=200/13≈15.384615 |

Deterministic invariants:

- each add conserves Y except numeric roundoff;
- J <= I always;
- h <= h_max;
- no out-of-barrier exit in continuous model;
- invalid probability rejects configuration; never silently clips.

## Hidden assumptions

1. Nominal wealth and personal cash are distinct.
2. Optional stopping conditions matter.
3. Absorption must occur.
4. v0 assumes continuous monitoring/exact execution/no overshoot.
5. Adds are self-financing.
6. delta is an assumption/sensitivity input, not empirical evidence.
7. High win rate does not imply positive expectancy.
8. Geometric attempt formulas require IID or correct conditional probabilities.
9. Costs must be counted exactly once.
10. Exact hitting kernel omits time/path interior.

## Explicitly deferred

- historical market data/backtest;
- empirical delta estimation;
- physical mean-reversion dynamics;
- jumps/slippage/execution costs against equity;
- trailing drawdown/daily limits/consistency/calendar;
- partial exits/scratch/BE;
- sizing optimization;
- correlated attempts;
- limited personal budget;
- payouts after first;
- game-theoretic prop response;
- infrastructure.

## Final verdict

**MATH_GO**

# ECHO FUTURES — D4-B2 / Q13
# GERARD HARDSCALPING MONEYMANAGEMENT EXACT SPEC

**Status:** OWNER-CORRECTED CANDIDATE — READY FOR MANAGER QA
**Supersedes inside Q13:** Strategy-owned profit target; equity-percentage-first economic model.
**Scope:** MoneyManagement only. No Strategy-specific branch, no provider-specific subclass, no implementation, no D4 gate.

## 1. Executive decision

GerardMM V1 queda definido como una política monetaria account/day-aware. Strategy entrega entry technical intent, direction y technical_stop/reference; Strategy puede cerrar su propio technical cycle mediante CLOSE/CLOSE_ALL, pero no fija profit target. GerardMM posee current_loss_budget_money, current_profit_objective_money, sizing, hardscalping, protective stop y profit-taking monetario.

La configuración Owner inicial para EVALUATION queda congelada como datos: business day 1 SL USD 2000 / TP USD 1500; business day 2 SL USD 2000 / TP USD 1500. Los valores FUNDED no se inventan. El schema admite FUNDED_INITIAL y FUNDED_STEADY sin cambiar el algoritmo.

D4-A2 y D4-A3 permanecen authority. GerardMM decide una quantity exacta; echo/provider_rules(account_id) puede autorizar exactamente esa quantity o denegar. No existe silent resize, probing iterativo, hard-cap override ni max_admissible_qty.

R se conserva sólo como unidad técnica de spacing respecto de P0/D0. Ya no es authority económica de SL ni TP.

## 2. Evidence boundary

La evidencia pública disponible respalda sólo el concepto general de adverse adds/DCA, positive pyramiding y protección dinámica con confianza limitada/moderada. No demuestra thresholds, ratios, cantidad de adds, fórmula monetaria ni horarios exactos como reglas universales de Gerard.

Los valores SL=2000 y TP=1500 para evaluation day 1/2 son OWNER-PROVIDED INITIAL CONFIGURATION.

Los thresholds 0.25R/0.50R, ratios 1.0/0.5 y límites 2/1 continúan como research/test seeds que LIVE/DEMO debe declarar explícitamente en GerardMMConfig.

## 3. Ownership boundaries

Strategy posee setup técnico, direction, entry semantics, technical_stop/reference y su lifecycle técnico. No posee profit target, desired USD profit ni sizing.

GerardMM vive como plugin stateful dentro de echo/operation. Posee economic plan selection, monetary objective, monetary loss budget, initial sizing, adds, protective stop y profit termination.

Operation sigue siendo authority de lifecycle, Orders, Fills, signed logical exposure, average fill state derivable, direction immutable, q_exec_max/local claims y serialization.

Account state entrega observación account/day necesaria para la economía Gerard. No se crea portfolio aggregate ni cross-account state.

ProviderRuleSet completo permanece read-only en GerardMM. Sus evaluadores tipados pueden producir constraints conservadores; echo/provider_rules(account_id) sigue siendo authority account-wide y final.

Position no reemplaza Fill truth ni Operation exposure.

## 4. Small economic configuration

GerardMMConfig contiene una pieza pequeña de configuración; no es workflow engine ni DSL.

~~~text
GerardMMConfig {
  economics {
    currency: USD

    evaluation_by_business_day {
      1 { loss_budget_money: 2000, profit_objective_money: 1500 }
      2 { loss_budget_money: 2000, profit_objective_money: 1500 }
    }

    funded {
      initial { loss_budget_money: REQUIRED_CONFIG, profit_objective_money: REQUIRED_CONFIG }
      steady  { loss_budget_money: REQUIRED_CONFIG, profit_objective_money: REQUIRED_CONFIG }
    }
  }

  scaling {
    adverse_step_R
    max_adverse_adds
    adverse_add_ratio

    positive_step_R
    max_positive_adds
    positive_add_ratio
  }
}
~~~

Para EVALUATION, account_state debe entregar trading_business_day_ordinal dentro del stage actual. Matching es exacto contra evaluation_by_business_day. Day 3+ no hereda silenciosamente day 2: si no existe row explícita, GERARD_ECONOMIC_PLAN_UNRESOLVED y new risk fail-closed.

Para FUNDED, account_state/config debe entregar funded_mode=INITIAL|STEADY. Q13 no inventa cuándo cambia INITIAL→STEADY; esa selección es dato de account/control-plane. El plan numérico correspondiente debe existir antes de habilitar new risk.

El config efectivo queda pinneado en el snapshot MM de la Operation según D2-08. Una selección posterior nunca puede aflojar un protective stop ya comprometido.

No se infiere stage desde strings de provider ni se crean TopstepGerardMM, TradeDayGerardMM u otras subclases.

## 5. Required normalized inputs

~~~text
GerardMMInput {
  gerard_config

  signal {
    direction
    entry_semantics
    technical_stop
  }

  account_state {
    account_currency
    economic_stage                 # EVALUATION | FUNDED
    trading_business_day_ordinal?  # required for EVALUATION
    funded_mode?                   # INITIAL | STEADY, required for FUNDED

    account_day_id
    account_day_realized_pnl_money
    account_day_current_pnl_money
    pnl_snapshot_version
  }

  provider_rule_set_read_only
  contract_specs_pinned
  operation_state
  orders
  fills
  trigger
  market_context_decision_scope
  runtime_ts
}
~~~

account_day_id y sus PnL usan la DayBoundary authority ya congelada por D2-05/provider_rules; no usan ExchangeSession date como sustituto.

account_day_realized_pnl_money es PnL realizado account-wide del day corriente según la observación autoritativa disponible. Incluye realized de Operations previas y partial exits de la Operation actual.

account_day_current_pnl_money es PnL corriente account-wide del mismo day, incluyendo realized + unrealized observado por la Account. GerardMM lo usa para loss safety; no intenta atribuir el unrealized de otras Operations.

Si los inputs económicos requeridos están ausentes, stale o en currency no convertible de forma determinista, new risk falla cerrado. Salidas/safety no se bloquean por falta de datos de new risk.

## 6. Economic plan resolution

~~~text
IF economic_stage == EVALUATION:
  plan =
    economics.evaluation_by_business_day[trading_business_day_ordinal]

IF economic_stage == FUNDED:
  plan =
    economics.funded[funded_mode]

IF exactly one plan does not resolve:
  economic_plan = UNRESOLVED
  new risk = DENY locally
~~~

La identidad mínima observable del plan es:

~~~text
economic_plan_key
account_day_id
loss_budget_money
profit_objective_money
currency
~~~

No se crea entidad GerardMMPlan ni service adicional; es config + resolución pura.

## 7. Profit objective semantics

~~~text
current_profit_objective_money =
  plan.profit_objective_money
~~~

Sea T=current_profit_objective_money.

Sea D=account_day_realized_pnl_money.

Para la Operation viva, con direction sign d (+1 LONG, -1 SHORT), open quantity Q>0, fill-derived average open price A y point_value V en account currency, el unrealized de esta Operation al exit-side mark M es:

~~~text
U_op(M) =
  d * Q * (M - A) * V
~~~

M usa bid para LONG y ask para SHORT.

El realized de cualquier partial exit de esta Operation ya pertenece a D. GerardMM no suma unrealized de otras Operations al profit objective; eso evita convertir Q13 en portfolio manager. Cuando esas exposiciones realizan PnL, su resultado entra a D por Account state.

~~~text
current_profit_progress_money =
  D + U_op(M)

remaining_profit_objective_money =
  max(0, T - current_profit_progress_money)
~~~

Si no existe exposición Q, U_op=0.

Si D>=T antes de crear new risk, GerardMM no abre una nueva Order para ese account day.

Si una Operation está viva y remaining_profit_objective_money=0, profit termination gana precedencia sobre cualquier ADD/PYRAMID: bloquea new risk y entra al exit path de §18.

### Dynamic implicit target mark

No se persiste fixed target price. Para observabilidad y trigger determinista, la marca implícita que haría D+U_op=T es:

~~~text
target_mark_raw =
  A + d * ((T - D) / (Q * V))
~~~

Tick rounding conservador:

~~~text
LONG:
  target_mark = round_up_to_tick(target_mark_raw)

SHORT:
  target_mark = round_down_to_tick(target_mark_raw)
~~~

Cada Fill, partial reduction o cambio de D puede cambiar A, Q o realized PnL; target_mark se recalcula y no es authority persistida.

Los exit fees futuros aún no realizados no se inventan. D usa realized net según Account authority. Si más adelante existe fee model determinista para open exposure, puede entrar como input sin cambiar la frontera.

## 8. Loss budget semantics

~~~text
configured_loss_budget_money =
  plan.loss_budget_money
~~~

Sea L=configured_loss_budget_money.

Owner interpreta SL=X como límite económico del account day, no como allowance independiente por trade.

Sea P_day=account_day_current_pnl_money. El headroom hasta el floor -L es:

~~~text
owner_drawdown_headroom_money =
  max(0, L + P_day)
~~~

Para que ganancias previas no amplíen el risk appetite por sobre el SL configurado:

~~~text
owner_remaining_loss_budget_money =
  min(L, owner_drawdown_headroom_money)
~~~

Ejemplos:

~~~text
P_day = 0       and L = 2000 -> owner remaining = 2000
P_day = -500    and L = 2000 -> owner remaining = 1500
P_day = +500    and L = 2000 -> owner remaining = 2000
P_day <= -2000  and L = 2000 -> owner remaining = 0
~~~

Owner trading objective y provider hard rule siguen siendo constraints distintos.

Para cada hard monetary ProviderRuleSet family aplicable, su evaluator tipado produce RemainingLossBudget(rule, account_state) en account currency:

~~~text
provider_remaining_loss_budget_money =
  min(all resolved hard monetary provider headrooms)

if no hard monetary provider family applies:
  provider_remaining_loss_budget_money = +infinity

if an applicable hard monetary family cannot be evaluated safely:
  provider_remaining_loss_budget_money = 0 for new risk
~~~

Effective conservative budget:

~~~text
current_loss_budget_money =
  min(
    owner_remaining_loss_budget_money,
    provider_remaining_loss_budget_money
  )
~~~

echo/provider_rules(account_id) sigue siendo final account-wide authority y todavía debe grant/revalidate toda quantity aplicable.

## 9. Initial sizing

GerardMM requiere Strategy technical_stop y un executable entry reference.

~~~text
P0 = ask for LONG MARKET
P0 = bid for SHORT MARKET

S0 = technical_stop
D0 = abs(P0 - S0)
D0_ticks = D0 / tick_size

require D0_ticks >= 1
require S0 < P0 for LONG
require S0 > P0 for SHORT
~~~

Para entry type exacto no-MARKET, P0 es el precio exacto entregado por Strategy. Sin precio exacto, MM_NO_ACTION.

~~~text
risk_per_contract_money =
  D0_ticks * tick_value_account

q_risk =
  floor(current_loss_budget_money / risk_per_contract_money)

q_ceiling =
  min(
    q_risk,
    contract.qty_max if present,
    provider PER_ORDER max contracts if applicable
  )

q0 =
  NormalizeQtyDown(q_ceiling)
~~~

Si q0=0, MM_NO_ACTION.

Shared caps no generan max_admissible_qty. q0 exacta atraviesa D4-A2 reservation y D4-A3 ReservationRevalidate. DENIED/INVALID no dispara probing con quantity menor.

0.5% equity deja de formar parte de la definición económica Owner.

## 10. Technical stop + monetary stop + provider constraints

Strategy technical_stop es referencia de invalidación/protección y GerardMM jamás puede alejarla.

GerardMM conserva S_prev, el protective stop efectivo más protector ya comprometido. S_prev se obtiene de la Order protectora; no necesita scalar duplicado en mm_state.

Para Q>0 y exit-side mark M:

~~~text
money_distance =
  current_loss_budget_money / (Q * V)

money_stop_raw =
  M - d * money_distance
~~~

Rounding siempre hacia más protección:

~~~text
LONG:
  money_stop = round_up_to_tick(money_stop_raw)
  desired_stop = max(S0, S_prev, money_stop)

SHORT:
  money_stop = round_down_to_tick(money_stop_raw)
  desired_stop = min(S0, S_prev, money_stop)
~~~

Tras Fill de favorable pyramid se mantiene además protección mínima en aggregate break-even:

~~~text
LONG:
  desired_stop = max(desired_stop, round_up_to_tick(A))

SHORT:
  desired_stop = min(desired_stop, round_down_to_tick(A))
~~~

Si current_loss_budget_money<=0 o el exit-side mark ya cruzó desired_stop antes de poder instalarlo, GerardMM inicia termination/protection exit; no publica un STOP inválido detrás del mercado.

La garantía es planned/account-snapshot safety, no promesa contra gap/slippage/venue breach. Fill truth siempre gana.

## 11. R as technical spacing unit only

GerardMM conserva una unidad técnica simple:

~~~text
P0 = initial entry reference
S0 = Strategy technical stop
D0 = abs(P0 - S0)

progress_R =
  d * (M - P0) / D0
~~~

R aquí significa fracción de la distancia técnica inicial P0→S0. No representa profit target, daily SL, equity risk fraction ni ProviderRuleSet budget.

Los adds nunca re-anclan P0/D0.

## 12. Candidate add economic feasibility

Para cualquier adverse ADD o favorable PYRAMID, GerardMM construye una sola quantity configurada y nunca busca cantidades por ensayo.

Antes de pedir provider grant, simula localmente el candidate al executable-side price E:

~~~text
Q_candidate =
  Q + q_add

A_candidate =
  weighted_average_from_actual_fills_plus_candidate(E)

U_current(M) =
  d * Q * (M - A) * V

U_candidate(M) =
  d * Q_candidate * (M - A_candidate) * V

P_day_candidate =
  account_day_current_pnl_money
  + (U_candidate(M) - U_current(M))

owner_remaining_candidate =
  min(
    L,
    max(0, L + P_day_candidate)
  )

current_loss_budget_candidate =
  min(
    owner_remaining_candidate,
    provider_remaining_loss_budget_money
  )

remaining_profit_candidate =
  max(
    0,
    T - (D + U_candidate(M))
  )
~~~

El candidate sólo es localmente elegible si:

- remaining_profit_objective_money > 0.
- economic plan resuelto y current_loss_budget_money > 0.
- quantity completa respeta lattice, Contract qty_max y PER_ORDER local.
- current_loss_budget_candidate > 0.
- con Q_candidate/A_candidate existe desired_stop compatible con Strategy S0, S_prev y candidate monetary budget, al menos un tick por el lado protector del current exit-side mark.
- el implicit target mark derivado de remaining_profit_candidate/Q_candidate no queda más lejos del current mark que el target mark actual.
- ningún termination intent, new_risk_locked ni breach bloquea new risk.

Después de este filtro local, la quantity exacta atraviesa D4-A2/D4-A3. Si provider la deniega, no se prueba otra quantity.

La comparación de target distance es un guard booleano, no un optimizer.

## 13. Negative hardscalping exact rules

LIVE/DEMO debe declarar scaling config. Research/test seed:

~~~text
adverse_step_R = 0.25
max_adverse_adds = 2
adverse_add_ratio = 1.00
~~~

Threshold ordinal i:

~~~text
threshold_i =
  -adverse_step_R * i
~~~

Eligible:

~~~text
Operation ACTIVE with exposure > 0
no termination intent
new_risk_locked == false
branch == NEUTRAL or ADVERSE
adverse_attempts < max_adverse_adds
no pending new-risk add
market quote READY and not stale
remaining_profit_objective_money > 0
progress_R <= threshold_(adverse_attempts + 1)
candidate add passes §12
~~~

~~~text
q_add =
  NormalizeQtyDown(q0 * adverse_add_ratio)
~~~

Al construir el primer adverse ADD, branch=ADVERSE. Positive pyramiding queda deshabilitado para esa Operation.

adverse_attempts incrementa al construir la Order exacta. Partial Fill consume ordinal; no top-up. No se construye otro add hasta que la anterior deje de tener q_exec_max/finality pendiente.

Cada Fill recalcula average, remaining objective, implicit target mark y desired_stop. Protective stop sólo puede mantenerse o apretarse.

DENIED/INVALID o terminal venue failure con cero Fill activa new_risk_locked. Partial Fill conserva el step consumido.

## 14. Positive hardscalping exact rules

LIVE/DEMO debe declarar scaling config. Research/test seed:

~~~text
positive_step_R = 0.50
max_positive_adds = 1
positive_add_ratio = 0.50
~~~

Threshold ordinal i:

~~~text
threshold_i =
  +positive_step_R * i
~~~

Eligible:

~~~text
Operation ACTIVE with exposure > 0
no termination intent
new_risk_locked == false
branch == NEUTRAL or FAVORABLE
positive_attempts < max_positive_adds
no pending new-risk add
market quote READY and not stale
remaining_profit_objective_money > 0
progress_R >= threshold_(positive_attempts + 1)
candidate pyramid passes §12
~~~

~~~text
q_pyramid =
  NormalizeQtyDown(q0 * positive_add_ratio)
~~~

Al construir el primer favorable ADD, branch=FAVORABLE. Negative recovery queda deshabilitado para esa Operation.

positive_attempts incrementa al construir la Order exacta. Partial Fill consume ordinal; no top-up.

Tras cualquier favorable Fill, protective stop queda al menos en aggregate break-even además de límites técnicos/monetarios.

Si candidate no mejora/mantiene la distancia al monetary objective, no se piramidea. Si provider DENIED/INVALID, new_risk_locked=true y no existe retry con quantity menor.

## 15. Adverse / favorable branch interaction

~~~text
branch =
  NEUTRAL
  | ADVERSE
  | FAVORABLE
~~~

Transiciones:

~~~text
NEUTRAL -> ADVERSE
NEUTRAL -> FAVORABLE
ADVERSE -> ADVERSE
FAVORABLE -> FAVORABLE
~~~

No existen ADVERSE -> FAVORABLE ni FAVORABLE -> ADVERSE.

Un trade que hizo adverse recovery puede recuperarse y alcanzar monetary profit objective, pero no empieza luego a pyramid. Un trade que pyramid favorablemente y revierte no se transforma en DCA negativo.

## 16. Minimal mm_state

~~~text
GerardMMState {
  economic_plan_key
  economic_plan_currency

  p0_entry_reference
  s0_technical_stop
  d0_price_distance
  q0_initial

  branch
  adverse_attempts
  positive_attempts
  new_risk_locked

  pending_add_order_id?
  protective_stop_order_id?
}
~~~

No se persiste fixed profit target price.

No se persisten current_loss_budget_money, remaining_profit_objective_money, target_mark, average entry, exposure, account PnL, provider reservations ni Position. Son derivados de authorities corrientes + config + Fills/Orders.

No existe state cross-Operation.

## 17. Trigger requirements and precedence

~~~text
market_event = QUOTE
bar_close = NONE
timers = NONE
~~~

GerardMM corre ante SignalDelivery, Fill, OrderStatus/OrderAction/finality, provider gate result, ForceClose/termination intent y QUOTE notification. Account state/day changes se vuelven visibles en contexto account-specific; una implementación puede entregar AccountStateUpdate como trigger sin cambiar lógica pura.

Toda decisión market-dependent usa D4-A1 decision-scoped MarketContext. No se usa stale/last-known quote para ENTRY, ADD, PYRAMID ni monetary profit trigger.

Prioridad después de aplicar el fact:

1. SAFETY/provider termination intent.
2. Strategy CLOSE/CLOSE_ALL o owner/provider monetary loss exhaustion.
3. Monetary profit objective reached.
4. Exposure invariant/physical-state restrictions: cero new risk.
5. Reconcile protective stop contra exposure real.
6. Evaluate un adverse/favorable add si corresponde.
7. NO_ACTION.

Una vez existe termination intent, no hay new risk.

## 18. Profit exit and protective stop coexistence

GerardMM mantiene exactamente una protective STOP Order lógica para la reducible exposure no reclamada.

El monetary TP no se implementa como segunda full-size resting target Order. target_mark es condición dinámica de decisión.

Cuando remaining_profit_objective_money=0:

1. registra normal MM termination reason MONETARY_PROFIT_OBJECTIVE;
2. cancela/modifica protective STOP según D4-A2;
3. conserva q_exec_max hasta venue finality;
4. sólo cuando existe reducible exposure no reclamada solicita MARKET EXIT por esa quantity exacta;
5. atraviesa reservations/revalidation cuando shared caps aplicables lo exijan.

Fill-vs-cancel no puede double-close.

## 19. Partial fills / cancel / deny

Initial entry partial Fill protege sólo quantity realmente filled. Stop no anticipa Fill futuro.

ADD/PYRAMID partial Fill consume ordinal, recalcula economics con quantity real y no top-up.

Cancel request/ACK no libera local claim ni reservation sin finality autoritativa.

ENTRY DENIED/INVALID: no quantity probing; si MM desiste, Operation converge al terminal reason existente correspondiente.

ADD/PYRAMID DENIED/INVALID: new_risk_locked=true; Operation existente sigue administrándose.

EXIT pendiente por cap/finality conserva termination intent y no hace polling ciego por cada quote; reevalúa frente a input autoritativo que cambie la situación.

Late Fill siempre se incorpora como truth; post-finality breach usa path D4-A2/D2 existente.

## 20. ForceClose / safety precedence

ForceClose corta new risk inmediatamente y tiene precedencia sobre profit objective, Strategy CLOSE y hardscalping.

No emite full close ignorando protective stop/other reducing Orders. Conserva q_exec_max hasta finality, cancela Orders incompatibles, incorpora late Fill y sólo construye close Order por reducible exposure no reclamada.

GerardMM no posee hard-cap override. Si no existe safe unwind mínimo bajo una combinación real de rules, permanece DEFERRED_YAGNI de D4-A2.

## 21. Numerical examples — Owner configuration

Los valores de esta sección son Owner-provided config para evaluation day 1/2; precios/ticks son ejemplos matemáticos.

~~~text
evaluation day 1:
  loss_budget_money = 2000 USD
  profit_objective_money = 1500 USD

evaluation day 2:
  loss_budget_money = 2000 USD
  profit_objective_money = 1500 USD
~~~

### 21.1 Remaining objective

~~~text
D = +400 realized day PnL
current Operation U_op = +350
T = 1500

current_profit_progress_money = 750
remaining_profit_objective_money = 750
~~~

### 21.2 Prior loss reduces Owner headroom; prior profit does not enlarge configured SL

~~~text
L = 2000

P_day = -700
owner_remaining_loss_budget_money = 1300

P_day = +500
owner_remaining_loss_budget_money = 2000
~~~

Si provider hard headroom=900, current_loss_budget_money=min(owner remaining,900).

### 21.3 Initial sizing from money + technical stop

~~~text
tick_size = 0.25
tick_value_account = 5 USD
P0 = 20000
S0 = 19995
D0 = 20 ticks

current_loss_budget_money = 2000
risk_per_contract_money = 100
q_risk = 20 contracts
~~~

Contract/PER_ORDER/shared provider limits aún pueden reducir o negar la acción según sus contracts. GerardMM no usa 0.5% equity como authority primaria.

### 21.4 Dynamic target after quantity changes

LONG, V=20 USD/point, D=400, T=1500.

Antes del add:

~~~text
Q = 4
A = 20000

target_mark_raw =
  20000 + 1100/(4*20)
  = 20013.75
~~~

Después de hypothetical adverse add 4 @ 19998:

~~~text
Q_candidate = 8
A_candidate = 19999

target_mark_raw_candidate =
  19999 + 1100/(8*20)
  = 20005.875
~~~

El target económico implícito se movió por quantity/average. No fue entregado por Strategy ni persistido.

## 22. Invariants

- GMM-I1 — Strategy no posee profit target; GerardMM no consume fixed target price desde Signal.
- GMM-I2 — Owner economic objective y provider hard rule son constraints separados.
- GMM-I3 — current_loss_budget_money=min(owner remaining, provider hard monetary headroom).
- GMM-I4 — Owner loss budget es account-day scoped; prior loss reduce remaining budget y prior profit no lo amplía por sobre L.
- GMM-I5 — remaining_profit_objective_money usa account-day realized + current Operation unrealized; no unrealized de otras Operations.
- GMM-I6 — target_mark es derivado/dinámico; no state authority.
- GMM-I7 — technical_stop nunca se aleja; protective stop es monotónico hacia más protección.
- GMM-I8 — Fill truth domina projected quantity.
- GMM-I9 — adverse/favorable branches son mutuamente excluyentes.
- GMM-I10 — partial Fill consume ordinal; no top-up.
- GMM-I11 — toda new-risk quantity es exacta; provider grant/deny, nunca silent resize.
- GMM-I12 — no max_admissible_qty/probing/hard-cap override.
- GMM-I13 — no new risk con economic plan unresolved, stale economic state o current_loss_budget_money<=0.
- GMM-I14 — profit objective reached gana a scaling.
- GMM-I15 — termination intent corta new risk.
- GMM-I16 — protective stop y monetary profit exit no double-spend reducible exposure.
- GMM-I17 — same ordered inputs + same config + same decision-scoped MarketContext => same decisions.
- GMM-I18 — Position no sustituye Operation/Fills.
- GMM-I19 — TERMINAL siempre NO_ACTION.
- GMM-I20 — funded numeric values no se inventan.

## 23. LIVE / BACKTEST / EXACT_REPLAY

La lógica GerardMM es pura respecto de runtime adapters. LIVE usa echo/operation, Account state, shared MarketContext y provider protocols reales.

BACKTEST suministra Account state/day stage determinista, config económico explícito, mismo Strategy Signal, mismo GerardMM y SimExecution. No existe gerard_live vs gerard_backtest.

EXACT_REPLAY mantiene D4-A1: BBO/market reads decision-critical se capturan en ContextReads. Account/config transitions que cambian decisiones deben formar parte del input ordenado/manifest según boundary vigente. No se reproduce side effect físico del venue.

## 24. S1 / S2 integration

S1 y S2 entregan el mismo seam:

~~~text
Signal OPEN {
  direction
  entry semantics
  technical_stop
  no profit target
}
~~~

S1 technical_stop proviene del low/high acumulado desde premarket start hasta previous closed 5m.

S2 technical_stop proviene del extremo de trigger bar + buffer ya congelado.

GerardMM no branch-ea por strategy_id. Dado Signal técnico + Account state + stage/day config + ProviderRuleSet + Fills + Market state, resuelve plan, current_loss_budget_money, remaining_profit_objective_money, exact quantity/action y dynamic target mark sin decisión humana runtime.

Strategy CLOSE/CLOSE_ALL mantiene precedencia técnica cuando llega; no redefine monetary objective.

## 25. SPEC deltas

### D2-08 Strategy Runtime

Signal.details para S1/S2 no entrega technical profit target. GerardMM necesita QUOTE; Strategy requirements siguen independientes.

### D2-04 Operation

mm_state cambia de r0-money/target snapshot a plan identity + P0/S0/D0/q0 + branch counters. No cambia lifecycle, Order, Fill ni ownership.

### D2-05 / D2-05C

Account DayBoundary define account_day_id. Provider hard monetary evaluators exponen conservative headroom read-only; provider_rules conserva final authority.

### D4-A1

Toda lectura BBO decision-critical sigue decision-scoped/captured.

### D4-A2 / D4-A3

Sin cambios: q_exec_max, local claims, reservation completeness, exact grant, no silent resize, final ReservationRevalidate, direction immutable y no double-close.

## 26. Acceptance cases

- AC-Q13-01: evaluation business day 1 resuelve SL=2000 USD y TP=1500 USD.
- AC-Q13-02: evaluation business day 2 resuelve SL=2000 USD y TP=1500 USD.
- AC-Q13-03: evaluation day sin row explícita falla cerrado para new risk.
- AC-Q13-04: FUNDED_INITIAL/FUNDED_STEADY schema resuelve sólo con valores configurados; hoy no inventa números.
- AC-Q13-05: D=400 y U=350 con T=1500 produce remaining objective=750.
- AC-Q13-06: D>=T antes de entry produce cero new risk.
- AC-Q13-07: current account-day loss reduce owner_remaining_loss_budget_money.
- AC-Q13-08: prior account-day profit no amplía Owner loss budget sobre L.
- AC-Q13-09: provider hard monetary headroom menor gobierna effective budget conservador sin reemplazar provider authority.
- AC-Q13-10: technical stop más protector que monetary stop nunca se afloja.
- AC-Q13-11: monetary stop más protector que Strategy stop se usa.
- AC-Q13-12: candidate add que requiere stop ya cruzado se rechaza localmente sin resize.
- AC-Q13-13: candidate add que empeora target distance se omite; no optimizer/probing.
- AC-Q13-14: provider DENIED/INVALID de exact add no prueba quantity menor.
- AC-Q13-15: partial Fill recalcula A/Q/remaining objective/target mark y consume ordinal.
- AC-Q13-16: favorable Fill protege al menos aggregate break-even.
- AC-Q13-17: remaining objective llega a cero y profit exit gana a threshold de add simultáneo.
- AC-Q13-18: Strategy CLOSE_ALL gana a scaling sin alterar monetary objective.
- AC-Q13-19: ForceClose con reducing Order outstanding no double-close.
- AC-Q13-20: stale/missing economic state bloquea new risk, no safety exit.
- AC-Q13-21: stale quote no genera add ni monetary profit trigger.
- AC-Q13-22: S1 y S2 usan el mismo GerardMM sin branch por Strategy.
- AC-Q13-23: same ordered inputs/config/context producen misma decision en replay/backtest boundary.
- AC-Q13-24: TERMINAL siempre NO_ACTION.
- AC-Q13-25: ninguna Signal Strategy requiere profit target para GerardMM.

## 27. KISS / YAGNI

Se mantienen una tabla económica pequeña, selector stage/day, dos branches bounded, un protective stop, monetary objective dinámico y exact provider gate.

No se crean campaign workflow engine, generic phase DSL, portfolio manager, optimization loop, dynamic AI sizing, provider-specific MM subclasses, unlimited schedules, aggregate diario nuevo, service nuevo, Strategy-side profit target, max_admissible_qty ni hard-cap override.

## 28. Owner decisions

Las decisiones Owner entregadas en D4-B3 quedan integradas y no se vuelven a pedir.

FUNDED tiene schema listo y valores numéricos pendientes de configuración futura. Eso no bloquea GerardMM; bloquea únicamente habilitar new risk en un funded account cuyo plan no tenga valores.

OWNER_DECISIONS_REQUIRED=NONE.

~~~text
Q13_GERARD_MM: OWNER_CORRECTED_CANDIDATE

MONETARY_LOSS_BUDGET:
COMPLETE

MONETARY_PROFIT_OBJECTIVE:
COMPLETE

EVALUATION_DAY_1:
SL_USD=2000
TP_USD=1500

EVALUATION_DAY_2:
SL_USD=2000
TP_USD=1500

FUNDED_CONFIG:
SCHEMA_READY

STRATEGY_OWNS_PROFIT_TARGET:
NO

PROVIDER_RULESET_INTEGRATION:
RESOLVED

MM_STATE:
MINIMAL

OWNER_DECISIONS_REQUIRED:
NONE

NEW_ARCHITECTURE_REQUIRED:
NO

READY_FOR_MANAGER_QA:
YES
~~~
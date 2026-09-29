# ECHO FUTURES — D4-B2 / Q13
# GERARD HARDSCALPING MONEYMANAGEMENT EXACT SPEC

## 1. Executive decision

Q13 queda resuelto a nivel candidate con un MoneyManagement V1 mecánico, determinista y pequeño, inspirado en la evidencia pública disponible sobre hardscalping pero sin atribuir a Gerard parámetros ni fórmulas que la evidencia no demuestra.

GerardMM V1 congela cinco decisiones estructurales: 1R es un presupuesto monetario inicial fijo por Operation; todo trigger de progreso usa como escala la distancia inicial entre entry reference y technical stop; negative recovery y positive pyramiding son ramas mutuamente excluyentes para una misma Operation; el stop ejecutable nunca puede alejarse respecto del riesgo ya protegido; y toda cantidad que MM decide debe atravesar sin resize silencioso los contratos D4-A2/D4-A3 antes de cualquier egress.

La política no intenta reproducir perfectamente una metodología privada. El objetivo es que, dados los mismos Signal, Account state, ProviderRuleSet, Contract, Operation/Fills/Orders y MarketContext, GerardMM produzca exactamente las mismas acciones.

No se cambia Strategy Runtime, no se cambia ownership, no se introduce arquitectura nueva y no se emite gate global de D4.

## 2. Evidence assessment

### 2.1 SOURCE-SUPPORTED

El research disponible respalda con confianza limitada/moderada las ideas generales de adverse adds/DCA, positive pyramiding, protección de ganancia mediante stop más favorable y gestión activa de exposición durante una operación.

También respalda que la gestión es una parte central del concepto de hardscalping y que las adiciones pueden modificar el precio medio de la posición.

### 2.2 NOT SOURCE-SUPPORTED

No existe evidencia pública suficiente para afirmar como hechos de Gerard: thresholds exactos en R, tamaños exactos de cada add, número exacto de adds, fórmula exacta de riesgo, fórmula exacta de stop, progresión de riesgo entre Operations, multiplicador después de pérdidas ni una semántica concreta de target.

Los ejemplos 3+3+3, 0.2R–0.5R, +0.5R y otros números presentes en el research son ilustrativos o rangos de experimentación, no autoridad factual.

### 2.3 ECHO DESIGN DECISION

Echo congela defaults concretos para obtener una V1 implementable y backtesteable. Esos defaults son decisiones de diseño de Echo GerardMM V1, no afirmaciones sobre Gerard.

### 2.4 UNKNOWN / DEFERRED

La progresión variable de riesgo entre Operations permanece DEFERRED_YAGNI. Cada nueva Operation calcula su propio R desde el Account state corriente con la misma configuración GerardMM; no existe loss-streak state, martingale entre Operations ni multiplicador de recuperación V1.

## 3. GerardMM V1 en lenguaje simple

GerardMM recibe una intención técnica de Strategy con dirección, entry semantics, technical stop y technical target opcional.

Primero calcula cuánto dinero puede planificar como riesgo inicial y cuántos contratos completos caben entre la entrada de referencia y el technical stop. Si no cabe al menos la cantidad mínima del Contract, no opera.

Una vez existe exposición real por Fill, mantiene un único stop protector ejecutable para la exposición actual. Ese stop puede quedarse donde estaba o apretarse; nunca se aleja para aceptar más pérdida.

Si el precio avanza en contra, puede hacer hasta dos adverse adds de tamaño igual a la entrada inicial. Después de cada Fill recalcula el precio medio y aprieta el stop para que el riesgo monetario planificado al stop no supere 1R.

Si el precio avanza a favor antes de haber entrado en recovery adverso, puede hacer un único favorable pyramid por 50% del tamaño inicial. Cuando ese pyramid obtiene Fill, el stop se protege al menos en break-even del conjunto de exposición.

La primera rama de add elegida queda latched para toda la Operation: si hubo adverse recovery, nunca se activa positive pyramiding; si hubo positive pyramiding, nunca se activa adverse recovery después de una reversión.

El technical target de Strategy, cuando existe, queda congelado como target máximo normal de la Operation. MM puede salir antes por stop, protección, CLOSE/CLOSE_ALL o safety, pero no extiende el target más allá del nivel técnico.

## 4. Ownership / boundaries

Strategy sigue siendo autoridad de intención técnica. Entrega direction, entry semantics, technical_stop, technical_target opcional y contexto técnico; no calcula quantity, dollar risk ni progresión hardscalping.

GerardMM vive como plugin dentro de echo/operation y posee exclusivamente sus decisiones de sizing, riesgo monetario, adds, protección, target execution y mm_state.

Operation sigue siendo autoridad de lifecycle, Orders, Fills, logical exposure, direction immutable y serialización de eventos.

ProviderRuleSet efectivo completo llega read-only al contexto de MM. MM puede usarlo para eligibility, límites locales deterministas y presupuesto de seguridad, pero no se transforma en provider authority.

echo/provider_rules(account_id) conserva toda autoridad account-wide: reservations, shared caps, trust state y revalidación final exacta. MM jamás replica las fórmulas GROSS/NET_ABS/GROUP_WEIGHTED ni infiere un max admissible quantity.

Position sigue siendo observación física y nunca reemplaza la exposición lógica de la Operation.

## 5. Input contract

Una decisión GerardMM recibe exactamente las authorities necesarias:

~~~text
GerardMMInput {
  effective_mm_config
  signal_technical_context
  account_state
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

Requisitos mínimos del Contract:

~~~text
tick_size > 0
tick_value > 0
qty_min > 0
qty_step > 0
qty_max?              # ausencia = sin máximo Contract adicional
quote_currency
~~~

Requisitos mínimos del Account state para new risk:

~~~text
account_currency
equity > 0
typed provider-risk inputs necesarios para evaluar los hard monetary loss budgets aplicables
~~~

Si quote_currency != account_currency, GerardMM requiere una conversión FX determinista disponible en el contexto de sizing. La tasa usada queda pinneada en mm_state como fx_rate_initial. Si esa conversión no existe, new risk falla cerrado con MM_FX_RATE_UNRESOLVED. Las salidas existentes no se bloquean por esta limitación.

Para MARKET entry, entry_reference es el BBO ejecutable-side observado en el decision-scoped MarketContext: ask para LONG y bid para SHORT. Para LIMIT/STOP entry, entry_reference es el precio exacto definido por la Signal. Si un tipo de entry no MARKET carece de precio exacto, MM_NO_ACTION.

GerardMM V1 requiere technical_stop. Si falta, está fuera del tick grid después de normalización, queda del lado favorable de entry_reference o deja distancia menor a un tick, no existe fallback técnico: MM_NO_ACTION.

technical_target es opcional. Si existe, debe estar al menos un tick en el lado favorable de entry_reference. Si ya fue alcanzado o quedó detrás de entry_reference antes de materializar la entry, MM_NO_ACTION. Si no existe, GerardMM no inventa un target; la salida puede venir de stop, protección, Strategy CLOSE/CLOSE_ALL o safety.

## 6. ProviderRuleSet interaction

GerardMM consume el ProviderRuleSet completo pero separa cuatro usos.

Eligibility: si un rule/account input necesario para new risk está UNKNOWN, unresolved o ya determina que la cuenta no puede abrir riesgo, GerardMM no produce una nueva Order expansiva. Stage-1 debería impedir la materialización en la mayoría de estos casos; este chequeo no reemplaza esa authority.

Sizing ceiling: para la Order inicial se aplican únicamente límites deterministas que MM puede calcular sin estado compartido, como max contracts/order y qty_max del Contract. Shared exposure caps no se convierten en un quantity menor dentro de MM.

Safety budget: para cada familia monetaria dura aplicable, el evaluator tipado del RuleSet calcula RemainingLossBudget(rule, account_state) en account currency. Sea H el mínimo de esos valores. Si no existe ninguna familia monetaria dura aplicable, H = +infinity. Si alguna familia aplicable necesita datos faltantes y no puede producir un remaining budget determinista, H = 0 para new risk.

Adds: cada adverse add o positive pyramid se decide por su cantidad completa configurada. Si la cantidad completa viola un límite local determinista, el step no se redimensiona y queda agotado. Si el gate account-wide la DENIED o la revalidación final la INVALID, no hay silent resize ni probing con cantidades menores.

Toda Order que pueda afectar shared caps atraviesa D4-A2. Todo grant todavía no emitido atraviesa ReservationRevalidate de D4-A3. VALID autoriza exactamente el grant original; INVALID no produce side effect.

Una DENIED/INVALID de ENTRY termina el intento inicial sin retry V1. Una DENIED/INVALID de ADD activa new_risk_locked para el resto de la Operation; la exposición existente continúa administrándose. Una DENIED/INVALID de una salida conserva el termination intent, no redimensiona y no hace polling ciego; queda pendiente hasta un trigger autoritativo posterior que permita reevaluar. El edge donde ninguna cantidad mínima de unwind puede satisfacer otra hard cap permanece el DEFERRED_YAGNI ya congelado por D4-A2.

## 7. Unit of risk

1R es el presupuesto monetario inicial planificado de la Operation, expresado en account currency.

Se fija una sola vez al crear mm_state y no cambia después de adds, pyramids, partial fills ni movimientos de stop.

Default Echo:

~~~text
initial_risk_fraction = 0.005    # 0.5% de equity; ECHO DESIGN DECISION
R_equity = account_equity * initial_risk_fraction
R_provider = H
R0 = min(R_equity, R_provider)
~~~

Si R0 <= 0, MM_NO_ACTION.

R0 es planned price risk al stop. No es promesa de pérdida máxima física: gaps, slippage, comisiones, venue behavior o fills posteriores a finality pueden producir otro resultado. Provider safety sigue siendo autoridad externa.

La unidad de progreso de precio también queda fija al inicio:

~~~text
P0 = entry_reference
S0 = technical_stop
D0 = abs(P0 - S0)
D0_ticks = D0 / tick_size
~~~

D0_ticks debe ser un entero positivo después de normalización al tick grid.

Para cualquier current exit-side mark M:

~~~text
direction_sign = +1 LONG, -1 SHORT
progress_R = direction_sign * (M - P0) / D0
~~~

M usa bid para LONG y ask para SHORT, porque representa el lado al que la exposición podría salir.

Ejemplos: progress_R = -0.25 significa un cuarto de la distancia inicial al stop en contra desde P0; progress_R = +0.50 significa media distancia inicial a favor. Los adds nunca re-anclan P0 ni D0, evitando thresholds móviles después de cambiar el average entry.

## 8. Initial sizing formula

La conversión económica se hace sin hardcodear NQ.

~~~text
fx0 = 1                                    si quote_currency == account_currency
fx0 = deterministic FX quote pinned       en caso contrario

risk_per_contract =
  D0_ticks
  * tick_value
  * fx0

q_risk_raw =
  floor(R0 / risk_per_contract)
~~~

La función NormalizeQtyDown(x) usa el lattice del Contract:

~~~text
si x < qty_min:
  0
si x >= qty_min:
  qty_min + floor((x - qty_min) / qty_step) * qty_step
~~~

El ceiling estático inicial es:

~~~text
q_ceiling =
  min(
    q_risk_raw,
    contract.qty_max si existe,
    provider max_contracts_per_order si aplica
  )

q0 = NormalizeQtyDown(q_ceiling)
~~~

Si q0 = 0, la Operation no emite entry Order y registra terminación MM_NO_ACTION.

No se usa un max_admissible_qty account-wide. Si q0 exacto no obtiene grant Stage-2, no se prueba q0-1, q0-2, etc.; la entry queda REJECTED{PROVIDER_GATE} y la Operation converge a ENTRY_REJECTED.

Para MARKET la Order inicial usa quantity q0 y tipo MARKET. Para una Strategy que entregue LIMIT/STOP exacto, GerardMM conserva ese tipo y precio; sizing sigue usando el entry_reference exacto de esa Order.

## 9. Technical SL / TP precedence

### 9.1 Technical stop

technical_stop es obligatorio y define la frontera técnica inicial. GerardMM lo usa como S0 y nunca puede alejar el stop ejecutable más allá de S0.

Después de Fills, MM puede apretarlo para limitar el riesgo monetario o proteger ganancia. Nunca puede moverlo en dirección de mayor pérdida.

Para exposición actual Q > 0 y average open price A, con point_value_account = tick_value / tick_size * fx0:

~~~text
risk_cap_distance = R0 / (Q * point_value_account)

LONG:
  risk_cap_stop_raw = A - risk_cap_distance
  risk_cap_stop = round_up_to_tick(risk_cap_stop_raw)

SHORT:
  risk_cap_stop_raw = A + risk_cap_distance
  risk_cap_stop = round_down_to_tick(risk_cap_stop_raw)
~~~

El rounding siempre aprieta protección y nunca aumenta el riesgo planificado.

Sea S_prev el stop protector efectivo más favorable ya comprometido. El stop deseado base es:

~~~text
LONG:  max(S0, S_prev, risk_cap_stop)
SHORT: min(S0, S_prev, risk_cap_stop)
~~~

Tras un favorable pyramid con Fill, se agrega break-even aggregate:

~~~text
LONG:  desired_stop = max(base_stop, round_up_to_tick(A))
SHORT: desired_stop = min(base_stop, round_down_to_tick(A))
~~~

Si el current exit-side mark ya cruzó desired_stop antes de poder instalarlo, MM no publica un stop inválido detrás del mercado: registra termination intent de protección y entra al full-exit path.

### 9.2 Technical target

technical_target, si existe, queda pinneado al valor entregado por Strategy. GerardMM no lo extiende, no lo sustituye por un multiple de R y no lo mueve después de adds.

El target es un full-exit threshold lógico, no una segunda resting Order simultánea con el protective stop. Esto evita que stop y target double-spend la misma reducible exposure bajo D4-A2.

Cuando el exit-side BBO alcanza o cruza technical_target, target exit tiene precedencia sobre cualquier nuevo add: MM registra termination intent, cancela el protective stop, conserva su q_exec_max hasta finality y sólo después intenta una MARKET EXIT por la exposición todavía no reclamada.

Si Strategy no entrega target, no existe target inventado.

## 10. Negative hardscalping exact rules

Defaults Echo:

~~~text
adverse_step_R = 0.25
max_adverse_adds = 2
adverse_add_ratio = 1.00
~~~

El next adverse threshold para ordinal i, comenzando en 1, es:

~~~text
threshold_i = -adverse_step_R * i
~~~

El add se considera elegible sólo si todas estas condiciones son verdaderas:

~~~text
Operation ACTIVE con exposure > 0
sin termination intent
new_risk_locked == false
branch == NEUTRAL o ADVERSE
adverse_attempts < max_adverse_adds
no pending new-risk add
current quote READY y no stale
progress_R <= threshold_(adverse_attempts + 1)
technical target no alcanzado
~~~

La quantity deseada del step es:

~~~text
q_add = NormalizeQtyDown(q0 * adverse_add_ratio)
~~~

Si q_add = 0 o la cantidad completa no satisface max contracts/order/qty_max local, el step se marca agotado sin Order y no se redimensiona.

Al construir el primer adverse ADD, branch pasa de NEUTRAL a ADVERSE antes del request de provider. Desde ese momento positive pyramiding queda deshabilitado para toda la Operation.

Cada adverse ADD es MARKET. adverse_attempts incrementa cuando se construye la Order exacta, no por cantidad filled. Un partial fill consume igualmente ese ordinal; no existe top-up para completar el ratio configurado.

Mientras una ADD Order tenga q_exec_max > 0 o finality pendiente, no se construye otro add.

Cada Fill de ADD actualiza exposición y average open price usando Fill truth; inmediatamente se recalcula el desired protective stop con la fórmula de §9.1. Esto conserva planned stop risk <= 1R siempre que el nuevo stop pueda ejecutarse normalmente; no se falsifica garantía ante gaps o races físicas.

Si el add exacto es DENIED/INVALID por provider, new_risk_locked = true, no existe retry con menos quantity y no se intentan adverse adds posteriores.

Si una ADD termina con cero Fill por rechazo/fallo terminal de venue, new_risk_locked = true. Si termina parcialmente filled, el step queda consumido y un step posterior puede ser evaluado después de finality, usando la exposición real.

Maximum negative desired exposure por configuración, ignorando provider denial, es:

~~~text
q0 + max_adverse_adds * NormalizeQtyDown(q0 * adverse_add_ratio)
~~~

Esto es un desired envelope de MM, no una autorización provider.

## 11. Positive hardscalping exact rules

Defaults Echo:

~~~text
positive_step_R = 0.50
max_positive_adds = 1
positive_add_ratio = 0.50
~~~

El next favorable threshold para ordinal i es:

~~~text
threshold_i = +positive_step_R * i
~~~

El pyramid se considera elegible sólo si:

~~~text
Operation ACTIVE con exposure > 0
sin termination intent
new_risk_locked == false
branch == NEUTRAL o FAVORABLE
positive_attempts < max_positive_adds
no pending new-risk add
current quote READY y no stale
progress_R >= threshold_(positive_attempts + 1)
technical target ausente o todavía no alcanzado
~~~

Quantity:

~~~text
q_pyramid = NormalizeQtyDown(q0 * positive_add_ratio)
~~~

Si q_pyramid = 0 o no cabe completa en los límites locales deterministas, el step se agota sin Order y no se redimensiona.

Al construir el primer favorable ADD, branch pasa de NEUTRAL a FAVORABLE. Desde entonces negative recovery queda deshabilitado para toda la Operation, incluso si el precio revierte después.

Cada favorable ADD es MARKET. positive_attempts incrementa al construir la Order. Partial fill consume el ordinal y no genera top-up.

Tras el primer Fill favorable, el desired protective stop debe quedar al menos en break-even del average open price agregado según §9.1. Si ese nivel ya quedó cruzado por el mercado, MM inicia full exit por PROTECTION_CROSSED.

Si provider DENIED/INVALID el pyramid, new_risk_locked = true y no existe retry ni step posterior.

## 12. Interaction negative ↔ positive

GerardMM V1 usa una sola variable branch:

~~~text
NEUTRAL
ADVERSE
FAVORABLE
~~~

Transiciones permitidas:

~~~text
NEUTRAL -> ADVERSE     al construir el primer adverse ADD
NEUTRAL -> FAVORABLE   al construir el primer favorable ADD
ADVERSE -> ADVERSE
FAVORABLE -> FAVORABLE
~~~

No existen ADVERSE -> FAVORABLE ni FAVORABLE -> ADVERSE.

Caso entry → adverse add → recovery → favorable zone: branch ya es ADVERSE. El trade conserva technical target y protective stop, pero no piramidea ganancia. Si alcanza target, sale; si revierte, aplica el siguiente adverse step permitido o el stop.

Caso entry → favorable pyramid → reversal: branch ya es FAVORABLE. No se hace DCA negativo. El stop protegido en break-even/risk-cap gobierna la salida.

Esta latched branch es una decisión estructural V1. Evita que una Operation acumule primero tamaño en pérdida y luego vuelva a expandirse en recuperación, o que una ganadora protegida se transforme después en averaging-down.

## 13. Minimal mm_state

GerardMM persiste sólo lo que no puede reconstruirse de Operation/Orders/Fills/Provider authority:

~~~text
GerardMMState {
  r0_money
  p0_entry_reference
  s0_technical_stop
  d0_price_distance
  fx_rate_initial
  q0_initial

  technical_target?

  branch
  adverse_attempts
  positive_attempts
  new_risk_locked

  pending_add_order_id?
  protective_stop_order_id?
}
~~~

No se persisten average entry, current exposure, filled quantity, provider reservations, RuleSet state, Position ni current market price: todos tienen otra authority.

No se persiste S_prev separadamente si existe protective_stop_order_id; su stop_price autoritativo se obtiene de la Order. Si el stop está en transición cancel/replace, el desired stop se recalcula determinísticamente desde R0, Fills, branch y average open price al procesar el siguiente action result.

No existe state cross-Operation.

## 14. Trigger requirements

GerardMM V1 declara:

~~~text
market_event = QUOTE
bar_close = NONE
timers = NONE
~~~

No necesita H4, 5m, indicadores ni barras. Strategy ya resolvió el setup técnico.

MM corre ante:

- SignalDelivery inicial y Signals REDUCE/CLOSE/CLOSE_ALL posteriores.
- Fill.
- OrderStatus / OrderActionResult / finality.
- Provider gate result asociado a sus Orders.
- termination / ForceClose intent.
- QUOTE notification para adverse/favorable/target thresholds.

Toda decisión market-dependent usa D4-A1 MarketContext decision-scoped. LIVE captura exactamente el BBO/version observado; EXACT_REPLAY consume context_reads[]; BACKTEST usa el estado sintético determinista.

No se usa last-known/stale quote para ENTRY, ADD, PYRAMID ni target triggering. Un outage no inventa una salida monetaria; el protective STOP ya emitido permanece en el venue y safety/provider conservan sus propios mecanismos.

## 15. Order / action behavior

Prioridad determinista después de aplicar el fact que disparó la invocación:

1. Safety/provider termination intent ya registrado.
2. Strategy CLOSE/CLOSE_ALL o MM protection/technical-target termination.
3. Exposure invariant breach / provider physical-state restrictions: cero new risk; sólo acciones permitidas por los contratos existentes.
4. Reconciliar protective stop contra la exposición real y el desired stop.
5. Evaluar adverse/favorable new-risk step si todavía está permitido.
6. No action.

Una vez existe termination intent, GerardMM no produce ENTRY/ADD/PYRAMID nuevos.

ENTRY y todos los hardscalping adds son MARKET en V1 salvo que la Signal inicial defina explícitamente un entry type exacto distinto.

Protective stop: después del primer Fill, GerardMM mantiene como objetivo exactamente una protective STOP Order lógica para toda la exposición no reclamada por otro exit. Si la Order necesita aumentar qty o apretar price, se prefiere modify nativo cuando la capability declarada lo soporta. Modify-increase sigue D4-A2 y adquiere el claim/reservation delta antes de egress.

Si la capability no soporta el modify requerido, se usa cancel + finality + nueva STOP Order. La Order vieja conserva q_exec_max y protección hasta finality; la nueva no se construye como executable mientras duplicaría el claim de reducción.

Technical target y normal CLOSE no usan una resting target Order paralela al stop. Cancelan primero el protective stop, esperan finality y luego solicitan MARKET EXIT por la exposición no reclamada. Fill-vs-cancel se resuelve por Fill truth; nunca se sobre-cierra.

GerardMM V1 no hace partial profit-taking por iniciativa propia.

## 16. Partial fills / cancel / deny behavior

### 16.1 Initial entry partial fill

El primer Fill transforma la Operation en ACTIVE y crea protección sólo por la exposición realmente filled. La entry restante no se cuenta como reducible exposure.

Cada Fill adicional aumenta la exposición firme y dispara reconciliación del protective stop qty. El stop nunca se expande anticipando un Fill todavía no ocurrido.

Si la entry finaliza con algún Fill, la Operation continúa con la quantity real. Si finaliza con cero Fill, GerardMM desiste y termina como ENTRY_FAILED/ENTRY_REJECTED según causa.

### 16.2 ADD partial fill

El ordinal fue consumido al construir la ADD Order. Cada Fill real recalcula stop y average. No se emite otro add mientras la Order anterior tenga q_exec_max/finality pendiente. Finality con partial fill no genera top-up.

### 16.3 Cancel / replace

Cancel request o cancel ACK no liberan reducible claim ni provider reservation por sí mismos. GerardMM espera la finality autoritativa congelada por D4-A2.

Replace de protective stop sólo ocurre si no existe modify nativo capaz de representar la nueva protección. Old y new no double-spend exposure: la nueva cantidad executable espera la liberación autoritativa necesaria.

### 16.4 Provider deny / invalid

ENTRY exacta denied: no retry con cantidad menor; termination ENTRY_REJECTED.

ADD exacta denied: no side effect, release del claim cuando corresponda, new_risk_locked = true, Operation sigue viva.

EXIT exacta denied por shared-cap semantics: termination permanece pending, no silent resize y no polling por cada QUOTE. Se reevalúa sólo frente a un trigger autoritativo posterior que cambie el estado relevante.

### 16.5 Late fills

Todo late Fill es hecho. Si llega mientras la Operation sigue viva, actualiza exposición y se vuelve a proteger/terminar según state actual. Si contradice finality post-terminal, rige el breach ya congelado; GerardMM no inventa reparación.

## 17. ForceClose / termination precedence

Todo termination intent corta new risk inmediatamente.

Precedencia semántica de reason:

~~~text
SAFETY_PLANE / provider ForceClose / session-risk forced termination
  >
MM normal termination / technical CLOSE / CLOSE_ALL / technical target / protection
~~~

Si una terminación normal ya estaba activa y luego llega ForceClose, el requested_by/reason efectivo se eleva a SAFETY_PLANE. Si ForceClose llegó primero, un CLOSE técnico posterior no lo degrada.

ForceClose no emite un cierre full-size ignorando Orders existentes. Sigue D4-A2: solicita cancel de Orders incompatibles, conserva q_exec_max hasta finality, calcula sólo exposición reducible no reclamada y construye close Orders exactas cuando puede hacerlo sin cruzar dirección ni violar la authority account-wide.

Si ForceClose llega mientras existe una ADD MARKET aún no final: no se construyen más adds; se intenta cancelar si físicamente posible; cualquier Fill tardío se incorpora; el close final usa la exposición real posterior. El termination intent nunca se pierde.

GerardMM deja de producir nuevas acciones de riesgo cuando ocurre cualquiera de estos estados: termination intent, new_risk_locked para el branch de scaling, Operation TERMINAL, exposure invariant breach que bloquee new risk, o provider state que bloquee new risk.

En TERMINAL, GerardMM produce siempre NO_ACTION.

## 18. Parameters + deterministic defaults

### 18.1 Structural semantics

Cambiar cualquiera de estos puntos constituye otra política MM o una V2 semántica: R fijo por Operation; technical stop obligatorio; stop nunca se afloja; progress anclado a P0/D0; ramas adverse/favorable mutuamente excluyentes; technical target nunca se extiende; no simultaneous resting stop+target que double-spend exposure; adds MARKET; provider exact-grant/no resize; no inter-trade martingale.

### 18.2 Tunable parameters

| Parameter | Default Echo V1 | Semántica |
| --- | ---: | --- |
| initial_risk_fraction | 0.005 | fracción de equity para R_equity |
| adverse_step_R | 0.25 | separación fija de adverse thresholds |
| max_adverse_adds | 2 | máximo de adverse steps |
| adverse_add_ratio | 1.00 | add quantity respecto de q0 |
| positive_step_R | 0.50 | separación fija de favorable thresholds |
| max_positive_adds | 1 | máximo de pyramids |
| positive_add_ratio | 0.50 | pyramid quantity respecto de q0 |

No se agregan ATR multipliers, volatility adaptation, ML, dynamic optimization, loss-streak multiplier, session-dependent scaling ni target-R fallback.

## 19. Numerical walkthroughs

Todos los números de esta sección son ejemplos de la SPEC, no evidencia de rentabilidad ni parámetros reales de Gerard.

Supuesto común: LONG, tick_size 0.25, tick_value USD 5, por lo tanto point_value USD 20 por punto; account currency USD; equity USD 100,000; initial_risk_fraction 0.5%; provider remaining hard monetary budget H = USD 400; qty_min 1; qty_step 1; sin cap local menor.

### 19.1 Initial sizing

~~~text
R_equity = 100000 * 0.005 = 500
R0 = min(500, 400) = 400

P0 = 20000.00
S0 = 19995.00
D0 = 5.00 points = 20 ticks

risk_per_contract = 20 ticks * USD 5 = USD 100
q0 = floor(400 / 100) = 4 contracts
~~~

GerardMM decide MARKET BUY 4. Stage-2 debe conceder exactamente 4 o denegar.

### 19.2 First adverse add

Threshold 1 = -0.25R-price = 20000 - 1.25 = 19998.75.

Con Fill de ADD 4 @ 19998.75:

~~~text
Q = 8
A = (4*20000 + 4*19998.75) / 8 = 19999.375
risk_cap_distance = 400 / (8*20) = 2.5 points
risk_cap_stop_raw = 19996.875
round_up_to_tick = 19997.00
planned stop price-risk = 8 * (19999.375 - 19997.00) * 20 = USD 380
~~~

El technical stop original 19995.00 no se aleja; el nuevo stop se aprieta a 19997.00.

### 19.3 Second adverse add / maximum

Threshold 2 = -0.50R-price = 19997.50.

Con Fill de otros 4 @ 19997.50:

~~~text
Q = 12
A = 19998.75
risk_cap_distance = 400 / (12*20) = 1.666666...
risk_cap_stop_raw = 19997.0833...
round_up_to_tick = 19997.25
planned stop price-risk = 12 * 1.50 * 20 = USD 360
~~~

adverse_attempts = 2 = max_adverse_adds. Aunque el precio siga cayendo, no existe tercer add.

### 19.4 Favorable pyramid

Nueva Operation limpia con q0 = 4, P0 = 20000, D0 = 5. Threshold favorable = +0.50R-price = 20002.50. positive_add_ratio = 0.5 ⇒ q_pyramid = 2.

Con Fill 2 @ 20002.50:

~~~text
Q = 6
A = (4*20000 + 2*20002.50) / 6 = 20000.8333...
break_even_tick = round_up_to_tick(A) = 20001.00
risk_cap_stop = 19997.50
desired_stop = max(19995.00, 19997.50, 20001.00) = 20001.00
~~~

El branch queda FAVORABLE; no habrá DCA negativo posterior.

### 19.5 Favorable → reversal

Con el stop protegido en 20001.00, una reversión ejecuta la protección. El gross price P&L ilustrativo antes de costes sería:

~~~text
4 * (20001 - 20000) * 20 = +80
2 * (20001 - 20002.50) * 20 = -60
total = +20
~~~

Aunque luego el precio caiga a -0.25R desde P0, branch FAVORABLE prohíbe adverse adds.

### 19.6 Initial partial fill

Entry BUY 4 recibe primero Fill 2 @ 20000.00. La exposición real es 2 y el protective stop cubre sólo 2. El risk-cap calculado sería 19990.00, por lo que S0=19995.00 sigue siendo más protector.

Llega después Fill 1 @ 20000.25:

~~~text
Q = 3
A = 20000.0833...
risk_cap_stop_raw = 20000.0833 - 400/(3*20) = 19993.4166...
desired_stop = max(19995.00, 19993.50) = 19995.00
~~~

El protective stop pasa a quantity 3 sólo mediante el protocolo seguro de modify-increase/reservation. El cuarto contrato no se protege antes de existir como Fill.

### 19.7 Provider deny de adverse add

progress_R llega a -0.25. GerardMM construye MARKET ADD 4 exacta. provider_rules DENIED el grant por un shared cap. Resultado: ninguna Order escapa, el local claim converge, new_risk_locked = true, no se prueba quantity 3 ni 2 y no se intenta el segundo adverse step. La Operation mantiene sus 4 contratos iniciales y su protección normal.

### 19.8 Strategy technical target

Signal S2 trae technical_target = 20004.00. Cuando bid >= 20004.00, el target gana antes de evaluar pyramiding/add. GerardMM registra termination intent, cancela el protective STOP, espera su finality y solicita MARKET EXIT por la exposición no reclamada. El target permanece 20004.00 aunque existieran adverse adds y el average entry hubiera bajado.

### 19.9 ForceClose durante hardscalping

Operation LONG tiene exposición 8, protective STOP SELL 8 y un adverse ADD BUY 4 pendiente. Llega ProviderForceClose.

GerardMM bloquea new risk, solicita cancel del ADD y del stop según el safety flow, pero mantiene ambos q_exec_max hasta finality. No emite SELL 8 inmediatamente porque el STOP ya reclama esa exposición y el ADD todavía podría fill-ear. Si el ADD obtiene Fill 2 antes de finality, exposición pasa a 10. Cuando ADD y stop quedan finalizados, ForceClose intenta cerrar exactamente los 10 contratos no reclamados, sujeto al exact-grant protocol. No existe double close ni exposición anticipada.

## 20. Invariants

- GMM-I1 — Operation direction nunca cambia; GerardMM no crea hedge/reversal dentro de la misma Operation.
- GMM-I2 — 1R se fija una vez y nunca aumenta por adds.
- GMM-I3 — technical_stop inicial es frontera máxima de pérdida planificada; todo movimiento posterior del stop es igual o más protector.
- GMM-I4 — una Fill es un hecho y siempre domina cualquier expectativa de quantity.
- GMM-I5 — adverse y favorable branches son mutuamente excluyentes.
- GMM-I6 — no existe más de una new-risk ADD pendiente a la vez por Operation.
- GMM-I7 — partial fill consume el ordinal de add; no existe top-up.
- GMM-I8 — no se produce nuevo riesgo después de termination intent.
- GMM-I9 — toda reducing Order respeta los local claims/q_exec_max de D4-A2; no double-spend de reducible exposure.
- GMM-I10 — MM nunca emite una quantity mayor a la que decidió; provider sólo puede autorizar exactamente esa quantity o denegar.
- GMM-I11 — ningún provider DENIED/INVALID provoca silent resize.
- GMM-I12 — ProviderRuleSet local/read-only nunca sustituye la final authority de echo/provider_rules(account_id).
- GMM-I13 — technical_target nunca se mueve a un precio más lejano para extender la operación.
- GMM-I14 — same ordered inputs + same config + same decision-scoped MarketContext ⇒ same mm_state y mismas acciones.
- GMM-I15 — Position no sustituye Operation/Fills como verdad lógica.
- GMM-I16 — no new-risk action usa stale/last-known market price.
- GMM-I17 — protective stop y target exit nunca quedan simultáneamente ejecutables por full quantity de manera que puedan cruzar cero.
- GMM-I18 — TERMINAL siempre produce NO_ACTION.
- GMM-I19 — inter-trade risk progression no existe en V1.

## 21. LIVE / BACKTEST / EXACT_REPLAY compatibility

La lógica GerardMM es una función pura sobre input, mm_state y MarketContext; no conoce Kafka, StateFun, PG, transport SDK ni wall clock.

LIVE usa echo/operation como state owner, MarketContext compartido y los protocolos D4-A2/A3 reales.

BACKTEST usa la misma config, el mismo state machine, las mismas fórmulas de sizing/progress/stop y SimExecution. El runner sintetiza BBO/Order/Fills determinísticamente; no existe gerard_live vs gerard_backtest.

EXACT_REPLAY conserva el boundary D4-A1: si una decisión GerardMM depende de BBO u otro pull de mercado, LIVE captura la lectura en context_reads[] y EXACT_REPLAY la reinyecta por la misma logical key/version. No se amplía replay hacia side effects físicos ni se pretende reproducir venue execution.

R0, P0, D0, q0, branch y counters forman parte del mm_state recuperable con la Operation. Orders/Fills continúan siendo sus authorities propias.

## 22. SPEC deltas

### D2-04 Operation / Order / Fill

GerardMM concreta el contenido mínimo de mm_state definido por D2-04. No cambia lifecycle ni identity.

Se requiere distinguir en la decisión MM las acciones INITIAL_ENTRY, ADVERSE_ADD, FAVORABLE_ADD, PROTECTIVE_STOP y NORMAL_EXIT para trazabilidad; esto puede viajar como metadata de decision/action, no requiere nueva entidad.

### D2-05 / D2-05C Provider

Los límites PER_ORDER deterministas pueden alimentar initial sizing. Daily-loss/trailing RuleSet families pueden limitar R0 mediante RemainingLossBudget sobre el Account state disponible, pero provider authority permanece externa.

El wording histórico de D2-05C según el cual todas las EXIT bypassan shared capacity queda superseded por D4-A2: si una reducción/exit afecta shared caps, necesita la reservation exacta correspondiente.

### D2-08 Strategy Runtime

GerardMM declara QUOTE como único market input adicional. No necesita bars ni indicators. technical_stop/technical_target continúan llegando desde Signal.details.

### D4-A1

Toda lectura BBO decision-critical usa decision-scoped MarketContext y context_reads[] para EXACT_REPLAY.

### D4-A2

Todas las Orders, incluidas protective stop, target exit y ForceClose close-orders, respetan q_exec_max, local reducing claims, reservation completeness y no silent resize.

### D4-A3

Cada exact grant no emitido atraviesa ReservationRevalidate. GerardMM no interpreta epochs ni calcula max_admissible_qty.

### D4-B1 / S2

Q13 cierra su ambigüedad: S2 technical_stop es obligatorio como S0; S2 technical_target es target normal inmutable y no se extiende. GerardMM puede apretar stop y salir antes, pero no lo afloja ni reemplaza target por otra extensión.

## 23. Acceptance cases

- AC-Q13-01: misma Signal/Account/RuleSet/Contract/BBO produce exactamente el mismo R0, q0 y entry Order.
- AC-Q13-02: technical_stop ausente produce MM_NO_ACTION y cero Order.
- AC-Q13-03: q0 menor que qty_min produce MM_NO_ACTION.
- AC-Q13-04: MARKET LONG usa ask como P0; MARKET SHORT usa bid.
- AC-Q13-05: cross-currency sin FX determinista produce MM_FX_RATE_UNRESOLVED para new risk.
- AC-Q13-06: first adverse threshold produce exactamente un ADD y latch ADVERSE.
- AC-Q13-07: adverse branch que recupera a favorable threshold no produce pyramid.
- AC-Q13-08: first favorable threshold produce exactamente un pyramid y latch FAVORABLE.
- AC-Q13-09: favorable branch que revierte a adverse threshold no produce recovery add.
- AC-Q13-10: second adverse add alcanza max y un tercer threshold produce NO_ACTION.
- AC-Q13-11: partial ADD Fill recalcula stop con quantity real y no top-up del ordinal.
- AC-Q13-12: provider DENIED de ADD activa new_risk_locked y no retry con menor qty.
- AC-Q13-13: provider INVALID final impide egress aunque el RuleSet snapshot local pareciera permitido.
- AC-Q13-14: target alcanzado y pyramid threshold simultáneo produce termination/target path, no pyramid.
- AC-Q13-15: technical target no cambia después de adverse add.
- AC-Q13-16: risk-cap stop posterior a add nunca queda menos protector que S0/S_prev.
- AC-Q13-17: positive pyramid Fill mueve protección al menos a aggregate break-even.
- AC-Q13-18: current mark ya cruzó newly required protective stop produce full-exit intent, no stop inválido detrás del mercado.
- AC-Q13-19: ForceClose con outstanding reducing Order no emite otra full close que double-spendee exposición.
- AC-Q13-20: termination intent seguido de QUOTE favorable/adverso nunca genera new risk.
- AC-Q13-21: stale quote no genera entry/add/pyramid/target trigger.
- AC-Q13-22: same LIVE context_reads[] reproducidas en EXACT_REPLAY producen la misma decisión market-dependent.
- AC-Q13-23: BACKTEST con mismos inputs sintéticos produce las mismas acciones lógicas que el motor MM.
- AC-Q13-24: Operation TERMINAL siempre retorna NO_ACTION.
- AC-Q13-25: nueva Operation posterior a una pérdida vuelve a calcular R desde config/account state sin multiplicador de loss streak.

## 24. KISS / YAGNI sweep

Se mantienen sólo: risk sizing fijo, dos branches de scaling, un stop protector, technical target opcional, counters mínimos y exact provider gate.

Se rechazan V1: martingale entre Operations, unlimited adds, unlimited pyramids, ATR/dynamic spacing, adaptive parameters, optimization engine, DSL, plugin-system interno adicional, portfolio coordinator, cross-account MM state, probabilistic sizing, ML, generic risk graph, provider-specific MM subclasses, global position manager, hedging opuesto dentro de la Operation, simultaneous OCO assumptions no certificadas, generic wind-down, HARD_CAP_WINS, max_admissible_qty y liquidation override.

No se agrega timer porque QUOTE + execution facts + termination intents alcanzan para las reglas V1.

## 25. Evidence vs Echo design decisions

| Tema | Fuente / estado | GerardMM V1 |
| --- | --- | --- |
| adverse adds / DCA | SOURCE-SUPPORTED limitado/moderado | IN_V1 |
| positive pyramiding | SOURCE-SUPPORTED limitado/moderado | IN_V1 |
| proteger ganancias con stop | SOURCE-SUPPORTED limitado/moderado | IN_V1 |
| thresholds 0.25R / 0.50R | no demostrados | ECHO DESIGN DECISION |
| adverse add ratio 1.0 | no demostrado | ECHO DESIGN DECISION |
| positive ratio 0.5 | sólo ilustrativo en research | ECHO DESIGN DECISION |
| max adverse 2 / positive 1 | no demostrado | ECHO DESIGN DECISION |
| 0.5% equity initial risk | rango research no probatorio | ECHO DESIGN DECISION |
| R fijo intra-Operation | no demostrado como fórmula Gerard | ECHO DESIGN DECISION para bounded risk |
| branch mutual exclusion | no demostrado | ECHO DESIGN DECISION KISS/safety |
| stop risk-cap exact formula | no demostrada | ECHO DESIGN DECISION |
| technical target inmutable | Strategy contract, no evidencia Gerard | ECHO DESIGN DECISION de integración |
| inter-trade risk increase | UNKNOWN | DEFERRED_YAGNI |
| disposable prop account philosophy | UNKNOWN | NO FORMA PARTE DE MM V1 |

## 26. Owner decisions

OWNER_DECISIONS_REQUIRED = NONE.

Los defaults numéricos de V1 son tunables de research y quedan explícitamente etiquetados como decisiones Echo. No cambian la arquitectura ni afirman evidencia que no existe.

Una decisión Owner sólo sería necesaria si el producto quisiera convertir en requirement una progresión de riesgo entre Operations, un bypass/override de hard provider caps, una promesa distinta de pérdida máxima o un scope de liquidación que contradiga los boundaries congelados. Ninguna de esas decisiones es necesaria para cerrar Q13 V1.

```text
Q13_GERARD_MM: CANDIDATE_RESOLVED

NEGATIVE_HARDSCALPING:
COMPLETE

POSITIVE_HARDSCALPING:
COMPLETE

TECHNICAL_SL_TP_PRECEDENCE:
RESOLVED

PROVIDER_RULESET_INTEGRATION:
RESOLVED

MM_STATE:
MINIMAL

OWNER_DECISIONS_REQUIRED:
NONE

DEFERRED_YAGNI:
INTER_TRADE_VARIABLE_RISK; GENERIC_WIND_DOWN/HARD_CAP_OVERRIDE; MAX_ADMISSIBLE_QTY; GENERIC_LIQUIDATION_OVERRIDE; OCO_SEMANTICS_NOT_CERTIFIED

NEW_ARCHITECTURE_REQUIRED:
NO

READY_FOR_MANAGER_QA:
YES
```
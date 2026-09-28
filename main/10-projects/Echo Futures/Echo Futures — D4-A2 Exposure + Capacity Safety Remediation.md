---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D3 Astra Architecture Review]]"
  - "[[Echo Futures Architecture Candidate V1]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
  - "[[Echo Futures — D2-05 Instrument Session Provider]]"
  - "[[Echo Futures — D2-07 Execution Runtime]]"
aliases:
  - Echo Futures D4-A2
  - EF D4-A2 Exposure Capacity Safety
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-remediation
created: "2026-09-28"
updated: "2026-09-28"
---

# Echo Futures — D4-A2 Exposure + Capacity Safety Remediation

## 1. Propósito y alcance

Este artifact es una corrección arquitectónica candidata y acotada para los findings aceptados D3-02 y D3-03. No reemplaza al Primary Manager, no modifica las authorities D2 congeladas y no emite ningún gate global de D4.

La corrección trata ambos findings como un único problema: distinguir exposición firme ya ejecutada de cantidad todavía físicamente ejecutable, y demostrar que ningún ordering permitido de esas cantidades puede (a) invertir una Operation mediante Orders de reducción correctamente emitidas por Echo ni (b) exceder el envelope account-wide de una policy provider.

El modelo conserva los boundaries congelados: echo/operation sigue siendo owner del lifecycle, Orders, Fills, MoneyManagement state y exposición lógica de cada Operation; echo/provider_rules(account_id) sigue siendo owner de caps y reservas compartidas por cuenta. Position física continúa siendo una observación separada del venue y jamás se transforma en verdad lógica de una Operation. Fill continúa siendo el hecho venue-authoritative del que deriva la exposición lógica firmada. ForceClose continúa siendo un intent de safety y no una transición mágica.

Fuera de alcance: D3-04, D3-06, market identity/replay, selección de transport, implementación StateFun/Kafka, D5/D6, Q12/Q13, reconciliation repair y cualquier mutación de Echo físico.

## 2. Baseline y evidencia utilizada

Autoridades primarias revisadas:

- [[Echo Futures]] — D1 y D2 cerrados, D3 aceptado, boundaries y restricciones de producto.
- [[Echo Futures — D3 Astra Architecture Review]] — evidencia y contraejemplos D3-02 y D3-03.
- [[Echo Futures Architecture Candidate V1]] — integración congelada D2.
- [[Echo Futures — D2-04 Operation Order Fill Position]] — ownership de Operation/Order/Fill, múltiples Orders vivas, guard de dirección, lifecycle, replace, partial fill, late fill y finality.
- [[Echo Futures — D2-05 Instrument Session Provider]] y su child [[Echo Futures — D2-05C Provider Program Rules]] — Stage-2, firm_by_operation, live_reservations, GROSS/NET_ABS/GROUP_WEIGHTED, hot policy y finality de reservas.
- [[Echo Futures — D2-07 Execution Runtime]] — M1/M2, venue-authoritative finality, cancel/fill race, modify/replace, reconnect y separación entre Operation facts y Position física.

Baseline Echo congelado por el workstream: xKoRx/echo@372af59a7b83604781346613da01e3d510ea1360. No fue necesario abrir source adicional para decidir esta corrección: ambos defects viven en contratos Futures D2 todavía no implementados. D2-09 ya clasificó echo/operation, echo/provider_rules y el nuevo domain package como superficies NEW_REQUIRED_FOR_V1. El source permanece READ-ONLY EVIDENCE y esta corrección no le atribuye capacidades Futures inexistentes.

## 3. Trazabilidad de los defects

| Finding | Defecto demostrado | Causa contractual | Corrección candidata |
|---|---|---|---|
| D3-02 | Dos REDUCE/EXIT distintas pueden validar contra la misma logical_exposure y llenar ambas, cruzando la dirección de la Operation. | La guard actual mira cada Order aisladamente y no descuenta la cantidad todavía ejecutable de otras Orders opuestas vivas. | La Operation debe acotar el conjunto completo de cantidad todavía ejecutable en sentido reductor. La Order misma actúa como claim local mientras pueda producir fills adicionales. |
| D3-03 | Una EXIT local puede aumentar NET_ABS account-wide; con otra reserva viva el cap puede romperse aunque cada decisión individual parezca válida. | Las salidas no participan universalmente en live_reservations; por eso firm_by_operation cambia después del Fill sin que el envelope previo haya cubierto ese Fill. | Toda Order que pueda mover una métrica shared-cap debe reservar su delta ejecutable firmado, también REDUCE/EXIT/ForceClose. El cap se evalúa sobre el conjunto alcanzable completo, no sobre roles semánticos. |

La corrección es una sola: **un Fill futuro permitido debe estar previamente representado como cantidad ejecutable outstanding en el owner que necesita demostrar su invariant**. Localmente esa cantidad protege la dirección de una Operation; account-wide esa misma cantidad alimenta el envelope de provider capacity.

## 4. Modelo contractual unificado

### 4.1 Convención de signos

BUY aporta delta positivo. SELL aporta delta negativo.

Para una Operation o:

- e_o = exposición lógica firme actual = suma firmada de sus Fills venue-authoritative.
- d_o = +1 para LONG y −1 para SHORT; la dirección sigue sellada por el OPEN Signal y es immutable.
- x_o = d_o × e_o. En estado normal x_o ≥ 0. x_o < 0 sigue siendo el breach existente EXPOSURE_INVARIANT_BREACH; esta corrección no clampa ni repara Fill truth.
- Para cada Order j existe q_exec_max(j): cota superior de cantidad adicional que todavía puede ejecutar físicamente según la evidencia autoritativa conocida.
- b_o = suma de q_exec_max de Orders BUY de la Operation.
- s_o = suma de q_exec_max de Orders SELL de la Operation.

El intervalo de exposición firmada físicamente alcanzable desde el estado actual, si las Orders vivas ejecutan en cualquier ordering permitido, es:

I_o = [e_o − s_o, e_o + b_o]

No se requiere una nueva entidad de dominio para representar I_o. Se deriva del estado de Orders que ya pertenece al aggregate.

### 4.2 Qué significa q_exec_max

q_exec_max no es filled_qty restante por conveniencia de UI. Es la cota conservadora de fills adicionales todavía posibles.

Reglas mínimas:

- Una Order PENDING_SUBMIT que todavía puede llegar al egress cuenta por su qty actualmente autorizable.
- Una Order SUBMITTED/WORKING cuenta por su remaining executable quantity.
- Una cancel request o cancel ACK no reduce q_exec_max por sí sola.
- CANCELLED/EXPIRED sin TERMINAL_EXECUTION_FINAL conservan el remanente que el venue todavía podría reportar como late fill.
- Un modify-increase adquiere capacidad adicional antes de poder emitirse; desde el point-of-no-return se cuenta por el máximo de los términos viejo/nuevo todavía físicamente posible hasta que el venue haga autoritativo el nuevo estado.
- Un modify-decrease no libera cantidad hasta ACK venue-authoritative del nuevo quantity.
- Replace cancel+new mantiene simultáneamente la capacidad de la Order vieja y la de la nueva mientras ambas puedan ejecutar; no existe transferencia optimista de claim.
- FILLED con filled quantity que ya consume toda la cantidad ejecutable deja remanente cero; la finality continúa gobernando la liberación de cualquier remanente no ejecutado.
- REJECTED es cero sólo cuando la semántica M2 demuestra que ninguna orden física fue aceptada; timeout/ambigüedad no equivalen a REJECTED.
- TERMINAL_EXECUTION_FINAL fija q_exec_max = 0 para el remanente no ejecutado.
- Un Fill genuino posterior a la finality que contradiga esa evidencia permanece fact real y entra al breach existente post-finality; no se inventa una reserva retroactiva.

Esta definición reutiliza directamente la autoridad D2-07 sobre finality. No crea una segunda noción de “Order viva”.

## 5. Corrección D3-02 — Operation direction safety

### 5.1 Reducible exposure local

Para una Operation LONG, las Orders que pueden cruzar la dirección son SELL. Para una SHORT, son BUY.

Definimos outstanding_reducing_qty como la suma de q_exec_max de todas las Orders cuyo side es opuesto a d_o.

La condición local obligatoria pasa de “new_reduce_qty ≤ logical_exposure” a:

outstanding_reducing_qty + candidate_reduce_qty ≤ x_o

Equivalente por dirección:

- LONG: e_o − s_o ≥ 0.
- SHORT: e_o + b_o ≤ 0.

Una nueva REDUCE, EXIT o Order de ForceClose sólo puede construirse/expandirse si después de incorporarla sigue cumpliéndose esa desigualdad. El role de la Order continúa siendo auditoría; la seguridad se decide por side y cantidad ejecutable.

### 5.2 Por qué cierra la carrera de dos reducciones

El state owner echo/operation ya serializa decisiones para una Operation. Cuando la primera reducción crea su Order PENDING_SUBMIT, esa Order entra inmediatamente en outstanding_reducing_qty, incluso antes de Fill. La segunda decisión observa el claim ya consumido y sólo puede usar el saldo no reclamado.

Serializar construcción ahora sí sirve porque el recurso serializado no es “exposición ya fill-eada”, sino “exposición todavía no comprometida a otra Order que puede fill-ear”.

### 5.3 Fill como transferencia, no liberación optimista

Cuando una reducción obtiene Fill f:

- e_o se acerca a cero por f.
- q_exec_max de esa misma Order disminuye por f.

Ambos cambios pertenecen al mismo aggregate event. La cota local no se abre artificialmente: cantidad que estaba outstanding pasa a firm ejecutada.

Ejemplo LONG e=5 con SELL outstanding 3: lower bound = 2. Fill SELL 1 produce e=4 y remaining SELL=2: lower bound sigue 2. El Fill no crea un hueco que otra reducción pueda consumir dos veces.

### 5.4 ForceClose

ForceClose registra termination intent como ya exige D2. No emite “SELL/BUY por logical_exposure completa” ignorando Orders existentes.

Al recibir ForceClose, echo/operation:

- solicita cancel de Orders incompatibles con terminar, según el safety flow existente;
- conserva los q_exec_max de esas Orders hasta finality real;
- calcula sólo el exposure todavía no reclamado por reducciones ejecutables;
- puede crear nuevas close Orders únicamente por esa cantidad no reclamada;
- reevalúa después de cada Fill/finality/ACK que cambie la cota.

Por tanto EXIT normal + ForceClose no pueden crear dos cierres completos sobre la misma exposición.

### 5.5 ENTRY/ADD durante termination

Una Order expansiva no autoriza anticipadamente una reducción mayor. Si ENTRY/ADD todavía no fill-eó, su quantity no incrementa x_o.

Si un Fill expansivo ocurre primero, e_o aumenta y recién ese hecho venue-authoritative puede aumentar la cantidad reducible local. Esto mantiene safety bajo el ordering adversarial “reduce fills before add”.

## 6. Corrección D3-03 — account-wide executable capacity

### 6.1 Capacity projection

echo/provider_rules(account_id) conserva su ownership y los dos conjuntos congelados, refinados así:

- firm_by_operation mantiene e_o firmado, proveniente exclusivamente de CapacityStateUpdate cumulativo emitido desde Fills ya aceptados por echo/operation.
- live_reservations representa **toda cantidad de Order todavía físicamente ejecutable que afecte un shared cap**, no sólo ENTRY/ADD. Incluye REDUCE, EXIT y safety/ForceClose cuando sus deltas impactan GROSS, NET_ABS o GROUP_WEIGHTED.

Una reservation debe poder identificar al menos: account, operation, order/request, contract/product_group/scope, side/sign, cantidad concedida, cantidad acumulada fill-eada, q_exec_max remanente, finality state y provenance del grant/rule authority.

No se crea portfolio aggregate ni coordinator. Sigue siendo estado account-keyed dentro de provider_rules.

### 6.2 El boundary Operation → provider_rules

Antes de que una Order capaz de afectar shared capacity pueda volverse físicamente ejecutable, echo/operation solicita una reservation por el delta firmado y exacto de esa Order.

El orden conceptual es:

1. Operation valida direction safety local.
2. Operation construye/retiene la Order como PENDING_SUBMIT; por ello su claim local ya existe.
3. Si la Order toca shared caps, solicita CapacityReservation por su cantidad firmada ejecutable.
4. provider_rules serializa el request junto con firm_by_operation y todas las live_reservations de la account.
5. GRANTED agrega la reservation antes de que el resultado durable pueda habilitar egress.
6. DENIED impide egress; la Order converge a REJECTED por provider gate según el contrato existente y el claim local se libera sólo porque se demostró que ningún side effect físico fue permitido.
7. D4-A3 decidirá cómo revalidar autoritativamente el grant justo antes del egress; este artifact no diseña ese mecanismo.

PER_ORDER puro sigue siendo chequeo local cuando no existe shared cap aplicable. No se obliga a crear shared state donde la policy no lo necesita.

### 6.3 Fill update: reservation → firm

Todo Fill Echo, cualquiera sea el role de su Order, ya genera CapacityStateUpdate cumulativo. La corrección exige que, si el Fill pertenece a una Order con reservation, provider_rules actualice en una única invocación account-keyed:

- firm_by_operation al nuevo e_o cumulativo;
- filled quantity de la reservation;
- q_exec_max remanente de esa reservation.

Esto convierte capacidad incierta en exposición firme sin ampliar el conjunto alcanzable.

La propiedad que D2 intentaba atribuir al skew se vuelve verdadera después de esta corrección: mientras provider_rules todavía no procesa el Fill, conserva la reservation antigua completa, que ya incluía ese Fill como resultado físicamente posible. Por eso el estado stale sobre-reserva o conserva exactamente el envelope; no puede omitir el Fill. El defecto D3-03 existía precisamente porque una EXIT no estaba representada antes del Fill.

## 7. Métricas account-wide

Todas las fórmulas siguientes se evalúan por el scope tipado de la policy. Un mismo Order puede afectar más de un constraint; el grant es válido sólo si satisface todos los constraints aplicables.

### 7.1 NET_ABS

Sea:

- N = suma de e_o firmes en el scope.
- B = suma de q_exec_max de todas las reservations BUY vivas en el scope.
- S = suma de q_exec_max de todas las reservations SELL vivas en el scope.

El neto físicamente alcanzable por Orders correctamente autorizadas está contenido en:

I_account = [N − S, N + B]

El envelope NET_ABS es:

Env_NET_ABS = max(abs(N − S), abs(N + B))

Un candidate Order se incorpora primero al lado B o S que corresponda y sólo recibe grant normal si el envelope resultante es ≤ cap.

Esto no netea Orders outstanding entre sí. Evalúa ambos extremos de ejecución adversarial.

### 7.2 Demostración directa del contraejemplo D3-03

Estado inicial: A=+4, B=−4, por lo tanto N=0 y cap NET_ABS=5.

Si C obtiene BUY 5 primero, B=5 y Env=5. La EXIT de la Operation short B es también BUY 4: incorporarla produciría B=9 y Env=9, por lo que no puede quedar simultáneamente ejecutable.

Si la EXIT BUY 4 obtiene grant primero, Env=4. El BUY 5 de C produciría Env=9 y es denegado.

El orden de requests cambia quién obtiene capacidad primero, pero ningún orden válido deja ambas cantidades ejecutables a la vez. El cap permanece demostrado.

### 7.3 GROSS

Para cada Operation o, su intervalo alcanzable es I_o=[L_o,U_o]=[e_o−s_o,e_o+b_o].

El peor gross de esa Operation es:

G_o = max(abs(L_o), abs(U_o))

El envelope GROSS del scope es:

Env_GROSS = Σ G_o

Con Orders físicamente independientes este es el peor caso exacto por Operation y evita tanto el netting inseguro como la sobre-simplificación “toda exit libera gross”. Bajo direction safety local, una reducción pura no aumenta G_o; una expansión sí puede hacerlo.

### 7.4 GROUP_WEIGHTED

GROUP_WEIGHTED no gana una semántica implícita nueva. El RuleSet debe declarar si el grupo usa agregación weighted-GROSS o weighted-NET_ABS y los pesos tipados positivos aplicables.

- weighted-GROSS: Σ w_o × max(abs(L_o), abs(U_o)).
- weighted-NET_ABS: max(abs(Σ w_o×e_o − Σ w_o×s_o), abs(Σ w_o×e_o + Σ w_o×b_o)).

No se permite netear productos heterogéneos sólo porque comparten product_group; debe existir la regla/weight authority que ya exige D2-05.

## 8. Exposición física existente y Position

La corrección no promueve Position a verdad de Operation ni inventa residuals sintéticos.

La base de capacity firm atribuible a Echo sigue siendo Fill-derived firm_by_operation. Position física venue-authoritative cumple una función diferente: validar si esa base puede considerarse confiable para seguir autorizando efectos.

Regla:

- si Position fresca/completa reconcilia con la suma lógica dentro de la tolerancia vigente, provider_rules puede seguir usando firm_by_operation + reservations para enforcement;
- si existe POSITION_MISMATCH material, Position stale/ausente o breach post-finality, PHYSICAL_STATE_UNTRUSTED corta grants ordinarios que puedan aumentar el envelope;
- no se calcula silently “exposición por Operation” desde Position ni se fabrican Fills;
- una acción automática de close/safety bajo estado físico no confiable sólo puede seguir cuando la evidencia disponible permite demostrar que es no-expansiva; de lo contrario el runtime conserva termination pending y exige reconcile-first/operator según D2-07.

Así la exposición física ya existente participa de safety sin contaminar la identidad lógica.

## 9. Exits, safety y la propiedad de no dejar una posición atrapada

### 9.1 Se eliminan dos equivalencias falsas

REDUCE/EXIT/ForceClose local ≠ reducción de toda métrica account-wide.

Role EXIT ≠ bypass de capacity.

Una Order puede reducir x_o de su Operation y a la vez aumentar NET_ABS account-wide al retirar una pata que estaba offsetting otra Operation.

### 9.2 Regla V1

Para V1 no se agrega una semántica genérica de wind-down, chunking automático ni override de hard caps. Una Order que afecte un shared cap se valida contra las familias de reglas **realmente soportadas por los ProviderRuleSet V1**.

El caso teórico donde ninguna cantidad mínima permitida puede reducir una Operation sin violar otra regla queda **DEFERRED / YAGNI**. Se reabre sólo con evidencia de una prop/programa real que lo necesite. No requiere Owner Decision en D4.

## 10. Lifecycle de reservations y local claims

### Partial fill

El Fill siempre se conserva. Operation actualiza e_o y q_exec_max local. CapacityStateUpdate mueve la misma cantidad de reservation a firm. No se libera headroom dos veces.

### Cancel + Fill race

Cancel request/ACK no libera local claim ni provider reservation. Si el Fill gana la race, estaba cubierto por ambas cotas. Finality posterior libera sólo el remanente que venue-authoritative evidence demuestra imposible de ejecutar.

### Late fill

Mientras no exista finality, el late Fill estaba dentro de q_exec_max y la reservation. Después de finality, un Fill nuevo contradice la autoridad usada para cerrar el envelope: se preserva como hecho y entra al breach post-finality ya definido; esta corrección no falsifica seguridad frente a un venue que contradice su propia finality.

### Modify increase

La expansión de q_exec_max necesita primero direction headroom local si es reducción, y capacity delta adicional si toca shared caps. Sólo después puede emitirse el modify.

### Modify decrease

No se reduce q_exec_max ni reservation hasta ACK venue-authoritative de los términos menores. Un rechazo conserva el estado anterior.

### Replace

Old Order y replacement Order son dos side effects independientes. El old q_exec_max/reservation permanece hasta finality; el new necesita su propio local headroom y provider grant. Durante la transición se puede denegar de más; nunca se cuenta de menos.

### Terminal Operation

La Operation sigue exigiendo e_o=0, cero Orders con q_exec_max>0 o finality pendiente relevante, e intent de terminación. Finality de Orders y exposure cero deben estar demostrados antes de liberar el lifecycle.

## 11. Invariantes corregidos

**A2-I1 — Fill truth:** e_o es siempre la suma firmada de Fills venue-authoritative; jamás clamped o derivada desde Position.

**A2-I2 — Direction safety:** para toda Operation no-breach, el peor caso de todas sus Orders correctamente emitidas no cruza cero: LONG ⇒ e_o−s_o≥0; SHORT ⇒ e_o+b_o≤0.

**A2-I3 — No local double-spend:** una cantidad de exposición ya representada por q_exec_max de una reducción no puede volver a ser reclamada por otra reducción hasta Fill/finality/ACK que cambie esa cota.

**A2-I4 — Reservation completeness:** toda Order que pueda mover un shared cap posee una reservation que cubre su q_exec_max antes de poder ser físicamente ejecutable; role EXIT/REDUCE/SAFETY no constituye exención.

**A2-I5 — Reachability envelope:** provider_rules concede una reservation sólo si firm exposure + live reservations satisfacen las reglas/caps aplicables del ProviderRuleSet V1.

**A2-I6 — Fill covered before arrival:** todo Fill normal de una Order Echo estaba contenido en el reachable set previamente reservado. Al convertirse de reservation a firm no puede ensanchar ese reachable set.

**A2-I7 — Conservative skew:** una CapacityStateUpdate atrasada no subestima riesgo mientras la reservation anterior permanece viva; el provider puede denegar de más, no autorizar de más. Este claim sólo es válido después de hacer reservation-complete todas las Orders afectantes del cap.

**A2-I8 — Venue-authoritative release:** cancel request, local enum terminal y timeout no liberan quantity ejecutable; únicamente evidence autoritativa de nueva qty/finality permite disminuir q_exec_max o liberar reservation.

**A2-I9 — Physical/logical separation:** Position no muta e_o ni atribuye exposure a Operations; mismatch/staleness degrada trust y corta grants ordinarios.

**A2-I10 — Safety is intent:** ForceClose usa exactamente las mismas cotas locales y account-wide. No puede saltarse direction safety ni inventar capacity por ser safety.

**A2-I11 — No cap-by-role:** el provider evalúa signed executable quantity y scope; no infiere riesgo de labels ENTRY/ADD/REDUCE/EXIT.

**A2-I12 — No hidden resize:** provider_rules concede o deniega la cantidad exacta construida por MM; nunca redimensiona silenciosamente una Order.

## 12. Boundary de información

### Pertenece exclusivamente a echo/operation

- direction immutable de la Operation.
- e_o lógico derivado de sus Fills.
- Orders y q_exec_max por Order.
- outstanding_reducing_qty y available_reducible_qty locales.
- lifecycle, termination intent, mm_state, replace/modify lineage y operation_event_seq.
- decisión de MM de construir una nueva Order o un chunk.

### Pertenece exclusivamente a echo/provider_rules(account_id)

- RuleSet/binding/account risk state.
- firm_by_operation como proyección de capacity, no como aggregate alternativo.
- live_reservations de todas las Orders relevantes para shared caps.
- envelopes GROSS/NET_ABS/GROUP_WEIGHTED por scope.
- grant/deny, reason y provenance.
- PHYSICAL_STATE_UNTRUSTED y safety/cap conditions account-wide.

### ProviderRuleSet completo → MoneyManagement

El `ProviderRuleSet` efectivo se expone **completo y read-only** al contexto account-specific/MM; no existe un subset filtrado “sólo para sizing”. El MM puede usar cualquier regla de la prop para decidir sizing, exposición y comportamiento de la Operation.

`MoneyManagement` sigue siendo la autoridad de sizing/risk de la Operation. `echo/provider_rules(account_id)` no calcula sizing ni compite con MM: mantiene la autoridad externa de las reglas de la prop y el gate serializado necesario para constraints account-wide/concurrentes.

La Strategy base permanece account-agnostic en V1. Como el ProviderRuleSet completo queda modelado y disponible en el seam account-specific, estrategias provider-aware futuras pueden agregarse de forma aditiva sin rehacer el modelo de policy.

### Debe cruzar el boundary

Operation → provider_rules: request_id, operation_id, order_id, account_id, instrument/contract/product_group necesarios para resolver scope, signed side/qty, q_exec_max solicitado, kind normal/modify-increase y provenance mínima de la Order.

provider_rules → Operation: grant exacto o deny, decision/grant identity, rule authority provenance, constraints evaluados y cantidad exacta reservada.

Fill path Operation → provider_rules: operation_event_seq cumulativo, e_o cumulativo, order_id y cumulative filled/remaining data suficiente para mover reservation→firm idempotentemente.

Finality/modify path Operation → provider_rules: evidence/result que autoriza disminuir la reservation, siempre asociado a order/action identity.

Position path no cruza como “Operation exposure”: sólo alimenta el trust/safety state account-wide por el boundary de reconciliation ya congelado.

## 13. SPEC deltas candidatos

### D2-04 Operation / Order / Fill / Position

Reemplazar la guard individual “REDUCE/EXIT qty ≤ logical_exposure” por la guard conjunta sobre q_exec_max de todas las Orders opuestas todavía ejecutables.

Agregar q_exec_max como concepto derivado/contractual de Order; no requiere entidad nueva.

Reescribir ForceClose para que emita sólo reducible exposure no reclamado por otras Orders y espere finality antes de reutilizar quantity cancelada.

Reemplazar el riesgo R5 “concurrent close converges por dedup/terminal guards” por el invariant preventivo A2-I2/A2-I3. Dedup sigue siendo necesario para duplicate events, pero deja de presentarse como exclusión económica entre Orders distintas.

Alinear modify/replace con la misma cota local: increase reclama delta antes de egress; decrease libera sólo tras ACK; replacement no hereda claim prematuramente.

### D2-05 / D2-05C Provider

Cambiar Stage-2 desde “reserva de new risk” a “reserva de signed executable quantity que afecte shared caps”.

Retirar I-C6 en su forma “salidas jamás bloqueadas por gates provider”. Sustituir por: ninguna salida se bloquea por ser salida cuando es account-wide non-expanding; salidas que expanden una métrica requieren headroom normal o el comportamiento owner-decided de OD-D4-A2-01.

Reemplazar las fórmulas que sólo suman reservations de ENTRY/ADD por los envelopes de reachable intervals de §7.

Mantener venue-authoritative reservation finality, pero hacerla aplicable a reservas de EXIT/REDUCE/safety.

Corregir el claim de skew: es conservador sólo si todas las Orders que pueden mover el cap están previamente representadas por reservation.

Mantener PHYSICAL_STATE_UNTRUSTED como guard; no promover Position a firm_by_operation.

### Architecture Candidate V1

En §4 direction/lifecycle: sustituir la validación individual por local reachable-exposure safety.

En §7 Provider runtime: eliminar “salidas nunca bloqueadas” y declarar reservation completeness sólo para las familias de policy V1 realmente soportadas.

En §7 Capacity: definir firm + all executable live reservations como la única base demostrable del envelope.

En §8/Finality: conservar sin cambios conceptuales la autoridad venue; referenciarla como única vía de release del remanente incierto.

## 14. Walkthroughs adversariales

### W1 — dos REDUCE simultáneas

Operation LONG e=5. REDUCE A SELL3 se construye primero: s=3, lower=2. REDUCE B SELL3 intentaría s=6, lower=−1 ⇒ rechazo local antes de provider/egress. Si B pide SELL2, s=5, lower=0 ⇒ permitido. Cualquier combinación de fills A/B termina entre 0 y 5, nunca short.

### W2 — EXIT completa + ForceClose

LONG e=1. EXIT SELL1 está WORKING, q_exec_max=1. ForceClose registra termination y pide cancel. Mientras no exista finality de EXIT, available reducible=0; no puede crear otro SELL1. Si EXIT fill-ea, e→0 y remaining→0: termination converge. Si venue finaliza cancel sin fill, q_exec_max→0, e sigue1 y recién entonces ForceClose puede emitir SELL1.

### W3 — partial fill + cancel

LONG e=3. SELL3 está reservada local/account-wide. Fill1 produce e=2 y q_exec_max=2. Cancel ACK llega: q_exec_max sigue2 hasta finality. Late Fill1 antes de finality produce e=1/q=1 y ya estaba cubierto. Finality venue-filled-total=2 libera el último1; safety puede ahora decidir qué hacer con e=1.

### W4 — replace

LONG e=3. Old EXIT SELL3 tiene q=3. Se solicita replace. Mientras old no sea final, new SELL3 no cabe localmente porque old ya reclama toda la reducción. El sistema debe esperar finality o reemplazar con una cantidad cuya suma old+new siga ≤3. Esto es deliberadamente conservador salvo que D6 certifique una primitive venue realmente atómica/mutually-exclusive; el generic V1 no la presume.

### W5 — modify decrease race

EXIT SELL4 sobre LONG e=4. Modify a SELL2 sale; hasta ACK, local y provider siguen contando 4. Si fill3 llega antes del ACK, estaba cubierto. Si ACK de 2 es venue-authoritative respecto de remaining terms, recién entonces se ajusta q_exec_max según fills ya observados.

### W6 — NET_ABS con Operations opuestas y nueva exposición

A=+4, B=−4, cap5. C BUY5 obtiene grant ⇒ B reservations total BUY=5. EXIT de B BUY4 intentaría envelope9 ⇒ denegada. Alternativamente EXIT B primero ⇒ envelope4 y C queda denegada. Ningún ordering de grants permite el estado inseguro D3-03.

### W7 — NET_ABS con dos exits opuestas

A=+4 y B=−4, cap5. EXIT A SELL4 y EXIT B BUY4 pueden coexistir: N=0, S=4, B=4 ⇒ reachable [−4,+4], Env=4. Si una llena primero, el net físico llega como máximo a ±4; si la otra llena después vuelve a0. Clasificarlas ambas como “reservadas” no significa bloquearlas: significa demostrar que juntas caben.

### W8 — ForceClose account-wide

Varias Operations reciben ProviderForceClose. Cada op genera intents, pero cada close Order solicita capacity account-keyed. provider_rules serializa grants y conserva el envelope después de cada prefix. No existe un coordinator global; el owner account-keyed ya necesario para caps basta para impedir combinaciones inseguras. Operations denegadas permanecen termination pending y reevalúan tras fills/finality/capacity changes.

### W9 — reservation stale mientras Fill ya ocurrió

provider_rules observa e=0 y BUY reservation5. En el venue ocurre Fill BUY3; Operation ya pasó a e=3 y remaining2, pero CapacityStateUpdate aún no llegó. provider_rules todavía mantiene reachable [0,5]. El estado físico real3 sigue dentro de la cota. Al aplicar update: firm3 + remaining BUY2 conserva upper endpoint5. No hubo ventana de subestimación.

### W10 — EXIT Fill stale, el caso que antes rompía D3-03

Operation short −4 tiene EXIT BUY4 reservada antes del egress. Aunque su Fill llegue físicamente antes del CapacityStateUpdate, provider_rules ya tenía B=4 en el interval. El net account-wide que puede crear esa salida estaba cubierto antes de existir. La salida deja de ser una mutación sorpresa del firm projection.

### W11 — Position mismatch / actividad externa

firm_by_operation suma net +3 pero Position fresca reporta +5. No se asigna el residual +2 a ninguna Operation. PHYSICAL_STATE_UNTRUSTED corta grants ordinarios. Safety sólo emite acciones demostrablemente no-expansivas con evidencia suficiente o hace reconcile-first; ningún provider cap se “repara” inventando Fill.

### W12 — Fill posterior a TERMINAL_EXECUTION_FINAL

La reservation fue liberada porque venue finality afirmó que no había remanente. Aparece un execution id genuino nuevo. El Fill se conserva; Operation no se reescribe ni se clampa. Se marca el breach post-finality/provider cap breach existente. La garantía preventiva se define contra un venue que respeta su evidencia de finality; una contradicción del propio venue queda fail-visible, igual que D2 ya exige.

## 15. Acceptance cases para SPEC/QA posterior

| ID | Caso | Acceptance |
|---|---|---|
| A2-01 | Two independent REDUCE | La suma de q_exec_max opuesta jamás supera x_o; la segunda Order incompatible no llega a egress. |
| A2-02 | EXIT + ForceClose | ForceClose no duplica la cantidad ya reclamada por EXIT; cancel no libera hasta finality. |
| A2-03 | Partial fill | Fill mueve cantidad de outstanding a firm sin ensanchar el local/account reachable set. |
| A2-04 | Cancel/fill race | Todo late Fill pre-finality estaba cubierto por claim+reservation; no existe release por cancel ACK. |
| A2-05 | Modify increase/decrease | Increase requiere delta local+provider antes de egress; decrease no libera antes de ACK. |
| A2-06 | Replace | Old+new se cuentan concurrentemente mientras ambas puedan ejecutar; no optimistic transfer. |
| A2-07 | NET_ABS offsetting + entry | El escenario +4/−4, BUY5, EXIT BUY4 nunca supera cap5 bajo ningún ordering de grant/fill. |
| A2-08 | Two opposite exits | +4/−4 con SELL4+BUY4 puede ser autorizado bajo cap5 porque envelope reachable es [−4,+4]. |
| A2-09 | GROSS | Cada Operation usa max(abs(L),abs(U)); una reducción direction-safe no aumenta su gross worst-case. |
| A2-10 | GROUP_WEIGHTED | La evaluación usa modo weighted-GROSS o weighted-NET_ABS explícito; no hay netting implícito cross-product. |
| A2-11 | Stale CapacityStateUpdate | Mientras el Fill no se proyecta, la reservation antigua sigue cubriendo el estado físico posible. |
| A2-12 | Physical mismatch | Position no muta Operation; mismatch corta grants ordinarios y no fabrica attribution. |
| A2-14 | Exit that affects a supported shared cap | No recibe bypass por role; se valida contra la familia de policy V1 aplicable. |
| A2-15 | Provider grant denied | No hay side effect; reservation y claim local convergen a release, Order queda durable REJECTED{PROVIDER_GATE}. |
| A2-16 | Late fill after finality | Fill preservado + breach visible; no clamp, no reserva retroactiva, no contaminación silenciosa. |
| A2-17 | ForceClose multi-Operation | Cada prefix de grants account-keyed mantiene todos los envelopes; no coordinator global requerido. |

## 16. Contrato que D4-A3 puede consumir sin reinterpretación

D4-A3 debe tomar los siguientes hechos como input congelable de este workstream y resolver únicamente authoritative revalidation:

1. **Grant exacto, no permiso genérico.** Un grant corresponde a una Order/action identity concreta, una signed executable qty exacta y los cap scopes/families evaluados.
2. **Reservation ya existe al conceder.** Cuando GRANTED es durable, provider_rules ya incorporó esa cantidad a live_reservations en el owner account-keyed. El result no precede a la reserva.
3. **Grant no es final egress authority.** Prueba que la cantidad cabía en el linearization point del grant; no prueba que una authority update posterior permita todavía emitirla.
4. **Reservation completeness.** EXIT/REDUCE/ForceClose que afecten shared caps llegan a D4-A3 con reservation igual que ENTRY/ADD. A3 no puede aplicar bypass por role.
5. **Local direction safety ya fue resuelta por Operation.** A3 no recalcula reducible exposure, no cambia direction y no aumenta qty. Un provider grant nunca autoriza a violar el claim local.
6. **Cap math pertenece a provider_rules.** A3 no reimplementa NET_ABS/GROSS/GROUP_WEIGHTED desde un snapshot local. Debe consultar/atravesar la authority account-keyed de manera que D3-04 quede cerrada en su propio workstream.
7. **Revalidation trabaja sobre el grant original.** Debe preservar grant/request/order/operation identity, signed qty, scope/family y rule provenance. Si la policy vigente cambia el resultado, la respuesta es VALID o INVALID para esa cantidad; no silent resize.
8. **INVALID antes de egress significa cero side effect.** Operation lleva la Order a REJECTED{PROVIDER_GATE}, libera provider reservation mediante el protocolo owner-to-owner y libera el claim local sólo porque se ha demostrado que esa Order nunca quedó físicamente ejecutable. Si era safety, termination intent permanece pending.
9. **Fill/finality siguen gobernando después de egress.** Una vez el command puede haber alcanzado el venue, A3 no revoca capacity “por config”; reservation→firm/finality usa los facts M2 ya definidos.
10. **Position no es input para reatribuir Operation.** A3 puede respetar PHYSICAL_STATE_UNTRUSTED/account safety state de provider_rules, pero no calcula exposición de Operation desde Position.
11. **D3-04 permanece abierto.** Este artifact deliberadamente no decide el protocolo que garantiza que la revalidation observa la authority más reciente; sólo fija qué debe revalidarse y quién posee la matemática.

## 17. Riesgos residuales y decisiones

### Deferred V1 — no-safe-unwind edge

El caso donde ninguna cantidad mínima permitida puede reducir una Operation sin violar otra regla queda fuera de V1 por YAGNI. Se reabre sólo con evidencia de una prop/programa real que lo necesite; no existe Owner Decision pendiente en D4-A2.

### Riesgos que no requieren nueva arquitectura

- Venue que contradice TERMINAL_EXECUTION_FINAL: breach fail-visible ya aceptado; no se puede hacer preventivamente safe contra evidencia autoritativa falsa.
- Transport con replace/OCO/reduce-only realmente atómico: puede permitir una cota q_exec_max menor que la suma independiente, pero sólo después de certificación transport-specific. Generic V1 asume independencia; no diseña optimización hoy.
- CapacityStateUpdate lag: con reservation completeness pasa a ser conservador; requiere tests de fault/interleaving pero no un nuevo state owner.

## 18. Veredicto de workstream

D3-02 queda corregido por contrato: el aggregate Operation deja de validar reducciones una a una contra el mismo firm exposure y pasa a demostrar un lower/upper bound conjunto sobre todas las Orders todavía ejecutables.

D3-03 queda corregido para el alcance V1: una Order que pueda mover una familia shared-cap realmente soportada participa de live_reservations antes de poder ejecutar; firm + outstanding define el reachable envelope bajo cualquier ordering permitido. Casos de policy no demostrados por providers V1 se agregan después como extensiones aditivas.

D3-02: CANDIDATE_RESOLVED

D3-03: CANDIDATE_RESOLVED

OWNER_DECISIONS_REQUIRED: NONE

CONTRACT_FOR_D4_A3: grant exacto por Order/action + signed executable qty + cap scopes/families + rule provenance; reservation account-keyed creada antes del GRANTED; EXIT/REDUCE/ForceClose incluidas cuando afectan shared caps; local direction claim pertenece a Operation y no puede ser reinterpretado; cap math pertenece a provider_rules; revalidation debe validar el grant exacto contra authority account-keyed vigente sin silent resize ni bypass por role; INVALID pre-egress implica cero side effect y release explícito de reservation/claim; post-egress Fill/finality siguen venue-authoritative.

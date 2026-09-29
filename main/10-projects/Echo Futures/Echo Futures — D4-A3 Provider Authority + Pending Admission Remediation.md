---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D3 Astra Architecture Review]]"
  - "[[Echo Futures Architecture Candidate V1]]"
  - "[[Echo Futures — D4-A1 Market Identity + Exact Replay Remediation]]"
  - "[[Echo Futures — D4-A2 Exposure + Capacity Safety Remediation]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
  - "[[Echo Futures — D2-05 Instrument Session Provider]]"
  - "[[Echo Futures — D2-05C Provider Program Rules]]"
  - "[[Echo Futures — D2-07 Execution Runtime]]"
  - "[[Echo Futures — D2-08 Strategy Runtime]]"
aliases:
  - Echo Futures D4-A3
  - EF D4-A3 Provider Authority Pending Admission
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-remediation
created: "2026-09-28"
updated: "2026-09-28"
---

# Echo Futures — D4-A3 Provider Authority + Pending Admission Remediation

## 1. Scope y status

Este artifact es una corrección arquitectónica candidata y acotada para los findings aceptados D3-04 y D3-06.

No reemplaza al Primary Manager, no modifica Echo físico, no emite un gate global de D4, no diseña D5, Q12 ni Q13 y no produce una Architecture Candidate V2.

La corrección consume sin reinterpretación los contratos ya aceptados de D4-A1 y D4-A2. En particular:

- echo/operation, key account_id:account_strategy_id, sigue siendo owner de lifecycle, Orders, Fills, exposición lógica, MoneyManagement state y claims locales;
- echo/provider_rules, key account_id, sigue siendo la única authority account-wide de ProviderRuleSet, binding/provider state, caps, reservations y provider safety;
- el grant de D4-A2 es exacto para una Order/action concreta, con signed executable quantity y scopes/families aplicables;
- la reservation account-wide ya existe antes de GRANTED;
- local direction safety no se recalcula en A3;
- cap math no se replica en Operation;
- INVALID antes de egress implica cero side effect físico;
- después de egress, Fill/finality continúan siendo venue-authoritative;
- Position física no atribuye exposure a Operations;
- ProviderRuleSet completo continúa disponible read-only para el contexto account-specific/MoneyManagement; provider_rules no se convierte en un segundo MoneyManagement.

La causa común de ambos findings es la misma: una respuesta asíncrona de provider_rules no puede actuar como permiso descontextualizado. Debe estar ligada a una continuación exacta y consumirse bajo el owner correcto.

La solución NO crea un framework genérico de continuations. Aplica el mismo principio en dos lugares concretos:

1. D3-04: un grant reservado sólo habilita egress después de atravesar una vez más, de forma obligatoria, la authority account-keyed. Ese paso final queda committed en la reservation existente.
2. D3-06: un OPEN pre-Operation mantiene una única continuación pending dentro del state owner echo/operation. Signals posteriores pueden invalidarla o supersederla antes de que un AdmissionResult tenga efecto.

## 2. Conclusión ejecutiva

### D3-04

La condición local “revalidar sólo si veo que cambió el epoch” se elimina.

Toda Order/action con grant todavía no emitida ejecuta exactamente una revalidación autoritativa final antes del command egress:

Operation
→ ReservationRevalidate(grant exacto)
→ echo/provider_rules(account_id)
→ VALID | INVALID

La request SIEMPRE atraviesa provider_rules. Ningún snapshot/kache/epoch observado por Operation decide si puede omitirla.

El linearization point es el procesamiento de esa ReservationRevalidate en la cola serializada del owner account-keyed. VALID no es sólo una lectura: en esa misma transición provider_rules marca la live_reservation como egress-committed para ese grant exacto y conserva la authority provenance usada.

Después de ese commit, una authority update posterior está ordenada después de la autorización de esa Order y no la revoca retroactivamente. Esto evita dos errores opuestos:

- emitir con una authority v5 cuando v6 ya había sido procesada por provider_rules;
- revalidar indefinidamente porque una nueva update siempre podría aparecer después de la respuesta anterior.

INVALID retira/invalida la reservation pre-egress en el mismo owner. Operation recibe el resultado, deja la Order REJECTED{PROVIDER_GATE} y libera su claim local. No existe silent resize.

### D3-06

Antes de que exista una Operation, el function owner echo/operation puede tener un único slot nullable:

pending_admission

Ese slot no es una Operation, no es un aggregate nuevo y no es un workflow.

OPEN(k) crea el slot antes de enviar AdmissionRequest. El request_id es la continuation identity. Un AdmissionResult sólo puede tener efecto si sigue coincidiendo con el pending_admission activo.

Mientras espera:

- CLOSE(k) invalida la continuación;
- CLOSE_ALL(k) invalida la continuación;
- OPEN(k+1) supersede la continuación k y comienza la de k+1 sin mantener dos admissions vivas;
- config local/binding de AccountStrategy que invalide el OPEN invalida la continuación;
- un result viejo o redelivered cuyo request_id ya no coincide es stale y no materializa nada.

DENY limpia el slot sin crear Operation. ALLOW sólo materializa si la continuación sigue activa y las guards locales corrientes continúan válidas.

La authority provider del ALLOW sigue teniendo el mismo significado de D2-05 R15: fue válida en el linearization point de ese AdmissionRequest. No se usa un snapshot local para declarar que una authority provider posterior “no cambió”. Si provider_rules cambia después de ese ALLOW, ninguna Order puede escapar con authority stale porque D3-04 obliga al commit autoritativo final antes de egress.

## 3. Reconstrucción precisa — D3-04

D2-05C C-R3.6 intentó cerrar el caso hot-cap mediante un guard local:

1. grant bajo v5;
2. Operation compara el epoch del grant con su vista corriente;
3. sólo si observa cambio dispara ReservationRevalidate;
4. si no observa cambio, emite.

Ese contrato mezcla dos authorities distintas.

La vista local de Operation puede estar atrasada aunque provider_rules ya haya procesado v6. Por lo tanto:

- “mi snapshot sigue en v5” no demuestra “la authority sigue en v5”;
- “no detecté cambio” no es una decisión autoritativa;
- el branch que omite la request evita precisamente el único owner que podría responder correctamente.

Contraejemplo aceptado por D3:

1. provider_rules concede qty 5 bajo v5;
2. la reservation exacta queda viva;
3. provider_rules procesa v6 y la authority account-keyed ya cambió;
4. Operation aún observa v5;
5. el guard local concluye “epoch unchanged”;
6. la Order puede ser emitida aunque v6 la haría INVALID.

El defecto NO exige simultaneidad global. Sólo exige que una decisión que todavía puede impedir egress atraviese a la authority que ya posee el orden de RuleSet/binding/account/risk/cap updates.

## 4. Corrección candidata — D3-04

### 4.1 Ownership

echo/operation conserva:

- Order/action identity;
- signed executable quantity construida por MM;
- q_exec_max y claim local de direction safety;
- lifecycle local;
- decisión de emitir o no el command una vez autorizado.

echo/provider_rules(account_id) conserva:

- authority provider corriente;
- RuleSet/binding/account/risk/trust state;
- cap scopes/families;
- live_reservations;
- decisión VALID/INVALID para el grant exacto;
- el commit final de egress sobre esa reservation.

Operation no calcula provider validity a partir de un epoch local.

### 4.2 Revalidación final obligatoria

Para cada grant exacto no emitido:

1. Operation conserva el grant_id/decision identity y todos los datos congelados por D4-A2.
2. Justo antes de habilitar command egress envía ReservationRevalidate.
3. La request referencia el grant exacto; no solicita un qty nuevo.
4. provider_rules procesa la request en su única cola account-keyed.
5. provider_rules evalúa la authority vigente en ese punto, incluida la reservation exacta y todas las provider-owned guards aplicables.
6. El resultado es sólo VALID o INVALID para la cantidad original.

No existe branch local “epoch igual ⇒ skip”.

No existe max_admissible_qty.

No existe silent resize.

No existe recalculation de NET_ABS/GROSS/GROUP_WEIGHTED en Operation.

### 4.3 VALID es un egress commit, no un lease

Cuando provider_rules decide VALID:

- la live_reservation ya existente permanece viva;
- en la misma transición autoritativa se registra egress_committed para ese grant;
- se conserva la provenance de authority usada en el commit;
- el resultado VALID se vuelve idempotente para redelivery del mismo grant.

egress_committed es un atributo pequeño de la reservation existente. No crea entidad, aggregate, coordinator ni timer.

Su semántica es one-shot:

> este grant exacto fue autorizado para cruzar el Core command egress en el linearization point account-keyed registrado.

Una RuleSet/binding/provider update procesada después de ese commit gobierna decisiones posteriores, pero no revoca retroactivamente esta autorización exacta.

Esto es necesario. Si toda update posterior pudiera desautorizar un VALID ya retornado, ningún punto finito podría habilitar egress sin una distributed transaction entre Operation, provider_rules y el execution edge.

### 4.4 Consumo local del VALID

Operation consume VALID sólo si:

- corresponde al grant exacto esperado por esa Order/action;
- la Order sigue localmente elegible para egress;
- el local direction claim sigue vigente;
- la continuación de egress no fue cancelada/superseded por state local.

Cuando lo consume, no intercala un nuevo ciclo de negocio. Su siguiente efecto permitido es publicar el mismo command por el boundary M1 ya congelado.

Si el estado local dejó de permitir emisión mientras esperaba el VALID:

- no se emite command;
- se ejecuta el release pre-egress explícito de la reservation;
- el claim local se libera sólo cuando queda demostrado que esa Order no pudo escapar.

No hace falta reabrir provider math para ese release.

### 4.5 INVALID y convergencia de ambos owners

Cuando provider_rules decide INVALID:

- invalida/retira la live_reservation pre-egress dentro del mismo owner account-keyed;
- persiste el resultado idempotente asociado al grant;
- responde INVALID con reason/decision provenance.

Operation al consumir INVALID:

- no publica command;
- lleva la Order a REJECTED{source: PROVIDER_GATE, decision_id};
- libera el claim local asociado a esa Order/action;
- si era una action de safety, el termination intent permanece pending.

Puede existir skew transitorio seguro:

provider reservation ya liberada
+
claim local todavía retenido mientras el INVALID no vuelve a Operation

Ese skew deniega de más localmente; no autoriza de más account-wide. Al redelivery/recovery ambos convergen.

### 4.6 Linearization point

El punto de linearización de la autorización final es:

> el procesamiento de ReservationRevalidate(grant_id) dentro de echo/provider_rules(account_id).

Secuencias:

A. v6 procesada antes de ReservationRevalidate
→ la request observa v6
→ VALID/INVALID bajo v6
→ Operation no puede “quedarse” en v5.

B. ReservationRevalidate se procesa antes de v6
→ si resulta VALID, el grant queda egress-committed bajo la authority anterior
→ v6 está ordenada después
→ no revoca retrospectivamente esa Order.

No existe tercer caso donde v6 ya fue procesada por la authority pero Operation pueda saltarse la consulta.

### 4.7 Cutoff de revocación y point-of-no-return

Hay dos fronteras distintas y no deben confundirse.

Provider revocation cutoff de A3:

> cuando el command de esa Order queda committed/visible en el egress M1 de Core.

A partir de ahí provider_rules no puede liberar o invalidar la reservation por un cambio de config porque el Futures Bridge puede consumir inmediatamente el command.

Physical point-of-no-return de M2:

> permanece en el Futures Bridge/ExecutionAdapter, después del write-ahead PREPARED/SUBMITTING definido por D2-07 y antes del primer paso que puede alcanzar al venue.

A3 no mueve ni redefine M2.

El provider commit ocurre antes del cutoff M1. Después del cutoff M1, cualquier cambio de policy actúa mediante los mecanismos normales posteriores: deny de nuevas decisiones, safety intents cuando una familia real los declare, cancel/reconciliation/finality. Nunca mediante revocación retroactiva de capacity que ya puede estar físicamente en vuelo.

## 5. Reconstrucción precisa — D3-06

D2 congeló correctamente:

- SignalDelivery ordenada por AccountStrategy;
- máximo una Operation materializada por strategy_cycle_seq;
- last_materialized_cycle_seq;
- un ciclo futuro diferible cuando la Operation anterior todavía converge.

El hueco está antes de que exista Operation.

OPEN(k) puede hacer:

OPEN(k)
→ AdmissionRequest
→ espera

Durante esa espera, echo/operation sigue recibiendo Signals de la misma AccountStrategy.

El wording anterior decía que una management Signal sin Operation es no-op/fail-visible. Aplicado literalmente:

OPEN(k)
→ pending admission
→ CLOSE_ALL(k)
→ no Operation, por lo tanto no-op
→ ALLOW antiguo
→ Operation(k) aparece tarde

Eso viola el orden lógico del ciclo: el cierre fue recibido mientras la apertura seguía siendo sólo una continuación pendiente.

La serialización por key no basta si el state owner no conserva qué continuación está abierta.

## 6. Corrección candidata — D3-06

### 6.1 Estado mínimo pre-Operation

echo/operation puede poseer, además de su state ya congelado, un único slot nullable:

~~~text
pending_admission? {
  request_id
  opening_signal_id
  strategy_cycle_seq
  opening_signal_delivery
  deferred_same_cycle_signals[]   # reutiliza el buffer acotado por un solo ciclo
}
~~~

No es domain Operation.

No obtiene operation_id.

No contiene MM state.

No reserva capacity.

No crea un nuevo state owner.

No hay más de un pending_admission activo por AccountStrategy.

La apertura original se conserva porque, si llega ALLOW, todavía se necesitan sus datos exactos para ejecutar las guards y materializar la Operation.

### 6.2 Continuation identity

request_id es suficiente como continuation identity.

Requisito de generación:

- una redelivery de la misma opening Signal debe reutilizar el mismo request_id;
- una nueva tentativa legítima originada por otra Signal usa otro request_id;
- AdmissionResult porta exactamente ese request_id.

La fórmula física queda para SPEC, pero no debe depender de wall clock para distinguir redelivery. Puede derivarse de account_strategy_id + signal_id + purpose admission, o persistirse antes del send con la misma identidad ante replay.

No se introduce continuation_id adicional.

### 6.3 OPEN(k) → pending → ALLOW

1. owner recibe OPEN(k);
2. ejecuta guards locales baratos;
3. crea pending_admission antes de enviar AdmissionRequest;
4. envía request;
5. llega ALLOW;
6. aplica sólo si result.request_id == pending_admission.request_id;
7. re-chequea valid_until, AccountStrategy vigente/enabled y guards locales ya congeladas;
8. materializa Operation(k);
9. actualiza last_materialized_cycle_seq;
10. limpia pending_admission;
11. entrega en orden cualquier deferred_same_cycle_signals retenida.

El ALLOW no autoriza Orders futuras. Toda Order sigue Stage-2 + commit final D3-04.

### 6.4 OPEN(k) → pending → DENY

DENY con request_id activo:

- produce/retiene la ProviderDecision ya definida;
- no crea Operation;
- limpia pending_admission y su buffer;
- NO avanza last_materialized_cycle_seq porque no existió Operation.

Por lo tanto un OPEN(k) distinto, posterior y todavía válido puede intentar la primera materialización del ciclo, tal como D2-08 ya congeló.

### 6.5 OPEN(k) → pending → CLOSE(k) → ALLOW

Cuando CLOSE(k) es serializada por echo/operation mientras pending_admission.strategy_cycle_seq == k:

- invalida y elimina pending_admission;
- descarta su deferred_same_cycle_signals con reason fail-visible;
- no crea termination intent porque no existe Operation;
- no necesita enviar cancel al provider: Stage-1 no posee reservation ni recurso account-wide.

Si después llega ALLOW del request antiguo:

- request_id ya no coincide con una continuation activa;
- se clasifica STALE_ADMISSION_RESULT;
- no crea Operation;
- no ejecuta MM;
- no produce Order.

CLOSE deja de ser “no-op puro” sólo en este caso preciso: no opera sobre una Operation inexistente, pero sí invalida la continuación pre-Operation que pertenece al mismo owner.

### 6.6 OPEN(k) → pending → CLOSE_ALL(k) → ALLOW

Misma regla que CLOSE(k).

CLOSE_ALL(k) invalida el pending_admission del ciclo k.

El ALLOW posterior queda stale por identity, independientemente de cuántas veces sea redelivered.

### 6.7 OPEN(k) → pending → OPEN(k+1) → resultado anterior

strategy_cycle_seq es monotónico y Strategy sólo abre k+1 después de cerrar técnicamente k.

Por lo tanto, si OPEN(k+1) es serializada mientras k sólo existe como pending_admission:

- k queda superseded;
- se elimina pending_admission(k) y su buffer;
- no se crea Operation(k);
- OPEN(k+1) comienza su propio flujo Stage-1 en el mismo único slot;
- el resultado posterior del request k se ignora por request_id mismatch.

No se mantienen admissions concurrentes k y k+1.

No se necesita una queue de ciclos.

Un salto incoherente o una acumulación que exceda las guards de cycle lag ya congeladas permanece fail-closed; A3 no inventa un backlog.

### 6.8 Signals del mismo ciclo mientras admission espera

No se permite que la latencia del provider cambie silenciosamente la semántica de Signals ya recibidas.

Mientras pending_admission(k) está activo:

- CLOSE/CLOSE_ALL(k) invalidan inmediatamente;
- otras Signals válidas del mismo ciclo que sólo pueden aplicarse tras materialización se retienen en el buffer acotado por ese único ciclo, preservando signal_seq;
- ALLOW materializa y luego las aplica en orden;
- DENY/supersede las descarta explícitamente porque no existe Operation a la cual aplicarlas.

Esto reutiliza la capacidad de buffer por un único ciclo ya aceptada en D2-08. No crea una queue genérica.

### 6.9 Config/binding/provider state mientras admission espera

Se separan authorities.

#### Cambio local que invalida la continuación

Si echo/operation procesa antes del result un cambio local que hace inválida la opening Signal —por ejemplo AccountStrategy eliminado/disabled o valid_until ya vencido— el pending_admission se invalida.

Un ALLOW posterior queda stale y no materializa.

No existe automatic retry en A3.

#### Provider update ordenada antes del AdmissionRequest

provider_rules la observa porque ambos están en la misma cola account-keyed. El AdmissionResult ya refleja la authority nueva.

#### Provider update ordenada después del AdmissionRequest/ALLOW

El ALLOW fue válido en su linearization point de Stage-1 y no se convierte retroactivamente en falso por una lectura local.

Puede todavía materializar Operation si la continuation local sigue activa.

Eso NO concede derecho de egress: antes de cualquier command, la Order debe superar el ReservationRevalidate obligatorio de D3-04 contra la authority corriente. Si la nueva provider state prohíbe la emisión, el final egress commit es INVALID y no existe side effect físico.

Así A3 evita reintroducir el mismo error de D3-04 dentro de Stage-1: un snapshot local nunca pretende decir si provider authority cambió.

## 7. Principio común entre D3-04 y D3-06

No se crea una abstracción AsyncWorkflow.

El principio compartido es sólo:

> una response asíncrona tiene identidad de continuación y sólo el owner correcto puede consumirla; una authority externa se decide en su owner serializado, y lifecycle local se decide en su owner serializado.

Aplicación:

- ReservationRevalidate usa grant_id para identificar la continuación exacta y provider_rules como authority owner.
- AdmissionResult usa request_id para identificar la continuación exacta y echo/operation como lifecycle owner.

La similitud termina ahí. No hay motivo para fusionar ambos mensajes en un protocolo genérico.

## 8. State mínimo y ownership

### 8.1 echo/operation

Estado nuevo mínimo:

- pending_admission? nullable;
- buffer same-cycle ya conceptualmente permitido por D2-08, reutilizado mientras no exista Operation.

Estado existente reutilizado:

- Signal dedup;
- last_materialized_cycle_seq;
- pending_next_cycle_open/cycle-lag semantics;
- Orders;
- q_exec_max/claims locales;
- mm_state;
- operation_event_seq.

Operation NO guarda una copia autoritativa de provider caps.

### 8.2 echo/provider_rules(account_id)

Estado nuevo mínimo dentro de live_reservation:

~~~text
egress_committed
egress_commit_decision_id
egress_commit_authority_provenance
~~~

El naming físico puede refinarse en SPEC; la semántica no.

El marker pertenece a la reservation existente. No es una nueva entidad ni un tercer state owner.

State existente reutilizado:

- effective ProviderRuleSet/binding/account/risk/trust state;
- firm_by_operation;
- live_reservations;
- dedup/results de requests;
- provider decisions;
- routing/safety state.

## 9. Message e identity contract mínimo

### 9.1 Stage-1

AdmissionRequest conserva el shape D2-05 y agrega ninguna entidad.

Identidad requerida:

~~~text
request_id
account_id
account_strategy_id
signal_id
strategy_cycle_seq
~~~

AdmissionResult:

~~~text
request_id
ALLOW | DENY_NEW_RISK
decision_id
rule authority provenance
reason
~~~

Regla:

> un result nunca se aplica “al pending actual” por posición; se aplica sólo si su request_id coincide con el pending_admission activo.

### 9.2 Stage-2 final authority commit

ReservationRevalidate reutiliza el grant exacto de D4-A2.

Debe preservar como mínimo:

~~~text
grant_id / exact grant identity
reservation request identity
operation_id
order_id
action identity cuando aplique
account_id
signed executable quantity exacta
instrument / contract / product_group / scopes necesarios
cap families evaluadas
original rule authority provenance
~~~

No requiere enviar un snapshot de cap math.

Resultado:

~~~text
grant_id
VALID | INVALID
decision_id
current authority provenance
reason?
~~~

VALID para el mismo grant es idempotente.

INVALID para el mismo grant es idempotente.

No se necesita un revalidate_id nuevo: el grant es one-shot y ya identifica exactamente qué autorización está siendo committed.

## 10. Failure / recovery walkthroughs

### W1 — D3-04 original

grant qty5 bajo v5
→ provider_rules procesa v6
→ Operation local todavía ve v5
→ ReservationRevalidate obligatorio
→ provider_rules evalúa v6
→ INVALID
→ reservation retirada pre-egress
→ Order REJECTED
→ claim local liberado
→ cero command.

La vista local atrasada deja de ser relevante.

### W2 — v6 llega después del commit

grant v5
→ ReservationRevalidate
→ provider_rules decide VALID y marca egress_committed
→ provider_rules procesa v6
→ Operation consume VALID y publica command M1.

Resultado correcto: la Order está linealizada antes de v6 para este grant exacto. v6 gobierna decisiones posteriores y safety posterior; no revoca retroactivamente.

### W3 — crash provider después del decision

provider_rules procesa ReservationRevalidate y el checkpoint no committea
→ state/result rollback
→ request redelivered
→ se reevalúa bajo el orden restaurado.

O el checkpoint committea
→ egress_committed/result quedan durables juntos
→ redelivery devuelve el mismo outcome por grant identity.

No hay double reservation ni segundo commit.

### W4 — crash Operation después de VALID y antes de M1 commit

Operation procesa VALID y prepara command, pero el checkpoint M1 aborta
→ local state/egress rollback juntos
→ callback/redelivery se vuelve a consumir
→ provider devuelve VALID idempotente para el mismo committed grant
→ el mismo Order command vuelve a intentarse bajo M1.

No aparece una segunda Order ni otro grant.

### W5 — INVALID liberado provider, response retrasada

provider_rules invalida/release
→ response se retrasa
→ Operation conserva temporalmente claim local
→ puede denegar de más
→ response/redelivery llega
→ Order REJECTED + claim local release.

No existe ventana de autorización de más.

### W6 — local cancel después de provider VALID pero antes de command

provider grant queda egress-committed
→ antes de publicar command, Operation procesa una causa local que vuelve la Order no elegible
→ no publica
→ ejecuta release pre-egress explícito
→ provider libera
→ claim local libera.

El commit provider no obliga a emitir una Order que el lifecycle local ya canceló.

### W7 — OPEN pending + CLOSE + late ALLOW

OPEN(k)
→ pending request R1
→ CLOSE(k) en owner local
→ pending R1 eliminado
→ ALLOW(R1)
→ stale no-op
→ no Operation.

### W8 — OPEN pending + CLOSE_ALL + ALLOW redelivered N veces

CLOSE_ALL elimina la continuation.

Cada ALLOW(R1) posterior falla la misma identity guard.

No existe efecto acumulativo.

### W9 — OPEN pending + DENY + retry legítimo del mismo ciclo

OPEN signal S1(k)
→ request R1
→ DENY
→ pending clear, no materialization
→ OPEN distinto S2(k)
→ request R2
→ puede ser evaluado.

last_materialized_cycle_seq no avanza por R1.

### W10 — OPEN k pending + OPEN k+1

R1(k) pending
→ OPEN(k+1)
→ R1 superseded
→ R2(k+1) pasa a ser el único pending
→ ALLOW(R1) tarde = stale
→ ALLOW(R2) puede materializar sólo k+1.

Nunca coexisten dos pending admissions.

### W11 — account binding disabled mientras espera

R1 pending
→ config local deshabilita AccountStrategy
→ pending invalidado
→ ALLOW R1 tarde
→ stale no-op.

No se crea Operation con binding local inválido.

### W12 — provider RuleSet cambia mientras ALLOW viaja

AdmissionRequest R1 lineariza bajo v5
→ ALLOW v5
→ provider_rules procesa v6
→ Operation todavía puede materializar si la continuation local sigue válida
→ MM construye Order
→ reservation/grant
→ ReservationRevalidate obligatorio contra provider current
→ v6 decide final egress.

Stage-1 histórico no se confunde con final egress authority.

## 11. Invariants

### A3-I1 — Provider authority is traversed

Ningún grant no emitido cruza Core egress sin una ReservationRevalidate procesada por echo/provider_rules(account_id).

### A3-I2 — No local authority inference

Epoch/config/kache local puede servir para observabilidad/prefilter, jamás para decidir que la revalidación autoritativa puede omitirse.

### A3-I3 — Exact grant only

Revalidation nunca cambia qty, direction, Order/action identity ni cap scopes. VALID o INVALID sobre el grant original.

### A3-I4 — One final provider commit

Un grant puede alcanzar egress_committed una sola vez. Redelivery es idempotente por grant identity.

### A3-I5 — Post-commit updates are prospective

Una authority update posterior al egress commit no revoca retroactivamente ese grant. Puede afectar decisiones posteriores y safety normal.

### A3-I6 — Pre-egress INVALID has zero physical effect

INVALID implica que ningún command de esa Order/action fue publicado por M1. Reservation y claim local convergen a release.

### A3-I7 — Post-M1 no config revocation

Una vez command publication puede haber escapado de Core, capacity sólo converge por execution facts/finality ya congelados, no por una config revalidation tardía.

### A3-I8 — One pending admission per AccountStrategy

Antes de Operation existe como máximo un pending_admission activo en echo/operation.

### A3-I9 — Admission result by identity

AdmissionResult sólo puede afectar state si request_id coincide con la continuation activa.

### A3-I10 — Close dominates a still-pending open

Si CLOSE/CLOSE_ALL(k) fue serializada por el owner mientras OPEN(k) seguía pending, ningún ALLOW posterior de esa request puede materializar Operation(k).

### A3-I11 — New cycle supersedes old pending cycle

OPEN(k+1) no convive con pending admission k; reemplaza/supersede la continuación anterior.

### A3-I12 — No materialization bookkeeping lie

DENY o supersede pre-Operation no modifica last_materialized_cycle_seq. Sólo la creación real de Operation consume la identidad del ciclo.

### A3-I13 — No provider state duplicated in Operation

pending_admission no almacena una copia autoritativa de ProviderRuleSet/caps/risk. Provider provenance es evidencia, no authority local.

### A3-I14 — Recovery preserves continuation semantics

Request/result redelivery no crea segunda reservation, segunda Operation ni segundo command.

## 12. SPEC deltas requeridos

### D2-04 — Operation / Order / Fill / Position

Agregar explícitamente que el StateFun owner echo/operation puede mantener pending_admission aun cuando no exista domain Operation.

Definir que una management Signal para el mismo ciclo:

- permanece no-op/fail-visible si no existe Operation ni pending admission;
- si existe pending_admission, CLOSE/CLOSE_ALL invalidan esa continuación antes de ser no-op respecto de Operation.

Mantener max one Operation identity per AccountStrategy + strategy_cycle_seq y last_materialized_cycle_seq sin cambios.

Agregar consumo idempotente de provider callbacks por exact continuation identity.

### D2-05 — Instrument / Session / Provider

§14:

- declarar pending_admission como owner-local pre-materialization continuation;
- DENY limpia sin materializar;
- ALLOW sólo aplica si request_id sigue activo y guards locales siguen válidas;
- CLOSE/CLOSE_ALL y OPEN de ciclo siguiente pueden invalidar/supersederla;
- provider ALLOW conserva provenance de su own linearization point y no sustituye Stage-2 final authority.

§15:

reemplazar el egress guard:

“si epoch cambió → ReservationRevalidate”

por:

“todo grant no emitido → ReservationRevalidate obligatorio en provider_rules”.

Eliminar cualquier claim de que un snapshot local puede demostrar que la authority no cambió.

### D2-05C — Provider Program Rules

Reemplazar C-R3.6 en su parte condicional.

Nuevo contrato:

- grant exacto siempre atraviesa ReservationRevalidate antes de egress;
- provider owner decide bajo authority corriente;
- VALID marca egress_committed en live_reservation;
- INVALID retira/invalida reservation pre-egress;
- authority update posterior a egress_committed es prospectiva para ese grant;
- no local epoch detection como correctness condition.

Preservar sin cambios las familias/cap math de D4-A2 y el ProviderRuleSet completo read-only para MM.

### D2-07 — Execution Runtime

No cambia M1/M2.

Agregar sólo la aclaración de frontera:

- A3 provider revocation cutoff termina cuando el Order command queda committed/visible por M1;
- M2 physical point-of-no-return sigue perteneciendo al Bridge/Adapter.

No mover provider_rules al Bridge.

### D2-08 — Strategy Runtime

Extender §7:

- pending admission pre-Operation participa del lifecycle del mismo AccountStrategy;
- CLOSE/CLOSE_ALL del ciclo pendiente invalidan la continuation;
- OPEN(k+1) supersede pending k sin segunda Operation;
- deferred Signals del mismo ciclo pueden usar el buffer acotado ya congelado;
- no backlog arbitrario.

No cambiar Strategy ni hacerla account-aware.

### D2-09 — Blocking Refactors

No requiere componente/aggregate nuevo.

Sólo debe reflejar, al consolidar D4, que request_id/grant identity participan en dedup de continuations live y que el path provider requiere el commit final obligatorio. No cambia el boundary EXACT_REPLAY de ejecución.

### Architecture Candidate V1

§4 Lifecycle:

incluir pending_admission como state pre-Operation del mismo owner, no como status de Operation.

§7 Provider runtime:

cambiar “guard revalida epoch del grant” por “todo grant ejecuta final authoritative ReservationRevalidate; VALID committea egress sobre la reservation”.

§8 Execution runtime:

referenciar el cutoff M1 de A3 sin alterar M2.

## 13. Acceptance cases

| ID | Caso | Acceptance |
|---|---|---|
| A3-01 | grant v5, provider procesa v6, Operation local sigue v5 | Revalidate obligatorio observa v6; ningún branch local permite skip |
| A3-02 | no provider update | Igual existe exactamente un final ReservationRevalidate; VALID committea egress |
| A3-03 | provider update después de VALID commit | Update no revoca retroactivamente el grant; gobierna decisiones posteriores |
| A3-04 | INVALID | Cero command M1; provider reservation y claim local convergen a release |
| A3-05 | duplicate ReservationRevalidate | Mismo grant produce mismo outcome; no duplica reservation/commit |
| A3-06 | crash Operation antes de M1 checkpoint | Recovery puede reconsumir VALID y producir un solo command lógico |
| A3-07 | local cancel después de VALID antes de M1 | Cero command; release pre-egress explícito y seguro |
| A3-08 | OPEN pending → ALLOW | Una Operation como máximo; pending clear |
| A3-09 | OPEN pending → DENY | Cero Operation; ciclo no se marca materializado |
| A3-10 | OPEN pending → CLOSE → ALLOW | ALLOW stale; cero Operation |
| A3-11 | OPEN pending → CLOSE_ALL → ALLOW | ALLOW stale; cero Operation |
| A3-12 | OPEN k pending → OPEN k+1 → old result | k superseded; old result no materializa; sólo un pending |
| A3-13 | binding disabled mientras pending | old ALLOW no materializa |
| A3-14 | request/result redelivery | no segunda admission, Operation ni side effect |
| A3-15 | RuleSet cambia después de Stage-1 ALLOW | Stage-1 puede conservar su historical decision; final egress authority usa estado actual |
| A3-16 | same-cycle Signals mientras pending | orden preservado por buffer acotado; CLOSE/CLOSE_ALL invalidan inmediatamente |
| A3-17 | Position mismatch/provider trust invalid | final revalidation puede INVALID según provider authority; Operation no recalcula Position/exposure |

## 14. Cross-workstream constraints

### D4-A1

A3 no toca market identity ni EXACT_REPLAY.

No usa stream_seq como identity.

No introduce DecisionObservation ni otra entidad *Observation.

El patrón que sí comparte con A1 es conceptual: ordering e identity son cosas distintas. Aquí request_id/grant_id identifican la continuation; el owner queue define ordering.

### D4-A2

A3 consume literalmente:

- exact grant per Order/action;
- signed executable quantity;
- reservation-before-GRANTED;
- reservation completeness para las families V1 soportadas;
- local direction claim exclusivo de Operation;
- cap authority exclusiva de provider_rules;
- no silent resize;
- INVALID pre-egress sin side effect;
- post-egress Fill/finality venue-authoritative.

A3 no reabre q_exec_max ni las fórmulas de envelope.

### MoneyManagement / ProviderRuleSet

ProviderRuleSet efectivo completo permanece read-only en el contexto account-specific/MM.

MM decide cuánto/cómo operar.

provider_rules decide si esa decisión satisface la authority externa account-wide en sus linearization points.

No existe provider-rules-for-sizing subset.

### Strategy

Strategy base permanece account-agnostic.

pending_admission es exclusivamente una preocupación de la materialización por AccountStrategy.

### Execution

No cambia Order identity, client_order_id, journal M2 ni finality.

No mueve side-effect authority al Core/provider_rules.

## 15. KISS / YAGNI sweep

### Conceptos que sí sobreviven

1. pending_admission: necesario porque sin state pre-Operation CLOSE/CLOSE_ALL puede perderse frente al callback.
2. reservation egress commit marker: necesario porque sin él un VALID final no tiene un punto finito después del cual updates posteriores sean prospectivas.

Ambos viven en owners ya existentes.

### Conceptos rechazados

- generic Continuation entity;
- workflow engine;
- saga;
- distributed transaction;
- global coordinator;
- provider policy cache autoritativo en Operation;
- lease/TTL de grant;
- generic queue de pending cycles;
- multiple concurrent Stage-1 admissions por AccountStrategy;
- max_admissible_qty;
- silent resize;
- HARD_CAP_WINS;
- WIND_DOWN;
- generic liquidation override;
- revalidation post-M1 por config;
- nueva entity para audit de callback;
- nuevo topic sólo para “continuations”.

### Por qué no hay lease

Un lease agregaría clock, expiry, renewal y otra carrera.

V1 no lo necesita: la reservation ya conserva capacity y el egress commit es one-shot. Si una implementación futura demuestra que un Operation owner puede quedar vivo indefinidamente después del VALID sin poder completar M1, se puede agregar una política de liveness posteriormente. No se diseña hoy.

### Por qué no se cancela Stage-1 en provider_rules

Admission Stage-1 no reserva capacity ni posee un recurso que deba liberarse.

Cuando CLOSE invalida pending_admission, alcanza con que el lifecycle owner olvide la continuation. Un result tardío queda stale por request_id. Agregar AdmissionCancel sería protocolo sin beneficio de correctness V1.

## 16. Owner decisions

No se identifica una decisión Owner necesaria.

Las decisiones son técnicas y quedan dentro de authorities ya congeladas:

- provider_rules es authority account-keyed;
- Operation es lifecycle owner account-strategy;
- no silent resize;
- fail-closed antes de egress;
- un ciclo futuro acotado;
- Stage-1 DENY no consume materialización;
- M1/M2 permanecen separados.

El naming físico final de campos/messages y la representación concreta del small buffer corresponden a Technical SPEC/implementación, no a Owner.

D3-04: CANDIDATE_RESOLVED
D3-06: CANDIDATE_RESOLVED

OWNER_DECISIONS_REQUIRED:
NONE

NEW_V1_CONCEPTS:
- pending_admission: slot nullable pre-Operation dentro de echo/operation; no entidad ni aggregate nuevo
- reservation egress commit: marker one-shot dentro de live_reservation, producido por ReservationRevalidate obligatorio

DEFERRED_YAGNI:
- generic async workflow / saga / continuation framework
- múltiples pending admissions o queue arbitraria de ciclos
- lease/TTL/renewal del egress commit sin evidencia de necesidad
- provider-specific no-safe-unwind/liquidation edge cases ya diferidos por D4-A2

READY_FOR_MANAGER_QA: YES
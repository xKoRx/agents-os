# Echo Futures — D6 C1-R1 Physical Order Semantics + Entitlement Repair

**Shot:** D6 C1-R1 — TOP Execution Semantics / Architecture Repair Specialist (one-shot, fresh context)
**Date:** 2026-10-01
**Project:** [[Echo Futures]]
**Echo frozen baseline:** `xKoRx/echo@13e087a3bb762f65b060d3b3200fb00a67c6ff1d` (D5 Shot 3; verificada en clone local `~/aranea/work/d5-foundations-20260929/echo`)
**Prior artifacts:** C0 (`./C0-NINJATRADER-PHYSICAL-TRANSPORT-CERTIFICATION.md`), C1 (`./C1-NINJATRADER-ADAPTER-FIT-ANALYSIS.md` — AddOn seam y todo lo no cuestionado se REUTILIZA; su veredicto `PASS` quedó `NOT ACCEPTED` por Manager QA con dos findings, que son el único alcance de este repair)
**Trigger:** `D6_C1_MANAGER_QA = REPAIR_REQUIRED` (project note 2026-09-30): F1 protective-order physical semantics + F2 transport entitlement gate
**Verdict:** `D6_C1_R1 = PASS` — ambos findings tienen corrección mínima demostrada. F1 es una **corrección aditiva acotada del contrato D5** (nueva primitiva `STOP_MARKET`; el adapter NO puede resolverla sin mentir sobre `Order.Type`). F2 es una **segunda corrección aditiva acotada** (dimensión explícita de aceptación de riesgo owner; `UNKNOWN` jamás se reclasifica como grant del firm). Ninguna altera Strategy, Signals, ownership de Operation, economics de GerardMM, ProviderRuleSet, recovery, EXACT_REPLAY ni la topología del Futures Bridge.

## 0. Alcance, hard safety y convención de evidencia

No se implementó código, no se enviaron órdenes (`ORDERS_SENT = 0`), no se tocó product code D5/D6. Toda cita Echo usa la forma `xKoRx/echo@13e087a3:<path>:<líneas>` y fue leída directamente del baseline. Toda cita NinjaTrader es documentación oficial NT8. El resto del análisis C1 (AddOn fit, account discovery, market data, recovery, warm-up, M1/M2, runtime placement) queda REUTILIZADO tal cual por mandato /reuse.

---

## F1 — Protective order: semántica física

### FINDING

La orden protectora de GerardMM se modela como `LIMIT` al nivel de stop. Físicamente eso no es un stop-loss: en cualquier venue real es una **marketable limit** que ejecuta inmediatamente, cerrando la posición en el momento de instalar la protección en vez de descansar hasta que el precio deteriore. La conclusión C1 de que "STOP no es necesario y MARKET/LIMIT mapean 1:1" es refutada.

### CURRENT_BEHAVIOR

- `gerardmm.go:561-584` (`protectiveOrder`): emite `OrderRequest{Role: OrderRoleProtective, Side: opuesto a la dirección, Type: OrderTypeLimit, LimitPrice: &nivel_de_stop}`.
- `gerardmm.go:417-531` (`reconcileProtection`): calcula `desired` (piso técnico S0 + componente monetario del budget + break-even post-piramidal; la fórmula del nivel NO se toca en este repair). Sólo si el mark NO está cruzado instala/aprieta la orden; el tighten es cancel+replace monotónico (`gerardmm.go:505-525`).
- `gerardmm.go:494-503` + `:533-560`: si el mark ya cruzó el nivel al momento de la decisión (`PROTECTIVE_STOP_CROSSED`), cancela la protectora y manda MARKET de salida.
- El motor MM es one-shot por ciclo: entre ciclos la protección es exclusivamente la orden descansando en el venue.
- El contrato `ExecutionAdapter` sólo acepta MARKET/LIMIT: `core/capabilities/adapter.go:90-97` (switch con default error), y `Order.Validate` del dominio rechaza cualquier otro tipo (`domain/operation.go:94-101`); igual el switch Core-side en `operation/engine.go:1002-1010`.

### PHYSICAL_REALITY

- Un LIMIT descansa sólo si su precio está del lado NO ejecutable del mercado. Un SELL LIMIT con precio ≤ mejor bid es marketable: llena inmediatamente al bid. Un BUY LIMIT con precio ≥ mejor ask es marketable: llena inmediatamente al ask. Esto es mecánica estándar de exchange y NT la comparte: un limit "ensure[s] you get filled at the price you specified **or better**" — para un vendedor, cualquier fill al bid ≥ limit es "mejor", hence ejecución inmediata ([Order Types – NinjaTrader 8](https://static.ninjatrader.com/support/helpGuides/nt8/order_types.htm)).
- Un STOP_MARKET es la primitiva con la semántica requerida: "These orders **wait** for the price of the instrument to pass your stop price. Once it passes the stop price the order becomes a market order for execution" ([Order Types – NinjaTrader 8](https://static.ninjatrader.com/support/helpGuides/nt8/order_types.htm)). Descansa en el venue hasta el trigger.
- NT distingue además las **simulated stop orders**, "conditional **locally held** (PC simulated)" orders, "held and simulated locally on your PC and are therefore subject to issues such as **loss of internet connection and computer crashes**" ([Simulated Stop Orders](https://static.ninjatrader.com/support/helpguides/nt8/simulated_stop_orders.htm)). La protección venue-side requiere stop nativo (provider/exchange-held), no simulado en el PC.

### CONTRADICTION

Para una posición LONG el nivel de stop está estrictamente debajo del mark (el crossed-check garantiza `mark > desired` al instalar). Un SELL LIMIT a ese precio llega al venue **marketable** y cierra la posición inmediatamente al bid — exactamente lo contrario del propósito congelado (descansar hasta deterioro). Para SHORT, el BUY LIMIT por encima del ask cierra inmediatamente al ask. Además, como el motor MM evalúa por ciclos discretos, entre ciclos la única protección posible es una orden venue-side; una LIMIT marketable no protege nada porque no descansa. La propia implementación D5 delata la intención congelada: los comentarios dicen "no invalid **STOP** is published behind the market (D4-B2 §10)" (`gerardmm.go:419-421`), "exactly one logical protective **STOP** per D4-B2 §18" (`gerardmm.go:968-971`), y la función se llama `reconcileProtection`/emite "protective stop". El D4-B2 congelado siempre habló de STOP; el enum D5 (sólo MARKET/LIMIT) forzó el colapso a LIMIT. Por último, el defecto es estructuralmente invisible para la suite D5: el venue SIM no modela matching por precio — los fills son guion inyectado (`SubmitStep.Outcome ∈ {NoAnswer, Reject, FullFill, Partial, AcceptWork, Ambiguous}`, `adapters/sim/venue.go:176-230`) y `SubmitAcceptWork` acepta cualquier orden como descansada sin chequear marketability; por eso ATP 113/0/0/2 pasó con esta forma.

### MINIMUM_CORRECTION

Corrección aditiva del contrato D5: introducir la primitiva física que falta y hacer que GerardMM la emita. El cálculo del nivel, la monotonicidad del tighten y el camino crossed→MARKET quedan intactos.

1. `domain/operation.go`: agregar `OrderTypeStopMarket OrderType = "STOP_MARKET"` al enum (`:40-43`) y `StopPrice *units.Price` al struct `Order` (con `json:"stop_price,omitempty"`). `Order.Validate`: caso `STOP_MARKET` exige `StopPrice != nil` (y `LimitPrice == nil`); LIMIT y MARKET sin cambios; default sigue rechazando.
2. `operation/mm.go` (`OrderRequest`, `:232-241`): agregar `StopPrice *units.Price`.
3. `operation/engine.go` (`:1002-1010`): caso `STOP_MARKET` exige `StopPrice` no nula (misma forma que LIMIT/LimitPrice).
4. `operation/wire.go` (`SubmitOrderIntent`, `:139-142`): agregar `StopPrice *units.Price json:"stop_price,omitempty"`.
5. `core/internal/futuresruntime/runtime.go` (`BridgeCommandEnvelope`, `:263-330`): proyectar `stop_price` field-by-field (la proyección es explícita campo a campo; sin el campo el egress pierde el precio de trigger).
6. `futures-bridge/core/capabilities/adapter.go`: `SubmitSpec.StopPrice` + caso `STOP_MARKET` en el switch `:90-97`. `CapabilityDeclaration.SupportedOrderTypes` se extiende por adapter (SIM hoy `sim_adapter.go:97`; el adapter NT declarará STOP_MARKET sólo tras certificar soporte nativo).
7. `futures-bridge/adapters/journalfs/journal.go`: `Terms.StopPrice` + inclusión en `sameIntent` (`:232-242`, mismo patrón nil-safe de `priceEqual`) para que el dedup de intent idéntico distinga stops con distinto nivel.
8. `gerardmm.go`: `protectiveOrder` emite `Type: OrderTypeStopMarket, StopPrice: &p` (decision_id, rol, side, qty, nivel: sin cambios); el tighten de `reconcileProtection` compara `desired` contra `protective.StopPrice` (`:505-511`). El camino `PROTECTIVE_STOP_CROSSED`→MARKET queda EXACTAMENTE igual (sigue siendo correcto: no se publica un stop detrás del mercado; un stop market detrás del mercado dispararía instantáneo — se manda MARKET directo).
9. `futures-bridge/adapters/sim`: `SupportedOrderTypes` += STOP_MARKET; el venue almacena el tipo (ya lo hace, `venue.go:38,219,452`) y los fills siguen siendo guion — con el enum correcto la forma deja de mentir y el escenario existente no cambia de semántica.
10. Adapter NT (trabajo D6-N2 ya clasificado SMALL_D6_ADAPTER_WORK): `STOP_MARKET` → `OrderType.StopMarket` vía `Account.CreateOrder` con stop price; el adapter declara `STOP_MARKET` en capabilities **sólo si** el soporte de stop en la cuenta es NATIVO (venue-held).

Alternativas evaluadas y rechazadas:

- **STOP_LIMIT:** tras el trigger descansa un limit; en mercado rápido puede no llenar = ventana sin protección en el camino de max-loss. El protective de GerardMM es una cota de pérdida (garantía de salida) con slippage acotado por mercado, no un precio objetivo. STOP_MARKET es la primitiva correcta.
- **MIT:** trigger por touch en la dirección FAVORABLE — primitiva de toma de ganancia, no de protección. Incorrecta.
- **Trigger client-side (AddOn vigila precio y dispara MARKET):** la protección muere con NT/bridge/Echo o con la conexión; no es equivalente a una orden venue-side (el propio manual NT lo documenta para simulated stops). Rechazado por crash/disconnect safety.
- **Transformación LIMIT→STOP dentro del adapter:** obliga a mentir sobre `Order.Type` (Echo creería haber enviado un LIMIT que físicamente es un stop), le daría al adapter autoridad de decisión de trading (contradice el frozen D2-07 §5 "Bridge sin autoridad de dominio"), y rompería reconcile-by-terms por diseño (el venue sostendría un stop mientras el journal pinnea un LIMIT). Rechazado.

### FILES/CONTRACTS_AFFECTED

`domain/operation.go`, `operation/mm.go`, `operation/engine.go`, `operation/wire.go`, `core/internal/futuresruntime/runtime.go`, `futures-bridge/core/capabilities/adapter.go`, `futures-bridge/adapters/journalfs/journal.go`, `futures-bridge/adapters/sim/sim_adapter.go` (+venue passthrough), `sdk/futures/gerardmm/gerardmm.go`, y en D6 el adapter NT + su `CapabilityDeclaration`. Sin cambios en: claims/q_exec_max, Fill identity/dedup, reservations, admission, EXACTLY_ONCE egress, projectors, EXACT_REPLAY, readiness/barrier.

### D5_FREEZE_IMPACT

**YES** — corrección acotada demostrada, del tipo que /improve autoriza: el freeze no puede obligar al sistema a enviar una orden físicamente incorrecta. Es aditiva (+1 valor de enum, +1 campo price en 6 superficies, +1 rama de validación en 3 switches) y **realinea la implementación con el intent congelado D4-B2 §10/§18**, que siempre habló de protective STOP; la omisión del enum fue la desviación, no este repair. Los comentarios del código D5 ya usan la palabra STOP — el repair elimina la contradicción código-vs-contrato en vez de crearla.

### N1_IMPACT

Ninguno en runtime: N1 es read-only y no envía órdenes. La corrección puede viajar en la misma slice o en la de N2; no bloquea N1.

### N2_IMPACT

Precondición obligatoria de N2 (ejecución): sin esto, N2 codificaría el contrato protector equivocado (mandato explícito del Manager QA). Gate de certificación nuevo que se agrega a la lista D6: **soporte de stop NATIVO en la cuenta Tradovate/GAU50** — `Account.IsOrderTypeSupported(StopMarket)` + prueba física de venue-held (la orden stop sigue visible en `Account.Orders` tras restart de NT; una stop simulada local no resucitaría). Si el soporte nativo no se demuestra, el camino protector queda fail-closed para ese transport (`UNSUPPORTED_FOR_V1_EXACT_SUBMISSION`, misma clase que los gates de identidad ya definidos).

### OWNER_DECISION_REQUIRED

Ninguno para esta corrección: es verdad física del contrato, no riesgo de negocio. La aceptación del gate de certificación de stop nativo es manager-level, no owner.

### /verify F1 — demostración

- Source Echo exacto: `protectiveOrder` emite LIMIT al nivel de stop (`xKoRx/echo@13e087a3:v3/sdk/futures/gerardmm/gerardmm.go:561-584`, LIMIT en `:575`); instalación sólo cuando `mark` no cruzó (`:494-531`), es decir, siempre con el precio del limit del lado marketable del libro.
- Comportamiento normal NT: LIMIT llena "at the price you specified or better" (marketable si el precio está detrás del mercado); STOP_MARKET "wait[s] for the price... to pass your stop price. Once it passes... becomes a market order" ([Order Types](https://static.ninjatrader.com/support/helpGuides/nt8/order_types.htm)).
- Consecuencia LONG: posición LONG, protective = SELL LIMIT con precio < mark ⇒ al llegar al venue ejecuta inmediatamente al bid ⇒ la "instalación de protección" ES el cierre de la posición, en el peor nivel previsto, sin haber descansado nunca. Con SELL STOP_MARKET: descansa en el venue; dispara sólo cuando el trade pasa el stop ⇒ salida garantizada venue-side con slippage posible.
- Consecuencia SHORT: BUY LIMIT con precio > ask ⇒ ejecuta inmediatamente al ask ⇒ mismo cierre instantáneo. BUY STOP_MARKET descansa y dispara al pasar el stop.
- Sim: `SubmitAcceptWork` descansa cualquier orden sin marketability (`adapters/sim/venue.go:198-230`) ⇒ ningún test D5 podía observar el defecto (coincide con el QA del Manager).

---

## F2 — Entitlement UNKNOWN vs fail-closed del binding

### FINDING

`ProviderAccountBinding.Validate()` impide habilitar un binding con `Transport.Entitlement = UNKNOWN`. La autorización pública de Earn2Trade para algoritmo propio sigue UNKNOWN; el Owner decidió continuar asumiendo ese riesgo pero prohibió falsear evidencia externa. El contrato congelado no tiene hoy ningún estado veraz para "operar bajo riesgo aceptado con entitlement no confirmado": o se miente (ALLOWED/CONDITIONAL) o no se opera.

### CURRENT_BEHAVIOR

- Significado congelado exacto (comentario de dominio, D2-05C §7): `TransportEntitlement` es "the automation entitlement **the firm grants** for a program/phase"; "`UNKNOWN` is never interpreted as allowed" (`domain/provider.go:280-288`). Valores: ALLOWED / CONDITIONAL / FORBIDDEN / UNKNOWN. Es un hecho de política del PROVIDER, no una decisión de Echo de operar.
- Gate exacto `ProviderAccountBinding.Validate()` (`domain/provider.go:322-338`): binding `Enabled` exige entitlement ∈ {ALLOWED, CONDITIONAL}; `UNKNOWN`/`FORBIDDEN` ⇒ error `"cannot be enabled with %s automation entitlement"`.
- El mismo predicado vive duplicado en dos superficies más: `session.staticEligible()` (`futures-bridge/internal/session/session.go:521-536`, alimenta `StaticEligible` en `:494` y de ahí la conjunción de readiness) y **admission en dos switches** (`sdk/futures/provider/admission.go:125-133` y `:227-233` ⇒ `DenyReasonEntitlementRevoked`, denegando la apertura de nuevas operaciones).
- El loader ETCD `loadBinding` (`futures-bridge/cmd/futures-bridge/main.go:227-252`) NO carga `TransportSpec.Conditions` y el default del key ausente es `ALLOWED` (comportamiento SIM/dev preexistente; para la cuenta Earn2Trade el config debe fijar UNKNOWN explícitamente — disciplina de config, nota operacional).

### PHYSICAL_REALITY

Earn2Trade no ha confirmado ni denegado la automatización (preflight `BLOCKED_PENDING_PROVIDER_CONFIRMATION`, no reabierto por mandato). El owner ya decidió: continuar asumiendo el riesgo, sin fabricar confirmación. Físicamente hoy: el binding con UNKNOWN ni siquiera carga (Validate en `main.go:250`) ⇒ no hay sesión de bridge, no hay N1, no hay N2 para esa cuenta.

### CONTRADICTION

El owner quiere operar bajo riesgo aceptado; el contrato sólo represente estados de GRANT del firm. Poner `ALLOWED` o `CONDITIONAL` en config pasaría los tres gates **sin cambio de código**, pero falsearía la semántica: afirmaría un grant del firm que no está evidenciado — exactamente lo que el owner prohibió y lo que el Manager QA señal ("does not automatically satisfy the frozen D5 binding invariant"). Y `UNKNOWN` habilitado por decreto del owner es hoy ilegal bajo el contrato congelado.

### MINIMUM_CORRECTION

Segunda corrección aditiva acotada: dar al contrato la dimensión que falta — la decisión del Owner como dato explícito y auditable, separada del grant del firm.

1. `domain/provider.go`: agregar a `TransportSpec` el campo `OwnerRiskAccepted *OwnerRiskAcceptance` con `type OwnerRiskAcceptance struct { DecisionRef string; DecidedAt time.Time }` (`DecisionRef` = referencia a la decisión owner registrada en el project note; `DecidedAt` = fecha). NO se agrega ningún valor al enum `TransportEntitlement`: el entitlement sigue siendo UNKNOWN (verdad sobre el firm), y la aceptación es un hecho distinto (decisión local) con su propio campo. El invariante congelado "UNKNOWN is never interpreted as allowed" permanece literalmente verdadero.
2. Predicado único compartido (p. ej. `func (t TransportSpec) AutomationAuthorized() bool`): `ALLOWED|CONDITIONAL` ⇒ true; `UNKNOWN` ⇒ true **sólo si** `OwnerRiskAccepted != nil` (y `DecisionRef` no vacío); `FORBIDDEN` ⇒ **siempre false** (una prohibición conocida del firm jamás se invalida por decisión owner — frontera dura, no negociable). Reemplazar los tres switches duplicados (`provider.go:330-336`, `session.go:527-532`, `admission.go:126-132` y `:228-233`) por el predicado.
3. `ProviderAccountBinding.Validate()`: `Enabled` exige `AutomationAuthorized()`; cuando la habilitación descansa en UNKNOWN+aceptación, exigir `DecisionRef` no vacío (procedencia obligatoria, alineada con el patrón `RuleSourceRef` de los RuleSets).
4. `loadBinding` (main.go): leer el flag desde ETCD (p. ej. `binding/owner-risk-accepted-ref` + `binding/owner-risk-accepted-at`); opcionalmente empezar a cargar `conditions` (hoy se pierde).
5. Observabilidad obligatoria: readiness/session Status expone la degradación `ENTITLEMENT_UNCONFIRMED_OWNER_ACCEPTED` (detalle no bloqueante) mientras el entitlement siga UNKNOWN. El estado no confirmado nunca desaparece de la superficie: no es un green silencioso.

Rechazadas:

- **Config-only CONDITIONAL/ALLOWED:** cero código, pero falsifica — afirma un grant del firm sin evidencia. Prohibida por el owner y por este repair.
- **Nuevo valor de enum `UNKNOWN_OWNER_ACCEPTED`:** veraz pero mezcla dos planos (grant del firm vs decisión local) dentro del enum del firm; obliga a tocar los mismos switches y ensucia toda comparación de grants. La variante del campo separado es igual de pequeña y más limpia.
- **Modo sin binding / bypass para N1:** inventaría un segundo camino de ejecución para esquivar el invariante — peor que el mecanismo veraz.
- **Aplicar el mecanismo a FORBIDDEN:** jamás. FORBIDDEN es evidencia negativa del firm; sólo la evidencia externa puede revertirla.

### FILES/CONTRACTS_AFFECTED

`domain/provider.go` (struct + predicado + Validate), `sdk/futures/provider/admission.go` (2 switches), `futures-bridge/internal/session/session.go` (`staticEligible`), `futures-bridge/cmd/futures-bridge/main.go` (loader), surface de readiness/Status (detalle de degradación). Sin cambios en: reglas de admission restantes (RuleSet authority, instrumentos, ventanas), claims, exits/protective (que nunca pasaron por admission — el entitlement es gate de NEW RISK por construcción congelada; los caminos de salida/ForceClose no se tocan ni se tocan ahora), M1/M2, recovery.

### D5_FREEZE_IMPACT

**YES** — aditiva y acotada. El invariante congelado se preserva en su verdad: UNKNOWN no se interpreta como allowed (no lo es); se habilita bajo un acto explícito, registrado y auditable del Owner, representado en un campo propio. Manager QA lo pidió literalmente: el riesgo owner "must be explicitly adjudicated" — este es el mecanismo de adjudicación.

### N1_IMPACT

Hoy F2 bloquea N1 (el binding no carga). Con el mecanismo implementado + la aceptación registrada en config, **N1 read-only procede sin confirmación externa**: el entitlement es gate de egress/admisión de nuevo riesgo, y N1 no envía órdenes. La implementación del mecanismo es micro-slice y puede viajar dentro de N1.

### N2_IMPACT

Con el mecanismo + aceptación registrada, N2 no queda bloqueado por la confirmación externa (decisión owner vigente), PERO antes del primer submit físico deben estar resueltos: (1) la corrección F1 (STOP_MARKET) implementada; (2) el gate de stop nativo certificado en la cuenta; (3) la aceptación owner registrada con `DecisionRef` y el re-affirm explícito de que cubre egress físico (ver OWNER_DECISIONS). La confirmación externa de Earn2Trade sigue UNKNOWN y se mantiene visible; si llega, el config migra a ALLOWED/CONDITIONAL con procedencia (claim/URL/fecha, estilo RuleSourceRef).

### OWNER_DECISION_REQUIRED

1. Registrar formalmente la aceptación de riesgo en el config del binding (ETCD) con referencia a la decisión owner del 2026-09-30 — el owner YA decidió asumir el riesgo; lo que falta es el registro en el formato que el contrato corregido exige (acto de config, no de código).
2. Confirmar en el despacho de N2 que la aceptación registrada cubre **egress físico** (o, si prefiere, acotarla a read-only hasta confirmación externa — decisión owner en ese momento).
3. Frontera FORBIDDEN: sin decisión (queda fail-closed por contrato).

### /verify F2 — demostración del gate exacto

`xKoRx/echo@13e087a3:v3/sdk/futures/domain/provider.go:329-336`: `if b.Enabled { switch b.Transport.Entitlement { case EntitlementAllowed, EntitlementConditional: case EntitlementForbidden, EntitlementUnknown: return fmt.Errorf("domain: binding for account %s cannot be enabled with %s automation entitlement", ...) } }`. Consumo real de ese predicado en `session.go:521-536` (readiness/egress) y `admission.go:125-133, 227-233` (denial de apertura). No es un check nominal: sin binding válido no hay proceso, y sin admission no hay operaciones nuevas. La solución CONDITIONAL-sin-evidencia pasaría hoy por mera config — se rechaza como falsificación, no como imposibilidad técnica.

---

## Clasificación de delta consolidada (sobre el handoff C1)

- `REUSE_AS_IS`: todo el C1 no cuestionado (AddOn seam, identidad de cuenta, market data, M1/M2, recovery/barrier, warm-up wiring, topología bridge, Strategy/Signals/Operation ownership/economics/ProviderRuleSet/M1/M2/recovery/EXACT_REPLAY).
- `D5_CONTRACT_CORRECTION (aditiva, demostrada)`: F1 STOP_MARKET (enum + campo precio en 6 superficies + 3 switches de validación + emisión GerardMM) y F2 OwnerRiskAccepted (campo + predicado + 3 consumidores + loader + observabilidad). Ambas son pequeñas, independientes entre sí, y no reabren arquitectura.
- `SMALL_D6_ADAPTER_WORK` (actualizado): el adapter NT mapea además STOP_MARKET→`OrderType.StopMarket` (reflexión C1: el valor existe en el binario 8.1.8.3).
- `D6_CERTIFICATION_ONLY` (un gate nuevo): stop NATIVO venue-held en la cuenta GAU50 (`IsOrderTypeSupported` + visibilidad post-restart); se suma a los gates ya listados por C1.
- Sin `MATERIAL_CONTRADICTION` residual: con ambas correcciones especificadas, no queda ninguna conclusión C1 falsa; lo que queda es implementación acotada.

Secuenciación recomendada al Manager: (1) micro-slice de implementación C1-R1 (ambas correcciones + regresiones verdes; puede dividirse: F2 dentro de N1, F1 completa dentro de N2 — pero F1 debe aterrizar completa, dominio→bridge→sim→GerardMM, en una sola pieza coherente); (2) owner registra aceptación ETCD ⇒ despachar **D6-N1** (scope del C1 sin cambios); (3) **D6-N2** tras F1 + certificación de stop nativo + re-affirm owner de egress. No emitir `EF_D6_E2E_PASS` desde este repair.

---

## Handoff

```text
D6_C1_R1 = PASS

PROTECTIVE_ORDER:
CURRENT: GerardMM emite OrderRoleProtective como LIMIT al nivel de stop (gerardmm.go:561-584); para LONG es un SELL LIMIT bajo el mercado y para SHORT un BUY LIMIT sobre el mercado — marketable limits que cierran la posición al instalar la protección en vez de descansar como stop venue-side; invisible para la suite porque el venue SIM llena por guion sin marketability.
CORRECT_PHYSICAL_FORM: STOP_MARKET venue-side (resting hasta trigger, luego market; garantía de salida = propósito max-loss congelado D4-B2 §10/§18, que siempre habló de STOP). STOP_LIMIT, MIT, trigger client-side y transformación en adapter: evaluados y rechazados (gap de llenado, primitiva equivocada, no crash-safe, mentiría Order.Type y daría autoridad de dominio al bridge).
MINIMUM_CHANGE: aditiva — OrderTypeStopMarket + StopPrice en Order/OrderRequest/SubmitOrderIntent/SubmitSpec/Terms(+sameIntent), +3 switches de validación, proyección stop_price en BridgeCommandEnvelope, GerardMM protectiveOrder → STOP_MARKET (nivel/monotonicidad/crossed→MARKET intactos), sim declara el tipo.
D5_CONTRACT_CHANGE: YES (corrección acotada demostrada; realinea implementación con el intent congelado; sin cambio en economics/claims/fills/M1/EXACT_REPLAY)

ENTITLEMENT:
CURRENT: TransportEntitlement = grant de automatización del FIRM (D2-05C §7); ProviderAccountBinding.Validate() (provider.go:322-338) prohíbe Enabled con UNKNOWN/FORBIDDEN; mismo predicado en session.staticEligible (session.go:521-536) y admission (admission.go:125-133, 227-233 → ENTITLEMENT_REVOKED); el binding Earn2Trade con UNKNOWN no carga hoy ⇒ sin sesión, sin N1, sin N2.
OWNER_RISK_COMPATIBLE_WITH_CURRENT_CONTRACT: NO (el contrato actual no tiene estado veraz para operar bajo riesgo aceptado; ALLOWED/CONDITIONAL por config pasaría los gates pero falsificaría un grant del firm sin evidencia — prohibido)
MINIMUM_CHANGE: TransportSpec.OwnerRiskAccepted{DecisionRef,DecidedAt} (decisión owner explícita y auditable, separada del grant del firm; UNKNOWN jamás se reclasifica) + predicado único AutomationAuthorized() (ALLOWED|CONDITIONAL ⇒ true; UNKNOWN ⇒ true sólo con aceptación registrada con ref; FORBIDDEN ⇒ siempre false, sin excepción) en los 3 consumidores + loader ETCD + degradación visible ENTITLEMENT_UNCONFIRMED_OWNER_ACCEPTED en readiness/Status.
BLOCKS_N1: YES hoy (el binding no carga); NO una vez implementado el mecanismo + aceptación registrada en config (read-only no envía órdenes; entitlement es gate de new-risk, no de observación)
BLOCKS_N2: YES hoy; NO tras mecanismo + F1 + certificación de stop nativo + re-affirm owner de egress; la confirmación externa Earn2Trade sigue UNKNOWN y permanece visible (no es precondición según decisión owner vigente)

C1_FINAL_STATUS:
PASS (con C1-R1 incorporado: las dos conclusiones materiales corregidas; todo lo demás del C1 se reutiliza tal cual)

N1_AUTHORIZABLE:
YES — condicionado a: micro-slice de implementación del mecanismo F2 (o incluida en N1) + registro owner de la aceptación en ETCD binding config (acto de config owner, no código). F1 no afecta el runtime read-only de N1.

N2_AUTHORIZABLE:
YES — condicionado a: corrección F1 implementada completa (dominio→engine→wire→bridge→sim→GerardMM en una pieza), gate de stop NATIVO venue-held certificado en la cuenta GAU50 (IsOrderTypeSupported + visibilidad post-restart), y re-affirm owner explícito de que la aceptación registrada cubre egress físico. Los gates C1 previos (ExecutionId/Name retention, horizon, etc.) siguen vigentes.

OWNER_DECISIONS_REQUIRED:
1) Registrar la aceptación de riesgo en el binding ETCD con DecisionRef de la decisión owner 2026-09-30 (formaliza lo ya decidido; FORBIDDEN queda fail-closed por contrato, sin decisión). 2) En el despacho de N2, confirmar que la aceptación cubre egress físico o acotarla a read-only hasta confirmación externa. 3) Disciplina de config: la cuenta Earn2Trade fija entitlement=UNKNOWN explícito (el default del loader ausente es ALLOWED, comportamiento SIM/dev preexistente).

NEXT_MANAGER_ACTION:
Aceptar este C1-R1 y despachar la implementación acotada: (a) micro-slice F2 + registro ETCD owner → autorizar D6-N1 read-only con scope del C1 sin cambios; (b) F1 como precondición de D6-N2 junto con el nuevo gate de certificación de stop nativo; mantener PROJECTX/Rithmic/CQG intactos. No emitir EF_D6_E2E_PASS desde este repair.
```

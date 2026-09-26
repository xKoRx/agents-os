# ECHO FUTURES — D1 / FRONT D

# EXECUTION TRANSPORT FEASIBILITY — MULTI-PROP EVIDENCE

/goal

Actúa como Principal Execution Infrastructure Researcher, Futures API Integration Architect y auditor adversarial de feasibility.

Trabajas para Echo Futures D1.

Front C ya está cerrado para D1.

Existe una cohorte factual suficiente de ProviderPrograms compatibles o condicionalmente compatibles con automatización. Tu misión NO es volver a investigar prop firms ni diseñar el Core final.

Tu misión es determinar qué TRANSPORTES REALES puede usar Echo para ejecutar Futures a través de esa cohorte, qué capabilities ofrece cada transport, qué entitlement real existe por ProviderProgram y qué gaps debe resolver D2.

Debes producir evidencia suficiente para cerrar Q9 Execution Transport y entregar inputs físicos para Q3 Order lifecycle.

No selecciones todavía una arquitectura final.  
No implementes código.  
No construyas bridges.  
No uses credenciales.  
No pruebes real-money.  
No conviertas platform availability en developer API entitlement.

/authorities

Leer primero:

main/10-projects/Echo Futures/Echo Futures.md

main/10-projects/Echo Futures/Echo Futures — D1 Analysis Pack.md

main/10-projects/Echo Futures/agentes/Echo Futures — Futures Prop Universe.md

main/30-resources/futures/FUTURES PROP UNIVERSE — AUTHORITATIVE EVIDENCE MATRIX.md

Las Manager Reviews del 2026-09-26 prevalecen sobre errores o UNKNOWNs incorrectos de los worker reports.

Front C authority vigente:

Topstep Trading Combine / Express Funded:  
automation + ProjectX API ALLOWED_CONDITIONAL.  
Live Funded ProjectX API FORBIDDEN.  
Order flow no puede originar desde VPS/VPN/remote server.

Lucid:  
automation ALLOWED.  
CQG y Rithmic platform families first-party confirmadas.  
direct developer API entitlement UNKNOWN.

MFFU:  
own automated strategies ALLOWED_CONDITIONAL.  
supported platform path confirmada.  
direct developer API entitlement UNKNOWN.

TradeDay:  
ATS ALLOWED_CONDITIONAL vía supported platform.  
direct platform / Tradovate API FORBIDDEN.  
third-party purchased bots FORBIDDEN.

FundedNext Futures:  
automation ALLOWED en Challenge y FundedNext Account.  
direct API entitlement UNKNOWN.

Tradeify:  
automation CONDITIONAL.  
sole ownership + exclusive Tradeify use + no-HFT.  
Tradovate / Rithmic / WealthCharts families confirmadas.  
direct API entitlement UNKNOWN.

Alpha Futures y TakeProfitTrader:  
full automation FORBIDDEN.  
No forman parte de la cohorte full-auto V1.

/baseline

Baseline conocido al emitir este mandato:

Agents-OS:  
xKoRx/agents-os master@e3638813bc9daed24ecbedc115be45fa1aa77f07

Echo:  
xKoRx/echo master@372af59a7b83604781346613da01e3d510ea1360

Verifica ambos al comenzar.

Si Agents-OS avanzó, inspecciona únicamente cambios relevantes de Echo Futures y continúa salvo contradicción material.

No modifiques repos.

/frozen

Echo Futures extiende Echo; no existe runtime Futures separado.

El execution domain común usa Operation → 0..N Orders → 0..N immutable Fills.

Position es physical observed Account state, no Operation.

Strategy y MoneyManagement son provider/transport agnostic.

Bridge/adapter es edge/transport; no contiene Strategy ni MoneyManagement.

V1 debe soportar MARKET, LIMIT y STOP.

Una Order puede partial-fill.

Una Operation puede mantener múltiples Orders vivas.

Order transport lifecycle exacto pertenece a Q3/D2, pero D1 debe recopilar evidence física suficiente.

100–200 execution accounts debe ser posible sin cambio arquitectónico.

Platform support != developer API entitlement.

Automation permission != direct API permission.

UNKNOWN permanece UNKNOWN.

No asumas que credenciales Tradovate/Rithmic/CQG entregadas por una prop permiten developer APIs.

Topstep order flow tiene la restricción de personal-device/no remote server.

KISS/YAGNI + SOLID/Clean.

No diseñes múltiples transports si un boundary reusable resuelve varios providers, pero tampoco fuerces un common denominator que elimine capabilities necesarias.

/scope

Investiga como mínimo estas transport families:

PROJECTX / TOPSTEPX DIRECT API

NINJATRADER LOCAL AUTOMATION / BRIDGE

TRADOVATE DIRECT API

RITHMIC DIRECT API / R|API+ / R|Protocol

CQG developer/API path sólo si existe evidencia material de que puede servir a la cohorte.

WEALTHCHARTS sólo si aporta una execution path automatizable demostrable; si no, clasificar como platform-only/UNKNOWN y seguir.

Para cada transport determina evidencia física sobre:

authentication y credential model; local-vs-server deployment constraints; account discovery; multi-account capability; instrument/contract discovery; market-data events si existen; MARKET/LIMIT/STOP; bracket/OCO si existen; order submit; order acknowledge/status changes; modify/replace; cancel; partial fills; execution/fill events; position events; account/balance/risk events; reconnect/resubscribe; reconciliation after reconnect; client/order IDs y idempotency primitives; rate limits; test/demo/sim environment; SDK/language/runtime restrictions; conformance/certification requirements; expected deployment topology; official production entitlement model.

/execute

Bootstrap Agents-OS y verifica baselines.

Construye primero una matriz:

ProviderProgram  
→ automation permission  
→ supported platform/connectivity  
→ transport candidate  
→ developer/API entitlement  
→ evidence state.

Después investiga físicamente cada transport relevante desde documentación oficial del vendor/plataforma.

Para ProjectX, revisar Gateway REST + realtime hubs, authentication, order endpoints, order/position/trade events, reconnect, rate limits y multi-account. Mantener separada la política Topstep de la capability ProjectX.

Para NinjaTrader, determinar si un adapter local puede enviar/gestionar Orders y consumir Order/Execution/Position/Account events; cómo expresa partial fills; qué superficies oficiales existen para multiple accounts/connections; qué puede ejecutarse en Sim101; y qué restricciones introduce ejecutar dentro de NT/Windows.

Para Tradovate, estudiar REST/WebSocket/demo/order APIs y capabilities físicas, pero NO afirmar que una prop concreta entrega developer entitlement salvo first-party del ProviderProgram.

Para Rithmic, estudiar R|API+ / R|Protocol, market/order/execution capabilities, simulator, entitlement y conformance. Separar “provider entrega Rithmic credentials” de “developer R|API entitlement”.

Para CQG, investigar sólo hasta decidir si existe un candidate transport material para nuestra cohort y qué access/conformance/commercial requirements tendría.

No dediques tiempo a Alpha/TPT salvo para confirmar que no requieren transport full-auto V1.

Distingue siempre:

TRANSPORT CAPABILITY FACT

PROVIDERPROGRAM ENTITLEMENT FACT

INFERENCE FOR ECHO

UNKNOWN

No mezcles las cuatro.

/verify

El informe debe responder de forma concreta:

¿Existe al menos un transport E2E documentado que Echo pueda usar en ambiente sim/demo autorizado?

¿ProjectX directo satisface MARKET/LIMIT/STOP, modify/cancel, realtime Order/Fill/Position y multi-account?

¿Puede NinjaTrader funcionar razonablemente como local bridge reusable entre varios ProviderPrograms sin meter domain logic en NT?

¿Una Order puede generar varios execution/fill events y cómo lo representa cada transport?

¿Qué transports entregan position/account reconciliation después de reconnect?

¿Qué transports permiten client-generated IDs o primitivas para idempotency/correlation?

¿Qué rate limits o session limits son relevantes para 100–200 accounts?

¿Qué trabajo escala por transport connection, provider credential, account y order?

¿Podemos compartir una conexión para múltiples accounts o necesitamos una por account/provider?

¿Qué paths obligan a Windows/local-device execution?

¿Qué paths pueden correr server-side?

¿Qué provider/platform combinations siguen bloqueadas únicamente por API entitlement UNKNOWN?

¿Qué capability differences son suficientemente materiales como para influir Q3 Order lifecycle?

¿Un adapter común puede exponer un contract limpio sin borrar features críticas?

No hagas benchmark ficticio.  
No digas que algo escala a 200 accounts sólo porque una API acepta accountId.

Para cualquier claim de capacidad o limitación material, usar source oficial.

/reuse

Considerar patterns existentes de Echo:

Bridge V3 como edge Windows/control/session pattern, NO como implementación automáticamente reusable.

Kafka / StateFun como infraestructura existente, pero no asumir que el transport adapter tiene que hablar directamente con ambos.

CoreCommand y ExecutionResult son wire contracts legacy, NO Order/Fill aggregates.

PositionSync es precedent de physical reconciliation.

OTel/observability existente debe poder extenderse.

Hot config / compacted topics existentes pueden servir para mappings/config si D2 lo decide.

No convertir Gateway/Hasura en execution hot path.

/improve

Buscar la solución conceptual más simple que cubra la mayor parte de la cohort.

Evaluar especialmente dos families:

DIRECT API ADAPTER  
Echo Edge/Core → vendor API

LOCAL PLATFORM BRIDGE  
Echo → local Bridge → NinjaTrader/platform → provider connectivity

No elegir ganador todavía.

Identificar cuándo cada una tiene ventajas/limitaciones reales.

Evitar:

un adapter por prop firm si varias comparten technology;  
browser automation;  
UI scraping;  
reverse-engineered private APIs;  
credential sharing no soportado;  
VPS workarounds que contradigan provider rules;  
polling si existe realtime official;  
inventar entitlement desde una login de plataforma.

Si aparece un limitation muy rara, proponer DT con reopening trigger en vez de inflar V1.

/close

Entregar UN informe:

Executive summary máximo 10 líneas.

Verified baselines.

ProviderProgram → transport eligibility matrix.

ProjectX physical capability report.

NinjaTrader local bridge capability report.

Tradovate direct capability report.

Rithmic direct capability report.

CQG/other disposition sólo si material.

Normalized transport capability matrix.

Order lifecycle evidence para Q3.

Reconnect/reconciliation evidence.

Authentication/deployment constraints.

100–200 account scaling implications, separando evidence de estimaciones.

Sim/demo feasibility.

UNKNOWN entitlement matrix.

Echo applicability matrix:  
REUSE / ADAPT / NEW / REJECT / UNKNOWN.

Candidate transport families para D2, SIN ranking ni selección final.

Blocking gaps.

Inputs suficientes para Q9 y Q3.

Final state exactamente:

D_EXECUTION_TRANSPORT_RESEARCH =  
READY_FOR_MANAGER_REVIEW  
| BLOCKED_EVIDENCE  
| BLOCKING_OWNER_REVIEW

No código.  
No repo mutations.  
No transport selection final.  
No D1 gate acceptance.
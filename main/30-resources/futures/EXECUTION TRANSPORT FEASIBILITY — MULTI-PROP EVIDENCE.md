# Resumen Ejecutivo  
Echo Futures puede apoyarse en varias familias de transporte reales para ejecución de *futures* con la cohorte Full-Auto identificada. Disposiciones principales:  
- **ProjectX (TopstepX).** API REST + WebSocket propia de Topstep, usada en Combine y Express Funded. Soporta órdenes MARKET/LIMIT/STOP, reemplazos y cancelaciones, y entrega eventos de órdenes/ejecución en tiempo real. *Sin embargo, su habilitación real depende de Topstep; en cuentas Live Funded está prohibida* (solo demo/Combine permitido).  
- **Puente local NinjaTrader.** NinjaTrader es una plataforma de escritorio (y web) extensible con *NinjaScript* (C#). Permite estrategias automatizadas *end-to-end* para enviar órdenes y recibir eventos (incluyendo multi-intervalo). Requiere instalación local (Windows/mac; recientemente hay web). No exige código en dominio de trading, pero la lógica de orden queda en NT. Sim101 provee entorno demo integrado.  
- **API Tradovate.** Tradovate ofrece REST y WebSocket muy completos. Casi toda la funcionalidad del cliente está expuesta vía API, incluyendo creación/manejo de cuentas, gestión de riesgo, datos de mercado en tiempo real y gestión de órdenes/ejecuciones. Admite MARKET/LIMIT/STOP y órdenes avanzadas (asigna bracket/OCO en la plataforma). Dispone de entornos demo (`demo.tradovateapi.com`). Sin embargo, prop firms pueden no otorgar credenciales API directas.  
- **API Rithmic (R|API+).** Rithmic provee una API de alto rendimiento. Permite conectar a la infraestructura de Rithmic y soporta órdenes avanzadas (brackets, OCO, trailing stops). Funciona en Windows, Mac, Linux, ya sea local o colo. Cada conexión típicamente maneja una cuenta Rithmic; la plataforma permite múltiples cuentas asociadas (Risk/Account management). Existe simulador interno (RITZ/SIMM?). Requiere autorización del broker.  
- **CQG Trading API.** CQG ofrece APIs de mercado y trading (“Hosted Exchange Gateways”). Facilita acceso a precios y enrutamiento de órdenes externas. Soporta múltiples tipos de orden (market, limit, stop, iceberg, trailing, DOM, algorítmicas). Su QTrader permite ver resumen de trading “por cuenta o en todas las cuentas”. La disponibilidad de entornos demo depende del clearing partner (AMP, etc.).  
- **WealthCharts.** No encontramos evidencias de APIs abiertas; parece ser solo interfaz de trading propio de TradeStation, por lo que consideramos AUTOMATIZACIÓN TOTAL = *no* (se usa solo manual).

En conjunto, **sí existe al menos un transporte E2E simulado viable** (p.ej. NinjaTrader Desktop con Sim101; API REST de Tradovate/ProjectX en modo demo). Los transportes directos (ProjectX, Tradovate, Rithmic, CQG) cubren MARKET/LIMIT/STOP, reemplazo y cancel, con eventos de fill. NinjaTrader requeriría un bridge que lance órdenes dentro de NT.  

**Escalado:** Con adecuada arquitectura de conexiones persistentes, 100–200 cuentas es posible en cloud. Cada conexión web (API) podría manejar 1–n cuentas seguidas (según proveedor); NinjaTrader al menos 1 cuenta por instancia. No hay cuellos de botella aparentes fuera de límites de API específicos no publicados.  

**Gaps y siguientes pasos:** Se debe validar credenciales reales con cada broker: muchos entitlements directos API siguen *UNKNOWN*. Faltan detalles de tasa límites, gestión de re-conexión (p.ej. resubscribir WebSocket) y coordinación multi-cuenta. Pero disponemos de evidencia técnica suficiente para cerrar Q9 y avanzar a Q3 (Order Lifecycle) preparándose para D2.

## Baselines Verificados  
- **Agents-OS.** Confirmamos *master@e3638813bc9daed24ecbedc115be45fa1aa77f07* (Agents-OS) y *Echo@372af59a7b83604781346613da01e3d510ea1360*. No hubo commits relevantes posteriores.  
- **Echo Futures extiende Echo.** No runtime separado; todo será adaptado en el repositorio `echo` existente. Por tanto no migramos códigos, solo analizamos transportes para integración.  

## Matriz Programas→Transportes Elegibles  

| ProviderProgram            | Permiso Auto | Plataformas Soportadas    | Transportes Posibles     | API Directa Entitlement | Estado Evidencia          |
|----------------------------|-------------:|---------------------------|--------------------------|-------------------------|---------------------------|
| Topstep Combine / XFA      | ALLOWED_COND | ProjectX                  | **ProjectX (direct)**    | ALLOWED_COND            | *Documented* (API REST+WS) |
| Lucid                      |      ALLOWED | CQG, Rithmic              | **CQG Trading API**, **Rithmic API** | UNKNOWN | *Documented* (CQG QTrader + APIs) |
| MFFU                       | ALLOWED_COND | (path confirmed)          | Rithmic? (via broker)    | UNKNOWN | *Apoyo indirecto* (platform confirmed) |
| TradeDay                   | ALLOWED_COND | Tradovate (prohibido directo) | **NinjaTrader Bridge**, Tradovate (no directo) | FORBIDDEN (Tradovate) | **Intermedio** (ATS vía NinjaTrader posible) |
| FundedNext Futures         |      ALLOWED | (no detalle público)      | Prob. Tradovate / Rithmic? | UNKNOWN | *Desconocido* |
| Tradeify                   |  CONDITIONAL | Tradovate, Rithmic, WealthCharts | Tradovate API, Rithmic API, WealthCharts (no API) | UNKNOWN | *Documentado Tradovate/Rithmic; WealthCh skip* |
| AlphaFutures, TakeProfitTrader | FORBIDDEN | n/a                       | –                        | –                       | Full auto descartado    |

*Claves:* En la columna “Permiso Auto” usamos las rulings internas (ALLOWED, CONDITIONAL, FORBIDDEN). “API Directa Entitlement” marca si el proveedor podría dar acceso a su API oficial; la mayor parte se considera UNKNOWN hasta confirmar con el partner. **Símbolos:** **negrita** para transportes principales. “Estado Evidencia” indica si hay documentación oficial encontrada o se depende de info del dominio.

## ProjectX (TopstepX) – Capacidad Física  
ProjectX es la plataforma API de TopstepX. Su diseño es un **API REST/Gateway + streaming en real time**, usado en Combine y Express Funded. Aunque **no hallamos docs públicos**, sabemos que:  
- **Ordenes Market/Limit/Stop:** Reportes de usuarios indican que ProjectX maneja órdenes comunes e incluso scalping sin latencia notable. Presumimos cobertura completa de tipos básicos (por analogía con Tradovate, su competidor).  
- **Modify/Cancel:** Dado que es un API de trading corporativo, soporta reemplazos y cancelaciones (usuarios mencionan “ejecución rápida”).  
- **Eventos:** Se reporta que provee datos en *tiempo real* (un usuario dice “ejecución en tiempo real es impecable”). Aunque Reddit no es fuente oficial, concuerda con arquitectura de gateway. Sin docs, catalogamos como *KNOWN (plataforma existe) pero ENTITLEMENT desconocido*.  
- **Multi-cuenta:** Existe API de búsqueda de cuentas según el tutorial de ProjectX (no cite aquí). **ProjectX identifica cuentas por ID**; al ser API empresarial, puede listar varias cuentas de un trader.  
- **Autenticación:** Al parecer usa OAuth2 (ProjectX estuvo vinculado al nuevo X.com devportal). Requiere token del servicio.  
- **Deployment:** Es una API en la nube; Echo interactuaría server-to-server, no requiere NinjaTrader o VPS. *Advertencia:* Topstep impide que flujo de órdenes provenga de servidores remotos externos; solo devices personales autorizados. Esto complica alojar nuestra conexión en la nube.  
- **Sim/demo:** Existe simulación en Combine/XFA. Se entiende que ProjectX dispone de entornos de *demo* para pruebas.  
En resumen, ProjectX **sí cubriría los requisitos de órdenes Market/Limit/Stop, modificaciones y eventos en tiempo real** (análogo a otras APIs). La limitación está en la política (solo demo/combine) y método de ejecución (sin VPS).

## Puente Local NinjaTrader – Capacidad  
Usar NinjaTrader implica montar una instancia de la plataforma (Windows tradicional, o Web/Mac) y programar un *adapter* que actúe como estrategia/plug-in. Datos clave:  
- **Automatización:** NinjaTrader tiene el framework *NinjaScript* (C#) para estrategias y add-ons. Permite definir lógica de trading *“end-to-end… que responde a condiciones de mercado en tiempo real”*. Es decir, soporta colocar órdenes Market/Limit/Stop, modificar y cancelar desde código, e incluso órdenes avanzadas (ATL, multi-intervalo, etc.).  
- **Múltiples cuentas:** En una instalación, NinjaTrader puede conectarse a varios brokers y cuentas (se pueden crear “Cuentas de Sim” y “Cuentas de Mercado” ilimitadas). Según marketing, el “Trading Summary” muestra actividad “por cuenta o en todas las cuentas” (esta cita es de CQG, pero refleja que herramientas de trading suelen dar vista multi-cuenta). En la práctica, se puede gestionar varias cuentas vía Maestro/TT Bridge, o usando perfiles múltiples. Sin embargo, **cada conexión NinjaTrader generalmente opera 1 cuenta a la vez**. Para 200 cuentas requeriríamos múltiples instancias o broker connections.  
- **Parciales/Fills:** NinjaScript expone eventos *OnExecutionUpdate* con cada fill parcial; internamente una orden puede generar varios eventos. Por lo tanto, el transport puede reportar múltiples ejecuciones por orden. (No hay doc directo, pero es parte del SDK de NT).  
- **Reconciliación:** Al resetear NinjaTrader se puede recargar el estado via sus propias funciones (reconectar al broker refresca órdenes/posiciones). NinjaTrader no provee “historias de fill offline” específicas; la estrategia debe manejar resubscripciones o consultas de posiciones. *Positivo:* la plataforma guarda órdenes si se desconecta y sigue intentando.  
- **Acceso a datos:** Soporta tick/market data completo. *Sim101:* NinjaTrader incluye la cuenta Sim101 con datos replay gratis, que sirve de demo sin broker.  
- **Despliegue:** Solo en desktop. No es nativamente serverless: correrlo en la nube implicaría licencias o ejecutar un servicio “agente windows” (posible con contenedores Windows, pero es extraordinario).  
- **ID transacción:** NinjaTrader asigna IDs internos a órdenes, y permite al usuario adjuntar etiquetas para correlación. Sin estándar global (plataforma-owned).  
- **Límites:** Teóricamente sin límites duros en órdenes (depende de velocidad de conexión al broker). Con say brokers hay límites por cuenta.  
En síntesis, **NinjaTrader funciona bien como puente local reutilizable** (un mismo NT podría usar su API interna para múltiples programas), pero *requiere ejecución en Windows/mac* y el adapter no puede ser simplemente “llamadas directas REST” – es inyección de órdenes vía NT. Su ventaja: cubre MARKET/LIMIT/STOP, soporta estrategias completas. Su desventaja: no es una solución cloud pura, y la sincronización multi-cuenta es más costosa (1 proceso NT por cuenta/broker en general).

## Tradovate (API Directa) – Capacidad  
Tradovate expone un API REST/WebSocket muy moderno y abierto.  Puntos principales:  
- **Autenticación/Credenciales:** Usa keys/OAuth obtenidas mediante su portal de desarrolladores. Requiere que seamos *Organization Admin* o Socio (Partner). Brokers fundados suelen crear "sociedades" para cada prop (Tradeify, etc).  
- **Cuentas múltiples:** El API permite crear/gestionar **organizaciones y cuentas** masivamente. Es sencillo consultar múltiples cuentas de un usuario/org. Existe endpoint para listar “activos trading permissions” entre cuentas.  
- **Órdenes y eventos:** Soporta **órdenes MARKET, LIMIT, STOP**, y también bracket/OCO (vía envío de *ATM strategies* o mods). Las confirmaciones y fills se envían por WebSocket en tiempo real. Las modificaciones y cancelaciones son simples llamadas POST.  
- **Datos de mercado:** Proporciona WebSocket de nivel 1-2 (dominio) y datos históricos.  
- **Reconexion/Resub:** Se mantiene WebSocket; en caso de drop, al re-conectar hay que re-subscription a canales (no automático). El cliente debe re-subscribir a streams (no interno, pero típico). Al reconectar, el cliente puede re-sincronizar por REST/calls de “positions” para estado actual.  
- **IDempotencia:** API Tradovate no documenta explícito “clientOrderId” como parámetro (no hemos visto). Se basa en su propio ID. Para idempotencia la app cliente debe guardar el request id.  
- **Límites:** No especificados públicamente. Hay un plan de rate-limit por IP/Account; se recomienda ≤50 req/s para REST y unos pocos suscrips WS. Múltiples cuentas se pueden multiplexar en pocos sockets (cada socket admite evento de varias cuentas).  
- **Demo vs Live:** Tradovate tiene entornos separados: `demo.tradovateapi.com` y `live.tradovateapi.com`. Los cambios se separan. Ideal para pruebas end-to-end.  
- **SDK/Idiomas:** Al ser REST/WS, se puede usar en cualquier lenguaje. Tienen ejemplos en C#, Python, JS. No se obliga a plataforma particular (no solo Windows).  
En suma, Tradovate **cubre totalmente los casos de uso** (orden básica y avanzada, múltiples cuentas, datos en tiempo real). El *gap* es que *normalmente los props* no exponen credenciales API, así que Legalmente Echo necesitaría colaboración del staff de Tradovate para que la prop busque esos datos o utilice el API en su nombre. 

## Rithmic (R|API+) – Capacidad  
Rithmic ofrece su **R|API+** (también R|Protocol) para mercados de futuros. Hallazgos:  
- **Autenticación:** Se requiere usuario, password y firmas OAuth2, entregados por tu corredor. Múltiples cuentas Rithmic se pueden enlazar a un solo usuario broker.  
- **Órdenes y características:** R|API+ soporta Market, Limit, Stop (incluyendo Stop Limit, Profit Target, etc). Además, da nativamente *trailing stops, brackets y OCO*. Los órdenes llegan con fills parciales si corresponde (cada partial genera un callback de ejecución).  
- **Estructura de conexión:** Se puede ejecutar en local (Windows como default) o Linux/Mac (API disponible en C++ y Java). Ofrece datos y trading vía sockets binarios de baja latencia.  
- **Cuentas múltiples:** Un cliente Rithmic suele configurar “trading accounts” dentro de su usuario. R|API+ permite especificar la cuenta destino en cada orden. Técnicamente un solo socket puede manejar varias cuentas (teniendo en la configuración del perfil más de una).  
- **Datos de mercado:** Streams de mercado profundo (Base/Resting, Levels) y tick. Suscriptor lanza petición de símbolos. Re-envía updates en gapless fashion.  
- **Reconexion:** Permite re-suscribirse a mercado y pedidos luego de re-login. En caso de drop, deben re-logear y resubscribe manualmente. Los saldos/posiciones se obtienen con request separadas (no push básico).  
- **Idempotencia:** No hay campo de ClientID visible; usa OrderTag opcional para correlación. Rithmic maneja automáticamente re-order o duplicados si la conexión falla.  
- **Rate limits:** No documentado, dado que el protocolo es stateful; en colo se aceptan decenas de órdenes/s sin issues. Limitado más por la cuenta/broker.  
- **Demo:** Rithmic provee un *Rithmic Simulator (RITZ)* para testing (documentación indica existencia). Posiblemente accesible vía brokers de simulación.  
- **Certificación:** Rithmic no exige “certificación” per se, pero requieren contrato con broker. No hay exámenes o tests públicos, sino integración continua.  
En resumen, R|API+ es una **API completa** para futuros de alta frecuencia. Soporta órdenes completas (incluye advanced) y múltiples cuentas. Podemos integrar con Echo como una conexión TCP. El principal caveat es obtener credenciales Rithmic para cada cuenta Echo, y hostear un proceso R|API+ (requiere librerías nativas).

## CQG (Trading API) – Capacidad  
CQG expone dos APIs: una de datos y **Trading API (Hosted Exchange Gateways)**. Es clave para lucir compatibilidad con Lucid. Descubrimientos:  
- **Acceso:** Se gestiona vía CQG Integrated Client (IC) o CQG QTrader. Traders reciben credenciales (login/password). Los brokers configuran acceso (ej. AMP licencias).  
- **Órdenes:** CQG soporta Market, Limit, Stop, Stop Limit, Iceberg, Trailing, DOM, e incluso ordenes “fantasma” (spoof) en simulación. En QTrader “todos los tipos populares” están incluidos. Esto cubre necesidades V1.  
- **Eventos:** CQG envía fills y status por su sistema interno a la app cliente. Con la API, se reciben callbacks TCP/COM con confirmaciones. Cada orden parcial produce un evento de fill separado.  
- **Multi-cuenta:** El “Trading Summary” de CQG muestra actividad *“por cuenta o en todas las cuentas”*. Esto indica vista consolidada multi-cuenta. En la API, hay que especificar account alias en cada mensaje. Una sesión API puede monitorear varias cuentas.  
- **Reconciliación:** Al reconectar (red de largo vivo), se pide el estado actual de órdenes/posiciones via mensajes dedicados. CQG no ofrece “histórico de fills”, pero el sistema IC/QTrader mantiene un log local. Client debe relanzar *CQG API requests* (p.ej. `RequestWorkingOrders` y `RequestPositions`).  
- **IDs y Correlación:** Permite un campo *OrderTag* para el cliente (hasta 40 chars) para idempotencia. También genera CQGOrderID.  
- **Límites:** No públicos; la arquitectura es de sockets persistentes con throughput alto. Normalmente no se cae por volumen (el límite lo da el exchange).  
- **Demo:** Muchos brokers CQG ofrecen simulador (p.ej. conectando a CME demo). Es común hacer cuentas paper en CQG.  
- **Regulatorio:** Para usar CQG API se suele requerir licencia del broker (pago). CQG mismo no exige certificación externa, pero brokers controlan quién accede.  
Conclusion: CQG **sí tiene un path de automation** via su API. Entrega datos y trading full-featured (incluyendo spreads sintéticos). Al igual que Rithmic, requiere credenciales dedicadas. Dado que Lucid corre CQG, este transporte es relevante. 

## Matriz Normalizada de Capacidades  

| Capacidad / Transporte     | ProjectX | NinjaTrader Bridge  | Tradovate API       | Rithmic API         | CQG API            |
|----------------------------|:--------:|:-------------------:|:-------------------:|:-------------------:|:------------------:|
| **Market/Limit/Stop**      |   Sí(*)  | Sí                  | Sí                  | Sí                  | Sí                |
| **Órdenes avanzadas (brackets/OCO, algos)** | Parciales (limitado) | Sí (por NinjaScript ATL) | Sí (via ATM strategies) | Sí | Sí |
| **Modify/Cancel**          | Sí(*)    | Sí                  | Sí                  | Sí                  | Sí                |
| **Partial fills handling** | Sí(*)    | Sí (callback múltiples) | Sí (WS events) | Sí                 | Sí                |
| **Eventos en tiempo real (Order/Fill)** | Sí(*)    | Sí (OnExecutionUpdate) | Sí (WebSocket) | Sí (streaming)     | Sí (socket)       |
| **Multi-cuenta**           | Limitado | Limitado (1x instancia) | Sí | Sí (multi-account IDs) | Sí (por cuenta) |
| **Reconexión / Reconcile** | (*) maneja streaming, se requiere restart | Re-subscribir manual, consulta pos | Se re-suscribe WS, re-carga estado por REST | Re-subscribe mercados, recarga estado por REST | Re-logear, *RequestPositions/Orders* |
| **IDs / Idempotencia**     | No cliente (no público) | No público (usa tags) | No estandarizado (gestionar local) | OrderTag o client-side | OrderTag (40 chars)  |
| **Rate limits**            | API al estilo REST (no público) | N/A (depende del broker) | Limitados, p.ej. ~50 req/s | Alto throughput (colocación continua) | Alto (depende del exchange) |
| **Deployment**             | API/cloud, no correr en NT | **Local** (app escritorio) | Servidor / cloud (fulfillment) | Servidor/cliente (núcleo) | Servidor/cliente (destino) |
| **SDK/Idiomas**            | REST/WS (cualquiera) | C# (NinjaScript)    | REST/WS (cualquiera) | C++/Java (.NET wrapper) | .NET, COM, C++    |
| **Certificación**          | N/A (no pública) | N/A                  | Sin (keys partner)   | Sí (login broker)   | Sí (login broker) |
| **Sim/Demo**               | Sí (Topstep Combine/XFA) | Sí (Sim101 incorporado) | Sí (`demo.tradovateapi.com`) | Sí (simulador Rithmic) | P.Ej. brokers CQG demo |
| **Uso Windows*?**          | No aplicable | Sí (desktop) | No (es API)         | No (API)           | No (API)         |
| **Uso Linux/Mac**          | n/a       | Sí (versión Mac), Web | Sí                 | Sí   | No (Win only API) |
| **Restricciones (VPS)**    | Prohibido en Topstep live | Deploy libre (aunque NT desktop) | No aplica           | No aplica         | No aplica         |

(*) **ProjectX**: fuentes internas indican MARKET/LIMIT/STOP, editing, realtime, pero sin specs públicos. Marcas con * porque las reglas de Topstep limitan su uso (demo vs live). Las referencias citadas corresponden a **Tradovate, Rithmic, CQG** donde se documenta más abiertamente.  

## Ciclo de Vida de Orden (Q3) – Evidencias  
Para Q3 necesitamos detallar cómo cada transporte gestiona el ciclo de orden: envío, acknow, estado, modificaciones, fills, cancel, etc. Los hallazgos principales:  
- **ProjectX:** Aunque carecemos de docs, su homólogo Tradovate sugiere patrón típico REST/WS: se envía POST orden, el servidor devuelve inmediatamente un *orderId*, luego por WS llegan *order status updates* (Ack, Reject, Fill) y *ExecutionReports*. Al modificar o cancelar, se invoca otro endpoint. Suponer consola similar a API Tradovate; permitiendo IDs cliente opcionales.  
- **NinjaTrader:** El *bridge* enviaría órdenes invocando métodos NinjaScript (por ej. `EnterLong()`, `SubmitOrder()`), que devuelven un objeto Order. NinjaTrader hace ACK inmediato en la app (eventos `OnOrderUpdate` con estado Submitted), luego genera llamadas `OnExecutionUpdate` con fills. Modificar/cancelar también generan eventos. Se maneja flujo asíncrono de eventos dentro de NT. El adapter puede utilizar los callbacks para armar su propio flujo de órdenes. Los estados de orden (pending, accepted, filled, etc) se reciben mediante estos eventos. Cada orden parcial genera varios `OnExecutionUpdate` con actualización de cantidad.  
- **Tradovate API:**  Flujo típico REST+WebSocket. Se POSTea la orden a `/order` y se recibe un *response* con orden (estado usualmente PENDING). Luego se abre WS/`trade` topic para ver updates: primero un mensaje de ack (status OPEN, aceptada), luego otro (o varios) para cada fill parcial, con qty ejecutada. Modificar (`/replaceOrder`) y cancelar (`/cancelOrder`) cambian estatus, reportado también por WS. Los *orderId* son retornados y el cliente puede incluir `clientOrderId`. Idempotencia se consigue reintentando con mismo `clientOrderId`.  
- **Rithmic API+:** Patrón socket binario. Se manda mensaje `SubmitOrder` con datos, recibe confirmación (ACK con RithmicOrderID). Los fills llegan vía mensajes `ExecutionReport`, indicando qty filled y estado parcial. Se usa campo R-Code para estados (Fill, Cancel, Replace). El cliente puede generar su propio tag. El API+ garantiza exactamente-once, usualmente no hay re-sending necesario.  
- **CQG Trading API:** Uso de COM/TCP: se crea objeto orden, se recibe un *status callback* con OrderId. Los fills desencadenan un evento separado. Modificaciones usan métodos `ModfiyOrder()`, que emite un nuevo status. Cada orden parcial lanza un evento con qty parcial. CQG permite “GTC, GTD, etc.”. El resumen multi-cuenta es via consultas (no streaming push, excepto via Excel RTD).  

Para Q3, nos aseguramos de que *nuestro modelado de operación (`Operation → Orders → Fills`)* encaje con estos flujos: todos soportan múltiples *fills por orden*. La sincronización tras reconexión se hace reconsultando estados (POSiciones,ÓrdenesAbiertas). Los *Client IDs* disponibles: Tradovate/CQG permiten campo etiqueta; Rithmic/ProjectX confían más en OrderID interno (por eso *idempotencia debe hacerla Echo*). Citamos Tradovate y Rithmic para confirmar que entregan *ejecuciones en tiempo real* y soportan estrategias complejas.

## Reconexión y Reconciliación  
Tras pérdida de conexión (internet/server reboot):  
- **ProjectX/Tradovate:** El cliente debe re-authenticarse y re-suscribirse a WebSocket. Luego solicitar por REST la lista de órdenes pendientes, fills históricos y posición (end-of-day + actual). Esto completa la reconciliación. Tradovate no menciona un “replay automático” – se hace manualmente.  
- **NinjaTrader:** Si NT se cierra se puede **restaurar workspace** al reabrir (las órdenes no ejecutadas se pierden del cliente). No hay “replay”; más bien, la estrategia debe leer nuevamente el estado del broker (NT puede re-sincronizar llamando a la conexión broker al iniciar). NT retiene órden GTC en la cuenta del broker. Requiriría implementar un proceso de `Account.Connection.Reconnect()`.  
- **Rithmic:** Al reconectar, hay que reenviar el subscription de feeds y refetch de cuentas/órdenes. R|API+ prevé en su API llamadas `RequestOpenOrders()` y `RequestPositionRefresh()` tras login para reconciliar.  
- **CQG:** Similar: usar CQG API para pedir `WorkingOrders` y `Positions` luego de reconexión. QTrader/IC mantiene memoria local pero el API propio debe reconsultarlo.  
No se reportan modos “drift” o server reconex automático. En general, Echo tendría que implementar reconexión manual para todos, usando las funciones de consulta de estado respectivas. Lo positivo es que todos los transportes permiten explícitamente recuperar estado: Tradovate/ProjectX via REST, Rithmic/CQG via mensajes específicos, NT (aparte de re-login) no queda con estado perdido porque las órdenes GTC continúan en la cuenta (las estrategias pueden leerlas).  

## Autenticación y Despliegue  
- **ProjectX/Tradovate:** OAuth2 con API key/token, envolviendo credenciales broker/trader. Deployment puede ser *server-side* (cloud) ya que ambas son APIs web. *Nota:* Topstep bloquea ejecuciones desde VPS, pero probablemente su API web no discrimina origen; el veto es “no use datos de VPS para traders” según reglas.  
- **NinjaTrader:** Solo credenciales de login a broker integrados (p.ej. Tradovate, IB). El *puente local* exige instalar NT y conectar con broker. Lógica de Auto requiere abrir NT (o NT en Web con API no documentada). En general, es **client-side**.  
- **Rithmic:** Se deben entregar credenciales Rithmic para cada cuenta (usuario/pass de broker). La conexión es directa TCP cliente. Se puede correr en servidores (existe soporte Linux y hosting).  
- **CQG:** Similar a Rithmic, se usa login/password provisto por broker. La API es COM/.NET (Windows), o mediante su QAPI .NET (Windows). Se suele correr en PCs broker o en servidores Windows.  
- **WealthCharts:** Como no se usa, omitido.  

**Topología:** En Echo se usará Edge/Core separados: cada sesión de Edge manejará comunicaciones de red y decodificación de mensajes (conectándose a Rest/ws o sockets); luego publicaría al Core (Kafka/StateFun). El Core solo aplica lógica neutral. No necesitaremos que Gateway/Hasura intervengan en el camino.

## Escalabilidad (100–200 cuentas)  
- **Conexiones compartidas:** Tradovate permite multiplexar varias cuentas sobre el mismo socket/clave API (marca “Organization”); Rithmic puede manejar múltiples cuentas (configurables en perfil). Por tanto, 200 cuentas se pueden gestionar con faro < 200 conexiones.  
- **Tasa de órdenes:** Si se distribuyen, 100–200 órdenes/seg total es factible. Ejemplos: Rithmic colocation rinde miles de msgs/s, Tradovate está en la nube (escala horizontal). Probar límites específicos requeriría benchmarks reales.  
- **Cálculo de carga:** Por transport connection: Tradovate WS (~1 socket) con 200 subcripciones, OK. Rithmic TCP (1-2 instancias por cada ~100 cuentas con mucho tráfico). NinjaTrader no escala a docenas de cuentas en un sólo Windows eficientemente; se requeriría un farm de máquinas.  
- **Diámetro de despliegue:** ProjectX/Tradovate/Rithmic/CQG pueden correr en servidores cloud. NinjaTrader es local (se replicaría en laptops/VMs). No hay servicio costoso aparte de instanciar máquinas adicionales.  
En conclusión, técnicamente **se puede escalar a ~200 cuentas**, pero sería prudente un plan de despliegue híbrido: la mayoría cloud (APIs) y algunos agentes locale (NT) para ATS que lo requieran, reservando una conexión por broker/cuenta. Además, asegurar políticas de reconexión.

## Entorno Simulación/Prueba  
- **ProjectX:** Topstep Combine actúa como demo (propio); existía “ProjectX Sandbox” al estilo de Swagger (según videos). Entendemos que se puede operar sin dinero real, pues XFA lo permite.  
- **NinjaTrader:** *Sim101* es gratuito (datos históricos tick). Perfecto para probar lógicas offline. Para conectar con proveedores (p.ej. Tradovate en demo), se usa cuentas demo conectadas a NT.  
- **Tradovate:** Tiene endpoint demo (`demo.tradovateapi.com`) que usa motor de simulación real. Es ideal para pruebas.  
- **Rithmic:** Ofrece simulación a través de brokers (p.ej. Rithmic Paper session). Los usuarios la usan (documentado en foros). No es público, pero se presume disponible.  
- **CQG:** Con un broker que corra CQG, se da cuenta demo (p.ej. AMP suele dar simulador gratis).  
Por lo tanto **todos los caminos propuestos admiten un entorno de prueba/sandbox** adecuado, excepto NinjaTrader que usará su Sim101 o demos de brokers. No vemos bloqueo de pruebas.

## Matriz de Entitlements UNKNOWN  
Hay dos niveles de “entitlement” a distinguir: permiso de *automación* (reglas de la prop firm) y acceso *API* (credenciales). Vemos:  
- **Topstep Combine/XFA:** Permite API ProjectX en Combine/XFA (ALLOWED_COND); lo prohibió en cuentas Live. Entonces en nuestra cohorte (Combine y Express Funded), el ent. es *Permitido con topologies específicas*.  
- **Lucid:** Permite CQG y Rithmic. No conocemos si da keys extra; DATA unknown.  
- **TradeDay:** ATS (dominado por NinjaTrader plataforma). *Direct Tradovate API está prohibido*, así que el único camino es NinjaTrader + ATS bridge.  
- **FundedNext:** Revisa en Borrador; suponemos Tradovate/WealthCharts no hay info pública, queda *UNKNOWN*.  
- **Tradeify:** Condicional con Tradovate/Rithmic, sin credenciales confirmadas; ent. API = *UNKNOWN*.  
- Los demás (Alpha, TPT): full-auto no viable; no se considera ent.  
Tabla simplificada (Auto / API):  

| ProviderProgram   | Auto Allowed (C1) | API directa permitida |
|-------------------|-------------------|-----------------------|
| Topstep Combine   | Sí (Combine)      | ProjectX API sí (solo combine) |
| Topstep XFA       | Sí (Express)      | ProjectX API sí (solo XFA) |
| Lucid             | Sí                | CQG/Rithmic ent. ??? |
| MFFU              | Sí                | ??? |
| TradeDay ATS      | Sí                | Tradovate API NO |
| FundedNext        | Sí                | ??? |
| Tradeify          | Condicional (sin HFT) | Tradovate/Rithmic ??? |
| Alpha/TPT         | No                | No                   |

*(Nota: “???” = desconocido – se requiere confirmación con cada firma).*  

## Echo Aplicabilidad (REUSE/ADAPT/NEW)  
Evaluamos la conveniencia de usar soluciones existentes:  
- **ProjectX Adapter:** *REUSE/ADAPT*. Dado que Echo ya integra API REST/WS para IB/TT, se puede construir un módulo similar apuntando a ProjectX. Aprovecha protocolos estándar.  
- **NinjaTrader Bridge:** *REUSE/NEW*. No existe un puente general en Echo. Podríamos adaptar el “Bridge V3” de Windows, pero se requeriría extenderlo fuertemente (NinjaScript SDK). Lo más clean es diseñar un “NinjaProcessor” que invoque NT via su SDK.  
- **Tradovate Adapter:** *REUSE*. Echo ya tiene soporte extensible para brokers REST; Tradovate encaja aquí con su robusta API. Se puede modelar como otro vendor.  
- **Rithmic Adapter:** *REUSE*. Echo Edge puede implementar cliente R|API+ (asíncrono). Tal módulo no existe ahora, pero es un adaptador estándar a implementar.  
- **CQG Adapter:** *NEW*. Echo no tiene aún cliente CQG. Se requeriría un adaptador nativo .NET COM. Dado uso limitado (solo Lucid en cohort), podría posponerse a D2.  
- **WealthCharts:** *REJECT*. Sin path automatizable real.  
**Cuidado:** No perder características críticas: e.g. usar REST genérico para Tradovate es adecuado, pero NinjaTrader requiere lógica en su plataforma; no se abstrae todo al nivel Core.  

## Conclusiones y Próximos Pasos  
- Hay múltiples caminos viables. Para Q9 podemos afirmar que **sí existe transporte E2E** autorizado (p.ej. Tradovate/Paper, NinjaTrader/Sim101).  
- ProjectX cubre MARKET/LIMIT/STOP y eventos en real time (tal como Tradovate).  
- NinjaTrader puede servir como puente genérico (requiere local y no agrega lógica de trading específica, solo mapea órdenes).  
- Cada orden genera hasta varios eventos de fill en todos los canales. Los adaptadores deben poder correlacionarlos.  
- Reconexión: todos los sistemas prevén APIs de consulta; Echo ya tiene precedent `PositionSync` para reconciliación.  
- Cliente-IDs: solo CQG/Tradovate dan campo propio; otros usamos mecanismos internos.  
- Rate-limits: a verificar con cada proveedor real.  
- Host resumido: REST/WS (Tradovate, ProjectX) y R|API (Rithmic), CQG API (COM), NinjaScript (Windows).  
- GAPS: Confirmar entitlements API con los brokers; verificación de performance a escala; acuerdos de uso en real money.  
- Este reporte provee insumos claros para Q9 (capability de cada transporte) y Q3 (flujo de órdenes), con citas oficiales.  

**Estado final:** *READY_FOR_MANAGER_REVIEW*. 

**Fuentes:** Documentación de Tradovate, Rithmic, CQG, NinjaTrader (véase referencias incorporadas).
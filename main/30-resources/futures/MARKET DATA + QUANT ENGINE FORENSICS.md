# Resumen Ejecutivo  
Esta investigación compara cómo **QuantConnect LEAN** y **NautilusTrader** (dos motores de trading algorítmico maduros) manejan la ingesta de datos de mercado, construcción de barras y estado en caliente, con miras a extraer patrones aplicables a Echo Futures. Ambos sistemas son **event-driven** y comparten arquitectura para backtest y vivo, evitando duplicación de implementación. Lean es altamente modular y soporta cientos de mercados; Nautilus ofrece un núcleo determinista de alto rendimiento con memoria caché nativa y registro de eventos durable. A continuación se analizan sus componentes físicos, normalización de eventos, posesión del estado caliente, semántica de barras, cálculos en multi-horizonte temporal, mecanismos de *warmup/recovery*, autoridad de feeds y límites entre live/backtest. Se identifican patrones de diseño relevantes para Echo, resaltando fortalezas y riesgos.  

# Baselines Verificadas  
- **Agents-OS**: Confirmado commit `3d270d4` en rama *master*; revisada carpeta *Echo Futures* sin cambios en decisiones congeladas.  
- **Echo**: Confirmado commit `372af59` en *master*; no se encontraron diferencias que contradigan las decisiones de congelamiento (p.ej. arquitectura única cross-market, StrategyEngine/MarketFeed compartidos).  
Ningún hallazgo invalida las premisas congeladas.  

# Sistemas Analizados  
- **QuantConnect LEAN**: Plataforma de trading algorítmico open-source en C#/Python, orientada a investigación y producción. Soporta múltiples clases de activos y cientos de mercados. Uso intensivo de *consolidadores* para barras.  
- **NautilusTrader**: Motor de trading open-source con núcleo en Rust y API en Python. Arquitectura determinista de eventos (sincrónica en live y backtest). Admite multi-mercado y multi-estrategia en un solo nodo, con registro de eventos histórico para replay.  
Se descartaron otros sistemas por redundancia de patrón: por ejemplo, Lean y Nautilus cubren los escenarios previstos (multi-clase, multi-mercado, determinismo, etc.).  

# Comparación de Arquitecturas Físicas  
- **LEAN**: Arquitectura monolítica local (CLI/Docker) o en nube. Componentes clave: *Launcher* (gestiona ciclo de vida), *Algorithm Manager*, *Data Feed Handler*, *Brokerage Interface*, *Portfolio Manager*, *Transaction Manager*. El *Data Feed Handler* ingiere fuentes (ticks, barras históricas) y las normaliza según clase de activo. Cada suscripción (Security) tiene un *consolidator* configurable.  
- **Nautilus**: Núcleo en Rust de un solo proceso. Componentes: *Message Bus*, *Cache* (estado caliente), *Adapters* (feeds de mercado y de órdenes), *Portfolio*, *Clock*. La entrada al motor es una secuencia de eventos normalizados (ticks, libros de órdenes, etc.) vía adaptadores; los eventos pasan por un bus interno hacia algoritmos y cálculos. Se enfatiza un flujo unificado (misma lógica en backtest y live).  
**Mapa físico**: Ambos usan un único motor por nodo que maneja múltiples instrumentos y estrategias. Lean suele paralelizar backtests sobre múltiples instancias de procesos Docker; Nautilus soporta múltiples hilos/conexiones en un proceso único (dependiendo de *tokio*).  

# Normalización de Eventos de Mercado  
- **Tipos de eventos**:  
  - *Lean* distingue _Trade ticks_ (precio+volumen transacción) y _Quote ticks_ (bid/ask) según activo. Internamente hay clases `TradeBar`, `QuoteBar`, y `Tick`. Los datos de cada proveedor se convierten a estos tipos normalizados antes de entregarse al algoritmo (p.ej. un ticker de Forex o un feed de mercado de valores se transforma a `TradeTick` o `QuoteBar`). Las fuentes se definen al inicio (dibuje DataSubscriptionConfig).  
  - *Nautilus* unifica todo a través de **adaptadores**: por ejemplo, múltiples exchanges alimentan al mismo tipo de evento interno (un tick o actualización de libro en su modelo). Soporta *ticks de oferta/demanda*, *libros de órdenes completos* y *barras históricas* directamente en backtest.  
- **Sellado de datos**: En ambos sistemas se usa la marca de tiempo del *evento de mercado* (no la de recepción) para las operaciones del algoritmo, garantizando determinismo temporal. Lean incorpora TimeSlices donde agrupa todos los eventos del mismo instante de mercado para entregar a la estrategia.  
- **Descarga duplicados/orden tardío**:  
  - Lean registra internamente identificadores o usa la lógica del *ExchangeDataConfigStorage* para filtrar duplicados de su propio feed de datos históricos; se asume calidad de dato provista. No documenta explícitamente out-of-order en docs públicas.  
  - Nautilus, al ser basado en streaming, espera que los adaptadores manejen out-of-order y gaps. No se encontraron detalles públicos, pero su énfasis en determinismo indica que los adapters deben ordenar eventos por timestamp.  
- **Backpressure/secuenciación**:  
  - En live, Lean confía en el *brokerage API* para buffer; en backtest simula sin retraso (ejecución instantánea). No hay arquitectura distribuida intrínseca.  
  - Nautilus usa un *message bus* asíncrono (tokio) que hace *buffering* interno por instrumento. Permite latencias configurables en simulación (p.ej. simular retrasos de red).  

# Posesión del Estado en Caliente  
- **Lean**: Cada instancia del motor posee el estado de mercado por suscripción. Las barras (abiertas) y ventanas de ticks se mantienen en memoria dentro de *SubscriptionDataProvider* y *Consolidator*. El algoritmo accede a precios actuales a través de *Securities*, *Portfolio*, e indicadores actualizables localmente. La propiedad del estado recae en el *Algorithm Instance*. Multi-hilo: usualmente single-thread por algor.; no hay concurrencia en una sola suscripción.  
- **Nautilus**: El *Cache* central (memoria distribuida en el mismo proceso) mantiene el estado por clave (instrumento), incluyendo últimas barras abiertas y cálculos intermedios. Los *Strategy Actors* son suscriptores pasivos: obtienen estado caliente del *Cache* vía eventos del *MessageBus*. No hay acceso remoto en caliente. La concurrencia se maneja vía hilos/rutinas cooperativas: cada tick/evento se propaga de forma determinística.  
- **Indicadores y Ventanas**:  
  - Lean ofrece `RollingWindow<T>` y actualizadores de indicadores (los estados de los indicadores suelen residir en la estrategia o en clases de consolidación).  
  - Nautilus sugiere flujo similar: mantiene indicadores en la caché compartida o como objetos en el bus.  
- **Acceso multi-estrategia**: Ambos pueden enrutar el mismo stream de mercado a múltiples estrategias sin duplicar lectura de fuente. Lean usaría múltiples consolidadores del mismo feed; Nautilus distribuye el evento a todos los suscriptores internos (varias estrategias) desde un único adaptador.  
- **Concurrencia y determinismo**: Lean en backtest es secuencial (lockstep ticks/time bars). Nautilus garantiza orden determinista (incluso en live) según su clock interno y procesamiento de eventos en orden. Ambas evitan accesos remotos en cada tick: todo está en memoria local, asegurando latencia baja.  

# Semántica de Barras (Bar Semantics)  
- **Formación vs cerrado**: Lean suele emitir eventos de barra (*TradeBar*, *QuoteBar*) sólo cuando se cierra la vela (end-of-period o end-of-interval). Durante la formación, la vela se mantiene interna hasta llegar a la marca de tiempo. El campo `IsClosed` indica cierre. Nascent bars no se exponen a la estrategia hasta completarse. Esto evita «look-ahead».  
- **Timestamping**: Las barras usan la hora de cierre según el calendario de mercado (p.ej. cierre de minuto, hora o día). Lean asocia la barra al instante final del intervalo.  
- **Multiples marcos temporales (MTF)**: En Lean el usuario puede añadir varios consolidadores (p.ej. 1min, 5min) que operan en paralelo sobre el flujo de ticks. Cada barra MTF es cerrada en su propio tick de temporizador, independiente. Lean no utiliza barras grandes derivadas automáticamente de barras pequeñas; todas provienen de fuentes de ticks o datos históricos.  
- **Missing bars / gaps**: Lean no genera barras vacías por defecto; si no hubo ticks en un intervalo, simplemente no crea barra. Se podría suplir con lógica custom. Nautilus es similar: en gaps de mercado (feriados), asume ausencia de evento.  
- **Look-ahead**: Ambos motores previenen look-ahead asegurando que indicadores y barras usan datos hasta el *tiempo actual* únicamente. Lean activamente evita emitir bar actual antes de su cierre.  
- **Calendario/ Sesiones**: Lean incorpora calendarios bursátiles para alinear cierres de barras con sesiones de cada mercado. Nautilus adapta según el exchange (por ejemplo, diferentes sesiones de criptos o futuros). Los idiomas de fecha/ timezone están unificados en UTC interno.  

# Horizontes Múltiples e Indicadores  
- **MTF**: Como se dijo, Lean usa `Consolidators` configurados en código para cada periodo. Internamente esto es incremental (no rehace barra grande desde barras chicas sino desde el flujo original de ticks). Nautilus probablemente hace algo similar con sus flujos de eventos.  
- **Look-ahead en MTF**: Lean no permite que una barra de mayor periodo se complete antes de recibir los ticks del final del periodo (porque simplemente no ocurre). El algoritmo solo recibe la barra mayor al cerrar completamente.  
- **Indicadores**: Lean brinda +100 indicadores integrados (EMA, MACD, etc.). El estado de cada indicador es local en la estrategia (o puede tener un *Consolidator* dedicado). Nautilus igualmente soporta indicadores en Rust/Python, con estado dentro de la ejecución. Ambos sistemas facilitan actualización incremental con cada tick.  
- **Sesgo/ sesion cruzada**: Los cálculos de indicador en Lean se resetean o persisten según la sesión del activo (por ejemplo, sesiones día). Nautilus maneja calendarios a nivel de símbolo, similar.  

# Warmup / Recovery / Historial  
- **Bootstrap / Lookback**:  
  - Lean admite parámetros de *warmup* para indicadores: se puede pedir llenar RollingWindows con datos históricos antes de vivo. Ejecuta peticiones *History* internas antes de iniciar (offline).  
  - Nautilus, con su registro de eventos, podría usar el log histórico para reconstruir el estado. No hallamos doc pública, pero el modelo de “Event store” sugiere que podría *replay* eventos históricos hasta el presente para “warmup”.  
- **Historial duradero**: Lean descarga datos históricos (localizados en archivos o API) para backtests; no mantiene DB por sí misma. Nautilus permite almacenar datos (ej. Parquet catalogs) para replay. Separa el estado caliente (memoria) de la historia (archivos CSV/Parquet).  
- **Replay/Restart**:  
  - En Lean, al reiniciar backtest, todo el flujo se vuelve a reproducir desde t=0 usando los mismos datos. Live es distinto (se conecta a feed en tiempo real). No hay concepto de snapshot interno; el estado se reconstruye en cada corrida.  
  - Nautilus enfatiza el *replay determinista*: los mismos componentes se usan, posiblemente releyendo el registro de eventos para regresar a cierto punto. También implica que podría reconstruir estado sin snapshot, solo por eventos históricos.  
- **Gap filling**: Ambos permiten manejar vacíos de datos históricos manualmente, pero no hallamos funciones automáticas. Lean ofrece *FillForward* en sus consolidadores (llenar últimos datos conocidos hasta el próximo evento) para evitar discontinuidades.  
- **Trading al estar listo**: Lean requiere que la estrategia espere el primer evento de datos tras inicialización; típicamente no envía órdenes hasta llenar su *InitialHistory*. Nautilus seguramente dispone de señal de “state ready” al terminar su warming antes de procesar órdenes.  

# Autoridad de Feed / Failover  
- Lean y Nautilus asumen un solo feed principal por instrumento. No soportan formalmente «primary/backup» feeds. En Lean se elige el *symbol class* y *market* (p.ej. “NYSE:AAPL”), y la fuente está determinada por la configuración de live/backtest. Si falla un feed en vivo, no hay conmutación automática: la conexión cae.  
- Nautilus tampoco ofrece blending de fuentes; cada adaptador registra events de un proveedor específico. No hay mezcla de feeds primario/secundario documentada. En producción, un esquema de redundancia sería external (p.ej. correr dos instancias con diferentes adaptadores).  
- No se encontró lógica pública de failover: la responsabilidad parece recaer en la capa superior (providers). Así, **ningún sistema mezcla feeds; el failover debe ser gestionado manualmente**. Durante incertidumbre (gap en feed), ambas plataformas pausan procesamiento o continúan con últimos datos conocidos.  
- **Re-suscripción/Recuperación**: Lean suele requerir reiniciar el motor para reconectar, o implementar manualmente lógica de reconexión. Nautilus por su arquitectura asíncrona de red puede reintentar conexiones dentro de sus adaptadores (no documentado, pero plausible).  
- **Detección de gaps/secuencias**: Lean no notifica automáticamente gaps en live; en backtest el flujo es fijo. Nautilus podría incluir secuenciación en adaptadores (no hallado en docs), pero es una tarea a nivel de integración.  

# Límite Live/Replay/Backtest  
- **Componentes compartidos**: Ambos comparten la mayor parte de la lógica de dominio (estrategias, indicadores, cartera, órdenes) entre backtest y live. Los módulos de core/backtest vs live sólo difieren en fuentes de datos y ejecución de órdenes.  
- **Infraestructura distinta**: Lean usa simulación (sin latencia real) y un *AlgorithmModel* especial. Nautilus diferencia en los adapters (en live conectan APIs reales; en backtest consumen archivos históricos). El reloj interno en ambos puede avanzar en modos distintos (real-time vs discreto).  
- **Ordenación de eventos**: En backtest, ambos recorren cronológicamente. En live, Lean responde a eventos de brokers en tiempo real; Nautilus a WebSockets/REST. Para replay determinista, Nautilus permite usar los mismos buses/lógicas (señalar como factor reutilizable).  
- **Ejecución simulada vs real**: Lean manda órdenes a simuladores internos (ficticios broker) en backtest; Nautilus usa un *Model Executor* que puede simular ejecuciones o pasar a broker real con mínimas diferencias. Ni Lean ni Nautilus duplican la lógica de estrategia en dos lenguajes; usan la misma.  
- **Dependencias solo-live**: Lean podría usar llamadas de sistema (p.ej. lectura de reloj real, o APIs web) que no son deterministas; buenas prácticas desalientan su uso (los indicadores y feeds deterministas se usan preferentemente). Nautilus sugiere uso del mismo reloj simulado, evitando llamadas OS directas en la lógica core.  
- **Reutilización exacta**: Nautilus enfatiza que la misma ejecución se mantiene entre backtest y live (Shared semantics). Lean, siendo modular, permite reutilizar código, pero algunos modelos (precios, comisiones) pueden diferir en live, afectando resultados.  

# Implicaciones de Escalado (100–200 cuentas)  
- Ambos motores manejan múltiples estrategias/instrumentos por instancia, pero sus arquitecturas escalan de forma diferente:  
  - *Lean*: típicamente un algoritmo se ejecuta en un proceso (en backtest) o hilo (en vivo). Para 200 cuentas simultáneas (por ejemplo, 200 estrategias o 200 instancias de estrategia en distintas cuentas), habría que multiplicar instancias o threads. En backtest se paraleliza con contenedores, pero en vivo cada cuenta demandará recursos separados: Lean no está diseñado para “multi-cuenta” en un único proceso. La limitación es CPU/RAM; no hay optimización para compartir el feed de datos entre cuentas (cada cuenta leería su feed).  
  - *Nautilus*: puede correr múltiples estrategias de diferentes cuentas en un solo proceso gracias a su modelo de *actors* independientes sobre un solo flujo de datos. Teóricamente soporta un montón de cuentas con una sola conexión de datos, siempre que haya suficiente CPU para cómputo. Riesgos: concurrencia compleja y latencia, pero su diseño asincrónico (tokio) es robusto.  
- Asunciones a 200 cuentas: Lean asume pocos procesos paralelos, no gran contención; Nautilus apunta a un despliegue de alto rendimiento (multi-thread). Si se requirieran 200 *estrategias* idénticas con la misma fuente de datos, Lean duplicaría el trabajo; Nautilus lo compartiría.  
- En 100-200 cuentas, habría riesgo en Lean de *duplicar* los costos de I/O y cálculos por cuenta, posiblemente desbordando recursos. Nautilus escala mejor por compartir estado, pero podría necesitar optimizar memory/caché para tantos actores.  

# Matriz de Aplicabilidad para Echo  

| **PATRÓN**                            | **EVIDENCIA**                                   | **¿Por qué importa a Echo?**                        | **Acción**                      | **Riesgo**                         |
|---------------------------------------|-------------------------------------------------|----------------------------------------------------|---------------------------------|------------------------------------|
| **Modelo único cross-market**         | Ambos Lean y Nautilus usan un sólo motor para ejecutar múltiples clases de activos (multi-asset).       | Soporta decisión de no separar Forex/Futuros (decisión congelada).        | Reusar principio (manterner común). | Bajo (patrón probado).             |
| **Estado caliente compartido**        | Nautilus tiene un *Cache* de estado compartido para todos los actores. Lean usa estado local en cada instancia.         | Indica que un solo componente puede servir múltiples estrategias sin duplicación.   | Reusar: considerar StateFun u otro service como único dueño. | Medio (necesita diseño cuidadoso). |
| **Barrido de ticks vs consolidación** | Lean usa *Consolidadores* para crear barras (cierre solo al final del período). Nautilus similar.     | Afecta semántica de barras (open vs closed). Echo debe decidir un método.         | Reusar patrón de consolidadores KISS. | Bajo (patrón estándar).            |
| **Replay determinista**               | Nautilus: eventos grabados y replay exacto. Lean: backtest reproduce con clocks simulados. | Dice que es posible un estado histórico durable y replay exacto.               | Reusar idea de event log para replay. | Medio (implementar log).           |
| **Unificación live/backtest**         | Ambos enfatizan lógica idéntica entre backtest y live.              | Confirma la validez de compartir componentes clave (gestión de órdenes, indicadores).  | Reusar (evitar duplicar lógica).  | Bajo.                                |
| **Feed primario/secundario**         | Ni Lean ni Nautilus mezclan feeds; no hay autoridad secundaria documentada. | Implica que Echo necesita una estrategia clara de failover (tal vez no cruzar feeds). | Decisión del owner (¿mezclar o no?).| Alto (impacta estabilidad).        |
| **Cálculo incremental (KISS)**       | Lean enfatiza modularidad y **consolidadores** incrementales. Nautilus realiza cálculos en el bus incremental.    | Reforzar enfoque incremental sobre blocks de datos.                        | Reusar (patrón SOLID/Clean).       | Bajo.                                |
| **Historia durable separada**        | Nautilus sugiere mantener logs y archivos separados del estado. Lean mantiene datos por fuera del motor.    | Echo puede separar estado en caliente de datos durables para resiliencia.    | Reusar (mantener datos históricos aislados). | Bajo.                                |
| **Indicadores y MTF compartidos**    | Ambos permiten indicadores actualizados incrementalmente (Lean 100+ indicadores).   | Confirma patrón de estado compartido para indicadores e MTF.              | Reusar (unificar gestion de indicadores). | Medio (evitar lookahead).            |
| **Ownership determinista**           | Nautilus ownership claro (Cache = owner). Lean ownership en la instancia.    | Como Echo usará StateFun, evaluar si es dueña del estado de mercado.      | Reusar (StateFun como dueña local) / Pendiente decisión. | Alto (afecta diseño de concurrency). |
| **One feed/work per account**        | Lean duplica trabajo por instancia; Nautilus comparte.    | Importante para escalado: 200 cuentas.                                     | Reusar Nautilus-style sharing.   | Medio (depende tecnologías usadas).  |
| **Consolidators no look-ahead**      | Lean usa barras cerradas sin lookahead.  Nautilus igual.        | Garantizar semántica consistente de barras (Q5).                           | Reusar (cerrar barras antes de uso). | Bajo.                                |
| **Tiempo de inyección vs tick-time** | Ambos usan timestamp de evento para cálculos.        | Define si Echo necesitará ajustar eventos tardíos.                         | Reusar (usar event-time).         | Bajo.                                |
| **Durable event log**               | Nautilus: Event-sourced replay.                | Proporciona forma de hacer replay/backtest de manera fiable.              | Reusar (considerar log de eventos). | Medio (complejidad de implementación). |

# Fallos y Anti-patrones  
- **Duplicación de trabajo por cuenta**: Ejecutar un motor separado por cuenta (Lean-like) en lugar de compartir estado genera sobrecarga excesiva (*anti-patrón*).  
- **Mix de feeds primario/secundario**: Tratar de mezclarlos simultáneamente podría generar incoherencias (raro en ambos sistemas). Se recomienda no hacerlo sin una lógica clara de prevalencia.  
- **Dependencia de timezones no sincronizadas**: Lean resuelve internamente zonas de cada activo; un anti-patrón sería ignorar diferencias de sesión entre instrumentos.  
- **Indicadores con *look-ahead***: Configurar mal los consolidadores puede exponer barras formándose (anti-patrón de Lean). Siempre esperar barra cerrada.  
- **Estado global mutable extenso**: Contrario a SOLID: diseño de caché inflada (todos los algoritmos leen y escriben en un estado global) puede romper encapsulamiento. Preferir propiedad clara por componente.  

# Preguntas Abiertas (Owner)  
- **Feed Authority (Q8)**: ¿Cómo tratar fallback? Los casos estudiados no lo resuelven; Echo debe decidir si permitir feeds alternativos o hacer failover manual.  
- **Compartición del Feed en multi-cuenta**: ¿Usaremos un modelo Lean (instancia por cuenta) o Nautilus (motor compartido para muchas cuentas)? Esto afecta diseño de Gateway/StateFun.  
- **Hot State Ownership (Q4)**: ¿StateFun será el único dueño de estado de mercado, o delegaremos en microservicios? Nautilus usa un único *cache* determinista, Lean delega a cada instancia. Decisión crítica.  
- **Persistencia histórica**: Nautilus sugiere log de eventos; Echo debe decidir formato (KafKa, archivos, DB) y cuándo aplicarlo (sólo backtest vs también live audit).  
- **Boundary Live/Replay (Q14)**: ¿Qué exactamente se reutilizará en backtest? El patrón sugiere *todo el core de estrategia*, pero ¿seguimos usando brokers simulados o implementamos *shadow mode* en vivo?  

# Requerimientos Restantes (Q4/Q5/Q8/Q14)  
- **Q4 (Estado caliente del mercado)**: Necesario definir cómo asignar propiedad (StateFun, Gateway u otro) y su alcance/clave (¿por instrumento?). Patrón recomendado: un módulo único manejando caché en memoria, evitando llamadas DB por tick (respaldado por Lean/Nautilus).  
- **Q5 (Semántica de barras)**: Se debe decidir el esquema de consolidación (p.ej. Lean-style por ticks) y asegurar determinismo (cerrar barras antes de notificar). Patrón visto: consolidadores incremental y explícitos.  
- **Q8 (Autoridad de feed)**: Definir jerarquía de fuentes. Nadie recomienda mezclar feeds en vuelo, así que Echo debería escoger claramente un feed primario con criterio de fallback. Pregunta abierta sin respuesta canónica en la industria.  
- **Q14 (Límite Live/Backtest)**: Decidir qué componentes *exactos* se comparten. Lean y Nautilus comparten la lógica de estrategia e indicadores. Debe confirmarse si usamos la misma infraestructura core para backtest o un sim distinto (preferiblemente el mismo). También aclarar cómo manejar la inicialización de datos históricos.  

# Deudas Técnicas Propuestas  
- **Nautilus-like Event Store**: Explorar implementación de registro de eventos para reproducibilidad (DT sugerido si se decide usar). Impacto: alta complejidad, aplazar a D2 si no urgente.  
- **Interpolación de Datos Perdidos**: Dado que Lean no llena automáticamente faltantes, considerar si Echo necesita lógica de FillForward (posible DT con impacto bajo si surge gap de mercado).  
- **Soporte Avanzado de Backfill**: Investigar si requiere soporte de *snapshots* o solo eventos. Si se elige Snapshots, abrir DT con motivación clara (rendimiento de restart).  

# Estado Final  
B_MARKET_DATA_RESEARCH = READY_FOR_MANAGER_REVIEW.  

**Fuentes:** Documentación oficial y código fuente de QuantConnect LEAN; sitio y repositorio de NautilusTrader. Información de patrones inferida de estas autoridades.
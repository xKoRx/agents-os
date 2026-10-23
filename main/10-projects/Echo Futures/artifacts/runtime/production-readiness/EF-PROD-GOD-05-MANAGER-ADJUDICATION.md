---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures — Runtime Pools]]"
  - "[[EF-PROD-GOD-01-SOURCE-FORENSICS]]"
  - "[[EF-PROD-GOD-02-PRODUCTION-ARCHITECTURE]]"
  - "[[EF-PROD-GOD-03-IMPLEMENTATION-PLAN]]"
  - "[[EF-PROD-GOD-04-CERTIFICATION-AND-RELEASE]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-23"
updated: "2026-10-23"
---

# EF-PROD-GOD-05 — Primary Manager G-DOC Adjudication

## Decisión y alcance

**G-DOC = ACCEPTED_WITH_BINDING_AMENDMENTS**, Primary Manager GPT-6, 2026-10-23.
Se aprueba **opción A como diseño candidato de implementación para DEV/aislamiento**, con las precisiones obligatorias M01–M07 siguientes; no es certificación ni autorización de PROD, SIM u órdenes. Las precisiones de este documento tienen prioridad para EF-PROD sobre las propuestas numéricas o formulaciones ambiguas de EF-PROD-GOD-02/03/04, sin reescribir el paquete original. Los freezes D1–D6/R6, FEFB G3 y F1 siguen vigentes salvo las enmiendas explícitas aquí aceptadas. La opción B es contingencia condicionada, no trabajo autorizado automáticamente.

**Base comprobada:** source xKoRx/echo `feature/ef-runtime-pools@ac0621a1917a9ecbed50b3daed4add1518ffc71d` remoto; cuatro documentos GOD publicados en Agents-OS/master y leídos completos. Contrastados en source: `futuresruntime.EvaluateColdRecovery` sólo coteja pins; `develop/module.yaml` egress Futures sin `deliverySemantic`; `session.EventGate.Observe` marca `seenFills` antes de publicar; `ninjatrader.Adapter.handleExecutions` marca `executionSeen` antes de publicar; `StreamSequencer.Accept` sólo deduplica una ventana bounded; M1 bridge group incluye hostname; `journalfs.SetFenceEpoch` ignora fallas de fsync del directorio. La especificación oficial StateFun 3.2 permite Kafka egress `deliverySemantic: exactly-once`, sujeto al JAR real, checkpoints y transacciones Kafka. **No se ejecutaron tests ni se accedió a infraestructura física durante esta revisión; la RCA exacta del resubmit Flink es evidencia pendiente.**

## Adjudicación de hallazgos

| Finding GOD | Dictamen del Manager | Mandato |
|---|---|---|
| F01 P0 — restauración/ownership | **ACEPTADO** (brecha estática + resubmit sin estado reportado; causa inicial pendiente) | Continuidad de checkpoint+offsets+owners acreditada y bloqueo de fresh-submit vacío |
| F02 P0 — M1/recording | **ACEPTADO** (config egress sin modo explícito; no hay atomicidad causal demostrada) | EXACTLY_ONCE de Flink+egress transaccional real+read_committed, validado contra JAR/config desplegables |
| F03 P0 — fills perdidos | **ACEPTADO** (source marca visto antes de publicación durable) | Inbox/outbox/journal y ACK en orden; observación sin correlación nunca se descarta silenciosamente |
| F04 P1 — horizonte dedup | **ACEPTADO** (ventana 4096; no extrapolar garantía a redelivery remoto) | Cursor/protocolo y old-redelivery fail-closed por lane/stream |
| F05 P1 — persistencia power-loss | **ACEPTADO** (flush/cursor/fence insuficientes) | fsync/atomicidad comprobada; error de storage bloquea |
| F06 P1 — propietario físico | **ACEPTADO** (consumer group hostname no es fence) | Exclusividad binding+generation hasta último salto físico |
| F07 P1 — tiempo/paridad | **ACEPTADO COMO GAP DE CONTRATO** (riesgo respaldado; divergencia física no demostrada) | Tiempo inmutable por transición y recording causal compatible; sin modificar kernels económicos |
| F08 P1 — economía/protección | **ACEPTADO COMO GAP DE AUTORIDAD/EVIDENCIA** (no se afirma ausencia general de protección) | Conectar productor real y readiness; NO-GO por binding si venue/terminal no acredita protección |
| F09 P1 — capacidad/progreso | **ACEPTADO** (fallo compartido y no equivalencia de health/freshness) | Gate de recuperación, observabilidad diferenciada, campaña batched física y evaluación de blast radius |
| F10 P2 — versiones/escala | **DEFERIDO CON INVENTARIO OBLIGATORIO** | Release identity, compatibilidad y vulnerabilidad bloqueante si se demuestra; no upgrade de stack cosmético |

## Enmiendas vinculantes (M01–M07)

**M01 — Flink metadata como autoridad.** RecoveryManifest, registry ETCD, attestation y markers son barreras/proyecciones de control, **nunca una simulación de checkpoint**. El último estado realmente COMPLETED y su metadata de coordenadas/offsets/transacciones debe ser verificable desde Flink y storage independiente. Registry atrasado o logs irrecuperables => no escoger checkpoint por hora/nombre. Una configuración igual de ETCD no concede permiso económico. La RCA E01 puede quedar UNRESOLVED si la prevención verificable cubre los failure modes; NO atribuirla a HTTP timeouts sin logs.

**M02 — M1 y latencia.** Implementar egress EXACTLY_ONCE con el schema real soportado por StateFun 3.2 y JAR efectivo, consumidor read_committed e integración real con checkpoints; mantener M2 y reconciliación venue porque no hay atomicidad Flink↔PostgreSQL↔broker. **Los números propuestos en GOD (§5 checkpoint interval 1 s, p99≤1 s, age≤5 s, p99 E2E≤5 s, CPU/RAM headroom, RTO≤15 min) son objetivos iniciales de commissioning y pruebas de factibilidad, NO valores garantizados del hardware ni obligaciones congeladas por su sola aceptación documental.** Registrar latencia/throughput/freshness y ValidUntil de la estrategia; adjudicar un envelope final por pruebas y requisitos económicos reales antes de G-CERT, sin debilitar EXACTLY_ONCE, freshness=30 s vigente, ni protecciones para dar PASS. Si la combinación de transacciones/recovery no permite operar de forma segura, NO-GO y evaluación de opción B o menor scope físico, no at-least-once encubierto.

**M03 — FX compartido y operación existente.** A sólo es elegible si el scope concreto de DEV/PROD preserva FX y se puede demostrar su coexistencia/gestión segura en el job compartido. No modificar clientes MT4/MT5, apagar cuentas FX ni tocar PROD automáticamente para pasar Futures. Extensión mecánica FX sólo en ramas/superficies autorizadas, con regresiones y despliegue propio; si FX necesita nueva exposición no compatible con fencing/gate de A, bloquear la promoción compartida y proponer B con migración explícita, sin ejecutar B por cuenta propia. El operador/Owner decide la ventana física; ninguna certificación Futures implica armar FX.

**M04 — Protección física y economía.** Conectar sólo feeds contables legítimos y conservar fórmulas Provider/MM. Una capacidad de protección persistente debe demostrarse en API+venue+cuenta reales, antes de GO de ese binding. Nunca fabricar bracket/OCO sintético, fill, fees o ledger para satisfacer aceptación; falta de capability => ese binding NO-GO sin bloquear el cierre de código con fail-closed comprobado. Una posición plana no prueba ausencia de órdenes/ejecuciones pendientes.

**M05 — No multiplicar infraestructura.** RuntimeControl es utilidad acotada del despliegue EXISTENTE, no daemon/orquestador aparte. Reutilizar Flink recovery APIs, ETCD CAS, journalfs M2, SDK y PG existentes. No introducir un segundo bus, nueva base por tick, migración backtester/Lab, sharding de un owner o un nuevo money manager. Markers por owner deben mantener costos de estado acotados; pruebas de restore/roster compatibles con StateFun real. Si el JAR no permite inspeccionar un campo pretendido, usar attestation nativa y manifest externo verificable o mantener BLOCKED: no crear evidencia ficticia.

**M06 — Capas y fuente de verdad.** Distintas garantías y gates: (a) source/unit/Go SDK; (b) StateFun+Kafka transacciones reales aislados; (c) C# compilado+NT/relay/feed real; (d) M2+venue SIM; (e) PROD por cuenta/entitlement. PASS inferior no sustituye superior. Sólo el Owner puede instalar/reiniciar terminal con perfil sensible y autorizar armamento Sim101/PROD; GLM no genera permisos ni resuelve cuenta comercial por ID histórico.

**M07 — Concurrencia, integración y cierre.** El repo producto comparte la rama con The Lab V4: refrescar HEAD al inicio, worktrees aislados, ownership sin solapamiento y FF sin force sobre SHAs acordados; no reset/rebase de cambios ajenos. B1→B2→B3 son **bloques internos de UNA implementación GLM**, no shots nuevos para reclamar autorización por defectos menores. Mantener un único dictamen adversarial consolidado y un G-IMPL de Manager. Cambios fuera del freeze se informan juntos; peligro P0 no justifica ejecutar nada físico sin autorización.

## Ejecución autorizada y gates

**PRD.2 — AUTORIZADO para GLM LOCAL como implementación de producto y pruebas en entornos AISLADOS, no sobre servicios compartidos ni cuentas físicas.** Un Submanager único coordina B1→B2→B3 y especialistas ONE-SHOT, con contrato y frontera de archivos, devolviendo hallazgos al dueño dentro del mismo encargo. No habilita modificación ni despliegue automático de servicios DEV compartidos, PRODUCTION ni NinjaTrader. PRD.3, G-IMPL y certificación física siguen pendientes. El producto debe terminar en candidato inmutable, con evidence index y recursos/roles identificados; se aceptará sólo tras verificación independiente y dictamen Manager.

**Ruta de entrega:** G-DOC accepted → B1 recovery/M1/owner → B2 durable observations/time/market/economics → B3 integración y QA in-proc/aislada → G-IMPL review del Manager → G-ENV/G-FEED/G-REC → autorización SIM Owner → PROD Owner explícito. No S4 FEFB, no nueva arquitectura GOD.

**STOP:** cero deploy, órdenes y promoción con este gate documental. El F1 LIVE DEV existente no acredita restauración ni capacidad de la ruta NT nueva.

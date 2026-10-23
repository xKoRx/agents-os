---
type: doc
schema_version: 1
status: draft
area: "[[Echo]]"
related: ["[[Echo Futures — Runtime Pools]]", "[[EF-PROD-GOD-01-SOURCE-FORENSICS]]", "[[EF-PROD-GOD-02-PRODUCTION-ARCHITECTURE]]", "[[EF-PROD-GOD-03-IMPLEMENTATION-PLAN]]"]
aliases: []
tags:
  - kind/doc
created: "2026-10-23"
updated: "2026-10-23"
---

# EF-PROD-GOD-04-CERTIFICATION-AND-RELEASE

## Propósito

Definir aceptación, certificación física, release y recuperación del diseño EF-PROD-GOD-01. **Todas las pruebas de este documento son futuras: NOT_RUN en esta sesión.** La aceptación documental o del código no constituye CERT-NT-01 PASS, permiso SIM ni activación LIVE. El planificador único y su historial permanecen en [[Echo Futures — Runtime Pools]].

## Contenido

### 1. Qué puede aprobar cada gate

| Gate | Responsable | Entrada | Salida permitida |
|---|---|---|---|
| G-DOC | Primary Manager | Cuatro documentos, source baseline, findings y contratos | Diseño accepted o correcciones específicas; ninguna mutación operacional |
| G-IMPL | Primary Manager sobre verificador independiente | SHA consolidado B1–B3, repros y compatibilidad | Código listo para certificación; no cuenta armada |
| G-ENV | Responsable operacional autorizado | Scope, single owner, imágenes/almacenamiento/secret refs/cuentas, backup y rollback | Entorno de certificación permitido y aislado |
| G-FEED | Certificador técnico bajo autorización Owner de terminal | Instalación y perfil reales, C3 feed-only, C2 | Feed/batching/continuidad acreditados para envelope concreto |
| G-REC | Certificador técnico independiente | Runtime real aislado + recovery manifest | Recovery correcto o fail-closed demostrado |
| G-SIM | Owner autoriza; Submanager ejecuta; verificador adjudica evidencia | G-IMPL/G-ENV/G-FEED/G-REC, identidad Sim101 vigente | Ejecución SIM acotada verificada; vuelve desarmado |
| G-PROD | Owner explícito + Manager técnico | Todas las matrices y requisitos venue/account concretos | Promoción de scope exacto; nunca autorización genérica de cuentas |

La numeración C0–C6 de CERT-NT-01 conserva sus significados históricos y cada reporte fecha su corte. Mapeo de continuidad: C3 instalación/validación feed-only → G-ENV/G-FEED; C2 capacidad/freshness → G-FEED; C4 físico/recovery → G-REC/G-SIM según si requiere órdenes; C5 armado Sim101 exige autorización aparte. Este paquete no vuelve a ejecutar ni reabre fases de desarrollo FEFB; añade criterios de producción en el mismo ledger.

### 2. Preflight de una campaña física futura

El operador identifica deployment y ambiente Echo DEV/PROD según contrato vigente; no usar PROD porque DEV no esté disponible. Una prueba de fallo nunca se ejecuta sobre FX/cuentas compartidas sin autorización específica y plan de protección. Entorno aislado significa topics/groups/prefijos/puertos/M2/terminal de pruebas identificados, ausencia de consumidores ajenos y prueba negativa de no-interferencia; no sólo un flag ENV.

Registrar SHA source completo y remoto, hashes de binarios/assembly cargados, image/JAR, module efectivo, flink-conf efectivo, fingerprint del snapshot ETCD sin secretos, UID/ValueSpec map y config de Kafka/RF/minISR/retention/transactions. Si diverge del release, STOP antes del primer evento económico. El bundle mixto Core ac0621a1/gateway+relay 2ee61791 es historia reportada; el futuro release declara sus binarios individualmente, no finge un SHA homogéneo.

Registrar catálogo de cuenta en terminal: ambiente, provider ref, canonical execution ID, physical binding, terminal/profile, Account.Name y Account.Id, connection/entitlement; sólo Sim101 para la certificación autorizada actual. Token se verifica localmente, nunca se publica. Buscar aliases que apunten a la misma cuenta y bindings comerciales activos; cualquier ambigüedad detiene armado. No asumir ID 2. Una captura “Sim101” sin binding completo es insuficiente.

Antes de fallos: snapshot M2/outboxes/manifest, baseline de posiciones/órdenes/fills/reservas, medios de reconciliación/historia y prueba de rollback en aislamiento. Definir abort conditions, duración, límites de órdenes SIM y operador de terminal disponible. No reiniciar NT si puede afectar posiciones ajenas. En feed-only los negativos son explícitos: sin permiso ejecución, sin listener armado ni keys de cuentas autorizantes, asociación disabled y ausencia de órdenes atribuibles al ensayo. La autorización feed-only no incluye “smoke” de órdenes.

### 3. Matriz de aceptación funcional y técnica

`L1` reducer/serialización; `L2` handler StateFun Go real; `L3` Kafka + StateFun Java reales aislados; `L4` NT/Bridge físicos; `L5` SIM venue; `L6` cuenta/proveedor de destino bajo futura autorización. PASS de capa inferior no satisface capa superior. Cada prueba registra estado inicial/final, identidades, hashes y frontier, no sólo exit code.

| ID / findings | Estímulo futuro | Oráculo y criterio preciso | Capa mínima |
|---|---|---|---|
| REC-01 / F01 | Restart Core con request in-flight, mismo job | Mismo lineage/run/owner identity; state_seq no vuelve a cero, offsets restaurados coherentes, ningún bootstrap vacío; efectos confirmados conservados | L3 |
| REC-02 / F01 | Matar TM y JM separadamente | Restore del último checkpoint COMPLETED y mismo roster; M1 visible y M2 concilian; permisos invalidan expansión durante incertidumbre | L3 |
| REC-03 / F01 | Agotar restart strategy / contenedor nuevo | RuntimeControl usa restore explícito compatible; si no hay candidato queda BLOCKED, nunca startupPosition como recuperación | L3 |
| REC-04 / F01 | Borrar sólo copia aislada de checkpoint, falsificar pin igual, dejar prior ausente | No state initialization de owners históricos, no comandos expansivos ni rearm; razón COLD_RECOVERY_REQUIRED | L2+L3 |
| REC-05 / F01 | Job vacío nuevo mientras Core anterior sigue vivo | Watchdog identifica generation/JobID distinto, permiso expira ≤TTL aprobado, NT rechaza comando anterior; ningún OPEN posterior al fence/expiry | L3+L4 |
| REC-06 / F01/F10 | Cambiar UID, ValueSpec/type, key encoding o maxParallelism incompatible | Rechazo explícito, ningún allowNonRestoredState, snapshot anterior preservado; migración compatible mantiene hash semántico | L3 |
| REC-07 / F01/F05 | Power loss de entorno aislado equivalente | Snapshot, registry y M2 íntegros o BLOCKED; no bootstrap por file missing; recuperar posiciones/órdenes reales de scope | L3+L4 |
| KAF-01 / F02 | Crash antes de respuesta HTTP, antes/después de checkpoint y commit Kafka | Read_committed no ve tx abortadas; decisiones/IDs ya visibles no divergen del estado recuperado; una intención física efectiva | L3, L5 para efecto |
| KAF-02 / F02 | Caída broker/líder/ISR, ACK perdido | Sin ack de publicación no se retira outbox; orden por stream preservado; RF/minISR efectivos; no silent loss tras failover | L3+L4 |
| KAF-03 / F01/F04 | Low watermark supera offset de snapshot / topic recreado | Recovery bloqueado con gap exacto; ningún auto-offset-reset ni earliest/latest para ocultarlo | L3 |
| SEQ-01 / F04 | 4097+ identidades, reentrega primera, reagrupamiento 1/2/50/1001, epoch viejo | No nueva stream_seq/Signal por identidad expirada; old-redelivery explícita; mismos hechos dentro de ventana comparan digest | L1+L2+L3 |
| SEQ-02 / F04 | Multi-stream interleaved, gap real, revisions tardías | Cursores por stream evitan falso gap; gap real bloquea decisiones dependientes, backfill/revisión no crea trade retrospectivo | L2+L4 |
| OBS-01 / F03 | Kafka falla después de callback/dedup antes de publish | Fill queda pending durable; vuelve a publicarse mismo ID/payload; una sola aplicación contable; ninguna pérdida por seenFills/executionSeen | L2+L3+L4 |
| OBS-02 / F03 | Crash tras publicación antes de marca published y tras terminal de orden | Redelivery idempotente; command terminal no borra fill pending; covers-through comprobable | L3+L4 |
| OBS-03 / F03 | Mismo execution_id contenido distinto, correlación ausente | Conflicto/quarantine durable con scope; cuenta UNKNOWN; no sumas dobles de ObservedFilledQty ni synthetic fills | L1+L3+L5 |
| DISK-01 / F05 | Corte append/cursor/identity/compaction; ENOSPC y fsync failure | Frame/cursor íntegro previo o nuevo, no cursor por delante del dato; error degrada readiness; tail incierto/GAP visible | L4 filesystem equivalente |
| OWN-01 / F06 | Dos hosts/groups/lanes para misma cuenta; viejo revive | Segundo propietario no manda; fence generation persistido rechaza viejo, incluido comando ya leído; takeover sin old-fence prohibido | L3+L4 |
| OWN-02 / F06 | Account.Id drift, Name/ref distintos, alias doble, SIM token en LIVE | Cero órdenes; motivo por identidad exacta; ninguna selección de fallback | L4 |
| TIME-01 / F07 | Clock atrás/adelante, retry, timer duplicado y expiración en backlog | RuntimeTs por owner no retrocede, una transición ve un instante; expiry impide expansión; timer obsoleto no se repite | L1+L2+L3 |
| PAR-01 / F07 | LIVE grabado y EXACT_REPLAY con mismos inputs/contextos | Hashes de decisiones/Signal/commands/state equivalentes por owner/causal frontier, sin wall-clock ni lookahead; omisión de contexto devuelve INCOMPLETE | L2+L3 |
| DAY-01 / F07/F08 | Sesión overnight, DST, feriado, reconnect en boundary, DD latched | Account-day por calendario/RuleSet; sin reset de breach por clock; policy se reanuda sólo con hecho válido | L1+L3+L5 en boundary real |
| ECON-01 / F08 | Partial fill, fees, comisión tardía, correction y snapshot atrasado | Ledger revision única/digest/covers-through; Provider no autoriza con autoridad faltante; posición independiente no crea PnL ficticio | L3+L5 |
| ORD-01 / F03/F08 | Submit/ACK incierto, cancel-fill, replace parcial, fill después de release | Misma identidad, AMBIGUOUS no retry ciego, reserva conserva outstanding, late fill original refuta drain y bloquea sucesora | L2+L5 |
| PROT-01 / F08 | Caída Core/Kafka/Bridge/NT en cada frontera entry→partial fill→stop | Protección exigida por plan permanece confirmada y no genera reversión; si no se demuestra, NO_GO_PROD del binding | L5; L6 para custodia/historia real |
| POOL-01 / F08 | Claims concurrentes entre pools, pause/day return con órdenes vivas | Una activa por asociación, una autoridad por cuenta, afinidad intacta, sin release por timeout y sin parar Strategy | L2+L3; multicuenta física separada |
| FEED-01 / F09 | Terminal integrado ALL/50ms/NATIVE | Frame/header/config aplicada coinciden con Kafka y owner; todos los items admitidos reconciliados por identidad, un productor, ninguna barra sustituida por agregado | L4 |
| FEED-02 / F09 | NACK/backpressure/outbox full/ACK perdido/restart NT | ACK control no retira; cursor datos sólo prefijo publicado; pendientes durables regresan en orden; gaps no recuperables declarados | L4 |
| FEED-03 / F09 | Corte conexión del terminal, silencio fuera de pausa y reopen | STALE/UNKNOWN según evidencia, permiso expira, backfill/cobertura antes de readiness; heartbeat no rejuvenece quote | L4 |
| PERF-01 / F09 | 1×/2×, burst capturado, backlog con arrivals continuas, estado maduro | Envelope §4, lag no creciente a 1×, 2× headroom, drain medido, edad real, tx/checkpoint incluidos, sin pérdidas | L3+L4 |
| SCALE-01 / F09 | 1/100/200 deliveries sobre misma Signal | Una evaluación Strategy/analytics y suscripción por stream; costo account-scoped; caps conservan state vivo | L2+L3 |
| POISON-01 / F09 | Payload inválido repetido / config incompatible | Rechazo durable y scope bloqueado; no fresh job, no retry storm ilimitada ni descarte de economía; resto progresa según aislamiento | L3 |
| FX-01 / F01/F02/F09 | Restore/deploy compartido y replay controlado FX aislado | Offsets/IDs conservados; exact duplicate no cambia journal; conflicto real visible; no nueva ejecución durante estado incierto | L3, L4 legacy según adapter |
| OPS-01 / F09 | OTEL caído, /health200 con STALE, checkpoint viejo, lease perdido | Cuatro dimensiones no colapsadas; new-risk no depende de exporter; alertas/evidencia recuperables; falta de evidencia bloquea certificación | L3+L4 |
| ROL-01 / F01/F10 | Upgrade y rollback antes/después de efecto | Compatibilidad probada, no retroceso de generation ni pérdida de acción; después de efecto usar estado compatible/forward repair | L3+L5 |

Los ataques destructivos a storage usan copias/VMs de ensayo autorizadas, nunca backup único ni cuenta del Owner. Para cada punto ambiguo se inyecta fallo inmediatamente antes y después de la escritura/ACK que cambia autoridad. Power-loss no se demuestra sólo con kill de un proceso; ambos escenarios se registran por separado.

### 4. Protocolo de capacidad y continuidad

Fijar antes de medir: dataset/captura RTH y su hash, instrumento/contrato/TFs, calendario, perfil ALL/NATIVE, source/consumer mode, cuentas/pools, estado maduro, hardware/límites, background load, versions, configuración checkpoint y Kafka. No sacar sweeps de coverage simultáneos para luego comparar sin declarar contención. La carga de producción declarada sí se reproduce; no matar procesos ajenos para “estabilizar” medición.

Campañas futuras: (a) 30 min mínimos de peak vivo sin reinicios/timeouts, (b) una sesión completa para crecimiento/boundaries, (c) replay open-loop aislado 2× del peak representativo y bursts capturados, (d) backlog preexistente + ingreso continuo hasta drenaje, (e) recuperación después de stall/restart. Mantener singleton de compatibilidad en ensayo separado, sin contaminar autoridad del stream batched. No usar su throughput como techo FEFB.

**Criterios propuestos de A, congelados para el ensayo tras G-DOC:** μ≥2λ a carga de headroom; backlog slope≤0 en steady 1×; cero pérdida silenciosa/identidad conflictiva; capturados=publicados+pending+rechazados durables con razón; ningún reject/gap esperado en camino nominal ALL. Freshness 30 s/default como límite de seguridad, p99 received→canonical≤1 s y máximo normal≤5 s como presupuesto operativo. Decisión→M1 committed p99≤2 s; extremo a extremo p99≤5 s y siempre compatible con validez/protección del plan. Cualquier estado STALE bloquea expansión aun si el promedio cumple.

Checkpoints p99≤1 s y edad completed≤5 s en steady; cero checkpoints fallidos durante ventana nominal; restore usa el último committed lineage, no el más cómodo. Registrar interval/min-pause, duration/alignment/async upload/commit y bytes totales/incrementales. CPU steady<60%, peak<80%, RAM<75%, disco libre>30% con retención íntegra son headroom propuesto. Si un límite no se sostiene, evidencia FAIL y tuning permitido dentro del contrato; no cambiar retrospectivamente el umbral para declarar PASS.

Recuperación: objetivo de commissioning `T_detect + T_restore + T_reconcile + T_catchup ≤ 15 min` en el envelope ensayado; no es tiempo para mantener posiciones sin protección. Si no se alcanza, permanece desarmado y se declara RTO real mayor; no GO para un release que prometió ese RTO. Espera de Owner para rearmar se reporta aparte. RPO de intents/fills durables=0 bajo fallos cubiertos; datos de fuente no capturados se representan como gap, no RPO cero ficticio.

Comparar bytes/owner y slope durante sesión: memoria hot crece sólo por streams/TFs/lookback/estado vivo; terminal history se contrae según horizon. Publicar número de reservations/grants vivos, tombstones y pending M2; cap alcanzado no descarta estado económico. Medir GC/compaction/serde y estado RocksDB: sumar CPU/latencia de serialización, no llamar “persistencia a disco por tick” a Storage.Set.

200 cuentas es prueba estructural/capacidad aislada; el release físico lista exactamente cuáles y cuántas se observaron. Sim101 sola no demuestra múltiples cuentas físicas ni límites de conexiones/provider. No contratar un número de símbolos/cuentas que no pasó su envelope.

### 5. Camino físico NT/Bridge/Kafka/Flink

Cadena probatoria mínima para cada muestra: callback o evento de API nativa identificado → outbox frame/lane/data_seq y config aplicada → bytes recibidos por relay → Kafka topic/partition/offset y payload digest → StateFun owner_input_seq/stream_seq/lineage → analytics bar revision/coverage → Strategy Signal y delivery si corresponde → Provider revision/decision → command M1 committed → M2 PREPARED/SUBMITTING → NT account/order/execution IDs → observation outbox → Kafka fact → Operation/ledger final. En feed-only la cadena se detiene antes de orden; los restantes segmentos se prueban después con autorización.

Installation proof: hash de los tres `.cs`, una sola definición cargada, assemblies reales/version NT y perfil aplicado, sin EchoFeedAddOn legacy activo sobre mismo stream. Archivo en staging no es archivo cargado; log “config loaded” no demuestra callback nativo ni batching. Registrar hello/capabilities, ACK control sentinel, versión aplicada, samples market_batch, origen NATIVE y todos los TFs declarados. Feed metadata debe provenir del cliente configurado, no ser inyectada por harness después del relay.

Comparación causal de ALL: no comparar sólo counts si duplicados compensan faltantes; reconciliar IDs/digests/orden y clases. Captura durante outbox full se contabiliza como no admitida/gap; no se presenta como lossless nominal. Sampling LAST exige ensayo independiente, metadatos de omisión y rechazo de consumidores no compatibles. No modificar flush para esconder pérdida de callbacks.

Barras: comprobar golden OHLCV/TF/calendario contra API nativa dentro de cobertura real; min/max updated indexes, backfill superpuesto, primera barra post-reconnect, revisión tardía y cierre diario. Nunca usar la barra calculada por Core como oráculo de la misma barra. Tiempo del terminal y del host se documentan con offset; disponible_at preserva latencia real.

Drills de transporte: falla publicación broker→NACK→stall→outbox lleno→recuperación; ACK de control inesperado cursor alto; ACK perdido; reconectar relay y terminal; caída entre durable-write y send; duplicados anteriores a ventana; múltiples streams sin falso gap. C4 aislado histórico de cliente sintético sirve como regresión, no sustituye estas pruebas del AddOn instalado.

### 6. SIM101 y verificación FX

SIM101 requiere autorización de órdenes acotada del Owner recibida después de preflight. Registrar scope, vencimiento, máximo exposición/órdenes permitido y política de parada; no seleccionar valores por inferencia en este diseño. Ejecutar nominal + partial/cancel-fill/ACK incierto + restore mientras una orden propia está pendiente, según capacidades reales SIM. Confirmar estado final económico: fills, fees simuladas declaradas, balances, reservas, operaciones, órdenes abiertas y posiciones; final FLAT exige evidencia, no sólo retorno de command.

Si no se autorizó un escenario que requiere exposición, marcar NOT_RUN y mantener gate correspondiente. Multiaccount sigue NOT_DEMONSTRATED con una sola Sim101; su simulación en harness no acredita dos bindings físicos. Tests de identidad negativa pueden demostrar rechazo de otra cuenta sin enviarle orden; nunca usar cuenta comercial como “control positivo”.

FX se verifica en baseline equivalente antes y después de cambios compartidos. Inventariar ingresses y consumer groups de reference-events, execution-results, trade-closes, close-results, snapshots/config/position-sync; sellar offsets y estado. Clasificar tormenta de journal por duplicate exacto/open-after-closed/close mismatch/quarantine con hashes y estado final; no asumir benignidad porque una unique key evitó overwrite. Probar fail-closed de expansión durante recovery incierto y preservación de gestión/observaciones legacy. Ningún cambio masivo de earliest/latest, TTL o cleanup Journal se admite como remedio.

En shared runtime, medir FX lag, latencia y error rate durante pico Futures y failure drills aislados. Aceptación exige cero contaminación cruzada de cuentas, cero pérdida de identidad y parada segura conjunta; el error budget de downtime debe quedar firmado en release envelope. Si FX debe permanecer disponible durante una falla total del job Futures, eso activa obligatoriamente B; A no afirma ese aislamiento.

### 7. GO / NO-GO inequívocos

**GO documental:** cuatro documentos completos, source/contratos trazables, decisiones candidatas adjudicadas, gaps con fallback cerrado y plan de ejecución acotado. No necesita fingir RCA ni física faltante. Estado de esta entrega: READY_FOR_MANAGER_REVIEW, no G-DOC accepted.

**GO para instalación feed-only:** G-IMPL de componentes requeridos, entorno permitido, release/hash probado, rollback de NT y cuenta sin afectación ajena; ejecución desarmada. No requiere armar para validar un feed.

**GO SIM:** todos los P0 cerrados, P1 relevantes probados en su capa, recovery y M1 reales, identidad/binding/unique owner, contabilidad/config válidas para escenario, outboxes y NTP sanos, feed fresco/cobertura completa y permiso Owner explícito Sim101. El objetivo es certificar, no obtener ganancias. Final de ventana vuelve DISARMED/gestión segura con inventario residual.

**GO PROD:** además de SIM, envelope real por proveedor/cuenta, reglas y entitlement vigentes, historia/recovery horizon, custodia y persistencia de protección acreditadas, continuidad/restores/rollback demostrados, riesgos residuales aceptados y permiso Owner explícito de cuenta/capital/riesgo/ventana. Las reglas externas del proveedor se verifican en fuentes oficiales actuales durante esa promoción; este documento no las declara vigentes ni legales por inferencia.

**NO-GO inmediato:** cualquier P0 abierto; checkpoint sin lineage/objetos; offsets fuera de retención; state vacío inesperado; double owner; cuenta no acreditada; generation/claim vieja; M1 no transaccional; fill pendiente perdido/conflictivo; protección no demostrada; economía UNKNOWN; feed stale/gap material; clock no confiable; rollback incapaz de conservar efectos; incapacidad de medir el envelope; credenciales/namespace de LIVE en replay; escenario físico obligatorio NOT_RUN. Un P2 sólo puede diferirse si no viola estos invariantes y tiene responsable/trigger documentado.

La falta de E01 no fuerza una RCA inventada: se exige o evidencia del actor original o constancia formal de evidencia irrecuperable con eliminación demostrada de todos los caminos equivalentes de fresh-submit. La aceptación puede cerrar el riesgo prevenible sin afirmar causa histórica confirmada. La falta de E02/E05/E06 para el scope concreto sí bloquea armado/PROD.

### 8. Release por SHA y procedimiento de parada

Preparar release inmutable con hashes por binario/config/assembly, firma o digest del manifest, compatibilidad y rollback. Inventario de permisos: quién puede submit/cancel job, cambiar config, armar cuenta y custodiar secretos. REST Flink no queda abierto a operadores/productores ajenos; endpoint Core sólo invocable por runtime autorizado y tráfico de administración separado. TLS/auth/ACL y secretos de mínimo scope se verifican en entorno, no se asumen por red privada.

Antes del corte: cerrar expansión fuera de Flink, ACK de fence/generation en Bridge/NT, preservar protección, conciliar inflight y obtener snapshot/savepoint válido; productores siguen capturando según outbox/Kafka. Congelar cambios config y registrar frontier. Corte del job coordinado, no rolling ciego. Restaurar con manifest exacto; verificar owners/offsets/economía/M2/venue y catch-up; nueva checkpoint completa; READY_DISARMED. Owner concede nuevo permiso sólo después de ver evidencia y scope.

Parada programada: impedir entradas → resolver pendientes conforme a MM/Provider autorizado → verificar protección o cierre real de posiciones → confirmar estado final y M2 sin ambigüedad → checkpoint/savepoint → detener componentes no necesarios. No interpretar STOP como cancelar toda orden protectora. Si quedan posiciones protegidas overnight bajo reglas vigentes, documentar custodio y continuidad; no apagarlas por conveniencia del deploy.

Rollback previo a efectos vuelve binario/snapshot compatibles. Posterior a efecto usa estado actualizado, jamás snapshot anterior sin reconciliación y reconstrucción causal aprobada. Abort de la campaña conserva evidencia y deja new-risk cerrado; no intenta “volver a RUNNING” sembrando job nuevo.

### 9. Disaster recovery e incident response

1. Detectar y registrar UTC, JobID/generation, fuente/config, última checkpoint completada y fronteras Kafka/M2; cerrar expansión con permiso/fence independiente. Mantener gestión segura disponible cuando haya autoridad.
2. Preservar logs JM/TM/Core/Bridge/NT, eventos container/orchestrator, configuración efectiva y manifests; snapshots de evidencia read-only sin secretos. No reiniciar repetidamente borrando el primer error.
3. Clasificar: transitorio recuperable con mismo estado; terminal con candidato compatible; estado/offset/historia perdido; cuenta física incierta. Ejecutar únicamente la rama autorizada de recovery.
4. Verificar storage de checkpoints/HA, Kafka y ETCD antes de Core; M2 y outbox antes de conectar ejecución; historia y snapshot de cuenta antes de readiness. Boot del host no implica boot económico.
5. Si todo el host de Flink se pierde, recuperar en reemplazo sólo después de cercar el anterior; restore desde almacenamiento independiente, mismos IDs/offsets. Si se pierde M2, usar backup + historia exacta con autorización; sin native IDs/horizon no resubmit y cuenta BLOCKED.
6. Conciliar todas las posiciones/órdenes/fills, reservas, claims, fences, config, daily state y causal frontier. No liberar cuenta por neto cero ni aceptar lectura “flat” sin cobertura temporal del venue.
7. Registrar RTO/RPO reales, gaps y evidencia irrecuperable. Volver READY_DISARMED; rearm explícito. Postmortem separa causa, factores y acciones, nunca infiere éxito desde health.

Backups: manifests y objetos dependientes completos, M2/outboxes y registry; copias fuera del host fallido con políticas de acceso/retención; ensayo de restore desde copia, no sólo checksum local. Generation/fence no retrocede al restaurar ETCD desde backup; contrastar máximo con manifest/M2/terminal y mantener bloqueado si no puede demostrarse. Quorum/almacenamiento que comparte dominio eléctrico sigue siendo residual documentado.

### 10. Evidencia mínima y readback

Paquete por campaña con `release-manifest`, `effective-runtime-manifest`, `recovery-inventory`, `account-readiness-evidence`, `capacity-envelope`, timeline UTC, matriz de escenarios y evidence index con hashes. Estado PRE/POST de cinco capas de desarme, posiciones/órdenes/fills, M2 pending/ambiguous, Kafka offsets/transactions y checkpoints. Guardar logs crudos fuera del vault con referencia segura; en Agents-OS resultados, hashes y enlaces durables. Si un raw se pierde, declarar cuál y qué conclusión queda sin prueba.

Para PASS físico, el verificador contrasta terminal→broker→StateFun→Core→M2 de la misma campaña/source/config. La lectura read-only de logs históricos de esta sesión no es recertificación. Un smoke con JSON fabricado o fixtures que inyectan hechos contables no prueba wiring productivo. Un test rojo→verde prueba defecto reparado, no capacidad total.

Cada gate tiene responsable, fecha, SHA, scope y resultado. Owner autoriza dinero real; Manager acepta diseño/código y evidencia; Submanager ejecuta sólo el mandato recibido; certificador entrega dictamen sin autootorgarse autorización. Publicar documentación se verifica mediante readback Git de paths/commit; jamás afirmar despliegue/certificación por esa publicación.

### 11. Estado de esta sesión y siguiente paso

Diseño candidato entregado; pruebas de esta matriz **NOT_RUN**. CERT-NT-01 continúa bloqueado/desarmado según última autoridad histórica, no verificado en vivo aquí. G-DOC pendiente del Primary Manager. B1–B3 no iniciados; G-IMPL/G-FEED/G-REC/G-SIM/G-PROD pendientes. No se envían instrucciones a otro chat ni se lanza GLM.

## Fuentes

- [[EF-PROD-GOD-01-SOURCE-FORENSICS]], [[EF-PROD-GOD-02-PRODUCTION-ARCHITECTURE]], [[EF-PROD-GOD-03-IMPLEMENTATION-PLAN]], [[Echo Futures — Runtime Pools]], [[OWNER-CHECKLIST-CERT-NT-01]].
- [[EXECUTION-FEED-BATCHING-VERIFICATION]]: diferencia entre suites, handler real, broker sintético y terminal físico; preservación de la evidencia S3 sin trasladar PASS a capas no ejecutadas.

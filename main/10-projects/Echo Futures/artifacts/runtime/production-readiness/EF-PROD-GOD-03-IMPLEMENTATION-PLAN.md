---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related: ["[[Echo Futures — Runtime Pools]]", "[[EF-PROD-GOD-02-PRODUCTION-ARCHITECTURE]]", "[[EF-PROD-GOD-04-CERTIFICATION-AND-RELEASE]]"]
aliases: []
tags:
  - kind/doc
created: "2026-10-23"
updated: "2026-10-23"
---

# EF-PROD-GOD-03-IMPLEMENTATION-PLAN

## Propósito

Plan consolidado para UN Submanager GLM LOCAL después de aceptación documental explícita del Primary Manager. Tres bloques coherentes, no una nueva secuencia de microshots FEFB. Este documento no despacha GLM ni autoriza ejecutar sus acciones. Baseline de diseño: `xKoRx/echo feature/ef-runtime-pools@ac0621a1917a9ecbed50b3daed4add1518ffc71d`; planificación y estado exclusivamente en [[Echo Futures — Runtime Pools]].

## Contenido

### 1. Gates y orden crítico

`G-DOC adjudicación → B1 continuidad/contratos → B2 seguridad end-to-end/paridad → B3 integración/migración/evidencia → G-IMPL revisión independiente → autorización física separada → G-CERT → decisión PROD Owner`.

Cada bloque produce un baseline integrado único y manifiesto de evidencia. No se inicia el siguiente con contratos compartidos divergentes. El Manager puede revisar entregas intermedias para resolver una contradicción concreta; no se requiere otra revisión arquitectónica general. Cualquier cambio a reglas económicas congeladas, motor/storage alternativo o relajación de invariantes exige decisión nueva y queda fuera de este plan.

El Submanager posee integración, baseline, tareas y evidence index; especialistas ONE-SHOT acotados por módulo y un verificador independiente sirven dentro de los tres bloques. Nadie se autoacepta. Un solo writer por archivo; el Submanager integra secuencialmente cambios que compartan contratos. Paralelismo sólo en paths disjuntos después de fijar schemas.

### 2. Precondiciones antes del primer cambio

1. Leer los cuatro documentos completos y la adjudicación G-DOC; conservar R6/FEFB/F1 y D1–D6. Gates CERT-NT-01 históricos no se reetiquetan PASS. Registrar el SHA de cada autoridad.
2. Refrescar HEAD de rama runtime; comparar exclusivamente deltas materiales contra ac0621a1. Separar commits The Lab V4. Si el código de un finding cambió, revalidar esa ruta, sin revertir trabajo ajeno. Crear/reusar checkout aislado de producto conforme a policy; Agents-OS master sólo documentación.
3. Inventario `effective-runtime-manifest.json` y E01–E07 de Forensics mediante lectura autorizada. El mandato de implementación de software no autoriza deploy/shared infra; pruebas físicas se ejecutan sólo en entorno aislado autorizado, o quedan NOT_RUN con gate bloqueado.
4. Registrar estado seguro sin deducirlo de una nota vieja. Para trabajar sólo en source basta conservar no-touch; para prueba física futura demostrar scope/owner lock, cuentas SIM, negativo PROD/Forge/FX compartido y ausencia de competidor.
5. Clasificar data plane existente de cada cuenta: previous economic history, M2, native history, current claims, exact config. Si faltan checkpoints, implementar y probar el guard igualmente; no rellenar pins para probar “verde”.
6. No activar cuenta real ni asumir ID Sim101 fijo. No cambiar master producto, sync.sh o .sync/. No limpiar evidencia histórica para ganar espacio; dimensionar scratch fuera del vault.

### 3. Contratos compartidos que se fijan primero

| Contrato | Writer inicial | Consumidores | Congelación exigida |
|---|---|---|---|
| C-REC-1..4 | Submanager + especialista lifecycle | Core shells, deploy utility, Bridge, QA | campos exactos, canonical digest, roster, missing-state behavior, manifest/attestation y matriz de compatibilidad |
| C-EXEC-1 | Especialista ejecución con aprobación de integración | SDK, Core, bridge, NT | runtime generation ≠ claim epoch, scope, expiry, account binding y manejo de reducción |
| C-DATA-1 / C-SEQ-1 | Especialista market | FEFB C#, relay, SDK, recording | stream_data_seq/previous, epochs, identities, tratamiento legacy y fuera de horizonte |
| C-OBS-1/2 | Especialista ejecución | journalfs, EventGate, adapter NT, AddOn | estado pending/published, native ID+digest, ACK durable, quarantine, idempotencia de fill evidence |
| C-TIME-1 | Especialista Core | Provider/Operation/Strategy shells, replay adapter | clock fijo por Apply, owner_input_seq, context reads y config/calendario refs |
| C-ECON-1 | Especialista economía técnica | projector, SDK accounting, Provider ingress | revision/covers-through/fees/boundary/outbox, sin fórmulas nuevas |

Los nombres de nuevos archivos de las tablas siguientes son decisiones propuestas de implementación, no claims de archivos existentes. Mantener definiciones wire en SDK, adapters en su módulo y kernels puros; Core no importa internals de Bridge ni viceversa. Fixtures de contrato versionadas acompañan los schemas. No duplicar una definición de cuenta o clock en cada módulo.

### 4. B1 — Continuidad verificable, M1 y gates de ownership

**Objetivo:** un estado económico previo nunca puede convertirse en job vacío habilitado. Cierra F01/F02/F06 y sienta contratos de F07/F09. Baseline de entrada ac0621a1 o su HEAD reconciliado; salida `B1_SHA` inmutable, `B1_RELEASE_MANIFEST` y reporte de compatibilidad.

| Owner especialista | Paths existentes / nuevos propuestos | Trabajo integrado |
|---|---|---|
| Lifecycle/Core | `v3/core/internal/futuresruntime/recovery.go`, `runtime.go`; `v3/core/cmd/echo-core/main.go`; nuevo `v3/core/internal/runtimecontrol/` y `v3/core/cmd/echo-runtime-control/` | REC-03 real, registry/manifest, único submission, detectar cambio de job con Core vivo, readiness y watchdog independiente del mailbox; sin bootstrap por pins vacíos |
| SDK contracts | `v3/sdk/futures/domain/`; nuevo `v3/sdk/futures/recovery/` | lineage/permit/admission schemas, validadores, hashes canónicos y tipos de error; paquete pequeño sin imports de infraestructura |
| StateFun shells | `v3/core/internal/functions/futures_{market_stream,market_analytics,strategy_engine,signal_fanout,pool_manager,provider_rules,operation}.go` | marker por owner, recuperación sin inicialización silenciosa y attestation; preservar ValueSpecs, keys y owners existentes |
| Deploy/config | `v3/core/deploy/flink-statefun/{develop,production}/{module.yaml,flink-conf.yaml,docker-compose.yml}` | manifests objetivos, checkpoint EO/egress EO, storage independiente, política de restore/retención y prohibición de autosubmit vacío; no aplicar a hosts en bloque source |
| Ejecución técnica | `v3/futures-bridge/adapters/kafka/command_consumer.go`, `core/ntx/{wire,server}.go`, `internal/session/session.go`, `adapters/journalfs/fence.go`, `cmd/futures-bridge/main.go`; AddOn `EchoExecutionAddOn.cs` | stable group, lock/registry/generation, fence último salto, propagación de fsync failure, permiso expirable y pin de cuenta |
| FX integration | `v3/bridge/internal/session/{command_consumer,execution_session}.go`, `v3/bridge/internal/pipe_handler.go`, `v3/bridge/cmd/echo-bridge/main.go`; wrappers registrados en `v3/core/cmd/echo-core/main.go` (incluidos `mm_engine.go`, `execution_planner.go`, `trade_journal.go`); cliente activo `v3/clients/mt4/execution_agent_v3.mq4` o `mt5/execution_agent_v3.mq5` | ReadCommitted y offsets explícitos en FX, guard de continuidad compartido y control new-risk antes del pipe y broker; extensión mecánica de generation/expiry en cliente sólo para coexistencia FX armada, sin alterar MM/SL/TP/sizing. Capability ausente ⇒ FX new-risk cerrado o B antes de coexistencia, conforme Documento 2 §7; no reescritura EA |

**Qué debe quedar probado en B1:** fresh namespace autorizado vs missing registry desconocido; prior run con pin coincidente pero checkpoint vacío rechazado; job sustituido mientras Core vive; terminal failure sin candidato; restore de checkpoint válido con offsets/owners; no duplicación ante submit outcome incierto; late old generation y dos hosts; `read_committed` frente a abort/commit real en entorno aislado; ningún cambio de startupPosition para recuperar.

**Compatibilidad:** reader entiende schema anterior, writer nuevo sólo después de migración autorizada. Añadir markers a snapshot existente es una migración concreta con roster y fingerprint pre/post; no habilitar por default de JSON. Todas las keys preexistentes incluidas; activas de FX no desaparecen. Nueva condición fail-closed puede reducir disponibilidad legacy; es intencional y debe aparecer en release notes. Si se cambia group M1, tomar posición anterior y reconciliar M2 antes de mover; jamás iniciar desde head porque sea más rápido.

**Evidencia de salida:** `contracts-v1.md` con matrices/campos, manifests válidos/inválidos sin secretos, matriz de UIDs/ValueSpecs, escenarios de restore y transacciones, negación de ejecución sin permiso, cambios de source y criterio de rollback. RCA E01 se adjunta si apareció; su ausencia no se maquilla ni impide escribir un guard genérico. No declarar la causa original cerrada por pasar pruebas nuevas.

### 5. B2 — Entrega económica durable, feed seguro y tiempo/paridad

**Objetivo:** completar end-to-end la autoridad de hechos, identidad y tiempo, manteniendo kernels. Depende del SHA/contratos B1. Salida `B2_SHA` integrado sobre B1; un especialista puede trabajar ejecución y otro mercado en paralelo sólo después de fijar SDK/C# compartidos.

| Owner especialista | Paths | Trabajo integrado |
|---|---|---|
| M2/observaciones | `v3/futures-bridge/internal/session/gate.go`, `adapters/ninjatrader/{adapter,helpers}.go`, `adapters/journalfs/{journal,fence}.go`; nuevos `journalfs/observations.go`, `core/capabilities/observation_delivery.go`; `adapters/kafka/publisher.go` | Durable pending→publish→published; quitar marcas anticipadas de todos los niveles; errores de órdenes no ignorados; cuarentena persistente; native ID+digest también antes de sumar ObservedFilledQty |
| NT execution | `v3/futures-bridge/addon-ninjatrader/EchoExecutionAddOn.cs`; nuevo archivo de storage común sólo si reduce duplicación | ACK recibido por Bridge durable separado de command_result; persistir callbacks/pendientes, history horizon y replay tras NT restart; no Queue.Clear que pierda hechos sin recovery |
| FEFB storage/feed | `EchoFeedV1.cs`, `EchoNativeBars.cs`, `adapters/ntfeed/{relay_batch,kafka}.go`, `core/ntfeed/{frame,market_batch}.go` | Flush-to-disk/atomic replace/corruption; C-SEQ-1; control/data ACK intactos; native coverage y unique producer; fixture legacy preservado |
| Market identity | `v3/sdk/futures/market/{ingress,batch,canonicalize,engine,recording}.go`; shell market_stream | Cursores por lane/epoch/stream, old-redelivery fail-visible, digest conflict, gap protocol; no ventana ilimitada ni reducir 4096 para perf |
| Tiempo/recording | `v3/sdk/futures/domain/clock.go`; shells Futures y `futuresruntime`; `sdk/futures/market/recording.go`; extensiones de interfaces de recording en SDK | AdmissionContext immutable por owner, monotonicidad persistida, replay del journal de cuenta/contextos y clock guard; no nuevas fórmulas Strategy/MM |
| Economía técnica | `v3/futures-projector/` (entrypoint/consumer/storage existentes), `v3/sdk/futures/accounting/`, `provider/input.go`, `core/internal/functions/futures_provider_rules.go`; schema/migración PG bajo árbol actual de DB del producto | Productor causal de revisión contable + outbox transaccional PG, ingress account-authority, snapshot inicial autoritativo, fees/corrections/session coverage, sin per-tick DB |
| Config/producer | `v3/sdk/messaging/kafka_producer.go`, `v3/sdk/domain/client_config.go`, `v3/core/deploy/flink-statefun/*/module.yaml` | Idempotencia y orden de producer sync por perfil, sin regresión async FX; bindings/version/digest/expiry, routing de authority topic |

**Límites del bloque:** no tocar política económica de provider ni math de MM/Strategy; se agregan metadatos/adapters de causalidad. Si un input inexistente era satisfecho por fixture, conectar una fuente autoritativa o dejar UNKNOWN, nunca fabricar. Backtester recibe fixtures y contratos de admission/replay compartidos; sólo adapter técnico mínimo para consumirlos si el mandato de implementación lo autoriza expresamente, nunca cambiar resultados de campaña por conveniencia. The Lab no se modifica.

**Casos obligatorios:** Kafka caído justo tras marcar fill; terminal orden antes de publication; redelivery de mismo native ID con mismo/distinto digest; reboot en cada fase del outbox; error fsync dir; >4096 identidades y replay; old epoch; barras late/revised/gap con source ALL vs LAST; config versión igual contenido distinto; NTP atrás/adelante; varias Clock.Now en una transición; cierre diario con operaciones outstanding; late fill después de release; journal incompleto debe rechazar EXACT_REPLAY.

**Protección:** implementar capability gate y transportar planes sellados existentes sólo cuando soportados; registrar prueba requerida de supervivencia de protección. No implementar un bracket sintético con decisiones MM en AddOn para aprobar. Si la combinación actual no satisface contrato, el resultado correcto es esa combinación bloqueada y el motivo preciso, no una emulación no autorizada.

**Evidencia de salida:** repros F03/F04/F05 antes/después, fixtures wire Go↔C#, manifests de state migration, hashes de inputs/outputs de paridad, evidencia de todos los owners temporales, informe de contrato físico que aún falta. Fills aplicados, ledger y exposición deben coincidir, no sólo conteos de Kafka.

### 6. B3 — Integración, operación y paquete único de certificación

**Objetivo:** producto integrado, migrable, operable y verificable sin otra revisión general. Depende de B2. Un verificador ONE-SHOT independiente audita el delta total desde baseline reconciliado; especialistas correctivos corrigen dentro del mismo bloque. Una sola entrega final y un único G-IMPL.

| Trabajo | Ownership | Resultado |
|---|---|---|
| Runtime real aislado y adversarial | Verificador independiente + Submanager | Flink Java/Kafka real con image/module exactos, checkpoints/restore, dataset maduro y failures, sin inferirlo del Go harness |
| Envelope | Integración/perf | ALL/50ms/NATIVE, 1×/2×/bursts, arrivals vivos, costes tx/serde, 1/100/200 deliveries, contención controlada; números bajo hardware declarado |
| Operación/observabilidad | Lifecycle + Core/Bridge | /health y /ready separados, alertas y permisos vencibles, datos para incidentes/rollout/rollback/power-loss |
| Migración | Submanager | Snapshot pre/post, roster/offsets/UIDs y semántica, config historical refs, rollback después de efectos explícito; ninguna migración aplicada al shared runtime sin mandato físico |
| NT bundle | Especialista NT | Compilación integrada futura con assemblies reales en staging aislado, hashes de cada archivo/assembly, rollback/install card; una sola definición de AddOn |
| FX | Verificador | Mismos ingress IDs/keys/offsets, no reset de estado; consumidores read_committed y conflictos Journal clasificados; outage gate y último salto probados si se pide coexistencia armada, o declaración obligatoria FX new-risk desarmado; no nueva expansión bajo recovery incierto |
| A/B decision | Manager usando evidencia | A cumple y se mantiene; si no, NO-GO con razón específica y activar B bajo el contrato de migración §13; no esconder fallo cambiando límites |

**Salida final:** SHA único source; release manifest por binario; package `implementation-evidence/` con índice y checksums; dictamen independiente por finding; todos los defectos críticos reparados o condición de capability explicitamente bloqueada; procedimiento de instalación reversible; `PHYSICAL_CERTIFICATION_READY` sólo si ya existen las precondiciones. Si falta entorno aislado, marcar pruebas no ejecutadas y G-IMPL bloqueado en esas garantías, no dar PASS condicionado que parezca certificación.

### 7. Migración y rollback, por tipo de estado

| Estado | Migración | Condición de rollback |
|---|---|---|
| StateFun/offsets | Snapshot completo compatible con roster/UID/key/ValueSpec intactos; nuevas fields con default sólo semánticamente seguro; marker bootstrap explícito | Binario anterior lee schema nuevo probado, o vuelta al corte sólo si no hubo efectos después; de otro modo forward repair |
| M2 intents/fences | Reader dual, append versionado, backup íntegro; jamás borrar SUBMITTING/AMBIGUOUS | Conserva máximo fence/generation; downgrade no acepta formato desconocido ni pierde pending |
| Observations outbox | Inicializar sobre journal/historia real con native identity; pending primero; no terminal GC hasta covers-through | Reader anterior incapaz de pending → no downgrade con pendientes; drenaje y snapshot requerido |
| NT feed storage | Converter aislado, original intacto, checksum y atomic rename; cursor no supera persisted data | Rollback de binario sólo con formato legible; sino restauración coherente de bundle identity/outbox/cursor, con gap declarado |
| Config/registry | Compare-and-swap, version/digest; snapshots históricos conservados | No reducir generation, no borrar prior existence ni reutilizar authorization |
| PG contabilidad | Migraciones aditivas, revisión/outbox en transacción, unique keys con digest | Retener journal original; no destruir revisión ni revertir fills físicos |
| Kafka topics/groups | Nunca reset para migración; nueva identity requiere barrera y frontier firmado | Volver a prefijo previo sólo sin lectores/escritores competidores y con M2/historia reconciliados |

Para el estado perdido F1, el Submanager debe producir `f1-continuity-disposition.md`: qué existe, qué falta, evidencia de economía previa, lineage recuperable o retiro explícito. Una declaración textual de que no hubo órdenes no reemplaza M2/venue/command-topic evidence para permitir bootstrap. FX se concilia independientemente; no se borra el job compartido por facilitar FUTURES.

### 8. QA/adversarial consolidado y aceptación del código

Los IDs de escenarios/medidas se fijan en Documento 4, sin duplicar otra checklist operativa. Cada finding F01–F09 debe enlazar source antes/después, repro rojo cuando sea defecto, resultado integrado y gate físico aplicable. Tests nuevos cubren invariantes/crashes/orden, no mirrors de implementation. No tests que “simulan” ACK rellenando el resultado que deben probar.

Mantener los cinco fallos heredados identificados FEFB por caso/causa; no aceptar una falla actual automáticamente por tener el mismo nombre. Comparar baseline exacto y confirmar que no afecta el contrato productivo nuevo. Coverage ≥95% del código nuevo con denominador publicado después de funcionalidades críticas; delta completo y exclusiones declarados aparte. No silenciar timeout/race ni cambiar aserciones para obtener verde. Tests existentes son oráculos; modificación sólo justificada por contrato adjudicado.

Capas de evidencia separadas: (1) reducers y serialización; (2) RequestReplyHandler SDK real, múltiples invocaciones/owners/error mid-request; (3) Kafka y StateFun Java aislados con transacciones/checkpoints; (4) C# real + assemblies/install; (5) terminal físico feed-only; (6) ejecución SIM autorizada; (7) venue/producto real bajo permiso futuro. Ninguna capa sustituye la posterior. Tests y campañas no se ejecutan en esta sesión GOD.

**G-IMPL acepta sólo:** P0 reparados, P1 cerrados en source y pruebas de su capa disponible, contratos/wiring completos (no sólo consumidores), ninguna decisión de negocio inventada, schemas y rollback definidos, gate de versión/seguridad satisfecho, scripts operacionales revierten seguro y no fresh-submit. G-IMPL no autoriza armar ni declarar CERT PASS.

### 9. Evidencia mínima de cada entrega

- `BASELINE.json`: fuente, HEAD remoto, SHA de contratos y toolchains; diff material vs baseline y segregación Lab.
- `RELEASE-MANIFEST.json`: hashes por binario/assembly/config/schema, no secretos; hash SHA completo, nunca sólo tag.
- `EVIDENCE-INDEX.md`: escenario, ambiente, datos, comando futuro ejecutado por GLM, inicio/fin UTC, resultado, raw ref/hash, límites; sin dumps pesados en vault.
- `STATE-COMPATIBILITY.md`: ValueSpecs/UIDs/serializers/keys, migración, propiedad de cada estado y matriz old/new reader/writer.
- `RECOVERY-PROOF.md`: checkpoint lineage/offsets/markers/cuentas/M2; fallos/restore y rearm por separado.
- `ACCEPTANCE-MATRIX.md`: IDs Documento 4, PASS/FAIL/NOT_RUN/EVIDENCE_GAP, evidencia y responsable; no “pass agregado” ocultando un gap.
- `HANDOFF.md`: SHA integrado, defectos restantes, cuentas/gates desarmados y siguiente responsable; no autorización implícita de siguiente fase.

### 10. Necesario, diferido y no autorizado

Necesario para A: F01–F09, registry/guard, storage recuperable, M1, observaciones durables y no dedup prematuro, cursor/horizon, persistencia eléctrica, permit/fencing, tiempo/recording, autoridad contable, gates de protección, evidencia FX/NT y envelope. Correcciones precisas se integran como un paquete; no abrir “FEFB S4”.

Diferido P2: actualización de engine si inventario de seguridad no demuestra bloqueo, HA multi-host, separación B hasta trigger, optimización compacta adicional tras medir, archivo frío optimizado. C: active-active, sharding intracuenta, portfolio dinámico, migración masiva Forex/MT, motor nuevo o The Lab. No duplicar Strategy/MM para LIVE/replay/backtest.

Precondiciones de certificación real: G-DOC/G-IMPL aceptados, SHA/binarios exactos, permisos de entorno aislado y Owner de terminal, cuentas SIM verificadas, M2/backup, plan de paro/rollback viable, carga/ventana autorizada, fuentes de evidencia operativas. La falta de historia/contador/calendario/economía/protección se resuelve en modo fail-closed, no con defaults de fixture.

### 11. Responsabilidades y STOP

Primary Manager adjudica diseño integral, alcance, evidencia y G-IMPL. Submanager GLM LOCAL coordina implementación y verifica límites/autoridades; no acepta su propio gate. Especialistas ONE-SHOT entregan módulos y evidence en paths asignados. Verificador independiente cuestiona el conjunto. Owner controla terminal, cuenta, exposición, ventanas y autorización económica; sólo él autoriza promoción de cuentas reales.

El siguiente responsable ahora es **Primary Manager**. GLM no está lanzado/autorizado por publicar este documento. No ejecutar pruebas, deploy, cuentas ni infraestructura desde EF-PROD-GOD-01.

## Fuentes

- [[EF-PROD-GOD-01-SOURCE-FORENSICS]], [[EF-PROD-GOD-02-PRODUCTION-ARCHITECTURE]], [[EF-PROD-GOD-04-CERTIFICATION-AND-RELEASE]], [[Echo Futures — Runtime Pools]].
- [[ECHO-FUTURES-RUNTIME-POOL-DESIGN]] R6, [[EXECUTION-FEED-BATCHING-DESIGN]] y [[EXECUTION-FEED-BATCHING-VERIFICATION]]: conservar freezes, límites físicos y oráculos históricos.

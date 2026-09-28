---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
  - "[[Echo Futures — D2-05 Instrument Session Provider]]"
  - "[[Echo Futures — D2-06 Market Runtime]]"
  - "[[Echo Futures — D2-07A Execution Adapter Contract]]"
  - "[[Echo Futures — D2-07B Transport Selection]]"
aliases:
  - Echo Futures D2-07C
  - EF Execution Runtime Topology
  - EF Futures Bridge Topology
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-design
created: "2026-09-27"
updated: "2026-09-27"
---

# Echo Futures — D2-07C Execution Runtime Topology

## Propósito

Resolver exclusivamente D2-07C: topología del execution runtime, boundary Bridge/Adapter, modelo de sesiones, side-effect authority, colocación del journal M2, routing de comandos y semántica de reconexión/reconciliación. La pregunta central es si Echo Futures extiende físicamente el Bridge V3 (`v3/bridge`) o construye un sibling que reutilice sus patrones y aloje los execution adapters futures. No implementa código, no selecciona transport (D2-07B ya recomendó `PROJECTX_DIRECT` como candidato), no certifica vendors, no integra D2-07 y no abre D2-08.

Autoridades consumidas: [[Echo Futures]], [[Echo Futures — D2-04 Operation Order Fill Position]], [[Echo Futures — D2-05 Instrument Session Provider]], [[Echo Futures — D2-06 Market Runtime]], [[Echo Futures — D2-07A Execution Adapter Contract]] (autoridad inmediata del contrato del adapter), [[Echo Futures — D2-07B Transport Selection]] (separación D2/D6 ya reparada). Baseline físico: `xKoRx/echo origin/master = 372af59a7b83604781346613da01e3d510ea1360`, re-verificada con `git fetch` sin delta. Baseline Agents-OS: `9f3c950bd86e5a83f9af1fbeec841888c0898ebf`.

## 1. Executive verdict

```text
D2-07C STATUS: READY_FOR_SUBMANAGER_REVIEW

BRIDGE DECISION: FUTURES_BRIDGE_SIBLING

reuses V3 bridge patterns (per-account sessions, dedicated Kafka consumers,
circuit breaker, pause/resume, kache/telemetry/etcd conventions)
does NOT extend v3/bridge and does NOT create a bridge-framework
```

El Bridge V3 no puede alojar los adapters futures sin deformarse: es un proceso **Windows-only** (`//go:build windows` en `v3/bridge/cmd/echo-bridge/main.go`) cuya razón de existir es el transporte Named Pipes hacia los EAs MetaTrader, mientras el primer transport futures recomendado es network-native y su constraint operacional (Topstep: order flow desde dispositivo personal del trader, sin VPS/VPN) coloca el runtime en un host distinto del edge MT. Extenderlo obligaría a acoplar crash domain, deployment, release cadence y superficie de credenciales de dos familias de transporte con requisitos de host incompatibles, contradiciendo la disposición ya congelada de D2-04 ("Bridge = REUSE patrones / ADAPTER NUEVO; el adapter MetaTrader actual no se deforma").

La recomendación es un **sibling** (nombre conceptual `v3/futures-bridge`; el naming final es decisión de implementación D4/D6) que reutiliza patrones y las librerías `v3/sdk/*` tal cual, duplica las pocas piezas bridge-internal que necesita (varios cientos de líneas) en vez de extraer prematuramente un framework, y aloja el `ExecutionAdapter` como componente interno transport-specific. No se crea un cuarto servicio: no existe `ExecutionAdapterHost` como proceso independiente; para la familia desktop-hosted el componente platform-side es parte del adapter (la misma forma física que hoy tienen el Bridge V3 + EA MetaTrader), no una nueva capa.

La ventana M2 del legado quedó confirmada físicamente en baseline: el EA MT5 valida idempotencia con `g_Journal.FindByCommandId` **antes** de `g_Trade.Buy/Sell` (líneas 1764–1815) pero persiste el outcome con `g_Journal.Add` **después** del side effect (líneas 1841/1863); MT4 repite el patrón (`OrderSend` línea 1961 → `g_Journal.Add` líneas 1975/2005). Un crash entre side effect y journal permite replay físico. El runtime Futures no hereda esa forma: el journal M2 write-ahead (D2-07A §7) vive en el futures-bridge, **antes** del point-of-no-return.

`OWNER DECISIONS REQUIRED: NONE`. No hay bloqueo arquitectónico: ningún gap de evidencia de vendor afecta la topología (los gaps ProjectX permanecen como certification gates D6 según el repair D2-07B).

## 2. Scope / authorities

- **En scope:** boundary físico Bridge/Adapter, proceso/host cardinality conceptual, sesiones, side-effect authority, colocación del journal M2, command routing Kafka, retorno de eventos normalizados, reconnect/readiness barrier, cambios de binding en caliente, degraded close, modelos de host network-native y desktop-hosted, matriz de reuso Echo V3, sharing mínimo de código, escala estructural y escenarios de aceptación.
- **Fuera de scope:** implementación, elección de store físico del journal (D6), certificación M2 de cualquier transport (D6), selección owner del transport inicial (OD-D2-07-1, candidate only), integración D2-07, D2-08, adapters concretos, HA/fencing technology, benchmarks de capacidad.
- **Jerarquía:** D2-07A es autoridad del contrato del adapter (M1/M2, journal, readiness, finality, reconnect) y sus 14 constraints de §22 son insumo vinculante de este artefacto. D2-04 es autoridad de Operation/Order/Fill/Position, correlación adapter-owned (§8.2) y topología Core. D2-05 es autoridad de `ProviderAccountBinding`/transport entitlement/DayBoundary. D2-06 separa market runtime de execution transport. D2-07B fija que la certificación física es D6 y que este worker no depende de ningún vendor.

## 3. Physical Echo V3 findings (inspección `372af59a`)

Hallazgos materiales del execution path, verificados sobre el clon en `~/aranea/work/d3-shot3-correction-20260924/echo`:

- **Proceso Windows-only:** `v3/bridge/cmd/echo-bridge/main.go` está gated `//go:build windows`; todo el transporte hacia la plataforma es Named Pipes gestionado por `internal/pipe_manager.go` (prefijos `bridge/reference_*`/`bridge_execution_*` desde ETCD `bridge/pipe_prefix`). Bootstrap: `di.InitSelective` (ETCD + Telemetry + Kafka) → config ETCD (`bridge/*`, `kafka/brokers`) → `NewBridgeWithDI` → `bridge.Run()` bloquea hasta shutdown ordenado (HTTP → SessionManager → kache → notifier → symbol mapping → pipes → producer).
- **Consumo de comandos per-account:** `v3/bridge/internal/session/command_consumer.go` crea un consumer Sarama dedicado por cuenta con topic `echo.commands.{execution_account_id}.v1` (línea 107), group `echo-session-{account}-{hostname}`, `OffsetNewest` + commit híbrido (auto-commit 1 s + `MarkMessage` tras procesar) = at-least-once con ventana de redelivery; retry FIFO con backoff para fallos de entrega al pipe; circuit breaker cierra la sesión tras N fallos consecutivos (`recordFailure`/`triggerSessionClose`); Pause/Resume ate el consumo a la conexión del pipe (backpressure: los comandos se acumulan en Kafka mientras el EA está desconectado).
- **Publicadores legacy de Core:** `v3/core/internal/functions/mm_engine.go:585-586` y `close_handler.go:369` publican comandos directamente a `echo.commands.{execution_account_id}.v1` por egress StateFun; el topic per-account ya es la convención física vigente.
- **Wire contracts legacy:** `CoreCommand` (`v3/sdk/domain/reference_event.go:304`) transporta `command_id/trade_id/strategy_id/execution_account_id/broker/canonical_symbol/broker_symbol/side/lot_size` + SL/TP físicos e ideales + TTL (`max_open_delay_seconds`) + contexto de telemetría; `ExecutionResult` (`:526`) colapsa a un único resultado con `Ticket/Success/ErrorCode/FillPrice` (sin Order→N Fill); `PositionSnapshot` (`v3/sdk/domain/position_snapshot.go:19`) es MT-oriented por ticket (`account_id, ticket, TradeID, StrategyID, …`). Topics legados: `echo.execution-results.v1` (key=TradeID), `echo.close-results.v1`, `echo.account-snapshots.v1`, `echo.instrument-snapshots.v1`, `echo.position-snapshots.v1` (key=AccountID) — publicados por `pipe_handler.go`.
- **Sesiones:** `session/execution_session.go` + `session/session_manager.go`: `GetOrCreateSession` maneja reconexión (crea si CLOSED, actualiza handler + resume si PAUSED/CONNECTING), estados `CONNECTING/ACTIVE/PAUSED/CLOSED`, timeout de pausa (5 min) cierra la sesión, reconciliación de broker canónico sobre la autodeclaración del EA (`UpdateBroker`/`resolveAccountBroker`), aislamiento por construcción (cada cuenta: topic + consumer + breaker propios; comentario físico cita el freeze del 2025-12-18 de un consumer compartido como motivación).
- **Registro:** `internal/http_server.go` expone `POST /api/v1/register` (número de cuenta + tipo `reference|execution_agent` + broker autodeclarado) y `GET /api/v1/health`; `account_registry.go` mantiene el registro in-memory y el callback `onAccountRegistered` crea pipe + sesión.
- **Config/símbolos/telemetría:** kache consume `echo.account-configs.v1` (compacted) con group por hostname; `ConfigChangeNotifier` propaga `ClientConfig` a sesiones y pipes; `SymbolMappingCache` carga mappings por topic compactado de Kafka (eliminó el PG directo) y alimenta detransform canonical→broker en comandos y handshake; telemetría OTel con propagación de `ExecutionFlowTelemetry` comando→resultado.
- **Readiness:** mecanismo interno de señales (kache + symbol mapping) que retiene el HTTP server hasta ready; no existe superficie de execution-readiness (socket activo se trata implícitamente como ejecutable).
- **M2 journal del legado:** no existe journal en el Bridge; vive en el EA (`v3/clients/mt4/execution_agent_v3.mq4`, `v3/clients/mt5/execution_agent_v3.mq5` + `EchoPersistence.mqh`): rolling journal de archivos (500 + archive) con `FindByCommandId` antes del send y `Add` después del `OrderSend`/`CTrade` — ventana de crash física confirmada (§1). El journal guarda ticket/resultado, no el intent pinneado completo, y su rolling no está ligado ni al redelivery Kafka ni al history horizon del venue.
- **`module.yaml` (`v3/core/deploy/flink-statefun/develop`):** sin `delivery semantics` declarada; el runtime es `apache/flink-statefun:3.2.0` — consistente con el requisito de config EXACTLY_ONCE de D2-04 §5.6 (config de SPEC, no comportamiento demostrado).

## 4. Bridge role (terminología congelada)

```text
Core (echo/operation) ──Kafka──▶ Futures Bridge ──▶ ExecutionAdapter ──▶ Platform / Venue
                                     (proceso/runtime shell)   (componente interno)
```

- **Bridge = process/runtime shell:** bootstrap/config/sesiones/consumo Kafka/egress de observaciones/telemetría/health. Posee credentials y sessions porque la ejecución física lo exige (D2-07A: el edge puede poseer credentials/session), no porque tenga dominio.
- **ExecutionAdapter = componente interno transport-specific:** instancia por familia/binding; implementa el contrato D2-07A (journal M2, point-of-no-return, reconciliación, observaciones normalizadas).
- **NO se crea `ExecutionAdapterHost`:** no hay cuarto servicio. Si hace falta nombrar el rol interno que aloja adapters, es un rol del propio Bridge. En la familia desktop-hosted el componente platform-side (análogo al EA MetaTrader) es la mitad del adapter que vive dentro del proceso de la plataforma; conceptualmente sigue siendo "el adapter", no un servicio nuevo con identidad propia de negocio.

## 5. Extend-vs-sibling decision

```text
RECOMMENDATION:
FUTURES_BRIDGE_SIBLING
```

Justificación por las dimensiones del mandato §24:

- **Legacy MT coupling:** Named Pipes, handshake EA, broker-symbol detransform, TTL-on-delivery, snapshots por ticket y journal EA son semántica MT; extender obligaría a introducir ramas de "tipo de adapter" dentro de un proceso cuya razón de ser es MT.
- **Failure-domain isolation:** hoy el breaker/pipe aísla por cuenta pero el proceso es un único crash/deploy domain del edge MT; una fuga de memoria de un adapter network o una rotación de credenciales futures no debe reiniciar la ejecución MT en vivo (y viceversa).
- **OS constraints (carga decisiva):** `v3/bridge` es Windows-only por Named Pipes; ProjectX exige order flow desde el dispositivo personal del trader (sin VPS/VPN/relay). Los hosts físicos de ambas familias son distintos por mandate del vendor y por topología de terminales, no por preferencia.
- **Reuse potential:** los patrones reutilizables (sesión per-account, topic dedicado, pause/resume, breaker, kache/notifier, readiness signals, telemetría, convención ETCD) son pequeños y re-implementables en cientos de líneas; el grueso del código del bridge (`pipe_handler.go` solo 2213 líneas) es MT-only.
- **Deployment model / release cadence:** el edge MT se despliega junto a terminales MT; el futures-bridge se despliega en el dispositivo del trader; versionarlos acoplados forces redeploys del edge MT por cambios futures (riesgo de regresión sobre sistema estable, contrario a "do not deform stable legacy code").
- **Config/session model:** el binding futures vive en `ProviderAccountBinding`/`Account.execution_binding_id` (D2-05) con entitlement y condiciones; el modelo MT (broker autodeclarado + mapping broker-symbol) no lo representa.
- **M2 journal needs:** el journal write-ahead debe vivir en el durability domain del side-effect owner (el proceso futures); `v3/bridge` no tiene infra de journal y añadiría una responsabilidad nueva a un proceso legacy.
- **Testing:** el sibling permite validar Core→Kafka→Bridge→SimExecutionAdapter sin terminales MT ni Windows (§13), cosa imposible dentro de un proceso Windows-gated.
- **Migration risk / code duplication / operational complexity:** el sibling duplica ~pocas piezas pequeñas en V1 (aceptado por KISS, §26) a cambio de cero riesgo para el legado; extender tiene menor duplicación inicial pero acopla todo lo demás.
- **Future adapter extensibility:** un segundo network adapter (CQG, candidato de contraste D2-07B) o un desktop-hosted futuro encajan como nuevas instancias de adapter dentro del mismo sibling sin tocar MT.

Los dos extremos prohibidos quedan fuera: no se copia el Bridge entero (sólo patrones) y no se convierte `v3/bridge` en un framework universal de execution edges.

## 6. Minimal runtime topology

```text
                     Core (StateFun, Linux/Aranea)
                     echo/operation  key account:strategy
                        │  egress EXACTLY_ONCE (M1)
                        ▼
        echo.order-commands.{execution_account_id}.v1
                        │
                        ▼
   ┌──────────────────────── Futures Bridge (1 proceso) ───────────────────────┐
   │  config/kache · session registry per account · command consumers          │
   │  telemetry · health · normalized-event egress · M2 journal (per account)  │
   │                                                                            │
   │  ExecutionAdapter (instancia por account/binding)                          │
   │   ├─ SimExecutionAdapter            (sim, sin credenciales)                │
   │   ├─ DirectNetworkAdapter           (ProjectX: HTTP/WebSocket → venue)     │
   │   └─ DesktopHostedAdapter           (futuro: conector + componente         │
   │                                      platform-side dentro del desktop)     │
   └────────────────────────────────────────────────────────────────────────────┘
                        │  echo.execution-events.v1 (key=op key, correlacionado)
                        │  echo.position-observations.v1 (key=account)
                        ▼
                     Core (ingress → echo/operation / proyección Position)
```

Mismas fronteras de garantía que D2-04: M1 termina en el egress transaccional de Core; M2 empieza en el primer paso del Bridge/Adapter que puede alcanzar al venue y se cubre con el journal durable + reconciliación (D2-07A §8). El Bridge nunca es autoridad de dominio; su única "verdad" local es el journal M2 y las observaciones físicas.

## 7. Bridge responsibilities (mínimas)

- consumir comandos normalizados de su cuenta (`SubmitOrder`/modify/cancel D2-07A §5);
- resolver/configurar el `ExecutionAdapter` declarado por el binding de cada cuenta;
- poseer el runtime de cuenta/sesión (consumer dedicado, ciclo CONNECTING→ACTIVE→PAUSED→CLOSED, backpressure, breaker);
- sostener el journal M2 write-ahead por cuenta y su recovery al arranque;
- ejecutar la acción de transporte vía adapter y preservar correlación física;
- recover/reconcile tras restart/reconnect (D2-07A §17) antes de reabrir riesgo;
- normalizar y publicar OrderObservation/OrderActionObservation/Fill/PositionObservation/ExecutionSessionObservation;
- exponer health/readiness/telemetry (incluida observación de `AMBIGUOUS`/readiness/lag de reconciliación).

Nada más: sin Strategy, sin MM, sin reglas provider, sin sizing, sin rollover, sin autoridad de market data, sin inventar Operation.

## 8. ExecutionAdapter responsibility

El adapter es la unidad transport-specific que implementa D2-07A: secuencia de submit con `PREPARED/SUBMITTING` durables antes del point-of-no-return (§6.1–6.2), resolución de ambiguos por `client_order_id`/idempotencia nativa/history (§6.1.9–11), five event families (§9), finality evidence (§16), reconnect sequence (§17), capability declaration (§13) y static eligibility vs dynamic readiness (§14–15). Ejemplos informativos: ProjectX = familia direct-network; NinjaTrader = familia desktop-hosted. No se desarrolla ningún adapter concreto en D2.

## 9. SimExecution path

`SimExecutionAdapter` implementa el mismo contrato D2-07A dentro del futures-bridge y permite validar el seam completo sin credenciales ni vendor:

```text
Core → Kafka → Futures Bridge → SimExecutionAdapter → observaciones normalizadas → Core
```

Puede ejercitar ACK, reject, fill, partial fills, cancel, modify, reconnect y ambigüedad simulada (crash post-SUBMITTING sin outcome). Dos separaciones obligatorias: (1) no es un exchange simulator completo ni un backtester — el backtest del dominio sigue siendo el `SimExecution` puro de Core (D2-04 §8.7) sobre el mismo contrato de eventos; (2) SimExecution no transforma el journal M2 en decoración: la simulación de ambigüedad debe ejercitar journal + recovery real del bridge, porque ese es el código que D6 certificará con un transport real.

## 10. Process / account / session cardinality

Identidades distintas (nunca colapsadas):

```text
bridge instance        = proceso desplegado (host del trader/edge)      — no identifica negocio
adapter instance       = configuración/vivencia de una familia dentro del bridge — no identifica negocio
transport session      = conexión autenticada efímera (epoch)           — cambia en reconnect
execution account      = execution_account_id Echo                      — identidad de routing/dominio
provider external account = identidad que el venue autentica/observa    — verificada contra binding
```

Cardinalidad soportada: `1 bridge → N accounts` cuando el adapter lo soporta (familia network: una sesión ProjectX addressa N cuentas) y `1 bridge/session → 1 account` cuando el transport lo exige (familia desktop: una instancia por terminal/proceso de plataforma). Core no depende de la cardinalidad: el topic per-account y el keying por cuenta hacen invisible cuántos bridges/procesos existen.

## 11. Ownership / side-effect authority

Por cada `execution account + physical binding` existe **como máximo una autoridad activa** capaz de side-effectear:

- La asignación cuenta→bridge instance es configuración (binding plane), no emergente de Kafka. `Kafka consumer ownership NO es fencing físico`: un proceso stale puede seguir teniendo consumer vivo y alcanze al venue; un fencing token local no detiene a un proceso particionado que aún puede transmitir.
- **V1 KISS: NO AUTOMATIC CROSS-HOST TAKEOVER.** Un binding se ejecuta en exactamente un host/instancia designada. El crash se recupera in-place (restart en el mismo host consumiendo el mismo journal + reconciliación de venue — eso es seguro porque el journal es durable y el binding físico es el mismo). Migrar el binding a otro host es acción operacional explícita: el nuevo owner arranca con el mismo journal durable y re-executa la secuencia de recovery D2-07A §17; el host anterior se detiene primero. Fail-closed antes que HA falsa.
- Session generation/epoch: cada sesión de bridge porta una generation por cuenta, registrada en el journal; un owner reemplazado/stale no puede re-habilitar submission (D2-07A constraint 4). La generación es **detección** de stale-owner (discrepancia visible, NEW_RISK off), no un kill remoto; la contención física se previene por la regla de instancia única + operador.
- Duplicate bridge processes sobre la misma cuenta = config error detectable: misma cuenta en dos instancias debe ser rechazada por config/validación (misma cuenta, dos consumers del mismo topic con groups distintos es observable; telemetría de doble-owner) y por la generation del journal.

## 12. M2 journal placement

D2-07A §7 congeló semántica, no tecnología. Colocación congelada aquí:

- El journal M2 vive en el **durability domain del side-effect owner**: dentro del futures-bridge, co-localizado con el adapter instance que ejecuta el binding (mismo host). Es la condición para que `I4 write-before-side-effect` sea real: la escritura no puede cruzar un red que pueda caerse antes del venue.
- Un store durable local (detrás de interface, single-writer por cuenta) basta en D2: `durable local/shared store behind interface`. No se elige SQLite/Postgres/RocksDB/etc. (decisión D6 con el transport real). Prohibido: Core PG como M2 authority (D2-07A constraint 13); Kafka como journal primario (el egress de Core ya garantiza M1; usar Kafka para el write-ahead del adapter añadiría una segunda frontera transaccional entre el bridge y su side effect sin necesidad).
- Debe sobrevivir process restart, command redelivery, fast fill y lost ACK; almacena el binding físico pinneado (transport_id, provider external account, external contract identifier, términos completos, action ids — D2-07A §7.1) para reconciliar contra el mismo transport/session/account.
- GC/tombstones: se aplican las reglas D2-07A §7.5 (nunca GC `AMBIGUOUS`; tombstone compacto preferido); la retention la dimensiona D6 con el history horizon real del transport.

## 13. Kafka command routing

```text
Convención actual:      echo.commands.{execution_account_id}.v1
Futures:                echo.order-commands.{execution_account_id}.v1   (D2-04 §8.3)
Disposición:            REUSE del patrón / familia NUEVA (ADAPT)
```

- **REUSE del patrón:** topic por cuenta con la cuenta en el nombre; un consumer por sesión; egress account-keyed desde Core (`mm_engine.go:586`/`close_handler.go:369` ya lo hacen para legacy); orden por key/partición.
- **Familia nueva, no topic compartido:** el payload Futures es `SubmitOrder/modify/cancel` D2-07A §5 con semántica y requisitos de consumo distintos (`read_committed`, correlación op-key en los eventos de retorno). Mezclar ambos en `echo.commands.*` obligaría a versionar el payload en el mismo stream que consume el legado.
- Garantías: el bridge consume **sólo** las cuentas de su config/binding (validación adicional payload `execution_account_id == session account`, defence-in-depth); key/account consistency (topic + payload + journal en la misma identidad); **no transport branching en Core** — el egress es account-keyed y la resolución de transporte vive en la config del binding (D2-05); redelivery no implica physical retry (offset commit tras outcome + journal M2, el consumo at-least-once del legado se mantiene como pattern pero el commit del side effect es el journal, nunca el offset — D2-07A constraint 8); ordering relevante por Account/Order (una cola serializada por cuenta; order_id/action_id estables).
- No se crean: topic por Order, topic por transport, function type por vendor.

## 14. Normalized event return

El futures-bridge publica a `echo.execution-events.v1` (key = op key, ingress directo a `echo/operation`, D2-04 §8.2) las cinco familias D2-07A §9, cada evento con identidades suficientes: `execution_account_id`, `operation_id`, `order_id/client_order_id`, `provider_order_id?`, `provider_execution_id?`, `contract_id`. Familias: `OrderObservation`, `OrderActionObservation`, `Fill`, `PositionObservation` (→ `echo.position-observations.v1`, shape neto `(account, contract)` D2-04 R8) y `ExecutionSessionObservation`. Actividad manual/desconocida: observación física + reconciliation debt (`POSITION_MISMATCH`), nunca Operation fabricada (I10 D2-07A). Los DTOs legacy (`ExecutionResult`/`PositionSnapshot`/`CloseResult`) no se promueven al camino futures; coexisten para el legado (§10 del mandato).

## 15. Reconnect / readiness barrier

Después de restart/reconnect, por cuenta: `NEW_RISK = OFF` hasta completar la secuencia D2-07A §17 (auth → verificar binding → event stream → cargar journal no-terminal → resolver cada `PREPARED/SUBMITTING/VENUE_BOUND/AMBIGUOUS` → listar/reconciliar open orders → recuperar executions desde cursor → position snapshot fresca → emitir missed observations → contrastar físico vs lógico). Sólo entonces `EXECUTION_READY_NEW_RISK`, y únicamente si la static eligibility D2-05 (entitlement/RuleSet/DayBoundary) también lo permite. Reconnect jamás resubmite automáticamente (I12). El patrón de sesión legado (pausar consumo mientras no hay edge, reanudar al reconectar) se reutiliza, pero la reanudación del consumo **no** es readiness: consumer saludable con venue unhealthy no ejecuta (D2-07A §15.2).

## 16. Hot binding change

D2-05/D2-07A §19: si cambia `ProviderAccountBinding`/`Account.execution_binding_id`, las submissions nuevas van al binding nuevo sólo tras readiness del nuevo; las Orders físicas vivas permanecen pinneadas al binding físico original hasta terminal/reconciliación — sin live migration. El runtime conserva la recovery information del binding anterior (journal + sesión/session generation de ese binding) aunque la Account ya tenga otro current binding; si el transport anterior deja de ser accesible, el estado es recovery debt/operador, no remap silencioso. La cuenta puede tener dos durabilities de journal coexistiendo (old binding en recovery, new binding activo) — la identidad del journal es por binding, no por cuenta sola (refina la PK conceptual D2-07A §7.1 `(execution_account_id, client_order_id)` que sigue siendo la clave de dedup; el pin de transporte vive dentro del record).

## 17. Degraded close / ForceClose con bridge DOWN

Si Core tiene termination/ForceClose pendiente y el bridge está DOWN: la termination **permanece pendiente, no es terminal** (D2-04 R3: ForceClose es intent); alert/readiness degraded visibles (ExecutionSessionObservation). Al recuperar: reconciliar primero (secuencia §15) y recién después continuar la termination hacia guards. Nunca synthetic success. No existe "emergency transport switch" para cerrar por otro adapter: sólo un diseño futuro explícito podría introducirlo. El gate CLOSE/REDUCE degradado sigue D2-07A §15.3 (sólo si se demuestra que la acción no aumenta riesgo y conserva finality).

## 18. Network adapter model

```text
Futures Bridge (host autorizado por el provider, p.ej. dispositivo personal del trader)
  └─ DirectNetworkAdapter → HTTP/WebSocket → venue
```

Bridge y adapter en el mismo proceso; el adapter consume la sesión de red y las credenciales del binding. Los hosts/despliegues son territorio D6 (incluida la constraint Topstep de dispositivo personal), pero la topología ya no obliga a ningún componente Windows ni a terminales MT.

## 19. Desktop adapter model

Misma forma física que el legado MT: el adapter se divide en conector bridge-side + **componente platform-side thin** corriendo dentro de la plataforma desktop (análogo al EA), hablando IPC local con el bridge. Conceptualmente sigue siendo un solo `DesktopHostedAdapter`; el componente platform-side no tiene identidad de dominio, no journala M2 por sí solo (el journal sigue en el side-effect owner del bridge; el componente platform-side es transporte, igual que hoy el EA — su deuda M2 es exactamente la razón por la que el path MT no se reutiliza como M2) y no aparece como servicio adicional. Si algún día un transport desktop demostrara que el side-effect owner real es el proceso de la plataforma, ese caso se diseña explícitamente entonces; V1 no lo asume.

## 20. Echo V3 reuse matrix

| Pieza V3 | Disposición | Razón |
|---|---|---|
| process/bootstrap (DI, config ETCD, run/shutdown) | **EXTRACT/SHARE (patrón) / ADAPT** | La forma es correcta y pequeña; el sibling repite el bootstrap usando `v3/sdk/di` tal cual; el `main.go` MT es Windows-gated |
| Kafka connection (producer DI, consumer patterns) | **REUSE** | `v3/sdk/messaging` + config Sarama probada |
| per-account command consumer | **ADAPT** | Mismo shape (topic dedicado, pause/resume, breaker, retry FIFO); futures añade `read_committed`, sin TTL-on-deliver, dispatch al adapter con journal write-ahead |
| command topic convention | **REUSE patrón / familia nueva** | `echo.commands.{acct}.v1` legado intacto; futures usa `echo.order-commands.{acct}.v1` |
| session registry (GetOrCreate/estados/pause timeout) | **ADAPT** | Semántica idéntica desacoplada de pipes; re-implementar pequeña, no importar el paquete acoplado a PipeHandler |
| HTTP registration de EAs | **REPLACE_FOR_FUTURES** | No hay EAs que registren; queda health endpoint y surface operacional |
| Named Pipes / pipe manager / pipe handlers | **MT_ONLY** | Transporte MT; inaplicable a familia network |
| config cache (kache + ChangeNotifier) | **REUSE** | Mismo mecanismo para catálogos futures (calendars/bindings) |
| symbol mapper / SymbolMappingCache | **MT_ONLY** (patrón de distribución REUSE) | Futures resuelve `ContractIdentifier` por `(source, context)` D2-05; no existe detransform broker-symbol |
| telemetry (OTel + semconv + trace propagation) | **REUSE** | Directo desde `v3/sdk/telemetry` |
| health/readiness signals | **ADAPT** | Añadir superficie de execution-readiness por cuenta (D2-07A §15); el gate de "socket" se queda corto por diseño |
| account/instrument snapshots (batch publishing) | **MT_ONLY** shape / **REUSE** batching pattern | Futures emite observaciones normalizadas propias |
| position snapshots | **REPLACE_FOR_FUTURES** | Shape MT por ticket → `PositionObservation` neta `(account, contract)` D2-04 R8 |
| ExecutionResult / CloseResult | **MT_ONLY** | Wire legacy; `echo.execution-results.v1` no recibe fills futures |
| local command journal (EA `SlaveCommandJournal`) | **REPLACE_FOR_FUTURES** | Post-side-effect, rolling sin contrato de recovery; el journal M2 write-ahead es nuevo en el bridge |
| etcd/config conventions | **REUSE** | Namespace `futures-bridge/*` nuevo, mismas convenciones |

## 21. Minimal shared code (KISS)

Día 1 se comparte **sólo lo que ya es librería**: `v3/sdk/*` (messaging, telemetry, kache, etcd, di, domain DTOs como wire legacy). No se extrae nada nuevo de `v3/bridge/internal`: la sesión per-account, el breaker y el readiness-signaling se **duplican** en el sibling como implementación pequeña (cientos de líneas) — duplicar antes que crear `bridge-framework`, `plugin-runtime`, `generic-adapter-sdk` o un dynamic plugin loader. La extracción se reconsidera cuando exista un tercer consumidor real de esos patrones o cuando una corrección tenga que replicarse dos veces; hasta entonces, dos copias pequeñas y estables son más baratas que una abstracción prematura.

## 22. Scale implications

La decisión no obliga a `1 heavyweight process per account`: un solo proceso futures-bridge hostea N adapter instances/sessions (familia network) y Core ve cuentas, no procesos. Pressure points identificados (sin certificar): número de consumer groups/topics per-account crece linealmente con cuentas (patrón ya vivido en legado; monitorear overhead de rebalance), IO del journal append-only por cuenta, reconnect storm tras restart masivo (reconciliación por cuenta debe ser rate-limited/escalalonada), límite de sesiones/credenciales por transport (una sesión ProjectX addressa N cuentas — favorable), count de procesos desktop en familia desktop-hosted (1 por terminal). Benchmark de 100–200 cuentas = D6; ninguna decisión de este artefacto hace el target estructuralmente inalcanzable.

## 23. Acceptance scenarios

- **A — Normal submit:** Core Order → egress M1 → topic per-account → bridge session → adapter `PREPARED`/`SUBMITTING` durables → venue/sim → ACK/Fill → `OrderObservation`+`Fill` correlacionados (key op key) → `echo/operation`. Una sola physical order (M1+M2).
- **B — Partial fills:** BUY 3 con executions `+1,+1,+1` → tres Fill facts inmutables por `provider_execution_id`; Core deriva filled/avg. Sin colapso a ExecutionResult.
- **C — Kafka redelivery tras submit físico:** offset sin commit + journal con outcome → `DUPLICATE_SUBMIT_SUPPRESSED`; journal `PENDING` → resolución contra venue antes de re-enviar; jamás blind duplicate.
- **D — Bridge restart con Order working:** mismo host/journal; carga no-TERMINAL, reconcilia open orders por tag, conserva binding físico, re-evalúa readiness; la Order sigue viva, no se duplica ni cancela.
- **E — Fill antes que ACK:** `SUBMITTING` + Fill primero → Fill se preserva como primera evidencia autoritativa; order state se reconstruye desde fill/history (D2-07A §6.3).
- **F — Actividad manual:** observación física + `POSITION_MISMATCH`/debt; nada entra a `echo/operation` como Fill Echo; nunca Operation fabricada.
- **G — Binding change con Order viva:** nuevas submissions → binding nuevo tras readiness; Order viva pinneada al binding original; journal del binding viejo conserva recovery info; coexistencia de durabilities por binding (§16).
- **H — ForceClose con bridge down:** termination pendiente + alert; al volver: reconciliar → continuar termination → TERMINAL sólo por guards; sin synthetic success ni transport switch.
- **I — Fallo de sesión de Account A:** breaker/pausa de la sesión A; los comandos de B siguen por su topic/sesión/journal propios; ningún comando de B alcanza a A (topic per-account + validación payload + journal por binding).
- **J — SimExecution:** mismo Core→Kafka→Bridge boundary con `SimExecutionAdapter`, sin credenciales; ejercita ambigüedad/crash y recovery del journal real.

## 24. Risks / deferred work

- **R1 — Journal technology:** el store durable detrás de interface debe elegirse/certificarse en D6 (fsync semantics, corruption recovery); la corrección de D2 depende de que "durable" sea realmente durable.
- **R2 — Doble-owner residual:** la regla NO AUTOMATIC TAKEOVER previene takeover automático pero no puede impedir físicamente que un operador arranque dos instancias; mitigación = validación de config + telemetría de doble-owner + generation en journal. Es fail-visible, no infalible — honesto ante el mandato §16.
- **R3 — Stale process con alcanze al venue:** un proceso particionado puede side-effectear aunque haya perdido ownership lógico; V1 lo acepta como riesgo operacional acotado por instancia única por host; fencing technology real queda deferred.
- **R4 — Consumer count por cuenta:** el patrón topic-per-account multiplica consumers; con cientos de cuentas el overhead Kafka debe medirse en D6 (alternativa de partición compartida keyed-by-account es un cambio local del routing, no del boundary).
- **R5 — Desktop family sin diseño concreto:** el componente platform-side queda a nivel conceptual; su protocolo/IPC se diseña cuando un transport desktop sea seleccionado.
- **R6 — Duplicación V1:** las piezas duplicadas (session/consumer/breaker) pueden divergir del legado; aceptado mientras ninguna corrección tenga que replicarse más de una vez antes de reconsiderar extracción.

## 25. Constraints exported to integrated D2-07

1. `FUTURES_BRIDGE_SIBLING`: la ejecución futures vive en un proceso propio reutilizando patrones/SDK de V3; `v3/bridge` no se deforma ni recibe adapters futures.
2. Bridge = shell; ExecutionAdapter = componente interno; no existe `ExecutionAdapterHost` ni cuarto servicio; platform-side desktop = parte del adapter.
3. Journal M2 write-ahead en el durability domain del side-effect owner (futures-bridge), store físico D6, nunca Core PG ni Kafka como journal primario.
4. Una autoridad de side effect por `(execution account, physical binding)`; NO AUTOMATIC CROSS-HOST TAKEOVER en V1; takeover operacional exige mismo journal + recovery completo; session generation para detección de stale owner.
5. Command routing: familia nueva `echo.order-commands.{execution_account_id}.v1` reutilizando la convención per-account; sin branching de transport en Core; redelivery ≠ physical retry.
6. Retorno por las cinco familias normalizadas D2-07A hacia `echo.execution-events.v1` (key op key) + `echo.position-observations.v1` neto; DTOs legacy no promovidos.
7. Reconnect barrier completa antes de `EXECUTION_READY_NEW_RISK`; readiness ≠ consumer saludable ≠ socket.
8. Live Orders pinneadas al binding físico original; journals por binding para recovery; hot rebind prospectivo only.
9. ForceClose con bridge down = pendiente, nunca terminal; reconcile-first al recuperar; sin emergency switch.
10. SimExecutionAdapter valida el seam completo sin vendor y ejercita el journal/recovery real; no es backtester ni exchange simulator.
11. Shared code día 1 = `v3/sdk/*` únicamente; duplicación KISS de piezas bridge-internal; prohibido bridge-framework/plugin-runtime.
12. Implementación física, host placement, store del journal, certificación M2 y benchmarks de capacidad pertenecen a D6/D4 según la separación D2-07B.

## Fuentes

- [[Echo Futures]] — estado D2-07 dispatch, decisiones D2-01..06.
- [[Echo Futures — D2-04 Operation Order Fill Position]] — M1/M2, §8.2 correlación adapter-owned, §8.3 topics, §9 disposición Bridge = REUSE patrones/adapter nuevo.
- [[Echo Futures — D2-05 Instrument Session Provider]] — ProviderAccountBinding/transport/entitlement, `Account.execution_binding_id`.
- [[Echo Futures — D2-06 Market Runtime]] — separación market/execution, `REPLACE/DO NOT PROMOTE` del bridge MT feed.
- [[Echo Futures — D2-07A Execution Adapter Contract]] — contrato del adapter y 14 constraints a D2-07C.
- [[Echo Futures — D2-07B Transport Selection]] — separación D2/D6, ProjectX candidate, constraints de host.
- `xKoRx/echo@372af59a` — source físico: `v3/bridge/cmd/echo-bridge/main.go` (Windows gate), `v3/bridge/internal/{bridge,pipe_manager,pipe_handler,http_server,account_registry,config,symbol_mapping_cache,telemetry}.go`, `v3/bridge/internal/session/{command_consumer,execution_session,session_manager,interfaces}.go`, `v3/core/internal/functions/{mm_engine,close_handler}.go`, `v3/core/deploy/flink-statefun/develop/module.yaml`, `v3/sdk/domain/{reference_event,position_snapshot,snapshots,trade_close}.go`, `v3/sdk/statefun/constants.go`, `v3/clients/mt4/execution_agent_v3.mq4`, `v3/clients/mt5/execution_agent_v3.mq5`.
- [[Echo + Echo Forge — Environment Contract]] — modelo de ambientes (este worker: arquitectura local, sin mutación de infra).

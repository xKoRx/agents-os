# Echo Futures — D6 BRIDGE RESTART RECOVERY REMEDIATION (F-D6-H)

**Rol:** TOP Senior Recovery / Execution Transport Remediation Lead (one-shot, fresh context)
**Fecha:** 2026-10-04
**Proyecto:** [[Echo Futures]]
**Repositorio:** `xKoRx/echo` · branch `feature/d6-shot1-execution-vertical`
**BASELINE_SHA:** `32baeaeb49cff8b4227b850d7a575549bbcf54a2` (HEAD == origin, worktree limpio, verificado antes de tocar fuente)
**FINAL_SHA:** `d08a30ce9815f820fda7132e20dc42cc345eb8e8` (push FF `32baeaeb..d08a30ce`, sin rewrite; origin == HEAD al cierre)

## Verdict

```text
D6_BRIDGE_RESTART_RECOVERY_REMEDIATION = PASS
BRIDGE_RESTART_RECOVERY = 6/6 PASS (physical, REAL AddOn, first try, no lucky alignment)
```

Corrección del ÚNICO defecto físicamente demostrado en el ATTEMPT 6 (`D6_REAL_EXECUTION_LANE_NO_EGRESS = REMEDIATION_REQUIRED`): la carrera de recovery del bridge al rearrancar. El remedio vive íntegro bridge-side en la semántica de recovery/subscription readiness del adaptador NinjaTrader, exactamente como adjudicó el Primary Manager. `EchoExecutionAddOn.cs` y `EchoFeedAddOn.cs` **byte-idénticos** (cero cambios AddOn, cero re-instalación NinjaTrader, cero acción Owner). KISS/YAGNI: un marker nuevo (`ordersAt`), un reset session-scoped en el hello, y `RestoreSubscriptions` re-autorizada — sin sleep fijo, sin retry ciego, sin coordinator nuevo, sin knob de config nuevo.

**Seguridad física:** `PHYSICAL_ORDERS_SENT = 0` · `PHYSICAL_ORDERS_MODIFIED = 0` · `PHYSICAL_ORDERS_CANCELLED = 0` · `OD-D6-1` SIN consumir. Cero command frames (topic `echo.order-commands.E2T-GAU50-01.v1` con 0 mensajes, lag 0, committed offset intacto `-1001` antes y después). Journal M2 con 0 registros antes y después. G-EGRESS-0 restaurado y probado al cierre.

## Reproducción física 1/6 (ATTEMPT 6, 2026-10-04)

6 arranques del bridge contra el AddOn REAL corregido: **1 PASS / 5 FAIL**. Las 5 fallas con la firma exacta `barrier: reconcile: ninjatrader: no position snapshot observed yet` a +2.8–6.1 s del `account session built` (evidencia: `~/aranea/work/d6-reallane-cert-attempt6-20261004/evidence/c-bridge-journal-full-run.log`; ciclo 13:26:15 built → 13:26:18 ERROR; 13:39:26 → 13:39:32; 13:41:51 → 13:41:57; 13:42:06 → 13:42:11; 13:42:20 → 13:42:26). El único PASS ocurrió cuando el tick periódico de snapshot del AddOn cayó dentro de la ventana de milisegundos entre el hello y el reconcile — suerte de timing, inaceptable para el drill de restart FIRST-TRY del ladder.

## Root cause (confirmada en source @ 32baeaeb antes de modificar)

La secuencia del barrier (`internal/session/session.go` `RunRecoveryBarrier`: Connect → Authenticate → VerifyBinding → RestoreSubscriptions → load journal → Reconcile) chocaba con tres hechos del adaptador:

1. **Hello contaba como observación de recovery.** `HandleFrame` setea `lastObserved` en TODO frame entrante, incluido el hello (`adapter.go:289` baseline), y `RestoreSubscriptions` sólo esperaba `lastObserved != zero` (`adapter.go:223-241`) ⇒ hello solo ⇒ restore PASS.
2. **Reconcile sin precondición.** `Reconcile` → `PositionSnapshot` falla instantáneo con `no position snapshot observed yet` si `positionsAt == zero` (`adapter.go:941`).
3. **El AddOn real sólo publica positions/orders en su tick de snapshot** (`EchoExecutionAddOn.cs`: fastTimer 2 s × `snapshot_seconds` 5 = tick cada 10 s, sin burst al conectar) ⇒ el éxito de arranque dependía de la fase del timer. Los tests pasaban porque enviaban la ráfaga de fixtures inmediatamente después del hello y nunca veían la carrera.

Dos brechas adicionales confirmadas en el mismo source: **H5** — `handleOrders` actualizaba el map de órdenes sin ningún marker de recepción (`adapter.go:380-398`): un map vacío era indistinguible entre `orders=[]` autoritativo y `ningún orders frame llegó`; **H2** — `handleHello` no reseteaba las vistas de observación (`positionsAt`, `positions`, `orders`, `orderIndex`): el estado de snapshot de una sesión superseda sobrevivía al hello de la sesión nueva y habría satisfecho su recovery.

## Manager adjudication aplicada

Primary Manager ACEPTA el finding H; C0/C/D/E/F/G quedan certificados por la evidencia física del ATTEMPT 6 (pickup, transporte, binding, observaciones, barrier estable, reconnect/fencing — intactos). La corrección acotada a la semántica de recovery/subscription readiness bridge-side; prohibidos sleep fijo, retry ciego, bypass del barrier, relax fail-closed, coordinator nuevo, state machine global, knob nuevo no imprescindible y modificación del AddOn por timing. El bridge debe esperar evidencia física suficiente de la sesión actual antes de reconciliar.

## Code delta (4 archivos, +372/−66; producto: `adapters/ninjatrader/adapter.go`)

### H1 — RECOVERY SNAPSHOT AUTHORITY
`RestoreSubscriptions` ahora espera los DOS snapshot families venue-authoritativos de la sesión actual: **positions observado AND orders observado**. El hello/heartbeat sólo alimenta liveness (`lastObserved`, `streamLiveLocked`); jamás recovery readiness. **Un snapshot observado-VACÍO es evidencia autoritativa** — `positions=[]`/`orders=[]` aceptados (readiness sin `POSITION_NOT_FRESH`), y `no observado` permanece materialmente distinto de `observado vacío`. No se inventaron requirements adicionales: no se exige snapshot de executions (familia identity-keyed, no es precondición de reconcile en el V1 lane).

### H2 — SESSION-SCOPED EVIDENCE
El hello de una sesión nueva retira los markers de snapshot y el outcome de reconciliación de la sesión superseda: `orders`/`orderIndex`/`ordersAt`/`positions`/`positionsAt`/`reconcileAuth`/`reconciled` se resetean bajo el mismo lock (`handleHello`). SESSION_B jamás recupera sobre observaciones de SESSION_A; sus propios snapshots deben llegar. El fencing de sesión activa existente queda intacto (los frames tardíos de A siguen siendo rechazo contado — segunda barrera tras el fenceo server-side del `ntx.Server`). `executions`/`executionSeen` se conservan deliberadamente: la dedup y los fills acumulados están keyed por identidad nativa de ejecución (hecho de venue independiente de sesión; limpiarlos duplicaría fills en el journal).

### H3 — BOUNDED WAIT, NOT TIMING LUCK
La espera usa el presupuesto de frescura de observación EXISTENTE del adaptador (`ObservationFreshness`, default 30 s = 3 ticks de snapshot a la cadencia certificada; producción corre el default — sin key ETCD ni knob nuevo). `CommandTimeout` queda reservado a su autoridad propia (command/result). En timeout: **FAIL CLOSED** con la clase de error exigida `ninjatrader: required recovery snapshots not observed within bound (positions=<bool> orders=<bool>)` — nombra la familia faltante, cero comandos consumidos, cero side effects.

### H4 — RECONCILE PRECONDITION
`PositionSnapshot` NO fue debilitado: sin observación alguna sigue fallando cerrado con su error físico exacto (`no position snapshot observed yet`), pineado por test (`TestRealLaneBarrier_MissingPositionsStillFailsClosed` + capa reconcile). `no observado` jamás se convierte en `observado vacío`.

### H5 — ORDERS SNAPSHOT EVIDENCE
Marker interno mínimo `ordersAt` seteado en `handleOrders` a la recepción de CUALQUIER orders snapshot (incluido el vacío): la llegada del frame ES la evidencia. El estado del map en memoria deja de ser la única señal — `orders=[]` autoritativo ≠ `ningún orders frame llegó`.

## H6 — TESTS DE LA CARRERA (reallane + adapter, comportamiento sobre el stack REAL)

`internal/session/reallane_barrier_test.go` — `ntx.Server` + `Adapter` + `Session` reales sobre TCP con los fixtures AddOn comprometidos; harness extendido con segunda conexión (`dialAddon`) y session ids distintos. Los 7 casos exigidos:

| Caso | Test | Resultado |
|---|---|---|
| 1 HELLO ONLY | `TestRealLaneBarrier_HelloOnlyNeverSatisfiesRestore` | PASS — bounded FAIL-CLOSED `…(positions=false orders=false)`, `Recovered=false`, comandos sin iniciar |
| 2 DELAYED SNAPSHOT (el regression 1/6) | `TestRealLaneBarrier_WaitsForDelayedSnapshots` | PASS — el barrier ESPERA ≥300 ms (ventana sin settle), pasa inmediatamente al llegar los snapshots; demora real, no burst sincrónico |
| 3 EMPTY SNAPSHOTS | `TestRealLaneBarrier_AdvancesOnAddOnObservationSequence` | PASS — `orders=[]`+`positions=[]` aceptados como evidencia; readiness sin `POSITION_NOT_FRESH` |
| 4 MISSING POSITIONS | `TestRealLaneBarrier_MissingPositionsStillFailsClosed` | PASS — bounded FAIL `…(positions=false orders=true)`; `PositionSnapshot` mantiene su error físico exacto |
| 5 MISSING ORDERS | `TestRealLaneBarrier_MissingOrdersStillFailsClosed` | PASS — bounded FAIL `…(positions=true orders=false)` |
| 6 SUPERSEDED SESSION | `TestRealLaneBarrier_SupersededSessionCannotReuseSnapshots` | PASS — A observado → B hello (TCP nuevo, fenceo server visible en log) → barrier ESPERA (A no satisface B) → snapshots de B → PASS |
| 7 WRONG ACCOUNT | `TestRealLaneBarrier_WrongAccountStillFailsClosed` | PASS — sin regresión, stop en verify_binding |

Tests existentes actualizados al contrato nuevo: `TestBarrierBranchFailures/restore subscriptions timeout` (clase de error nueva, budget explícito vía `mustAdapterFresh`), `barrierUp` (envía también orders-empty y espera ambos markers). `TestRealLaneBarrier_SubmittingOrderAbsentFromEmptySnapshotFailsClosed` intacto y verde (AMBIGUOUS + `ReadyNewRisk=false`).

## Coverage y regression suite

- Funciones cambiadas: `RestoreSubscriptions` **100%**, `handleHello` **100%**, `handleOrders` **100%**, `PositionSnapshot` **100%** (sin cambiar). Paquete `adapters/ninjatrader` total **95.9%**.
- Suite completa `v3/futures-bridge/...`: **14/14 paquetes ok** (`go test -count=1`), incluye los guards estructurales AddOn (`config_guard`, `egress_guard`, `endpoint_guard`, `protocol_contract`) — AddOn byte-idéntico.
- `go vet` limpio; `gofmt -w` aplicado a los 3 archivos tocados (desviaciones gofmt preexistentes en otros archivos del baseline NO tocadas).

## Validación física NO-EGRESS (6/6 contra el AddOn REAL)

Despliegue: SOLO el binario del bridge corregido, release-dir `~/opt/echo-dev/releases/d08a30ce9815f820fda7132e20dc42cc345eb8e8/futures-bridge` (build `-trimpath` desde HEAD commiteado y pusheado, `vcs.revision=d08a30ce…`, `vcs.modified=false`, worktree limpio; sha256 `fb1ce6d44da0cdc27ca06fca0fd6b97e0d22958a6e668f05af390099a39670e5`); unidad `echo-futures-bridge.service` apuntada al nuevo release. NinjaTrader NO tocado, NO re-instalado, AddOn certificado preservado (sin W1, sin F5 — el AddOn no cambió). NT en dev-win .132 vivo durante todo el drill (relay :9770 con las 2 sesiones del AddOn publicando account RESOLVED Id "3" + `positions:[]` + `orders:[]` durante y después de los 6 ciclos, `reconnects:1` estable).

Armado del runtime (mismo ciclo G-EGRESS-0 del ATTEMPT 6): la clave de enumeración `/echo/development/futures-bridge/accounts` estaba AUSENTE (estado desarmado del cierre del attempt 6 — sin ella el bridge arranca con `accounts:0` y queda idle, sin barrier; descubierta en el primer intento de drill, registrado en `evidence/prearm-timeout/`). Se armó `="E2T-GAU50-01"` (rev 59388) para la ventana de validación y se eliminó al cierre (rev 59389). Un único intended account en todo momento.

Drill (script + journals en `~/aranea/work/d6-bridge-restart-recovery-20261004/`): 6 ciclos consecutivos `systemctl --user start/stop`, cada uno con sesión AddOn autenticada ESTABLISHED observada por `ss`, account resuelto, espera de snapshots de la sesión actual, y `echo.execution.recovered":true` en el PRIMER log de readiness (+30 s tick) del ciclo — first try, sin retry interno, sin errores:

| Ciclo | session built (local −03) | 1.er readiness | recovered | ambiguous | mismatches | dropped | errores |
|---|---|---|---|---|---|---|---|
| 1 | 14:43:00 | 14:43:30 | true | 0 | 0 | 0 | 0 |
| 2 | 14:43:34 | 14:44:04 | true | 0 | 0 | 0 | 0 |
| 3 | 14:44:07 | 14:44:37 | true | 0 | 0 | 0 | 0 |
| 4 | 14:44:41 | 14:45:11 | true | 0 | 0 | 0 | 0 |
| 5 | 14:45:14 | 14:45:44 | true | 0 | 0 | 0 | 0 |
| 6 | 14:45:47 | 14:46:17 | true | 0 | 0 | 0 | 0 |

`UnknownLiveOrders = 0` (journal vacío + snapshot vacío autoritativo, mismatch list vacía), `AccountMismatch = 0`, `ambiguous = 0`, `replay = 0` (committed offset `-1001` invariante). Blockers de readiness presentes y esperados por diseño Shot 1 (`STATIC_ELIGIBILITY_NOT_ELIGIBLE`, `SUBMISSION_CAPABILITIES_NOT_EXACT_READY` — capabilities UNKNOWN hasta sus gates G; ajenos a H). **BRIDGE_RESTART_RECOVERY = 6/6 PASS, sin alineación afortunada: el barrier esperó el tick del AddOn cuando hizo falta y pasó first-try en los 6 ciclos.**

## G-EGRESS-0 final (restaurado y probado)

Clave `accounts` eliminada (raw ETCD API, rev 59389, `deleted:1`, re-check `KEY GONE`) · unidad `inactive` + `disabled` · `:9771` FREE, cero conexiones exec · ETCD `/echo/development/futures-bridge/` **21 claves == baseline** (MCP RO) · topic `echo.order-commands.E2T-GAU50-01.v1` 0 mensajes, lag 0, committed `-1001` invariante · journal M2 **0 archivos** · AddOn feed/market lanes observando (relay :9770) sin ninguna mutación.

## Notas residuales y tooling

- El MCP ETCD RO devolvió una lectura FUZZY para la clave inexistente (`accounts` → `"17:00"`, valor de otra clave del prefijo) — gotcha ya conocido en memoria; la verdad se estableció por API cruda (`/v3/kv/range` keys_only). Confirmar por cliente crudo antes de cualquier escritura guardada.
- La bit-reproducción del binario anterior (484b550b) no fue posible con flags idénticos (`-trimpath`, CGO=1, go1.27.1 ⇒ shas distintos); la proveniencia queda anclada por FINAL_SHA pusheado + `go version -m` del binario (vcs.revision/vcs.modified) + sha256 registrado. El binario anterior queda intacto en su release-dir.

## Disposición

- `RESIDUAL_FINDINGS`: NONE sobre H.
- `OWNER_DECISION_REQUIRED`: NONE.
- `NEXT_MANAGER_ACTION`: aceptar H como CERRADO; congelar C0–H / execution transport (no tocar AddOns ni recovery transport nuevamente); certificar G-REALTIME (feed-lane-only, no depende de H); luego el ladder físico D6 ya autorizado en la primera ventana admisible (lun 2026-10-05 00:00–15:50 CT). NO emitir `EF_D6_E2E_PASS` hasta que el ladder pase.

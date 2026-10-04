# Echo Futures — D6 EXECUTION PROTOCOL REMEDIATION (F-D6-EXEC-01/02/03)

**Rol:** TOP Senior NinjaTrader / Execution Transport Remediation Lead (one-shot, fresh context)
**Fecha:** 2026-10-04
**Proyecto:** [[Echo Futures]]
**Repositorio:** `xKoRx/echo` · branch `feature/d6-shot1-execution-vertical`
**BASELINE_SHA:** `ffa493d8d179c9f9374d0a935e7916be15367ce8` (HEAD == origin == worktree limpio, verificado antes de tocar fuente)
**FINAL_SHA:** `32baeaeb49cff8b4227b850d7a575549bbcf54a2` (push FF `ffa493d8..32baeaeb`, sin rewrite; origin == HEAD == worktree limpio al cierre)

## Verdict

```text
D6_EXECUTION_PROTOCOL_REMEDIATION = PASS
```

Remediación de los DOS defectos de producto demostrados físicamente en el intento 4 de la certificación real C→K (`D6_REAL_EXECUTION_LANE_NO_EGRESS = REMEDIATION_REQUIRED`, artifact `d6-real-execution-lane-20261003`), más el endurecimiento mínimo del residual D3. Topología congelada del Design Freeze §6.1 preservada exactamente: market lane → nt-feed-relay (`echo.ntfeed.v1`, one-way), execution lane → futures-bridge (`echo.ntx.v1`, bidireccional). Sin tercer transporte, sin rediseño N1, sin tocar el EchoFeedAddOn certificado (byte-idéntico `581a7087…`), sin debilitar el parser del bridge.

**Seguridad física:** `PHYSICAL_ORDERS_SENT = 0` · `PHYSICAL_ORDERS_MODIFIED = 0` · `PHYSICAL_ORDERS_CANCELLED = 0`. Sin bridge, sin sesiones de ejecución, sin mutaciones ETCD, sin publishing Kafka, sin LIVE run, sin egress. Shadow-compile y arnés en staging `C:\Temp\d6exec-proto\` únicamente — NADA instalado en NinjaTrader por el agente (instalación = ciclo Owner). El token ntx y el token del feed nunca fueron impresos ni persistidos (sólo largos `len=64` en VERIFY).

---

## F-D6-EXEC-01 — market lane dializa el endpoint/protocolo equivocado

### ROOT CAUSE
`EnsureMarketLane` del `EchoExecutionAddOn` dializaba el MISMO endpoint que el execution lane (`ntxHost:ntxPort` = bridge `:9771`, `EchoExecutionAddOn.cs:283-330` baseline) porque compartía los campos de config del execution lane; el market lane habla `echo.ntfeed.v1` (`SendMarketHello`), y el bridge ntx rechaza cualquier schema distinto (`core/ntx/frame.go` `Frame.Validate`). Físico 2026-10-04 05:20:58.7Z: `[ntx] 132:55256 rejected: frame schema "echo.ntfeed.v1" is not "echo.ntx.v1"`.

### CONTRACT VIOLATED
D6 Final Design Freeze §6.1 (congelado): market lane termina en el **nt-feed-relay** (`:9770`, one-way, `echo.ntfeed.v1`, zero churn); execution lane termina en el **futures-bridge** (listener de config, `echo.ntx.v1`).

### CHANGE
- Nuevo `ResolveMarketEndpoint(out host, out port)`: lee `bridge_host`/`bridge_port` del **feed config certificado** `echo-feed-addon.json` — la autoridad existente del endpoint ntfeed (mismo archivo que ya era la fuente del token del market lane vía `GetMarketToken()`; cero valores inventados, cero claves nuevas en `echo-execution-addon.json`). Fail-closed: ausencia/error de parse ⇒ market lane DOWN con warning una sola vez (`marketEndpointFailed`); el execution lane nunca depende de ese archivo.
- `EnsureMarketLane` dializa SOLO el endpoint resuelto del feed config; `EnsureExecLane` dializa SOLO `ntxHost:ntxPort` (guard estructural: el region del market lane no contiene `ntxHost`/`ntxPort` y viceversa).
- Envolventes de schema por lane intactas y pineadas: `PublishMarketFrame`/`SendMarketHello` ⇒ `echo.ntfeed.v1`; `PublishExecFrame`/`SendExecHello` ⇒ `echo.ntx.v1`. Ningún método del fuente mezcla ambos literales de schema.

### TESTS
- `endpoint_guard_test.go::TestF_D6_EXEC_01_MarketLaneTargetsNtfeedRelay` — market lane dializa vía `ResolveMarketEndpoint` (`bridge_host`/`bridge_port`), jamás `ntxHost/ntxPort`.
- `…_ExecLaneTargetsBridge` — execution lane dializa sólo `ntxHost:ntxPort`, sin dependencia del feed config.
- `…_NoCrossProtocolContamination` — ningún método fuente contiene ambos schema literals; el dial de cada lane está limpio del schema del otro.
- `protocol_contract_test.go::TestF_D6_EXEC_01_EndpointParsersRejectForeignSchema` — wire-level, determinista: un frame `echo.ntfeed.v1` es rechazado por el parser del endpoint ntx y un `echo.ntx.v1` por el del endpoint ntfeed; cada frame parsea en su propio endpoint (fixtures del AddOn, no strings hand-written).

### COVERAGE
Structural guards sobre el fuente real (metodología aceptada `config_guard_test.go`) + behavioral wire-level con fixtures producidos por código extraído mecánicamente del `.cs` (ver `/protocol_contract_tests`). 100% de los cambios de wiring de D1 cubiertos por los 4 tests.

### COMPILE
Shadow-compile físico contra NT 8.1.8.3 (dev-win .132, `csc.exe` .NET Framework64 v4.0.30319, refs `NinjaTrader.Core.dll` + `NinjaTrader.Gui.dll` + `WindowsBase.dll` físicas): **EXEC 0 errores** (3 warnings preexistentes del baseline certificado: `CS0612 Account.CreateOrder`, `CS0649 marketEvents/accountEvents ×2`; 0 nuevas). FEED 0 errores/0 warnings (sin cambios).

### ACCEPTANCE
PASS. El market lane sólo puede hablar `echo.ntfeed.v1` al endpoint del feed config (relay); el execution lane sólo `echo.ntx.v1` al endpoint de config (bridge); sin frame ntfeed posible hacia el socket ntx ni comando/evidencia ntx hacia el socket ntfeed (separación estructural en fuente + rechazo mutuo de parsers en wire).

---

## F-D6-EXEC-02 — frame account del execution lane con `resolved` bool

### ROOT CAUSE
La rama exec de `OnTimerSnapshot` serializaba `{"match":…,"resolved":true|false}` (bool) y omitía `discovered`/`balances`, mientras la rama market construía el payload ntfeed correcto con `resolved` como objeto. El parser del bridge exige `Resolved *AccountRecord` (`core/ntx/observations.go:137`, unmarshal estricto). Físico 05:21:08Z (tras hello+auth pasados): `family data does not parse: json: cannot unmarshal bool into Go struct field AccountData.resolved of type ntx.AccountRecord` ⇒ sin account observation ⇒ sin positions/orders ⇒ `recovery barrier failed … no position snapshot observed yet` (+3.692 s, fail-closed correcto).

### CONTRACT VIOLATED
Freeze §6.1/§6.2: las familias de observación reutilizadas llevan **"same payloads as ntfeed"**. El payload ntfeed real (evidence sink, feed lane físico) lleva `resolved` como objeto `{id,name,display_name}` + `discovered[8]` + `balances{}`.

### CHANGE
- Un ÚNICO builder canónico `AccountPayloadJson(discovered, resolvedJson, balancesJson, match)` + `AccountRecordJson(id,name,display_name)`: `resolved` es el objeto AccountRecord tipado con el balance map; publicado con **bytes idénticos en ambas lanes** (`PublishMarketFrame("account", p)` + `PublishExecFrame("account", p)`).
- Identidad preservada: nombre de negocio/proveedor (`name`/`display_name` = `RJARA114411201551`), `Account.Id` runtime donde el contrato lo lleva (`resolved.id`, hint), representación resolved única, semántica de binding/match (`match` = RESOLVED/MISMATCH/DRIFT/DISCOVERY_ONLY; DRIFT ⇒ sin objeto resolved), campos de balance del contrato existente (5 llaves extraídas de la región real `Balances`). Cero campos inventados, cero shapes duales: una forma canónica.
- El parser del bridge NO se tocó (implementa el payload congelado). La forma bool histórica sigue rechazada fail-closed (test negativo con el error exacto).

### TESTS
- `protocol_contract_test.go::TestF_D6_EXEC_02_ExecFixturesParseOnBridgeContract` — la cadena completa exigida: fixture producida por el AddOn (código extraído mecánicamente, compilado y ejecutado en .NET real) → `ntx.ParseFrame` → parser de familia real. Familias: hello, session, account (resolved/mismatch), positions (vacío/no vacío), orders (vacío/no vacío), executions, heartbeat, command_result. Para account resolved: `resolved` deserializa en `ntx.AccountRecord` con identidad íntegra (id "3", name/display_name "RJARA114411201551") + discovered + balances + match.
- `…_AccountPayloadSameOnBothLanes` — el payload account es byte-idéntico en ambas lanes; sólo difiere el envelope (schema).
- `…_OldBoolShapeRejected` — negativo: la forma histórica bool (los bytes exactos del incidente físico, fixture `account-resolved-bool-REJECTED.json`) sigue rechazada con `cannot unmarshal bool into Go struct field AccountData.resolved of type ntx.AccountRecord`.
- `endpoint_guard_test.go::TestF_D6_EXEC_02_AccountPayloadCanonicalBothLanes` — la serialización bool está prohibida en fuente; un solo builder alimenta ambas lanes; `AccountRecordJson` es el único origen del objeto resolved.
- E2E en el barrier: `reallane_barrier_test.go::TestRealLaneBarrier_AdvancesOnAddOnObservationSequence` — hello → account RESOLVED → positions → orders sobre el stack REAL (`ntx.Server` + `Adapter` + `Session`) por TCP real ⇒ barrier completa (`Recovered=true`, 0 mismatches).

### COVERAGE
Los 11 builders extraídos (JsonEscape, FrameJson, HelloDataJson, AccountRecordJson, AccountPayloadJson, CommandResultPayload, PositionRecordJson, OrderRecordJson, ExecutionRecordJson, MarketHeartbeatPayload, ExecHeartbeatPayload) se ejercitan comportamentalmente al 100% vía fixtures (cada builder produce al menos una fixture parseada por el parser real); los guards estructurales cubren el wiring. Cobertura del `RunRecoveryBarrier` real: 76.7% con sólo los 4 tests nuevos del harness (la suite completa del paquete queda verde).

### COMPILE
EXEC 0 errores (mismas 3 warnings preexistentes; 0 nuevas).

### ACCEPTANCE
PASS. El frame account del execution lane es el payload congelado; deserializa en el `AccountRecord` real del bridge; la forma bool está estructuralmente imposible en fuente y sigue rechazada en wire.

---

## F-D6-EXEC-03 — silencio post-reject (verificación + remediación mínima)

### DETERMINACIÓN
D1/D2 explican POR QUÉ el market y el exec lane eran rechazados, pero NO explican el silencio: la cadencia congelada (≤5–10 s) produjo dial #2 (+5 s, identidad nueva, auth re-pasada — reconexión real demostrada) y luego CERO dials ≥15 min en ambas lanes. Por inspección de fuente existe una clase de mecanismos capaz de producir exactamente ese cuadro: un `Send` bloqueante sobre socket muerto/half-open sostiene el lock del lane y el slow tick (que ejecuta `EnsureMarketLane` ANTES de `EnsureExecLane` bajo el mismo catch) deja de alcanzar el scan del otro lane ⇒ silencio de ambas lanes simultáneo (el patrón observado). No discriminable agente-side (ACL log NT); el mecanismo exacto lo discriminará el log NT del próximo ciclo físico, pero la clase queda cerrada por construcción.

### CHANGE (promovido a finding y corregido al mínimo)
1. `s.SendTimeout = 3000` en ambos sockets: un peer muerto falla la escritura acotada y el lane re-entra al loop de reconexión en vez de sostener el lock indefinidamente.
2. `OnSlowTick` con aislamiento por lane (try/catch propio por lane): el fallo de un lane jamás salta el scan de reconexión del otro.
3. `ExecReadLoop` cierra el socket en EOF (sin handles huérfanos) y restaura la cadencia +5 s.
4. Contrato de reconexión intacto y pineado: cada (re)dial instala identidad de sesión NUEVA + seq 0 (F-S2-01; físicamente demostrado en el dial #2 del 2026-10-04).

### TESTS
- `endpoint_guard_test.go::TestF_D6_EXEC_03_ReconnectLoopSurvivesRemoteReject` — send acotado en ambos sockets, aislamiento por lane en el slow tick, cierre de socket en EOF, identidad nueva+seq 0 en cada dial.
- Behavioral (loop real): `TestRealLaneBarrier_*` demuestran que tras rechazos/respuestas fail-closed del stack real el lane queda operativo; la reconexión física con identidad nueva ya observada en el runtime real (dial #2 del intento 4) + el pinneado estructural cierran el ciclo. El rechazo remoto con reconexión posterior queda demostrado por: (a) física — dial #2 a +5 s con identidad nueva y auth re-pasada; (b) fuente — el EOF path y el send-failure path restauran `execNextConnect` (+5 s/+10 s) sin cap; (c) guard — SendTimeout+aislamiento hacen imposible la clase de wedge identificada.

### COVERAGE / COMPILE
Cubierto por guard estructural + harness; EXEC 0 errores.

### ACCEPTANCE
`F_D6_EXEC_03 = FIXED` (promovido y corregido al mínimo; no `CLOSED_AS_CONSEQUENCE` porque D1/D2 no explican el silencio ≥15 min observado). `RECONNECT_AFTER_REMOTE_REJECT = PASS`.

---

## /protocol_contract_tests — resumen de la cadena de compatibilidad

`EchoExecutionAddOn.cs` (builders extraídos MECÁNICAMENTE por marcadores, sólo rewrite de visibilidad — `proto-harness/gen_proto_harness.py`) → compilado con `csc.exe` .NET Framework real (dev-win .132) → 15 fixtures wire deterministas (tokens sintéticos, sesiones/ts/seq fijos) → commiteadas en `proto-harness/fixtures/` → `protocol_contract_test.go` las corre por `ntx.ParseFrame` + parsers de familia reales (y `ntfeed.ParseFrame` para el lane market). Negativo incluido (bool shape). No-grep: los tests consumen bytes producidos por el código fuente real.

**Nota de proceso:** en la PRIMERA corrida en .NET real el arnés detectó un defecto del refactor (falta de la comilla de cierre de `ts_utc` en `FrameJson` — la comilla vivía en el literal adyacente del código original). Corregido antes del stage; las 15 fixtures finales parsean. Esto valida la cadena de tests exigida (hubiera rechazado la build defectuosa).

## /endpoint_tests

Deterministas, sin orden-egress: (1) fuente — separación estructural por método (guards); (2) wire — cada schema es rechazado por el parser del endpoint ajeno y aceptado por el propio (`EndpointParsersRejectForeignSchema`). Market: `echo.ntfeed.v1` → feed config endpoint (relay :9770). Exec: `echo.ntx.v1` → `ntx_host:ntx_port` (:9771). Contaminación cruzada: NONE.

## /recovery_barrier_contract

`internal/session/reallane_barrier_test.go` — stack REAL (`ntx.Server` + `ninjatrader.Adapter` + `session.Session`), frames AddOn reales por TCP:
- `hello → account RESOLVED → positions → orders` ⇒ barrier AVANZA (sin debilitamiento ni bypass).
- positions ausentes ⇒ `barrier: reconcile: ninjatrader: no position snapshot observed yet` (el fail-closed físico del 2026-10-04, reproducido).
- orders ausentes con record SUBMITTING en journal ⇒ converge AMBIGUOUS, mismatch `M2_UNRESOLVED_ABSENCE` visible, `ReadyNewRisk=false` (nuevo riesgo bloqueado).
- account incorrecto ⇒ barrier se detiene en `verify binding` (Name-primary §3.2, nunca resuelve).

## /account_identity

Modelo congelado preservado: durable Echo `E2T-GAU50-01` · provider/business `RJARA114411201551` (Name-primary, resolución única) · NT `Account.Id` "3" = hint runtime/evidencia. Sin fallback por Id, sin rediseño de account management; el drift sigue degradando fail-closed (`match=DRIFT` ⇒ sin objeto resolved; el adapter mantiene su gate propio de hello).

## /config

Sin regresión del parser fix: `echo-execution-addon.json` **sin cambios** (`9ca3fddc…`), parsea pretty con `ntx_host=192.168.31.161`, `ntx_port=9771`, `account_name=RJARA114411201551`; token secreto (sólo `len=64` en VERIFY). D1 NO requirió claves nuevas en la config de ejecución: el endpoint ntfeed se resuelve del feed config certificado existente (`bridge_host`/`bridge_port` de `echo-feed-addon.json`), sin valores inventados.

## /install_verify

- `INSTALL-ECHO-D6.ps1` **sin cambios** (`635ab76a…`); dry-run sandbox fresco: **PASS** (1 declaración por clase, SHA256 bundle↔destino OK, config host/port/account OK, jamás imprime token).
- `VERIFY-ECHO-D6.ps1` actualizado (`bd68f529…`): agrega chequeo READ-ONLY del feed config (`bridge_host`/`bridge_port` parsean, `auth_token present=True len=64`) — el market lane depende de ese archivo y VERIFY lo hace visible. Dry-runs sandbox: PASS-path **PASS** (`bridge_host=192.168.31.161 bridge_port=9770` visible, sin tokens); fail-path (feed config ausente) **FAIL** con mensaje explicativo y exit 1. Ambos scripts con la forma owner exacta: `powershell.exe -ExecutionPolicy Bypass -File …`.

## /bundle

`C:\Temp\EchoD6Bundle` re-stageado DESDE ESTE HEAD (repo = autoridad de fuente; sin archivos sueltos viejos):

| Archivo | SHA256 |
|---|---|
| `EchoExecutionAddOn.cs` | `7f76b30e3c60961d85a193b464997678990d99416c9178c8a11f685d61239441` (= `git show 32baeaeb`, byte-idéntico repo↔bundle) |
| `EchoFeedAddOn.cs` | `581a7087b1b870c78ac43e67027e5edaacf59134f4bf5f03d8b9aec9d7fd5ae4` (sin cambios, certificado) |
| `echo-execution-addon.json` | `9ca3fddc31330b2d5b485fd0869801b486b1443972bbf5ba50c56862feeea71b` (sin cambios) |
| `INSTALL-ECHO-D6.ps1` | `635ab76a7785b9862d053f2d51e0e142c27d32743f7e068ae608245af03a9af8` (sin cambios) |
| `VERIFY-ECHO-D6.ps1` | `bd68f52906ee722eafef365c28b7655673286f8ae15b4361c610dd5bdc8adbf4` |
| `SHA256SUMS.txt` | regenerado desde la ubicación stageada (3 archivos producto) |
| `BUILD-INFO.txt` | `a4fcc9fb3c9632bd13c8609243c3ddface726a3a8a970c1ecefc8849b0f37e0b` |

El arnés de parser (paralelo del anterior) queda como evidencia auxiliar FUERA del payload de instalación (bundle mínimo de 7, convención canónica).

## /csharp — shadow compile físico

dev-win 192.168.31.132, NT 8.1.8.3 físico, `csc.exe` .NET Framework64 v4.0.30319, `/t:library`, refs `NinjaTrader.Core.dll` (`C:\Program Files\NinjaTrader 8\bin\`), `NinjaTrader.Gui.dll`, `WindowsBase.dll`:

| Target | Errores | Warnings |
|---|---|---|
| EchoFeedAddOn.cs (sin cambios) | **0** | 0 |
| EchoExecutionAddOn.cs (remediación) | **0** | 3 preexistentes, 0 nuevas (`CS0612 Account.CreateOrder`, `CS0649 marketEvents/accountEvents ×2`) |

Staging `C:\Temp\d6exec-proto\` — DLLs/exe de salida SOLO en staging; NADA instalado en NinjaTrader.

## /coverage — metodología

- Código Go de producto: SIN cambios (sólo tests/fixtures/harness). Suite completa del módulo `futures-bridge`: **14/14 paquetes ok**.
- C# cambiado (medible): los 11 builders puros — 100% ejercitados comportamentalmente vía fixtures sobre .NET real y validados byte-a-byte por el parser real del bridge; wiring de lanes/reconexión — pineado por guards estructurales sobre el fuente real; barrier bridge-side — `RunRecoveryBarrier` 76.7% con sólo los 4 tests nuevos (suite del paquete completa verde).
- Protocol compatibility tests mandatorios: presentes y verdes aunque la cobertura estática C# sea ajena al runtime NT (metodología aceptada Shot 3 / parser-fix).

## /close

```text
D6_EXECUTION_PROTOCOL_REMEDIATION = PASS

BASELINE_SHA:
ffa493d8d179c9f9374d0a935e7916be15367ce8

FINAL_SHA:
32baeaeb49cff8b4227b850d7a575549bbcf54a2

F_D6_EXEC_01:
PASS

MARKET_LANE_ENDPOINT:
192.168.31.161:9770 (echo-feed-addon.json bridge_host/bridge_port, nt-feed-relay; schema echo.ntfeed.v1, token del mismo feed config)

EXECUTION_LANE_ENDPOINT:
192.168.31.161:9771 (echo-execution-addon.json ntx_host/ntx_port, futures-bridge; schema echo.ntx.v1, token ntx propio)

CROSS_PROTOCOL_CONTAMINATION:
NONE (separación estructural por método en fuente + rechazo mutuo de parsers por wire, ambos pineados por tests)

F_D6_EXEC_02:
PASS

ACCOUNT_RESOLVED_SHAPE:
objeto AccountRecord tipado {id,name,display_name} + discovered[] + balances{} + match, bytes idénticos en ambas lanes (freeze §6.2 same-payloads-as-ntfeed)

NTX_ACCOUNT_FRAME_COMPATIBILITY:
PASS (fixtures AddOn reales → ntx.ParseFrame + ParseAccountData → aceptado; resolved deserializa en ntx.AccountRecord con identidad íntegra)

OLD_BOOL_SHAPE_REJECTED:
PASS (fixture histórica → "cannot unmarshal bool into Go struct field AccountData.resolved of type ntx.AccountRecord"; parser sin debilitar)

RECOVERY_BARRIER_CONTRACT:
PASS (barrier real avanza con hello/account-RESOLVED/positions/orders; fail-closed preservado: sin positions ⇒ error físico reproducido; SUBMITTING ausente ⇒ AMBIGUOUS + ReadyNewRisk=false; account incorrecto ⇒ verify binding falla)

F_D6_EXEC_03:
FIXED (promovido: D1/D2 no explican el silencio ≥15 min; corrección mínima: SendTimeout 3s ambos sockets + scan por-lane aislado + socket liberado en EOF)

RECONNECT_AFTER_REMOTE_REJECT:
PASS (físico: dial #2 a +5 s con identidad nueva + seq 0 + auth re-pasada; fuente: EOF/send-failure restauran cadencia sin cap; guard: clase de wedge cerrada)

ACCOUNT_IDENTITY:
PASS (E2T-GAU50-01 durable; RJARA114411201551 Name-primary; Id "3" hint; sin fallback por Id; drift fail-closed)

PROTOCOL_TESTS:
15 fixtures del arnés mecánico (.NET real) parseadas por la cadena parser real del bridge (hello/session/account/positions/orders/executions/heartbeat/command_result) + negativo bool rechazado + rechazo cruzado de endpoints; guards estructurales endpoint/reconnect/payload; harness de barrier real-lane 4/4

CHANGED_CODE_COVERAGE:
builders extraídos 100% ejercitados vía fixtures (.NET real); wiring D1/D3 pineado estructuralmente; RunRecoveryBarrier 76.7% con los 4 tests nuevos; suite módulo 14/14 ok; sin cambios de producto Go

FEED_SHADOW_COMPILE:
PASS (0 errores, 0 warnings)

EXEC_SHADOW_COMPILE:
PASS (0 errores, 3 warnings preexistentes, 0 nuevas)

BUNDLE_PATH:
C:\Temp\EchoD6Bundle

INSTALL_SCRIPT:
PASS (dry-run sandbox end-to-end)

VERIFY_SCRIPT:
PASS (dry-run sandbox pass-path; fail-path verifica FAIL correcto sin feed config)

PHYSICAL_ORDERS_SENT:
0

OWNER_DECISION_REQUIRED:
NONE

NEXT_OWNER_ACTION:
Cerrar NinjaTrader → powershell.exe -ExecutionPolicy Bypass -File "C:\Temp\EchoD6Bundle\INSTALL-ECHO-D6.ps1" → powershell.exe -ExecutionPolicy Bypass -File "C:\Temp\EchoD6Bundle\VERIFY-ECHO-D6.ps1" → abrir NinjaTrader.

NEXT_MANAGER_ACTION:
Tras el ciclo Owner (instalación corregida), certificación fresh-context C→K (no realizada aquí): comprobar en log NT el market lane conectado al relay (hello [ntfeed] sin rechazos) y el exec lane con sesión estable + account parseado + barrier completado, luego el ladder congelado en la primera ventana admisible lun 2026-10-05 00:00–15:50 CT. OD-D6-1 sigue AUTHORIZED y SIN consumir (0 órdenes en 4 intentos). No emitir EF_D6_E2E_PASS.
```

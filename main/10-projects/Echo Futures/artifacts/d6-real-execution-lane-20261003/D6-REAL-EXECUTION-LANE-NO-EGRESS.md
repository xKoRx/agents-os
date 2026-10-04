# Echo Futures — D6 Real Execution Lane Post-Owner-Install (NO EGRESS) — 2026-10-03

**Shot:** D6 — REAL EXECUTION LANE, POST OWNER INSTALL — TOP Senior Physical Integration / Certification Lead (one-shot, fresh context; no Manager, no Owner)
**Date:** 2026-10-03 (sábado; evidencia UTC ≈19:37Z–20:25Z, local -03 ≈16:37–17:25; CME cerrado desde vie 16:00 CT)
**Project:** [[Echo Futures]]
**Owner authorization:** OD-D6-1 = AUTHORIZED y VIGENTE (sin consumir: `PHYSICAL_ORDERS_SENT = MODIFIED = CANCELLED = 0`); OD-D6-4 standing (ciclo de instalación owner).
**Baseline / Final SHA:** `xKoRx/echo@40102ea5a44be9a618ac12529e6f0e9fdfd46d34` (`origin/feature/d6-shot1-execution-vertical`) — worktree limpio verificado al inicio y al cierre; **cero commits, cero cambios de producto**.
**Verdict:** `D6_REAL_EXECUTION_LANE_NO_EGRESS = FAIL` — la certificación del lane NO se completó: el **EchoExecutionAddOn real nunca se cargó en NinjaTrader** tras el ciclo owner W1 (cero evidencia runtime de carga, evidencia multiplicada y re-verificada con el proceso NT sin cambios). No es defecto de producto (los mismos bytes pasaron shadow-compile físico en Shot 3 contra 8.1.8.3; el lado bridge/transporte permanece certificado). Tampoco es REMEDIATION_REQUIRED (no hay candidato de defecto de código): es un **fallo de instalación/arranque lado NT** que exige repetir W1 con verificación. Toda la parte agent-side ejecutable fue ejecutada y quedó en fail-closed probado; el estado final es **G-EGRESS-0** probado, no asumido.

---

## A — VERIFY OWNER INSTALL

**Staged bundle (C:\Temp, dev-win): re-verificado HOY byte-idéntico a HEAD con método probado en el mismo host:**

| Archivo | SHA256 (hoy) | == HEAD |
|---|---|---|
| `EchoExecutionAddOn.cs` | `b2a29a3608cf1e1b767844156c8d03f23fd324e668fab1efde97489fd885729a` | ✔ |
| `EchoFeedAddOn.cs` | `581a7087b1b870c78ac43e67027e5edaacf59134f4bf5f03d8b9aec9d7fd5ae4` | ✔ |
| `echo-execution-addon.json` | `9ca3fddc31330b2d5b485fd0869801b486b1443972bbf5ba50c56862feeea71b` | ✔ |

**Installed files (perfil KoR): NO verificables por el agente — estructuralmente imposible, probado:**
- ACL: `C:\Users\KoR\Documents` → `UnauthorizedAccessException` (5.ª re-probe en 4 sesiones); `dir` sobre `NINJAT~1` → doble error PermissionDenied + PathNotFound (deny en toda la raíz del perfil; ni siquiera se resuelven los short names 8.3).
- **Artefacto de quoting demostrado por contra-prueba:** `certutil -hashfile "C:\...\NinjaTrader 8\..."` (con espacio y comillas) devolvió `FILE_NOT_FOUND` incluso para el `EchoFeedAddOn.cs` que SÍ está corriendo; el mismo comando sobre `C:\Temp\EchoFeedAddOn.cs` (sin espacios) funciona y da el hash correcto. Las comillas se stripppean en el transporte ⇒ ese resultado nunca fue evidencia de ausencia. `OWNER_W1_VERIFIED = FAIL` por combinación de: bytes instalados no verificables (ACL) + evidencia runtime de carga negativa (§B).

## B — VERIFY NINJATRADER RESTART + ADDON LOAD

- **Restart confirmado:** NinjaTrader PID **1876 → 8700** (netstat dev-win: `TCP 192.168.31.132:58256 → 192.168.31.161:9770 ESTABLISHED, PID 8700`). StartTime no consultable (ACL — igual que weekend); el instante del restart queda fijado por el hello de la sesión feed nueva.
- **Feed AddOn cargado y compilado — PASS:** sesión nueva `64803b9b23534187894ae1a1a49db817`, hello `2026-10-03T19:38:33.657Z` seq 0 (`addon_version 1.0.0`, `nt_version 8.1.8.3`, `expected_account_id "3"`, `expected_account_name RJARA114411201551`, `instruments ["NQ 12-26"]`), `reconnects:1`; families account/positions/orders/heartbeat cada ~10 s desde entonces. Un AddOn que no compila no publica frames ⇒ compilación del feed probada físicamente.
- **EchoExecutionAddOn cargado — FAIL (evidencia runtime, no presencia de archivos):** entre el restart (19:38:33Z) y el cierre (~20:25Z), con el bridge LISTENING en `*:9771` desde 19:46:20Z y `Test-NetConnection 192.168.31.161 -Port 9771 = True` desde el propio host NT:
  - **0 intentos de conexión** del exec lane en ~40 min con cadencia de diseño ≤10 s (fuente @ HEAD: timers 1 s scan / 2 s ticks al cargar, `EchoExecutionAddOn.cs:68-83`; dial con retry 10 s, `:405-415`; config ausente ⇒ lane down silencioso con warning, `:119-122`).
  - 0 hellos `[ntx]`, 0 líneas de auth en el journal del bridge; dev-win `netstat :9771` vacío en todos los snapshots (ni SYN_SENT; con LISTEN activo un AddOn cargado quedaría ESTABLISHED).
  - **PID 8700 sin cambio en la re-verificación final** ⇒ ningún evento NT-side posterior; la evidencia permanece vigente.
- **Compile state:** `NINJATRADER_COMPILE_ERRORS = 0` no demostrable para el exec AddOn (sin señal runtime de ningún tipo). `C:\Temp\compile-errors.txt` NO existe (señal débil — sólo la crea el owner si ve errores). Los mismos bytes del exec AddOn pasaron shadow-compile físico contra las DLL reales 8.1.8.3 en Shot 3 (0 errores, 3 warnings preexistentes) ⇒ **candidato de defecto de producto refutado**. Variantes restantes (todas owner-side): `.cs` no presente en target · compile-fail en el arranque real · config JSON no encontrado en `NinjaTrader 8\echo\`.

## C — PREPARE BRIDGE FOR REAL ADDON

Verificado antes de habilitar la sesión (todo PASS): release exacta `40102ea5` (`vcs.revision=40102ea5…`, `vcs.modified=false`, SHA256 binario `484b550b…`, desplegada weekend); journal M2 limpio (directorio vacío); `ntx/auth-token` presente (64 hex, sin impresión); binding ETCD correcto (12 claves exactas: enabled/ALLOWED/GAU50-EVAL v1/RJARA114411201551/Id "3"/America/Chicago/reset 17:00/NQ 12-26/transport NINJATRADER_BRIDGE); sin clave de sesión vieja (`futures-bridge/accounts` ausente, lectura exacta); topic `echo.order-commands.E2T-GAU50-01.v1` inexistente (list_topics completo) ⇒ 0 comandos replayables. Secuencia respetada según el hallazgo weekend (el shell no reintenta la sesión): el AddOn debía estar conectando antes del arranque — no lo estuvo (§B), y el barrier falló cerrado a los ~10 s como el despacho anticipa.

## D — ENABLE MINIMUM EXECUTION SESSION

- Escritura guardada ETCD `/echo/development/futures-bridge/accounts` = `E2T-GAU50-01`: pre-lectura exacta ausente → put → read-back exacto (version 1) → cross-check MCP RO independiente (`E2T-GAU50-01`, size 12).
- Bridge arrancado: **PID 1737260**, release `40102ea5`, **listener `*:9771`** (`ss`), `account session built` (`echo.execution_account E2T-GAU50-01`, `echo.topic echo.order-commands.E2T-GAU50-01.v1`, `transport NINJATRADER_BRIDGE`).
- **TCP peer / sesión autenticada / session ID / secuencia: NINGUNO** — cero clientes llegaron al listener (§B). 0 comandos en todo momento.

## E — REAL ACCOUNT BINDING

- **Desde el EchoExecutionAddOn real: NOT_RUN** (nunca hubo sesión).
- **Evidencia de identidad viva del mismo perfil (feed AddOn, mismo proceso NT, sink sin máscara):** discovery 8 cuentas (`Backtest`, `Playback101`, `Sim101`, 5× `RJARA…`), **exactamente 1 match** para `RJARA114411201551`, `match RESOLVED`, **NT `Account.Id "3"` == hint ETCD — 5.ª sesión consecutiva** (2/2 N1 + intento 1 + weekend + hoy). Binding Name-primary intacto; `E2T-GAU50-01` ↔ `RJARA114411201551` sin drift.

## F — REAL ACCOUNT OBSERVATION

- **Por el exec AddOn real: NOT_RUN.** No se fabricaron snapshots.
- **Observación real del feed lane (mismo AddOn fuente, proceso NT real):** positions `[]`, orders `[]` en todos los ciclos; balances `NLV/cash 50000/50000`, `BP/uPnL/rPnL 0/0/0` (**variante demo 01-oct** — a las 14:42Z el mismo camino exponía 0/0/0/0/0; documentada, no estado inesperado). Las observaciones alcanzan el runtime (Kafka p4 avanzó 5476458 → 5476461 con el replay estático de la sesión nueva, `ingress_ref log_identity ninjatrader-addon/64803b9b`).

## G — REAL RECOVERY BARRIER

**FAIL (fail-closed correcto, PASS imposible sin AddOn):** el barrier falló a los ~10 s con razón exacta `session: recovery barrier failed for E2T-GAU50-01: barrier: connect: ninjatrader: no authenticated AddOn session on the execution lane`; `account session exited` sin retry del shell (comportamiento documentado weekend §3). Sin observaciones venue reales del exec lane, el barrier se negó a completar — **no se debilitó la reconciliación ni se fabricaron snapshots**. `UnknownLiveOrders = 0`, `AccountMismatch = 0`, `ambiguous journal = 0` (journal M2 vacío).

## H — REAL SESSION RECONNECT / FENCING (F-S2-01 / F-S2-04)

**NOT_RUN** — requieren el EchoExecutionAddOn real; el despacho prohíbe probe como sustituto y no se usó. Lado server/transporte: permanece certificado weekend §5 (auth negativa constant-time, fencing B→A con cierre inmediato, reconnect identidad nueva + seq 0) — mismos binarios, mismo SHA, sin cambios.

## I — BRIDGE RESTART RECOVERY

**NOT_RUN con AddOn real** (sin cliente que reconecte no ejercita nada nuevo; weekend §8 certificó 2× restart con journal 0-phantom y reconexión <1.5 s lado transporte). En esta corrida el bridge corrió una sola vez (19:46:20Z → teardown 20:0xZ) sin recibir jamás una conexión.

## J — NINJATRADER RESTART RECOVERY

Restart NT automatizado: **imposible por ACL** (sesión owner interactiva; tasklist ya denegado). Se **reutiliza explícitamente** el restart owner de las 19:38:33Z como evidencia equivalente (permitido por el despacho): feed AddOn compiló/cargó/recuperó ✔; **execution lane NO recuperó** (AddOn sin evidencia de carga) ⇒ `NINJATRADER_RESTART_RECOVERY = FAIL` por causa de instalación, no por mecánica del restart. Estado post-restart consistente: cuenta rediscovery 1/8, Id "3", sin corrupción de estado observable.

## K — G_HORIZON REAL PRECHECK

`G_HORIZON_PRECHECK = PARTIAL_NEEDS_CREATED_ORDER` — la cuenta GAU50 no tiene ningún evento histórico de la vertical (0 órdenes acumuladas) y las superficies `LookbackDays*`/historia sólo son inspectables desde dentro de NT con el AddOn cargado. **No se creó orden para mejorar el resultado.** Al ladder live le queda probar: retención real `LookbackDays*`, retención `order.Name`/`Order.OrderId`/`ExecutionId` realtime↔historia↔restart (G-ID-Retention + G-HORIZON con la primera orden del ciclo G-E2E).

## L — CURRENT READINESS

Capturada con el bridge corriendo (cada 30 s, toda la corrida): `ready_new_risk=false`, blockers exactamente los esperados para AddOn ausente + mercado cerrado:
`[NOT_AUTHENTICATED NOT_CONNECTED ORDER_EXECUTION_EVENT_STREAM_NOT_HEALTHY POSITION_NOT_FRESH PROVIDER_ACCOUNT_BINDING_NOT_VERIFIED RECONCILIATION_AUTHORITY_UNAVAILABLE STATIC_ELIGIBILITY_NOT_ELIGIBLE SUBMISSION_CAPABILITIES_NOT_EXACT_READY]`, `ambiguous_orders=0 mismatches=0 dropped_commands=0 recovered=false`.
Separación de estado: **EXECUTION TRANSPORT** = bridge-side certificado y listo para re-enable (hoy detenido, G-EGRESS-0) · **ACCOUNT/BINDING** = PASS feed-side vivo · **RECOVERY** = FAIL sin AddOn · **MARKET_FRESHNESS = STALE** (último `event_ts 2026-10-02T21:38:25.95Z`, edad ≈22 h >> bound 30 s; Kafka p4 5476461 = replay estático, no eventos nuevos) · **NEW_RISK_READY = NO** (doble fail-closed: freshness + ventana GAU50-EVAL L–V). No se manipuló ningún timestamp ni readiness.

## M — SUNDAY G-REALTIME READINESS

`SUNDAY_G_REALTIME_RUNBOOK = READY` — procedimiento determinista, **ya ejecutado hoy como prueba** (misma llamada, resultado reproducible), sin investigación restante:

```text
CUÁNDO: domingo 2026-10-04 ≥ 17:00 CT (22:00Z; reopen CME). Duración ~2 min. Sin bridge, sin órdenes.
1. mcp aranea-kafka-dev-admin consume_messages topic=echo.futures.market-feed-candidates.v1 partition=4 offset=latest limit=1
2. Verificar: stream_id NQ:NQZ6, source NINJATRADER_ADDON, event_ts NUEVO (≠ 2026-10-02T21:38:25.95Z).
3. event_age = now − event_ts ; receive_lag = receive_ts − event_ts.
4. Repetir (2) tras ≥30 s: Kafka offsets deben avanzar (2 tomas).
5. G-REALTIME provisional FRESH ⇔ event_age < 30 s (bound frozen) en ambas tomas con calendar activo.
   Alternativa equivalente: herramienta repo `kafka-last -n 1 echo.futures.market-feed-candidates.v1` (patrón scratch-weekend).
6. Si STALE con feed vivo en ventana ⇒ escalar OD-D6-3 (condicional). NO ejecutar ladder el domingo (engine: Sunday fuera de days ⇒ WINDOW_CLOSED ⇒ DENY).
```

## N — MONDAY LIVE LADDER READINESS

`MONDAY_PHYSICAL_LADDER_RUNBOOK = READY` — secuencia restante completa, sin gaps de investigación; **gate 0 = fix owner W1 verificado** (§9 checklist):

```text
0. Owner re-ciclo W1 con verificación → señal de éxito observable: dial :9771 cada ≤10 s (netstat dev-win / journal bridge).
1. Re-despacho pasos C–K de este artifact (enable sesión + bridge + barrier con AddOn real + D–I): ~5 min dentro de la ventana.
2. market FRESH (runbook M) + ventana GAU50-EVAL abierta (lun 2026-10-05 00:00–15:50 CT o 17:10–23:59 CT).
3. Account observations/recovery barrier con venue real (G de este artifact → PASS).
4. Warm-up (config de run Manager, densidad Min5mPerH4Region=8 frozen).
5. RUN_START (dentro de ventana; OD-D6-1 vigente, mismo scope).
6. Escenario congelado G-E2E: MARKET entry + STOP_MARKET venue-held + tighten cancel/replace + cancel + flat + drill restart con protectora working + 0 unknown live orders (freeze §14.13; NQ/NQZ6; cap GROSS 6; SL/TP 2000/1500 day1; side/qty = output frozen, jamás parámetro humano).
7. G-STOP → 8. G-ID-Retention → 9. G-HORIZON (evidencia restante) → 10. G-E2E → 11. G-PERF.
FIRST_PHYSICAL_CERT_SCENARIO = FULLY_DEFINED · MISSING_PHYSICAL_PARAMETERS = NONE. No ejecutar hoy.
```

## /final_safety_state — probado al cierre (no asumido)

- **G-EGRESS-0 restaurado y verificado:** unidad `echo-futures-bridge` **inactive** (`reset-failed` tras stop) + **disabled**; `:9771` FREE (`ss`); clave ETCD `futures-bridge/accounts` **eliminada** con ciclo guardado (pre-read exacta `E2T-GAU50-01` → delete → read-back ausente → listing exacto **21 claves**, `session_key_present=False`); quedan inertes release/journal-root/auth-token/12 claves binding/7 nt-feed.
- **Feed lane conectado y observando** (relay + AddOn feed): cuenta observable, `RESOLVED` vivo.
- **AddOns instalados en el perfil owner** (afirmación owner; agente NO puede verificar bytes — ACL; runtime: feed activo, exec no cargado).
- **No LIVE run; no pending order command; no unresolved ambiguity** (journal vacío, topic de comandos inexistente, `COMMAND_FRAME` grep = 0); **new-risk configurationally disabled** (sin sesión habilitada + sin topic M1 + ventana/freshness DENY).
- Nota operacional: el exec AddOn, si se carga en un futuro restart, dials `:9771` y recibe refusal — sin estado, sin riesgo (no hay listener ni sesión habilitada).
- Gotcha del MCP RO ETCD re-observado (2.ª vez): tras el borrado devolvió `"17:00"` (hermana `day-boundary-reset`) para la clave de sesiones — la lectura exacta del cliente crudo es la autoridad.

## /product_changes

**NONE.** Cero commits, cero cambios de source (worktree limpio al inicio y al cierre, `HEAD == origin == 40102ea5`). No se demostró candidato de defecto de producto (mismos bytes shadow-compilados OK en Shot 3; transporte y bridge verificados hoy) ⇒ no aplica REMEDIATION_REQUIRED de código.

## /close — Final handoff

```text
D6_REAL_EXECUTION_LANE_NO_EGRESS =
FAIL (certificación no completada: EchoExecutionAddOn real nunca se cargó en NT tras el ciclo owner W1; fallo de instalación/arranque NT-side, no defecto de producto; todo lo agent-side ejecutado y fail-closed probado)

BASELINE_SHA:
40102ea5a44be9a618ac12529e6f0e9fdfd46d34

FINAL_SHA:
40102ea5a44be9a618ac12529e6f0e9fdfd46d34 (cero commits; worktree limpio al cierre; delta infra neto CERO)

OWNER_W1_VERIFIED:
FAIL (bytes instalados no verificables por ACL estructural — probado con contra-prueba de quoting; evidencia runtime de carga NEGATIVA: 0 dials en ~40 min con cadencia de diseño ≤10 s, 0 hellos, 0 sockets)

NINJATRADER_PID:
8700 (antes 1876; StartTime no consultable por ACL; restart probado por PID + hello feed 2026-10-03T19:38:33.657Z seq 0; PID sin cambio en re-verificación final)

NINJATRADER_COMPILE:
FAIL (feed AddOn: compilación probada físicamente — corre y publica; exec AddOn: cero evidencia runtime de carga; compile-errors.txt no presente (señal débil); shadow-compile Shot 3 de los mismos bytes = PASS ⇒ defecto de producto refutado)

EXECUTION_ADDON_LOADED:
FAIL

EXECUTION_LANE_REAL:
FAIL (bloqueado por AddOn ausente; lado bridge/transporte permanece certificado weekend §3/§5/§8 — mismo SHA y binarios)

REAL_SESSION_ID_INITIAL:
NONE (ningún cliente autenticó jamás en :9771 durante esta corrida)

ACCOUNT_BINDING:
PASS feed-side vivo (discovery 1/8 match RESOLVED; RJARA114411201551 = NT Account.Id "3" == hint ETCD, 5.ª sesión consecutiva; Name-primary intacto) · exec-side NOT_RUN

CURRENT_NT_ACCOUNT_ID:
"3"

ACCOUNT_OBSERVATION:
FAIL por el exec lane (NOT_RUN, sin datos fabricados) · feed-lane real documentado: positions []/orders [] todos los ciclos, balances 50000/50000 variante demo, observaciones llegan al runtime (Kafka p4 replay de sesión nueva)

REAL_RECOVERY_BARRIER:
FAIL — fail-closed correcto con razón exacta "no authenticated AddOn session on the execution lane"; PASS imposible sin AddOn; reconciliación no debilitada; 0 UnknownLiveOrders / 0 AccountMismatch / journal vacío

REAL_SESSION_RECONNECT:
FAIL (NOT_RUN — sin AddOn; probe prohibido como sustituto y no usado)

REAL_SESSION_FENCING:
FAIL (NOT_RUN — ídem; F-S2-01/04 server-side certificados weekend)

BRIDGE_RESTART_RECOVERY:
FAIL (NOT_RUN con AddOn real; weekend PASS lado transporte vigente)

NINJATRADER_RESTART_RECOVERY:
FAIL (restart owner 19:38:33Z reutilizado como evidencia equivalente — permitido por despacho: feed recuperó ✔, execution lane no recuperó ✘ por instalación; sin corrupción de estado)

G_HORIZON_PRECHECK:
PARTIAL_NEEDS_CREATED_ORDER (cuenta GAU50 sin historial de la vertical; superficies LookbackDays*/historia requieren AddOn dentro de NT; NO se creó orden para mejorar el resultado)

EXECUTION_TRANSPORT_READY:
NO (G-EGRESS-0 al cierre por final_safety_state; bridge-side certificado y listo para re-enable en ~1 min)

CURRENT_MARKET_FRESHNESS:
STALE (event_ts 2026-10-02T21:38:25.95Z, edad ≈22 h >> bound 30 s; p4 offset 5476461 = replay estático de la sesión nueva, no eventos nuevos)

NEW_RISK_READY:
NO

SUNDAY_G_REALTIME_RUNBOOK:
READY (procedimiento determinista §M, ya probado hoy con la misma llamada; sin investigación restante)

MONDAY_PHYSICAL_LADDER_RUNBOOK:
READY (secuencia §N completa; gate 0 = fix owner W1 verificado; ventana admisible lun 2026-10-05 00:00–15:50 CT / evening 17:10–23:59 CT)

FIRST_PHYSICAL_CERT_SCENARIO:
FULLY_DEFINED (freeze §14.13; NQ/NQZ6; cap GROSS 6; SL/TP 2000/1500 day1; side/qty = output frozen de Strategy+GerardMM)

MISSING_PHYSICAL_PARAMETERS:
NONE

FINAL_SAFETY_STATE:
G-EGRESS-0 PROBADO (unidad inactive+disabled, :9771 FREE, accounts key eliminada con lectura exacta 21 claves; feed lane conectado y observando; AddOns lado owner — bytes no agent-verificables por ACL; 0 LIVE run; 0 comandos; 0 ambigüedad; new-risk configurationally disabled)

PHYSICAL_ORDERS_SENT:
0

PHYSICAL_ORDERS_MODIFIED:
0

PHYSICAL_ORDERS_CANCELLED:
0

PRODUCT_CODE_CHANGES:
NONE

OWNER_DECISION_REQUIRED:
Repetir W1 CON VERIFICACIÓN (no decisión nueva — mismo ciclo standing OD-D6-4): (1) verificar desde su sesión que existen los 3 archivos en target — EchoExecutionAddOn.cs (46.676 B) y EchoFeedAddOn.cs (45.803 B) en "...\NinjaTrader 8\bin\Custom\AddOns\", echo-execution-addon.json (304 B) en "...\NinjaTrader 8\echo\"; (2) opcional: certutil hashes vs b2a29a36… / 581a7087… / 9ca3fddc…; (3) re-copiar con -Force desde C:\Temp y REINICIAR NT DESPUÉS de copiar; (4) si NinjaScript muestra errores de compilación → C:\Temp\compile-errors.txt. Señal de éxito observable sin owner: dial 192.168.31.161:9771 cada ≤10 s.

NEXT_MANAGER_ACTION:
Veredicto FAIL ⇒ no certificar lane ni ejecutar ladder hasta el fix. Tras la señal de éxito del AddOn: re-despachar pasos C–K de este artifact (~5 min, dentro de ventana), luego domingo G-REALTIME con el runbook §M, luego ladder congelado §N en la primera ventana admisible lun 2026-10-05. OD-D6-1 AUTHORIZED vigente sin consumir. No emitir EF_D6_E2E_PASS.
```

---
---

# POST OWNER FIX / RETRY — 2026-10-03 (tarde, evidencia UTC ≈21:25Z–21:50Z, local -03 ≈18:25–18:50)

**Nota de esquema:** el despacho pide una sección "SUCCESSFUL RETRY"; el retry NO completó la certificación (veredicto sigue FAIL), así que se titula RETRY a secas para no falsificar el resultado. Lo que SÍ se resolvió: el hallazgo anterior (`EXECUTION_ADDON_LOADED = FAIL`) quedó **SUPERSEDED** — ambos AddOns ahora cargan en NinjaTrader real. El nuevo hallazgo, raíz única y accionable: **la config JSON instalada para el AddOn de ejecución parsea `ntx_port = 0`** ⇒ ambos lanes del AddOn quedan inertes por diseño de guards y el endpoint efectivo NO existe.

## R0 — /critical_precheck RESUELTO: `ntx=****.161:0` es puerto REAL 0 (opción B), no redacción de log

Cadena de evidencia completa:

1. **Fuente @ HEAD** (`EchoExecutionAddOn.cs`, SHA256 `b2a29a36…` == bundle == instalado): el log de carga imprime el puerto parseado SIN máscara — `ntx={MaskId(ntxHost)}:{ntxPort}` (`EchoExecutionAddOn.cs:134-137`); `MaskId` se aplica sólo a host y cuenta. ⇒ `:0` **es el valor parseado**, no comportamiento de render.
2. **Host parseó bien:** `****.161` ⇒ el archivo de config EXISTE en el path fijo (`UserDataDir\echo\echo-execution-addon.json`, `:117-119`) y su `ntx_host` = `192.168.31.161`. El defecto queda aislado a `ntx_port`: ausente, con comillas (`"9771"` es string ⇒ `GetNumber` no escanea dígitos tras la comilla ⇒ default 0) o no numérico (`GetNumber(json,"ntx_port",0)`, `:127`).
3. **Guards silenciosos:** `EnsureMarketLane` (`:271`) y `EnsureExecLane` (`:407`) arrancan con `if (... || ntxPort <= 0) return;` — puerto 0 ⇒ ni un syscall de conexión, sin warning, sin reintento, para siempre (determinista).
4. **Físico decisivo (listener activo):** bridge release `40102ea5` con sesión habilitada y **`*:9771` LISTEN continuo >2.5 min** (18:40:03→18:43+ local): **0 conexiones, 0 ESTABLISHED, 0 líneas `[ntx]`** en journal, cubriendo ≥7 fases del retry de diseño (≤10 s). Contra un listener ACTIVO un dial exitoso es ESTABLISHED persistente (no el SYN_SENT sub-milisegundo que se escapa al sampling contra puerto cerrado). Muestreo adicional pre-bridge (8 tomas × ~3 s): 0 sockets. AddOn cargado (evidencia owner + §R1) + cero dials vs listener ⇒ **puerto efectivo 0 confirmado físicamente**.
5. **El bundle correcto está intacto y NO es lo que el AddOn cargó:** `C:\Temp\echo-execution-addon.json` re-verificado hoy (304 B, SHA256 `9ca3fddc…` == HEAD/weekend) con `"ntx_host": "192.168.31.161", "ntx_port": 9771` numérico. ⇒ el archivo en el target del perfil KoR difiere del bundle (copiado de otra fuente, editado a mano, o variante con puerto string/ausente).
6. **ACL (6.ª re-probe):** `dir "C:\Users\KoR\Documents\NinjaTrader 8\echo"` → `Access is denied` + `PathNotFound` (deny de raíz del perfil) ⇒ el archivo instalado sigue siendo **no verificable por el agente**; la corrección es ciclo owner.

**Clasificación: defecto CONFIG-ONLY (archivo instalado), NO defecto de parser de producto.** El parser sobre la entrada válida (el bundle) produce 9771 (misma familia de parser que lleva 6 sesiones cargando bien la config del feed AddOn; lógica verificada línea a línea). Observación de producto residual registrada (no elevada, ver §R8).

## R1 — AddOn load / NinjaTrader restart (reutilizado como evidencia I)

- **NT reiniciado de nuevo HOY ≈21:25Z** (PID **8700 → 11412**, netstat dev-win: `TCP 192.168.31.132:65168 → 192.168.31.161:9770 ESTABLISHED, PID 11412`; StartTime no consultable por ACL; instante fijado por: sesión feed nueva con seq ~430 a las 21:43:00Z ⇒ arranque ≈21:25Z, consistente con replay estático a Kafka `2026-10-03T21:25:21.358Z`).
- **NINJATRADER_COMPILE = PASS y FEED_ADDON_LOADED = PASS (físico):** sesión feed nueva `2e031cd240b445ab8f2bc0251389c6ea`, `reconnects:1`, familias account/positions/orders/heartbeat cada 10 s (seq 430→474+ durante la ventana; sink sin máscara `evidence.jsonl`). Un AddOn que no compila no carga ni publica.
- **EXECUTION_ADDON_LOADED = PASS (evidencia owner log, SUPERSEDE el FAIL del intento 1):** log NT visible por el Owner: `EchoExecutionAddOn config loaded: ntx=****.161:0 account=… contracts=…` + `EchoExecutionAddOn started (dual channel; execution lane STAGED build)` — formato exacto del source @ HEAD ⇒ los bytes instalados son la build correcta y el AddOn ejecuta su ciclo Active (LoadConfig + timers). El incidente de fuente duplicada NinjaScript quedó **RESOLVED** (compila y ambos cargan; sin síntomas).

## R2 — C REAL EXECUTION TRANSPORT (ejecutado al máximo posible sin endpoint)

- Preflight PASS completo (re-verificado hoy): release exacta `40102ea5` (binario desplegado SHA256 `484b550b…`, `vcs.revision` weekend, BUILD.md); journal M2 con **0 registros**; `ntx/auth-token` presente (64 hex, cliente crudo, no impreso); binding ETCD **12/12 valores exactos** por lectura cruda (`enabled=true, ALLOWED, RJARA114411201551, id "3", GAU50-EVAL/1, EARN2TRADE/GAU50, America/Chicago, 17:00, NQ 12-26, NINJATRADER_BRIDGE`); clave de sesión `futures-bridge/accounts` AUSENTE pre-write; topic `echo.order-commands.E2T-GAU50-01.v1` NO existe (list_topics completo) ⇒ **0 comandos replayables, 0 ambigüedad**.
- Escritura guardada: `futures-bridge/accounts = E2T-GAU50-01` (pre-read ausente → put → read-back writer `"E2T-GAU50-01"` → cross-check MCP RO independiente found/size 12/value exacto).
- Bridge arrancado: **PID 1798251**, `account session built` (`echo.execution_account E2T-GAU50-01`, topic `echo.order-commands.E2T-GAU50-01.v1`, transport `NINJATRADER_BRIDGE`) a los 1.0 s, **listener `*:9771`**.
- **EchoExecutionAddOn → TCP 192.168.31.161:9771 → echo.ntx.v1 → bridge: NO OCURRIÓ** — authenticated hello/session ID/seq del exec lane: **NINGUNO** (0 líneas `[ntx]` en todo el runtime del bridge). El transporte bridge-side (auth, fencing, seq, publisher) permanece certificado weekend §3/§5 — mismo binario y SHA. Con el endpoint no resuelto, el mandato prohíbe seguir: nada de D–K del exec lane fue intentado ni simulado.

## R3 — REAL RECOVERY BARRIER (F)

**FAIL — fail-closed correcto, 2.ª demostración con listener activo:** `account session exited` a los **10.0 s** exactos del built (`18:40:13.075 local`): `barrier: connect: ninjatrader: no authenticated AddOn session on the execution lane`. Sin observaciones venue del exec lane el barrier se negó a completar; reconciliación no debilitada; `UnknownLiveOrders = 0` (`ambiguous_orders=0 mismatches=0 dropped_commands=0` en toda la sesión), journal M2 vacío (0 non-terminal), **0 command replay**.

## R4 — D / E (binding y observación por el exec lane)

- **Por el EchoExecutionAddOn real: NOT_RUN** (nunca hubo sesión; no se fabrican snapshots).
- **Identidad viva del mismo perfil y proceso NT (feed AddOn, sink sin máscara):** discovery 8 cuentas, **exactamente 1 match** `RJARA114411201551`, `match RESOLVED`, **`resolved id "3"` == hint ETCD — 6.ª sesión consecutiva** (2/2 N1 + intento 1 + weekend + intento 1 del lane + hoy). Positions `[]` y orders `[]` observados en todos los ciclos; balances `NLV/cash 50000/50000`, `BP/uPnL/rPnL 0/0/0` (variante demo documentada). `CURRENT_NT_ACCOUNT_ID = "3"`.

## R5 — G / H (reconnect-fencing y bridge restart con AddOn real)

- **REAL_SESSION_RECONNECT / REAL_SESSION_FENCING: NOT_RUN** — requieren sesión del AddOn real; probe prohibido y no usado. Lado server/transporte (F-S2-01/F-S2-04) permanece certificado weekend §5 con los mismos binarios.
- **BRIDGE_RESTART_RECOVERY: NOT_RUN con AddOn real.** Evidencia parcial de hoy: arranque limpio con journal 0 registros, session built 1.0 s, barrier fail-closed determinista; weekend §8 mantiene el PASS de transporte (2× restart, journal reload 0-phantom, reconnect <1.5 s).

## R6 — I NINJATRADER RESTART EVIDENCE

**PASS (reutilizado, permitido por despacho):** el restart owner de ≈21:25Z demostró sobre runtime real: feed AddOn compiló/cargó/recuperó (sesión nueva, rediscovery RESOLVED 1/8, sin corrupción observable); exec AddOn cargó y arrancó (log owner); **el exec lane no recuperó por la config puerto 0** — causa única aislada, no mecánica del restart.

## R7 — K READINESS (capturada con bridge corriendo, cada 30 s)

`ready_new_risk=false` con blockers exactamente los esperados para AddOn-inerte + mercado cerrado: `[NOT_AUTHENTICATED NOT_CONNECTED ORDER_EXECUTION_EVENT_STREAM_NOT_HEALTHY POSITION_NOT_FRESH PROVIDER_ACCOUNT_BINDING_NOT_VERIFIED RECONCILIATION_AUTHORITY_UNAVAILABLE STATIC_ELIGIBILITY_NOT_ELIGIBLE SUBMISSION_CAPABILITIES_NOT_EXACT_READY]`, `ambiguous_orders=0 mismatches=0 dropped_commands=0 recovered=false`. Separación: **EXECUTION_TRANSPORT_READY = NO** (endpoint AddOn no resuelto; bridge-side certificado y listo) · **ACCOUNT_READY = YES** (feed-side RESOLVED vivo) · **RECOVERY_READY = NO** (sin exec lane) · **MARKET_FRESHNESS = STALE** (último `event_ts 2026-10-02T21:38:25.95Z`, edad ≈24 h >> bound 30 s; el replay estático de la sesión nueva a las 21:25:21Z, offsets p4 5476462→5476468, NO refresca evidencia de evento — disciplina F-S2-02: heartbeats/transporte jamás pliegan) · **NEW_RISK_READY = NO** (doble fail-closed: freshness + ventana GAU50-EVAL L–V, sábado cerrado). Sin manipulación de timestamps.

## R8 — G_HORIZON (J) y hallazgo de producto residual

- **G_HORIZON_PRECHECK = PARTIAL_NEEDS_CREATED_ORDER** (sin cambio): la cuenta GAU50 no tiene historial de la vertical y las superficies `LookbackDays*` sólo son inspectables desde NT con el exec AddOn funcional. No se creó orden.
- **Observación de producto residual (registrada, NO elevada a REMEDIATION_REQUIRED):** `LoadConfig` acepta una config con `ntx_port` inválida/ausente — incumple la disciplina declarada en su propio comentario ("any deviation = load failed fail-closed", `EchoExecutionAddOn.cs:104-106`): hace default 0 silencioso y loguea `config loaded` en Information; combinado con los guards silenciosos, una config fatal queda indistinguible de idle sin correlar con el bridge. Reproducción exacta: instalar `echo-execution-addon.json` con `ntx_port` ausente o string ⇒ log `config loaded: ntx=****.161:0`, cero dials vs listener activo (probado hoy). Misma clase que la nota no-elevada "robustez AddOn stageada" de Shot 3; candidato de adjudicación para el Manager; **sin cambios de código en este shot** (mandato: no ocultar, no rediseñar).

## R9 — Owner action exacta (config-only, ACL exige ciclo owner)

1. En sesión owner de dev-win: `copy /Y C:\Temp\echo-execution-addon.json "C:\Users\KoR\Documents\NinjaTrader 8\echo\echo-execution-addon.json"` — reemplazo completo desde el bundle; **NO editar a mano**.
2. Verificar hash en su consola: `certutil -hashfile "C:\Users\KoR\Documents\NinjaTrader 8\echo\echo-execution-addon.json" SHA256` == `9ca3fddc31330b2d5b485fd0869801b486b1443972bbf5ba50c56862feeea71b` (el artefacto de quoting sólo afecta al transporte del agente; en la consola owner las comillas funcionan).
3. (Opcional) abrir el JSON y confirmar `"ntx_port": 9771` **numérico** (sin comillas).
4. **Reiniciar NinjaTrader** (la config se lee una sola vez en State.Active).
Señal de éxito observable por el agente, sin intervención owner: con el bridge en marcha, ESTABLISHED del PID NT → `192.168.31.161:9771` + hello `[ntx]` autenticado en journal ≤10 s tras el arranque de NT.

## /final_safety_state — probado al cierre (no asumido)

- **G-EGRESS-0 restaurado y verificado:** unidad `echo-futures-bridge` **inactive + reset-failed + disabled**; `:9771` FREE (sin listener ni sockets); clave ETCD `futures-bridge/accounts` **eliminada** con ciclo guardado (pre-read exacta `E2T-GAU50-01` → delete → read-back ausente → cross-check MCP RO count **21 claves** == baseline pre-shot); journal M2 **0 registros**; topic de comandos inexistente; **0 LIVE run, 0 comandos, 0 ambigüedad** en toda la sesión.
- **Feed lane conectado y observando** (relay `:9770` + AddOn feed, sesión `2e031cd2…`): permitido por final_safety_state; cuenta observable RESOLVED.
- **AddOns lado owner:** binarios correctos y cargados; exec AddOn INERTE por config (con o sin listener, puerto 0 ⇒ jamás conecta; tras el fix owner, sin listener recibe refusal sin estado ni riesgo).
- **New-risk configurationally disabled** (sin sesión habilitada + sin topic M1 + STALE + ventana cerrada sábado).

## /close — Final handoff (POST OWNER FIX / RETRY)

```text
D6_REAL_EXECUTION_LANE_NO_EGRESS =
FAIL (2.º consecutivo, ahora con RAÍZ ÚNICA identificada y acción owner exacta: el EchoExecutionAddOn SÍ carga —supersede del hallazgo previo— pero la config JSON instalada parsea ntx_port=0 ⇒ lanes inertes por guards; defecto config-only, no de producto; todo lo agent-side re-verificado fail-closed)

BASELINE_SHA:
40102ea5a44be9a618ac12529e6f0e9fdfd46d34

FINAL_SHA:
40102ea5a44be9a618ac12529e6f0e9fdfd46d34 (cero commits; worktree limpio al cierre; herramienta efímera ETCD eliminada; delta infra neto CERO)

OWNER_W1:
PASS (compilación y carga de AMBOS AddOns verificadas: log owner formato exacto de la build HEAD + lane feed físico activo; incidente fuente-duplicada RESOLVED. Excepción registrada aparte: el echo-execution-addon.json instalado ≠ bundle ⇒ puerto 0)

NINJASCRIPT_DUPLICATE_SOURCE_INCIDENT:
RESOLVED

NINJATRADER_COMPILE:
PASS (ambos AddOns cargan y ejecutan; feed publica frames físicos; exec publica su ciclo Active — un AddOn sin compilar no carga)

FEED_ADDON_LOADED:
PASS (sesión 2e031cd240b445ab8f2bc0251389c6ea, ESTABLISHED PID 11412→:9770, frames cada 10 s, reconnects 1)

EXECUTION_ADDON_LOADED:
PASS (carga probada: log owner config loaded + started; SUPERSEDE el FAIL del intento 1 — pero sus lanes quedaron inertes por ntx_port=0)

NTX_EFFECTIVE_ENDPOINT:
NINGUNO (config cargada = 192.168.31.161:0 ⇒ guards `ntxPort<=0 ⇒ return` ⇒ cero dials; endpoint requerido 192.168.31.161:9771 NO efectivo)

NTX_PORT_ZERO_LOG_EXPLAINED:
YES — opción B: el puerto 0 es REAL. El format string imprime el valor parseado sin máscara (MaskId sólo aplica a host/cuenta); host parseó OK ⇒ archivo existe con ntx_host correcto y ntx_port ausente/string/no-numérico; bundle correcto (9ca3fddc, 9771 numérico) intacto en C:\Temp ⇒ el instalado difiere; confirmado físicamente: cero conexiones contra listener *:9771 activo >2.5 min (≥7 fases de retry)

EXECUTION_LANE_REAL:
FAIL (sin sesión; hello/session ID/seq del exec lane: NINGUNO; lado bridge/transporte permanece certificado weekend — mismo binario y SHA)

REAL_SESSION_ID_INITIAL:
NONE (ningún cliente autenticó jamás en :9771 en esta corrida)

ACCOUNT_BINDING:
PASS feed-side vivo (RESOLVED 1/8, RJARA114411201551 = NT id "3" == hint ETCD, 6.ª sesión consecutiva) · exec-side NOT_RUN

CURRENT_NT_ACCOUNT_ID:
"3"

ACCOUNT_OBSERVATION:
PASS como observación real del feed lane (positions []/orders [] todos los ciclos; balances NLV/cash 50000/50000, BP/uPnL/rPnL 0/0/0, variante demo; discovery 8 cuentas con sink sin máscara) · por el exec lane NOT_RUN (sin datos fabricados)

REAL_RECOVERY_BARRIER:
FAIL — fail-closed correcto 2.ª demostración: "no authenticated AddOn session on the execution lane" a los 10.0 s exactos con listener activo; reconciliación no debilitada; 0 UnknownLiveOrders / 0 AccountMismatch / journal 0 non-terminal

REAL_SESSION_RECONNECT:
FAIL (NOT_RUN — sin AddOn funcional; probe prohibido y no usado; F-S2-01/04 server-side certificados weekend)

REAL_SESSION_FENCING:
FAIL (NOT_RUN — ídem)

BRIDGE_RESTART_RECOVERY:
FAIL (NOT_RUN con AddOn real; arranque de hoy limpio: journal 0, built 1.0 s, barrier fail-closed determinista; weekend §8 PASS de transporte vigente)

NINJATRADER_RESTART_EVIDENCE:
PASS (restart owner ≈21:25Z reutilizado, PID 8700→11412: feed recuperó ✔ rediscovery RESOLVED 1/8; exec cargó y arrancó ✔; exec lane no recuperó por config — causa única aislada)

G_HORIZON_PRECHECK:
PARTIAL_NEEDS_CREATED_ORDER (sin historial de la vertical; superficies LookbackDays* requieren exec AddOn funcional; NO se creó orden)

EXECUTION_TRANSPORT_READY:
NO (endpoint AddOn no resuelto; bridge-side certificado y listo para re-enable en ~1 min tras el fix)

CURRENT_MARKET_FRESHNESS:
STALE (event_ts 2026-10-02T21:38:25.95Z, edad ≈24 h >> bound 30 s; replay estático de la sesión nueva a las 21:25:21Z — offsets p4 5476462→5476468 — no refresca evidencia de evento, F-S2-02)

NEW_RISK_READY:
NO

SUNDAY_G_REALTIME_RUNBOOK:
READY (§M del intento 1, determinista y ya probado; NOTA: G-REALTIME es feed-lane-only ⇒ certificable domingo 17:00 CT INDEPENDIENTE del fix owner del exec AddOn)

LIVE_PHYSICAL_LADDER_RUNBOOK:
READY (§N del intento 1; gate 0 ACTUALIZADO = fix config §R9 + restart NT + señal de éxito observable; resto sin cambios)

FIRST_PHYSICAL_CERT_SCENARIO:
FULLY_DEFINED (freeze §14.13; NQ/NQZ6; cap GROSS 6; SL/TP 2000/1500 day1; side/qty = output frozen)

MISSING_PHYSICAL_PARAMETERS:
NONE

FINAL_SAFETY_STATE:
G-EGRESS-0 PROBADO (unidad inactive+disabled, :9771 FREE, accounts key eliminada — cross-check MCP RO 21 claves == baseline; journal M2 0 registros; feed lane conectado observando; exec AddOn inerte por config; 0 LIVE run; 0 comandos; 0 ambigüedad; new-risk configurationally disabled)

PHYSICAL_ORDERS_SENT:
0

PHYSICAL_ORDERS_MODIFIED:
0

PHYSICAL_ORDERS_CANCELLED:
0

PRODUCT_CODE_CHANGES:
NONE

RESIDUAL_FINDINGS:
1) LoadConfig acepta ntx_port inválida con default silencioso 0 + log "config loaded" (contradice su disciplina declarada fail-closed; repro exacta §R8) — clase "robustez AddOn", adjudicación Manager, sin cambio en este shot · 2) variante demo de balances 50000/50000 persistente (re-observar en ventana) · 3) ACL owner 6.ª re-probe: instalados no agent-verificables (verificación de corrección = señal conductual §R9.4)

OWNER_DECISION_REQUIRED:
Una sola acción exacta (§R9): reemplazar el echo-execution-addon.json del perfil KoR con la copia íntegra de C:\Temp (hash 9ca3fddc…; "ntx_port": 9771 numérico; NO editar a mano) y REINICIAR NinjaTrader. No es decisión nueva: mismo ciclo standing OD-D6-4. Señal de éxito observable por el agente: ESTABLISHED→:9771 + hello [ntx] autenticado ≤10 s tras el arranque de NT con el bridge en marcha.

NEXT_MANAGER_ACTION:
Veredicto FAIL ⇒ no certificar lane ni ejecutar ladder hasta el fix §R9. Domingo 2026-10-04 ≥17:00 CT: certificar G-REALTIME con el runbook §M (feed-lane-only, NO depende del fix). Tras la señal de éxito del AddOn: re-despachar C–K (~5 min, dentro de ventana) y ejecutar el ladder congelado §N en la primera ventana admisible lun 2026-10-05 00:00–15:50 CT. OD-D6-1 vigente sin consumir. No emitir EF_D6_E2E_PASS.
```

---
---

# POST CONFIG FIX / FINAL C–K CERTIFICATION — 2026-10-03 (noche, evidencia UTC ≈22:15Z–23:00Z, local -03 ≈19:15–20:00)

**Nota de esquema:** el despacho C→K pedía certificar sobre la config corregida (verdad física nueva del owner: `C:\Temp` → destino con SHA `9ca3fddc…` en ambos, `ntx_port = 9771` parseado, NT reiniciado después). La certificación **NO se completó**: el runtime real del nuevo proceso NT **contradice** la corrección atestiguada — el EchoExecutionAddOn del PID 4576 **no hizo NI UN intento de conexión** a `:9771` contra un listener vivo durante 18+ minutos, con cadencia de diseño ≤10 s desde ~1 s tras su activación. Es la MISMA firma conductual del incidente puerto-0 (o bien el AddOn no cargó en este boot; indistinguible para el agente por ACL del log NT). Por mandato C0 (`If runtime still says :0: STOP. Return exact contradiction`) la fase física se detuvo ahí; C1 (producto) SÍ se cerró con fix acotado. Veredicto: **REMEDIATION_REQUIRED**.

## C0 — VERIFY EXECUTION ADDON CONFIG RELOAD: FAIL (contradicción exacta)

1. **Owner ciclo (atestiguado, no agent-verificable en destino):** config corregida al destino con SHA `9ca3fddc…`; NT reiniciado después. **Fuente verificada por el agente HOY:** `C:\Temp\echo-execution-addon.json` → SHA256 `9ca3fddc31330b2d5b485fd0869801b486b1443972bbf5ba50c56862feeea71b` ✔ (certutil dev-win).
2. **Restart físico confirmado:** NinjaTrader PID **11412 → 4576** (netstat dev-win: `192.168.31.132:52883 → 192.168.31.161:9770 ESTABLISHED, PID 4576`; `Get-Process 4576` = NinjaTrader, StartTime no accesible por ACL). Instante del boot fijado por el hello feed: sesión nueva `f2756ae6a27c4a5fad67954c2fb9f9a1` a las **2026-10-03T22:13:09.941Z** (`reconnects:1`). Hubo un boot intermedio brevísimo (`de38c5f2…`, 23 frames, ≈22:12Z) — el owner reinició dos veces en ≈1 min; ambos boots son post-fix.
3. **FEED_ADDON_LOADED = PASS (físico):** la sesión `f2756ae6…` publica hello/account/positions/orders/heartbeat cada 10 s (seq 1→334+ durante la ventana); rediscovery 8 cuentas, 1 match, RESOLVED.
4. **EXECUTION_ADDON_LOADED + effective port 9771 = FAIL (conductual, decisivo):** con el bridge LISTENING en `*:9771` ininterrumpidamente desde las **22:29:32Z** (PID 2155952, verificado con `ss` en tomas repetidas):
   - El barrier falló a los **10.015 s** exactos del built (`22:29:32.617Z` → `22:29:42.632Z`, razón literal `session: recovery barrier failed for E2T-GAU50-01: barrier: connect: ninjatrader: no authenticated AddOn session on the execution lane`) — **3.ª demostración fail-closed**.
   - **CERO sockets con puerto 9771 de cualquier estado en dev-win** en 2 ventanas de muestreo (7×2 s + 10×2.2 s) y cero ESTABLISHED lado servidor (`ss`) en todo el runtime. Contra un listener ACTIVO un dial del AddOn queda ESTABLISHED persistente (backlog del kernel) — no haySampling que se escape.
   - El listener quedó disponible **≥18 minutos** ⇒ ≥100 ciclos de retry esperados según el diseño (primer dial ~1 s tras Active, backoff 10 s, `EchoExecutionAddOn.cs:271-297/:407-430`); **0 intentos**. Un AddOn cargado con `ntx_port=9771` NO puede comportarse así.
5. **Discriminación no posible por el agente (ACL 7.ª/8.ª re-probe):** log NT (`Documents\NinjaTrader 8\log`) no accesible; `Get-Process .StartTime` vacío; `tasklist /m /fi "PID eq 4576"` = `Access is denied`. Las dos hipótesis restantes — (a) la config efectiva cargada en el PID 4576 sigue sin puerto dialable (firma puerto-0 idéntica al retry) o (b) el AddOn de ejecución no cargó/compiló en ESTE boot — requieren el log NT owner. **La evidencia conductual contradice la atestación del owner; mandato C0 ⇒ STOP físico.**

## C1 — CONFIG FAIL-CLOSED REPAIR: PASS (código acotado, commit `d361008b`)

El hallazgo residual §R8 del retry quedó **CERRADO como fix de producto** (no residual): con este guard, el incidente de hoy habría sido unívoco desde el log.

- **Fix (11 líneas, `EchoExecutionAddOn.cs` `LoadConfig`):** tras parsear, valida `ntx_host` no vacío, `ntx_port > 0`, `auth_token`, `account_id`, `account_name`, `contracts` no vacíos, `snapshot_seconds/heartbeat_seconds > 0`. En fallo: **resetea `ntxHost/ntxPort/authToken` a inertes** (los guards de ambos lanes exigen host+puerto+token ⇒ hard-down), loguea `EchoExecutionAddOn config FAILED: invalid/missing required fields …; execution lane stays down` en **LogLevel.Error**, y **retorna ANTES del log de éxito** — jamás imprime `config loaded` sobre una config fatal.
- **Test estructural enfocado:** `v3/futures-bridge/addon-ninjatrader/config_guard_test.go` (`TestExecAddOnConfigLoadFailsClosedOnInvalid`) — fija el contrato a nivel source dentro de la región `LoadConfig`: rama `config FAILED` existe, precede al log de éxito, cubre port/token/account/contracts, resetea a inerte y usa `LogLevel.Error`. Suite del paquete **5/5 PASS** (los 4 guards G-EGRESS-0 previos intactos). `go build ./v3/futures-bridge/...` OK.
- **Shadow-compile físico contra DLL reales 8.1.8.3 (dev-win):** transporte efímero http.server+`curl.exe`+SHA byte-verify (`72d97ad6c776ba56ea0d8aadfd44be2caa12ab884602c29995ffe5e75e92653f` idéntico ambos lados); **EXEC_EXIT=0, 0 errores**, exactamente los 3 warnings PREEXISTENTES de Shot 1/3 (CS0612 CreateOrder, 2× CS0649); **ningún warning nuevo**. DLL sólo en `C:\Users\TEMP`; servidor apagado; **NADA instalado en NT**.
- **Commit:** `d361008bfe4aa54fe3d8b6380d290bf92e1f1c08` sobre `feature/d6-shot1-execution-vertical` (FF `40102ea5..d361008b`, **push a origin verificado**). Cobertura de changed-code: el cambio ejecutable es C# (no CI-ejecutable sin runtime NT); la evidencia medible máxima = test estructural + shadow-compile (documentado como tal). El binario del bridge desplegado sigue siendo `40102ea5` (SHA `484b550b…`): el commit no toca código Go de producto (sólo .cs + test), comportamiento del bridge idéntico.
- **Pickup físico:** el AddOn instalado en NT sigue siendo la build `b2a29a36…` (40102ea5). El fix entra en vigencia física en el PRÓXIMO ciclo de instalación owner (W1) — ver gate 0 del handoff.

## D — REAL EXECUTION TRANSPORT: FAIL (sin AddOn; preflight íntegro re-verificado)

Preflight completo PASS: release desplegada `40102ea5` (SHA binario `484b550b…`, unit ExecStart apuntando al release dir); journal M2 **0 registros**; `futures-bridge/ntx/auth-token` presente (64 B, meta cruda, no impreso); binding ETCD **12/12 valores exactos por lectura cruda** (`enabled=true, ALLOWED, GAU50, EARN2TRADE, RJARA114411201551, GAU50-EVAL/1, America/Chicago, 17:00, NQ 12-26, "3", NINJATRADER_BRIDGE`); clave de sesión `futures-bridge/accounts` AUSENTE pre-write; topic `echo.order-commands.E2T-GAU50-01.v1` NO existe (list_topics completo ⇒ 0 comandos replayables). Escritura guardada: `--expect-absent` → put → read-back `E2T-GAU50-01`. Bridge: **PID 2155952**, `account session built` <0.1 s tras el start (22:29:32.617Z, `echo.execution_account E2T-GAU50-01`, topic `echo.order-commands.E2T-GAU50-01.v1`, transport NINJATRADER_BRIDGE), listener `*:9771`. **NT → AddOn → TCP :9771 → echo.ntx.v1 → bridge: NO OCURRIÓ** (§C0). NT PID 4576; bridge PID 2155952; SESSION_A: **NINGUNA**; release SHA lane = binario `484b550b…` (release 40102ea5) + AddOn instalado `b2a29a36…`. No synthetic probe en D.

## E — ACCOUNT BINDING

- **Por el exec AddOn real: NOT_RUN** (nunca hubo sesión).
- **Identidad viva del mismo perfil/proceso (feed AddOn, sink sin máscara, sesión `f2756ae6…` @ 22:27Z):** discovery 8 cuentas (`Backtest, Playback101, Sim101, 5×RJARA…`), **exactamente 1 match** `RJARA114411201551`, `match RESOLVED`, **NT `Account.Id "3"` == hint ETCD — 7.ª sesión consecutiva**. Binding Name-primary intacto, `E2T-GAU50-01` ↔ `RJARA114411201551` sin drift.

## F — REAL ACCOUNT OBSERVATION

- **Por el exec lane: NOT_RUN** (sin datos fabricados).
- **Feed lane real (mismo proceso NT):** positions `[]`, orders `[]` en todos los ciclos; balances `NLV/cash 50000/50000`, `BP/uPnL/rPnL 0/0/0` (variante demo, 3.ª sesión consecutiva documentándola). Las observaciones alcanzan el runtime (Kafka p4: el replay estático del boot corto `de38c5f2` a las 22:12:29Z, offset 5476470, ingress_ref del propio mensaje).

## G — REAL RECOVERY BARRIER: FAIL (fail-closed correcto, 3.ª demostración)

`account session exited` a los **10.015 s** del built con razón exacta `barrier: connect: ninjatrader: no authenticated AddOn session on the execution lane`. Sin observaciones venue del exec lane el barrier se negó a completar; reconciliación no debilitada; `UnknownLiveOrders = 0`, `AccountMismatch = 0` (`ambiguous_orders=0 mismatches=0 dropped_commands=0` en las 28 tomas de readiness), journal M2 vacío (0 non-terminal), **0 command replay**.

## H — REAL RECONNECT + SESSION FENCING: NOT_RUN

Requieren una sesión del AddOn real que fencear/reconectar; no existió. El probe weekend (`scratch-weekend ntx-probe`, modes connect/badtoken/rewind, token vía ETCD) quedó listo y NO se usó — sin SESSION_A no hay fencing que ejercitar. Lado server/transporte: F-S2-01/04 permanecen certificados weekend (mismos binarios).

## I — BRIDGE RESTART RECOVERY: NOT_RUN con AddOn real

Evidencia parcial de hoy: arranque limpio (journal 0 registros, built <0.1 s, barrier fail-closed determinista, unidad `Restart=on-failure` intacta); weekend §8 mantiene el PASS de transporte (2× restart, 0-phantom, reconexión <1.5 s). El bridge corrió una sola vez en esta corrida (22:29:32Z → teardown ~23:00Z) sin recibir jamás una conexión.

## J — G_HORIZON REAL PRECHECK

`G_HORIZON_PRECHECK = PARTIAL_NEEDS_CREATED_ORDER` (sin cambio, 3.ª vez): la cuenta GAU50 no tiene historial de la vertical y las superficies `LookbackDays*`/historia sólo son inspectables desde NT con el exec AddOn funcional. No se creó orden.

## K — READINESS COMPOSITION (capturada con bridge corriendo, 28 tomas cada 30 s)

`ready_new_risk=false`; blockers exactamente los esperados para AddOn-inerte + mercado cerrado: `[NOT_AUTHENTICATED NOT_CONNECTED ORDER_EXECUTION_EVENT_STREAM_NOT_HEALTHY POSITION_NOT_FRESH PROVIDER_ACCOUNT_BINDING_NOT_VERIFIED RECONCILIATION_AUTHORITY_UNAVAILABLE STATIC_ELIGIBILITY_NOT_ELIGIBLE SUBMISSION_CAPABILITIES_NOT_EXACT_READY]`, `ambiguous_orders=0 mismatches=0 dropped_commands=0 recovered=false`. Separación: **EXECUTION_TRANSPORT_READY = NO** (endpoint AddOn no resuelto; bridge-side certificado y listo para re-enable en ~1 min) · **ACCOUNT_READY = YES** (feed-side RESOLVED vivo) · **RECOVERY_READY = NO** (sin exec lane) · **MARKET_FRESHNESS = STALE** (`kafka-last` p4 5476470 @ 22:12:29Z = replay estático del boot corto `de38c5f2`; último event_ts real `2026-10-02T21:38:25.95Z`, edad ≈24 h >> bound 30 s — F-S2-02) · **NEW_RISK_READY = NO** (doble fail-closed: freshness + ventana GAU50-EVAL L–V, sábado cerrado).

## L — SUNDAY G-REALTIME HANDOFF

`SUNDAY_G_REALTIME_RUNBOOK = READY` (sin cambios; herramienta `kafka-last` re-ejecutada HOY con resultado reproducible — ver §K). G-REALTIME es **feed-lane-only** ⇒ certificable domingo ≥17:00 CT (22:00Z) INDEPENDIENTE del fix del exec AddOn. Runbook determinista completo en §M del intento 1 (Kafka offsets, event_ts/receive_ts, age/lag, stream canónico NQ:NQZ6, FRESH ⇔ event_age < 30 s en 2 tomas, transporte vivo; alternativa `kafka-last -n 1`).

## /final_safety_state — probado al cierre (no asumido)

- **G-EGRESS-0 restaurado y verificado:** unidad `echo-futures-bridge` **inactive + reset-failed + disabled**; `:9771` FREE (`ss`); clave ETCD `futures-bridge/accounts` **eliminada con ciclo guardado** (pre-read exacta `E2T-GAU50-01` → delete → read-back ausente → cross-check MCP RO **21 claves == baseline pre-shot**); journal M2 **0 registros**; **0 COMMAND_FRAME** en todo el runtime (histograma completo de msgs del bridge verificado: sólo init/built/exited/readiness); topic de comandos inexistente.
- **Feed lane conectado y observando** (relay `:9770` + AddOn feed, sesión `f2756ae6…`): permitido por final_safety_state; cuenta observable RESOLVED.
- **AddOns lado owner:** binarios de la build `b2a29a36…` instalados (agente no puede verificar bytes por ACL); exec AddOn INERTE en el PID 4576 (causa en diagnóstico §C0.5 — config efectiva sin puerto dialable o AddOn no cargado este boot).
- **New-risk configurationally disabled** (sin sesión habilitada + sin topic M1 + STALE + sábado fuera de ventana).
- Nota: el exec AddOn, aún si se corriese con config válida, sólo dials a `:9771` — hoy sin listener = refusal sin estado ni riesgo.

## /close — Final handoff (POST CONFIG FIX / FINAL C–K)

```text
D6_REAL_EXECUTION_LANE_NO_EGRESS =
REMEDIATION_REQUIRED (3.er intento consecutivo; la certificación física C–K NO se completó: el runtime del nuevo NT PID 4576 contradice la corrección atestiguada — cero intentos de conexión a :9771 en ≥18 min contra listener vivo con cadencia de diseño ≤10 s; C0 STOP por mandato; C1 de producto SÍ cerrado)

BASELINE_SHA:
40102ea5a44be9a618ac12529e6f0e9fdfd46d34

FINAL_SHA:
d361008bfe4aa54fe3d8b6380d290bf92e1f1c08 (FF sobre 40102ea5, PUSHED a origin; fix C1 = EchoExecutionAddOn.cs LoadConfig fail-closed + config_guard_test.go; el binario del bridge físico sigue siendo release 40102ea5 / SHA 484b550b — el commit no toca código Go de producto)

CONFIG_FIX:
PASS lado bundle (C:\Temp SHA 9ca3fddc… re-verificado por agente hoy; atestación owner de destino con mismo SHA) · CONTRADICHO por el runtime del PID 4576 (cero dials) ⇒ el estado efectivo del lane NO cambió; causa residual (config no efectiva vs AddOn no cargado este boot) indistinguible sin log NT owner

NTX_EFFECTIVE_ENDPOINT:
NINGUNO (el AddOn del PID 4576 no dialing; endpoint requerido 192.168.31.161:9771 NO efectivo)

CONFIG_FAIL_CLOSED_REPAIR:
PASS (commit d361008b: guard fail-closed + test estructural 5/5 + shadow-compile físico 8.1.8.3 EXIT=0 sin warnings nuevos; pickup físico pendiente al próximo ciclo de instalación owner)

NINJATRADER_COMPILE:
FEED PASS (físico: sesión f2756ae6 publicando desde el boot 22:13:09Z) · EXEC DESCONOCIDO este boot (sin señal runtime; sombra de la build corregida 72d97ad6… compila EXIT=0)

FEED_ADDON_LOADED:
PASS (sesión f2756ae6a27c4a5fad67954c2fb9f9a1, hello 22:13:09.941Z, frames cada 10 s, rediscovery RESOLVED)

EXECUTION_ADDON_LOADED:
FAIL/UNKNOWN (cero dials en ≥18 min vs listener vivo = firma puerto-0 o no-carga; indistinguible por ACL del log NT — discriminación = diagnóstico owner §OWNER_DECISION_REQUIRED)

EXECUTION_LANE_REAL:
FAIL (sin sesión; 0 hellos [ntx], 0 sockets, 0 líneas de auth; lado bridge/transporte permanece certificado weekend — mismo binario)

REAL_SESSION_ID_INITIAL:
NONE (ningún cliente autenticó jamás en :9771 en esta corrida)

ACCOUNT_BINDING:
PASS feed-side vivo (RESOLVED 1/8, RJARA114411201551 = NT id "3" == hint ETCD, 7.ª sesión consecutiva) · exec-side NOT_RUN

CURRENT_NT_ACCOUNT_ID:
"3"

ACCOUNT_OBSERVATION:
PASS como observación real del feed lane (positions []/orders [] todos los ciclos; balances NLV/cash 50000/50000 demo, 3.ª sesión; discovery 8 cuentas sin máscara) · por el exec lane NOT_RUN (sin datos fabricados)

REAL_RECOVERY_BARRIER:
FAIL — fail-closed correcto 3.ª demostración: "no authenticated AddOn session on the execution lane" a los 10.015 s exactos con listener activo; reconciliación no debilitada; 0 UnknownLiveOrders / 0 AccountMismatch / journal 0 / 0 replay

REAL_SESSION_RECONNECT:
FAIL (NOT_RUN — sin AddOn funcional; probe listo y NO usado)

REAL_SESSION_FENCING:
FAIL (NOT_RUN — ídem; F-S2-01/04 server-side certificados weekend)

BRIDGE_RESTART_RECOVERY:
FAIL (NOT_RUN con AddOn real; arranque de hoy limpio: journal 0, built <0.1 s, barrier fail-closed determinista; weekend §8 PASS de transporte vigente)

G_HORIZON_PRECHECK:
PARTIAL_NEEDS_CREATED_ORDER (sin historial de la vertical; superficies LookbackDays* requieren exec AddOn funcional; NO se creó orden)

EXECUTION_TRANSPORT_READY:
NO (G-EGRESS-0 al cierre; bridge-side certificado, re-enable ~1 min tras la señal de éxito del AddOn)

CURRENT_MARKET_FRESHNESS:
STALE (event_ts real 2026-10-02T21:38:25.95Z, edad ≈24 h >> bound 30 s; p4 5476470 @ 22:12:29Z = replay estático del boot corto de38c5f2, no refresca evidencia — F-S2-02)

NEW_RISK_READY:
NO

SUNDAY_G_REALTIME_RUNBOOK:
READY (feed-lane-only ⇒ certificable dom 2026-10-04 ≥17:00 CT INDEPENDIENTE del fix del exec AddOn)

LIVE_PHYSICAL_LADDER_RUNBOOK:
READY con gate 0 ACTUALIZADO = diagnóstico owner del runtime NT (log de boot 22:13:09Z) + corrección + pickup del fix C1 (reinstalar EchoExecutionAddOn.cs desde HEAD d361008b, bytes 72d97ad6…) + señal de éxito observable; ventana admisible lun 2026-10-05 00:00–15:50 CT / evening 17:10–23:59 CT

FIRST_PHYSICAL_CERT_SCENARIO:
FULLY_DEFINED (freeze §14.13; NQ/NQZ6; cap GROSS 6; SL/TP 2000/1500 day1; side/qty = output frozen)

MISSING_PHYSICAL_PARAMETERS:
NONE

FINAL_SAFETY_STATE:
G-EGRESS-0 PROBADO (unidad inactive+reset-failed+disabled, :9771 FREE, accounts key eliminada con ciclo guardado — cross-check MCP RO 21 claves == baseline; journal M2 0 registros; 0 COMMAND_FRAME; feed lane conectado observando; exec AddOn inerte; 0 LIVE run; 0 comandos; 0 ambigüedad; new-risk configurationally disabled)

PHYSICAL_ORDERS_SENT:
0

PHYSICAL_ORDERS_MODIFIED:
0

PHYSICAL_ORDERS_CANCELLED:
0

PRODUCT_CODE_CHANGES:
1 commit acotado: d361008b (LoadConfig fail-closed + test estructural; sin cambios Go de producto; shadow-compile físico EXIT=0; NO instalado en NT — pickup en próximo W1)

RESIDUAL_FINDINGS:
1) Causa raíz NT-side indeterminada agente-side (config efectiva sin puerto dialable vs AddOn no cargado en el boot 22:13:09Z — el log NT owner discrimina en 1 minuto) · 2) variante demo de balances 50000/50000 persistente (re-observar en ventana) · 3) ACL owner (7.ª/8.ª re-probe: log NT, StartTime, módulos del proceso — todos denegados; verificación conductual es la única vía agente) · 4) boot intermedio brevísimo de38c5f2 (≈22:12Z, 23 frames) no explicado — owner reinició 2× en ~1 min

OWNER_DECISION_REQUIRED:
Un solo ciclo diagnóstico+fix (standing OD-D6-4): (1) en su sesión, abrir el log de NT del boot 19:13 local (C:\Users\KoR\Documents\NinjaTrader 8\log\NinjaTrader_2026-10-03…) y reportar cuál de estas líneas apareció: "EchoExecutionAddOn config loaded: ntx=****.161:9771 account=…" + "started (dual channel…)" ⇒ hipótesis (a) refutada, escalar a red/firewall del perfil NT (no visto: Test-NetConnection 9771=True físico en intento 1); sólo "started" sin "config loaded" o ausencia total de líneas EchoExecutionAddOn ⇒ el AddOn no cargó este boot: re-verificar los 2 .cs en "...\NinjaTrader 8\bin\Custom\AddOns\" + recompilar NinjaScript (F5) + revisar C:\Temp\compile-errors.txt; (2) en CUALQUIER rama, para el próximo ciclo de instalación reinstalar EchoExecutionAddOn.cs desde HEAD d361008b (bytes 72d97ad6…) para que una config fatal quede visible como "config FAILED"; (3) reiniciar NT y dejar el bridge en marcha — señal de éxito observable por el agente sin intervención owner: ESTABLISHED del PID NT → 192.168.31.161:9771 + hello [ntx] autenticado en journal ≤10 s.

NEXT_MANAGER_ACTION:
Veredicto REMEDIATION_REQUIRED ⇒ no certificar lane ni ejecutar ladder. Domingo 2026-10-04 ≥17:00 CT: certificar G-REALTIME (runbook §M intento 1 — feed-lane-only, no depende del fix). Tras la señal de éxito del AddOn: re-despachar C–K (~5 min dentro de ventana; preflight de este artifact es re-ejecutable tal cual) y ejecutar el ladder congelado §N en la primera ventana admisible lun 2026-10-05 00:00–15:50 CT. OD-D6-1 AUTHORIZED vigente sin consumir (0 órdenes en 3 intentos). No emitir EF_D6_E2E_PASS.
```

---
---

# FINAL PARSER-FIX RETRY — REAL C→K — 2026-10-04 (madrugada, evidencia UTC ≈05:14Z–05:40Z, local -03 ≈02:14–02:40; domingo, CME cerrado)

**Nota de esquema:** el despacho pide certificar C→K sobre la verdad física nueva (owner ejecutó el bundle rebuild y NT arrancó con `EchoExecutionAddOn config loaded: ntx=****.161:9771 account=****1551 contracts=1` + `started (dual channel…)`). El parser fix quedó **FÍSICAMENTE CONFIRMADO por primera vez con evidencia conductual agente-side**, y el lane de ejecución REAL llegó por primera vez en 4 intentos al bridge, **pasó hello+auth** — y ahí la certificación volvió a detenerse, ahora por **DOS DEFECTOS DE PRODUCTO nuevos, demostrados físicamente y con reproducción exacta en fuente** (nunca ejercitados antes: el bridge sólo había sido probado contra el probe sintético, cuyo shape de frames ES el del bridge). Veredicto: **REMEDIATION_REQUIRED**. Cero órdenes, cero comandos, cero mutaciones de producto.

## P0 — PARSER FIX CONFIRMED + ADDON LOADED (supersede definitivo de los 3 intentos previos)

- **Verdad física nueva (owner):** log NT del boot vigente: `EchoExecutionAddOn config loaded: ntx=****.161:9771 account=****1551 contracts=1` + `EchoExecutionAddOn started (dual channel; execution lane STAGED build)`; EchoFeedAddOn conectado normal a :9770. El `config FAILED` histórico pertenece a boots previos.
- **Confirmación conductual agente-side (independiente del log owner):** dev-win netstat, NinjaTrader **PID 13068**: feed `192.168.31.132:54550 → 192.168.31.161:9770 ESTABLISHED` y **DOS sockets `SYN_SENT → 192.168.31.161:9771` del mismo PID** (dual channel dializando). Con config puerto 0 esto es estructuralmente imposible (guards `ntxPort<=0 ⇒ return`, sin un solo syscall). `CONFIG_PARSER_FIX = PHYSICALLY_CONFIRMED`; `NTX_EFFECTIVE_ENDPOINT = 192.168.31.161:9771`.
- Los bytes instalados son la build `2c8ab2cf…` (bundle EchoD6Bundle @ `ffa493d8`), feed `581a7087…`, config `9ca3fddc…`.

## C — REAL EXECUTION TRANSPORT: PROGRESO HISTÓRICO, LUEGO DEFECTOS

- **Preflight PASS completo (re-verificado hoy por lectura exacta cliente crudo + MCP RO):** release desplegada `40102ea5` (binario SHA256 `484b550b…`, unit ExecStart apunta al release dir; el delta `40102ea5..ffa493d8` es sólo `.cs` + test Go + harness Python ⇒ binario alineado); journal M2 **0 registros**; `ntx/auth-token` presente (64 hex, no impreso); binding ETCD **12/12 valores exactos** (`enabled=true, ALLOWED, GAU50, EARN2TRADE, RJARA114411201551, GAU50-EVAL/1, America/Chicago, 17:00, NQ 12-26, "3", NINJATRADER_BRIDGE`); clave de sesión `futures-bridge/accounts` AUSENTE pre-write; topic `echo.order-commands.E2T-GAU50-01.v1` sin particiones (0 comandos replayables); bridge inactive+disabled, `:9771` FREE; sin `/demo` cross-contamination (prefijo verificado `PREFIX /echo/development/`).
- **Escritura guardada:** `futures-bridge/accounts = E2T-GAU50-01` (pre-read exacta ABSENT → put → read-back writer `"E2T-GAU50-01"` → cross-check MCP RO independiente found/size 12/valor exacto).
- **Bridge arrancado:** **PID 2518565**, `account session built` a las **05:20:58.658Z** (`echo.execution_account E2T-GAU50-01`, topic `echo.order-commands.E2T-GAU50-01.v1`, transport NINJATRADER_BRIDGE), listener `*:9771` verificado con `ss`.
- **NT → AddOn → TCP :9771 → echo.ntx.v1 → bridge: OCURRIÓ por primera vez** — y ahí aparecen los defectos (D1/D2 abajo). Transporte capturado: NT PID 13068, bridge PID 2518565, pares 192.168.31.132:55256/55257 → 192.168.31.161:9771, release SHA lane = binario `484b550b…` (40102ea5) + AddOn `2c8ab2cf…`. **SESSION_A: no capturable como identidad estable** — el bridge no emite línea de sesión en auth exitoso y ninguna sesión sobrevivió (la autenticación del lane exec quedó probada por la PROGRESIÓN del rechazo: `55257` pasó schema y auth y falló recién en family-data parse).

## D1 — DEFECTO DE PRODUCTO A: market lane del AddOn dializa el endpoint equivocado (violación freeze §6.1)

- **Físico:** `[ntx] ntx: 192.168.31.132:55256 rejected: ntx: frame schema "echo.ntfeed.v1" is not "echo.ntx.v1"` a las 05:20:58.7Z.
- **Fuente:** el `EchoExecutionAddOn` dializa AMBOS lanes al mismo `ntxHost:ntxPort` (`EnsureMarketLane` y `EnsureExecLane` comparten endpoint, `EchoExecutionAddOn.cs:283-330/:419-464`) y el market lane habla `echo.ntfeed.v1` (`SendMarketHello`, `:324`). El **D6 Final Design Freeze §6.1** congela: market lane → **nt-feed-relay (Daedalus :9770)**, one-way, N1-certified, zero churn; execution lane → bridge listener con `echo.ntx.v1`. El bridge ntx rechaza cualquier schema distinto (`core/ntx/server.go:308`). ⇒ **el market lane del AddOn es estructuralmente incapaz de conectar** al único endpoint que su configuración le da; además su socket muerto queda `marketConnected=true` sin reader (outbound-only) ⇒ nunca re-dializa ni detecta la muerte.
- Sin efecto de seguridad (frame rechazado y cerrado; sin estado), pero bloquea la topología congelada del AddOn dual-channel.

## D2 — DEFECTO DE PRODUCTO B: frame `account` del lane ntx no parsea en el bridge (violación §6.1 "same payloads as ntfeed")

- **Físico:** `[ntx] ntx: 192.168.31.132:55257 rejected: ntx: family data does not parse: json: cannot unmarshal bool into Go struct field AccountData.resolved of type ntx.AccountRecord` a las 05:21:08Z (hello+auth de esa conexión PASARON).
- **Fuente:** AddOn (lane exec): `exec.Append("{\"match\":…,\"resolved\":").Append(resolved != null && match == "RESOLVED" ? "true" : "false").Append("}")` (`EchoExecutionAddOn.cs:~880-884`, comentario reclama "same evidence + match used by the bridge binding verification") — serializa `resolved` como **bool** y omite `discovered`/`balances`. Bridge: `AccountData{ Discovered []AccountRecord; Resolved *AccountRecord; Match string; Balances map }` (`core/ntx/observations.go:130-141`) con unmarshal estricto. El freeze §6.1 exige "same payloads as ntfeed": el payload ntfeed REAL (observable en el evidence sink del feed lane) manda `resolved` como **objeto** `{id,name,display_name}` + `discovered[8]` + `balances{}`. ⇒ **el frame account del lane ntx jamás puede parsear** ⇒ `VerifyBinding` jamás recibe match, positions/orders/executions jamás se publican (se emiten sólo si `match == "RESOLVED"`), el recovery barrier jamás puede completar. El lane MARKET del mismo AddOn serializa el payload ntfeed correcto (`:875-882`) — el bug es sólo de la rama exec.
- **Cadena de barrera observada (4.ª demostración fail-closed, causa raíz nueva):** session built 05:20:58.658Z → Connect pasó (auth exitosa <1 s) → **`account session exited` 05:21:02.350Z (+3.692 s)**, razón exacta `session: recovery barrier failed for E2T-GAU50-01: barrier: reconcile: ninjatrader: no position snapshot observed yet` — fail-closed correcto: sin positions venue reales (bloqueadas por D2) el barrier se negó a completar; reconciliación no debilitada.

## D3 — ANOMALÍA NT-SIDE RESIDUAL: el AddOn dejó de dializar tras el 2.º rechazo

- Tras el cierre de `55257` (05:21:08Z) **cero dials adicionales en ≥15 min** (0 sockets :9771 en dev-win, 0 líneas `[ntx]` nuevas), contra cadencia de diseño ≤5–10 s (`ExecReadLoop` EOF ⇒ re-dial +5 s, sin cap). El dial #2 sí ocurrió (+5 s tras el exit de la sesión #1 ⇒ reconexión real con identidad nueva+seq 0 demostrada conductualmente; auth re-pasó). Las hipótesis (muerte del timer NT por excepción en send al socket muerto del market lane vs. estado half-open indistinguible) **no discriminables agente-side** (ACL: log NT/StartTime/módulos denegados, 9.ª re-probe). El bridge restart (H) con el AddOn en silencio no ejercitaría nada ⇒ no se intentó como teatro.

## D/E — REAL ACCOUNT BINDING + OBSERVATION

- **Por el exec lane real: NOT_RUN** (ningún frame sobrevivió al parser; sin datos fabricados).
- **Feed lane real (mismo proceso NT PID 13068, evidence sink sin máscara, sesión `a9ddeb5b…` viva con frames cada 10 s):** discovery 8 cuentas (`Backtest, Playback101, Sim101, 5×RJARA…`), **exactamente 1 match**, `resolved {"id":"3","name":"RJARA114411201551","display_name":"RJARA114411201551"}`, `match RESOLVED`, **NT `Account.Id "3"` == hint ETCD — 8.ª sesión consecutiva**. Positions `[]`, orders `[]`; balances `NLV/cash 50000/50000`, `BP/uPnL/rPnL 0/0/0` (variante demo, 4.ª sesión documentándola). `CURRENT_NT_ACCOUNT_ID = "3"`; binding Name-primary `E2T-GAU50-01` ↔ `RJARA114411201551` sin drift.

## F–H — BARRIER / RECONNECT-FENCING / BRIDGE RESTART

- **REAL_RECOVERY_BARRIER = FAIL** (4.ª demostración; causa raíz ahora D2 — con el AddOn real el barrier es estructuralmente inalcanzable hasta remediar). `UnknownLiveOrders = 0`, `AccountMismatch = 0`, `ambiguous journal = 0` (M2 vacío), `command replay = 0`, `dropped_commands=0` en toda la sesión.
- **REAL_SESSION_RECONNECT:** la reconexión real del AddOn (identidad nueva + seq 0, +5 s, auth re-pasada) se observó una vez; sin sesión estable que fencear ⇒ **FAIL/NOT_RUN ejecutable**. Fencing F-S2-01/04 server-side permanece certificado weekend (mismo binario `484b550b…`).
- **BRIDGE_RESTART_RECOVERY = FAIL (NOT_RUN con AddOn real)** — D3. Weekend §8 (2× restart, 0-phantom, reconexión <1.5 s) sigue vigente lado transporte.

## I — NINJATRADER RESTART EVIDENCE: PASS (reutilizado, permitido por despacho)

El boot owner vigente (PID 13068, ≥2 boots hoy: feed hello `3bb88562…` 01:19:36Z, sesión actual `a9ddeb5b…` con `reconnects:1`) demostró sobre runtime real: Feed AddOn cargado y publicando ✔; Execution AddOn cargado con config `:9771` (log owner + dials `SYN_SENT→:9771` + hello `echo.ntx.v1` autenticado — 1.ª vez) ✔; cuenta discoverable (RESOLVED 1/8) ✔. No se pidió otro restart.

## J — G_HORIZON PRECHECK

`G_HORIZON_PRECHECK = PARTIAL_NEEDS_CREATED_ORDER` (4.ª vez, sin cambio): la cuenta GAU50 no tiene historial de la vertical y las superficies `LookbackDays*`/historia sólo son inspectables desde NT con el exec AddOn funcional end-to-end. No se creó orden.

## K — READINESS COMPOSITION (capturada con bridge corriendo, cada 30 s)

`ready_new_risk=false`; blockers observados (conjunto REDUCIDO vs intentos previos — coherentemente con la autenticación ocurrida): `[POSITION_NOT_FRESH RECONCILIATION_AUTHORITY_UNAVAILABLE STATIC_ELIGIBILITY_NOT_ELIGIBLE SUBMISSION_CAPABILITIES_NOT_EXACT_READY]`, `ambiguous_orders=0 mismatches=0 dropped_commands=0 recovered=false` — exactamente los esperados para lane-autenticado-pero-sin-observaciones + mercado cerrado. Separación: **EXECUTION_TRANSPORT_READY = NO** (defectos D1/D2; bridge-side certificado y listo) · **ACCOUNT_READY = feed-side YES (RESOLVED vivo) / exec-side NO** · **RECOVERY_READY = NO** · **MARKET_FRESHNESS = STALE** (último `event_ts 2026-10-02T21:38:25.95Z`, edad ≈31 h >> bound 30 s; Kafka p4 offset 5476476 @ 04:59:33Z = replay estático del boot, F-S2-02) · **NEW_RISK_READY = NO** (doble fail-closed: freshness + ventana GAU50-EVAL L–V, domingo cerrado).

## /final_safety_state — probado al cierre (no asumido)

- **G-EGRESS-0 restaurado y verificado:** unidad `echo-futures-bridge` **inactive + reset-failed + disabled**; `:9771` FREE (`ss`, sin listener ni sockets); clave ETCD `futures-bridge/accounts` **eliminada con ciclo guardado** (pre-read exacta `E2T-GAU50-01` → DELETED 1 → read-back ABSENT → cross-check MCP RO **21 claves == baseline pre-shot**); journal M2 **0 registros**; **0 COMMAND_FRAME** en todo el runtime; topic de comandos sin particiones (0 posibles); **0 LIVE run, 0 comandos, 0 ambigüedad** en toda la sesión.
- **Feed lane conectado y observando** (relay `:9770` + AddOn feed PID 13068, sesión `a9ddeb5b…`): permitido por final_safety_state; cuenta observable RESOLVED.
- **AddOns instalados lado owner** (bytes `2c8ab2cf`/`581a7087`/`9ca3fddc`); exec AddOn IDLE tras el silencio D3 (si re-dializara contra listener inexistente: refusal sin estado ni riesgo).
- **New-risk configurationally disabled** (sin sesión habilitada + sin topic M1 + STALE + domingo fuera de ventana).
- Worktree `~/aranea/work/d6-lane-final-20261003/echo` limpio al cierre, `HEAD == origin == ffa493d8`; herramienta ETCD efímera fuera del repo (`~/aranea/work/d6-reallane-cert-final-20261004/tool/`); evidencia en `~/aranea/work/d6-reallane-cert-final-20261004/evidence/` (`c-bridge-journal.log` captura completa, `c0-netstat-prebridge.txt`, timestamps).

## /product_changes

**NONE.** Cero commits, cero cambios de source. Los defectos D1/D2 quedan documentados con reproducción exacta; el mandato prohíbe remediar inline ("If a defect appears: return REMEDIATION_REQUIRED"). Nota de alcance: `git diff 40102ea5..ffa493d8` prueba que D1/D2 existen idénticos en `40102ea5` — nunca fue un skew de versión: el par AddOn↔bridge real jamás se había ejercitado (los gates previos usaron el probe, cuyo shape de frames es el del bridge).

## /close — Final handoff (FINAL PARSER-FIX RETRY — REAL C→K)

```text
D6_REAL_EXECUTION_LANE_NO_EGRESS =
REMEDIATION_REQUIRED (4.º intento; progreso histórico real: parser fix CONFIRMADO físicamente, AddOn cargado, dializa :9771, hello+auth del lane exec PASAN — la certificación C–K se detiene en DOS defectos de producto nuevos demostrados físicamente con repro exacta en fuente: D1 market-lane endpoint/schema viola freeze §6.1, D2 frame account del lane ntx bool-vs-objeto viola §6.1 "same payloads as ntfeed"; sin barrier posible hasta remediar)

SOURCE_SHA:
ffa493d8d179c9f9374d0a935e7916be15367ce8 (HEAD == origin == worktree limpio al inicio y al cierre)

CONFIG_PARSER_FIX_PHYSICAL:
PASS (log owner `config loaded: ntx=****.161:9771 … contracts=1` + confirmación conductual agente-side: 2× SYN_SENT→:9771 del PID NT + hello echo.ntx.v1 con auth aceptada — imposible con puerto 0; supersede definitivo de los 3 intentos previos)

NTX_EFFECTIVE_ENDPOINT:
192.168.31.161:9771 (efectivo, dializado por ambos lanes; exec lane autenticó)

FEED_ADDON_LOADED:
PASS (sesión a9ddeb5b34e74f6382aa597fa5594239 viva, ESTABLISHED PID 13068→:9770, frames cada 10 s, rediscovery RESOLVED 1/8)

EXECUTION_ADDON_LOADED:
PASS (1.ª vez en 4 intentos: log owner + dials físicos + ciclo Active; build instalada 2c8ab2cf = HEAD)

EXECUTION_LANE_REAL:
FAIL (transporte TCP + schema ntx + auth demostrados; sin sesión estable ni observaciones: D1 rechaza el market lane estructuralmente, D2 rechaza el frame account del exec lane; bridge/transporte server-side permanece certificado weekend — mismo binario 484b550b)

REAL_SESSION_ID_INITIAL:
NONE capturable (ninguna sesión sobrevivió; el bridge no emite identidad de sesión en auth exitoso y la sesión #1 murió a los +3.692 s; auth demostrada por progresión del reject de 55257: pasó schema+auth, falló en family-data)

ACCOUNT_BINDING:
PASS feed-side vivo (RESOLVED 1/8, RJARA114411201551 = NT id "3" == hint ETCD, 8.ª sesión consecutiva) · exec-side NOT_RUN (el frame que porta match/resolved para VerifyBinding jamás parsea — D2)

CURRENT_NT_ACCOUNT_ID:
"3"

ACCOUNT_OBSERVATION:
FAIL por el exec lane (NOT_RUN físico: frames rechazados por D2; sin datos fabricados) · feed-lane real documentado: discovery 8 cuentas, positions []/orders [], balances NLV/cash 50000/50000 demo, observaciones llegan al runtime (sink + Kafka p4 5476476)

REAL_RECOVERY_BARRIER:
FAIL — 4.ª demostración fail-closed, causa raíz NUEVA y de producto: "barrier: reconcile: ninjatrader: no position snapshot observed yet" a los +3.692 s del built (positions bloqueadas por D2); reconciliación no debilitada; 0 UnknownLiveOrders / 0 AccountMismatch / journal M2 0 / 0 replay

REAL_SESSION_RECONNECT:
FAIL (una reconexión real observada: identidad nueva + seq 0 a +5 s, auth re-pasada, cerrada por D2; después silencio D3; sin fencing ejercitable — F-S2-01/04 server-side certificados weekend)

REAL_SESSION_FENCING:
FAIL (NOT_RUN ejecutable — sin sesión estable; cero command frames en toda la sesión)

BRIDGE_RESTART_RECOVERY:
FAIL (NOT_RUN con AddOn real — D3: AddOn en silencio, restart no ejercita nada; weekend §8 PASS de transporte vigente)

G_HORIZON_PRECHECK:
PARTIAL_NEEDS_CREATED_ORDER (4.ª vez; superficies LookbackDays* requieren lane funcional end-to-end; NO se creó orden)

EXECUTION_TRANSPORT_READY:
NO (D1+D2; bridge-side certificado y listo para re-enable en ~1 min tras la remediación + pickup)

CURRENT_MARKET_FRESHNESS:
STALE (event_ts 2026-10-02T21:38:25.95Z, edad ≈31 h >> bound 30 s; p4 5476476 @ 04:59:33Z = replay estático del boot — F-S2-02; domingo, CME cerrado: blocker esperado y válido)

NEW_RISK_READY:
NO (doble fail-closed: freshness + ventana GAU50-EVAL L–V con domingo cerrado)

PHYSICAL_ORDERS_SENT:
0

PHYSICAL_ORDERS_MODIFIED:
0

PHYSICAL_ORDERS_CANCELLED:
0

PRODUCT_CODE_CHANGES:
NONE (cero commits; los 2 defectos documentados con repro exacta para el shot de remediación)

RESIDUAL_FINDINGS:
1) DEFECTO D1 — EchoExecutionAddOn market lane dializa ntxHost:ntxPort (9771) con schema echo.ntfeed.v1; freeze §6.1 lo destina al nt-feed-relay :9770; socket muerto queda marketConnected=true sin reader (nunca re-dializa); repro: físico 05:20:58.7Z `frame schema "echo.ntfeed.v1" is not "echo.ntx.v1"` · 2) DEFECTO D2 — frame account del lane ntx serializa resolved como bool (EchoExecutionAddOn.cs ~880-884) vs bridge AccountData.Resolved *AccountRecord (observations.go:137); freeze §6.1 "same payloads as ntfeed" (payload ntfeed real manda objeto+discovered+balances); repro: físico 05:21:08Z `cannot unmarshal bool into …AccountData.resolved` · 3) D3 anomalía NT-side: cero dials ≥15 min tras el 2.º reject vs cadencia ≤10 s (timer muerto vs half-open; log NT owner discrimina) · 4) variante demo balances 50000/50000 persistente (5.ª sesión; re-observar en ventana) · 5) ACL owner 9.ª re-probe (log NT/StartTime/módulos denegados)

OWNER_DECISION_REQUIRED:
Autorizar el shot de remediación de producto (no es ciclo de instalación nuevo): corregir D1 (endpoint del market lane según freeze §6.1 — config separada o dial al relay :9770 — y detección de socket muerto) y D2 (serializar el frame account del lane ntx same-as-ntfeed con resolved objeto + discovered/balances), con tests estructurales + shadow-compile 8.1.8.3 + re-stage del bundle (patrón EchoD6Bundle) y ciclo owner W1 → re-despacho C–K. OD-D6-1 sigue AUTHORIZED y SIN consumir (0 órdenes en 4 intentos).

NEXT_MANAGER_ACTION:
Veredicto REMEDIATION_REQUIRED ⇒ no certificar lane ni ejecutar ladder. (a) Despachar remediación D1+D2 acotada (fuente arriba; el bridge NO requiere cambios — su parser implementa el payload congelado). (b) Domingo 2026-10-04 ≥17:00 CT: G-REALTIME es feed-lane-only y NO depende de estos defectos — certificable con el runbook §M del intento 1 (feed AddOn intacto). (c) Tras remediación + W1 + re-despacho C–K en verde: ladder congelado §N en la primera ventana admisible lun 2026-10-05 00:00–15:50 CT. No emitir EF_D6_E2E_PASS.
```

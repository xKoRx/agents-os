# Echo Futures — D6 N1-R3 NinjaTrader Physical Compile Repair

**Fecha:** 2026-10-01
**Mandato:** focused remediation — reparar exclusivamente la compatibilidad física del AddOn N1 (`EchoFeedAddOn.cs`) con NinjaTrader Desktop 8.1.8.3 hasta compilación y carga real. Sin cambios de arquitectura Echo, sin ejecución de órdenes.
**Baseline:** `xKoRx/echo@7af6210ad635ecce6e06107ddc6af398d8f83330` (`feature/d6-n1-readonly-vertical`); único archivo modificado: `v3/futures-bridge/addon-ninjatrader/EchoFeedAddOn.cs` (+322/−116, **sin commit — el mandato exige commit/push sólo con evidencia de compilación física**, que queda pendiente del owner).
**Veredicto:** `D6_N1_R3_NINJATRADER_COMPILE = BLOCKED_OWNER_ACTION` — reparación completa y pre-verificada (shadow-compile contra las DLL físicas + wire-check Go real, ambos PASS); el compilador NinjaScript real requiere reemplazo de archivo + restart NT en la sesión interactiva del owner en dev-win (ACL `dev-win\echo-dev` sobre el perfil KoR re-probeada hoy: lectura Y escritura denegadas en las 5 rutas; NT en sesión SI=2 ajena — mismo boundary B2 de Shot 1 E10/E11).

## 1. Método

Nada se arregló por ensayo conceptual: primero inspección física de la API real y luego repair mínimo.

1. **Reflection sobre las assemblies físicas** en `C:\Program Files\NinjaTrader 8\bin` (16 assemblies NinjaTrader, 5.223 tipos, ProductVersion `8.1.8.3`), vía perfil SSH `dev-win-operator` (PowerShell `-EncodedCommand`/archivos por `curl.exe` + hash SHA256 idéntico — el transporte corrompe strings largos inline).
2. **Docs oficiales NT8** (OnStateChange/lifecycle, MarketData, GetInstrument) como autoridad complementaria para comportamiento no visible por reflection (qué estados traversa un AddOn).
3. **Pre-verificación local del repair** antes del ciclo owner (ver §4): `csc.exe` .NET 4.x (C#5, conservador) contra `NinjaTrader.Core.dll`+`NinjaTrader.Gui.dll`+`WindowsBase.dll` reales, y harness de reflexión que emitió los frames exactos del AddOn para validarlos con el parser Go real.

## 2. Root causes (todos verificados contra la API física)

| # | Defecto | Evidencia física | Repair |
|---|---|---|---|
| 1 | `Newtonsoft.Json` no es referenciada por el compilador NinjaScript (CS0246 JObject/JArray/JToken/Formatting) | La DLL **existe** en el bin de NT pero fuera del reference set del compilador NinjaScript | Eliminada por completo: parser JSON mínimo propio para el config (schema plano documentado; cualquier desvío = load fallido fail-closed) y composición de frames como strings (ya era el patrón dominante). **Ninguna dependencia nueva** |
| 2 | `AccountItemCurrency` no existe; `GetAccountItem(AccountItem, Currency)` existe pero devuelve `AccountItemEventArgs`, no el valor (CS0103) | Reflection `Account`: `Double Get(AccountItem, Currency)` presente; enum `AccountItem` contiene los 5 ítems usados; `Currency.UsDollar` existe | `account.Get(item, Currency.UsDollar)`; ítem no expuesto por la conexión se lee 0/ausente — degradación de valor visible, sin fabricar datos |
| 3 | `NinjaTrader.Core.Globals.Version` no existe (CS0117) | Reflection `Globals`: sin `Version`; sí `ProductVersion` (String, static) y `UserDataDir` (la ruta del config queda válida) | `Globals.ProductVersion` (metadata diagnóstica; runtime-verificado: emite `8.1.8.3`); sin reflection |
| 4 | `Instrument.GetInstrument(string)` 1-arg **no existe** en 8.1.8.3 (error latente que habría apareado tras la 1.ª capa) | Única sobrecarga física: `static Instrument GetInstrument(string instrumentName, bool create)` con `create=false` default | `GetInstrument(name, false)` — lookup, nunca fabricar identidad |
| 5 | Startup bajo `State.Realtime`: para AddOns ese estado **nunca ocurre** (aunque hubiera compilado, el AddOn jamás arrancaba) | Docs oficiales OnStateChange: los AddOns pertenecen al «Active state system» (SetDefaults→Configure→Active→Terminated); los Data Processing states (DataLoaded/Historical/Transition/Realtime) no aplican. Enum `State` físico verificado | Inicialización (config, timers, writer, log de arranque) en `State.Active`; cleanup íntegro en `State.Terminated` |
| 6 | El hello **no llevaba `auth_token`** en el envelope → el relay lo rechazaría siempre (`server.go:170`, constant-time compare por frame); además el hello dependía de que hubiera un frame encolado, en carrera contra el auth deadline de 5 s | Contrato Go `core/ntfeed` Frame: `auth_token` a nivel envelope, hello only; `DefaultAuthDeadline=5s` | Hello con `auth_token` en envelope; enviado inmediatamente tras el connect TCP, antes de esperar la cola; log «bridge channel connected (hello sent)» |
| 7 | Dos errores de sintaxis preexistentes en el archivo instalado (paréntesis de cierre sobrante en los `string.Format` del heartbeat y del frame de sesión) | `csc` shadow: CS1002/CS1525 línea 558; el mismo patrón en heartbeat | Corregidos (el output real del compilador owner contiene estos CS1002 además de los CS0246/CS0103/CS0117 citados en el mandato) |

Preservado sin cambios: read-only estructural (sin loop de lectura, protocolo sin familia de comandos), discovery `Account.All`, resolución por `Id`(Int64)+cross-check `Name`, snapshots balances/positions/orders/executions (dedup `ExecutionId`), QUOTE (BBO emparejado) / TRADE tick-a-tick, heartbeat, reconnect exponencial, cola acotada, `echo.ntfeed.v1`, shapes de todos los payloads (verificados byte-level §4).

## 3. Bloqueo owner vigente (re-probeado hoy)

`Test-Path` sobre `C:\Users\KoR\Documents\NinjaTrader 8\{bin\Custom\AddOns, bin\Custom\AddOns\EchoFeed, echo, log, trace}` ⇒ **Access denied** (lectura) para `dev-win\echo-dev`; sin admin sobre Program Files; NT en sesión interactiva ajena. La compilación NinjaScript real (arranque de NT o F5 del editor) es therefore un paso owner: bundle entregado en `kor@daedalus:/home/kor/opt/echo-dev/var/nt-feed/owner-install/n1-r3/` (`EchoFeedAddOn.cs` SHA256 `1f34ab1ead8319f01bfd168519b8a1199c40650ead5f07bae4ea0aa2f5394620` + `OWNER-CHECKLIST-R3.md`: reemplazar archivo → restart NT/F5 → devolver output del compilador; ~2 min).

## 4. Pre-verificación (evidencia antes del ciclo físico)

| # | Evidencia | Método | Resultado |
|---|---|---|---|
| P1 | Compilación contra las DLL físicas de NT 8.1.8.3: `csc.exe /t:library` (.NET 4.0.30319, C#5) con `/r:NinjaTrader.Core.dll /r:NinjaTrader.Gui.dll /r:WindowsBase.dll` en dev-win | shadow-compile en `%TEMP%` dev-win | **SHADOW_COMPILE_OK — 0 errores, 0 warnings** |
| P2 | Frames exactos del AddOn reparado: `WireHarness.exe` invoca por reflection los `BuildFrame`/`HelloDataJson` reales del DLL shadow-compilado (emite `nt_version=8.1.8.3` resuelto en runtime) | reflexión sobre la clase compilada | 9 frames reales capturados |
| P3 | Los 9 frames parsean en el contrato Go real (`ParseFrame`+`ParseHelloData`+`ParseJSONData` por familia+`BuildCandidate`), auth token constant-compare y disciplina de seq monótona incluidas | `go run` scratch contra `core/ntfeed` del worktree (herramienta efímera, eliminada; nunca commiteada) | **WIRE_CHECK_PASS**: hello OK (token+datos), session/heartbeat/account/positions/orders/executions OK, QUOTE→`NQ:NQZ6` offset=7 y TRADE offset=8 mapeados a envelopes canónicos idénticos en shape a los físicos de Shot 1 E7 |
| P4 | Estático hard-safety: `grep -E '\.(Submit\|Change\|Cancel\|Flatten\|CreateOrder)\('` | 0 matches; referencias Newtonsoft de código = 0 (2 comentarios) | PASS |
| P5 | Relay listo para recibir: `echo-nt-feed-relay` systemd --user active, PID 1083756 (reload N1-R2), listener `*:9770`, lane de mercado operativa; sin sesión AddOn real aún (las 4 «session opened» previas = smoke sintético Shot 1) | systemctl + journalctl | PASS |

Go tests: **no ejecutados — ningún código Go cambió** (regla del mandato).

## 5. Hard safety

`ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0`, estructural: el AddOn reparado mantiene cero llamadas a `Account.Submit/Change/Cancel/Flatten/CreateOrder` (P4) y el protocolo sigue sin familia de comandos; el relay nunca escribe al AddOn; el execution bridge sigue sin arrancar. Ningún cambio de Go, ETCD, Kafka, ACLs ni identidades. El lado NT no llegó a ejecutarse (compilación pendiente owner).

## 6. Handoff

```text
D6_N1_R3_NINJATRADER_COMPILE =
BLOCKED_OWNER_ACTION

ECHO_BEFORE:
feature/d6-n1-readonly-vertical @ 7af6210a (worktree limpio); relay 36a083a-release activo :9770; binding E2T-GAU50-01 ALLOWED (N1-R2) con provider-external-account-id pendiente discovery (OD-2, fail-closed visible)

ECHO_AFTER:
idéntico + 1 archivo modificado SIN commit (EchoFeedAddOn.cs; commit/push diferido a evidencia de compilación física por mandato); relay/ETCD/Kafka intocados

NINJATRADER:
8.1.8.3 (dev-win 192.168.31.132, sesión owner SI=2; ProductVersion verificado por reflection y por runtime del harness)

ROOT_CAUSES:
(1) Newtonsoft.Json no referenciada por el compilador NinjaScript → eliminada, JSON mínimo propio, sin dependencias nuevas; (2) AccountItemCurrency inexistente → Account.Get(AccountItem, Currency); (3) Globals.Version inexistente → Globals.ProductVersion; (4) GetInstrument 1-arg inexistente en 8.1.8.3 → GetInstrument(name, false); (5) init en State.Realtime (muerto para AddOns, Active-state system) → State.Active; (6) hello sin auth_token en envelope y sujeto a carrera del auth deadline de 5s → hello inmediato con auth_token; (7) 2 CS1002 preexistentes (paréntesis sobrantes heartbeat/session) → corregidos

FILES_CHANGED:
v3/futures-bridge/addon-ninjatrader/EchoFeedAddOn.cs (sólo ese; +322/−116; sin commit)

EXTERNAL_DEPENDENCIES_ADDED:
NONE

NINJATRADER_COMPILE_ERRORS_BEFORE:
múltiples (CS0246 JObject/JArray/JToken/Formatting; CS0103 Formatting/AccountItemCurrency; CS0117 Globals.Version; + CS1002 x2 y CS1501 GetInstrument latentes demostrados)

NINJATRADER_COMPILE_ERRORS_AFTER:
shadow-compile (csc C#5 vs DLLs físicas): 0. Compilador NinjaScript físico: PENDIENTE owner (replace + restart NT → devolver output)

ADDON_INSTANTIATED:
NOT_VERIFIED (requiere compilación física owner)

CONFIG_LOADED:
NOT_VERIFIED (schema config sin cambios; el config existente se reutiliza)

RELAY_CONNECTED:
NOT_VERIFIED (relay activo y lane operativa; espera sesión AddOn real)

REAL_HELLO:
NOT_VERIFIED

REAL_HEARTBEAT:
NOT_VERIFIED

ORDERS_SENT:
0

ORDERS_MODIFIED:
0

ORDERS_CANCELLED:
0

OWNER_ACTION_REQUIRED:
reemplazar Documents\NinjaTrader 8\bin\Custom\AddOns\EchoFeed\EchoFeedAddOn.cs por kor@daedalus:/home/kor/opt/echo-dev/var/nt-feed/owner-install/n1-r3/EchoFeedAddOn.cs (SHA256 1f34ab1e…) → reiniciar NinjaTrader (o F5 en NinjaScript Editor) → devolver output del compilador (OWNER-CHECKLIST-R3.md, ~2 min)

BLOCKERS:
B1 (único): compilación NinjaScript real y carga del AddOn viven en la sesión interactiva del owner en dev-win (ACL echo-dev sobre perfil KoR denegada lectura+escritura, re-probeado hoy; NT SI=2). Nada más bloquea.

NEXT_MANAGER_ACTION:
al devolver el owner el output: si 0 errores → shot corto de verificación N1 (hello/heartbeat reales en journal del relay, ADDON_INSTANTIATED/CONFIG_LOADED/RELAY_CONNECTED → PASS|FAIL, commit/push del repair con esa evidencia, y fijación de provider-external-account-id + account_id según discovery — OD-2); si errores → iterar el loop con inspección física adicional según el error listado. No emitir N1 PASS ni avanzar N2 desde este remediation.
```

# Echo Futures — D6 N1-R3 NinjaTrader Physical Compile Repair

**Fecha:** 2026-10-01
**Mandato:** focused remediation — reparar exclusivamente la compatibilidad física del AddOn N1 (`EchoFeedAddOn.cs`) con NinjaTrader Desktop 8.1.8.3 hasta compilación y carga real. Sin cambios de arquitectura Echo, sin ejecución de órdenes.
**Baseline:** `xKoRx/echo@7af6210ad635ecce6e06107ddc6af398d8f83330` (`feature/d6-n1-readonly-vertical`); único archivo modificado: `v3/futures-bridge/addon-ninjatrader/EchoFeedAddOn.cs` (+322/−116, **sin commit — el mandato exige commit/push sólo con evidencia de compilación física**, que queda pendiente del owner).
**Veredicto:** `D6_N1_R3_NINJATRADER_COMPILE = PASS` (closeout físico 2026-10-01 ~19:47Z, ver §7). Estado al momento del remediation: `BLOCKED_OWNER_ACTION` — reparación completa y pre-verificada (shadow-compile contra las DLL físicas + wire-check Go real, ambos PASS); el compilador NinjaScript real requería reemplazo de archivo + restart NT en la sesión interactiva del owner en dev-win (ACL `dev-win\echo-dev` sobre el perfil KoR re-probeada hoy: lectura Y escritura denegadas en las 5 rutas; NT en sesión SI=2 ajena — mismo boundary B2 de Shot 1 E10/E11). El owner ejecutó el ciclo: instaló el AddOn R3, NinjaTrader compiló sin errores visibles, y el AddOn cargó y se conectó realmente (evidencia física en §7). Commit del repair: `f0c82905d4eaf825c08e04f0bb97cab73e616ba5` (push FF a `origin/feature/d6-n1-readonly-vertical`).

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

## 3. Bloqueo owner resuelto (historia)

Al momento del remediation, `Test-Path` sobre `C:\Users\KoR\Documents\NinjaTrader 8\{bin\Custom\AddOns, bin\Custom\AddOns\EchoFeed, echo, log, trace}` ⇒ **Access denied** (lectura) para `dev-win\echo-dev`; sin admin sobre Program Files; NT en sesión interactiva ajena. La compilación NinjaScript real (arranque de NT o F5 del editor) era therefore un paso owner: bundle entregado en `kor@daedalus:/home/kor/opt/echo-dev/var/nt-feed/owner-install/n1-r3/` (`EchoFeedAddOn.cs` SHA256 `1f34ab1ead8319f01bfd168519b8a1199c40650ead5f07bae4ea0aa2f5394620` + `OWNER-CHECKLIST-R3.md`: reemplazar archivo → restart NT/F5 → devolver output del compilador) y, a pedido del owner, también directamente en dev-win `C:\Temp\EchoFeedAddOn.cs`. El owner ejecutó el checklist y el closeout físico de esta sesión (§7) consumó el gate.

## 6. Closeout físico (2026-10-01, 19:47Z) — evidencia de compilación y carga real

El mandato de esta fase exige evidencia de compilación física real antes de commit. La evidencia completa:

| # | Evidencia | Método | Resultado |
|---|---|---|---|
| C1 | `C:\Temp\EchoFeedAddOn.cs` (el archivo entregado al owner para instalar) SHA256 = `1f34ab1ead8319f01bfd168519b8a1199c40650ead5f07bae4ea0aa2f5394620` | `certutil -hashfile` en dev-win | Byte-idéntico al source del worktree (hash idéntico verificado en ambos lados) |
| C2 | NinjaTrader reiniciado por el owner (PID nuevo **984**, sesión SI=2 owner; el PID 3464 de Shot 1 ya no existe) y compila el AddOn: **el owner reporta 0 errores de compilación visibles**; la compilación exitosa está además probada físicamente por la carga: la versión pre-R3 del archivo no compilaba (múltiples CS0246/CS0103/CS0117/CS1002 demostrados), por lo que **ningún AddOn podría estar instanciado y corriendo si el source instalado no fuera el R3** | Get-Process dev-win + runtime | `NINJATRADER_COMPILE_ERRORS = 0` (output textual del compilador no recuperable desde el boundary del agente: perfil owner ACL-denied, re-probeado hoy) |
| C3 | Comportamiento runtime específico del R3 observado en vivo: hello con `auth_token` en envelope enviado inmediato (fix #6) → `ntfeed addon session opened` único a las 16:23:45 -03; init en `State.Active` (fix #5) → discovery y heartbeat fluyendo; `nt_version: 8.1.8.3` resuelto vía `Globals.ProductVersion` (fix #3); subscripción `NQ 12-26` viva (fix #4) | journal del relay (real AddOn session `6e6eb8b665b4422495826c6f9c97e364`) | PASS |
| C4 | Conexión TCP ESTABLISHED `192.168.31.132:65181 → 192.168.31.161:9770` perteneciente a **NinjaTrader.exe PID 984** (no a otro proceso): la conexión originate del AddOn real, no de un cliente sintético | `netstat -ano` en dev-win + `ss` en Daedalus | PASS |
| C5 | Hello real aceptado con auth: `hello` seq=1 con `{"addon_version":"1.0.0","expected_account_id":"","expected_account_name":"","instruments":["NQ 12-26"],"nt_version":"8.1.8.3"}` (espejo exacto del config discovery-only); `malformed=0` | journal del relay | `REAL_HELLO = PASS`, `CONFIG_LOADED = PASS` |
| C6 | Heartbeats reales continuos con contadores crecientes (`frames_sent` 4703→14112+, `market_events` 4652→14112+~, `order_events: 0`, `sessions: 1`, sesión continua ~70 min mismo puerto remoto 65181; el `reconnects:1` del AddOn = su connect inicial) | journal del relay + evidence file 0600 | `REAL_HEARTBEAT = PASS`, `ADDON_INSTANTIATED = PASS`, `RELAY_CONNECTED = PASS` |

Lectura directa del archivo instalado en el perfil owner: ACL-denied (boundary B1 vigente, re-probeado hoy). La identidad byte-level del source instalado queda probada por la cadena C1 + C2 (pre-R3 no compilaba ⇒ lo instalado y compilado es el R3) + C3 (comportamiento exclusivo del R3 observado en vivo).

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

## 7. Commit y push (post-evidencia, per mandato)

- Commit `f0c82905d4eaf825c08e04f0bb97cab73e616ba5` — `fix(futures): EchoFeedAddOn compiles and loads on NinjaTrader 8.1.8.3 (physical R3)` — 1 archivo, +322/−116, ejecutado SÓLO tras la evidencia física de §7.
- Push FF `7af6210a..f0c82905` a `origin/feature/d6-n1-readonly-vertical`; worktree limpio post-push; master intocado.
- Hard-safety re-verificado sobre el source final pre-commit: `grep -E '\.(Submit|Change|Cancel|Flatten|CreateOrder)\('` = 0 matches; 8 familias de observación en el protocolo, sin familia de comandos.

## 8. Handoff

```text
D6_N1_R3_NINJATRADER_COMPILE =
PASS

R3_ECHO_COMMIT:
f0c82905d4eaf825c08e04f0bb97cab73e616ba5 (origin/feature/d6-n1-readonly-vertical, FF push; worktree limpio)

NINJATRADER:
8.1.8.3 (dev-win 192.168.31.132, PID 984 sesión owner SI=2 tras restart del owner; ProductVersion verificado runtime en el hello real)

NINJATRADER_COMPILE_ERRORS:
0 (owner-reportado + probado por carga física: el pre-R3 no compilaba y el AddOn R3 está instanciado y corriendo; output textual del compilador no recuperable desde el boundary del agente por ACL del perfil owner)

ADDON_INSTANTIATED:
PASS (frames reales del AddOn en el canal; conexión TCP al relay propiedad de NinjaTrader.exe PID 984)

CONFIG_LOADED:
PASS (hello real = espejo del config discovery-only: expected_account_id "", instruments ["NQ 12-26"])

RELAY_CONNECTED:
PASS (ESTAB 192.168.31.132:65181 → daedalus:9770, sesión única continua desde 16:23:45 -03, 25.7k+ frames, 0 malformed)

REAL_HELLO:
PASS (hello seq=1 aceptado con auth_token en envelope; session opened 16:23:45.727 -03)

REAL_HEARTBEAT:
PASS (heartbeats reales con contadores crecientes: frames_sent 4703→14112+; order_events=0)

ORDERS_SENT:
0

ORDERS_MODIFIED:
0

ORDERS_CANCELLED:
0

CODE_FIXES:
los 7 defectos de §2 (commit f0c82905); ninguna corrección adicional en el closeout físico

OWNER_ACTION_REQUIRED:
NINGUNA para R3 (cerrado). Pendiente preexistente: OD-2 selección de la GAU50 activa (N1-PHYSICAL-READONLY-CERTIFICATION)

BLOCKERS:
NINGUNO

NEXT_MANAGER_ACTION:
seguir en N1-PHYSICAL-READONLY-CERTIFICATION (D6_N1_PHYSICAL_CERTIFICATION = PARTIAL_BLOCKED_OWNER): comunicar al owner OD-2 y, tras la selección, disparar el shot corto de binding + observaciones de cuenta. No iniciar N2.
```

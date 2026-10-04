# Echo Futures — D6 Owner Bundle Build (pickup fix C1, instalación owner)

**Shot:** D6 — BUILD + STAGE OWNER NINJATRADER BUNDLE — TOP Senior Build / Release Preparation Specialist (one-shot, fresh context; no Manager, no Owner, no certificación física)
**Date:** 2026-10-03 → 2026-10-04 (evidencia de compile 2026-10-04T00:14:28Z)
**Project:** [[Echo Futures]]
**Baseline:** `xKoRx/echo@d361008bfe4aa54fe3d8b6380d290bf92e1f1c08` (`origin/feature/d6-shot1-execution-vertical`; FF sobre `40102ea5`; incluye el repair fail-closed de `LoadConfig` del incidente real-lane 2026-10-03)
**Verdict:** `D6_OWNER_BUNDLE = READY` — bundle autocontenido staged en dev-win `C:\Temp\EchoD6Bundle\`, shadow-compile real 0 errores, hashes byte-identicos, scripts de instalacion/verificacion probados en dry-run.
**Safety:** `PHYSICAL_ORDERS_SENT = 0` · sin bridge · sin mutaciones ETCD · sin publishing Kafka · perfil NinjaTrader del Owner INTACTO (ACL respetada; la instalación es ciclo owner).

---

## 1. Source truth (repo, no copias C:\Temp)

| Chequeo | Resultado |
|---|---|
| Branch | `feature/d6-shot1-execution-vertical` |
| HEAD | `d361008bfe4aa54fe3d8b6380d290bf92e1f1c08` |
| origin/HEAD | idéntico (`git fetch` + `rev-parse origin/...` = mismo SHA) |
| Worktree | limpio (`status --porcelain` = 0) |
| Clone físico | `~/aranea/work/d6-shot1-20261001/echo` (worktree D6 Shot 1) |
| Fuentes únicas | `v3/futures-bridge/addon-ninjatrader/EchoFeedAddOn.cs` (una sola clase `EchoFeedAddOn`) · `EchoExecutionAddOn.cs` (una sola clase `EchoExecutionAddOn`) — sin duplicados en el input de build (incidente de fuente duplicada NinjaScript no reproducible desde HEAD) |

Hashes fuente @ HEAD (coinciden con lo declarado en real-lane C1):

- `EchoExecutionAddOn.cs` = `72d97ad6c776ba56ea0d8aadfd44be2caa12ab884602c29995ffe5e75e92653f` (incluye fix fail-closed LoadConfig, 11 líneas; test estructural `config_guard_test.go` en el repo, suite 5/5)
- `EchoFeedAddOn.cs` = `581a7087b1b870c78ac43e67027e5edaacf59134f4bf5f03d8b9aec9d7fd5ae4` (byte-idéntico Shot 3)
- `echo-execution-addon.json` = `9ca3fddc31330b2d5b485fd0869801b486b1443972bbf5ba50c56862feeea71b` (config validada vigente, weekend-readiness; copia canónica Daedalus `owner-install/weekend-20261003/`; C:\Temp NO usado como autoridad)

## 2. Config validation (sin imprimir secretos)

| Campo | Valor | Chequeo |
|---|---|---|
| ntx_host | `192.168.31.161` | PASS (== host del bridge DEV en Daedalus) |
| ntx_port | `9771` | PASS (mandato: != 9771 ⇒ FAIL; no aplicó) |
| account_name | `RJARA114411201551` | PASS |
| account_id | `3` | runtime hint según diseño Name-primary (verificado vivo en 4+ sesiones, intento 1/final-cert) |
| contracts | `NQZ6` ↔ `NQ 12-26` | PASS |
| snapshot/heartbeat | 5 s / 5 s | PASS |
| auth_token | PRESENTE_REDACTADO | 64 hex, presente en el JSON, jamás impreso ni persistido en logs/reportes |

## 3. Shadow compile real — NinjaTrader 8.1.8.3 (dev-win 192.168.31.132)

Método D6 probado (Shot 1/Shot 3): `csc.exe` .NET Framework64 v4.0.30319, `/nologo /t:library`, contra las DLL físicas instaladas:

- `C:\Program Files\NinjaTrader 8\bin\NinjaTrader.Core.dll` (6,715,752 B, presente)
- `C:\Program Files\NinjaTrader 8\bin\NinjaTrader.Gui.dll` (14,060,392 B, presente)
- `C:\Windows\Microsoft.NET\Framework64\v4.0.30319\WPF\WindowsBase.dll` (presente)

`NinjaTrader.exe` FileVersion = **8.1.8.3** (verificado por `VersionInfo`).

| Target | Exit | Errores | Warnings |
|---|---|---|---|
| EchoFeedAddOn.cs → DLL shadow | **FEED_EXIT=0** | **0** | **0** |
| EchoExecutionAddOn.cs → DLL shadow | **EXEC_EXIT=0** | **0** | **3 preexistentes** |

Compile timestamp: `2026-10-04T00:14:28Z`. Los 3 warnings son EXACTAMENTE los preexistentes de Shot 1/Shot 3 (ninguno nuevo introducido por el fix C1): `CS0612 Account.CreateOrder(...) obsoleta @654` (gate G-STOP/G-E2E) y `CS0649 marketEvents/accountEvents @52` (lane de market no cableada en build stageado). DLLs de salida solo en staging `C:\Users\TEMP\d6bundle-src\` — **NADA instalado en NinjaTrader**.

Transporte de fuentes: http.server efímero en Daedalus (192.168.31.161:18099) + `curl.exe` dev-win, SHA256 verificado byte-a-byte en ambos lados (los 7 archivos); servidor apagado al cierre.

## 4. Stage bundle — `C:\Temp\EchoD6Bundle\`

Recreado limpio (sin restos de bundles anteriores; los archivos sueltos viejos de `C:\Temp` —pre-fix `EchoExecutionAddOn.cs` `b2a29a36…`— quedan fuera del bundle y quedan SUPERSEDED por este bundle):

| Archivo | Bytes | SHA256 |
|---|---|---|
| `EchoFeedAddOn.cs` | 45,803 | `581a7087b1b870c78ac43e67027e5edaacf59134f4bf5f03d8b9aec9d7fd5ae4` |
| `EchoExecutionAddOn.cs` | 47,492 | `72d97ad6c776ba56ea0d8aadfd44be2caa12ab884602c29995ffe5e75e92653f` |
| `echo-execution-addon.json` | 304 | `9ca3fddc31330b2d5b485fd0869801b486b1443972bbf5ba50c56862feeea71b` |
| `INSTALL-ECHO-D6.ps1` | 5,613 | `635ab76a7785b9862d053f2d51e0e142c27d32743f7e068ae608245af03a9af8` |
| `VERIFY-ECHO-D6.ps1` | 3,956 | `35ed7480b735098c28e254dfc814d8a1e2e7f407c9eaa0d0ac0823971706e999` |
| `SHA256SUMS.txt` | 266 | `adac26ed2bbae3b9314b22b95b719c2aebb950183b0dfea320acd047d25ba7b9` |
| `BUILD-INFO.txt` | 1,653 | `f6bac2a280ba3d338f1835ef7ebf77c0c2e9e7ce1a2118e575bf0b677edcac0b` |

`STAGE_ECHO_D6_BUNDLE = PASS` (hashes recalculados DESDE la ubicación stageada contra `SHA256SUMS.txt`; repo ↔ bundle identidad byte-a-byte). Sin token en `SHA256SUMS.txt` ni `BUILD-INFO.txt` (el token viaja solo DENTRO del JSON).

## 5. Scripts owner + dry-run evidence

**`INSTALL-ECHO-D6.ps1`** (parámetros extra `-NtRoot`/`-AllowNtRunning` SOLO para dry-run/CI; el owner corre sin parámetros): guard NT-corriendo → resuelve `$env:USERPROFILE\Documents\NinjaTrader 8` → crea `bin\Custom\AddOns\EchoFeed\` + `echo\` → instala AMBOS AddOns en la MISMA ubicación canónica → instala config → elimina SOLO los duplicados conocidos de raíz (`AddOns\EchoFeedAddOn.cs` / `AddOns\EchoExecutionAddOn.cs`) → exige exactamente 1 declaración por clase en todo `bin\Custom` (FAIL con listado file:line si hay duplicados) → compara SHA256 bundle↔destino → parsea el JSON instalado (host/port/account; jamás imprime token) → `INSTALL_ECHO_D6 = PASS` + "Abre/reinicia NinjaTrader ahora." No inicia NT.

**`VERIFY-ECHO-D6.ps1`** — 100% read-only: paths, tamaños, SHA256, nº de copias por clase, host/port/account, `auth_token present=True` (booleano, sin valor). `VERIFY_ECHO_D6 = PASS|FAIL`.

**Dry-runs ejecutados en dev-win sobre perfil simulado `C:\Users\TEMP\sim-nt` (eliminado al cierre; perfil real del Owner jamás tocado):**

| Prueba | Resultado |
|---|---|
| Syntax-check (PowerShell Language Parser) ambos scripts | PASS, 0 errores |
| Guard NT-corriendo con NT REAL corriendo (PID 4576), sin parámetros | PASS — "Cierra NinjaTrader antes de instalar", exit 2, cero escrituras |
| INSTALL negativo (duplicado en raíz + copia extra en subcarpeta `Old\`) | PASS — eliminó solo el duplicado de raíz, FAIL con listado exacto de las 2 declaraciones `EchoExecutionAddOn` (exit 1) |
| INSTALL positivo (limpio) | PASS — 1 declaración por clase, SHA256 OK ×3, config OK |
| VERIFY positivo | PASS — paths/sizes/hashes/copias=1/config, token solo como booleano |
| VERIFY negativo (tamper `ntx_port`→0) | PASS — doble detección: SHA256 MISMATCH + `ntx_port inesperado: 0` ⇒ `VERIFY_ECHO_D6 = FAIL` |
| Restore + INSTALL re-run | PASS |

Rutas incorrectas / variables sin definir: ninguna (parser limpio + 6 ejecuciones completas cubriendo ambos scripts, incluida resolución `$PSScriptRoot` desde cwd ajeno).

## 6. Owner experience (COPY-PASTE, nada editable)

Con NinjaTrader CERRADO:

```powershell
& "C:\Temp\EchoD6Bundle\INSTALL-ECHO-D6.ps1"
```

```powershell
& "C:\Temp\EchoD6Bundle\VERIFY-ECHO-D6.ps1"
```

Después: ABRIR NINJATRADER. Nada más.

Si ExecutionPolicy bloquea:

```powershell
powershell.exe -ExecutionPolicy Bypass -File "C:\Temp\EchoD6Bundle\INSTALL-ECHO-D6.ps1"
powershell.exe -ExecutionPolicy Bypass -File "C:\Temp\EchoD6Bundle\VERIFY-ECHO-D6.ps1"
```

Señal de éxito observable tras el restart (para el agente de la ventana, sin intervención owner): `EchoExecutionAddOn config loaded: ntx=****.161:9771 account=…` + `started (dual channel…)` en el log de boot de NT, ESTABLISHED del PID NT → `192.168.31.161:9771` y hello `[ntx]` autenticado en el journal del bridge ≤10 s. Con config fatal, el build d361008b ahora imprime `EchoExecutionAddOn config FAILED: …` en Error level (jamás `config loaded` silencioso).

## 7. Final handoff

```text
D6_OWNER_BUNDLE =
READY

SOURCE_SHA:
d361008bfe4aa54fe3d8b6380d290bf92e1f1c08 (origin/feature/d6-shot1-execution-vertical; worktree limpio; origin == HEAD)

BUNDLE_PATH:
C:\Temp\EchoD6Bundle

FEED_SOURCE:
v3/futures-bridge/addon-ninjatrader/EchoFeedAddOn.cs = 581a7087b1b870c78ac43e67027e5edaacf59134f4bf5f03d8b9aec9d7fd5ae4

EXEC_SOURCE:
v3/futures-bridge/addon-ninjatrader/EchoExecutionAddOn.cs = 72d97ad6c776ba56ea0d8aadfd44be2caa12ab884602c29995ffe5e75e92653f (incluye repair fail-closed LoadConfig d361008b)

FEED_SHADOW_COMPILE:
PASS — FEED_EXIT=0, 0 errores, 0 warnings (vs NinjaTrader 8.1.8.3 real, DLLs fisicas dev-win)

EXEC_SHADOW_COMPILE:
PASS — EXEC_EXIT=0, 0 errores (vs NinjaTrader 8.1.8.3 real, DLLs fisicas dev-win)

FEED_WARNINGS:
0

EXEC_WARNINGS:
3 (preexistentes Shot 1/3: CS0612 CreateOrder obsoleta @654; CS0649 marketEvents/accountEvents @52 x2; ninguno nuevo)

CONFIG:
host=192.168.31.161
port=9771
account=RJARA114411201551

CONFIG_TOKEN:
PRESENT_REDACTED (64 hex dentro del JSON; no impreso, no persistido en logs/reportes)

SOURCE_STAGE_HASH_MATCH:
PASS (repo == C:\Temp\EchoD6Bundle byte-a-byte, 3 archivos producto; SHA256SUMS.txt verificado desde la ubicacion stageada)

INSTALL_SCRIPT:
PASS (syntax OK; dry-run negativo duplicados + positivo + guard NT-corriendo con NT real + restore; sin rutas incorrectas ni variables sin definir)

VERIFY_SCRIPT:
PASS (syntax OK; read-only; positivo + tamper ntx_port->0 detectado como FAIL doble; token solo booleano)

OWNER_COMMAND_1:
& "C:\Temp\EchoD6Bundle\INSTALL-ECHO-D6.ps1"

OWNER_COMMAND_2:
& "C:\Temp\EchoD6Bundle\VERIFY-ECHO-D6.ps1"

NEXT_OWNER_ACTION:
Close NinjaTrader → run command 1 → run command 2 → open NinjaTrader.

NEXT_MANAGER_ACTION:
After NinjaTrader restart, fresh-context agent verifies: EchoExecutionAddOn config loaded with :9771 → real TCP → authenticated ntx hello → remaining C–K certification.

SAFETY:
NO physical orders (0) · NO bridge · NO ETCD mutations · NO Kafka command publishing · NO NinjaTrader Owner profile mutation (dry-runs solo en C:\Users\TEMP\sim-nt, eliminado)
```

# Echo Futures — D6 Config Parser Fix (GetNumber whitespace, owner bundle rebuild)

**Shot:** D6 — EXECUTION ADDON CONFIG PARSER REMEDIATION + OWNER BUNDLE REBUILD — TOP NinjaTrader / C# Runtime Remediation Lead (one-shot, fresh context; no Manager, no Owner, sin continuar a C→K)
**Date:** 2026-10-03 → 2026-10-04 (compile 2026-10-04T02:45Z)
**Project:** [[Echo Futures]]
**Baseline entrada:** `xKoRx/echo@d361008b` (`origin/feature/d6-shot1-execution-vertical`)
**Delta:** `xKoRx/echo@7fbd7e99` (push FF `d361008b..7fbd7e99`, 2 archivos, +61/−2)
**Verdict:** `D6_PARSER_FIX = PASS` — defecto reproducido físicamente, corregido, probado adversarialmente (estructural red/green + conductual 14/14 en runtime .NET real), shadow-compilado contra NT 8.1.8.3 físico (0 errores, 0 warnings nuevas), owner bundle RE-STAGEADO en `C:\Temp\EchoD6Bundle\` con solo `EchoExecutionAddOn.cs` cambiado.
**Safety:** `PHYSICAL_ORDERS_SENT = 0` · sin bridge · sin mutaciones ETCD · sin publishing Kafka · perfil NinjaTrader del Owner INTACTO (nada instalado por el agente; instalación = ciclo owner) · token ntx nunca embebido en el arnés (se lee del archivo en runtime) ni impreso.

---

## 1. El defecto (raíz física)

`GetNumber` en `EchoExecutionAddOn.cs` escaneaba el token numérico arrancando en `colon + 1`:

```csharp
int end = colon + 1;   // "ntx_port": 9771  -> arranca en el ESPACIO
while (end < json.Length && (char.IsDigit(json[end]) || ...)) end++;
return double.TryParse(json.Substring(colon + 1, end - colon - 1), ...) ? v : def;
```

Con whitespace JSON legal tras el dos puntos (config pretty-printed), el primer char no es dígito → el scan no avanza → `Substring` devuelve `""` → `TryParse` falla → **default**. `ntx_port` caía a `0` y el gate fail-closed de `d361008b` dejaba ambas lanes HARD-DOWN con `"config FAILED"` en Error level — sobre un JSON perfectamente válido. Cascada exacta: **la config `echo-execution-addon.json` del propio owner bundle (pretty-printed, hash `9ca3fddc`) reproducía el defecto**: el bundle stageado instalaba una config que el AddOn rechazaba. Strings (host/account/contracts) no se afectan (`ExtractJsonString` busca la comilla de apertura saltando whitespace), por eso el incidente se veía como "config aparentemente bien, lanes down".

Alcance: `EchoFeedAddOn.cs` NO tiene `GetNumber` (grep cero) — el defecto es exclusivo de `EchoExecutionAddOn.cs`.

## 2. Fix (`7fbd7e99`)

`GetNumber` ahora: (a) salta whitespace JSON (`' '`, `'\t'`, `'\r'`, `'\n'`) tras el colon; (b) escanea y parsea el token desde la posición post-whitespace (`Substring(p, end - p)`); (c) guarda `end > p` para que token vacío/no-numérico siga fail-closed al default; (d) guardas explícitas `k < 0` y `colon < 0` → default (comportamiento preservado). C# 5-compatible, mismo estilo. +7 líneas netas.

Semántica fail-closed del contrato `d361008b` intacta: port ausente → 0 (gate rechaza); valor whitespace-only → 0; port como string `"9771"` → 0 (jamás coerciona); port negativo → `-5` parseado fiel y rechazado por `ntxPort <= 0`.

## 3. Verificación adversarial

### 3.1 Estructural (paquete guardas `addon-ninjatrader`, Go)

Nueva guarda `TestExecAddOnConfigGetNumberToleratesJSONWhitespace` en `config_guard_test.go`: fija el skip explícito de los 4 whitespace JSON, el parse desde posición post-whitespace, el guard `end > p`, las guardas de key/colon ausentes y el charset numérico (dígitos/signo/fracción/exponente). Red/green físico:

| Source | Guarda nueva | Resultado |
|---|---|---|
| `d361008b` (viejo) | `TestExecAddOnConfigGetNumberToleratesJSONWhitespace` | **FAIL** (`missing "json[p] == ' '"`) — caza el defecto |
| fix (`7fbd7e99`) | ídem | **PASS** — `go test ./...` verde (paquete completo) |
| `d361008b` | guarda previa `TestExecAddOnConfigLoadFailsClosedOnInvalid` | PASS (sin falso positivo) |

### 3.2 Conductual (dev-win .132, runtime real .NET Framework 4)

Arnés generado **mecánicamente** desde el `.cs` real por extracción de marcadores (`gen_harness.py`; funciones `ExtractJsonString/GetString/GetNumber/ParseContracts` byte-verbatim, solo cambia visibilidad — sin copia manual, sin drift posible). 14 vectores adversariales, compilado y EJECUTADO con `csc.exe` Framework64 v4.0.30319 (el mismo compilador del shadow-compile):

| Arnés | Resultado |
|---|---|
| **Viejo (d361008b)** | **5/14 PASS, 9 FAIL** — `V01` (JSON del goal): `port=0`; `V02` (**la config REAL del bundle leída de `C:\Temp\EchoD6Bundle\echo-execution-addon.json` en runtime**): `port=0` con contracts/host/account correctos — firma exacta del incidente |
| **Nuevo (fix)** | **14/14 PASS, 0 FAIL** — incluye `V02` real, CRLF+tabs, espacio antes del colon, float/exponente, escapes `\"`/`\\`, contracts pretty (2 mappings) |

Vectores fail-closed idénticos en viejo y nuevo (sin regresión): V07 ausente→0, V08 ws-only→0, V10 string-typed→0.

## 4. Shadow compile real — NinjaTrader 8.1.8.3 (dev-win 192.168.31.132)

Método D6 probado: `csc.exe` .NET Framework64 v4.0.30319 `/t:library` contra DLLs físicas (`NinjaTrader.Core.dll`, `NinjaTrader.Gui.dll`, `WindowsBase.dll`).

| Target | Exit | Errores | Warnings |
|---|---|---|---|
| EchoFeedAddOn.cs (sin cambios) | 0 | 0 | 0 |
| EchoExecutionAddOn.cs (fix) | 0 | 0 | 3 preexistentes, 0 nuevas |

Warnings = exactamente las documentadas: `CS0612 Account.CreateOrder` (desplazada 654→661 por las +7 líneas del fix) y `CS0649 marketEvents/accountEvents ×2 @52`. DLLs shadow solo en staging `C:\Temp\d6parser-verify\` — **NADA instalado en NinjaTrader**.

Transporte: http.server efímero Daedalus (192.168.31.161:18999) + `curl.exe` dev-win; SHA256 verificado byte-a-byte ambos lados (fuentes + arnés + bundle); servidor apagado al cierre.

## 5. Owner bundle re-stageado — `C:\Temp\EchoD6Bundle\`

Solo cambió `EchoExecutionAddOn.cs` (+`SHA256SUMS.txt`/`BUILD-INFO.txt` regenerados; nuevos `PARSER-VERIFY.txt` y `OWNER-CHECKLIST-W2.md`). `EchoFeedAddOn.cs`, `echo-execution-addon.json`, `INSTALL-ECHO-D6.ps1` y `VERIFY-ECHO-D6.ps1` quedan byte-idénticos (los ps1 conservan sus hashes previos `635ab76a…`/`35ed7480…`).

| Archivo | Bytes | SHA256 |
|---|---|---|
| `EchoFeedAddOn.cs` | 45,803 | `581a7087…` (sin cambios, Shot 3) |
| `EchoExecutionAddOn.cs` | 47,979 | `2c8ab2cfd6b89c390f791148cf36e72213a5a761646e36f86d59357c3b7e757f` (**era `72d97ad6…`, defectuoso**) |
| `echo-execution-addon.json` | 304 | `9ca3fddc…` (sin cambios) |
| `SHA256SUMS.txt` | 266 | `98ec5a70fc88e5d74a9f17265e0eb6aec8644b6c07cff95bfa2add0df4e27bb6` |
| `BUILD-INFO.txt` | 2,977 | `094b0878a3fa178cf83121429e473a0e356346e7a66813a7a13a2721dea43f77` |
| `PARSER-VERIFY.txt` | 3,053 | `8a4fbb817b11a586d840e238355d505fd3704734e564540bb85c99f03a5ede3c` |
| `OWNER-CHECKLIST-W2.md` | 2,225 | `531010aacfc5e2ef6e9655bb1b96122dc2d4cb71970244d53c8e4f07001fb8ad` |

Verificado on-box: SHA256 del exec addon = `2c8ab2cf…`; MD5 del sums local↔box = `0a365446…`; regex del INSTALL parsea las 3 filas OK (CRLF incluido); `harness-new.exe` re-corrido post-stage contra la config re-stageada = 14/14.

## 6. Pasos Owner (copy-paste, PowerShell en dev-win)

```powershell
# 1. Cerrar NinjaTrader si está abierto (el install lo verifica)
& "C:\Temp\EchoD6Bundle\INSTALL-ECHO-D6.ps1"    # debe terminar INSTALL_ECHO_D6 = PASS
# 2. Abrir NinjaTrader (compila AddOns al arranque; 0 errores esperados)
& "C:\Temp\EchoD6Bundle\VERIFY-ECHO-D6.ps1"     # debe terminar VERIFY_ECHO_D6 = PASS
```

Log NT esperado: `EchoExecutionAddOn config loaded: ntx=192.168.31.1*9771 account=****1551 contracts=1` — **NO** `config FAILED`.

## 7. Estado y no-continuación

- Repo: `origin/feature/d6-shot1-execution-vertical` @ `7fbd7e99` (push FF). Worktree D6 Shot 1 local FF al mismo SHA.
- NO se continuó a C→K (mandato). NO se habilitó Futures Bridge, NO se tocó ETCD, NO se publicó Kafka, NO se ejecutaron órdenes, NO se instaló nada en el perfil NT del Owner.
- Pendiente owner: los 2 comandos del §6 (instalación + verify) y, tras su ciclo, verificación externa del hello en :9771 cuando el bridge corra con la sesión habilitada.
- Arnés y generador: `~/aranea/work/d6-parser-fix-20261003/harness/` (`gen_harness.py` `d017fffa…`, `ParserHarnessOld.cs` `6847985d…`, `ParserHarnessNew.cs` `1bf679dd…`); staging físico en dev-win `C:\Temp\d6parser-verify\` (harness-old/new.exe + DLLs shadow).

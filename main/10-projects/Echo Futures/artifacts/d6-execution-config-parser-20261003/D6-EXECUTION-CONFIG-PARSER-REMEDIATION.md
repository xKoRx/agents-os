# Echo Futures — D6 Execution Config Parser Remediation (GetNumber whitespace → owner bundle rebuild)

**Shot:** D6 — EXECUTION ADDON CONFIG PARSER REMEDIATION + OWNER BUNDLE REBUILD — TOP NinjaTrader / C# Runtime Remediation Lead (one-shot; no Manager, no Owner, sin continuar a certificación física C→K)
**Date:** 2026-10-03 → 2026-10-04 (shadow-compile 2026-10-04T02:45Z; dry-runs 2026-10-04T03:3xZ)
**Project:** [[Echo Futures]]
**Baseline:** `xKoRx/echo@d361008bfe4aa54fe3d8b6380d290bf92e1f1c08` (`origin/feature/d6-shot1-execution-vertical`, worktree limpio verificado al inicio)
**FINAL_SHA:** `ffa493d8d179c9f9374d0a935e7916be15367ce8` — push FF `d361008b..7fbd7e99` (fix+guarda) y `7fbd7e99..ffa493d8` (harness de regresión); sin rewrite de historia.
**Verdict:** `D6_EXECUTION_CONFIG_PARSER_REMEDIATION = PASS`
**Safety:** `PHYSICAL_ORDERS_SENT = 0` · sin Futures Bridge · sin mutaciones ETCD · sin publishing Kafka · sin LIVE run · perfil NinjaTrader del Owner INTACTO (agente NO instaló nada; instalación = ciclo owner con los 2 comandos) · token ntx jamás embebido en el arnés ni impreso (se lee del archivo en runtime).

---

## 1. Reproducción física (evidencia Owner, aceptada como input)

- JSON instalado verificado por el Owner ANTES de minificar: source SHA256 = destino SHA256 = `9CA3FDDC…EEEA71B` (copia byte-idéntica), con exactamente UN `echo-execution-addon.json` bajo el perfil NinjaTrader, semántica correcta (`ntx_host=192.168.31.161`, `ntx_port=9771`, `account_name=RJARA114411201551`, `account_id=3`, `token_length=64`).
- A pesar de eso, el runtime logueó: `EchoExecutionAddOn config loaded: ntx=****.161:0 …` — puerto 0 con config válida.
- El workaround del Owner (`ConvertTo-Json -Compress`) NO cambió el parseo (siguió en 0): evidencia diagnóstica de que el problema era el parser, no el formato.

## 2. Root cause — CONFIRMADO (YES)

Inspección del `GetNumber()` real @ `d361008b` ANTES de modificar código (mandato /root_cause_confirmation):

```csharp
int colon = json.IndexOf(':', k + needle.Length);
int end = colon + 1;                       // arranca EN el whitespace post-colon
while (end < json.Length && (char.IsDigit(json[end]) || json[end] == '-' || ...)) end++;
return double.TryParse(json.Substring(colon + 1, end - colon - 1), ...) ? v : def;
```

Sin skip de whitespace: con `"ntx_port": 9771` el primer char escaneado es el espacio → el token sale vacío → `TryParse("")` falla → default `0`. El branch de éxito de `LoadConfig` imprimía `config loaded … :0` porque 0 llega como default-parsed, no como error fatal — exactamente el log físico del Owner. La validación de `d361008b` ya cubría port<=0 para NUEVAS cargas fail-closed, pero el print de este incidente precede a ese repair instalado (el binario instalado era el previo); en cualquier caso la causa raíz es una sola: **`GetNumber` sin skip de whitespace JSON**.

**Comparación con el parser físicamente funcional** (`EchoFeedAddOn`, misma config pretty, feed lane viva en N1): el FeedAddOn usa un tokenizer real con `SkipWs(s, ref pos)` alrededor de CADA token (llamadas 218/220/225/227/229/237, def @247) más `ParseJsonLiteral` que corta en whitespace — el whitespace post-colon se salta por construcción. El ExecutionAddOn usa needle-scan y `GetNumber` era el único lugar sin skip. Diagnóstico sin contradicciones → proceder.

## 3. Fix (F1, mínimo) — `7fbd7e99`

`GetNumber` (única función tocada, +7 líneas netas, C# 5-compatible):

1. guardas explícitas `k < 0` / `colon < 0` → default (comportamiento preservado);
2. skip de whitespace JSON (`' '`, `'\t'`, `'\r'`, `'\n'`) tras el colon;
3. scan del token numérico desde la posición post-whitespace con el charset original (dígitos, signo, decimal, exponente);
4. `end > p &&` para que token vacío/no-numérico siga fail-closed al default;
5. `double.TryParse(Substring(p, end-p), NumberStyles.Float, CultureInfo.InvariantCulture)` — parsing invariant culture preservado.

NO se reemplazó el parser completo, NO se agregó Newtonsoft ni librería de config (KISS). F2: `LoadConfig` / gate fail-closed de `d361008b` INTACTO (misma rama de validación, mismo reset de dials, mismo log `config FAILED` en Error level; la guarda Go previa sigue en verde sobre el fix — sin regresión).

## 4. Tests exactos (F3)

### 4.1 Estructural (Go, `config_guard_test.go`)

`TestExecAddOnConfigGetNumberToleratesJSONWhitespace` — fija skip de los 4 whitespace JSON, parse post-whitespace, guard `end > p`, guardas key/colon ausentes, charset numérico. Red/green físico: **red @ d361008b** (`missing "json[p] == ' '"`), **green @ fix** (`go test ./...` paquete verde), guarda previa `TestExecAddOnConfigLoadFailsClosedOnInvalid` sin falso positivo (PASS en ambos). La guarda Go NO es la única evidencia: 4.2 es la conductual.

### 4.2 Conductual (parser-harness @ `ffa493d8`, .NET Framework REAL)

Arnés generado MECÁNICAMENTE desde el `.cs` real (extracción por marcadores de `GetNumber/ExtractJsonString/GetString/ParseContracts`; solo visibilidad; generador `parser-harness/gen_harness.py` en el repo, README con procedimiento y matriz). Compilado y ejecutado con `csc.exe` Framework64 v4.0.30319 en dev-win .132 (mismo compilador del shadow-compile). Matriz de 17 vectores:

| # | Forma | Requerido | Viejo d361008b | Fix |
|---|---|---|---|---|
| V01 | pretty multi-línea `"ntx_port": 9771` | 9771 | FAIL (0) | PASS |
| V02 | config REAL del bundle leída de `C:\Temp\EchoD6Bundle` | 9771 | **FAIL (0)** | **PASS** |
| V03 | compact `"ntx_port":9771` | 9771 | PASS | PASS |
| V04 | CRLF + tabs | 9771 | FAIL (0) | PASS |
| V05 | espacio ANTES del colon | 9771 | FAIL (0) | PASS |
| V06 | espacios tras el valor (`9771  ,`) | 9771 | FAIL (0) | PASS |
| V07 | port ausente | 0 fail-closed | PASS | PASS |
| V08 | valor whitespace-only | 0 fail-closed | PASS | PASS |
| V09 | port negativo (-5) | -5 (gate `<=0` rechaza) | FAIL (0) | PASS |
| V10 | port tipo string `"9771"` | 0 fail-closed (jamás coerciona) | PASS | PASS |
| V11 | escapes `\"` `\\` en account_name | decodificado verbatim | PASS | PASS |
| V12 | contracts pretty (2 mappings) | 2 | FAIL (port) | PASS |
| V13/14 | float/exponente (`5.0`, `5e0`) pretty/compact | 5 | V13 FAIL / V14 PASS | PASS |
| V15 | `"ntx_port":     9771` (multi-espacio, mandato) | 9771 | FAIL (0) | PASS |
| V16 | newline+indent entre colon y valor (mandato) | 9771 | FAIL (0) | PASS |
| V17 | `"ntx_port": 0` (mandato) | 0 fail-closed | PASS | PASS |

**Resultado certificado:** viejo **6/17 PASS** con `EXECUTION_ADDON_PARSED_PORT=0` (réplica exacta del log físico del owner `ntx=****.161:0` sobre los MISMOS bytes de config); fix **17/17 PASS** con **`EXECUTION_ADDON_PARSED_PORT=9771`** (F7: el parser reparado corriendo él mismo contra la config canónica pretty — NO inferido de `ConvertFrom-Json`). Exit code 0 solo con los 17 en verde.

## 5. F4 — pretty JSON sigue siendo el contrato

`echo-execution-addon.json` canónico queda en forma pretty legible (hash sin cambios `9ca3fddc…`). La minificación del Owner fue SOLO evidencia diagnóstica; el fix hace que la forma canónica parseé idéntico a la compacta. Nada del producto exige JSON minificado.

## 6. Shadow compile real (F5) — NinjaTrader 8.1.8.3, dev-win 192.168.31.132

`csc.exe` .NET Framework64 v4.0.30319, `/t:library`, contra DLLs físicas (`NinjaTrader.Core.dll`, `NinjaTrader.Gui.dll`, `WindowsBase.dll`):

| Target | Errores | Warnings |
|---|---|---|
| EchoFeedAddOn.cs (sin cambios) | **0** | 0 |
| EchoExecutionAddOn.cs (fix) | **0** | 3 preexistentes, 0 nuevas: `CS0612 Account.CreateOrder` (654→661 por +7 líneas del fix), `CS0649 marketEvents/accountEvents ×2 @52` |

DLLs shadow solo en staging `C:\Temp\d6parser-verify\` — NADA instalado en NinjaTrader.

## 7. Owner bundle final (F6/F8/F9) — `C:\Temp\EchoD6Bundle\`

Re-stageado desde HEAD actual (`ffa493d8`; el `.cs` es byte-idéntico: `git show HEAD:…` = `2c8ab2cf…` = staged on-box). EXACTAMENTE los 7 archivos mandados:

| Archivo | Bytes | SHA256 |
|---|---|---|
| `EchoFeedAddOn.cs` | 45,803 | `581a7087b1b870c78ac43e67027e5edaacf59134f4bf5f03d8b9aec9d7fd5ae4` |
| `EchoExecutionAddOn.cs` | 47,979 | `2c8ab2cfd6b89c390f791148cf36e72213a5a761646e36f86d59357c3b7e757f` (era `72d97ad6…` defectuoso) |
| `echo-execution-addon.json` | 304 | `9ca3fddc31330b2d5b485fd0869801b486b1443972bbf5ba50c56862feeea71b` (sin cambios) |
| `INSTALL-ECHO-D6.ps1` | 5,613 | `635ab76a7785b9862d053f2d51e0e142c27d32743f7e068ae608245af03a9af8` (sin cambios, reutilizado) |
| `VERIFY-ECHO-D6.ps1` | 4,125 | `8382e4574946fa352395ffcc71ef0e9f47eacfc2b942e030b83d23a2e294cbce` (actualizado: exige `auth_token` largo 64) |
| `SHA256SUMS.txt` | 266 | `98ec5a70fc88e5d74a9f17265e0eb6aec8644b6c07cff95bfa2add0df4e27bb6` |
| `BUILD-INFO.txt` | 3,619 | `58cd1c8810630f0cc87cd16dbcf72ae82546443aeb39bb07dff2933a68a4f927` |

Hashes on-box verificados con `certutil` == repo HEAD (SOURCE_STAGE_HASH_MATCH = PASS). F7 validación sin imprimir token: host/port/account/`token_len=64` (línea `config: … auth_token present=True len=64` del VERIFY contra la config real `9ca3fddc`) + `EXECUTION_ADDON_PARSED_PORT=9771`.

**Dry-runs en sandbox** (`C:\Temp\d6verify-dryrun`, parámetro `-NtRoot`, perfil Owner intocado; sandbox con token DUMMY de 64 — el token real jamás salió del bundle):
- `VERIFY-ECHO-D6.ps1 -NtRoot sandbox` sobre instalación limpia → **`VERIFY_ECHO_D6 = PASS`** (SHA ×3 OK, 1 clase por AddOn, config semántica OK, len=64).
- **Tamper `ntx_port=0`** → **`VERIFY_ECHO_D6 = FAIL`** con `VERIFY: FAIL: ntx_port inesperado: 0 (se requiere 9771)` (exit 1).
- `INSTALL-ECHO-D6.ps1 -NtRoot sandbox -AllowNtRunning` → **`INSTALL_ECHO_D6 = PASS`** (restaura el tamper, SHA256 bundle↔destino ×3 OK, config OK port 9771, 1 declaración por clase).

## 8. Owner handoff (F10 — COPY-PASTE)

**STEP 1 — NinjaTrader closed**

```text
powershell.exe -ExecutionPolicy Bypass -File "C:\Temp\EchoD6Bundle\INSTALL-ECHO-D6.ps1"
```

**STEP 2**

```text
powershell.exe -ExecutionPolicy Bypass -File "C:\Temp\EchoD6Bundle\VERIFY-ECHO-D6.ps1"
```

**STEP 3** — Open NinjaTrader.

Sin edición manual de JSON. Sin copia manual de archivos. Log NT esperado tras STEP 3: `EchoExecutionAddOn config loaded: ntx=****.161:9771 account=****1551 contracts=1` y **NUNCA** `config FAILED`.

## 9. Commits

| SHA | Contenido |
|---|---|
| `7fbd7e99` | fix GetNumber whitespace + guarda estructural Go (push FF `d361008b..7fbd7e99`) |
| `ffa493d8` | `parser-harness/` (generador + README con matriz y procedimiento) (push FF `7fbd7e99..ffa493d8`) |

`origin/feature/d6-shot1-execution-vertical` = `ffa493d8` = HEAD local; worktree D6 Shot 1 FF al mismo SHA; historia intacta.

## 10. No-continuación y siguiente

NO se ejecutó certificación física C→K (mandato). Siguiente paso físico = ciclo Owner (STEP 1→2→3) y, tras restart, certificación fresh-context que primero debe probar en el runtime log `EchoExecutionAddOn config loaded … :9771`, luego TCP real :9771 + hello ntx autenticado, y recién ahí retomar C→K.

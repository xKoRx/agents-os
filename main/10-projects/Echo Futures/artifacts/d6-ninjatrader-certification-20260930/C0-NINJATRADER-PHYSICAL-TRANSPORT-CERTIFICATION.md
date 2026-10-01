# Echo Futures — D6 C0 NinjaTrader / Tradovate Physical Transport Certification

**Shot:** D6 C0 — Physical transport certification (no orders)
**Role:** TOP Physical Execution Transport Certifier
**Date:** 2026-09-30 (evidencia UTC cruzando 2026-10-01T02:0xZ, timestamps explícitos por test)
**Project:** [[Echo Futures]]
**Echo frozen baseline:** `xKoRx/echo@13e087a3bb762f65b060d3b3200fb00a67c6ff1d`
**D6 program:** GAU50 (5 evaluaciones compradas + 5 resets, ≤10 intentos)
**Transport target:** `NINJATRADER_TRADOVATE`
**Prior artifact:** `main/10-projects/Echo Futures/artifacts/d6-earn2trade-preflight-20260930/EARN2TRADE-FIRST-PARTY-PREFLIGHT-RESEARCH.md` (BLOCKED_PENDING_PROVIDER_CONFIRMATION; no se reabre entitlement/policy)
**Verdict:** `D6_C0_NINJATRADER = BLOCKED` — bloqueo físico concreto y accionable: los observables de cuenta/GUI/market data/log viven en la sesión interactiva del owner en la máquina Windows y no son observables por la identidad de automatización. El transporte de red sí quedó certificado físico. Resolución estimada: checklist GUI del owner (~5 min) + opcional grant de lectura ACL.

## 1. Hard safety

No se colocó, modificó ni canceló orden alguna. `ORDERS_SENT = 0`. No se instaló NinjaScript, no se tocó Strategy/GerardMM/ProviderRuleSet/Bridge/ExecutionAdapter ni ningún contrato D5. Ninguna credencial Tradovate fue leída, pedida ni persistida (permanecen en la sesión interactiva del owner, fuera del alcance de la identidad de automatización).

## 2. Entorno y acceso usado

- Target físico: **`dev-win` = `192.168.31.132`** (designado Windows del track Echo en el Environment Contract §2; el owner lo señaló como "win-dev"). Acceso exclusivamente por el plano MCP certificado `aranea-ssh` → perfiles `dev-win` (viewer RO) y `dev-win-operator` (operator no-admin), identidad remota `dev-win\echo-dev`. Verified vivo hoy: `/status` del plano lista ambos perfiles apuntando a `echo-dev@192.168.31.132`; `read-command whoami` (viewer) y `run-command whoami` (operator) devolvieron `dev-win\echo-dev`.
- Sistema operativo observado: `Microsoft Windows [Version 10.0.26100.5074]` (familia 26100 — Windows 11 24H2 / Server 2025), vía `cmd /c ver`.
- La sesión MCP del plano estaba con pool agotado (firma documentada 503 + `/status 200 connections:[]`); se aplicó el recovery del runbook `aranea-ssh-mcp` (config 600 sin drift → `docker restart ssh-mcp` vía management path `mcps-ops` → initialize 200 + sid + notification 202). Contenedor `local/ssh-mcp:2.8.0-d2d7696-h2fix` intacto, mismo binary que la certificación previa.
- Límites reales de la identidad `dev-win\echo-dev` (demostrados, no asumidos): sin admin; CIM denegado (`Get-CimInstance`/`Get-DnsClientCache` → Access denied); `tasklist /v` de proceso de otra sesión → Access denied; `C:\Users\KoR\Documents` → Access denied; comandos fuera de clase safe en operator → `APPROVAL_UNAVAILABLE` (elicitation no soportada por cliente HTTP; fail-closed correcto). Es la misma frontera ya certificada para `mt5-kronos`; no se amplió ninguna policy.

## 3. Registro de evidencia física

| # | Evidencia | Método (nivel) | Timestamp UTC |
|---|---|---|---|
| E1 | `C:\Program Files\NinjaTrader 8` existe; subcarpetas `bin`, `db`, `workspaces`, `templates` con LastWriteTime 2026-09-30 22:24 local (instalación de hoy) | `Get-ChildItem` por MCP operator (físico) | 2026-10-01T02:0xZ |
| E2 | `bin\NinjaTrader.exe` FileVersion/ProductVersion **8.1.8.3**, FileDescription NinjaTrader; binarios 2026-09-29 04:31 | `.VersionInfo` (físico, recurso de versión) | 2026-10-01T02:0xZ |
| E3 | Proceso **NinjaTrader corriendo**: PID 3464, sesión interactiva SI=2, WS ≈ 662 MB | `Get-Process` (físico) | 2026-10-01T02:0xZ |
| E4 | 6 conexiones TCP ESTABLISHED desde PID 3464, incluidas **2× → `34.117.68.229:443` = `demo.tradovateapi.com`** (match por DNS forward con resolver independiente), **1× → `3.133.196.229:31655`** (gateway AWS us-east-2, puerto de market data de Tradovate), 1× → `ninjatrader.com` (Cloudflare), 1× → `34.8.154.29:443` (GCP), 1× → `3.33.235.18:443` (AWS Global Accelerator) | `netstat -ano` + DNS cruzado (físico de red) | 2026-10-01T01:5xZ |
| E5 | Estabilidad: mismas conexiones Tradovate (mismos puertos origen 49960/53464/63089/63260) persistentes en muestreo repetido; poller cada 20 s corriendo (`nt-conn-poll.log` en workspace externo) | `netstat` repetido (físico) | 2026-10-01T02:11–02:12Z+ |
| E6 | Caché DNS de la máquina con `license.ninjatrader.com` y `apiproxy.ninjatrader.com` resueltos recientemente | `ipconfig /displaydns` (físico) | 2026-10-01T02:0xZ |
| E7 | `bin\Custom` contiene sólo `Backup`/`Snippet` (instalación limpia, sin NinjaScript de usuario) | `Get-ChildItem` (físico) | 2026-10-01T02:0xZ |
| E8 | `db\NinjaTrader.sqlite` (3.3 MB, 2026-09-29 04:25): búsqueda binaria con `Select-String -Quiet` → `NQ`/`ES`/`instrument` True, `Globex`/`NQZ6` False (evidencia débil de metadata de instrumentos; contratos de mes se generan dinámicamente — no concluyente) | lectura remota (físico débil) | 2026-10-01T02:0xZ |
| E9 | `C:\Users\KoR\Documents` Access denied para `echo-dev`; perfil `C:\Users\echo-dev` contiene sólo `.ssh`; `C:\Users\Public\Documents` inexistente/vacío ⇒ **user data de NinjaTrader (config de conexiones, logs, trace) vive en el perfil interactivo del owner y no es legible por la identidad de automatización** | `Get-ChildItem` + errores ACL (físico negativo) | 2026-10-01T02:0xZ |
| E10 | Listeners locales de NT `0.0.0.0:4530` y `0.0.0.0:36973`, protocolo binario no-HTTP (verificado probe) | `netstat` + probe (físico) | 2026-10-01T02:0xZ |

Contexto de mercado al momento de la medición: martes 2026-09-30 ≈ 22:00 ET (UTC-4), CME Globex abierto (ventana diaria 17:00–18:00 ET ya pasada) ⇒ las pruebas dependientes de mercado abierto SÍ estaban en condiciones de ejecutarse; el límite fue de acceso, no temporal.

## 4. Matriz de certificación (/verify)

Clasificación por punto del /execute, distinguiendo nivel: **[F]** observado físicamente por este shot, **[C]** documentación/configuración, **[I]** inferencia explícita.

| # | Prueba | Resultado | Nivel y fundamento |
|---|---|---|---|
| 1 | NinjaTrader Desktop instalado y versión | **PASS** | [F] E1+E2: NT 8.1.8.3 instalado hoy en dev-win. |
| 2 | Login exitoso por la ruta Tradovate de Earn2Trade | **PASS (nivel transporte; confirmación GUI pendiente)** | [F] E4+E5: conexiones establecidas y persistentes a `demo.tradovateapi.com` + gateway :31655 + endpoints de licencia NT. [I] La persistencia ≥15 min de la dupla API+MD con mercado abierto es consistente con sesión autenticada viva; un login fallido no retendría el par de conexiones en reposo. La autenticación explícita (estado "Connected" verde en Control Center) queda pendiente de confirmación GUI del owner. |
| 3 | Conexión en modo correcto para Evaluation (simulated) | **PASS (nivel entorno; indicador GUI pendiente)** | [F] El endpoint con conexiones vivas es `demo.tradovateapi.com` (entorno demo de Tradovate). [C] Earn2Trade documenta Evaluation como cuenta simulada vía la ruta Tradovate/NinjaTrader. La unión de ambos (cuenta simulada visible en GUI) es la parte pendiente. |
| 4 | Al menos una GAU50 visible | **BLOCKED** | El listado de cuentas es observable sólo dentro de la app en la sesión interactiva (SI=2) del owner; la identidad de automatización no puede leer ese estado (E9, CIM denegado, cross-session denegado). No se inventa resultado. |
| 5 | Balance/account state observable | **BLOCKED** | Misma causa que #4. |
| 6 | NQ disponible | **BLOCKED** | NQ como instrumento en GUI/lista no observable. Evidencia parcial [F débil] E8 y gateway MD conectado (E4); no se promueve a visible. |
| 7 | Market data de NQ observable (mercado abierto) | **BLOCKED** | Mercado abierto comprobado; gateway MD establecido (E4), pero el flujo de ticks/last-price es observable sólo en GUI (chart/DOM). Clasificado BLOCKED por acceso, no NOT_TESTABLE_NOW (la condición temporal sí se cumplía). |
| 8 | Posiciones actuales observables | **BLOCKED** | Misma causa que #4. |
| 9 | Órdenes actuales observables | **BLOCKED** | Misma causa que #4. |
| 10 | Disconnect/reconnect controlado | **NOT_TESTABLE_NOW** | Requiere operación GUI del owner (menú Conexiones). El certificador no mata ni reinicia la app del owner: hacerlo sin poder restaurarla visible dejaría la sesión 2 rota. Poller físico armado (E5) para capturar el corte/reestablecimiento con timestamps cuando el owner lo ejecute. |
| 11 | Restart de NinjaTrader y recuperación | **NOT_TESTABLE_NOW** | Misma causa que #10. |
| 12 | Ubicación y utilidad de logs | **BLOCKED (acceso); ubicación documentada** | [C] Por convención del producto los logs/trace viven en `Documents\NinjaTrader 8\log|trace` del usuario que ejecuta la app (KoR). [F] E9 demuestra que esa ruta está denegada por ACL para `echo-dev`. Bloqueo material para una futura certificación del adapter con la identidad actual. |

Separación exigida por /verify: una conexión configurada y establecida NO fue promovida a market data ni a account observability (ítems 4–9); el login PASS es de nivel transporte con su inferencia declarada, no una captura de GUI.

## 5. Reuse compliance

No se repitió research público de Earn2Trade ni de otros props; no se reabrió comparación GAU/TCP ni entitlement/policy del preflight (se conserva su `BLOCKED_PENDING_PROVIDER_CONFIRMATION` intacto). Este shot aportó únicamente evidencia física nueva de la máquina.

## 6. C1 inputs (observaciones para el Primary Manager — no diseño, no implementación)

- **Versión:** NinjaTrader Desktop 8.1.8.3 sobre Windows build 26100, 64-bit, en VM `dev-win` (.132) con RDP/SSH/SMB expuestos en LAN. La 8.1.x es la línea vigente soportada para NinjaScript.
- **Topología de red observada de la conexión Tradovate:** API en `demo.tradovateapi.com:443` (GCP, 2 conexiones concurrentes), gateway de market data en AWS us-east-2 puerto **31655**, servicios de licencia/proxy en `license.ninjatrader.com` / `apiproxy.ninjatrader.com` / `ninjatrader.com:443` (Cloudflare). Esta huella es el patrón que un futuro smoke del adapter puede usar como negativo/positivo de conexión.
- **Superficie local:** NT abre listeners LAN-visibles `0.0.0.0:4530` y `0.0.0.0:36973` (protocolo binario interno, no HTTP) — inventario de hardening futuro si dev-win comparte LAN con infra productiva.
- **Límites de la identidad de automatización en dev-win:** `dev-win\echo-dev` es no-admin, CIM denegado, sin lectura del perfil interactivo (KoR) y sin interacción con la sesión GUI. Para certificar un adapter (logs, trace, eventos de orden) hay tres caminos posibles a evaluar en C1: (a) ejecutar NT bajo la identidad de servicio/echo-dev, (b) grant ACL de lectura del folder `Documents\NinjaTrader 8` hacia `echo-dev`, o (c) patrón publisher de evidencia (equivalente `AraneaEvidencePublish` de worker-kronos). Decisión pendiente del manager/owner; este shot no la toma.
- **Clean slate NinjaScript:** `bin\Custom` sin scripts de usuario en la instalación global (nota: el compilador de usuario de NT8 trabaja sobre el `Documents\...\bin\Custom` del perfil interactivo, hoy ilegible para automatización — ver punto anterior).
- **Soporte remoto disponible en la máquina:** `TeamViewerQS_en.exe` dentro de `bin` (canal owner, no usado en este shot).
- **Comportamiento de red observado en reposo:** las conexiones a `ninjatrader.com:443` rotan puerto origen periódicamente (long-poll/salud), mientras las 4 conexiones Tradovate (2× demo API + 1× MD :31655 + 1× accelerator) permanecen idénticas — base empírica para distinguir liveness de app vs sesión de trading en futuros monitores.
- **Contenido no verificado en este shot:** whether NT tiene habilitado auto-connect al arrancar (se demostrará con el restart del owner), credenciales/entitlement Tradovate direct API (fuera de scope por /frozen), y cualquier estado de cuenta real (pendiente GUI).

## 7. Blockers

1. **B1 (principal): observables de cuenta/GUI/market data/log inaccesibles para la identidad de automatización.** La app corre en la sesión interactiva del owner (SI=2) y el user data de NT está bajo `C:\Users\KoR` (ACL denegada para `echo-dev`, demostrado). Resolución: checklist GUI del owner (~5 min) para ítems 2/3/4/5/6/7/8/9 y, para el camino de automatización, elegir a/b/c en §6. No es un fallo del transporte: la máquina, la app y la conexión están operativas.
2. **B2: pruebas de discontinuidad (reconnect/restart) no ejecutables por el agente** sin un operador GUI; quedan armadas con poller físico para capturarse en el momento en que el owner las ejecute.

## 8. Acción mínima del owner para cerrar C0 (checklist GUI, ~5 min)

1. En NinjaTrader de dev-win: confirmar conexión **Tradovate** en verde/"Connected" (Control Center, abajo-izquierda) y el indicador de cuenta **Simulated**.
2. Pestaña **Accounts**: verificar que aparece la cuenta de la evaluación GAU50 con su balance (reportar últimos 4 dígitos o nickname, nunca el ID completo).
3. Abrir chart o SuperDOM de **NQ 12-26** (front actual) y confirmar last price actualizándose (mercado abierto).
4. Pestañas **Positions** y **Orders**: confirmar vacías.
5. (Opcional, cierra ítems 10–11): menú Conexiones → disconnect/reconnect Tradovate; luego cerrar y reabrir NinjaTrader. El poller físico captura los timestamps de corte/reestablecimiento por sí solo.
6. (Opcional, cierra B1-camino-automatización): otorgar a `dev-win\echo-dev` lectura del folder `Documents\NinjaTrader 8` del perfil KoR, o indicar el camino preferido (a/b/c de §6).

## 9. Handoff

```text
D6_C0_NINJATRADER = BLOCKED

ARTIFACT:
main/10-projects/Echo Futures/artifacts/d6-ninjatrader-certification-20260930/C0-NINJATRADER-PHYSICAL-TRANSPORT-CERTIFICATION.md

AGENTS_OS_SHA:
e518a3150a2919053d7210c70562da14d8b2b5ea

NINJATRADER_VERSION:
8.1.8.3 (Windows build 26100.5074, dev-win 192.168.31.132)

CONNECTION:
PASS

EVALUATION_ACCOUNT_VISIBLE:
BLOCKED

GAU50_VISIBLE:
BLOCKED

NQ_VISIBLE:
BLOCKED

MARKET_DATA:
BLOCKED

ACCOUNT_STATE:
BLOCKED

ORDERS_OBSERVABLE:
BLOCKED

POSITIONS_OBSERVABLE:
BLOCKED

RECONNECT:
NOT_TESTABLE_NOW

RESTART_RECOVERY:
NOT_TESTABLE_NOW

ORDERS_SENT:
0

BLOCKERS:
B1: observables de cuenta/GUI/market data/log viven en la sesión interactiva del owner (SI=2) y el user data NT bajo C:\Users\KoR es ACL-denegado para dev-win\echo-dev (demostrado); resolver con checklist GUI del owner + elección de camino de evidencia (§6 a/b/c). B2: reconnect/restart requieren operación GUI del owner; poller físico armado para capturarlos.

C1_INPUTS:
NT 8.1.8.3 línea vigente NinjaScript; huella de red Tradovate demo (2× demo.tradovateapi.com:443 + MD gateway AWS :31655 + license/apiproxy ninjatrader.com) usable como patrón de smoke; listeners locales 0.0.0.0:4530/36973 (hardening futuro); identidad echo-dev no-admin con CIM denegado y sin lectura del perfil interactivo ⇒ certificación de adapter requiere resolver acceso a evidencia (NT como echo-dev | ACL lectura | publisher de evidencia estilo worker-kronos); bin\Custom limpio; auto-connect y credenciales sin verificar (fuera de scope).

NEXT_MANAGER_ACTION:
Ejecutar la checklist GUI del owner (§8) con este shot o uno nuevo; con ella se re-clasifican los ítems 2–9 (y 10–11 si ejecuta reconnect/restart) y se decide si C0 emite PASS físico completo. En paralelo, el manager decide el camino de evidencia para la certificación del adapter (§6). NO emitir EF_D6_E2E_PASS desde este shot; no implementar adapter ni NinjaScript.
```

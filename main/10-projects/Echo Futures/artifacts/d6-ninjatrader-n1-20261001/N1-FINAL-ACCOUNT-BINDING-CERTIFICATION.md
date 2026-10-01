# Echo Futures — D6 N1 — Final Account Binding Certification

**Fecha:** 2026-10-01 (fase blocked: evidencia 20:35–20:50Z / local -03; fase final tras ciclo owner: evidencia 21:15–21:27Z)
**Role:** TOP Physical Integration Certifier / N1 Finalization Worker (no Manager, no Owner, no arquitecto)
**Base:** [[N1-PHYSICAL-READONLY-CERTIFICATION]] (PARTIAL_BLOCKED_OWNER, OD-2 pendiente) + [[N1-R3-NINJATRADER-PHYSICAL-COMPILE-REPAIR]] + [[N1-R2-CORRECT-EARN2TRADE-ENTITLEMENT]] + [[N1-R1-REMOVE-UNAUTHORIZED-OWNER-RISK-MODEL]] + [[N1-SHOT1-READONLY-VERTICAL]]
**Owner decision ejecutada (OD-2, final para N1):** `E2T-GAU50-01` → NinjaTrader account `Name = RJARA114411201551`
**Echo branch:** `origin/feature/d6-n1-readonly-vertical` @ `f0c82905d4eaf825c08e04f0bb97cab73e616ba5` (verificado al iniciar ambas fases; worktree limpio antes y después; sin commits en esta certificación)
**Veredicto final:** `D6_N1_FINAL_ACCOUNT_BINDING = PASS` y **`D6_N1 = PASS`** — el owner ejecutó el ciclo stageado (instaló el config final y reinició NinjaTrader); la sesión AddOn nueva `2f6a4d5375714a13b237f5ab65ba1fd6` (21:16:11Z, PID 1876) resuelve `RJARA114411201551` → `Id "3"` con `match=RESOLVED`, `binding_loaded=true`, `binding_error=""`, `binding_match=RESOLVED`, observaciones de cuenta completas (balances reales $50,000 NLV, positions/orders EMPTY_OBSERVED, executions NOT_OBSERVED) y market lane PASS con QUOTE/TRADE físicos en el ingress canónico. Id estable entre restarts (2/2 sesiones hoy). `ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0`. Fases anteriores (§1–§8) se preservan como historia; el estado final vive en §9–§15. N2 sigue NOT AUTHORIZED; no se emite `EF_D6_E2E_PASS`.

## 0. Hard safety

`ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0`, estructural y observado: grep `\.Submit(|\.Change(|\.Cancel(|\.Flatten(|\.CreateOrder(` sobre `EchoFeedAddOn.cs` @ `f0c82905` = **0 matches** (re-verificado al cierre de esta certificación; la única mención es el comentario negativo línea 18); el protocolo `echo.ntfeed.v1` mantiene exactamente 8 familias de observación sin familia de comandos; el relay nunca escribe al AddOn (única escritura: evidence file local 0600); el execution bridge sigue sin arrancar; los heartbeats reales del AddOn reportan `order_events: 0` durante toda la sesión incluida la ventana de esta certificación. No se generó orden alguna para fabricar evidencia. Únicas mutaciones de esta certificación: 1 clave ETCD DEV (provider-external-account-id, dentro del binding E2T-GAU50-01) + restart controlado de `echo-nt-feed-relay` (unidad systemd --user propia de este vertical, release intacta). Master intocado, PROD intocado.

## 1. Rediscovery del account seleccionado (sesión real viva)

Método: frames de discovery full-fidelity del AddOn real en el evidence sink del relay (`/home/kor/opt/echo-dev/var/nt-feed/evidence.jsonl`, 0600), NO el valor histórico del artefacto previo.

- Sesión AddOn real vigente: `6e6eb8b665b4422495826c6f9c97e364` (la misma de la certificación física; sin restart de NT: PID 984 sesión SI=2 y TCP ESTABLISHED `192.168.31.132:65181 → 192.168.31.161:9770` propiedad de NinjaTrader.exe verificados por netstat dev-win 20:36Z).
- Frame account más reciente al momento del rediscovery: `ts_utc 2026-10-01T20:39:48.574Z`, seq 81992, `match: DISCOVERY_ONLY`.
- `RJARA114411201551`: **exactly 1 cuenta** con ese Name entre las 8 descubiertas (5 GAU50 + Backtest/Playback101/Sim101).
- **Current NinjaTrader `Account.Id` = `"3"`** — confirmado independientemente por la sesión actual viva (no reutilizado por supuesto desde el artefacto previo).

## 2. Binding ETCD DEV (paso 3 del mandato)

- Estado pre: `/echo/development/futures-bridge/accounts/E2T-GAU50-01/` con 10 keys; `provider-external-account-id` **ausente** (estado N1 declarado; read plano MCP ETCD RO `found=false`).
- Escritura con herramienta efímera SDK (patrón N1-R2: `etcd.New(WithApp("echo"), WithEnv("development"))` = namespace idéntico al del relay; guardas: pre-lectura exige ABSENT con abort ante cualquier otro valor, `SetVar`, read-back exige valor exacto). Salida: `before: ABSENT → after: "3" → WRITE_VERIFIED`. Herramienta y binario eliminados del worktree inmediatamente (nunca commiteados; `git status` = 0 entradas después).
- Post: conteo del prefijo = **11 keys** (10 → 11, exactamente la clave nueva; cero hermanas creadas o eliminadas); `entitlement=ALLOWED`, `enabled=true`, `provider-id=EARN2TRADE`, `nt-feed/active-account=E2T-GAU50-01` verificados intactos; read-back doble (writer + MCP ETCD RO: `value "3", size 1`).
- Clave: `futures-bridge/accounts/E2T-GAU50-01/provider-external-account-id` (hermana del prefijo `binding/`, schema existente D5/N1; **sin** schema nuevo).

## 3. Relay: binding cargado + defence-in-depth (pasos 5 y 7)

`systemctl --user restart echo-nt-feed-relay` a las 20:43:00Z (PID 1083756→1276323; release `7af6210a` intacta — correcto: `f0c82905` sólo cambió el C# del AddOn, cero código Go desde `7af6210a`).

- **`BINDING_LOADED = PASS`** (plano binding): journal del proceso nuevo: `"echo.ntfeed.binding_loaded":true, "echo.ntfeed.binding_error":""` — el binding `E2T-GAU50-01` carga con `entitlement=ALLOWED` + `provider-external-account-id="3"` (fin del estado fail-closed `binding_loaded=false`/`provider-external-account-id is empty` de Shot 1 E4 / R2 §5).
- **`ACCOUNT_MATCH = MISMATCH` (fail-closed correcto, causa exacta conocida):** el AddOn reconectó de inmediato (nuevo puerto remoto 65432, mismo AddOn session id) y su hello lleva `expected_account=""` porque su config sigue discovery-only ⇒ `ntfeed.binding_match=MISMATCH`, detail `addon expects ****, binding authority is ****`. Ésta es la defensa defence-in-depth operando según diseño: sin config del AddOn alineada, la lane de cuenta no resuelve — jamás una resolución parcial o inventada.
- **Market lane regression = PASS:** contador del relay post-restart `published` 131→275 en 30 s (creciente), `publish_errors=0`, `malformed=0`, `rejected=1` (frame seq-0 post-reconnect, disciplina de seq fail-safe OK — mismo patrón que la certificación previa); heartbeats reales post-restart con `frames_sent` 89258+ creciente, `order_events=0`, `reconnects=2` (connect inicial + el reconnect real provocado por el restart del relay — primera demostración física de reconnect del AddOn contra relay real); heartbeat NQ vivo.
- **Ingress canónico con frames reales post-restart:** registros físicos en `echo.futures.market-feed-candidates.v1` (20:48Z, p4 offsets 87584+): QUOTE con BBO real (`bid 30774.5×4 / ask 30775×1` → evolución a `30775.5×2/30776×2`) y TRADE tick-a-tick (`price 30775.5 qty 1`, offsets 87730/87733/87738/87741/87752/87755), envelope congelado intacto (`stream_id=NQ:NQZ6`, `source_id=NINJATRADER_ADDON`, `log_identity=ninjatrader-addon/6e6eb8b665b4422495826c6f9c97e364`, `offset=seq` del AddOn).

## 4. Observaciones de cuenta (paso 6) — NOT_OBSERVABLE, fail-closed

Balances, positions, orders y executions de `RJARA114411201551` **no se publican** en este estado: el AddOn sólo publica snapshot/balances/positions/orders/executions cuando resuelve la cuenta configurada (`ResolveAccount`: `Id` esperado + cross-check `Name`), y su config sigue discovery-only. Es `NOT_OBSERVABLE` (la lane ni corre para la cuenta), **no** `EMPTY_OBSERVED`; no se fabricó evidencia con órdenes ni con configs parciales. La no-publicación es la degradación fail-closed diseñada, visible en journal (`MISMATCH`) — no un defecto.

## 5. Verificación de matriz (/verify)

| Item | Valor | Evidencia |
|---|---|---|
| OWNER_SELECTED_ACCOUNT_NAME | RJARA114411201551 | OD-2 owner (autoridad final N1) |
| CURRENT_NT_ACCOUNT_ID | "3" | Rediscovery vivo §1 (sesión 6e6eb8b6, frame 20:39:48Z seq 81992) |
| ACCOUNT_MATCH_COUNT | 1 | Mismo frame: 1 Name `RJARA114411201551` entre 8 descubiertas |
| ETCD_PROVIDER_EXTERNAL_ACCOUNT_ID | "3" | Escritura verificada §2 (read-back doble; 11 keys) |
| ADDON_ACCOUNT_ID | BLOCKED_OWNER (stageado "3") | §6: escritura del config vive en perfil owner (ACL denegada re-probeada 20:36Z: `Get-Content`/`Get-Acl` sobre `Documents\NinjaTrader 8\echo\` = Access denied) |
| ADDON_ACCOUNT_NAME | BLOCKED_OWNER (stageado "RJARA114411201551") | Ídem |
| BINDING_LOADED | **PASS** (plano relay/binding) | §3: `binding_loaded=true`, `binding_error=""` |
| ACCOUNT_MATCH | **MISMATCH** (fail-closed correcto; requiere ciclo owner) | §3: hello `expected_account=""` vs binding `"3"` |
| ACCOUNT_STATE | NOT_OBSERVABLE (fail-closed) | §4 |
| BALANCES | NOT_OBSERVABLE (fail-closed) | §4 |
| POSITIONS | NOT_OBSERVABLE (fail-closed) | §4 |
| ORDERS | NOT_OBSERVABLE (fail-closed) | §4 |
| EXECUTIONS | NOT_OBSERVED (sin orden generada) | §4 |
| REAL_HEARTBEAT | **PASS** | §3: heartbeats reales continuos post-restart, `frames_sent` 89258+, `order_events=0` |
| MARKET_LANE | **PASS** | §3: published creciente 0 errores, QUOTE/TRADE en el ingress |
| QUOTE_TO_ECHO | **PASS** | §3: registros QUOTE físicos p4 87584+ |
| TRADE_TO_ECHO | **PASS** | §3: registros TRADE físicos (price 30775.5 qty 1) |
| ORDERS_SENT | 0 | Estructural + heartbeats toda la sesión |
| ORDERS_MODIFIED | 0 | Ídem |
| ORDERS_CANCELLED | 0 | Ídem |

## 6. Bundle owner stageado (camino de cierre, ~2 min)

El config final del AddOn quedó construido y verificado sin tocar el perfil owner:

- **Archivo:** `kor@daedalus:/home/kor/opt/echo-dev/var/nt-feed/owner-install/n1-final/echo-feed-addon.json` (0600) — **idéntico al bundle original excepto `account_id: "3"` y `account_name: "RJARA114411201551"`** (diferencia demostrada por diff de campos); SHA256 `cc7bf7fac22ac1f730960dae95bf74092a4a4b77f4b67e88f80723438af313cf`.
- **Token verificado sin exponerlo:** tool efímero que compara el token del archivo vs `futures-bridge/nt-feed/auth-token` ETCD imprimiendo sólo `EQUAL` → **EQUAL** (el token del bundle = token ETCD = token desplegado, éste último probado por la auth real del hello 17:43:01Z). Eliminado tras la corrida.
- **Checklist owner:** `OWNER-CHECKLIST-N1-FINAL.md` SHA256 `17258d9c9d7f5ff15944d4592a52fd29a544a76e08f86ab05dd75a7d447b7cc7` — copiar `C:\Temp\echo-feed-addon.json` → `Documents\NinjaTrader 8\echo\` + restart NT; nada más.
- **Push físico a dev-win:** ambos archivos en `C:\Temp\` con hash idéntico verificado por `certutil` en dev-win vs `sha256sum` en Daedalus (transporte http.server local efímero + curl.exe, servidor apagado al cierre).

Tras ese ciclo owner, el reconnect del AddOn ya demostrado (§3) entrega automáticamente el nuevo hello con `expected_account="3"` ⇒ `binding_match=RESOLVED` + snapshots/balances/positions/orders/executions de la cuenta, sin ninguna acción Echo-side adicional. Un shot corto de re-verificación clasifica entonces los NOT_OBSERVABLE y cierra `D6_N1 = PASS`.

## 7. D6 DESIGN INPUT — ACCOUNT IDENTITY (registrado, NO resuelto aquí)

Observado en esta certificación (input para el Design Freeze, decisión Primary Manager):

- Echo necesita su propia representación/referencia durable de una cuenta; la identidad de negocio seleccionada por el owner es el `Name` Tradovate-embebido `RJARA114411201551` (autoridad `E2T-GAU50-01 → Name`).
- El `Account.Id` de NinjaTrader es un entero pequeño runtime-local (`"0"`–`"7"`: 3 cuentas locales + 5 GAU50, enumeradas en esta sesión); su estabilidad entre restarts de NT **no está demostrada** (observado `"3"` en una sola sesión NT; la de hoy comenzó post-restart del owner). Un drift de Ids post-restart rompería el binding actual — el diseño fallaría SEGURO (el cross-check `Name` del AddOn produciría `MISMATCH`, jamás datos de la cuenta equivocada), pero exigiría re-discovery + re-config: exactamente el costo que el freeze debe evaluar.
- Estado actual del binding (para contexto del freeze): la autoridad ETCD guarda el Id (`"3"`); el AddOn resuelve por `Id` con cross-check `Name`; el hello compara `Id` contra la autoridad (defence-in-depth Id↔Id). No se cambió nada de esto en esta certificación (mandato: usar el modelo D5 existente, sin nuevo schema).
- El diseño futuro no debe depender ciegamente de un identificador efímero de colección/runtime de NinjaTrader; la referencia business/provider durable hoy es el `Name`.

## 8. Handoff

```text
D6_N1_FINAL_ACCOUNT_BINDING =
BLOCKED_OWNER_ACTION (último ciclo físico owner: config AddOn + restart NT; stageado y verificado, ~2 min)

OWNER_SELECTED_ACCOUNT:
RJARA114411201551 (E2T-GAU50-01; OD-2 ejecutado)

CURRENT_NT_ACCOUNT_ID:
"3" (rediscovery vivo 2026-10-01T20:39:48Z, sesión 6e6eb8b665b4422495826c6f9c97e364, seq 81992; match count = 1)

PROVIDER_EXTERNAL_ACCOUNT_ID:
"3" (ETCD DEV /echo/development/futures-bridge/accounts/E2T-GAU50-01/provider-external-account-id; escritura guardada + read-back doble; 10→11 keys, hermanas intactas)

ADDON_ACCOUNT_ID:
BLOCKED_OWNER (stageado "3" en n1-final bundle; SHA cc7bf7fa…313cf; token verificado EQUAL contra ETCD sin imprimirlo)

ADDON_ACCOUNT_NAME:
BLOCKED_OWNER (stageado "RJARA114411201551", mismo bundle)

BINDING_LOADED:
PASS (relay release 7af6210a, PID 1276323: echo.ntfeed.binding_loaded=true, binding_error="")

ACCOUNT_MATCH:
MISMATCH (fail-closed correcto: hello del AddOn discovery-only expected_account="" vs binding "3"; se resuelve solo tras el ciclo owner)

ACCOUNT_STATE:
NOT_OBSERVABLE (lane fail-closed por diseño; no EMPTY_OBSERVED)

BALANCES:
NOT_OBSERVABLE (ídem)

POSITIONS:
NOT_OBSERVABLE (ídem)

ORDERS:
NOT_OBSERVABLE (ídem)

EXECUTIONS:
NOT_OBSERVED (ninguna orden generada para fabricar evidencia)

MARKET_LANE_REGRESSION:
PASS (post-restart: published creciente, publish_errors=0, malformed=0, rejected=1 seq-disciplina fail-safe; reconnect físico del AddOn demostrado; heartbeats frames_sent 89258+ order_events=0)

QUOTE_TO_ECHO:
PASS (ingress p4 87584+ BBO real 20:48Z)

TRADE_TO_ECHO:
PASS (ingress TRADE price 30775.5 qty 1, 20:48Z)

ORDERS_SENT:
0

ORDERS_MODIFIED:
0

ORDERS_CANCELLED:
0

ACCOUNT_IDENTITY_DESIGN_INPUT:
NT Account.Id = entero runtime-local ("0"-"7" en esta sesión); estabilidad entre restarts no demostrada; Name = identidad business durable hoy; diseño actual falla SEGURO ante drift Id (cross-check Name ⇒ MISMATCH, nunca cuenta equivocada) pero exige re-config; no resolver aquí — D6 Design Freeze (Primary Manager)

MUTATIONS_THIS_CERTIFICATION:
1 clave ETCD DEV (provider-external-account-id="3") + restart controlado de echo-nt-feed-relay (unidad propia del vertical, release intacta 7af6210a); cero cambios de código; worktree limpio antes y después; master y PROD intocados

BLOCKERS:
B-FINAL (único): escribir account_id/account_name en Documents\NinjaTrader 8\echo\echo-feed-addon.json + restart NT — sesión interactiva owner dev-win (ACL lectura+escritura denegadas a dev-win\echo-dev, re-probeada 2026-10-01T20:36Z; NT PID 984 SI=2). Todo stageado byte-verificado en C:\Temp + owner-install/n1-final con checklist (~2 min)

OWNER_DECISION_REQUIRED:
NINGUNA decisión nueva (OD-2 ejecutado); sólo ejecutar el checklist stageado OWNER-CHECKLIST-N1-FINAL.md

NEXT_MANAGER_ACTION:
comunicar al owner el checklist n1-final (copiar C:\Temp\echo-feed-addon.json → Documents\NinjaTrader 8\echo\ + restart NT); tras el restart, disparar el shot corto de re-verificación N1: hello binding_match=RESOLVED automático + clasificar ACCOUNT_STATE/BALANCES/POSITIONS/ORDERS (EMPTY_OBSERVED o datos reales) + smoke mercado → recién entonces D6_N1 = PASS. N2 sigue NOT AUTHORIZED (F1 STOP_MARKET + re-affirm owner de egress físico). No emitir EF_D6_E2E_PASS.
```

---

# FASE FINAL — CICLO OWNER EJECUTADO Y VERIFICADO (2026-10-01 21:15–21:27Z / local -03)

El owner ejecutó el checklist stageado §6: instaló `echo-feed-addon.json` final (`account_id: "3"`, `account_name: "RJARA114411201551"`) en `Documents\NinjaTrader 8\echo\` y reinició NinjaTrader Desktop. Shot corto de verificación ejecutado sobre esa realidad física, sin ninguna acción Echo-side adicional (relay y ETCD quedaron exactamente como en §2–§3).

## 9. Sesión física nueva (fresh NinjaTrader + AddOn)

- **NINJATRADER_FRESH_SESSION = PASS:** `NinjaTrader.exe` **PID 1876** (el de la fase blocked era 984), con **exactamente un** TCP `ESTABLISHED 192.168.31.132:49166 → 192.168.31.161:9770` (netstat dev-win, propiedad del PID 1876); el journal del relay registra `ntfeed addon session opened` a las 21:16:11.346Z desde `192.168.31.132:49166` — mismo puerto, cadena física PID↔conexión↔sesión coherente. La sesión previa `6e6eb8b6…` queda `stale=true` en la estadística del relay (tabla de sesiones, no conexión viva).
- **Nueva AddOn session id: `2f6a4d5375714a13b237f5ab65ba1fd6`** — hello (seq 0, evidence sink 0600, fidelidad completa): `addon_version 1.0.0`, `nt_version 8.1.8.3`, `expected_account_id: "3"`, `expected_account_name: "RJARA114411201551"`, `instruments: ["NQ 12-26"]`. El hello autenticado es el espejo en runtime del config instalado por el owner (la lectura directa del archivo sigue bloqueada por ACL del perfil owner; el hello ES la prueba física de lo que el AddOn cargó).
- **TRADOVATE_CONNECTED = PASS:** el PID 1876 mantiene `ESTABLISHED` a `34.117.68.229:443` ×2 (demo.tradovateapi.com, mismos endpoints certificados en C0/E9) + gateway de market data `3.140.144.89:31655` + `34.8.154.29:443`, `104.17.158.117:443`, `76.223.31.44:443`; frames `session` del AddOn: conexión `"Simulación"` Connecting (21:16:22.374Z) → Connected (21:16:25.387Z).
- **REAL_HELLO = PASS** (hello real autenticado, `session opened` 21:16:11.346Z) y **REAL_HEARTBEAT = PASS** (heartbeats reales continuos: `frames_sent` 3 → 759+ creciente al cierre, `reconnects: 1` = su connect inicial).

## 10. Rediscovery del account tras el restart

- Discovery vivo de la sesión nueva (frames `account`, ciclo ~10 s, sink full-fidelity): 8 cuentas — Backtest "0", Playback101 "1", Sim101 "2", **RJARA114411201551 "3"**, RJARA114411201571 "4", RJARA114411201541 "5", RJARA114411201491 "6", RJARA114411201521 "7". `RJARA114411201551` aparece **exactamente 1 vez** (resolución por Name única; match count = 1).
- **CURRENT_NT_ACCOUNT_ID = "3"** — observado en la sesión nueva post-restart, NO asumido del artefacto previo. `resolved = {id: "3", name: "RJARA114411201551"}` y **`match: RESOLVED` en todos** los frames `account` de la sesión (60+ al cierre).
- **NT_ACCOUNT_ID_STABLE_ACROSS_RESTART = YES** (acotado): `"3"` antes (sesión 6e6eb8b6, frame 20:39:48Z) y `"3"` después (sesión 2f6a4d53) del restart del owner — 2/2 sesiones de hoy. No es garantía general de estabilidad del enumerador runtime de NT; sigue siendo input de diseño (§7), no un supuesto del producto.
- **ETCD_PROVIDER_EXTERNAL_ACCOUNT_ID = "3"** — re-verificado por lectura plana MCP ETCD RO (`/echo/development/futures-bridge/accounts/E2T-GAU50-01/provider-external-account-id`, value "3", size 1; 11 keys en el prefijo, hermanas intactas). Sin escritura en esta fase.

## 11. Relay: binding cargado y resuelto

Journal del relay (release `7af6210a` intacta, PID 1276323, restart 20:43Z de la fase anterior): línea `ntfeed relay binding state` al arranque con `echo.execution_account: "E2T-GAU50-01"`, **`echo.ntfeed.binding_loaded: true`, `echo.ntfeed.binding_error: ""`**; la línea `session opened` del hello nuevo (21:16:11Z) lleva **`ntfeed.binding_match: "RESOLVED"`**. La única línea `binding_match: "MISMATCH"` de la ventana corresponde al `session opened` de la sesión vieja discovery-only (20:43Z, `expected_account=""`) — el fail-closed correcto de la fase anterior, ya superado. En los logs del relay los Ids de cuenta van enmascarados (`****`, sanitización de logs); la fidelidad completa vive en el evidence sink 0600.

## 12. Observaciones de cuenta (cuenta resuelta)

- **ACCOUNT_STATE = PASS:** frame `account` con `match: RESOLVED`, `resolved = {id: "3", name: "RJARA114411201551"}` — identifica inequívocamente la cuenta seleccionada.
- **BALANCES = PASS:** valores reales expuestos por la conexión Tradovate — `net_liquidation 50000`, `cash_value 50000`, `unrealized_profit_loss 0`, `realized_profit_loss 0`, `buying_power 0` (los cinco campos soportados con valores; no se exige ningún AccountItem no soportado). Progresión real observada: los primeros frames de la sesión traen 0/0 hasta que llegan los datos del proveedor (~5 s), luego los valores finales se estabilizan.
- **POSITIONS = PASS | EMPTY_OBSERVED:** `"positions": []` en todas las observaciones de la sesión (60+ frames).
- **ORDERS = PASS | EMPTY_OBSERVED:** `"orders": []` en todas las observaciones (60+ frames).
- **EXECUTIONS = NOT_OBSERVED:** no existe ningún frame de la familia `executions` en la sesión; el AddOn publica executions sólo por `ExecutionId` nuevo post-priming (el primer snapshot prima la historia sin publicarla) y en todos los heartbeats `order_events == account_events` exactamente — cero ejecuciones nuevas. No se generó actividad alguna para fabricar evidencia.
- **Semántica del contador (clasificación honesta, ver código @ f0c82905):** `order_events` es un contador de *observaciones* ("orders+executions observations", línea 83): +1 por cada publicación de la colección orders (línea 757) aunque esté vacía, +1 sólo por ejecución nueva (línea 796). Por eso en discovery-only era 0 (sesión vieja) y con cuenta resuelta crece 1:1 con `account_events` sin significar creación de órdenes. `orders: []` en todas las observaciones es la evidencia de ausencia de órdenes.

## 13. Market lane — regresión acotada

- **MARKET_LANE = PASS:** `market_ok: 525` frames de mercado procesados por el relay para la sesión nueva con `anomalies: []`, `stale: false`; contadores globales post-restart `published: 19707`, `publish_errors: 0`, `malformed: 0`, `rejected: 12` (disciplina de seq fail-safe: 11 anomalías de la sesión vieja + 1 del arranque; `malformed=0`). El burst de mercado ocurrió al inicio de la sesión (~21:16:29Z) y el venue demo quedó quieto después; la sesión sigue viva (frames_sent 759+ y frames de cuenta fluyendo al cierre). `NQ 12-26` suscripto (hello + frames procesados).
- **QUOTE_TO_ECHO = PASS / TRADE_TO_ECHO = PASS:** registros físicos en `echo.futures.market-feed-candidates.v1` p4 offsets 102123–102128 con `log_identity: ninjatrader-addon/2f6a4d5375714a13b237f5ab65ba1fd6` — QUOTE con BBO real (`bid 30770.25×1 / ask 30771.25×2` → evolución `30760×2/30810×1`) y TRADE tick-a-tick (`price 30770.25 qty 1`, `30771.25 qty 1`), envelope congelado intacto (`stream_id=NQ:NQZ6`, `source_id=NINJATRADER_ADDON`, `ingress_ref.offset` = seq del AddOn 526–531). El delay ~600 s de `event_ts` (feed demo) persiste — hallazgo 1 de la certificación previa, vigente, no bloquea N1.
- Observación ambiental no bloqueante: `failed to upload metrics ... 192.168.31.45:4317 connection refused` (OTEL dev caído, preexistente e ignorado por el lane).

## 14. Safety final

`grep -nE '\.Submit\(|\.Change\(|\.Cancel\(|\.Flatten\(|\.CreateOrder\('` sobre `v3/futures-bridge/addon-ninjatrader/EchoFeedAddOn.cs` @ `f0c82905` (worktree limpio) = **0 matches** (única mención: comentario negativo línea 18). El protocolo `echo.ntfeed.v1` mantiene exactamente las familias de observación sin familia de comandos; el relay nunca escribe al AddOn; el execution bridge sigue sin arrancar. `ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0`, estructural y observado (colecciones orders/positions vacías en todas las observaciones, cero ejecuciones nuevas, heartbeats sin eventos de orden). Mutaciones de la fase final: **ninguna** (cero escrituras ETCD, cero restarts, cero cambios de código; master y PROD intocados).

## 15. Matriz final (/verify) y handoff

| Item | Valor | Evidencia |
|---|---|---|
| NINJATRADER_FRESH_SESSION | **PASS** | PID 1876 ≠ 984; sesión nueva `2f6a4d53…`; TCP :49166 → :9770 propiedad de NinjaTrader.exe; session opened 21:16:11.346Z |
| TRADOVATE_CONNECTED | **PASS** | PID 1876 ESTABLISHED demo.tradovateapi.com ×2 + MD gateway :31655 + 3 endpoints; frames session "Simulación" Connected |
| ADDON_LOADED | **PASS** | AddOn compilado corriendo y publicando frames en la sesión nueva |
| REAL_HELLO | **PASS** | hello seq 0 autenticado 21:16:11.333Z con identidad de cuenta configurada |
| REAL_HEARTBEAT | **PASS** | frames_sent 3→759+ creciente, reconnects 1 |
| OWNER_SELECTED_ACCOUNT | RJARA114411201551 | OD-2 owner (autoridad final N1) |
| CURRENT_NT_ACCOUNT_ID | **"3"** | Rediscovery vivo sesión nueva (match count 1 de 8) |
| NT_ACCOUNT_ID_STABLE_ACROSS_RESTART | **YES (acotado 2/2 sesiones hoy)** | §10; sigue siendo input de diseño |
| ETCD_PROVIDER_EXTERNAL_ACCOUNT_ID | "3" | MCP ETCD RO read-back (11 keys, sin escritura en esta fase) |
| HELLO_EXPECTED_ACCOUNT_ID | "3" | hello frame sesión nueva |
| HELLO_EXPECTED_ACCOUNT_NAME | RJARA114411201551 | hello frame sesión nueva |
| BINDING_LOADED | **PASS** | `binding_loaded=true`, `binding_error=""` (journal relay) |
| BINDING_MATCH | **RESOLVED** | línea `session opened` 21:16:11Z; todos los frames account `match=RESOLVED` |
| ACCOUNT_STATE | **PASS** | resolved {id "3", name RJARA114411201551} + balances |
| BALANCES | **PASS** | NLV 50000 / cash 50000 / UP 0 / RL 0 / buying_power 0 (lo que expone la conexión) |
| POSITIONS | **PASS \| EMPTY_OBSERVED** | `[]` en todas las observaciones |
| ORDERS | **PASS \| EMPTY_OBSERVED** | `[]` en todas las observaciones |
| EXECUTIONS | **NOT_OBSERVED** | 0 ejecuciones nuevas post-priming; sin actividad fabricada |
| MARKET_LANE | **PASS** | market_ok 525, anomalies=[], published 19707, errs 0, malformed 0 |
| QUOTE_TO_ECHO | **PASS** | ingress p4 102123+ BBO real, log_identity sesión nueva |
| TRADE_TO_ECHO | **PASS** | ingress p4 102124+ price/qty reales, log_identity sesión nueva |
| ORDERS_SENT | 0 | estructural + observado |
| ORDERS_MODIFIED | 0 | ídem |
| ORDERS_CANCELLED | 0 | ídem |

```text
D6_N1_FINAL_ACCOUNT_BINDING =
PASS

D6_N1 =
PASS

OWNER_SELECTED_ACCOUNT:
RJARA114411201551

NT_ACCOUNT_ID_BEFORE_RESTART:
3 (sesión 6e6eb8b665b4422495826c6f9c97e364, rediscovery vivo 20:39:48Z)

NT_ACCOUNT_ID_AFTER_RESTART:
3 (sesión 2f6a4d5375714a13b237f5ab65ba1fd6, rediscovery vivo post-restart 21:16Z+, match count 1 de 8)

ACCOUNT_ID_STABILITY_OBSERVATION:
YES acotado — "3" en 2/2 sesiones de NT de hoy (pre y post restart del owner); el Id sigue siendo un entero runtime-local de NT sin garantía general de estabilidad; la referencia business durable es el Name RJARA114411201551; cross-check Name del AddOn permanece como defensa ante drift (MISMATCH fail-closed, nunca cuenta equivocada). Decisión de representación durable de Account = D6 Design Freeze (Primary Manager), no se resuelve aquí.

BINDING_LOADED:
PASS (binding_loaded=true, binding_error="", journal relay release 7af6210a PID 1276323)

BINDING_MATCH:
RESOLVED (session opened 21:16:11Z; match=RESOLVED en todos los frames account de la sesión nueva)

ACCOUNT_STATE:
PASS (resolved {id "3", name RJARA114411201551}, match RESOLVED, balances incluidos)

BALANCES:
PASS (net_liquidation 50000, cash_value 50000, unrealized 0, realized 0, buying_power 0 — campos soportados expuestos por la conexión Tradovate demo; progresión real 0/0→valores observada)

POSITIONS:
PASS | EMPTY_OBSERVED ([] en todas las observaciones)

ORDERS:
PASS | EMPTY_OBSERVED ([] en todas las observaciones)

EXECUTIONS:
NOT_OBSERVED (0 ejecuciones nuevas post-priming; order_events==account_events en todos los heartbeats, sin frames executions; ninguna orden generada para fabricar evidencia)

MARKET_LANE:
PASS (market_ok 525 anomalies=[], published 19707 publish_errors=0 malformed=0; QUOTE/TRADE físicos en ingress con log_identity=ninjatrader-addon/2f6a4d53…; delay ~600 s del feed demo persiste, no bloquea)

QUOTE_TO_ECHO:
PASS (p4 102123+ BBO real, envelope congelado intacto)

TRADE_TO_ECHO:
PASS (p4 102124+ price/qty reales, envelope congelado intacto)

ORDERS_SENT:
0

ORDERS_MODIFIED:
0

ORDERS_CANCELLED:
0

MUTATIONS_THIS_PHASE:
NINGUNA (cero ETCD, cero restarts, cero código; sólo lectura física y este artefacto)

BLOCKERS:
NONE

OWNER_DECISION_REQUIRED:
NONE

NEXT_MANAGER_ACTION:
Registrar D6_N1 = PASS en la verdad del proyecto y pasar a la planificación D6-N2, que sigue NOT AUTHORIZED hasta que (a) F1 STOP_MARKET esté implementado/certificado y (b) el owner re-affirme explícitamente la autorización de egress físico para la cuenta GAU50 seleccionada. El input de identidad de cuenta (§7 + estabilidad observada 2/2) queda para el D6 Design Freeze del Primary Manager. No emitir EF_D6_E2E_PASS.
```

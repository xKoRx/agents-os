# Echo Futures — D6 N1 — Physical Read-Only Certification

**Fecha:** 2026-10-01 (evidencia 19:23–19:47Z / local -03)
**Alcance:** certificación física read-only del vertical NinjaTrader AddOn → `nt-feed-relay` → ingress canónico, tras el closeout R3. Sin ejecución de órdenes. N2 = NOT AUTHORIZED.
**Role:** Physical Integration Certifier (no Manager, no Owner, no arquitecto)
**Base:** [[N1-SHOT1-READONLY-VERTICAL]] + [[N1-R1-REMOVE-UNAUTHORIZED-OWNER-RISK-MODEL]] + [[N1-R2-CORRECT-EARN2TRADE-ENTITLEMENT]] + [[N1-R3-NINJATRADER-PHYSICAL-COMPILE-REPAIR]] (PASS, commit `f0c82905`)
**Sesión física verificada:** AddOn real session `6e6eb8b665b4422495826c6f9c97e364`, iniciada 2026-10-01T19:23:45.727Z (16:23:45 -03) desde `192.168.31.132:65181`, TCP continuo sin cortes.

## 0. Hard safety

`ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0`, estructural y observado: el AddOn no contiene ninguna llamada a `Account.Submit/Change/Cancel/Flatten/CreateOrder` (grep sobre el source final = 0 matches, re-verificado pre-commit `f0c82905`); el protocolo `echo.ntfeed.v1` mantiene exactamente 8 familias de observación sin familia de comandos; el relay nunca escribe al AddOn; el execution bridge sigue sin arrancar; los heartbeats reales del AddOn reportan `order_events: 0` durante toda la sesión. No se generó orden alguna para fabricar evidencia de ejecución. Ningún cambio de Go, ETCD, Kafka, ACLs ni identidades en esta certificación.

## 1. Matriz de evidencia física (/verify)

| Item | Valor | Evidencia |
|---|---|---|
| NINJATRADER_RUNNING | PASS | `NinjaTrader.exe` PID 984, sesión SI=2 (owner), vivo en dev-win; hello real reporta `nt_version: 8.1.8.3` resuelto en runtime vía `Globals.ProductVersion` |
| TRADOVATE_CONNECTED | PASS | TCP ESTABLISHED del PID 984 hacia los mismos endpoints certificados en C0/E9: `34.117.68.229:443` ×2 (demo.tradovateapi.com) + `3.133.196.229:31655` (MD gateway) + 2 endpoints adicionales; puertos locales nuevos del restart del owner |
| R3_COMPILE_ERRORS | 0 | Owner reporta 0 errores visibles; probado físicamente por carga (el pre-R3 no compilaba y el AddOn está corriendo); output textual no recuperable desde el boundary del agente (ACL perfil owner, re-probeada) |
| ADDON_INSTANTIATED | PASS | Frames reales del AddOn en el canal (~25.7k frames); conexión al relay propiedad de NinjaTrader.exe PID 984 (`netstat -ano` dev-win) |
| CONFIG_LOADED | PASS | Hello real = espejo del config discovery-only: `expected_account_id: ""`, `instruments: ["NQ 12-26"]` |
| REAL_RELAY_CONNECTION | PASS | ESTAB `192.168.31.132:65181 → daedalus:9770`, sesión única desde 19:23:45Z, mismo puerto remoto sin cortes; `sessions: 1` |
| REAL_HELLO | PASS | `ntfeed addon session opened` 19:23:45.727Z post-auth (constant-time compare; `malformed=0`); hello seq=1 con `addon_version 1.0.0` |
| REAL_HEARTBEAT | PASS | Heartbeats reales con contadores crecientes: `frames_sent` 4703→14112+ (19:32Z), `order_events: 0`; el `reconnects: 1` del AddOn = su connect inicial (una sola sesión TCP) |
| GAU50_DISCOVERED_COUNT | 5 | Discovery real vía `Account.All`: 5 cuentas GAU50 `RJARA*` + 3 cuentas locales NT (Backtest, Playback101, Sim101); `match: DISCOVERY_ONLY` |
| NQ_SUBSCRIPTION | PASS | `NQ 12-26` resuelto (`GetInstrument(name, false)`), frames de mercado continuos: `market_ok` 353→25464 en ~23 min |
| BID | PASS | QUOTE con BBO emparejado (p.ej. `bid_price 30796.25 qty 2`); múltiples updates reales |
| ASK | PASS | Ídem (`ask_price 30796.75 qty 4`); ladder realista 1–5 contratos |
| LAST | PASS | TRADE tick-a-tick con price/qty (p.ej. `price 30797 qty 2`), timestamps del feed |
| QUOTE_TO_RELAY | PASS | Frames QUOTE procesados por el relay (`market_ok` counter), `published=25464`, `publish_errors=0`, `malformed=0` |
| TRADE_TO_RELAY | PASS | Frames TRADE procesados por el relay, misma disciplina |
| QUOTE_TO_ECHO_INGRESS | PASS | Registros físicos en `echo.futures.market-feed-candidates.v1` (p4 offsets 11569+/12770+): envelope con `source_id=NINJATRADER_ADDON`, `log_identity=ninjatrader-addon/<sesión real>`, payload canónico QUOTE |
| TRADE_TO_ECHO_INGRESS | PASS | Ídem, `event_type: TRADE` en el mismo log_identity |
| ACCOUNT_BINDING | BLOCKED_OWNER_DECISION | `provider-external-account-id` nunca existió en ETCD (10 keys verificadas RO); no existe autoridad preexistente que mapee una GAU50 descubierta a `E2T-GAU50-01`; relay fail-closed visible (`binding_loaded=false`, lane de mercado stream-level operativa) |
| ACCOUNT_STATE | NOT_APPLICABLE | Balances sólo se publican con cuenta resuelta (diseño); discovery-only publicará identidad, no balances |
| POSITIONS | NOT_APPLICABLE | Sólo se publican para la cuenta resuelta (diseño); en discovery-only no aplican |
| ORDERS | NOT_APPLICABLE | Ídem; `order_events: 0` en toda la sesión |
| EXECUTIONS | NOT_APPLICABLE | Ídem; `EXECUTIONS = NOT_OBSERVED` quedaría subsumido; sin orden alguna generada para fabricar evidencia |

## 2. Discovery GAU50 — candidatos sanitizados para decisión owner

Observados vía el AddOn real (`Account.All`, publicación periódica cada ~10 s, ids tal como los reporta NinjaTrader en esta sesión):

| Cuenta (NT Name) | NT `Account.Id` observado | Clasificación |
|---|---|---|
| RJARA114411201551 | "3" | GAU50 Evaluation (candidata) |
| RJARA114411201571 | "4" | GAU50 Evaluation (candidata) |
| RJARA114411201541 | "5" | GAU50 Evaluation (candidata) |
| RJARA114411201491 | "6" | GAU50 Evaluation (candidata) |
| RJARA114411201521 | "7" | GAU50 Evaluation (candidata) |
| Backtest / Playback101 / Sim101 | "0" / "1" / "2" | cuentas locales NT, no GAU50 |

No se eligió ninguna, no se infirió la activa, no se tomó la primera por orden. Caveat material para la decisión: los `Account.Id` observados son enteros pequeños internos de NT en esta sesión (el número Tradovate viaja en el `Name`); la estabilidad de esos Ids entre restarts de NT no fue demostrada (una sola observación post-restart). El AddOn resuelve por `Id` con cross-check `Name` — la pregunta owner debe considerar ambos campos.

## 3. Market data — cadena física completa

QUOTE y TRADE demostrados en los tres planos con la misma identidad de sesión: (1) AddOn side — frames enviados por el AddOn real (evidence sink 0600 + journal del relay con payloads `instrument: "NQ 12-26"`); (2) relay side — `published=25464, publish_errors=0, malformed=0, rejected=2, stale=false` (19:46:59Z); (3) ingress — registros en `echo.futures.market-feed-candidates.v1` con envelope congelado (`stream_id=NQ:NQZ6`, key `NQ:NQZ6`, `ingress_ref{log_identity: ninjatrader-addon/6e6eb8b665b4422495826c6f9c97e364, partition:0, offset:seq}`). Ningún evento sintético participa en esta certificación (el smoke sintético Shot 1 queda registrado como historia).

`NQ_FULLNAME = "NQ 12-26"` — resuelto físicamente por el AddOn instalado (la ruta de fallo de resolución es fail-closed y no se disparó); mapping canónico NQ→NQZ6 aplicado por el relay.

## 4. Hallazgos (observaciones honestas, ninguno bloquea N1)

1. **Market data retrasada ~600 s (entorno, no defecto del AddOn):** `event_ts` constante exactamente ~600 s detrás del tiempo de llegada, desde el primer frame; el reloj de dev-win fue verificado correcto contra Daedalus (19:35:38.99Z); el AddOn usa `e.Time` del evento de mercado de NT (código línea 460, propagación fiel). Conclusión: el feed demo del venue entrega market data con delay de 10 minutos (entitlement demo). **Input N2:** ninguna decisión de estrategia puede tomarse contra este feed demo; producción exige entitlement real-time.
2. **Enumeración de conexiones NT:** el scan del AddOn publicó exactamente una conexión CBI (`"Simulación"`, Connected) en toda la sesión; el transporte Tradovate está vivo a nivel TCP (mismos endpoints C0/E9). El mapeo entre la colección `Connection.Connections` visible al AddOn y la sesión Tradovate demo no es verificable desde el boundary del agente (GUI/logs NT ACL-owner). Sin impacto en las obligaciones N1 (eventos, discovery y transporte verificados físicamente); queda para awareness owner.
3. **Disciplina de seq (fail-safe OK):** 2 frames rechazados en ~25.7k (seq 0 = frame encolado antes del hello inmediato del fix #6; seq 4583 = duplicado por reenvío in-flight), `malformed=0`; el tracker monótono funcionó como diseñado, integridad preservada.
4. **Estabilidad de `Account.Id`:** ver §2 — caveat para la decisión owner de binding.

## 5. Handoff

```text
D6_N1_R3_NINJATRADER_COMPILE =
PASS

R3_ECHO_COMMIT:
f0c82905d4eaf825c08e04f0bb97cab73e616ba5

D6_N1_PHYSICAL_CERTIFICATION =
PARTIAL_BLOCKED_OWNER

NINJATRADER_VERSION:
8.1.8.3 (dev-win 192.168.31.132, PID 984, sesión owner SI=2)

TRADOVATE_CONNECTED:
PASS (TCP endpoints demo.tradovateapi.com x2 + MD gateway 31655 desde PID 984; ver hallazgo 2 sobre la enumeración CBI)

ADDON_COMPILE_ERRORS:
0

ADDON_INSTANTIATED:
PASS

CONFIG_LOADED:
PASS

REAL_RELAY_CONNECTED:
PASS

REAL_HELLO:
PASS

REAL_HEARTBEAT:
PASS

GAU50_DISCOVERED_COUNT:
5 (más 3 cuentas locales NT: Backtest, Playback101, Sim101)

DISCOVERED_GAU50:
RJARA114411201551 (Id "3") | RJARA114411201571 (Id "4") | RJARA114411201541 (Id "5") | RJARA114411201491 (Id "6") | RJARA114411201521 (Id "7")

ACTIVE_ACCOUNT_AUTHORITY:
OWNER_DECISION_REQUIRED

PROVIDER_EXTERNAL_ACCOUNT_ID:
NOT_CONFIGURED (clave inexistente en ETCD; OD-2 pendiente)

NQ_FULLNAME:
"NQ 12-26" (resuelto por el AddOn instalado; mapping canónico NQ→NQZ6 en el relay)

NQ_SUBSCRIPTION:
PASS

BID:
PASS

ASK:
PASS

LAST:
PASS

QUOTE_TO_RELAY:
PASS

TRADE_TO_RELAY:
PASS

QUOTE_TO_ECHO_INGRESS:
PASS

TRADE_TO_ECHO_INGRESS:
PASS

ACCOUNT_STATE:
NOT_APPLICABLE (post-binding; discovery-only por config)

POSITIONS:
NOT_APPLICABLE (sólo con cuenta resuelta, por diseño)

ORDERS:
NOT_APPLICABLE (ídem; order_events=0 en toda la sesión)

EXECUTIONS:
NOT_APPLICABLE (ídem; ninguna orden generada para fabricar evidencia)

ENTITLEMENT:
ALLOWED

ORDERS_SENT:
0

ORDERS_MODIFIED:
0

ORDERS_CANCELLED:
0

CODE_FIXES:
NINGUNO en esta certificación (closeout = commit-only del repair R3 f0c82905 tras evidencia física)

BLOCKERS:
B-OD2 (único): selección owner de la GAU50 activa — sin ella no hay binding ni observaciones de cuenta

OWNER_DECISION_REQUIRED:
Select one discovered GAU50 as E2T-GAU50-01 — candidatos en §2; considerar el caveat de estabilidad de Account.Id (elegir y documentar si la identidad de binding es el Id, el Name, o ambos como cross-check ya implementado)

NEXT_MANAGER_ACTION:
comunicar OD-2 al owner con los candidatos §2; tras la selección: fijar provider-external-account-id en ETCD DEV + account_id en la config del AddOn (misma identidad), reload mínimo, shot corto de verificación (binding_loaded=true + match RESOLVED + balances/positions/orders/executions EMPTY_OBSERVED o datos reales) → entonces D6_N1 PASS completo; N2 sigue NOT AUTHORIZED (F1 STOP_MARKET + re-affirm owner de egress físico pendientes). No emitir EF_D6_E2E_PASS.
```

# Echo Futures — D6 Weekend Physical Readiness (NO EGRESS) — 2026-10-03

**Shot:** D6 — WEEKEND PHYSICAL READINESS — TOP Senior Physical Readiness Lead (one-shot, fresh context; no Manager, no Owner)
**Date:** 2026-10-03 (sábado; evidencia UTC 14:25Z–15:10Z, CME cerrado desde vie 2026-10-02 ~16:00 CT)
**Project:** [[Echo Futures]]
**Owner authorization:** OD-D6-1 = AUTHORIZED y VIGENTE (no consumido por este shot: `PHYSICAL_ORDERS_SENT = MODIFIED = CANCELLED = 0`). Este mandato NO autoriza egress y no emitió ninguno.
**Baseline:** `xKoRx/echo@40102ea5a44be9a618ac12529e6f0e9fdfd46d34` (`origin/feature/d6-shot1-execution-vertical`, candidato Shot 3) — verificado worktree limpio, `origin == HEAD`.
**Final SHA:** `40102ea5a44be9a618ac12529e6f0e9fdfd46d34` — **cero commits, cero cambios de producto** (los únicos deltas son config-act DEV + deployment del bridge + bundle owner; ver §15).
**Verdict:** `D6_PHYSICAL_READINESS_NO_EGRESS = READY` (con un único paso owner-assisted pendiente por diseño: ciclo de instalación del AddOn de ejecución, preparado y checklisteado — ver §2 y §14).

---

## 1. Baseline (heredado + re-verificado hoy)

| Hecho | Valor | Verificación de hoy |
|---|---|---|
| Repo | `40102ea5` en `feature/d6-shot1-execution-vertical`, tree limpio, `origin == HEAD` | `git rev-parse` + `status --porcelain` = 0 |
| NinjaTrader | 8.1.8.3, dev-win 192.168.31.132, PID 1876, sesión owner SI=2, continuo | Get-Process (StartTime no consultable por ACL) |
| Feed AddOn instalado | sesión `2f6a4d53…` viva; versión instalada = **R3 @ f0c82905** (más antigua que HEAD) | frames del relay + hashes §2 |
| Relay feed | `echo-nt-feed-relay` release `170a4581`, PID 1388002, `:9770` LISTEN, frames fluyendo | systemctl + journalctl + `ss` |
| Execution AddOn | STAGED en `C:\Users\TEMP`, hash `b2a29a36…` == HEAD byte-idéntico (certutil) | re-probado hoy |
| ACL owner profile | **Access denied** (4.ª re-probe consecutiva en 3 sesiones): toda instalación es ciclo owner (OD-D6-4) | `Test-Path` → UnauthorizedAccess |
| Binding ETCD DEV | 9 claves binding (enabled=true, ALLOWED, EARN2TRADE/GAU50, GAU50-EVAL v1, ref RJARA114411201551, tz America/Chicago, reset 17:00) + transport-id=NINJATRADER_BRIDGE + Id hint "3" + NQ 12-26 | lectura exacta por cliente crudo (no fuzzy) |
| `futures-bridge/accounts` (sesiones) | AUSENTE al inicio (G-EGRESS-0) | lectura exacta |
| `futures-bridge/ntx/auth-token` | AUSENTE al inicio (el bridge es fail-closed sin él) | lectura exacta |
| Kafka DEV | topic `echo.order-commands.E2T-GAU50-01.v1` **no existe** (0 riesgo de replay); `echo.futures.session-observations.v1` no existía | list_topics + describe |
| Mercado | sábado: último evento `NQ:NQZ6` event_ts `2026-10-02T21:38:25.95Z` (vie 16:38:25 CDT) | kafka-last (§9) |

## 2. Real AddOn installation (W1) — **BLOCKED_OWNER_ACTION** (acción preparada al 100%)

El perfil owner (`C:\Users\KoR\Documents\NinjaTrader 8\…`) es deny read/write desde el acceso agente (realidad C0/N1-R3, re-probada hoy). Se preparó el ciclo owner completo, byte-verificado:

- **Bundle en dev-win `C:\Temp\`** (transporte http.server efímero + `curl.exe`; servidor apagado al cierre; SHA256 idénticos en ambos lados):
  - `EchoExecutionAddOn.cs` = `b2a29a3608cf1e1b767844156c8d03f23fd324e668fab1efde97489fd885729a` (HEAD; shadow-compile Shot 3 PASS vs 8.1.8.3, 3 warnings preexistentes registrados).
  - `EchoFeedAddOn.cs` = `581a7087b1b870c78ac43e67027e5edaacf59134f4bf5f03d8b9aec9d7fd5ae4` (HEAD; **actualiza el instalado R3** con la inversión Name-primaria; shadow-compile 0 warnings).
  - `echo-execution-addon.json` = `9ca3fddc31330b2d5b485fd0869801b486b1443972bbf5ba50c56862feeea71b` (schema del parser del AddOn: ntx_host 192.168.31.161:9771, token ntx DEV, account_name RJARA114411201551, account_id 3, contracts NQZ6↔NQ 12-26, snapshot/heartbeat 5 s).
  - `OWNER-CHECKLIST-W1.md` (pasos exactos: copiar 2 .cs a `bin\Custom\AddOns\` + json a `echo\` + restart NT + devolver compile errors si los hay; **sin órdenes**).
- Copia canónica en Daedalus: `/home/kor/opt/echo-dev/var/nt-feed/owner-install/weekend-20261003/`.
- **El token ntx** vive en ETCD DEV (`futures-bridge/ntx/auth-token`, creado hoy, 64 hex, secreto no impreso) y viaja al perfil sólo dentro del JSON del checklist.

Estado: `EXECUTION_ADDON_INSTALLED = BLOCKED_OWNER_ACTION` — el paso es el ciclo owner standing (OD-D6-4, ~3 min con el checklist), diseñado para ejecutarse junto a la ventana (recomendado: domingo previo al reopen o lunes pre-ladder). Mientras no exista, el lane de ejecución queda sin endpoint AddOn; todo lo demás del ladder está preparado.

## 3. Execution lane startup (W2) — **PASS (lado bridge, transporte real)**

Deployment DEV nuevo (layout canónico Daedalus, propiedad de esta sesión):

- Release `/home/kor/opt/echo-dev/releases/40102ea5a44be9a618ac12529e6f0e9fdfd46d34/futures-bridge` — go1.27.1, `-trimpath -buildvcs=true`, **`vcs.revision=40102ea5…`, `vcs.modified=false`**, SHA256 `484b550b740981ab1ff4a6e32290865f742c2a47519473c3b35a7a8a7e39a8bc`. `BUILD.md` con rollback documentado.
- Unidad systemd --user `echo-futures-bridge.service` (EnvironmentFile 0600 con ETCD endpoints; **disabled**: no arranca en reboot; started manualmente para esta sesión).
- Config-act ETCD DEV (escritura guardada: pre-lectura exacta → SetVar → read-back del writer → cross-check RO MCP independiente): `futures-bridge/ntx/auth-token` (nuevo, secreto), `futures-bridge/journal-root=/home/kor/opt/echo-dev/var/futures-bridge/journal`, `futures-bridge/accounts=E2T-GAU50-01`.
- **Proceso físico:** PID 1697786 (y tras restarts 1699685/1699941), RSS ~30 MB, CPU 0.1%, listener `*:9771`, journal M2 abierto (0 registros), consumer `echo-futures-bridge-E2T-GAU50-01-daedalus` (ReadCommitted, OffsetOldest; estado DEAD benigno porque el topic de comandos aún no existe — el join ocurrirá con el primer comando, sin pérdida).
- **NO-EGRESS estructural verificado en runtime:** readiness surface del bridge cada 30 s: `ready_new_risk=false` con blockers `[POSITION_NOT_FRESH RECONCILIATION_AUTHORITY_UNAVAILABLE STATIC_ELIGIBILITY_NOT_ELIGIBLE SUBMISSION_CAPABILITIES_NOT_EXACT_READY]`, `ambiguous_orders=0, mismatches=0, dropped_commands=0`. Capabilities M2 todo UNKNOWN ⇒ `SubmissionCapabilitiesReady=false` ⇒ la conjunción congelada jamás abre new risk; ningún comando M1 existe (no hay run LIVE; feed STALE ⇒ 0 señales; topic de comandos inexistente).
- **Barrier fail-closed positivo:** sin observaciones venue reales el recovery barrier SE NIEGA a completar (`barrier: reconcile: ninjatrader: no position snapshot observed yet`, reproducible en 3 arranques). No se inyectaron snapshots vacíos ni datos fabricados: la sesión de cuenta permanece fail-closed hasta que el AddOn real publique evidencia venue. **Nota operacional para la ventana:** el shell no reintenta la sesión — arrancar el bridge con el AddOn ya conectado (o restart del bridge tras el ciclo owner).
- **Path completo físicamente probado con sesión de transporte auto-etiquetada** (probe cliente ntx, hello `addon_version=weekend-readiness-probe`, ref de binding correcta, SOLO hello+heartbeats — jamás familias de observación): lane → adapter (hello RESOLVED) → gate → Kafka `echo.futures.session-observations.v1` registro real (`SESSION E2T-GAU50-01 NINJATRADER_BRIDGE CONNECTED`, latencia hello→Kafka 281 ms). Registros de sesión del probe quedan en DEV, auto-identificados por session_id y superseded automáticamente por el AddOn real en la ventana.

## 4. Account binding (W3) — **PASS**

Resolución viva durante toda la sesión (frames del relay 11:31–11:44Z + evidence sink sin máscara):

- Discovery: 8 cuentas (`Backtest`, `Playback101`, `Sim101`, 5× GAU50 `RJARA…491/521/541/551/571`) — **exactamente 1 match** para `RJARA114411201551`.
- `"match":"RESOLVED"`, `"resolved":{"id":"3","name":"RJARA114411201551"}` — **NT `Account.Id` actual = "3"** = hint ETCD (4.ª sesión consecutiva observada: 2/2 N1 + intento 1 + hoy). Sin drift; identidad Name-primary intacta; identidad de negocio no mutada.
- Hello defence de transporte: el probe autenticado con la ref correcta resolvió `RESOLVED`; con token erróneo → rechazo (§5); el adapter fail-closes `MISMATCH`/`DRIFT` (código congelado + tests).

## 5. Session/reconnect evidence (W4) — **PASS (lado server/transporte; endpoint AddOn en G-E2E)**

Drills físicos contra el bridge release `40102ea5` corriendo (protocolo `echo.ntx.v1` real, sin comandos, sin datos fabricados):

| Drill | Resultado | Evidencia |
|---|---|---|
| Auth negativa (token erróneo) ×N | **PASS** — hello rechazado constant-time, TCP cerrado sin datos | 5+ `[ntx] … rejected: hello auth token mismatch` (journal 11:53:0x) + `badtoken_result EOF read_n=0` ×N |
| Fencing de sesión activa (F-S2-04) | **PASS** — B autentica ⇒ server CIERRA la conexión de A inmediatamente | `[ntx] 8ce02863… rejected: session superseded by "dbcf431c…"; previous connection fenced`; A recibe broken pipe en su siguiente heartbeat |
| Reconnect con identidad nueva (F-S2-01) | **PASS** — A re-dial con NUEVO session_id y seq=1 aceptado | A: `session_id c387e111…` (antes `8ce02863…`); sin reject de seq; lo mismo en cada reconnect (8+ identidades) |
| Seq rebobinada dentro de sesión | **PASS** — frame rechazado como *counted evidence*: jamás es dato (0 publicaciones, 0 cambios de estado), conexión preservada | `rewind_result` + tracker del adapter (contrato frozen `TestServerActiveSessionFencing`); sin línea de reject por diseño (`dup ⇒ return nil`) |
| Transferencia de autoridad | **PASS** — cada hello nuevo = único punto de transferencia; sesiones supersedadas jamás alcanzan el handler (segunda barrera del adapter: código congelado + 2 tests adversariales; el ejercicio físico con frame en-vuelo queda en G-E2E por diseño congelado) | drills de fencing ×3 (B→A, rewind→A, restart→A) |

`COMMAND_FRAME_RECEIVED` (alerta del probe ante cualquier frame de comando): **0 en todos los logs**. El bridge nunca escribió un comando (no hay autorización ni journal PREPARED).

## 6. Account observation (W5) — **PASS (plane de observación real, account flat)**

- **Feed lane (real, AddOn real):** snapshots cada ~5 s de `account` (balances NLV/cash/BP/uPnL/rPnL = 0/0/0/0/0 — variante demo de fin de semana documentada en el intento 1), `positions: []`, `orders: []`, sesión `2f6a4d53` continua, heartbeat `frames_sent 5,435,534 · market_events 5,375,579 (estático desde el cierre) · order_events/account_events 14,984 · reconnects 2`.
- **Serialization/reconciliation input:** el payload `account` lleva discovery completo + match + resolved por campo; frames `orders`/`positions` vacíos consistentes en todos los ciclos.
- **Bridge publisher path:** familia SESSION publicada a Kafka con envelope frozen (schema/family/event) — verificado en `echo.futures.session-observations.v1` (§3). Las familias order/fill/position comparten el mismo publisher (routing frozen 3 topics; sólo se ejercitó SESSION por no fabricar datos venue).
- `EXECUTIONS`: primed-not-published (el feed lane no publica executions sin eventos; la cuenta no tiene historial en la vertical) — ver §7.

## 7. History / G-HORIZON precheck (W6) — **PARTIAL_NEEDS_CREATED_ORDER**

- **API surface:** `Account.LookbackDaysExecutions/LookbackDaysOrders` existen como config de cuenta NT (fuente S del freeze §6.5, reflection 8.1.8.3 N1-R3); su VALOR runtime y el horizonte real de retención sólo son medibles desde dentro de NT (AddOn de ejecución) ⇒ bloqueado por §2.
- **Mientras el mercado está cerrado:** los candidates del feed persisten en Kafka (retención observada 168 h; p4 oldest 2382161) y el evidence sink del relay persiste (25 MB JSONL); los snapshots venue del AddOn de ejecución sobreviven vía reconciliation barrier al restart del bridge (journal reload verificado §8).
- **Historial de cuenta:** la cuenta GAU50 **no tiene ninguna orden/ejecución histórica de la vertical** (0 órdenes D6 acumuladas; executions primed-not-published). No hay contra qué ejercitar identidad de orden histórica. No se fabricó PASS ni se creó subsystem histórico (mandato).
- **Lo que queda para la ladder live:** con el primer ciclo G-E2E: medir retención real (`LookbackDays*`), retención `order.Name`/`Order.OrderId`/`ExecutionId` realtime↔historia↔restart, y pinar config. Exactamente los gates frozen G-ID-Retention + G-HORIZON.

## 8. Recovery without orders (W7) — **PASS**

Drills con cuenta flat y 0 working orders (2× bridge restart, kill -9 del transporte, reconexiones):

- **Bridge restart ×2** (`systemctl restart`): nuevo PID, `account session built` ≤1.2 s tras el arranque, journal reload `ListNonTerminal` = **0 registros** (sin phantom), probe reconectado con sesión nueva en **<1.5 s** desde el start del proceso, readiness re-evaluada fail-closed consistente (mismos blockers), `ambiguous_orders=0 mismatches=0 dropped_commands=0` en ambos ciclos.
- **Transport interruption:** SIGKILL del probe ⇒ server detecta EOF y dropea la conexión (0 sockets residuales); relanzamiento del probe ⇒ reconexión inmediata aceptada.
- **Cero command replay, cero submit físico** en todos los ciclos: el topic de comandos no existe, no hay fuente M1, y el capability gate es pre-journal (STOP_MARKET y cualquier tipo: rechazo antes de escribir journal).
- **NT restart:** NO ejecutado — requiere ciclo owner interactivo (ACL) y dejaría el feed lane caído durante el fin de semana; el gate físico nativo (orden venue-held visible post-restart) es G-STOP/G-E2E por diseño. Clasificado como pendiente de ventana, no como gap de este shot.

## 9. Closed-market fail-closed + G-REALTIME probe (W8) — **PASS (fail-closed correcto; G-REALTIME sigue indecidible-en-positivo)**

- Estado capturado hoy 14:42Z: último evento del stream `NQ:NQZ6` = QUOTE `event_ts 2026-10-02T21:38:25.95Z` (`receive_ts 2026-10-02T22:29:08Z`, Kafka p4 offset 5476458) ⇒ **edad del event_ts ≈ 17 h** >> bound 30 s ⇒ autoridad frozen clasifica **STALE** (`EVENT_TS_AGE_EXCEEDS_FRESHNESS_BOUND`, decay por timer F-S2-02) ⇒ 0 señales, admission refusa (`DENY_MARKET_NOT_FRESH`). **No se llamó G_REALTIME PASS** — es exactamente el comportamiento correcto con mercado cerrado.
- **Probe determinista G-REALTIME** (repetir tal cual cuando abra la sesión; sin investigación):
  `tool/scratch-weekend kafka-last -n 1 echo.futures.market-feed-candidates.v1` — imprime por partición `{offset, kafka_ts, event_ts}` del último candidato ⇒ `event_ts_age = now − event_ts`; FRESH ⇔ age < bound (30 s) con calendario activo. Herramienta efímera regenerable desde el repo (`scratch-weekend` patrón) o equivalente MCP (`consume` último offset p4). Evidencia base persistida: `evidence/w8-kafka-last-a.json`.

## 10. Next realtime window + Sunday admission (W9) — **evaluado por el ENGINE, no por suposición**

Harness sobre el materialization real (`v3/core/config/futures/gau50-eval-v1.json` embed, `AssertFrozenShape` + `Validate` PASS) y los evaluadores frozen reales (`windowOpen`, `applicableCaps`, `grossEnvelope`, `evaluateConsistency`):

- Ventana GAU50-EVAL v1: **L–V** `[00:00,15:50)` + `[17:10,23:59)` America/Chicago (half-open; days=[Mon..Fri]).
- Evaluaciones: SÁB hoy (cualquier hora) ⇒ **cerrada**; DOM 2026-10-04 16:55/17:05/17:30/20:00 CT ⇒ **cerrada** (weekday fuera de days 1–5); LUN 00:05 ⇒ abierta; LUN 15:49 ⇒ abierta; **LUN 15:50 ⇒ cerrada (edge exacto)**; LUN 16:15 ⇒ cerrada; LUN 17:10/17:15/23:58 ⇒ abierta; SÁB siguiente ⇒ cerrada.
- **CME reopen:** domingo 2026-10-04 **17:00 CT** (el feed calló viernes ~16:38 CT post-cierre; Globex semanal abre dom 17:00 CT).
- Respuestas: **A. G-REALTIME sólo** — domingo sirve para certificar feed FRESH (probe §9) porque el transporte de mercado no depende de la ventana; **NO** sirve para el ladder: la admission del engine DENIES Sunday new-risk (doble capa: weekday fuera de days + ninguna sesión GAU50 domingo).
- `NEXT_REALTIME_WINDOW` (realtime + admisión): **lunes 2026-10-05 00:00 CT (05:00Z)** — ventana 1 `00:00–15:50 CT`; ventana 2 `17:10–23:59 CT`; edge de forma 23:59–00:00 excluido (documentado Shot 1 §7.6). Reopen del feed 31.5 h antes (dom 17:00 CT) permite pre-certificar G-REALTIME y calentar.

## 11. First physical certification scenario (W10) — **FULLY_DEFINED**

Resuelto de las autoridades frozen (nada elegido por este shot):

- **Escenario:** G-E2E del Design Freeze §14.13 — UN ciclo controlado owner-autorizado en la GAU50: **entrada MARKET + instalación de la protectora STOP_MARKET venue-held + tighten monotónico por cancel/replace + cancel + flat**, con drill de restart/reconnect durante la protectora working, fills dedup por `ExecutionId`, transiciones de journal VENUE_BOUND/TERMINAL observadas y **0 unknown live orders al cierre**.
- **Cuenta/instrumentos:** `E2T-GAU50-01` ↔ `RJARA114411201551` (NT `NQ 12-26` / Echo `NQZ6` — ambas identidades aceptadas por el adapter).
- **Límites:** cap GROSS account-wide **6** (engine verificado: 6 abiertas ⇒ breach; 5 ⇒ room para 1); ventana L–V (§10); SL/TP owner day 1/2 = **2000/1500 USD** (modelo D4 frozen, config de run); `(E2T-GAU50-01, client_order_id)` dedup, `sameIntent` con nivel de stop; no-blind-retry.
- **Side/qty/precio:** NO son parámetros humanos — salidas runtime del camino frozen Strategy(S1/S2)→GerardMM dentro de esos límites (diseño: nadie elige la orden).
- **Configuración de run** (selección S1/S2 + EconomicPlanRowSet/Scaling + warm-up corpus + RUN_START): es la preparación operacional DENTRO de la ventana ya registrada por el intento 1 (§17.2), instanciada de las autoridades frozen — **no es un parámetro financiero faltante ni decisión owner nueva**.
- `MISSING_PHYSICAL_PARAMETERS = NONE`. Gates owner vigentes: OD-D6-1 (AUTHORIZED, sin consumir) y OD-D6-4 (standing, ciclo de instalación).

## 12. Provider gates (W11) — **PASS (engine operativo; DENY esperado hoy)**

- Entitlement ALLOWED (ETCD RO read-back); programa EVALUATION; binding↔RuleSet match (GAU50-EVAL v1/EARN2TRADE/GAU50) verificado por `Validate()`.
- Ventana: tabla §10 (hoy DENY `WINDOW_CLOSED` — doble fail-closed con freshness).
- Capacity: cap 6 con semántica de envelope GROSS account-wide (evaluada con buckets reales del evaluador).
- Risk-state: DLL 1100 ABSOLUTE basis **PREV_DAY_CLOSE** flatten; EOD DD 2000 EOD_TRAILING basis **INITIAL_BALANCE** flatten (F-S2-06); con snapshot de fin de semana (PnL 0, balances 0) ⇒ sin breach ⇒ los deny de hoy son sólo de ventana/freshness, como corresponde.
- Consistency 30%: `UNDETERMINED` con evidencia nula/cero (jamás fabricada en compliance; jamás gatea), `BREACHED` en 31 % (boundary `>=` confirmado por fuente verbatim). `ReservationRevalidate` path intacto (código frozen + tests; su ejercicio físico es del ladder).
- `PROVIDER_RULE_VIOLATIONS = 0` (no hubo orden que evaluar).

## 13. Performance precheck (W12) — **PARTIAL**

Medido físicamente hoy (sin órdenes):

| Métrica | Valor | Nota |
|---|---|---|
| hello → observación en Kafka (lane→gate→publish) | **281 ms** | incluye batching producer 100 ms + append |
| bridge start → lane re-acepta sesión (reconnect recovery) | **<1.5 s** | 2 restarts medidos |
| barrier hasta fail-closed sin venue snapshots | **7.7 s** | Connect+reconcile wait (CommandTimeout acotado) — desaparece con el AddOn real |
| bridge RSS / CPU steady-state | ~30 MB / 0.1 % | presupuesto de proceso holgado |
| auth+fencing drill RTT | sub-segundo | badtoken→EOF inmediato |

**DEFERRED_TO_LIVE_EGRESS** (requieren feed vivo u órdenes; fabricarlos sería evidencia falsa): ingest p50/p95/p99 de mercado, event-to-bar, Signal→delivery, MM decision, admission/revalidation latency, costo fsync M2 (0 registros hoy), latencias de orden/comando. El lane de mercado mantiene el baseline N1 (feed byte-unchanged).

## 14. Sim rehearsal (W13) — **SKIP**

No existe soporte limpio: el rehearsal exigiría instalar/configurar el AddOn en el perfil owner (el mismo paso bloqueado por ACL) o reconfigurar el feed AddOn, mutando el vertical certificado para una prueba que por mandato no cuenta como evidencia. Implementar arquitectura de simulador estaba explícitamente prohibido. `SKIPPED_NOT_SUPPORTED_CLEANLY`.

## 15. Cambios de infraestructura (todas DEV, reversibles, con rollback documentado)

| Delta | Detalle | Rollback |
|---|---|---|
| ETCD DEV +3 claves | `futures-bridge/ntx/auth-token` (nuevo, secreto 64 hex), `futures-bridge/journal-root`, `futures-bridge/accounts=E2T-GAU50-01` | al cierre de ESTE shot: unidad parada y `futures-bridge/accounts` ELIMINADA (vuelve a G-EGRESS-0 sin sesiones); token y journal-root quedan (inertes sin sesiones) |
| Deployment | release `40102ea5` + unidad `echo-futures-bridge` (disabled) + `var/futures-bridge/journal` | stop + borrar unidad/release; relay feed `170a4581` INTACTO siempre |
| Bundle owner | `C:\Temp\` + `owner-install/weekend-20261003/` + checklist | borrar archivos (el perfil owner no fue tocado) |
| Producto | **NINGUNO** (0 commits; worktree limpio verificado al cierre) | n/a |

## 16. Regresión (scoped, mismo SHA, corrida hoy tras el work)

`go test -race -count=1` @ `40102ea5` (GOTMPDIR en disco): `v3/futures-bridge/...` **15 pkgs ok, BRIDGE_EXIT=0** · `v3/sdk/futures/...` **ok, SDK_EXIT=0** · `v3/core/internal/functions/...` ok · `v3/core/config/futures/...` ok · `v3/core/futuresvertical/... -timeout 30m` ok (VEREDICTO en el close block). Sin shadow-compile nuevo (source byte-idéntico a Shot 3; hashes §2). Herramientas scratch (probe/harness) eliminadas; tree limpio.

## 17. LIVE-ONLY REMAINING (lo único que queda, en orden)

1. **Ciclo owner W1** (OD-D6-4 standing, ~3 min): checklist `C:\Temp\OWNER-CHECKLIST-W1.md` — instala AddOn de ejecución + actualiza feed AddOn + config JSON + restart NT. Recomendado dom previo al reopen o lunes pre-ladder.
2. **Domingo ≥17:00 CT (opcional, sin riesgo):** certificar G-REALTIME con el probe §9 (feed ya fluyendo; sin bridge ni órdenes). Si el feed real midiera stale ⇒ OD-D6-3 conditional escalation.
3. **Lunes 00:00–15:50 CT (o 17:10–23:59 CT), dentro de la ventana:** habilitar sesión (`futures-bridge/accounts`) + arrancar unidad → AddOn real conecta (supersede automática de cualquier sesión vieja) → barrier completa con venue snapshots reales → verificar `SubmissionCapabilitiesReady`/readiness → configurar run (warm-up + RUN_START desde las autoridades frozen) → ladder congelado G-REALTIME(positivo) → G-STOP → G-ID-Retention → G-HORIZON → G-E2E (+ drill reconnect) → G-PERF.
4. GATES owner: OD-D6-1 vigente (AUTHORIZED, sin consumir). No emitir `EF_D6_E2E_PASS` hasta ladder completo.

---

## 18. Final handoff

```text
D6_PHYSICAL_READINESS_NO_EGRESS =
READY (con ciclo owner de instalación W1 preparado y checklisteado — único paso pendiente por diseño, OD-D6-4)

BASELINE_SHA:
40102ea5a44be9a618ac12529e6f0e9fdfd46d34

FINAL_SHA:
40102ea5a44be9a618ac12529e6f0e9fdfd46d34 (cero commits; deltas = config-act DEV + deployment bridge + bundle owner)

EXECUTION_ADDON_INSTALLED:
BLOCKED_OWNER_ACTION (ACL owner re-probada hoy; bundle byte-verificado en C:\Temp + checklist; ~3 min)

EXECUTION_LANE:
PASS (lado bridge/transporte físico: listener :9771, auth constant-time, seq discipline, fencing, path gate→Kafka probado con sesión auto-etiquetada; endpoint AddOn pendiente del ciclo W1; barrier fail-closed sin venue snapshots demostrado)

ACCOUNT_BINDING:
PASS (RESOLVED 1/8 vivo; NT Account.Id "3" == hint ETCD, 4.ª sesión consecutiva; sin drift; identidad de negocio intacta)

CURRENT_NT_ACCOUNT_ID:
3

SESSION_RECONNECT:
PASS (nueva identidad de sesión por conexión + seq 0 aceptada, F-S2-01; 8+ reconnects físicos; reconnect AddOn-binario en G-E2E por diseño)

SESSION_FENCING:
PASS (server cierra la conexión supersedada al autenticar la nueva — log "session superseded … fenced"; segunda barrera del adapter congelada por tests; frame en-vuelo físico en G-E2E)

ACCOUNT_OBSERVATION:
PASS (feed lane real: account/positions/orders con account RESOLVED y balances weekend-demo 0/0/0/0/0; serialization frozen; bridge publisher SESSION→Kafka verificado; executions primed-not-published; 0 datos fabricados)

G_HORIZON_PRECHECK:
PARTIAL_NEEDS_CREATED_ORDER (cuenta sin historial de la vertical; LookbackDays* runtime medible sólo desde NT; retención Kafka 168 h + evidence sink persistente observadas; sin subsystem histórico creado)

RECOVERY_PRECHECK:
PASS (2× bridge restart con journal reload 0-phantom y reconnect <1.5 s; SIGKILL transporte → EOF drop → reconexión; 0 command replay; 0 phantom orders; 0 journal corruption; NT restart reservado a ventana/owner)

CLOSED_MARKET_FAIL_CLOSED:
PASS (STALE por edad 17 h >> 30 s, decay F-S2-02, 0 señales, admission refusa; G_REALTIME sigue FAIL-por-calendario del intento 1, NO re-certificado hoy)

NEXT_REALTIME_WINDOW:
feed realtime: dom 2026-10-04 17:00 CT (reopen CME) · primera ventana ADMISIBLE (realtime+new-risk): lun 2026-10-05 00:00–15:50 CT (edge 15:50 exacto; evening 17:10–23:59 CT; días L–V)

SUNDAY_G_REALTIME_POSSIBLE:
YES (G-REALTIME es independiente de la ventana de admission; probe determinista §9 listo)

SUNDAY_PHYSICAL_LADDER_POSSIBLE:
NO (engine evalúa Sunday fuera de days 1–5 ⇒ WINDOW_CLOSED ⇒ DENY de new-risk todo el domingo; respuesta W9 = A)

FIRST_PHYSICAL_CERT_SCENARIO:
FULLY_DEFINED (G-E2E freeze §14.13: MARKET entry + STOP_MARKET protectora venue-held + tighten cancel/replace + cancel + flat, drill de restart con protectora working, 0 unknown live orders; NQ/NQZ6, cap 6, SL/TP 2000/1500 day1; side/qty = output frozen de Strategy+GerardMM, nunca parámetro humano)

MISSING_PHYSICAL_PARAMETERS:
NONE (run-config de ventana = trabajo Manager instanciado de autoridades frozen; no es decisión owner nueva)

PROVIDER_RULESET:
PASS (GAU50-EVAL v1 ACTIVE, 7 SourceRefs, guard 16 mutaciones verde; ventana/cap/consistency/risk-state evaluados por los evaluadores reales; DENY sábado correcto)

PERFORMANCE_PRECHECK:
PARTIAL (281 ms publish lane→Kafka; <1.5 s reconnect; 7.7 s barrier fail-closed; 30 MB RSS; order/feed-dependent → DEFERRED_TO_LIVE_EGRESS)

LIVE_ONLY_REMAINING:
(1) ciclo owner W1 instalación AddOns+config (checklist C:\Temp) · (2) G-REALTIME positivo en ventana (probe listo; dom opcional) · (3) habilitar sesión+arrancar bridge dentro de ventana → barrier con venue real → run config (warm-up+RUN_START) → ladder G-STOP→G-ID-Retention→G-HORIZON→G-E2E(+drill)→G-PERF · (4) G-HORIZON/G-ID-Retención necesitan la primera orden (PARTIAL_NEEDS_CREATED_ORDER)

PHYSICAL_ORDERS_SENT:
0

PHYSICAL_ORDERS_MODIFIED:
0

PHYSICAL_ORDERS_CANCELLED:
0

WRONG_ACCOUNT_EVENTS:
0

DUPLICATE_PHYSICAL_SUBMITS:
0

BLIND_RETRIES:
0

UNRESOLVED_AMBIGUOUS_SUBMITS:
0

PROVIDER_RULE_VIOLATIONS:
0

COMMAND_FRAMES_RECEIVED_BY_ANY_CLIENT:
0 (alerta estructural del probe; el bridge jamás escribió un comando)

REGRESSION:
PASS @ 40102ea5 (bridge 15 pkgs EXIT=0; sdk EXIT=0; core functions+config EXIT=0; futuresvertical -timeout 30m EXIT=0) — veredicto por suite en el project note

OWNER_DECISION_REQUIRED:
NONE (OD-D6-1 AUTHORIZED vigente sin consumir; OD-D6-4 standing cubre el ciclo de instalación; OD-D6-3 conditional sólo si G-REALTIME midiera stale en ventana)

NEXT_MANAGER_ACTION:
Re-despachar el ladder físico congelado en la ventana lun 2026-10-05 00:00–15:50 CT con la secuencia §17 (ciclo owner W1 puede anticiparse dom ≥17:00 CT para aprovechar el reopen y pre-certificar G-REALTIME con el probe §9). No emitir EF_D6_E2E_PASS hasta ladder completo.
```

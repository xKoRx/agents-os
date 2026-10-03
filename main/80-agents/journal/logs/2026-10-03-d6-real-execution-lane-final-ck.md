# Change Log — 2026-10-03 — D6 Real Execution Lane FINAL C–K post config fix (REMEDIATION_REQUIRED; C1 cerrado como código)

- **Fecha:** 2026-10-03
- **Entidad:** [[Echo Futures]]
- **Tipo:** updated + code-fix
- **Archivo(s):**
  - `10-projects/Echo Futures/artifacts/d6-real-execution-lane-20261003/D6-REAL-EXECUTION-LANE-NO-EGRESS.md` (append §POST CONFIG FIX / FINAL C–K: C0 contradicción runtime-vs-atestación con cadena de evidencia, C1 fix, D–I, J–L, /close; intentos 1 y retry preservados íntegros)
  - `xKoRx/echo` `origin/feature/d6-shot1-execution-vertical` `40102ea5..d361008b` (FF, pusheado): `v3/futures-bridge/addon-ninjatrader/EchoExecutionAddOn.cs` (LoadConfig fail-closed, 11 líneas) + `config_guard_test.go` (nuevo)
  - `10-projects/Echo Futures/Echo Futures.md` (nueva entrada de bitácora D6: FINAL C–K POST CONFIG FIX)
  - `80-agents/journal/agent-runs/2026-10-03-zcode-glm53-d6-lane-final-ck.md` (nuevo)
  - `80-agents/journal/sessions/raw/2026-10-03-d6-lane-final-ck-raw.md` (nuevo L0 compacto)

## Motivo

- Nueva verdad física del Owner: config corregida al destino (SHA `9ca3fddc…` en ambos extremos, `ntx_port = 9771` parseado) y NT reiniciado después. Despacho de certificación final C0–M one-shot NO-EGRESS con mandato de STOP si el runtime contradecía la corrección.

## Resolución aplicada

- **C0 = FAIL con contradicción exacta:** NT boot físico 22:13:09Z (PID 11412→4576; hello feed `f2756ae6…`); bridge release `40102ea5` (PID 2155952, binario `484b550b…`) LISTENING `*:9771` desde 22:29:32Z; el EchoExecutionAddOn del PID 4576 hizo **cero intentos de conexión en ≥18 min** (diseño: primer dial ~1 s tras Active, retry 10 s ⇒ ≥100 ciclos esperados; muestreo dev-win multi-ventana + `ss` servidor); barrier fail-closed a los **10.015 s** (3.ª demostración). Fuente `C:\Temp` re-verificada por agente (`9ca3fddc…` ✔). Hipótesis restantes indistinguibles agente-side (ACL 7.ª/8.ª: log NT, StartTime, tasklist /m denegados): (a) config efectiva sin puerto dialable, (b) exec AddOn no cargó este boot. **STOP por mandato C0.**
- **C1 = PASS como código (commit `d361008bfe4aa54fe3d8b6380d290bf92e1f1c08`, push FF verificado):** `LoadConfig` valida host/port/token/account/contracts/intervals; en fallo resetea `ntxHost/ntxPort/authToken` a inertes y loguea `config FAILED` (Error) ANTES de cualquier log de éxito; test estructural `TestExecAddOnConfigLoadFailsClosedOnInvalid` (paquete 5/5 PASS); `go build` OK; shadow-compile físico 8.1.8.3 EXIT=0 (0 errores, 3 warnings preexistentes, bytes `72d97ad6…` byte-verified). SUPERSEDE el residual §R8 del retry. Pickup físico pendiente al próximo ciclo de instalación owner (el AddOn instalado sigue siendo `b2a29a36…`).
- **D–I:** exec-side NOT_RUN/FAIL (sin sesión nunca; 0 hellos `[ntx]`, 0 sockets; probe weekend listo y NO usado). E/F feed-side vivos: RESOLVED 1/8, `RJARA114411201551` = id `"3"` == hint ETCD (7.ª sesión consecutiva). J: `G_HORIZON = PARTIAL_NEEDS_CREATED_ORDER`. K: readiness 8 blockers exactos 0/0/0; STALE ≈24 h (replay estático del boot corto `de38c5f2` no refresca — F-S2-02); NEW_RISK_READY = NO. L: `SUNDAY_G_REALTIME_RUNBOOK = READY` (feed-lane-only, independiente del fix). M: ladder READY con gate 0 actualizado (diagnóstico owner + pickup C1).
- **Teardown a G-EGRESS-0 probado:** unidad inactive+reset-failed+disabled, `:9771` FREE, clave de sesión eliminada con ciclo guardado (pre-read exacta → delete → read-back ausente → cross-check MCP RO **21 claves == baseline**), journal M2 0 registros, **0 COMMAND_FRAME** (histograma de msgs verificado). `PHYSICAL_ORDERS_SENT = MODIFIED = CANCELLED = 0` (3.er intento consecutivo).

## Validación

- Evidencia conductual decisiva contra LISTEN activo (dial exitoso = ESTABLISHED persistente por backlog del kernel — no hay sampling que se escape), cross-verificada con SSH dev-win-operator, ETCD crudo (probe weekend: etcd-get/put --expect-absent/meta + scratch-del), journalctl bridge/relay, sink `evidence.jsonl` sin máscara, Kafka MCP (`kafka-last` re-ejecutado hoy) y shadow-compile físico. OD-D6-1 AUTHORIZED vigente sin consumir. Sin secretos persistidos (token 64 B sólo por meta/longitud).

## Compartibilidad

- Owner: 1 ciclo diagnóstico+fix — (1) log NT del boot 19:13 local: ¿`config loaded: ntx=****.161:9771` + `started`? ⇒ escalar red/perfil NT; ¿líneas EchoExecutionAddOn ausentes? ⇒ el AddOn no cargó: re-verificar los 2 .cs en `AddOns\`, recompilar NinjaScript, revisar `C:\Temp\compile-errors.txt`; (2) en cualquier rama reinstalar `EchoExecutionAddOn.cs` desde HEAD `d361008b` (bytes `72d97ad6…`) para que una config fatal sea visible; (3) restart NT con bridge en marcha. Señal agente-observable: ESTABLISHED→:9771 + hello `[ntx]` ≤10 s.
- Manager: REMEDIATION_REQUIRED ⇒ no certificar lane ni ejecutar ladder. Domingo 2026-10-04 ≥17:00 CT: G-REALTIME certificable (feed-lane-only, NO depende del fix, runbook §M intento 1). Con la señal: re-despachar C–K (~5 min en ventana) → ladder congelado §N lun 2026-10-05 00:00–15:50 CT. No emitir `EF_D6_E2E_PASS`.

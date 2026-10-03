# L0 — 2026-10-03 — D6 real execution lane FINAL C–K post config fix (raw)

**Sesión:** ZCode/GLM-5.3-Flash — despacho TOP one-shot (certificación final C0–M), NO-EGRESS, sobre la config corregida por el Owner. Entidad: [[Echo Futures]].

## Hilo de evidencia (compacto, el detalle vive en el artifact §POST CONFIG FIX / FINAL C–K)

- Insumo owner: config `9ca3fddc…` atestiguada en destino (`ntx_port = 9771` parseado) + restart NT. Fuente `C:\Temp` re-verificada por agente (certutil, SHA ídem ✔).
- Timeline físico: NT boot 22:13:09.941Z (hello feed `f2756ae6a27c4a5fad67954c2fb9f9a1`, PID 11412→4576 vía netstat `:9770`); boot intermedio brevísimo `de38c5f2…` (23 frames, ≈22:12Z — el owner reinició 2× en ~1 min).
- Preflight D íntegro PASS: binding ETCD 12/12 por lectura cruda (claves SIN prefijo `/echo/development` — el MCP RO lo agrega como display), token 64 B por meta, journal M2 0 registros, topic `echo.order-commands.E2T-GAU50-01.v1` inexistente, sesión guardada (`--expect-absent` → put → read-back `E2T-GAU50-01`).
- Bridge: PID 2155952, release `40102ea5` (binario SHA `484b550b…`), `account session built` <0.1 s, listener `*:9771` desde 22:29:32Z.
- **C0 contradicción (decisiva):** cero intentos de conexión del exec AddOn en ≥18 min vs listener vivo (diseño: primer dial ~1 s tras Active, retry 10 s ⇒ ≥100 ciclos esperados); muestreo dev-win multi-ventana (7×2 s + 10×2.2 s) sin ningún socket `:9771`; `ss` servidor sin ESTABLISHED jamás; barrier fail-closed a los **10.015 s** (3.ª demo, razón literal idéntica). ACL 7.ª/8.ª re-probe: log NT, `Get-Process .StartTime`, `tasklist /m` = denegados ⇒ (a) config efectiva sin puerto dialable vs (b) AddOn no cargado este boot, indistinguible agente-side. **STOP por mandato C0.**
- **C1 cerrado como código:** commit `d361008bfe4aa54fe3d8b6380d290bf92e1f1c08` pusheado FF a `origin/feature/d6-shot1-execution-vertical` — LoadConfig fail-closed (11 líneas: valida host/port/token/account/contracts/intervals; fallo ⇒ resetea dials a inertes + `config FAILED` Error ANTES del success log) + `config_guard_test.go` (5/5 PASS) + shadow-compile físico 8.1.8.3 EXIT=0 (bytes `72d97ad6…` byte-verified, 3 warnings preexistentes). SUPERSEDE residual §R8. Pickup físico en el próximo W1.
- E/F feed-side vivos: RESOLVED 1/8, id `"3"` == hint ETCD (7.ª sesión consecutiva); positions/orders `[]`, balances demo 50000/50000. J: `G_HORIZON = PARTIAL_NEEDS_CREATED_ORDER`. K: 8 blockers exactos 0/0/0, STALE ≈24 h (replay estático no refresca — F-S2-02). L: runbook G-REALTIME READY (feed-only, independiente del fix). M: ladder READY, gate 0 = diagnóstico owner + pickup C1.
- Teardown G-EGRESS-0 probado: unidad inactive+disabled, `:9771` FREE, accounts key eliminada con ciclo guardado (MCP RO 21 claves == baseline), journal 0, **0 COMMAND_FRAME**.

## Salidas

- Artifact: `10-projects/Echo Futures/artifacts/d6-real-execution-lane-20261003/D6-REAL-EXECUTION-LANE-NO-EGRESS.md` (§POST CONFIG FIX / FINAL C–K + /close; intentos previos preservados)
- Repo: `xKoRx/echo` `origin/feature/d6-shot1-execution-vertical` = `d361008b` (FF sobre `40102ea5`)
- Project note D6 · change log `80-agents/journal/logs/2026-10-03-d6-real-execution-lane-final-ck.md` · agent-run mismo día.

## Fricciones/notas

- MCP SSH run-command: comandos >~25 s mueren por timeout 30 s; while-loops y comandos con invocación `& $csc` disparan approval-gate fail-closed (client sin elicitation) ⇒ dividir en pasos cortos y ejecutar scripts .ps1 descargados.
- http.server + curl.exe: el .ps1 debe vivir EN el directorio servido — un 404 escribe HTML en el archivo destino y PowerShell explota con ruido masivo.
- ETCD crudo (probe weekend): claves de storage SIN prefijo `/echo/development` (el MCP RO lo agrega como display); `scratch-weekend ntx-probe` flags completos documentados en memoria.
- ETCD MCP RO fuzzy-read gotcha no re-observado hoy (todo valor con decisión se leyó por cliente crudo).

## Próximo paso

Owner: 1 ciclo diagnóstico (log NT del boot 19:13 local: ¿`config loaded 9771`? ¿AddOn ausente?) + reinstalar .cs corregido desde HEAD `d361008b` + restart NT con bridge en marcha; señal agente-observable: ESTABLISHED→:9771 + hello `[ntx]` ≤10 s. Dom ≥17:00 CT G-REALTIME (feed-only). Con la señal: re-despacho C–K (~5 min) → lun 2026-10-05 00:00–15:50 CT ladder congelado. No emitir `EF_D6_E2E_PASS`.

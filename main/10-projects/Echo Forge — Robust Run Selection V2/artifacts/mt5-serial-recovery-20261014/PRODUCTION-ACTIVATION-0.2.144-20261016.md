# PRODUCTION ACTIVATION 0.2.144 — Real drain certification (2026-10-16)

**STATUS: FORGE_OPERATIONAL_SAFETY_PRODUCTION_PASS**

Sesión one-shot ZCode/GLM-5.3-Flash en daedalus (mandato "ECHO FORGE — FINAL PRODUCTION ACTIVATION · RELEASE 0.2.144 · REAL DRAIN CERTIFICATION", manager GPT-6). Baseline symphony `e4d37ffd82a6c4a0c4e2bdddef5afaf6c363089c` verificada en master == origin/master; stager `32e1554` == origin/master. Sin rediseño, sin features nuevas, sin tocar Echo, sin reboot, sin autologon, sin repetir wave3t.

## Resultado

La primera release **con trigger de drain** (0.2.144) está activa en producción (worker-kronos) y su adopción + el ciclo de drain completo quedaron certificados físicamente:

- **Adopción de la primera release por el supervisor drain-aware** (transición de una sola vez del binario pre-trigger 0.2.143).
- **Drain real con activity en vuelo**: la actividad terminó íntegra después de la señal, el worker salió limpio (exit 0), el supervisor relanzó 0.2.144 y el host quedó sano.
- **Canary guard efectivo con el binario instalado**: reuso rechazado con error tipado y canario con SourceKey nuevo corriendo la ruta física.

## 1. Preflight (idle físico demostrado)

- Git limpio y sincronizado (symphony `e4d37ff`, stager `32e1554`, ambos == origin).
- Worker 0.2.143 sano: pid 29292, `Path` bajo `releases\0.2.143`, vivo continuo desde 23:44Z del 15-oct.
- Stager `committed` (activación `b6a3a8e2` 0.2.143), `StagerReconcile` Last Result 0 cada minuto.
- Supervisor drain-aware instalado y verificado: script SHA256 `8DD18240…27EB` (== certificación 2026-10-16 previa), supervisor único pid 6292 desde 02:02:07Z, cero líneas taskkill de su era.
- Temporal sin activities MT5: última `activity.ok` 00:12:12Z (canario r2 0.2.143), >3h de silencio al momento del cambio; 0 workflows `MT5BacktestArtifactWorkflow` Running; 0 procesos terminal64/MetaEditor64/metatester64.
- Leases/ownership sin trabajo pendiente: 124 registros `echo-forge/mt5/logical-jobs/`, **todos** `state=FAILED` (terminales), 0 vivos.

## 2. Release 0.2.144

- Publicación canónica: `./deploy_release.sh --release-only 0.2.144` en daedalus desde árbol limpio (`vcs.modified=false`), plataformas linux-amd64 + windows-amd64, deployer-watcher en screen `deployer` publicó a MinIO `deploy/` (telemetría OTLP degradada 192.168.31.45:4317, no bloqueante — preexistente).
- Manifiesto: `deploy/manifest.json` v0.2.144, windows `bin/sqx-mt5-worker.exe` size 37,520,384 SHA256 **`ba4948d45b94a71c78921bfa4be8e76a6f904982e575b58c17f1b81c91ad904e`**. Cadena verificada: manifiesto local == binario local == objeto MinIO == binario staged en kronos (Get-FileHash `BA4948D4…904E`).
- Commit de manifiesto: `5a66bb6` "chore(release): manifest 0.2.144 (windows sqx-mt5-worker ba4948d4)" — pusheado a master.
- Rollout del script: "Release PUBLICADA; rollout NO VERIFICADO (0/3)" — gotcha documentado de daedalus (SSH keyless BatchMode); verificación física realizada por SSH propio. La flota Linux corre SQX worker en contenedores (`sqx-ulab-*-0`, pollers de `sqx-main-queue` saludables 3/3); `/opt/symphony/CURRENT` de zeus es legacy preexistente, fuera del alcance del mandato.
- Staging en kronos ≤60s: `StagerReconcile` stageó `releases\0.2.144`, CURRENT→0.2.144, y el supervisor registró **"evento de drain Global\echo-forge-sqx-mt5-worker-drain inaccesible; activacion de release 0.2.144 pendiente (worker vivo se conserva, sin kill)"** — exactamente la transición documentada (worker pre-trigger conservado). Stager quedó `phase=signaled` (activación `5e930dee`).

## 3. Parada controlada del worker 0.2.143 (transición de una sola vez)

- **Vía graciosa intentada y no viable desde este transporte**: CTRL_C por consola (AttachConsole+GenerateConsoleCtrlEvent) requiere ejecutar en la sesión interactiva; toda vía remota vive en sesión 0 y Task Scheduler rechaza lanzar tareas `/IT` desde ahí (0x80070490 "Element not found", `schtasks /run` y `Start-ScheduledTask`). La vía graciosa del propio supervisor (SetEvent) exige el trigger que 0.2.143 no tiene.
- **Fallback ejecutado (autorizado por el mandato): parada forzada estrictamente limitada al PID 29292** (`Stop-Process -Id 29292 -Force`), con idle re-verificado al momento (último log del worker 00:12:12Z, 0 GUI, 0 activities en vuelo, target confirmado por `Path` antes de parar). **Registro: NO fue drain.** El recovery de diseño cubre esta vía (singleton `previousWorkerDeadProven` → recuperación de leases stale + same-host, certificada en test B del hardening 15-oct).
- Adopción: supervisor lanzó 0.2.144 en ≤40s (03:30:01Z "lanzando release 0.2.144", pid 19864). Cero taskkill del supervisor en toda la operación.

## 4. Verificación de producción (FASE 3)

- Worker Windows **0.2.144** pid 19864 con `Path` bajo `releases\0.2.144\bin` y SHA del binario vivo == manifiesto (`BA4948D4…904E`).
- Startup del worker: "Singleton sqx-mt5-worker adquirido", **"Trigger de drain de adopción de release observando"** (evento `Global\echo-forge-sqx-mt5-worker-drain`), `env=production`, "Ownership global MT5 compuesto".
- Un solo worker (1 proceso `sqx-mt5-worker`), un solo supervisor (pid 6292; los "2 powershell" de la primera pasada eran auto-match del propio comando de verificación).
- Pollers Temporal (namespace `sqx-prop`, verificado con helper Go `mt5ops`, no con el MCP cuyo perfil apunta a otro namespace): `sqx-mt5-queue` → `19864@worker-kronos`; `sqx-main-queue` → 3 pollers de flota; 0 workflows MT5 Running.
- Stager: activación `5e930dee` 0.2.143→0.2.144 **`phase=committed`**, `current=0.2.144`, `running.release=0.2.144` (observado 03:31:01Z). **CURRENT = RUNNING = 0.2.144.**
- Reconcile posterior idempotente: `StagerReconcile` Last Result 0 en cada minuto durante toda la sesión, CURRENT estable sin drift.

## 5. Test real de drain (FASE 4) — activity en vuelo

Backtest MT5 auténtico y acotado: workflow `MT5BacktestArtifactWorkflow:smoke-drain-02144-20261016` (run `01a142cb-b020-7947-9184-42a6516c1fe9`), EX5 durable byte-exacto del finalista 89171ea6 (copia server-side, etag `6f5d8831…` == SHA256 conocido `92b025f2…b7f20`), SourceKey NUEVO `smoke-drain-02144-20261016/08_mt5_ex5/final-89171ea6.ex5`, NDX_SQX H1 2025.07.01–2026.10.14, `smoke_canary=false`.

1. `activity.start` 03:40:07Z; terminal64 pid 5900 + metatester64 pid 34148 físicamente vivos desde 00:40 local.
2. Señal de drain **como la haría el supervisor**: `OpenEventW`+`SetEvent` sobre `Global\echo-forge-sqx-mt5-worker-drain` → `drain-senalado=True` (el evento existe: lo crea el worker 0.2.144 — el 0.2.143 nunca pudo ser señalado).
3. **El proceso NO terminó mientras la actividad continuaba**: worker-vivo=True y tester-vivo=True tras la señal (verificado a +5s y +70s); la actividad siguió ~2.5 min más.
4. `activity.ok status=success` 03:44:13Z — HTM **2,025,096 B** + `.tester.ini` + `.terminal.log` + `.tester.log` 11,651,354 B + `.agent.log` 12,922,508 B durables en `sqx-strategies/smoke-drain-02144-20261016/09_mt5_backtest/` (prefijo nuevo).
5. Cierre limpio: supervisor "worker pid 19864 termino: **uptime=861s exitcode=0**"; SDK "Stopped Worker … WorkerID 19864@worker-kronos@". Leases/ownership liberados: 124/124 registros terminales, 0 vivos.
6. Recuperación del supervisor: backoff 2s → relanzamiento 03:44:26Z pid **5308**; singleton re-adquirido, trigger observando, poller `5308@worker-kronos` de vuelta al primer chequeo; 0 procesos GUI residuales.

## 6. Canary guard (FASE 5) — con el binario efectivamente instalado

- **Regresiones del guard en el host**: binario de test GOOS=windows compilado del mismo árbol instalado (HEAD `5a66bb6`, código del binario 0.2.144 == `e4d37ff`), subido con hash verificado (`ffb16de8…4795`), corrido en worker-kronos: **3/3 PASS** — `TestMT5ArtifactBacktest_SmokeCanaryReuseRejected`, `_RegularReuseUnaffectedByCanaryGuard`, `_SmokeCanaryWithoutHTMRunsPhysical`. (Nota: el primer intento falló por fixture `mt5-export.htm` ausente en la ruta relativa `..\..\..\` del binario — resuelto recreando la estructura `guardroot\a\b\c\`; fallo de transporte del fixture, no del guard.)
- **Reuso rechazado con error tipado (físico)**: canario `smoke_canary=true` sobre el SourceKey del canario 0.2.143 (`smoke-canary-02143-20261015/08_mt5_ex5/final-89171ea6.ex5`) → `activity.error` 03:47:38Z con el sentinel `smoke canary source reuse: … ya tiene HTM durable reutilizable … despache con un SourceKey nuevo` (`smoke_canary_source_reused`, `retryable: false`, Attempt 1), **sin spawn físico** (run `01a142d2-922f-79d5-bf84-1a397cec4cb0`).
- **SourceKey nuevo ejecuta la ruta física**: canario `smoke-canary-02144-20261016` (run `01a142d3-8cec-7164-a63d-eef970a1b861`) → backtest físico real 03:48:45Z→03:52:37Z (~3m52s), `activity.ok status=success` 03:52:56Z, HTM **2,027,156 B** + 4 journals durables en `smoke-canary-02144-20261016/09_mt5_backtest/`. La evidencia Gate B de slot-1 permaneció PASS (build 6230==htm_build) sin refresco de `checked_at` — correcto: con evidencia PASS vigente el canario no re-certifica (sólo lo hace sobre UNPROVEN); la prueba física nueva queda demostrada por el HTM nuevo.
- Wave3t y los artefactos del canario 0.2.143 intactos (sólo prefijos nuevos); no se repitió wave3t.

## 7. Estado final

- Producción: worker-kronos con **un solo worker 0.2.144** (pid 5308, SHA `BA4948D4…904E`), un solo supervisor (pid 6292), stager `committed` (activación `5e930dee`), CURRENT=RUNNING=0.2.144, `StagerReconcile` Last Result 0, pollers Temporal saludables, 0 activities interrumpidas por el despliegue.
- Supervisor log: cero taskkill en toda la era drain-aware (las 8 líneas del log son las adopciones 0.2.141→142 y 0.2.142→143 del supervisor v2.1, 15-oct, documentadas).
- A partir de esta release, **toda adopción posterior es drain automático** — la transición pre-trigger quedó consumida.
- Limpieza: helper efímero `sqx/tools/mt5ops` eliminado del repo (árbol limpio, master `5a66bb6` pusheado); host sin tareas efímeras ni archivos temporales de prueba (tarea `EF-CtrlC-02144` borrada); http.server local detenido.
- Pendientes owner pre-existentes intactos: autologon post-reboot, LiveUpdate 6230, re-evaluación SCM.

## 8. Commits, IDs y trazabilidad

- symphony master: `e4d37ff` (baseline) → **`5a66bb6`** (manifest 0.2.144). Sin otros cambios de código.
- Stager: `32e1554` sin cambios.
- Release: 0.2.144, windows SHA256 `ba4948d45b94a71c78921bfa4be8e76a6f904982e575b58c17f1b81c91ad904e`, size 37,520,384.
- Workflows (namespace `sqx-prop`): drain test `MT5BacktestArtifactWorkflow:smoke-drain-02144-20261016` run `01a142cb-b020-7947-9184-42a6516c1fe9` (success); guard reuse `…:smoke-canary-reuse-02144-20261016` run `01a142d2-922f-79d5-bf84-1a397cec4cb0` (rechazo tipado esperado); canario nuevo `…:smoke-canary-02144-20261016` run `01a142d3-8cec-7164-a63d-eef970a1b861` (success).
- Evidencia en host: `C:\ProgramData\Stager\session-worker.supervisor.log`, `session-worker.out-20261016-003001.log` (era pid 19864), `session-worker.out-20261016-004426.log` (era pid 5308), stager status JSON, hashes certutil de transferencias.
- Helper efímero (borrado tras uso): `sqx/tools/mt5ops` (pollers/owners/dispatch, patrón `di.InitSelective("sqx-watcher")`).

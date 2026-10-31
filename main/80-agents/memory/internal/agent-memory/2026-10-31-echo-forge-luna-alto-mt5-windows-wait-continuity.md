---
type: agent_memory
schema_version: 1
scope: project
created: "2026-10-31"
updated: "2026-10-31"
area: "[[Echo Forge]]"
project: "[[Echo Forge]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[2026-10-31-luna-alto-mt5-windows-wait-root-cause]]"
aliases:
  - LUNA_ALTO mt5 windows wait checkpoint
  - checkpoint LUNA_ALTO 20261031
confidence: high
memory_state: active
continuity_key: echo-forge/luna-alto-20261031-mt5-windows-wait
supersedes:
superseded_by:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-memory
  - agent/internal
  - project/echo-forge
  - checkpoint
---

# LUNA_ALTO 20261031 — checkpoint: cierre MT5 Windows y campaña final Forge → Echo

## Objetivo y gate actual

- Objetivo: cerrar el bloqueo del worker MT5 en Windows (Run B `a5eafeb7-da3a-4986-9bfb-e2b005da2144`) y ejecutar UNA aceptación integral Forge → Echo (Top 4 por tipo, 2 tipos).
- Gate actual: **Shot 1 — causa raíz PROBADA, fix NO implementado.** Gate de salida de Shot 1 pendiente.
- Ojo: Run B está **bloqueado**, no terminado. No es candidato a "terminar" hasta que el worker libere el slot.

## Último hecho probado (OBSERVADO, no inferido)

- `terminal64.exe` PID 7668 sigue VIVO 5,5 h después de su lanzamiento; CPU acumulada 9,73 s; 4 threads; 394 handles; `Responding=True`; `MainWindowTitle` vacío; **sin conexiones TCP** (descarta espera de broker).
- Log del terminal MT5 `C:\MT5\slots\slot-1\logs\20261031.log`:
  - `13:52:41.972 Tester last test passed with result "successfully finished" in 0:00:52.490`
  - `13:52:43.886 Terminal exit with code 0` ← **el terminal YA registró su salida**
  - `13:52:44.902 MQL5.community authorization failed`; `13:52:47.907…13:52:59.912 LiveUpdate timeout on stop` (×5); `13:52:59.913 LiveUpdate terminated` ← última línea del log; después, silencio.
  - Conclusión: el cálculo terminó y el terminal intentó salir; el **proceso quedó vivo en el teardown post-salida**.
- Tester log: `NDX_SQX,H1: 55270679 ticks, 3539 bars generated. Test passed in 0:00:52.490`; `final balance 100000.00 USD`; **0 trades** (`Alert: Not enough money to send order with 9.50000000 lot or Margin Calculation Error` repetido).
- Último log del worker (`session-worker.out-20261031-135126.log`): `cmd_executor.go:174 "Iniciando ejecución de comando"` con `configured_timeout_ms=0`, `configured_grace_ms=0`. Sin línea posterior en 5,5 h.
- Transición exacta del bloqueo: `sqx/adapters/cmd-executor/process_windows.go` → `managedProcess.wait()` → `windows.WaitForSingleObject(p.process, windows.INFINITE)` sobre el proceso raíz. El `select` de `cmd_executor.go` no tiene rama viva: `configuredTimeout==0` ⇒ sin deadline; `configuredGrace==0` ⇒ `graceTimer==nil` ⇒ la 3ª rama del `select` bloquea en un canal sin buffer para siempre.
- Consecuencia: la actividad Temporal `mt5_backtest_artifact` no retorna ⇒ no hay ACK, no se publica el artifact, no se libera la lease del slot ⇒ los 5 hijos hermanos quedan PENDING y Run B queda colgado para siempre.

## SHA / binario efectivo (verificado byte a byte)

- Fuente desplegada: worktree privado `/home/kor/aranea/work/forge-independent-logical-types-20261029`, rama `codex/forge-independent-logical-types`, HEAD **`6614b2b05c03db9b39b5467b46e2c2c7d0c1fa19`**.
- `deploy/manifest.json` está **modificado sin commitear** (0.6.2 → 0.6.4). Bookkeeping pendiente.
- Binario Windows desplegado: `C:\ProgramData\Stager\releases\0.6.4\bin\sqx-mt5-worker.exe`, SHA256 **`172d395e78f842662a7850493d0a609b7c090e02c8d5fbad7dfa265628da4a0f`**, 37 578 752 B — **idéntico** a `deploy/0.6.4/windows-amd64/sqx-mt5-worker.exe` del mismo worktree.
- Corrección sobre el mandato: la base 0.6.4 reportada (`84088bb`, `3a30155`, `4a4c1bb`, `d3069ee`) es incompleta; el binario desplegado incluye además `d5eca5a`, `02cf77b`, `6614b2b`. `a736102` es sólo el ancestro, no el SHA probado.
- `stager` release activo: `CURRENT` = 0.6.4. Supervisor: `C:\ProgramData\Stager\bin\Start-EchoForgeSessionWorker.ps1` (tarea programada `\EchoForgeMT5WorkerSession`).

## FlowRun / RunID / ActivityID / attempt

- FlowRun B: `a5eafeb7-da3a-4986-9bfb-e2b005da2144`; workflow padre `sqx-main-v1-ff9dac60-acd5-4e9c-bd5c-1c2ca9cae04f`; RunID padre `01a19228-b765-72dc-a54a-2d1623cc7fa1`.
- Child colgado: `mt5-backtest-ndx-flow-example-2-v1-wluna-alto-20261031b-754c3d397dcee983`, RunID `01a1926e-0928-7c05-a9f5-b106b79210a6`, **activity_id "5"**, tipo `mt5_backtest_artifact`, queue `sqx-mt5-queue`, namespace `sqx-prop`, **attempt 227 en estado Started**.
- Timeouts de la actividad: `start_to_close_timeout = 3 153 600 000 s` (100 años ⇒ nunca expira), `heartbeat_timeout = 120 s` (el worker sigue latiendo ⇒ el bloqueo NO se resuelve por timeout).
- Retry policy: `initial_interval 5s`, `backoff 2.0`, `max_interval 30s`, `non_retryable = {source_not_found, contract_error}`.
- Fallo del intento 226 (el que explica las 226 reintentos): `mt5_backtest_artifact: infrastructure: ... INI efectivo: roundtrip temporal no exacto: [1766620800000,1785715199999) → 2025.12.25..2026.08.02 → [1766620800000,1785715200000): no representable por fechas MT5`. **Defecto secundario: un error determinista de contrato clasificado como `infrastructure:` ⇒ retry futile en bucle (226 intentos).** Corregido en `02cf77b`; el fallo no se clasifica como `contract_error`.

## Propietario del proceso / slot

- Proceso: `sqx-mt5-worker.exe` PID 6468 (padre), `terminal64.exe` PID 7668 (hijo), slot `slot-1` (`C:\MT5\slots\slot-1`).
- Lease del slot: `C:\MT5\slots\slot-1\EchoForgeJobs\.echo-forge-slot-lease.json` — `operation=backtest`, `activity_id=5`, `run_id=01a1926e-0928-7c05-a9f5-b106b79210a6`, `acquired_at=2026-10-31T16:51:31.7012822Z`. **Sigue retenida.**
- Owner del slot = este worker. Único terminal64 vivo en el host ⇒ no hay terminal ajeno que matar.

## Artifact / oráculo

- HTM nativo completo y **de ESTE intento**: `C:\MT5\slots\slot-1\EchoForgeJobs\NDX_flow_example_2_v1_wLUNA_ALTO_20261031b\backtest\5-227\output\final-055f737e-dce2-4d5f-8e65-b36f6c4ecda9.htm` (40 306 B, escrito 13:52:41, `</html>` presente, tabla Deals presente). PNG (holding/hst/mfemae) 13:52:41. CSV del agente: `C:\MT5\slots\slot-1\Tester\Agent-127.0.0.1-3000\MQL5\Files\final-055f737e-....csv` (472 B, 13:52:40).
- `tester.ini` de ESTE intento: `ShutdownTerminal=1`, `Model=4`, `FromDate=2025.12.25`, `ToDate=2026.08.02`, `Report=EchoForgeJobs\...\output\final-055f737e-...`, `ReplaceReport=1`.
- Oráculos preparados: `~/aranea/work/luna-alto-20261031/bin/{mgo,oracle,tqprobe,wfdesc}`.
- **Pendiente de transición, no de permiso**: los 5 hijos PENDING son de la MISMA wave de Run B. No son una campaña distinta.

## Estado colateral verificado (no bloquea el fix, pero condiciona la campaña)

- **Monitor `automation-ae1c1041`**: NO está vivo. Es una tarea programada ZCode de 15 min, `workspaceKey=/home/kor/secondbrain/main`, que enviaba prompt a la sesión previa `session_cb03a0489abceef5a89f8c26cc27ea1e` para verificar el ranking y la igualdad de conjuntos en Echo cuando cerrara el FlowRun. Disparó 5 veces (15:34, 15:49, 16:04, 16:19, 16:34 hora local) y **no ha disparado desde 19:34Z**; `CronList` de este workspace devuelve `[]`. ⇒ No hay segundo actor reconciliando/publikando. No crear otro monitor. Documentar su estado al cierre y desactivarlo sólo si recupera función.
- **Flota**: `sqx-main-queue` con 4 pollers (hefesto/zeus/kronos/hera), `sqx-mt5-queue` con **1 solo** poller (`6468@worker-kronos`). El bloqueo es de un único punto. Hay 7 workflows RUNNING (padre + 6 children MT5).
- **La parte SQX de Run B YA ESTÁ COMPLETA**: `wavecount` muestra 6 evaluaciones de `final-reretester`, `optimizer`, `retester`, `evaluate_strategy`, `apply_selected_run`, `mt5_compiler`; 120 `overview`; 102 `wfm`; colecciones con 56 999 metric_sets, 682 trade_sets, 237 scores, 966 group_documents. **`mt5_backtest_artifact` = 0 evaluaciones**: sólo falta ese paso.
- **Los 5 hermanos no están "colgados": están `Scheduled`** (no `Started`), con attempt 227/228/230/231/231 y el MISMO fallo de roundtrip. El último de ellos que corrió fue el que penduló; los demás esperan el slot.
- **Rango de datos del símbolo**: `NDX_SQX: history synchronized from 2024.01.02 to 2026.10.09` y `real ticks begin from 2025.07.01` ⇒ **la ventana pedida 2025.12.25..2026.08.02 SÍ está cubierta**. Cierra la pregunta abierta de la sesión anterior.
- **0 trades en el backtest de 5-227**: 1277 alertas `Not enough money to send order with 9.50000000 lot or Margin Calculation Error`, con Free Margin 100 000 y leverage 1:100, contract size 10. El EA dimensiona 9,5 lotes (riesgo 200 USD / 21 USD por lote). Es un tema de **economía del candidato/broker**, NO de la instalación: el `report_smoke` vigente del slot es `status: PASS`, `terminal_sha256: 5ECE7395…` (= SHA real de `terminal64.exe`), `trades_closed: 145`. La historia que va a Echo es la **declarada (SQX)**, no una historia MT5 supuesta.
- **Echo DEV (PG `192.168.31.220/echo-develop`, schema `echo`, user `echo_user`)**: 148 `strategy_definitions`, 7 `strategy_versions`, 1 `strategy_history_state`, 8 `strategy_identity_mappings`, 6 `promotion_records`, y **1 solo** `strategy_ingestion_receipts` (`idempotency_key=dev-smoke-register-4`, `registry_namespace=lab-cert`, `producer_writer=a1401909-…`, `accepted_at=2026-10-28T18:28:57Z`) ⇒ **NO existe todavía el caso positivo de la frontera Echo por task de Forge** (`source.type=task_output`, `source.task=e2e-group`). Ese es exactamente el control barato de Shot 3.
- **Gateway DEV**: `/home/kor/opt/echo-dev/current` → `releases/labv4-3eaed4d2-20261031`, PID 591545, `env=development`, `etcd_prefix=/echo/development/`, escuchando `:8090`. Core DEV PID 423833 (`releases/64f0853b…`). El MCP postgres-**ro** está ligado a `echo` (PROD); el **rw** a `echo-develop`.
- **Cross-compilación**: `GOOS=windows GOARCH=amd64 go build ./sqx/cmd/sqx-mt5-worker` funciona desde Daedalus (go1.27.1 linux/amd64, go.work con `./deployer` + `./sqx`).

## Plan de drenaje del slot (para Shot 2, luego del fix desplegado)

1. Stagear la release corregida y escribir `C:\ProgramData\Stager\CURRENT` **con LF y sin BOM** (known-error `stager-windows-powershell-crlf-current`: PowerShell 5.1 `Set-Content` mete CRLF y el runtime no selecciona la release).
2. El supervisor `Start-EchoForgeSessionWorker.ps1` detecta que CURRENT avanzó y **señala el drain** (`Global\echo-forge-sqx-mt5-worker-drain`) → `main.go:314 controller.BeginDrain()`. **VERIFICADO EN CÓDIGO**: `sqx/core/lifecycle/controller.go:29 TryAdmit()` sólo admite en `StateAccepting`; `BeginDrain()` (línea 51) pasa a `StateDraining` ⇒ `sqx/core/lifecycle/temporal.go:41` devuelve `worker_draining` (retryable) para toda activity nueva. **El worker viejo NO puede robar el retry.**
3. **El drain NO se completará solo**: `Drained()` sólo cierra cuando `active == 0`, y la activity bloqueada mantiene `active = 1` para siempre. Por eso hace falta el paso 4.
4. Con la admisión cerrada, terminar **sólo** el `terminal64.exe` del job propio (PID verificado por la lease: `run_id=01a1926e-0928-…`, `activity_id=5`, `strategy_ref=055f737e-…`), nunca por nombre ni terminales ajenos. Con eso la activity devuelve (fallo físico honesto), el allocator libera la lease, `Release()` baja `active` a 0, `drained` cierra, `worker.Stop()` + `MarkStopped()` + `singleton.Release()` ⇒ salida limpia. **Un binario nuevo no cambia una goroutine vieja**: por eso el orden stage→drain→release es obligatorio.
5. El supervisor, al ver el worker ausente, barre huérfanos GUI bajo `C:\MT5` (`Remove-Mt5GuiOrphans`) y adopta la release nueva. La activity reintentada la toma el worker corregido. `MaxConcurrentActivityExecutionSize = 1` (`main.go:43`) ⇒ una activity a la vez en el host.
6. Verificar ausencia de procesos/ownership incompatibles antes de permitir el retry.

## Parámetros operativos para el acto final (verificados en ventana o leídos de skill canónica)

- **Host Windows real = `192.168.31.128`** (el Environment Contract §0 dice "VM 135": dato OBSOLETO; el feedback LUNA_ALTO lo declara obsoleto y el host .135 es inalcanzable). Perfiles MCP: `mt5-kronos` (RO), `mt5-kronos-operator` (operator, `echo-dev` no-admin), `mt5-kronos-admin` (admin OS local). Evidencia fresca: `C:\ProgramData\Aranea\evidence\stager-evidence-latest.json` — `generated_at_utc=2026-10-31T20:28:07Z`, `partial=false`, `run_identity="nt authority\system"`, `inspector_sha256=28d782b7…`, worker PID 6468 con `exe_sha256=172d395e…`. Los 4 criterios de certificación se cumplen.
- **Temporal real en `192.168.31.46:7233`** (lo.poll del worker). El MCP `aranea-temporal-ro` está apuntado al namespace `sqx-dev` **destruido** ⇒ sus errores (`Namespace ... Deleted`, `INTERNAL_ERROR`) son del perfil, NO del sistema. Para `sqx-prop` usar cliente propio (`~/aranea/work/luna-alto-20261031/bin/{wfdesc,mgo,tqprobe}` ya funcionan contra `sqx-prop`).
- **Mecanismo de release y rollout**: `./deploy_release.sh --release-only <X.Y.Z>` desde el worktree limpio (publica MinIO + manifest); el apply lo hace el stager externo. **Acreditar por lectura física de SHA en cada host** (`/opt/stager/releases/<V>/bin/symphony`, `cat /opt/stager/CURRENT`): `scripts/verify_rollout.sh` no autentica por SSH desde Daedalus y su "0/3" NO significa fallo. En Windows: `C:\ProgramData\Stager\releases\<V>\bin\sqx-mt5-worker.exe`; las activities `mt5_backtest_artifact`/`list_mt5_artifacts` **sólo** las registra ese binario ⇒ un fix en `core/domain` no toma efecto hasta que el worker Windows adopta la release.
- **CURRENT con LF y sin BOM**: escribir con `[IO.File]::WriteAllText($path, "0.6.5`n", (New-Object System.Text.UTF8Encoding $false))`. PowerShell 5.1 `Set-Content` mete CRLF y el runtime no selecciona la release (known-error `stager-windows-powershell-crlf-current`).
- **Dispatch de una wave**: watcher EN ZEUS, `/home/echo-dev/certw12/sqx-watcher` (ENV=certw12 ⇒ ETCD propio ⇒ `sqx-prop`/`sqx-main-queue`). Su binario debe ser ≥ la release que introduce los campos del spec (0.4.8 rechaza `calendar_profile_ref` 0.5.2+). Intake = JSON de spec + los 4 CFX juntos; al consumir mueve todo a `processed/`. **Un wave despachado queda QUEMADO para siempre** (cfgID determinista) ⇒ identidad nueva por intento, nunca re-despachar el mismo wave.
- **Invariante SQX vinculante**: 1 VM = 1 worker = 1 task en ejecución (`MaxConcurrentActivityExecutionSize: 1`, protegido por test). El fan-out ENTRE hosts sí existe (`max_parallel: K` en groups durables sin source).
- **Cadena completa en UN FlowRun** (corrección owner 2026-10-16/17): builder→overview→classification→early ranking→selection→GROUP (`source.type=ranking_snapshot`, anidado retester+optimizer+evaluate_wfm+select_robust_run)→apply→final reretester→tradelist→report→MQ5→EX5→MT5→fidelity→ranking→promoción. Duración medida con builder de 750–1000 estrategias: **2–3,5 h**.
- **Preflight de fidelidad (crítico, quemaría la corrida al final)**: `mt5_score_shadow_v1` falla NO-retryable si el alias del símbolo no está en `sqx/core/evaluation/canonical_scope.go`. **VERIFICADO OK**: `ndx_sqx` → `ndx` y `usatechidxusd_dukascopy_utc02` → `ndx` ya están mapeados.
- **Baseline de performance iterable**: Precision `batch_size≈90`, Full `batch_size=10`, Optimizer `batch_size=1`, `max_parallel=3`. Lo FROZEN es que el fan-out existe.
- **Retomar un FlowRun sellado FAILED no es "continuar"**: `flow_run_seal` rechaza FAILED→COMPLETED (terminal por diseño). Un reset Temporal re-ejecuta el tramo, pero **"continuar" = re-despachar con wave nueva** (identidad limpia).
- **Delta de skill al cierre**: la skill de repo `echo-forge-testing` §[2026-10-31] dice hoy "el backtest no avanza". Mi evidencia OBSERVADA lo **refuta**: el cálculo SÍ avanzó (`Tester last test passed with result "successfully finished"`, 55 270 679 ticks, reporte y CSV escritos) y lo que quedó vivo fue el **proceso** en el teardown post-salida. La prueba es cruzar el journal del Tester con el log de sesión del worker. Y `LiveUpdate timeout on stop` **no es diagnóstico** por sí solo (queda como parte del teardown normal de este host).

## Siguiente comando / acción exacta

1. Implementar el fix mínimo de Shot 1 en el worktree privado (`6614b2b`): señal terminal correlacionada → **gracia de cierre acotada y configurable** → `TerminateJobObject` del job propio → resultado con **código de salida y razón físicos** (nunca exit 0 fabricado) → validación completa del reporte antes de declarar PASS.
2. Contraprueba independiente + canario físico de 2 backtests consecutivos en el mismo worker Windows (Shot 2).
3. Congelar y publicar sólo lo necesario; luego una única campaña de aceptación (Shot 3 → acto final).

## Acciones que NO deben repetirse

- **NO** declarar PASS por `Test passed`, por el HTM, por el CSV, por "el archivo dejó de crecer" ni por un timeout.
- **NO** matar procesos por nombre, servicios compartidos ni terminales ajenos; sólo el job propio.
- **NO** reintentar el intento a ciegas ni "resellar" Run B mientras la lease siga retenida.
- **NO** usar `WithGracePeriod` como atajo: una muerte por temporizador **no es exit code 0** (hoy `cmd_executor.go` marca exit 0 en `graceTriggered` — defecto a corregir).
- **NO** añadir timeout global de negocio, cambiar las retry policies aprobadas, ampliar slots MT5 ni instalar un watchdog externo permanente.
- **NO** meter reglas de `terminal64`/MT5/textos de log en el workflow, el `group` o el SDK genérico: la señal terminal es del adaptador MT5; el executor sólo inicia/espera/drena la unidad física.
- **NO** habilitar EAs, cuentas, capital ni trading. `REGISTER_ONLY` en Echo DEV.
- **NO** dos monitores/actores reconciliando o publicando a la vez.

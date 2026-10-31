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
- **Higiene de release (defecto heredado, corregir en Shot 3)**: los binarios desplegados de 0.6.4 llevan `vcs.revision=02cf77b8791e2e10adfda8bfe17db7c23a2f0394`, `vcs.time=2026-10-31T16:49:20Z` y **`vcs.modified=true`** (el árbol estaba sucio por el bump del manifest). El gate `release-certification` exige `vcs.modified=false` ⇒ la 0.6.5 debe salir de árbol limpio. Secuencia que lo logra: (1) commit del fix ⇒ árbol limpio; (2) build de `deploy/<v>/{linux,windows}-amd64/`; (3) commit de los artefactos + manifest; (4) **rebuild** desde el árbol ya limpio (Go sella `vcs.time` = hora del commit, no de build ⇒ el binario es byte-idéntico y el manifest sigue valiendo) ⇒ `vcs.modified=false`. Nota: `deploy/0.6.4/**` SÍ está versionado en git (por eso el `git status` sólo muestra `M deploy/manifest.json`).
- **Corrección al informe previo**: la fuente RUNTIME efectiva del worker desplegado es `02cf77b` (los 4 arreglos + el fix de RoundtripExact), **no** `6614b2b`: `6614b2b` es un commit de docs fechado 18:21:44Z, posterior al build de 16:49:20Z. Los bytes del binario sí son idénticos a `deploy/0.6.4/windows-amd64/sqx-mt5-worker.exe` del worktree, pero ese artefacto se construyó desde `02cf77b` con el manifest sin commitear.

## Shot 1 ENTREGADO (2026-10-31)

- **Commit del fix: `412c50e`** "fix(worker): señal terminal correlacionada + gracia acotada para el linger infinito de terminal64 tras exit with code 0". Rama `codex/forge-independent-logical-types`, sin push/tag/deploy.
- **Bookkeeping: `ac306fc`** "chore(deploy): manifest de release 0.6.4" — deja el árbol limpio para poder construir con `vcs.modified=false`.
- Diseño: **Capa 1 (executor, agnóstica de dominio)** — `TerminalSignalRunner.ExecuteWithTerminalSignal` como capacidad **opcional** (no extiende `capabilities.CommandExecutor`, consumidores intactos); disparador por **canal explícito** (no context value); knob propio `WithTerminalSignalGraceMs` (default finito **60 s** > linger real ~16 s), distinto del `success_grace_ms` legacy; `WithDrainTimeout` (30 s); `ReaderDrainTimeout` (5 s) para el segundo deadlock (`wg.Wait()` sin EOF). Resultado estructurado en `ExecResult`: `TerminationReason` (`exited_normally` | `terminated_by_terminal_signal_grace`) + `TerminalSignalDrained` + **exit code físico**. **Capa 2 (adaptador MT5)** — `terminal_observer.go` observa los **deltas por offsets** del `LogSnapshot` de ESTE intento; dispara con `exit with code 0` del journal de terminal o con fin de tester + HTM del intento completo (UTF-16LE vía `report.DecodeUTF16LE`); un timeout, un CSV suelto, un HTM parcial o de otro intento **nunca** disparan. `concludeTerminalSignalRecovery` exige **drenaje acreditado + `report.Parse` nativo** para dar `Success` + `Warnings`; si falta cualquiera ⇒ error técnico con evidencia conservada (`cleanupOnError=false`).
- **Rama legacy intacta**: `WithGracePeriod`/`success_grace_ms` sigue fabricando exit 0 para `campaign-etcd/maintenance_executor.go` (único consumidor real). La ruta MT5 **no puede alcanzarlo** (neutralización local + test).
- **ATRIBUCIÓN DE REGRESIÓN (medida por el manager, no por el implementador)**: en `6614b2b` (pre-fix) y en `412c50e` el conjunto de tests que fallan es **IDÉNTICO**: `adapters/mt5`=7, `adapters/mt5/binding`=27, `adapters/mt5/normalization`=10, `adapters/mt5/report`=28, `adapters/mt5/scoring`=0, `activities/worker`=68 ⇒ **140 en ambos**; el `diff` de nombres sólo difiere en dígitos de tiempo. `adapters/cmd-executor` = **ok** en ambos (medido: 6,5 s). Los 140 fallos son preexistentes y por fixture ausente (`mt5-export.htm` en la raíz del repo).
- **Release en Windows**: el staging NO es manual — `StagerReconcile` (tarea SYSTEM, `stager.exe --target-config C:\ProgramData\Stager\target.yaml`, **cada minuto**, `LastTaskResult 0`) reconcilia desde el manifest. Un `CURRENT` escrito a mano puede ser revertido en ≤1 min ⇒ la candidate debe entrar por el **manifest canónico** (`deploy_release.sh --release-only <v>`), no a mano.
- `deploy/0.6.5/` y los artefactos de release están **gitignored** (no versionados) ⇒ no ensucian el árbol para el build.

## Shot 2a — VEREDICTO DEL VERIFICADOR INDEPENDIENTE (2026-10-31)

- El verificador (autor distinto del implementador; baseline clonado y medido por él) concludes: **la afirmación central del fix RESISTE la refutación**. Oráculos (a)-(g) = PASS (a con salvedad). Conteo de fallos idéntico al baseline: `cmd-executor` ok, `mt5` 7, `report` 28, `normalization` 10, `activities/worker` 68 ⇒ **140, cero crecimiento** (coincide con la medición independiente del manager: 7/27/10/28/0/68 = 140, y el `diff` del set de nombres sólo difiere en dígitos de tiempo).
- RED propio del verificador en baseline: `Execute` cuelga (timeout=0, grace=0) y `grace` fabricaba exit 0. Reproducidos por él, no por el implementador.
- **H2 (MEDIO-BAJO, CORRECCIÓN OBLIGATORIA antes de congelar)**: `log_snapshot.go` (`deltaBytes`, rama same-size + mtime nuevo) relee desde offset 0 ⇒ el observador puede disparar con `Terminal exit with code 0` **de otro intento** ⇒ armaría la gracia y mataría un backtest ajeno. La sonda `TestVerifierWatcher_SameSizeRewriteReplaysHistoricalSignal` FALLÓ y lo confirmó. Es semántica preexistente de `deltaBytes`, pero el fix la **escala** de "journal delta equivocado" a "kill de un backtest ajeno". Corrección: el observador sólo acepta **crecimiento estricto de tamaño** o **archivo nuevo** como delta de este intento.
- **H1 (MEDIO, documental)**: el RED de "wg.Wait() cuelga por descendiente que retiene el pipe" **no se reproduce en Linux baseline** (os/exec cierra los extremos al salir el root; el test retornó éxito silencioso en 0,02 s con el descendiente vivo). En Linux el peligro del baseline era **éxito silencioso con job no drenado**; el hang de lectores es propio de la **vía Windows**, no ejecutable en este host. La sobre-declaración queda corregida en el commit siguiente (no se reescribe `412c50e`).
- **H3 (BAJO, riesgo residual)**: sin señal correlacionada el bloqueo sigue existiendo por diseño (compensación del "sin timeout global de negocio"). Se cierra (si es seguro) con un trigger secundario per-attempt: **HTM del path exacto del intento + `report.Parse` OK + tamaño estable entre dos polls** ⇒ inicia la gracia, **nunca declara éxito**. El mandato lo autoriza explícitamente.
- **H4 (BAJO, aceptado)**: el drain en Linux por `kill(-pgid,0)` es sensible a reuso de PID en la ventana de 30 s. Riesgo declarado, no bloqueante; en Windows no aplica (Job Object por handle).
- **H5/H6 (cosméticos)**: motivo `exited_normally` impreciso en el híbrido con drenaje no acreditado; comentario engañoso sobre `sqcli/success_grace_ms` en `cmd_executor.go:175`.
- **Límite material del verificador**: los tests Windows (`cmd_executor_terminal_signal_windows_test.go`) sólo **compilan** (`GOOS=windows go vet` + `go test -c` ok); **no son ejecutables en este host Linux**. Toda la evidencia de la Capa 1 es vía process-groups Linux. El canario real en `mt5-kronos` es lo que cierra ese hueco.
- **Otro dato del verificador**: `go build ./sqx/...` falla en `sqx/tools/` (mains redeclared) — **preexistente**, idéntico en baseline (diff vacío en `sqx/tools/`). La afirmación literal "go build ./sqx/... ok" sólo vale excluyendo `sqx/tools`.
- Residuo del verificador en el worktree (untracked): `sqx/adapters/cmd-executor/cmd_executor_verifier_test.go`, `sqx/adapters/mt5/terminal_observer_verifier_test.go` → adoptados por el implementador como tests de regresión permanentes.

## Shot 2b — CANARIO FÍSICO PASADO (2026-10-31 22:27–22:33Z)

- **Release 0.6.5 publicada por el mecanismo canónico** (`./deploy_release.sh --release-only 0.6.5` desde el worktree privado): `vcs.modified=**false**` y `vcs.revision=31e69908c687e4abbb44f484df096e80631cfafc` (el commit final exacto) — se corrige el defecto de higiene heredado de 0.6.4. Windows `sqx-mt5-worker.exe` SHA256 **`5712027e00ef7ae0a35463430ba0b93cb2f1b8965234bd0a3cd9188534e5005f`** (37 622 272 B), Linux `symphony` SHA `b83ea78cc27b9786f8f9f07933f47b754745be442fa73498b2415a0c10a92833`. MinIO confirmó el manifest `worker/sqx/manifest.json` v0.6.5. El "rollout 0/3" del script es la limitación SSH conocida: la adopción se acreditó **por SHA físico en cada host**.
- **Drenaje del slot ocupado, en orden y con evidencia**:
  1. 22:24:01Z el stager de Windows stageó `releases\0.6.5` (SHA 5712027e… verificado en disco).
  2. 22:24:02Z el supervisor: *"update de release 0.6.5: drain solicitado al worker pid 6468"* ⇒ **admisión cerrada**. Prueba: los 5 hermanos siguieron `Scheduled` con **contadores de intento intactos** (227/231/230/231/228) ⇒ el worker viejo **no admitió nada nuevo**.
  3. Identidad del proceso colgado verificada antes de tocarlo: PID 7668, parent 6468 (nuestro worker), command line apuntando al `tester.ini` de **nuestro** intento `5-227`, lease `run_id=01a1926e-0928-…`/`activity_id=5`/`strategy_ref=055f737e-…`. Se terminó **sólo esa raíz de job** (`Stop-Process -Id 7668 -Force`); la **lease se liberó**.
  4. 22:27:02Z el supervisor: *"worker previo pid 6468 ya no esta (cierre probado): adoptando release 0.6.5"* ⇒ worker nuevo **PID 6528** con `releases\0.6.5\bin\sqx-mt5-worker.exe`.
- **CANARIO (2+ backtests consecutivos, mismo worker, mismo slot, SIN reinicio, SIN kill manual, SIN limpieza manual entre ellos)**:
  - `activity.ok status=success` a las **22:28:25Z, 22:29:41Z, 22:30:48Z, 22:31:56Z** (separación 67–76 s), todas con el mismo `trace_id` de wave `LUNA_ALTO_20261031b` y el mismo worker 6528 / `slot-1`.
  - **El intento que llevaba 5,5 h colgado (5-228, estrategia `055f737e`) completó en `duration_ms=58239`** con `"Comando ejecutado exitosamente"` ⇒ exit code 0 **real**, sin warning de recuperación. Antes/after: 5,5 h bloqueado → 58 s.
  - Artefactos publicados por intento (bucket `sqx-strategies`, prefijo `durable/mt5-export/v1/a5eafeb7-…/<strategy_ref>/sha256:…/13_mt5_backtest/`): `.htm` (p.ej. **942 324 B**, sha `1cc5e71e…` ⇒ historia positiva real, no el HTM de 40 KB con 0 trades) y `.terminal.log` (4 200 B, sha `798d85c7…`/`bb221fdd…`/`7a07e330…`).
  - `wavecount`: `mt5-backtest.v1` **0 → 6** evaluaciones, `schema mt5-evaluation.v1` 6, total de evaluaciones 258 → 273. **El paso MT5 de Run B está COMPLETO.**
- **CAMINO REALMENTE EJERCITADO = el limpio, no el de recuperación.** El log del terminal ahora muestra un cierre COMPLETO que en el intento colgado **no existía**: `Terminal exit with code 0` → `Network disconnected` → `Terminal stopped with 0` → `Terminal shutdown with 0`. En el colgado, en cambio, el teardown entró en `MQL5.community authorization failed` → `LiveUpdate timeout on stop` ×5 → `LiveUpdate terminated` y **el proceso nunca terminó**. ⇒ El cuelgue original fue una **anomalía de entorno** (fallo de autenticación de MQL5.community que dejó el thread de LiveUpdate colgado) **agravada por un defecto estructural** (el executor sin timeout ni gracia esperaba para siempre). El fix elimina la espera **no acotada**; en este canario no necesitó disparar su gracia porque el terminal salió limpio.
- **HUECO QUE QUEDA ABIERTO Y DEBE DECLARARSE**: la rama de **terminación forzada por gracia** (Win32 `TerminateJobObject` + acreditación de drenaje + motivo `terminated_by_terminal_signal_grace`) **NO fue ejecutada**: es la única prueba que este host no dio. Está verificada por compilación (`GOOS=windows go vet` + `go test -c` ok) y su gemelo semántico Linux **sí** se ejecutó con `-race` (drenaje no acreditado → error observable sin huérfanos; lectores acotados; cancelación preservada). El host MT5 **no tiene toolchain Go** y no se instaló uno (mutar el host del slot en plena campaña es desproporcionado). Transferir el binario de test cross-compilado exige un canal HTTP que el host Windows no abre hacia Daedalus (verificado).
- **Riesgo declarado V6b**: si el journal activo se reescribe in-place creciendo, la zona crecida puede contener una línea histórica de otro intento ⇒ gracia espuria ⇒ kill de un job propio ⇒ **intento fallido con error observable, NO hay camino a falso PASS** (el PASS exige drenaje acreditado + parser nativo del HTM de ESTE intento). Decidido NO endurecer: hacerlo exigiría verificar la integridad del prefijo y añadiría modos de fallo nuevos al propio mecanismo que arregla el cuelgue.

## Shot 2b-bis — BATERÍA WINDOWS EJECUTADA NATIVAMENTE (hueco cerrado)

- El host MT5 **no tiene toolchain Go** y no se instaló ninguno (mutar el host del slot en plena campaña es desproporcionado). Solución usada: **cross-compilar el binario de test en Linux y ejecutarlo nativamente en Windows** (`GOOS=windows GOARCH=amd64 go test -c`), transferido por HTTP desde Daedalus (el host Windows SÍ abre a `192.168.31.161:8899` — el fallo previo era el `-Method Head`, no la red) y verificado **byte-exacto por SHA256** (`29bcedd2…`).
- **Resultado con el fix (31e6990)**: 15 PASS / 3 FAIL. Los PASS que **sólo existen con el fix** y que ejercitan la vía Win32 real:
  - `TestWindowsTerminalSignal_TerminatesOwnJobAndPreservesPhysicalExit` (0,37 s) — Job Object + `TerminateJobObject` + **exit code físico preservado**.
  - `TestWindowsTerminalSignal_NeutralizesLegacySuccessGrace` (0,46 s) — **no** fabrica exit 0.
  - `TestWindowsTerminalSignal_TerminationFailureIsObservableWithoutOrphans` (0,25 s) — fallo observable, **0 huérfanos**.
  - Además pasan los helpers Win32 preexistentes: `TreeIsOwnedAndCanceledAsOneUnit`, `DeadlineDrainsTreeAndPreservesTimeout`, `NormalExitWaitsForDescendants`, `GraceKillsWholeTree`, `OutsiderSurvives` (no mata ajenos), `RepeatExecutionLeavesNoTree`, `CapturesOutputAndQuotesArguments`, `CreateFailureDoesNotFallback`.
- **Atribución de los 3 FAIL**: son **preexistentes y ambientales** — invocan `/bin/sleep` y `sh -c "sleep 30"` (`cmd_executor_cancel_test.go:46`, `sqcli_executor_test.go:93,107`), que no existen en Windows. **Probado** ejecutando el binario cross-compilado del commit **base 6614b2b** en el MISMO host: falla **exactamente los mismos 3** (`TestCommandExecutorSuite`, `TestExecute_CancelPreservesContextCanceled`, `TestExecutorRFCSuite`) y pasa los mismos 12 helpers ⇒ **cero regresiones introducidas por el fix en la vía Win32**.
- Artefactos de prueba borrados del host (`sqx-cmdexec*.test.exe`, `win-tests*.txt`) y worktree base eliminado.

## Estado de Run B tras el canario (2026-10-31 22:40Z)

- El grupo **iteró con candidatas nuevas** (segunda tanda), como manda la receta cuando faltan seleccionadas: `sqx-apply-selected-run` 6→**12**, `sqx-retester` 6→12, `sqx-optimizer` 6→12, `strategy-evaluation.v2` 6→12, `sqx-wfm` 102→**204**, `wfm-cell` 96→192, `wfm-aggregate` 6→12, `sqx-final-reretester` 6→**10**, `mt5-compiler` 6→**7** (compilando ahora), `mt5-backtest` 0→**6**. Totales: evaluaciones 258→**401**, metric_sets 56 999→**57 125**, trade_sets 682→**691**, scores 237→**243**, group_documents 966→**1 016**.
- ⇒ **Run B puede alcanzar Top 4 por tipo por sí solo** (2 tipos × ≥4 candidatas evaluadas); no hace falta lanzar una wave nueva para el gate de Top 4.
- **Echo DEV todavía sin el caso positivo de entrega por task de Forge**: `echo.strategy_ingestion_receipts` sigue con **1 sola fila**, `dev-smoke-register-4` (namespace `lab-cert`, 2026-10-28) ⇒ la ingesta por task (`source.type=task_output`, `source.task=e2e-group`) **aún no se ha disparado**: depende del cierre del group (selección → ranking → promoción → ingesta). Es el gate de Shot 3c que queda pendiente de observar.
- Flujo pendiente en Run B: el parent muestra `PENDING_ACTIVITY type=project` (etapas post-MT5: selección robusta, ranking, promoción, ingesta) y 2 children `mt5-compile-*` nuevos.

## Siguiente comando / acción exacta

1. **Shot 3c — observar el cierre de Run B hasta la ingesta Echo**: esperar a que el group cierre (selección → ranking → promoción), que la activity `echo_ingestion_v2` dispare **por task de Forge** y verificar en `echo-develop`: `strategy_ingestion_receipts` con `registry_namespace=lab-cert`, `producer_writer` = identidad de la wave, receipt válido, y `strategy_history_state` materializada (historia declarada SQX, perfil `SQX_TRADELIST_V1`, `REGISTER_ONLY`). Readback en la capa dueña (PG + readback HTTP del gateway), no sólo un HTTP 200.
2. **Regresión acotada de los cuatro arreglos** sobre los bytes finales 0.6.5: bucket/origen exacto del lote, `GetTelemetry` por el camino registrado, aceptación de ancestría válida y rechazo de otra estrategia/EX5, equivalencia de fin inclusivo/exclusivo sin tolerancia a ventanas diferentes. La campaña de Run B **ya ejercita los cuatro** (los 6→12 apply, los 12 evaluate_strategy, los 6→10 final-reretester y los mt5-backtest con el INI efectivo por ventana) ⇒ la evidencia está en `wavecount`, no hace falta re-ejecutar.
3. **Acto final**: si Run B cierra con Top 4 por tipo en 2 tipos y la ingesta Echo es positiva, **NO lanzar una wave nueva**: Run B ES la aceptación integral (Builder real ya acreditado, receta completa, historial consultable). Si al cierre el Top 4 por tipo no se alcanza con evidencia de EOF, informar la escasez legítima; si la ingesta Echo falla, reproducir y corregir **sólo esa unión**.
4. **Cierre**: actualizar la skill de repo `echo-forge-testing` con el delta comprobado (el cálculo **sí** puede haber terminado: "cuelgue de shutdown" ≠ "backtest lento"; `LiveUpdate timeout on stop` es parte del teardown normal y **no es diagnóstico**; y el lento del worker es "sin línea nueva en el log de sesión + sin artefactos nuevos"). Registrar "sin delta" donde corresponda. Un solo checkpoint/bitácora. Desactivar `automation-ae1c1041` si recupera función (hoy **no** está viva: `CronList` vacío y sin disparo desde 19:34Z).
5. **Deuda que queda declarada, no resuelta**: (a) la rama de cierre forzado por gracia no se ejecutó en el canario físico (MT5 salió limpio) — sí se ejecutó **nativamente en Windows** vía binario cross-compilado; (b) riesgo V6b declarado; (c) H3 (sin señal correlacionada el bloqueo persiste por diseño); (d) `sqx/tools/` no compila (preexistente); (e) 140 tests preexistentes que fallan por fixture ausente `mt5-export.htm` en la raíz del repo.

## Acciones que NO deben repetirse

- **NO** declarar PASS por `Test passed`, por el HTM, por el CSV, por "el archivo dejó de crecer" ni por un timeout.
- **NO** matar procesos por nombre, servicios compartidos ni terminales ajenos; sólo el job propio.
- **NO** reintentar el intento a ciegas ni "resellar" Run B mientras la lease siga retenida.
- **NO** usar `WithGracePeriod` como atajo: una muerte por temporizador **no es exit code 0** (hoy `cmd_executor.go` marca exit 0 en `graceTriggered` — defecto a corregir).
- **NO** añadir timeout global de negocio, cambiar las retry policies aprobadas, ampliar slots MT5 ni instalar un watchdog externo permanente.
- **NO** meter reglas de `terminal64`/MT5/textos de log en el workflow, el `group` o el SDK genérico: la señal terminal es del adaptador MT5; el executor sólo inicia/espera/drena la unidad física.
- **NO** habilitar EAs, cuentas, capital ni trading. `REGISTER_ONLY` en Echo DEV.
- **NO** dos monitores/actores reconciliando o publicando a la vez.

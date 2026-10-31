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

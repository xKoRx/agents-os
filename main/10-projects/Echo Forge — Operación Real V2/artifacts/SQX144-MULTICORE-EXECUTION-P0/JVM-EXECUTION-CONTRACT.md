---
type: evidence_pack
schema_version: 1
status: final
created: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application: "[[xKoRx/symphony]]"
baseline: "xKoRx/symphony 492a271e (0.3.1)"
tags:
  - kind/evidence-pack
  - area/echo
  - tech/runtime
---

# JVM-EXECUTION-CONTRACT — contrato de arranque y ejecución observado (0.3.1)

Cadena exacta reconstruida de source + confirmada físicamente en esta sesión:

## 1. Temporal → worker

- Worker Temporal con `MaxConcurrentActivityExecutionSize: 1` por host (`sqx/cmd/sqx-worker/main.go:468-478`, protegido por test) ⇒ a lo sumo UNA actividad pesada (y por tanto un sqcli) por VM; los hosts paralelizan entre sí por la task queue compartida.
- Cada actividad construye proyecto + databank y termina invocando `SQXExecutor.ExecuteAndWait` (`sqx/adapters/executor-sqx/sqx_executor.go:55`): `sqcli -project action=start name=<project>`, binario SIEMPRE el de la versión activa (`runtime.GetSQXExecutablePath()`); éxito/error por markers ETCD (`sqcli/success_markers|error_markers`); duración telemetrizada (`symphony.sqx.sqcli.duration_ms`).

## 2. CommandExecutor → proceso

- `process_nonwindows.go`: `exec.CommandContext` + `SysProcAttr{Setpgid:true}`; sin taskset/affinity/quota; terminate = SIGTERM al grupo + SIGKILL a 5 s. El sqcli queda líder de su propio process-group (instrumentado aquí con samplers por pgid).

## 3. sqcli = JVM (hecho nuevo medido)

- El launcher Go `sqcli` **exec-reemplaza a la JVM en el mismo proceso/PID** (comm permanece `sqcli` con 258-273 threads; NO existe proceso hijo `java` — verificado con ps/pgrep durante runs). El "process group" del Execute ES la JVM.
- Config JVM efectiva (headless flota): `sqcli.config` gana sobre `JAVA_TOOL_OPTIONS` por orden: `-Xms4g` (config) + `-Xmx55g` (JTO de la unidad systemd) + `-XX:+UseParallelGC` + proxies/TLS; `--enable-native-access=ALL-UNNAMED`. En los benchmarks se replicó con `JAVA_TOOL_OPTIONS="-Xms34g -Xmx55g"` y config candidate idéntica (sin JFR). MaxRSS observado 1,4-18,2 GB según workload.
- Arranque observado en cada run (consola): licencia OK → "High priority: ON" → "Adjusting used cores to: 72 from requested: 76" → "Using: 72 cores, core usage configuration: '100%'" → "Preparing thread executors: 72" → datos cargados → HTTP API local 5050 → proyecto.
- Settings leídos en CADA arranque desde `user/settings/settings.xml` (cada run es una JVM nueva; `coreUsage=100%`, `highPriority=true`, `threadAffinity=false`, ParallelGC).
- Lock single-instance por host: un sqcli/GUI vivo bloquea el siguiente boot ("It seems another instance...") — respetado por preflight en el harness.

## 4. Suministro de trabajo por tipo de stage (durable pipeline, `steps.go`)

- **Retester durable**: 1 corrida sqcli retestea el databank upstream COMPLETO del chunk (`steps.go:377-379, 513-537`); descarga N `.sqx` al databank input del proyecto (`DownloadDurableToCustom` → `databanks/input`, `minio_storage.go:81-128` + `GetSQXPaths`); el tamaño del chunk lo fija `batch_size` del group.
- **Final reretester**: exactamente 1 estrategia por invocación (`steps.go:403-427`) — contrato de fidelidad.
- **Optimizer**: exactamente 1 estrategia upstream (`steps.go:467-468`); el WFO interno de SQX paraleliza los combos (pico medido 72,6 cores).
- **Builder**: proyecto con task Build (template/acciones según etapa); el pool genético usa todos los cores mientras dura la generación (medido 68,5 cores sostenidos).
- Semántica congelada por el owner (2026-09-28): `batch_size` = paralelismo interno SQX por host; `max_parallel` = sqcli concurrentes ENTRE hosts.

## 5. Implicación para CPU

Con este contrato, la CPU por host = función directa de (unidades de trabajo por corrida) × (corridas concurrentes permitidas=1). SQX multiplica bien: la palanca es `batch_size` del retester (y la secuencialidad fail-closed de groups con `source`), no el motor ni el launcher.

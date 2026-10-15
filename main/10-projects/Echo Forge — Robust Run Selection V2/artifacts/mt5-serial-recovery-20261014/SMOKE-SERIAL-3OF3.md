# MT5_SERIAL_SMOKE_3_OF_3 — Evidencia física (2026-10-14/15)

**STATUS: MT5_SERIAL_SMOKE_3_OF_3_PASS**

## Mecanismo de prueba

Tres ejecuciones directas del workflow registrado `MT5BacktestArtifactWorkflow`
(Temporal namespace `sqx-prop`, task queue `sqx-main-queue`), despachadas
concurrentemente, con EX5 auténticos del cohort wave2b (durable
`durable/mt5-export/v1/cd697133-4d2a-49d3-bd24-45c391b404d8/<strategyRef>/sha256:<digest>/06_mt5_ex5/…​.ex5`,
tamaños y SHA256 verificados antes del despacho). Salidas publicadas bajo
`…/07_smoke_serial_20261014/` (carpeta nueva, sin tocar la evidencia terminal
de wave3s en `07_mt5_backtest/`).

## Workflows

| WorkflowId | StrategyRef | EX5 sha256 (input) | status | HTM durable (size) |
|---|---|---|---|---|
| smoke-serial-01-r3-20261014 | 02ca621f-100d-4e74-8769-967a96450061 | ab2de4db45d4…e7f6e3 (218748 B) | success | final-02ca621f….htm (4.051.508 B) |
| smoke-serial-02-r3-20261014 | 3bf04cb9-5c35-4e4a-b58e-f1e284ee84e9 | 48a263c35973…ac8544f2 (218734 B) | success | final-3bf04cb9….htm (708.948 B) |
| smoke-serial-03-r3-20261014 | 89171ea6-9ece-4f15-acee-c79da3abc288 | 92b025f2642b…538b7f20 (220836 B) | success | final-89171ea6….htm (2.029.296 B) |

Cada resultado trae `input` (key/size/sha256 del EX5 ejecutado, verificado por
el worker contra el durable ref — contratos `FetchDurableToPath` +
`validateLocalArtifactAgainstDurable`) y 4 evidencias
(`.tester.ini`, `.terminal.log`, `.tester.log`, `.agent.log`) publicadas en
MinIO `sqx-strategies` bajo el prefijo durable de cada estrategia.

## Condiciones verificadas

1. **Una ejecución completa por vez** — watcher `smoke_watch.log` (2 s de
   cadencia): terminal 20868 vivo 21:51:53→21:55:46, gap, terminal 25672 vivo
   21:56:30→22:00:13, gap, tercer terminal 22:00:37→22:04:09. Nunca `terminals>1`.
2. **Reporte HTM válido** — 3/3 HTM durables no vacíos (tabla arriba).
3. **Journals frescos** — 12 objetos de evidencia (3× ini+terminal+tester+agent)
   con mtime 2026-10-15T00:56Z, publicados por la activity.
4. **Evidencia del slot utilizado** — `C:\MT5\slots\slot-2\logs\20261014.log`:
   tres bloques `Startup successfully initialized from start config
   "C:\MT5\slots\slot-2\EchoForgeJobs\smoke-serial-0X-r3-20261014\…\tester.ini"`
   → `last test passed "successfully finished"` → `exit with code 0`
   (3:43.1, 3:33.6, 3:21.8). Lease física `slot-2` visible en el watcher.
5. **Ningún terminal simultáneo** — watcher, nunca >1.
6. **Cero fallos por ausencia de journal** — los deltas de journals se
   escribieron 3/3 (el fallo journal-contract de INFRA-1 no reapareció).
7. **Sin colisión de lease ni workspace** — workspaces
   `EchoForgeJobs\smoke-serial-0X-r3-20261014` exclusivos y limpiados por
   attempt; leases adquiridas y liberadas serialmente.
8. **Reconciliación con los EX5** — SHA256 del `input` de cada resultado ==
   SHA256 del objeto durable EX5 descargado y hasheado antes del despacho.

## Intento previo r2 (no-pass, conserva evidencia)

Los workflows `smoke-serial-0{1,2,3}-r2-20261014` y `smoke-serial-04-good-20261014`
(4/4 con el EX5 del éxito wave3s) terminaron `failed/report_not_found`: el tester
corría íntegro ("last test passed", CSV del EA, balance final idéntico al éxito)
pero el terminal no escribía el HTM, con cualquier launcher (worker 0.2.141,
schtasks kor session-0). Causa: degradación del stack gráfico/sesión del host
(los terminales en session 0 mostraban `MDI create failed`/`create frame failed`
y sin precarga del experto). Fix operativo: `tscon 2 /dest:console` (sesión KoR
Disc→Active en consola), zombie `MetaEditor64` (C:\MT5\test, vivo desde 12-oct,
ocupaba 127.0.0.1:22345) terminado, y worker 0.2.141 movido a tarea programada
interactiva `EchoForgeMT5WorkerSession` (misma supervisión de release vía
CURRENT del stager; servicio StagerRuntime detenido y Disabled). Tras el cambio,
el probe interactivo y los 3 smoke pasaron.

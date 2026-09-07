---
type: project
owner: agent
root: false
cssclasses:
  - wide
status: completed
priority: P1
area: "[[Echo]]"
parent: "[[Echo Forge]]"
sprint:
start: 2026-08-06
due: 2026-08-14
progress: 100
repo: symphony
jira:
prs:
tags:
  - area/echo
  - kind/project
created: 2026-08-06
updated: 2026-08-14
aliases:
  - Echo Forge - Etapa 6
  - Etapa 6 MT5
  - backtesting MT5
---
# Echo Forge - Etapa 6: Compilación y Backtesting MT5

> [!info]+ Echo Forge - Etapa 6: Compilación y Backtesting MT5
> **Padre:** [[Echo Forge]] · **Área:** [[Echo]] · **Estado:** done · **Prioridad:** P1 · **Progreso:** 100%
> Dos task types atómicos: `mt5_compiler` y `mt5_backtesting`. Cerrada 2026-08-14: F10 observado y F11 PASS.

## 🎯 Objetivo

- Cerrar la validación real en MetaTrader 5 agregando **dos tareas atómicas e independientes** al pipeline dinámico de Echo Forge, cada una con fan-out de una subtarea por estrategia, ejecutadas en un worker de clase MT5 sobre Windows, y depositando sus artefactos crudos en MinIO bajo la convención de rutas existente.
- Formalizar el **tipado de workers por clase** (`sqx` / `mt5`) mediante task queues de Temporal, para que el flujo despache cada task type a la máquina que tiene el software que necesita.

## 📊 Estado actual

- **Cerrada PASS (100%, 2026-08-14)**: F10 observado contra binarios `0.2.42` (no `f33-lifecycle`). Temporal `sqx-main-00_configs-v1-XAUUSD-H1-L-1786733372` **Completed**; MinIO `example_flow_3` con 12 `.ex5` y 12 `.htm`; Windows worker como `kor`. F11 PASS: cobertura nueva 85.02%, race dirigido, vet/gofmt, anti-masking, builds Linux/Windows. Residual: journals UTF-16 vs sanitizer UTF-8 ([[symphony-mt5-utf16-journal-sanitizer-bypass]]). Fuera de alcance: parseo Mongo, desviación SQX vs MT5, Etapas 5/7.
- **Git**: feature `6b0fa42` mergeada a `master` `b6e7629` y pusheada (`c616cc8..b6e7629`). T11.14 incluido. Workers siguen en `0.2.42`; el merge no redeploya.
- **Plan de ejecución**: F0–F11 completas. Cierre de producto hecho.

## 🧭 Alcance decidido

### Dentro

- Task type `mt5_compiler`: toma cada `.mq5` de `source_folder` en MinIO, lanza una subtarea por archivo, compila con MetaEditor64 y deja el `.ex5` en MinIO bajo `folder`.
- Task type `mt5_backtesting`: toma cada `.ex5` de `source_folder`, lanza una subtarea por estrategia, ejecuta el Strategy Tester y sube el reporte `.htm` (más `tester.ini` y logs) a MinIO bajo `folder`, con el nombre de la estrategia.
- Clases de worker por task queue, con la afinidad `task type → clase` declarada en un único registro.
- Despliegue del `sqx-mt5-worker` en la máquina Windows y smoke test E2E real.

### Fuera (deliberadamente)

- Parseo de métricas, normalización a modelo canónico y escritura en Mongo: es trabajo de tareas posteriores que consumirán los artefactos desde MinIO.
- Filtro de desviación SQX vs MT5 y cualquier gate que descarte estrategias.
- Inyección de parámetros vía `.set` / `TesterInputs`: el EA exportado por SQX ya trae sus parámetros.
- Optimización, modo visual, agentes remotos/cloud, pool de instalaciones MT5, publish en demo, NinjaTrader.

## 🔍 Contexto verificado en el repo (2026-08-06)

| Hecho | Evidencia |
|---|---|
| `mt5_exporter` ya hace fan-out por estrategia y sube un `.mq5` por estrategia a MinIO | `sqx/activities/worker/robust_activity.go:1206-1253` |
| La ruta MinIO es determinista por identidad lógica, sin segmento por ejecución | `sqx/core/domain/paths.go` — `BuildMinIOPath(wave, inst, dirCode, tf, strategy, version, folder, filename)` |
| Existe worker Windows con dos activities registradas en la queue MT5 | `sqx/cmd/sqx-mt5-worker/main.go:151-153` |
| Adapters MT5 completos: compiler, runner, parser | `sqx/adapters/mt5/{compiler,runner,parser}.go` |
| Las queues ya están declaradas como constantes | `sqx/core/adaptive/contracts.go:32-35` → `sqx-main-queue`, `sqx-mt5-queue` |
| `generic_workflow.go` usa **una sola** queue para todo, leída de `sqx/task_queue` | `sqx/workflows/generic_workflow.go:1233`, `:1371`, `:1517` |
| `adaptive_workflow.go` ya encadena compile → backtest → deviation, pero es un workflow paralelo que **no** consume el `config.json` | `sqx/workflows/adaptive_workflow.go:277-285`, `:454-474` |
| Mongo ya sabe persistir resultados MT5 (queda sin uso en esta etapa) | `capabilities.MT5BacktestWriter` / `MT5BacktestReader` en `sqx/core/capabilities/mt5.go:19-27` |
| El worker MT5 registra activities, pero no workflows | `sqx/cmd/sqx-mt5-worker/main.go:151-153` |
| Los child workflows sólo están registrados en el worker principal | `sqx/cmd/sqx-worker/main.go:322-327` |
| La concurrencia de activities ya está fijada globalmente en 1 | SDK `pkg/shared/temporal/client.go` — `MaxConcurrentActivityExecutionSize: 1` |
| La validación real del `config.json` ocurre en el watcher y hoy sólo revisa campos raíz | `sqx/activities/watcher/steps.go:147-165`; `NewRuntimeConfig` no está en esa ruta |
| Línea base focalizada en PASS | `go test ./adapters/mt5`; `go test ./activities/worker -run TestMT5`; workflows Generic/Group |

### Hallazgos que hay que corregir

| ID | Hallazgo | Impacto |
|---|---|---|
| H1 | `MT5Compile` descarta la key del `.ex5` (`_ = ex5Key`) y el backtest la reconstruye asumiendo `{strategyID}.mq5` o `candidate.EchoRef`, **no** el layout de `BuildMinIOPath` con wave/instrument/folder | `sqx/activities/worker/mt5_activities.go:61`, `:200-217` — las activities MT5 hoy no saben leer las keys que produce el pipeline real |
| H2 | `MT5Backtest` es batch: itera `Picks` dentro de un único activity | `sqx/activities/worker/mt5_activities.go:87-91` — incompatible con "una subtarea por estrategia" |
| H3 | El runner borra su workspace (`defer os.RemoveAll`) y no sube reporte ni logs | `sqx/adapters/mt5/runner.go:68` — hoy no queda evidencia auditable |
| H4 | `tester.ini` escribe `Period` como minutos (`60`) en vez de `H1` | `sqx/adapters/mt5/runner.go:175`, `:191-210` |
| H5 | Falta `ReplaceReport=1`, `Visual=0`, `UseLocal=1`, `UseRemote=0`, `UseCloud=0` en el `tester.ini` | `sqx/adapters/mt5/runner.go:165-189` |
| H6 | El `tester.ini` escribe login/password/server de la cuenta demo | `sqx/adapters/mt5/runner.go:167-171` — es el GAP `EF-G27` del backlog del padre; se cierra quitando `[Common]` |
| H7 | El runner mezcla ejecución, recolección y parseo en un solo método | `sqx/adapters/mt5/runner.go:50-114` — viola SRP y bloquea la separación "artefactos ahora, parseo después" |
| H8 | El plugin Java nombra el `.mq5` con `strategyName.replaceAll("[^a-zA-Z0-9\\-_]", "_")`, **no** con `CanonicalStrategyID` | `sqx/exporter-plugin/src/.../EchoForgeMT5Exporter.java:64-65` — el nombre en MinIO no round-trippea con la identidad canónica de Go, y eso rompe el requisito de que el artefacto se llame como la estrategia (`strategy-1.2.4.htm`) |
| H9 | `mt5_compile` y `mt5_backtest` son nombres y contratos ya consumidos por `adaptive_workflow.go` | Reescribirlos para las tareas nuevas rompe BWC. Las nuevas activities deben tener nombres y payloads propios; los puertos legacy se mantienen |
| H10 | El diseño anterior mandaba el child workflow a `sqx-mt5-queue`, pero esa queue no tiene workflows registrados | El child quedaría `Running` sin ejecutor. El child hereda la queue principal; sólo su activity nativa se despacha a MT5 |
| H11 | El ejemplo usa `Model=4`, pero `domain.TickModelRealTicks` vale `5`; además el INI anterior serializaba `Leverage=100` | Documentación oficial MT5: real ticks es `4` y leverage es `1:100`; el contrato actual debe corregirse sin tocar el parser |
| H12 | Agregar validación sólo en `NewRuntimeConfig` no protege el flujo real | La validación de tasks debe centralizarse y ser llamada por `ValidateSpecStep` antes de disparar Temporal |
| H13 | `list_strats` elimina el path y no filtra extensión | Para encadenar stages sin reconstruir keys se requiere una activity de artefactos que devuelva full keys, ordenadas, deduplicadas y filtradas |
| H14 | El plan prometía `terminal.log` y `tester.log` sin conocer su directorio físico ni cómo aislar las líneas de esta ejecución | F0 debe fijar los paths y el algoritmo de snapshot por offset/tiempo; está prohibido subir logs históricos completos |
| H15 | Se proponían nuevas claves `temporal/queue/*` pese a que ya existe la deuda `sqx/task_queue` vs `temporal/task_queue` | No se introduce un tercer esquema. Se mantienen `sqx-main-queue` / `sqx-mt5-queue`; unificar claves queda fuera de esta etapa |
| H16 | El WorkflowID propuesto omitía el request y podía colisionar en re-ejecuciones | Debe incluir `request_id` y hash corto de la full source key: determinista dentro del job y único entre jobs |

### Estado SDD de la feature en el repo

`FEAT-SQX-MT5-BACKTEST-COMPILE` tiene una implementación base verificada en PASS y un `CHANGE-001` aprobado pero pendiente. Ese delta mezcla reportes crudos, métricas, trade lists, checksums, lineage, credenciales y compile reusable; este proyecto sólo cubre una parte.

1. subir reporte crudo, JSON normalizado y trades con checksums;
2. publicar métricas bajo el catálogo canónico;
3. integrar el eslabón `mt5_result` en `strategy_lineage`;
4. purgar credenciales del `.ini` después de ejecutar;
5. exponer `compile_and_upload` reutilizable.

No se sobrescriben el `PLAN.md`, `TASKS.md` ni `VERIFICATION.md` históricos de esa implementación. F0 crea la feature SDD separada `FEAT-SQX-MT5-PIPELINE-ARTIFACTS`, que referencia la capacidad base y declara exactamente los dos task types del pipeline dinámico. `CHANGE-001` queda enlazado con una tabla `cubierto / pendiente`, sin fingir que lineage, métricas o sidecars fueron implementados.

`specs/SPECS.md` está **correcto** al mostrar `Spec-Active (+CHANGE-001 Approved)`: un PASS histórico no cierra un delta aprobado aún pendiente. Sólo se agrega la nueva feature al catálogo y su estado avanza por el ciclo SDD normal.

## 🏗️ Diseño

### Flujo objetivo en `config.json`

```json
{
  "type": "mt5_exporter",
  "source_folder": "05_reretester",
  "folder": "07_mt5_mq5"
},
{
  "type": "mt5_compiler",
  "source_folder": "07_mt5_mq5",
  "folder": "08_mt5_ex5"
},
{
  "type": "mt5_backtesting",
  "source_folder": "08_mt5_ex5",
  "folder": "09_mt5_backtest",
  "mt5": {
    "symbol": "XAUUSD",
    "period": "H1",
    "from": "2024.01.01",
    "to": "2025.12.31",
    "model": 4,
    "execution_mode": 0,
    "deposit": 10000,
    "currency": "USD",
    "leverage": 100,
    "timeout": "30m"
  }
}
```

`symbol` y `period` son obligatorios; no se infieren del root. Validación mínima: `model ∈ {0,1,2,3,4}`, `execution_mode == -1 || 0..600000`, fechas válidas con `from <= to`, `deposit > 0`, `currency` de tres letras, `leverage > 0` y `timeout` parseable y positivo. `leverage: 100` en JSON se serializa como `Leverage=1:100`.

### Anatomía común de las dos tareas

Ambas comparten exactamente la misma mecánica; la única diferencia es qué binario invocan y qué artefactos recolectan.

```text
Padre (GenericSQXWorkflow o GroupSQXWorkflow; queue principal)
  1. list_mt5_artifacts(source_folder, extension) -> full keys ordenadas
  2. por cada full key: child workflow que HEREDA la queue principal
     WorkflowID = mt5-<op>-<request_id>-<hash(source_key)>
  3. el child ejecuta una activity en sqx-mt5-queue
  4. junta todos los resultados, incluso errores de child; nunca corta al primero
  5. current.Keys = basenames de los artefactos exitosos; Origin se conserva

Child (workflow en queue principal)
  a. configura ActivityOptions con TaskQueue=sqx-mt5-queue
  b. ejecuta exactamente una estrategia
  c. devuelve ArtifactTaskResult estructurado

Activity física (worker MT5; concurrencia 1 ya impuesta por SDK)
  a. workspace <jobs_root>/<request_id>/<activity_id>-<attempt>/{input,output,logs}
  b. descarga por full source key; jamás reconstruye la key desde StrategyID
  c. invoca el binario con timeout, cancelación y heartbeat
  d. sube evidencia antes de limpiar
  e. elimina sólo su workspace y su subcarpeta de Expert
```

### Task 1 — `mt5_compiler`

- **Identidad**: la full source key es la autoridad; `artifact_stem` es el basename sin `.mq5`, tratado como string opaco. No se intenta revertir el sanitizado Java ni aplicar `CanonicalStrategyID`.
- **Output key**: reemplazar exactamente el segmento `source_folder` por `folder` y la extensión; error si el segmento no aparece exactamente una vez.
- **Pasos**: descarga → copia a `<mql5_root>/Experts/EchoForge/<activity_id>/<stem>.mq5` → MetaEditor → valida `.ex5` → sube `.ex5` y `compile.log` → limpia.
- **Fallo funcional**: `compilation_failed` se devuelve como `ArtifactTaskResult{status:"failed"}` con `compile.log` ya subido y sin Go error, para que el padre continúe. Errores de storage/infra se propagan para retry de Temporal.

### Task 2 — `mt5_backtesting`

- **Identidad y output key**: misma regla opaca que compiler, ahora `.ex5` → `.htm` y sidecars en el stage `folder`.
- **Pasos**: descarga → copia a una subcarpeta única de `MQL5/Experts/EchoForge` → snapshot de offsets de logs → genera INI → terminal64 → verifica reporte no vacío → captura sólo el delta de logs → sube → limpia.
- **Salida requerida en éxito**: `<stem>.htm`, `<stem>.tester.ini`, `<stem>.terminal.log`, `<stem>.tester.log`, `<stem>.agent.log`. F0 localizó y capturó los tres journals por delta; la implementación no puede volverlos opcionales por cuenta propia.
- **Sin parseo, sin Mongo**: el `.htm` se sube byte a byte sin llamar `ParseReportHTML`.
- **Fallo funcional**: `backtest_timeout` y `report_not_found` retornan resultado `failed` con toda evidencia disponible. Fallos de storage/infra sí retornan error retryable.

`tester.ini` objetivo:

```ini
[Tester]
Expert=EchoForge\<activity_id>\<strategy>
Symbol=<mt5.symbol>
Period=<mt5.period>
Model=<mt5.model>
ExecutionMode=<mt5.execution_mode>
Optimization=0
UseDate=1
FromDate=<YYYY.MM.DD>
ToDate=<YYYY.MM.DD>
Deposit=<mt5.deposit>
Currency=<mt5.currency>
Leverage=1:<mt5.leverage>
Report=<patrón verificado en F0; sin extensión para que MT5 produzca .htm>
ReplaceReport=1
ShutdownTerminal=1
Visual=0
UseLocal=1
UseRemote=0
UseCloud=0
```

Sin sección `[Common]`: la terminal ya está logueada en la máquina y las credenciales no las administra el sistema. Esto cierra el GAP `EF-G27`.

### Clases de worker y task queues

El registro de afinidad es puro y acotado a las dos tareas nuevas. No consulta ETCD dentro de un workflow y no reemplaza el routing de tasks existentes:

```go
// sqx/core/runtime/worker_affinity.go
type WorkerClass string

const (
    WorkerClassSQX WorkerClass = "sqx" // máquina con StrategyQuant
    WorkerClassMT5 WorkerClass = "mt5" // máquina Windows con MetaTrader 5
)

func WorkerClassOf(taskType string) (WorkerClass, bool)
func QueueOf(class WorkerClass) string
```

- `mt5_compiler` y `mt5_backtesting` → `WorkerClassMT5`; el helper nuevo sólo se invoca desde esos cases.
- Los child workflows heredan la queue principal y sólo sus activities usan `QueueOf(WorkerClassMT5)`.
- Se mantienen `sqx-main-queue` y `sqx-mt5-queue`. Renombrar o unificar `sqx/task_queue` con `temporal/task_queue` queda fuera por riesgo de despliegue coordinado.

### Mapa de impacto de archivos

| Zona | Cambios permitidos |
|---|---|
| Contratos | `sqx/core/runtime/config.go`, nuevos `mt5_task_config.go`, `worker_affinity.go`, `sqx/core/domain/mt5_artifacts.go`, `artifact_paths.go`, `sqx/core/capabilities/mt5.go` con APIs **aditivas** |
| Validación/listado | `sqx/activities/watcher/steps.go`, nuevo `sqx/activities/worker/list_mt5_artifacts.go` |
| Físico MT5 | Nuevos `sqx/adapters/mt5/artifact_compiler.go` y `artifact_runner.go`; `parser.go` y los métodos legacy quedan prohibidos |
| Temporal | Nuevo `sqx/activities/worker/mt5_artifact_activities.go`, nuevos child workflows y helper compartido; cases mínimos en ambos switches de `generic_workflow.go` |
| Wiring | `sqx/cmd/sqx-worker/main.go` registra list activity + child workflows; `sqx/cmd/sqx-mt5-worker/main.go` registra sólo activities nuevas y carga config física una vez al boot |
| SDD/ops | Nueva `specs/FEAT-SQX-MT5-PIPELINE-ARTIFACTS/`, catálogo, script/runbook Windows y fixtures sanitizados |

### Archivos prohibidos durante implementación

- `sqx/workflows/adaptive_workflow.go`, `sqx/core/adaptive/contracts.go` y las activities `MT5Compile` / `MT5Backtest` existentes.
- `sqx/adapters/mt5/parser.go` y persistencia Mongo.
- Tests existentes. Cada fase crea tests nuevos; si uno existente debe cambiar, se detiene y abre `TEST_CHANGE_REQUEST.md`.
- CI, fixtures no relacionados, deployers Linux y cualquier rename de task queues.

## 🧱 Contrato de despacho entre agentes

- **Unidad de trabajo**: una fase = un agente = un commit revisable. Ningún agente empieza F(n+1) sin gate PASS y handoff de F(n).
- **Contexto mínimo**: leer `AGENTS.md`, `CONSTITUTION.md`, las reglas SDD, `## 📊 Estado actual`, este contrato, la fase asignada y la última línea de bitácora. No releer toda la historia si no cambia una decisión.
- **Rama única**: `feature/feat-sqx-mt5-pipeline-artifacts` desde `master`; un commit por fase. No crear una rama/PR por microtarea.
- **Worktree**: preservar cambios ajenos. La auditoría encontró `deployer_screen.log` modificado y no relacionado; no tocarlo.
- **Disciplina SDD**: Coordinator escribe SPEC/PLAN/TASKS; Implementor sólo Allowed Files de su fase; Verifier sólo VERIFICATION. No mezclar roles.
- **Tests**: no modificar tests existentes ni bajar assertions/cobertura. Los tests físicos usan command/storage fakes; sólo F0/F10 ejecutan MT5 real.
- **Resultado estándar**: cada fase termina actualizando su checkbox, una línea de bitácora y un handoff con commit, archivos, comandos, resultados, riesgos y siguiente fase.
- **Stop conditions**: contrato ambiguo, output key no derivable, fixture con secreto, necesidad de tocar un archivo prohibido, test baseline que falla fuera de la limitación ya registrada, o discrepancia con F0. Detenerse; no inventar fallback.

## 🪜 Fases implementables de peso equivalente

Cada fase apunta a una sesión de agente mediana: un outcome, un commit, entre dos y seis archivos productivos, tests nuevos focalizados y un gate binario. Las fases operacionales/documentales se consideran del mismo peso por acceso físico, evidencia y revisión humana, no por cantidad de líneas.

### F0 — Contrato físico Windows + SPECIFY

- **Rol**: Coordinator (`arquitecto-autor`) sin acceso directo a la VM Windows. El agente prepara el paquete reproducible y el owner ejecuta el spike físico en PowerShell; MinIO se inspecciona mediante los clientes existentes. Cero código productivo.
- **Entrada**: decisiones D1-D12, instalación real MT5 logueada y un `.mq5` producido por `EchoForgeMT5Exporter`.
- **Permitido**: crear `specs/FEAT-SQX-MT5-PIPELINE-ARTIFACTS/SPEC.md`, `evidence/WINDOWS-CONTRACT.md` y fixtures sanitizados; agregar la fila `Spec-Active` a `specs/SPECS.md` tras aprobación del SPEC.
- **Procedimiento**:
  1. Clasificar como `CAPABILITY_SPEC` de integración dinámica; enlazar la feature MT5 base y `CHANGE-001` sin reescribirlos.
  2. Registrar, sin secretos, rutas de `MetaEditor64`, `terminal64`, installation root, data root, `MQL5` root, Experts, jobs root, reportes, terminal logs y tester logs.
  3. Listar full keys reales `.mq5`; probar que el cambio de segmento de stage produce keys destino no ambiguas.
  4. Compilar manualmente dentro de una subcarpeta de `MQL5/Experts/EchoForge`; confirmar includes, nested Expert path y nombre del `.ex5`.
  5. Ejecutar backtest manual sin `[Common]`, con `Period=H1`, `Model=4`, `Leverage=1:100`; confirmar símbolo broker, ticks del rango, `Report` relativo/absoluto, extensión `.htm` y paths de logs.
  6. Capturar `.htm`, INI, compile log y deltas de logs sanitizados. Confirmar que el EA usa parámetros default horneados y no necesita `.set`.
- **Gate PASS**: SPEC aprobada por el owner; `WINDOWS-CONTRACT.md` no tiene NEED-INFO; fixtures sin cuenta, password, IP privada ni logs históricos. Si falla cualquier punto, F1 no parte.

### F1 — PLAN/TASKS SDD + baseline reproducible

- **Rol**: Coordinator (`arquitecto-revisor`). Cero código y cero edición de tests.
- **Permitido**: sólo `PLAN.md`, `TASKS.md`, links de `SPEC.md` y estado de catálogo de la feature nueva.
- **Procedimiento**: traducir F0 y esta nota a Allowed/New/Prohibited Files exhaustivos por fase; congelar payloads JSON/Temporal, matriz de errores retryable/no retryable, rutas de artefactos, rollout y rollback. Hay dos pausas obligatorias dentro de la fase: aprobación de `PLAN.md` antes de escribir `TASKS.md`, y aprobación de `TASKS.md` antes de abrir implementación. Usar la rama única abierta desde `master@c616cc8` y registrar el commit base.
- **Baseline obligatorio**: `go test ./adapters/mt5`; `go test ./activities/worker -run TestMT5`; `go test ./workflows -run 'Test.*(Generic|Group|SQXE2E)'`; `go test ./core/runtime ./core/adaptive`.
- **Gate PASS**: PLAN aprobado y TASKS aprobado; cada tarea refleja exactamente F2-F11; ningún archivo legacy o test existente aparece como editable. Suite focalizada PASS o excepción preexistente documentada con evidencia.

### F2 — Contratos, configuración y validación real

- **Rol**: Implementor (`artesano`).
- **Permitido**: `sqx/core/runtime/config.go`; nuevos `mt5_task_config.go` y tests; nuevo `sqx/core/domain/mt5_artifacts.go` y tests; `sqx/activities/watcher/steps.go`; test nuevo exclusivo para validación MT5.
- **Implementar**: bloque `TaskSpec.MT5`; validación recursiva de tasks y groups llamada por el watcher real; `ArtifactRef`, `ArtifactTaskRequest`, `ArtifactTaskResult`, status/error codes; constantes correctas de modelo MT5 sin cambiar payloads adaptive existentes.
- **Casos de test mínimos**: config compiler válida sin bloque MT5; backtesting válido; symbol/period/fechas/model/execution/deposit/currency/leverage/timeout inválidos; task dentro de group; JSON round-trip; input no mutado.
- **Gate PASS**: `go test ./core/runtime ./core/domain ./activities/watcher`; `go vet` de esos packages; cero cambio en `core/adaptive`.

### F3 — Derivación de keys, listado y afinidad

- **Rol**: Implementor.
- **Permitido**: nuevos `sqx/core/domain/artifact_paths.go`, `sqx/core/runtime/worker_affinity.go`, `sqx/activities/worker/list_mt5_artifacts.go` y sus tests; registro de list activity en `sqx/cmd/sqx-worker/main.go`.
- **Implementar**: sustitución exacta de un segmento de stage; extensión esperada case-insensitive; rechazo de path traversal, segmento ausente/duplicado y stem vacío; listado de full keys con filtro, sort y dedupe; mapa puro `task type → WorkerClass` y `WorkerClassMT5 → adaptive.QueueMT5` sin I/O ni ETCD en workflow.
- **Gate PASS**: tests table-driven cubren keys reales de F0, duplicados, extensiones ajenas y errores; build de `sqx-worker`; ninguna key se reconstruye con `CanonicalStrategyID`.

### F4 — Compiler físico orientado a artefactos

- **Rol**: Implementor.
- **Permitido**: extensión aditiva en `sqx/core/capabilities/mt5.go`; nuevo `sqx/adapters/mt5/artifact_compiler.go` y test nuevo. Prohibido modificar `compiler.go` legacy salvo `TEST_CHANGE_REQUEST` aprobado.
- **Implementar**: una estrategia por llamada; config inmutable recibida por constructor; workspace y Experts subfolder por activity/attempt; download por full key; MetaEditor; collect `.ex5` y compile log; upload a keys derivadas; cleanup después de upload.
- **Errores**: compilación/missing EX5 → resultado funcional failed con log; download/upload/FS inesperado → error propagado; cancelación respeta `ctx`.
- **Gate PASS**: tests success, compiler exit no-cero, EX5 ausente, upload fallido, cancelación y cleanup; `go test ./adapters/mt5`; legacy tests sin cambios y PASS.

### F5 — Activity y child workflow de compiler

- **Rol**: Implementor.
- **Permitido**: nuevo `sqx/activities/worker/mt5_artifact_activities.go` y test; nuevo `sqx/workflows/mt5_compile_workflow.go` y test; wiring mínimo en ambos `cmd` workers.
- **Implementar**: activity name nuevo, no `mt5_compile`; conversión de errores funcionales a result; heartbeat; child de una source key que hereda queue principal y ejecuta activity en `sqx-mt5-queue`; registrar workflow sólo en main y activity sólo en MT5.
- **Gate PASS**: test Temporal afirma explícitamente queue del child y queue de la activity; build de ambos workers; `adaptive_workflow` y activities legacy siguen compilando y pasando.

### F6 — Integración `mt5_compiler` en ambos intérpretes

- **Rol**: Implementor.
- **Permitido**: `sqx/workflows/generic_workflow.go` y un test nuevo de integración compiler. No copiar dos implementaciones: ambos cases llaman el mismo helper puro/workflow.
- **Implementar**: listar siempre desde `source_folder`; fan-out de children con ID `request_id + hash(full key)`; recolectar todos los futures; continuar ante result failed o child error agotado; mantener sólo `.ex5` exitosos en `current.Keys`; telemetría de total/success/failed sin alta cardinalidad.
- **Gate PASS**: tests Generic y Group con 2 éxitos, 1 fallo funcional y 1 child error; rerun con otro request ID no colisiona; task desconocido sigue fallando; suite completa de workflows PASS.

### F7 — Runner físico crudo e INI correcto

- **Rol**: Implementor.
- **Permitido**: extensión aditiva en capability; nuevo `sqx/adapters/mt5/artifact_runner.go` y test nuevo. `runner.go` y `parser.go` legacy quedan prohibidos.
- **Implementar**: config física inmutable cargada al boot; download/copy del EX5; INI sin `[Common]` ni `TesterInputs` inventado; valores exactos validados en F0; ejecución con timeout/cancelación; localizar `.htm` no vacío sin parsearlo; cleanup diferido hasta que el caller recolecte.
- **Gate PASS**: golden INI prueba ausencia de credenciales, `Model=4`, `Period=H1`, `Leverage=1:100`, flags locales y report path; tests timeout, cancel, report missing/empty y `ParseReportHTML` no invocado; adapters legacy PASS.

### F8 — Evidencia, upload y activity de backtesting

- **Rol**: Implementor.
- **Permitido**: completar `artifact_runner.go`; nuevo helper de log snapshot si hace falta; extender `mt5_artifact_activities.go`; tests nuevos; wiring de activity en MT5 worker.
- **Implementar**: snapshot de offsets antes del proceso y sólo delta posterior; recolectar los cuatro artefactos; subirlos antes del cleanup; no subir log previo; failed result para timeout/report missing con evidencia disponible; infra errors retryable.
- **Gate PASS**: tests prueban los cinco objetos en éxito, evidencia parcial en fallo, exclusión de líneas históricas y cleanup; scan de fixtures/INI sin secretos; build Windows del worker.

### F9 — Child + integración `mt5_backtesting`

- **Rol**: Implementor.
- **Permitido**: nuevo `sqx/workflows/mt5_backtest_workflow.go` y test; `generic_workflow.go`; wiring de workflow en main worker; test nuevo de integración.
- **Implementar**: child por full `.ex5` key, activity en MT5 queue, mismo agregador compartido que compiler; cases en Generic y Group; `current.Keys` sólo con `.htm` exitosos; failures completos sin abortar.
- **Gate PASS**: mismos escenarios de F6 más timeout y report missing; assertions de routing; `go test ./workflows ./activities/worker ./adapters/mt5`; build de ambos workers.

### F10 — Despliegue Windows y smoke E2E real

- **Rol**: operador/Implementor con acceso Windows. No cambiar contratos.
- **Permitido**: script de despliegue Windows dedicado, runbook, config de ejemplo y evidencia E2E sanitizada; no deployers Linux.
- **Procedimiento**: cross-compile; backup recuperable del binario anterior; poblar sólo claves ETCD aprobadas por F0 (`MetaEditor64/binary_path`, `terminal64/binary_path`, roots físicos y timeout); confirmar poll en `sqx-mt5-queue`; ejecutar 2 estrategias válidas y 1 fixture de fallo; re-ejecutar el mismo config con request nuevo.
- **Verificación**: cada válida produce 2 artefactos compiler + 5 backtest; fallo conserva evidencia y no corta las otras; mismas keys se sobrescriben sin sufijos; child count/queues correctos en Temporal; workspace y Expert subfolders limpios; ningún INI/log contiene credenciales.
- **Gate PASS**: evidencia MinIO + Temporal + worker, comandos y rollback documentados; rollback ensayado o validado de forma no destructiva.

### F11 — Verificación independiente y handoff

- **Rol**: Verifier distinto de los implementors (`esceptico` + revisión de telemetría). Sólo edita `VERIFICATION.md` y estados SDD autorizados.
- **Procedimiento**: revisar diff contra Allowed Files; ejecutar `go fmt`, `go vet`, `staticcheck`, `go test -race -cover ./...` desde `sqx`, anti-test-masking y builds Linux/Windows; auditar BWC del adaptive workflow, determinismo Temporal, manejo de secretos, cleanup, retries, telemetría y evidencia F10.
- **Gate PASS**: cero BLOQ/MAY; cobertura del código nuevo ≥85%; VERIFICATION PASS; feature nueva `Completed`; `CHANGE-001` muestra honestamente qué GWT siguen pendientes. Si falla, reabre la fase responsable y no maquilla tests.
- **Entrega**: todas las tareas de este proyecto en `[x]`, progreso 100%, estado listo para Review y tarea puente del padre `[/] → [r]`; sólo el owner puede marcarla `[x]`.

## 🧠 Asignación de inteligencia y modelos

La carga es de **razonamiento y riesgo de decisión**, no de cantidad de líneas. Las fases fueron diseñadas con peso operativo parecido, pero no tienen la misma complejidad cognitiva. Esta es la asignación base para el pool disponible; los gates y la revisión humana siguen siendo obligatorios.

| Nivel | Fases | Por qué | Modelo recomendado | Uso de los demás modelos |
|---|---|---|---|---|
| **L5 — máxima** | **F0, F1, F6, F9, F11** | Definen o auditan contratos irreversibles, SDD, semántica Temporal entre dos intérpretes, tolerancia a fallos y regresión global. Un error se propaga a todo el pipeline. | **GPT Sol** como responsable. F0 además requiere owner con acceso Windows; F11 debe ser un agente distinto. | **Grok 4.5** como crítico independiente de diseño/diff; **Terra** puede preparar evidencia o tests, no cerrar el gate. |
| **L4 — alta** | **F2, F4, F5, F7, F8, F10** | Contratos MT5, I/O físico, cancelación, reintentos, secretos, logs por delta y despliegue Windows. El alcance es acotado, pero los fallos son costosos o difíciles de observar. | **GPT Terra** como implementor; revisión de **GPT Sol** antes del gate. Para F10, Terra/Sol sólo con operador humano y acceso a la VM. | **GLM 5.2** puede proponer tests/implementación en paralelo; **Grok 4.5** sirve para revisar seguridad y casos borde. |
| **L3 — media-alta** | **F3** | Funciones puras, listado y afinidad, con tests table-driven. Tiene riesgos de path traversal e identidad, pero el contrato y los archivos están bien delimitados. | **GPT Terra** directamente. | **GLM 5.2** puede implementar un primer borrador o ampliar la matriz de tests; Terra conserva el commit y gate. |

### Uso explícitamente descartado como responsable de fase

- **Luna** y **Minimax M3**: sólo apoyo mecánico —matriz de casos, borrador de documentación, inventario de diffs, scan de secretos o resumen de evidencia—, nunca responsables de una fase ni de un gate.
- **GLM 5.2**: no usar solo en F0/F1/F5/F6/F7/F8/F9/F10/F11; su aporte debe ser acotado y revisado por Terra o Sol.
- Ninguna fase es suficientemente trivial para asignarla a un modelo liviano sin revisión: todas tocan un pipeline productivo, sus artefactos o su evidencia.

### Orden práctico de despacho

1. **F0–F1:** GPT Sol, con Grok 4.5 como revisión adversarial puntual.
2. **F2–F5:** GPT Terra; GLM 5.2 puede preparar tests/diff y Sol revisa los gates L4.
3. **F6:** GPT Sol; es el punto de mayor riesgo de regresión del workflow existente.
4. **F7–F8:** GPT Terra con revisión Sol antes de sus gates.
5. **F9:** GPT Sol; repite el riesgo sistémico de F6 para backtesting.
6. **F10:** GPT Terra operando con el owner; escalar a Sol ante cualquier discrepancia con F0.
7. **F11:** GPT Sol independiente del implementor, con Grok 4.5 como segunda lectura del diff si el costo lo justifica.

## ✅ Tareas

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
const ord={" ":0,"/":1,"r":2,"x":3,"X":3,"-":4};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
const tasks=dv.current().file.tasks.array().sort((a,b)=>(ord[a.status]??9)-(ord[b.status]??9));
const el=dv.el('div','');
el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");
```

> [!example]- Fuente de tareas — editar / mover de estado aquí
> - [x] **F0 — Contrato físico Windows + SPECIFY** #owner/agent #type/docs #area/echo
> - [x] **F1 — PLAN/TASKS SDD + baseline reproducible** #owner/agent #type/docs #area/echo
> - [x] **F2 — Contratos, configuración y validación real** #owner/agent #type/dev #area/echo
> - [x] **F3 — Derivación de keys, listado y afinidad** #owner/agent #type/dev #area/echo
> - [x] **F4 — Compiler físico orientado a artefactos** #owner/agent #type/dev #area/echo
> - [x] **F5 — Activity y child workflow de compiler** #owner/agent #type/dev #area/echo
> - [x] **F6 — Integración `mt5_compiler` en ambos intérpretes** #owner/agent #type/dev #area/echo
> - [x] **F7 — Runner físico crudo e INI correcto** #owner/agent #type/dev #area/echo
> - [x] **F8 — Evidencia, upload y activity de backtesting** #owner/agent #type/dev #area/echo
> - [x] **F9 — Child + integración `mt5_backtesting`** #owner/agent #type/dev #area/echo
> - [x] **F10 — Despliegue Windows y smoke E2E real** — observado 2026-08-14: 12 EX5 + 12 HTM, Temporal Completed, worker `kor` #owner/agent #type/dev #area/echo
> - [x] **F11 — Verificación independiente y handoff** — re-ejecutada PASS 2026-08-14; waiver F10 sustituido por evidencia #owner/agent #type/test #area/echo
> - [x] **Rework F11 — journals activos/rescan, sanitización IP/path, cobertura nueva ≥85% y `gofmt`** — `03879d1`; gates focales PASS #owner/agent #type/dev #area/echo
> - [x] **Repetir F11 — VERIFY independiente y decisión final de merge** — PASS; owner pidió cierre en sesión 2026-08-14 #owner/agent #type/test #area/echo

## 📋 Tablero

#### 🟦 To Do
```tasks
sort by priority
path includes Echo Forge - Etapa 6
status.name includes Todo
short mode
hide task count
```

#### 🟡 WIP
```tasks
sort by priority
path includes Echo Forge - Etapa 6
status.name includes WIP
short mode
hide task count
```

#### 🔵 Review
```tasks
sort by priority
path includes Echo Forge - Etapa 6
status.name includes Review
short mode
hide task count
```

#### ✅ Done
```tasks
sort by priority
path includes Echo Forge - Etapa 6
done
short mode
hide task count
```

## 🧭 Decisiones

Tomadas en la entrevista del 2026-08-06 con el owner:

- **D1 — Puerta única**: el task type vive en `generic_workflow.go` (el flujo que consume `config.json`). `adaptive_workflow.go` queda como legado y no se extiende.
- **D2 — Subtarea = child workflow**: una ejecución de Temporal propia por estrategia, visible en la UI, con retry y cancelación independientes e historial acotado.
- **D3 — Dos tareas atómicas separadas**: `mt5_compiler` produce el `.ex5`; `mt5_backtesting` lo consume. Ninguna hace más de una cosa.
- **D4 — Sin gate y sin procesamiento**: las tareas no descartan estrategias, no calculan desviación y no escriben métricas en Mongo. Solo dejan artefactos crudos en MinIO. El procesamiento es trabajo de tareas posteriores.
- **D5 — Parámetros en el `config.json`**: símbolo, período, rango de fechas y condiciones del tester se declaran explícitamente en el task. Lo propio de la estrategia (su nombre) viene de la ejecución.
- **D6 — Credenciales fuera del sistema**: la terminal MT5 ya está logueada en la instancia; el `tester.ini` no lleva `[Common]`.
- **D7 — Reporte `.htm`**: un único formato, forzado con `Report=` + `ReplaceReport=1`.
- **D8 — Serial**: una ejecución de MT5 a la vez por instalación; el tiempo total no es una restricción para v1.
- **D9 — Fallo parcial tolerado**: las estrategias que fallan se reportan y no abortan el flujo.
- **D10 — Sin idempotencia por skip**: se re-ejecuta siempre y se sobrescriben los artefactos en MinIO.
- **D11 — Clases de worker y routing Temporal**: la afinidad de las dos tareas nuevas vive en un registro puro; los child workflows permanecen en la queue principal y sólo las activities físicas usan `sqx-mt5-queue`. Se mantienen los nombres de queue actuales.
- **D12 — Alcance del proyecto**: incluye el despliegue del worker en Windows y el smoke E2E real.
- **D13 — Identidad opaca**: la full source key de MinIO es la autoridad. El stem se deriva sólo del basename/extensión; no se intenta deshacer el sanitizado Java ni reconstruir paths desde `StrategyID`.
- **D14 — BWC del flujo adaptativo**: las activities, payloads, adapters y parser legacy quedan intactos. Las capacidades para el pipeline dinámico son aditivas y usan nombres nuevos.
- **D15 — SDD separado**: la integración dinámica vive en `FEAT-SQX-MT5-PIPELINE-ARTIFACTS`; no se sobrescribe la verificación histórica de `FEAT-SQX-MT5-BACKTEST-COMPILE`.
- **D16 — Semántica de fallo**: errores funcionales por estrategia retornan un resultado `failed` con evidencia y no abortan el padre; errores de infraestructura retornan error para retry. El padre consume todos los futures.
- **D17 — Contrato MT5 oficial**: real ticks es `Model=4`; `Period` usa `H1`; leverage se escribe `1:N`; el INI no contiene `[Common]`.
- **D18 — Validación antes de Temporal**: el watcher rechaza cualquier task MT5 inválido, incluso dentro de groups. No se aceptan defaults silenciosos de símbolo, período o parámetros financieros.
- **D19 — Evidencia aislada**: los logs subidos contienen sólo el delta generado por la ejecución actual; nunca se publica el journal histórico de la terminal.

## ⚠️ Riesgos y supuestos

| ID | Riesgo / supuesto | Mitigación |
|---|---|---|
| R1 | El nombre del símbolo en el broker difiere del `instrument` de SQX y el backtest corre sin datos | F0 lo confirma antes de escribir código; `mt5.symbol` es explícito en el task |
| R2 | El `.mq5` exportado por SQX no compila sin includes adicionales en la instancia | El owner confirma que compila limpio; F0 lo verifica a mano y deja el comando documentado |
| R3 | La terminal no genera el `.htm` (rango sin datos, símbolo inválido) y el fallo se ve igual que un timeout | Errores tipados distintos: `ErrReportNotFound` vs `ErrBacktestTimeout`; se sube el log del terminal como evidencia |
| R4 | Terminales MT5 huérfanas de una ejecución previa bloquean la siguiente | Nunca matar por nombre de imagen; validar ruta del ejecutable y handle del proceso lanzado por el worker |
| R5 | El tocar `generic_workflow.go` regresiona task types existentes | Cases mínimos que llaman un helper compartido + suite completa de workflows en F6/F9 |
| R6 | MT5 genera automáticamente un `.set` después del test y podría confundirse con input externo | F0 confirmó defaults horneados sin `ExpertParameters`/`TesterInputs`; el `.set` posterior es side effect, no se usa, publica ni valida como input |
| R7 | La forma exacta del prefix producido por `mt5_exporter` puede no coincidir con `BuildMinIOPath(req.Spec...)` | F0 guarda full keys reales; F3 lista y propaga keys completas y deriva destino sustituyendo el segmento de stage |
| R8 | El naming no round-trippea porque el `.mq5` viene sanitizado por Java | El stem sanitizado se trata como identidad física opaca de esta cadena; no hay conversión reversible ficticia |
| R9 | Etapa 6 se aborda antes de cerrar Etapa 5, invirtiendo el orden del roadmap | Excepción consciente: las dos tareas de esta etapa consumen `.mq5` ya existentes en MinIO y no dependen de nada de Etapa 5. Se documenta en el programa padre para no perder el rastro |
| R10 | Child workflow enviado a MT5 queda sin poller de workflows | Tests de F5/F9 afirman child en queue principal y activity en MT5 |
| R11 | Cambiar puertos/activities legacy rompe `adaptive_workflow` | APIs aditivas, archivos legacy prohibidos y regresión explícita en cada gate |
| R12 | Los logs de MT5 incluyen actividad histórica o datos de cuenta | Snapshot por offset/tiempo, sanitización en F0 y scan de secretos en F8/F10 |
| R13 | Reintentos duplican una operación física larga | Workspace por attempt, outputs sobrescribibles, errores funcionales no retryables y política de retry congelada en F1 |
| R14 | Un agente implementa contra una SPEC histórica que mezcla lineage/Mongo | Feature SDD separada y F0/F1 bloqueantes antes del código |
| R15 | `Report=` absoluto o nested Expert no funciona en la instalación real | F0 prueba ambos en la VM y congela el patrón exacto; ningún implementor elige por intuición |

## 📆 Bitácora

- **2026-08-14** — Cierre Etapa 6. F10 observado (release `0.2.42`, strategy `example_flow_3`, 12/12 EX5 y HTM, worker `kor`). F11 PASS (`VERIFICATION.md`); `SPECS.md` → Completed. Owner pidió cerrar la etapa en esta sesión; puente del padre a Done por esa instrucción. Residual UTF-16 documentado como known error. Sin commit (T11.14) salvo pedido explícito.
- **2026-08-10** — Corrección `TelemetryCarrier` aplicada en ambos contratos: `MT5ArtifactListRequest` y `ArtifactTaskRequest` llevan `Telemetry` + `GetTelemetry`; builders de Generic/Group propagan el contexto a `list_mt5_artifacts` y a los child workflows de compile/backtest. Tests nuevos: assertions de interfaz (runtime + SDK) y ejecución con el interceptor productivo de Temporal; integración MT5 afirma telemetría en el list request. Gates PASS: suites dirigidas domain/activities/workflows, `go vet`, build `sqx-worker` y cross-build Windows amd64 de `sqx-mt5-worker`. Sin commit ni despliegue en esta sesión. Próximo: redeploy de ambos workers y smoke runtime / retomar F11 independiente.
- **2026-08-10** — Diagnóstico runtime de `list_mt5_artifacts`: el request `domain.MT5ArtifactListRequest` no implementa el contrato estricto `TelemetryCarrier` impuesto por el interceptor Temporal del SDK; el fallo ocurre en el worker principal antes de entrar a la activity o crear children, por lo que el worker Windows no recibe trabajo. Hallazgo adicional para el fix: `domain.ArtifactTaskRequest`, usado por las activities físicas `mt5_compile_artifact` y `mt5_backtest_artifact`, tampoco implementa el mismo contrato; corregir sólo el listado desplazaría el fallo al worker MT5. Los tests existentes invocan `Execute` o mocks de workflow sin el interceptor productivo, y no detectan este borde. Próximo implementor: propagar `telemetry.Context` por ambos payloads y sus builders/callers, implementar `GetTelemetry`, agregar assertions de interfaz y un test con el interceptor real; luego validar ambos workers antes del smoke Windows. Sin cambios de código ni despliegue en esta sesión.
- **2026-08-08** — F11 ejecutada por verifier independiente con waiver explícito del owner para asumir exitoso F10, sin fabricar evidencia. Veredicto `FAIL / NOT APPROVED`: `BLOQ-01` snapshot de journals elige el primer path lexicográfico y no redescubre logs creados/modificados durante el attempt; `BLOQ-02` sanitización no cubre IPs ni paths privados; `BLOQ-03` cobertura ponderada de código nuevo `74.86%` (`667/891`) bajo el 85%; además `gofmt -d` deja diff. Gates positivos: Allowed/Prohibited Files, anti-test-masking, suite dirigida `-race`, regresión `core/adaptive`, vet dirigido y builds Linux/Windows. Suite global limitada por `sqx/tools` (múltiples `main`) y tests ETCD de `sqx/examples`; `staticcheck`/`pwsh` no disponibles. `VERIFICATION.md` quedó versionado en `88867f5`; F11 queda ejecutada pero el proyecto reabre rework y mantiene el puente en WIP.
- **2026-08-08** — Rework crítico F11 completo en `03879d1`: snapshot rescanea todos los journals y captura archivos nuevos, modificados o truncados por tipo con orden determinista; Agent se clasifica antes que Tester; sanitización cubre credenciales, redes privadas IPv4/IPv6 y paths Windows/UNC. Se agregaron pruebas de runner, compiler, activities, storage y workspace. Gates PASS: cobertura nueva `85.38%` (`765/896`), suite focal, `-race`, `go vet`, `gofmt`, anti-test-masking, `git diff --check` y builds Linux/Windows amd64 del worker MT5. Cambios ajenos y paquete F10 quedaron fuera del commit. Siguiente acción: verifier independiente repite F11; el waiver F10 no equivale a evidencia runtime.
- **2026-08-08** — F10 avanzó hasta la frontera física: creados scripts Windows con `-WhatIf`, runbook, JSON sin secretos y plantilla `F10-SMOKE.md`; `go test ./...`, cross-build Windows amd64, JSON y `git diff --check` PASS. Falta ejecutar el paquete en la VM con el owner (incluido parser PowerShell, deploy, poll, 2 válidas + 1 fallo, rerun y rollback). No se declarará PASS sin evidencia real de MT5, Temporal y MinIO.
- **2026-08-07** — F9 cerrado `PASS`: child `MT5BacktestArtifactWorkflow` registrado sólo en el worker principal; timeout Start-to-Close = `mt5.timeout + 2m`; activity física en `sqx-mt5-queue`; integración Generic/Group mediante agregador compartido con compiler; fan-out ordenado, fallo parcial tolerado y salida sólo con `.htm` exitosos preservando `Origin`. Gates PASS: suite completa `./workflows ./activities/worker ./adapters/mt5`, selección `-race`, regresión legacy, `go vet`, builds de ambos workers, cross-build Windows amd64 y `git diff --check`. Commit `d724059`; cambios ajenos preservados. Siguiente fase F10.
- **2026-08-08** — F9 iniciado sobre `feature/feat-sqx-mt5-pipeline-artifacts` en `b4cc7b4`: child workflow de backtesting, integración Generic/Group, registro en worker principal y E2E lógico. Se preservan como cambios ajenos `deployer_screen.log` y `specs/FEAT-SQX-STRATEGY-EVALUATION/fixtures/phase4_performance.json`.
- **2026-08-08** — F8 cerrado `PASS`: `mt5_backtest_artifact` publica `.htm`, `tester.ini` y deltas sanitizados `terminal/tester/agent` antes del cleanup; errores de upload siguen retryables. Worker MT5 compone el runner portable y registra sólo la activity nueva, preservando contracts legacy. Gates PASS: tests focalizados/regresión de adapters y activities, `-race`, cross-build Windows y `git diff --check`. Commit `b4cc7b4`; siguiente fase F9.
- **2026-08-08** — F7 cerrado `PASS`: runner físico portable sin `[Common]`, `Period=H1`, `Model=4`, `Leverage=1:N`, reporte relativo `.htm`, preflight recursivo de indicadores SQ y snapshots por offset con sanitización. No invoca parser ni persiste Mongo. Gates PASS: tests focalizados/regresión de adapters, `-race` y `git diff --check`. Commit `6fc3999`; siguiente fase F8.
- **2026-08-07** — F6 cerrado `PASS`: Generic y Group llaman el mismo agregador `mt5_compiler`; listing `.mq5` por `source_folder`, full keys ordenadas, child ID `request_id + hash(full key)`, recolección completa, fallos parciales tolerados, salida sólo con basenames `.ex5` exitosos y `Origin` preservado. Tests nuevos cubren cero/una/múltiples keys, orden, fallo funcional, infra agotada, queues, rerun y task desconocido. Gates PASS: suite focalizada y completa de workflows, race focalizado, `go vet ./workflows`, build de `sqx-worker` y `git diff --check`. Commit `e3aee85`; `deployer_screen.log` ajeno preservado. Siguiente fase F7.
- **2026-08-07** — F6 iniciado: integración `mt5_compiler` en Generic/Group según PLAN/TASKS aprobados. La tarea puente del padre vuelve de Review a WIP porque el proyecto completo aún mantiene F6–F11 abiertos. Se preserva `deployer_screen.log` como cambio ajeno.
- **2026-08-07** — F5 cerrado `PASS`: `mt5_compile_artifact` + `MT5CompileArtifactWorkflow` + helpers de ID/queues/retry; wiring en ambos workers; tests afirman activity en `sqx-mt5-queue` y child en queue padre. Gates PASS (`go test` focalizado, builds Linux + Windows amd64, vet, `git diff --check`). Commit `64fc351`. `deployer_screen.log` ajeno preservado. Siguiente fase F6.
- **2026-08-07** — F3 cerrado `PASS`: `DeriveArtifactKey`/`ArtifactStem` con key F0 opaca, `worker_affinity` → `sqx-mt5-queue`, port `ArtifactStorage` aditivo, `list_mt5_artifacts` con full keys ordenadas/dedupe y wiring en `sqx-worker`. Gates PASS (`go test` focalizado, build worker, vet, `git diff --check`). Commit `917965c`; siguiente fase F4.
- **2026-08-07** — F2 cerrado `PASS`: se agregaron contratos de artefactos MT5, `TaskSpec.MT5`, validación centralizada y validación recursiva desde watcher; tests nuevos cubren round-trip JSON, omitempty, límites MT5, stages, tareas anidadas y rechazo antes de Temporal. Gates: `go test ./core/domain ./core/runtime ./activities/watcher`, `go vet ./core/domain ./core/runtime ./activities/watcher` y `git diff --check`, todos PASS. Commit `3f5d9a7`; siguiente fase F3.
- **2026-08-07** — F1 cerrado `PASS`: el owner aprobó TASKS, que quedó versionado en `e6a1fa1`; PLAN ya estaba aprobado en `aa4bcc1`. Los 115 checkpoints F1–F11 cubren todos los Allowed/New Files del PLAN y mantienen intocables contratos/tests legacy. Worktree final de la feature limpio salvo `deployer_screen.log`, cambio ajeno preservado. No se inició F2. Sesión AGENTS OS cerrada con continuidad en este proyecto.
- **2026-08-07** — PLAN F1 aprobado explícitamente por el owner y versionado en `aa4bcc1`. Se redactó `TASKS.md` con 115 tareas/checkpoints F1–F11, dependencias secuenciales, tests first, commits atómicos, stop conditions y operaciones F10 reservadas al owner Windows. Segundo gate humano abierto: aprobar TASKS. No se modificó código productivo ni se inició F2.
- **2026-08-07** — Draft F1 `PLAN.md` listo para aprobación del owner. Congela bloque `mt5` sin defaults silenciosos, payloads Temporal aditivos, full keys opacas, workflow IDs con `request_id` + hash, child en queue principal, activities físicas en `sqx-mt5-queue`, retry sólo de infraestructura, roots portable, compiler timeout, preflight SQ, reporte relativo, tres deltas de journal, Allowed/New/Prohibited Files y rollout/rollback PowerShell. Baseline focalizada PASS. `TASKS.md` e implementación continúan bloqueados por el gate humano.
- **2026-08-07** — F0 cerrado `PASS` por el owner. Instancia MT5 portable (`data_root == installation_root`), MetaEditor/terminal con `/portable`, indicador SQ faltante detectado (`SqLinReg.ex5`) y preflight final `MQ5 sin EX5: 0`. Compile PASS con exit code `1`, EX5 no vacío y log `Result: 0 errors`; backtest XAUUSD/H1 Model=4 PASS con 13,090,434 ticks y 503 bars. `Report=` relativo PASS; absoluto no produce output. Sin `[Common]`, `.set` de entrada ni overrides; el `.set` posterior es side effect. Evidencia sanitizada, SPEC `Spec-Active`, catálogo actualizado y commit `47e7275`. F1 iniciado exclusivamente en fase PLAN; pausa obligatoria antes de TASKS.
- **2026-08-06** — F0 preparado hasta la frontera física. Se creó `feature/feat-sqx-mt5-pipeline-artifacts` desde `master` `c616cc8`, preservando el cambio ajeno `deployer_screen.log`. El cliente oficial ETCD/DI/MinIO listó 263 `.mq5`; se seleccionó una key XAUUSD/H1 real y se registraron tamaño, SHA-256 y derivaciones de stage sin usar `CanonicalStrategyID`. Se creó `SPEC.md` (`CAPABILITY_SPEC`, draft), `evidence/WINDOWS-CONTRACT.md`, `fixtures/minio-keys.json`, `fixtures/tester.ini.example` y la política de fixture no versionado. `verify-spec.sh` = `READY`, JSON válido, `git diff --check` limpio y secret scan limpio. El `.mq5` temporal fue eliminado tras el scan. Próximo bloqueo intencional: owner ejecuta el paquete PowerShell, sanitiza evidencia y aprueba SPEC; recién entonces inicia F1/PLAN.
- **2026-08-06** — El owner resolvió la NEED-INFO: la rama canónica parte desde `master`; la VM Windows ya existe, pero sólo el owner accede y ejecutará el worker manualmente desde PowerShell por ahora. F0 se reanuda como operación asistida: el agente construye SPEC/contrato/paquete de captura y el owner devuelve evidencia física sanitizada. MinIO se deriva de la implementación existente del proyecto.
- **2026-08-06** — NEED-INFO de F0 confirmado con evidencia local: `~/.ssh/config` sólo declara `github.com` y `develop`, sin host Windows; no hay cliente MinIO configurado disponible; y el repo `symphony` está en `master` commit `c616cc8`, con `origin/master` como default y sin rama `develop` local/remota. Se detiene antes de inventar rutas, keys o branch base. Se requiere del owner el método de acceso a Windows/MT5 + MinIO y la rama base correcta.
- **2026-08-06** — F0 iniciado. Se cargó el contrato operativo del proyecto, se confirmó la tarea puente del padre en WIP y se comenzó el inventario del repo y del acceso físico requerido. No se presume evidencia de Windows/MinIO: si la configuración existente no permite operar la VM, F0 quedará bloqueado con la NEED-INFO explícita antes de redactar contratos definitivos.
- **2026-08-06** — Proyecto creado. Entrevista de requerimientos completada en tres rondas con el owner usando `agents-os-requirement-interview`. Alcance reducido deliberadamente respecto de la guía externa `GUIA_WORKER_TEMPORAL_MT5` (que proponía parseo, Mongo, deviation y lock distribuido en la misma tarea): el owner definió dos tareas atómicas que solo producen artefactos en MinIO. Inventariada la base preexistente (worker Windows y adapters MT5 ya implementados y testeados) y registrados siete hallazgos de desalineamiento (H1–H7), uno de los cuales cierra el GAP `EF-G27` del backlog del programa. Etapa 6 se separó del proyecto de agente que la contenía, que quedó como [[Echo Forge - Etapas 5 y 7]].
- **2026-08-06** — Verificación cruzada del plan contra el repo con tres exploraciones paralelas (inventario MT5, mecánica del `generic_workflow`, estado SDD y roadmap). El diseño se sostuvo; se incorporaron tres hechos nuevos: (a) hallazgo H8, el plugin Java nombra el `.mq5` con un sanitizado propio y no con `CanonicalStrategyID`, lo que amenaza el requisito de nombrar los artefactos como la estrategia; (b) `FEAT-SQX-MT5-BACKTEST-COMPILE` ya tiene un `CHANGE-001` en estado `Approved` y sin implementar que pide justamente subir los reportes crudos a MinIO y purgar credenciales del `.ini`, así que F6 lo extiende en vez de redactar un delta nuevo; (c) se explicita que esta etapa se adelanta a Etapa 5 (R9) y que no existe procedimiento de despliegue para el worker Windows. H1 se reforzó: las activities MT5 hoy asumen keys `{strategyID}.mq5`, ajenas al layout de `BuildMinIOPath` que produce el pipeline real.
- **2026-08-06** — Auditoría crítica y replanificación para ejecución por agentes menos capaces. Se corrigieron ocho supuestos del plan anterior: SDD pasa al inicio; se crea una feature separada para no pisar la verificación histórica; `Spec-Active (+CHANGE-001 Approved)` es un estado correcto; los contratos legacy no se reescriben; los child workflows heredan la queue principal y sólo las activities corren en MT5; `Model=4` y `Leverage=1:N` se fijan desde documentación oficial; la full MinIO key se vuelve autoridad opaca; y los logs se capturan por delta. El plan quedó dividido en doce fases secuenciales homogéneas con Allowed/Prohibited Files, tests, gates y stop conditions. Línea base focalizada PASS; también pasaron el cross-build Windows de `sqx-mt5-worker` y el build local de `sqx-worker`. La suite amplia de activities no pudo escribir `artifacts/f5_replay_signature.txt` por el sandbox de lectura del repo, limitación de esta auditoría y no fallo atribuido al código.
- **2026-08-06** — Se registró la asignación de capacidad para el pool actual de modelos: GPT Sol es responsable de F0/F1/F6/F9/F11; GPT Terra implementa F2–F5/F7/F8/F10 con revisión Sol en gates L4; F3 puede delegarse a Terra con apoyo de GLM 5.2. Luna y Minimax M3 quedan restringidos a apoyo mecánico, sin ownership de fase ni gate.

## 🔗 Docs / Links

- [[Echo Forge]] (programa padre)
- [[Echo Forge - Etapas 5 y 7]] (etapas hermanas)
- [[echo-forge]] (Aplicación)
- Guía externa de referencia (no normativa): [[GUIA_WORKER_TEMPORAL_MT5]]
- `specs/FEAT-SQX-MT5-BACKTEST-COMPILE/` — SPEC, PLAN, TASKS, VERIFICATION en el repo `symphony`
- `specs/FEAT-SQX-MT5-PIPELINE-ARTIFACTS/` — SPEC, evidencia F0, PLAN, TASKS, F0–F10 y `VERIFICATION.md`; rework `03879d1` listo para repetir F11
- `specs/FEAT-SQX-DEVIATION-FILTER/` — consumidor futuro de los artefactos de esta etapa
- `specs/FEAT-SQX-FINALIST-ARTIFACTS-LINEAGE/` — lineage de artefactos finalistas
- [MetaTrader 5 — Platform Start / Tester configuration](https://www.metatrader5.com/en/terminal/help/start_advanced/start) — fuente primaria para `Model`, `Period`, `Leverage`, `Report` y flags del tester

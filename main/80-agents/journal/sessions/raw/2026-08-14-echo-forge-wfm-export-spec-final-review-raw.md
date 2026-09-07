---
type: raw_session
schema_version: 1
scope: session
created: "2026-08-14"
updated: "2026-08-14"
area: "[[Echo]]"
project: "[[Echo Forge - Optimización de Latencia WFM Exporter]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge]]"
  - "[[Symphony]]"
related:
  - "[[2026-08-14-echo-forge-one-vm-one-worker-one-task]]"
aliases: []
confidence: verified
source_session:
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-raw.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# Echo Forge WFM Export — Final SPEC review raw

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: [[Codex]]
- Proyecto o entidad: [[Echo Forge - Optimización de Latencia WFM Exporter]]
- Objetivo de la sesión: revisión crítica final contra Symphony `master`, persistencia de continuidad y cierre completo.

## Transcript

~~~~text
Quiero que hagas una última revisión crítica del SPEC `FEAT-SQX-WFM-EXPORT-EXECUTION` contra el estado ACTUAL de `master` de Symphony, corrijas únicamente lo que la evidencia del repositorio demuestre necesario y después cierres esta sesión.

No implementes código productivo en esta sesión.

1. Revalidar contra master actual

El repositorio `xKoRx/symphony` acaba de ser actualizado con lo último desarrollado en `master`.

Antes de tocar el SPEC:

- actualiza/revalida la referencia de `master`;
- registra commit/HEAD observado;
- revisa `git status`;
- preserva cualquier cambio ajeno;
- usa código, tests y contratos actuales como fuente de verdad;
- no reutilices conclusiones de una revisión anterior si `master` actual las contradice.

2. Punto crítico: una estrategia por activity DEBE permitir paralelismo real entre workers

Mi intención no es solamente obtener:

```text
N estrategias → N activities
```

sino que las N activities WFM queden despachadas a Temporal sin esperar una por una, de forma que distintos workers/VMs puedan tomarlas simultáneamente.

La arquitectura sigue siendo:

```text
1 VM = 1 worker = 1 activity SQX en ejecución
```

Por tanto, el paralelismo ocurre entre workers, no dentro de un worker.

Antes de modificar el SPEC, valida el patrón existente en Symphony

Busca cómo el código actual implementa otros trabajos por estrategia, especialmente alrededor de:

- `evaluate_wfm`;
- `evaluate_strategy`;
- `verify_wfm_evaluated`;
- `select_robust_run`;
- otros loops equivalentes de activities/futures;
- caminos equivalentes dentro de `GroupSQXWorkflow`.

Mi expectativa, que debes verificar contra código y no asumir, es encontrar un patrón equivalente a:

```go
for each item:
    future := workflow.ExecuteActivity(...)
    futures = append(futures, future)

// recién después
for each future:
    future.Get(...)
```

y NO:

```go
for each item:
    workflow.ExecuteActivity(...).Get(...)
```

Si ese patrón está efectivamente establecido en Symphony, la implementación WFM debe reutilizar exactamente esa arquitectura existente, no crear una abstracción o mecanismo nuevo.

El SPEC debe dejar inequívoco el resultado requerido:

```text
N estrategias
    ↓
despachar N project/wfm_exporter activities
sin esperar individualmente durante el despacho
    ↓
Temporal las distribuye por la task queue normal
    ↓
cada worker sigue serial por contrato
    ↓
esperar/recoger los resultados según el patrón vigente
    ↓
continuar con la evaluación WFM existente
```

No hardcodear N=12.

3. Revisar cuidadosamente la redacción sobre fan-in

El SPEC actualmente declara fuera de alcance cambios de `fan-in`.

No interpretes eso automáticamente como un error ni lo cambies por criterio genérico.

Primero determina qué significa realmente el patrón vigente en Symphony.

La intención del owner es:

- NO rediseñar la semántica de fan-in;
- NO inventar políticas nuevas de agregación;
- NO cambiar retries/fallos parciales/resultados parciales;
- PERO sí realizar el mecanismo mínimo y normal del proyecto necesario para despachar las N activities y luego esperar/recoger sus resultados antes de continuar.

Si la redacción actual de `fan-in OUT` puede llevar a un implementador a ejecutar:

```go
ExecuteActivity(...).Get(...)
ExecuteActivity(...).Get(...)
ExecuteActivity(...).Get(...)
```

secuencialmente, corrígela para eliminar esa ambigüedad.

La corrección debe expresar algo equivalente a:

```text
OUT:
- rediseño o cambio semántico del fan-in existente.

IN:
- reutilizar el patrón vigente de futures/join necesario para
  despachar todas las exportaciones por estrategia antes de esperarlas.
```

Solo haz este cambio si la inspección de master confirma que refleja la arquitectura real existente.

4. Double-check de otros posibles puntos ambiguos

Revisa los siguientes puntos, pero NO hagas cambios preventivos. Solo corrige si HEAD/tests/contratos actuales demuestran una inconsistencia.

A. Terminología `evaluate_wfm`

Comprueba si existe ambigüedad entre workflow task `evaluate_wfm` y Temporal activity `evaluate_wfm`. Si puede inducir al implementador a modificar el componente equivocado, aclara la terminología del SPEC sin cambiar comportamiento.

B. Orden, multiplicidad y correlación

Confirma cómo el código actual correlaciona input strategies, futures y results cuando las activities pueden completar físicamente en distinto orden.

No inventes una nueva estrategia de correlación. Si el código existente ya usa índices/futures u otro mecanismo determinista, el SPEC debe exigir preservar ese patrón. Considera agregar un GWT de completion order invertido solamente si sirve para verificar una semántica ya existente y no introduce una nueva.

C. Invariante del worker

Confirma en código/configuración/documentación vigente que `MaxConcurrentActivityExecutionSize = 1` sigue siendo efectivo.

La decisión canónica `[[2026-08-14-echo-forge-one-vm-one-worker-one-task]]` sigue siendo vinculante. No agregar locks, mutexes, scopes, workspaces ni ninguna exclusión local.

D. Heartbeat

Revisa que el contrato del heartbeat especifique comportamiento observable y no una implementación innecesariamente específica.

Debe mantenerse wave, strategy, phase, attempt, elapsed y progress, y el ticker no debe volver a pisar el último contexto real con un mensaje estático.

No agregar OTel, dashboards ni modificaciones de timeout/retry.

5. Restricciones absolutas

Continúan OUT:

- cambios de timeouts;
- cambios de retry policy;
- locks/mutexes/semaphores/host slots;
- scopes/hash wave+strategy;
- workspaces/directorios por request;
- layouts MinIO nuevos;
- cambio de identidad de strategy;
- sort/dedupe;
- optimización interna Java;
- cambios al 6×9;
- cambios al evaluator;
- cambios de schema/matemática/selección WFM;
- nuevas políticas de partial failure;
- arquitectura nueva cuando ya existe un patrón equivalente en Symphony.

Especialmente: preferir copiar/reutilizar el patrón ya utilizado por Symphony antes que crear una solución nueva.

6. Revisar SPEC + CHANGE + RCA como conjunto

Después de validar master:

1. revisa `SPEC.md`;
2. revisa `CHANGE-001-single-strategy-execution-heartbeat.md`;
3. revisa `RCA-001-double-execution.md`;
4. verifica que no se contradigan;
5. corrige solamente lo necesario;
6. ejecuta los validadores SDD correspondientes.

Si descubres una diferencia material que cambia una decisión ya aprobada por el owner, no la resuelvas por cuenta propia: documenta la evidencia y deja el gate nuevamente en Review.

Si solo estás aclarando contractualmente cómo reutilizar un comportamiento ya existente y aprobado, registra la aclaración sin inventar una nueva decisión.

7. Resultado esperado de esta revisión

Al terminar, debe ser imposible interpretar el SPEC como:

```text
S1 → ejecutar → esperar
S2 → ejecutar → esperar
S3 → ejecutar → esperar
```

si la arquitectura vigente de Symphony permite y utiliza:

```text
dispatch S1
dispatch S2
dispatch S3

wait S1
wait S2
wait S3
```

La feature debe explotar la distribución horizontal normal de Temporal:

```text
VM A → strategy 1
VM B → strategy 2
VM C → strategy 3
...
```

sin asignar hosts manualmente y manteniendo un solo proceso SQX activo por worker.

8. Cerrar sesión

Una vez terminada la revisión:

- actualiza `[[Echo Forge - Optimización de Latencia WFM Exporter]]`;
- actualiza SPEC/CHANGE/RCA si hubo correcciones;
- registra master/HEAD usado como evidencia;
- actualiza progreso, gates y bitácora;
- actualiza el journal/handoff de sesión;
- preserva la decisión canónica `1 VM = 1 worker = 1 task`;
- deja claramente registrada cualquier aclaración contractual realizada;
- deja preparado el despacho de la próxima fase;
- ejecuta los mecanismos normales de cierre/memoria/indexación de AGENTS OS;
- no inicies PLAN ni implementación durante esta sesión.

Termina entregándome solamente un resumen corto:

MASTER VALIDADO:
PATRÓN DE PARALELISMO ENCONTRADO:
CAMBIOS AL SPEC:
CAMBIOS A CHANGE/RCA:
G0:
ARCHIVOS ACTUALIZADOS:
RIESGOS/PUNTOS ABIERTOS:
PRÓXIMA FASE:
PRÓXIMO DESPACHO:
CIERRE DE SESIÓN:

No introduzcas arquitectura nueva ni scope adicional.
~~~~

## Evidencia externa

- Solicitud adjunta por el owner en esta sesión; se conserva completa arriba. No se incluyen logs pesados ni razonamiento interno.

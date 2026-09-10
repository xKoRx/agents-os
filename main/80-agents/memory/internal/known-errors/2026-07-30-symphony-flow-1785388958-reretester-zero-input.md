---
type: known_error
index_priority: never
indexable: false
load_policy: manual
memory_state: archived
scope: session
tags:
  - kind/doc
  - kind/known-error
  - tech/symphony
  - tech/sqx
  - severity/high
  - status/diagnosed
created: 2026-07-30
updated: 2026-09-09
aliases:
  - 1785388958
  - flow_46 reretester zero
  - sqx-main-1785388958
---

# Known Error — Symphony Flow `1785388958` termina tras `05_reretester` por **input vacío**

## TL;DR

- Workflow Temporal `sqx-main-00_configs-v1-NDX-H1-L-1785388958` **terminó exitosamente** (`WorkflowExecutionCompleted`), **no se quedó pegado**.
- La **causa raíz** es un bug de contrato: la actividad `05_reretester` (tipo `project`, `source_folder: "04_optimizer_robust"`) recibe un `InputBatch.Keys` con **12 nombres `WF_Matrix_-_NDX_..._Strategy_X.X.XX.z0.sqx`** (outputs del `03_optimizer`), pero el `source_folder` apunta a `04_optimizer_robust/` que contiene archivos con **nombre distinto** (`NDX_..._Strategy_X.X.XX.z0_robust.sqx`).
- El filtro del step (`prepareProjectInput`) hace **match exacto por nombre base** después de trimSuffix `.sqx`. Como los sufijos no coinciden, **`filtered_count: 0`**, **`effective_count: 0`**, **`started_count: 0`** ⇒ la actividad "tiene éxito" con 0 keys y el flujo termina.
- 12 `apply_selected_run` **sí corrieron** (una por cada `selected_robust_run`) — el watcher **no tuvo nada que ver** con el fallo.

## Síntomas

- Workflow Temporal en estado `Completed` con muy pocos eventos después del `05_reretester` (no hay `trade_list_exporter`, `generate_report`, `mt5_exporter`).
- `apply_selected_run` parece exitoso (12 ejecuciones), pero no se traduce en inputs al `05_reretester`.
- En `/var/log/symphony/symphony-worker.log` del worker que ejecutó `05_reretester` (Hera) aparece:
  ```json
  {"message":"Project input preparado", "metadata":{"available_count":12, "filtered_count":0, "effective_count":0, "input_count":0, "prefix":"…/04_optimizer_robust/", "task_folder":"05_reretester"}}
  ```

## Causa raíz confirmada

En `sqx/activities/worker/steps/steps.go` (~líneas 195-218):

```go
availableSet := make(map[string]string, len(availableKeys))
for _, k := range availableKeys {
    parts := strings.Split(k, "/")
    baseName := parts[len(parts)-1]
    cleanName := strings.TrimSuffix(baseName, ".sqx")  // ← 'NDX_..._Strategy_X.X.XX.z0_robust'
    availableSet[cleanName] = baseName
}
filtered := make([]string, 0, len(st.InputBatch.Keys))
for _, key := range st.InputBatch.Keys {
    fileName := key
    if strings.Contains(key, "/") {
        parts := strings.Split(key, "/")
        fileName = parts[len(parts)-1]
    }
    cleanInputName := strings.TrimSuffix(fileName, ".sqx")  // ← 'WF_Matrix_-_NDX_..._Strategy_X.X.XX.z0'
    if realBaseName, ok := availableSet[cleanInputName]; ok {  // ← siempre false
        filtered = append(filtered, prefix+realBaseName)
    }
}
```

**Tabla de mapeo concreto**:

| `InputBatch.Keys` (lo que pasa el workflow) | Disponible en `04_optimizer_robust/` |
|---|---|
| `WF_Matrix_-_NDX_L_H1_example_flow_46_v1_Strategy_3.1.17.z0` | `NDX_L_H1_example_flow_46_v1_Strategy_3.1.17.z0_robust` |

El lookup es por **igualdad estricta** y los nombres no coinciden nunca.

## Evidencia recolectada

### 1. Conteo real de actividades (Temporal)

| Actividad | Cuenta |
|---|---|
| `project` | 4 (builder, retester, reretester, metadata) |
| `classify_and_rank` | 1 |
| `load_logical_types` | 1 |
| `list_strats` | 1 |
| `evaluate_wfm` | 14 |
| `select_robust_run` | 12 |
| `apply_selected_run` | 12 |
| `list_selected_strategies` | 1 |

> Las **12 `apply_selected_run` SÍ se ejecutaron** (1 por cada `selected_robust_run`), pero el resultado no se enlazó al `05_reretester`.

### 2. Input real del `05_reretester` (Temporal activity event)

`project` activity id=326, schedID=326 — `Started: 2026-07-30 06:58:51Z`, `Completed: 2026-07-30 06:59:12Z`, host `sqx-ulab-hera-0`.

Input (literal):
```json
{
  "input": {
    "keys": [
      "WF_Matrix_-_NDX_L_H1_example_flow_46_v1_Strategy_3.1.14.z0.sqx",
      "WF_Matrix_-_NDX_L_H1_example_flow_46_v1_Strategy_3.1.15.z0.sqx",
      "WF_Matrix_-_NDX_L_H1_example_flow_46_v1_Strategy_3.1.16.z0.sqx",
      "WF_Matrix_-_NDX_L_H1_example_flow_46_v1_Strategy_3.1.17.z0.sqx",
      "WF_Matrix_-_NDX_L_H1_example_flow_46_v1_Strategy_3.1.19.z0.sqx",
      "WF_Matrix_-_NDX_L_H1_example_flow_46_v1_Strategy_3.1.23.z0.sqx",
      "WF_Matrix_-_NDX_L_H1_example_flow_46_v1_Strategy_3.1.25.z0.sqx",
      "WF_Matrix_-_NDX_L_H1_example_flow_46_v1_Strategy_8.1.18.z0.sqx",
      "WF_Matrix_-_NDX_L_H1_example_flow_46_v1_Strategy_8.1.24.z0.sqx",
      "WF_Matrix_-_NDX_L_H1_example_flow_46_v1_Strategy_8.1.25.z0.sqx",
      "WF_Matrix_-_NDX_L_H1_example_flow_46_v1_Strategy_8.1.26.z0.sqx",
      "WF_Matrix_-_NDX_L_H1_example_flow_46_v1_Strategy_8.1.27.z0.sqx"
    ],
    "origin": "sqx-strategies"
  },
  "payload": {"task":{"folder":"05_reretester","source_folder":"04_optimizer_robust"}}
}
```

Output (resumen):
```json
{
  "status": "success",
  "result": {
    "keys": [],
    "started_count": 0,
    "output_count": 0,
    "hostname": "sqx-ulab-hera-0"
  }
}
```

### 3. Logs del watcher step (Hera)

```json
{
  "message": "Project input preparado",
  "trace_id": "0d155562a6286cfaf855889be62bc04e",
  "metadata": {
    "task_folder": "05_reretester",
    "source_folder": "04_optimizer_robust",
    "prefix": "wave_test/ndx/l_h1/example_flow_46/v1/0d155562a6286cfaf855889be62bc04e/04_optimizer_robust/",
    "available_count": 12,
    "filtered_count": 0,
    "effective_count": 0,
    "input_count": 0
  }
}
```

### 4. MinIO tiene las 12 robustas

```text
s3://sqx-strategies/wave_test/ndx/l_h1/example_flow_46/v1/0d155562a6286cfaf855889be62bc04e/04_optimizer_robust/
  NDX_L_H1_example_flow_46_v1_Strategy_3.1.14.z0_robust.sqx  (4004444 bytes)
  NDX_L_H1_example_flow_46_v1_Strategy_3.1.15.z0_robust.sqx  (3563454 bytes)
  NDX_L_H1_example_flow_46_v1_Strategy_3.1.16.z0_robust.sqx  (2080981 bytes)
  NDX_L_H1_example_flow_46_v1_Strategy_3.1.17.z0_robust.sqx  (4671391 bytes)
  NDX_L_H1_example_flow_46_v1_Strategy_3.1.19.z0_robust.sqx  (4629999 bytes)
  NDX_L_H1_example_flow_46_v1_Strategy_3.1.23.z0_robust.sqx  (4526879 bytes)
  NDX_L_H1_example_flow_46_v1_Strategy_3.1.25.z0_robust.sqx  (4014859 bytes)
  NDX_L_H1_example_flow_46_v1_Strategy_8.1.18.z0_robust.sqx  (1998506 bytes)
  NDX_L_H1_example_flow_46_v1_Strategy_8.1.24.z0_robust.sqx  (3832546 bytes)
  NDX_L_H1_example_flow_46_v1_Strategy_8.1.25.z0_robust.sqx  (5258920 bytes)
  NDX_L_H1_example_flow_46_v1_Strategy_8.1.26.z0_robust.sqx  (3475530 bytes)
  NDX_L_H1_example_flow_46_v1_Strategy_8.1.27.z0_robust.sqx  (5880348 bytes)
```

Las 12 estrategias robustas **sí se generaron** (convención `…_Strategy_X.X.XX.z0_robust.sqx`).

### 5. MinIO tiene las 12 estrategias optimizadas (output `03_optimizer`)

```text
s3://sqx-strategies/wave_test/ndx/l_h1/example_flow_46/v1/0d155562a6286cfaf855889be62bc04e/03_optimizer/
  WF_Matrix_-_NDX_L_H1_example_flow_46_v1_Strategy_3.1.14.z0.sqx
  WF_Matrix_-_NDX_L_H1_example_flow_46_v1_Strategy_3.1.15.z0.sqx
  … (12 archivos WF_Matrix)
```

Y exactamente esos **12 nombres son los que recibió el `05_reretester`** como `InputBatch.Keys`.

### 6. Distribución por worker

| Worker | Tareas del trace_id 0d15556 |
|---|---|
| Zeus (192.168.31.101) | `01_builder`, `03_optimizer` |
| Hera (192.168.31.111) | `02_retester`, `03_optimizer`, **`05_reretester`**, `metadata` |
| Kronos (192.168.31.121) | `02_retester`, `03_optimizer`, `metadata` |

Las 3 estrategias robustas distintas se generaron: una por cada worker (Kronos=3.1.17, Hera=8.1.24, Zeus=8.1.25). El databank de `EchoForgeRobustRunExporter/output/` queda con 1 archivo por worker porque el exporter corre 1 estrategia por invocación.

### 7. Las dos carpetas en MinIO (`NDX_example_flow_4{6,7}_v1_wtest`)

NO es algo del watcher "cagándola" ni de pruebas anteriores. Es el patrón documentado:

- El watcher sube los `.cfx` de `00_configs/` con el prefijo `…/v1/NDX_example_flow_4X_v1_wtest/00_configs/` (sin `request_id`).
- El workflow después lee la config desde ese path (lo confirma el log: `"config_key":"…/NDX_example_flow_47_v1_wtest/00_configs/optimizer_test.cfx"`).

Fecha de creación: `flow_46` 05:22:40Z, `flow_47` 05:23:28Z — antes del workflow real (05:32:28Z para `flow_47`). **Comportamiento esperado del watcher**.

## Preguntas del usuario respondidas

### 1. "Se abrieron 12 `apply_selected_run`, ¿no deberían haber 12 robustas?"

**Sí, las 12 robustas se generaron** (ver evidencia §4). El que solo veamos 1 archivo en `/home/kor/sqx/user/projects/EchoForgeRobustRunExporter/databanks/output/` por worker es porque el exporter se ejecuta **una estrategia por invocación**, así que cada llamada sobrescribe el `output/`. En MinIO sí están las 12.

### 2. "La tarea de `05_reretester` sí corrió — input contract es X. ¿Por qué no se siguió?"

**Sí corrió** pero con `filtered_count: 0` por la incompatibilidad de sufijos. La actividad termina con `status: success`, `started_count: 0`, `output_count: 0` y el workflow no encadena nada porque no hay outputs que pasar.

### 3. "¿Fue el watcher el que la cagó? ¿O fueron tus pruebas?"

**Ninguna de las dos**. Las dos carpetas `…_v1_wtest/` son del watcher (prefijo legacy sin `request_id`) y se usan legítimamente por el workflow (log confirma el `cfg_id: NDX_example_flow_4X_v1_wtest`). Las pruebas que hice solo invocaron `ListStrategies`/`ListObjects` que son **read-only** — no escribieron nada.

## Causa raíz última: diseño del flow

El config actual mezcla dos convenciones:

```json
{
  "type": "apply_selected_run",
  "folder": "04_optimizer_robust",
  "source_folder": "03_optimizer"
}
```
produce `_robust.sqx` en `04_optimizer_robust/` (12 archivos), pero el workflow mantiene en `InputBatch.Keys` los nombres `WF_Matrix_-_...` del `03_optimizer` (que es el `source_folder` que el step lee).

El siguiente step:
```json
{
  "type": "project",
  "folder": "05_reretester",
  "source_folder": "04_optimizer_robust"
}
```
busca en `04_optimizer_robust/` por **nombre exacto** y nunca matchea.

## Soluciones posibles (a evaluar por arquitecto)

1. **Mínimo cambio**: en `apply_selected_run`, después de producir `_robust.sqx`, **escribir también el nombre base equivalente** (`NDX_…_Strategy_X.X.XX.z0.sqx` sin sufijo) como **symlink** o duplicado en la misma carpeta `04_optimizer_robust/`. Cambio pequeño, baja superficie.
2. **Cambio en el flow**: pasar como `keys` los `_robust` directamente al `05_reretester` (actualizar `apply_selected_run` para que devuelva los nombres `_robust` en lugar de los `WF_Matrix`).
3. **Cambio en el step**: cambiar el filtro de `prepareProjectInput` para hacer **match por prefijo / sufijo de strategy** (`Strategy_X.X.XX.z0`) en vez de por igualdad de nombre completo.
4. **Cambio en el config**: agregar un task intermedio tipo `remap_robust_keys` entre `apply_selected_run` y `05_reretester` que mapee WF_Matrix → robust.

## Skills / Reglas activadas

- `.agents/skills/worker-troubleshooting/SKILL.md`
- `.agents/rules/11-verify-spec.md` (verificación bit-a-bit)

## Archivos relevantes

- `sqx/activities/worker/steps/steps.go` (líneas 195-218 — el filtro bug)
- `sqx/activities/worker/robust_activity.go` (líneas 280-285 — fija el sufijo `_robust` en `SourceStrategyArtifact`)
- `sqx/activities/watcher/steps.go` (PipelineStep project / upload)
- `input/example/config.json` (config del flow afectado)
- `scratch/inspect_reretester_activity.go` (script de evidencia)

## Status

Diagnóstico confirmado al 100% con:
- Inspección del input/output literal en Temporal
- Conteo de actividades en el workflow
- Estado de MinIO (12 robustas + 12 WF_Matrix)
- Logs estructurados en Hera con el counter `filtered_count: 0`

**Pendiente**: el arquitecto evaluará las 4 opciones de solución propuestas y seleccionará la de menor riesgo.
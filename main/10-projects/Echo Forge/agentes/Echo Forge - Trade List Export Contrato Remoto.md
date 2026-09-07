---
type: project
owner: agent
root: false
cssclasses:
  - wide
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo Forge - Cierre de Etapa 4]]"
sprint: "[[A26Q2S7]]"
start: 2026-07-31
due:
progress: 90
repo: symphony
jira:
prs:
  - "https://github.com/xKoRx/symphony/pull/50"
tags:
  - area/echo
  - project/echo-forge
  - kind/project
  - owner/agent
created: 2026-07-31
updated: 2026-08-04
aliases:
  - EF-G32
  - Trade List Export Contrato Remoto
  - trade_list_exporter contrato remoto
---

# Echo Forge - Trade List Export Contrato Remoto

> [!info]+ Echo Forge - Trade List Export Contrato Remoto
> **Padre:** [[Echo Forge - Cierre de Etapa 4]] · **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Sprint:** [[A26Q2S7]]
> Rediseño del contrato de la task `trade_list_exporter`: una sola activity Temporal autosuficiente que exporta, publica en MinIO y registra en Mongo. Cero paths de filesystem local en el contrato entre activities. Gap `EF-G32`.

## 🎯 Objetivo

- Eliminar el bug de arquitectura: hoy `trade_list_exporter` devuelve `ndjson_path` (ruta local del worker A) y el workflow se lo pasa a `act_upsert_trade_list`, que Temporal puede schedular en el worker B, donde ese archivo no existe.
- Dejar el contrato Temporal de trade list **puramente remoto**: identificadores de scope + keys de MinIO + manifest. Los directorios locales pasan a ser detalle privado de la activity, nunca contrato.
- Pagar la deuda de aridad (`activity expects exactly 1 argument, got 3`) retirando la activity que la causaba, no parchándola.
- Cerrar los skips silenciosos del flujo (scope inválido, 0 trades) que hoy marcan éxito sin publicar nada.

## 📊 Estado actual

- **2026-08-04 — Estado del ciclo reajustado por owner.** EF-G32 sigue siendo requisito del smoke: impide que una activity posterior intente leer el NDJSON local de otro worker. T1–T8 permanecen implementados; falta integrar/desplegar la versión que los contiene y demostrar publish+Mongo dentro del smoke. EF-G28 no requiere desarrollo: `05_reretester`/`reretester_test.cfx` ya alimenta a TradeList mediante `source_folder`. EF-G29 está deprecado y EF-G31 diferido; la única precondición funcional pendiente es EF-G30 (identidad real, sin defaults).
- **2026-08-02 — Hotfix cluster publish MinIO (en curso E2E).** En rama `fix/ef-g32-trade-list-remote-contract`, worker desplegado `0.2.30` (3 hosts). Dos blockers runtime de publish cerrados: Stat 404 mal clasificado ([[2026-08-02-minio-nosuchkey-misclassified-as-transient]]) y `Content-Type` en UserMetadata ([[2026-08-02-minio-content-type-user-metadata-rejected]]). Ver [[2026-08-02-echo-forge-trade-list-minio-stat-put-fix]]. Pendiente: confirmar éxito E2E de `trade_list_exporter` en `example_flow_65+` / `example_flow_67`, commit de working tree sdk+symphony, merge PR [#50](https://github.com/xKoRx/symphony/pull/50).
- **2026-07-31/08-01 — Implementación T1–T8 + PR listos (90%; contexto histórico).** Código mergeado en branch `fix/ef-g32-trade-list-remote-contract`; PR [#50](https://github.com/xKoRx/symphony/pull/50) abierto para Review. Tests verdes en worker/domain/runtime/storage-minio/workflows/cmd. La lista histórica de bloqueos fue sustituida por la decisión vigente de 2026-08-04: EF-G28 está cubierto por `05_reretester`, EF-G29 deprecado, EF-G31 diferido y EF-G30 es la única precondición funcional.
- Desviación registrada: al cambiar la firma de `UploadScopeArtifacts`, `ProjectActivity.UpsertTradeList` seguía siendo caller (hueco del plan tras T2d); se retiró en la misma ventana de compilación que T3 (contenido de T6). El PR supera 20 archivos porque EF-G32 depende de `BuildMinIOPath`/CanonicalStrategyID aún no en `master`.
- **Dependencia vigente con el padre:** `EF-G32` es **ortogonal y solo-Go**: no toca el fix Robust Run ni los `.cfx`. Debe estar integrado antes del smoke E2E, porque sin este contrato Temporal puede publicar/exportar en un host y luego intentar el upsert desde otro host sin acceso al path local. `05_reretester` ya es la fuente configurada de TradeList; la precondición funcional pendiente del smoke es EF-G30 (identidad real). EF-G29 está deprecado y EF-G31 diferido por decisión del owner.
- **Efecto colateral deseado y explícito:** al cerrar el skip silencioso de `trade_count == 0`, el pipeline **falla en voz alta** si el insumo de `05_reretester` no contiene órdenes cerradas. Es intencional (regla anti-masking + lección de proceso de `§10.8`): antes publicaba manifests vacíos y marcaba la wave como exitosa. El smoke debe confirmar que el productor configurado sí entrega órdenes; no se crea otra etapa para ello.

## 🧭 Contexto verificado — no volver a investigar esto

Todo lo de esta sección fue verificado leyendo el código el 2026-07-31. El agente implementador debe tomarlo como dado.

### Estado real del código (rutas relativas a la raíz del repo `symphony`)

| Rol | Archivo | Hecho relevante |
|---|---|---|
| Activity de export | `sqx/activities/worker/trade_list_exporter_activity.go` | `Execute` termina devolviendo `NDJSONPath`/`ManifestPath`/`SuccessPath`/`OutputDir` **locales** + `Manifest` parseado. No sube nada a MinIO ni escribe Mongo. |
| Activity de upsert | `sqx/activities/worker/project_activity.go` L293-335 (`ProjectActivity.UpsertTradeList`) | Firma `(ctx, scope, manifest, ndPath string)`. Lee `ndPath` del disco local → viola el invariante por construcción. |
| Wrapper Temporal | `sqx/cmd/sqx-worker/main.go` L392-420 (`actUpsertTradeList`) | Registra `act_upsert_trade_list` con **3 argumentos**. Origen del `expects exactly 1 argument, got 3`. |
| Wiring | `sqx/cmd/sqx-worker/main.go` L294 | `NewExportTradeListActivity(metadataStore, metadataStore, metadataStore, storageAdapter, sqxExecutor, di.Container.Etcd)` — **no** recibe writer MinIO ni repo Mongo de trade list. |
| Wiring de puertos ya disponibles | `sqx/cmd/sqx-worker/main.go` L241-268 | `tradeListRepo` (`capabilities.TradeManifestRepository`) y `tradeListWriter` (`*storageminio.TradeListStorage`, implementa `TradeArtifactWriter` y `TradeArtifactReader`) **ya existen construidos** en `main`. Solo hay que pasarlos también a la activity de export. |
| Workflow (camino simple) | `sqx/workflows/generic_workflow.go` L927-1055 | `case "trade_list_exporter"`. L1040 deriva scope, L1048 llama `act_upsert_trade_list` con `exportRes.NDJSONPath`. |
| Workflow (camino grupo) | `sqx/workflows/generic_workflow.go` L2465-2593 | Bloque análogo, idéntico problema, L2586. |
| Helper a borrar | `sqx/workflows/generic_workflow.go` L2788-2809 (`scopeFromExportedManifest`) | Devuelve `nil` si el scope no valida → el workflow hace `continue` y **marca éxito sin publicar**. Es el único uso de los imports `sqxsdk` y `capabilities` en ese archivo. |
| Puerto MinIO | `sqx/adapters/storage-minio/trade_lists.go` (`UploadScopeArtifacts`) | Sube el paquete del scope, calcula sha256, es **idempotente** (noop si ETag coincide, re-upload si difiere el tamaño) y clasifica errores en `ErrTradeContract` / `ErrTradeTransient`. Toda esa mecánica se conserva. Lo único que cambia (T3) es **quién decide la key**: hoy la inventa `remoteArtifactKey` (L467-506) con un esquema paralelo. |
| Contrato de paths en MinIO | `sqx/core/domain/paths.go` L8-27 (`BuildMinIOPath`) | Doc explícito: es el **mecanismo ÚNICO** de rutas, determinista por identidad lógica (`instrument/direction/timeframe/strategy/version`) y **sin segmentos de ejecución** (`request_id`, `run_id`, `trace_id`). Nombra a `trade_list_exporter` entre los consumidores obligados. `remoteArtifactKey` lo viola de frente: emite `waves/.../requests/<request_id>/runs/<run_id>/...`. |
| Key builder duplicado | `sqx/core/capabilities/trade_keys.go` (`TradeArtifactKeyBuilderImpl`) + puerto `TradeArtifactKeyBuilder` en `trades.go` L73-78 | **Código muerto:** el único caller es su propio test. Nadie lo inyecta ni lo usa en producción. Codifica el mismo esquema prohibido con `request_id`/`run_id`. |
| Validación de la key | `sdk/pkg/sqx/trade_manifest.go` L135-138 (`TradeArtifactRef.Validate`) | Solo exige `artifact_key` **no vacía**. No hay patrón, sufijo ni prefijo obligatorio → cambiar la forma de la key **no toca el SDK**. |
| Datos de placement ya disponibles | `sqx/activities/worker/trade_list_exporter_activity.go` L185-240 (`resolveRobustArtifactKey`) | La activity **ya resuelve** `instrument`, `dirCode`, `timeframe` (de `StrategyMetadata` + partes del `StrategyID`) y recibe `strategy`, `version`, `folder` en `ExportTradeListRequest` (L84-87). O sea: todo lo que `BuildMinIOPath` necesita ya está calculado ahí. |
| Puerto Mongo | `sqx/adapters/metadata-mongo/trade_lists.go` (`UpsertManifest`) | `ReplaceOne` con `upsert:true` sobre la clave natural de 9 campos; índice único `uniq_scope_natural_v1`. **Idempotente. No hay que tocarlo.** |
| Clasificación non-retryable | `sqx/activities/worker/project_activity.go` L337-393 | `wrapTradeContractForTemporal` + `nonRetryableTradeError`. Viven en el paquete `worker`, así que la activity de export puede usarlos sin mover nada. **Bug latente:** `nonRetryableTradeError` es un tipo propio y la `RetryPolicy` del workflow (`generic_workflow.go` L56-61) **no** declara `NonRetryableErrorTypes` → hoy un error de contrato reintenta para siempre. |
| Layout local del plugin | `sqx/exporter-plugin/src/SQ/CustomAnalysis/trades/TradeListArtifactWriter.java` | Escribe `trades.ndjson.gz`, `trades_manifest.json`, `export_run.json`, `_SUCCESS` dentro de `<outputDir>/<strategyId>___<sample>/`. `_SUCCESS` solo si todo lo anterior tuvo éxito. |
| Directorios locales | `sqx/core/runtime/config.go` L161-180 | `GetSQXPaths(project)` → `databanks/input`, `databanks/output`. `GetSQXTradeListOutputDir(project)` → `user/projects/<project>/tradelist` (**tercer directorio**, se elimina en T2c). |
| Limpieza de databanks | `sqx/core/runtime/config.go` L187-213 (`CleanProjectDatabanks`) | Ya existe y limpia `databanks/input` + `databanks/output` + `overview` del proyecto. Es la primitiva que la activity debe usar antes y después de cada ejecución. |
| Config del flujo | `input/example/config.json` L102-106 | La task se declara `{"type":"trade_list_exporter","source_folder":"05_reretester","folder":"06_trade_list"}` → **entra por el `case` del workflow**, no por el pipeline de 4 steps. |
| Pipeline de 4 steps | `sqx/activities/worker/steps/trade_lists.go` + `sqx/activities/worker/pipeline/builder.go` L45-50 | `collect/upload/import/upsert_trade_list` se insertan **solo** si `TaskSpec.ExporterProject == "EchoForgeTradeListExporter"` en una task `type: project`. Con la config actual **no se ejecutan nunca**. Es el segundo caller de `UploadScopeArtifacts` y la segunda convención de output dir. Se borra en T2d. `IsTradeListTask` solo se usa en `builder.go` y su test (verificado por grep). |
| ActivityOptions | `sqx/workflows/generic_workflow.go` L51-62 y L1630-1641 | `HeartbeatTimeout: 2m`, `StartToCloseTimeout: 10d`, `MaximumAttempts: 0` (reintentos ilimitados), `InitialInterval: 1m`, backoff 2.0, máx 30m. Sin `NonRetryableErrorTypes`. |
| Temporal SDK | `go.mod` L22 | `go.temporal.io/sdk v1.35.0`. `temporal.NewNonRetryableApplicationError(msg, errType, cause, details...)` existe y `*ApplicationError` implementa `Unwrap()`, así que `errors.Is(err, sqxcore.ErrTradeContract)` sigue funcionando tras envolver. |
| Concurrencia del worker | `sdk/pkg/shared/temporal/client.go` L144-151 | `worker.Options{MaxConcurrentActivityExecutionSize: 1}` — comentado como "Concurrencia estricta: SQX corre de a 1". **Las activities se serializan por host.** Esto es lo que hace seguro que la activity limpie `databanks/input` y el output dir en cada ejecución, aunque el workflow lance las N estrategias en paralelo. No hace falta ningún mutex ni lock de proyecto. |
| Divergencia de output dir | `sqx/activities/worker/steps/trade_lists.go` L110-112 vs `sqx/core/runtime/config.go` L178 | El step legacy busca en `databanks/output/tradelist`, mientras la activity escribe en `user/projects/<project>/tradelist`. **Nunca se encontrarían.** Síntoma de tener dos convenciones; se resuelve en T2c + T2d dejando **una sola**: `databanks/output`. |
| Input dir hardcodeado | `sqx/activities/worker/trade_list_exporter_activity.go` L328 | La activity arma `.../databanks/input` con un `filepath.Join` propio en vez de usar `runtime.GetSQXPaths`. Mismo valor, pero es una segunda fuente de verdad. Se unifica en T3. |

### Contexto de negocio que condiciona el diseño

- El `.sqx` robusto ya está en MinIO con key jerárquica determinística (`domain.BuildMinIOPath` + `domain.CanonicalStrategyFilename`), sin segmentos de ejecución. La activity lo descarga a un temp local. Eso ya es correcto y no cambia.
- El único paso que **exige disco local** es `sqcli` + el plugin Java: consume un databank de entrada y escribe archivos. Es inevitablemente local.
- El manifest es la fuente del **scope lógico**: `wave_key`, `request_id`, `run_id`, `strategy_id`, `stage`, `variant`, `result_key`, `cell_key`, `sample_type`. Ese scope es la clave natural del documento Mongo. Pero **no** es la fuente de la ruta: la ruta se deriva de la identidad de la configuración (ver `BuildMinIOPath`), y de `result_key`/`request_id`/`run_id` no depende ningún path.
- **Convención de nombres del resto del pipeline** (`03_optimizer`, `04_optimizer_robust`, `05_reretester`, `mt5_eas`): un archivo por estrategia, nombrado `<canonical_strategy_id>.<ext>`, dentro de la carpeta que declara el campo `folder` de la task en `config.json`. La etapa se distingue por **carpeta**, no por nombre de archivo (`domain.CanonicalStrategyFilename`, `sqx/core/domain/canonical_strategy_id.go` L153-163). El trade list debe entrar por esta misma puerta.

## 🧱 Diseño objetivo

### Secuencia Temporal

**Antes (roto):**

```text
worker A: trade_list_exporter  →  NDJSON en disco de A, retorna path de A
worker B: act_upsert_trade_list(scope, manifest, /path/de/A)  →  ENOENT
```

**Después:**

```text
worker A: trade_list_exporter
   1. carga selected_robust_run + robust_run_setup (Mongo)
   2. descarga .sqx robusto (MinIO → temp local)
   3. limpia databanks/input + databanks/output
   4. prepara databanks/input + exporter.properties (output_dir=databanks/output)
   5. ejecuta sqcli (plugin Java)          ← único paso local, inevitable
   6. localiza TODOS los scope dirs con _SUCCESS bajo databanks/output
   7. por cada scope: valida manifest → deriva scope → construye la key con
                      BuildMinIOPath → UploadScopeArtifacts (MinIO)
                      → UpsertManifest (Mongo)
   8. limpia databanks/input + databanks/output (solo si todo publicó)
   9. retorna SOLO identificadores remotos
(no hay segunda activity)
```

Una sola activity. El invariante se cumple por construcción: nada del filesystem cruza el borde de la activity.

### Contrato nuevo

`sqx/activities/worker/trade_list_exporter_activity.go`:

```go
// ExportTradeListRequest NO cambia. Sigue siendo un único struct.

// PublishedTradeList describe un scope publicado. Solo identificadores
// remotos: cualquier consumidor posterior localiza el artefacto en MinIO
// por ArtifactKey y el documento en Mongo por Scope.
type PublishedTradeList struct {
	Scope             capabilities.TradeScope `json:"scope"`
	ArtifactKey       string                  `json:"artifact_key"`
	ArtifactSHA256    string                  `json:"artifact_sha256"`
	CompressedBytes   int64                   `json:"compressed_bytes"`
	UncompressedBytes int64                   `json:"uncompressed_bytes"`
	TradeCount        int                     `json:"trade_count"`
}

// ExportTradeListResult es el output de la activity. Invariante:
// ningún campo puede contener una ruta de filesystem.
type ExportTradeListResult struct {
	ExportStatus string               `json:"export_status"` // "EXPORTED"
	ExportedAt   time.Time            `json:"exported_at"`
	Published    []PublishedTradeList `json:"published"`
	TradeCount   int                  `json:"trade_count"` // suma de todos los scopes
}
```

Campos eliminados: `NDJSONPath`, `ManifestPath`, `SuccessPath`, `OutputDir`, `Manifest`.

### Layout de artefactos

**Remoto (MinIO) — una sola convención, la del resto del pipeline.**

```text
wave_<wave>/<instrument>/<l|s>_<tf>/<strategy>/<version>/<folder>/<canonical_strategy_id>.trades.ndjson.gz
wave_<wave>/<instrument>/<l|s>_<tf>/<strategy>/<version>/<folder>/<canonical_strategy_id>.trades.manifest.json
```

Ejemplo real con la task `{"type":"trade_list_exporter","folder":"06_trade_list"}`:

```text
wave_flow_46/ndx/l_h1/example_flow_46/v1/06_trade_list/NDX_L_H1_example_flow_46_v1_Strategy_3.1.14.z0.trades.ndjson.gz
```

Se construye con `domain.BuildMinIOPath(wave, instrument, dirCode, tf, strategy, version, req.Folder, filename)`, exactamente igual que el `.sqx` que la propia activity descarga de `05_reretester`. Nueve estrategias → nueve archivos distintos en la misma carpeta, uno por estrategia, igual que en todas las demás etapas.

**Desambiguación cuando hay más de un scope por estrategia** (muestras IS/OOS o celdas WFM; hoy el plugin emite solo `FULL` porque `stage=robust_run_setup`):

```text
<canonical_strategy_id>.trades.ndjson.gz                 sample FULL, sin celda  ← caso normal
<canonical_strategy_id>.OOS.trades.ndjson.gz             sample != FULL
<canonical_strategy_id>.OOS.<cell>.trades.ndjson.gz      celda WFM
```

**Local — solo `databanks/input` y `databanks/output`.**

```text
<sqx_base>/user/projects/EchoForgeTradeListExporter/
  databanks/input/<canonical_strategy_id>.sqx      ← lo que consume sqcli
  databanks/output/<strategyId>___FULL/{trades.ndjson.gz, trades_manifest.json, _SUCCESS}
```

`databanks/output` es el `output_dir` que la activity escribe en `exporter.properties`, así que el plugin Java obedece sin tocar el plugin. Los nombres **dentro** de `databanks/output` los pone el plugin Java y no importan: ese directorio se limpia completo antes y después de cada ejecución, y el nombre canónico se aplica al publicar en MinIO.

**Ciclo de limpieza (obligatorio en cada ejecución de la activity):**

1. `runtime.CleanProjectDatabanks(ctx, project)` **antes** de escribir el input → garantiza que ninguna task previa contamine esta.
2. Ejecutar `sqcli`, descubrir scopes, publicar en MinIO + Mongo.
3. `runtime.CleanProjectDatabanks(ctx, project)` **después**, solo si la publicación fue exitosa → deja el disco limpio sin borrar la evidencia de un fallo.

El paso 3 es seguro porque al llegar ahí el artefacto ya vive en MinIO y su manifest en Mongo. Si algo falló, los archivos quedan en disco para RCA y la siguiente ejecución los borra en el paso 1.

### Reglas de fallo (anti-masking)

| Situación | Hoy | Objetivo |
|---|---|---|
| Ningún `_SUCCESS` bajo el output dir | error enriquecido con `export_run.json` | igual, se mantiene |
| Manifest ilegible o `Validate()` falla | error genérico → reintenta 10 días | `ErrTradeContract` → non-retryable |
| Scope derivado del manifest no valida | warning + `continue`, wave marcada exitosa | `ErrTradeContract` → non-retryable |
| Suma de `trade_count` de todos los scopes == 0 | publicaría manifests vacíos | `ErrTradeContract` → non-retryable, mensaje explícito |
| Un scope individual con `trade_count == 0` pero otros con datos | — | warning, se publica igual (una muestra OOS vacía es posible) |
| Fallo de MinIO/Mongo transitorio | — | error transient → Temporal reintenta |

## 🗺️ Plan de implementación

> [!important]+ Reglas para el agente implementador
> 1. **No inventes rutas ni símbolos**: todo lo que necesitas está en §🧭 Contexto verificado con archivo y línea.
> 2. **No toques** `sqx/adapters/metadata-mongo/trade_lists.go`: ya es idempotente y correcto. De `sqx/adapters/storage-minio/trade_lists.go` cambia **solo** lo que T3 indica (de dónde sale la key y el nombre del sidecar); la mecánica de sha256, idempotencia y clasificación de errores se conserva intacta.
> 3. **No toques el plugin Java** ni los `.cfx`. Este gap es solo-Go.
> 4. **No agregues test-skips ni relajes asserts** para que pase la build. Si un test existente falla, el fix va en producción o el test se actualiza con justificación en la bitácora de esta nota.
> 5. Ejecuta las tareas **en orden**. Cada una deja el repo compilando.
> 6. Al terminar cada tarea, marca su checkbox en §✅ Tareas y agrega una línea en §📆 Bitácora.

### T1 — `TradeScope` viaja limpio por Temporal

**Allowed files:** `sqx/core/capabilities/trades.go`

Agregar tags JSON a los 9 campos de `TradeScope` (L20-30). Nada más en ese archivo.

```go
type TradeScope struct {
	WaveKey    string                 `json:"wave_key"`
	RequestID  string                 `json:"request_id"`
	RunID      string                 `json:"run_id"`
	StrategyID string                 `json:"strategy_id"`
	Stage      sqxsdk.TradeStage      `json:"stage"`
	Variant    sqxsdk.TradeVariant    `json:"variant"`
	ResultKey  string                 `json:"result_key"`
	CellKey    *string                `json:"cell_key,omitempty"`
	SampleType sqxsdk.TradeSampleType `json:"sample_type"`
}
```

**Aceptación:** `go build ./...` verde. No hay cambio de comportamiento: el adapter Mongo mapea campo a campo a BSON y no depende de estos tags.

### T2 — Contrato non-retryable real

**Allowed files:** `sqx/activities/worker/project_activity.go`

Reemplazar el cuerpo de `temporalNonRetryable` (L368-381) por la API oficial del SDK, y borrar el tipo `nonRetryableTradeError` (L383-393) junto con el comentario que lo describe:

```go
// temporalNonRetryable envuelve err como ApplicationError non-retryable
// del SDK de Temporal. A diferencia del wrapper propio anterior, esto NO
// depende de que la RetryPolicy del workflow declare NonRetryableErrorTypes:
// Temporal respeta el flag del propio error. `*ApplicationError` implementa
// Unwrap(), así que errors.Is(err, sqxcore.ErrTradeContract) sigue siendo
// verdadero aguas abajo.
func temporalNonRetryable(err error) error {
	if err == nil {
		return nil
	}
	return temporal.NewNonRetryableApplicationError(err.Error(), "TradeContractError", err)
}
```

Agregar el import `"go.temporal.io/sdk/temporal"`.

**Aceptación:** los tests `TestWrapTradeContract*` de `project_activity_trade_list_test.go` se actualizan para afirmar (a) `errors.Is(wrapped, sqxcore.ErrTradeContract)` y (b) que un error transient **no** se envuelve. Se elimina cualquier assert que referencie `*nonRetryableTradeError`.

### T2b — Nombre canónico del trade list en `core/domain`

**Allowed files:** `sqx/core/domain/trade_list_paths.go` (nuevo), `sqx/core/domain/trade_list_paths_test.go` (nuevo)

Crear el helper que centraliza el nombre del archivo, al lado de `CanonicalStrategyFilename` y con la misma filosofía: una sola función decide el nombre físico y nadie más lo concatena a mano.

```go
package domain

// Extensiones canónicas del trade list. El artefacto es el mismo NDJSON
// gzipeado que produce el plugin Java; solo cambia el nombre con el que
// se publica, para que la carpeta de la etapa se lea igual que las demás
// (un archivo por estrategia, nombrado por su canonical_strategy_id).
const (
	TradeListArtifactExt = ".trades.ndjson.gz"
	TradeListManifestExt = ".trades.manifest.json"
)

// TradeListArtifactFilename devuelve el nombre físico del NDJSON de trades
// de una estrategia:
//
//	<canonical_strategy_id>.trades.ndjson.gz                 sample FULL sin celda
//	<canonical_strategy_id>.<SAMPLE>.trades.ndjson.gz        sample != FULL
//	<canonical_strategy_id>.<SAMPLE>.<cell>.trades.ndjson.gz celda WFM
//
// sampleType y cellKey solo aparecen cuando aportan información: el caso
// normal (FULL, sin celda) produce el nombre limpio. Así una carpeta de
// etapa con N estrategias tiene N archivos y ninguna colisión, y el
// nombre sigue siendo legible por un humano que lista el bucket.
//
// Devuelve "" si strategyID no produce un canonical id (input inválido);
// el caller debe tratarlo como error de contrato.
func TradeListArtifactFilename(strategyID, sampleType, cellKey string) string

// TradeListManifestFilename es el sidecar JSON del mismo scope, con
// idéntica lógica de sufijos y extensión TradeListManifestExt.
func TradeListManifestFilename(strategyID, sampleType, cellKey string) string
```

Reglas de implementación:

- `id := CanonicalStrategyID(strategyID)`; si queda vacío → devolver `""`.
- `sampleType` se omite si está vacío o si en mayúsculas es `FULL`; si no, se usa en mayúsculas.
- `cellKey` se omite si está vacío (trim).
- Sanitizar `sampleType` y `cellKey` reemplazando todo lo que no sea `[A-Za-z0-9_-]` por `_`, para que una celda WFM con caracteres raros no rompa la key.
- Función pura: sin I/O, sin env, sin `os.Getenv` propio (el hostKey ya lo maneja `CanonicalStrategyID`).

**Tests (tabla):** caso normal produce `NDX_L_H1_example_flow_46_v1_Strategy_3.1.14.z0.trades.ndjson.gz`; input con prefijo `WF_Matrix_-_` y sufijo `_robust` normaliza al mismo nombre; `sample=OOS` inserta `.OOS`; `cell="2020Q1"` inserta `.OOS.2020Q1`; celda con `/` o espacios queda sanitizada; strategyID vacío devuelve `""`; **unicidad**: un mapa con las combinaciones (2 estrategias × {FULL, IS, OOS} × {sin celda, celda}) no produce nombres repetidos.

**Aceptación:** `go test ./sqx/core/domain/...` verde.

### T2c — Databanks: solo `input` y `output`

**Allowed files:** `sqx/core/runtime/config.go`, `sqx/core/runtime/config_test.go`

El proyecto del exporter deja de tener un tercer directorio. `GetSQXTradeListOutputDir` se mantiene como nombre (dos callers lo usan y documenta la intención) pero pasa a delegar en `GetSQXPaths`, que es la única fuente de verdad:

```go
// GetSQXTradeListOutputDir devuelve el directorio donde el plugin Java del
// exporter deja sus artefactos: el databank de salida del proyecto.
//
// Antes esto apuntaba a un tercer directorio hermano
// (`user/projects/<project>/tradelist`). Se elimina a propósito: el
// contrato de cada task es "leo de databanks/input, escribo en
// databanks/output, y limpio ambos antes y después". Un directorio fuera
// de ese par no lo limpia nadie, así que acumulaba artefactos de
// ejecuciones viejas que la siguiente task podía volver a descubrir
// (datos contaminados) y obligaba a mantener dos convenciones de ruta
// para lo mismo.
func GetSQXTradeListOutputDir(projectName string) string {
	_, outputDir := GetSQXPaths(projectName)
	return outputDir
}
```

En `config_test.go`, `TestGetSQXTradeListOutputDir` (L301-315) espera hoy `.../tradelist`. Actualizarlo para afirmar (a) que el resultado es exactamente `.../databanks/output`, (b) que coincide con el `outputDir` de `GetSQXPaths` para el mismo proyecto, y (c) que sigue sin contener `C:` (la regresión Windows-style que el test original protegía).

**Aceptación:** `go test ./sqx/core/runtime/...` verde.

### T2d — Borrar el pipeline legacy de 4 steps

**Allowed files:** `sqx/activities/worker/steps/trade_lists.go` (borrar), `sqx/activities/worker/steps/trade_lists_test.go` (borrar), `sqx/activities/worker/steps/steps.go`, `sqx/activities/worker/pipeline/builder.go`, `sqx/activities/worker/pipeline/builder_test.go`

Los steps `collect/upload/import/upsert_trade_list` son una segunda implementación del mismo flujo, inalcanzable con la config actual (requieren `type: project` + `ExporterProject == "EchoForgeTradeListExporter"`), y son el segundo caller de `UploadScopeArtifacts`. Mantenerlos obligaría a sostener dos convenciones de naming y de output dir. Se borran:

1. `rm sqx/activities/worker/steps/trade_lists.go sqx/activities/worker/steps/trade_lists_test.go`.
2. En `steps/steps.go` L1455-1460: quitar la llamada `RegisterAllTradeListSteps(reg)` y el comentario que la acompaña.
3. En `pipeline/builder.go`: borrar `IsTradeListTask` (L22-27), el bloque `if IsTradeListTask(spec) {...}` (L45-52), las 4 líneas del doc comment que describen esos steps (L32-37) y el import `strings` si queda sin uso. Dejar en el doc comment una línea que diga que la publicación del trade list vive en la activity `trade_list_exporter`, no en el pipeline.
4. En `pipeline/builder_test.go`: borrar el test de `IsTradeListTask` (L10-18) y los asserts que esperan los 4 steps (L27-28, L40-62). Los tests del orden base (`prepare_input → … → collect_results`) se conservan.
5. `sqx/activities/worker/pipeline/step.go`: dejar los campos `TradeList*` del `State` como están (no los usa nadie más, y borrarlos amplía el diff sin beneficio), pero corregir el comentario de L59 que menciona `import_trade_list`.

**Aceptación:** `go build ./...`, `go vet ./sqx/...` y `go test ./sqx/activities/worker/...` verdes. `grep -rn "collect_trade_list\|IsTradeListTask" sqx/` sin resultados.

### T3 — Activity de export: publicar y registrar

**Allowed files:** `sqx/activities/worker/trade_list_exporter_activity.go`, `sqx/adapters/storage-minio/trade_lists.go`, `sqx/adapters/storage-minio/trade_lists_test.go`, `sqx/core/capabilities/trade_keys.go` (borrar), `sqx/core/capabilities/trade_keys_test.go` (borrar), `sqx/core/capabilities/trades.go`

> [!warning]+ Esta tarea es un solo commit
> El cambio de firma de `UploadScopeArtifacts` y su único caller (la activity) viajan juntos. No intentes compilar entre el paso 0 y el paso 5.

0. **La key la decide el caller, no el adapter.** En `sqx/adapters/storage-minio/trade_lists.go`:

   a. `UploadScopeArtifacts` recibe la key ya construida:

   ```go
   // UploadScopeArtifacts sube el paquete del scope bajo artifactKey:
   //   <artifactKey>                        gzip del NDJSON canónico
   //   <artifactKey sin ext> + manifest ext sidecar JSON del manifest
   //
   // La key la construye el caller con domain.BuildMinIOPath: es el único
   // mecanismo de rutas del sistema y solo el caller conoce la identidad
   // lógica de la configuración (instrument/direction/timeframe/strategy/
   // version/folder). El adapter mueve bytes y garantiza idempotencia; no
   // inventa rutas.
   func (s *TradeListStorage) UploadScopeArtifacts(
       ctx context.Context,
       scope sqxcaps.TradeScope,
       manifest sqxsdk.TradeListManifest,
       gzipPath string,
       artifactKey string,
   ) (sqxsdk.TradeArtifactRef, error)
   ```

   Validar `artifactKey`: no vacía y sin `/` inicial → si no, `sqxcore.NewTradeContract`. Actualizar la firma en el puerto `capabilities.TradeArtifactWriter` (`sqx/core/capabilities/trades.go`).

   b. Borrar `remoteArtifactKey` (L467-506) por completo.

   c. `uploadCompanions` recibe también la key: el sidecar pasa a ser `strings.TrimSuffix(artifactKey, domain.TradeListArtifactExt) + domain.TradeListManifestExt`.

   d. **Borrar el `_SUCCESS` remoto** (L329, L338-343). Motivo: con un archivo por estrategia dentro de `06_trade_list/`, un `_SUCCESS` por carpeta sería un marcador único compartido por las 9 estrategias, es decir ambiguo por construcción. El registro de completitud de un scope es su documento en Mongo, que se escribe después del upload. Verificado por grep: **nadie lee** ese objeto (ni Go ni el plugin Java).

   e. Borrar `sqx/core/capabilities/trade_keys.go` y `trade_keys_test.go`, y el puerto `TradeArtifactKeyBuilder` de `trades.go` (L73-78). Es código muerto que codifica el esquema con `request_id`/`run_id` prohibido por `BuildMinIOPath`.

   f. En `trade_lists_test.go` del adapter: actualizar toda expectativa sobre la forma de la key (ahora se inyecta, así que los tests la pasan explícitamente) y borrar los asserts sobre el `_SUCCESS` remoto. **No** debilitar los asserts de sha256, idempotencia ni clasificación de errores.

1. **Dependencias.** Agregar dos campos al struct y dos parámetros al constructor, al final para no romper el orden existente:

1. **Dependencias.** Agregar dos campos al struct y dos parámetros al constructor, al final para no romper el orden existente:

```go
type ExportTradeListActivity struct {
	runReader   capabilities.SelectedRobustRunReader
	setupReader capabilities.RobustRunSetupReader
	metaReader  capabilities.StrategyMetadataReader
	storage     capabilities.StrategyStorage
	executor    SQXExecutor
	etcd        etcd.CacheClient
	tradeWriter capabilities.TradeArtifactWriter
	tradeRepo   capabilities.TradeManifestRepository
}

func NewExportTradeListActivity(
	runReader capabilities.SelectedRobustRunReader,
	setupReader capabilities.RobustRunSetupReader,
	metaReader capabilities.StrategyMetadataReader,
	storage capabilities.StrategyStorage,
	executor SQXExecutor,
	etcdClient etcd.CacheClient,
	tradeWriter capabilities.TradeArtifactWriter,
	tradeRepo capabilities.TradeManifestRepository,
) *ExportTradeListActivity
```

2. **Contrato.** Reemplazar `ExportTradeListResult` por la definición de §🧱 y agregar `PublishedTradeList`.

3. **Guard de dependencias.** Al inicio de `Execute`, junto a las validaciones de `RequestID`/`SelectedRobustRunKey`:

```go
if a.tradeWriter == nil || a.tradeRepo == nil {
	return ExportTradeListResult{}, wrapTradeContractForTemporal(
		sqxcore.NewTradeContract(
			errors.New("trade capabilities no inyectadas"),
			"trade_list_exporter requiere TradeArtifactWriter y TradeManifestRepository"))
}
```

3.b **Directorios: solo `input` y `output`, limpios antes y después.** Reemplazar el manejo actual de directorios (L325-355):

```go
// Contrato de la task: se lee de databanks/input y se escribe en
// databanks/output, y ambos se limpian antes y después. Un tercer
// directorio (el viejo `tradelist/`) no lo limpiaba nadie: acumulaba
// artefactos de ejecuciones previas que un descubrimiento posterior podía
// confundir con los de esta corrida.
//
// Limpiar es seguro aunque el workflow lance N estrategias en paralelo:
// el worker corre con MaxConcurrentActivityExecutionSize: 1, así que las
// activities se serializan por host.
if err := runtime.CleanProjectDatabanks(ctx, EchoForgeTradeListExporterName); err != nil {
	return ExportTradeListResult{}, sqxcore.NewTradeTransient(err, "limpiar databanks previo al export")
}

tlInputDir, outputDir := runtime.GetSQXPaths(EchoForgeTradeListExporterName)
```

- Ambos directorios se crean con `os.MkdirAll` después de limpiar (`CleanProjectDatabanks` puede dejarlos ausentes).
- Borrar el `filepath.Join(sqxDir, "user", "projects", ..., "databanks", "input")` hardcodeado (L328) y el barrido manual de `.sqx` (L332-339): la limpieza ya lo cubre.
- Borrar `clearTradeListOutputDir` (L440-459) y las constantes que queden sin uso.
- `outputDir` se sigue escribiendo tal cual en `exporter.properties` (`output_dir=`), así que el plugin Java no cambia.
- **Al final de `Execute`, tras publicar todos los scopes con éxito**, limpiar otra vez con `CleanProjectDatabanks`. Si falla la limpieza final, solo loguear warning: los artefactos ya están en MinIO y Mongo, así que la ejecución **no** debe fallar por no poder borrar. Si el export o la publicación fallaron, **no** limpiar: los archivos quedan para RCA y la siguiente ejecución los borra.

3.c **Placement único para leer y escribir.** Extraer de `resolveRobustArtifactKey` (L185-240) la resolución de identidad, para que la key de origen (`05_reretester/<id>.sqx`) y la de destino (`06_trade_list/<id>.trades.ndjson.gz`) usen exactamente los mismos valores y no puedan divergir:

```go
// tradeListPlacement es la identidad lógica de configuración que
// BuildMinIOPath necesita. Se resuelve una sola vez por ejecución y la
// usan tanto la descarga del .sqx robusto como la publicación del trade
// list, para que ambos coincidan por construcción.
type tradeListPlacement struct {
	Wave       string
	Instrument string
	DirCode    string
	Timeframe  string
	Strategy   string
	Version    string
}

func (a *ExportTradeListActivity) resolvePlacement(
	ctx context.Context,
	selectedRun domain.SelectedRobustRun,
	strategyName, version string,
) (tradeListPlacement, error)
```

`resolveRobustArtifactKey` pasa a recibir el placement + el stage y solo llama a `BuildMinIOPath`. La lógica de derivación (metadatos → `parts := strings.Split(StrategyID, "_")` → `dirCode`) se mueve tal cual, **sin cambios de comportamiento**.

La carpeta destino viene de la task:

```go
// destFolder es el `folder` que declara la task en config.json
// ("06_trade_list"). Es la misma carpeta donde el resto de las etapas
// deposita su archivo por estrategia.
destFolder := strings.TrimSpace(req.Folder)
if destFolder == "" {
	destFolder = tlDefaultDestFolder // const = "06_trade_list"
	telemetry.Warn(ctx, "trade_list_exporter: task sin folder, usando default",
		attribute.String("folder", destFolder))
}
```

4. **Descubrir todos los scopes.** Sustituir `findTradeListScopeArtifacts` (singular, corta en el primer `_SUCCESS` con `errStopWalk`) por una versión plural. Borrar `errStopWalk` si queda sin uso:

```go
// tradeListScopeArtifacts son los 3 archivos que el plugin Java emite
// dentro de un scope dir (`<strategyId>___<sample>[___cell]`).
type tradeListScopeArtifacts struct {
	ScopeDir     string
	NDJSONPath   string
	ManifestPath string
	SuccessPath  string
}

// findAllTradeListScopeArtifacts recorre root y devuelve un entry por cada
// `_SUCCESS` encontrado, ordenado por ScopeDir para que el resultado sea
// determinista. El plugin puede emitir más de un scope por ejecución
// (FULL / IS / OOS, o celdas WFM): quedarse con el primero perdía datos
// en silencio.
func findAllTradeListScopeArtifacts(root string) ([]tradeListScopeArtifacts, error)
```

Reglas: si un scope dir tiene `_SUCCESS` pero le falta el NDJSON o el manifest → error (contrato roto del plugin). Si no hay ningún `_SUCCESS` → error, enriquecido con `enrichTradeListFindError` (se mantiene tal cual). El root del walk ahora es `databanks/output`; conservar el guard `if info.Name() == "output" && path != root → SkipDir` tal como está (no afecta al root y sigue protegiendo de un `output/` anidado que cree SQX).

5. **Publicar cada scope.** Después del descubrimiento, por cada entry: leer y validar el manifest, derivar el scope, subir a MinIO, upsertear en Mongo.

```go
// publishScope sube el paquete del scope a MinIO y registra su manifest en
// Mongo. Es el corazón del contrato remoto: al retornar, el artefacto es
// alcanzable por cualquier worker del cluster y el disco local deja de
// importar. Ambas operaciones son idempotentes (MinIO compara sha256,
// Mongo hace upsert por clave natural), así que un reintento de la
// activity converge al mismo estado.
func (a *ExportTradeListActivity) publishScope(
	ctx context.Context,
	art tradeListScopeArtifacts,
	place tradeListPlacement,
	destFolder string,
) (PublishedTradeList, error) {
	raw, err := os.ReadFile(art.ManifestPath)
	if err != nil {
		return PublishedTradeList{}, sqxcore.NewTradeTransient(err, "leer manifest %s", art.ManifestPath)
	}
	var manifest sqxsdk.TradeListManifest
	if err := json.Unmarshal(raw, &manifest); err != nil {
		return PublishedTradeList{}, sqxcore.NewTradeContract(err, "manifest JSON inválido en %s", art.ManifestPath)
	}
	if err := manifest.Validate(); err != nil {
		return PublishedTradeList{}, sqxcore.NewTradeContract(err, "manifest inválido en %s", art.ManifestPath)
	}

	scope := scopeFromTradeListManifest(manifest)
	if err := scope.Validate(); err != nil {
		return PublishedTradeList{}, sqxcore.NewTradeContract(err, "scope derivado del manifest %s", art.ManifestPath)
	}

	// La key sale del mecanismo único de rutas, igual que el .sqx de las
	// etapas anteriores: la carpeta identifica la etapa y el filename
	// identifica la estrategia.
	filename := domain.TradeListArtifactFilename(
		manifest.StrategyID, string(manifest.SampleType), cellKeyOrEmpty(manifest.CellKey))
	if filename == "" {
		return PublishedTradeList{}, sqxcore.NewTradeContract(
			fmt.Errorf("strategy_id inválido en manifest: %q", manifest.StrategyID),
			"nombre de artefacto para %s", art.ScopeDir)
	}
	artifactKey := domain.BuildMinIOPath(
		place.Wave, place.Instrument, place.DirCode, place.Timeframe,
		place.Strategy, place.Version, destFolder, filename)

	ref, err := a.tradeWriter.UploadScopeArtifacts(ctx, scope, manifest, art.NDJSONPath, artifactKey)
	if err != nil {
		return PublishedTradeList{}, err // ya clasificado por el adapter
	}
	if err := a.tradeRepo.UpsertManifest(ctx, scope, manifest, ref); err != nil {
		return PublishedTradeList{}, err // ya clasificado por el adapter
	}

	return PublishedTradeList{
		Scope:             scope,
		ArtifactKey:       ref.ArtifactKey,
		ArtifactSHA256:    ref.ArtifactSHA256,
		CompressedBytes:   ref.CompressedBytes,
		UncompressedBytes: ref.UncompressedBytes,
		TradeCount:        manifest.TradeCount,
	}, nil
}

// scopeFromTradeListManifest rehidrata el scope desde el manifest.
// Reemplaza a scopeFromExportedManifest, que vivía en el workflow y
// devolvía nil (skip silencioso) en vez de un error.
func scopeFromTradeListManifest(m sqxsdk.TradeListManifest) capabilities.TradeScope

// cellKeyOrEmpty desreferencia el cell_key opcional del manifest.
func cellKeyOrEmpty(cell *string) string
```

6. **Cierre de `Execute`.** Acumular resultados, exigir trades y clasificar el error final:

```go
published := make([]PublishedTradeList, 0, len(arts))
total := 0
for _, art := range arts {
	p, errPub := a.publishScope(ctx, art, place, destFolder)
	if errPub != nil {
		telemetry.RecordError(ctx, errPub)
		return ExportTradeListResult{}, wrapTradeContractForTemporal(errPub)
	}
	if p.TradeCount == 0 {
		telemetry.Warn(ctx, "trade_list_exporter: scope publicado sin trades",
			attribute.String("scope_dir", art.ScopeDir),
			attribute.String("artifact_key", p.ArtifactKey),
		)
	}
	published = append(published, p)
	total += p.TradeCount
}

// Una estrategia robusta con cero trades cerrados es imposible: si el
// agregado es 0, el plugin no extrajo nada (ver EF-G28) y publicar el
// manifest vacío convertiría una falla en un éxito con datos falsos.
if total == 0 {
	return ExportTradeListResult{}, wrapTradeContractForTemporal(
		sqxcore.NewTradeContract(
			errors.New("trade_count agregado = 0"),
			"el exporter no extrajo trades para %s (%d scopes)",
			req.SelectedRobustRunKey, len(published)))
}

// Todo publicado: el disco local ya no aporta nada y se limpia para que
// la próxima task no encuentre residuos. Un fallo aquí no invalida la
// publicación, así que solo se loguea.
if err := runtime.CleanProjectDatabanks(ctx, EchoForgeTradeListExporterName); err != nil {
	telemetry.Warn(ctx, "trade_list_exporter: no se pudo limpiar databanks tras publicar",
		attribute.String("error", err.Error()))
}

return ExportTradeListResult{
	ExportStatus: "EXPORTED",
	ExportedAt:   time.Now().UTC(),
	Published:    published,
	TradeCount:   total,
}, nil
```

7. **Telemetría** (regla `050-observability-telemetry`): al inicio de `Execute`, una sola vez:

```go
ctx = telemetry.AppendEventAttrs(ctx,
	telemSem.Logs.Feature.String("TradeList"),
	telemSem.Logs.Event.String("export.publish"),
)
```

El span `activity.trade_list_exporter` ya existe y se mantiene. Agregar `attribute.Int("scopes_published", len(published))` y `attribute.Int("trade_count_total", total)` antes del return. Un span hijo por scope: `telemetry.StartSpan(ctx, "trade_list.publish_scope")` dentro de `publishScope`, cerrado con `defer`. Todos los errores pasan por `telemetry.RecordError`.

8. **Doc comment del archivo.** Reescribir el bloque de cabecera: la activity ahora es autosuficiente y el contrato de salida es remoto. Mencionar explícitamente por qué no hay segunda activity.

**Aceptación:** `go build ./...` y `go vet ./sqx/...` verdes.

### T4 — Workflow: una sola llamada

**Allowed files:** `sqx/workflows/generic_workflow.go`

1. En el bloque `case "trade_list_exporter"` (~L1026-1055), reemplazar el loop de futures por:

```go
for idx, f := range exportFutures {
	var exportRes worker.ExportTradeListResult
	if err := f.Get(ctx, &exportRes); err != nil {
		di.Container.Telemetry.Error(context.Background(), "Error en trade_list_exporter para la estrategia "+strategies[idx], err)
		return fmt.Errorf("error en trade_list_exporter para la estrategia %s: %w", strategies[idx], err)
	}
	di.Container.Telemetry.Info(context.Background(), "trade_list_exporter: trade list publicada",
		attribute.String("strategy_id", strategies[idx]),
		attribute.Int("scopes", len(exportRes.Published)),
		attribute.Int("trade_count", exportRes.TradeCount),
	)
	passedKeys = append(passedKeys, current.Keys[idx])
}
```

Se eliminan: la rama `ExportStatus != "EXPORTED" → continue`, la derivación de scope y el `ExecuteActivity("act_upsert_trade_list", ...)`. La activity ya no devuelve estados intermedios: o publica todo, o falla.

2. Aplicar el **mismo cambio** en el bloque del workflow de grupo (~L2565-2593), respetando que ahí el `return` es `runtime.StratBatch{}, fmt.Errorf(...)`.

3. Borrar `scopeFromExportedManifest` (L2788-2809) y los imports que quedan sin uso: `sqxsdk "github.com/xKoRx/sdk/pkg/sqx"` (L11) y `"github.com/xKoRx/symphony/sqx/core/capabilities"` (L17). Verificado: son sus únicos usos en el archivo.

**Aceptación:** `go build ./...` verde y `go vet` sin "imported and not used".

### T5 — Wiring del worker

**Allowed files:** `sqx/cmd/sqx-worker/main.go`

1. L294: pasar los dos puertos nuevos, que ya están construidos más arriba (L241-268):

```go
exportTradeListActivity := worker.NewExportTradeListActivity(
	metadataStore, metadataStore, metadataStore, storageAdapter, sqxExecutor, di.Container.Etcd,
	tradeListWriter, tradeListRepo,
)
```

2. Borrar el registro de `act_upsert_trade_list` (L340-358) y la función `actUpsertTradeList` (L392-420).

3. Limpiar los imports que queden sin uso tras el paso 2 (candidatos: `sqxsdk`, `capabilities` — verificar con `go build`, `capabilities` sí se usa en L241 para el tipo de `tradeListRepo`).

4. Dejar un comentario corto donde estaba el registro, explicando que el upsert vive dentro de `trade_list_exporter` porque el contrato entre activities es remoto.

5. **Una sola base path.** Justo después de cargar la config de ETCD (donde se resuelve `SQCLIBinaryPath`), fijar la base que usan los helpers de `runtime`:

```go
// runtime.GetSQXPaths / CleanProjectDatabanks cuelgan de sqxExecBasePath,
// que hasta ahora nadie inicializaba: se quedaba en el default
// "/home/kor/sqx" mientras las activities derivaban sus rutas de
// filepath.Dir(etcd "sqcli/binary_path"). Coinciden en los 3 workers
// actuales, así que esto es un no-op hoy; pero eran dos fuentes de verdad
// para la misma ruta y la activity de trade list ahora limpia directorios
// reales. Con una sola fuente, escribir y limpiar no pueden divergir.
runtime.SetSQXExecBasePath(filepath.Dir(cfg.SQCLIBinaryPath))
```

Verificar antes de desplegar: `etcdctl get <prefix>/sqcli/binary_path` debe ser `/home/kor/sqx/sqcli` en Zeus, Hera y Kronos. Si en algún host difiere, este cambio además **corrige** una divergencia real de rutas; anotarlo en la bitácora.

**Aceptación:** `go build ./sqx/cmd/sqx-worker` verde.

### T6 — Retirar la activity con path local

**Allowed files:** `sqx/activities/worker/project_activity.go`, `sqx/activities/worker/project_activity_trade_list_test.go`

1. Borrar `ProjectActivity.UpsertTradeList` (L293-335) y su bloque de comentario de sección (L273-292).
2. **No borrar** `wrapTradeContractForTemporal`, `temporalNonRetryable` ni `TradeListCapabilitiesReady`: los usa la activity de export (mismo paquete `worker`).
3. **No borrar** los campos `tradeListWriter`/`tradeListRepo`/`tradeListReader` ni sus `With*`: siguen alimentando `pipeline.Capabilities` en L162-164. Tras T2d ya no los consume ningún step, pero son inyección inerte y borrarlos amplía el diff hacia el wiring sin beneficio.
4. En el test: borrar los tres `TestProjectActivity_UpsertTradeList_*` y los helpers que solo ellos usaban. Conservar los tests de `wrapTradeContractForTemporal` ya actualizados en T2.

**Aceptación:** `go test ./sqx/activities/worker/...` verde.

### T7 — Tests de la activity

**Allowed files:** `sqx/activities/worker/trade_list_exporter_activity_test.go`

Los 5 tests existentes (`ResolvesHierarchicalKey`, `StrategyIDWithHeraSuffix`, `DownloadFails_PropagatesError`, `MetadataMissing`, `WritesCanonicalExporterProperties`) deben seguir pasando; adaptar solo la construcción del activity (dos parámetros nuevos) y los asserts sobre el result. Agregar fakes en memoria:

```go
type fakeTradeWriter struct {
	ref  sqxsdk.TradeArtifactRef
	err  error
	got  []capabilities.TradeScope
}
type fakeTradeRepo struct {
	err  error
	got  []capabilities.TradeScope
}
```

Tests nuevos, todos table-driven o con setup/ejecución/verificación explícitos:

| Test | Verifica |
|---|---|
| `TestExportTradeListActivity_Execute_PublishesAllScopes` | Con 2 scope dirs válidos en el output dir, se llama `UploadScopeArtifacts` y `UpsertManifest` **una vez por scope**, y `Result.TradeCount` es la suma. |
| `TestExportTradeListActivity_Execute_ResultHasNoLocalPaths` | Regresión del bug: por reflexión sobre `ExportTradeListResult`, ningún campo string contiene un separador de path (`os.PathSeparator`) ni el output dir del test. Este test es el que evita que el bug vuelva. |
| `TestExportTradeListActivity_Execute_ZeroTradesIsContractError` | Un scope con `trade_count: 0` → error que satisface `errors.Is(err, sqxcore.ErrTradeContract)` y **no** se llamó al writer ni al repo... o se llamó y falló al final: afirmar el error, y que el result esté vacío. |
| `TestExportTradeListActivity_Execute_InvalidScopeIsContractError` | Manifest sin `result_key` → `ErrTradeContract`, sin llamada al repo Mongo. |
| `TestExportTradeListActivity_Execute_MongoTransientPropagates` | `fakeTradeRepo.err = sqxcore.NewTradeTransient(...)` → el error propagado **no** es non-retryable. |
| `TestExportTradeListActivity_Execute_MissingCapabilities` | Sin writer/repo inyectados → `ErrTradeContract`. |
| `TestExportTradeListActivity_Execute_SuccessWithoutManifest` | Scope dir con `_SUCCESS` pero sin `trades_manifest.json` → error de contrato del plugin. |
| `TestExportTradeListActivity_Execute_ArtifactKeyFollowsStageConvention` | La `artifactKey` que recibe el writer es exactamente `wave_<wave>/<inst>/l_<tf>/<strategy>/<version>/06_trade_list/<canonical_id>.trades.ndjson.gz`, y **no** contiene `requests/`, `runs/` ni `trades.v1.ndjson.gz`. |
| `TestExportTradeListActivity_Execute_KeysAreUniquePerStrategy` | Dos estrategias del mismo wave/carpeta producen dos keys distintas (regresión de la colisión que motivó el rediseño). |
| `TestExportTradeListActivity_Execute_CleansDatabanksBeforeAndAfter` | Sembrar un `.sqx` y un scope dir basura de una "ejecución previa" en `databanks/input` y `databanks/output`: no aparecen en `Published` (limpieza previa) y tras un export exitoso ambos directorios quedan vacíos (limpieza posterior). |
| `TestExportTradeListActivity_Execute_KeepsDatabanksOnFailure` | Si la publicación falla, los artefactos del scope **siguen** en `databanks/output` para RCA. |

**Aceptación:** `go test ./sqx/activities/worker/... -run TradeList -v` verde y cobertura del archivo ≥ 85%.

> [!warning]+ Los tests que tocan `databanks` deben aislar la base
> `runtime.GetSQXPaths` cuelga de `GetSQXDataBasePath()`, que devuelve la variable de paquete `sqxExecBasePath`. El patrón ya establecido en el repo es:
>
> ```go
> original := runtime.GetSQXExecBasePath()
> defer runtime.SetSQXExecBasePath(original)
> runtime.SetSQXExecBasePath(t.TempDir())
> ```
>
> Es **estado global**: restaurarlo con `defer` es obligatorio o contaminas los demás tests del paquete. Los tests actuales de la activity (L206, L318, L501) ya llaman `SetSQXExecBasePath` pero **sin** restaurar; al tocarlos, agregar el `defer`. Y nunca apuntes a `~/sqx` real: `CleanProjectDatabanks` borra contenido de verdad.

### T8 — Test de workflow y limpieza final

**Allowed files:** `sqx/workflows/sqx_e2e_json_test.go`

1. En `sqx_e2e_json_test.go`: borrar el registro mock de `act_upsert_trade_list` (L149-151) y ajustar el mock de `trade_list_exporter` (L145-147) al nuevo result:

```go
env.RegisterActivityWithOptions(func(ctx context.Context, req worker.ExportTradeListRequest) (worker.ExportTradeListResult, error) {
	return worker.ExportTradeListResult{
		ExportStatus: "EXPORTED",
		ExportedAt:   time.Now().UTC(),
		TradeCount:   1,
	}, nil
}, activity.RegisterOptions{Name: "trade_list_exporter"})
```

Limpiar los imports `sqxcaps`/`sqxsdk` si quedan sin uso.

2. Barrido de residuos de la convención vieja, que debe dar **cero resultados** fuera de `scratch/`:

```bash
grep -rn "trades\.v1\.ndjson\.gz\|trade-manifest\.v1\.json\|remoteArtifactKey\|TradeArtifactKeyBuilder" sqx/ --include="*.go"
grep -rn '"tradelist"' sqx/ --include="*.go"
grep -rn "collect_trade_list\|IsTradeListTask" sqx/ --include="*.go"
```

(El prefijo del temp file `echoforge-tradelist-input-*.sqx` de la activity **sí** contiene la subcadena `tradelist` y es legítimo: por eso el grep busca el segmento de ruta entre comillas, no la subcadena suelta.)

Si algún test conserva una key de ejemplo con la forma vieja (`sqx/activities/worker/shadow_compute_only_test.go`, `sqx/adapters/metadata-mongo/trade_lists_test.go`), actualizarla a la nueva convención. Son strings de fixture: cambiarlos no debilita ningún assert.

3. Validación final, en la raíz del repo:

```bash
go build ./...
go vet ./sqx/...
go test ./sqx/... 2>&1 | tail -40
```

4. `graphify-personal update .` para refrescar el grafo.

**Aceptación:** los 3 comandos verdes, sin tests saltados ni asserts debilitados.

### Qué NO se hace en este alcance

- **No se toca el plugin Java.** Los nombres que escribe en disco (`trades.ndjson.gz`, `trades_manifest.json`, `_SUCCESS` dentro de `<strategyId>___<sample>/`) se quedan como están: ese directorio se limpia entero en cada ejecución, así que sus nombres no son un contrato con nadie. El nombre canónico se aplica al publicar. Tampoco se toca el contenido de `exporter.properties` más allá de `output_dir` (el resto es `EF-G30`) ni los `.cfx` (`EF-G29`).
- **No se migran los objetos MinIO viejos** bajo `waves/wave_*/requests/...`. Quedan huérfanos: nada los va a leer y todos los resultados previos ya están en cuarentena `unverified` por `§10.8` del padre. Purga en una pasada de mantenimiento aparte, no en este PR.
- **No se migran documentos Mongo.** La clave natural (los 9 campos del scope) no cambia; solo cambia el valor de `artifact_key` que se escribirá de ahora en adelante. Un documento viejo apuntando a la key vieja es basura de la cuarentena, no un dato a rescatar.
- No se implementa el recibo de publicación (`EF-G33`, ver §🚧).
- No se cambia el formato del artefacto: sigue siendo NDJSON gzipeado. Cambia el nombre, no los bytes ni el `content-encoding`.

## 🤖 Prompt maestro para la IA implementadora

Copiar tal cual. Asume que la IA tiene el repo `symphony` abierto y acceso a esta nota.

````text
Vas a implementar el gap EF-G32 del repo `symphony` (Go). El diseño ya está
cerrado y auditado: NO rediseñes, NO re-investigues, NO propongas alternativas.
Tu única fuente de verdad es la nota de proyecto:

  10-projects/Echo Forge/agentes/Echo Forge - Trade List Export Contrato Remoto.md

y, en el repo, el gap `specs/FEAT-SQX-STRATEGY-EVALUATION/G6_HANDOFF.md` §10.9.

Léelas completas antes de escribir una línea. La sección "🧭 Contexto verificado"
trae archivo y línea de todo lo que necesitas: si algo te parece que falta,
vuelve a esa sección antes de explorar el repo.

QUÉ SE ARREGLA (tres incumplimientos de la misma task, `06_trade_list`):
1. El contrato entre activities de Temporal transportaba un path del filesystem
   local, así que el upsert fallaba cuando Temporal lo schedulaba en otro worker.
   Se fusiona todo en una sola activity `trade_list_exporter` que exporta, sube a
   MinIO y upsertea en Mongo antes de retornar, y cuyo output solo lleva
   identificadores remotos.
2. La key MinIO del trade list ignoraba la decisión EF-G27: incluía
   `requests/<request_id>/runs/<run_id>`. Pasa a construirse con
   `domain.BuildMinIOPath` como todas las demás etapas:
   `<carpeta de la task>/<canonical_strategy_id>.trades.ndjson.gz`.
3. El exporter escribía en un tercer directorio local que nadie limpiaba. Pasa a
   usar solo `databanks/input` y `databanks/output`, y la activity los limpia
   antes de usarlos y después de publicar con éxito.

CÓMO TRABAJAR:
- Ejecuta las tareas en el orden exacto de la sección "🗺️ Plan de
  implementación": T1, T2, T2b, T2c, T2d, T3, T4, T5, T6, T7, T8.
- Cada tarea declara "Allowed files". No toques ningún archivo fuera de esa
  lista en esa tarea. Si crees que necesitas otro archivo, detente y repórtalo.
- Cada tarea deja el repo compilando, con una sola excepción declarada en la
  propia nota: T3 cambia la firma de `UploadScopeArtifacts` y su único caller en
  el mismo commit.
- Al terminar cada tarea: marca su checkbox en "✅ Tareas" y agrega una línea a
  "📆 Bitácora" con qué hiciste y el resultado de los comandos de aceptación.

REGLAS NO NEGOCIABLES:
- Prohibido `t.Skip`, borrar asserts, relajar comparaciones o comentar tests para
  que la build pase. Si un test existente falla, o el fix va en producción, o el
  test se actualiza y justificas el cambio en la bitácora.
- Prohibido inventar nombres, rutas o convenciones nuevas. Todo lo que hay que
  crear está especificado con su firma en la nota.
- Prohibido `fmt.Println`, `log.*` o cualquier logger ad-hoc: solo
  `github.com/xKoRx/sdk/pkg/shared/telemetry`. Los errores pasan por
  `telemetry.RecordError`. Los atributos se ponen una vez en el contexto
  (`AppendEventAttrs`), no se repiten en cada llamada.
- Configuración solo desde ETCD vía el cliente del SDK. Nada de `os.Getenv`
  salvo las excepciones ya aprobadas (`HOST_KEY`, `ENV`, `os.Hostname`).
- Las entidades de negocio viven en `github.com/xKoRx/sdk`. No crees ni
  extiendas entidades ahí; si te falta un campo, detente y repórtalo.
- Los tests que ejercitan rutas locales deben aislar la base con
  `runtime.SetSQXExecBasePath(t.TempDir())` y restaurarla con `defer`. La
  limpieza de databanks borra archivos de verdad: si apuntas a `~/sqx` destruyes
  el entorno del worker.

VALIDACIÓN FINAL (en la raíz del repo, los tres verdes y sin tests saltados):
  go build ./...
  go vet ./sqx/...
  go test ./sqx/...

Y estos greps deben dar cero resultados fuera de `scratch/`:
  grep -rn "trades\.v1\.ndjson\.gz\|remoteArtifactKey\|TradeArtifactKeyBuilder" sqx/ --include="*.go"
  grep -rn '"tradelist"' sqx/ --include="*.go"
  grep -rn "collect_trade_list\|IsTradeListTask" sqx/ --include="*.go"

Luego `graphify-personal update .` para refrescar el grafo.

ENTREGA:
- PR en español siguiendo `docs/pull_request_template.md`, con bump de versión
  PATCH en el README, evidencia antes/después y la lista de archivos tocados.
- No ejecutes el smoke E2E en el cluster desde este alcance de implementación: lo
  corre el owner después de EF-G30 y del despliegue homogéneo de EF-G32.
- Si cualquier paso te obliga a desviarte del plan, PARA y reporta la desviación
  con el archivo, la línea y el motivo. No improvises.
````

## 🧪 Verificación E2E (después del merge)

Requiere EF-G30 (identidad sin defaults) y el despliegue homogéneo de EF-G32. EF-G28 queda cubierto por `05_reretester`; EF-G29 está deprecado y EF-G31 diferido. Si el insumo configurado no entrega órdenes, `trade_count == 0` hará fallar el paso 4 a propósito.

1. Desplegar el worker en los 3 hosts (Zeus/Hera/Kronos) con la misma versión.
2. Lanzar una wave completa `00_configs → 06_trade_list` con el `config.json` de ejemplo.
3. Verificar en Temporal que `06_trade_list` ejecuta **una** activity por estrategia (ya no dos).
4. Verificar en MinIO que `wave_<wave>/<inst>/<dir_tf>/<strategy>/<version>/06_trade_list/` contiene **un `.trades.ndjson.gz` por estrategia**, nombrado igual que el `.sqx` de `05_reretester/` salvo la extensión. Con 9 estrategias: 9 archivos + 9 sidecars, ninguno pisado.
5. Verificar en Mongo `trade_lists`: un documento por scope, con `artifact_key` apuntando a esa key nueva y `artifact_sha256` coincidente con el objeto.
5b. Verificar en el worker que `user/projects/EchoForgeTradeListExporter/` tiene **solo** `databanks/` (+ `exporter.properties`) y que `databanks/input` y `databanks/output` quedaron vacíos al terminar la wave. No debe existir ningún `tradelist/`; si quedó del despliegue anterior, borrarlo a mano una vez.
6. **Prueba del invariante:** forzar que el export corra en Zeus y confirmar que el documento Mongo y el objeto MinIO quedan completos sin que ningún otro worker toque disco. Con la activity fusionada esto es estructural, pero conviene dejar la evidencia en la bitácora.

## ✅ Tareas

> [!note]+ Ownership y tarea puente
> Este es un proyecto de agente. La tarea puente humana vive en [[Echo Forge - Cierre de Etapa 4]]. Esta nota es el planificador único del trabajo delegado.

> [!example]- Fuente de tareas — editar / mover de estado aquí
> - [x] Auditar el flujo real export/upsert y aislar el invariante violado #owner/agent #type/research #area/echo
> - [x] Decidir arquitectura objetivo y registrar decisiones con rationale #owner/agent #type/research #area/echo
> - [x] Escribir el plan de implementación ejecutable por un agente ligero #owner/agent #type/research #area/echo
> - [x] **T1** — Tags JSON en `capabilities.TradeScope` #owner/agent #type/dev #area/echo
> - [x] **T2** — `temporalNonRetryable` usa `NewNonRetryableApplicationError` #owner/agent #type/dev #area/echo
> - [x] **T2b** — `domain.TradeListArtifactFilename`: un archivo por estrategia #owner/agent #type/dev #area/echo
> - [x] **T2c** — Databanks: solo `input` y `output`, muere el dir `tradelist` #owner/agent #type/dev #area/echo
> - [x] **T2d** — Borrar el pipeline legacy de 4 steps #owner/agent #type/dev #area/echo
> - [x] **T3** — Activity publica con key canónica + adapter recibe la key + limpieza de databanks #owner/agent #type/dev #area/echo
> - [x] **T4** — Workflow con una sola llamada, sin skips silenciosos #owner/agent #type/dev #area/echo
> - [x] **T5** — Wiring del worker y baja de `act_upsert_trade_list` #owner/agent #type/dev #area/echo
> - [x] **T6** — Retirar `ProjectActivity.UpsertTradeList` #owner/agent #type/dev #area/echo
> - [x] **T7** — Tests de la activity: sin paths locales, key canónica, limpieza de databanks #owner/agent #type/dev #area/echo
> - [x] **T8** — Test de workflow, barrido de residuos de la convención vieja y validación estática #owner/agent #type/dev #area/echo
> - [x] **PR** — Abrir PR en español con template, evidencia y bump de versión #owner/agent #type/dev #area/echo
> - [ ] **E2E** — Smoke real en el cluster y evidencia en bitácora (precondición funcional: EF-G30 sin defaults de identidad; fuente: `05_reretester`) #owner/agent #type/dev #area/echo #blocked
> - [r] **Cierre** — Dejar la tarea puente en Review con evidencia; solo el owner marca Done #owner/agent #type/supervision #area/echo

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label]of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any)dv.paragraph("_Sin tareas._");}
const owner=((dv.current().owner)==="agent")?"agent":"me";
const all=dv.current().file.tasks.array();
const primary=all.filter(t=>has(t,`owner/${owner}`));
const loose=all.filter(t=>!has(t,"owner/me")&&!has(t,"owner/agent"));
dv.header(3, owner==="agent"?"🤖 Tareas del agente":"🧍 Mis tareas");
board(primary);
if(loose.length){dv.header(3,"🧺 Sin owner (clasificar)");render(loose);}
```

## 🚧 Riesgos y trade-offs aceptados

| # | Riesgo | Decisión |
|---|---|---|
| R1 | Un reintento de la activity vuelve a ejecutar `sqcli` (minutos) aunque solo hubiera fallado el upsert Mongo. Con `MaximumAttempts: 0` esto puede repetirse indefinidamente si Mongo está caído. | **Aceptado.** El export es idempotente y los fallos de Mongo son raros y cortos. Escape hatch diseñado y no implementado: **EF-G33 — recibo de publicación**: al final del export, escribir `<misma carpeta de la etapa>/<canonical_strategy_id>.trades._published.json` con la lista de `PublishedTradeList`; al inicio, si el recibo existe y parsea, retornar ese mismo result sin ejecutar `sqcli` (`ExportStatus: "ALREADY_PUBLISHED"`). La key sale del mismo `BuildMinIOPath` que el artefacto, así que es determinística por identidad lógica y **un reintento de Temporal la encuentra** (con una key por `run_id` el recibo sería inútil, porque cada reintento estrenaría una key nueva). Implementar solo si el costo del reintento se vuelve un problema real. |
| R2 | Duplicación lógica entre la activity y los steps `upload_trade_list`/`upsert_trade_list` del pipeline legacy. | **Resuelta borrando los steps** (D11, T2d). Sostener dos implementaciones con una sola convención de naming era invitar a que la copia muerta reviviera con la convención vieja. |
| R6 | Objetos MinIO viejos bajo `waves/wave_*/requests/...` quedan huérfanos tras el cambio de key. | **Aceptado.** Nadie los lee y todos los resultados previos están en cuarentena `unverified` (`§10.8` del padre). Purgarlos en una pasada de mantenimiento con `mc rm --recursive`, fuera de este PR y con evidencia aparte. |
| R7 | Convivencia durante el despliegue: un worker viejo escribiendo la key vieja y uno nuevo la key nueva en la misma wave. | **Mitigado por procedimiento, no por código.** Es el mismo requisito que R5: desplegar los 3 hosts con la misma versión antes de lanzar waves. Al no haber lectores de esas keys todavía (F4 aún no consume trade lists), una mezcla no rompe nada más allá de dejar objetos huérfanos. |
| R3 | El fallo duro por `trade_count == 0` bloqueará una wave si `05_reretester` no entrega órdenes cerradas. | **Intencional.** Es exactamente el comportamiento que `§10.8` del padre exige: fallar ruidosamente en vez de persistir datos falsos. El smoke verifica ese insumo existente. |
| R4 | Sin verificación round-trip (descargar + decodificar) tras subir. | **Aceptado.** El upload ya calcula y compara sha256 sobre el contenido plano y la idempotencia valida el ETag. Re-descargar cada artefacto duplica I/O por un riesgo que el `sha256` del `ref` ya cubre cuando F4 lea el artefacto. |
| R5 | Runs en vuelo con el contrato viejo. | **Sin migración necesaria.** Los workflows en vuelo con el contrato antiguo ya están fallando por el bug (ENOENT en el upsert). Se terminan/reinician; no hay estado parcial que rescatar porque la publicación era todo-o-nada. Sí hay que desplegar los 3 workers con la misma versión antes de lanzar waves nuevas: un worker viejo registrando `act_upsert_trade_list` y uno nuevo sin ella conviviendo en la misma task queue producirían fallos confusos. |

## 🧭 Decisiones

- **D1 — Una sola activity (`trade_list_exporter` = export + publish + register).** Rechazada la opción B (export sube a MinIO y una segunda activity solo hace Mongo): agrega un round-trip y más historia de Temporal sin quitar ningún riesgo, porque el upsert Mongo es una llamada de milisegundos que no necesita aislamiento propio. Rechazada la opción C (reusar el pipeline de 4 steps): acopla el exporter a `TaskSpec`/`project_activity` y no elimina la duplicación, la esconde.
- **D2 — El output solo lleva identificadores remotos.** Invariante verificado por un test de reflexión, no por convención.
- **D3 — N scopes por export.** Iterar todos los `_SUCCESS`, no el primero. El plugin puede emitir FULL/IS/OOS y celdas WFM; quedarse con el primero perdía datos en silencio.
- **D4 — La key MinIO se alinea con el resto del pipeline: `<folder de la task>/<canonical_strategy_id>.trades.ndjson.gz`.** Corrige la decisión anterior de esta misma nota (que defendía mantener `waves/.../requests/<request_id>/runs/<run_id>/.../trades.v1.ndjson.gz`). Razones, en orden de peso:
  1. **Contradice una decisión ya firmada del repo.** `domain.BuildMinIOPath` documenta ser el mecanismo **único** de rutas, determinista por identidad lógica y **sin segmentos de ejecución**, y nombra a `trade_list_exporter` entre los consumidores obligados (decisión `2026-07-31-storage-path-deterministic-by-logical-identity`, EF-G27). `remoteArtifactKey` mete `requests/<request_id>/runs/<run_id>`: es exactamente la clase de bug "path mismatch" que esa decisión eliminó. Mi defensa anterior evaluó costo de migración e ignoró que la regla ya existía.
  2. **La identidad del artefacto es la configuración, no la corrida.** Reexportar la misma estrategia debe sobrescribir el mismo objeto, no crear una key nueva por `run_id`. Con la key vieja, cada reintento de Temporal (que cambia `run_id`) dejaba un objeto huérfano y el consumidor no podía predecir cuál leer.
  3. **Legibilidad y simetría.** Un humano que lista `06_trade_list/` ve los mismos nombres que en `05_reretester/`, con otra extensión. La versión de schema no se pierde: vive en `manifest.schema_version` y en la metadata del objeto (`x-sqx-manifest-version`), que es donde corresponde.
  4. **Costo real de migrar: cero.** `TradeArtifactRef.Validate` solo exige key no vacía, nada parsea la forma de la key, y los objetos/documentos previos ya están en cuarentena `unverified`.
- **D5 — Se mantiene gzip.** Solo cambia el **nombre**, no los bytes. El contrato del SDK (`TradeArtifactContentType`/`Encoding`, sha256 sobre el contenido plano) y el writer Java ya emiten comprimido, y `DownloadNDJSON` descomprime al leer. Pasar a `.ndjson` plano rompería el contrato del SDK e inflaría storage y ancho de banda por un artefacto que nadie edita a mano. Si en algún momento se quiere el plano, es un cambio de una constante en `core/domain` + el encoding del ref, no un rediseño.
- **D6 — Los trades NO van a Mongo.** Mongo guarda manifest + `ref` (índice consultable, un documento por scope); MinIO guarda el NDJSON (bulk inmutable). Motivos: el límite de 16 MB por documento, la amplificación de escritura de miles de trades por estrategia, y que nada en Etapa 4 consulta trades individuales. Si F4 necesita analítica trade a trade, se lee por streaming desde MinIO con `trades.DecodeNDJSON`, que ya existe. Revisar solo si aparece un caso de uso que exija filtrar trades por atributo en el servidor.
- **D7 — Se retira `act_upsert_trade_list`.** Su firma toma un path local: viola el invariante por construcción, no por accidente. Retirarla paga la deuda de aridad (`got 3`) en la raíz. La reconciliación manual se cubre re-ejecutando la task, que es idempotente de punta a punta.
- **D8 — `temporalNonRetryable` usa la API oficial del SDK.** El wrapper propio `nonRetryableTradeError` no tenía efecto real: Temporal solo lo habría respetado si la `RetryPolicy` declarara su nombre en `NonRetryableErrorTypes`, y no lo hace. `NewNonRetryableApplicationError` marca el flag en el propio error, sin depender de la policy.
- **D10 — Solo `databanks/input` y `databanks/output`; se limpian antes y después de cada ejecución.** Corrige la decisión anterior de esta nota (que mantenía un tercer directorio `user/projects/<project>/tradelist`). El argumento que yo daba —"`CleanProjectDatabanks` podría borrar artefactos a mitad de vuelo"— se cae con dos hechos: (a) el worker corre con `MaxConcurrentActivityExecutionSize: 1`, así que no hay dos activities compitiendo por el mismo proyecto; (b) la limpieza es **parte del contrato de la task**, no un accidente: quien limpia es la propia activity al empezar, no un tercero. El problema real era el opuesto: un directorio que nadie limpia acumula artefactos de corridas viejas que un descubrimiento posterior puede confundir con los de la corrida actual —justo la contaminación que hay que evitar—, y obligaba a mantener dos convenciones de ruta para lo mismo (la divergencia verificada entre el step legacy y la activity). Con el par `input`/`output` hay una sola ruta, un solo dueño y un ciclo de vida explícito: limpiar → escribir → publicar → limpiar.
- **D11 — Se borra el pipeline legacy de 4 steps.** Contradice la decisión anterior (R2, "aceptar la duplicación"). Con una sola convención de naming y de directorios, mantener una segunda implementación inalcanzable (requiere `type: project` + `ExporterProject`) significaría sostener dos veces la misma lógica y arriesgar que la copia muerta reviva con la convención vieja. El blast radius es mecánico y acotado: `builder.go`, un `Register` y dos archivos de test. Si algún día se necesita publicar trade lists desde el pipeline, la refactorización correcta es extraer un `trades.Publisher` en `sqx/core/trades/`, no resucitar los steps.
- **D12 — La key la construye el caller; el adapter mueve bytes.** `UploadScopeArtifacts` recibe `artifactKey`. Motivo estructural: la ruta depende de la identidad **de la configuración** (instrument/direction/timeframe/strategy/version/folder), que vive en el `TaskSpec` y en los metadatos de la estrategia, no en el `TradeScope`. Un adapter que inventa rutas necesita que el scope arrastre datos de configuración que no son suyos, o duplica el algoritmo —que es exactamente cómo nacieron `remoteArtifactKey` y `TradeArtifactKeyBuilderImpl`, dos copias divergentes de `BuildMinIOPath`—. Con la key inyectada hay un solo constructor de rutas en todo el sistema y el adapter queda con una sola responsabilidad. Se borran ambas copias y el puerto `TradeArtifactKeyBuilder` (código muerto: su único caller era su test).
- **D13 — Muere el `_SUCCESS` remoto.** Con un archivo por estrategia en la carpeta de la etapa, un `_SUCCESS` por carpeta sería un marcador compartido por las 9 estrategias: no puede afirmar nada sobre ninguna en particular. El registro de completitud por scope es su documento en Mongo, escrito después del upload. El sidecar del manifest **sí** se mantiene (renombrado por estrategia): es barato, autodescribe la carpeta y sirve para inspección manual sin abrir Mongo.
- **D9 — Nada de sticky worker ni task queue por host.** Se descartó explícitamente: resolvería el síntoma atando el pipeline a la topología del cluster y rompería el balanceo entre Zeus/Hera/Kronos.

## 📆 Bitácora

- **2026-08-01 — Contexto histórico de implementación T1–T8.** Activity autosuficiente con key `BuildMinIOPath` + `TradeListArtifactFilename`, databanks `input`/`output` con limpieza, pipeline legacy y `act_upsert_trade_list` retirados, `_SUCCESS` remoto eliminado, `SetSQXExecBasePath` en el worker. Tests: `go test` verde en worker/domain/runtime/storage-minio/workflows/cmd-sqx-worker. Branch `fix/ef-g32-trade-list-remote-contract`, PR https://github.com/xKoRx/symphony/pull/50, badge README → 0.1.2. Tarea puente del padre movida a Review. La lista de bloqueos de esa fecha fue reemplazada: el smoke vigente parte en EF-G30, con EF-G32 desplegado y `05_reretester` como fuente ya configurada.

- **2026-07-31** — Sesión de diseño. Auditado el flujo completo (activity de export, `UpsertTradeList`, wrapper Temporal, ambos bloques del workflow, adapters MinIO/Mongo, pipeline de 4 steps y plugin Java). Confirmado que la task se declara como `type: trade_list_exporter`, así que el pipeline de 4 steps no se ejecuta y el camino real es el `case` del workflow. Aislados 3 defectos adicionales al bug reportado: (1) `scopeFromExportedManifest` devuelve `nil` y el workflow hace `continue`, marcando éxito sin publicar; (2) `findTradeListScopeArtifacts` corta en el primer `_SUCCESS` y descarta scopes; (3) `nonRetryableTradeError` no produce un error non-retryable real para Temporal porque la `RetryPolicy` no lo declara. Diseño cerrado en opción A (activity única) con contrato de salida remoto. Plan T1-T8 escrito para ejecución por agente ligero. Sin cambios de código.

- **2026-07-31 (noche, revisión del owner)** — ⚠️ *Entrada histórica: sus conclusiones sobre naming y databanks quedaron **superadas** por la entrada siguiente. Se conserva por trazabilidad del razonamiento.* El owner preguntó si 9 estrategias se pisarían al compartir el filename `trades.v1.ndjson.gz`. Verificado que no: `strategy_id` es segmento de la key MinIO (`.../strategies/<strategy_id>/...`) y del scope dir local (`<strategyId>___FULL`), así que hay un artefacto por estrategia en prefijos distintos; el filename solo codifica schema y formato. El único escenario de colapso es `strategy_id` vacío, que el `scope.Validate()` previo a la subida ya bloquea. En la misma revisión se descartó una colisión local por concurrencia: el workflow lanza las N activities en paralelo, pero el worker se crea con `MaxConcurrentActivityExecutionSize: 1`, así que se serializan por host y la limpieza del databank/output dir es segura sin locks. Se detectó y sumó a T8 una divergencia real: el step legacy `collect_trade_list` leía `databanks/output/tradelist` mientras la activity escribe en `<project>/tradelist`. Decisión D10 registrada sobre mantener el output fuera de `databanks/`, con opción B de una línea si el owner prefiere lo contrario.

- **2026-07-31 (cierre, corrección de rumbo del owner)** — El owner rechazó de plano ambas decisiones: el artefacto no puede llamarse por la ejecución del flujo (`requests/<request_id>/runs/<run_id>/trades.v1.ndjson.gz`) sino por la estrategia, en la carpeta que declara la config; y los databanks deben ser solo `input`/`output`, porque son los que cada task limpia antes y después para no heredar datos contaminados. Al verificar contra el código, tenía razón en los dos puntos y mi defensa anterior era mala: `sqx/core/domain/paths.go` L8-27 documenta que `BuildMinIOPath` es el **mecanismo único** de rutas, determinista por identidad lógica y **sin segmentos de ejecución**, y nombra explícitamente a `trade_list_exporter` entre los consumidores obligados; `remoteArtifactKey` (y su gemelo muerto `TradeArtifactKeyBuilderImpl`) son dos copias divergentes que violan esa decisión firmada (EF-G27). Sobre los databanks: el riesgo que yo temía (limpieza a mitad de vuelo) no existe con `MaxConcurrentActivityExecutionSize: 1`, y el riesgo real era el que el owner señaló, un directorio que nadie limpia acumulando residuos entre tasks. Cambios en la nota: **D4 y D10 revertidas**, agregadas **D11** (borrar el pipeline legacy de 4 steps, que era el segundo caller de `UploadScopeArtifacts` y la segunda convención de directorios), **D12** (la key la construye el caller; el adapter mueve bytes) y **D13** (muere el `_SUCCESS` remoto, que con un archivo por estrategia sería un marcador ambiguo compartido). Tareas nuevas T2b/T2c/T2d, T3 ampliada al adapter y al ciclo de limpieza, T5 con `SetSQXExecBasePath` para que escribir y limpiar no puedan divergir, T7 con 4 tests nuevos, T8 con barrido de residuos. Verificado además que el cambio de key **no toca el SDK**: `TradeArtifactRef.Validate` solo exige key no vacía. Sin cambios de código todavía.

## 🔗 Docs / Links

- Padre: [[Echo Forge - Cierre de Etapa 4]] — plan canónico de Etapa 4 y orden de remediación.
- Gaps relacionados en `symphony`: `specs/FEAT-SQX-STRATEGY-EVALUATION/G6_HANDOFF.md` §10.4 (EF-G28 extracción), §10.5 (EF-G29 instrumento), §10.6 (EF-G30 `exporter.properties`), §10.7 (EF-G31 release del JAR), §10.8 (orden de remediación y criterio de cierre). Este proyecto es `EF-G32`.
- Spec de la feature: `specs/FEAT-SQX-TRADE-LIST-METADATA/` (`SPEC.md` §4.4 describe la activity que aquí se retira; `PLAN.md`, `TASKS.md`, `G3_HANDOFF.md`).
- Known error previo: [[2026-07-29-sqx-trade-list-exporter-source-order-count-zero]].

## 💡 Ideas

### Backlog de ideas

- **EF-G33** — Recibo de publicación `_PUBLISHED.json` para saltar el export en reintentos (diseño completo en §🚧 R1).
- Si alguna vez se necesita publicar trade lists desde el pipeline de `project`, extraer un `trades.Publisher` en `sqx/core/trades/` con la lógica de `publishScope` y consumirlo desde ahí. Nunca resucitar los steps borrados en T2d.
- Purga de los objetos MinIO huérfanos de la convención vieja (`waves/wave_*/requests/...`), con inventario previo y evidencia. Ver R6.
- Métrica de negocio `trading.sqx.trade_lists_published` con atributos `wave`/`stage`/`sample_type` vía `SQXMetrics`, para ver cobertura de trade lists por wave sin consultar Mongo.

### Motivos / principios

- Un contrato entre activities de Temporal solo puede referir estado alcanzable desde cualquier worker. El filesystem local es privado de la activity, siempre.
- Fallar ruidosamente vale más que registrar un éxito vacío: un skip silencioso convierte un bug en datos falsos, que es estrictamente peor.
- Idempotencia en cada borde (MinIO por sha256, Mongo por clave natural) es lo que permite que la unidad de retry sea gruesa sin corromper estado.

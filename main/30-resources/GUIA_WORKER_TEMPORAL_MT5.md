---
type: doc
schema_version: 1
status: active
area: "[[Echo Forge]]"
related: []
aliases: []
tags:
  - kind/doc
created: 2026-08-10
updated: 2026-08-10
---

# Guía de implementación: worker Temporal para backtesting MT5

## Propósito

Documentación canónica legacy de [[Echo Forge]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


## 1. Objetivo

Implementar en el worker existente de Echo Forge un nuevo tipo de tarea llamado `mt5`.

Hasta ahora, las tareas procesadas por el worker pueden considerarse de tipo `sqx`. El nuevo tipo `mt5` debe ejecutar backtests automatizados en MetaTrader 5 usando una instalación disponible en:

```text
C:\mt5\backtesting
```

El flujo general será:

```text
Workflow Echo Forge
    ↓
Tarea type=mt5
    ↓
Worker Temporal en Go
    ↓
Preparar EA + parámetros + configuración
    ↓
Ejecutar MetaTrader 5 Strategy Tester
    ↓
Esperar finalización
    ↓
Extraer y normalizar resultados
    ↓
Persistir resultado MT5 en MongoDB
    ↓
Comparar posteriormente MT5 vs SQX
```

El primer alcance es exclusivamente **backtesting MT5**. La administración de cuentas reales, múltiples terminales y NinjaTrader debe quedar fuera de esta primera implementación, aunque el diseño no debe bloquear esas extensiones futuras.

---

## 2. Alcance inicial

El nuevo worker o handler `mt5` debe ser capaz de:

1. Recibir una tarea Temporal de tipo `mt5`.
2. Validar su configuración.
3. Tomar un EA compilado de MetaTrader 5.
4. Aplicar parámetros dinámicos según cada caso.
5. Crear una ejecución aislada dentro de un workspace por job.
6. Ejecutar el Strategy Tester de MT5 usando la instalación de:

   ```text
   C:\mt5\backtesting
   ```

7. Esperar el término del proceso.
8. Detectar errores, timeout o cancelación.
9. Obtener:
   - reporte del Strategy Tester;
   - logs del terminal;
   - logs del tester;
   - configuración efectiva;
   - parámetros efectivos.
10. Parsear y normalizar las métricas relevantes.
11. Insertar el resultado en MongoDB.
12. Dejar el registro asociado a la estrategia o ejecución SQX original.
13. Permitir una comparación posterior entre métricas SQX y métricas MT5.

---

## 3. Fuera de alcance inicial

No implementar todavía:

- operación en cuentas reales;
- login automatizado a brokers;
- múltiples cuentas MT5;
- administración de varias instalaciones MT5;
- ejecución de EAs en gráficos live;
- optimización genética;
- agentes remotos o MQL5 Cloud Network;
- NinjaTrader;
- backtesting NinjaTrader;
- comparación automática o decisión final de aceptación;
- modificación del código fuente `.mq5`;
- compilación automática de `.mq5`.

La primera versión debe trabajar con un EA ya compilado, normalmente un archivo:

```text
.ex5
```

> MetaTrader 5 no utiliza normalmente `.mt5` como extensión de EA. El ejecutable compilado esperado es `.ex5`, el código fuente es `.mq5` y los parámetros suelen guardarse en `.set`.

---

## 4. Principios de diseño

### 4.1. Separar tarea, ejecución e infraestructura

No representar todo como una única entidad.

```text
MT5Task
    definición solicitada por el workflow

MT5Execution
    intento concreto de ejecutar la tarea

MT5Runtime
    instalación y proceso de MetaTrader 5

MT5Result
    resultado normalizado del backtest
```

Una tarea puede tener varios intentos por retry. Cada intento debe producir una ejecución identificable y auditable.

### 4.2. Idempotencia

Temporal puede reintentar activities. Por eso:

- no insertar resultados duplicados;
- no ejecutar dos veces el mismo backtest si ya terminó correctamente;
- usar identificadores deterministas;
- verificar el estado previo antes de iniciar;
- hacer upsert en MongoDB;
- conservar el número de intento de Temporal.

Una clave lógica sugerida:

```text
workflow_id + task_id + strategy_id + mt5_config_hash
```

### 4.3. Reproducibilidad

Cada resultado debe guardar exactamente:

- EA utilizado;
- hash SHA-256 del `.ex5`;
- parámetros utilizados;
- configuración del tester;
- rango de fechas;
- símbolo;
- timeframe;
- modelo de ticks;
- balance inicial;
- moneda;
- leverage;
- build de MT5;
- timestamps;
- versión del worker;
- logs y reporte producidos.

El objetivo no es solamente obtener un número. Debe ser posible explicar cómo se obtuvo.

### 4.4. Aislamiento por job

Aunque inicialmente exista una sola instalación MT5, cada job debe tener su propio workspace:

```text
C:\mt5\jobs\<execution-id>\
```

Nunca reutilizar directamente reportes, `.ini` o `.set` entre dos ejecuciones.

### 4.5. Una ejecución MT5 simultánea por instalación

Para la primera versión, usar un lock exclusivo para:

```text
C:\mt5\backtesting
```

Esto evita que dos activities lancen el mismo `terminal64.exe` al mismo tiempo y se pisen:

- perfiles;
- tester;
- archivos;
- reportes;
- historial;
- procesos.

Más adelante se podrá crear un pool de instalaciones MT5 independientes.

---

## 5. Organización propuesta del código

Ejemplo adaptable al repositorio actual:

```text
internal/
├── tasks/
│   ├── sqx/
│   └── mt5/
│       ├── handler.go
│       ├── validation.go
│       ├── models.go
│       └── errors.go
│
├── temporal/
│   ├── workflows/
│   │   └── mt5_backtest_workflow.go
│   └── activities/
│       └── mt5/
│           ├── prepare.go
│           ├── execute.go
│           ├── collect.go
│           ├── parse.go
│           └── persist.go
│
├── mt5/
│   ├── runtime.go
│   ├── process_windows.go
│   ├── config_ini.go
│   ├── parameters_set.go
│   ├── report_parser.go
│   ├── log_parser.go
│   ├── workspace.go
│   └── lock.go
│
├── persistence/
│   └── mongo/
│       ├── mt5_execution_repository.go
│       └── mt5_result_repository.go
│
└── domain/
    ├── backtest.go
    ├── strategy.go
    └── metrics.go
```

No es obligatorio copiar esta estructura literalmente. La regla importante es evitar que:

- el workflow conozca detalles de archivos MT5;
- el parser conozca Temporal;
- el repositorio Mongo lance procesos;
- el handler `sqx` acumule condiciones especiales para MT5.

---

## 6. Registro de tipos de tarea

Evitar una cadena grande de `if` o `switch` repartida por el código.

Definir un tipo explícito:

```go
type TaskType string

const (
    TaskTypeSQX TaskType = "sqx"
    TaskTypeMT5 TaskType = "mt5"
)
```

Definir un contrato común:

```go
type TaskHandler interface {
    Type() TaskType
    Validate(ctx context.Context, task Task) error
    Execute(ctx context.Context, task Task) error
}
```

Registro:

```go
type HandlerRegistry struct {
    handlers map[TaskType]TaskHandler
}

func (r *HandlerRegistry) Register(handler TaskHandler) {
    r.handlers[handler.Type()] = handler
}

func (r *HandlerRegistry) Get(taskType TaskType) (TaskHandler, bool) {
    handler, ok := r.handlers[taskType]
    return handler, ok
}
```

De este modo, el worker puede atender:

```text
sqx
mt5
```

sin contaminar las implementaciones entre sí.

---

## 7. Contrato de la tarea MT5

La tarea debe usar un contrato explícito y versionado.

```go
type MT5BacktestTask struct {
    SchemaVersion string `json:"schema_version" bson:"schema_version"`

    TaskID       string `json:"task_id" bson:"task_id"`
    WorkflowID   string `json:"workflow_id" bson:"workflow_id"`
    StrategyID   string `json:"strategy_id" bson:"strategy_id"`
    SQXResultID  string `json:"sqx_result_id,omitempty" bson:"sqx_result_id,omitempty"`

    EA            MT5EAConfig      `json:"ea" bson:"ea"`
    Market        MT5MarketConfig  `json:"market" bson:"market"`
    Tester        MT5TesterConfig  `json:"tester" bson:"tester"`
    Runtime       MT5RuntimeConfig `json:"runtime" bson:"runtime"`
    Correlation   CorrelationData  `json:"correlation" bson:"correlation"`
}
```

### 7.1. Configuración del EA

```go
type MT5EAConfig struct {
    Name          string                 `json:"name" bson:"name"`
    ArtifactPath  string                 `json:"artifact_path" bson:"artifact_path"`
    ArtifactHash  string                 `json:"artifact_hash,omitempty" bson:"artifact_hash,omitempty"`
    Parameters    map[string]any         `json:"parameters" bson:"parameters"`
    BaseSetPath   string                 `json:"base_set_path,omitempty" bson:"base_set_path,omitempty"`
}
```

Ejemplo:

```json
{
  "name": "EchoStrategy",
  "artifact_path": "C:\\echo\\artifacts\\EchoStrategy.ex5",
  "parameters": {
    "RiskPercent": 1.0,
    "ATRPeriod": 14,
    "EntryPeriod": 20,
    "ExitPeriod": 10
  }
}
```

### 7.2. Configuración de mercado

```go
type MT5MarketConfig struct {
    Symbol    string    `json:"symbol" bson:"symbol"`
    Timeframe string    `json:"timeframe" bson:"timeframe"`
    From      time.Time `json:"from" bson:"from"`
    To        time.Time `json:"to" bson:"to"`
}
```

Ejemplo:

```json
{
  "symbol": "EURUSD",
  "timeframe": "H1",
  "from": "2024-01-01T00:00:00Z",
  "to": "2025-12-31T23:59:59Z"
}
```

### 7.3. Configuración del tester

```go
type MT5TesterConfig struct {
    Model             int     `json:"model" bson:"model"`
    ExecutionMode     int     `json:"execution_mode" bson:"execution_mode"`
    Optimization      bool    `json:"optimization" bson:"optimization"`
    Deposit           float64 `json:"deposit" bson:"deposit"`
    Currency          string  `json:"currency" bson:"currency"`
    Leverage          string  `json:"leverage" bson:"leverage"`
    Visual            bool    `json:"visual" bson:"visual"`
}
```

Para el primer alcance:

```text
Optimization = false
Visual = false
UseLocal = true
UseRemote = false
UseCloud = false
```

### 7.4. Configuración de runtime

```go
type MT5RuntimeConfig struct {
    InstallationPath string        `json:"installation_path" bson:"installation_path"`
    Timeout          time.Duration `json:"timeout" bson:"timeout"`
    KeepWorkspace    bool          `json:"keep_workspace" bson:"keep_workspace"`
}
```

Valor por defecto:

```text
InstallationPath = C:\mt5\backtesting
```

No confiar ciegamente en una ruta enviada por la tarea. El worker debe usar una allowlist o configuración local.

---

## 8. Ejemplo completo de tarea

```yaml
schema_version: "1"

task_id: "mt5-bt-000042"
workflow_id: "sqx-main-00-configs-v5"
strategy_id: "strategy-73920"
sqx_result_id: "sqx-result-91823"

ea:
  name: "EchoStrategy"
  artifact_path: "C:\\echo\\artifacts\\EchoStrategy.ex5"
  base_set_path: "C:\\echo\\artifacts\\EchoStrategy.base.set"
  parameters:
    RiskPercent: 1.0
    ATRPeriod: 14
    EntryPeriod: 20
    ExitPeriod: 10

market:
  symbol: "EURUSD"
  timeframe: "H1"
  from: "2024-01-01T00:00:00Z"
  to: "2025-12-31T23:59:59Z"

tester:
  model: 4
  execution_mode: 0
  optimization: false
  deposit: 10000
  currency: "USD"
  leverage: "1:100"
  visual: false

runtime:
  installation_path: "C:\\mt5\\backtesting"
  timeout: "2h"
  keep_workspace: true

correlation:
  pipeline_id: "echo-forge-e2e-001"
  group_id: "NDX-H1-L"
  source: "sqx"
```

---

## 9. Workflow Temporal propuesto

El workflow no debe ejecutar operaciones de filesystem o procesos directamente.

```text
MT5BacktestWorkflow
├── ValidateMT5Task
├── ReserveMT5Runtime
├── PrepareMT5Workspace
├── ExecuteMT5Backtest
├── CollectMT5Artifacts
├── ParseMT5Result
├── PersistMT5Result
└── ReleaseMT5Runtime
```

### 9.1. Activity options sugeridas

Las activities deben tener políticas diferentes.

#### Preparación

- `StartToCloseTimeout`: corto;
- retries habilitados;
- idempotente.

#### Ejecución del backtest

- timeout según tarea;
- heartbeat frecuente;
- cancelación soportada;
- retry limitado;
- no relanzar sin comprobar estado previo.

#### Parsing y persistencia

- retries habilitados;
- idempotentes;
- sin dependencia del proceso MT5 una vez recolectados los artifacts.

Ejemplo conceptual:

```go
executionOptions := workflow.ActivityOptions{
    StartToCloseTimeout: task.Runtime.Timeout + 5*time.Minute,
    HeartbeatTimeout:    30 * time.Second,
    RetryPolicy: &temporal.RetryPolicy{
        MaximumAttempts: 2,
    },
}
```

No usar `MaximumAttempts` alto para lanzar MetaTrader una y otra vez sin control.

---

## 10. Activities sugeridas

### 10.1. `ValidateMT5Task`

Debe validar:

- tipo `mt5`;
- versión soportada del schema;
- IDs obligatorios;
- existencia del `.ex5`;
- extensión `.ex5`;
- existencia opcional del `.set` base;
- fechas válidas;
- `from < to`;
- símbolo no vacío;
- timeframe permitido;
- balance mayor que cero;
- moneda válida;
- leverage válido;
- timeout razonable;
- ruta de instalación permitida;
- parámetros serializables;
- ausencia de rutas fuera de allowlist.

Errores de validación deben ser no reintentables.

### 10.2. `ReserveMT5Runtime`

Debe adquirir un lock exclusivo para la instalación.

Opciones:

- mutex de proceso, sólo si existe un único worker;
- lock file con ownership;
- lock distribuido en MongoDB;
- lock distribuido mediante Temporal;
- semaphore en el workflow.

Recomendación inicial: lock persistente o lease con TTL asociado a:

```text
runtime_id = mt5-backtesting-default
```

Debe guardar:

```text
owner_workflow_id
owner_run_id
execution_id
lease_expires_at
heartbeat_at
```

### 10.3. `PrepareMT5Workspace`

Crear:

```text
C:\mt5\jobs\<execution-id>\
├── input\
├── output\
├── logs\
└── metadata\
```

Ejemplo:

```text
C:\mt5\jobs\mt5-bt-000042-attempt-1\
├── input\
│   ├── EchoStrategy.ex5
│   ├── parameters.set
│   └── tester.ini
├── output\
│   └── report.htm
├── logs\
└── metadata\
    ├── task.json
    ├── execution.json
    └── checksums.json
```

También debe:

1. calcular hash del `.ex5`;
2. copiar o verificar el artifact;
3. generar parámetros efectivos;
4. generar `tester.ini`;
5. guardar una copia de la tarea;
6. registrar la ejecución como `PREPARING`.

### 10.4. `ExecuteMT5Backtest`

Debe:

1. confirmar lock;
2. verificar que no exista otro proceso MT5 de la misma instalación;
3. instalar/copiar el EA en el lugar esperado;
4. instalar/copiar el `.set`;
5. ejecutar:

   ```text
   C:\mt5\backtesting\terminal64.exe
   ```

5. usar modo portable si la instalación está preparada para ello;
6. pasar la configuración generada;
7. registrar PID y timestamp;
8. enviar heartbeats;
9. soportar cancelación;
10. aplicar timeout;
11. esperar cierre;
12. comprobar existencia del reporte;
13. guardar exit code y estado final.

Comando conceptual:

```powershell
C:\mt5\backtesting\terminal64.exe `
  /portable `
  /config:C:\mt5\jobs\<execution-id>\input\tester.ini
```

En Go:

```go
cmd := exec.CommandContext(
    ctx,
    terminalPath,
    "/portable",
    "/config:"+configPath,
)

cmd.Dir = installationPath
```

No asumir que `stdout` contiene los logs importantes de MT5. La mayor parte estará en archivos propios del terminal y del tester.

### 10.5. `CollectMT5Artifacts`

Debe localizar y copiar al workspace:

- reporte;
- journal del terminal;
- logs del tester;
- configuración;
- `.set`;
- hashes;
- metadata del proceso.

La resolución de rutas debe encapsularse en una implementación por build o layout de MT5. No repartir rutas mágicas por el código.

### 10.6. `ParseMT5Result`

Debe transformar los datos de MT5 a un modelo canónico.

No guardar solamente HTML crudo. El HTML sirve como evidencia, pero la comparación debe usar campos estructurados.

### 10.7. `PersistMT5Result`

Debe hacer upsert idempotente en MongoDB.

Después de persistir correctamente:

- marcar la ejecución `SUCCEEDED`;
- relacionarla con `strategy_id`;
- relacionarla con `sqx_result_id`;
- guardar el hash de configuración;
- guardar referencias a artifacts.

### 10.8. `ReleaseMT5Runtime`

Debe ejecutarse incluso ante fallos.

Responsabilidades:

- cerrar procesos residuales;
- liberar lock;
- actualizar lease;
- dejar el runtime disponible;
- marcar workspace para retención o limpieza.

Usar un bloque equivalente a `defer` mediante manejo explícito de errores en workflow.

---

## 11. Preparación del EA

La instalación esperada:

```text
C:\mt5\backtesting
```

En modo portable, el EA normalmente debe quedar bajo una estructura equivalente a:

```text
C:\mt5\backtesting\MQL5\Experts\Echo\EchoStrategy.ex5
```

Los parámetros de tester:

```text
C:\mt5\backtesting\MQL5\Profiles\Tester\<execution-id>.set
```

No sobrescribir un archivo compartido como:

```text
EchoStrategy.set
```

Usar un nombre específico por ejecución.

Ejemplo:

```text
mt5-bt-000042-attempt-1.set
```

---

## 12. Generación de parámetros `.set`

### 12.1. Recomendación

Mantener un `.set` base generado por MetaTrader para cada versión del EA.

Flujo:

```text
base.set
    ↓
leer
    ↓
reemplazar parámetros permitidos
    ↓
validar parámetros desconocidos
    ↓
guardar execution-id.set
```

### 12.2. Reglas

- rechazar parámetros desconocidos;
- preservar el formato esperado;
- no convertir silenciosamente tipos;
- registrar valores efectivos;
- soportar `int`, `float`, `bool`, `string` y enums;
- usar formato decimal independiente del locale;
- no modificar el archivo base;
- calcular hash del archivo final.

### 12.3. Validación de schema de parámetros

Idealmente definir metadata por EA:

```yaml
ea: EchoStrategy
version: "4.2.0"

parameters:
  RiskPercent:
    type: float
    min: 0.1
    max: 5.0

  ATRPeriod:
    type: int
    min: 2
    max: 200

  UseBreakEven:
    type: bool
```

Así el worker no se limita a reemplazar texto a ciegas.

---

## 13. Generación de `tester.ini`

Ejemplo base:

```ini
[Tester]
Expert=Echo\EchoStrategy
ExpertParameters=mt5-bt-000042-attempt-1.set

Symbol=EURUSD
Period=H1

Model=4
ExecutionMode=0
Optimization=0

FromDate=2024.01.01
ToDate=2025.12.31

Deposit=10000
Currency=USD
Leverage=1:100

Report=C:\mt5\jobs\mt5-bt-000042-attempt-1\output\report
ReplaceReport=1
ShutdownTerminal=1

Visual=0
UseLocal=1
UseRemote=0
UseCloud=0
```

### Reglas

- usar rutas absolutas para outputs;
- `ReplaceReport=1`;
- `ShutdownTerminal=1`;
- `Visual=0`;
- optimización deshabilitada inicialmente;
- agentes remotos y cloud deshabilitados;
- fechas con formato MT5;
- el nombre de `Expert` debe coincidir con la ruta dentro de `MQL5\Experts`;
- escapar correctamente backslashes;
- guardar el archivo exacto usado.

---

## 14. Manejo del proceso MT5

### 14.1. Estados

```text
CREATED
PREPARING
STARTING
RUNNING
COLLECTING
SUCCEEDED
FAILED
CANCELED
TIMED_OUT
```

### 14.2. Cancelación

Cuando Temporal cancele la activity:

1. marcar ejecución como `CANCEL_REQUESTED`;
2. intentar cierre normal;
3. esperar un grace period;
4. terminar el proceso;
5. terminar hijos si corresponde;
6. recolectar logs parciales;
7. persistir estado `CANCELED`.

### 14.3. Timeout

Cuando exceda el tiempo:

1. marcar `TIMED_OUT`;
2. terminar proceso;
3. guardar logs;
4. liberar runtime;
5. devolver error tipado.

### 14.4. Procesos huérfanos

Antes de iniciar:

- buscar un proceso asociado a la instalación;
- validar executable path;
- validar start time;
- no matar otros terminales MT5 del sistema por nombre solamente.

No ejecutar indiscriminadamente:

```powershell
taskkill /IM terminal64.exe /F
```

Eso podría matar terminales ajenos.

Idealmente usar Windows Job Objects o mantener un process handle administrado por el agente.

---

## 15. Extracción de resultados

El parser debe aceptar el reporte de MT5 y producir un modelo normalizado.

### 15.1. Métricas mínimas

```go
type BacktestMetrics struct {
    InitialDeposit        float64 `bson:"initial_deposit" json:"initial_deposit"`
    NetProfit             float64 `bson:"net_profit" json:"net_profit"`
    GrossProfit           float64 `bson:"gross_profit" json:"gross_profit"`
    GrossLoss             float64 `bson:"gross_loss" json:"gross_loss"`
    ProfitFactor          float64 `bson:"profit_factor" json:"profit_factor"`
    ExpectedPayoff        float64 `bson:"expected_payoff" json:"expected_payoff"`
    AbsoluteDrawdown      float64 `bson:"absolute_drawdown" json:"absolute_drawdown"`
    MaximalDrawdown       float64 `bson:"maximal_drawdown" json:"maximal_drawdown"`
    MaximalDrawdownPct    float64 `bson:"maximal_drawdown_pct" json:"maximal_drawdown_pct"`
    RelativeDrawdownPct   float64 `bson:"relative_drawdown_pct" json:"relative_drawdown_pct"`
    TotalTrades           int64   `bson:"total_trades" json:"total_trades"`
    WinningTrades         int64   `bson:"winning_trades" json:"winning_trades"`
    LosingTrades          int64   `bson:"losing_trades" json:"losing_trades"`
    WinRatePct            float64 `bson:"win_rate_pct" json:"win_rate_pct"`
    LossRatePct           float64 `bson:"loss_rate_pct" json:"loss_rate_pct"`
    LargestProfitTrade    float64 `bson:"largest_profit_trade" json:"largest_profit_trade"`
    LargestLossTrade      float64 `bson:"largest_loss_trade" json:"largest_loss_trade"`
    AverageProfitTrade    float64 `bson:"average_profit_trade" json:"average_profit_trade"`
    AverageLossTrade      float64 `bson:"average_loss_trade" json:"average_loss_trade"`
    MaximumConsecutiveWin float64 `bson:"maximum_consecutive_win" json:"maximum_consecutive_win"`
    MaximumConsecutiveLoss float64 `bson:"maximum_consecutive_loss" json:"maximum_consecutive_loss"`
    SharpeRatio           float64 `bson:"sharpe_ratio" json:"sharpe_ratio"`
    RecoveryFactor        float64 `bson:"recovery_factor" json:"recovery_factor"`
}
```

Agregar métricas disponibles y necesarias en el pipeline real.

### 15.2. Datos de contexto

También guardar:

```go
type BacktestContext struct {
    Platform       string    `bson:"platform" json:"platform"`
    PlatformBuild  string    `bson:"platform_build" json:"platform_build"`
    Symbol         string    `bson:"symbol" json:"symbol"`
    Timeframe      string    `bson:"timeframe" json:"timeframe"`
    From           time.Time `bson:"from" json:"from"`
    To             time.Time `bson:"to" json:"to"`
    TickModel      int       `bson:"tick_model" json:"tick_model"`
    Deposit        float64   `bson:"deposit" json:"deposit"`
    Currency       string    `bson:"currency" json:"currency"`
    Leverage       string    `bson:"leverage" json:"leverage"`
    EAName         string    `bson:"ea_name" json:"ea_name"`
    EAHash         string    `bson:"ea_hash" json:"ea_hash"`
    ParametersHash string    `bson:"parameters_hash" json:"parameters_hash"`
    ConfigHash     string    `bson:"config_hash" json:"config_hash"`
}
```

---

## 16. Modelo MongoDB propuesto

Puede usarse una sola colección o separar ejecución y resultado.

Recomendación:

```text
mt5_backtest_executions
mt5_backtest_results
```

### 16.1. `mt5_backtest_executions`

Guarda estado operacional:

```json
{
  "_id": "mt5-bt-000042-attempt-1",
  "task_id": "mt5-bt-000042",
  "workflow_id": "sqx-main-00-configs-v5",
  "temporal_run_id": "temporal-run-id",
  "attempt": 1,

  "strategy_id": "strategy-73920",
  "sqx_result_id": "sqx-result-91823",

  "status": "SUCCEEDED",

  "runtime": {
    "installation_path": "C:\\mt5\\backtesting",
    "workspace": "C:\\mt5\\jobs\\mt5-bt-000042-attempt-1",
    "pid": 1234
  },

  "started_at": "2026-08-06T18:00:00Z",
  "finished_at": "2026-08-06T18:12:30Z",

  "error": null,

  "artifacts": {
    "report_path": "C:\\mt5\\jobs\\mt5-bt-000042-attempt-1\\output\\report.htm",
    "tester_log_path": "...",
    "terminal_log_path": "..."
  }
}
```

### 16.2. `mt5_backtest_results`

Guarda resultado de dominio:

```json
{
  "_id": "mt5-result-000042",

  "execution_id": "mt5-bt-000042-attempt-1",
  "task_id": "mt5-bt-000042",
  "workflow_id": "sqx-main-00-configs-v5",

  "strategy_id": "strategy-73920",
  "sqx_result_id": "sqx-result-91823",

  "platform": "mt5",
  "schema_version": "1",

  "context": {
    "symbol": "EURUSD",
    "timeframe": "H1",
    "from": "2024-01-01T00:00:00Z",
    "to": "2025-12-31T23:59:59Z",
    "tick_model": 4,
    "deposit": 10000,
    "currency": "USD",
    "leverage": "1:100",
    "ea_name": "EchoStrategy",
    "ea_hash": "sha256:...",
    "parameters_hash": "sha256:...",
    "config_hash": "sha256:..."
  },

  "parameters": {
    "RiskPercent": 1.0,
    "ATRPeriod": 14,
    "EntryPeriod": 20,
    "ExitPeriod": 10
  },

  "metrics": {
    "net_profit": 3240.15,
    "profit_factor": 1.72,
    "maximal_drawdown_pct": 8.41,
    "total_trades": 382,
    "winning_trades": 214,
    "losing_trades": 168,
    "win_rate_pct": 56.02,
    "sharpe_ratio": 1.31,
    "recovery_factor": 2.89
  },

  "raw": {
    "report_format": "html",
    "report_hash": "sha256:..."
  },

  "created_at": "2026-08-06T18:12:31Z"
}
```

---

## 17. Índices MongoDB

Índices sugeridos:

```javascript
db.mt5_backtest_executions.createIndex(
  { execution_id: 1 },
  { unique: true }
)

db.mt5_backtest_executions.createIndex(
  { workflow_id: 1, task_id: 1, attempt: 1 },
  { unique: true }
)

db.mt5_backtest_results.createIndex(
  { execution_id: 1 },
  { unique: true }
)

db.mt5_backtest_results.createIndex(
  { strategy_id: 1, sqx_result_id: 1 }
)

db.mt5_backtest_results.createIndex(
  { strategy_id: 1, "context.config_hash": 1 },
  { unique: true }
)

db.mt5_backtest_results.createIndex(
  { workflow_id: 1, created_at: -1 }
)
```

El índice único final depende de si se permiten reejecuciones intencionales con exactamente la misma configuración.

---

## 18. Comparación MT5 vs SQX

El resultado MT5 debe vincularse a la estrategia SQX original:

```text
strategy_id
sqx_result_id
workflow_id
group_id
```

No comparar directamente nombres de campos de ambas plataformas. Crear un modelo canónico.

### 18.1. Modelo común

```go
type CanonicalBacktestResult struct {
    Platform   string
    StrategyID string
    Metrics    CanonicalMetrics
    Context    CanonicalContext
}
```

### 18.2. Métricas comparables

Ejemplo inicial:

| Métrica canónica | SQX | MT5 |
|---|---|---|
| `net_profit` | resultado SQX | Total Net Profit |
| `profit_factor` | Profit Factor | Profit Factor |
| `max_drawdown_pct` | Max DD % | Relative/Max Drawdown % |
| `total_trades` | Number of Trades | Total Trades |
| `win_rate_pct` | Winning % | Profit Trades % |
| `average_trade` | Avg Trade | Expected Payoff |
| `sharpe_ratio` | Sharpe | Sharpe Ratio |
| `recovery_factor` | Ret/DD u homólogo | Recovery Factor |

### 18.3. No asumir equivalencia perfecta

SQX y MT5 pueden diferir por:

- datos históricos;
- timezone;
- zona horaria del broker;
- spread;
- comisión;
- swap;
- especificación del símbolo;
- tamaño de contrato;
- digits;
- lote mínimo;
- step de volumen;
- ejecución intrabar;
- modelo de ticks;
- slippage;
- reglas del EA;
- interpretación del timeframe;
- rounding.

Por eso la comparación debe guardar también el contexto de ejecución.

### 18.4. Resultado de comparación futuro

```go
type BacktestComparison struct {
    StrategyID string

    SQXResultID string
    MT5ResultID string

    MetricDeltas map[string]MetricDelta

    Comparable bool
    Warnings   []string
}
```

Ejemplo:

```json
{
  "metric_deltas": {
    "net_profit": {
      "sqx": 3500.0,
      "mt5": 3240.15,
      "absolute_delta": -259.85,
      "relative_delta_pct": -7.42
    },
    "profit_factor": {
      "sqx": 1.81,
      "mt5": 1.72,
      "absolute_delta": -0.09,
      "relative_delta_pct": -4.97
    }
  }
}
```

---

## 19. Hash de configuración

Calcular un hash determinista usando:

- hash del EA;
- parámetros ordenados;
- símbolo;
- timeframe;
- fechas;
- modelo;
- depósito;
- moneda;
- leverage;
- configuración relevante del tester.

Ejemplo:

```go
type MT5ConfigFingerprint struct {
    EAHash        string
    Parameters    map[string]any
    Symbol        string
    Timeframe     string
    From          time.Time
    To            time.Time
    Model         int
    Deposit       float64
    Currency      string
    Leverage      string
}
```

Serializar de manera canónica antes del SHA-256. No calcular hash sobre un `map` sin ordenar.

Uso:

- idempotencia;
- detección de duplicados;
- auditoría;
- caché futura;
- comparación de reejecuciones.

---

## 20. Errores tipados

Definir errores de dominio:

```go
type ErrorCode string

const (
    ErrInvalidTask          ErrorCode = "INVALID_TASK"
    ErrEAArtifactNotFound   ErrorCode = "EA_ARTIFACT_NOT_FOUND"
    ErrInvalidParameter     ErrorCode = "INVALID_PARAMETER"
    ErrRuntimeBusy          ErrorCode = "RUNTIME_BUSY"
    ErrMT5NotFound          ErrorCode = "MT5_NOT_FOUND"
    ErrMT5StartFailed       ErrorCode = "MT5_START_FAILED"
    ErrMT5UnexpectedExit    ErrorCode = "MT5_UNEXPECTED_EXIT"
    ErrMT5Timeout           ErrorCode = "MT5_TIMEOUT"
    ErrMT5Canceled          ErrorCode = "MT5_CANCELED"
    ErrReportNotFound       ErrorCode = "REPORT_NOT_FOUND"
    ErrReportParseFailed    ErrorCode = "REPORT_PARSE_FAILED"
    ErrMongoPersistFailed   ErrorCode = "MONGO_PERSIST_FAILED"
)
```

Cada error debe indicar:

- código;
- mensaje;
- retryable;
- execution ID;
- activity;
- causa;
- metadata segura.

No incluir secrets ni contenido completo de archivos en logs.

---

## 21. Observabilidad

### 21.1. Logs estructurados

Campos mínimos:

```text
workflow_id
temporal_run_id
task_id
execution_id
strategy_id
sqx_result_id
activity
attempt
runtime_id
mt5_pid
symbol
timeframe
status
duration_ms
error_code
```

### 21.2. Métricas

```text
echo_mt5_backtest_total
echo_mt5_backtest_success_total
echo_mt5_backtest_failure_total
echo_mt5_backtest_duration_seconds
echo_mt5_runtime_busy_total
echo_mt5_report_parse_failure_total
echo_mt5_mongo_persist_failure_total
echo_mt5_orphan_process_total
```

### 21.3. Trazas

Crear spans para:

```text
mt5.validate
mt5.reserve_runtime
mt5.prepare_workspace
mt5.execute
mt5.collect
mt5.parse
mt5.persist
mt5.release_runtime
```

Propagar el contexto OpenTelemetry desde Temporal cuando sea posible.

---

## 22. Seguridad

- permitir solamente rutas configuradas;
- no aceptar ejecutables arbitrarios;
- verificar extensión `.ex5`;
- idealmente verificar hash esperado;
- usar ACL en workspaces;
- no ejecutar como administrador salvo necesidad real;
- no aceptar argumentos CLI arbitrarios desde la tarea;
- escapar todas las rutas;
- validar nombres de archivos;
- impedir path traversal;
- no guardar credenciales;
- no habilitar DLL imports por defecto;
- no habilitar trading real en la instancia de backtesting;
- mantener la instancia aislada de cuentas live.

---

## 23. Limpieza y retención

### En éxito

Conservar al menos:

- tarea;
- configuración;
- parámetros;
- reporte;
- logs;
- resultado parseado;
- hashes.

### En fallo

Conservar especialmente:

- logs;
- configuración;
- parámetros;
- estado del proceso;
- reason del fallo.

### Política sugerida

- workspace local exitoso: 7 días;
- workspace local fallido: 14–30 días;
- artifacts importantes: almacenamiento persistente;
- MongoDB: metadata permanente según política del proyecto.

No borrar inmediatamente los artifacts al terminar. Los primeros meses se necesitarán para depurar diferencias SQX vs MT5.

---

## 24. Configuración local del worker

Ejemplo:

```yaml
workers:
  mt5:
    enabled: true
    task_queue: "echo-mt5-backtesting"

    runtime:
      id: "mt5-backtesting-default"
      installation_path: "C:\\mt5\\backtesting"
      terminal_path: "C:\\mt5\\backtesting\\terminal64.exe"
      jobs_path: "C:\\mt5\\jobs"
      portable: true
      max_concurrency: 1

    execution:
      default_timeout: "2h"
      shutdown_grace_period: "30s"
      heartbeat_interval: "10s"

    artifacts:
      keep_workspace_on_success: true
      keep_workspace_on_failure: true

    mongo:
      database: "echo_forge"
      executions_collection: "mt5_backtest_executions"
      results_collection: "mt5_backtest_results"
```

### Task Queue

Recomendación inicial:

```text
echo-mt5-backtesting
```

Separarla de SQX permite:

- worker sólo en Windows;
- concurrencia independiente;
- despliegue independiente;
- límites distintos;
- observabilidad más limpia.

El workflow principal puede despachar la tarea MT5 a esa task queue.

---

## 25. Concurrencia

Primera versión:

```text
max_concurrency = 1
```

Razones:

- una instalación;
- un Strategy Tester;
- un directorio de datos;
- menor riesgo de corrupción;
- troubleshooting simple.

Más adelante:

```text
C:\mt5\instances\bt-01
C:\mt5\instances\bt-02
C:\mt5\instances\bt-03
```

Cada instalación tendría:

- runtime ID;
- lock;
- capacidad;
- proceso;
- workspace;
- estado.

Entonces podría agregarse un scheduler:

```text
AcquireAvailableMT5Runtime
```

No implementar ese pool antes de estabilizar una instancia.

---

## 26. Compatibilidad con el worker existente

La implementación debe minimizar el impacto sobre SQX.

### Reglas

- no alterar el comportamiento actual de tareas `sqx`;
- agregar tests de regresión;
- registrar activities nuevas;
- registrar task queue nueva;
- evitar compartir directorios temporales;
- reutilizar solamente componentes realmente genéricos:
  - logging;
  - Mongo;
  - Temporal;
  - tracing;
  - artifact storage;
  - modelos canónicos.

### Posible dispatch

```go
switch task.Type {
case TaskTypeSQX:
    return sqxHandler.Execute(ctx, task)
case TaskTypeMT5:
    return mt5Handler.Execute(ctx, task)
default:
    return fmt.Errorf("unsupported task type: %s", task.Type)
}
```

El switch central es aceptable si sólo resuelve el handler. La lógica de MT5 debe quedar completamente fuera de él.

---

## 27. Pruebas

### 27.1. Unitarias

- validación de tarea;
- generación de `tester.ini`;
- modificación de `.set`;
- serialización canónica;
- hashes;
- parser del reporte;
- normalización de métricas;
- clasificación de errores;
- idempotencia del repositorio.

### 27.2. Integración sin MT5

Usar fixtures:

```text
testdata/
├── reports/
│   ├── successful-report.htm
│   ├── empty-report.htm
│   └── malformed-report.htm
├── sets/
└── logs/
```

### 27.3. Integración con MT5

Casos mínimos:

1. EA válido y backtest exitoso.
2. EA inexistente.
3. parámetro inválido.
4. símbolo inexistente.
5. rango sin datos.
6. timeout.
7. cancelación Temporal.
8. proceso MT5 huérfano.
9. reporte no generado.
10. reporte corrupto.
11. Mongo temporalmente caído.
12. retry después de persistencia parcial.
13. misma tarea ejecutada dos veces.
14. diferencia entre hash esperado y real.

### 27.4. Golden test del parser

Guardar reportes reales conocidos y comparar contra JSON esperado.

```text
report.htm
    ↓ parser
expected-result.json
```

Esto es crítico porque el HTML puede cambiar o depender del idioma configurado en MT5.

---

## 28. Riesgo importante: idioma del reporte

Configurar la instalación MT5 con un idioma fijo, idealmente inglés.

El parser no debe depender de etiquetas traducidas como:

```text
Beneficio Neto Total
Total Net Profit
Lucro Líquido Total
```

Alternativas:

1. fijar idioma inglés en la plantilla MT5;
2. parsear por estructura estable;
3. soportar diccionario de etiquetas;
4. extraer desde un formato más estructurado si está disponible;
5. generar un export adicional desde el EA.

Para la primera versión, fijar inglés y usar golden tests.

---

## 29. Riesgo importante: validez del backtest

Un resultado exitoso técnicamente no implica comparabilidad con SQX.

Antes de marcarlo como comparable, verificar:

- símbolo esperado;
- fechas cubiertas;
- número de barras o ticks;
- depósito;
- leverage;
- moneda;
- spread;
- comisión;
- reporte sin errores;
- trades mayores que cero cuando corresponda;
- modelo de ticks esperado;
- EA correcto;
- parámetros correctos.

Agregar:

```go
type ResultValidation struct {
    Valid      bool
    Comparable bool
    Warnings   []string
    Errors     []string
}
```

Ejemplos de warning:

```text
MT5 returned zero trades
MT5 symbol differs from SQX symbol
History coverage does not include full requested range
Commission model is unknown
MT5 report uses a different deposit
```

---

## 30. Plan de implementación incremental

### Fase 1: ejecución local manual

- preparar instalación MT5;
- ejecutar un `.ex5`;
- generar `.set`;
- generar `.ini`;
- obtener reporte;
- documentar rutas reales.

### Fase 2: package Go `mt5`

- workspace;
- config renderer;
- process runner;
- timeout;
- cancelación;
- artifact collector.

### Fase 3: parser

- fixtures;
- métricas canónicas;
- validación;
- golden tests.

### Fase 4: Mongo

- colecciones;
- índices;
- upsert;
- idempotencia;
- correlación SQX.

### Fase 5: Temporal

- task queue;
- workflow;
- activities;
- heartbeats;
- retries;
- cleanup.

### Fase 6: integración Echo Forge

- nuevo `TaskTypeMT5`;
- dispatch desde pipeline;
- asociación con estrategia;
- persistencia final;
- observabilidad.

### Fase 7: comparación

- adaptador SQX a modelo canónico;
- cálculo de delta;
- tolerancias;
- flags de comparabilidad.

---

## 31. Criterios de aceptación

La implementación se considera lista cuando:

1. Una tarea `mt5` válida puede enviarse por Temporal.
2. El worker Windows la recibe desde una task queue dedicada.
3. Usa exclusivamente:

   ```text
   C:\mt5\backtesting
   ```

4. Crea un workspace aislado.
5. Copia o verifica el `.ex5`.
6. Genera parámetros dinámicos sin modificar el artifact original.
7. Genera `tester.ini`.
8. Ejecuta MT5 automáticamente.
9. Espera el cierre sin intervención humana.
10. Soporta timeout.
11. Soporta cancelación Temporal.
12. No permite dos backtests simultáneos sobre la instalación.
13. Recolecta reporte y logs.
14. Parsea métricas estructuradas.
15. Inserta o actualiza MongoDB idempotentemente.
16. Relaciona el resultado MT5 con:
    - `strategy_id`;
    - `workflow_id`;
    - `sqx_result_id`.
17. Una repetición del mismo activity no crea duplicados.
18. Un fallo deja información suficiente para diagnóstico.
19. Las tareas SQX existentes continúan funcionando sin cambios.
20. Existe al menos un test E2E real con un EA conocido.

---

## 32. Entregables esperados de la implementación

La IA o desarrollador que implemente esto debe entregar:

- modelos de dominio;
- nuevo tipo de tarea `mt5`;
- workflow Temporal;
- activities;
- task queue dedicada;
- runtime MT5 Windows;
- renderer `.ini`;
- generador/modificador `.set`;
- ejecución y cancelación de proceso;
- parser de reporte;
- repositorios Mongo;
- índices Mongo;
- logs, métricas y trazas;
- pruebas unitarias;
- fixtures;
- prueba E2E;
- documentación de configuración;
- ejemplo de payload;
- runbook de troubleshooting.

---

## 33. Decisiones recomendadas

Para evitar ambigüedades durante la implementación:

```text
EA de entrada:
    .ex5 ya compilado

Instalación:
    C:\mt5\backtesting

Modo:
    portable

Concurrencia inicial:
    1

Task queue:
    echo-mt5-backtesting

Optimización:
    deshabilitada

UI visual:
    deshabilitada

Agentes remotos/cloud:
    deshabilitados

Persistencia:
    MongoDB

Correlación:
    strategy_id + sqx_result_id + workflow_id

Resultado:
    modelo canónico + reporte crudo + logs

Idioma de MT5:
    inglés fijo

Idempotencia:
    config_hash + strategy_id

Backtesting NinjaTrader:
    fuera de alcance
```

---

## 34. Resultado arquitectónico esperado

La solución final de esta etapa debe verse así:

```text
Echo Forge Workflow
        │
        │ task type=mt5
        ▼
Temporal Task Queue
echo-mt5-backtesting
        │
        ▼
Go MT5 Worker
        │
        ├── Validate
        ├── Lock runtime
        ├── Prepare workspace
        ├── Render .set
        ├── Render tester.ini
        ├── Start terminal64.exe
        ├── Heartbeat / cancel / timeout
        ├── Collect report and logs
        ├── Parse metrics
        ├── Upsert MongoDB
        └── Release runtime
                │
                ▼
MongoDB
├── mt5_backtest_executions
└── mt5_backtest_results
                │
                ▼
Future comparison service
SQX metrics vs MT5 metrics
```

El objetivo de esta primera versión no es construir un administrador universal de terminales. Es establecer un runner MT5 reproducible, observable e idempotente, integrado correctamente con Temporal y MongoDB. Una vez estabilizado, la misma base permitirá agregar un pool de instancias, operación live y otros clientes sin rehacer el corazón del sistema.

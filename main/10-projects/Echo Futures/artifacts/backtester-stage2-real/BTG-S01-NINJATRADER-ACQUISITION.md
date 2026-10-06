---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-S01-DATASET-INVENTORY]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01-NINJATRADER-ACQUISITION

## Propósito

Resolver si las capabilities existentes permiten adquirir histórico real desde NinjaTrader para BTG-S01 sin intervenir D6. El Owner seleccionó NinjaTrader como fuente; no se busca proveedor alternativo ni se compra histórico.

## Contenido

### Resultado y corte

`ACQUISITION_STATE = BLOCKED_EXTERNAL`; existe un exportador oficial, pero esta superficie no controla la GUI de NinjaTrader ni tiene un archivo original identificado y legible con el permiso vigente. `CORPUS = NOT_ACQUIRED`; cobertura, contratos, counts, digests y suficiencia offline siguen `NOT_VERIFIED`. El bloqueo independiente `GERARD_IDENTITY = BLOCKED_DECISION` conserva su autoridad en el worker de identidad; este lookup no habilita ningún run certificatorio.

Corte de investigación: 2026-10-06, America/Santiago; observaciones propias por MCP/documentación realizadas antes de 2026-10-06T03:01:18Z. Agents-OS master observado `83a410df3503e105d42b0ac857c80289612986da`; source Backtester leído en `xKoRx/echo@cd451972b242c8933321e03001decd4b6d778c61`, worktree limpio. Echo master `372af59a7b83604781346613da01e3d510ea1360` y D6 `d08a30ce9815f820fda7132e20dc42cc345eb8e8` son refs de continuidad del mandato, no una nueva certificación física.

### Evidencia de acceso y mecanismos existentes

| Mecanismo | Evidencia | Conclusión acotada |
| --- | --- | --- |
| SSH `dev-win` | `list_connections` propio confirma profile viewer, `echo-dev`, target `.132`; `dev-win-operator` utiliza el mismo usuario OS. | El listado certifica exposición del profile, no permiso de leer caché NT ni de descargar. No se utilizó operator. |
| Caché NT `db/tick` del usuario interactivo | [[BTG-S01-DATASET-INVENTORY]] registra `Access is denied` / `UnauthorizedAccessException`, exit 1, al `ls` allowlisted; `Get-ChildItem` devuelve `POLICY_DENIED`. | Ruta no verificada debido a acceso; no inferir ausencia. No se repitieron probes, ni se cambió ACL, identidad o policy. |
| Stages legibles conocidos | Inventory revisó workspaces históricos locales, Downloads/Documents y stage D6; no identificó export TXT/archivo histórico pertinente legible. | No existe un path confirmado para recuperar un original mediante SFTP en este shot; resultado acotado, no ausencia global. |
| Transferencia SFTP | Tool `sftp_download(remotePath, profile)` expuesta; [[aranea-ssh-mcp]] condiciona ejecución al profile y permiso OS. | Sin archivo conocido no se prueba descarga a ciegas. `POLICY_DENIED` o EACCES futuros conservan el boundary. |
| Control GUI NT | Catálogo expuesto no ofrece control remoto de la GUI Windows/NinjaTrader ni una tool NT de exportación; `cua_repl` declara APIs nativas deshabilitadas. | El exportador GUI existe, pero no es ejecutable por este agente con esta superficie. No se abrió CUA ni se improvisó automatización GUI/SSH. |
| `BarsRequest` | C1 documenta API NinjaScript/AddOn para solicitar barras históricas, con profundidad tick desconocida; su warm-up sintetizado es distinto del corpus real BTG-S01. | API documentada no equivale a exportador histórico independiente ya expuesto. Usarla mediante instalación/cambio de AddOn o runtime D6 rebasa el mandato. |

La inspección propia remota fue únicamente `list_connections`; los rechazos filesystem proceden del inventory enlazado. No se escaneó el host, no se consultó ni capturó el feed y no se emplearon credenciales superiores/direct SSH. Las capabilities de storage amplias no prueban un stage NT autorizado ni justifican buscar objetos sin una ruta respaldada.

### Exportador oficial y acción mínima del Owner

NinjaTrader exporta sólo datos ya guardados como TXT. Abrir Control Center → Tools → Historical Data → Export; elegir instrumento, intervalo `Tick`, tipo `Last`, rango y destino. Los intervalos y tipos disponibles aparecen según los datos existentes; repetir para `Bid` y `Ask` cuando estén. El export usa timestamps UTC y formato de importación, con semántica End of Bar documentada. Este mecanismo no demuestra que el rango solicitado esté completo. [Exporting](https://static.ninjatrader.com/support/helpGuides/nt8/exporting.htm), [Historical Data Window](https://static.ninjatrader.com/support/helpGuides/nt8/historical_data_manager.htm).

La acción mínima es entregar esos TXT sin editarlos después de exportar, más una identificación de los instrumentos físicos y rango exportado y una captura o registro de las opciones elegidas. Exportar por expiry explícito, conservando el nombre NT; no usar una serie continua como prueba de contrato físico. No fijar fechas arbitrarias: primero reportar el rango tick disponible; la selección final dependerá de la Strategy/config autoritativa, warm-up y varios account-days.

La entrega puede ser un archivo adjunto o un stage de workspace ya accesible. Una ruta Windows nueva sólo podrá usarse después de confirmar permiso de lectura/transferencia vigente; esta nota no prescribe cambios de ACL. Los agentes recuperan por el mecanismo existente, preservan los TXT entregados, calculan SHA-256/tamaño/filas/rangos y construyen el manifest sólo con los bytes recibidos. El export es una representación generada por NT, no una copia byte a byte de `.ntd`/SQLite ni prueba de integridad de una caché inaccesible.

### Si la caché no alcanza

El Download oficial exige conexión y disponibilidad histórica del proveedor, permite elegir instrumento/rango/intervalos/tipos y muestra estado en la ventana. La documentación advierte que pedir fechas más antiguas que la retención del proveedor puede perder datos ya guardados. Además, `MergeBackAdjusted`/`MergeNonBackAdjusted` cambia contrato al cruzar rollovers; `DoNotMerge` corresponde sólo al contrato seleccionado. [Download](https://static.ninjatrader.com/support/helpGuides/nt8/download.htm).

Por preservación de originales y D6, este shot no descarga en la instancia activa ni cambia Merge Policy, Record live data, conexiones o settings. Si los TXT disponibles resultan insuficientes, falta un contexto NinjaTrader independiente autorizado por el Owner para descargar/exportar mediante su entitlement existente, sin interferir con D6 y con contratos físicos verificables. No se ha demostrado que tal contexto exista ni que el proveedor cubra el horizonte necesario. La tabla oficial de capacidades describe proveedores, no la cobertura/retención/entitlement efectivo de este login. [Data by Provider](https://static.ninjatrader.com/support/helpGuides/nt8/data_by_provider.htm).

### Qué admite el producto y qué debe comprobar el corpus

BT-S01 §5.1 congela `DatasetSource.Open(selection) → HistoricalCursor`, manifest lógico separado del receipt físico y consumo streaming. El source certificado ofrece `ndjson` plain/gzip; no lee TXT NT ni `.ntd`. El TXT necesitará conversión derivada después de comprobar el original; no se implementó parser/adaptador/framework antes de tener corpus.

Los formatos oficiales incluyen tick de tres campos `timestamp;price;volume`, con resolución de segundos o siete dígitos fraccionales, y variantes Tick Replay que incluyen last/bid/ask/volume. El archivo identifica Last/Bid/Ask. Examinar el formato real entregado antes de escoger parser; el formato documentado para importar Tick Replay no demuestra que este export incluya esas columnas, ni que contenga todos los updates de cada lado. [Importing](https://static.ninjatrader.com/support/helpGuides/nt8/importing.htm).

Debe preservarse orden original por archivo y distinguir registros iguales; timestamps no son IDs nativos. Normalizar UTC, unidades y contratos físicos contra autoridad, declarar resolución, cobertura/gaps/sesiones/rollover y guardar provenance/ref/ordinal más digests físico y normalizado. La exportación no entrega por sí sola identidad nativa de evento, orden total entre archivos ni freshness por lado. No inventar estas propiedades.

`OBSERVED_BBO` exige timestamps/refs de Bid y Ask por separado, coherencia de contrato/epoch y antigüedad comprobable; actualizar Bid no rejuvenece Ask. No mirar hacia adelante para completar el par. El `ndjson.decodeLine` certificado acepta TRADE/QUOTE y para QUOTE asigna a ambos lados el mismo ref y `event_ts` (`v3/backtester/internal/datasets/ndjson/ndjson.go`, líneas 556–562 y 638–647). Por tanto, combinar exports separados como QUOTE simultánea ocultaría la edad del lado previo. Con corpus real, seleccionar una representación que conserve evidencia lateral detrás del port existente; no certificar esa conversión por sólo decodificar NDJSON. Esto es una limitación de selección/representación comprobada en source, no un finding material de run ni un permiso para reparar sin input real.

Si sólo hay Last, `TRADE_MODEL` existe en BT-S01 §5.2, pero requiere offsets/costos explícitos y conserva el claim limitado: no fabrica QUOTE canónica ni reproduce el cadence BBO LIVE. Esta nota no elige ese modelo por inferencia ni afirma `LIVE_EQUIVALENT`.

### Handoff y cierre ONE-SHOT

- Resultado: ruta oficial identificada, adquisición externa bloqueada, original no recuperado. Sin manifest de corpus, sin conversión, smoke/longitudinal/rerun `NOT_RUN`.
- Próxima acción mínima: Owner entrega export TXT de caché NT disponible con provenance; el submanager comprueba bytes/cobertura y resuelve autoridad Gerard antes del run.
- D6: cero comandos de ejecución, trading, reconexión, restart, instalación, captura o mutación de runtime/AddOn/bridge/feed/egress/perfiles/cuentas; originales intocados.
- Registro `agents-os-agent-run-register`: skipped, lookup/documentación únicamente; source acotado leído para compatibilidad, sin evaluación de implementación o suite de producto.
- `agents-os-session-feedback = NONE`: no fricción reusable nueva; acceso restringido ya identificado por inventory y conserva el boundary conocido.
- `agents-os-session-close`: ejecutado por mandato explícito de cierre del worker, persistiendo este delta y su único change_log; no L0/L1, memoria duplicada ni cierre del submanager/programa.
- `REUSABLE_BEHAVIOR_CANDIDATES = NONE`; `PRO_CHAT_POOL_DELTA = 0` (superficie Codex LOCAL, sin consumo Pro confirmado).

## Fuentes

- [[BTG-PLAN]], [[BTG-S01-SUBMANAGER-PROMPT]] y steering Owner: obtener todo desde NinjaTrader.
- [[BTG-S01-DATASET-INVENTORY]], evidencia delegada de permisos/stages y alcance de inventario; draft observado al realizar este lookup, commit final pendiente del worker.
- [[Echo Futures — BT-S01 Backtester V1 Design]], §5.1–5.3 incluidas enmiendas frozen; `xKoRx/echo@cd451972b242c8933321e03001decd4b6d778c61:v3/backtester/dataset.go` y `v3/backtester/internal/datasets/ndjson/ndjson.go`.
- [[C1-NINJATRADER-ADAPTER-FIT-ANALYSIS]], evidencia histórica de BarsRequest y límites del warm-up; no usada como prueba de corpus o entitlement actual.
- [[Echo + Echo Forge — Environment Contract]], [[aranea-agent-dev]], [[aranea-mcps-expert]], [[aranea-ssh-mcp]] y tool surface actual del consumidor.
- Documentación oficial NinjaTrader enlazada por claim, consultada el 2026-10-06 UTC; profundidad/cobertura del login activo `UNKNOWN`.

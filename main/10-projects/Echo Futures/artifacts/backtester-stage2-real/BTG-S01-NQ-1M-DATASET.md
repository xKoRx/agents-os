---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-S01-DATASET-INVENTORY]]"
  - "[[BTG-S01-NINJATRADER-ACQUISITION]]"
  - "[[BTG-S01-IDENTITY-CONFIG]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01-NQ-1M-DATASET

## Propósito

Fijar el estado físico comprobable del histórico NQ Last de NinjaTrader para BTG-S01 y separar lo que el Owner ve en la GUI de lo que puede leerse, hashearse y servir como corpus durable en este entorno. Este inventario cubre datos solamente; no ejecuta simulaciones ni selecciona estrategia o configuración.

## Contenido

### Veredicto

`PHYSICAL_CORPUS = NOT_ACQUIRED`; `OWNER_GUI_DOWNLOAD = CONFIRMED_BY_OWNER`; `AGENT_READABLE_BYTES = NONE`; `PHYSICAL_MANIFEST = NOT_CREATED`; `LOGICAL_MANIFEST = NOT_CREATED`; `DATASET_SOURCE_ADAPTER = NDJSON_V1_ONLY_IN_CERTIFIED_S04`. La confirmación de descarga/visibilidad en NinjaTrader no acredita que exista una exportación durable, que el rango pedido esté completo ni que el agente tenga acceso a los bytes. No se declara ausencia global.

### Descarga observada por el Owner

El Owner confirma que NinjaTrader 8 estaba conectado vía Earn2Trade y que solicitó `NQ / Last / 1 minute` para `2023-10-01..2026-10-06`, con `Global Merge Policy = MergeNonBackAdjusted` y contratos físicos `12-23`, `03/06/09/12-24`, `03/06/09/12-25`, `03/06/09-26` y `12-26` como el contrato vigente al momento del download. En `12-23` reportó barras visibles de septiembre, octubre, noviembre y diciembre de 2023. Estos son hechos reportados de GUI; no se recibieron archivos, captura/export de opciones ni evidencia física independiente en esta ejecución. No se infiere que cada expiry tenga cobertura completa entre las fechas solicitadas ni que el año más reciente esté completo.

El Owner también reporta `Last / Tick` visible para `03-26` entre `2026-01-02..2026-03-20`; el download de ticks para `12-23` apareció sin datos. No hay bytes ni conteos de ticks para inspección. Este reporte de tick no amplía el corpus de barras de un minuto.

### Inspección física read-only de esta ejecución

| Superficie o acción | Resultado actual | Alcance de la conclusión |
|---|---|---|
| SSH `dev-win`, `list_connections` | Profile `dev-win` con rol `viewer`, identidad configurada `echo-dev@192.168.31.132`; `read-command whoami` respondió `dev-win\\echo-dev`. | Identidad del canal confirmada; no se usó `dev-win-operator` ni otra identidad. |
| `C:/Users` y `C:/Users/KoR` | `ls` permitió ver los perfiles `echo-dev`, `KoR`, `Public`, `TEMP`, y la lista superior de `KoR` con `Documents` y `Downloads`. No apareció un directorio `OneDrive` en esa lista. | Enumera los nombres de nivel superior visibles; no acredita el contenido de carpetas personales. |
| `C:/Users/KoR/Documents` y `C:/Users/KoR/Downloads` | `read-command ls` respondió `Access to the path ... is denied` / `UnauthorizedAccessException`. | No se pudieron buscar exports TXT, `.ntd` ni otros archivos bajo esas carpetas. |
| `C:/Users/Public` | `read-command ls` respondió `Access to the path ... is denied`. | No se pudieron inspeccionar archivos o stages en Public. |
| `C:/Users/echo-dev` | `ls` sólo mostró `.ssh`. | No se encontró un directorio NinjaTrader visible bajo el perfil remoto usado. |
| Caché `C:/Users/KoR/Documents/NinjaTrader 8/db/minute` | La única comprobación solicitada por `read-command ls` devolvió `Access is denied` / `UnauthorizedAccessException` y un mensaje secundario `Cannot find path`. | Resultado inconcluso por boundary; no permite decidir existencia ni contenido de `db/minute`. No se repitió con otro perfil. |
| Export TXT o archivo original remoto | No hay path de archivo confirmado y legible. `sftp-download` no se ejecutó. | Sin nombre de archivo verificado y permiso efectivo, no hay transferencia segura que iniciar. |
| Acceso a GUI/export de NinjaTrader | No hay capability de GUI disponible en esta ejecución. | La exportación desde GUI depende de una acción del Owner. |

La comprobación alcanzó un boundary concreto: `dev-win\\echo-dev` puede enumerar la raíz de `C:/Users` y `C:/Users/KoR`, pero Windows deniega el acceso a `KoR/Documents`, `KoR/Downloads`, `Public` y la carpeta `db/minute`. No se cambió identidad, ACL, profile, política ni runtime para superar la denegación. Como las carpetas del usuario quedaron inaccesibles y no hay un archivo identificado, esta inspección no demuestra ausencia de exportaciones ni de otros directorios potenciales.

### Contrato de manifest y campos aún no disponibles

No se creó un manifest físico o lógico sin bytes. Para cada archivo original elegible deben registrarse SHA-256, bytes, nombre/path de origen, fuente/proveedor y opciones de exportación, símbolo y expiry físico, tipo Last/Bid/Ask, intervalo, número de filas, primer/último timestamp UTC, semántica del timestamp NT (end-of-bar), OHLCV y validación de valores, duplicados, orden original, gaps, sesiones, límites de cobertura y provenance de rollover. En ausencia de originales, todos estos campos quedan `UNAVAILABLE`; no se sustituyen con las fechas pedidas en la GUI ni con eventos del feed D6.

`MergeNonBackAdjusted` es la política reportada para la serie descargada. La conservación de barras por expiry evita tratar una serie continua como prueba de cobertura por contrato; el rollover y la procedencia de cada fila deben determinarse desde archivos exportados y metadatos disponibles, no inferirse de una política global. El `timestamp` NT debe verificarse con el archivo real antes de fijar semántica end-of-bar, zona y normalización.

### Compatibilidad del DatasetSource S04

El source certificado `xKoRx/echo@cd451972b242c8933321e03001decd4b6d778c61` separa `DatasetSource.Open(selection)` y `HistoricalCursor` del engine. El único adapter físico revisado para esta compatibilidad es NDJSON V1 (`v3/backtester/internal/datasets/ndjson`), que admite NDJSON plano o gzip y valida manifiesto/identidad, rango y orden. No lee directamente NinjaTrader `.ntd`/SQLite ni TXT del exportador. No se construyó parser, conversor ni adapter porque todavía no existe un original para comprobar el formato y conservar provenance.

### Acción mínima para desbloquear

Delta submanager tras el cierre del inventario: `read_command ls C:/` y `ls C:/Temp`, mismo perfil `dev-win`, permitieron leer la raíz y el stage C:\Temp. Sólo se observaron bundles/checklists D6 y archivos AddOn/config en ese nivel, sin TXT histórico; no se leyeron sus contenidos ni se alteraron. C:\Temp es un destino legible comprobado. `C:\Temp\BTG-NQ-1m` se propone como carpeta nueva de export por Owner, todavía no creada ni inspeccionada. No fue un intento de entrar por otra identidad a la carpeta denegada.

El Owner debe exportar desde NinjaTrader la cobertura disponible como TXT, conservando los archivos originales de exportación sin edición, con un contrato físico por archivo y el rango/opciones reales de export registrados; luego debe dejar los bytes en un stage local legible o adjuntarlos. Si el output elegido no conserva intervalos de un minuto y el timestamp NT, no usarlo como prueba de barras 1m. Tras recibir bytes, guardar los originales fuera del vault en `Aranea work/btg-s01-nt-bars-data/originals/`, calcular hashes/bytes y producir el manifest físico/logical sólo con los registros observados. Mientras ese handoff no ocurra, corpus `NOT_ACQUIRED`; no ejecutar el backtester ni seleccionar un slice por inferencia.

## Fuentes

- Confirmación del Owner en esta ejecución, 2026-10-06: descarga NQ Last 1m, contratos solicitados, política MergeNonBackAdjusted y ventanas visibles reportadas; ticks Last de 03-26 y ausencia reportada para 12-23. La GUI no fue inspeccionada por el agente.
- Resultado vivo de `aranea-ssh__list_connections`, `read_command whoami`, y lecturas `ls` sobre las rutas listadas; perfil `dev-win` viewer. No hubo SFTP.
- [[BTG-S01-DATASET-INVENTORY]] y [[BTG-S01-NINJATRADER-ACQUISITION]] para superficies previas, restricciones de acceso y mecanismo de exportación oficial.
- `xKoRx/echo@cd451972b242c8933321e03001decd4b6d778c61`, `v3/backtester/dataset.go` y `v3/backtester/internal/datasets/ndjson/ndjson.go`, leídos para compatibilidad; tree de S04 limpio al revisar.
- [[BTG-S01-IDENTITY-CONFIG]] para la autoridad de identidad/configuración, fuera del scope de este inventario físico.

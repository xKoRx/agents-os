---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-PLAN]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-05"
updated: "2026-10-06"
---

# BTG-S01-DATASET-INVENTORY

## Propósito

Registrar qué histórico físico durable está realmente disponible para BTG-S01, qué superficies se inspeccionaron y qué evidencia impide seleccionar un slice real. Este documento no certifica la identidad de Strategy/MM ni inicia un backtest.

## Contenido

### Veredicto

`DATASET_STATUS = NOT_FOUND_IN_INSPECTED_SURFACES`; no equivale a `ABSENT_GLOBALLY`. No se encontró un dataset histórico físico de NQ/CME ni otro contrato autorizado que cubra varios account-days. No hay original elegible que se pueda identificar, hashear, convertir o seleccionar; por lo tanto, no se produjo derivado ni se ejecutó backtest.

`PRIMARY_PROGRAM_BLOCKER = BLOCKED_DECISION` por identidad exacta de Strategy Gerard/configuración, según la coordinación del Primary Manager; el inventario de datos mantiene `SECONDARY_BLOCKER = BLOCKED_EXTERNAL` porque no se recuperó histórico durable suficiente y la ruta Windows candidata denegó lectura. La identidad/configuración pertenece al otro worker y aquí queda `NOT_EVALUATED`.

### Fuentes inspeccionadas

| Superficie | Evidencia observada | Clasificación para BTG-S01 |
|---|---|---|
| Worktree certificado `bt-s04-20261004/echo` en `cd451972b242c8933321e03001decd4b6d778c61` | `AGENTS.md` leído; branch de certificación limpia; contiene `v3/backtester/dataset.go` y `v3/backtester/internal/datasets/ndjson/ndjson.go`; no se halló corpus histórico NQ allí. | Producto/adapters; no fuente de mercado. |
| Worktree local `hist-acq-20260921` | Catálogo físico incluye extracciones nombradas `mlb-*-2026-09-01.ndjson`, archivos de benchmark `events*.parquet`/`events.csv` y `book_levels.*`; son superficies de adquisición/benchmark de otros mercados, sin procedencia NQ/CME demostrada. | Rechazado: mercado/contrato y provenance no satisfacen el mandato. No se leyeron ni transformaron como entrada. |
| Worktree local `hist-l2-forensic-20260922` | `data/cohort_full.ndjson` (41,507,309 bytes, fecha de filesystem 2026-09-21) y scripts de reconstrucción de libros con contratos/eventos de prediction market. Es derivado de forensics L2, no barras/ticks NQ. | Rechazado: contrato y fuente no pertinentes; no se usó como histórico de backtest. |
| `Downloads` y `Documents` del workspace local | Ambos directorios existen. `find` y `rg --files`, enfocados hasta seis niveles, no encontraron nombres NQ/CME/tick/market/historical/export ni archivos `.dbn`, `.ntd`, `.ndjson`, `.jsonl`, `.csv`, `.parquet` o `.zip`. | Sin stage/export de NinjaTrader identificado en esos directorios; resultado acotado al filtro de nombres y profundidad indicados. |
| `opt/echo-dev` del workspace local | El inventario enfocado encuentra fuentes/configuraciones y checklists del AddOn, scripts `devwin-inspect` y `var/nt-feed/evidence.jsonl` (69,214,280 bytes, fecha de filesystem 2026-10-05). No aparece export/tick archive de NinjaTrader en ese árbol. | Stage accesible conocido sólo documenta/builda D6 o guarda evidencia de feed; no es dataset histórico. El JSONL no se leyó ni copió. |
| NinjaTrader `db/tick` en `dev-win` | Perfil MCP `dev-win` resuelve a identidad OS `dev-win\echo-dev`. `aranea-ssh/read-command` con el comando allowlisted `ls 'C:\Users\KoR\Documents\NinjaTrader 8\db\tick'` devolvió `Access is denied` (`UnauthorizedAccessException`, exit 1), seguido por un mensaje secundario `Cannot find path`. El resultado no permite decidir existencia ni contenido. | `PATH_UNRESOLVED_DUE_ACCESS_DENIED`; no concluir ausencia. No cambiar perfil/permisos. |
| `Get-ChildItem` contra esa ruta en `dev-win` | `aranea-ssh/read-command` devolvió `POLICY_DENIED` para el cmdlet invocado; no se reintentó por `run-command` ni por otra identidad. | Rechazo de policy; no evidencia de estado de archivos. |
| Descarga SFTP desde `dev-win` | El runbook documenta la tool `sftp-download` condicionada a permiso del profile; sin listado autorizado no hay nombre de archivo físico verificable que descargar. | No ejecutada: falta un path de archivo confirmado y no se conoce permiso de descarga de este profile. |
| MinIO | El runbook registra sólo `aranea-minio-rw`: identidad upstream owner FULL y `MCP_S3_EXT_READONLY=false`; también documenta tools metadata/list separadas de put/copy/delete. Se usó únicamente `s3_list_buckets`, que no muta objetos y devolvió 12 nombres sin uno identificable por nombre como archive/export NinjaTrader. | No se llamaron `list_objects`, `get_object_metadata`, `get_object` ni tools mutantes: no hay una stage NinjaTrader respaldada que justifique explorar objetos con esa identidad amplia. Bucket inventory no prueba ausencia global de archivos NT. |

El owner seleccionó NinjaTrader como fuente y descartó adquirir/proveer históricos externos. Los artefactos `hist-acq-20260921` y `hist-l2-forensic-20260922` quedan como pistas revisadas previamente y fuera de la búsqueda activa; no sustituyen datos de NinjaTrader. Un especialista de adquisición confirmó que la exportación disponible es por la GUI oficial de NinjaTrader; no hay capability GUI expuesta ni API independiente existente para ejecutarla desde este entorno. El TXT resultante es un artefacto transformado por el exportador, no una copia equivalente del cache NTD/SQLite; cualquier digest futuro corresponderá al TXT entregado, preservado sin editar tras la exportación. Los documentos D6 acreditan NQ (`NQ 12-26` ↔ `NQZ6`, stream `NQ:NQZ6`) y observaciones reales TRADE/BBO en un feed/tópico durante ventanas físicas; no acreditan un archive durable y no se consultaron offsets, consumidores ni el feed vivo para fabricar una ventana.

### Contrato del adapter y fidelidad que falta

El adapter del Backtester S04 es `DatasetSource.Open(selection) → HistoricalCursor`; el cursor entrega `HistoricalRecord` con `source_record_ref`, `source_order`, envelope normalizado y evidencia opcional por lado quote. El adapter NDJSON V1 admite archivos plain/gzip y valida identidad lógica/rango, schema, unidades, orden, payload y digest; su receipt separa representación física, SHA-256 de partes, tamaños y rangos de ordinales. La identidad lógica conserva corpus/version, stream, cobertura, conteos y digest normalizado. El diseño congelado permite otro adapter sin cambiar el engine.

No hay datos candidatos con los que llenar esos manifests: provenance/fuente, fecha económica, contrato, conteo, orden por stream, timestamps/zone, sesiones, rollover, gaps, TRADE/BID/ASK/BBO, source refs, digest lógico, SHA-256 físico y tamaños permanecen `UNAVAILABLE`. No se debe copiar esos campos desde D6 ni inferirlos de un nombre de archivo.

La fidelidad futura depende del corpus: `OBSERVED_BBO` requiere ambos lados realmente observados, con sus timestamps/referencias, contrato y epoch coherentes; actualizar un lado no rejuvenece el otro. Si sólo hay TRADE, el diseño contempla `TRADE_MODEL` con offsets enteros explícitos y claim limitado; no se reconstruyen BID/ASK ni QUOTE canónicos desde trades. No hay aquí una conversión obvia ni autorizada que aplicar.

### Slice real mínimo pendiente

No se seleccionó rango porque no hay corpus admisible y la identidad exacta solicitada está siendo resuelta por otro worker. Cuando ambas condiciones se cierren, elegir desde el original inmutable un tramo con warm-up previo a la ventana de Strategy, varios account-days, orden/event-time verificables y contratos físicos pertinentes; revisar calendario/sesiones y rollover cuando el rango cruce expiries. La evidencia plausible de breakout debe surgir de observaciones TRADE dentro del tramo y satisfacer la Strategy/config que se demuestre canónica; no se asume que Gerard sea `S1_NY_ORB_30M_V1` ni se presupone el tipo de señal. Una ventana sin breakout puede ser una observación válida pero no ejercita esa señal.

### Acción mínima para desbloquear

Para continuar desde NinjaTrader, la acción mínima es que el owner ejecute el exportador de la GUI oficial y entregue el TXT exportado en una ruta local accesible, sin editarlo después, junto con símbolo/contrato, rango, zona horaria y evidencia de la configuración/opciones del export. El TXT no se considera equivalente al cache NTD/SQLite ni se presupone compatible con el adapter NDJSON; primero se debe inspeccionar formato y fidelidad. Como alternativa, se requeriría permiso RO explícito para listar/leer el archive desde `dev-win\echo-dev`. Hoy ese perfil no puede inspeccionar `C:\Users\KoR\Documents\NinjaTrader 8\db\tick`; no se debe cambiar el perfil ni sortear ACL. No se necesita usar proveedor externo, capturar el feed D6 ni ampliar privilegios a una capability RW.

### Integridad y límites

No se modificó ningún original, repo de producto, configuración, perfil, cuenta física, runtime D6, bridge, egress ni offset Kafka. No hubo conversión, descarga, test de adapter ni corrida backtest. No se afirma `LIVE_EQUIVALENT`, corpus real disponible, slice representativo ni identidad de Strategy Gerard.

## Fuentes

- [[BTG-PLAN]] y [[BTG-S01-SUBMANAGER-PROMPT]], paquete Stage 2 vigente.
- [[Echo Futures — BT-S01 Backtester V1 Design]], §5.1–5.3 y enmiendas frozen de identidad, orden y fidelidad.
- [[Echo Futures — BT-S04 Final Remediation and Certification]], BT-S03-F08, certificación NDJSON y estado certificado del backtester.
- [[Echo + Echo Forge — Environment Contract]], §0–1 y §4; [[aranea-agent-dev]], [[aranea-mcps-expert]] y [[aranea-ssh-mcp]].
- Workspaces locales inspeccionados por nombre relativo: `bt-s04-20261004/echo`, `hist-acq-20260921`, `hist-l2-forensic-20260922`, y `opt/echo-dev/var/nt-feed`.
- Referencias D6 consultadas sólo como procedencia/routing: `artifacts/d6-g-realtime-20261004/D6-G-REALTIME-CERTIFICATION.md` y `artifacts/d6-owner-bundle-20261003/D6-OWNER-BUNDLE-BUILD.md`.

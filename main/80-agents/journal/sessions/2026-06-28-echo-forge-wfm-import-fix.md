---
type: session
scope: session
created: "2026-06-28"
updated: "2026-06-28"
area: "[[Personal]]"
project: "[[Symphony]]"
application: "[[Echo Forge]]"
entities:
  - "[[Symphony]]"
  - "[[Echo Forge]]"
related: []
aliases: []
confidence: high
source_session: "8e111370-744b-4d70-8c21-e2ed84e0d2d9"
load_policy: manual
indexable: false
index_priority: never
tags:
  - app/echo-forge
  - app/echoforge
  - area/personal
  - kind/session
  - project/symphony
  - scope/session
---
# Session Summary - 2026-06-28 - WFM Metadata Import Fix

> [!info]+ Session summary L1
> Resumen operativo del troubleshooting y fix final de la importación de metadatos de robustez Walk-Forward.

## Objetivo

- Identificar por qué fallaba la etapa de importación de metadatos de WFM (`03_wfm_optimizer` / `metadata_import`) del pipeline de SQX en Zeus, y resolver el problema de raíz en el plugin de Java y el worker de Go.

## Contexto cargado

- **Host y Credenciales de Zeus:** `kor@worker.zeus.lab.aranea` (IP: `192.168.31.101`).
- **Estado Inicial:** Las etapas de Builder y Retester completaban con éxito, pero la importación para `03_wfm_optimizer` fallaba porque no se encontraban los archivos `export_run.json` ni `wfm_matrices.ndjson` en MinIO/local.

## Trabajo realizado

1. **Corrección de Estrategia de Carga en StrategyQuant:**
   - Descubrimos que StrategyQuant X no cargaba el JAR del plugin de Custom Analysis (`echo-forge-sqx-exporter.jar`) desde `user/libs` para compilar extensiones de databanks al vuelo.
   - La solución fue mover el código fuente `WFMOptimizerJsonExporter.java` directamente a la carpeta de snippets compilables en caliente de SQX: `/home/kor/sqx/user/extend/Snippets/SQ/CustomAnalysis/WFMOptimizerJsonExporter.java`.
   - Limpiamos el archivo `.jar` obsoleto de `/home/kor/sqx/user/libs/` en Zeus.
2. **Corrección de Mapeo de Nombre de Plugin:**
   - Modificamos el constructor de `WFMOptimizerJsonExporter.java` para que el nombre del plugin registrado coincida exactamente con el tag `<FullDatabank1>WFMOptimizerJsonExporter</FullDatabank1>` usado en el CFX (`CustomAnalysis-Task2.xml`), en lugar del nombre largo con espacios anterior.
3. **Robustecimiento del Worker (Go):**
   - Corregimos un panic de puntero nulo (nil pointer dereference) en `steps.go:888` que ocurría al intentar leer `centerCell.Overview.OOS` cuando `wfm_cells` venía vacío en la matriz. Implementamos una protección defensiva para evitar la caída del worker ante matrices vacías.
4. **Validación de Extremo a Extremo (E2E):**
   - Compilamos localmente la versión `0.1.27` del worker, la empaquetamos con `./deploy_sqx.sh 0.1.27` y actualizamos el `manifest.json`.
   - El stager remoto en Zeus actualizó e inició automáticamente la versión `0.1.27` en caliente.
   - Disparamos una nueva wave de prueba (Wave 13) colocando el archivo de workflow en `./input/`.
   - Verificamos que la optimización `03_wfm_optimizer` completara correctamente ejecutando el plugin de Custom Analysis en Java (tardó 4.7s), escribiera los archivos locales y que la actividad de `metadata_import` de Go persistiera con éxito las matrices y corridas en MongoDB.

## Artifacts creados o modificados

- [WFMOptimizerJsonExporter.java](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/exporter-plugin/src/SQ/CustomAnalysis/WFMOptimizerJsonExporter.java) (Constructor corregido).
- [steps.go](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/activities/worker/steps/steps.go) (Fix defensivo de puntero nulo).
- [manifest.json](file:///Users/rjara/go/src/github.com/xKoRx/symphony/deploy/manifest.json) (Bumpeado a `0.1.27`).

## Memoria propuesta o creada

- **Ubicación de Extensiones de SQX:** Se descubrió que la ruta correcta para compilar y cargar snippets de extensiones en StrategyQuant X Build 142 de Zeus es `/home/kor/sqx/user/extend/Snippets/SQ/CustomAnalysis/` y no en `extend/Code/` o `libs/`.

## Decisiones

- **Despliegue del Plugin en Formato Fuente (.java):** Se optó por desplegar los plugins de Custom Analysis copiando directamente el archivo `.java` a la carpeta de snippets compilables en caliente de SQX en Zeus, asegurando la carga nativa al arrancar `sqcli`.

## Pendiente

- Ninguno. La importación de metadatos de WFM de SQX ya está funcionando end-to-end e insertando los datos correctamente en MongoDB.

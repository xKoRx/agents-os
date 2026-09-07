---
type: session
scope: session
created: "2026-07-10"
updated: "2026-07-10"
area: "[[Symphony]]"
project: "[[EchoForge]]"
application: "[[Symphony]]"
entities:
  - "[[EchoForge]]"
  - "[[Symphony]]"
related: []
aliases: []
confidence: high
source_session: 3c0133b0-cd67-4f2c-b398-1b670d3a753f
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

# EchoForge: Exporter Renaming and Stabilization Summary

> [!info]+ Session summary L1
> Resumen operativo sobre el renombrado de los exportadores JSON a la nomenclatura EchoForge, estabilización de los tests unitarios y despliegue del binario y snippets actualizados en Zeus.

## Objetivo

- Corregir las aserciones y datos simulados en las pruebas unitarias afectadas por el renombrado de los exporters de SQX.
- Alinear el directorio de descarga de metadatos con el proyecto fijo correspondiente.
- Subir los snippets Java actualizados a Zeus y eliminar los antiguos.
- Desplegar la nueva versión del worker (v0.1.65) y confirmar su ejecución exitosa.

## Contexto cargado

- Resumen del Handoff y logs de pruebas anteriores.
- Estructura de directorios de StrategyQuant en Zeus (`/home/kor/sqx/user/extend/Snippets/SQ/CustomAnalysis/`).
- Flujo de empaquetado y stager documentado en las skills `sqx-deployer` y `worker-ssh`.

## Trabajo realizado

- **Renombrado y Unificación de Nomenclatura**:
  - Renombramos los Custom Analysis Java locales a:
    - `EchoForgeOverviewExporter.java`
    - `EchoForgeWFMExporter.java`
    - `EchoForgeAutomator.java` (mantiene su nombre original ya que no es un exportador físico, sino un automatizador en caliente de parámetros y magic numbers)
  - Modificamos las validaciones e inyecciones en el monorepo en Go para que se correspondan con los nuevos nombres de exporter.
  - Corregimos y alineamos el directorio de descarga de metadatos en `ImportMetadataActivity` (`import_metadata.go`) para usar las rutas fijas de estos nuevos exportadores.
  - Actualizamos los archivos estáticos de datos de prueba (`overview.ndjson` y los mocks en los tests unitarios) para reflejar los nuevos strings de exporter.

2. **Estabilización de Tests Unitarios**:
  - Ajustamos las expectativas y mockups en `project_activity_test.go` para reflejar la eliminación del paso `write_exporter_properties` en el pipeline del builder/optimizer.
  - Todos los tests unitarios en `sqx/activities/worker/...` se encuentran en verde (**100% PASS**).

3. **Despliegue y Validación en Caliente (v0.1.70)**:
  - Eliminados en Zeus los archivos Java antiguos `EchoForgeAutomator*.java`.
  - Subidos a Zeus los nuevos snippets renombrados: `EchoForgeOverviewExporter.java`, `EchoForgeWFMExporter.java`, `EchoForgeRobustRunExporter.java` y `EchoForgeMT5Exporter.java` bajo `/home/kor/sqx/user/extend/Snippets/SQ/CustomAnalysis/`.
  - Compilamos la biblioteca de producción `EchoForgeAutomator.jar` mediante el compilador remoto contra las dependencias reales de SQX y la instalamos en `/home/kor/sqx/user/libs/` para habilitar la carga headless en Zeus.
  - Empaquetamos la release `0.1.70` del worker mediante `./deploy_sqx.sh 0.1.70` y actualizamos el manifiesto.
  - Verificado que el stager actualizó el binario en Zeus a la versión `0.1.70` y que el worker de Symphony está corriendo exitosamente.

---

## Configuración de los 4 Proyectos Fijos en la GUI de SQX (Zeus)

Para que el pipeline funcione de forma correcta, debes crear los siguientes 4 proyectos en la interfaz de StrategyQuant en Zeus:

### 1. Proyecto: `EchoForgeOverviewExporter`
* **Propósito:** Exportar metadatos y métricas básicas de estrategias en formato NDJSON (`overview.ndjson`).
* **Configuración:**
  - Agregar una tarea de **Custom Analysis** (`CustomAnalysis`).
  - Método de Custom Analysis: Seleccionar `EchoForgeOverviewExporter`.
  - Databanks: Entrada = `input`, Salida = `output`.

### 2. Proyecto: `EchoForgeWFMExporter`
* **Propósito:** Exportar la matriz WFM y los runs OOS en formato NDJSON (`wfm_matrices.ndjson`).
* **Configuración:**
  - Agregar una tarea de **Custom Analysis** (`CustomAnalysis`).
  - Método de Custom Analysis: Seleccionar `EchoForgeWFMExporter`.
  - Databanks: Entrada = `input`, Salida = `output`.

### 3. Proyecto: `EchoForgeRobustRunExporter`
* **Propósito:** Aplicar los parámetros de Walk-Forward y el Magic Number elegidos por Go.
* **Configuración:**
  - Agregar una tarea de **Custom Analysis** (`CustomAnalysis`).
  - Método de Custom Analysis: Seleccionar `EchoForgeRobustRunExporter`.
  - Databanks: Entrada = `input`, Salida = `output`.

### 4. Proyecto: `EchoForgeMT5Exporter`
* **Propósito:** Traducir estrategias `.sqx` (de cualquier origen) y exportar el código MetaTrader 5 `.mq5`.
* **Configuración:**
  - Agregar una tarea de **Custom Analysis** (`CustomAnalysis`).
  - Método de Custom Analysis: Seleccionar `EchoForgeMT5Exporter`.
  - Databanks: Entrada = `input`.

## Artifacts creados o modificados

- [manifest.json](file:///Users/rjara/go/src/github.com/xKoRx/symphony/deploy/manifest.json)
- [walkthrough.md](file:///Users/rjara/.gemini/antigravity/brain/3c0133b0-cd67-4f2c-b398-1b670d3a753f/walkthrough.md)

## Memoria propuesta o creada

- Ninguna memoria persistente L3 se requiere dado que los cambios corresponden al mantenimiento y resolución de la deuda de renombrado de la sesión anterior.

## Decisiones

- Desacoplar definitivamente la descarga de metadatos de los directorios de proyecto dinámicos de ejecución (`custom`), forzando que tanto la descarga como la lectura compartan la ruta estructurada bajo los proyectos de los exportadores fijos.

## GAPs de Diseño Identificados (Deuda Crítica de Escalabilidad)

> [!WARNING]
> **Hardcodeo de Carpetas de Tareas (`03_wfm_optimizer`)**:
> En el código del worker de Go (`steps.go`, `evaluate_wfm.go` e `import_metadata.go`), existe una condición explícita que evalúa si el nombre de la carpeta de la tarea es exactamente `"03_wfm_optimizer"` para decidir si gatillar el exportador de Walk-Forward (`EchoForgeAutomatorWFMExporter`) en lugar del de Overview (`EchoForgeAutomatorOverview`).
> 
> * **Problema de Escalabilidad**: Este condicional es un remanente obsoleto. En el diseño definitivo, **los exportadores son proyectos fijos** y su nombre de proyecto se define explícitamente a nivel de tarea en el archivo JSON del workflow.
> * **Solución Propuesta para la Siguiente Fase**: Eliminar por completo esta inferencia hardcodeada del código Go. El worker de Go debe leer únicamente el nombre del proyecto fixed del exportador parametrizado directamente en la tarea del JSON del workflow, eliminando cualquier lógica de strings condicionales sobre nombres de carpetas.

## Pendiente

- Limpiar la inferencia obsoleta de carpetas en Go, alineándola al 100% con la definición explícita del proyecto de exportación parametrizado en el JSON de las tareas.

---
type: known_error
scope: application
created: "2026-06-28"
updated: "2026-06-28"
area: "[[Symphony Portal]]"
project: "[[Symphony]]"
application: "[[StrategyQuant X]]"
entities:
  - "[[Symphony]]"
  - "[[StrategyQuant X]]"
related: []
aliases:
  - "StrategyQuant CLI Project Does Not Exist"
  - "sqcli config.xml task root error"
confidence: verified
source_session: "4af42ce7-35ef-4f46-9445-a0a05872312a"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - app/strategyquant
  - app/strategyquant-x
  - app/strategyquantx
  - area/symphony-portal
  - area/symphonyportal
  - kind/knownerror
  - project/symphony
  - scope/application
---
# SQCLI Project Does Not Exist (Task Root Tag Error)

## Síntoma

Al intentar ejecutar una tarea a través de la interfaz de línea de comandos de StrategyQuant (`sqcli`):
```bash
sqcli -project action=start name=02_retester_full
```
El proceso falla rápidamente (normalmente en menos de 10 segundos) con el siguiente error en la salida de consola:
```text
Starting StrategyQuant X in command line mode.
Params: -project action=start name=02_retester_full
18:28:49 Starting project '02_retester_full'
Error: Project '02_retester_full' does not exist.
```
A pesar de que el directorio físico `/home/kor/sqx/user/projects/02_retester_full` existe y contiene el archivo `project.cfx`.

## Causa

El archivo `project.cfx` (que es un archivo ZIP) contiene un archivo `config.xml` corrupto o con la estructura incorrecta:
1. **Diferencia entre Proyecto y Tarea:** En StrategyQuant X, un proyecto se define por un `config.xml` con etiqueta raíz `<Project>` que declara la lista de tareas (`<Tasks>`) y recursos (`<Resources>`). Las tareas individuales dentro de dicho proyecto se guardan como archivos XML complementarios (ej. `Retest-Task1.xml`).
2. **Exportaciones de Tarea:** Cuando un usuario exporta una tarea individual desde la GUI (como el Retester o el Optimizador), StrategyQuant genera un archivo `.cfx` que contiene únicamente un `config.xml` cuya etiqueta raíz es directamente `<Task>`.
3. **Sobreescritura directa:** Si el pipeline de despliegue descarga el archivo `.cfx` de la tarea de MinIO y lo escribe directamente como `project.cfx` en la ruta del proyecto, `sqcli` fallará al cargarlo porque no encuentra el elemento raíz `<Project>`, interpretando que el proyecto no existe.

## Impacto

Fallo inmediato de la ejecución de actividades de tipo `project` en el worker para tareas de re-test u optimización que utilicen configuraciones de tarea exportadas directamente.

## Detección

1. Inspeccionar la salida estándar de `sqcli` capturada por `cmd_executor.go` o en los logs de journal de la VM (`journalctl -u symphony-worker.service`).
2. Verificar el contenido del XML dentro del `.cfx` del proyecto:
   ```bash
   python3 -c "import zipfile; z = zipfile.ZipFile('project.cfx'); print(z.read('config.xml').decode('utf-8')[:200])"
   ```
   Si la salida comienza con `<Task ...>` en lugar de `<Project ...>`, la estructura está mal formada para actuar como un archivo de proyecto.

## Mitigación

Re-empaquetar la configuración antes de entregarla al worker para envolver la tarea dentro de un proyecto:
1. Crear un `config.xml` con la etiqueta raíz `<Project name="..." version="...">`.
2. Incluir una tarea que referencie a un archivo XML secundario: `<Task type="..." name="..." taskXMLFile="Task-File.xml" />`.
3. Copiar el XML original de la tarea (`<Task>`) con el nombre referenciado (ej. `Retest-Task1.xml` o `Optimize-Task1.xml`).
4. Añadir el bloque `<Resources>` y `<Databanks>` necesarios.
5. Comprimir ambos archivos en el `.cfx` final.

## Evidencia

- Documentado en la sesión de troubleshooting de [[Symphony]] el 2026-06-28.

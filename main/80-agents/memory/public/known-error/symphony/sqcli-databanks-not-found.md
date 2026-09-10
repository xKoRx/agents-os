---
type: known_error
scope: application
created: "2026-06-27"
updated: "2026-06-27"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities: []
related: []
aliases:
  - Error Databanks not found SQX
  - Element Databanks not found en sqcli
confidence: high
source_session: "8c11ec26-7ad2-4f0d-a862-0c85ceebe285"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - app/echo-forge
  - app/echoforge
  - area/echo
  - kind/known-error
  - project/echo-forge
  - project/echoforge
  - scope/application
  - tool/strategyquant
---
# StrategyQuant CLI Databanks Not Found Error

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- Al ejecutar la CLI de StrategyQuant (`sqcli`) con un archivo `.cfx` provisto como tarea, el comando falla con código de salida `1`.
- En los logs detallados de Java/StrategyQuant se observa la excepción:
  `java.lang.Exception: Element 'Databanks' not found`

## Causa

- Los archivos `.cfx` (que son en realidad archivos ZIP renombrados) provistos como configuración no contienen un proyecto completo de StrategyQuant (`Custom Project`).
- En lugar de eso, contienen una definición suelta de tarea (`<Task>`) guardada bajo el nombre de `config.xml` en la raíz del archivo zip.
- La CLI de StrategyQuant requiere obligatoriamente que el archivo `.cfx` tenga un nodo raíz `<Project>` con una estructura que defina `<Databanks>` (donde se especifican las entradas y salidas de las bases de datos) y que a su vez referencie a la tarea real en un archivo XML externo (ej: `Build-Task1.xml`, `Retest-Task1.xml`, etc.).

## Impacto

- Fallo inmediato del paso `execute_sqx` y de las actividades que interactúan con `sqcli` en el pipeline, abortando el workflow de Temporal.

## Detección

- Buscar en el output de error de la actividad o logs de StrategyQuant el texto `Element 'Databanks' not found` o la excepción Java correspondiente.

## Mitigación

1. Envolver la estructura de la tarea XML original en un nodo `<Project>` válido que contenga la estructura `<Databanks>`.
2. Renombrar el XML de la tarea (ej: de `config.xml` a `Build-Task1.xml` o similar) y referenciarlo dentro del nuevo `<Project>`.
3. Empaquetar el archivo `config.xml` del proyecto y el XML de la tarea de vuelta en un archivo ZIP con extensión `.cfx`.
4. La sesión fuente usó un script efímero `fix_cfx_final.py` para corregir estos archivos; no es una dependencia durable ni portable.

## Evidencia

- Evidencia efímera de la sesión fuente: `compare_builder_cfx.py`, `diff_builder_xml.py` y `fix_cfx_final.py`; no se conservan como locators canónicos.

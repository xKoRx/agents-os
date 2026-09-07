---
conversation_id: "3c0133b0-cd67-4f2c-b398-1b670d3a753f"
title: Echo Forge Magic Number & Robust Run Completed
created: 2026-07-09
type: change_log
tags:
  - log/change
  - app/echo-forge
  - topic/robustness
---

# Change Log: Echo Forge Magic Number & Robust Run Completed

## Qué cambió
- Agregamos lógica de restauración automática de la plantilla `.cfx` de robustez (`project.cfx.robust_template`) sobre `project.cfx` antes de llamar a SQX en [robust_activity.go](file:///Users/rjara/go/src/github.com/xKoRx/symphony/sqx/activities/worker/robust_activity.go). Esto evita que tareas del pipeline (como el retester o el optimizer) colisionen al compartir la carpeta del proyecto `"custom"`.
- Creamos la plantilla zip de robustez (`project.cfx`) y la respaldamos en `/home/kor/sqx/user/projects/custom/project.cfx.robust_template` en Zeus.
- Desplegamos la versión `0.1.66` de Symphony y reiniciamos el worker en Zeus.

## Motivo
- Asegurar que la actividad `ApplySelectedRunActivity` de Temporal use siempre la plantilla que contiene la tarea de `Custom Analysis` para ejecutar el plugin Java `EchoForgeAutomator`, permitiendo la exportación del código MetaTrader 5 (.mq5).

## Validación
- Corrimos con éxito el binario `test_apply_selected` en Zeus. El plugin inyectó los parámetros robustos y el Magic Number (`888111`) en el XML de la estrategia, exportando con éxito el EA `.mq5` (`263.49 KB`) y la estrategia robusta `.sqx` (`1.52 MB`) a MinIO.

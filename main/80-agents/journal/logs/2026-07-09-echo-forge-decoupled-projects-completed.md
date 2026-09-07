---
conversation_id: "3c0133b0-cd67-4f2c-b398-1b670d3a753f"
title: Echo Forge Decoupled Projects Completed
created: 2026-07-09
type: change_log
tags:
  - log/change
  - app/echo-forge
  - topic/robustness
---

# Change Log: Echo Forge Decoupled Projects Completed

## Qué cambió
- Dividimos el plugin en dos snippets de Custom Analysis: `EchoForgeAutomator` (aplica robustez y magic number) y `EchoForgeMT5Exporter` (exporta a MT5).
- Modificamos `robust_activity.go` para que corra consecutivamente los dos proyectos de SQX con sus respectivos properties de forma totalmente aislada.
- Desplegamos la versión `0.1.68` del worker de Temporal a Zeus.
- Rediseñamos la extracción de metadatos (overview y matrices WFM) para correr como tareas posteriores secuenciales e independientes sobre los proyectos fijos `EchoForgeOverviewExporter` y `EchoForgeWFMExporter`, manteniendo limpias las plantillas `.cfx` del pipeline.
- Diseñamos y agregamos el diagrama de Mermaid de orquestación del pipeline (Hito 1) en el [PRD de Echo Forge](file:///Users/rjara/go/src/github.com/xKoRx/symphony/docs/prd/SQX_Adaptive_E2E_Pipeline_PRD.md) junto con la explicación de la lógica de ordenamiento y deduplicación por tipo lógico del cerebro de clasificación (`ClassifyAndRankActivity`).
- Actualizamos formalmente las especificaciones funcionales en `FEAT-SQX-JAVA-EXPORTER-PLUGIN` y `FEAT-SQX-ROBUST-RUN-SETUP`.

## Motivo
- Permitir ejecutar de forma independiente el seteo de robustez y la exportación a MT5 desde proyectos desacoplados en SQX, evitando colisiones e inestabilidad en `project.cfx`.
- Garantizar que la tarea `EchoForgeMT5Exporter` sea genérica, desacoplada de la robustez, y aplicable sobre cualquier estrategia (inclusive directa de builder).
- Garantizar que las plantillas `.cfx` de generación/optimización sean completamente puras, delegando la exportación a proyectos fijos dedicados.
- Otorgar una vista clara y autoexplicativa del flujo del Hito 1 libre de GAPs.

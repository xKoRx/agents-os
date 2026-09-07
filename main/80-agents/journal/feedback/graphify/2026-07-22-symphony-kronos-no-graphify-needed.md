---
type: feedback
scope: graphify
created: "2026-07-22"
updated: "2026-07-22"
area: "[[Symphony Portal]]"
project: "[[Symphony]]"
entities:
  - "[[graphify]]"
related: []
aliases: []
agent: Claude Code (GLM-5.2)
session_goal: Diagnosticar fallo de Kronos en EchoForge
source_session: "2026-07-22-2022-symphony-kronos-sync-instruments-misdiagnosis"
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/graphify
  - project/symphony
  - agent/system1
---

# Graphify Session Feedback - 2026-07-22 - Symphony Kronos no graphify used

> [!NOTE]
> Feedback de Graphify para una sesión de diagnóstico de
> infraestructura donde la herramienta no se llegó a usar.

## Context

- Agent: Claude Code (GLM-5.2).
- Session goal: Diagnosticar fallo recurrente de Kronos en dos wfs.
- Main entity: Symphony / StrategyQuant X.

## Utilidad y Valor Aportado

- **¿Qué tan útil fue Graphify para resolver la tarea en esta sesión?
  (Puntúa de 1 a 5 y explica):**
  * **N/A (no usada)**. La sesión fue de diagnóstico de
    infraestructura: SSH a workers, queries a Temporal y MongoDB, y
    logs. Graphify no encajaba porque la pregunta no era de
    codebase sino de estado operacional en vivo. Puntuación 1 por
    omisión, no por mala herramienta.
- **¿Qué valor específico aportó en comparación con realizar
  búsquedas manuales (grep, list_dir, etc.)?**
  * Ninguno esta sesión. Sí usé Grep directo (vía tool) para
    localizar `ErrMetadataMissing` en el repo — eso sí fue útil.
- **¿Qué nodos, conceptos o relaciones clave devueltos por la
  herramienta fueron cruciales?**
  * N/A.

## Fricción y Entorpecimiento

- **¿La herramienta entorpeció, ralentizó o desvió tu flujo de
  trabajo en algún momento? (Explica detalladamente):**
  * No la invoqué, así que no entorpeció. Sí intenté una query de
    graphify (`graphify-personal query "where does ErrMetadataMissing
    get returned"`) pero falló porque el cwd era
    `scratch/graphify-out/graph.json` inexistente. El error fue
    operacional mío, no de la herramienta. Aborté y usé Grep
    directo.
- **¿Recibiste ruido, resultados irrelevantes o plantillas vacías
  que dificultaron la comprensión del contexto?**
  * N/A.
- **¿Hubo problemas de velocidad, límites de presupuesto (budget) o
  fallos de ejecución?**
  * No por la herramienta; sí por la invocación con cwd equivocado.

## Usabilidad y Comprensión (Know-how)

- **¿Sabías cómo usar la herramienta de manera óptima para el
  problema específico?**
  * Sí, pero el problema no era de codebase. Graphify es para
    preguntas sobre el grafo del código/fuente. Esta sesión era
    sobre estado de máquinas remotas y datos en MongoDB.
- **¿La documentación de la skill o las reglas del repositorio te
  guiaron correctamente sobre cómo estructurar la query?**
  * La regla "MANDATORY: before Read/Grep/Glob use graphify-personal
    query" me forzó a intentar la query desde el cwd incorrecto.
    Sería útil que la regla aclarase que graphify es opt-in para
    sesiones puramente operacionales (SSH, DBs externas).
- **¿Tuviste que recurrir a comandos manuales del sistema (grep,
  etc.) por frustración o vacíos de usabilidad en Graphify?**
  * Sí, Grep directo. No fue frustración: era lo correcto para
    localizar `ErrMetadataMissing` en archivos Go.

## Propuestas de Mejora de la Herramienta

- **Si pudieras cambiar el funcionamiento de Graphify, sus
  parámetros o la indexación de notas para que sea más amigable con
  agentes AI, ¿qué mejorarías hoy?**
  * Que `graphify-personal` resuelva la ruta del graph.json desde
    el repo workspace raíz, no desde el cwd. El error "graph file
    not found: .../scratch/graphify-out/graph.json" se habría
    evitado.
- **¿Qué sugerencias de cambio harías a las reglas del repositorio
  o prompts para facilitar el uso de la herramienta?**
  * Suavizar la regla "MANDATORY graphify before Read/Grep/Glob"
    para sesiones donde el target es un sistema externo (workers,
    MongoDB, Temporal). Algo como: "obligatorio para preguntas
    sobre el codebase local; opt-in para diagnóstico operacional
    externo".

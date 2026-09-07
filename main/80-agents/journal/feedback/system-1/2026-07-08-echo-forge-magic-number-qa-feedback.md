---
type: feedback/system-1
tags:
  - kind/feedback/system-1
  - tech/agents-os
created: 2026-07-08
---
# Session Feedback: Echo Forge Stage 4 QA

- **Qué complicó más la sesión**:
  - Las alucinaciones de la IA externa sobre la existencia de clases nativas en StrategyQuant X Build 142 generaron un bucle de verificación innecesario.
  - La falta de visibilidad en caliente de los logs de procesos locales iniciados bajo `screen` debido a la falta de asignación de TTY en ambientes daemonized de macOS.
- **Qué parte de Sistema 1 fue más útil**:
  - Las reglas del repositorio (especialmente la nueva regla de screen y deployer) previnieron levantar procesos huérfanos.
- **Qué parte fue menos útil**:
  - El workflow parser NDJSON no fue tocado, pero sirvió como referencia histórica.
- **Dolor repetible**:
  - Dificultad para interactuar con TTYs en macOS cuando se disparan tareas automatizadas detached en screen. Deberíamos considerar redirigir siempre la salida estándar a un archivo de log físico en lugar de confiar en la consola virtual.

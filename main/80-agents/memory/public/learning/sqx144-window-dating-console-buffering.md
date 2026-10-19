---
type: learning
schema_version: 1
scope: area
area: "[[Echo]]"
created: "2026-10-19"
updated: "2026-10-19"
confidence: verified
entities:
  - "[[Echo Forge — Operación Real V2]]"
related:
  - "[[Echo Forge — Operación Real V2]]"
aliases:
  - sqx task window dating
  - sqx global log timestamps
load_policy: manual
indexable: true
index_priority: normal
tags:
  - kind/learning
  - area/echo
  - tech/sqx
  - tech/measurement
---

# La ventana canónica de una tarea SQX es el `global_log`, no la consola ni el perfil CPU

SQX 144 headless bufea la salida de consola de sus tareas (CustomAnalysis y ReTest impresas al flush) y el reloj del log global va en hora local del host (UTC−6 en Kronos) mientras los filenames y `fc-run` van en UTC. Datar ventanas de energía por consola (poll de tamaño) o por landmarks del perfil CPU produce errores gruesos: la sesión del 2026-10-19 (gap closure) midió así "0,05–0,6 CPU-s → sin cómputo" en el retester N=10 y la re-medición canónica dio **22,50 CPU-s para el mismo corpus**.

Regla operativa:

- Convertir `TASK STARTED at YYYY.MM.DD HH:MM:SS.mmm` / `TASK FINISHED …` del `user/projects/<p>/log/global_log_*.log` más nuevo a epoch (local + offset UTC) y slice los CSV del sampler con esas marcas.
- "Task finished in X s" de SQX mide tiempo interno de tarea, no la ventana física completa; sirve como cross-check, no como ventana.
- Un veredicto de "sin cómputo" por energía ausente exige primero descartar artefacto de datación (energía negativa en el slice correcto = ventana mal datada, no trabajo ausente).
- Los group-jiffies @200 ms son la fuente autoritativa de energía; el sampler per-tid @1 s sub-muestrea en ventanas <20 s (detección de JVM intermitente): útil para forma (workers equilibrados), no para sumas.

Evidencia: [[CPU-GAP-CLOSURE-RESOLUTION-20261019]] §GAP 2; scripts `g2-energy.sh`/`analyze-g1.py` en `forge-cert-20261018/gap1/` (Kronos).

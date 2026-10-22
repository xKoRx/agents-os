---
type: session_feedback
schema_version: 1
scope: project
created: "2026-10-22"
updated: "2026-10-22"
area: "[[Echo]]"
project: "[[Echo Futures — Execution Client y Feed Batching]]"
entities:
  - "[[Echo Futures — Execution Client y Feed Batching]]"
related: []
aliases: []
confidence: verified
load_policy: manual
indexable: true
index_priority: low
tags:
  - kind/session-feedback
  - area/echo
---

# Feedback — FEFB S02 auditoría adversarial (procesos en background y contención de sweeps)

- **Pain pattern candidate (wrapper "completed" mata/malreporta hijos en background):** un `go test` largo lanzado con `&` dentro de una llamada Bash reporta "completed" al terminar el wrapper mientras el hijo sigue vivo; en una segunda intención de relanzamiento truncó el log del hijo original (`>` reabre el fd) y la lectura de estado con `pgrep -c "go test"` (sin `-f`) da 0 porque el comm no coincide. Patrón seguro para corridas >2min: `setsid bash -c '... > log 2>&1; echo EXIT=$? >> log' < /dev/null > /dev/null 2>&1 &` + sondeo del log/`pgrep -f`. Aplica a cualquier grind con suites largas.
- **Transferible (capacidad):** las campañas con barra de latencia sobre reloj real (AC13) no son ejecutables en paralelo con otros sweeps: 2 sweeps concurrentes en 8 cores degradaron la edad max de 11,14s a 36,5s y voltearon el PASS. Toda medición de capacidad/race debe correr sola en el host; el implementador además dejó evidencia de su propia corrida de cobertura fallando la campaña (923s) — declarar host dedicado como condición del gate.

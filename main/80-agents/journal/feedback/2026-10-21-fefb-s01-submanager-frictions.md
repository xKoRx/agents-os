---
type: session_feedback
schema_version: 1
created: "2026-10-21"
updated: "2026-10-21"
area: "[[Echo]]"
project: "[[Echo Futures — Execution Client y Feed Batching]]"
tags:
  - kind/feedback
  - area/echo
---

# 2026-10-21 — FEFB S01 fricciones y defensas

- **Pausa del host mata workers mid-flight sin rastro.** El corte 02:30 eliminó la tarea del worker W3 (sin reporte, sin notificación) dejando 26 rutas sin commit ni explicación. Defensa ejecutable: antes de una parada planificada, exigir checkpoint del worker (commit WIP en rama desechable o reporte parcial) y registrar en memoria qué worker estaba en vuelo; al reanudar, evaluar el árbol con build+suite ANTES de decidir reparar/rehacer (aquí evitó rehacer 3h de trabajo).
- **El PASS verbal del worker puede apoyarse en evidencia sobrescrita.** W4 reportó números correctos de la corrida de 30min, pero el artefacto durable fue sobrescrito por una smoke posterior (mismo path). Defensa: nombre de artefacto por run (timestamp/knob) o append-only; el revisor contrasta el PASS contra el LOG de la corrida, no sólo contra el artefacto.
- **Verificación de "fallos preexistentes": worktree limpio del SHA base es el oráculo barato.** W4 lo hizo con restore-revert de sus archivos; el submanager lo replicó con `git worktree add` al SHA base (3 fallos confirmados preexistentes). Hacerlo estándar en toda integración multi-worker.
- **go test full-module tarde 30min de penalización por un test colgado** (timeout por defecto del paquete). Defensa: en suites de integración grandes, correr primero con `-timeout` corto y `-run` acotado para triage, luego la corrida completa.

---
type: session_feedback
schema_version: 1
scope: session
created: "2026-10-19"
updated: "2026-10-19"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application:
entities:
  - "[[Echo Forge — Operación Real V2]]"
aliases: []
confidence: verified
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session-feedback
  - scope/session
  - area/echo
---

# 2026-10-19-sqx144-cpu-gap-resolution-session-feedback

## Pain Pattern Candidate

- **La datación por perfil CPU tampoco basta para tareas SQX calladas:** la sesión anterior detectó el buffering de consola y pasó a datar por landmarks del perfil CPU; con eso mismo se firmó "0,05–0,6 CPU-s → sin cómputo" en el retest N=10 y era FALSO (medición correcta por `TASK STARTED → TASK FINISHED` del log global: 22,50 CPU-s para el mismo corpus). Regla dura: **la única ventana canónica para energía/throughput de una tarea SQX son los timestamps del `global_log` del proyecto** (convertidos local→UTC); consola y perfil CPU son indicativos, nunca certificado. Un veredicto FAIL por "energía ausente" requiere descartar primero artefacto de datación.
- **Instalaciones de flota con `internal/` kor-owned:** cualquier experimento que deba tocar `Snippets.jar` necesita la instalación candidate-local escribible; verificar el SHA del jar ENCONTRADO antes de tocarlo y restaurarlo al cierre (esta sesión encontró el perf jar ya restaurado a fleet `aac0e8f2` por la sesión S01 — el estado inicial no siempre es el esperado; verificar, no asumir).
- **Corridas que reemplazan bancos de datos:** snapshottear los outputs ANTES del siguiente run — el run N=1 pisó el banco de salida del run N=10 y obligó a un re-run (barato aquí porque la corrida era 27 s, pero el patrón escala mal).
- **Transporte MCP SSH para ingeniería pesada:** límite de 5000 caracteres por comando, heredoc inestable, sftp fail-closed y redacción de nombres por entropía — trabajar con gzip+base64 por pipes y scripts residentes en el host es el patrón que funcionó de principio a fin.

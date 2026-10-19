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

# 2026-10-19-sqx144-full-cpu-gap-closure-session-feedback

## Pain Pattern Candidate

- **Certificaciones de lineage con sellos parciales:** el cert selló cohort↔builder-output y las fuentes del optimizer, pero nunca comparó esas fuentes contra el banco físico de salida del retester — el único salto roto (Retester→Optimizer, bytes pre-retest) quedó fuera de los sellos. Regla para próximos certs: el manifiesto de continuidad debe encadenar TODOS los saltos contra el output físico de cada etapa, y el harness debe sembrar cada etapa desde el banco de salida de la anterior.
- **Dación de fases por consola no sirve para tareas SQX calladas:** la tarea CustomAnalysis bufea su salida ("Starting…" y "Task finished" aparecen pegados en el flush final) y el poller de tamaño de consola data mal la ventana. Datar por landmarks del perfil CPU (asentamiento post-boot, cola de save) + per-tid; ya documentado como gotcha en CPU-GAP-CLOSURE-20261019.md.

## Fricción de superficie (menor, conocida)

- El transporte MCP-ssh redacta strings de alta entropía (nombres de clase en unzip -l) y rompe heredocs/multi-línea python: workaround estable = scripts subidos por HTTP+SHA y one-liners de shell; ya registrado en feedbacks previos del 2026-10-18/19.

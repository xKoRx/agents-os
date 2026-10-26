---
type: session_feedback
schema_version: 1
scope: session
created: "2026-10-23"
updated: "2026-10-23"
area: "[[Echo]]"
project: "[[Echo Futures — Optimización de Campañas]]"
application:
entities: ["[[Echo Futures — Optimización de Campañas]]"]
related: ["[[80-agents/skills/agents-os-skill-authoring/SKILL.md|agents-os-skill-authoring]]"]
aliases: []
confidence: verified
source_session:
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/feedback
  - scope/session
  - area/echo
---

# 2026-10-23 — Echo Futures R03 session feedback

## Pain Pattern Candidate

**Monitores que cuentan en-vuelo como pendiente.** El verificador de una línea del run (patrón copiado de R02) computaba `pend = total − ok` sin restar los jobs en vuelo, produjo una falsa alarma de sub-admisión que pudo disparar un relanzamiento innecesario del supervisor. Regla absorbida en `echo-retester-master`: `pend_real = total − ok − inflight` con inflight contado por `comm` real, y `ACCION` sólo con `pend_real > 0`.

## Fricciones efectivas

- **Convención de digest no declarada en el caché**: `r02_finalize.py` guarda el digest del result como hex crudo; un reimplementador natural agrega el prefijo `sha256:` e invalida TODO el caché silenciosamente (89 re-caracterizaciones bajo carga antes de detectarlo). Lección: las convenciones de clave implícitas deben declararse en el propio script (ya documentado en `echo-retester-master`).
- **Binarios de diagnóstico vs identidad del motor**: el motor valida `vcs.revision`/`vcs.modified`/sha contra el plan; un parche temporal requiere worktree + commit limpio + plan regenerado con esa identidad. No estaba documentado como procedimiento; quedó en `echo-retester-master` (lecciones R03).
- **`__pycache__` rastreados en el repo de producto**: intentos de limpieza de cachés generan ruido en `git status` y estampan `vcs.modified=true` en builds si quedan sin rastrear; la higiene propuesta (borrarlos) arrastraba su eliminación al commit del fix y hubo que revertirla para mantener el commit quirúrgico.
- **Timeout de shell (10 min) con salida por `tail`**: los logs de procesos largos redirigidos a `| tail` pierden todo el buffer si el comando muere por timeout; el patrón correcto es redirigir a archivo y leer el archivo.

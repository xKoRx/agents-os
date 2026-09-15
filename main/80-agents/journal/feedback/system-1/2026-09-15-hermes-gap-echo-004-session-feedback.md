---
type: feedback
schema_version: 1
created: "2026-09-15"
area: "[[Aranea]]"
project: "[[HERMES — Agent Access Operations]]"
related:
  - "[[mcp-access-plane-operations]]"
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/feedback
  - scope/session
---

# 2026-09-15 — Hermes GAP-ECHO-004 session feedback

- **Friction:** el gate de aprobación local (timeout sin respuesta) abortó un comando compuesto pipe bearer→ssh local aunque era el patrón documentado; reestructurar a 100% server-side (scp + ejecución en mcps, bearer stdin local) lo evitó de raíz. Costo: un ciclo completo de retry.
- **Friction:** `write_file` emitió un archivo Python corrupto (texto interno mezclado, sintaxis rota) en el primer intento; detectado por el lint del propio tool y reescrito limpio. Vigilar outputs de generación larga en scripts.
- **Pain Pattern Candidate:** owner seed bundles construidos por agentes asumen estado del target no verificado (identidad `echo-dev` preexistente — no lo estaba; el owner lo resolvió creándola). Regla nueva en runbook + skill: preflight obligatorio `id -u <user>` (y existencia de paths) antes de emitir un bundle; el bundle debe ser válido para "identidad no existe" o declararlo explícitamente.
- **Nota positiva:** el quirk del pool de 64 sesiones de ssh-mcp quedó con prevención (sesión única por probe) documentada en runbook/skill/template en la misma sesión.

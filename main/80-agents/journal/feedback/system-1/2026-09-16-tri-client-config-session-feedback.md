---
type: session-feedback
schema_version: 1
created: "2026-09-16"
area: "[[Aranea]]"
project: "[[AGENTS OS]]"
related: []
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session-feedback
  - scope/session
---

# 2026-09-16 — Tri-client config session feedback

- **Fricción (menor):** `session_search` FTS5 no indexa contenido de mensajes largos por keyword puntual (0 hits en queries específicas p.ej. nombres de backups); el hallazgo salió por workspace + scroll window. Scroll por `around_message_id` sí funcionó bien para reconstruir la sesión colgada.
- **Hallazgo de proceso:** sesiones one-shot con `clarify` sin respuesta dejan el estado solo en el workspace efímero (`~/tmp-tri-client/`) y en el historial — nada en el vault hasta el cierre. El recovery funcionó, pero un checkpoint temprano (change-log corto al completar cada gate) habría ahorrado la reconstrucción.
- **Observación:** mtimes de configs kor (13:26:41) sin change_log que los ampare pese a sesión vault declarada read-only la misma mañana — reforzar disciplina: toda edición fuera del vault genera su log inmediato.

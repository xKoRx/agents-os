---
type: change_log
schema_version: 1
scope: session
created: "2026-08-14"
updated: "2026-08-14"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
  - "[[ZCode]]"
related:
  - "[[Codex]]"
  - "[[Claude Code]]"
  - "[[Cursor]]"
  - "[[Antigravity]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - project/agentsos
  - scope/session
---

# Change Log — Registro de superficie ZCode en crew (2026-08-14)

## Cambios

- Creada nota canónica `80-agents/crew/ZCode.md` (`type: agent`, materializada vía `materialize_schema_note.py`) extendiendo el registro de superficies antes de registrar el primer run atribuible a ZCode, según exige `agents-os-agent-run-register`.
- Primer agent run registrado: `2026-08-14-zcode-glm-5-3-echo-native-dailyops-fix.md` (modelo host-reported `builtin:zai-coding-plan/GLM-5.3`).

## Razón

- Sesión de debug/fix en Echo V3 (ops NATIVE invisibles en Daily Ops) ejecutada íntegramente en ZCode; sin superficie registrada no existía evidencia auditable de la combinación superficie×modelo.

## Impacto

- `crew/INDEX.md` no requiere edición: las superficies se listan por dataview sobre `type = "agent"`.
- Sin cambios de comportamiento operativo; sólo registro.

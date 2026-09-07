---
type: change_log
schema_version: 1
scope: session
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities: []
related:
  - "[[2026-09-04-echo-forge-mt5-report-6180-compatible-allowlist]]"
  - "[[2026-09-04-mt5-terminal-build-unsupported]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-MT5-BUILD-6180-PARSER-CERTIFICATION-TOP
source_feedbacks:
  - "[[2026-09-04-echo-forge-mt5-6180-parser-cert-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-04-echo-forge-mt5-6180-parser-cert

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - created `80-agents/memory/public/decision/symphony/2026-09-04-echo-forge-mt5-report-6180-compatible-allowlist.md`
  - created `80-agents/memory/internal/agent-memory/2026-09-04-echo-forge-mt5-6180-parser-cert-continuity.md`
  - created `80-agents/journal/agent-runs/2026-09-04-cursor-grok-4-6-echo-forge-mt5-6180-parser-cert.md`
  - created `80-agents/journal/feedback/system-1/2026-09-04-echo-forge-mt5-6180-parser-cert-session-feedback.md`
  - updated `80-agents/memory/public/known-error/symphony/2026-09-04-mt5-terminal-build-unsupported.md` (síntoma Live Update 6180 + clasificación A pendiente de NORMAL)
  - este change log
  - sin cambios de source symphony (TOP read-only)

## Motivo

- Cerrar la certificación física de MT5 build 6180 y dejar el contrato NORMAL ejecutable, más el checkpoint para reanudar Finalist Factory V1.

## Fuentes usadas

- symphony `0f18ef0440e104c6a38ba4cc259f674cfad3c390`; SPEC-PARSER.md; CORPUS.md; `sqx/adapters/mt5/report/{types,parse,crosscheck,parse_test,corpus_test}.go`; HTM físico Kronos SHA `6c9e975f…`

## Resolución aplicada

- Clasificación A; `parser_version` intacta; allow-list recomendada `{6090,6140,6180}`; evidencia HTM fuera de repo.

## Validación

- `Parse(raw6180)` → `ErrBuildNotSupported{6180}`; mutación allow-list → 7/7 PASS; procesos Windows en cero al cierre.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin credenciales, sin paths de máquina en la decisión pública más allá de host lógico `worker-kronos`

## Rollback

- Borrar las notas created de esta sesión; revertir el párrafo 6180 del known-error. El HTM `/tmp` no está en git.

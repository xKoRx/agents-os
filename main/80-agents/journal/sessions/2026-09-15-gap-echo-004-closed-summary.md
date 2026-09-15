---
type: session-summary
schema_version: 1
created: "2026-09-15"
area: "[[Aranea]]"
project: "[[HERMES — Agent Access Operations]]"
related:
  - "[[ACCESS-CERTIFICATION]]"
  - "[[Echo — Access & Physical Capability Matrix]]"
  - "[[Echo + Echo Forge — Deferred Certification Backlog]]"
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session-summary
  - scope/session
---

# 2026-09-15 — GAP-ECHO-004 closed

- **Objetivo:** completar el seed SSH mínimo del target `.71`, recertificar `echo-runtime-prod` desde el consumer real y cerrar formalmente GAP-ECHO-004. Sin MCP nuevo, sin tocar Echo productivamente, sin restarts, sin rotar host keys, sin etcd/Temporal.
- **Resultado: PASS — GAP-ECHO-004 CLOSED.** Owner seed instalado (identidad dedicada `echo-dev` creada por el owner tras corrección del bundle; key del plane append-only en `authorized_keys`). Recertificación viewer PASS end-to-end: identity `echo-dev@echo` sin sudo; Gateway/Core/`echo-functions` RUNNING, **Bridge NOT_DEPLOYED** (evidencia, no se levanta); listeners 80/9080/9090/8080/8090; negative `run-command` → POLICY_DENIED MUST DENY; leak CLEAN. Observación runtime PROD queda dual: viewer SSH + `aranea-observability-ro`.
- **Quirk nuevo registrado:** pool de 64 sesiones de ssh-mcp se agota con probes init-only por llamada → sesión única por probe; recovery `docker restart ssh-mcp`.
- **Evidencia durable:** change log `80-agents/journal/logs/2026-09-15-gap-echo-004-closed.md` · [[ACCESS-CERTIFICATION]] § GAP-ECHO-004 CLOSED · bitácoras de [[HERMES — Agent Access Operations]] (+A-D08), E-02 y delta de readiness del backlog.
- **Deuda separada no bloqueante:** host key `.71` idéntica a `sqx-zeus` (rotación owner opcional).

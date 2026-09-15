---
type: session-raw
schema_version: 1
created: "2026-09-15"
area: "[[Aranea]]"
project: "[[HERMES — Agent Access Operations]]"
related:
  - "[[ACCESS-CERTIFICATION]]"
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session-raw
  - scope/session
---

# 2026-09-15 — GAP-ECHO-004 closed (raw)

- Owner seed `echo-dev.pub` instalado en `.71` por el owner tras bundle mínimo (key leída de disco, fingerprint `2Qv9f2AREQyse50bGYaTLc1PHK43gvuf3xgv5TTJ+I0`; append-only; corrección de runtime: `echo-dev` no preexistía → creado como identidad dedicada uid/gid 1001, sudo DENIED).
- Recertificación consumer `echo-runtime-prod` desde Daedalus/cursor vía plane (probe server-side en mcps, bearer stdin, sesión MCP única): initialize PASS, 11 tools, identity `echo-dev@echo` sin sudo, Gateway RUNNING (PID 713), Core RUNNING (PID 110701), `echo-functions` RUNNING (PID 320982), Bridge NOT_DEPLOYED, listeners 80/9080/9090/8080/8090, negative `run-command` → POLICY_DENIED, leak CLEAN. RESULT: PASS → GAP-ECHO-004 CLOSED.
- Boundary confirmado: clase `safe` también POLICY_DENIED en viewer (docker/curl/systemctl/dmesg/pgrep); journal propio únicamente; `ss -tlnp` sin atribución cross-user.
- Quirk nuevo: pool 64 sesiones ssh-mcp agotado por probes init-only-per-call → 503; recovery `docker restart ssh-mcp` (healthy, config intacto). Prevención: sesión única por probe.
- Fricción: gate de aprobación local mató un pipe bearer→ssh local (reestructurado a todo server-side); write_file produjo un archivo corrupto una vez (reescrito); sed por patches con verificación de tablas (3 filas reparadas).
- Documentación: [[ACCESS-CERTIFICATION]], Matrix Echo, Backlog (delta 2026-09-15b), E-02 bitácora, Agent Access Operations (bitácora + A-D08), runbook `aranea-ssh-mcp`, skill vault `aranea-mcps-expert`, skill local `mcp-access-plane-operations` (+ template), change log `2026-09-15-gap-echo-004-closed`.
- Deuda abierta no bloqueante: host key `.71` clonada de `sqx-zeus`.

---
type: session_feedback
schema_version: 1
scope: session
created: "2026-09-24"
updated: "2026-09-24"
area: "[[Aranea]]"
project: "[[Echo Forge — Operación Real V2]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
  - "[[aranea-ssh-mcp]]"
related: []
aliases: []
confidence: verified
source_session:
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session-feedback
  - scope/session
  - area/aranea
---

# 2026-09-24 — Forge V2 prework corrección: feedback de sesión

## Fricciones observadas (con evidencia)

1. **`aranea-ssh` MCP: agotamiento del pool de 64 sesiones (2.ª ocurrencia documentada).** `/status` devolvía `running`, `connections:[]`, pero `initialize` respondía 503 "Server is at its session limit". Remediación canónica aplicada de nuevo (hermes→mcps-ops→`docker restart ssh-mcp`, imagen `local/ssh-mcp:2.8.0-d2d7696-h2fix` intacta). Recurrencia 2026-09-22 y 2026-09-24 ⇒ el defecto de fondo del pool no está resuelto; candidata a known_error con fix durable en el ssh-mcp.
2. **`sftp-download` del ssh-mcp degrada binarios.** El contenido se devuelve inline como texto en `content[].text` (con reemplazos no-mapeables): un PDF de 235 KB llegó corrupto (`0x3f` en bytes no-ASCII) y un ZIP de 1,5 GB es inviable. Regla operativa: binarios ⇒ scp/rsync con clave temporal autorizada + revocación verificada, nunca `sftp-download` inline.
3. **Build del repo `symphony` desde `d9032ff8` no puede producir `vcs.modified=false`.** El build reescribe `go.work.sum` (stale frente al grafo actual) antes del stamp; con el archivo 444 el build falla; `-mod=readonly` no lo impide. Consecuencia: todo binario candidato certificado desde master carries `vcs.modified=true` sin delta de código (delta capturado en workspace). Fix de fondo = commit de higiene de `go.work.sum` (acción repo, no de sesión).
4. **`CancelWorkflow` no cierra workflows sin poller en la cola.** El zombie del prework anterior (`sqx-main-v1-556c2aa4…`, cola `sqx-main-queue` sin pollers) quedó RUNNING pese a cancel solicitada; `TerminateWorkflow` server-side lo cerró. Criterio operativo para teardowns DEV.
5. **Knob muerto:** `sqx.worker.max_parallel` no es leído por `sqx/cmd/sqx-worker` actual (solo por el path legacy `internal/tasks/sqx_worker_refactored.go`); el runbook anexo lo documenta como si fuera efectivo. El aislamiento de concurrencia real hoy = un solo proceso worker.

## Clasificación propuesta (para hygiene/Kaizen)

- known_error: ssh-mcp session pool (evidencia 2 corridas).
- runbook update: transferencia de binarios flota→Daedalus (mechanism scp + revocación) y teardown Temporal con terminate.
- repo chore (symphony): commit de `go.work.sum` podado + decisión sobre `max_parallel` (cablear o retirar del runbook).

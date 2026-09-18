---
type: session_feedback
schema_version: 1
scope: system-1
created: "2026-09-18"
updated: "2026-09-18"
area: "[[Echo]]"
project: "[[Echo + Echo Forge — Deferred Certification Backlog]]"
entities:
  - "[[Echo Forge]]"
  - "[[Aranea]]"
related:
  - "[[aranea-agent-dev]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
aliases: []
confidence: high
source_session:
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session-feedback
  - scope/system-1
---

# 2026-09-17-f05c-cert-f04-01-rerun3-session-feedback

- **Fricción MCP SSH (`-32001 Session not found or expired`):** el server aranea-ssh perdió todo su session store a las ~23:56Z durante la ventana crítica post-fallo del run (worker log de Zeus y evidence publisher Windows inalcanzables por ~1 h; `list-connections` fallaba igual que `run-command`, sin ruta de re-inicialización desde el agente). Se recuperó solo ~00:57Z. Pain pattern candidate: un outage del MCP SSH durante una certificación deja sin observación física a toda la flota (Linux + Windows) simultáneamente; mitigación usada: frontend Temporal directo con binario scratch read-only.
- **MCP Temporal RO apunta a namespace distinto de `sqx-prop`:** `describe`/`list` no ven ningún workflow del stack productivo (ni siquiera históricos conocidos del RERUN); los perfiles ETCD declaran `sqx-prop` como namespace productivo. Si el profile `aranea` del server apuntara a `sqx-prop`, el MCP cubriría solo el error literal sin necesidad del binario scratch.
- **Observabilidad sin ingestión symphony:** Loki no tiene streams del worker log de symphony (`/var/log/symphony/symphony-worker.log`) y el collector OTLP (`192.168.31.45:4317`) rechaza conexiones (visto en los propios logs de `release-authority`). La trazabilidad de errores literales de actividades dependió 100% de canales alternativos.
- **Limitaciones ya conocidas y recurrentes (no nuevas):** MinIO-RO 403 en bucket `sqx-strategies` y Mongo forge RO `-32003` — registradas en EXEC/RERUN; persisten en RERUN-3.

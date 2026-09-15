---
type: session_summary
schema_version: 1
date: 2026-09-15
project: "[[HERMES — Bootstrap & Self-Sufficiency]]"
area: "[[Aranea]]"
source_session:
tags:
  - kind/session-summary
  - area/aranea
  - tech/mcp
---

# 2026-09-15 — B3.3 `aranea-observability-ro` CLOSED (summary)

- **Resultado:** `B3.3 PASS` end-to-end. Desbloqueado por el owner (SA Viewer `mcp-observability-ro` + token `glsa_…`); transferencia stdin-only Daedalus→mcps por management paths certificados (sha íntegro en 3 puntos, cero impresión). Deploy backend `grafana/mcp-grafana@sha256:f87fa67a…` + proxy canónico `:3009`; cert server **PASS 12/12** (401 · initialize · superficie 22 exacta · negative write · Prometheus/Loki/Grafana probes bounded reales · leak clean); consumer Daedalus **smoke PASS** (entry `${env:ARANEA_OBSERVABILITY_MCP_RO_BEARER}`, bearer stdin); rollback byte-identical probado (`1ba82805…`→`4a8222d5…`); drift cero 3000–3008.
- **Desvíos corregidos con evidencia:** red pre-stageada `--internal` no publica puertos host y sin egress a Grafana → bridge estándar (patrón de las 5 familias); token file `600 root:root` ilegible por uid1000/gid999 de la imagen → `0:999`+`640`. Quirks 1.4.2 documentados en el runbook.
- **SoT:** runbook `30-resources/runbooks/aranea-observability-mcp.md` (nuevo) · router [[aranea-mcps-expert]] · inventario `aranea-mcp-capability-plane` · change_log `80-agents/journal/logs/2026-09-15-b33-observability-ro-closed.md` (la nota BLOCKED queda superseded).
- **Pendiente owner-side (documentado, no bloquea):** alta de `ARANEA_OBSERVABILITY_MCP_RO_BEARER` en el chain env KDE de kor (configured-vs-exposed).
- **Reanudación:** B3 cerrado → siguiente **B4 human-exit audit** ([[HERMES — Bootstrap & Self-Sufficiency]] § B4). Echo/Forge permanece cerrado hasta B4.

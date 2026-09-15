---
type: raw_session
schema_version: 1
date: 2026-09-15
project: "[[HERMES — Bootstrap & Self-Sufficiency]]"
area: "[[Aranea]]"
source_session:
tags:
  - kind/raw-session
  - area/aranea
  - tech/mcp
---

# 2026-09-15 — B3.3 `aranea-observability-ro` BLOCKED (raw)

- Solicitud owner: golden deploy B3.3 con manager/upstream/tool surface/auth congelados (`grafana/mcp-grafana` 1.4.2, RO estricto, endpoint :3009, sin tocar ARGUS ni Echo/Forge). Session close + feedback obligatorio.
- Secuencia: bootstrap cold (constitución, bootstrap, INDEX, registry routers, perfil global) → discovery (skill operador, plane + arquitectura, runbook capability-plane, ACCESS-CERTIFICATION H1/H2, docs ARGUS legacy/real, runbook Traefik §ARGUS) → PINNED upstream (release v1.4.2 → commit `b56dceea` → digest índice `f87fa67a…`/amd64 `9a10fd78…`; flags 1.4.2; `GRAFANA_SERVICE_ACCOUNT_TOKEN_FILE`) → baseline `mcps` (3000–3008 ocupados, 3009 libre; registry alcanzable; 4G disco/2.3G RAM) → target proof ARGUS (qemu/160 = `192.168.31.60`: Grafana 12.1.1 healthy 401-sin-token, Prometheus `up` real, Loki ready) → authority discovery credencial (0 hits en `/opt/mcp`, `.env` Hermes, chain Daedalus) → pre-staging AUTO idempotente (dirs + red `mcp-observability`) → **BLOCKED** → OWNER ACTION BUNDLE → Agents-OS updates.
- Hallazgos: tag Docker Hub es `1.4.2` sin `v` (404 previo fue naming propio); `mcps-ops` loguea argv completo (token jamás por argv); `terminal` bloquea/flaggea URLs con IP RFC1918 como MEDIUM y un timeout de aprobación abortó un comando combinado (no reintentado); `--enable-query` 1.4.2 = SQL crudo (prohibido); dashboard write-class tools de 1.4.2 (`get_dashboard`, `list_dashboard_versions`, `get_dashboard_by_uid`) son RO por diseño.
- Veredicto: `B3.3 BLOCKED` — única causa: inexistencia de credencial Grafana read-only (crear SA Viewer excede autoridad). Ningún despliegue; pre-staging revertible documentado.
- Artefactos: change_log `2026-09-15-b33-observability-ro-blocked-credential` · bitácoras Bootstrap + Access Plane · skill operador +3 invariantes · bundle `workspace/owner-action-bundle.md`.

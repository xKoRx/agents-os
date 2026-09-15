---
type: change_log
schema_version: 1
scope: session
created: "2026-09-15"
updated: "2026-09-15"
area: "[[Aranea]]"
project: "[[HERMES — Bootstrap & Self-Sufficiency]]"
entities:
  - "[[HERMES — Bootstrap & Self-Sufficiency]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
related:
  - "[[mcp-access-plane-operations]]"
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
  - scope/session
---

# 2026-09-15-b33-observability-ro-closed

%% Routing: area/project/entities/related usan links canónicos. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - `30-resources/runbooks/aranea-observability-mcp.md` (created: runbook de familia observability)
  - `30-resources/agents/skills/aranea-mcps-expert/SKILL.md` (updated: related/aliases/runbook + fila PROD-RO en tabla de ambientes)
  - `30-resources/runbooks/aranea-mcp-capability-plane.md` (updated: inventario de capabilities + endpoints certificados + frontmatter updated)
  - `10-projects/Aranea/agentes/HERMES — Bootstrap & Self-Sufficiency.md` (updated: B3.3 cerrado PASS, bitácora, tareas B3.3/B3.4)
  - `80-agents/journal/logs/2026-09-15-b33-observability-ro-blocked-credential.md` (updated: BLOCKED → superseded por cierre)

## Motivo

- Cerrar B3.3 (golden configure/deploy) del proyecto HERMES — Bootstrap & Self-Sufficiency sobre la necesidad real de lectura observability (Grafana/Prometheus/Loki de ARGUS), desbloqueada por el OWNER ACTION BUNDLE aplicado (SA Viewer `mcp-observability-ro` + token `glsa_…` entregado por stdin a disco en `mcps`).

## Transferencia de la credencial (desvío owner-side documentado)

- El owner dejó el token temporalmente en `hermes-ops@daedalus:/home/hermes-ops/grafana-observability-ro.token` (600) y dirigió usar los management paths certificados en vez de root sobre `mcps`. Transferencia stdin-only: `ssh daedalus-ops 'cat token'` → pipe → `mcps-ops 'cat > /tmp/…'` → `sudo install` a `runtime/secrets/grafana_service_account_token`. Integridad sha256-16 (`cbac842f…`) verificada en los tres puntos; valores jamás impresos ni en argv (wrapper `mcps-ops` loguea argv). Temporales eliminados y ausencia verificada en ambos hosts.

## Resolución aplicada

- Backend `observability-mcp-ro`: `grafana/mcp-grafana@sha256:f87fa67a…` (1.4.2, digest verificado en pull), flags `--transport streamable-http --endpoint-path /mcp --disable-write --enabled-tools search,datasource,prometheus,loki,dashboard`, env `GRAFANA_URL` + `GRAFANA_SERVICE_ACCOUNT_TOKEN_FILE`, red `mcp-observability` (bridge, sin host port), `restart=unless-stopped`.
- Proxy `observability-mcp-auth-ro`: Nginx digest canónico `56168782…`, `:3009->8080`, template canónico + `proxy_set_header Host 127.0.0.1:8000`, bearer `daedalus.bearer` (openssl rand -hex 32 server-side, 600).
- Desvío de arquitectura: la red pre-stageada era `--internal`; Docker no publica puertos host en redes internal y el backend requiere egress a Grafana → red recreada como bridge normal (patrón idéntico a las 5 familias). El desvío interno propuesto (red egress dedicada) se eliminó tras verificarlo innecesario; cero residuo.
- Dos defectos míos corregidos con evidencia: (1) deploy inicial sin las env de contrato → recreado; (2) permisos del token file 600 root:root ilegibles por el usuario de la imagen (uid 1000/gid 999) → `chown 0:999 + chmod 640`; diagnóstico por log WARN del backend, no por conjetura.

## Validación

- Certificación server-side (sonda con aserciones duras): unauth 401 · initialize 200 (`mcp-grafana`) · tools/list = 22 exactas (superficie congelada) · negative write `delete_dashboard` → -32602 · `query_prometheus up` instant bounded → 5 series reales · labels Prometheus/Loki PASS · `query_loki_stats` {job="echo-core"} → conteos reales · `query_loki_logs` → líneas reales de echo · `check_datasources_health` → 3/3 OK · `search_dashboards` → 0 (estado real) · leak check `glsa_` CLEAN. **CERT PASS 12/12.**
- Consumer: entry `aranea-observability-ro` en `/home/kor/.cursor/mcp.json` (ref `${env:ARANEA_OBSERVABILITY_MCP_RO_BEARER}`, sin bearer literal) + smoke desde Daedalus resolviendo la config real (bearer sólo stdin): initialize/tools-list-22/prometheus/health/negative-write/leak → **CONSUMER-SMOKE PASS**.
- Rollback demostrado: remove → sha256 `1ba82805…` byte-identical al baseline → re-add → sha256 `4a8222d5…` byte-identical → re-smoke PASS.
- Drift cero: containers/redes/ports 3000–3008 + ssh-mcp + portainer idénticos al baseline; red egress temporal eliminada; `/tmp` limpio en mcps y Daedalus.
- Quirks 1.4.2 documentados en el runbook (endTime obligatorio, stepSeconds en range, Host header anti-rebind, permisos token file, ERROR de arranque esperado, serverInfo "(devel)").

## Pendiente owner-side (configured vs exposed, no bloquea el cierre técnico)

- Alta de `ARANEA_OBSERVABILITY_MCP_RO_BEARER` en el chain env KDE de kor (`plasma-workspace/env/aranea-mcp.sh` → `.config/mcp/aranea-env.sh`), mismo mecanismo que las 9 variables existentes; los secret files de kor son inaccesibles para `hermes-ops` por diseño. Hasta entonces Cursor no resuelve la entry (config publicada y certificada; smoke usa bearer por stdin).

## Compartibilidad

- Patrón B3.3 replicable para próxima familia: baseline → digest-pinned deploy → cert server con superficie congelada → consumer onboarding B2 → rollback byte-identical → SoT. Detalle de quirks por servicio en el runbook de familia.

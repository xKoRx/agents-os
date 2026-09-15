---
type: runbook
schema_version: 1
scope: area
created: "2026-09-15"
updated: "2026-09-15"
area: "[[Aranea]]"
project: "[[AGENT-PLATFORM - MCP Access Plane]]"
application:
entities:
  - "[[Aranea]]"
  - "[[Echo]]"
related:
  - "[[aranea-mcps-expert]]"
  - "[[aranea-mcp-capability-plane]]"
  - "[[AGENT-PLATFORM - MCP Access Plane - Architecture]]"
  - "[[aranea-mcp-plane-operator]]"
aliases:
  - runbook Observability MCP Aranea
  - aranea observability mcp
  - mcp grafana
  - aranea-observability-ro
  - mcp prometheus
  - mcp loki
confidence: verified
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/area
  - area/aranea
  - tech/mcp
  - tech/grafana
  - tech/prometheus
  - tech/loki
  - action/mcp-observability
---

# aranea-observability-mcp

## Propósito

Operar la lectura read-only de observabilidad de Aranea (Grafana, Prometheus, Loki en ARGUS) a través del capability `aranea-observability-ro` del MCP Access Plane. El routing agent-facing vive en [[aranea-mcps-expert]], la mecánica común del plano en [[aranea-mcp-capability-plane]] y la arquitectura/deployment común en [[AGENT-PLATFORM - MCP Access Plane - Architecture]].

Este capability es **Viewer/read-only estricto**: no existe superficie de escritura en el backend desplegado (allowlist de toolsets + `--disable-write`), no es una surface de administración de Grafana ni un sustituto del stack de observabilidad (dashboards/alertas se gestionan en ARGUS, fuera del plano MCP).

## Capability certificada

| Ambiente | Capability | Endpoint | Autoridad | Estado |
|---|---|---|---|---|
| PROD-RO (lectura) | `aranea-observability-ro` | `http://mcps.lab.aranea.cl:3009/mcp` | read-only sobre Grafana/Prometheus/Loki de ARGUS | PASS / CLOSED end-to-end |

## Upstream pinneado

```text
repo:    grafana/mcp-grafana
release: v1.4.2 (tag Docker Hub sin prefijo 'v': 1.4.2)
commit:  b56dceea
digest:  sha256:f87fa67a561f7b3deb412402887117bd1e9f1f7a8695935d27c498543ab3458b (índice; amd64 9a10fd78…)
flags:   --transport streamable-http --endpoint-path /mcp --disable-write
         --enabled-tools search,datasource,prometheus,loki,dashboard
env:     GRAFANA_URL=http://192.168.31.60:3000
         GRAFANA_SERVICE_ACCOUNT_TOKEN_FILE=/run/secrets/grafana_service_account_token
```

`--enable-query` queda prohibido (amplía superficie). El toolset `alert`/admin no está habilitado.

## Target upstream verificado

```text
VM:      argus (qemu/160), LAN 192.168.31.60
Grafana: 12.1.1 en :3000 (healthy, exige token)
Datasources (vía API con el SA Viewer):
  Prometheus  uid PBFA97CFB590B2093 (default)
  Loki        uid P8E80F9AEF21F6940
  Jaeger      uid jaeger_uid (visible; SIN toolset jaeger habilitado en el MCP)
Credencial: Service Account `sa-1-mcp-observability-ro` (login `sa-1-mcp-observability-ro`),
rol Viewer, token `glsa_…` gestionado por el owner; negativas write 403/403 verificadas.
```

## Deployment certificado

Topología:

```text
Cursor / Daedalus
  -> Authorization: Bearer *** token
  -> mcps.lab.aranea.cl:3009/mcp
  -> observability-mcp-auth-ro (Nginx, :3009->8080)
  -> observability-mcp-ro:8000 (red mcp-observability, sin host port)
  -> Grafana API http://192.168.31.60:3000 (egress LAN desde el backend)
```

Containers/red:

```text
backend: observability-mcp-ro      grafana/mcp-grafana@sha256:f87fa67a…  restart=unless-stopped
proxy:   observability-mcp-auth-ro nginx@sha256:56168782… (digest canónico del plane)  restart=unless-stopped
network: mcp-observability (bridge, NO --internal: el backend necesita egress a Grafana y
         Docker no publica puertos host en redes internal)
```

Paths server-side (ubicación, jamás contenido):

```text
/opt/mcp/observability/runtime/proxy/mcp.conf.template                    (template Nginx canónico + proxy_set_header Host 127.0.0.1:8000)
/opt/mcp/observability/runtime/proxy-secrets/daedalus.bearer              (bearer cliente->proxy, 600 root)
/opt/mcp/observability/runtime/secrets/grafana_service_account_token      (upstream, 640 root:999 — ver quirk de permisos)
```

## Tool surface certificada

`tools/list` server-side devolvió exactamente 22 tools (2026-09-15):

```text
analyze_loki_labels          check_datasources_health    get_dashboard_by_uid
get_dashboard_panel_queries  get_dashboard_property      get_dashboard_summary
get_datasource               list_dashboard_versions     list_datasources
list_loki_label_names        list_loki_label_values      list_prometheus_label_names
list_prometheus_label_values list_prometheus_metric_metadata list_prometheus_metric_names
query_loki_logs              query_loki_patterns         query_loki_stats
query_prometheus             query_prometheus_histogram  search_dashboards
search_folders
```

No existe tool de escritura (`create_/update_/delete_` ausentes de la superficie). Negative probe: `delete_dashboard` → `-32602 tool not found`.

## Quirks verificados 1.4.2 (no tratar como fallas)

```text
1) query_prometheus: endTime es OBLIGATORIO (vacío -> parse error tNOW/tDIGIT);
   queryType=range exige stepSeconds; para lectura puntual usar queryType=instant + endTime.
2) La imagen corre como usuario no-root (uid 1000/gid 999): el token file debe ser
   640 root:999 (grupo NUMÉRICO, el gid no existe como grupo con nombre en el LXC).
   Con 600 root:root el backend loguea "Failed to read GRAFANA_SERVICE_ACCOUNT_TOKEN_FILE,
   ignoring" y las tools fallan con 401 upstream.
3) El backend valida el header Host (anti-DNS-rebinding): el proxy DEBE enviar
   proxy_set_header Host 127.0.0.1:8000 (patrón del template postgres mcp-ro-final);
   sin ello responde 403 "forbidden: host not allowed".
4) Mcp-Session-Header en el PROPIO initialize devuelve cuerpo vacío; usar session id
   sólo desde la segunda llamada (init-only pattern de las sondas certificadas).
5) Al arranque loguea ERROR "SECURITY: serving on a non-loopback address with NO caller
   authentication" en 0.0.0.0:8000: warning upstream esperado; el boundary real es el
   proxy bearer en la red dedicada.
6) serverInfo.version reporta "(devel)" aunque la imagen sea el digest 1.4.2 pinneado;
   la evidencia de versión es el digest de imagen, no ese string.
```

## Certificación material 2026-09-15

```text
unauthenticated :3009/mcp -> 401
authenticated initialize   -> 200 + Mcp-Session-Id (server mcp-grafana)
tools/list                 -> 22 exactas (superficie congelada)
negative write             -> BLOCKED (-32602 tool not found)
query_prometheus up (instant, now-1h) -> 5 series reales (job otelcol entre ellas)
list_prometheus_label_names (limit 5) -> PASS
list_loki_label_names      -> 6 labels (job, level, host, service_name…)
query_loki_stats {job="echo-core"}    -> streams/chunks/entries/bytes reales
query_loki_logs {job="echo-core"}     -> líneas reales (echo mt4-ftmo observado)
check_datasources_health   -> 3/3 datasources OK
search_dashboards (limit 5) -> 0 dashboards (estado real del Grafana: sin dashboards)
leak check (glsa_ en respuestas) -> CLEAN
Consumer smoke desde Daedalus (config real + bearer por stdin) -> PASS
Rollback demostrado: remove entry -> sha256 byte-identical al baseline (1ba82805…) -> re-add
-> sha256 byte-identical al post-add (4a8222d5…) -> re-smoke PASS
Drift: 9 capabilities 3000-3008 + ssh-mcp + portainer byte-idénticos al baseline.
```

## Cliente Daedalus / Cursor

```text
entry mcp.json: aranea-observability-ro
url:            http://mcps.lab.aranea.cl:3009/mcp
Authorization:  Bearer ${env:ARANEA_OBSERVABILITY_MCP_RO_BEARER}
env var:        ARANEA_OBSERVABILITY_MCP_RO_BEARER  (64 hex)
```

Loader: mismo chain KDE del resto (`~/.config/plasma-workspace/env/aranea-mcp.sh` → `~/.config/mcp/aranea-env.sh`). Residual owner-side CERRADO 2026-09-15 (B4, sin owner): `ARANEA_OBSERVABILITY_MCP_RO_BEARER` persistida por Hermes — secret file `~kor/.config/aranea/secrets/hermes-managed/observability-mcp-ro.bearer` (640 + ACL u:kor:r--) + bloque `if [ -r ]` en `aranea-env.sh` (mecanismo completo en [[aranea-mcp-capability-plane]] § Consumer onboarding managed). Los secret files originales de kor siguen inaccesibles para `hermes-ops`; chain-cert PASS resolviendo la entry real de `mcp.json` (rollback byte-identical y re-aplicación convergente demostrados).

## Revoke path

```text
1) Revocar el token en Grafana (UI ARGUS -> Service accounts -> token)  # corte inmediato upstream
2) En mcps:
   sudo docker rm -f observability-mcp-ro observability-mcp-auth-ro
   sudo rm /opt/mcp/observability/runtime/secrets/grafana_service_account_token \
           /opt/mcp/observability/runtime/proxy-secrets/daedalus.bearer
   # opcional (rollback total de la familia):
   sudo docker network rm mcp-observability
   sudo rm -rf /opt/mcp/observability
3) En Daedalus: remove de la entry (operador B2) -> sha256 byte-identical verificado.
El pre-staging no afecta las capabilities 3000-3008.
```

## Troubleshooting

```text
401 en :3009            -> bearer cliente->proxy o env del consumer; no tocar Grafana.
403 "host not allowed"  -> proxy sin proxy_set_header Host 127.0.0.1:8000; revisar template.
Tools con 401 upstream  -> token file ilegible por el backend (quirk 2) o token revocado
                           en Grafana; verificar WARN "Failed to read …TOKEN_FILE" en logs
                           y GET /api/user con el valor server-side (nunca imprimirlo).
"stepSeconds must…"     -> queryType=range sin stepSeconds; usar instant o agregar step.
"parsing end time"      -> falta endTime en query_prometheus.
Entry en Cursor sin tools -> env var no heredada (revisar chain/secret file de la capability) o proceso sin restart.
Capacidad de consulta   -> toda query es bounded: fijar endTime/limit explícito.
```

## Hard Rules

- Aranea-only; nunca usar contra MELI/corporativo.
- La capability es lectura: no ampliar toolsets ni habilitar `--enable-query`, `alert` o admin sin certificación explícita y decisión de [[aranea-mcps-expert]].
- No crear mutadores sobre ARGUS vía este capability; la administración de Grafana pertenece al owner/stack ARGUS.
- No publicar el backend al host ni mover la familia a otra red sin evidencia material (el backend requiere egress a Grafana: red bridge dedicada, no --internal).
- El token upstream (`glsa_…`) y el bearer del proxy nunca se imprimen ni documentan; sólo paths/sha.
- Toda query contra Prometheus/Loki es bounded (endTime/limit explícitos).
- Cambios de imagen sólo por digest pinneado; nunca por tag flotante.

## Validación

```text
Environment:            PROD-RO (lectura sobre stack de observabilidad ARGUS)
Capability:             aranea-observability-ro
Endpoint:               http://mcps.lab.aranea.cl:3009/mcp
Proxy unauthenticated:  401
MCP initialize/tools:   PASS / 22 exactas
Negative write:         BLOCKED
Prometheus/Loki/Grafana probes: PASS (bounded, datos reales)
Backend host port:      none
Consumer:               Daedalus/Cursor entry publicada; chain-cert PASS (env resuelta del chain persistente, B4 2026-09-15)
Owner-side residual:    NONE ROUTINE — alta de ARANEA_OBSERVABILITY_MCP_RO_BEARER en chain kor ejecutada por Hermes (B4, sin owner)
Secrets exposed:        no
E2E:                    PASS / CLOSED (2026-09-15)
```

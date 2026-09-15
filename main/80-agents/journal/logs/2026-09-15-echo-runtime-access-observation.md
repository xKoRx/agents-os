---
type: change_log
schema_version: 1
scope: session
created: "2026-09-15"
updated: "2026-09-15"
area: "[[Aranea]]"
project: "[[HERMES — Agent Access Operations]]"
entities:
  - "[[HERMES — Agent Access Operations]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
  - "[[Echo]]"
related:
  - "[[ACCESS-CERTIFICATION]]"
  - "[[Echo — Access & Physical Capability Matrix]]"
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

# 2026-09-15-echo-runtime-access-observation

%% Routing: area/project/entities/related usan links canónicos. %%

## Cambio

- **Tipo:** updated + created
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo — Access & Physical Capability Matrix.md` (updated: reconciliación de gaps stale 001/002/003/007 → RESUELTOS; GAP-ECHO-004 redefinido con target real; gate E-02 Gateway physical actualizado; frontmatter updated)
  - `10-projects/Aranea/AGENT-PLATFORM/agentes/workstreams/ACCESS-CERTIFICATION.md` (updated: veredicto ampliado; sección "Observación runtime Echo — 2026-09-15"; tabla de superficies sin capacidad; conclusión; frontmatter)
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (updated: delta de readiness 2026-09-15 añadido sobre el de 2026-09-14; frontmatter)
  - `10-projects/Echo/agentes/Echo — E-02 Control Safety, Auth and Journal Recovery.md` (updated: bitácora 2026-09-15 sin cambio de gates)
  - `10-projects/Aranea/agentes/HERMES — Agent Access Operations.md` (updated: A0.1/Bitácora/Decisiones)
  - `30-resources/runbooks/aranea-ssh-mcp.md` (updated: profile viewer `echo-runtime-prod` staged + quirk de orden connect→policy + finding host-key duplicada)
  - `30-resources/agents/skills/aranea-mcps-expert/SKILL.md` (updated: fila viewer `echo-runtime-prod` PENDING en tabla de ambientes)

## Motivo

- Primer workload A0 de [[HERMES — Agent Access Operations]]: reconciliar los gaps Echo contra el Access Plane ACTUAL y resolver el blocker de observación runtime Gateway/Core/Bridge reutilizando `aranea-ssh` primero. Sin instalar servicios del homelab, sin tocar product source, sin ejecutar trading.

## Resultado

- **Gaps stale reconciliados (sin auditoría global):** GAP-ECHO-001/002/003 (Hasura/Kafka/Flink) y GAP-ECHO-007 (observabilidad) RESUELTOS — las capabilities existían certificadas desde 2026-09-12/13 y la matriz de 2026-09-14 no las vio; GAP-ECHO-007 cerrado además por `aranea-observability-ro` (:3009, PASS 12/12 + consumer PASS, B33/B4). Evidencia en [[ACCESS-CERTIFICATION]] y la matriz.
- **Target runtime Echo resuelto con source/runtime proof:** `.211` MUERTO (22/8090 closed desde mcps). Runtime vivo = PROD `192.168.31.71` = `prod.echo.gateway.lab.aranea` (PTR real; `GET /health` 200 `{"status":"ok"}`; 8082 cerrado; 404 Go net/http; logs `env=production host=echo service=echo-core`). DEV runtime NOT_DEPLOYED (docker-echo-dev: sólo Flink/Hasura/Portainer, verificado vía `docker-echo-dev-operator`). Gateway/Core/Bridge comparten ese host PROD (Gateway HTTP vivo; Core vía StateFun/PG; ningún Bridge localizado — pendiente viewer).
- **Capability (manager decision reuse-first):** `aranea-ssh` EXTENDIDO con profile VIEWER `echo-runtime-prod` (`echo-dev@192.168.31.71:22`, `readOnly=true`, `role=viewer`, `group=prod`, host key pinneada, keyRef existente `echo-dev`). SSH básicamente puede expresar toda la evidencia pedida (identity/health/logs/listeners/fs-meta vía read-command allowlist + curl local read-only si permitido): NO se requiere capability nueva. Config `22664e96…` → `047d00e7…` con backup byte-identical en `mcps:/tmp/config.toml.pre-echo-runtime-prod`; crash-loop transitorio por modo/ownership del config corregido (600, 65532:65532 — el container lee como uid 65532, no como el dueño original root del bind).
- **PENDING_OWNER_GATE (único, GATED):** instalar `mcps:/opt/mcp/ssh/keys/echo-dev.pub` en `authorized_keys` de `echo-dev` en `.71` (12 combinaciones key×usuario probeadas → Permission denied; ninguna identidad del plane o local está autorizada allí). Post-instalación: recertificar identity/health/logs/listeners + negative `run-command` (H2 deny será observable; el orden upstream es connect→policy y hoy falla cerrado en connect).
- **Observación runtime PROD ya operativa SIN owner action:** `aranea-observability-ro` — `query_loki_logs {job="echo-core"}` → líneas reales en vivo (`account_sync: flushed snapshots`, `inst_snapshot: updated` ORION GOLD, `telemetry.go` de `xKoRx/echo/v3`); `query_prometheus up` → 5 series. Quirks 1.4.2: args `logql/startRfc3339/endRfc3339/expr` + `datasourceUid` obligatorio.
- **Enforcement H2 re-certificado consumer-side (Daedalus real, RESULT: PASS):** `run-command` en viewer alcanzable → POLICY_DENIED; viewer read PASS; 7 perfiles visibles; cero secrets.
- **Finding:** host key ED25519 de `.71` IDÉNTICA a `sqx-zeus` (`zPHN…wdfU`) — clon sin regenerar; rotación owner-side sugerida (no bloqueante).

## Validación

- Consumer cert Daedalus EXIT=0 (surface 11 tools, list-connections, negatives H2, pending-gate clasificado).
- Server smoke list-connections: 7 perfiles, viewer visible, sessions=0.
- Sonda observabilidad: RESULT PASS (Loki + Prom, bounded).
- Drift: único delta en mcps = profile staged (047d00e7) + backup; resto del plane sin tocar; `/tmp` limpio en mcps/Daedalus/local; container ssh-mcp healthy.
- Sin mutación en `.71`; sin secrets en chat/vault (keys/bearers sólo por referencia/stdin).

## Pendiente

- Owner: instalar public key en `.71` (y opcionalmente rotar su host key). Después: certificación viewer completa (identity/health/logs/listeners/negative) → cierre GAP-ECHO-004 y trigger pleno CERT-E04-01.
- Recertificación con la matriz: E-02 puede ejecutar ya sus verificaciones físicas Hasura/Kafka/Flink contra capabilities certificadas (no ejecutadas en esta sesión por scope).

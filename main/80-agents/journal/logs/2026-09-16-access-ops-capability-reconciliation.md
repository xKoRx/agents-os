---
type: change_log
schema_version: 1
scope: session
created: "2026-09-16"
updated: "2026-09-16"
area: "[[Aranea]]"
project: "[[HERMES — Agent Access Operations]]"
entities:
  - "[[HERMES — Agent Access Operations]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
  - "[[Echo]]"
  - "[[Echo Forge]]"
related:
  - "[[ACCESS-CERTIFICATION]]"
  - "[[Echo — Access & Physical Capability Matrix]]"
  - "[[Echo + Echo Forge — Deferred Certification Backlog]]"
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

# 2026-09-16-access-ops-capability-reconciliation

%% Routing: area/project/entities/related usan links canónicos. %%

## Cambio

- **Tipo:** updated (1 archivo Sistema 2) + extracción read-only.
- **Archivo(s):**
  - `10-projects/Aranea/agentes/HERMES — Agent Access Operations.md` (updated: Bitácora 2026-09-16b — reconciliación de capability requests Echo/Forge).

## Motivo

- Workload owner: identificar el blocker MCP vigente y demostrable que impide trabajar a un agente de Echo o Echo Forge, reconciliando solicitudes reales, backlog, roadmap e inventario certificado. Sesión estrictamente de extracción: sin gates, sin certificaciones, sin implementación.

## Fuentes leídas

- `agents-os.md`, `agent-constitution.md`, bootstrap, `agents-os-session-close` (guía Agents-OS).
- `10-projects/Aranea/agentes/HERMES — Agent Access Operations.md` (roadmap A0–A5, bitácora, decisiones A-D01…A-D08).
- `10-projects/Aranea/AGENT-PLATFORM/agentes/AGENT-PLATFORM - MCP Access Plane.md` (inventario 10 capabilities, bitácora).
- `10-projects/Aranea/AGENT-PLATFORM/agentes/workstreams/ACCESS-CERTIFICATION.md` (runs 09-14/15/16, GAP-ECHO-010, E-02 CLOSED).
- `10-projects/Echo/agentes/Echo — Access & Physical Capability Matrix.md` (gaps, roadmap matrix).
- `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (clases A/B/C, triggers).
- `10-projects/Echo/agentes/Echo Forge — F-04 Magic allocation, version seal and handoff.md` (T2.11–T2.13, viewer Windows).
- `10-projects/Echo/agentes/Echo Forge — F-05-I Cohesive release and read surfaces.md` (read models sobre PG/Mongo/MinIO/Temporal cols — source, no MCP).
- `10-projects/Echo/agentes/Echo — E-02 Control Safety, Auth and Journal Recovery.md` (bitácora 09-16, E02 CLOSED).
- `30-resources/agents/skills/aranea-mcps-expert/SKILL.md` (matriz de ambientes vigente).
- Change logs 2026-09-15/16 relevantes.

## Resultado

- **FIRST BLOCKER: GAP-ECHO-010** (P1 Access Plane) — único blocker vigente con evidencia demostrable y de fecha 2026-09-16 que impide trabajo agent-first confiable: proxies nginx-wrapped (ssh :3000, hasura :3006, flink :3008) entran en modo async-202 sin `Mcp-Session-Id` tras churn de sesiones, bloqueando clientes stateless (init-per-run). Workaround certificado (restart backend proxy); causa raíz mcp-proxy 6.7.16 sin diagnosticar. Impacto: TODA ejecución agent-side de gates sobre el plane.
- Needs evaluadas: etcd scoped (GAP-ECHO-005) = dependencia de roadmap para E-06/E-11/E-12 sin solicitud runtime activa; viewer Windows MT5 read surface = solicitud explícita F-04 2026-09-13 pero lane clase C deferred; Temporal visibility = T5 DEFERRED + alternativa existente (SSH logs + read models PG) cubre la evidencia actual; MinIO artifacts = solo soporte temporal DEV probado, NEEDS_SOURCE_PROOF.
- E-02 handoff verificado en disco: branch `feature/e02-control-safety-journal-recovery` @ `f7ddea18` preservado (bitácora 09-16 sesión 2, change log `2026-09-16-e02-closed`, matriz actualizada). Sin delta de sincronización detectado.

## Validación

- Read-only: cero mutaciones de infraestructura; cero certificaciones; cero secretos impresos.
- Doble fuente por hecho: cada fila de la matriz reconciliada contrasta proyecto + certification note fechada.

## Pendiente

- Decisión del manager sobre next workload (recomendación en informe: golden repair GAP-ECHO-010 = A1.1, AUTO).
- NEEDS_SOURCE_PROOF para etcd/MinIO si el manager los prioriza.

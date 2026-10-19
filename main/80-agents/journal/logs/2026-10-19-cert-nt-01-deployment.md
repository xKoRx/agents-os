---
type: change_log
schema_version: 1
scope: session
created: "2026-10-19"
updated: "2026-10-19"
area:
project:
application:
entities: []
related: []
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

# 2026-10-19-cert-nt-01-deployment

## Cambio

- **Entidad/proyecto:** [[Echo Futures — Runtime Pools]] — planner + nuevo artefacto de certificación.
- **Qué cambió:** (1) planner: decisión G4 `accepted` recibida del Primary Manager persistida (estado/gates/tareas/bitácora), nuevo ledger «Certificación operativa CERT-NT-01» (matriz C0, gates C0–C5, evidencia C1/C2/C5, estado final CERT_NT_BLOCKED, bitácora ×2); normalización de rutas de workspace externo a forma `~/` (validate_plan errors=0). (2) nuevo artefacto `10-projects/Echo Futures/artifacts/runtime/cert-nt-01/OWNER-CHECKLIST-CERT-NT-01.md` (2 acciones Owner para reanudar C2–C4). (3) agent-runs ×3 (A despliegue, C verificación, submanager) y feedback de sesión.
- **Motivo y autoridad:** mandato CERT-NT-01 del Primary Manager (G4 accepted sobre `b13ef43d`); etapa operativa post S01–S04; sin merge, sin egress real, sin cuentas comerciales del Owner.
- **Validación:** validate_plan 0/0; verificación independiente C5_READY (`~/aranea/work/cert-nt-01-c/HANDOFF-C.md`); controles de bloqueo re-verificados por cliente crudo.
- **No tocado:** producto `xKoRx/echo` (rama y master), Echo PROD, flota Forge, perfiles NT del Owner, claves ETCD ajenas.

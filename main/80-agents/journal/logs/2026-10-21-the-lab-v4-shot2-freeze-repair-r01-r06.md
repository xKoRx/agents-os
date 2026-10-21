---
type: change_log
schema_version: 1
created: 2026-10-21
project: "[[The Lab]]"
tags:
  - kind/change-log
  - project/the-lab-v4
---

# 2026-10-21 — The Lab V4 Shot 2: paquete de freeze revisión 2 (reparación R01–R06)

- **Qué cambió:** en `10-projects/Echo/The Lab/V4 — Shot 2/`, `1 — TECHNICAL_FREEZE_PACKET.md` se reemplaza por la REVISIÓN 2 (estado pedido `TECHNICAL_FREEZE_READY_V2`) respondiendo el dictamen Manager `TECHNICAL_FREEZE_REPAIR_REQUIRED` sobre el blob `6f1d3982`; se crea `2 — Preflight Evidence (U01–U06).md` (evidencia sanitizada y re-verificada 2026-10-21 con 4 correcciones a los findings) y `0 — Submanager State.md` se actualiza (gate, baselines, correcciones, restricciones, siguiente acción).
- **Contenido material de la reparación:** matriz de adopción acotada de `feature/e04-dev-ingest-recovery@4aad647b` (5 commits; seeds de master se preservan por superiores; edición in-place de 061 rechazada y su intención trasladada a la migración de retiro legacy 070 con guard de ownership); plan de migraciones reconciliado 067→068→069→070 con prerrequisito de crear `schema_migrations` en DEV (no existe); contrato de plataforma versionada (`strategy_platform_kinds`, ECHO_NATIVE/ANALYTIC, sin SQX_NATIVE, tokens sellados preservados porque platform es parte del hash de `version_ref`); recorrido Operation/Order/Fill→LAB con `accounting.Ledger` como autoridad económica y verificación por recomputación; taxonomía Q_i de 4 categorías con `risk_method` (el 64,7% del journal reclasificado TICKET_INITIAL_RISK, no cobertura D10), fijación en `engine.go:1051`, transición `QI_SEALED` y validación transaccional con control de writers y correcciones por supersede; `history_id` con `producer_writer` en la PK (colisión entre productores imposible); receipts en tabla nueva sin tocar promotion_records; retención de inputs write-ahead digest-addressed con GC por referencia; 64 MiB aclarado como request completo con caps (100k ops/historia, 8 historias/request) y 413 sin aceptación parcial; transporte medido (p95 ≈ 24,8 KB, max 23,65 MB, 412–421 B/op sobre 210 historias reales) sustituyendo la estimación 6–9 MB; benchmark congelado con la CDF empírica real (p50=19/p95=59/p99=24.682/max=56.884 ops) y gates alcanzables (speedup ≥2× observado con 8 workers, sin promesa 8×); caso T verificable sin venue/LIVE; U01–U06 clasificados VERIFIED/SPECIFIED_FOR_IMPLEMENTATION/NOT_DEMONSTRATED (frontera PROD acotada al retiro de 066); reconocimiento formal de que el preflight no fue verificación independiente.
- **Dónde:** repo vault (rama master, commit de este change_log); repos producto SIN cambios (reparación de SPEC only, read-only sobre echo/symphony/PG DEV).
- **Por qué:** dictamen del Primary Manager 2026-10-21 exige concretar R01–R06 antes del único gate de aceptación técnica del freeze; sin reabrir D09/D10/D11/D16 ni pedir nuevas decisiones de producto.
- **Sin cambios en:** decisiones ratificadas, producto (echo/symphony), PROD, Gateway, skills/constitución globales.

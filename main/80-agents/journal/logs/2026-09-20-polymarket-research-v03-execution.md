---
type: change_log
schema_version: 1
scope: session
created: 2026-09-20
updated: 2026-09-20
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine — MVP]]"
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

# 2026-09-20 — Polymarket Research v0.3: ejecución del mandato y checkpoint de entidad

## Cambio canónico

- **Entidad actualizada, no recreada:** `main/10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md` — nueva sección `## 🚀 Research v0.3 — NegRisk Validation + Sports Continuous Capture` (antes de la sección v0.2) y nueva entrada en `## 📆 Bitácora` (2026-09-20, `RS_V03_PARTIAL_DATA`).
- **Estado registrado:** baseline `7bd264d` → final `f070496` (branch `feature/research-strategies-v01`, sin push); gates A `ea1e3c8` (V03_PREFLIGHT_PASS), B `cc57e8d`, C `4189a9b`, D `eaf2d94`; certificado `M4_CERTIFIED_NON_LIVE` re-pineado en `f070496`; cobertura `cmd/engine` 98.24% sin excepciones pendientes; POC-S01 línea completa (membership on-chain VERIFIED sobre 159954; 663 sets INCONCLUSIVE), POC-S02 parcial (fase 1 ejecutada, ventana completa preregistrada como runbook).
- **Evidencia:** `testdata/research-v03/` en el repo engine (COVERAGE, B3, B4, C2, runbook, manifests, certificado); bundles `polymarket-engine-datasets/rs-v02/` y `rs-v03/` con verificación física desde el destino.

## Validación y pendientes

- PASS: regresión completa con race 28/28; certify con baseline exacto + prueba negativa `M4_STALE_CERTIFICATION`; replay de journals desde los bundles con digests idénticos; `diff -r` originales intactos.
- Pendiente del owner/próxima sesión: ejecutar la fase 2 deportiva (runbook T-8.5h del 2026-09-22); re-run NegRisk 159954 post-resolución (2026-12-09); revisar el push externo del checkpoint `25f578a` al remoto (esta ejecución no hizo push).

## Seguridad

Sin wallet, claves, signing, transacciones ni RPC administrativo; lectura pública on-chain únicamente (eth_call view, block-pinned). Sin órdenes; LIVE_DISABLED intacto; sin push desde esta ejecución.

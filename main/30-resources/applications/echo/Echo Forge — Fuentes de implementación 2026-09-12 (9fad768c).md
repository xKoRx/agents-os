---
type: source
schema_version: 1
status: active
area: "[[Echo]]"
source_url:
repo: "xKoRx/symphony"
path: "sqx/"
author:
published:
captured: "2026-09-13"
license:
checksum:
supersedes:
superseded_by:
aliases: []
tags:
  - kind/source
  - area/echo
created: "2026-09-13"
updated: "2026-09-13"
---

# Echo Forge — Fuentes de implementación 2026-09-12 (9fad768c)

## Referencia

- **Origen resoluble:** repo `xKoRx/symphony`, commit `9fad768ccd1f9d25ebb535a2d26edb3d74556c10`, branch `feature/f04-magic-version-handoff` (master/origin-master `0b9742b0`), working tree con 1 archivo dirty (`specs/FEAT-SQX-STRATEGY-EVALUATION/fixtures/phase4_performance.json`, intocado por la campaña).
- **Fecha de captura:** 2026-09-13 (fase C de [[Echo — Knowledge Base Consolidation]]).

## Alcance

- Cartografía funcional completa de Echo Forge (módulo `sqx/`) al baseline: `GenericSQXWorkflow` secuencial + `ForgeCampaignWorkflow` multi-wave sobre Temporal (SDK v1.35.0 en `sqx/go.mod`), WFM durable export+seal, ranking `score_descending.v1`/`weighted_combination_minmax.v1`, selección `stage4.v1`, FinalistPromotion V2, MT5 real (tester.ini + reporte parseado + reconcile + score shadow), migraciones PG 001–016, Mongo evidencia, MinIO `sqx-strategies`, etcd.
- Evidence pack completo: `10-projects/Echo/agentes/kb-consolidation/artifacts/03-forge-cartography.md` (claim → file → symbol → test → confidence).
- Límite declarado: F-04 (magic V1 allocator + seal + handoff + migraciones 015/016) es BRANCH-ONLY en `9fad768c`; `SealStrategyVersion` sin caller de producción; única ingress de handoff = `FakeConsumerIngress` (tests); testdata = copia byte-equal del corpus S0 Echo (no fixture auténtica del producer).

## Notas de provenance

- Captura read-only durante la campaña KBC (sin checkout/reset/stash; lectura committed); respalda las páginas [[echo-forge]] y [[echo-forge-integration-boundary]].
- Provenance histórica previa (Symphony `a10c26c`): [[Echo Forge — Fuentes de arquitectura y producto 2026-09-06]].

## Lifecycle

- **Supersedes:** — (nota source por baseline; complementa, no reemplaza, la de 2026-09-06).
- **Superseded by:** —

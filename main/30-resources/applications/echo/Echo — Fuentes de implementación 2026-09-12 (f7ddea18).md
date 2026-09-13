---
type: source
schema_version: 1
status: active
area: "[[Echo]]"
source_url:
repo: "xKoRx/echo"
path: "v3/; specs/"
author:
published:
captured: "2026-09-12"
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

# Echo — Fuentes de implementación 2026-09-12 (f7ddea18)

## Referencia

- **Origen resoluble:** repo `xKoRx/echo`, commit `f7ddea18cab51db72c9765aa74381328134d7ce7`, branch `feature/e02-control-safety-journal-recovery` (master/origin-master `a99f9a63`), working tree clean.
- **Fecha de captura:** 2026-09-12 (fase B de [[Echo — Knowledge Base Consolidation]]).

## Alcance

- Cartografía funcional completa de Echo al baseline: entrypoints (echo-core StateFun, echo-gateway, echo-bridge Windows, lab-worker, journalctl, toolkit, front Vue, EAs MT4/MT5), contratos frozen `v3/sdk/contracts`, migraciones 001..062, Gateway + auth E-02, 17 topics Kafka, persistencia PG esquema `echo`, observability OTel, retry/recovery, 137 archivos de test como evidencia.
- Evidence pack completo: `10-projects/Echo/agentes/kb-consolidation/artifacts/02-echo-cartography.md` (claim → file → symbol → test → confidence).
- Límite declarado: E-02 (auth 4 actores, journal quarantine + replay) es BRANCH-ONLY en `f7ddea18`, no en master `a99f9a63`, y PHYSICAL_PARTIAL (T14/T15 físico sin ejecutar).

## Notas de provenance

- Captura read-only durante la campaña KBC; el repo sigue siendo desarrollado en paralelo por otros agentes — este nota fija QUÉ baseline respaldan las páginas [[echo-core]] y [[echo-forge-integration-boundary]].
- Provenance histórica previa (master `04c16bd`): [[Echo — Fuentes de arquitectura y producto 2026-09-06]].

## Lifecycle

- **Supersedes:** — (nota source por baseline; complementa, no reemplaza, la de 2026-09-06).
- **Superseded by:** —

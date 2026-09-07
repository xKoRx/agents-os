---
type: change_log
scope: session
created: 2026-07-25
updated: 2026-07-25
area: "[[Echo Forge]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
entities:
  - "[[EchoForgeTradeListExporter]]"
  - "[[TradeListArtifactWriter]]"
related:
  - "[[Echo Forge - Cierre de Etapa 4]]"
aliases: []
confidence: verified
source_session: 2026-07-25-fix-pack-g2-review
source_feedbacks:
  - "[[2026-07-25-echo-forge-g2-review-rework-session-feedback]]"
share_scope: team
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - project/echo-forge
---

# Change log - 2026-07-25 - Echo Forge G2 review fix-pack

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - `80-agents/memory/public/known-error/2026-07-25-success-sentinel-after-manifest-rewrite.md` (created)
  - `80-agents/memory/public/decision/2026-07-25-atomic-artifact-writer-single-call.md` (created)
  - `80-agents/memory/public/runbook/2026-07-25-fix-pack-for-gate-handoff-review.md` (created)
  - `80-agents/journal/feedback/system-1/2026-07-25-echo-forge-g2-review-rework-session-feedback.md` (created)
  - `10-projects/Echo Forge/agentes/Echo Forge - Cierre de Etapa 4.md` (updated: Bitácora F2, Estado actual, OD-P2.5)
  - `specs/FEAT-SQX-METRICS-CONTRACT/phase2/G2_HANDOFF.md` (rewritten)
  - `sqx/core/runtime/{config.go,config_test.go}` (mapping 5 task types + test)
  - `sqx/exporter-plugin/src/SQ/CustomAnalysis/EchoForgeTradeListExporter.java` (sin rewrite post-gzip)
  - `sqx/exporter-plugin/src/SQ/CustomAnalysis/trades/TradeListArtifactWriter.java` (+writeScopeArtifacts)
  - `sqx/exporter-plugin/src/SQ/CustomAnalysis/trades/ProductionSQXTradeSource.java` (Directions via reflexión)
  - `sqx/exporter-plugin/test-support/simulator/.../TradeListExportSmoke.java` (asserts duros + caso 4b)
  - `sqx/exporter-plugin/test-support/fixtures/trades/SHA256SUMS.txt` (regenerado)
  - `sqx/exporter-plugin/test-support/fixtures/trades/regenerate_sha256sums.sh` (new)
  - `sqx/exporter-plugin/scripts/verify_build.sh` (new)
  - `sqx/exporter-plugin/docs/ROLLBACK.md` (new)

## Motivo

Cerrar los 4 blockers y 3 non-blockers identificados en el veredicto del owner sobre el handoff G2 del pase F2 (commit `b2848d7`). Sin promover G2 — sólo resolver los blockers para re-validación.

## Fuentes usadas

- Veredicto del owner (mensaje de chat con tabla `Blocker | Evidencia`).
- Handoff G2 review en `specs/FEAT-SQX-METRICS-CONTRACT/phase2/G2_HANDOFF.md`.
- Nota canónica [[Echo Forge - Cierre de Etapa 4]].
- Plan de Fase 2 en la misma nota (decisiones OD-P2.1..OD-P2.4 v1).

## Resolución aplicada

- **B1 — SHA-256**: regenerado `SHA256SUMS.txt` desde disco (39/39 OK); script `regenerate_sha256sums.sh` idempotente con self-check.
- **B2 — Atomicidad**: nueva API `writeScopeArtifacts(ndjson, result, ExportRunSpec)` que comprime NDJSON en memoria, conoce `compressed_bytes` reales, compone manifest + `export_run.json`, y emite `_SUCCESS` sólo si los 3 archivos se persistieron. Reescritura externa del exporter eliminada.
- **B3 — OD-P2.1**: `import Directions` eliminado; `Directions.Both` resuelto por reflexión con cache `DIRECTIONS_BOTH`.
- **B4 — DoD**: `docs/ROLLBACK.md`, `scripts/verify_build.sh`, `ResolveLocalProjectNameByType` mapea 5 task types + test 8/8 PASS, defer firmado para smoke SQX real.
- **Non-blockers**: `phase1/G1_HANDOFF.md` staged + committeado; handoff ya no dice "sin git"; Overview/WFM no migraron al kernel común (decisión explícita).

## Validación

- `TARGET_DIR=/tmp/f2_final ./build.sh` exit=0.
- `bash scripts/verify_build.sh` exit=0 (5 exporters en prod, sin test-support).
- `TradeExtractionConformanceTest` 5/5 PASS.
- `TradeListExportSmoke` exit=0 (FULL/IS/OOS + 4a/4b).
- `sha256sum -c test-support/fixtures/trades/SHA256SUMS.txt` 39/39 OK.
- `go test -run TestResolveLocalProjectNameByType_FixedProjects -v` 8/8 PASS.
- Commit `5c186a3`: 12 archivos, +1176/−184. Sin `reset`, sin `checkout --`, sin reescritura de commits previos.

## Compartibilidad

- **Scope:** team — la memoria pública sobre atomicidad de artefactos y runbook de fix-pack son reutilizables para cualquier proyecto con pipelines de artefactos multi-archivo.
- **Redacción revisada:** sin identidad personal, sin paths absolutos de máquina, sin secretos, sin dumps pesados. Los hashes son verificables en el commit `5c186a3` del repo `symphony`.

## Rollback

- Si un próximo veredicto rechaza el fix-pack: `git revert 5c186a3` (commit aislado, no toca `b2848d7`).
- Si se descubre que el fix B2 (API única) es incorrecto: el contrato sigue siendo "una sola API, sin reescritura externa" — el bug específico puede parchearse sobre el writer sin tocar el exporter.
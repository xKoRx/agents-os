---
type: agent_memory
scope: internal
created: 2026-07-26
updated: 2026-09-09
index_priority: never
indexable: false
load_policy: manual
memory_state: archived
tags:
  - kind/agent_memory
  - tech/go
  - app/echo-forge
  - topic/sdd
  - topic/phase4
---

# Continuidad Operativa: Echo Forge Fase 4 (G4) Cerrada

## Estado
- **G4 = accepted** tras rework B1–B4. `FEAT-SQX-STRATEGY-EVALUATION` pasa de `Spec-Active` a `Accepted (G4)`.
- Commits en symphony: `db5e19f` (rework) + `ce5cff6` (pin SHA); HEAD `ce5cff6`, **14 ahead** de `origin/master`. Revalidación owner 16:30 CLT confirmó build/vet/test/race verdes.
- Los 4 archivos `input/processed/20260720_233713_*` se preservan intactos (ajenos al rework).

## Handoff canónico
- `specs/FEAT-SQX-STRATEGY-EVALUATION/G4_HANDOFF.md` (creado en este rework).
- Fixtures reproducibles: `specs/FEAT-SQX-STRATEGY-EVALUATION/fixtures/phase4_custom_metrics.json`, `phase4_shadow_compute_only.json`, `phase4_performance.json`.

## Decisiones técnicas relevantes
- **`SetSQXNativeMetrics`** ya no delega en `SetMetrics`: cada uno escribe su slice (`SQXNativeMetrics` vs `Metrics`). Lógica común extraída a `normalizeMetrics`.
- **Upsert en Mongo** enforce `EvaluationMode = "shadow"` a nivel contrato: rechaza valores distintos con `ContractError`, y si llega vacío lo fija en `shadow` (defensa en profundidad).
- **`EnsureIndexes`** cableado en `cmd/sqx-worker/main.go` siguiendo patrón de `TradeListRepository`. Crea `wave_evaluated_at_v1`, `scope_lookup_v1`, `wave_verdict_v1`.
- **`ShadowComputeOnlyActivity`** vive en `sqx/activities/worker/` (no en `core/evaluation`) para evitar import cycle con `core/domain`.
- Performance 10k trades: ~1.39 ms/op, 4.08 MB/op, 12614 allocs/op (Apple M4).

## Riesgos abiertos (no bloquean G4)
- `TestStrategyEvaluationRepository_Upsert_DefaultsEmptyModeToShadow` retirado en iteración previa; reabrir como `TB-G4-1`.
- Smoke E2E con Mongo real pendiente (requiere cluster).

## Próximo paso
F4 cerrada. F5 (`FEAT-SQX-CLASSIFICATION-RANKING` / selector) sólo arranca con orden explícita del owner ("avanza F5").
# Change Log — 2026-09-20: E-07 corrección Manager C1 (defectos C1–C5)

## Contexto

Revisión de source del Manager demostró defectos sobre la implementación E-07 @ `7c836619`. Ejecución del mandato MANAGER CORRECTION C1: corregir C1–C3, declarar el conflicto contractual C4 y clasificar C5, sin reconstruir E-07 ni tocar Forge/E-06.

## Cambios

- Repo `xKoRx/echo` (fuera del vault): push FF `7c836619..a7a61875` en `origin/feature/e07-raw-facts-deal-lifecycle` — commit único con C1 (bytes originales en `raw_payload`), C2 (`Service.RecoverPendingFact` transaccional + driver delegante), C3 (lookup tx-scoped sólo OPEN; error ⇒ rollback), C4 (emitter fail-closed `ErrOriginIdentityUnavailable` + STOP `E07_ORIGIN_IDENTITY_CONTRACT_CONFLICT` documentado en VERIFICATION §8.2), C5 (receta `fact_ref` sin autoridad S0, a ratificación). 9 archivos source/test + `VERIFICATION.md` §8.
- `specs/FEAT-RAW-FACTS-DEAL-COVERAGE-LIFECYCLE-E7/VERIFICATION.md`: delta nuevo §8 (revisión Manager, correcciones rojo→verde, STOP C4, gates re-ejecutados, estado por gate con aceptación Manager RETENIDA); evidencia NORMAL §1–§7 conservada intacta.
- Entidad/proyecto `[[Echo — E-07 Raw Facts DEAL Coverage Trade Lifecycle]]`: bitácora y estado actualizados por delta (E07_IMPLEMENTATION_COMPLETE v1.0.0 con corrección Manager C1 aplicada; siguiente acción única = decisión Manager sobre C4/C5).
- Registro de ejecución: `80-agents/journal/agent-runs/2026-09-20-zcode-glm-5.3-flash-e07-manager-correction-c1.md` ([[ZCode]] × GLM-5.3-Flash, coding/high, success/passed).

## Verificación

- Fase roja demostrada: 9 tests rojos exactos sobre `7c836619` (C1 base64; C2×4 PENDING perpetuo; C3×2 error SQL commiteado; C4×2 ticket publicado) → verde `-race`.
- Failing sets idénticos por nombre vs `7c836619` (== baseline `b66dc5ff` por §7.1): sin PG 4/4, con PG 55/55, diff 0. Harness `trade_facts_e7` 061→065 PASS (PG 17.11 descartable). `git diff --check` limpio; go.mod/go.sum delta 0; migraciones y S0 diff 0.

## No-tocados

- Base histórica E-06 (`b66dc5ff`), migraciones 001–065 (ninguna modificación SQL), S0 `contracts/**`, gateway, Flink, Hasura, MQL collector, Forge, master. Sin tags/releases. Sin SHARED DEV ni PROD. Sin modificar SPEC frozen (C4 resuelto como STOP, no como cambio unilateral).

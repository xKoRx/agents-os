---
type: known_error
schema_version: 1
scope: application
created: "2026-08-13"
updated: "2026-08-14"
area: "[[Echo]]"
project: "[[Stager - Cross-Platform Deployment Lifecycle]]"
application: "[[symphony]]"
entities:
  - "[[Symphony]]"
  - "[[Echo Forge]]"
related:
  - "[[stager-mt5-heartbeat-late-started]]"
  - "[[symphony-mt5-backtest-report-htm-absent]]"
aliases:
  - EX5 ausente o vacío
  - mt5_eas compile 1s
  - compile log UTF-16
confidence: verified
source_session: 11f6babe-3522-40c1-bb09-f29b5012c34d
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
  - area/echo
  - tech/mt5
  - project/echo-forge
---

# symphony-mt5-compile-ex5-absent

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- Histórico: `mt5_compile_artifact` COMPLETED en ~1s con `EX5 ausente o vacío`.
- Segunda capa: MetaEditor sí compiló (`Result: 0 errors`, log UTF-16) y el matcher UTF-8 rechazó el log.

## Causa

- Argv `/compile:"path"` (comillas embebidas) + `exec.Command` en Windows: MetaEditor no compilaba.
- Exit 1 de MetaEditor portable tratado como infra aunque hubiera EX5 + `Result: 0 errors`.
- Log de compile UTF-16 LE (`FF FE`); regex UTF-8 no veía `Result: 0 errors`.

## Impacto

- Bloqueaba E2E compile. OccupiedDrain G3 no dependía de EX5. **Resuelto 2026-08-14** en `artifact_compiler.go` (`/compile:` sin quotes, exit ≠0 no-infra si el proceso corrió, `normalizeCompileLog`).

## Detección

- ~1s + `EX5 ausente` → quoting. EX5 presente + `compile log sin Result: 0 errors` + BOM `FF FE` → UTF-16.

## Mitigación

- No reabrir F3.6. No publicar MinIO `0.2.41`. No meter comillas en argv de MetaEditor. Decodificar UTF-16 antes del matcher.

## Evidencia

- FAIL histórico: [[2026-08-13-2300-stager-g3-occupieddrain-close-summary]]
- PASS: `f36-occupied-f36-occ-a2861961` 8/8 success; EX5 `Strategy_1_1_22` 150588 B; [[2026-08-14-stager-e2e-close-summary]]

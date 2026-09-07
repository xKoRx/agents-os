---
type: change_log
scope: project
created: 2026-08-03
updated: 2026-08-03
area: "[[Echo]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo Forge - Cierre de Etapa 4]]"
  - "[[2026-08-03-symphony-flow-1785813489-tradelist-manifest-sha256-mismatch]]"
  - "[[2026-08-03-echo-forge-apply-selected-run-params-fix-verified]]"
  - "[[2026-08-03-echo-forge-stage4-audit-flow-71-summary]]"
source_session: cursor-654adfaa-echo-forge-stage4-flow71-audit-2026-08-03
indexable: true
index_priority: medium
tags:
  - kind/changelog
  - project/echo-forge
  - area/echo
---

# Change log — Echo Forge Stage 4 audit, flow 71 (2026-08-03)

## Qué cambió

- Verificado que `apply_selected_run` en el workflow `1785813489` ahora sí aplica los valores de los parámetros del WFM (no solo el `MagicNumber`). 8/10 strategies auditadas muestran cambios reales (Period, Number, ProfitTarget, StopLoss, Fast/Slow/Smooth, EAB, TrailingStop) entre `03_optimizer` y `04_optimizer_robust`.
- Identificado issue preexistente (no regresión): SHA256 mismatch en `06_trade_list/*.trades.manifest.json` — el hash declarado no coincide con el SHA256 real del `.ndjson.gz`. Reproducible en `1785786248` y `1785813489`.
- Confirmado que `05_reretester` no modifica parámetros (0 diffs vs `04` en todas las strategies verificadas) — comportamiento esperado, el re-test usa los params ya aplicados en `04`.

## Artefactos de memoria

- [[2026-08-03-echo-forge-apply-selected-run-params-fix-verified]] — resolución del bug de params del WFM.
- [[2026-08-03-symphony-flow-1785813489-tradelist-manifest-sha256-mismatch]] — known-error activo del SHA256.
- [[2026-08-03-echo-forge-stage4-audit-flow-71-summary]] — session summary.

## Repo / branch

- No se modificó código en esta sesión. Auditoría read-only.
- `symphony`: working tree sin cambios.
- `sdk`: working tree sin cambios.
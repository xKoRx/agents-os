---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related: ["[[Echo Forge — Operación Real V2]]", "[[Dynamic Groups — Shot 1 — Autoridad privada]]"]
aliases: []
tags:
  - kind/doc
created: "2026-10-26"
updated: "2026-10-26"
---

# Dynamic Groups — Shot 2 — Estado de implementación

## Propósito

Registrar el resultado de **Shot 2 — Implementation** de Dynamic Group Targets & Runtime Task Bindings sobre [[Echo Forge — Operación Real V2]], enlazando la autoridad técnica privada sin copiar contenido propietario al vault público.

## Contenido

**SHOT2_PARTIAL_WITH_FINDINGS**, 2026-10-26. Los ocho tramos del Implementation Plan congelado (2.1–2.8) están implementados y committeados en la rama `codex/forge-dynamic-groups` de Symphony (privado), candidata pusheada a origin: `64d2dc5` (2.1 contratos/identidad V2/dispatcher) → `b5f3a6c` (2.2 universo/CAS PG, migraciones 017-018) → `a2cedb6` (2.3 ranking/selection V2) → `e8cdd4b` (2.4 lifecycle del group) → `31cb3e8` (2.5 bindings/evaluate_strategy durable) → `455311a` (2.6 SelectedPeriod/Apply) → `1428efc` (2.7 CFX/MT5 efectivos) → `f31e605` (2.8 wiring worker/watcher + verificación). El documento de verificación del implementador, la matriz R/C/A y los comandos reproducibles viven en `specs/FEAT-SQX-DYNAMIC-GROUP-TARGETS/SHOT2-VERIFICATION.md` en ese branch. Sin deploy, sin releases, sin campañas, sin backtests físicos, sin integración Echo.

Alcance funcional: group con `target.top_n=X` por logical_type consume Y candidatas por iteración de un universo congelado, repite el subflujo declarado desde la task 0, acumula supervivientes con ledger TaskResult.v2, re-rankea el acumulado completo con el kernel compartido y entrega exactamente X o UNDERFILLED con agotamiento demostrado; bindings tipados opt-in por instancia (`exact_evaluation.v1`, `wfm.selected_last_is.v1`, `applied_wfm_period.v1`); SelectedPeriod WFM con regla del último IS no-future fail-closed; CFX efectivo parcheado sólo en dateFrom/dateTo con diff semántico; INI MT5 por instancia con roundtrip temporal exacto. Contrato V1 replay intacto (fail set de la suite `workflows` idéntico al baseline, verificado dos veces).

**Findings que acompañan el candidato:** F-S2-01 cobertura del código nuevo 86,5% < 95% exigido (caminos críticos cubiertos, gap en guardas de validadores); F-S2-02 continue-as-new checkpoint (R25) no implementado — recovery actual = replay determinista + CAS idempotente; F-S2-03 exporters Java sin metadata adicional de período (queda para Shot 4); F-S2-04/F-S2-05 menores. A-cases verdes, parciales y su disposición exacta constan en SHOT2-VERIFICATION.md.

**NEXT EXACT:** iniciar **Shot 3 — revisión adversarial independiente** desde el candidato congelado `f31e605` (branch `codex/forge-dynamic-groups`), ejecutando A01–A39 con failpoints reales sobre stores descartables y Temporal test server, según `07 — Adversarial Plan.md` del paquete privado. El revisor no debe reutilizar los tests del implementador como único oráculo.

## Fuentes

- [[Echo Forge — Operación Real V2]]
- [[Dynamic Groups — Shot 1 — Autoridad privada]]
- Symphony privado: `xKoRx/symphony`, rama `codex/forge-dynamic-groups` @ `f31e605`, `specs/FEAT-SQX-DYNAMIC-GROUP-TARGETS/`

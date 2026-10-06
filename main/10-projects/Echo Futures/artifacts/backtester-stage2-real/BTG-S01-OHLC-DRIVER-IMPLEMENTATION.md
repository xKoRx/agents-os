---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related: ["[[Echo Futures]]", "[[BTG-S01-FUNCTIONAL-BASELINE-PROFILE]]", "[[OHLC-RUN-CONTRACT]]"]
aliases: []
tags:
  - kind/doc
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01 native OHLC functional driver implementation

## Propósito

Registrar la implementación y pruebas locales del candidato nativo, con límites y gates pendientes verificables.

## Contenido

### Estado verificable

Fuente candidata congelada y publicada e2e15a3559034a3ed08c04f247baf4919e20b2ff, rama codex/btg-s01-ohlc-driver, base directa B933b40d65d7fe0946bb5b75038f6c4858d9912ea. Integración exacta del adapter/TCR/SDD B desde e44b741e0a6c32d39326b46738dc70565db4759c y autoridad ingress54698cb0, sin merge/rebase/cherry-pick ni edición local B. Candidato sintético bloqueado por finding material BT2-F08 confirmado en revisión independiente. Sourcefreeze no cambia; fresh corrective worker y rerun original pendientes. Race longitudinal cancelada por Coordinator, INTERRUPTED_BY_COORDINATOR_AFTER_MATERIAL_REVIEW_FINDING, exit143; no PASS. Primera subprueba stop completó assertions/digests y comenzó tp antes de interrupción.

### Implementación y contratos

Perfil opt-in BTG_FUNCTIONAL_NQ_EVAL_V1 materializa configuración S2/GerardMM real, SIM100000USD plano, plan diario SL2000/TP1500, scaling ausente NO_ADDS_FUNCTIONAL_BASELINE_V1, NQ20USD/point y tick0.25, fee2.49 porcontrato/fill, spreadmodel1/1tick y slip1tick, GTC y markage1m. Calendario semanal funcional Chicago Sun..Thu17→next16, reset17, sin overrides históricos inventados. No default productivo, reglas prop ni validación scaling. API FunctionalNQEvalSpec(FunctionalNQEvalInput)(RunSpec,error) devuelve configuración/plan/catalog/calendario/identidades; FunctionalNQCalendarV1 devuelve market.CalendarDataset.

Open modelado sólo expone Open e identidad. SourceClose conoce HLCV al End, ejecuta protección resting primero y observaciones monetarias adversa→favorable→Close con revisión económica correlacionada, todas a End; mercado cierra en siguiente Open físico pinned. Se reutilizan facts/finality/fees/ledger/provider/pump. MarketContext single-Mark por fallback, sin ExecutableQuoteSource/trade/quote falsos. InputSequence(ref) y consumed count sólo en SourceClose. Todas las sources coincidentes cierran antes de boundaries/timers y próximo Open; no retrofactos ni riesgo nuevo al horizonte.

Minutos faltantes fallan visibles por calendario real declarado; prefijo incompleto no fabrica H4/5m completos. Se requieren51 H4 y20 5m completos con elegibilidad causal. Streams futuros/retirados siguen deber físico y selección/pins, active-flat EOF truncado falla y oldpinned sinolddata da OLD_CONTRACT_DATA_UNAVAILABLE sin valoración por nueva expiry. Control tardío dentro de intervalo expuesto/working falla antes de efectos en todas las pendientes; control exactamente a EndExclusive permanece pending según contrato half-open y no invalida cierre terminal.

### Prueba independiente y correcciones

Cuatro casos de minute corpus completo S2→GerardMM→Operation→Provider→venue→accounting pasan normal171.45s: long/short SL y TP-next-Open. Cantidad30 y costes149.4USD se comprueban con oracle big.Rat desde fills físicos. En entry Open102 la liquidación causa unrealized-450USD y fee74.7USD; budget1475.3/600 redondeado a tick da distancia2.25. Stops actuales99.75/104.25, fills99.5/104.5. La primera prueba short asumía erróneamente stop>105; RED conservado, command/ledger rev23785 prueban ajuste legítimo MM; oracle corregido, sin cambio de fórmula. Short forensic dirigido PASS44.310s.

Perturbar futuro High deja igual prefijo bajo referencias sintéticas fijas; esto no afirma identidad byte a byte de referencias NT reales cuyo contenido cambia digest/runID. Prueba de fresh-process determinismo válida sólo sintética. Native protocol/context/profile/venue race PASS31.642s, H4 causal50/51 y selección timers race PASS1.110s. Regresiones legacy/S04/schedule/rollover/horizon/determinism/control race PASS35.902s; adapter B y venue suites completas race PASS1.335s/1.033s; vet dirigido PASS.

BT2-F06 elimina historial Fired de cola nativa entre roots con orden/generación preservados. Replay48/1000min con5000 históricos descartados mantiene digest completo records/result/inputrefs y peakpending<=20; equaldeadlines, stale rearm, residuals y legacy cubiertos. Race original agotó600.126s, no PASS. Medición normal emparejada40.48→42.46s con digests idénticos no demuestra speedup ni bottleneck dominante. CPU GC47.4%, completeNativeBar4.82% no justifica caches ni SDK tuning; performance original NOT_MEASURED.

### Límites y continuidad

Sin modificación SDK/Core/S2/MM/fixtures/defaults/CLI/D6. Sin datos originales NT ni adquisición/histórico certificados; multi-expiry físico y rerun real esperan manifest/bytes/schedule. Gate Owner y review independiente pertenecen al Coordinator. Source no cambia. Cobertura final cambiada conservadora525/562=93.4164% bruta; aplicable525/552=95.1087% con10 invariantes imposibles/constantes excluidas, aceptadas por revisión independiente comunicada por Coordinator. Mapping/block/provenance en coverage-final-current.json y coverage-union-current.cover; no exclusiones ledger/recorder/OS o lógica económica. VERIFICATION del commit conserva snapshot del freeze; cierre actual aquí explica gate material posterior.

Evidencia externa, logs RED/Green, perfiles de CPU/coverage, comandos y hashes en el reporte técnico de implementación mantenido por el worker fuera del vault. Modelo gpt-6.1-sol, model_source host, superficie Codex, PRO_CHAT_POOL_DELTA0. Parent refrescó AgentsOS07ea7468/Echo372af59a/S04cd451972/D6d08a30ce; delta D6 futures-bridge sin intersección SDK/Core.

### BT2-F08 — primer account-day parcial

Revisión independiente reproduce sourcee2e15a35 con Warmup2026-10-05T20:59Z (Chicago15:59), TradeStart22:00:59.999999999Z y End22:01Z, source20:59→21:00 y22:00→22:01 respetando break16–17. openInitialAccountDay asigna ad-20261005 por civilDate(WarmupStart); reset17Chicago22Z intenta abrir el mismo ID y Ledger falla ACCOUNT_DAY_FAILED a22:00 antes del segundo SourceClose. Esperado: intervalo inicial que contiene WarmupStart [Oct4 17CT,Oct5 17CT) distinto del nuevo intervalo. Defecto heredado también reproducido por legacyTRADEMODEL, sin fórmula S2/MM afectada.

Estado OPEN_REPRODUCED_REMEDIATION_PENDING bajo [[BTG-S01-FINDINGS]]. Worker actual no corrige fuente congelada; fresh worker usará civilDateOf/boundaryOf sin24h fijo, preservando PlanID/ledgerID separados y warmupordinal0. Evidencia TOP externa independent-fast.log y account-day-legacy-reference.log. Candidato C no aceptado pese a cobertura y transport assertions locales; original NOT_RUN. Probes nativos son PERMANENT_REGRESSION y perfiles/logs/coverage unions DISPOSABLE_REPRODUCER retained externally; no framework ni L3 reutilizable nuevo.

Cierre ONE-SHOT de este worker: implementación/run/log y feedback puntual de comando namespace, schema focal válido, recuperación exacta Markdown porque Graphify CLI/MCP no expuesto; no rebuild ni cierre root. Reusable NONE. PRO_CHAT_POOL_DELTA0.

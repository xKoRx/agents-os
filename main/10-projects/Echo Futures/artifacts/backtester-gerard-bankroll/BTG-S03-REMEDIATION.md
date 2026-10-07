---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
project: "[[Echo Futures]]"
related: ["[[BTG-PLAN]]", "[[BTG-S03-IMPLEMENTATION]]", "[[BTG-S03-OWNER-MANDATE-20261006]]"]
aliases: []
tags:
  - kind/doc
created: "2026-10-07"
updated: "2026-10-07"
---

# BTG-S03-REMEDIATION (devolución correctiva)

## Propósito

Devolución correctiva S03 al mismo implementador (instrucción Owner 2026-10-07): terminar lo pedido y probarlo. CORRECCIÓN y COMPLETADO de producto, regresiones ejecutadas y pruebas faltantes corriendo. No es S04. Rol: implementation lead LOCAL, superficie ZCode (GLM, host no expone identificador exacto), ONE-SHOT con delegación acotada.

## Contenido

### Estado

S03_REMEDIATION ejecutada sobre xKoRx/echo carril `codex/btg-s03-remediation`, base `c1c0e7d4`, commits `09702442` (R1–R5) y `adfe4087` (paridad runtime strategy-seam), pusheados. Suite backtester completa verde (827s, 45m timeout por el test a52 largo; sdk verde salvo fallos preexistentes de entorno: `sdk/postgres` TestScratch_QueryDB y `httpobs` Jaeger — ambos fallan también sin el delta, requieren DB/collector vivos). Corridas reales sobre NQZ3 derivado (originales intactos) con binary identificado SHA256 `3f1311e2…71d20d`.

### R1 — Continuidad completa (cumplido)

Campaña = UN experimento causal continuo (`RunCampaign` conduce UN `RunState`): mercado, analítica, reloj, fanout y los OwnerState de Strategy evolucionan sin reinicio; sólo el compartimento de cuenta (Account/Operation/MM/Provider/ledger/venue) se reemplaza en frontera drenada vía `RunState.ReplaceAccount` (quiescencia exigida; nada financiero cruza: balance fresco, estados propios). Activación, settlement y reemplazo usan la autoridad de sesión del propio run (`sessionNegotiable` walker sobre Calendar/SessionGrid) — el calendario paralelo de 17:00 fue eliminado. Durante pausa/burn/ausencia de destinatario el driver sigue consumiendo barras y cierres (test: sesiones completas con evaluaciones, ninguna oscura). El estado nativo del venue (intervalo abierto) se traslada al sucesor (`ExportNativeSeed/SeedNativeState`) para que el cierre de la barra en vuelo complete idéntico. Fanout retargetea por plano vivo; el timer de frontera del compartimento anterior se cancela antes del swap (fix: doble apertura de día). Desviación aceptada por evidencia y reparada en composición: la transferencia analytics/market owner state produjo `ANALYTICS_SOURCE_FAILED` (máquina de regiones no reanudable); la continuidad de decisión vive en el OwnerState de Strategy (autocontenida) y los rings se reconstruyen — declarado en código y doc.

Pruebas: TestBTGS03_CampaignCashBurnReplacementAndContinuity (burn mid-sesión, pausa con cierres 5m/H4, activación en minuto admisible del propio run, caja 5000→4880→4520 conciliada, 4 burns, ninguna sesión oscura, saltos de activación ≤ 25 min); TestBTGS03_CampaignDeterministicReplay (byte-idéntico).

### R2 — Intrabar OHLC con MM activo (cumplido)

Modelo nuevo `OHLC_CAUSAL_PATH_V2` (V1 se conserva como receta reproducible explícita; el golden V1 queda byte-idéntico): cada intervalo 1m camina un path de referencia declarado (LONG O→L→H→C, SHORT O→H→L→C; SL-first por orden del path) en pasos de un tick sobre lattice exacto, con instantes modelados `start+floor(i·dur/(K+1))`. Cada paso: match en venue (stops cruzados al primer precio posterior + costos; MARKET aceptados en cursor estrictamente anterior — nunca retroactivo), mark-to-market, QuoteNotification al owner (MM reacciona por paso), drain completo entre pasos y avance causal del reloj (fix probado: sin él las quotes llegaban "del futuro" y se absorbían). V2 admite `scaling_mode CONFIGURED` (guard actualizado); V1 sigue rechazándolo. Barras sin movimiento (K=0) conservan el matching V1 en close.

Pruebas: TestBTGS03_V2IntrabarAddsAdverseAndProtection (adds adversos GerardMM por la entrada normal: ≥3 fills, un fill por orden — sin doble cierre, ningún fill retroactivo contra su submit, rama ADVERSE); suite completa verde (regresión Generic20 detectada y reparada: la rotación de selectores diarios quedó keyed al stage del propio plan).

### R3 — Sustitución utilizable + paridad (cumplido con alcance declarado)

Seam de composición público `CompositionOptions{StrategyModule, MoneyManager}` resuelto ANTES de componer (NewRunWithComposition); la campaña crea cada compartimento por el mismo seam (sin default GerardMM escondido). Pruebas: sustitución de Strategy por el seam (fixture corre donde S2 falla-cerrado por SU readiness — need_h4=51 vía contrato, no literal); sustitución de MM por el seam (deny-all → cero fills; GerardMM opera); variación de TP de plan rows cambia la economía efectiva (oráculo de fills distintos; probe DBGTP verificó tp=1 vs tp=1500 resueltos por el manager). Paridad runtime: TestBTGS03_RuntimeStrategySeamParity — el MISMO módulo detrás de `strategy.NewEngine` (constructor del runtime) emite señales idénticas trigger-a-trigger al run del backtester sobre la misma secuencia de barras. ALCANCE DECLARADO: la paridad cubre la capa strategy-seam (mismo Engine, mismos triggers, mismas señales); el differential harness completo vertical-vs-backtester con fills inyectados lado a lado sigue siendo superficie de S04.

### R4 — Piso estático (cumplido)

`STATIC_LOCK` como variante del evaluador compartido (provider/risk_eval): piso = inicial − límite, nunca remonta, touch/below breach con el comparador conservador; pruebas propias (ganancia previa no sube el piso; toc/cruza 98000 latchea TRAILING_DRAWDOWN; variante desconocida falla cerrada). El perfil de campaña deriva el límite de la configuración (`start − piso`, p.ej. 2000 de 100000/98000) — el 2000 hardcodeado fue eliminado; cambiar la config cambia la regla consumida.

### R5 — Cobros y terminales (cumplido)

`PayoutsCollected` cuenta SOLO débitos APPLIED + acreditación única de caja (ordinales de solicitud separados en `PayoutsRequested`); el retiro ocurre tras el cuarto COBRO; solicitud pendiente al horizonte ⇒ PENDING_AT_HORIZON, sin cuarto abono y sin retiro prematura (TestBTGS03_CampaignPendingPayoutAtHorizon: 3 cobrados + 4ª pendiente, caja sin el cuarto crédito); rechazo/conflicto nunca cuenta. Terminales honestos: `RUN_FAILED`/control error/fuente incompleta ≠ HORIZON_REACHED (FailureCode y motivo al caller/CLI; la conciliación aritmética sola no valida el lifecycle).

### Corridas reales (NQZ3 derivado; binario 1bf45050 SHA256 3f1311e2…71d20d; workspace reports/)

| Corrida | Ventana | Resultado | Evidencia |
| --- | --- | --- | --- |
| BASIC V1 NO_ADDS (golden re-verify) | 2023-10-29→11-23 (25 días) | COMPLETE, run_id `bt-bd627d8a…` IDÉNTICO, economía idéntica (−34293.32, 78 fills/113 ops) | artefacto `9058477a…`; PRIMER DELTA identificado: campo nuevo `observed_steps_policy:""` en fidelity (modelo versionado; sin cambio de semántica) |
| BASIC V2 CONFIGURED | 2023-10-29→10-30 (1 día, warmup Oct-15) | COMPLETE, 9 fills/7 ops (adds adversos activos), neto −2123.80 | `bt-b15d13d1…`, artefacto `b4d193f6…` |
| BASIC V2 fresh reproduce | ídem | IDENTICAL (96.441 records, proceso fresco) | `basic-v2-reproduce/` |
| CAMPAIGN V2 CONFIGURED | 2023-10-29→11-02 (3 días) | HORIZON_REACHED, 1 compra, cuenta ACTIVE_AT_HORIZON sobre el piso STATIC (98.007,24 ≥ 98.000: sin burn — el piso configurado se demostró en real), caja 5000→4880 conciliada, 0 payouts (EVALUATION sin pass) | `campaign-result.json` SHA256 `936b5c55…`; run sellado `bt-c-aedeb4b9…` artefacto `9179be1a…` |

NOTA DE COSTO (gate T37, medido): V2 con observación completa por paso costaba ~40–45 CPU-min por día de mercado vs ~0.3 V1 (corrida de 25 días abortada tras 97+ CPU-min al ~40%). Cuello demostrado y CORREGIDO EN ESTE SHOT con el mecanismo del propio diseño: `OBSERVED_STEPS_INERT_SKIP_V2` (S02 §7.1 SKIP_PROVEN_INERT, condición conservadora por barra: cero exposición + cero órdenes trabajando ⇒ pasos inértes omitidos; re-evaluado por barra). Resultado: warmup+1 día bajó de horas a 1m35s de pared. Equivalencia probada en TestBTGS03_V2InertSkipEquivalence (T35/T36: ALL vs SKIP, mismos fills/comandos/señales 1:1 tras normalizar sólo identidades no semánticas derivadas del run; economías idénticas). Reproducción fresca de la ventana larga V2: NO_RUN por presupuesto de tiempo (la determinística in-process y la reproduce del BASIC V2 sí corrieron); queda para S05.

### TICKS/MIXED y cobertura

TICKS (TRADE_MODEL) verificado por la suite existente E2E (a43 20 account-days con fills por día pinneados + fresh-process determinism). MIXED_MINUTE: NO_IMPLEMENTADO (no existe autoridad por minuto en el manifest; declarado, no simulado). Cobertura integral de los 13 contratos: sin cambios respecto a la frontera S01 (FAIL_VISIBLE_GAPS_V1); rollover E2E sintético existente intacto; la CLI no finge multi-contrato (rechaza ≠1 stream).

### Matriz R1–R5

| Req | Resultado | Evidencia |
| --- | --- | --- |
| R1 continuidad | CUMPLIDO | ReplaceAccount + walker de sesión del run + seed de venue; tests de burn/pausa/continuidad/replay |
| R2 intrabar+scaling | CUMPLIDO | OHLC_CAUSAL_PATH_V2 + adds E2E + V1 golden intacto; costo medido y declarado |
| R3 sustitución+paridad | CUMPLIDO (strategy-seam parity; differential vertical → S04) | CompositionOptions + tests de sustitución + RuntimeStrategySeamParity |
| R4 piso estático | CUMPLIDO | STATIC_LOCK + tests + perfil derivado de config |
| R5 cobros/terminales | CUMPLIDO | collected-vs-requested + pending-at-horizon + terminales honestos, tests |

## Fuentes

- Instrucción Owner 2026-10-07 (devolución correctiva), [[BTG-S03-OWNER-MANDATE-20261006]], [[BTG-S02-DESIGN]], [[BTG-PLAN]].
- Producto: codex/btg-s03-remediation @ adfe4087; workspace ~/aranea/work/btg-s03-remediation/reports/.

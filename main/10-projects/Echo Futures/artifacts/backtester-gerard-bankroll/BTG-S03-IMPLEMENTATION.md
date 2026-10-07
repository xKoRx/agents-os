---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
project: "[[Echo Futures]]"
related: ["[[BTG-PLAN]]", "[[BTG-S02-DESIGN]]", "[[BTG-S03-OWNER-MANDATE-20261006]]"]
aliases: []
tags:
  - kind/doc
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S03-IMPLEMENTATION

## Propósito

Candidato ejecutable de los DOS modos del mismo backtester (BASIC 100k continuo y CAMPAIGN caja 5000/compra 120/hasta 4 cobros) con Strategy/MM intercambiables por los seams existentes, ejecutado sobre histórico NQ real y con pruebas focalizadas. Rol: implementation lead TOP LOCAL ONE-SHOT; superficie ZCode (GLM), host no expone identificador exacto de modelo. Devuelve CANDIDATE_READY_FOR_PRIMARY_REVIEW; no ejecuta el adversarial S04 ni autoadjudica gates. Mandato Owner: [[BTG-S03-OWNER-MANDATE-20261006]].

## Contenido

### Estado y autoridades

PROGRAMA = BTG-PLAN five shots; este cierre corresponde a S03 (implementación). CURRENT_TASK_STATE = S03_CANDIDATE_READY_FOR_PRIMARY_REVIEW. Fecha de cierre: 2026-10-06 America/Santiago (dentro de la ventana Owner 6–7 oct). Producto: xKoRx/echo carril `codex/btg-s03-implementation`, baseline 77e188bc (S01 real diagnostics), tip final `c1c0e7d4` pusheado; corridas reales ejecutadas en `b531acfa` (binary SHA256 `812a2d36a1102f3eef191ed05e64de06fb448c28057942d520b0d7ecf5f68814`); el delta posterior `c1c0e7d4` agrega sólo superficie config de gerardmm (`ExplicitNoAdds`) + tests, sin cambiar el run path ejecutado (suites gerardmm/backtester/core verdes post-cambio). Agents-OS master: limpieza de rama + mandato + delta registrados en c3f8c36e / 8b3882e4 (+sync cron).

Prioridad Owner aplicada: engine correctness sobre ROI; T30/holdout/ranking SUPERSEDED_BY_OWNER_SCOPE (no PASS); T38 acotada a propagación de configuración; resultado económico negativo aceptado como resultado válido.

### 1. Limpieza administrativa (mandato /execute 1)

Rama `codex/btg-s02-design-cloud-20261006` retirada de xKoRx/agents-os: feedback original recuperado desde el tip verificado 00514fe65d0b4a06975096de17a3c2246d573c92 a master (commit c3f8c36e, fast-forward con control de concurrencia y readback), eliminación remota ejecutada sólo tras verificar el tip inmóvil, 0 refs remanentes local+remota tras prune, sin PR asociado (búsqueda gh), sin topar ramas/PR ajenos. El diseño v1 de esa rama queda como historia supersedida por el diseño reparado en master. AGENTS_OS_OLD_BRANCH_CLEANUP = DELETED_VERIFIED.

### 2. Delta Owner registrado (mandato /execute 2)

[[BTG-S03-OWNER-MANDATE-20261006]] creado (contrato prompt); [[BTG-PLAN]] sección 9 registra el delta vigente (engine correctness, módulos intercambiables, ROI fuera de alcance, F3 sin búsqueda de rentabilidad); change_log único `80-agents/journal/logs/2026-10-06-echo-futures-btg-s03-owner-delta.md`. Sin otra ronda de arquitectura: el diseño S02 reparado se implementó tal cual con las precisiones del mandato.

### 3. Implementación de producto (commit 8e320b9c + fixes 4fd9ac6d/b531acfa/c1c0e7d4)

| Delta | Contrato | Evidencia |
| --- | --- | --- |
| `strategy.WarmupReadiness` (SDK nuevo, opcional por módulo) | El driver OHLC ya no decodifica s2.State ni hardcodea 51/20; S2 declara su propia readiness (períodos + elegibilidad temporal H4) por el contrato; módulos sin el contrato conservan el gate genérico de cero evaluaciones | v3/sdk/futures/strategy/readiness.go; s2.ReadyFromState; ohlc_driver.requireNativeWarmup reescrito |
| `ScalingMode` explícito NO_ADDS/CONFIGURED en config SDK | Tabla S02 §4: NO_ADDS+bloque rechaza; CONFIGURED sin bloque rechaza; modo desconocido rechaza; ausente+bloque normaliza CONFIGURED; ausente sin bloque en LIVE sigue rechazando; NO_ADDS explícito compone también en LIVE vía gerardmm.Config.ExplicitNoAdds (el nil implícito sigue denegado en LIVE) | config/snapshot.go, config/mm.go, gerardmm/config.go; TestBTGS03_ScalingModeResolution |
| Campaña (backtester/campaign.go) | Caja personal exacta (rationals), compra ON_DEMAND 120, pass→FUNDED vía ACCOUNT_CONTEXT_TRANSITION (RESET_ADJUSTMENT + START_NEW_STAGE + risk seed 98000 + re-arm de entradas) y payouts vía ACCOUNT_CASHFLOW PAYOUT_DEBIT con pausa/reanudación de binding, retiro al 4.º cobro con residual forfeited, burn por breach (EOD trailing, familia única soportada V1), reemplazo con continuidad F1 | campaign.go; re-arm simétrico en run.applyContextTransition |
| Perfil `BTG_FUNCTIONAL_NQ_CAMPAIGN_V1` | FUNCTIONAL_ASSUMPTIONS declaradas (piso modelado EOD trailing 2000 desde INITIAL_BALANCE; FUNDED INITIAL/STEADY rows materializadas; split 100%/fee 0; terms EVALUATION 3000/2 días; warmup prefijo sólo cuenta 1) | campaign_profile.go |
| CLI `echo-backtest campaign` | Input JSON sellado (schema echo.backtest.campaign.input.v1), exports por cuenta (spool sellado + runspec seal) + campaign-result.json con curva de caja, compras, payouts, reconciliación y reemplazos | cmd/echo-backtest/campaign.go |
| Módulo fixture `FIXTURE_BAR_CLOSE_SCRIPT_V1` (sólo backtester, config.ModuleFixture) | Sustitución de Strategy sin tocar el motor; runtime (futuresruntime) NO lo resuelve → sin superficie LIVE | fixture_strategy.go; compose.moduleFor |

Continuidad F1: el reemplazo recompone sólo el compartimento de cuenta (ledger/venue/operation/MM/provider nuevos con identidad propia) e inyecta en memoria los OwnerState de Strategy del run anterior antes de consumir inputs; el warmup genérico se omite por diseño cuando WarmupStart==TradeStart (runs hijos) y la cuenta 1 conserva el prefijo único del experimento. DESVIACIÓN DECLARADA: el estado market/analytics NO se traslada entre runs — la máquina de regiones de sesión V1 no resumible entre runs (demostrado: ANALYTICS_SOURCE_FAILED al intentarlo); la continuidad técnica de S2 es autocontenida en su ModuleState y ningún camino de decisión de los perfiles funcionales lee los rings; los rings acotados se reconstruyen por cuenta.

### 4. Pruebas focalizadas (v3/backtester/btg_s03_test.go, todas PASS)

- TestBTGS03_StrategySubstitutionRunsSameEngine: mismo corpus, cambio de UN campo (module s2→fixture): S2 falla cerrado por SU readiness (need_h4=51 vía contrato, no literal) y el fixture opera — sustitución + requisitos respetados por el mismo motor.
- TestBTGS03_MMSubstitutionConsumesContract: MM alternativo inyectado por el mismo seam de composición (operation.NewEngine) → cero fills/economía; GerardMM opera el mismo corpus.
- TestBTGS03_MMParametersChangeEconomics (T38): TP de plan rows 1500→1 con todo lo demás congelado cambia la configuración efectivamente consumida (netos distintos; rows digest distinto).
- TestBTGS03_CampaignCashBurnAndReplacement (T18/T33/T34 acotado): compra 5000→4880 exacta, burn sin segundo débito, reemplazo con OwnerState continuado (sin re-warmup), segunda compra; caja conciliada.
- TestBTGS03_CampaignPassPayoutCapAndForfeit (T20/T21/T22 acotado): PASS 2 días/+3000 → transición FUNDED (sin segunda compra), 4 cobros de 1500 con pausa/cobro/reanudación, retiro al cuarto, SIN quinto payout, residual forfeited 2253, reemplazo idle; caja 5000−2×120+6000 = 10760.
- TestBTGS03_CampaignDeterministicReplay + TestBTGS03_ScalingModeResolution (T12): replay byte-idéntico in-process; tabla de resolución fail-closed.
- Suite completa verde post-delta: v3/sdk/... ok, v3/core/... ok, v3/backtester ok (849s; primer intento con timeout default de go test de 10m abortó por el test lento a52 — re-run con -timeout 40m PASS, no es falla de producto).

### 5. Corridas reales (workspace ~/aranea/work/btg-s03-20261006/reports, offline unshare sin red, sin -race)

BASIC_REAL (perfil BTG_FUNCTIONAL_NQ_EVAL_V1 intacto, spec preparado S01, ventana NQZ3 2023-10-29T22:00Z→2023-11-23T03:29Z, warmup desde 2023-10-15T22:00Z): RunID `bt-bd627d8a82e7faf07c5f17c0e89e60352d46abd882e64fa7286f99fd0430029f` — IDÉNTICO al golden S01; artefacto sellado SHA256 `b11bd4e7776762523f29c9dda8e264c98818f5e209c7b051e72e6e671222a637` — BYTE-IDÉNTICO al sello S01; 113 operaciones materializadas / 78 fills / neto −34.293,32 USD (−27.650 gross / 6.643,32 costos); COMPLETE con residuales REPORT_RESIDUALS declarados; wall 7m12.14s, maxRSS 573.268 KiB. Reproduce proceso fresco: IDENTICAL (270.781 records; wall 8m59.77s, maxRSS 531.368 KiB). El refactor de readiness no alteró V1: golden preservado byte a byte (T01).

CAMPAIGN_REAL (perfil BTG_FUNCTIONAL_NQ_CAMPAIGN_V1, misma ventana y dataset derivado, cfg 5000/120/1500/4/100000/98000/3000/2 días, NO_ADDS): campaña `btg-NQZ3-20231029`; 3 compras aplicadas; caja 5000→4640 (reconciliada: 5000−3×120+0); cuenta 1 BURNED_RISK_BREACH 2023-10-31 (balance 97.997,72; 14 fills/10 ops); cuenta 2 BURNED_RISK_BREACH 2023-11-08 (98.001,76 — piso EOD trailing remontó por watermark, desviación declarada); cuenta 3 ACTIVE_AT_HORIZON al 2023-11-23T03:29Z (98.000,94; 4 fills/62 ops); 0 cobros (la estrategia pierde en la ventana: resultado negativo válido bajo el mandato); replacements=2 con OwnerState continuado (sin re-warmup, sin señales backlog); wall 3m49.67s, maxRSS 214.608 KiB; replay de campaña BYTE-IDÉNTICO (campaign-result.json SHA256 `d499b2ab2455af26040b11493d56eaac0394a95593f6d7ff1fe2c6bb4f33afc5`); artefactos por cuenta sellados bajo campaign-real/bt-c-*/.

### 6. Alcance, no-ejecutados y desviaciones (para S04/S05)

- RUNTIME_PARITY_SCOPE: paridad demostrada como mismo-motor (golden byte-idéntico; sustituciones por los seams del runtime; fixture comparado en ambos sentidos). El harness dedicado runtime-vs-backtest con fills inyectados (T02 completo) NO se construyó en S03: queda superficie de falsificación para S04.
- OHLC V1 se conserva (fidelidad UNOBSERVED_MODELED/SL_FIRST_NEXT_OPEN declarada en cada artefacto); el path intrabar V2 del diseño (lattice lazy + T35/T36) NO se implementó: T35/T36 = NOT_APPLICABLE (ningún atajo nuevo; V1 intacto y su repro demostrada), no PASS.
- CONFIGURED adds: resolución config completa y fail-closed; la EJECUCIÓN de adds intrabar en OHLC V1 sigue rechazada por diseño (OHLC_SCALING_UNSUPPORTED); adds reales (T13/T14) no re-ejecutados en este shot (quedan los tests gerardmm existentes; la E2E de adds vía TRADE path es superficie S04/S05).
- Ticks/MIXED: NOT_RUN_DATA_UNAVAILABLE (sin corpus de ticks; no bloquea OHLC). Rollover histórico: no ejercitado en las corridas reales (un contrato); rollover E2E sintético existente intacto.
- Cobertura integral 13 contratos: sin cambios respecto a la frontera S01 (FAIL_VISIBLE_GAPS_V1 detiene en missing-open; corridas acotadas a NQZ3 derivado); COMPLETE acotado al horizonte pedido, no gate integral.
- Campaña real usó la política FUNCTIONAL_ASSUMPTIONS (piso EOD trailing vs piso estático del diseño: desviación declarada en perfil y artefacto; el Owner itera los valores/reglas después).
- Ejecución_state INCOMPLETE de cuentas quemadas/retiradas antes del horizonte: sello honesto de no-horizonte; el outcome de negocio vive en campaign-result (BURNED/RETIRED), no se maquilla a COMPLETE.

## Fuentes

- [[BTG-S03-OWNER-MANDATE-20261006]] y [[BTG-PLAN]] §9 (delta vigente).
- [[BTG-S02-DESIGN]] (diseño reparado implementado) y evidencia S01 (codex/btg-s01-evidence @ e4a177eb; [[BTG-S01-REAL-GERARD-RESULT]]).
- Producto: xKoRx/echo `codex/btg-s03-implementation` @ c1c0e7d4 (commits 8e320b9c, 4fd9ac6d, b531acfa, c1c0e7d4; pusheado).
- Artefactos físicos: /home/kor/aranea/work/btg-s03-20261006/reports/ (basic-real, basic-real-reproduce, campaign-real, campaign-real-replay, campaign-input-nqz3.json, bin/echo-backtest SHA256 812a2d36…f68814).

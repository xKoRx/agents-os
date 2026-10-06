---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-S01-OHLC-RUN-CONTRACT]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01 — Forensics de cobertura real NQ 1m

## Propósito

Resolver el primer SOURCE_COVERAGE_INCOMPLETE real, medir ventanas con warmup completo usando el Calendar y SessionGrid compartidos, y separar datos ausentes de defectos de diagnóstico. Scope ONE-SHOT TOP LOCAL Codex gpt-6.1-sol, sin subdelegación. No se cambia S2, GerardMM, costos, account-day, roll, calendario ni políticas de gaps; no se acepta una campaña ni se certifica BT-S04.

## Contenido

Estado: strict halt del primer gap CORRECTO; cobertura íntegra que cruce todos los gaps internos de los13exports BLOCKED bajo FAIL_VISIBLE_GAPS_V1; BT2-F12 FIXED_WITH_REAL_RERUN: ambos failed slices conservan el rechazo, records/state/economics y fresh reproduce IDENTICAL. BT2-F13/F14 de summary counters/residual terminal quedan FIXED_WITH_REAL_RERUN: smoke raw corregido COMPLETE y fresh reproduce IDENTICAL, con24fills/30operaciones y sin residual operativo terminal. Binario candidato F12/F13/F14 desde xKoRx/echo commitd69d03eceeac1495522473a95baf08087f5c28b3, SHA25679bd5f2aab74c242dbece8ebd274975c94d37100d18af80103e3c44d62e69839. Es evidencia de implementación acotada, no aprobación de gate.

### Primera divergencia física

NQ 12-23.Last.txt SHA256caead986337256d77011d58cb49d4d4b20393b1261c0f1ef4c494cd0397c6c94, 68.777 rows. Línea8416 termina2023-10-10T00:16Z; línea8417 termina00:19Z. Faltan end-minutes00:17 y00:18, por tanto intervalos[00:16,00:17) y[00:17,00:18). El primer intervalo es lunes19:16Chicago, dentro de la sesión del snapshot weekly17→16. Los refs prev/next del artifact original son ntminute:4ccbec72f0e4388a0c12c8d64f5a7456c97beb6518140df2d15b6e91d8fe7e63 y ntminute:1a2308f359132edd885ca35ce8d5ed472edfbdf772dcceb0a0d02239a960a7d3. Runbt-862144ea…f97c consumió8.415 source bars,18.561 roots,52.238 records,FAILED sin fills/operations y balance100.000USD. El guard detuvo en00:16 antes de admitir la siguiente barra.

El contrato OHLC aceptado permite detener el slice al primer gap material; readiness y agregados evaluables no pueden esconder missing minutes. El export Last por sí solo no atribuye ausencia a no-trade, interrupción del proveedor ni feriado. Causa subyacente UNKNOWN. No se registra esta ausencia como bug de código.

### Segunda divergencia y BT2-F12

El slice warmupOct10T00:33Z / tradeOct22→29 NO falló inmediatamente. Sus33.308 records llegan aOct13T20:59Z. Después de línea13797=endOct13T21:00Z, línea13798=endOct15T04:33Z tiene OHLC15107.5/volumen2 (sábado23:32–23:33Chicago) y línea13799=endOct15T20:10Z tiene OHLC15107.5/volumen1 (domingo15:09–15:10Chicago). Ambos intervalos están fuera del weekly declarado. El rechazo de sesión es correcto; la procedencia económica de esos prints queda UNKNOWN. La última barra válida estaba abierta[Oct13T20:59,21:00) cuando el lookahead inválido detuvo el motor.

BT2-F12 es defecto de diagnóstico: Finish usaba caller frontier para FAILED aunque el clock y los records habían avanzado; además nextRoot-error atribuía la validación al mismo frontier y podía omitir el ref/intervalo del source rechazado. El fix mantiene caller frontier/scheduler y sólo reporta clock alcanzado para FAILED, clock alcanzado en nextRoot-error y source_ref/stream/intervalo ofensivo en el cause. No afirma que el source rechazado haya sido consumido. Regresiones RED→GREEN, race y vet focalizados pasan; real gap rerunbt-2b7e9fc2cb026457b303c8c32a557bc1c117b8b060775961afda076b6fad39f4 conserva52.238records y clockOct10T00:16Z; outside-session rerunbt-e036b4f09404a8f588f5b50a08dcdee0495b6389f1c353eab2f372bab4b16fd7 conserva33.308records, clockOct13T20:59Z y refntminute:c43f2f9c050a75647ec4f61e87897df120bd46646e0cd12cad9975e7b9060fab/intervaloOct15[04:32,04:33). Freshprocess reproduce de ambos devuelveIDENTICAL; código/SDD aislados en branchcodex/btg-s01-real-diagnostics. Existing tests intactos.

### Taxonomía observable

- CALENDAR_ONLY_CLOSURE: salto físico íntegramente explicado por el Calendar semanal; no exige barra sintética.
- MISSING_OPEN_INTERVAL: al menos un intervalo1m ausente que el Calendar espera abierto; cause proveedor/no-trade/feriado UNKNOWN.
- OUTSIDE_DECLARED_SESSION_SOURCE: barra física real cuyo intervalo no pertenece a región negociable del snapshot; no es un gap rellenado ni autorización para cambiar el calendario.
- PARTIAL_PREFIX: inicio de export/slice dentro de un agregado; el motor conserva INCOMPLETE_PREFIX y excluye de Signal/readiness el agregado cuya secuencia de refs no cubre BucketOpen→CloseBoundary.
- EXPORT_TAIL: horizonte elegido posterior al último intervalo completo; requiere cobertura explícita, no extrapolación. Diciembre2026 es export parcial hastaOct6; no se infiere resto del trimestre.
- DUPLICATE_OR_REVERSE: contador físico observado0 en los13 exports.

### Inventario RAW y warmup máximo

1.096.336 rows /57.457.558bytes;24.831 minutos esperados abiertos ausentes entre rows;226 rows fuera del weekly. Estas cifras son relativas al snapshot congelado sin overrides; no son una afirmación del horario histórico oficial CME ni prueban causa de feriados. El helper usa directamente sdk/futures/calendar.Resolver y sdk/futures/bars.SessionGrid.RegionAt; no implementa otro motor, trades, risk ni PnL. Corta segmentos ante missing-open o source fuera de sesión y cuenta sólo regiones cuyos intervalos fuente cubren íntegramente open→close. H4 incluye la región final truncada por Calendar, conforme al grid real.

| Export | Rows | Gaps abiertos | Minutos ausentes | Rows fuera sesión | H4 completas máximas | Segmentos ≥51H4 |
|---|---:|---:|---:|---:|---:|---:|
| NQ 03-24.Last.txt | 88987 | 190 | 3573 | 40 | 60 | 1 |
| NQ 03-25.Last.txt | 88215 | 170 | 4304 | 18 | 48 | 0 |
| NQ 03-26.Last.txt | 88617 | 286 | 3922 | 19 | 115 | 1 |
| NQ 06-24.Last.txt | 97534 | 198 | 1965 | 19 | 83 | 2 |
| NQ 06-25.Last.txt | 90602 | 223 | 1954 | 36 | 54 | 1 |
| NQ 06-26.Last.txt | 89946 | 270 | 1193 | 1 | 146 | 4 |
| NQ 09-24.Last.txt | 91385 | 55 | 1024 | 9 | 56 | 1 |
| NQ 09-25.Last.txt | 91064 | 201 | 1355 | 20 | 49 | 0 |
| NQ 09-26.Last.txt | 94569 | 627 | 1971 | 1 | 274 | 2 |
| NQ 12-23.Last.txt | 68777 | 5 | 469 | 6 | 90 | 2 |
| NQ 12-24.Last.txt | 91773 | 107 | 647 | 20 | 90 | 2 |
| NQ 12-25.Last.txt | 90626 | 277 | 1808 | 37 | 34 | 0 |
| NQ 12-26.Last.txt | 24241 | 239 | 646 | 0 | 66 | 1 |

Antes de la derivación autorizada, los RAW NQ03-25(max48H4),09-25(max49H4),12-25(max34H4) no ofrecen una secuencia estricta suficiente para S2 defaults; la insuficiencia puede provenir de prints fuera de sesión que cortan segmentos, además de gaps internos. Esta conclusión se limita a RAW sin exclusiones y no se reutiliza como blocker del dataset derivado. El código ya soporta CalendarOverride fechado y el SDK conserva agregados parciales visibles; no existe policy de run que reanude después de missing-open bajo este freeze. Inventar overrides a partir de huecos, saltar source guards, interpolar, resetear cuenta o sumar PnL de slices no satisface el baseline.

### Derivación autorizada por Owner

Owner autorizó preparación derivada usando el Calendar configurado, excluyendo únicamente SourceBars cuyo intervalo completo queda fuera de su región negociable. Los originales permanecen intactos. El helper existente agrega modo de salida determinista NT sameformat: conserva byte por byte cada línea retenida, incluyendo newline; no reescribe OHLCV ni timestamp. Manifest exhaustivo incluye SHA/bytes/counts originales y derivados, más originalfileSHA:line, raw-lineSHA, start/end y razón por exclusión. Verificación independiente comprobó cada derivado como subsecuencia exacta de bytes originales y todos los SHA/ref de exclusiones.

Excluidos226 source rows; retenidos1.096.110. Gaps intrasesión y sus24.831 minutos ausentes permanecen; no se etiqueta un missing-open como closure. SourceOrdinal del derivado puede diferir del original y su identidad/digest es nuevo, explícitamente documentado; los refs de manifest enlazan a los originales. Evidence externa reports/real-gap-forensics/derived-nt-weekly-v1/exclusions-manifest.json+verification.json y derived-inventory.json.

Después de excluir sólo source fuera de sesión, TODOS los13 derivados tienen segmentos con≥51H4 reales. Esto permite smokes individuales por calidad, sin asegurar un run continuo por los13 períodos completos, donde los gaps internos siguen siendo materiales.

| Export derivado | H4 máximas | Inicio del segmento | Ready-at51H4/20M5 | Fin del segmento |
|---|---:|---|---|---|
| NQ 03-24.Last.txt | 85 | 2024-02-19T23:00:00Z | 2024-03-01T11:00:00Z | 2024-03-11T03:00:00Z |
| NQ 03-25.Last.txt | 89 | 2025-02-24T06:17:00Z | 2025-03-06T19:00:00Z | 2025-03-17T03:00:00Z |
| NQ 03-26.Last.txt | 115 | 2026-02-16T23:00:00Z | 2026-02-27T11:00:00Z | 2026-03-16T03:00:00Z |
| NQ 06-24.Last.txt | 83 | 2024-04-12T04:51:00Z | 2024-04-24T18:00:00Z | 2024-05-02T04:14:00Z |
| NQ 06-25.Last.txt | 154 | 2025-04-20T22:00:00Z | 2025-05-01T10:00:00Z | 2025-05-26T17:00:00Z |
| NQ 06-26.Last.txt | 146 | 2026-04-21T05:42:00Z | 2026-05-01T18:00:00Z | 2026-05-25T17:00:00Z |
| NQ 09-24.Last.txt | 56 | 2024-08-05T14:48:00Z | 2024-08-16T06:00:00Z | 2024-08-19T02:39:00Z |
| NQ 09-25.Last.txt | 89 | 2025-07-08T23:15:00Z | 2025-07-21T14:00:00Z | 2025-07-29T23:18:00Z |
| NQ 09-26.Last.txt | 274 | 2026-07-05T22:00:00Z | 2026-07-16T10:00:00Z | 2026-09-07T17:00:00Z |
| NQ 12-23.Last.txt | 192 | 2023-10-10T00:31:00Z | 2023-10-20T14:00:00Z | 2023-11-23T03:29:00Z |
| NQ 12-24.Last.txt | 144 | 2024-10-22T04:30:00Z | 2024-11-01T18:00:00Z | 2024-11-25T07:16:00Z |
| NQ 12-25.Last.txt | 197 | 2025-10-13T17:51:00Z | 2025-10-24T06:00:00Z | 2025-11-27T18:00:00Z |
| NQ 12-26.Last.txt | 66 | 2026-09-21T00:00:00Z | 2026-10-01T14:00:00Z | 2026-10-06T03:50:00Z |

El derivadoNQZ3 conserva68.771rows, SHA25685d88ed0b2df3ab6435546676ba49549cfce5cec75495552a28edd13860e7750 (6exclusiones). Su segmento mayor esOct10T00:31Z→Nov23T03:29Z,192H4, listoOct20T14Z; el warmup alineadoOct15T22Z permite ampliar el mismo account desde tradeOct29 sin reset/PnLsum hasta el primer gap interno. Root/NORMAL poseen ejecución/config/artifacts de ese run.

### BT2-F13/F14 — resumen frente a hechos reales

El smoke raw COMPLETE bt-0049ea259d5b853e3ef4504f6330790048e5401c966d98d8a191b9b5b1ad5fb0 contiene24fills únicos por(account,provider_execution_id),30operations materializadas(CREATED IDs) y12operations con fills. Los campos summary.fills/operations incorrectamente siguen0/0. La Operation final retenida es TERMINAL/MM_NO_ACTION: su ID existe para auditoría, sin exposición; reportarlo como residual de operación activa es falso.

Root extendió SDD/AllowedFiles para un getter Ledger.FillCount O(1) sobre dedup permanente, operaciones desde el cursor canónico IssuedOperationIDs y residual sólo para status distinto de TERMINAL (nil conservado como desconocido). No se usa Owner.CrossOperationFillDedup FIFO4096 ni copiar todos los mark revisions para contar. RED real-model fixture prueba2fills/1op versus0/0, terminal residual falso, duplicate physical fill sin doble economía y materialized-never-filled con residual activo. Getter test valida0,qty≠fillcount,duplicate/conflict,context/day continuity y read-only. GREEN full51H4 semantic tests PASS86.666s, terminalcheck old-finishoverlayRED48.789s, short diagnostic/getterrace PASS1.151s/1.026s, vetsPASS; getter100% statementcoverage. Real COMPLETE rerun y fresh reproduce observados abajo. El primer oráculo stop-fill⇒TERMINAL era incorrecto: flat sin termination intent conservaACTIVE y residual legítimo. Se corrigió newtest a MMtarget-close constatusTERMINAL explícito; existingtests intactos. La fullwarmuprace llegó timeout10min y queda FAIL visible, no tratado comoPASS.

El candidato corregido raw bt-b9676b4bb62b7ed7dbd30a626209b0ead77f92672c5b6754b9fef6ade10e4d44 es COMPLETE con136.932records,20.700SOURCE_CLOSE únicos,24fills/30operaciones, balance/equity90.029,30USD, gross−8.900USD, costes1.070,70USD/net−9.970,70USD y unrealized0USD; residual sólo account_day_open:ad-20231102 +stage_open. Economía, ledger/risk digest coinciden con original; provider digest y refs cambian con RunID. Censo recursivo de records encuentra sólo IDs/ref/provenance distintos, sin cambios de tiempos/precios/qty/dinero; no se afirma igualdad byte entre builds. Freshprocess reproduce del nuevo RunID devuelveIDENTICAL=true. Root/NORMAL poseen artifacts smoke-clean-long-candidate y reproduce-smoke-clean-long-candidate; reports/real-gap-forensics/real-counters-candidate-comparison.json conserva censo reproducible. FIXED_WITH_REAL_RERUN es evidencia de implementación, no gate independiente.

### Candidato smoke por calidad, no PnL

NQZ3 warmup2023-10-15T22:00Z alcanza51H4 completas y20x5m a2023-10-26T10:00Z y sigue íntegro hasta2023-11-03T21:00Z, con90H4 completas. Candidato operable trade2023-10-29T22:00Z→2023-11-03T21:00Z; alternativa más corta29→31octubre. La elección usa sólo source/calendario/warmup; resultado de trading permanece propiedad Root. Causal eligibility requiere closeH4≤5mBucketOpen; empezar después del ready-at elimina el borde simultáneo. El dataset permanece unmodified.

Evidence externa reusable: workspaceBTG-S01, reports/real-gap-forensics/probe/main.go+go.mod (comando inventory offline), inventory.json (gaps y segmentos con líneas), inventory-summary.tsv (bytes/SHA/taxonomía por archivo), quality-window-candidates.tsv (todas las ventanas suficientes, sin selección por economics), diagnostic-red/green/race/vet.log y real-reruns/. Los comandos están aislados de red; el helper no evalúa Strategy/MM. No se copia dump pesado al vault.

### Límites y siguiente paso

OHLC_1M_MODEL_V1 /SL_FIRST_NEXT_OPEN_V1 modela intrabar no observado; NO_ADDS conserva baseline funcional; sin equivalencia ticks/LIVE, campañas/bankroll ni checkpoints/resume. Gaps, prints fuera de snapshot y insuficiencia warmup son límites materiales visibles. Para un13-file longitudinal que cruce TODOS los gaps internos, Root/Owner necesita cobertura real distinta o una decisión explícita del contrato de recuperación frente a gaps; eso es frontera producto/datos, no bug probado del halt. No se diseña esa extensión en este shot.

Cierre de ONE-SHOT por delta: artifact+change_log+agent_run; feedback de fricción real (oráculo inicial/timeout; sin candidato reusable de comportamiento), REUSABLE_BEHAVIOR_CANDIDATES:NONE. No cambios de skills, memoria ni cuota ChatPro; ejecución Codex no implica consumo ChatPro. Root mantiene el proyecto/plan/resultado y gate.

## Fuentes

- [[Echo Futures — BT-S01 Backtester V1 Design]] — identidad, causalidad, Calendar/data coverage y separación feed/analytical readiness.
- [[Echo Futures — BT-S04 Final Remediation and Certification]] — límites V1, preservación successful semantics y evidence explícita.
- [[BTG-S01-OHLC-RUN-CONTRACT]] — first-gap strict halt,51H4/20x5m, partial diagnostics y datos reales.
- xKoRx/echo@fb210ac4: v3/backtester/ohlc_driver.go, driver.go, finish.go, v3/sdk/futures/calendar/resolver.go, bars/grid.go, analytics/engine.go y strategies/s2/s2.go.
- xKoRx/echo@970f1d52: specs/btg-s01-real-diagnostics y v3/backtester/real_failure_frontier_test.go.
- Originales Owner NinjaTrader Last1m UTCend-minute y artifacts sellados Root en workspaceBTG-S01 reports/real-history-execution; transferencia bytes verificables en history/nq/nq.

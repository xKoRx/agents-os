---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[A — Product Contract — The Lab]]"
  - "[[B — Architecture Decision Report]]"
  - "[[E — First Usable Vertical Slice]]"
aliases: []
tags:
  - kind/doc
  - area/echo
created: "2026-09-22"
updated: "2026-09-22"
---

# C — Reality and Gap Matrix

> **Evidencia acotada al 2026-09-22.** Se reutilizan certificaciones anteriores sin repetir pruebas. `SOURCE`/`DEV`/`PHYSICAL`/`PROD`/`USABLE` no son sinónimos. Los datos de ambientes son snapshots documentados, no verificaciones nuevas. Consultar [[B — Architecture Decision Report]] para decisiones, [[D — Revised Roadmap]] para el plan. No se accedió a infraestructura, MCP, datos productivos, brokers ni repos completos.

## Matriz de evidencia por capacidad

| Componente / afirmación | Fuente específica y corte | Source/contract | Física documentada | PROD actual | Usable para The Lab y brecha |
|---|---|---|---|---|---|
| Echo SDK S0 shared semantic types, `NormalizedOperationV1`, Scope, TradeSet, MetricSet, digest | `xKoRx/echo@5dd998f1:v3/sdk/contracts/analytics.go`; [[Echo — E-01 Canonical SDK Foundation S0]]; [[Echo SDK — Canonical Contract Final Freeze Review — Fable 5.1]] | E-01 CONTRACT_PASS; IDs TradeSet derivados inputs no output; semantics exactas | E-01 source/fixtures certificadas en notas | No nuevo deploy afirmado | Foundation KEEP. No HistoryRevision ni curva temporal extensible demostrada. |
| E-04 Forge promotion ingestion | `xKoRx/echo@5dd998f1:specs/FEAT-FORGE-INGESTION-E1/SPEC.md`; [[Echo — E-04 Forge Ingestion E1]] 2026-09-21 | Implementation/contract integrado; existing receipt `INGESTED` sin analytics | CERT-E04-01 / CERT-F04-03 PASS DEV con 5 golden handoff bodies, cinco 201 + replay 200 + GET 200 + conflicto 409 + no efectos | PROD sin nuevo certificado; Gateway DEV sí documentado | Operative ingestion YES; SQX+MT5 individual operations/historical admission NO DEMOSTRADO. 201 no es history ready. |
| Forge F-01/F-02/F-03 and F-04 | [[Echo Forge — Factory V2 Completion]] 2026-09-21, [[Echo Forge — F-04 Magic allocation, version seal and handoff]] | F01/F02/F03/F04 CLOSED según proyecto y F04 producer | CERT-F04-01/02/03 y E04 join PASS documentados | Deployed no presumido fuera de evidencia por versión | Reusar factory y handoff; ampliar manifest/version metadata con dual per-trade history references sólo si extracción auténtica comprobada. |
| Forge F-05-C golden FULL | [[Echo Forge — Factory V2 Completion]] 2026-09-21; `xKoRx/symphony@745bc8b` commit release matrix | F-05-I read surface SOURCE verified; V2 release 0.2.105 | `CERT_F05_01/02/03_PASS`, campaña FULL `0ce72173…`, 3 finalistas, HTM byte-verificados según nota | Factory V2 PHYSICALLY_CERTIFIED en alcance documentado, no traduce a Lab | Primer candidato real disponible por certificado; no afirmar que HTM sea trade list ni que los dos históricos cubran [−∞,A)/[A,B). H0 debe inspeccionar por candidato. |
| E-05 analytics foundation | `xKoRx/echo@5dd998f1:specs/FEAT-ANALYTICS-CONVERGENCE-A0/SPEC.md`, `v3/sdk/analytics/calculator/calculator.go`, [[Echo — E-05 Analytics Convergence A0]] Sep16 | Writer/canonical TradeSet/MetricSet/calculator fuente integrada, Verifier #4 PASS | DEV PostgreSQL 063 aplicado; Hasura readonly SELECT smoke PASS; en ese snapshot 0 filas, worker no lanzado | PROD NOT DEPLOYED al snapshot; estado actual no revisado | Fundación reusable, NO historia SQX+MT5 publicada, NO operación indexada para consultas, NO curva temporal N, NO UI usable certificada. |
| Lab legacy / Lab Clean | SPEC E05 §3 y [[Echo - Reporte de Estado Lab y Journal 2026-08-21]] | Journal, outcomes, snapshots, front read paths existentes; `ReplaceByScope` mutable; Lab R AUTO; recorded window distinta | Datos/bugs documentados en auditorías anteriores; no repetidos | Registro histórico no inventariado ahora | Mantener journal operacional como autoridad; snapshots, curves y chart antiguos NO canónicos: versión NULL, win_rate 0..1 pintado `%` sin ×100 en componente, default USD y ejecución por INNER JOIN omite missing. Reemplazo de lectores semánticos después de paridad. |
| E-06/E-07 Reference, facts, coverage | [[Echo — Live Platform V1]] 2026-09-21; [[Echo — E-10 Strategy Quality and Eligibility]] M6/M7 | Contratos y captura versionados implementados en feature consolidada, provenance canónica, coverage UNKNOWN-first | PHYSICAL_PENDING para productor/Reference real según proyectos | No nueva inferencia | Fuente REAL preparada en source; REAL no se publica con fixtures/silencio. Primer slice puede marcar REAL UNKNOWN y diferir integración observada. |
| E-08/E-09 economic routing and Execution Fidelity | [[Echo — Live Platform V1]] 2026-09-21, feature @ `8655320` | SOURCE APPROVED para E08 C3 y E09 C2; conservan required expected command set, no INNER JOIN | PHYSICAL_PENDING; activación económica pendiente | No afirmado | KEEP separado de estrategia y de historia SQX/MT5; E09 no debe bloquear desarrollo E10 ni first slice. |
| E-10 Strategy Quality | [[Echo — E-10 Strategy Quality and Eligibility]] Sep22 M7 @ `1485baa4` | T05 forward derivation/integrity M7-R1…R5 fixed; exact decimal, real fact refs, one snapshot | Fixture/harness físico descartable documentado; Reference LIVE real y policy certification pending | Sin certificación del flujo Reference real | Reusar DQ/expectations/assessment; T05 manager re-review pendiente, SAMPLE_POLICY unratified provisional, T06–T10 NO AUTHORIZED. Elegibilidad no equivale a curvas ni ranking Lab. |
| Front / screener / calendar | `xKoRx/echo:specs/FEAT-ANALYTICS-CONVERGENCE-A0/SPEC.md` §3 y [[Echo — Live Platform V1]] | Legacy front / Hasura paths documentados | Sin E2E auténtico de historia dual + nuevas curvas | No afirmado | REPLACE chart/comparison semánticamente incorrectos, ADAPT shell/graph/Hasura; calendario y ranking canónico pendientes. |
| Portfolios E-11…E-13 | [[Echo — Producto Integrado]], [[Echo — Live Platform V1]] | Roadmap antiguo contiene intención/shadow/apply | No certificación portfolio nueva | No afirmar | DEFER hasta que historia, curvas y comparabilidad existan; no calcular correlaciones desde ranking individual. |

## Evidencias y contradicciones que cambian el roadmap

1. Septiembre 6 decía `Forge Finalist Factory V1` y falta de ingreso canónico; Septiembre 21 documenta V2 FULL y E04 golden PASS. El estado de septiembre 6 es histórico, no actual. Fuente vigente [[Echo Forge — Factory V2 Completion]], [[Echo — E-04 Forge Ingestion E1]].
2. E05 es un núcleo usable técnicamente, pero la certificación de DEV del 16 de septiembre probó un **resultado vacío** del read model (0 sets), no un producto con una estrategia real. `SOURCE_PASS` tampoco significa dual-history ready. Fuente [[Echo — E-05 Analytics Convergence A0]].
3. E10 M7 demuestra que la derivación de Reference puede generar un TradeSet/MetricSet preciso bajo fixtures, no que existan historias Forge SQX/MT5 ni que la elegibilidad haya sido ratificada. Su autoridad incluye `sample_policy_ref = expectation_ref` declarado provisional, por tanto T06… no se continúa automáticamente. Fuente [[Echo — E-10 Strategy Quality and Eligibility]].
4. GitHub `xKoRx/echo` master comprobado `5dd998f16aea7b2821f460188718d7a6d279829c`; el proyecto registra feature consolidada E06–E09+E04 recovery @ `865532078f2c1993e7a3a542a78a9db0fad1f015` y E10 M7 @ `1485baa4574b3a65fa97cf0be842ca8ac581097a`. No confundir branch producto no mergeada con master ni presumir que M7 forma parte de la feature consolidada. `xKoRx/symphony` master verificado `745bc8b94e1f6148ddc16c02eb86a755088c2666`. SHA exactos del contexto documental no prueban HEAD de cada feature al minuto presente.

## Matriz de datos reales pendiente — primer hito obligatorio, NO condición para esta revisión

| Pregunta física para una StrategyVersion de FULL `0ce72173…` | Estado aquí | Prueba H0 y efecto si falla |
|---|---|---|
| StrategyRef/StrategyVersionRef y lineage versionada | Proyecto confirma finalistas sellados, objeto exacto no leído | Resolver un miembro auténtico F-05 read surface; pin exacto ID y seal; sin él stop publicación, no crear identidad artificial. |
| SQX individual trade list, formato, instantes, IS/OOS | NO DEMOSTRADO | Resolver source artifact digest, contar registros y empatar contra report SQX; sólo resumen => TRAINING_DATA NOT_READY. |
| MT5 individual deals/trades/HTM, rango y overlap | HTM byte verificado, detalle no leído | Verificar HTM trade-level realmente parseable, open/close, costos, lot/risk, comparar reporte; agregado => PRE_REAL NOT_READY. |
| Match económico SQX↔MT5 y cronología | NO DEMOSTRADO | Armar intersecciones de instantes y IDs, detectar conflicto, cobertura contra A/B; si ambos se limitan a training => no declarar PRE_REAL disponible. |
| Monetary input: initial risk, pip size, profit currency, costs | NO DEMOSTRADO para candidato | R/pips/virtual sólo si demostrables; null/INSUFFICIENT de lo contrario. |
| Reference REAL bajo B | NO DEMOSTRADO en este review | REAL = UNKNOWN/no observación suficiente, no rendimiento cero; E06/07 físicos después. |

## Límites de investigación y clasificación final

Material leído: Agents-OS Markdown enfocado por proyecto y source seleccionado vía GitHub, auditorías anteriores sin nuevas pruebas. No se revisaron RFC-003/004/009 r8/010 ni el código completo de Lab Worker/Front/Forge extraction ni material físico de los tres finalistas; su semántica no se inventa: el diseño usa contracts conocidos y exige pin/validación de rutas exactas durante H0. Graphify no está disponible en esta superficie; se utilizó búsqueda puntual de Library y GitHub sin reparar conectores. Estado exacto de PROD, workers, bancos de datos, infraestructura y certificado dual-history: **NO VERIFICADOS**, explícitamente fuera de alcance. Esta matriz no certifica flujo nuevo ni declara que se ejecutaron tests durante esta sesión.

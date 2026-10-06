---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
  - "[[Echo Futures — D4-B2 Q13 Gerard Hardscalping MoneyManagement]]"
  - "[[Echo Futures — BT-S01 Backtester V1 Design]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01 Final Operation Residual Classification

## Propósito

Clasificar el único residual Operation del histórico longitudinal auténtico contra el contrato compartido vigente, preservando el dominio y el modelo OHLC. Veredicto: `EXPECTED_SHARED_DOMAIN_NONTERMINAL_RESIDUAL`; `NO_BACKTEST_DIVERGENCE_CONFIRMED`. No requiere fix dentro de BTG-S01.

## Contenido

La autoridad [[Echo Futures — D2-04 Operation Order Fill Position]] §3.1 e I5 exige simultáneamente exposición lógica cero, cero órdenes vivas y una intención de término registrada. ACTIVE puede tener exposición temporalmente cero. Un fill protector, una Order FILLED o Position flat no terminan la Operation por sí mismos. La autoridad [[Echo Futures — D4-B2 Q13 Gerard Hardscalping MoneyManagement]] §17.5 prioriza intents y luego reconcilia protección contra exposición real; §18 prescribe intent para el TP monetario. No prescribe que todo fill protector fabrique un intent de término.

El resultado `bt-bd627d8a82e7faf07c5f17c0e89e60352d46abd882e64fa7286f99fd0430029f`, SHA256 `b11bd4e7776762523f29c9dda8e264c98818f5e209c7b051e72e6e671222a637`, conserva Operation `fop-ded07864ad9b5e99750fcfc4863c9866115baff7e0f6b30da331be780d80a7f5`, LONG, ciclo113. Hechos exactos:

| Record | Tiempo UTC | Hecho |
| --- | --- | --- |
| 270578 | 2023-11-23T03:05:00Z | CREATED desde OPEN; sin termination |
| 270594 | 2023-11-23T03:05:00Z | ENTRY BUY100 a16053.5 |
| 270610 | 2023-11-23T03:06:00Z | PROTECTIVE SELL100 a16052.5 |
| 270611 | 2023-11-23T03:06:00Z | PROTECTIVE FILLED, q_exec_max0 |
| 270612 | 2023-11-23T03:06:00Z | Último OPERATION_SNAPSHOT, event386, ACTIVE sin termination; ENTRY y PROTECTIVE FILLED, q_exec_max0 |

Exposición fill-derived100−100=0; no inversión ni orden ejecutable residual. El ledger final tiene unrealized0USD y balance/equity65706.68USD; el net−34293.32USD incluye costes6643.32USD y gross−27650USD. Son78fills y113Operations materializadas. El horizonte alcanzado es2023-11-23T03:29Z; residual Operation listado íntegramente junto a account_day_open, stage_open y timers posteriores. Se distingue residual de lifecycle de exposición económica abierta.

El código compartido `echo:v3/sdk/futures/operation/engine_inputs.go:1223–1248` retorna sin terminalizar cuando Termination es nil, aun con exposición y q_exec cero. `echo:v3/sdk/futures/gerardmm/gerardmm.go:271–333` procesa el fact sin generar intent para esta exposición plana; `:423–428` devuelve no-op cuando Q<=0. `echo:v3/backtester/finish.go:239–242` conserva el residual de una Operation no terminal. [[Echo Futures — BT-S01 Backtester V1 Design]] §15 permite COMPLETE con residuales explícitos compatibles con REPORT_RESIDUALS; EOF no inventa cierre, fill ni intent.

No se demuestra divergencia runtime/backtest: el mismo owner y GerardMM compartidos poseen lifecycle/intents. La política NO_ADDS no redefine terminalidad. Convertir automáticamente el stop físico en termination o cerrar al EOF sería un cambio de contrato/policy del owner; no una corrección de reporte F14. Esta clasificación no decide una nueva política ni certifica el runtime físico D6.

Baseline productivo declarado `d69d03eceeac1495522473a95baf08087f5c28b3`; el worktree diagnóstico `77e188bc1ab7cfddcb99e5fcd1a0ffc0c49ea626` no difiere en los tres archivos de autoridad revisados. El binario verificado tiene SHA256 `79bd5f2aab74c242dbece8ebd274975c94d37100d18af80103e3c44d62e69839`. Producto quedó clean y sin mutaciones; no se ejecutaron simulaciones nuevas, infraestructura ni pruebas D6. Las reproducciones IDENTICAL de la corrida larga y el smoke de cinco días son evidencia informada por Root, no reejecutada por este worker.

## Fuentes

- [[Echo Futures — D2-04 Operation Order Fill Position]] §3.1, I5 (líneas132–134,170).
- [[Echo Futures — D4-B2 Q13 Gerard Hardscalping MoneyManagement]] §17.5 y §18 (líneas572–600).
- [[Echo Futures — BT-S01 Backtester V1 Design]] §15 (líneas654–674); [[Echo Futures — BT-S04 Final Remediation and Certification]] Known limitations preservadas.
- Repo `echo`, paths `v3/sdk/futures/operation/engine_inputs.go`, `v3/sdk/futures/gerardmm/gerardmm.go`, `v3/backtester/finish.go`, `specs/btg-s01-real-diagnostics/VERIFICATION.md:23`.
- Workspace externo Aranea, relativo `work/btg-s01-20261006/reports/real-history-execution/longitudinal-nqz3-derived-candidate/bt-bd627d8a82e7faf07c5f17c0e89e60352d46abd882e64fa7286f99fd0430029f/result.json.gz`.
- Reuse: NONE; no nuevo test ni fix. Feedback: [[2026-10-06-btg-s01-operation-residual-session-feedback]] por conformance global rojo fuera del delta; sin skill cambiada. Consumo real: Work/Codex, modelo informado `gpt-6.1-sol`; sin métricas de consumo expuestas y sin atribución a ChatPro. Cierre solicitado: clasificación y registro persistidos; Root conserva aceptación y control del proyecto.

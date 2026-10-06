---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01-OHLC-DRIVER-FINAL-REVIEW

## Propósito

Revisión adversarial TOP LOCAL independiente del native OHLC driver congelado, usando el baseline funcional S2 + GerardMM reales. **REMEDIATION_REQUIRED: BT2-F08 HIGH bloquea el gate local.** No aceptación Owner, cierre histórico, resultado de campaña ni certificación de CLI.

## Contenido

### Identidad y límites

Source `xKoRx/echo`, branch `codex/btg-s01-ohlc-driver`, **e2e15a3559034a3ed08c04f247baf4919e20b2ff**. Detached review checkout limpio antes/después; frozen source y tests existentes intocados. Probes nuevos en checkout disposable de ese SHA, fuera del vault. SDK/Core/Strategy/GerardMM byte-idénticos a407e03dd; integración B e44 aceptada como dependencia ya revisada, sin repetir su auditoría. Diff C vsB incorpora exclusivamente sus archivos autorizados. AGENTS/CONSTITUTION, SDD exacto y autoridades Root cargadas.

Codex LOCAL, **agent_model=gpt-6.1-sol**, **model_source=host** confirmado por Root; PRO_CHAT_POOL_DELTA=0. Este ONE-SHOT cierra sólo el reviewer, Root mantiene coordinación. Docs lane `xKoRx/agents-os:codex/btg-s01-ohlc-driver-final-review`, desde master07ea7468. No cambios master, sync.sh/.sync, runtime/infra/D6 ni otros workers.

### BT2-F08 — primer account-day parcial colisiona en el reset17:00

**HIGH / REPRODUCED / BLOCKING_LOCAL_GATE**, reconocido por Root. Inputs: perfil BTG_FUNCTIONAL_NQ_EVAL_V1, NQZ6 tick0.25/point20, Chicago17:00, warmup2026-10-05T20:59:00Z=15:59CT, trade2026-10-05T22:00:59.999999999Z, end22:01Z. Corpus sintético REFERENCE_ONLY de dos minutos completos:20:59→21:00 y22:00→22:01. Respeta el descanso16:00→17:00, sin minuto interpolado, sin exposición ni Operation.

Expected: inicializar la identidad del account-day que contiene15:59, correspondiente al intervalo [Oct4 17:00CT,Oct5 17:00CT); el reset Oct5 17:00 abre un día distinto. Completar el slice cubierto sin excepción y sin consumir ordinal económico durante warmup. Si falta el segundo minuto, diagnosticar SOURCE_COVERAGE_INCOMPLETE desde22:00, conservando el descanso como cierre normal.

Actual: NewRun abre `ad-20261005`; el reset22:00Z vuelve a abrir `ad-20261005`, y ambos casos abortan con **ACCOUNT_DAY_FAILED: accounting: account day ad-20261005 is already open**. First divergence: `v3/backtester/run.go:684` deriva el ID inicial del civil date directo de WarmupStart; `driver.go:413` deriva el mismo ID en el boundary; `driver.go:496` ignora la hora de reset para el intervalo que contiene la fecha inicial. Los sources/minutos son válidos; la falla precede a cualquier problema de readiness o gap.

Origen: helper preexistente e idéntico en933/S04, expuesto por el nuevo baseline Chicago17 y su rango permitido. Probe separado sobre la ruta TRADE_MODEL del mismo frozen source, con offsets explícitos1/1 y source vacío, confirma exactamente el mismo ACCOUNT_DAY_FAILED al reset22:00 antes de TradeStart. Es evidencia de ownership compartido en el caller backtester, no un repro de OHLC sobre un baseline que todavía no tenía ese seam. No se descarta como fuera de C: impide el baseline funcional solicitado.

Corrección mínima propuesta, sin implementar: resolver el boundary que contiene WarmupStart desde las autoridades instaladas timezone/reset, reutilizando `experiment_plan.go` civilDateOf/boundaryOf y el día civil anterior cuando boundary.After(at), con AddDate para DST; pasar la fecha de ese boundary al helper estable. Preservar los IDs de boundaries naturales y casos UTC00 existentes, sin esquema paralelo native ni cambio SDK. La autoridad aplica también a inicialización legacy parcial si Root la incluye. `Plan.Days[0].AccountDayID=ad-btg-functional-1`, ordinal1, es identidad separada del materializador; los selectors resuelven por intervalo, no se exige igualdad con el ID civil del ledger. No rediseñar contextos ni modificar MM/Provider para evitar el error.

Evidencia: `independent-fast.log` RED para complete-break y truncated; `account-day-legacy-reference.log` PASS1.058s demuestra el error esperado de la referencia legacy. Conservar el repro nativo como PERMANENT_REGRESSION candidate y volverlo verde tras el fix; luego probar before/at/after17 y DST, mismo slice, sin tocar oráculos S04.

### Matriz crítica y contraste de hipótesis

| Contrato | Evidencia / conclusión |
| --- | --- |
| Future HLCV / input consumption | Independiente race PASS: dos variantes válidas con High500/Low1/Close400/Volume999999 conservan prefix exacto hasta59s, cero refs/consumed y un Open reservado. Al availability los registros cambian y se consumen exactamente dos refs al close; ningún full source previo. |
| BT2-F07 late-control | Independiente race PASS, seis casos flat/working y31s/end/end+1ns: control flat legítimo aplica7USD; working intrabar falla antes de cashflow/ref/ledger mutation y diagnostic>=completedfrontier30s; at/after globalEnd quedan pending sin cashflow, terminal close/ref sí se consumen. Producto late/control-end y múltiples pending streams también ejecutados intactos. |
| Native close/boundary/timers/Open | Source audit más frozen fast race: closephase1 precede controls2, boundaries3, timers5 y nextOpen6; all pending closes seleccionados antes de cualquier coincident Open. Entrada nueva y stops/close tardíos no retrofill source HLC. |
| Warmup/readiness | Frozen fast race: incomplete-prefix no readiness por count; complete exact source intervals y50/51 causally eligible H4,20x5m, H4Close<=5mOpen. Product domain4cases suministran 51H4 reales sintéticos completos; no reducir warmup para justificar S2. |
| BT2-F06 timers | Frozen fast race incluye48/1000minutes y5000 fired-history; records/result/ref digest idénticos y peak<=20, live generation/order/residual. Auditoría independiente confirma compaction nativa estable antes de cualquier index selection; fireTimer/pushTimer retornan antes del siguiente nextRoot. Legacy no prune. No speed claim:40.48→42.46s matchednonrace, GC dominant. |
| Resting stop gap / long-short | Independiente venue race PASS1.023s: stop SELL95 ya resting antes de Open90 llena89.5; BUY105/Open110 llena110.5;qty3 y finality exactas. No precio regalado de95/105. |
| Adverse entry Open | Hipótesis de stop técnico regalado **DISPROVED_WITH_EVIDENCE para S2 exacta**. Full warmup real-domain perturbado entryOpen90 con technical97.25: BUY30@90.5, GerardMM genera MARKET safety close y SELL30@nextOpen103 modeled102.5, resultado COMPLETE. La primera aserción reviewer esperaba erróneamente89.5: RED del oráculo conservado y expectativa corregida explícitamente, sin nuevo warmup duplicado. No product failure. |
| Venue manual crossed stop | Probe manual activa STOP95 después de Open90 y recibe94.75 al close: REFERENCE_ONLY fuera del path baseline observado; no se convierte en finding S2 ni se afirma corrección universal del venue. Reabrir sólo con otro path legítimo de dominio que produzca ese STOP. |
| EOF / rollover obligations | Frozen fast race PASS: selected-flat truncated EOF visible, retired-flat sin falsegap, old-pinned OLD_CONTRACT_DATA_UNAVAILABLE sin nuevos marks/fills crosscontract. El probe real-calendar break queda bloqueado porF08, no se reporta PASS. |
| Domain money / SL-first | Evidencia completed frozen C: cuatro casos full domain long/short SL y monetaryTP-nextOpen, qty30, fee74.7/fill149.4 total. Literal short stop104.25/fill104.5 corregido frente a MM real sin cambiar fórmula. Normal4domains+futureextrema+legacy PASS258.765s; no multiplicar el coste repitiendo4warmups en reviewer. |
| Legacy / identity / S04 | SDK/Core byteexact407 y old tests diff vacío C-vsB; narrow legacy/S04 offline race independiente PASS: Driver/horizon/corpusshort/freshprocess/control dispositions/replay/EOD boundary, con loopback local, y frozenC guard evidence. Native model/policies digest y fidelity explícitos; TRADE legacy route conserva branches/bytes. |

Frozen fast actual independiente: **race PASS30.363s**, explicitregex OHLC gaps/scaling/inputsequence/readiness/order/controls/faults/coverage/horizon/freshprocess/timers/profile/context. Original producer profiles siguen evidencia de dependencia, no se llaman pruebas independientes. Ningún control/contexto se oculta para green.

### Cobertura independiente

Gate nuevo aplicable reconstruido con Go blocks, cuatro archivos nuevos completos más todo bloque instrumentado que intersecta líneas añadidas/reemplazadas de seis existentes C; B adapter no forma parte de ese denominador. SHA de los diez sources y de los cuatro perfiles completed verificados contra frozen source. **Mapping exacto independently reconstructed:525/562 raw=93.4164%;525/552 applicable=95.1087%**, exclusiones10. New-only408/438 raw y408/428 aplicable se informa separadamente; no agregado whole-module ficticio.

Exclusiones aceptadas sólo para la composición inmutable del producto: cuatro errores de constantes válidas NewContractSnapshot/NewWallClock/SIMRuleSet/JSON en functional_profile38/46/55/59; ask AddTicks con tick positivo validado y offsets no negativos ohlc_driver277; Views economía instalada/refrescada sin nil/removal en304; venue66/115/158 repiten side/tick validations del mismo catálogo inmutable; venue78 invoca ExpireDay concreto que siempre retorna nil. Función TickSize dinámica manipulada fuera del catálogo compuesto no queda certificada por estas exclusiones. No se excluyen handlers OS, ledger, recorder ni errores económicos alcanzables. Coverage PASS no subsanaF08.

Fuentes completed: final-domain-current.cover normal258.765s; final-fast-current.cover race31.642s; final-warmup-selection.cover race1.110s; frozen-full-venue.cover race1.041s. Union y auditor propios externos: coverage_audit.py/coverage-independent.json verifican hashes/rangos exactos y no usan los porcentajes resumidos como autoridad. Extended4domain race fue detenido por Root trasF08; **INTERRUPTED_NOT_PASS**, no se cuenta como completado. Histórico real NOT_RUN.

### Seguridad, retención y cierre

Todo comando Go corrió con lista de packages/regex explícita, `unshare --user --map-root-user --net`, GOPROXY=off/GOSUMDB=off/GOFLAGS=-mod=readonly. Sólo namespace loopback habilitado para los HTTP fixtures S04; sin NIC externa. No `go test ./...`, suites desconocidas/seeds/infra/live/D6. Source freeze intacto; probes adicionales únicamente en checkout disposable externo. Dos errores de setup propios (sintaxis extra y TRADE_MODEL sin offsets explícitos) se corrigieron en probes nuevos; logs preservados, sin tocar producto.

Evidence workspace Aranea relativo `work/btg-s01-20261006/reports/ohlc-driver-final-review/`: reviewer tests, hashes, commands/README, red/green logs, raw profiles y coverage audit. PERMANENT_REGRESSION candidates:F08 partial-first-day y latecontrols/terminalsource; E2E_CANDIDATE:futureHLCV causal prefix/sequence y calendarbreak con EOF; DISPOSABLE_REPRODUCER:manual crossedSTOP y adverseentry oracle errado, reference legacy empty-source; HARNESS_TOOLKIT_CANDIDATE:coverage_audit.py sólo tras confirmar owner existente, sin framework/promoción automática. No skills nuevas ni recomendaciones rituales.

Originales13NT exports C:/Temp/history permanecen **POLICY_DENIED / NOT_ACQUIRED**; sólo names/muestrasprevias REFERENCE_ONLY. Historical rerun/economics/Owner acceptance no demostrados. F06/F07 quedan FIX_AND_REGRESSION_INDEPENDENTLY_VERIFIED en scope sintético, OPEN_REAL_RERUN_REQUIRED; F08 OPEN_REPRODUCED_REMEDIATION_REQUIRED. Root debe congelar correction del account-day inicial, despachar fresh worker/fresh reviewer y repetir slice/regresiones; después original autorizado y real rerun.

REUSABLE_BEHAVIOR_CANDIDATES=NONE; SESSION_FEEDBACK=NONE: ningún gap real de Sistema1 que amerite otra nota. Agent-run y change_log por delta; sesión ONE-SHOT reviewer cerrada conforme mandato, sin L0/L1/memoria duplicada/cierre Root. por favor gracias

## Fuentes

- Root evidence lane canónico: `10-projects/Echo Futures/artifacts/backtester-stage2-real/BTG-S01-FUNCTIONAL-BASELINE-PROFILE.md`, OWNER-S2-BARS-AUTHORITY, FINDINGS y NTMINUTE-FINAL-REVIEW; BTG-PLAN y BT-S01 design amendments/S04 final certification como autoridades de boundary/legacy.
- Repo xKoRx/echo e2e15a3 y `specs/btg-s01-ohlc-driver/{SPEC,PLAN,TASKS,VERIFICATION}.md`; sdk/core unchanged407; adapter exacte44 input accepted.
- [[2026-10-06-codex-gpt-6.1-sol-btg-s01-ohlc-driver-final-review]], external evidence relativo arriba y [[Echo Futures]].

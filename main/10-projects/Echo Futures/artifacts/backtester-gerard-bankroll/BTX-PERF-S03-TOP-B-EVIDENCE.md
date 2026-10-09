---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related: []
aliases: []
tags:
  - kind/doc
created: "2026-10-09"
updated: "2026-10-09"
---


# BTX-PERF-S03-TOP-B-EVIDENCE

## Propósito

TOP B independiente LOCAL fresh-context ONE-SHOT de continuidad S03. Resultado: **FINDINGS / REJECT_CANDIDATE_FOR_S04** por tres fronteras defectuosas ejecutadas: sello de admisión expuesto por lectura pública, aplicación del control mutable original con dinero distinto del admitido y compra inicial con caja insuficiente. No certifica los cuatro gates ni acepta el producto. No se modificó código de producto, README, BTG-PLAN, informe S02, preliminar ni originales. No hubo commit/push manual; sincronización automática del vault es ajena a esta ejecución.

## Contenido

### Autoridad, identidades y límites

Autoridad leída: agents-os/bootstrap/constitución/perfil/índice; technical-project-manager; skills agent-run/feedback/close; router Aranea y contrato Echo/Forge; BTG-PLAN blob `de3753b81564eb62f64a8b5eb18f198a6a81fd27`; adenda Owner de BTX-PERF-DESIGN; evidencia preliminar ACOTADA y recibos selectos; README canónico del source. Mandato acotado prevalece sobre propuestas históricas. Esta verificación no autoriza otra ventana Owner ni otro shot.

| Identidad | Evidencia |
|---|---|
| Source auditado | xKoRx/echo `bbbcc1d5dc0ed18badae46b4eba1a17822632b60`, checkout fuente limpio; overlay creado mediante git archive, sin .git |
| Archive completo SHA256 | `5f45a04dfccac63f8178e1f7dbec41d6bc5d0c738880eda2148650bc99441d25` |
| Bin de tests final ejecutado | `bin/backtester.test`, SHA256 `45ba14ba265290fa3fb164ccfe4d79bedb77620c09ddc1a2e66e95ae1d6c5671` |
| Bin Gerard retenido | `bin/gerardmm.test`, SHA256 `cc5b9d22624b63c0bc69cc646b58faecd849eab064398ee10f44ed95e5a42923`; ejecución Gerard fue go test contra el mismo source, bin retenido compilado después |
| Toolchain | go1.27.1 linux/amd64; paths/hash completos go/git/timeout/python3/tar en IDENTITY.json |
| Inputs / fixtures | Sólo fuentes sintéticas de tests existentes y módulos propios; cero corpus NT financiero consumido. Cada archivo source/fixture/oracle y delta propio tiene SHA256 completo en SHASUMS.txt |
| Paquete externo | `~/aranea/work/btx-perf-s03-top-b-20261009/`: overlay, bin, logs, COMMANDS.md, IDENTITY.json, prior-verification.json, seal.py, SHASUMS.txt |
| Recibos heredados | Verificados contra SHASUMS del preliminar antes de reutilizar: RECEIPTS, t5 candidate/baseline, t5c largecorpus, bin CLI preliminar `c9ac66caf363e1eda662c15d07b7c6cdb2fa11e773c30243d23e4aed7edc13b8`; matches=true en prior-verification.json |
| Modelo / consumo | Pedido Owner GPT-6.1 Sol; identidad exacta real no expuesta por harness: UNKNOWN. Tokens/context high-water/consumo/Pro pool delta: UNKNOWN; no inventar entitlement ni consumo cero |

Ejecución financiera serial; timeout120s por comando; no backtest histórico, benchmark/perfil, lote13x, LIVE/D6/PROD, broker ni infraestructura. Tiempo de tests sumado desde líneas terminales conservadas ampliamente menor12min; no comando financiero llegó a timeout. Tiempo exacto agregado de compilación no instrumentado, no se presenta como medición de performance. Overlay creado22:31:06Z; el trabajo fue acotado al límite operativo35min, sin convertirlo en autorización Owner. Comandos exactos, CWD, redirecciones y rc están en COMMANDS.md; los nuevos RED finales se ejecutaron en el bin sellado mediante `timeout 120s .../bin/backtester.test -test.run '^TestTOPB' -test.v` (rc1 esperado). Todos los procesos propios terminaron.

### Nuevos defectos ejecutados y corrección mínima S04

**B-01 — getter público corrompe el sello interno de admisión (MAJOR, DEFECTO_VIGENTE).** `run.go:847-850` copia el slice de ControlAdmission superficialmente; TypedPayload y ContextTransition quedan prestados. `TestTOPBAdmissionsReadIsolation` admite la transición top-b-read, obtiene Admissions(), cambia solamente `view[0].TypedPayload.ContextTransition.NextContext.ContextID`, y vuelve a consultar. Primera divergencia: el cuerpo interno ya dice caller-corruption y no coincide con Digest inmutable. Digest admitido `sha256:c64c6cc65135d1036458e8090e53d380c5152641c00c5ca431f28c74f7533a4d`; cuerpo después `sha256:cbaad4812b5ec11d1798f8af930e1e0e658b1603fdbdfb73709fd046696c89af`. No hace falta Apply para destruir la evidencia de replay. La adenda exige sellado tipado/digest independiente de APPLIED. Owner: backtester RunState/admission read-model. Cambio mínimo: devolver copia profunda de cada payload/nested map desde la frontera pública, conservar seal privado. Criterio: mutar cualquier vista pública no cambia siguiente getter, digest/input final ni cuerpo recuperable; extender a Cashflow y mapas anidados. Log definitivo final-sealed-own.log.

**B-02 — pending Apply usa el objeto mutable original y aplica dinero distinto del sellado (CRITICAL, DEFECTO_VIGENTE).** `EnqueueControl`, run.go:802-827, crea payload profundo para admissions pero agrega `c` original a pendingControls. `TestTOPBPendingControlUsesAdmittedBody` altera ExpectedContextDigest después de admisión; Apply falla CONTEXT_DIGEST_MISMATCH usando la corrupción del caller, aunque el cuerpo sellado admitido conserva el digest correcto. `TestTOPBCashflowUsesFrozenMoney` añade oráculo monetario: admite CashflowAdjustment +1 USD; después cambia caller.Amount a +2; AdvanceUntil(+30s) devuelve éxito, ledger.Cashflows.Amount=2 y disposición APPLIED usa el digest mutado. Digest admitido `sha256:4c472c69516c48a53e191ad5987ce4ef052052bfc6a6377daaa866f761e5ec6b`; digest caller/aplicado `sha256:db86e30d877183a5b6f826101209ae06fb72e0c385477f4f8f434baeac342a24`. Primera divergencia contractual: la disposición aplicada y crédito2 no corresponden al cuerpo admitido1. No es doble dinero de duplicado: es sustitución mutable del cuerpo después de admitir. Owner: cola de controles/driver. Cambio mínimo: pending debe poseer el Control reconstruido desde el body congelado, no c; comparar/cerrar admisión y disposición contra identidad sellada. Criterio: cambiar importe/digest/EffectiveAt/Ordinal/maps del caller no altera tiempo, orden, disposición ni dinero; aplicar1 exactamente una vez. Log money-close.log y final-sealed-own.log.

**B-03 — compra inicial sobregira caja119/120 (MAJOR, DEFECTO_VIGENTE).** RunCampaign, campaign.go:297-300, llama d.cash.debit y aumenta Purchases sin comprobar asequibilidad; CampaignConfig.Validate sólo exige cantidades no negativas. `TestTOPBInitialCash119120` final usa fixture válido entries1, horizonte9min, sin trading: 119→compra1→-1 USD, terminal HORIZON_REACHED y FailureCode vacío;120→compra1→0 USD, mismo terminal. Primera versión entries0 produjo además STRATEGY_EVAL_FAILED y se preserva como experimento descartado; el RED limpio final elimina esa ambigüedad. Autoridad: compraON_DEMAND sólo con caja disponible, dinero exacto y boundary119/120 pedido expresamente; no cambia el perfil funcional5000. Owner: campaignDriver inicialización/cashBook. Cambio mínimo: aplicar el mismo criterio de fondos a primera compra antes de crear/admitir cuenta operante/debitar, con terminal explícito de falta de fondos según contrato existente. Criterio:119 cero compras/cero sobregiro;120 una compra/caja0; pérdidas nominales no vuelven a debitar, reinversión depende sólo de cobros efectivos. Logs initial-cash-valid.log y final-sealed-own.log.

### Cinco rojos originales: adjudicación por causa, no por preexistencia

Todos reproducidos sin editar tests originales: five-reds.log rc1, paquete7.853s. La preexistencia baseline no se usa como exoneración. La autoridad de compra/protección actual cambia la interpretación de varios assertions de fixture.

| Test exacto | Clase | Fuente / primera divergencia / autoridad |
|---|---|---|
| TestBTGS03_CampaignCashBurnReplacementAndContinuity | EXPECTATIVA_SUPERSEDIDA | Assertion exige4 cuentas quemadas pero observa4 quemadas + quinta activa sin fills al horizonte. ON_DEMAND requiere recompra tras desenlace y quiescencia cuando hay caja/mercado, no detener compras al agotarse el script. No existe cap4 compras: cap4 **cobros efectivos por cuenta**. README CAMPAIGN y BTG-PLAN vigentes. Producto preserva pérdida nominal sin redebito. No quitar recompra para poner fixture verde |
| TestBTGS04CampaignBurnCashLedger | EXPECTATIVA_SUPERSEDIDA | Espera3 compras/caja4640 para3 burns; compra sucesora adicional produce4 compras/caja4520, idle ACTIVE_AT_HORIZON. TestTOPBOnDemandBurnCashOracle independiente confirma3 burns/4 compras/caja4520 y Reconciled=true. Ajustar oráculo de fixture con cuenta activa/compra exigida; no adaptar política del producto |
| TestBTGS03_V2IntrabarAddsAdverseAndProtection | FALLO_HARNESS | Assertion len(fills)>=3 dice adds ausentes; diagnóstico demuestra entrada50@150.5, ADD MARKET50 SUBMIT@22:11:06.666666666, SL50 llena@22:11:10 a148.75, CANCEL del ADD pendiente en ese mismo cierre. El add sí fue emitido, stop cierra antes de su elegibilidad y se cancela new risk. Forzar fill adicional violaría el oráculo no exposición huérfana. Reformular fixture si se quiere ejercicio de ADD lleno posterior: garantizar tramo posterior elegible sin SL previo, mantener prueba pendiente tras cierre |
| TestBTGS04_MixedMinuteCapabilityBoundary | EXPECTATIVA_SUPERSEDIDA | Test pide rechazo de unsupported MIXED_MINUTE sin OHLCModel. spec.go:698-705 admite explícitamente MarketDataMixedMinute con modelo; error actual exige ohlc_model, no el texto antiguo market_data_mode must be. No es evidencia de aceptación silenciosa sin modelo. Capability real multistream CLI sigue NOT_IMPLEMENTED en preliminar, separada de este API mode |
| TestBTGS04_StructuralReferenceSkipFirstDivergence | NO_RESUELTO | Original oráculo permite bijections para order_id pero omite provider_order_ref y cause_ref derivados. Drift primero provider_order_ref sim-order:ord…@22:11:06.666; ledgerRev36/36,74 records/74, StrategyState/risk iguales. Probe propio vincula sólo provider prefix al orden ya bijectado y mueve primera divergencia a cause_ref FILL:sim-exec:ord…:1@22:11:13.333. No borra valores monetarios ni acepta IDs libremente. Falta cerrar TODAS las referencias con mapa uno-a-uno, ciclos y oráculo negativo; no declaro paridad ni defecto de dinero desde igualdad de snapshots |

Ajuste obligatorio del preliminar: son **3 CLI tests reparados**, no2: TestFreshProcessDeterminism, TestBT_S04_StandaloneReproduceClosedSpec y TestLargeCorpusStreamingMetrics. Evidencia heredada verificada: RECEIPTS informa3/8 PASS; t5 candidate registra5 fallos y t5c confirma LargeCorpusStreamingMetrics PASS332.98s. Los dos primeros son nombres corroborados por la nota preliminar y recibos baseline; el t5 candidato sin -v no emite sus líneas verdes individuales. Esta entrega distingue corroboración documental de nuevo PASS ejecutado. No se repitió LargeCorpus ni se atribuye su duración a TOP B.

### Bordes financieros y públicos ejercitados

| Requisito | Evidencia y límite |
|---|---|
| LONG/SHORT, adds adversos/pirámide, tramos, ACK/claims y cierre con ADD pendiente | 8 tests Gerard PASS, protection.log: TestBTGS05_ProtectionTranchesAndFinality LONG/SHORT×adverse/pyramid; PartialEntryDoesNotEarnBreakEven; CloseCancelsEveryTrancheAndPendingAdd LONG/SHORT; WorkingAckResumesOnlyFreshProtectedAdmission; MultipleTighteningClaimsBlockQuoteAndOpenAdds; UnrepresentableProtectionResidualNeverAdmitsNewRisk; LateAddAfterPriorFlatHasNoInventedBreakEven; ProtectiveFlatCancelsPendingNewRisk LONG/SHORT×Fill/Final. Tests reutilizados, no nuevos ni certificación broker |
| Parciales/duplicados/finality y reservas reales | TestBTGS05_NativeFixturePartialDuplicateDelayedFinalityALLSkip y RealPendingReservationsAndProtectionALLSkip PASS; causes-and-admissions.log. No duplicación financiera observada en fixture |
| Timer intrabar/control y fases | TestBTGS05_ExposedMidMinuteControlAndTimer PASS acotado. Callback timer→orden nueva y elegibilidad posterior con negación de fill retrospectivo adicional: NOT_RUN |
| Batch Record/ownership/generación | TestTOPBHistoryFailureAndOwnership PASS cuatro subcasos: Record falla tras primera llamada retiene5 revisiones, sink borrowed(false) retiene5, owned(true) captura2 y libera a1, callback cambia ledger produce LEDGER_OWNERSHIP_CHANGED y conserva5 en dueño anterior. Guard igualdad intacto. Sink malicious que afirma ownership pero guarda referencias es violación de contrato del sink, no prueba driver universal |
| Close fallido | TestTOPBRecorderCloseFailure PASS: Finish devuelve error backtest: recorder close: top-b-close-failed, aunque Result diagnóstico ya contiene COMPLETE. Consumidor debe respetar error; no se adjudica sólo por el campo como nuevo defecto |
| Admisiones APPLIED/CONFLICT/REJECTED/horizonte | TestBTGS04CampaignCashflowDuplicateConflictRejectHorizon PASS: duplicate debit total-1500 una vez; conflict-1600 rechaza, REJECTED contexto wrong conserva saldo100000, PENDING_AT_HORIZON conserva saldo. Presencia/copia profunda de TypedPayload de cada disposición final no se vuelve a certificar: B-01/B-02 rechazan frontera actual |
| Lifecycle FUNDED/4ªsolicitud y caja | FourthRequestPending PASS6.26s: cuarta solicitud pendiente no cobra/retira cuenta. ReplacementRestoresEvaluationTerms PASS: FUNDED anterior no contamina términos EVALUATION sustituta. OnDemandBurnCashOracle PASS independiente. Boundary119/120 RED B-03. Residual separado al cuarto cobro tiene test existente fuera de este lote; NOT_RUN aquí |
| Strategy pública sustituible, estado y BarRange | TestTOPBStatefulPublicStrategyReadIsolation PASS6 callbacks; contador int Encode/Decode coincide en cada callback, muta Close de BarRange recibido a999 y exige lectura nueva150 y primera lectura150 en cada evaluación: no corrupción same-scope ni historia posterior. TestBTGS04CampaignSubstitutionRequirements PASS con requisitosH4 de módulo público. Eventos/timers de Strategy y MM stateful custom completo: NOT_RUN |
| Rollover API A→B | TestBTGS05_V2PublicRolloverPreservesSeparatePrefixes PASS, incluido retired-working-order-requires-own-price. Exige stream propio del retirado; no inventar precio. No prueba merge/CLI multistream: ausente y ya RED previo. Warmup/readiness de seleccionado, posición+claim retirado simultáneos con stateful módulos nuevos: NOT_RUN |

### NOT_RUN conservados como gates S04

RED temprano es suficiente para rechazo, no para clausurar exhaustivamente S03. No se implementó multistream ni replay CLI. Requisitos pendientes:

- Timer entre pasos que crea orden y callback reinicia timer: comprobar drain completo, fases, submit causa anterior y fill sólo paso elegible posterior; matriz LONG/SHORT y ALL/SKIP. Gate causalidad, motivo: priorización de RED admisión/dinero; test existente de clock no prueba ese recorrido entero.
- Batch día/contexto/stage con todas revisiones, mutación reentrante y reemplazo real de ledger durante callback: pruebas S02 existentes aceptadas acotadas; own replacement=nil sólo falsifica guard y conservación del antiguo dueño. Gate: cada commit capturado en orden, autoridad final, ninguna revisión prestada liberada; nunca LatestRevision ni guard<=.
- Sellado profundo para APPLIED/REJECTED/CONFLICT/PENDING junto con finish/input digest y mutación del getter después de Finish: B-01/B-02 bloquean; oracle full cuerpo/digest inmutables y dinero exactamente una vez. No readmitir externamente controles regenerados CAMPAIGN.
- Cobro4 efectivo con retiro/residual separado, reinversión prolongada hasta falta de fondos y segunda cuenta pasando FUNDED: no nuevo lote prolongado; gate cash=start−120*compras+neto **cobrado**, cuarta solicitud no equivale cobro ni residual. Boundary inicial demostrado, reemplazo insuficiente existente no reejecutado.
- MM público custom stateful que observe events/timers y conserve callbacks al rollover/reemplazo junto con Strategy eventful: prueba own cubre estado Strategy y lecturas, no todos eventos/timers. Gate no ifGerard, sin callbacks perdidos ni estado reset técnico; SL/TP/sizing/adds/fees no cambian.
- Rollover prospectivo con posición+orden+claim retirados, readiness/warmup seleccionado, caja/estado compartidos y year/month propio: fixture API existente parcial PASS; combinación completa NOT_RUN. Núcleo y CLI ausente se adjudican separadamente.
- StructuralReference mapping completo bijectivo para provider_order_ref/cause_ref/provenance/owner refs con pruebas negativas de colisión y money mutation: NO_RESUELTO. Nunca remover IDs/ref del comparador ni tomar snapshots iguales como cierre.
- NQZ5 completo/reconciliación tipada18nov/20nov, cobertura95%, -race, benchmarks/perfiles, pipeline concurrente/CLI multistream/replay completo, historias all-years: NOT_RUN por mandato de gasto/scope. Ausencias de funcionalidad quedan NOT_IMPLEMENTED con oracle S04, nunca construirlas durante verificación.

### Assets transportables y clasificación

No promoción automática. Todos los nuevos archivos son overlay-only y conservan originals intactos.

| Test/probe propio | Clase / razón |
|---|---|
| TestTOPBAdmissionsReadIsolation | PERMANENT_REGRESSION: integridad del read-model de admisión profundo |
| TestTOPBPendingControlUsesAdmittedBody | PERMANENT_REGRESSION: estabilidad postadmisión del contexto aplicado |
| TestTOPBCashflowUsesFrozenMoney | PERMANENT_REGRESSION: mismo sello, disposición y dinero aplicado |
| TestTOPBInitialCash119120 | PERMANENT_REGRESSION: frontera exacta compra inicial; preservar versión válida9min |
| TestTOPBHistoryFailureAndOwnership | PERMANENT_REGRESSION: evidencia poseída y rechazo fallos de Record/cambio de dueño |
| TestTOPBRecorderCloseFailure | PERMANENT_REGRESSION: Close fallido invalida aceptación |
| TestTOPBOnDemandBurnCashOracle | E2E_CANDIDATE: controller continuo, burns+recompra+ledger exacto |
| TestTOPBStatefulPublicStrategyReadIsolation | E2E_CANDIDATE: seam pública stateful y lectura historia inmutable |
| TestTOPBAddsDiagnostic | DISPOSABLE_REPRODUCER: dumping acotado aclara fixture rojo; no assertion de add filled |
| TestTOPBStructuralReferencesBijection | HARNESS_TOOLKIT_CANDIDATE: ampliación parcial; todavía rojo/NO_RESUELTO, no promote antes de mapa completo y negativo |
| seal.py / COMMANDS / hashes | HARNESS_TOOLKIT_CANDIDATE: trazabilidad fuente→fixtures→bin→logs; no herramienta productiva |

### Cierre y continuidad

REUSABLE_BEHAVIOR_CANDIDATES: `test_harness` — probar dos fronteras separadas de ownership de admisiones (vista pública y cola de ejecución) y agregar oráculo monetario exacto, porque un seal correcto aislado no demuestra uso de ese body. Evidencia B-01/B-02. `pattern` — rojo de fixture len(fills)/cuentas debe adjudicarse por causa/obligaciones, no por conteo: SL cancela ADD y ON_DEMAND compra idle replacement. Promoción sólo posterior con Owner; no edición de skills/memorias públicas en este shot.

Agent-run propio [[2026-10-09-codex-unknown-btx-perf-s03-top-b]] y feedback [[2026-10-09-btx-perf-s03-top-b-session-feedback]] materializados vía contrato. Cierre por delta: sin L0/transcript nuevo, sin L1 ni memoria global; continuidad requerida vive en esta evidencia. Próximo paso GOD: reconciliar con TOP A y congelar scope S04; no atribuir estos RED a baseline por inferencia. FINAL_OWNER_ACCEPTANCE=NOT_GRANTED. No procesos propios pendientes.

## Fuentes

[[BTG-PLAN]], [[BTX-PERF-DESIGN]], [[BTX-PERF-IMPLEMENTATION]] (objeto auditoría, no autoridad que exima rojo), [[BTX-PERF-S03-TOP-EVIDENCE]] (ACOTADO), xKoRx/echo@bbbcc1d5 README/run.go/campaign.go/spec.go/driver.go/finish.go y tests fixtures señalados. Hashes completos y recibos fuera vault en paquete TOP B. No fuentes de D1–D6 ni conversaciones históricas reabiertas.

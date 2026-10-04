---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — BT-S01 Backtester V1 Design]]"
  - "[[Echo Futures — BT-S02 Backtester V1 Implementation Handoff]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-04"
updated: "2026-10-04"
---

# Echo Futures — BT-S03 Adversarial Review

## Propósito

Intentar refutar BT-S02 aceptado, con cinco subagentes reales y revisión integradora independiente. No se implementaron fixes, no se inició BT-S04 y no se mergeó/cherry-pickeó D6.

## Contenido

### Executive verdict

**REMEDIATION_REQUIRED.** Cinco CRITICAL, ocho MATERIAL, un KISS obligatorio y dos MINOR aceptados. F01/F02/F03/F05 quedan adversarialmente confirmados; F04 requiere remediación. Las suites heredadas verdes no prueban las propiedades que contradicen los repros nuevos. BT-S01 y BT-S02 fueron leídos completos antes del dictamen.

Existe además un **incidente operativo abierto y escalado al Owner**, separado de los defectos del backtester: un subagente ejecutó una suite SDK amplia que escribió configuración ETCD de producción. No afirmar “infraestructura intacta” ni “review sin efectos externos”. La recuperación no está certificada y no forma parte del contrato productivo S04.

### Baselines y alcance

| Superficie | Baseline |
| --- | --- |
| Repo | `xKoRx/echo` |
| Backtester aceptado / remoto inicial | `feature/backtester-v1-s02@f41da25cc0b779ea48375198dbedaf932b930a80` |
| Tree aceptado | `3ea08df70e2c226aaaa5697f33afc549c2ff8410` |
| Review aislado | `codex/bt-s03-adversarial-review`; sólo archivos nuevos de tests con build tag `s03review` |
| Baseline concurrente original | `7fbd7e990ac6628df3e4cc2717e96efd83bfbbf6` |
| D6 HEAD inicial | `32baeaeb49cff8b4227b850d7a575549bbcf54a2` |
| Toolchain observado | Go1.27.1 linux/amd64; go.work declara1.25.5, sin cambio de toolchain/dependencias |

Commit de review **`13bb72bbe237aae0d191f26d9c5ca89a5b5b9670`**, publicado en `origin/codex/bt-s03-adversarial-review`: seis archivos nuevos, 924 líneas, exclusivamente tests tagged; cero diff de producto contra f41da25c. Backtester remoto final permanece f41da25c. Los paths de SOURCE de los findings son relativos a `xKoRx/echo:v3/` en el baseline aceptado; los tests viven en el branch de review. Evidencia local externa al vault: workspace `bt-s03-20261004/reports/`.

### D6 concurrent delta

Refresh inicial confirmó los HEADs del mandato. Desde 7fbd7e99: 23 archivos,1548 inserciones/96 eliminaciones, concentrados en `v3/futures-bridge/addon-ninjatrader/EchoExecutionAddOn.cs`, `endpoint_guard_test.go`, `parser-harness/`, `proto-harness/`, `protocol_contract_test.go` y `v3/futures-bridge/internal/session/reallane_barrier_test.go`. Ningún cambio a `v3/sdk`, `v3/core` ni `v3/backtester`; ninguna intersección con archivos productivos cambiados por S02. No se certifica D6 ni su gate físico.

El refresh final observó D6 **`d08a30ce9815f820fda7132e20dc42cc345eb8e8`**. Delta nuevo desde 32baeaeb: cuatro archivos,372 inserciones/66 eliminaciones: `v3/futures-bridge/adapters/ninjatrader/{adapter.go,adapter_test.go,coverage_test.go}` y `v3/futures-bridge/internal/session/reallane_barrier_test.go`. Se inspeccionó el diff de producto: readiness de recovery por snapshots de positions/orders de la sesión actual, sin cambiar tipos/contratos compartidos; no toca SDK/Core/Backtester. Ninguna reconciliación D6 requerida para estos hallazgos, ninguna integración realizada.

```text
CONCURRENT_D6_CONFLICT = NO
D6_CONCURRENT_DELTA = NON_CONFLICTING
```

### SUBAGENT UTILIZATION

El host no expuso GPT-6 Luna/Sol. El Owner autorizó expresamente `gpt-5.6-luna` y `gpt-5.6-sol` antes del primer dispatch. Coordinación: GPT-6 Astra/GOD según mandato. Cinco agentes reales, en dos olas; no se usaron subagentes Astra.

| Modelo / agente | Frente y razón | Output reutilizado / duplicación evitada |
| --- | --- | --- |
| gpt-5.6-luna / luna_acceptance | Barrido barato de aceptación/dataset/result/control | Seis repros; Astra challengeó sus precondiciones, refinó severidad y no repitió el barrido. |
| gpt-5.6-luna / luna_fixes | F01–F05 independientes | Cuatro confirmaciones y repro F04; Sol recibió sólo el seam relevante. |
| gpt-5.6-luna / luna_kiss | Call sites/duplicación/dead code | Astra aceptó dos reducciones concretas; rechazó eliminación especulativa de API y del lifecycle obligatorio. |
| gpt-5.6-sol / sol_parity | Razón cross-domain Core→Operation→economía | Cuatro repros por ingress real, agrupados por causa; no repitió F01/F02/F03/F05. |
| gpt-5.6-sol / sol_causal | Causalidad/economía/contexto/rollover | Seis probes más gaps source; Astra revisó hallazgos materiales y ejecutó repros finales aislados. Este agente causó el incidente documentado. |

Astra añadió las sondas de identidad temporal, reproducción autocontenida y Finish temprano. Se leyeron personalmente las fuentes de findings materiales/ambiguos; no se releyó todo el source cubierto. Tokens exactos no expuestos; no se estiman por número de agentes.

### F01–F05 adversarial status

```text
F01 = ADVERSARIALLY_CONFIRMED_FIXED
F02 = ADVERSARIALLY_CONFIRMED_FIXED
F03 = ADVERSARIALLY_CONFIRMED_FIXED
F04 = REMEDIATION_REQUIRED
F05 = ADVERSARIALLY_CONFIRMED_FIXED
```

Evidencia: regresiones `provider/bt_f01..f03_test.go`, `operation/bt_f04..f05_test.go` y vecinos nuevos `s03_luna2_*`. Luna probó nil distribution atómica, clear/reacquire permutation, required-flat EXACT_REPLAY y fallo de allocator de Operation con retry. F04 falla con correlación omitida válida; F02 del catálogo S03 conserva ese repro junto con la frontera de ownership incompleta, sin cobrarlo como dos hallazgos.

### Findings aceptados

REPRO nombra tests. Comando común desde raíz del repo: `go test -tags s03review <paquete> -run '<nombre>' -count=1`. Paquetes: `./v3/backtester`, `./v3/core/internal/functions`, `./v3/sdk/futures/{operation,provider}` según ubicación. Para toda la evidencia nueva: `go test -tags s03review ./v3/backtester ./v3/core/internal/functions ./v3/sdk/futures/provider ./v3/sdk/futures/operation -run '^(TestS03_|Test_s03_)' -count=1 -timeout 10m`. El rojo es evidencia esperada, nunca suite certificada verde.

#### BT-S03-F01 — CRITICAL

- **ID:** BT-S03-F01
- **SEVERITY:** CRITICAL
- **SUMMARY:** Los límites temporales no participan en RunID ni input_sha256.
- **BROKEN_INVARIANT:** §13.1/§16.1: identidad por todos los inputs causales, incluido rango.
- **SOURCE:** backtester/identity.go:43–110; compose.go:194–210,337–358.
- **REPRO:** TestS03_Astra_TimeBoundsParticipateInIdentity, seis variantes: tres límites × dos modos.
- **EXPECTED:** Cambiar warmup_start/trade_start/end_exclusive cambia identidad.
- **ACTUAL:** Mismo RunID y digest; warmup/end cambian roots 49→48 y end cambia frontera16:00→15:59.
- **IMPACT:** Experimentos distintos comparten identidad canónica; determinismo bajo inputs completos no es defendible.
- **S04_REQUIRED_CHANGE:** Incluir los tres límites y todo parámetro causal omitido en ImmutableInputs y BaseImmutableInputs; reconstruirlos desde resultado.
- **REGRESSION_REQUIRED:** Seis variantes rojas; mantener A/A/B/A, procesos frescos y equivalencia entre layouts.

#### BT-S03-F02 — CRITICAL

- **ID:** BT-S03-F02
- **SEVERITY:** CRITICAL
- **SUMMARY:** Fills de otra cuenta/contrato atraviesan los guards; correlación ausente se inventa.
- **BROKEN_INVARIANT:** §8.2/BT-F04: ownership y correlación original antes de mutar estado/economía.
- **SOURCE:** sdk/futures/operation/engine_inputs.go:327–329,478–524; domain/execution.go:52–85.
- **REPRO:** TestS03_Sol1_ForeignExecutionAccountCannotMutateOwner; ForeignContractCannotFillPinnedOrder; TestS03_Luna2_F04_MissingCorrelationDoesNotUseCurrent.
- **EXPECTED:** Causa ajena auditada sin mutar owner; IDs desconocidos permanecen desconocidos.
- **ACTUAL:** Core real registra fill acct-foreign o ESZ6 en owner/orden NQZ6; fact sin IDs recibe op-1 actual.
- **IMPACT:** Contaminación de exposición, orden, capacidad y MM; fallback durable demuestra F04 incompleto.
- **S04_REQUIRED_CHANGE:** Validar cuenta y contrato contra owner/Operation/orden antes de sidecar; preservar correlación original o UNKNOWN explícito en facts.
- **REGRESSION_REQUIRED:** Tres repros; assert estado/MM/efectos intactos, tipado/raw/direct Apply y late/terminal/current.

#### BT-S03-F03 — MATERIAL

- **ID:** BT-S03-F03
- **SEVERITY:** MATERIAL
- **SUMMARY:** La economía del fill se instala antes de dedup nativo y correlación de orden.
- **BROKEN_INVARIANT:** §8.2: duplicado/ajeno no reemplaza autoridad económica.
- **SOURCE:** sdk/futures/operation/engine_inputs.go:335–377.
- **REPRO:** TestS03_Sol1_RawDuplicateCannotDowngradeIndependentEconomics; UnmatchedOrderCannotInstallEconomicsSidecar.
- **EXPECTED:** Dedup/order guard primero; revisión independiente intacta.
- **ACTUAL:** Raw duplicate cambia fresh true→false; orden desconocida instala revisión AVAILABLE con PnL -900.
- **IMPACT:** Decisiones posteriores observan autoridad incorrecta aunque el input adversarial no vuelva a llamar MM inmediatamente.
- **S04_REQUIRED_CHANGE:** Resolver guards/dedup antes de normalizar, registrar e instalar sidecar; conservar auditoría física.
- **REGRESSION_REQUIRED:** Los dos repros por fn.Invoke real; revisión, freshness, MM count y efectos exactos.

#### BT-S03-F04 — CRITICAL

- **ID:** BT-S03-F04
- **SEVERITY:** CRITICAL
- **SUMMARY:** El cambio de contexto conserva autoridad anterior y admite state modes incompatibles.
- **BROKEN_INVARIANT:** §11.2/A45–A47/A59–A60: next_context completo, coherente y atómico.
- **SOURCE:** backtester/run.go:33–144; controls.go:73–79; driver.go:324–326; run.go:510–530.
- **REPRO:** Test_s03_sol2_context_transition_installs_next_binding; preserve_stage_rejects_stage_change.
- **EXPECTED:** Binding deshabilitado bloquea fills; PRESERVE_STAGE rechaza stage distinto.
- **ACTUAL:** Dos fills después de instalar contexto con binding disabled; PRESERVE_STAGE acepta otro stage. Apply reutiliza binding/RuleSet del spec inicial y calendario anterior.
- **IMPACT:** Resultado nombra contexto B mientras riesgo/operación siguen usando A; progreso puede quedar atribuido a etapas distintas.
- **S04_REQUIRED_CHANGE:** Materializar autoridades completas existentes de next_context; validar modes contra contexto instalado; preparar y comprometer Provider/ledger/views/MM/calendario conjuntamente; fencing de timers.
- **REGRESSION_REQUIRED:** Dos repros; RuleSet/MM A→B, rollback sin effects, balance preservado, contexto en EOD/DST y exacto un boundary.

#### BT-S03-F05 — CRITICAL

- **ID:** BT-S03-F05
- **SEVERITY:** CRITICAL
- **SUMMARY:** Lifecycle STOP/AWAIT_CONTEXT no tiene productor dentro del engine.
- **BROKEN_INVARIANT:** §11.1/§11.4/A48: outcome causal de etapa, drain y continuidad reales.
- **SOURCE:** backtester/compose.go:110–114; driver.go:309–313; finish.go:33–34; run.go:71–72,139–143; sdk/futures/provider/risk_eval.go:403–468.
- **REPRO:** Test_s03_sol2_lifecycle_is_produced_in_engine y búsqueda de call sites EvaluateLifecycle/currentTerms.
- **EXPECTED:** Resultado de etapa asentado produce STOP o AWAITING_NEXT_CONTEXT.
- **ACTUAL:** Cero lifecycle rows y avance al horizonte; ningún call site del evaluator en backtester, ni inicialización de currentTerms al componer.
- **IMPACT:** A48 no está implementada; resultados de evaluación/continuidad no son certificables.
- **S04_REQUIRED_CHANGE:** Conectar evaluator shared, terms iniciales, progreso/outcome de etapa y políticas STOP/AWAIT_CONTEXT en prefijos asentados; conservar latches/archive.
- **REGRESSION_REQUIRED:** Repro actual usa umbral artificial -100 USD y net -72.48; es sonda del wiring, no certificación prop. S04 debe añadir PASS con target positivo, FAIL terminal, mínimo0/nil/positivo, ambos modos y siguiente contexto causal.

#### BT-S03-F06 — CRITICAL

- **ID:** BT-S03-F06
- **SEVERITY:** CRITICAL
- **SUMMARY:** La freshness económica no envejece y COMPLETE acepta posiciones con marks vencidos.
- **BROKEN_INVARIANT:** §9.2/§15/A11/A23: valoración/riesgo actual antes de decisiones y al terminar.
- **SOURCE:** backtester/projection.go:72–76; finish.go:78–84; sdk/futures/accounting/ledger.go:242–266,714–761; ningún SetFreshness en backtester.
- **REPRO:** Test_s03_sol2_final_open_position_rejects_stale_mark.
- **EXPECTED:** Mark requerido vencido bloquea nuevo riesgo y finalización válida.
- **ACTUAL:** COMPLETE a16:00 con NQZ6 +1 y unrealized -3.75 usando mark14:10, max age1min.
- **IMPACT:** Valuación/riesgo falsamente vigentes, especialmente sin ticks y en contrato retirándose.
- **S04_REQUIRED_CHANGE:** Revalidar edad contra reloj lógico en avances/decisiones/finalización; propagar revisión no-fresh/unresolved; no condicionar rechazo al unrealized distinto de cero.
- **REGRESSION_REQUIRED:** Repro; marca ausente con unrealized0, cashflow/timer al límite, viejo contrato y sin tick, restauración por dato válido.

#### BT-S03-F07 — MATERIAL

- **ID:** BT-S03-F07
- **SEVERITY:** MATERIAL
- **SUMMARY:** El driver absorbe conflictos de identidad de cashflow.
- **BROKEN_INVARIANT:** §11.3/A50: igual identidad y payload=no-op; payload distinto=conflicto fatal.
- **SOURCE:** backtester/run.go:179–193; sdk/futures/accounting/ledger.go:641–652.
- **REPRO:** Test_s03_sol2_cashflow_identity_conflict_is_fatal.
- **EXPECTED:** Mismo cashflow_id con100 y200 falla explícitamente.
- **ACTUAL:** COMPLETE, sólo100 asentados y ningún capsule de conflicto.
- **IMPACT:** Una instrucción monetaria contradictoria parece retry exitoso.
- **S04_REQUIRED_CHANGE:** Propagar el conflicto del ledger; distinguir replay idéntico antes de exigir contexto actual, incluso tras transición.
- **REGRESSION_REQUIRED:** Repro; replay idéntico antes/después de contexto con una sola revisión monetaria y conflicto en ambos casos.

#### BT-S03-F08 — MATERIAL

- **ID:** BT-S03-F08
- **SEVERITY:** MATERIAL
- **SUMMARY:** NDJSON no comprueba la identidad lógica pedida al abrir el corpus.
- **BROKEN_INVARIANT:** §2.1/§5.1: manifest/selection inmutables compatibles.
- **SOURCE:** backtester/internal/datasets/ndjson/ndjson.go:357–385.
- **REPRO:** Test_s03_luna1_ndjson_selection_identity, subtests corpus_id/version.
- **EXPECTED:** Rechazar corpus/version no correspondientes.
- **ACTUAL:** Ambas selecciones incompatibles retornan cursor. CLI tiene guard parcial separado; API pública no.
- **IMPACT:** Dataset distinto puede ejecutarse bajo identidad declarada del caller.
- **S04_REQUIRED_CHANGE:** Validar identidad/versión y correspondencia con manifest en la frontera del adapter/API; mantener receipt fuera del hash lógico.
- **REGRESSION_REQUIRED:** Ambos negativos; mismo manifest por una parte/chunks/gzip/segundo adapter continúa idéntico.

#### BT-S03-F09 — MATERIAL

- **ID:** BT-S03-F09
- **SEVERITY:** MATERIAL
- **SUMMARY:** Se certifica COMPLETE sin haber alcanzado un stop contractual válido.
- **BROKEN_INVARIANT:** §14–§15/A27/A33/A42: horizonte y cobertura demostrados, no inferidos de EOF/Finish.
- **SOURCE:** backtester/finish.go:16–24,65–103; driver.go:230–245; spec.go:103–126.
- **REPRO:** TestS03_Astra_EarlyFinishCannotCertifyHorizon; Test_s03_luna1_short_corpus_cannot_complete.
- **EXPECTED:** Finish temprano no COMPLETE; cobertura declarada hasta16:00 no acredita horizonte18:00.
- **ACTUAL:** COMPLETE con roots0/frontier12:00 o corpus declarado hasta16:00 y frontier18:00.
- **IMPACT:** Acceptance falsa por ausencia de causas o cobertura; el test S02 dependía de REQUIRE_FLAT, no de la propiedad de horizonte.
- **S04_REQUIRED_CHANGE:** Exigir prueba de stop alcanzado/settled o marcar INCOMPLETE; validar cobertura declarada; ausencia legítima de trades no equivale a gap.
- **REGRESSION_REQUIRED:** Ambos repros; pausa parcial, STOP válido, EOF cubierto sin trades y old-contract data unavailable explícito.

#### BT-S03-F10 — MATERIAL

- **ID:** BT-S03-F10
- **SEVERITY:** MATERIAL
- **SUMMARY:** El schedule de rollover admite orden/cobertura/config refs inconsistentes.
- **BROKEN_INVARIANT:** §4.3/A37–A42: schedule total y candidatos causalmente preparados con config exacta.
- **SOURCE:** backtester/spec.go:384–431; run.go:314–338.
- **REPRO:** Test_s03_sol2_schedule_preflight_closes_causal_gaps: successor_coverage/effective_order/strategy_config_refs.
- **EXPECTED:** Rechazo previo de las tres inconsistencias.
- **ACTUAL:** Preflight acepta cobertura que acaba antes de prepare_at, sucesor efectivo antes del predecesor y refs ausentes; envelope se reconstruye sin consumir refs.
- **IMPACT:** Rollovers pueden fallar tarde o usar autoridad diferente a la declarada.
- **S04_REQUIRED_CHANGE:** Validar orden/cadena/cobertura requerida y refs/digests exactos; consumir configuración candidata fijada; conservar slots/pins existentes.
- **REGRESSION_REQUIRED:** Tres repros; A→B→C con drenaje solapado, no resurrection ABA, cobertura vieja hasta liberar obligaciones.

#### BT-S03-F11 — MATERIAL

- **ID:** BT-S03-F11
- **SEVERITY:** MATERIAL
- **SUMMARY:** Seal/verificación/finalización aceptan input_sha256 falso.
- **BROKEN_INVARIANT:** §16.1/A31: digest final corresponde exactamente a ImmutableInputs.
- **SOURCE:** backtester/resultwriter.go:241–270; reproduce.go:262–294.
- **REPRO:** Test_s03_luna1_result_input_digest_is_verified.
- **EXPECTED:** Rechazar digest falso antes de aceptación canónica.
- **ACTUAL:** Artifact producido por engine real con digest alterado se finaliza y verifica.
- **IMPACT:** La verificación avala una identidad de inputs inconsistente; no se afirma que Run normal la compute mal.
- **S04_REQUIRED_CHANGE:** Recalcular/validar digest y coherencia de identidad/modo en las fronteras existentes de seal/read/finalize.
- **REGRESSION_REQUIRED:** Repro con inputs válidos; tamper en digest/inputs, ambos modos, idempotencia/conflicto preservados.

#### BT-S03-F12 — MATERIAL

- **ID:** BT-S03-F12
- **SEVERITY:** MATERIAL
- **SUMMARY:** El artifact no contiene todo lo necesario para reproducir configuración y controles.
- **BROKEN_INVARIANT:** §16.1/§18/A30/A57: autocontenido salvo corpus/build durable; replay de admisiones por frontera.
- **SOURCE:** backtester/identity.go:43–110; cmd/echo-backtest/reproduce.go:54–57,169–192; run.go:133–139.
- **REPRO:** TestS03_Astra_ResultReproducesWithoutSiblingSpec: artifact COMPLETE real + corpus original + CLI real.
- **EXPECTED:** Reproducir desde artifact sin archivo lateral de configuración.
- **ACTUAL:** CLI falla buscando runspec.json; inputs sólo guardan ConfigDigest y digests de controles/admisiones.
- **IMPACT:** Un result descargado aisladamente no puede reconstruir el experimento; controles pendientes carecen de payload reproducible inline.
- **S04_REQUIRED_CHANGE:** Sellar configuración resuelta y payloads tipados/admisiones completos; reconstruir RunSpec y replay causal desde resultado.
- **REGRESSION_REQUIRED:** Repro; reproducción standalone CLOSED_SPEC y CALLER_CONTROLLED con control aplicado y futuro pendiente; primera divergencia completa.

#### BT-S03-F13 — MATERIAL

- **ID:** BT-S03-F13
- **SEVERITY:** MATERIAL
- **SUMMARY:** Controles CLOSED_SPEC al horizonte no tienen disposición pendiente estructurada.
- **BROKEN_INVARIANT:** §11.4/§15–§16: todo control aceptado termina aplicado o pendiente declarado.
- **SOURCE:** backtester/driver.go:259–266; finish.go:106–140.
- **REPRO:** Test_s03_luna1_closed_control_at_horizon_is_visible.
- **EXPECTED:** Control sin efecto conserva disposición pending explícita.
- **ACTUAL:** inputs.Controls retiene cf-at-end, pero COMPLETE no contiene residual/admission pending ni cashflow record.
- **IMPACT:** Auditoría del resultado queda incompleta; el control no desaparece de inputs ni se aplica fuera de tiempo.
- **S04_REQUIRED_CHANGE:** Sellar disposición de controles declarados y admitidos uniformemente, sin efectos fuera del horizonte.
- **REGRESSION_REQUIRED:** Control antes/en/después del límite en ambos modos y replay del pendiente.

#### BT-S03-F14 — KISS

- **ID:** BT-S03-F14
- **SEVERITY:** KISS
- **SUMMARY:** Publish verifica dos veces el mismo gzip en la misma frontera CLI y quedan tres helpers muertos.
- **BROKEN_INVARIANT:** §4/§17 y gate KISS: una responsabilidad, sin trabajo/código innecesario.
- **SOURCE:** backtester/cmd/echo-backtest/publish.go:39–45,86–96; run.go:190–202; compose.go:334; backtester/run.go:208; driver.go:132.
- **REPRO:** Inspección de llamadas consecutivas y rg de liveConfigPtr/isCashflowDup/calendarTransitionKind: sólo definiciones.
- **EXPECTED:** Una lectura verificada devuelve count/state/runID; ningún helper sin caller.
- **ACTUAL:** Dos ReadResult+VerifyResultIntegrity completos; tres funciones sin caller.
- **IMPACT:** Coste duplicado proporcional al artifact y código inalcanzable sin invariante propia.
- **S04_REQUIRED_CHANGE:** Reutilizar una lectura en CLI; borrar esos tres helpers. Mantener verificación independiente del publisher público. No nueva abstracción/framework.
- **REGRESSION_REQUIRED:** Conformance local/fake-S3, COMPLETE vs attempts, counts/IDs/digests idénticos; build y búsqueda cero refs colgantes.

#### BT-S03-F15 — MINOR

- **ID:** BT-S03-F15
- **SEVERITY:** MINOR
- **SUMMARY:** El driver confía en que el adapter filtre market en end_exclusive.
- **BROKEN_INVARIANT:** §15: ningún fill causado por market fuera del intervalo half-open.
- **SOURCE:** backtester/driver.go:258–299.
- **REPRO:** Test_s03_luna1_market_at_end_exclusive con source deliberadamente no filtrante.
- **EXPECTED:** No fill en límite o error de contrato nombrado.
- **ACTUAL:** Fill simulado exactamente en end_exclusive; NDJSON normal sí filtra.
- **IMPACT:** Defensa faltante frente a adapter incumplidor; no se demostró fallo del adapter productivo normal.
- **S04_REQUIRED_CHANGE:** No obligatorio para S04; si se toca esa frontera, rechazar market fuera de selección sin bloquear timers legítimos del límite.
- **REGRESSION_REQUIRED:** Repro adversarial y timer/session legítimo al horizonte.

#### BT-S03-F16 — MINOR

- **ID:** BT-S03-F16
- **SEVERITY:** MINOR
- **SUMMARY:** ReproduceCmd emite una invocación ajena a la CLI entregada.
- **BROKEN_INVARIANT:** §18: comando de reproducción utilizable.
- **SOURCE:** backtester/reproduce.go:301–324; cmd/echo-backtest/reproduce.go:24–37.
- **REPRO:** Test_s03_luna1_reproduce_cmd_is_executable.
- **EXPECTED:** echo-backtest reproduce con result/dataset resolubles.
- **ACTUAL:** btctl backtest reproduce con flags no implementados y corpus@version en vez de archivo.
- **IMPACT:** Capsule requiere corrección manual del comando; no altera economía.
- **S04_REQUIRED_CHANGE:** No blocker independiente; corregir al tocar reproducción por F12 sin crear otra CLI.
- **REGRESSION_REQUIRED:** Ejecutar el comando generado contra artifact/corpus del repro.

### KISS/YAGNI, false positives y acceptance challenges

`KISS_YAGNI = REMEDIATION_REQUIRED`, exclusivamente F14. No cleanup masivo. No se exige quitar interfaces de I/O, doble frontera interna/pública de publicación, spoolRecorder, preflight NDJSON ni complejidad intrínseca de rollover/accounting. Consolidar otras recetas SHA queda observación opcional; borrar API pública sin probar consumidores fue rechazado. La rama AWAIT_CONTEXT es requisito sin wiring, no código que pueda borrarse por estética.

- A28: A/A y procesos frescos iguales son evidencia útil, pero no cubren experimentos distintos que colisionan en identidad (F01).
- A53–A56: el test sí atraviesa decode/dispatch Core real. Dos adapters pueden coincidir ejecutando el mismo defecto shared; eso no certifica ownership ni economía (F02/F03).
- A27/A42: REQUIRE_FLAT fallaba por la posición; el caso no probaba cobertura bajo REPORT_RESIDUALS ni Finish temprano (F09).
- A45–A48/A59–A60: assertions de identidad/record y tests puros SDK no demuestran que el driver instale otra autoridad o produzca lifecycle (F04/F05).
- A49/A50: ledger correcto no compensa al caller que convierte conflicto en éxito (F07).
- A31: hash lógico consistente de un footer internamente incoherente no demuestra input_sha256 correcto (F11).
- A30/A57: replay manual alimentado con configuración/controles originales no prueba reproducción desde artifact standalone (F12).
- A51/A52: chunk/gzip/streaming conservan evidencia base; eso no valida identidad incompatible al abrir (F08).
- F15 fue reducido a MINOR: sólo source incumplidor; no se acusa a NDJSON normal. Su repro distingue fills fuera de horizonte de timers legítimos en el límite.
- F13 no afirma pérdida del payload declarado ni cashflow fuera de tiempo: demuestra falta de disposición estructurada en el resultado.

### Veredictos de dominio

**Runtime parity:** extracción y shared path son reales; no se demostró una implementación duplicada ni una divergencia adicional entre adapters equivalentes. **Corrección compartida no defendible** por F02/F03, reproducidos mediante Core real y relevantes para LIVE. La provisión/deploy físico de economía LIVE continúa fuera de scope.

**Causal/economic:** no defendible por contexto anterior operativo, lifecycle ausente, marks vencidos, conflictos monetarios absorbidos y COMPLETE prematuro. No se contradijeron las fórmulas FIFO/fee-once ni el matching normal por contrato de la fixture. No se acepta un finding separado de lookahead, double-close o carrera sealed-fill/cancel sin repro suficiente.

**Determinism:** repetición del mismo fixture/build puede ser byte-idéntica; la identidad no representa todos los inputs causales y reproducción standalone no está completa. No se certifica deterministic reproducibility global. Nada se afirma cross-build.

### Verificación final y residuales

Tras integrar sólo tests nuevos se ejecutaron paquetes explícitos dentro de namespace de red nuevo (`unshare --user --map-root-user --net`, sólo loopback habilitado), con GOPROXY/GOSUMDB deshabilitados. No utilizar `go test ./...` desde SDK: contiene tests que escriben ETCD real.

Comandos requeridos: SDK `go test ./v3/sdk/futures/...`; Backtester `go test ./v3/backtester/...`; Core `go test ./v3/core/internal/functions ./v3/core/internal/futuresruntime ./v3/core/internal/futuresvertical`; consumidores `go test ./v3/futures-bridge/... ./v3/futures-projector/...`; build `go build ./v3/backtester/cmd/echo-backtest`. Todos con `-count=1` y timeout explícito cuando aplica. Logs `reports/final-*.log` externos; repros tagged separados de suite heredada.

| Validación final Astra | Resultado |
| --- | --- |
| SDK futures completo | PASS, exit0 |
| Backtester completo | PASS, paquete principal397.002s; NDJSON12.356s; store0.445s; sim0.099s |
| Core affected surfaces | PASS, functions0.466s, futuresruntime0.041s, futuresvertical67.149s |
| futures-bridge + futures-projector | PASS, exit0; consumers local-only, no certificación D6 |
| Build CLI | PASS, exit0 |
| Repros tagged | FAIL esperado,20 tests top-level rojos; vecinos provider/F05 sin falla nueva |
| Diff hygiene / producto | PASS; sólo seis tests nuevos, branch aceptado no mutado |

La suite SDK amplia accidental anterior **FAIL y con efectos externos** no se cuenta como certificación. Los repros son diagnósticos: si S04 rechaza correctamente un input antes del punto que hoy alcanza el repro (por ejemplo Seal/FinalizeLocal en F11), se puede ajustar exclusivamente ese oráculo para aceptar el rechazo correcto y conservar la propiedad; nunca debilitarla para forzar verde.

`REAL_CONDITIONAL_WRITE = NOT_VERIFIED_ENVIRONMENTAL`. No se buscaron credenciales S3 ni se certificó escritura condicional remota. Fake/local conformance se incluye en Backtester. Esto no se convierte en finding ambiental de código.

### Incidente operativo abierto — fuera del contrato productivo BT-S04

El subagente Sol causal ejecutó por error `go test ./...` desde `v3/sdk`, pese al límite de paquetes y prohibición de infraestructura. El test legacy `TestSeedEchoConfig_Production` reportó escrituras bajo `/echo/production/` a las 14:19:46–14:19:48 America/Santiago del 2026-10-04. El resumen dijo 32 claves; 31 nombres Set individuales quedaron observados. Familias afectadas: bridge, core, functions, gateway, kafka, postgres y telemetry; incluye `postgres/password`. No se persisten valores ni se infiere la clave restante. Después falló el readback de `bridge/reference_accounts`; también hubo fallos de autenticación PostgreSQL y conexión Jaeger. Esas fallas no cuantifican el impacto runtime.

El comando SDK terminó FAIL por sí mismo. El Primary detuvo el frente, terminó dos procesos posteriores de backtester y escaló inmediatamente al Owner. No hubo restauración ni lectura adicional de stores para investigar valores. La evidencia original está en el transcript de herramientas y su resumen sanitizado en `reports/incident.md`; no existe stdout completo guardado como archivo. No confundir “sin cambios productivos en Git” con “sin efectos externos”. La responsabilidad de coordinación permanece en el Primary.

**Pendiente humano:** revisar/restaurar desde historial autorizado y verificar servicios afectados. Ninguna suite local posterior certifica recuperación. Las suites finales se aislaron sin red externa precisamente para impedir recurrencia. Este incidente no modifica la evaluación del delta Git D6 ni acredita su estado físico.

### BT-S04 REMEDIATION CONTRACT

- **Findings aceptados obligatorios:** BT-S03-F01–BT-S03-F13 y reducción KISS BT-S03-F14. F15/F16 son MINOR; no justifican por sí solos ampliar el shot. F16 puede corregirse al resolver F12. F01/F02/F03/F05 originales conservan cierre; F04 original se cierra con evidencia de F02 S03.
- **Product code:** únicamente identidad/composición/driver/finalización/control/proyección/dataset/result/reproducer del Backtester y shared Operation en las fuentes nombradas; wiring/evaluator shared Provider según F05. Instalar autoridades frozen existentes, no crear campañas, DSL, workflow ni otro runtime. Corregir causación económica y validación antes de producir efectos. No implementar una solución específica de fixture.
- **Tests requeridos:** conservar y volver verdes los repros materiales/críticos; agregar únicamente las regresiones de cada finding, especialmente target positivo STOP/AWAIT_CONTEXT, transición RuleSet/MM/calendar/EOD/DST, native dedup, stale marks y replay de controles desde el artifact. No debilitar asserts ni convertir errores en skip. Los MINOR quedan separados mientras estén abiertos.
- **KISS obligatorio:** una lectura/verificación CLI para count/state/runID; borrar liveConfigPtr/isCashflowDup/calendarTransitionKind; preservar la verificación de integridad del publisher público. No otras eliminaciones/refactors masivos.
- **D6 reconciliation:** NON_CONFLICTING al HEAD final d08a30ce; ninguna integración D6 requerida. Refrescar ambos branches y revisar sólo el nuevo delta; no merge/cherry-pick preventivo.
- **Final certification suite:** SDK futures, Backtester completo+CLI build, Core functions/futuresruntime/futuresvertical, consumers futures-bridge/futures-projector; misma build A/A/B/A, procesos frescos, layouts alternativos, replay caller-controlled y conformance local/fake-S3. Usar lista de paquetes explícita y aislamiento sin red externa; MinIO real sólo con acceso autorizado. Certificar contra el HEAD exacto de S04 con todos los bloqueantes verdes.

### Final gate

El Manager revisa primero este artifact. No se emite prompt de BT-S04 al Owner ni se inicia implementación. Los hallazgos demostrados impiden PASS independientemente de que la suite heredada resulte verde.

El cierre de Agents-OS conserva continuidad en el proyecto y registros por modelo, sin L0/L1 inventados. Feedback limitado al incidente reusable. Próximo responsable: Primary Technical Manager; la recuperación de configuración de producción sigue escalada por separado.

## Fuentes

- [[Echo Futures — BT-S01 Backtester V1 Design]], autoridad frozen completa.
- [[Echo Futures — BT-S02 Backtester V1 Implementation Handoff]], claims aceptados como objeto de challenge.
- [[Echo Futures]], proyecto activo; Agents-OS bootstrap y cierre por delta.
- `xKoRx/echo@f41da25cc0b779ea48375198dbedaf932b930a80`, source inspeccionado; branch review con repros tagged.
- Workspace externo de review `bt-s03-20261004/reports/{luna1,luna2,luna3,sol1,sol2,astra,incident}.md`, baselines y logs finales. Reportes subordinados a la integración y severidades de este documento.

BT_S03_REMEDIATION_REQUIRED

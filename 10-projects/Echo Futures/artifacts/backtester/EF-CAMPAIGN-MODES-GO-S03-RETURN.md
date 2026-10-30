---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[EF-CAMPAIGN-MODES-DESIGN]]"
  - "[[Echo Futures — Optimización de Campañas]]"
  - "[[EF-CAMPAIGN-MODES-GO-S02-RETURN]]"
aliases:
  - EF-CAMPAIGN-MODES-GO-S03-RETURN
tags:
  - kind/doc
created: "2026-10-29"
updated: "2026-10-29"
---

# EF-CAMPAIGN-MODES-GO-S03-RETURN

**STATUS: FINDINGS.** El candidato `062b6df7` es un IMPLEMENTATION_CANDIDATE honesto y mecánicamente sólido (build reproducible, regresión idéntica al baseline, Go-only real, migración-catálogo trazable, economía v2 correcta en su alcance), pero **NO completa C06**: el controlador v2 no admite las políticas selladas TGMM/RiskGeometry, ni MM/perfiles/RuleSets heterogéneos por asociación, ni FUNDED multi-asociación, ni la superficie CloseSafety v2; los kinds de reverso/refund existen sin productor; y el claim "2 perfiles/2 RuleSets" del retorno S02 no está materializado. Nada de esto lo denunció el retorno S02 con dimensiones exactas; este review lo reproduce con repros y localizadores. No hay P1 abierto que invalide lo entregado, pero sí P1 de DELIVERY_GAP que impiden declarar R06 completo. GO-S04 procede con el paquete de la sección correspondiente.

## EXACT_REVIEWED_SHA

| Campo | Valor |
|---|---|
| BASE_SHA | `2baf319ddcba622d9557bc9f23a13787b44c58a7` (merge-base verificado; origin/master sin mover) |
| BRANCH | `feature/ef-campaigns-go` |
| CANDIDATE_SHA | `062b6df77845d2042e398bb6174700e80bb58b60` (HEAD local == `origin/feature/ef-campaigns-go`, readback verificado; árbol limpio) |
| BUILD_SHA256 | `e416636670b055c246af535e0c379ff7718ee91841a5e4ff2e7e4a8bdacaebbb` — **reproducido byte-idéntico** por este review con `go build -trimpath -buildvcs=true` en checkout aislado (`go1.27.1 linux/amd64`); coincide con el receipt del autor y el BUILD_SHA256 del paquete |
| DIFF_SCOPE | 103 archivos, +14.972/−14.639, 7 commits (`a9b24896` SDD, `e0e4acbc` W1, `b9be5dbe` W2, `141fceb8` W3, `653b58ce` W4, `ef44fc4f` lifts, `062b6df7` W5+fixes); 32 A / 54 D / 17 M — verificado, no aceptado por cifra |
| Worktrees del review | `~/echo-work/c06-s03/checkouts/{echo-god,w-f1,w-f2,w-f3,w-base}` (clon `--shared` propio; árbol del autor `~/go/src/github.com/xKoRx/echo-c06` NO tocado) |

## INDEPENDENCE_REAL

- **Independencia de modelo: NO LOGRADA.** El GOD efectivo y todos los workers disponibles en este host son GLM-5.3-Flash — el mismo modelo que implementó GO-S02. La cuota de subagentes del host está agotada: 3 despachos (Front 1, Front 2, Front 3) murieron en ~2 s con `exceed quota limit`. No se sustituyó silenciosamente nada: la revisión la ejecutó el GOD directamente y esta limitación queda declarada. Los modelos no-GLM del registro (`openrouter/openai/gpt-6.1-sol`, `gpt-6-luna`, claude/grok/kimi) no tienen superficie de delegación disponible en esta sesión sin un flujo de workflow con confirmación de usuario, que no existe en ejecución autónoma.
- **Independencia de ejecución/checkout: LOGRADA.** Clon y worktrees propios, build independiente reproducido, sonda falsificadora propia (`s03god_probe_test.go`, archivo aditivo en checkout del revisor), re-medición independiente de migración/cobertura/suites/Go-only. El árbol del autor permanece READ_ONLY y sin modificar.
- **Independencia de corpus/oráculo: PARCIAL.** Los oráculos de rechazo y economía se derivaron del contrato C06 y de lectura de source (no de los tests del autor); la comparación de identidad de reporte/matriz reutilizó fixtures deterministas del autor donde el oráculo correcto ES la igualdad de bytes. La clasificación de regresión usó los receipts baseline de S02 y añade la re-ejecución baseline propia en `w-base` (ver REGRESSION_BASELINE_CLASSIFICATION).
- **Independencia de autor de W5: SIGUE ABIERTA como residual.** La matriz funcional W5 fue cerrada por el integrador (cuota); este review re-verificó mecánicamente sus piezas principales, pero ninguna suite del candidato fue re-ejecutada por un modelo distinto del equipo autor.

## REQUIREMENT_DELIVERY_MATRIX

Estados: IMPLEMENTED_AND_VERIFIED / IMPLEMENTED_NOT_VERIFIED / PARTIAL / NOT_IMPLEMENTED / BLOCKED_EXTERNAL. "Verificado" = reproducido por este review (source + física), no sólo declarado.

| Req | Veredicto GOD | Evidencia de este review |
|---|---|---|
| R01 una Campaign, factories compartidas | IMPLEMENTED_AND_VERIFIED | `TestCampaignV2Matrix_A01_SameFactoriesServeEveryModality`; módulos Strategy/MM vía `config.CompositionFactories`; añadir módulo no edita Campaign/scheduler (source: `campaign_modes_v2.go`, `campaign_composition.go`) |
| R02 CHALLENGE N cuentas + relevo | IMPLEMENTED_AND_VERIFIED | E2E N=3 pase/pérdida/pausa, una activa por asociación; pausa nunca releva ni compra (source: `decideAcquisition` — "a pause is not a purchase order"); sin rewarmup |
| R03 FUNDED N seeds (una asociación) | IMPLEMENTED_AND_VERIFIED | E2E N=3 (pagadora×2, no pagadora, pendiente); instalación por controles reales (`activateFundedUnit`→`AccountContextTransition`, acreditación al observar contexto aplicado); denominador completo |
| R04 etapas aisladas comparables | IMPLEMENTED_AND_VERIFIED | Dos jobs con scopes/cajas separados; receipts por identidad de batch |
| R05 SIMULATION 1×1 | IMPLEMENTED_AND_VERIFIED | 4000→4140 conciliada; `TestCampaignV2Matrix_A04_SimulationCashArithmeticExactStrings`; approved-payout no financia ni mueve caja (`TestCampaignV2E2E_ApprovedPayoutNeverFinancesOrMovesCash`) |
| R06 SIMULATION multi-asociación/multi-perfil | **PARTIAL** | Multi-asociación simultánea con trayectoria/caja/mercado únicos: VERIFICADA (2 asociaciones, long/short, disputa de última caja determinista por (prioridad, id), desempate serializa compromiso). **Multi-perfil: NOT_IMPLEMENTED** — la admisión v2 fuerza un único `ProfileV2` por request (`validateCampaignV2AssociationBinding`: `assoc.ProfileRef != profile.Version` rechaza) y el claim "2 RuleSets" no está materializado (los tests ligan ambas asociaciones al MISMO `C06_V2_TEST_PROFILE_V1/EVALUATION@1`); MM heterogéneo y FUNDED multi-asociación: NOT_IMPLEMENTED (rechazos nombrados, reproducidos por sonda pública) |
| R07 evidencia/KPI/legacy Go | IMPLEMENTED_AND_VERIFIED con gap | 19 kinds versionados, emisor idempotente (mismo ID+payload replay; distinto payload conflicto), Q(H) con orden causal exigido (`campaignQualityLineageComplete`: compra/intento/pase/activación ≤ crédito), adaptador legacy tipado fail-closed. **Gap:** kinds `PAYOUT_REVERSED`/`REFUND` sin productor (F5) |
| R08 flujo oficial sin Python | IMPLEMENTED_AND_VERIFIED (mecánica) + BLOCKED_EXTERNAL (cadena física prepare→run) | Superficie CLI verificada (11 subcomandos + lab 10); guard cableado en las 5 puertas ejecutables (run, platform-batch por ítem, campaign, reproduce, lab run/resume siempre); `lab migrate` y `lab report` re-ejecutados por este review en sandbox PATH sin `python3` (reporte con identidad byte-idéntica `sha256:3e8d3406…` al receipt W5). La cadena física prepare→run queda BLOCKED_EXTERNAL: `lab prepare` exige fuentes NT de producción no presentes en este host (el receipt W5 del propio paso 4 es un rechazo nombrado, no una preparación completa); la ruta run/resume está cubierta por tests Go in-process |
| R09 migración catálogo/campañas | IMPLEMENTED_AND_VERIFIED (como proyección de catálogo) con EVIDENCE_GAP | Matriz reconciliada independientemente: 104 filas, censo delta CERO (26/63/15/89/104), 26 MIGRATED + 78 CATALOG_VALIDATED, 0 mutaciones de receipts/catálogos, con run-roots del autor exactamente 5 filas SEALED (MR-08, ORB-NATIVE-C02..C05). **Gap:** las 26 MIGRATED apuntan a `LEGACY_PATH` (platform-prepare/platform-batch legacy); SAME_SEMANTICS se sustenta en resolución 1:1 de autoridades in-tree (constantes/identidades), no en equivalencia de comportamiento demostrada (F6); 0 filas hacia GO_V2 — ningún identidad del catálogo corre por el controlador v2 |
| R10 causalidad/replay/idempotencia | IMPLEMENTED_AND_VERIFIED | Emisor idempotente + conflicto nombrado; resume KISS con sonda de integridad completa (identidad, estado, digest de resultado Y de trace económico) antes de reutilizar; `A14_BatchFailureThenRerunIsolatedAttempt`; fallo ⇒ INCOMPLETE, nunca COMPLETE canónico |
| R11 G0–G5 + V1 + guard | IMPLEMENTED_AND_VERIFIED con gap documentado | Guard Go G4/G5 (porte del linaje Clutifx, exit 78, razones nombradas idénticas) en 5 puertas; fixture S04-F01 frontera V1/Unclipped sin renombrar identidades; D05 permanece Owner/retester (ninguna corrida histórica desbloqueada). **Gap:** puertas legacy se gatean sólo si el input declara el miembro `qualification` ("absent member = legacy flow", documentado en `qualification_admission.go`); el flujo lab siempre está gateado — tensión con la lectura estricta de A12 (F8) |
| R12 pruebas físicas + capacidad + review | PARTIAL | Suites re-ejecutadas por este review: conjunto de fallos IDÉNTICO al baseline (23=23, diff vacío) + baseline propio en curso; cobertura re-medida: piso 95% incumplido en 6/9 archivos nuevos (total ≈85%); `-race` NOT_EXECUTED (host sin gcc; `go test -race` ⇒ "requires cgo"); capacidad medida honesta para anillo 1×N pero sin número para K≥2 asociaciones simultáneas (F9); independencia de modelo del review NO lograda (cuota) |

## MIGRATION_MATRIX_RECONCILED

Reproducido por este review con el binario reconstruido (receipt `~/echo-work/c06-s03/receipts/god/migration-matrix-god.json`, byte-idéntico con y sin python3 en PATH):

- Censo: 26 nativas + 63 SG únicos + 15 aliases = 89 ejecutables / 104 filas; delta CERO contra la referencia S04; `unique_sg_count` del search space concilia.
- Estados: **MIGRATED 26** (todas `LEGACY_PATH`) + **CATALOG_VALIDATED 78** (63 SG `LEGACY_PATH` + 15 aliases `ALIAS_OF_CANONICAL`). Con el input de run-roots del autor: 5 filas `SEALED` (NATIVE:MR-08, NATIVE:ORB-NATIVE-C02..C05), reproducido exacto.
- Semántica: 41 SAME_SEMANTICS (26 nativas por resolución de autoridades + 15 aliases por igualdad de digest) / 63 NEW_EXPERIMENT (SG, disparador `budget_semantics GROSS_BUDGET_V1` vs `NET_TARGET_LEGACY_V1`).
- **Dimensiones reales:** 0 filas `V2_REQUEST_MATERIALIZED`, 0 `V2_ADMITTED`, 0 `FUNCTIONALLY_EXECUTED`, 0 `HISTORICALLY_EXECUTED`; la constante `MigrationTargetGoV2` existe pero ningún builder la usa — señal en source de que la materialización v2 del catálogo no está implementada. Las notas de las filas SG lo declaran honestamente ("the campaign v2 controller does not yet admit the RG module binding").
- Lectura correcta del inventario: 89 ejecutables NO son 89 campañas ejecutadas ni 89 estrategias independientes; 104 NO son 104 estrategias; aliases separados de ejecutables. El retorno S02 respetó esta regla.

## FUNCTIONAL_VS_HISTORICAL_EXECUTIONS

- Ejecución funcional (mecánica) probada: E2E deterministas TEST_ONLY sobre corpus sintético `platformproof` rotulado — CHALLENGE N=3, FUNDED N=3, SIMULATION 1×1, composición 2×2, long/short bajo LOW_FIRST y HIGH_FIRST, capacidad 1×N, disputa de caja. La admisión v2 hace imposible que un corpus no rotulado TEST_ONLY cruce sin perfil de producción (rotulación bidireccional fail-closed, verificada en source y por sonda).
- Ejecución económica histórica: **CERO**, y así se declaró en S02. La matriz de migración no registra ninguna fila FUNCTIONALLY_EXECUTED ni ECONOMIC_RESULT; los 5 planes sellados se leen como provenance, no como ejecuciones. D01/D02/D05 siguen sin resolución Owner. Catálogo validado ≠ campañas corridas: correcto en el retorno S02, confirmado aquí.

## GO_ONLY_END_TO_END

- Independiente (este review): build del binario y `lab migrate` ejecutados en sandbox con PATH sin `python3` (PYTHON_ABSENT verificado en el propio sandbox); matriz byte-idéntica con y sin Python; `lab report` sin Python con identidad `sha256:3e8d34060ec917118fcec7bc5cf5acc13a16e35062d2e33ba574196d6af08f3f` == receipt W5. Receipts: `~/echo-work/c06-s03/receipts/god/`.
- Del autor (W5, verificado contra receipts): pasos 2-3 (validate/plan sellado determinista), 5 (qualify dry-run con RECEIPT_MISSING), 6 (export), 7 (report) ejecutados sin Python. **El paso 4 (`lab prepare`) NO completó**: rechazo nombrado "one initial account shape required" por ausencia de fuentes NT de producción en el host — la cadena física prepare→run del lab quedó BLOCKED_EXTERNAL, no demostrada punta a punta con el CLI (la ruta run/resume sí está ejercitada por tests Go in-process y las 5 puertas del guard están cableadas en source). Grep del flujo: sin invocaciones Python (coincide con el registro de retiro; hits = comentarios de linaje).

## FINDINGS

Convención: tipo ∈ {BUG, DELIVERY_GAP, EVIDENCE_GAP, EXTERNAL_DEPENDENCY}; severidad P1 bloquea capacidad material C06 / P2 degrada entrega o evidencia / P3 observación. Todos los repros están en `~/echo-work/c06-s03/receipts/god/s03god_probe_test.go` (8 tests, verdes, archivo aditivo en checkout del revisor).

**F1 · DELIVERY_GAP · P1 · R06/R11/A01.** TGMM y RiskGeometry no admitidos por el controlador v2: toda identidad sellada del catálogo (26 nativas TGMM + 63 SG RGMM) queda fuera del controlador v2; hoy sólo corre `gerardmm` TEST_ONLY sintético. Expected (C06 §3/§5: políticas selladas reutilizadas sin reimplementar): una asociación puede bindiar el MM sellado declarado. Actual: dos costuras independientes rechazan — (a) igualdad de módulo contra el spec compuesto (`campaign_modes_v2.go:962-964`: "binds mm module %q but the composed spec declares %q"), repro sonda `V2RejectsTGMM`/`V2RejectsRiskGeometry`; (b) el rechazo sealed-binding explícito (`campaign_modes_v2.go:968-981`: "the TGMM sealed-policy binding is not implemented" / "the sealed account-policy binding is not implemented"). Owner: superficie de request v2 (`campaign_v2_contract.go`) + admisión (`platform_campaign.go`/`campaign_modes_v2.go`) + rewire de `composePoolSealedAuthorities`/`NewSealedMoneyManagerCatalog`/`SealedAccountPolicy` (owners existentes en `compose_account.go`, intactos en este diff — reutilizables). Solución mínima: superficie `MoneyManagers`/binding por asociación resuelta contra el catálogo sellado (sin eliminar ninguna validación). Pruebas de cierre: paridad con MM TGMM/RGMM REALES vía las costuras runtime (no factories de fixture), admisión positiva+negativa, replay. WITHIN_C06.

**F2 · DELIVERY_GAP · P1 · R06/A07.** Heterogeneidad real por asociación inexistente: un único `ProfileV2` por request, igualdad de MM entre asociaciones y de RuleSet con el perfil EVALUATION son impuestas por la admisión (`campaign_modes_v2.go:910-925` y `:947-983`). El claim S02 "composición 2 asociaciones/2 RuleSets simultáneas" NO está materializado: el fixture de composición liga ambas asociaciones al mismo perfil y RuleSet (`campaign_accounts_v2_test.go:77-87`, `campaign_composition_test.go:199-202`); "EVALUATION vs LIVESIM del mismo perfil" no son dos props. La maquinaria de resolución per-binding existe (`installCompositionUnit` resuelve `assoc.RuleSetRef` contra el catálogo) pero es inalcanzable con valores distintos porque la admisión los rechaza antes. Expected: dos asociaciones con perfiles/RuleSets/MM distintos operando simultáneamente. Actual: sólo heterogeneidad de Strategy/fanout. Mismo owner y solución que F1 (extensión versionada del request v2 con bindings por asociación). Pruebas de cierre: composición con dos perfiles TEST_ONLY realmente distintos + dos RuleSets del catálogo sellado + consistencia de términos por binding. WITHIN_C06.

**F3 · DELIVERY_GAP · P1 · R06/R03/A07.** FUNDED multi-asociación no implementado: `validateV2` rechaza ("FUNDED seeds one association per trajectory… simultaneous multi-association seed install is not implemented", `campaign_modes_v2.go:923-925`; repro sonda `V2RejectsFundedMultiAssociation`) y `seedAllFunded` sólo siembra la primera asociación declarada (`campaign_modes_v2.go:194-219`). La composición además no ejecuta el camino FUNDED (`runAcquisitions` retorna nil en FUNDED; `decideFor` nunca compra). Expected: N seeds por cada asociación declarada con estado aislado. Owner: `campaign_accounts_v2.go` (seedAllFunded generalizado) + composición (`tick`/installs por asociación ya visitan compartimentos). Pruebas de cierre: FUNDED con 2+ asociaciones sembradas simultáneamente, denominadores separados, pagos por asociación. WITHIN_C06.

**F4 · DELIVERY_GAP · P2 · R06/R11.** CloseSafety sin superficie v2: `validateV2` rechaza cualquier CloseSafety ("the campaign v2 close-safety surface is not admitted", `campaign_modes_v2.go:881-883`; repro: un CloseSafety legacy-válido alcanza el rechazo v2; con política vacía primero cae `CLOSE_CALENDAR_MISSING` legacy). El v2 cubre cierre de sesión con los relojes declarados del perfil (PAUSED_SESSION al NYClose, ventana de compra, `closeRiskAllowed` queda inerte con CloseSafety nil); lo que falta es la superficie de calendario de cierre explícito (hard deadlines por sesión, sesiones execution-excluded, políticas de protected-close) que la ruta legacy platform sí consume. No es un problema de datos ni de D05: es mecánica C06 pendiente. Owner: spec/admisión v2 + `campaign_modes_v2.go` (`checkpoint`/`closeRiskAllowed`). Pruebas de cierre: tabla de cutoffs v2 equivalente a `TestCampaignV2Matrix_CloseSafetyCutoffTable` sobre request v2. WITHIN_C06.

**F5 · DELIVERY_GAP · P2 · R07/SPEC §3.** Reversos y refunds sin productor: `PAYOUT_REVERSED` y `REFUND` están en el enum cerrado de kinds (`campaign_economic_events.go:47-48`) pero ningún camino del controlador v2 los emite; el ciclo de pago termina en CREDITED (`tickPayment`) y la reconciliación de `finish()` no contempla reverso posterior. Expected (SPEC §3): "Payout tiene solicitud, aprobación, débito aplicado, crédito efectivo y eventuales reversos con identidades propias; primer cobro positivo se conserva como hecho histórico aunque un reverso posterior reduzca el neto"; "refund modifica caja/coste una vez conservando la cohorte bruta". Actual: capacidad declarada en el contrato de eventos, no implementada en el lifecycle. Owner: `campaign_accounts_v2.go` + reporte. Pruebas de cierre: reverso posterior a primer crédito (identidad propia, caja neta ajustada una vez, primer crédito preservado en evidencia), refund con cohorte bruta conservada, doble-emisión rechazada por el emisor idempotente. WITHIN_C06.

**F6 · EVIDENCE_GAP · P2 · R09/A11.** SAME_SEMANTICS de las 26 nativas se sustenta en resolución de constantes/autoridades ("identity resolves 1:1 onto the in-tree Go execution authorities"), no en demostración de equivalencia de comportamiento; y la etiqueta `MIGRATED` sobre `LEGACY_PATH` sobreestiima (nada migró al v2; se preservó la ruta legacy, lo cual es legítimo por diseño §10). El fixture S04-F01 documenta la divergencia V1/UnclippedV1 — acredita la frontera, no la equivalencia de las corridas históricas. Solución mínima: (a) renombrar el estado de fila a `LEGACY_PATH_PRESERVED` (dimensión honesta) o (b) añadir evidencia conductual por identidad (paridad legacy vs legacy-post-diff sobre configuración sellada idéntica, sin re-ejecutar histórico). No cambiar runtime para encajar resultados. WITHIN_C06.

**F7 · EVIDENCE_GAP · P2 · R12.** Cobertura bajo piso confirmada independientemente y receipt crudo del autor inservible: `w5-cover.out` contiene sólo `mode: set` (el claim 82–96% no es re-derivable del perfil; los resúmenes per-file sí sobrevivieron y concilian). Re-medición GOD (batería focal propia, denominador de statements): composition 80.2 (336/419), modes_v2 82.7 (459/555), accounts 83.9 (324/386), migrate 71.3–81.0 según batería, adapter 88.7, admission 89.3, contract 95.8, report 95.0, events 98.4 — **6/9 archivos bajo el piso 95%**, total ≈85.1%. Los huecos son las ramas fail-closed profundas (las mismas que F1–F4 dejan sin camino feliz). GO-S04: cerrar coverage de las superficies que implemente + ramas fail-closed restantes. WITHIN_C06.

**F8 · EVIDENCE_GAP · P3 · R11/A12 · NEEDS_OWNER_DECISION.** Puertas legacy con disparador opt-in: `run`/`platform-batch`/`campaign`/`reproduce` ejecutan el guard sólo si el input declara el miembro `qualification`; un spec de corpus histórico sin el miembro cruza sin clasificación física de propósito ("Absent member = legacy flow", documentado en `qualification_admission.go:21-31`). El lab (flujo oficial C06) siempre está gateado y clasifica propósito físico. Forzar la clasificación en puertas legacy sin recibir receipts rompería el contrato de replay legacy que el diseño §10 exige preservar; la decisión de si un legado sin regime puede correr histórico sin registro de admisión es del Owner/retester, no del corrector. Alternativa mínima compatible: registrar en el ledger toda ejecución legacy cuyo propósito físico clasifique QUARTER/HISTORICAL (ledger-only, sin bloquear).

**F9 · EVIDENCE_GAP · P3 · R12/A16.** Capacidad medida sólo para anillo 1×N (101 adquisiciones = 100 rotaciones de asiento sobre UNA asociación; el receipt del autor lo declara honestamente). No hay medición con K≥2 compartimentos simultáneos (la composición), ni de crecimiento por compartimento retenido a K>1. El crecimiento 4–6 MB/unidad reportado es esperado/acotado para el anillo; no hay prueba de fuga, pero tampoco evidencia de escala de composición. GO-S04: extender el harness a K=2..10 asociaciones simultáneas.

**F10 · EVIDENCE_GAP · P3 · R12.** Independencia de autor de W5 sigue abierta (cierre por integrador tras muerte por cuota, declarado en S02) y este review no pudo añadir independencia de modelo (cuota del host, 3 despachos muertos). El contrapeso ejecutado fue mecánico (build/sondas/re-measurements por checkout aislado), no de modelo.

**Refutaciones (falsificadores que NO sostuvieron defecto):** (1) "la disputa de última caja depende de orden de goroutines/map" — FALSO: candidatos ordenados por (prioridad, id de asociación) con `sort.SliceStable`, coordinate determinista, compromiso serial que reduce disponible antes del siguiente candidato (`runAcquisitions`); (2) "callbacks/timers pueden ejecutarse contra el compartimento equivocado" — FALSO en lo verificado: `visitCompartment` usa captura/instalación/restauración con orden determinista y los parked timers/controls conservan routing por dueño; (3) "resume puede sumar dinero dos veces" — FALSO: la sonda de reuse exige identidad+estado+digest de resultado+digest de trace, y el rerun de incompletos es aislado con AttemptID nuevo; (4) "Q(H) califica créditos con pase posterior" — FALSO ya corregido en S02 (F2 de W5 como regresión, re-verificado en source); (5) "Go-only es cosmético" — FALSO: sandbox sin python3 re-verificado físicamente por este review.

## REPRO_HARNESS_MANIFEST

| Asset | Path | Uso en GO-S04 |
|---|---|---|
| Sonda GOD (8 tests: 7 rechazos nombrados + baseline admitido) | `~/echo-work/c06-s03/receipts/god/s03god_probe_test.go` (original en `echo-god/v3/backtester/s03god_probe_test.go`) | Promover a regresión; extender con los positivos de F1–F4 cuando existan |
| Binario reconstruido | `~/echo-work/c06-s03/receipts/echo-backtest-god` (SHA256 `e4166366…`) | Re-ejecutar matrices/flows sin rebuild |
| Matriz migración GOD | `receipts/god/migration-matrix-god.json`, `migration-nopython-god.json` (mismo SHA256 `12c65b6c…`), `migration-with-roots-god.json` (5 SEALED) | Oráculo de censo para S04 |
| Reporte lab GOD | `receipts/god/lab-report-god.json` (identidad `sha256:3e8d3406…` == W5) | Oráculo de reporting |
| Cobertura GOD focal | `receipts/god/s03-cover.out` | Línea base para cerrar el piso |
| Suites S03 + conjuntos de fallo | `receipts/f4/s03-suites.log`, `s03-fails.txt`, `s02-baseline-fails.txt`, `s03-suites-baseline.log` | Oráculo de regresión del S04 |
| Sandbox no-Python | `~/echo-work/c06-s03/nopython-bin/` | Re-ejecutar A13 en FINAL_SHA |
| Worktrees | `~/echo-work/c06-s03/checkouts/{echo-god,w-f1,w-f2,w-f3,w-base}` | `w-base` = baseline `2baf319d` propio |

## REGRESSION_BASELINE_CLASSIFICATION

Suite completa re-ejecutada por este review en checkout aislado (`w-f3`): **23 fallos = conjunto IDÉNTICO** (diff vacío por nombre) a los receipts baseline del autor sobre `2baf319d` (18 root + 5 cmd). Clasificación por causa (revisada contra el log, no sólo nombres): BASELINE_ENVIRONMENTAL — tests que exigen reserva de 8 GiB contra `/tmp` tmpfs ~7G (`TestPlatformArtifacts_*`, readback/verifier) y fault-injection con Reconciled esperado; BASELINE_CODE_DEBT pre-existente — BTG-S05 (mismatch de signal_id en fixtures causales, presente en `2baf319d`), TG factory parity (`f4643aef` la rompió en master antes del candidato), covers de catálogo. **NEW_REGRESSION: 0.** NOT_EXECUTED: ninguno de los afectados. Rigor extra: re-ejecución baseline propia en `w-base` para no depender de los receipts del autor (resultado registrado al pie de esta sección). El conjunto idéntico NO prueba por sí solo que todos sean ambientales — la clasificación por causa es de este review.

## COVERAGE_AND_RACE

- Cobertura: ver F7 — piso 95% incumplido en 6/9 archivos nuevos (re-medición independiente con denominador de statements); total ≈85.1% de 2.617 statements de desarrollo nuevo. Media de porcentajes por función NO usada como prueba; denominador explícito.
- `-race`: **NOT_EXECUTED** — host sin gcc (`which gcc` vacío; `go test -race` ⇒ "go: -race requires cgo; enable cgo by setting CGO_ENABLED=1", receipt en `receipts/god/`). No se instaló infraestructura ni se alteraron hosts (sin autorización aplicable). Queda residual para GO-S04 en host compatible autorizado.

## CAPACITY_LIMITS

- Medido (receipt W5 + re-lectura GOD): anillo 1×N con rotación por pase — N=100 ⇒ 101 adquisiciones, ~17.2 s wall, ~634 MB RSS pico, artifact 15.1 MB lineal, cancel-drain limpio (goroutines 2→2). **101 adquisiciones NO son 100 asociaciones simultáneas** — el propio receipt del autor lo declara; este review lo confirma y lo eleva a límite del claim.
- No medido: K≥2 compartimentos simultáneos (composición), retención por compartimento retirado a K>1, throughput QUOTE/MixedMinute en composición (UNKNOWN ya declarado en S02).
- Veredicto: crecimiento reportado esperado/acotado para el anillo; sin prueba de fuga; riesgo de escala de composición sin caracterizar (F9).

## GO_S04_REPAIR_AND_COMPLETION_PACKAGE

Un solo shot, agrupado por owner/dependencia para no re-descubrir arquitectura. Orden recomendado: A→B en paralelo con C; D al cierre; E transversal.

- **Grupo A — superficie de bindings por asociación (resuelve F1+F2+F3).** Owner: `campaign_v2_contract.go` (nueva versión de CampaignV2Association con MM/Profile/RuleSet refs por asociación resueltos contra catálogos sellados) + admisión (`campaign_modes_v2.go validateV2/validateCampaignV2AssociationBinding`) + composición (`campaign_composition.go installCompositionUnit` ya resuelve per-binding) + rewire sellado (`compose_account.go`: `composePoolSealedAuthorities`/`NewSealedMoneyManagerCatalog`/`WireSealedMoneyManagers`/`SealedAccountPolicy` — owners existentes, sin modificar runtime) + `seedAllFunded` generalizado para N asociaciones. Permitir TGMM/RGMM: resolver el binding sellado por asociación en vez de rechazar; mantener TODAS las validaciones actuales como casos negativos (nada se elimina). Pruebas de cierre: (1) composición 2 asociaciones con TGMM y RGMM reales simultáneas vía costuras runtime; (2) dos perfiles TEST_ONLY realmente distintos + dos RuleSets; (3) FUNDED multi-asociación con denominadores separados; (4) las 7 negativas de la sonda GOD mutadas a sus positivos + nuevas negativas de consistencia (binding inexistente sigue fallando cerrado); (5) paridad monocuenta se mantiene byte-idéntica.
- **Grupo B — CloseSafety v2 (resuelve F4).** Owner: spec/admisión v2 + `checkpoint`/`closeRiskAllowed` en `campaign_modes_v2.go`. Aceptar la superficie legacy-shaped de calendario de cierre en request v2; tabla de cutoffs sobre request v2 (espejo de `TestCampaignV2Matrix_CloseSafetyCutoffTable`).
- **Grupo C — reversos/refunds (resuelve F5).** Owner: `campaign_accounts_v2.go` + `campaign_economic_report.go`. Transición de reverso con identidad propia tras crédito, efecto de caja único, primer crédito positivo preservado como hecho histórico, refund con cohorte bruta conservada; reconciliación de `finish()` extendida. Pruebas: reverso posterior, doble reverso rechazado por idempotencia, refund/restart sin doble cargo.
- **Grupo D — evidencia y honestidad de matriz (resuelve F6+F7).** Owner: `campaign_migrate.go` + tests. Decidir (manager) renombrar MIGRATED→LEGACY_PATH_PRESERVED o añadir evidencia conductual por identidad; cerrar coverage de ramas fail-closed de los archivos <95%; `-race` en host compatible autorizado; capacidad K≥2 (F9).
- **Grupo E — transversal.** Corpus GOD como regresión permanente (sonda + suites + sandbox no-Python sobre FINAL_SHA); ledger-only para propósito físico en puertas legacy si el Owner adjudica F8; nada de esto re-abre D01/D02/D05 ni habilita corridas económicas históricas.

## NOT_EXECUTED / UNKNOWN

- NOT_EXECUTED: `-race` (sin gcc); cadena física `lab prepare`→`lab run` sin Python (fuentes NT de producción ausentes en host — EXTERNAL_DEPENDENCY, no gap de código); revisión adversarial con modelo independiente (cuota del host); re-ejecución de históricos (prohibida sin D01/D02/D05/budget Owner); validación de reglas comerciales reales de props (TEST_ONLY únicamente).
- UNKNOWN: comportamiento QUOTE/MixedMinute de composición sin E2E (heredado de S02); `prepareFixtureScope` multi-compartimento; régimen canario/WINDOW_REGISTRY del guard vs contrato Clutifx (decisión W4 documentada; no redefinido aquí); consumo Pro/pool del host.
- Consumo de presupuesto del review: 1 sesión GOD + 0 workers efectivos (3 despachos muertos por cuota ~2 s c/u); suites root+cmd ~14 min (candidato) + baseline propio en `w-base`; sin compras, sin trading, sin datos históricos.

## SUBAGENT_RECEIPTS

| Despacho | Modelo efectivo | Resultado |
|---|---|---|
| Front 1 (completitud/migración) | clf-flash GLM-5.3-Flash | FALLO ~2 s: `exceed quota limit` — sin trabajo |
| Front 2 (composición/seguridad) | clf-flash GLM-5.3-Flash | FALLO ~2 s: `exceed quota limit` — sin trabajo |
| Front 3 (economía/causalidad, reintento) | clf-flash GLM-5.3-Flash | FALLO ~2 s: `exceed quota limit` — sin trabajo |
| Ejecución efectiva | GOD directo (GLM-5.3-Flash, sesión `zcode` local) | Todo el review: verificación baseline, lectura de source, sonda propia, suites, matriz, cobertura, Go-only, capacidad, síntesis |

Ningún resultado de subagente fue inventado ni presupuestado; la sección INDEPENDENCE_REAL declara la consecuencia.

## AGENTS_OS_PATHS_SHA

Vault `main/` NO es git en este host (create-only + sincronización por el repo de publicación `agents-os-master-20261024`). Este retorno: `10-projects/Echo Futures/artifacts/backtester/EF-CAMPAIGN-MODES-GO-S03-RETURN.md` (nuevo, create-only; no reemplaza el retorno S02). Delta del planner: `10-projects/Echo Futures/agentes/Echo Futures — Optimización de Campañas.md` (actualización por delta de CURRENT_TASK_STATE + Bitácora). Run-register: `80-agents/journal/agent-runs/2026-10-29-zcode-glm-5.3-flash-echo-c06-go-s03.md` (journal privado, registro local; sin fingir publicación). Corte documental consumido por este review: el vigente al despacho (C06 design/planner/I0-LOCAL/GO-S02-RETURN leídos del vault vivo).

## PRO_CHAT_POOL_DELTA

UNKNOWN (sin observabilidad del pool desde esta superficie; consumo GLM-5.3-Flash confirmado por identidad de modelo, volumen no observable).

## Base de la clasificación de regresión (re-ejecución baseline propia)

Resultado de la suite completa sobre `w-base` (`2baf319d`, checkout propio): ver línea añadida al cierre — `receipts/f4/s03-suites-baseline.log`.

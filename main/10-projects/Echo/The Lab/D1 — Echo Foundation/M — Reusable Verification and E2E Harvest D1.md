---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[I — Independent Verification D1 (Shot 2)]]"
  - "[[K — Final Correction and Gate D1 (Shot 3)]]"
  - "[[L — Manager Final Acceptance D1]]"
  - "[[A — Technical SPEC D1]]"
aliases:
  - D1 reusable verification and E2E harvest
tags:
  - kind/doc
  - area/echo
  - the-lab
  - d1
created: "2026-09-23"
updated: "2026-09-23"
---

# M — Reusable Verification and E2E Harvest D1

## Propósito

Evidencia del mandato harvest 2026-09-23: recuperar el valor reusable de la verificación independiente Shot 2 (`d1-shot2-verify@6fafe683`), compararlo contra el HEAD certificado `64b616ff`, eliminar duplicación, retener invariantes fuertes como regresiones permanentes cerca de su owner y crear la suite E2E por SPEC. Ninguna afirmación sin ejecución detrás.

## Veredicto

**D1_E2E_HARVEST_PASS** (2026-09-23). Los 30 tests + helpers de Shot 2 inventariados y dispositionados al 100%; ninguna cobertura fuerte perdida; cero cambios semánticos productivos (diff solo tests/harness: 7 archivos, +1672/−0); suites verdes salvo preexistencias certificadas.

## Base y ejecución

- Repositorio `xKoRx/echo`; branch nueva `feature/d1-e2e-harvest` derivada de `feature/d1-echo-foundation-final` @ `64b616fff9ac2c76de6260a42c73ec4c363d6c54` (worktree `/home/kor/aranea/work/d1-e2e-harvest-20260923/echo`).
- Sin reconciliación con master necesaria: `3596fc48` (master local) es ancestro de `64b616ff`, y la línea bridge `c99aee06` diverge en `5dd998f1` siendo funcionalmente independiente (decisión del mandato). Todo compila y pasa contra `64b616ff` puro.
- Commits: `f66178de` (regresiones permanentes harvest) → `94f864a6` (suite E2E por SPEC) → `22b26716` (fix de geometría en fixture). HEAD final `22b26716`; worktree limpio; sin merge a master; sin push.
- PG desechable real 17.11 por corrida (binarios zonky `/tmp/echo-e08-pg`, `LD_LIBRARY_PATH` a `../libs`), puerto libre sondeado, migraciones 000+001..063+064 vía el harness canónico `v3/sdk/postgres/tests/d1_foundation/run.sh`. Go 1.27.1. Sin PROD/DEV compartida/ETCD/Kafka.

## Inventario Shot 2

El delta `e35d4347..6fafe683` contiene exactamente 3 archivos de test (+2317/−0, 1 commit): `v3/sdk/contracts/d1_shot2_verify_test.go` (10 tests + receta independiente), `v3/sdk/postgres/d1_shot2_verify_test.go` (14 tests + harness de PG y builders), `v3/gateway/internal/d1_shot2_http_verify_test.go` (6 tests + httptest env). Total: 30 funciones de test y 3 grupos de helpers.

## Matriz de disposition

Estados: `ALREADY_PROMOTED` (promovido por Shot 3), `COVERED_EQUIVALENT` (equivalencia demostrada, no se duplica), `PERMANENT_REGRESSION` (retenido en el paquete owner), `E2E_PROMOTED` (promovido a la suite por SPEC), `HARNESS_TOOLKIT_PROMOTED` (test-support reusable), `DISPOSABLE_WITH_REASON`.

### Contracts — `d1_shot2_verify_test.go`

| Shot2 artifact | Invariante | Cobertura existente | Disposition | Path permanente | Razón |
|---|---|---|---|---|---|
| TestShot2IndependentDigestRecipe (+shot2HashTagged) | receta record/dataset/history digest verificada SIN el SDK | TestHistoryRecordDigestDeterministic usa el SDK (tautológico) | PERMANENT_REGRESSION | contracts/strategy_history_harvest_regression_test.go::TestD1DigestRecipeIndependentVerification | anti-tautología única; absorbe namespace∈digest (de DigestSensitivity) e identidad-smuggled-inerte (de WireDecodePolicy) |
| TestShot2DigestInputOrderIndependence | dataset digest independiente del orden | TestHistoryDatasetDigestOrderIndependent | COVERED_EQUIVALENT | contracts/strategy_history_test.go | misma invariante con fuerza igual; history digest deriva del dataset digest |
| TestShot2DigestSensitivity | digest sensible a A/B/instrumento/contenido/timezone; convergencia de offsets | TestHistoryDigestChangesWithMaterialChange + TestHistoryUnsupportedContractVersionAndTimezone | COVERED_EQUIVALENT | contracts/strategy_history_test.go | todos los ejes cubiertos; delta namespace absorbido en la regresión de receta independiente |
| TestShot2DecimalCanonicalizationAdversarial | 24 formas no canónicas rechazadas; única forma por valor | TestHistoryDecimalWireFailsNoFloatPath sólo cubre number-token | PERMANENT_REGRESSION | contracts/strategy_history_harvest_regression_test.go::TestD1DecimalCanonicalizationAdversarial | estrictamente más fuerte que la permanente |
| TestShot2Numeric3818Limits | 20+18 dígitos verbatim; 21 enteros/19 fraccionarios rechazados a nivel contrato | sin equivalente permanente | PERMANENT_REGRESSION | contracts/strategy_history_harvest_regression_test.go::TestD1Numeric3818ContractLimits | límite contractual único que complementa el límite real de PG |
| TestShot2PeriodBorders | SQX<A; MT5 [A,B); B<=A; closed==opened; IANA | casos 17-20 + IncoherentBounds + ClosedBeforeOpen + IANA | COVERED_EQUIVALENT | contracts/strategy_history_test.go | todas las fronteras cubiertas con códigos exactos |
| TestShot2EconomicsExact | identidad económica exacta big.Rat; artefactos float rechazados | TestHistoryEconomicsIdentity | COVERED_EQUIVALENT | contracts/strategy_history_test.go | misma aritmética exacta; forma -0 cubierta por la tabla decimal retenida |
| TestShot2SubMicrosecondInstantNormalization | instante ns aceptado; nota receta-ns vs PG-µs | fidelidad sub-segundo en regresión F-S2-02 y E2E-01/06 | DISPOSABLE_WITH_REASON | — | sonda informativa sin aserción durable; el conocimiento queda registrado en K (riesgo conocido) |
| TestShot2DuplicatesAndDeclarations | duplicados intra-dataset; mismo id cross-dataset; count/digest mismatch; contract version | casos 14-16 + 23-24 + v2/IANA | COVERED_EQUIVALENT | contracts/strategy_history_test.go | mismos invariantes con códigos exactos |
| TestShot2WireDecodePolicy | dup keys, null tipado, number token, dataset ausente, count fraccional | wire profile (TestValidate_RejectsDuplicateKeysAndTypedNull) + TestHistoryDecodeTypeErrors/RequiredTopLevel | COVERED_EQUIVALENT | contracts/wire/validate_test.go + contracts/strategy_history_test.go | delta smuggling de identidad absorbido en la regresión de receta independiente |

### PostgreSQL — `d1_shot2_verify_test.go`

| Shot2 artifact | Invariante | Cobertura existente | Disposition | Path permanente | Razón |
|---|---|---|---|---|---|
| TestShot2ConcurrentAvsB (40 iter) | replacement concurrente converge a UN dataset completo sin mezcla | TestD1ConcurrentReplacementConverges + 60 replacements de la regresión F-S2-01 | COVERED_EQUIVALENT | postgres/strategy_history_integration_test.go + strategy_history_concurrent_read_regression_test.go | misma invariante; la repetición es stress, no invariante nuevo |
| TestShot2ConcurrentReplayAvsReplaceB (30+20) | replay vs replace concurrentes; doble replay idempotente | ídem + UNCHANGED sin churn (caso 38 + lifecycle HTTP) | COVERED_EQUIVALENT | ídem | ídem |
| TestShot2ConcurrentABC (25) | concurrencia 3-way, sin mezcla | ídem | COVERED_EQUIVALENT | ídem | cardinalidad es variante del mismo invariante de serialización |
| TestShot2ConcurrentReadDuringReplace | GET continuo sin torn head/ops | promovido por Shot 3 | ALREADY_PROMOTED | postgres/strategy_history_concurrent_read_regression_test.go::TestD1GetHistoryConsistentReadSnapshot | versión permanente más fuerte (60 replacements, coherencia exacta head↔dataset, REFERENCE en cada lectura) |
| TestShot2RollbackInjectedAfterDelete | fault seam post-delete ⇒ rollback completo | TestD1ReplayReplacementReferenceRollback caso 41 (mismo seam + head digest) | COVERED_EQUIVALENT | postgres/strategy_history_integration_test.go | cobertura idéntica o mayor |
| TestShot2RollbackRealBackendCancel | fallo REAL de backend (pg_cancel_backend) a mitad de transacción | sin equivalente (solo seam y sqlmock) | PERMANENT_REGRESSION | postgres/strategy_history_harvest_regression_test.go::TestD1ReplaceHistoryRealBackendCancelRollsBack | único fallo físico de backend; verifica head+counts+REFERENCE por lectura directa |
| TestShot2RollbackContextDeadline | deadline sobre advisory lock ⇒ UNAVAILABLE (503 retryable) + estado intacto | error mapping sqlmock sin path real de lock | PERMANENT_REGRESSION | ídem (fase deadline del mismo test) | clasificación retryable demostrada sobre lock real |
| TestShot2EmptyDatasets | datasets vacíos válidos; replace a cero ⇒ READY; replay UNCHANGED; digest vacío definido | parcial (empty training en WithLiveStart; nada de both-empty) | PERMANENT_REGRESSION | postgres/strategy_history_harvest_regression_test.go::TestD1EmptyDatasetReplacementSemantics | semántica de vacíos única no cubierta antes |
| TestShot2SymbolAuthority | canónico ok; alias/inactivo/inexistente ⇒ UNKNOWN_INSTRUMENT; sin mutación de authority | TestD1HistoryCanonicalInstrumentAuthority (canónico/desconocido/sin-mutación) | PERMANENT_REGRESSION | postgres/strategy_history_harvest_regression_test.go::TestD1HistoryInstrumentResolverCanonicalOnly | deltas únicos: alias rechazado AUN con mapping activo, y mapping inactivo |
| TestShot2NamespaceIsolation | tenancy: mismo ref en 2 namespaces; GET cruzado 404; replacement sin cruce; digests distintos | sin cobertura permanente a nivel servicio | E2E_PROMOTED | e2e/specs/THE-LAB-D1-ECHO-FOUNDATION/d1_scenarios_test.go::TestE2ED107NamespaceIsolation | invariante cross-component (identidad→servicio→PG) y escenario E2E-07 del mandato |
| TestShot2ReferenceImmutability | REFERENCE byte a byte en put/replay/replace/empty/failed/concurrent | counts-level (caso 40) + visible por lectura (F-S2-01) | E2E_PROMOTED | d1_scenarios_test.go::TestE2ED106ReferencePreservedAcrossLifecycle | escenario E2E-06 del mandato: preservación a través de todo el ciclo de vida |
| TestShot2BulkInsertBoundedStatements | INSERT acotado por chunks (1/250/251/700/2000) | TestD1BulkInsertBoundedStatements (700→3 + constante) | ALREADY_PROMOTED | postgres/strategy_history_integration_test.go | caso permanente completo; los otros boundaries son variantes de la fórmula ceil |
| TestShot2ReadbackExactnessAndNumericDBLimit | readback verbatim de 18 fraccionarios; 21 enteros rechazados por PG directo | readback numérico-exacto (caso 34) con decimales cortos | PERMANENT_REGRESSION | postgres/strategy_history_harvest_regression_test.go::TestD1LongDecimalReadbackAndNumericDBLimit | verbatim de precisión completa + límite real de PG + bulk multi-chunk funcional (300 ops reales) |
| TestShot2LargeDatasetEndToEnd | 700/5000 ops funcionales + tiempos informativos | mecanismo por mock (#anterior) + funcional a escala chica | COVERED_EQUIVALENT | postgres/strategy_history_harvest_regression_test.go (caso bulk 300 con PG real) | la parte funcional multi-chunk real quedó absorbida en la regresión; el timing no aserta thresholds |

### Gateway — `d1_shot2_http_verify_test.go`

| Shot2 artifact | Invariante | Cobertura existente | Disposition | Path permanente | Razón |
|---|---|---|---|---|---|
| TestShot2HTTPAuth | 401 sin/incorrecto token; 503 fail-closed sin token configurado (PUT/GET) | TestD1HTTPRejections (401) + TestD1HTTPMisconfigured503 | COVERED_EQUIVALENT | gateway/internal/strategy_history_handler_test.go | mismos invariantes; la variante GET-503 es path de config equivalente |
| TestShot2HTTPNamespaceSmuggling | identidad del body ignorada; historia queda en namespace server-side | sin equivalente permanente | PERMANENT_REGRESSION | gateway/internal/strategy_history_namespace_regression_test.go::TestD1HTTPHistoryBodyIdentityFieldsIgnored | invariante de boundary única (identidad server-side) |
| TestShot2HTTPWireAttacks (16 ataques) | matriz de status exactos (400/404/413/422) | TestD1HTTPRejections + wire profile + contratos + límites contractuales retenidos | COVERED_EQUIVALENT | gateway/internal/strategy_history_handler_test.go + suites contracts | todos los mappings de status cubiertos permanentemente; dup-keys/UTF-8 en el wire profile |
| TestShot2HTTPReadSurface | order_by inválido 400; source/rangos/limit; determinismo con empates; REFERENCE visible | TestD1HTTPReadSurfaceParams | COVERED_EQUIVALENT | gateway/internal/strategy_history_handler_test.go | REFERENCE-visible absorbida por E2E-06 |
| TestShot2HTTPResultLifecycle | 201 CREATED → 200 UNCHANGED → 200 REPLACED | TestD1HTTPHistoryLifecycle (más fuerte: match con estado PG + cero side effects) | ALREADY_PROMOTED | gateway/internal/strategy_history_handler_test.go | cobertura permanente igual o mayor |
| TestShot2HTTPGetSubSecondProjection | sonda de proyección sub-segundo del GET | promovida por Shot 3 | ALREADY_PROMOTED | gateway/internal/strategy_history_timestamp_regression_test.go::TestD1HTTPHistoryTimestampFidelity | versión permanente con round-trip exacto y formato limpio |

### Helpers

| Shot2 artifact | Disposition | Path permanente | Razón |
|---|---|---|---|
| shot2DB + seeds idempotentes + limpieza dirigida | HARNESS_TOOLKIT_PROMOTED | e2e/specs/THE-LAB-D1-ECHO-FOUNDATION/e2e_suite_test.go (e2eDB/e2eSeedVersion/e2eSeedSymbol/e2eSeedReference/e2eReadReferenceRows) | patrón re-materializado como test-support del módulo E2E; el paquete postgres conserva su propio harness (d1HistoryDB) |
| shot2RequestBody builders (productor conforme vía SDK) | HARNESS_TOOLKIT_PROMOTED | e2e_suite_test.go (e2eRequestBody/e2eRequestBodyOps/e2eTrainingOp) | builders reutilizables por todos los escenarios E2E |
| shot2HashTagged (receta independiente) | PERMANENT_REGRESSION | contracts/strategy_history_harvest_regression_test.go (hrvHashTagged) | parte integral de la regresión de receta independiente |

## E2E creados

Carpeta `v3/e2e/specs/THE-LAB-D1-ECHO-FOUNDATION/` (paquete `d1foundation`, primer adoptante de la convención por SPEC): `README.md` (manifest: autoridad, invariantes, ejecución, qué NO prueba, relación con regresiones externas), `run.sh` (PG desechable + rebuild 064 canónico + suite + cleanup), `e2e_suite_test.go` (helpers), `d1_scenarios_test.go`. Escenarios: E2E-01 ciclo completo PUT→validación→PG→GET · E2E-02 replay UNCHANGED sin churn · E2E-03 replacement atómico · E2E-04 rechazo atómico · E2E-05 rollback por fallo real (lock externo + deadline, sin seam) · E2E-06 REFERENCE byte a byte en 6 rutas · E2E-07 aislamiento de namespaces. E2E-08/E2E-09 del mandato NO se duplican: enlazan `TestD1GetHistoryConsistentReadSnapshot` y `TestD1HTTPHistoryTimestampFidelity`, estrictamente más fuertes.

## Regresiones permanentes retenidas

8 funciones nuevas: contracts 3 (`TestD1DigestRecipeIndependentVerification`, `TestD1DecimalCanonicalizationAdversarial`, `TestD1Numeric3818ContractLimits`), postgres 4 (`TestD1ReplaceHistoryRealBackendCancelRollsBack`, `TestD1EmptyDatasetReplacementSemantics`, `TestD1HistoryInstrumentResolverCanonicalOnly`, `TestD1LongDecimalReadbackAndNumericDBLimit`), gateway 1 (`TestD1HTTPHistoryBodyIdentityFieldsIgnored`). Regresiones existentes reutilizadas como autoridad: F-S2-01 y F-S2-02 (de Shot 3) más las suites integration/handler de Shot 1.

## Comandos y resultados

- `bash v3/e2e/specs/THE-LAB-D1-ECHO-FOUNDATION/run.sh` → harness 064 OK (probe BEGIN+064+ROLLBACK, apply estricto, idempotente, down+up, objetos verificados) + suite E2E **7/7 PASS** (1.18s).
- `cd v3/sdk/contracts && GOWORK=off go test ./...` → ok; filtro `TestHistory|TestD1` → **23 PASS / 0 FAIL** (20 permanentes + 3 harvest).
- `go test ./v3/sdk/postgres/ -count=1` → **143 PASS / 1 FAIL**; el único FAIL es `TestScratch_QueryDB` (preexistente certificada, modo idéntico: credencial DEV hardcodeada).
- `go test ./v3/gateway/internal/ -count=1` → **65 PASS / 0 FAIL** (incluye F-S2-02 y la regresión de smuggling).
- `go test -race`: contracts ok; postgres ok (solo el scratch preexistente); gateway ok — **sin DATA RACE**.
- `go test ./...` en `v3/e2e`: paquete specs ok (verde con PG, skip limpio sin PG); paquete raíz `v3/e2e` **FAIL preexistente** (TestOpenFlow/TestFullFlow/TestSymbolMapping del framework copy-flow V2) — mismo modo de fallo en master `3596fc48` y en el worktree; ajeno a D1 y no tocado.
- `go vet` y `gofmt -l` limpios en los 7 archivos del diff; builds `go build ./...` en gateway, lab-worker, sdk, core, bridge, toolkit, e2e → **7/7 OK**.

## Riesgos restantes

- Persisten los riesgos de K: 064 sin aplicar en bases reales, seeding owner de `symbol_mappings` antes de D2, defaults 64 MiB/60s a medir, credencial versionada en `scratch_query_test.go`.
- Nuevo: el paquete raíz `v3/e2e` arrastra ~14 tests rojos preexistentes del framework copy-flow V2; cualquier gate que corra `go test ./...` en ese módulo los pisa — la suite por SPEC es inmune (paquete separado). Higiene owner pendiente.
- Nuevo: la máquina acumula instancias postgres huérfanas en puertos 154xx (de sesiones anteriores); los harnesses deben sondear puerto libre antes de arrancar (run.sh de esta suite ya lo hace).

## Final verdict

D1_E2E_HARVEST_PASS: el valor reusable de Shot 2 quedó preservado al 100% — 8 regresiones permanentes nuevas junto a sus owners, 2 escenarios promovidos a la suite E2E por SPEC, 2 reproducers ya promovidos por Shot 3 enlazados, equivalencias demostradas para el resto sin duplicar cobertura — con la suite E2E `THE-LAB-D1-ECHO-FOUNDATION` ejecutable y verde contra el HEAD D1 certificado, cero cambios semánticos productivos y las dos únicas preexistencias (`TestScratch_QueryDB`, paquete raíz `v3/e2e`) certificadas como ajenas a D1.

## Fuentes

- [[I — Independent Verification D1 (Shot 2)]] · [[J — Manager Decision after Shot 2]] · [[K — Final Correction and Gate D1 (Shot 3)]] · [[L — Manager Final Acceptance D1]] · [[A — Technical SPEC D1]]
- Agent run atribuible: `80-agents/journal/agent-runs/2026-09-23-zcode-glm53-d1-e2e-harvest.md`
- Repo `xKoRx/echo`, branch `feature/d1-e2e-harvest`, HEAD `22b26716` (local, sin push; worktree registrado `/home/kor/aranea/work/d1-e2e-harvest-20260923/echo`)

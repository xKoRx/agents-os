# Echo — E-10 Manager Review M7: cierre de integridad T05 forward

Fecha: 2026-09-22. Rol: manager técnico. Repo `xKoRx/echo`, única branch `feature/e09-execution-copy-reconciliation-fidelity`. Baseline revisado `a504411237c5fa780d354504b996dfe639713d1c`; master verificado `5dd998f16aea7b2821f460188718d7a6d279829c`.

## Decisión

M6 source delta verificado: FF de cuatro commits desde `6c7c2531`, 32 archivos; sólo migración 065 cambiada; S0/go.mod sin delta según compare, master intacto. Reparación E-07 instrument/side y llamada real a CanonicalWriter presentes en source. Tests, PG 065 no desplegada y 121 failing sets idénticos son evidencias reportadas por el ejecutor, no re-ejecutadas por manager. **No aceptar cierre técnico definitivo T05; NO liberar T06.** Estado: `E07_ANALYTICAL_SOURCE_REPAIRED / T05_FORWARD_IMPLEMENTED_WITH_INTEGRITY_BLOCKERS / T05_NOT_CLOSED / T06_T10_NOT_AUTHORIZED / POLICY_RATIFICATION_UNACCREDITED / PHYSICAL_INTEGRATION_PENDING / FINAL_CLOSED_NO`.

## M7-R1 — Provenance contaminada y tipo de referencia

`v3/sdk/postgres/strategy_quality_forward.go::loadTradeEvidenceRefs` hace `SELECT trade_id, fact_digest FROM echo.raw_trade_events WHERE fact_kind IN ('OPEN','CLOSE_ASSERTION') AND trade_id = ANY($1)` sin filtrar `processing_status`, binding, version, ni comprobar consistencia con lifecycle. `v3/core/internal/tradefacts/ingress.go::ProcessTradeFact` conserva una fila raw `SKIPPED` tras contradicción de pins y agrega quarantine. Por tanto un CLOSE rechazado entra en `source_evidence_refs` del TradeSet aceptado. Además E-07 distingue explícitamente `fact_ref` (referencia del hecho) de `fact_digest` (sello del contenido); no intercambiarlos sin contrato. Corregir lectura para usar SOLO hechos PROCESSED realmente atribuibles al trade/binding/version, con identidad/fact_ref auténticos y comprobados; decidir y documentar autoridad exacta de ref sin parsear raw_payload opaco del productor. Test físico: OPEN procesado + CLOSE contradictorio SKIPPED + quarantine; el último jamás participa en operation refs/inputs/digests.

## M7-R2 — Allowlist (key,basis,formula) se degrada a key

`forwardMetricQuestion` deduplica `AllowedComparisons` exclusivamente por key y devuelve `RequestedKeys` con `MetricDefaults.RiskBasis` vacío. `CanonicalWriter.Write` pasa esas keys a `calculator.Compute`; `calculator.resolveBasis` exige `defaults.RiskBasis` para `return.total`/`return.expectancy`. Expectation válida `return.total|R_MONEY` pasa DQ pero el writer devuelve `ErrUnresolvableBasis`. Si la allowlist tiene más de una basis del mismo key, el writer A0 acepta sólo una base por key: no debe seleccionar ni ocultar la otra. Resolver desde selectors completos y comprobar antes de escribir que la pregunta E-05 representa exactamente la allowlist; setear defaults tipados solamente donde son únicos/contractuales; si no representable, fail-closed PRE-write con error tipado y escalar extensión E-05 por separado. Tests R_MONEY, R_PIPS, dos bases de la misma key, formula_id explícito y no efectos ante fracaso.

## M7-R3 — Pérdida de precisión NUMERIC→float64→Decimal S0

`loadForwardTrades` escanea precios, economía e initial risk PG `numeric` en `sql.NullFloat64`; `deriveForwardOperation` usa `strconv.FormatFloat`. El paso binario NO preserva decimales PG exactos y puede modificar contenido sellado/métricas de dinero. Leer decimales como texto/decimal exacto nullable validado con contratos S0; no pasar por float64 ni redondear silenciosamente. Tests reales con `numeric(18,4)` alto, comisiones fraccionales y precio/riesgo que demuestren byte-equivalencia canónica desde PG al NDJSON/readback.

## M7-R4 — Snapshot inconsistente entre DQ y forward

`ForwardPipeline.Run` invoca `GetByVersion`, `CoverageAssembler.Assemble` (3 SELECT sobre DBTX/pool), `ForwardEvidenceLoader.Load` (BeginTx(ctx,nil), aislamiento PG por defecto READ COMMITTED y queries múltiples) y baseline queries por separado. NO es un snapshot consistente. Cambios de lifecycle/coverage durante la corrida pueden combinar inputs de generaciones distintas y sellar write-once un resultado no reproducible. Corregir con un único snapshot read-only REPEATABLE READ para todas las lecturas que participan en el mismo input DQ/TradeSet, sin volver a anidar transacciones; sellar refs/as_of del snapshot y escribir sólo después de validar. Test de interleaving controlado y comparaciones de input digest vs refs aceptados.

## M7-R5 — ArtifactRef no tiene locator por set

`SealForwardTradeSet` publica `Payload{StoreID:'echo-pg-e10-forward',Bucket:'canonical_trade_sets',Key:'payload-ndjson',Sha256:...}` con la misma clave para todos los sets; el payload real se guarda en `echo.canonical_trade_sets` bajo `ref`, y no hay en ese path una ruta de resolución real de `payload-ndjson` a la fila. S0 valida la forma pero no acredita que el locator apunte a los bytes. Construir un locator estable, único y realmente resoluble por ref/digest vía storage 063, sin cambiar S0; probar recuperación exacta y `VerifyArtifactBytes` de DOS TradeSets distintos. Si no existe contrato de locator autorizado, STOP específico al manager; jamás afirmar ArtifactRef real sólo por Validate.

## Decisión de sample_policy_ref

**No ratificado** `sample_policy_ref = expectation_ref`. `ScopeV1.TimeWindowV1.sample_policy_ref` identifica la política de selección de membresía, mientras StrategyExpectation pinnea baseline, comparaciones y `minimum_observation_policy_ref` — no demuestra por sí sola reglas de muestreo ni ratificación owner. No sustituir con minimum_observation_policy_ref automáticamente. Registrar contrato concreto de qué política determina la membresía de la ventana efectiva y su ref durable; proponer alternativa documentada y prueba de readback, sin inventar ratificación ni política de clase C. Puede mantenerse provisional para fixture T05 sólo si explícitamente NO se certifica como política real; ningún uso autoritativo para T06 hasta resolverlo.

## Mandato NEXT NORMAL — M7 acotado

Pre-flight SHA exacto, worktree aislado, Environment Contract. Corregir SOLO M7-R1..R5 en tests/forward/adapter canónico, sin reabrir E-07 A/B, sin modificar 065 ni S0, 066–069, master, DEV/PROD, Forge, T06–T10 o activación. Antes de cada fix: rojo conductual reproducible y test físico/contractual; después verde. Commits atómicos por defecto, docs de E10 VERIFICATION, push FF/readback, Agents-OS change_log/agent_run/session-close. Si R2 requiere cambiar interface E-05 o R5 nueva autoridad de locator, STOP preciso. Si sample policy no se puede certificar, no declarar T05 FINAL PASS. Repetir focused domain, E-07, E-10 PG arnés, E-08/E-09 propios si cruzados, build/vet/gofmt/-race, failing-set por nombre apples-to-apples. El manager revisa el delta después; T06 no autorizado.

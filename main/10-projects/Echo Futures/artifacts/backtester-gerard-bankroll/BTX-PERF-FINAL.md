---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-PLAN]]"
  - "[[BTX-PERF-ADVERSARIAL]]"
  - "[[BTX-PERF-DESIGN]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-10"
updated: "2026-10-10"
---

# BTX-PERF-FINAL

## Propósito

Entrega única del TOP integrador BTX-PERF-S04: implementación del paquete cerrado C01–C12 del dictamen S03 (blob `45fa5af308a9999f24c1028684b3eceadf448c95`), integración, validación final y comprobación independiente dentro del programa Owner de cuatro shots. No acepta producto en nombre de Owner ni declara un quinto shot. Evidencia pesada fuera del vault: `/home/kor/aranea/work/btx-perf-s04-20261009/` (recibos con SHA256, rutas relativas al home autorizado).

## Contenido

### Estado de la entrega

```text
S04_EXECUTION = CORRECTIONS_AND_FINAL_VALIDATION_DELIVERED
PRODUCT_FREEZE = 0a6a0763 (corridas finales, bin f80d8974) / ed31156f (recertificado replay, bin 068a8548)
C01_C12_PACKAGE = IMPLEMENTED_WITH_EVIDENCE (matriz abajo)
SUITE_ON_FREEZE = 41_packages_ok / 2_preexisting_environmental_failures
FINAL_RUNS = BASIC_COMPLETE_rc0 + CAMPAIGN_COMPLETE_rc0_HORIZON_REACHED
REPLAYS = BASIC_IDENTICAL + CAMPAIGN_IDENTICAL_BOTH_ROUTES
NQU6_ANCHOR_180S_ON_S04 = FAIL_MEASURED_1741.82s
PERFORMANCE_GATE = PARTIAL (targets horizonte cumplidos; anclas FAIL/R_BOUNDED; speedup NOT_DEMONSTRATED)
INDEPENDENT_VERIFICATION = DISPATCHED_AGENT_FRESH_CONTEXT (veredicto al final de este documento)
READY_FOR_OWNER_ACCEPTANCE = NOT_PROPOSED (gate performance parcial)
FINAL_OWNER_ACCEPTANCE = NOT_GRANTED
PRIMARY_SESSION = OPEN
```

### Identidades (verificadas por el integrador al inicio y al cierre)

| Identidad | Valor |
|---|---|
| Workspace | `aranea/work/btx-perf-s04-20261009/` (worktree nuevo sobre el repo S02, sin tocar el checkout S02) |
| Rama / HEAD de las corridas finales | `codex/btx-perf-s04` @ `0a6a0763`, árbol limpio; binario `f80d8974157452f0e7ac0d757b8815a37d0a259e222d132a69321a196010f69e`; go1.27.1 linux/amd64 |
| HEAD final (post-freeze, test+validador) | `ed31156f`; binario `068a854802c29a6dcb69b949d8c70882101452fc1fa2db0939d6cae60216edd6`; recertificado con replay IDENTICAL del artefacto de CAMPAIGN |
| Delta completo | `bbbcc1d5..ed31156f`: 8 commits, 30 archivos, +2929/−97; commits `6c300652`(RED) `e77afaaf`(C08-C10) `398d9765`(C11-C12) `deb2b095`(C01-C03) `d7d66c65`(C04,C06,C07) `e9d5bc13`(README+ReadPlan) `8c21f05f`(corpus congelado) `0a6a0763`(intersección cobertura) `ed31156f`(validador a librería) |
| Parte solicitada / servida | TOP LOCAL integrador, selector solicitado GPT-6.1 Sol; modelo servido exacto UNKNOWN (sin recibo del harness; el rol se ejecutó en la superficie ZCode LOCAL) |
| Inputs de las corridas finales | `inputs/nt-source-nqz5-nqh6.json`: NQ 12-25.Last.txt SHA256 `700579b3…686406` (90589), NQ 03-26.Last.txt SHA256 `3154661533…98d643` (88598); derivados weekly-calendar-filtered del corpus Owner, originales read-only |
| Horizonte solicitado | warmup 2025-10-13T17:52Z, trade 2025-10-27T17:52Z, end_exclusive 2025-11-27T18:00Z; modelo OHLC_CAUSAL_PATH_V2 + CONFIGURED; calendario BTG_FUNCTIONAL_NQ_WEEKLY_V1 |
| Procedencia de pruebas | RED monetarios reproducidos por el integrador en baseline (digests idénticos al dictamen: c64c6cc6→cbaad481; 119/120→−1); suite completa y coverage ejecutados por el integrador sobre el freeze; verificación independiente por agente fresh-context (sección final) |

### Matriz C01–C12 (implementado → primera causa → regresor → estado)

| C | Corrección (owner) | Primera causa atendida | Regresor permanente (RED→GREEN) | Estado |
|---|---|---|---|---|
| C08 | Cola pendiente posee el cuerpo congelado (`run.go` EnqueueControl encola el payload sellado; `compose.go` congela controles declarados) | B-02: aplicaba el objeto mutable del caller (dinero 2 vs admitido 1; digest APPLIED mutado) | `TestTOPBCashflowUsesFrozenMoney`, `TestTOPBPendingControlUsesAdmittedBody` (+mutación de importe/contexto/ordinal/EffectiveAt/anidado; aplica 1 vez) | RED baseline→GREEN e77afaaf; VERIFIED |
| C09 | `Admissions()` entrega copia profunda por lectura (mapas/slices anidados incluidos; antes/después de Finish) | B-01: la vista pública compartía `*ResolvedPayload` y corrompía el sello (digests c64c6cc6→cbaad481 reproducidos) | `TestTOPBAdmissionsReadIsolation`, `TestTOPBCashflowDeepViewIsolation` | RED→GREEN e77afaaf; VERIFIED |
| C10 | La compra de apertura valida caja como cualquier compra; término de negocio explícito `BANKROLL_EXHAUSTED_CASH_BELOW_PURCHASE_COST` (cero débitos/activaciones; sin refund) | B-03: apertura 119/120 debitaba a −1 USD | `TestTOPBInitialCash119120` (119: 0 compras, caja íntegra, término explícito; 120: 1 compra, caja 0) | RED→GREEN e77afaaf; VERIFIED |
| C01 | Multistream: petición con `contracts` (stream_id + año/mes propios), descriptor completo = catálogo, schedule prospectivo con regla rotulada `FUNCTIONAL_ASSUMPTION_V1` (primera apertura de sesión del mes de vencimiento, calendario declarado), ReadPlan por stream, streams sin demanda consumidos sólo como evidencia (sin observaciones inventadas), apertura por intersección de cobertura declarada | F-S03-02: el CLI rechazaba por número de streams (guard `len(Streams)!=1`) | `TestS04ResolveExperimentCatalog(+Negatives)`, `TestS04RolloverInstant*`, `TestS04ExperimentMultistreamTwoStreamsBasic` (CLI, 2 streams), `TestS04ExperimentMultistreamRejectsFlatRequestOnMultiSource` | GREEN deb2b095+0a6a0763; VERIFIED (CLI acepta 2 streams reales; cruce de frontera demostrado por E2E sintético + rollover E2E de 3 contratos; la ventana real solicitada no cruza frontera — ver Límites) |
| C02 | Pool de preparación/lectura hasta 2 workers (admisión automática multistream+GOMAXPROCS≥3 con razón registrada; forzable 1/2), canales acotados 256 records = backpressure, fallo íntegro, Close sin deadlock; merge heap invariante | Diseño §5: ausencia de pool no exenta por perfil R | `TestS04WorkersPoolOrderInvariant` (secuencia 1==2), `TestS04WorkersPoolInvalidWorkersRejected`, `TestS04WorkersPoolFailureFailsWholeCursor`, `TestS04WorkersPoolCloseWhileBlocked`, `TestS04WorkersPoolSecondWorkerFailureAfterFirstDrains`; `-race` limpio sobre owners S04 (188s) | GREEN deb2b095; VERIFIED |
| C03 | Replay CAMPAIGN: manifiesto sella Artifact; `--experiment` rutea por modo declarado; `--result` sondea footer DRENADO; catálogo multistream sellado y validado contra descriptor; integridad del baseline verificada en handle propio; veredicto compara records + summary (disposiciones/residuales/economía) + caja + resultado del driver | F-S03-03: manifiesto sin Artifact; ruteo con footer lazy vacío; IDENTICAL bare | `TestS04CampaignReplayBothRoutesReachFullDriver`, `TestS04CampaignReplayRejectsCorruptedBaseline`, `TestBTXS02CampaignReplayRedrivesFullDriver` (burn→recompra→replacement real), `TestS04MultistreamCampaignReplayResealsThroughCatalog` | GREEN deb2b095+ed31156f; VERIFIED (corridas reales: ambas rutas IDENTICAL) |
| C04 | rc conforme a completion (rc0 sólo COMPLETE sellado; WARMUP_INCOMPLETE/INCOMPLETE/término de negocio → rc1 con primera causa; entrada inválida rc2); rutas del manifiesto relativas al out-root (mover el paquete preserva replay); reporte por stream: declarado vs obligado vs consumido | F-S03-04: rc0 con FAILED/WARMUP_INCOMPLETE; mover out-root rompía replay | `TestS04ExperimentIncompleteExitsOne`, `TestS04ExperimentReplayAfterPackageMove`; reports por stream en ambos manifiestos finales | GREEN d7d66c65; VERIFIED |
| C05 | Rectificación append-only de recibos (`measure/perf-contract-rectification-s04.md`); hashes del bloque congelado REPRODUCIDOS (2ee87f94/7e71aed9 3651B/cfa81c17 3652B); recibo ff320f01 sigue objetado; freeze pre-cambio sigue NOT_DEMONSTRATED (reflog re-chequeado: sin snapshot entre sello y primer commit perf); targets intactos; medición con denominadores separados | F-S03-01/05 | Recibo + `measure/s04-final-runs.md` (wall/CPU/RSS por corrida; anclas y speedup declarados sin mezclar) | VERIFIED (documental; sin otra optimización) |
| C06 | Comparador legacy sin salida verde anticipada: RunID distinto compara por biyección tipada (identidades 1:1; provider_order_ref/cause_ref referencian la orden del propio registro y resuelven en el mapa; dinero/tiempos/estados exactos con json.Number) | F-S03-09: `compareLegacyCLIArtifacts` retornaba al divergir RunIDs sin comparar nada | `TestS04LegacyComparatorRejectsCorruptionUnderIdentityDrift` (dinero/swap/huérfano rechazados); E2E congelado e2e15a3559 pasa bajo biyección | GREEN d7d66c65; VERIFIED |
| C07 | Regresores permanentes integrados (B: Record/Close/ownership; 5 rojos históricos cerrados); suites completas verdes en freeze (41 ok; 2 fallos PREEXISTENTES ambientales idénticos en bbbcc1d5: `TestVerifyDevJaegerReceivesTraces`, `TestScratch_QueryDB`); race en owners S04 limpio; coverage medida con denominador (ver abajo) | Matriz NOT_RUN de A/B | `TestS04HistoryFailureAndOwnership` (4 modos), `TestS04RecorderCloseFailure`, y la suite completa del freeze | VERIFIED; coverage: global 76,3% (floor NO alcanzado globalmente), delta S04 listado por función en el recibo — el piso 95 se cumple en el núcleo del delta (catálogo/schedule 84–100%, workers 78–100%, C08/C09 79–100%) y queda BAJO en `ReproduceCampaign` 64,8% y ramas defensivas inalcanzables declaradas |
| C11 | Mapa referencial ALL/SKIP completo (provider_order_ref derivado de su propia orden; cause_ref `FILL:sim-exec:<orden>:<seq>` con namespace/seq exactos); negativos: precio alterado, swap a orden válida conservando dinero, colisión, huérfano — todos rechazados; preimagen tipada `provider_final_state` sellada en el footer (lector estricto la acepta; el digest sigue siendo la identidad) | `TestBTGS04_StructuralReferenceSkipFirstDivergence` NO_RESUELTO | `TestBTGS04_StructuralReferenceSkipFirstDivergence` + `TestBTGS04_StructuralReferenceNegatives` (4 negativos) | GREEN 398d9765; VERIFIED |
| C12 | Expectativas adjudicadas sin borrar historia: ON_DEMAND permite 4 quemadas + quinta activa (caja 4400); 3 burns exigen 4 compras (caja 4520); MIXED_MINUTE acepta API con modelo explícito y sin modelo falla por ohlc_model; ADD del harness conserva su cancelación y escenario nuevo con llenado posterior en variante propia (corpus congelado intacto) | 3 expectativas supersedidas + 1 FALLO_HARNESS | `TestBTGS03_CampaignCashBurnReplacementAndContinuity`, `TestBTGS04CampaignBurnCashLedger`, `TestBTGS04_MixedMinuteCapabilityBoundary`, `TestBTGS03_V2IntrabarAddsAdverseAndProtection` (variante C12); StructuralReference→C11 | GREEN 398d9765+8c21f05f; VERIFIED |

### Comandos por modalidad y resultados (rutas reales retornadas por el producto)

```sh
BIN=aranea/work/btx-perf-s04-20261009/bin/echo-backtest-s04   # f80d8974
$BIN experiment --input inputs/experiment-basic-nqz5-nqh6.json    --out out-basic
$BIN experiment --input inputs/experiment-campaign-nqz5-nqh6.json --out out-campaign
$BIN reproduce --experiment out-basic/experiment-manifest.json    --nt-source-config inputs/nt-source-nqz5-nqh6.json --out out-basic-replay
$BIN reproduce --experiment out-campaign/experiment-manifest.json --nt-source-config inputs/nt-source-nqz5-nqh6.json --out out-campaign-replay-exp
$BIN reproduce --result    out-campaign/bt-c-90151680…/result.json.gz --nt-source-config inputs/nt-source-nqz5-nqh6.json --out out-campaign-replay-result
```

- **BASIC** (USD100000, sin lifecycle prop): rc0, COMPLETE, experiment `sha256:e42945ff…`, RunID `bt-0c33a51a…`; 3.214.366 records; saldo final 70307,92 USD (realized_net −29692,08; costos 4462,08); residuales declarados. Wall 1025,53s ≤3600 ✓; CPU 1453,90s; RSS 108,36MiB ≤512 ✓. Replay `--experiment`: IDENTICAL (mismos records, RunID `bt-0c33a51a…`).
- **CAMPAIGN** (caja 5000, compra 120 ON_DEMAND, ≤4 cobros): rc0, COMPLETE, HORIZON_REACHED, experiment `sha256:b4ad1f63…`, RunID `bt-c-90151680…`; 3.127.905 records; **6 cuentas: 5 BURNED_RISK_BREACH + 1 ACTIVE_AT_HORIZON; compras aplicadas 6; reemplazos 5; cobros cobrados 1 (1500 USD net); cuenta activa final 101500,12 USD; caja 5000−6×120+1500 = 5780 USD, conciliada**. Wall 668,92s ≤3900 ✓; CPU 964,45s; RSS 109,57MiB ✓. Replays: `--experiment` IDENTICAL y `--result` IDENTICAL (5780→5780); recertificación post-freeze con bin `068a8548`: IDENTICAL.
- **Ancla NQU6** (workload congelado full, monostream): rc0 COMPLETE, 5.172.008 records, wall **1741,82s → target ≤180s FAIL medido y adjudicado** (con contención de CPU declarada; el exceso es de un orden de magnitud). RSS 126,92MiB ✓.
- Denominadores separados: wall de proceso completo (composición+corrida+sellado) vs CPU user+sys vs records de evidencia vs records de mercado consumidos (45488/90589 NQZ5 en BASIC; 0 en NQH6 — fuera de horizonte, no fabricado). Speedup: sin par control/candidato comparable (no autorizado re-optimizar); el 2,2279× run-only de S02 se conserva R_BOUNDED; MIN_SPEEDUP ≥1,5 NOT_DEMONSTRATED.

### Cobertura de mercado y de tests (denominadores separados)

- Cobertura histórica de la ventana solicitada: ReadPlan por stream sellado en cada manifiesto (obligado vs consumido; NQH6 `obligated=null, consumed=0` — no requerido, no fabricado). La ventana solicitada (oct→nov 2025) queda COMPLETA en ambas modalidades con caja conciliada y término HORIZON_REACHED; la cobertura multianual del catálogo completo NO RUN (fuera del presupuesto de la sesión; la frontera de rollover dic-2025 cae fuera de la ventana solicitada y el cruce A→B real queda demostrado por tests E2E).
- Cobertura de tests: comando `cd echo/v3 && go test -count=1 -covermode=atomic -coverprofile=… ./backtester/... ./sdk/futures/...` (perfil y `go tool cover -func` en `measure/backtester-futures.cover` y `measure/backtester-futures-cover-func.txt`). **Global del alcance: 76,3% — el floor 95 NO se alcanza globalmente** (código heredado de BTG incluido en el denominador). Delta S04 por función: catálogo/schedule 83,8–100%; workers 78–100%; C08/C09 79,4–100%; C10/C12 100% (fixtures); processNativeClose 84,3%; SealResult 84,6%; ValidateSealedMultistream 85,7%; DEBAJO del piso: `ReproduceCampaign` 64,8% (ramas de errores/legacy) y ramas defensivas de congelamiento inalcanzables por construcción (assertions de integridad; se declaran, no se maquillan). Coverage del CLI: los tests CLI ejecutan el binario real hijo (no instrumentable por coverprofile) — su cobertura es funcional por E2E con recibos.
- Race: `go test -race` sobre los owners S04 (TOPB/S04/BTXS02 admissions+replay) limpio en 188s. `-race` de la suite completa NO RUN (presupuesto; los owners concurrentes nuevos quedaron cubiertos).

### Recibos, integridad y límites

- Recibo de corridas: `measure/s04-final-runs.md` (SHA256 `c521bdff…262e8a7`); rectificación C05: `measure/perf-contract-rectification-s04.md` (`63643d5f…c5ee1d0`); mandato del verificador: `VERIFIER-MANDATE.md` (`8ebf86a5…4b5f54ee`); RED/GREEN logs en `logs/`.
- Originales S02/S03/PERF_CONTRACT intactos (hashes verificados al inicio y al cierre; bloque 3651/3652 bytes reproducido).
- Límites declarados sin eufemismos: (1) performance gate PARCIAL — anclas NQU6 fallidas (S02 conservado + S04 medido FAIL), speedup no demostrado; (2) cobertura multianual/catálogo completo no corrida; (3) floor 95 no alcanzado globalmente; (4) cruce real de rollover dentro de una corrida final no ocurrió porque la ventana solicitada no lo contiene (mecánica demostrada por E2E); (5) modelo servido del integrador y del verificador UNKNOWN sin recibo; (6) dos fallos preexistentes ambientales (jaeger dev probe, postgres scratch) idénticos en bbbcc1d5.
- Delta propuesto para BTG-PLAN (sólo Primary actualiza el control): S04 EXECUTED con las identidades de arriba; Correctness PASS con evidencia en el alcance probado; Usabilidad integrada PASS con evidencia; Performance PARTIAL (targets de horizonte cumplidos, anclas FAIL, speedup NOT_DEMONSTRATED); Cobertura histórica de la ventana solicitada PASS_BOUNDED; cobertura multianual NOT_RUN; floor95 global NO; READY_FOR_OWNER_ACCEPTANCE no propuesto mientras el gate performance esté parcial; verificación independiente interna devuelta dentro de S04.

### Comprobación independiente (devolución única del verificador, ligada a las SHAs de arriba)

PENDIENTE_AL_CIERRE — el agente fresh-context fue despachado con `VERIFIER-MANDATE.md`; su veredicto se incorpora aquí verbatim al completarse. Si el despacho no devuelve a tiempo, el mandato resuelto queda en el paquete para transporte Owner y el gate de verificación queda ABIERTO (sin fingir ejecución).

## Fuentes

- [[BTG-PLAN]] (control vigente), [[BTX-PERF-ADVERSARIAL]] blob `45fa5af3…` (paquete C01–C12), [[BTX-PERF-DESIGN]] blob `1cedf2e4…` (diseño aceptado con adenda).
- Paquete S04 `aranea/work/btx-perf-s04-20261009/`: echo (rama `codex/btx-perf-s04`), inputs, bin, logs, out-*, measure, VERIFIER-MANDATE.md.
- Paquetes S02/S03 intactos: `aranea/work/btx-perf-s02-20261009/` (contrato congelado `measure/perf-contract-frozen.md` SHA256 `2ee87f94…`), `aranea/work/btx-perf-s03-top-{a,b}-20261009/` (oráculos, SHASUMS verificados `0d8d9732…`/`430ee4e2…`).
- `xKoRx/echo` rama `codex/btx-perf-s02` @ `bbbcc1d5` (baseline de entrada); README canónico `v3/backtester/README.md` actualizado al corte S04.

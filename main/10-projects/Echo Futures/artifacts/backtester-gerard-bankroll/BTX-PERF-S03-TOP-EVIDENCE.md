---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[BTG-PLAN]]"
  - "[[BTX-PERF-DESIGN]]"
  - "[[BTX-PERF-IMPLEMENTATION]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-09"
updated: "2026-10-09"
---

# BTX-PERF-S03-TOP-EVIDENCE

## Propósito

Evidencia del TOP LOCAL independiente dentro de S03: falsificación ejecutada del candidato S02 (`584a3cd9`, HEAD revisado `bbbcc1d5`) sobre Daedalus, ONE-SHOT. Este artefacto aporta pruebas ejecutadas y verificación de recibos para el dictamen GOD independiente de S03 (`BTX-PERF-ADVERSARIAL.md` sigue reservado a ese dictamen); no acepta producto, no reemplaza el gate Primary ni concede FINAL_OWNER_ACCEPTANCE. Producto/originales intactos: el checkout `xKoRx/echo` quedó limpio (0 dirty), y toda prueba propia vivió en un overlay exportado por `git archive bbbcc1d5` (sin `.git`, sin cambios de producto). Modelo ejecutado real: GLM-5.3-Flash (plan `zai-individual-coding-plan`) sobre superficie [[ZCode]]; tokens/costos no expuestos = UNKNOWN. Límites del harness: sesión iniciada 2026-10-09 ~17:15-03:00, ventana histórica NO reiniciada (T0=180min sigue UNKNOWN, no se adoptan 4h); procesos propios terminados al cierre.

## Contenido

### Identidad verificada de la entrada

- Repo `xKoRx/echo` (workspace `~/aranea/work/btx-perf-s02-20261009/echo`): HEAD `bbbcc1d5dc0ed18badae46b4eba1a17822632b60` en `codex/btx-perf-s02`, tree limpio, igual al HEAD leído por Primary; sin delta remoto observable. DAG confirmado: `50250a2b` (08-oct 13:01-03) → `d609ca24` control (09-oct 10:12:06-03) → `584a3cd9` primera optimización (10:28:47-03) → `bbbcc1d5` (11:57:02-03). Compare `584a→bbb`: sólo README + `btx_s02_ring_shared_test.go` (95 inserciones), como adjudicó Primary.
- Binarios: `bin/echo-backtest-control` SHA256 `0db2feae…` (vcs.revision=`d609ca24`, vcs.modified=false) y `bin/echo-backtest-optimized` SHA256 `e5d4860b…` (vcs.revision=`584a3cd9`, vcs.modified=false) — coinciden con lo reportado en el informe S02.
- Binario de verificación propio: `btx-perf-s03-top-20261009/bin/echo-backtest-s03` SHA256 `c9ac66ca…`, construido desde el checkout limpio con stamp `vcs.revision=bbbcc1d5`, `vcs.modified=false`.
- Receipts E1/S02 presentes en `~/aranea/work/btx-perf-s02-20261009/` (inputs, logs, measure, out-*, bin) y cápsula E1 en `~/aranea/work/btx-perf-s01-e1-20261008/` (no regenerada).

### F-S03-01 — Sello PERF_CONTRACT: orden verificado, recibo publicado NO reproducible, timestamp del bloque falso (MAJOR, evidencia)

- Orden `control corregido → sello → primera optimización` VERIFICADO por vía independiente de la fecha escrita: `perf-contract-frozen.md` (mtime 10:16:59-03, entre el commit control 10:12:06 y el commit de optimización 10:28:47) contiene el bloque PERF_CONTRACT byte-idéntico al publicado en Agents-OS (blob `cec0feae` del informe en `534daa16`, presente desde la sync 10:17:03-03 y sin cambios en las syncs posteriores 11:32/11:58).
- El recibo publicado NO es reproducible: el informe declara «SHA256 del bloque PERF_CONTRACT (delimitadores inclusive) = ff320f01…», pero ninguna variedad natural de los bytes del bloque produce ese hash (inner `d00eacdc…`, con fences `7e71aed9…`, con fence+NL `cfa81c17…`, encabezado+bloque `a97700c6…`, CRLF `e1ea9714…`/`c5f73cbd…`). El recibo físico que existe en la evidencia (`measure/perf-contract-seal.sha256`) hash-ea el DOCUMENTO COMPLETO `perf-contract-frozen.md` = `2ee87f94…`, no «el bloque con delimitadores»: el sello publicado queda sin binding verificable a los bytes que dice cubrir.
- El timestamp escrito en el bloque («SEALED_2026-10-09T13:20-03:00») es imposible: los bytes idénticos ya estaban publicados en Agents-OS a las 11:58:03-03 (`5a7d194c`) y congelados localmente a las 10:16:59-03. La hora del sello es falsa por ≥1,5h; el ORDEN sobrevive por mtime+DAG+identidad de bytes, pero la autodescripción del sello no es confiable.
- Adjudicación sugerida para S03/S04: PERF_TARGET_FREEZE cumplido en el orden temporal, `PERF_CONTRACT_SEAL` degradado de REPORTED a SEAL_RECEIPT_NOT_REPRODUCIBLE; re-sello con hash reproducible y timestamp verdadero (contenido del bloque intacto) queda como repair de evidencia S04, sin mover objetivos.
- Comandos: `git cat-file blob 534daa16:main/…BTX-PERF-IMPLEMENTATION.md`, SHA256 sobre 10 variantes del bloque, `stat`/`shasum -a 256` de `measure/perf-contract-frozen.md` y `perf-contract-seal.sha256`. Recibos en el paquete transportable (`logs/seal-verification.txt`).

### F-S03-02 — M1 multicontrato: guard monostream EXECUTED_RED (usabilidad integrada FAIL)

- Requisito: la superficie `experiment` integrada debe aceptar el descriptor común con múltiples streams físicos (diseño §4/§10; el experimento multicontrato es el alcance S02).
- Ejecutado: descriptor válido con DOS streams físicos reales (NQU6 `NQ 09-26.Last.txt` + NQZ5 `NQ 12-25.Last.txt`, mismos archivos derivados Owner read-only de los descriptores `btg-s06-user-oneshot-20261008/inputs/nt/*`), request `echo.backtest.experiment.v1` por AMBAS modalidades → `rc=2`, stderr `experiment requires exactly one physical stream, source declares 2` en BASIC y CAMPAIGN, antes de cualquier procesamiento. Source: `cmd/echo-backtest/experiment.go:65-67` (`len(manifest.Streams) != 1`, uso exclusivo de `Streams[0]`).
- Estado: SOURCE_CONFIRMED + EXECUTED_RED. Severidad: MAJOR (carencia de implementación, no bloqueo externo). La nueva entrada no cumple todavía el experimento integrado; los tests multicontrato del autor (`TestBTXS02MultiContractCatalog…`) cubren el catálogo en memoria, no la entrada física multiplexada. Owner S04: `cmd/echo-backtest/experiment.go` (merge de streams + schedule por contrato) sin quitar el guard para un solo stream.

### F-S03-03 — M2 replay CAMPAIGN: ruta por manifest propia EXECUTED_RED y ruta `--result` muerta por enrutado lazy-footer (MAJOR, amplía M2)

- (a) Ejecutado: campaña mínima REAL por el CLI público (`experiment --input` mode=CAMPAIGN, NQU6 ventana R 2026-07-19T22:01→23:00Z, política de caja completa): COMPLETE, HORIZON_REACHED, caja 5000→4880 (1 compra), 31,8s wall, manifest sellado en `out/f2-campaign/experiment-manifest.json` con `"artifact": null` aunque el artefacto causal existe (`bt-c-cd25…/result.json.gz`). `reproduce --experiment <ese manifest> --nt-source-config …` → `rc=2`, `schema/artifact missing` (source `reproduce.go:59`). La ruta anunciada por README v3/backtester (línea 221: «CAMPAIGN re-compone el driver completo desde la petición sellada» vía `--experiment`) está rota por contrato de source: la rama CAMPAIGN de `cmdExperiment` (líneas 210-215) nunca rellena `ExperimentManifest.Artifact`.
- (b) Inspección acotada adicional EJECUTADA: el enrutado `--result` de `cmdReproduce` (reproduce.go:75-81) lee `Footer.Campaign` inmediatamente después de `ReadResult`; el contrato del lector (`resultwriter.go` ParsedResult) parsea el footer SÓLO cuando el array de records cierra, y `campaignArtifactRequest` (replay.go:38-58) drena a EOF antes de leerlo precisamente por eso. Ejecuciones: `reproduce --result <artefacto de campaña>` SIN `--nt-source-config` produce el error del camino BARE (`nt_source.go:96`), no el guard de campaña (`campaign reproduce requires --nt-source-config`); CON descriptor produce `IDENTICAL` en 55s pero con el verdict BARE (sin `cash_final_baseline/cash_final_replay`): idéntico aquí sólo porque la ventana mínima no contiene reemplazo. Conclusión ejecutada: el replay full-driver de campaña (repair C) es INALCANZABLE por CLI en ambas rutas; sólo existe como API de biblioteca + test con `fixtureFactory` (`btx_s02_campaign_replay_test.go`, fixture fxCorpus/fxSpec — válido como fixture, no como E2E por CLI ni como NQZ5 histórico).
- Estado: EXECUTED_RED. Severidad: MAJOR. Owner S04: sellar `Artifact`+`Runspec` en la rama CAMPAIGN y drenar el footer antes del enrutado (reusar el drain de `campaignArtifactRequest`); no declarar la ruta como existente en README hasta que el E2E por CLI la cubra.

### F-S03-04 — Semántica de resultado y portabilidad (F3): rutas absolutas y rc0 con FAILED EXECUTED_RED (MODERATE)

- Portabilidad: `ExperimentManifest` documenta `Artifact/Runspec` «relative to the experiment out root», pero sella rutas ABSOLUTAS (source: `outcome.Artifact` de `FinalizeLocal`). Ejecutado: BASIC real por CLI (COMPLETE, 36,4s), `mv` del out-root, `reproduce --experiment` desde la nueva ubicación → `rc=2` intentando la ruta ORIGINAL (`no such file or directory`). El manifest no es reubicable; la resolución relativa sólo aplica al `nt_source_config` del request.
- rc: `experiment` selló `execution_state=FAILED` / `WARMUP_INCOMPLETE` (request con warmup deliberadamente insuficiente, 3,2s) y devolvió `rc=0`. Los códigos propuestos por el diseño §10 (0 completo / 1 INCOMPLETE-divergente / 2 inválido) no están implementados en la superficie nueva; el README (línea 340) ya documentaba el equivalente para `run`. Un rc0 no distingue éxito.
- Coverage del manifest: `Coverage` = `From/To/RecordCount` del descriptor fuente (experiment.go:190), no cobertura procesada — SOURCE_CONFIRMED, coherente con la advertencia del mandato.
- Severidad: MODERATE (usabilidad/semántica de operación). Owner S04: rutas relativas + mapeo estado→exit code en `cmdExperiment`.

### F-S03-05 — Performance con recibos: ancla NQU6 BASIC FAIL, MIN_SPEEDUP sólo R, cifras §7.2/§7.3 citadas NO recuperables de artefactos preservados (MAJOR evidencia; adjudicación, no redefinición de contrato)

- Censuras verificadas: `measure/*.rc` = rc124 para ctrl-NQU6full, opt-NQU6full (3 intentos), NQZ5, NQZ5R, probe-NQZ5R/R2; rc0 para control-R y opt-R (los únicos pares COMPLETE). El par R REPORTADO (75,77s→34,01s, 2,23×) tiene recibos físicos (`logs/run-control-R.stderr.log` time -v 1:15.77, `run-opt-R.*`); CPU/RSS de §6.1 no re-meditas (REPORTED, consistente con recibos parciales).
- Ancla NQU6 BASIC ≤180s: FAIL (no NOT_VERIFIED): el candidato censurado supera holgadamente 180s — tres intentos preservados con progreso 1.474.230 / 2.576.162 / 3.524.375 records (últimos ts 2026-07-29T16:44Z / 08-06T19:51Z / 08-19T06:47Z). MIN_SPEEDUP queda demostrado SÓLO para el prefijo R; CAMPAIGN y horizonte completo NOT_DEMONSTRATED (tiempos censurados, sin cociente). La proyección ≈5h es CONSISTENTE con la tasa observada en los intentos preservados (~3.900 records/s estable entre intentos), pero sigue siendo proyección.
- Cifras citadas sin recibo recuperable: §7.2 «en 900s procesa 301.911 records llegando a 2026-07-21T03:43Z» no corresponde a NINGÚN intento preservado (el menor muestra 1,47M records @07-29 — el progreso preservado es MAYOR que el citado); §7.3 «spool 40MB, 49.359 records, warmup hasta 2025-10-21» no corresponde a ningún spool preservado (ver F-S03-06); «4,9 ms/record en warmup NQZ5» es incompatible con los spools preservados (NQZ5: 2,76M records ≈600s ⇒ ~0,22 ms/record). Clasificación: mala clasificación de evidencia en dirección desfavorable al candidato en §7.2 y favorable-declarativa en §7.3; en ambos casos las cifras publicadas no son la evidencia existente. El bloque sellado no se toca; el reporte de resultados S02 queda ajustado por esta adjudicación.
- Pool de preparación: constatado AUSENTE en la ejecución (C=1 en todas las corridas; el informe lo declara omitido por no dominar R) — el contrato lo admite comoWorkers∈{1,2} sujeto a recursos, así que es omisión DECLARADA, no incumplimiento; queda pendiente para el horizonte completo donde la preparación sí puede dominar.

### F-S03-06 — NQZ5 real: el spool preservado CRUZA la transición pass-funded del 2025-11-20 SIN fallo de liberación — la narrativa §7.3 queda contradicha por los propios artefactos (MAJOR, favorable al candidato y no reportado)

- Evidencia ejecutada (inspección de recibos existentes, SIN re-corridas): el spool del candidato NQZ5 (`out-opt-NQZ5/bt-c-e4cc…/attempt-dm0ct6ccs13a…/result.json.gz`, 90MB, rc=124 ≈600s) contiene 2.764.372 records hasta 2025-11-21T21:01:45Z, con `ACCOUNT_REPLACEMENT` @seq 2.009.468 (≈2025-11-18T08:06Z), `ACCOUNT_LIFECYCLE` + `ACCOUNT_CASHFLOW` + `ACCOUNT_CONTEXT_TRANSITION` @2025-11-20T01:55:16Z (la transición pass-funded, clase exacta del defecto E1 4869–4872) y una segunda `ACCOUNT_CONTEXT_TRANSITION` @2025-11-21T00:00Z; cero ocurrencias de `LEDGER_HISTORY_RELEASE_FAILED` / `not current authority`; el stream siguió grabando después de la transición. El spool NQZ5-R (`out-opt-NQZ5R`, 40,5MB) muestra 1.137.892 records hasta 2025-11-07T19:19Z; los probes NQZ5R/R2, 605.914/571.158 records hasta 2025-11-03.
- Consecuencias: (1) repair A tiene evidencia REAL NQZ5 a través de la ventana del defecto dentro de una corrida censurada — no cierra el gate de NQZ5 completo (el horizonte no terminó) pero el requisito «cualquier ejecución futura debe alcanzar la transición real» ya fue alcanzado y preservado; (2) las cifras §7.3 del informe («sólo al 21-oct», «49.359 records», «prefijo excede 240s») no describen ningún artefacto preservado; (3) para S04 la verificación NQZ5 debe partir de estos spools (reconciliación tipada del reemplazo del 18-nov y de la transición del 20-nov, y completar horizonte en ventana dedicada), no re-descubrir desde cero.
- Estado: EXECUTED (lectura de evidencia preservada). Severidad: MAJOR por la brecha entre lo reportado y lo preservado; el sentido del error SUBESTIMA al candidato.

### F-S03-07 — Equivalencia de IDs (109 diferencias): clasificación independiente CORROBORA la afirmación §6.1; comparador del producto tiene dientes y es estricto (verificación cerrada)

- Método: overlay test propio (`btx_s03_top_evidence_diff_test.go`) sobre los artefactos sellados reales del par control→candidato (integridad verificada primero con `VerifyResultIntegrity`, handles frescos para la comparación).
- Resultado: 88.362/88.362 records presentes en ambos; EXACTAMENTE 109 records con ≥1 hoja distinta; 39 rutas de hoja distintas, TODAS de ID/referencia derivados de build (`run_id` ×73, `operation_id`, `order_id`, `provider_execution_id`, `provider_order_ref`, `request_id`, `cause_ref`, `command_id`, `signal_id`, `owner_key`, `coordinate.owner_ref`, `provenance.run_id`, y `payload.detail` = cadena de admisión con hash derivado — inspeccionado); CERO hojas numéricas/de precio/tiempo/kind. El dinero sellado es idéntico. La afirmación «109 diferencias, todas cascada de IDs, cero divergencia semántica» queda CORROBORADA por conteo independiente.
- Dientes del oráculo: inyección de una mutación material (un centavo en `fill_price` de un FILL) en una COPIA del artefacto de control → `CompareRecords` rechaza con `FIELD_MISMATCH payload.fill.fill_price @seq 85929`. El comparador del producto es ESTRICTO (sin normalización de IDs): un replay cross-build por el producto sería DIVERGENT por diseño — la equivalencia de los 109 NO proviene del comparador de producto sino de tooling del autor NO PRESENTE en la evidencia (ni mapa ni recibo recuperable): ese mecanismo queda REPORTED; la clasificación independiente de esta prueba suple la verificación del resultado.
- Estado: EXECUTED (verificación positiva). Sin defecto.

### F-S03-08 — Historial/admisiones y RecentShared/findSource: regresores GREEN, paridad y estabilidad verificadas, sin defecto encontrado en los bordes ejercitados

- Los 9 regresores TestBTXS02 del autor ejecutan PASS en overlay (batch de revisiones, sello de payload contra mutación post-admisión, payload sobrevive aplicación fallida, rechazo de liberación stale y mutación reentrante, multicontrato ×3, replay de campaña con oráculo de caja A→B 4880→4760, ventana RecentShared). El guard del ledger sigue siendo igualdad estricta `revision != l.seq` con rechazo de mutación reentrante (ledger.go:998-1008) — sin sustitución por `<=`.
- Pruebas independientes propias (overlay): (1) ventana `RecentShared` estable byte a byte bajo 40 pushes con evictiones múltiples, ciclo Resize down/up, PushEvict y DiscardForming; (2) paridad del índice `findSource` contra la semántica del scan lineal pre-S02 (transcripción propia del oracle): 840 sondas sobre 120 minutos con applies, idempotencia, conflictos de identidad y discards — 0 divergencias. La propiedad de la ventana transferida sigue siendo disciplina documentada (comentarios) y no tipos: riesgo residual registrado, sin mutación demostrada.
- `-race` focalizado: NOT_RUN aquí (el reporte lo declara PASS en el delta; re-ejecutarlo no cambia ningún repair S04 bajo la regla de gasto).

### F-S03-09 — M5 comparador legacy: obligación omitida CONFIRMADA y el oráculo saltado quedó ejecutado por esta prueba (drift identidad-only)

- SOURCE_CONFIRMED: `compareLegacyCLIArtifacts` hace `t.Logf + return` cuando difieren los RunID, ANTES de comparar ExecutionState, InputSHA256 y bytes del artefacto — ese verde no acredita equivalencia entre builds.
- Prueba independiente con el oráculo conservado (overlay `btx_s03_top_legacy_crossbuild_test.go`): baseline congelado `e2e15a3559` (git archive read-only del checkout limpio) vs actual `bbbcc1d5`, ambos UNSTAMPED con la misma identidad declarada (`legacy-pipeline-compare`), mismos inputs sintéticos: RunID difiere (`bt-c770c805…` vs `bt-cec18f81…`), `input_sha256` difiere, `execution_state` IGUAL, y **0 hojas distintas en los streams de records**. El drift es de contrato de identidad, no de pipeline, en este fixture — la clasificación del autor queda CONFIRMADA y la obligación que su test salteó queda verificada para este par. El weakness del test sigue vigente (aceptaría silenciosamente divergencias reales futuras): restaurar el comparador entre builds consciente de identidad queda como repair de higiene S04 (MINOR).

### F-S03-10 — Ocho fallos «preexistentes»: preexistencia CONFIRMADA, pero «fallos idénticos en los tres worktrees» es FALSO — el candidato reparó 2 (clase CLI-fixture)

- Baseline `50250a2b` (clon s06 limpio): los 8 fallan (recibo `logs/t5-baseline-5025.log`): CampaignCashBurn (esperaba 4 quemadas, hay 5 cuentas con la 5ª ACTIVE_AT_HORIZON), V2IntrabarAdds (adds adversos no disparan, 2 fills), CampaignBurnCashLedger (caja compra/quema), MixedMinuteCapability (falta boundary explícita de modo no-soportado), StructuralReferenceSkip (provider_order_ref difiere ALL vs SKIP a igual timestamp — clase invariancia IDs), FreshProcessDeterminism (exit 2), LargeCorpusStreamingMetrics (exit 2), StandaloneReproduceClosedSpec (exit 2).
- Candidato `bbbcc1d5` (overlay): 5/8 FALLAN con causas IDÉNTICAS a baseline (recibo `logs/t5-candidate-bbb.log`); `TestFreshProcessDeterminism` y `TestBT_S04_StandaloneReproduceClosedSpec` PASAN en candidato y FALLAN en baseline (re-verificado simétrico) — reparados por el fix de identidad declarada del binario (`btxS02DeclaredBuild`); `TestLargeCorpusStreamingMetrics` [resultado en paquete: ver RECIBOS — pendiente al cierre de este documento si no completa]. La frase del informe «fallos idénticos» (triple ejecución) es incorrecta para esa clase; «ni introducidos ni agravados» SÍ queda demostrado. Clasificación de los 5 vivos: los tres primeros son expectativas de fixture del ciclo contable de campaña (correctness de dinero/protección — vigentes para S04), MixedMinuteCapability es contrato de fail-closed, StructuralReferenceSkip es la deuda de invariancia de IDs ya adjudicada por Primary.

### Cobertura

Re-medición NO ejecutada (regla de gasto): el propio informe admite «floor 95% del paquete NO alcanzado» (58,1% agregado con sólo regresores S02; funciones nuevas 69–83%). Ambas lecturas quedan bajo el piso sin importar el denominador exacto: floor95 NOT_MET por admisión del autor; los caminos críticos nuevos quedan con coverage parcial declarado (ramas de fallo integrity/ownership parcialmente ejercitadas). Cobertura total del programa: NOT_DEMONSTRATED.

### Matriz de las cuatro preguntas (verdict RED acotado, sin aprobación final)

| Pregunta | Verdict | Sustento |
|---|---|---|
| Correctness | NOT_CLOSED (avance real) | Repairs A–D GREEN verificados (9/9) + 109 diferencias corroboradas como cascada de IDs + transición NQZ5 real ejecutada sin fallo en spool censurado; 5 fallos de correctness de fixture vivos; horizonte completo no terminado |
| Performance | R-prefix REPORTED+recibos; ancla NQU6 BASIC FAIL; resto NOT_DEMONSTRATED | 2,23× R con recibos; rc124 en todas las censuras; sello con recibo no reproducible y timestamp falso (F-S03-01) |
| Usabilidad integrada | FAIL_SOURCE_CONFIRMED + EXECUTED_RED | F-S03-02/03/04: guard monostream, replay campaña inalcanzable por CLI (ambas rutas), manifest no portable, rc0 con FAILED |
| Cobertura | NOT_MET (floor95) | Admisión del autor + verificación acotada; no re-medido por regla de gasto |

### Revisado vs NO revisado (explícito)

- REVISADO: identidad/dirty/deltas del repo y binarios; sello y recibos de medición R y censuras; F1/F2/F3 ejecutados por CLI público con corpus real; clasificación 109 diffs + inyección material; paridad findSource/estabilidad ventana; comparador legacy cross-build con oráculo conservado; 9 regresores del autor + E2E (checkout real, 71,96s PASS); 8 fallos preexistentes en ambos extremos; spools NQZ5/NQU6full preservados (conteos, ts de frontera, kinds de control, ausencia de fallo de liberación).
- NOT_RUN (obligatoriedad conservada, nunca PASS): NQZ5 horizonte completo y reconciliación tipada del reemplazo 18-nov/transición 20-nov (spools listos para S04); corridas 300/600/900s (prohibidas por mandato); lote 13×; re-perfilado o nuevo benchmark; `-race` focalizado; re-medición de coverage; LONG/SHORT adds/protección, claims/finality, timers, sustitución pública Strategy/MM, rollover con obligaciones y workers (falsificadores restantes de S03); auditoría de la interfaz multicontrato ausente más allá del guard.

### Afirmaciones S02: qué se sostiene y qué no

- SE SOSTIENE: orden del sello por evidencia independiente; 9/9 regresores; 2,23× R con recibos; dinero idéntico y 109 diffs = cascada de IDs (corroborado por conteo propio); comparador con dientes; guard del ledger intacto; paridad findSource/estabilidad ventana; drift legacy identidad-only (verificado con oráculo propio); 5 fallos preexistentes intactos; preexistencia de los 8 en `50250a2b`.
- NO SE SOSTIENE (ajustado por esta evidencia): recibo del sello tal como está publicado (hash no reproducible; timestamp 13:20 falso); «fallos idénticos» en los tres worktrees (2 reparados por el candidato); cifras §7.2 (301.911 @03:43Z) y §7.3 (49.359 @21-oct; 4,9 ms/record) — sin correspondencia con artefacto preservado alguno; «el spool llegó sólo al 21-oct» (los spools preservados llegan al 07-nov y 21-nov cruzando la transición sin fallo); la ruta CAMPAIGN→replay por CLI como existente (rota por ambas rutas); el manifest como reubicable.
- Sigue abierto: FINAL_OWNER_ACCEPTANCE=NOT_GRANTED; los cuatro gates del programa siguen sin aprobarse; RED temprano ≠ S03 completo.

## Fuentes

- Control: [[BTG-PLAN]] (adjudicación Primary M1–M7), [[BTX-PERF-DESIGN]] (adenda Owner), [[BTX-PERF-IMPLEMENTATION]] (informe del autor, blob `cec0feae` @ Agents-OS `534daa16`).
- Source: `xKoRx/echo` @ `bbbcc1d5` (limpio): `cmd/echo-backtest/experiment.go`, `cmd/echo-backtest/reproduce.go`, `experiment.go`, `replay.go`, `reproduce.go`, `result.go`/`resultwriter.go`, `sdk/futures/bars/ring.go`/`builder.go`/`source_bar.go`, `sdk/futures/marketctx/feed.go`, `sdk/futures/accounting/ledger.go`, `native_cli_e2e_test.go`, `btx_s02_*_test.go`, `README.md`.
- Evidencia S02 local (no regenerada): `~/aranea/work/btx-perf-s02-20261009/` (measure/logs/out-*/bin/inputs); E1 `~/aranea/work/btx-perf-s01-e1-20261008/`; corpus NT `~/aranea/work/btg-s06-user-oneshot-20261008/inputs/nt/` y derivados `~/aranea/work/btg-s01-20261006/reports/real-gap-forensics/derived-nt-weekly-v1/` (read-only).
- Paquete transportable de esta verificación (fuera del vault): `~/aranea/work/btx-perf-s03-top-20261009/` — `RECEIPTS.md` con SHA256, `logs/` (F1/F2/F3, sello, T3/T4/T5), `overlay/` (3 tests propios, sin cambios de producto), `bin/echo-backtest-s03` (`c9ac66ca…` @ `bbbcc1d5`), `inputs/` (descriptor 2-stream + requests), `out/` (campaña mínima, BASIC, portabilidad).
